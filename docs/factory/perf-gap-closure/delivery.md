# Delivery: perf-gap-closure — parallel unit graph

**Status**: lowered for Mind routing 2026-08-27; AMENDED 2026-08-28 (reopen package, Mind memo `cbc68961` — §7 PGC-R series supersedes the undispatched C1/C3/C4 cards and folds B/C residuals; no GO stamp)
**Goal**: [`goal.md`](goal.md), committed `bd37d20`; this document adds execution detail and does not amend the goal
**Assignment**: Vivi task `943dc1fc` (planner lowering)
**Primary repo**: `/Users/ianzepp/work/faberlang/gradus`
**Named arms**: `/Users/ianzepp/work/faberlang/hosts`, `/Users/ianzepp/work/faberlang/radix`, and `/Users/ianzepp/work/ianzepp/skills`
**Planner boundary**: planning text only. No `.fab`, compiler, corpus, or skills content changes are part of this commit.

## 1. Binding execution law

### 1.1 Standing baseline and measurement law

Every measurement in this delivery reads the standing gradus-llama-parity
baseline. U5 owns the first AC baseline when landed. Until then, the U2 live
captures at `/tmp/glp-u2-live-final-1787859628`, mirrored in the U3 fixture
pair, are the working baseline. A unit never reads another perf-gap-closure
unit's numbers as its baseline.

Every paired delta uses the same GGUF, statues, environment identity, power
class, certified per-side counts, and phase accounting as that baseline.
Bench-law AC/power rules apply. A measurement-bearing unit changes one lever,
runs one paired parity measurement, and attributes only that delta to the
lever. This is gpu-lessons L84. Structural changes create a new append-only
capture; they never rewrite the baseline. Device kernels never execute under
the MIR runner (L86).

Baseline facts and hypotheses retained from the goal:

| Row | llama | gradus | ratio |
| --- | ---: | ---: | ---: |
| short decode (8 tok) | 236.5 t/s | 32.2 t/s | 7.33× |
| fixed-1000 decode | 231.8 t/s | 15.65 t/s | **14.81×** |
| short prefill | 3066 t/s | 571 t/s | 5.37× |
| fixed-1000 prefill | 3158 t/s | 567 t/s | 5.57× |

Fixed-1000 decode is 63.890 ms/step; short decode is 31.013 ms/step. Prefill
is approximately 63 ms in both statues. The goal-level expectation ladder is
a hypothesis, not a promise: B plus A fusion plausibly reaches about
10–15 ms/decode step (about 65–100 t/s); llama-class 4.3 ms requires every
track. No card may turn these figures into a synthetic target or a pass gate.

### 1.2 Guidance law inherited by every A card

A-series cards inherit goal §3 and must cite both `PGC-A0` and this section in
their dispatch packet. The law intentionally overrides the common C/Python
prior: accumulator bindings, counter loops, nested stride walks, and
hand-written folds freeze one imperative shape. Faber's language-level tensor
and collection constructs expose a shape the compiler can lower to the exact
target recipe.

The conversion families are binding:

| Hand-written family | Required convert-or-record candidate |
| --- | --- |
| counter `while` / managed counter walk | `for range`; n-ary range for Cartesian walks; `for from` series for zip walks |
| accumulator binding plus loop | `.reduce((acc, x) ∴ expr, init)` |
| transform loop building a list | `.map(x ∴ expr)` |
| predicate loop with appends | `.filter(x ∴ pred)` |
| tensor reduction loops | from-family with multi-index `at` clauses, such as `max from scores at [i, j]` |
| best-index scans | `.argmax()` / `.argmin()` twins under the lang-surface-reduction Wave-0 rulings |

A site without a covering construct stays and receives an in-code reason.
No seat invents semantics to force a conversion. The compiler recipes include
tensor `·` → `Collection(TensorMatMul)` →
`CollectionKernelPlan::TiledMatMul`, with target-owned threadgroup tiles,
barriers, and zero-fill. Kernel bodies are already mostly modern; the measured
debt is host-side and on older paths. Starting facts are zero closure-intrinsic
uses under `gradus/src/`, with known accumulator sites at `nn.fab:488`,
`train.fab:266`, `attention.fab:337/350/432`, and `sampling.fab:458`.
Measured loop density starts at tokenizer 51, cache 33, math 31, block_verify
28, calibration 26, sampling 24, and serialize 23 sites.

The deterministic work list comes from the machine. Every A card names the
fully resolved commands and output paths in §3.2/§3.3; a placeholder is not
executable evidence:

1. From the Gradus checkout, capture
   `faber check --air --json /Users/ianzepp/work/faberlang/gradus/src/<module>.fab`
   to that card's `air-before.json` and `air-after.json` paths.
2. Work `ADMISSIBLE-ONE-AWAY` rows in ranked order.
3. Record `ADMISSIBLE-KERNEL` as the consumable-now set.
4. Triage, but do not churn on, `WOULD-REJECT` rows.
5. Capture WARN027 `complexity_budget_exceeded` rows with the exact
   `faber check --complexity-budget 12` and, when the module has kernel-marked
   rows, `faber check --kernel-complexity-budget 2` forms. Count rows into the
   card's explicit `warn027-*.rows` evidence paths.
6. Commit the before/after census rows and WARN027 evidence with the batch.

The exact resolved command shape for each A card is:

```text
faber check --air --json /Users/ianzepp/work/faberlang/gradus/src/<module>.fab > /Users/ianzepp/work/faberlang/gradus/docs/factory/perf-gap-closure/evidence/<card-id>/air-before.json
faber check --complexity-budget 12 /Users/ianzepp/work/faberlang/gradus/src/<module>.fab > /Users/ianzepp/work/faberlang/gradus/docs/factory/perf-gap-closure/evidence/<card-id>/complexity-before.txt 2>&1
faber check --kernel-complexity-budget 2 /Users/ianzepp/work/faberlang/gradus/src/<module>.fab > /Users/ianzepp/work/faberlang/gradus/docs/factory/perf-gap-closure/evidence/<card-id>/kernel-complexity-before.txt 2>&1
```

Run the same three commands with `before` replaced by `after`. Count
`WARN027` lines from the two captured budget outputs into
`warn027-before.rows` and `warn027-after.rows` under the same card directory.
The `--kernel-complexity-budget` capture is `not-applicable` only when the AIR
census proves there are no kernel-marked rows; the card still records that
fact at its named kernel-complexity evidence path. A named card may not omit a
budget command or its applicability proof.

The three governing references act together: `$faber`,
`$faber/canonical-faber`, and `$gpu-lessons`. The kernel-purity-census campaign
owns the purity definition. Dense typed assembly owns the small typed leaf
law. Radix AIR already carries the fusion-table side channel, and `to_mir.rs`
already lowers only a fused group's root. Purity is the prerequisite for
fusion; a polish seat must preserve leaves rather than build a mega-kernel.
LSR wave 6 rulings govern functional-intrinsic adoption.

### 1.3 Parallel and packet law

Implementation proceeds in parallel where the declared write paths permit
it. No unit depends on another unit's unlanded output.

Wave 1 is deliberately split into two top-level sub-waves. `PGC-W1A` is the
maximal entry/case-disjoint set: `B1`, `B3`, `C2`, and `C5` may run
concurrently. The common physical Gradus paths in that set are
`gradus/src/kernel.fab` and the co-located test file `gradus/src/kernel.proba`.
The goal's §4 packet mechanism explicitly permits both: each card owns named,
disjoint `kernel.fab` entry regions and named `kernel.proba` cases (or an
explicit verify-untouched scope), and the Mind folds both paths' packet
commits serially. Their new export and device test files are per-card and
additive; `kernel.proba` is the intentional shared test file handled by case
ownership, not an unowned append surface. `PGC-W1B` is the remainder. Its
cards are one-card, file-disjoint folds in the stated order because the
`radix-mir` kernel-plan files are shared by `B2`, `C1`, `C3`, and `C4`, and
`radix-mir-metal` `emit/matmul.rs` plus its test are shared by `B2` and `C4`.
No two cards in `PGC-W1B` are live concurrently.

| Wave | Parallel group | Execution |
| --- | --- | --- |
| 0 | `PGC-W0-DIRECT` | `PGC-D1` in hosts direct mode and `PGC-A0` in the skills repo direct mode, concurrently |
| 1a | `PGC-W1A` | `PGC-B1`, `PGC-B3`, `PGC-C2`, and `PGC-C5` in separate packets, concurrently; disjoint `kernel.fab` entry regions and `kernel.proba` cases fold serially through the Mind |
| 1b.1 | `PGC-W1B-1` | `PGC-B2` alone; owns the shared kernel-plan and Metal matmul paths for this fold |
| 1b.2 | `PGC-W1B-2` | `PGC-C1` after `PGC-B2`; owns the kernel-plan paths for this fold |
| 1b.3 | `PGC-W1B-3` | `PGC-C3` after `PGC-C1`; owns the kernel-plan paths for this fold |
| 1b.4 | `PGC-W1B-4` | `PGC-C4` after `PGC-C3`; owns the shared kernel-plan and Metal matmul paths for this fold |
| 2+ | `PGC-WA-<n>` | per-module A-series packets, massively parallel after `PGC-A0` lands |

Every Wave-1 packet is `worktrees/pgc-<lowercase-id>/` on branch
`factory/pgc-<lowercase-id>`; for example `worktrees/pgc-b1/` and
`factory/pgc-b1`. Each card owns one defect, its declared Gradus entry region,
and additive-only per-card export/device test files. The co-located
`gradus/src/kernel.proba` test file is intentionally shared by case, not by
append. The `kernel_plan/{plan,build,kernel_plan_test}.rs` and
`emit/matmul.rs`/`emit/tests/matmul.rs` paths never occur in two live
sub-waves. Shared physical `kernel.fab` and `kernel.proba` are the allowed
concurrent Gradus paths and are handled only by disjoint entry/case ownership
plus serial packet folds through the Mind. Each A card uses `worktrees/pgc-<lowercase-id>/` and
`factory/pgc-<lowercase-id>` by the same rule. Cheap seats are welcome for A
batches because their oracle is mechanical.

B, C, and A work always reads the standing baseline, never another card's
capture. A0 gates only A-series dispatch. D1 does not gate B or C. B and C do
not gate each other or A, except for the explicit file-ownership order inside
`PGC-W1B`.

The `PGC-W1B` order is a file-ownership rule, not a semantic dependency: each
card still reads the standing baseline and proves its own vertical. A card may
leave a conditionally listed implementation path read-only only when its
preflight proof records that no fact there changed; it may not edit a path
owned by another `PGC-W1B` fold.

All Wave-1 export and device proofs are additive and use per-card files. No
B/C card appends to `radix/crates/mir-emit-harness/src/gea3_pipeline_test.rs`
or `hosts/macos-arm64/tests/gea3_decode.rs`; each uses its own path named on
its card below. The co-located `gradus/src/kernel.proba` file is the exception
for Gradus proba tests: its named cases are disjoint and its packet folds stay
serial through the Mind, just like the shared `kernel.fab` entry regions.

## 2. Unit cards

### PGC-D1 — harden timing and receipt truth

| Field | Value |
| --- | --- |
| `id` | `PGC-D1` |
| `outcome` | Report GPU timestamp coverage honestly for all 2,115 encoders: either sample every encoder or put the partial fraction in every dependent field's name/shape. Remove the false `sync_wait_us` meaning, rename it to the launch clock it measures, and add a true submit-plus-sync clock only if that boundary is observable. |
| `write_scope` | `hosts/macos-arm64/src/metal_host.rs` (`TIMESTAMP_SAMPLE_CAPACITY` and sampling/coverage receipt facts only); `hosts/macos-arm64/tests/gea3_decode.rs` (parity timing companion, fixed-1000 physical receipt fields, and their focused self-tests). `radix/crates/mir-emit-harness/src/gea3_pipeline_test.rs` only if live inspection proves the sample-count fact is emitted there; otherwise it is read-only. No kernel source. |
| `done_when` | A fixed-1000 decode receipt reports per-step GPU busy over all 2,115 encoders, or mechanically reports the sampled numerator and total 2,115 in the field shape; no dependent field implies full coverage when only 1,024 encoders are sampled. `sync_wait_us` is absent from the affected receipt and replaced by the true launch-clock name. A submit-plus-sync duration exists only if directly observed. Focused hosts receipt/self-tests pass. One live fixed-1000 receipt is re-captured under the new fields and records certified 1000/1000 gradus output. |
| `depends_on` | none |
| `sanity` | Read one emitted decode step and verify timestamp numerator, denominator, clock labels, launch-clock sum, and queue boundary reconcile without treating queue minus sampled GPU time as measured bubbles. |
| `non_goals` | No kernel source; no performance claim; no extrapolated GPU time; no MIR runner; no parity baseline rewrite. |
| `risk` | medium — Metal counter capacity and observability may force explicit partial labeling rather than full sampling; honesty is the oracle. |
| `integrable` | yes — hosts direct-mode, path-limited commit |
| `parallel_group` | `PGC-W0-DIRECT` |

Evidence retained: 2,048 timestamp slots sample 1,024 of 2,115 encoders;
the existing `sync_wait_us` equals the launch clock. Bubble figures remain
upper bounds until this card lands.

### PGC-A0 — install the anti-prior guidance law

| Field | Value |
| --- | --- |
| `id` | `PGC-A0` |
| `outcome` | Put the complete §1.2 anti-prior law into standing skill text: why C/Python accumulator and counter-loop priors are wrong for Faber; how language constructs reach AIR and target recipes; all named conversion families; and the convert-or-record clause. |
| `write_scope` | `/Users/ianzepp/work/ianzepp/skills/faber/canonical-faber/SKILL.md`; `/Users/ianzepp/work/ianzepp/skills/gpu-lessons/references/laws.md` (one LLM-prior hazard law row). Commit in `/Users/ianzepp/work/ianzepp/skills`. |
| `done_when` | Both skills carry the law in their existing voice and the skills-repo commit exists. Text includes counter-`while` → `for range` including n-ary Cartesian walks; managed folds/transforms/predicates → `.reduce`/`.map`/`.filter` with `∴`; tensor reductions → from-family multi-index `at`; best-index → argmax twins; compiler target-recipe rationale; and convert-or-record. Every A card below cites `PGC-A0` and §1.2. |
| `depends_on` | none |
| `sanity` | Read both committed skill entries against goal §3 and §1.2; every named family and the no-covering-construct reason clause is present. |
| `non_goals` | No Gradus, Radix, Hosts, corpus, or unrelated skill restructuring. |
| `risk` | low — wording must preserve strong guidance without pretending every site has a covering construct. |
| `integrable` | yes — skills direct-mode, path-limited commit |
| `parallel_group` | `PGC-W0-DIRECT` |

