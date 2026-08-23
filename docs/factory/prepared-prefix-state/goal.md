# GOAL: prepared-prefix-state — device-neutral prepared state for exact-prefix continuation

**Status**: active — DENSE SPINE COMPLETE: PP-U1 5f1ad4d, U2 398545d, U3a 4ad5621, U3b 68f58c3, U4a 50fe7e8 (cold-vs-warm equivalence proven at 1e-5); U5 truth pass gated on U4b (hybrid, blocked MODEL-03/04). Known non-blocker: radix-mir-runner textus.get carrier divergence (fix 4baa3f09 in flight) explains tokenizer red (2026-08-23)
**Created**: 2026-08-21
**Campaign:** `speculative-decode`
**Source:** operator expansion of the SD5 boundary, grounded in the live Gradus cache/decode surface and PML MODEL-01–04 composition contracts
**Dependency state:** dense rows are implementable from live source; hybrid closeout waits for MODEL-03 state and MODEL-04 full-model composition (verified 2026-08-23: MODEL-01 admission chain landed on main; MODEL-02 done 2026-08-22, receipt `8febe40`; LIB-02 tokenizer landed — no longer blocking)
**Repos:** primary: `gradus/`; evidence only: `inferentia/`
**Related:** [`../speculative-decode/CAMPAIGN.md`](../speculative-decode/CAMPAIGN.md); [`MODEL-01`](../production-ml-library/pml5-gguf-m1-qwen35moe-admission-delivery.md); [`MODEL-02`](../production-ml-library/pml5-gguf-m2-moe-router-delivery.md); [`MODEL-03`](../production-ml-library/pml5-gguf-m3-ssm-attention-state-delivery.md); [`MODEL-04`](../production-ml-library/model04-full-model-reference-inference-delivery.md); [`LIB-02 tokenizer`](../production-ml-library/pml5-lib02-tokenizer-delivery.md); `gradus/docs/api-reference.md`

---

## Invariant

A prepared state is a complete, device-neutral logical snapshot for the
admitted model at an exact token prefix and position: KV state plus every
recurrent, convolutional, or other architecture-required state family. Its
canonical identity binds content, model, state-producing execution config,
tokenizer, and position. Attaching a continuation to the longest authorized
exact prefix produces the same state and token stream as a cold run.

Gradus exposes values and pure attach/continue operations only. It does not
retain states, authorize callers, choose tenants, own a registry, or carry
device handles.

## Problem

The current cache surface is a single transformer KV value with exact token
history and structural identity fields, not a complete prepared-state or
reuse protocol (`src/cache.fab` contract `:21-61`; `KVCache` `:239`;
`append`/`extend`/`reset` `:413-494`; `CacheIdentity` `:505-579`; identity
wire `:589-632`). The current identity is useful precedent, but it does not
itself provide candidate selection, payload binding, or continuation.

Batched prefill remains empty-prefix-only: `prefill_cached`
(`src/model/dense.fab:681`, zero-prefix guard at `:695`) rejects a non-empty
prefix. The landed SD2 seam `decode_block` (`src/model/dense.fab:589`,
commit `fad0d57`) already performs multi-row incremental decode over a
non-empty per-layer cache, so suffix execution exists as a building block;
what is missing is continuation from a complete prepared state that consumes
only the suffix and returns the next complete state. The generation entry
point updates cache state internally and returns only tokens, discarding the
updated state (`generate_dense_with_stop`, `src/generation.fab:1100`). The
public decode `Session` tracks only position and context
(`src/decode.fab:551-601`).

The future model set is not KV-only. The MODEL-03 contract requires separate
attention KV state and linear-attention recurrent plus convolution state,
with reset, replay, position handling, and incremental updates
(`docs/factory/production-ml-library/pml5-gguf-m3-ssm-attention-state-delivery.md`)
§1–§2. A prefix goal that models only KV would silently make hybrid models
unsafe to reuse.

## Proposal

Introduce one logical prepared-state contract, extending the existing cache
identity precedent rather than creating a second fast-path decode API.

### Canonical identity

The identity is versioned and field-wise comparable. It contains:

| Component | Required binding |
| --- | --- |
| Content | Exact canonical token prefix plus length. Serialized lookup may carry an opaque host/provider-supplied digest; Gradus does not compute a cryptographic digest, and equality remains exact token equality rather than digest-only. |
| Model | Admitted model/capsule identity, model version, and artifact content identity. |
| Execution config | Every state-producing fact: architecture/state schedule, attention/SSM family, context and RoPE/position rules, dtype, layout, and relevant KV structure. Sampling-only fields that do not change prepared state are not smuggled into this component. |
| Tokenizer | Tokenizer identity, schema/version, vocabulary/merge identity, and special-token policy used to produce the prefix. |
| Position | Exact consumed range, next position, and any sectioned-RoPE or recurrent-position coordinates. |

The prepared payload carries the corresponding typed state for every declared
layer/state family. A payload binding covers the canonical identity and the
payload shape/content; a mismatch rejects before attachment. Serialization is
versioned and fail-closed. A serialized identity is an index key, not an
authorization grant.

### Attach and continue

The attach operation receives a caller-provided, already-authorized set of
candidate prepared states and the request's canonical token sequence. It:

1. rejects candidates whose model/config/tokenizer/position or payload binding
   does not match;
