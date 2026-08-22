# DELIVERY: cached-block-verification — k-row reference verification over an admitted prefix

**Status**: lowered 2026-08-22 — U1 (`6754440`) and U2 (`fad0d57`) landed; U3 in flight (task `94c72dfe`); U4→U5 serial spine; whole goal parallel-safe with every radix lane — gradus writes only
**Goal:** [`goal.md`](goal.md) (goal-check verdict: **READY** — record below)
**Campaign:** [`speculative-decode`](../speculative-decode/CAMPAIGN.md) stage SD2 (gate: nonempty prefix + nonempty candidate block → pinned `[k, V]` row convention and complete staged state; all rows and final state match full recompute; failure is atomic; reference evidence only)
**Repos:** primary `gradus/` (this repo); evidence-only `radix/`, `hosts/` (no writes)
**Dependencies satisfied:** SD0 [`speculative-decode-contract`](../../archived/speculative-decode-contract/goal.md) done 7/7; SD1 [`kv-cache-branching`](../../archived/kv-cache-branching/goal.md) done 6/6 (commit `1bb5ddb`). This goal's units consume both; they never redefine them.

---

## 0. Goal check (gate for this lowering)

**Verdict: READY.** Evaluator: planner. Consumer: delivery. Every goal source pin
re-verified against the live gradus tree 2026-08-22 (drift is line-number only);
both named dependencies are landed and archived done; all three goal open
questions pin against live code below. No architecture gap: the state carrier,
forward seam, and transaction primitive already exist — this goal composes them.

| Goal claim | Live check | Result |
| --- | --- | --- |
| Cache exposes sequential `append`, prefill `extend`, whole-cache `reset` only; no candidate-block transaction (`cache.fab:31-58, 387-475`) | `append` `:413`, `extend` `:451`, `reset` `:490`; grep finds no block/verify operation anywhere in `src/` | live |
| Cached decoder is one-token-per-call (`decode.fab:470-511`) | `decode_cached(token_id, position, m, layer)` `:511` → `DecodeStep {logits [V], state}` | live |
| Campaign needs one forward for `L + k` with `[k, V]` logits and all-layer state result | `dense.decode_step` `:500` enforces `position ≡ prefix_before` and admits exactly one token; `dense.prefill_cached` `:588` admits multi-row only from an empty prefix (campaign ground-truth row) | live — the nonempty-prefix k-row gap is real and unimplemented |
| Lower primitives can carry several rows (campaign ground truth) | `dense.fab`'s per-layer `_block_cached(h, positions, cache, tokens, …)` takes positions/token **lists**; attention/cache multi-row verified by the campaign at `attention.fab:1071-1111`, `cache.fab extend` | live — implementable without new math |
| SD1 dependency (branch/commit transaction) | `src/cache_branch.fab` landed (712 lines): `KVCheckpoint` `:115`, `construct_checkpoint` `:189`, `SpeculativeBranch`/`construct_branch` `:265/:464`, `AcceptanceDecision`/`construct_decision` `:324/:516`, `commit` `:592`, transaction seam `begin`/`inspect`/`abort`/`commit_transaction` (file tail); SD1 archived done `1bb5ddb` | satisfied — consume, do not re-own |
| SD0 dependency (acceptance oracle + provider seam) | `src/speculative.fab`: `GreedyAcceptance` + `first_divergence` `:150`; SD0 handoff `cached-block-verification (SD2)` row frozen | satisfied |
| OQ1 carrier shape | `KVCheckpoint` over `list<kv.KVCache>` is already the all-layer logical state and the dense route's currency | **pinned here**: `KVCheckpoint` is the state carrier; one new typed `BlockVerification` result wraps rows + acceptance + committed checkpoint; no second KV identity type |
| OQ2 numeric comparison | `dense.proba` uses the admitted reference epsilon `1e-5` f32 (e.g. `dense.proba:252`) | **pinned here**: row/state comparison within `1e-5`, first-divergence index recorded; never widened locally |
| OQ3 failure carrier | `cache_branch` values make "untouched" provable via `checkpoint_equal` | default holds: typed error + untouched input checkpoint; no partial state returned |

