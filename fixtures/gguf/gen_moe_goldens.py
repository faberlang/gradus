#!/usr/bin/env python3
"""MODEL-02-U2 independent MoE oracle: goldens generator.

The pinned-identity oracle for the `gradus:model/moe` surface
(`pml5-gguf-m2-moe-router-delivery-2026-08-22.md` §M2-U2):

  (a) reads the real Qwen3.6-35B-A3B artifact read-only and verifies the
      pinned identity (SHA-256 + length — never committed, never copied);
  (b) dequantizes the router / routed-expert / shared-expert tensors with
      llama.cpp `ggml/src/ggml-quants.c` @ `a957b7747` semantics
      {F32, BF16, Q4_K, Q5_K, Q6_K, Q8_0} via the committed
      `gen_dequant_goldens.py` kernels;
  (c) computes the exact delivery-§2 MoE math in numpy f32 for every
      (layer, probe) — layers 0, 3, 39, 40 × 2 probes — plus a strict-f64
      pass for the band floor, and the U1 synthetic exact-tie router.

Outputs (committed):
  - `fixtures/gguf/gguf-moe-goldens.json` (schema `gguf-moe-goldens-v1`):
    per (layer, probe): full logits [256], probabilities [256], top-8
    indices, 8 renormalized weights, per-selected-expert intermediates
    h_e [512] + outputs [2048], shared-expert output [2048], gated shared
    output [2048], final FFN output [2048]; plus the synthetic tie row
    (indices [2, 5]).
  - `fixtures/gguf/gguf-moe-goldens-oracle.md` (commands, identity, pin,
    Δ derivation: Δ = clamp(10·R, 1e-5, 5e-4) where
    R = max |f32_ref − f64_ref| over the final FFN outputs).

Determinism: reruns are byte-identical (f32 serialized as u32 LE bit hex;
fixed JSON layout; no clock/os input beyond the pinned artifact path).

Usage:
  python3 gen_moe_goldens.py [--check]   # --check regenerates in memory,
                                        # byte-compares the committed files
Artifact path (operator-local, never committed):
  default /Users/ianzepp/ai/models/Qwen3.6-35B-A3B-UD-Q4_K_M.gguf,
  override with the GGUF_MOE_ARTIFACT env var.

Requirements: Python 3.11+ with numpy.
"""
from __future__ import annotations

import hashlib
import json
import os
import struct
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from gen_dequant_goldens import TYPE_BLOCK, TYPE_NAME, dequant_block  # noqa: E402

# ---------------------------------------------------------------------------
# Pinned identity + frozen geometry (delivery §2 frozen semantics).
# ---------------------------------------------------------------------------

ARTIFACT_DEFAULT = "/Users/ianzepp/ai/models/Qwen3.6-35B-A3B-UD-Q4_K_M.gguf"
ARTIFACT_SHA256 = "0b21525e972670ed59e1812e170b27c26355381f0656ecc4e25617ece7dac58b"
ARTIFACT_LENGTH = 22_663_387_424
LLAMA_CPP_PIN = "a957b7747"

LAYERS = [0, 3, 39, 40]
N_EXPERT = 256
N_EXPERT_USED = 8
EXPERT_FFN = 512
SHARED_FFN = 512
EMBED = 2048
ALLOWED_KINDS = {"F32", "BF16", "Q4_K", "Q5_K", "Q6_K", "Q8_0"}

BAND_CAP = 5e-4        # gradus forward band (numeric-policy v1.0.0)
MATMUL_FLOOR = 1e-5    # matmul family floor
REPLACE_EPS = np.float32(6.103515625e-5)  # llama.cpp norm_w guard (2^-14)

SCHEMA = "gguf-moe-goldens-v1"

# ---------------------------------------------------------------------------
# f32 serialization (u32 LE bit hex — byte-stable across platforms).
# ---------------------------------------------------------------------------

def f32_hex_row(a) -> list[str]:
    # Same convention as gguf-moe-probes.json / gguf-moe-synthetic.json:
    # struct.pack('<f') byte dump (u32 LE bit hex).
    a = np.asarray(a, dtype=np.float32)
    return [struct.pack("<f", float(v)).hex() for v in a]


def hex_row_f32(row: list[str]) -> np.ndarray:
    return np.asarray(
        [struct.unpack("<f", bytes.fromhex(h))[0] for h in row], dtype=np.float32
    )

# ---------------------------------------------------------------------------
# Minimal read-only GGUF v3 reader (metadata KV + tensor info + windows).
# ---------------------------------------------------------------------------

