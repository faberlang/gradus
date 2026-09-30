# PGC-C2 evidence

This directory records the C2 terminal-row-only prefill logits proof.

- `gradus-no-diff.txt` records the required `git diff --exit-code -- src/kernel.fab src/kernel.proba` proof.
- `proba-tuples.json` records the two named case tuples. The packet's current
  unchanged `kernel.proba` stops package analysis at `SEM013` on line 598 before
  the selected case executes. The before/after status and exact stderr bytes
  are retained and byte-identical.
- `proba-before/` and `proba-after/` retain the raw stdout/stderr bytes used by
  the tuple record.
- `parity-raw/`, `parity-receipt.json`, and `baseline-candidate/` retain one
  baseline-grade full-stage paired capture, its reduction, and the append-only
  candidate baseline.
- `terminal-row-delta.json` records the fixed1000 prefill paired wall/throughput
  receipt and the C2 structural delta: row 35, 49,152 logits, 196,608-byte
  one-row readback, and 47,185,920 scalar LM-head FMAs instead of the old
  1,698,693,120 all-row FMAs.

The export and device tests are additive packet files. They pin row 35 as the
terminal view, use the existing decode-shaped `head_rmsnorm` and `lm_head_gemv`
entries, read back exactly 49,152 F32 logits, and compare the observed vector and
argmax to the terminal row of the old full-row fixture.

The full-stage capture intentionally runs the existing shared GEA3 parity
statue. Its receipt still reports the unchanged shared prefill shape
`[36,49152]`; C2-specific wall improvement is not attributed to that receipt.
The terminal-row shape/FMA/readback result is the additive C2 contract proven by
the packet tests, while the paired receipt supplies the required baseline-grade
prefill measurement context.
