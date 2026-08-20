# Gradus diagnostics map

**Document**: `gradus-diagnostics v1.0.0`
**Campaign unit**: PML6-U2
**Status**: structural (live `src/**/*.fab` surface; no executed-tier claim)
**Scope**: every public typed error `discretio` — code + message + resolution

## Contract

- **Code** = `ErrorType.Variant`. Stable identity is the `discretio` case name. Codes do not change without a named compatibility note.
- **Message** = the `text message` on the variant, rendered by `message(e)`. Messages are locale-ready English. Dynamic suffixes (appended names, versions, counts) are written as a trailing `…` when the live source concatenates.
- **Resolution** = the closed action that makes the call succeed. Gradus fails closed — no silent coercion.
- **Reserved / mapped variants**: some variants exist for cross-module mapping or class coverage and have no direct `iace finge "…"` literal site; they still have stable codes. Mapped facades (e.g. `GradusError`, `TransformerError`) preserve the underlying message text.
- **Executed tier**: this map documents fail-closed identity on the compiled surface. Focused `faber test` proba execution and broader inference exempla remain on the FMIR lever (CTO8-1); the separate GGUF-A1b synthetic and real-file inspection receipts are recorded in their exemplar READMEs and are not model-execution or inference claims. REF-01-U1.9 (`exempla/dense-prefill-smollm2`) did not reach Gradus typed diagnostics: FINAL rebuilt packet `faber` at radix `2ed9914e4` / faber `b1adfc9` (CODEGEN001/E0432/PKG001 `processus:exi` cleared), then rustc failed the emitted crate (258 errors; first: `cast cannot be followed by a method call`). REF-01-U1.10 (`exempla/dense-prefill-qwen2`) did not reach Gradus typed diagnostics: FINAL rebuilt packet `faber` at radix `2ed9914e4` (PKG001 `processus:exi` closed) and rust-target emit reached cargo, which failed rustc 248 errors (first `E0015` const `vec!` for `PINNED_TOKENS`). Prior stops: PKG001 at `3853d4b8f`; E0432 at `b919052f0`; compiler `CODEGEN001` (`dense_qwen2.fab`, definition id 4127). Those are Faber/rustc diagnostics, not a `DenseError` / `DenseQwen2Error` variant.

## EOG identity — `TokenizerError.BadEog`

EOG-set mismatch is **tokenizer identity**, not a value error (correctness wave `2cdc498` / `6cc0eb5` / capsule exact pin `{0,2}`).

| Code | Live messages | Resolution |
| --- | --- | --- |
| `TokenizerError.BadEog` | `malformed EOG set`<br>`EOG set does not match the pinned row: …`<br>`pinned row is BOS-free (add_bos_token = false)` / `pinned row is BOS-free`<br>`pinned row is space-prefix-free (add_space_prefix = false)` / `pinned row is space-prefix-free` | Admit the **exact** pinned EOG set `{0,2}` (wire form `"0,2"`, strictly ascending non-negative ids). A well-formed-but-different set is a **different tokenizer**. BOS / space-prefix polarity: pinned row is BOS-free and space-prefix-free — `bos_vacua` and `spatium_vacua` must be `verum` (guards use `≡` against the falsum add-* flags). |

The schema-2 capsule (A1C-M1) no longer carries tokenizer identity — EOG
identity lives in `gradus:tokenizer` (`TokenizerError.BadEog`) and in the
per-format admission entries' own tokenizer checks; it does not surface as
an `AdmissionError` variant.

Generation stop-policy binds the same identity via `tokenizer.is_eog` (admitted EOG tokens `{0, 2}`): the default generate / generate_cancelled / generate_dense routes terminate after the **first** admitted EOG token; `max_tokens` is a ceiling, never a promise to emit that many tokens (`0d50d60`). The additive `StopPolicy` argument on `generate_with_stop` / `generate_cancelled_with_stop` / `generate_dense_with_stop` keeps that default as `Eog`. `IgnoreEos` is the llama.cpp `ignore_eos` row: admitted EOG ids are suppressed from sampling (finite large-negative mask) and the loop runs to the `max_tokens` ceiling.

Pinned proba messages (do not drift):

```text
malformed EOG set
EOG set does not match the pinned row: 1,5
pinned row is BOS-free (add_bos_token = false)
pinned row is space-prefix-free (add_space_prefix = false)
```

## Index of error types

| Module | Error type | Variants | Source |
| --- | --- | ---: | --- |
| `gradus:attention` | `AttentionError` | 11 | `src/attention.fab` |
| `gradus:cache` | `CacheError` | 8 | `src/cache.fab` |
| `gradus:decode` | `DecodeError` | 11 | `src/decode.fab` |
| `gradus:dtype` | `DTypeError` | 4 | `src/dtype.fab` |
| `gradus:generation` | `GenerationError` | 7 | `src/generation.fab` |
| `gradus:gradient` | `GradienteError` | 2 | `src/gradient.fab` |
| `gradus:gradus` | `GradusError` | 8 | `src/gradus.fab` |
| `gradus:loss` | `LossError` | 9 | `src/loss.fab` |
| `gradus:math` | `MathError` | 11 | `src/math.fab` |
| `gradus:metrics` | `MetricError` | 7 | `src/metrics.fab` |
| `gradus:model/artifact` | `ArtifactError` | 3 | `src/model/artifact.fab` |
| `gradus:model/capsule` | `AdmissionError` | 6 | `src/model/capsule.fab` |
| `gradus:model/dense_llama` | `DensumLlamaError` | 4 | `src/model/dense_llama.fab` |
| `gradus:model/dequant` | `DequantError` | 4 | `src/model/dequant.fab` |
| `gradus:model/gguf` | `GgufError` | 10 | `src/model/gguf.fab` |
| `gradus:model/gguf_manifest` | `GgufManifestError` | 12 | `src/model/gguf_manifest.fab` |
| `gradus:model/safetensors` | `SafetensorError` | 11 | `src/model/safetensors.fab` |
| `gradus:model/tensor_payload` | `PayloadError` | 3 | `src/model/tensor_payload.fab` |
| `gradus:model/tensor_view` | `VisioError` | 7 | `src/model/tensor_view.fab` |
| `gradus:model/dense_qwen2` | `DenseQwen2Error` | 5 | `src/model/dense_qwen2.fab` |
| `gradus:model/dense` | `DenseError` | 4 | `src/model/dense.fab` |
| `gradus:nn` | `NnError` | 9 | `src/nn.fab` |
| `gradus:optimize` | `OptimizeError` | 14 | `src/optimize.fab` |
| `gradus:parameter` | `ParametrumError` | 10 | `src/parameter.fab` |
| `gradus:sampling` | `SamplingError` | 3 | `src/sampling.fab` |
| `gradus:serialize` | `SerializeError` | 6 | `src/serialize.fab` |
| `gradus:shape` | `FormaError` | 6 | `src/shape.fab` |
| `gradus:tensor` | `TensorError` | 3 | `src/tensor.fab` |
| `gradus:tokenizer` | `TokenizerError` | 14 | `src/tokenizer.fab` |
| `gradus:train` | `TrainError` | 10 | `src/train.fab` |
| `gradus:transformer` | `TransformerError` | 12 | `src/transformer.fab` |

**Total**: 228 public error codes across 30 error types.

## `gradus:model/artifact` — `ArtifactError`

Pathless content identity for bounded model artifacts. The identity carries
only the lower-case `sha-256` algorithm, a 64-digit lower-case hexadecimal
digest, and a positive byte length. It never carries a path, URL, reader,
file handle, mapping, host/device object, or payload.

| Code | Live messages | Resolution |
| --- | --- | --- |
| `ArtifactError.UnknownAlgorithm` | `unknown content identity algorithm: …` | Supply the admitted lower-case `sha-256` name. |
| `ArtifactError.BadDigest` | `content digest must be 64 lower-case hexadecimal digits` | Supply the canonical 64-digit lower-case hexadecimal digest. |
| `ArtifactError.BadLength` | `content length must be positive` | Supply the positive artifact byte length. |

## `gradus:model/gguf_manifest` — `GgufManifestError`

GGUF-A1b's format-general, structural GGUF v3 parser. It accepts either a
caller-supplied bounded table corpus or an operation-scoped exact-range
function, and retains metadata wire values plus tensor descriptors. It does
not admit an architecture or claim inference execution. Metadata and tensor
directories are bounded at 4,096 entries, and retained metadata values and
individual reads are bounded at 64 MiB. The package-MIR exemplar executes 40
synthetic cases with 40 PASS / 0 FAIL. A guarded source adapter also inspected
six operator-local real files, matched independent offsets/counts, and rejected
any attempted read into tensor data. Exact receipts are in
`exempla/gguf-manifest/README.md` and `exempla/gguf-inspect/README.md`.
The LIB-02-U1 array accessors (`texts`/`numbers`) additionally expose the
tokenizer metadata arrays with typed `BadWire`/`BadBounds` rows for
non-array values, wrong element kinds, and oversized counts.

