# Delivery: GGUF-A3 — Checked Packed Storage And Tensor Materialization (Qwen LIB-03)

**Status**: re-split 2026-08-14 by planner-23 (task `5655bca9`) — GGUF-A1c (LIB-01) landed at main `2b3e41a` and A3-C1 landed at main `82048b5` (merge `24928b9`); the 2026-08-13 entry gate is **OPEN**. C2 and C3 are re-lowered into **12 dispatch-ready one-behavior-family micro-units** per operator directive 2026-08-14 (granularity bar: ~10–15 min per unit, all 8 campaign-rule-2 fields). Planning artifact only: no product code is written by this revision.
**Campaign**: [`CAMPAIGN.md`](CAMPAIGN.md) — PML5-GGUF Qwen3.6 invariant; umbrella Radix `gpu-production-readiness` row **LIB-03**
**Delivery authority**: [`pml5-general-gguf-delivery.md`](pml5-general-gguf-delivery.md) — unit **GGUF-A3** ("Packed Storage And Reference Materialization")
**Repo**: `gradus` (branch `factory/planner-23`, baseline `bc500993c97b99bb4ca3ff0d98828b56c750eec0`); planning docs only
**Goal chain (goal-check)**: umbrella goal `gol_634a0417d02c510f` (Qwen3.6 35B GGUF execution — sole priority) -> PML5-GGUF delivery-authority goal `gol_67b635603712f01` -> this unit. Both goals are registered in Vivi (`vivi board` 2026-08-13). **Goal-check: PASS — no new goal or forge needed**; this lowering is the delivery-level unit spec under the existing registered chain.
**Freshness**: derived independently from the campaign, the delivery authority, and the live product repos; no planner-1..19 worktree, commit, partial artifact, or cancelled transcript was read.

## Unit Identity

| Field | Value |
| --- | --- |
| Umbrella row | **LIB-03** — "Implement checked packed storage and tensor materialization" |
| Umbrella done oracle | Every target tensor required by execution has a validated range, shape, layout, and bounded materialization path |
| Delivery unit | **GGUF-A3** — Packed Storage And Reference Materialization |
| Delivery done oracle | Every tensor required by the Qwen3.6 forward graph has a checked range, shape, storage layout, and bounded materialization path; selected tensor slices match the independent oracle |
| Owner | Gradus |
| Depends on | **LIB-01 (GGUF-A1c)** — capsule/caller clean break (entry gate, see §Predecessor And Entry Gate) |

## Outcome (exact executed result)

The unit lands a public `gradus:*` packed-storage/materialization surface that

1. separates **logical dtype** (f32 compute values) from **physical storage** (per-tensor GGML type),
2. binds one `GgufTensorDescriptor` + one validated `TensorPayload` at a time into a typed tensor view with the full shape (ranks 1–3; rank-3 expert tensors explicit),
3. implements **every physical layout used by the four mandatory artifacts** — the union set **{F32, BF16, Q5_0, Q8_0, Q4_K, Q5_K, Q6_K}** — by extending the existing CPU dequant codecs with **BF16** and **Q5_K** (the two layouts present in the Qwen3.6 completion row and missing today),
4. materializes bounded logical-element windows to f32 in GGUF block order, reading payload sub-windows through the operation-scoped range source (never a whole-model, whole-tensor, or unbounded byte list), and
5. proves **selected tensor slices match the independent oracle** (llama.cpp `ggml-quants.c` @ pinned `a957b7747`, bit-exact f32) through an executed package-MIR exemplar against the real local Qwen3.6 artifact plus deterministic in-repo fixtures.

Whole-model conversion to F32 is **not** an admitted execution path: there is no public operation that materializes the model or any unbounded tensor as f32. Each materialization call is a bounded window.

## Ground Truth (verified live 2026-08-13)

Baseline state (gradus `bc500993c97b`, tree clean; `./scripta/check-source` PASS). Codec facts below are superseded by the C1 landing (`82048b5` — see §Predecessor And Entry Gate); the manifest/dtype facts remain current:

- `gradus:model/gguf_manifest` (GGUF-A1a/A1b) already provides: format-general `GgufManifest`, `GgufTensorDescriptor` (name, shape, typo_ggml, offset_relativum, elements, `GgmlLayout`), `inveni_tensorem`, checked absolute-range validation and overlap rejection in `_construct`, `layout(typo_ggml, forma)` resolving `GgmlLayout.Cognita` block geometry for 22 GGML ids, and `read_fragmentum` (checked bounded tensor subrange reads through an operation-scoped `SourceRead`). A1b's guarded `exempla/gguf-inspect` already inspects all six local rows incl. `qwen35moe/753`.
- `gradus:model/dequant` (PML2-U5) provides CPU block/row dequant for the pinned **SmolLM2 row set {F32, Q5_0, Q8_0, Q4_K, Q6_K}** (`dequantize_block`, `dequantize_order`, `block_elements`, `block_bytes`, `DequantError`), bit-exact against the GI2-1 reference semantics (`_dimidium` half decode, `_scala_minima_k4`, left-associative f32 operation order).
- `gradus:dtype` carries the logical `DType` tag {F32, F16, I32, U8}; the materialization view is f32-valued (dequant output), so no new logical dtype is required.
- Local-corpus storage-type distributions (operator evidence, radix `gpu-inference-gguf/evidence/gguf-metadata.txt`; cited read-only):

| Artifact | Arch | Tensors | tensor_types |
| --- | --- | ---: | --- |
| `SmolLM2-360M-Instruct-Q4_K_M.gguf` | `llama` | 290 | F32 65 / Q4_K 16 / Q5_0 176 / Q6_K 16 / Q8_0 17 |
| `Qwen2.5-0.5B-Instruct-Q4_K_M.gguf` | `qwen2` | 290 | **not recorded in shared evidence — derive at unit boundary** |
| `Qwen2.5-1.5B-Instruct-Q4_K_M.gguf` | `qwen2` | 338 | **not recorded in shared evidence — derive at unit boundary** |
| `Qwen3.6-35B-A3B-UD-Q4_K_M.gguf` | `qwen35moe` | 753 | **BF16 2 / F32 368 / Q4_K 82 / Q5_K 38 / Q6_K 4 / Q8_0 259** |

