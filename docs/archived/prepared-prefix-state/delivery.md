# DELIVERY: prepared-prefix-state — units U1–U5 (identity, state, attach, continuation, truth pass)

**Status**: re-lowered 2026-08-23 (task `fc36232c`) — full unit graph `PP-U1`…`PP-U5` including the previously-punted U1/U2; goal re-checked against live code the same day (§0). **Dense spine (`PP-U1 → PP-U2 → PP-U3a → PP-U3b → PP-U4a → PP-U5`) is dispatch-ready now**; hybrid `PP-U4b` is blocked on unlanded MODEL-03/MODEL-04 receipts (MODEL-01 landed, MODEL-02 done, LIB-02 landed — no longer blocking).
**Goal:** [`goal.md`](goal.md)
**Campaign:** [`speculative-decode`](../speculative-decode/CAMPAIGN.md) — **numbering disambiguation: board SD4 = this goal (`prepared-prefix-state`); campaign SD4 = `context-lookup-drafting`** (this goal is campaign **SD5**). The campaign status line's "SD4 U1/U2 landed" refers to `context-lookup-drafting` under campaign numbering — it is not evidence that this goal's U1/U2 landed (see §0). Unit ids here use the goal's own U-numbering, prefixed `PP-`, so they cannot collide with the already-used `SD2-*`/`SD4-*` ids.
**Repos:** primary `gradus/` (this repo); evidence-only `inferentia/` (no writes)
**Mandatory dependency:** SD1 [`kv-cache-branching`](../../archived/kv-cache-branching/goal.md) done 6/6 (commit `1bb5ddb`); this goal consumes its immutable/transactional state, never re-owns it.

---

## 0. Goal check (gate for this lowering)

**Verdict: READY (dense spine).** Evaluator: planner. Consumer: delivery.
Re-verified against live git and source 2026-08-23 (gradus HEAD `65ffa49`,
tree clean). The 2026-08-22 `NOT READY` verdict's two blocking gaps are
resolved by this lowering: (1) U1/U2 were never landed — they are now lowered
here as `PP-U1`/`PP-U2` (no prepared-state code exists on main today either —
grep over `src/` for `PreparedState|prepared_state|PreparedIdentity|CanonicalIdentity`
returns zero matches; the goal ledger is still all-pending); (2) hybrid
`PP-U4b` remains gated on unlanded MODEL-03/MODEL-04 receipts — held, not
weakened.