| Code | Class / when | Resolution |
| --- | --- | --- |
| `GgufManifestError.BadFormat` | GGUF magic is malformed. | Supply a GGUF file prefix beginning with `GGUF`. |
| `GgufManifestError.UnknownVersion` | GGUF version is not v3. | Use a supported GGUF v3 artifact or a later parser unit. |
| `GgufManifestError.Truncata` | The bounded corpus ends before a required field. | Supply the complete header, metadata, tensor table, and permitted alignment padding. |
| `GgufManifestError.BadWire` | Value kind, UTF-8, boolean, array, or wire field is malformed; array accessors reject non-array values and non-string/non-integer element kinds. | Repair the GGUF wire encoding; read string arrays with `texts` and integer arrays with `numbers`. |
| `GgufManifestError.BadBounds` | Count, rank, dimension, string, array, or checked arithmetic ceiling is exceeded (including accessor-side array count and per-string ceilings). | Keep bounded counts and lengths within the documented parser ceilings. |
| `GgufManifestError.Superfluitas` | The supplied corpus contains bytes from the tensor data region. | Stop the corpus at or before the checked data offset. |
| `GgufManifestError.DuplicateKey` | A metadata key occurs more than once. | Keep metadata keys unique. |
| `GgufManifestError.TensorDuplicatum` | A tensor name occurs more than once. | Keep tensor names unique. |
| `GgufManifestError.BadOffset` | A known GGML range is incomplete, overflowing, overlapping, or outside the artifact. | Correct tensor shapes, relative offsets, and artifact length. Unknown raw type IDs remain inspectable. |
| `GgufManifestError.UnknownLayout` | A tensor fragment was requested for an unknown raw GGML layout. | Add and verify that layout before requesting payload bytes. |
| `GgufManifestError.BadIdentity` | The pathless content identity does not match the supplied artifact length or canonical form. | Supply a valid `artifact.IdentitasContenuti`. |
| `GgufManifestError.BadSource` | A range source failed or returned a byte count different from the exact requested range. | Repair the caller-owned source adapter and return exactly the requested bytes. |

## `gradus:attention` — `AttentionError`

Source: `src/attention.fab`. Render with module `message(e)`.

| Code | Class / when | Live messages (representative) | Resolution |
| --- | --- | --- | --- |
| `AttentionError.NegativeDimension` | Negative dimension in a shape or index. | `negative dimension` | Fix caller shapes, ranks, dtypes, and element counts so they satisfy the operation contract. |
| `AttentionError.DimensionAboveLimit` | A single dimension exceeds the module ceiling. | `dimension above ceiling` | Stay within the library hard ceilings for counts, key lengths, and element totals. |
| `AttentionError.ProductumSupraLimitem` | Element count (product of dims) exceeds the module ceiling. | `element count above ceiling` | Stay within the library hard ceilings for counts, key lengths, and element totals. |
| `AttentionError.GradusMismatch` | Rank / axis mismatch for the operation. | `attention requires rank-2 tensors`<br>`matmul requires rank-2 operands`<br>`rope requires rank-2 tensor`<br>`multi-head attention requires rank-2 tensors` | Fix caller shapes, ranks, dtypes, and element counts so they satisfy the operation contract. |
| `AttentionError.ShapeMismatch` | Shape mismatch between operands or against a required layout. | `positions must match the token count`<br>`query, key, value must share shape`<br>`query, key, value must share the token count`<br>`key width must equal num_kv_heads * head dim`<br>`value width must equal num_kv_heads * head dim`<br>`output projection must be [H*D, H*D]`<br>`shapes not broadcastable` | Fix caller shapes, ranks, dtypes, and element counts so they satisfy the operation contract. |
| `AttentionError.Incompatibilis` | Operands are not compatible under the operation rules. | `inner dimensions mismatch` | Fix caller shapes, ranks, dtypes, and element counts so they satisfy the operation contract. |
| `AttentionError.DtypeMismatch` | Dtype mismatch or unsupported dtype for this surface. | `dtype mismatch`<br>`unsupported dtype for attention primitive` | Fix caller shapes, ranks, dtypes, and element counts so they satisfy the operation contract. |
| `AttentionError.ElementMismatch` | Element-count / emptiness failure. | `empty attention input`<br>`empty rope input` | Fix caller shapes, ranks, dtypes, and element counts so they satisfy the operation contract. |
| `AttentionError.InvalidPosition` | Invalid position / epoch / step (negative or out of range). | `negative position` | Correct the field to the documented admitted range and re-construct. |
| `AttentionError.InvalidDimension` | Invalid dimension parameter (e.g. RoPE dim, embedding width). | `rope dim exceeds head width`<br>`rope dim must be at least 2`<br>`rope dim must be even` | Correct the field to the documented admitted range and re-construct. |
| `AttentionError.InvalidConfig` | Invalid RoPE / head configuration (frequency base / scale not positive and finite; head counts or widths inconsistent). | `rope frequency base must be positive`<br>`rope scale must be positive`<br>`num_heads must be positive`<br>`num_kv_heads must be positive`<br>`num_kv_heads must not exceed num_heads`<br>`num_heads must be a multiple of num_kv_heads`<br>`query width must be a multiple of num_heads`<br>`head dim must be positive` | Correct the config field to the documented admitted range and re-construct via `structa_rope_configura` or valid head counts / packed widths. |

## `gradus:cache` — `CacheError`

Source: `src/cache.fab`. Render with module `message(e)`.

| Code | Class / when | Live messages (representative) | Resolution |
| --- | --- | --- | --- |
| `CacheError.EmptyName` | Empty or reserved name / owner / identity field. | `empty execution config`<br>`empty model name`<br>`empty model version`<br>`empty tokenizer identity`<br>`reserved wire character in identity` | Use the pinned tokenizer identity (gpt2/BBPE, pre=`smollm`, EOG `{0,2}`, BOS-free, space-prefix-free). |
| `CacheError.IdExtra` | Token id outside the admitted range. | `token id must be non-negative` | Keep token ids in the admitted range for the row. |
| `CacheError.ShapeMismatch` | Shape mismatch between operands or against a required layout. | `K must be [1, dim]`<br>`V must be [1, dim]` | Fix caller shapes, ranks, dtypes, and element counts so they satisfy the operation contract. |
| `CacheError.DtypeMismatch` | Dtype mismatch or unsupported dtype for this surface. | `unsupported dtype for cache` | Fix caller shapes, ranks, dtypes, and element counts so they satisfy the operation contract. |
| `CacheError.InvalidDimension` | Invalid dimension parameter (e.g. RoPE dim, embedding width). | `embedding dimension must be at least one`<br>`layer count must be at least one` | Correct the field to the documented admitted range and re-construct. |
| `CacheError.ElementMismatch` | Element-count / emptiness failure. | `unreachable` (internal) | Fix caller shapes, ranks, dtypes, and element counts so they satisfy the operation contract. |
| `CacheError.UnknownVersion` | Unknown or unsupported schema / file / marker version. | `unknown cache schema version` | Re-emit with the current schema stamp; never guess an unknown version. |
| `CacheError.BadWire` | Malformed wire / bytes / marker / field encoding. | `empty dtype in cache identity`<br>`empty execution config in cache identity`<br>`empty layout in cache identity`<br>`empty model name in cache identity`<br>`empty model version in cache identity`<br>`empty tokenizer identity in cache identity`<br>`invalid layer count in cache identity`<br>`malformed cache identity wire`<br>`malformed layer count in cache identity`<br>`malformed position span in cache identity`<br>`unknown cache marker` | Re-emit with the current schema stamp; never guess an unknown version. |

## `gradus:decode` — `DecodeError`

Source: `src/decode.fab`. Render with module `message(e)`.

| Code | Class / when | Live messages (representative) | Resolution |
| --- | --- | --- | --- |
| `DecodeError.IdExtra` | Token id outside the admitted range. | `token id out of vocabulary range` | Keep token ids in the admitted range for the row. |
| `DecodeError.InvalidPosition` | Invalid position / epoch / step (negative or out of range). | `position out of context`<br>`prompt exceeds the context limit` | Correct the field to the documented admitted range and re-construct. |
| `DecodeError.Terminus` | A configured ceiling was reached (context, tokens, …). | `context limit reached` | Reduce the request or fix indices so they stay within the configured ceiling. |
| `DecodeError.InvalidDecoder` | Decode model / config construction failed. | `context length must be at least one`<br>`embedding columns must equal the dimension`<br>`embedding dimension must be at least one`<br>`embedding must be rank-2`<br>`embedding rows must equal the vocabulary`<br>`invalid attention scale`<br>`output projection bias must be [vocab]`<br>`output projection must be rank-2`<br>`output projection shape must be [dim, vocab]`<br>`vocabulary must be non-empty` | Correct the field to the documented admitted range and re-construct. |
| `DecodeError.ShapeMismatch` | Shape mismatch between operands or against a required layout. | `bias does not match output width` | Fix caller shapes, ranks, dtypes, and element counts so they satisfy the operation contract. |
| `DecodeError.DtypeMismatch` | Dtype mismatch or unsupported dtype for this surface. | `dtype mismatch` | Fix caller shapes, ranks, dtypes, and element counts so they satisfy the operation contract. |
| `DecodeError.ElementMismatch` | Element-count / emptiness failure. | `empty prompt`<br>`unreachable` (internal) | Fix caller shapes, ranks, dtypes, and element counts so they satisfy the operation contract. |
| `DecodeError.Incompatibilis` | Operands are not compatible under the operation rules. | `inner dimensions mismatch` | Fix caller shapes, ranks, dtypes, and element counts so they satisfy the operation contract. |
| `DecodeError.InvalidDimension` | Invalid dimension parameter (e.g. RoPE dim, embedding width). | `unknown attention mode` | Correct the field to the documented admitted range and re-construct. |
| `DecodeError.Cancelata` | Cooperative cancellation requested. | `cancellation requested` | Clear the cancellation flag or end the run; cancellation fails closed. |
| `DecodeError.SamplingDefecta` | Sampling step failed (mapped). | _(reserved / mapped — no direct literal `iace` site; code is live on the `discretio`)_ | Fix the sampling configuration or logits before drawing. |

## `gradus:dtype` — `DTypeError`

Source: `src/dtype.fab`. Render with module `message(e)`.

| Code | Class / when | Live messages (representative) | Resolution |
| --- | --- | --- | --- |
| `DTypeError.UnknownName` | Unknown name (dtype, mode, identity lookup miss). | `unknown dtype name: …` | Correct the failing field per the message and re-invoke the fail-closed constructor. |
| `DTypeError.UnknownVersion` | Unknown or unsupported schema / file / marker version. | `malformed dtype serialization`<br>`unknown dtype marker`<br>`unknown dtype schema version` | Re-emit with the current schema stamp; never guess an unknown version. |
| `DTypeError.NonFinite` | Non-finite value (NaN/Inf) rejected. | `non-finite value in cast to i32`<br>`non-finite value in cast to u8` | Ensure inputs are finite; reject NaN/Inf at the boundary. |
| `DTypeError.Superfluitas` | Value overflows the destination type range. | `f16 overflow in cast`<br>`i32 overflow in cast`<br>`u8 overflow in cast` | Cast or clamp into the destination type's finite range. |

