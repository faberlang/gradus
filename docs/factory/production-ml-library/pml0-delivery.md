# Delivery: PML0 — Charter, API map, and measured baseline

**Goal**: `docs/factory/production-ml-library/CAMPAIGN.md` (PML0 gate)
**Status**: lowered 2026-08-08 — planned; Mind owns admission
**Repo**: gradus (`docs/factory/production-ml-library/`); radix factory docs
only for the GI4+ ownership amendment; **no product code anywhere**
**Sibling packet**: NGAB0 delivery (faber `native-gpu-application-bundle`),
GI0-GI3 facts (radix `gpu-inference-gguf`)

## Phase Intent

PML0 is **discovery-first**: freeze ownership, module graph, support matrix,
compatibility posture, and the measured baseline *before* broad implementation.
It produces the artifacts PML1-PML7 consume: the accepted module DAG and
shared/training/inference ownership table, the public symbol inventory, the
proof-shaped API ledger, the support-matrix schema, the numerical/claim-drift
baseline, the `norma:model` migration decision, and the exact cross-campaign
interface packet (paired with NGAB0, run in parallel). It also discharges seven
Council of Minds mandates (C1/C3/C4/C5/C7/C8 below; C2 folded into C1's
migration map in U11).

**Outcome**: an operator-accepted `pml0-gradus-contract.md` naming every future
Gradus ownership boundary, plus a committed GI4+ ownership amendment and
migration map in `radix/docs/factory/gpu-inference-gguf/`. PML0 **cannot close**
while GI4+ still assigns model runtime or serving to `faber-runtime` or any
other old owner.

**Non-goals** (per campaign): no GPU/device handles in the Gradus API; no
serving; no performance-before-correctness; no model-format code migration
(that is PML2); no compiler/package workarounds routed to the sibling campaign;
no `src/**` edits — PML0 only measures and freezes the current tree.

**Decision owner**: operator (binding decisions route through a Vivi need To
`reviewer`/`operator@`; the recorded defaults proceed until overridden).
Operator decisions: U7 admission-code migration mechanics, U8 `norma:model`
posture, U9 packet freeze vs reserved-seam split, U14 capsule trust anchor.

**Forbidden paths**: `faber/**`, `radix/**`, `hosts/**`, `examples/**` product
code; `gradus/src/**`; `gradus/corpus/**`; `norma/src/**`. Exceptions: U11
writes radix **factory docs** under `radix/docs/factory/gpu-inference-gguf/`;
U2/U13 add thin tool scripts under `gradus/scripta/`. Never hand-edit
`docs/factory/README.md` — regenerate it.

**Source snapshot**: refresh the campaign's six revisions (gradus
`29d26735d0d9`, norma `84f27dacd6f9`, faber `26b503a0e3bb`, radix
`a01543b06bfe`, hosts `e066ee0ae98a`, examples `aad199ecf07c`), record dirty
state per repo, and replace any drifted claim — that is U1.

## Interpreted Scope And Normalized Spec

The phase is done when every PML0 gate item has a committed, verifiable
artifact and the two required outputs exist. Nothing is implemented, built, or
measured beyond source-level facts.

Gate artifacts (campaign PML0): module DAG + ownership table (U4), public
symbol inventory (U2), proof-shaped API ledger (U3), support-matrix schema
(U5), numerical baseline (U6), `norma:model` migration decision (U8), exact
interface packet (U9). Required outputs: `pml0-gradus-contract.md` (U10) and
the committed GI4+ ownership amendment + migration map in radix
`gpu-inference-gguf/` (U11). Council mandates: C1→U11, C3→U7, C4→U9, C5→U12,
C7→U13, C8→U14. Snapshot refresh + dirty state → U1.

## Repo-Aware Baseline

Verified 2026-08-08 (grep/ls, not claims):

- `gradus/src/` = 11 `.fab` files, 723 lines; 21 `functio` declarations
  (attention 1, gradient 2, loss 3, nn 6, optimize 2, train 4, transformer 3;
  math/tensor/data have **0** — stubs; `gradus.fab` facade has 0).
