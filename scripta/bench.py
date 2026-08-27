#!/usr/bin/env python3
"""Bench pin-and-build driver (bench-harness delivery GB-U1), run
loop + JSON emitter (GB-U3), stage ladder (GB-U3b), and per-row
power-state capture (GB-U3c).

materialize  detached git worktrees of radix/hosts/gradus at explicit
             hashes into a scratch root outside all repos
build        release faber from the pinned radix worktree
run          sample the pinned bench manifest on the four-stage ladder
             (goal §Stage ladder) and emit
             check-benchmark-regression-format JSON with the
             environment-identity metadata block, per-row `power_state`
             (sampled at each row's execution), and the
             `metadata.power_class` run summary (ea4dd0a3)
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

Run laws (delivery.md GB-U3; goal §Run loop + §Perf-taxonomy):

* the manifest, the bench package, and every `gradus:*` import resolve
  from the pinned gradus worktree inside the scratch root, so a run is
  attached to the recorded triple (reproducibility law); the harness
  itself may run from a dev checkout — the pinned tree is what is timed;
* protocol is pinned at the top stage: 3 discarded warmups + 10 measured
  samples of `faber run`/`faber check` wall time per case, K iterations
  per case from the manifest (benchmark-method §4.3; K calibrated so the
  op loop dominates process startup); lesser ladder stages reduce
  warmup/sample counts and label breadth only — never K;
* the stage ladder (GB-U3b; goal §Stage ladder, operator rulings
  1309af45/88895a02/d3cc0123) controls both knobs — label breadth ×
  repetition depth: smoke (1 label, 1 warmup + 3 samples), dev
  (2 labels, 1/3; the no-flag default), rough (all labels, 1 warmup +
  2 samples — the full-breadth rough pass), full (all labels, 3/10 —
  the byte-preserved GB-U3 protocol, the only gate-comparable shape);
  `--label` picks an explicit subset at the selected stage's sampling
  (iteration-signal only); K never shrinks on any stage, so per-sample
  t/s math is identical across the ladder;
* runtime caps are safety circuit breakers only — never a metric, never
  pass/fail: a sample exceeding `cap_s` is killed at the cap and records
  its valid t/s plus `capped: true`, and the run does not fail;
* sole throughput metric: t/s = (K × units_per_iteration) /
  min(sample wall, cap_s) per sample, median across samples;
  `median_ms` stays the checker's gate quantity;
* a case's value-check line must be observed during sampling or its
  result row records `ok: false` (no zero-artifact greens);
* the emitted JSON keeps the exact checker contract —
  `format_version:"1"` + `results[].label/median_ms` — plus composing
  extra fields; every metadata field records a value or an explicit
  `unavailable`, never a silent drop;
* per-row power-state capture (GB-U3c; goal §Per-row power-state law,
  ruling ea4dd0a3): every result row carries `power_state` (ac|battery|
  mixed|unavailable) from two probes — immediately before the row's
  first warmup and immediately after its last measured sample; agreeing
  probes → that class, ac↔battery disagreement inside the row → mixed,
  non-macOS or any probe miss → unavailable, never a guess.
  `metadata.power_state` stays the start-of-run point observation;
  `metadata.power_class` is the run summary the law keys on (unanimous
  row class, else mixed with power_class_first/_last recorded).

Errors are typed: `bench: <kind>: <message>` on stderr, exit 1.
"""

from __future__ import annotations

import argparse
import json
import os
import platform
import re
import shutil
import signal
import socket
import statistics
import subprocess
import sys
import threading
import time
import tomllib
from datetime import datetime, timezone
from pathlib import Path

REPOS = ("radix", "hosts", "gradus")
TRIPLE_SCHEMA = 1
TRIPLE_FILE = "triple.json"
DEFAULT_MIN_FREE_GB = 10.0
DEFAULT_DISK_FLOOR_GB = 1.0
BYTES_PER_GIB = 1024**3

# GB-U3 run-loop law (benchmark-method §4.3, unchanged by the harness) —
# the full-stage protocol, byte-preserved as the ladder's top stage.
WARMUPS = 3
SAMPLES = 10
CHECKER_FORMAT_VERSION = "1"
BENCH_MANIFEST = Path("bench") / "cases.toml"  # inside the pinned gradus worktree
DEFAULT_CAP_S = 60  # per goal §Perf-taxonomy; overridable per case in the manifest

