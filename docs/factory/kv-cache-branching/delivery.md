# DELIVERY: kv-cache-branching — immutable all-layer speculative branches with atomic prefix commit

**Status**: lowered 2026-08-22 — ready for Mind to file Hands (U1/U2 dispatchable now; U3 gated on SD0-U7's handoff; U6 after the cache.proba classification seat)
**Goal:** [`goal.md`](goal.md) (goal-check verdict: **READY** — record below)
**Campaign:** [`speculative-decode`](../speculative-decode/CAMPAIGN.md) stage SD1 (gate: immutable checkpoint, private branch, zero/partial/full commit, unchanged base on failure, no device handles)
**Repos:** primary `gradus/` (this repo); evidence-only `inferentia/`, `radix/`, `hosts/` (no writes)
**Live-seat fences:** SD0-U6/U7 pending behind the expfix (53bf8fba) + pkghang (ed794237) seats — U3's contract consumption is to-verify-at-dispatch against SD0-U7's `handoff.md`; the gradus cache.proba classification seat (a816aad1) owns `src/cache.proba` classification — U6's cache.fab header edits serialize behind its receipt; B2 safetensors + sampling seats own `src/model/safetensors.*` / `src/sampling.*` (disjoint). See §3 Foreign lanes.

---

## 0. Goal check (gate for this lowering)

**Verdict: READY.** Evaluator: planner. Consumer: delivery. Every source pin
re-verified against the live gradus tree 2026-08-22 (drifts are line-number
only); the goal's four open questions all pin against live code; SD0's landed
contract surface (U1–U5) is confirmed present so SD1 consumes rather than
redefines.

| Goal claim | Live check | Result |
| --- | --- | --- |
| Cache supports one-token `append`, batched `extend`, whole-cache `reset` only (`cache.fab:386-469`) | `append` `:403`, `extend` `:441`, `reset` `:480` (each `_keep(...)`-constructed; `version + 1` per write) | live; ~15-line drift |
| `cache_equal` compares values but no API coordinates an all-layer prefix (`:306-323`) | `cache_equal` `:317`; no all-layer/multi-layer cache API exists anywhere in `src/` | live |
| Dense route enforces a shared prefix for all layers; one-token cached continuation (`dense.fab:488-560`); prefill admits multi-row only from empty prefix (`:563-648`) | `decode_step` `:492`; `prefill_cached` `:580`; `_shared_prefix` `:319` + `_admit_cached` `:330` already compute the all-layer shared-prefix invariant | live; `_shared_prefix` is U1's natural checker (consume, don't reinvent) |
| Identity records exact prefix metadata but no branch ownership/snapshot lifetime (`cache.fab:471-555`) | `CacheIdentity` class `:495` (9 fields), `cache_identity_equal` `:545`, `cache_identity` `:561`, wire `serialize/deserialize_identity` `:579/:588` | live; opaque-equality use confirmed |
| No branch/checkpoint/commit surface exists | grep clean — no `KVCheckpoint`/`SpeculativeBranch`/branch/commit API (`decode.fab`'s "cooperative checkpoint" is PML5-U5 cancellation, unrelated) | live — all SD1 code paths are new |
| SD0 contract dependency | SD0 goal ledger: **5/7 landed (U1–U5)**; `src/speculative.fab` present with `GreedyAcceptance {accepted_prefix, divergence}` + `first_divergence` + `acceptance_equal` (U4); `src/receipt.fab` (U5); `baseline.md` (U1) | live — U3 wraps `GreedyAcceptance`, never redefines acceptance |
| OQ3 epoch representation (unpinned in goal) | `KVCache.version: int`, bumped `+1` by every `_keep` write today | **pinned here**: branch creation does not advance; one successful commit advances exactly once (`base.version + 1`, all layers together); `n = 0` returns an equivalent base state with version unchanged; failed commit/aborted branch leave it unchanged |
| OQ4 capacity accounting (unpinned in goal) | `_admit_write(c, added)` `:346` rejects `write_position + added > capacity` **before any row exists**; `HELPER_CAPACITY = 2048` `:336` | **pinned here**: branch admission runs the same `_admit_write` bound against the base prefix; overflow rejects with no partially extended layer set |
| OQ2 value-copy boundary | `_keep` constructs fresh `KVCache` values; tensors are staged f32 (`_tensor`) | default holds: functional values, fresh tensors at the logical boundary; structural sharing only if unobservable |

No architecture gap. The only structural decision the goal left open — where
the new values live — is settled below (new leaf, SD0 precedent), not invented
architecture: `cache.fab` is a live seat surface and the campaign gives SD2–SD5
one import point.

## 1. Interpreted theme

The cache has single-mutation primitives but no transaction: a speculative
candidate cannot be evaluated without either mutating the shared cache or
rebuilding it wholesale, and a rejected candidate would leak rows to other
consumers. SD1 adds the value-level transaction — checkpoint, private branch,
accepted-prefix commit — with all-layer atomicity and unchanged-on-failure as
the contract, and no physical handles anywhere.

## 2. Normalized spec

A new leaf `src/cache_branch.fab` (module `gradus:cache_branch`, one
map-comment line in `src/gradus.fab` — the SD0 `speculative`/`receipt`
precedent) owns the whole transaction contract: an immutable `KVCheckpoint`
over `list<kv.KVCache>` (all layers same accepted prefix, identity-compatible,
base version recorded); a `SpeculativeBranch` value materialized from one
checkpoint plus a bounded candidate block with independent per-layer logical
state and candidate provenance; a typed acceptance/decision result wrapping
`gradus:speculative`'s landed `GreedyAcceptance` (accepted count `n` from
`accepted_prefix_length()`, never recomputed); and one atomic
`commit(checkpoint, branch, n)` producing a fresh all-layer state — every
layer `base prefix + first n branch rows`, version `base + 1` exactly once on
`n > 0`, `n = 0` an equivalent base state, invalid `n`/identity mismatch
rejected with zero partial writes. A device-neutral begin/inspect/commit/abort
seam exposes the lifecycle to SD2–SD5 consumers. No dense logits, no policy,
no generation state, no device anything.

