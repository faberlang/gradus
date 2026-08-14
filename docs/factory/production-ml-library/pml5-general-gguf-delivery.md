# Delivery: PML5-GGUF — Qwen3.6 35B End-to-End Inference

**Status**: active — GGUF-A1a and GGUF-A1b implemented; GGUF-A1c passed the aggregate M8R4 gate and integrated to Gradus main at 2b3e41a
**Campaign**: [`CAMPAIGN.md`](CAMPAIGN.md), mandatory completion of PML5
**Umbrella**: Radix `gpu-production-readiness` Qwen3.6 invariant
**Repo**: `gradus`
**Integration stop**: `factory/merge` only; this delivery does not fast-forward
any main branch

## Outcome

Turn the structural PML2/PML3/PML5 proofs into a real, device-neutral GGUF
inference library. A valid GGUF v3 file is parsed into a format manifest without
assuming its architecture is executable. Separately admitted architecture,
tokenizer, storage, and execution rows fail closed until they have direct
reference evidence.

The completion row is the exact local
`Qwen3.6-35B-A3B-UD-Q4_K_M.gguf` artifact. Format-general inspection is a
foundation, not the delivery result.

## Delivery Invariant

This delivery is complete only when `exempla/qwen36-35b-inference`, using
public `gradus:*` imports, runs the artifact with byte length `22,663,387,424`
and SHA-256
`0b21525e972670ed59e1812e170b27c26355381f0656ecc4e25617ece7dac58b`.

One normal Faber package command must verify and admit the artifact, encode an
operator-supplied Unicode prompt, execute the complete `qwen35moe` graph,
generate at least 256 new tokens, decode them to text, and repeat for a second
prompt through the same admitted model session. The run must keep weights and
model state resident, avoid per-token reload/recompile/rebuild, match the
pinned `llama.cpp` comparison policy, and produce current Metal and CUDA
receipts with exact source, model, hardware, output, memory, and timing facts.

No earlier unit or partial proof satisfies this invariant.

## Why This Continuation Exists

The historical phases remain true at their stated structural scope:

- PML2 admits one scaled SmolLM2-shaped GGUF fixture with caller-supplied exact
  counts. It discards metadata values and tensor descriptors after validation.
- PML3 executes a fixed B=2, D=8 transformer fragment, not a complete Llama or
  Qwen model.
- PML5 composes one block, logical cache values, sampling, and bounded token
  pins. It has no current full-model executed-token receipt.

The live loader also fixes alignment at 32, assumes unpadded contiguous tensor
payloads, rejects unknown metadata keys, accepts only ranks 1 and 2, stores the
whole file in a `lista<u8>` capsule, and labels a mixed-storage artifact with
one global quantization row. Those invariants do not fit real GGUF files or
artifacts up to 35 GB.

## Grounded Local Acceptance Corpus

The corpus is operator-local evidence and is never committed into Gradus.

| Artifact | Architecture | Tensor count | Mandatory role |
| --- | --- | ---: | --- |
| `SmolLM2-360M-Instruct-Q4_K_M.gguf` | `llama` | 290 | dense reference rung |
| `Qwen2.5-0.5B-Instruct-Q4_K_M.gguf` | `qwen2` | 290 | dense Qwen reference rung |
| `Qwen2.5-1.5B-Instruct-Q4_K_M.gguf` | `qwen2` | 338 | scale-independent dense adapter proof |
| `Qwen3.6-35B-A3B-UD-Q4_K_M.gguf` | `qwen35moe` | 753 | campaign completion row |

The corpus proves why a filename or `general.file_type` cannot stand in for a
per-tensor storage manifest. The files contain mixed F32 and quantized tensors;
the hybrid rows also include rank-3 expert tensors and may include BF16 or
Q5_K storage.

## Ownership And Clean Boundary

