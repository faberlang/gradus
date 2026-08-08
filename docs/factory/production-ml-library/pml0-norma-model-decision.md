# PML0-U8 Decision — `norma:model` migration (Safetensors/GGUF parsing)

**Unit**: PML0-U8 (`norma:model` migration decision)
**Decision date**: 2026-08-08
**Decision owner**: **operator** (binding decisions route through a Vivi need To
`reviewer`/`operator@`; the recorded defaults proceed until overridden — per
`pml0-delivery.md` §Decision owner)
**Dependencies**: PML0-U1 (source snapshot), read-only facts from
`../norma/src/model.fab`
**Feeds**: PML2-U5 (migration enforcement point, C3), PML0-U10 (contract
assembly), PML0-U11 (GI4+ migration map)
**Status**: recorded decision — defaults proceed until overridden

## Decision in one line

The Safetensors/GGUF parsing currently in `../norma/src/model.fab` **migrates
into Gradus at PML2 — not now** — under a **no-dual-authority** rule enforced
by **code location**, with a **no-stranded-callers** condition and a defined
fallback; operator owns the decision.

## Current state (verified 2026-08-08, read-only)

`../norma/src/model.fab` (1242 lines, SHA-1 pinned at norma HEAD
`84f27dacd6f9` per PML0-U1) is a **Stage-1 facade**: its own header comment
states "Stage 1 facade only. Binary safetensors/GGUF parsing belongs to small
parser". Facts:

- **Imports**: single `importa ex "norma:tensor" privata tensor` — the module
  is **self-contained**; it imports no Gradus surface.
- **Public surface** (13 `functio`): `formatum`, `diagnosticum`,
  `severitas_pro_status`, `inanis_diagnosticum`, `vacua_summarium`,
  `safetensors_header_textus`, `safetensors_summarium`,
  `tempta_safetensors_summarium`, `gguf_quantization_fragmentum`,
  `gguf_summarium`, `tempta_gguf_summarium`, `safetensors_tensor_f32`,
  `tempta_safetensors_tensor_f32`.
- **Safetensors**: header floor (first-8-Little-Endian length, printable
  ASCII, tensor-name JSON walk, `__metadata__` ignored, compact `dtype` /
  `shape` fields, fail-closed shape tokens) → `ModelSummary`.
- **GGUF**: scalar/array metadata walk, GGML/llama type-name mapping,
  quantization fragment, fail-closed parse → `ModelSummary`.
- **Types owned here**: `MetadataTensor`, `Diagnosticum`, `ModelSummary` —
  summary/diagnostic records.

Self-contained rule (grep proof, live):

```bash
grep -rn 'importa.*"norma:' gradus/src/        # → no output (gradus imports no norma)
grep -rn 'importa.*"gradus:' norma/src/        # → no output (norma imports no gradus)
```

Both directions are empty today: Gradus is self-contained and `norma:model` is
self-contained. The rule must stay intact through the migration.

## Decision — destination-API posture

