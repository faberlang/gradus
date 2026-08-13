# Delivery: GGUF-A3 — Checked Packed Storage And Tensor Materialization (Qwen LIB-03)

**Status**: lowered 2026-08-13 by planner-23 (task `67de6722` / handle `e06a6ef5`) — **READY at the spec level; dispatch-gated on LIB-01 (GGUF-A1c) landing**. Planning artifact only: no product code is written by this lowering.
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
2. binds one `DescriptioTensorisGguf` + one validated `TensorPayload` at a time into a typed tensor view with the full shape (ranks 1–3; rank-3 expert tensors explicit),
3. implements **every physical layout used by the four mandatory artifacts** — the union set **{F32, BF16, Q5_0, Q8_0, Q4_K, Q5_K, Q6_K}** — by extending the existing CPU dequant codecs with **BF16** and **Q5_K** (the two layouts present in the Qwen3.6 completion row and missing today),
4. materializes bounded logical-element windows to f32 in GGUF block order, reading payload sub-windows through the operation-scoped range source (never a whole-model, whole-tensor, or unbounded byte list), and
5. proves **selected tensor slices match the independent oracle** (llama.cpp `ggml-quants.c` @ pinned `a957b7747`, bit-exact f32) through an executed package-MIR exemplar against the real local Qwen3.6 artifact plus deterministic in-repo fixtures.

Whole-model conversion to F32 is **not** an admitted execution path: there is no public operation that materializes the model or any unbounded tensor as f32. Each materialization call is a bounded window.

## Ground Truth (verified live 2026-08-13)

Baseline state (gradus `bc500993c97b`, tree clean; `./scripta/check-source` PASS):

- `gradus:model/gguf_manifest` (GGUF-A1a/A1b) already provides: format-general `ManifestumGguf`, `DescriptioTensorisGguf` (name, forma, typo_ggml, offset_relativum, elementa, `LayoutGgml`), `inveni_tensorem`, checked absolute-range validation and overlap rejection in `_constitue`, `layout(typo_ggml, forma)` resolving `LayoutGgml.Cognita` block geometry for 22 GGML ids, and `lege_fragmentum` (checked bounded tensor subrange reads through an operation-scoped `LectioFontis`). A1b's guarded `exempla/gguf-inspect` already inspects all six local rows incl. `qwen35moe/753`.
- `gradus:model/dequant` (PML2-U5) provides CPU block/row dequant for the pinned **SmolLM2 row set {F32, Q5_0, Q8_0, Q4_K, Q6_K}** (`dequantizas_glomulus`, `dequantizas_ordo`, `elementa_glomoris`, `octeti_glomoris`, `DequantError`), bit-exact against the GI2-1 reference semantics (`_dimidium` half decode, `_scala_minima_k4`, left-associative f32 operation order).
- `gradus:dtype` carries the logical `DType` tag {F32, F16, I32, U8}; the materialization view is f32-valued (dequant output), so no new logical dtype is required.
- Local-corpus storage-type distributions (operator evidence, radix `gpu-inference-gguf/evidence/gguf-metadata.txt`; cited read-only):

| Artifact | Arch | Tensors | tensor_types |
| --- | --- | ---: | --- |
| `SmolLM2-360M-Instruct-Q4_K_M.gguf` | `llama` | 290 | F32 65 / Q4_K 16 / Q5_0 176 / Q6_K 16 / Q8_0 17 |
| `Qwen2.5-0.5B-Instruct-Q4_K_M.gguf` | `qwen2` | 290 | **not recorded in shared evidence — derive at unit boundary** |
| `Qwen2.5-1.5B-Instruct-Q4_K_M.gguf` | `qwen2` | 338 | **not recorded in shared evidence — derive at unit boundary** |
| `Qwen3.6-35B-A3B-UD-Q4_K_M.gguf` | `qwen35moe` | 753 | **BF16 2 / F32 368 / Q4_K 82 / Q5_K 38 / Q6_K 4 / Q8_0 259** |

- The Qwen3.6 completion row uses exactly six physical layouts: **BF16, F32, Q4_K, Q5_K, Q6_K, Q8_0**. The current dequant set covers all except **BF16** and **Q5_K** — the two missing codecs are the unit's first implementation frontier.
- Size constraint that shapes the design: the largest Qwen3.6 tensors (e.g. `token_embd.weight`, hundreds of MB of payload) exceed the manifest's single-read `CORPUS_LIMES` of 64 MiB and would produce multi-GB f32 lists. The materialization surface is therefore **windowed**: bounded payload reads + bounded logical-element windows.

## Predecessor And Entry Gate

