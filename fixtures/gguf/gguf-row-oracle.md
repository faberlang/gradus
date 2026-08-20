# PML2-U3 Oracle — pinned GGUF row fixture (smollm2-360m-scaled-row)

**Unit**: PML2-U3 (GGUF row admission — Lane 2). **Repo**: gradus.
**Date**: 2026-08-09. **Owner**: hand-4 (implement), mind@ (admission).

This document pins the LEGAL fixture + oracle for the one admitted GGUF
row. The module `gradus:model/gguf` admits EXACTLY this row into the
schema-2 `capsule.Capsula` (capsule-schema-2.0.0, A1C-M1): a pathless
content identity plus the per-format GGUF manifest, per the GGUF-A1c
clean break.

## Row identity (pinned facts)

The row is a **scaled structural stand-in** for the pinned row
SmolLM2-360M-Instruct-Q4_K_M of `gi0-model-contract` 1.0.0 (GI0-3) /
`gi1-closeout.md`. Architecture, quantization, and tokenizer identity are
pinned from that contract verbatim (values the real model carries); the
tensor table, counts, and ceilings are scaled so the proba proves the
admission RULES, not the 270 MB row (same convention as the U1 capsule
proba and the U2 Safetensors fixture). No model file was downloaded or
redistributed (§8 redistribution boundary — local synthetic fixture only).

| Fact | Pinned value | Source |
| --- | --- | --- |
| Architecture | `llama` / `dense` | gi0-model-contract §2.1 (`general.architecture` = `llama`) |
| Layers | `32` | gi0-model-contract §2.1 (`llama.block_count`) |
| Context | `8192` | gi0-model-contract §2.1 (`llama.context_length`) |
| Vocab size | `49152` | gi0-model-contract §2.1 (`llama.vocab_size`) |
| Embedding size | `960` | gi0-model-contract §2.1 (`llama.embedding_length`) |
| GGUF file version | `3` | gi0-model-contract §1 (`GGUF.version`) |
| File type | `15` (MOSTLY_Q4_K_M) | gi0-model-contract §3 (`general.file_type`) |
| Quantization version | `2` | gi0-model-contract §3 (`general.quantization_version`) |
| Tokenizer kind | `gpt2` (BPE) | gi0-model-contract §4 (`tokenizer.ggml.model`) |
| Pre-tokenizer | `smollm` | gi0-model-contract §4 (`tokenizer.ggml.pre`) |
| BOS / EOS / PAD / UNK ids | `1` / `2` / `2` / `0` | gi0-model-contract §4 |
| BOS-free / space-prefix-free | true / true | gi0-model-contract §4 (`add_bos_token=false`, `add_space_prefix=false`) |
| EOG set | `{0,2}` | gi0-model-contract §4 (eos 2, unk 0) |
| Vocab digest claim | 64-hex fixture value (form-valid) | pinned metadata; vocab-only digest execution is PML2-U4 |
| GGML block layout | Q8_0 32/34, F32 1/4, Q4_K 256/144 | gi0-model-contract §3 (pinned GGML table) |
| GGML type ids | F32 0, Q5_0 6, Q8_0 8, Q4_K 12, Q6_K 14 | pinned toolchain llama.cpp `a957b7747` `ggml.h` |

## Tensor table (pinned, exactly 3)

Offsets are **relative to the data-section start** and must equal the
running cumulative byte size (the llama.cpp reader check `ti.offset ==
ctx->size`); the data region tiles exactly (coverage_ok).

| Name | ggml_type | shape | offset | elements | bytes |
| --- | --- | --- | --- | --- | --- |
| `token_embd.weight` | Q8_0 (8) | [32, 16] | 0 | 512 | 544 |
| `blk.0.attn_norm.weight` | F32 (0) | [16] | 544 | 16 | 64 |
| `blk.0.ffn_down.weight` | Q4_K (12) | [256, 16] | 608 | 4096 | 2304 |
| **Total** | | | | **4624** | **2912** |

Every byte size is a 32-multiple (the pinned row's property, gi1-closeout
residual), so the data section tiles exactly with no per-tensor padding.