- The Qwen3.6 completion row uses exactly six physical layouts: **BF16, F32, Q4_K, Q5_K, Q6_K, Q8_0**. **C1 landed the two missing codecs (BF16, Q5_K) at `82048b5` — the admitted union set is complete**; what remains is the windowed materialization surface that consumes them.
- Size constraint that shapes the design: the largest Qwen3.6 tensors (e.g. `token_embd.weight`, hundreds of MB of payload) exceed the manifest's single-read `CORPUS_LIMES` of 64 MiB and would produce multi-GB f32 lists. The materialization surface is therefore **windowed**: bounded payload reads + bounded logical-element windows.

## Predecessor And Entry Gate

- **Predecessor receipt**: LIB-01 = **GGUF-A1c** (capsule/caller clean break). **Landed** at main `2b3e41a` (a1c-chain M1–M7, M8R4 aggregate gate, post-integration record correction `aace34b`) — schema 1 has no live constructor or parser caller; schema-2 `artifact.ContentIdentity` + `gguf_manifest` values are the only authority; source, compile, and migrated format probas pass. **The A3 entry gate is OPEN.**
- **C1 receipt**: A3-C1 (BF16 + Q5_K codecs, union-set goldens) landed at main `82048b5` (merge `24928b9`, 2026-08-14; Hand receipt task `3158007b`): check-source/check-compile green, goldens bit-exact 15/15, proba execution FMIR-blocked tree-wide (recorded residual, not a unit defect).
- **Dispatch disposition (2026-08-14 revision)**: C2 and C3 are re-lowered into 12 micro-units (§Implementation Frontier And Split Boundary) — **READY for dispatch, no outstanding gate**. Every unit carries the 8 campaign-rule-2 fields and obeys the operator's granularity bar (one behavior family, ~10–15 min).
- **Executed-tier lever (CTO8-1)**: the FMIR library-call gap remains the named open gate for *executed-token/model identity* claims. This unit's executed claims are at the **A1b precedent tier**: package-MIR exemplar receipts with observed PASS lines over real tensor slices and in-repo fixtures. No token, logit, model-execution, or device claim is made here; full executed-model identity remains gated on CTO8-1 (GGUF-A4+).

## First Failing Oracle

The first red case the implementing Hand writes before any codec change, per red-green:

```text
case q5k-block-dequant-golden:
  dequantize_block(GGML_Q5_K, <Q5_K block fixture bytes>)
  → must equal the golden f32 block values (bit-exact, llama.cpp a957b7747 order)
  current: TypoIgnotum (un-admitted GGML type id: 13)  ← RED
```

then the BF16 twin case (`GGML_BF16`), then the windowed-materializer boundary cases (requested element window and payload window exceed bounds → typed error; block-aligned windows only), then the rank-3 expert slice case. All fail closed until the extended codecs and the view/materializer surface land. The codec oracles above are **landed** with C1 (`82048b5`); each C2/C3 micro-unit's own first-failing oracle is in §Implementation Frontier And Split Boundary.

## Public Surface (frozen for this unit)

The exact spellings below follow the codebase's Faber Latin convention and the A1a amendment precedent (`inveni_tensorem`). Any spelling change at implementation routes through the delivery-amendment path; no compatibility alias is added.

### `gradus:model/tensor_payload` — new module `src/model/tensor_payload.fab` + `.proba`

```text
genus TensorPayload {
    textus name                  # descriptor name this payload binds to
    numerus absolute_start     # absolute byte offset into the content identity
    numerus length             # exact stored byte length of these bounded bytes
    octeti bytes                  # bounded bytes for that range
}
discretio PayloadError {
    NomineIgnota { textus message }
    RangeMala { textus message }
    LongitudoMala { textus message }
}
functio message(PayloadError) → textus
```

`TensorPayload` carries no path, URL, reader, file handle, mapping, device object, or whole-model byte list (delivery clean-boundary). Bytes are bounded by the read window that produced them; the value validates its own range facts against a `GgufTensorDescriptor` when bound.

### `gradus:model/tensor_view` — new module `src/model/tensor_view.fab` + `.proba`

```text
genus TensorView {
    textus name                  # descriptor name
    lista<numerus> shape          # full GGUF shape; rank 3 = expert tensor, kept explicit
    numerus typo_ggml             # physical storage type id
    numerus elements              # logical element count
    GgmlLayout layout             # Cognita (known) or Ignota (inspectable, not materializable)
    numerus absolute_start     # absolute start of the tensor payload
    numerus longitudo_payloadis   # exact stored byte length (Cognita.longitudo_octetorum)
}
discretio ViewError {
    NomineIgnota { textus message }
    RangeMala { textus message }
    LongitudoMala { textus message }
    LayoutIgnota { textus message }
    TypoIgnotum { textus message }
    OrdoMala { textus message }
    LimitesMala { textus message }
}
functio message(ViewError) → textus

# Bind one descriptor + one validated payload into the typed view. Fails closed
# on unknown name, absolute-range mismatch (payload.absolute_start must equal
# data_inceptum + offset_relativum), stored-length mismatch, unknown layout, or
# un-admitted physical type.
functio links(GgufManifest m, TensorPayload p) → TensorView ⇥ ViewError

# Materialize a bounded logical-element window to f32 in GGUF block order.
# start/length are element-aligned (block-boundary checked); the payload
# sub-windows are read through the operation-scoped source and each stays at or
# under the manifest CORPUS_LIMES. The requested element window is capped at
# MAXIMUM_SLICEM_ELEMENTA (16,777,216 = 64 MiB f32); larger consumption is the
# caller's windowed loop. No whole-tensor or whole-model call exists.
functio materialize_slice(TensorView v, numerus initium_elementum,
    numerus longitudo_elementum, (numerus, numerus) → SourceRead fons)
    → lista<f32> ⇥ ViewError

# Materialize one complete block by block index (the dequant-block probe).
functio materialize_block(TensorView v, numerus index_glomuli,
    (numerus, numerus) → SourceRead fons) → lista<f32> ⇥ ViewError
```

`ViewError.TypoIgnotum` mirrors the dequant fail-closed rule (un-admitted physical type before any byte is touched); `LayoutIgnota` mirrors `GgufManifestError.LayoutIgnota` (unknown codec stays inspectable, never materialized). `TensorView` never retains a path, reader, or source function.

### `gradus:model/gguf_manifest` — additive accessor in the existing module

```text
# Exact stored byte range of one known-layout tensor: (absolute_start,
# longitudo_payloadis) relative to the content identity. Ignota layout fails
# closed. Reuses the already-validated range/overlap facts from parse/inspect.
functio limes_payloadis(GgufManifest m, textus nomen)
    → (numerus, numerus) ⇥ GgufManifestError
```