- **Predecessor receipt**: LIB-01 = **GGUF-A1c** (capsule/caller clean break). Its done oracle: schema 1 has no live constructor or parser caller; schema-2 `artifact.IdentitasContenuti` + `gguf_manifest` values are the only authority; source, compile, and migrated format probas pass.
- **Entry-gate state at the lowering boundary**: GGUF-A1c is **NOT landed** — `pml5-general-gguf-delivery.md` and gradus `CAMPAIGN.md` both record "GGUF-A1c is the next mandatory unit". The A1b receipt (`exempla/gguf-inspect/README.md`, 2026-08-13) is the latest landed proof.
- **Lowering disposition**: this spec is **complete and READY**; dispatch of the implementing Hand is **gated on the A1c receipt** (the affected edge `A1c → A3` blocks; execution rule 6 — no other ready unit is affected, and GGUF-A2/LIB-02 runs parallel-safe on disjoint surfaces). **Recheck handle**: the A1c closeout record in `pml5-general-gguf-delivery.md` / gradus `CAMPAIGN.md` status line.
- **Executed-tier lever (CTO8-1)**: the FMIR library-call gap remains the named open gate for *executed-token/model identity* claims. This unit's executed claims are at the **A1b precedent tier**: package-MIR exemplar receipts with observed PASS lines over real tensor slices and in-repo fixtures. No token, logit, model-execution, or device claim is made here; full executed-model identity remains gated on CTO8-1 (GGUF-A4+).

## First Failing Oracle

The first red case the implementing Hand writes before any codec change, per red-green:

```text
case q5k-block-dequant-golden:
  dequantizas_glomulus(GGML_Q5_K, <Q5_K block fixture bytes>)
  → must equal the golden f32 block values (bit-exact, llama.cpp a957b7747 order)
  current: TypoIgnotum (un-admitted GGML type id: 13)  ← RED
```

then the BF16 twin case (`GGML_BF16`), then the windowed-materializer boundary cases (requested element window and payload window exceed bounds → typed error; block-aligned windows only), then the rank-3 expert slice case. All fail closed until the extended codecs and the view/materializer surface land.

## Public Surface (frozen for this unit)

The exact spellings below follow the codebase's Faber Latin convention and the A1a amendment precedent (`inveni_tensorem`). Any spelling change at implementation routes through the delivery-amendment path; no compatibility alias is added.

### `gradus:model/tensor_payload` — new module `src/model/tensor_payload.fab` + `.proba`

```text
genus TensorPayload {
    textus nomen                  # descriptor name this payload binds to
    numerus initium_absolutum     # absolute byte offset into the content identity
    numerus longitudo             # exact stored byte length of these bounded bytes
    octeti bytes                  # bounded bytes for that range
}
discretio PayloadError {
    NomineIgnota { textus causa }
    RangeMala { textus causa }
    LongitudoMala { textus causa }
}
functio causa(PayloadError) → textus
```

`TensorPayload` carries no path, URL, reader, file handle, mapping, device object, or whole-model byte list (delivery clean-boundary). Bytes are bounded by the read window that produced them; the value validates its own range facts against a `DescriptioTensorisGguf` when bound.

### `gradus:model/tensor_view` — new module `src/model/tensor_view.fab` + `.proba`

```text
genus VisumTensoris {
    textus nomen                  # descriptor name
    lista<numerus> forma          # full GGUF shape; rank 3 = expert tensor, kept explicit
    numerus typo_ggml             # physical storage type id
    numerus elementa              # logical element count
    LayoutGgml layout             # Cognita (known) or Ignota (inspectable, not materializable)
    numerus initium_absolutum     # absolute start of the tensor payload
    numerus longitudo_payloadis   # exact stored byte length (Cognita.longitudo_octetorum)
}
discretio VisioError {
    NomineIgnota { textus causa }
    RangeMala { textus causa }
    LongitudoMala { textus causa }
    LayoutIgnota { textus causa }
    TypoIgnotum { textus causa }
    OrdoMala { textus causa }
    LimitesMala { textus causa }
}
functio causa(VisioError) → textus

# Bind one descriptor + one validated payload into the typed view. Fails closed
# on unknown name, absolute-range mismatch (payload.initium_absolutum must equal
# data_inceptum + offset_relativum), stored-length mismatch, unknown layout, or
# un-admitted physical type.
functio vincula(ManifestumGguf m, TensorPayload p) → VisumTensoris ⇥ VisioError

# Materialize a bounded logical-element window to f32 in GGUF block order.
# initium/longitudo are element-aligned (block-boundary checked); the payload
# sub-windows are read through the operation-scoped source and each stays at or
# under the manifest CORPUS_LIMES. The requested element window is capped at
# MAXIMUM_SLICEM_ELEMENTA (16,777,216 = 64 MiB f32); larger consumption is the
# caller's windowed loop. No whole-tensor or whole-model call exists.
functio materializa_slicem(VisumTensoris v, numerus initium_elementum,
    numerus longitudo_elementum, (numerus, numerus) → LectioFontis fons)
    → lista<f32> ⇥ VisioError

# Materialize one complete block by block index (the dequant-block probe).
functio materializa_glomulum(VisumTensoris v, numerus index_glomuli,
    (numerus, numerus) → LectioFontis fons) → lista<f32> ⇥ VisioError
```

