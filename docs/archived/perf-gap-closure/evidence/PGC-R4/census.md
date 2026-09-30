# PGC-R4 FMA / barrier / launch census (condition-B primary evidence)

Model, corrected per CTO-B finding 2 (verdict `a694cd2c`; verbatim
`d726be16` FINDING 2): **dispatched FMA counts every matrix slot the
8×8 MMA executes** — a dispatched multiply-accumulate is a slot the body
runs, whether or not its operands are useful. The old scalar body
dispatched the tile-padded row extent (`ceil(M/8)·8` rows) because its
tail lanes run the full K loop on zero-filled operands with no guard
distinction. The simdgroup recipe dispatches the **same** padded extent:
the partial band's guards zero-fill the A tile **before** the accumulate,
so the zero-filled rows are executed as slots that contribute no useful
multiply. The earlier census claimed the simdgroup recipe's counted
dispatched class collapses onto the useful `M × N × K` product
("padding class gone"); **that claim is withdrawn** — the zero-filled
simdgroup slots still execute, and the body-efficiency win is the
simdgroup datapath plus the barrier-pair removal, not slot elimination.

Per-family, fixed-1000 statue (launch counts identical to the R3 family —
launch graph unchanged, verified against this branch's exported plan):

| entry | launches | useful FMAs/launch (M·N·K) | dispatched FMAs/launch (every slot the 8×8 MMA executes — 40-row padded) | zero-filled/padded slots/launch (dispatched − useful; still executed) | recipe |
| --- | ---: | ---: | ---: | ---: | --- |
| prefill_gemm_gate_up | 64 | 88,473,600 | 98,304,000 | 9,830,400 | simdgroup |
| prefill_gemm_down | 32 | 88,473,600 | 98,304,000 | 9,830,400 | simdgroup |
| prefill_gemm_qo | 32 | 33,177,600 | 36,864,000 | 3,686,400 | simdgroup |
| prefill_gemm_kv | 64 | 11,059,200 | 12,288,000 | 1,228,800 | simdgroup |
| prefill_gemm_o | 32 | 33,177,600 | 36,864,000 | 3,686,400 | scalar (chunked arm, excluded) |
| prefill_lm_head_gemv | 1 | 47,185,920 | 1,698,693,120 | — | scalar (frozen pin; R2/C2 family) |
| prefill_score/context_gemm | 480+480 | bucketed extents (B1 arms) | 40×40/36×36 class | — | scalar (strided/bucketed, excluded) |

For the four admitted entries the dispatched extent is the same
40-row-padded slot count the old scalar body executed — the recipe
changes the datapath and the barriers, not the dispatched slot count.

**Zero-filled/padded slot census (still executed):** the four admitted
entries' zero-filled/padded slots total
`4·(960·960 + 320·960 + 2560·960 + 2560·960) × launches`
= 117,964,800 (qo) + 78,643,200 (kv) + 629,145,600 (gate_up) +
314,572,800 (down) = **1,140,326,400 slots (~1.14B)** — and the 8×8 MMA
executes every one of them. The earlier "~1.14B dispatched-FMA removal"
claim is withdrawn (CTO-B finding 2, verdict `a694cd2c`; verbatim
`d726be16` FINDING 2): dispatched FMAs count every matrix slot the MMA
executes, and the partial band's zero-filled rows are executed slots,
not eliminated ones. The ~1.65B 40-row-padding class never falls at the
hardware level; the census now separates useful FMAs from
zero-filled/padded slots instead of folding them into one count.

**Card status: the padding-removal criterion is NOT met.** The R4
`done_when`'s padded-FMA-class-falls / "padding class gone" criterion is
not satisfied — the ~1.14B zero-filled/padded slots still execute as
simdgroup MMA slots. The completion contract is operator scope and is
NOT amended by this record; this is the honest status per CTO-B finding
2. What does land is the simdgroup datapath plus the barrier-pair
removal (barrier census below), not slot elimination. The remainder
(~0.5B: chunked `gemm_o` plus the bucketed score/context arms) is
outside this recipe's admission law and stays scalar — an honest
boundary, not a hidden regression.

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
