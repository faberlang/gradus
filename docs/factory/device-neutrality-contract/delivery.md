# DELIVERY: device-neutrality-contract — Gradus states its tier and parameterizes backend-family law

**Status**: lowered — ready for Hand tasking
**Created**: 2026-08-21
**Goal:** [`goal.md`](goal.md) (goal-check verdict: READY; all F6.1–F6.3 source pins re-verified live at gradus `ce604b1`, post `d6138d5`/`7646ed7`)
**Campaign:** radix [`emission-lane-parity`](../../../../../radix/docs/factory/emission-lane-parity/CAMPAIGN.md) goal ELP-10 (independent entry point; no campaign dep edges in)
**Planner handle:** `a1bd9796`
**Repos:** `gradus/` only (this repo); `radix` receipts are read-only evidence

---

## 1. Interpreted Unit

ELP-10 removes three neutrality erosions inside Gradus without touching
execution: (a) the llama.cpp/GI4 attention-family law (quantized V ⇒ flash,
flash ⇒ straight V, classic ⇒ transposed V) is currently baked as unconditional
library admission and becomes an explicit, parameterized profile with a
declared-but-empty CUDA slot that fails closed; (b) the opened KV dtype set
(F16 default) is stated without saying the executed `KVCache` is f32-staged —
the opened/executed distinction is written down at every claim site; (c) the
bench exemplar and the numeric design matrix conflate capability with
execution — Metal/CUDA cells and bench rows gain honest evidence-class labels
and reserved CUDA mirror slots. The CPU/reference tier becomes Gradus's stated
tier of record.

Binding goal invariants carried into every unit: no numeric-behavior change
for the admitted profile (proba rows stay green, pinned messages
byte-identical); no device residency/emission work in Gradus (Radix/hosts
own it); no CUDA execution (ELP-06 proves the lane on Radix fixtures);
no weakening of the U5 truth pass (README `7646ed7`) — this delivery builds
on its wording.

## 2. Normalized Spec

Delivery-sized outcome: after DNC-U1..U6, a reviewer can verify from live
artifacts alone that (1) no backend family's layout law is unconditional
admission — `cache.fab` validates against a named profile record, the
current profile is exactly today's GI4 law, and a `cuda` profile rejects
construction with a named error citing the missing evidence; (2) every
opened-KV-dtype claim sits beside the f32-staged executed-tier fact and
names the owning campaign for closing the gap; (3) README and
api-shape-policy name the CPU/reference tier as the executed tier of
record; (4) the design matrix's every Metal/CUDA cell carries an
emittable-vs-executed label with a receipt citation; (5) the bench has
reserved CUDA slots (no numbers) for CAP-02/ELP-06-era runs.

## 3. Repo-Aware Baseline

Verified live 2026-08-21 at gradus `ce604b1` (clean tree; moves since the
goal draft `6e02baa`: `d6138d5` FMIR text-scalar normalize, `7646ed7` U5
truth pass — README/cache headers refreshed, `612cb25` SD0 lowering).

