# Goal: perf-gap-closure — close the measured gradus-vs-llama parity gaps

**Status**: active — ADMITTED 2026-08-27 (terminal sweep f8861915 after repairs afdf79d/6f70767/0b1db1e; delivery frozen 0b1db1e; goal bd37d20 unchanged); wave 0 COMPLETE (D1 hosts 1ef244a: coverage 1024/2115 labeled, launch_encode_us + true submit_sync_us, mislabeled clock gone, live 1000-step receipt AC; A0 skills f7c2f7f: anti-prior law + L87); wave 1a: C2 folded (LM-head FMAs 1.70B→47.2M) + C5 folded (residency proven; RESIDUAL: full-stage C5 capture owed — RAM-disk eviction killed the run, route at measurement checkpoint); B2 closed residual (b8f48ff3): one-row T=1 dispatch landed (radix 8111e4f2f, hosts 9b7e4fb + 6f4284e lockfile, gradus evidence 09f72bd) — FMA census 3.31e9→4.14e8 met, wall FALSIFIED (fixed1000 decode 15.7→6.96 t/s, ratio 14.8→31.8), B2-RETUNE closed clean_pass (b12ac9a5): winner w16 landed (radix 51263402f, hosts 4d4c18e, gradus evidence 75dee06) — every width recovers (w8 16.34 / w16 16.44 / w32 16.21 / w64 16.28 vs 15.77 baseline; direct per-column body is the dominant repair); MIND DECISION: KEEP at width 16 (B2 FMA reduction stands with net decode gain; no revert); base reds repaired (hosts mapper pitch-truth = B1 harness-law mirror; kv_append pins kept as protocol truth — gradus pin lags post-B3 main by design, re-pin routed to reopen); CTO condition-A hold resolved (baseline family may re-key post-retune); B3 FOLDED (gradus d942388 KV appends via selected rows; radix cdd092995 export proof; hosts d195382 device test — device proof DISCHARGED (hosts f503b99: MetalHandleId fix, 4/4 green incl. arena lineage + position envelope); full-stage parity deferred to the post-B-series baseline family per append-only identity law); B1 FOLDED (radix d7c0be536+e4fd38849 style rider, hosts 4b0f250): decode attention work extents bucketed early-64/late-1088 at capacity 1100; radix suite 21 green; hosts dispatch proof 1000x4 both buckets; proba byte-identical; full-stage delta + physical gate owed at the post-B-series baseline checkpoint; A-series five of six landed: A2 27660dd, A3 75e3e33, A4 9085f48, A5 f5d0e1b, A6 b30812f (WARN027 tally across landed modules: sampling 1→0, math 4→2, cache 7→6, calibration 2→2, block_verify 6→6 — all survivors reasoned; closure intrinsics 0→N in every module); A1 tokenizer landed 974d7a6 — A-SERIES COMPLETE (6/6 modules; every module 0→N closure intrinsics, every WARN027 survivor reasoned, every proba tuple byte-identical); wave 1b queued (RAM); waves firing per operator parallel order — forged 2026-08-27 from the operator gap-analysis order (six inspection/audit seats: four Luna xhigh row inspectors + two GLM-5.3 phase auditors; reports cited below) and the operator running commentary (fusion pre-work, the anti-prior guidance law, closure intrinsics, deterministic drivers). Admission pending operator fine-tuning; no unit routed yet.
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

## 3. The guidance law and the fusion chain (operator commentary, 2026-08-27 — binding context for every unit)

**The law (strong guidance, written to override LLM training priors).** LLMs
have seen millions of C/Python softmax/rope/matmul/stride-walk kernels
written *without* language-level tensor constructs — accumulator variables,
`while`+`for` pairs, nested counter loops — because those languages have no
streamlined forms. That prior is wrong here. Faber's constructs put the lane
and thread into the loop itself (`sum from … at [i] thread f const s { }`),
walk Cartesian coordinates in ONE loop definition (`for range a‥b, c‥d
const i, j` — corpus `itera/range-product-n2.fab`), and fold via closure
intrinsics (`res.reduce((acc, x) ∴ acc + x, 0)`). The compiler lowers these
to per-target recipes (e.g. tensor `·` → `Collection(TensorMatMul)`
intrinsic + `CollectionKernelPlan::TiledMatMul`: threadgroup tiles,
barriers, zero-fill — chosen for the exact backend, CUDA/Metal/other). A
hand-rolled loop freezes one imperative shape and can never reach those
recipes. **Polish seats specifically hunt hand-rolled implementations and
convert them to language-level constructs; the compiler does a better job of
optimizing the shape for the target than the hand ever will.**

**Pattern-family targets (convert-or-record; a site with no covering
construct stays, with an in-code reason):**

| Hand-rolled prior | Faber construct |
| --- | --- |
| counter-`while` / managed counter walks | `for range` (n-ary for Cartesian; zip walks are `for from` series) |
| accumulator variable + loop (10 lines) | `.reduce((acc, x) ∴ expr, init)` — 1 line, no managed binding |
| transform loop building a new list | `.map(x ∴ expr)` |
| predicate loop with appends | `.filter(x ∴ pred)` |
| tensor reduction loops | from-family with multi-index `at`-clauses (`max from scores at [i, j]`) |
| best-index scan loops | `.argmax()` / `.argmin()` twins (LSR W0) |

