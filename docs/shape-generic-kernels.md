---
title: Shape-generic kernel entries — the preferred multi-geometry form
date: 2026-08-24
status: design note for GEA2-U3 authorship
---

# Shape-generic kernel entries

`tbf16[320,960]` is a receipt pin, not an idiom. When a kernel serves more
than one concrete geometry, the preferred form is the shipped shape-generics
surface — `magnitudo` parameters unified from argument shapes at call sites
(shape-generics D1; closed 2026-08-18, four phases):

```
# en surface
@ kernel
fn gemv<size A, size B>(tbf16[A, B] weights, tf32[B] input, mut tf32[A] output, u32 id) → void {
    output ← weights · input
}
```

This signature checks green today (probed 2026-08-24). Phase-4 monomorphization
delivers the per-shape device bodies; the call site binds `A`/`B` implicitly
from argument shapes — no explicit shape arguments, no concrete-overload zoo
(the `sgd_step_2x2`-class repetition shape-generics deleted in norma).

## When concrete, when generic

- **Concrete shapes**: justified while a campaign's identity law pins one
  geometry for receipts (GEA1's `[320,960]` is a frozen-chain artifact — the
  pinned receipt, not the style).
- **Generic shapes**: the default the moment a second geometry exists. GEA2's
  block needs QKV, FFN, and (MoE variants) expert projections at different
  geometries — one `gemv<A, B>` monomorphized per projection, not five
  concrete bodies. Multiple concrete callers are themselves the two-bodies
  evidence the campaign law asks for before an abstraction is shared.
- **Deliberate limits** (shape-generics D5): dims are literals and `magnitudo`
  params only; no shape arithmetic (`tbf16[A, B+1]` is out of scope by
  design); no general const expressions in figura position.

## The standing law

Do not hand-name shapes (`const GEMV_N ← 320` re-spelling the type), and do
not hand-copy concrete bodies per geometry. Shapes live in the type — as
literals when pinned, as `magnitudo` parameters when the kernel is generic.
This is the L3 remedy in `docs/legacy-ml-antipatterns.md`: delete the
duplicate spellings; parameterize the geometry when it varies.

## Consumers

- GEA2-U3 authorship (the first multi-geometry caller).
- `docs/legacy-ml-antipatterns.md` L3 (shape recovery / triple-spelling).
- faber skill idioms (cross-reference when the generic-kernel exemplar lands).
