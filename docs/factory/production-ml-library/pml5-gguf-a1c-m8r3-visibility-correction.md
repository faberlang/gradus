# Delivery Lowering — A1C-M8R3 Correction: Cross-Module `@ publica` Closure for the Remaining Pre-Existing SEM006 Surface (math/parameter/gradient/train + cascade) + Candidate-Refresh / M8R4 Aggregate Gate

**Planner**: planner-40. **Assignment**: task `6e4092f0` (Mind, 2026-08-13T21:49:15+00:00) —
"lower A1C M8R3 math visibility correction".
**Failure receipt**: merge task `c3ed38a6`; refusal report `88009081`; candidate `93b33d0`
(`93b33d05f385aebd55f76a9d939a6a47e8c90bd8`, `factory/a1c-chain`); baseline/main `61aac27`
(`61aac27d1b3c1c66882480ccea3b6d57f3a369fe`).
**Predecessor correction**: planner-38 delivery
[`pml5-gguf-a1c-visibility-correction.md`](../../../../../planner-38/gradus/docs/factory/production-ml-library/pml5-gguf-a1c-visibility-correction.md)
(revision `b386f3f`, admitted by audit report `953afcd3`), whose VIS-S/D/T units
(shape/dtype/tensor) landed as hand-16/17/18 (`5d388f4`/`eefa5f2`/`bb76992`) and are
ancestors of the candidate. The M8R3 refusal shows that correction cleared its own
13-symbol surface but a *broader* pre-existing surface remains — the subject of this
delivery.
**Campaign**: [`radix/docs/factory/gpu-production-readiness/CAMPAIGN.md`](../../../../radix/docs/factory/gpu-production-readiness/CAMPAIGN.md)
(row `LIB-01` / GGUF-A1c).
**Delivery authority**: [`pml5-general-gguf-delivery.md`](pml5-general-gguf-delivery.md) §GGUF-A1c;
A1C micro-unit doc [`pml5-gguf-a1c-micro-units.md`](../../../../../planner-39/gradus/docs/factory/production-ml-library/pml5-gguf-a1c-micro-units.md)
unit M8.
**Repo baselines**: Gradus main/factory-merge `61aac27`; candidate `93b33d0` (A1C chain on
`factory/a1c-chain`); Radix `b6d6e17c8` (lane-local faber 1.6.0); planner-40 lane clean at those tips.

## 1. Goal-check verdict (compact)

- **Goal path**: campaign mandatory row `LIB-01` → GGUF-A1c (mandatory enabling work for
  the A1C M8 aggregate gate through CLOSE-01).
- **Evaluator mode**: goal-check + delivery lowering of the M8R3 correction per task
  `6e4092f0` (reproduce the usage-driven closure; re-lower into one-logical-change units
  by declaration module; add one aggregate candidate-refresh + M8R4 gate owned by merge).
- **Intended consumer**: delivery (Mind dispatches the visibility Hands, then re-runs
  A1C-M8R4 via merge).
- **Verdict**: **READY**.
- **Reasoning**: report `88009081` is accurate about *what* failed (21 SEM006 at
  check-compile step 1 on candidate `93b33d0`, library files byte-identical to baseline,
  baseline reproduces the same set) but **incomplete about the root cause and scope**.
  The 21 SEM006 (17 distinct merged-line sites) are **not** all `math.*`: 7 sites are
  `math.*` (attention 4, nn 3), 5 are `parametrum.*`/`gradient.*` (optimize 5), 5 are
  `train.*` (sampling 5). The provider surface is therefore four modules (math,
  parameter, gradient, train) — not one. And the M8 gate runs `./scripta/check-compile`,
  which checks the *whole package plus all exempla*; the compiler stops at the first
  failing module wave, so the 21 reported SEM006 are only the first wave of a cascade.
  This delivery reproduces the **complete** normalized failure set under the authority
  setup, proves the exact annotation closure that makes `check-compile` green (96 `@
  publica` lines across 15 gradus modules, verified on a scratch copy of the candidate),
  and sizes one Hand unit per declaration module (the planner-38 VIS-S/D/T pattern).
  One cross-repo residual remains: the `gguf-inspect` exempla (part of `check-compile`)
  imports `norma:processus`/`norma:solum`, whose consumed symbols are also
  module-private post-flip (§10).