| Fact | Live authority (verified) | Delivery consequence |
| --- | --- | --- |
| **F6.1 live** — family law is unconditional admission: quantized V ⇒ flash; flash ⇒ straight V; classic ⇒ not-straight | `src/cache.fab:1366-1374` inside `construct_kv_structure_with_partitions` (`:1361`; public wrapper `:1356`); helpers `_kv_dtype_quantized` `:755`, `_attention_is_flash` `:1014`, `_v_layout_is_straight` `:1026`, `_check_block` `:1281` | DNC-U1 moves exactly this law into a profile record |
| Error messages are proba-pinned | `src/cache.proba:458-461, 491-492` (exact message strings) | Behavior-unchanged bar: these rows stay byte-identical green |
| Public constructor consumers outside cache | `exempla/dense-decode-smollm2/src/main.fab:441`; `exempla/generate-smollm2/src/main.fab:445` (9-arg `construct_kv_structure`) | U1 is additive: existing constructor signatures unchanged |
| Wire carries the profile's serialized tag already | `structure_schema` `1.0.0` `:616`, v1.1.0 `:618`; `reserve_policy` serialized `:1616`, enforced `≡ RESERVE_GI4` `:1656` (`RESERVE_GI4` `:620`) | No wire change: GI4 profile identified by existing tag; `cuda` has no wire form and rejects at construct |
| **F6.2 live** — opened set F16-default vs f32-staged executed cache | header `src/cache.fab:63-68` ("opened set {F32, F16, Q8_0, Q4_K} (F16 default)" at `:67`); `union KvDtype` `:632-637`; executed identity `dtype()` "f32" `:265-268`, `layout()` "staged" `:270-273`; construction pins `:362`; hard f32 requires `:398-399, :433-434` | DNC-U2 states the distinction at all three claim sites |
| Opened-set revision record | `docs/design/gi4-contract.md:20-30` ("Revised dtype row", Default **F16** at `:24`); `docs/design/numeric-flexibility-performance.md:191, 499` | U2's doc sites |
| Reference-tier carrier | `src/tensor.fab:145-148` (`class Tensor { … list<f32> data }`) | U3's tier-of-record citation |
| **F6.3 live** — matrix conflates capability with execution | `docs/design/numeric-flexibility-performance.md` §3.2 `:139-158`: F32 "✅ (GI3)" = executed receipt; BF16 "✅ (R-PACK-02)" = emitters only; Q8_0/Q5_0/Q4_K/Q5_K/Q6_K rows bare "✅" = uncited | DNC-U4 labels every cell with evidence class + receipt |
| R-PACK-02 is emitter-complete, device-run reserved | radix `docs/factory/gpu-production-readiness/exec02-packed-kernels-delivery.md:9` ("device-run intentionally not attempted, reserved for R-PACK-05") | U4's receipt citations; never upgraded to "executed" |
| Bench has no CUDA lane | `exempla/dense-prefill-smollm2/bench/` — `llama-bench-{smollm2,qwen05}-{cpu,cpu-t1,metal}.md` only; `RECEIPT.md` already honest that our side is `cpu-reference` | DNC-U5 adds reserved CUDA slots; builds on, never edits, measured numbers |
| README non-claims anchor (U5-refreshed) | `README.md:199-204` ("GPU-scale training or broad executed performance evidence … CPU-reference-level at most") | U3 tier statement + U5 bench sentence land here |
| `./scripta/check-source` GREEN at HEAD | executed 2026-08-21, exit 0 (U4b repair `d6138d5` landed) | Closeout gate is green-owned; no foreign-red caveat |
| Concurrent seats | SD0-U1 owns `src/generation.proba` + `docs/factory/speculative-decode-contract/`; train-step closeout audit owns `docs/factory/train-step-optimizer-call/` | Disjoint from every DNC write scope |

## 4. Unit Graph — Hand units

Shared non-goals for every unit (per goal + campaign): no device/Metal/CUDA
vocabulary in live source, no device residency or emission work, no CUDA
execution, no KV-semantics change (paging/branching stay with radix
`kv-cache-*` goals), no default-dtype change (goal open question 3: F16
stays the opened default), no numeric-behavior change for the admitted
profile, no campaign or sibling-goal file edits, no edit to
`src/generation.proba` or `docs/factory/speculative-decode-contract/`
(foreign seat), no edit to `docs/factory/train-step-optimizer-call/`.

### DNC-U1 — KV family-law profile parameterization (cache)

- **outcome**: `src/cache.fab` gains a cache-local profile record (goal open
  question 1 default: no new module) carrying the family law — allowed
  V-layouts per attention family, quantized-V rule, KV dtype set, block
  rules, reserve tag. `cache.profile_gi4()` admits exactly today's law;
  `cache.profile_cuda()` is a declared slot with no admitted law — any
  KVStructure construction under it rejects fail-closed with the pinned
  message `"cuda profile has no admitted KV layout law; awaiting device receipts (ELP-06/EXEC-02)"`.
  Existing `construct_kv_structure` / `construct_kv_structure_with_partitions`
  signatures are unchanged (they validate against `profile_gi4()`); a new
  additive profile-aware constructor takes the profile explicitly. Wire
  forms unchanged: `cache/structure/1.0.0` and `1.1.0` decode exactly as
  today; no `cuda` wire form exists (deserialize keeps requiring
  `reserve ≡ RESERVE_GI4`, `:1656`).
