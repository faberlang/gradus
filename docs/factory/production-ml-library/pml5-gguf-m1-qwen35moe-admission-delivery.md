# Delivery: GGUF-M1 — qwen35moe Admission And Tensor Map (MODEL-01)

**Campaign**: Radix `gpu-production-readiness` Qwen3.6 invariant —
[MODEL-01](../../../../radix/docs/factory/gpu-production-readiness/CAMPAIGN.md)
**Semantic authority**: [`pml5-general-gguf-delivery.md`](pml5-general-gguf-delivery.md) §GGUF-M1
**Campaign mode**: run
**Repo**: `gradus`
**Status**: READY FOR DELIVERY — implementation gated on predecessor receipts
**Planner**: planner-25 (fresh lowering; no planner-1..19 artifacts reused)
**Date**: 2026-08-13
**Integration stop**: `factory/merge` only; this delivery does not fast-forward any main branch

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

The admission validates every canonical tensor against the frozen config:

- `embedding_length` 2048 is the first stored dim of `attn_*` weights, norms,
  and `ffn_*_shexp`/`ffn_*_inp*` tensors.
- `expert_count` 256 is the third stored dim of the three `*_exps` rank-3
  tensors in every block.
- `expert_feed_forward_length` 512 is the second stored dim of
  `ffn_*_exps` and the `ffn_*_shexp` weights.
- `ssm.state_size` 128 matches `ssm_norm.weight`; `ssm.time_step_rank` 32
  matches `ssm_a`, `ssm_dt.bias`, and the second stored dim of
  `ssm_alpha`/`ssm_beta`.
- `ssm.conv_kernel` 4 matches the first stored dim of `ssm_conv1d.weight`.
- `ssm.inner_size` 4096 matches `ssm_out.weight`/`attn_output.weight` first
  stored dim and `attn_gate.weight` second stored dim.
- `attention.head_count_kv` 2 × `attention.key_length` 256 = 512 = the second
  stored dim of `attn_k.weight`/`attn_v.weight`; `attn_q_norm.weight` and
  `attn_k_norm.weight` carry 256.
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
| GGUF-A1a manifest parser | `exempla/gguf-manifest` 31 PASS / 0 FAIL | implemented |
| GGUF-A1b range seam + real-file inspection | `exempla/gguf-inspect` 6-file guarded receipt | implemented |
| GGUF-A1c capsule/caller clean break | `pml5-general-gguf-delivery.md` §GGUF-A1c | **next mandatory — not yet landed** |
| GGUF-A2 tokenizer runtime (LIB-02) | campaign MODEL-01 depends on LIB-02 | not yet landed |
| GGUF-A3 packed storage (LIB-03) | campaign MODEL-01 depends on LIB-03 | not yet landed |

Per the campaign dependency table, MODEL-01 cannot be dispatched to a Hand
before the LIB-02 and LIB-03 predecessor receipts are accepted; the delivery
authority's unit graph additionally orders GGUF-A1c before GGUF-A2/A3. This
delivery artifact is lowered now so the unit is implementation-ready when the
predecessor receipts land; it does not claim predecessor completion.

## Exact Write Scope

Only the files below. No product source outside this list, no docs outside
the listed set.

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

## Closeout Command

```bash
cd /Users/ianzepp/work/faberlang/worktrees/<hand>/gradus
./scripta/check-source
env FABER_LIBRARY_HOME=/Users/ianzepp/work/faberlang/worktrees/<hand> \
  FABER_BIN=/Users/ianzepp/work/faberlang/worktrees/<hand>/radix/target/debug/faber \
  ./scripta/check-compile
env FABER_LIBRARY_HOME=/Users/ianzepp/work/faberlang/worktrees/<hand> \
  /Users/ianzepp/work/faberlang/worktrees/<hand>/radix/target/debug/faber \
  check --diagnostics .
env FABER_LIBRARY_HOME=/Users/ianzepp/work/faberlang/worktrees/<hand> \
  /Users/ianzepp/work/faberlang/worktrees/<hand>/radix/target/debug/faber \
  run --target fmir exempla/gguf-admit-qwen35moe -- \
  /Users/ianzepp/Ai/models/Qwen3.6-35B-A3B-UD-Q4_K_M.gguf \
  10991392 \
  0b21525e972670ed59e1812e170b27c26355381f0656ecc4e25617ece7dac58b
git diff --check -- src/model/qwen35moe.fab src/model/qwen35moe.proba \
  src/model/gguf_manifest.fab src/model/gguf_manifest.proba \
  docs/module-map.md docs/api-reference.md docs/regression-corpus.md \
  docs/factory/production-ml-library/pml0-symbol-inventory.md \
  docs/factory/production-ml-library/pml0-support-matrix.md \
  exempla/gguf-admit-qwen35moe scripta/check-compile
```

## Expected Observed Result

- `check-source` and `check-compile` exit 0; `faber check` ends `ok: .`;
  `git diff --check` silent.
- The admission exemplar prints `ADMIT` with the frozen configuration (all
  values from the table above), `753` tensors, the block schedule
  (30 hybrid / 10 full-attention / 1 nextn / 3 global), and the storage
  distribution (f32 368 / q8_0 259 / q4_K 82 / q5_K 38 / q6_K 4 / bf16 2),
  then exits 0. The receipt records the exact command, working directory,
  artifact identity, and observed output.
- The package-MIR mutation suite prints PASS for every named positive case
  and every mutation family fails with a typed first-divergence diagnostic.
- No real-file tensor payload byte is read (the adapter guard proves it).

## Work-Token Estimate

- `est_work_tokens`: 90k–150k.
- `est_basis`: `pilot` (first unit of a new class; no ledger class exists for
  GGUF-M1 qwen35moe admission — the ledger's closest classes are
  `diagnostics-oracle` and `compiler-surface-feature`, neither of which
  covers a Gradus architecture-admission module; this unit seeds the class
  baseline).
- `tool_latency`: `check-compile`/`faber check` and the package-MIR exemplar
  run through the lane-local Radix faber binary, ~2–5 min cold; no GPU or
  long-running device work.

## Named Split Boundary

MODEL-01 is one coherent unit: admission + canonical tensor map for the exact
target. It is not split further because the done oracle is a single executed
admission receipt. It is also **not** widened: MoE router/expert execution
(MODEL-02), hybrid SSM/attention state (MODEL-03), full-model reference
inference (MODEL-04), tokenizer runtime (LIB-02), and packed storage
materialization (LIB-03) are separate units with their own receipts.

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

## Stop Conditions

- Target identity diverges (bytes, digest, architecture, counts) → pause,
  route a correction to the owning repo.
- A required architecture fact cannot be represented by the typed config →
  report the gap To mind with a default and options; do not invent a
  representation.
- The oracle (independent `llama-gguf` facts / live parse) is unavailable →
  pause the executed proof; the proba mutation surface can proceed.
- Any public Gradus API would acquire device ownership or file ownership →
  stop; that fact belongs to the Hosts/application seam.
