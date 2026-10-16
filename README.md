# Gradus — the Faber Autograd and ML Library

**Gradus** (Latin: "step, pace, degree" — the root of *gradient*) is Faber's
native library for automatic differentiation, loss functions, optimizers,
neural-network primitives, and training mechanics.

Gradus wraps the compiler's reverse-mode autograd transform (`radix-air`)
into clean Faber source contracts. The architecture is JAX-shaped, not
PyTorch-shaped: models are pure functions with explicit parameters, gradients
are compiler-generated companion functions, and the backward pass is
generated code — not a runtime tape replay.

> **Experimental.** Like Faber itself, this library is experimental until
> Faber 2; APIs change without notice.

## Start here

Gradus is a JAX-shaped autograd and ML library: models are pure functions
with explicit parameters, reverse-mode gradients are compiler-generated
companion functions rather than a runtime tape, and public types are
device-neutral contracts. Foundation modules (`gradus:dtype`,
`gradus:shape`, `gradus:tensor`, `gradus:math`) feed loss, optimizers, and
neural-network primitives; those compose into attention and transformer
blocks; model-admission modules bind GGUF and Safetensors artifacts into
typed capsules without retaining paths or whole-model payloads. The tensor
module provides decoded F32 compute carriers; `gradus:storage` keeps opaque
encoded bytes, representation identity, and block metadata as separate
values. Decode, cache, sampling, and generation sit on the same forward row.
Import the leaf that owns the type you use — the façade does not re-export
genera.

The smallest useful program, a numbered learning path, and which demo to
open first per capability are in
[`docs/quickstart.md`](docs/quickstart.md). After that page's snippet, open
[`exempla/dense-rmsnorm/`](exempla/dense-rmsnorm/) — an in-memory RMSNorm
row that type-checks with `faber check`.

## Install

> **Experimental.** Like Faber itself, this library is experimental until
> Faber 2; APIs change without notice.

Package installation is not yet available in the public toolchain: `faber`
never installs packages, and the separate package-store tool is not released.
Instead, clone this repository and tell `faber` where to find it.