# Stage ladder (GB-U3b; goal §Stage ladder): both knobs per stage — label
# breadth × repetition depth. Full keeps WARMUPS/SAMPLES above exactly; no
# stage exceeds it, and K (manifest iterations) never shrinks on any stage.
STAGE_LADDER = {
    "smoke": {"number": 1, "warmups": 1, "samples": 3},
    "dev": {"number": 2, "warmups": 1, "samples": 3},
    "rough": {"number": 3, "warmups": 1, "samples": 2},
    "full": {"number": 4, "warmups": WARMUPS, "samples": SAMPLES},
}
STAGE_TOKENS = {
    **{name: name for name in STAGE_LADDER},
    "1": "smoke", "2": "dev", "3": "rough", "4": "full",
}
DEFAULT_STAGE = "dev"  # no-flag run = stage 2 dev (operator default dev mode)
DEFAULT_SMOKE_LABEL = "gemv.f32.320x960"  # cheapest measured (goal table)
DEFAULT_DEV_LABELS = ("gemv.f32.320x960", "carrier.reduce.sum.f32.320x960")

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


# ---------------------------------------------------------------------------
# run — the bench run loop + checker-format JSON emitter (GB-U3)
# ---------------------------------------------------------------------------

CITATIONS = [
    "gradus/docs/benchmark-method.md v1.0.0 §4.3 — 3 warmups / 10 samples / "
    "wall clock, min-median-max",
    "gpu-lessons L1 L2 L4 L12 L13 L17 L21 — "
    "~/work/ianzepp/skills/gpu-lessons/references/laws.md",
    "battery ruling — radix/docs/factory/perf-parity-baseline/evidence/"
    "2026-08-26-metal-m5max-soak-l2000/perf-parity-receipt-v1-2026-08-27-soak.json"
    " (operator ruling; U7 status clause)",
    "gradus/docs/factory/bench-harness/goal.md §Perf-taxonomy — t/s sole "
    "metric; caps circuit breakers; class-(b) not fitting",
    "gradus/docs/factory/bench-harness/delivery.md — unit GB-U3 "
    "(run loop + emitter)",
]


