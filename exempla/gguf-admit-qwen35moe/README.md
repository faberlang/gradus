# GGUF-A1b guarded real-file qwen35moe admission

This package is the application-owned file adapter for
`gradus:model/qwen35moe`. It resolves one local path, reads the independently
bounded header/table prefix once (the first `data_expectata` bytes), calls the
public admission entry (`qwen35moe.admitto`), and prints the ADMIT receipt: the
frozen configuration + the 753-tensor receipt (block schedule + storage
distribution). Gradus receives and retains no path, file handle, mapping,
callback, or whole-model payload.

This is model admission, not inference. The local file is operator evidence
and is not committed or redistributed.

## Tensor-data guard

The second CLI operand is the data offset from the independent GGUF reader
(10,991,392 for the pinned artifact). The adapter calls
`solum.partem(path, 0, oracle_offset)` once and rejects a short prefix; the
corpus it hands Gradus is exactly those bytes, so `manifestum.parse` sees
`corpus_longitudo == data_inceptum` and its "bounded GGUF corpus contains
bytes from the data region" rejection (`Superfluitas`) cannot trigger. The
adapter never requests a byte at or beyond the data offset, so a passing run
proves that no tensor-payload byte was read. The CLI also feeds the operator-
measured SHA-256 digest and byte length into the identity precondition, which
fails before any architecture read.

## Model identity

The pinned artifact facts below were measured with `stat -f '%z'` and
`shasum -a 256`; the 10,991,392-byte table prefix, the 55 metadata entries,
and the 753-tensor directory were read independently with
`/opt/homebrew/bin/llama-gguf <file> r 1`.

| Fact | Value |
| --- | --- |
| Local artifact | `/Users/ianzepp/Ai/models/Qwen3.6-35B-A3B-UD-Q4_K_M.gguf` |
| Bytes | 22,663,387,424 |
| SHA-256 | `0b21525e972670ed59e1812e170b27c26355381f0656ecc4e25617ece7dac58b` |
| Data offset (oracle) | 10,991,392 |
| Metadata entries | 55 |
| Tensors | 753 |
| Architecture | `qwen35moe` |

## Revisions

- Gradus `model/qwen35moe` admission surface (MODEL-01-M3…M6) on branch
  `factory/hand-13`:
  - M3 configuration genus + metadata freeze
  - M4 canonical 753-tensor map + block schedule
  - M5 dimension/storage cross-reference validation
  - M6 admission entry + identity precondition + typed refusal matrix
    (`0c28ca3`)
- This exemplar: MODEL-01-M7 (`<commit>`), non-integrable (MODEL-01 chain).

## Expected vs observed rows

Expected values are the frozen architecture configuration and the 753-tensor
receipt from the MODEL-01 delivery; observed values are what the executed
exemplar printed against the real artifact.

| Row | Expected | Observed |
| --- | --- | --- |
| ADMIT | `qwen35moe` | `qwen35moe` |
| `general.architecture` | `qwen35moe` | `qwen35moe` |
| `general.file_type` | 15 | 15 |
| `general.quantization_version` | 2 | 2 |
| `qwen35moe.block_count` | 41 | 41 |
| `qwen35moe.context_length` | 262144 | 262144 |
| `qwen35moe.embedding_length` | 2048 | 2048 |
| `qwen35moe.attention.head_count` | 16 | 16 |
| `qwen35moe.attention.head_count_kv` | 2 | 2 |
| `qwen35moe.attention.key_length` | 256 | 256 |
| `qwen35moe.attention.value_length` | 256 | 256 |
| `qwen35moe.attention.layer_norm_rms_epsilon` | 1e-6 | <observed> |
| `qwen35moe.rope.freq_base` | 10000000.0 | <observed> |
| `qwen35moe.rope.dimension_count` | 64 | 64 |
| `qwen35moe.rope.dimension_sections` | `[11,11,10,0]` | `[11,11,10,0]` |
| `qwen35moe.expert_count` | 256 | 256 |
| `qwen35moe.expert_used_count` | 8 | 8 |
| `qwen35moe.expert_feed_forward_length` | 512 | 512 |
| `qwen35moe.expert_shared_feed_forward_length` | 512 | 512 |
| `qwen35moe.ssm.conv_kernel` | 4 | 4 |
| `qwen35moe.ssm.state_size` | 128 | 128 |
| `qwen35moe.ssm.group_count` | 16 | 16 |
| `qwen35moe.ssm.time_step_rank` | 32 | 32 |
| `qwen35moe.ssm.inner_size` | 4096 | 4096 |
| `qwen35moe.full_attention_interval` | 4 | 4 |
| `qwen35moe.nextn_predict_layers` | 1 | 1 |
| `tokenizer.ggml.model` | `gpt2` | `gpt2` |
| `tokenizer.ggml.pre` | `qwen35` | `qwen35` |
| `tokenizer.ggml.tokens` | 248320 | 248320 |
| `tokenizer.ggml.token_type` | 248320 | 248320 |
| `tokenizer.ggml.merges` | 247587 | 247587 |
| `tokenizer.ggml.eos_token_id` | 248046 | 248046 |
| `tokenizer.ggml.padding_token_id` | 248055 | 248055 |
| `tokenizer.ggml.bos_token_id` | 248044 | 248044 |
| `tokenizer.ggml.add_bos_token` | false | false |
| `tensors total` | 753 | 753 |
| block schedule | 30 hybrid / 10 full-attention / 1 nextn / 3 global | 30/10/1/3 |
| storage distribution | f32 368 / q8_0 259 / q4_K 82 / q5_K 38 / q6_K 4 / bf16 2 | 368/259/82/38/4/2 |

