# Campaign: Production ML Library

**Status**: active — PML5-GGUF Qwen3.6 invariant; GGUF-A1a/A1b implemented, GGUF-A1c integrated at main 2b3e41a, GGUF-A3 (checked packed storage + bounded tensor materialization, LIB-03) implemented at the output-checked slice tier, and MODEL-02 MoE router/expert/full-layer component surface implemented through U6 at gradus `b1ccfc8`; PML5 remains active until the Qwen3.6 invariant executes end to end
**Created**: 2026-08-08
**Mode**: routing artifact — draft/maintain; does not implement code directly
**Control-plane repo**: `/Users/ianzepp/work/faberlang/gradus`
**Participating repos**: `gradus`; `examples` for capstones; `radix`, `faber`,
and `hosts` only through named compiler and execution dependencies
**Sibling campaign**:
[`native-gpu-application-bundle`](../../../../faber/docs/factory/native-gpu-application-bundle/CAMPAIGN.md)
**Supersedes**: the production-library routing portions of
[`gradus-ml-foundation`](../gradus-ml-foundation/GOAL.md); that goal remains
the historical autograd and nanoGPT architecture source
**Lowers to**: `delivery` then `factory`
**Campaign readiness**: **READY FOR DELIVERY — PML5-GGUF-A1c SELECTED**

## Summary

Turn Gradus from a narrow static-shape proof library into Faber's
production-quality machine-learning computation library. Gradus owns the
device-neutral model semantics shared by training and inference, plus clearly
separated training-only and inference-only modules. It does not own GPU
drivers, kernel launch, application packaging, request scheduling, HTTP
serving, or deployment.

## Non-Negotiable Inference Invariant

This campaign cannot complete until a Faber package successfully runs the
hash-pinned local `Qwen3.6-35B-A3B-UD-Q4_K_M.gguf` artifact through public
`gradus:*` APIs and the accepted Faber/Radix/Hosts execution path.

`Successfully runs` means that one normal Faber package command:

1. verifies the artifact's SHA-256
   `0b21525e972670ed59e1812e170b27c26355381f0656ecc4e25617ece7dac58b`
   and byte length `22,663,387,424` before admission;
2. admits the `qwen35moe` architecture and every tensor required by the
   forward path;
3. accepts operator-supplied Unicode text, applies the artifact tokenizer and
   special-token policy, executes full-model prefill and autoregressive
   decode, and detokenizes generated tokens to text;
4. generates at least 256 new tokens for each of two distinct prompts while
   reusing one admitted model session, with weights and model state remaining
   resident and without per-token model reload, recompilation, or packet
   rebuild;
5. matches the pinned independent `llama.cpp` oracle under the campaign's
   declared token/logit comparison policy;
6. executes on both admitted single-device backends, Metal and CUDA; and
7. records the exact command, source revisions, model identity, hardware,
   backend, output, peak memory, and timing in reproducible receipts.

HTTP, request scheduling, and deployment are not part of this invariant. They
may wrap the accepted library later, but cannot substitute for it here.

## Problem

Gradus has proved explicit tensor values, compiler-generated backward
companions, losses, optimizers, attention, transformer blocks, and small
training steps. The public surface is still dominated by fixed-shape
functions such as `*_2x2`, `*_4x4`, and `*_2x8`. Its README also describes
attention and transformer work as planned while live source records a shipped
BERT-tiny slice.

Inference and training now risk growing separate tensor, tokenizer, model,
and transformer stacks. `norma:model` already contains Safetensors and GGUF
parsing that belongs with ML model representation. Gradus needs one production
campaign so application repositories can depend on a coherent library rather
than a collection of demonstrations.

## Desired End State

1. Gradus has a documented, versioned, device-neutral public API.
2. Tensor, dtype, shape, parameter, model-format, tokenizer, neural-network,
   attention, and transformer contracts are shared by training and inference.
3. Autograd, losses, optimizers, datasets, and training loops remain a
   training layer over reusable forward functions.
4. Decode state, KV cache, sampling, and generation are an inference layer
   over those same forward functions.
5. Model admission fails closed by format, architecture, dtype, quantization,
   shape, tokenizer identity, and version.
6. Supported rows have tests, examples, diagnostics, performance evidence,
   and an explicit compatibility policy.
7. One training capstone and one inference capstone consume only public
   `gradus:*` modules.
8. A separate Faber application can compile those inference calls into a
   native executable with embedded GPU kernels without Gradus learning about
   device handles or backends.