GGUF_TYPES = {}
GGUF_V3 = 3


def _read_str(f) -> str:
    (n,) = struct.unpack("<Q", f.read(8))
    return f.read(n).decode("utf-8")


def _read_scalar(f, t: int):
    if t == 0:
        return struct.unpack("<B", f.read(1))[0]
    if t == 1:
        return struct.unpack("<b", f.read(1))[0]
    if t == 2:
        return struct.unpack("<H", f.read(2))[0]
    if t == 3:
        return struct.unpack("<h", f.read(2))[0]
    if t == 4:
        return struct.unpack("<I", f.read(4))[0]
    if t == 5:
        return struct.unpack("<i", f.read(4))[0]
    if t == 6:
        return struct.unpack("<f", f.read(4))[0]
    if t == 7:
        return bool(f.read(1)[0])
    if t == 8:
        return _read_str(f)
    if t == 10:
        return struct.unpack("<Q", f.read(8))[0]
    if t == 11:
        return struct.unpack("<q", f.read(8))[0]
    if t == 12:
        return struct.unpack("<d", f.read(8))[0]
    raise ValueError(f"unsupported gguf value type {t}")


def parse_gguf(path: Path):
    """Return (metadata, {name: (ggml_type, [ne...], abs_data_offset)})."""
    f = open(path, "rb")
    magic = f.read(4)
    assert magic == b"GGUF", f"not a GGUF file: {magic!r}"
    (version, n_tensors, n_kv) = struct.unpack("<IQQ", f.read(20))
    assert version == GGUF_V3, f"unsupported gguf version {version}"
    meta = {}
    for _ in range(n_kv):
        key = _read_str(f)
        (t,) = struct.unpack("<I", f.read(4))
        if t == 9:  # array
            (et,) = struct.unpack("<I", f.read(4))
            (n,) = struct.unpack("<Q", f.read(8))
            meta[key] = [_read_scalar(f, et) for _ in range(n)]
        else:
            meta[key] = _read_scalar(f, t)
    tensors = {}
    for _ in range(n_tensors):
        name = _read_str(f)
        (n_dims,) = struct.unpack("<I", f.read(4))
        ne = list(struct.unpack(f"<{n_dims}Q", f.read(8 * n_dims)))
        (ggml_type,) = struct.unpack("<I", f.read(4))
        (rel_off,) = struct.unpack("<Q", f.read(8))
        tensors[name] = (ggml_type, ne, rel_off)
    align = int(meta.get("general.alignment", 32))
    data_start = (f.tell() + align - 1) // align * align
    f.close()
    return meta, {n: (t, ne, data_start + off) for n, (t, ne, off) in tensors.items()}


def verify_identity(path: Path) -> None:
    assert path.stat().st_size == ARTIFACT_LENGTH, "artifact length mismatch"
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 24), b""):
            h.update(chunk)
    digest = h.hexdigest()
    assert digest == ARTIFACT_SHA256, f"artifact digest mismatch: {digest}"


class TensorSource:
    """Windowed read-only dequantizing source over the pinned artifact."""

    def __init__(self, path: Path, tensors: dict):
        self.f = open(path, "rb")
        self.tensors = tensors
        self.cache: dict[tuple, np.ndarray] = {}

    def close(self):
        self.f.close()

    def kind(self, name: str) -> str:
        t = self.tensors[name][0]
        kind = TYPE_NAME[t]
        assert kind in ALLOWED_KINDS, (
            f"stop condition: {name} storage kind {kind} outside the frozen set"
        )
        return kind

    def window(self, name: str, elem_start: int, elem_length: int) -> np.ndarray:
        """Dequantize [elem_start, elem_start+elem_length) in storage order.

        Windows must land on quantization-block boundaries (the layout
        contract guarantees this: every window is whole rows of ne[0]).
        """
        key = (name, elem_start, elem_length)
        if key in self.cache:
            return self.cache[key]
        ggml_type, ne, base = self.tensors[name]
        block_elems, block_bytes = TYPE_BLOCK[ggml_type]
        ne0 = ne[0]
        assert elem_start % ne0 == 0 and elem_length % ne0 == 0, (
            f"{name}: window not whole rows"
        )
        blocks_per_row = ne0 // block_elems
        assert ne0 % block_elems == 0, f"{name}: ne[0]={ne0} not block-aligned"
        row_start = elem_start // ne0
        n_rows = elem_length // ne0
        first_block = row_start * blocks_per_row
        n_blocks = n_rows * blocks_per_row
        offset = base + first_block * block_bytes
        self.f.seek(offset)
        raw = self.f.read(n_blocks * block_bytes)
        assert len(raw) == n_blocks * block_bytes, f"{name}: short read"
        if ggml_type == 0:  # F32
            out = np.frombuffer(raw, dtype="<f4").astype(np.float32, copy=True)
        elif ggml_type == 30:  # BF16 — exact bits<<16 mapping (ggml semantics)
            u16 = np.frombuffer(raw, dtype="<u2")
            out = (u16.astype(np.uint32) << 16).view(np.float32).copy()
        else:
            out = np.empty(n_blocks * block_elems, dtype=np.float32)
            for i in range(n_blocks):
                blk = raw[i * block_bytes : (i + 1) * block_bytes]
                out[i * block_elems : (i + 1) * block_elems] = dequant_block(ggml_type, blk)
        assert np.isfinite(out).all(), f"{name}: non-finite dequantized values"
        self.cache[key] = out
        return out

