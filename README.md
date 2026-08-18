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

Re-baselined 2026-08-12 to the live post-PML1–5 + correctness-wave surface
(`docs/api-reference.md`, `gradus-api-reference v1.0.0`). Every layer below
is the **structural tier** — compile-validated and proba-pinned. Executed
value-identity is env-blocked on the FMIR lever (CTO8-1) and is an
auditor-owned gate, never claimed here.

| Layer | State |
| --- | --- |
| Foundation (dtype, shape, tensor, math) | **Shipped (PML1)** — staged-carrier tensor, shape rules, operation families |
| Shared contracts (parameter, serialize) | **Shipped (PML1)** — identity + versioned wire forms |
| Gradient wrapper | **Shipped (PML4)** — the ONE companion-call entry: `gradientes_simple_loss` |
| Loss functions | **Shipped (PML4)** — shape-generic `mse`, `cross_entropy` + fixed-shape MSE rows |
| Optimizers | **Shipped (PML4)** — SGD state contract: slots, `passus`, serialization |
| NN primitives | **Shipped (PML3)** — shape-generic `linear`, `gelu`, `layernorm` + fixed-shape rows; **REF-01-U1.1** adds the generic `rmsnorm` row (llama-arch last-axis norm, no centering) with an executed `exempla/dense-rmsnorm` proof (32 PASS / 0 FAIL) |
| Attention / transformer | **Shipped (PML3)** — SDPA/RoPE + transformer block on the staged carrier, plus the fixed-shape BERT-tiny rows |
| Training (steps, schedules, mode, RNG, checkpoint) | **Shipped (PML4)** — `Tabula` checkpoint, LR schedules, mode, seeded RNG, dropout |
| Metrics | **Shipped (PML4)** — `accuratezza` + `Metricum` record |
| Model admission | **Shipped (PML2)** — `capsule-schema-2.0.0` capsule (A1C clean break: pathless identity + per-format manifest) + admitted rows; GGUF-A1b adds pathless range inspection proven against six operator-local GGUF v3 files; GGUF-A3 adds the `tensor_payload` / `tensor_view` typed-view surface (payload carrier, `vincula` bind, bounded windowed materializers) and widens the dequant union set to F32/BF16/Q5_0/Q8_0/Q4_K/Q5_K/Q6_K; REF-01-U1.6 adds the typed `llama` (SmolLM2) architecture adapter (`gradus:model/dense_llama`, executed 19 PASS / 0 FAIL adapter proof in `exempla/dense-llama-adapter`); it does not admit those architectures or claim inference |
| Tokenizer identity | **Shipped (PML2/PML5)** — pinned-row probe parity + `est_eog` stop binding |
| Inference (decode, cache, sampling, generation) | **Shipped (PML5)** — decode/prefill, KV-cache, sampling pipeline, generation config + cursor |
| GPU training / executed runs | Blocked on the FMIR lever (CTO8-1) — structural tier only, no executed claim |

The GGUF foundation is deliberately bounded: metadata and tensor directories
are capped at 4,096 entries and individual retained metadata/range reads at
64 MiB, which admits the inventoried local maximum of 753 tensors. The
package-MIR synthetic proof executes 40 named cases with 40 PASS / 0 FAIL.
The separate A1b adapter inspected six operator-local files from 270 MB through
36.9 GB and matched independent data offsets, metadata counts, tensor counts,
and architecture names. Its guard rejects any inspection read that intersects
the tensor data region. Tensor fragments are available only through checked,
operation-scoped range functions; Gradus retains no path, URL, file handle,
mapping, source function, or whole-model payload. These are format and range
proofs, not tokenizer, model execution, or inference claims. Exact receipts
live in `exempla/gguf-manifest/README.md` and
`exempla/gguf-inspect/README.md`.

The REF-01 dense reference surface begins with the typed architecture
adapters: `gradus:model/dense_qwen2` resolves the canonical qwen2 dense
tensor-name family (the same canonical family as the `llama` adapter) to the
exact GGUF-A1b manifest descriptor facts, with the qwen2 deltas (tensor-set
tie status, GQA head config, rope_theta 1000000) and fail-closed typed
diagnostics. The adapter's executed proof (`exempla/dense-qwen2-adapter`)
prints 23 PASS / 0 FAIL (exit 0) over the pinned Qwen2.5-0.5B descriptor
facts; it does not tokenize, materialize payloads, or claim inference.
REF-01-U1.8 assembles the full dense forward graph —
`gradus:model/dense` `praevideo` (embedding gather → N ordered U1.5 blocks →
final RMSNorm → output projection, tied/untied embedding handling) — with an
executed proof (`exempla/dense-model`) of 37 PASS / 0 FAIL over the pinned
f64 full-graph references; it does not execute a real model payload.

