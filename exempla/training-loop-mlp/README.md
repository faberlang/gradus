# training-loop-mlp — seeded MLP training loop

The bounded-convergence workload is a 4×4 two-layer MLP (linear → GELU →
linear → MSE), trained for 100 steps at lr 0.1 from three fixed seeds (1, 7,
42). All trainable tensors come from `random.initialize_fan_uniform`; no
weights are literal constants. The executable prints the per-seed
final/initial ratio and convergence-gate result.

**Tier**: executed (MIR interpreter). The shared typed forward, optimizer,
metrics, and checkpoint round-trip remain visible in each run.

## Convergence and trajectory

The gate is `final/initial < 0.1`. Measured f32 losses at steps 0, 10, 25,
50, 75, and 99 are pinned below; final ratios are printed by the executable.
All three seeds pass.

| Seed | Step 0 | Step 10 | Step 25 | Step 50 | Step 75 | Step 99 | Final/initial |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 1.1323851 | 0.5709054 | 0.27122456 | 0.070147224 | 0.0129020875 | 0.0037757207 | 0.0033343078 |
| 7 | 1.017981 | 0.6513029 | 0.3317264 | 0.12416615 | 0.05316765 | 0.026682222 | 0.02539877 |
| 42 | 1.1955258 | 0.68769 | 0.37669003 | 0.08676115 | 0.015014685 | 0.0030090334 | 0.002359472 |

The former single-seed oracle pins were step 0 `1.576448169383708`, step 10
`0.7815377070077427`, step 25 `0.4303461875641296`, step 50
`0.13848813116166797`, step 75 `0.04746405569680761`, and step 99
`0.017928625511508454` (ratio `0.01137`). They are replaced by the seeded
trajectory table above. `src/mlp.proba` pins the seed-1 gate and descending
trajectory at steps 0/10/50/75.

## Composed training path

| Step | Surface |
| --- | --- |
| Schedule → optimizer-state binding | `schedule.scheduled_rate` feeds the constant lr 0.1 into optimizer state each step |
| Shared-layer training path | `mlp.forward_mlp_loss` + generated `forward_mlp_loss_backward` |
| Forward agreement | The typed shared `mlp.forward_mlp` is checked against the training loss each step |
| Per-parameter gradients | `gradient.construct` records identity and generation |
| Optimizer steps | `optimize.sgd_step` updates tensors; `optimize.step` tracks parameter/checkpoint state |
| Per-step metric log | `metrics.metric` records loss and regression-match rate |
| Checkpoint in/out | Optimizer state and RNG state survive the checkpoint wire round-trip |

Run with `faber run --library-home "$LIBHOME" exempla/training-loop-mlp`.
