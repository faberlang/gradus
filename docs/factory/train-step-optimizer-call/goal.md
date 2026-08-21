# GOAL: train-step-optimizer-call — delegate `train_step_*` to the optimizer now that library-to-library calls execute

**Status**: planned — verified against live code 2026-08-21; pre-implementation, ready for `$delivery` lowering
**Created**: 2026-08-21
**Campaign:** `—` (standalone)
**Source:** operator verification request (session 2026-08-21). A documentation session claimed "the compiler cannot yet resolve library-to-library calls, so `train_step_*` carries the update math inline rather than calling the optimizer." Verification found the workaround real but its justification **stale**: the runtime gap closed in radix on 2026-08-09 and the revisit trigger this repo recorded ("revisit when that runtime gap closes") fired without anyone revisiting.
**Repos:**
- primary: `gradus/` — `src/train.fab`, `src/optimize.fab`, `src/model/`, `src/*.proba` headers, `README.md`, `exempla/training-loop-mlp/`
- evidence only (no writes): `radix/`

**Related:**

| Artifact | Relationship |
| --- | --- |
| `radix/docs/factory/faber-test-reliability/goal.md` | Owns the `faber test` routing/reporting surface this goal's executed-proba validation rides on; units 7–11 pending there |
| `radix` `43c0102ba` (LIB-MIR, 2026-08-09) + `2e8042ae7` (regression tests, 2026-08-11) | The fix that closed the gap; nothing for this goal to do in radix |
| `radix/crates/radix-program/src/mir/lane_test.rs` (`package_mir_training_loop_mlp_runs_on_fmir_lane`) | Pinned executable proof that gradus multi-module library-to-library calls run; must stay green |
| `docs/factory/production-ml-library/pml0-proof-api-ledger.md` rows 10–11 | The `sgd_step_2x2/_4x4` retirement this goal revisits (retired for the toolchain gap, not for design) |
| `docs/archived/` (gpu-training-lowering stage-4 receipt) | Historical record of the original gap; stays historical |

---

## Invariant

Gradus tells the truth about runtime capability and keeps one copy of the SGD
update math: library-to-library calls execute on the FMIR stepper, so
`train_step_*` delegates to the optimizer surface instead of carrying inlined
duplicates, and no live source or doc claims the closed gap still exists.

## Problem

All evidence observed live on 2026-08-21 with `radix/target/debug/faber`
built from radix HEAD.

| # | Probe | Observed |
| --- | --- | --- |
| E1 | The claim's origin | `README.md` (added `cd3883d`, 2026-08-04): "The compiler cannot yet resolve library-to-library calls, so `train_step_*` currently carries the update math inline rather than calling the optimizer; revisit when that runtime gap closes." |
| E2 | Gap closed upstream | Radix `43c0102ba` "LIB-MIR — register textus.accipe intrinsic + SizedNumeric zero-init arm" (2026-08-09); lane test comment: "the FMIR runner now lowers library-to-library calls in the gradus multi-module library"; regression-locked by `2e8042ae7` (2026-08-11). |
| E3 | Pinned proof green | `cargo test -p radix-program package_mir_training_loop_mlp_runs_on_fmir_lane` → **ok** (this session, 8.2s). |
| E4 | CLI execution proof | `faber run gradus/exempla/training-loop-mlp/src/main.fab` executes the full 100-step loop through `optimize.step` (which calls `parameter.mutate`, `gradient.obsolete`, `dtype.finite` — all library-to-library); final loss `0.017928625511508454` and the sampled trajectory match the pinned f64 oracle exactly. |
| E5 | Workaround still live | `src/train.fab:69–105` (`train_step_2x2/_4x4`) and `:123–160` (`train_step_bert_*` + `_sgd_family`) inline `param − lr·grad`; the same element math exists a third time in `optimize.step` (`src/optimize.fab:440–465`). The KNOWN TOOLCHAIN CONSTRAINT header (train.fab:38–46) cites the closed gap. |
| E6 | Stale claims tree-wide | ~20 live files carry "env-blocked tree-wide today (FMIR stepper / library-import gap)" headers: `src/{train,optimize,loss,metrics,generation,decode,gradus}.fab`, `src/{train,optimize,gradient,nn,metrics,loss,transformer,sampling,math}.proba`, README. Also stale: the `exempla/training-loop-mlp/src/main.fab` header ("NO executed convergence is claimed") contradicts E4. |
| E7 | Package analysis broken (separate defect) | `faber check`/`faber test` package route in gradus fails on real SEM errors in fresh model modules: `src/model/gguf.proba:5493` (`s ↦ number` → SEM001/SEM008) and `src/model/qwen35moe.fab:43773` (`corpus.identity.algorithm` → SEM004). No live consumer imports them (the exemplum's transitive analysis passes), but they block `faber check .` / `faber test` on this repo. |
| E8 | Adjacent run-route defect (residual, not this goal) | `exempla/gradient-seam`: `faber check` → ok, `faber run` → ~21 bare "call argument type mismatch" errors with no file/line. Also `faber run`/`check` with a relative path from a manifest cwd reads an empty path. Both belong to the faber-test-reliability surface; recorded here so they are not lost. |

**Net:** the claim's second half (inline math) is true; its first half (the
compiler limitation) has been false for 12 days. The recorded revisit trigger
fired silently. The fix is gradus-side: delegate, then tell the truth in
source and docs.

