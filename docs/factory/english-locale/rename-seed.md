# Rename seed — Pass B identifier map

**Status**: planned — reserved names locked; remaining rows are defaults until S2 starts
**Pass A does not apply this file.** Pass A only rewrites locale-pack vocabulary.

## How to use

1. Pass A lands first. After it, code looks like `fn figura() → list<int>`.
2. Before a Pass B family starts, copy the relevant rows into that family’s
   delivery spec and lock any still-open default.
3. Apply the rename in source, `.proba`, exempla, tests, and the api-reference
   section for that module in the same logical change (or immediately after).
4. Never rename to a reserved escape. Probe `faber check` on the first file
   of each family before batching.

## Reserved — do not use these English spellings

These are English pack keywords or types. Tela already proved `fn value`
is `SEM005`.

| Latin identifier | Illegal English | Locked escape | Why |
| --- | --- | --- | --- |
| `valor` (method) | `value` | `payload` on tensor-ish carriers; `get` only if there is no existing `get` | en type `valor = "value"` |
| `typus` / `typo` (method) | `type` | `dtype` on `Tensor`; `kind` elsewhere | en keyword `typus = "type"` |
| `gradus` (method) | — | `rank` | library name; `rank` is the tensor meaning |
| any new fn | `class`, `enum`, `union`, `fn`, `let`, `return`, `match`, `self`, `optional`, `public`, `private`, `import`, `from`, `as`, `main`, `print`, `test` | pick a non-keyword | en `[keywords]` |
| any new type name | `string`, `int`, `bool`, `float`, `list`, `map`, `set`, `bytes`, `value`, `void`, `null` | qualify (`TensorError`, `ShapeError`) | en `[types]` |

`causa` → `message` is legal. `forma` → `shape` is legal. `figura` → `shape`
is legal only when it does not collide with a field also named `shape` on
the same genus — `Tensor` has field `forma` and method `figura()`; after
rename they should be one `shape` field plus a `shape()` getter, or the
getter should stay only if the field is private. Default: field `shape`,
method `shape()`.

## Already English — do not invent Latin-looking replacements

Keep: `Tensor`, `DType`, `linear`, `gelu`, `layernorm`, `rmsnorm`, `silu`,
`swiglu`, `mse`, `cross_entropy`, `scaled_dot_product`, `parse`, `layout`,
`admit` (gguf), `CacheError`, `DenseError`, and other already-English
type/function names. Pass B is not a style pass over English names.

## Seed map — shared verbs

| Latin | English | Notes |
| --- | --- | --- |
| `causa` | `message` | every `*Error` accessor; diagnostic strings are already English |
| `structa` | `construct` | shared constructor; already-English `tensor`/`cache` names stay |
| `verifica` | `verify` | |
| `serializa_*` | `serialize_*` | |
| `deserializa_*` | `deserialize_*` | |
| `aequus` / `*_aequus` | `equal` / `*_equal` | |
| `valet` | `valid` | predicate; not `is_valid` unless a family already uses `is_` |
| `accipe` | `get` | user method; lista intrinsic `accipe` already becomes `get` in Pass A |
| `appende` | `append` | |
| `inveni` | `find` | |
| `admitto` | `admit` | qwen35moe; gguf already has `admit` |
| `congela` | `freeze` | config freeze from manifest |
| `praevideo` | `forward` | dense model assembly |
| `redintegra` | `reset` | cache / cursor |
| `inspice` | `inspect` | |
| `lege_*` | `read_*` | |
| `textum` / `textorum` | `text` / `texts` | manifest accessors |
| `numerum` / `numerorum` | `number` / `numbers` | |
| `boleanum` | `boolean` | |
| `metadatum` | `metadata` | |
| `identitas` | `identity` | |
| `accuratezza` | `accuracy` | |
| `passus` | `step` | optimizer / train |
| `lentus` | `rate` | learning rate; or `learning_rate` if a family wants the long form |
| `semen` | `seed` | |
| `stratorum` | `layers` | |
| `dimensio` | `dimension` | |
| `clavis` | `key` | cache K; also metadata key |
| `nomen` | `name` | field; `nomen` is also an en-pack annotation key — probe before renaming call sites that are annotations |
| `datos` | `data` | |
| `forma` | `shape` | |
| `figura` | `shape` | see Tensor note above |
| `quantitas` | `size` | element count; en keyword `magnitudo = "size"` is a keyword, not a type — probe `fn size()` |
| `longitudo` (user method) | `length` | Pass A already maps the lista intrinsic |

`quantitas` → `size` needs a one-file probe. If `fn size()` collides with
the `size` keyword (`magnitudo`), lock `numel` or `element_count` instead.

## Seed map — types

