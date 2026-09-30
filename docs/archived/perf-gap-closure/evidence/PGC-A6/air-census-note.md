# PGC-A6 AIR census note

The exact `faber check --air --json` invocation exits 0 but emits no JSON
rows for `src/sampling.fab` — the same instrument behavior recorded by
PGC-A2 (cache), PGC-A3 (math), and PGC-A5 (calibration): the single-file
AIR advisory path analyzes an import-free source only and returns no report
for an imported module while ordinary check diagnostics still appear on
stderr. `air-before.json` and `air-after.json` are the exact zero-byte
stdout captures; observed stderr byte counts and SHA-256 values are in
`air-*.rows`, raw streams in `air-*.stderr` (stderr differs only because
source text and line numbers changed; check exits `ok` on both sides).

AIR tier counts are explicitly **not observable** (`not_observable`,
zero-row), not zero. No synthetic tier rows were added; the
one-away-to-admissible clause is therefore not applicable to this module
and that machine result is recorded here. Loop/intrinsic and WARN027
deltas are in `census-before.rows`, `census-after.rows`, and
`warn027-*.rows`. WARN027 in-scope rows: 1 before (`_softmax`,
sampling.fab:438) → 0 after.

The `complexity-*.txt` / `kernel-complexity-*.txt` captures also carry
LOCALE002/WARN003/WARN013 diagnostics and WARN027 rows from imported
modules (dtype, shape, parameter, optimize, train, tensor); those files
are outside the PGC-A6 write scope and contribute zero sampling WARN027
rows.
