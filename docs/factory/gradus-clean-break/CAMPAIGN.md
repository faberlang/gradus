# gradus-clean-break campaign stub

Routing stub for operator need `127f9fd6` (3-wave conversion order, settled).
Wave 1 is chartered and lowered; waves 2-3 are gated successors named here so
later planning cannot mint a duplicate home. One wave per planner assignment;
this stub does not lower waves 2-3.

| Wave | Scope | State / gate |
| --- | --- | --- |
| 1 — collapse existing twins | Delete the seven named `_NxM` wrappers whose typed generic twin already exists; move all callers (both repos); docs closeout. Goal [`GOAL.md`](GOAL.md), units [`wave-1-delivery.md`](wave-1-delivery.md) | **Chartered** — task `4aa2f634`, operator need `127f9fd6` + amendment `59b4074a` |
| 2 — author missing twins, delete remaining zoo | `mse<M,N>` twin then delete `mse_2x2/4x4/2x8`; per-channel `[N]` bias `linear` form and `layernorm<T,D>` twin then delete `linear_2x8`/`layernorm_2x8`; re-sweep `train_step_*` / `bert_tiny_block_2x8` / `forward_mlp_loss [4,4]` against whatever twins then exist | **Gated**: starts only after wave 1 closes (need's conversion order). Lane paper: `factory/krs-2` branch `c419b02` body-reroutes for `linear_2x8`/`layernorm_2x8`; `*_carrier` residuals shrink as callers pin (SEM014/SEM005 posture, not this campaign's rewrite) |
| 3 — kernel.fab statues to size-generic device leaves | Convert the 48 `kernel.fab` fixed-shape statues to size-generic device leaves | **Gated**: not before wave 1 done AND shape-generic-device-route SGD-1 (imported-generic entry discovery) settled. Receipt-pin exceptions (`gea3-*-v1` replay, GEA1 gemv `[320,960]` frozen-chain) are frozen evidence, not callable API (amendment `59b4074a`) |

Campaign law (operator ruling, standing): old fixed-shape sizes go away
completely in favor of shape generics unless a named identity/receipt pin is
an absolute requirement; a training exemplum that happens to be 2×2 or 4×4
instantiates the generic at the call site; named overloads are the defect.