| Concern | Owner | Contract |
| --- | --- | --- |
| GGUF wire parsing, metadata, tensor directory, normalized model semantics | Gradus | pathless immutable descriptors |
| Tokenizer behavior, model graph, logical KV state, sampling | Gradus | device-neutral values and operations |
| Lowering, fusion, generated kernels, `DeviceProgram` | Radix | consumes admitted semantic operations |
| File mapping, range reads, allocation, residency, upload, launch | Hosts/application | resolves bounded ranges against content identity |
| CLI, HTTP, scheduling, streaming, deployment | Inferentia or later product | wraps accepted Gradus and execution APIs |

The clean-break artifact boundary is:

```text
ParsedArtifact
  ContentIdentity { algorithm, digest, byte_length }
  GgufManifest { version, alignment, data_offset, metadata, tensors }

TensorDescriptor
  name
  shape
  element_count
  raw_ggml_type
  known block geometry when available
  ByteRange { start, length }

AdmittedModel
  ParsedArtifact identity
  supported ArchitectureSpec
  supported TokenizerSpec
  explicit execution capabilities

TensorPayload
  one validated ByteRange
  bounded bytes for that range
```

No Gradus semantic value owns a path, URL, file descriptor, memory mapping,
device handle, or whole-model byte list. Byte ranges are absolute offsets into
the content identity. Unknown metadata and unknown raw GGML type identifiers
remain inspectable; unsupported execution fails at the admission boundary.

## Scope Matrix

| In scope | Out of scope |
| --- | --- |
| GGUF v3 metadata and tensor-directory parsing | GGUF writers or converters |
| Configurable alignment and padded tensor spans | Filesystem, mmap, HTTP, Hub downloads |
| Per-tensor raw storage descriptors | Device allocation and kernel launch |
| Real tokenizer encode/decode for all mandatory rows | Universal chat-template language |
| Dense reference models and full `qwen35moe` admission | Other model architectures |
| Rank-3 expert tensors, MoE routing, and expert dispatch | Serving, scheduling, continuous batching |
| Hybrid SSM/attention state, prefill, and decode | HTTP and deployment |
| CPU/reference logits and deterministic token receipts | Unqualified “all GGUF models work” claims |
| Native quantized Metal and CUDA execution | Silent full-model F32 expansion as GPU support |
| Persistent Faber capstone for the selected Qwen3.6 artifact | Other local 35B variants |

## Unit Graph

```text
GGUF-A0 inventory
  -> GGUF-A1a manifest and bounded-corpus parser
       -> GGUF-A1b range-source seam and real-file inspection
            -> GGUF-A1c capsule/caller clean break
                 -> GGUF-A2 tokenizer runtime
                 -> GGUF-A3 packed storage and reference materialization
                      -> GGUF-A4 dense Llama/Qwen primitives and full model
                           -> GGUF-A5 per-layer KV prefill/decode
                                -> GGUF-A6 real dense rows
                                     -> GGUF-A7 native quantized execution contract

GGUF-A2 + GGUF-A3
  -> GGUF-M1 qwen35moe admission and tensor map
       -> GGUF-M2 MoE router and expert execution
       -> GGUF-M3 hybrid SSM/attention state
            -> GGUF-M4 full-model reference inference

GGUF-A7 + GGUF-M4
  -> GGUF-M5 persistent Metal and CUDA execution
       -> GGUF-M6 Faber Qwen3.6 capstone and closeout
```

ML-01, the imported-library execution seam, is an acceptance dependency for
broader executed claims. GGUF-A1a now has a bounded synthetic package-MIR
receipt through the hand-2 Radix binary; full real-file, tensor-payload, and
inference execution remains a Radix/Faber gate.

## Unit Admission And Progress Ratchet

Every unimplemented unit below must be lowered into a task body that names its
exact write scope, predecessor receipt, first failing oracle, closeout command,
expected observed result, work-token estimate basis, and stop condition. A raw
unit heading is not a Hand assignment. The delivery audit must admit the task
body before implementation.

Each completed unit must add one new executed proof at its declared boundary.
If execution diverges, the receipt records the first divergent tokenizer id,
tensor, layer, state update, logit, or token. Documentation, compilation, and
structural artifacts may support a unit but cannot replace its executed proof.
A compiler or host blocker is routed to its owning repository with that exact
divergence; all unaffected units continue.

### GGUF-A0 — Inventory And Capability Rows

