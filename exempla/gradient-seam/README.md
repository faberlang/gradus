# gradient-seam — library-import gradient companion (structural)

Consumer fixture for the Gradus reverse-AD import seam: calls
`gradus:gradient` through `importa` (SEM004 companion export) and compares
the companion gradient to a per-element central finite-difference check.

## Inputs (pinned in `src/main.fab`)

| Symbol | Value |
| --- | --- |
| `x` | `[[1.0, 2.0], [3.0, 4.0]]` f32 |
| `w` | `[[0.5, -0.25], [1.0, 1.5]]` f32 |
| Forward | `gradient.simple_loss(x, w)` = `mean(x · w)` (elementwise product, then mean) |
| Backward | `gradient.loss_backward(x, w, gradient.nil(), 1.0)` → `grad_w` |
| FD step | `eps = 1e-5` central difference on each element of `w` |

## Expected oracle (f64 evaluations of the documented arithmetic)

These are the **accepted pins** for the seam once the executed lane is open.
They match the arithmetic in `src/main.fab` (and the historical S0-D rebaseline
record). **This README does not claim an executed run.**

| Quantity | Expected |
| --- | --- |
| Forward loss | `2.25` |
| Companion `grad_w` (flat) | `[0.25, 0.5, 0.75, 1.0]` |
| FD vs companion | per-element diffs on the order of `~1e-11` (central difference) |

Printed order in `main.fab`: `nota loss_lib`, `nota flat_gw`,
`nota [fd0…fd3]`, `nota [dif0…dif3]`.

## What it proves (structural tier)

| Step | Surface |
| --- | --- |
| Library import | `importa ex "gradus:gradient"` + `gradus:math` |
| Forward wrapper | `gradient.simple_loss` across the `importa` boundary |
| Companion call | `gradient.loss_backward` — compiler-generated companion exported through SEM004; no local `@ radix backward` mirror required |
| FD check | four central-difference probes on `w` |

`faber check` on this package is the structural gate (import seam + reverse-AD
transform type-check).

## Execution record (honest — CTO Q2 / CTO8-1)

**No executed run is claimed here.** Campaign posture (PML6): exempla e2e and
proba execution remain on the **FMIR lever** until that pre-release item opens.
The co-located source header still records the library-import residual for
`faber run -t fmir` on library-importing packages; the self-contained
companion path lives in `exempla/gradient-seam-nolib/`.

Historical S0-D rebaseline evidence (toolchain-dependent; not a standing
executed claim for this campaign):
`radix/docs/factory/gpu-training-lowering/gradus-seam-rebaseline.md`.

To run once the FMIR lever opens:

```bash
faber check .
faber run -t fmir .
# compare printed loss / grad_w / FD diffs to the oracle table above
```

## Related

- Self-contained companion path: `exempla/gradient-seam-nolib/`
- Training composition: `exempla/training-loop-mlp/`
- Diagnostics: `docs/diagnostics.md`
- API: `docs/api-reference.md` (`gradus:gradient`)
