# PGC-A2 AIR census note

The exact `faber check --air --json` invocation exits 0 but emits no JSON rows
for `src/cache.fab`. The module is an English source with imported
`gradus:dtype` and `gradus:tensor` providers. The current single-file AIR
advisory path analyzes an import-free source only; its internal analysis
returns no report for an imported module while ordinary check diagnostics still
appear on stderr. `air-before.json` and `air-after.json` therefore contain the
exact zero-byte stdout captures. The observed stderr byte counts and SHA-256
values are retained in `air-*.rows`; raw diagnostic streams are not duplicated
beside the required named stdout captures.

AIR tier counts are explicitly **not observable**, not zero. No synthetic tier
rows were added. The loop/intrinsic and WARN027 deltas are recorded in
`census-before.rows`, `census-after.rows`, and `warn027-*.rows`.
