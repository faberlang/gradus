# PML3 Closeout Note — phase gate MET (forward composability + autograd independence + oracle matching)

**Unit**: PML3 phase closeout (campaign gate; PML4 next)
**Date**: 2026-08-09
**Predecessor**: PML3-U1..U5 all landed and admitted by Mind — U1 9822cfa (NN
primitives), U2 5260049 (attention), U3 7bf9acc (transformer block),
U4 359c5f0 (facade — forward with and without autograd), U5 92df3ff (support
rows). Delivery: `pml3-delivery.md`; support rows:
`pml0-support-matrix.md` (PML0-U5 schema v0.1.0).
**Repo**: gradus.

## Outcome: phase gate **MET** — PML3 delivered

The PML3 phase gate (`pml3-delivery.md` §Phase gate, campaign PML3 §Gate) is
satisfied. PML4 is the next phase; the phase intent "PML3 must not require
PML4" is held — no PML3 unit depends on training machinery (see checklist).

## Phase-gate checklist

| Gate clause | Evidence | Verdict |
| --- | --- | --- |
| Forward functions composable | `src/nn.fab` (U1 9822cfa), `src/attention.fab` (U2 5260049), `src/transformer.fab` (U3 7bf9acc), `src/gradus.fab` facade (U4 359c5f0) compose as linear/gelu/layernorm → attention (causal + RoPE) → transformer block; the shared layer is the `gradus.fab` facade per PML0-U4 | **MET** |
| Autograd-independent | Forward functions are pure value functions; `gradus.fab` imports no autograd surface; the training path requests gradient construction solely via the single `@ radix backward` annotation. `check-compile` (faber check) proves the import DAG has no autograd dependency in the forward path | **MET** (structural proof) |
| Oracle-matching | Pinned f64 CPU-reference oracle values: `src/nn.proba`, `src/attention.proba` (COS_1/SIN_1), `src/transformer.proba` (LN3_*/IN_LN3_*), `src/gradus.proba` (forward_mlp) within the documented 5e-4 absolute tolerance; independent external-Python f64 evaluation of the documented formulas reproduces the pins | **MET** |
| U4 partial note (CTO Q2) | Runtime identity of bare forward vs the generated backward companion is **NOT claimed**: selected training/proba paths now execute on the FMIR stepper, but this row has no executed identity or numerical-bound-at-runtime evidence for the generated backward companion. Deferred to a runtime-evidence gate — recorded as residual #2 below | **PARTIAL — recorded, admitted** |
| Support rows populated (U5) | Two admitted architecture rows in `pml0-support-matrix.md` (PML0-U5 schema v0.1.0, all 11 fields each): row 1 = training architecture row (BERT-tiny fragment transformer block, forward-only, f32); row 2 = selected inference architecture row (SmolLM2-360M scaled, llama/dense, Q4_K_M storage / f32 compute). Reject log records R3/R4/R5/R9/R10/R11 rejections | **MET** |
| README regen + audit 0 findings | `generate-factory-readme.py --check` fresh after regeneration; goal-status audit 0 findings (see Validation) | **MET** |

## Decision context honored

- **Phase intent held**: PML3 forward functions do not require PML4 training
  machinery (campaign Dependency Rule 3). The training path (`forward_mlp_loss`)
  consumes the compiler-generated backward companion, which is PML4's domain to
  productize; PML3 only proves the shared forward composes with it structurally.
- **CTO Q2 deferral recorded, not hidden**: the U4 partial note appears in the
  support matrix rows (`pml0-support-matrix.md` §1 row notes) and in this
  closeout. Rows do not claim executed identity.
- **One-row narrowing**: rows are exact admitted combinations; no other
  architecture/dtype/shape/quantization is claimed.

## Validation (one closeout run)

- `grep -n '^\*\*Status\*\*' CAMPAIGN.md`: PML3 stage line machine-parseable
  (`**Status**: delivered — …PML4 next…`); PML2 line unchanged (active, C3
  blocked); all stages still carry status lines.
- gradus `check-source`: PASS.
- gradus `check-compile` (FABER_BIN=faber/target/release/faber): PASS (gradus
  library source + gradient-seam consumer fixture).
- `python3 ../radix/scripta/generate-factory-readme.py --factory-root
  docs/factory --check`: PASS after regeneration (this record added to the
  gradus factory README).
- goal-status audit (`audit-factory-goal-status.py --factory-root
  docs/factory`): **0 findings**.
- `git diff --check`: PASS.

## Residuals + owners

| # | Residual | Owner | State |
| --- | --- | --- | --- |
| 1 | PML6-U3 aggregates every admitted row (formats, architectures, dtypes, quantizations, shapes, tokenizers, backends) into `pml0-support-matrix.md` (`pml6-delivery.md` PML6-U3) — the PML3 two rows join that full-matrix aggregation, not this closeout | PML6 delivery owner (Mind/planner routes at PML6 lowering) | pending — PML6 stage |
| 2 | Runtime-evidence gate for U4: execute bare forward vs the generated backward companion and record a numerical identity bound (CTO Q2) after the runtime-evidence gate exercises this path; then the training row's identity claim can be upgraded from structural to executed | auditor / faber test path (runtime-evidence gate) | deferred — gate pending |
| 3 | Verify at the runtime-evidence gate that the deferred identity claim was never asserted in support rows (reject log R9/R11 discipline holds) | auditor / faber test path | pass (re-verify at gate) |

## Escalation

None — gate MET, phase delivered. PML4 is next (planned, after PML3). Residuals
#1 and #2 are forward-bound, not PML3-blocking.
