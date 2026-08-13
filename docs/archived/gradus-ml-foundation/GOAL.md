# Goal: Gradus ML Foundation And nanoGPT Training Architecture

**Status**: Horizon 0 (architecture checkpoint) complete — frozen 2026-08-01.
Vision confirmed; gradient-seam, tensor-contract, and train-seam boundaries
recorded. Operator approved train-seam **Option C (compiler-fix-first)** on
2026-08-01. **Compiler-fix track CLEARED 2026-08-01** — LIB-MIR, SEM004,
SEM010 all shipped and verified (fresh compiler): consumer
`gradus/exempla/gradient-seam/` runs mirror-free with FD match ~1e-11.
Horizon 1–2 delivery (JAX-shaped `gradus:train` + linear-regression proof) is
unblocked ([freeze receipt](checkpoint-close.md)).

**Owner repo**: `/Users/ianzepp/work/faberlang/gradus`

**Participating repos**: `gradus`, `radix`, `faber`, `faber-runtime`,
`examples`; `hosts` only for a future GPU execution checkpoint; `cista` only
for an explicit distribution checkpoint

**Lowers to**: compiler-fix track (LIB-MIR → SEM004 → SEM010) → Horizon 1–2 delivery spec → `delivery` → `factory`

**Batching posture**: discovery-first for the autograd ergonomics and first
training vertical slice; batch-by-default for repeated primitive, loss, and
optimizer families after the gradient seam is proven

**Primary product target**: a self-contained Faber autograd and ML library
that lets Faber authors define differentiable models, compute gradients,
train neural networks, and run LLM-shaped workloads without importing from
Norma or writing raw `@ radix backward` annotations outside the library.

## Purpose

This goal records the architectural destination for Gradus as Faber's native
autograd and ML foundation. It is intentionally a vision artifact, not an
implementation-ready delivery specification. It names the package/module
boundaries, ownership rules, target file inventory, layering responsibilities,
and capstone outcomes that later delivery work must refine against live
compiler and host evidence.

The central decision is:

> Gradus remains one versioned Faber source package, organized as explicit
> importable modules representing the ML stack from tensor foundation through
> training loop. The autograd capability is owned by Radix (`radix-air`
> reverse-mode AD); Gradus owns the user-facing ergonomics, differentiable
> primitives, architecture blocks, and training mechanics that compose on top
> of it. Gradus is fully self-contained — it does not import from Norma or
> any sibling library.

The forcing-function workload is nanoGPT on Shakespeare: a minimal GPT
implementation that trains on CPU (slowly) and demands the GPU gradient path
to close for real iteration speed.

## Vision

Faber authors should be able to define, train, and evaluate neural networks
from ordinary library values:

- tensor construction, shape management, and basic operations;
- differentiable functions with compiler-generated gradient companions;
- loss functions (MSE, cross-entropy) and optimizers (SGD, Adam);
- neural-network primitives (Linear, activation, norm, embedding, dropout);
- attention mechanisms and transformer architecture blocks;
- training loops with metrics, checkpointing, and reproducible convergence;
- data loading with batching, shuffling, and tokenization;
- full LLM-shaped training workloads (nanoGPT) through library calls alone.

The authoring program should describe the model and its training. The
compiler should generate gradients. The host should execute on CPU or GPU.
The author should never write calculus by hand or manage gradient tapes.

The production-level outcome is not API compatibility with PyTorch or JAX.
It is a coherent Gradus library with the following user experience:

```text
Faber model package
  → Gradus primitives / architecture / training contracts
    → Radix lowering and reverse-AD transform
      → MIR gradient code (fused, device-ready)
        → selected host backend (CPU now, GPU future)
          → trained model
```

Every standard training workload should use the same Gradus library and
compiler path. A workload may exercise a new primitive or architecture, but it
must not carry a private autograd implementation or raw `@ radix backward`
annotations outside the `gradient` module.

## Current baseline

The compiler's autograd capability is already shipped, not aspirational:

- Campaign `mir-autograd` closed at commit `336f359ec`.
- The AIR reverse-mode AD transform is shipped and verified. The transform
  covers 16 AIR tensor operations (matmul, add, sub, mul, div, mean, sum, max,
  gelu, tanh, exp, log, relu, sqrt, softmax, layernorm) with VJPs. Two ops
  (broadcast, reduce) have partial support — rank-extension broadcast is
  limited (BERT-tiny exemplum duplicates bias rows as a workaround).