- 17 fixed-shape functions (`*_2x2/_4x4/_2x8`), grep-verified: nn 6
  (`linear_2x2/_4x4/_2x8`, `gelu_4x4/_2x8`, `layernorm_2x8`), loss 3
  (`mse_2x2/_4x4/_2x8`), optimize 2 (`sgd_step_2x2/_4x4`), attention 1
  (`scaled_dot_product_2x8`), transformer 3 (`attention_block_2x8`,
  `ffn_block_2x8`, `bert_tiny_block_2x8`), train 2 (`train_step_2x2/_4x4`).
- Claim drift verified: README lists attention/transformer as **Planned**
  while `src/gradus.fab:32-34` + `src/transformer.fab` record a shipped
  BERT-tiny slice; `AGENTS.md` references `corpus/nanogpt-shakespeare` but
  **no `corpus/` exists**; `AGENTS.md` references `docs/module-map.md` +
  `docs/api-shape-policy.md` but **docs/ holds only `factory/`**; the
  co-located `src/**/*.proba` rule has **zero `.proba` files** in the tree.
- Snapshot: gradus HEAD `29d26735d0d9` and radix HEAD `a01543b06bfe` match the
  campaign's pins; gradus dirt = untracked `docs/factory/README.md` +
  `docs/factory/production-ml-library/` (the campaign draft itself — expected).
  Norma/faber/hosts/examples must be refreshed by U1.
- GI4+ stale clauses (C1 targets, grep-verified live): model-runtime and
  tokenizer owners = **`faber-runtime`** in `gi0-delivery.md:59-60` /
  `gi0-closeout.md:27`; `gi4-contract.md`/`gi4-delivery.md` assign
  `faber-runtime/src/{partition,device,prefill}.rs` + session/invocation types
  to GI4 (`gi4-delivery.md:200`: no `KvCacheLayout`/`SequenceState` type exists).
- Validation facts: README generator `--factory-root docs/factory --check`
  green today (2 goals, exit 0); `audit-factory-goal-status.py` **does** support
  `--factory-root` (line 583) + `--fail-on error`; gradus gates =
  `./scripta/check-source` (grep-based) + `./scripta/check-compile`
  (`faber check`, no cargo).
- Authority order (campaign): live Gradus source + tests → accepted Gradus
  contracts → accepted compiler/package contracts → campaign stage receipts →
  examples and historical plans.

## Unit Graph

All units are docs/measurement with hard `done_when`. Write scope is
`gradus/docs/factory/production-ml-library/` unless stated. No unit needs
`cargo build/test`; validation uses doc-existence checks, `--check` scripts,
grep-count proofs, and one small shell/python assertion per doc.
### PML0-U1 — Source snapshot refresh + dirty-state record
- **done_when**: `pml0-source-snapshot.md` committed listing all six pinned
  revisions, per-repo `git status --porcelain` dirty state, and a "drift
  replaced" line per correction; the six `git rev-parse` values equal live HEADs.
- **write_scope**: `pml0-source-snapshot.md`. **est_work_tokens**: 6k–12k.
- **tool_latency**: none (git reads only). **dependencies**: none.
- **validation**: `git rev-parse HEAD` in all six repos diffed against the doc;
  `git diff --check`.
- **parallel_children_considered**: indivisible (one revision set, one dirty
  table); later units consume its stamps.
### PML0-U2 — Public symbol inventory
- **done_when**: `scripta/inventory-public-symbols` (grep-based; emits module →
  `functio` table + total) committed; output captured as
  `pml0-symbol-inventory.md`; assertions hold: total `functio` == 21 and
  per-module counts match baseline (nn 6, train 4, loss 3, transformer 3,
  gradient 2, optimize 2, attention 1).
- **write_scope**: `gradus/scripta/inventory-public-symbols` +
  `pml0-symbol-inventory.md`. **est_work_tokens**: 8k–16k.
- **tool_latency**: none (grep, <1 s). **dependencies**: U1 (version stamps).
- **validation**: `./scripta/inventory-public-symbols` output diffs clean
  against the doc; the `grep -c 'functio ' src/*.fab` total == 21 assertion;
  `git diff --check`.
- **parallel_children_considered**: runs beside U4/U5 after U1 (own script
  file, disjoint).
