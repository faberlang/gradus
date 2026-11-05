#!/usr/bin/env python3
"""Small independent f64 oracle and strict two-device runner for layer_step."""
import json
import math
import os
import pathlib
import re
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[2]
PACKAGE = pathlib.Path(__file__).resolve().parent
# Fixed before this receipt's device run: the existing decode_step numeric
# contract is |error| <= 1e-5 + 1e-4 * |reference| for serial f32 kernels.
ABS_CAP = 1.0e-5
REL_CAP = 1.0e-4

D, QD, KVD, F, H, C = 4, 4, 2, 6, 2, 3
POS, DH, GROUP = 1, 2, 2
EPS, LN_THETA, SCALE, THETA = 1.0e-5, 11.512925, 0.5, 100000.0


def weight(r, c, salt):
    return ((r * 7 + c * 3 + salt * 5) % 17 - 8) * 0.025


def matrix(rows, cols, salt):
    return [[weight(r, c, salt) for c in range(cols)] for r in range(rows)]


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def gemv(w, x):
    return [dot(row, x) for row in w]


def rms(x, gamma):
    inv = 1.0 / math.sqrt(sum(v * v for v in x) / len(x) + EPS)
    return [v * inv * g for v, g in zip(x, gamma)]


def rope_pairs(x, pos):
    out = list(x)
    span = DH // 2
    for head in range(len(x) // DH):
        for p in range(span):
            i = head * DH + p * 2
            angle = pos * math.exp(-(p / span) * LN_THETA)
            c, s = math.cos(angle), math.sin(angle)
            a, b = x[i], x[i + 1]
            out[i], out[i + 1] = a * c - b * s, a * s + b * c
    return out


def reference():
    hin = [((j * 2 - 3) * 0.2) for j in range(D)]
    anorm = [0.8 + j * 0.1 for j in range(D)]
    fnorm = [1.1 - j * 0.05 for j in range(D)]
    wq, wk, wv = matrix(QD, D, 1), matrix(KVD, D, 2), matrix(KVD, D, 3)
    wo, wg, wu, wd = matrix(D, QD, 4), matrix(F, D, 5), matrix(F, D, 6), matrix(D, F, 7)
    kin = [[(1 + r * 3 + c) * 0.1 for c in range(KVD)] for r in range(C)]
    vin = [[-(1 + r * 2 + c) * 0.07 for c in range(KVD)] for r in range(C)]

    normed = rms(hin, anorm)
    q = rope_pairs(gemv(wq, normed), POS)
    k = rope_pairs(gemv(wk, normed), POS)
    v = gemv(wv, normed)
    kin[POS], vin[POS] = k, v

    context = []
    for h in range(H):
        kv_head = h // GROUP
        scores = []
        for c in range(POS + 1):
            scores.append(dot(q[h * DH:(h + 1) * DH], kin[c][kv_head * DH:(kv_head + 1) * DH]) * SCALE)
        peak = max(scores)
        exps = [math.exp(s - peak) for s in scores]
        denom = sum(exps)
        probs = [v / denom for v in exps]
        for d in range(DH):
            context.append(sum(probs[c] * vin[c][kv_head * DH + d] for c in range(POS + 1)))

    h1 = [x + y for x, y in zip(hin, gemv(wo, context))]
    ffn = rms(h1, fnorm)
    gate, up = gemv(wg, ffn), gemv(wu, ffn)
    act = [g / (1.0 + math.exp(-g)) * u for g, u in zip(gate, up)]
    hidden = [x + y for x, y in zip(h1, gemv(wd, act))]
    return {"hidden": hidden, "key": [v for row in kin for v in row], "value": [v for row in vin for v in row]}


def parse_output(text):
    values = {}
    for line in text.splitlines():
        m = re.fullmatch(r"(hidden|key|value)\[([^]]+)\]=([-+0-9.eE]+)", line.strip())
        if not m:
            continue
        name, index, value = m.groups()
        values.setdefault(name, {})[index] = float(value)
    expected_counts = {"hidden": D, "key": C * KVD, "value": C * KVD}
    parsed = {}
    for name, count in expected_counts.items():
        if len(values.get(name, {})) != count:
            raise AssertionError(f"output missing {name} values: {len(values.get(name, {}))}/{count}\n{text}")
        if name == "hidden":
            parsed[name] = [values[name][str(i)] for i in range(D)]
        else:
            parsed[name] = [values[name][f"{r},{c}"] for r in range(C) for c in range(KVD)]
    return parsed


def errors(actual, expected):
    maxima = {}
    for name, ref_values in expected.items():
        deltas = [abs(a - b) for a, b in zip(actual[name], ref_values)]
        allowed = [ABS_CAP + REL_CAP * abs(v) for v in ref_values]
        if any(delta > tol for delta, tol in zip(deltas, allowed)):
            i = max(range(len(deltas)), key=deltas.__getitem__)
            raise AssertionError(f"{name}[{i}] error {deltas[i]:.9g} exceeds fixed cap {allowed[i]:.9g}")
        maxima[name] = max(deltas, default=0.0)
    return maxima


def main():
    faber = os.environ.get("FABER_BIN")
    if not faber or not pathlib.Path(faber).is_file():
        raise SystemExit("set FABER_BIN to the current radix faber executable")
    expected = reference()
    runs = {}
    with tempfile.TemporaryDirectory(prefix=".decode-layer-pin-home-", dir=ROOT) as home:
        pathlib.Path(home, "gradus").symlink_to(ROOT, target_is_directory=True)
        for device in ("reference", "metal"):
            cmd = [faber, "run", "--library-home", home, "--device", device, str(PACKAGE)]
            completed = subprocess.run(cmd, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            if completed.returncode:
                raise SystemExit(f"{device} run failed (exit {completed.returncode}); no device skips are allowed:\n{completed.stdout}")
            observed = parse_output(completed.stdout)
            maxima = errors(observed, expected)
            runs[device] = {"max_abs_error": maxima, "output": observed}
            print(f"{device}: layer_step passed; max abs error {max(maxima.values()):.9g}")
        for name in expected:
            diffs = [abs(a - b) for a, b in zip(runs["reference"]["output"][name], runs["metal"]["output"][name])]
            cap = [ABS_CAP + REL_CAP * abs(v) for v in expected[name]]
            if any(d > t for d, t in zip(diffs, cap)):
                raise SystemExit(f"reference/metal {name} parity exceeds the fixed cap")
        receipt = {
            "dimensions": {"D": D, "QD": QD, "KVD": KVD, "F": F, "dh": DH, "group": GROUP, "capacity": C, "position": POS},
            "tolerance": {"absolute": ABS_CAP, "relative": REL_CAP, "basis": "existing decode_step serial-f32 numeric contract, fixed before the device run"},
            "devices": runs,
            "result": "pass",
        }
        (PACKAGE / "receipt-tiny.json").write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n")
    print("tiny layer_step pin passed on reference and metal")


if __name__ == "__main__":
    main()
