# S2 collision ledger — mandatory preflight

**Status**: complete — S2-PREFLIGHT gate artifact
**Repo**: `gradus` main, commit base `adb632f`
**Radix evidence**: clean temporary worktree `/tmp/gradus-s2-radix`, HEAD `4350f4f8c90c2f1f7e6301720628d8dbe6dc52a7`
**Faber binary**: `/tmp/gradus-s2-radix/target/debug/faber` (`faber 1.7.0`)
**Probe environment**: `FABER_LIBRARY_HOME=/Users/ianzepp/work/faberlang`
**Scope**: documentation and `/tmp/gradus-s2-*` receipts only. This unit made no `src/`, `.proba`, `exempla/`, `tests/`, pack, or sibling-repository writes.

## Contract completion — verbatim done-when clauses

(1) the 750-symbol live census is recorded;

(2) every family row has a complete old→new member ledger, including private helpers and collision-sensitive fields;

(3) the reserved lock is checked against live Radix `[keywords]`, `[types]`, `[intrinsics]`, builtin `STATUS_VARIANTS`, scalar-interval rules, tensor-directed rules, and frame-view methods;

(4) the Tensor field/method shape probe is recorded;

(5) the member-scoped parameter policy is recorded;

(6) one scratch convert+rename+`faber check` probe has run for each source family before any batch;

(7) the artifact says explicitly that Gradus owns this preflight and that no pack-row mechanism is involved.

## Ownership and no-pack-row ruling

Gradus owns `S2-PREFLIGHT`. This ledger is the gate artifact for the nine ordered S2 rows. It creates no `[[library_members]]` row, adds no locale-pack row, and requires no Radix edit. The preflight makes no implementation rename. Import coordinates remain unchanged. Later family units must consume the locked names below rather than reopening the collision decisions.

## Live 750-symbol census

The census was run from the Gradus repository root with:

```bash
cd /Users/ianzepp/work/faberlang/gradus
./scripta/inventory-public-symbols
rg -n --glob '*.fab' --glob '*.proba' \
  '\\b(figura|forma|gradus|typus|typo|valor|causa|accipe|structa|verifica|serializa|deserializa|quantitas|longitudo|nomen|segmentum)\\b' src
```

The complete raw outputs are retained at `/tmp/gradus-s2-inventory.txt` and `/tmp/gradus-s2-source-census.txt`. The inventory result was:

| Live `.fab` module | `fn ` declarations |
| --- | ---: |
| `attention` | 35 |
| `cache` | 37 |
| `data` | 0 |
| `decode` | 46 |
| `dtype` | 14 |
| `generation` | 27 |
| `gradient` | 13 |
| `gradus` | 7 |
| `loss` | 11 |
| `math` | 23 |
| `metrics` | 6 |
| `model/artifact` | 4 |
| `model/capsule` | 45 |
| `model/dense_llama` | 6 |
| `model/dense_qwen2` | 14 |
| `model/dense` | 11 |
| `model/dequant` | 21 |
| `model/gguf_manifest` | 49 |
| `model/gguf` | 10 |
| `model/qwen35moe` | 42 |
| `model/safetensors` | 24 |
| `model/tensor_payload` | 1 |
| `model/tensor_view` | 7 |
| `nn` | 24 |
| `optimize` | 26 |
| `parameter` | 37 |
| `sampling` | 27 |
| `serialize` | 34 |
| `shape` | 9 |
| `tensor` | 11 |
| `tokenizer` | 74 |
| `train` | 41 |
| `transformer` | 14 |
| **TOTAL** | **750** |

The 750 count is declaration inventory, not the rename count. Fields, union/class types, private helpers, already-English members, parameters, comments, and string literals are accounted for in the family rows and policy below.

The family partition is the completed census boundary:

| Family | Source boundary | Files | `fn ` count |
| --- | --- | ---: | ---: |
| L1 | `src/dtype*`, `shape*`, `tensor*`, `math*` | 4 | 57 |
| Shared | `src/parameter*`, `serialize*`, `gradient*` | 3 | 84 |
| Train | `src/loss*`, `optimize*`, `nn*`, `train*`, `metrics*`, `data*` | 6 | 108 |
| Arch | `src/attention*`, `transformer*` | 2 | 49 |
| Model | all live `src/model/*.fab` and `.proba` | 12 | 234 |
| Tokenizer | `src/tokenizer*` | 1 | 74 |
| Inference | `src/cache*`, `decode*`, `sampling*`, `generation*` | 4 | 137 |
| Facade | `src/gradus*` plus remaining in-repo callers | 1 | 7 |
| Docs/inventory | no source file; final docs and gate rebase | — | — |
| **Source total** | all live modules | **33** | **750** |

## Reserved-name and compiler-owned census

### Live English pack

The required command was run against `/Users/ianzepp/work/faberlang/radix/stdlib/locale/en/pack.toml`:

```bash
rg -n '^(typus|valor|magnitudo|nomen|subtrahe|longitudo|applica|magnitudines|crea)\\s*=' \
  /Users/ianzepp/work/faberlang/radix/stdlib/locale/en/pack.toml
```

The exact matched rows were:

```text
typus = "type"
magnitudo = "size"
nomen = "name"
valor = "value"
longitudo = "length"
subtrahe = "subtract"
magnitudines = "shape"
crea = "create"
applica = "apply"
```

The full `[keywords]`, `[types]`, and `[intrinsics]` section snapshot is retained at `/tmp/gradus-s2-pack-sections.txt`. Relevant live rows include:

```text
[ keywords ]
genus = "class"
functio = "fn"
importa = "import"
typus = "type"
exitus = "exit"
magnitudo = "size"
privata = "private"
publica = "public"
sponte = "optional"
redde = "return"
cape = "catch"
argumenta = "args"
incipit = "main"
ad = "call"
fiet = "async"
tacebit = "await"
nomen = "name"

[ types ]
textus = "string"
numerus = "int"
fractus = "float"
bivalens = "bool"
nihil = "null_ty"
vacuum = "void"
ignotum = "unknown"
octeti = "bytes"
valor = "value"
lista = "list"
tabula = "map"
copia = "set"
tensor = "tensor"
vector = "vector"
matrix = "matrix"

[ intrinsics ]
accipe = "get"
addita = "added"
appende = "append"
continet = "contains"
longitudo = "length"
sectio = "slice"
subtrahe = "subtract"
multiplica = "multiply"
magnitudines = "shape"
forma = "reshape"
matmul = "matmul"
crea = "create"
strue = "from_flat"
transpone = "transpose"
applica = "apply"
```

The reserved lock therefore treats `value`, `string`, `int`, `bool`, `float`, `list`, `map`, `set`, `bytes`, `void`, `unknown`, `null`, `tensor`, `vector`, `matrix`, `fn`, `class`, `union`, `enum`, `type`, `const`, `let`, `var`, `import`, `from`, `as`, `public`, `private`, `optional`, `return`, `if`, `else`, `elif`, `then`, `for`, `while`, `match`, `case`, `throw`, `catch`, `do`, `assert`, `panic`, `true`, `false`, `and`, `or`, `not`, `is`, `self`, `main`, `print`, `test`, `read`, `write`, `warn`, `debug`, `size`, `name`, `step`, `range`, `between`, `within`, `until`, `line`, `args`, `call`, `await`, `async`, `future`, `format`, `require`, and `exit` as reserved unless the exact receiver/member probe below proves a member position is accepted.

