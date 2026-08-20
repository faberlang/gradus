# Gradus — the Faber Autograd and ML Library

**Gradus** (Latin: "step, pace, degree" — the root of *gradient*) is Faber's
native library for automatic differentiation, loss functions, optimizers,
neural-network primitives, and training mechanics.

Gradus wraps the compiler's reverse-mode autograd transform (`radix-air`)
into clean Faber source contracts. The architecture is JAX-shaped, not
PyTorch-shaped: models are pure functions with explicit parameters, gradients
are compiler-generated companion functions, and the backward pass is
generated code — not a runtime tape replay.

## Install

Local `faber` resolves `gradus:*` from the shared library home:

```text
$FABER_LIBRARY_HOME/gradus/src/**/*.fab
```

In local Faber development, `FABER_LIBRARY_HOME` is usually the parent
`faberlang/` directory that contains sibling checkouts:

```text
faberlang/
  radix/
  norma/
  triga/
  gradus/      # this repo
```

```bash
export FABER_LIBRARY_HOME=/path/to/faberlang
```

Install into the shared package store (from sibling `cista`):

```bash
cargo run -p cista -- install \
  --path ../gradus \
  --target-language rust \
  --store "${CISTAE_HOME:-$HOME/.faber/cistae}"
```

That snapshots product `*.fab` under `src/` to
`$CISTAE_HOME/gradus/<version>/interfaces/` (interfaces-only; `*.proba`
test sources are excluded). `faber` still uses `FABER_LIBRARY_HOME` until
tooling consumes packaged paths.

## Example

From an empty directory, with `FABER_LIBRARY_HOME` set as above and a
current `faber` binary on `PATH`:

`faber.toml`:

```toml
[package]
name = "hello-gradus"
version = "0.1.0"
edition = "2026"

[paths]
source = "src"
entry = "main.fab"

[build]
target = "fmir"
kind = "bin"

[locale]
locale = "en"
```

`src/main.fab` (same `import from` / `main` / `from_flat` shape as
`exempla/gradient-seam/src/main.fab` and `exempla/*/src/main.fab`):

```fab
import from "gradus:loss" loss

main {
    const tensor<f32, []> seed ← vacua
    const list<int> shape_2x2 ← [2, 2]
    const tensor<f32, [2, 2]> prediction ← seed.from_flat([1.0, 2.0, 3.0, 4.0], shape_2x2)
    const tensor<f32, [2, 2]> target ← seed.from_flat([1.0, 2.0, 3.0, 3.0], shape_2x2)
    const f32 value ← loss.mse_2x2(prediction, target)
    print value
}
```

```bash
faber check .
```

`loss.mse_2x2` is mean squared error over a 2×2 f32 pair; the snippet's
inputs yield `0.25`. `faber check` is the standing proof that the import
and call type-check. `faber run` of packages that import `gradus:*` is
not claimed here — the compiler cannot yet execute library-to-library
calls. Worked demos live under `exempla/` (start with
`exempla/gradient-seam/` for the import shape, or
`exempla/dense-rmsnorm/` for an in-memory executed row).

## Status

Gradus is pre-1.0 with a clean-break posture; APIs may change. See
[`docs/compatibility-policy.md`](docs/compatibility-policy.md).

What ships today is the **structural** surface: compile-validated,
proba-pinned source contracts. Executed value-identity — running a
training loop or model forward and matching goldens — is blocked on the
compiler's library-import execution gap. No GPU training or executed
performance is claimed here.

| Layer | State |
| --- | --- |
| Foundation (dtype, shape, tensor, math) | Shipped |
| Parameters and serialization | Shipped |
| Gradient wrapper, loss, SGD, training, metrics | Shipped (structural) — `gradients_simple_loss`, `mse` / `cross_entropy`, `SgdState` / `step`, `Checkpoint`, `accuracy` / `Metric` |
| NN primitives, attention, transformer | Shipped (structural); several `exempla/dense-*` packages have executed in-memory proofs |
| Model admission (capsule, GGUF, Safetensors) | Shipped; GGUF inspection has executed real-file receipts. `tensor_view.links` binds a payload to a manifest. Architecture adapters do not claim inference |
| Tokenizer identity | Shipped |
| Inference (decode, cache, sampling, generation) | Shipped (structural) |
| Dense forward (`gradus:model/dense` `forward`) | Shipped over synthetic graphs; not a real-model inference claim |
| GPU training / executed runs | Not claimed |

Campaign ledgers, unit receipts, and per-symbol coverage live in
[`docs/api-reference.md`](docs/api-reference.md),
[`docs/module-map.md`](docs/module-map.md), and
[`docs/factory/production-ml-library/`](docs/factory/production-ml-library/).
Exemplum receipts sit next to each demo under `exempla/`.

The compiler's reverse-mode AD transform covers 16 of 18 AIR tensor ops
with VJPs; two ops (broadcast, reduce) have partial support. Gradus wraps
that capability into a self-contained user library.

GGUF metadata and tensor directories are capped at 4,096 entries and
individual retained reads at 64 MiB. Gradus retains no path, URL, file
handle, mapping, source function, or whole-model payload. Format and
range proofs live in `exempla/gguf-manifest/` and `exempla/gguf-inspect/`.

## Design principles