The receipt proves real-file qwen35moe admission through the public surface on
the exact frozen facts. It does not prove tokenizer behavior, tensor
materialization, model semantics, logits, token generation, CPU inference, or
GPU inference. Those remain GGUF-A2/A3 and GGUF-A7.

## Command

From the Hand packet:

```bash
cd /Users/ianzepp/work/faberlang/worktrees/hand-13/gradus
env FABER_LIBRARY_HOME=/Users/ianzepp/work/faberlang/worktrees/hand-13 \
  /Users/ianzepp/work/faberlang/worktrees/hand-13/radix/target/debug/faber \
  run --target fmir exempla/gguf-admit-qwen35moe -- \
  /Users/ianzepp/Ai/models/Qwen3.6-35B-A3B-UD-Q4_K_M.gguf \
  10991392 \
  0b21525e972670ed59e1812e170b27c26355381f0656ecc4e25617ece7dac58b
```

The digest is re-derived externally with `shasum -a 256` and compared to the
pinned value before a run counts as evidence; the FMIR surface has no sha-256
primitive.

## Observed receipt

The exemplar files are complete per the M7 contract, but the executed proof is
**blocked by a defect in the M6 surface it consumes** (`src/model/qwen35moe.fab`,
committed `0c28ca3`) — not by the adapter. The FMIR consumer analysis of
`gradus:model/qwen35moe` fails closed before the exemplar's own code runs:

- `faber check exempla/gguf-admit-qwen35moe` → `SEM004.unknown_struct_field`
  at `corpus.identitas.algorithmus` in `admitto`: the module reads fields of
  `artifact.IdentitasContenuti` without importing `gradus:model/artifact`
  directly (only transitively through `gguf_manifest`).
- With that import added temporarily, the FMIR run then fails at the package
  MIR merge: `identity-bearing enum ErrorAdmissionisQwen35moe variant
  ReferentiaDiversa is not resolvable in the consumer analysis`. The public
  error enum nests sibling public enums as variant payloads; the consumer
  import installs nominal shells in BTreeMap (alphabetical) order and imports
  enum variant payloads eagerly in Phase 1 (struct fields are deferred to
  Phase 2), so the payload shells that sort after the carrier enum are not yet
  installed when its variants import. A minimal reproduction confirmed the
  shape: payload-enum-before-carrier imports fine; carrier-before-payload
  fails closed. Any FMIR consumer of the module fails the same way.

Corrective options (routed via Vivi need): defer enum variant payload imports
to Phase 2 in the compiler seam, or rework the M6 public error surface so its
variants carry `textus` causes (matching the `GgufManifestError` pattern) and
add the direct `artifact` import. The exemplar itself is unchanged by either
fix and is expected to print the receipt table below once the surface is
consumable.

Expected receipt (blocked run — to be captured after the correction):

```text
<receipt>
```
