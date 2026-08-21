# Campaign: MLX Model Bundle Support

**Status**: planned — high-level routing grounded; MLX0 is the first mandatory stage to lower
**Created**: 2026-08-21
**Mode**: routing artifact — draft/maintain; does not implement code directly
**Source**: operator request to support MLX model artifacts in Gradus alongside GGUF
**Control-plane repo**: `/Users/ianzepp/work/faberlang/gradus`
**Participating repos**: `gradus`; `radix` and `hosts` only through existing compiled-execution contracts; `examples` only if a public consumer capstone is required
**Related**: [`production-ml-library`](../production-ml-library/CAMPAIGN.md); [`native-gpu-application-bundle`](../../../../faber/docs/factory/native-gpu-application-bundle/CAMPAIGN.md)
**Lowers to**: `delivery` then `factory`
**Campaign readiness**: **READY FOR DELIVERY — MLX0 SELECTED**

## Summary

Add fail-closed support for MLX model bundles without adding MLX as a Gradus
execution backend. Gradus will admit the bundle's configuration, tokenizer,
Safetensors members, shard index, tensor descriptors, and affine packed-weight
semantics into its existing device-neutral model path. A pinned
SmolLM2-135M-Instruct 8-bit bundle is the qualification row. Qwen3.8 is a
downstream architecture campaign that consumes this campaign's finished
bundle and quantization contracts; it is not allowed to enlarge the first MLX
implementation with linear-attention, recurrent-state, MoE, or multimodal
work.

## Non-Negotiable Invariants

1. **MLX is an artifact contract, not a backend.** Gradus does not import,
   embed, or call Apple's MLX runtime. `mlx-lm` is an independent oracle only.
2. **Safetensors stays standards-correct.** The first little-endian `u64`
   contains the JSON header byte count; the JSON begins at byte 8 and the data
   region begins at `8 + N`.
3. **A bundle has one pathless identity.** File paths, Hub repository names,
   cache locations, and filenames are locators. A versioned bundle identity
   binds every admitted logical member, member digest, byte length, and role.
4. **Admission is complete or rejected.** Unknown files may be ignored only by
   an explicit closed policy. Missing, duplicate, contradictory, unindexed,
   or hash-mismatched required members reject before tensor materialization.
5. **Architecture semantics are format-neutral.** Architecture adapters must
   consume canonical model/tensor facts rather than a GGUF-specific manifest.
6. **Storage and compute remain distinct.** `U32` packed weights plus floating
   scales and biases describe MLX affine storage. They do not silently become
   a claim about compute dtype, numerical parity, or device execution.
7. **Format support does not absorb architecture work.** SmolLM2 is the full
   executable qualification row for this campaign. Qwen3.8 architecture and
   state semantics lower separately after this contract closes.

## Problem

Gradus has a live `gradus:model/safetensors` module, but it is an exact
synthetic F32 row rather than general Safetensors or MLX support:

- `src/model/safetensors.fab` caps the row at 16 tensors, admits only `F32`,
  requires five exact names and shapes, and expects model/tokenizer facts in
  custom `__metadata__` fields.
- The same module and its committed fixture interpret the header length as
  including the eight-byte prefix. The Safetensors specification defines it
  as the number of JSON-header bytes after that prefix. The live MLX fixture
  uses the standard definition.
- `capsule.ContentIdentity` binds one file. An MLX model is a logical bundle of
  configuration, tokenizer assets, an index, and one or more Safetensors
  members.
- `src/model/dense_llama.fab` resolves canonical names directly through
  `gguf_manifest.GgufManifest`; its architecture facts and tensor naming are
  not yet reusable by a Safetensors/MLX bundle.
- Existing GGUF materialization and dequantization understand GGML block
  layouts, not MLX's `U32` packed affine rows with sibling `.scales` and
  `.biases` tensors.

A `.safetensors` extension therefore does not establish MLX support. The
bundle, identity, quantization, architecture, tokenizer, and executable oracle
must agree end to end.

## Desired End State

1. Gradus has a versioned, pathless model-bundle identity and manifest.
2. Safetensors parsing follows the public format and supports bounded
   inspection through a range source rather than requiring whole-file bytes.
