# Delivery Lowering — GGUF-A1c (LIB-01): Capsule/Caller Schema-2 Clean Break

**Planner**: planner-21. **Assignment**: fresh Qwen LIB-01 lowering (task
6e17ec90 / handle `f4d3bce3`), derived independently from the Qwen3.6 campaign,
the PML5-GGUF delivery authority, and the live product repos — no reuse of
planner-1..19 worktrees, commits, or cancelled transcripts.
**Campaign**: [`radix/docs/factory/gpu-production-readiness/CAMPAIGN.md`](../../../../radix/docs/factory/gpu-production-readiness/CAMPAIGN.md)
(Radix worktree `b6d6e17c8ad7`).
**Delivery authority**: [`pml5-general-gguf-delivery.md`](pml5-general-gguf-delivery.md)
(Gradus worktree `bc500993c97b`), §GGUF-A1c.
**Repo baselines**: Radix `b6d6e17c8ad7`; Gradus `bc500993c97b`; Hosts
`57d659d60430`; public Faber `1fb6cc97e66d`. All verified against the
planner-21 worktree heads.

## 1. Goal-check verdict (compact)

- **Goal path**: `radix/docs/factory/gpu-production-readiness/CAMPAIGN.md`,
  mandatory work row `LIB-01` (owner Gradus, depends on A1b).
- **Evaluator mode**: goal-check against the delivery authority (GGUF-A1c
  section) and the live gradus worktree.
- **Intended consumer**: delivery.
- **Verdict**: **READY**.
- **Reasoning**: the delivery authority freezes A1c's contract (replace the
  byte-owning/path-carrying/one-global-quantization capsule with schema-2
  identity/manifest values; reject schema 1 at the new boundary; migrate all
  constructor callers in one unit; no forwarding shim; no dual GGUF authority)
  with a named done-when. The schema-2 values (`gradus:model/artifact`,
  `gradus:model/gguf_manifest`) already exist and are pathless; the two
  schema-1 constructor callers (`src/model/gguf.fab`,
  `src/model/safetensors.fab`) and the three probas are present and locatable.
  No architecture gap blocks the unit. The only design fork — how the
  Safetensors row is represented inside the schema-2 capsule — is named with a
  default in §5 and flagged to Mind in §13.
- **Key points**: schema-1 live callers are exactly `gguf.fab`
  (`capsula.construct` at src/model/gguf.fab:773) and `safetensors.fab`
  (`capsula.construct` at src/model/safetensors.fab:1056);
  `tests/admission_conformance.fab` composes both. No non-gradus repo imports
  `gradus:model/capsule`, `gradus:model/gguf`, or `gradus:model/safetensors`
  (checked `norma`, `faber`, `radix`, `examples`); the migration is contained
  in gradus. The schema-2 `gguf_manifest` module already covers rank 3, unknown
  layouts, alignment, and the 753-tensor ceiling, so the capsule can consume
  it without extension.
- **Blocking gaps**: none.
- **Recommended next step**: deliver GGUF-A1c as the single unit A1C-01 below.

## 2. Interpreted unit / problem

LIB-01 = GGUF-A1c, "capsule/caller clean break". Today `gradus:model/capsule`
is `capsule-schema-1.0.0`: it owns the admitted byte payload (`corpus`), a
provenance path (`semita`), one global quantization row (`quantizatio`), and
the pinned-row architecture/tokenizer/bounds facts. `gradus:model/gguf` and
`gradus:model/safetensors` are the only two constructors of that capsule, each
embedding its own wire parser (a second GGUF authority alongside
`gradus:model/gguf_manifest`). That shape does not fit real GGUF files or the
35 GB target: byte ownership, path carrying, and a single global quantization
row contradict the per-tensor, pathless `ParsedArtifact` boundary that the
delivery authority fixes.

The unit must:

1. Replace the schema-1 capsule with a schema-2 capsule that carries
   **identity/manifest values only** — pathless content identity
   (`artifact.ContentIdentity`) plus a per-format manifest with per-tensor
   storage descriptors (mixed F32/quantized, rank-3 capable) — and that
   **rejects schema 1 at the new boundary**.
2. Migrate every constructor caller (`gguf.fab`, `safetensors.fab`) to the
   schema-2 values so **schema 1 has no live constructor or parser caller**.
3. Delete the dual GGUF wire parser so **one GGUF authority remains**
   (`gradus:model/gguf_manifest`); add **no forwarding shim** and **no
   compatibility façade**.
4. Migrate the three probas and `tests/admission_conformance.fab`, update the
   fixture contracts and API/support documentation, and pass
   source/compile/migrated-proba checks.

## 3. Normalized spec

One coherent delivery-sized outcome:

> After this unit, `gradus:model/capsule` is `capsule-schema-2.0.0` and holds
> exactly `ContentIdentity` + a per-format manifest (GGUF:
> `GgufManifest`; Safetensors: see §5 default). It owns no bytes, no path,
> no reader, no device handle, and no single global quantization row. The
> schema-1 wire form (`capsule-schema-1.0.0`) is rejected with a typed error
> at the new boundary. `gguf.fab` and `safetensors.fab` admit through the
> schema-2 capsule only; every GGUF parse delegates to
> `gradus:model/gguf_manifest`. `gradus:model/gguf` no longer contains a wire
> parser. The public import names stay: `gradus:model/capsule`,
> `gradus:model/gguf`, `gradus:model/safetensors` (schema-2 surfaces; no
> aliases, no shims, no deleted-entry forwarding).

Non-goals (this unit): tokenizer runtime (GGUF-A2/LIB-02), packed storage and
materialization (GGUF-A3/LIB-03), architecture admission (GGUF-M1/MODEL-01),
real-file payload reads, native execution, and any Metal/CUDA work.

## 4. Repo-aware baseline (live evidence)

Verified in `/Users/ianzepp/work/faberlang/worktrees/planner-21/gradus`
(branch `factory/planner-21`, HEAD `bc50099`):

| Surface | Current state | Role in A1c |
| --- | --- | --- |
| `src/model/capsule.fab` | `capsule-schema-1.0.0`; `genus Capsule` with `BytesValida bytes` + `semita` path + one `Quantizatio` row; constructor `construct(26 params) → Capsule ⇥ AdmissionError`; 9 `AdmissionError` variants incl. `BytesMala` | Rewrite to schema 2 (identity/manifest values) |
| `src/model/capsule.proba` | 41 compile-level cases against schema-1 `construct` | Migrate to schema-2 proba |
| `src/model/gguf.fab` | One-row (SmolLM2-360M scaled) GGUF wire parser; `admit(...) → capsula.Capsule ⇥ GgufError`; calls `capsula.construct` (line 773) | Delete dual wire parser; admit via `manifestum.parse`/`inspect` → schema-2 capsule |
| `src/model/gguf.proba` | Builds the scaled row byte sequence in code; asserts schema-1 capsule | Migrate to schema-2 |
| `src/model/safetensors.fab` | Safetensors header/JSON parser; `admittas(...) → capsula.Capsule ⇥ SafetensorError`; calls `capsula.construct` (line 1056) | Migrate to schema-2 capsule (per §5 default) |
| `src/model/safetensors.proba` | Schema-1 capsule assertions | Migrate to schema-2 |
| `tests/admission_conformance.fab` | Composes `safetensors.admittas` + `gguf.admit` into `capsula.Capsule` | Migrate caller (part of "all constructor callers") |
| `src/model/artifact.fab` | `ContentIdentity` + `identitas(algorithmus, digestio, longitudo) ⇥ ArtifactError` — pathless | Schema-2 identity source (read-only) |
| `src/model/gguf_manifest.fab` | `GgufManifest`, `parse`, `inspect`, `read_fragmentum`, `metadata`, `textum`, `numerum`, `inveni_tensorem`, `layout` (A1b) | Schema-2 GGUF manifest (read-only for this unit) |
| `exempla/gguf-manifest`, `exempla/gguf-inspect` | Consume `artifact` + `gguf_manifest` only; 40 PASS / 0 FAIL synthetic proof and six-file inspection receipt | Unaffected (verify they still compile) |
| Fixture contracts | `fixtures/gguf/gguf-row-oracle.md`, `fixtures/safetensors/safetensors-row-oracle.md` cite `capsule-schema-1.0.0` and `capsula.verify_against` | Update to schema-2 facts |
| Docs | `docs/api-reference.md` (§capsule/gguf/safetensors), `docs/module-map.md`, `docs/diagnostics.md` (`AdmissionError` table), `docs/regression-corpus.md` (v1.2.0), `README.md`, `docs/factory/production-ml-library/pml0-symbol-inventory.md`, `pml0-support-matrix.md` (Rows 1–2 + A1b note) | Update (API/support docs scope) |
| Historical docs | `pml0-model-capsule-contract.md`, `pml0-module-dag.md`, `pml0-claim-register.md` cite schema 1 | Leave as historical; supersession note goes in support-matrix/api-reference (see §13 Q3) |