9. The non-negotiable Qwen3.6 invariant is executed and its Metal and CUDA
   receipts are current.

```text
application repository
  -> gradus:model / tokenizer / transformer / decode / sampling / cache
  -> Faber and Radix compilation
  -> host and device execution
```

## Development Posture

- **One ML library.** Do not create a parallel inference tensor, tokenizer,
  model, or transformer library while Gradus owns those concepts.
- **Clean break.** Gradus is pre-1.0. Replace proof-shaped APIs when the
  production contract is known; do not preserve numbered-shape aliases
  without a real external caller.
- **Forward functions first.** Reusable model evaluation must not depend on
  autograd. Training requests compiler-generated backward companions;
  inference calls forward and decode paths without building a gradient path.
- **Device neutral.** No CUDA, Metal, allocator, stream, command-buffer, or
  device-session value enters the public Gradus API.
- **Named production row.** Intermediate rows establish correctness, but the
  selected Qwen3.6 artifact is the campaign completion row.
- **Correctness before performance.** Tokenization, logits, gradients, state
  mutation, and deterministic sampling gate speed claims.
- **Second caller before abstraction.** Split nested module families only
  after concrete leaves or callers establish the boundary.

## Implementation Workflow

1. Lower each PML stage through `delivery` before implementation.
2. Execute delivery-sized units through `factory` with focused red-green
   proofs and Gradus's source and compile gates.
3. Use `examples` only for capstone consumers and evidence.
4. Route compiler, package, or host gaps into the sibling native-GPU
   application campaign. Do not work around them in Gradus.
5. Update this campaign and the factory index at every stage boundary.

## Scope Routing

### In campaign

- Public API charter, module DAG, naming, diagnostics, and compatibility.
- Tensor values, shapes, dtypes, layouts, parameters, and pure operations.
- Model metadata, model admission, Safetensors, admitted GGUF rows, and
  tokenizer identity.
- Neural-network primitives, attention, transformer blocks, and reusable
  forward evaluation.
- Autograd wrappers, losses, optimizers, training steps, checkpoint state,
  metrics, and reproducibility.
- Decode loop semantics, KV-cache values and mutation rules, sampling, and
  generation configuration.
- Unit, conformance, numerical, property, capstone, documentation, benchmark,
  and release gates.

### Split out

- GPU lowering, fusion, kernel generation, and backend optimization -> Radix.
- Executable assembly, embedded device artifacts, target selection, and
  application launch -> Faber native-GPU application campaign.
- Driver contexts, streams, physical allocation, and device lifecycle -> hosts.
- CLI product, HTTP API, request scheduler, continuous batching,
  authentication, observability, and deployment -> separate application repo.
- Multi-device placement and distributed execution -> existing multi-device
  campaign after the single-device library contract is stable.

## Batching And Split Policy

- **PML0: discovery-first.** Freeze ownership, module graph, support matrix,
  compatibility posture, and measured baseline before broad implementation.
- **PML1-PML5: split-on-boundary.** Split on API ownership, numerical risk,
  model-format admission, state semantics, or independent validation. Batch
  homogeneous operations after the first accepted pattern.
- **PML6-PML7: batch-by-default.** Apply accepted quality and release gates
  uniformly across the public surface and capstones.
- Never split parameter identity, tokenizer identity, model admission, KV
  mutation, checkpoint versioning, or metric definitions across units.

## Ground Truth Researched

| Fact | Authority | Treatment |
| --- | --- | --- |
| Gradus is self-contained and device-neutral | `AGENTS.md`, `README.md` | Preserve |
| Live modules include tensor, gradient, loss, optimize, NN, attention, transformer, train, and data | `src/*.fab` | Baseline, not production proof |
| Current functions are dominated by fixed proof shapes | `src/nn.fab`, `src/attention.fab`, `src/transformer.fab`, `src/train.fab` | Replace through admitted production contracts |
| Forward model composition is already shared in principle | `src/gradus.fab`, `src/transformer.fab` | Common training/inference layer |
| GGUF and Safetensors parsing currently lives in Norma | `../norma/src/model.fab` | Migrate after PML2 freezes ownership |
| The compiler generates reverse-mode companions | `gradus-ml-foundation/GOAL.md`, Radix AIR | Consume; do not duplicate |
| `llvm-host` and device execution are separate live paths | live `faber targets`, Faber package sources | Cross-campaign composition dependency |

