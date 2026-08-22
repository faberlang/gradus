# SD0 contract handoff

Status: **frozen for downstream consumption**. Downstream goals import these
fields; they do not reinterpret them.

Oracle: `generation.generate_dense_with_stop`
([baseline.md](baseline.md)). Disabled `AccelerationPolicy` is the
constructor default and the legacy `1.0.0` decode. There is no parallel
fast-path generate API in `src/`.

## Consumed fields by downstream goal

### kv-cache-branching (SD1)

Import `gradus:speculative`. Wrap, do not recompute, greedy acceptance.

| Field | Authority | Meaning |
| --- | --- | --- |
| `GreedyAcceptance.accepted_prefix_length()` | `src/speculative.fab` | accepted candidate count `n` |
| `GreedyAcceptance.divergence_index()` | same | first mismatch index, or `-1` if none |
| `first_divergence(target_ids, candidate_ids)` | same | pure greedy oracle |
| `acceptance_equal` | same | value equality |
| baseline route | [baseline.md](baseline.md) | `generate_dense_with_stop` k=1 stream |

Do not invent a second acceptance length. Sampled admission stays on
`admit_greedy` (typed reject) and is out of SD1 scope.

### cached-block-verification (SD2)

Import `gradus:speculative` for the provider seam and the same first-divergence
oracle SD1 wraps.

| Field | Authority | Meaning |
| --- | --- | --- |
| `ProviderRequest.prompt` / `.history` / `.block_size` | `src/speculative.fab` | tokenized context, accepted history, authorized `k` |
| `construct_request(..., min_block, max_block)` | same | `min_block`/`max_block` come from `AccelerationPolicy` |
| `ProviderResult` `candidates` / `no_draft` | same | candidate ids + provenance, or empty proposal |
| `CandidateProvenance.source` | same | `"context_lookup"` only |
| `first_divergence` | same | row-to-candidate accept/reject against target ids |

Block evaluation itself is SD2. Candidate search is not.

### context-lookup-drafting (SD3 / SD4 in the campaign path)

Implements lookup against the frozen policy mode and seam. Scores against the
checked-in corpus.

| Field | Authority | Meaning |
| --- | --- | --- |
| `AccelerationMode` `context_lookup` | `src/generation.fab` `acceleration_context_lookup()` | the only enabled mode |
| `AccelerationPolicy.version` / `.min_block` / `.max_block` | same | policy `1.0.0`; bounds ≥ 1 |
| `GenerationConfig.acceleration` | same | one field; wire `1.1.0` 13-part |
| `admit_greedy` | `src/speculative.fab` | sampled request → `SampledAccelerationRejected` before lookup |
| provider seam | same | `construct_request` / `ProviderResult` / provenance |
| corpus rows | [corpus/](corpus/) | regime, prompt ids, disabled-policy wire, seed, stop, baseline stream |

Empty lookup is `no_draft()`, not a second generate route.

### prepared-prefix-state (SD5)

Binds identity to the corpus rows and carries evidence in `gradus:receipt`.

| Field | Authority | Meaning |
| --- | --- | --- |
| `model.id` / `model.version` / `model.config` | corpus JSON | cache identity bindings |
| `tokenizer.id` | corpus JSON | tokenizer identity binding |
| `prompt_ids` | corpus JSON | exact prefix tokens |
| `Receipt.regime` | `src/receipt.fab` | `context-reproduction` \| `ordinary-chat` |
| `Receipt.backend` / `.warmth` | same | `reference`/`compiled`/`metal`/`cuda` and `cold`/`warm` |
| `Receipt.equivalence` | same | required before TTFT/throughput |

A receipt cannot report throughput without an equivalence verdict.

### speculative-verification-execution and speculative-decode-cuda-qualification

Device goals label evidence with the receipt regime and evidence pair; they
do not mint a second vocabulary.

| Field | Authority | Meaning |
| --- | --- | --- |
| `regime_context_reproduction()` / `regime_ordinary_chat()` | `src/receipt.fab` | workload class |
| `backend_reference()` / `backend_compiled()` / `backend_metal()` / `backend_cuda()` | same | execution tier |
| `warmth_cold()` / `warmth_warm()` | same | cache residency |
| `evidence(receipt)` | same | `"backend:warmth"` |
| `Receipt.policy` / `.policy_version` / `.block_size` | same | disabled or `context_lookup`, policy `1.0.0` |
| `Receipt.accepted` / `.rejected` / `.first_divergence` / `.equivalence` | same | token-level result |

Metal receipts use `backend=metal`. CUDA qualification uses `backend=cuda`.
Neither backend may claim speed without `equivalence`.

## Parallel fast-path check

Grep of `src/**/*.fab` generate entry points (2026-08-22):
`generate_with_stop`, `generate_cancelled`, `generate_cancelled_with_stop`,
`generate_dense`, `generate_dense_with_stop`. No speculative, draft, or
lookahead generate API exists. Disabled policy must keep using
`generate_dense_with_stop`.