**Done when**: every local file is recorded by content identity, architecture,
format version, tokenizer identity, shape features, tensor storage types, and
reference/native support state. Filenames are provenance only.

**Evidence**: an independent reader and `llama.cpp` agree on header, metadata,
tensor counts, offsets, and type distributions.

### GGUF-A1a — Manifest And Bounded-Corpus Parser

**Selected first unit.**

**Write scope**:

- `src/model/artifact.fab` and `src/model/artifact.proba`, public import
  `gradus:model/artifact`
- `src/model/gguf_manifest.fab` and `src/model/gguf_manifest.proba`, public
  import `gradus:model/gguf_manifest`
- `fixtures/gguf/gen_manifest_fixtures.py`,
  `fixtures/gguf/general-manifest-oracle.md`, and generated small fixtures
  `llama-manifest-v3.gguf`, `qwen2-manifest-v3.gguf`, and
  `qwen35moe-manifest-v3.gguf`
- `README.md`, `docs/module-map.md`, `docs/api-reference.md`,
  `docs/diagnostics.md`, `docs/regression-corpus.md`,
  `docs/factory/production-ml-library/pml0-symbol-inventory.md`, and
  `docs/factory/production-ml-library/pml0-support-matrix.md`
- `exempla/gguf-manifest/faber.toml`,
  `exempla/gguf-manifest/src/main.fab`,
  `exempla/gguf-manifest/README.md`, and `scripta/check-compile` for the
  bounded package-MIR proof and its receipt

**Frozen public surface**:

- `gradus:model/artifact` exports `IdentitasContenuti { textus algorithmus,
  textus digestio, numerus longitudo }`, `ArtifactError { AlgorithmusIgnotus
  { textus causa }, DigestioMala { textus causa }, LongitudoMala { textus
  causa } }`, `causa(ArtifactError)`, and
  `identitas(textus algorithmus, textus digestio, numerus longitudo) ->
  IdentitasContenuti ⇥ ArtifactError`. The first row accepts only the
  lower-case `sha-256` name, a 64-digit lower-case hexadecimal digest, and a
  positive length. It contains no path, URL, reader, file handle, host/device
  object, or payload.
- `gradus:model/gguf_manifest` exports `CorpusGguf { octeti tabula, numerus
  longitudo_artifacti, artifact.IdentitasContenuti identitas }`,
  `MetadatumGguf { textus clavis, numerus typo, octeti valor_wire }`,
  `LayoutGgml { Cognita { numerus elementa_per_blockum, numerus
  octeti_per_blockum, numerus longitudo_octetorum }, Ignota { numerus typo }
  }`, `DescriptioTensorisGguf { textus nomen, lista<numerus> forma, numerus
  typo_ggml, numerus offset_relativum, numerus elementa, LayoutGgml layout }`,
  and `ManifestumGguf { artifact.IdentitasContenuti identitas, numerus
  versio, numerus concordatio, numerus data_inceptum, numerus
  longitudo_artifacti, lista<MetadatumGguf> metadata,
  lista<DescriptioTensorisGguf> tensores }`.
- Its operations are `parse(CorpusGguf) -> ManifestumGguf ⇥
  GgufManifestError`, `metadatum(ManifestumGguf, textus) -> MetadatumGguf ⇥
  GgufManifestError`, `textum(ManifestumGguf, textus) -> textus ⇥
  GgufManifestError`, `numerum(ManifestumGguf, textus) -> numerus ⇥
  GgufManifestError`, `inveni_tensorem(ManifestumGguf, textus) ->
  DescriptioTensorisGguf ⇥ GgufManifestError`, and
  `layout(numerus typo_ggml, lista<numerus> forma) -> LayoutGgml ⇥
  GgufManifestError`.
- `GgufManifestError` is the only parser error surface. Its frozen variants
  are `FormatMala`, `VersioIgnota`, `Truncata`, `WireMala`, `LimitesMala`,
  `Superfluitas`, `ClavisDuplicata`, `TensorDuplicatum`, `OffsetMala`, and
  `IdentitasMala`, each carrying `textus causa`; `causa(GgufManifestError)`
  renders it. Unknown architecture names and raw GGML type ids are data, not
  parser errors. `LayoutGgml.Ignota` is the explicit unresolved codec state;
  an architecture adapter introduced after this unit owns typed unsupported
  execution.
