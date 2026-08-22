# GOAL: kv-cache-branching — immutable all-layer speculative branches with atomic prefix commit

**Status**: done — U1–U6 landed (U1 `63a8d73`; U2 `f8f4b43`; U3 `0530fee`; U4 `dd385c1`; U5 `5392885`; U6 receipt recorded in the ledger). The immutable checkpoint/private branch and atomic all-layer commit contract is closed out; physical allocation, residency, quantization, and scheduling remain outside the Gradus value contract.
**Created**: 2026-08-21
**Campaign:** `speculative-decode`
**Source:** speculative-decode campaign lowering and the 2026-08-21 live-code audit
**Repos:**
- primary: `gradus/` — `src/cache.fab`, `src/model/dense.fab`, `src/attention.fab`, `src/transformer.fab`, co-located `.proba`, and logical cache documentation
- evidence only (no writes): `inferentia/`, `radix/`, `hosts/`
**Related:**

| Artifact | Relationship |
| --- | --- |
| `../../archived/speculative-decode-contract/goal.md` | Consumes this branch/checkpoint contract for lossless dense verification and policy dispatch |
| `../../factory/cached-block-verification/goal.md` | Owns dense nonempty-prefix block evaluation over this transaction primitive |
| `../../factory/speculative-decode/CAMPAIGN.md` | Parent routing artifact; this goal lowers SD1 only |
| `../../factory/production-ml-library/CAMPAIGN.md` | Existing KV identity, dense cache, and generation ownership authority |

---

## Invariant

A speculative operation never mutates or invalidates its all-layer base
checkpoint. Candidate tokens are evaluated on a private logical branch. One
atomic commit returns the accepted prefix across every layer and discards the
unaccepted suffix; any failure leaves the base checkpoint unchanged. The
contract is device-neutral and contains no physical handles. It treats the
existing cache identity as an opaque equality fact and does not define the
canonical reusable prepared-state identity.

## Problem

`KVCache` currently supports one-token `append`, batched `extend`, and
whole-cache `reset` (`src/cache.fab:386-469`). There is no trim, rollback,
checkpoint, branch, or all-layer commit operation. `cache_equal` compares
individual values, but no API coordinates a consistent prefix across all
layers (`src/cache.fab:306-323`).

The dense route enforces a shared prefix for all layers and currently exposes
one-token cached continuation (`src/model/dense.fab:488-560`). Its batched
prefill path only accepts an empty prefix (`src/model/dense.fab:563-648`), so
verification against a nonempty generation prefix cannot safely append a
candidate block and then retain only its accepted prefix. A naive in-place
trim of one shared cache would also make rejected rows observable to another
consumer and could leave layers at different lengths.

Cache identity records exact prefix metadata (`src/cache.fab:471-555`), but it
does not establish branch ownership, payload binding, or snapshot lifetime.
The new primitive must be a value-level logical contract: no device pointers,
residency handles, aliasing promises, or scheduler ownership.

## Proposal

1. Add an immutable `KVCheckpoint` value for an ordered set of dense layer
   caches. It records the all-layer prefix length, the existing opaque
   `CacheIdentity` equality value, cache generation/epoch, and all-layer
   model/cache state only. Every layer must have the same accepted prefix and
   compatible existing identity. This goal does not carry generation history,
   output cursor/budget, stop state, or RNG; context-lookup integration owns
   those facts and coordinates their publication with cache commit. This goal
   does not add identity fields or a new identity wire.
2. Add a `SpeculativeBranch` value created from one checkpoint and a bounded
   candidate block. Branch evaluation constructs independent logical layer
   values and records target rows/candidate provenance needed by the caller.
   It never writes through or trims the checkpoint. Candidate evaluation may
   fail for shape, gap, capacity, identity, or numeric reasons without
   changing the checkpoint.
3. Add an acceptance result and one atomic commit operation. The caller gives
   an accepted-prefix count `n` with `0 ≤ n ≤ k`; commit returns a new
   all-layer state containing the base prefix plus exactly the first `n`
   branch rows and discards the suffix. `n = 0` returns an equivalent base
   state. Invalid counts or mismatched branch/checkpoint identity reject
   without partial writes.
4. Implement commit by constructing a fresh logical state (or an equivalent
   persistent value) from the checkpoint and accepted branch prefix. It must
   not mutate a shared cache in place and must not expose a `trim(shared)`
   escape hatch. Version/epoch changes are defined once for an atomic commit,
   and all layer versions move together.
5. Keep physical allocation, device residency, quantization, scheduling, and
   handles outside this contract. The logical branch may later be lowered to
   those mechanisms, but such a backend must preserve the value-level
   isolation and atomic result defined here.

### Non-goals

- No speculative acceptance policy, lookup drafting, sampling correction, or
  generation dispatch; those belong to `speculative-decode-contract`.
- No generation history, output cursor/budget, stop state, or RNG transaction.
  `context-lookup-drafting` owns that generation state and coordinates it with
  this goal's model/cache commit.
- No canonical prepared-state identity, payload binding, serialized lookup
  key, or reuse authorization. `prepared-prefix-state` owns those contracts.
- No model-based draft weights, external services, request scheduling,
  continuous batching, or prefix-store ownership.
- No physical device handles, Metal/CUDA kernels, residency management,
  memory pools, or quantized KV representation.
- No naive per-layer trim or mutable shared-cache transaction that can expose
  the speculative suffix.
- No weakening of the existing cache identity fields or silent acceptance of
  a branch with a different model/config/tokenizer/position contract.

