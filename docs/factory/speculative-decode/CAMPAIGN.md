# Campaign: Speculative Decode And Prepared-Prefix Reuse

**Status**: planned — live-code review complete 2026-08-21; lowered into eight named factory goals; no delivery or implementation has started
**Created**: 2026-08-21
**Mode**: low-priority routing artifact — keep visible and execute incrementally when capacity is assigned
**Control-plane repo**: `/Users/ianzepp/work/faberlang/gradus`
**Participating repos**: `gradus` (logical decode, cache, sampling, and prepared-state contracts); `radix` and `hosts` (compiled device execution); `inferentia` (single-node retained-state consumer)
**Source**: operator-forwarded RTX 3090 post; [current reproduction repository](https://github.com/syv-ai/qwen38-27b-rtx3090); [DFlash paper](https://arxiv.org/abs/2602.06036)
**Related**: [`production-ml-library`](../production-ml-library/CAMPAIGN.md); [`radix device-executor`](../../../../radix/docs/factory/device-executor/goal.md); [`radix kv-cache-decode`](../../../../radix/docs/factory/kv-cache-decode/CAMPAIGN.md); [`Inferentia`](../../../../inferentia/docs/factory/inferentia/CAMPAIGN.md)
**Campaign readiness**: READY FOR DELIVERY — [`speculative-decode-contract`](../../archived/speculative-decode-contract/goal.md) is the first mandatory goal when this campaign receives capacity

## Summary

Add one explicit, lossless acceleration policy to the current dense generation
surface. The first candidate provider is deterministic context lookup. Gradus
owns reference semantics and complete prepared state; Radix/Hosts own compiled
multi-row execution; Inferentia owns private retention and warm-request
evidence. Metal is the development route and CUDA is a mandatory peer
qualification before campaign close.

Low priority is a scheduling decision, not reduced scope. Every named goal
below is part of the completion contract. Model drafters, quantized KV,
continuous batching, and multi-device cache tiers are outside this campaign
and require a separate campaign or an explicit amendment.

## Source Claims And Transferable Direction

The current reproduction repository reports about 133 tok/s for ordinary chat,
up to 381 tok/s for context-reproduction workloads, 15.0 accepted tokens per
target step in its reported run, and repeat-prefix prefill falling from 22.4 s
to 0.56 s. It combines a DFlash2 draft model, context lookup, and complete
prepared-state reuse. Hybrid-model reuse includes attention KV and recurrent
state; it is not a KV-only cache.

Those figures are external technique evidence, not Gradus targets. The durable
direction is:

1. score a candidate block in one batched target invocation and commit only its
   accepted prefix;
2. use exact prompt/history matches as a weightless first candidate provider;
3. retain complete state for an exact prepared prefix, including non-KV state;
4. separate context-reproduction and ordinary-chat measurements; and
5. gate every speed or TTFT claim on output/state equivalence.

One batched invocation is not assumed to cost the same as one scalar decode.
Acceptance, target work, transfer overhead, and throughput are measured
separately.

## Verified Ground Truth

Source snapshot: Gradus `cf82f70`, Inferentia `3c7211d`, Radix `04d8d5cc4`,
Hosts `2097ffc` on 2026-08-21. Unrelated semantic work was present in Gradus
and Radix during the documentation edit and was left untouched. Delivery must
refresh these facts before implementation.

| Fact | Live authority | Consequence |
| --- | --- | --- |
| The cache-aware generation baseline is `generate_dense_with_stop`, which advances through scalar `dense.decode_step`. | `gradus/src/generation.fab:775-812`; `gradus/src/model/dense.fab:488-560` | Equivalence and k=1 behavior are pinned to this route, not the noncached toy generator. |
| `prefill_cached` accepts several rows only when the prior prefix is empty. | `gradus/src/model/dense.fab:572-647` | Verification needs an explicit nonempty-prefix block operation. |
| Lower attention/cache primitives can carry several rows. | `gradus/src/attention.fab:1071-1111`; `gradus/src/cache.fab:393-456` | Reference block verification is directionally implementable now. |
| Cache supports append, extend, and reset, but no checkpoint, branch, commit, or rollback. | `gradus/src/cache.fab:393-468` | Candidate state must be private and atomically committed; shared-cache trimming is not the contract. |
| `CacheIdentity` is metadata, not retained payload, lifecycle, scope, or authorization. | `gradus/src/cache.fab:480-607` | Reuse requires complete state, payload binding, and a product-owned private registry. |
| `KVCache` stores staged f32 rows; Q8/Q4 values are descriptor rows, not quantized execution proof. | `gradus/src/cache.fab:393-456` and dtype declarations | Quantized KV remains outside this campaign. |
| Greedy sampling is exact argmax; stochastic sampling advances explicit history/RNG state. | `gradus/src/sampling.fab:195-235` | Greedy is admitted first. Sampled acceleration requires pathwise proof or a typed reject. |
| Inferentia keeps weights resident but constructs and discards fresh caches for every request. | `inferentia/src/main.fab:965-1007,1448-1462` | Warm-prefix reuse needs an explicit consumer lifecycle. |
| Inferentia still has a frozen-prompt tokenizer fallback and emits SSE only after generation completes. | `inferentia/src/main.fab:727-750,874-887` | Arbitrary-prompt tokenization and a true first-token boundary precede honest warm TTFT evidence. |
| Radix device execution has static prefill/scalar-decode modes; M4 device KV work is incomplete. | `radix/docs/factory/device-executor/goal.md`; `radix/docs/factory/kv-cache-decode/CAMPAIGN.md` | The device goal consumes these campaigns and does not duplicate them. |
| CUDA has a real one-shot kernel proof, but rejects dynamic/nonzero/runtime KV bindings. | `hosts/macos-arm64/src/cuda_host.rs`; `hosts/macos-arm64/src/device_host.rs` | CUDA qualification includes the missing persistent dynamic-binding path before a speculative receipt. |
| The old RunPod verification goal is archived and does not prove inference. | `radix/docs/archived/runpod-gpu-verification/goal.md` | Future paid evidence uses the live CAP-02 rails with a new speculative receipt and fresh authorization. |

## Non-Negotiable Invariants

1. `generate_dense_with_stop` remains the plain semantic oracle.
2. Acceleration is one versioned explicit policy and defaults to disabled.
3. An admitted path emits the same tokens and logical state as the plain path
   under the same model, prompt, configuration, stop policy, and seed.
4. This campaign accelerates greedy generation only. Sampled acceleration
   rejects before lookup, RNG consumption, or branch creation.
5. A speculative branch cannot mutate its base. Commit is all-layer atomic.
6. Prepared state includes every architecture-required KV, recurrent, SSM,
   convolution, and position component.
7. Identity verifies compatibility; it never grants authorization. Raw token
   keys are not a public product surface.
8. Receipts label context-reproduction versus ordinary chat and distinguish
   reference, compiled, Metal, CUDA, cold, and warm evidence.
9. No stage closes on a shaped fixture, fake driver, or prose claim when its
   gate requires executed value identity.

## Named Factory Goals

| Goal | Repo | Owns | Mandatory dependency |
| --- | --- | --- | --- |
| [`speculative-decode-contract`](../../archived/speculative-decode-contract/goal.md) | Gradus | dense baseline, policy/version, acceptance and receipt contracts | PML generation/config authority |
| [`kv-cache-branching`](../kv-cache-branching/goal.md) | Gradus | immutable checkpoint, private branch, atomic prefix commit | contract |
| [`cached-block-verification`](../cached-block-verification/goal.md) | Gradus | nonempty-prefix k-row reference verification | branching |
| [`context-lookup-drafting`](../context-lookup-drafting/goal.md) | Gradus | deterministic weightless candidate policy and transactional greedy generation integration | contract, cached block |
| [`prepared-prefix-state`](../prepared-prefix-state/goal.md) | Gradus | canonical complete state, payload binding, exact-prefix continuation | branching; hybrid-state contract |
| [`speculative-verification-execution`](../../../../radix/docs/factory/speculative-verification-execution/goal.md) | Radix/Hosts | versioned device ABI and compiled Metal block verification | cached block; device-executor M4; kv-cache-decode |
| [`prefix-reuse-consumer`](../../../../inferentia/docs/factory/prefix-reuse-consumer/goal.md) | Inferentia | private bounded retention, attach lifecycle, real streaming/TTFT receipt | prepared state; tokenizer; clock/streaming |
| [`speculative-decode-cuda-qualification`](../../../../radix/docs/factory/speculative-decode-cuda-qualification/goal.md) | Radix/Hosts | persistent CUDA binding/lifecycle and authorized RunPod qualification | all semantic/consumer goals and Metal execution |

These goal files are planning artifacts. Their presence does not mean work is
running, implemented, or validated.

## Campaign Path

### SD0 — Contract and evidence schema

**Goal**: [`speculative-decode-contract`](../../archived/speculative-decode-contract/goal.md)
**Gate**: named dense baseline; explicit disabled-by-default policy; greedy and
sampled admission rules; context-reproduction and ordinary-chat corpora; one
versioned receipt schema. No candidate implementation is part of SD0.

### SD1 — Transactional logical state

**Goal**: [`kv-cache-branching`](../kv-cache-branching/goal.md)
**Gate**: immutable all-layer checkpoint; private branch; zero/partial/full
accepted-prefix commit; unchanged base on every failure; no device handles.

### SD2 — Reference cached-block verification

**Goal**: [`cached-block-verification`](../cached-block-verification/goal.md)
**Gate**: nonempty prefix plus nonempty candidate block yields the pinned
`[k,V]` row convention and complete staged state; all rows and final state
match full recompute; failure is atomic. This is reference evidence only.

### SD3 — Compiled Metal execution

**Goal**: [`speculative-verification-execution`](../../../../radix/docs/factory/speculative-verification-execution/goal.md)
**Gate**: one versioned candidate-block device operation consumes the existing
device-executor/KV-cache contracts, executes k rows on real Metal, commits only
the accepted prefix, and matches SD2. Fake-backed or MIR-only receipts do not
close this stage.

### SD4 — Context lookup integration

**Goal**: [`context-lookup-drafting`](../context-lookup-drafting/goal.md)
**Gate**: exact deterministic lookup feeds SD2/SD3, empty match falls back to a
plain target step, greedy output/cache/history/cursor/stop state is exact,
sampled acceleration rejects before work, and both regimes have honest
acceptance/overhead receipts.

### SD5 — Complete prepared prefix and product consumer

**Goals**: [`prepared-prefix-state`](../prepared-prefix-state/goal.md), then
[`prefix-reuse-consumer`](../../../../inferentia/docs/factory/prefix-reuse-consumer/goal.md)
**Gate**: Gradus can continue from a verified complete prefix state for every
admitted architecture row. Inferentia retains it within a private bounded
scope, skips the exact consumed prefix, streams the first generated token, and
records cold/warm token/text equality plus true TTFT. No fixed speedup is
promised.

### SD6 — CUDA peer qualification

**Goal**: [`speculative-decode-cuda-qualification`](../../../../radix/docs/factory/speculative-decode-cuda-qualification/goal.md)
**Gate**: persistent CUDA sessions support the required dynamic KV/state
bindings and explicit teardown; the SD0 corpora are equivalent on real CUDA;
an operator-authorized RunPod receipt uses the live CAP-02 evidence rails.
The campaign cannot close Metal-only.

## Dependency Rules

```text
SD0 contract
  -> SD1 branching
     -> SD2 reference block -> SD3 Metal execution -> SD4 lookup
     -> SD5 prepared state -> SD5 Inferentia consumer

SD3 + SD4 + SD5 -> SD6 CUDA qualification
```

- SD3 also waits for the exact interfaces delivered by device-executor M4 and
  kv-cache-decode. It extends those authorities rather than forking them.
- SD5's Inferentia consumer also waits for real arbitrary-prompt tokenization,
  Inferentia I2's planned streaming host effect, and the live monotonic clock
  seam. Its hybrid state row waits for PML MODEL-01–04 and LIB-02 receipts.
- SD6 includes missing CUDA dynamic binding and lifecycle work. It is not only
  a request to rerun the old one-shot proof.
- Paid RunPod work requires fresh operator authorization for that run.

## Scope Boundaries

### In campaign

- explicit policy and equivalence/receipt contracts;
- logical branch/commit and reference k-row verification;
- deterministic context lookup;
- compiled Metal and CUDA execution for the admitted path;
- complete logical prepared state and single-node private retention;
- cold/warm and regime-labeled equality/performance evidence.

### Outside campaign

- DFlash, MTP, or other learned/model drafter artifacts and training;
- quantized KV or activation implementation;
- continuous batching, broad scheduler redesign, or deployment;
- multi-device prefix tiers, migration, or routing (MD4D owns these);
- general kernel/power tuning beyond the operation required for exact
  candidate verification;
- cross-tenant sharing or identity-as-authorization.

These are excluded, not deferred campaign work. Adding any one changes the
completion contract and requires an explicit campaign amendment.

## First Useful Milestones

1. **Exact reference block** — SD0–SD2 establish implementable semantics.
2. **Context-assisted decode** — SD4 produces exact lookup acceleration; SD3
   supplies device speed evidence.
3. **Warm prepared prefix** — SD5 proves cold/warm identity and measures TTFT.
4. **Peer-target proof** — SD6 closes the same contracts on CUDA.

## Acceptance Criteria

- [ ] All eight named goals are `done`; no admitted unit remains optional,
      deferred, or outside a commit.
- [ ] Disabled policy preserves the named dense baseline.
- [ ] Greedy accelerated runs are token- and state-exact; sampled acceleration
      returns the declared typed reject before lookup/RNG/branch work.
- [ ] Reference, Metal, and CUDA receipts prove the same row/state contract.
- [ ] Context-reproduction and ordinary-chat receipts remain separate.
- [ ] Complete prepared state, private scope, capacity, expiry/eviction,
      release, and no-raw-key boundaries are exercised.
- [ ] Cold/warm output equality and true first-token timing are executed in
      Inferentia.
- [ ] CUDA dynamic state bindings and teardown are real-device proven, and the
      authorized RunPod receipt names its exact revisions and environment.
- [ ] Factory audits and each goal's declared validation are green.

## Settled Decisions

- The initial candidate provider is context lookup only.
- Learned/model drafters are outside this campaign.
- `generate_dense_with_stop` is the semantic baseline.
- One versioned policy defaults to disabled.
- Greedy is the only accelerated acceptance mode in this campaign. Sampled
  acceleration requires a future explicit amendment with generation/RNG
  transaction ownership and pathwise proof.
- Prepared state is complete architecture state, never KV-only.
- Gradus owns logic, Radix/Hosts own compiled execution, and Inferentia owns
  retention/authorization policy.
- Metal develops; CUDA is a required peer closeout target.
- External headline figures inform corpus design only.

## Validation

Planning-artifact closeout:

```bash
python3 ../radix/scripta/audit-factory-goal-status.py \
    --factory-root docs/factory --fail-on error
git diff --check
```

Implementation validation lives in each named goal. Broad product suites and
paid GPU runs are not planning-doc gates.

## Stop Conditions

Pause and route a need when an accelerated path cannot preserve output/state;
a public Gradus type would need a physical device handle; identity would be
used as authorization; a receipt cannot distinguish regimes or evidence
tiers; an existing device/KV campaign's contract conflicts with SD3; CUDA
would still rely on fake or one-shot evidence; or external execution needs
fresh authorization.

---

<!-- Created from radix/docs/factory/TEMPLATE.md. Status line is the audit
     authority; named goals carry implementation ledgers. -->