### Wave-1 common vertical oracle

The eight B/C cards each own one defect from a declared Gradus entry/proba
scope through the export pin and physical device proof. A source-writing card
may change only its named `gradus/src/kernel.fab` entry region and focused
`gradus/src/kernel.proba` cases. The shared `kernel.fab` path is allowed only
under the goal §4 packet mechanism: entry ownership is explicit below and
packet commits fold serially. The shared `radix-mir` kernel-plan paths and
Metal matmul paths are not concurrent; their one-card `PGC-W1B` folds own the
whole listed file set for their turn.

Every card records every affected proba case before and after as the exact
three-field tuple `(case_path, status, stderr bytes)`. The tuple must be
byte-identical for every case. No expected output, tolerance, order, status,
or error variant changes. `C2` and `C5` are the allowed verify-untouched
exception on the Gradus side: their cards still name the owned entry/case
scope, capture the same tuple, and include an explicit no-diff proof for both
Gradus files. A host/export-only vertical must never silently omit its Gradus
scope.

Every measurement-bearing B/C card performs exactly one baseline-grade full
paired-parity run for its named phase and statue. From the Radix checkout, the
capture command is exactly `scripta/parity run --stage full` with that card's
`--output-dir`; the card then names its exact `scripta/parity reduce` command,
its append-only `scripta/parity baseline` candidate command, and the evidence
path. Lesser stages may be used for iteration but never produce the card's
baseline-grade delta. The capture records the complete three-repo pin, power
class, certified per-side counts, phase wall, and card-specific work evidence.
It reports the paired delta even when the wall does not move. A failed
hypothesis is honest evidence; it is not permission to pull another lever into
the card.

#### PGC-B1 — dynamic or bucketed decode attention length

| Field | Value |
| --- | --- |
| `id` | `PGC-B1` |
| `outcome` | Stop splicing capacity 1,100 into decode attention work. Score, mask/softmax, transpose, and context use actual history length or a declared bucket while preserving the capacity allocation boundary. |
| `write_scope` | Packet `worktrees/pgc-b1/`, branch `factory/pgc-b1`. `gradus/src/kernel.fab` only entries `decode_key_transpose`, `decode_score_gemm`, `decode_masked_softmax`, and `decode_context_gemm`; `gradus/src/kernel.proba` only the named cases for those four entries. **AMENDED 2026-08-27 (scope-amendment law; stop-report handle `882873ea` verdict block_ship, packet clean):** the owned source entries are pinned at `L_max=76` in gradus source (mask-beyond-L semantics already present); the 1,100 work extent arrives via the export-time capacity specialization in `radix/crates/mir-emit-harness/src/gea3_pipeline_test.rs` — therefore this card ALSO owns, exclusively in its wave, the capacity-specialization code paths for its four entries inside `gea3_pipeline_test.rs` (extent follows actual/declared-bucket history length; allocation capacity may remain 1,100). New additive-only export test `radix/crates/mir-emit-harness/src/gea3_pipeline_pgc_b1_test.rs`; new additive-only device test `hosts/macos-arm64/tests/gea3_decode_pgc_b1.rs`. No other kernel entries; no edits to unrelated `gea3_pipeline_test.rs` regions. Packet membership: gradus + radix + hosts writable. |
| `done_when` | Focused proba tuples (`case_path`, `status`, exact stderr bytes) are byte-identical before/after. A device test proves early and late fixed-1000 steps dispatch score/softmax/transpose/context at actual or declared bucket extent rather than 1,100, while certified output stays 1000/1000. Exactly one fixed-1000 decode paired-parity capture against the standing baseline records per-step wall and the affected entry geometry; expected-effect hypothesis retained: about 64 → about 50 ms/step (decode report range 48–52 ms). |
| `measurement_commands` | From `/Users/ianzepp/work/faberlang/radix`: `scripta/parity run --stage full --output-dir /Users/ianzepp/work/faberlang/gradus/docs/factory/perf-gap-closure/evidence/PGC-B1/parity-raw`; then `scripta/parity reduce /Users/ianzepp/work/faberlang/gradus/docs/factory/perf-gap-closure/evidence/PGC-B1/parity-raw --out /Users/ianzepp/work/faberlang/gradus/docs/factory/perf-gap-closure/evidence/PGC-B1/parity-receipt.json`; then append-only candidate `scripta/parity baseline /Users/ianzepp/work/faberlang/gradus/docs/factory/perf-gap-closure/evidence/PGC-B1/parity-raw --baselines-dir /Users/ianzepp/work/faberlang/gradus/docs/factory/perf-gap-closure/evidence/PGC-B1/baseline-candidate --receipt-out /Users/ianzepp/work/faberlang/gradus/docs/factory/perf-gap-closure/evidence/PGC-B1/baseline-candidate.md`. Raw capture, reduced receipt, candidate baseline, and geometry/delta evidence live under `gradus/docs/factory/perf-gap-closure/evidence/PGC-B1/`; a lesser stage is not baseline-grade. |
| `depends_on` | none |
| `sanity` | Inspect step 1 and step 1000 descriptors: allocation capacity remains 1,100, work extent follows valid length/bucket, and masked results preserve token/proba identity. |
| `non_goals` | No GEMV retile (B2), KV mutator rewrite (B3), fusion, sampling move, comparator change, or baseline rewrite. |
| `risk` | high — runtime extent must not weaken capacity, mask, or bounds safety. |
| `integrable` | yes — one defect, named entry regions, packet fold |
| `parallel_group` | `PGC-W1A` |

Evidence retained: fixed score GEMM has 70,400 key elements versus 4,864;
softmax is 1,100 elements versus 76; per-step walls are flat. The observed
7.33× → 14.81× spread is static overcompute, not history growth.

#### PGC-B2 — T=1 GEMV and reduction specialization

| Field | Value |
| --- | --- |
| `id` | `PGC-B2` |
| `outcome` | Give T=1 decode GEMV/reduction entries a one-row specialization so seven of eight row lanes do not compute and synchronize useless accumulators. |
| `write_scope` | Packet `worktrees/pgc-b2/`, branch `factory/pgc-b2`. `gradus/src/kernel.fab` only `decode_gemv_qo`, `decode_gemv_kv`, `decode_gemv_gate_up`, `decode_gemv_down`, `lm_head_gemv`, and the T=1 score/context reduction specialization points; `gradus/src/kernel.proba` only their cases. **AMENDED 2026-08-27 (scope-amendment law; stop-report reply `79a7fe97`/message `e1d7dd10`, verdict block_ship, packet clean):** the T=1 dispatch-shape mechanism spans surfaces the original list cannot reach — this fold EXCLUSIVELY owns, for this wave, additionally: the T=1 GEMV entry pin regions inside `radix/crates/mir-emit-harness/src/gea3_pipeline_test.rs` (the `workgroup_x:8/workgroup_y:8` plan-fact pins, the `(8,8,1)` launch-grid pins, and the geometry-drift equality assertions for the named T=1 entries ONLY — unrelated regions untouched); `radix/crates/radix-mir/src/kernel_plan/validate.rs` (the workgroup==tile law, for the T=1 one-row exception or equivalent smallest mechanism); `radix/crates/radix-mir-metal/src/abi/contract.rs`, `abi/resource.rs`, `device_program/types.rs` (launch-grid derivation for the named entries); `radix/crates/radix-mir-metal/src/emit/recipes.rs` and `emit/mod.rs` (plan resolution + `emit_tiled_matmul` call site for the one-row recipe). If the chosen mechanism introduces a new `CollectionKernelPlan` variant, exhaustive-match updates in the files it breaks are in scope for THIS fold with each file named in the report — choose the SMALLEST mechanism that changes the dispatch shape (a guard-only accumulator change inside `matmul.rs` is explicitly NOT sufficient; done_when requires the one-row dispatch shape). Plan-fact and kernel_plan tests own the updated expectations. New additive-only export test `gea3_pipeline_pgc_b2_test.rs`; new additive-only device test `hosts/macos-arm64/tests/gea3_decode_pgc_b2.rs`; no edits to unrelated `gea3_pipeline_test.rs` regions or `gea3_decode.rs`; no other kernel entries. |
| `done_when` | Focused proba tuples (`case_path`, `status`, exact stderr bytes) are byte-identical before/after. Device evidence shows T=1 entries do not dispatch an 8-row work shape and counts useful versus dispatched row work. Exactly one fixed-1000 decode paired-parity capture records per-step wall and GEMV FMA/row-work delta. Expected effect retained: remove about 7/8 of decode GEMV FMA work. |
| `measurement_commands` | From `/Users/ianzepp/work/faberlang/radix`: `scripta/parity run --stage full --output-dir /Users/ianzepp/work/faberlang/gradus/docs/factory/perf-gap-closure/evidence/PGC-B2/parity-raw`; then `scripta/parity reduce /Users/ianzepp/work/faberlang/gradus/docs/factory/perf-gap-closure/evidence/PGC-B2/parity-raw --out /Users/ianzepp/work/faberlang/gradus/docs/factory/perf-gap-closure/evidence/PGC-B2/parity-receipt.json`; then append-only candidate `scripta/parity baseline /Users/ianzepp/work/faberlang/gradus/docs/factory/perf-gap-closure/evidence/PGC-B2/parity-raw --baselines-dir /Users/ianzepp/work/faberlang/gradus/docs/factory/perf-gap-closure/evidence/PGC-B2/baseline-candidate --receipt-out /Users/ianzepp/work/faberlang/gradus/docs/factory/perf-gap-closure/evidence/PGC-B2/baseline-candidate.md`. Raw capture, reduced receipt, candidate baseline, and GEMV/row-work delta evidence live under `gradus/docs/factory/perf-gap-closure/evidence/PGC-B2/`; a lesser stage is not baseline-grade. |
| `depends_on` | none |
| `sanity` | Emitted Metal for one projection and `lm_head_gemv` has one-row work, valid barriers, and identical readback for a pinned input. |
| `non_goals` | No dynamic attention extent (B1), KV rewrite (B3), prefill GEMM tuning (C4), fusion, or numerical-order change. |
| `risk` | high — specialization must retain tail, barrier, and weight-layout laws. |
| `integrable` | yes — one defect, named entry regions, packet fold |
| `parallel_group` | `PGC-W1B-1` |

Evidence retained: current T=1 8×8 geometry performs 8× row work; the report's
static proxy is 3,814,195,200 dispatched versus 476,528,640 useful FMAs.

#### PGC-B3 — direct KV write and compact dynamic constants

| Field | Value |
| --- | --- |
| `id` | `PGC-B3` |
| `outcome` | Replace capacity-scaled full-arena KV append scans with a direct selected-row write and compact runtime selection constants. |
| `write_scope` | Packet `worktrees/pgc-b3/`, branch `factory/pgc-b3`. `gradus/src/kernel.fab` only `kv_append_k` and `kv_append_v`; `gradus/src/kernel.proba` only the named cases `kv_append_k` and `kv_append_v`. New additive-only export test `radix/crates/mir-emit-harness/src/gea3_pipeline_pgc_b3_test.rs`; new additive-only device test `hosts/macos-arm64/tests/gea3_decode_pgc_b3.rs` covering KV append constant construction, launch binding, arena probe, and focused physical assertions. No edits to shared `gea3_pipeline_test.rs` or `gea3_decode.rs`; no prefill KV entries. |
| `done_when` | Focused proba tuples (`case_path`, `status`, exact stderr bytes) are byte-identical before/after. Device test proves only the selected K/V row changes, all prior rows remain identical, no full `[capacity,1]` selector is staged, and certified output remains 1000/1000. Exactly one fixed-1000 decode paired-parity capture records per-step wall, KV write bytes/work, and compact-constant bytes. Expected effect retained: trim per-step KV-side waste. |
| `measurement_commands` | From `/Users/ianzepp/work/faberlang/radix`: `scripta/parity run --stage full --output-dir /Users/ianzepp/work/faberlang/gradus/docs/factory/perf-gap-closure/evidence/PGC-B3/parity-raw`; then `scripta/parity reduce /Users/ianzepp/work/faberlang/gradus/docs/factory/perf-gap-closure/evidence/PGC-B3/parity-raw --out /Users/ianzepp/work/faberlang/gradus/docs/factory/perf-gap-closure/evidence/PGC-B3/parity-receipt.json`; then append-only candidate `scripta/parity baseline /Users/ianzepp/work/faberlang/gradus/docs/factory/perf-gap-closure/evidence/PGC-B3/parity-raw --baselines-dir /Users/ianzepp/work/faberlang/gradus/docs/factory/perf-gap-closure/evidence/PGC-B3/baseline-candidate --receipt-out /Users/ianzepp/work/faberlang/gradus/docs/factory/perf-gap-closure/evidence/PGC-B3/baseline-candidate.md`. Raw capture, reduced receipt, candidate baseline, and KV work evidence live under `gradus/docs/factory/perf-gap-closure/evidence/PGC-B3/`; a lesser stage is not baseline-grade. |
| `depends_on` | none |
| `sanity` | Probe first, middle, and last legal positions plus the capacity boundary; row lineage and arena bounds stay exact. |
| `non_goals` | No decode attention extent change (B1), GEMV specialization (B2), prefill KV rewrite, cache API redesign, or fusion. |
| `risk` | high — an in-place selected-row update must preserve dependency ordering and cannot race attention reads. |
| `integrable` | yes — one defect, named entry regions, packet fold |
| `parallel_group` | `PGC-W1A` |