External consumers: none — `norma`, `faber`, `radix`, `examples` do not import
`gradus:model/capsule`, `gradus:model/gguf`, or `gradus:model/safetensors`.
The exempla `gguf-manifest`/`gguf-inspect` do not reference the capsule.

## 5. Design decisions (defaults for the implementing Hand)

**D1 — schema-2 capsule shape (default, matches the authority's
`ParsedArtifact` boundary).** `capsula.Capsule` becomes
`capsule-schema-2.0.0` and carries exactly:

- `artifact.ContentIdentity` identity (algorithm, digest, byte_length),
  pathless;
- one per-format manifest genus: `manifestum.GgufManifest` for GGUF, and —
  for Safetensors — a new `SafetensorsManifest` genus defined **inside
  `capsule.fab`** (format/version + header metadata + per-tensor descriptors:
  name, dtype, shape, data_offsets), mirroring `GgufManifest`'s
  descriptor style.

The schema-1 field groups that die: `BytesValida` (byte ownership),
`semita` (path), the single `Quantizatio` row, and the schema-1 hard-coded
architecture/tokenizer pins. Per-tensor storage lives in the manifest
descriptors (`GgmlLayout` / dtype+offsets), so mixed storage is representable.
`AdmissionError` drops `BytesMala` and gains a schema-1 rejection variant
(see D2); the remaining variants stay where they still apply.

**D2 — schema 1 rejection at the new boundary.** `schema_versio` becomes
`"2.0.0"`. The schema-2 constructor, `verify`, and
`deserialize_identity` return a **typed error that explicitly names schema 1**
(e.g. `AdmissionError.VersioIgnota` with message `schema 1 is retired — capsule
schema is 2.0.0`, or a dedicated `SchemaVetus` variant; the Hand freezes one
variant and its docs row). Because the schema-2 constructor has a different
signature (no bytes, no path, no single-quantization row), a schema-1 call
site also fails to compile — the dual guarantee: compile-time (no such
constructor) and runtime (wire/`verify` rejection).

**D3 — single GGUF authority, no façade.** The byte-level GGUF wire parser
inside `src/model/gguf.fab` (`_legere_u32` … `_legere_bool`,
`_clavis_admissa`, `_typo_admissus`, …) is **deleted**. `gguf.fab` keeps its
public admission entry `admit` as a thin wrapper that (a) calls
`manifestum.parse`/`inspect` to obtain the `GgufManifest`, (b) validates the
pinned one-row contract **through manifest accessors** (`metadata`, `textum`,
`numerum`, `inveni_tensorem`), and (c) builds the schema-2 capsule. No alias,
no forwarding, no compatibility import. `gradus:model/gguf_manifest` is the
only GGUF parse path; the A1a "frozen public surface" of `gguf_manifest` is
not modified by this unit.