# ---------------------------------------------------------------------------
# MoE math (delivery §2) — dtype-parameterized for the f32 / strict-f64 pass.
# ---------------------------------------------------------------------------

def sigmoid(x):
    if x.dtype == np.float32:
        return (np.float32(1.0) / (np.float32(1.0) + np.exp(-x, dtype=np.float32))).astype(np.float32)
    return 1.0 / (1.0 + np.exp(-x))


def silu(x):
    return x * sigmoid(x)


def softmax_full(logits):
    m = logits.max()
    e = np.exp(logits - m, dtype=logits.dtype)
    return e / e.sum(dtype=logits.dtype)


def route_dt(x, W_router, n_used, dtype):
    logits = (W_router @ x).astype(dtype)
    probs = softmax_full(logits.astype(np.float32)).astype(dtype)
    # top-n_used by probability, exact ties -> lowest expert index first.
    order = sorted(range(len(probs)), key=lambda i: (-float(probs[i]), i))
    sel = order[:n_used]
    w = probs[[*sel]]
    s = w.sum(dtype=dtype)
    guard = REPLACE_EPS if dtype == np.float32 else np.float64(REPLACE_EPS)
    w = w / max(s, guard)
    return logits, probs, sel, w


def layer_row(x, layer, src: TensorSource, dtype):
    """Compute the full §2 golden row for one (layer, probe) in `dtype`."""
    def W(name, start, length, rows, cols):
        return src.window(name, start, length).reshape(rows, cols).astype(dtype)

    n_e = f"blk.{layer}.ffn_gate_inp.weight"          # [2048, 256]
    router = W(n_e, 0, EMBED * N_EXPERT, N_EXPERT, EMBED)
    logits, probs, sel, wsel = route_dt(x, router, N_EXPERT_USED, dtype)

    gate_n = f"blk.{layer}.ffn_gate_exps.weight"      # [2048, 512, 256]
    up_n = f"blk.{layer}.ffn_up_exps.weight"
    down_n = f"blk.{layer}.ffn_down_exps.weight"      # [512, 2048, 256]
    win = EMBED * EXPERT_FFN
    experts = []
    moe_out = np.zeros(EMBED, dtype=dtype)
    for e in sorted(sel):  # ascending expert index — pinned accumulation order
        g = W(gate_n, e * win, win, EXPERT_FFN, EMBED)
        u = W(up_n, e * win, win, EXPERT_FFN, EMBED)
        d = W(down_n, e * EMBED * EXPERT_FFN, EMBED * EXPERT_FFN, EMBED, EXPERT_FFN)
        h = silu(g @ x) * (u @ x)
        out = d @ h
        experts.append({"expert": e, "h": h, "out": out})
        wi = wsel[sel.index(e)]
        moe_out = moe_out + (out * wi).astype(dtype)

    sh_g = W(f"blk.{layer}.ffn_gate_shexp.weight", 0, EMBED * SHARED_FFN, SHARED_FFN, EMBED)
    sh_u = W(f"blk.{layer}.ffn_up_shexp.weight", 0, EMBED * SHARED_FFN, SHARED_FFN, EMBED)
    sh_d = W(f"blk.{layer}.ffn_down_shexp.weight", 0, SHARED_FFN * EMBED, EMBED, SHARED_FFN)
    sh_r = src.window(f"blk.{layer}.ffn_gate_inp_shexp.weight", 0, EMBED).astype(dtype)
    sh_out = sh_d @ (silu(sh_g @ x) * (sh_u @ x))
    gate = sigmoid(sh_r @ x)
    gated_shared = (gate * sh_out).astype(dtype)
    ffn = (moe_out + gated_shared).astype(dtype)
    return {
        "logits": logits,
        "probabilities": probs,
        "indices": sel,
        "weights": wsel,
        "experts": experts,
        "shared_out": sh_out,
        "gated_shared": gated_shared,
        "ffn": ffn,
    }

