# PGC-B1 owed evidence — discharged by PGC-R3 (audit-debt 77ca6b07)

## Physical gate (RAN, on device)

`cargo test -p faber-host-macos-arm64 --release --test gea3_decode_pgc_b1`
with `GEA3_PGC_B1_ARTIFACT_DIR` = the exported early/late bundles:

- `gea3_decode_pgc_b1_dispatches_early_and_late_work_buckets` — **green**:
  both bucket extents at allocation capacity 1100; early and late buckets each
  dispatch ENTRIES × 1000 steps.

## Certified-join gate

- Faber receipt (R3 family capture, run-001 fixed1000): status green,
  n_predict 1000, l_max 1100, step_count 1000, steps = 1001 (prefill + 1000) —
  all assertions pass.
- Comparator assertion (`eval time … / 1000 tokens`) is **unmeetable as
  written**: the pinned comparator naturally completes at 40 tokens (greedy
  EOS) in every recorded family capture, including the standing AC baseline
  (comparator certified_count 40 ×3). The count law (46ab4e94) pins counts
  per side independently; the gate text contradicts the family record.
  Finding filed to mind (gate repair belongs to a lint/hand lane).

## B1 delta (derived from the R3 family capture)

Attention-family work extents follow the declared bucket, not capacity:
fixed1000 export carries decode score/context GEMMs at n=1088 (34-bucket × 32)
with the w16 one-row workgroup (grid 68) — the B1 bucketed-extent fold plus
the B2-RETUNE KEEP-w16 posture are both present in the re-keyed family.
Wall deltas are withheld (battery capture; condition-B: census deltas
primary, wall L1-gated).
