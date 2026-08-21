# Campaign: Speculative Decode And Prefix Reuse

**Status**: planned — drafted 2026-08-21 from the operator-forwarded RTX 3090 DFlash2 post; no stage lowered or implemented yet
**Created**: 2026-08-21
**Mode**: routing artifact — draft/maintain; does not implement code directly
**Control-plane repo**: `/Users/ianzepp/work/faberlang/gradus`
**Participating repos**: `gradus` (decode, cache, sampling, generation semantics); `inferentia` (prefix-reuse consumer evidence); `radix` and `hosts` only through named compiler and device dependencies
**Source**: operator-forwarded X post (2026-08-21) on `syv-ai/qwen38-27b-rtx3090`; GitHub repo verified live the same day
**Related**: [`production-ml-library`](../production-ml-library/CAMPAIGN.md) (owns the decode/cache/generation contracts this campaign accelerates); [`inferentia`](../../../../inferentia/docs/factory/inferentia/CAMPAIGN.md) (serving consumer); radix `runpod-gpu-verification` (paid CUDA evidence lane)
**Lowers to**: `delivery` then `factory`
**Campaign readiness**: READY FOR ROUTING ONLY — SD0 is the entry stage when the operator starts this campaign

## Summary

Accelerate Gradus decode by admitting multi-token verification, context-sourced
drafting, and cross-request prefix reuse as lossless, device-neutral Gradus
semantics — the techniques behind the RTX 3090 Qwen3.8-27B results — with
Metal as the development backend and CUDA as a peer target qualified through
RunPod enterprise-GPU mass testing.

## Source Post (claims, not repo truth)

The operator forwarded an X post (2026-08-21) describing a 24 GB RTX 3090
running Qwen3.8-27B at ~381 tok/s single-request on document-reproduction
tasks (~133 tok/s on ordinary chat), via: speculative decoding with a
DFlash2 block-diffusion drafter, lookup-augmented drafting that fills extra
draft positions from prompt context, 16-token verification blocks with 15/16
acceptance, prefix caching (22.4 s → 0.56 s TTFT on a repeat question against
a ~25K-token document), and quantized KV/weights/activations. The GitHub repo
`syv-ai/qwen38-27b-rtx3090` was checked live on 2026-08-21 and its README
matches these numbers and knobs (`SPEC=dflash2`, `DFLASH_TOKENS=15`,
`PREFIX_CACHE=1`). The DFlash2 paper (arXiv:2602.06036) was not read directly;
it is cited here only as reported.

Durable transferable ideas — independent of NVIDIA/vLLM kernel work:

1. **Verification block length is a free parameter.** Scoring k draft tokens
   costs roughly one target forward pass, so acceptance rate converts directly
   into throughput.
2. **Draft positions can come from anywhere cheap** — a draft model, or the
   prompt itself when the answer quotes, edits, or extracts context.
3. **Prefix reuse converts repeat-prompt prefill into near-zero TTFT.**
4. **Regime honesty.** The headline number holds only when answers are
   near-verbatim from context; ordinary chat is a different regime and must be
   reported as one.

## Problem

Gradus decode is strictly one token per step. `generation.fab` advances
`generate`/`generate_with_stop`/`generate_cancelled*` (lines 691–706) through
`_prefill` (622) and `_decode_one` (632); `decode.fab` exposes
`construct_decoder` (365), `decode_data` (458), and `decode_cached` (511) —
all single-token steps. A search of `gradus/src` on 2026-08-21 found no
speculative decoding, drafting, or lookahead anywhere. No cross-request cache
reuse exists in gradus or inferentia. Every generated token therefore pays a
full forward pass, and every request re-prefills shared prompts from scratch —
exactly the costs the source post removes.

The building blocks exist: `cache.fab` already keys cache identity on the
exact token prefix (lines 255, 543–558) and carries `KvDtype` Q8_0 (block 32)
and Q4_K (block 256) rows; `sampling.fab` already has greedy argmax (`max`,
line 201) and seeded `sample` (228) on which acceptance rules can be defined.

## Desired End State

1. The decode loop can verify k draft tokens in one target forward pass,
   accept the matching prefix, and roll the KV cache back to the accepted
   prefix on rejection — as public, device-neutral Gradus semantics.
2. A lookup drafting policy fills draft positions from prompt/context tokens
   with no new model weights, giving measured multi-x throughput on
   context-reproduction workloads (quoting, editing, extraction) while never
   regressing ordinary-chat decode beyond a bounded overhead.
