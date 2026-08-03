# Gradus — the Faber Autograd and ML Library

**Gradus** (Latin: "step, pace, degree" — the root of *gradient*) is Faber's
native library for automatic differentiation, loss functions, optimizers,
neural-network primitives, and training mechanics.

Gradus wraps the compiler's reverse-mode autograd transform (`radix-air`)
into clean Faber source contracts. The architecture is JAX-shaped, not
PyTorch-shaped: models are pure functions with explicit parameters, gradients
are compiler-generated companion functions, and the backward pass is
generated code — not a runtime tape replay.

## Status

| Layer | State |
| --- | --- |
| Foundation (math, tensor) | Scaffold — day-one target |
| Gradient wrapper | Scaffold — wraps `@ radix backward` |
| Optimizers | Planned — SGD first, then Adam |
| Loss functions | Planned — MSE first, then cross-entropy |
| NN primitives | Planned — Linear, activation, norm, embedding |
| Attention / transformer | Planned — nanoGPT forcing function |
| GPU training | Blocked on mir-swarm device gradient rung |

The compiler's autograd capability is shipped (campaign `mir-autograd`, closed
at `336f359ec`): the reverse-mode AD transform covers 16 of 18 AIR tensor ops
with VJPs; two ops (broadcast, reduce) have partial support (rank-extension
broadcast is limited). A linear+MSE training loop matches finite differences,
and an MLP exemplum landed. Gradus's job is to wrap that capability into a
clean, self-contained user library.

### Seam status (rebaselined 2026-08-03)

The gradient seam (`exempla/gradient-seam`) **compiles and executes end to end
through `faber run -t fmir` with the current release faber toolchain**
(v1.4.0, includes faber `180bcef`): forward loss via `gradient.simple_loss`,
companion backward `gradient.loss_backward` across the `importa` boundary
(SEM004), and the per-element FD comparison all run; the companion gradient
matches finite differences to ~1e-11. The two U1 compiler blockers this seam
depends on — SEM004 and LIB-MIR — are resolved on that toolchain. The seam
fixture header's "faber run -t fmir fails (LIB-MIR gate)" claim is stale.

Caveat: `./scripta/check-compile` resolves `faber` from PATH and currently
fails on the seam consumer (SEM004) when the on-PATH binary is the stale
2026-08-01 debug build — refresh the toolchain before trusting that gate.
Full evidence: `radix/docs/factory/gpu-training-lowering/gradus-seam-rebaseline.md`.

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
  minimal GPT on the complete works of Shakespeare. It runs on CPU (slowly)
  for correctness and forces the GPU gradient path to close for real
  iteration speed.

## Who this is for

- **Faber model authors** who want to define differentiable models, compute
  gradients, and train neural networks using library calls instead of raw
  compiler annotations.
- **Compiler integrators** validating the Radix autograd pipeline through a
  clean library surface.
- **Early adopters** willing to work within known compiler constraints (CPU
  execution, no GPU, static shapes, forward inlined in loops).

## Who this is NOT yet for

- **Production deployment.** Gradus is pre-1.0; APIs may change. No
  checkpointing, no safetensors, no model distribution.
- **GPU-scale training.** GPU gradient execution is a Radix/hosts concern
  (mir-swarm rung), not a Gradus concern. CPU training is correct but slow.
- **PyTorch users.** Gradus is JAX-shaped (pure functions, explicit params), not
  PyTorch-shaped (nn.Module class hierarchy). No object-oriented model
  registration.
- **Checkpoint serialization.** Model save/load is deferred to Horizon 9
  (safetensors gate).

## What ships now vs what is planned

| Capability | Status | Owner |
| --- | --- | --- |
| Reverse-mode AD (all differentiable AIR tensor ops) | **Shipped** (Radix mir-autograd campaign) | Radix |
| `gradus:tensor` genus | **Horizon 1** (architecture checkpoint complete) | Gradus |
| `gradus:gradient` wrapper | **Horizon 1** (architecture checkpoint complete) | Gradus |
| Linear regression + FD gradient proof | **Horizon 2** | Gradus |
| SGD, MSE loss | **Horizon 2** | Gradus |
| MLP with GELU, cross-entropy | **Horizon 3–4** | Gradus |
| Attention, transformer | **Horizon 5–6** | Gradus |
| nanoGPT on Shakespeare (CPU) | **Planned** (Horizon 7 forcing-function demo) | Gradus |
| nanoGPT on GPU (10–100× faster) | **Planned** (Horizon 8 — depends on Radix/hosts) | Radix + hosts |

## Import

```fab
importa ex "gradus:math" privata math
importa ex "gradus:tensor" privata tensor
importa ex "gradus:gradient" privata gradient
importa ex "gradus:optimize" privata optimize
importa ex "gradus:loss" privata loss
```

Radix and `faber` resolve provider imports from the shared library home:

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

## Layout

```text
faber.toml     library provider metadata for faber package resolution
cista.toml     package identity + version (cista install)
src/           public `gradus:*` Faber modules (`name.fab` + co-located `name.proba`)
exempla/       instructional demos for gradus types
corpus/        training demos (nanogpt-shakespeare, …)
scripta/       source-library checks
docs/          policy + module map + factory history
```

## Checks

```bash
./scripta/check-source
./scripta/check-compile
```