3. `config.json` and `model.safetensors.index.json` are admitted through typed,
   closed schemas sufficient for supported rows.
4. Single-file and multi-file shard maps resolve every admitted tensor to one
   content-identified member and byte range.
5. The admitted dtype set includes the floating and packed storage required by
   the selected rows: `F32`, `F16`, `BF16`, and `U32`.
6. Global affine quantization at group size 64 supports 8-bit and 4-bit packed
   weights with exact shape and sibling-tensor validation.
7. Canonical architecture adapters are independent of GGUF names and can bind
   either GGUF or MLX manifests without duplicating forward code.
8. The pinned SmolLM2 development bundle passes admission, tokenizer,
   dequantization, logits, and deterministic generation oracles.
9. A downstream Qwen3.8 campaign can consume the bundle, Safetensors, shard,
   and affine-quantization contracts without reopening them.
10. The support matrix and public documentation state the exact admitted row,
    modes, dtypes, quantization parameters, and residual exclusions.

## Development Posture

- **Clean break.** Replace the nonstandard Safetensors fixture and row contract;
  do not preserve its header-length interpretation as compatibility behavior.
- **General format before model family.** The SmolLM2 row and downstream model
  families consume one bundle/manifest/quantization path rather than acquiring
  per-model parsers.
- **Reference before packed execution.** Establish exact dequantized values and
  logits first. Direct packed matrix execution may follow only through the
  same storage contract and an equivalence gate.
- **No ambient Hub behavior.** Gradus consumes local bounded sources. Download,
  authentication, cache policy, and network access remain product/tooling work.
- **No remote code.** A bundle requiring `model_file`, `trust_remote_code`, or
  executable repository content rejects in this campaign.
- **One global affine row first.** Mixed-bit recipes, per-layer modes, `mxfp4`,
  `nvfp4`, `mxfp8`, AWQ/GPTQ transformation, adapters, and LoRA are outside
  this contract.
- **Honest evidence tiers.** Header inspection, bundle admission, one-matrix
  dequantization, logits, tokens, and compiled-device execution are separate
  receipts. None substitutes for a later tier.

## Implementation Workflow

1. Lower each campaign stage through `delivery` before implementation.
2. Execute delivery-sized units through `factory` with focused red-green
   fixtures and typed rejection cases.
3. Keep model downloads outside Git. Commit only small synthetic fixtures,
   manifests, hashes, oracle outputs, and reproduction commands.
4. Use the pinned local bundle as artifact-backed evidence only after its
   revision and file digests are reverified.
5. Route compiler or physical-device gaps to Radix/Hosts rather than adding
   device handles or backend concepts to Gradus.
6. Update this campaign and any owning goal status in the same turn that a
   stage lands.

## Scope Routing

### In campaign

- Standards-correct Safetensors parsing and typed diagnostics.
- Bundle member roles, versioned bundle identity, and capsule handoff.
- `config.json`, tokenizer assets, and Safetensors index admission.
- Single- and multi-member shard resolution.
- MLX global affine `U32` packed storage for 8-bit and 4-bit, group size 64.
- Format-neutral canonical architecture binding for the admitted Llama row.
- SmolLM2 development and qualification proof.
- Synthetic negative corpus, real-artifact receipts, support matrix, and docs.

### Outside campaign

- Calling MLX, Metal Performance Shaders, Python, or Swift from Gradus.
- Hub download/cache/auth APIs and model discovery UI.
- HTTP serving, scheduling, batching policy, and product configuration.
- LoRA/adapters, training conversion, checkpoint export, and model publication.
- Mixed-bit/per-layer recipes and non-affine MLX quantization modes.
- Qwen3.8 architecture execution, vision/audio bundles, draft/MTP-only
  artifacts, assistant-only artifacts, MoE rows, and SSM/hybrid rows. Those
  require separate campaigns consuming this artifact layer.
- New GPU kernels or backend-specific execution contracts; those remain with
  Radix and Hosts.

## Batching And Split Policy

- **MLX0-MLX1: discovery-first.** Settle the corrected format and bundle
  identity contracts before implementation spreads across callers.
