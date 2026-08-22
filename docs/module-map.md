# Gradus Module Map

**Entrypoint** (thin; the full module DAG + ownership table live in
[`docs/factory/production-ml-library/pml0-module-dag.md`](factory/production-ml-library/pml0-module-dag.md)).
The authoritative per-symbol surface is [`docs/api-reference.md`](api-reference.md)
(post-no-latin English identifier surface).

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

The live documented tree has 36 modules (the U15 `gradus:mlp` leaf added to the prior 34, plus the MODEL-02 `gradus:model/moe` leaf). Module names
are unchanged. This inventory is verified against the live `src/**/*.fab` tree after the no-latin
conversion (U1–U6); it does not reuse a pre-conversion name map. The source
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
| `gradus:dtype` | `src/dtype.fab` | Versioned dtype tag + cast/round/serialize (`dtype-schema-1.0.0`) |
| `gradus:shape` | `src/shape.fab` | Shape rules: broadcast/reshape/expand, bounded product |
| `gradus:tensor` | `src/tensor.fab` | Staged-carrier tensor construction/shape/ops (not autograd-aware) |
| `gradus:math` | `src/math.fab` | Pure operation families (elementwise/reduce/matmul/cast/concat/slice) |
| `gradus:parameter` | `src/parameter.fab` | Parameter identity + traversal (`parameter-identity-schema-1.0.0`) |
| `gradus:serialize` | `src/serialize.fab` | Versioned bytes wire contract (`serialize-schema-1.0.0`) |
| `gradus:gradient` | `src/gradient.fab` | Autograd wrapper — the ONE companion-call entry (PML4) |
| `gradus:loss` | `src/loss.fab` | Losses: `mse`, `cross_entropy` + fixed-shape MSE rows (PML4) |
| `gradus:optimize` | `src/optimize.fab` | SGD optimizer state: slots, step, wires (PML4) |
| `gradus:nn` | `src/nn.fab` | Primitives: `linear`, `gelu`, `layernorm`, `rmsnorm`, `silu`, `swiglu` + fixed-shape rows (PML3; RMSNorm REF-01-U1.1, SiLU/SwiGLU REF-01-U1.2) |
| `gradus:attention` | `src/attention.fab` | SDPA + RoPE (fixed-shape row + staged surface, PML3); configurable RoPE — frequency base/scale/pair policy, consecutive-pair vs interleaved-pair (REF-01-U1.3); multi-head attention with GQA KV-head sharing, causal + RoPE, output projection (REF-01-U1.4) |
| `gradus:transformer` | `src/transformer.fab` | Transformer block (fixed-shape row + staged surface, PML3); generic dense transformer block — input RMSNorm → GQA attention (causal + RoPE) → residual → post-attn RMSNorm → SwiGLU MLP → residual, composing the U1.1/U1.2/U1.4 rows (REF-01-U1.5) |
| `gradus:mlp` | `src/mlp.fab` | Two-layer MLP: staged `forward_mlp` + annotated `forward_mlp_loss` companion (PML3-U4) |
| `gradus:train` | `src/train.fab` | Train steps, schedules, mode, RNG, dropout, and checkpoint `Checkpoint` (PML4) |
| `gradus:metrics` | `src/metrics.fab` | Defined metrics: `accuracy`, `Metric` (PML4) |
| `gradus:data` | `src/data.fab` | Stub — batching/shuffling/tokenization declared future |
| `gradus:model/artifact` | `src/model/artifact.fab` | Pathless content identity for bounded model artifacts (GGUF-A1a) |
| `gradus:model/capsule` | `src/model/capsule.fab` | Admitted-model capsule — the typed identity handoff (`capsule-schema-2.0.0`, PML2, C8; A1C-M1 clean break — schema 1 retired) |
| `gradus:model/dense_llama` | `src/model/dense_llama.fab` | Typed `llama` (SmolLM2) architecture adapter — canonical tensor-name → manifest-descriptor mapping over the GGUF-A1b surface, frozen SmolLM2-360M config, fail-closed typed diagnostics (REF-01-U1.6) |
| `gradus:model/gguf_manifest` | `src/model/gguf_manifest.fab` | Format-general GGUF v3 bounded-corpus parser plus pathless range inspection, checked tensor fragments, and typed tokenizer metadata array accessors (`texts`/`numbers`, LIB-02-U1) |
| `gradus:model/gguf` | `src/model/gguf.fab` | GGUF row admission → capsule (PML2) |
| `gradus:model/safetensors` | `src/model/safetensors.fab` | Safetensors row admission → capsule (PML2) |
| `gradus:model/dequant` | `src/model/dequant.fab` | CPU dequant of the admitted GGML block types — union set F32/F16/BF16/Q5_0/Q8_0/Q4_K/Q5_K/Q6_K (PML2; GGUF-A3 widens to BF16 + Q5_K; W1-U3 admits F16 via NativeF16Convert) |
| `gradus:model/tensor_payload` | `src/model/tensor_payload.fab` | `TensorPayload` value + `PayloadError` diagnostics — pathless payload carrier (name, absolute start, length, bytes) (GGUF-A3) |
| `gradus:model/tensor_view` | `src/model/tensor_view.fab` | `TensorView` typed view + `ViewError` + `links` bind + bounded windowed materializers `materialize_slice`/`materialize_block` (GGUF-A3) |
| `gradus:model/dense_qwen2` | `src/model/dense_qwen2.fab` | Typed `qwen2` (Qwen2.5) architecture adapter — canonical dense tensor-name → manifest-descriptor resolution (`config`/`resolve`/`render_description`) with the qwen2 deltas: tensor-set tie status, GQA head config, rope_theta 1000000 (REF-01-U1.7) |
| `gradus:model/dense` | `src/model/dense.fab` | Dense model assembly — the complete ordered dense forward graph (`forward`): embedding gather → N ordered U1.5 `dense_block` rows → final RMSNorm → output projection, assembled from the typed architecture config (`DenseConfig`) and materialized stored-weight views via canonical names; tied/untied embedding handling; zero per-row constants (REF-01-U1.8). Real-file Qwen2.5-0.5B prefill consumer: `exempla/dense-prefill-qwen2` (REF-01-U1.10; FINAL stop at radix `2ed9914e4`: packet `faber` green; PKG001 closed; rustc cargo-101, first `E0015` const `vec!`) |
| `gradus:model/qwen35moe` | `src/model/qwen35moe.fab` | qwen35moe architecture admission: frozen config + canonical 753-tensor map + dimension/storage cross-reference validation + identity-precondition admission (MODEL-01, read through the `gguf_manifest` typed accessors) |
| `gradus:model/moe` | `src/model/moe.fab` | MODEL-02 carrier-tier MoE router, deterministic top-k selection, bounded rank-3 expert dispatch, weighted accumulation, and gated shared-expert FFN |
| `gradus:tokenizer` | `src/tokenizer.fab` | Tokenizer identity + probe parity + `is_eog` (PML2/PML5) + artifact-backed byte-level BPE runtime with the composed qwen35 pre-tokenizer and special/EOG/BOS/chat policy surface (LIB-02-U2/U3; completion oracle pinned in `fixtures/tokenizer/pinned-probe-oracle.md`); capstone tokenizer phase run by `exempla/qwen36-35b-inference` (LIB-02-U4-1) |
| `gradus:cache` | `src/cache.fab` | KV-cache values + mutation rules (PML5) |
| `gradus:calibration` | `src/calibration.fab` | Residual-energy calibration bake (W5d-U1) — per-expert output-energy scores, K-recommendation curve, overlap census, 75e4ab98 provenance; measurement artifact, not a weight transform |
| `gradus:decode` | `src/decode.fab` | Decode/prefill/session/cancel + replica loop (PML5) |
| `gradus:sampling` | `src/sampling.fab` | Sampling pipeline: greedy + filters + draw (PML5) |
| `gradus:generation` | `src/generation.fab` | Generation config + cursor (PML5) |
| `gradus:gradus` | `src/gradus.fab` | Facade map — no genera |

## Layers

```text
L1  Tensor foundation   gradus:dtype, gradus:shape, gradus:math, gradus:tensor
L2  Autograd core       gradus:gradient
L3  Loss                gradus:loss
L4  Optimization        gradus:optimize
L5  NN primitives       gradus:nn
L6  Architecture blocks gradus:attention, gradus:mlp, gradus:transformer
L7  Training            gradus:train, gradus:metrics, gradus:data
PML2 Model admission    gradus:model/artifact, gradus:model/capsule,
                        gradus:model/gguf_manifest, gradus:model/gguf,
                        gradus:model/safetensors, gradus:model/dequant,
                        gradus:model/tensor_payload, gradus:model/tensor_view
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
