# Delivery: bench-harness — P3 unit graph

**Status**: P3 — FILEABLE (gate MET: goal-check READY, independent planner pass 2026-08-27; goal `goal.md` forged from TEMPLATE same day)
**Goal**: [`goal.md`](goal.md) — verdict **READY**, consumer: delivery
**Planner**: planner (mind task `076e7a1a`, operator pause-exception order 2026-08-27)
**Amended**: 2026-08-27 — audit `c4f621fa` fix pass (perf-taxonomy fold incl. class-(b) not-fitting ruling, GB-U1 scratch-worktree teardown, GB-U4/GB-U5 capture-ordering invariant)
**Write theme**: gradus-only. `radix/` and `hosts/` are pinned read-only inputs — zero tracked-content contact by construction (linked-worktree registration under each source repo's `.git/worktrees/` is named in GB-U1 and removed by `clean`).

---

## 1. Interpreted theme / problem

Operator order (4 verbatim requirements in goal §Problem): a repeatable
bench harness whose numbers attach to the radix+hosts+gradus triple, are
reproducible from those three hashes alone, are committed inside gradus,
and whose process is law in `gradus/AGENTS.md`.

## 2. Normalized spec (delivery-sized outcome)

`gradus/scripta/bench` materializes detached worktrees of the three repos
at explicit hashes into a scratch root outside all repos (with `clean`
teardown so worktree registrations never accumulate), builds a
release `faber` from the pinned radix, runs a fixed 7-label case
inventory through the MIR runner (3 warmups / 10 samples / median per
label; every case fixed-oracle class with t/s metric fields, runtime
caps as safety circuit breakers only), emits
`check-benchmark-regression`-format JSON with full
environment-identity metadata (including power state per the battery
ruling), commits a dated 3-hash baseline + receipt under
`gradus/bench/baselines/` (recorded gradus sha already contains the
complete harness), proves the gate green and red, demonstrates
once that reproduction works from the recorded triple, and records the
law in `gradus/AGENTS.md` + `docs/benchmark-method.md` v1.1.0.

### Taxonomy disposition (operator addendum mail `46ab4e94`)

- **Class (a) fixed-oracle — folded.** Manifest entries gain `class` +
  metric fields (`work_unit`, `units_per_iteration`, `cap_s` default
  60); decode/prefill cases count tokens; kernel cases define their
  fixed work unit + throughput label. Sole throughput metric: t/s =
  unit-count / min(completion, cap); `median_ms` remains the checker's
  gate quantity (format unchanged, extra fields compose).
- **Caps — safety circuit breakers.** Never metrics, never pass/fail; a
  capped sample records valid t/s + `capped: true`.
- **Class (b) fixed-output-length — NOT FITTING (explicit ruling).** Its
  expected per-side token counts presuppose a second tokenizer side
  (llama) to differ from; this solo gradus harness has one side and
  fixed computations, so a per-side expected-count oracle has nothing to
  ground it on. Class (b) belongs to the gradus-v-llama parity harness
  when one is ordered — do not force it here. The t/s + caps laws above
  still carry into the GB-U6 AGENTS.md law so the future parity harness
  inherits them.

## 3. Repo-aware baseline

- Gate consumer (read-only): `radix/scripta/check-benchmark-regression.py`
  — `format_version:"1"` + `results[].label/median_ms`; 10 % default;
  `BENCH_REGRESSION_THRESHOLD` override; exit 0/1; machine-blind (the
  gradus wrapper adds the comparability refusal the checker lacks).
- Format precedent: `radix/docs/benchmarks/baseline-2026-07-27.json`.
- Protocol authority: `gradus/docs/benchmark-method.md` §4.3 (3/10/wall).
- Env seams: `FABER_LIBRARY_HOME` (pinned gradus library), release
  `cargo build -p faber` in the pinned radix worktree with its own target;
  `FABER_SUPPORT_PATH_OVERRIDE` documented for the future compiled arm
  only (`radix/crates/faber/src/package/runtime_sources.rs:17`).
- Case route: `faber run` package route (single-file scripts reject kernel
  imports, PKG001 — `gradus/scripta/check-compile` header).
- Current triple at forge time: gradus `4488598` · radix `9dc17410d` ·
  hosts `c9cfb5a`.

## 4. Hand unit graph

Parallelism: GB-U1 ∥ GB-U2 (disjoint surfaces); then the chain
GB-U3 → GB-U4 → GB-U5 → GB-U6.

| Field | GB-U1 — pin-and-build driver |
| --- | --- |
| `outcome` | `scripta/bench materialize` + `build` + `clean`: detached-worktree pinning of radix/hosts/gradus at explicit hashes into a scratch root outside all repos, a release faber build from the pinned radix, and scratch-worktree teardown (`git worktree remove --force` per worktree + `git worktree prune` in each source repo + scratch-root removal) so registrations never accumulate |
| `write_scope` | `gradus/scripta/bench` (new, +x), `gradus/scripta/bench.py` (new). Scratch root default `<workspace>/.bench/gradus/<r7>-<h7>-<g7>/` — no repo files outside the two named |
| `done_when` | From a clean scratch root at an explicit triple: (a) each worktree `git rev-parse HEAD` equals its requested hash; (b) `cargo build --release -p faber` succeeds inside the pinned radix with its own target dir; (c) `FABER_LIBRARY_HOME=<scratch> <scratch-faber> doctor` reports the scratch library home with gradus resolvable; (d) a bogus hash fails closed with a typed error, non-zero exit; (e) after `clean`, the scratch root is gone and `git worktree list` in radix, hosts, and gradus shows no scratch registrations (prune verified) |
| `depends_on` | — |
| `sanity` | Run materialize+build at the current triple; keep the `doctor` output for the unit report |
| `non_goals` | No timing, no JSON, no bench cases; no tracked-content writes inside `radix/`, `hosts/`, or main `gradus/` (linked-worktree registration writes admin metadata under each source repo's `.git/worktrees/` — named here, removed by `clean`); no `CARGO_TARGET_DIR` sharing; no clones |
| `risk` | medium — worktree + cargo-isolation mechanics; mitigation: fail-closed hash verification (done_when a/d) |
| `integrable` | yes |

| Field | GB-U2 — bench case package |
| --- | --- |
| `outcome` | `gradus/bench/` Faber package: 7 case programs at the GEA tell-tale shapes (goal §Case inventory) + case manifest (label → entry, `class`, `work_unit` + `units_per_iteration`, `cap_s` default 60, iterations K, tier), each case printing a non-trivial value-check line |
| `write_scope` | `gradus/bench/**` (faber.toml, source, `cases.toml`) |
| `done_when` | (a) `faber check` green on the bench package with the current binary; (b) `faber run` executes every manifest label to natural exit printing its check line (goal table labels present; any device-only surface substituted per the goal's substitution rule and recorded in a manifest comment); (c) manifest labels unique; (d) every entry carries `class: fixed-oracle` + metric fields — decode/prefill cases count tokens as the unit, kernel cases name their fixed work unit and throughput label (goal §Perf-taxonomy) |
| `depends_on` | — |
| `sanity` | `faber check` + one label run at HEAD |
| `non_goals` | No harness logic, no timing, no changes under `src/` (shipped surface untouched), no `@ externa`/`@ subsidia`, no new public gradus APIs |
| `risk` | medium — a named surface may not execute on the MIR runner; substitution rule bounds it |
| `integrable` | yes |

| Field | GB-U3 — run loop + JSON emitter |
| --- | --- |
| `outcome` | `scripta/bench run`: per case 3 warmups + 10 samples of `faber run` wall time over the manifest iteration count, each sample bounded by the case's `cap_s` as a safety circuit breaker; emits checker-format JSON (`format_version:"1"`, `results[].label/median_ms/min/max/samples/iterations/ok` + taxonomy fields `class/work_unit/units_per_sample/median_units_per_s/capped`) with the full environment-identity metadata block |
| `write_scope` | `gradus/scripta/bench.py`, `gradus/scripta/bench` (extend) |
| `done_when` | (a) `run` at the current triple emits JSON that passes `python3 ../radix/scripta/check-benchmark-regression.py <out> <out>` (self-compare exit 0, zero SKIP/REGRESS rows); (b) metadata block complete: timestamp, hostname, machine/cpu/cores/memory/os/arch, `power_state` + `pmset_raw`, full triple SHAs, faber profile/rustc/build command, protocol (3/10/K per case), citations; (c) every case's check line observed during sampling or the result row is `ok:false`; (d) every row carries the t/s metric fields (t/s = unit-count / min(completion, cap), median across samples) and a cap-hit sample records its valid t/s + `capped: true` without failing the run — caps are never metrics, never pass/fail (goal §Perf-taxonomy) |
| `depends_on` | GB-U1, GB-U2 |
| `sanity` | Self-compare command above |
| `non_goals` | No threshold logic, no baseline commit, no gate; no in-Faber timing intrinsics (process wall is the method) |
| `risk` | low — format contract is small and pinned by the checker source |
| `integrable` | yes |

| Field | GB-U4 — baseline capture + gate wrapper |
| --- | --- |
| `outcome` | `scripta/bench capture` + `gate`: commit the first baseline (`bench/baselines/baseline-YYYYMMDD-r…-h…-g….json` + same-stem receipt `.md`); gate refuses non-comparable environments (machine or power-class mismatch → `NOT COMPARABLE`, distinct exit) then delegates to the radix checker |
| `write_scope` | `gradus/bench/baselines/**` (new), `gradus/scripta/bench.py` (extend) |
| `done_when` | (a) baseline captured at the current triple with AC power verified (`power_state: ac (pmset-verified…)`); battery capture allowed only battery-labeled per the ruling; (b) receipt committed with environment table + run transcript; (c) gate green path exit 0 against the committed baseline; (d) red path proven once — forced exit 1 (e.g. `BENCH_REGRESSION_THRESHOLD=0.000001`) — transcript kept in the receipt (L1); (e) gate `NOT COMPARABLE` path proven once with a doctored environment field; (f) ordering invariant held — the recorded `gradus_sha` already contains the complete harness: capture runs only after the harness + case commits land, and verifies the recorded hash resolves `scripta/bench` with the full subcommand set before writing the baseline |
| `depends_on` | GB-U3 |
| `sanity` | `scripta/bench gate <baseline>` green then red |
| `non_goals` | No threshold changes (10 % default stands), no CI wiring, no editing of any previously committed baseline |
| `risk` | medium — capture honesty (power verification, warmups honored); fail-closed metadata checks bound it |
| `integrable` | yes |

| Field | GB-U5 — reproduction proof from the triple |
| --- | --- |
| `outcome` | Demonstrate requirement 2 once: fresh scratch materialization from the committed baseline's recorded `triple` (harness + cases invoked from the pinned gradus worktree at the recorded gradus sha — which GB-U4 pinned as harness-complete), rerun, gate PASS at default threshold |
| `write_scope` | `gradus/bench/baselines/<baseline-stem>.md` (receipt rider; or same-stem `-reproduction.md`) |
| `done_when` | (a) reproduction run's environment identity matches the baseline's machine + power class (else the receipt records NOT COMPARABLE honestly and the unit reports back instead of forcing green); (b) gate exit 0 within default threshold; (c) receipt records both runs side by side (hashes, environment, per-label medians + t/s) and cites the recorded `gradus_sha` as harness-complete (the GB-U4 ordering invariant); (d) no baseline file modified |
| `depends_on` | GB-U4 |
| `sanity` | The gate run itself |
| `non_goals` | No re-capture, no threshold tuning to force PASS (L21), no investigation of an exceeded threshold inside this unit — that is recorded signal for a new goal |
| `risk` | medium — run-to-run variance on the same machine; the 3/10-median protocol and 10 % threshold are the designed buffer |
| `integrable` | yes |

| Field | GB-U6 — AGENTS.md law + benchmark-method v1.1.0 |
| --- | --- |
| `outcome` | Requirement 4: `## Benchmarks` section in `gradus/AGENTS.md` (3-hash law, exact run commands incl. `clean` teardown, baseline home + append-only rule, environment-identity + battery ruling, threshold policy, metric law — t/s = unit-count / min(completion, cap) sole throughput metric, runtime caps safety circuit breakers never pass/fail, class-(b) not-fitting ruling pointing at the parity harness — citations); `docs/benchmark-method.md` bumped to v1.1.0 recording the harness delta |
| `write_scope` | `gradus/AGENTS.md`, `gradus/docs/benchmark-method.md` |
| `done_when` | (a) AGENTS.md section present, naming `./scripta/bench materialize/build/run/capture/gate/clean` and the committed baseline path of record; (b) benchmark-method v1.1.0 with delta note (its §6 "no benchmark binary" clause superseded by the 2026-08-27 operator order, cited); (c) the section carries the taxonomy law — t/s sole metric, caps as circuit breakers, class-(b) not-fitting ruling (goal §Perf-taxonomy; addendum mail `46ab4e94`); (d) no other AGENTS.md section weakened or reordered; (e) citations resolve (goal path, perf-parity U7 receipt, gpu-lessons) |
| `depends_on` | GB-U5 (the law cites a demonstrated reproduction) |
| `sanity` | Grep the section; open the cited paths |
| `non_goals` | No goal.md ledger/status edits (Mind-owned), no harness code changes |
| `risk` | low |
| `integrable` | yes |

## 5. Integration / merge gate

No non-integrable units; no dual-authority surface (harness, cases,
baselines, law are additive, disjoint per unit). Standard merge-lane
ownership applies: stages per the workspace ladder, gradus
`./scripta/check-source` + `./scripta/check-compile` green on the
integrated tree. No aggregate gate beyond that.

## 6. Lane-owned validation (named once)

- Lint lane: workspace stages 1–2 as they apply to gradus.
- Test lane: `gradus/scripta/check-source`, `gradus/scripta/check-compile`
  (package + admitted exempla — bench package is additive, not in the
  exempla list), goal §Validation closeout commands including the
  red-path proof.
- Merge lane: integrated-tree green + baseline JSON present + AGENTS.md
  law present (goal acceptance 1–6).

## 7. Open questions for Mind

Goal §Open questions 1–4 stand (baseline home default
`gradus/bench/baselines/`; `check.library.compile` compiler-sensitive
label kept; compiled/device arm deferred — extends the pin law when
ordered; gate advisory until wired). The operator perf-taxonomy
disposition (class (a) folded, caps as circuit breakers, class (b)
not-fitting ruling) is recorded in §2 above and goal §Perf-taxonomy.
None block dispatch.

Hand tasking pointer: goal path + unit id (e.g.
`gradus/docs/factory/bench-harness/` + `GB-U3`). Mind prepares and files
Hands; this graph is the whole assignment surface.