- **Blocking gaps**: none inside the gradus scope named below; the `norma:*` cross-repo
  dependency is a named residual with a route (§10, open question Q1).

## 2. Evidence — reproduction, the 21-SEM006 decomposition, and the complete gate closure

**Setup** (matches the M8R3 authority and the planner-38 precedent): faber binary 1.6.0
built from radix `b6d6e17c8` (`worktrees/merge/radix/target/debug/faber`);
`FABER_LIBRARY_HOME` = lane parent (script default); `./scripta/check-compile` from the
gradus checkout under test.

**Candidate reproduction (this lane, candidate `93b33d0` via the merge-lane checkout)**:
`./scripta/check-compile` exit 1; **21 SEM006** (`import_module_private`) + 14 cascading
SEM010 at the same sites. Deduplicated to **17 distinct (file, merged-line) sites**:

| File | Sites | Referenced provider symbols |
| --- | --- | --- |
| `src/attention.fab` | 4 | `math.matmul` ×2, `math.mul`, `math.causa` |
| `src/nn.fab` | 3 | `math.matmul`, `math.add`, `math.causa` |
| `src/optimize.fab` | 5 | `parametrum.Parametrum` ×4, `gradient.Gradiente` |
| `src/sampling.fab` | 5 | `train.Semen` ×4, `train.FructusF32` + `train.proximus_f32` |

**Provenance**: the four files are byte-identical between baseline `61aac27` and
candidate `93b33d0` (report `88009081`; re-verified). A fresh reproduction on the
planner-40 lane at `61aac27` yields the identical 21-SEM006 set. This is pre-existing
post-flip enabling work, not A1C regression — same class as the planner-38 13-symbol
surface, which the VIS-S/D/T repairs cleared.

**Root-cause correction vs report `88009081`**: the report states "src/math.fab carries
zero @ publica annotations; matmul/mul/causa/… are module-private". That is only true for
7 of the 17 distinct sites. The remaining 10 sites reference `parameter.Parametrum`,
`gradient.Gradiente`, `train.Semen`, `train.FructusF32`, `train.proximus_f32` — four
provider modules, not one. A math.fab-only repair would leave 10 SEM006 (optimize +
sampling) and the gate still red.

**Cascade (why the 21 is not the whole gate surface)**: `faber check "$ROOT"` compiles
the package module graph and reports per import site; modules whose dependencies fail are
skipped, so the reported set is the *first wave*. The A1C M8 closeout requires
`./scripta/check-compile` to exit 0 **including all exempla** (`gradient-seam`,
`training-loop-mlp`, `token-generation`, `gguf-manifest`, `gguf-inspect`). On a scratch
copy of the candidate, this delivery applied the exact usage-driven closure of
cross-module-consumed non-underscore symbols (§3) and re-ran the full gate:

- `faber check` on the gradus library: **exit 0, zero SEM006**.
- `./scripta/check-compile`: library + `gradient-seam` + `training-loop-mlp` +
  `token-generation` + `gguf-manifest` **exit 0, zero errors**; `gguf-inspect` exit 1 with
  3 SEM006 on `norma:processus.argumenta` / `norma:solum.mensura` / `norma:solum.partem`
  (§10 — cross-repo).
- `faber check --diagnostics .`: `ok:`.
- `./scripta/inventory-public-symbols`: exit 0, total 582 unchanged (annotation lines add
  no `functio` count and every non-underscore name is already documented — zero ripple).
- `./scripta/check-source`: exit 0.

The closure therefore makes the gradus-side of the M8 gate green; the sole remaining
gate failure is the `norma:*` dependency inside the `gguf-inspect` exempla (§10).

## 3. Usage-driven declaration set — 96 `@ publica` annotations across 15 gradus modules

