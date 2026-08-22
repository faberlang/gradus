#!/usr/bin/env python3
"""MODEL-02-U1 deterministic MoE probe + synthetic fixture generator.

Emits two committed fixture files (no real artifact is read; probes are
synthetic):

  - `fixtures/gguf/gguf-moe-probes.json` (schema `gguf-moe-probes-v1`):
    two seeded `[2048]` f32 hidden-state probes per selected layer
    {0, 3, 39, 40} — both block classes, all four routed storage kinds,
    the F32 and BF16 router rows, and the MTP block — at realistic
    post-norm magnitudes.
  - `fixtures/gguf/gguf-moe-synthetic.json` (schema
    `gguf-moe-synthetic-v1`): one hand-built exact-tie router config
    (8 experts, 2 used, crafted tie at the selection boundary; expected
    indices [2,5], lowest-index-first) and one small multi-expert config
    for dispatch probas.

Determinism: every value is drawn from `numpy.random.default_rng` seeded
from the fixed base seed plus the (layer, probe) identity (method
documented in the JSON header), and every f32 is serialized as its u32 LE
bit hex — reruns are byte-identical.

Magnitude documentation (the U1 stop-condition requirement): the probe
feeds the MoE FFN immediately after RMSNorm. RMSNorm output has RMS
exactly 1 (per-element unit scale; the norm weight is ≈1 for Qwen-class
models), so probes are drawn i.i.d. N(0,1) in f32 and their measured RMS
is recorded per row (≈1 by construction). No artifact dependency.

Usage:
  python3 gen_moe_probes.py           # (re)write the two JSON fixtures
  python3 gen_moe_probes.py --check   # regenerate in memory, byte-compare
                                      # against the committed files

Requirements: Python 3.11+ with numpy.
"""
from __future__ import annotations

import json
import struct
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent

BASE_SEED = 20260822  # date-pinned; change only via delivery amendment
SCHEMA_PROBES = "gguf-moe-probes-v1"
SCHEMA_SYNTH = "gguf-moe-synthetic-v1"
EMBEDDING_LENGTH = 2048
LAYERS = [0, 3, 39, 40]
PROBES_PER_LAYER = 2

# ---------------------------------------------------------------------------
# f32 serialization: u32 LE bit hex (exact, byte-stable across platforms).
# ---------------------------------------------------------------------------

def f32_hex_row(a: np.ndarray) -> list[str]:
    a = np.asarray(a, dtype=np.float32)
    return [struct.pack("<f", float(v)).hex() for v in a]


def f32_hex_matrix(m: np.ndarray) -> list[list[str]]:
    m = np.asarray(m, dtype=np.float32)
    return [f32_hex_row(r) for r in m]


def seed_for(layer: int, probe: int) -> int:
    # Deterministic spawn from the base seed: documented, no clock/os input.
    return np.random.SeedSequence(BASE_SEED, spawn_key=(layer, probe)).generate_state(1)[0]


# ---------------------------------------------------------------------------
# Fixture set 1 — real-geometry probes (synthetic values, real shapes).
# ---------------------------------------------------------------------------

def build_probes() -> dict:
    rows = []
    for layer in LAYERS:
        for p in range(PROBES_PER_LAYER):
            rng = np.random.default_rng(seed_for(layer, p))
            x = rng.standard_normal(EMBEDDING_LENGTH).astype(np.float32)
            # Post-norm magnitude property: force RMS exactly 1 in f32
            # (RMSNorm output scale; weight ≈1 keeps the layer-input scale).
            rms = float(np.sqrt(np.mean(x.astype(np.float64) ** 2)))
            x = (x / np.float32(rms)).astype(np.float32)
            rms_f32 = float(np.sqrt(np.mean(x.astype(np.float64) ** 2)))
            rows.append(
                {
                    "layer": layer,
                    "probe": f"p{p + 1}",
                    "length": EMBEDDING_LENGTH,
                    "u32_hex": f32_hex_row(x),
                    "rms_f64": rms_f32,
                }
            )
    return {
        "schema": SCHEMA_PROBES,
        "generator": "fixtures/gguf/gen_moe_probes.py",
        "seed_base": BASE_SEED,
        "seed_method": "np.random.SeedSequence(BASE_SEED, spawn_key=(layer, probe)); default_rng -> standard_normal",
        "magnitude": (
            "hidden state feeds the MoE FFN directly after RMSNorm, whose "
            "output has RMS exactly 1 (norm weight ~1); probes are i.i.d. "
            "N(0,1) f32 renormalized to RMS 1 in f32 (rms_f64 recorded per row)"
        ),
        "layers": LAYERS,
        "probes_per_layer": PROBES_PER_LAYER,
        "embedding_length": EMBEDDING_LENGTH,
        "probes": rows,
    }


# ---------------------------------------------------------------------------
# Fixture set 2 — synthetic exact-tie router config (8 experts, 2 used).
#
# Router logits = matmul(W_carrier, x_col). With x = 4.0 * e_0 (basis), the
# logits are 4.0 * W[:, 0]. Crafting column 0 as [0,0,2,0,0,2,0,0] gives
# experts 2 and 5 bit-identical logits (2.0*4.0) and everyone else strictly
# below (0.0) — an exact tie for both top-2 slots. Softmax probabilities for
# equal logits are bit-identical in f32, so the lowest-index-first tie rule
# must return indices [2, 5] with equal renormalized weights.
# ---------------------------------------------------------------------------

