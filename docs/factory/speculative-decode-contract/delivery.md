# DELIVERY: speculative-decode-contract — SD0 contract, schema, and corpus

**Status**: lowered — ready for Hand tasking
**Created**: 2026-08-21
**Goal:** [`goal.md`](goal.md) (goal-check verdict: READY; all source pins re-verified live)
**Campaign:** [`../speculative-decode/CAMPAIGN.md`](../speculative-decode/CAMPAIGN.md) stage SD0
**Planner handle:** `bbbf8d85`
**Repos:** primary `gradus/` (this repo); evidence-only `inferentia/`, `radix/`, `hosts/`

---

## 1. Interpreted Unit

SD0 is the campaign's mandatory first goal: freeze the semantic contracts every
later speculative stage consumes, without implementing any candidate path. Four
contract surfaces leave this stage: (a) the pinned dense baseline oracle,
(b) one versioned `AccelerationPolicy` carried by the generation configuration
wire (disabled by default, `context_lookup` the only other admitted mode),
(c) the candidate-provider seam plus greedy first-divergence acceptance and the
sampled typed-reject rule, and (d) the two-regime equivalence corpus with a
versioned receipt schema. No drafting, verification loop, cache branch, device
work, or throughput claim exists in SD0.

Binding campaign invariants carried into every unit: `generate_dense_with_stop`
is the pinned oracle; the policy is explicit, versioned, and disabled by
default; greedy is admitted first and sampled acceleration rejects before
lookup, RNG consumption, or branch creation; receipts separate
`context-reproduction` from `ordinary-chat` and label
reference/compiled/Metal/CUDA and cold/warm evidence.

## 2. Normalized Spec

Delivery-sized outcome: a mid-tier Hand can land each unit below without
inventing architecture, and SD1–SD6 can consume the frozen contracts by import
path plus the handoff map, with zero reinterpretation.

- The baseline contract is a named, documented, proba-pinned oracle
  (`baseline.md` + executing rows), not a prose claim.
- The policy is exactly one added field on `GenerationConfig`, additive to the
  public constructor (existing 9-arg callers unchanged), versioned on the wire
  (`1.0.0` legacy → disabled; `1.1.0` carries one policy segment); every
  unknown version, mode, field count, or policy encoding rejects.
- The provider seam and acceptance contract live in one new leaf
  (`gradus:speculative`); the receipt schema lives in its own leaf
  (`gradus:receipt`) so cross-repo consumers (radix, inferentia) import it
  without the speculative seam.
- The corpus is checked-in data plus an integrity script plus executing proba
  rows; baseline streams are captured from real `generate_dense_with_stop`
  runs, never hand-written.
- Disabled-policy equivalence to the legacy wire is proven by regression before
  closeout.

## 3. Repo-Aware Baseline

Verified against live code 2026-08-21 at gradus `d4fb784` (campaign snapshot
`cf82f70`; the delta is train/optimize `.proba`, exempla, and docs only — no
`.fab` contract surface moved).