The compiler's autograd capability is shipped (campaign `mir-autograd`, closed
at `336f359ec`): the reverse-mode AD transform covers 16 of 18 AIR tensor ops
with VJPs; two ops (broadcast, reduce) have partial support (rank-extension
broadcast is limited). A linear+MSE training loop matches finite differences,
and an MLP exemplum landed. Gradus's job is to wrap that capability into a
clean, self-contained user library.

### Seam status (PML6-U2 — structural tier)

The gradient seam consumers live under `exempla/`:

| Exemplum | Role | Tier (PML6) |
| --- | --- | --- |
| `exempla/gradient-seam` | Library import of `gradus:gradient` + FD check (SEM004 companion across `importa`) | **Structural** — `faber check`; oracle pins in the exemplum README |
| `exempla/gradient-seam-nolib` | Self-contained `@ radix backward` + FD (no library import) | **Structural** — `faber check`; same arithmetic oracle |
| `exempla/dense-qwen2-adapter` | Typed `qwen2` architecture adapter executed proof — every canonical resolution + fail-closed rejection row over the pinned Qwen2.5-0.5B descriptor facts (REF-01-U1.7) | **Executed** — package-MIR run, 23 PASS / 0 FAIL, exit 0; receipt in the exemplum README |
| `exempla/dense-block` | Generic dense transformer block executed proof — input RMSNorm → GQA attention (causal + RoPE) → residual → post-attn RMSNorm → SwiGLU MLP → residual over a synthetic T=2/D=16 config, composing the U1.1/U1.2/U1.4 rows (REF-01-U1.5) | **Executed** — package-MIR run, 32 PASS / 0 FAIL, exit 0; receipt in the exemplum README |
| `exempla/dense-model` | Dense model assembly executed proof — the complete ordered dense forward graph (embedding gather → 2 ordered U1.5 blocks → final RMSNorm → output projection) over a synthetic T=2/D=16/vocab-8 config with tied + untied embedding rows + the fail-closed rejection row (REF-01-U1.8) | **Executed** — package-MIR run, 37 PASS / 0 FAIL, exit 0; receipt in the exemplum README |
| `exempla/dense-prefill-smollm2` | REF-01-U1.9 SmolLM2 compiled-route prefill-logit consumer (U1.8 forward vs pinned llama.cpp golden at prompt-end) | **Stop** — FINAL at radix `2ed9914e4` / faber `b1adfc9`: packet `faber` green; prior CODEGEN001/E0432/PKG001 `processus:exi` cleared; rust emit reaches cargo; rustc fails 258 errors (first: `cast cannot be followed by a method call`); no rust binary, no executed logits |
| `exempla/dense-prefill-qwen2` | REF-01-U1.10 Qwen2.5-0.5B real-file prefill consumer through `gradus:model/dense` `forward` | **Stop** — FINAL at radix `2ed9914e4`: packet `faber` green; PKG001 closed; rust emit reaches cargo; rustc 248 errors (first `E0015` const `vec!` for `PINNED_TOKENS`); no rust binary, no executed logits |

Pinned oracle (f64 arithmetic of the documented loss): forward loss `2.25`,
companion `grad_w = [0.25, 0.5, 0.75, 1.0]`, FD diffs ~`1e-11`. See each
exemplum README for inputs and the honest execution record.

**No executed seam run is claimed at the campaign gate.** Exempla e2e and
proba execution remain on the FMIR lever (CTO8-1 named pre-release item).
Historical toolchain rebaseline (S0-D, not a standing executed claim):
`radix/docs/factory/gpu-training-lowering/gradus-seam-rebaseline.md`.
Use a current release `faber` binary for `./scripta/check-compile` (set
`FABER_BIN` if PATH points at a stale build).

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
  compiler annotations — through the staged-carrier tensor surface, the
  loss/optimizer/train layers, and the model-admission capsule.
- **Compiler integrators** validating the Radix autograd pipeline through a
  clean library surface.
- **Inference consumers** of the PML5 surface — decode, KV-cache, sampling,
  and generation configuration over the shared forward row.
- **Early adopters** willing to work within known constraints (structural
  tier: compile-validated + proba-pinned; executed value-identity is the
  auditor-owned runtime-evidence gate, currently env-blocked on the FMIR
  lever).

## Who this is NOT yet for

- **Production deployment.** Gradus is pre-1.0 with a clean-break posture;
  APIs may change. The support matrix and compatibility policy (PML6-U3)
  define exactly what is admitted and what migrates.
