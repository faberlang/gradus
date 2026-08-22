# DELIVERY: prepared-prefix-state — remaining units U3–U5 (attach, continuation, truth pass)

**Status**: lowered 2026-08-22 — delivery rows produced for the goal's remaining units, **but not dispatchable**: the task premise "U1/U2 landed" is false against the live tree (see §0). Dense spine (`U3a→U3b→U4a→U5`) is dispatch-ready only after U1/U2 land; hybrid `U4b` is additionally blocked on unlanded PML receipts.
**Goal:** [`goal.md`](goal.md)
**Campaign:** [`speculative-decode`](../speculative-decode/CAMPAIGN.md) — the board labels this goal **SD4**; the campaign path numbers it **SD5** (campaign SD4 = `context-lookup-drafting`). Unit ids here use the goal's own U-numbering, prefixed `PP-`, so they cannot collide with the already-used `SD2-*`/`SD4-*` ids.
**Repos:** primary `gradus/` (this repo); evidence-only `inferentia/` (no writes)
**Mandatory dependency:** SD1 [`kv-cache-branching`](../../archived/kv-cache-branching/goal.md) done 6/6 (commit `1bb5ddb`); this goal consumes its immutable/transactional state, never re-owns it.

---

## 0. Goal check (gate for this lowering)

**Verdict: NOT READY.** Evaluator: planner. Consumer: delivery. Two blocking
gaps and one factual correction on the task body, all verified against live
git and source 2026-08-22.

| Claim | Live check | Result |
| --- | --- | --- |
| **Task: "U1 (7125e596) and U2 (d1898cf) landed"** | `git cat-file -t 7125e596` → `fatal: Not a valid object name`; `d1898cf` = `feat(context_lookup): implement deterministic provider` (SD3 `context-lookup-drafting` U2). No commit anywhere matches `prepared` / `prefix-state`; grep for `PreparedState|prepared_state|PreparedIdentity|CanonicalIdentity` over `src/` returns **zero** matches; the goal ledger is still all-pending. | **FALSE — U1 and U2 have not landed.** The cited hashes belong to the sibling `context-lookup-drafting` goal. This is a blocking gap, not a typo. |
| Goal status line | `**Status**: planned — pre-implementation` | not yet goal-checked; no delivery existed before this file |
| U1 precedent (existing cache identity) | `cache.fab:505` `CacheIdentity` (model/model_version/config/tokenizer/history/position/layers/dtype/layout); `cache_identity` `:571`; field-wise `cache_identity_equal` `:541`; wire `cache/identity/1.0.0` `:605` | live — U1's "existing cache identity" precedent is real; U1 still must build the **canonical prepared identity** on top of it |
| U2 typed-state precedent | no complete prepared-state type exists; `KVStructure` `cache.fab:1253` is a descriptor (not payload), `list<kv.KVCache>` + `KVCheckpoint` (`cache_branch.fab`) carry dense KV only | U2's "complete KV + recurrent/SSM/convolution state" value is **not** landed |
| Tokenizer identity component | `tokenizer.fab` `TokenizerIdentity` schema `1.0.0`, fail-closed `construct` `:493` | live — U3's tokenizer binding source |
| Dense nonempty-prefix gap | `dense.decode_block` `dense.fab:589` (multi-row, nonempty prefix) landed `fad0d57`; `prefill_cached` `:681` still empty-prefix-only; `decode_step` `:500` still requires `position ≡ prefix_before` | partially closed — suffix prefill has a landed multi-row seam, but "suffix-only from a prepared prefix" is still new |
| Generation discards updated state | `generate_dense_with_stop` `generation.fab:924` returns `list<int>`; `_dense_one`/`_dense_prefill` wrap `decode_step`/`prefill_cached` and the updated `layers` are threaded internally, not returned as prepared state | live — the goal's problem statement still holds |
| Hybrid state (U4b) | `qwen35moe.fab` freezes SSM/nextn **metadata only**; MODEL-03 delivery status "dispatch waits on predecessor receipts"; MODEL-01/02/04 "READY/dispatch-gated on predecessors" | **blocked** — no recurrent/convolution/SSM execution state exists |

**Blocking gaps (for `NOT READY`):**
1. **U1/U2 are not landed.** The task body's premise is false. U3–U5 consume
   U1 (canonical prepared identity) and U2 (typed prepared state) — neither
   exists. Nothing in this graph can dispatch until those two land, or the
   task is amended to also lower U1/U2.
2. **Hybrid `U4b` is gated on unlanded PML receipts.** MODEL-01 (GGUF-M1
   qwen35moe admission), MODEL-02 (MoE router/expert), MODEL-03 (SSM/attention
   state), MODEL-04 (full-model composition) are all "lowered/READY,
   dispatch-gated on predecessors" — none landed. Only the **dense** spine
   (U3a→U3b→U4a→U5-dense) is implementable now once U1/U2 land.