## `gradus:generation` — `GenerationError`

Source: `src/generation.fab`. Render with module `message(e)`.

| Code | Class / when | Live messages (representative) | Resolution |
| --- | --- | --- | --- |
| `GenerationError.InvalidConfig` | Generation / sampling / config field out of admitted range. | `context length must be at least one`<br>`maximum generated tokens must be at least one`<br>`maximum generated tokens must fit within the context`<br>`min-p must be within [0, 1]`<br>`prompt batch size must be at least one`<br>`repetition penalty must be at least one`<br>`seed must be at least one`<br>`temperature must be non-negative`<br>`top-k must be non-negative`<br>`top-p must be within [0, 1]`<br>`unreachable` (internal) | Use a seed that meets the contract (non-zero / ≥ 1 as required). |
| `GenerationError.ElementMismatch` | Element-count / emptiness failure. | _(reserved / mapped — no direct literal `iace` site; code is live on the `discretio`)_ | Fix caller shapes, ranks, dtypes, and element counts so they satisfy the operation contract. |
| `GenerationError.DtypeMismatch` | Dtype mismatch or unsupported dtype for this surface. | _(reserved / mapped — no direct literal `iace` site; code is live on the `discretio`)_ | Fix caller shapes, ranks, dtypes, and element counts so they satisfy the operation contract. |
| `GenerationError.Incompatibilis` | Operands are not compatible under the operation rules. | _(reserved / mapped — no direct literal `iace` site; code is live on the `discretio`)_ | Fix caller shapes, ranks, dtypes, and element counts so they satisfy the operation contract. |
| `GenerationError.UnknownVersion` | Unknown or unsupported schema / file / marker version. | `unknown generation schema version` | Re-emit with the current schema stamp; never guess an unknown version. |
| `GenerationError.BadWire` | Malformed wire / bytes / marker / field encoding. | `malformed context length in generation wire`<br>`malformed generation config wire`<br>`malformed max tokens in generation wire`<br>`malformed min-p in generation wire`<br>`malformed prompt batch in generation wire`<br>`malformed repetition penalty in generation wire`<br>`malformed seed in generation wire`<br>`malformed temperature in generation wire`<br>`malformed top-k in generation wire`<br>`malformed top-p in generation wire`<br>`unknown generation marker` | Re-emit with the current schema stamp; never guess an unknown version. |
| `GenerationError.Terminus` | A configured ceiling was reached (context, tokens, …). | `context limit reached`<br>`maximum generated tokens reached` | Reduce the request or fix indices so they stay within the configured ceiling. |

## `gradus:gradient` — `GradienteError`

Source: `src/gradient.fab`. Render with module `message(e)`.

| Code | Class / when | Live messages (representative) | Resolution |
| --- | --- | --- | --- |
| `GradienteError.GradusIgnotum` | Unknown or empty gradient identity field. | `empty gradient name`<br>`empty gradient owner`<br>`no gradient for that parameter identity` | Supply a non-empty name/owner with no reserved wire characters. |
| `GradienteError.GradientVersion` | Invalid gradient generation counter. | `invalid gradient generation` | Supply a non-empty gradient owner/name and a valid generation counter. |

## `gradus:gradus` — `GradusError`

Source: `src/gradus.fab`. Render with module `message(e)`.

Facade: `_mappa` preserves nn message texts into these variants (text unchanged). Unmapped nn texts fall through to `ShapeMismatch`.

| Code | Class / when | Live messages (representative) | Resolution |
| --- | --- | --- | --- |
| `GradusError.NegativeDimension` | Negative dimension in a shape or index. | `negative dimension` | Fix caller shapes, ranks, dtypes, and element counts so they satisfy the operation contract. |
| `GradusError.DimensionAboveLimit` | A single dimension exceeds the module ceiling. | `dimension above ceiling` | Stay within the library hard ceilings for counts, key lengths, and element totals. |
| `GradusError.ProductumSupraLimitem` | Element count (product of dims) exceeds the module ceiling. | `element count above ceiling` | Stay within the library hard ceilings for counts, key lengths, and element totals. |
| `GradusError.GradusMismatch` | Rank / axis mismatch for the operation. | `linear requires rank-2 input`<br>`linear requires rank-2 weight` | Fix caller shapes, ranks, dtypes, and element counts so they satisfy the operation contract. |
| `GradusError.ShapeMismatch` | Shape mismatch between operands or against a required layout. | `bias does not match output shape`<br>`bias does not match output width`<br>`bias must be per-channel or output-shaped` | Fix caller shapes, ranks, dtypes, and element counts so they satisfy the operation contract. |
| `GradusError.Incompatibilis` | Operands are not compatible under the operation rules. | `inner dimensions mismatch` | Fix caller shapes, ranks, dtypes, and element counts so they satisfy the operation contract. |
| `GradusError.DtypeMismatch` | Dtype mismatch or unsupported dtype for this surface. | `dtype mismatch`<br>`unsupported dtype for nn primitive` | Fix caller shapes, ranks, dtypes, and element counts so they satisfy the operation contract. |
| `GradusError.ElementMismatch` | Element-count / emptiness failure. | _(reserved / mapped — no direct literal `iace` site; code is live on the `discretio`)_ | Fix caller shapes, ranks, dtypes, and element counts so they satisfy the operation contract. |

## `gradus:loss` — `LossError`

Source: `src/loss.fab`. Render with module `message(e)`.

| Code | Class / when | Live messages (representative) | Resolution |
| --- | --- | --- | --- |
| `LossError.NegativeDimension` | Negative dimension in a shape or index. | `negative dimension` | Fix caller shapes, ranks, dtypes, and element counts so they satisfy the operation contract. |
| `LossError.DimensionAboveLimit` | A single dimension exceeds the module ceiling. | `dimension above ceiling` | Stay within the library hard ceilings for counts, key lengths, and element totals. |
| `LossError.ProductumSupraLimitem` | Element count (product of dims) exceeds the module ceiling. | `element count above ceiling` | Stay within the library hard ceilings for counts, key lengths, and element totals. |
| `LossError.GradusMismatch` | Rank / axis mismatch for the operation. | `cross_entropy requires rank-2 logits`<br>`cross_entropy target must be rank-1` | Provide a non-empty finite logits vector. |
| `LossError.ShapeMismatch` | Shape mismatch between operands or against a required layout. | `prediction and target shapes differ`<br>`target length does not match logits rows` | Provide a non-empty finite logits vector. |
| `LossError.DtypeMismatch` | Dtype mismatch or unsupported dtype for this surface. | `cross_entropy target must be i32 class indices`<br>`dtype mismatch`<br>`unsupported dtype for loss` | Fix caller shapes, ranks, dtypes, and element counts so they satisfy the operation contract. |
| `LossError.ElementMismatch` | Element-count / emptiness failure. | `empty batch`<br>`empty class axis`<br>`empty loss input` | Fix caller shapes, ranks, dtypes, and element counts so they satisfy the operation contract. |
| `LossError.Incompatibilis` | Operands are not compatible under the operation rules. | `target class out of range`<br>`target must be integer class indices` | Keep token ids in the admitted range for the row. |
| `LossError.NonFinite` | Non-finite value (NaN/Inf) rejected. | `non-finite logits`<br>`non-finite prediction`<br>`non-finite target` | Provide a non-empty finite logits vector. |

## `gradus:math` — `MathError`

Source: `src/math.fab`. Render with module `message(e)`.

| Code | Class / when | Live messages (representative) | Resolution |
| --- | --- | --- | --- |
| `MathError.NegativeDimension` | Negative dimension in a shape or index. | `negative dimension` | Fix caller shapes, ranks, dtypes, and element counts so they satisfy the operation contract. |
| `MathError.DimensionAboveLimit` | A single dimension exceeds the module ceiling. | `dimension above ceiling` | Stay within the library hard ceilings for counts, key lengths, and element totals. |
| `MathError.ProductumSupraLimitem` | Element count (product of dims) exceeds the module ceiling. | `element count above ceiling` | Stay within the library hard ceilings for counts, key lengths, and element totals. |
| `MathError.ShapeMismatch` | Shape mismatch between operands or against a required layout. | _(reserved / mapped — no direct literal `iace` site; code is live on the `discretio`)_ | Fix caller shapes, ranks, dtypes, and element counts so they satisfy the operation contract. |
| `MathError.GradusMismatch` | Rank / axis mismatch for the operation. | `axis out of range`<br>`concat rank mismatch`<br>`concat requires rank >= 1`<br>`matmul requires rank-2 operands`<br>`reduce requires rank >= 1`<br>`slice requires rank >= 1` | Keep token ids in the admitted range for the row. |
| `MathError.Incompatibilis` | Operands are not compatible under the operation rules. | `concat dimension mismatch`<br>`inner dimensions mismatch`<br>`slice bounds out of range` | Keep token ids in the admitted range for the row. |
| `MathError.DtypeMismatch` | Dtype mismatch or unsupported dtype for this surface. | `dtype mismatch` | Fix caller shapes, ranks, dtypes, and element counts so they satisfy the operation contract. |
| `MathError.ElementMismatch` | Element-count / emptiness failure. | `element count mismatch`<br>`empty concat list`<br>`empty reduction axis` | Fix caller shapes, ranks, dtypes, and element counts so they satisfy the operation contract. |
| `MathError.NonFinite` | Non-finite value (NaN/Inf) rejected. | `non-finite value in cast to i32`<br>`non-finite value in cast to u8` | Ensure inputs are finite; reject NaN/Inf at the boundary. |
| `MathError.Superfluitas` | Value overflows the destination type range. | _(reserved / mapped — no direct literal `iace` site; code is live on the `discretio`)_ | Cast or clamp into the destination type's finite range. |
| `MathError.UnknownName` | Unknown name (dtype, mode, identity lookup miss). | _(reserved / mapped — no direct literal `iace` site; code is live on the `discretio`)_ | Correct the failing field per the message and re-invoke the fail-closed constructor. |

