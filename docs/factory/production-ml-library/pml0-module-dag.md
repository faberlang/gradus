# PML0 Module DAG + Ownership Table — gradus

**Unit**: PML0-U4 (module DAG + ownership table), re-snapshotted at PML1
closeout
**Date**: 2026-08-08 (PML0) / 2026-08-09 (PML1 re-snapshot; grep/ls of
`src/*.fab`, no cargo anywhere)
**Source**: live `src/*.fab` — the 15 modules; `src/gradus.fab` facade layer
map; comment-declared dependency contracts and "must not import" rules inside
each module.
**Method**: `grep -o 'gradus:[a-z_]*' src/*.fab | sort -u` for the import
surface; `grep '^importa' src/*.fab` for live import edges; module header
comments for declared dependency intent and forbidden edges.
**Version stamps**: PML1 closeout at gradus HEAD (PML1-U1..U7 landed,
45a09d9..de017eb). U1/U2/U4/U5/U7 touched product code since the PML0
snapshot; this re-snapshot reflects the live tree.
**Consumed by**: PML0-U9 (interface packet — module DAG as compiler fact),
PML0-U10 (contract assembly), PML3 (reusable forward models), PML5
(inference layer over the same forward functions).

## 1. The 15 live modules

| Module | File | `functio` | Role today |
| --- | --- | --- | --- |
| attention | `src/attention.fab` | 1 | scaled dot-product attention (`scaled_dot_product_2x8`) |
| data | `src/data.fab` | 0 | stub — batching, shuffling, tokenization planned |
| dtype | `src/dtype.fab` | 14 | versioned dtype system: DType tag + cast/round/serialize (U2) |
| gradient | `src/gradient.fab` | 2 | autograd wrapper (`nil`, `simple_loss`) |
| gradus | `src/gradus.fab` | 0 | facade — package map only, no genera |
| loss | `src/loss.fab` | 3 | loss functions (MSE 2×2/4×4/2×8) |
| math | `src/math.fab` | 22 | pure operation families (elementwise/reduce/matmul/cast/concat) |
| nn | `src/nn.fab` | 6 | differentiable primitives (linear, GELU, LayerNorm) |
| optimize | `src/optimize.fab` | 0 | empty facade post-U6 (sgd_step_* retired) |
| parameter | `src/parameter.fab` | 37 | parameter identity and traversal (U5) |
| serialize | `src/serialize.fab` | 34 | versioned bytes serialization contract (U7) |
| shape | `src/shape.fab` | 9 | shape rules: broadcast/reshape/expand, bounded product (U3) |
| tensor | `src/tensor.fab` | 11 | plain tensor construction/shape/ops (not autograd-aware) |
| train | `src/train.fab` | 4 | training steps (2×2, 4×4, bert_linear, bert_layernorm) |
| transformer | `src/transformer.fab` | 1 | transformer blocks (`bert_tiny_block_2x8`) |

"Stub"/"empty facade" means zero public genera, not zero code: `data` and
`optimize` hold no functions; `gradus` is the facade map. `functio` counts
include `@ privata` helpers (math 8, parameter 5, serialize 15, shape 2) —
the live inventory table (`pml0-symbol-inventory.md`) carries the full counts.

## 2. Import DAG

### 2a. Live import edges (the only `importa` statements in the tree)

```text
gradus:math ──importa──▶ gradus:dtype
gradus:math ──importa──▶ gradus:shape
gradus:math ──importa──▶ gradus:tensor
gradus:parameter ──importa──▶ gradus:dtype
gradus:parameter ──importa──▶ gradus:shape
gradus:parameter ──importa──▶ gradus:tensor
gradus:gradient ──importa──▶ gradus:tensor
gradus:tensor ──importa──▶ gradus:dtype
gradus:tensor ──importa──▶ gradus:shape
```

- `src/tensor.fab` — `importa ex "gradus:dtype" privata dtype`,
  `importa ex "gradus:shape" privata forma`
- `src/gradient.fab` — `importa ex "gradus:tensor" privata tensor`
- `src/math.fab` — `importa ex "gradus:dtype" privata dtype`,
  `importa ex "gradus:shape" privata forma`,
  `importa ex "gradus:tensor" privata tensor`
- `src/parameter.fab` — `importa ex "gradus:dtype" privata dtype`,
  `importa ex "gradus:shape" privata forma`,
  `importa ex "gradus:tensor" privata tensor`

