# PGC-R4 evidence — simdgroup/vectorized prefill GEMM recipes

Status: **all primary (census/structural) evidence discharged; wall rows are
battery captures (power_class battery, 29% charge) recorded as L1-gated
secondary only — no wall claim is made; AC re-capture owed** (same posture as
the R3 capture; operator request for AC power rides the R3 `c2635c71` ask).

## What changed

`radix 80981a08e` (packet `factory/pgc-b2`): the Metal emitter lowers the
`TiledMatMul` recipe for the dense-f32 partial-band prefill class
(multi-row, `K` a tile multiple, `M` not — the `M = 36` family) through a
simdgroup fast path. Two simdgroups per 8×8 workgroup split the K slices by
parity with `simdgroup_multiply_accumulate`; full output bands load operand
tiles straight from device memory (`simdgroup_load`, zero barriers in the K
loop); the `M = 36` tail band stages double-buffered `float4` tiles with
zero-fill guards at ONE barrier per K slice (the scalar body's per-K-slice
barrier pair is gone); the two K-parity partials combine through one
threadgroup buffer and one end-of-kernel barrier. Launch graph, plan facts,
wire identities, and signature are unchanged (B2-class dispatch shape;
frozen exports green). `hosts 3a064e3` adds the device proof.

Admission law (`radix_mir::simdgroup_matmul_admission`): dense f32,
multi-row, `k % 8 == 0`, `m % 8 != 0`, workgroup (8,8), `n ≤ 8192`
(`SIMDGROUP_MATMUL_MAX_N` — the vocab-scale `prefill_lm_head_gemv` twin
keeps its frozen scalar emission pin; its useful-work narrowing is the
R2/C2 family, not this wave). Emit-side: no strided/chunked/gathered
operand windows, no launch output windows — `prefill_gemm_o` (chunked
context arm), score/context gemms (strided/bucketed arms), decode T=1, and
the kv-append rank-1 update all keep the scalar/one-row bodies.

## Two-class numeric declaration (per entry)

| entry | class | oracle |
| --- | --- | --- |
| prefill_gemm_qo / kv / gate_up / down | **B** — simdgroup accumulate contracts the multiply-add | frozen per-family tolerance vs the old recipe output (`frozen-tolerance.json`), never widened |
| prefill_gemm_o | **A** — excluded from the recipe (chunked arm); body byte-identical | new-vs-old delta exactly 0.0 on device |

Frozen bounds (device A/B, identical seeded inputs, LCG
`0x2545F4914F6CDD1D`, `device-ab/`):

| entry | old max abs vs CPU | new max abs vs CPU | new max abs vs old | new max rel vs CPU |
| --- | ---: | ---: | ---: | ---: |
| prefill_gemm_qo | 6.10e-05 | 5.49e-04 | 5.49e-04 | 2.32e-06 |
| prefill_gemm_kv | 4.58e-05 | 5.49e-04 | 5.49e-04 | 1.98e-06 |
| prefill_gemm_gate_up | 6.10e-05 | 5.80e-04 | 5.95e-04 | 2.46e-06 |
| prefill_gemm_down | 2.44e-04 | 2.56e-03 | 2.56e-03 | 3.99e-06 |

The hosts physical gate (`gea3_decode_pgc_r4.rs`, ignored test) re-ran the
exported entry sources on the real device and confirmed the observed
deltas at or under every frozen bound (green, see validation.md).

## Proba tuples

The four named cases' `(case_path, status, stderr bytes)` tuples are
byte-identical before/after (`proba-before/`, `proba-after/`,
`proba-tuples.json`): exit 1 at the pre-existing SEM013 at
`kernel.proba:596`, the same posture recorded by PGC-C2/R2. Gradus source
is untouched (`gradus-no-diff-proof.txt`, `git diff --exit-code`).

## Census (primary evidence — condition-B rider)

See `census.md`. Launch counts and geometries are unchanged from the R3
family (exported plan: prefill 2115 launches; gate_up 64 / down 32 /
kv 64 / qo+o 32+32). The four admitted entries' padded-FMA class
(~1.14B FMAs of the ~1.65B 40-row-padding class) falls in the
declared-work census; the remainder (chunked `gemm_o`, bucketed
score/context arms) is outside this recipe's admission and stays scalar.

## Paired parity (L1-gated secondary — battery, no claim)

`parity-raw/` + `parity-receipt.json` + `baseline-candidate/` per the
card's measurement commands, run from the packet at radix `80981a08e`,
hosts `3a064e3`, gradus pin `b7621636`. Battery observations only
(power_class battery, both arms): gradus prefill wall 75.8 ms
(median-of-3 runs 75.8/75.8/…; R3's battery capture recorded 197.9 ms on
the same battery class — recorded, NOT claimed; AC re-capture owed),
sampled GPU-busy 19.9 ms over 1024/2115 encoders (≈41.2 ms extrapolated)
vs the R3-era ~50.6 ms GPU-busy record. No wall or TFLOP/s claim is made
from this capture.