Delivery-level non-goals (inherited from goal §Non-goals): no acceptance
policy or lookup drafting (SD0/SD3); no generation history/cursor/stop/RNG
transaction (SD3 context-lookup); no prepared-state identity/payload binding
(SD4); no device handles, kernels, residency, quantization; no `trim(shared)`
escape hatch; no identity-field additions or wire changes.

## 3. Repo-aware baseline

| Surface | Today | Note |
| --- | --- | --- |
| Cache value | `KVCache {model, model_version, config, tokenizer, history, key: tensor, payload: tensor, version, dimension, capacity}`; `_keep` `:355` the sole constructor path; `_admit_write` `:346` the capacity gate | branch/commit build on `_keep` + `_admit_write` semantics |
| All-layer type | `list<kv.KVCache>` (`dense.fab:319` `_shared_prefix`, `:330` `_admit_cached`, `:482` `empty_caches`) | checkpoint's payload type — already the dense route's currency |
| Acceptance contract | `gradus:speculative` `GreedyAcceptance`/`first_divergence`/`acceptance_equal` (landed SD0-U4) | U3 wraps; SD0-U7's handoff.md will pin the consumed fields — to-verify-at-dispatch |
| New-leaf precedent | `speculative.fab`/`receipt.fab` + one map-comment line each in `gradus.fab` | same shape for `cache_branch.fab` |
| Proba discipline | co-located `*.proba`; `faber test src/<file>.proba <filter>` runs focused rows on the MIR runner | Hand sanity is file + filter; the package-route loader defect (pkghang, ed794237, in flight) makes package-wide runs hang — never use them |
| Foreign lanes | **a816aad1 (live)**: `src/cache.proba` classification/fixes. **B2 (live)**: `src/model/safetensors.*`, `src/sampling.*`, fixtures. **SD0-U6/U7 seats**: expfix 53bf8fba (runner exp overflow) + pkghang 19-classification gate | no unit writes a foreign file; U6's `cache.fab` header-comment edits serialize behind a816aad1; U1–U5 write only new files + `gradus.fab` comment line (verify clean at dispatch) |

## 4. Stage Graph — Hand units

```text
SD1-U1 (checkpoint) ──> SD1-U2 (branch) ──> SD1-U3 (decision, gated on SD0-U7 handoff)
                              │                     │
                              └──────> SD1-U4 (atomic commit)
                                                            │
                                        SD1-U5 (transaction seam) <─ U1..U4
                                                            │
                                        SD1-U6 (truth pass + closeout, after a816aad1)
```

