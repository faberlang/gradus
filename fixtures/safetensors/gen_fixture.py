#!/usr/bin/env python3
"""Deterministic generator for the pinned PML2-U2 Safetensors row fixture.

Row: scaled structural stand-in for the SmolLM2-360M-Instruct row
(gi0-model-contract 1.0.0): llama arch facts + gpt2/smollm tokenizer
identity pinned in __metadata__, F32-only tensor table (5 tensors), 8-byte
aligned, exactly tiling data region. See safetensors-row-oracle.md.

The output bytes are byte-for-byte reproducible: JSON key order, padding,
and the data-byte pattern are all fixed. The Faber-side proba reconstructs
the same bytes from the same JSON string + pattern, so the pinned oracle
hash binds both.

Run: python3 fixtures/safetensors/gen_fixture.py [out_dir]
"""

import hashlib
import json
import struct
import sys
from pathlib import Path

VOCAB_DIGEST = "a" * 64

# The pinned header JSON — key order is part of the byte identity. The
# Faber constant safetensors.fab/PRAESTOLATUM_JSON must match this EXACTLY.
HEADER = json.dumps(
    {
        "__metadata__": {
            "format.name": "safetensors",
            "format.version": "1.0.0",
            "model.arch": "llama",
            "model.density": "dense",
            "model.layers": "1",
            "model.context": "2048",
            "tokenizer.model": "gpt2",
            "tokenizer.pre": "smollm",
            "tokenizer.vocab_digest": VOCAB_DIGEST,
            "tokenizer.eog": "0,2",
            "tokenizer.bos_free": "true",
            "tokenizer.space_prefix_free": "true",
        },
        "model.embed_tokens.weight": {"dtype": "F32", "shape": [8, 4], "data_offsets": [0, 128]},
        "model.norm.weight": {"dtype": "F32", "shape": [8], "data_offsets": [128, 160]},
        "model.layers.0.self_attn.q_proj.weight": {
            "dtype": "F32",
            "shape": [8, 8],
            "data_offsets": [160, 416],
        },
        "model.layers.0.self_attn.v_proj.weight": {
            "dtype": "F32",
            "shape": [8, 4],
            "data_offsets": [416, 544],
        },
        "model.layers.0.mlp.down_proj.weight": {
            "dtype": "F32",
            "shape": [4, 8],
            "data_offsets": [544, 672],
        },
    },
    separators=(",", ":"),
)


def data_pattern(n: int) -> bytes:
    """Deterministic data-byte pattern (matches the Faber-side builder)."""
    return bytes((i * 13 + 7) % 256 for i in range(n))


def build() -> bytes:
    """Assemble the Safetensors container per the reference format."""
    header_bytes = HEADER.encode("utf-8")
    n = len(header_bytes)
    aligned_n = ((n + 7) // 8) * 8
    padded = header_bytes + b" " * (aligned_n - n)
    header_size = len(padded)  # JSON header length; excludes the 8-byte prefix
    assert header_size % 8 == 0
    data = data_pattern(672)
    return struct.pack("<Q", header_size) + padded + data


def main() -> None:
    out_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent
    out_dir.mkdir(parents=True, exist_ok=True)
    blob = build()
    out = out_dir / "smollm2-360m-scaled-row.safetensors"
    out.write_bytes(blob)
    print(f"wrote {out} ({len(blob)} bytes)")
    print(f"sha256 = {hashlib.sha256(blob).hexdigest()}")
    print(f"header_size = {struct.unpack('<Q', blob[0:8])[0]}")
    print(f"header json len = {len(HEADER.encode('utf-8'))}")


if __name__ == "__main__":
    main()