## 1. Interpreted theme

The cache can append one token or prefill from empty, and SD1 can branch and
commit atomically — but nothing can *evaluate* a candidate block: score k
candidate tokens against a nonempty admitted prefix in one forward, produce the
`[k, V]` target rows plus the per-layer candidate K/V rows, and commit only
through the SD1 transaction. SD2 is that reference operation: typed contract,
k-row forward, all-layer atomic staging, a full-recompute oracle that owns the
row-to-position convention, and one consumer seam for the speculative loop.
Reference evidence only — no device, residency, or performance claim.

## 2. Normalized spec

A new leaf `src/block_verify.fab` (module `gradus:block_verify`, one
map-comment line in `src/gradus.fab` — the SD0/SD1 leaf precedent) owns the
verification family: a typed block request over an admitted `KVCheckpoint`
(nonempty prefix `L`, nonempty candidate ids `k`, structural admission before
any evaluation); a k-row reference forward producing per-layer `[k, dim]`
candidate K/V rows and one `[k, V]` logits matrix with the pinned row
convention (row `i` = the target distribution used to accept/reject candidate
`i`, computed from the prefix plus candidates before `i`; candidate `i` writes
K/V at position `L + i`); staging and commit exclusively through the landed
`cache_branch` transaction (`begin` → `commit_transaction`), so every failure
path leaves the caller's checkpoint untouched; a full-recompute oracle (fresh
empty caches, scalar replay of prefix then candidates) that is the authority
for the row mapping; and one public verify seam returning the typed
`BlockVerification` (rows, `GreedyAcceptance` via `first_divergence`, committed
checkpoint). The k-row forward seam lives additively in `src/model/dense.fab`
(one public multi-row cached step mirroring `decode_step`'s walk) so the leaf
does not duplicate the weights walk — see OQ1.

Delivery-level non-goals (inherited from goal §Non-goals): no candidate policy,
lookup, or scheduling (SD4); no device/Metal/CUDA/residency/quantization; no
prefix pinning, cross-request reuse, paging, eviction; no sampler contact; no
new KV identity type or wire; no change to `generate_dense_with_stop`.

## 3. Repo-aware baseline

| Surface | Today | Note |
| --- | --- | --- |
| State carrier | `KVCheckpoint` over `list<kv.KVCache>` (`cache_branch.fab:115`); `checkpoint_equal` `:168` | U3's unchanged-on-failure predicate |
| Transaction | `begin(checkpoint, CandidateBlock)` → `BranchHandle`; `commit_transaction(current, handle, n)`; `abort` (`cache_branch.fab` tail) | the only staging/commit path — never a direct `extend` on shared layers |
| Cached walk | `dense.decode_step` `:500` (scalar, `position ≡ prefix_before`, per-layer `_block_cached` over positions/tokens lists); `prefill_cached` `:588` (multi-row, empty prefix only) | U2 mirrors the walk at `T = k`, positions `L..L+k-1`, nonempty prefix |
| Acceptance oracle | `speculative.GreedyAcceptance` / `first_divergence` (`speculative.fab:150`) | U5 wraps; never recomputes acceptance |
| Tolerance | `1e-5` f32 reference epsilon (`dense.proba:252` and siblings) | U4's comparison bound; first-divergence index recorded |
| Proba discipline | co-located `*.proba`; `faber test src/<file>.proba <filter>` on the MIR runner | Hand sanity is file + filter; package-wide runs stay banned pending the radix loader fix (`ed794237`) — verify at dispatch |
| Foreign fences | gradus tree clean 2026-08-22; prior live seats (`cache.proba` classification, B2 safetensors/sampling) have landed their receipts | `dense.fab` additive touch is unfenced today — re-check `git status` at dispatch |

## 4. Unit graph — Hand units

```text
SD2-U1 (typed block contract) ──> SD2-U2 (k-row forward seam) ──> SD2-U3 (atomic staging/commit)
                                                                        │
                                          SD2-U4 (full-recompute oracle) │  (U3 ∥ U4 logically; same file → land serially)
                                                                        │
                                          SD2-U5 (consumer verify seam) <─ U3, U4
```

Shared non-goals for every unit (goal §Non-goals + campaign invariants 5, 9):
no candidate/lookup policy, no device/Metal/CUDA/kernel/residency work, no
quantized KV, no sampling/RNG contact, no edits to `src/generation.fab`,
`src/cache.fab`, `src/cache_branch.fab`, or `src/speculative.fab` (landed
authorities), no campaign or sibling-goal file edits (each unit's own proba
excepted), no throughput or device claims.

### SD2-U1 — typed block request/result contract

| Field | Value |
| --- | --- |
| outcome | `block_verify.fab` defines the typed contract: `BlockRequest` over an admitted `KVCheckpoint` plus candidate token ids, and the result carrier(s) with value equality. Structural admission rejects before anything evaluates: nonempty prefix (`L ≥ 1`), nonempty candidates (`k ≥ 1`), `k` within remaining capacity against the checkpoint's layer capacity, non-negative token ids, and result-constructor bounds. Every reject is typed (`VerifyError` vocabulary local to the leaf) and leaves inputs untouched (assert via `checkpoint_equal`). No forward, no model import. |
| write_scope | `src/block_verify.fab` (new); `src/block_verify.proba` (new); `src/gradus.fab` (one map-comment line) |
| done_when | proba rows prove: `L ≥ 1` / `k ≥ 1` enforced (empty-prefix and empty-candidate requests reject typed); `k` over remaining capacity rejects; negative token id rejects; each reject leaves the input checkpoint `checkpoint_equal` to before; result carriers round-trip value equality |
| first-failing oracle | the empty-prefix reject row cannot run today — no block contract exists (grep-clean verified) |
| depends_on | — |
| parallel | **yes** — new files only; disjoint from SD4-U1/U2 and every radix lane (gradus repo only). Only shared touch is the one `gradus.fab` comment line, also touched by SD4-U1 — land those two comment lines sequentially (trivial) |
| sanity | `faber test src/block_verify.proba contract` |
| non_goals | candidate evaluation (U2); staging/commit (U3); oracle (U4); any model/dense import |
| risk | low — additive leaf |
| integrable | yes |

### SD2-U2 — k-row reference forward and candidate K/V rows

| Field | Value |
| --- | --- |
| outcome | The reference forward for a nonempty admitted prefix: one additive public multi-row cached step in `dense.fab` (mirroring `decode_step`'s per-layer walk at `T = k`, positions `L..L+k-1`, attending to prefix + earlier candidate rows) plus the `block_verify.fab` wrapper producing per-layer `[k, dim]` f32 candidate K/V rows and one `[k, V]` logits matrix under the pinned row convention: row `i` is the target distribution used to accept/reject candidate `i`, computed from the prefix plus candidates before `i`; candidate `i` writes K/V at `L + i`. Model-relative admission (token ids within vocab, cache dimension/dtype match, finite values) rejects typed before any row exists. Device-neutral: imports carry no device/scheduler surface. |
| write_scope | `src/model/dense.fab` (one additive public step; no edits to `decode_step`/`prefill_cached` semantics); `src/model/dense.proba` (rows for the new step); `src/block_verify.fab`; `src/block_verify.proba` |
| done_when | proba rows prove: a fixture model + admitted multi-layer checkpoint (3+ layers) yields `k` logit rows of width `V` at positions `L..L+k-1` and per-layer `[k, dim]` K/V rows; vocab/dimension/dtype/non-finite rejects fire before any row exists; the row convention is recorded in fixtures (row `i` distribution follows prefix + candidates `< i`) — cross-checked against the oracle in U4 |
| first-failing oracle | the multi-row nonempty-prefix step fails today: `decode_step` rejects any `position ≠ prefix_before + 1` shape and `prefill_cached` rejects a nonempty prefix |
| depends_on | SD2-U1 |
| parallel | no — same leaf file as U1's spine; also the graph's only `dense.fab` touch (serialize behind a clean `git status` on that file) |
| sanity | `faber test src/block_verify.proba forward` |
| non_goals | acceptance decisions (U5); staging/commit (U3); oracle comparison (U4 — the row convention's authority); performance or batching claims |
| boundary rule | `dense.fab` hunk is additive-only; if the walk cannot be expressed over existing private helpers, stop and report rather than refactoring `decode_step` |
| risk | medium — the row-convention off-by-one is the care point; U4's oracle is the designed catch |
| integrable | yes |

### SD2-U3 — all-layer atomic staging and commit through the SD1 transaction

| Field | Value |
| --- | --- |
| outcome | `block_verify.fab` stages the U2 forward result per-layer into `cache_branch.CandidateBlock` and drives the landed transaction exclusively: `begin(checkpoint, block)` materializes the private branch; `commit_transaction(checkpoint, handle, n)` commits the first `n` candidate rows across **all layers together** (SD1's pinned version rule: `+1` exactly once on `n > 0`, `n = 0` equivalent base); `abort` discards. Every failure path — structural reject, forward reject, identity mismatch, stale checkpoint, out-of-range `n` — returns a typed error with the caller's checkpoint `checkpoint_equal` to the original. No direct `append`/`extend` on shared layers anywhere in the leaf. |
| write_scope | `src/block_verify.fab`; `src/block_verify.proba` |
| done_when | proba rows prove: success path commits all layers to `L + n` with history/version per SD1 rules; forced failure paths (bad `n`, identity mismatch, stale checkpoint) leave the input `checkpoint_equal` unchanged; a 3+ layer fixture shows no interleaved/partial layer state is constructible; `n = 0` returns the equivalent base |
| first-failing oracle | the unchanged-on-forward-reject row fails today (no staging path exists) |
| depends_on | SD2-U1, SD2-U2 |
| parallel | no — same leaf file (logical sibling of U4; whichever seat frees first lands first) |
| sanity | `faber test src/block_verify.proba atomic` |
| non_goals | choosing `n` (acceptance policy is U5 via `first_divergence`); generation state staging (SD4); any second commit authority |
| risk | medium — the atomicity heart; mitigated by composing the proven SD1 transaction rather than new mutation paths |
| integrable | yes |

### SD2-U4 — full-recompute oracle and equivalence

| Field | Value |
| --- | --- |
| outcome | `block_verify.fab` adds the full-recompute oracle and the equivalence check: from fresh empty caches, scalar-replay the same prefix then the candidate block one token at a time through the same cached seam, collecting the target rows at positions `L..L+k-1` and the final per-layer states. The comparison checks every `[k, V]` row, the position mapping, the token history, and every layer's final staged tensors within the admitted `1e-5` reference epsilon, recording the first divergence index; no tolerance is widened locally. The oracle is the authority for the U2 row convention. |
| write_scope | `src/block_verify.fab`; `src/block_verify.proba` |
| done_when | proba rows prove: block result ≡ oracle on a multi-layer fixture — all `k` rows within `1e-5`, final per-layer states and histories equal, positions `L..L+k-1` agree; a forced-perturbation fixture records the first divergence index honestly instead of passing; the comparison refuses to widen tolerance (a >`1e-5` delta surfaces as divergence) |
| first-failing oracle | the forced-divergence row fails today (no oracle exists to record it) |
| depends_on | SD2-U1, SD2-U2 |
| parallel | no — same leaf file as U3 (logical sibling; land serially) |
| sanity | `faber test src/block_verify.proba oracle` |
| non_goals | tolerance changes; comparing against device/compiled tiers (radix goals own that); performance measurement |
| risk | low-medium — mechanical replay; the value is being the independent authority for U2's convention |
| integrable | yes |

### SD2-U5 — consumer verify seam for the speculative loop

| Field | Value |
| --- | --- |
| outcome | `block_verify.fab` publishes one public verify operation composing U1–U4: request → structural admission → k-row forward → greedy acceptance via `speculative.first_divergence` over the target rows and candidates → `commit_transaction` for the accepted `n` → typed `BlockVerification { rows, acceptance, committed checkpoint }`. Every failure returns the typed error with state unchanged. A lifecycle fixture drives admitted-prefix + candidates through verify → accept → committed state end to end. No candidate policy, no provider, no generation loop, no device route — the seam SD4 (context-lookup) consumes. |
| write_scope | `src/block_verify.fab`; `src/block_verify.proba` |
| done_when | lifecycle proba rows: verify accepts `n < k` and `n = k` fixtures with committed state matching the oracle's prefix; a reject fixture leaves the checkpoint unchanged; module imports show no device/scheduler/policy surface (grep clean); acceptance equals `first_divergence` output (wrap, not recompute) |
| first-failing oracle | the end-to-end verify row fails today (no compose operation exists) |
| depends_on | SD2-U3, SD2-U4 |
| parallel | no — closes the spine |
| sanity | `faber test src/block_verify.proba verify` |
| non_goals | candidate production (SD4); generation integration (SD4-U3); receipts (SD4-U5); device execution (radix SD3) |
| risk | low — composition over proven units |
| integrable | yes |

## 5. Implementation Work (Mind pointers)

Each Hand task is a pointer: goal path + unit id + write_scope + done_when from
§4. **Dispatch order:** U1 immediately (new files, no live-seat overlap; land
the `gradus.fab` comment line before or after SD4-U1's, not concurrently);
U2 next (the only `dense.fab` touch — verify that file clean at dispatch);
U3/U4 as serial siblings in either order; U5 last. The whole goal runs in
parallel with any radix lane and with SD4-U1/U2 — no shared write surface.

## 6. Checkpoints and gates

**Batching:** five Hands, no merge gate — every unit is independently
integrable and green at its own commit. U1→U2→(U3,U4 serial)→U5 is the spine.

**Lane-owned gates (named once, never copied onto child Hands):**

| Lane | Owns |
| --- | --- |
| lint | `./scripta/check-source` |
| test/compile | `./scripta/check-compile`; focused `faber test src/block_verify.proba <filter>` (file + filter only; package-wide runs banned pending the radix loader fix) — the goal's rows must prove the `[k, V]` convention and all-layer atomicity, not single-row appends |
| merge | path-limited source+docs commits; `git diff --check` |
| factory audit | `python3 ../radix/scripta/audit-factory-goal-status.py --factory-root docs/factory --fail-on error` |

**Delivery closeout (final unit runs; all green or honestly blocked-reported):**

```bash
python3 ../radix/scripta/audit-factory-goal-status.py --factory-root docs/factory --fail-on error
./scripta/check-source
./scripta/check-compile
faber test src/block_verify.proba
git diff --check
```

**Release posture:** not-applicable — reference library contract; the radix
device goals consume this seam later.

## 7. Open questions for Mind

1. **Forward seam placement (default: additive `dense.fab` step).** U2 adds one public multi-row cached step to `src/model/dense.fab` rather than duplicating the weights walk inside the leaf. If the operator prefers leaf purity over seam reuse, U2 rewrites to a `block_verify.fab`-local walk — flag before dispatch; done_when is unchanged.
2. **Leaf name.** Default `gradus:block_verify` (`src/block_verify.fab`), following `cache_branch`/`speculative`/`receipt` precedent. Flag to rename.
3. **Oracle replay primitive.** Default: scalar replay through the same cached seam (k=1 positions per step). If implementation finds a cheaper exact oracle over `dense.forward`, that is acceptable only if U4's done_when rows are unchanged.