- A linear+MSE training loop compiles forward + backward + SGD and matches
  finite differences over multiple steps (CPI-only; source-integration,
  backend-emission, and device-execution are outside the proof code's scope).
- An MLP training exemplum landed (`examples/training/mlp/`) — SGD is inlined
  because MIR-backed targets cannot yet import library modules.
- Control-flow AD (Block, If, Match) and interprocedural AD landed.
- The fusion-ordering ADR (`ee3c00a3a`) ensures gradient code is fused before
  the AD transform, keeping generated gradients compilation-ready.
- Sibling tests in `radix` and `faber-runtime` validate the toolchain, not the
  Gradus library package. Gradus integration is unproven until the Horizon 0
  gradient-wrapper fixture passes.

The current ownership boundary is:

| Area | Current authority | Long-term authority |
| --- | --- | --- |
| Autograd transform (reverse-mode AD) | `radix/crates/radix-air` | Remains in Radix |
| MIR gradient ops | `radix/crates/radix-mir/src/gradient.rs` | Remains in Radix |
| Runtime tensor type | `faber-runtime/src/tensor.rs` | Generated-code runtime only |
| Runtime autograd tape (oracle) | `faber-runtime/src/autograd.rs` | Validation oracle only; not the user path |
| Optimizer stub (SGD) | `norma/src/optimizer.fab` | Stays in Norma (plain math context) |
| Tensor helpers | `norma/src/tensor.fab` | Stays in Norma (plain math context) |
| User-facing autograd ergonomics | *(none)* | `gradus/src/gradient` |
| Differentiable primitives | *(none)* | `gradus/src/nn` |
| Training loop and loss | *(none)* | `gradus/src/train`, `gradus/src/loss` |
| GPU gradient execution | *(open mir-swarm rung)* | Radix + hosts |

### Compiler capability matrix (Horizon 0 baseline)

| Dimension | Status | Notes |
| --- | --- | --- |
| AIR reverse-mode AD transform | **Shipped** | 16 of 18 tensor ops differentiable; 2 have partial support |
| MIR gradient lowering (LLVM) | **Shipped** | CPU execution path verified |
| MIR gradient lowering (WGSL) | **In progress** | GPU shader emission; mir-swarm rung |
| MIR gradient lowering (SPIR-V) | **Planned** | Vulkan compute path |
| CPU execution (LLVM backend) | **Shipped** | Linear+MSE+MLP verified |
| GPU execution (WGSL/SPIR-V) | **Not yet** | Blocked on mir-swarm device gradient rung |
| Control-flow AD (Block, If, Match) | **Shipped** | Verified in campaign mir-autograd |
| Interprocedural AD | **Shipped** | Companion functions generated across call boundaries |
| Fusion ordering (fuse before AD) | **Shipped** | ADR `ee3c00a3a` |
| Provider imports (library modules) | **Verified** | `gradus:*` stubs compile; `faber check` passes |
| Consumer import of library (gradus:gradient from external pkg) | **Unverified** | U1 discovery gate |
| Tensor-returning calls in loops | **SEM010 — blocked** | Exempla inline forward pass in `incipit` |
| Rank-extension broadcast | **Limited** | BERT-tiny duplicates bias rows |

The current Gradus repo is a scaffold: `faber.toml`, `cista.toml`,
`AGENTS.md`, `README.md`, the `src/gradus.fab` facade documenting the full
target module map, and top-level leaf stubs for `math`, `tensor`, `gradient`,
`loss`, `optimize`, `nn`, `attention`, `transformer`, `train`, and `data`.

## Structural model

### Faber package and import terminology

Faber does not need a Cargo-style subcrate split for this architecture. Keep a
single `gradus` source package and use source modules as the stable import
boundaries:

```text
src/math.fab                       → gradus:math
src/loss/mse.fab                   → gradus:loss/mse
src/optimize/adam.fab              → gradus:optimize/adam
```

Nested directories are namespaces, not independently versioned packages. A
nested package should contain at least two modules and preferably three. A
facade such as `src/loss.fab` may document or compose the leaves, but current
Faber policy does not provide type re-export semantics. Consumers import the
leaf that owns the type.

The `gradus:gradus` facade must remain a map and orientation point. It must
not become a god module, a compatibility barrel, or an ownership escape hatch.

### Dependency DAG

The dependency graph must remain acyclic and point from stable semantics toward
execution:

```text
math / tensor
      ↓
gradient
      ↓
loss / optimize
      ↓
nn (primitives)
      ↓
attention / transformer
      ↓
train / data
      ↓
Radix lowering and host backend
```

The following reverse dependencies are architectural defects:

- `gradient` importing `nn`, `loss`, or `optimize` — autograd is pure calculus;
  it does not know what it differentiates;
- `optimize` importing `nn` — optimizers consume raw parameter tensors, not
  layer abstractions;
- `loss` importing `optimize` — a loss is a differentiable function, not an
  optimization concern;
- `nn` importing `attention` or `transformer` — primitives do not know the
  architectures built from them;
- `attention` importing `transformer` — attention is a building block, not a
  transformer component;
- `train` importing a specific model definition — the training loop is
  reusable across models;
- any layer importing a GPU device handle, CUDA context, or backend execution
  state.

### JAX-shaped, not PyTorch-shaped

Gradus follows the JAX functional model, not the PyTorch object-oriented model.
A model is a pure function: `(params, x) → y`. Parameters are explicit values
carried in records, not registered through class machinery. The gradient is a
compiler-generated companion function. The optimizer takes the gradients and
produces new params.

```text
# Forward: pure function with explicit parameters
fn gpt_forward(params: GptParams, x: Tensor) → Tensor { ... }

# Gradient: compiler-generated companion
@ radix backward "gpt_backward"
fn gpt_forward(params: GptParams, x: Tensor) → Tensor { ... }

# Training: explicit stateless loop
fn train_step(params: GptParams, batch: Batch, lr: f32) → GptParams {
    logits = gpt_forward(params, batch.x)
    loss = cross_entropy(logits, batch.y)
    grads = gpt_backward(params, batch.x)
    return sgd_step(params, grads, lr)
}
```

No `nn.Module`. No registration. No class hierarchy. The forward function is
pure; the compiler generates its gradient companion from the AIR transform.

### Self-containment

Gradus does not import from Norma or any sibling library. This is a deliberate
boundary decision: a Gradus user should never have to decide whether to import
from `norma:*` or `gradus:*`. If you need autograd or ML, import from Gradus.
If you need plain math, import from Norma. Duplication between them is
intentional isolation, not a bug.

### Device-neutral boundary

Gradus public types are pure mathematical contracts — tensors as shape+dtype
values, gradients as functions, optimizers as parameter-update rules. The
compute intent is described in Gradus source. Radix lowers it to CPU or GPU
kernels. The host manages device execution.

Gradus must not carry:
- GPU device handles or buffer objects in public Faber values;
- Backend-specific execution state;
- Kernel launch or dispatch logic;
- Device memory management.

## Proposed Gradus file inventory

This is the target inventory. File names are proposed ownership markers, not a
commit to create every leaf in one change. A later delivery must split files
only at a demonstrated semantic, ownership, validation, migration, or
correctness boundary.

```text
gradus/
  faber.toml
  cista.toml
  src/
    math.fab                         # tensor-aware math foundation (own copy)
    tensor.fab                       # tensor construction, shape/dtype, basic ops
                                     # plain values — NOT autograd-aware

    gradus.fab                       # orientation facade; no genera ownership

    # ── Layer 2: Autograd core ──
    gradient.fab                     # @ radix backward wrapper ergonomics
                                     # forward call → output; companion → gradients
                                     # finite-difference validation helpers

    # ── Layer 3: Loss ──
    loss.fab                         # loss facade/map after split
    loss/
      mse.fab                        # mean squared error (regression)
      cross_entropy.fab              # cross-entropy (classification / next-token)

    # ── Layer 4: Optimization ──
    optimize.fab                     # optimizer facade/map after split
    optimize/
      sgd.fab                        # SGD with momentum
      adam.fab                       # Adam optimizer
      schedule.fab                   # learning-rate schedules (warmup, cosine decay)

    # ── Layer 5: NN primitives ──
    nn.fab                           # nn facade/map after split
    nn/
      linear.fab                     # Linear (matmul + bias)
      activation.fab                 # GELU, ReLU, Sigmoid, Tanh, SiLU
      norm.fab                       # LayerNorm, RMSNorm
      embedding.fab                  # token / position embedding lookup
      dropout.fab                    # dropout (train vs eval behavior)

    # ── Layer 6: Architecture blocks ──
    attention.fab                    # attention facade/map after split
    attention/
      scaled_dot_product.fab         # scaled dot-product attention
      causal.fab                     # causal masking
      multi_head.fab                 # multi-head composition

    transformer.fab                  # transformer facade/map after split
    transformer/
      block.fab                      # block = attn + ffn + residual + norm
      position.fab                   # positional encoding (learned, sinusoidal, RoPE)
      head.fab                       # output projection (logits)

    # ── Layer 7: Training and data ──
    train.fab                        # training facade/map after split
    train/
      loop.fab                       # forward → loss → backward → step structure
      metric.fab                     # loss, accuracy, perplexity tracking
      checkpoint.fab                 # model save/load (future; safetensors gate)

    data.fab                         # data facade/map after split
    data/
      batch.fab                      # batching and shuffling
      token.fab                      # tokenization (char-level, BPE)

  exempla/
    gradient-basics.fab              # basic autograd demos
    linear-regression.fab            # first training loop proof
    attention-proof.fab              # finite-difference gradient check on attention

  corpus/
    nanogpt-shakespeare/             # the forcing-function demo
      src/
        model.fab                    # nanoGPT model definition
        train.fab                    # training script
      data/
        input.txt                    # Shakespeare text (~1MB)
      faber.toml
      faber.lock
      tests/run.sh

  docs/
    factory/
      gradus-ml-foundation/GOAL.md   # this vision artifact
    module-map.md                    # full module ownership map
    api-shape-policy.md              # API shape and naming conventions
    ...
```

## Responsibilities by module family

### Foundation: `math` and `tensor`

`math` owns backend-neutral scalar math, shape utilities, and numeric
constants needed across Gradus modules. It must not know about gradients,
losses, or a GPU backend.

`tensor` owns the tensor type, construction helpers, and basic operations. It
expresses all data needed for computation without carrying gradient metadata
or autograd annotations. Tensor operations are plain math; the autograd
wrapper in `gradient` makes them differentiable.

### Autograd core: `gradient`

`gradient` owns the user-facing API surface around the compiler's reverse-mode
AD transform. It wraps `@ radix backward` annotations into clean ergonomics
and provides finite-difference validation helpers for gradient correctness
proofs.

It is pure calculus. It does not know what it differentiates — it must not
import from loss, optimize, nn, attention, transformer, train, or model.

### Loss and optimization: `loss` and `optimize`

`loss` owns differentiable loss functions: MSE for regression, cross-entropy
for classification and next-token prediction. A loss is a differentiable
function that consumes model output and target values to produce a scalar. It
must not import from optimize.

`optimize` owns parameter-update rules: SGD with momentum, Adam, and
learning-rate schedules. Optimizers consume raw parameter tensors and gradient
tensors. They do not know about layer abstractions and must not import from nn,
attention, or transformer.

### Primitives: `nn`

`nn` owns differentiable building blocks: Linear, activation functions (GELU,
ReLU, Sigmoid, Tanh, SiLU), normalization (LayerNorm, RMSNorm), embedding
lookup, and dropout. Each primitive must be independently differentiable —
gradient correctness must be verifiable via finite-difference checks.

Primitives do not know the architectures built from them. They must not import
from attention or transformer.

### Architecture blocks: `attention` and `transformer`

`attention` owns scaled dot-product attention, causal masking, and multi-head
composition. Attention is a building block that composes primitives.

`transformer` owns the transformer block (attention + feed-forward + residual
+ norm), positional encoding, and the output projection head. It composes
primitives and attention blocks into a model architecture.

Neither module owns the training loop. They must not import from train.

### Training and data: `train` and `data`

`train` owns the reusable training-loop structure (forward → loss → backward →
step), metrics (loss, accuracy, perplexity), and checkpointing (model
save/load, future, gated on the safetensors device rung).

`data` owns batching, shuffling, and tokenization. The Shakespeare corpus and
a future safetensors dataset feed the same training loop through the same
batch interface.

## Compiler and package ownership

### Radix

Radix owns the autograd transform, MIR gradient ops, and all codegen. This
includes:

- the AIR reverse-mode AD transform (`radix-air/src/reverse_ad.rs`);
- MIR gradient operations (`radix-mir/src/gradient.rs`);
- gradient lowering in each MIR backend (`radix-mir-wgsl/src/gradient.rs`,
  `radix-mir-llvm/src/gradient.rs`);
- fusion ordering (differentiate before fuse, per ADR `ee3c00a3a`);
- GPU kernel emission (PTX via LLVM→NVVM, WGSL) — the open mir-swarm rungs.

Gradus does not fork or extend the compiler. It consumes the compiler's
autograd capability through `@ radix backward` annotations wrapped behind the
`gradient` module.

### Faber

`faber` owns package build/run orchestration and library-provider resolution.
It should not absorb training policy or become a second model definition
surface.

### `faber-runtime`

`faber-runtime` receives only the generated-code representations that the
application lane needs. The existing runtime autograd tape is a validation
oracle for the compiler output, not the user path. It must not become the
Gradus user surface.

### Examples and corpus

`gradus/corpus` owns training demos that pressure the public Gradus modules.
`examples` owns cross-repository capstones. Neither repository may hide
missing compiler capabilities behind demo-local autograd implementations.

### Cista

Distribution and versioned installation remain a later release checkpoint.
Internal Gradus modules should not become separately versioned Cista packages
until independent release cadence or target isolation is proven.

## Capability vision

### Standard training

The library must provide a standard path for:

- tensor construction and basic operations;
- differentiable functions with compiler-generated gradients;
- gradient correctness validation via finite differences;
- loss functions (MSE, cross-entropy);
- optimizers (SGD, Adam) with learning-rate schedules;
- the training-loop structure (forward, loss, backward, step, metric);
- data loading with batching and shuffling.

### Neural-network primitives

The library must provide differentiable building blocks:

- Linear layer (matmul + bias);
- activation functions (GELU, ReLU, Sigmoid, Tanh, SiLU);
- normalization (LayerNorm, RMSNorm);
- embedding lookup (token and position);
- dropout with train/eval mode switching.

Each primitive must be independently differentiable and finite-difference
validated.

### LLM-shaped architecture

The library must grow toward:

- scaled dot-product attention with causal masking;
- multi-head attention composition;
- transformer blocks (attention + feed-forward + residual + norm);
- positional encoding (learned, sinusoidal, RoPE);
- output projection (logits);
- a complete nanoGPT model definition.

### Training workloads

The library must support:

- character-level tokenization;
- batched training with shuffling;
- training-loop metrics (loss, perplexity, tokens/sec);
- convergence proof (loss decreasing to a real target on a real dataset);
- model save/load (future, gated on safetensors rung).

### GPU acceleration (forcing function)

nanoGPT on Shakespeare is the forcing function. It runs on CPU for correctness
but is agonizingly slow for real iteration (roughly 100× slower than GPU).
This gap drives the GPU gradient path in mir-swarm:

| What nanoGPT demands | What mir-swarm rung it forces |
| --- | --- |
| Fast matrix multiply at real sizes | PTX/CUDA kernels via the LLVM→NVVM path |
| Backward pass through attention at scale | The GPU gradient path — the specific open gap |
| Loading a pre-trained checkpoint later | Safetensors ingest (open device rung) |
| Adam optimizer with momentum states | Real optimizer beyond Norma's SGD stub |

## Proposed implementation horizon

This is a vision-level sequence. Each stage must later lower to its own
repo-aware delivery spec with an executable workload and negative coverage.

### Horizon 0 — Architecture checkpoint

- Freeze the module ownership map and dependency DAG.
- Confirm the Gradus/Radix autograd boundary.
- Confirm the Gradus/Norma isolation boundary.
- Define the first training workload and capstone.
- Record target file names only after live consumers and compiler seams are
  inspected.

### Horizon 1 — Foundation

- Implement `math`, `tensor`, and `gradient` modules.
- Prove finite-difference gradient checks on basic tensor operations.
- Keep all source and generated-Rust gates honest.

### Horizon 2 — First training proof

- Implement `optimize/sgd` and `loss/mse`.
- Prove linear regression converges on CPU through library calls alone.
- This is the "Triga corpus demo renders" equivalent.

### Horizon 3 — NN primitives

- Implement `nn/{linear, activation, norm, embedding}`.
- Each primitive differentiable, finite-difference-checked.
- Expand to `loss/cross_entropy` for classification.

### Horizon 4 — Optimization expansion

- Implement `optimize/adam` and `optimize/schedule`.
- Prove MLP classification converges on CPU.
- The compiler already has an MLP exemplum; the library wraps it.

### Horizon 5 — Attention

- Implement `attention/{scaled_dot_product, causal, multi_head}`.
- Attention differentiable, finite-difference-checked.
- This tests the autograd engine against the hardest math in modern ML.

### Horizon 6 — Transformer

- Implement `transformer/{block, position, head}`.
- Forward pass produces sane output on CPU.
- The full GPT architecture is assembled through library calls.

### Horizon 7 — nanoGPT

- Implement `data/{batch, token}` and the `corpus/nanogpt-shakespeare` demo.
- Train on Shakespeare, generate text.
- **Runs on CPU (slowly); demands GPU.** This is the forcing function.

### Horizon 8 — GPU gradient path

- Radix/host work, not Gradus.
- nanoGPT training 10–100× faster.
- The CPU-to-GPU speedup proves the device-neutral boundary was correct.

### Horizon 9 — Real model work

- `train/checkpoint` (model save/load via safetensors).
- Load, fine-tune, distill a real open-weights model.
- This is where the second-repo question (PyTorch-shaped nn library) becomes
  real — but only if a second caller emerges.

## Capstone vision

The goal should not be considered production-oriented until a training
capstone can:

1. Define a transformer model entirely through Gradus library calls.
2. Train it on a real dataset through the library's training loop.
3. Generate coherent output (Shakespeare-like text).
4. Verify gradients match finite differences at every layer.
5. Demonstrate the CPU-to-GPU speedup once the device path lands.
6. Report structured training metrics (loss, perplexity, tokens/sec).

The capstone is a workload proof, not a benchmark claim. A future model
library or fine-tuning product can be built on these APIs, but Gradus must
first make the gradient, optimization, architecture, and training boundaries
sound.

## Invariants

- One `gradus` source package remains the default distribution unit.
- Every public module has one clear semantic owner.
- No dependency cycle exists between tensor, gradient, loss, optimize, nn,
  attention, transformer, train, and data.
- Gradus public types remain device/backend-neutral.
- Gradus does not import from Norma or any sibling library.
- `@ radix backward` annotations live behind the `gradient` module wrapper,
  not leaked into every public API.
- Gradient correctness requires finite-difference validation.
- Training claims require convergence proof (loss going down to a real target).
- A capability claim requires an executable workload and negative evidence.
- Models are pure functions with explicit parameters (JAX-shaped), not
  object-oriented modules with hidden registration.

## Stop conditions

Stop and revise the architecture if:

- `gradus:gradus` becomes a god module that owns every ML type;
- every new model carries its own optimizer, loss function, or training loop;
- `@ radix backward` appears in every public function signature instead of
  behind the gradient wrapper;
- a specific GPU backend leaks into public Faber values;
- training readiness is claimed without a convergence proof;
- gradient correctness is claimed without finite-difference validation;
- a model is defined that cannot be differentiated end-to-end through Gradus;
- Gradus imports from Norma or any sibling library, breaking self-containment;
- a campaign score is earned by declarations or static source alone rather
  than a real training workload with measurable convergence;
- production readiness is claimed without the nanoGPT capstone and documented
  performance/device limits.

## Validation direction

Every implementation stage must validate at the strongest honest rung:

```text
source checked
  → compiler lowered
    → gradient generated (reverse-AD companion)
      → finite-difference validated
        → training executed
          → convergence measured
            → output checked
```

Required validation families include:

- Gradus source and module-map checks;
- generated-Rust acceptance where the application lane consumes the types;
- Radix gradient lowering and reflection;
- finite-difference gradient checks for every differentiable primitive;
- training-loop execution with explicit loss/perplexity measurement;
- convergence proof (loss decreasing to a real target on a real dataset);
- deterministic reproducibility for the same seed and data;
- performance and memory measurements once GPU scale is claimed.

Static source, generated gradients, or finite-difference checks alone cannot
claim a working training system.

## Later delivery questions

The following questions are intentionally left for architecture checkpoint and
delivery research rather than guessed here:

- What is the minimum tensor genus shape that supports both CPU reference
  execution and future GPU dispatch without a public API break?
- Does Faber need generic field-mapping for parameter-record updates, or is
  per-genus handwriting sufficient through Horizon 7?
- Which positional encoding variant (learned, sinusoidal, RoPE) should be the
  first implementation?
- What tokenization depth is needed for the nanoGPT demo (character-level
  vs. BPE), and does BPE require a Radix-level parsing capability?
- How does checkpoint serialization interact with the safetensors device rung?
- What is the right learning-rate schedule default for nanoGPT-scale training?
- Does a second repo (PyTorch-shaped nn ergonomics) emerge at Horizon 9, or
  does the functional JAX-shape prove sufficient?
- Which second compute backend (after CPU/GPU) gives the most architectural
  information?

## Completion posture

This document is complete as a production vision when it can guide later
delivery work without requiring each stage to rediscover the ownership model.
It is not complete as an implementation plan. No factory phase should begin
from this document alone. The next authorized step is an architecture
checkpoint that converts one bounded horizon into a delivery spec with live
file ownership, fixtures, gates, and commit boundaries.