`VisioError.TypoIgnotum` mirrors the dequant fail-closed rule (un-admitted physical type before any byte is touched); `LayoutIgnota` mirrors `GgufManifestError.LayoutIgnota` (unknown codec stays inspectable, never materialized). `VisumTensoris` never retains a path, reader, or source function.

### `gradus:model/gguf_manifest` — additive accessor in the existing module

```text
# Exact stored byte range of one known-layout tensor: (initium_absolutum,
# longitudo_payloadis) relative to the content identity. Ignota layout fails
# closed. Reuses the already-validated range/overlap facts from parse/inspice.
functio limes_payloadis(ManifestumGguf m, textus nomen)
    → (numerus, numerus) ⇥ GgufManifestError
```

No existing manifest behavior changes; the A1b proba surface stays green.

### `gradus:model/dequant` — extended admitted set

The admitted physical set widens from **{F32, Q5_0, Q8_0, Q4_K, Q6_K}** to **{F32, BF16, Q5_0, Q8_0, Q4_K, Q5_K, Q6_K}**:

- **BF16** (`GGML_BF16 ← 30`, 1 element/block, 2 bytes/block): value-arithmetic bf16→f32 (sign/8-bit exponent/7-bit mantissa via the `_potentia_duorum` seam — bit-exact for every finite bf16; Inf via f64 overflow-narrowing; NaN fails closed `ValorMala`), mirroring llama.cpp's bf16 row conversion.
- **Q5_K** (`GGML_Q5_K ← 13`, 256 elements/block, 176 bytes/block): `dequantize_row_q5_K` — d/dmin halves + `get_scale_min_k4` (the existing `_scala_minima_k4` helper) + qh[32] + qs[128], same f32 operation order, bit-exact.
- `elementa_glomoris` / `octeti_glomoris` grow the two rows; the dequant layout constants are cross-checked against `LayoutGgml.Cognita` at the view-binding boundary (the manifest is the single layout authority — dequant validates, never re-derives independently).

## Write Scope (exact)

All paths under the implementing Hand's gradus worktree on `factory/planner-23`; gradus is a dedicated-agent repo added per task via `--repos gradus`:

- `src/model/tensor_payload.fab`, `src/model/tensor_payload.proba` (create)
- `src/model/tensor_view.fab`, `src/model/tensor_view.proba` (create)
- `src/model/dequant.fab`, `src/model/dequant.proba` (extend: BF16 + Q5_K codecs, layout cross-check, widened admitted set)
- `src/model/gguf_manifest.fab`, `src/model/gguf_manifest.proba` (add `limes_payloadis` only)
- `fixtures/gguf/gen_dequant_goldens.py` + `fixtures/gguf/gguf-dequant-goldens.json` (create; deterministic block fixtures for the union set, schema `gguf-dequant-goldens-v2`)
- `fixtures/gguf/gguf-dequant-goldens-oracle.md` (create; derivation contract: llama.cpp `ggml-quants.c` @ `a957b7747`, generator command, SHA-256 pins)
- `exempla/gguf-materialize/faber.toml`, `exempla/gguf-materialize/src/main.fab`, `exempla/gguf-materialize/README.md` (create; app-owned file adapter + real-file slice receipt, mirroring `exempla/gguf-inspect`)
- `scripta/check-compile` and `scripta/check-compile.fab` (add the `gguf-materialize` exemplar target)
- Docs: `README.md` (module/surface list), `docs/module-map.md` (two new module rows + counts), `docs/api-reference.md` (new `tensor_payload`/`tensor_view` sections; dequant section widened to the union set), `docs/diagnostics.md` (new `PayloadError`/`VisioError` tables; `DequantError` rows for the new codecs), `docs/regression-corpus.md` (bump to `gradus-regression-corpus v1.3.0`; new proba suites + goldens), `docs/factory/production-ml-library/pml0-symbol-inventory.md` (new public symbols + module counts), `docs/factory/production-ml-library/pml0-support-matrix.md` (storage/materialization rows at the **output-checked slice tier** — see §Validation), and the owning delivery/status docs (`pml5-general-gguf-delivery.md` GGUF-A3 section marked implemented + gradus `CAMPAIGN.md` status line) at the unit's closeout.
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

Split-on-boundary (each slice a landed commit; no dual authority ever exists between slices):