Decisions from the live pack and probes:

- `valor` never targets the reserved en type `value`. Tensor/value carriers use `payload`; an accessor may use `get` only when its receiver has no existing `get` member.
- `typus`/`typo` targets `dtype` on DType-bearing carriers and `kind` outside that meaning. It never targets `type`.
- `quantitas` targets `numel`, not `size`. The live en row is `magnitudo = "size"`; `size` is compiler-owned even though an isolated declaration can parse.
- `nomen` targets `name` only in a member position. The Shared first-file probe and the synthetic docs smoke probe both accepted the field/method position.
- `longitudo` user members may target `length` only on their Gradus receiver. The compiler's scalar/list intrinsic remains compiler-owned.
- `forma`/`figura` collapse to `shape` only on the Tensor/value member rows covered by the Tensor shape probe. Compiler `forma` remains the reshape intrinsic.

### Frame statuses and view methods

The required frame census was run with:

```bash
rg -n 'STATUS_VARIANTS|request|item|byte|bulk|done|error|cancel' \
  /Users/ianzepp/work/faberlang/radix/crates/radix/src/builtins/frame_types.rs \
  /Users/ianzepp/work/faberlang/radix/crates/radix-runtime-contract/src/frame.rs
```

Live `STATUS_VARIANTS` is exactly:

```text
["request", "item", "byte", "bulk", "done", "error", "cancel"]
```

`radix-runtime-contract/src/frame.rs` confirms the same order and classification: `request` is non-terminal/non-content; `item`, `byte`, and `bulk` are content; `done`, `error`, and `cancel` are terminal/non-content. These seven names are locked out of every new target. No Gradus member targets a frame status.

`call.rs` was checked for compiler view methods. The live branches are:

```text
meus.da
meus.fini
tuus.accipe
tuus.cursor
tuus.exhauri
tuus.fini
```

The live `meus`/`tuus` receiver branches and their DefIds are in `/tmp/gradus-s2-view-census.txt`. `Tensor.accipe → get` is a Gradus receiver decision and does not rename the compiler-owned `tuus.accipe` branch.

### Scalar intervals and tensor-directed names

The live scalar interval evidence is retained at `/tmp/gradus-s2-interval-census.txt` and `/tmp/gradus-s2-interval-narrow.txt`. `intrinsics.rs:199–204` dispatches the compiler `intervallum.longitudo` intrinsic to `check_intervallum_longitudo_bound`; `intervallum.rs:120–124` says the v1 bound is bare `numerus` only. A Gradus user `longitudo` may become `length` only by receiver/member ledger. The compiler interval rule is not a Gradus alias and does not authorize `size`.

The tensor-directed evidence is retained at `/tmp/gradus-s2-directed-census.txt`. The live compiler-owned set is:

```text
module/receiver: creata, structa, crea, formata
removed/diagnostic: structa_forma
```

`structa` in a Gradus user constructor targets `construct`. Compiler-directed `creata`, `crea`, `formata`, and the removed-shape diagnostic remain Radix names and are not swept as Gradus members. The live tensor-index evidence is retained at `/tmp/gradus-s2-tensor-index-narrow.txt` and records `strue`, `sectio`, `transpone`, `addita`, `subtrahe`, `multiplica`, and `matmul`. The requested audit spelling `tranzone` is absent; the live key is `transpone`. `scalar_text.rs:100–103` independently confirms a compiler `MethodCall` branch for `sectio`.

### Valor/catch/typo classification

The required live source command was run over both `.fab` and `.proba`:

```bash
cd /Users/ianzepp/work/faberlang/gradus
rg -n --glob '*.fab' --glob '*.proba' \
  '\\b(figura|forma|gradus|typus|typo|valor|causa|accipe|structa|verifica|serializa|deserializa|quantitas|longitudo|nomen|segmentum)\\b' src
```

The raw collision census is `/tmp/gradus-s2-source-census.txt`. The dedicated Valor/catch receipt is `/tmp/gradus-s2-valor-classification.txt`; it found 164 `valor` occurrences and 700 `catch err` bindings across the live source. Every `valor` hit is classified by syntactic position before a family opens:

1. **Member/field/accessor position** — fields such as `KVCache.valor`, accessor `valor()`, carrier fields, and receiver calls. These are ledger candidates and target `payload` or a receiver-specific safe name. None targets `value`.
2. **Parameter/local position** — function parameters and locals such as `cast`'s numeric input, gradient construction temporaries, and test locals. These remain `valor` under the member-scoped parameter policy unless incidentally swept by a member declaration/reference rename.
3. **String/comment position** — diagnostic prose, wire literals, comments, and fixture text. These remain byte-for-byte unchanged.

The source receipt contains the exhaustive line evidence used for that classification. `catch err` is a local binding, not a member row; every `catch err` binding remains `err`. Only a `causa` member accessor becomes `message`. `class` is the English rendering of the Faber `genus` keyword, not a user type target. The HIR/typecheck catch and conversion sources were also checked at `radix-hir/src/nodes.rs` and `radix/src/semantic/passes/typecheck/*.rs`; their evidence is retained at `/tmp/gradus-s2-radix-catch.txt`.

## Tensor field/method shape probe

This is the required re-run of the `9678ecd` shape probe. The synthetic input and receipts are retained at:

```text
/tmp/gradus-s2-tensor-shape/shape.fab
/tmp/gradus-s2-tensor-shape/shape.converted.fab
/tmp/gradus-s2-tensor-shape/convert.stderr
/tmp/gradus-s2-tensor-shape/check.stdout
/tmp/gradus-s2-tensor-shape/check.stderr
```

The probe input had one `list<int> shape` field and one `fn shape() → list<int>` method returning `self.shape`. It ran:

```bash
FABER_LIBRARY_HOME=/Users/ianzepp/work/faberlang \
  /tmp/gradus-s2-radix/target/debug/faber convert --to en --stdout \
  /tmp/gradus-s2-tensor-shape/shape.fab \
  > /tmp/gradus-s2-tensor-shape/shape.converted.fab
FABER_LIBRARY_HOME=/Users/ianzepp/work/faberlang \
  /tmp/gradus-s2-radix/target/debug/faber check \
  /tmp/gradus-s2-tensor-shape/shape.converted.fab
```

`convert` exit `0`; `check` exit `0`. The real L1 first-file probe independently accepted the same Tensor shape collapse. Locked result: Tensor field `forma → shape`, Tensor method `figura() → shape()`. `datos → data` is the adjacent Tensor carrier field. This is a field/method namespace collapse, not a facade or alias.

## Member-scoped parameter policy

The following policy is copied from the delivery authority and is locked for all nine rows:

> Gradus adopts the Norma reconciliation in `norma` commit `f7a5cc8` (`docs(factory): reconcile param-rename depth policy`). Pass B renames **members**: functions, types, fields, and private helpers. A parameter is renamed only incidentally when the same spelling is swept by a member rename, and the English spelling comes from the family ledger. Every other Latin parameter is retained by decision, is outside the member guard, and is not a unit done-when. This avoids positional-parameter churn and false positives for words that are also valid English or domain vocabulary. `catch err` bindings are local bindings, not member rows.

A member rename must not leave a same-spelling parameter stale when the declaration/reference sweep necessarily changes it. The sweep must not widen to every Latin parameter in a file. Wire literals, version markers, diagnostic strings, comments, import coordinates, and fixture text are not identifier members and remain unchanged.

## Nine family ledgers

The maps below are the complete S2 member maps. An entry not listed as a rename is already English and retained. Private helper lists are explicit; this prevents the 750-function inventory from hiding helper collisions. Parameter/local names are governed by the policy above, not by these member maps.

### 1. S2-L1 — dtype / shape / tensor / math

**Files**: `src/dtype.{fab,proba}`, `src/shape.{fab,proba}`, `src/tensor.{fab,proba}`, `src/math.{fab,proba}`.

**Types and public members**:

```text
FormaError → ShapeError
causa → message
nomen → name
ex_nomine → from_name
amplitudo → width
serializa → serialize
 deserializa → deserialize
promovet → promote
angusta → narrow
finita → finite
casta → cast
valet → valid
gradus → rank
quantitas → numel
broadcastum → broadcast
reformanda → reshape
expansio → expand
figura → shape
forma (Tensor field) → shape
datos (Tensor field) → data
typus → dtype
accipe → get
structa → construct
structa_typo → construct_dtype
impleta → fill
concatenatio → concatenate
segmentum → slice
summa → sum
media → mean
```

The already-English arithmetic members `add`, `sub`, `mul`, `div`, `neg`, `abs`, `signum`, and `matmul` stay. DType carrier names `DType`, `DTypeError`, and constructors `f32`, `f16`, `i32`, `u8` stay. `TensorError` and `MathError` stay as already-English type names; their `causa` accessors become `message`.

**Private helpers**:

```text
_productus → _product
_dimensio → _dimension
_quantitas_forma → _numel_shape
_forma_broadcast → _shape_broadcast
_quantitas_valid → _numel_valid
_coordinata → _coordinate
_planus_axis → _flat_axis
_typo_par → _dtype_pair
_typus_ex_nomine → _dtype_from_name
```

`_index_broadcast` and `_index_axis` are already-English and stay. Compiler `forma`, `crea`, `formata`, `subtrahe`, `magnitudines`, and `longitudo` implementations are not edited by this row.

**Collision-sensitive fields and receiver decisions**:

```text
Tensor.forma → Tensor.shape
Tensor.datos → Tensor.data
Tensor.figura() → Tensor.shape()
Tensor.gradus() → Tensor.rank()
Tensor.quantitas() → Tensor.numel()
Tensor.typus() → Tensor.dtype()
Tensor.valet() → Tensor.valid()
Tensor.accipe() → Tensor.get()
```

`quantitas → numel` is locked because `size` is the live compiler spelling. `segmentum → slice` is probed as a Gradus method separately from compiler-owned `sectio → slice`.

**Probe receipt**: first file `src/tensor.fab`; `/tmp/gradus-s2-l1/`. `tensor.input.fab` → `tensor.converted.fab` with `convert` exit `0`; renamed `tensor.probe.fab` checked with exit `0`. The map includes the field/method shape collapse, `rank`, `numel`, `dtype`, `get`, `construct`, and `fill`. Import coordinates were protected. `convert.stderr`, `check.stdout`, and `check.stderr` are retained.

**Implementation receipt**: checked. The four source modules and co-located proofs use the row's locked names; compiler-owned `forma`, `crea`, `formata`, `subtrahe`, `magnitudines`, and `longitudo` implementations were not edited. Real-module checks passed with exit `0` for `src/dtype.fab`, `src/shape.fab`, `src/tensor.fab`, and `src/math.fab` under `FABER_LIBRARY_HOME=/Users/ianzepp/work/faberlang`; only existing locale/unused warnings remain. `./scripta/inventory-public-symbols` also passes with the 750 total and L1 counts `dtype=14`, `shape=9`, `tensor=11`, `math=23`. The L1 public-name map is rebased in `docs/api-reference.md`.

### 2. S2-SHARED — parameter / serialize / gradient

**Files**: `src/parameter.{fab,proba}`, `src/serialize.{fab,proba}`, `src/gradient.{fab,proba}`.

**Types and public members**:

```text
Statio → Station
Parametrum → Parameter
ParametrumError → ParameterError
Identitas → Identity
Registrum → Registry
Tensum → SerializedTensor
ParametrumWire → ParameterWire
Gradiente → Gradient
Gradientes → Gradients
GradienteError → GradientError
causa → message
statio_nomen → status_name
nomen → name
nomen_typi → dtype_name
figura → shape
possessor → owner
identia → identity
statio → status
quantitas → numel
valor → payload
muta → mutate
structa → construct
structa_gelida → construct_frozen
numerus → count
contineo → contains
inveni → find
trainabiles → trainable
gelidae → frozen
ordo → order
adscisco → add
identitas_aequus → identity_equal
structa_gradientes → construct_gradients
obsoletus → obsolete
serializa → serialize
deserializa → deserialize
statium → status
```

The existing `SerializeError` type and already-English `simple_loss` stay. `Statio`'s status semantics become `Station`; the wire values `trainable` and `frozen` remain unchanged.

**Private helpers**:

```text
_gelida → _frozen
_structum → _construct
_digitum → _digit
_numerica → _numeric
_habeat_solidum → _has_no_separator
_octeti_lista → _byte_list
_textus_bytes → _text_bytes
_be4_lege → _be4_read
_be8_lege → _be8_read
_caput → _header
_legere_textus → _read_text
_quantitas → _numel
_gradus → _rank
_iunge_datos → _join_data
_divido_datos → _split_data
_tag_a → _tag_from_name
_nomen_a_tag → _name_from_tag
_habeat_solidum → _has_no_separator
```

`_octeti_lista`, `_be4`, `_be8`, `_iunge_datos`, and the other byte helpers are private members even when their target is a mechanical English spelling. `serializa_dtype`, `serializa_shape`, `serializa_tensor`, `serializa_parametrum`, `deserializa_dtype`, `deserializa_shape`, `deserializa_tensor`, and `deserializa_parametrum` become the corresponding `serialize_*`/`deserialize_*` names.

**Collision-sensitive fields**:

```text
Identitas.nomen → name
Identitas.typo → dtype
Identitas.forma → shape
Identitas.versio → version
Identitas.possessor → owner
Parametrum.identitas → identity
Parametrum.statio → status
Parametrum.valor → payload
Tensum.typo → dtype
Tensum.forma → shape
Tensum.datos → data
ParametrumWire.nomen → name
ParametrumWire.possessor → owner
ParametrumWire.typo_nomen → dtype_name
ParametrumWire.forma → shape
ParametrumWire.versio → version
ParametrumWire.statio_nomen → status_name
ParametrumWire.datos → data
Gradiente.valor → payload
```

