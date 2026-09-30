# PGC-A3 AIR census note

The exact `faber check --air --json` invocation exits 0 but emits no JSON rows
for `src/math.fab`, the same instrument behavior recorded by PGC-A2 for
`src/cache.fab`. The module is an English source importing `gradus:dtype`,
`gradus:shape`, and `gradus:tensor` providers; the current single-file AIR
advisory path analyzes an import-free source only and returns no report for an
imported module while ordinary check diagnostics still appear on stderr.
`air-before.json` and `air-after.json` are therefore the exact zero-byte
stdout captures, with the observed stderr byte counts and SHA-256 values
retained in `air-*.rows`. Raw diagnostic streams are kept beside them as
`air-*.stderr`.

AIR tier counts are explicitly **not observable**, not zero. No synthetic tier
rows were added. The loop/intrinsic and WARN027 deltas are recorded in
`census-before.rows`, `census-after.rows`, and `warn027-*.rows`.

WARN027 note: `complexity-before.txt` and `complexity-after.txt` (and the
kernel-budget twins) each carry two additional WARN027 rows in imported
`src/shape.fab` (lines 158/203). `shape.fab` is outside the PGC-A3 write
scope and those rows are unchanged before/after; they are excluded from the
card's math-module WARN027 counts, which drop 4 → 2 with both survivors
(matmul, concatenate) carrying in-code convert-or-record reasons.
