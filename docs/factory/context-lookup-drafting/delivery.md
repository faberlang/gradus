# DELIVERY: context-lookup-drafting — deterministic context-sourced candidates and transactional greedy integration

**Status**: lowered 2026-08-22 — U1 (`43c6a75`) and U2 (`d1898cf`) landed; U3 gated on SD2-U5 receipt (per unit graph); no dispatchable unit until then
**Goal:** [`goal.md`](goal.md) (goal-check verdict: **READY** — record below)
**Campaign:** [`speculative-decode`](../speculative-decode/CAMPAIGN.md) stage SD4 — the Mind task and SD0 handoff label it "SD3"; the campaign path numbers it SD4 (radix Metal execution holds SD3). Unit ids here use the campaign number; the handoff records both spellings.
**Repos:** primary `gradus/` (this repo); evidence-only `radix/`, `inferentia/` (no writes)
**Dependencies:** SD0 [`speculative-decode-contract`](../../archived/speculative-decode-contract/goal.md) done 7/7 (policy + seam + corpus + receipt schema landed); SD1 [`kv-cache-branching`](../../archived/kv-cache-branching/goal.md) done 6/6 (transaction seam landed); SD2 [`cached-block-verification`](../cached-block-verification/delivery.md) **lowered, not landed** — U3 depends on its U5 verify seam (cross-goal dep, declared below).

---

## 0. Goal check (gate for this lowering)

**Verdict: READY.** Evaluator: planner. Consumer: delivery. Goal source pins
re-verified against the live gradus tree 2026-08-22 (drift is line-number
only); SD0/SD1 dependencies confirmed landed; the one material finding — the
closed receipt wire lacks the fallback/overhead fields the goal requires — is
resolved by a pinned additive schema bump inside U5 and flagged for Mind
(OQ1), not an architecture gap.

| Goal claim | Live check | Result |
| --- | --- | --- |
| Generation samples one target token then one cached decode step at a time (`generation.fab:706-740, 769-811`) | `generate_with_stop` `:845`; `generate_dense_with_stop` `:924` advances through scalar `dense.decode_step` (`dense.fab:500`) | live |
| `GenerationConfig` is a versioned, validated authority; unknown controls rejected (`generation.fab:189-327, 362-427`) | Ten-field config (nine controls + `AccelerationPolicy` `:245` with `min_block`/`max_block`), `construct_generation_with_policy` fail-closed, wire `1.1.0` with legacy `1.0.0` → disabled (SD0-U2, commit `ce08816`) | live — SD4 consumes; never extends |
| No lookup/draft provider in the tree | `src/speculative.fab` freezes the seam only ("This module has no propose implementation" — module header); grep finds no lookup provider | live — all provider code is new |
| SD0 contract dependency | `speculative.fab`: `SpeculativeError` (incl. `SampledAccelerationRejected`), `ProviderRequest`/`ProviderResult`/provenance via `construct_request(min_block, max_block)`, `GreedyAcceptance`, `first_divergence` `:150`; handoff `context-lookup-drafting` row frozen; corpus `context-reproduction.json` + `ordinary-chat.json` with fail-closed `scripta/check-corpus` | satisfied |
| SD1 dependency (branch/commit) | `cache_branch.fab` transaction seam landed (`begin`/`inspect`/`abort`/`commit_transaction`) | satisfied |
| SD2 dependency (block verification) | [`../cached-block-verification/delivery.md`](../cached-block-verification/delivery.md) lowered this pass; U5 owns the verify seam | declared cross-goal dep: SD4-U3 waits on SD2-U5 |
| OQ1 window default | Policy's only bounds are `min_block`/`max_block`; no window field exists and config extension is a goal non-goal | **pinned here**: window maximum `= min(policy.max_block, tokens_available − 1)` where `tokens_available = prompt + accepted history`; search suffix lengths downward to 1; a match must have a following source token; the reject boundary is the existing `construct_request` policy bounds — no new wire field |
| OQ2 tie rule | Provenance already carries `source_offset` + `match_length` | **pinned here**: longest exact match first, then lowest source offset; any change must move fixtures and receipt provenance together |
| OQ3 sampler policy | `admit_greedy` + `SampledAccelerationRejected` landed (SD0-U4) | default holds: `no_draft` → plain target step; sampled request → typed reject **before** lookup, RNG, or branch |
| Receipt fields (goal §6: draft length, acceptance rate, fallback rate, overhead as separate measured fields) | `Receipt` v1.0.0 closed wire carries policy/version/block_size/accepted/rejected/first_divergence/equivalence/ttft/throughput/backend/regime/warmth only | **gap, pinned**: U5 extends `gradus:receipt` additively to `1.1.0` (fallback + overhead + draft-length fields; `1.0.0` wires still decode — the generation `1.0.0→1.1.0` precedent); Mind ack requested (OQ1) |