- **write_scope**: `src/cache.fab`; `src/cache.proba`
- **depends_on**: —
- **done_when**: new proba rows prove (a) construction under
  `profile_cuda()` rejects with the pinned message before any law check,
  (b) every pre-existing pinned-message row (`:458-461`, `:491-492`) and
  the full existing cache proba suite are green and byte-identical, (c) the
  two exempla constructors are untouched (no signature change).
- **first-failing oracle**: the `profile_cuda()` rejection row — red first
  (no profile surface exists to call), green only when the fail-closed slot
  lands; then the existing `:458-461` rows prove the GI4 law moved, not
  changed.
- **sanity**: `faber test src/cache.proba <new-profile-filter>`
- **est**: M — basis: one genus + constructor surgery on a 1720-line module
  with 29 pinned proba tests; precedent: the W2-U1/W5c-U8 KVStructure
  landings (additive descriptor beside live cache).
- **risk**: medium — public constructor surface on the hottest cache seam;
  mitigated by additive-only posture and message-pinned regression rows.
- **integrable**: yes

### DNC-U2 — opened-vs-executed KV dtype honesty

- **outcome**: every site stating the opened KV dtype set states beside it
  that the executed `KVCache` today is f32-staged (`dtype()` "f32",
  `layout()` "staged", `src/cache.fab:265-273, :362, :398-399`) and that
  closing the gap is `production-ml-library` execution-tier scope. Sites:
  the `cache.fab` header comment block (`:63-68`), the gi4-contract
  revision record (`docs/design/gi4-contract.md:20-30`), and
  `docs/design/numeric-flexibility-performance.md` §4.1 (`:191`).
- **write_scope**: `src/cache.fab` (header comment block only — no code);
  `docs/design/gi4-contract.md`; `docs/design/numeric-flexibility-performance.md`
  (§4.1 sentence only)
- **depends_on**: DNC-U1 (serializes `src/cache.fab`)
- **done_when**: each of the three sites carries the f32-staged
  executed-tier sentence naming the owning campaign; no numeric claim or
  admitted-set membership changes.
- **first-failing oracle**: `grep -rn "F16 default" src/cache.fab docs/design/gi4-contract.md docs/design/numeric-flexibility-performance.md`
  — today the hits carry no staged-execution distinction; after, every
  hit's surrounding block does (gi4-contract hit is the "Default | f32 |
  **F16**" row at `:24`; its distinction rides the adjacent paragraph).
- **sanity**: `./scripta/check-source` (comment-only src edit)
- **est**: S — basis: three claim-site edits; precedent: the U5 truth pass
  (`7646ed7`) README/claim refresh.
- **risk**: low — comments + docs; the only failure mode is weakening an
  existing claim, excluded by done_when.
- **integrable**: yes

### DNC-U3 — CPU/reference tier of record

- **outcome**: README Status section and `docs/api-shape-policy.md` state
  Gradus's executed tier of record is the CPU/reference tier — f32
  host-list carrier (`src/tensor.fab:145-148`), reference kernels, FMIR
  stepper receipts — and that device residency/emission is Radix + hosts
  scope. Builds on the U5-refreshed wording (`README.md:113-140, 199-204`);
  strengthens, never weakens, the executed-MLP-receipt and no-GPU-training
  claims.
- **write_scope**: `README.md`; `docs/api-shape-policy.md`
- **depends_on**: —
- **done_when**: both documents name the CPU/reference tier as the executed
  tier of record in ≤2 sentences each with the carrier citation;
  `api-shape-policy` version header unchanged (statement, not policy
  change).
- **first-failing oracle**: `grep -in "tier of record" README.md docs/api-shape-policy.md`
  — empty today; non-empty and correctly scoped after (must not claim
  device execution anywhere).
- **sanity**: visual diff review only (docs).
- **est**: S — basis: two short statements at pre-anchored sites.
- **risk**: low.
- **integrable**: yes

### DNC-U4 — design-matrix capability-vs-execution split

