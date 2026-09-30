# PGC-A5 AIR census note

The exact `faber check --air --json` invocation exits 0 but emits no JSON
rows for `src/calibration.fab`, the same instrument behavior recorded by
PGC-A2 (src/cache.fab) and PGC-A3 (src/math.fab). The module is an English
source importing the `gradus:dtype` provider; the current single-file AIR
advisory path analyzes an import-free source only and returns no report for
an imported module while ordinary check diagnostics still appear on stderr.
`air-before.json` and `air-after.json` are therefore the exact zero-byte
stdout captures, with the observed stderr byte counts and SHA-256 values
retained in `air-*.rows`. Raw diagnostic streams are kept beside them as
`air-*.stderr` (stderr differs before/after only because the source text and
line numbers changed; check exits 0 with `ok` on both sides).

AIR tier counts are explicitly **not observable**, not zero. No synthetic
tier rows were added; the one-away→admissible clause is therefore not
applicable to this module and that machine result is recorded here. The
loop/intrinsic and WARN027 deltas are recorded in `census-before.rows`,
`census-after.rows`, and `warn027-*.rows`.

WARN027 note: `complexity-*.txt` and `kernel-complexity-*.txt` outputs also
carry LOCALE002/WARN003/WARN024/WARN025 diagnostics from imported
`src/dtype.fab`; dtype.fab is outside the PGC-A5 write scope and contributes
zero WARN027 rows. Calibration-module WARN027 rows are 2 before and 2 after;
both survivors (bake, _validate_corpus) carry in-code keeper reasons.