The post-rename wire field order and literals remain identical. The first-file probe specifically settled `nomen → name`, `typo → dtype`, `valor → payload`, and `causa → message` in member positions.

**Probe receipt**: first file `src/parameter.fab`; `/tmp/gradus-s2-shared/`. `convert` exit `0`; renamed `parameter.probe.fab` checked with exit `0`. The probe preserved the external `gradus:shape` alias and old external Tensor/DType APIs; only Shared members were renamed.

**Implementation receipt**: checked. `src/parameter.fab`, `src/serialize.fab`, and `src/gradient.fab` use the locked Shared names, including `numel`, `payload`, and the private byte-helper targets; wire field order and literals remain unchanged. The annotated `simple_loss` target-lane section is byte-for-byte isolated; the wrapper around it uses the renamed Gradient surface and the landed L1 Tensor/DType/Shape APIs. Real-module `faber check` passed with exit `0` for all three files under `FABER_LIBRARY_HOME=/Users/ianzepp/work/faberlang`; only existing locale/unused warnings remain. `./scripta/inventory-public-symbols` reports the unchanged 750 total and Shared counts `parameter=37`, `serialize=34`, `gradient=13`; the rebased API reference covers every Shared public symbol. The full shared-workspace inventory invocation still reports only public-name coverage gaps from concurrent non-Shared family WIP, with no Shared coverage failures.

### 3. S2-TRAIN — loss / optimize / nn / train / metrics / data

**Files**: `src/loss.{fab,proba}`, `src/optimize.{fab,proba}`, `src/nn.{fab,proba}`, `src/train.{fab,proba}`, `src/metrics.{fab,proba}`, `src/data.fab`.

**Types and public members**:

```text
SgdStatum → SgdState
Passus → StepResult
Schedula → Schedule
Modus → Mode
Semen → Seed
Fructus → Draw
FructusF32 → DrawF32
Excutio → Dropout
Tabula → Checkpoint
Metricum → Metric
causa → message
lentus_vertex → rate_vertex
incalesco → warmup
passus_total → total_steps
lentus_finis → rate_end
structa_schedula → construct_schedule
lentus_schedulata → scheduled_rate
modus_nomen → mode_name
est_disciplina → is_discipline
est_aestimatio → is_estimate
modus → mode
dropout_pars → dropout_probability
structa_semen → construct_seed
valor → payload
semen → seed
proximus → next
proximus_f32 → next_f32
excutio → dropout
serializa_semen → serialize_seed
deserializa_semen → deserialize_seed
aetas → age
passus → step
statum_wire → state_wire
structa_tabula → construct_checkpoint
tabula_aequus → checkpoint_equal
serializa_tabula → serialize_checkpoint
deserializa_tabula → deserialize_checkpoint
accuratezza → accuracy
damnum → loss
metricum → metric
metrica_aequus → metric_equal
structa → construct
lentus → rate
semen → seed
stratorum → layers
dimensio → dimension
adscisco → add
inveni → find
contineo → contains
statum_aequus → state_equal
sgd_aequus → sgd_equal
sgd_vacuum → empty_sgd
novus (Step field/accessor) → fresh
statum (Step field/accessor) → state
serializa_statum → serialize_state
deserializa_statum → deserialize_state
```

`mse`, `cross_entropy`, `linear`, `gelu`, `layernorm`, `rmsnorm`, `silu`, `swiglu`, `train_step_*`, and other already-English public names stay. `OptimizeError`, `NnError`, `TrainError`, and `MetricError` stay unless a later family ledger explicitly names a type correction; their `causa` member becomes `message`.

**Private helpers**:

```text
_quantitas_valid → _numel_valid
_typo_par_duo → _dtype_pair
_typo_f32 → _dtype_f32
_exponens → _exp
_logarithmus → _log
_habeat_solidum → _has_no_separator
_digitum → _digit
_numerica → _numeric
_structum → _construct
_cosinus → _cos
_disciplina → _discipline
_digitum → _digit
_numerica → _numeric
_quantitas_valid → _numel_valid
_typo_par_tres → _dtype_triplet
_typo_par → _dtype_pair
_tanh → _tanh
_radix → _sqrt
_gelu_scalaris → _scalar_gelu
_sigmoidea → _sigmoid
_silu_scalaris → _scalar_silu
_elementa_mul → _mul_elements
```

The optimizer probe also records the collision-safe status/rate targets: `size`, `step`, `name`, `type`, and all frame status names remain reserved. The optimizer's gradient-dependent `passus` section was omitted from the isolated scratch check because the imported `gradient.fab` carries a target-lane annotation; the state, constructor, member, and serialization surface was checked in full. The live package itself was not altered.

**Collision-sensitive fields**:

```text
SgdState.possessor → owner
SgdState.nomen → name
SgdState.versio → version
SgdState.generatio → generation
SgdState.passus → step
SgdState.lentus → rate
Sgd.states (from statia) → states
StepResult.novus → fresh
StepResult.statum → state
Schedule.lentus_vertex → rate_vertex
Schedule.passus_total → total_steps
Schedule.lentus_finis → rate_end
Seed.valor → payload
Seed.semen → seed
Checkpoint.aetas → age
Checkpoint.passus → step
Checkpoint.statum_wire → state_wire
Metric.damnum → loss
Metric.accuratezza → accuracy
```

**Probe receipt**: first file `src/optimize.fab`; `/tmp/gradus-s2-train/`. `convert` exit `0`; source-only optimizer state/serialization probe checked with exit `0`. `gradient` import and the gradient-dependent `passus` block are explicitly recorded in `check.stderr`/this row as the target-lane isolation, not silently treated as product evidence.

**Implementation receipt**: source/proof batch applied. `src/loss.fab`, `src/optimize.fab`, `src/nn.fab`, `src/train.fab`, `src/metrics.fab`, and the co-located Train proofs use the locked row, including `numel`, `payload`, and the reserved `step` member positions; wire literals and diagnostic strings remain unchanged. Real-module `faber check` passed with exit `0` for all six `.fab` modules under `FABER_LIBRARY_HOME=/Users/ianzepp/work/faberlang`; only the existing locale/unused warnings remain. The source declaration inventory remains stable at `loss=11`, `optimize=26`, `nn=24`, `train=41`, `metrics=6`, `data=0` (108 Train declarations; 750 total). The Train public-name map is rebased in `docs/api-reference.md`; the known `shape.fab:4544` PKG001 and later caller/proof integration remain outside this family unit.

### 4. S2-ARCH — attention / transformer

**Files**: `src/attention.{fab,proba}`, `src/transformer.{fab,proba}`.

**Types and public members**:

```text
RopePolitica → RopePolicy
RopeConfigura → RopeConfig
politica_consecutiva → consecutive_policy
politica_interposita → interleaved_policy
politica_nomen → policy_name
politica (RopeConfig field/accessor) → policy
structa_rope_configura → construct_rope_config
causa → message
rotary_position_embedding_configura → rotary_position_embedding_config
```