| Latin | English |
| --- | --- |
| `Capsula` | `Capsule` |
| `Identitas` | `Identity` |
| `IdentitasContenuti` | `ContentIdentity` |
| `IdentitasCache` | `CacheIdentity` |
| `IdentitasTokenizator` | `TokenizerIdentity` |
| `Tokenizator` | `Tokenizer` |
| `ManifestumGguf` | `GgufManifest` |
| `ManifestumSafetensors` | `SafetensorsManifest` |
| `MetadatumGguf` | `GgufMetadata` |
| `DescriptioTensorisGguf` | `GgufTensorDescriptor` |
| `DescriptioTensorisSafetensori` | `SafetensorsTensorDescriptor` |
| `CorpusGguf` | `GgufCorpus` |
| `LectioFontis` | `SourceRead` |
| `VisumTensoris` | `TensorView` |
| `VisioError` | `ViewError` |
| `Manifesta` | `Manifest` |
| `FormaError` | `ShapeError` |
| `Parametrum` | `Parameter` |
| `ParametrumError` | `ParameterError` |
| `ParametrumWire` | `ParameterWire` |
| `Registrum` | `Registry` |
| `Gradiente` / `Gradientes` / `GradienteError` | `Gradient` / `Gradients` / `GradientError` |
| `Metricum` | `Metric` |
| `Tabula` | `Checkpoint` |
| `Schedula` | `Schedule` |
| `Semen` | `Seed` |
| `Fructus` / `FructusF32` | `Draw` / `DrawF32` |
| `Excutio` | `Dropout` |
| `Modus` | `Mode` |
| `SgdStatum` | `SgdState` |
| `Passus` | `Step` |
| `Configura` | `Config` |
| `ConfiguraDensa` | `DenseConfig` |
| `ConfiguratioQwen35moe` | `Qwen35moeConfig` |
| `RopeConfigura` | `RopeConfig` |
| `RopePolitica` | `RopePolicy` |
| `GeneratioConfigura` | `GenerationConfig` |
| `GenereCursor` | `GenerationCursor` |
| `Decodere` | `Decoder` |
| `Pondera` | `Weights` |
| `Sessio` | `Session` |
| `Cancelatum` | `Cancellation` |
| `Sortitio` | `Sampler` |
| `Tensum` | `SerializedTensor` |
| `Statio` | `Station` |
| `ArsLlama` | `LlamaArch` |
| `DescriptioCanonica` | `CanonicalDescriptor` |
| `Repertum` | `Lookup` |
| `AdmissioQwen35moe` | `Qwen35moeAdmission` |
| `SummaTensoriorumQwen` | `QwenTensorSummary` |
| `TensorCanonicusQwen` | `QwenCanonicalTensor` |
| `CategoriaUnicode` | `UnicodeCategory` |
| `ScalaMinima` | `MinScale` |
| `LayoutGgml` | `GgmlLayout` |

Error type names that are already English (`TensorError`, `MathError`,
`GgufError`, …) stay. Latin-only error names follow the type they wrap
(`ErrorConfiguratioQwen35moe` → `Qwen35moeConfigError`).

## Seed map — Tensor (L1 proof row)

After Pass A the live surface is still Latin names on English keywords:

```text
class Tensor {
    dtype.DType dtype
    list<int> forma
    list<f32> datos
    fn figura() → list<int>
    fn rank-method is still named gradus()
    fn quantitas() → int
    fn typus() → dtype.DType
    fn valet() → bool
    fn accipe(list<int> indices) → f32
}
```

Locked L1 target:

| Current | Target |
| --- | --- |
| field `forma` | `shape` |
| field `datos` | `data` |
| `figura()` | `shape()` |
| `gradus()` | `rank()` |
| `quantitas()` | probe `numel()` if `size()` is illegal; else `size()` |
| `typus()` | `dtype()` |
| `valet()` | `valid()` |
| `accipe()` | `get()` |
| `FormaInvalida` | `InvalidShape` |
| `ElementaMismatch` | `ElementMismatch` |
| `TerminusExcedit` | `IndexOutOfBounds` |

## What Pass A already changes (do not list as Pass B)

These become English in S1 via the pack. Leave them alone in S2.

Keywords: `fn`, `class`, `union`, `enum`, `type`, `const`, `let`, `var`,
`import`, `from`, `as`, `public`, `private`, `optional`, `return`, `if`,
`else`, `elif`, `then`, `for`, `while`, `match`, `case`, `break`,
`continue`, `throw`, `catch`, `do`, `assert`, `panic`, `true`, `false`,
`null`, `and`, `or`, `not`, `is`, `self`, `main`, `print`, `test`, …

Types: `string`, `int`, `bool`, `float`, `list`, `bytes`, `void`,
`unknown`, `tuple`, `value` (the type), …

Intrinsics (receiver methods on std types): `length`, `contains`, `get`,
and the rest of `en` `[intrinsics]`. A Gradus method that currently shares
a Latin intrinsic spelling (`longitudo` on `KVCache`) stays Latin through
Pass A and is renamed in Pass B.

## Probe list before each family

Run on the first converted file of the family:

```bash
"$FABER_BIN" check --locale en path/to/file.fab
```

After the package locale flip, drop `--locale en`. Extra probes when the
family introduces: `fn size()`, `fn name()`, `fn value`-like escapes,
annotation `@ public` / `@ radix backward`.