3. Cross-request prefix reuse, keyed by the existing cache identity, lets a
   served second question against an already-prefilled document skip re-prefill,
   with warm-cache TTFT receipts in inferentia.
4. All of the above is lossless: under identical `GenerationConfig` and seed,
   the emitted token stream matches the non-accelerated decode loop.
5. Receipts exist on Metal (development backend) and CUDA (peer target),
   including RunPod enterprise-GPU mass testing; the campaign cannot close
   Metal-only.
6. Acceleration is explicit `GenerationConfig` surface — supported values,
   defaults, validation, and reject rows per the PML5 generation-configuration
   contract — never a silent behavior change.

## Non-Negotiable Correctness Invariant

This campaign cannot complete while any accelerated path emits a token stream
that differs from the plain decode loop under the same configuration. Greedy
acceptance must match the plain loop's tokens exactly on the regression
corpus; any sampled acceptance rule must be admitted only with an equivalence
proof under pinned seeds. Prefix reuse must produce the same tokens a cold
cache would. Every throughput or TTFT receipt is regime-labeled
(context-reproduction vs ordinary chat); unlabeled headline numbers are a
campaign defect.

## Development Posture

- **Metal develops, CUDA qualifies.** Metal is the current development and
  test backend; CUDA is an admitted peer target with live host support
  (`hosts` `cuda_host.rs`, `cuda_launch_adapter.rs`, `cuda-tier-f-proof`;
  the PML Qwen3.6 invariant itself requires both backends). Full CUDA
  qualification of this stack lands after core Gradus stability, through
  SD5.
- **RunPod is the mass-test lane.** Operator-confirmed RunPod accounts provide
  enterprise-GPU mass testing. Every RunPod execution is operator-authorized
  evidence, never a default gate.
- **Semantics, not kernels.** Gradus owns verification/acceptance/rollback and
  reuse semantics. CUDA graphs, int8 tensor-core GEMMs, fused verification
  kernels, and power tuning are radix/hosts lowering work, routed out.
- **Lossless before fast.** Token-stream equivalence gates every speed claim.
- **One decode surface.** Acceleration extends `decode`/`generation`/`cache`
  contracts owned by the PML campaign; no parallel fast-path API fork.

## Implementation Workflow

1. Lower each stage through `delivery` before implementation.
2. Execute delivery-sized units through `factory` with red-green proofs and
   `./scripta/check-source` / `./scripta/check-compile`.
3. Route compiler or device gaps to the owning campaigns (radix MIR-GPU,
   hosts, NGAB); do not work around them in Gradus.
4. Update this campaign's stage statuses at every stage boundary.

## Scope Routing

### In campaign

- Verification-block semantics, acceptance rules, KV rollback, and their
  `decode`/`generation`/`cache` contracts and proofs.
- Lookup/context drafting as a weightless drafting policy.
- Cross-request prefix reuse semantics and the inferentia consumer receipt.
- Regime-labeled measurement method, baseline, and receipts.
- CUDA and RunPod qualification of the above.

### Split out

- Kernel-level acceleration (CUDA graphs, int8 GEMMs, fused verify kernels,
  quantized activations) → radix/hosts lowering campaigns.
- Quantized-KV long-context rows (KVarN-style 4-bit/2-bit) → PML5-GGUF
  continuation; `cache.fab` already owns `KvDtype` and its flash-attention
  blocker. Do not duplicate here.
- Model-drafter speculative decoding (MTP / DFlash2 draft weights) → separate
  future campaign once SD2/SD3 establish the drafting-policy seam and an
  admissible draft-model row exists with a pinned legal fixture and oracle.
- Continuous batching, request scheduling, HTTP serving → inferentia product
  scope.
- Multi-device placement → existing multi-device campaign.

## Batching And Split Policy

- **SD0: discovery-first.** Freeze contracts, acceptance rule, measurement
  method, and baseline before implementation.
- **SD1–SD3: split-on-boundary** — cache mutation, decode-loop semantics, and
  drafting policy are separate risk boundaries; batch homogeneous proof rows
  after each first accepted pattern.
- **SD4–SD5: batch-by-default** after their first receipts.

## Ground Truth Researched

