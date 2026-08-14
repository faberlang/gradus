# Delivery: GGUF-M1 — qwen35moe Admission And Tensor Map (MODEL-01)

**Campaign**: Radix `gpu-production-readiness` Qwen3.6 invariant —
[MODEL-01](../../../../radix/docs/factory/gpu-production-readiness/CAMPAIGN.md)
**Semantic authority**: [`pml5-general-gguf-delivery.md`](pml5-general-gguf-delivery.md) §GGUF-M1
**Campaign mode**: run
**Repo**: `gradus`
**Status**: READY FOR DELIVERY — implementation gated on predecessor receipts
**Planner**: planner-25 (fresh lowering; no planner-1..19 artifacts reused)
**Date**: 2026-08-13; **re-split 2026-08-14** (operator granularity directive — one
behavior family per unit; see §Hand Unit Graph)
**Integration stop**: `factory/merge` only; this delivery does not fast-forward any main branch

## Dispatch Authority (resolves need `13bce68c`)

This document — planner-25's amended `pml5-gguf-m1-qwen35moe-admission-delivery.md`
(head `76d306c`, M1–M9 + G1) — is **THE single dispatch authority** for MODEL-01.
planner-39's `pml5-gguf-m1-qwen35moe-micro-units.md` (`df3c016`, frontier-corrected
`c69d6a7`) carries the same M1–M9 + G1 boundaries and is **superseded**; it is not
a competing authority. Dispatch reads unit definitions, write scopes, dependencies,
and the serialization frontier from this document only.

## Executed Outcome

One new public Gradus module, `gradus:model/qwen35moe`, admits the exact local
`Qwen3.6-35B-A3B-UD-Q4_K_M.gguf` artifact into a **complete typed execution
configuration** and a **canonical 753-tensor map**, and fails closed with
typed first-divergence diagnostics when any required fact is mutated, missing,
or unknown. The unit produces no logits, no token generation, no MoE routing,
and no SSM/attention state — those are GGUF-M2/M3/M4. This unit is the
admission gate those successors consume.

The exact executed proof is a real-file admission receipt: the guarded
application-owned adapter (the GGUF-A1b range-source pattern) feeds the
bounded manifest of the target artifact to `gradus:model/qwen35moe`, which
returns ADMIT with the frozen configuration and 753 admitted tensors. A
package-MIR mutation suite proves every required failure mode with typed
diagnostics.

The outcome is delivered as a ten-entry unit graph (§Hand Unit Graph): nine
one-behavior-family micro-units (M1–M9) plus one aggregate integration gate
(G1). The mandatory scope is the union of the unit scopes and is not narrowed
by the re-split.

## Goal-Check Verdict

**READY.** The GGUF-M1 spec in the delivery authority is concrete, the frozen
target facts are independently verified below against the live artifact, the
manifest accessor surface exists (GGUF-A1b), and the predecessor units name
exact receipts. No architecture gap requires inventing design at delivery
time; MoE routing, hybrid SSM state, and full-model inference are explicitly
deferred to their owning units.

## Frozen Target Identity

| Fact | Value | Independent evidence |
| --- | --- | --- |
| Filename | `Qwen3.6-35B-A3B-UD-Q4_K_M.gguf` | `exempla/gguf-inspect/README.md` inventory |
| Byte length | 22,663,387,424 | `stat -f '%z'` (A1b receipt) + GGUF header |
| SHA-256 | `0b21525e972670ed59e1812e170b27c26355381f0656ecc4e25617ece7dac58b` | `shasum -a 256` (A1b receipt) |
| GGUF version | 3 | `llama-gguf` r + live header parse |
| Alignment | 32 | `llama-gguf` r + live header parse |
| Data offset | 10,991,392 | `llama-gguf` r oracle + live parse |
| Metadata entries | 55 | `llama-gguf` r + live parse |
| Tensor count | 753 | `llama-gguf` r + live parse |
| Architecture | `qwen35moe` | `general.architecture` value |

The identity is the admission precondition: a manifest whose content identity
does not match these three facts (filename is provenance only) is rejected
before any architecture read.

## Frozen Architecture Configuration

Values below are read from the live artifact's 55 metadata entries on
2026-08-13 (independent `llama-gguf` key listing + direct wire-value parse).
The admission must freeze these as a typed configuration and fail closed on
any divergence.

| Metadata key | Wire kind | Frozen value |
| --- | --- | --- |
| `general.architecture` | string | `qwen35moe` |
| `general.file_type` | uint32 | 15 (MOSTLY_Q4_K_M) |
| `general.quantization_version` | uint32 | 2 |
| `qwen35moe.block_count` | uint32 | 41 |
| `qwen35moe.context_length` | uint32 | 262144 |
| `qwen35moe.embedding_length` | uint32 | 2048 |
| `qwen35moe.attention.head_count` | uint32 | 16 |
| `qwen35moe.attention.head_count_kv` | uint32 | 2 |
| `qwen35moe.attention.key_length` | uint32 | 256 |
| `qwen35moe.attention.value_length` | uint32 | 256 |
| `qwen35moe.attention.layer_norm_rms_epsilon` | float32 | 1e-6 (0.0000009999999974752427 f32) |
| `qwen35moe.rope.freq_base` | float32 | 10000000.0 |
| `qwen35moe.rope.dimension_count` | uint32 | 64 |
| `qwen35moe.rope.dimension_sections` | array<uint32> (4) | `[11, 11, 10, 0]` |
| `qwen35moe.expert_count` | uint32 | 256 |
| `qwen35moe.expert_used_count` | uint32 | 8 |
| `qwen35moe.expert_feed_forward_length` | uint32 | 512 |
| `qwen35moe.expert_shared_feed_forward_length` | uint32 | 512 |
| `qwen35moe.ssm.conv_kernel` | uint32 | 4 |
| `qwen35moe.ssm.state_size` | uint32 | 128 |
| `qwen35moe.ssm.group_count` | uint32 | 16 |
| `qwen35moe.ssm.time_step_rank` | uint32 | 32 |
| `qwen35moe.ssm.inner_size` | uint32 | 4096 |
| `qwen35moe.full_attention_interval` | uint32 | 4 |
| `qwen35moe.nextn_predict_layers` | uint32 | 1 |
| `tokenizer.ggml.model` | string | `gpt2` |
| `tokenizer.ggml.pre` | string | `qwen35` |
| `tokenizer.ggml.tokens` | array<string> | 248320 entries |
| `tokenizer.ggml.token_type` | array<int32> | 248320 entries |
| `tokenizer.ggml.merges` | array<string> | 247587 entries |
| `tokenizer.ggml.eos_token_id` | uint32 | 248046 |
| `tokenizer.ggml.padding_token_id` | uint32 | 248055 |
| `tokenizer.ggml.bos_token_id` | uint32 | 248044 |
| `tokenizer.ggml.add_bos_token` | bool | false |