Verified statically on candidate `93b33d0` (baseline public set subtracted): every symbol
below is consumed cross-module by a gradus library or exempla file, carries **no**
`@ publica` on the baseline/candidate, and is **not** `_`-prefixed (all `_`-helpers stay
private). `@ publica` is inserted as a one-line annotation immediately above the
top-level declaration (column 0), per the VIS-04/VIS-05/VIS-S/D/T convention. Line
numbers are from candidate `93b33d0` (all non-model files identical to `61aac27`;
`model/gguf_manifest.fab` differs only by the A1C-chain publica already landed — the 6
annotations below are the ones still missing).

### V-MATH — `src/math.fab` (4)

| Line | Declaration |
| --- | --- |
| 92 | `functio causa(MathError e) → textus {` |
| 297 | `functio add(tensor.Tensor a, tensor.Tensor b) → tensor.Tensor ⇥ MathError {` |
| 331 | `functio mul(tensor.Tensor a, tensor.Tensor b) → tensor.Tensor ⇥ MathError {` |
| 486 | `functio matmul(tensor.Tensor a, tensor.Tensor b) → tensor.Tensor ⇥ MathError {` |

Consumers: attention.fab, nn.fab, transformer.fab. These four clear the 7 `math.*` sites
of the exact 21.

### V-PARAM — `src/parameter.fab` (5)

| Line | Declaration |
| --- | --- |
| 113 | `functio causa(ParametrumError e) → textus {` |
| 182 | `genus Parametrum {` |
| 255 | `functio est_gelida(Parametrum p) → bivalens {` |
| 304 | `functio structa(textus nomen, textus possessor, textus typo_nomen, lista<numerus> forma, lista<f32> datos) → Parametrum ⇥ ParametrumError {` |
| 320 | `functio muta(Parametrum p, lista<f32> datos) → Parametrum ⇥ ParametrumError {` |

Consumers: optimize.fab, exempla/training-loop-mlp.

### V-GRAD — `src/gradient.fab` (5)

| Line | Declaration |
| --- | --- |
| 94 | `genus Gradiente {` |
| 124 | `functio structa(textus nomen, textus possessor, numerus versio, tensor.Tensor valor) → Gradiente ⇥ GradienteError {` |
| 173 | `functio obsoletus(Gradiente g, numerus versio_currens) → bivalens {` |
| 183 | `functio nil() → vacuum {` |
| 195 | `functio simple_loss(tensor<f32, [2,2]> x, tensor<f32, [2,2]> w) → f32 {` |

Consumers: optimize.fab, exempla/gradient-seam, exempla/training-loop-mlp. (The
compiler-generated companions `loss_backward` / `forward_mlp_loss_backward` inherit the
annotated source function's visibility — verified: both exempla compile green with only
these annotations.)

### V-TRAIN — `src/train.fab` (13)

| Line | Declaration |
| --- | --- |
| 293 | `functio causa(TrainError e) → textus {` |
| 319 | `genus Schedula {` |
| 346 | `functio structa_schedula(textus nomen, numerus aetas, lista<f32> rates) → Schedula ⇥ TrainError {` |
| 386 | `functio lentus_schedulata(Schedula s, numerus passus) → f32 ⇥ TrainError {` |
| 539 | `genus Semen {` |
| 549 | `functio structa_semen(numerus semen) → Semen ⇥ TrainError {` |
| 591 | `genus FructusF32 {` |
| 606 | `functio proximus_f32(Semen s) → FructusF32 {` |
| 708 | `genus Tabula {` |
| 737 | `functio structa_tabula(numerus aetas, numerus passus, Semen rng, textus statum_wire) → Tabula ⇥ TrainError {` |
| 751 | `functio tabula_aequus(Tabula a, Tabula b) → bivalens {` |
| 765 | `functio serializa_tabula(Tabula c) → textus {` |
| 788 | `functio deserializa_tabula(textus wire) → Tabula ⇥ TrainError {` |

Consumers: sampling.fab, decode.fab, generation.fab, exempla/training-loop-mlp,
exempla/token-generation.

### V-NN — `src/nn.fab` (4)