## Fixture identity (ORACLE)

| Field | Value |
| --- | --- |
| File | `fixtures/gguf/smollm2-360m-scaled-row.gguf` |
| Byte size | **3936** |
| SHA-256 | **`d89c9ef917158bfb5600f417020479499c6c042f728e9a29c8457a6b1a8f0974`** |
| Metadata KV count | 18 (the 15 identity-bearing required keys + 3 optional admitted keys) |
| Tensor table end | 994 |
| Data-section start | 1024 (= align32(994); 30 pad bytes mirror the GGUF writer) |
| Data region | 2912 bytes (bytes 1024..3936), offset base = data-section start |
| Data pattern | byte k = `(k*13 + 7) mod 256` (deterministic; data content is not semantically inspected) |

The conformance suite and `gguf.proba` reconstruct the same byte sequence
in code (the `aedifica` builder) and admit it into the schema-2 capsule,
whose pathless content identity carries the digest; the digest VALUE is
host-computed per the capsule boundary (capsule.fab header — the language
surface has no digest primitive) and re-verifiable via
`capsule.verifica_contra` (capsule-schema-2.0.0).

## Row ceilings (admit-time caller limits)

| Ceiling | Value | Caller ceiling |
| --- | --- | --- |
| File size (artifact bytes) | 3936 | — (data region ≤ file size) |
| Metadata KV count | 18 | ≤ 4096 (row ceiling) |
| Tensor count | 3 | ≤ 65536 (row ceiling) |
| Tensor-name length | ≤ 128 | ≤ 128 |
| Per-dimension size | ≤ 65536 | ≤ 65536 |
| Total elements | 4624 | ≤ 1e9 |
| Per-string bytes | ≤ 4096 | ≤ 1 MiB (authority text limit) |

Per-type tensor counts (exact row pin): F32 1 / Q4_K 1 / Q5_0 0 / Q6_K 0 /
Q8_0 1.

## Fail-closed matrix (per PML2-U3 done_when)

`gradus/src/model/gguf.proba` and `tests/admission_conformance.fab` prove,
at compile level: the happy row admits → schema-2 capsule with the pinned
identity; and each negative fails closed with the module's typed error
before any allocation sized by a parsed count, across the full dimension
set:

- **format**: bad magic (BadFormat), truncated header (BadWire).
- **version**: unsupported GGUF version (UnknownVersion), u64 field above
  the integer carrier (BadWire).
- **counts/bounds**: kv-count and tensor-count mismatch, expected ceilings
  outside the admitted range, per-type counts not summing (BadBounds).
- **metadata**: unknown key, duplicate key, missing required key, wrong
  value type, key > 128 B, string > 4096 B (BadWire / BadArchitecture /
  UnknownQuantization / BadTokenizer / BadBounds).
- **architecture**: arch id, layer count, context, vocab, embedding
  mismatches (BadArchitecture).
- **dtype/quantization**: file-type mismatch, quantization-version
  mismatch, unknown ggml type, non-block-multiple elements, byte size not
  a 32-multiple, per-type count mismatch (UnknownQuantization).
- **offsets/coverage**: non-contiguous / overlapping / duplicate tensor
  offsets, truncated data region, trailing bytes (BadOffset).
- **shapes**: unsupported rank, invalid/zero/oversized dims, total element
  mismatch (BadShape).
- **tokenizer**: model, pre-tokenizer, bos/eos/pad/unk ids, add_bos,
  add_space_prefix mismatches (BadTokenizer).
- **tensor names**: empty, duplicate, > 128 B (BadWire).

## Regeneration

`python3 fixtures/gguf/gen_fixture.py` — deterministic; the output file is
byte-identical across runs (verify with `shasum -a 256` before any
re-pin). A re-pin is an operator decision (CAMPAIGN stop conditions); any
change to the metadata keys/values, tensor table, padding, or data pattern
changes the oracle hash and MUST update this document, the proba
constants, and `gradus/src/model/gguf.fab`'s pinned contract together.
