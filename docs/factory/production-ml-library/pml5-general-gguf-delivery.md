# Delivery: PML5-GGUF — General GGUF Inference Continuation

**Status**: active — GGUF-A1a selected for implementation in `factory/hand-1`
**Campaign**: [`CAMPAIGN.md`](CAMPAIGN.md), continuation after structural PML5
**Umbrella**: Radix `gpu-production-readiness` units ML-01 through ML-07
**Repo**: `gradus`
**Integration stop**: `factory/merge` only; this delivery does not fast-forward
any main branch

## Outcome

Turn the structural PML2/PML3/PML5 proofs into a real, device-neutral GGUF
inference library. A valid GGUF v3 file is parsed into a format manifest without
assuming its architecture is executable. Separately admitted architecture,
tokenizer, storage, and execution rows fail closed until they have direct
reference evidence.

“General GGUF” means format-general inspection plus an extensible, explicit
execution matrix. It does not mean that every architecture or quantization
published on Hugging Face is immediately executable.

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

| Artifact | Architecture | Tensor count | Initial disposition |
| --- | --- | ---: | --- |
| `SmolLM2-360M-Instruct-Q4_K_M.gguf` | `llama` | 290 | format + first dense reference row |
| `Qwen2.5-0.5B-Instruct-Q4_K_M.gguf` | `qwen2` | 290 | format + first useful Qwen row |
| `Qwen2.5-1.5B-Instruct-Q4_K_M.gguf` | `qwen2` | 338 | format now; execution after 0.5B |
| `Qwen3.6-35B-A3B-UD-Q4_K_M.gguf` | `qwen35moe` | 753 | format now; hybrid MoE/SSM execution separate |
| `heretic-UD-Q6_K.gguf` | `qwen35moe` | 733 | format now; hybrid MoE/SSM execution separate |
| `ornith-1.0-35b-Q8_0.gguf` | `qwen35moe` | 733 | format now; hybrid MoE/SSM execution separate |

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
| Real tokenizer encode/decode for admitted rows | Universal chat-template language |
| Dense Llama/SmolLM and Qwen2 reference models | `qwen35moe` execution in the dense unit |
| Full-layer prefill, decode, and KV semantics | Serving, scheduling, continuous batching |
| CPU/reference logits and token receipts | Unqualified “all GGUF models work” claims |
| Packed/native quantization capability contract | Silent full-model F32 expansion as GPU support |

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

GGUF-A1a -> GGUF-M1 qwen35moe architecture delivery (separate continuation)
```

ML-01, the imported-library execution seam, is an acceptance dependency for
broader executed claims. GGUF-A1a now has a bounded synthetic package-MIR
receipt through the hand-2 Radix binary; full real-file, tensor-payload, and
inference execution remains a Radix/Faber gate.

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
  23 PASS / 0 FAIL with exit 0; it covers only deterministic in-source
  bounded corpora and is not a real-file, tensor-payload, or inference claim.

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
ends in `ok: .`; the package-MIR exemplar prints 23 observed PASS lines, zero
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

### GGUF-A2 — Tokenizer Runtime

Load vocab, token types, merges, pre-tokenizer identity, special-token policy,
encode/decode, EOG behavior, and an explicitly supported chat-template subset
from the parsed artifact. SmolLM and Qwen2 arbitrary-Unicode probes must match
the pinned `llama.cpp`/Hugging Face token IDs and decoded text exactly.

### GGUF-A3 — Packed Storage And Reference Materialization

Separate logical dtype from physical storage. Bind one `TensorDescriptor` and
validated `TensorPayload` at a time to dense or packed tensor views. Connect
the existing CPU codecs and add only the layouts required by the selected
dense rows. Mixed per-tensor storage remains explicit. Whole-model conversion
to F32 is not an admitted native-execution path.

### GGUF-A4 — Dense Llama/Qwen Full Model

Implement RMSNorm, SiLU/SwiGLU, configurable RoPE, multi-head attention, GQA,
tied/untied embeddings, final normalization, output projection, and a complete
ordered layer stack. Assemble weights by explicit architecture adapters and
canonical tensor names. A full SmolLM2 and Qwen2.5-0.5B prefill logit row must
match an independent CPU oracle at the first-divergence boundary.

### GGUF-A5 — Real Prefill, Decode, And KV State

Replace the one-block cache proof with per-layer, per-KV-head state integrated
into attention. Prefill and incremental decode must agree on logits. Reset,
context rejection, cancellation, replay, and session identity are executed,
not only structurally compiled.

### GGUF-A6 — Multiple Dense Acceptance Rows

The actual local SmolLM2 and Qwen2.5-0.5B files pass manifest, tokenizer,
materialization, full-model, prefill/decode, and deterministic token receipts.
Qwen2.5-1.5B follows only after the same adapter proves it without special-case
constants. Unsupported families retain exact typed diagnostics.

### GGUF-A7 — Native Quantized Execution Contract

Gradus supplies packed layout and semantic operation requirements. Radix owns
lowering/kernels; Hosts owns physical storage and execution. A qualified
Q4_K_M path proves it does not expand the whole model to F32 and records
correctness, memory, timing, backend identity, and fail-closed capability
evidence. This unit is a cross-repo dependency, not an Inferentia task.

### GGUF-M1 — Hybrid Qwen35MoE/SSM Row

Lower separately after GGUF-A1a. The local `qwen35moe` files require MoE router
and expert dispatch plus hybrid SSM/attention semantics. Format parsing is part
of GGUF-A1a; execution is not hidden inside the dense Qwen adapter.

## Gates Before Inferentia

Inferentia remains paused until all of these are current evidence:

1. bounded package-aware Gradus execution through the imported-library seam;
2. generic inspection of an actual downloaded GGUF;
3. real encode/decode and special-token behavior;
4. mixed packed storage bound to tensor descriptors;
5. full-model CPU/reference logits;
6. persistent per-layer KV prefill/decode;
7. at least SmolLM2 and one Qwen dense executed row;
8. one persistent native GPU row with honest memory and correctness receipts.

Once those gates pass, the server work is intentionally thin: model selection,
request/config mapping, streaming, lifecycle, and operations around the Gradus
library and accepted execution host.

## Lane And Merge Procedure

Implementation uses `/Users/ianzepp/work/faberlang/worktrees/hand-1/gradus` on
`factory/hand-1`. Each unit commits exact paths and stops at its done oracle.
Integration uses `/Users/ianzepp/work/faberlang/worktrees/merge/gradus` on
`factory/merge`. This session may merge into `factory/merge`; it must not
fast-forward Gradus, Radix, Faber, or Hosts main.

No Tugboat or Vivi records are part of this delivery's execution process.