| Line | Declaration |
| --- | --- |
| 174 | `functio causa(NnError e) → textus {` |
| 297 | `functio linear(tensor.Tensor x, tensor.Tensor w, tensor.Tensor b) → tensor.Tensor ⇥ NnError {` |
| 366 | `functio gelu(tensor.Tensor x) → tensor.Tensor ⇥ NnError {` |
| 385 | `functio layernorm(tensor.Tensor x, tensor.Tensor scale, tensor.Tensor offset, f32 epsilon) → tensor.Tensor ⇥ NnError {` |

Consumers: transformer.fab, gradus.fab, decode.fab, exempla/training-loop-mlp,
exempla/token-generation.

### V-ATTN — `src/attention.fab` (4)

| Line | Declaration |
| --- | --- |
| 153 | `functio causa(AttentionError e) → textus {` |
| 519 | `functio scaled_dot_product(tensor.Tensor q, tensor.Tensor k, tensor.Tensor v, f32 scale) → tensor.Tensor ⇥ AttentionError {` |
| 531 | `functio scaled_dot_product_causal(tensor.Tensor q, tensor.Tensor k, tensor.Tensor v, f32 scale) → tensor.Tensor ⇥ AttentionError {` |
| 543 | `functio scaled_dot_product_causal_rope(tensor.Tensor q, tensor.Tensor k, tensor.Tensor v, f32 scale, lista<numerus> positions, numerus dim) → tensor.Tensor ⇥ AttentionError {` |

Consumer: transformer.fab.

### V-SAMP — `src/sampling.fab` (7)

| Line | Declaration |
| --- | --- |
| 67 | `discretio SamplingError {` |
| 73 | `functio causa(SamplingError e) → textus {` |
| 86 | `genus Configura {` |
| 122 | `functio structa_configura(` |
| 157 | `genus Sortitio {` |
| 177 | `functio maxima(lista<f32> logits) → numerus ⇥ SamplingError {` |
| 229 | `functio sors(lista<f32> logits, Configura c, lista<numerus> historia, train.Semen semen) → Sortitio ⇥ SamplingError {` |

Consumers: decode.fab, generation.fab, exempla/token-generation.

### V-DEC — `src/decode.fab` (13)

| Line | Declaration |
| --- | --- |
| 103 | `discretio DecodeError {` |
| 117 | `functio causa(DecodeError e) → textus {` |
| 142 | `genus Pondera {` |
| 184 | `functio structa_pondera(` |
| 213 | `genus Decodere {` |
| 264 | `functio structa_decodere(` |
| 415 | `functio decodere_datum(` |
| 470 | `genus Sessio {` |
| 486 | `functio sessio_fresh(` |
| 503 | `functio redintegra(` |
| 516 | `genus Cancelatum {` |
| 526 | `functio cancelatum_fresh(` |
| 538 | `functio observa_cancellationem(` |

Consumers: generation.fab, exempla/token-generation.

### V-GEN — `src/generation.fab` (9)

| Line | Declaration |
| --- | --- |
| 88 | `discretio GeneratioError {` |
| 117 | `genus GeneratioConfigura {` |
| 193 | `functio structa_generatio(` |
| 284 | `functio configura(GeneratioConfigura g) → sampling.Configura ⇥ GeneratioError {` |
| 297 | `functio semen(GeneratioConfigura g) → train.Semen ⇥ GeneratioError {` |
| 454 | `genus GenereCursor {` |
| 470 | `functio cursor_fresh(` |
| 485 | `functio verbum_licet(` |
| 494 | `functio cursor_progredere(` |

Consumer: exempla/token-generation.

### V-OPT — `src/optimize.fab` (13)

| Line | Declaration |
| --- | --- |
| 189 | `genus SgdStatum {` |
| 230 | `functio statum_aequus(SgdStatum a, SgdStatum b) → bivalens {` |
| 258 | `functio structa(textus nomen, textus possessor, numerus generatio, f32 lentus) → SgdStatum ⇥ OptimizeError {` |
| 267 | `genus Sgd {` |
| 294 | `functio sgd_aequus(Sgd a, Sgd b) → bivalens {` |
| 309 | `functio sgd_vacuum() → Sgd {` |
| 314 | `functio adscisco(Sgd o, SgdStatum s) → Sgd ⇥ OptimizeError {` |
| 328 | `genus Passus {` |
| 350 | `functio passus(SgdStatum s, parametrum.Parametrum p, gradient.Gradiente g) → Passus ⇥ OptimizeError {` |
| 398 | `functio serializa_statum(SgdStatum s) → textus {` |
| 403 | `functio deserializa_statum(textus wire) → SgdStatum ⇥ OptimizeError {` |
| 465 | `functio serializa(Sgd o) → textus {` |
| 473 | `functio deserializa(textus wire) → Sgd ⇥ OptimizeError {` |