Authority order: live Gradus source and tests; accepted Gradus contracts;
accepted compiler/package contracts; this campaign's stage receipts; examples
and historical plans.

Source snapshot used for this draft: Gradus `29d26735d0d9`, Norma
`84f27dacd6f9`, Faber `26b503a0e3bb`, Radix `a01543b06bfe`, hosts
`e066ee0ae98a`, and examples `aad199ecf07c`. PML0 must refresh these revisions,
record dirty state, and replace any drifted claim before lowering PML1.

## Related Campaign And Goal Dependency Ledger

This table is the handoff inventory for cross-campaign priority and ordering.
“Consume” means accepted evidence or contracts are prerequisites, not that this
campaign takes ownership of the older artifact.

| Related artifact | Live state on 2026-08-08 | What this campaign uses or supplies | Stage edge | Routing disposition |
| --- | --- | --- | --- | --- |
| [`gradus-ml-foundation`](../gradus-ml-foundation/GOAL.md) | Horizon 0 architecture checkpoint complete; later horizons remain described | JAX-shaped model semantics, autograd ownership, module DAG, nanoGPT forcing function | predecessor -> PML0/PML4 | Consume history; PML campaign becomes production control plane |
| [`gpu-training-lowering`](../../../../radix/docs/factory/gpu-training-lowering/CAMPAIGN.md) | active; single-device Metal/CUDA training path accepted through Stage 6 evidence | `DeviceProgram`, persistent session, generated backward, Gradus training proofs, hardware receipts | supplies PML1/PML3/PML4 and NGAB substrate | Continues independently; do not reopen accepted stages |
| [`gpu-inference-gguf`](../../../../radix/docs/factory/gpu-inference-gguf/CAMPAIGN.md) | active; GI3 compiler/prefill work in flight after GI2 | pinned GGUF/oracle contracts and accepted decoder-kernel evidence | supplies PML2/PML3/PML5 and NGAB5 | Reuse GI0-GI3 facts; re-lower GI4+ ownership into Gradus plus a separate product repo |
| [`gpu-inference-multi-device`](../../../../radix/docs/factory/gpu-inference-multi-device/CAMPAIGN.md) | active; MD3 partially accepted, physical multi-device proof pending | future placement and distributed execution consumer of stable logical cache/session semantics | PML5 + NGAB4 -> later MD stages | Downstream; not a single-device blocker |
| [`llvm-host-parity`](../../../../radix/docs/factory/llvm-host-parity/CAMPAIGN.md) | in factory; behavioral parity gaps remain, while live Faber already exposes `llvm-host` | native LLVM host ABI, link/runtime patterns, remaining semantic coverage | supplies NGAB0-NGAB3; broad parity runs independently | Consume live product path; do not wait for zero-gap parity unless a needed LLM carrier is missing |
| [`mir-gpu`](../../../../radix/docs/factory/mir-gpu/CAMPAIGN.md) | active GPU compiler architecture track | shader/device-stage driver and backend emitter foundations | supplies NGAB1-NGAB2; compiler gaps from PML route here | Continue as compiler owner, not Gradus work |
| [`mir-llvm`](../../../../radix/docs/factory/mir-llvm/CAMPAIGN.md) | parked historical authority | LLVM/NVVM design history and constraints | research input to NGAB1 | Do not revive as a competing control plane |
| [`mir-library-imports`](../../../../faber/docs/factory/mir-library-imports/goal.md) | implemented | linked `gradus:*` calls through FMIR and consumer proof | prerequisite already satisfied for PML capstones | Consume; archive status is separate housekeeping |
| [`inference-session-boundary`](../../../../faber/docs/factory/inference-session-boundary/goal.md) | proposed; metadata/session contract only | earlier Faber CLI and model-handoff boundary | informs PML2/NGAB0 and later product repo | Reconcile; do not implement its old runtime ownership literally |
| [`target-build-pipelines`](../../../../faber/docs/factory/target-build-pipelines/goal.md) | proposed; parts predate the live `llvm-host` product path | Faber emit/build/artifact ownership and build-plan concepts | supplies NGAB0/NGAB2 | Rebaseline against live targets; absorb only current clauses |
| [`runpod-gpu-verification`](../../../../radix/docs/factory/runpod-gpu-verification/goal.md) | active; harness and first card matrix exist, same-artifact proof pending | paid, ephemeral CUDA evidence path | NGAB5 local CUDA -> NGAB6 RunPod | Downstream and authorization-gated |
| [`gpu-workload-floor`](../../../../radix/docs/factory/gpu-workload-floor/goal.md) | active measurement track | workload ladder and honest capability floors | evidence input to NGAB4 and PML6 | Continue as measurement authority |
| [`agent-native-device-runtime`](../../../../radix/docs/factory/agent-native-device-runtime/goal.md) | planned pre-implementation | alternative device-resident process research | may consume PML5 and NGAB3 later | Downstream research; not a prerequisite |
| [`pytorch-session-continuation`](../../../../faber/docs/factory/pytorch-session-continuation/goal.md) | proposed proof-era continuation | older cross-entropy/training-session gaps | maps into PML4 discovery | Re-lower useful gaps into Gradus; do not extend the old runtime-local ownership |
| Inference product campaign *(not yet drafted)* | missing | CLI/server repository, request API, scheduling, streaming, operations, and mapping tuning input into Gradus generation configuration | product shell may start after PML0; execution depends on PML5 + NGAB5 | Required third campaign; PML and NGAB must not absorb it |
| RunPod deployment campaign *(not yet drafted)* | missing | image publication, provisioning, ingress, secrets, health, observability, autoscaling, and teardown | consumes NGAB6 plus inference product | Required for an operated cloud service; not a local executable blocker |