No existing manifest behavior changes; the A1b proba surface stays green.

### `gradus:model/dequant` — extended admitted set

The admitted physical set widens from **{F32, Q5_0, Q8_0, Q4_K, Q6_K}** to **{F32, BF16, Q5_0, Q8_0, Q4_K, Q5_K, Q6_K}**:

- **BF16** (`GGML_BF16 ← 30`, 1 element/block, 2 bytes/block): value-arithmetic bf16→f32 (sign/8-bit exponent/7-bit mantissa via the `_power_two` seam — bit-exact for every finite bf16; Inf via f64 overflow-narrowing; NaN fails closed `ValorMala`), mirroring llama.cpp's bf16 row conversion.
- **Q5_K** (`GGML_Q5_K ← 13`, 256 elements/block, 176 bytes/block): `dequantize_row_q5_K` — d/dmin halves + `get_scale_min_k4` (the existing `_scala_minima_k4` helper) + qh[32] + qs[128], same f32 operation order, bit-exact.
- `block_elements` / `block_bytes` grow the two rows; the dequant layout constants are cross-checked against `GgmlLayout.Cognita` at the view-binding boundary (the manifest is the single layout authority — dequant validates, never re-derives independently).

## Write Scope (exact)

All paths under the implementing Hand's gradus worktree on `factory/planner-23`; gradus is a dedicated-agent repo added per task via `--repos gradus`:

- `src/model/tensor_payload.fab`, `src/model/tensor_payload.proba` (create)
- `src/model/tensor_view.fab`, `src/model/tensor_view.proba` (create)
- `src/model/dequant.fab`, `src/model/dequant.proba` (extend: BF16 + Q5_K codecs, layout cross-check, widened admitted set) — **C1 landed the codecs and the widened admitted set (`82048b5`); the remaining A3 touch is the dequant layout cross-check at the view-binding boundary (C2-U3)**
- `src/model/gguf_manifest.fab`, `src/model/gguf_manifest.proba` (add `limes_payloadis` only)
- `fixtures/gguf/gen_dequant_goldens.py` + `fixtures/gguf/gguf-dequant-goldens.json` (create; deterministic block fixtures for the union set, schema `gguf-dequant-goldens-v2`) — **C1 landed (schema v2 present); no further fixture-json touch**
- `fixtures/gguf/gguf-dequant-goldens-oracle.md` (create; derivation contract: llama.cpp `ggml-quants.c` @ `a957b7747`, generator command, SHA-256 pins) — **not yet landed; created in C3-U5**
- `exempla/gguf-materialize/faber.toml`, `exempla/gguf-materialize/src/main.fab`, `exempla/gguf-materialize/README.md` (create; app-owned file adapter + real-file slice receipt, mirroring `exempla/gguf-inspect`)
- `scripta/check-compile` and `scripta/check-compile.fab` (add the `gguf-materialize` exemplar target) — **the bash launcher is the live gate; C3-U1 extends it (the `.fab` variant is not an execution surface — see Open Item 4)**
- Docs: `README.md` (module/surface list), `docs/module-map.md` (two new module rows + counts), `docs/api-reference.md` (new `tensor_payload`/`tensor_view` sections; dequant section widened to the union set), `docs/diagnostics.md` (new `PayloadError`/`ViewError` tables; `DequantError` rows for the new codecs), `docs/regression-corpus.md` (bump the corpus version — next after `v1.3.0`; new proba suites + goldens), `docs/factory/production-ml-library/pml0-symbol-inventory.md` (new public symbols + module counts), `docs/factory/production-ml-library/pml0-support-matrix.md` (storage/materialization rows at the **output-checked slice tier** — see §Validation), and the owning delivery/status docs (`pml5-general-gguf-delivery.md` GGUF-A3 section marked implemented + gradus `CAMPAIGN.md` status line) at the unit's closeout.
- Closeout commit on `factory/planner-23` (gradus lane).

## Read Scope

- `pml5-general-gguf-delivery.md` (GGUF-A3/A4/A7 + clean boundary), gradus `CAMPAIGN.md`
- Live `src/model/gguf_manifest.fab` / `dequant.fab` / `dtype.fab` / `tensor.fab` / `shape.fab`
- `exempla/gguf-inspect` (the file-adapter + operation-scoped range pattern to mirror)
- Radix evidence cited read-only: `gpu-inference-gguf/evidence/gguf-metadata.txt` (corpus type distributions), `gi2-dequant-reference.py` + `gi2-dequant-goldens.json` (dequant oracle semantics), `gi4-delivery.md` §CTO8-1 (executed-tier lever state)
- `fixtures/gguf/gguf-row-oracle.md`, `general-manifest-oracle.md`, `gen_manifest_fixtures.py` (fixture/oracle conventions)

## Forbidden Scope