Consumer: exempla/training-loop-mlp.

### V-GRADUS — `src/gradus.fab` (5)

| Line | Declaration |
| --- | --- |
| 89 | `discretio GradusError {` |
| 100 | `functio causa(GradusError e) → textus {` |
| 174 | `functio forward_mlp(` |
| 186 | `functio nil() → vacuum {` |
| 205 | `functio forward_mlp_loss(` |

Consumer: exempla/training-loop-mlp. (`forward_mlp_loss_backward` is compiler-generated
from the annotated `forward_mlp_loss`; verified green in the exempla with only these
annotations.)

### V-METRICS — `src/metrics.fab` (4)

| Line | Declaration |
| --- | --- |
| 64 | `functio causa(MetricError e) → textus {` |
| 85 | `functio accuratezza(tensor.Tensor prediction, tensor.Tensor target) → f32 ⇥ MetricError {` |
| 155 | `genus Metricum {` |
| 172 | `functio metricum(` |

Consumer: exempla/training-loop-mlp.

### V-TOK — `src/tokenizer.fab` (1)

| Line | Declaration |
| --- | --- |
| 109 | `functio est_eog(numerus id) → bivalens {` |

Consumer: exempla/token-generation.

### V-TRANS — `src/transformer.fab` (3)

| Line | Declaration |
| --- | --- |
| 164 | `discretio TransformerError {` |
| 179 | `functio causa(TransformerError e) → textus {` |
| 334 | `functio transformer_block(` |

Consumer: decode.fab.

### V-GGUFM — `src/model/gguf_manifest.fab` (6)

| Line | Declaration |
| --- | --- |
| 96 | `genus CorpusGguf {` |
| 119 | `discretio LayoutGgml {` |
| 124 | `genus DescriptioTensorisGguf {` |
| 691 | `functio inveni_tensorem(ManifestumGguf m, textus nomen) → DescriptioTensorisGguf ⇥ GgufManifestError {` |
| 784 | `functio parse(CorpusGguf corpus) → ManifestumGguf ⇥ GgufManifestError {` |
| 1071 | `functio lege_fragmentum(` |

