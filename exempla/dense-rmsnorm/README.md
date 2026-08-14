# REF-01-U1.1 — Generic RMSNorm executed proof

This package is the executed proof for the generic RMSNorm forward row
(`gradus:nn rmsnorm`) — the llama-arch norm family:

```text
rmsnorm(x, γ, ε) = x / sqrt(mean(x²) + ε) · γ   (LAST axis, no centering)
```

It runs the row over the staged f32 carrier through package MIR and prints
PASS for every pinned value (0 FAIL, exit 0). Every pinned reference value is
an independent f64 evaluation of the documented formula (external Python), ε
per llama-arch (`1e-5`, the llama.cpp `LLM_NORM_RMS` default). Each pin
compares within the documented `5e-4` absolute tolerance (the PML3 norm
precedent): the reference is f64, the row is f32 self-hosted (Newton sqrt).

The package is fully deterministic and in-memory: no filesystem read, no
model payload, no device handle.

## Pin surface

| Row | Input x | Scale γ | ε | Reference values (f64) |
| --- | --- | --- | --- | --- |
| 1 | `[1..8]` (rank 1) | unit `[8]` | `1e-5` | `0.198029 … 1.584236` |
| 2 | `[1..8]` (rank 1) | `[0.5 … 4.0]` `[8]` | `1e-5` | `0.099015 … 6.336943` (per-feature scaling) |
| 3 | `[9..16]` (`[2,4]`) | unit `[4]` | `1e-5` | rows normalize independently over the LAST axis |
| 4 | `[-3,-1,0,1,3,5,7,9]` | unit `[8]` | `1e-5` | negative values keep their sign (no centering) |

32 pinned values; 32 PASS / 0 FAIL.

## Receipt

Command, from the Hand packet:

```text
cd /Users/ianzepp/work/faberlang/worktrees/hand-2/gradus
env FABER_LIBRARY_HOME=/Users/ianzepp/work/faberlang/worktrees/hand-2 \
  /Users/ianzepp/work/faberlang/worktrees/hand-2/radix/target/debug/faber \
  run --target fmir exempla/dense-rmsnorm
```

Observed result (2026-08-14): exit `0`; 32 PASS lines and 0 FAIL lines.

```text
rmsnorm-row1-x0: PASS observed=0.19802946976603086
rmsnorm-row1-x1: PASS observed=0.3960589395320617
rmsnorm-row1-x2: PASS observed=0.5940884092980926
rmsnorm-row1-x3: PASS observed=0.7921178790641235
rmsnorm-row1-x4: PASS observed=0.9901473488301543
rmsnorm-row1-x5: PASS observed=1.1881768185961852
rmsnorm-row1-x6: PASS observed=1.386206288362216
rmsnorm-row1-x7: PASS observed=1.584235758128247
rmsnorm-row2-x0: PASS observed=0.09901473488301543
rmsnorm-row2-x1: PASS observed=0.3960589395320617
rmsnorm-row2-x2: PASS observed=0.8911326139471389
rmsnorm-row2-x3: PASS observed=1.584235758128247
rmsnorm-row2-x4: PASS observed=2.4753683720753856
rmsnorm-row2-x5: PASS observed=3.5645304557885558
rmsnorm-row2-x6: PASS observed=4.851722009267756
rmsnorm-row2-x7: PASS observed=6.336943032512988
rmsnorm-row3-r0c0: PASS observed=0.852324664637845
rmsnorm-row3-r0c1: PASS observed=0.9470274051531611
rmsnorm-row3-r0c2: PASS observed=1.041730145668477
rmsnorm-row3-r0c3: PASS observed=1.1364328861837931
rmsnorm-row3-r1c0: PASS observed=0.8938983922919382
rmsnorm-row3-r1c1: PASS observed=0.9626598070836258
rmsnorm-row3-r1c2: PASS observed=1.0314212218753134
rmsnorm-row3-r1c3: PASS observed=1.100182636667001
rmsnorm-row4-x0: PASS observed=-0.6414268339779874
rmsnorm-row4-x1: PASS observed=-0.21380894465932915
rmsnorm-row4-x2: PASS observed=0
rmsnorm-row4-x3: PASS observed=0.21380894465932915
rmsnorm-row4-x4: PASS observed=0.6414268339779874
rmsnorm-row4-x5: PASS observed=1.0690447232966458
rmsnorm-row4-x6: PASS observed=1.496662612615304
rmsnorm-row4-x7: PASS observed=1.9242805019339624
```

`faber check exempla/dense-rmsnorm` is green, and `scripta/check-compile`
includes the library check that validates the same `nn.rmsnorm` surface. The
co-located `src/nn.proba` suite pins the same f64 references at compile level
(`faber test` execution remains blocked by the imported-library provider
seam — the A1a precedent; this package is the executed proof).

## Evidence boundary

This is an executed forward-row receipt, not a model or inference claim. No
Metal/CUDA execution, no full-model payload residency, no GGUF file read.
The surface is device-neutral by design (`gradus:nn` imports no attention,
transformer, or backend module).
