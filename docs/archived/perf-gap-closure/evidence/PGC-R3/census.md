# PGC-R3 evidence — post-fix re-census, baseline-family re-key, owed-evidence discharge

Status: **capture re-run owed on AC power** — the 2026-08-28 full-stage capture
below completed on battery power (`power_class: battery`, burgus discharging);
the card's done_when requires power AC. Need `c2635c71` requests operator AC.
Everything except the AC re-capture and the baseline append (which certifies
the family of record and is therefore withheld until the AC capture exists)
is discharged here.

## Re-keyed pin block (operator ruling 442f7f0d — §7.5 option a, re-pin)

| Member | Pin |
| --- | --- |
| gradus revision | `b762163664b65fcb3d8d71aee23b181ecdd3a1f6` (R3-time gradus, post-B3/R1/R2 folds) |
| gradus `src/kernel.fab` sha256 | `c9cdbb54e5bd35f0dec076f63bb67a289aae71e014360a2550d470a96bf2e08c` |
| radix revision | `c34b3976a0242b9c61018e0677879f72ee50796e` (re-pin commit: target statues + kv_append frozen identities) |
| hosts revision | `007ba2acaddcb8b6abcfd23e3c42801455bdc1be` (R1 wire round-trip closure in the shared driver) |
| comparator | `b10290-c8e03ce81` (unchanged; sha `125a9512…`) |
| GGUF | SmolLM2-360M-Instruct-f32, sha `4d10b02e…` (unchanged) |
| superseded gradus pin | `de687a4d…` / kernel sha `57345d45…` (pre-B3) |

The `kv_append` frozen-sha base-red family cleared with the re-pin:
`kv_append_k` → `6f6c2e69…`, `kv_append_v` → `d278360f…` (the post-B3
identities of `2f5d9ff9e`, restored from the `7d302c35f` hold at the pre-B3
protocol pin). Frozen-identity + bundle-export tests green under the new pin.

### §7.5 re-verification pass (inside R3)

Re-run under the new pin: `gea3_pipeline_test` frozen-identity family,
fixed1000/soak/full-model bundle exports, `gea3_pipeline_pgc_b1_test`
bucketed-attention export, hosts device family `gea3_decode_pgc_{b2,b3,c2,c5,r1,r2}`
(all green; commands in validation.md). Two latent shared-test drifts were
unmasked — findings, not fixed here (no-test-edit law; routed to mind):
`gea3_pipeline_plan_admission_rejects_missing_edges_or_undeclared_facts`
(popping the final dependency edge no longer trips "missing dependency") and
`gea4_admission_derived_gates_fail_closed` (kernels[0] workgroup mutation
admitted; kernels[0] is now the R1 gather, not a TILE-class row).

## R1 open fact — ids `element_ty` (recorded, resolved as recorded divergence)

The plan/wire mirror stamps the gather ids resource `element_ty: "f32"`
(element_count 1 decode / 36 prefill, 4 B per id) because the hosts GEA3
statue is F32-only (`DeviceDataType` has no `u32`); the emitted MSL truth is
`device const uint* ids`, fail-closed at the emitter
(`radix-mir-metal/src/emit/gather.rs:91-100`) and pinned by
`gea3_decode_pgc_r1.rs`. Byte width is correct (4 B = u32); the mirror dtype
label is the statue constraint, not a defect. Recorded in the re-key per the
R1 validation's instruction; resolution = keep the f32 wire label, uint
emitted truth.

## Census (battery capture — structural rows power-independent; wall/encode rows provisional)

Per-step, fixed1000 statue, run-001, vs the PGC-B2 capture (pre-R1 family):

