# Gradus Module Map

**Entrypoint** (thin; the full module DAG + ownership table live in
[`docs/factory/production-ml-library/pml0-module-dag.md`](factory/production-ml-library/pml0-module-dag.md)).
The authoritative per-symbol surface is [`docs/api-reference.md`](api-reference.md)
(`gradus-api-reference v1.0.0`).

One `.fab` file → one import path. Nested dirs for packages.

## Live modules (post-PML1–5 + correctness wave)

The live tree has 27 modules and 612 declared functions. The GGUF-A1a parser
surface is compile/typecheck-validated and has an executed bounded package-MIR
proof over deterministic in-source corpora; its exact receipt and boundaries
are recorded in
[`exempla/gguf-manifest/README.md`](../exempla/gguf-manifest/README.md).

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
| `gradus:nn` | `src/nn.fab` | Primitives: `linear`, `gelu`, `layernorm` + fixed-shape rows (PML3) |
| `gradus:attention` | `src/attention.fab` | SDPA + RoPE (fixed-shape row + staged surface, PML3) |
| `gradus:transformer` | `src/transformer.fab` | Transformer block (fixed-shape row + staged surface, PML3) |
| `gradus:train` | `src/train.fab` | Train steps, schedules, mode, RNG, dropout, checkpoint `Tabula` (PML4) |
| `gradus:metrics` | `src/metrics.fab` | Defined metrics: `accuratezza`, `Metricum` (PML4) |
| `gradus:data` | `src/data.fab` | Stub — batching/shuffling/tokenization declared future |
| `gradus:model/artifact` | `src/model/artifact.fab` | Pathless content identity for bounded model artifacts (GGUF-A1a) |
| `gradus:model/capsule` | `src/model/capsule.fab` | Admitted-model capsule — the typed identity handoff (PML2, C8) |
| `gradus:model/gguf_manifest` | `src/model/gguf_manifest.fab` | Format-general GGUF v3 metadata/tensor manifest parser (GGUF-A1a) |
| `gradus:model/gguf` | `src/model/gguf.fab` | GGUF row admission → capsule (PML2) |
| `gradus:model/safetensors` | `src/model/safetensors.fab` | Safetensors row admission → capsule (PML2) |
| `gradus:model/dequant` | `src/model/dequant.fab` | CPU dequant of the admitted GGML block types (PML2) |
| `gradus:tokenizer` | `src/tokenizer.fab` | Tokenizer identity + probe parity + `est_eog` (PML2/PML5) |
| `gradus:cache` | `src/cache.fab` | KV-cache values + mutation rules (PML5) |
| `gradus:decode` | `src/decode.fab` | Decode/prefill/session/cancel + replica loop (PML5) |
| `gradus:sampling` | `src/sampling.fab` | Sampling pipeline: greedy + filters + draw (PML5) |
| `gradus:generation` | `src/generation.fab` | Generation config + cursor (PML5) |
| `gradus:gradus` | `src/gradus.fab` | Facade map — no genera; MLP forward convenience |

## Layers

```text
L1  Tensor foundation   gradus:dtype, gradus:shape, gradus:math, gradus:tensor
L2  Autograd core       gradus:gradient
L3  Loss                gradus:loss
L4  Optimization        gradus:optimize
L5  NN primitives       gradus:nn
L6  Architecture blocks gradus:attention, gradus:transformer
L7  Training            gradus:train, gradus:metrics, gradus:data
PML2 Model admission    gradus:model/artifact, gradus:model/capsule,
                        gradus:model/gguf_manifest, gradus:model/gguf,
                        gradus:model/safetensors, gradus:model/dequant
PML2 Tokenizer identity gradus:tokenizer
PML5 Inference          gradus:decode, gradus:cache, gradus:sampling,
                        gradus:generation
SC  Shared contracts    gradus:parameter, gradus:serialize
```

## Pointers

- Per-symbol signatures, errors, and semantics: [`docs/api-reference.md`](api-reference.md)
- Full import DAG + ownership table: [`docs/factory/production-ml-library/pml0-module-dag.md`](factory/production-ml-library/pml0-module-dag.md)
  (the DAG's §1 counts snapshot predates PML3–5 and the correctness wave;
  the live module table above and the inventory
  [`pml0-symbol-inventory.md`](factory/production-ml-library/pml0-symbol-inventory.md)
  are the current authority — the DAG's import edges and ownership table
  remain valid architecture)
- API shape posture: [`docs/api-shape-policy.md`](api-shape-policy.md)
- Public symbol inventory (machine-checked): [`docs/factory/production-ml-library/pml0-symbol-inventory.md`](factory/production-ml-library/pml0-symbol-inventory.md)
