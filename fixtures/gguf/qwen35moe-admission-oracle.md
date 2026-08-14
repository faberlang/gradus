# Qwen35Moe Admission Oracle — pinned facts fixture

**Unit**: MODEL-01-M2 (admission oracle facts fixture) — `gradus`
**Source authority**: `docs/factory/production-ml-library/pml5-gguf-m1-qwen35moe-admission-delivery.md`
(planner-25, head `76d306c`) — single dispatch authority; values pinned
verbatim from its tables. All facts were read live from the target artifact
on 2026-08-13 (independent `llama-gguf` key listing + direct wire-value
parse).
**Nature**: facts only. No GGUF bytes, no execution claims, no codec
behavior — this fixture pins the frozen admission facts for
`gradus:model/qwen35moe`.
**Status**: facts frozen — any divergence from the delivery tables is a
stop condition (do not invent; record to the owning repo).

## Target identity

The identity is the admission precondition: a manifest whose content
identity does not match these three facts — byte length, SHA-256,
architecture — is rejected before any architecture read (filename is
provenance only).

| Fact | Frozen value |
| --- | --- |
| Filename | `Qwen3.6-35B-A3B-UD-Q4_K_M.gguf` |
| Byte length | 22,663,387,424 |
| SHA-256 | `0b21525e972670ed59e1812e170b27c26355381f0656ecc4e25617ece7dac58b` |
| GGUF version | 3 |
| Alignment | 32 |
| Data offset | 10,991,392 |
| Metadata entries | 55 |
| Tensor count | 753 |
| Architecture | `qwen35moe` |

## Frozen architecture configuration

All metadata rows from the delivery's frozen configuration table are
pinned verbatim below. The tokenizer rows freeze the tokenizer *identity
facts* only; tokenizer execution (encode/decode/EOG/chat-template) is
GGUF-A2's unit.

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

## Canonical 753-tensor map

Raw tensor directory as stored in the target artifact (dims in GGUF file
order; GGUF stores the last logical dimension first). Storage types are the
raw GGML type IDs resolved to names.

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

Rank-3 expert tensors: **123** (41 blocks × 3 expert tensors —
`ffn_down_exps`, `ffn_gate_exps`, `ffn_up_exps`). For known K-quant
layouts, block divisibility checks against the first GGML dimension
(q4_K/q5_K/q6_K blocks = 256 elements; 256 divides the expert axis).

## Typed refusal matrix (seven families)

For each mutation family below, the admission returns a **typed
first-divergence diagnostic** naming the first diverging fact (metadata
key / tensor name / shape / storage / count), not a generic parse error.
The first divergent fact in the divergence receipt routes the repair to
the owning repository (Gradus for admission, Radix/Faber/Hosts only for
facts that belong to their seam).

1. **Metadata** — any frozen `qwen35moe.*` value changed (block_count,
   embedding_length, head counts, expert counts, SSM sizes, rope facts,
   nextn count); a required key missing; an extra unknown key that shadows
   a required fact.
2. **Name** — a canonical tensor renamed, duplicated, or replaced by an
   unknown name.
3. **Shape** — a canonical tensor's shape or rank changed (including
   rank-3 → rank-2 expert tensors).
4. **Storage** — a canonical tensor's raw GGML type changed (including the
   bf16/f32 anomaly in `blk.40` being "corrected" away, and mixed-storage
   collapsing to one global row).
5. **Count** — tensor count ≠ 753, metadata count ≠ 55, or a block family
   count out of schedule.
6. **Identity** — byte length or SHA-256 divergence (fail before any
   architecture read).
7. **Unsupported-but-inspectable** — an *unknown* architecture name or raw
   GGML type stays inspectable as data (GGUF-A1a rule) but cannot admit as
   `qwen35moe`.

## Provenance

- Facts source: `pml5-gguf-m1-qwen35moe-admission-delivery.md` tables
  (§Frozen Target Identity, §Frozen Architecture Configuration,
  §Canonical 753-Tensor Map, §Mutation Fail-Closed Requirements), read
  live from the artifact on 2026-08-13.
- The operator-local artifact (`Qwen3.6-35B-A3B-UD-Q4_K_M.gguf`) is local
  corpus evidence and is never committed; this fixture pins facts only.
- Any re-pin is an operator decision (campaign stop conditions); a change
  to a frozen value MUST update this document and the delivery tables
  together.