| Fact | Authority | Treatment |
| --- | --- | --- |
| Decode is single-token-per-step; no speculative/draft/lookahead code exists | `src/generation.fab` 601–775, `src/decode.fab` 365–511; search 2026-08-21 | The gap this campaign fills |
| Cache identity keys on exact token prefix; empty-prefix segment defined | `src/cache.fab` 47–71, 255, 543–558 | Reuse foundation; consume, do not fork |
| `KvDtype` Q8_0/Q4_K rows exist; quantized-V blocked on flash-attention family | `src/cache.fab` 626–749 | Owned by PML5-GGUF; out of scope here |
| Greedy argmax and seeded sampling exist | `src/sampling.fab` 144–328 | Acceptance-rule substrate |
| Generation-config explicit contract (values, defaults, reject rows) | PML5 gate in `production-ml-library/CAMPAIGN.md` | Acceleration config must obey it |
| Inferentia consumes `gradus:*` for admit/tokenize/generate (provider ruling 2615e6a9) | `inferentia/docs/factory/inferentia/CAMPAIGN.md` | SD4 consumer; no `faber-runtime` revival |
| CUDA host support is live in hosts; Qwen3.6 invariant requires Metal and CUDA | `hosts` cuda sources; PML non-negotiable invariant | Peer-target posture, not aspiration |
| RunPod accounts exist for enterprise-GPU mass testing | Operator statement 2026-08-21; radix `runpod-gpu-verification` goal | Authorization-gated evidence lane |
| RTX 3090 recipe numbers and knobs | X post 2026-08-21; `syv-ai/qwen38-27b-rtx3090` README (web-checked 2026-08-21) | External claims — technique authority only, never a gradus receipt |

Source snapshot for this draft: gradus `c67f55231018`, inferentia
`3c7211d35963`, radix `f9dd3c14563c` (all clean at snapshot). SD0 must refresh
these revisions before lowering.

## Current State

| Track | State | Next action |
| --- | --- | --- |
| Verification contracts and baseline | Absent | SD0 discovery |
| KV rollback / prefix pin | Absent (identity keying exists) | SD1 after SD0 |
| Batched verification loop | Absent | SD2 after SD1 |
| Lookup drafting | Absent | SD3 after SD2 |
| Cross-request prefix reuse | Absent | SD4 after SD1 (parallel with SD2/SD3) |
| CUDA / RunPod qualification | CUDA target live; no decode-acceleration receipts | SD5 after SD2–SD4 |

## Campaign Path

### SD0 — Contracts, acceptance rules, and measured baseline

**Status**: planned — entry stage
**Owner**: Gradus.
**Source**: this campaign, `src/decode.fab`, `src/generation.fab`,
`src/cache.fab`, `src/sampling.fab`, `docs/benchmark-method.md`.
**Gate**: accepted decode-acceleration contract — verification-block
semantics, acceptance rule (greedy exact-match first; sampled rule only with
an equivalence proof), rollback semantics, drafting-policy seam,
`GenerationConfig` surface with defaults and reject rows; a regime-labeled
measurement method with two corpora (context-reproduction and ordinary chat);
and baseline tok/s + TTFT receipts for the current loop on Metal.
**Batch posture**: discovery-first.
**Lowers to**: `delivery` then `factory`.

### SD1 — KV rollback and prefix-pin primitives

**Status**: planned — after SD0
**Owner**: Gradus.
**Source**: SD0 contract; `src/cache.fab` identity keying.
**Gate**: cache can be trimmed to an accepted prefix and pinned for reuse with
exact identity round-trip preserved; proba proofs for rollback/rejection and
pin/unpin paths.
**Batch posture**: split-on-boundary.
**Lowers to**: `delivery` then `factory`.

### SD2 — Batched multi-token verification in the decode loop

**Status**: planned — after SD1
**Owner**: Gradus.
**Source**: SD0/SD1; `src/decode.fab`, `src/generation.fab`.
**Gate**: the loop scores k draft tokens in one forward pass, accepts the
matching prefix, rolls back on rejection, and emits tokens that match the
plain loop exactly on the regression corpus under greedy acceptance with
oracle drafts; no throughput regression at k=1. Speed gates arrive with SD3.
**Batch posture**: split-on-boundary.
**Lowers to**: `delivery` then `factory`.

### SD3 — Lookup-augmented drafting

**Status**: planned — after SD2
**Owner**: Gradus.
**Source**: SD2 seam; source-post technique 2.
**Gate**: a weightless drafting policy fills draft positions from
prompt/context; measured multi-x throughput on the context-reproduction
corpus and bounded overhead on the chat corpus, both regime-labeled; greedy
token-stream equivalence preserved; acceptance-rate receipts recorded.
**Batch posture**: split-on-boundary, then batch policy variants.
**Lowers to**: `delivery` then `factory`.

### SD4 — Cross-request prefix reuse

