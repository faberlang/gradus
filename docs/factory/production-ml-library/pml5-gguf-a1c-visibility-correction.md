# Delivery Lowering — A1C Visibility Correction: SEM006 Cross-Module Function Visibility Units (shape / dtype / tensor) + Aggregate Merge Retry Gate

**Planner**: planner-38. **Assignment**: task `125a0fbc` (Mind, 2026-08-13T16:54:05+00:00) —
"lower Qwen-critical Gradus visibility correction".
**Resume/correction**: mail `8f46be38` (captured `39a0bd41`, Mind, 2026-08-13T20:46:21+00:00).
**Supersedes (as lowerings go)**: the pre-VIS-01/04/05 27-error declaration set
(`dtype.DType`, `artifact.IdentitasContenuti`, `capsule.Capsula`) — already landed via
VIS-01/VIS-04/VIS-05 and no longer the failing surface.
**Current authority**: failed aggregate task `9058ef55` ("A1C-M8R2: retry aggregate gate
after Tensor repair"), refusal report `7ee11a87`, Gradus main/`factory/merge` `1462cd8`,
A1C candidate `factory/a1c-chain` `7221555` (untouched, re-runnable).
**Campaign**: [`radix/docs/factory/gpu-production-readiness/CAMPAIGN.md`](../../../../radix/docs/factory/gpu-production-readiness/CAMPAIGN.md)
(exact Qwen3.6 completion contract; sole-priority goal `gol_634a0417d02c510f`).
**Delivery authority**: [`pml5-general-gguf-delivery.md`](pml5-general-gguf-delivery.md) §GGUF-A1c.
**Repo baselines**: Gradus `1462cd8` (`1462cd874bb6`); Radix `b6d6e17`; Hosts `57d659d`;
Faber `1fb6cc97`. Planner-38 lane verified clean at those tips.

## 1. Goal-check verdict (compact)

- **Goal path**: campaign mandatory work row `LIB-01` → GGUF-A1c (the correction is mandatory
  enabling work for LIB-01 through CLOSE-01; scope_closure contract from task `125a0fbc`).
- **Evaluator mode**: goal-check + delivery lowering of the current correction per
  Mind correction `8f46be38` (reproduce usage-driven declaration set; re-lower into
  one-logical-change units by declaration module; add one aggregate merge retry gate).
- **Intended consumer**: delivery (Mind dispatches the visibility Hands, then the A1C chain).
- **Verdict**: **READY**.
- **Reasoning**: the baseline is exactly 56 `SEM006:import_module_private` diagnostics on
  12 module-private **functions** in `shape.fab` / `dtype.fab` / `tensor.fab`, consumed
  cross-module by 7 library files (reproduced live under the report `7ee11a87` authority
  setup; identical on main `1462cd8` and candidate `7221555`, so the A1C chain introduced
  none of them). Each of the 12 declarations is a genuine public cross-module consumer
  surface (usage inventory §3), none is a genuinely private `_`-prefixed helper (§4), and
  all 12 names are already documented in `docs/api-reference.md` (verified — so the
  annotation-only change has zero doc/inventory ripple). The lowering is 3 parallel
  single-file annotation units + 1 aggregate merge retry gate that re-runs A1C-M8R2 after
  the units land.
- **Blocking gaps**: none within the correction's scope. Named, routed residuals: model/*
  visibility surfaces that are the A1C chain's own files (see §10); they do not appear
  under the authority setup (§2) and are explicitly not absorbed here.

## 2. Reproduction evidence (authority setup, planner-38 lane, 2026-08-13)

Setup matches report `7ee11a87`: current-Faber binary 1.6.0 built from radix `b6d6e17c8`
(`worktrees/hand-24/radix/target/debug/faber`); `FABER_LIBRARY_HOME=worktrees/merge`
(script default in the merge lane — the same home that yields the correction's 56 count);
`FABER_BIN` exported explicitly. Command: `./scripta/check-compile` (gradus `scripta`).

| Target | Ref | `./scripta/check-compile` | `SEM006` total | Shape | Dtype | Tensor | Other |
| --- | --- | --- | --- | --- | --- | --- | --- |
| main (baseline) | `1462cd8` | exit 1, FAILED | **56** | 12 | 31 | 13 | 0 |
| candidate (A1C chain) | `7221555` | exit 1, FAILED | **56** | 12 | 31 | 13 | 0 |

- First error (identical to report): `math.fab:6286` → `redde forma.broadcastum(a, b)`
  (`broadcastum` module-private in `shape.fab`, zero `@ publica` in the whole file).
- Per-file SEM006 distribution (identical between the two refs): math 15, parameter 11,
  loss 10, train 7, metrics 6, cache 4, gradient 3. No `model/*`, `tests/`, or `exempla/`
  site under the authority setup.
- Library files are byte-identical between `1462cd8` and `7221555` (reproved via the
  identical error set; the A1C chain only rewrote its own `model/*` + docs surfaces).
- `faber check src/<module>.fab` alone (lane-local `FABER_BIN`, `FABER_LIBRARY_HOME`):
  `shape.fab`, `dtype.fab`, `tensor.fab` each exit 0 (LOCALE002 warnings only) — the
  failures are purely cross-module imports, i.e. `import_module_private`.
- Caveat recorded: with a **different** `FABER_LIBRARY_HOME` (e.g. the planner-38 lane
  parent) module resolution of `gradus:*` package imports can resolve against the library
  home's gradus copy and surface extra `model/*` diagnostics (capsule/manifestum). The
  authority setup (merge lane home) is the one that reproduces the correction's 56 and the
  refused gate's count; all unit proofs and the retry gate use it.

## 3. Usage-driven declaration set (12 symbols, 56 SEM006 sites)

Verified live on `1462cd8`. `@ publica` must be inserted as a one-line annotation
immediately above each `functio` declaration (the VIS-04/VIS-05 convention; same syntax as
`@ publica` on `genus Tensor` at `tensor.fab:132` and the `dtype` tag factories at
`dtype.fab:80..95`).

### Unit VIS-S — `src/shape.fab` (4 annotations, clears 12 sites)

| Line | Declaration | Cross-module consumers (site count) |
| --- | --- | --- |
| 95 | `functio causa(FormaError e) → textus {` | math, loss (3) |
| 108 | `functio valet(lista<numerus> forma) → bivalens {` | parameter (1) |
| 146 | `functio quantitas(lista<numerus> forma) → numerus ⇥ FormaError {` | math, loss (2) |
| 166 | `functio broadcastum(lista<numerus> a, lista<numerus> b) → lista<numerus> ⇥ FormaError {` | math (6) |

### Unit VIS-D — `src/dtype.fab` (5 annotations, clears 31 sites)

| Line | Declaration | Cross-module consumers (site count) |
| --- | --- | --- |
| 131 | `functio causa(DTypeError e) → textus {` | math, parameter (4) |
| 144 | `functio nomen(DType t) → textus {` | cache, loss, metrics, parameter (10) |
| 153 | `functio ex_nomine(textus s) → DType ⇥ DTypeError {` | math, parameter (3) |
| 272 | `functio finita(f32 x) → bivalens {` | loss, metrics, train (13) |
| 287 | `functio casta(f32 valor, DType origo, DType scopum) → f32 ⇥ DTypeError {` | math (1) |

### Unit VIS-T — `src/tensor.fab` (3 annotations, clears 13 sites)

| Line | Declaration | Cross-module consumers (site count) |
| --- | --- | --- |
| 210 | `functio causa(TensorError e) → textus {` | cache, gradient, math, parameter, train (6) |
| 242 | `functio structa(lista<f32> datos, lista<numerus> forma) → Tensor ⇥ TensorError {` | cache, gradient, math, train (5) |
| 250 | `functio structa_typo(lista<f32> datos, lista<numerus> forma, dtype.DType typo) → Tensor ⇥ TensorError {` | parameter (2) |

Note: `tensor.fab` already carries `@ publica` on `genus Tensor` (:132, VIS-05) — that is
the genus-visibility fix that landed; the three functions above are the remaining
module-private cross-module surfaces of the same module.

## 4. Non-goals, preserved privacy, ripple

- **Preserved `@ privata` helpers** (no blanket sweep): `shape.fab` `_productus` (:124),
  `_dimensio` (:152); `tensor.fab` `_quantitas_forma` (:229); `dtype.fab` `_*` family and
  any other `_`-prefixed name. These are module-internal and stay private.
- **No other files edited** by the three units. No `.proba`, no `docs/`, no `scripta/`,
  no `tests/`, no `model/*`, no other repo.
- **Zero inventory/doc ripple (verified)**: `scripta/inventory-public-symbols` counts
  `functio ` declaration lines — annotation lines change no count, so the per-module
  table and the tracked total 618 are unchanged; its coverage gate requires every
  non-`_` function name to appear in `docs/api-reference.md`, and all 12 names are already
  documented under `## gradus:shape` / `## gradus:dtype` / `## gradus:tensor` (spot-checked
  `broadcastum`, `quantitas`, `valet`, `finita`, `ex_nomine`, `casta`, `structa_typo` all
  ≥1 hit). The correction therefore needs no M5/M6-style follow-up.
- **No semantic change**: `@ publica` on an already cross-module-consumed function does not
  alter behavior; module-private semantics are preserved for everything not annotated.
- **A1C chain serialization preserved**: per the A1C micro-unit doc §7 conclusion (the
  "27-error" premise is superseded by this baseline, the ordering conclusion is not), the
  visibility correction merges to `factory/merge` **before A1C M1 starts** so the
  package-check baseline is SEM006-green throughout the A1C chain.

## 5. Unit graph

```
factory/merge (1462cd8)
  ├─ VIS-S  shape.fab @ publica ×4      (parallel, disjoint file)
  ├─ VIS-D  dtype.fab @ publica ×5      (parallel, disjoint file)
  └─ VIS-T  tensor.fab @ publica ×3     (parallel, disjoint file)
        │  (each merges to factory/merge individually — safe alone: additive annotation)
        ▼
factory/merge green on the 56 (12 symbols)
        │
        ▼
A1C chain resumes: M1 → M2∥M3∥M5 → M4∥M6∥M7 → M8   (its own delivery doc)
        │
        ▼
G  A1C-M8R2 aggregate merge retry gate (the only gate; re-runs the refused 7ee11a87 gate)
```

- **Maximum safe parallelism**: 3 (VIS-S ∥ VIS-D ∥ VIS-T), disjoint primary files.
- **Integration**: each VIS unit merges to `factory/merge` on its own
  `factory/<lane>` branch; no dual-authority or intermediate-broken state is possible
  (adding `@ publica` cannot break any module). Merge order among the three is free.
- **Branch protocol**: `factory/<lane>` off `factory/merge`, commit message
  `fix(gradus): expose <module> <symbols> to package consumers` style (VIS-04/VIS-05
  precedent), `non-integrable` marker **not** required (each is individually integrable),
  but the A1C-M8R2 gate G must not be run until all three are on `factory/merge`.

## 6. Unit specs

### VIS-S — shape module publica (4 symbols)

| Field | Value |
| --- | --- |
| `outcome` | `shape.broadcastum`, `shape.quantitas`, `shape.valet`, `shape.causa` are `@ publica`; the 12 SEM006 sites that reference them across math/loss/parameter are gone |
| `primary files` | `src/shape.fab` (1) |
| `write_scope` | `src/shape.fab` — exactly 4 one-line `@ publica` insertions at :95, :108, :146, :166 (immediately above each `functio`, after any preceding comment block) |
| `read_scope` | this delivery §3 table; `docs/api-reference.md` `## gradus:shape` (names already documented — do not touch) |
| `forbidden_scope` | any other annotation; any edit to `_productus`/`_dimensio` or any other `_`-helper; `.proba`/`docs/`/`scripta/`/`tests/`/`model/*`; check-compile/package/stage gates (none on Hands); absorbing dtype/tensor errors |
| `red` | before change (authority setup, lane-local `FABER_BIN`/`FABER_LIBRARY_HOME`): `faber check src/math.fab` emits `SEM006:import_module_private` lines whose code references `forma.` (first: `math.fab:6286` `forma.broadcastum`). Record first divergence |
| `green` | `faber check src/shape.fab` exit 0; `grep -n -B1 "functio \(broadcastum\|quantitas\|valet\|causa\)" src/shape.fab` shows `@ publica` immediately above all four; focused importer sanity: `faber check src/math.fab` output contains **no** `SEM006` line referencing `forma.` (the importer may still show `dtype.`/`tensor.` sites — those belong to VIS-D/VIS-T; record them, do not fix); `git diff --check` silent |
| `done_when` | (a) 4 `@ publica` lines present exactly at the §3 lines; (b) shape.fab check exit 0; (c) zero `forma.` SEM006 in the math importer sanity; (d) `git diff --check` silent; (e) report records the importer's remaining `dtype.`/`tensor.` site count as owned by VIS-D/VIS-T |
| `est_work_tokens` | 3–4k |
| `est_basis` | pilot; 4 one-line annotations + one narrow importer check (VIS-04/VIS-05 scale) |
| `tool_latency` | low — two single-file `faber check` invocations + greps |
| `depends_on` | base `factory/merge` `1462cd8` |
| `parallel_with` | VIS-D, VIS-T |
| `integrable` | **yes** (additive annotation; merges to `factory/merge` alone) |
| `risk` | negligible — behavior identical; all 4 names already documented |

### VIS-D — dtype module publica (5 symbols)

| Field | Value |
| --- | --- |
| `outcome` | `dtype.finita`, `dtype.nomen`, `dtype.ex_nomine`, `dtype.casta`, `dtype.causa` are `@ publica`; the 31 SEM006 sites across cache/loss/metrics/parameter/train/math are gone |
| `primary files` | `src/dtype.fab` (1) |
| `write_scope` | `src/dtype.fab` — exactly 5 one-line `@ publica` insertions at :131, :144, :153, :272, :287 |
| `read_scope` | this delivery §3 table; `docs/api-reference.md` `## gradus:dtype` (names already documented) |
| `forbidden_scope` | any other annotation; edits to the existing `@ publica` blocks (:69–:95 tag factories / `discretio DType`) or to `discretio DTypeError`; `_`-helpers; any non-`src/dtype.fab` file; check-compile/package/stage gates; absorbing shape/tensor errors |
| `red` | before change: `faber check src/loss.fab` (or `src/metrics.fab`/`src/train.fab`) emits SEM006 referencing `dtype.` (e.g. `dtype.finita`, `dtype.nomen`). Record first divergence |
| `green` | `faber check src/dtype.fab` exit 0; `grep -n -B1 "functio \(finita\|nomen\|ex_nomine\|casta\|causa\)" src/dtype.fab` shows `@ publica` above all five; focused importer sanity: `faber check src/loss.fab` and `faber check src/train.fab` output contains **no** `SEM006` line referencing `dtype.`; `git diff --check` silent |
| `done_when` | (a) 5 `@ publica` lines present exactly at the §3 lines; (b) dtype.fab check exit 0; (c) zero `dtype.` SEM006 in the loss/train importer sanity; (d) `git diff --check` silent; (e) report records the importer's remaining `shape.`/`tensor.` site count as owned by VIS-S/VIS-T |
| `est_work_tokens` | 3–4k |
| `est_basis` | pilot; 5 one-line annotations + two narrow importer checks |
| `tool_latency` | low — three single-file `faber check` invocations + greps |
| `depends_on` | base `factory/merge` `1462cd8` |
| `parallel_with` | VIS-S, VIS-T |
| `integrable` | **yes** |
| `risk` | negligible |

### VIS-T — tensor module publica (3 symbols)

| Field | Value |
| --- | --- |
| `outcome` | `tensor.structa`, `tensor.structa_typo`, `tensor.causa` are `@ publica`; the 13 SEM006 sites across cache/gradient/math/parameter/train are gone |
| `primary files` | `src/tensor.fab` (1) |
| `write_scope` | `src/tensor.fab` — exactly 3 one-line `@ publica` insertions at :210, :242, :250; do **not** move or duplicate the existing `@ publica` at :132 (`genus Tensor`, VIS-05) |
| `read_scope` | this delivery §3 table; `docs/api-reference.md` `## gradus:tensor` (names already documented) |
| `forbidden_scope` | any other annotation; edits to `genus Tensor` (:132) or `_quantitas_forma` (:229); any non-`src/tensor.fab` file; check-compile/package/stage gates; absorbing shape/dtype errors |
| `red` | before change: `faber check src/train.fab` (or `src/cache.fab`) emits SEM006 referencing `tensor.` (e.g. `tensor.structa`, `tensor.causa`). Record first divergence |
| `green` | `faber check src/tensor.fab` exit 0; `grep -n -B1 "functio \(structa\|structa_typo\|causa\)" src/tensor.fab` shows `@ publica` above all three (note `structa` vs `structa_typo` — assert both); focused importer sanity: `faber check src/train.fab` and `faber check src/cache.fab` output contains **no** `SEM006` line referencing `tensor.`; `git diff --check` silent |
| `done_when` | (a) 3 `@ publica` lines present exactly at the §3 lines; (b) tensor.fab check exit 0; (c) zero `tensor.` SEM006 in the train/cache importer sanity; (d) `git diff --check` silent; (e) report records the importer's remaining `shape.`/`dtype.` site count as owned by VIS-S/VIS-D |
| `est_work_tokens` | 3–4k |
| `est_basis` | pilot; 3 one-line annotations + two narrow importer checks |
| `tool_latency` | low — three single-file `faber check` invocations + greps |
| `depends_on` | base `factory/merge` `1462cd8` |
| `parallel_with` | VIS-S, VIS-D |
| `integrable` | **yes** |
| `risk` | negligible |

## 7. Aggregate merge retry gate — G (A1C-M8R2 retry)

| Field | Value |
| --- | --- |
| `outcome` | the gate refused at `7ee11a87` (task `9058ef55`, A1C-M8R2) is re-run once the VIS units are on `factory/merge`, and its step-1 SEM006 blocker (the 56) is proven cleared; the A1C candidate `7221555` becomes re-runnable through a green package check |
| `primary files` | none — validation + (if green) the A1C integration merge; no product/doc edits |
| `write_scope` | the A1C integration merge into `factory/merge` per the A1C micro-unit doc M8 (merge-lane operation); commit message names the merged VIS + A1C heads |
| `read_scope` | merged `factory/merge` (post VIS-S/D/T), the A1C candidate `7221555`, report `7ee11a87` evidence |
| `forbidden_scope` | any product code; re-running any unit's work; editing source to "fix" the check; absorbing the A1C chain's model/* surfaces; running before all three VIS units are merged |
| `red` (do not merge) | `./scripta/check-compile` still emits any `SEM006:import_module_private` referencing `shape.`/`dtype.`/`tensor.` symbols, or `git diff --check` is not silent → record the exact residual and stop; do not weaken the gate |
| `green` (run once) | authority setup (`FABER_BIN` = current-Faber binary from radix `b6d6e17c8`, `FABER_LIBRARY_HOME` = merge lane parent, script default): `./scripta/check-compile` exit 0 with **zero** `SEM006` on the merged gradus library source; `grep -c SEM006` == 0 vs 56 pre-fix; `git diff --check` silent. Then the A1C chain's own M8 closeout (per its delivery doc) runs and the A1C integration lands |
| `done_when` | (a) the 56-error baseline is reduced to 0 under the authority setup on the merged main; (b) the candidate `7221555` rebased on the fixed main also yields 0 SEM006; (c) residual model/* visibility diagnostics, if any surface under the merged-tree setup, are recorded with their owning A1C unit (M1/M8) and routed — not absorbed; (d) merge lane re-queues A1C-M8R2 |
| `est_work_tokens` | 3–5k |
| `est_basis` | pilot; one aggregate validation pass + merge (matches A1C-M8 scale) |
| `tool_latency` | medium — the only package-level compile in this delivery |
| `depends_on` | VIS-S + VIS-D + VIS-T merged on `factory/merge` |
| `parallel_with` | none — last |
| `integrable` | **the gate itself is the A1C integration**; the A1C chain's M8 remains the sole atomic A1C merge per its delivery doc |

## 8. Serialization vs the A1C chain (mandatory)

1. VIS-S ∥ VIS-D ∥ VIS-T land on gradus `factory/merge` (any order; all three before anything else runs).
2. A1C chain resumes on the corrected `factory/merge` (M1 → M2∥M3∥M5 → M4∥M6∥M7 → M8, per
   `pml5-gguf-a1c-micro-units.md`). Its §7 "27-error" premise is superseded by this
   baseline (the `dtype.DType`/`artifact.IdentitasContenuti`/`capsule.Capsula` errors are
   gone; the live 56 are the 12 shape/dtype/tensor functions lowered here); the §7 ordering
   conclusion (visibility before M1) is unchanged.
3. G re-runs A1C-M8R2 once the A1C integration branch is assembled on the fixed main.
4. If a VIS unit is not landed when M1 is dispatched, M1 waits; M1 must not "help" by adding
   annotations (per the A1C delivery doc).

## 9. Red oracle (review fail conditions)

This lowering must fail review if any child:

- exceeds 8k `est_work_tokens` or touches more than its one primary file;
- adds any annotation beyond the §3 declaration list, or removes/weakens any `@ privata`
  helper (`_productus`, `_dimensio`, `_quantitas_forma`, any `_`-prefixed name);
- runs a broad package/`check-compile`/`inventory-public-symbols` gate (only G may);
- edits docs, `.proba`, `scripta/`, `tests/`, or `model/*` (each unit's forbidden scope);
- claims green while the importer sanity still emits the unit's own symbols (i.e. weakens
  the focused check to "exit 0 on the module alone");
- is dispatched to touch `tensor.fab:132` (`genus Tensor` publica) — that is already landed
  (VIS-05) and must be preserved untouched by VIS-T.

## 10. Named residuals and routes (out of scope, not gaps)

- **model/* visibility surfaces** (candidate `model/capsule.fab` referencing
  `manifestum.ManifestumGguf`; main `model/gguf.fab`/`model/safetensors.fab` referencing
  `capsula.structa`/`capsula.causa`): these are the A1C chain's own rewritten files and its
  M1/M8 surface; not part of the correction's 56 and not absorbed. They did not surface
  under the authority setup (§2). If they appear under the merged-tree setup at G, record
  and route to the A1C chain M1/M8.
- **`inventory-public-symbols` baseline** (total 618): unchanged by this correction
  (verified §4) — no re-baseline unit needed; the A1C chain's M6 re-baseline absorbs any
  future A1C count changes.
- **A1C micro-unit doc §7 premise**: stale "27-error" description is superseded by this
  doc; that doc lives on `factory/planner-39` and is not in this lane — no edit here.