- **outcome**: `docs/design/numeric-flexibility-performance.md` §3.2 matrix
  (`:139-158`) splits the Metal and CUDA/NVVM columns into
  "emittable (recipe/emitter receipt)" vs "executed (device receipt)"
  labels: F32 = executed (GI3 receipt); BF16/Q8_0/Q5_0/Q4_K/Q5_K/Q6_K =
  emittable (R-PACK-02, radix `b199834f8`), executed none — reserved
  R-PACK-05. A legend defines both labels once; the WGSL ("recipes"/later)
  and CPU (dequant classes) columns get their evidence-class labels; §1
  gains a one-line 2026-08-21 refresh note (R-PACK-05 still pending).
- **write_scope**: `docs/design/numeric-flexibility-performance.md` (§1
  stamp note, §3.2 table + legend)
- **depends_on**: DNC-U2 (same file, serializes)
- **done_when**: no bare `✅` cell remains without an evidence-class label
  and receipt citation; no cell upgrades to "executed" (R-PACK-05 has not
  run).
- **first-failing oracle**: `grep -n "✅" docs/design/numeric-flexibility-performance.md`
  — today returns bare-✅ cells (Q8_0..Q6_K rows `:144-158`); after, every
  ✅ carries a label + receipt.
- **sanity**: the grep oracle above plus a read of the legend.
- **est**: S–M — basis: one table + legend with cross-repo receipt
  citations; accuracy of citations is the work.
- **risk**: low — docs-only, but a wrong "executed" label would be a
  truth regression; done_when forbids upgrades.
- **integrable**: yes

### DNC-U5 — bench CUDA mirror slots + bench-tier statement

- **outcome**: `exempla/dense-prefill-smollm2/bench/` gains one
  `cuda-pending.md` mirror file reserving CUDA comparator rows for both
  models (SmolLM2-360M, Qwen2.5-0.5B) — explicit NONPRODUCT/pending
  markers, no numbers, named consumer (CAP-02 / ELP-06-era runs) — and
  `RECEIPT.md`'s comparison-table section gains a one-line "CUDA
  comparator lane — reserved (no run)" pointer to it. README's non-claims
  bullet (`:199-204`) gains one sentence: comparator benches to date pin
  llama.cpp Metal and CPU rows on burgus; no CUDA comparator row exists
  yet (reserved).
- **write_scope**: `exempla/dense-prefill-smollm2/bench/cuda-pending.md`
  (new); `exempla/dense-prefill-smollm2/bench/RECEIPT.md` (one annotation);
  `README.md` (one sentence)
- **depends_on**: DNC-U3 (serializes README)
- **done_when**: the bench dir contains the reserved CUDA slots with zero
  numeric cells; RECEIPT.md points at them; README names the reserved lane;
  no measured number anywhere is edited.
- **first-failing oracle**: `ls exempla/dense-prefill-smollm2/bench/*cuda*`
  — empty today; after, returns the pending file whose content contains no
  timing numbers.
- **sanity**: visual review that no numbers entered the pending file.
- **est**: S — basis: one small marker file + two one-line annotations.
- **risk**: low.
- **integrable**: yes

### DNC-U6 — closeout, ledger, handoff

- **outcome**: goal.md Ledger rows and Status move to landed per unit
  receipt; this delivery's ledger matches; closeout commands all green;
  READY evidence reported on the Mind handle.
- **write_scope**: `docs/factory/device-neutrality-contract/goal.md`
  (Ledger + Status lines); `docs/factory/device-neutrality-contract/delivery.md`
  (ledger)
- **depends_on**: DNC-U1, DNC-U2, DNC-U3, DNC-U4, DNC-U5
- **done_when**: the closeout block below is green end-to-end at HEAD and
  each unit's receipt is recorded in both ledgers.
- **first-failing oracle**: the closeout block itself — first command run
  is the factory-status audit; any red reports blocked, never weakened.
- **sanity**: —
- **est**: S — basis: ledger edits + one command block; precedent:
  SD0-U7 closeout shape.
- **risk**: low.
- **integrable**: yes

## 5. Checkpoints And Gates

**Batching decision**: six Hands. The goal's three-unit sketch split at two
seams: unit 2 bundled the dtype-honesty, tier, and matrix families (three
claim families on five surfaces) and unit 3 bundled bench slots with the
README statement; both split to keep one behavior family per Hand while
serializing only where write scopes collide (`src/cache.fab` → U1→U2;
`numeric-flexibility-performance.md` → U2→U4; `README.md` → U3→U5). U1 and
U3 are the parallel entry pair.