## `gradus:metrics` — `MetricError`

Source: `src/metrics.fab`. Render with module `message(e)`.

| Code | Class / when | Live messages (representative) | Resolution |
| --- | --- | --- | --- |
| `MetricError.GradusMismatch` | Rank / axis mismatch for the operation. | `accuracy requires rank-2 predictions`<br>`accuracy target must be rank-1` | Fix caller shapes, ranks, dtypes, and element counts so they satisfy the operation contract. |
| `MetricError.ShapeMismatch` | Shape mismatch between operands or against a required layout. | `target length does not match predictions rows` | Fix caller shapes, ranks, dtypes, and element counts so they satisfy the operation contract. |
| `MetricError.DtypeMismatch` | Dtype mismatch or unsupported dtype for this surface. | `accuracy target must be i32 class indices`<br>`unsupported dtype for metric` | Fix caller shapes, ranks, dtypes, and element counts so they satisfy the operation contract. |
| `MetricError.ElementMismatch` | Element-count / emptiness failure. | `empty batch`<br>`empty class axis` | Fix caller shapes, ranks, dtypes, and element counts so they satisfy the operation contract. |
| `MetricError.NonFinite` | Non-finite value (NaN/Inf) rejected. | `non-finite prediction`<br>`non-finite target` | Ensure inputs are finite; reject NaN/Inf at the boundary. |
| `MetricError.Incompatibilis` | Operands are not compatible under the operation rules. | `target class out of range`<br>`target must be integer class indices` | Keep token ids in the admitted range for the row. |
| `MetricError.Invalida` | Metric record field out of range. | `accuracy must be finite`<br>`accuracy must be in [0, 1]`<br>`loss must be finite` | Keep metric fields finite and inside the documented range (loss finite; accuracy in [0,1]). |

## `gradus:model/capsule` — `AdmissionError`

Source: `src/model/capsule.fab`. Render with module `message(e)`.
Schema: `capsule-schema-2.0.0` (A1C-M1 clean break). Schema 1 is retired —
every entry point rejects a schema-1 stamp with the typed `SchemaVetus`.

| Code | Class / when | Live messages (representative) | Resolution |
| --- | --- | --- | --- |
| `AdmissionError.UnknownVersion` | Unknown capsule schema version (reject, no partial reads). | `unknown capsule schema version: …` | Re-emit with the current schema stamp; never guess an unknown version. |
| `AdmissionError.SchemaVetus` | Retired schema-1 stamp at the schema-2 boundary (constructor, `verify`, or wire form). | `schema 1 is retired — capsule schema is 2.0.0` | Re-admit with a `capsule-schema-2.0.0` capsule / identity wire. |
| `AdmissionError.UnknownAlgorithm` | Un-admitted digest algorithm. | `unknown digest algorithm: …` | Supply the admitted lower-case `sha-256` algorithm. |
| `AdmissionError.BadDigest` | Malformed digest value (format / length / charset) or a digest mismatch on verification. | `digest mismatch — capsule does not match the expected artifact`<br>`malformed digest value` | Supply the canonical 64-digit lower-case hexadecimal digest that matches the artifact. |
| `AdmissionError.BadManifest` | Malformed per-format manifest: empty or non-matching format/version, artifact-length mismatch, invalid byte length, malformed tensor descriptor, or a manifest inconsistent with the carried identity. | `manifest is inconsistent with the artifact identity`<br>`invalid artifact byte length`<br>`capsule failed verification`<br>`metadata index out of bounds`<br>`tensor descriptor index out of bounds` | Supply a per-format manifest whose format/version, lengths, and tensor descriptors are consistent with the artifact identity. |
| `AdmissionError.BadWire` | Malformed capsule identity wire form. | `malformed capsule identity wire form`<br>`malformed numeric field`<br>`numeric field above the integer carrier`<br>`unknown capsule identity marker`<br>`invalid byte length in capsule identity`<br>`unreachable` (internal) | Re-emit with the current schema stamp; never guess an unknown version. |

## `gradus:model/dense_llama` — `DensumLlamaError`

Source: `src/model/dense_llama.fab` (REF-01-U1.6). Render with module
`message(e)`. The typed `llama` architecture adapter fails closed on any
canonical resolution that cannot be represented: unknown canonical names,
layer indices outside the frozen range, a canonical target's GGUF tensor
absent from the manifest, and unknown GGML layouts.

| Code | Class / when | Live messages (representative) | Resolution |
| --- | --- | --- | --- |
| `DensumLlamaError.UnknownCanonicalName` | Unknown canonical tensor name in the llama mapping. | `unknown canonical tensor name: …` | Use a canonical family the adapter defines (`model.embed_tokens`, `model.layers.{N}.{…}`, `model.norm`, `lm_head`). |
| `DensumLlamaError.StrataExcessiva` | Layer index outside the frozen layer range `[0, strata)`. | `layer index outside the frozen llama layer range: …` | Supply a layer index within the frozen config's layer count. |
| `DensumLlamaError.TensorDeest` | The canonical target's GGUF tensor is absent from the manifest (or descriptor resolution failed). | `canonical tensor is absent from the manifest: …`<br>`canonical tensor resolution failed: …` | Admit a manifest whose tensor table carries the canonical target's GGUF row (e.g. tied rows share `token_embd.weight`). |
| `DensumLlamaError.UnknownLayout` | The resolved tensor's GGML layout is unknown (unlisted type id). | `canonical tensor resolves to an unknown GGML layout: …` | Use a manifest whose GGML type ids resolve to known layouts. |

## `gradus:model/dequant` — `DequantError`

Source: `src/model/dequant.fab`. Render with module `message(e)`.

Admitted physical set (GGUF-A3 C1 + W1-U3): **{F32, F16, BF16, Q5_0, Q8_0,
Q4_K, Q5_K, Q6_K}** — the Qwen3.6 completion-row union set plus F16 native
convert. The A3 additions are **BF16** (`GGML_BF16`, id 30; 1 element/block,
2 bytes/block — bf16→f32 value arithmetic, bit-exact for every finite
bf16) and **Q5_K** (`GGML_Q5_K`, id 13; 256 elements/block, 176
bytes/block — `dequantize_row_q5_K`). W1-U3 adds **F16** (`GGML_F16`, id
1; 1 element/block, 2 bytes/block — IEEE binary16→f32 via `_half`, same
NativeF16Convert pattern as BF16). The layout constants are cross-checked against
`LayoutGgml.Known` at the `tensor_view.links` view-binding boundary —
the manifest is the single layout authority, dequant validates admission
and never re-derives layout.

| Code | Class / when | Live messages (representative) | Resolution |
| --- | --- | --- | --- |
| `DequantError.UnknownDtype` | un-admitted / unknown GGML type id. | `un-admitted GGML type id: …`<br>`unreachable` (internal) | Use an admitted type/quantization row from the closed set; ensure block layouts tile. |
| `DequantError.BadBlock` | block byte length != the layout's block_bytes. | `block byte length mismatch` | Provide a payload whose lengths/offsets match the layout (exact tile, no gaps/overlaps). |
| `DequantError.BadOrder` | row byte length not a multiple of block_bytes. | `row byte length not a multiple of block_bytes` | Provide a payload whose lengths/offsets match the layout (exact tile, no gaps/overlaps). |
| `DequantError.BadPayload` | malformed value (NaN half/bf16) fails closed. | `NaN f32 value in dequant block`<br>`NaN half in dequant block`<br>`NaN bf16 value in dequant block` | Ensure inputs are finite; reject NaN/Inf at the boundary. |

## `gradus:model/tensor_payload` — `PayloadError`

Source: `src/model/tensor_payload.fab`. Render with module `message(e)`.

The bounded per-tensor payload value (GGUF-A3 C2-U2) carries exactly the
stored range facts — name, absolute byte start, stored length — plus the
bounded bytes. It carries no path, reader, handle, or whole-model byte list.

| Code | Class / when | Live messages (representative) | Resolution |
| --- | --- | --- | --- |
| `PayloadError.UnknownName` | Tensor name not present in the manifest. | `tensor name is not present in the manifest` | Bind against a name the manifest's tensor table actually carries. |
| `PayloadError.BadRange` | Byte range lies outside the artifact. | `tensor byte range lies outside the artifact` | Provide a payload whose lengths/offsets match the layout (exact tile, no gaps/overlaps). |
| `PayloadError.BadLength` | Payload length does not match the stored layout length. | `tensor payload length does not match the stored layout length` | Provide a payload whose lengths/offsets match the layout (exact tile, no gaps/overlaps). |

## `gradus:model/tensor_view` — `VisioError`

Source: `src/model/tensor_view.fab`. Render with module `message(e)`.

The typed view + bind + windowed materializers (GGUF-A3 C2-U3/C2-U4).
`links` binds one descriptor + one validated payload; the manifest is the
single layout authority (dequant only cross-checks admission via
`elementa_glomoris`). `materialize_slice`/`materialize_block`
dequantize bounded windows one block per source read; no whole-tensor or
whole-model read path exists.

