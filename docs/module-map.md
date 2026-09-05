# Gradus Module Map

**Entrypoint** (thin; the full module DAG + ownership table live in
[`docs/factory/production-ml-library/pml0-module-dag.md`](factory/production-ml-library/pml0-module-dag.md)).
The authoritative per-symbol surface is [`docs/api-reference.md`](api-reference.md)
(post-no-latin English identifier surface).

## Greek naming convention (Gradus-only policy)

Gradus permits a visually distinct subset of Greek letters as ordinary
identifier vocabulary on paper-fidelity surfaces. The active convention is:

| Letter | Quantity |
| --- | --- |
| `σ` | sigmoid |
| `γ` | normalization gain |
| `ε` | tolerance or normalization epsilon |
| `θ` | RoPE base or model parameter |
| `τ` | sampling temperature |
| `α`, `β` | optimizer coefficients when an optimizer surface needs them |

Only the visually distinct subset is allowed: `α β γ δ ε θ λ μ π σ τ φ ω Δ`.
Never use Latin-lookalike Greek letters (`ο ν ρ ι κ χ υ ζ`), and never use
Unicode subscripts; plain digits are canonical. This is Gradus naming policy for
paper-fidelity members and parameters only. It is not a precedent for Norma,
Triga, or Tela, whose identifiers remain word-shaped.

One `.fab` file → one import path. Nested dirs for packages.

## Examples tour

First-time path: [`docs/quickstart.md`](quickstart.md) (snippet →
[`exempla/dense-rmsnorm/`](../exempla/dense-rmsnorm/)). Open this first
for each live import that has a demo:

| Import | Open first |
| --- | --- |
| `gradus:nn` | [`exempla/dense-rmsnorm/`](../exempla/dense-rmsnorm/) |
| `gradus:attention` | [`exempla/dense-rope/`](../exempla/dense-rope/) |
| `gradus:transformer` | [`exempla/dense-block/`](../exempla/dense-block/) |
| `gradus:gradient` | [`exempla/gradient-seam/`](../exempla/gradient-seam/) |
| `gradus:mlp` | [`exempla/training-loop-mlp/`](../exempla/training-loop-mlp/) |
| `gradus:loss` | [`docs/quickstart.md`](quickstart.md) snippet; then [`exempla/training-loop-mlp/`](../exempla/training-loop-mlp/) |
| `gradus:optimize`, `gradus:train`, `gradus:metrics` | [`exempla/training-loop-mlp/`](../exempla/training-loop-mlp/) |
| `gradus:model/gguf_manifest` | [`exempla/gguf-manifest/`](../exempla/gguf-manifest/) |
| `gradus:model/tensor_payload`, `gradus:model/tensor_view` | [`exempla/gguf-materialize/`](../exempla/gguf-materialize/) |
| `gradus:model/dense_llama` | [`exempla/dense-llama-adapter/`](../exempla/dense-llama-adapter/) |
| `gradus:model/dense_qwen2` | [`exempla/dense-qwen2-adapter/`](../exempla/dense-qwen2-adapter/) |
| `gradus:model/dense` | [`exempla/dense-model/`](../exempla/dense-model/) |
| `gradus:model/qwen35moe` | [`exempla/gguf-admit-qwen35moe/`](../exempla/gguf-admit-qwen35moe/) |
| `gradus:model/moe` | MODEL-02 component surface; the real-artifact adapter is the U7 `moe-probe` handoff |
| `gradus:tokenizer` | [`exempla/qwen36-35b-inference/`](../exempla/qwen36-35b-inference/) |
| `gradus:generation` | [`exempla/generate-route/`](../exempla/generate-route/) |
| `gradus:decode`, `gradus:sampling` | [`exempla/token-generation/`](../exempla/token-generation/) |
| `gradus:cache` | [`exempla/dense-decode-smollm2/`](../exempla/dense-decode-smollm2/) |

Real-file GGUF inspection starts at
[`exempla/gguf-inspect/`](../exempla/gguf-inspect/). Real-model prefill
starts at [`exempla/dense-prefill-smollm2/`](../exempla/dense-prefill-smollm2/).

## Live modules (post-PML1–5 + correctness wave)