- `gradus:model/gguf` remains the old one-row capsule authority through
  GGUF-A1b. The new authority is only format parsing and is named
  `gradus:model/gguf_manifest`; GGUF-A1c deletes the dual format parser while
  migrating callers. A1a adds no forwarding import or compatibility facade.

**API spelling amendment (2026-08-12, head-cxo).** The frozen tensor accessor
is `inveni_tensorem(ManifestumGguf, textus)`. The earlier provisional spelling
`tensor` is retired because it is reserved in current Radix; `tensorum` is not
the public spelling. This is a clean break with no compatibility alias.

**Required behavior**:

1. Parse GGUF v3 from an explicitly supplied bounded corpus containing the
   complete header, metadata, and tensor table, plus caller-supplied total file
   length and content identity. The parser never accepts or retains the data
   region. A typed truncation result tells a source adapter that its corpus did
   not contain the complete table. `general.alignment`, when present, must be
   use the GGUF_UINT32 wire kind and be a valid positive power-of-two value. A
   different present wire kind is a typed wire error. When absent, parsing uses the
   GGUF default alignment of 32. The table end is rounded up with checked
   arithmetic to obtain `data_inceptum`; a corpus may end at the table or
   within its padding but must not contain a byte from the data region.
2. Preserve every metadata entry with its GGUF value kind. Known scalar/text
   fields have typed accessors; arrays needed by tokenizer and architecture
   units remain preserved rather than discarded.
3. Preserve every raw tensor name, shape, rank, logical element count, raw GGML
   type, and relative offset. A separate layout resolution step produces an
   exact stored byte length only when that GGML layout is known; the parser
   then derives its checked absolute range from `data_inceptum` and
   `offset_relativum`; every relative offset, including an unknown raw type,
   must satisfy `data_inceptum + offset_relativum <= total`. Unknown layouts
   remain inspectable but are not materializable.
4. Honor legal `general.alignment`; validate power-of-two alignment,
   non-overlapping known ranges irrespective of tensor-table order, overflow,
   truncation, duplicate names, and file bounds. Reject rank zero. For known
   quantized layouts, block divisibility is checked against the first GGML
   dimension, not only the total element product. Bound metadata and tensor
   directories at 4,096 entries and the retained corpus prefix at 64 MiB;
   these conservative ceilings bound the duplicate/overlap scans while
   admitting all six inventoried local models (maximum 753 tensors).
5. Parse rank-3 expert tensors and unknown raw storage identifiers as
   inspectable descriptors. Do not claim a decoder or kernel for them.
6. Separate `parse` from `admit`: A1a adds no admission or execution entry
   point. Valid unknown architecture names parse as metadata. A later
   architecture adapter must return a typed unsupported-architecture result
   when admission or execution is requested.
7. Do not edit the old capsule or its GGUF/Safetensors callers in this unit.
   The new parser is the replacement foundation, not a compatibility façade;
   GGUF-A1c owns the clean deletion/migration boundary.

**Red proof**: before implementation, add focused cases for custom alignment,
padded spans, rank 3, unknown metadata, mixed storage, and a Qwen architecture
against the not-yet-present format-general parser. Record the failing command
and first divergence.

**Green proof**:

- small synthetic `llama`, `qwen2`, and `qwen35moe` fixtures parse into the
  same artifact type;
- one fixture omits `general.alignment` and resolves to 32; another supplies
  a non-default legal alignment and proves the resulting padded data offset;
- malformed/truncated/overflowing/overlapping fixtures fail with typed errors;
- unsupported architecture and codec states are distinct from malformed GGUF;
- changed-source checks and package-aware semantic analysis pass;
- `exempla/gguf-manifest` runs through package MIR and prints observed PASS
  results for every named positive and negative case. The hand-2 receipt is
  31 PASS / 0 FAIL with exit 0; it covers all thirteen metadata wire kinds,
  exact `valor_wire` preservation, nested arrays, descriptor ranges, and the
  typed BOOL `numerum` rejection in deterministic in-source bounded corpora.
  It is not a real-file, tensor-payload, or inference claim.