- **MLX2-MLX3: split-on-boundary.** Separate container/index parsing from
  quantized numerical semantics. Batch homogeneous dtype and rejection rows
  after the first pattern is accepted.
- **MLX4: discovery-first.** Prove one layer/matrix against `mlx-lm`, then
  complete the whole SmolLM2 row as one mandatory slice.
- **MLX5: batch-by-default.** Apply the accepted support and documentation
  schema across every admitted row in one closeout wave.

## Ground Truth Researched

Source snapshot: Gradus `c9961aff9e9e8c54b1509d878b9ae3da1d483945`
on 2026-08-21. Delivery must refresh the snapshot and foreign-dirt state.

| Fact | Live authority | Consequence |
| --- | --- | --- |
| Current Safetensors admission is one five-tensor, F32-only row with a 16-tensor ceiling. | `src/model/safetensors.fab:126-177,905-1005` | MLX cannot be added as another pinned-name branch; the parser must become format-general. |
| Current code and fixture count the prefix inside `header_size`. | `src/model/safetensors.fab:31-36`; `fixtures/safetensors/safetensors-row-oracle.md` | MLX0 replaces the fixture and parser rule together. |
| The public format says the first `u64` is `N`, followed by `N` JSON bytes. | [Safetensors format](https://github.com/huggingface/safetensors#format) | Data begins at `8 + N`; the old row is not retained as a compatibility dialect. |
| Capsule schema 2 binds one `ContentIdentity` to one GGUF or Safetensors manifest. | `src/model/artifact.fab`; `src/model/capsule.fab:226-303,543-547` | A bundle identity/schema decision precedes MLX admission. |
| The Llama adapter directly depends on `GgufManifest`. | `src/model/dense_llama.fab:1-18,167-180` | Canonical architecture facts and format-specific resolution must separate. |
| MLX affine quantization packs elements in unsigned 32-bit integers with one scale and bias per group. | [MLX quantized matmul](https://ml-explore.github.io/mlx/build/html/python/_autosummary/mlx.core.quantized_matmul.html) | MLX storage is a new packed layout, not a GGML type alias. |
| `mlx-lm` selects quantized modules from config and sibling `.scales` tensors, defaulting omitted mode to `affine`. | [`mlx_lm/utils.py`](https://github.com/ml-explore/mlx-lm/blob/main/mlx_lm/utils.py) | Admission must bind config, tensor inventory, shapes, and defaulted mode together. |
| The pinned bundle is a dense Llama row with global `{group_size: 64, bits: 8}`. | Local `config.json` under the pinned model directory | It avoids MoE, SSM, mixed-bit, and custom-code concerns. |
| The pinned index maps 694 tensors to one shard; the file contains 483 `F16` and 211 `U32` tensors. | Local index plus standards-correct header inspection | It proves realistic counts and MLX triplets while keeping sharding topology simple. |

### Pinned development artifact

| Field | Value |
| --- | --- |
| Hub model | `mlx-community/SmolLM2-135M-Instruct-8bit` |
| Revision | `0f0d9b8218915bc34d401e1a340b8c049d300d5e` |
| Local locator | `/Users/ianzepp/ai/models/SmolLM2-135M-Instruct-8bit` |
| Required remote members | 10 files; configuration, index, one weight member, and tokenizer assets |
| Logical bundle bytes | 147,877,089 bytes, excluding downloader cache metadata |
| Weight member | `model.safetensors`, 143,030,401 bytes |
| Weight SHA-256 | `ec569c771e56424636be99625aba9031abc525a68a5f4ab16d678eca96fef12c` |
| Config SHA-256 | `5da91905efdfde905f566d76d4031e6ca7c4cb2a01dc4e3812a70b855188fc73` |
| Index SHA-256 | `d016e7514e8bfed162eb9d0716c73244c1b73792db3143e92e54138c1772db44` |
| Safetensors header `N` | 75,257 bytes; data begins at byte 75,265 |
| Safetensors metadata | `{"format":"mlx"}` |
| Indexed tensors / shards | 694 / 1 |
| Stored dtypes | 483 `F16`; 211 `U32` |
| Quantized siblings | 211 `.scales`; 211 `.biases`; corresponding packed `.weight` tensors |
| Architecture | Llama; 30 layers; hidden 576; 9 attention heads; 3 KV heads; vocab 49,152; tied embeddings |

## Current State

| Track | State | Next action |
| --- | --- | --- |
| Safetensors container | Pinned synthetic F32 dialect; header rule conflicts with public format | MLX0 replace the rule and fixture |
| Artifact identity | One file per capsule | MLX1 settle versioned bundle identity |
| Bundle/index/config | No Gradus contract | MLX1 define; MLX2 implement |
| Dtypes | Safetensors admits F32 only | MLX2 add F16/BF16/U32 descriptor semantics |
| MLX quantization | No storage or math contract | MLX3 affine group-64 8/4-bit |
| Llama architecture | Typed adapter is GGUF-specific and frozen to SmolLM2-360M | MLX4 separate canonical facts and bind the 135M row |
| Tokenizer | SmolLM GPT-2/BPE runtime exists | MLX4 bind bundle assets and compare oracle IDs |
| Qwen3.8 | Local artifacts identify a separate hybrid architecture/state problem | Route a downstream campaign after MLX5; do not enlarge this one |
| Support claims | Safetensors synthetic row and GGUF rows only | MLX5 aggregate the exact MLX row |

## Campaign Path

### MLX0 — Standards-correct Safetensors reset

**Status**: planned — selected
**Source**: public Safetensors format; live parser and fixture contradiction
**Why now**: every later real MLX file uses the standard `8 + N` boundary
**Batching posture**: discovery-first
**Gate**: an accepted corrected container contract; regenerated legal fixture;
negative cases for truncated prefix/header/data, malformed JSON, overflow,
offset overlap/gaps, dtype-size mismatch, and duplicate names; old dialect has
no live acceptance path.
**Lowers to**: `delivery`, then `factory`

### MLX1 — Bundle identity and admission contract

**Status**: planned
**Depends on**: MLX0
**Source**: capsule schema 2, local MLX bundle topology, pathless-identity law
**Batching posture**: discovery-first
**Gate**: versioned logical-member roles; canonical bundle identity; required
and ignored member policy; digest/length verification order; capsule schema
decision; single- and multi-shard invariants; typed rejection matrix.
**Lowers to**: `delivery`, then `factory`

### MLX2 — General manifest, config, index, and shard resolution

**Status**: planned
**Depends on**: MLX1
**Batching posture**: split-on-boundary
**Gate**: bounded range-source Safetensors inspection; F32/F16/BF16/U32
descriptors; closed config projection; index `weight_map` validation; every
tensor resolves to exactly one identified member and range; synthetic
multi-shard positive and negative corpus; no whole-model byte list required.
**Lowers to**: `delivery`, then `factory`

### MLX3 — Affine packed-weight semantics

**Status**: planned
**Depends on**: MLX2
**Batching posture**: split-on-boundary
**Gate**: global affine group-size-64 admission for 8-bit and 4-bit rows;
packed shape recovery; `.weight`/`.scales`/`.biases` association; absent-bias
policy; bounds and tail rules; exact selected-value and one-matrix comparison
against MLX; unsupported modes and per-layer recipes reject before execution.
**Lowers to**: `delivery`, then `factory`

### MLX4 — SmolLM2 development-row execution

**Status**: planned
**Depends on**: MLX3
**Source**: pinned development artifact above
**Batching posture**: discovery-first, then mandatory whole-row completion
**Gate**: bundle admission; format-neutral Llama architecture binding; complete
required tensor inventory; tokenizer IDs and detokenization parity; selected
dequantized matrices; fixed-input logits/top-k within declared tolerance;
deterministic greedy token prefix; reproducible receipt through public
`gradus:*` APIs. One-layer or one-matrix evidence alone does not complete MLX4.
**Lowers to**: `delivery`, then `factory`

### MLX5 — Conformance, support matrix, and closeout

**Status**: planned
**Depends on**: MLX4
**Batching posture**: batch-by-default
**Gate**: synthetic and real-artifact suites pass; support matrix names exact
format, bundle schema, dtype, quantization, architecture, tokenizer, and proof
tiers; public API/diagnostics/module-map docs match live code; stale
Safetensors claims are removed; source and compile gates pass; the real 8-bit
row and synthetic 4-bit numerical row have reproducible receipts; the
downstream Qwen3.8 handoff names the finished contracts it may consume; no
campaign item remains incomplete.
**Lowers to**: `delivery`, then `factory`

## Dependency Rules

1. MLX0 precedes every real-artifact parser claim.
2. MLX1 identity precedes shard loading or capsule handoff.
3. MLX2 descriptors precede MLX3 quantized values.
4. MLX3 numerical parity precedes full-model inference.
5. SmolLM2 closes the reusable path before Qwen-specific work begins in a
   separate campaign.
6. Gradus may expose device-neutral packed operations. Radix/Hosts own any
   compiled kernel or physical residency work those operations reveal.
7. A local downloaded artifact is evidence input, never a committed fixture or
   a substitute for a receipt.

## First Useful Milestones

1. A standard external Safetensors file inspects correctly and the retired
   synthetic dialect rejects.
2. The pinned local MLX bundle produces one verified bundle manifest and
   resolves all 694 indexed tensors.
3. One packed 8-bit matrix dequantizes identically to the MLX oracle.
4. SmolLM2 emits matching fixed-input logits and a greedy token prefix.

## Campaign Artifact Acceptance Criteria

- Every mandatory workstream has one ordered campaign stage.
- MLX0 is the named next stage and can lower without reopening campaign scope.
- The development artifact is revision- and digest-pinned outside Git.
- Qwen3.8 is explicitly routed downstream so its hybrid architecture cannot
  weaken or expand the initial MLX artifact contract.
- Format inspection, bundle admission, quantized math, model execution, and
  device evidence are not conflated.
- Unsupported modes and external-effect boundaries have explicit stop rules.
- Implementation acceptance details remain owned by delivery specs and factory
  phases.

## Validation

Campaign-artifact validation:

```bash
git diff --check -- docs/factory/mlx-support/CAMPAIGN.md
../radix/scripta/check-factory-goal-status
```

Downstream delivery specs must name focused Gradus gates. The normal closeout
floor is:

```bash
./scripta/check-source
./scripta/check-compile
```

Real-model receipts additionally pin model revision, logical member digests,
oracle version, prompt/token inputs, tolerance policy, generated IDs, source
revision, hardware, and exact command.

## Open Questions

1. **Bundle identity encoding.** Default: a versioned canonical manifest over
   logical member role, normalized logical name, SHA-256, and byte length; the
   manifest digest is the bundle identity. Filesystem order and paths never
   participate.
2. **Capsule evolution.** Default: clean-break schema 3 with a bundle manifest,
   rather than pretending the current single-file `ContentIdentity` covers a
   directory. MLX1 may choose an equally strict new carrier if schema 3 would
   distort GGUF's single-file path.
3. **Reference versus direct packed execution.** Default: dequantize selected
   tensors for correctness first, then retain packed storage for direct
   execution only after the same values and logits match.
4. **Qwen3.8 follow-on.** Default: open a separate architecture campaign only
   after MLX5, then select its exact repository and revision there. The local
   Qwen3.8 evidence already shows that format compatibility alone cannot supply
   linear-attention and recurrent-state semantics.

## Stop Conditions

Pause instead of improvising when:

- a standards-correct Safetensors fix would preserve the old dialect or leave
  two parser authorities;
- bundle identity would depend on a path, mutable Hub branch, filename alone,
  or unverified member;
- a selected row requires remote code, executable repository content, a
  non-affine mode, mixed-bit configuration, or per-layer quantization;
- Qwen3.8 architecture, recurrent state, multimodal components, or MoE work is
  pulled into this campaign instead of routed downstream;
- exact scale/bias/packing semantics cannot be established from MLX and a
  pinned oracle;
- implementation requires a Gradus device handle, backend branch, network
  client, or Python/Swift/MLX runtime dependency;
- a real-model receipt would require publication, paid infrastructure,
  credentials, or another external effect not freshly authorized;
- foreign dirt overlaps a stage's write scope without a live-owner
  disposition.
