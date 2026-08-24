# Legacy ML Shapes and Patterns that are Faber Anti-Patterns

**Status**: active — inventory v1 (session-codified 2026-08-24); drives the
gradus conversion sweep and the skill's review triggers

## Why this document exists

Training data for ML code is overwhelmingly Python/C-shaped: loops over
extents, manual accumulators, stride arithmetic, shape recovery from runtime
values. LLM-authored Faber will faithfully resurrect those shapes because
retrieval has seen nothing else — the 960× guarded GEMV scan in GEA1 was not
carelessness, it was training-data residue from languages that lacked the
construct. In Faber, each legacy shape is not merely unidiomatic: it re-opens a
bug class the language construct exists to make unwritable. This inventory
names each legacy shape, the Faber form that replaces it, and the bug class
the replacement deletes. The canonical review surface (canonical-faber) flags
these on sight; the faber skill's idiom section carries the same list as
authoring guidance.

## The inventory

| # | Legacy ML shape (Python/C prior) | Faber form | Bug class deleted | Live instances |
|---|---|---|---|---|
| L1 | Matmul/conv/GEMV by nested loops with guards ("if in my row/col") | tensor glyphs `· ⊗ ⊙ ×`; recipe lowering | guard-logic errors; O(rows·cols) scans reading as O(n) work; accumulation-order bugs | GEA1 pre-glyph (deleted); watch corpus |
| L2 | `for i in range(n)` where n re-derives a container's extent; body hand-indexes that container (`x[i*cols+j]`) | `for from x at [i]` / `at [r, c]` — iterate the container | stride math errors (silent OOB reads); AIR unroll impossible (non-literal extents fail closed); severed loop↔data coupling | attention.fab softmax ×3; 21 range loops in 4 ML files; 23 stride expressions |
| L3 | Shape recovery ritual: `m ← shape.get(0) coalesce 1; k ← shape.get(1) coalesce 1` before any compute | shapes in types (`tf32[320,960]` when pinned; `magnitudo` params when the kernel serves multiple geometries — see `docs/shape-generic-kernels.md`; shape-binding proposal REJECTED 2026-08-24 on LLM-ergonomics grounds — literals + compiler consistency checks, not named shapes) | coalesce-eaten OOB (plausible-zero reads); magic-number drift between type literal, const, and message string; runtime shape lies | nn.fab:398-400; attention.fab ×4; safetensors 1006 |
| L4 | Manual accumulator loops (`acc ← 0.0; for … acc ← acc + x`) | `sum from … at [i] thread f const s { … }` (lane-distributed on device) | accumulation-order bugs; init-value bugs; serial-reading parallel work | attention softmax exp-sum; train loops |
| L5 | Softmax-by-hand (find max, exp loop, sum, divide) | the causal-softmax / reduce construct family (device-admitted: `causal_softmax` plan exists) | numerically-unstable max-omission; three separate hand loops per site | attention.fab `_softmax` ×2 (near-duplicates) |
| L6 | Error-type string matching / message wrapping (`case` per variant just to unwrap a string; comparing caught message text) | `@ commune` shared fields + direct `e.message`; variant-matched catch | wording-coupled misclassification; wrapper drift across 39 unions (fixed 2026-08-24); silent catch-all reclassification | converted; qwen35moe 3 dispatch wrappers remain |
| L7 | Checked-get appeasement (`x.get(i) coalesce 0.0` in loops the author knows are in-bounds) | iterate-the-container (L2); bounded containers + bounds law tiers (check-time literal rejection; runtime hard error) | bug-eater: OOB reads return plausible zeros, no diagnostic; 266 zero-coalesces in gradus, most appeasement not padding | attention/cache/generation passim |
| L8 | Identity/extent arguments threaded by hand (`u32 id` lane params; passing shapes as args) | `@ kernel lane "name"` binding (landed K1); shapes in types | signature lies (unused-but-required params); ABI coupling to hand-threaded identity | GEA1 entries (K2 sweep pending); corpus exemplars |
| L9 | Per-dtype copy-paste types (Bf16View/F32View field-identical classes) | generic `class Box<T>` today; dtype-parameterized carriers when S0-R1 constraints land | edit-one-forget-the-other divergence | kernel.fab views (2 classes; unification gated on receipts + constraints) |
| L10 | Equality-by-field ladders (`eq()` hand-comparing every member; 32 ladders tree-wide) | structural `≡` (EBNF-promised; rust-route derive delivery filed as compiler need 273d2c83) | missed-field comparisons; drift on every new field | prepared_state ×6; 32 across gradus |

## Standing law for new code

1. If a loop exists to visit a container, the container is the loop (`for from … at […]`).
2. If a numeric shape is written in source, it lives in the type or a figura — once, not three times.
3. If a reduction is hand-accumulated, use the reduce.
4. If a wrapper exists to unwrap what a construct already exposes, delete the wrapper.
5. If `coalesce` appears in a loop over known-bounded data, the loop is wrong — not the null.

## Consumers

- faber skill (references/idioms.md): the authoring-side list (B4 lands the L2
  entry; the rest follow as units touch them).
- canonical-faber: review triggers — L1, L2, L3, L4, L6 have pairs or
  one-liners; add the rest as conversions land.
- gradus conversion sweep (next unit): work L1-L7 through the library in
  ranked order (stride/coalesce density), each conversion red-green against
  the library's own checks.

## Out of scope

Python-interop shims; genuine count-like `for range` loops (protocol steps,
repeat-N); padding-semantics coalesces (conv borders, KV tails) — those are
legitimate and the sweep must distinguish, per the bounds-law discussion.