def probe(argv: list[str], cwd: Path | None = None, timeout: float = 10.0) -> str | None:
    """Run one environment-identity probe; None records 'unavailable'."""
    try:
        proc = subprocess.run(
            argv,
            cwd=str(cwd) if cwd else None,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    if proc.returncode != 0:
        return None
    return proc.stdout.strip() or None


def probe_file(path: str) -> str | None:
    try:
        return Path(path).read_text(encoding="utf-8").strip() or None
    except OSError:
        return None


def sysctl(name: str) -> str | None:
    return probe(["sysctl", "-n", name])


def load_manifest(scratch: Path) -> dict:
    """Read bench/cases.toml from the pinned gradus worktree (the run is
    attached to the recorded triple) and fail closed on taxonomy gaps.
    Returns the case list plus the ladder label-breadth fields
    (`smoke_label` / `dev_labels`; goal-table defaults when the pinned
    manifest predates GB-U3b)."""
    path = scratch / "gradus" / BENCH_MANIFEST
    if not path.is_file():
        raise BenchError(
            "manifest-missing",
            f"{path} is missing in the pinned gradus worktree (gradus sha "
            f"predates the GB-U2 bench package?)",
        )
    try:
        data = tomllib.loads(path.read_text(encoding="utf-8"))
    except (ValueError, OSError) as err:
        raise BenchError("manifest-invalid", f"{path}: {err}") from err
    cases = data.get("case")
    if not isinstance(cases, list) or not cases:
        raise BenchError("manifest-invalid", f"{path}: no [[case]] entries")

    seen: set[str] = set()
    for entry in cases:
        if not isinstance(entry, dict):
            raise BenchError("manifest-invalid", f"{path}: [[case]] entry is not a table")
        label = entry.get("label")
        if not isinstance(label, str) or not label:
            raise BenchError("manifest-invalid", f"{path}: [[case]] without a label")
        if label in seen:
            raise BenchError("manifest-invalid", f"{path}: duplicate label {label!r}")
        seen.add(label)
        if entry.get("class") != "fixed-oracle":
            raise BenchError(
                "manifest-invalid", f"{label}: class must be 'fixed-oracle' (v1 taxonomy)"
            )
        route = entry.get("route")
        if route not in ("run", "check"):
            raise BenchError("manifest-invalid", f"{label}: route must be 'run' or 'check'")
        if route == "run" and not isinstance(entry.get("entry"), str):
            raise BenchError("manifest-invalid", f"{label}: run route needs an entry")
        if route == "check" and not isinstance(entry.get("target"), str):
            raise BenchError("manifest-invalid", f"{label}: check route needs a target")
        for field in ("work_unit", "units_per_iteration", "iterations"):
            if field not in entry:
                raise BenchError(
                    "manifest-invalid", f"{label}: missing metric field {field}"
                )
        if not isinstance(entry["units_per_iteration"], int) or entry["units_per_iteration"] < 1:
            raise BenchError(
                "manifest-invalid", f"{label}: units_per_iteration must be a positive int"
            )
        if not isinstance(entry["iterations"], int) or entry["iterations"] < 1:
            raise BenchError("manifest-invalid", f"{label}: iterations must be a positive int")
        cap = entry.get("cap_s", DEFAULT_CAP_S)
        if isinstance(cap, bool) or not isinstance(cap, (int, float)) or cap <= 0:
            raise BenchError("manifest-invalid", f"{label}: cap_s must be a positive number")

    smoke_label = data.get("smoke_label", DEFAULT_SMOKE_LABEL)
    if not isinstance(smoke_label, str) or smoke_label not in seen:
        raise BenchError(
            "manifest-invalid",
            f"{path}: smoke_label {smoke_label!r} is not a manifest label",
        )
    dev_labels = data.get("dev_labels", list(DEFAULT_DEV_LABELS))
    if (
        not isinstance(dev_labels, list)
        or not 1 <= len(dev_labels) <= 2  # dev mode = 1-2 tests at most (ruling 88895a02)
        or any(not isinstance(label, str) or label not in seen for label in dev_labels)
        or len(set(dev_labels)) != len(dev_labels)
    ):
        raise BenchError(
            "manifest-invalid",
            f"{path}: dev_labels {dev_labels!r} must be 1-2 distinct manifest labels",
        )
    return {"cases": cases, "smoke_label": smoke_label, "dev_labels": dev_labels}


def case_command(faber: Path, scratch: Path, case: dict) -> list[str]:
    """The sampled command: `faber run` over the pinned bench package (MIR
    runner, package route — single-file scripts reject kernel imports) or
    `faber check` on the pinned library for check-route labels."""
    if case["route"] == "check":
        target = (scratch / "gradus" / case["target"]).resolve()
        return [str(faber), "check", str(target)]
    package = scratch / "gradus" / "bench"
    return [str(faber), "run", str(package), "--", case["label"], str(case["iterations"])]


def timed_sample(command: list[str], cap_s: float, env: dict, cwd: Path) -> dict:
    """One wall-timed sample. cap_s is a safety circuit breaker only: a
    sample that exceeds it is killed at the cap (whole process group) and
    records capped=true — never a metric, never pass/fail."""
    start = time.monotonic()
    try:
        proc = subprocess.Popen(
            command,
            cwd=str(cwd),
            env=env,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            start_new_session=True,
        )
    except OSError as err:
        raise BenchError("spawn-failed", f"{' '.join(command)}: {err}") from err
    try:
        stdout, stderr = proc.communicate(timeout=cap_s)
        capped = False
    except subprocess.TimeoutExpired:
        capped = True
        try:
            os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
        except OSError:
            proc.kill()
        stdout, stderr = proc.communicate()
    return {
        "wall_s": time.monotonic() - start,
        "capped": capped,
        "returncode": proc.returncode,
        "stdout": stdout or "",
        "stderr": stderr or "",
    }


def check_observed(case: dict, sample: dict) -> bool:
    """The case's value-check line (done_when c). Run route: the case prints
    '<label>: PASS …' and panics on mismatch (GB-U2 check_line). Check
    route: `faber check` exit 0 is the checker's own ok line."""
    if case["route"] == "check":
        return sample["returncode"] == 0
    if sample["returncode"] != 0:
        return False
    label = case["label"]
    return any(
        label in line and "PASS" in line for line in sample["stdout"].splitlines()
    )


def select_labels(
    stage: str, manifest: dict, explicit: list[str] | None
) -> tuple[list[str], str]:
    """Ladder label breadth (goal §Stage ladder): the stage's label set,
    or the explicit `--label` subset at the same sampling. Explicit
    subsets are iteration-signal only — never gate input."""
    if explicit:
        known = {case["label"] for case in manifest["cases"]}
        unknown = [label for label in explicit if label not in known]
        if unknown:
            raise BenchError(
                "label-unknown",
                f"--label {', '.join(unknown)}: not in the pinned manifest "
                f"(labels: {', '.join(sorted(known))})",
            )
        selected: list[str] = []
        for label in explicit:
            if label not in selected:
                selected.append(label)
        return selected, "explicit"
    if stage == "smoke":
        return [manifest["smoke_label"]], "stage"
    if stage == "dev":
        return list(manifest["dev_labels"]), "stage"
    return [case["label"] for case in manifest["cases"]], "stage"


def comparability_note(stage: str, label_mode: str, labels: list[str], cases: list[dict]) -> str:
    """Protocol identity for the GB-U4 wrapper: only the exact full shape
    (stage full, no explicit subset, all manifest labels) is
    gate-comparable; everything else is iteration-signal only."""
    if (
        stage == "full"
        and label_mode == "stage"
        and len(labels) == len(cases)
    ):
        return (
            "gate-comparable: stage full, warmups 3 / samples 10, all "
            "manifest labels — the only gate-comparable shape "
            "(goal §Stage ladder)"
        )
    return (
        "iteration-signal only: recorded protocol is not the full "
        "3/10 all-manifest-label capture shape; the GB-U4 gate wrapper "
        "refuses it as NOT COMPARABLE"
    )


# ---------------------------------------------------------------------
# per-row power-state law (GB-U3c; goal §Per-row power-state law,
# operator ruling ea4dd0a3)
# ---------------------------------------------------------------------

def classify_power(pmset_batt: str | None) -> str | None:
    """Classify one `pmset -g batt` output: 'ac' | 'battery', None on a
    miss (unknown text) — never a guess."""
    if pmset_batt is None:
        return None
    if "AC Power" in pmset_batt:
        return "ac"
    if "Battery Power" in pmset_batt:
        return "battery"
    return None


def probe_power_class() -> str:
    """One power-class probe: 'ac' | 'battery'; 'unavailable' on
    non-macOS or any probe miss — never a guess."""
    if sys.platform != "darwin":
        return "unavailable"
    return classify_power(probe(["pmset", "-g", "batt"])) or "unavailable"


def row_power_state(power_start: str, power_end: str) -> str:
    """Row class from its two probes: agreeing → that class; an ac↔battery
    transition inside the row → 'mixed'; any miss → 'unavailable'."""
    if "unavailable" in (power_start, power_end):
        return "unavailable"
    if power_start != power_end:
        return "mixed"
    return power_start


def power_class_summary(rows: list[dict]) -> dict:
    """Run summary the law keys on: the unanimous row class, else 'mixed'
    with power_class_first/_last recording the first/last row classes."""
    classes = [row["power_state"] for row in rows]
    if not classes:
        return {"power_class": "unavailable"}
    power_class = classes[0] if len(set(classes)) == 1 else "mixed"
    summary: dict = {"power_class": power_class}
    if power_class == "mixed":
        summary["power_class_first"] = classes[0]
        summary["power_class_last"] = classes[-1]
    return summary


def run_case(
    scratch: Path,
    faber: Path,
    case: dict,
    env: dict,
    warmups: int,
    samples: int,
) -> dict:
    label = case["label"]
    cap_s = float(case.get("cap_s", DEFAULT_CAP_S))
    iterations = case["iterations"]
    command = case_command(faber, scratch, case)

    # per-row law: probe immediately before the first warmup …
    power_start = probe_power_class()

    for index in range(warmups):
        sample = timed_sample(command, cap_s, env, scratch)
        state = (
            "capped" if sample["capped"]
            else ("ok" if check_observed(case, sample) else "FAILED")
        )
        print(
            f"bench: {label} warmup {index + 1}/{warmups} "
            f"wall={sample['wall_s']:.3f}s {state}",
            file=sys.stderr,
        )

    units_per_sample = iterations * case["units_per_iteration"]
    samples_list: list[dict] = []
    for index in range(samples):
        sample = timed_sample(command, cap_s, env, scratch)
        sample["observed"] = (not sample["capped"]) and check_observed(case, sample)
        # t/s law (goal §Perf-taxonomy): units produced (K ×
        # units_per_iteration) over min(sample wall, cap_s). A capped sample
        # keeps its valid t/s and is marked; caps never gate anything.
        sample["units_per_s"] = units_per_sample / min(sample["wall_s"], cap_s)
        samples_list.append(sample)
        state = "capped" if sample["capped"] else ("ok" if sample["observed"] else "FAILED")
        print(
            f"bench: {label} sample {index + 1}/{samples} "
            f"wall={sample['wall_s']:.3f}s {state}",
            file=sys.stderr,
        )

    # … and immediately after the last measured sample (ea4dd0a3)
    power_end = probe_power_class()
    power_state = row_power_state(power_start, power_end)

    walls_ms = [sample["wall_s"] * 1000.0 for sample in samples_list]
    failures = [s for s in samples_list if not s["capped"] and not s["observed"]]
    verified = [s for s in samples_list if s["observed"]]
    return {
        "label": label,
        "median_ms": round(statistics.median(walls_ms), 3),
        "min_ms": round(min(walls_ms), 3),
        "max_ms": round(max(walls_ms), 3),
        "samples": samples,
        "iterations": iterations,
        "ok": bool(verified) and not failures,
        "class": case["class"],
        "work_unit": case["work_unit"],
        "throughput": case.get("throughput", "units/s"),
        "units_per_sample": units_per_sample,
        "median_units_per_s": round(
            statistics.median([s["units_per_s"] for s in samples_list]), 6
        ),
        "capped": any(sample["capped"] for sample in samples_list),
        "tier": case.get("tier", "cpu-reference"),
        "power_state": power_state,
    }


def collect_metadata(
    scratch: Path,
    triple: dict,
    faber: Path,
    cases: list[dict],
    stage: str,
    warmups: int,
    samples: int,
    labels: list[str],
    label_mode: str,
) -> dict:
    """Environment-identity block (done_when b). Missing-any-voids-the-claim:
    every field records a value or an explicit 'unavailable'."""
    mac = sys.platform == "darwin"

    os_name = "unavailable"
    if mac:
        product = probe(["sw_vers", "-productVersion"])
        build = probe(["sw_vers", "-buildVersion"])
        if product:
            os_name = f"macOS {product}" + (f" ({build})" if build else "")
    else:
        release = probe_file("/etc/os-release")
        if release:
            for line in release.splitlines():
                if line.startswith("PRETTY_NAME="):
                    os_name = line.split("=", 1)[1].strip('"')
                    break
        else:
            os_name = f"{platform.system()} {platform.release()}".strip() or "unavailable"

    memory = "unavailable"
    mem_raw = sysctl("hw.memsize") if mac else None
    if mem_raw and mem_raw.isdigit():
        memory = f"{int(mem_raw) / BYTES_PER_GIB:.0f} GiB"
    else:
        meminfo = probe_file("/proc/meminfo") or ""
        for line in meminfo.splitlines():
            if line.startswith("MemTotal:"):
                try:
                    memory = f"{int(line.split()[1]) / 2**20:.0f} GiB"
                except (ValueError, IndexError):
                    pass
                break

    # start-of-run point observation only (ea4dd0a3) — the per-row law
    # samples each row at its own execution window (run_case)
    power_state = "unavailable"
    pmset_raw = "unavailable"
    pmset_batt = probe(["pmset", "-g", "batt"]) if mac else None
    if pmset_batt:
        charge_match = re.search(r"(\d+)%", pmset_batt)
        charge = charge_match.group(1) if charge_match else ""
        pmset_full = probe(["pmset", "-g"])
        pmset_raw = "$ pmset -g batt\n" + pmset_batt
        if pmset_full:
            pmset_raw += "\n$ pmset -g\n" + pmset_full
        if "AC Power" in pmset_batt:
            power_state = "ac (pmset-verified"
            power_state += f"; {charge}% charged)" if charge else ")"
        elif "Battery Power" in pmset_batt:
            power_state = "battery (pmset-verified"
            power_state += f"; {charge}%" if charge else ""
            power_state += "; absolutes depressed, ratio-is-signal)"

    cpu = sysctl("machdep.cpu.brand_string") if mac else None
    if not cpu:
        cpuinfo = probe_file("/proc/cpuinfo") or ""
        for line in cpuinfo.splitlines():
            if line.startswith("model name"):
                cpu = line.split(":", 1)[1].strip()
                break
    cpu = cpu or platform.processor() or "unavailable"

    machine_model = sysctl("hw.model") if mac else None
    machine_model = machine_model or probe_file(
        "/sys/devices/virtual/dmi/id/product_name"
    ) or "unavailable"

    rustc = probe(["rustc", "--version"], cwd=scratch / "radix") or "unavailable"

    return {
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "stage": stage,
        "stage_number": STAGE_LADDER[stage]["number"],
        "hostname": platform.node() or socket.gethostname() or "unavailable",
        "machine_model": machine_model,
        "cpu": cpu,
        "cores": (sysctl("hw.ncpu") if mac else None)
        or (str(os.cpu_count()) if os.cpu_count() else "unavailable"),
        "memory": memory,
        "os": os_name,
        "kernel": platform.release() or "unavailable",
        "arch": platform.machine() or "unavailable",
        "power_state": power_state,
        "pmset_raw": pmset_raw,
        "triple": {
            "radix_sha": triple["radix"],
            "hosts_sha": triple["hosts"],
            "gradus_sha": triple["gradus"],
        },
        "faber_binary": {
            "path": str(faber),
            "profile": "release",
            "rustc": rustc,
            "build_command": "cargo build --release -p faber",
            "build_cwd": str(scratch / "radix"),
            "target_dir": str(scratch / "radix" / "target"),
        },
        "protocol": {
            "warmups": warmups,
            "samples": samples,
            "label_selection": {"mode": label_mode, "labels": labels},
            "iterations": {case["label"]: case["iterations"] for case in cases},
            "timer": "wall clock — time.monotonic seconds around the faber "
            "process (benchmark-method §4.3)",
            "route": "faber run — MIR runner, interpreted, package route "
            "(telemetry off; the product path carries the number, gpu-lessons L2)",
            "stdout": "captured per sample to observe each case's "
            "value-check line (one line per run)",
            "throughput_law": "t/s = (K × units_per_iteration) / "
            "min(sample wall, cap_s), median across samples "
            "(goal §Perf-taxonomy)",
            "cap_law": "cap_s is a safety circuit breaker only — never a "
            "metric, never pass/fail; a capped sample records its valid "
            "t/s plus capped=true",
        },
        "citations": CITATIONS,
        "comparability": comparability_note(stage, label_mode, labels, cases),
    }


def cmd_run(args: argparse.Namespace) -> int:
    if args.full and args.stage:
        raise BenchError(
            "stage-conflict", "--full and --stage are mutually exclusive; pick one"
        )
    stage = STAGE_TOKENS[args.stage or ("full" if args.full else DEFAULT_STAGE)]
    spec = STAGE_LADDER[stage]
    warmups, samples = spec["warmups"], spec["samples"]

    scratch = single_scratch(args.scratch)
    triple = load_triple(scratch)
    verify_triple(scratch, triple)
    faber = scratch / "radix" / "target" / "release" / "faber"
    if not (faber.is_file() and os.access(faber, os.X_OK)):
        raise BenchError(
            "no-build", f"{faber} is missing; run `bench build` before `bench run`"
        )
    manifest = load_manifest(scratch)
    cases = manifest["cases"]
    if any(case["route"] == "run" for case in cases) and not (
        scratch / "gradus" / "bench" / "faber.toml"
    ).is_file():
        raise BenchError(
            "no-bench-package",
            f"{scratch / 'gradus' / 'bench'} has no faber.toml (pinned gradus "
            f"predates the GB-U2 bench package)",
        )
    labels, label_mode = select_labels(stage, manifest, args.label)
    selected = [case for case in cases if case["label"] in labels]

    env = os.environ.copy()
    # gradus:* imports resolve to the pinned gradus worktree (check-compile seam).
    env["FABER_LIBRARY_HOME"] = str(scratch)
    # compiled-arm-only seam (runtime_sources.rs); keep the MIR arm deterministic
    env.pop("FABER_SUPPORT_PATH_OVERRIDE", None)

    metadata = collect_metadata(
        scratch, triple, faber, cases, stage, warmups, samples, labels, label_mode
    )
    print(
        f"bench: run stage {stage} ({spec['number']}) — {len(selected)} label(s) "
        f"[{label_mode} selection], {warmups} warmup + {samples} sample(s) per "
        f"label, K per manifest; radix {triple['radix'][:7]} "
        f"hosts {triple['hosts'][:7]} gradus {triple['gradus'][:7]}",
        file=sys.stderr,
    )
    rows = [
        run_case(scratch, faber, case, env, warmups, samples) for case in selected
    ]
    # power_class summarizes the emitted rows (ea4dd0a3) — appended after
    # collect_metadata because only the rows know their classes
    power_class = power_class_summary(rows)
    metadata.update(power_class)
    document = {
        "format_version": CHECKER_FORMAT_VERSION,
        "metadata": metadata,
        "results": rows,
    }
    payload = json.dumps(document, indent=2) + "\n"
    if args.out:
        out_path = Path(args.out)
        if out_path.parent != Path(""):
            out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(payload, encoding="utf-8")
        print(f"bench: wrote {out_path}", file=sys.stderr)
    else:
        sys.stdout.write(payload)

    for row in rows:
        print(
            f"bench: {row['label']} median={row['median_ms']}ms "
            f"min={row['min_ms']}ms max={row['max_ms']}ms "
            f"t/s={row['median_units_per_s']} {row['throughput']} "
            f"capped={row['capped']} ok={row['ok']} power={row['power_state']}",
            file=sys.stderr,
        )
    if power_class["power_class"] == "mixed":
        print(
            f"bench: power_class=mixed "
            f"(first {power_class['power_class_first']}, "
            f"last {power_class['power_class_last']})",
            file=sys.stderr,
        )
    else:
        print(f"bench: power_class={power_class['power_class']}", file=sys.stderr)
    failed = [row["label"] for row in rows if not row["ok"]]
    if failed:
        print(
            f"bench: case-failed: no value-check line observed for "
            f"{', '.join(failed)}",
            file=sys.stderr,
        )
        return 1
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

    run = sub.add_parser(
        "run",
        help="sample the pinned bench manifest on the stage ladder and "
        "emit checker-format JSON with per-row power_state + the "
        "metadata.power_class run summary (ea4dd0a3; default: stage 2 dev)",
    )
    run.add_argument("--scratch", metavar="DIR", help="scratch root to run against")
    run.add_argument(
        "--stage",
        choices=sorted(STAGE_TOKENS),
        default=None,
        metavar="STAGE",
        help=(
            "ladder stage by name or number — smoke|dev|rough|full ≡ 1|2|3|4 "
            "(goal §Stage ladder: smoke 1 label, 1 warmup + 3 samples; dev "
            "2 labels, 1/3; rough all labels, 1 warmup + 2 samples; full "
            "all labels, 3/10, the byte-preserved capture protocol). "
            "Default: dev (stage 2, the operator fast path)"
        ),
    )
    run.add_argument(
        "--full",
        action="store_true",
        help="alias for --stage full — the 3-warmup/10-sample all-label "
        "protocol, the only gate-comparable shape",
    )
    run.add_argument(
        "--label",
        action="append",
        metavar="LABEL",
        help="explicit label subset at the selected stage's sampling "
        "(repeatable; iteration-signal only, never gate input)",
    )
    run.add_argument(
        "--out",
        metavar="FILE",
        help="write the JSON here (default: stdout; progress always goes to stderr)",
    )
    run.set_defaults(fn=cmd_run)

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