The live documented tree follows the current `src/**/*.fab` tree. Five former
single-file packages are nested leaves plus a docs-only facade:
`tokenizer`, `cache`, `attention`, `generation`, and `model/qwen35moe_state`.
Prefer the leaf import that owns the type. This inventory is verified against
the live `src/**/*.fab` tree after the no-latin conversion (U1–U6); it does
not reuse a pre-conversion name map. The source
surface includes the A1C capsule-schema-2.0.0 surface, LIB-02 tokenizer
runtime, GGUF-A3 tensor payload/view and widened dequant rows, REF-01
architecture adapters and dense assembly, MODEL-01 qwen35moe admission, and
MODEL-02 MoE routing, expert dispatch, and full-layer FFN composition.
See the coverage gate in [`docs/api-reference.md`](api-reference.md). The
GGUF-A1b surface has an executed 40-case synthetic package-MIR proof and
guarded real-file inspection receipts for six operator-local GGUFs. Exact
evidence and boundaries are recorded in
[`exempla/gguf-manifest/README.md`](../exempla/gguf-manifest/README.md) and
[`exempla/gguf-inspect/README.md`](../exempla/gguf-inspect/README.md).

| Import | File | Role |
| --- | --- | --- |
| `gradus:dtype` | `src/dtype.fab` | Versioned dtype tag + cast/round/serialize (`dtype-schema-1.0.0`), including BF16 storage width |
| `gradus:kernel` | `src/kernel.fab` | Shape-parameterized BF16/F32 GEMV, normalization, attention, MLP, decode, prefill, and head entries with F32 accumulation; callers supply geometry and normalization epsilon |
| `gradus:shape` | `src/shape.fab` | Shape rules: broadcast/reshape/expand with checked products |
| `gradus:tensor` | `src/tensor.fab` | Decoded F32 `NumericBlock` compute carrier with runtime shape and indexed access (not autograd-aware) |
| `gradus:storage` | `src/storage.fab` | Open encoded storage: opaque bytes plus representation identity and block metadata |
| `gradus:math` | `src/math.fab` | Pure operation families (elementwise/reduce/matmul/cast/concat/slice) |
| `gradus:parameter` | `src/parameter.fab` | Parameter identity + traversal (`parameter-identity-schema-1.0.0`) |
| `gradus:serialize` | `src/serialize.fab` | Versioned bytes wire contract (`serialize-schema-1.0.0`) |
| `gradus:gradient` | `src/gradient.fab` | Autograd wrapper — the ONE companion-call entry (PML4) |
| `gradus:loss` | `src/loss.fab` | Shape-generic typed `mse<M,N>`, decoded-carrier `mse_carrier`, and `cross_entropy` (PML4) |
| `gradus:optimize` | `src/optimize.fab` | SGD optimizer state: slots, step, wires (PML4) |
| `gradus:nn` | `src/nn.fab` | Shape-generic typed and decoded-carrier primitives: `linear`, `gelu`, `layernorm`, `rmsnorm`, `silu`, `swiglu` (PML3; RMSNorm REF-01-U1.1, SiLU/SwiGLU REF-01-U1.2) |
| `gradus:attention` | `src/attention.fab` | Docs-only facade — import `attention/rope` or `attention/gqa` |
| `gradus:attention/rope` | `src/attention/rope.fab` | RopeConfig, RopePolicy, AttentionError; configurable RoPE (REF-01-U1.3) |
| `gradus:attention/gqa` | `src/attention/gqa.fab` | SDPA, causal, rotary, multi-head, cached attention (REF-01-U1.4) |
| `gradus:transformer` | `src/transformer.fab` | Generic runtime-carrier and typed dense transformer blocks — input RMSNorm → GQA attention (causal + RoPE) → residual → post-attn RMSNorm → SwiGLU MLP → residual, composing the U1.1/U1.2/U1.4 rows (REF-01-U1.5) |
| `gradus:mlp` | `src/mlp.fab` | Two-layer MLP: decoded-carrier `forward_mlp` + annotated `forward_mlp_loss` companion (PML3-U4) |
| `gradus:train` | `src/train.fab` | Schedules, modes, RNG, dropout, and checkpoint `Checkpoint` (PML4) |
| `gradus:metrics` | `src/metrics.fab` | Defined metrics: `accuracy`, `Metric` (PML4) |
| `gradus:test_util` | `src/test_util.fab` | Shared proba-support helpers: `or_default` (U4a proba do/catch deblock) |
| `gradus:data` | `src/data.fab` | Batch leaf: deterministic shuffle over `gradus:train` Seed/Draw + order-preserving batch slicing of rank-1 i32 token-id tensors (short last batch; fail-closed empty/size bounds); tokenization still future |
| `gradus:model/artifact` | `src/model/artifact.fab` | Pathless content identity for bounded model artifacts (GGUF-A1a) |
| `gradus:model/capsule` | `src/model/capsule.fab` | Admitted-model capsule — the typed identity handoff (`capsule-schema-2.0.0`, PML2, C8; A1C-M1 clean break — schema 1 retired) |
| `gradus:model/dense_llama` | `src/model/dense_llama.fab` | Typed `llama` (SmolLM2) architecture adapter — canonical tensor-name → manifest-descriptor mapping over the GGUF-A1b surface, frozen SmolLM2-360M config, fail-closed typed diagnostics (REF-01-U1.6) |
| `gradus:model/gguf_manifest` | `src/model/gguf_manifest.fab` | Format-general GGUF v3 bounded-corpus parser plus pathless range inspection, checked tensor fragments, and typed tokenizer metadata array accessors (`texts`/`numbers`, LIB-02-U1) |
| `gradus:model/gguf` | `src/model/gguf.fab` | GGUF row admission → capsule (PML2) |
| `gradus:model/safetensors` | `src/model/safetensors.fab` | Safetensors row admission → capsule (PML2) |
| `gradus:model/dequant` | `src/model/dequant.fab` | CPU F32 decoding for supported GGML representations; the encoded storage model remains open (PML2; GGUF-A3 widens to BF16 + Q5_K; W1-U3 admits F16 via NativeF16Convert) |
| `gradus:model/tensor_payload` | `src/model/tensor_payload.fab` | `TensorPayload` value + `PayloadError` diagnostics — pathless payload carrier (name, absolute start, length, bytes) (GGUF-A3) |
| `gradus:model/tensor_view` | `src/model/tensor_view.fab` | `TensorView` typed view + `ViewError` + `links` bind from open encoded storage + bounded windowed materializers `materialize_slice`/`materialize_block` (GGUF-A3) |
| `gradus:model/dense_qwen2` | `src/model/dense_qwen2.fab` | Typed `qwen2` (Qwen2.5) architecture adapter — canonical dense tensor-name → manifest-descriptor resolution (`config`/`resolve`/`render_description`) with the qwen2 deltas: tensor-set tie status, GQA head config, rope_theta 1000000 (REF-01-U1.7) |
| `gradus:model/dense` | `src/model/dense.fab` | Dense model assembly — the complete ordered dense forward graph (`forward`): embedding gather → N ordered U1.5 `dense_block` rows → final RMSNorm → output projection, assembled from the typed architecture config (`DenseConfig`) and materialized stored-weight views via canonical names; tied/untied embedding handling; zero per-row constants (REF-01-U1.8). Real-file Qwen2.5-0.5B prefill consumer: `exempla/dense-prefill-qwen2` (REF-01-U1.10; FINAL stop at radix `2ed9914e4`: packet `faber` green; PKG001 closed; rustc cargo-101, first `E0015` const `vec!`) |
| `gradus:model/qwen35moe` | `src/model/qwen35moe.fab` | qwen35moe architecture admission: frozen config + canonical 753-tensor map + dimension/storage cross-reference validation + identity-precondition admission (MODEL-01, read through the `gguf_manifest` typed accessors) |
| `gradus:model/moe` | `src/model/moe.fab` | MODEL-02 carrier-tier MoE router, deterministic top-k selection, bounded rank-3 expert dispatch, weighted accumulation, and gated shared-expert FFN |
| `gradus:model/qwen35moe_state` | `src/model/qwen35moe_state.fab` | Docs-only facade — import schedule/session/linear_attn/full_attn |
| `gradus:model/qwen35moe_state/schedule` | `src/model/qwen35moe_state/schedule.fab` | MODEL-03 trunk schedule, LayerKind, Qwen35moeStateError |
| `gradus:model/qwen35moe_state/session` | `src/model/qwen35moe_state/session.fab` | ConvState, RecurrentState, KeyValueState, HybridSession |
| `gradus:model/qwen35moe_state/linear_attn` | `src/model/qwen35moe_state/linear_attn.fab` | Gated DeltaNet linear-attention path |
| `gradus:model/qwen35moe_state/full_attn` | `src/model/qwen35moe_state/full_attn.fab` | Full-attention KV path |
| `gradus:tokenizer` | `src/tokenizer.fab` | Docs-only facade — import identity/unicode/bpe |
| `gradus:tokenizer/identity` | `src/tokenizer/identity.fab` | TokenizerIdentity, probes, and caller-supplied EOG-set validation (PML2/PML5) |
| `gradus:tokenizer/unicode` | `src/tokenizer/unicode.fab` | Unicode categories and scanners |
| `gradus:tokenizer/bpe` | `src/tokenizer/bpe.fab` | Artifact-backed BPE runtime (LIB-02-U2/U3; GEA3-U2 `admit_gea3_tables`); capstone `exempla/qwen36-35b-inference` |
| `gradus:cache` | `src/cache.fab` | Docs-only facade — import kv/identity/structure |
| `gradus:cache/kv` | `src/cache/kv.fab` | KVCache, CacheError, append/extend/reset (PML5) |
| `gradus:cache/identity` | `src/cache/identity.fab` | CacheIdentity and identity wire |
| `gradus:cache/structure` | `src/cache/structure.fab` | KVStructure, profiles, GI4 unions |
| `gradus:calibration` | `src/calibration.fab` | Residual-energy calibration bake (W5d-U1) — per-expert output-energy scores, K-recommendation curve, overlap census, 75e4ab98 provenance; measurement artifact, not a weight transform |
| `gradus:decode` | `src/decode.fab` | Decode/prefill/session/cancel + replica loop (PML5) |
| `gradus:sampling` | `src/sampling.fab` | Sampling pipeline: greedy + filters + draw (PML5) |
| `gradus:generation` | `src/generation.fab` | Docs-only facade — import config/decoder/dense |
| `gradus:generation/config` | `src/generation/config.fab` | GenerationConfig, GenerationError, acceleration (PML5) |
| `gradus:generation/decoder` | `src/generation/decoder.fab` | Cursor, stop policy, decoder generate |
| `gradus:generation/dense` | `src/generation/dense.fab` | DenseEngine and dense generate |
| `gradus:gradus` | `src/gradus.fab` | Facade map — no genera |

