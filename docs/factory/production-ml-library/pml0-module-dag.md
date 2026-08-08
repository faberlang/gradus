# PML0 Module DAG + Ownership Table — gradus

**Unit**: PML0-U4 (module DAG + ownership table)
**Date**: 2026-08-08 (grep/ls of `src/*.fab`; no cargo anywhere)
**Source**: live `src/*.fab` — the 11 modules; `src/gradus.fab` facade layer
map; comment-declared dependency contracts and "must not import" rules inside
each module.
**Method**: `grep -o 'gradus:[a-z_]*' src/*.fab | sort -u` for the import
surface; `grep '^importa' src/*.fab` for live import edges; module header
comments for declared dependency intent and forbidden edges.
**Version stamps**: gradus live HEAD at snapshot `d7e85aa6aad1fd41c53524f08c481553b154d042`
(`pml0-source-snapshot.md`); live HEAD at write time `c02ec57` (includes
U1/U2/U5/U7/U8/U14). U4 touches no product code, so `src/**` is unchanged.
**Consumed by**: PML0-U9 (interface packet — module DAG as compiler fact),
PML0-U10 (contract assembly), PML3 (reusable forward models), PML5
(inference layer over the same forward functions).

## 1. The 11 live modules

| Module | File | `functio` | Role today |
| --- | --- | --- | --- |
| attention | `src/attention.fab` | 1 | scaled dot-product attention (`scaled_dot_product_2x8`) |
| data | `src/data.fab` | 0 | stub — batching, shuffling, tokenization planned |
| gradient | `src/gradient.fab` | 2 | autograd wrapper (`nil`, `simple_loss`) |
| gradus | `src/gradus.fab` | 0 | facade — package map only, no genera |
| loss | `src/loss.fab` | 3 | loss functions (MSE 2×2/4×4/2×8) |
| math | `src/math.fab` | 0 | scalar foundation (`epsilon` const; zero genera) |
| nn | `src/nn.fab` | 6 | differentiable primitives (linear, GELU, LayerNorm) |
| optimize | `src/optimize.fab` | 2 | optimizers (SGD step 2×2/4×4) |
| tensor | `src/tensor.fab` | 0 | plain tensor construction/shape/ops (zero genera; owns live `importa`) |
| train | `src/train.fab` | 4 | training steps (2×2, 4×4, bert_linear, bert_layernorm) |
| transformer | `src/transformer.fab` | 3 | transformer blocks (attention, FFN, BERT-tiny) |

"Stub" means zero public genera, not zero code: `math` holds the `epsilon`
constant and `tensor` owns the only live `importa` edge below `gradient`.

## 2. Import DAG

### 2a. Live import edges (the only `importa` statements in the tree)

```text
gradus:gradient ──importa──▶ gradus:tensor ──importa──▶ gradus:math
```

Two live edges, both foundation-building:
- `src/tensor.fab:17` — `importa ex "gradus:math" privata math`
- `src/gradient.fab:15` — `importa ex "gradus:tensor" privata tensor`

The compiled module graph is deliberately small: `math` is the root,
`tensor` builds on it, `gradient` builds on `tensor`. Every other module
declares its dependencies in header comments only, because of the recorded
FMIR stepper limitation — library→library calls are unresolvable, so all
public functions are self-contained tensor-op bodies (`pml0-delivery.md`
"KNOWN TOOLCHAIN CONSTRAINT"; same note in `attention.fab`, `train.fab`,
`transformer.fab`).

### 2b. Comment-declared dependency contract (intent, not live `importa`)

| Module | Declared `Depends on` |
| --- | --- |
| attention | gradus:tensor, gradus:gradient, gradus:nn |
| data | gradus:tensor |
| gradient | gradus:tensor (live) |
| math | nothing (foundation layer) |
| tensor | gradus:math (live) |
| transformer | gradus:tensor, gradus:gradient, gradus:nn, gradus:attention |

### 2c. Facade layer map (`src/gradus.fab`, seven layers)

```text
L1  Tensor foundation   gradus:math, gradus:tensor
L2  Autograd core       gradus:gradient
L3  Loss                gradus:loss
L4  Optimization        gradus:optimize
L5  NN primitives       gradus:nn
L6  Architecture blocks gradus:attention, gradus:transformer
L7  Training and data   gradus:train, gradus:data
```

### 2d. Full module DAG (declared intent, layers L1→L7)

```text
gradus (facade) — owns no genera; maps the leaves below
    │
L1  gradus:math (root — no imports)
      │
    gradus:tensor ──▶ gradus:math          (live edge)
      │
L2  gradus:gradient ──▶ gradus:tensor      (live edge)
      │
L3  gradus:loss        (differentiable; declared standalone)
L4  gradus:optimize    (declared standalone)
L5  gradus:nn          (declared standalone)
      │
L6  gradus:attention ──▶ gradus:tensor, gradient, nn   (declared)
    gradus:transformer ──▶ gradus:tensor, gradient, nn, attention  (declared)
      │
L7  gradus:train       (declared standalone; inline update math)
    gradus:data ──▶ gradus:tensor          (declared)
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
| math | **shared** | scalar foundation; no autograd, no training machinery; consumed by the tensor layer and every tensor-typed module |
| tensor | **shared** | plain tensor values, explicitly NOT autograd-aware (`tensor.fab`); forward evaluation must not depend on autograd |
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
shared:     math, tensor, nn, attention, transformer     (5)
training:   gradient, loss, optimize, train, data        (5)
inference:  (none today — PML5 modules not yet in the tree)
other:      gradus (facade)                              (1)
TOTAL       11
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

- **Parameters** (PML1) — explicit identity and traversal for trainable
  values, consumed by forward evaluation, training updates, and inference
  loading alike.
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
grep -o 'gradus:[a-z_]*' src/*.fab | sort -u   # == the 11 live module names exactly
grep -c '^| gradus' docs/factory/production-ml-library/pml0-module-dag.md   # 1 (facade row)
grep -c '^| ' docs/factory/production-ml-library/pml0-module-dag.md         # 11 rows, each module once
git diff --check
```

- Every `gradus:*` reference in `src/*.fab` resolves to a live module — the
  `sort -u` set is exactly {attention, data, gradient, gradus, loss, math,
  nn, optimize, tensor, train, transformer}, the 11 live modules. There are
  no references to not-yet-existing modules (no `gradus:model`,
  `gradus:decode`, etc.).
- The ownership table contains all 11 live modules exactly once (one row per
  module; shared 5 + training 5 + other 1).
- `git diff --check` clean.

Outcome: `sort -u` import surface == the 11 live modules; the table is
exactly-once over all 11; `git diff --check` clean.