| Fact | Live authority (verified) | Delivery consequence |
| --- | --- | --- |
| `generate_dense_with_stop` prefill + scalar `dense.decode_step` loop | `src/generation.fab:775-811`; `src/model/dense.fab:488-560` | Baseline pin (U1) documents exactly this route |
| Plain route is noncached `decode.decode_data` | `src/generation.fab:691-741` (helper `:634`) | Not the oracle; named as such in `baseline.md` |
| `GenerationConfig`: nine fields, wire `generation/config/1.0.0/…`, 12 slash parts, unknown version rejects | `src/generation.fab:185-427` (`deserialize_generation:412`) | U2 bumps to `1.1.0` 13-part; legacy 12-part decodes to disabled |
| inferentia calls the 9-arg `construct_generation` and parses `1.0.0` wires; its reject row expects 13-part `1.0.0` → "malformed generation config wire" | `inferentia/src/main.fab:961-962`; `inferentia/tests/generate-gate/src/main.fab:527,612` | Constructor must stay additive; legacy wire shape must keep rejecting extra parts |
| Greedy = exact argmax (`sampling.max`); stochastic draw advances explicit `train.Seed` | `src/sampling.fab:195-235`; `:556-569` | U4's first-divergence oracle and sampled-reject fixtures build on these |
| `prefill_cached` admits multi-row only from an empty prefix; `decode_step` is k=1 with `position ≡ prefix` | `src/model/dense.fab:572-647`; `:488-560` | Baseline k=1 semantics; block ops belong to SD1/SD2, not SD0 |
| Cache has append/extend/reset only — no checkpoint/branch/commit; `CacheIdentity` is metadata | `src/cache.fab:393-468`; `:479-607` | SD0 defines no branch; contract text only |
| No speculative/lookup/draft/acceleration surface exists in `src/` (grep clean); `corpus/` does not exist in gradus | verified 2026-08-21 | All SD0 code paths are new |
| `faber test <path> [FILTER]` runs proba on the MIR runner; full-file runs are minutes-scale | `faber test --help`; timed run | Hand sanity uses file + FILTER, not package-wide runs |
| `./scripta/check-source` is RED at HEAD on foreign lane commits (`textus` latin identifiers, `src/train.fab:272`, `src/optimize.fab:63`) | executed 2026-08-21; owned by `train-step-optimizer-call` U4b | Foreign red; SD0 never edits those files; U7 closeout requires green and reports blocked rather than weakening |

## 4. Stage Graph — Hand units

Shared non-goals for every unit (per goal + campaign): no candidate/draft
implementation or search policy, no model drafter, no cache
branch/checkpoint/commit, no device/Metal/CUDA work, no serving or retention,
no quantized KV, no new sampling algorithm, no throughput or speed claim, no
edit to `src/train.fab` or `src/optimize.fab` (foreign lane), no campaign or
sibling-goal file edits.

### SD0-U1 — Pinned dense baseline oracle

- **outcome**: `baseline.md` freezes `generate_dense_with_stop` as the named
  oracle — dense prefill capture, one-token `decode_step` advance, logits/token
  alignment, EOG/`StopPolicy` semantics, prompt tokens excluded from the
  repetition-penalty history, seed→RNG projection, k=1 behavior — and
  `generation.proba` gains executing determinism/stop-policy rows for that
  route.
- **write_scope**: `docs/factory/speculative-decode-contract/baseline.md` (new);
  `src/generation.proba` (new describe blocks only)
- **depends_on**: —
- **done_when**: a reviewer can reproduce the named baseline from `baseline.md`
  alone, and the new rows prove same-config/same-seed → identical stream plus
  the pinned `eog_stop` vs `IgnoreEos` divergence boundary.
- **first-failing oracle**: the same-seed determinism row (identical
  config+seed+stop → identical token list) fails first if the pinned route or
  its documented semantics are wrong.
- **sanity**: `faber test src/generation.proba <new-describe-filter>`
- **est**: S–M — basis: one focused doc page + 2–3 describe blocks; precedent:
  the existing stop-policy describe (`src/generation.proba:544`).
- **risk**: low — no product code; docs + additive proba.
- **integrable**: yes

### SD0-U2 — Versioned `AccelerationPolicy` on the generation config wire

- **outcome**: `generation.fab` gains one `AccelerationPolicy` value (modes:
  `disabled` constructor-default, `context_lookup`; policy version; block-size
  bounds ≥ 1; unknown mode/version/field rejects), `GenerationConfig` carries
  exactly one added field, `construct_generation` keeps its 9-arg signature and
  yields disabled, a new explicit policy constructor is added, `generation_equal`
  and `support_flags()` extend by the one field, and the wire migrates:
  `schema_version` `1.1.0` with one policy segment (13 parts) on serialize;
  deserialize accepts legacy `1.0.0` 12-part → disabled and `1.1.0` 13-part;
  every other shape rejects.
- **write_scope**: `src/generation.fab`; `src/generation.proba`
- **depends_on**: SD0-U1 (serializes the shared proba file)
- **done_when**: legacy `1.0.0` wires decode to disabled-policy configs, new
  policy values round-trip, and malformed/unknown-version/unknown-mode/extra-
  part wires all reject with pinned messages (including the inferentia-shaped
  13-part `1.0.0` "malformed generation config wire" row).