The rows below are still produced in full (the task asked for them) so Mind
can dispatch the dense spine the moment U1/U2 land and hold `U4b` until its
receipts. No unit is weakened to hide the gap.

## 1. Interpreted theme

`CacheIdentity` names a prefix and `KVCheckpoint` snapshots dense KV, but
nothing can **reuse** that snapshot for a new request: there is no canonical
prepared identity, no typed prepared-state payload, and no attach operation
that picks the longest authorized prefix and hands back an independent
continuation state. U3–U5 finish that contract — attach/admission, exact-prefix
continuation for dense (now) and hybrid (blocked), and the truth pass that
proves the surface owns no registry, auth, or device handles.

## 2. Normalized spec

A new leaf `src/prepared_state.fab` (module `gradus:prepared_state`, one
map-comment line in `src/gradus.fab` — the `cache_branch`/`speculative`/
`receipt` precedent) owns the attach/continue family, consuming U1's prepared
identity and U2's typed prepared state wherever they land. Attach is a pure
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

| Surface | Today | Note |
| --- | --- | --- |
| Identity precedent | `CacheIdentity` (`cache.fab:505`) + `cache_identity_equal` (`:541`) + `cache/identity/1.0.0` wire (`:605`) | U1 extends to canonical prepared identity; U3 consumes field-wise equality |
| Typed state | `list<kv.KVCache>` / `KVCheckpoint` (`cache_branch.fab`) dense-only; `KVStructure` (`cache.fab:1253`) descriptor-only | U2 adds recurrent/SSM/convolution payload + binding |
| Dense continuation seam | `dense.decode_block` (`dense.fab:589`, multi-row nonempty prefix, landed `fad0d57`); `prefill_cached` `:681` empty-prefix-only | U4a's suffix prefill building block |
| Generation surface | `generate_dense_with_stop` (`generation.fab:924`) returns `list<int>` only | U4a must expose updated prepared state without forking a second public entry (see OQ) |
| Tokenizer binding | `TokenizerIdentity` (`tokenizer.fab:493`, fail-closed, schema `1.0.0`) | U3's tokenizer component |
| Hybrid state | none executed (`qwen35moe.fab` = metadata freeze) | U4b blocked on MODEL-01..04 |
| Proba discipline | co-located `*.proba`; `faber test src/<file>.proba <filter>` | Hand sanity = file + filter; package-wide runs banned pending radix loader fix (`ed794237`) — verify at dispatch |
| Foreign fences | gradus tree clean 2026-08-22 (HEAD `fad0d57`) | re-check `git status` at dispatch |

## 4. Unit graph — Hand units

```text
(U1, U2 — NOT landed, prerequisite) ──> PP-U3a (admission) ──> PP-U3b (attach/continue)
                                                                      │
                                                          ┌───────────┴───────────┐
                                                          v                       v
                                                   PP-U4a (dense, now)    PP-U4b (hybrid, BLOCKED on MODEL-01..04)
                                                          │                       │
                                                          └───────────┬───────────┘
                                                                      v
                                                                   PP-U5 (truth pass)
```