| Row | B2 | R3 | delta |
| --- | ---: | ---: | --- |
| prefill launches/encoders | 2115 | 2115 | 0 (selector matmul → gather launch, 1:1) |
| prefill staged bytes | 23,076,864 | 15,999,120 | **−7,077,744** (one-hot selector removed; ids upload 144 B) |
| prefill copy-in handles | 1089 | 1089 | 0 |
| prefill readback bytes | 7,077,888 | 7,077,888 | 0 (36-row logits output still declared; R2 consumes the final row) |
| decode launches/encoders | 2115 | 2115 | 0 |
| decode readback bytes | 196,608 | 196,608 | 0 (one vocab row) |
| decode copy-in handles | 1089 | 1089 | 0 |
| prefill wall ms (battery — not AC-comparable) | 64.3 (AC) | 197.9 | battery-throttled; withhold |
| decode encode ms (battery — not AC-comparable) | 4.16 (AC) | 74.9 | battery-throttled; withhold |

Dispatched-FMA/launch census per entry family (derived from the exported
fixed1000 program plan, corrected graph):

| entry family | launches | dispatched FMAs | notes |
| --- | ---: | ---: | --- |
| prefill_gemm_gate_up | 64 | 5,662,310,400 | body-efficiency lane (R4) |
| prefill_gemm_down | 32 | 2,831,155,200 | R4 |
| prefill_lm_head_gemv | 1 | 1,698,693,120 | useful 47,185,920 final-row (36× overcompute stands in dispatch) |
| prefill_gemm_qo / gemm_o | 32+32 | 1,061,683,200 each | R4 |
| prefill_gemm_kv | 64 | 707,788,800 | |
| prefill_kv_write_k/v | 32+32 | 405,504,000 each | |
| prefill_score/context_gemm | 480+480 | 39,813,120 each | per-bucket extents (B1) |
| prefill_embedding_gather | 1 | 0 | R1 row copy; 36×960 useful copies; selector staging gone |
| decode_score/context_gemm | 480+480 | 33,423,360 each | w16 one-row (B2 KEEP), n=1088, grid 68 |
| decode_gemv_gate_up | 64 | 157,286,400 | |
| decode_gemv_down | 32 | 78,643,200 | |
| decode_gemv_qo | 64 | 58,982,400 | |
| kv_append_k/v | 32+32 | 11,264,000 each | B3 selected-row writes |
| lm_head_gemv (decode) | 1 | 47,185,920 | |
| elementwise/rope/transpose/softmax/rmsnorm families | — | 0 GEMM-class | fusion candidates below |

Two-class-compatible fusion candidates (compatible launch graph; byte/exact
identity only where materialization-free):
1. rope_q ∥ rope_k (per layer, independent inputs, same geometry) — elementwise class.
2. residual_add after swiglu/gemv_down consumers (elementwise chain).
3. decode_key_transpose → decode_score_gemm (producer-consumer, avoids intermediate materialization).
4. kv_append_k ∥ kv_append_v pair (identical shape, disjoint outputs).
5. decode_masked_softmax → decode_context_gemm (adjacency).
6. prefill head chain: prefill_head_rmsnorm → prefill_lm_head_gemv (final-row view already present).

## Owed-evidence discharge

- `PGC-B1/`: physical gate RAN (hosts `gea3_decode_pgc_b1_dispatches_early_and_late_work_buckets`,
  both buckets at capacity 1100, green on device). Certified-join gate: all
  Faber-side assertions pass on the R3 receipt (status green, n_predict 1000,
  l_max 1100, 1000 steps + prefill); its comparator assertion
  ("/ 1000 tokens") is unmeetable — the comparator naturally completes at 40
  tokens in every recorded family capture including the standing baseline
  (tokenizer-divergence law 46ab4e94, independent pins). Finding filed.
- `PGC-C5/`: copy-in census derivation above (staging bytes 23,076,864 →
  15,999,120 with handles constant 1089 — weight-shaped restaging was already
  once-resident in the folded family; the remaining delta is R1's selector
  removal); `gea3_pgc_c5_*` green on the R3 family bundle/receipt; gradus
  no-diff proof artifact `gradus-no-diff-proof.txt`.
