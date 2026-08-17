# Delivery Lowering — Gradus tree-wide SEM006 import-seam migration: per-module publica units (need 8e70a5b2)

**Planner**: planner-33. **Assignment**: task `ab897911` (Mind, 2026-08-14) —
"lower SEM006 migration wave: gradus tree-wide privata->publica (NOT YET LOWERED)".
**Need**: `8e70a5b2` — "gradus tree-wide SEM006 migration incomplete — faber test
blocked at baseline (~675)" (LIB-02-U1 residual 2, hand-16 report; recheck after
LIB-02/LIB-03 chains land).
**Campaign**: [`radix/docs/factory/gpu-production-readiness/CAMPAIGN.md`](../../../../radix/docs/factory/gpu-production-readiness/CAMPAIGN.md)
(single-priority goal `gol_634a0417d02c510f`; mandatory work rows LIB-02/LIB-03 and
their proba executed-value evidence are gated on the SEM006-clean baseline).
**Pattern authority**: A1C publica closure on main — VIS-S/D/T (hand-10..hand-32,
`61aac27`/`93b33d0`), the M6-U1 repair `5445111`, Q1 norma `b73a206`, and the
planner-38 correction `d678547`/`b386f3f`.
**Repo baselines (measured)**: Gradus main `698d12f`; the packet gradus member
`worktrees/planner-33/gradus` was found **stale** at `1462cd8` (pre-A1C) and was not
used as the measurement surface — see §9. All measurements below are against current
local main `698d12f` (read-only), except the scratch end-state proof (§4).

## 1. Goal-check summary (compact)

- **Goal path**: campaign mandatory work `LIB-01` → `LIB-02`/`LIB-03`; the SEM006-clean
  baseline is the precondition for the campaign's proba executed-value evidence.
- **Evaluator mode**: goal-check + delivery lowering of the tree-wide SEM006 migration.
- **Intended consumer**: delivery (Mind dispatches Hands; merge lane integrates; test
  lane owns `faber test`).
- **Verdict**: **READY**.
- **Reasoning**: current main `698d12f` has exactly **357** `SEM006:import_module_private`
  diagnostics (reproduced under the authority setup below), all cross-module references
  to unmarked top-level declarations in 18 modules; `faber check .` (package mode) is
  already exit 0, so the entire remaining SEM006 surface lives in the proba/tests
  consumers. Every site maps to an enumerable per-module annotation set (129 annotations
  across 23 module files, inventoried §4). A scratch-copy proof (§4) applying the full
  inventory drives `faber test .` semantic errors to **zero**. Each module family is one
  additive, individually-integrable unit; all 23 units are mutually parallel.
- **Blocking gaps**: none. Residuals routed out: (a) after the migration, `faber test .`
  still cannot execute proba bodies (`unsupported MIR lowering: method call before
  runtime/provider MIR lowering`) — that is the separate FMIR-lever gate named in the
  need, not this wave; (b) the packet gradus member is stale vs local main (§9) — Mind
  should refresh `planner-33` before dispatch.

## 2. Reproduction evidence (authority setup, measured on main `698d12f`)

Setup: current-Faber binary built from the planner-33 packet radix member
(`worktrees/planner-33/radix/target/debug/faber`, faber 1.6.0);
`FABER_LIBRARY_HOME=/Users/ianzepp/work/faberlang` (the check-compile default for the
main checkout); `FABER_BIN` exported explicitly. Commands: `faber test .`,
`faber check .`, `faber check <file>` per source/proba file, `faber check <exemplum>`.

| Surface | Baseline on main `698d12f` |
| --- | --- |
| `faber test .` | exit 1 — **357** `SEM006.import_module_private` + 338 SEM010/SEM011 + 1 `package analysis failed` |
| `faber check .` (package mode) | **exit 0** (all `src/*.fab` library source clean) |
| Per-file sweep (`faber check` each of 28 `.fab` + 27 `.proba`) | 357 SEM006 total; the SEM006 count matches `faber test .` exactly |
| exempla (gradient-seam, training-loop-mlp, token-generation, gguf-manifest, gguf-inspect, qwen36-35b-inference) | 0 errors each |
| `tests/admission_conformance.fab` | 7 SEM006 (all `tokenizer.*` — covered by the tokenizer unit) |
| LIB-03 additions (`src/model/tensor_payload.{fab,proba}`, A3-C2-U1/U2) | 0 SEM006 (already annotated by the LIB-03 hands) |

The earlier `~675` figure (need `8e70a5b2`) predates the A1C visibility closure and the
M6-U1/Q1 repairs; the current, authoritative baseline is **357**.

### SEM006 by target module (defining module) on main `698d12f`

math 95 · dtype 35 · cache 33 · generation 32 · train 30 · shape 21 · loss 19 ·
parameter 19 · decode 16 · tokenizer 15 · metrics 11 · attention 7 · model/gguf 7 ·
model/gguf_manifest 6 · gradient 5 · serialize 4 · gradus 1 · sampling 1.

### First failing oracle per module (first SEM006 site at baseline)