### PML0-U3 — Proof-shaped API ledger
- **done_when**: `pml0-proof-api-ledger.md` committed enumerating the 17
  grep-verified fixed-shape functions with module, name, shape, caller
  evidence (or "none"), and a disposition (retire / admit / replace) under the
  clean-break rule — no preservation without a real external caller.
- **write_scope**: `pml0-proof-api-ledger.md`. **est_work_tokens**: 8k–16k.
- **tool_latency**: none. **dependencies**: U2 (inventory feeds the rows).
- **validation**: `grep 'functio' src/*.fab | grep -c '_2x2\|_4x4\|_2x8'` == 17
  matches the doc's 17 rows and per-module breakdown; every row has a
  disposition; `git diff --check`.
- **parallel_children_considered**: indivisible (one ledger, one disposition
  vocabulary); parallel with U6 after U2.
### PML0-U4 — Module DAG + ownership table
- **done_when**: `pml0-module-dag.md` committed with (a) the import DAG of the
  11 live modules, (b) each module exactly once in a shared/training/inference/
  other ownership table, (c) a section defining the future shared layer
  (forward semantics usable with and without autograd) per the desired end state.
- **write_scope**: `pml0-module-dag.md`. **est_work_tokens**: 10k–20k.
- **tool_latency**: none. **dependencies**: U1, U2.
- **validation**: `grep -o 'gradus:[a-z_]*' src/*.fab | sort -u` rows all
  resolve to live modules; the 11 live modules appear in the table (grep-count);
  `git diff --check`.
- **parallel_children_considered**: parallel with U3/U5/U6 (doc-only, disjoint).
### PML0-U5 — Support-matrix schema
- **done_when**: `pml0-support-matrix-schema.md` committed defining the
  versioned row schema (format, architecture, dtype, quantization, shape,
  tokenizer identity, legal fixture ref, oracle ref, evidence links,
  compatibility policy) with a "one admitted row first" posture and explicit
  reject-row rules; includes an empty row template and a schema version stamp.
- **write_scope**: `pml0-support-matrix-schema.md`. **est_work_tokens**: 8k–14k.
- **tool_latency**: none. **dependencies**: U1.
- **validation**: doc contains each required field with a validation rule; zero
  populated product rows (template only); `git diff --check`.
- **parallel_children_considered**: parallel with U3/U4/U6; U12 later consumes
  its row vocabulary.
### PML0-U6 — Numerical + claim-drift baseline
- **done_when**: `pml0-numerical-baseline.md` committed with (a) a per-module
  coverage table (functions vs co-located `.proba` — currently **zero** proba
  files in the tree), (b) the four verified claim drifts each with a correction
  disposition, (c) a "measured, not claimed" header.
- **write_scope**: `pml0-numerical-baseline.md`. **est_work_tokens**: 8k–16k.
- **tool_latency**: low — `check-compile` runs `faber check` (seconds to ~1
  min, no cargo). **dependencies**: U1, U2.
- **validation**: `./scripta/check-source && ./scripta/check-compile` exit 0;
  `find . -name '*.proba' -not -path './worktrees/*' | wc -l` == 0 matches doc;
  `git diff --check`.
- **parallel_children_considered**: parallel with U3/U4/U5; single closeout run
  of check-source/check-compile (Cargo discipline).
### PML0-U7 — Admission-code migration mechanics decision (C3)
- **done_when**: `pml0-admission-migration-decision.md` committed deciding, for
  GI1's accepted admission code in `faber-runtime` (`gguf.rs`, `tokenizer/`,
  `dequant.rs`), either "migrate into Gradus" or "formally retire", with: a
  named decision owner, a fallback rule if the chosen path is blocked, and an
  explicit **no-dual-authority** statement enforced by **code location** (one
  owning module path named; the other location must not host admission logic).
  A Vivi need recording the decision is filed To `operator@`.
- **write_scope**: `pml0-admission-migration-decision.md`. **est_work_tokens**:
  8k–14k. **tool_latency**: none.
- **dependencies**: U1; read-only facts from `gi1-closeout.md`/`gi2-closeout.md`.
- **validation**: doc contains owner, fallback, and the named single owning
  code location; cited GI grep findings form U11's reconciliation list;
  `git diff --check`.