**Status**: planned — after SD1; may run parallel with SD2/SD3
**Owner**: Gradus semantics; inferentia consumer evidence.
**Source**: SD1 pin primitive; inferentia campaign.
**Gate**: a second question against an already-prefilled long document reuses
pinned cache; warm-vs-cold TTFT receipt in inferentia; warm token stream
identical to cold; no server or scheduler code enters Gradus.
**Batch posture**: batch-by-default after first receipt.
**Lowers to**: `delivery` then `factory`.

### SD5 — Cross-backend qualification: Metal, CUDA, RunPod

**Status**: planned — final; opens after SD2–SD4 land on Metal
**Owner**: Gradus contracts; radix/hosts execution path; RunPod evidence
operator-authorized.
**Source**: SD2–SD4 receipts; PML Qwen3.6 dual-backend invariant; radix
`runpod-gpu-verification`.
**Gate**: the SD0 corpora and equivalence proofs are green on CUDA through the
accepted execution path; RunPod enterprise-GPU mass-test receipts recorded
(operator-authorized); campaign cannot close Metal-only.
**Batch posture**: batch-by-default.
**Lowers to**: `delivery` then `factory`.

## Dependency Rules

1. SD0 freezes contracts and baseline before any implementation stage.
2. SD1 rollback is a hard precondition for SD2 verification and SD4 reuse.
3. SD4 depends only on SD1 and may proceed in parallel with SD2/SD3.
4. SD3 establishes the drafting-policy seam before any model-drafter campaign
   is drafted; that campaign is outside this one.
5. Every implementation stage carries the losslessness gate; a stage cannot
   close on throughput alone.
6. Compiler or device limitations become sibling-campaign needs, never Gradus
   workarounds.
7. RunPod and any paid GPU execution requires operator authorization per use.

## First Useful Milestones

1. **Lossless fast decode (SD0–SD3)**: multi-x context-reproduction
   throughput on Metal with token-exact greedy equivalence.
2. **Warm-cache TTFT (SD4)**: repeat-question prefill collapse, evidenced in
   inferentia.
3. **Peer-target proof (SD5)**: same corpus green on CUDA plus RunPod
   enterprise receipts.

## Acceptance Criteria

- [ ] Every stage has a source, gate, batching posture, and lowering route.
- [ ] SD0 is the named entry stage and is grounded in live source.
- [ ] The losslessness invariant is executed at every implementation stage,
      not asserted.
- [ ] All throughput/TTFT receipts are regime-labeled; the source post's
      numbers never appear as Gradus claims.
- [ ] CUDA and RunPod receipts exist; the campaign does not close Metal-only.
- [ ] No stage authorizes serving, scheduling, deployment, paid GPU use
      without operator authorization, or kernel work inside Gradus.

## Validation

```bash
python3 ../radix/scripta/audit-factory-goal-status.py \
    --factory-root docs/factory --fail-on error
./scripta/check-source
./scripta/check-compile
```

(`./scripta/check-factory-goal-status` is the native launcher for the same
audit; it requires the released faber binary.) Implementation stages add the
measurement commands SD0 pins; cross-backend and RunPod commands are named by
their delivery specs.

## Settled Decisions

- Metal is the development backend; CUDA is a peer target extended to full
  support once core Gradus stability is in place (operator, 2026-08-21).
- RunPod accounts exist and are the enterprise-GPU mass-test lane, always
  operator-authorized (operator, 2026-08-21).
- Model-drafter speculative decoding is out of this campaign's admitted
  scope; SD3's drafting-policy seam is the handoff point.
- The source post's absolute numbers are technique evidence, never Gradus
  targets or receipts.

## Open Questions

1. **Sampled acceptance rule.** Default: greedy exact-match only in the first
   contracts; a rejection-sampling rule is admitted only with a seeded
   equivalence proof. Decider: SD0 delivery.
2. **Verification block size default.** Default: measured by SD0 across k ∈
   {4, 8, 16}; the post's 16 informs the sweep, not the answer. Decider: SD0
   delivery.
3. **Reuse pin scope.** Default: gradus owns pin/identity semantics, inferentia
   owns request-to-pin matching. Decider: SD4 delivery.

## Stop Conditions

Pause and route a need when: a public Gradus API would need a device handle;
an acceptance or reuse semantic cannot be made lossless; measurement cannot
separate regimes honestly; a CUDA execution gap is actually a compiler/host
limitation; or any stage would trigger paid GPU use, deployment, or external
effects without operator authorization.