**Lane-owned gates (named once, never on a child Hand)**:

- lint lane: `./scripta/check-source`
- test/compile lanes: `./scripta/check-compile`; focused `faber test` on
  touched proba files
- merge lane: path-limited docs+source commits; `git diff --check`
- factory audit: `python3 ../radix/scripta/audit-factory-goal-status.py --factory-root docs/factory --fail-on error`

**Delivery closeout (DNC-U6 runs; all must be green)**:

```bash
python3 ../radix/scripta/audit-factory-goal-status.py --factory-root docs/factory --fail-on error
./scripta/check-source
./scripta/check-compile
faber test src/cache.proba
git diff --check
```

(`faber` invocations use `FABER_LIBRARY_HOME`/`FABER_BIN` exactly as
`scripta/check-compile` sets them.) Unlike SD0, there is no foreign-red
caveat: `check-source` is green at HEAD `ce604b1` (verified 2026-08-21) —
if a concurrent seat re-reddens it, U6 reports blocked on the handle
rather than narrowing the gate.

**U6 closeout input (cache.proba classification)**:
[`cache-proba-classification.md`](cache-proba-classification.md), handle
`9975f4a4`. Focused `--include cache` is 33 passed / 0 failed. Bare
`faber test src/cache.proba` remains environment-red (package MIR link of
`decode.proba`). No remaining cache-semantics defect. This pointer does
not land U6 or rewrite ledger Status.

**Release posture**: not-applicable — no package/release train; the
profile record is additive library surface with no wire change.

## 6. Validation

Hand sanity is the per-unit focused check named above — nothing wider.
Lane gates own source/compile/package routes. The behavior-unchanged bar is
objective: every pre-existing `src/cache.proba` row (29 tests, messages
pinned at `:458-461, :491-492`) stays green and byte-identical through
DNC-U1; `faber test src/cache.proba` at closeout proves it. The
fail-closed negative is the goal's named validation: constructing a KV
structure under the `cuda` profile before evidence exists rejects with the
named error.

## 7. Companion Skill Plan

None required. Hands may run `$polish` over their primary touched files
before commit; no `$campaign` or `$factory` load is needed by the units
themselves.

## 8. Open Questions

1. **Campaign status staleness** (Mind owns): radix
   `emission-lane-parity/CAMPAIGN.md` ELP-10 row and M5 gate go stale as
   units land; campaign edits stay with Mind per routing-artifact
   ownership.
2. **CUDA profile seed values** (settled by goal open question 2, flagged
   for audit): the slot stays empty + fail-closed; predeclaring llama.cpp
   CUDA law would repeat the assumption drift this campaign removes.
   ELP-06/EXEC-02 receipts fill it in a later amendment.
3. **Profile record shape** (Hand latitude): genus-with-accessors vs
   function table inside `cache.fab` is left to DNC-U1 within the
   additive, cache-local, message-pinned constraints; a second consumer
   triggers extraction (goal open question 1).

## Unit ledger

| Unit | Status | Seat | Receipt | Notes |
| --- | --- | --- | --- | --- |
| DNC-U1 | done | hand | `2712d8f` | KV family-law profiles (F6.1) |
| DNC-U2 | done | hand | `c9961af` | opened-vs-executed dtype honesty (F6.2) |
| DNC-U3 | done | hand | `58e0155` | CPU/reference tier of record |
| DNC-U4 | done | hand | `d6f2b99` | matrix capability/executed split (F6.3) |
| DNC-U5 | done | hand | `58a704a` | bench CUDA mirror slots (F6.3) |
| DNC-U6 | done | hand | [`cache-proba-classification.md`](cache-proba-classification.md) (`324e344`) | closeout: `faber test --include cache` 33/0; check-source; check-compile; factory audit 0 findings |

---

<!-- Lowered from goal.md by planner handle a1bd9796 on 2026-08-21. Goal
     ledger in goal.md remains the audit authority; this table tracks Hand
     dispatch. -->
