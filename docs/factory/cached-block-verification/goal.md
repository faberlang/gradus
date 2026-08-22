# GOAL: cached-block-verification — verify a candidate token block against the Gradus reference path

**Status**: active — U1/U2 landed 2026-08-22 (`6754440` contract, `fad0d57` forward seam; proba green); U3 in flight; U4→U5 serial spine (U3∥U4 logically, same file → land serially)
**Created**: 2026-08-21
**Campaign:** `speculative-decode`
**Source:** SD2 in [`../speculative-decode/CAMPAIGN.md`](../speculative-decode/CAMPAIGN.md); operator request to lower the cached verification block as a named Gradus goal
**Repos:** primary `gradus/`; evidence-only `radix/` and `hosts/` for the separate device route
**Related:** [`../speculative-decode/CAMPAIGN.md`](../speculative-decode/CAMPAIGN.md); [`../production-ml-library/CAMPAIGN.md`](../production-ml-library/CAMPAIGN.md); `radix/docs/factory/kv-cache-semantic-contract/goal.md`; `radix/docs/factory/kv-cache-model-session/goal.md`

---

## Invariant

For a nonempty accepted prefix of length `L` and a nonempty candidate block of
`k` token ids, the Gradus reference contract produces one `[k, V]` target-logit
matrix and one committed state result. Candidate `i` is evaluated at position
`L + i`; the returned row-to-position convention is fixed and agrees with the
full-recompute oracle. Either every admitted layer advances atomically through
the block or no layer/state is changed.

The goal proves structural/reference semantics only. It does not claim device
execution, residency, kernel fusion, CUDA/Metal performance, or value identity
outside the accepted Gradus reference tier.

## Problem

The live cache contract exposes sequential `append`, prefill `extend`, and
whole-cache `reset`, but no candidate-block transaction (`src/cache.fab:31-58,
387-475`). The live cached decoder is explicitly one-token-per-call
(`src/decode.fab:470-511`), while the campaign requires one forward contract
for `L + k` with `[k, V]` logits and an all-layer state result. The current
source has no named speculative or lookahead operation. Existing KV identity
and mutation rules are the foundation, not a second block-verification
authority.

## Proposal

1. Define a typed reference operation over an already admitted, nonempty prefix
   and a nonempty candidate block. The operation validates token ids, context
   capacity, layer/state shapes, and the exact candidate positions
   `L..L+k-1` before it evaluates anything.
2. Pin the logit-row convention: row `i` is the target distribution used to
   accept or reject candidate `i`, computed from the prefix plus candidates
   before `i`; candidate `i` writes its K/V at position `L+i`. The full
   recompute oracle is the authority for this mapping.
3. Return the complete per-layer state after the candidate block only on
   success. A validation, forward, shape, capacity, or numeric failure returns
   a typed error and leaves the caller's original state unchanged. No partial
   layer result is observable.
4. Expose the narrow result as the consumer seam for the later speculative
   loop. This goal does not choose draft candidates, acceptance policy, or
   request scheduling.

### Non-goals

- No Metal, CUDA, device handle, residency, allocator, descriptor, kernel, or
  performance implementation. Those route to the Radix/Hosts device goals.
- No prefix pinning, cross-request reuse, paging, eviction, or tenant scope.
- No model-drafter weights, MTP, DFlash, or lookup policy. Candidate production
  belongs to a separate Gradus goal.
- No new sampler algorithm and no silent change to the PML5 generation-config
  authority.
- No executed-device or end-to-end product claim from structural/reference
  receipts.

## Units (lowering sketch — refine via `$delivery`)

| Unit | Scope | Depends on | Hand evidence |
| --- | --- | --- | --- |
| 1 | Freeze the candidate-block contract: nonempty `L`, nonempty `k`, exact position and logit-row mapping, shapes, bounds, and typed failures; update the co-located contract/proba surface | PML5 cache/decode contracts | contract receipt with reject rows |
| 2 | Add the Gradus reference block operation and result carrier over the existing logical per-layer cache state; keep the API device-neutral | 1 | compile receipt and reference invocation |
| 3 | Enforce all-layer atomicity: validate and stage every layer, commit all layers together, and preserve the original state on every failure path | 1, 2 | success/failure state snapshots and multi-layer proba |
| 4 | Build the full-recompute oracle for the same prefix and candidates; compare every `[k, V]` row, position, token history, and final layer state under the admitted numeric tolerance | 2, 3 | exact first-divergence/equivalence receipt |
| 5 | Publish the consumer seam for the speculative loop without adding candidate policy or a device route | 3, 4 | typed consumer fixture and structural receipt |

Every unit is required for this goal. No unit is deferred or optional.

## Validation

- `./scripta/check-source` and `./scripta/check-compile` pass in `gradus/`.
- The scoped Gradus proba cases cover `L >= 1`, `k >= 1`, positions
  `L..L+k-1`, context/shape/token rejection, and all-layer atomic failure.
- Full-recompute comparison covers every returned logit row and every layer's
  final logical state; the first divergence is recorded and no tolerance is
  widened locally.
- The result carrier contains no device or scheduler dependency. Validation
  reports structural/reference evidence separately from any downstream Radix
  device receipt.

## Ledger

| Unit | Status | Seat | Receipt (commit/handle) | Notes |
| --- | --- | --- | --- | --- |
| 1 | done | hand | `6754440` | contract and reject rows (7/7 proba) |
| 2 | done | hand | `fad0d57` | reference block/result carrier (4/4 proba) |
| 3 | in flight | hand | task `94c72dfe` | all-layer atomicity |
| 4 | pending | — | — | full-recompute oracle |
| 5 | pending | — | — | speculative-loop consumer seam |

## Open questions

1. **Carrier shape.** Default: reuse the existing logical list-of-layer cache
   state and add one typed block result rather than minting a second KV identity
   type. The delivery may choose a dedicated aggregate only if it preserves
   field-wise identity and atomicity.
2. **Numeric comparison.** Default: use the already-admitted PML/GI reference
   tolerance and first-divergence rule; this goal does not widen it.
3. **Failure carrier.** Default: typed error plus the untouched input state;
   no partial state is returned even if an earlier layer succeeded.

---

<!-- Created from radix/docs/factory/TEMPLATE.md. Status line is the audit
     authority; ledger phase table drives completion %. -->
