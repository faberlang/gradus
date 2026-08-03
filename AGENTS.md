# Gradus Agent Instructions

Gradus is the public Faber source library for `gradus:*` imports — automatic
differentiation, loss functions, optimizers, neural-network primitives, and
training-loop mechanics. This repo owns `.fab` source under `src/`; Radix and
`faber` consume it through `FABER_LIBRARY_HOME`, usually the parent
`faberlang/` directory in local development.

Gradus is fully self-contained. It does not import from Norma or any other
sibling library. A Gradus user never needs to decide between `norma:*` and
`gradus:*` — if you need autograd or ML, import from Gradus; if you need plain
math, import from Norma. Duplication between them is intentional isolation.

GPU execution, kernel fusion, and tensor memory management are Radix and host
concerns. Gradus owns device-neutral mathematical contracts; the compiler
and host execute them.

## Module layout (Norma / Triga style)

One `.fab` file → one import path. Nested dirs for packages.

| Import | Role |
| --- | --- |
| `gradus:math` | Tensor-aware math foundation (own copy; independent of Norma) |
| `gradus:tensor` | Tensor construction, shape/dtype, basic ops (plain values — not autograd-aware) |
| `gradus:gradient` | `@ radix backward` wrapper ergonomics; forward + companion gradient calls |
| `gradus:loss` | Loss functions (MSE, cross-entropy) |
| `gradus:optimize` | Optimizers (SGD, Adam) and learning-rate schedules |
| `gradus:nn` | Differentiable primitives: Linear, activation, norm, embedding, dropout |
| `gradus:attention` | Scaled dot-product attention, causal masking, multi-head |
| `gradus:transformer` | Transformer block, positional encoding, output head |
| `gradus:train` | Training loop, metrics, checkpointing |
| `gradus:data` | Batching, shuffling, tokenization |
| `gradus:gradus` | Facade map only (no genera) |

Nested package dirs only with **≥2 modules** (prefer ≥3). A single nested file
is flattened to a top-level leaf (`gradus:optimize`, not
`gradus:optimize/sgd`).

Full map: [`docs/module-map.md`](docs/module-map.md). API shape:
[`docs/api-shape-policy.md`](docs/api-shape-policy.md). Target architecture:
[`docs/factory/gradus-ml-foundation/GOAL.md`](docs/factory/gradus-ml-foundation/GOAL.md).

## Corpus

`corpus/` holds training demos that exercise the public `gradus:*` surface.
The primary forcing-function demo is `corpus/nanogpt-shakespeare/` — a
minimal nanoGPT implementation trained on Shakespeare text. This demo runs on
CPU (slowly) for correctness and forces the GPU gradient path to close for
real iteration speed. Details and per-demo commands: `corpus/README.md`.

Demos should exercise the public `gradus:*` surface and feed gaps back into
the library or into Radix mir-swarm rungs, not grow workarounds.

## Rules

- Keep public modules under `src/**/*.fab`.
- Keep package tests as co-located `src/**/*.proba` (`name.fab` + `name.proba`).
- Keep instructional demos under `exempla/**/*.fab`.
- Keep training demos under `corpus/<slug>/`.
- Do not add `@ externa` or `@ subsidia`.
- Optional genus fields use `sponte`.
- Prefer leaf imports; do not grow genera on the `gradus:gradus` facade.
- Prefer receiver methods on genera; free functions for constructors / scalars
  / generators only.
- Nested package directories need at least two leaves (prefer three+).
- Do not import from Norma or any sibling library. Gradus is self-contained.
- Never `importa` a `.proba` file; shared helpers stay in `.fab` modules.
- `@ radix backward` annotations live behind the `gradient` module wrapper, not
  leaked into every public function signature.

## Validation

```bash
./scripta/check-source
./scripta/check-compile
```