Consumers: exempla/gguf-manifest, exempla/gguf-inspect. (The A1C chain already landed
`@ publica` on `GgufManifestError`, `LectioFontis`, `MetadatumGguf`, `ManifestumGguf`,
`causa`, `metadatum`, `textum`, `numerum`, `inspice` — those stay; these six are the
remaining consumers' symbols.)

## 4. Non-goals, preserved privacy, ripple

- **Preserved `@ privata` / `_`-prefixed helpers (no blanket sweep)**: every `_`-prefixed
  function in the 15 modules stays private (e.g. `math._forma_broadcast`,
  `_quantitas_valid`, `_index_broadcast`, `_index_axis`, `_coordinata`, `_planus_axis`,
  `_typo_par`, `_typus_ex_nomine`; `train`/`nn`/`attention`/`sampling`/`decode`/
  `generation`/`optimize`/`gguf_manifest` `_*` helpers). Only the 96 top-level names in
  §3 are annotated.
- **No other files edited** by the 15 units: no `.proba`, no `docs/`, no `scripta/`, no
  `tests/`, no other repo. Each unit edits exactly its one `src/*.fab`.
- **Zero inventory/doc ripple (verified)**: `scripta/inventory-public-symbols` counts
  `functio ` declaration lines — annotation lines change no count (total 582 on both
  baseline and the annotated scratch); its coverage gate requires every non-`_` name to
  appear in `docs/api-reference.md`, and all 96 names are already documented (spot-verified
  on baseline for representative names across all 15 modules). No M5/M6-style follow-up.
- **No semantic change**: `@ publica` on an already cross-module-consumed declaration
  changes visibility only; module-private semantics are preserved for everything not
  annotated.
- **A1C chain serialization preserved**: this correction merges to gradus
  `factory/merge` **before** the A1C M1 dispatch continues (planner-39 doc §7 ordering);
  A1C units do **not** add annotations themselves. The candidate `93b33d0` is re-runnable
  as-is once these repairs land (§7).

## 5. Unit graph

```
factory/merge (61aac27)
  ├─ V-MATH    math.fab        @ publica ×4   (∥ all)
  ├─ V-PARAM   parameter.fab   @ publica ×5
  ├─ V-GRAD    gradient.fab    @ publica ×5
  ├─ V-TRAIN   train.fab       @ publica ×13
  ├─ V-NN      nn.fab          @ publica ×4
  ├─ V-ATTN    attention.fab   @ publica ×4
  ├─ V-SAMP    sampling.fab    @ publica ×7
  ├─ V-DEC     decode.fab      @ publica ×13
  ├─ V-GEN     generation.fab  @ publica ×9
  ├─ V-OPT     optimize.fab    @ publica ×13
  ├─ V-GRADUS  gradus.fab      @ publica ×5
  ├─ V-METRICS metrics.fab     @ publica ×4
  ├─ V-TOK     tokenizer.fab   @ publica ×1
  ├─ V-TRANS   transformer.fab @ publica ×3
  └─ V-GGUFM   model/gguf_manifest.fab @ publica ×6
        │  (each merges to factory/merge individually — additive annotation, cannot break)
        ▼
factory/merge SEM006-green on the 96-symbol closure
        │
        ▼
G  candidate-refresh + A1C-M8R4 aggregate gate (merge-owned; §7)
```

- **Maximum safe parallelism**: 15 — every unit touches a disjoint primary file; no
  ordering among them.
- **Integration**: each unit merges to `factory/merge` alone on its own
  `factory/<lane>` branch; commit message `fix(gradus): expose <module> <symbols> to
  package consumers` (VIS-04/05/hand-16/17/18 precedent). No dual-authority or
  intermediate-broken state is possible (adding `@ publica` cannot break a module).
- **Branch protocol**: `factory/<lane>` off `factory/merge`; `non-integrable` marker
  **not** required (each is individually integrable). Gate G must not run until all 15
  are on `factory/merge` **and** the `norma:*` residual (Q1) is resolved.

## 6. Unit specs

Each unit shares the same shape (one module, N one-line annotations, one narrow importer
sanity); per-unit fields are the §3 table plus the following. The "focused importer
sanity" is the **first** consumer that previously emitted SEM006 for the unit's symbols;
it must show **zero** SEM006 referencing the unit's symbols (other units' symbols may
still appear — record and route, do not fix).

| Field | Value (all units) |
| --- | --- |
| `outcome` | the §3 symbols of the unit's module are `@ publica`; the unit's consumer SEM006 sites are gone |
| `primary files` | the one `src/*.fab` named in §5 |
| `write_scope` | that one file — exactly the N `@ publica` insertions at the §3 lines |
| `read_scope` | this delivery §3 table; `docs/api-reference.md` section for the module (names already documented — do not touch) |
| `forbidden_scope` | any other annotation; edits to `_`-helpers or any existing `@ publica` block; `.proba`/`docs/`/`scripta/`/`tests/`/other files; package/`check-compile`/stage gates (none on Hands); absorbing other units' errors |
| `red` | before change (authority setup, lane-local `FABER_BIN`/`FABER_LIBRARY_HOME`): `faber check <first consumer>` emits SEM006 referencing the unit's symbols. Record the first divergence |
| `green` | `faber check src/<module>.fab` exit 0; `grep -n -B1` shows `@ publica` immediately above every §3 declaration; focused importer sanity: the consumer's output contains **no** SEM006 line referencing the unit's symbols; `git diff --check` silent |
| `done_when` | (a) N `@ publica` lines at the §3 lines; (b) module check exit 0; (c) zero SEM006 for the unit's symbols in the focused importer sanity; (d) `git diff --check` silent; (e) report records the importer's remaining other-unit SEM006 count as routed, not fixed |
| `est_work_tokens` | 2–4k (N ≤ 13 one-line annotations + 1–2 narrow checks; VIS-S/D/T scale) |
| `est_basis` | pilot; annotation-only, VIS-04/05/hand-16/17/18 scale |
| `tool_latency` | low — two single-file `faber check` invocations + greps |
| `depends_on` | base `factory/merge` `61aac27` |
| `parallel_with` | the other 14 units |
| `integrable` | **yes** (additive annotation; merges to `factory/merge` alone) |
| `risk` | negligible — behavior identical; all 96 names already documented |