**Commands** (from the Hand packet):

```bash
cd /Users/ianzepp/work/faberlang/worktrees/hand-1/gradus
./scripta/check-source
env FABER_LIBRARY_HOME=/Users/ianzepp/work/faberlang/worktrees/hand-1 \
  FABER_BIN=/Users/ianzepp/work/faberlang/worktrees/hand-2/radix/target/debug/faber \
  ./scripta/check-compile
env FABER_LIBRARY_HOME=/Users/ianzepp/work/faberlang/worktrees/hand-1 \
  /Users/ianzepp/work/faberlang/worktrees/hand-2/radix/target/debug/faber \
  check --diagnostics .
env FABER_LIBRARY_HOME=/Users/ianzepp/work/faberlang/worktrees/hand-1 \
  /Users/ianzepp/work/faberlang/worktrees/hand-2/radix/target/debug/faber \
  run --target fmir exempla/gguf-manifest
git diff --check -- src/model/artifact.fab src/model/artifact.proba \
  src/model/gguf_manifest.fab src/model/gguf_manifest.proba fixtures/gguf \
  README.md docs/module-map.md docs/api-reference.md docs/diagnostics.md \
  docs/regression-corpus.md \
  docs/factory/production-ml-library/pml0-symbol-inventory.md \
  docs/factory/production-ml-library/pml0-support-matrix.md \
  exempla/gguf-manifest/faber.toml exempla/gguf-manifest/src/main.fab \
  exempla/gguf-manifest/README.md scripta/check-compile
```

**Expected result**: `check-source` and `check-compile` exit 0; `faber check`
ends in `ok: .`; the package-MIR exemplar prints 31 observed PASS lines, zero
FAIL lines, and exits 0; `git diff --check` is silent; all synthetic
manifest/parser cases type-check. This is the executed A1a bounded-parser
proof. It does not parse committed fixtures, read real files or tensor
payloads, or claim inference; focused `faber test` remains provider-blocked.

`docs/regression-corpus.md` must inventory both new `.proba` suites and all
three generated fixtures, update its suite/fixture totals, and bump its
document version under the corpus contract. Stale totals block closeout.

**Non-goals**: tokenization, tensor payload codecs, model assembly, inference,
GPU work, Hosts work, Inferentia, or main-branch integration.

### GGUF-A1b — Range Source And Real-File Inspection

**Implemented evidence**: `gradus:model/gguf_manifest` now exposes the
operation-scoped `LectioFontis` callback contract, `inspice`, and
`lege_fragmentum`. The 40-case synthetic package proof covers source failures,
short reads, exact tensor fragments, range rejection, and unknown layouts. The
guarded `exempla/gguf-inspect` adapter matched the six local rows as
`llama/290`, `qwen2/290`, `qwen2/338`, and
`qwen35moe/753/733/733`; every computed data offset matched the independent
GGUF reader. The adapter reads exactly the independently bounded header/table
prefix once, then serves exact subranges through a captured operation-scoped
callback. Any inspection request that intersects tensor data fails against the
prefix bound. Exact commands, content identities, sizes, offsets, and observed
output are in `exempla/gguf-inspect/README.md`.

Define the exact failable range-source contract only after its Faber
function-value ABI is executable through an imported Gradus package. The
source is passed per operation and is never retained. Add bounded table reads
and tensor-fragment reads with checked absolute ranges and exact-length return
checks.

This unit owns the real local inventory oracle. Its receipt must name the
source adapter and command, prove that no read intersects the tensor data
region during inspection, and report `llama/290`, `qwen2/290`, `qwen2/338`,
and `qwen35moe/753/733/733` against the independent reader. A package-aware
compile-only check is insufficient for this unit.

### GGUF-A1c — Capsule And Caller Clean Break

