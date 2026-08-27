# PGC-C2 evidence

This directory records the C2 terminal-row-only prefill logits proof.

- `gradus-no-diff.txt` records the required `git diff --exit-code -- src/kernel.fab src/kernel.proba` proof.
- `proba-tuples.json` records the two named case tuples. The packet's current
  unchanged `kernel.proba` stops package analysis at `SEM013` on line 598 before
  the selected case executes. The before/after status and exact stderr bytes
  are retained and byte-identical.
- `proba-before/` and `proba-after/` retain the raw stdout/stderr bytes used by
  the tuple record.
- `parity-raw/`, `parity-receipt.json`, and `baseline-candidate/` are the
  baseline-grade paired-parity artifacts. The full-stage run is required before
  this directory can claim a measured C2 delta.

The export and device tests are additive packet files. They pin row 35 as the
terminal view, use the existing decode-shaped `head_rmsnorm` and `lm_head_gemv`
entries, read back exactly 49,152 F32 logits, and compare the observed vector and
argmax to the terminal row of the old full-row fixture.