Tokenizer execution (encode/decode/EOG/chat-template) is GGUF-A2's unit; the
admission here only freezes the tokenizer *identity facts* so the complete
typed configuration names the exact tokenizer row the artifact carries.

## Canonical 753-Tensor Map

The map below is the **raw tensor directory as stored** in the target
artifact (dims in GGUF file order; GGUF stores the last logical dimension
first). Storage types are the raw GGML type IDs resolved to names. All facts
below were read live from the file on 2026-08-13.

### Global tensors (3)

| Tensor | Stored shape | Storage | Note |
| --- | --- | --- | --- |
| `output.weight` | `(2048, 248320)` | q6_K | vocab 248320 × embd 2048 |
| `output_norm.weight` | `(2048,)` | f32 | |
| `token_embd.weight` | `(2048, 248320)` | q8_0 | |

### Block schedule (41 blocks)

`qwen35moe.block_count` = 41; indices 0..40. `full_attention_interval` = 4,
so the 10 **full-attention blocks** are `blk.3, blk.7, blk.11, blk.15,
blk.19, blk.23, blk.27, blk.31, blk.35, blk.39` (index ≡ 3 mod 4). The
remaining 30 blocks (all other indices 0..38 except 40) are **hybrid
SSM/attention blocks**. `nextn_predict_layers` = 1 makes `blk.40` the
**nextn block** with the full-attention set plus `nextn.*` tensors.

| Block class | Count | Tensors per block | Total |
| --- | ---: | ---: | ---: |
| Hybrid SSM/attention | 30 | 19 | 570 |
| Full attention | 10 | 16 | 160 |
| Nextn (`blk.40`) | 1 | 20 | 20 |
| Global | — | — | 3 |
| **Total** | | | **753** |

### Hybrid block tensor set (19 tensors) — shape/storage frozen

| Canonical name | Stored shape | Storage |
| --- | --- | --- |
| `blk.N.attn_gate.weight` | `(2048, 4096)` | q8_0 |
| `blk.N.attn_norm.weight` | `(2048,)` | f32 |
| `blk.N.attn_qkv.weight` | `(2048, 8192)` | q8_0 |
| `blk.N.ffn_down_exps.weight` | `(512, 2048, 256)` | q5_K (q6_K in blk.34/38/39) |
| `blk.N.ffn_down_shexp.weight` | `(512, 2048)` | q8_0 |
| `blk.N.ffn_gate_exps.weight` | `(2048, 512, 256)` | q4_K |
| `blk.N.ffn_gate_inp.weight` | `(2048, 256)` | f32 |
| `blk.N.ffn_gate_inp_shexp.weight` | `(2048,)` | f32 |
| `blk.N.ffn_gate_shexp.weight` | `(2048, 512)` | q8_0 |
| `blk.N.ffn_up_exps.weight` | `(2048, 512, 256)` | q4_K |
| `blk.N.ffn_up_shexp.weight` | `(2048, 512)` | q8_0 |
| `blk.N.post_attention_norm.weight` | `(2048,)` | f32 |
| `blk.N.ssm_a` | `(32,)` | f32 |
| `blk.N.ssm_alpha.weight` | `(2048, 32)` | f32 |
| `blk.N.ssm_beta.weight` | `(2048, 32)` | f32 |
| `blk.N.ssm_conv1d.weight` | `(4, 8192)` | f32 |
| `blk.N.ssm_dt.bias` | `(32,)` | f32 |
| `blk.N.ssm_norm.weight` | `(128,)` | f32 |
| `blk.N.ssm_out.weight` | `(4096, 2048)` | q8_0 |

### Full-attention block tensor set (16 tensors) — shape/storage frozen

| Canonical name | Stored shape | Storage |
| --- | --- | --- |
| `blk.N.attn_k.weight` | `(2048, 512)` | q8_0 |
| `blk.N.attn_k_norm.weight` | `(256,)` | f32 |
| `blk.N.attn_norm.weight` | `(2048,)` | f32 |
| `blk.N.attn_output.weight` | `(4096, 2048)` | q8_0 |
| `blk.N.attn_q.weight` | `(2048, 8192)` | q8_0 |
| `blk.N.attn_q_norm.weight` | `(256,)` | f32 |
| `blk.N.attn_v.weight` | `(2048, 512)` | q8_0 |
| `blk.N.ffn_down_exps.weight` | `(512, 2048, 256)` | q5_K |
| `blk.N.ffn_down_shexp.weight` | `(512, 2048)` | q8_0 |
| `blk.N.ffn_gate_exps.weight` | `(2048, 512, 256)` | q4_K |
| `blk.N.ffn_gate_inp.weight` | `(2048, 256)` | f32 |
| `blk.N.ffn_gate_inp_shexp.weight` | `(2048,)` | f32 |
| `blk.N.ffn_gate_shexp.weight` | `(2048, 512)` | q8_0 |
| `blk.N.ffn_up_exps.weight` | `(2048, 512, 256)` | q4_K |
| `blk.N.ffn_up_shexp.weight` | `(2048, 512)` | q8_0 |
| `blk.N.post_attention_norm.weight` | `(2048,)` | f32 |

### Nextn block `blk.40` tensor set (20 tensors)

The full-attention 16-tensor set above plus:

| Canonical name | Stored shape | Storage |
| --- | --- | --- |
| `blk.40.nextn.eh_proj.weight` | `(4096, 2048)` | q8_0 |
| `blk.40.nextn.enorm.weight` | `(2048,)` | f32 |
| `blk.40.nextn.hnorm.weight` | `(2048,)` | f32 |
| `blk.40.nextn.shared_head_norm.weight` | `(2048,)` | f32 |

