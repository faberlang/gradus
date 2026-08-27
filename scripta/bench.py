#!/usr/bin/env python3
"""Bench pin-and-build driver (bench-harness delivery GB-U1).

materialize  detached git worktrees of radix/hosts/gradus at explicit
             hashes into a scratch root outside all repos
build        release faber from the pinned radix worktree
clean        worktree remove --force + prune in each source repo, then
             scratch-root removal, so registrations never accumulate

Laws (gradus/docs/factory/bench-harness/delivery.md GB-U1):

* scratch root defaults to <workspace>/.bench/gradus/<r7>-<h7>-<g7>/
  where <workspace> is the parent of this gradus checkout; it is never
  allowed inside one of the three source repos;
* pinning is fail-closed: a hash that does not resolve is a typed
  error, and every worktree HEAD is verified against the requested
  hash after checkout;
* the release build owns its target dir: ambient CARGO_TARGET_DIR is
  stripped for the child, never set or shared (container AGENTS.md
  cargo-isolation law);
* ENOSPC guard: free space is checked before the build and monitored
  while cargo runs; below the floor the build is stopped and reported,
  not wedged;
* clean is the only teardown: `git worktree remove --force` per
  worktree, `git worktree prune` in each source repo, then scratch-root
  removal, verified registration-free before exit.

Errors are typed: `bench: <kind>: <message>` on stderr, exit 1.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import signal
import subprocess
import sys
import threading
import time
from datetime import datetime, timezone
from pathlib import Path

REPOS = ("radix", "hosts", "gradus")
TRIPLE_SCHEMA = 1
TRIPLE_FILE = "triple.json"
DEFAULT_MIN_FREE_GB = 10.0
DEFAULT_DISK_FLOOR_GB = 1.0
BYTES_PER_GIB = 1024**3

SCRIPT = Path(__file__).resolve()
GRADUS_ROOT = SCRIPT.parents[1]
WORKSPACE = SCRIPT.parents[2]
BENCH_ROOT = WORKSPACE / ".bench" / "gradus"


class BenchError(Exception):
    """A typed, fail-closed driver error."""

    def __init__(self, kind: str, message: str):
        super().__init__(message)
        self.kind = kind


def source_repo(name: str) -> Path:
    path = WORKSPACE / name
    if not (path / ".git").exists():
        raise BenchError(
            "bad-workspace",
            f"expected {name} checkout at {path} (sibling of the gradus "
            f"checkout containing {SCRIPT})",
        )
    return path


def run_git(repo: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess:
    proc = subprocess.run(
        ["git", "-C", str(repo), *args],
        capture_output=True,
        text=True,
    )
    if check and proc.returncode != 0:
        detail = proc.stderr.strip() or proc.stdout.strip()
        raise BenchError("git-failed", f"git -C {repo} {' '.join(args)}: {detail}")
    return proc


def resolve_commit(repo: Path, name: str, ref: str) -> str:
    proc = run_git(repo, "rev-parse", "--verify", f"{ref}^{{commit}}", check=False)
    if proc.returncode != 0:
        raise BenchError(
            "hash-unresolved",
            f"{name}: {ref!r} does not resolve to a commit in {repo}",
        )
    sha = proc.stdout.strip().lower()
    if len(sha) != 40 or any(c not in "0123456789abcdef" for c in sha):
        raise BenchError("hash-unresolved", f"{name}: {ref!r} resolved to {sha!r}")
    return sha


def default_scratch(triple: dict[str, str]) -> Path:
    stem = "-".join(triple[name][:7] for name in REPOS)
    return BENCH_ROOT / stem


def guard_scratch_outside_repos(scratch: Path) -> None:
    for name in REPOS:
        repo = source_repo(name).resolve()
        if scratch == repo or scratch.is_relative_to(repo):
            raise BenchError(
                "scratch-inside-repo",
                f"scratch root {scratch} is inside source repo {repo}",
            )


def resolve_scratch_candidates(explicit: str | None) -> list[Path]:
    if explicit:
        return [Path(explicit).resolve()]
    if not BENCH_ROOT.is_dir():
        return []
    return sorted(path for path in BENCH_ROOT.iterdir() if path.is_dir())


def single_scratch(explicit: str | None) -> Path:
    candidates = resolve_scratch_candidates(explicit)
    if not candidates:
        raise BenchError(
            "no-scratch",
            f"no scratch root under {BENCH_ROOT}; run `bench materialize` "
            f"first or pass --scratch",
        )
    if len(candidates) > 1:
        listing = ", ".join(str(path) for path in candidates)
        raise BenchError(
            "ambiguous-scratch",
            f"multiple scratch roots under {BENCH_ROOT}: {listing}; pass --scratch",
        )
    return candidates[0]


def load_triple(scratch: Path) -> dict:
    path = scratch / TRIPLE_FILE
    if not path.is_file():
        raise BenchError(
            "no-triple",
            f"{path} is missing; run `bench materialize` before build/clean",
        )
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except ValueError as err:
        raise BenchError("no-triple", f"{path}: not valid JSON ({err})") from err
    for name in REPOS:
        if not isinstance(data.get(name), str):
            raise BenchError("no-triple", f"{path}: missing {name} hash")
    return data


def verify_triple(scratch: Path, triple: dict) -> None:
    for name in REPOS:
        worktree = scratch / name
        if not (worktree / ".git").exists():
            raise BenchError(
                "no-worktree", f"{worktree} is not a git worktree; re-materialize"
            )
        got = run_git(worktree, "rev-parse", "HEAD").stdout.strip().lower()
        if got != triple[name]:
            raise BenchError(
                "hash-mismatch",
                f"{name}: worktree HEAD {got} != pinned {triple[name]} "
                f"({scratch})",
            )


def free_bytes(path: Path) -> int:
    stat = os.statvfs(path)
    return stat.f_bavail * stat.f_frsize


def cmd_materialize(args: argparse.Namespace) -> int:
    triple: dict[str, str] = {}
    for name in REPOS:
        repo = source_repo(name)
        ref = getattr(args, name) or "HEAD"
        triple[name] = resolve_commit(repo, name, ref)

    scratch = (
        Path(args.scratch).resolve() if args.scratch else default_scratch(triple)
    )
    guard_scratch_outside_repos(scratch)
    if scratch.exists() and any(scratch.iterdir()):
        raise BenchError(
            "scratch-not-empty",
            f"{scratch} exists and is not empty; run "
            f"`bench clean --scratch {scratch}` first",
        )

    for name in REPOS:
        print(f"bench: pin {name} {triple[name]}")
    print(f"bench: scratch root {scratch}")
    scratch.mkdir(parents=True, exist_ok=True)

    try:
        for name in REPOS:
            repo = source_repo(name)
            worktree = scratch / name
            proc = run_git(
                repo,
                "worktree",
                "add",
                "--detach",
                str(worktree),
                triple[name],
                check=False,
            )
            if proc.returncode != 0:
                detail = proc.stderr.strip() or proc.stdout.strip()
                raise BenchError(
                    "worktree-add-failed", f"{name}: git worktree add: {detail}"
                )
            got = run_git(worktree, "rev-parse", "HEAD").stdout.strip().lower()
            if got != triple[name]:
                raise BenchError(
                    "hash-mismatch",
                    f"{name}: worktree HEAD {got} != requested {triple[name]}",
                )
            print(f"bench: {name} worktree ok at {worktree}")
    except BenchError as err:
        raise BenchError(
            err.kind,
            f"{err}; partial scratch remains at {scratch} — run "
            f"`bench clean --scratch {scratch}` before retrying",
        ) from err

    payload = {
        "schema": TRIPLE_SCHEMA,
        "created_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        **{name: triple[name] for name in REPOS},
    }
    (scratch / TRIPLE_FILE).write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(f"bench: materialize ok; next: bench build --scratch {scratch}")
    return 0


def cmd_build(args: argparse.Namespace) -> int:
    scratch = single_scratch(args.scratch)
    triple = load_triple(scratch)
    verify_triple(scratch, triple)
    radix_worktree = scratch / "radix"

    if shutil.which("cargo") is None:
        raise BenchError("cargo-missing", "cargo not found on PATH")

    min_free = args.min_free_gb * BYTES_PER_GIB
    free = free_bytes(scratch)
    if free < min_free:
        raise BenchError(
            "low-disk",
            f"{free / BYTES_PER_GIB:.1f} GiB free on {scratch} is below the "
            f"{args.min_free_gb:g} GiB build requirement; free space or "
            f"lower --min-free-gb",
        )
    print(
        f"bench: disk guard ok — {free / BYTES_PER_GIB:.1f} GiB free "
        f"(min {args.min_free_gb:g} GiB, floor {args.disk_floor_gb:g} GiB)"
    )

    env = os.environ.copy()
    for var in ("CARGO_TARGET_DIR", "CARGO_BUILD_TARGET_DIR"):
        env.pop(var, None)

    command = ["cargo", "build", "--release", "-p", "faber"]
    print(f"bench: building pinned radix {triple['radix']} in {radix_worktree}")
    print(f"bench: $ {' '.join(command)}")

    floor = args.disk_floor_gb * BYTES_PER_GIB
    tripped: list[int] = []
    proc = subprocess.Popen(command, cwd=str(radix_worktree), env=env, start_new_session=True)
    stop = threading.Event()

    def watch_disk() -> None:
        while not stop.wait(5.0):
            try:
                free_now = free_bytes(scratch)
            except OSError:
                continue
            if free_now < floor:
                tripped.append(free_now)
                try:
                    os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
                except OSError:
                    pass
                return

    watcher = threading.Thread(target=watch_disk, daemon=True)
    watcher.start()
    started = time.monotonic()
    code = proc.wait()
    stop.set()
    watcher.join()

    if tripped:
        raise BenchError(
            "low-disk",
            f"free space fell below {args.disk_floor_gb:g} GiB during the "
            f"build (last seen {tripped[0] / BYTES_PER_GIB:.2f} GiB); cargo "
            f"was stopped (exit {code}) — free space, then re-run",
        )
    if code != 0:
        raise BenchError(
            "build-failed",
            f"cargo build --release -p faber exited {code} in {radix_worktree}",
        )

    faber_bin = radix_worktree / "target" / "release" / "faber"
    if not (faber_bin.is_file() and os.access(faber_bin, os.X_OK)):
        raise BenchError(
            "build-missing-binary",
            f"expected executable {faber_bin} after a successful build",
        )
    print(f"bench: build ok in {time.monotonic() - started:.1f}s -> {faber_bin}")
    print(
        f"bench: verify with: FABER_LIBRARY_HOME={scratch} "
        f"{faber_bin} doctor"
    )
    return 0


def clean_one(scratch: Path) -> None:
    print(f"bench: clean {scratch}")
    for name in REPOS:
        repo = source_repo(name)
        worktree = scratch / name
        if worktree.exists():
            proc = run_git(
                repo, "worktree", "remove", "--force", str(worktree), check=False
            )
            if proc.returncode != 0:
                detail = proc.stderr.strip() or proc.stdout.strip()
                print(f"bench: {name}: worktree remove failed, continuing: {detail}")
        run_git(repo, "worktree", "prune", check=False)

    if scratch.exists():
        shutil.rmtree(scratch)
    if scratch.exists():
        raise BenchError("scratch-remove-failed", f"could not remove {scratch}")

    residual = []
    for name in REPOS:
        repo = source_repo(name)
        listing = run_git(repo, "worktree", "list", "--porcelain").stdout
        for line in listing.splitlines():
            if not line.startswith("worktree "):
                continue
            path = Path(line[len("worktree ") :])
            if path.is_relative_to(scratch):
                residual.append(f"{name}: {path}")
    if residual:
        raise BenchError(
            "residual-registration",
            f"scratch registrations survived clean: {'; '.join(residual)}",
        )
    print(f"bench: clean ok — {scratch} gone, no registrations in {', '.join(REPOS)}")


def cmd_clean(args: argparse.Namespace) -> int:
    if args.all:
        targets = resolve_scratch_candidates(args.scratch)
        if not targets:
            print(f"bench: no scratch roots under {BENCH_ROOT}")
            return 0
    else:
        targets = [single_scratch(args.scratch)]
    for scratch in targets:
        clean_one(scratch)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="bench",
        description="Bench pin-and-build driver: pin the radix/hosts/gradus "
        "triple into a scratch root, build the pinned faber, tear down "
        "clean. Errors are typed (`bench: <kind>: <message>`, exit 1).",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    materialize = sub.add_parser(
        "materialize",
        help="detached worktrees of radix/hosts/gradus at pinned hashes",
    )
    for name in REPOS:
        materialize.add_argument(
            f"--{name}",
            metavar="SHA",
            help=f"{name} commit hash (default: {name} source HEAD)",
        )
    materialize.add_argument(
        "--scratch",
        metavar="DIR",
        help=f"scratch root (default: {BENCH_ROOT}/<r7>-<h7>-<g7>)",
    )
    materialize.set_defaults(fn=cmd_materialize)

    build = sub.add_parser(
        "build", help="cargo build --release -p faber in the pinned radix"
    )
    build.add_argument("--scratch", metavar="DIR", help="scratch root to build in")
    build.add_argument(
        "--min-free-gb",
        type=float,
        default=DEFAULT_MIN_FREE_GB,
        metavar="N",
        help=f"required free space before the build (default {DEFAULT_MIN_FREE_GB:g})",
    )
    build.add_argument(
        "--disk-floor-gb",
        type=float,
        default=DEFAULT_DISK_FLOOR_GB,
        metavar="N",
        help=(
            "free-space floor watched during the build; below it cargo is "
            f"stopped and reported (default {DEFAULT_DISK_FLOOR_GB:g})"
        ),
    )
    build.set_defaults(fn=cmd_build)

    clean = sub.add_parser(
        "clean", help="remove worktrees, prune registrations, delete the scratch root"
    )
    clean.add_argument("--scratch", metavar="DIR", help="scratch root to tear down")
    clean.add_argument(
        "--all",
        action="store_true",
        help=f"tear down every scratch root under {BENCH_ROOT}",
    )
    clean.set_defaults(fn=cmd_clean)

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return args.fn(args)
    except BenchError as err:
        print(f"bench: {err.kind}: {err}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("bench: interrupted", file=sys.stderr)
        return 130


if __name__ == "__main__":
    sys.exit(main())