Evidence retained: current append scans the full KV arena and scales with
capacity. The fixed report estimates about 180.224 MB K/V read+write per step
versus roughly 81.9 KB for direct K/V row writes.

#### PGC-C1 — true embedding gather

| Field | Value |
| --- | --- |
| `id` | `PGC-C1` |
| `outcome` | Implement embedding as direct token-row gather rather than dense one-hot matrix multiplication. |
| `write_scope` | Packet `worktrees/pgc-c1/`, branch `factory/pgc-c1`. `gradus/src/kernel.fab` only `embedding_gather` and its prefill-shaped use; `gradus/src/kernel.proba` only embedding cases. This fold owns `radix/crates/radix-mir/src/kernel_plan/plan.rs`, `radix/crates/radix-mir/src/kernel_plan/build.rs`, and `radix/crates/radix-mir/src/kernel_plan/kernel_plan_test.rs` only for gather admission facts. For Metal: `radix/crates/radix-mir-metal/src/emit/gather.rs` and `radix/crates/radix-mir-metal/src/emit/tests/gather.rs` only. New additive-only export test `radix/crates/mir-emit-harness/src/gea3_pipeline_pgc_c1_test.rs`; new additive-only device test `hosts/macos-arm64/tests/gea3_decode_pgc_c1.rs` covering compact token-id binding and embedding physical assertions. No edits to shared `gea3_pipeline_test.rs` or `gea3_decode.rs`. |
| `done_when` | Focused proba tuples (`case_path`, `status`, exact stderr bytes) are byte-identical before/after. Device proof reads exactly the selected rows and stages compact token ids rather than a `36 × 49,152` one-hot selector. Exactly one fixed-1000 prefill paired-parity capture records prefill wall and embedding FMA/staged-byte delta. Expected effect retained: remove a large share of the 3.73B avoidable embedding-plus-head FMAs; embedding's reported component is 1,698,693,120 scalar MAC iterations, replaced by 36 × 960 row copies. |
| `measurement_commands` | From `/Users/ianzepp/work/faberlang/radix`: `scripta/parity run --stage full --output-dir /Users/ianzepp/work/faberlang/gradus/docs/factory/perf-gap-closure/evidence/PGC-C1/parity-raw`; then `scripta/parity reduce /Users/ianzepp/work/faberlang/gradus/docs/factory/perf-gap-closure/evidence/PGC-C1/parity-raw --out /Users/ianzepp/work/faberlang/gradus/docs/factory/perf-gap-closure/evidence/PGC-C1/parity-receipt.json`; then append-only candidate `scripta/parity baseline /Users/ianzepp/work/faberlang/gradus/docs/factory/perf-gap-closure/evidence/PGC-C1/parity-raw --baselines-dir /Users/ianzepp/work/faberlang/gradus/docs/factory/perf-gap-closure/evidence/PGC-C1/baseline-candidate --receipt-out /Users/ianzepp/work/faberlang/gradus/docs/factory/perf-gap-closure/evidence/PGC-C1/baseline-candidate.md`. Raw capture, reduced receipt, candidate baseline, and embedding FMA/staged-byte evidence live under `gradus/docs/factory/perf-gap-closure/evidence/PGC-C1/`; a lesser stage is not baseline-grade. |
| `depends_on` | none |
| `sanity` | Duplicate and boundary token ids gather byte-identical rows in source order; invalid ids fail under the existing bounds law. |
| `non_goals` | No terminal-head narrowing (C2), RMSNorm (C3), general GEMM tuning (C4), staging cleanup outside the selector (C5), or fusion. |
| `risk` | medium — tied embedding storage and layout must remain one physical buffer with exact row indexing. |
| `integrable` | yes — one defect, named entry regions, packet fold |
| `parallel_group` | `PGC-W1B-2` |

#### PGC-C2 — terminal-row-only prefill logits

| Field | Value |
| --- | --- |
| `id` | `PGC-C2` |
| `outcome` | Compute and observe only the final prompt row's logits during prefill instead of all 36 rows. |
| `write_scope` | Packet `worktrees/pgc-c2/`, branch `factory/pgc-c2`. `gradus/src/kernel.fab` read-only verification scope: the prefill terminal-row call-site/view wiring that selects row 35; no Gradus source edit. `gradus/src/kernel.proba` read-only verification scope: the live cases `src/kernel.proba:test "gea3u3c_head_rmsnorm_static_f32_shape"` and `src/kernel.proba:test "gea3u3c_lm_head_gemv_static_f32_shape"`; no proba edit. New additive-only export test `radix/crates/mir-emit-harness/src/gea3_pipeline_pgc_c2_test.rs` covering the final-row view pin and output count; new additive-only device test `hosts/macos-arm64/tests/gea3_decode_pgc_c2.rs` covering terminal-row binding, logits readback, and physical assertions. No edits to shared `gea3_pipeline_test.rs` or `gea3_decode.rs`; `lm_head_gemv` remains B2-owned and `head_rmsnorm` remains C3-owned. |
| `done_when` | Export and device tests prove the prefill terminal head consumes row 35 through the existing decode-shaped entry, emits 49,152 logits rather than `36 × 49,152`, and selects the same next token. The card records `git diff --exit-code -- gradus/src/kernel.fab gradus/src/kernel.proba` as the explicit verify-untouched proof. For every named Gradus proba case, the before/after tuple (`case_path`, `status`, exact stderr bytes) is byte-identical. Exactly one fixed-1000 prefill paired-parity capture records prefill wall, lm-head FMA count, and logits readback bytes. Expected effect retained: about 36× less lm-head prefill work; remove 1,651,507,200 of 1,698,693,120 scalar MAC iterations and shrink readback 36× to 196,608 B. |
| `measurement_commands` | From `/Users/ianzepp/work/faberlang/radix`: `scripta/parity run --stage full --output-dir /Users/ianzepp/work/faberlang/gradus/docs/factory/perf-gap-closure/evidence/PGC-C2/parity-raw`; then `scripta/parity reduce /Users/ianzepp/work/faberlang/gradus/docs/factory/perf-gap-closure/evidence/PGC-C2/parity-raw --out /Users/ianzepp/work/faberlang/gradus/docs/factory/perf-gap-closure/evidence/PGC-C2/parity-receipt.json`; then append-only candidate `scripta/parity baseline /Users/ianzepp/work/faberlang/gradus/docs/factory/perf-gap-closure/evidence/PGC-C2/parity-raw --baselines-dir /Users/ianzepp/work/faberlang/gradus/docs/factory/perf-gap-closure/evidence/PGC-C2/baseline-candidate --receipt-out /Users/ianzepp/work/faberlang/gradus/docs/factory/perf-gap-closure/evidence/PGC-C2/baseline-candidate.md`. Raw capture, reduced receipt, candidate baseline, terminal-row FMA/readback evidence, and the explicit Gradus no-diff proof live under `gradus/docs/factory/perf-gap-closure/evidence/PGC-C2/`; a lesser stage is not baseline-grade. |
| `depends_on` | none |
| `sanity` | Compare the final-row vector and argmax from old full-row fixture evidence to the new one-row observation byte-for-byte. |
| `non_goals` | No embedding gather (C1), RMSNorm recipe change (C3), general GEMM tuning (C4), or token sampling change. |
| `risk` | medium — final-row view arithmetic must not select row 34/36 or alter tied-weight layout. |
| `integrable` | yes — one defect, named entry regions, packet fold |
| `parallel_group` | `PGC-W1A` |

#### PGC-C3 — single-pass RMSNorm

| Field | Value |
| --- | --- |
| `id` | `PGC-C3` |
| `outcome` | Reduce each 960-wide row once, then normalize its outputs, rather than rescanning the row once per output element. |
| `write_scope` | Packet `worktrees/pgc-c3/`, branch `factory/pgc-c3`. `gradus/src/kernel.fab` only `prefill_rmsnorm` and `head_rmsnorm` recipe uses; `gradus/src/kernel.proba` only norm cases. This fold owns `radix/crates/radix-mir/src/kernel_plan/plan.rs`, `radix/crates/radix-mir/src/kernel_plan/build.rs`, and `radix/crates/radix-mir/src/kernel_plan/kernel_plan_test.rs` only for RMS-normalization plan facts. For Metal: `radix/crates/radix-mir-metal/src/emit/rmsnorm.rs` and `radix/crates/radix-mir-metal/src/emit/tests/rmsnorm.rs` only. New additive-only export test `radix/crates/mir-emit-harness/src/gea3_pipeline_pgc_c3_test.rs`; new additive-only device test `hosts/macos-arm64/tests/gea3_decode_pgc_c3.rs` covering RMSNorm recipe/export/device assertions. No edits to shared `gea3_pipeline_test.rs` or `gea3_decode.rs`. |
| `done_when` | Focused proba tuples (`case_path`, `status`, exact stderr bytes) are byte-identical before/after. Device proof counts one reduction per row and pins byte-identical output for the existing f32 fixture. Exactly one fixed-1000 prefill paired-parity capture records prefill wall and RMSNorm reduction/FMA evidence. Expected effect retained: remove approximately 2.15B avoidable operations (reported 2,154,297,600 redundant inner-loop iterations; O(D²) → O(D)). |
| `measurement_commands` | From `/Users/ianzepp/work/faberlang/radix`: `scripta/parity run --stage full --output-dir /Users/ianzepp/work/faberlang/gradus/docs/factory/perf-gap-closure/evidence/PGC-C3/parity-raw`; then `scripta/parity reduce /Users/ianzepp/work/faberlang/gradus/docs/factory/perf-gap-closure/evidence/PGC-C3/parity-raw --out /Users/ianzepp/work/faberlang/gradus/docs/factory/perf-gap-closure/evidence/PGC-C3/parity-receipt.json`; then append-only candidate `scripta/parity baseline /Users/ianzepp/work/faberlang/gradus/docs/factory/perf-gap-closure/evidence/PGC-C3/parity-raw --baselines-dir /Users/ianzepp/work/faberlang/gradus/docs/factory/perf-gap-closure/evidence/PGC-C3/baseline-candidate --receipt-out /Users/ianzepp/work/faberlang/gradus/docs/factory/perf-gap-closure/evidence/PGC-C3/baseline-candidate.md`. Raw capture, reduced receipt, candidate baseline, and RMSNorm evidence live under `gradus/docs/factory/perf-gap-closure/evidence/PGC-C3/`; a lesser stage is not baseline-grade. |
| `depends_on` | none |
| `sanity` | Constant, mixed-sign, and near-epsilon rows preserve current f32 order/epsilon contract and do not cross a barrier unsafely. |
| `non_goals` | No layernorm redesign, terminal-row narrowing (C2), GEMM tuning (C4), fusion, tolerance change, or f16/quantized work. |
| `risk` | high — parallel reduction order can change f32 results; byte-identical proba and pinned device output are mandatory. |
| `integrable` | yes — one defect, named entry regions, packet fold |
| `parallel_group` | `PGC-W1B-3` |

#### PGC-C4 — tuned tiled prefill GEMM recipes

| Field | Value |
| --- | --- |
| `id` | `PGC-C4` |
| `outcome` | Replace scalar untuned 8×8 prefill GEMM emission with the target-owned tiled/vectorized Metal recipe while preserving the language-level tensor `·` source contract. |
| `write_scope` | Packet `worktrees/pgc-c4/`, branch `factory/pgc-c4`. `gradus/src/kernel.fab` only the prefill GEMM entry declarations `prefill_gemm_qo`, `prefill_gemm_kv`, `prefill_gemm_gate_up`, `prefill_gemm_down`, and the shared body used by `prefill_gemm_o`; `gradus/src/kernel.proba` only their cases. This fold owns `radix/crates/radix-mir/src/kernel_plan/plan.rs`, `radix/crates/radix-mir/src/kernel_plan/build.rs`, and `radix/crates/radix-mir/src/kernel_plan/kernel_plan_test.rs` for its plan facts. It also owns `radix/crates/radix-mir-metal/src/emit/matmul.rs` and `radix/crates/radix-mir-metal/src/emit/tests/matmul.rs` only for the prefill recipe. New additive-only export test `radix/crates/mir-emit-harness/src/gea3_pipeline_pgc_c4_test.rs`; new additive-only device test `hosts/macos-arm64/tests/gea3_decode_pgc_c4.rs` covering GEMM recipe/export/device assertions. No edits to shared `gea3_pipeline_test.rs` or `gea3_decode.rs`. |
| `done_when` | Focused proba tuples (`case_path`, `status`, exact stderr bytes) are byte-identical before/after. Device evidence proves the named entries use the target-owned tuned recipe, with valid tail zero-fill/barriers and unchanged f32 outputs. Exactly one fixed-1000 prefill paired-parity capture records prefill wall, dispatched versus useful FMA/padding counts, and GPU-busy efficiency evidence. Expected effect retained: remove the approximately 1.65B padded-FMA class, remove padding waste, and raise GPU-busy efficiency; no wall estimate is invented. |
| `measurement_commands` | From `/Users/ianzepp/work/faberlang/radix`: `scripta/parity run --stage full --output-dir /Users/ianzepp/work/faberlang/gradus/docs/factory/perf-gap-closure/evidence/PGC-C4/parity-raw`; then `scripta/parity reduce /Users/ianzepp/work/faberlang/gradus/docs/factory/perf-gap-closure/evidence/PGC-C4/parity-raw --out /Users/ianzepp/work/faberlang/gradus/docs/factory/perf-gap-closure/evidence/PGC-C4/parity-receipt.json`; then append-only candidate `scripta/parity baseline /Users/ianzepp/work/faberlang/gradus/docs/factory/perf-gap-closure/evidence/PGC-C4/parity-raw --baselines-dir /Users/ianzepp/work/faberlang/gradus/docs/factory/perf-gap-closure/evidence/PGC-C4/baseline-candidate --receipt-out /Users/ianzepp/work/faberlang/gradus/docs/factory/perf-gap-closure/evidence/PGC-C4/baseline-candidate.md`. Raw capture, reduced receipt, candidate baseline, and GEMM FMA/padding evidence live under `gradus/docs/factory/perf-gap-closure/evidence/PGC-C4/`; a lesser stage is not baseline-grade. |
| `depends_on` | none |
| `sanity` | Inspect emitted Metal and run non-multiple tile tails; every workgroup barrier is uniform and padded reads zero-fill without changing valid outputs. |
| `non_goals` | No decode T=1 specialization (B2), embedding gather (C1), terminal-head narrowing (C2), RMSNorm (C3), fusion, MPS dependency, or quantization. |
| `risk` | high — tile/barrier/layout errors can be silently numerically wrong; focused device readback is required. |
| `integrable` | yes — one defect, named entry regions, packet fold |
| `parallel_group` | `PGC-W1B-4` |