## 1. Interpreted theme

The dense loop can only take one target step at a time, and the SD0 policy
wire can say `context_lookup` but nothing answers it. SD4 supplies the
weightless candidate source — exact token lookup over the request's own
prompt + accepted history, deterministic and pure — and the generation
integration that feeds candidates through the SD2 verify seam and the SD1
transaction, staging accepted history, output cursor/budget, and stop state
so the accelerated greedy stream is provably identical to
`generate_dense_with_stop`, while sampled acceleration rejects before any
work and empty lookup falls back to the plain step without relabeling.

## 2. Normalized spec

A new leaf `src/context_lookup.fab` (module `gradus:context_lookup`, one
map-comment line in `src/gradus.fab`) owns the provider family: the frozen
search semantics (window/tie/extension/fallback contract) and the
deterministic `propose` implementation against the SD0 `ProviderRequest`/
`ProviderResult` seam. Generation integration lands inside
`generate_dense_with_stop` in `src/generation.fab` (no new public generate
entry — the SD0 parallel-fast-path check must stay true): policy dispatch on
`acceleration.mode`; `admit_greedy` before anything else; provider request
from prompt + accepted history; SD2-U5 verify; SD1 `commit_transaction`;
transactional staging of accepted history, emitted/budget cursor, and stop
state, published only after commit. Evidence closes with an additive
`receipt` schema bump to `1.1.0` and regime-labeled receipts for both
checked-in corpora, reference tier only.

Delivery-level non-goals (inherited from goal §Non-goals): no model drafter/
MTP/DFlash/weights; no kernel/device/scheduler/HTTP; no cross-request prefix
cache or tenant policy; no new sampling algorithm or unproven
sampled-equivalence claim; no `GenerationConfig` extension or parallel
speculative API; no device or product performance claim.

## 3. Repo-aware baseline

| Surface | Today | Note |
| --- | --- | --- |
| Provider seam | `speculative.fab`: `construct_request(prompt, history, block_size, min_block, max_block)`, `ProviderResult` (`candidates`/`no_draft`), provenance `{source="context_lookup", source_offset, match_length}` | U2 implements against this seam; SD0 owns the types |
| Policy wire | `AccelerationPolicy {version "1.0.0", mode, min_block, max_block}` on `GenerationConfig` (`generation.fab:245`); `admit_greedy` reject vocabulary | U3 dispatch source; bounds feed `construct_request` |
| Baseline loop | `generate_dense_with_stop` `:924` (campaign invariant 1 oracle); `dense.decode_step` `:500` | disabled path stays byte-identical in behavior (U4 regression) |
| Transaction | `cache_branch.fab` `begin`/`inspect`/`abort`/`commit_transaction` | U3's only branch/commit path |
| Verify seam | SD2-U5 `BlockVerification` (lowered, not landed) | U3's cross-goal gate |
| Corpus + receipts | `docs/archived/speculative-decode-contract/corpus/{context-reproduction,ordinary-chat}.json`; `scripta/check-corpus` fail-closed; `receipt.fab` v1.0.0 closed wire, `absent_timing = -1.0` | U5 inputs + evidence carrier |
| Proba discipline | co-located `*.proba`; `faber test src/<file>.proba <filter>` | Hand sanity is file + filter; package-wide runs banned pending the radix loader fix — verify at dispatch |
| Foreign fences | gradus tree clean 2026-08-22 | `generation.fab` last touched by SD0-U2 (`ce08816`) — re-check `git status` at dispatch |

## 4. Unit graph — Hand units