The compiled module graph has nine live edges over the foundation leaves:
`dtype` and `shape` are roots (import nothing); `tensor` builds on both;
`math` builds on all three; `parameter` builds on all three; `gradient`
builds on `tensor`. Every other module declares its dependencies in header
comments only, because of the recorded FMIR stepper limitation —
library→library calls are unresolvable, so all public functions are
self-contained tensor-op bodies (`pml0-delivery.md` "KNOWN TOOLCHAIN
CONSTRAINT"; same note in `attention.fab`, `train.fab`, `transformer.fab`).

The dtype seam: PML1-U2 moved the dtype tag to `src/dtype.fab` because
cross-module enum variant references are unsupported in library context
(SEM001/SEM041 — a language constraint, recorded here; the DType tag lives
in one module and is consumed via factory functions `dtype.f32()` etc., and
error types use `causa()` accessors rather than cross-module variant
matching). The U1 tensor → math edge is dropped at U4: math.fab owns the
pure operation families and imports tensor (math → tensor is the live edge;
tensor never referenced math — the import was unused). Tensor construction
consumes ONE validator from `gradus:shape` (`quantitas`, the bounded
product) — CTO-2 shape-policy correction, PML1 closeout.

### 2b. Comment-declared dependency contract (intent, not live `importa`)

| Module | Declared `Depends on` |
| --- | --- |
| attention | gradus:tensor, gradus:gradient, gradus:nn |
| data | gradus:tensor |
| dtype | nothing (foundation layer; owns the DType tag) |
| gradient | gradus:tensor (live) |
| math | gradus:tensor, gradus:dtype, gradus:shape (all live) |
| parameter | gradus:dtype, gradus:shape, gradus:tensor (all live) |
| serialize | nothing (leaf module; contract mirrors documented in header) |
| shape | nothing (leaf module) |
| tensor | gradus:dtype, gradus:shape (both live) |
| transformer | gradus:tensor, gradus:gradient, gradus:nn, gradus:attention |

### 2c. Facade layer map (`src/gradus.fab`)

```text
L1  Tensor foundation   gradus:dtype, gradus:shape, gradus:math, gradus:tensor
L2  Autograd core       gradus:gradient
L3  Loss                gradus:loss
L4  Optimization        gradus:optimize
L5  NN primitives       gradus:nn
L6  Architecture blocks gradus:attention, gradus:transformer
L7  Training and data   gradus:train, gradus:data
SC  Shared value contracts (PML1)   gradus:parameter, gradus:serialize
```

### 2d. Full module DAG (declared intent, layers L1→L7 + SC)

```text
gradus (facade) — owns no genera; maps the leaves below
    │
L1  gradus:dtype (root — no imports)    gradus:shape (root — no imports)
      │                                       │
    gradus:tensor ──▶ gradus:dtype, gradus:shape   (live edges)
      │
L2  gradus:gradient ──▶ gradus:tensor      (live edge)
      │
    gradus:math ──▶ gradus:dtype, gradus:shape, gradus:tensor   (live edges)
    gradus:parameter ──▶ gradus:dtype, gradus:shape, gradus:tensor (live edges)
      │
L3  gradus:loss        (differentiable; declared standalone)
L4  gradus:optimize    (empty facade post-U6)
L5  gradus:nn          (declared standalone)
      │
L6  gradus:attention ──▶ gradus:tensor, gradient, nn   (declared)
    gradus:transformer ──▶ gradus:tensor, gradient, nn, attention  (declared)
      │
L7  gradus:train       (declared standalone; inline update math)
    gradus:data ──▶ gradus:tensor          (declared)
      │
SC  gradus:serialize   (leaf — no imports; mirrors shape ceilings and dtype
                        names in its own contract)
```

### 2e. Forbidden edges (architectural rules recorded in the modules)

| Module | Must not import from | Rationale (verbatim intent) |
| --- | --- | --- |
| attention | gradus:transformer | attention is a building block, not a transformer component |
| loss | gradus:optimize, gradus:nn | a loss is a differentiable function, not an optimization concern |
| nn | gradus:attention, gradus:transformer | primitives do not know the architectures built from them |
| optimize | gradus:nn, gradus:attention, gradus:transformer | optimizers consume raw tensors, not layer abstractions |
| transformer | gradus:train | a transformer does not own its training loop |
| gradient | loss, optimize, nn, attention, transformer | pure calculus — does not know what it differentiates |
| train | any specific model definition | the training loop is reusable across models |

The DAG is acyclic under both the live edges and the declared intent; no
layer imports upward.

## 3. Ownership table (each module exactly once)

Ownership follows the campaign's desired end state: shared contracts are
consumed unchanged by training **and** inference; autograd, losses,
optimizers, datasets, and training loops stay a training layer over reusable
forward functions; the inference layer (decode, KV cache, sampling,
generation) lands in PML5 over the same forward functions.

| Module | Ownership | Basis |
| --- | --- | --- |
| dtype | **shared** | element-type tag + cast/round rules; consumed by tensor/math/parameter and every value surface, training and inference alike |
| shape | **shared** | shape rules over dimension vectors; consumed by tensor/math/parameter/serialize and the admission surfaces |
| math | **shared** | scalar/foundation + pure operation families; consumed by the tensor layer and every tensor-typed module |
| tensor | **shared** | plain tensor values, explicitly NOT autograd-aware (`tensor.fab`); forward evaluation must not depend on autograd |
| parameter | **shared** | parameter identity and traversal, consumed by forward evaluation, training updates, and inference loading alike (U4 §4) |
| serialize | **shared** | versioned bytes round-trip for tensor/dtype/shape/parameter; consumed by training (checkpoint) and inference (model load) |
| nn | **shared** | differentiable NN primitives used by forward evaluation; desired end state: neural-network contracts shared by training and inference |
| attention | **shared** | attention is a building block over forward functions; desired end state: attention contracts shared |
| transformer | **shared** | transformer contracts shared by training and inference; block functions are forward-only (usable with and without autograd) |
| gradient | **training** | the autograd wrapper; "Autograd … remain a training layer over reusable forward functions" |
| loss | **training** | losses are the training layer's objective over forward outputs |
| optimize | **training** | optimizers update parameters only inside training |
| train | **training** | training steps and the training loop |
| data | **training** | data loading (batching, shuffling) feeds the training loop; the future `data/token` leaf's tokenizer-identity contract is shared per desired end state #2 and splits at the nested-leaf boundary |
| gradus | **other** | facade — package map, owns no genera and no semantics |

```text
shared:     dtype, shape, math, tensor, parameter, serialize, nn,
            attention, transformer              (9)
training:   gradient, loss, optimize, train, data        (5)
inference:  (none today — PML5 modules not yet in the tree)
other:      gradus (facade)                              (1)
TOTAL       15
```

Inference ownership is **empty by measurement, not by omission**: no decode,
KV-cache, sampling, or generation module exists in the live tree. Those
modules are PML5 work and will sit in the inference column over the shared
forward functions above.

## 4. Future shared layer — forward semantics usable with and without autograd

The desired end state's invariant: **reusable model evaluation must not
depend on autograd** (CAMPAIGN.md, Development Posture — "Forward functions
first"). Training requests compiler-generated backward companions from
`gradus:gradient`; inference calls forward and decode paths without building
a gradient path. The future shared layer is the set of modules both sides
consume unchanged:

- **Parameters** (PML1, landed U5) — explicit identity and traversal for
  trainable values, consumed by forward evaluation, training updates, and
  inference loading alike.
- **Serialization** (PML1, landed U7) — versioned bytes round-trip for
  tensor/dtype/shape/parameter values; the wire contract both sides consume.
- **`gradus:model` + model-format admission** (PML2) — model metadata,
  Safetensors and admitted GGUF rows, migrated from `norma:model` under the
  PML0-U8 decision (no dual authority; migrate at PML2, not now). Admission
  fails closed by format, architecture, dtype, quantization, shape,
  tokenizer identity, and version (PML0-U5 schema).
- **Tokenizer identity** (PML2, split from `data`) — the shared tokenizer
  contract named in desired end state #2; `data` itself stays the
  training-side loader.
- **Forward architectures** (PML3) — nn, attention, and transformer functions
  qualified as composable, testable, and usable with and without autograd.
- **Decode, KV-cache, sampling, generation** (PML5) — the inference layer,
  **not** shared (training never builds a gradient path through them); they
  consume the shared forward functions above.

Membership rule: a module is shared when **both** training and inference
consume the same function unchanged. Autograd-gated variants (gradient,
loss, optimize, train) and data loading are training-layer. Decode/cache/
sampling/generation are inference-layer. This keeps the shared layer
autograd-free by construction — the compiler generates backward companions
only when training composes the same forward calls.

## 5. Validation

```bash
cd /Users/ianzepp/work/faberlang/gradus
grep -o 'gradus:[a-z_]*' src/*.fab | sort -u   # == the 15 live module names exactly
grep -c '^| gradus' docs/factory/production-ml-library/pml0-module-dag.md   # 1 (facade row)
grep -c '^| ' docs/factory/production-ml-library/pml0-module-dag.md         # 15 rows, each module once
git diff --check
```

- Every `gradus:*` reference in `src/*.fab` resolves to a live module — the
  `sort -u` set is exactly {attention, data, dtype, gradient, gradus, loss,
  math, nn, optimize, parameter, serialize, shape, tensor, train,
  transformer}, the 15 live modules. There are no references to not-yet-
  existing modules (no `gradus:model`, `gradus:decode`, etc.).
- The ownership table contains all 15 live modules exactly once (one row per
  module; shared 9 + training 5 + other 1).
- `git diff --check` clean.

Outcome: `sort -u` import surface == the 15 live modules; the table is
exactly-once over all 15; `git diff --check` clean.
