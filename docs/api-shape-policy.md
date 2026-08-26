# Gradus API-Shape Policy

**Version**: `gradus-api-shape-policy v1.1.0` (2026-08-21, TEU5 — B1-vs-B2
error-identity ruling recorded below; v1.0.0 re-baselined 2026-08-11,
PML6-U1 — lands the PML1 API-shape decision, recorded at the PML1 closeout
R1 record 1 and in `src/tensor.fab` / `src/shape.fab` headers).
**Authority**: the PML0 tensor-API shape posture decision (PML0-U4/U9, open
question answered by PML0; PML1-U3 implements it), the PML1 closeout R1
record 1, the live source headers, and for error identity the 2026-08-21
operator session recorded in faber `docs/design/typed-error-union.md`.

## The posture: the staged carrier

Gradus uses the **staged carrier**: shape is a runtime dimension list inside
the value carrier (`NumericBlock.shape`), and the **static shape is pinned by the
consumer at materialization** (boundary types stay `tensor<f32, [2,2]>`).

- **Why**: the generic shape genus (`genus NumericBlock<magnitudo F>` type-argument
  application) is `PARSE001` and the shape-hole `tensor<f32, _>` genus fields
  / returns are `SEM014` in standalone library context. The staged carrier
  compiles today (PML1 closeout R1 record 1; compiler evidence recorded in
  `src/shape.fab` and `src/tensor.fab`).
- **Boundary unchanged**: the interface packet v1 shape facts (compile-time
  class — shapes are static facts at the boundary) stand. The runtime list is
  the value-carrier representation; the boundary still carries static
  `tensor<f32, [2,2]>` types. This is a representation decision, not a
  boundary revision.

## Executed tier of record

Gradus's executed tier of record is the CPU/reference tier — f32 host-list
carrier (`src/tensor.fab` `class NumericBlock` `list<f32> data`), reference
kernels, and FMIR stepper receipts. Device residency and emission are
Radix and hosts scope.

## What it means for signatures

| Surface | Signature form | Example |
| --- | --- | --- |
| **Fixed-shape admitted rows** | `tensor<f32, [..]>` typed tensors | `linear_2x2`, `mse_4x4`, `bert_tiny_block_2x8` — the admitted caller-backed rows |
| **Production (shape-generic)** | `tensor.NumericBlock` staged carrier | `nn.linear`, `loss.mse`, `attention.scaled_dot_product`, `math.add` — runtime shape facts |

The concrete-overload precedent (norma:optimizer) governs the fixed-shape
rows; the production surface keeps shapes as runtime facts.

## R3 — no one-row / one-shape narrowing in the public API

Admission and capability descriptors stay **extensible**: support rows and
descriptors carry shape/dtype/quantization facts as data, never as
hard-coded public-API generics. A new admitted row is a new support row in
`pml0-support-matrix.md` (U3), not a new API shape. The capsule's
`Limites` / `Quantizatio` / `Architectura` field groups are the current
shape-carriers (PML2, council R3).

## Cross-module variant constraint

Enum variants cannot be referenced across module boundaries in
library-context checks (SEM001/SEM041 — a language constraint, recorded
PML1). Consequences:

- The `DType` tag lives in ONE module (`gradus:dtype`) and is consumed via
  factory functions (`dtype.f32()`), never cross-module variant matching.
- Error types expose `message()` accessors rather than cross-module variant
  matching; every public function's error vocabulary is the module's own
  typed `*Error` discretio.
- The model module follows the same rule: gguf/safetensors consume
  `model/capsule` through accessors and constructors, never through variant
  matching.

## Ceilings (CTO-2 correction, folded at PML1 closeout)

- The 65536 per-dimension cap is the GI1 pinned-row **capsule/support-row
  admission ceiling** (`pml0-model-capsule-contract.md` §5 row 5), NOT a
  general math limit.
- General checked shape arithmetic (`numel` / `broadcast` /
  `reshape` / `expand`) does not apply the per-dimension cap, so
  128k–152k vocab rows stay expressible. NumericBlock construction routes the
  element product through ONE validator: `shape.numel`.
- The serialize mirror was aligned to `shape.numel` (no per-dimension
  cap; element ceiling 1_000_000_000 and negative-dim rejection retained;
  wire schema unchanged — `serialize-schema-1.0.0`).

## Rules of the road

- Prefer leaf imports; do not grow genera on the `gradus:gradus` facade.
- Prefer receiver methods on genera; free functions for constructors /
  scalars / generators only.