The already-English `AttentionError`, `TransformerError`, `scaled_dot_product`, `scaled_dot_product_causal`, `scaled_dot_product_causal_rope`, `multi_head_attention`, `base`, `scale`, and `_attention_core` stay. `Transformer._mappa → _map_error`; `Transformer._attentio → _attention` is the mode-selected wrapper; `_linear`, `_gelu`, `_layernorm`, `_add`, `_rmsnorm`, and `_swiglu` are already English. `_multi_attentio → _multi_attention` follows the same private-helper rule. `_softmax` is already English and retained.

**Private helpers**:

```text
_typo_f32 → _dtype_f32
_typo_par → _dtype_pair
_typo_tres → _dtype_triplet
_exponens → _exp
_reduce_angulus → _reduce_angle
_sinus → _sin
_cosinus → _cos
_transpone → _transpose
_impleta → _fill
_interposita → _interleaved
_valida_triplum → _validate_triplet
_valida_rope → _validate_rope
_valida_multi → _validate_multi
_caput → _head
_concilio → _reconcile
_matmul_attentio → _attention_matmul
```

The implementation must choose one stable canonical for the two trigonometric helpers before the Arch batch; the probe used `_sin`/`_cos` and passed. No compiler view or tensor intrinsic is captured by this row.

**Collision-sensitive fields**:

```text
RopeConfig.base → base (retained)
RopeConfig.scale → scale (retained)
RopeConfig.politica → policy
```

`forma`, `figura`, and `typus` occurrences on imported `tensor.Tensor` remain old in this isolated probe; they belong to L1 and are not Arch members.

**Probe receipt**: first file `src/attention.fab`; `/tmp/gradus-s2-arch/`. `convert` exit `0`; renamed attention probe checked with exit `0`. External Tensor/DType/Math APIs and import coordinates were protected.

**Implementation receipt**: source/proof batch applied. `src/attention.fab` checks green with exit `0` under `FABER_LIBRARY_HOME=/Users/ianzepp/work/faberlang`, with only the existing locale/unused warnings; the clean committed-base transformer probe at `/tmp/gradus-s2-arch/transformer-isolated.stderr` also checks green with exit `0`. The live transformer check is currently blocked before Arch diagnostics by `PKG001:library_conflicting_aliases` in the concurrent uncommitted S2-TRAIN `nn` lane; no Arch source error is reported. The Arch declaration inventory remains `attention=35`, `transformer=14` (49 family declarations; total 750), and the final docs/API inventory rebase remains owned by S2-DOCS.

### 5. S2-MODEL — model artifacts and format leaves

**Files**: `src/model/artifact.{fab,proba}`, `capsule.{fab,proba}`, `dense.{fab,proba}`, `dense_llama.{fab,proba}`, `dense_qwen2.{fab,proba}`, `dequant.{fab,proba}`, `gguf.{fab,proba}`, `gguf_manifest.{fab,proba}`, `qwen35moe.{fab,proba}`, `safetensors.{fab,proba}`, `tensor_payload.{fab,proba}`, `tensor_view.{fab,proba}`.

**Types**:

```text
IdentitasContenuti → ContentIdentity
MetadatumSafetensori → SafetensorsMetadata
DescriptioTensorisSafetensori → SafetensorsTensorDescriptor
ManifestumSafetensors → SafetensorsManifest
Manifesta → Manifest
Capsula → Capsule
Identitas → Identity
ConfiguraDensa → DenseConfig
Repertum → Lookup
DensumLlamaError → LlamaError
ArsLlama → LlamaArch
DescriptioCanonica → CanonicalDescriptor
ConfiguraDensaQwen2 → DenseQwen2Config
ScalaMinima → MinScale
CorpusGguf → GgufCorpus
LectioFontis → SourceRead
MetadatumGguf → GgufMetadata
LayoutGgml → GgmlLayout
DescriptioTensorisGguf → GgufTensorDescriptor
ManifestumGguf → GgufManifest
ConfiguratioQwen35moe → Qwen35moeConfig
ErrorConfiguratioQwen35moe → Qwen35moeConfigError
ErrorTensorumQwen35moe → Qwen35moeTensorError
SummaTensoriorumQwen → QwenTensorSummary
TensorCanonicusQwen → QwenCanonicalTensor
ErrorReferentiaeQwen35moe → Qwen35moeReferenceError
AdmissioQwen35moe → Qwen35moeAdmission
ErrorAdmissionisQwen35moe → Qwen35moeAdmissionError
Tokenum → Token
Structura → Structure
Stringum → StringValue
MetaCursus → MetadataCursor
TensorCursus → TensorCursor
NumeriCursus → NumberCursor
CaputCursus → HeaderCursor
VisumTensoris → TensorView
VisioError → ViewError
TensorPayload and PayloadError → retained
```

Already-English `ArtifactError`, `AdmissionError`, `DenseError`, `GgufError`, `GgufManifestError`, `DequantError`, `SafetensorError`, `TensorError`, `TensorPayload`, `PayloadError`, and technical dtype/layout names stay. `FormaError → ShapeError` is the L1 type decision and is not duplicated here.

**Public members**:

```text
causa → message
clavis → key
valor → payload
nomen → name
typo/typus → dtype (dtype-bearing member), kind otherwise
forma/figura → shape
initium → start
finis → end
elementa → elements
formatum → format
versio → version
longitudo_artefacti → artifact_length
longitudo_datorum → data_length
metadatorum_numerus → metadata_count
tensorum_numerus → tensor_count
metadatum → metadata
descriptio → description
manifestum_gguf → gguf_manifest
manifestum_safetensors → safetensors_manifest
schematis → schema
identitas_artificii → artifact_identity
algorithmus → algorithm
digestio → digest
longitudo → length
longitudo_bytes → byte_length
identia → identity
identitas_aequus → identity_equal
structa_manifestum → construct_manifest
verifica → verify
verifica_contra → verify_against
serializa_identitas → serialize_identity
deserializa_identitas → deserialize_identity
praevideo → forward
configura → config
ars_smollm2 → smollm2_arch
layout_nota → layout_note
nomen_gguf → gguf_name
resolvo → resolve
descriptio_render → render_description
elementa_glomoris → block_elements
octeti_glomoris → block_bytes
dequantizas_glomulus → dequantize_block
dequantizas_ordo → dequantize_order
admitto/admissio → admit/admission
inspice → inspect
lege_* → read_*
parse/layout/admit stay
```

`dequant`'s `_byte`, `_le_u16`, `_le_u32`, `_i8`, `_f32le`, `_bfloat16`, and quantization leaf names are already technical/English and stay unless a concrete collision is found. `gguf.admit` remains `admit`; it is not duplicated as `admitto`.

**Private helpers, by file**:

```text
artifact: _digestio_recta → _digest_ok
capsule: _est_hex → _is_hex; _hex_recta → _hex_ok; _est_digitum → _is_digit; _descriptio_recta → _description_ok; _manifestum_recta → _manifest_ok; _parsa → _parse
 dense: _fons → _source; _forma_textus → _shape_text; _forma → _shape; _transpone → _transpose; _collige → _collect; _nullum_bias → _no_bias
 dense_llama: _descriptio → _description
 dense_qwen2: _inveni → _find; _digitorum → _digits; _stratum → _layer; _digiti_numerus → _digit_count; _gguf_suffix → _gguf_suffix (retained); _gguf_nomen → _gguf_name; _textum_factum → _text_value; _numerum_factum → _number_value; _ligatum → _tied
 gguf: _fons → _source; _errorem_manifesti → _manifest_error; _inspice → _inspect; _textus_pacta → _text_value; _numerus_pacta → _number_value; _bivalens_pacta → _bool_value; _continet → _contains; _clavis_pacta → _key_value
 gguf_manifest: _octeti_lista → _byte_list; _octeti_ex_lista → _byte_from_list; _fons_lege → _read_source; _scalar_magnitudo → _scalar_size; _typo_validum → _dtype_valid; _iunge_octeti → _join_bytes; _valorem_fonte → _source_value; _valor_magnitudo → _size_value; _continet → _contains; _digestio_recta → _digest_ok; _identitas_valet → _identity_valid; _metadatum_inveni → _find_metadata; _valor_u16/_valor_i32/_valor_i64/_valor_u32/_valor_u64 → _value_u16/_value_i32/_value_i64/_value_u32/_value_u64; _numerum_scalarum → _scalar_count; _numerum_wire → _wire_count; _valor_textus → _text_value; _layout_blockum → _block_layout; _layout_octeti → _byte_layout; _elementa → _elements; _align → _align; _potentia_duorum → _power_two; _constitue → _construct
 qwen35moe: _clavis_requisita_qwen → _required_qwen_key; _clavis_qwen_ignota → _unknown_qwen_key; _octeti_lista → _byte_list; _potentia_duorum → _power_two; _f32_le → _f32_le; _exige_meta → _require_metadata; _exige_numerum → _require_number; _exige_textum → _require_text; _exige_bool → _require_bool; _exige_longitudo → _require_length; _exige_f32 → _require_f32; _exige_sectiones → _require_sections; _classis_blocki → _block_class; _tensores_globales/_tensores_hybridae/_tensores_plenae/_tensores_nextn → _global_tensors/_hybrid_tensors/_dense_tensors/_nextn_tensors; _canonici_blocki → _canonical_block; _inveni → _find; _exige → _require; _refer_inveni → _find_reference; _refer_dim → _reference_dim; _refer_gradu → _reference_rank; _refer_unum → _reference_one; _refer_ffn → _reference_ffn; _refer_hybrida → _reference_hybrid; _refer_plena_core → _reference_dense_core; _admitto_parse → _parse_admission; _architectura_lecta → _read_architecture; _typus_ignotus_primus → _first_unknown_dtype; _admitto_congela → _freeze_admission; _admitto_tensores → _admit_tensors; _admitto_referantia → _admit_references
 safetensors: _est_digitum → _is_digit; _est_hex → _is_hex; _est_sponte → _is_optional; _hex_recta → _hex_ok; _caput → _header; _lege_string → _read_string; _lege_number → _read_number; _scander → _scan; _typo → _dtype; _valor → _value; _parsa_integrum → _parse_integer; _parsa_numerorum → _parse_numbers; _parsa_meta → _parse_metadata; _parsa_tensoris → _parse_tensor; _perambulare → _walk; _metadatorum → _metadata; _meta_quaero → _metadata_get; _meta_exige → _metadata_require; _inveni_nomen → _find_name; _quantitas → _numel; _formae_aequae → _shapes_equal
 tensor_payload: retained `causa → message`
 tensor_view: _descriptio → _description; _limes → _limit; vincula → links; _fons_lege → _read_source; materializa_slicem → materialize_slice; materializa_glomulum → materialize_block
```

The remaining private `.fab` helpers are explicitly retained or mapped as follows:

```text
attention._softmax → _softmax (retained)
dequant._dimidium → _half
dequant._dequant_q8_0/_dequant_q5_0/_dequant_q4_k/_dequant_q5_k/_dequant_q6_k/_dequant_f32/_dequant_bf16 → same technical names
dequant._scala_minima_k4 → _min_scale_k4
gguf_manifest._stringa → _string
gguf_manifest._u8val → _u8_value
safetensors._le8 → _le8 (retained)
sampling._top_k/_top_p/_min_p/_softmax → same technical names
```

The co-located `.proba` helper functions are proof-private, not public Gradus members. They are included in the family write scope and are swept with the same family lexicon: `*_resultum → *_result`, `*_fragmentum/fragmenta → *_fragment/*_fragments`, `*_tensores/tensorum → *_tensors`, `*_numerum → *_number`, `*_longitudo → *_length`, `*_typo → *_dtype`, `*_encoda → *_encode`, `*_decoda → *_decode`, `*_scanna → *_scan`, `*_inspice → *_inspect`, `*_lectio → *_read`, `*_congela → *_freeze`, `*_admissio → *_admission`, and `*_appende → *_append`. Technical fixture stems (`corpus`, `bytes`, `tokens`, `eog`, `chat`, `template`, `qwen35moe`, `llama`) remain technical names. This rule covers every private helper declaration in the 32 co-located `.proba` files without expanding the public inventory or parameter guard.

The implementation must use exact identifier-boundary replacements. It must not rename qualified external `artifact.*`/`manifestum.*` fields while the Model row is still transitional.

**Collision-sensitive fields**:

```text
IdentitasContenuti.algorithmus → algorithm
IdentitasContenuti.digestio → digest
IdentitasContenuti.longitudo → length
MetadatumSafetensori.clavis → key
MetadatumSafetensori.valor → payload
DescriptioTensorisSafetensori.nomen → name
DescriptioTensorisSafetensori.typo → dtype
DescriptioTensorisSafetensori.forma → shape
DescriptioTensorisSafetensori.initium/finis → start/end
DescriptioTensorisSafetensori.elementa → elements
Capsula.schema/identitas/manifestum → schema/identity/manifest
Capsula.longitudo_bytes → byte_length
DescriptioTensorisGguf.nomen/forma/typo_ggml → name/shape/dtype_ggml
ManifestumGguf.longitudo_artifacti → artifact_length
ManifestumGguf.metadata/tensores → metadata/tensors
ConfiguraDensa.strata/capita/capita_kv → layers/heads/kv_heads
ConfiguraDensa.dimensio_capitis/dimensio_occulta/vocabulum/ligatum → head_dim/hidden_dim/vocab/tied
ArsLlama.strata/capita/capita_kv/dimensio_capitis/dimensio_occulta/vocabularia/nexa_immortalia → layers/heads/kv_heads/head_dim/hidden_dim/vocab/tied
TensorCanonicusQwen.nomen/forma/typo_ggml → name/shape/dtype_ggml
VisumTensoris.nomen/forma/typo_ggml → name/shape/dtype_ggml
TensorPayload.nomen/initium_absolutum/longitudo → name/absolute_start/length
```

Model wire keys, hashes, offsets, schema markers, admission constants, error strings, and serialized field order remain unchanged. The Model probe settled `valor → payload`, `nomen → name`, `forma → shape`, `longitudo → length`, and `causa → message` in the actual capsule receiver positions.

