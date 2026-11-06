#!/usr/bin/env python3
"""Exact-math check of decode_step's split GEMV (gemv_part + gemv_fin_residual, P = 64).

The Faber program builds weights and input as exact multiples of 2^-10 on the device:

    w[i, k] = ((7919 i + 104729 k + 5) mod 4096) / 2048                  in [0, 2)
    x[k]    = +/- (((40503 k + 11) mod 2048) + 1) / 2048, negative for k >= n/2

The positive weights make the first half of each row add up and the negative half of x
cancel it, so the sum of absolute products is far above the exact sum (cancellation) and
the f32 partial sums grow past 2^24 units, where rounding occurs.

Every product is an integer count of 2^-22 and fits f32 exactly, so the exact dot product
is a Python integer. A library-chosen reduction order is judged against exact math, not
against another order:

    |faber - exact| <= C * sqrt(n) * 2^-24 * sum(|x_i * w_i|),   C = 4

Route agreement: the Metal and CPU results of the same program agree to
1e-6 * sum(|x_i * w_i|) per row.

    python3 check.py --faber <faber> --library-home <parent of the gradus checkout>
"""
import argparse
import math
import pathlib
import statistics
import struct
import subprocess
import sys
from fractions import Fraction

PACKAGE = pathlib.Path(__file__).resolve().parent
ROWS = 384
CASES = (960, 2560)
SEED_W = 5
SEED_X = 11
C = 4
U = 2.0 ** -24
ROUTE_TOL = 1.0e-6


def weight_units(i, k):
    return (7919 * i + 104729 * k + SEED_W) % 4096


def input_units(k, n):
    magnitude = (40503 * k + SEED_X) % 2048 + 1
    return -magnitude if k >= n // 2 else magnitude


def exact_row(i, n):
    """Exact sum and sum of absolute products, both in units of 2^-22 (Python ints)."""
    total = 0
    magnitude = 0
    for k in range(n):
        product = weight_units(i, k) * input_units(k, n)
        total += product
        magnitude += abs(product)
    return total, magnitude


def f32_round(text):
    """The f32 a shortest round-trip decimal names (the program prints f32 values)."""
    return struct.unpack("<f", struct.pack("<f", float(text)))[0]


def run(faber, library_home, device):
    command = [
        faber, "run", str(PACKAGE),
        "--library-home", str(library_home),
        "--device", device, "--strict-engine",
    ]
    done = subprocess.run(command, capture_output=True, text=True, check=False)
    if done.returncode != 0:
        sys.exit(f"{device}: faber exited {done.returncode}\n{done.stderr}")
    results = {n: [] for n in CASES}
    current = None
    for line in done.stdout.splitlines():
        if line.startswith("case K="):
            current = int(line[len("case K="):])
        elif line.startswith("row "):
            _, index, value = line.split()
            if int(index) != len(results[current]):
                sys.exit(f"{device}: rows out of order at K={current}: {line}")
            results[current].append(f32_round(value))
    for n in CASES:
        if len(results[n]) != ROWS:
            sys.exit(f"{device}: K={n} printed {len(results[n])} rows, expected {ROWS}")
    return results


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--faber", required=True)
    parser.add_argument("--library-home", required=True)
    args = parser.parse_args()

    oracle = {n: [exact_row(i, n) for i in range(ROWS)] for n in CASES}
    routes = {device: run(args.faber, args.library_home, device) for device in ("metal", "cpu")}
    failures = 0

    for device, results in routes.items():
        for n in CASES:
            ratios = []
            cancelling = 0
            for i, (total, magnitude) in enumerate(oracle[n]):
                exact = Fraction(total, 1 << 22)
                bound_scale = math.sqrt(n) * U * (magnitude / (1 << 22))
                err = abs(Fraction(results[n][i]) - exact)
                ratio = float(err) / bound_scale
                ratios.append(ratio)
                if abs(total) * 8 < magnitude:
                    cancelling += 1
                if ratio > C:
                    failures += 1
                    print(f"FAIL {device} K={n} row {i}: err/(sqrt(n)*2^-24*sum|xw|) = {ratio:.3f} > {C}")
            print(f"{device:5s} K={n:4d} rows={ROWS} max={max(ratios):.4f} median={statistics.median(ratios):.4f} "
                  f"bound C={C} rows with |sum| < sum|xw|/8: {cancelling}")

    for n in CASES:
        worst = 0.0
        for i, (_, magnitude) in enumerate(oracle[n]):
            gap = abs(routes["metal"][n][i] - routes["cpu"][n][i]) / (magnitude / (1 << 22))
            worst = max(worst, gap)
            if gap > ROUTE_TOL:
                failures += 1
                print(f"FAIL route K={n} row {i}: |metal - cpu| / sum|xw| = {gap:.3e} > {ROUTE_TOL:.0e}")
        print(f"route K={n:4d} max |metal - cpu| / sum|xw| = {worst:.3e} (tolerance {ROUTE_TOL:.0e})")

    print("PASS" if failures == 0 else f"FAILED ({failures})")
    sys.exit(0 if failures == 0 else 1)


if __name__ == "__main__":
    main()