- Optional genus fields use `sponte`.
- `@ radix backward` annotations live behind the `gradus:gradient` wrapper,
  not leaked into every public function signature.
- Public signatures stay on primitives plus the module's own genera so proba
  file-interfaces keep every export (WARN014 seam).

## Error identity (TEU5) — B1 vs B2

**Decider**: operator session 2026-08-21 (faber
`docs/design/typed-error-union.md`, fork-3 remainder).
**Recorded**: TEU5, 2026-08-21, this section.
**Status**: **default-not-settled.** The session lean is the default this
delivery executes unless the operator flips to B2 before TEU7 is tasked.
TEU7's `done_when` already carries both branches. This ruling does not
re-open fork 1 (`@ commune`) or the rejected Zig-style `⇥` widening.

**Execution dependency X1** (blocks TEU7, not this ruling): radix
`compiler-defect-sprint` units `cds-u1-union-match` (registry row 1,
SEM001 imported-union match) and `cds-u7-generic-construction` +
`cds-u8-import-binding-collisions` (registry row 9, qualified variant
construction). The "Cross-module variant constraint" section above still
states the stale PML1 framing; TEU8 rewrites that paragraph after X1
lands. TEU6 (`@ commune` mirrors) is independent of this fork.

### The two options

**B1 — shared package error union.** `gradus:error` owns `GradusError`.
Package-internal composition throws its variants directly. Remap chains
and error-translating wrappers disappear on every edge that shares the
type. Cost: one package-global variant namespace; per-module vocabulary
moves into function docs.

**B2 — per-module unions + typed remap.** Every module keeps its `*Error`
union. Wrappers stay, but match imported variants (`case nn.NegativeDimension`)
instead of comparing `message()` text. Compiler-checked identity. The
N×M wrapper wall remains.

**Session lean (default-not-settled):** B1 for package-internal
composition, with per-module unions only at genuine public boundaries.
That is **lean-B1**, not full-B1. Full-B1 (every union merges) is recorded
below as the stricter sibling so the operator can flip the merge set
without a new design session.

### Lean-B1 membership test (the TEU7 criterion)

A per-module union **merges** into `gradus:error GradusError` when both:

1. A majority of its variants are the **shape-family eight** copied up the
   spine: `NegativeDimension`, `DimensionAboveLimit`, `ProductAboveLimit`,
   `GradusMismatch`, `ShapeMismatch`, `Incompatible`, `DtypeMismatch`,
   `ElementMismatch`.
2. The union exists primarily so a composer can remap a callee's error
   into "this module's" type.

A per-module union **stays** (genuine public boundary) when either:

1. Its variants name facts only this module observes (tokenizer vocab,
   GGUF wire, cache gap, admission digest, optimizer slot identity).
2. Merging would collide a name with a different meaning (`Overflow` as
   cache capacity vs numeric cast; `UnknownName` as dtype tag vs
   parameter vs payload tensor).

The current `gradus:mlp` union is already named `GradusError`. Lean-B1
vacates that name: mlp's union *is* the seed of the package type;
`gradus:mlp` then imports `gradus:error`.

### Inventory — 36 error unions at HEAD `5ed351e`

35 modules; `data.fab` (stub) and the `gradus.fab` facade have none.
36 error unions, 33 `fn message()` mirrors (qwen35moe carries four unions
and three renderers: `message` / `tensor_message` / `reference_message`).
269 variant slots, 120 distinct variant names (45 names appear in more
than one union, 75 are unique).

#### Merge under lean-B1 (composition cluster — 8 unions, 73 slots)

| Module | Union | Variants | Shape-family share |
| --- | --- | --- | --- |
| `gradus:shape` | `ShapeError` | 6 | 6/6 |
| `gradus:math` | `MathError` | 11 | 8/11 |
| `gradus:nn` | `NnError` | 9 | 8/9 |
| `gradus:attention` | `AttentionError` | 11 | 8/11 |
| `gradus:transformer` | `TransformerError` | 12 | 8/12 |
| `gradus:mlp` | `GradusError` | 8 | 8/8 |
| `gradus:loss` | `LossError` | 9 | 8/9 |
| `gradus:metrics` | `MetricError` | 7 | 6/7 |

