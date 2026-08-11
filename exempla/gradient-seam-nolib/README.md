# gradient-seam-nolib — self-contained reverse-AD + FD (structural)

Self-contained companion of `exempla/gradient-seam`: the same forward loss and
per-element finite-difference check, but **without** `gradus:*` library imports.
The `@ radix lane "air"` + `@ radix backward "loss_backward"` annotations live
in this package so the reverse-AD path can be proven without the import seam.

## Inputs (pinned in `src/main.fab`)

| Symbol | Value |
| --- | --- |
| `x` | `[[1.0, 2.0], [3.0, 4.0]]` f32 |
| `w` | `[[0.5, -0.25], [1.0, 1.5]]` f32 |
| Forward | local `simple_loss(x, w)` = `mean(x.multiplica(w))` |
| Backward | local companion `loss_backward(x, w, nil(), 1.0)` → `grad_w` |
| FD step | `eps = 1e-5` central difference on each element of `w` |

## Expected oracle (f64 evaluations of the documented arithmetic)

Same arithmetic as `gradient-seam` (the library wrapper is a thin import of
this shape). **This README does not claim an executed run.**

| Quantity | Expected |
| --- | --- |
| Forward loss | `2.25` |
| Companion `grad_w` (flat) | `[0.25, 0.5, 0.75, 1.0]` |
| FD vs companion | per-element diffs on the order of `~1e-11` |

Printed order in `main.fab`: `nota loss`, `nota flat_gw`,
`nota [fd0…fd3]`, `nota [dif0…dif3]`.

## What it proves (structural tier)

| Step | Surface |
| --- | --- |
| Local forward | `simple_loss` with `@ radix lane "air"` + `@ radix backward "loss_backward"` |
| Companion | `loss_backward` called in-file (no `importa`) |
| FD check | four central-difference probes on `w` |

`faber check` on this package is the structural gate (AIR-lane reverse-AD
annotation + FD composition type-check).

## Execution record (honest — CTO Q2 / CTO8-1)

**No executed run is claimed here.** Campaign posture (PML6): exempla e2e and
proba execution remain on the **FMIR lever** (CTO8-1 named pre-release item)
until that gate opens. This package is the self-contained companion path that
historically carried the U1 execution proof when the toolchain allowed; that
history is not restated as a current executed claim.

To run once the FMIR lever opens:

```bash
faber check .
faber run -t fmir .
# compare printed loss / grad_w / FD diffs to the oracle table above
```

## Related

- Library-import seam: `exempla/gradient-seam/`
- Training composition: `exempla/training-loop-mlp/`
- Diagnostics: `docs/diagnostics.md`