**Probe receipt**: first file `src/model/capsule.fab`; `/tmp/gradus-s2-model/`. `convert` exit `0`; renamed capsule probe checked with exit `0`. The qualified imported `artifact.IdentitasContenuti` and `manifestum.ManifestumGguf` names were kept on their live pre-S2 surface.

**Family-unit receipt (`f50fbbfb`)**: the twelve `.fab` modules and matching `.proba` proof surfaces were swept with the locked member-scoped mappings. `faber check` is green for eleven model source leaves; `dense.fab` reproduces the pre-existing `PKG001:library_conflicting_aliases` diagnostic at `src/shape.fab:4544` even when checked from a clean `git archive HEAD` library, so no foreign-family fix was absorbed here. The required inventory run remains structurally stable at **750** declarations, including **234** model declarations; API-reference coverage failures are the later S2-DOCS chase, not a model-source failure. Wire literals, hashes, format keys, admission constants, and diagnostic strings were byte-for-byte preserved.

### 6. S2-TOKENIZER — tokenizer

**File**: `src/tokenizer.{fab,proba}`.

**Types and public members**:

```text
Tokenizator → Tokenizer
IdentitasTokenizator → TokenizerIdentity
CategoriaUnicode → UnicodeCategory
causa → message
schematis → schema
progenies → merge_kind
pre_tokenizator → pre_tokenizer
digestio_vocabuli → vocab_digest
bos_vacua → bos_free
spatium_vacua → space_free
structa → construct
verifica_proba → verify_probe
pinnata_proba → pinned_probe
proba_aequa → probe_equal
proba_ida → probe_id
clavis_tokenizatoris → tokenizer_key
serializa_identitas → serialize_identity
deserializa_identitas → deserialize_identity
fabricare → build
encoda → encode
decoda → decode
categoria → category
categoria_nomen → category_name
scanna_verba → scan_words
redde_turnum_user → render_user_turn
est_littera/est_signum/est_numerus/est_spatium/est_novum_linea/est_aliud → is_letter/is_symbol/is_number/is_space/is_newline/is_other
```

`eog`, `add_bos`, `chat_template`, `top_k`, and other technical members retain their existing spellings. The `test`/`print`/`name`/`value` set remains reserved.

**Private helpers**:

```text
_est_hex → _is_hex
_hex_recta → _hex_ok
_est_digitum → _is_digit
_eog_recta → _eog_ok
_id_in_ambitu → _id_in_range
_codicillus_ex_octeto → _code_from_byte
_octetus_ex_codicillo → _byte_from_code
_textus_ex_octeti → _text_from_bytes
_textus_ex_codicillo → _text_from_code
_codicillus_ex_vestigio → _code_from_trace
_octeti_numeri → _number_bytes
_vestigium_ex_octeto → _trace_from_byte
_textum_artificii → _artifact_text
_textorum_artificii → _artifact_texts
_typi_artificii_optativa → _artifact_optional_types
_par_recta → _pair_ok
_bpe_coagmenta → _bpe_merge
_in_tabula → _in_table
_nomen_categoriae → _category_name
_codicilli_textus → _text_codes
_codicillus_littera/_signum/_numerus/_spatium/_linea/_album/_aliud/_parvus → _letter_code/_symbol_code/_number_code/_space_code/_newline_code/_blank_code/_other_code/_small_code
_verba_ex_codicillis → _words_from_codes
_inveni → _find
_encoda_verborum → _encode_words
_in_nomine → _in_name
_ordo_surgens → _sort_ascending
_fim_artificii → _artifact_end
_eog_artificii → _artifact_eog
_add_bos_artificii → _artifact_add_bos
_chat_template_artificii → _artifact_chat_template
```

**Collision-sensitive fields**:

```text
IdentitasTokenizator.progenies → merge_kind
IdentitasTokenizator.pre_tokenizator → pre_tokenizer
IdentitasTokenizator.digestio_vocabuli → vocab_digest
IdentitasTokenizator.bos_vacua/spatium_vacua → bos_free/space_free
Tokenizator.verborum/vocabulum/concursus/specialia_textus/specialia_ids/eog/add_bos/chat_template/multitudo → retained technical fields except where the ledger names a member
```

The first default `progenies → merges` was rejected by the live first-file probe: `build` already has a local `merges` list in the same function scope, so the target produced `SEM005:duplicate_definition`. The collision-safe and semantic target is `merge_kind` because this field stores the tokenizer kind (`gpt2`), not the merge list. This is the required concrete collision surprise and is now locked.

**Probe receipt**: first file `src/tokenizer.fab`; `/tmp/gradus-s2-tokenizer/`. `convert` exit `0`; the collision-safe `merge_kind` rename probe checked with exit `0`. The failed intermediate `merges` attempt and its `SEM005` receipt are retained at `/tmp/gradus-s2-tokenizer/tokenizer.merges-collision.fab` and `/tmp/gradus-s2-tokenizer/collision-merges.stderr`; the final receipt is green.

### 7. S2-INFERENCE — cache / decode / sampling / generation

**Files**: `src/cache.{fab,proba}`, `src/decode.{fab,proba}`, `src/sampling.{fab,proba}`, `src/generation.{fab,proba}`.

**Types and public members**:

```text
IdentitasCache → CacheIdentity
Pondera → Weights
Decodere → Decoder
Sessio → Session
Cancelatum → Cancellation
Configura → Config
Sortitio → Sampler
GeneratioConfigura → GenerationConfig
GenereCursor → GenerationCursor
causa → message
versio_modelis → model_version
configuratio → config
tokenizator → tokenizer
historia → history
stratorum → layers
typo → dtype
ordinatio → layout
clavis → key
valor → payload
versio → version
dimensio → dimension
longitudo → length
appende → append
redintegra → reset
positio → position
cache_aequus → cache_equal
cache_vacua → empty_cache
identitas_cache_aequus → cache_identity_equal
identitas_cache → cache_identity
serializa_identitas → serialize_identity
deserializa_identitas → deserialize_identity
structa_pondera → construct_weights
structa_decodere → construct_decoder
praefundere → prefill
progredere → advance
cancellata → cancelled
cancelatum_fresh → fresh_cancellation
cancelatum_cancellata → cancellation_cancelled
observa_cancellationem → observe_cancellation
sessio_fresh → fresh_session
mensa → table
pondera → weights
projectio → projection
scala → scale
vocabulum → vocabulary
contextus → context
redintegra → reset
```

Sampling and generation members:

```text
poena_repetitionis → repetition_penalty
structa_configura → construct_config
temperatura → temperature
semen → seed
maxima → max
distributio → distribution
sors → sample
generatio_aequus → generation_equal
structa_generatio → construct_generation
generatio_defecta → generation_failure
imperia_subsidia → support_flags
imperium_admissum → admitted_features
configura → config
serializa_generatio → serialize_generation
deserializa_generatio → deserialize_generation
sessio → session
prolata → emitted
cursor_fresh → fresh_cursor
verbum_licet → token_allowed
cursor_progredere → cursor_advance
cursor_redintegra → cursor_reset
```