### Shape-generic device entries

`gradus:kernel` exposes independently selectable, position-independent F32
entries. The signatures are shape-parameterized source/device contracts;
model widths, sequence lengths, head geometry, and KV capacity are caller or
plan facts. RMSNorm receives its epsilon from the caller.

| Entry | Idiom | Declared input shape(s) → output shape |
| --- | --- | --- |
| `rmsnorm<T,D>` | `rms_norm(input, epsilon, weight)` | `[T,D]`, `[D]` → `[T,D]` |
| `gemm_qo<T,D>` | `input · weights` | `[T,D]`, `[D,D]` → `[T,D]` |
| `gemm_kv<T,D,K>` | `input · weights` | `[T,D]`, `[D,K]` → `[T,K]` |
| `gemm_gate_up<T,D,F>` | `input · weights` | `[T,D]`, `[D,F]` → `[T,F]` |
| `gemm_down<T,F,D>` | `input · weights` | `[T,F]`, `[F,D]` → `[T,D]` |
| `rope_q` | `rope_norm<d>(0, rope_table)` | generic `[T,D]`, table `[T,P,3]` → `[T,D]` |
| `rope_k` | `rope_norm<d>(0, rope_table)` | generic `[T,K]`, table `[T,P,3]` → `[T,K]` |
| `transpose<T,d>` | `input.transpose()` | `[T,d]` → `[d,T]` |
| `score_gemm<T,d>` | `(query · key_transposed) ⊙ attention_scale` | `[T,d]`, `[d,T]`, scale `[T,T]` → `[T,T]` |
| `causal_softmax<T>` | causal masking then `scores.softmax()` | `[T,T]` → `[T,T]` |
| `context_gemm<T,d>` | `probabilities · values` | `[T,T]`, `[T,d]` → `[T,d]` |
| `swiglu<T,F>` | `gate.silu() ⊙ up` | `[T,F]`, `[T,F]` → `[T,F]` |
| `residual_add<T,D>` | `left + right` | `[T,D]`, `[T,D]` → `[T,D]` |