```text
SD4-U1 (search contract) ──> SD4-U2 (deterministic provider) ──┐
                                                                ├──> SD4-U3 (generation integration, gated on SD2-U5)
                                                                │          │
                                                                │          v
                                                                │      SD4-U4 (fallback + reject proofs)
                                                                │          │
                                              SD4-U5 (receipt schema bump + two-corpus receipts) <─ U2, U3, U4
```

SD4-U1/U2 share no file with any SD2 unit and nothing in radix — they are
dispatchable immediately, in parallel with the SD2 spine.

Shared non-goals for every unit (goal §Non-goals + campaign invariants 1–4, 7):
no model drafter or learned proposal; no device/kernel/residency/scheduler;
no cross-request/tenant reuse; no sampling algorithm change; no RNG contact
while proposing; no `GenerationConfig`/wire extension; no second generate API;
no edits to `src/speculative.fab`, `src/cache_branch.fab`, `src/cache.fab`,
`src/model/dense.fab`, or SD2's leaf; no campaign or sibling-goal file edits.

### SD4-U1 — search and fallback contract

| Field | Value |
| --- | --- |
| outcome | `context_lookup.fab` freezes the search semantics as typed, testable contract pieces: the pinned window rule (suffix lengths from `min(max_block, tokens_available − 1)` downward to 1, following source token required), the tie rule (longest exact match, then lowest source offset), candidate extension bounds (through `max_block` and available context), empty-result = ordinary `no_draft` fallback (never an error), and the typed reject boundary (malformed state / out-of-policy bounds reject through the SD0 `SpeculativeError` vocabulary — no silent downgrade). Constants and admission helpers are public and pure; no search loop yet. |
| write_scope | `src/context_lookup.fab` (new); `src/context_lookup.proba` (new); `src/gradus.fab` (one map-comment line) |
| done_when | proba rows prove: window maximum honors both `max_block` and available-context caps; suffix lengths enumerate downward to 1; the following-token requirement rejects a match at the context tail; extension clamps at `max_block` and context end; empty-context/undersized requests reject typed; no new config or policy wire field exists (grep) |
| first-failing oracle | the window-bound reject rows cannot run today — no lookup module exists (grep-clean verified) |
| depends_on | — (consumes landed SD0 policy/seam types only) |
| parallel | **yes** — new files; disjoint from the entire SD2 spine and all radix lanes. Coordinate the one `gradus.fab` comment line with SD2-U1's (land sequentially; trivial) |
| sanity | `faber test src/context_lookup.proba contract` |
| non_goals | the search implementation (U2); generation integration (U3); receipt fields (U5) |
| risk | low — additive leaf over landed types |
| integrable | yes |

### SD4-U2 — deterministic context-only provider

| Field | Value |
| --- | --- |
| outcome | `context_lookup.fab` implements `propose` against the frozen seam: exact token-id matching over prompt + accepted history only (no text normalization, no request-boundary crossing, no unaccepted candidate tokens), under the U1 window/tie/extension rules; results are `construct_candidates` with provenance `{source = "context_lookup", source_offset, match_length}` or `no_draft()`. A pure function of `ProviderRequest`: equal requests → equal results; consumes no seed/RNG, mutates no cache/history/generation state; module imports no sampling/train surface. |
| write_scope | `src/context_lookup.fab`; `src/context_lookup.proba` |
| done_when | proba rows prove: repeated identical requests return identical candidates + metadata; longest-match beats shorter matches; lowest offset breaks ties; window cap and candidate cap clamp; context-repetition fixture (a repeated phrase in prompt) returns the following tokens; no-occurrence fixture returns `no_draft`; purity row shows no sampling/train import and unchanged inputs after propose |
| first-failing oracle | the same-input same-output repeatability row fails today (no propose implementation exists) |
| depends_on | SD4-U1 |
| parallel | no within SD4 (same leaf); **yes** relative to SD2 — zero shared files |
| sanity | `faber test src/context_lookup.proba propose` |
| non_goals | acceptance or verification (SD2); generation loop changes (U3); performance measurement |
| risk | low-medium — deterministic search; the care point is exact token-id discipline (no text fallback) |
| integrable | yes |

### SD4-U3 — verification-loop and generation integration (transactional staging)