### Cross-campaign ordering constraints

```text
PML0  <->  NGAB0                 shared interface freeze; run in parallel
  |          |
PML1       NGAB1 -> NGAB2 -> NGAB3
  |                         |
PML2 + PML3              NGAB4 generic composite proof
  |          \              |
PML4         PML5 --------> NGAB5 LLM executable
  |            |              |
PML6 ---------+-----------> NGAB6 portability
  \-----------------------> PML7 + NGAB7 closeout

PML5 + NGAB4 -> multi-device continuation (separate priority lane)
```

PML4 training productization can proceed beside PML5/NGAB work after PML3.
RunPod and multi-device work are downstream evidence lanes, not prerequisites
for the first local single-device LLM executable.

## Current State

| Track | State | Next action |
| --- | --- | --- |
| Library charter | Training/autograd centered | PML0 broaden to shared ML computation |
| Tensor and math | Small static-shape proof surface | PML1 production contracts |
| Model formats | Partial support in `norma:model` | PML2 freeze ownership and migrate |
| Forward architectures | BERT-tiny-shaped source exists | PML3 admitted reusable rows |
| Training | Small SGD/MSE/static-step proofs | PML4 production training layer |
| Inference | Structural decode/cache/sampling receipts plus GGUF inspection; no full Qwen3.6 execution | PML5-GGUF complete the Qwen3.6 invariant |
| Quality and releases | Source/compile checks only | PML6 establish support and release gates |
| Capstones | Training proofs; no paired capstones | PML7 qualify both modes |

## Campaign Path

### PML0 — Charter, API map, and measured baseline

**Status**: planned — selected
**Owner**: Gradus; Faber, Radix, and hosts contribute the cross-campaign
interface.
**Source**: this campaign, `AGENTS.md`, `README.md`, `src/`, and
`gradus-ml-foundation/GOAL.md`
**Gate**: accepted module DAG; shared/training/inference ownership table;
public symbol inventory; proof-shaped API ledger; support-matrix schema;
numerical baseline; `norma:model` migration decision; and exact cross-campaign
interface packet.
**Required outputs**:
`docs/factory/production-ml-library/pml0-gradus-contract.md` and a committed
ownership amendment plus migration map in
`radix/docs/factory/gpu-inference-gguf/`; PML0 cannot close while GI4+ still
assigns model runtime or serving to the old owners.
**Batch posture**: discovery-first.
**Lowers to**: `delivery` then `factory`.

### PML1 — Tensor, dtype, shape, and parameter foundation

**Status**: planned — after PML0
**Owner**: Gradus.
**Source**: PML0, `src/math.fab`, `src/tensor.fab`, and live Radix tensor/type
capability facts.
**Gate**: admitted tensor/dtype/shape rows have stable construction,
validation, operation, error, and serialization contracts; parameters have
explicit identity and traversal; proof-only helpers are retired or admitted.
**Overlap rule**: Gradus describes mathematical values; Radix owns lowering;
hosts own physical storage.
**Batch posture**: split-on-boundary, then batch operation families.
**Lowers to**: `delivery` then `factory`.

### PML2 — Model, format, tokenizer, and checkpoint admission

