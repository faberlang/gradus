# PGC-R5 resume-gate landing — option (b) NVVM row-mapping (receipt)

Landing date: 2026-08-28. Unit: task `160d6429` (hand, packet
`worktrees/pgc-r5`, branch `factory/pgc-r5`). Authority: delivery card
§7.4 `PGC-R5` as amended by §7.7 (ruling `dce2a356`; head-cto `190e7520`,
posture `correct_before_resume`); CTO-B `a694cd2b` finding 4.

This receipt records the §7.7 resume-condition proofs landed with the
NVVM consumer. It is NOT the R5 closeout receipt: the device/evidence
stage (hosts `gea3_decode_pgc_r5.rs`, the fixed-1000 paired-parity
capture, FMA/iteration census) remains open R5 scope, and every wall /
certification claim stays WITHHELD pending AC (condition-B rider,
burgus on battery).

## Resume condition 1 — bag names option (b) and the NVVM consumer

Satisfied by amendment §7.7 itself (planner, task `443d2c25`). This
landing implements it:

- `radix/crates/radix-mir-llvm/src/nvvm/recipe.rs` — the row-mapping
  bodies, selected by `Some(RowReduction)` for `TensorRmsNorm`,
  `TensorCausalMaskedSoftmax`, and the additive-mask `TensorSoftmax`
  idiom (the GEA2-U5e `(scores + causal_mask).softmax()` surface):
  one 32-lane workgroup per row (`ctaid.x` owns the row, `tid.x` is
  the lane), lanes striding the row, one warp `shfl.sync.down.f32`
  butterfly per row statistic (register-only, full-warp membermask),
  and a strided scale/output pass over the same row. RMSNorm keeps
  `llvm.sqrt.f32` + plain `fdiv` (the pinned clang 18.1.3 NVPTX law);
  the causal softmax keeps the INLINE exp sequence (C7).
- `radix/crates/radix-mir-llvm/src/nvvm_descriptor.rs` — the matching
  signature route: the `RowReduction` contract flows through the shared
  `contract_shape_signature` arm (workgroup `(32,1,1)`, dispatch
  `rows × 32` threads under the 1D thread law). The earlier
  reset-to-1D interception at this seam — the retired containment
  attempt — is deleted.

Never-elsewhere law (fail-closed selection): a resolved
`Some(RowReduction)` contract emits the row body or fails closed with a
named diagnostic (geometry/admission disagreement). A `(1,1,1)`
signature under a resolved contract is the mixed-subchain union
dispatch and keeps the frozen per-element body — the correct body for
that 1D launch. A rows-x-32 grid can never reach a per-element body.

## Resume condition 2 — fail-closed proof: no RowReduction signature
reaches an old per-element body

Focused proofs (all in `radix/crates/mir-emit-harness/src/
gea3_pipeline_pgc_r5_test.rs` unless noted):

- NVVM consumes: `pgc_r5_nvvm_consumes_row_reduction_with_row_mapping_body`
  — the admitted `[36,960]` rmsnorm kernel emits the row body
  (`ctaid`-mapped row, exactly one strided squared-values scan, one
  5-fold warp butterfly) and the frozen per-element mapping
  (`%faber.rn.outer`, `udiv i32 %faber.index, 960`) is ABSENT.
- NVVM fallback law: `pgc_r5_nvvm_non_admitted_shape_keeps_frozen_per_element_body`
  (`[2,8]` keeps the frozen body, no warp collective) and
  `pgc_r5_nvvm_causal_softmax_row_body_and_decode_twin` (the `[36,36]`
  additive idiom takes the row body with the per-element body absent;
  the decode `[1,76]` twin keeps the frozen body — B1/B2-landed).
- WGSL stays unadmitted:
  `pgc_r5_wgsl_rejects_the_row_reduction_family` — the WGSL probe has
  no emit arm for the family and rejects the compile (per-op gate),
  so no `RowReduction` launch signature ships on the WGSL lane. Shared
  synthesis applying the contract backend-blind is not containment,
  and none of it is produced.
- Metal consumes (prior WIP, adopted): the Metal row bodies in
  `emit/rmsnorm.rs` / `emit/causal_softmax.rs` / `emit/rowsoftmax.rs`
  with the same admission + geometry cross-check, proven by
  `metal_emits_rms_norm_affine_structure`,
  `metal_rms_norm_non_admitted_shape_keeps_per_element_body`,
  `metal_causal_softmax_row_reduction_structure_admitted_shape`, and
  the harness tests `pgc_r5_rmsnorm_family_emits_the_row_reduction_recipe`,
  `pgc_r5_prefill_causal_softmax_emits_the_row_reduction_recipe`,
  `pgc_r5_decode_masked_softmax_keeps_the_frozen_body`.

## Resume condition 3 — Class B unchanged; barrier/masking proofs

- Class B stands for all three entries (threadgroup/warp reduction
  changes summation order): no tolerance was widened; no byte-identity
  claim was made anywhere in this landing. The frozen per-family
  tolerance mint remains the R5 implementation phase
  (`pgc-r4-frozen-tolerance-v1` schema). The f32 sanity
  `pgc_r5_rmsnorm_row_reduction_stays_inside_f32_contract` checks
  constant / mixed-sign / near-epsilon rows against the declared f32
  contract under the emitted lane-strided + tree order.
