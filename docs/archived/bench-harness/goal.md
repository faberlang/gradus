# GOAL: bench-harness — repeatable gradus bench pinned to the radix+hosts+gradus triple, with committed baselines

**Status**: done — closed 2026-08-27 by end-of-goal audit `e3c9cd4a` (CLEAN PASS: requirements 1–4 satisfied; acceptance 1–9 traced to receipts with the critical gate paths independently re-proven — checker self-compare, wrapper green/red, all four NOT COMPARABLE refusals at exits 3/4/5/6; all 17 work+fold hashes verified; machine audit 0 findings). Eight units landed across folds `f85272b`/`f2d3595`/`19937dc`/`c3bb796`/`4158a2b`/`15c643e`/`533121e`/`a8c0182`. Baseline of record: `baseline-20260827-re792964-hc9cfb5a-g536b7ab` (+receipt +reproduction rider; noise floor ~±1% AC). Residuals: gate advisory until the operator wires it; battery-labeled captures legal, never the first baseline. The gradus polish wave is OPEN on this record.
**Created**: 2026-08-27
**Campaign:** `—` (standalone; operator pause-exception order 2026-08-27 morning, task `076e7a1a`)
**Source:** operator order (verbatim requirements 1–4 in §Problem); routed by mind task `076e7a1a`
**Amended:** 2026-08-27 — audit `c4f621fa` fix pass: operator perf-taxonomy folded (addendum mail `46ab4e94`, delivered via mind task `06a9cf0b`; §Perf-taxonomy), scratch-worktree teardown added to the pin driver, baseline-capture ordering invariant pinned
**Amended:** 2026-08-27 — stage-ladder amendment (operator rulings, mind mails `1309af45` + `88895a02` + `d3cc0123`; planner task `8add67c0`): §Stage ladder added (scripta/test-model stages smoke/dev/rough/full; full 3/10/7-label protocol byte-preserved as the top stage; default dev mode = stage 2), unit GB-U3b added, GB-U4/GB-U5 ordering invariant extended to the ladder, GB-U6 law extended
**Amended:** 2026-08-27 — per-row power-state amendment (operator ruling 4, mind mail `ea4dd0a3`, extends `1309af45`/`88895a02`/`d3cc0123`; planner task `4f87b663`): §Environment-identity gains the per-row power-state law (row-level `power_state` sampled at each row's execution; `metadata.power_class` run summary with honest mixed semantics; §Output-format row example extended), §Stage-ladder comparability rules gain power-class stratification (cross-class NOT COMPARABLE; per-class ratio law), §Threshold policy keyed on `power_class`, unit GB-U3c added (capture) with GB-U4 (wrapper stratified refusal) re-gated on it, acceptance 9 added. The AC gate on the first baseline capture is NOT rescinded.

Ruling 3 reconciliation (mail `d3cc0123`, folded via planner resume before
commit): the ladder now exposes BOTH knobs — label breadth × repetition
count — per stage. Stage 3 was redefined from a 6-compute-label focused
subset to the full-breadth rough pass of ruling 3 (all 7 labels at 1 warmup
+ 2 samples, ~7–8 min): a rough t/s for every test, because dev-time signal
is order-of-magnitude difference, which 1–2 reps catch. The old focus stage
is retired (it never landed): its breadth use is strictly dominated by the
rough pass (7 labels at under half its wall), and its subset-depth use
remains available via `--label <set>` at the selected stage's sampling
(iteration-signal only). A fifth token was rejected — ruling 2 mandates the
stages-1–4 mirror, and the old focus added no capability the two knobs do
not already cover. Statistical reliability stays reserved for the top
stage, byte-preserved 3/10.
**Repos:** primary: `gradus/` (writes gradus-only); read-only pinned inputs: `radix/`, `hosts/`
**Related:** `gradus/docs/benchmark-method.md` (v1.0.0 — amended by this goal to v1.1.0); `radix/scripta/check-benchmark-regression.py` (gate consumer, read-only); `radix/docs/factory/perf-parity-baseline/` (receipt + battery-ruling precedent); `~/work/ianzepp/skills/gpu-lessons/` (measurement laws, cited not duplicated); `gradus/docs/factory/kernel-purity-census/` (the perf work that needs this harness)

---

## Invariant

Every gradus performance number committed to this repository is reproducible
from exactly three commit hashes — radix, hosts, gradus — plus the recorded
environment identity, and is comparable through the existing
`check-benchmark-regression` gate without a new format.

## Problem

Operator order, 2026-08-27 morning (pause exception #3), verbatim
requirements:

1. A repeatable bench harness recording performance attached to the most
   recent commit of all three relevant repos: radix, hosts, gradus.
2. Future benchmarks must be reproducible from just those three commit
   hashes.
3. The benchmark numbers are committed inside gradus — part of the library
   history.
4. The process is recorded in the gradus AGENTS.md file.

Evidence that this is a real gap, not aspiration:

- `gradus/docs/benchmark-method.md` v1.0.0 (PML6-U4, 2026-08-11) pins a
  sampling *protocol* but explicitly states "No committed bench binary lands
  in this phase" (Open Question 5) and "No sample from this protocol is
  published". No numeric baseline exists anywhere in gradus.
- Timing claims in the live record live in prose receipts tied to single
  runs (e.g. `kernel-purity-census/wave-1-delivery.md` operator-provenance
  paragraph citing task `ed5144c7` and receipt `4bce158c9`; perf-parity U5
  queue_wait 210ms/step attribution) — none reproducible by command from a
  committed pin.
- The kernel-purity campaign is actively reshaping the hottest gradus
  surfaces (carrier → typed static-shape entries) with a standing
  instruction that purity is the prerequisite for fusion; there is no
  committed before/after numeric instrument to hold that work honest
  (gpu-lessons L17: re-census after a structural change).
- gpu-lessons L4 (FM-49): a number existing only in mail or /tmp is a
  claim; the receipt must be committed with the code. Gradus currently has
  no such committed receipts.

## Proposal

A bench harness in `gradus/scripta/` that (a) materializes the three repos
at three given hashes into a scratch root outside all repositories
(detached git worktrees), (b) builds a release `faber` binary from the
pinned radix, (c) runs a small fixed inventory of `.fab` bench cases
through the MIR runner (`faber run` — interpreted execution, no Cargo on
the package), (d) emits checker-compatible JSON, and (e) commits dated,
3-hash-suffixed baselines with full environment-identity metadata inside
gradus. The process law lands in `gradus/AGENTS.md`.

### Pin mechanics (design input, resolved)

| Concern | Decision |
| --- | --- |
| Materialization | `git worktree add --detach` from the existing sibling checkouts into a scratch root **outside every repo**, default `<workspace>/.bench/gradus/<r7>-<h7>-<g7>/` (workspace root is not a git repo; no ignore churn). Never clones (quarantine law), never writes tracked content inside `radix/`, `hosts/`, or the main `gradus/` checkout. Honest caveat: registering a linked worktree writes admin metadata under each source repo's `.git/worktrees/` — so `scripta/bench clean` tears every scratch triple down (`git worktree remove --force` per worktree, `git worktree prune` in each source repo, then scratch-root removal); registrations and multi-GB checkouts never accumulate. |
| Binary | `cargo build --release -p faber` inside the pinned radix worktree, its own Cargo target (cargo-isolation law; never share `CARGO_TARGET_DIR`). Release profile: a debug binary would measure debug codegen; profile recorded in metadata. |
| Library resolution | `FABER_LIBRARY_HOME=<scratch-root>` so `gradus:*` imports resolve to the pinned gradus worktree (same seam `scripta/check-compile` uses; `faber doctor` proves it). |
| Hosts role | Recorded in the pin and in every baseline name. The MIR-runner arm does not link hosts crates; the hash is still part of the reproducibility law because the triple is the unit of record, and any future device/compiled arm (open question 3) consumes hosts via `FABER_SUPPORT_PATH_OVERRIDE` path deps (`radix/crates/faber/src/package/runtime_sources.rs` — the offline seam that replaces branch-pinned git sources with container-local checkouts). |
| Case source on reproduction | The harness itself and the bench cases live in gradus, so a reproduction run invokes `scripta/bench` **from the pinned gradus worktree** — cases, manifest, and harness are all at the recorded gradus hash. The main-checkout invocation is the dev path. Ordering invariant: the recorded `gradus_sha` must **already contain the complete harness** — capture runs only after the harness + case commits land, and verifies the recorded hash resolves `scripta/bench` with the full subcommand set before writing the baseline; the reproduction proof cites that hash as harness-complete. |
| Run loop | Per case: 3 discarded warmups, 10 measured samples (benchmark-method §4.3 protocol, unchanged), each sample = wall time of `faber run` over an in-case fixed-iteration loop (K per case from the manifest, calibrated so op time dominates process startup; K recorded per case in the baseline). Report min/median/max; `median_ms` per label is the gate quantity (checker contract unchanged). Timer: portable wall clock. Runtime caps (`cap_s` per case, default 60) are **safety circuit breakers, never metrics and never pass/fail**: a capped sample still records its valid throughput (units produced / min(elapsed, cap)) plus a `capped: true` marker; completion under the cap is not a performance datum. The 3/10/7-label shape is the **stage-4 (full)** protocol (§Stage ladder); dev iteration runs the cheaper ladder stages. |
| Baseline naming | `gradus/bench/baselines/baseline-YYYYMMDD-r<radix7>-h<hosts7>-g<gradus7>.json` + same-stem `.md` receipt. Append-only: a new triple gets a new file; an existing baseline is never edited (library history, requirement 3). |
| Execution route | `faber run` (MIR interpreter, feature `runner`) — package route, not single-file scripts (kernel imports in staged scripts fail PKG001; `scripta/check-compile` documents the same constraint). One bench package, main dispatches on a label argument; `--`-args pass-through is the exempla precedent. |

### Output format (design input, resolved)

The exact shape `radix/scripta/check-benchmark-regression.py` already
accepts, following the committed convention
`radix/docs/benchmarks/baseline-2026-07-27.json`:

```json
{
  "format_version": "1",
  "metadata": { "…": "environment identity, see below" },
  "results": [
    { "label": "gemv.f32.320x960", "median_ms": 0.0, "min_ms": 0.0,
      "max_ms": 0.0, "samples": 10, "iterations": 25, "ok": true,
      "class": "fixed-oracle", "work_unit": "<manifest-defined>",
      "units_per_sample": 0, "median_units_per_s": 0.0, "capped": false,
      "power_state": "ac" }
  ]
}
```

The checker reads only `format_version`, `results[].label`, and
`results[].median_ms`; extra fields compose — including the per-row
`power_state` field (`ea4dd0a3`): the checker is power-blind by
contract, and the gradus gate wrapper owns every power-class refusal
(§Per-row power-state law). Gate: exit 0 pass / exit 1 regress; default
threshold 10 %, overridable via `BENCH_REGRESSION_THRESHOLD` (checker's
own contract, unchanged).

### Environment-identity metadata (design input, resolved)

Every baseline `metadata` block carries, missing-any-voids-the-claim
(benchmark-method §5 discipline, extended):

| Field | Source |
| --- | --- |
| `timestamp` (UTC), `hostname`, `machine_model`, `cpu`, `cores`, `memory`, `os`/`kernel`, `arch` | `sysctl`/`sw_vers`/`uname`/`hostname` — the gi0 run-metadata precedent (`radix/docs/factory/gpu-inference-gguf/gi0-inventory.md` §277; `trials` harness `run_metadata.py`) |
| `power_state` (AC/battery + charge % + powermode), `pmset_raw`, `power_class` | `pmset -g batt` / `pmset -g`. **Per-row power-state law (`ea4dd0a3`)**: every result row carries `power_state` sampled at that row's execution; `metadata.power_state` (descriptive string) is the start-of-run point observation only; `metadata.power_class` is the run summary (§Per-row power-state law). **Battery ruling applies to absolute numbers**: a battery capture's absolutes are depressed and are NOT steady-state claims; ratio-is-signal per class (perf-parity soak receipt `environment_note`; §Per-row power-state law). Non-macOS records `unavailable` and is not gate-comparable. |
| `triple` (`radix_sha`, `hosts_sha`, `gradus_sha` — full SHAs) | requirement 2 |
| `faber_binary` (profile, rustc version, build command) | binary identity, benchmark-method §5 |
| `protocol` (warmups=3, samples=10, per-case iterations, timer) | §Run loop above |
| `citations` (benchmark-method version, gpu-lessons law ids, battery-ruling handle) | cite, never duplicate |

### Per-row power-state law (operator ruling `ea4dd0a3`, resolved)

Operator ruling 4 (2026-08-27): the harness must capture, for each test
it runs, whether the machine was on battery or AC — a per-result-row
`power_state` field sampled at that row's execution, not only the
run-level metadata label. Motivation includes mixed-power runs: a 31-min
full sweep can span a plug-in transition, so the run-level label can
misdescribe later rows; per-row capture makes battery data honestly
usable via stratification instead of discarded.

Field shape (additive; checker-untouched; protocol and K unchanged):

- `results[].power_state` ∈ `ac | battery | mixed | unavailable`,
  sampled at that row's execution: one probe immediately before the
  row's first warmup and one immediately after its last measured
  sample. Probes agreeing → that class; disagreeing → `mixed` (a point
  sample that can misdescribe its own row is the run-label's defect one
  level down — avoided). Non-macOS → `unavailable`. Every stage of the
  ladder emits the field (smoke through full); the 3/10/K protocol is
  untouched and K stays fixed on every stage.
- `metadata.power_state` (existing descriptive string: class + charge %
  + pmset-verified) is now defined honestly as the **start-of-run point
  observation** — kept for continuity with the landed GB-U3 evidence,
  never a claim about later rows.
- `metadata.power_class` ∈ `ac | battery | mixed | unavailable` is the
  **run summary the law keys on**: the unanimous row class when every
  row agrees, else `mixed`; when mixed, `power_class_first` and
  `power_class_last` record the first and last row classes. A
  unanimous-battery run is a battery run — honestly labeled, never
  discarded.

Comparison law (extends the §Stage-ladder comparability rules):

- **Stratify per test by power class.** A test's AC rows compare
  against that test's AC rows across runs; battery against battery.
  Cross-class comparison is **NOT COMPARABLE** — the same refusal family
  as environment mismatch and lesser-stage protocol. Rows that are
  `mixed`, `unavailable`, or missing the field compare against nothing
  (fail closed: a row-field-less JSON is treated as unavailable-class
  and refused, never silently comparable).
- **Gate grade vs signal grade.** The gate wrapper (GB-U4) requires
  whole-file unanimity: both sides' `metadata.power_class` ∈ {ac,
  battery} and equal, else `NOT COMPARABLE` before the checker runs.
  Per-test stratified row comparison (AC vs AC, battery vs battery,
  across runs) is legitimate recorded signal in receipts — never a gate
  mode in v1.
- **Per-class ratio law.** As long as gradus and a comparison side
  (llama, in the future parity harness) run the SAME test on the SAME
  power class, their ratio/difference is valid signal even on battery —
  the perf-parity ratio-is-signal precedent extended per class. Battery
  absolutes stay depressed, never steady-state claims; the ratio
  carries.
- **AC gate on the first baseline — NOT rescinded.** GB-U4 done_when
  (a) still requires AC for the first baseline capture; a battery
  capture is battery-labeled per this law and is valid evidence, but it
  is not the first baseline.

Measurement laws that govern (gpu-lessons, canonical
`~/work/ianzepp/skills/gpu-lessons/`, laws in `references/laws.md`):
L1 (a gate never seen red is unfalsifiable — the red path is proven in
delivery), L2 (state which path carries the number; here always the
MIR-runner product path, telemetry off), L4 (receipt committed with the
code), L12/L13 (decompose the wall; process-startup share is named and
amortized by K, never hidden), L17 (re-census after structural change —
the re-baseline trigger), L21 (never widen a threshold after an
observation to force green).

### Case inventory (design input, resolved — first baseline, 7 labels)

Hot gradus surfaces at the GEA tell-tale sizes
(`gradus/docs/module-map.md` §kernel; GEA receipts in
`radix/docs/factory/gpu-execution-architecture/`). Public `gradus:*`
surface only; each case prints a non-trivial value check line (FM-5/L1:
no zero-artifact greens).

| Label | Surface | Shape (tell-tale source) |
| --- | --- | --- |
| `carrier.elementwise.add.f32.320x960` | `gradus:math` elementwise on `tensor.NumericBlock` (carrier seam) | `[320,960]` F32 (GEA1 GEMV width) |
| `carrier.reduce.sum.f32.320x960` | reduction over a carrier block | `[320,960]` F32 |
| `gemv.f32.320x960` | matmul/GEMV public surface | GEA1 `[320,960]` |
| `block.matmul.f32.t8.d960.f2560` | block matmul (GEA2 entry shape) | T=8, D=960, F=2560 |
| `decode.attention.row76.d960` | attention row op | GEA3-U3a T=1, L_max=76 |
| `prefill.attention.rows36.l76.d960` | prefill-shaped attention/reduction | GEA3-U3b T_p=36, L_max=76 |
| `check.library.compile` | `faber check` wall on the gradus library package | benchmark-method §2 workload 1; exercises the pinned radix compiler |

Substitution rule: if a named surface is device-admission-only and cannot
execute on the MIR runner, the Hand substitutes the nearest public carrier
surface at the same shape and records the substitution in the baseline
receipt — it never silently drops a label.

### Perf-taxonomy (operator addendum, resolved — mail `46ab4e94`)

Operator perf-taxonomy addendum 2026-08-27 (delivered to planner via
mind task `06a9cf0b`) defines two test classes and one metric law.
Disposition:

- **Class (a) fixed-oracle — FITTING, folded.** Every v1 case is
  fixed-oracle: a fixed computation run to completion. Each case-manifest
  entry gains `class` + metric fields: `class` (always `fixed-oracle` in
  v1), `work_unit` (what one unit is) + `units_per_iteration`, and
  `cap_s` (default 60). Decode/prefill cases (`decode.attention.row76…`,
  `prefill.attention.rows36…`) count **tokens** as the unit; kernel
  cases define their fixed work unit and its throughput label (unit
  name, Hand-defined and recorded in the manifest); a case whose unit is
  a single pass (`check.library.compile`) sets `units_per_iteration: 1`.
  Sole throughput metric: **t/s = unit-count / min(completion, cap)** —
  per sample, units produced (K × `units_per_iteration`) divided by
  min(sample wall, `cap_s`); median across samples. The 3/10 wall-time
  protocol stays the instrument and `median_ms` stays the checker's gate
  quantity (format unchanged, extra fields compose); the t/s fields are
  the published performance numbers.
- **Runtime caps — circuit breakers only.** A cap bounds a runaway
  sample; it is never a metric and never pass/fail. A capped sample
  records its valid t/s plus `capped: true`; the run does not fail, and
  no gate reads the marker.
- **Class (b) fixed-output-length — NOT FITTING this harness (recorded
  ruling).** Class (b) benches a prompt with a known expected output
  (~1000-token cap, ~5m) and carries **per-side expected token counts**
  because gradus and a llama side tokenize the same text differently.
  This is a solo gradus harness over fixed computations: there is no
  second tokenizer side, so an expected-output token count has nothing
  to be per-side *about* — forcing class (b) here would fabricate an
  expected-token oracle the harness cannot ground. Class (b) belongs to
  the gradus-v-llama parity harness when one is ordered. The t/s law and
  caps-as-breakers law above still carry into the AGENTS.md law (GB-U6)
  so that future harness inherits them correctly.

### Stage ladder (operator rulings 2026-08-27 — mails `1309af45` + `88895a02` + `d3cc0123`, resolved)

Operator rulings (2026-08-27, while GB-U3's full sweep ran at 35–40 min):
bench runs used during development must execute exactly one or two tests,
minutes at most (target ~2–3 min wall) as the default dev mode; the harness
must be a staged ladder modeled on `radix/scripta/test` stages 1–4 — earlier
stages very fast, progressing into slower and more thorough — so iteration
never waits on the full sweep; the ladder must control repetition count per
stage, not just label breadth — the fast stage may run the FULL 7-label
corpus at 1–2 repetitions per test (rough t/s for every test; dev-time
signal is order-of-magnitude difference), while statistical reliability is
reserved for the top stage. The full 3-warmup/10-sample/7-label protocol is
**byte-preserved unchanged as the top stage** (baseline-capture and
reproduction mode). Disposition — a four-stage ladder on `scripta/bench
run`, cheap-first law mirrored from `radix/scripta/test`, both knobs per
stage:

| Stage | Token(s) | Label set (breadth) | Warmups | Samples (reps) | Expected wall | Purpose |
| --- | --- | --- | --- | --- | --- | --- |
| 1 smoke | `--stage smoke` / `--stage 1` | 1 label — manifest `smoke_label` (default `gemv.f32.320x960`, cheapest measured) | 1 | 3 | ≤ 1 min (measured ≈ 45 s + overhead) | wiring smoke: pin → build → run → emit end-to-end; iteration-signal only |
| 2 dev **(default)** | `--stage dev` / `--stage 2` | 2 labels — manifest `dev_labels` (default `gemv.f32.320x960` + `carrier.reduce.sum.f32.320x960`) | 1 | 3 | ~2–3 min (measured est. ≈ 2 m 20 s + overhead) | the operator fast path: default dev mode, iteration signal while developing; iteration-signal only |
| 3 rough | `--stage rough` / `--stage 3` | all 7 labels | 1 | 2 | ~7–8 min (measured arithmetic: 3 × ≈ 144.2 s ≈ 7.2 min + overhead) | full-breadth rough pass (`d3cc0123`): a rough t/s for every test; order-of-magnitude signal across the whole inventory; iteration-signal only |
| 4 full | `--stage full` / `--stage 4` / `--full` | all 7 labels | 3 | 10 | 35–40 min (measured; full-sweep log 2026-08-27) | statistical-reliability stage: full sweep, baseline-grade capture (GB-U4) + reproduction (GB-U5); the **only** gate-comparable shape |

Laws (mirroring `radix/scripta/test`'s cheap-first discipline):

- **Explicit stage selection.** `run` takes `--stage <token>` (name or
  number: `smoke|dev|rough|full` ≡ `1|2|3|4`; `--full` aliases stage 4).
  `--label <label>` (repeatable) selects an explicit label subset at the
  selected stage's sampling (stage-2 sampling when no stage is given).
  **Default (no flags) = stage 2 dev** — the operator ruling names the
  1–2-label fast path as the default dev mode, a deliberate deviation
  from scripta/test's default-to-cheapest (the wiring smoke is not the
  dev loop).
- **Two knobs, monotonic total cost.** Each stage is strictly more
  expensive in expected total wall than the one before it
  (≈ 45 s → ~2–3 min → ~7–8 min → 35–40 min). Label breadth is
  non-decreasing (1 → 2 → 7 → 7); repetition depth is the second knob
  (`d3cc0123`) and statistical depth (3 warmups / 10 samples) is
  reserved for the top stage — no lower stage's per-label protocol
  exceeds it.
- **Iteration policy — K fixed across the ladder (t/s math preserved).**
  Rulings `88895a02` and `d3cc0123` both permit per-case in-case
  iterations K to shrink per stage only where the t/s math is preserved
  (units-per-sample recomputed from the actual K). This ladder never
  exercises that permission: every stage meets its wall bar at the
  manifest K (now proven by measurement — all seven per-sample walls are
  measured), and fixed K keeps units-per-sample identical across stages,
  so per-sample t/s needs no per-stage reconciliation. Shrinking K on
  any stage requires a new amendment naming the stage and the recomputed
  unit fields.
- **Stage identity in output.** Every stage's JSON carries additive
  metadata: `stage` (name), `stage_number`, and the run's actual
  warmup/sample counts in `metadata.protocol`. The checker reads only
  `format_version` / `results[].label` / `median_ms` — extra fields
  compose; no checker change.
- **Comparability rules (checker), keyed on protocol identity.** Only
  JSON whose recorded protocol is exactly the full shape — stage full,
  warmups 3, samples 10, all 7 manifest labels — is gate-comparable:
  eligible as baseline capture and as gate input. Everything else —
  lesser stage, explicit `--label` subset, any samples/protocol override
  — is **iteration-signal only**: the GB-U4 gate wrapper refuses it
  (`NOT COMPARABLE`, the same refusal family as the environment
  mismatch) before the checker runs. Same-stage / same-shape comparison
  (e.g. rough vs rough, before/after a change) is legitimate recorded
  signal and never gates. Checker self-compare (same file on both sides)
  remains valid format evidence for any stage.
- **Power-class stratification (`ea4dd0a3`), same refusal family.** On
  top of protocol identity, gate comparability requires power-class
  identity: both files' `metadata.power_class` ∈ {ac, battery} and
  equal. Cross-power-class comparison is **NOT COMPARABLE** (refused
  before the checker runs); `mixed`/`unavailable` runs and
  row-field-missing files are refused fail-closed. Per-test stratified
  comparison (AC rows vs AC rows, battery vs battery, across runs) is
  recorded signal only (§Per-row power-state law). The per-class ratio
  law makes same-test same-class gradus-vs-llama ratios valid signal
  even on battery.
- **Pre-release depth (10–20 reps class) — deferred.** No `--samples`
  override ships in GB-U3b. If deep pre-release verification is ordered
  later, it lands as an explicit `--samples N` override on `run`,
  signal-only by the comparability law above (the wrapper refuses
  anything whose recorded protocol is not exactly 3/10 × 7 labels); the
  capture/reproduction path stays 3/10 byte-preserved (`88895a02`).
- **Measured context** (per-sample walls, full-sweep log 2026-08-27,
  radix `9c90249` hosts `c9cfb5a` gradus `f2d3595`, RUN_EXIT 0): gemv
  ≈ 11.3 s · block.matmul ≈ 23.5 s · carrier.reduce ≈ 24.3 s · prefill
  ≈ 26.4 s · carrier.elementwise ≈ 28.4 s · decode ≈ 29.1 s ·
  check.library.compile ≈ 1.22 s. Six compute labels ≈ 143.0 s per
  full pass; all seven ≈ 144.2 s. Rough = 3 passes ≈ 7.2 min; full
  ≈ 31 min run time + overhead = 35–40 min.

### Threshold policy (design input, resolved)

- Gate default 10 % (the checker's own default). Same machine AND same
  power class required — the checker is machine- and power-blind, so
  the gradus gate wrapper refuses comparison on environment-identity
  mismatch or power-class mismatch (`metadata.power_class` not both
  {ac, battery} and equal — `NOT COMPARABLE`, distinct exit) before the
  checker ever runs (§Per-row power-state law).
- First generation is advisory: the gate is demonstrated green and red,
  but gradus merges are not blocked on it until the operator wires it.
- Re-baseline = new committed file at a new triple (append-only). L21:
  thresholds are never widened after an observation to force green; a
  same-machine regression beyond threshold is recorded and investigated
  (L17), not suppressed.

### AGENTS.md law (design input, resolved)

New `## Benchmarks` section in `gradus/AGENTS.md` recording: the 3-hash
reproducibility law; the run command (`./scripta/bench …` with
subcommands, `clean` teardown included); where baselines live and the
append-only rule; the environment-identity + battery-ruling requirement;
the threshold policy; the stage ladder (both knobs: label breadth × repetition count; default dev mode = stage 2, one–two labels, ~2–3 min; stage 3 = full-breadth rough pass at 1–2 reps, ~7–8 min; `--stage` tokens smoke/dev/rough/full; the full 3/10 protocol is the top stage and the only gate-comparable shape; lesser stages and any protocol override are iteration-signal only); the per-row power-state law (row-level `power_state` sampled at each row's execution; `metadata.power_class` run-summary semantics with honest mixed handling; stratified comparison — cross-class NOT COMPARABLE; per-class ratio-is-signal even on battery, perf-parity precedent; AC-gated first baseline — `ea4dd0a3`); the metric law (t/s = unit-count /
min(completion, cap) is the sole throughput metric; runtime caps are
safety circuit breakers, never metrics, never pass/fail); the class-(b)
not-fitting ruling (fixed-output-length + per-side expected counts are
parity-harness territory — §Perf-taxonomy); citations
(benchmark-method v1.1.0, gpu-lessons, perf-parity U7).
`docs/benchmark-method.md` bumps to v1.1.0 recording the harness (its §6
"no benchmark binary" line is superseded by the operator order; version
bump + delta per its own §7).

### Non-goals

- No GPU/device-arm benchmarking. Device throughput is NGAB's
  (benchmark-method §1); device/backend execution routes stay out of v1.
- No compiled-Rust-carrier arm (needs the `faber` runtime crate — a fourth
  input; open question 3).
- No changes to `radix/` or `hosts/` — pinned read-only inputs, checked
  out at hash, built, driven.
- No performance optimization of gradus itself; the harness measures, it
  does not fix.
- No CI wiring; scripta is the dev-side surface (gradus has no CI gates).
- No class-(b) fixed-output-length cases — not-fitting ruling
  (§Perf-taxonomy): per-side expected token counts need a second
  tokenizer side; that is the gradus-v-llama parity harness, not this
  solo harness.
- No new tolerance envelopes or numeric-contract changes (gpu-lessons
  L20–L24 territory, untouched).

## Ground truth researched

| Claim | Artifact |
| --- | --- |
| Checker contract (`format_version` + `results`, `median_ms` per label, 10 % default, `BENCH_REGRESSION_THRESHOLD`, exit 0/1, machine-blind) | `radix/scripta/check-benchmark-regression.py:34-38,92-99,148,174` |
| Committed benchmark-JSON convention to copy | `radix/docs/benchmarks/baseline-2026-07-27.json` (`format_version:"1"`, `metadata`, `results[].median_ms/p10/p90/ok`) |
| Sampling protocol (3 warmups / 10 samples / wall clock / min-median-max) | `gradus/docs/benchmark-method.md` §4.3 |
| Battery ruling (power state recorded; battery absolutes depressed, ratio-is-signal) | `radix/docs/factory/perf-parity-baseline/evidence/2026-08-26-metal-m5max-soak-l2000/perf-parity-receipt-v1-2026-08-27-soak.json:118,836`; U7 status clause in `perf-parity-baseline/goal.md:3` |
| gpu-lessons measurement laws | `~/work/ianzepp/skills/gpu-lessons/SKILL.md` + `references/laws.md` (L1, L2, L4, L12, L13, L17, L21) |
| GEA tell-tale sizes | `gradus/docs/module-map.md` (GEA1 `[320,960]`; GEA2 T=8/D=960/F=2560; GEA3-U3a T=1, U3b T_p=36, L_max=76; U3c head `[V,960]`) |
| MIR-runner execution route (`faber run`, package route, args pass-through, no Cargo) | `radix/crates/faber/src/commands/run.rs:1-60`; receipts `faber run --target fmir exempla/… --` in `gradus/docs/factory/production-ml-library/` |
| Offline path-dep seam for support crates (hosts by path instead of branch-pinned git) | `radix/crates/faber/src/package/runtime_sources.rs:17-21` (`FABER_SUPPORT_PATH_OVERRIDE`) |
| Library-home seam (`FABER_LIBRARY_HOME`, `faber doctor`) | `gradus/scripta/check-compile`; faber CLI `Doctor` |
| Single-file scripts reject kernel imports (package route required) | `gradus/scripta/check-compile` header comment (PKG001); `gradus/scripta/check-factory-goal-status` staging workaround |
| Shipped surface is `src/` only — `bench/` and `scripta/` never ship | `gradus/cista.toml` (`interfaces = "src"`) |
| `check-source` scans `src/` only — bench cases cannot trip it | `gradus/scripta/check-source:4` |
| Current triple (2026-08-27) | gradus `4488598` · radix `9dc17410d` · hosts `c9cfb5a` |
| Perf-taxonomy addendum (two classes; t/s sole metric; caps as circuit breakers; per-side expected counts) | operator mail `46ab4e94` (2026-08-27 12:21 UTC), delivered to planner via mind task `06a9cf0b`; disposition §Perf-taxonomy |

## Reference packet (paths/commands to inspect)

- `radix/scripta/check-benchmark-regression.py` — the gate this composes with
- `radix/docs/benchmarks/*.json` — format precedent
- `gradus/docs/benchmark-method.md` — protocol authority (this goal amends it)
- `gradus/scripta/check-compile`, `gradus/scripta/check-factory-goal-status` — env-seam and binary conventions
- `radix/crates/faber/src/commands/run.rs`, `radix/crates/faber/src/package/runtime_sources.rs`
- `~/work/ianzepp/skills/gpu-lessons/references/laws.md`
- `radix/docs/factory/perf-parity-baseline/` — receipt + battery ruling

## Constraints and invariants

- Writes gradus-only. radix and hosts are pinned read-only inputs.
- Numbers are CPU-reference tier (`cpu-reference`), never GPU claims
  (benchmark-method §1 claim rules survive this goal).
- Baselines append-only; committed inside gradus (requirement 3).
- Reproducible from the three hashes alone (requirement 2) — no other
  hidden state beyond recorded environment identity.
- Harness never mutates the sibling checkouts; scratch roots live outside
  all repos; per-scratch-root Cargo targets (cargo-isolation law).
- Faber source in bench cases obeys gradus source law (no `@ externa`/
  `@ subsidia`; en-locale; public-surface imports only).

## Architecture direction

Ownership: gradus owns the harness, cases, baselines, receipts, and the
AGENTS.md law. Radix owns the gate script (consumed read-only, never
forked). Hosts owns nothing here in v1 — it is a pinned input of record.
The harness is a python3 core (`gradus/scripta/bench.py`) behind a bash
wrapper (`gradus/scripta/bench`) with subcommands `materialize`, `build`,
`run`, `capture`, `gate`, `clean` (scratch-worktree teardown) — the same
wrapper+python split as
`check-benchmark-regression`/`check-benchmark-regression.py`. Failure
semantics: fail closed with typed errors (missing hash, dirty pin, power
state unverifiable on the capture machine, environment mismatch at the
gate); no silent fallback, no default-threshold widening.

## Supporting skills

`$faber` (case authoring/checking), `$faberlang` (container law),
`gpu-lessons` (measurement laws — load before timing work).

## Implementation shape (first milestone, not a delivery graph)

`./scripta/bench materialize --radix R --hosts H --gradus G` →
`./scripta/bench build` → `./scripta/bench run` emits checker JSON →
`./scripta/bench capture` commits a dated 3-hash baseline + receipt →
`./scripta/bench gate <baseline>` refuses non-comparable environments,
then delegates to the radix checker. `./scripta/bench clean` tears the
scratch triple down (`git worktree remove --force` + `git worktree
prune` + scratch-root removal). Defaults: hashes = current HEAD of
each sibling; scratch root under `<workspace>/.bench/gradus/`.

## Release posture

None. Gradus ships `src/` only (`cista.toml`); `bench/` and `scripta/`
are contributor surface. No version bump of the gradus package.

## Exit strategy

The harness is additive. Removing `gradus/bench/` + the AGENTS.md section
retracts the surface with zero product impact; committed baselines remain
valid history either way (append-only, never rewritten).

## Acceptance criteria

1. Harness runs green on the current triple (gradus `4488598` · radix
   `9dc17410d` · hosts `c9cfb5a` or their successors at capture time):
   materialize → build → run → capture, exit 0.
2. A committed baseline exists at
   `gradus/bench/baselines/baseline-YYYYMMDD-r…-h…-g….json` + same-stem
   receipt `.md`, carrying the full environment-identity block including
   power state.
3. Reproduction from the three hashes demonstrated once: a fresh scratch
   materialization at the recorded triple, rerun, gate PASS within the
   default threshold; both runs recorded in the receipt.
4. The gate's red path is proven once (forced exit 1) — L1 falsifiability.
5. `gradus/AGENTS.md` contains the Benchmarks law with the exact run
   command; `docs/benchmark-method.md` is v1.1.0 with the delta recorded.
6. Emitted JSON validates against
   `radix/scripta/check-benchmark-regression.py` (self-compare PASS).
7. Taxonomy carried: every result row has class/work-unit/units/t-s
   fields; a capped sample records valid t/s + `capped: true` and never
   fails the run; the checker contract is untouched (§Perf-taxonomy).
8. Stage ladder live: all four stages selectable by name and number;
   no-flag `run` = stage 2 dev; smoke ≤ 1 min, dev ≤ 3 min, and rough
   ≤ 10 min measured on the current triple with all 7 labels present in
   rough output; stage 4 byte-preserves the 3/10/7-label protocol (K
   unshrunk on every stage); any JSON whose recorded protocol is not
   exactly 3/10 × 7 labels is refused by the gate wrapper (proven with
   the GB-U4 `NOT COMPARABLE` path).
9. Per-row power-state law live (`ea4dd0a3`): every stage's run output
   carries `results[].power_state` on every row plus the
   `metadata.power_class` summary; the gate wrapper refuses
   cross-power-class, mixed-class, and row-field-missing JSON
   (`NOT COMPARABLE`, proven with the GB-U4 refusal path); the first
   baseline remains AC-gated (a battery capture is battery-labeled
   evidence, not the first baseline).

## Units (lowering sketch — refined in `delivery.md`)

| Unit | Scope | Depends on | Hand evidence |
| --- | --- | --- | --- |
| GB-U1 | pin-and-build driver: `scripta/bench` materialize+build (detached worktrees at 3 hashes, release faber, `faber doctor` proof) + `clean` teardown (worktree remove/prune; registrations never accumulate) | — | landed `c212004` (fold `f85272b`) |
| GB-U2 | bench case package: `bench/` Faber package, 7 labels at GEA tell-tale shapes + manifest (class + work-unit/metric fields + `cap_s` per case) | — | landed `e5f658f` (fold `f2d3595`) |
| GB-U3 | run loop + emitter: 3/10 sampling, caps as circuit breakers, checker-format JSON (median_ms + t/s metric fields) + environment-identity metadata | GB-U1, GB-U2 | landed `d85c3c9` (fold `19937dc`) |
| GB-U3b | stage ladder on `scripta/bench run`: `--stage smoke/dev/rough/full` (+`1-4`, `--full`), `--label` subsets, manifest `smoke_label`/`dev_labels`, stage identity in metadata, default = dev | GB-U3 | landed 71ab87a (fold c3bb796) |
| GB-U3c | per-row power-state capture: run-loop probes each row's power class at its execution window; additive `results[].power_state` + `metadata.power_class` summary (`power_class_first`/`_last` when mixed) on every stage; usage text | GB-U3, GB-U3b | landed 407a9df (fold 4158a2b) |
| GB-U4 | baseline capture + gate wrapper: committed dated 3-hash baseline + receipt; gate comparability refusal (environment mismatch, lesser-stage protocol, cross-power-class) + green/red proofs | GB-U3, GB-U3b, GB-U3c | landed 536b7ab+9ceeb71 (fold 15c643e) |
| GB-U5 | reproduction proof: fresh materialization from the recorded triple, gate PASS, receipt rider | GB-U4 | none |
| GB-U6 | AGENTS.md Benchmarks law + `docs/benchmark-method.md` v1.1.0 amendment | GB-U5 | none |

No unit needs a fork decided beyond the goal's Open questions (all carry
defaults); no unit carries a stage/full-suite closeout — lane-owned
validation is named once in `delivery.md` §6.

## Validation

```bash
cd /path/to/faberlang/gradus
./scripta/bench gate bench/baselines/<latest-baseline>.json   # green path, exit 0
BENCH_REGRESSION_THRESHOLD=0.000001 ./scripta/bench gate bench/baselines/<latest>.json  # red path, exit 1
./scripta/bench run --stage smoke   # <= 1 min wiring smoke
./scripta/bench run                 # default = stage 2 dev, ~2-3 min
./scripta/bench run --stage rough   # ~7-8 min full-breadth rough pass, 1-2 reps
./scripta/bench clean                                         # teardown: no scratch worktree registrations remain
./scripta/check-source && ./scripta/check-compile             # repo still green (lane-owned at merge)
```

Reproduction proof (once, at closeout): materialize from the committed
baseline's recorded `triple`, `run`, `gate` — PASS. Recorded in the
baseline receipt.

## Open questions

1. **Baseline home** — default `gradus/bench/baselines/` (numbers live
   with the harness; survives goal archival; requirement 3 "part of the
   library history" reads naturally). Alternative: goal `evidence/` dir
   (perf-parity precedent) — but that moves on archival. Default stands
   unless the operator prefers the factory-doc home.
2. **`check.library.compile` label** — it times the pinned radix compiler,
   not gradus runtime; it is the one label where a radix-only change moves
   the number. Default: keep it (it proves the triple pin exercises
   radix); the receipt names which labels are compiler-sensitive.
3. **Compiled/device arm** — the 3-hash law covers the MIR-runner arm.
   A compiled arm needs the `faber` runtime crate (tag-pinned
   faberlang/faber — a fourth input) and the device arm needs the host
   driver. Both extend the pin law; neither is invented here. Revisit when
   an operator-ordered device bench exists.
4. **Threshold wiring** — advisory-first (this goal). Operator may later
   wire the gate into a merge lane; the wrapper already exists.

## Stop conditions

- Pinned-hash reproduction exceeds threshold on the same machine and
  power class: that is signal (L17) — record it, investigate, never widen
  the threshold (L21); the goal does not "fix" it by loosening the gate.
- A named case surface cannot execute on the MIR runner and no public
  carrier substitute exists at the same shape: drop the label, record it
  in the receipt; do not invent a private API to force it.
- The capture machine cannot verify power state (non-macOS): the baseline
  records `power_state: unavailable` and is marked not gate-comparable;
  capture does not silently proceed as if comparable.
- Materialization cannot resolve a hash (missing object in a shallow
  checkout): fail closed; never substitute a nearby hash.

## Delivery checklist

| Check | Enforced by |
| --- | --- |
| Baseline JSON parses and self-compares green in the radix checker | `check-benchmark-regression.py` (acceptance 6) |
| Baseline carries triple + power state (run summary + per-row fields) + protocol metadata | Receipt review + `capture` fail-closed checks |
| AGENTS.md section names the exact run command | Acceptance 5 |
| No writes outside `gradus/` | Unit write scopes (`delivery.md`) + merge review |

## Ledger

| Unit | Status | Seat | Receipt | Notes |
| --- | --- | --- | --- | --- |
| GB-U1 pin-and-build driver | landed | hand | `c212004` (fold `f85272b`) | `scripta/bench` materialize+build |
| GB-U2 bench case package | landed | hand | `e5f658f` (fold `f2d3595`) | `bench/` package, 7 labels |
| GB-U3 run loop + JSON emitter | landed | hand | `d85c3c9` (fold `19937dc`) | full sweep RUN_EXIT 0; self-compare green; battery-labeled format evidence |
| GB-U3b stage ladder | landed | hand | `71ab87a` (fold `c3bb796`) | measured: smoke 45 s, dev 2 m22 s (default), rough 7 m14 s all-7, full 31 m42 s; self-compares green at every stage |
| GB-U3c per-row power-state capture | landed | hand | `407a9df` (fold `4158a2b`) | smoke rows labeled live; mock transition → mixed; additive-only diff; unavailable proven |
| GB-U4 baseline capture + gate wrapper | landed | hand | `536b7ab`+`9ceeb71` (fold `15c643e`) | first baseline at radix e792964/hosts c9cfb5a/gradus 536b7ab; AC unanimous; refusals at exits 3-6 |
| GB-U5 reproduction proof | landed | hand | `7ed603e` (fold `533121e`) | gate PASS default threshold; worst +0.96%; noise floor ~±1% |
| GB-U6 AGENTS.md law + method v1.1.0 | landed | hand | `17dd979` (fold `a8c0182`) | requirement 4; both law families carried |