| Module | First site |
| --- | --- |
| math | `src/attention.proba:72:15` (`math.cast`) |
| dtype | `src/dtype.proba:49:33` (`dtype.deserialize`) |
| shape | `src/shape.proba:42:21` (`shape.rank`) |
| tensor | `src/tensor.proba` (genus/surface errors — module-private error type) |
| cache | `src/cache.proba:79:29` (`cache.KVCache`) |
| decode | `src/decode.proba:140:35` (`decode.prefill`) |
| generation | `src/generation.proba:62:15` (`generation.message`) |
| gradient | `src/gradient.proba:76:32` (`gradient.Gradients`) |
| loss | `src/loss.proba:77:25` (`loss.mse`) |
| metrics | `src/metrics.proba:80:25` (`metrics.accuracy`) |
| nn | `src/nn.proba` (module-private error type) |
| attention | `src/attention.proba:94:35` (`attention.rotary_position_embedding`) |
| transformer | `src/transformer.proba` (module-private error type) |
| train | `src/train.proba:80:21` (`train.Mode`) |
| parameter | `src/parameter.proba:40:26` (`parameter.Identity`) |
| optimize | `src/optimize.proba` (`optimize.*` sites) |
| serialize | `src/serialize.proba:117:25` (`serialize.SerializedTensor`) |
| tokenizer | `src/tokenizer.proba:54:27` (`tokenizer.TokenizerIdentity`) |
| sampling | `src/sampling.proba:124:15` (`sampling.distribution`) |
| gradus | `src/gradus.proba:97:15` (`gradus.message`) |
| model/gguf | `src/model/gguf.proba:380:37` (`gguf.admit`) |
| model/gguf_manifest | `src/model/gguf_manifest.proba:556:40` (`manifestum.textorum`) |
| model/artifact | `src/model/artifact.proba` (module-private error type) |

## 3. Migration model (why annotation-only units are sufficient)

The current visibility seam (Radix `import_seam`, VM-U2/VM-U3):
unmarked or `@ privata` top-level declarations are **never** importable across files
(`SEM006:import_module_private`). `@ publica` is the only tier importable across
packages; `@ interna` is same-package only. Gradus is a consumed library (exempla and
the capstone are separate packages), so the public surface is marked `@ publica` — the
A1C pattern (`5445111`: mark at the defining declaration, keep `_`/`@ privata` helpers
private, no alias, no blanket sweep).

**Masking discovery (evidence §4)**: the checker short-circuits after a failed
reference, so per-file SEM006 counts at baseline **under-report** the true surface
(e.g. `tokenizer.proba` reports 15 at baseline; after its visible annotations land,
71 sites surface). The migration must therefore be driven by the **complete** per-module
annotation inventory (§4), not by the baseline site list. Each unit's done-oracle
("zero SEM006 referencing module X in the whole sweep") is self-completing: if a
late-surfacing member outside the inventory appears, the Hand annotates it in the same
module file and re-verifies.