- **parallel_children_considered**: parallel with U8/U14 (decision docs, no
  shared surface); feeds U11.
### PML0-U8 — `norma:model` migration decision
- **done_when**: `pml0-norma-model-decision.md` committed recording the
  destination-API posture for the Safetensors/GGUF parsing in
  `../norma/src/model.fab` (migrate at PML2, not now), the no-dual-authority
  rule, the no-stranded-callers condition, the fallback if a caller is found;
  decision owner named.
- **write_scope**: `pml0-norma-model-decision.md`. **est_work_tokens**: 6k–12k.
- **tool_latency**: none. **dependencies**: U1.
- **validation**: doc names the target stage (PML2), the transfer condition, and
  the fallback; grep shows no gradus→norma imports (self-contained rule intact);
  `git diff --check`.
- **parallel_children_considered**: parallel with U7/U14.
### PML0-U9 — Cross-campaign interface packet v1 (C4)
- **done_when**: `pml0-interface-packet.md` committed, version-stamped v1 and
  labeled **"revisable through PML1/NGAB1"** (not frozen-for-all-phases),
  containing: semantic identities for model/tokenizer/parameters/
  generation-config/KV state; compile-time vs load-time vs call-time fact
  classes; typed values/layouts/mutation/lifetimes/observations/reset/
  cancellation/errors; host-device ABI + manifest-version relationship;
  version-bump authority + rejection/migration policy; frozen-now vs
  reserved-seam field split; **no device handle, no HTTP policy**. Cross-links
  the NGAB0 packet and `gi3-contract.md` facts.
- **write_scope**: `pml0-interface-packet.md`. **est_work_tokens**: 12k–20k.
- **tool_latency**: none. **dependencies**: U4, U5, U1.
- **validation**: doc contains every listed section; "device handle" appears
  only in the exclusion clause; revision label present; `git diff --check`.
- **parallel_children_considered**: indivisible (one packet, one version
  authority); pairs with NGAB0's packet in a parallel lane.
### PML0-U10 — `pml0-gradus-contract.md` assembly (required output)
- **done_when**: `pml0-gradus-contract.md` committed as the top-level PML0
  contract: summarizes U2-U9 artifacts, names the interface-packet revision it
  references, restates ownership matrix + non-goals (no device handle, no
  serving, correctness before performance), and is the document NGAB0 lists as
  a Gradus required output.
- **write_scope**: `pml0-gradus-contract.md`. **est_work_tokens**: 10k–20k.
- **tool_latency**: low (README regen check). **dependencies**: U2, U3, U4,
  U5, U6, U8, U9.
- **validation**: doc links each of U2-U9 artifacts by path; README generator
  `--check` exit 0 after regen; `git diff --check`.
- **parallel_children_considered**: assembly — the synthesis owner; no parallel
  children on the same file.
### PML0-U11 — GI4+ ownership amendment + migration map in radix (C1, HARD PREREQUISITE)
- **done_when**: `gi4-ownership-amendment.md` committed in
  `radix/docs/factory/gpu-inference-gguf/` plus a migration map, the stale
  `faber-runtime` runtime-owner clauses in `gi0-delivery.md:59-60`,
  `gi0-closeout.md:27`, `gi4-contract.md`, `gi4-delivery.md` reconciled, and
  (C2) the MD3I entry gate in `radix/docs/factory/gpu-inference-multi-device/
  CAMPAIGN.md` ("MD3 + GI4 accepted — GI4 contract freeze") amended to the new
  contract authority (Gradus PML5 decode/KV semantics + NGAB composite session
  facts). Exit condition: **no GI4+ doc still assigns model runtime, tokenizer
  runtime, or serving to `faber-runtime`**; a GI-dir grep shows only amendment
  + reconciliation notes. This is a PML0 **required unit**, not a side-output —
  PML0 cannot close without it.
- **write_scope**: `radix/docs/factory/gpu-inference-gguf/gi4-ownership-amendment.md`
  + reconciliation edits to the four GI docs above
  + `radix/docs/factory/gpu-inference-multi-device/CAMPAIGN.md` (MD3I entry
  gate, C2). **est_work_tokens**: 12k–24k.
