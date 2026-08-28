# PGC-R4 FMA / barrier / launch census (condition-B primary evidence)

Model, stated explicitly (truth over safety): the census counts
**declared multiply-accumulate work per launch** — a contracted
multiply-add counts when it operates on two non-zero-guarded operands.
The old scalar body counts the tile-padded row extent
(`ceil(M/8)·8` rows) because its tail lanes run the full K loop on
zero-filled operands with no guard distinction. The simdgroup recipe's
partial band guards zero-fill the A tile **before** the accumulate, so
rows past `M` contribute no counted multiply. **Hardware caveat,
disclosed:** the 8×8 simdgroup mma slot for a partial band still
executes over the zero-filled rows — the padded-row *slots* are not
eliminated at the hardware level; what falls is the counted padded-FMA
class, and the body-efficiency win is the simdgroup datapath plus the
barrier-pair removal, not slot elimination.

Per-family, fixed-1000 statue (launch counts identical to the R3 family —
launch graph unchanged, verified against this branch's exported plan):

| entry | launches | useful FMAs/launch (M·N·K) | old dispatched FMAs/launch (40-row padded) | padding class/launch | recipe |
| --- | ---: | ---: | ---: | ---: | --- |
| prefill_gemm_gate_up | 64 | 88,473,600 | 98,304,000 | 9,830,400 | simdgroup |
| prefill_gemm_down | 32 | 88,473,600 | 98,304,000 | 9,830,400 | simdgroup |
| prefill_gemm_qo | 32 | 33,177,600 | 36,864,000 | 3,686,400 | simdgroup |
| prefill_gemm_kv | 64 | 11,059,200 | 12,288,000 | 1,228,800 | simdgroup |
| prefill_gemm_o | 32 | 33,177,600 | 36,864,000 | 3,686,400 | scalar (chunked arm, excluded) |
| prefill_lm_head_gemv | 1 | 47,185,920 useful final-row vs 1,698,693,120 dispatched | — | — | scalar (frozen pin; R2/C2 family) |
| prefill_score/context_gemm | 480+480 | bucketed extents (B1 arms) | 40×40/36×36 class | — | scalar (strided/bucketed, excluded) |

**Padding-class delta:** the four admitted entries remove
`4·(960·960 + 320·960 + 2560·960 + 2560·960) × launches`
= 117,964,800 (qo) + 78,643,200 (kv) + 629,145,600 (gate_up) +
314,572,800 (down) = **1,140,326,400 FMAs (~1.14B)** of the ~1.65B
40-row-padding class. The remainder (~0.5B: chunked `gemm_o` plus the
bucketed score/context arms) is outside this recipe's admission law and
stays scalar — an honest boundary, not a hidden regression.

**Barrier census (gate_up, per launch, 1600 workgroups, 120 K slices):**

| recipe | in-loop barriers/workgroup | combine barriers/launch | total barriers/launch |
| --- | ---: | ---: | ---: |
| old scalar | 2 × 120 = 240 (all 1600 wg) | 0 | 384,000 |
| simdgroup | 120 × 320 partial-band wg only | 1600 | 40,000 |

≈ 9.6× fewer threadgroup barriers per launch; the 1280 full-band
workgroups execute the entire K loop with **zero** barriers (direct
device `simdgroup_load`), and no workgroup executes the scalar body's
per-K-slice barrier pair.

**Staging census:** unchanged (same signature/ABI; the fixed-1000
staged-byte row is byte-identical to the R3 family — 15,999,120 B,
copy-in handles 1089 — this card changes no binding).