# ---------------------------------------------------------------------------
# Golden emission.
# ---------------------------------------------------------------------------

def row_to_json(row: dict) -> dict:
    out = {
        "indices": [int(i) for i in row["indices"]],
        "weights_u32_hex": f32_hex_row(row["weights"]),
        "logits_u32_hex": f32_hex_row(row["logits"]),
        "probabilities_u32_hex": f32_hex_row(row["probabilities"]),
        "experts": [
            {
                "expert": int(e["expert"]),
                "h_u32_hex": f32_hex_row(e["h"]),
                "out_u32_hex": f32_hex_row(e["out"]),
            }
            for e in row["experts"]
        ],
        "shared_expert_out_u32_hex": f32_hex_row(row["shared_out"]),
        "gated_shared_out_u32_hex": f32_hex_row(row["gated_shared"]),
        "ffn_out_u32_hex": f32_hex_row(row["ffn"]),
    }
    for key in ("logits", "probabilities", "weights", "shared_out", "gated_shared", "ffn"):
        assert np.isfinite(row[key]).all(), f"non-finite golden row field {key}"
    return out


def main(argv: list[str]) -> int:
    check = "--check" in argv
    artifact = Path(os.environ.get("GGUF_MOE_ARTIFACT", ARTIFACT_DEFAULT))

    verify_identity(artifact)
    meta, tensors = parse_gguf(artifact)
    arch = meta.get("general.architecture")
    assert arch == "qwen35moe", f"unexpected architecture {arch!r}"
    src = TensorSource(artifact, tensors)

    # Storage-kind audit (stop condition: kinds outside the frozen set).
    kinds = {}
    for layer in LAYERS:
        for suffix in (
            "ffn_gate_inp", "ffn_gate_inp_shexp", "ffn_gate_exps",
            "ffn_up_exps", "ffn_down_exps",
            "ffn_gate_shexp", "ffn_up_shexp", "ffn_down_shexp",
        ):
            name = f"blk.{layer}.{suffix}.weight"
            kinds[f"{layer}.{suffix}"] = src.kind(name)

    probes_doc = json.loads((HERE / "gguf-moe-probes.json").read_text())
    rows, band_r = [], 0.0
    for probe in probes_doc["probes"]:
        x32 = hex_row_f32(probe["u32_hex"])
        f32_row = layer_row(x32, probe["layer"], src, np.float32)
        f64_row = layer_row(x32.astype(np.float64), probe["layer"], src, np.float64)
        r = float(np.max(np.abs(f32_row["ffn"].astype(np.float64) - f64_row["ffn"])))
        band_r = max(band_r, r)
        row = row_to_json(f32_row)
        row["layer"] = probe["layer"]
        row["probe"] = probe["probe"]
        row["f64_dev_max"] = r
        rows.append(row)
    src.close()

    # Synthetic exact-tie router row (U1 fixture; router surface only).
    synth = json.loads((HERE / "gguf-moe-synthetic.json").read_text())["exact_tie"]
    xs = hex_row_f32(synth["x_u32_hex"])
    Ws = np.asarray([hex_row_f32(r) for r in synth["router_weight_u32_hex"]], dtype=np.float32)
    logits, probs, sel, wsel = route_dt(xs, Ws, synth["config"]["expert_used_count"], np.float32)
    assert [int(i) for i in sel] == [2, 5], f"tie fixture drifted: {sel}"
    synth_row = {
        "source": "synthetic exact-tie-router (gguf-moe-synthetic.json)",
        "indices": [int(i) for i in sel],
        "weights_u32_hex": f32_hex_row(wsel),
        "logits_u32_hex": f32_hex_row(logits),
        "probabilities_u32_hex": f32_hex_row(probs),
    }

    delta = max(min(10.0 * band_r, BAND_CAP), MATMUL_FLOOR)
    delta = float(f"{delta:.6g}")

    golden = {
        "schema": SCHEMA,
        "purpose": "moe-router-oracle",
        "artifact": {
            "file": "Qwen3.6-35B-A3B-UD-Q4_K_M.gguf",
            "length": ARTIFACT_LENGTH,
            "sha256": ARTIFACT_SHA256,
            "architecture": "qwen35moe",
        },
        "transform": {"impl": "ggml/src/ggml-quants.c", "commit": LLAMA_CPP_PIN},
        "config": {
            "expert_count": N_EXPERT,
            "expert_used_count": N_EXPERT_USED,
            "expert_ffn_length": EXPERT_FFN,
            "shared_ffn_length": SHARED_FFN,
            "embedding_length": EMBED,
        },
        "band": {
            "f64_max_deviation": float(f"{band_r:.6g}"),
            "delta": delta,
            "derivation": "Δ = clamp(10·R, 1e-5, 5e-4), R = max |f32_ref − f64_ref| over final FFN outputs",
            "accumulation_order": "ascending expert index (pinned, deterministic)",
            "tie_rule": "lowest expert index first on exact ties",
            "norm_w_guard": "6.103515625e-5 (2^-14, llama.cpp norm_w)",
        },
        "storage_kinds": kinds,
        "f32_encoding": "u32 LE bit hex",
        "generator": "fixtures/gguf/gen_moe_goldens.py",
        "rows": rows,
        "synthetic_tie": synth_row,
    }
    goldens_bytes = (json.dumps(golden, indent=2) + "\n").encode()

    oracle_md = f"""# GGUF MoE Goldens Oracle (MODEL-02-U2)

Independent Python oracle for the `gradus:model/moe` surface. Generated by
`fixtures/gguf/gen_moe_goldens.py`; committed outputs:
`gguf-moe-goldens.json` (schema `{SCHEMA}`).

## Artifact identity (verified read-only every run)

- File: `Qwen3.6-35B-A3B-UD-Q4_K_M.gguf` (operator-local path; never
  committed; override via `GGUF_MOE_ARTIFACT`)
- Length: `{ARTIFACT_LENGTH}` bytes
- SHA-256: `{ARTIFACT_SHA256}`
- Architecture: `qwen35moe`

## Semantic pin

llama.cpp `{LLAMA_CPP_PIN}` — dequant kernels mirror
`ggml/src/ggml-quants.c` (F32/BF16/Q4_K/Q5_K/Q6_K/Q8_0); MoE call shape per
`src/models/qwen35moe.cpp` `build_moe_ffn(..., LLM_FFN_SILU, true /*norm_w*/,
..., SOFTMAX, ...)` + sigmoid `ffn_gate_inp_shexp` shared gate. Router tie
rule is OURS (lowest expert index first; llama.cpp argsort is not stable on
exact ties — recorded divergence policy, delivery §2).

## Commands

```
cd gradus && python3 fixtures/gguf/gen_moe_goldens.py          # regenerate
cd gradus && python3 fixtures/gguf/gen_moe_goldens.py --check  # byte-compare
```

## Δ derivation

`R = max |f32_ref − f64_ref|` over the final FFN outputs of all 8
real-artifact rows (strict-f64 pass re-runs the identical §2 math in
float64 over the same dequantized values): **R = {band_r:.6g}**.
`Δ = clamp(10·R, 1e-5, 5e-4)` (gradus forward band cap `5e-4`, matmul
family floor `1e-5`, numeric-policy v1.0.0): **Δ = {delta}**.

First-divergence discipline: any graded-side mismatch reports the first
divergent element (index + both values); tolerances are never widened.

## Rows

8 real-artifact rows (layers 0, 3, 39, 40 × probes p1, p2) + 1 synthetic
exact-tie router row (indices `[2, 5]`, from `gguf-moe-synthetic.json`).
Storage kinds per layer/tensor are recorded in the JSON `storage_kinds`
map; layers 0/3 are one block class, 39/40 the other (down Q5_K except
blk.34/38/39 Q6_K; blk.40 carries BF16 router rows).
"""
    oracle_bytes = oracle_md.encode()

    outputs = {
        HERE / "gguf-moe-goldens.json": goldens_bytes,
        HERE / "gguf-moe-goldens-oracle.md": oracle_bytes,
    }
    if check:
        first_div = "none"
        for path, data in outputs.items():
            committed = path.read_bytes() if path.exists() else None
            if committed != data:
                print(f"FAIL goldens not byte-stable (or stale): {path.name}", file=sys.stderr)
                return 1
        print(
            f"OK goldens: {len(rows)} real-artifact rows + 1 synthetic row; "
            f"Δ={delta}; first-divergence {first_div}"
        )
        return 0
    for path, data in outputs.items():
        path.write_bytes(data)
        print(f"wrote {path.name} ({len(data)} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