**Status**: delivered/accepted — PML2 U1–U6 delivered and admitted (435ccd6, 07291d6, b392fc8, f12deaf, d6954ab/22041e6, 02fae61); the retired runtime split was deleted after the decouple (9a0295e/08d195f), and the closeout transitive-closure gate found zero live references or forwarding shims
**Owner**: Gradus; Norma participates only in the controlled source migration.
**Source**: PML0/PML1, `norma/src/model.fab`, GI0-GI2 model/oracle contracts,
and admitted legal fixtures.
**Gate**: one Safetensors row and one selected GGUF row fail closed on format,
version, architecture, dtype/quantization, offsets, shapes, and tokenizer;
accepted `norma:model` behavior migrates with no dual authority.
**Overlap rule**: Gradus owns model bytes and semantic admission; applications
own paths/configuration and hosts own physical upload.
**Batch posture**: discovery-first per format, then batch validation cases.
**Lowers to**: `delivery` then `factory`.

### PML3 — Reusable forward models and architecture rows

**Status**: active — PML3 U1–U5 historical dense/structural receipts landed (9822cfa, 5260049, 7bf9acc, 359c5f0, 92df3ff); the stage remains incomplete until the selected `qwen35moe` forward architecture executes through the PML5-GGUF invariant
**Owner**: Gradus.
**Source**: `src/nn.fab`, `src/attention.fab`, `src/transformer.fab`, accepted
GPU-training proofs, and the PML1 parameter contract.
**Gate**: NN, attention, and transformer forward functions are composable,
testable, usable with and without autograd, and qualified for one training
architecture and the selected inference architecture.
**Overlap rule**: Gradus owns semantics; backend fusion is not a public
semantic shortcut.
**Batch posture**: split by architecture or numerical oracle.
**Lowers to**: `delivery` then `factory`.

### PML4 — Production training layer

**Status**: active — PML4 U1–U6 structural receipts landed (5f98e8b, e09c79c, 9bebda9, 4b24c81, 94d8a94, fc85de7); executed convergence remains an incomplete campaign item and cannot be treated as delivered
**Owner**: Gradus.
**Source**: `src/gradient.fab`, `src/loss.fab`, `src/optimize.fab`,
`src/train.fab`, GPU-training receipts, and PML1/PML3.
**Gate**: losses, gradient calls, optimizer state, schedules, training/eval
mode, checkpoint resume, metrics, deterministic seeds, and failure behavior
compose publicly; a bounded workload converges and resumes reproducibly.
**Batch posture**: batch-by-default after one optimizer-state contract.
**Lowers to**: `delivery` then `factory`.

### PML5 — Production inference computation layer

**Status**: active — PML5 U1–U6 structural receipts landed (bdefb5a, 3b2fc9b, b1b01f1, 56e70f0, 8cf798a, 1a6abd0), GGUF-A1a/A1b inspect the real corpus, and GGUF-A3 packed-storage materialization is implemented at the output-checked slice tier (LIB-03); PML5 remains incomplete until the Qwen3.6 invariant executes end to end
**Owner**: Gradus.
**Source**: PML2/PML3, GI0-GI3 oracle and decoder contracts, and independent
token/logit fixtures.
**Gate**: decode, KV-cache, sampling, and generation configuration produce
oracle-matching tokens for the admitted model; reset, context limits,
cancellation observation points, and deterministic sampling are explicit; no
server or device handle leaks into Gradus.
The generation-configuration contract must name supported values, defaults,
validation, and deterministic mapping for at least context length, prompt
batch size, maximum generated tokens, seed, temperature, top-k, top-p, min-p,
and repetition penalty. Unsupported llama.cpp-style controls remain explicit
reject rows rather than silently ignored options.
**Overlap rule**: owns computation and logical state, not scheduling,
continuous batching, HTTP, or physical residency.
**Batch posture**: split on cache mutation, sampling, and numerical oracles.
**Lowers to**: `delivery` then `factory`.

**Mandatory Qwen3.6 continuation**:
[`pml5-general-gguf-delivery.md`](pml5-general-gguf-delivery.md) corrects the
one-row/one-block boundary through format-general GGUF artifacts, real
tokenization, packed storage, complete dense reference models, `qwen35moe`
MoE/SSM semantics, integrated KV/recurrent decode, native quantized execution,
and the exact Qwen3.6 capstone. Every unit in that delivery is mandatory.

### PML6 — Production quality, performance, and release contract