Storage anomaly to preserve, not normalize: in `blk.40`,
`ffn_gate_inp.weight` and `ffn_gate_inp_shexp.weight` are **bf16** while the
same tensors are f32 in every other block. The mixed-storage directory is a
per-tensor fact; the admission must not collapse it to one global storage row.

Block-40 nextn/MTP rule (frozen): `blk.40` is the sole nextn block; its 20
tensors are **admitted** as part of the canonical map (map completeness
requires all 753), but the main forward layer schedule is blocks 0..39. The
admission records nextn tensors as loaded-not-main-pass and claims no
nextn/MTP execution semantics — those belong to GGUF-M2/M3/M4.

### Storage-type distribution (753 tensors)

| Storage | Count |
| --- | ---: |
| f32 | 368 |
| q8_0 | 259 |
| q4_K | 82 |
| q5_K | 38 |
| q6_K | 4 |
| bf16 | 2 |
| **Total** | **753** |

Rank-3 expert tensors: 123 (41 blocks × 3 expert tensors — `ffn_down_exps`,
`ffn_gate_exps`, `ffn_up_exps`). For known K-quant layouts, block
divisibility checks against the first GGML dimension (q4_K/q5_K/q6_K blocks =
256 elements; 256 divides the expert axis).

## Dimension And Cross-Reference Validation

The admission validates every canonical tensor against the frozen config.
Stored dims are GGUF file order (last logical dimension first); each bullet
names the exact stored-dim position per tensor family so per-tensor
validation predicates copy directly:

- `embedding_length` 2048 is stored dim 0 of `attn_gate`, `attn_qkv`,
  `attn_k`, `attn_v`, `attn_q`, `ffn_gate_inp`, `ssm_alpha`, `ssm_beta`,
  `output`/`token_embd`, and stored dim 1 of `ffn_down_exps`/
  `ffn_down_shexp`, `ssm_out`, `attn_output`, and `nextn.eh_proj`. It is the
  single dim of `attn_norm`, `post_attention_norm`, `ffn_gate_inp_shexp`,
  `output_norm`, and the `nextn.*` norms. It is NOT dim 0 of
  `attn_output`/`ssm_out`/`nextn.eh_proj` (4096), `ffn_down_exps`/
  `ffn_down_shexp` (512), or `attn_k_norm`/`attn_q_norm` (256).
- Expert rank-3 families: `ffn_down_exps` stores `[ffn, embd, experts]` =
  `(512, 2048, 256)`; `ffn_gate_exps` and `ffn_up_exps` store
  `[embd, ffn, experts]` = `(2048, 512, 256)`.
- `expert_count` 256 is stored dim 2 of the three `*_exps` rank-3 tensors in
  every block and stored dim 1 of `ffn_gate_inp`.
- `expert_feed_forward_length` 512 is stored dim 0 of the down family
  (`ffn_down_exps`, `ffn_down_shexp`) and stored dim 1 of the gate/up
  family (`ffn_gate_exps`, `ffn_up_exps`, `ffn_gate_shexp`, `ffn_up_shexp`).
- `ssm.state_size` 128 matches `ssm_norm.weight`; `ssm.time_step_rank` 32
  matches `ssm_a`, `ssm_dt.bias`, and the second stored dim of
  `ssm_alpha`/`ssm_beta`.
- `ssm.conv_kernel` 4 matches the first stored dim of `ssm_conv1d.weight`.
- `ssm.inner_size` 4096 is stored dim 0 of `ssm_out.weight`,
  `attn_output.weight`, and `nextn.eh_proj.weight`, and stored dim 1 of
  `attn_gate.weight`.
- `attention.head_count_kv` 2 × `attention.key_length` 256 = 512 = the
  second stored dim of `attn_k.weight`/`attn_v.weight`; `attn_q_norm.weight`
  and `attn_k_norm.weight` are single-dim 256 (= `key_length` =
  `value_length`).
- Block schedule: exactly 10 full-attention blocks at index ≡ 3 mod 4 and
  exactly one nextn block (`blk.40`) when `nextn_predict_layers` = 1.
- Element counts equal the product of stored dims and every tensor's checked
  absolute range satisfies `data_inceptum + offset_relativum <= total`
  (GGUF-A1a/A1b guarantees).

## Mutation Fail-Closed Requirements (first failing oracle)

For each mutation family below, the admission returns a **typed
first-divergence diagnostic** naming the first diverging fact (metadata key /
tensor name / shape / storage / count), not a generic parse error:

1. **Metadata mutations** — any frozen `qwen35moe.*` value changed
   (block_count, embedding_length, head counts, expert counts, SSM sizes,
   rope facts, nextn count); a required key missing; an extra unknown key
   that shadows a required fact.
2. **Name mutations** — a canonical tensor renamed, duplicated, or replaced
   by an unknown name.
3. **Shape mutations** — a canonical tensor's shape or rank changed
   (including rank-3 → rank-2 expert tensors).
4. **Storage mutations** — a canonical tensor's raw GGML type changed
   (including the bf16/f32 anomaly in `blk.40` being "corrected" away, and
   mixed-storage collapsing to one global row).
5. **Count mutations** — tensor count ≠ 753, metadata count ≠ 55, or a block
   family count out of schedule.
6. **Identity mutations** — byte length or SHA-256 divergence (fail before
   any architecture read).
7. **Unsupported-but-inspectable** — an *unknown* architecture name or raw
   GGML type stays inspectable as data (GGUF-A1a rule) but cannot admit as
   `qwen35moe`.

The first failing oracle is the first divergent fact in the divergence
receipt; the receipt routes the repair to the owning repository (Gradus for
admission, Radix/Faber/Hosts only for facts that belong to their seam).

## Dependencies And Predecessor Receipts

| Dependency | Receipt | State |
| --- | --- | --- |
| GGUF-A1a manifest parser | `exempla/gguf-manifest` executed synthetic receipt | implemented |
| GGUF-A1b range seam + real-file inspection | `exempla/gguf-inspect` 6-file guarded receipt | implemented |
| GGUF-A1c capsule/caller clean break (LIB-01) | aggregate gate M8R4 | **landed — Gradus main `2b3e41a`** |
| GGUF-A2 tokenizer runtime (LIB-02) | [`pml5-lib02-tokenizer-delivery.md`](pml5-lib02-tokenizer-delivery.md) micro-unit chain | **in progress** — U1 typed metadata array accessors landed (`c4d0750`); aggregate gate pending |
| GGUF-A3 packed storage (LIB-03) | [`pml5-gguf-a3-packed-storage-delivery.md`](pml5-gguf-a3-packed-storage-delivery.md) micro-unit chain | **in progress** — A3-C1 BF16/Q5_K codecs landed (`82048b5`); aggregate gate pending |

