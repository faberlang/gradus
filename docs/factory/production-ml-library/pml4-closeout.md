# PML4 Closeout Note — phase gate MET at the structural tier (executed tier deferred, recorded not claimed)

**Unit**: PML4 phase closeout (campaign gate; PML5 next per the ordering graph)
**Date**: 2026-08-09
**Predecessor**: PML4-U1..U6 all landed and admitted by Mind — U1 5f98e8b
(loss surface), U2 e09c79c (gradient-call contract), U3 9bebda9 (optimizer
state), U4 4b24c81 (schedules + train/eval mode), U5 94d8a94 (checkpoint
resume + metrics + seeds), U6 fc85de7 (bounded convergence + resume proof).
Delivery: `pml4-delivery.md`.
**Repo**: gradus.

## Outcome: phase gate **MET at the structural tier** — PML4 delivered

All six PML4 units landed. The phase gate (`pml4-delivery.md` §Phase gate) is
satisfied at the **structural (compile-level) tier**: losses, gradient calls,
optimizer state, schedules, train/eval mode, checkpoint resume, metrics,
deterministic seeds, and failure behavior compose publicly as a training
layer over the reusable forward functions (PML3), and the bounded workload's
convergence + resume reproducibility are proven at the composition level.

The **executed tier is explicitly deferred**, not claimed: executed
convergence values are env-blocked on both available lanes today (see the
runtime-evidence-gate blockers below). Every unit recorded its PARTIAL status
per CTO Q2; this closeout aggregates them.

## Per-unit evidence

| Unit | Commit | Evidence (structural tier) | Tier |
| --- | --- | --- | --- |
| U1 — Loss surface | 5f98e8b | `src/loss.fab` mse + cross_entropy over the tensor surface (typed errors, deterministic, non-finite fail-closed); `src/loss.proba` f64 oracle rows vs the accepted proofs (2×2 / 4×4 / 2×8 MSE, logsumexp CE) | structural |
| U2 — Gradient-call contract | e09c79c | `src/gradient.fab` one-contract companion invocation (`gradientes_simple_loss` calls the compiler-generated `loss_backward` inside the module wrapper), per-parameter `Gradiente` identity + generation, `obsoletus` staleness; f64 gradient oracle pins | structural |
| U3 — Optimizer state | 9bebda9 | `src/optimize.fab` SGD state: `SgdStatum` (identity/versio/generatio/passus/lentus), `passus` mutation rules (fresh-gradient, identity, trainable, shape — fail-closed), versioned wire exact round-trip; f64 update pins | structural |
| U4 — Schedules + mode | 4b24c81 | `src/train.fab` `Schedula` (warmup + cosine, self-hosted cos) + `Modus`/`dropout_pars` explicit-mode gate (no hidden global state); f64 schedule pins; attention.fab stale-header fold | structural |
| U5 — Checkpoint + metrics + seeds | 94d8a94 | `Semen` xorshift64 seed/RNG (owns the U4 dropout seam — `excutio` mask), `Tabula` checkpoint (state wire verbatim + RNG + epoch/step, interrupted-resume fail-closed), `metrics.fab` `accuratezza` + `Metricum`; exact state/draw/mask pins | structural |
| U6 — Bounded convergence + resume | fc85de7 | `exempla/training-loop-mlp` composed loop over U1–U5 (schedule→state binding, companion via the U2 contract, per-step `Metricum`, checkpoint in/out), compile-validated through the reverse-AD transform; `src/train.proba` U6 section pins the accepted trajectory + ratio gate | structural |

## Phase-gate checklist

| Gate clause | Evidence | Verdict |
| --- | --- | --- |
| Losses, gradient calls, optimizer state, schedules, train/eval mode, checkpoint resume, metrics, seeds, failure behavior compose publicly | U1–U5 surfaces land in `src/loss.fab`, `src/gradient.fab`, `src/optimize.fab`, `src/train.fab`, `src/metrics.fab`; every surface has a co-located proba (compile-level, causa-identity per validation) | **MET** |
| A bounded workload converges to the accepted training proof's target | The composed loop (`exempla/training-loop-mlp`) drives the accepted MLP 4×4 workload (lr 0.1, 100 steps). Accepted-trajectory pins (f64): steps 0/10/25/50/75/99 → 1.576448169383708 / 0.7815377070077427 / 0.4303461875641296 / 0.13848813116166797 / 0.04746405569680761 / 0.017928625511508454; convergence gate `final/initial = 0.01137 < 0.1` — **pinned and proba'd at the compile level** | **MET (structural)** |
| Resume reproducibility | U5 `Tabula` round-trip + the U6 composition-level checkpoint (four-slot optimizer-state wire + RNG + epoch/step) round-trip exactly (`tabula_aequus`); the embedded state wire validates at resume (`optimize.deserializa`); interrupted/corrupt-state wires fail closed explicitly | **MET (structural)** |
| Deterministic-seed test | Same seed → same xorshift64 sequence + draws (`train.proba` U5); same schedule → same lr sequence (`train.proba` U6). The accepted workload has no dropout, so the trajectory is seed-independent by construction; the seed is checkpoint-carried | **MET (structural)** |
| No performance claims | No throughput/latency/memory claims anywhere in the units or this closeout — correctness gate only | **MET** |
| Executed convergence | Executed loss-trajectory values vs the pins are env-blocked on both lanes — deferred to the auditor-owned runtime-evidence gate (blockers below) | **DEFERRED — recorded, not claimed** |
| README regen + audit 0 findings | `generate-factory-readme.py` regenerated + `--check` green; goal-status audit 0 findings (see Validation) | **MET** |

