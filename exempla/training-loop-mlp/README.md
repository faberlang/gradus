# training-loop-mlp — the PML4-U6 composed training loop

The bounded-convergence workload for the PML4 phase gate
(`gradus/docs/factory/production-ml-library/pml4-delivery.md` PML4-U6):
a 4×4 two-layer MLP (linear → GELU → linear → MSE), 100 steps, lr 0.1 —
the accepted MLP training-proof shape (`examples/training/mlp`, the pinned
CPU/FMIR oracle).

**Tier**: executed (FMIR stepper). Oracle pins below match `src/train.proba`
(PML4-U6). The 100-step loop runs through the delegating stepper
(`train.train_step_4x4` → `optimize.sgd_step_4x4`); printed losses match
the pins (final `0.017928625511508454`).

## What the loop composes (the U6 residual from PML4-U5)

| Step | Surface |
| --- | --- |
| Schedule → optimizer-state binding | `train.scheduled_rate` (U4) feeds `optimize.construct`'s `rate` (U3) each step — the accepted constant lr 0.1 is the schedule `Schedule(0.1, 0, 1, 0.1)` (vertex == end) |
| Shared-layer training path | `gradus.forward_mlp_loss` (loss) + the compiler-generated companion `forward_mlp_loss_backward` (gradients) |
| Per-parameter gradients | `gradient.construct` records (U2): identity + generation = the parameter version at the backward |
| Optimizer steps | Tensor SGD: `train.train_step_4x4` → `optimize.sgd_step_4x4` (the delegating stepper). Parameter/checkpoint: `optimize.step` (U3) fresh-gradient rules, fail-closed; `parameter.mutate` bumps version |
| Per-step metric log | `metrics.metric` (U5): `loss` = the loss (the accepted trajectory); `accuracy` = the documented regression-match rate (`|pred − target| ≤ 0.1` over the 16 output elements, read from the bare shared forward `gradus.forward_mlp`) |
| Checkpoint in/out | `train.construct_checkpoint` (U5): whole-optimizer state wire (U3 `serialize`) + RNG state + epoch/step; `serialize_checkpoint` → `deserialize_checkpoint` is the resume round-trip (`checkpoint_equal`) |

## Convergence target (accepted oracle, f64 evaluations)

Pinned in `src/train.proba` (PML4-U6). The proba asserts the gate
`final/initial < 0.1` and the trajectory points below (step 25 is part of
the documented target series; the proba binds l0/l10/l50/l75/l99 for the
ratio checks):

| Step | Loss |
| --- | --- |
| 0 | 1.576448169383708 |
| 10 | 0.7815377070077427 |
| 25 | 0.4303461875641296 |
| 50 | 0.13848813116166797 |
| 75 | 0.04746405569680761 |
| 99 | 0.017928625511508454 |

Convergence ratio `final/initial = 0.01137 < 0.1` (the accepted gate).

## Execution record (train-step-optimizer-call unit 4)

The library-backed composition **executes** on the FMIR stepper.
Library-to-library calls resolve (radix `43c0102ba`). The tensor SGD
update is `train.train_step_4x4` → `optimize.sgd_step_4x4`. Printed
per-step losses match the pins above (final `0.017928625511508454`);
values did not move vs the pre-delegation oracle.

Run: `faber run src/main.fab` from this package (or
`faber run gradus/exempla/training-loop-mlp/src/main.fab` from the
container), with `FABER_LIBRARY_HOME` pointing at `faberlang/`.

## Related

- Seam consumers: `exempla/gradient-seam/`, `exempla/gradient-seam-nolib/`
- Token generation: `exempla/token-generation/`
- Diagnostics: `docs/diagnostics.md`