| Code | Class / when | Live messages (representative) | Resolution |
| --- | --- | --- | --- |
| `VisioError.UnknownName` | Descriptor name absent from the manifest (bind). | `tensor not found: …`<br>`manifest tensor range facts are invalid` (mapped) | Bind against a name the manifest's tensor table actually carries. |
| `VisioError.BadRange` | Absolute-range mismatch — payload start must equal `data_start + relative_offset` — or a source/decode failure (materialize). | `payload start does not match the manifest tensor range`<br>`payload range source failed: …`<br>`payload range source returned an unexpected byte length`<br>`block sub-window range is negative`<br>`block value decode failed: …`<br>`block decode failed` | Provide a payload whose range facts match the manifest; repair the caller-owned source adapter and return exactly the requested bytes. |
| `VisioError.BadLength` | Stored-length mismatch vs `Known.byte_length`. | `payload length does not match the stored layout length` | Provide a payload whose lengths/offsets match the layout (exact tile, no gaps/overlaps). |
| `VisioError.UnknownLayout` | Unknown layout — inspectable, not materializable. | `tensor layout is unknown; payload range is unavailable` | Add and verify that layout before requesting payload bytes. |
| `VisioError.UnknownDtype` | Un-admitted physical type (dequant `elementa_glomoris` cross-check). | `un-admitted GGML type id: …` | Use an admitted type/quantization row from the closed set; ensure block layouts tile. |
| `VisioError.BadOrder` | Element window not block-aligned. | `element window is not aligned to the tensor block boundary` | Request windows aligned to `Known.elements_per_block`. |
| `VisioError.BadBounds` | Negative / out-of-tensor / over-cap window, or out-of-range block index. | `element window is negative`<br>`element window exceeds the bounded slice cap`<br>`element window exceeds the tensor`<br>`block index is negative`<br>`block index exceeds the tensor block count` | Keep windows within the tensor and at or under `MAXIMUM_SLICEM_ELEMENTA` (16 Mi elements); larger consumption is the caller's windowed loop. |

## `gradus:model/dense_qwen2` — `DenseQwen2Error`

Source: `src/model/dense_qwen2.fab`. Render with module `message(e)`.

The typed `qwen2` (Qwen2.5) architecture adapter (REF-01-U1.7): canonical
dense tensor-name → manifest-descriptor resolution. The canonical family is
the same as the `llama` adapter; the qwen2 deltas are the tensor-set tie
status for `lm_head`, the GQA head config, and the frozen rope_theta
1000000. Every failure is a typed diagnostic — the adapter never guesses a
canonical name, layer index, or tensor fact.

| Code | Class / when | Live messages (representative) | Resolution |
| --- | --- | --- | --- |
| `DenseQwen2Error.UnknownArchitecture` | Manifest architecture is not qwen2. | `architecture is not qwen2: …` | Admit a qwen2 row (the qwen2 family adapter resolves only qwen2 manifests). |
| `DenseQwen2Error.UnknownCanonical` | Unknown canonical tensor name or unknown layer-tensor suffix. | `unknown canonical qwen2 tensor name: …`<br>`unknown canonical qwen2 layer tensor suffix: …` | Use one of the canonical family names (`model.embed_tokens`, `model.layers.{N}.*`, `model.norm`, `lm_head`) with a known layer suffix. |
| `DenseQwen2Error.LayerOutOfRange` | Layer index outside `[0, strata)`. | `layer index out of range for canonical tensor: …` | Address a layer within the frozen block count. |
| `DenseQwen2Error.TensorAbsens` | A canonical tensor is missing from the manifest. | `canonical … missing from manifest: …`<br>`canonical model.embed_tokens missing from manifest: token_embd.weight` | Resolve against a manifest whose tensor table carries the canonical tensor. |
| `DenseQwen2Error.BadConfig` | A frozen-config fact is unavailable or invalid. | `qwen2 metadata fact unavailable: …`<br>`qwen2 head count must be positive`<br>`qwen2 token_embd.weight must be rank 2` | Provide the qwen2 metadata facts (architecture, block/head/kv/embedding counts) and a rank-2 `token_embd.weight`. |

## `gradus:model/dense` — `DenseError`

Source: `src/model/dense.fab`. Render with module `message(e)`.

The dense model assembly (REF-01-U1.8) fails closed with typed diagnostics
on every canonical resolution and shape/sequence fact: a resolver that
cannot materialize a canonical tensor (`TensorAbsens` — the resolver's
message is preserved verbatim), an architecture config that cannot be
assembled (`BadConfig`), a materialized tensor whose shape contradicts
the config (`BadShape`), and a token id outside the embedding vocabulary
(`TerminusExcedit`). Sub-call failures from `gradus:nn` /
`gradus:transformer` / `gradus:tensor` are mapped into `BadShape`
preserving the documented message text.

