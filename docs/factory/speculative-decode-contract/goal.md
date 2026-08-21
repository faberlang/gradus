# GOAL: speculative-decode-contract — explicit, lossless acceleration policy over the dense baseline

**Status**: active — 5/7 units landed (U1–U5 on gradus main); U6 next; U7 gated on U6. Lowered to [delivery.md](delivery.md), 7 units, 2026-08-21.
**Created**: 2026-08-21
**Campaign:** `speculative-decode`
**Source:** speculative-decode campaign lowering and the 2026-08-21 live-code audit
**Repos:**
- primary: `gradus/` — `src/generation.fab`, `src/decode.fab`, `src/sampling.fab`, `src/model/dense.fab`, co-located `.proba`, and the campaign-owned corpus/receipt documentation
- evidence only (no writes): `inferentia/`, `radix/`, `hosts/`
**Related:**

| Artifact | Relationship |
| --- | --- |
| `../kv-cache-branching/goal.md` | Supplies the immutable all-layer checkpoint and branch commit primitive used by an accelerated dense loop |
| `../speculative-decode/CAMPAIGN.md` | Parent routing artifact; this goal lowers SD0 only |
| `../production-ml-library/CAMPAIGN.md` | Existing dense generation, cache, sampling, and GenerationConfig authority |

---

## Invariant

`generate_dense_with_stop` remains the canonical non-accelerated baseline. An
acceleration request is explicit, versioned, and disabled by default; an
admitted path emits the same token stream as that baseline under the same
model, prompt, `GenerationConfig`, stop policy, and seed. This campaign admits
accelerated greedy generation only. Any sampled acceleration request fails
closed with a typed reject; it never silently changes sampling or falls back
while claiming acceleration.

## Problem

The current dense route is the only cache-aware generation baseline:
`generation.generate_dense_with_stop` prefills the dense cache and advances
with `dense.decode_step` (`src/generation.fab:775-812`). The plain generation
route uses `decode.decode_data` for each next token without KV state
(`src/generation.fab:691-740`), so it is not a suitable equivalence baseline
for speculative work.

`GenerationConfig` currently has exactly nine fields and a `1.0.0` wire shape
(`src/generation.fab:185-428`), with no acceleration policy. There is no live
lookup, draft, speculative, or lookahead policy in `src/`. The sampling
surface has greedy argmax plus seeded stochastic sampling
(`src/sampling.fab:195-235`), and the stochastic draw advances explicit RNG
state (`src/sampling.fab:556-569`). Accepting a draft token without a target
probability/correction contract therefore cannot claim pathwise-identical
sampling.

The parent campaign also requires measurements to distinguish
context-reproduction workloads from ordinary chat. No checked-in corpus or
receipt schema currently binds those regimes to a baseline, policy version,
seed, and token-equivalence result.

## Proposal

1. Freeze `generate_dense_with_stop` as the named baseline, including its
   current prompt/history and stop-policy semantics. The baseline captures
   the initial next-token logits from dense prefill and then the one-token
   `dense.decode_step` loop; prompt tokens are not silently added to the
   generation repetition-penalty history.
2. Add one typed `AccelerationPolicy` carried by the versioned generation
   configuration. Its admitted modes are `disabled` and `context_lookup`.
   `disabled` is the constructor default and is the only behavior selected by
   the existing configuration wire. Unknown policy versions, modes, fields,
   block sizes, or sampling modes reject.
3. Freeze a candidate-provider interface for the sole admitted initial mode,
   `context_lookup`. It receives tokenized prompt context, accepted generation
   history, and a requested block size and returns candidate ids plus
   provenance or an explicit no-draft result. The lookup goal owns the search
   policy and implementation.
4. Greedy acceptance is admitted only after exact first-divergence comparison
   against target logits. A requested sampled acceleration returns a typed
   reject before a speculative branch is created. A future campaign amendment
   may admit sampling only after it names generation/RNG transaction ownership
   and proves pathwise identity.
5. Every performance receipt names one of two regimes: `context-reproduction`
   or `ordinary-chat`. A checked-in corpus binds prompt ids, model/tokenizer
   identity, baseline token stream, configuration, seed, and expected stop
   behavior. Receipts report policy/version, block size, accepted and rejected
   counts, first divergence, equivalence, TTFT, throughput, backend, and
   regime. The source post's headline numbers are not Gradus targets.

### Non-goals

- No model-based drafter, DFlash/MTP weights, or external draft service.
- No physical device handles, residency, CUDA graphs, fused kernels, quantized
  activations, or backend-specific scheduling in Gradus.
- No serving, continuous batching, HTTP, request matching, or prefix-store
  ownership; the inferentia consumer owns request-to-prefix selection.
- No quantized KV execution. `KvDtype` descriptors are not evidence that
  `KVCache` currently stores quantized rows (`src/cache.fab:351-362`,
  `394-434`, `630-749`).
