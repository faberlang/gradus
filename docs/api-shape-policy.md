# Gradus API-Shape Policy

**Version**: `gradus-api-shape-policy v1.0.0` (re-baselined 2026-08-11,
PML6-U1 — lands the PML1 API-shape decision, recorded at the PML1 closeout
R1 record 1 and in `src/tensor.fab` / `src/shape.fab` headers).
**Authority**: the PML0 tensor-API shape posture decision (PML0-U4/U9, open
question answered by PML0; PML1-U3 implements it), the PML1 closeout R1
record 1, and the live source headers.

## The posture: the staged carrier

Gradus uses the **staged carrier**: shape is a runtime dimension list inside
the value carrier (`Tensor.shape`), and the **static shape is pinned by the
consumer at materialization** (boundary types stay `tensor<f32, [2,2]>`).

- **Why**: the generic shape genus (`genus Tensor<magnitudo F>` type-argument
  application) is `PARSE001` and the shape-hole `tensor<f32, _>` genus fields
  / returns are `SEM014` in standalone library context. The staged carrier
  compiles today (PML1 closeout R1 record 1; compiler evidence recorded in
  `src/shape.fab` and `src/tensor.fab`).
- **Boundary unchanged**: the interface packet v1 shape facts (compile-time
  class — shapes are static facts at the boundary) stand. The runtime list is
  the value-carrier representation; the boundary still carries static
  `tensor<f32, [2,2]>` types. This is a representation decision, not a
  boundary revision.

## What it means for signatures

| Surface | Signature form | Example |
| --- | --- | --- |
| **Fixed-shape admitted rows** | `tensor<f32, [..]>` typed tensors | `linear_2x2`, `mse_4x4`, `bert_tiny_block_2x8` — the admitted caller-backed rows |
| **Production (shape-generic)** | `tensor.Tensor` staged carrier | `nn.linear`, `loss.mse`, `attention.scaled_dot_product`, `math.add` — runtime shape facts |

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
  128k–152k vocab rows stay expressible. Tensor construction routes the
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

## Pointers

- Per-symbol signatures: [`docs/api-reference.md`](api-reference.md)
- Module layout + DAG: [`docs/module-map.md`](module-map.md)
- Recorded posture + compiler evidence: PML1 closeout R1 record 1
  (`docs/factory/production-ml-library/pml1-closeout.md`); `src/tensor.fab`
  and `src/shape.fab` headers.