**Error enums are part of the public surface.** Every `XxxError` discretio referenced
by proba `cape` clauses must also be `@ publica`, otherwise the per-file proba check
reports SEM010 cascade noise (package mode is clean either way, but the focused
per-file oracle is the Hand's closeout — see §5). The inventory includes them.

## 4. Scratch proof of the complete end-state

A copy of main `698d12f` (`git archive HEAD`) was annotated with the full inventory
below and re-checked under `FABER_LIBRARY_HOME=/tmp` (scratch parent):

- `faber check .` (package mode): **exit 0, zero errors**.
- `faber test .`: **zero SEM006/SEM010/SEM011 semantic errors**. The only remaining
  failures are the MIR-stepper runtime limits (`unsupported MIR lowering: method call
  before runtime/provider MIR lowering`, `failed to lower/run tests in …`) — the FMIR
  lever gate named in the need, out of this wave's scope.
- Per-file sweep across all 28 `.fab` + 27 `.proba`: **zero SEM006**; 10 residual
  SEM010/SEM014/SEM041 lines in 4 proba files (`gguf_manifest.proba:480/495`,
  `gguf.proba:448`, `parameter.proba:85/98`, `tensor.proba:21`) that are **per-file-mode
  resolution artifacts** — the same lines are clean in package mode (`faber test .` /
  `faber check .`). Documented; not migration scope.
- Total annotations applied: **129** across **23 module files**.

### Complete annotation inventory (anchored to main `698d12f` line numbers)

Insert one line `@ publica` immediately above each listed top-level declaration
(the VIS-04/VIS-05/`5445111` convention; the line preceding the declaration currently
has no `@ publica`).

| Module file | Annotations (name@line) |
| --- | --- |
| `src/math.fab` | MathError@78, construct@278, sub@316, div@351, neg@368, abs@379, signum@396, sum@411, mean@447, cast@545, concatenate@568, slice@634 |
| `src/dtype.fab` | DTypeError@124, width@165, serialize@178, deserialize@182, promote@203, narrow@239 |
| `src/shape.fab` | ShapeError@85, rank@118, reshape@219, expand@277 |
| `src/tensor.fab` | TensorError@119 |
| `src/cache.fab` | CacheError@62, message@73, KVCache@162, cache_equal@243, empty_cache@265, append@313, reset@367, CacheIdentity@393, cache_identity_equal@416, cache_identity@431, serialize_identity@458, deserialize_identity@466 |
| `src/decode.fab` | DecodeError@103, prefill@442, advance@503, cancellation_cancelled@542, replica@574 |
| `src/generation.fab` | GeneratioError@88, message@98, generation_equal@176, generation_failure@256, support_flags@266, admitted_features@272, serialize_generation@318, deserialize_generation@339, cursor_reset@517 |
| `src/gradient.fab` | GradientError@71, message@76, Gradients@145, construct_gradients@163 |
| `src/loss.fab` | LossError@93, message@105, mse@220, cross_entropy@261 |
| `src/metrics.fab` | MetricError@54, message@64, accuracy@85, metric_equal@188 |
| `src/nn.fab` | NnError@162 |
| `src/attention.fab` | AttentionError@140, rotary_position_embedding@508 |
| `src/transformer.fab` | TransformerError@164 |
| `src/train.fab` | TrainError@280, Mode@423, mode_name@429, is_discipline@445, is_estimate@450, mode@457, dropout_probability@472, Draw@563, next@580, Dropout@630, dropout@645, serialize_seed@678, deserialize_seed@682 |
| `src/parameter.fab` | status_name@88, ParameterError@100, Identity@134, identity_equal@170, is_trainable@253, construct_frozen@313, Registry@355, empty_registry@413, add@419, serialize@465, deserialize@473 |
| `src/optimize.fab` | OptimizeError@115, message@132, state_equal@231, sgd_equal@297, serialize_state@405, deserialize_state@410 |
| `src/serialize.fab` | SerializeError@117, message@126, SerializedTensor@144, ParameterWire@166, serialize_dtype@460, serialize_shape@472, serialize_tensor@506, serialize_parameter@543, deserialize_dtype@634, deserialize_shape@647, deserialize_tensor@677, deserialize_parameter@719 |
| `src/tokenizer.fab` | TokenizerError@207, message@219, TokenizerIdentity@240, probe_equal@352, probe_id@368, verify_probe@402, pinned_probe@412, construct@437, verify@495, tokenizer_key@535, serialize_identity@550, deserialize_identity@557 |
| `src/sampling.fab` | distribution@200 |
| `src/gradus.fab` | GradusError@89, message@100 |
| `src/model/gguf.fab` | GgufError@149, message@162, admit@331 |
| `src/model/gguf_manifest.fab` | layout@653, textorum@703, numerorum@732 |
| `src/model/artifact.fab` | ArtifactError@9 |

Anchors are against main `698d12f`; if a Hand's packet differs, locate by
`grep -n '^\(functio\|genus\|construct\|discretio\) <name>' <file>` — the first
top-level match with that name is the target (member functions are indented and are
**not** targets; note `metrics.accuracy` has an indented member overload — annotate
the top-level one only).

## 5. Unit graph

```
factory/merge (698d12f)
  ├─ SEM-MATH       src/math.fab           (12)   ─┐
  ├─ SEM-DTYPE      src/dtype.fab          ( 6)   │
  ├─ SEM-SHAPE      src/shape.fab          ( 4)   │
  ├─ SEM-TENSOR     src/tensor.fab         ( 1)   │
  ├─ SEM-CACHE      src/cache.fab          (12)   │
  ├─ SEM-DECODE     src/decode.fab         ( 5)   │
  ├─ SEM-GENERATION src/generation.fab     ( 9)   │
  ├─ SEM-GRADIENT   src/gradient.fab       ( 4)   │
  ├─ SEM-LOSS       src/loss.fab           ( 4)   │
  ├─ SEM-METRICS    src/metrics.fab        ( 4)   │
  ├─ SEM-NN         src/nn.fab             ( 1)   │  all parallel —
  ├─ SEM-ATTENTION  src/attention.fab      ( 2)   │  disjoint files,
  ├─ SEM-TRANSFORMER src/transformer.fab   ( 1)   │  additive annotations
  ├─ SEM-TRAIN      src/train.fab          (13)   │
  ├─ SEM-PARAMETER  src/parameter.fab      (11)   │
  ├─ SEM-OPTIMIZE   src/optimize.fab       ( 6)   │
  ├─ SEM-SERIALIZE  src/serialize.fab      (12)   │
  ├─ SEM-TOKENIZER  src/tokenizer.fab      (12)   │
  ├─ SEM-SAMPLING   src/sampling.fab       ( 1)   │
  ├─ SEM-GRADUS     src/gradus.fab         ( 2)   │
  ├─ SEM-GGUF       src/model/gguf.fab     ( 3)   │
  ├─ SEM-GGUFM      src/model/gguf_manifest.fab ( 3) │
  └─ SEM-ARTIFACT   src/model/artifact.fab ( 1)   ─┘
        │  (each merges to factory/merge alone — individually integrable)
        ▼
factory/merge SEM006-green on the 357 (+ masked) sites
        │
        ▼
Test lane owns `faber test .` / stages 3–6 (proba executed-value still gated on the FMIR lever)
```

- **Maximum safe parallelism**: 23 (all units disjoint files; additive `@ publica`
  cannot break any module; merge order free).
- **Integration**: each unit lands on its own `factory/<lane>` branch off
  `factory/merge`; commit message style `fix(gradus): expose <module> <symbols> to
  package consumers` (VIS-04/05/`5445111` precedent). `integrable: yes` for every unit.
- **No aggregate gate**: the final SEM006-zero state is verified by the test lane
  (`faber test .` shows no semantic errors) after all units are on `factory/merge`.

## 6. Unit specs (campaign rule-2 fields — one unit per module family)

Common fields per unit: `write_scope` = the single module file, exactly the listed
one-line `@ publica` insertions; `forbidden_scope` = any other annotation (preserve
`_`-helpers and `@ privata`), any other file, `.proba`/`docs/`/`scripta/`/`tests/`/
exempla edits, and the `faber test .`/`check-compile`/`--stage` gates (lane-owned);
`est_basis` = pilot at VIS-04/05/`5445111` scale — N one-line annotations + two narrow
checks (≈3–5k tokens); `depends_on` = base `factory/merge` `698d12f`; `integrable` = yes.

**Closeout command (each unit; run from the gradus packet root with the authority
setup — lane-local `FABER_BIN`, `FABER_LIBRARY_HOME="$(cd "$ROOT/.." && pwd)"`):**

```bash
faber check .                                   # package mode — expect exit 0 (unchanged)
faber check src/<X>.proba 2>&1 | grep SEM006    # focused — expect 0 lines after the unit
for f in src/*.proba src/model/*.proba tests/admission_conformance.fab; do
  faber check "$f" 2>&1 | grep SEM006; done     # sweep — expect no SEM006 referencing <X>
git diff --check                                # silent
```

**Expected observed result (each unit):** every member in the unit's inventory line is
`@ publica` immediately above its declaration (grep-verifiable); `faber check .` stays
exit 0; the focused proba check and the sweep show **zero SEM006 referencing module X**;
`faber test .`'s SEM006 total decreases by at least the module's §2 visible count;
remaining SEM006 lines (if any) reference other modules' aliases — record them, do not
fix; `git diff --check` silent. If a SEM006 referencing module X survives the inventory
(late-surfacing member), annotate it in the same file and re-verify (self-completing
oracle).

### SEM-MATH — `src/math.fab` (12 annotations)

| Field | Value |
| --- | --- |
| outcome | math family public-import surface complete: MathError + construct/sub/div/neg/abs/signum/sum/mean/cast/concatenate/slice `@ publica`; all SEM006 referencing `math.` cleared tree-wide (95 visible sites at baseline) |
| exact write scope | `src/math.fab` — `@ publica` immediately above each of the 12 §4 anchors (MathError@78, construct@278, sub@316, div@351, neg@368, abs@379, signum@396, sum@411, mean@447, cast@545, concatenate@568, slice@634) |
| first failing oracle | `src/attention.proba:72:15` SEM006 (`math.cast`) |
| closeout command | common closeout with `<X>` = math |
| expected observed result | zero SEM006 referencing `math.` in the sweep; `faber test .` SEM006 drops by ≥95; `faber check .` exit 0; remaining SEM006 are non-math targets (record) |
| est_basis | pilot; 12 one-line insertions + narrow checks (math.proba is the largest proba; single-file checks <1s) |
| stop condition | all 12 anchors carry `@ publica`; zero `math.` SEM006 in the sweep; `git diff --check` silent |
| depends_on | base `698d12f` |

### SEM-DTYPE — `src/dtype.fab` (6 annotations)

| Field | Value |
| --- | --- |
| outcome | dtype family public-import surface complete: DTypeError + width/serialize/deserialize/promote/narrow `@ publica`; all SEM006 referencing `dtype.` cleared (35 visible sites) |
| exact write scope | `src/dtype.fab` — `@ publica` above DTypeError@124, width@165, serialize@178, deserialize@182, promote@203, narrow@239 |
| first failing oracle | `src/dtype.proba:49:33` SEM006 (`dtype.deserialize`) |
| closeout command | common closeout with `<X>` = dtype |
| expected observed result | zero SEM006 referencing `dtype.` in the sweep; `faber test .` SEM006 drops by ≥35 |
| est_basis | pilot; 6 one-line insertions + narrow checks |
| stop condition | all 6 anchors annotated; zero `dtype.` SEM006 in the sweep; `git diff --check` silent |
| depends_on | base `698d12f` |

### SEM-SHAPE — `src/shape.fab` (4 annotations)

| Field | Value |
| --- | --- |
| outcome | shape family public-import surface complete: ShapeError + rank/reshape/expand `@ publica`; all SEM006 referencing `shape.` cleared (21 visible sites) |
| exact write scope | `src/shape.fab` — `@ publica` above ShapeError@85, rank@118, reshape@219, expand@277 |
| first failing oracle | `src/shape.proba:42:21` SEM006 (`shape.rank`) |
| closeout command | common closeout with `<X>` = shape |
| expected observed result | zero SEM006 referencing `shape.` in the sweep; `faber test .` SEM006 drops by ≥21 |
| est_basis | pilot; 4 one-line insertions + narrow checks |
| stop condition | all 4 anchors annotated; zero `shape.` SEM006 in the sweep; `git diff --check` silent |
| depends_on | base `698d12f` |

### SEM-TENSOR — `src/tensor.fab` (1 annotation)

| Field | Value |
| --- | --- |
| outcome | tensor family public surface complete: TensorError `@ publica` (genus Tensor and its constructors already publica on main); tensor.proba's `cape`-typed error surface SEM006-free |
| exact write scope | `src/tensor.fab` — `@ publica` above TensorError@119 only |
| first failing oracle | `src/tensor.proba` SEM006 on the module-private error type (visible at baseline; exact line in the tensor.proba check output) |
| closeout command | common closeout with `<X>` = tensor |
| expected observed result | zero SEM006 referencing `tensor.` in the sweep; `faber test .` SEM006 decreases |
| est_basis | pilot; 1 one-line insertion + narrow checks (smallest unit — Mind may batch with other small units at dispatch) |
| stop condition | TensorError annotated; zero `tensor.` SEM006 in the sweep; `git diff --check` silent |
| depends_on | base `698d12f` |

### SEM-CACHE — `src/cache.fab` (12 annotations)

| Field | Value |
| --- | --- |
| outcome | cache family public-import surface complete: CacheError, KVCache, CacheIdentity + message/cache_equal/empty_cache/append/reset/cache_identity_equal/cache_identity/serialize_identity/deserialize_identity `@ publica`; all SEM006 referencing `cache.` cleared (33 visible + masked sites) |
| exact write scope | `src/cache.fab` — `@ publica` above the 12 §4 anchors (CacheError@62 … deserialize_identity@466) |
| first failing oracle | `src/cache.proba:79:29` SEM006 (`cache.KVCache`) |
| closeout command | common closeout with `<X>` = cache |
| expected observed result | zero SEM006 referencing `cache.` in the sweep; `faber test .` SEM006 drops by ≥33 (masked sites in cache.proba surface with this unit — the full cache set clears here) |
| est_basis | pilot; 12 one-line insertions + narrow checks |
| stop condition | all 12 anchors annotated; zero `cache.` SEM006 in the sweep; `git diff --check` silent |
| depends_on | base `698d12f` |

### SEM-DECODE — `src/decode.fab` (5 annotations)

| Field | Value |
| --- | --- |
| outcome | decode family public-import surface complete: DecodeError + prefill/advance/cancellation_cancelled/replica `@ publica`; all SEM006 referencing `decode.` cleared (16 visible sites) |
| exact write scope | `src/decode.fab` — `@ publica` above DecodeError@103, prefill@442, advance@503, cancellation_cancelled@542, replica@574 |
| first failing oracle | `src/decode.proba:140:35` SEM006 (`decode.prefill`) |
| closeout command | common closeout with `<X>` = decode |
| expected observed result | zero SEM006 referencing `decode.` in the sweep; `faber test .` SEM006 drops by ≥16 |
| est_basis | pilot; 5 one-line insertions + narrow checks |
| stop condition | all 5 anchors annotated; zero `decode.` SEM006 in the sweep; `git diff --check` silent |
| depends_on | base `698d12f` |

### SEM-GENERATION — `src/generation.fab` (9 annotations)

| Field | Value |
| --- | --- |
| outcome | generation family public-import surface complete: GeneratioError + message/generation_equal/generation_failure/support_flags/admitted_features/serialize_generation/deserialize_generation/cursor_reset `@ publica`; all SEM006 referencing `generation.` cleared (32 visible sites) |
| exact write scope | `src/generation.fab` — `@ publica` above the 9 §4 anchors (GeneratioError@88 … cursor_reset@517) |
| first failing oracle | `src/generation.proba:62:15` SEM006 (`generation.message`) |
| closeout command | common closeout with `<X>` = generation |
| expected observed result | zero SEM006 referencing `generation.` in the sweep; `faber test .` SEM006 drops by ≥32 |
| est_basis | pilot; 9 one-line insertions + narrow checks |
| stop condition | all 9 anchors annotated; zero `generation.` SEM006 in the sweep; `git diff --check` silent |
| depends_on | base `698d12f` |

### SEM-GRADIENT — `src/gradient.fab` (4 annotations)

| Field | Value |
| --- | --- |
| outcome | gradient family public-import surface complete: GradientError, Gradients + message/construct_gradients `@ publica`; all SEM006 referencing `gradient.` cleared (5 visible + masked sites) |
| exact write scope | `src/gradient.fab` — `@ publica` above GradientError@71, message@76, Gradients@145, construct_gradients@163 |
| first failing oracle | `src/gradient.proba:76:32` SEM006 (`gradient.Gradients`) |
| closeout command | common closeout with `<X>` = gradient |
| expected observed result | zero SEM006 referencing `gradient.` in the sweep; `faber test .` SEM006 decreases |
| est_basis | pilot; 4 one-line insertions + narrow checks |
| stop condition | all 4 anchors annotated; zero `gradient.` SEM006 in the sweep; `git diff --check` silent |
| depends_on | base `698d12f` |

### SEM-LOSS — `src/loss.fab` (4 annotations)

| Field | Value |
| --- | --- |
| outcome | loss family public-import surface complete: LossError + message/mse/cross_entropy `@ publica`; all SEM006 referencing `loss.` cleared (19 visible sites) |
| exact write scope | `src/loss.fab` — `@ publica` above LossError@93, message@105, mse@220, cross_entropy@261 |
| first failing oracle | `src/loss.proba:77:25` SEM006 (`loss.mse`) |
| closeout command | common closeout with `<X>` = loss |
| expected observed result | zero SEM006 referencing `loss.` in the sweep; `faber test .` SEM006 drops by ≥19 |
| est_basis | pilot; 4 one-line insertions + narrow checks |
| stop condition | all 4 anchors annotated; zero `loss.` SEM006 in the sweep; `git diff --check` silent |
| depends_on | base `698d12f` |

### SEM-METRICS — `src/metrics.fab` (4 annotations)

| Field | Value |
| --- | --- |
| outcome | metrics family public-import surface complete: MetricError + message/accuracy (top-level overload)/metric_equal `@ publica`; all SEM006 referencing `metrica.` cleared (11 visible sites) |
| exact write scope | `src/metrics.fab` — `@ publica` above MetricError@54, message@64, accuracy@85, metric_equal@188 (the indented member `accuracy()` inside Metric is NOT a target) |
| first failing oracle | `src/metrics.proba:80:25` SEM006 (`metrics.accuracy`) |
| closeout command | common closeout with `<X>` = metrics |
| expected observed result | zero SEM006 referencing `metrica.` in the sweep; `faber test .` SEM006 drops by ≥11 |
| est_basis | pilot; 4 one-line insertions + narrow checks |
| stop condition | all 4 anchors annotated; zero `metrica.` SEM006 in the sweep; `git diff --check` silent |
| depends_on | base `698d12f` |

### SEM-NN — `src/nn.fab` (1 annotation)

| Field | Value |
| --- | --- |
| outcome | nn family public surface complete: NnError `@ publica`; nn.proba's error surface SEM006-free |
| exact write scope | `src/nn.fab` — `@ publica` above NnError@162 only |
| first failing oracle | `src/nn.proba` SEM006 on the module-private error type (baseline check output) |
| closeout command | common closeout with `<X>` = nn |
| expected observed result | zero SEM006 referencing `nn.` in the sweep; `faber test .` SEM006 decreases |
| est_basis | pilot; 1 one-line insertion + narrow checks (small unit — batchable at dispatch) |
| stop condition | NnError annotated; zero `nn.` SEM006 in the sweep; `git diff --check` silent |
| depends_on | base `698d12f` |

### SEM-ATTENTION — `src/attention.fab` (2 annotations)

| Field | Value |
| --- | --- |
| outcome | attention family public-import surface complete: AttentionError + rotary_position_embedding `@ publica`; all SEM006 referencing `attention.` cleared (7 visible sites) |
| exact write scope | `src/attention.fab` — `@ publica` above AttentionError@140, rotary_position_embedding@508 |
| first failing oracle | `src/attention.proba:94:35` SEM006 (`attention.rotary_position_embedding`) |
| closeout command | common closeout with `<X>` = attention |
| expected observed result | zero SEM006 referencing `attention.` in the sweep; `faber test .` SEM006 drops by ≥7 |
| est_basis | pilot; 2 one-line insertions + narrow checks |
| stop condition | both anchors annotated; zero `attention.` SEM006 in the sweep; `git diff --check` silent |
| depends_on | base `698d12f` |

### SEM-TRANSFORMER — `src/transformer.fab` (1 annotation)

| Field | Value |
| --- | --- |
| outcome | transformer family public surface complete: TransformerError `@ publica`; transformer.proba's error surface SEM006-free |
| exact write scope | `src/transformer.fab` — `@ publica` above TransformerError@164 only |
| first failing oracle | `src/transformer.proba` SEM006 on the module-private error type (baseline check output) |
| closeout command | common closeout with `<X>` = transformer |
| expected observed result | zero SEM006 referencing `transformer.` in the sweep; `faber test .` SEM006 decreases |
| est_basis | pilot; 1 one-line insertion + narrow checks (small unit — batchable at dispatch) |
| stop condition | TransformerError annotated; zero `transformer.` SEM006 in the sweep; `git diff --check` silent |
| depends_on | base `698d12f` |

### SEM-TRAIN — `src/train.fab` (13 annotations)

| Field | Value |
| --- | --- |
| outcome | train family public-import surface complete: TrainError, Mode, Draw, Dropout + mode_name/is_discipline/is_estimate/mode/dropout_probability/next/dropout/serialize_seed/deserialize_seed `@ publica`; all SEM006 referencing `train.` cleared (30 visible + masked sites) |
| exact write scope | `src/train.fab` — `@ publica` above the 13 §4 anchors (TrainError@280 … deserialize_seed@682) |
| first failing oracle | `src/train.proba:80:21` SEM006 (`train.Mode`) |
| closeout command | common closeout with `<X>` = train |
| expected observed result | zero SEM006 referencing `train.` in the sweep; `faber test .` SEM006 drops by ≥30 (masked train.proba + optimize-targeted sites surface here or under SEM-OPTIMIZE; record non-train ones) |
| est_basis | pilot; 13 one-line insertions + narrow checks |
| stop condition | all 13 anchors annotated; zero `train.` SEM006 in the sweep; `git diff --check` silent |
| depends_on | base `698d12f` |

### SEM-PARAMETER — `src/parameter.fab` (11 annotations)

| Field | Value |
| --- | --- |
| outcome | parameter family public-import surface complete: ParameterError, Identity, Registry + status_name/identity_equal/is_trainable/construct_frozen/empty_registry/add/serialize/deserialize `@ publica`; all SEM006 referencing `parametrum.` cleared (19 visible + masked sites) |
| exact write scope | `src/parameter.fab` — `@ publica` above the 11 §4 anchors (status_name@88 … deserialize@473) |
| first failing oracle | `src/parameter.proba:40:26` SEM006 (`parameter.Identity`) |
| closeout command | common closeout with `<X>` = parameter |
| expected observed result | zero SEM006 referencing `parametrum.` in the sweep; `faber test .` SEM006 drops by ≥19 |
| est_basis | pilot; 11 one-line insertions + narrow checks |
| stop condition | all 11 anchors annotated; zero `parametrum.` SEM006 in the sweep; `git diff --check` silent |
| depends_on | base `698d12f` |

### SEM-OPTIMIZE — `src/optimize.fab` (6 annotations)

| Field | Value |
| --- | --- |
| outcome | optimize family public-import surface complete: OptimizeError + message/state_equal/sgd_equal/serialize_state/deserialize_state `@ publica`; all SEM006 referencing `optimize.` cleared (masked sites in optimize.proba/train.proba) |
| exact write scope | `src/optimize.fab` — `@ publica` above OptimizeError@115, message@132, state_equal@231, sgd_equal@297, serialize_state@405, deserialize_state@410 |
| first failing oracle | `src/optimize.proba` SEM006 (`optimize.*` sites — baseline check output) |
| closeout command | common closeout with `<X>` = optimize |
| expected observed result | zero SEM006 referencing `optimize.` in the sweep; note optimize.proba's masked sites also reference parameter/gradient (record, non-optimize targets) |
| est_basis | pilot; 6 one-line insertions + narrow checks |
| stop condition | all 6 anchors annotated; zero `optimize.` SEM006 in the sweep; `git diff --check` silent |
| depends_on | base `698d12f` |

### SEM-SERIALIZE — `src/serialize.fab` (12 annotations)

| Field | Value |
| --- | --- |
| outcome | serialize family public-import surface complete: SerializeError, SerializedTensor, ParameterWire + message/serialize_dtype/serialize_shape/serialize_tensor/serialize_parameter/deserialize_dtype/deserialize_shape/deserialize_tensor/deserialize_parameter `@ publica`; all SEM006 referencing `serialize.` cleared (4 visible + masked sites) |
| exact write scope | `src/serialize.fab` — `@ publica` above the 12 §4 anchors (SerializeError@117 … deserialize_parameter@719) |
| first failing oracle | `src/serialize.proba:117:25` SEM006 (`serialize.SerializedTensor`) |
| closeout command | common closeout with `<X>` = serialize |
| expected observed result | zero SEM006 referencing `serialize.` in the sweep; `faber test .` SEM006 decreases |
| est_basis | pilot; 12 one-line insertions + narrow checks |
| stop condition | all 12 anchors annotated; zero `serialize.` SEM006 in the sweep; `git diff --check` silent |
| depends_on | base `698d12f` |

### SEM-TOKENIZER — `src/tokenizer.fab` (12 annotations)

| Field | Value |
| --- | --- |
| outcome | tokenizer family public-import surface complete: TokenizerError, TokenizerIdentity + message/probe_equal/probe_id/verify_probe/pinned_probe/construct/verify/tokenizer_key/serialize_identity/deserialize_identity `@ publica`; all SEM006 referencing `tokenizer.` cleared (15 visible + masked sites; also clears the 7 `tests/admission_conformance.fab` sites) |
| exact write scope | `src/tokenizer.fab` — `@ publica` above the 12 §4 anchors (TokenizerError@207 … deserialize_identity@557) |
| first failing oracle | `src/tokenizer.proba:54:27` SEM006 (`tokenizer.TokenizerIdentity`) |
| closeout command | common closeout with `<X>` = tokenizer (sweep includes `tests/admission_conformance.fab`) |
| expected observed result | zero SEM006 referencing `tokenizer.` in the sweep (including admission_conformance.fab); `faber test .` SEM006 drops by ≥15 |
| est_basis | pilot; 12 one-line insertions + narrow checks (masking-heavy proba — the inventory already includes the masked members) |
| stop condition | all 12 anchors annotated; zero `tokenizer.` SEM006 in the sweep; `git diff --check` silent |
| depends_on | base `698d12f` |

### SEM-SAMPLING — `src/sampling.fab` (1 annotation)

| Field | Value |
| --- | --- |
| outcome | sampling family public-import surface complete: distribution `@ publica`; all SEM006 referencing `sampling.` cleared (1 visible site) |
| exact write scope | `src/sampling.fab` — `@ publica` above distribution@200 only |
| first failing oracle | `src/sampling.proba:124:15` SEM006 (`sampling.distribution`) |
| closeout command | common closeout with `<X>` = sampling |
| expected observed result | zero SEM006 referencing `sampling.` in the sweep |
| est_basis | pilot; 1 one-line insertion + narrow checks (small unit — batchable at dispatch) |
| stop condition | distribution annotated; zero `sampling.` SEM006 in the sweep; `git diff --check` silent |
| depends_on | base `698d12f` |

### SEM-GRADUS — `src/gradus.fab` (2 annotations)

| Field | Value |
| --- | --- |
| outcome | gradus facade public surface complete: GradusError + message `@ publica`; all SEM006 referencing `gradus.` cleared (1 visible site) |
| exact write scope | `src/gradus.fab` — `@ publica` above GradusError@89, message@100 |
| first failing oracle | `src/gradus.proba:97:15` SEM006 (`gradus.message`) |
| closeout command | common closeout with `<X>` = gradus |
| expected observed result | zero SEM006 referencing `gradus.` in the sweep |
| est_basis | pilot; 2 one-line insertions + narrow checks |
| stop condition | both anchors annotated; zero `gradus.` SEM006 in the sweep; `git diff --check` silent |
| depends_on | base `698d12f` |

### SEM-GGUF — `src/model/gguf.fab` (3 annotations)

| Field | Value |
| --- | --- |
| outcome | gguf admission family public-import surface complete: GgufError + message/admit `@ publica`; all SEM006 referencing `gguf.` cleared (7 visible sites) |
| exact write scope | `src/model/gguf.fab` — `@ publica` above GgufError@149, message@162, admit@331 |
| first failing oracle | `src/model/gguf.proba:380:37` SEM006 (`gguf.admit`) |
| closeout command | common closeout with `<X>` = model/gguf |
| expected observed result | zero SEM006 referencing `gguf.` in the sweep; `faber test .` SEM006 drops by ≥7 |
| est_basis | pilot; 3 one-line insertions + narrow checks |
| stop condition | all 3 anchors annotated; zero `gguf.` SEM006 in the sweep; `git diff --check` silent |
| depends_on | base `698d12f` |

### SEM-GGUFM — `src/model/gguf_manifest.fab` (3 annotations)

| Field | Value |
| --- | --- |
| outcome | gguf_manifest family public-import surface complete: layout/textorum/numerorum `@ publica`; all SEM006 referencing `manifestum.` cleared (6 visible sites) |
| exact write scope | `src/model/gguf_manifest.fab` — `@ publica` above layout@653, textorum@703, numerorum@732 |
| first failing oracle | `src/model/gguf_manifest.proba:556:40` SEM006 (`manifestum.textorum`) |
| closeout command | common closeout with `<X>` = model/gguf_manifest |
| expected observed result | zero SEM006 referencing `manifestum.` in the sweep; `faber test .` SEM006 drops by ≥6 |
| est_basis | pilot; 3 one-line insertions + narrow checks |
| stop condition | all 3 anchors annotated; zero `manifestum.` SEM006 in the sweep; `git diff --check` silent |
| depends_on | base `698d12f` |

### SEM-ARTIFACT — `src/model/artifact.fab` (1 annotation)

| Field | Value |
| --- | --- |
| outcome | artifact family public surface complete: ArtifactError `@ publica` (identitas/message already publica via `5445111`); artifact.proba's error surface SEM006-free |
| exact write scope | `src/model/artifact.fab` — `@ publica` above ArtifactError@9 only |
| first failing oracle | `src/model/artifact.proba` SEM006 on the module-private error type (baseline check output) |
| closeout command | common closeout with `<X>` = model/artifact |
| expected observed result | zero SEM006 referencing `artifact.` in the sweep |
| est_basis | pilot; 1 one-line insertion + narrow checks (small unit — batchable at dispatch) |
| stop condition | ArtifactError annotated; zero `artifact.` SEM006 in the sweep; `git diff --check` silent |
| depends_on | base `698d12f` |

## 7. Lane-owned validation (named once, not on children)

- **Lint lane** owns stages 1–2 on the integrated tree (mechanical; annotation lines
  carry no lint risk).
- **Test lane** owns `faber test .` and stages 3–6 after the wave lands: expected
  outcome is **zero semantic errors** (SEM006/SEM010/…); proba *executed-value* evidence
  remains gated on the FMIR lever (`unsupported MIR lowering: method call before
  runtime/provider MIR lowering`) — that is the need's own residual, not this wave.
- **Merge lane** integrates each unit via `factory/merge` (ff-only on main); additive
  annotations cannot conflict across units, so merge order is free.

## 8. Parallelism with the LIB-02/03 chain

- **Currently safe.** LIB-02-U1 (`c4d0750`), A3-C1 (`82048b5`), and A3-C2-U1/U2
  (`f6732db`, `fc59ac4`, `e640a50`) are merged on main; no LIB-02/03 hand task is open
  on the board at dispatch time. The wave is parallel-safe to dispatch **now**.
- **Overlapping files with future LIB-02/03 units**: `src/model/gguf_manifest.fab`
  (SEM-GGUFM), `src/tokenizer.fab` (SEM-TOKENIZER), `src/model/gguf.fab` (SEM-GGUF),
  `src/decode.fab` (SEM-DECODE), `src/generation.fab` (SEM-GENERATION). If LIB-02/03
  dispatches a unit on one of these files while the corresponding SEM unit is in
  flight, the one-line annotations can conflict mechanically with new code. Per the
  standing non-overlap rule: serialize those pairs (dispatch order: SEM unit first —
  the annotations are trivial to rebase; or LIB unit first — the SEM list re-anchors).
  Mind should not dispatch both on the same file concurrently.
- No cross-repo parallelism constraints (radix/faber/hosts untouched by this wave).

## 9. Open questions for Mind

1. **Packet staleness**: the `planner-33` packet gradus member is at `1462cd8`
   (pre-A1C), not local main `698d12f`. Refresh the lane (`scripta/hand-packet refresh
   planner-33`) before dispatch so Hands measure the same baseline this delivery cites.
2. **Batch dispatch**: the five 1-annotation units (SEM-TENSOR, SEM-NN,
   SEM-TRANSFORMER, SEM-SAMPLING, SEM-ARTIFACT) sit at the small end of the granularity
   bar. They are individually valid (each clears a real proba surface) but may be
   batched into two units at dispatch if Hand-turn economy argues for it — the unit
   graph and oracles are unchanged by batching.
3. **Per-file-mode residual noise**: after the wave, per-file `faber check` on 4 proba
   files (`gguf_manifest`, `gguf`, `parameter`, `tensor`) reports 10 SEM010/SEM014/
   SEM041 lines that are clean in package mode (proven on the scratch copy). If the
   test lane wants a zero-noise per-file sweep, that is a separate radix-side
   resolution-mode question, not a gradus migration item.

## 10. Honesty notes

- The `~675` count in the need is historical (pre-A1C). The measured baseline on
  current main is **357** SEM006; the end-state proof (§4) clears the 357 plus all
  masked sites revealed by annotation (total 129 annotations).
- The end-state proof was executed on a scratch copy of main `698d12f` under
  `FABER_LIBRARY_HOME=/tmp`; the authoritative gate (`faber test .` on the merged tree)
  is owned by the test lane per §7.
- Masking means a module's true SEM006 site count can exceed the §2 visible count;
  unit oracles are written against "zero SEM006 referencing module X" (the count, not
  the estimate), so no unit can close while its module still leaks sites.