| Field | Value |
| --- | --- |
| outcome | `generation.fab`'s `generate_dense_with_stop` gains the policy dispatch **inside the existing loop** (no new public entry): `disabled` → the current scalar `dense.decode_step` path unchanged; `context_lookup` → `admit_greedy` first (a sampled request throws the SD0 `SampledAccelerationRejected` typed reject **before** any provider call, RNG advance, or branch creation), then provider request from prompt + accepted history with block size inside `[min_block, max_block]`, SD2-U5 verify over a checkpoint of the current layers, greedy acceptance, SD1 `commit_transaction` for the accepted `n`. Accepted token history, output cursor (`emitted`)/budget, and stop state are staged alongside the cache branch and published only after the target acceptance commits; abort or verify failure leaves every one of those facts unchanged and the loop continues by the plain target step with no relabeling. |
| write_scope | `src/generation.fab`; `src/generation.proba` |
| done_when | proba rows prove: greedy plain-vs-lookup fixtures emit identical tokens and end with identical layer states, histories, and cursor/stop facts; a sampled-policy request rejects typed with zero provider invocations and an untouched seed/history (assert state before/after); a forced mid-transaction failure leaves all staged facts equal to pre-step; `disabled` fixtures still route through the unchanged scalar path |
| first-failing oracle | the sampled-reject-before-lookup row fails today — `generate_dense_with_stop` ignores the policy (no dispatch exists) |
| depends_on | SD4-U2; **SD2-U5** (cross-goal: the verify seam; hold dispatch until its receipt lands); SD1 (landed) |
| parallel | no — `generation.fab` is the campaign's baseline oracle surface; also gated on SD2 |
| sanity | `faber test src/generation.proba lookup` |
| non_goals | fallback/reject proof matrix (U4); receipts (U5); any edit to `dense.fab`/decode paths; a second public generate API |
| boundary rule | campaign invariant 1: `generate_dense_with_stop` remains the named oracle — the disabled path must be behavior-identical (U4 proves it); if integration cannot preserve the plain path, stop and report rather than forking a fast-path entry |
| risk | high — the transactional heart plus baseline preservation; mitigated by the U4 regression matrix and the landed SD1/SD2 seams it composes |
| integrable | yes |

### SD4-U4 — disabled/no-match fallback and reject behavior

| Field | Value |
| --- | --- |
| outcome | The fallback and reject behavior family, proven: disabled policy performs the plain target step with no acceleration claim (bit-identical stream to the SD0 baseline fixtures); `no_draft` lookup takes the plain target step as an ordinary fallback — no receipt or label may claim acceleration for it; malformed or unsupported policy values (unknown version/mode, `min_block > max_block`, zero bounds) retain the SD0 constructors' typed rejects before any lookup runs; a forced equivalence mismatch surfaces as divergence, never hidden behind a fallback label. |
| write_scope | `src/generation.proba`; `src/context_lookup.proba`; `src/generation.fab` (only if U3 review names a concrete dispatch gap — otherwise untouched) |
| done_when | regression rows: disabled-policy fixtures match the SD0 corpus baseline streams (`scripta/check-corpus` inputs); no-match fixture emits the plain stream with no acceleration provenance; malformed-policy rows reject typed with zero provider calls; forced-mismatch fixture reports the divergence rather than passing |
| first-failing oracle | the no-match-no-acceleration-claim row fails today (no dispatch exists to fall back from) |
| depends_on | SD4-U3 |
| parallel | no — proves U3's landed dispatch |
| sanity | `faber test src/generation.proba fallback` |
| non_goals | new dispatch logic beyond a named U3 gap; receipts (U5); sampled admission (campaign-settled reject) |
| risk | low — proof unit over landed behavior |
| integrable | yes |

### SD4-U5 — receipt schema bump and two-corpus regime receipts