**D4 — Safetensors row.** `safetensors.admittas` keeps its entry and returns
the schema-2 capsule holding `ContentIdentity` + `SafetensorsManifest`
(D1). The Safetensors row remains an F32 structural fixture; no real-file
claim is added.

## 6. Ordered unit graph

The delivery authority freezes A1c as **one unit** ("Migrate all constructor
callers in one unit") and the campaign's LIB-01 done oracle is a single line
("One GGUF authority remains; all callers and probas use it"). Splitting the
migration across dispatched units would risk intermediate dual-authority
states the clean break forbids. This lowering therefore emits **one
implementable unit**, with named intra-unit phases (sequencing for the Hand,
not separate tasks) and a named split boundary.

### A1C-01 — GGUF-A1c capsule/caller schema-2 clean break

| Field | Value |
| --- | --- |
| `id` | `A1C-01` |
| `outcome` | `gradus:model/capsule` is schema-2 (`capsule-schema-2.0.0`): pathless `ContentIdentity` + per-format manifest only, no bytes/path/one-global-quantization; schema 1 rejected at the boundary; `gguf.fab` and `safetensors.fab` are the only admission entries and both produce the schema-2 capsule; the dual GGUF wire parser in `gguf.fab` is deleted; `gradus:model/gguf_manifest` is the one GGUF authority; all probas, the conformance test, fixture contracts, and API/support docs are migrated; no forwarding shim exists |
| `write_scope` | Gradus worktree (this lowering's lane or the Mind-assigned Hand lane), all on `factory/planner-21`: `src/model/capsule.fab`, `src/model/capsule.proba`, `src/model/gguf.fab`, `src/model/gguf.proba`, `src/model/safetensors.fab`, `src/model/safetensors.proba`, `tests/admission_conformance.fab`, `fixtures/gguf/gguf-row-oracle.md`, `fixtures/safetensors/safetensors-row-oracle.md`, `docs/api-reference.md`, `docs/module-map.md`, `docs/diagnostics.md`, `docs/regression-corpus.md`, `docs/factory/production-ml-library/pml0-symbol-inventory.md`, `docs/factory/production-ml-library/pml0-support-matrix.md`, `docs/factory/production-ml-library/CAMPAIGN.md` (status line only), `docs/factory/production-ml-library/pml5-general-gguf-delivery.md` (status line + A1c "implemented evidence" note) |
| `read_scope` | `src/model/artifact.fab`, `src/model/gguf_manifest.fab` + `.proba`, `exempla/gguf-manifest/`, `exempla/gguf-inspect/`, `docs/factory/production-ml-library/pml0-model-capsule-contract.md` (historical), `docs/factory/production-ml-library/pml0-support-matrix-schema.md`, `docs/factory/production-ml-library/pml5-general-gguf-delivery.md`, `docs/compatibility-policy.md` |
| `forbidden_scope` | `src/model/artifact.fab` and `src/model/gguf_manifest.fab` (schema-2 authorities — read-only for this unit); `src/model/dequant.fab`; `src/tokenizer.fab` (GGUF-A2 owns it); `src/cache.fab`, `src/generation.fab`, `src/decode.fab`; any radix/hosts/faber/norma checkout or main-branch edit; any new public module outside the listed files; any forwarding shim, compatibility alias, or dual parser; no commit that leaves both a schema-1 constructor caller and schema-2 authority live |
| `done_when` | (a) schema 1 has no live constructor or parser caller: `capsula.construct(` absent from `src` and `tests`; `capsule-schema-1.0.0` absent from `src`, `fixtures`, `tests`; (b) schema-2 identity/manifest values are the only authority: `gguf.fab` delegates all wire parsing to `manifestum` and its old wire helpers are gone; (c) `schema_versio` in `capsule.fab` is `"2.0.0"`; a schema-1 stamp is rejected by a typed error case in `capsule.proba`; (d) `./scripta/check-source` and `./scripta/check-compile` exit 0; `faber check` on the gradus package ends `ok: .`; (e) migrated `capsule.proba`, `gguf.proba`, `safetensors.proba` and `tests/admission_conformance.fab` type-check; (f) `git diff --check` silent; (g) the docs inventory is migrated (support-matrix Rows 1–2 cite `capsule-schema-2.0.0`, diagnostics `AdmissionError` table matches the new surface, regression-corpus version bumped, symbol inventory counts refreshed) |
| `validation` | See §10 closeout commands |
| `depends_on` | GGUF-A1b receipt (`exempla/gguf-inspect/README.md`; the 40-case synthetic proof + six-file real inspection). A1b evidence must be re-verified to still hold after the caller migration (the exempla do not import the capsule, so they must be unaffected — a compile check confirms) |
| `non_goals` | Tokenizer runtime (GGUF-A2), packed storage/materialization (GGUF-A3), `qwen35moe` admission (GGUF-M1), real-file tensor-payload reads, native kernels, Metal/CUDA, HTTP/serving, any other model architecture, main-branch integration |
| `risk` | **medium** — the capsule is a public module with a frozen documented surface; the schema-2 signature change and the deleted GGUF parser must land atomically to avoid dual-authority states; proba migrations must keep their oracle pins (row facts are read-only citations, not re-derived). Feeds the A1c delivery audit. |
| `test_owner` | A1C-01 implementing Hand; `check-source`/`check-compile`/`faber check` + the schema-1-caller greps are the oracle |

### Intra-unit phases (Hand sequencing within A1C-01)

1. **Red**: add the schema-2 proba cases first — schema-1 stamp rejected,
   schema-2 identity/manifest admitted, no path/bytes fields, per-tensor
   layout visibility — and the no-schema-1-caller grep. Record the first
   failure (§8).
2. **Capsule rewrite**: `capsule.fab` → schema-2 (D1/D2) + migrate
   `capsule.proba`.
3. **GGUF caller**: delete the dual parser in `gguf.fab`, admit via
   `manifestum`, migrate `gguf.proba`.
4. **Safetensors caller**: migrate `safetensors.fab` + `safetensors.proba`
   (D4), and `tests/admission_conformance.fab`.
5. **Fixture contracts + docs**: oracle docs, api-reference, module-map,
   diagnostics, regression-corpus, symbol-inventory, support-matrix, README,
   campaign/delivery status lines.
6. **Green**: run §10 closeout commands; record observed results.

**Named split boundary**: (intra-unit) the schema-2 capsule module is the
seam — phases 3/4 are unsafe to ship without phase 2, and the whole unit must
land without an intermediate commit in which a schema-1 caller and the
schema-2 authority coexist; (downstream) A1C-01 completes the last
"clean-break plumbing" rung of milestone Q1, and its completion **splits**
into two independent successors: GGUF-A2 (LIB-02 tokenizer) and GGUF-A3
(LIB-03 packed storage), both of which consume the schema-2 capsule. Neither
successor starts inside A1C-01.

## 7. Mandatory successors preserved through CLOSE-01

Nothing below is narrowed, deferred, made optional, or moved outside the
campaign by this lowering:

```
LIB-01 (this unit) → LIB-02 (GGUF-A2) + LIB-03 (GGUF-A3)
  → REF-01 (dense reference rungs)
  → MODEL-01 (qwen35moe admission) → MODEL-02 (MoE) + MODEL-03 (SSM/attention)
  → MODEL-04 (full-model reference inference)
  → EXEC-01 (Faber package plan) + EXEC-02 (packed native kernels)
  → EXEC-03 (persistent resident sessions)
  → CAP-01 (Metal) + CAP-02 (CUDA)
  → CLOSE-01 (reconcile + independent audit)
```

Cross-repo joins (Faber/Radix/Hosts) and the exact-artifact completion
contract (`Qwen3.6-35B-A3B-UD-Q4_K_M.gguf`, 22,663,387,424 bytes, SHA-256
`0b21525e972670ed59e1812e170b27c26355381f0656ecc4e25617ece7dac58b`,
complete `qwen35moe` graph, 256+ tokens × 2 prompts in one resident session,
Metal and CUDA, every receipt clause) are unchanged. The Gradus GGUF stage
graph (GGUF-A1..A7, GGUF-M1..M6) is unchanged beyond A1c's own section.

## 8. First failing oracle (red proof)

Before the migration lands:

- Add the schema-2 proba cases (schema-1 stamp → typed rejection; schema-2
  identity/manifest admitted; no path/bytes surface; per-tensor descriptors
  visible) and the caller greps.
- Run `faber check` on the package and the schema-1-caller greps.

**Expected first failure**: the schema-1 surface fails the new cases — e.g.
`capsula.deserialize_identity` accepts a `1.0.0`-stamped wire (schema-2 must
reject it), `capsula.Capsule` exposes `corpus`/`semita` (schema-2 forbids
them), and `gguf.fab` still references the to-be-removed schema-1 constructor.
Record the failing command and the first divergence (variant/method/line)
before proceeding; the proba/grep pair is the divergence recorder.

## 9. Checkpoints and gates

| Checkpoint | Gate |
| --- | --- |
| Red proof recorded | First failing command + divergence named; proba cases in place |
| Capsule schema-2 compiles | `faber check` passes after phase 2 with callers still on schema 1? — **not allowed**: no dual state. Phases 2+3 must land together in the working tree before a green is claimed |
| No live schema-1 caller | greps in §10 return empty over `src` + `tests` |
| Migrated probas + conformance type-check | `faber check` ends `ok: .` |
| Docs migrated | support-matrix Rows 1–2 + A1b note, diagnostics table, symbol inventory, regression corpus all cite schema-2 |
| Delivery audit | Mind routes the A1c task body for audit before dispatch (campaign Execution Rule 3) |
| Milestone | LIB-01 **advances milestone Q1** (executable library inputs); Q1 completes only when A1c **and** A2 **and** A3 receipts are accepted |

## 10. Validation summary (closeout commands + expected observed result)

Commands (lane-relative; `FABER_BIN` points at a lane-local faber binary, per
the A1a Hand-packet precedent):

```bash
cd /Users/ianzepp/work/faberlang/worktrees/<lane>/gradus
./scripta/check-source
env FABER_LIBRARY_HOME=/Users/ianzepp/work/faberlang/worktrees/<lane> \
  FABER_BIN=/Users/ianzepp/work/faberlang/worktrees/<lane>/radix/target/debug/faber \
  ./scripta/check-compile
env FABER_LIBRARY_HOME=/Users/ianzepp/work/faberlang/worktrees/<lane> \
  /Users/ianzepp/work/faberlang/worktrees/<lane>/radix/target/debug/faber \
  check --diagnostics .
# schema-1 rejection + single-authority greps
grep -rn "capsula\.construct(" src tests        # must print nothing
grep -rn "capsule-schema-1.0.0" src fixtures tests   # must print nothing
grep -n "schema_versio" src/model/capsule.fab # must show 2.0.0
grep -rln "importa ex \"gradus:model/gguf_manifest\"" src tests   # every GGUF parse caller
git diff --check -- src/model/capsule.fab src/model/capsule.proba \
  src/model/gguf.fab src/model/gguf.proba src/model/safetensors.fab \
  src/model/safetensors.proba tests/admission_conformance.fab \
  fixtures/gguf fixtures/safetensors docs README.md
```

**Expected observed result**: `check-source` and `check-compile` exit 0;
`faber check` ends `ok: .`; the schema-1 greps are empty; `schema_versio` is
`"2.0.0"`; migrated probas and the conformance test type-check;
`git diff --check` is silent; the exempla `gguf-manifest`/`gguf-inspect`
still compile unchanged (proving the A1b receipt is unaffected). This is the
executed A1c clean-break proof at the **source/compile boundary** — it does
not read real tensor payloads and does not claim inference.

## 11. Local corpus boundary and hardware/backend authority

- **Local corpus boundary**: the A1c proof does **not** read the
  operator-local six-file corpus (SmolLM2-360M, Qwen2.5-0.5B/1.5B,
  Qwen3.6-35B). A1c is bounded to the committed synthetic fixtures
  (`fixtures/gguf/smollm2-360m-scaled-row.gguf`, the three A1a manifest
  fixtures, `fixtures/safetensors/smollm2-360m-scaled-row.safetensors`) and
  the compile-level probas. Real-file inspection is A1b's already-accepted
  receipt; real tokenizer/materialization reads belong to A2/A3+.
- **Hardware/backend authority**: none. A1c is device-neutral and
  compile/CPU-only; no Metal or CUDA authority, no host/device objects. Backend
  authority belongs to GGUF-A7/GGUF-M5 (Radix + Hosts) and the capstone
  (CAP-01/CAP-02). This matches the campaign's clean-boundary table.

## 12. Work-token estimate

- **est_work_tokens**: 20k–32k.
- **est_basis**: pilot (extrapolated — source+proba+docs migration unit at
  A1a's module scale; no close-ledger class exists for a migration unit; the
  A1a package-MIR proof and A1b real-file inspection are the nearest executed
  peers and both shipped without device runs).
- **tool_latency**: medium — `check-source` + `faber check` runs per phase
  (compile-only, no cargo build inside the unit; the faber binary is
  lane-provided), plus the schema-1-caller greps. No device runs.

## 13. Open questions for Mind

1. **Safetensors manifest representation (default chosen: new
   `SafetensorsManifest` genus inside `capsule.fab`).** The delivery
   authority's `ParsedArtifact` boundary names `GgufManifest` only; Safetensors
   has no manifest module. The default mirrors `GgufManifest`'s descriptor
   style inside the capsule module so the migration stays in the stated write
   scope. **Options**: (a) default; (b) format-agnostic generic manifest genus
   shared by both formats (more abstraction, no existing precedent); (c)
   defer Safetensors migration to a later unit (rejected — it would leave a
   schema-1 constructor caller live, contradicting "migrate all constructor
   callers in one unit"). Confirm (a) or route to head-cto for the capsule
   surface shape.
2. **Schema-1 rejection variant naming.** Whether the typed rejection is
   `AdmissionError.VersioIgnota` with a schema-1-specific message or a new
   `SchemaVetus` variant. The Hand freezes one and documents it; Mind should
   confirm no external consumer depends on the schema-1 `AdmissionError`
   surface (none found in `norma`/`faber`/`radix`/`examples`).
3. **Historical PML0 docs** (`pml0-model-capsule-contract.md`,
   `pml0-module-dag.md`, `pml0-claim-register.md`) still describe
   `capsule-schema-1.0.0`. **Default**: leave them as dated historical records
   and carry the supersession in `pml0-support-matrix.md` +
   `docs/api-reference.md` (live authority). If Mind wants the historical docs
   annotated, that is an additional docs write to scope.

## 14. Honesty gate

GGUF-A1c is one unit and this lowering does not pretend it is more. It does
not compile A2/A3/M-units, does not lower `qwen35moe`, and does not claim the
campaign invariant. Unit completion is **not** campaign completion: LIB-01
completion yields one clean schema-2 admission authority and advances
milestone Q1 by one of three receipts; the Qwen3.6 invariant requires the
full LIB/REF/MODEL/EXEC/CAP chain through CLOSE-01, which this lowering
preserves verbatim.