- **tool_latency**: low (radix README check). **dependencies**: U7 (decision
  feeds the map), U1.
- **validation**: `grep -rn 'faber-runtime' radix/docs/factory/gpu-inference-gguf/`
  returns only amendment/reconciliation citations (assertion: no line assigns
  runtime ownership); `cd radix && python3 scripta/generate-factory-readme.py
  --check` exit 0; `git diff --check`.
- **parallel_children_considered**: sole writer of the GI docs — no parallel
  children there; the phase-critical path.
### PML0-U12 — Cross-campaign claim/capability register skeleton (C5)
- **done_when**: `pml0-claim-register.md` committed with a versioned row schema
  (claim, status vocabulary: `accepted`/`partial`/`in flight`, owner, evidence
  ref, campaign stage) and the first Gradus rows (autograd wrapper = accepted-
  proof, static-shape SGD = accepted-proof, attention/transformer =
  in-flight-claim, GGUF/Safetensors admission = none), so register status can
  never read as product support.
- **write_scope**: `pml0-claim-register.md`. **est_work_tokens**: 6k–12k.
- **tool_latency**: none. **dependencies**: U5 (row vocabulary), U9.
- **validation**: schema section + ≥6 populated Gradus rows, each with a status
  from the closed vocabulary; `git diff --check`.
- **parallel_children_considered**: parallel with U13/U14 after U5.
### PML0-U13 — Joint receipt schema + Gradus-scoped audit entrypoint (C7)
- **done_when**: (a) `pml0-receipt-schema.md` committed defining the joint
  cross-repo receipt schema (repo, commit, dirty state, command, artifact hash,
  verdict, stage) shared with NGAB0 receipts; (b) `gradus/scripta/check-factory-goal-status`
  committed as a thin wrapper calling the shared audit scoped to gradus, with
  the selection documented in `pml0-audit-entrypoint.md` — the campaign's
  "add or select a Gradus-scoped audit entrypoint" requirement.
- **write_scope**: `pml0-receipt-schema.md`, `pml0-audit-entrypoint.md`,
  `gradus/scripta/check-factory-goal-status`. **est_work_tokens**: 8k–16k.
- **tool_latency**: low (audit + README check, seconds). **dependencies**: U9
  (ABI/manifest version relationship), U14 (capsule).
- **validation**: `./scripta/check-factory-goal-status --fail-on error` exits 0
  with 0 findings; `python3 ../radix/scripta/audit-factory-goal-status.py
  --factory-root docs/factory --fail-on error` matches; README `--check` exit 0;
  `git diff --check`.
- **parallel_children_considered**: runs parallel with U12/U11; wrapper file is
  its own surface.
### PML0-U14 — Admitted-model capsule contract (C8)
- **done_when**: `pml0-model-capsule-contract.md` committed defining the typed
  admitted-model capsule as the handoff across owner boundaries: validated
  bytes + cryptographic identity + tokenizer identity + quantization + bounds +
  architecture facts; states raw GGUF bytes/paths are **not** trust anchors and
  only the capsule carries identity across Gradus ↔ faber-runtime/hosts;
  schema version-stamped.
- **write_scope**: `pml0-model-capsule-contract.md`. **est_work_tokens**: 8k–14k.
- **tool_latency**: none. **dependencies**: U1; read-only facts from
  `gi1-closeout.md` admission behavior.
- **validation**: doc names all six capsule fields with validation rules, the
  non-trust-anchor statement, and a schema version; `git diff --check`.
- **parallel_children_considered**: parallel with U7/U8/U12.

## Parallelism And Lane Notes

- **Lane A (measure)**: U1 → U2 → U3 + U6.
- **Lane B (structure)**: U1 → U4 + U5 (parallel with Lane A after U1).
- **Lane C (decisions)**: U1 → U7 (C3) + U8 + U14 (C8), parallel; U7 → U11
  (C1, phase-critical).