Cluster-local extras fold into the shared type (one copy each):
`InvalidEpsilon` (collapses transformer's `EpsilonInvalida`),
`InvalidPosition`, `InvalidDimension`, `InvalidConfig`, `InvalidMode`,
`NonFinite`, `Overflow` (math numeric), `UnknownName` (math←dtype),
`Invalid` (metrics). After collapse the shared union is ~17 variants,
not 73.

#### Stay under lean-B1 (genuine public boundaries — 28 unions)

Foundation that is not a shape-family copy: `DTypeError`, `TensorError`
(`IndexOutOfBounds` is tensor-local).

Training / values: `ParameterError`, `SerializeError`, `GradientError`,
`OptimizeError`, `TrainError`.

Inference domain: `CacheError`, `DecodeError`, `SamplingError`,
`GenerationError`.

Tokenizer / calibration: `TokenizerError`, `CalibrationError`.

Model admission and adapters: `ArtifactError`, `AdmissionError`,
`GgufError`, `GgufManifestError`, `SafetensorError`, `DequantError`,
`PayloadError`, `ViewError`, `DenseError`, `LlamaError`,
`DenseQwen2Error`, and qwen35moe's four
(`Qwen35moeConfigError` / `Qwen35moeTensorError` /
`Qwen35moeReferenceError` / `Qwen35moeAdmissionError`).

`DecodeError` (5/11 shape-family) and `DenseError` (assembly-specific
`MissingTensor` / `TerminusExcedit` / copied `Overflow`/`Gap`) stay
because callers of those import paths match domain variants, not the
spine eight. Their remaining spine remaps become **typed match on the
one `GradusError`**, an N×1 wall, not N×M.

#### Merge under full-B1 (all 36 → 1)

Everything in both tables. Six names need disambiguating prefixes
because they do **not** mean the same thing across unions:

| Name | Distinct meanings |
| --- | --- |
| `Overflow` | cache/dense capacity vs dtype/math numeric cast |
| `UnknownName` | dtype tag vs parameter vs payload tensor vs qwen35moe reference |
| `InvalidConfig` | attention RoPE vs generation vs sampling |
| `Invalid` | calibration vs metrics |
| `BadShape` | serialize wire vs GGUF/safetensors vs dense runtime |
| `IdOutOfRange` | cache vs decode |

The other shared names (shape-family eight, `Gap` — dense copies cache,
`BadDigest` / `BadFormat` / `MissingTensor` / `Cancelled` / `BadWire` / …)
are the same fact copied. Full-B1 is correct for those and punitive for
the colliding six.

### Wrappers and remap chains

Named string→variant chains (the census three):

| Site | Today | Lean-B1 | Full-B1 | B2 |
| --- | --- | --- | --- | --- |
| `src/transformer.fab:259` `_map_error` (12 throw sites: nn/math/attention) | string match | **delete** (same `GradusError`) | **delete** | typed `match err { case nn.… }` |
| `src/mlp.fab:122` `_map_error` (2 throw sites: nn) | string match | **delete** | **delete** | typed match |
| `src/model/dense.fab:311` `_map_cached` (1 throw site: transformer) | string match | typed match on `GradusError` / `CacheError` (Dense stays) | **delete** | typed match |

Error-translating private wrappers that exist only to change the error
type (vanish under lean-B1 on the composition cluster, under full-B1
everywhere):

- transformer: `_linear`, `_gelu`, `_layernorm`, `_add`, `_attention`,
  `_rmsnorm`, `_swiglu`, `_multi_attention`, `_attention_cached`,
  `_multi_attention_cached`
- mlp: `_linear`, `_gelu`

Inline string-compare remaps (not named `_map_*`; same defect):

- composition cluster, callee also merges (vanish under lean-B1):
  `math.fab` shape (2 sites), `nn.fab` shape (1) + math (2),
  `attention.fab` math (4), `loss.fab` shape (1)
- foundation/domain edges that stay under lean-B1 (typed match; vanish
  only under full-B1): `math.fab` tensor (1) + dtype (2), `attention.fab`
  tensor (1) + cache (1), `decode.fab` transformer (2) + nn (1),
  `generation.fab` (sampling/train/decode/dense/tensor), `dense.fab`
  (tensor/nn/transformer message-copy into `BadShape`), plus
  message-copy wrappers in `parameter`, `optimize`, `cache`, `train`,
  `gradient`, `tokenizer`, `qwen35moe`, `safetensors`, `gguf`,
  `tensor_view`, `dense_qwen2`

Under B2 every row in that list stays as a function and only the body
changes from `if c ≡ "…"` to `case callee.Variant`.

### Blast radius against the census

Recorded census (delivery, 2026-08-21, gradus `5ed351e`): 3 remap chains,
33 mirrors across 35 modules, 111 `message(` occurrences in `src` (33 of
them the mirror definitions), 200 in `.proba`, 260 `^\s+string message$`
payload lines in 32 files.

Live re-measure at the same commit (ground truth; `rg --count-matches`):

| Surface | Recorded | Live |
| --- | --- | --- |
| `fn message(` mirrors | 33 | 33 |
| modules (error-bearing / total) | 33 / 35 | 33 / 35 |
| error unions | (not separately counted) | 36 |
| `^\s+string message$` payload lines | 260 (32 files) | 260 (32 files) |
| `message(` in `src/**/*.fab` | 111 | **116** (33 defs + 83 uses) |
| `message(` in `src/**/*.proba` | 200 | **203** |
| named remap chains | 3 | 3 |
| `⇥ *Error` signatures in `src/**/*.fab` | (not in census) | 397 (32 files) |

The live `message(` delta (+5 src, +3 proba) is counted here so TEU6's
call-site oracle is not short. Mirrors and payload lines match. TEU6
still owns the 33-mirror / 260-payload clean break regardless of B1/B2.

| Option | Mirrors (TEU6) | Named chains | Translating wrappers | `⇥ *Error` signatures | Variant namespace |
| --- | --- | --- | --- | --- | --- |
| B2 | 33 → 0 via `@ commune` | 3 bodies become typed match | stay (N×M) | 36 types unchanged | 36 unions, 120 names |
| Lean-B1 (default) | same TEU6 | 2 of 3 delete; `_map_cached` becomes typed match | cluster wrappers delete; domain←spine become N×1 typed match | 8 modules retarget onto `GradusError`; 28 keep their type | 1 shared (~17 variants) + 28 domain |
| Full-B1 | same TEU6 | 3 delete | all delete | 397 signatures → `⇥ GradusError` | 1 union; 6 colliding names renamed |

### Recommendation and migration cost

**Recommend lean-B1** (the session lean, default-not-settled).

It kills the fragile half of the problem — the three named chains and the
composition-cluster N×M wall — without forcing tokenizer / GGUF /
optimizer / cache callers onto a 120-name package enum. Domain modules
keep a vocabulary callers already match. The remaining remaps are typed
and one-sourced (`GradusError` or a named domain union), which is what
X1 makes cheap.

Per-option TEU7 cost (TEU6 is the same clean break in all three):

| Option | TEU7 shape | Cost | Residual |
| --- | --- | --- | --- |
| **B2** | Rewrite every string-compare remap body to `case callee.Variant`. Keep wrappers and 36 unions. | Lowest signature blast. Mechanical, still N×M functions to keep forever. | Wrapper wall; new composers add another `_map_error`. |
| **Lean-B1** | Add `src/error.fab` (`gradus:error`). Move the 8-union cluster onto `GradusError`. Delete transformer/mlp `_map_error` and the type-changing wrappers. Rewrite remaining domain←spine remaps as typed match. | Medium. Signature chase limited to the 8 merged modules + their probas/exempla. mlp's `GradusError` name is reused, not invented. | N×1 typed remaps at dense/decode/generation/parameter/… boundaries. Operator may later fold a boundary (e.g. `DecodeError`) without a language change. |
| **Full-B1** | Same new module; merge all 36; prefix the 6 colliding names; retarget 397 `⇥ *Error` sites and every proba/exempla catch. | Highest. Docs absorb per-module vocab. One catch type for the whole package. | Zero remaps. Callers of `gradus:tokenizer` and `gradus:nn` share one enum; exhaustiveness and docs become the vocabulary. |

Flip window: operator may choose B2 or widen lean-B1 to full-B1 before
TEU7 is tasked. After X1, not before. TEU6 does not wait on this ruling.

## Pointers

- Per-symbol signatures: [`docs/api-reference.md`](api-reference.md)
- Module layout + DAG: [`docs/module-map.md`](module-map.md)
- Recorded posture + compiler evidence: PML1 closeout R1 record 1
  (`docs/factory/production-ml-library/pml1-closeout.md`); `src/tensor.fab`
  and `src/shape.fab` headers.
- Error-identity design (fork 1 `@ commune`, fork-3 B1/B2, X1): faber
  `docs/design/typed-error-union.md`; delivery unit TEU5 in faber
  `docs/factory/typed-error-union/delivery.md`.
