# Delivery: PML2 — Model, format, tokenizer, and checkpoint admission

**Goal**: `docs/factory/production-ml-library/CAMPAIGN.md` (PML2 gate)
**Status**: scoped 2026-08-08 — entry-gated; full P3 confirmation at gate by planner; Mind owns admission
**Repo**: gradus (`src/model.fab`, `src/tokenizer.fab`, capsule types); controlled `norma` migration (C3); NO faber/radix/hosts product code
**Predecessors**: PML1 (tensor/dtype/shape/parameter), PML0 (U7 admission-migration decision, U14 capsule contract), GI0–GI2 pinned model/oracle contracts (read-only)

## Phase Intent

Gradus owns model bytes and semantic admission: one Safetensors row and one selected GGUF row fail closed on format, version, architecture, dtype/quantization, offsets, shapes, tokenizer identity, and bounds; accepted `norma:model` and GI1 admission behavior migrates in with **no dual authority** (C3 — enforced by code location). This is the security-critical admission boundary for the future server (C8).

**Entry gate**: PML1 accepted; PML0-U7/U14 dispositions recorded; the first GGUF architecture/quantization row selected (operator decision from PML0 open question — defaults proceed until overridden).

**Non-goals**: forward architectures (PML3); physical upload/device residency (hosts); paths/config ownership (applications); general GGUF support beyond the admitted row.

## Unit Graph

### PML2-U1 — Admitted-model capsule implementation (C8)
- **done_when**: the typed admitted-model capsule from PML0-U14 exists as a gradus type (validated bytes + cryptographic identity + tokenizer identity + quantization + bounds + architecture facts); raw GGUF/Safetensors bytes and paths are never trust anchors — only the capsule carries identity across Gradus ↔ faber-runtime/hosts; schema version-stamped.
- **write_scope**: `gradus/src/model/capsule.fab`, tests. **est_work_tokens**: 12k–24k. **tool_latency**: low.
- **dependencies**: none — leaf by design (capsule imports nothing; ceilings mirrored as constants; PML0-U14 contract only).
- **parallel_children_considered**: none — capsule is the admission root.

### PML2-U2 — Safetensors row
- **done_when**: one Safetensors row parses → capsule with fail-closed rejection on format/version/architecture/dtype/offsets/shapes/tokenizer mismatch; legal fixture + oracle pinned (hash); negative matrix (truncated, duplicate, overlapping, misaligned, unsupported, arch-mismatch) fails closed with typed errors; allocation ceilings enforced before counts drive allocation (GI1 precedent).
- **write_scope**: `gradus/src/model/safetensors.fab`, fixtures, tests. **est_work_tokens**: 12k–24k. **tool_latency**: low.
- **dependencies**: U1, GI0–GI1 facts (read-only).
- **parallel_children_considered**: parallel with U3 (disjoint format files) after U1; negative cases batch after the happy row.

### PML2-U3 — GGUF row (selected architecture/quantization)
- **done_when**: the selected GGUF row parses → capsule with fail-closed rejection on the full dimension set (format, version, architecture, dtype/quantization, offsets, shapes, tokenizer); pinned legal fixture + oracle from GI0–GI2; negative matrix per U2 standard; exact GGML quantization block layouts admitted (no toy packed-u4 as GGUF quant).
- **write_scope**: `gradus/src/model/gguf.fab`, fixtures, tests. **est_work_tokens**: 15k–30k. **tool_latency**: low–medium.
- **dependencies**: U1, GI0–GI2 pinned model facts (read-only), PML1-U2.
- **parallel_children_considered**: none (one row, one admission contract); U2 runs beside it.

### PML2-U4 — Tokenizer identity
- **done_when**: tokenizer identity for the admitted row(s) is a versioned contract (byte-level/BBPE per row; BOS/EOS/special-token behavior); token ids match the pinned `llama.cpp` fixture exactly; tokenizer identity is part of the capsule and KV identity key (MD-A9 precedent).
- **write_scope**: `gradus/src/tokenizer.fab`, fixtures, tests. **est_work_tokens**: 10k–20k. **tool_latency**: low.
- **dependencies**: U1; GI1 tokenizer facts.
- **parallel_children_considered**: none (identity is indivisible per campaign rule); parallel with U2/U3 after U1.

### PML2-U5 — `norma:model` + GI1 admission migration (C3)
- **done_when**: per PML0-U7 decision — either the accepted admission code from `norma/src/model.fab` (+ GI1's `faber-runtime` admission rows) is **moved** into gradus and the old location no longer hosts admission logic, or formally retired; grep proves the old owning module path hosts no admission entry points; no stranded callers (documented + tested); no dual authority.
- **write_scope**: `gradus/src/model/`, `../norma/src/model.fab` (controlled migration), tests; `faber-runtime` only if the PML0-U7 decision says migrate-from there.
- **est_work_tokens**: 12k–24k. **tool_latency**: medium (norma/faber-runtime build check, no cargo in dev loop).
- **dependencies**: U1–U4 (destination API exists), PML0-U7 decision record.
- **parallel_children_considered**: none — the migration is the C3 enforcement point; serializes with any in-flight norma/faber-runtime edits (check dirty state first).

### PML2-U6 — Negative matrix + admission conformance
- **done_when**: the full fail-closed negative matrix across U2/U3/U4 (format/version/arch/dtype/quant/offset/shape/tokenizer/bounds/counts) is a committed conformance suite with typed-error assertions; every negative case fails closed before allocation or launch; conformance gate green once.
- **write_scope**: `gradus/tests/admission_conformance.fab`, fixtures. **est_work_tokens**: 10k–20k. **tool_latency**: low.
- **dependencies**: U2, U3, U4.
- **parallel_children_considered**: none (conformance is the aggregate admission proof).

## Parallelism

- Lane 1: U1 → U2 + U4 (parallel) → U5.
- Lane 2: U1 → U3 → U6 (U6 aggregates U2/U3/U4).
- U5 serializes with in-flight norma/faber-runtime edits (check dirty state; additive only).
- Cross-campaign: runs beside NGAB1–NGAB4 (disjoint repos; NGAB2 consumes the capsule contract, not code), GI3-8 (read-only GI facts consumed), training capstone. The capsule contract is the shared handoff — coordinate with NGAB0-U4 (manifest identity) at the packet level.
- **Phase gate**: U1–U6 done; one admitted Safetensors row + one admitted GGUF row fail closed; negative matrix green; no dual authority (grep proof); README regen + audit 0 findings.

## Validation

```bash
cd gradus && ./scripta/check-source && ./scripta/check-compile
cd gradus && python3 ../radix/scripta/generate-factory-readme.py --factory-root docs/factory --check
cd gradus && ./scripta/check-factory-goal-status --fail-on error
```
Admission conformance suite once at closeout (targeted, not full ladder).

## Council Dispositions (applicable)

| Item | Mandate | Where |
| --- | --- | --- |
| C3 | No dual authority — code location, not prose | U5 (the enforcement unit) |
| C8 | Admitted-model capsule; raw bytes/paths not trust anchors | U1, U6 |
| C1/C2 | GI4+ amendment + MD3I gate (from PML0-U11) | PML2 consumes the amended contracts; no stale ownership |
| R6 | Pending GI units vs shared surfaces | U5's dirty-state check before migrating norma/faber-runtime |
| R3 | One-row admission must stay extensible | U2/U3 keep admission + capability descriptors extensible |

## Open Questions

- First GGUF architecture/quantization row (operator; defaults proceed).
- Whether `faber-runtime` admission code migrates or retires (PML0-U7 decision outcome).