Per-unit importer sanity targets (first consumer that emitted for that unit's symbols):
V-MATH → `faber check src/attention.fab` and `src/nn.fab`; V-PARAM/V-GRAD →
`src/optimize.fab`; V-TRAIN → `src/sampling.fab`; V-NN → `src/transformer.fab`;
V-ATTN → `src/transformer.fab`; V-SAMP → `src/decode.fab`; V-DEC → `src/generation.fab`;
V-GEN → `exempla/token-generation`; V-OPT/V-GRADUS/V-METRICS → `exempla/training-loop-mlp`;
V-TOK → `exempla/token-generation`; V-TRANS → `src/decode.fab`; V-GGUFM →
`exempla/gguf-manifest`.

## 7. Aggregate gate — G (candidate-refresh + A1C-M8R4, merge-owned)

| Field | Value |
| --- | --- |
| `outcome` | the M8 gate refused at report `88009081` (task `c3ed38a6`, A1C-M8R3) is re-run once the 15 units are on gradus `factory/merge` and the `norma:*` residual (Q1) is resolved; the refreshed candidate is proven green and the A1C chain lands |
| `primary files` | none — validation + candidate-refresh + merge; no product/doc edits |
| `write_scope` | the merge lane: refresh `factory/a1c-chain` onto the corrected `factory/merge`, run the M8 closeout once, then the A1C integration merge per the A1C micro-unit doc M8 (commit message names the merged VIS + A1C heads) |
| `read_scope` | merged `factory/merge` (post all 15 units), the A1C candidate, report `88009081` evidence |
| `forbidden_scope` | any product code; re-running any unit's work; editing source to "fix" the check; absorbing the `norma:*` repair into gradus; running before all 15 units are merged; `hand-23`/`hand-26` |
| `red` (do not merge) | `./scripta/check-compile` still emits any SEM006 on gradus library or gradus exempla, or `git diff --check` not silent → record the exact residual and stop; do not weaken the gate |
| `green` (run once) | authority setup (`FABER_BIN` = lane-local faber 1.6.0 from radix `b6d6e17c8`, `FABER_LIBRARY_HOME` = lane parent): `./scripta/check-source` exit 0; `./scripta/check-compile` exit 0 (library + all gradus exempla); `faber check --diagnostics .` ends `ok: .`; the A1C clean-break greps per the A1C micro-unit doc M8 (`capsula.structa(` in src/tests empty; `capsule-schema-1.0.0` absent from live surfaces; `schema_versio` = `"2.0.0"`); `./scripta/inventory-public-symbols` exit 0 (total 582); `git diff --check` silent. Then merge the A1C integration branch atomically to `factory/merge` and fast-forward main per the merge recipe |
| `done_when` | (a) the 21-SEM006 first-wave set is 0 under the authority setup on the refreshed candidate; (b) the complete gradus closure (§3) yields zero SEM006 on library + gradus exempla; (c) residual `norma:*` diagnostics are either fixed on the norma side or explicitly routed (Q1); (d) A1C candidate refreshed on corrected main yields green M8 closeout; (e) merge lane re-queues A1C-M8R4 after the candidate refresh |
| `est_work_tokens` | 3–5k |
| `est_basis` | pilot; one aggregate validation pass + merge (matches A1C-M8 scale) |
| `tool_latency` | medium — the only package-level compiles in this delivery |
| `depends_on` | all 15 units on `factory/merge`; Q1 resolved |
| `parallel_with` | none — last |
| `integrable` | the gate itself is the A1C integration; the A1C chain's M8 remains the sole atomic A1C merge per its delivery doc |

## 8. Serialization vs the A1C chain (mandatory)

1. V-MATH … V-GGUFM (15 units) land on gradus `factory/merge` in any order (all 15
   before G runs).
2. `norma:*` residual (Q1) resolved on the norma side (separate repo/lane) before G, so
   the `gguf-inspect` exempla compiles.
3. G refreshes `factory/a1c-chain` onto the corrected `factory/merge` and re-runs
   A1C-M8R4; on green, the A1C integration lands atomically (per `pml5-gguf-a1c-micro-units.md`
   M8).
4. A1C M1 must not start until the visibility surface is green; A1C units never add
   annotations themselves (planner-39 doc §7).

## 9. Red oracle (review fail conditions)

This delivery must fail review if any child:

- exceeds 4k `est_work_tokens` or touches more than its one primary file;
- adds any annotation beyond the §3 declaration list, or removes/weakens any `_`-helper;
- omits any §3 symbol for its module (the "no missing member of the diagnostic class"
  claim is a hard criterion — the 96-symbol closure is the verified gate surface);
- runs a broad package/`check-compile`/`inventory-public-symbols` gate (only G may);
- edits docs, `.proba`, `scripta/`, `tests/`, or another repo (each unit's forbidden
  scope);
- claims green while the focused importer sanity still emits the unit's own symbols;
- is dispatched to touch `model/capsule.fab`, `model/gguf.fab`, or `model/safetensors.fab`
  (the A1C chain's own rewritten files — their surfaces are A1C-owned, and the candidate
  has no SEM006 there).

## 10. Named residuals and routes (out of gradus scope, not gaps)

- **`norma:*` visibility** (blocks G at the `gguf-inspect` exempla): the exempla imports
  `norma:processus` (`processus.argumenta`, line 170, no `@ publica`) and `norma:solum`
  (`solum.mensura` line 206, `solum.partem` line 83, no `@ publica`). Post-flip these are
  module-private, so `./scripta/check-compile` fails at the `gguf-inspect` stage even
  with the full gradus closure. This is the same pre-existing post-flip class, but in the
  **norma** repo. **Default route**: a parallel norma-side visibility repair mirroring
  this delivery's shape (three `@ publica` annotations), owned by its own lane, merged
  before G; or Mind re-scopes the `gguf-inspect` exempla check. Gradus must **not** absorb
  it (AGENTS.md: gradus imports no sibling library surface).
- **Planner-38's model/* routing**: unchanged. `model/capsule.fab`, `model/gguf.fab`,
  `model/safetensors.fab` are the A1C chain's own rewritten files; the candidate shows no
  SEM006 there (verified on `93b33d0`), so nothing is routed to them from this delivery.
- **`inventory-public-symbols` baseline** (total 582): unchanged (§4) — no re-baseline
  unit needed.

## 11. Open questions for Mind

- **Q1 (blocking for G, not for the 15 units)**: the `gguf-inspect` exempla needs
  `norma:processus.argumenta`, `norma:solum.mensura`, `norma:solum.partem` `@ publica`.
  Default: route a parallel norma visibility repair (three one-line annotations, same
  class as this delivery) on the norma lane, merged before G; alternative: Mind re-scopes
  the `gguf-inspect` exempla check for M8R4.
- None blocking for the 15 gradus units: dispatch order is free, each is integrable alone,
  and the first eligible frontier is **all 15 units immediately** (base
  `factory/merge` `61aac27`), with G last.

## 12. Honesty gate

This lowering corrects the M8R3 report's root cause (four provider modules, not math.fab
alone; a cascade closure, not the first wave) and lowers the verified complete gradus
closure. It does not fix the `norma:*` cross-repo dependency (that is norma's lane, Q1).
It does not claim the A1C chain is complete: G re-runs the refused M8R4 gate; LIB-01
completion still requires the A1C M8 closeout and the campaign's full LIB/REF/MODEL/EXEC/CAP
chain through CLOSE-01. Chain completion is not campaign completion.
