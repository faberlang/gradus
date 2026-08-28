# PGC-R4 validation record

All commands from the packet `worktrees/pgc-b2` (branches `factory/pgc-b2`;
radix `80981a08e`, hosts `3a064e3`, gradus evidence-only commit). The
card's measurement commands name the main-checkout evidence path; the
output-dir was pointed at the packet gradus evidence tree (packet-scoped
write law) — same commands, same statue, packet-resident output.

## Radix

- `cargo test -p radix-mir-metal --lib` — 187 passed (incl. the two new
  PGC-R4 emit tests and the retargeted scalar-OOB-tail test).
- `cargo test -p radix-mir --lib kernel_plan` — 89 passed (incl. the two
  new admission tests).
- `cargo test -p mir-emit-harness --lib gea3_pipeline -- --test-threads=1
  --include-ignored` — green except the two pre-existing latent drifts
  R3 already routed to mind (`gea3_pipeline_plan_admission_rejects…`,
  `gea4_admission_derived_gates_fail_closed`) and the env-gated artifact
  tests, which pass when run with their env (below). The
  `gea3_num4_embedding_family…` pitch pin for `prefill_lm_head_gemv`
  stays green (vocab-scale exclusion).
- `GEA3_FIXED1000_ARTIFACT_DIR=<tmp> cargo test -p mir-emit-harness --lib
  gea3_pipeline_test::gea3_pipeline_exports_fixed1000_bundle -- --exact`
  — 1 passed (frozen identities hold under the new emission; the exported
  `prefill_gemm_*.metal` under `recipe-record/` came from this run).
- `GEA3_ARTIFACT_DIR=<tmp> … gea3_pipeline_exports_full_model_bundle` —
  1 passed.

## Proba tuples (before/after)

`faber test src/kernel.proba --name <case> --format json` from the packet
gradus with `FABER_LIBRARY_HOME=<packet root>`; before-binary built at
radix `80981a08e~1` (detached worktree), after-binary at `80981a08e`.
All four cases exit 1 at the pre-existing SEM013 (`kernel.proba:596`);
stdout/stderr/status byte-identical before/after (`proba-before/`,
`proba-after/`).

## Device

- Recipe development probe (`device-ab/`, standalone MSL): the exact
  recipe validated on device across all family shapes plus edge shapes
  (both-tails 36×960×36, single-tile 8×8×8), 3 stable repeat runs; the
  first run exposed and fixed a single-buffered staging race
  (double-buffered now).
- A/B capture (`device-ab/ab.swift`, `ab2.log`): old-recipe MSL (the R3
  evidence export — the frozen scalar emission) vs this branch's export,
  identical seeded inputs → `frozen-tolerance.json` (the class-B frozen
  contract; never widened).
- Hosts physical gate: `GEA3_R4_METAL_SOURCE_DIR=<export>
  GEA3_R4_FROZEN_TOLERANCE=<frozen-tolerance.json> cargo test --release
  -p faber-host-macos-arm64 --test gea3_decode_pgc_r4 -- --ignored
  --nocapture` — 1 passed (tail zero-fill on the M=36/N-multiple edges,
  CPU-reference deltas at or under every frozen bound).
- Hosts structural: `cargo test -p faber-host-macos-arm64 --test
  gea3_decode_pgc_r4` — 2 passed, 1 ignored (the physical gate).

## Parity (card measurement commands)

- `scripta/parity run --stage full --output-dir …/PGC-R4/parity-raw
  --radix-rev 80981a08e --hosts-rev 3a064e3` — EXIT 0, both targets,
  3 runs each, power_class **battery** (29%): faber fixed1000
  natural_completion count 1000 ×3; comparator count 40 ×3 (the known
  tokenizer-divergence law `46ab4e94` posture from the standing
  baseline, unchanged).
- `scripta/parity reduce …/parity-raw --out …/parity-receipt.json` —
  EXIT 0.
- `scripta/parity baseline …/parity-raw --baselines-dir
  …/baseline-candidate --receipt-out …/baseline-candidate.md` — EXIT 0
  (append-only candidate; certification withheld until the AC
  re-capture, mirroring the R3 battery posture).

Wall rows from this capture are battery-throttled and are recorded in
the receipt only — no wall/TFLOP/s claim is made (condition-B rider;
AC re-capture owed, riding the R3 `c2635c71` operator ask).