## Runtime-evidence-gate blockers (recorded compiler-lane inputs)

Executed training of the library-backed composed loop is blocked on both
available lanes. The concrete errors:

1. **FMIR stepper / library-import gap** — `faber test` on a library-importing
   surface fails with `unsupported MIR lowering: method call before
   runtime/provider MIR lowering`; `faber run -t fmir` on
   `exempla/training-loop-mlp` fails with `package MIR cannot transplant
   const data member initializer with unsupported expression shape`.
   Library-to-library calls do not resolve in the stepper (the recorded
   LIB-MIR gap).
2. **Rust emit lane / AIR-companion** — `faber emit -t rust` on the training
   path fails with `TARGETLANE001: lane_requires_mir_backed_target`: the
   AIR-lane reverse-AD companion (`@ radix lane "air"` + `@ radix backward`)
   does not lower to the Rust target lane, which also blocks the
   Tela-style scratch-crate cargo-run lane.

Named compiler-lane inputs: (a) FMIR library-call resolution in the MIR
stepper, or (b) Rust-lane lowering for the AIR reverse-AD companion. When
either opens, the auditor-owned runtime-evidence gate runs the composed loop
and compares its loss trajectory + resume trajectory + seeded runs against
the pins under numeric-policy v1.0.0 (gradient row 1e-4; loss row).

## Decision context honored

- **Executed tier deferred, not claimed**: every unit recorded PARTIAL per
  CTO Q2; no executed-identity claims exist in any proba, exemplum, or this
  closeout. The PML0-U5 schema rows' executed tier remains noted as
  structural (the PML3 rows already carry the `does NOT claim executed
  identity` note; no re-rows beyond that honesty note).
- **No new gradus code in this unit**: all six units landed; the only code
  touch is the exemplum-wiring decision below.
- **Exemplum-wiring decision (Mind-routed, recorded here)**: wire
  `exempla/training-loop-mlp` into `scripta/check-compile` alongside
  `exempla/gradient-seam` — **DECIDED: yes** (a compile-level gate, the same
  convention as the seam fixture). Implemented and verified green in this
  closeout; disclosed in the closeout commit.
- **Ordering-graph pointer**: the campaign ordering graph runs PML4 beside
  PML5/NGAB lanes after PML2+PML3; PML5 is the next Gradus phase
  (production inference computation layer — decode, KV-cache, sampling,
  generation configuration). PML4's structural training layer is PML5's
  input (the training path's composed loop is the aggregate reference).

## Validation (one closeout run)

- `grep -n '^\*\*Status\*\*' CAMPAIGN.md`: PML4 stage line machine-parseable
  (`**Status**: delivered (structural tier) — …PML5 next…`); all other stage
  lines unchanged.
- gradus `check-compile` (FABER_BIN=faber/target/release/faber): PASS
  (gradus library source + gradient-seam consumer + the wired
  training-loop-mlp composed-loop exemplum).
- `python3 ../radix/scripta/generate-factory-readme.py --factory-root
  docs/factory --check`: PASS after regeneration (this record added to the
  gradus factory README).
- goal-status audit (`./scripta/check-factory-goal-status`): **0 findings**.
- `git diff --check`: PASS.

## Residuals + owners

| # | Residual | Owner | State |
| --- | --- | --- | --- |
| 1 | Runtime-evidence gate for PML4 executed convergence (loss trajectory + resume trajectory + seeded runs vs the pins under numeric-policy v1.0.0). Blocked by the named compiler-lane inputs (FMIR library-call resolution OR AIR-companion Rust lowering) — the two blockers above are the gate's prerequisites | Auditor (faber test path) + radix lane (named inputs) | pending — gate |
| 2 | PML5 (production inference computation layer) is the next Gradus phase per the ordering graph; PML4's composed loop is its aggregate training reference | Mind routes at PML5 lowering | pending — PML5 |
| 3 | PML6-U3 aggregates every admitted row into `pml0-support-matrix.md` — the PML4 structural-tier rows join that full-matrix aggregation | PML6 delivery owner | **closed** — U3 `43d75ce` (full-matrix aggregation; see `pml6-closeout.md`) |