Replace the byte-owning, path-carrying, one-global-quantization capsule with
schema-2 identity/manifest values and reject schema 1 at the new boundary.
Explicit write scope includes `src/model/capsule.fab`, capsule probas,
`src/model/gguf.fab`, `src/model/safetensors.fab`, both format probas,
fixture contracts, and API/support documentation. Migrate all constructor
callers in one unit; add no forwarding shim and leave no dual GGUF authority.

**Done when**: schema 1 has no live constructor or parser caller; schema 2
identity/manifest values are the only authority; source, compile, and migrated
format probas pass.

**Implemented evidence**: the A1C clean break is implemented across the
transitional A1C micro-unit chain M1–M7: M1 capsule schema-2 producer
`1c3bc51`, M2 GGUF caller/parser migration `baa32c5`, M3 Safetensors
caller/proba migration `3a3d906`, M4 conformance/fixtures schema-2 migration
`ba2aae9`, M5 API/support docs `fb41344`, M6 inventory re-baseline `4f3abb7`,
and M7 status records `77dd706`, plus the visibility-correction fixes. The
refreshed candidate tip `3a1ef0f` passed the aggregate M8R4 gate (green
receipt `b31b5a86`) and was integrated atomically to Gradus main at `2b3e41a`;
schema 1 has no live constructor or parser caller and schema 2 is the only
authority. This closes LIB-01 only — it is not campaign completion and claims
no exact-Qwen Metal/CUDA execution. The next dependencies remain LIB-02
(artifact-backed tokenizer/detokenizer) and LIB-03 (checked packed storage and
tensor materialization).

### GGUF-A2 — Tokenizer Runtime

Load vocab, token types, merges, pre-tokenizer identity, special-token policy,
encode/decode, EOG behavior, and the selected chat-template behavior from the
parsed artifact. The three dense rungs and selected Qwen3.6 artifact must match
the pinned `llama.cpp` token ids and decoded text for two Unicode probes.

**Primary scope**: `src/tokenizer.fab`, `src/tokenizer.proba`, manifest metadata
accessors, and the tokenizer phase of `exempla/qwen36-35b-inference`.

**Done when**: the real Qwen3.6 tokenizer consumes metadata from the artifact;
no hard-coded prompt or token-id fallback exists in the capstone path; encode
and decode match the independent oracle.

**Implemented evidence**: LIB-02 is implemented across the micro-unit chain on
the `factory/hand-16` packet (U1 `c4d0750`, U2 `f3cfa58`, U3-1 `58786db`,
U3-2 `00f5540`, U3-3 `e1b818f`, U3-4 `90b0522`, U3-5 `a2dcd8d`, U3-6
`cc92176`, U3-7 `82a2863`, U4-1 `4ceb1d3`), with the capstone tokenizer-phase
exempla running green on the target artifact on 2026-08-14. The run printed
`PASS` for both pinned probe id lists and both decoded round-trips (Probe A
Thai → 8 ids, Probe B CJK/emoji/digits → 18 ids, both decode back to the
exact prompt text), `TOKENIZER PHASE PASS`, and exited 0 with no read into
the tensor data region; focused negatives exit nonzero with typed causes and
any probe divergence prints a `DIVERGENCE` receipt naming the first divergent
id/character. The artifact-backed runtime is consumed through the public
`gradus:tokenizer` surface (vocab 248,320, merges 247,587, `gpt2` byte-level
BPE + `qwen35` pre-tokenizer, EOG {248044, 248046, 248063, 248064, 248065},
BOS-free); no hard-coded prompt or token-id fallback exists in the capstone
path. Full receipts are in `pml5-lib02-tokenizer-delivery.md` §Delivery
Receipt and `exempla/qwen36-35b-inference/README.md`. This executes the
tokenizer input of milestone Q1 — it is not model execution: no logits,
tensor materialization, GPU work, or generated tokens are claimed (GGUF-A3+
and GGUF-M4..M6 remain mandatory with their frozen oracles).

### GGUF-A3 — Packed Storage And Reference Materialization

Separate logical dtype from physical storage. Bind one `TensorDescriptor` and
validated `TensorPayload` at a time to dense or packed tensor views. Connect
the existing CPU codecs and implement every physical layout used by the four
mandatory artifacts. Mixed per-tensor storage and rank-3 expert tensors remain
explicit. Whole-model conversion to F32 is not an admitted execution path.

