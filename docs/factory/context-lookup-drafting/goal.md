# GOAL: context-lookup-drafting — deterministic context-sourced candidates for speculative verification

**Status**: planned — pre-implementation; ready for delivery
**Created**: 2026-08-21
**Campaign:** `speculative-decode`
**Source:** SD4 in [`../speculative-decode/CAMPAIGN.md`](../speculative-decode/CAMPAIGN.md); operator request to lower the lookup-drafting policy as a named Gradus goal
**Repos:** primary `gradus/`; evidence-only `radix/` and `inferentia/`
**Related:** [`../speculative-decode/CAMPAIGN.md`](../speculative-decode/CAMPAIGN.md); [`../cached-block-verification/goal.md`](../cached-block-verification/goal.md); [`../production-ml-library/CAMPAIGN.md`](../production-ml-library/CAMPAIGN.md); `inferentia/docs/factory/inferentia/CAMPAIGN.md`

---

## Invariant

For fixed accepted token history, prompt context, and versioned generation
configuration, context lookup returns the same candidate sequence or the same
empty result on every run. Search, tie-breaking, window bounds, and fallback
are explicit token-level semantics, with no model-drafter weights and no RNG
consumption while proposing candidates.

When the candidates enter the speculative loop, the accepted greedy token
stream and generation state are identical to the plain path. Sampled
acceleration rejects before lookup or branch creation in this campaign.

## Problem

The live generation path samples one target token and then performs one cached
decode step at a time (`src/generation.fab:706-740, 769-811`), and the current
Gradus tree has no lookup/draft provider. `GenerationConfig` is a versioned,
validated nine-field authority (`src/generation.fab:189-327, 362-427`); unknown
controls are rejected rather than ignored. The speculative campaign therefore
needs an additive, versioned lookup policy and a deterministic seam that can
feed the cached-block contract without creating a model-drafter or a parallel
fast-path API.

## Proposal

1. Search only the admitted token context: the prompt plus accepted generated
   history. Match the current suffix as exact token ids; do not normalize text,
   cross a request boundary, or inspect unaccepted candidate tokens.
2. Use a bounded lookup window from the versioned policy. Search suffix lengths
   from the configured maximum downward, require a following source token, and
   extend only through the configured candidate limit and available context.
   The default tie rule is longest exact match first, then lowest source offset.
3. Return a deterministic candidate list plus search metadata, or an empty
   proposal when no usable occurrence exists. Empty lookup is an ordinary,
   valid fallback to the plain target step. Invalid policy, ambiguous state, or
   inability to preserve target sampler state is a typed reject, not a silent
   fast-path downgrade.
4. Consume the versioned acceleration policy frozen by
   [`speculative-decode-contract`](../speculative-decode-contract/goal.md).
   This goal implements its lookup mode and does not mint a second config wire
   or choose different defaults.
5. Feed the candidates through
   [`cached-block-verification`](../cached-block-verification/goal.md). Draft
   proposal itself consumes no sampler seed. The generation integration stages
   accepted token history, output cursor/budget, and stop state alongside the
   cache branch and publishes them only after the target acceptance commits.
   Abort leaves those facts unchanged. Sampled policy rejects before staging.
6. Record regime-labeled equivalence and acceptance receipts for a
   context-reproduction corpus and an ordinary-chat corpus. Throughput, draft
   length, acceptance rate, fallback rate, and overhead are separate measured
   fields; external technique numbers are not Gradus targets.

### Non-goals

- No model-drafter, MTP, DFlash, auxiliary weights, or learned proposal model.
- No kernel, device, residency, CUDA/Metal, scheduler, HTTP, or serving work.
- No cross-request prefix cache or tenant/reclamation policy.
- No new sampling algorithm and no unproven sampled-equivalence claim.
- No silent extension of `GenerationConfig` and no parallel speculative API
  that bypasses its validation and wire version.

## Units (lowering sketch — refine via `$delivery`)

| Unit | Scope | Depends on | Hand evidence |
| --- | --- | --- | --- |
| 1 | Freeze exact token search, suffix/window bounds, tie rule, candidate extension, empty-result fallback, and typed reject semantics | SD0 contract | deterministic policy receipt |
| 2 | Implement the context-only deterministic candidate provider against the frozen provider seam and co-located repeatability/search-boundary proofs | 1; speculative-decode contract | same-input same-output receipt |
| 3 | Integrate candidates with the cached-block verification seam and existing dense generation dispatch; transactionally stage accepted token history, output cursor/budget, and stop state with cache commit; reject sampled policy before branch creation | `cached-block-verification`, `kv-cache-branching`, 2 | plain-vs-lookup token/generation/cache-state comparison |
| 4 | Prove the disabled/no-match path performs the plain target step without claiming acceleration, and malformed or unsupported policy values retain the contract's rejection behavior | speculative-decode contract, 3 | policy dispatch and fallback/reject fixtures |
| 5 | Produce regime-labeled equivalence, acceptance, fallback, and overhead receipts for context-reproduction and ordinary-chat corpora | 2–4 | two-corpus receipt with first-divergence rule |

Every unit is required for this goal. No unit is deferred or optional.

## Validation

- `./scripta/check-source` and `./scripta/check-compile` pass in `gradus/`.
- Scoped Gradus proba cases prove exact token search, longest-match/offset tie
  behavior, window and candidate limits, empty lookup, malformed policy
  rejection, and configuration wire compatibility.
- Repeated runs with identical context/config produce identical candidates and
  metadata. The candidate provider never advances the sampler seed.
- Greedy lookup runs match the plain loop token-for-token and state-for-state,
  including accepted history, output cursor/budget, and stop behavior. Sampled
  acceleration returns the typed reject before lookup, RNG use, or branch
  creation; no mismatch is hidden by a fallback label.
- Both corpus receipts label regime, context, draft length, acceptance,
  fallback, overhead, TTFT/tok/s, and first divergence separately. No device or
  product performance claim is made by this Gradus goal.

## Ledger

| Unit | Status | Seat | Receipt (commit/handle) | Notes |
| --- | --- | --- | --- | --- |
| 1 | pending | — | — | search and fallback contract |
| 2 | pending | — | — | deterministic provider |
| 3 | pending | — | — | verification-loop and generation integration |
| 4 | pending | — | — | disabled/no-match fallback and reject behavior |
| 5 | pending | — | — | regime-labeled receipts |

## Open questions

1. **Window default.** Default: search the configured maximum suffix length
   downward to one token, never beyond available context; delivery pins the
   concrete default and reject boundary.
2. **Tie rule.** Default: longest exact match, then lowest source offset. Any
   change must update the deterministic fixtures and receipt schema together.
3. **Sampler policy.** No-match is an empty proposal and plain target step.
   Any sampled acceleration request returns the contract's typed reject before
   lookup or transaction work. Broadening this requires a campaign amendment.

---

<!-- Created from radix/docs/factory/TEMPLATE.md. Status line is the audit
     authority; ledger phase table drives completion %. -->
