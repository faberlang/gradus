#!/usr/bin/env python3
"""Tiny f64 oracle and frozen-tolerance two-device runner for layer_step."""
import hashlib
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
# The tiny starter uses the established decode-step serial-f32 contract.
# Real-shape device parity gets output-specific caps from a calibration pass;
# the accepted cap is frozen at 110% of the measured maximum before validation.
ABS_CAP = 1.0e-5
REL_CAP = 1.0e-4

SHAPES = {
    "tiny": {"D": 4, "QD": 4, "KVD": 2, "F": 6, "H": 2, "C": 3,
             "POS": 1, "DH": 2, "GROUP": 2, "SCALE": 0.5},
    "real": {"D": 960, "QD": 960, "KVD": 320, "F": 2560, "H": 15, "C": 8,
             "POS": 7, "DH": 64, "GROUP": 3, "SCALE": 0.125},
}
SHAPE = "tiny"
D, QD, KVD, F, H, C = 4, 4, 2, 6, 2, 3
POS, DH, GROUP, SCALE = 1, 2, 2, 0.5
EPS, LN_THETA, THETA = 1.0e-5, 11.512925, 100000.0
PACKAGE_DIR = PACKAGE
# Frozen after the real-shape calibration receipt was measured. These caps do
# not adapt to observations from the validation runs.
REAL_CALIBRATION = {
    "hidden": {"max_abs_delta": 2.0, "scale": 4209934.0, "absolute_cap": 2.2},
    "key": {"max_abs_delta": 1.1999999999900979e-05, "scale": 45.431854, "absolute_cap": 1.3199999999891077e-05},
    "value": {"max_abs_delta": 0.0, "scale": 37.80865, "absolute_cap": 4.957856535911561e-06},
}


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


def configure(shape):
    global SHAPE, D, QD, KVD, F, H, C, POS, DH, GROUP, SCALE, PACKAGE_DIR
    SHAPE = shape
    dims = SHAPES[shape]
    D, QD, KVD, F, H, C = (dims[k] for k in ("D", "QD", "KVD", "F", "H", "C"))
    POS, DH, GROUP, SCALE = (dims[k] for k in ("POS", "DH", "GROUP", "SCALE"))
    PACKAGE_DIR = PACKAGE if shape == "tiny" else PACKAGE / "real"


def compare_outputs(left, right, caps):
    measured = {}
    for name in left:
        deltas = [abs(a - b) for a, b in zip(left[name], right[name])]
        cap = caps[name]
        if any(delta > cap for delta in deltas):
            i = max(range(len(deltas)), key=deltas.__getitem__)
            raise AssertionError(f"{name}[{i}] device delta {deltas[i]:.9g} exceeds fixed cap {cap:.9g}")
        measured[name] = max(deltas, default=0.0)
    return measured


def run_device(faber, home, device):
    cmd = [faber, "run", "--library-home", home, "--device", device, str(PACKAGE_DIR)]
    completed = subprocess.run(cmd, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if completed.returncode:
        raise SystemExit(f"{device} run failed (exit {completed.returncode}); no device skips are allowed:\n{completed.stdout}")
    return parse_output(completed.stdout)


def main():
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--shape", choices=SHAPES, default="tiny")
    args = parser.parse_args()
    configure(args.shape)

    faber = os.environ.get("FABER_BIN")
    if not faber or not pathlib.Path(faber).is_file():
        raise SystemExit("set FABER_BIN to the current radix faber executable")
    runs = {}
    with tempfile.TemporaryDirectory(prefix=".decode-layer-pin-home-", dir=ROOT) as home:
        pathlib.Path(home, "gradus").symlink_to(ROOT, target_is_directory=True)
        if SHAPE == "tiny":
            expected = reference()
            for device in ("reference", "metal"):
                observed = run_device(faber, home, device)
                maxima = errors(observed, expected)
                runs[device] = {"max_abs_error": maxima, "output": observed}
                print(f"{device}: layer_step passed; max abs oracle error {max(maxima.values()):.9g}")
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
            receipt_path = PACKAGE / "receipt-tiny.json"
        else:
            caps = {name: values["absolute_cap"] for name, values in REAL_CALIBRATION.items()}
            validation_outputs = {}
            for device in ("reference", "metal"):
                observed = run_device(faber, home, device)
                validation_outputs[device] = observed
                output_bytes = json.dumps(observed, sort_keys=True, separators=(",", ":")).encode()
                runs[device] = {
                    "output_sha256": hashlib.sha256(output_bytes).hexdigest(),
                    "value_count": {name: len(values) for name, values in observed.items()},
                    "sample": {name: values[:4] + values[-4:] for name, values in observed.items()},
                }
            observed_delta = compare_outputs(validation_outputs["reference"], validation_outputs["metal"], caps)
            for device in ("reference", "metal"):
                print(f"{device}: real layer_step passed; compared {sum(runs[device]['value_count'].values())} values")
            receipt = {
                "dimensions": {"D": D, "QD": QD, "KVD": KVD, "F": F, "dh": DH, "group": GROUP, "capacity": C, "position": POS},
                "tolerance": {
                    name: {
                        "absolute": values["absolute_cap"],
                        "basis": "fixed at 1.10 times the measured calibration max, or the f32-epsilon scale floor; not adapted during validation",
                    }
                    for name, values in REAL_CALIBRATION.items()
                },
                "calibration_max_abs_delta": {name: values["max_abs_delta"] for name, values in REAL_CALIBRATION.items()},
                "calibration_max_abs_scale": {name: values["scale"] for name, values in REAL_CALIBRATION.items()},
                "validation_reference_metal_max_abs_delta": observed_delta,
                "devices": runs,
                "result": "pass",
            }
            receipt_path = PACKAGE / "receipt-real.json"

        receipt_path.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n")
    print(f"{SHAPE} layer_step pin passed on reference and metal")


if __name__ == "__main__":
    main()