- **A3-C1 — codec extension (first implementation frontier)**: BF16 + Q5_K in `dequant.fab`, the two `elementa_glomoris`/`octeti_glomoris` rows, the goldens generator + `gguf-dequant-goldens.json` (union set), the dequant proba cases. Independent and first — it is the first missing capability and carries the first failing oracle.
- **A3-C2 — payload + view + bounded materializer**: `tensor_payload.fab`, `tensor_view.fab`, `limes_payloadis`, their probas, the `MAXIMUM_SLICEM_ELEMENTA` bound, the windowed read loop. Consumes C1's codecs; the public surface lands once here.
- **A3-C3 — exempla receipt + docs + closeout**: `exempla/gguf-materialize` real-file slice receipt across the mandatory corpus, `scripta/check-compile` targets, all doc updates, the coverage record, the closeout commit. Closes the unit.

Serial `C1 → C2 → C3`; no parallel children needed (single Hand owns the shared `dequant.fab`/`gguf_manifest.fab` files; sibling LIB-02 Hand is hunk-serialized on the shared `src/model/` tree via landed-commit boundaries).

## Oracle And Local Corpus Boundary

- **Independent oracle**: llama.cpp `ggml-quants.c` at the pinned checkout `a957b7747` (the GI2-1 pin), expressed by `gi2-dequant-reference.py` semantics. A3 extends to the union set: deterministic in-repo block fixtures + goldens committed as `fixtures/gguf/gguf-dequant-goldens.json` (schema `gguf-dequant-goldens-v2`), and real-file slice goldens derived at the unit boundary from the local Qwen3.6 artifact and recorded in the exempla receipt.
- **Slice selection (named at the unit boundary from the live manifest)**: the two BF16 tensors (both — they are the only BF16 rows in the artifact), one Q4_K weight slice, one Q5_K slice, one Q6_K slice, one Q8_0 slice, one F32 slice, and one rank-3 expert tensor slice (a bounded per-expert window).
- **Local corpus**: the real artifacts under `/Users/ianzepp/ai/models/` (the four mandatory files + the two additional `qwen35moe` rows) are operator evidence, never committed and never redistributed; Gradus never receives their paths — the exempla's app-owned adapter resolves them (the `gguf-inspect` pattern). The two Qwen2.5 dense rows' exact type distributions are **not in shared evidence**; the unit derives them from the live manifest at its boundary and records them in the coverage record. If a derived layout lies outside the admitted set {F32, BF16, Q5_0, Q8_0, Q4_K, Q5_K, Q6_K}, the unit records a unit-scope gap with the exact tensor and routes a correction — it never guesses or widens the set silently.

## Closeout Commands And Expected Observed Result

From the Hand packet (substitute the lane worktree paths):

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

- **est_work_tokens**: 18k–28k. **est_basis**: pilot (extrapolated — gradus Fab codec + tensor-view surface + goldens + package-MIR receipt; no close ledger class; the two new codecs carry the bulk).
- **tool_latency**: medium — `check-source`/`check-compile` (narrow) plus one `faber run --target fmir` exempla execution and the oracle-derivation step; no cargo, no device runs.

## Stop Conditions / Escalation

- If GGUF-A1c has not landed at the dispatch boundary, the Hand records the recheck and stops (never proceeds on the assumed post-A1c authority — "summaries are claims").
- If a mandatory-artifact layout outside the admitted set appears in the live distributions, the unit records the exact tensor and routes a correction (campaign stop condition) — no silent widening of the codec set.
- A golden mismatch on any slice is a divergence receipt naming the first divergent block element, never a tolerance-widened pass (truth over safety; bit-exact f32 contract).
- A window/materialization bound that would need to exceed `MAXIMUM_SLICEM_ELEMENTA` or `CORPUS_LIMES` for the forward graph is recorded with its consuming successor (GGUF-A4/M-rungs) and escalated — the bounded-window design is the contract, not a negotiable ceiling.

## Open Items For Mind (none blocks this lowering)

1. **GGUF-A1c (LIB-01) landing** — the dispatch gate for this unit; recheck at the A1c closeout.
2. **Qwen2.5 dense-row type distributions** — derived at the unit boundary (evidence gap recorded; low risk given the admitted union set).
3. **Exact public spellings** (`TensorPayload`/`VisumTensoris`/`vincula`/`materializa_slicem`/`limes_payloadis`) — frozen by this lowering per the codebase Latin convention; any amendment routes through the delivery-amendment path (A1a precedent).

---

*Planning artifact only. No product code was written by this lowering. LIB-03/GGUF-A3 is lowered as three serial slices (C1 codec extension → C2 payload/view/materializer → C3 exempla receipt + docs + closeout); dispatch is gated on LIB-01 (GGUF-A1c). The unit preserves every mandatory successor through CLOSE-01 and advances umbrella milestone Q1 without completing the campaign.*