| Code | Class / when | Live messages (representative) | Resolution |
| --- | --- | --- | --- |
| `DenseError.TensorAbsens` | A canonical tensor cannot be materialized (resolver `successus = falsum`). | `canonical tensor missing: …` (the resolver's message, preserved) | Provide a resolver that materializes every canonical name the config requires (`model.embed_tokens`, `model.layers.{N}.*`, `model.norm`, and `lm_head` for untied rows). |
| `DenseError.BadConfig` | The architecture config cannot be assembled, or the token sequence/positions are inconsistent. | `layer count must be at least 1`<br>`head count must be at least 1`<br>`KV head count must be between 1 and the head count`<br>`head count must be a multiple of the KV head count`<br>`head dim must be at least 1`<br>`hidden dim must be at least 1`<br>`vocabulary size must be at least 1`<br>`token sequence must be non-empty`<br>`positions must match the token count` | Provide a positive config consistent with the materialized tensor shapes, and one position per token. |
| `DenseError.BadShape` | A canonical tensor's shape contradicts the config, or a composed-row sub-call failed. | `canonical tensor … has shape …, expected …`<br>`embedding must be rank 2`<br>`block input must be rank 2`<br>`block weight must be rank 2`<br>`canonical tensor … must be rank 2` + the preserved nn/transformer/tensor message texts | Provide materialized stored-weight views whose shapes match the config (`[D, V]` embed, `[D]` norm scales, `[D, H·D]`/`[D, K·D]`/`[H·D, H·D]` projections, `[D, F]`/`[F, D]` MLP rows). |
| `DenseError.TerminusExcedit` | A token id is outside the embedding vocabulary. | `token id out of range for the embedding` | Provide token ids within `[0, vocab)`. |

## `gradus:model/gguf` — `GgufError`

Source: `src/model/gguf.fab`. Render with module `message(e)`.

| Code | Class / when | Live messages (representative) | Resolution |
| --- | --- | --- | --- |
| `GgufError.BadFormat` | bad magic (not a GGUF file). | `not a GGUF file — bad magic` | Provide a well-formed file with the expected magic and version. |
| `GgufError.UnknownVersion` | unsupported GGUF file version. | `unsupported GGUF file version: …` | Re-emit with the current schema stamp; never guess an unknown version. |
| `GgufError.BadArchitecture` | architecture facts (arch id, layers, context, | `architecture mismatch`<br>`context length mismatch`<br>`embedding size mismatch`<br>`layer count mismatch`<br>`missing required metadata key: general.architecture`<br>`missing required metadata key: llama.block_count`<br>`missing required metadata key: llama.context_length`<br>`missing required metadata key: llama.embedding_length`<br>`missing required metadata key: llama.vocab_size`<br>`vocabulary size mismatch` | Match the admitted architecture facts (arch, layers, context, vocab, embedding). |
| `GgufError.UnknownQuantization` | Unknown or mis-laid-out quantization row. | `file type mismatch`<br>`missing required metadata key: general.file_type`<br>`missing required metadata key: general.quantization_version`<br>`quantization version mismatch`<br>`tensor byte size not a multiple of the 32-byte data alignment`<br>`tensor size not a multiple of its block layout`<br>`tensor type count mismatch`<br>`unknown ggml tensor type` | Use an admitted type/quantization row from the closed set; ensure block layouts tile. |
| `GgufError.BadOffset` | tensor offsets / data-region tiling (coverage). | `data region does not tile exactly`<br>`tensor offsets are not contiguous` | Provide a payload whose lengths/offsets match the layout (exact tile, no gaps/overlaps). |
| `GgufError.BadShape` | shapes: rank, dims, total element count. | `invalid tensor dimension`<br>`tensor element count above the expected total`<br>`total element count above the expected total`<br>`total element count mismatch`<br>`unsupported tensor rank` | Stay within the library hard ceilings for counts, key lengths, and element totals. |
| `GgufError.BadTokenizer` | tokenizer identity facts. | `add_bos_token mismatch`<br>`add_space_prefix mismatch`<br>`bos token id mismatch`<br>`eos token id mismatch`<br>`missing required metadata key: tokenizer.ggml.add_bos_token`<br>`missing required metadata key: tokenizer.ggml.add_space_prefix`<br>`missing required metadata key: tokenizer.ggml.bos_token_id`<br>`missing required metadata key: tokenizer.ggml.eos_token_id`<br>`missing required metadata key: tokenizer.ggml.model`<br>`missing required metadata key: tokenizer.ggml.padding_token_id`<br>`missing required metadata key: tokenizer.ggml.pre`<br>`missing required metadata key: tokenizer.ggml.unknown_token_id`<br>`padding token id mismatch`<br>`tokenizer model mismatch`<br>`tokenizer pre-tokenizer mismatch`<br>`unknown token id mismatch` | Use the pinned tokenizer identity (gpt2/BBPE, pre=`smollm`, EOG `{0,2}`, BOS-free, space-prefix-free). |
| `GgufError.BadBounds` | count ceilings (kv/tensor/element, key length). | `expected element count outside the admitted range`<br>`expected kv count outside the admitted range`<br>`expected tensor count outside the admitted range`<br>`expected tensor type counts do not sum to the tensor count`<br>`expected tensor type counts outside the admitted range`<br>`metadata KV count mismatch`<br>`metadata key exceeds the 128-byte ceiling`<br>`tensor count mismatch` | Stay within the library hard ceilings for counts, key lengths, and element totals. |
| `GgufError.BadWire` | malformed bytes: truncation, unknown/duplicate | `array element count above ceiling`<br>`duplicate metadata key`<br>`duplicate tensor name`<br>`empty tensor name`<br>`gguf field above the integer carrier`<br>`invalid UTF-8 in gguf string`<br>`malformed bool value`<br>`string exceeds the 4096-byte ceiling`<br>`tensor name exceeds the 128-byte ceiling`<br>`truncated gguf field`<br>`truncated gguf header`<br>`truncated string field`<br>`unexpected metadata value type`<br>`unknown array element type`<br>`unknown gguf metadata value type`<br>`unknown metadata key`<br>`unreachable` (internal) | Re-emit with the current schema stamp; never guess an unknown version. |
| `GgufError.BadCapsule` | capsule construction failed. | `capsule construction failed: …`<br>`unreachable` (internal) | Read the suffix message for the underlying admission failure; fix that field and re-admit. |

## `gradus:model/safetensors` — `SafetensorError`

Source: `src/model/safetensors.fab`. Render with module `message(e)`.

| Code | Class / when | Live messages (representative) | Resolution |
| --- | --- | --- | --- |
| `SafetensorError.BadShape` | Malformed shape / header / dimension on a wire or file. | `\\`<br>`\n`<br>`\r`<br>`\t`<br>`array must contain only integers`<br>`dtype must be a string`<br>`duplicate data_offsets in tensor descriptor`<br>`duplicate dtype in tensor descriptor`<br>`duplicate shape in tensor descriptor`<br>`empty header`<br>`expected an integer array`<br>`header is not a JSON object`<br>`header is not valid UTF-8`<br>`integer above the numeric carrier`<br>`invalid safetensors header size`<br>`malformed \\u escape`<br>`malformed array separator`<br>`malformed header member`<br>`malformed header separator`<br>`malformed integer`<br>_… +29 more live messages in `src/model/safetensors.fab`_ | Stay within the library hard ceilings for counts, key lengths, and element totals. |
| `SafetensorError.UnknownVersion` | Unknown or unsupported schema / file / marker version. | `unsupported safetensors row version: …` | Re-emit with the current schema stamp; never guess an unknown version. |
| `SafetensorError.BadArchitecture` | Architecture facts mismatch or missing. | `architecture mismatch`<br>`tensor count mismatch`<br>`tensor not in admitted row: …` | Match the admitted architecture facts (arch, layers, context, vocab, embedding). |
| `SafetensorError.UnknownDtype` | Unknown dtype name/tag or un-admitted type id. | `unsupported dtype: …` | Use an admitted type/quantization row from the closed set; ensure block layouts tile. |
| `SafetensorError.BadOffset` | Safetensors data_offsets failure. | `data region does not tile exactly`<br>`data region truncated — tensor extends beyond file: …`<br>`data_offsets must have exactly 2 values: …`<br>`duplicate tensor name: …`<br>`malformed data offsets for `<br>`misaligned tensor data offset: …`<br>`overlapping tensor data regions` | Provide a payload whose lengths/offsets match the layout (exact tile, no gaps/overlaps). |
| `SafetensorError.BadShape` | Safetensors shape failure. | `empty shape`<br>`non-positive dimension`<br>`shape mismatch for `<br>`shape/offset inconsistency for ` | Fix caller shapes, ranks, dtypes, and element counts so they satisfy the operation contract. |
| `SafetensorError.BadTokenizer` | Tokenizer identity admission failure. | `tokenizer identity mismatch` | Use the pinned tokenizer identity (gpt2/BBPE, pre=`smollm`, EOG `{0,2}`, BOS-free, space-prefix-free). |
| `SafetensorError.BadBounds` | Ceiling / bound violation. | `array above length ceiling`<br>`dimension above ceiling`<br>`element count above ceiling`<br>`header size above ceiling`<br>`header token count above ceiling`<br>`metadata KV count above ceiling`<br>`tensor count above ceiling`<br>`tensor name above length ceiling`<br>`total element count above ceiling` | Stay within the library hard ceilings for counts, key lengths, and element totals. |
| `SafetensorError.BadDigest` | Malformed or mismatched digest. | `malformed digest value`<br>`malformed vocabulary digest` | Supply a well-formed digest (64-hex vocab digest / admitted algorithm) that matches the artifact. |
| `SafetensorError.BadMetadata` | Safetensors __metadata__ failure. | `duplicate __metadata__`<br>`malformed metadata member`<br>`malformed metadata separator`<br>`metadata must be a JSON object`<br>`metadata value must be a string`<br>`missing colon in metadata`<br>`missing required metadata key: …`<br>`trailing comma in metadata`<br>`unterminated metadata object` | Supply required metadata keys as strings; remove duplicates and trailing commas. |
| `SafetensorError.BadAdmission` | Capsule admission rejected from safetensors path. | `capsule admission rejected: …` | Read the suffix message for the underlying admission failure; fix that field and re-admit. |

## `gradus:nn` — `NnError`

Source: `src/nn.fab`. Render with module `message(e)`.

| Code | Class / when | Live messages (representative) | Resolution |
| --- | --- | --- | --- |
| `NnError.NegativeDimension` | Negative dimension in a shape or index. | `negative dimension` | Fix caller shapes, ranks, dtypes, and element counts so they satisfy the operation contract. |
| `NnError.DimensionAboveLimit` | A single dimension exceeds the module ceiling. | `dimension above ceiling` | Stay within the library hard ceilings for counts, key lengths, and element totals. |
| `NnError.ProductumSupraLimitem` | Element count (product of dims) exceeds the module ceiling. | `element count above ceiling` | Stay within the library hard ceilings for counts, key lengths, and element totals. |
| `NnError.GradusMismatch` | Rank / axis mismatch for the operation. | `layernorm requires rank >= 1`<br>`rmsnorm requires rank >= 1`<br>`linear requires rank-2 input`<br>`linear requires rank-2 weight`<br>`matmul requires rank-2 operands`<br>`swiglu requires rank-2 gate and up` | Fix caller shapes, ranks, dtypes, and element counts so they satisfy the operation contract. |
| `NnError.ShapeMismatch` | Shape mismatch between operands or against a required layout. | `bias does not match output shape`<br>`bias does not match output width`<br>`bias must be per-channel or output-shaped`<br>`layernorm offset must be per-channel`<br>`layernorm offset width mismatch`<br>`layernorm scale must be per-channel`<br>`layernorm scale width mismatch`<br>`rmsnorm scale must be per-channel`<br>`rmsnorm scale width mismatch`<br>`shapes not broadcastable`<br>`gate and up must share the same shape` | Fix caller shapes, ranks, dtypes, and element counts so they satisfy the operation contract. |
| `NnError.Incompatibilis` | Operands are not compatible under the operation rules. | `inner dimensions mismatch` | Fix caller shapes, ranks, dtypes, and element counts so they satisfy the operation contract. |
| `NnError.DtypeMismatch` | Dtype mismatch or unsupported dtype for this surface. | `dtype mismatch`<br>`unsupported dtype for nn primitive` | Fix caller shapes, ranks, dtypes, and element counts so they satisfy the operation contract. |
| `NnError.ElementMismatch` | Element-count / emptiness failure. | `empty normalization axis` | Fix caller shapes, ranks, dtypes, and element counts so they satisfy the operation contract. |
| `NnError.EpsilonInvalida` | Invalid (negative) epsilon. | `negative epsilon` | Correct the field to the documented admitted range and re-construct. |

## `gradus:optimize` — `OptimizeError`

Source: `src/optimize.fab`. Render with module `message(e)`.

| Code | Class / when | Live messages (representative) | Resolution |
| --- | --- | --- | --- |
| `OptimizeError.EmptyName` | Empty or reserved name / owner / identity field. | `empty state name`<br>`empty state owner`<br>`reserved wire character in name or owner` | Supply a non-empty name/owner with no reserved wire characters. |
| `OptimizeError.InvalidVersion` | Invalid or malformed version field. | `invalid state version` | Re-emit with the current schema stamp; never guess an unknown version. |
| `OptimizeError.InvalidGeneration` | Invalid generation counter on optimizer state. | `invalid generation` | Correct the field to the documented admitted range and re-construct. |
| `OptimizeError.InvalidStep` | Invalid optimizer step count. | `invalid step count` | Correct the field to the documented admitted range and re-construct. |
| `OptimizeError.InvalidRate` | Invalid learning rate. | `invalid learning rate` | Correct the field to the documented admitted range and re-construct. |
| `OptimizeError.IdentityMismatch` | Parameter / gradient / state identity fields disagree. | `gradient identity does not match the parameter`<br>`state identity does not match the parameter` | Match parameter/gradient/state identity fields; recompute gradients after any parameter mutation. |
| `OptimizeError.StaleGradient` | Stale gradient (parameter mutated since compute). | `stale gradient: parameter mutated since the gradient was computed` | Match parameter/gradient/state identity fields; recompute gradients after any parameter mutation. |
| `OptimizeError.Frozen` | Frozen-parameter / frozen-slot rule violation. | `frozen parameter cannot be optimized` | Do not mutate a frozen parameter; construct a trainable parameter instead. |
| `OptimizeError.ShapeMismatch` | Shape mismatch between operands or against a required layout. | `gradient shape does not match the parameter` | Fix caller shapes, ranks, dtypes, and element counts so they satisfy the operation contract. |
| `OptimizeError.Mutatio` | Disallowed mutation path. | _(reserved / mapped — no direct literal `iace` site; code is live on the `discretio`)_ | Use the documented mutation path only. |
| `OptimizeError.DuplicateName` | Duplicate registration of an identity. | `optimizer state already registered for that parameter` | Register each identity at most once. |
| `OptimizeError.UnknownName` | Unknown name (dtype, mode, identity lookup miss). | `no optimizer state for that parameter` | Look up an identity that was previously registered. |
| `OptimizeError.UnknownVersion` | Unknown or unsupported schema / file / marker version. | `unknown optimizer schema version` | Re-emit with the current schema stamp; never guess an unknown version. |
| `OptimizeError.BadWire` | Malformed wire / bytes / marker / field encoding. | `malformed generation in optimizer wire`<br>`malformed learning rate in optimizer wire`<br>`malformed optimizer wire`<br>`malformed optimizer wire header`<br>`malformed sgd-state wire`<br>`malformed slot count in optimizer wire`<br>`malformed state version in optimizer wire`<br>`malformed step count in optimizer wire`<br>`slot count mismatch in optimizer wire`<br>`unknown optimizer marker`<br>`unknown optimizer-state marker` | Re-emit with the current schema stamp; never guess an unknown version. |

## `gradus:parameter` — `ParametrumError`

Source: `src/parameter.fab`. Render with module `message(e)`.

| Code | Class / when | Live messages (representative) | Resolution |
| --- | --- | --- | --- |
| `ParametrumError.EmptyName` | Empty or reserved name / owner / identity field. | `empty parameter name`<br>`empty parameter owner` | Supply a non-empty name/owner with no reserved wire characters. |
| `ParametrumError.ReservedName` | Reserved wire character or invalid identity shape. | `reserved wire character in name or owner` | Supply a non-empty name/owner with no reserved wire characters. |
| `ParametrumError.UnknownDtype` | Unknown dtype name/tag or un-admitted type id. | _(reserved / mapped — no direct literal `iace` site; code is live on the `discretio`)_ | Correct the failing field per the message and re-invoke the fail-closed constructor. |
| `ParametrumError.InvalidShape` | Invalid shape at construction. | `invalid shape` | Fix caller shapes, ranks, dtypes, and element counts so they satisfy the operation contract. |
| `ParametrumError.ElementMismatch` | Element-count / emptiness failure. | `unreachable` (internal) | Fix caller shapes, ranks, dtypes, and element counts so they satisfy the operation contract. |
| `ParametrumError.FrozenMutation` | Mutation of a frozen parameter. | `frozen parameter cannot be mutated` | Do not mutate a frozen parameter; construct a trainable parameter instead. |
| `ParametrumError.DuplicateName` | Duplicate registration of an identity. | `parameter identity already registered` | Register each identity at most once. |
| `ParametrumError.UnknownName` | Unknown name (dtype, mode, identity lookup miss). | `no parameter with that identity` | Look up an identity that was previously registered. |
| `ParametrumError.InvalidVersion` | Invalid or malformed version field. | `invalid version in parameter identity`<br>`malformed version in parameter identity` | Re-emit with the current schema stamp; never guess an unknown version. |
| `ParametrumError.BadWire` | Malformed wire / bytes / marker / field encoding. | `empty name in parameter identity`<br>`empty owner in parameter identity`<br>`malformed dimension in parameter identity`<br>`malformed parameter identity`<br>`unknown identity marker`<br>`unknown parameter marker`<br>`unknown parameter schema version` | Re-emit with the current schema stamp; never guess an unknown version. |

## `gradus:sampling` — `SamplingError`

Source: `src/sampling.fab`. Render with module `message(e)`.

| Code | Class / when | Live messages (representative) | Resolution |
| --- | --- | --- | --- |
| `SamplingError.LogitsInvalida` | Logits vector invalid (empty or non-finite). | `logits must be finite`<br>`logits must be non-empty` | Provide a non-empty finite logits vector. |
| `SamplingError.InvalidConfig` | Generation / sampling / config field out of admitted range. | `min-p must be within [0, 1]`<br>`repetition penalty must be at least 1`<br>`temperature must be non-negative`<br>`top-k must be non-negative`<br>`top-p must be within [0, 1]` | Correct the field to the documented admitted range and re-construct. |
| `SamplingError.InvalidHistory` | History token invalid for sampling. | `history token out of vocabulary range` | Keep history tokens inside the vocabulary range. |

## `gradus:serialize` — `SerializeError`

Source: `src/serialize.fab`. Render with module `message(e)`.

| Code | Class / when | Live messages (representative) | Resolution |
| --- | --- | --- | --- |
| `SerializeError.UnknownVersion` | unknown magic / schema byte (version rejection). | `unknown serialize magic`<br>`unknown serialize schema version` | Re-emit with the current schema stamp; never guess an unknown version. |
| `SerializeError.GenusIgnotum` | unknown kind byte. | `unknown serialize kind` | Align the wire kind and element payload with the declared count and format. |
| `SerializeError.UnknownDtype` | unknown dtype name (serialize) or tag (deserialize). | `unknown dtype name: …`<br>`unknown dtype tag` | Use an admitted type/quantization row from the closed set; ensure block layouts tile. |
| `SerializeError.BadShape` | rank/dimension/element-count ceiling violations. | `element count above ceiling`<br>`negative dimension`<br>`rank above ceiling` | Stay within the library hard ceilings for counts, key lengths, and element totals. |
| `SerializeError.BadWire` | malformed bytes: truncation, bad length, invalid version | `empty parameter name`<br>`empty parameter owner`<br>`invalid UTF-8 text field`<br>`invalid parameter version`<br>`invalid version in serialized parameter`<br>`malformed dtype payload`<br>`malformed parameter payload`<br>`malformed shape payload`<br>`malformed tensor payload`<br>`reserved wire character in name or owner`<br>`serialized name too large`<br>`truncated header`<br>`truncated parameter data length`<br>`truncated parameter fields`<br>`truncated parameter name`<br>`truncated parameter owner`<br>`truncated parameter payload`<br>`truncated shape payload`<br>`truncated tensor data length`<br>`truncated tensor payload`<br>`truncated text field`<br>`unknown parameter status`<br>`unreachable` (internal) | Re-emit with the current schema stamp; never guess an unknown version. |
| `SerializeError.BadData` | element-data failures: count mismatch, malformed tokens. | `element count mismatch`<br>`element count mismatch in serialized data`<br>`malformed float token`<br>`missing element data`<br>`serialized data too large` | Align the wire kind and element payload with the declared count and format. |

## `gradus:shape` — `FormaError`

Source: `src/shape.fab`. Render with module `message(e)`.

| Code | Class / when | Live messages (representative) | Resolution |
| --- | --- | --- | --- |
| `FormaError.NegativeDimension` | Negative dimension in a shape or index. | `negative dimension` | Fix caller shapes, ranks, dtypes, and element counts so they satisfy the operation contract. |
| `FormaError.DimensionAboveLimit` | A single dimension exceeds the module ceiling. | _(reserved / mapped — no direct literal `iace` site; code is live on the `discretio`)_ | Fix caller shapes, ranks, dtypes, and element counts so they satisfy the operation contract. |
| `FormaError.ProductumSupraLimitem` | Element count (product of dims) exceeds the module ceiling. | `element count above ceiling` | Stay within the library hard ceilings for counts, key lengths, and element totals. |
| `FormaError.Incompatibilis` | Operands are not compatible under the operation rules. | `shapes not broadcastable` | Fix caller shapes, ranks, dtypes, and element counts so they satisfy the operation contract. |
| `FormaError.ElementMismatch` | Element-count / emptiness failure. | `at most one inferred dimension`<br>`element count mismatch`<br>`inferred dimension not integral`<br>`inferred dimension not resolvable` | Fix caller shapes, ranks, dtypes, and element counts so they satisfy the operation contract. |
| `FormaError.GradusMismatch` | Rank / axis mismatch for the operation. | `target rank above ceiling`<br>`target rank below current rank` | Stay within the library hard ceilings for counts, key lengths, and element totals. |

## `gradus:tensor` — `TensorError`

Source: `src/tensor.fab`. Render with module `message(e)`.

| Code | Class / when | Live messages (representative) | Resolution |
| --- | --- | --- | --- |
| `TensorError.InvalidShape` | Invalid shape at construction. | `negative dimension` | Fix caller shapes, ranks, dtypes, and element counts so they satisfy the operation contract. |
| `TensorError.ElementMismatch` | Element-count / emptiness failure. | `element count mismatch` | Fix caller shapes, ranks, dtypes, and element counts so they satisfy the operation contract. |
| `TensorError.TerminusExcedit` | Index or access exceeds the tensor bounds. | `empty tensor`<br>`index out of bounds`<br>`index rank mismatch`<br>`negative index` | Reduce the request or fix indices so they stay within the configured ceiling. |

## `gradus:tokenizer` — `TokenizerError`

Source: `src/tokenizer.fab`. Render with module `message(e)`.

| Code | Class / when | Live messages (representative) | Resolution |
| --- | --- | --- | --- |
| `TokenizerError.UnknownVersion` | unknown tokenizer identity schema version. | `unknown tokenizer identity schema version: …` | Re-emit with the current schema stamp; never guess an unknown version. |
| `TokenizerError.UnknownMergeKind` | un-admitted tokenizer kind (must be gpt2 / BBPE). | `un-admitted tokenizer kind: …` | Use the pinned tokenizer identity (gpt2/BBPE, pre=`smollm`, EOG `{0,2}`, BOS-free, space-prefix-free). |
| `TokenizerError.UnknownPreTokenizer` | un-admitted pre-tokenizer (must be smollm). | `un-admitted pre-tokenizer: …` | Use the pinned tokenizer identity (gpt2/BBPE, pre=`smollm`, EOG `{0,2}`, BOS-free, space-prefix-free). |
| `TokenizerError.BadVocab` | vocab / merges / specials count mismatch. | _(reserved / mapped — no direct literal `iace` site; code is live on the `discretio`)_ | Match the pinned vocabulary / merges / specials counts for the admitted row. |
| `TokenizerError.BadDigest` | malformed vocabulary digest (not 64-hex). | `malformed vocabulary digest` | Supply a well-formed digest (64-hex vocab digest / admitted algorithm) that matches the artifact. |
| `TokenizerError.BadEog` | malformed EOG set (must be {0, 2}). | `EOG set does not match the pinned row: …`<br>`malformed EOG set`<br>`pinned row is BOS-free`<br>`pinned row is BOS-free (add_bos_token = false)`<br>`pinned row is space-prefix-free`<br>`pinned row is space-prefix-free (add_space_prefix = false)` | Admit the exact pinned EOG set `{0,2}` (wire `"0,2"`, ascending). A well-formed-but-different set is a **different tokenizer**. For BOS/space messages: set `bos_vacua`/`spatium_vacua` to `verum` (pinned row is BOS-free and space-prefix-free). |
| `TokenizerError.IdExtra` | token id outside the admitted range [0, vocab). | `token id out of range: …` | Keep token ids in the admitted range for the row. |
| `TokenizerError.ProbeDivergens` | probe id list diverges from the pinned fixture | `tokenizer ids diverge from the pinned llama.cpp probe: …` | Re-admit against the pinned probe fixtures — divergence means a different tokenizer. |
| `TokenizerError.BadArtifact` | artifact tokenizer metadata is unavailable or malformed (LIB-02-U2 runtime). | `tokenizer array is unavailable: …`<br>`tokenizer metadata is unavailable: …`<br>`tokenizer vocabulary is empty` | Supply a schema-2 manifest whose tokenizer metadata block carries the tokens/merges arrays. |
| `TokenizerError.BadMerges` | malformed merge entry in the artifact. | `malformed merge entry: …` | A merge entry must be exactly `left right` (one space, non-empty halves) — the no-space-in-token invariant. |
| `TokenizerError.IdIgnotum` | unknown token id in decode (out of range). | `token id outside the vocabulary range: …` | Keep decoded ids within the artifact vocab range `[0, vocab)`. |
| `TokenizerError.UnknownTrace` | display character with no byte mapping (or byte piece missing from the vocab). | `display character has no byte mapping (codepoint …)`<br>`byte piece missing from the vocabulary: …` | The vocab must contain the 256 gpt2 byte tokens and only display-mapped characters. |
| `TokenizerError.BadUtf8` | byte sequence is not valid UTF-8 (decode output / display character). | `decoded byte sequence is not valid UTF-8`<br>`display character bytes are not valid UTF-8` | The byte-level decode is lossless only when every token's display characters map back to bytes that form valid UTF-8. |
| `TokenizerError.BadWire` | malformed tokenizer identity wire form. | `malformed pinned id list`<br>`malformed tokenizer identity wire form`<br>`non-digit token id in pinned fixture`<br>`tokenizer identity failed verification`<br>`unknown pinned probe: …`<br>`unknown tokenizer identity marker` | Re-emit with the current schema stamp; never guess an unknown version. |

The LIB-02 artifact-backed runtime (U2/U3) renders through the same
`TokenizerError` table; the composed two-probe completion oracle
(Probe A/B exact id lists, raw-prompt rows, decode round-trips) is pinned in
`fixtures/tokenizer/pinned-probe-oracle.md`. A divergence from those rows is
the campaign's stop condition (rule 5): the receipt names the first
divergent probe id or decoded character and routes the repair — the probe
rows never hard-code probe ids.

The capstone tokenizer phase (`exempla/qwen36-35b-inference`, LIB-02-U4-1)
runs the composed runtime through the public surface on the target
artifact and surfaces the same `TokenizerError` rows fail-closed; a probe
or decode divergence exits nonzero with the typed cause naming the first
divergent id/character.

## `gradus:train` — `TrainError`

Source: `src/train.fab`. Render with module `message(e)`.

| Code | Class / when | Live messages (representative) | Resolution |
| --- | --- | --- | --- |
| `TrainError.InvalidSchedule` | Learning-rate schedule construction failed. | `final learning rate above peak`<br>`invalid final learning rate`<br>`invalid peak learning rate`<br>`negative warmup steps`<br>`schedule horizon must be at least one step`<br>`warmup exceeds the schedule horizon` | Correct the field to the documented admitted range and re-construct. |
| `TrainError.UnknownMode` | Unknown train/eval mode name. | `unknown mode name` | Correct the field to the documented admitted range and re-construct. |
| `TrainError.ExcutioInvalida` | Invalid execution policy field (e.g. dropout rate). | `dropout rate must be in [0, 1]` | Correct the field to the documented admitted range and re-construct. |
| `TrainError.NegativeStep` | Negative schedule step. | `schedule step must be non-negative` | Correct the field to the documented admitted range and re-construct. |
| `TrainError.InvalidSeed` | Invalid RNG seed. | `seed must be non-zero` | Use a seed that meets the contract (non-zero / ≥ 1 as required). |
| `TrainError.BadPayload` | Malformed numeric value at a boundary. | _(reserved / mapped — no direct literal `iace` site; code is live on the `discretio`)_ | Reject NaN/malformed values at the boundary; re-export clean weights. |
| `TrainError.InvalidPosition` | Invalid position / epoch / step (negative or out of range). | `epoch must be non-negative`<br>`step must be non-negative` | Correct the field to the documented admitted range and re-construct. |
| `TrainError.EmptyState` | Empty checkpoint / state wire. | `checkpoint state wire is empty` | Provide a non-empty checkpoint wire produced by the current serialize path. |
| `TrainError.UnknownVersion` | Unknown or unsupported schema / file / marker version. | `unknown checkpoint schema version`<br>`unknown rng schema version` | Re-emit with the current schema stamp; never guess an unknown version. |
| `TrainError.BadWire` | Malformed wire / bytes / marker / field encoding. | `malformed checkpoint wire`<br>`malformed epoch in checkpoint wire`<br>`malformed rng state`<br>`malformed rng state in checkpoint wire`<br>`malformed rng wire`<br>`malformed step in checkpoint wire`<br>`unknown checkpoint marker`<br>`unknown rng marker` | Re-emit with the current schema stamp; never guess an unknown version. |

## `gradus:transformer` — `TransformerError`

Source: `src/transformer.fab`. Render with module `message(e)`.

Sub-call errors from `NnError` / `AttentionError` / `MathError` are mapped into `TransformerError` by message text (cross-module enum variants are not referenceable).

| Code | Class / when | Live messages (representative) | Resolution |
| --- | --- | --- | --- |
| `TransformerError.NegativeDimension` | Negative dimension in a shape or index. | `negative dimension` | Fix caller shapes, ranks, dtypes, and element counts so they satisfy the operation contract. |
| `TransformerError.DimensionAboveLimit` | A single dimension exceeds the module ceiling. | `dimension above ceiling` | Stay within the library hard ceilings for counts, key lengths, and element totals. |
| `TransformerError.ProductumSupraLimitem` | Element count (product of dims) exceeds the module ceiling. | `element count above ceiling` | Stay within the library hard ceilings for counts, key lengths, and element totals. |
| `TransformerError.GradusMismatch` | Rank / axis mismatch for the operation. | `attention requires rank-2 tensors`<br>`layernorm requires rank >= 1`<br>`linear requires rank-2 input`<br>`linear requires rank-2 weight`<br>`matmul requires rank-2 operands`<br>`multi-head attention requires rank-2 tensors`<br>`rmsnorm requires rank >= 1`<br>`swiglu requires rank-2 gate and up` | Fix caller shapes, ranks, dtypes, and element counts so they satisfy the operation contract. |
| `TransformerError.ShapeMismatch` | Shape mismatch between operands or against a required layout. | _(reserved / mapped — no direct literal `iace` site; code is live on the `discretio`)_ | Fix caller shapes, ranks, dtypes, and element counts so they satisfy the operation contract. |
| `TransformerError.Incompatibilis` | Operands are not compatible under the operation rules. | `inner dimensions mismatch` | Fix caller shapes, ranks, dtypes, and element counts so they satisfy the operation contract. |
| `TransformerError.DtypeMismatch` | Dtype mismatch or unsupported dtype for this surface. | `dtype mismatch`<br>`unsupported dtype for attention primitive`<br>`unsupported dtype for nn primitive` | Fix caller shapes, ranks, dtypes, and element counts so they satisfy the operation contract. |
| `TransformerError.ElementMismatch` | Element-count / emptiness failure. | `empty attention input`<br>`empty normalization axis` | Fix caller shapes, ranks, dtypes, and element counts so they satisfy the operation contract. |
| `TransformerError.EpsilonInvalida` | Invalid (negative) epsilon. | `negative epsilon` | Correct the field to the documented admitted range and re-construct. |
| `TransformerError.InvalidPosition` | Invalid position / epoch / step (negative or out of range). | `negative position` | Correct the field to the documented admitted range and re-construct. |
| `TransformerError.InvalidDimension` | Invalid dimension parameter (e.g. RoPE dim, embedding width). | `rope dim exceeds head width`<br>`rope dim must be at least 2`<br>`rope dim must be even` | Correct the field to the documented admitted range and re-construct. |
| `TransformerError.InvalidMode` | Unknown attention / block mode. | `unknown attention mode` | Correct the field to the documented admitted range and re-construct. |

## Validation

Every code in this document must resolve to a live `discretio` variant under `src/`:

```bash
# Resolve one code: TokenizerError.BadEog
rg -n 'BadEog' src/tokenizer.fab
# Count public error discrim
rg -n '^discretio \w+Error' src --glob '*.fab'
```

Discipline: for each `ErrorType.Variant` row, `Variant` appears inside `discretio ErrorType { … }` in the listed source file. Representative messages are substrings of live `message = "…"` (or mapped `message = c` texts) in that file.

## Related

- API reference: [`docs/api-reference.md`](api-reference.md) (PML6-U1)
- Module map: [`docs/module-map.md`](module-map.md)
- Support matrix: [`docs/factory/production-ml-library/pml0-support-matrix.md`](factory/production-ml-library/pml0-support-matrix.md)
- Compatibility policy: [`docs/compatibility-policy.md`](compatibility-policy.md) (PML6-U3, when present)
- Exempla: `exempla/*/README.md`