2. finds the longest exact candidate prefix of the requested tokens;
3. applies deterministic tie handling for equal-length candidates;
4. returns an independent continuation state plus the consumed prefix length;
5. leaves the candidate snapshot unchanged, so multiple continuations cannot
   mutate one another.

No global cache, retention policy, tenant decision, ACL, or device residency
is part of this contract. The product caller decides which candidates are
authorized and passes only those candidates to Gradus.

### Non-goals

- No Inferentia HTTP/session registry, tenant authorization, retention, TTL,
  eviction, or capacity policy.
- No raw product request routing or scheduling.
- No device handles, allocator ownership, device placement, multi-device
  tiers, or cross-device routing. MD4D owns multi-device tiers and routing;
  this goal is one logical state contract.
- No CUDA/Metal kernels, quantized-KV storage policy, or performance claim.
- No tokenizer implementation, model admission, MoE routing, or model-drafter
  speculative decoding.
- No multi-token verification policy; this goal shares branching primitives
  with cached-block verification but does not own its candidate/logit contract.

## Units (lowering sketch — lowered 2026-08-23 in [`delivery.md`](delivery.md) as `PP-U1`…`PP-U5`; U3/U4 split per behavior family)

All units below are admitted and mandatory. There are no optional or deferred
units in this goal.

| Unit | Scope | Depends on | Hand evidence |
| --- | --- | --- | --- |
| 1 | Canonical prepared identity and versioned identity wire in `src/cache.fab` (or the owning state module) and `docs/api-reference.md`; include content/model/config/tokenizer/position fields and field-wise equality. A lookup digest is opaque host/provider input, never language-computed or equality authority. | Existing cache identity; MODEL-01/capsule content identity; LIB-02 tokenizer identity | `faber check .`; focused identity proba with exact fixtures |
| 2 | Complete typed prepared-state value covering KV and architecture-declared recurrent/SSM/convolution state, reset/copy semantics, and payload binding. Done when dense and hybrid state families are represented without device handles or hidden global state. | 1; MODEL-01 architecture; MODEL-02 router/expert state consumers; MODEL-03 state schedule | `faber check .`; focused state construction/reset/equality proba |
| 3 | Longest-authorized-prefix attach and independent continuation state. Done when exact-prefix candidates select the longest valid prefix, mismatches reject, equal candidates resolve deterministically, and the source snapshot remains unchanged. | 1, 2; tokenizer and position semantics | `faber test` scoped to identity/state/attach cases; first-divergence state comparison |
| 4 | Continuation integration for dense and hybrid execution surfaces, including suffix prefill from a prepared state and returned updated state. Done when warm continuation consumes only the suffix and exposes the complete next prepared state through one decode/generation surface. | 2, 3; dense continuation; MODEL-03 incremental state; MODEL-04 full-model composition; LIB-02 tokenizer | Executed cold-vs-warm token/logit equality on each admitted architecture row |
| 5 | Contract truth pass: diagnostics, API reference, module map, reject rows, and regression fixtures document no-retention/no-auth/no-device ownership. Done when the public surface and source agree and malformed or incompatible prepared payloads fail closed. | 1–4 | `faber check .`; scoped `faber test`; `rg` audit for stale KV-only/reuse claims |

## Validation

The closeout gate requires all of the following:

- `faber check .` is green in `gradus/`.
- Scoped Gradus tests/proba prove identity round-trip, every identity mismatch
  row, payload-binding mismatch, reset, independent branching, longest-prefix
  selection, and fail-closed behavior.
- A dense fixture proves cold prefill followed by continuation is state- and
  token-stream-equivalent to a fresh cold run under identical configuration
  and seed.
- A hybrid fixture proves KV plus recurrent/convolution state is carried,
  reset, replayed, and continued without conflation; the first divergence is
  recorded per layer and position.
- The prepared-state source exposes no registry, authorization decision,
  retention policy, device handle, or physical residency field.
- API and diagnostic docs identify MD4D as the owner of multi-device tiers and
  routing, and identify Inferentia as the product consumer of this contract.

## Ledger

| Unit | Status | Seat | Receipt | Notes |
| --- | --- | --- | --- | --- |
| 1 | pending | — | — | Canonical identity and wire |
| 2 | pending | — | — | Complete KV plus recurrent/SSM prepared state |
| 3 | pending | — | — | Longest authorized prefix attach |
| 4 | pending | — | — | Dense and hybrid continuation |
| 5 | pending | — | — | Truth, diagnostics, and regression fixtures |

## Open questions

1. **Identity representation** — exact token equality is authoritative inside
   Gradus. Serialized lookup may carry a versioned, opaque host/provider-supplied
   digest plus length; Gradus does not compute it and never treats a digest
   collision as equality.
2. **Sampling fields** — default: identity includes only fields that can alter
   prepared state; the cold/warm proof nevertheless pins the complete
   `GenerationConfig` and seed. A future state-affecting sampler must be added
   to the execution-config component before reuse is admitted.
3. **Candidate authorization** — default: the caller supplies the authorized
   candidate set; Gradus verifies identity and payload but performs no auth.
4. **State ownership after attach** — default: prepared snapshots are
   immutable from the caller's perspective and continuation returns a new
   state. No in-place branch mutation is admitted.