Shared non-goals for every unit (goal §Non-goals + campaign invariants 5, 7, 9):
no registry/retention/auth/tenant, no device handles/placement, no
kernels/quantization/perf claims, no tokenizer/model/MoE implementation, no
multi-token verification policy, no edits to landed authorities
(`cache_branch.fab`, `speculative.fab`, `cache.fab` identity mutation paths),
no campaign or sibling-goal file edits (each unit's own proba excepted).

### PP-U3a — attach admission: identity and payload-binding reject

| Field | Value |
| --- | --- |
| outcome | `prepared_state.fab` owns the attach admission. Before any continuation, reject every candidate whose canonical identity (content / model / model_version / config / tokenizer / position — consumed from U1's prepared identity) or whose payload binding (identity + payload shape/content — consumed from U2's typed prepared state) does not match the request. Every mismatch is a typed `PreparedStateError`; source snapshots are left unchanged. No model/dense/generation import in this unit. |
| write_scope | `src/prepared_state.fab` (new); `src/prepared_state.proba` (new); `src/gradus.fab` (one map-comment line) |
| done_when | proba rows prove: each identity component (model, model_version, config, tokenizer, position, content) rejects typed on mismatch; payload-binding mismatch rejects typed; all-matching candidates pass admission; every reject leaves input snapshots unchanged (assert via U2's state equality); the leaf imports no model/dense/generation surface |
| first-failing oracle | the admission rows cannot run today — no prepared-state module exists (grep-clean verified) |
| depends_on | **U1, U2 (goal contract — NOT landed; blocking)** |
| parallel | yes relative to radix lanes and to the whole gradus tree except U3b (same leaf) |
| sanity | `faber test src/prepared_state.proba admission` |
| non_goals | prefix selection (U3b); continuation execution (U4a/U4b); any model import |
| risk | low — additive leaf over (unlanded) U1/U2 types |
| integrable | yes |

### PP-U3b — longest-authorized-prefix selection, tie, independent continuation

| Field | Value |
| --- | --- |
| outcome | `prepared_state.fab` implements the attach continuation: among admitted candidates, find the longest exact prefix of the request's canonical token sequence; resolve equal-length candidates deterministically (default: lowest declared source order); return an independent continuation state plus the consumed prefix length. The candidate snapshot is immutable — mutating the returned state leaves the candidate `equal` (U2 equality). No registry, retention, auth, or device surface appears. |
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
| outcome | Wire the U3 continuation into the dense surface: given a prepared dense state plus suffix tokens, run only the suffix through the landed dense seam (`decode_block` / `prefill_cached` family) and expose the complete **next** prepared state (updated KV + canonical identity) through one decode/generation surface. Prove cold-vs-warm equivalence: cold prefill + continuation emits the same tokens and final state as a fresh cold run under identical config and seed. |
| write_scope | `src/prepared_state.fab` (continuation compose seam); `src/prepared_state.proba`; `src/model/dense.fab` + `src/model/dense.proba` **only if** the landed `decode_block` cannot serve suffix prefill directly (additive seam; otherwise untouched); `src/generation.fab` + `src/generation.proba` **only if** the "one decode/generation surface" requirement is met by extending the existing entry (see boundary rule) |
| done_when | dense fixture proves: warm continuation consumes only suffix tokens (not the full prefix); emitted tokens and final prepared state equal a fresh cold run; cold-vs-warm logits match within the admitted `1e-5` reference epsilon; the returned next prepared state round-trips identity + payload |
| first-failing oracle | the suffix-only + returned-state row fails today — `generate_dense_with_stop` returns tokens only and `prefill_cached` rejects a nonempty prefix |
| depends_on | U2, PP-U3b (and landed `dense.decode_block` `fad0d57`) |
| parallel | no — spine; touches the prepared_state leaf and the generation/dense surface |
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
| depends_on | U2, PP-U3b; **MODEL-01 (GGUF-M1) admission, MODEL-02 router/expert execution, MODEL-03 SSM/attention state, MODEL-04 full-model composition, LIB-02 tokenizer receipts — all unlanded** |
| parallel | yes relative to U4a (different write surface) once its dependencies land |
| sanity | `faber test src/prepared_state.proba hybrid` |
| non_goals | dense continuation (U4a); model admission/MoE routing (PML owns); kernels/quantization |
| risk | high — blocked on five external receipts |
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
from §4. **Nothing dispatches until U1/U2 land** (the task's premise is
false — see §0). After that: `PP-U3a → PP-U3b → (PP-U4a ∥ PP-U4b when hybrid
deps land) → PP-U5`. The dense spine `U3a→U3b→U4a→U5` is serial; the only
internal parallelism is `U4a ∥ U4b` (disjoint write surfaces), and `U4b` is
held until MODEL-01..04 + LIB-02 receipts.

## 6. Checkpoints and gates

**Batching:** five rows, no merge gate — each integrable unit lands green at
its own commit. `U3a→U3b→U4a→U5` dense spine; `U4b` held.

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

1. **U1/U2 are not landed (blocking).** The task body cites `7125e596`
   (invalid object) and `d1898cf` (`context_lookup` provider — SD3's U2). No
   prepared-identity or prepared-state code exists and the goal ledger is
   all-pending. Either land U1/U2 first (and I lower them, if you want), or
   amend this task. Until then, U3–U5 cannot dispatch.
2. **Hybrid `U4b` holds.** MODEL-01/02/03/04 are "lowered/READY,
   dispatch-gated on predecessors" and none landed; LIB-02 is executed. The
   goal's own dependency-state line already says this — the dense spine is the
   only immediately-implementable path.
3. **Leaf name / U1-U2 home.** Default `gradus:prepared_state`
   (`src/prepared_state.fab`) owns U3–U5; U1's identity and U2's typed state
   land either there or in `cache.fab` per U1's "or the owning state module".
   Where U1/U2 land changes U3a's `write_scope` (same leaf vs import-from-cache),
   not its `done_when`. Flag to fix.
4. **"One decode/generation surface" (U4a).** `generate_dense_with_stop` returns
   tokens only. Default: an additive continuation entry in the prepared_state
   leaf returns the next prepared state; the public generate signature is
   unchanged. If the operator requires the state on the existing generate
   return, that is a goal amendment, not a delivery choice.