#### PGC-C5 — stop re-staging weight-shaped prefill inputs

| Field | Value |
| --- | --- |
| `id` | `PGC-C5` |
| `outcome` | Keep weight-shaped inputs resident and stop presenting them as per-prefill dynamic inputs, without changing model weights or kernel numerics. |
| `write_scope` | Packet `worktrees/pgc-c5/`, branch `factory/pgc-c5`. `gradus/src/kernel.fab` read-only verification scope: prefill weight-input/resource call sites and entry bindings; no Gradus source edit. `gradus/src/kernel.proba` read-only verification scope: these concrete live prefill cases — `src/kernel.proba:test "gea3u3b_prefill_rmsnorm_static_f32_shape"`, `src/kernel.proba:test "gea3u3b_prefill_gemm_qo_static_f32_shape"`, `src/kernel.proba:test "gea3u3b_prefill_gemm_kv_static_f32_shape"`, `src/kernel.proba:test "gea3u3b_prefill_gemm_gate_up_static_f32_shape"`, `src/kernel.proba:test "gea3u3b_prefill_gemm_down_static_f32_shape"`, `src/kernel.proba:test "gea3u3b_prefill_rope_q_static_f32_table_shape"`, `src/kernel.proba:test "gea3u3b_prefill_rope_k_static_f32_table_shape"`, `src/kernel.proba:test "gea3u3b_prefill_kv_write_k_static_f32_block_geometry"`, `src/kernel.proba:test "gea3u3b_prefill_kv_write_v_static_f32_block_geometry"`, `src/kernel.proba:test "gea3u3b_prefill_key_transpose_static_f32_shape"`, `src/kernel.proba:test "gea3u3b_prefill_score_gemm_static_f32_shape"`, `src/kernel.proba:test "gea3u3b_prefill_causal_softmax_static_f32_shape"`, `src/kernel.proba:test "gea3u3b_prefill_context_gemm_static_f32_shape"`, `src/kernel.proba:test "gea3u3b_prefill_swiglu_static_f32_shape"`, and `src/kernel.proba:test "gea3u3b_prefill_residual_add_static_f32_shape"`; no proba edit. New additive-only export test `radix/crates/mir-emit-harness/src/gea3_pipeline_pgc_c5_test.rs` covering prefill resource lifetime/export pins; new additive-only device test `hosts/macos-arm64/tests/gea3_decode_pgc_c5.rs` covering prefill resource preparation, copy-in census, and physical receipt assertions. `hosts/macos-arm64/src/composite_host/session.rs` only if live tracing proves the incorrect lifetime is materialized there; otherwise read-only. No edits to shared `gea3_pipeline_test.rs` or `gea3_decode.rs`; no kernel entry body. |
| `done_when` | Export/device tests prove weight-shaped buffers are once-resident, not copied on each prefill invocation, while mutable activations remain dynamic. Certified outputs remain unchanged. The card records `git diff --exit-code -- gradus/src/kernel.fab gradus/src/kernel.proba` as the explicit verify-untouched proof. For every named Gradus proba case, the before/after tuple (`case_path`, `status`, exact stderr bytes) is byte-identical. Exactly one fixed-1000 prefill paired-parity capture records prefill wall, upload bytes, and copy-in handle count. Expected effect retained: remove the reported 23 MB of weight-shaped restaging and its encode-adjacent wall; the standing report values are 23.0/23.1 MB across 1,089 copy-in handles. |
| `measurement_commands` | From `/Users/ianzepp/work/faberlang/radix`: `scripta/parity run --stage full --output-dir /Users/ianzepp/work/faberlang/gradus/docs/factory/perf-gap-closure/evidence/PGC-C5/parity-raw`; then `scripta/parity reduce /Users/ianzepp/work/faberlang/gradus/docs/factory/perf-gap-closure/evidence/PGC-C5/parity-raw --out /Users/ianzepp/work/faberlang/gradus/docs/factory/perf-gap-closure/evidence/PGC-C5/parity-receipt.json`; then append-only candidate `scripta/parity baseline /Users/ianzepp/work/faberlang/gradus/docs/factory/perf-gap-closure/evidence/PGC-C5/parity-raw --baselines-dir /Users/ianzepp/work/faberlang/gradus/docs/factory/perf-gap-closure/evidence/PGC-C5/baseline-candidate --receipt-out /Users/ianzepp/work/faberlang/gradus/docs/factory/perf-gap-closure/evidence/PGC-C5/baseline-candidate.md`. Raw capture, reduced receipt, candidate baseline, copy-in evidence, and the explicit Gradus no-diff proof live under `gradus/docs/factory/perf-gap-closure/evidence/PGC-C5/`; a lesser stage is not baseline-grade. |
| `depends_on` | none |
| `sanity` | Run two prefill invocations in one prepared session: weight upload count does not increase on the second; activation updates and logits still do. |
| `non_goals` | No kernel source, weight format, quantization, embedding-selector cleanup (C1), KV constant cleanup (B3), general session redesign, or fusion. |
| `risk` | medium — incorrect lifetime promotion could retain mutable request state; only immutable weight-shaped resources qualify. |
| `integrable` | yes — one defect, packet fold |
| `parallel_group` | `PGC-W1A` |

## 3. A-series per-module polish batches

### 3.1 Common full card contract

The following contract is part of every A card, not optional boilerplate:

| Field | Value |
| --- | --- |
| `outcome` | Apply the `PGC-A0` / §1.2 convert-or-record law to exactly one module, driven by that module's `faber check --air --json` tiers and WARN027 rows. Convert hand-written loops/folds to language constructs without semantic drift; leave uncovered sites with an in-code reason. Preserve small typed pure leaves for the kernel-purity-census/dense-typed-assembly fusion chain. |
| `done_when` | Before/after proba tuples are byte-identical for every case: exact `case_path`, `status`, and stderr bytes. The committed evidence records module tier counts for `ADMISSIBLE-KERNEL`, `ADMISSIBLE-ONE-AWAY`, and `WOULD-REJECT`; at least one ranked one-away row moves to admissible when the module has one-away work. WARN027 rows drop to zero, or every survivor has an in-code reason. No expectation, tolerance, order, status, stderr, or error-variant change. If a module's deterministic capture has no actionable one-away or WARN027 row, the card records that machine result and makes no speculative rewrite. |
| `census_commands` | The exact per-card `faber check --air --json`, `faber check --complexity-budget 12`, and applicable `faber check --kernel-complexity-budget 2` commands, with output files and `WARN027` row-count paths, are resolved in §3.2.1. Run before and after; never report a census without its output path. |
| `depends_on` | `PGC-A0` only |
| `sanity` | Re-run `faber check --air --json` and focused module proba from the packet; compare the normalized tier/WARN rows and raw proba tuples to the before capture. |
| `non_goals` | No kernel mega-function; no B/C defect; no compiler, corpus, hosts, skills, other Gradus module, semantic redesign, tolerance change, or work on `WOULD-REJECT` without a covering construct. |
| `risk` | medium — apparently equivalent loop rewrites can change order, error timing, or alias behavior; byte-identical case/status/stderr is the hard oracle. |
| `integrable` | yes — one module, one packet, path-limited commit |
| `parallel_group` | `PGC-WA-<n>`; any cards with disjoint module paths may run concurrently after A0 |

Every A batch is non-measurement-bearing. It does not run parity and does not
claim encoder movement. The Mind owns the fusion checkpoint after each landed
A wave (§4). This keeps L84 attribution honest.

### 3.2 Named starting batches

Each row below is a full card consisting of its row plus §3.1. The paths are
exact; no card may touch another row's module.

| `id` | Module outcome focus | `write_scope` | Packet / branch | Parallel group |
| --- | --- | --- | --- | --- |
| `PGC-A1` | tokenizer's 51-site starting density; counter walks, `_in_name` contains-loop, folds/transforms | `gradus/src/tokenizer.fab`; `gradus/src/tokenizer.proba`; batch evidence under `gradus/docs/factory/perf-gap-closure/evidence/PGC-A1/` | `worktrees/pgc-a1/`; `factory/pgc-a1` | `PGC-WA-1` |
| `PGC-A2` | cache's 33-site starting density | `gradus/src/cache.fab`; `gradus/src/cache.proba`; `gradus/docs/factory/perf-gap-closure/evidence/PGC-A2/` | `worktrees/pgc-a2/`; `factory/pgc-a2` | `PGC-WA-1` |
| `PGC-A3` | math's 31-site starting density | `gradus/src/math.fab`; `gradus/src/math.proba`; `gradus/docs/factory/perf-gap-closure/evidence/PGC-A3/` | `worktrees/pgc-a3/`; `factory/pgc-a3` | `PGC-WA-1` |
| `PGC-A4` | block_verify's 28-site starting density | `gradus/src/block_verify.fab`; `gradus/src/block_verify.proba`; `gradus/docs/factory/perf-gap-closure/evidence/PGC-A4/` | `worktrees/pgc-a4/`; `factory/pgc-a4` | `PGC-WA-1` |
| `PGC-A5` | calibration's 26-site starting density | `gradus/src/calibration.fab`; `gradus/src/calibration.proba`; `gradus/docs/factory/perf-gap-closure/evidence/PGC-A5/` | `worktrees/pgc-a5/`; `factory/pgc-a5` | `PGC-WA-1` |
| `PGC-A6` | sampling's 24-site starting density, including the known accumulator near `sampling.fab:458` and argmax-twin rulings | `gradus/src/sampling.fab`; `gradus/src/sampling.proba`; `gradus/docs/factory/perf-gap-closure/evidence/PGC-A6/` | `worktrees/pgc-a6/`; `factory/pgc-a6` | `PGC-WA-1` |
| `PGC-A7` | serialize's 23-site starting density | `gradus/src/serialize.fab`; `gradus/src/serialize.proba`; `gradus/docs/factory/perf-gap-closure/evidence/PGC-A7/` | `worktrees/pgc-a7/`; `factory/pgc-a7` | `PGC-WA-1` |
| `PGC-A8` | attention host-side/older paths, including known accumulators near `attention.fab:337/350/432`; kernel bodies stay out unless the deterministic census names them | `gradus/src/attention.fab`; `gradus/src/attention.proba`; `gradus/docs/factory/perf-gap-closure/evidence/PGC-A8/` | `worktrees/pgc-a8/`; `factory/pgc-a8` | `PGC-WA-1` |

### 3.2.1 Exact census commands for the named starting cards

The commands below are run from `/Users/ianzepp/work/faberlang/gradus`. Each
line is an exact invocation, not a shorthand. Run the same command once with
`before` and once with `after` in the output filename. The two budget outputs
are the inputs to the named `WARN027` row-count files. A kernel-budget command
may be recorded as `not-applicable` at its same output path only when that
card's AIR JSON proves there are no kernel-marked rows.

- **`PGC-A1` — `src/tokenizer.fab`**
  ```text
  faber check --air --json /Users/ianzepp/work/faberlang/gradus/src/tokenizer.fab > /Users/ianzepp/work/faberlang/gradus/docs/factory/perf-gap-closure/evidence/PGC-A1/air-before.json
  faber check --complexity-budget 12 /Users/ianzepp/work/faberlang/gradus/src/tokenizer.fab > /Users/ianzepp/work/faberlang/gradus/docs/factory/perf-gap-closure/evidence/PGC-A1/complexity-before.txt 2>&1
  faber check --kernel-complexity-budget 2 /Users/ianzepp/work/faberlang/gradus/src/tokenizer.fab > /Users/ianzepp/work/faberlang/gradus/docs/factory/perf-gap-closure/evidence/PGC-A1/kernel-complexity-before.txt 2>&1
  ```
  After paths are `air-after.json`, `complexity-after.txt`, and
  `kernel-complexity-after.txt` in the same directory. WARN027 row counts are
  `warn027-before.rows` and `warn027-after.rows`.

- **`PGC-A2` — `src/cache.fab`**
  ```text
  faber check --air --json /Users/ianzepp/work/faberlang/gradus/src/cache.fab > /Users/ianzepp/work/faberlang/gradus/docs/factory/perf-gap-closure/evidence/PGC-A2/air-before.json
  faber check --complexity-budget 12 /Users/ianzepp/work/faberlang/gradus/src/cache.fab > /Users/ianzepp/work/faberlang/gradus/docs/factory/perf-gap-closure/evidence/PGC-A2/complexity-before.txt 2>&1
  faber check --kernel-complexity-budget 2 /Users/ianzepp/work/faberlang/gradus/src/cache.fab > /Users/ianzepp/work/faberlang/gradus/docs/factory/perf-gap-closure/evidence/PGC-A2/kernel-complexity-before.txt 2>&1
  ```
  After paths are `air-after.json`, `complexity-after.txt`, and
  `kernel-complexity-after.txt` in the same directory. WARN027 row counts are
  `warn027-before.rows` and `warn027-after.rows`.