- **first-failing oracle**: the legacy-decode row
  (`deserialize_generation("generation/config/1.0.0/…")` → disabled policy)
  fails first if the migration breaks the existing consumer wire.
- **sanity**: `faber test src/generation.proba <wire/policy filters>`
- **est**: M — basis: wire migration + reject-row family on an 812-line module;
  precedent: the versioned-wire describe (`src/generation.proba:222-297`).
- **risk**: medium — public config surface with a live cross-repo consumer
  (`inferentia/src/main.fab:962`); mitigated by the additive constructor and
  legacy decode mandate.
- **integrable**: yes
- **non_goals**: no second acceleration knob, no lookup semantics, no behavior
  change for disabled configs.

### SD0-U3 — Candidate-provider seam (`gradus:speculative` leaf)

- **outcome**: new leaf `src/speculative.fab` defines the provider request
  (tokenized prompt context, accepted generation history, requested block size
  within policy bounds), the provider result (candidate ids + provenance, or a
  typed no-draft), and the purity contract (deterministic in its inputs; no RNG
  consumption; no cache/history/state mutation) — interface only, no search.
- **write_scope**: `src/speculative.fab` (new); `src/speculative.proba` (new);
  `src/gradus.fab` (one map-comment line)
- **depends_on**: SD0-U2 (policy owns the block-size bound authority)
- **done_when**: the context-lookup goal can implement one interface without
  touching generation or cache contracts; invalid block sizes and malformed
  requests reject through typed errors.
- **first-failing oracle**: the out-of-policy block-size reject row (request
  with block size outside the policy bounds → typed reject) fails first if the
  seam admits work the policy did not authorize.
- **sanity**: `faber test src/speculative.proba`
- **est**: M — basis: new value-contract leaf ~150–250 lines + proba; precedent:
  `gradus:parameter` / `gradus:serialize` contract leaves.
- **risk**: low
- **integrable**: yes

### SD0-U4 — Greedy acceptance contract + sampled typed reject

- **outcome**: `speculative.fab` adds the pure greedy first-divergence oracle
  (target token ids + candidate ids → accepted prefix length + first divergence
  index or none) and the admission check (policy + `GenerationConfig` →
  admitted-greedy | typed reject) where any sampled request (active
  temperature/top-k/top-p/min-p) under an enabled policy rejects before any
  provider call, RNG consumption, or history/state mutation; the future
  sampled-mode proof obligations are recorded as contract notes.
- **write_scope**: `src/speculative.fab`; `src/speculative.proba`
- **depends_on**: SD0-U2, SD0-U3
- **done_when**: greedy fixtures pin accepted/rejected/first-divergence
  outcomes; the sampled-reject fixture returns the same typed reject and leaves
  a supplied seed and history value untouched.
- **first-failing oracle**: the sampled-reject row (temperature > 0 +
  `context_lookup` policy → typed reject, seed/history bit-identical) fails
  first if a sampled request can reach lookup or RNG.
- **sanity**: `faber test src/speculative.proba <acceptance filters>`
- **est**: S–M — basis: two pure functions + fixture rows on the U3 leaf.
- **risk**: low
- **integrable**: yes

### SD0-U5 — Versioned receipt schema (`gradus:receipt` leaf)

- **outcome**: new leaf `src/receipt.fab` defines the versioned receipt value
  with fail-closed serialize/deserialize: regime is exactly
  `context-reproduction` or `ordinary-chat`; evidence labels distinguish
  `reference`/`compiled`/`metal`/`cuda` and `cold`/`warm`; fields bind policy +
  version, block size, accepted/rejected counts, first divergence, equivalence
  verdict, TTFT, and throughput; the constructor refuses any receipt carrying
  timing/throughput without an equivalence verdict.
- **write_scope**: `src/receipt.fab` (new); `src/receipt.proba` (new);
  `src/gradus.fab` (one map-comment line)
