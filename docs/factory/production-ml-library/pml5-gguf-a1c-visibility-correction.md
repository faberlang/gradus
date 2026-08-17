# Delivery Lowering — A1C Visibility Correction: SEM006 Cross-Module Function Visibility Units (shape / dtype / tensor) + Aggregate Merge Retry Gate

**Planner**: planner-38. **Assignment**: task `125a0fbc` (Mind, 2026-08-13T16:54:05+00:00) —
"lower Qwen-critical Gradus visibility correction".
**Resume/correction**: mail `8f46be38` (captured `39a0bd41`, Mind, 2026-08-13T20:46:21+00:00).
**Audit revise**: task `b8bb6b2c`, auditor-7 report `654ab80b` (verdict revise — P2
`tensor.fill` missing function, P2 §2 count/composition inconsistency). This revision
amends VIS-T to 4 annotations and reconciles the evidence section; no other unit,
boundary, or gate changes.
**Supersedes (as lowerings go)**: the pre-VIS-01/04/05 27-error declaration set
(`dtype.DType`, `artifact.ContentIdentity`, `capsule.Capsule`) — already landed via
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
- **Reasoning**: the declaration set is **13** module-private **functions** in
  `shape.fab` / `dtype.fab` / `tensor.fab` — every documented-public,
  cross-module-consumed function of the three modules, with no member of the class
  missing (audit `654ab80b` confirmed `tensor.fill` was the sole omitted one; added to
  VIS-T below). Statically verified cross-module call sites: **73** for the 13-symbol set,
  of which **48** sit in the 7 library files the refusal report lists as emitting and 25
  in non-emitting importers (§2); `tensor.fill` contributes exactly one site
  (`attention.fab:287`). The gate baseline is the report-recorded **56 total SEM006**
  including `model/*` rows (report `7ee11a87`; composition uncertainty is stated in §2 —
  not invented precision). Each of the 13 declarations is a genuine public cross-module
  consumer surface (usage inventory §3), none is a genuinely private `_`-prefixed helper
  (§4), and all 13 names are already documented in `docs/api-reference.md` (verified — so
  the annotation-only change has zero doc/inventory ripple). The lowering is 3 parallel
  single-file annotation units + 1 aggregate merge retry gate that re-runs A1C-M8R2 after
  the units land.
- **Blocking gaps**: none within the correction's scope. Named, routed residuals: model/*
  visibility surfaces that are the A1C chain's own files (see §10). Report `7ee11a87`
  records them (`model/gguf` 2 + `model/safetensors` 2) inside its 56 total, while a live
  authority-setup reproduction measured none — the composition is unresolved (audit
  `654ab80b` blind spot) and the surfaces are explicitly routed to the A1C chain, not
  absorbed here.

## 2. Evidence — static inventory, report-recorded gate baseline, and emission uncertainty

Setup matches report `7ee11a87` where reproduced: current-Faber binary 1.6.0 built from
radix `b6d6e17c8` (`worktrees/hand-24/radix/target/debug/faber`);
`FABER_LIBRARY_HOME` = merge lane parent (script default); command
`./scripta/check-compile` (gradus `scripta`). **Check-compile is NOT replayed for this
revision** (task `3feac66d` forbids; report `7ee11a87` owns the emitted figure). All
numbers below are either verified static greps (this lane, baseline `1462cd8`) or cited
from report `7ee11a87`; composition uncertainty is stated, not papered over.