- **`PGC-A3` — `src/math.fab`**
  ```text
  faber check --air --json /Users/ianzepp/work/faberlang/gradus/src/math.fab > /Users/ianzepp/work/faberlang/gradus/docs/factory/perf-gap-closure/evidence/PGC-A3/air-before.json
  faber check --complexity-budget 12 /Users/ianzepp/work/faberlang/gradus/src/math.fab > /Users/ianzepp/work/faberlang/gradus/docs/factory/perf-gap-closure/evidence/PGC-A3/complexity-before.txt 2>&1
  faber check --kernel-complexity-budget 2 /Users/ianzepp/work/faberlang/gradus/src/math.fab > /Users/ianzepp/work/faberlang/gradus/docs/factory/perf-gap-closure/evidence/PGC-A3/kernel-complexity-before.txt 2>&1
  ```
  After paths are `air-after.json`, `complexity-after.txt`, and
  `kernel-complexity-after.txt` in the same directory. WARN027 row counts are
  `warn027-before.rows` and `warn027-after.rows`.

- **`PGC-A4` — `src/block_verify.fab`**
  ```text
  faber check --air --json /Users/ianzepp/work/faberlang/gradus/src/block_verify.fab > /Users/ianzepp/work/faberlang/gradus/docs/factory/perf-gap-closure/evidence/PGC-A4/air-before.json
  faber check --complexity-budget 12 /Users/ianzepp/work/faberlang/gradus/src/block_verify.fab > /Users/ianzepp/work/faberlang/gradus/docs/factory/perf-gap-closure/evidence/PGC-A4/complexity-before.txt 2>&1
  faber check --kernel-complexity-budget 2 /Users/ianzepp/work/faberlang/gradus/src/block_verify.fab > /Users/ianzepp/work/faberlang/gradus/docs/factory/perf-gap-closure/evidence/PGC-A4/kernel-complexity-before.txt 2>&1
  ```
  After paths are `air-after.json`, `complexity-after.txt`, and
  `kernel-complexity-after.txt` in the same directory. WARN027 row counts are
  `warn027-before.rows` and `warn027-after.rows`.

- **`PGC-A5` — `src/calibration.fab`**
  ```text
  faber check --air --json /Users/ianzepp/work/faberlang/gradus/src/calibration.fab > /Users/ianzepp/work/faberlang/gradus/docs/factory/perf-gap-closure/evidence/PGC-A5/air-before.json
  faber check --complexity-budget 12 /Users/ianzepp/work/faberlang/gradus/src/calibration.fab > /Users/ianzepp/work/faberlang/gradus/docs/factory/perf-gap-closure/evidence/PGC-A5/complexity-before.txt 2>&1
  faber check --kernel-complexity-budget 2 /Users/ianzepp/work/faberlang/gradus/src/calibration.fab > /Users/ianzepp/work/faberlang/gradus/docs/factory/perf-gap-closure/evidence/PGC-A5/kernel-complexity-before.txt 2>&1
  ```
  After paths are `air-after.json`, `complexity-after.txt`, and
  `kernel-complexity-after.txt` in the same directory. WARN027 row counts are
  `warn027-before.rows` and `warn027-after.rows`.

- **`PGC-A6` — `src/sampling.fab`**
  ```text
  faber check --air --json /Users/ianzepp/work/faberlang/gradus/src/sampling.fab > /Users/ianzepp/work/faberlang/gradus/docs/factory/perf-gap-closure/evidence/PGC-A6/air-before.json
  faber check --complexity-budget 12 /Users/ianzepp/work/faberlang/gradus/src/sampling.fab > /Users/ianzepp/work/faberlang/gradus/docs/factory/perf-gap-closure/evidence/PGC-A6/complexity-before.txt 2>&1
  faber check --kernel-complexity-budget 2 /Users/ianzepp/work/faberlang/gradus/src/sampling.fab > /Users/ianzepp/work/faberlang/gradus/docs/factory/perf-gap-closure/evidence/PGC-A6/kernel-complexity-before.txt 2>&1
  ```
  After paths are `air-after.json`, `complexity-after.txt`, and
  `kernel-complexity-after.txt` in the same directory. WARN027 row counts are
  `warn027-before.rows` and `warn027-after.rows`.

- **`PGC-A7` — `src/serialize.fab`**
  ```text
  faber check --air --json /Users/ianzepp/work/faberlang/gradus/src/serialize.fab > /Users/ianzepp/work/faberlang/gradus/docs/factory/perf-gap-closure/evidence/PGC-A7/air-before.json
  faber check --complexity-budget 12 /Users/ianzepp/work/faberlang/gradus/src/serialize.fab > /Users/ianzepp/work/faberlang/gradus/docs/factory/perf-gap-closure/evidence/PGC-A7/complexity-before.txt 2>&1
  faber check --kernel-complexity-budget 2 /Users/ianzepp/work/faberlang/gradus/src/serialize.fab > /Users/ianzepp/work/faberlang/gradus/docs/factory/perf-gap-closure/evidence/PGC-A7/kernel-complexity-before.txt 2>&1
  ```
  After paths are `air-after.json`, `complexity-after.txt`, and
  `kernel-complexity-after.txt` in the same directory. WARN027 row counts are
  `warn027-before.rows` and `warn027-after.rows`.

- **`PGC-A8` — `src/attention.fab`**
  ```text
  faber check --air --json /Users/ianzepp/work/faberlang/gradus/src/attention.fab > /Users/ianzepp/work/faberlang/gradus/docs/factory/perf-gap-closure/evidence/PGC-A8/air-before.json
  faber check --complexity-budget 12 /Users/ianzepp/work/faberlang/gradus/src/attention.fab > /Users/ianzepp/work/faberlang/gradus/docs/factory/perf-gap-closure/evidence/PGC-A8/complexity-before.txt 2>&1
  faber check --kernel-complexity-budget 2 /Users/ianzepp/work/faberlang/gradus/src/attention.fab > /Users/ianzepp/work/faberlang/gradus/docs/factory/perf-gap-closure/evidence/PGC-A8/kernel-complexity-before.txt 2>&1
  ```
  After paths are `air-after.json`, `complexity-after.txt`, and
  `kernel-complexity-after.txt` in the same directory. WARN027 row counts are
  `warn027-before.rows` and `warn027-after.rows`.

### 3.3 Deterministically admitted continuation batches (`PGC-A9..An`)

The ellipsis in goal §5 is retained rather than narrowed. After the named
starting wave, the Mind captures a repo-wide `faber check --air --json` and
WARN027 census. For every remaining module with at least one
`ADMISSIBLE-ONE-AWAY` row or actionable WARN027 row, the Mind mints exactly one
card `PGC-A9..An` from §3.1 in stable module-path order.

For a module `src/<module>.fab`, the exact write scope is:

- `gradus/src/<module>.fab`;
- its existing `gradus/src/<module>.proba`;
- `gradus/docs/factory/perf-gap-closure/evidence/<card-id>/` for before/after
  census and proba tuples.

For a nested module, `<module>` retains the relative path, such as
`model/moe`. Packet and branch are `worktrees/pgc-<lowercase-id>/` and
`factory/pgc-<lowercase-id>`. A generated card inherits every field in §3.1,
cites `PGC-A0` and §1.2, and is gated only on A0. At mint time the Mind must
copy §3.2.1 with literal module/card paths into the card: `faber check
--air --json` writes `air-before.json`/`air-after.json`,
`faber check --complexity-budget 12` writes the regular-budget outputs, and
`faber check --kernel-complexity-budget 2` is run or explicitly marked
not-applicable from the AIR rows. The card names
`warn027-before.rows`/`warn027-after.rows` under its evidence directory. No
`<module>` or `<card-id>` placeholder is accepted in a dispatched card. The
Mind may group disjoint cards into `PGC-WA-2`, `PGC-WA-3`, and later waves for
fold capacity, but may not discard a machine-admitted module or add
cross-card dependencies.

Modules with only `WOULD-REJECT` rows receive a census disposition and no
rewrite card. That is the goal's honest far-set rule, not scope removal.

## 4. Mind-owned measurement checkpoints

These checkpoints are control-plane work, not implementation units. They
never become dependencies between B/C/A cards. Each checkpoint uses the
standing baseline and records full-stage AC paired parity when AC is available;
a labeled non-AC capture may be evidence but does not replace an AC baseline.
Every checkpoint is append-only and applies L84 per-track attribution.

| Checkpoint | Trigger | Mechanical record |
| --- | --- | --- |
| `PGC-M0` | D1 landed | Re-capture one fixed-1000 decode receipt and certify timestamp coverage/labels. No speed attribution to D1. |
| `PGC-MB` | each B card lands, and once after all landed B cards are folded | Preserve each card's own fixed-1000 decode paired delta; run one integrated paired capture against the standing baseline. Record counts, wall, encoder count, affected work evidence, and do not sum overlapping wall deltas as causal arithmetic. |
| `PGC-MC` | each C card lands, and once after all landed C cards are folded | Preserve each card's own fixed-1000 prefill paired delta; run one integrated paired capture against the standing baseline. Record counts, wall, FMAs/work bytes, encoder count, and retain the compute-bound interpretation rather than a 1.4 GB bandwidth-floor claim. |
| `PGC-MA<n>` | each A wave is folded | Run one paired full-stage capture against the standing baseline. Record `ADMISSIBLE-KERNEL` / `ADMISSIBLE-ONE-AWAY` / `WOULD-REJECT` and WARN027 totals from the wave's committed evidence, then measure encoders per decode step. Starting encoder count is 2,115; goal-level target is hundreds. Attribute encoder movement to the integrated A wave only, never to an individual non-measurement-bearing A card. |
| `PGC-MFINAL` | all admitted B, C, and deterministic A batches are folded | Run the full AC paired inventory for short and fixed-1000 decode and prefill. Report all four rates/ratios, 1000/1000 gradus fixed-output certification, phase walls, full encoder coverage, encoder count, and complete three-repo pins against the standing baseline. Evaluate the 10–15 ms / 65–100 t/s hypothesis honestly; do not turn it into a gate or promise. |

The fusion payoff metric is encoders per decode step: the measured start is
2,115, including approximately 1,440 per-head pieces averaging 11.6 µs GPU
work in the partial sample. The target is hundreds after A-wave purity enables
AIR fusion. D1 must land before any checkpoint treats GPU-busy coverage as
complete, but D1 does not block implementation.

## 5. Integration and closeout

Every implementation card is independently integrable. The Mind folds the
`PGC-W1A` packet commits serially within their declared `kernel.fab` entry
regions, then folds the `PGC-W1B-1` through `PGC-W1B-4` packets in order, then
folds A packets by wave, and advances goal status in the same reconciliation
turn. The 1b order is the mechanical resolution for the shared kernel-plan
and Metal matmul implementation files; no semantic overlap is hidden behind
that order. Outside the explicit `kernel.fab` entry-region exception, shared
files are not a concurrency mechanism and a scope overlap is a violation.

Unit closeout evidence is the card's mechanical oracle. Broader lint/test/e2e
ownership remains the workspace validation ladder and is named once here
rather than duplicated on every card. No card executes device kernels under
the MIR runner.

## 6. Non-goals and retained source authority

The goal's non-goals remain exact: no MIR-runner device execution (L86); no
quantization (f32 parity is the contract); no CUDA arm (blocked on hosts need
`411b16f3`, carried by gradus-llama-parity); no llama.cpp changes (the
comparator stays pinned); and no new model rung.

Evidence authority remains all six Vivi reports cited by the goal: prefill
audit `c1640a4e`; decode audits `ded525e1` / `02f34add`; fixed-1000 decode
inspector `c0c86fe4`; fixed-1000 prefill inspector `f6b12569`; short prefill
inspector `06a62904` + `051731ac`; short decode inspector `b1c7f917`.
Independent Luna and GLM families converged on encoder count, serialization,
capacity defects, and instrument defects, and both corrected the partial
sample and prefill bandwidth-floor errors. Operator commentary 2026-08-27
owns the fusion pre-work chain, anti-prior law, closure intrinsics, and
`--air` / `--complexity-budget` deterministic-driver contract.

## 7. Reopen package — amended unit graph (PGC-R series, 2026-08-28)

Added by planner under Vivi task `a7a9ffb5` from Mind memo `cbc68961`
(reopen package), CTO#1 mail `1bbfce59`, CTO#2 mail `54e48e56` (the sol
seat — amendments govern where the two differ), GAP findings
`f7f5dbd3` / `5f3b144d` / `b1c7f917` / `06a62904`+`051731ac`, and
B2-RETUNE close `82dc3199`. This section governs all reopen work; §1–§6
remain the record of waves 0–1 and keep their folded cards' authority.

### 7.0 Supersession and the landed-inliner constraint

| Old card | Disposition under §7 |
| --- | --- |
| `PGC-C1` (embedding gather) | **Superseded by `PGC-R1`** — do not dispatch C1 as written |
| `PGC-C2` (terminal-row logits) | Folded 2026-08-27 (LM-head FMAs 1.70B→47.2M); remaining producer-fact verification owned by `PGC-R2` |
| `PGC-C3` (single-pass RMSNorm) | **Superseded by `PGC-R5`** (row-reduction family widened to prefill softmax) — do not dispatch C3 as written |
| `PGC-C4` (tiled prefill GEMM) | **Superseded by `PGC-R4`** (vectorized prefill GEMM recipe class) — do not dispatch C4 as written |
| `PGC-C5` (resident weights) | Folded; owed full-stage capture + missing evidence dir owned by `PGC-R3` |
| `PGC-B1` (bucketed extents) | Folded; owed full-stage delta, physical gate, and missing evidence dir owned by `PGC-R3` |

**Landed-inliner law.** Semantic device-to-device call composition is LANDED
(radix `fae613683`, DFV2-4: `radix-module/src/mir/fragment_composition.rs`,
run post-monomorphization from `mir/lower.rs:363` and
`package_instantiate.rs:304`). No card in this delivery mints an inliner,
duplicates that pass, or adds an MSL device-function fallback rung — budget
overflow fails closed by the landed contract. The open work is
target-neutral **launch fusion / intermediate-materialization elision** at
the decomposition/DeviceProgram seam, per
`radix/docs/design/operation-fusion.md`, plus bounded Gradus corpus
adoption. The operation-fusion design's Units 1–2 (typed elementwise plan +
decomposition attachment) are also already landed as OF-1 `3d8ce4d8a6` and
OF-2 `aebec9180` (`radix-mir/src/elementwise_plan.rs`,
`kernel_decomposition.rs`); what is unbuilt is the backend consumer and the
corpus that exercises it.

