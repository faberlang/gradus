# GGUF-A3 C1 Oracle — union-set dequant goldens

**Unit**: LIB-03 GGUF-A3 C1 (BF16 + Q5_K codecs, union-set goldens). **Repo**: gradus.
**Date**: 2026-08-14. **Owner**: hand-24 (C1 implement), hand-1 (C3-U5 oracle doc).
**Fixture**: `fixtures/gguf/gguf-dequant-goldens.json` (schema
`gguf-dequant-goldens-v2`), 52 block fixtures — 15 real pinned-row blocks +
37 adversarial patterns across the union set {F32, BF16, Q5_0, Q8_0, Q4_K,
Q5_K, Q6_K}.

This document is the derivation contract for the C1-landed goldens: where
the arithmetic comes from, how to regenerate the fixture, and the byte-level
pins that make the goldens re-verifiable.

## Pinned reference (llama.cpp)

The golden arithmetic mirrors llama.cpp exactly (all elementwise IEEE-754 f32
via numpy float32, no FMA — bit-exact against the C kernels):

| Fact | Pin |
| --- | --- |
| Reference file | `ggml/src/ggml-quants.c` (`dequantize_row_q5_0` / `q8_0` / `q4_K` / `q5_K` / `q6_K` + `get_scale_min_k4`); `ggml/src/ggml-impl.h` `ggml_compute_bf16_to_fp32` |
| Commit | `a957b7747` (full `a957b77478d35c6a73fb9cb8160d7bf9ee016f34`) — the GI2-1 / GI0-3 pin |
| Local checkout | `/Users/ianzepp/work/ianzepp/llama.cpp` (at the pinned commit) |
| GGML type ids | F32 0, BF16 30, Q5_0 6, Q8_0 8, Q4_K 12, Q5_K 13, Q6_K 14 (`ggml.h`) |

The BF16 codec has no llama.cpp `dequantize_row_bf16`; its conversion mirrors
`ggml_compute_bf16_to_fp32` (`bits << 16` mapping, exact for every bf16 since
the 7-bit mantissa is representable in f32). The F32 codec passes the 4-byte
block through as `<f4`.

## Generator

```bash
cd /path/to/faberlang/gradus
python3 fixtures/gguf/gen_dequant_goldens.py
```

Requirements: Python 3.11+ with numpy (no model file is read; all block bytes
are committed constants in the script). The generator is **deterministic** —
reruns produce a byte-identical `fixtures/gguf/gguf-dequant-goldens.json`.
The JSON records the generating interpreter (`python` / `numpy` version
strings) at `generator.*`; those are informational, not pins.

## SHA-256 pins

| File | SHA-256 |
| --- | --- |
| `fixtures/gguf/gguf-dequant-goldens.json` | `be6cafd7554e60ecc33af20b1f138380edb270749af050ab3588dd0a4487c162` |
| `fixtures/gguf/gen_dequant_goldens.py` | `8438e302f5b61e7b34d2294de4fc56e488be50a7a8f5859c1fa1c224813f6676` |

The JSON additionally embeds `sha256` = SHA-256 of the sorted
`block_fixtures` array (its own content pin):
`06599186cdacb8b689c2d2631af66d384037ab03feeb852298b9113bf5d380d4`.

## Fixture composition

| Type | Real blocks | Adversarial | Total |
| --- | --- | --- | --- |
| F32 | 3 (`output_norm.weight` 0/479/959) | 7 | 10 |
| BF16 | 0 (no real in-repo block) | 10 | 10 |
| Q5_0 | 3 (`blk.0.attn_q.weight` 0/14400/28799) | 4 | 7 |
| Q8_0 | 3 (`blk.0.attn_v.weight` 0/4800/9599) | 4 | 7 |
| Q4_K | 3 (`blk.3.ffn_down.weight` 0/4800/9599) | 4 | 7 |
| Q5_K | 0 (no real in-repo block) | 4 | 4 |
| Q6_K | 3 (`blk.0.ffn_down.weight` 0/4800/9599) | 4 | 7 |
| **Total** | **15** | **37** | **52** |

Real blocks are committed read-only from the GI2-1 goldens
(`radix/docs/factory/gpu-inference-gguf/evidence/gi2-dequant-goldens.json`,
SmolLM2-360M row). BF16 and Q5_K have no real in-repo blocks (they live in
the Qwen3.6 artifact, operator evidence never committed); their fixtures are
deterministic crafted patterns exercising every codec path (see the
`ADVERSARIAL` map in the generator).

## Consumers

- `src/model/dequant.proba` — layout facts + fail-closed gates for the union
  set; the block constants mirror the goldens (structure pinned at compile
  level; exact f32 values are the auditor-owned execution path).
- `gradus:model/dequant` (`dequant.fab`) — layout authority
  (`elementa_glomoris` / `octeti_glomoris` per type).

## Re-pin rule

Any change to block geometry, kernel semantics, the pinned llama.cpp commit,
or the golden bytes is an operator decision (CAMPAIGN stop conditions). A
re-pin must update this document, the JSON's embedded `sha256`, and the
`dequant.proba` block constants together. Verify determinism with
`shasum -a 256` before any re-pin.
