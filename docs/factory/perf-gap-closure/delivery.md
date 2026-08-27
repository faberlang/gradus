# Delivery: perf-gap-closure — parallel unit graph

**Status**: lowered for Mind routing 2026-08-27 — dispatch-ready; no GO stamp
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
maximal entry-disjoint set: `B1`, `B3`, `C2`, and `C5` may run concurrently.
The only common physical source path in that set is `gradus/src/kernel.fab`,
which the goal's §4 packet mechanism explicitly permits: the cards own
disjoint entry regions and the Mind folds their packet commits serially. Their
export and device tests are not shared files. `PGC-W1B` is the remainder. Its
cards are one-card, file-disjoint folds in the stated order because the
`radix-mir` kernel-plan files are shared by `B2`, `C1`, `C3`, and `C4`, and
`radix-mir-metal` `emit/matmul.rs` plus its test are shared by `B2` and `C4`.
No two cards in `PGC-W1B` are live concurrently.

| Wave | Parallel group | Execution |
| --- | --- | --- |
| 0 | `PGC-W0-DIRECT` | `PGC-D1` in hosts direct mode and `PGC-A0` in the skills repo direct mode, concurrently |
| 1a | `PGC-W1A` | `PGC-B1`, `PGC-B3`, `PGC-C2`, and `PGC-C5` in separate packets, concurrently; shared `kernel.fab` entry regions fold serially |
| 1b.1 | `PGC-W1B-1` | `PGC-B2` alone; owns the shared kernel-plan and Metal matmul paths for this fold |
| 1b.2 | `PGC-W1B-2` | `PGC-C1` after `PGC-B2`; owns the kernel-plan paths for this fold |
| 1b.3 | `PGC-W1B-3` | `PGC-C3` after `PGC-C1`; owns the kernel-plan paths for this fold |
| 1b.4 | `PGC-W1B-4` | `PGC-C4` after `PGC-C3`; owns the shared kernel-plan and Metal matmul paths for this fold |
| 2+ | `PGC-WA-<n>` | per-module A-series packets, massively parallel after `PGC-A0` lands |

Every Wave-1 packet is `worktrees/pgc-<lowercase-id>/` on branch
`factory/pgc-<lowercase-id>`; for example `worktrees/pgc-b1/` and
`factory/pgc-b1`. Each card owns one defect, its declared Gradus entry region,
and additive-only per-card test files. The `kernel_plan/{plan,build,kernel_plan_test}.rs`
and `emit/matmul.rs`/`emit/tests/matmul.rs` paths never occur in two live
sub-waves. Shared physical `kernel.fab` is the sole allowed concurrent source
file and is handled only by disjoint entry ownership plus serial packet folds.
Each A card uses `worktrees/pgc-<lowercase-id>/` and
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

All Wave-1 export and device proofs are additive. No B/C card appends to
`radix/crates/mir-emit-harness/src/gea3_pipeline_test.rs` or
`hosts/macos-arm64/tests/gea3_decode.rs`; each uses its own path named on its
card below.

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
| `write_scope` | Packet `worktrees/pgc-b1/`, branch `factory/pgc-b1`. `gradus/src/kernel.fab` only entries `decode_key_transpose`, `decode_score_gemm`, `decode_masked_softmax`, and `decode_context_gemm`; `gradus/src/kernel.proba` only their cases. New additive-only export test `radix/crates/mir-emit-harness/src/gea3_pipeline_pgc_b1_test.rs`; new additive-only device test `hosts/macos-arm64/tests/gea3_decode_pgc_b1.rs`. No edits to shared `gea3_pipeline_test.rs` or `gea3_decode.rs`; no other kernel entries. |
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
| `write_scope` | Packet `worktrees/pgc-b2/`, branch `factory/pgc-b2`. `gradus/src/kernel.fab` only `decode_gemv_qo`, `decode_gemv_kv`, `decode_gemv_gate_up`, `decode_gemv_down`, `lm_head_gemv`, and the T=1 score/context reduction specialization points; `gradus/src/kernel.proba` only their cases. This fold owns `radix/crates/radix-mir/src/kernel_plan/plan.rs`, `radix/crates/radix-mir/src/kernel_plan/build.rs`, and `radix/crates/radix-mir/src/kernel_plan/kernel_plan_test.rs` for its plan facts, plus `radix/crates/radix-mir-metal/src/emit/matmul.rs` and `radix/crates/radix-mir-metal/src/emit/tests/matmul.rs` only for the one-row recipe. New additive-only export test `radix/crates/mir-emit-harness/src/gea3_pipeline_pgc_b2_test.rs`; new additive-only device test `hosts/macos-arm64/tests/gea3_decode_pgc_b2.rs`. No edits to shared `gea3_pipeline_test.rs` or `gea3_decode.rs`; no other kernel entries. |
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
| `write_scope` | Packet `worktrees/pgc-b3/`, branch `factory/pgc-b3`. `gradus/src/kernel.fab` only `kv_append_k` and `kv_append_v`; `gradus/src/kernel.proba` only their cases. New additive-only export test `radix/crates/mir-emit-harness/src/gea3_pipeline_pgc_b3_test.rs`; new additive-only device test `hosts/macos-arm64/tests/gea3_decode_pgc_b3.rs` covering KV append constant construction, launch binding, arena probe, and focused physical assertions. No edits to shared `gea3_pipeline_test.rs` or `gea3_decode.rs`; no prefill KV entries. |
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
| `write_scope` | Packet `worktrees/pgc-c2/`, branch `factory/pgc-c2`. `gradus/src/kernel.fab` read-only verification scope: the prefill terminal-row call-site/view wiring that selects row 35; no Gradus source edit. `gradus/src/kernel.proba` read-only verification scope: the existing `prefill_head_rmsnorm`/`prefill_lm_head_gemv` cases; no proba edit. New additive-only export test `radix/crates/mir-emit-harness/src/gea3_pipeline_pgc_c2_test.rs` covering the final-row view pin and output count; new additive-only device test `hosts/macos-arm64/tests/gea3_decode_pgc_c2.rs` covering terminal-row binding, logits readback, and physical assertions. No edits to shared `gea3_pipeline_test.rs` or `gea3_decode.rs`; `lm_head_gemv` remains B2-owned and `head_rmsnorm` remains C3-owned. |
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
| `write_scope` | Packet `worktrees/pgc-c5/`, branch `factory/pgc-c5`. `gradus/src/kernel.fab` read-only verification scope: prefill weight-input/resource call sites and entry bindings; no Gradus source edit. `gradus/src/kernel.proba` read-only verification scope: the existing prefill resource/lifetime cases; no proba edit. New additive-only export test `radix/crates/mir-emit-harness/src/gea3_pipeline_pgc_c5_test.rs` covering prefill resource lifetime/export pins; new additive-only device test `hosts/macos-arm64/tests/gea3_decode_pgc_c5.rs` covering prefill resource preparation, copy-in census, and physical receipt assertions. `hosts/macos-arm64/src/composite_host/session.rs` only if live tracing proves the incorrect lifetime is materialized there; otherwise read-only. No edits to shared `gea3_pipeline_test.rs` or `gea3_decode.rs`; no kernel entry body. |
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