All entries use F32 tensors and take geometry as explicit shape parameters or
inputs. No entry embeds a model-specific width, sequence length, scale table,
or RoPE table.

### Decode device entries

The decode family is shape-parameterized for a single query row. History and
capacity are supplied by the caller; no model-specific capacity or prompt
length is part of a kernel identity.

| Entry | Idiom | Declared input shape(s) → output shape |
| --- | --- | --- |
| `decode_rmsnorm<D>` | `rms_norm(input, epsilon, weight)` | `[1,D]`, `[D]` → `[1,D]` |
| `decode_gemv_qo<D>` | `input · weights` | `[1,D]`, `[D,D]` → `[1,D]` |
| `decode_gemv_kv<D,K>` | `input · weights` | `[1,D]`, `[D,K]` → `[1,K]` |
| `decode_mlp<D,F>` | inline gate/up projections, SiLU gate, and down projection | `[1,D]`, `[D,F]`, `[D,F]`, `[F,D]` → `[1,D]` |
| `decode_rope_q` | `rope_norm<d>(0, rope_table)` | generic `[1,D]`, table `[1,P,3]` → `[1,D]` |
| `decode_rope_k` | `rope_norm<d>(0, rope_table)` | generic `[1,K]`, table `[1,P,3]` → `[1,K]` |
| `kv_append_k<K>` | `history + row` | `[K]`, `[K]` → `[K]` |
| `kv_append_v<K>` | `history + row` | `[K]`, `[K]` → `[K]` |
| `decode_key_transpose<H,C,d>` | `input.transpose()` | `[H,C,d]` → `[H,d,C]` |
| `decode_score_gemm<H,Q,T,d,C>` | `(query · key_transposed) ⊙ attention_scale` | `[H,Q,T,d]`, `[H,d,C]`, scale `[H,Q,T,C]` → `[H,Q,T,C]` |
| `decode_masked_softmax<H,Q,T,C>` | `(scores + length_mask).softmax()` | `[H,Q,T,C]`, mask `[1,C]` → `[H,Q,T,C]` |
| `decode_context_gemm<H,Q,T,C,d>` | `probabilities · values` | `[H,Q,T,C]`, `[H,C,d]` → `[H,Q,T,d]` |
| `decode_residual_add<D>` | `left + right` | `[1,D]`, `[1,D]` → `[1,D]` |

