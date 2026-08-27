# PGC-B2 evidence record — T=1 one-row GEMV dispatch

## Mechanism (smallest that changes the dispatch shape)

No new `CollectionKernelPlan` variant. The one-row fact is typed by the
plan's own `m == 1`:

- `radix-mir-metal/src/lib.rs` — `apply_one_row_matmul_dispatch` beside the
  existing `apply_static_gemv_dispatch` precedent (called by both the
  canonical probe and the launch-variant seam in `launch_bindings.rs`):
  a dense M=1 matmul (literal left rows == 1, K > 1, N > 1) carries
  workgroup `(8, 1, 1)`; the tile grid `(ceil(N/8), 1, 1)` is unchanged.
- `emit/recipes.rs` — mirrors the launch fact onto the resolved
  `MatMulPlan` (`workgroup_y = 1`) and re-validates through the plan law.
- `kernel_plan/validate.rs` — the T=1 one-row exception to the
  workgroup==tile law (`m == 1` admits `(tile, 1)`; x must equal tile).
- `emit/matmul.rs` — the one-row B-tile load: each x lane loads its whole
  column strip (`gemv_ty` loop); A load, inner product, barriers, and the
  guarded write are unchanged (`ty`/`row` degenerate to 0).
- abi `contract.rs` / `resource.rs` / `device_program/types.rs` — no edit
  needed: the tile-grid dispatch and the verbatim matmul workgroup-count
  rule already carry the new shape once the signature carries it.
- `abi/contract.rs`, `resource.rs`, `types.rs` were read and proven
  no-fact-changed (the preflight option the wave law allows).

Mechanism-forced consequences outside the named entry list (each named
per the amended card's instruction):

- `gea3_pipeline_test.rs` embedding-gather T=1 pin region
  (`gea3_embedding_gather_t1_launch_matches_tiled_msl_geometry`, the
  `T=1 pinned` tile-law row, and the embedding body-text pin in
  `gea3_num4_embedding_family_pitches_the_tied_matrix_by_entry`): the
  decode embedding gather is itself an M=1 dense matmul
  (`[1,49152]·[49152,960]`), structurally indistinguishable from the
  named GEMVs, so the one-row law reaches it; its pins now carry
  `(8, 1, 1)`.
- `radix-mir-metal/src/launch_bindings.rs` — one call line
  (`apply_one_row_matmul_dispatch`) beside the existing
  `apply_static_gemv_dispatch` call: the launch-variant seam derives its
  own signature, so the one-row fact must be applied there too or the
  derived-geometry law reports plan/emitted drift.
- `radix-mir-metal/src/lib.rs` — the helper itself plus one call line in
  the canonical probe loop (direct sibling of the existing
  `apply_static_gemv_dispatch`).
- `mir-emit-harness/src/lib.rs` — the additive
  `gea3_pipeline_pgc_b2_test` module gate (the c2/c5 precedent).

## Proba tuple oracle

Isolated package (the PGC-B3 precedent — the full `src/kernel.proba`
package stays blocked by the pre-existing SEM013 at line 598): the seven
named cases extracted verbatim into `proba-oracle/pgc_b2.proba.extract`.
Before/after `faber test --format json` runs with the packet-built binary
are byte-identical (`proba-oracle/proba-{before,after}.stdout.json`,
3044 bytes each; per-case `(path, status=failed, reason="runner refuses
execution of @ kernel function")` unchanged; run stderr empty both sides).

## Row-work / FMA census (exported decode step)

From the exported `gea3-program-plan.json` (1186 T=1 launches per decode
step): useful FMA 413,614,080; dispatched FMA after 413,736,960 (column
padding only); dispatched FMA before (workgroup y = 8) 3,308,895,680
— a 87.5% (7/8) reduction in dispatched row work, the card's expected
effect. The hosts additive census test pins the same law per launch.

## Full-stage paired parity (the one baseline-grade capture)

`scripta/parity run --stage full --radix-rev 8111e4f2f --hosts-rev 9b7e4fb`
(2 targets × 3 paired runs, power class ac, all runs
`natural_completion`, fixed-1000 certified 1000/1000 gradus output):

- metal-m5max-fixed1000 decode: standing baseline median 15.77 t/s
  (~63.4 ms/step) → candidate median 6.96 t/s (~143.6 ms/step).
- metal-m5max decode: standing baseline 31.65 t/s → candidate 17.87 t/s.
- prefill unchanged within noise (536–570 t/s band both sides).

**The hypothesis is falsified on the wall: removing 7/8 of the dispatched
row FMA work regressed decode wall ~2.3×.** The `(8, 1)` threadgroup
drops from 64 to 8 threads per workgroup; the M5 Max loses latency
hiding/occupancy faster than it gains useful-FMA share, and the per-thread
serial strip load dominates. Per the wave law this is honest evidence,
not permission to pull another lever (a wider one-row threadgroup, e.g.
`(64, 1)` with eight column tiles per workgroup, is a follow-up lever the
Mind may card separately). The dispatch-shape done_when is met; the wall
verdict belongs to the Mind.

## Validation summary

- `cargo test -p radix-mir --lib` 674 passed (new T=1 law test included).
- `cargo test -p radix-mir-metal` 182 passed.
- `cargo test -p mir-emit-harness --lib` 769 passed; only the 9
  pre-existing env-gated failures (artifact-export and llvm gates) remain,
  identical to the pre-change baseline in this packet.
- hosts: `gea3_decode_pgc_b2` 3 passed; shared `gea3_decode` 7 passed
  against the new export; the one `dtype_surface_consistency_test` failure
  reproduces identically on main hosts + main radix (pre-existing F2
  placement-debt, unrelated).
