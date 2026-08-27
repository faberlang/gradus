# Goal: perf-gap-closure — close the measured gradus-vs-llama parity gaps

**Status**: planned — forged 2026-08-27 from the operator gap-analysis order (six inspection/audit seats: four Luna xhigh row inspectors + two GLM-5.3 phase auditors; reports cited below) and the operator running commentary (fusion pre-work, the anti-prior guidance law, closure intrinsics, deterministic drivers). Admission pending operator fine-tuning; no unit routed yet.
**Home**: `gradus/` (dominant write surface), with named arms in `hosts/`, `radix/`, and the skills repo.
**Baseline of record**: the gradus-llama-parity goal (`radix/docs/factory/gradus-llama-parity/`) — U5 owns the first AC baseline; until it lands, the U2 live captures (`/tmp/glp-u2-live-final-1787859628`, mirrored in the U3 fixture pair) are the working baseline.
**Governing laws**: gpu-lessons L84 (decompose algorithm vs dispatch; never credit one lever for another's movement), L86 (device kernels never execute under the MIR runner), structural-change re-baseline discipline; bench-law power/AC rules apply to every measurement this goal takes.

---

## 1. The measured problem (all numbers certified, AC power, SmolLM2-360M-Instruct f32, same GGUF both arms)

| Row | llama | gradus | ratio |
| --- | ---: | ---: | ---: |
| short decode (8 tok) | 236.5 t/s | 32.2 t/s | 7.33× |
| fixed-1000 decode (sustained) | 231.8 t/s | 15.65 t/s | **14.81×** |
| short prefill | 3066 t/s | 571 t/s | 5.37× |
| fixed-1000 prefill | 3158 t/s | 567 t/s | 5.57× |

Decode step wall 63.890 ms (fixed-1000); 31.013 ms (short). Prefill wall ~63 ms both
statues (statue-independent; ratio spread is comparator variance).

## 2. The three gap layers (six-seat consensus; Luna and GLM families agree independently)

**L1 — Dispatch/execution shell (both phases).** Every phase runs ~2,115
single-kernel Metal encoders (32 layers × 66 + 3), serialized on the GPU
timeline: ~51 ms queue sync in prefill / ~57 ms in decode, plus ~4–9 ms
encode, where llama executes one reused graph in 4.3 ms/step. GPU-busy
measurements cover 1,024 of 2,115 encoders (partial sample — all bubble
figures are upper bounds until D1 lands).

**L2 — Shape/capacity pinning (decode-dominant).** Full-capacity attention
spliced at 1100 (`score_gemm` 70,400 vs 4,864 elements), 1,100-element
softmax reductions every step, capacity-scaled KV writes, 8× T=1 GEMV row
overcompute. Per-step time is FLAT across the 1000-step run — the
7.33×→14.81× doubling is static overcompute, not history growth.

**L3 — Prefill algorithmic waste (compute-bound; the 1.4 GB bandwidth-floor
model is inapplicable here).** ~3.73B avoidable FMAs (dense one-hot
embedding matmul + all-36-row LM head where one row feeds next-token),
~2.15B avoidable (RMSNorm rescans each 960-wide row per output element —
O(D²) vs O(D)), ~1.65B padded (scalar untiled 8×8 GEMMs).

**Instrument defects found by the audits (fix first):** GPU-busy partial
sample unlabeled; receipt `sync_wait_us` mislabeled (it is the launch clock).

## 3. Parallelism architecture (the operator's structural requirement)

No unit in this goal depends on another unit's unlanded output. Parallelism
comes from three mechanisms:

1. **Disjoint vertical slices.** Every L2/L3 unit owns ONE defect across its
   whole vertical (gradus source → export pin → device test → paired-parity
   delta). Defects touch disjoint kernel entries, so units never share a
   done-oracle or an intermediate artifact.
2. **Packets for concurrent write seats.** Units touching `gradus/src/`
   (one file, many entries) run in `worktrees/<lane>/` packets on their own
   branches; the Mind folds serially. Disjoint entry regions keep fold
   conflicts mechanical.
3. **Already-existing baselines.** Every unit measures against the standing
   captures/baseline — no unit waits for another unit's numbers. Attribution
   comes from per-unit paired-parity deltas (L84 discipline: one lever, one
   measurement).

The serial exception is the polish wave's **guidance law (A0)**: polish
seats may not spawn before the law text exists. A0 is a skills-repo-only
unit and lands first.

## 4. Units

### D1 — instrument hardening (hosts + radix receipts)
| Field | Value |
| --- | --- |
| `id` | `PGC-D1` |
| `outcome` | Full encoder GPU-timestamp sampling (or explicit partial-sample labeling in every receipt field that depends on it); rename/fix `sync_wait_us` to its true meaning (launch clock) and add a true submit+sync clock if observable. |
| `write_scope` | `hosts/macos-arm64/` receipt/timing surfaces; the mir-emit-harness timing-companion emitter if the sample count lives there. No kernel source. |
| `done_when` | A fixed-1000 decode receipt reports per-step GPU busy over ALL encoders (or labels the sample fraction in the field name/shape); the mislabeled clock is gone; existing self-tests green; one live receipt re-captured under the new fields. |
| `parallel` | yes — hosts-only surface; runs with everything. |

### A0 — the anti-prior guidance law (skills repo)
| Field | Value |
| --- | --- |
| `id` | `PGC-A0` |
| `outcome` | The operator's law as standing skill text: LLM training priors (millions of C/Python tensor kernels) push toward accumulator-variable loops and hand-rolled folds; Faber's constructs lower to per-target recipes (AIR intrinsics, `CollectionKernelPlan` tiles) that hand-rolled code can never reach. Named pattern families: counter-`while` → `for range` (n-ary for Cartesian walks); managed-binding folds → `.reduce`/`.map`/`.filter` closure intrinsics (`∴`); tensor reductions → from-family with `at`-clauses; best-index → argmax twins. Convert-or-record clause: a site with no covering construct stays, with an in-code reason. |
| `write_scope` | `~/work/ianzepp/skills/faber/canonical-faber/SKILL.md` (catalog entries); `~/work/ianzepp/skills/gpu-lessons/` (LLM-prior hazard row). |
| `done_when` | Both skills carry the law in their existing voice; committed in the skills repo; every later polish task card in this goal cites it. |
| `parallel` | yes — skills-repo-only; gates nothing but polish seats (A1+). |

### B-series — shape/capacity verticals (decode-dominant; packets; parallel with each other)
Each B unit: one defect, gradus kernel entries + its export pin + a device test proving the shape change, plus ONE paired-parity run on the fixed-1000 statue showing the per-step wall delta. Oracle per unit: wall moves, certified counts unchanged (1000/1000), no proba drift outside the touched module.

| `id` | Defect | Evidence anchor | Expected effect (from reports) |
| --- | --- | --- | --- |
| `PGC-B1` | Dynamic or bucketed attention length (stop splicing capacity 1100 into score/softmax shapes) | score_gemm 70,400 vs 4,864 elements; flat per-step walls | ~64 → ~50 ms/step (decode auditor estimate) |
| `PGC-B2` | T=1 decode GEMV/reduction specialization (stop 8× row overcompute at decode) | 8× T=1 GEMV row overcompute; T=1 8×8 matmul geometry | removes ~7/8 of decode GEMV FMA work |
| `PGC-B3` | KV write scaling + compact dynamic constants | capacity-scaled KV writes; full KV-arena append scans | trims per-step KV-side waste |

### C-series — prefill algorithmic verticals (packets; parallel with each other and B)
Same unit shape; oracle: ONE paired-parity prefill delta + per-kernel FMA/receipt evidence. Prefill is compute-bound — measure FMAs dispatched, not bandwidth.

| `id` | Defect | Evidence anchor | Expected effect |
| --- | --- | --- | --- |
| `PGC-C1` | Embedding as gather, not dense one-hot matmul | one-hot embedding matmul; direct token-row gather recommended | large share of 3.73B avoidable FMAs |
| `PGC-C2` | Terminal-row-only logits at prefill | all-36-row LM head vs 1 needed row | ~36× less lm_head prefill work |
| `PGC-C3` | Single-pass RMSNorm (no per-output-element row rescan) | O(D²) rescan, ~2.15B avoidable FMAs | removes ~2.15B FMAs |
| `PGC-C4` | Tiled GEMM recipes on prefill paths | scalar untiled 8×8 GEMMs, ~1.65B padded FMAs | removes padding waste; raises GPU-busy efficiency |

### A-series — purity polish waves (after A0; massively parallel batches)
| Field | Value |
| --- | --- |
| `id` | `PGC-A1..An` (batch per module: tokenizer, cache, math, block_verify, calibration, sampling, serialize, attention-host, …) |
| `outcome` | Convert hand-rolled loops and folds to language constructs per the A0 law; deterministic work list from `faber check --air --json` (ADMISSIBLE-ONE-AWAY rows first, then WOULD-REJECT triage) and WARN027 complexity rows; zero closure-intrinsic usage today is the starting count. Cross-references the kernel-purity-census campaign as the purity-definition owner. |
| `write_scope` | One gradus module (its `.fab` + `.proba`) per batch; packets; cheap seats welcome — the done-oracle is mechanical. |
| `done_when` | Batch: proba outcomes byte-identical (case path/status + stderr); WARN027 rows in the module drop to zero or each survivor carries an in-code reason; tier counts move (one-away → admissible) in the committed census rows; no semantic drift (no tolerance/order changes). |
| `fusion metric` | The L1 payoff is measured at the goal level: encoders per decode step (2,115 → target: hundreds) via AIR fusion absorbing pure leaves — re-measured after each landed A wave. |

### M-series — measurement checkpoints (Mind-owned, not units)
After each landed track: one AC paired-parity run (full stage) recorded
against the baseline of record; per-track attribution per L84. Expectation
ladder from the reports: B+A fusion lands decode plausibly ~10–15 ms/step
(~65–100 t/s); llama-class 4.3 ms requires every track. No synthetic
targets — the ladder is a hypothesis to be measured, not a promise.

## 5. Non-goals

No MIR-runner execution of anything (L86); no quantization work (f32 parity
is the contract); no CUDA arm (blocked on hosts need `411b16f3`, carried by
the parity goal); no llama.cpp changes (comparator is pinned); no new model
rungs (larger models are a later goal — this goal closes the 360M rung's
gaps and builds the method).

## 6. Sources (all six reports, on the Vivi record)

Prefill audit (GLM-5.3) mail `c1640a4e`; decode audit (GLM-5.3) mails
`ded525e1`/`02f34add`; fixed-1000 decode inspector (Luna) mail `c0c86fe4`;
fixed-1000 prefill inspector (Luna) mail `f6b12569`; short prefill inspector
(Luna) mails `06a62904`+`051731ac`; short decode inspector (Luna) mail
`b1c7f917`. Operator commentary 2026-08-27: fusion pre-work chain, the
anti-prior law, closure intrinsics, `--air`/`--complexity-budget` as
deterministic drivers.
