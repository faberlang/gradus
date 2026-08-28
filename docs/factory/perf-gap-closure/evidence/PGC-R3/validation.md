# PGC-R3 validation record

## Commands (exact)

- Re-key: edits in radix `c34b3976a` (two target tomls + `gea3_pipeline_test.rs`
  kv_append identities) and hosts `007ba2a` (Gather mirror + compact ids binding).
- Family capture (battery — AC re-run owed):
  `./scripta/parity run --stage full --output-dir …/evidence/PGC-R3/parity-raw` → 6 paired rows,
  faber certified 1000/1000 ×3 (fixed1000) and 8/8 ×3 (short), all natural completion.
- Reduce: `./scripta/parity reduce …/parity-raw --out …/parity-receipt.json` (power_class battery).
- Baseline append: **withheld** pending the AC capture (a battery family would mis-key every later delta).
- Pipeline re-verification (radix, env GEA3_*_ARTIFACT_DIR set to exported bundles):
  `cargo test -p mir-emit-harness --lib gea3_pipeline -- --test-threads=1 --include-ignored`
  → green except two latent drifts (see census.md §re-verification; findings to mind).
- Hosts family: `cargo test -p faber-host-macos-arm64 --release --test gea3_decode_pgc_{b2,b3,c2,c5,r1,r2}`
  with GEA3_ARTIFACT_DIR = the R3 fixed1000 family bundle → all green.
- B1 physical gate: `cargo test --release --test gea3_decode_pgc_b1` with
  GEA3_PGC_B1_ARTIFACT_DIR (early/late buckets, capacity 1100) → green; certified-join
  Faber-side facts verified (comparator-line assertion unmeetable, finding filed).

## Environment

burgus.local, Apple M5 Max; battery power at capture time (57%→~30%);
comparator llama-cli b10290-c8e03ce81; on-device Metal arms only, MIR runner excluded.
