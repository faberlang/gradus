# Census Wave 0 — The Carrier/Admissions Ruling

**Kind**: ruling + delivery record (Census Wave 0 of the
[kernel-purity campaign](CAMPAIGN.md))
**Status**: done — delivered 2026-08-26 at gradus `500342d` (rename + rider)
**Ruling authority**: operator priority ruling on task `aee52855`, over the
OX-Alpha kernel-purity census `015eb5f7`
(report: `../../../.vivi/oxalpha-kernel-census-015eb5f7.md`, base `83b65fa`)
**Write scope**: `gradus` (src, exempla, docs) + `radix` digest lineage re-pin

---

## 1. The decision being recorded

The census's structural finding (§2 there): the production tensor-math core
is written on a **staged runtime carrier** while the kernel contract
admits **typed static-shape entries** (`gradus:kernel` `@ kernel`
declarations over `tf32[8,960]` / `tensor<f32,[M,N]>`). Waves 1–3 are all
gated on one seam decision. The operator ruled:

1. **Name**: the staged carrier `Tensor{data: list<f32>}` is the wrong name —
   it "implies tensor when it's a bag" (an LLM-confusion hazard: readers
   import tensor-algebra priors into a plain envelope). The class is
   **`NumericBlock`** — English, no Latin, in the envelope/headers/payload/
   metadata frame.
2. **Direction**: data exits the carrier as early as possible. **Weights
   exit at load** into typed entries where kernel surfaces exist; the
   carrier's legitimate long-term tenant is **dynamic activations**.
3. **This wave** is the ruling wave: rename + the boundary written down +
   the construction-time stride cache. It unlocks Waves 1–3.

## 2. The carrier/admissions boundary (the law)

**`NumericBlock` is an envelope, not a math object.** It carries a dtype
tag, a runtime shape vector, and row-major flat `list<f32>` bytes — headers
plus payload. It has no kernel meaning, no algebraic identity, and no
device residency. Treating it as "a tensor" is the category error the name
change exists to prevent.

| Question | Ruling |
| --- | --- |
| Who may **construct** a NumericBlock? | Only `gradus:tensor`'s constructor family: `construct` / `construct_dtype` / `fill` (fail-closed admissions — external data enters here, validated through `shape.numel`), `default` (placeholder), and `stage` (trusted-input staging for library-internal producers that just built `data` to match `shape`; no validation — the producer's shape arithmetic is the admission). Struct literals at other sites are retired (the 26 internal literal sites now call `stage`). |
| Who may **hold** one long-term? | Load/staging seams (before weight materialization), activations producers (decode/prefill forward stack), and host-side state (KV payload rows, session logits). |
| What must be a **typed static-shape entry** instead? | Anything that crosses the kernel boundary. `@ kernel` (`@ nucleum`) entries take shaped resident tensors + an output view; host validation happens before the boundary (the `kernel.fab` placement law). A carrier never crosses. |
| **Weights** | Exit the carrier **at load** to typed entries bound to kernel surfaces where those exist (the GEA2 pattern: `tensor_view` admission + frozen-shape entries). Where no kernel surface exists yet, a weight may transit the carrier temporarily — that is recorded debt, not endorsement; the exit is the standing direction. |
| **Activations** | Remain the carrier's legitimate tenant. Dynamic shapes (runtime T, decode T=1, prefill T_p) are exactly what the staged envelope is for; Waves 2–3 move the *math* onto entries while the *flow* between them stays staged until shape-generic admission lands. |