- **depends_on**: SD0-U2, SD0-U3 (serializes only the `gradus.fab` map edit)
- **done_when**: receipts round-trip through the wire; unknown
  regime/backend/version and throughput-without-equivalence reject; each
  receipt is independently classifiable by regime and evidence tier.
- **first-failing oracle**: the throughput-without-equivalence reject row fails
  first if a receipt can claim performance without a token-equivalence result.
- **sanity**: `faber test src/receipt.proba`
- **est**: M — basis: versioned wire + enum-label family mirroring the
  generation wire pattern.
- **risk**: low
- **integrable**: yes
- **non_goals**: no backend timing collection (inferentia/radix/hosts own
  execution receipts through their authorized paths), no fabricated receipts.

### SD0-U6 — Two-regime equivalence corpus + integrity check

- **outcome**: checked-in corpus rows for both regimes under
  `docs/factory/speculative-decode-contract/corpus/` binding regime,
  model/tokenizer identity, prompt ids, pinned `GenerationConfig` (disabled
  policy) + seed, expected stop behavior, and the baseline token stream
  captured from a real `generate_dense_with_stop` run (repeated-block prompts
  for context-reproduction; non-repeating prompts for ordinary-chat); new
  `scripta/check-corpus` validates structural integrity; `generation.proba`
  re-executes the dense baseline against the pinned rows.
- **write_scope**: `docs/factory/speculative-decode-contract/corpus/context-reproduction.json`
  (new); `docs/factory/speculative-decode-contract/corpus/ordinary-chat.json`
  (new); `scripta/check-corpus` (new); `src/generation.proba` (new describe)
- **depends_on**: SD0-U1, SD0-U2
- **done_when**: `scripta/check-corpus` exits 0 on both files and exits 1 on
  any missing binding field; the proba describe reproduces every pinned
  baseline stream through the live dense route.
- **first-failing oracle**: `scripta/check-corpus` on a corpus file missing any
  required binding (or a stream length beyond `max_tokens`) exits 1 first.
- **sanity**: `./scripta/check-corpus && faber test src/generation.proba <corpus filter>`
- **est**: M — basis: corpus capture runs the slow reference dense path (keep
  `max_tokens` small); the check script is a small structural validator.
- **risk**: low-medium — stream capture is minutes-scale on the MIR runner;
  mitigate with small token budgets, never hand-edit captured streams.
- **integrable**: yes

### SD0-U7 — Disabled-policy equivalence regression + contract handoff + closeout

- **outcome**: `generation.proba` proves a `1.1.0` disabled-policy config
  emits the identical token stream to the legacy `1.0.0` config under the same
  model/prompt/seed/stop; `handoff.md` publishes the exact consumed fields per
  downstream goal (kv-cache-branching: acceptance contract + baseline pointer;
  cached-block-verification: provider seam + first-divergence oracle;
  context-lookup-drafting: `context_lookup` policy mode + seam + corpus;
  prepared-prefix-state: receipt schema + corpus identity bindings;
  speculative-verification-execution and CUDA qualification: receipt regime and
  evidence labels); the goal ledger rows are marked done with receipts and the
  closeout block runs green.
- **write_scope**: `src/generation.proba` (one describe);
  `docs/factory/speculative-decode-contract/handoff.md` (new);
  `docs/factory/speculative-decode-contract/goal.md` (ledger rows + status line)
- **depends_on**: SD0-U1, SD0-U2, SD0-U3, SD0-U4, SD0-U5, SD0-U6
- **done_when**: no downstream goal must reinterpret policy, sampler, corpus,
  or receipt fields; no parallel fast-path API exists (grep-level check);
  disabled-policy regression green; closeout block green.
- **first-failing oracle**: the disabled-equivalence regression row
  (`1.1.0`-disabled stream ≡ `1.0.0` stream) fails first if the policy field
  leaks any behavior into the disabled path.
- **sanity**: `faber test src/generation.proba <disabled-equivalence filter>`
- **est**: S–M — basis: one regression describe + one handoff map page +
  ledger bookkeeping.
- **risk**: low — blocked, not weakened, if the foreign `check-source` red is
  still live at closeout.
- **integrable**: yes