### 7.1 Amended measurement law for R cards

These riders amend §1.1 for every R card. Where a rider and §1–§6 conflict,
the rider governs R cards.

**Condition-B rider (CTO#1 E(a) / CTO#2, binding).** L2/L3 units claim
**FMA / work-census / staged-byte / launch-graph deltas as primary
evidence**. Wall deltas (t/s, ms/step) are **L1-gated secondary
observations**: they may be reported only family-keyed against the re-keyed
baseline, with the L1 dispatch-shell state named (encoders per step, launch
encode ms), and are never the card's pass oracle. The corrected record
behind this: true decode idle is ~3.3 ms/step and the honest launch-boundary
class is ~6–10 ms/step (sample-cap correction, `5f3b144d`), not the
superseded ~28 ms reading; prefill is body-efficiency dominated (~50.6 ms
GPU busy at ~0.51 vs llama ~2.3 effective TFLOP/s on the same 26 GFLOP).

**Two-class numeric oracle (CTO#2 Q5, per `operation-fusion.md` §6).**
Byte/exact identity is the landing target **only** where the operation
contract and emitted form prove the change has no observable rounding,
contraction, or materialization effect (the B2 class: dispatch-shape change,
arithmetic untouched). Otherwise the frozen per-family numeric contract
applies — compared against the unfused/old output, **never widened after
observation**. Every R card states which class its change is in. Launch
count, geometry, slot/resource/version, and intermediate-materialization
deltas are pinned separately wherever they move; a numeric pass that hides a
launch-graph change is not a pass.

**Baseline family.** R cards measure against the gradus-llama-parity
baseline family of record (GLP U5 landed; first AC baseline
`radix/scripta/parity-baselines/`; relocated from the pre-9ed67b081 path `radix/docs/factory/gradus-llama-parity/baselines/`), re-keyed by `PGC-R3`
after the algebraic cards and the B2-RETUNE landing (w16, `82dc3199`,
KEEP at 16.44 t/s vs 15.77 baseline). Until R3 lands, no R card claims a
wall delta.

**Closeout-command correction (defect fix; three seats confirmed).** Any
closeout or proof command citing `exempla_rust_canonical` must name the rust
lane explicitly:

```text
cargo test -p exempla --no-default-features --features hir-rust --test e2e_harness exempla_rust_canonical -- --ignored --nocapture
```

`exempla`'s default feature set is empty (`radix/crates/exempla/Cargo.toml`
— per-lane default-off), so the bare form recorded in the test's own ignore
attribute compiles no lane and fails. R cards and any Mind-minted closeout
use the corrected form verbatim.

### 7.2 Parked delivery-repair findings — closed into this artifact

The three PGC-DELIVERY-REPAIR findings were repaired on the pre-reopen text
(gradus `afdf79d`, `6f70767`, `0b1db1e`). Their laws carry into every R
card and are hereby closed against §7:

| Finding | Law carried into §7 |
| --- | --- |
| `7c97ff62` (wave overlap) | Per-card additive test files for all new tests (`gea3_pipeline_pgc_r<N>_test.rs`, `hosts/macos-arm64/tests/gea3_decode_pgc_r<N>.rs`); no R card appends new cases to shared `gea3_pipeline_test.rs` / `gea3_decode.rs` — a card touches those two files only inside its named entry pin regions (the B1/B2 amended mechanism), with regions declared on the card; shared `kernel.fab` / `kernel.proba` handled by disjoint entry/case ownership with serial Mind folds; `kernel_plan/{plan,build,kernel_plan_test}.rs` never live in two cards (§7.3 order) |
| `ec594fd` (C2/C5 vertical narrowing) | Every host/export-only R card declares its Gradus entry/case scope explicitly (verify-untouched allowed only with the `git diff --exit-code` proof artifact) and captures the `(case_path, status, stderr bytes)` tuple oracle for every named case |
| `01fd4c61` (phantom proba names) | R cards name only live `src/kernel.proba` identifiers (verified 2026-08-28 against `gradus/src/kernel.proba`); no unbounded phrases like "existing prefill cases" |

### 7.3 R-wave structure

Execution order is the amended CTO#2 order: algebraic fixes → re-census /
baseline re-key → prefill body efficiency → launch-fusion lane (parallel
architecture track) → L13 encoder construction. `PGC-R6` is architecture
and runs parallel with `PGC-R4`/`PGC-R5` (CTO#2 Q3.5); nothing else
reorders.

| Wave | Cards | Mode / packet |
| --- | --- | --- |
| `R-W1` | `PGC-R1` ∥ `PGC-R2` (disjoint `kernel.fab` entry regions: embedding vs head) | packets `worktrees/pgc-r1/`, `worktrees/pgc-r2/` (`factory/pgc-r1`, `factory/pgc-r2`) |
| `R-W2` | `PGC-R3` alone | direct mode (captures + docs; no source) |
| `R-W3` | `PGC-R4` → `PGC-R5` (serial on `kernel_plan/` trio); `PGC-R6` ∥ both (emit files disjoint) | packets `worktrees/pgc-r4|r5|r6/` |
| `R-W4` | `PGC-R7` after `PGC-R6` + `PGC-R3` | packet `worktrees/pgc-r7/` |
| `R-W5` | `PGC-R8` after `PGC-R3` | direct mode (hosts-only, path-limited) |

File-disjointness inside `R-W3`: `PGC-R4` owns
`emit/matmul.rs` + `emit/tests/matmul.rs`; `PGC-R5` owns `emit/rmsnorm.rs`,
`emit/causal_softmax.rs` + their tests; `PGC-R6` owns `emit/elementwise.rs`,
`emit/recipes.rs`, the elementwise path of `emit/mod.rs`, and additive
`radix-mir/src/elementwise_plan*.rs` accessors. The
`kernel_plan/{plan,build,kernel_plan_test}.rs` trio is owned by `PGC-R4`
then folded to `PGC-R5` serially through the Mind.

### 7.4 Unit cards

#### PGC-R1 — indexed prefill embedding gather

| Field | Value |
| --- | --- |
| `id` | `PGC-R1` |
| `outcome` | Replace the dense one-hot embedding matmul with a direct indexed token-row copy kernel, prefill (`[36,49152]·[49152,960]` selector matmul → 36 row copies) and the shared entry's decode use. Supersedes `PGC-C1` and the one-hot idiom's design note at `gradus/src/kernel.fab:601-634` (CTO ruling `0891c09b` superseded by the reopen order). |
| `write_scope` | Packet `worktrees/pgc-r1/`, branch `factory/pgc-r1`. `gradus/src/kernel.fab` only the `embedding_gather` entry and its prefill-shaped use; `gradus/src/kernel.proba` only the live case `src/kernel.proba:test "gea3u3c_embedding_gather_static_f32_shape"`. Radix, only as live inspection requires and named in the report: the existing indexed/gather admission seams (`radix-mir-metal/src/emit/gather.rs`, `emit/literal_indexed.rs`), `kernel_plan/` admission facts if no existing recipe covers a token-indexed row copy (this card owns the trio in its wave; R4/R5 follow), and the embedding-entry pin regions inside `radix/crates/mir-emit-harness/src/gea3_pipeline_test.rs` (these supersede the B2-era T=1 matmul pins for that entry). New additive-only `radix/crates/mir-emit-harness/src/gea3_pipeline_pgc_r1_test.rs`; new additive-only `hosts/macos-arm64/tests/gea3_decode_pgc_r1.rs` (compact token-id binding, no selector upload, physical row-copy assertions). No other kernel entries; no edits to unrelated harness regions. |
| `done_when` | Focused proba tuple (`case_path`, `status`, exact stderr bytes) byte-identical before/after for the named case (two-class note: a row copy has no rounding surface — byte identity is the correct class). Export + device evidence prove no `[36,49152]` one-hot selector is staged (pre-prefill upload drops by ~7.08 MB of the 23.1 MB fixed-1000 staging) and dispatched embedding FMAs fall from the padded 1,887,436,800 (~1.89 GFMA, `06a62904`+`051731ac`: 40-row-padded `[40,49152,960]` vs 36×960 row copies) to zero GEMM-class work. Certified outputs unchanged (1000/1000 on the device test). No per-card wall claim (condition-B rider); wall observations belong to `PGC-R3`'s family capture. Evidence under `gradus/docs/factory/perf-gap-closure/evidence/PGC-R1/`. |
| `depends_on` | none |
| `sanity` | Duplicate and boundary token ids gather byte-identical rows in source order; invalid ids fail under the existing bounds law; tied `[49152,960]` buffer stays one physical allocation. |
| `non_goals` | No terminal-head work (R2), no GEMM recipe work (R4), no decode selector-upload cleanup beyond what the shared entry carries, no fusion, no quantization. |
| `risk` | medium — entry signature change (selector input → token-id input) must keep the plan-bound resource law and the tied-weight layout. |
| `integrable` | yes — one defect, named entry region, packet fold |
| `parallel_group` | `R-W1` |

#### PGC-R2 — final-row-only LM-head contract, producer facts explicit

| Field | Value |
| --- | --- |
| `id` | `PGC-R2` |
| `outcome` | Close the final-row prefill contract with every producer fact proven from live evidence, not from the fold claim. C2 folded the LM-head GEMV (goal Status: FMAs 1.70B→47.2M); CTO#2 requires the complete contract treated as explicit producer facts. The four facts: (a) prefill terminal head consumes row 35 through the decode-shaped entry; (b) prefill LM-head work is final-row-only (47,185,920 FMAs class, not 1,698,693,120 — the 36× evidence, `5f3b144d`); (c) prefill logits readback is one row (196,608 B / 49,152 floats, not `36×49152` / 7,077,888 B); (d) prefill head RMSNorm is final-row-only (`[1,960]` input, not the `[36,960]` 33.2M-FMA full-row scan, `06a62904`). Any unmet fact is implemented in this card's vertical (export pin + device test); every met fact is proven from committed receipts/tests. |
| `write_scope` | Packet `worktrees/pgc-r2/`, branch `factory/pgc-r2`. Gradus verify-untouched scope: `gradus/src/kernel.fab` head-entry regions (`head_rmsnorm`, `lm_head_gemv`) and `gradus/src/kernel.proba` live cases `src/kernel.proba:test "gea3u3c_head_rmsnorm_static_f32_shape"` and `src/kernel.proba:test "gea3u3c_lm_head_gemv_static_f32_shape"` — no Gradus edit; the card records `git diff --exit-code -- gradus/src/kernel.fab gradus/src/kernel.proba` as the explicit no-diff proof. If a producer fact is unmet, the implementation follows the C2 pattern — per-card additive files only: new additive-only `radix/crates/mir-emit-harness/src/gea3_pipeline_pgc_r2_test.rs` (final-row view pin, output count, head-norm row selection) and new additive-only `hosts/macos-arm64/tests/gea3_decode_pgc_r2.rs` (terminal-row binding, readback slice); no edits to shared `gea3_pipeline_test.rs` or `gea3_decode.rs`; no kernel-body source change (row selection is view/plan work). |
| `done_when` | Each of the four producer facts carries committed evidence (export pin assertion, device-test assertion, or receipt field) under `evidence/PGC-R2/`, or was implemented and then proven. Named proba tuples byte-identical before/after (row selection must not perturb kernel numerics — byte-identity class). Device test selects the same next token as the pre-fold fixture. FMA/readback census recorded per fact. No per-card wall claim (condition-B rider). |
| `depends_on` | none |
| `sanity` | Compare final-row vector and argmax byte-for-byte against the C2 fixture evidence (`evidence/PGC-C2/terminal-row-delta.json`); row 34/36 selection or a 35-row off-by-one fails. |
| `non_goals` | No embedding gather (R1), no row-reduction recipe work (R5), no sampling change, no new head entry. |
| `risk` | medium — a mis-selected row is silently plausible; byte-for-byte argmax continuity is the oracle. |
| `integrable` | yes — one contract, packet fold |
| `parallel_group` | `R-W1` |

#### PGC-R3 — post-fix re-census, baseline-family re-key, owed-evidence reconciliation

| Field | Value |
| --- | --- |
| `id` | `PGC-R3` |
| `outcome` | One certified post-retune, post-algebraic family capture that (1) re-keys the parity baseline family (condition-A resolved by `82dc3199`: KEEP w16), (2) discharges the B1/C5 owed evidence (auditor `77ca6b07` P2: `evidence/PGC-B1/` and `evidence/PGC-C5/` absent on main), and (3) re-censuses the corrected launch graph / FMA / staging table (L17) as the fusion-priority input CTO#2 demands — a census before R1/R2 is obsolete by construction. |
| `write_scope` | Direct mode. `gradus/docs/factory/perf-gap-closure/evidence/PGC-R3/` (family capture, reduced receipt, census tables); create and populate `evidence/PGC-B1/` (derive the B1 delta from the family capture **and run the B1 physical gate** — both bucket extents at capacity 1100, hosts `gea3_decode_pgc_b1.rs`) and `evidence/PGC-C5/` (copy-in census derivation + the C5 no-diff proof artifact); append-only baseline-family artifacts under `radix/scripta/parity-baselines/`. No source, no kernel, no test edits. |
| `done_when` | One full-stage paired capture (`scripta/parity run --stage full`) on the folded mains (radix/hosts/gradus post-pgc-b2-final), certified 1000/1000, power AC, three-repo pins recorded; `evidence/PGC-B1/` and `evidence/PGC-C5/` rows stop owing; the census table records per-step encoders, launches per family, launch-encode ms, upload bytes/handles, readback bytes, dispatched vs useful FMAs per entry family, and the two-class-compatible candidate list for fusion waves (compatible launch graph). Wall deltas for R1/R2 are reported here, L1-gated, never on those cards. Baseline re-key respects §7.5's pin ruling (default: keep pre-B3 gradus pin until the operator rules). |
| `measurement_commands` | From `/Users/ianzepp/work/faberlang/radix`: `scripta/parity run --stage full --output-dir /Users/ianzepp/work/faberlang/gradus/docs/factory/perf-gap-closure/evidence/PGC-R3/parity-raw`; `scripta/parity reduce /Users/ianzepp/work/faberlang/gradus/docs/factory/perf-gap-closure/evidence/PGC-R3/parity-raw --out /Users/ianzepp/work/faberlang/gradus/docs/factory/perf-gap-closure/evidence/PGC-R3/parity-receipt.json`; append-only candidate `scripta/parity baseline /Users/ianzepp/work/faberlang/gradus/docs/factory/perf-gap-closure/evidence/PGC-R3/parity-raw --baselines-dir /Users/ianzepp/work/faberlang/radix/scripta/parity-baselines/ --receipt-out /Users/ianzepp/work/faberlang/gradus/docs/factory/perf-gap-closure/evidence/PGC-R3/baseline-candidate.md`. A lesser stage is not baseline-grade. |
| `depends_on` | `PGC-R1`, `PGC-R2` |
| `sanity` | Family identity: same GGUF/statues/env/power as the GLP baseline of record; the capture tree integrates B1+B2(w16)+B3+C2+C5+R1+R2 — the receipt's per-entry census must show every one of those folds present before the re-key is certified. |
| `non_goals` | No source change, no new lever pulled inside the capture, no fusion target selection beyond recording the census, no MIR runner. |
| `risk` | medium — re-key discipline: append-only, never rewrite the standing family; the B1 physical gate must run, not be derived. |
| `integrable` | yes — direct-mode, path-limited commits (gradus evidence + radix baselines) |
| `parallel_group` | `R-W2` |

#### PGC-R4 — simdgroup/vectorized prefill GEMM recipes

| Field | Value |
| --- | --- |
| `id` | `PGC-R4` |
| `outcome` | Replace the scalar 8×8-tile, per-K-slice-barrier prefill GEMM emission with a simdgroup-matrix / vectorized-load recipe (float4 loads, cooperative simdgroup multiply-accumulate, partial-tile guards), preserving the language-level tensor `·` contract. Absorbs `PGC-C4`. Dominant prefill lever: ~0.51 vs ~2.3 effective TFLOP/s on the same 26 GFLOP (`5f3b144d`); the padded-FMA class (~1.65B, 40-row padding of M=36, score 40×40/36×36) falls with real tiles. |
| `write_scope` | Packet `worktrees/pgc-r4/`, branch `factory/pgc-r4`. `gradus/src/kernel.fab` only `prefill_gemm_qo`, `prefill_gemm_kv`, `prefill_gemm_gate_up`, `prefill_gemm_down` and any shared body helper they call (named in the report); `gradus/src/kernel.proba` only the live cases `gea3u3b_prefill_gemm_qo_static_f32_shape`, `gea3u3b_prefill_gemm_kv_static_f32_shape`, `gea3u3b_prefill_gemm_gate_up_static_f32_shape`, `gea3u3b_prefill_gemm_down_static_f32_shape`. Radix: `kernel_plan/{plan,build,kernel_plan_test}.rs` for the recipe plan facts (this card owns the trio in `R-W3`); `radix-mir-metal/src/emit/matmul.rs` + `emit/tests/matmul.rs` only. New additive-only `gea3_pipeline_pgc_r4_test.rs`; new additive-only `hosts/macos-arm64/tests/gea3_decode_pgc_r4.rs`. No edits to `emit/mod.rs`/`recipes.rs` (R6 owns them this wave) or shared harness regions. |
| `done_when` | Focused proba tuples byte-identical where the recipe preserves declared accumulation order; otherwise the frozen per-family tolerance vs the old recipe output, never widened (two-class note: the recipe's accumulate contracts the multiply-add — declare the class per entry in the report). Device evidence: valid tail zero-fill/barriers on M=36/N-multiple edges, dispatched-vs-useful FMA census (padding class gone), and one fixed-1000 prefill paired-parity capture vs the R3 family recording prefill wall + GPU-busy efficiency as **L1-gated secondary** with the FMA/efficiency census primary (condition-B rider). Evidence under `evidence/PGC-R4/`. |
| `measurement_commands` | From `/Users/ianzepp/work/faberlang/radix`: `scripta/parity run --stage full --output-dir /Users/ianzepp/work/faberlang/gradus/docs/factory/perf-gap-closure/evidence/PGC-R4/parity-raw`; then `scripta/parity reduce /Users/ianzepp/work/faberlang/gradus/docs/factory/perf-gap-closure/evidence/PGC-R4/parity-raw --out /Users/ianzepp/work/faberlang/gradus/docs/factory/perf-gap-closure/evidence/PGC-R4/parity-receipt.json`; then append-only candidate `scripta/parity baseline /Users/ianzepp/work/faberlang/gradus/docs/factory/perf-gap-closure/evidence/PGC-R4/parity-raw --baselines-dir /Users/ianzepp/work/faberlang/gradus/docs/factory/perf-gap-closure/evidence/PGC-R4/baseline-candidate --receipt-out /Users/ianzepp/work/faberlang/gradus/docs/factory/perf-gap-closure/evidence/PGC-R4/baseline-candidate.md`. Raw capture, reduced receipt, candidate baseline, and the FMA/efficiency census evidence live under `gradus/docs/factory/perf-gap-closure/evidence/PGC-R4/`; a lesser stage is not baseline-grade. |
| `depends_on` | `PGC-R3` |
| `sanity` | Emitted Metal for one GEMM shows simdgroup ops and no per-K-slice threadgroup barrier pair; non-multiple tails read zero-fill without changing valid outputs. |
| `non_goals` | No decode T=1 work (B2 landed), no row reductions (R5), no fusion (R6/R7), no weight-layout rewrite beyond what the recipe's load contract requires (named if touched), no quantization. |
| `risk` | high — tile/barrier/layout errors are silently numerically wrong; focused device readback and the tolerance declaration are mandatory. |
| `integrable` | yes — one recipe family, packet fold |
| `parallel_group` | `R-W3` |

#### PGC-R5 — vectorized prefill row reductions

| Field | Value |
| --- | --- |
| `id` | `PGC-R5` |
| `outcome` | One SIMD/threadgroup reduction per row, then a vectorized scale pass, for the prefill row-reduction family: `prefill_rmsnorm`/`head_rmsnorm` (O(D²) rescan: 2,156,544,000 iterations → 2,246,400, a 960× class, `06a62904`) and `prefill_causal_softmax` (36× per-column row recompute: 23,016,960 → 639,360 exp-class iterations). Absorbs `PGC-C3` and widens it to the softmax row reduction the same evidence names. |
| `write_scope` | Packet `worktrees/pgc-r5/`, branch `factory/pgc-r5`. `gradus/src/kernel.fab` only `prefill_rmsnorm`, `head_rmsnorm` recipe uses, and `prefill_causal_softmax`; `gradus/src/kernel.proba` only the live cases `gea3u3b_prefill_rmsnorm_static_f32_shape`, `gea3u3c_head_rmsnorm_static_f32_shape`, `gea3u3b_prefill_causal_softmax_static_f32_shape`. Radix: `kernel_plan/{plan,build,kernel_plan_test}.rs` (after R4's fold — serial ownership; `from_contract` match in `build.rs` gains the RowReduction arm); `radix-mir/src/abi/contract.rs` — RowReduction variant (workgroup 32,1,1; dispatch = rows) resolved ONLY for `TensorRmsNorm` + `TensorCausalMaskedSoftmax`; `radix-mir/src/device_program_plans.rs` — `contract_shape_signature` exhaustive match gains the RowReduction arm, `transformer_shape_signature` hands the two ops to the contract path; `mir-emit-harness/src/gea3_pipeline_test.rs` — three-entry launch/plan pin regions only (`launch_for_entry_at` else branch + `plan_for_entry` for prefill_rmsnorm/head_rmsnorm/prefill_causal_softmax; B1/B2 region-ownership precedent); `radix-mir-llvm/src/nvvm/{recipe.rs,nvvm_descriptor.rs}` — named either way per the containment choice (smallest path picked by the seat, named in the receipt); `radix-mir-metal/src/emit/rmsnorm.rs`, `emit/causal_softmax.rs` + `emit/tests/{rmsnorm,causal_softmax}.rs` only. New additive-only `gea3_pipeline_pgc_r5_test.rs`; new additive-only `hosts/macos-arm64/tests/gea3_decode_pgc_r5.rs`. |
| `done_when` | Two-class note governs: a threadgroup row reduction changes summation order — the frozen per-family numeric contract vs the old recipe output is the oracle (never widened), unless a variant preserves declared order and then byte identity holds; declare the class per entry. Proba tuples byte-identical **or** the declared tolerance proof recorded per the class. Device proof counts one reduction per row; FMA/iteration census primary; one fixed-1000 prefill paired-parity capture vs the R3 family with wall as L1-gated secondary. Evidence under `evidence/PGC-R5/`. |
| `measurement_commands` | From `/Users/ianzepp/work/faberlang/radix`: `scripta/parity run --stage full --output-dir /Users/ianzepp/work/faberlang/gradus/docs/factory/perf-gap-closure/evidence/PGC-R5/parity-raw`; then `scripta/parity reduce /Users/ianzepp/work/faberlang/gradus/docs/factory/perf-gap-closure/evidence/PGC-R5/parity-raw --out /Users/ianzepp/work/faberlang/gradus/docs/factory/perf-gap-closure/evidence/PGC-R5/parity-receipt.json`; then append-only candidate `scripta/parity baseline /Users/ianzepp/work/faberlang/gradus/docs/factory/perf-gap-closure/evidence/PGC-R5/parity-raw --baselines-dir /Users/ianzepp/work/faberlang/gradus/docs/factory/perf-gap-closure/evidence/PGC-R5/baseline-candidate --receipt-out /Users/ianzepp/work/faberlang/gradus/docs/factory/perf-gap-closure/evidence/PGC-R5/baseline-candidate.md`. Raw capture, reduced receipt, candidate baseline, and the reduction/iteration census evidence live under `gradus/docs/factory/perf-gap-closure/evidence/PGC-R5/`; a lesser stage is not baseline-grade. |
| `depends_on` | `PGC-R3`, `PGC-R4` (kernel_plan fold order) |
| `sanity` | Constant, mixed-sign, and near-epsilon rows stay inside the declared f32 contract; masked future columns remain excluded; no unsafe barrier crossing. |
| `constraints` | Amendment per head-cto mail 91fe3d59, 2026-08-28 (R5 scope-amendment verdict, section 3 invariants): (1) RowReduction variant gated to the two op kinds — every other op keeps its contract and launch facts byte-for-byte (`_ => {}` arm untouched); (2) cross-lane NVVM containment — the variant must not change the ABI signature for lanes without a consuming row-reduction recipe: gate at the target-aware synthesis seam (`storage_buffer_kernel_with_interner_for_target_entry`, `signature.rs:291`) or an admission const (`DECODE_GEMV_SELECTION_ENABLED` precedent, `contract.rs:~875`); a rows-x-32 grid under a per-element NVVM body is wrong code, not just slow; the alternative (an NVVM row-mapping body) pulls the `nvvm/{recipe.rs,nvvm_descriptor.rs}` files into scope — seat picks the smallest and names it in the receipt; (3) numeric class: Class B for all three entries (threadgroup tree reduction changes summation order); R5 mints its own frozen tolerance per the R4 schema (`pgc-r4-frozen-tolerance-v1`), never widened; (4) emitted-MSL sha changes for the three entries route through the §7.5 pin-regeneration path (B2-RETUNE precedent) — declared in the receipt. |
| `non_goals` | No GEMM recipe (R4), no decode softmax (B1 owns extents; decode body is B2-landed), no fusion, no f16/quantized work, no tolerance widening. |
| `risk` | high — reduction-order change is the whole risk; the two-class declaration plus frozen tolerance is the containment. |
| `integrable` | yes — one family, packet fold |
| `parallel_group` | `R-W3` (serialized after R4 on the kernel_plan trio) |

#### PGC-R6 — launch-fusion consumer: Metal emitter migration (operation-fusion OF-3 re-admission)

| Field | Value |
| --- | --- |
| `id` | `PGC-R6` |
| `outcome` | Migrate the Metal elementwise emit path to consume the landed target-neutral `ElementwisePlan` (OF-1 `3d8ce4d8a6`, OF-2 `aebec9180`) instead of rebuilding pointwise expressions backend-locally — the missing consumer of `radix/docs/design/operation-fusion.md` Unit 3. This is the re-admission of operation-fusion `OF-3`, deferred 2026-08-18 behind R-PACK-05; the reopen package (operator post-pause direction, memo `cbc68961`) is the re-admission authority, and the owning spec stays `radix/docs/factory/operation-fusion/{goal,delivery}.md` — this card does not re-lower it or duplicate its units. No wall claim: structural oracle only (condition-B rider). |
| `write_scope` | Packet `worktrees/pgc-r6/`, branch `factory/pgc-r6` (radix only). `radix-mir-metal/src/emit/elementwise.rs` + `emit/tests/elementwise.rs`; the elementwise path of `emit/mod.rs` and `emit/recipes.rs` (owned by this card in `R-W3`); additive accessors on `radix-mir/src/elementwise_plan.rs` + `elementwise_plan_test.rs` as the consumer requires. Consult-only (never edit this wave): `kernel_plan/`, `device_program_plans.rs`, `kernel_decomposition.rs`. New focused fixtures per design §11.4–11.6. |
| `done_when` | Design §11 proofs 4–6 green on Metal: **backend source proof** (one output store per elementwise-only subchain, no intermediate buffer/launch for the focused fixture); **unfused comparison** (planning-disabled vs enabled under the operation's declared tolerance — byte equality only where the contract promises it, per the two-class oracle); **no accidental scope expansion** (reduction, matmul, quantized unpack, fragment-call, and control-flow fixtures hit named barriers). Old backend-local builder removed in the same scoped migration once equivalence coverage exists. No proba tuple may change (radix-side change is emit-internal). Evidence under `evidence/PGC-R6/`. |
| `depends_on` | none (architecture lane; runs parallel with R4/R5 — CTO#2 Q3.5) |
| `sanity` | `cargo test -p radix-mir-metal elementwise` green at the packet; plan summary reports barrier reasons without parsing MSL. |
| `non_goals` | No new inliner (landed law §7.0), no MSL device-fn rung, no NVVM/WGSL migration (OF-4 territory), no driver flag unification (OF-5), no recipe-seam widening, no Gradus corpus change (R7), no performance receipt. |
| `risk` | medium — the old builder removal must carry equivalence coverage; fail-closed barrier reasons must not become silent fallbacks. |
| `integrable` | yes — one emit path, packet fold |
| `parallel_group` | `R-W3` |

#### PGC-R7 — bounded Gradus corpus adoption, wave 1 (public→private helper redesignation)

| Field | Value |
| --- | --- |
| `id` | `PGC-R7` |
| `outcome` | Redesignate one compatible-launch-graph family of Gradus public launch-ABI entries as private device helpers with composites exercising the landed semantic composition plus the R6 launch-fusion consumer; regenerate the frozen identities, resource maps, descriptors, launch plans, and parity evidence for that family. Wave-sized by compatible launch graph (per the R3 census), not a broad annotation cleanup — the corpus today is 48 flat `@ kernel`/`@ public` pairs with no helper call graph (CTO#2 Q4). KPC owns the purity definition; wave 1 stays monomorphic concrete instantiation, so SGR is not a gate (it hard-gates only the generic case). |
| `write_scope` | Packet `worktrees/pgc-r7/`, branch `factory/pgc-r7`. `gradus/src/kernel.fab` only the selected family's entry regions (family named in the dispatch from the R3 census; default candidate: one decode elementwise/epilogue family, e.g. the swiglu→residual neighborhood); `gradus/src/kernel.proba` only that family's live cases (named at dispatch from `src/kernel.proba`; no phantom identifiers). Radix/hosts: new additive-only `gea3_pipeline_pgc_r7_test.rs` and `hosts/macos-arm64/tests/gea3_decode_pgc_r7.rs`; regenerated export pins for the family's entries inside `gea3_pipeline_test.rs` region-ownership rules. |
| `done_when` | The five fused-unit oracle classes (CTO#2 Q4) all carry committed evidence under `evidence/PGC-R7/`: (a) unfused-vs-fused output oracle under the two-class numeric law (byte identity only where the contract proves no observable rounding/contraction — e.g. pure elementwise chains; else frozen per-family tolerance vs the unfused output, never widened); (b) intermediate visibility/materialization checks (an elided intermediate leaves device memory only with no live external consumer — otherwise the store is retained); (c) launch/resource/version graph pins (launch counts, geometries, slot maps, resource versions as receipt columns); (d) negative barrier cases (alias, control flow, multi-consumer, recipe-boundary fixtures refuse with typed reasons); (e) at least one physical family-keyed A/B receipt vs the R3 family — structural launch-count delta primary, wall L1-gated secondary. Certified outputs unchanged. |
| `depends_on` | `PGC-R3` (census + family key), `PGC-R6` (consumer) |
| `sanity` | One family, one packet: the redesignated entries' proba tuples stay byte-identical where semantics are untouched; composites fail closed on budget overflow (no silent unfused drift). |
| `non_goals` | No broad annotation sweep, no shape-generic `@kernel` (KPC waves 2–3 + SGR gate), no multi-family wave, no new fusion barriers beyond the design doc's set, no wall target. |
| `risk` | high — migration can temporarily enlarge composed MIR and cross recipe/storage/geometry barriers without reducing a launch; the oracle classes are the containment, and a wave that reduces no launch is an honest reportable result, not a failure to hide. |
| `integrable` | yes — one family, packet fold |
| `parallel_group` | `R-W4` |

#### PGC-R8 — L13 encoder-construction reduction (hosts)

| Field | Value |
| --- | --- |
| `id` | `PGC-R8` |
| `outcome` | Cut the 2,115 per-step encoder constructions: batch compatible launches into fewer compute encoders and/or reuse pre-encoded command state with persistent bindings where the ABI permits (`hosts/macos-arm64/src/metal_host.rs` `launch_kernel_bound`: one `new_compute_command_encoder` + bind-every-resource + `end_encoding` per launch). The host already submits once and waits once per step — this is construction cost, not a sync bubble, and it is **not** launch fusion (R6/R7 own launch-graph shape). Evidence: encode 9.15 ms prefill / 4.4–5.5 ms decode (~2.09–4.3 µs per launch × 2,115), `5f3b144d`/`b1c7f917`. |
| `write_scope` | Direct mode, hosts path-limited. `hosts/macos-arm64/src/metal_host.rs` (launch site: encoder construction/batching, binding-vector reuse); new additive-only `hosts/macos-arm64/tests/gea3_decode_pgc_r8.rs` (encoder-count census before/after, certified outputs). Radix ABI read-only unless a typed launch fact must extend — then named in the report and folded through the Mind. No kernel source, no Gradus change. |
| `done_when` | Encoder count per step drops measurably (receipt column, L13 law: keep launch/blocking-wait/readback counts first-class); certified outputs 1000/1000; one fixed-1000 paired capture (both phases) vs the R3 family with encode-ms as the primary delta and wall as L1-attributed secondary. Evidence under `evidence/PGC-R8/`. |
| `measurement_commands` | From `/Users/ianzepp/work/faberlang/radix`: `scripta/parity run --stage full --output-dir /Users/ianzepp/work/faberlang/gradus/docs/factory/perf-gap-closure/evidence/PGC-R8/parity-raw`; then `scripta/parity reduce /Users/ianzepp/work/faberlang/gradus/docs/factory/perf-gap-closure/evidence/PGC-R8/parity-raw --out /Users/ianzepp/work/faberlang/gradus/docs/factory/perf-gap-closure/evidence/PGC-R8/parity-receipt.json`; then append-only candidate `scripta/parity baseline /Users/ianzepp/work/faberlang/gradus/docs/factory/perf-gap-closure/evidence/PGC-R8/parity-raw --baselines-dir /Users/ianzepp/work/faberlang/gradus/docs/factory/perf-gap-closure/evidence/PGC-R8/baseline-candidate --receipt-out /Users/ianzepp/work/faberlang/gradus/docs/factory/perf-gap-closure/evidence/PGC-R8/baseline-candidate.md`. Raw capture, reduced receipt, candidate baseline, and the encoder-count census evidence live under `gradus/docs/factory/perf-gap-closure/evidence/PGC-R8/`; a lesser stage is not baseline-grade. |
| `depends_on` | `PGC-R3` |
| `sanity` | Ordered-binding validation (`metal_host.rs:810-864`) still proves per-launch resource order inside a batched encoder; no cross-launch hazard introduced by batching. |
| `non_goals` | No launch fusion, no kernel entry change, no sync-structure change (already one submit/wait), no CPU pipelining ahead of the GPU. |
| `risk` | medium — batching must not weaken the ordered-binding law or observability of per-launch validation. |
| `integrable` | yes — hosts direct-mode, path-limited commit |
| `parallel_group` | `R-W5` |

### 7.5 Baseline re-key and the gradus-pin question (operator draft)

The parity protocol pins gradus at `de687a4` (pre-B3); B3 folded to gradus
main (`d942388`, selected-row KV writes), and B2-RETUNE kept the original
`kv_append` frozen-sha pins as protocol truth (radix `7d302c35f`), routing
the pin lag to Mind for the next baseline regeneration — which is `PGC-R3`.
The re-pin decision is operator-owned (it changes the parity protocol's
identity law). Default until ruled: keep the pre-B3 pin; R3 records both
pin postures in its receipt.

Draft operator mail (Mind routes; planner does not mail the operator
directly):

> **Subject: PGC re-key — gradus parity pin posture (decision needed before
> PGC-R3 certifies the new baseline family)**
>
> The parity protocol pins gradus at `de687a4` (pre-B3) while gradus main
> carries B3 (`d942388`, selected-row KV appends). The R3 re-key must pick a
> posture:
>
> 1. **Re-pin to post-B3 main** (planner default): regenerate the
>    `kv_append` frozen identities, certify the new family on post-B3
>    truth. Cost: one pin regeneration + re-certification. Benefit: every
>    later delta keys against the tree that actually ships; B3's KV-write
>    change is inside the measured family.
> 2. **Keep pre-B3 pin**: cheaper now, but the family of record excludes a
>    folded main change and the protocol-vs-main drift compounds per
>    capture.
> 3. **Staged dual-family**: certify at the pre-B3 pin, then immediately
>    re-pin and take one confirmation capture. Cleanest record, two
>    captures.
>
> Recommendation: option 1 — truth over continuity; a baseline family that
> excludes a folded main change mis-keys every later wall delta.

### 7.6 Open questions for Mind

1. **Gradus-pin ruling** (§7.5) — gates R3's certification; operator
   decision requested.
2. **OF-3..OF-5 re-admission bookkeeping**: `PGC-R6` re-admits OF-3 under
   the reopen authority; the operation-fusion goal
   (`radix/docs/factory/operation-fusion/goal.md`) Status line and phase
   table are stale against landed OF-0/OF-1/OF-2 and the R6 re-admission —
   Mind owns advancing them in the same reconciliation turn.
3. **R-PACK-05 residual gate**: OF-3's original defer was "behind
   R-PACK-05"; EXEC-02 §8b re-lowered that surface 2026-08-22 and its
   completion state is not re-verified here. Mind confirms the emit-arm
   exclusivity concern is discharged (no live R-PACK emit wave) before R6
   dispatches.
4. **Goal Status advance**: this amendment supersedes C1/C3/C4 and folds
   the B/C residuals — the goal.md Status line and §5 tables need the
   matching Mind advance (planner annotated §5 below; the Status line is
   Mind-owned).
5. **L13 sequencing latitude**: CTO#1 ranked L13 earlier than CTO#2; the
   amended order (L13 last) governs, but R8 has no structural dependency on
   R4–R7 — Mind may pull it forward for seat-availability reasons without
   amending this delivery, provided its capture still keys against the R3
   family.

### 7.7 PGC-R5 bag amendment — option (b) NVVM row-mapping (ruling `dce2a356`, 2026-08-28)

Appended by planner under Vivi task `443d2c25` from Mind ruling `dce2a356`
(ruling thread `160d6429`; head-cto recommendation `190e7520`, posture
`correct_before_resume`, hard gate; CTO-B audit `a694cd2b` finding 4).
This section amends the `PGC-R5` card in §7.4 — where this section and the
card's frozen text differ, **this section governs** (append-only law: the
card text above is retained as record, not rewritten). All other §7 cards
are untouched.

**Amendment — containment mechanism settled to option (b).** The
containment fork the card's `constraints` invariant (2) left to the seat
("gate at the target-aware synthesis seam … or an admission const … seat
picks the smallest") is closed by ruling:

| Amended field | Operative amendment |
| --- | --- |
| `constraints` (2) | **Retired as mechanism**: containment at `storage_buffer_kernel_with_interner_for_target_entry` (`signature.rs:291`) — the seam carries **no backend parameter** and is **WGSL-shared**; gating there without an API/call-chain redesign would be a **false gate resolution**. **Adopted**: option (b) — the NVVM row-mapping recipe. RowReduction stays a target-neutral launch/body contract (workgroup `[32,1,1]`, dispatch/workgroup grid `[rows,1,1]`; one workgroup owns exactly one logical row). |
| `constraints` (2) / `write_scope` | The NVVM consumer is **mandatory in scope**, superseding the card's "nvvm files named either way per the containment choice (smallest path picked by the seat)": `radix-mir-llvm/src/nvvm/recipe.rs` — a row-mapping body selected by `Some(RowReduction)` (32 lanes strided over the owned row, uniform cooperative reduction, vectorized scale/output pass over the same row; **never** falls through to the per-element recipe) — plus `nvvm_descriptor.rs` — the matching signature route — for `TensorRmsNorm` and `TensorCausalMaskedSoftmax` only. Seam-redesign and admission-const gate work at `signature.rs`/`contract.rs` is **out of scope**. |
| `done_when` | Carries the fail-closed proof (resume condition 2 below) in addition to the card's two-class oracle: the receipt records the proof that **no RowReduction signature reaches an old per-element body**. |

**Resume conditions (all mandatory, from the ruling — implementation does
not resume until the amended bag carries all three):**

1. The bag names option (b) and the NVVM body/descriptor consumer
   (`nvvm/recipe.rs` row-mapping body + `nvvm_descriptor.rs` signature
   route) — satisfied by this amendment; Mind's re-issued Hand bag must
   carry it.
2. **Fail-closed proof**: no RowReduction signature reaches an old
   per-element body — any backend without a consuming row-mapping recipe
   **rejects the contract before launch/signature synthesis** (WGSL stays
   unadmitted; shared synthesis must not treat backend-blind code as
   backend containment). Focused proofs land **before** implementation
   resumes.
3. **Class B numeric tolerance unchanged** (frozen per-family contract per
   the R4 schema, never widened) plus the barrier/masking proofs per the
   `190e7520` seam-contract sketch: RMSNorm covers the full row width
   including 960-wide rows; causal softmax excludes masked future columns
   from max/sum and output semantics; no lane crosses a barrier
   conditionally.

**do_not carried forward**: no backend-blind admission const as
containment; no rows-x-32 grid over a per-element NVVM body (that is wrong
code, not slow code); not record-only.

**Effort**: M, est ~150k–300k tokens (CTO basis, `190e7520`: two
backend recipe/descriptor files already admitted by the amended card, plus
focused contract/launch/body proofs and the existing Metal/numeric work).

**Status**: `PGC-R5` stays **parked / resume-gated** (task `160d6429`).
Resume is ready-for-capacity after the live P1 repair burst. At resume, the
`worktrees/pgc-r5` packet holds dirty interrupted WIP — classify it against
this ruling before building on it (Mind owns the classification; nothing in
this amendment pre-approves it).
