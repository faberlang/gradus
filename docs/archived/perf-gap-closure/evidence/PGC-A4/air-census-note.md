# PGC-A4 AIR census note

The exact `faber check --air --json` invocation exits 0 but emits no JSON rows
for `src/block_verify.fab`, the same instrument behavior recorded by PGC-A2
(`src/cache.fab`) and PGC-A3 (`src/math.fab`). The module is an English source
importing `gradus:cache`, `gradus:cache_branch`, `gradus:attention`,
`gradus:dtype`, `gradus:model/dense`, `gradus:speculative`, and
`gradus:tensor` providers; the current single-file AIR advisory path analyzes
an import-free source only and returns no report for an imported module while
ordinary check diagnostics still appear on stderr. `air-before.json` and
`air-after.json` are therefore the exact zero-byte stdout captures, with the
observed stderr byte counts and SHA-256 values retained in `air-*.rows`. Raw
diagnostic streams are kept beside them as `air-*.stderr`.

AIR tier counts are explicitly **not observable**, not zero. No synthetic tier
rows were added. The loop/intrinsic and WARN027 deltas are recorded in
`census-before.rows`, `census-after.rows`, and `warn027-*.rows`.

WARN027 note: `complexity-before.txt` / `complexity-after.txt` (and the
kernel-budget twins) carry additional WARN027 rows in imported modules
(attention, cache, cache_branch, decode, generation, gguf_manifest, math,
model/dense, nn, optimize, parameter, sampling, shape, tokenizer, train).
Those files are outside the PGC-A4 write scope and their rows are unchanged
before/after; the card's block_verify-module counts stay 6 → 6, with all six
survivors carrying in-code convert-or-record reasons (see
`warn027-after.rows`). The three conversions (min-scan → `.reduce` with `⤓`,
all-finite check → `.filter` count form, history string fold → `.reduce`) did
not move any function below the complexity budget — the six warned functions
are dominated by their require/match admission chains, not by the converted
loops. The LSR-W0 argmax-twin form in `_greedy_targets` (gradus fold
`87888b2`) is preserved untouched as the model form.