| Field | Value |
| --- | --- |
| outcome | `receipt.fab` extends additively to schema `1.1.0`: draft length, fallback count/rate, and overhead as separate measured fields (constructors + wire; `1.0.0` wires still decode — the generation `1.0.0→1.1.0` migration precedent; no second receipt module). Then produce reference-tier receipts for both checked-in corpora (`context-reproduction`, `ordinary-chat`): regime, context, policy/version, block size, accepted/rejected counts, draft length, acceptance and fallback rates, overhead, first divergence, and the equivalence verdict — timings carried only where honestly measurable in the reference tier, `absent_timing` (`-1.0`) otherwise; equivalence always precedes any timing (the v1.0.0 rule, preserved). Receipts checked in under this goal dir. |
| write_scope | `src/receipt.fab` (additive `1.1.0` fields/constructors/wire); `src/receipt.proba`; `docs/factory/context-lookup-drafting/receipts/` (new, checked-in JSON rows for both regimes) |
| done_when | schema rows: `1.1.0` round-trips the new fields and still decodes `1.0.0` wires; unknown fields/versions reject as before. Receipt rows: both corpora produce classifiable receipts (regime + `backend=reference` + warmth) with equivalence verdicts recorded before any timing; acceptance/fallback/overhead are separate fields; first divergence recorded; no device or product performance claim present |
| first-failing oracle | the `1.1.0` round-trip row fails today — the closed v1.0.0 wire rejects the new fields by construction |
| depends_on | SD4-U2, SD4-U3, SD4-U4 |
| parallel | no — closes the goal |
| sanity | `faber test src/receipt.proba schema` |
| non_goals | device/compiled/Metal/CUDA receipts (radix goals); throughput targets from the external post; corpus rewrites (`check-corpus` inputs are frozen SD0 assets) |
| boundary rule | the schema bump touches SD0's frozen wire — additive + versioned only; Mind ack per OQ1 before dispatch |
| risk | medium — wire change on a frozen contract; mitigated by the closed-wire reject discipline and legacy decode rows |
| integrable | yes |

## 5. Implementation Work (Mind pointers)

Each Hand task is a pointer: goal path + unit id + write_scope + done_when
from §4. **Dispatch order:** U1 → U2 immediately (new files, no overlap with
SD2 or radix; sequence the two `gradus.fab` comment-line touches); hold U3
until SD2-U5's receipt lands; U4 after U3; U5 last (schema ack first). The
whole goal's gradus surface is disjoint from the blocked radix `mir-llvm`
work.

## 6. Checkpoints and gates

**Batching:** five Hands, no merge gate — each unit lands green at its own
commit. U1→U2 and (SD2 spine) run concurrently; U3→U4→U5 serial.

**Lane-owned gates (named once, never copied onto child Hands):**

| Lane | Owns |
| --- | --- |
| lint | `./scripta/check-source` |
| test/compile | `./scripta/check-compile`; focused `faber test src/<leaf>.proba <filter>` (file + filter only; package-wide runs banned pending the radix loader fix); `./scripta/check-corpus` stays green over the frozen SD0 corpus |
| merge | path-limited source+docs commits; `git diff --check` |
| factory audit | `python3 ../radix/scripta/audit-factory-goal-status.py --factory-root docs/factory --fail-on error` |

**Delivery closeout (final unit runs; all green or honestly blocked-reported):**

```bash
python3 ../radix/scripta/audit-factory-goal-status.py --factory-root docs/factory --fail-on error
./scripta/check-source
./scripta/check-compile
./scripta/check-corpus
faber test src/context_lookup.proba
faber test src/generation.proba
faber test src/receipt.proba
git diff --check
```

**Release posture:** not-applicable — reference library evidence; the radix
device goals and Inferentia consumer produce their own tiered receipts later.

## 7. Open questions for Mind

1. **Receipt schema `1.1.0` ack (U5).** The goal's separate fallback/overhead/draft-length fields cannot ride the closed v1.0.0 wire. Default: additive, versioned bump in `gradus:receipt` with legacy decode. This touches an SD0-frozen contract — ack before U5 dispatches, or amend the goal to drop the separate fields.
2. **Window pin (OQ1).** Pinned `min(max_block, tokens_available − 1)` downward — the only policy bounds that exist, honoring the no-config-extension non-goal. If the operator wants an independent window knob, that is a goal amendment (new wire field), not a delivery choice.
3. **U3 hold point.** U3 cannot dispatch until SD2-U5 lands. U1/U2 are not blocked — file them against this goal now if seats are free.
4. **Leaf name.** Default `gradus:context_lookup` (`src/context_lookup.fab`). Flag to rename.