Install the `faber` binary from the
[release page](https://github.com/faberlang/releases/releases/latest) (docs at
[faberlang.dev](https://faberlang.dev)). `faber` resolves `gradus:*` from a
library home: a directory that holds this repo as `gradus/`
(`--library-home <DIR>`, or `[paths] library_home` in your `faber.toml`).

```text
<library home>/gradus/src/**/*.fab
```

Norma is embedded in the `faber` binary and needs no home. Put only the
libraries you use in the library home; a stale `norma/` checkout beside
`gradus/` would shadow the embedded Norma.

```bash
mkdir libs && git clone https://github.com/faberlang/gradus libs/gradus
faber doctor --library-home libs            # library.gradus.availability should be faber-package
faber check --library-home libs /path/to/your-package
```

Use an absolute path for the library home; a relative one can fail to resolve
from inside a package.

## Example

From an empty directory, with the library home passed as above and a
current `faber` binary on `PATH` (checked with `faber` 1.14):

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

`src/main.fab` (same `import from` / `main` shape as
`exempla/gradient-seam/src/main.fab` and `exempla/*/src/main.fab`):

```fab
import from "gradus:loss" loss

main {
    let tensor<f32, [2, 2]> prediction ← [[1.0, 2.0], [3.0, 4.0]]
    let tensor<f32, [2, 2]> target ← [[1.0, 2.0], [3.0, 3.0]]
    let f32 value ← loss.mse(prediction, target)
    print value
}
```

```bash
faber check --library-home /absolute/path/to/libs .
```

`loss.mse` is mean squared error over the 2×2 f32 fixture; the inputs differ
in one element by 1, so the mean is `0.25`. `faber check` is the standing
proof that the import and call type-check. The training-loop exemplum is an
executed package proof: `faber run` executes its library-to-library calls on
the FMIR stepper. Other package runs, GPU
training, and executed model performance are not claimed here. Worked demos
live under `exempla/`;
the first-open-per-capability tour is [`docs/quickstart.md`](docs/quickstart.md).

## Status

**Experimental.** Like Faber itself, Gradus is experimental until Faber 2;
APIs change without notice, with a clean-break posture (no compatibility
shims). See [`docs/compatibility-policy.md`](docs/compatibility-policy.md).

What ships today is the **structural** surface: compile-validated,
proba-pinned source contracts, plus an executed 100-step MLP training
loop through explicit optimizer state and updates whose final loss
matches the f64 oracle (`0.017928625511508454`). Broader model-forward
identity, GPU training, and executed performance are not claimed here.

Gradus's executed tier of record is the CPU/reference tier — decoded F32
host-list compute carriers (`src/tensor.fab` `class NumericBlock`), reference
kernels, and FMIR stepper receipts. Encoded model bytes belong to the open
`gradus:storage` representation; device residency and emission belong to the compiler
and host runtimes, not to this library.

| Layer | State |
| --- | --- |
| Foundation (dtype, shape, tensor, math) | Shipped |
| Parameters and serialization | Shipped |
| Gradient wrapper, loss, SGD, training, metrics | Shipped (structural), with executed MLP training proof — `gradients_simple_loss`, `mse` / `cross_entropy`, `SgdState` / `step`, `Checkpoint`, `accuracy` / `Metric` |
| NN primitives, attention, transformer | Shipped (structural); several `exempla/dense-*` packages have executed in-memory proofs |
| Model admission (capsule, GGUF, Safetensors) | Shipped; GGUF inspection has executed real-file receipts. `tensor_view.links` binds a payload to a manifest. Architecture adapters do not claim inference |
| Tokenizer identity | Shipped |
| Inference (decode, cache, sampling, generation) | Shipped (structural) |
| Dense forward (`gradus:model/dense` `forward`, `prefill_cached`, `decode_step`) | Shipped over synthetic graphs (compile-pinned prefill then decode matching full recompute); not a real-model inference claim |
| GPU training | Not claimed |

KV-cache writes fail closed on gap and overflow against an immutable
capacity; cached-attention positions are absolute and include the
just-written row.

Generation stop handling reads `GenerationConfig.eog_ids`; the decoder's EOG
membership and suppression rules use that configured list.

Campaign ledgers, unit receipts, and per-symbol coverage live in
[`docs/api-reference.md`](docs/api-reference.md),
[`docs/module-map.md`](docs/module-map.md), and
[`docs/factory/production-ml-library/`](docs/factory/production-ml-library/).
Exemplum receipts sit next to each demo under `exempla/`.

Gradus wraps the compiler's reverse-mode AD transform (`radix-air`). The
admitted VJP family and its gaps live in that crate, not here.

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
  GPU execution, kernel fusion, and memory management are compiler and host
  concerns. Gradus describes *what* to compute; the compiler decides *how*.
- **Forcing function: nanoGPT on Shakespeare.** The primary demo trains a
  minimal GPT on the complete works of Shakespeare. It is planned (not
  in-tree yet). It should run on CPU (slowly) for correctness and force
  the GPU gradient path to close for real iteration speed.

## Who this is for

- **Faber model authors** who want to define differentiable models, compute
  gradients, and train neural networks using library calls instead of raw
  compiler annotations — through the decoded F32 carrier surface, the
  loss/optimizer/train layers, and the model-admission capsule.
- **Compiler integrators** validating the Radix autograd pipeline through a
  clean library surface.
- **Inference consumers** of decode, KV-cache, sampling, and generation
  configuration over the shared forward row.
- **Early adopters** willing to work within known constraints (structural
  tier: compile-validated + proba-pinned; executed value-identity is not
  a standing claim).

## Who this is NOT yet for

- **Production deployment.** Gradus is experimental until Faber 2, with a
  clean-break posture; APIs change without notice. The support matrix and compatibility policy define
  exactly what is admitted and what migrates.
- **GPU-scale training or broad executed performance evidence.** Outside the
  bounded training-loop proof, executed runs are not claimed; speed figures,
  when they exist, are CPU-reference-level at most and never precede the
  correctness gates. Comparator benches to date pin llama.cpp Metal and CPU
  rows on one Apple Silicon Mac; no CUDA comparator row exists yet (reserved).
- **PyTorch users.** Gradus is JAX-shaped (pure functions, explicit params), not
  PyTorch-shaped (nn.Module class hierarchy). No object-oriented model
  registration.
- **Device/backend residency.** Gradus owns mathematical contracts and
  logical state; device handles, scheduling, and physical storage belong to
  the host runtimes, not to a `gradus:*` import.

## What ships now vs what is planned

"Shipped" = committed + compile-validated + proba-pinned. Executed runs
are claim-specific and require a receipt; the MLP training receipt is listed
below.

| Capability | Status | Owner |
| --- | --- | --- |
| Reverse-mode AD (differentiable AIR tensor ops) | Shipped (compiler) | Radix |
| Decoded F32 compute carrier, shape rules, math families | Shipped | Gradus |
| `gradus:gradient` wrapper | Shipped — one companion-call entry | Gradus |
| Linear regression + finite-difference gradient proof | Shipped (structural) — `exempla/gradient-seam` | Gradus |
| SGD, loss, training, checkpoint `Checkpoint` | Shipped | Gradus |
| NN primitives + attention/transformer | Shipped | Gradus |
| Model admission (capsule + Safetensors + GGUF + dequant + open storage metadata) | Shipped | Gradus |
| Tokenizer identity + stop binding | Shipped | Gradus |
| Inference: decode, KV-cache, sampling, generation config | Shipped — fail-closed capacity; absolute cache positions | Gradus |
| nanoGPT on Shakespeare (CPU) | Planned (not in-tree) | Gradus |
| Executed training loop + train/optimize proba | Shipped — 100-step MLP; 90/90 cases | Gradus |
| Other executed proba / e2e runs | Not claimed | — |
| GPU training / executed performance | Planned — depends on compiler and host work | Compiler + host runtimes |

## Static-shape surface

The first concrete Gradus surface uses raw `tensor<f32, [shape]>` values,
explicit parameters, explicit gradients, scalar learning rates, and
explicit update tuples — no universal parameter registry, model class, or
device/backend handle:

- `gradus:nn` — `linear<M,K,N>`, `gelu<M,N>` (shape-generic leaves)
- `gradus:loss` — `mse<M,N>` plus decoded-carrier `mse_carrier`
- `gradus:train` — schedules, modes, RNG, dropout, and checkpoints; training
  updates use explicit parameters, gradients, and optimizer state

The `gradus:optimize` surface carries explicit `SgdState` slots, steps, and
wires. Dimensions such as 2×2 remain fixture choices in examples rather than
separate library entry points.

The seam proof for this surface is `exempla/gradient-seam/`. The
`@ radix backward` annotation lives in `gradus:gradient`; that exemplum
calls the generated companion through the import. Library-to-library calls
execute on the FMIR stepper. The BERT tuple call cases remain omitted from execution because
of the named package-MIR call-argument-mismatch residual (E8/E10).

## Import

```fab
import from "gradus:math" math
import from "gradus:tensor" tensor
import from "gradus:gradient" gradient
import from "gradus:optimize" optimize
import from "gradus:loss" loss
```

Same form as every live exemplum `src/main.fab`. Provider resolution is
the library home in [Install](#install).

## Layout

```text
faber.toml     library provider metadata for faber package resolution
cista.toml     package identity + version (for the separate package-store tool)
src/           public `gradus:*` Faber modules (`name.fab` + co-located `name.proba`)
exempla/       instructional demos for gradus types
scripta/       source-library checks (internal)
fixtures/      test corpus (internal)
docs/          quickstart, policy, module map, API reference, planning history
```

Internal vs product paths: [`docs/internal-surfaces.md`](docs/internal-surfaces.md).

## Checks

```bash
./scripta/check-source
./scripta/check-compile
```

## License

MIT. See [`LICENSE`](LICENSE).