**Migration stance** (Waves 1–3, census §4): annotation/method-twin swaps
first (zero-body-change functions), then one production chain (llama/
SmolLM2 prefill) off the carrier, then program composition. The radix
admissions list (shape-generic entries, broadcast-elementwise, device
layernorm, NEOX rope, device ln/lse, lane `sign`) is the dependency table —
see the [campaign waves](CAMPAIGN.md#waves).

**Terminology law** (collision discipline): `NumericBlock` never means a
transformer block. "Block" in transformer sense (`transformer_block`,
`CachedBlock`, decoder block weights) and in format/tiling sense (GGUF
dtype block rules) are different words sharing letters. Files that touch
both senses carry a disambiguation doc comment at first touch — landed in
`decode.fab` and `cache.fab` this wave; the class doc in `tensor.fab`
carries the note for every reader.

## 3. Scope decisions recorded (this wave)

| Decision | Ruling | Reason |
| --- | --- | --- |
| Error vocabulary | `TensorError` **stays** (also `TensorFailure` arms, `MissingTensor`, `GgufTensorDescriptor`, `SafetensorsTensorDescriptor`, `TensorView`, `TensorPayload`, … untouched) | Errors and artifact-format descriptors are a different question from the carrier name; renaming them is not this wave and would blur the census's seam. |
| Module name | `tensor.fab` / `gradus:tensor` **keeps its name** | The import path is public API consumed by every module and the exempla; the module hosts the construction/dtype admission seam, not only the class; a rename would churn every import line for zero behavioral gain and complicate the identical-outcome proof. A split may ride a later wave if the admissions surface grows its own module. |
| Struct-literal construction | Retired at internal sites (→ `tensor.stage`) | Every carrier must carry the stride/count cache; required (defaultless) `numel`/`strides` fields make bypassing the constructor family a compile error. |
| `stage` visibility | Public, documented as trusted-input staging | Cross-module internal producers exist (math/nn/attention/moe); external data still enters only through the validating constructors. |

## 4. Delivery record

### 4.1 Rename (converter-driven)

- 2,051 `NumericBlock` references now stand where `Tensor` stood:
  src 1,377 (`.fab` + `.proba`), exempla 404, docs 270
  (`docs/api-reference.md`, `docs/api-shape-policy.md`).
- Construction sites: 158 pre-existing constructor calls unchanged
  (`tensor.default` 113, `tensor.construct` 35, `tensor.fill` 5,
  `tensor.construct_dtype` 5) + 26 struct literals converted to
  `tensor.stage(...)` (math 13, nn 5, attention 4, moe 4).
- Converter: word-boundary regex (`tensor.Tensor` → `tensor.NumericBlock`;
  bare `Tensor` → `NumericBlock` with hyphen-compound and artifact-sense
  protections), then per-file `faber check`; hand review of every
  borderline prose site (safetensors "Tensor data_offsets" and
  "Tensor-descriptor", GGUF "753-Tensor Map", "Tensor-level coverage",
  "Tensor-type coverage" kept — artifact-format senses, not the class).
- Diff: 59 files, +1,627 / −1,549 lines, at `500342d`.

### 4.2 Stride cache (the perf rider)

`NumericBlock` gains required `int numel` + `list<int> strides` fields,
computed once in every constructor (`construct_dtype`, `fill`, `default`,
`stage`; helper `_strides`). `get()` is the row-major dot of indices with
the cached strides — identical arithmetic to the former per-call stride
walk (same bounds checks, same error order, same messages);
`numel()`/`valid()` read the cache. Zero-size shapes keep the
`empty tensor` get() failure; `_strides` never divides by a zero dim.

**Measurement** — decode logits handoff (`generation._last_logits`
pattern: the per-generated-token vocab-row walk through
`carrier.get([rows-1, i])`; bench mirrors it at vocab 49,152, 24 passes =
1,179,648 `get()` calls; `faber run` MIR runner; faber 1.8.0 debug build,
radix 0.83.0; Apple M5 Max, 18 cores, macOS 26.5.2; 3 runs each phase,
median):

| Phase | Median wall | Per get() |
| --- | --- | --- |
| before (HEAD `a39eefe`) | 87.47 s (88.02 / 87.47 / 87.28) | ≈ 74.1 µs |
| after (`500342d`) | 50.06 s (50.00 / 50.06 / 50.14) | ≈ 42.4 µs |

**1.75× (−42.8% wall)** on the walked path, bit-identical accumulator
(589824.0 both phases). In per-token terms the logits handoff drops
≈ 3.64 ms → ≈ 2.08 ms on this interpreter tier — the CPU/FMIR
reference-level number for the operator's tokens/sec thread (device
throughput remains NGAB's to measure, per `docs/benchmark-method.md`).
Bench source: `/tmp/w0_bench/bench_logits.fab` (session scratch; the
workload is four lines to reproduce from `generation.fab:_last_logits`).

### 4.3 Validation evidence

- `faber check` green: every `src/**/*.fab` (43 files), the package root,
  `./scripta/check-compile` (10 gated exempla + library), and 23/27 exempla
  packages individually.
- Pre-existing reds unchanged (verified against a HEAD worktree):
  `dense-block`/`dense-gqa`/`dense-model` (SEM010 list-literal equality —
  fails identically in isolation, untouched lines) and
  `kernel-byte-params-red` (PKG001 staged kernel script). Also pre-existing
  and untouched: `./scripta/check-source` no-Latin findings
  (`octeti`/`conversio`) and `tests/admission_conformance.fab`
  (`safetensors.message` SEM004) — outside this wave's write scope.
- **Proba identical-outcome**: all 42 non-tokenizer `.proba` suites run
  per-file before and after — case-level results identical (pass/fail/
  blocked/analysis-error patterns match; the only textual drift is
  warning-occurrence counts in the dense/moe analysis inventories:
  LOCALE002 1303→1286, WARN003 96→97 — inventory notes, not outcomes).
  `tokenizer.proba` is **not runtime-compared**: its import chain
  (tokenizer → model/gguf_manifest → model/artifact) contains no
  `gradus:tensor` edge, so the suite cannot observe the carrier rename or
  stride cache; a confirmatory before/after pair was launched, then
  discarded — the baseline worktree was cut after the rename commits
  (construction error, caught before use) and the concurrent U4b
  campaign began mutating `src/tokenizer.proba` mid-flight. The 42
  compared suites include every file that imports the carrier.

### 4.4 Digest re-adjudication (radix)

The GEA2 `GRADUS_SOURCE_LINEAGE` digests cover gradus **source bytes**
(SHA-256 of the `.fab` files). This wave changed three of the four lineage
files (`transformer.fab`, `attention.fab`, `nn.fab`; `dense_llama.fab` is
byte-identical — its `Tensor` hits are all longer identifiers). Re-pinned
explicitly in `radix` at `9e5070d76` (const + manifest `source_lineage`,
annotations citing this wave and the identity proof: proba identical-outcome
per file, `faber check` green tree-wide, diff is a pure rename + the stride
cache with bit-identical arithmetic). Precedent: `e5e484ec8`. Never silent.

### 4.5 Residuals (routed, not hidden)

- **`inferentia`** still references `tensor.Tensor` at 54 sites in 3 files
  (`src/main.fab`, `evidence/live-run/src/main.fab`,
  `tests/generate-gate/src/main.fab`) — outside this wave's declared paths
  (gradus + radix re-pin); those packages will not check until a follow-up
  unit applies the same converter there. Reported to mind for routing.
- Dense exempla SEM010 reds and the U4a proba-message analysis errors are
  pre-existing campaign surfaces, untouched by this wave.
- The `stage` constructor is new public surface on `gradus:tensor`
  (documented in `docs/api-reference.md`); if a later wave splits the
  admissions module, `stage` is the seam to revisit.