- Barrier law (per the `190e7520` sketch "no lane crosses a barrier
  conditionally"): the Metal bodies use threadgroup tree reductions
  with one barrier per halving step reached by every lane and no OOB
  early-return guard (`!msl.contains("if (id")`); the NVVM bodies are
  REGISTER-ONLY — the cooperative reduction is the warp shuffle
  butterfly with the full membermask, so there is no barrier to cross
  at all, and the entry guard's limit equals the dispatched thread
  count (rows × 32), so every lane enters the body and reaches the
  collective uniformly.
  Proofs: `pgc_r5_nvvm_row_body_barrier_and_masking_laws` plus the
  Metal structural tests above.
- Masking law: RMSNorm covers the FULL row width including 960-wide
  rows (the scan bound is the full width on both lanes); the causal
  softmax excludes masked future columns from max/sum AND from the
  output (`min(row + 1, cols)` unmasked extent; both statistics bound
  their scans by it; the scale pass writes `0.0` above it; no masked
  column feeds an exp — the guard precedes the read).

## Dirty-WIP classification (required by §7.7 "classify before building")

The packet's interrupted prior-R5 attempt (radix only; gradus/hosts
clean):

- ADOPTED (matches option (b)): the RowReduction contract
  (`abi/contract.rs`), admission facts + `kernel_plan` arms, the
  `contract_shape_signature` / transformer-subchain signature routes
  (`device_program_plans.rs`), the Metal row bodies + emit tests, the
  harness launch pins, and the R5 harness test file.
- REPAIRED (interrupted-write artifacts, not design): `abi/contract.rs`
  was corrupted by an interleaved duplicate write (the file carried a
  truncated first copy plus two overlapping copies of the body);
  reconstructed to the single intended content (HEAD + the R5
  additions), one residual type error and three dead wildcard arms
  fixed, one empty `if` debris removed.
- REPLACED (retired mechanism): the `nvvm_descriptor.rs` reset-to-1D
  interception — the pre-amendment containment attempt at the
  WGSL-shared seam. Option (b) supersedes it (see condition 1).
- NOT PRESENT in the WIP (landed by this unit): the entire NVVM
  consumer (`nvvm/recipe.rs` row bodies) and the fail-closed /
  barrier / masking proofs above.

## Shared-layer repairs the NVVM consumer required (all in card scope)

The WIP had not yet driven the device-program lane green; three
shared-layer gaps surfaced under the focused proofs and were fixed in
card-scope files:

- `kernel_plan/build.rs` — `transformer_operand_dims` is now
  temp-aware: the additive-idiom softmax's `(x + mask)` elementwise
  temp has its type in the temps table, invisible to the local-only
  lookup (the plan pass failed closed with "no resolvable shape
  facts"). Mirrors the contract resolver's temp lookup.
- `abi/contract.rs` — `stability_max_is_dead` published, and applied
  by the plan / subchain scans in `device_program_plans.rs`: a DEAD
  `_stability_max` reduction is not a recipe (the same dead skip the
  contract resolver applies), so a decomposition slice whose only
  recipe is a dead stability max no longer fails closed demanding a
  dispatch contract for it.
- `device_program_plans.rs` — `validate_per_output_domains` now
  counts the row-reduction launch's COLLECTIVE coverage (one
  `ROW_REDUCTION_WORKGROUP_X`-lane workgroup owns one full row: work-
  groups × row width for `RmsNormalization` / `CausalMaskedSoftmax`,
  the row-partitioned output extent for the `RowSoftmax` idiom twin);
  the per-thread under-coverage oracle does not apply to a collective
  launch (the tiled-matmul over-cover class is the precedent), and an
  under-rowed launch still fails closed.

## Pin regeneration (§7.5 route, constraint 4) and test-scope notes

- The dead-skip legitimately changes the GEA2 `causal_softmax` [8,8]
  entry's ABI facts: pre-R5 the dead stability-max reduction drove a
  64-lane reduction launch with a 1-element output view; the entry now
  records the softmax's own generic 1D contract (workgroup (1,1,1),
  dispatch 64, full 64-element output view). The GEA2-U4b spec row and
  its geometry-proof comment were regenerated in
  `gea2_pipeline_test.rs` — the body is UNCHANGED (the GEA2-U5e
  structural causal softmax; the mask operand is identity data and
  never bound a buffer, pre- or post-R5).
- `radix-mir-llvm/tests/device_artifact.rs` (outside the card's named
  LLVM write scope) carries two GI3-4 rmsnorm pins whose [2,960]
  fixture now ADMITS the row reduction by design: the pins were
  updated to the row body's markers (`%faber.rr.*`, one strided scan,
  warp butterfly), and the no-libcall checker now admits inline PTX
  (`call … asm sideeffect`, the SFR-7 redux precedent — inline PTX is
  not a libcall). Declared here as a scope deviation: leaving the
  pins red would hand the merge lane a repair (the R4 gate lesson).
- Environment notes, not regressions: the unfiltered harness run's
  10 remaining failures are pre-existing at the lane base (9 export
  tests gated on `GEA*_ARTIFACT_DIR`, 1 corpus exemplum semantic
  error); the plain-lib doc-test pass has been broken at the base
  (`llvm_text_test` lacks the `#[cfg(test)]` gate); every clippy trip
  is the two pre-existing `radix-types/src/capability.rs` pedantic
  findings in an untouched crate.

## Disposition

Resume conditions 1–3 are landed with focused proofs; the
`RowReduction` contract is consumed by Metal and NVVM and rejected by
WGSL. R5 implementation (device test, parity/evidence stage) may
resume on this base. do_not held: no backend-blind admission const was
added; no rows-x-32 grid reaches a per-element body on any lane.
