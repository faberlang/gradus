#!/usr/bin/env python3
"""Wall-clock a compiled Gradus binary between stdout markers.

Does not modify the binary. Timestamps every stdout line; reports intervals
between named markers plus process lifetime. Used for the llama.cpp baseline
receipt (handle f8fce797) so prefill time excludes GGUF load and top-k scan.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
import time
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", required=True, help="receipt text path")
    parser.add_argument("cmd", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    cmd = args.cmd[1:] if args.cmd[:1] == ["--"] else args.cmd
    if not cmd:
        print("usage: time_markers.py --out receipt.txt -- <cmd...>", file=sys.stderr)
        return 2

    out_path = Path(args.out)
    t0 = time.perf_counter()
    lines: list[tuple[float, str]] = []
    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
    )
    assert proc.stdout is not None
    for raw in proc.stdout:
        now = time.perf_counter() - t0
        text = raw.rstrip("\n")
        lines.append((now, text))
        print(f"[{now:10.3f}s] {text}", flush=True)
    rc = proc.wait()
    total = time.perf_counter() - t0

    def first(prefix: str) -> float | None:
        for ts, text in lines:
            if text.startswith(prefix):
                return ts
        return None

    markers = {
        "admit": first("admit:"),
        "tokenizer": first("tokenizer:"),
        "load_start": first("loading stored-weight views"),
        "loaded_embed": first("loaded embed+norm"),
        "loaded_layer0": first("loaded layer 0"),
        "loaded_layer31": first("loaded layer 31"),
        "forward_start": first("forward start"),
        "forward_done": first("forward done"),
        "decode_prompt0": first("decode_step prompt pos=0"),
        "decode_prompt8": first("decode_step prompt pos=8"),
        "first_sampled": first("first_sampled="),
        "decode_gen1": first("decode_step generate pos="),
        "generated": first("generated="),
        "prefill_verdict": first("PREFILL:"),
        "decode_verdict": first("DECODE:"),
    }

    def delta(a: str, b: str) -> str:
        ta, tb = markers[a], markers[b]
        if ta is None or tb is None:
            return "n/a"
        return f"{tb - ta:.3f}"

    report = []
    report.append(f"cmd={' '.join(cmd)}")
    report.append(f"exit={rc}")
    report.append(f"total_s={total:.3f}")
    for name, ts in markers.items():
        report.append(f"marker.{name}={ts if ts is None else f'{ts:.3f}'}")
    report.append(f"interval.load_s={delta('load_start', 'loaded_layer31')}")
    report.append(f"interval.prefill_forward_s={delta('forward_start', 'forward_done')}")
    report.append(f"interval.decode_prompt_9steps_s={delta('decode_prompt0', 'first_sampled')}")
    report.append(f"interval.decode_generate_s={delta('decode_gen1', 'generated')}")
    report.append(f"interval.after_forward_to_verdict_s={delta('forward_done', 'prefill_verdict')}")
    text = "\n".join(report) + "\n"
    out_path.write_text(text)
    print(text, end="")
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
