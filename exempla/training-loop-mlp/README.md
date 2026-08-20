# training-loop-mlp — the PML4-U6 composed training loop

The bounded-convergence workload for the PML4 phase gate
(`gradus/docs/factory/production-ml-library/pml4-delivery.md` PML4-U6):
a 4×4 two-layer MLP (linear → GELU → linear → MSE), 100 steps, lr 0.1 —
the accepted MLP training-proof shape (`examples/training/mlp`, the pinned
CPU/FMIR oracle).

**Tier**: structural (PML6). Oracle pins below match `src/train.proba`
(PML4-U6). **No executed convergence is claimed** while the FMIR lever
(CTO8-1) is open.

## What the loop composes (the U6 residual from PML4-U5)

| Step | Surface |
| --- | --- |
| Schedule → optimizer-state binding | `train.scheduled_rate` (U4) feeds `optimize.construct`'s `rate` (U3) each step — the accepted constant lr 0.1 is the schedule `Schedule(0.1, 0, 1, 0.1)` (vertex == end) |
| Shared-layer training path | `gradus.forward_mlp_loss` (loss) + the compiler-generated companion `forward_mlp_loss_backward` (gradients) |
| Per-parameter gradients | `gradient.construct` records (U2): identity + generation = the parameter version at the backward |
| Optimizer steps | `optimize.step` (U3): fresh-gradient rules, fail-closed; `parameter.mutate` bumps version |
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

## Execution record (honest — CTO Q2 / CTO8-1)

This library-backed composition is **compile-validated** by
`faber check` on the package (the reverse-AD transform runs; every U1–U5
call and the companion invocation type-check). **Executed training is
env-blocked on both available lanes today**:

1. **FMIR stepper** — the recorded library-import gap: `faber test` on a
   library-importing surface fails with `unsupported MIR lowering: method
   call before runtime/provider MIR lowering` (library-to-library calls
   do not resolve in the stepper). Campaign name for the open gate:
   **FMIR lever / CTO8-1**.
2. **Rust emit lane** — `faber emit -t rust` on the training path fails
   with `TARGETLANE001: lane_requires_mir_backed_target`: the AIR-lane
   reverse-AD companion (`@ radix lane "air"` + `@ radix backward`) does
   not lower to the Rust target lane.

PML4-U6 is therefore **PARTIAL** per the standing bar: the convergence
proof is structural (composition + oracle pins), and executed
value-identity (the loop's loss trajectory vs the pins, the resumed
trajectory, the deterministic-seed byte identity) is deferred to the
auditor-owned runtime-evidence gate. **No executed convergence is
claimed.**

To run the gate once the lanes open: `faber run -t fmir .` (FMIR lane) or
emit-to-Rust + scratch-crate `cargo run` (Tela double-build pattern) and
compare the `loss_trace` against the pins above under numeric-policy
v1.0.0.

## Related

- Seam consumers: `exempla/gradient-seam/`, `exempla/gradient-seam-nolib/`
- Token generation: `exempla/token-generation/`
- Diagnostics: `docs/diagnostics.md`