Per the campaign dependency table (corrected frontier `c69d6a7`), the MODEL-01
chain dispatches only after the **LIB-02 and LIB-03 aggregate gates land on
`factory/merge`**; REF-01 (dense reference rungs) is a **sibling** of
MODEL-01, not a predecessor, and never gates this dispatch. GGUF-A1c (LIB-01)
is landed. This delivery artifact is lowered now so the units are
implementation-ready when the LIB-02/LIB-03 aggregate gates land; it does not
claim predecessor completion.

## Theme Write Scope (Mandatory Union — Unchanged)

Only the files below. No product source outside this list, no docs outside
the listed set. Each micro-unit's exact write scope in §Hand Unit Graph is a
subset of this union; the union is the mandatory MODEL-01 scope and the
re-split does not narrow it. One recommended addition (M2's facts fixture,
§Open Questions) pins the frozen facts beside the existing
`fixtures/gguf/general-manifest-oracle.md` / `gguf-row-oracle.md` pattern and
is flagged for Mind approval.

- `src/model/qwen35moe.fab` (new) — public import `gradus:model/qwen35moe`;
  typed configuration genus, admission entry point(s), canonical tensor map,
  dimension validation, fail-closed mutation diagnostics.
- `src/model/qwen35moe.proba` (new) — package tests covering every frozen
  config value, the 753-tensor map families, and all seven mutation families.
- `src/model/gguf_manifest.fab` + `src/model/gguf_manifest.proba` —
  only architecture-facing manifest accessors this unit needs that do not
  already exist (e.g. typed array-of-uint32 access for
  `rope.dimension_sections`); no parser behavior change.
- `docs/module-map.md` — add `gradus:model/qwen35moe` row + PML layer note.
- `docs/api-reference.md` — document every public symbol of
  `gradus:model/qwen35moe` (coverage gate: `scripta/inventory-public-symbols`
  must pass).
- `docs/factory/production-ml-library/pml0-symbol-inventory.md` — reflect the
  new module and its public symbols.
- `docs/factory/production-ml-library/pml0-support-matrix.md` — record the
  qwen35moe admission row (architecture + tensor-map facts; no execution
  claim).
- `docs/regression-corpus.md` — inventory the new proba suite and the
  admission exemplar, bump the suite totals under the corpus contract.
- `exempla/gguf-admit-qwen35moe/` (new) — guarded application-owned adapter
  (GGUF-A1b pattern): reads the bounded manifest of the target artifact,
  calls `gradus:model/qwen35moe` admission, prints ADMIT + frozen config +
  753-tensor receipt; `faber.toml`, `src/main.fab`, `README.md`.
- `scripta/check-compile` — register the new exemplum in the compile gate.

## Read Scope And Local Corpus Boundary

- Read (real-file oracle): `/Users/ianzepp/Ai/models/Qwen3.6-35B-A3B-UD-Q4_K_M.gguf`
  — bounded manifest prefix only (first 10,991,392 bytes); the adapter must
  prove no read enters the tensor data region, exactly as GGUF-A1b.
- Read (mutation oracle): synthetic in-source corpora in `.proba`; no real
  file is mutated or copied.
- The local corpus is operator-local evidence and is **never committed** to
  the repo (delivery authority §Grounded Local Acceptance Corpus).

## Hardware / Backend Authority

- This unit is CPU/reference and device-neutral. No Metal, CUDA, device
  handles, memory mapping, or kernel work — those belong to GGUF-A7/GGUF-M5
  and the Radix/Hosts seams.
- Hardware authority for the executed receipt: the local host running the
  package-MIR exemplar through the lane-local Radix `faber` binary.

## Hand Unit Graph (re-split 2026-08-14)

The former single unit (est 90k–150k work tokens — far over the operator's
granularity bar) is re-split into **nine one-behavior-family micro-units
(M1–M9) plus one aggregate integration gate (G1)**, per the operator
directive 2026-08-14: one behavior family per unit, executable by a Hand in
roughly 10–15 minutes with a focused check, commit, and close. Every unit
carries all eight campaign-rule-2 fields: `outcome`, `exact write scope`,
`first failing oracle`, `closeout command`, `expected observed result`,
`est_basis`, `stop condition`, `depends_on`.

The mandatory scope is preserved: the union of the unit write scopes equals
the Theme Write Scope (plus the M2 facts fixture, a recommended addition);
no frozen fact, tensor row, mutation family, or successor is narrowed,
deferred, or made optional. No child runs a package/source/compile/stage/
e2e/full closeout — `check-source` + `check-compile` are the narrowest
working gates for a Gradus library unit, and the only package-level compile +
fmir run in the whole chain is G1.

`est_basis` per unit is `pilot` (no ledger class exists for GGUF-M1 qwen35moe
admission; the ledger's closest classes are `diagnostics-oracle` and
`compiler-surface-feature`). M3 seeds the architecture-admission module class
baseline; M4–M6 inherit it. Tool latency per code unit: `faber check` through
the lane-local Radix binary, ~2–5 min cold; no GPU or long-running work.

### MODEL-01-M1 — Manifest architecture-facing typed accessors