## 5. Implementation Work

Mind files one Hand task per unit: pointer = goal path + this `id` + the
unit's `write_scope`/`done_when` above. Suggested dispatch order respecting the
graph: U1 → U2 → U3 → {U4, U5} (parallel, disjoint files) with U6 parallel
after U2 (touches only `generation.proba`, disjoint from U3/U4/U5), then U7.
All units are docs-or-additive-source changes; every unit is independently
integrable, so no merge gate beyond normal lane integration is required.

## 6. Checkpoints And Gates

**Batching decision**: seven Hands (the goal's six-unit sketch split at its
unit 5, which bundled receipt-schema code with corpus data — two behavior
families). No mega-Hand; no intra-unit phases.

**Lane-owned gates (named once, never on a child Hand)**:

- lint lane: `./scripta/check-source`
- test/compile lanes: `./scripta/check-compile`; focused `faber test` per
  touched proba file
- merge lane: path-limited docs+source commits; `git diff --check`
- factory audit: `python3 ../radix/scripta/audit-factory-goal-status.py --factory-root docs/factory --fail-on error`

**Delivery closeout (SD0-U7 runs; all must be green)**:

```bash
python3 ../radix/scripta/audit-factory-goal-status.py --factory-root docs/factory --fail-on error
./scripta/check-source
./scripta/check-compile
./scripta/check-corpus
faber test src/generation.proba
faber test src/speculative.proba
faber test src/receipt.proba
git diff --check
```

(`faber` invocations use `FABER_LIBRARY_HOME`/`FABER_BIN` exactly as
`scripta/check-compile` sets them.) If the foreign `check-source` red
(`textus` identifiers in `src/train.fab:272` / `src/optimize.fab:63`,
train-step U4b's repair surface) is still live, U7 reports blocked on the
handle — it never edits those files or weakens the gate.

**Release posture**: not-applicable — gradus has no package/release train; the
`1.0.0`→`1.1.0` wire bump is the versioned protocol migration inside U2, not a
release event.

## 7. Validation

Hand sanity is the per-unit focused `faber test` filter named above — nothing
wider. Lane gates own source/compile/package routes. Executed value identity
is mandatory where claimed: corpus streams and disabled-equivalence rows must
come from real `generate_dense_with_stop` runs on the MIR runner; compile-only
or receipt-shaped artifacts do not close their units (campaign invariant 9).

## 8. Companion Skill Plan

None required. Hands may run `$polish` over their primary touched files before
commit; no `$campaign` or `$factory` load is needed by the units themselves.

## 9. Open Questions

1. **Campaign status staleness** (Mind owns): `CAMPAIGN.md`'s status line says
   "no delivery or implementation has started"; it goes stale when SD0 lands.
   Campaign edits stay with Mind per the routing-artifact ownership rule.
2. **Foreign gate red** (sequencing): `./scripta/check-source` is red at HEAD
   from the train-step lane's committed `textus` identifiers. If U4b's repair
   has not landed by SD0-U7, U7 reports blocked rather than narrowing the gate.
3. **Corpus file format** (decided here, flagged for audit): JSON under the
   goal's `corpus/` dir with `scripta/check-corpus` as integrity owner — no
   repo precedent existed; gradus root `corpus/` is reserved for training
   demos and stays unused by SD0.

## Unit ledger

| Unit | Status | Seat | Receipt | Notes |
| --- | --- | --- | --- | --- |
| SD0-U1 | pending | — | — | baseline oracle pin |
| SD0-U2 | pending | — | — | versioned policy + wire migration |
| SD0-U3 | pending | — | — | provider seam leaf |
| SD0-U4 | pending | — | — | greedy acceptance + sampled reject |
| SD0-U5 | pending | — | — | receipt schema leaf |
| SD0-U6 | pending | — | — | two-regime corpus + integrity check |
| SD0-U7 | pending | — | — | equivalence regression + handoff + closeout |

---

<!-- Lowered from goal.md by planner handle bbbf8d85 on 2026-08-21. Goal
     ledger in goal.md remains the audit authority; this table tracks Hand
     dispatch. -->