**Verified static inventory — cross-module call sites of the 13-symbol set** (non-comment
`shape.|dtype.|tensor.<sym>(`, all non-model `src/**/*.fab`, excluding each declaring
module's own file):

- **73 total** cross-module sites across 13 consumer files.
- **48** of the 73 sit in the 7 files the report lists as emitting: math 10, parameter
  11, loss 10, train 5, metrics 6, cache 4, gradient 2 (= 48; re-verified 1:1 with the
  audit `654ab80b` recount).
- **25** of the 73 sit in importers the report did not list as emitting: attention 5,
  nn 6, generation 4, sampling 4, decode 3, optimize 1, tensor 2 (these call the same
  module-private symbols but did not appear in the emitted set — see emission
  uncertainty below).
- Importer set: **15** non-model `src/*.fab` import `gradus:shape|dtype|tensor`
  cross-module (attention, cache, decode, generation, gradient, gradus, loss, math,
  metrics, nn, optimize, parameter, sampling, train, transformer); 13 of the 15 carry
  call sites of the 13 symbols, gradus.fab and transformer.fab import without such sites.

**Report-recorded gate baseline (report `7ee11a87`)** — the figure the refused gate and
gate G compare against: **56 SEM006 total**, comprising library rows (math 11, parameter
12, loss 8, train 5, metrics 6, cache 4, gradient 2 = 48) **and** `model/gguf` 2 +
`model/safetensors` 2.

**Emission uncertainty (honest, per audit `654ab80b` blind spot)**:
- The report's own per-file rows sum to 52 while it states 56 total — the compiler emits
  diagnostics lexical grep cannot fully account for. A live authority-setup reproduction
  (planner-38 lane, 2026-08-13) measured 56 with a *different* per-file split (math 15,
  parameter 11, loss 10, train 7, metrics 6, cache 4, gradient 3) and **no** model rows.
- Emitted counts exceed static sites: one static `shape.broadcast` site
  (`math.fab:117` physical) emitted 6× in that reproduction; `dtype.finite` has 21
  static cross-module sites but the report's emitted loss+metrics+train rows account for
  fewer. The **56 figure is therefore neither confirmed nor refuted at composition
  level**; the stable, verified fact is the symbol set (§3) and its static inventory.
- Six non-emitting importers (attention, nn, generation, sampling, decode, optimize) and
  `tensor.fab` (calling `shape.message`/`shape.numel`) carry static cross-module sites
  yet did not emit — whether `faber check "$ROOT"` reaches them is compiler-scope-dependent
  and unverified without replay. `attention.fab` is the sole `tensor.fill` consumer
  (`attention.fab:287`), so VIS-T's focused sanity targets it directly (§6).
- Library files are byte-identical between `1462cd8` and `7221555` for all non-model
  surfaces (identical static inventory; the A1C chain only rewrote its own `model/*` +
  docs surfaces). `faber check src/<module>.fab` alone (lane-local `FABER_BIN` /
  `FABER_LIBRARY_HOME`): `shape.fab`, `dtype.fab`, `tensor.fab` each exit 0 (LOCALE002
  warnings only) — the failures are purely cross-module imports
  (`import_module_private`).

## 3. Usage-driven declaration set (13 symbols — static cross-module sites; §2)

Verified statically on `1462cd8`. Site counts are **static cross-module call sites**
(non-comment, excluding the declaring module's own file; the compiler may emit multiple
`SEM006` diagnostics per static site — §2). `@ publica` must be inserted as a one-line
annotation immediately above each `functio` declaration (the VIS-04/VIS-05 convention;
same syntax as `@ publica` on `genus Tensor` at `tensor.fab:132` and the `dtype` tag
factories at `dtype.fab:80..95`).

### Unit VIS-S — `src/shape.fab` (4 annotations, 11 static cross-module sites)

| Line | Declaration | Cross-module consumers (static site count) |
| --- | --- | --- |
| 95 | `functio message(ShapeError e) → textus {` | math (2), loss (1), nn (1), tensor (1) — 5 |
| 108 | `functio valid(lista<numerus> forma) → bivalens {` | parameter (1) — 1 |
| 146 | `functio numel(lista<numerus> forma) → numerus ⇥ ShapeError {` | math (1), loss (1), nn (1), tensor (1) — 4 |
| 166 | `functio broadcast(lista<numerus> a, lista<numerus> b) → lista<numerus> ⇥ ShapeError {` | math (1; emitted 6× in one live reproduction) — 1 |

### Unit VIS-D — `src/dtype.fab` (5 annotations, 46 static cross-module sites)

| Line | Declaration | Cross-module consumers (static site count) |
| --- | --- | --- |
| 131 | `functio message(DTypeError e) → textus {` | math (2), parameter (2) — 4 |
| 144 | `functio name(DType t) → textus {` | loss (4), nn (4), attention (3), cache (2), metrics (2), parameter (2) — 17 |
| 153 | `functio from_name(textus s) → DType ⇥ DTypeError {` | parameter (2), math (1) — 3 |
| 272 | `functio finite(f32 x) → bivalens {` | loss (4), generation (4), metrics (4), sampling (4), train (3), decode (1), optimize (1) — 21 |
| 287 | `functio cast(f32 valor, DType origo, DType scopum) → f32 ⇥ DTypeError {` | math (1) — 1 |

### Unit VIS-T — `src/tensor.fab` (4 annotations, 16 static cross-module sites)

| Line | Declaration | Cross-module consumers (static site count) |
| --- | --- | --- |
| 210 | `functio message(TensorError e) → textus {` | parameter (2), cache (1), decode (1), gradient (1), math (1), train (1), attention (1) — 8 |
| 242 | `functio construct(lista<f32> data, lista<numerus> shape) → Tensor ⇥ TensorError {` | cache (1), decode (1), gradient (1), math (1), train (1) — 5 |
| 250 | `functio construct_dtype(lista<f32> data, lista<numerus> shape, dtype.DType typo) → Tensor ⇥ TensorError {` | parameter (2) — 2 |
| 260 | `functio fill(lista<numerus> shape, f32 valor) → Tensor ⇥ TensorError {` | attention (1 — `attention.fab:287`; `attention.fab:36` imports `gradus:tensor`) — 1 |

Note: `tensor.fab` already carries `@ publica` on `genus Tensor` (:132, VIS-05) — that is
the genus-visibility fix that landed; the four functions above are the remaining
module-private cross-module surfaces of the same module. `tensor.fill` was the sole
member of this class omitted from the prior revision (audit `654ab80b` P2-1 confirmed);
`attention.fab`'s `_fill` wrapper (:286) is `@ privata` and stays private.

## 4. Non-goals, preserved privacy, ripple

- **Preserved `@ privata` helpers** (no blanket sweep): `shape.fab` `_product` (:124),
  `_dimension` (:152); `tensor.fab` `_numel_shape` (:229); `dtype.fab` `_*` family and
  any other `_`-prefixed name. These are module-internal and stay private.
- **No other files edited** by the three units. No `.proba`, no `docs/`, no `scripta/`,
  no `tests/`, no `model/*`, no other repo.
- **Zero inventory/doc ripple (verified)**: `scripta/inventory-public-symbols` counts
  `functio ` declaration lines — annotation lines change no count, so the per-module
  table and the tracked total 618 are unchanged; its coverage gate requires every
  non-`_` function name to appear in `docs/api-reference.md`, and all 13 names (incl.
  `fill`) are already
  documented under `## gradus:shape` / `## gradus:dtype` / `## gradus:tensor` (spot-checked
  `broadcast`, `numel`, `valid`, `finite`, `from_name`, `cast`, `construct_dtype`,
  `fill` all
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
  └─ VIS-T  tensor.fab @ publica ×4     (parallel, disjoint file)
        │  (each merges to factory/merge individually — safe alone: additive annotation)
        ▼
factory/merge SEM006-green on the 13-symbol set
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
| `outcome` | `shape.broadcast`, `shape.numel`, `shape.valid`, `shape.message` are `@ publica`; the `shape.*` `import_module_private` sites are gone — static cross-module sites: 11 (message 5, numel 4, valid 1, broadcast 1) across math/loss/parameter/nn/tensor (§2) |
| `primary files` | `src/shape.fab` (1) |
| `write_scope` | `src/shape.fab` — exactly 4 one-line `@ publica` insertions at :95, :108, :146, :166 (immediately above each `functio`, after any preceding comment block) |
| `read_scope` | this delivery §3 table; `docs/api-reference.md` `## gradus:shape` (names already documented — do not touch) |
| `forbidden_scope` | any other annotation; any edit to `_product`/`_dimension` or any other `_`-helper; `.proba`/`docs/`/`scripta/`/`tests/`/`model/*`; check-compile/package/stage gates (none on Hands); absorbing dtype/tensor errors |
| `red` | before change (authority setup, lane-local `FABER_BIN`/`FABER_LIBRARY_HOME`): `faber check src/math.fab` emits `SEM006:import_module_private` lines whose code references `shape.` (first per report `7ee11a87`: `math.fab` merged-line 6286 = physical :117 `shape.broadcast`). Record first divergence |
| `green` | `faber check src/shape.fab` exit 0; `grep -n -B1 "functio \(broadcast\|numel\|valid\|message\)" src/shape.fab` shows `@ publica` immediately above all four; focused importer sanity: `faber check src/math.fab` output contains **no** `SEM006` line referencing `shape.` (the importer may still show `dtype.`/`tensor.` sites — those belong to VIS-D/VIS-T; record them, do not fix); `git diff --check` silent |
| `done_when` | (a) 4 `@ publica` lines present exactly at the §3 lines; (b) shape.fab check exit 0; (c) zero `shape.` SEM006 in the math importer sanity; (d) `git diff --check` silent; (e) report records the importer's remaining `dtype.`/`tensor.` site count as owned by VIS-D/VIS-T |
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
| `outcome` | `dtype.finite`, `dtype.name`, `dtype.from_name`, `dtype.cast`, `dtype.message` are `@ publica`; the `dtype.*` `import_module_private` sites are gone — static cross-module sites: 46 (finite 21, name 17, message 4, from_name 3, cast 1) across 12 consumer files (§2) |
| `primary files` | `src/dtype.fab` (1) |
| `write_scope` | `src/dtype.fab` — exactly 5 one-line `@ publica` insertions at :131, :144, :153, :272, :287 |
| `read_scope` | this delivery §3 table; `docs/api-reference.md` `## gradus:dtype` (names already documented) |
| `forbidden_scope` | any other annotation; edits to the existing `@ publica` blocks (:69–:95 tag factories / `discretio DType`) or to `discretio DTypeError`; `_`-helpers; any non-`src/dtype.fab` file; check-compile/package/stage gates; absorbing shape/tensor errors |
| `red` | before change: `faber check src/loss.fab` (or `src/metrics.fab`/`src/train.fab`) emits SEM006 referencing `dtype.` (e.g. `dtype.finite`, `dtype.name`). Record first divergence |
| `green` | `faber check src/dtype.fab` exit 0; `grep -n -B1 "functio \(finite\|name\|from_name\|cast\|message\)" src/dtype.fab` shows `@ publica` above all five; focused importer sanity: `faber check src/loss.fab` and `faber check src/train.fab` output contains **no** `SEM006` line referencing `dtype.`; `git diff --check` silent |
| `done_when` | (a) 5 `@ publica` lines present exactly at the §3 lines; (b) dtype.fab check exit 0; (c) zero `dtype.` SEM006 in the loss/train importer sanity; (d) `git diff --check` silent; (e) report records the importer's remaining `shape.`/`tensor.` site count as owned by VIS-S/VIS-T |
| `est_work_tokens` | 3–4k |
| `est_basis` | pilot; 5 one-line annotations + two narrow importer checks |
| `tool_latency` | low — three single-file `faber check` invocations + greps |
| `depends_on` | base `factory/merge` `1462cd8` |
| `parallel_with` | VIS-S, VIS-T |
| `integrable` | **yes** |
| `risk` | negligible |

### VIS-T — tensor module publica (4 symbols)

| Field | Value |
| --- | --- |
| `outcome` | `tensor.construct`, `tensor.construct_dtype`, `tensor.message`, `tensor.fill` are `@ publica`; the tensor-symbol `import_module_private` sites are gone — static cross-module sites: 16 (construct 5, construct_dtype 2, message 8, fill 1) across cache/decode/gradient/math/parameter/train/attention |
| `primary files` | `src/tensor.fab` (1) |
| `write_scope` | `src/tensor.fab` — exactly 4 one-line `@ publica` insertions at :210, :242, :250, :260; do **not** move or duplicate the existing `@ publica` at :132 (`genus Tensor`, VIS-05) |
| `read_scope` | this delivery §3 table; `docs/api-reference.md` `## gradus:tensor` (names incl. `fill` already documented); audit `654ab80b` P2-1 (the `fill` omission) |
| `forbidden_scope` | any other annotation; edits to `genus Tensor` (:132), `_numel_shape` (:229), or any other `_`-helper; any non-`src/tensor.fab` file; check-compile/package/stage gates; absorbing shape/dtype errors |
| `red` | before change: `faber check src/attention.fab` (sole `tensor.fill` consumer) emits `SEM006:import_module_private` referencing `tensor.fill` (`attention.fab:287`); `faber check src/train.fab` (or `src/cache.fab`) emits `tensor.` sites. Record first divergence |
| `green` | `faber check src/tensor.fab` exit 0; `grep -n -B1 "functio \(construct\|construct_dtype\|message\|fill\)" src/tensor.fab` shows `@ publica` above all four (note `construct` vs `construct_dtype` — assert both, plus `fill`); focused importer sanity: `faber check src/attention.fab` and `faber check src/train.fab` and `faber check src/cache.fab` output contains **no** `SEM006` line referencing `tensor.` (attention.fab's `_fill` private wrapper stays untouched); `git diff --check` silent |
| `done_when` | (a) 4 `@ publica` lines present exactly at the §3 lines; (b) tensor.fab check exit 0; (c) zero `tensor.` SEM006 in the attention/train/cache importer sanity (attention.fab is the fill-specific target; if the lane-local single-file check does not emit there, record that fact in the report rather than weakening the gate); (d) `git diff --check` silent; (e) report records the importer's remaining `shape.`/`dtype.` site count as owned by VIS-S/VIS-D |
| `est_work_tokens` | 3–4k |
| `est_basis` | pilot; 4 one-line annotations + three narrow importer checks |
| `tool_latency` | low — four single-file `faber check` invocations + greps |
| `depends_on` | base `factory/merge` `1462cd8` |
| `parallel_with` | VIS-S, VIS-D |
| `integrable` | **yes** |
| `risk` | negligible — `fill` is the same class as the other three (documented public, cross-module consumed); behavior identical |

## 7. Aggregate merge retry gate — G (A1C-M8R2 retry)

| Field | Value |
| --- | --- |
| `outcome` | the gate refused at `7ee11a87` (task `9058ef55`, A1C-M8R2) is re-run once the VIS units are on `factory/merge`, and its step-1 SEM006 blocker (the report-recorded 56 baseline, §2) is proven cleared for the 13-symbol set; the A1C candidate `7221555` becomes re-runnable through a green package check |
| `primary files` | none — validation + (if green) the A1C integration merge; no product/doc edits |
| `write_scope` | the A1C integration merge into `factory/merge` per the A1C micro-unit doc M8 (merge-lane operation); commit message names the merged VIS + A1C heads |
| `read_scope` | merged `factory/merge` (post VIS-S/D/T), the A1C candidate `7221555`, report `7ee11a87` evidence |
| `forbidden_scope` | any product code; re-running any unit's work; editing source to "fix" the check; absorbing the A1C chain's model/* surfaces; running before all three VIS units are merged |
| `red` (do not merge) | `./scripta/check-compile` still emits any `SEM006:import_module_private` referencing `shape.`/`dtype.`/`tensor.` symbols, or `git diff --check` is not silent → record the exact residual and stop; do not weaken the gate |
| `green` (run once) | authority setup (`FABER_BIN` = current-Faber binary from radix `b6d6e17c8`, `FABER_LIBRARY_HOME` = merge lane parent, script default): `./scripta/check-compile` exit 0 with **zero** `SEM006` on the merged gradus library source; `grep -c SEM006` == 0 vs the report-recorded 56 pre-fix baseline (§2 — composition uncertainty acknowledged, the symbol set is the verified target); `git diff --check` silent. Then the A1C chain's own M8 closeout (per its delivery doc) runs and the A1C integration lands |
| `done_when` | (a) the report-recorded 56-error baseline is reduced to 0 for the 13-symbol set under the authority setup on the merged main; (b) the candidate `7221555` rebased on the fixed main also yields 0 SEM006 for the set; (c) residual model/* visibility diagnostics, if any surface under the merged-tree setup, are recorded with their owning A1C unit (M1/M8) and routed — not absorbed; (d) merge lane re-queues A1C-M8R2 |
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
   baseline (the `dtype.DType`/`artifact.ContentIdentity`/`capsule.Capsule` errors are
   gone; the library portion of the report-recorded 56 SEM006 is the 13 shape/dtype/tensor
   functions lowered here — 73 static cross-module sites, §2/§3 — while the model/* rows
   are the A1C chain's own surface, §10); the §7 ordering conclusion (visibility before
   M1) is unchanged.
3. G re-runs A1C-M8R2 once the A1C integration branch is assembled on the fixed main.
4. If a VIS unit is not landed when M1 is dispatched, M1 waits; M1 must not "help" by adding
   annotations (per the A1C delivery doc).

## 9. Red oracle (review fail conditions)

This lowering must fail review if any child:

- exceeds 8k `est_work_tokens` or touches more than its one primary file;
- adds any annotation beyond the §3 declaration list, or removes/weakens any `@ privata`
  helper (`_product`, `_dimension`, `_numel_shape`, `attention.fab` `_fill`, any
  `_`-prefixed name);
- omits `tensor.fill` (`tensor.fab:260`) from VIS-T or restates the declaration set
  with fewer than 13 symbols (the "no missing member of this diagnostic class" claim is a
  hard criterion — audit `654ab80b` P2-1);
- runs a broad package/`check-compile`/`inventory-public-symbols` gate (only G may);
- edits docs, `.proba`, `scripta/`, `tests/`, or `model/*` (each unit's forbidden scope);
- claims green while the importer sanity still emits the unit's own symbols (i.e. weakens
  the focused check to "exit 0 on the module alone");
- is dispatched to touch `tensor.fab:132` (`genus Tensor` publica) — that is already landed
  (VIS-05) and must be preserved untouched by VIS-T.

## 10. Named residuals and routes (out of scope, not gaps)

- **model/* visibility surfaces** (candidate `model/capsule.fab` referencing
  `manifestum.GgufManifest`; main `model/gguf.fab`/`model/safetensors.fab` referencing
  `capsula.construct`/`capsula.message`): these are the A1C chain's own rewritten files and its
  M1/M8 surface; not part of the correction's 13-symbol set and not absorbed. Report
  `7ee11a87` records `model/gguf` 2 + `model/safetensors` 2 within its 56 total; a live
  authority-setup reproduction measured none (module-resolution sensitivity, §2). The
  composition is unresolved — routed to the A1C chain M1/M8; gate G records whatever
  surfaces appear under the merged-tree setup and routes them the same way.
- **`inventory-public-symbols` baseline** (total 618): unchanged by this correction
  (verified §4) — no re-baseline unit needed; the A1C chain's M6 re-baseline absorbs any
  future A1C count changes.
- **A1C micro-unit doc §7 premise**: stale "27-error" description is superseded by this
  doc; that doc lives on `factory/planner-39` and is not in this lane — no edit here.