1. **Migrate at PML2, not now.** The parsing is already on the Gradus campaign
   critical path and is a PML2 gate input ("Model formats … PML2 freeze
   ownership and migrate" in CAMPAIGN.md §Current State). PML0 does **not**
   move code (non-goal: no `src/**` edits, no `norma/src/**` edits).
2. **Destination API** (PML2 delivery): `gradus/src/model/` owns model bytes
   and semantic admission:
   - `gradus/src/model/capsule.fab` — typed admitted-model capsule (PML0-U14):
     validated bytes + cryptographic identity + tokenizer identity +
     quantization + bounds + architecture facts; raw bytes/paths are never
     trust anchors.
   - `gradus/src/model/safetensors.fab` — one fail-closed Safetensors row
     (PML2-U2) with allocation ceilings before counts drive allocation.
   - `gradus/src/model/gguf.fab` — one fail-closed GGUF row, selected
     architecture/quantization (PML2-U3); exact GGML quantization block
     layouts, no toy packed-u4 as GGUF quant.
   - `gradus/src/tokenizer.fab` — tokenizer identity as part of the capsule
     (PML2-U4).
   The `ModelSummary`/`Diagnosticum` record role (currently a reusable summary
   floor for application packages) is absorbed by the capsule and its
   diagnostic types; the `norma:model` copy is **replaced, not duplicated**.

## No-dual-authority rule (enforced by code location)

After the PML2 migration, **one owning module path** holds model-format
admission: `gradus/src/model/`. The old owning module path
`norma/src/model.fab` must host **no admission entry points** — the grep proof
at PML2-U5 asserts the old path hosts none of: `safetensors_*`,
`gguf_*`, `tempta_*`, `*_summarium`, `safetensors_tensor_f32`. "No dual
authority" is a **code-location fact**, not prose: two locations parsing
Safetensors/GGUF is a stop condition (CAMPAIGN.md §Stop Conditions), not a
coexistence strategy. No forwarding shim, no re-export, no
`norma:model` facade that still parses.

## No-stranded-callers condition (transfer condition)

The migration at PML2 proceeds **only when**:

1. **Destination API exists**: PML2-U1…U4 accepted (capsule, Safetensors row,
   GGUF row, tokenizer identity) — the destination is a real admitted API, not
   a stub.
2. **No caller is stranded**: every live importer of `norma:model` is migrated
   or retired **in the same coordinated change** (or a change gated on the
   same release), so no code keeps pointing at a facade that no longer parses.
3. **Norma cooperates**: `norma` working tree clean or dirt classified
   (A/B/C) before touching `norma/src/model.fab` — additive only; never
   destructive to foreign WIP (PML2-U5 dirty-state check).

**Verified live callers today** (grep, 2026-08-08):

| Caller | Uses | Notes |
| --- | --- | --- |
| `examples/ai-workbench/packages/faber-ai/src/commands/model.fab` | `model.formatum`, `model.diagnosticum`, `model.gguf_quantization_fragmentum`, `model.tempta_safetensors_summarium`, `model.tempta_gguf_summarium` | Only known importer of `norma:model`; must be migrated in the same change as PML2-U5 |

Any additional importer discovered at PML2 is added to this list in the same
grep sweep before migration proceeds.

## Fallback if a caller is found (or the chosen path is blocked)

If at PML2 the migration is blocked — a live caller that cannot move in-band,
a foreign dirty `norma` tree that resists classification, or the destination
API failing its gate — the fallback is:

1. **Do not partially migrate.** No dual authority is ever created as an
   intermediate state; `norma/src/model.fab` keeps its current facade
   **unchanged** until the block clears.
2. **Escalate immediately**: file a Vivi need To `operator@` naming the
   blocking caller/path, the default (migrate the caller in the same change),
   and the alternatives. The recorded default proceeds until overridden.
3. **Default for a stranded caller**: migrate the caller's calls to the
   Gradus capsule API in the same change as U5; if the caller's repo cannot
   land in-band, coordinate a paired release with the caller's owner rather
   than stranding it.
4. Only after the block resolves does U5 execute the move + grep proof +
   retirement of the old entry points.

## PML0 posture (this phase)

PML0 records this decision and takes **no code action**: no `gradus/src/**`
edits, no `norma/src/**` edits, no faber/radix/hosts/examples edits. The
decision feeds PML0-U10 (contract assembly), PML0-U11 (GI4+ migration map in
`radix/docs/factory/gpu-inference-gguf/`), and PML2-U5 (the C3 enforcement
point). Gradus stays self-contained: grep shows no `gradus→norma` imports.

## Validation

```bash
grep -rn 'importa.*"norma:' gradus/src/     # empty — self-contained rule intact
grep -rn 'importa.*"norma:model"' ../examples 2>/dev/null  # caller census for the transfer condition
git -C gradus diff --check
```

Outcome: doc names the target stage (**PML2**), the transfer condition
(destination API exists + no stranded callers + norma cooperates), the
fallback (no partial migration, escalate to operator@, migrate callers
in-band), and the decision owner (operator). Grep shows no `gradus→norma`
imports. `git diff --check` clean.