The caller supplies history selectors and length masks when a route needs
them. Kernel entries do not prescribe a fixed-capacity storage layout.

### Prefill device entries

The prefill family is shape-parameterized by prompt length, model widths, and
storage capacity. Prompt and KV geometry are caller or plan facts, rather
than frozen entry identities.

| Entry | Idiom | Declared input shape(s) → output shape |
| --- | --- | --- |
| `prefill_rmsnorm<T,D>` | `rms_norm(input, epsilon, weight)` | `[T,D]`, `[D]` → `[T,D]` |
| `prefill_gemm_qo<T,D>` | `input · weights` | `[T,D]`, `[D,D]` → `[T,D]` |
| `prefill_gemm_kv<T,D,K>` | `input · weights` | `[T,D]`, `[D,K]` → `[T,K]` |
| `prefill_mlp<T,D,F>` | inline gate/up projections, SiLU gate, and down projection | `[T,D]`, `[D,F]`, `[D,F]`, `[F,D]` → `[T,D]` |
| `prefill_rope_q` | `rope_norm<d>(0, rope_table)` | generic `[T,D]`, table `[T,P,3]` → `[T,D]` |
| `prefill_rope_k` | `rope_norm<d>(0, rope_table)` | generic `[T,K]`, table `[T,P,3]` → `[T,K]` |
| `prefill_key_transpose<T,d>` | `input.transpose()` | `[T,d]` → `[d,T]` |
| `prefill_score_gemm<T,d>` | `(query · key_transposed) ⊙ attention_scale` | `[T,d]`, `[d,T]`, scale `[T,T]` → `[T,T]` |
| `prefill_causal_softmax<T>` | `scores + causal_mask`, then softmax | `[T,T]`, mask `[T,T]` → `[T,T]` |
| `prefill_context_gemm<T,d>` | `probabilities · values` | `[T,T]`, `[T,d]` → `[T,d]` |
| `prefill_residual_add<T,D>` | `left + right` | `[T,D]`, `[T,D]` → `[T,D]` |
| `prefill_kv_write_k<C,T,K>` | `history + block · rows` | `[C,K]`, block `[C,T]`, rows `[T,K]` → `[C,K]` |
| `prefill_kv_write_v<C,T,K>` | `history + block · rows` | `[C,K]`, block `[C,T]`, rows `[T,K]` → `[C,K]` |