- **Lane D (cross-campaign)**: U5 → U9 (C4) + U12 (C5); U9/U14 → U13 (C7).
- **Assembly**: U10 after all of U2-U9.
- **Shared hot paths**: none — PML0 touches no faber/radix/hosts/gradus product
  code. Each unit owns a disjoint new file (or exclusive doc/script path), so
  up to ~4 lanes run concurrently. U11 is the only writer in the radix GI docs.
- **Consumes GI facts read-only**: U7/U11/U14 read `gi0-closeout.md`,
  `gi1-closeout.md`, `gi2-closeout.md`, `gi4-contract.md`, `gi4-delivery.md`;
  U9 reads `gi3-contract.md`. No GI stage is reopened.
- **NGAB0 parallelism**: U9 pairs with the NGAB0 interface packet (faber side,
  same week); both are labeled revisable through PML1/NGAB1. NGAB0's required
  outputs include the Gradus `pml0-gradus-contract.md` (U10) — the campaigns
  converge on U10/U11, so U11's amendment and U10's contract are the shared
  merge point.

## Checkpoints And Gates

- **Gate A (baseline frozen)**: U1-U6 done — baseline committed, claim drifts
  corrected, `check-source`/`check-compile` green once.
- **Gate B (ownership + migration)**: U7, U8 decisions recorded with operator
  disposition; **U11 amendment committed in radix GI docs** (C1 hard
  prerequisite — PML0 cannot close while GI4+ assigns runtime to old owners).
- **Gate C (cross-campaign + closeout)**: U9-U14 done; U10 contract committed;
  README regenerated; Gradus-scoped audit entrypoint (U13) returns **0
  findings**; every PML0 gate item has a committed artifact; `git diff --check`
  clean across both repos.
- No release bump; no product commit; no cargo invocation.

## Validation

```bash
cd /Users/ianzepp/work/faberlang/gradus && ./scripta/check-source && ./scripta/check-compile
cd /Users/ianzepp/work/faberlang/gradus && python3 ../radix/scripta/generate-factory-readme.py --factory-root docs/factory
cd /Users/ianzepp/work/faberlang/gradus && python3 ../radix/scripta/generate-factory-readme.py --factory-root docs/factory --check
cd /Users/ianzepp/work/faberlang/gradus && ./scripta/check-factory-goal-status --fail-on error
cd /Users/ianzepp/work/faberlang/radix && python3 scripta/generate-factory-readme.py --check
cd /Users/ianzepp/work/faberlang && git -C gradus diff --check && git -C radix diff --check
```

## Open Questions

- First GGUF architecture/quantization row for PML2 — deferred to PML1.
- First production tensor API shape posture (generic / generated / staged mix)
  — PML0 records compiler evidence only (U4/U9); decision lands at PML1.
- Which application repo supplies the PML7 inference capstone — routed to the
  inference product campaign shell after PML0.
- U7 outcome (migrate vs retire GI1 admission code) — operator decision; the
  recorded defaults proceed until overridden.

## Council Dispositions (folded)

| Item | Mandate | Lands in |
| --- | --- | --- |
| C1 | GI4+ ownership amendment + migration map committed in radix `gpu-inference-gguf/`, stale `faber-runtime`/GI4+ clauses reconciled | **U11** — required unit, hard exit condition; Gate B |
| C2 | MD3I entry gate ("MD3 + GI4 accepted — GI4 contract freeze") amended to the new contract authority (Gradus PML5 decode/KV semantics + NGAB composite session facts) | **U11** — folded into C1's migration map; same write scope |
| C3 | Admission-migration mechanics decision, no-dual-authority by code location, owner + fallback | **U7** — decision record feeding U11's map |
| C4 | Interface packet v1: version authority + change procedure, labeled revisable through PML1/NGAB1; full contents list; no device handle, no HTTP policy | **U9** — paired with NGAB0's packet; referenced by U10 |
| C5 | Versioned claim/capability register skeleton (accepted/partial/in flight) | **U12** — first Gradus rows |
| C7 | Joint cross-repo receipt schema + Gradus-scoped audit entrypoint | **U13** — wrapper + selection; closes the campaign's status-audit gate |
| C8 | Admitted-model capsule as typed handoff; raw bytes/paths not trust anchors | **U14** — capsule schema, consumed by U13 receipts |