- **GPU-scale training or executed performance evidence.** Executed runs are
  env-blocked on the FMIR lever (CTO8-1); speed claims are CPU-reference-level
  at most and never precede the correctness gates.
- **PyTorch users.** Gradus is JAX-shaped (pure functions, explicit params), not
  PyTorch-shaped (nn.Module class hierarchy). No object-oriented model
  registration.
- **Device/backend residency.** Gradus owns mathematical contracts and
  logical state; device handles, scheduling, and physical storage belong to
  the hosts/NGAB surface, not to a `gradus:*` import.

## What ships now vs what is planned

Re-baselined to the live surface (structural tier). "Shipped" = committed +
compile-validated + proba-pinned; executed runs are the auditor-owned FMIR
gate.

| Capability | Status | Owner |
| --- | --- | --- |
| Reverse-mode AD (all differentiable AIR tensor ops) | **Shipped** (Radix mir-autograd campaign) | Radix |
| Staged-carrier tensor, shape rules, math families | **Shipped (PML1)** | Gradus |
| `gradus:gradient` wrapper | **Shipped (PML4)** — one companion-call entry | Gradus |
| Linear regression + FD gradient proof | **Shipped (S4-A)** — CPU seam proof | Gradus |
| SGD optimizer state, loss (`mse`/`cross_entropy`), training (steps, schedules, mode, RNG, dropout, checkpoint `Tabula`) | **Shipped (PML4)** | Gradus |
| NN primitives + attention/transformer (staged surface + fixed-shape rows) | **Shipped (PML3)**; configurable RoPE (freq base/scale/pair policy — consecutive-pair llama NORM vs interleaved-pair qwen2, REF-01-U1.3) with executed proof `exempla/dense-rope`; multi-head attention with GQA KV-head sharing — causal + RoPE + output projection (REF-01-U1.4) with executed proof `exempla/dense-gqa`; generic dense transformer block — input RMSNorm → GQA (causal + RoPE) → residual → post-attn RMSNorm → SwiGLU → residual, composing the U1.1/U1.2/U1.4 rows (REF-01-U1.5) with executed proof `exempla/dense-block` | Gradus |
| Model admission (capsule + Safetensors + GGUF + dequant) | **Shipped (PML2)** — schema-2 capsule (pathless identity + per-format manifest); format-general GGUF manifest/range inspection has an **executed A1b proof** over six operator-local real files; GGUF-A3 adds the `tensor_payload`/`tensor_view` modules (pathless payload carrier, `vincula` bind, bounded windowed materializers) and the widened dequant union set, without architecture admission, tokenizer, or inference claims | Gradus |
| Tokenizer identity + probe parity + `est_eog` | **Shipped (PML2/PML5)** | Gradus |
| Inference: decode, KV-cache, sampling, generation config | **Shipped (PML5)** | Gradus |
| nanoGPT on Shakespeare (CPU) | **Planned** (forcing-function demo; corpus/ not yet in-tree) | Gradus |
| Executed proba / e2e runs | **Auditor-owned** — env-blocked on the FMIR lever (CTO8-1); never a dev-loop claim | Auditor |
| GPU training / executed performance | **Planned** — depends on Radix/hosts (mir-swarm rung); NGAB owns executed evidence | Radix + hosts |

## Static-shape surface (S4-A)

The first concrete Gradus surface is bounded to the first two callers
(`gpu-training-lowering` stage-4-delivery.md P1). Raw `tensor<f32, [shape]>`
values, explicit parameters, explicit gradients, scalar learning rates, and
explicit update tuples — no universal parameter registry, model class, or
device/backend handle:

- `gradus:nn` — `linear_2x2`, `linear_4x4`, `gelu_4x4`
- `gradus:loss` — `mse_2x2`, `mse_4x4`
- `gradus:train` — `train_step_2x2`, `train_step_4x4` (explicit current
  parameters + explicit trainable gradients + scalar lr → explicit tuple of
  updated parameters)

The `sgd_step_*` fixed-shape helpers were retired at PML1-U6 (post-U6
cleanup, ledger rows 10–11); the SGD surface today is the PML4 optimizer
state contract (`gradus:optimize` — `SgdStatum` slots, `passus`, wires).
The fixed-shape MSE rows and train steps above remain the admitted caller
surface; their formula is exactly the shape-generic `loss.mse` /
`optimize`-state update over the same element arithmetic.

The linear-regression exemplum (`examples/training/linear-regression`) was
migrated onto this surface as the seam proof; its package-owned model function
retains its single explicit `@ radix backward` annotation. Known toolchain
constraint: the FMIR stepper cannot yet resolve library-to-library calls, so
`train_step_*` currently carries the update math inline rather than calling
it; revisit when that runtime gap closes.

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