- **JAX-shaped, not PyTorch-shaped.** Models are pure functions:
  `(params, x) → y`. No `nn.Module` class hierarchy, no hidden parameter
  registration. Parameters are explicit values carried in records.
- **Self-contained.** Gradus does not import from Norma or any sibling library.
  A Gradus user imports only from `gradus:*`. Duplication with Norma is
  intentional isolation, not a bug.
- **Device-neutral.** Gradus public types are pure mathematical contracts.
  GPU execution, kernel fusion, and memory management are Radix and host
  concerns. Gradus describes *what* to compute; Radix decides *how*.
- **Forcing function: nanoGPT on Shakespeare.** The primary demo trains a
  minimal GPT on the complete works of Shakespeare. It is planned (not
  in-tree yet). It should run on CPU (slowly) for correctness and force
  the GPU gradient path to close for real iteration speed.

## Who this is for

- **Faber model authors** who want to define differentiable models, compute
  gradients, and train neural networks using library calls instead of raw
  compiler annotations — through the staged-carrier tensor surface, the
  loss/optimizer/train layers, and the model-admission capsule.
- **Compiler integrators** validating the Radix autograd pipeline through a
  clean library surface.
- **Inference consumers** of decode, KV-cache, sampling, and generation
  configuration over the shared forward row.
- **Early adopters** willing to work within known constraints (structural
  tier: compile-validated + proba-pinned; executed value-identity is not
  a standing claim).

## Who this is NOT yet for

- **Production deployment.** Gradus is pre-1.0 with a clean-break posture;
  APIs may change. The support matrix and compatibility policy define
  exactly what is admitted and what migrates.
- **GPU-scale training or executed performance evidence.** Executed runs
  are not claimed; speed figures, when they exist, are CPU-reference-level
  at most and never precede the correctness gates.
- **PyTorch users.** Gradus is JAX-shaped (pure functions, explicit params), not
  PyTorch-shaped (nn.Module class hierarchy). No object-oriented model
  registration.
- **Device/backend residency.** Gradus owns mathematical contracts and
  logical state; device handles, scheduling, and physical storage belong to
  the hosts surface, not to a `gradus:*` import.

## What ships now vs what is planned

"Shipped" = committed + compile-validated + proba-pinned. Executed runs
are not a standing claim.

| Capability | Status | Owner |
| --- | --- | --- |
| Reverse-mode AD (differentiable AIR tensor ops) | Shipped (compiler) | Radix |
| Staged-carrier tensor, shape rules, math families | Shipped | Gradus |
| `gradus:gradient` wrapper | Shipped — one companion-call entry | Gradus |
| Linear regression + finite-difference gradient proof | Shipped (structural) — `exempla/gradient-seam` | Gradus |
| SGD, loss, training, checkpoint `Checkpoint` | Shipped | Gradus |
| NN primitives + attention/transformer | Shipped | Gradus |
| Model admission (capsule + Safetensors + GGUF + dequant) | Shipped | Gradus |
| Tokenizer identity + stop binding | Shipped | Gradus |
| Inference: decode, KV-cache, sampling, generation config | Shipped | Gradus |
| nanoGPT on Shakespeare (CPU) | Planned (not in-tree) | Gradus |
| Executed proba / e2e runs | Not claimed | — |
| GPU training / executed performance | Planned — depends on Radix/hosts | Radix + hosts |

## Static-shape surface

The first concrete Gradus surface uses raw `tensor<f32, [shape]>` values,
explicit parameters, explicit gradients, scalar learning rates, and
explicit update tuples — no universal parameter registry, model class, or
device/backend handle:

- `gradus:nn` — `linear_2x2`, `linear_4x4`, `gelu_4x4`
- `gradus:loss` — `mse_2x2`, `mse_4x4`
- `gradus:train` — `train_step_2x2`, `train_step_4x4` (explicit current
  parameters + explicit trainable gradients + scalar lr → explicit tuple of
  updated parameters)

The retired `sgd_step_*` helpers are gone; the SGD surface today is
`gradus:optimize` (`SgdState` slots, `step`, wires). The fixed-shape MSE
rows and train steps remain the admitted caller surface; their formula is
exactly the shape-generic `loss.mse` / optimizer-state update over the
same element arithmetic.

The seam proof for this surface is `exempla/gradient-seam/`. Its
package-owned model function retains a single explicit `@ radix backward`
annotation. The compiler cannot yet resolve library-to-library calls, so
`train_step_*` currently carries the update math inline rather than
calling the optimizer; revisit when that runtime gap closes.

## Import

```fab
import from "gradus:math" math
import from "gradus:tensor" tensor
import from "gradus:gradient" gradient
import from "gradus:optimize" optimize
import from "gradus:loss" loss
```

Same form as every live exemplum `src/main.fab`. Provider resolution is
the `FABER_LIBRARY_HOME` path in [Install](#install).

## Layout

```text
faber.toml     library provider metadata for faber package resolution
cista.toml     package identity + version (cista install)
src/           public `gradus:*` Faber modules (`name.fab` + co-located `name.proba`)
exempla/       instructional demos for gradus types
scripta/       source-library checks (internal)
fixtures/      test corpus (internal)
docs/          policy + module map + factory history
```

Internal vs product paths: [`docs/internal-surfaces.md`](docs/internal-surfaces.md).

## Checks

```bash
./scripta/check-source
./scripta/check-compile
```