Already-English sampling controls (`top_k`, `top_p`, `min_p`, `temperature`-style names), `KVCache`, `CacheError`, and decoder technical tensor slots stay.

**Private helpers**:

```text
_tense → _tensor
_accipe → _get
_habeat_solidum → _has_no_separator
_digitum → _digit
_numerica → _numeric
_tensor_aequus → _tensor_equal
_immersio → _embedding
_bloccum → _block
_projicere → _project
_mappa_sampling → _sampling_map
_exponens → _exp
_index_max → _max_index
_index_max_pars → _max_index_pair
_finita → _finite
_masks_falsa → _mask_false
_siste_bivalens → _binary
_siste_f32 → _f32
_poena_repetitionis → _repetition_penalty
_scala_temperatura → _temperature_scale
_renorma_maske → _renormalize_mask
_distributio → _distribution
_digitum → _digit
_numerica → _numeric
```

**Collision-sensitive fields**:

```text
KVCache.stratorum/typo/ordinatio/clavis/valor/versio/dimensio → layers/dtype/layout/key/payload/version/dimension
IdentitasCache.versio_modelis/configuratio/tokenizator/historia/positio/stratorum/typo/ordinatio → model_version/config/tokenizer/history/position/layers/dtype/layout
Pondera and Decoder carrier fields use the same `weights`, `projection`, `scale`, `vocabulary`, `context`, and `dimension` targets listed above.
GenerationConfig.contextus/magna_promptus/maxima_verborum/semen/poena_repetitionis → context/max_prompt/max_tokens/seed/repetition_penalty
GenerationCursor.sessio/prolata → session/emitted
```

`longitudo → length` is a receiver-specific Gradus method decision; no scalar interval implementation changes. `valor → payload` is required because `value` is a reserved type.

**Probe receipt**: first file `src/cache.fab`; `/tmp/gradus-s2-inference/`. `convert` exit `0`; renamed cache probe checked with exit `0`. External Tensor APIs stayed old in this isolated probe.

### 8. S2-FACADE — facade and callers

**File**: `src/gradus.{fab,proba}` plus the later in-repo caller chase.

```text
causa → message
_mappa → _map_error
```

`GradusError`, `forward_mlp`, `forward_mlp_loss`, `_linear`, `_gelu`, and `nil` stay. The facade error variants keep their semantic identities; their payload field/accessor is `message`. Imports remain `gradus:*`. No new facade genus is introduced.

**Probe receipt**: first file `src/gradus.fab`; `/tmp/gradus-s2-facade/`. `convert` exit `0`; source-only facade error/helper surface checked with exit `0`. The target-lane annotated `forward_mlp_loss` tail was omitted from this isolated source probe because direct scratch checking has no package target lane; that target-lane surface remains covered by the normal package gate in the owning family. This is recorded, not hidden.

### 9. S2-DOCS — docs / inventory / compatibility rebase

**Source boundary**: no source first file. This row runs only after the eight source probes and all family ledgers are closed. It rebases `docs/api-reference.md`, `docs/module-map.md`, compatibility policy, inventory, and source guards from the committed family maps. It does not rename product source.

**Ledger rule**:

```text
The docs row consumes the exact final maps above.
The inventory row changes only after the final live tree exists.
The source guard is member-scoped and excludes retained parameters/comments/strings.
The compatibility record says clean break, no aliases, no [[library_members]], and no sibling-repo migration.
```

Retained Latin parameters such as `via`, `nomen` when not a member, `partes`, `clavis`, and `initium` remain outside the member guard under the policy above.

**No-source probe receipt**: `/tmp/gradus-s2-docs/`. The synthetic representative API smoke input contains final `name`, `payload`, `shape`, and `message` field/method positions. It ran `convert --to en --stdout` with exit `0` and `faber check` with exit `0`. This is explicitly a no-source docs/inventory smoke receipt, not a claim that docs have already been rebased.

## Probe order and receipts

All nine receipts ran before any S2 source batch. The common command shape was:

```bash
FABER_LIBRARY_HOME=/Users/ianzepp/work/faberlang \
  /tmp/gradus-s2-radix/target/debug/faber convert --to en --stdout INPUT.fab \
  > CONVERTED.fab
# apply only the row's scratch old→new map to CONVERTED.fab
FABER_LIBRARY_HOME=/Users/ianzepp/work/faberlang \
  /tmp/gradus-s2-radix/target/debug/faber check PROBE.fab
```

| Order | Family | First file / probe | Convert | Check | Result |
| ---: | --- | --- | ---: | ---: | --- |
| 1 | L1 | `src/tensor.fab` / `/tmp/gradus-s2-l1/` | 0 | 0 | unblocked |
| 2 | Shared | `src/parameter.fab` / `/tmp/gradus-s2-shared/` | 0 | 0 | unblocked |
| 3 | Train | `src/optimize.fab` / `/tmp/gradus-s2-train/` | 0 | 0 | unblocked; gradient target-lane section isolated and recorded |
| 4 | Arch | `src/attention.fab` / `/tmp/gradus-s2-arch/` | 0 | 0 | unblocked |
| 5 | Model | `src/model/capsule.fab` / `/tmp/gradus-s2-model/` | 0 | 0 | unblocked |
| 6 | Tokenizer | `src/tokenizer.fab` / `/tmp/gradus-s2-tokenizer/` | 0 | 0 | unblocked after `merges` collision was resolved to `merge_kind` |
| 7 | Inference | `src/cache.fab` / `/tmp/gradus-s2-inference/` | 0 | 0 | unblocked |
| 8 | Facade | `src/gradus.fab` / `/tmp/gradus-s2-facade/` | 0 | 0 | unblocked; backward target-lane tail isolated and recorded |
| 9 | Docs/inventory | no source / `/tmp/gradus-s2-docs/` | 0 | 0 | unblocked; synthetic API smoke only |

The required `git diff --check` was run on the completed ledger before commit. The probe directories contain the input copy, converted output, rename result, and compiler stdout/stderr receipts. No source tree was used as a scratch write target.

## Collision surprises and locked findings

1. **Tokenizer `progenies → merges` collided.** `build` already declares a local `merges` list, so the first literal target produced `SEM005:duplicate_definition`. The field stores the tokenizer kind, so `progenies → merge_kind` is the semantic non-colliding target. The final probe is green.
2. **Tensor field/method collapse is legal.** The re-run of the `9678ecd` probe and the real Tensor first-file probe both accept a `shape` field plus `shape()` method. No facade is needed.
3. **`size` is not available for Gradus `quantitas`.** The live pack owns `size` through `magnitudo`; the locked target is `numel`.
4. **`value` is not available for Gradus `valor`.** The live pack owns `value` as a type; carriers use `payload`.
5. **`tranzone` is not a live Radix tensor key.** The verified key is `transpone`; this ledger does not invent a `tranzone` collision.
6. **Direct scratch checks of target-lane annotations are not package checks.** The Train gradient-dependent `passus` block and Facade backward-annotated tail were isolated only in their scratch copies. Their isolation is explicit in the receipts; no product code was weakened or changed.

All nine S2 family rows are now unblocked for their ordered implementation units.