## Proposal

1. **Restore a callable tensor-level optimizer step** in `gradus:optimize`
   (default: the retired-ledger shapes `sgd_step_2x2`/`sgd_step_4x4`,
   `param − lr·grad` over tensors; see Q1) with co-located proba.
2. **Delegate:** `train_step_2x2`/`train_step_4x4` and the `train_step_bert_*`
   pair call the optimizer surface instead of inlining; `_sgd_family` moves
   behind (or into) the optimizer. Public signatures and the admitted caller
   surface (`examples/training/*`) stay unchanged.
3. **Executed evidence:** the training-loop exemplum (and, once E7 is fixed,
   the train/optimize proba suites) runs on the FMIR stepper — executed
   values, not compile-only claims.
4. **Truth pass:** replace the stale constraint claims (E6) with the current
   capability statement; record the ledger reversal note for rows 10–11.
5. **Repair the package analysis errors** (E7, two observed sites) so
   `faber check .` in gradus is green and usable as this goal's validation.

### Non-goals

- No radix changes — the runtime capability is proven and regression-locked;
  E8's run-route defects route to `faber-test-reliability` follow-ups.
- No public `train_step_*` signature changes; no caller migrations in
  `examples/`.
- No GPU/device/backend work; no optimizer-algorithm work beyond SGD.
- No edits to `docs/archived/` — historical records stay as written.

## Units (lowering sketch — refine via `$delivery`)

| Unit | Scope | Depends on | Hand evidence |
| --- | --- | --- | --- |
| 1 | Tensor-level `sgd_step_*` restored in `src/optimize.fab` + proba; PML0 ledger rows 10–11 reversal note | — | none |
| 2 | `train_step_*` delegates; inline math + `_sgd_family` duplication deleted from `src/train.fab` | 1 | none |
| 3 | E7 repair: `src/model/gguf.proba:5493`, `src/model/qwen35moe.fab:43773`; `faber check .` green in gradus | — | none |
| 4 | Executed evidence: training-loop exemplum runs and matches the PML4 pins through the delegation path; train/optimize proba executed via `faber test` once 3 lands | 2, 3 | none |
| 5 | Truth pass over E6 file list + README + exemplum header | 2, 4 | none |

Red-green expectation: unit 1 proba fail first (symbols absent), then pass;
unit 4 pins the executed trajectory before and after delegation (values must
not move).

## Validation

- `faber check .` in `gradus/` → green (E7 repaired)
- `faber run gradus/exempla/training-loop-mlp/src/main.fab` → final loss
  `0.017928625511508454`, sampled trajectory matches pins, through the
  delegating steppers
- `faber test` scoped to the train/optimize suites → executed cases pass
- `cd radix && cargo test -p radix-program package_mir_training_loop_mlp_runs_on_fmir_lane` → stays green (guard, no radix edits)
- `rg -n "cannot yet resolve library-to-library|env-blocked tree-wide today" gradus --glob '!docs/archived/**'` → no live hits

## Ledger

| Unit | Status | Seat | Receipt | Notes |
| --- | --- | --- | --- | --- |
| 1 | pending | — | — | — |
| 2 | pending | — | — | — |
| 3 | pending | — | — | — |
| 4 | pending | — | — | — |
| 5 | pending | — | — | — |

## Open questions

1. **Optimizer surface shape** — default: restore tensor-level
   `sgd_step_2x2`/`sgd_step_4x4` under `gradus:optimize` (retired-ledger
   shapes, per-tensor in/out) so delegation is a drop-in. Alternative:
   express the steppers on the state contract (`Parameter`/`Gradient`/
   `SgdState` via `optimize.step`) — richer semantics but changes the
   admitted caller surface; reject unless the operator wants that migration.
2. **`_sgd_family` placement** — default: the shape-generic helper lives in
   `gradus:optimize` and both the fixed-shape steppers and the BERT pair
   delegate through it. Alternative: keep per-shape calls only (simpler
   calls, one more copy).
3. **E8 disposition** — default: file as named residuals against
   `faber-test-reliability` follow-ups (check-vs-run divergence on
   gradient-seam; relative-path reads from a manifest cwd). Not this goal's
   scope.

---

<!-- Created from radix/docs/factory/TEMPLATE.md. Status line is the audit
     authority; ledger phase table drives completion %. -->