- No change to the nine existing generation controls except the one explicit
  acceleration-policy field and its versioned wire migration.

## Units (lowering sketch — refine via `$delivery`)

| Unit | Scope | Depends on | Done when | Validation | Hand evidence |
| --- | --- | --- | --- | --- | --- |
| 1. Dense baseline oracle | Document and pin `generate_dense_with_stop` as the baseline, including logits/token alignment, stop policy, prompt/history treatment, and k=1 behavior. | — | A reviewer can reproduce the named baseline and every later equivalence receipt points to it. | Focused dense/generation `.proba` rows; `./scripta/check-source`; `./scripta/check-compile`. | none |
| 2. Versioned acceleration policy | Add one explicit `AccelerationPolicy` value to the generation configuration boundary; define `disabled` default, `context_lookup` mode, versioning, round-trip, unknown-value rejection, and migration of the existing wire. | 1 | Old configuration selects disabled behavior; new policy values round-trip; malformed or unsupported values reject before generation. | GenerationConfig/proba serialization, default, boundary, and reject rows; focused `faber test`; source/compile gates. | none |
| 3. Candidate-provider seam | Define the provider input/output, provenance, no-draft result, and purity requirements without implementing context search. | 1, 2 | The context-lookup goal can implement one interface without changing generation or cache contracts. | Type/wire fixtures, invalid block-size rows, source/compile gates. | none |
| 4. Acceptance contract | Freeze greedy first-divergence semantics and reject sampled acceleration before branch creation. Record the future proof obligations without admitting that mode. | 1, 2, 3 | Every downstream goal has one greedy acceptance oracle; sampled requests return the same typed reject and never consume RNG or mutate history/state. | Greedy oracle fixtures, sampled reject fixtures, first-divergence rows, unchanged seed/history checks. | none |
| 5. Regime corpus and receipt schema | Check in the two named corpus regimes and a versioned receipt shape binding baseline, policy, seed, model/tokenizer, token streams, state comparison, acceptance counts, timing, backend, and equivalence. | 1–4 | Each receipt is independently classifiable and cannot report throughput without an equivalence result. | Corpus integrity check, receipt schema round-trip/negative rows, `git diff --check`, source/compile gates. | none |
| 6. Contract handoff audit | Prove disabled policy preserves the baseline boundary and publish exact handoffs to branching, cached-block, lookup, prepared-state, and device goals. Do not implement those goals here. | 1–5 | No downstream goal must reinterpret policy, sampler, corpus, or receipt fields; no parallel fast-path API exists. | Dense disabled-policy regression, cross-goal field/link audit, factory audit. | none |

## Validation

The closeout gate is the unit validations above plus:

```bash
python3 ../radix/scripta/audit-factory-goal-status.py \
    --factory-root docs/factory --fail-on error
./scripta/check-source
./scripta/check-compile
```

The focused `.proba` suites must execute through the Gradus-supported test
route. A compile-only or receipt-shaped artifact does not prove token
equivalence. Backend and paid RunPod receipts are supplied by their owning
execution paths and remain regime-labeled; this goal does not fabricate them.

## Ledger

| Unit | Status | Seat | Receipt | Notes |
| --- | --- | --- | --- | --- |
| 1 | done | hand (a70d341f cycle-1) | `1147ede` | pinned dense baseline oracle |
| 2 | done | hand | `ce08816` | versioned AccelerationPolicy wire |
| 3 | done | hand | `9aeb6de` | candidate-provider seam (`gradus:speculative`) |
| 4 | done | hand | `64513a9` | greedy acceptance contract + typed reject |
| 5 | done | hand (a70d341f, resumed after drop) | `d5542fc` | `gradus:receipt` leaf; Mind re-ran closeout 2026-08-21: 8 passed, 0 failed |
| 6 | pending | — | — | two-regime corpus + integrity check |
| 7 | pending | — | — | disabled-policy regression + handoff + closeout (gated on 6) |

## Open questions

1. **Policy wire nesting.** Default: bump the generation configuration wire
   version and carry one versioned policy field with an unambiguous encoding;
   legacy `1.0.0` decodes to `disabled`. The delivery spec chooses the exact
   escaping/field representation without adding separate acceleration knobs.
2. **Lookup tie-break.** Default: choose the longest exact contiguous context
   match, then the earliest source position; equal candidates preserve source
   order. The delivery spec may change this only with a corpus oracle.
3. **Receipt timing owner.** Default: Gradus defines semantic fields and
   equivalence; inferentia/radix/hosts provide backend timing and execution
   receipts through their own authorized paths.

---

<!-- Created from radix/docs/factory/TEMPLATE.md. Status line is the audit
     authority; ledger phase table drives completion %. -->