| Claim | Live check (2026-08-23) | Result |
| --- | --- | --- |
| Goal status line | `**Status**: planned — pre-implementation` + goal-checked note | goal-checked this pass; ledger still all-pending — correct |
| U1 precedent (existing cache identity) | `cache.fab:505` `CacheIdentity` (model/model_version/config/tokenizer/history/position/layers/dtype/layout); `cache_identity` `:571`; field-wise `cache_identity_equal` `:555`; wire `cache/identity/1.0.0` (`serialize_identity` `:589`, `deserialize_identity` `:598`) | live — U1 builds the canonical prepared identity on top |
| U2 typed-state precedent | no complete prepared-state type exists; `KVStructure` `cache.fab:1253` is a descriptor (not payload), `list<kv.KVCache>` + `KVCheckpoint` (`cache_branch.fab`) carry dense KV only | U2's complete-state value is **not landed** — lowered here as PP-U2 |
| Tokenizer identity component | `tokenizer.fab` `TokenizerIdentity` schema `1.0.0`, record at `:296` region, fail-closed construct | live — U1/U3's tokenizer binding source |
| Dense nonempty-prefix seam | `dense.decode_block` `dense.fab:589` (multi-row, nonempty prefix) landed `fad0d57`; `prefill_cached` `:681` (guard `:695`) still empty-prefix-only; `decode_step` `:500` still requires `position ≡ prefix_before` | suffix execution seam landed; suffix-only continuation **from a prepared state** is still new (PP-U4a) |
| Generation discards updated state | `generate_dense_with_stop` `generation.fab:1100` returns `list<int>`; `_dense_one`/`_dense_prefill` wrap `decode_step`/`prefill_cached` and the updated `layers` are threaded internally, not returned as prepared state | live — the goal's problem statement still holds |
| Hybrid state (U4b) | `qwen35moe.fab` freezes SSM/nextn **metadata only** (`Qwen35moeConfig`; no executed recurrent/conv state anywhere in `src/model/`); MODEL-03 delivery still dispatch-gated; MODEL-04 lowered, unlanded | **blocked** on MODEL-03 + MODEL-04 |
| PML receipts | MODEL-01 unit chain M1–M9 landed on main (`0c28ca3`…`7004ed8`; the M1 doc's own status line is stale); MODEL-02 **done 2026-08-22** (M2-G1 receipt, commit `8febe40`); LIB-02 tokenizer landed (wind-down `7eb389f`); MODEL-03 `pml5-gguf-m3-ssm-attention-state-delivery.md` unlanded; MODEL-04 unlanded | U4b blockers narrowed to MODEL-03 + MODEL-04 |
| MD4D placement authority | `radix/docs/factory/gpu-inference-multi-device/CAMPAIGN.md` §MD4D ("Tiered KV service and shared-prefix reuse"; shared-prefix reuse explicitly waits for MD4D) | live — the goal's no-device/no-tier non-goal has a real named owner |

**Non-blocking correction applied to `goal.md` this pass:** the draft's
"current dense path cannot continue prefill from a non-empty prefix …
`dense.fab:562-647` requires `prefix_before` to be zero" conflated
`prefill_cached` (still zero-prefix, now at `:681`/`:695`) with the landed
`decode_block` seam (`:589`, `fad0d57`); the Problem section and the
`generation.fab`/`cache.fab` line cites were refreshed to live symbols.

## 1. Interpreted theme

`CacheIdentity` names a prefix and `KVCheckpoint` snapshots dense KV, but
nothing can **reuse** that snapshot for a new request: there is no canonical
prepared identity, no typed prepared-state payload, and no attach operation
that picks the longest authorized prefix and hands back an independent
continuation state. U1–U5 build and finish that contract — canonical
identity, typed prepared payload, attach/admission, exact-prefix continuation
for dense (now) and hybrid (blocked on MODEL-03/04), and the truth pass that
proves the surface owns no registry, auth, or device handles.

## 2. Normalized spec

A new leaf `src/prepared_state.fab` (module `gradus:prepared_state`, one
map-comment line in `src/gradus.fab` — the `cache_branch`/`speculative`/
`receipt` precedent) owns the whole contract family: U1's canonical prepared
identity, U2's typed prepared state, and the attach/continue operations.
Attach is a pure
value operation: admit only candidates whose canonical identity and payload
binding match, select the longest exact prefix, return an independent
continuation state plus consumed length, and leave the candidate snapshot
unchanged. Continuation (U4a/U4b) feeds the returned state into the execution
surface and exposes the complete **next** prepared state. No global registry,
retention, authorization decision, tenant choice, or device handle appears in
the leaf.

Delivery-level non-goals (goal §Non-goals): no Inferentia registry/auth/TTL;
no request routing/scheduling; no device handles/placement/tiers (MD4D owns);
no kernels/quantized-KV/perf claims; no tokenizer implementation/model
admission/MoE routing/drafter; no multi-token verification policy.

## 3. Repo-aware baseline

| Surface | Today (2026-08-23, HEAD `65ffa49`) | Note |
| --- | --- | --- |
| Identity precedent | `CacheIdentity` (`cache.fab:505`) + `cache_identity_equal` (`:555`) + `cache/identity/1.0.0` wire (`:589-632`) | PP-U1 extends to canonical prepared identity; PP-U3 consumes field-wise equality |
| Typed state | `list<kv.KVCache>` / `KVCheckpoint` (`cache_branch.fab`) dense-only; `KVStructure` (`cache.fab:1253`) descriptor-only | PP-U2 adds recurrent/SSM/convolution payload + binding |
| Dense continuation seam | `dense.decode_block` (`dense.fab:589`, multi-row nonempty prefix, landed `fad0d57`); `prefill_cached` `:681` empty-prefix-only | PP-U4a's suffix prefill building block |
| Generation surface | `generate_dense_with_stop` (`generation.fab:1100`) returns `list<int>` only; `generation.fab` last touched by `85d2e37` (context-lookup loop integration, SD4 board) | PP-U4a must expose updated prepared state without forking a second public entry (see OQ) |
| Tokenizer binding | `TokenizerIdentity` (`tokenizer.fab:296` region, fail-closed, schema `1.0.0`) | PP-U1's tokenizer component |
| Hybrid state | none executed (`qwen35moe.fab` = `Qwen35moeConfig` metadata freeze) | PP-U4b blocked on MODEL-03/04 (MODEL-01 landed, MODEL-02 done `8febe40`, LIB-02 landed) |
| Proba discipline | co-located `*.proba`; `faber test src/<file>.proba <filter>` | Hand sanity = file + filter; package-wide runs banned pending radix loader fix (`ac7efdda2`) — verify at dispatch |
| Foreign fences | gradus tree clean 2026-08-23 (HEAD `65ffa49`) | re-check `git status` at dispatch |

## 4. Unit graph — Hand units

```text
PP-U1 (canonical identity) ──> PP-U2 (typed state + binding) ──> PP-U3a (admission) ──> PP-U3b (attach/continue)
                                                                                              │
                                                                                  v
                                                                           PP-U4a (dense, now)
                                                                                  │
                                                                                  v
                                                                           PP-U4b (hybrid, BLOCKED on MODEL-03/04)
                                                                                  │
                                                                                  v
                                                                           PP-U5 (truth pass)
```

Shared non-goals for every unit (goal §Non-goals + campaign invariants 5, 7, 9):
no registry/retention/auth/tenant, no device handles/placement, no
kernels/quantization/perf claims, no tokenizer/model/MoE implementation, no
multi-token verification policy, no edits to landed authorities
(`cache_branch.fab`, `speculative.fab`, `cache.fab` identity mutation paths),
no campaign or sibling-goal file edits (each unit's own proba excepted).

### PP-U1 — canonical prepared identity (content/model/config/tokenizer/position)

| Field | Value |
| --- | --- |
| outcome | `src/prepared_state.fab` defines the canonical prepared identity: a versioned typed record binding content (exact canonical token prefix + length; an opaque host/provider-supplied lookup digest is carried as passthrough input, never computed by gradus and never equality-authoritative — a differing-token/same-digest pair is unequal), model/capsule identity, the state-producing execution config (sampling-only fields excluded), tokenizer identity (consumed from `tokenizer.fab` `TokenizerIdentity`), and position (exact consumed range, next position). Field-wise equality; a versioned fail-closed wire round-trips exactly (schema `prepared-state/identity/1.0.0`; empty-prefix sentinel documented). Registered in the module map (one `src/gradus.fab` line). Extends the `CacheIdentity` precedent (`cache.fab:505-632`) without editing it. |
| write_scope | `src/prepared_state.fab` (new); `src/prepared_state.proba` (new); `src/gradus.fab` (one map-comment line) |
| done_when | proba rows prove: field-wise equality holds per component and rejects per-component on mismatch; wire round-trips exactly (identity → wire → identity equal); malformed wire rejects typed fail-closed; the digest passthrough is never equality-authoritative (same digest, different tokens → unequal); no model/dense/generation import in the leaf |
| first-failing oracle | the identity rows cannot run today — no prepared-state module exists (grep-clean verified 2026-08-23) |
| depends_on | none (extends landed `CacheIdentity` `cache.fab:505-632`; `TokenizerIdentity` `tokenizer.fab:296` region) |
| parallel | yes relative to radix lanes and the whole gradus tree except PP-U2 (same leaf) |
| sanity | `faber test src/prepared_state.proba identity` |
| non_goals | typed state payload and binding (PP-U2); attach/selection (PP-U3); cryptographic digest computation; any model import |
| risk | low — additive leaf over landed identity precedents |
| integrable | yes |

### PP-U2 — typed prepared state (KV + architecture-declared state families) and payload binding

| Field | Value |
| --- | --- |
| outcome | `src/prepared_state.fab` adds the complete typed prepared-state value: dense KV state (`list<kv.KVCache>` / `KVCheckpoint` family) plus architecture-declared slots for recurrent/SSM/convolution state families (declared now; hybrid payloads populate when MODEL-03 state lands — the dense payload is fully constructible today). Reset semantics mirror `KVCache.reset` (state cleared, identity/capacity retained, generation advanced); copy semantics give value independence; a payload binding covers canonical identity plus payload shape/content, and a mismatch rejects typed before any attach. No device handle, registry, or hidden global state. |
| write_scope | `src/prepared_state.fab`; `src/prepared_state.proba` |
| done_when | proba rows prove: construction of a dense payload; reset clears state and retains identity/binding facts; mutating a copy leaves the original equal (value independence); payload-binding mismatch (identity or shape/content) rejects typed; grep shows no device-handle/registry field |
| first-failing oracle | the state rows cannot run today — no prepared-state type exists |
| depends_on | PP-U1 (same leaf) |
| parallel | no — same leaf as PP-U1 |
| sanity | `faber test src/prepared_state.proba state` |
| non_goals | attach/selection (PP-U3); continuation execution (PP-U4a/U4b); hybrid execution state (MODEL-03 owns the SSM/conv state math; this unit only declares the slot family) |
| risk | medium — slot-family declaration must not preempt MODEL-03's state design; on conflict, stop and report |
| integrable | yes |

### PP-U3a — attach admission: identity and payload-binding reject

| Field | Value |
| --- | --- |
| outcome | `prepared_state.fab` owns the attach admission. Before any continuation, reject every candidate whose canonical identity (content / model / model_version / config / tokenizer / position — consumed from PP-U1's prepared identity) or whose payload binding (identity + payload shape/content — consumed from PP-U2's typed prepared state) does not match the request. Every mismatch is a typed `PreparedStateError`; source snapshots are left unchanged. No model/dense/generation import in this unit. |
| write_scope | `src/prepared_state.fab` (new); `src/prepared_state.proba` (new); `src/gradus.fab` (one map-comment line) |
| done_when | proba rows prove: each identity component (model, model_version, config, tokenizer, position, content) rejects typed on mismatch; payload-binding mismatch rejects typed; all-matching candidates pass admission; every reject leaves input snapshots unchanged (assert via PP-U2's state equality); the leaf imports no model/dense/generation surface |
| first-failing oracle | the admission rows cannot run today — no prepared-state module exists (grep-clean verified 2026-08-23) |
| depends_on | PP-U1, PP-U2 |
| parallel | yes relative to radix lanes and to the whole gradus tree except U3b (same leaf) |
| sanity | `faber test src/prepared_state.proba admission` |
| non_goals | prefix selection (U3b); continuation execution (U4a/U4b); any model import |
| risk | low — additive leaf over (unlanded) U1/U2 types |
| integrable | yes |

### PP-U3b — longest-authorized-prefix selection, tie, independent continuation

| Field | Value |
| --- | --- |
| outcome | `prepared_state.fab` implements the attach continuation: among admitted candidates, find the longest exact prefix of the request's canonical token sequence; resolve equal-length candidates deterministically (default: lowest declared source order); return an independent continuation state plus the consumed prefix length. The candidate snapshot is immutable — mutating the returned state leaves the candidate `equal` (PP-U2 equality). No registry, retention, auth, or device surface appears. |
| write_scope | `src/prepared_state.fab`; `src/prepared_state.proba` |
| done_when | proba rows prove: longest exact prefix beats shorter ones; equal-length ties resolve deterministically (repeatable); the returned continuation state can be mutated without changing the candidate snapshot (assert equality); the consumed prefix length is correct; grep shows no registry/retention/auth/device-handle surface |
| first-failing oracle | the attach/continue rows fail today — no attach operation exists |
| depends_on | PP-U3a (same leaf) |
| parallel | no — same leaf as U3a |
| sanity | `faber test src/prepared_state.proba attach` |
| non_goals | dense/hybrid execution integration (U4a/U4b); device residency; candidate authorization policy (caller supplies the authorized set) |
| risk | medium — longest-prefix + tie determinism + immutability |
| integrable | yes |

### PP-U4a — dense continuation integration (suffix prefill + returned next state)

| Field | Value |
| --- | --- |
| outcome | Wire the PP-U3b continuation into the dense surface: given a prepared dense state plus suffix tokens, run only the suffix through the landed dense seam (`decode_block` / `prefill_cached` family) and expose the complete **next** prepared state (updated KV + canonical identity) through one decode/generation surface. Prove cold-vs-warm equivalence: cold prefill + continuation emits the same tokens and final state as a fresh cold run under identical config and seed. |
| write_scope | `src/prepared_state.fab` (continuation compose seam); `src/prepared_state.proba`; `src/model/dense.fab` + `src/model/dense.proba` **only if** the landed `decode_block` cannot serve suffix prefill directly (additive seam; otherwise untouched); `src/generation.fab` + `src/generation.proba` **only if** the "one decode/generation surface" requirement is met by extending the existing entry (see boundary rule) |
| done_when | dense fixture proves: warm continuation consumes only suffix tokens (not the full prefix); emitted tokens and final prepared state equal a fresh cold run; cold-vs-warm logits match within the admitted `1e-5` reference epsilon; the returned next prepared state round-trips identity + payload |
| first-failing oracle | the suffix-only + returned-state row fails today — `generate_dense_with_stop` returns tokens only and `prefill_cached` rejects a nonempty prefix |
| depends_on | PP-U2, PP-U3b (and landed `dense.decode_block` `fad0d57`) |
| parallel | no — spine; touches the prepared_state leaf and the generation/dense surface. Same-file dispatch partners (freshness 2026-08-23): `generation.fab` last touched by `85d2e37` (context-lookup loop integration) with SD4-U4 tests landed `456b858`; `dense.fab` last touched `fad0d57`; the dense.proba repair seat (task `81f2182c`) **landed** as `30ab749` — no longer a live fence. Verify `git status` clean on `dense.fab`/`generation.fab` at dispatch. |
| sanity | `faber test src/prepared_state.proba continue` |
| non_goals | hybrid/SSM/recurrent/convolution state (U4b); device/tier work; a second public generate entry |
| boundary rule | `generate_dense_with_stop` is campaign invariant 1's oracle — do not fork a fast path. If exposing the updated prepared state cannot be expressed additively (e.g. an added return or a sibling continuation entry), stop and report rather than changing the public generate signature. |
| risk | high — equivalence + the generation-surface return |
| integrable | yes |

### PP-U4b — hybrid continuation integration (BLOCKED)

| Field | Value |
| --- | --- |
| outcome | Continue from a prepared **hybrid** state: carry KV plus architecture-declared recurrent/convolution/SSM state across reset/replay/continue; suffix prefill from a prepared hybrid state; record the first divergence per layer and position. Consumes MODEL-03 incremental state and MODEL-04 full-model composition; MODEL-01/02 admission for the admitted MoE/SSM row. |
| write_scope | `src/prepared_state.fab`; `src/prepared_state.proba`; `src/model/qwen35moe.fab` + proba (or the MODEL-03/04 leaf surfaces); hybrid fixtures |
| done_when | hybrid fixture proves KV + recurrent/convolution state carried, reset, replayed, and continued without conflation; first divergence recorded per layer/position; cold-vs-warm token/state equality on the admitted hybrid row |
| first-failing oracle | the hybrid continuation rows fail today — no executed hybrid state exists (grep + `qwen35moe.fab` metadata-only) |
| depends_on | PP-U2, PP-U3b, **PP-U4a (same `prepared_state` leaf — serialized, not parallel)**; **MODEL-03 SSM/attention state ([`pml5-gguf-m3-ssm-attention-state-delivery`](../production-ml-library/pml5-gguf-m3-ssm-attention-state-delivery.md)) and MODEL-04 full-model composition — both unlanded (2026-08-23)**; MODEL-01 admission landed, MODEL-02 done (`8febe40`), LIB-02 tokenizer landed — **no longer blocking** |
| parallel | no — same `prepared_state.fab`/`prepared_state.proba` write surface as PP-U4a (audit `ceb0158d` finding 1); parallel only to radix lanes |
| sanity | `faber test src/prepared_state.proba hybrid` |
| non_goals | dense continuation (U4a); model admission/MoE routing (PML owns); kernels/quantization |
| risk | high — blocked on MODEL-03 + MODEL-04 (unlanded; audit `ceb0158d` finding 2 — MODEL-01/02 and LIB-02 no longer block) |
| integrable | yes (once landed) |

### PP-U5 — contract truth pass

| Field | Value |
| --- | --- |
| outcome | Diagnostics, `docs/api-reference.md`, module map, reject rows, and regression fixtures document no-retention/no-auth/no-device ownership; public surface and source agree; malformed or incompatible prepared payloads fail closed. An `rg` audit removes stale KV-only/reuse claims; the API reference identifies MD4D as owner of multi-device tiers/routing and Inferentia as the product consumer. |
| write_scope | `gradus/docs/api-reference.md`; the module-map doc; `src/prepared_state.proba` (regression/reject rows); this goal's `goal.md` ledger/status (bookkeeping only) |
| done_when | `faber check .` green; `rg` audit clean for stale KV-only/reuse claims; malformed-wire and incompatible-payload rows fail closed (typed); api-reference names MD4D + Inferentia |
| first-failing oracle | the malformed-payload fail-closed rows fail today (no prepared payload type exists) |
| depends_on | PP-U4a (dense truth now); PP-U4b (hybrid truth, blocked) — closes after both |
| parallel | no — final pass |
| sanity | `faber test src/prepared_state.proba truth` |
| non_goals | new product surface; re-auditing landed authorities beyond the rg claim scan |
| risk | low — documentation + regression fixtures |
| integrable | yes |

## 5. Implementation Work (Mind pointers)

Each Hand task is a pointer: goal path + unit id + write_scope + done_when
from §4. Dispatch order: `PP-U1 → PP-U2 → PP-U3a → PP-U3b → PP-U4a → PP-U4b
(once hybrid deps land) → PP-U5`. The full spine `U1→U2→U3a→U3b→U4a→U4b→U5`
is serial: one `prepared_state` leaf plus one integration point; U4a and U4b
share that leaf, so they never run in parallel (audit `ceb0158d` finding 1).

## 6. Checkpoints and gates

**Batching:** seven rows, no merge gate — each integrable unit lands green at
its own commit. `PP-U1→PP-U2→PP-U3a→PP-U3b→PP-U4a→PP-U4b→PP-U5` serial
spine; `PP-U4b` held until MODEL-03/04 receipts land and PP-U4a closes.

**Lane-owned gates (named once, never copied onto child Hands):**

| Lane | Owns |
| --- | --- |
| lint | `./scripta/check-source` |
| test/compile | `./scripta/check-compile`; focused `faber test src/prepared_state.proba <filter>` (file + filter only; package-wide runs banned pending radix loader fix) |
| merge | path-limited source+docs commits; `git diff --check` |
| factory audit | `python3 ../radix/scripta/audit-factory-goal-status.py --factory-root docs/factory --fail-on error` |

**Delivery closeout (final unit runs; all green or honestly blocked-reported):**

```bash
python3 ../radix/scripta/audit-factory-goal-status.py --factory-root docs/factory --fail-on error
./scripta/check-source
./scripta/check-compile
faber test src/prepared_state.proba
git diff --check
```

**Release posture:** not-applicable — reference library contract; the radix
device goals and Inferentia consumer produce their own tiered receipts later.

## 7. Open questions for Mind

1. **U1/U2 lowered here (resolved this pass).** The 2026-08-22 task body's
   premise was false (cited `7125e596` invalid; `d1898cf` is the
   context-lookup provider). This re-lowering adds `PP-U1`/`PP-U2` as full
   units, so the dense spine is dispatchable with no unmet prerequisite.
   Confirm dispatch of `PP-U1` first.
2. **Hybrid `PP-U4b` holds.** MODEL-03 (SSM/attention state) and MODEL-04
   (full-model composition) are unlanded as of 2026-08-23; MODEL-01 landed,
   MODEL-02 done (`8febe40`), LIB-02 landed. When MODEL-03's state design
   lands, re-check PP-U2's declared slot families against it before U4b
   dispatch (stop-and-report clause already on PP-U2).
3. ~~Leaf name / U1-U2 home~~ **settled this pass:** everything lands in the
   `gradus:prepared_state` leaf (`src/prepared_state.fab`); `cache.fab` is
   read-only precedent (landed authority, not edited).
4. **"One decode/generation surface" (PP-U4a).** `generate_dense_with_stop`
   returns tokens only. Default: an additive continuation entry in the
   prepared_state leaf returns the next prepared state; the public generate
   signature is unchanged. If the operator requires the state on the existing
   generate return, that is a goal amendment, not a delivery choice.