- No tokenizer work (GGUF-A2/LIB-02 — parallel-safe sibling), no model assembly/forward (GGUF-A4+), no KV/decode/sampling/generation (PML5 U1–U6 surfaces), no admission/tensor-map (GGUF-M1), no GPU/lowering/kernel/`DeviceProgram` (Radix), no physical storage/upload/residency (Hosts), no HTTP/serving (product repo), no changes to `src/model/capsule.fab` / `gguf.fab` / `safetensors.fab` (LIB-01's A1c clean-break scope — the A3 Hand works against the post-A1c authority and never re-opens the capsule), no edit to `pml5-general-gguf-delivery.md` beyond the GGUF-A3 closeout lines, no CAMPAIGN-semantics edits, no whole-workspace cargo/nextest in-loop (narrow `faber check` + one closeout run per boundary), no foreign dirt, no write to the main checkout or any other worktree.

## Implementation Frontier And Split Boundary

Re-split **2026-08-14** (planner-23, task `5655bca9`): the C1 grain — one
70-minute bag across 4 files with a latent-bug detour (`_scala_minima_k4`) —
was rejected by the operator. C2 and C3 are re-lowered here into
**one-behavior-family micro-units** (~10–15 min each, all 8 campaign-rule-2
fields). C1 is landed and kept as-is (receipt in §Predecessor And Entry Gate).
The mandatory scope of §Write Scope and §Public Surface is unchanged: every
path and behavior lands; nothing is narrowed, deferred, or made optional.

Split-on-boundary rules stay: each micro-unit lands as one commit; no dual
authority ever exists between units; the shared `src/model/` tree stays
hunk-serialized against the sibling LIB-02 Hand via landed-commit boundaries.
In the closeout commands below, `$WS` is the workspace root (e.g.
`/Users/ianzepp/work/faberlang/worktrees/hand-N`) and `$GRADUS` = `$WS/gradus`.

### C2 — payload, view, bounded materializer (5 micro-units)

```text
A3-C1 (landed 82048b5)
  ├─→ C2-U1 limes_payloadis (gguf_manifest.fab) ─┐
  └─→ C2-U2 tensor_payload module ────────────────┼─→ C2-U3 tensor_view + links
                                                  └──→ C2-U4 materialize_slice
                                                        └──→ C2-U5 materialize_block
```

C2-U1 ∥ C2-U2 are file-disjoint (parallel-safe); C2-U3 → C2-U5 are serial on
`src/model/tensor_view.fab`/`.proba`.

**C2-U1 — `limes_payloadis` payload-range accessor**
- **outcome**: one additive accessor on the existing `gradus:model/gguf_manifest`:
  `limes_payloadis(GgufManifest m, textus nomen) → (numerus, numerus) ⇥ GgufManifestError`
  returning the exact stored byte range `(absolute_start, longitudo_payloadis)`
  of one known-layout tensor, reusing `inveni_tensorem` + the already-validated
  `Cognita` facts (no new layout derivation); unknown name fails closed via the
  `inveni_tensorem` passthrough (`WireMala`); `Ignota` layout fails closed
  (`LayoutIgnota`). Marked `@ publica` per the landed post-visibility-flip
  convention.
- **write_scope**: `src/model/gguf_manifest.fab`, `src/model/gguf_manifest.proba`
- **first_failing_oracle**: proba case
  `manifestum.limes_payloadis(m, "token_embd.weight")` fails to compile (symbol
  absent) → RED.
- **closeout**: `cd $GRADUS && env FABER_LIBRARY_HOME=$WS $WS/radix/target/debug/faber check .` + `git diff --check -- src/model/gguf_manifest.fab src/model/gguf_manifest.proba`
- **expected_observed_result**: `faber check` ends `ok: .`; the accessor and its
  proba cases type-check; `git diff --check` silent.
- **est_basis**: mirrors the `inveni_tensorem`/`read_fragmentum` accessor seam
  (offset + checked-arithmetic pattern); ~25 fab lines + ~40 proba lines; no new
  error variant. ~12 min.
- **stop_condition**: if the accessor needs a range fact the manifest does not
  already carry at parse time, stop and route — the manifest is the single
  layout authority; never re-derive layout independently.
- **depends_on**: A3-C1 (landed `82048b5`)

**C2-U2 — `tensor_payload` module (value + diagnostics)**
- **outcome**: new module `gradus:model/tensor_payload`:
  `genus TensorPayload { textus name, numerus absolute_start, numerus length, octeti bytes }`,
  `discretio PayloadError { NomineIgnota, RangeMala, LongitudoMala }`,
  `message(PayloadError) → textus`; all `@ publica`. The value carries no path,
  URL, reader, handle, or whole-model byte list (delivery clean boundary).
- **write_scope**: `src/model/tensor_payload.fab`,
  `src/model/tensor_payload.proba` (both new)
- **first_failing_oracle**: proba `importa ex "gradus:model/tensor_payload"` fails
  to compile (module absent) → RED.
- **closeout**: `cd $GRADUS && env FABER_LIBRARY_HOME=$WS $WS/radix/target/debug/faber check .` + `git diff --check -- src/model/tensor_payload.fab src/model/tensor_payload.proba`
- **expected_observed_result**: `faber check` ends `ok: .`; payload construction
  and all three `PayloadError` `message` renderings type-check.
- **est_basis**: value + 3-variant error + `message` ≈ the `artifact.fab` module
  pattern; ~50 lines + ~45 proba lines. ~12 min.
- **stop_condition**: if a field would carry a path/reader/device object or a
  whole-model byte list, stop (clean boundary).
- **depends_on**: A3-C1 (landed `82048b5`)

**C2-U3 — `tensor_view` module (value, diagnostics, `links` binding)**
- **outcome**: new module `gradus:model/tensor_view`: `genus TensorView`
  (frozen field list), `discretio ViewError` (frozen 7 variants), `message`, and
  `links(GgufManifest m, TensorPayload p) → TensorView ⇥ ViewError` —
  bind one descriptor + one validated payload into the typed view with the full
  fail-closed matrix: unknown name → `NomineIgnota`; absolute-range mismatch
  (`payload.absolute_start` vs the `limes_payloadis` start) → `RangeMala`;
  stored-length mismatch (vs `Cognita.longitudo_octetorum`) → `LongitudoMala`;
  `Ignota` layout → `LayoutIgnota`; un-admitted physical type (dequant
  `block_elements` cross-check — the manifest stays the single layout
  authority) → `TypoIgnotum`. All `@ publica`.
- **write_scope**: `src/model/tensor_view.fab`, `src/model/tensor_view.proba`
  (both new)
- **first_failing_oracle**: proba `tensor_view.links(m, p)` fails to compile
  (module absent) → RED.
- **closeout**: `cd $GRADUS && env FABER_LIBRARY_HOME=$WS $WS/radix/target/debug/faber check .` + `git diff --check -- src/model/tensor_view.fab src/model/tensor_view.proba`
- **expected_observed_result**: `faber check` ends `ok: .`; the positive bind and
  each of the five fail-closed cases type-check.
- **est_basis**: one bind with five fail-closed branches reusing
  `limes_payloadis` + `inveni_tensorem` + dequant layout facts; ~90 lines + ~70
  proba lines. ~15 min.
- **stop_condition**: if binding would retain the source callback or read payload
  bytes, stop — windowed materialization is C2-U4's behavior family.
- **depends_on**: C2-U1, C2-U2

**C2-U4 — `materialize_slice` windowed materializer + cap**
- **outcome**: add `MAXIMUM_SLICEM_ELEMENTA ← 16777216` and
  `materialize_slice(TensorView v, numerus initium_elementum, numerus longitudo_elementum, (numerus, numerus) → SourceRead fons) → lista<f32> ⇥ ViewError`:
  element-window bounds check → `LimitesMala`; block-alignment check via
  `Cognita.elementa_per_blockum` → `OrdoMala`; window cap → `LimitesMala`;
  per-block payload sub-window reads through the operation-scoped source (source
  failure → `RangeMala`); `dequantize_block` assembly in GGUF block order.
  Each sub-window is one block (≤ `CORPUS_LIMES`); no whole-tensor or
  whole-model read path exists.
- **write_scope**: `src/model/tensor_view.fab`, `src/model/tensor_view.proba`
  (extend)
- **first_failing_oracle**: proba
  `tensor_view.materialize_slice(v, 0, 256, fons)` fails to compile (symbol
  absent) → RED.
- **closeout**: `cd $GRADUS && env FABER_LIBRARY_HOME=$WS $WS/radix/target/debug/faber check .` + `git diff --check -- src/model/tensor_view.fab src/model/tensor_view.proba`
- **expected_observed_result**: `faber check` ends `ok: .`; the positive window
  and the misaligned / over-cap / source-failure cases type-check.
- **est_basis**: the windowed loop is the `dequantize_order` pattern over a
  source callback (the `read_fragmentum` seam) with three bound checks;
  ~100 lines + ~60 proba lines. ~15 min.
- **stop_condition**: if the forward graph needs a window above
  `MAXIMUM_SLICEM_ELEMENTA` or a sub-window above `CORPUS_LIMES`, record with
  the consuming successor (GGUF-A4/M-rungs) and escalate — the bounded-window
  design is the contract, not a negotiable ceiling.
- **depends_on**: C2-U3

**C2-U5 — `materialize_block` single-block probe**
- **outcome**: add
  `materialize_block(TensorView v, numerus index_glomuli, (numerus, numerus) → SourceRead fons) → lista<f32> ⇥ ViewError`:
  block-index bounds check (`LimitesMala` when `index_glomuli` ≥ block count),
  one-block payload sub-window read, `dequantize_block` result.
- **write_scope**: `src/model/tensor_view.fab`, `src/model/tensor_view.proba`
  (extend)
- **first_failing_oracle**: proba `tensor_view.materialize_block(v, 0, fons)`
  fails to compile (symbol absent) → RED.
- **closeout**: `cd $GRADUS && env FABER_LIBRARY_HOME=$WS $WS/radix/target/debug/faber check .` + `git diff --check -- src/model/tensor_view.fab src/model/tensor_view.proba`
- **expected_observed_result**: `faber check` ends `ok: .`; the first-block probe
  and the out-of-range index case type-check.
- **est_basis**: thin wrapper over the C2-U4 read path; ~25 lines + ~40 proba
  lines. ~10 min.
- **stop_condition**: same as C2-U4 — never a whole-tensor read.
- **depends_on**: C2-U4

### C3 — exempla receipt + docs + closeout (7 micro-units)

```text
C2-U5 ──┬─→ C3-U1 exempla fixture mode + check-compile wiring ──→ C3-U2 exempla real-file mode + receipt
        ├─→ C3-U3 api-reference + diagnostics re-baseline
        ├─→ C3-U4 module-map + README surface lists
        └─→ C3-U5 regression-corpus + goldens-oracle docs
              └─→ C3-U6 symbol-inventory + support-matrix (also after C3-U2)
                    └─→ C3-U7 delivery/CAMPAIGN status + full closeout gate
```

C3-U1 ∥ C3-U3 ∥ C3-U4 ∥ C3-U5 are file-disjoint and parallel after C2-U5;
C3-U2 is serial after C3-U1 (extends its `main.fab`); C3-U6 needs the C3-U2
receipt for the support-matrix tier; C3-U7 closes.

**C3-U1 — exempla/gguf-materialize fixture mode + check-compile wiring**
- **outcome**: create `exempla/gguf-materialize/` (`faber.toml` +
  `src/main.fab`) as the app-owned file adapter (the `gguf-inspect` pattern):
  resolve one GGUF path, `inspect` the manifest, bind + materialize named
  tensor slices via `links`/`materialize_slice`, print observed PASS lines.
  First cut proves slices of the committed
  `fixtures/gguf/smollm2-360m-scaled-row.gguf` (deterministic data region;
  F32/Q8_0/Q4_K tensors). Wire the `gguf-materialize` block into
  `scripta/check-compile` (bash launcher — the live gate, per the
  gguf-manifest/gguf-inspect precedent).
- **write_scope**: `exempla/gguf-materialize/faber.toml`,
  `exempla/gguf-materialize/src/main.fab` (new), `scripta/check-compile`
- **first_failing_oracle**: `faber check $GRADUS/exempla/gguf-materialize` errors
  (package absent) → RED.
- **closeout**: `cd $GRADUS && env FABER_LIBRARY_HOME=$WS $WS/radix/target/debug/faber check .`; `env FABER_LIBRARY_HOME=$WS $WS/radix/target/debug/faber check exempla/gguf-materialize`; `env FABER_LIBRARY_HOME=$WS $WS/radix/target/debug/faber run --target fmir exempla/gguf-materialize -- fixtures/gguf/smollm2-360m-scaled-row.gguf`; `git diff --check -- exempla/gguf-materialize scripta/check-compile`
- **expected_observed_result**: both `faber check` runs end `ok: .`; the fixture
  run prints observed PASS lines for the fixture slices with exit 0;
  `git diff --check` silent.
- **est_basis**: mirrors `exempla/gguf-inspect` (adapter + range source + PASS
  printing, ~70 lines) plus the slice table and the
  `links`/`materialize_slice` calls; ~130 lines + `faber.toml` + one
  check-compile block. ~15 min.
- **stop_condition**: if a fixture tensor's type falls outside the admitted set,
  record it and pick an admitted slice — never widen the codec set.
- **depends_on**: C2-U5

**C3-U2 — exempla real-file mode + coverage + receipt**
- **outcome**: extend `exempla/gguf-materialize/src/main.fab` with the real-file
  mode (path + data-offset + sha256 args, the `gguf-inspect` 3-arg form), the
  Qwen3.6 slice table (BF16 ×2, Q4_K, Q5_K, Q6_K, Q8_0, F32, rank-3 expert
  window), bit-exact comparison against the committed
  `fixtures/gguf/gguf-dequant-goldens.json` values, the coverage line
  `PASS coverage tensors=753 known=753 unknown=0 types=…`, and the two Qwen2.5
  dense-row derived distribution lines; execute the guarded run against the
  local Qwen3.6 artifact; write `exempla/gguf-materialize/README.md` (command,
  content identities, slice names/ranges, observed values, dense-row
  distributions).
- **write_scope**: `exempla/gguf-materialize/src/main.fab`,
  `exempla/gguf-materialize/README.md`
- **first_failing_oracle**: the guarded real-file run errors or prints no PASS
  lines (real-file mode absent) → RED.
- **closeout**: `cd $GRADUS && env FABER_LIBRARY_HOME=$WS $WS/radix/target/debug/faber run --target fmir exempla/gguf-materialize -- /Users/ianzepp/ai/models/Qwen3.6-35B-A3B-UD-Q4_K_M.gguf 10991392 0b21525e972670ed59e1812e170b27c26355381f0656ecc4e25617ece7dac58b` + `git diff --check -- exempla/gguf-materialize`
- **expected_observed_result**: one PASS per golden slice (BF16 ×2, Q4_K, Q5_K,
  Q6_K, Q8_0, F32, rank-3 expert) matching the goldens bit-exactly, the coverage
  line 753/753/0, the two dense-row distribution lines, zero FAIL, exit 0; the
  receipt records the exact command and observed values.
- **est_basis**: extends the C3-U1 app with the slice table + golden comparison
  (golden values already committed) + one guarded run + the README receipt;
  ~80 lines + ~60 README lines. ~15 min plus run latency.
- **stop_condition**: a golden mismatch on any slice is a divergence receipt
  naming the first divergent block element (never tolerance-widened); a
  mandatory-artifact layout outside the admitted set is a unit-scope gap with
  the exact tensor and a correction route.
- **depends_on**: C3-U1

**C3-U3 — api-reference + diagnostics re-baseline**
- **outcome**: `docs/api-reference.md` — new `gradus:model/tensor_payload` and
  `gradus:model/tensor_view` sections (the frozen public surface), widen the
  `gradus:model/dequant` section to the union set (BF16/Q5_K layout facts + the
  view-boundary cross-check note); `docs/diagnostics.md` — new
  `PayloadError`/`ViewError` tables and the `DequantError` rows for the two new
  codecs; re-run the committed coverage gate so no public symbol is missing.
- **write_scope**: `docs/api-reference.md`, `docs/diagnostics.md`
- **first_failing_oracle**: `scripta/inventory-public-symbols` fails the
  committed coverage gate (new public symbols without a mention) → RED.
- **closeout**: `cd $GRADUS && ./scripta/inventory-public-symbols` + `env FABER_LIBRARY_HOME=$WS $WS/radix/target/debug/faber check .` + `git diff --check -- docs/api-reference.md docs/diagnostics.md`
- **expected_observed_result**: the inventory gate passes with every new public
  symbol inventoried; `faber check` ends `ok: .`; `git diff --check` silent.
- **est_basis**: two reference docs over an already-landed surface (the A1a/A1b
  module-section pattern); ~60–80 doc lines + one inventory re-baseline.
  ~12 min.
- **stop_condition**: if a doc claim would assert executed value-identity (proba
  execution / FMIR stepper), stop — the reference stays at the compiled-surface
  tier (CTO8-1).
- **depends_on**: C2-U5

**C3-U4 — module-map + README surface lists**
- **outcome**: `docs/module-map.md` — two new module rows
  (`gradus:model/tensor_payload`, `gradus:model/tensor_view`) + updated module/
  function counts; `README.md` — the module/surface list adds the two modules
  and the widened dequant union set.
- **write_scope**: `docs/module-map.md`, `README.md`
- **first_failing_oracle**: the module-map lacks the two new module rows and
  their `functio` counts → RED (counts must match the inventory script).
- **closeout**: `cd $GRADUS && ./scripta/inventory-public-symbols` + `env FABER_LIBRARY_HOME=$WS $WS/radix/target/debug/faber check .` + `git diff --check -- docs/module-map.md README.md`
- **expected_observed_result**: the inventory asserts every module's `functio`
  count including the two new modules; `faber check` ends `ok: .`.
- **est_basis**: two small list/table docs over landed module names; ~20 lines.
  ~10 min.
- **stop_condition**: documents the landed surface only — if a list needs an
  un-landed surface, stop.
- **depends_on**: C2-U5

**C3-U5 — regression-corpus + goldens-oracle contract docs**
- **outcome**: `docs/regression-corpus.md` — bump the corpus version (next after
  the current `v1.3.0`) and inventory the two new proba suites (`tensor_payload`,
  `tensor_view`), the widened `dequant` suite, and the
  `gguf-dequant-goldens.json` / `gguf-dequant-goldens-oracle.md` fixture
  entries; `fixtures/gguf/gguf-dequant-goldens-oracle.md` (new) — the goldens
  derivation contract (llama.cpp `ggml-quants.c` @ `a957b7747` pin, generator
  command, SHA-256 pins) for the C1-landed goldens.
- **write_scope**: `docs/regression-corpus.md`,
  `fixtures/gguf/gguf-dequant-goldens-oracle.md`
- **first_failing_oracle**: the corpus totals are stale against the landed proba
  suite count (suite/fixture totals mismatch) → RED.
- **closeout**: recount `find src -name '*.proba'` totals against the corpus
  inventory + `git diff --check -- docs/regression-corpus.md fixtures/gguf/gguf-dequant-goldens-oracle.md`
- **expected_observed_result**: corpus totals match the landed suites and
  fixtures; the oracle doc pins the derivation; `git diff --check` silent.
- **est_basis**: one table bump + a ~30-line derivation-contract doc over
  C1-landed facts; ~40 lines. ~10 min.
- **stop_condition**: if a pin (commit / SHA-256) cannot be verified against the
  pinned toolchain, record and escalate — no unverifiable pin is committed.
- **depends_on**: C2-U5

**C3-U6 — factory inventory docs (symbol inventory + support matrix)**
- **outcome**: `docs/factory/production-ml-library/pml0-symbol-inventory.md` —
  new public symbols + module counts for the two new modules and the widened
  `dequant`/`gguf_manifest` surfaces;
  `docs/factory/production-ml-library/pml0-support-matrix.md` — storage/
  materialization rows at the **output-checked slice tier** citing the C3-U2
  receipt (never executed-token/model identity — CTO8-1 stays the named gate).
- **write_scope**: `docs/factory/production-ml-library/pml0-symbol-inventory.md`,
  `docs/factory/production-ml-library/pml0-support-matrix.md`
- **first_failing_oracle**: the symbol inventory misses the landed public symbols
  (count mismatch vs `scripta/inventory-public-symbols`) → RED.
- **closeout**: `cd $GRADUS && ./scripta/inventory-public-symbols` +
  `git diff --check -- docs/factory/production-ml-library/pml0-symbol-inventory.md docs/factory/production-ml-library/pml0-support-matrix.md`
- **expected_observed_result**: inventory counts match the landed surface; the
  support-matrix rows classify the output-checked slice tier with the receipt
  link.
- **est_basis**: two factory inventory docs over landed, executed facts; ~50
  lines. ~10 min.
- **stop_condition**: if a support-matrix row would claim executed-token/model
  identity, stop — the tier is output-checked slices only (CTO8-1).
- **depends_on**: C2-U5, C3-U2

**C3-U7 — delivery/CAMPAIGN status closeout + full closeout gate**
- **outcome**: mark the GGUF-A3 section implemented in
  `docs/factory/production-ml-library/pml5-general-gguf-delivery.md`; update the
  gradus `CAMPAIGN.md` status line; run the delivery's declared closeout command
  set (§Closeout Commands And Expected Observed Result) over the whole A3 path
  list and record the receipt; the A3 closeout commit.
- **write_scope**: `docs/factory/production-ml-library/pml5-general-gguf-delivery.md`
  (GGUF-A3 section only), `docs/factory/production-ml-library/CAMPAIGN.md`
  (status line only)
- **first_failing_oracle**: the declared closeout commands fail (e.g.,
  check-compile errors on the `gguf-materialize` exemplar) → RED; nothing claims
  implemented before green.
- **closeout**: the §Closeout Commands command set: `./scripta/check-source`;
  `env FABER_LIBRARY_HOME=$WS FABER_BIN=$WS/radix/target/debug/faber ./scripta/check-compile`;
  the guarded real-file exempla run (C3-U2 form); `git diff --check -- <the full
  A3 path list from §Closeout Commands>`.
- **expected_observed_result**: `check-source` and `check-compile` exit 0; the
  exempla prints the PASS receipt (8 golden slices + coverage + dense-row
  distributions, zero FAIL, exit 0); `git diff --check` silent; the status docs
  describe the observed result exactly.
- **est_basis**: status-line edits + one full closeout run (tool-latency
  dominated); ~10 min of Hand time.
- **stop_condition**: any closeout gate failure is a real finding — record and
  route, never weaken the gate; READY is a readiness verdict, not a GO stamp
  (dispatch stays Mind/operator-owned).
- **depends_on**: C3-U1, C3-U2, C3-U3, C3-U4, C3-U5, C3-U6

### Parallelism and lane boundaries

- Maximum safe parallelism: **4** (C3-U1 ∥ C3-U3 ∥ C3-U4 ∥ C3-U5 after C2-U5);
  C2 opens with 2 (C2-U1 ∥ C2-U2).
- Lane-owned gates unchanged: lint owns stages 1–2; test owns stages 3–6 and
  broad suites; merge owns integration. No micro-unit carries a lane gate on its
  closeout — the narrow `faber check` is the unit gate; the full declared
  command set runs once at C3-U7.

## Oracle And Local Corpus Boundary

- **Independent oracle**: llama.cpp `ggml-quants.c` at the pinned checkout `a957b7747` (the GI2-1 pin), expressed by `gi2-dequant-reference.py` semantics. A3 extends to the union set: deterministic in-repo block fixtures + goldens committed as `fixtures/gguf/gguf-dequant-goldens.json` (schema `gguf-dequant-goldens-v2`), and real-file slice goldens derived at the unit boundary from the local Qwen3.6 artifact and recorded in the exempla receipt.
- **Slice selection (named at the unit boundary from the live manifest)**: the two BF16 tensors (both — they are the only BF16 rows in the artifact), one Q4_K weight slice, one Q5_K slice, one Q6_K slice, one Q8_0 slice, one F32 slice, and one rank-3 expert tensor slice (a bounded per-expert window).
- **Local corpus**: the real artifacts under `/Users/ianzepp/ai/models/` (the four mandatory files + the two additional `qwen35moe` rows) are operator evidence, never committed and never redistributed; Gradus never receives their paths — the exempla's app-owned adapter resolves them (the `gguf-inspect` pattern). The two Qwen2.5 dense rows' exact type distributions are **not in shared evidence**; the unit derives them from the live manifest at its boundary and records them in the coverage record. If a derived layout lies outside the admitted set {F32, BF16, Q5_0, Q8_0, Q4_K, Q5_K, Q6_K}, the unit records a unit-scope gap with the exact tensor and routes a correction — it never guesses or widens the set silently.

## Closeout Commands And Expected Observed Result

**A3 closeout gate (owned by C3-U7).** Each micro-unit's own closeout is the
narrow `faber check` on its touched surface (in the unit definitions in
§Implementation Frontier And Split Boundary); the full declared command set
below runs once at the C3-U7 closeout against the whole A3 path list. From the
Hand packet (substitute the lane worktree paths):

```bash
cd <hand-worktree>/gradus
./scripta/check-source
env FABER_LIBRARY_HOME=<worktree-root> \
  FABER_BIN=<worktree>/radix/target/debug/faber ./scripta/check-compile
env FABER_LIBRARY_HOME=<worktree-root> \
  <worktree>/radix/target/debug/faber run --target fmir exempla/gguf-materialize -- \
  /Users/ianzepp/ai/models/Qwen3.6-35B-A3B-UD-Q4_K_M.gguf 10991392 \
  0b21525e972670ed59e1812e170b27c26355381f0656ecc4e25617ece7dac58b
git diff --check -- src/model/tensor_payload.fab src/model/tensor_payload.proba \
  src/model/tensor_view.fab src/model/tensor_view.proba src/model/dequant.fab \
  src/model/dequant.proba src/model/gguf_manifest.fab src/model/gguf_manifest.proba \
  fixtures/gguf/gen_dequant_goldens.py fixtures/gguf/gguf-dequant-goldens.json \
  fixtures/gguf/gguf-dequant-goldens-oracle.md exempla/gguf-materialize \
  scripta/check-compile scripta/check-compile.fab README.md docs/module-map.md \
  docs/api-reference.md docs/diagnostics.md docs/regression-corpus.md \
  docs/factory/production-ml-library/pml0-symbol-inventory.md \
  docs/factory/production-ml-library/pml0-support-matrix.md \
  docs/factory/production-ml-library/pml5-general-gguf-delivery.md \
  docs/factory/production-ml-library/CAMPAIGN.md
```

**Expected observed result**: `check-source` and `check-compile` exit 0; `faber check` ends `ok: .`; the materialize exemplar prints PASS lines — one per golden slice (BF16 ×2, Q4_K, Q5_K, Q6_K, Q8_0, F32, rank-3 expert) with observed f32 values or value-digests matching the goldens bit-exactly, plus the coverage line `PASS coverage tensors=753 known=753 unknown=0 types=<the six distributions>` and the per-file distribution lines for the two Qwen2.5 dense rows; zero FAIL lines; exit 0. The receipt (in `exempla/gguf-materialize/README.md`) records the exact command, content identities, slice names/ranges, observed values, and the two dense rows' derived distributions. `git diff --check` silent. The support-matrix rows are classified **output-checked** at the tensor-slice level (never executed-token/model identity — CTO8-1 stays the named gate).

## Hardware / Backend Authority

Device-neutral unit. The exempla receipt executes on **burgus** (the local host that produced the A1b receipt; Apple M5 Max, CPU-only reference runs, no backend). No Metal/CUDA/GPU claim; no paid infrastructure; no device handle enters a `gradus:*` value. Backend-native materialization is GGUF-A7/GGUF-M5 territory (Radix/Hosts).

## Successor Preservation Through CLOSE-01

This lowering preserves every mandatory successor; nothing is narrowed, deferred, made optional, or moved outside the campaign:

- GGUF graph: `A1c → A2 ‖ A3`; `A3 → A4` (dense Llama/Qwen full model — consumes materialized dense weights), `A3 → A5` (KV prefill/decode), `A3 → A6` (dense acceptance rows), `A3 → A7` (native quantized execution contract — consumes the packed layout + bounded materialization semantics), `A3 → M1` (qwen35moe admission/tensor map — consumes range/shape/layout facts + per-file type distributions), `M1 → M2` (MoE router/expert execution — consumes rank-3 expert materialization), `M1 → M3` (hybrid SSM/attention), `M2+M3 → M4` (full-model reference), `A7+M4 → M5` (native Metal/CUDA), `M5 → M6` (Faber capstone + closeout).
- Umbrella rows: LIB-03 → REF-01, MODEL-01..04 → EXEC-01..03 → CAP-01/02 → CLOSE-01.
- The unit's surface is the storage/materialization authority those successors consume; A4/M1/M2 read its views rather than re-deriving ranges or re-implementing codecs.

## Scope Closure Statement

- **Milestone advanced**: umbrella **Q1 — executable library inputs** (clean GGUF authority, real tokenizer, packed tensor storage: gates A1c, A2, A3). LIB-03 completes the packed-storage third of Q1.
- **Why unit completion is not campaign completion**: Q4 (the Faber invariant — one public-Gradus capstone running the exact artifact through the complete `qwen35moe` graph for two prompts on Metal and CUDA) requires the full chain LIB-01..CLOSE-01. This unit adds the storage/materialization executed proof at the package-MIR slice tier only; it is not an execution, token, model, or device claim, and Q4 remains mandatory with every clause intact.

## Estimate

- **Micro-unit estimates** (Hand-active minutes, per the granularity bar):
  C2-U1 ~12, C2-U2 ~12, C2-U3 ~15, C2-U4 ~15, C2-U5 ~10, C3-U1 ~15, C3-U2 ~15,
  C3-U3 ~12, C3-U4 ~10, C3-U5 ~10, C3-U6 ~10, C3-U7 ~10. The serial chain
  C2-U1/U2 → C2-U5 bounds wall-clock; C3 opens 4-way parallel after C2-U5.
- **est_work_tokens**: 12 × 2k–4k ≈ 24k–48k total. **est_basis**: per-unit
  basis in the unit definitions (mirrors the landed A1a/A1b and C1 patterns; no
  close ledger class).
- **tool_latency**: medium — per-unit `faber check` (seconds) plus one
  `faber run --target fmir` real-file exempla execution and the
  oracle-derivation step at C3-U2; no cargo, no device runs.

## Stop Conditions / Escalation

- ~~If GGUF-A1c has not landed at the dispatch boundary, the Hand records the recheck and stops~~ — **resolved**: A1c landed at `2b3e41a` and C1 at `82048b5` (see §Predecessor And Entry Gate); the C2/C3 micro-units dispatch against the landed post-A1c authority.
- If a mandatory-artifact layout outside the admitted set appears in the live distributions, the unit records the exact tensor and routes a correction (campaign stop condition) — no silent widening of the codec set.
- A golden mismatch on any slice is a divergence receipt naming the first divergent block element, never a tolerance-widened pass (truth over safety; bit-exact f32 contract).
- A window/materialization bound that would need to exceed `MAXIMUM_SLICEM_ELEMENTA` or `CORPUS_LIMES` for the forward graph is recorded with its consuming successor (GGUF-A4/M-rungs) and escalated — the bounded-window design is the contract, not a negotiable ceiling.

## Open Items For Mind (none blocks this re-split)

1. **GGUF-A1c / A3-C1 landing** — resolved (`2b3e41a` / `82048b5`); the dispatch
   gate recorded by the 2026-08-13 lowering is open.
2. **Qwen2.5 dense-row type distributions** — derived at the C3-U2 boundary
   (evidence gap recorded; low risk given the admitted union set).
3. **Exact public spellings** (`TensorPayload`/`TensorView`/`links`/`materialize_slice`/`limes_payloadis`) — frozen by this lowering per the codebase Latin convention; any amendment routes through the delivery-amendment path (A1a precedent).
4. **`scripta/check-compile.fab` status** — the native-Faber variant is not an
   execution surface (PKG001) and was not extended for the gguf-manifest/
   gguf-inspect exempla; C3-U1 extends the bash launcher (the live gate).
   Whether to retire or resurface the `.fab` variant is a housekeeping question
   for Mind, not an A3 blocker.

---

*Planning artifact only. No product code was written by this revision. LIB-03/GGUF-A3: C1 landed (`82048b5`); C2 and C3 re-lowered into 12 dispatch-ready one-behavior-family micro-units (operator granularity bar, 2026-08-14). The unit preserves every mandatory successor through CLOSE-01 and advances umbrella milestone Q1 without completing the campaign.*