## Units (lowering sketch — refine via `$delivery`)

| Unit | Scope | Depends on | Done when | Validation | Hand evidence |
| --- | --- | --- | --- | --- | --- |
| 1. All-layer checkpoint contract | Define the checkpoint value, shared-prefix invariant, opaque existing-identity equality, generation/epoch semantics, and unchanged-on-failure rule. Do not extend identity or add a wire. | — | A checkpoint can be compared and resumed as one all-layer value; mismatched layer lengths or existing identities reject. | Cache equality/shape/error `.proba` rows; `./scripta/check-source`; `./scripta/check-compile`. | none |
| 2. Independent branch materialization | Create a bounded speculative branch from a checkpoint with independent per-layer logical state and candidate metadata; preserve the checkpoint on success and failure. | 1 | Mutating/evaluating a branch cannot change any checkpoint field, tensor, history, length, or epoch. | Branch isolation, multi-layer alignment, gap, capacity, and failure-invariance `.proba` rows; focused `faber test`. | none |
| 3. Accepted-prefix result | Define the typed acceptance result, including candidate count, accepted count, discarded suffix, resulting identity, and target rows required by the caller. | 1, 2 | Results distinguish zero, partial, and full acceptance and reject counts outside `0..k` without state changes. | Result serialization/equality and boundary/error `.proba` rows; source/compile gates. | none |
| 4. Atomic all-layer commit | Commit exactly the accepted prefix into a fresh all-layer state and discard the branch suffix in one operation; advance version/epoch once as specified. | 1, 2, 3 | Every committed layer has the same accepted length/history/identity; a failed commit leaves the original checkpoint byte-for-byte semantically unchanged. | Full/partial/zero acceptance, identity mismatch, overflow, and injected failure rows; focused `faber test`. | none |
| 5. Consumer transaction seam | Expose the device-neutral begin/inspect/commit/abort operations required by cached-block and prepared-state consumers without adding dense logits, candidate policy, or device execution. | 1–4 | A synthetic multi-layer fixture can exercise the whole transaction lifecycle through one public logical seam. | Cache transaction `.proba` rows for begin, zero/partial/full commit, abort, and stale checkpoint rejection. | none |
| 6. Contract closeout and truth pass | Update cache/dense headers and campaign references so rollback means branching/atomic commit, not naive trim; document all out-of-scope physical ownership. | 1–5 | No live Gradus doc or error path promises physical handles or mutable shared trimming; factory audit is clean. | `rg` truth scan, `git diff --check`, factory-goal status audit, source/compile gates. | none |

## Validation

The closeout gate is the unit validations above plus:

```bash
python3 ../radix/scripta/audit-factory-goal-status.py \
    --factory-root docs/factory --fail-on error
./scripta/check-source
./scripta/check-compile
```

The focused cache/dense proba cases must prove value isolation and
all-layer atomicity, not merely successful construction. A single-layer
append/trim test is insufficient. Execution receipts must distinguish the
logical Gradus contract from any later device-residency implementation.

## Ledger

| Unit | Status | Seat | Receipt | Notes |
| --- | --- | --- | --- | --- |
| 1 | done | hand | `63a8d73` | cache-branch contract leaf `src/cache_branch.fab` |
| 2 | done | hand | `f8f4b43` | isolated speculative branches |
| 3 | done | hand | `0530fee` | AcceptanceDecision wraps SD0-U4 `GreedyAcceptance`; validation re-proven on `9793720da` (filter 4/0; `--include cache_branch` 18/0). Sanity-string nit: delivery filter `decision` matches 1 of 4 titles — use `--filter AcceptanceDecision` |
| 4 | done | hand | `dd385c1` | atomic all-layer prefix commit; zero/partial/full and failure-invariance rows landed |
| 5 | done | hand | `5392885` | device-neutral begin/inspect/commit/abort lifecycle seam landed |
| 6 | done | hand | `edb8437` | cache/dense rollback boundary and physical-ownership comments; truth scan and closeout gates recorded by task receipt |

Lowered to [`delivery.md`](delivery.md) as SD1-1..6 (2026-08-22). Delivery
pins the goal's open questions against live code: epoch = the existing
`KVCache.version` (`+1` once per successful commit, `n = 0` equivalent-base);
capacity = the existing `_admit_write` bound; the new contract lives in a new
leaf `src/cache_branch.fab` so the live `cache.fab`/`cache.proba` seat
surfaces stay untouched. U3 wraps SD0-U4's landed `GreedyAcceptance`.

## Open questions

1. **Checkpoint state payload.** Include all-layer model/cache state, the
   existing opaque cache-identity equality value, prefix length, and epoch.
   Exclude generation history, output cursor/budget, stop state, and RNG.
   Context lookup coordinates those separate generation facts with this
   model/cache commit. Dense row production remains in cached-block
   verification.
2. **Value-copy boundary.** Default: use functional cache values and fresh
   tensors at the logical boundary. Any structural sharing must be
   unobservable and must preserve checkpoint immutability; no physical-handle
   contract may leak into Gradus.
3. **Version/epoch semantics.** Default: branch creation does not advance the
   base epoch; one successful commit advances it once; failed commit and
   discarded branch leave the base epoch unchanged. The delivery spec pins
   the exact integer representation.
4. **Capacity accounting.** Default: branch capacity is checked against the
   same logical context limit before evaluation, and overflow rejects without
   a partially extended layer set.

---

<!-- Created from radix/docs/factory/TEMPLATE.md. Status line is the audit
     authority; ledger phase table drives completion %. -->