### Head device entries

Head entries are shape-parameterized by vocabulary and hidden dimensions.
Whether embeddings are tied is a model or plan fact supplied outside the
kernel identity.

| Entry | Idiom | Declared input shape(s) → output shape |
| --- | --- | --- |
| `head_rmsnorm<D>` | `rms_norm(input, epsilon, weight)` | `[1,D]`, `[D]` → `[1,D]` |
| `lm_head_gemv<V,D>` | `input · embeddings.transpose()` | `[1,D]`, `[V,D]` → `[1,V]` |
| `embedding_gather<V,D>` | gather rows from embeddings | `[V,D]`, ids → `[1,D]` |

**Embedding row route (design note).** `embedding_gather` receives the
embedding table and token ids; the selected row geometry is determined by
`V` and `D` at specialization time.

## Layers

```text
L1  Tensor foundation   gradus:dtype, gradus:shape, gradus:math, gradus:tensor,
                        gradus:storage
L2  Autograd core       gradus:gradient
L3  Loss                gradus:loss
L4  Optimization        gradus:optimize
L5  NN primitives       gradus:nn
L6  Architecture blocks gradus:attention, gradus:mlp, gradus:transformer
L7  Training            gradus:train, gradus:metrics, gradus:data
GEA1 Kernel            gradus:kernel — paired BF16/F32 GEMV source bodies
PML2 Model admission    gradus:model/artifact, gradus:model/capsule,
                        gradus:model/gguf_manifest, gradus:model/gguf,
                        gradus:model/safetensors, gradus:model/dequant,
                        gradus:model/tensor_payload, gradus:model/tensor_view,
                        gradus:storage
REF-01 Dense reference  gradus:model/dense_llama (llama/SmolLM2 adapter,
                        REF-01-U1.6), gradus:model/dense_qwen2 (qwen2
                        adapter, REF-01-U1.7), gradus:model/dense (dense
                        model assembly, REF-01-U1.8)
MODEL-01 Architecture   gradus:model/qwen35moe — MODEL-01
admission (specific)    architecture-specific admission over the
                        format-general model rows
MODEL-02 MoE component   gradus:model/moe — carrier-tier router, expert
surface                  dispatch, weighted accumulation, and gated shared FFN
PML2 Tokenizer identity gradus:tokenizer
PML5 Inference          gradus:decode, gradus:cache, gradus:sampling,
                        gradus:generation
W5d Calibration         gradus:calibration — residual-energy bake (W5d-U1)
SC  Shared contracts    gradus:parameter, gradus:serialize
```

## Pointers

- First-time path (snippet → first exemplum → capability tour): [`docs/quickstart.md`](quickstart.md)
- REF-01-U1.9 compiled-route consumer: [`exempla/dense-prefill-smollm2/`](../exempla/dense-prefill-smollm2/) (FINAL stop at radix `2ed9914e4`: packet faber green; rust emit reaches cargo; rustc 258 errors, first `cast cannot be followed by a method call`; no executed logits)
- Per-symbol signatures, errors, and semantics: [`docs/api-reference.md`](api-reference.md)
- Full import DAG + ownership table: [`docs/factory/production-ml-library/pml0-module-dag.md`](factory/production-ml-library/pml0-module-dag.md)
  (the DAG's §1 counts snapshot predates PML3–5 and the correctness wave;
  the live module table above and the inventory
  [`pml0-symbol-inventory.md`](factory/production-ml-library/pml0-symbol-inventory.md)
  are the current authority — the DAG's import edges and ownership table
  remain valid architecture)
- API shape posture: [`docs/api-shape-policy.md`](api-shape-policy.md)
- Public symbol inventory (machine-checked): [`docs/factory/production-ml-library/pml0-symbol-inventory.md`](factory/production-ml-library/pml0-symbol-inventory.md)