**Primary scope**: `src/model/gguf_manifest.fab`, `src/model/dequant.fab`,
their probas, packed tensor-view modules introduced by this unit, and the
materialization phase of the capstone.

**Done when**: every tensor required by the Qwen3.6 forward graph has a checked
range, shape, storage layout, and bounded materialization path; selected
tensor slices match the independent oracle.

**Implemented evidence**: GGUF-A3 is implemented across the micro-unit chain
on the `factory/hand-24` packet (C1 `82048b5`; C2-U1 `fc59ac4`, C2-U2
`e640a50`, C2-U3 `6dd29fb`, C2-U4 `686653c`, C2-U5 `d182c5c`, C3-U1
`2ec80d8`/`4b1d165`, C3-U2 `edcff45`, C3-U6 `9643e5b`; the C3-U3/U4/U5 doc
units land through the parallel hand-3/hand-9/hand-1 packets and are verified
at merge time). The admitted codec set widens to
{F32, BF16, Q5_0, Q8_0, Q4_K, Q5_K, Q6_K}, and the surface adds
`limes_payloadis`, `TensorPayload`/`PayloadError`, `VisumTensoris`/
`VisioError` + `vincula`, and the bounded windowed materializers
`materializa_slicem` / `materializa_glomulum` — every byte read flows through
the operation-scoped source; no whole-tensor or whole-model read path exists.
The A3 closeout gate ran green on 2026-08-14 from the hand-24 packet:
`./scripta/check-source` exit 0, `./scripta/check-compile` ok, and the guarded
real-file exempla run against the local Qwen3.6 artifact printed 13 PASS /
0 FAIL with exit 0 — coverage `tensors=753 known=753 unknown=0` over
BF16:2/F32:368/Q8_0:259/Q4_K:82/Q5_K:38/Q6_K:4, the two Qwen2.5 dense-row
distributions, and all eight golden slices bit-exact against the committed
goldens (full receipt in `exempla/gguf-materialize/README.md`). This is the
output-checked slice-tier proof; executed token/model identity remains gated
on CTO8-1 (GGUF-A4+).

### GGUF-A4 — Dense Llama/Qwen Full Model

Implement RMSNorm, SiLU/SwiGLU, configurable RoPE, multi-head attention, GQA,
tied/untied embeddings, final normalization, output projection, and a complete
ordered layer stack. Assemble weights by explicit architecture adapters and
canonical tensor names. A full SmolLM2 and Qwen2.5-0.5B prefill logit row must
match an independent CPU oracle at the first-divergence boundary.

**Done when**: both dense rows execute complete layer stacks and publish
first-divergence receipts. This mandatory rung establishes the reusable
forward operations consumed by `qwen35moe`; it does not close the delivery.

### GGUF-A5 — Real Prefill, Decode, And KV State

Replace the one-block cache proof with per-layer, per-KV-head state integrated
into attention. Prefill and incremental decode must agree on logits. Reset,
context rejection, cancellation, replay, and session identity are executed,
not only structurally compiled.

**Done when**: full dense prefill and incremental decode produce equivalent
logits at the declared boundary, and two prompts prove reset/reuse semantics.

### GGUF-A6 — Multiple Dense Acceptance Rows

The actual local SmolLM2 and Qwen2.5-0.5B files pass manifest, tokenizer,
materialization, full-model, prefill/decode, and deterministic token receipts.
Qwen2.5-1.5B follows only after the same adapter proves it without special-case
constants. Unsupported families retain exact typed diagnostics.

**Done when**: all three dense files produce deterministic text receipts from
real prompts through the same public library surface.

### GGUF-A7 — Native Quantized Execution Contract

Gradus supplies packed layout and semantic operation requirements. Radix owns
lowering/kernels; Hosts owns physical storage and execution. A qualified
Q4_K_M path proves it does not expand the whole model to F32 and records
correctness, memory, timing, backend identity, and fail-closed capability
evidence. This unit is a cross-repo dependency, not an Inferentia task.