Shared non-goals for every unit (per goal + campaign invariants 4–5, 9): no
candidate/draft policy, no model drafter, no dense logits production, no
device/Metal/CUDA work, no quantized KV, no sampling/RNG contact, no edit to
`src/train.fab`/`src/optimize.fab`/`src/sampling.fab`/`src/model/safetensors.fab`
(foreign lanes), no sibling-goal or campaign file edits (U6's own goal/ledger
excepted), no throughput claims.

### SD1-U1 — `KVCheckpoint` value + all-layer invariant

| Field | Value |
| --- | --- |
| outcome | `cache_branch.fab` defines the immutable `KVCheckpoint` over `list<kv.KVCache>`: construction requires every layer at the same accepted prefix (reuse `dense.fab`'s `_shared_prefix` shape or an equivalent local check), layer identities equal under the existing opaque `cache_identity_equal` (model/version/config/tokenizer/dtype/layout fields), and records the all-layer prefix length, the identity value, and the base `version`. Mismatched layer lengths or identities reject typed before any value exists (unchanged-on-failure rule). Checkpoint equality is value equality over those facts. No new identity fields, no wire, no `_keep` bypass. |
| write_scope | `src/cache_branch.fab` (new); `src/cache_branch.proba` (new); `src/gradus.fab` (one map-comment line) |
| done_when | proba rows prove: equal multi-layer caches → constructible checkpoint, equality holds; one short layer → typed reject; one layer with a different model/config/tokenizer/dtype/layout → typed reject; reject leaves inputs untouched (functional values — assert equality after) |
| first-failing oracle | the mismatched-layers reject row cannot run today — no checkpoint API exists (grep-clean verified); red until U1 lands |
| depends_on | — |
| sanity | `faber test src/cache_branch.proba checkpoint` |
| non_goals | branch materialization (U2); identity field additions or a new identity wire; dense-route integration; `_shared_prefix` edits in `dense.fab` |
| boundary rule | `gradus.fab` carries one comment line only; verify `git status` clean on it at dispatch (not in any live seat's M list today) |
| risk | low — new leaf, additive |
| integrable | yes |

### SD1-U2 — `SpeculativeBranch` materialization (independent logical state)

| Field | Value |
| --- | --- |
| outcome | `cache_branch.fab` adds branch creation from one checkpoint plus a bounded candidate block (token ids + per-layer `[k, dim]` f32 K/V rows): every layer's candidate state is an independent logical value (fresh tensors at the boundary; `_keep` semantics), provenance records the target rows/candidate facts the caller needs. Capacity admits through the same `_admit_write` bound against the base prefix (overflow rejects before any layer extends). Shape/gap/identity/numeric failures return typed errors; the checkpoint is unchanged on success and on every failure. No write-through, no trim, no shared mutation. |
| write_scope | `src/cache_branch.fab`; `src/cache_branch.proba` |
| done_when | proba rows prove: branch construction leaves every checkpoint field equal (history, lengths, tensors, version, identity — full-field assert); capacity overflow rejects with all layers at base length; wrong-shape K/V, gap, and identity-mismatch candidates reject typed; multi-layer alignment rows (3+ layers) hold |
| first-failing oracle | the checkpoint-unchanged-after-branch row fails today (no branch API exists) |
| depends_on | SD1-U1 |
| sanity | `faber test src/cache_branch.proba branch` |
| non_goals | candidate evaluation against a model (dense logits are SD2); acceptance decisions (U3); commit (U4); structural sharing optimizations that could alias base tensors |
| boundary rule | none beyond shared non-goals |
| risk | low-medium — value-copy discipline is the care point; proba asserts full-field isolation |
| integrable | yes |

### SD1-U3 — Acceptance/decision result (wraps the landed SD0 contract)

| Field | Value |
| --- | --- |
| outcome | `cache_branch.fab` adds the typed commit decision: candidate count `k`, accepted count `n` sourced from `gradus:speculative`'s `GreedyAcceptance.accepted_prefix_length()` (the landed SD0-U4 contract — never recomputed here), discarded suffix `k − n`, the resulting identity facts, and the target rows the caller requires. `n` outside `0..=k` rejects typed with no state contact. Zero/partial/full acceptance are distinguishable values. |
| write_scope | `src/cache_branch.fab`; `src/cache_branch.proba` |
| done_when | proba rows prove: zero/partial/full decisions distinct and comparable; `n < 0` and `n > k` reject typed; the accepted count equals `GreedyAcceptance.accepted_prefix_length()` for fixture inputs (wrap, not reimplementation) |
| first-failing oracle | the out-of-range `n` reject row fails today (no decision API exists) |
| depends_on | SD1-U1, SD1-U2, **SD0-U7 handoff (pending)** — U7 publishes `handoff.md`'s kv-cache-branching row (acceptance contract + baseline pointer); the live shape is verified today (`speculative.fab` landed) and marked **to-verify-at-dispatch**: re-check `handoff.md` + `speculative.fab` for drift before this unit dispatches |
| sanity | `faber test src/cache_branch.proba decision` |
| non_goals | recomputing acceptance or divergence (SD0 owns the oracle); sampled-mode handling (campaign invariant 4 — greedy only); policy admission checks |
| boundary rule | if SD0-U7 is still blocked at dispatch (expfix/pkghang seats), Mind may dispatch U3 against the verified live `speculative.fab` shape with an explicit ack on the handle — the handoff row is the confirmation, not new information |
| risk | low — pure typed value over landed contracts |
| integrable | yes |

### SD1-U4 — Atomic all-layer prefix commit

| Field | Value |
| --- | --- |
| outcome | `cache_branch.fab` adds `commit(checkpoint, branch, n) → all-layer state`: every layer becomes base prefix + exactly the first `n` branch rows (fresh `_keep`-constructed values — no in-place mutation, no `trim(shared)`), history/identity recomputed through the existing conventions (comma-joined prefix, `"0..§"` position span), and `version = base.version + 1` advancing exactly once across all layers on `n > 0`. `n = 0` returns a state equal to the base (version unchanged). Invalid `n` or branch/checkpoint identity mismatch rejects with zero partial writes; every failure leaves the checkpoint unchanged. |
| write_scope | `src/cache_branch.fab`; `src/cache_branch.proba` |
| done_when | proba rows prove: full acceptance → all layers same accepted length/history/identity and version `+1` exactly once; partial → suffix rows absent from every layer; zero → state equal to base including version; identity mismatch and `n` out of range → typed reject with checkpoint equal after; multi-layer fixture (3+ layers) demonstrates all-layer simultaneity (no interleaved length states exist as values) |
| first-failing oracle | the partial-commit row fails today (no commit API exists); its absence is the campaign's F-finding — the shared-cache trim the campaign bans has no seam to misuse |
| depends_on | SD1-U1, SD1-U2, SD1-U3 |
| sanity | `faber test src/cache_branch.proba commit` |
| non_goals | epoch/version redesign beyond the pinned `+1` rule; generation cursor/stop state coordination (SD3); prepared-state payload binding (SD4); any device residency |
| boundary rule | OQ3 is pinned in §0 — if implementation finds the pinned rule contradicts a live `_keep` invariant, stop and report rather than choosing a different epoch rule |
| risk | medium — the atomicity heart of the goal; mitigated by functional-value construction (no in-place path exists to get wrong) |
| integrable | yes |

### SD1-U5 — Device-neutral consumer transaction seam

| Field | Value |
| --- | --- |
| outcome | `cache_branch.fab` exposes the begin/inspect/commit/abort lifecycle as one public logical seam over U1–U4 values: begin(checkpoint, block) → branch handle; inspect → decision facts; commit(n) → new all-layer state; abort → discard branch, base unchanged. A synthetic multi-layer fixture exercises the whole lifecycle. No dense logits, no candidate policy, no device execution, no scheduler state — the seam SD2 (cached-block) and SD4 (prepared-state) consume. |
| write_scope | `src/cache_branch.fab`; `src/cache_branch.proba` |
| done_when | lifecycle proba rows: begin → zero/partial/full commit; abort leaves the base checkpoint equal; stale checkpoint (a checkpoint taken before a later commit) rejects against the newer state; the fixture drives 3+ layers through begin→inspect→commit end to end |
| first-failing oracle | the stale-checkpoint reject row fails today (no lifecycle exists) |
| depends_on | SD1-U1..U4 |
| sanity | `faber test src/cache_branch.proba transaction` |
| non_goals | integration with `generate_dense_with_stop` or the policy dispatch (SD3/SD0); inferentia retention (SD5); concurrency/scheduler semantics |
| boundary rule | none beyond shared non-goals |
| risk | low — composition over proven units |
| integrable | yes |

### SD1-U6 — Contract closeout and truth pass

| Field | Value |
| --- | --- |
| outcome | Header comments in `src/cache.fab` and `src/model/dense.fab` state the rollback contract (branching + atomic commit, never naive trim or shared-cache mutation) and the out-of-scope physical ownership (allocation, residency, quantization, scheduling stay outside the value contract); the goal ledger rows are marked done with receipts; the campaign-facing references (rollback wording) are aligned; the closeout block below runs green. |
| write_scope | `docs/factory/kv-cache-branching/goal.md` (ledger + status); `src/cache.fab` (header comments only); `src/model/dense.fab` (header comments only) |
| done_when | `rg -n "trim|rollback|branch" src/ docs/` truth scan shows no live doc or error path promising physical handles or mutable shared trimming for the speculative path; audit clean; closeout block green (or honestly blocked-reported on foreign-gate reds, never weakened) |
| first-failing oracle | the truth scan finds the un-updated cache/dense headers today (they describe append/extend/reset only) |
| depends_on | SD1-U1..U5; **seat fence: a816aad1 cache.proba classification receipt before `cache.fab` edits** |
| sanity | `./scripta/check-source && ./scripta/check-compile` |
| non_goals | semantic edits to `cache.fab`/`dense.fab` (comments only); campaign CAMPAIGN.md edits (Mind owns routing artifacts) |
| boundary rule | comment-only hunks in the two live-adjacent files; any semantic drift found while editing headers is reported, not fixed here |
| risk | low |
| integrable | yes |

## 5. Implementation Work (Mind pointers)

Each Hand task is a pointer: goal path + unit id + write_scope + done_when
from §4. **Dispatch order:** U1 → U2 immediately (new files, no live-seat
overlap); U3 when SD0-U7 lands (or with Mind's live-shape ack per its boundary
rule); U4 → U5 serially after U3; U6 last, behind the a816aad1 receipt. U1's
`gradus.fab` comment line is the only shared-file touch in the whole graph.

## 6. Checkpoints And Gates

**Batching:** six Hands, no merge gate — every unit independently integrable
and green at its own commit. U1→U2→(U3)→U4→U5 is the serial spine; U6 closes.

**Lane-owned gates (named once, never copied onto child Hands):**

| Lane | Owns |
| --- | --- |
| lint | `./scripta/check-source` |
| test/compile | `./scripta/check-compile`; focused `faber test src/cache_branch.proba <filter>`; the goal's focused cache/dense rows must prove value isolation and all-layer atomicity — a single-layer append/trim test does not close any unit |
| merge | path-limited docs+source commits; `git diff --check` |
| factory audit | `python3 ../radix/scripta/audit-factory-goal-status.py --factory-root docs/factory --fail-on error` |

**Delivery closeout (SD1-U6 runs; all must be green or honestly blocked):**

```bash
python3 ../radix/scripta/audit-factory-goal-status.py --factory-root docs/factory --fail-on error
./scripta/check-source
./scripta/check-compile
faber test src/cache_branch.proba
git diff --check
```

(`faber` invocations use `FABER_LIBRARY_HOME`/`FABER_BIN` exactly as
`scripta/check-compile` sets them; the package-route loader defect seat
(ed794237) is in flight — file+filter runs only, never package-wide.) Foreign
gate reds are reported blocked on the handle, never weakened.

**Release posture**: not-applicable — no package/release train; the value
contract is library-internal until SD2+ consume it.

## 7. Open questions for Mind

1. **U3 dispatch without SD0-U7** (expfix/pkghang seats gate U6/U7 of SD0): default per the boundary rule — dispatch against the verified live `speculative.fab` shape with an explicit ack, or hold U3 (and the U4→U5 spine behind it) for the handoff. Mind's call; the handoff row is confirmation, not new information.
2. **Leaf name**: `gradus:cache_branch` (`src/cache_branch.fab`) — chosen to keep `cache.fab`/`cache.proba` (live seat surfaces) untouched and give SD2–SD5 one import point. Flag if the operator wants the family inside `cache.fab` instead.
3. **`n = 0` version rule**: pinned equivalent-base (no advance). If SD3's generation transaction later needs a distinguishable no-op commit receipt, that is an SD3-owned fact layered on top, not a version change here.
