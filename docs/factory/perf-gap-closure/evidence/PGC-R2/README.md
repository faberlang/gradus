# PGC-R2 evidence

Final-row-only prefill LM-head contract with all four producer facts explicit
(delivery §7.4, PGC-R2). C2's fold state was verified first; the met facts are
proven from committed receipts/tests, the unmet fact (d) was implemented
in-card.

- `gradus-no-diff.txt` — the required `git diff --exit-code -- src/kernel.fab
  src/kernel.proba` proof (EXIT=0): row selection is view/plan work, no kernel
  body change.
- `producer-facts.json` — the four facts with status, evidence citations, the
  per-fact FMA/readback census, the full producer-chain work-reduction census
  delta (1,731,870,720 → 48,107,520 FMAs; 7,077,888 → 196,608 readback bytes;
  36× each), and the C2 fixture continuity receipt (terminal-row sha256 +
  argmax token 42,424).
- `proba-tuples.json` + `proba-before/` + `proba-after/` — the two named
  cases' `(case_path, status, stderr bytes)` tuples, byte-identical
  before/after (byte-identity class: row selection must not perturb kernel
  numerics; the package still stops at the pre-existing SEM013 at line 598,
  matching the C2 record).

## Fact dispositions

| Fact | Statement | Status |
| --- | --- | --- |
| a | terminal head consumes row 35 through the decode-shaped entry | met — proven from `PGC-C2` receipts/tests |
| b | final-row-only LM-head work 47,185,920 FMAs (not 1,698,693,120) | met — proven from `PGC-C2` receipts/tests |
| c | one-row logits readback 196,608 B (not 7,077,888 B) | met — proven from `PGC-C2` receipts/tests |
| d | prefill head RMSNorm final-row-only `[1,960]` (not `[36,960]` 33,177,600-FMA scan) | **unmet at dispatch — implemented in-card** |

## In-card implementation (fact d)

Additive-only, per the C2 pattern (no shared `gea3_pipeline_test.rs` /
`gea3_decode.rs` edits, no kernel-body source change):

- `radix/crates/mir-emit-harness/src/gea3_pipeline_pgc_r2_test.rs` — head-norm
  row-selection view pin (row 35, one 3,840-byte hidden span, distinct row
  markers so row 34/0 fail), head-norm FMA census (921,600 final-row vs
  33,177,600 full-row, 36×), chained norm→GEMV census (48,107,520 total
  final-row FMAs vs 1,731,870,720 all-row), and the decode-shaped
  `head_rmsnorm` export pin (one-row output, no `tf32[36,960]`, workgroup 1).
- `hosts/macos-arm64/tests/gea3_decode_pgc_r2.rs` — `head_rmsnorm`
  terminal-row binding over the `[36,960]` activation (byte-exact row-35
  readback via the `observa` primitive) and the full head chain
  (`head_rmsnorm` row-35 → `lm_head_gemv` one-row) with a 196,608-byte
  one-vocab-row readback selecting the same next token (42,424) as the C2
  pre-fold fixture, byte-for-byte.

Condition-B rider honored: no wall claim; the FMA/readback census deltas are
this card's primary evidence.