**Done when**: the dense reference rows execute through native packed kernels
on Metal and CUDA without whole-model expansion, establishing the kernel and
residency substrate required by GGUF-M5.

### GGUF-M1 — Qwen35MoE Admission And Tensor Map

Read all required `qwen35moe` metadata, freeze the architecture configuration,
map canonical tensor names, validate layer/expert/state dimensions, and admit
every selected-artifact tensor required by execution. Unknown or missing
required facts fail at admission.

**Primary scope**: new `src/model/qwen35moe.fab` and proba, architecture-facing
manifest accessors, API/support documentation, and the admission phase of the
capstone.

**Done when**: the exact Qwen3.6 artifact admits with 753 tensors and a complete
typed execution configuration; mutated metadata, names, shapes, and storage
layouts fail with typed first-divergence diagnostics.

### GGUF-M2 — MoE Router And Expert Execution

Implement router logits, the artifact's declared expert selection and weight
normalization, rank-3 expert projection access, expert dispatch, accumulation,
and deterministic tie behavior.

**Done when**: selected layers match independent router choices, expert
weights, intermediate values, and outputs for pinned hidden-state probes.

### GGUF-M3 — Hybrid SSM And Attention State

Implement the architecture's declared SSM and attention layer schedule,
convolution/recurrent state, attention KV state, position handling, reset,
replay, and incremental updates without conflating the two state families.

**Done when**: per-layer prefill and one-token decode state and outputs match
the independent oracle at the first-divergence boundary; reset and replay are
deterministic.

### GGUF-M4 — Full-Model Qwen3.6 Reference Inference

Compose embeddings, all hybrid layers, normalization, output projection,
tokenizer, sampling, and logical model state into the public Gradus generation
surface.

**Done when**: the exact artifact accepts two arbitrary prompts and produces
matching reference logits/tokens and decoded text for a bounded CPU/reference
run. Any resource-limited reference mode must still execute every layer and
must not substitute a reduced model.

### GGUF-M5 — Persistent Native Metal And CUDA Execution

Lower every operation required by GGUF-M4 to packed native kernels, bind the
model through prepared host sessions, and retain weights plus KV/SSM state
across decode steps and sequential prompts.

**Done when**: Metal and CUDA each generate at least 256 new tokens for both
prompts without per-token reload, recompilation, packet rebuild, or full host
round-trip; receipts record correctness, peak memory, timing, backend,
hardware, and lifecycle cleanup.

### GGUF-M6 — Faber Qwen3.6 Capstone And Closeout

Create `exempla/qwen36-35b-inference` as the public-library consumer. The
application owns the path and I/O, Gradus owns the model semantics, Radix owns
lowering, and Hosts owns physical execution.

**Done when**: one documented Faber package command satisfies every clause of
the Delivery Invariant on Metal and CUDA; the receipt is reproducible from a
clean packet and the support matrix, API docs, regression inventory, and
campaign status all describe the observed result exactly.

## Campaign Closeout Gates

Every item below is mandatory:

1. bounded package-aware Gradus execution through the imported-library seam;
2. generic inspection of an actual downloaded GGUF;
3. real encode/decode and special-token behavior;
4. mixed packed storage bound to tensor descriptors;
5. full-model CPU/reference logits;
6. persistent per-layer KV prefill/decode;
7. all three dense reference rows execute through the shared public surface;
8. `qwen35moe` admission, MoE, SSM/attention, and full-model reference receipts;
9. persistent native Qwen3.6 execution on Metal and CUDA; and
10. the Faber capstone satisfies the Delivery Invariant.

## Lane And Merge Procedure

The Mind assigns a fresh role packet for each admitted unit. Each unit commits
exact paths and stops at its done oracle.
Integration uses `/Users/ianzepp/work/faberlang/worktrees/merge/gradus` on
`factory/merge`; main updates follow the workspace merge-lane rules.

Current Tugboat and Vivi law governs execution. Every dispatched unit requires
an admitted delivery lineage, a Vivi task, and a live role process; filed work
without a spawned process is not in flight.