**Status**: active — PML6 U1–U5 structural quality artifacts landed (1f4f0d2, 649b2f6/29fb2fb, 43d75ce, 5a5f295, 9a2ed8b); the stage remains incomplete until those artifacts and support claims include the executed Qwen3.6 receipts
**Owner**: Gradus.
**Source**: accepted PML contracts and receipts, package metadata, and the PML0
support-matrix baseline.
**Gate**: API reference, examples, diagnostics, support matrix, compatibility
policy, benchmark method, tolerances, regression corpus, package metadata, and
release checklist agree with live behavior.
**Batch posture**: batch-by-default.
**Lowers to**: `delivery` then `factory`.

### PML7 — Training and inference capstones

**Status**: planned — final
**Owner**: Gradus for library acceptance; examples for capstones; Faber/hosts
for NGAB cross-backend receipts.
**Source**: accepted PML1-PML6 and NGAB5/NGAB7 receipts.
**Gate**: one training app and
`exempla/qwen36-35b-inference` consume only public Gradus; CPU/reference
results pass; the inference capstone satisfies the non-negotiable Qwen3.6
invariant on Metal and CUDA; clean-install receipts pin package and toolchain
versions.
**Batch posture**: split only by capstone and backend receipt.
**Lowers to**: `delivery` then `factory`.

## Dependency Rules

1. PML0 freezes the Gradus-to-compiler interface before either campaign
   generalizes it.
2. PML1 is the common prerequisite for PML2-PML5.
3. PML3 forward functions must not require PML4 training machinery.
4. PML5 cannot complete until the sibling executable campaign supplies the
   physical-residency, Metal, and CUDA receipts required by the Qwen3.6
   invariant.
5. Model-format code moves from Norma only after PML2 names the destination
   API and proves accepted and rejected fixture equivalence.
6. Compiler limitations become sibling-campaign needs, not Gradus workarounds.
7. Model execution ownership is fixed: Gradus owns semantics, Radix owns
   lowering, Faber owns package/run composition, and Hosts owns physical
   execution. The retired runtime split is not a dependency.

## First Useful Milestones

1. **Library contract**: PML0 publishes the module and support map.
2. **Portable evaluation**: PML1-PML3 load one model and match a CPU oracle.
3. **Useful ML library**: PML4-PML5 expose stable training and full Qwen3.6
   generation.
4. **Product-ready dependency**: PML6-PML7 provide versioned packages and
   paired clean-install capstone receipts, including the Qwen3.6 invariant.

## Acceptance Criteria

- [ ] Every stage has a source, gate, batching posture, and lowering route.
- [ ] Shared, training, inference, compiler, host, and product ownership are
      unambiguous.
- [ ] PML0 is ready to lower into a delivery spec.
- [ ] Proof work is consumed without being promoted to production evidence.
- [ ] Release/version review occurs at PML6 and PML7.
- [ ] The exact Qwen3.6 invariant is executed on Metal and CUDA through one
      public-Gradus Faber capstone.
- [ ] Every PML stage with an open executed gate remains active until that gate
      is satisfied.
- [ ] No stage authorizes deployment, model acquisition, paid GPU use, or
      production mutation.

## Validation

```bash
python3 ../radix/scripta/generate-factory-readme.py --factory-root docs/factory
python3 ../radix/scripta/generate-factory-readme.py --factory-root docs/factory --check
git diff --check -- docs/factory/production-ml-library docs/factory/README.md
```

The shared status-audit script is hard-bound to Radix's `docs/factory` and has
no `--factory-root`. The sibling README generator uses the same status parser,
so `--check` is the current Gradus gate. PML0 must add or select a
Gradus-scoped audit entrypoint before claiming the full status-audit gate.

Implementation stages use `./scripta/check-source` and
`./scripta/check-compile`; cross-backend, performance, and release commands
must be named by their delivery specs.

## Settled Decisions

- The production inference row is the hash-pinned local
  `Qwen3.6-35B-A3B-UD-Q4_K_M.gguf` artifact.
- The public inference capstone is `exempla/qwen36-35b-inference`.
- The exact tensor-shape representation may be lowered by its owning delivery
  unit, but it may not change the invariant or remove any required model row.

## Stop Conditions

Pause and route a need when a public API requires a backend/device handle; a
shape or dtype cannot be represented truthfully; moving `norma:model` would
strand callers or create dual authority; a model/tokenizer row lacks a pinned
legal fixture and oracle; performance begins before correctness; or work would
implement a server, deployment, or paid external GPU operation here.