| Field | Value |
| --- | --- |
| `outcome` | `gradus:model/gguf_manifest` exposes the typed accessors the qwen35moe admission needs that are not already on the LIB-02 landed surface: typed array-of-uint32 read (so `qwen35moe.rope.dimension_sections` decodes to `[11, 11, 10, 0]`), bool read (for `tokenizer.ggml.add_bos_token`), and array-length read (for the tokenizer identity counts 248320 / 248320 / 247587); missing / malformed / duplicate / wrong-kind keys fail with typed `GgufManifestError` rows; **no parser behavior change**. If the landed LIB-02 surface already decodes a needed accessor, the unit narrows to the proba proof and adds no new symbol |
| `exact write scope` | `src/model/gguf_manifest.fab`, `src/model/gguf_manifest.proba` only |
| `first failing oracle` | the new proba cases asserting `rope.dimension_sections` → `[11, 11, 10, 0]`, `add_bos_token` → `falsum`, and the three tokenizer array lengths fail to compile/type-check (the packet baseline lacks the typed array/bool/length reads) |
| `closeout command` | `./scripta/check-source && ./scripta/check-compile` (lane-local `FABER_BIN`/`FABER_LIBRARY_HOME`); `git diff --check -- src/model/gguf_manifest.fab src/model/gguf_manifest.proba` |
| `expected observed result` | both gates exit 0; the new proba cases type-check; every existing manifest proba case is unchanged; `git diff --check` silent |
| `est_basis` | `pilot` — typed-accessor verification/extension on the LIB-02 landed seam (closest ledger class `compiler-surface-feature`); 3–5k tokens |
| `stop condition` | an accessor would require a parser/parse-behavior change → stop, report the seam violation To mind; a wire-kind coercion (e.g. BOOL read as UINT32) would be required → stop, the typed error is the behavior |
| `depends_on` | theme dispatch frontier only (LIB-02 + LIB-03 aggregate gates; §Dispatch Serialization) — no intra-theme unit |
| `gate` | proba decode + both gates green. **Non-integrable alone** (changes `model/gguf_manifest` symbol count and needs M8's api-reference coverage) — only G1 merges |

### MODEL-01-M2 — Qwen35moe admission oracle fixture

| Field | Value |
| --- | --- |
| `outcome` | a committed facts fixture `fixtures/gguf/qwen35moe-admission-oracle.md` pins every frozen fact verbatim from this delivery: target identity (byte length 22,663,387,424, SHA-256 `0b21525e…dac58b`, GGUF version 3, alignment 32, data offset 10,991,392, metadata 55, tensor count 753, architecture `qwen35moe`), all 30 frozen config rows (incl. `rope.dimension_sections` `[11, 11, 10, 0]` and the tokenizer identity facts), the four canonical tensor-family sets with exact shape/storage rows, the 41-block schedule (30 hybrid / 10 full-attention / 1 nextn / 3 global), the storage distribution (f32 368 / q8_0 259 / q4_K 82 / q5_K 38 / q6_K 4 / bf16 2), the blk.40 bf16 and blk.34/38/39 q6_K anomalies, the block-40 load-not-main-pass rule, rank-3 expert count 123, and the seven-family typed refusal matrix — facts only, no GGUF bytes, no execution claims |
| `exact write scope` | `fixtures/gguf/qwen35moe-admission-oracle.md` (new) only — the one recommended addition to the Theme Write Scope (§Open Questions) |
| `first failing oracle` | fixture absent or any frozen row missing/divergent from the tables in this delivery (grep assertions fail) |
| `closeout command` | grep-based completeness assertions over every table row; `git diff --check -- fixtures/gguf/qwen35moe-admission-oracle.md` |
| `expected observed result` | fixture committed and complete with every fact above; `git diff --check` silent |
| `est_basis` | `pilot` — first qwen35moe admission facts fixture (precedent: `general-manifest-oracle.md`); 3–5k tokens |
| `stop condition` | a frozen value cannot be confirmed against the live artifact or the independent `llama-gguf` oracle → stop, do not invent; record the divergence to the owning repo |
| `depends_on` | theme dispatch frontier only; runs in parallel with M1 (disjoint files) |
| `gate` | fixture completeness greps. **Non-integrable alone** (facts pinned ahead of the surface) — only G1 merges |

### MODEL-01-M3 — Configuration genus + metadata freeze

| Field | Value |
| --- | --- |
| `outcome` | the typed configuration genus in the new `gradus:model/qwen35moe` freezes all 30 frozen metadata rows (architecture, quantization, block_count 41, context_length 262144, embedding_length 2048, attention/rope/expert/SSM/nextn facts, tokenizer identity facts) read through the manifest accessors; metadata count 55 enforced; any frozen `qwen35moe.*` value changed, a required key missing, or an extra unknown key shadowing a required fact fails with a typed metadata-divergence diagnostic naming the first diverging key (mutation family 1); tokenizer facts are frozen as identity only |
| `exact write scope` | `src/model/qwen35moe.fab`, `src/model/qwen35moe.proba` only |
| `first failing oracle` | proba case with `qwen35moe.block_count` 41→42 (or a missing `qwen35moe.ssm.state_size` key) must yield a typed diagnostic naming that key; the cases fail today (module absent) |
| `closeout command` | `./scripta/check-source && ./scripta/check-compile`; `git diff --check -- src/model/qwen35moe.fab src/model/qwen35moe.proba` |
| `expected observed result` | both gates exit 0; all 30 frozen values + metadata-count 55 pins type-check; mutation family 1 fails with a typed first-divergence diagnostic |
| `est_basis` | `pilot` — first architecture-config freeze in Faber (seeds the architecture-admission module class); 5–7k tokens |
| `stop condition` | a required fact cannot be represented in the typed config → report the gap To mind with a default and options; do not invent a representation |
| `depends_on` | M1 + M2 |
| `gate` | module proof green. **Non-integrable alone** (partial module; inventory/docs gates break) — only G1 merges |

### MODEL-01-M4 — Canonical 753-tensor map + block schedule

| Field | Value |
| --- | --- |
| `outcome` | the canonical tensor map admits the four exact family sets (global 3: `output.weight`/`output_norm.weight`/`token_embd.weight`; hybrid 19×30; full-attention 16×10; nextn 20 on `blk.40`) with each tensor's exact stored shape and storage row; the 41-block schedule (indices 0..40; full-attention at index ≡ 3 mod 4; `blk.40` the sole nextn block per `nextn_predict_layers`=1); the storage distribution (f32 368 / q8_0 259 / q4_K 82 / q5_K 38 / q6_K 4 / bf16 2); the blk.40 bf16 and blk.34/38/39 q6_K anomalies preserved **per-tensor** (never collapsed to one global storage row); the block-40 nextn/MTP load-not-main-pass rule recorded (20 tensors admitted for map completeness; main-pass schedule blocks 0..39; no nextn execution claim); count invariants (753 total, metadata 55, block-family counts); mutation families 2 (name), 3 (shape), 4 (storage), 5 (count) fail with typed first-divergence diagnostics |
| `exact write scope` | `src/model/qwen35moe.fab`, `src/model/qwen35moe.proba` only |
| `first failing oracle` | proba case renaming a canonical tensor (e.g. `blk.0.attn_norm.weight` → `blk.0.attn_norm2.weight`), collapsing a rank-3 expert tensor to rank-2, "correcting" the blk.40 bf16 anomaly, or mutating the count 753→752 must each yield a typed first-divergence diagnostic naming the first diverging fact; the cases fail today (no map) |
| `closeout command` | `./scripta/check-source && ./scripta/check-compile`; `git diff --check -- src/model/qwen35moe.fab src/model/qwen35moe.proba` |
| `expected observed result` | both gates exit 0; family-set shapes/storage rows, count/schedule pins, distribution, and anomaly probas type-check; mutation families 2–5 fail typed |
| `est_basis` | `pilot` — 753-tensor family map in Faber (architecture-admission module class seeded by M3); 5–8k tokens |
| `stop condition` | a canonical tensor fact contradicts the live artifact → pause, re-verify against the independent oracle, and route the correction; never normalize an anomaly |
| `depends_on` | M3 (file-serialized on the module) |
| `gate` | module proof green. **Non-integrable alone** (partial module) — only G1 merges |

### MODEL-01-M5 — Dimension / storage cross-reference validation

| Field | Value |
| --- | --- |
| `outcome` | cross-reference validation between the frozen config and the canonical map per §Dimension And Cross-Reference Validation: `embedding_length` 2048 at its stored-dim positions per tensor family; `expert_count` 256 as rank-3 dim 2 of the three `*_exps` tensors and dim 1 of `ffn_gate_inp`; `expert_feed_forward_length` 512 at the down/gate-up positions; `ssm.state_size` 128 / `time_step_rank` 32 / `conv_kernel` 4 / `inner_size` 4096 dim matches; `head_count_kv` 2 × `key_length` 256 = 512 = dim 1 of `attn_k`/`attn_v` (norms carry 256); block-schedule consistency (10 ≡ 3 mod 4, one nextn when `nextn_predict_layers`=1); element counts = product of stored dims; every checked absolute range satisfies `data_inceptum + offset_relativum <= total` (GGUF-A1a/A1b guarantees); any cross-fact violation fails with a typed first-divergence diagnostic |
| `exact write scope` | `src/model/qwen35moe.fab`, `src/model/qwen35moe.proba` only |
| `first failing oracle` | proba case with a deliberate cross-fact violation (e.g. `head_count_kv`×`key_length` ≠ 512, or an `attn_qkv` embedding dim ≠ 2048) must yield the typed diagnostic; the cases fail today (no validator) |
| `closeout command` | `./scripta/check-source && ./scripta/check-compile`; `git diff --check -- src/model/qwen35moe.fab src/model/qwen35moe.proba` |
| `expected observed result` | both gates exit 0; all cross-reference pins type-check; violation rows fail with typed first-divergence diagnostics |
| `est_basis` | `pilot` — cross-reference validator in Faber (architecture-admission module class); 3–5k tokens |
| `stop condition` | a rule would require a fact outside the manifest/config (device, file ownership) → stop; that fact belongs to the Hosts/application seam |
| `depends_on` | M4 (file-serialized) |
| `gate` | module proof green. **Non-integrable alone** (partial module) — only G1 merges |

### MODEL-01-M6 — Admission entry point + identity precondition + typed refusal matrix

| Field | Value |
| --- | --- |
| `outcome` | the public admission entry on the new module composes identity precondition → config freeze (M3) → canonical tensor map (M4) → cross-reference validation (M5) and returns ADMIT with the frozen configuration + the 753-tensor receipt; the typed refusal matrix covers all seven mutation families — identity (family 6: byte length / SHA-256 divergence fails **before any architecture read**), metadata (1), name (2), shape (3), storage (4), count (5), and unsupported-but-inspectable (7: an unknown architecture name or raw GGML type stays inspectable as data per GGUF-A1a but cannot admit as `qwen35moe`); each failure returns a typed first-divergence diagnostic naming the first diverging fact that routes the repair to the owning repository |
| `exact write scope` | `src/model/qwen35moe.fab`, `src/model/qwen35moe.proba` only |
| `first failing oracle` | proba case with a wrong SHA-256 (or byte length) must fail with the identity diagnostic and never read architecture; proba case with `general.architecture = llama` must yield unsupported-but-inspectable (not a parse error); the cases fail today (no entry) |
| `closeout command` | `./scripta/check-source && ./scripta/check-compile`; `git diff --check -- src/model/qwen35moe.fab src/model/qwen35moe.proba` |
| `expected observed result` | both gates exit 0; the ADMIT + 753 receipt case type-checks on the exact frozen facts; all seven families fail closed with typed first-divergence diagnostics; the identity check precedes any architecture read |
| `est_basis` | `pilot` — admission composition + refusal matrix in Faber (closest ledger class `diagnostics-oracle`); 4–6k tokens |
| `stop condition` | admission would acquire device or file ownership → stop (Hosts/application seam); composition would weaken any mutation family → stop |
| `depends_on` | M5 (file-serialized) |
| `gate` | module proof green. **Non-integrable alone** (surface complete but needs M7/M8/M9/G1) — only G1 merges |

### MODEL-01-M7 — Exemplar adapter (executed real-file admission receipt)

| Field | Value |
| --- | --- |
| `outcome` | `exempla/gguf-admit-qwen35moe/` (new) — guarded application-owned adapter (GGUF-A1b range-source pattern): reads the bounded manifest prefix of the target artifact (first 10,991,392 bytes; **never a tensor-payload byte**), calls `gradus:model/qwen35moe` admission, prints ADMIT + the frozen configuration + the 753-tensor receipt (block schedule 30 hybrid / 10 full-attention / 1 nextn / 3 global; storage distribution f32 368 / q8_0 259 / q4_K 82 / q5_K 38 / q6_K 4 / bf16 2), exits 0; README records the exact command, revisions, model identity, expected vs observed rows, and the tensor-data guard proof |
| `exact write scope` | `exempla/gguf-admit-qwen35moe/` only (`faber.toml`, `src/main.fab`, `README.md`) |
| `first failing oracle` | the fmir run against the real artifact prints anything other than ADMIT + the exact frozen facts, or the guard would permit a tensor-region read |
| `closeout command` | `env FABER_LIBRARY_HOME=<packet root> FABER_BIN=<packet>/radix/target/debug/faber ./scripta/check-compile`; then `faber run --target fmir exempla/gguf-admit-qwen35moe -- /Users/ianzepp/Ai/models/Qwen3.6-35B-A3B-UD-Q4_K_M.gguf 10991392 0b21525e972670ed59e1812e170b27c26355381f0656ecc4e25617ece7dac58b`; `git diff --check -- exempla/gguf-admit-qwen35moe` |
| `expected observed result` | check-compile exit 0; the exemplar run prints ADMIT + all frozen table values + `753` + the block schedule + the storage distribution and exits 0; no tensor-payload byte is read (the adapter guard proves it) |
| `est_basis` | `pilot` — admission exemplar phase (precedent: `exempla/gguf-inspect` guarded adapter); 4–6k tokens |
| `stop condition` | target identity diverges on the real file → pause, route a correction to the owning repo; a short prefix read → adapter guard bug, fix the adapter not the oracle |
| `depends_on` | M6; runs in parallel with M8 (disjoint files) |
| `gate` | one fmir run exit 0 with the full ADMIT receipt. **Non-integrable alone** (executed proof lands with the surface it proves) — only G1 merges |

### MODEL-01-M8 — API/support docs

| Field | Value |
| --- | --- |
| `outcome` | docs describe the actual frozen surface: `docs/api-reference.md` gains a `## gradus:model/qwen35moe` section documenting every public symbol from the M3/M6 reports (+ any M1 accessor); `docs/module-map.md` gains the `gradus:model/qwen35moe` row + PML layer note; `docs/regression-corpus.md` inventories the new proba suite and the admission exemplum under the corpus contract and bumps the suite totals (current version `v1.3.0`; next bump for this delivery unless LIB-02/LIB-03 already bumped) |
| `exact write scope` | `docs/api-reference.md`, `docs/module-map.md`, `docs/regression-corpus.md` only |
| `first failing oracle` | the coverage snippet (mirroring `scripta/inventory-public-symbols`) reports a public qwen35moe `functio` absent from the api-reference section, or a corpus-total assertion fails |
| `closeout command` | the coverage snippet + `git diff --check -- docs/api-reference.md docs/module-map.md docs/regression-corpus.md` |
| `expected observed result` | every new public symbol appears in the api-reference section; the module-map row is present; the regression-corpus totals match the landed suite and exemplum |
| `est_basis` | `pilot` — selective docs touch (precedent: PML6-U1 re-baseline `1f4f0d2`); 4–6k tokens |
| `stop condition` | docs would describe a symbol that does not exist in the merged surface → stop, fix the doc not the code; corpus totals would require inventing counts → report the gap |
| `depends_on` | M6 (surface frozen there); runs in parallel with M7 (disjoint files) |
| `gate` | coverage snippet green. **Non-integrable alone** (docs ahead of the verified surface; zombie-doc coverage breaks) — only G1 merges |

### MODEL-01-M9 — Records + inventory re-baseline + gate registration

| Field | Value |
| --- | --- |
| `outcome` | `scripta/inventory-public-symbols` re-baselined to the merged surface (new `model/qwen35moe` row + any `model/gguf_manifest` count change from M1 + tracked total); `pml0-symbol-inventory.md` captured verbatim from a fresh run; `pml0-support-matrix.md` records the qwen35moe admission row (architecture + tensor-map facts; no execution claim); `scripta/check-compile` registers `exempla/gguf-admit-qwen35moe` |
| `exact write scope` | `scripta/inventory-public-symbols`, `docs/factory/production-ml-library/pml0-symbol-inventory.md`, `docs/factory/production-ml-library/pml0-support-matrix.md`, `scripta/check-compile` only |
| `first failing oracle` | `./scripta/inventory-public-symbols` exits non-zero (unknown module `model/qwen35moe`, stale tracked total), or `grep -c "gguf-admit-qwen35moe" scripta/check-compile` = 0 |
| `closeout command` | `./scripta/inventory-public-symbols` (must exit 0) + the check-compile grep + `git diff --check -- <the four paths>` |
| `expected observed result` | inventory exits 0 with re-baselined counts and total; symbol-inventory doc matches verbatim; support-matrix row present with no execution claim; check-compile registers the exemplum; `git diff --check` silent |
| `est_basis` | `pilot` — mechanical re-baseline + registration (precedent: `34a8a7f`); 3–5k tokens |
| `stop condition` | re-baselining would mask a symbol that should be private → stop, route to audit; a status claim would overclaim (no "audited" wording without an audit) → keep it factual |
| `depends_on` | M7 + M8 |
| `gate` | inventory exit 0 + registration grep. **Non-integrable alone** (records claim completion; only G1's validated merge makes that true) — only G1 merges |

### MODEL-01-G1 — Aggregate package validation and atomic integration

| Field | Value |
| --- | --- |
| `outcome` | merge the M1–M9 branch heads onto the MODEL-01 integration branch, run the full closeout validation once, and merge the integration branch into `factory/merge` as a single unit — `factory/merge` never observes a partial qwen35moe admission surface (no config without map, no map without admission, no module without its executed exemplar/docs/records) |
| `exact write scope` | the merge itself + a commit message naming the M1–M9 heads; no product or doc edits |
| `first failing oracle` | any closeout command fails, any closeout grep is non-empty, or the exemplar run diverges → **do not merge**; record the exact failure and stop |
| `closeout command` | lane-relative with lane-local `FABER_BIN`: `./scripta/check-source`; `./scripta/check-compile` (package + exempla incl. the new admission exemplum); `faber check --diagnostics .` ends `ok: .`; `faber run --target fmir exempla/gguf-admit-qwen35moe -- /Users/ianzepp/Ai/models/Qwen3.6-35B-A3B-UD-Q4_K_M.gguf 10991392 0b21525e972670ed59e1812e170b27c26355381f0656ecc4e25617ece7dac58b` prints ADMIT + frozen config + `753` + block schedule (30/10/1/3) + storage distribution (f32 368 / q8_0 259 / q4_K 82 / q5_K 38 / q6_K 4 / bf16 2) and exits 0; `./scripta/inventory-public-symbols` exit 0; `git diff --check` silent |
| `expected observed result` | all closeout commands pass on the merged tree; the integration branch lands on `factory/merge` as one atomic merge; the admission receipt records revisions, model identity, command, and expected vs observed rows |
| `est_basis` | `pilot` — one aggregate validation pass + merge; 3–5k tokens |
| `stop condition` | any closeout divergence → stop, record the exact failure; the gate verifies, it does not "fix" source |
| `depends_on` | M1–M9 merged on the MODEL-01 integration branch |
| `gate` | the aggregate closeout above — **the only integrable unit**; sole holder of the merge to `factory/merge` |

## Dependency And Parallelism Map

```text
factory/merge (post LIB-02 + LIB-03 aggregate gates)
  ├─ M1  manifest typed accessors            [∥ M2; disjoint files]
  └─ M2  admission oracle fixture            [∥ M1]
       └─ M3  configuration genus + freeze   [serial on src/model/qwen35moe.fab]
            └─ M4  canonical 753-tensor map + block schedule
                 └─ M5  dimension/storage cross-reference
                      └─ M6  admission entry + typed refusal matrix
                           ├─ M7  exemplar adapter (executed receipt)  [∥ M8]
                           └─ M8  API/support docs                     [∥ M7]
                                └─ M9  records + inventory + registration
                                     └─ G1  aggregate gate → factory/merge
```

- **Maximum safe parallelism**: M1 ∥ M2 at the start (disjoint files); then
  M3→M4→M5→M6 serializes on `src/model/qwen35moe.fab` (one new module surface —
  no safe parallelism on the same file); after M6, M7 ∥ M8 (disjoint files).
  Peak live Hands: 2.
- **Branch protocol**: every M1–M9 unit commits on its own `factory/<lane>`
  branch, based on the branch named in `depends_on`, with the commit message
  marked `non-integrable (MODEL-01 chain)`. G1 merges the complete integration
  branch to `factory/merge`.

## Integration Gate And Lane-Owned Validation

- `factory/merge` is the only integration stop. M1–M9 never merge to
  `factory/merge`; each is non-integrable alone (repo-gate breakage, partial
  module surface, records/docs ahead of the verified surface). G1 is the sole
  aggregate gate and owns the one package-level compile + fmir run in the
  chain.
- Lane-owned validation, named once (not copied onto child units): the lint
  lane owns stages 1–2 after integration (`check-source`, `check-compile`,
  `check-factory-goal-status`); the test lane owns stages 3–6 and broad
  suites; the merge lane owns `scripta/verify-main-consistent` and the
  fast-forward of main. `scripta/inventory-public-symbols` exit 0 is the
  release-checklist gate, satisfied by M9 + G1.

## Dispatch Serialization (Mandatory Predecessor Frontier)

1. LIB-01 (GGUF-A1c) landed on Gradus main (`2b3e41a`).
2. LIB-02 (GGUF-A2 tokenizer chain) and LIB-03 (GGUF-A3 packed storage chain)
   must each land their aggregate gates on `factory/merge` before the MODEL-01
   chain dispatches. REF-01 (dense reference rungs) is a **sibling** of
   MODEL-01 (both depend on LIB-02 + LIB-03); it is not a MODEL-01
   predecessor and never gates this dispatch.
3. MODEL-01 M1 and M2 are the first dispatchable pair (parallel, disjoint
   files). If LIB-02 or LIB-03 slips, MODEL-01 waits; the chain does not
   overlap those implementations.
4. MODEL-01 units touch no LIB-02/LIB-03 surface beyond preservation: M1
   re-uses the landed typed-array accessors and adds only a missing
   architecture-facing accessor; the module, fixture, and exemplum are new
   files.

## Successors Preserved Through CLOSE-01

This unit must not narrow, defer, or make optional any mandatory successor.
Preserved chain (campaign dependency graph):

```text
MODEL-01 -> MODEL-02 + MODEL-03 -> MODEL-04 -> EXEC-01 + EXEC-02
         -> EXEC-03 -> CAP-01 + CAP-02 -> CLOSE-01
```

The complete qwen35moe graph, 256+ token generation on both prompts in one
resident session, Metal and CUDA execution, and the Faber capstone all remain
mandatory campaign scope regardless of this unit's outcome.

## Milestone Advanced And Completion Honesty

MODEL-01 advances milestone **Q1 — executable library inputs** (admission of
the complete qwen35moe configuration is the last missing input-class fact) and
feeds **Q2 — complete model semantics**. It does **not** complete the
campaign: the campaign closes only when CLOSE-01 is accepted with both
capstone receipts and every invariant clause. A completed MODEL-01 with no
successor receipts leaves the campaign incomplete by design.

## Theme Stop Conditions (Aggregate)

- Target identity diverges (bytes, digest, architecture, counts) → pause,
  route a correction to the owning repo.
- A required architecture fact cannot be represented by the typed config →
  report the gap To mind with a default and options; do not invent a
  representation.
- The oracle (independent `llama-gguf` facts / live parse) is unavailable →
  pause the executed proof (M7/G1); the proba surface (M1–M6) can proceed.
- Any public Gradus API would acquire device ownership or file ownership →
  stop; that fact belongs to the Hosts/application seam.

## Open Questions (for Mind)

1. **M2 fixture scope addition**: `fixtures/gguf/qwen35moe-admission-oracle.md`
   is a one-file facts-pinning addition to the delivery's exact write scope
   (recommended; matches the sibling lane's split and the existing
   `*oracle*.md` pattern). If declined, M3/M4/M6 probas assert the frozen
   values as literals from this delivery's tables and no graph position
   changes.
2. **Status-line flips**: flipping GGUF-M1's status in
   `pml5-general-gguf-delivery.md` §GGUF-M1 and `CAMPAIGN.md` is outside this
   delivery's exact write scope; route to the merge lane (same atomic G1
   commit) or a follow-up docs unit.
3. **`docs/diagnostics.md` rows**: the typed diagnostic variants could get
   error-table rows there; the current write scope does not list the file —
   Mind decide whether to add it to M8.
4. **Sibling delivery artifact — RESOLVED** (need `13bce68c`, 2026-08-14):
   the planner-39 lane's `pml5-gguf-m1-qwen35moe-micro-units.md` (`df3c016`,
   frontier-corrected `c69d6a7`) carried the same M1–M9 + G1 boundaries but is
   **superseded** by this document as the single dispatch authority (§Dispatch
   Authority). No merge-lane reconciliation is needed.
5. **Regression-corpus version**: current `v1.3.0`; M8 bumps under the corpus
   contract to the next version (v1.4.0 unless LIB-02/LIB-03 already bumped)
   and records the observed version.
