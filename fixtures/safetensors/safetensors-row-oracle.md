# PML2-U2 Oracle — pinned Safetensors row fixture (smollm2-360m-scaled-row)

**Unit**: PML2-U2 (Safetensors row admission — Lane 1). **Repo**: gradus.
**Date**: 2026-08-09. **Owner**: hand-1 (implement), mind@ (admission).

This document pins the LEGAL fixture + oracle for the one admitted
Safetensors row. The module `gradus:model/safetensors` admits EXACTLY this
row into the schema-2 `capsule.Capsule` (capsule-schema-2.0.0, A1C-M1): a
pathless content identity plus the per-format Safetensors manifest, per
the GGUF-A1c clean break.

## Row identity (pinned facts)

The row is a **scaled structural stand-in** for the SmolLM2-360M-Instruct
row of `gi0-model-contract` 1.0.0 (GI0-3). Arch and tokenizer identity are
pinned from that contract verbatim (values the model really carries); the
tensor table, shapes, and ceilings are scaled so the proba proves the
admission RULES, not the 270 MB row (same convention as the U1 capsule
proba). No model file was downloaded or redistributed (§8 redistribution
boundary — local synthetic fixture only).

| Fact | Pinned value | Source |
| --- | --- | --- |
| Architecture | `llama` / `dense` | gi0-model-contract §2.1 (`general.architecture` = `llama`) |
| Layers | 1 (scaled) | fixture metadata `model.layers` |
| Context | `2048` (scaled) | fixture metadata `model.context` |
| Tokenizer kind | `gpt2` (BPE) | gi0-model-contract §4 (`tokenizer.ggml.model`) |
| Pre-tokenizer | `smollm` | gi0-model-contract §4 (`tokenizer.ggml.pre`) |
| EOG set | `{0,2}` | gi0-model-contract §4 (eos 2, unk 0) |
| BOS-free / space-prefix-free | true / true | gi0-model-contract §4 (`add_bos_token=false`, `add_space_prefix=false`) |
| Vocab digest claim | 64-hex fixture value (form-valid) | pinned metadata; vocab-only digest execution is PML2-U4 |
| Dtype set | `F32` only | pinned F32 structural row (D4) |
| Row format | `safetensors` / version `1.0.0` | fixture metadata `format.name` / `format.version` |

## Tensor table (pinned, exactly 5)

| Name | dtype | shape | data_offsets | elements | bytes |
| --- | --- | --- | --- | --- | --- |
| `model.embed_tokens.weight` | F32 | [8, 4] | [0, 128) | 32 | 128 |
| `model.norm.weight` | F32 | [8] | [128, 160) | 8 | 32 |
| `model.layers.0.self_attn.q_proj.weight` | F32 | [8, 8] | [160, 416) | 64 | 256 |
| `model.layers.0.self_attn.v_proj.weight` | F32 | [8, 4] | [416, 544) | 32 | 128 |
| `model.layers.0.mlp.down_proj.weight` | F32 | [4, 8] | [544, 672) | 32 | 128 |
| **Total** | | | | **168** | **672** |

All offsets 8-byte aligned; intervals tile the 672-byte data region
exactly (no gaps, no overlaps). Every byte length is a multiple of 8.

## Fixture identity (ORACLE)

| Field | Value |
| --- | --- |
| File | `fixtures/safetensors/smollm2-360m-scaled-row.safetensors` |
| Byte size | **1512** |
| SHA-256 | **`992426b54e8d7a1b7e24e4167a92a5e630bb79ef7e89efdd5fd2cb2b29d0a0bc`** |
| header length N (LE u64) | 832 (= padded JSON header; 8-byte prefix excluded; 832 % 8 == 0) |
| Data region | 672 bytes (bytes 840..1512), offset base = 8 + N |
| Data pattern | byte i = `(i*13 + 7) mod 256` (deterministic; data content is not semantically inspected) |

The conformance suite and `safetensors.proba` embed the same byte
sequence (reconstructed from the same JSON string + pattern) and verify
the schema-2 capsule's digest against this oracle via
`verify_against` (capsule-schema-2.0.0). The digest VALUE is
host-computed per the capsule boundary (capsule.fab header); the language
surface has no digest primitive.

## Row ceilings (admit-time caller limits)

| Ceiling | Value | Caller ceiling |
| --- | --- | --- |
| File size (artifact bytes) | 1512 | — (data region ≤ file size) |
| Metadata KV count | 12 | ≤ 64 (row ceiling) |
| Tensor count | 5 | ≤ 16 (row ceiling) |
| Tensor-name length | ≤ 128 | ≤ 128 |
| Per-dimension size | ≤ 65536 | ≤ 65536 |
| Total elements | 168 | ≤ 1e9 |
| Per-string bytes | ≤ 4096 | ≤ 1 MiB (header cap) |

## Fail-closed matrix (per PML2-U2 done_when)

`gradus/src/model/safetensors.proba` and `tests/admission_conformance.fab`
prove, at compile level: the happy row admits → schema-2 capsule with the
pinned identity; and each negative mutates the pinned row and fails closed
with the module's typed error before any
allocation sized by a parsed count — truncated prefix / truncated header /
truncated data region, non-JSON header, non-object header, format-name
mismatch, row-version mismatch, arch mismatch (metadata + extra tensor),
unsupported dtype, duplicate tensor name, misaligned data offset,
overlapping data regions, shape mismatch, tokenizer identity mismatch,
missing `__metadata__`, ceilings (name length, dimension, element count),
and malformed digest claim.

## Regeneration

`python3 fixtures/safetensors/gen_fixture.py` — deterministic; the output
file is byte-identical across runs (verify with `shasum -a 256` before any
re-pin). A re-pin is an operator decision (CAMPAIGN stop conditions); any
change to the JSON string, padding, or data pattern changes the oracle hash
and MUST update this document and the proba constant together.