**Measured starting point:** gradus uses closure intrinsics **zero times**
across `src/` while hand-rolled accumulators sit at `nn.fab:488`,
`train.fab:266`, `attention.fab:337/350/432`, `sampling.fab:458`, and
beyond; loop density: tokenizer 51 sites, cache 33, math 31, block_verify
28, calibration 26, sampling 24, serialize 23. Kernel bodies themselves are
largely modern already (`causal_softmax` = `max from … at [i,j] coalesce` +
`scores.softmax()`; zero `while` in `kernel.fab`/`math.fab`) — the debt is
host-side and older paths.

**The three skills define the refactor structure together:** `$faber`
(constructs + validation recipes), `$faber/canonical-faber` (anti-pattern
catalog — already cites gradus as bad examples: counter-`while` proven
across 15 files/~55 sites; the `tokenizer.fab _in_name` contains-loop), and
`$gpu-lessons` (measurement law: L84 decompose algorithm vs dispatch;
structural-change re-baseline). A0 writes the law into the first two as
standing text.

**The fusion chain and the machinery already waiting.** The pre-work thesis
is the kernel-purity-census campaign's own framing (operator fusion
directive, task `ed5144c7`): *"Purity is the prerequisite for fusion" —
typed, pure, small leaves mean fewer submissions, so fusion can erase
inter-kernel waits.* `dense-typed-assembly` defines the leaf law: the
compiler later fuses kernel leaves; fusion wants the leaves, not one
mega-kernel wrapping the split. On the radix side the machinery exists and
waits: `radix-air` carries a fusion-table side-channel for fused-kernel
lowering and `to_mir.rs` already absorbs fused groups (only the group root
is lowered). The measured L1 loss (2,115 serialized single-kernel encoders,
~1,440 of them per-head pieces averaging 11.6 µs GPU work —
`per-head fragmentation` per the prefill audit; llama runs one reused
graph) is exactly what that chain exists to erase. Track A executes the
purity prerequisite; the fusion payoff metric is encoders per decode step.

**Deterministic drivers (the work list comes from the machine, not vibes).**
`faber check --air --json` emits tier-labeled rows — `ADMISSIBLE-ONE-AWAY`
is the ranked fusion-candidate queue (one refactor from kernel
admissibility), `ADMISSIBLE-KERNEL` is the consumable-now set, `WOULD-REJECT`
is the honest far set polish turns must not waste on. `faber check` also
emits WARN027 `complexity_budget_exceeded` (`--complexity-budget` default
12 from the census p95=11 over 2,393 fns; `--kernel-complexity-budget`
default 2 — the 84 kernel-marked fns already max at 2, so hotspots are
host-side). Both surfaces are report-only by design: THIS goal owns the
enforcement moment — progress is measured as tier counts moving in
committed census rows and WARN027 rows falling per module, never as a gate
the polish has to fight. LSR campaign wave 6 (functional-intrinsic adoption
sweep) is the language-surface sibling of the A-series; its rulings apply.

## 4. Parallelism architecture (the operator's structural requirement)

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

## 5. Units

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
| `PGC-C1` | Embedding as gather, not dense one-hot matmul — **SUPERSEDED 2026-08-28 by `PGC-R1` (delivery §7.0); do not dispatch as written** | one-hot embedding matmul; direct token-row gather recommended | large share of 3.73B avoidable FMAs |
| `PGC-C2` | Terminal-row-only logits at prefill — folded 2026-08-27; producer-fact verification owned by `PGC-R2` (delivery §7.4) | all-36-row LM head vs 1 needed row | ~36× less lm_head prefill work |
| `PGC-C3` | Single-pass RMSNorm (no per-output-element row rescan) — **SUPERSEDED 2026-08-28 by `PGC-R5`; do not dispatch as written** | O(D²) rescan, ~2.15B avoidable FMAs | removes ~2.15B FMAs |
| `PGC-C4` | Tiled GEMM recipes on prefill paths — **SUPERSEDED 2026-08-28 by `PGC-R4`; do not dispatch as written** | scalar untiled 8×8 GEMMs, ~1.65B padded FMAs | removes padding waste; raises GPU-busy efficiency |
| `PGC-C5` | Stop re-staging weight-shaped inputs — folded; owed capture + evidence dir owned by `PGC-R3` (delivery §7.4) | 23 MB of weight-shaped inputs re-staged per prefill step (prefill audit) | removes redundant staging bytes and its encode-adjacent wall |

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

## 6. Non-goals

No MIR-runner execution of anything (L86); no quantization work (f32 parity
is the contract); no CUDA arm (blocked on hosts need `411b16f3`, carried by
the parity goal); no llama.cpp changes (comparator is pinned); no new model
rungs (larger models are a later goal — this goal closes the 360M rung's
gaps and builds the method).

## 7. Sources (all six reports, on the Vivi record)

Cross-family confidence: the Luna and GLM seats independently converged on
every major claim (encoder counts, serialization, capacity family,
instrument defects) and independently corrected the same two provisional
errors (the partial-sample bubble figure; the prefill bandwidth-floor
misapplication) — the two-dimension cross-comparison the operator ordered
did its job.

Prefill audit (GLM-5.3) mail `c1640a4e`; decode audit (GLM-5.3) mails
`ded525e1`/`02f34add`; fixed-1000 decode inspector (Luna) mail `c0c86fe4`;
fixed-1000 prefill inspector (Luna) mail `f6b12569`; short prefill inspector
(Luna) mails `06a62904`+`051731ac`; short decode inspector (Luna) mail
`b1c7f917`. Operator commentary 2026-08-27: fusion pre-work chain, the
anti-prior law, closure intrinsics, `--air`/`--complexity-budget` as
deterministic drivers.