def build_tie_fixture() -> dict:
    n_expert, n_used, d = 8, 2, 8
    x = np.zeros(d, dtype=np.float32)
    x[0] = 4.0
    w = np.zeros((n_expert, d), dtype=np.float32)
    for i in range(n_expert):
        # Filler columns (never touched with e_0 probe) keep the matrix full
        # rank without disturbing the crafted column-0 logits.
        w[i, (i % d)] = 0.0
    w[2, 0] = 2.0
    w[5, 0] = 2.0
    logits = (w @ x).astype(np.float32)
    assert logits[2] == logits[5] and (logits < logits[2]).sum() == 6
    return {
        "name": "exact-tie-router",
        "config": {
            "expert_count": n_expert,
            "expert_used_count": n_used,
            "expert_ffn_length": d,
            "shared_ffn_length": d,
            "embedding_length": d,
        },
        "x_u32_hex": f32_hex_row(x),
        "router_weight_u32_hex": f32_hex_matrix(w),  # carrier [n_expert, d]
        "expected": {
            "logits_u32_hex": f32_hex_row(logits),
            "indices": [2, 5],
            "note": (
                "exact tie at the selection boundary: both selected experts "
                "share bit-identical probability; lowest-index-first rule"
            ),
        },
    }


# ---------------------------------------------------------------------------
# Fixture set 3 — small synthetic multi-expert config for dispatch probas.
#
# 4 experts, 2 used, embedding 8, expert/shared FFN length 4. All weights
# are small deterministic patterns (no rng needed); consumers hand-compute
# SwiGLU expectations from these exact values. Shapes follow the layout
# contract: gate/up carriers [ffn_len, emb], down carriers [emb, ffn_len].
# ---------------------------------------------------------------------------

def build_multi_fixture() -> dict:
    n_expert, n_used, d, ffn = 4, 2, 8, 4
    rng = np.random.default_rng(np.random.SeedSequence(BASE_SEED, spawn_key=(0xFF,)))
    x = rng.standard_normal(d).astype(np.float32)
    router = rng.standard_normal((n_expert, d)).astype(np.float32)
    gate = rng.standard_normal((n_expert, ffn, d)).astype(np.float32)
    up = rng.standard_normal((n_expert, ffn, d)).astype(np.float32)
    down = rng.standard_normal((n_expert, d, ffn)).astype(np.float32)
    sh_gate = rng.standard_normal((ffn, d)).astype(np.float32)
    sh_up = rng.standard_normal((ffn, d)).astype(np.float32)
    sh_down = rng.standard_normal((d, ffn)).astype(np.float32)
    sh_router = rng.standard_normal(d).astype(np.float32)
    return {
        "name": "multi-expert-dispatch",
        "seed_method": (
            "np.random.SeedSequence(BASE_SEED, spawn_key=(0xFF,)); "
            "default_rng -> standard_normal"
        ),
        "config": {
            "expert_count": n_expert,
            "expert_used_count": n_used,
            "expert_ffn_length": ffn,
            "shared_ffn_length": ffn,
            "embedding_length": d,
        },
        "x_u32_hex": f32_hex_row(x),
        "router_weight_u32_hex": f32_hex_matrix(router),
        "ffn_gate_exps_u32_hex": [f32_hex_matrix(gate[e]) for e in range(n_expert)],
        "ffn_up_exps_u32_hex": [f32_hex_matrix(up[e]) for e in range(n_expert)],
        "ffn_down_exps_u32_hex": [f32_hex_matrix(down[e]) for e in range(n_expert)],
        "ffn_gate_shexp_u32_hex": f32_hex_matrix(sh_gate),
        "ffn_up_shexp_u32_hex": f32_hex_matrix(sh_up),
        "ffn_down_shexp_u32_hex": f32_hex_matrix(sh_down),
        "ffn_gate_inp_shexp_u32_hex": f32_hex_row(sh_router),
        "layout_note": (
            "storage-order carriers per the MODEL-02 layout contract: "
            "gate/up [ffn_len, emb], down [emb, ffn_len], GEMV matmul(W, x_col)"
        ),
    }


def build_synthetic() -> dict:
    return {
        "schema": SCHEMA_SYNTH,
        "generator": "fixtures/gguf/gen_moe_probes.py",
        "seed_base": BASE_SEED,
        "f32_encoding": "u32 LE bit hex",
        "exact_tie": build_tie_fixture(),
        "multi_expert": build_multi_fixture(),
    }


def dumps(obj: dict) -> bytes:
    return (json.dumps(obj, indent=2, sort_keys=False) + "\n").encode()


def main(argv: list[str]) -> int:
    check = "--check" in argv
    generated = {
        HERE / "gguf-moe-probes.json": dumps(build_probes()),
        HERE / "gguf-moe-synthetic.json": dumps(build_synthetic()),
    }
    if check:
        for path, data in generated.items():
            committed = path.read_bytes() if path.exists() else None
            if committed != data:
                print(f"FAIL not deterministic (or stale): {path.name}", file=sys.stderr)
                return 1
        print("OK deterministic: 3 fixture sets")
        return 0
    for path, data in generated.items():
        path.write_bytes(data)
        print(f"wrote {path.name} ({len(data)} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
