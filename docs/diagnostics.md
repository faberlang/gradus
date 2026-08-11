# Gradus diagnostics map

**Document**: `gradus-diagnostics v1.0.0`
**Campaign unit**: PML6-U2
**Status**: structural (live `src/**/*.fab` surface; no executed-tier claim)
**Scope**: every public typed error `discretio` — code + message + resolution

## Contract

- **Code** = `ErrorType.Variant`. Stable identity is the `discretio` case name. Codes do not change without a named compatibility note.
- **Message** = the `textus causa` on the variant, rendered by `causa(e)`. Messages are locale-ready English. Dynamic suffixes (appended names, versions, counts) are written as a trailing `…` when the live source concatenates.
- **Resolution** = the closed action that makes the call succeed. Gradus fails closed — no silent coercion.
- **Reserved / mapped variants**: some variants exist for cross-module mapping or class coverage and have no direct `iace finge "…"` literal site; they still have stable codes. Mapped facades (e.g. `GradusError`, `TransformerError`) preserve the underlying causa text.
- **Executed tier**: this map documents fail-closed identity on the compiled surface. Proba execution and exempla e2e runs remain on the FMIR lever (CTO8-1) until that gate opens — this document never claims executed runs.

## EOG identity — `TokenizerError.EogMala`

EOG-set mismatch is **tokenizer identity**, not a value error (correctness wave `2cdc498` / `6cc0eb5` / capsule exact pin `{0,2}`).

| Code | Live messages | Resolution |
| --- | --- | --- |
| `TokenizerError.EogMala` | `malformed EOG set`<br>`EOG set does not match the pinned row: …`<br>`pinned row is BOS-free (add_bos_token = false)` / `pinned row is BOS-free`<br>`pinned row is space-prefix-free (add_space_prefix = false)` / `pinned row is space-prefix-free` | Admit the **exact** pinned EOG set `{0,2}` (wire form `"0,2"`, strictly ascending non-negative ids). A well-formed-but-different set is a **different tokenizer**. BOS / space-prefix polarity: pinned row is BOS-free and space-prefix-free — `bos_vacua` and `spatium_vacua` must be `verum` (guards use `≡` against the falsum add-* flags). Capsule admission surfaces the same identity failure as `AdmissionError.TokenizerMala` with message `invalid tokenizer identity`. |

Generation stop-policy binds the same identity via `tokenizator.est_eog` (admitted EOG tokens `{0, 2}`): generation terminates after the **first** admitted EOG token; `maxima_verborum` is a ceiling, never a promise to emit that many tokens (`0d50d60`).

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
| `gradus:attention` | `AttentionError` | 10 | `src/attention.fab` |
| `gradus:cache` | `CacheError` | 8 | `src/cache.fab` |
| `gradus:decode` | `DecodeError` | 11 | `src/decode.fab` |
| `gradus:dtype` | `DTypeError` | 4 | `src/dtype.fab` |
| `gradus:generation` | `GeneratioError` | 7 | `src/generation.fab` |
| `gradus:gradient` | `GradienteError` | 2 | `src/gradient.fab` |
| `gradus:gradus` | `GradusError` | 8 | `src/gradus.fab` |
| `gradus:loss` | `LossError` | 9 | `src/loss.fab` |
| `gradus:math` | `MathError` | 11 | `src/math.fab` |
| `gradus:metrics` | `MetricError` | 7 | `src/metrics.fab` |
| `gradus:model/capsule` | `AdmissionError` | 9 | `src/model/capsule.fab` |
| `gradus:model/dequant` | `DequantError` | 4 | `src/model/dequant.fab` |
| `gradus:model/gguf` | `GgufError` | 10 | `src/model/gguf.fab` |
| `gradus:model/safetensors` | `SafetensorError` | 11 | `src/model/safetensors.fab` |
| `gradus:nn` | `NnError` | 9 | `src/nn.fab` |
| `gradus:optimize` | `OptimizeError` | 14 | `src/optimize.fab` |
| `gradus:parameter` | `ParametrumError` | 10 | `src/parameter.fab` |
| `gradus:sampling` | `SamplingError` | 3 | `src/sampling.fab` |
| `gradus:serialize` | `SerializeError` | 6 | `src/serialize.fab` |
| `gradus:shape` | `FormaError` | 6 | `src/shape.fab` |
| `gradus:tensor` | `TensorError` | 3 | `src/tensor.fab` |
| `gradus:tokenizer` | `TokenizerError` | 9 | `src/tokenizer.fab` |
| `gradus:train` | `TrainError` | 10 | `src/train.fab` |
| `gradus:transformer` | `TransformerError` | 12 | `src/transformer.fab` |

**Total**: 193 public error codes across 24 error types.

## `gradus:attention` — `AttentionError`

Source: `src/attention.fab`. Render with module `causa(e)`.

| Code | Class / when | Live messages (representative) | Resolution |
| --- | --- | --- | --- |
| `AttentionError.DimensioNegativa` | Negative dimension in a shape or index. | `negative dimension` | Fix caller shapes, ranks, dtypes, and element counts so they satisfy the operation contract. |
| `AttentionError.DimensioSupraLimitem` | A single dimension exceeds the module ceiling. | `dimension above ceiling` | Stay within the library hard ceilings for counts, key lengths, and element totals. |
| `AttentionError.ProductumSupraLimitem` | Element count (product of dims) exceeds the module ceiling. | `element count above ceiling` | Stay within the library hard ceilings for counts, key lengths, and element totals. |
| `AttentionError.GradusMismatch` | Rank / axis mismatch for the operation. | `attention requires rank-2 tensors`<br>`matmul requires rank-2 operands`<br>`rope requires rank-2 tensor` | Fix caller shapes, ranks, dtypes, and element counts so they satisfy the operation contract. |
| `AttentionError.FormaMismatch` | Shape mismatch between operands or against a required layout. | `positions must match the token count`<br>`query, key, value must share shape`<br>`shapes not broadcastable` | Fix caller shapes, ranks, dtypes, and element counts so they satisfy the operation contract. |
| `AttentionError.Incompatibilis` | Operands are not compatible under the operation rules. | `inner dimensions mismatch` | Fix caller shapes, ranks, dtypes, and element counts so they satisfy the operation contract. |
| `AttentionError.TypoMismatch` | Dtype mismatch or unsupported dtype for this surface. | `dtype mismatch`<br>`unsupported dtype for attention primitive` | Fix caller shapes, ranks, dtypes, and element counts so they satisfy the operation contract. |
| `AttentionError.ElementaMismatch` | Element-count / emptiness failure. | `empty attention input`<br>`empty rope input` | Fix caller shapes, ranks, dtypes, and element counts so they satisfy the operation contract. |
| `AttentionError.PositioInvalida` | Invalid position / epoch / step (negative or out of range). | `negative position` | Correct the field to the documented admitted range and re-construct. |
| `AttentionError.DimensioInvalida` | Invalid dimension parameter (e.g. RoPE dim, embedding width). | `rope dim exceeds head width`<br>`rope dim must be at least 2`<br>`rope dim must be even` | Correct the field to the documented admitted range and re-construct. |

## `gradus:cache` — `CacheError`

Source: `src/cache.fab`. Render with module `causa(e)`.

| Code | Class / when | Live messages (representative) | Resolution |
| --- | --- | --- | --- |
| `CacheError.NomenInane` | Empty or reserved name / owner / identity field. | `empty execution config`<br>`empty model name`<br>`empty model version`<br>`empty tokenizer identity`<br>`reserved wire character in identity` | Use the pinned tokenizer identity (gpt2/BBPE, pre=`smollm`, EOG `{0,2}`, BOS-free, space-prefix-free). |
| `CacheError.IdExtra` | Token id outside the admitted range. | `token id must be non-negative` | Keep token ids in the admitted range for the row. |
| `CacheError.FormaMismatch` | Shape mismatch between operands or against a required layout. | `K must be [1, dim]`<br>`V must be [1, dim]` | Fix caller shapes, ranks, dtypes, and element counts so they satisfy the operation contract. |
| `CacheError.TypoMismatch` | Dtype mismatch or unsupported dtype for this surface. | `unsupported dtype for cache` | Fix caller shapes, ranks, dtypes, and element counts so they satisfy the operation contract. |
| `CacheError.DimensioInvalida` | Invalid dimension parameter (e.g. RoPE dim, embedding width). | `embedding dimension must be at least one`<br>`layer count must be at least one` | Correct the field to the documented admitted range and re-construct. |
| `CacheError.ElementaMismatch` | Element-count / emptiness failure. | `unreachable` (internal) | Fix caller shapes, ranks, dtypes, and element counts so they satisfy the operation contract. |
| `CacheError.VersioIgnota` | Unknown or unsupported schema / file / marker version. | `unknown cache schema version` | Re-emit with the current schema stamp; never guess an unknown version. |
| `CacheError.WireMala` | Malformed wire / bytes / marker / field encoding. | `empty dtype in cache identity`<br>`empty execution config in cache identity`<br>`empty layout in cache identity`<br>`empty model name in cache identity`<br>`empty model version in cache identity`<br>`empty tokenizer identity in cache identity`<br>`invalid layer count in cache identity`<br>`malformed cache identity wire`<br>`malformed layer count in cache identity`<br>`malformed position span in cache identity`<br>`unknown cache marker` | Re-emit with the current schema stamp; never guess an unknown version. |

## `gradus:decode` — `DecodeError`

Source: `src/decode.fab`. Render with module `causa(e)`.

| Code | Class / when | Live messages (representative) | Resolution |
| --- | --- | --- | --- |
| `DecodeError.IdExtra` | Token id outside the admitted range. | `token id out of vocabulary range` | Keep token ids in the admitted range for the row. |
| `DecodeError.PositioInvalida` | Invalid position / epoch / step (negative or out of range). | `position out of context`<br>`prompt exceeds the context limit` | Correct the field to the documented admitted range and re-construct. |
| `DecodeError.Terminus` | A configured ceiling was reached (context, tokens, …). | `context limit reached` | Reduce the request or fix indices so they stay within the configured ceiling. |
| `DecodeError.DecodereInvalida` | Decode model / config construction failed. | `context length must be at least one`<br>`embedding columns must equal the dimension`<br>`embedding dimension must be at least one`<br>`embedding must be rank-2`<br>`embedding rows must equal the vocabulary`<br>`invalid attention scale`<br>`output projection bias must be [vocab]`<br>`output projection must be rank-2`<br>`output projection shape must be [dim, vocab]`<br>`vocabulary must be non-empty` | Correct the field to the documented admitted range and re-construct. |
| `DecodeError.FormaMismatch` | Shape mismatch between operands or against a required layout. | `bias does not match output width` | Fix caller shapes, ranks, dtypes, and element counts so they satisfy the operation contract. |
| `DecodeError.TypoMismatch` | Dtype mismatch or unsupported dtype for this surface. | `dtype mismatch` | Fix caller shapes, ranks, dtypes, and element counts so they satisfy the operation contract. |
| `DecodeError.ElementaMismatch` | Element-count / emptiness failure. | `empty prompt`<br>`unreachable` (internal) | Fix caller shapes, ranks, dtypes, and element counts so they satisfy the operation contract. |
| `DecodeError.Incompatibilis` | Operands are not compatible under the operation rules. | `inner dimensions mismatch` | Fix caller shapes, ranks, dtypes, and element counts so they satisfy the operation contract. |
| `DecodeError.DimensioInvalida` | Invalid dimension parameter (e.g. RoPE dim, embedding width). | `unknown attention mode` | Correct the field to the documented admitted range and re-construct. |
| `DecodeError.Cancelata` | Cooperative cancellation requested. | `cancellation requested` | Clear the cancellation flag or end the run; cancellation fails closed. |
| `DecodeError.SamplingDefecta` | Sampling step failed (mapped). | _(reserved / mapped — no direct literal `iace` site; code is live on the `discretio`)_ | Fix the sampling configuration or logits before drawing. |

## `gradus:dtype` — `DTypeError`

Source: `src/dtype.fab`. Render with module `causa(e)`.

| Code | Class / when | Live messages (representative) | Resolution |
| --- | --- | --- | --- |
| `DTypeError.NomenIgnotum` | Unknown name (dtype, mode, identity lookup miss). | `unknown dtype name: …` | Correct the failing field per the message and re-invoke the fail-closed constructor. |
| `DTypeError.VersioIgnota` | Unknown or unsupported schema / file / marker version. | `malformed dtype serialization`<br>`unknown dtype marker`<br>`unknown dtype schema version` | Re-emit with the current schema stamp; never guess an unknown version. |
| `DTypeError.NonFinita` | Non-finite value (NaN/Inf) rejected. | `non-finite value in cast to i32`<br>`non-finite value in cast to u8` | Ensure inputs are finite; reject NaN/Inf at the boundary. |
| `DTypeError.Superfluitas` | Value overflows the destination type range. | `f16 overflow in cast`<br>`i32 overflow in cast`<br>`u8 overflow in cast` | Cast or clamp into the destination type's finite range. |

## `gradus:generation` — `GeneratioError`

Source: `src/generation.fab`. Render with module `causa(e)`.

| Code | Class / when | Live messages (representative) | Resolution |
| --- | --- | --- | --- |
| `GeneratioError.ConfiguraInvalida` | Generation / sampling / config field out of admitted range. | `context length must be at least one`<br>`maximum generated tokens must be at least one`<br>`maximum generated tokens must fit within the context`<br>`min-p must be within [0, 1]`<br>`prompt batch size must be at least one`<br>`repetition penalty must be at least one`<br>`seed must be at least one`<br>`temperature must be non-negative`<br>`top-k must be non-negative`<br>`top-p must be within [0, 1]`<br>`unreachable` (internal) | Use a seed that meets the contract (non-zero / ≥ 1 as required). |
| `GeneratioError.ElementaMismatch` | Element-count / emptiness failure. | _(reserved / mapped — no direct literal `iace` site; code is live on the `discretio`)_ | Fix caller shapes, ranks, dtypes, and element counts so they satisfy the operation contract. |
| `GeneratioError.TypoMismatch` | Dtype mismatch or unsupported dtype for this surface. | _(reserved / mapped — no direct literal `iace` site; code is live on the `discretio`)_ | Fix caller shapes, ranks, dtypes, and element counts so they satisfy the operation contract. |
| `GeneratioError.Incompatibilis` | Operands are not compatible under the operation rules. | _(reserved / mapped — no direct literal `iace` site; code is live on the `discretio`)_ | Fix caller shapes, ranks, dtypes, and element counts so they satisfy the operation contract. |
| `GeneratioError.VersioIgnota` | Unknown or unsupported schema / file / marker version. | `unknown generation schema version` | Re-emit with the current schema stamp; never guess an unknown version. |
| `GeneratioError.WireMala` | Malformed wire / bytes / marker / field encoding. | `malformed context length in generation wire`<br>`malformed generation config wire`<br>`malformed max tokens in generation wire`<br>`malformed min-p in generation wire`<br>`malformed prompt batch in generation wire`<br>`malformed repetition penalty in generation wire`<br>`malformed seed in generation wire`<br>`malformed temperature in generation wire`<br>`malformed top-k in generation wire`<br>`malformed top-p in generation wire`<br>`unknown generation marker` | Re-emit with the current schema stamp; never guess an unknown version. |
| `GeneratioError.Terminus` | A configured ceiling was reached (context, tokens, …). | `context limit reached`<br>`maximum generated tokens reached` | Reduce the request or fix indices so they stay within the configured ceiling. |

## `gradus:gradient` — `GradienteError`

Source: `src/gradient.fab`. Render with module `causa(e)`.

| Code | Class / when | Live messages (representative) | Resolution |
| --- | --- | --- | --- |
| `GradienteError.GradusIgnotum` | Unknown or empty gradient identity field. | `empty gradient name`<br>`empty gradient owner`<br>`no gradient for that parameter identity` | Supply a non-empty name/owner with no reserved wire characters. |
| `GradienteError.GradusVersio` | Invalid gradient generation counter. | `invalid gradient generation` | Supply a non-empty gradient owner/name and a valid generation counter. |

## `gradus:gradus` — `GradusError`

Source: `src/gradus.fab`. Render with module `causa(e)`.

Facade: `_mappa` preserves nn causa texts into these variants (text unchanged). Unmapped nn texts fall through to `FormaMismatch`.

| Code | Class / when | Live messages (representative) | Resolution |
| --- | --- | --- | --- |
| `GradusError.DimensioNegativa` | Negative dimension in a shape or index. | `negative dimension` | Fix caller shapes, ranks, dtypes, and element counts so they satisfy the operation contract. |
| `GradusError.DimensioSupraLimitem` | A single dimension exceeds the module ceiling. | `dimension above ceiling` | Stay within the library hard ceilings for counts, key lengths, and element totals. |
| `GradusError.ProductumSupraLimitem` | Element count (product of dims) exceeds the module ceiling. | `element count above ceiling` | Stay within the library hard ceilings for counts, key lengths, and element totals. |
| `GradusError.GradusMismatch` | Rank / axis mismatch for the operation. | `linear requires rank-2 input`<br>`linear requires rank-2 weight` | Fix caller shapes, ranks, dtypes, and element counts so they satisfy the operation contract. |
| `GradusError.FormaMismatch` | Shape mismatch between operands or against a required layout. | `bias does not match output shape`<br>`bias does not match output width`<br>`bias must be per-channel or output-shaped` | Fix caller shapes, ranks, dtypes, and element counts so they satisfy the operation contract. |
| `GradusError.Incompatibilis` | Operands are not compatible under the operation rules. | `inner dimensions mismatch` | Fix caller shapes, ranks, dtypes, and element counts so they satisfy the operation contract. |
| `GradusError.TypoMismatch` | Dtype mismatch or unsupported dtype for this surface. | `dtype mismatch`<br>`unsupported dtype for nn primitive` | Fix caller shapes, ranks, dtypes, and element counts so they satisfy the operation contract. |
| `GradusError.ElementaMismatch` | Element-count / emptiness failure. | _(reserved / mapped — no direct literal `iace` site; code is live on the `discretio`)_ | Fix caller shapes, ranks, dtypes, and element counts so they satisfy the operation contract. |

## `gradus:loss` — `LossError`

Source: `src/loss.fab`. Render with module `causa(e)`.

| Code | Class / when | Live messages (representative) | Resolution |
| --- | --- | --- | --- |
| `LossError.DimensioNegativa` | Negative dimension in a shape or index. | `negative dimension` | Fix caller shapes, ranks, dtypes, and element counts so they satisfy the operation contract. |
| `LossError.DimensioSupraLimitem` | A single dimension exceeds the module ceiling. | `dimension above ceiling` | Stay within the library hard ceilings for counts, key lengths, and element totals. |
| `LossError.ProductumSupraLimitem` | Element count (product of dims) exceeds the module ceiling. | `element count above ceiling` | Stay within the library hard ceilings for counts, key lengths, and element totals. |
| `LossError.GradusMismatch` | Rank / axis mismatch for the operation. | `cross_entropy requires rank-2 logits`<br>`cross_entropy target must be rank-1` | Provide a non-empty finite logits vector. |
| `LossError.FormaMismatch` | Shape mismatch between operands or against a required layout. | `prediction and target shapes differ`<br>`target length does not match logits rows` | Provide a non-empty finite logits vector. |
| `LossError.TypoMismatch` | Dtype mismatch or unsupported dtype for this surface. | `cross_entropy target must be i32 class indices`<br>`dtype mismatch`<br>`unsupported dtype for loss` | Fix caller shapes, ranks, dtypes, and element counts so they satisfy the operation contract. |
| `LossError.ElementaMismatch` | Element-count / emptiness failure. | `empty batch`<br>`empty class axis`<br>`empty loss input` | Fix caller shapes, ranks, dtypes, and element counts so they satisfy the operation contract. |
| `LossError.Incompatibilis` | Operands are not compatible under the operation rules. | `target class out of range`<br>`target must be integer class indices` | Keep token ids in the admitted range for the row. |
| `LossError.NonFinita` | Non-finite value (NaN/Inf) rejected. | `non-finite logits`<br>`non-finite prediction`<br>`non-finite target` | Provide a non-empty finite logits vector. |

## `gradus:math` — `MathError`

Source: `src/math.fab`. Render with module `causa(e)`.

| Code | Class / when | Live messages (representative) | Resolution |
| --- | --- | --- | --- |
| `MathError.DimensioNegativa` | Negative dimension in a shape or index. | `negative dimension` | Fix caller shapes, ranks, dtypes, and element counts so they satisfy the operation contract. |
| `MathError.DimensioSupraLimitem` | A single dimension exceeds the module ceiling. | `dimension above ceiling` | Stay within the library hard ceilings for counts, key lengths, and element totals. |
| `MathError.ProductumSupraLimitem` | Element count (product of dims) exceeds the module ceiling. | `element count above ceiling` | Stay within the library hard ceilings for counts, key lengths, and element totals. |
| `MathError.FormaMismatch` | Shape mismatch between operands or against a required layout. | _(reserved / mapped — no direct literal `iace` site; code is live on the `discretio`)_ | Fix caller shapes, ranks, dtypes, and element counts so they satisfy the operation contract. |
| `MathError.GradusMismatch` | Rank / axis mismatch for the operation. | `axis out of range`<br>`concat rank mismatch`<br>`concat requires rank >= 1`<br>`matmul requires rank-2 operands`<br>`reduce requires rank >= 1`<br>`slice requires rank >= 1` | Keep token ids in the admitted range for the row. |
| `MathError.Incompatibilis` | Operands are not compatible under the operation rules. | `concat dimension mismatch`<br>`inner dimensions mismatch`<br>`slice bounds out of range` | Keep token ids in the admitted range for the row. |
| `MathError.TypoMismatch` | Dtype mismatch or unsupported dtype for this surface. | `dtype mismatch` | Fix caller shapes, ranks, dtypes, and element counts so they satisfy the operation contract. |
| `MathError.ElementaMismatch` | Element-count / emptiness failure. | `element count mismatch`<br>`empty concat list`<br>`empty reduction axis` | Fix caller shapes, ranks, dtypes, and element counts so they satisfy the operation contract. |
| `MathError.NonFinita` | Non-finite value (NaN/Inf) rejected. | `non-finite value in cast to i32`<br>`non-finite value in cast to u8` | Ensure inputs are finite; reject NaN/Inf at the boundary. |
| `MathError.Superfluitas` | Value overflows the destination type range. | _(reserved / mapped — no direct literal `iace` site; code is live on the `discretio`)_ | Cast or clamp into the destination type's finite range. |
| `MathError.NomenIgnotum` | Unknown name (dtype, mode, identity lookup miss). | _(reserved / mapped — no direct literal `iace` site; code is live on the `discretio`)_ | Correct the failing field per the message and re-invoke the fail-closed constructor. |

## `gradus:metrics` — `MetricError`

Source: `src/metrics.fab`. Render with module `causa(e)`.

| Code | Class / when | Live messages (representative) | Resolution |
| --- | --- | --- | --- |
| `MetricError.GradusMismatch` | Rank / axis mismatch for the operation. | `accuracy requires rank-2 predictions`<br>`accuracy target must be rank-1` | Fix caller shapes, ranks, dtypes, and element counts so they satisfy the operation contract. |
| `MetricError.FormaMismatch` | Shape mismatch between operands or against a required layout. | `target length does not match predictions rows` | Fix caller shapes, ranks, dtypes, and element counts so they satisfy the operation contract. |
| `MetricError.TypoMismatch` | Dtype mismatch or unsupported dtype for this surface. | `accuracy target must be i32 class indices`<br>`unsupported dtype for metric` | Fix caller shapes, ranks, dtypes, and element counts so they satisfy the operation contract. |
| `MetricError.ElementaMismatch` | Element-count / emptiness failure. | `empty batch`<br>`empty class axis` | Fix caller shapes, ranks, dtypes, and element counts so they satisfy the operation contract. |
| `MetricError.NonFinita` | Non-finite value (NaN/Inf) rejected. | `non-finite prediction`<br>`non-finite target` | Ensure inputs are finite; reject NaN/Inf at the boundary. |
| `MetricError.Incompatibilis` | Operands are not compatible under the operation rules. | `target class out of range`<br>`target must be integer class indices` | Keep token ids in the admitted range for the row. |
| `MetricError.Invalida` | Metric record field out of range. | `accuracy must be finite`<br>`accuracy must be in [0, 1]`<br>`loss must be finite` | Keep metric fields finite and inside the documented range (loss finite; accuracy in [0,1]). |

## `gradus:model/capsule` — `AdmissionError`

Source: `src/model/capsule.fab`. Render with module `causa(e)`.

| Code | Class / when | Live messages (representative) | Resolution |
| --- | --- | --- | --- |
| `AdmissionError.VersioIgnota` | unknown capsule schema version (reject, no partial | `unknown capsule schema version: …` | Re-emit with the current schema stamp; never guess an unknown version. |
| `AdmissionError.AlgorithmusIgnotus` | Unknown digest algorithm. | `unknown digest algorithm: …` | Supply a well-formed digest (64-hex vocab digest / admitted algorithm) that matches the artifact. |
| `AdmissionError.DigestioMala` | malformed digest value (format / length / charset) | `digest mismatch — capsule does not match the expected artifact`<br>`malformed digest value`<br>`malformed vocabulary digest` | Supply a well-formed digest (64-hex vocab digest / admitted algorithm) that matches the artifact. |
| `AdmissionError.BytesMala` | byte payload failures: empty payload, failed | `capsule failed verification`<br>`data-region coverage did not pass`<br>`data-region coverage did not pass — gapped or overlapping region`<br>`empty validated byte payload`<br>`invalid byte length in capsule identity`<br>`recorded byte length does not match the validated payload` | Provide a payload whose lengths/offsets match the layout (exact tile, no gaps/overlaps). |
| `AdmissionError.TokenizerMala` | malformed tokenizer identity (empty kind / | `invalid tokenizer identity` | Use the pinned tokenizer identity (gpt2/BBPE, pre=`smollm`, EOG `{0,2}`, BOS-free, space-prefix-free). |
| `AdmissionError.QuantizatioIgnota` | unknown quantization row or mis-laid-out block | `unknown or mis-laid-out quantization row: …`<br>`unknown quantization row: …` | Use an admitted type/quantization row from the closed set; ensure block layouts tile. |
| `AdmissionError.LimitesMala` | ceilings outside the library's hard limits or a | `invalid bounds ceilings` | Stay within the library hard ceilings for counts, key lengths, and element totals. |
| `AdmissionError.ArchitecturaMala` | malformed architecture facts. | `empty architecture identifier`<br>`invalid architecture facts`<br>`invalid layer count in capsule identity` | Match the admitted architecture facts (arch, layers, context, vocab, embedding). |
| `AdmissionError.WireMala` | malformed capsule identity wire form. | `malformed capsule identity wire form`<br>`malformed numeric field`<br>`numeric field above the integer carrier`<br>`unknown capsule identity marker`<br>`unreachable` (internal) | Re-emit with the current schema stamp; never guess an unknown version. |

## `gradus:model/dequant` — `DequantError`

Source: `src/model/dequant.fab`. Render with module `causa(e)`.

| Code | Class / when | Live messages (representative) | Resolution |
| --- | --- | --- | --- |
| `DequantError.TypoIgnotum` | un-admitted / unknown GGML type id. | `un-admitted GGML type id: …`<br>`unreachable` (internal) | Use an admitted type/quantization row from the closed set; ensure block layouts tile. |
| `DequantError.GlomulusMala` | block byte length != the layout's block_bytes. | `block byte length mismatch` | Provide a payload whose lengths/offsets match the layout (exact tile, no gaps/overlaps). |
| `DequantError.OrdoMala` | row byte length not a multiple of block_bytes. | `row byte length not a multiple of block_bytes` | Provide a payload whose lengths/offsets match the layout (exact tile, no gaps/overlaps). |
| `DequantError.ValorMala` | malformed value (NaN half) fails closed. | `NaN f32 value in dequant block`<br>`NaN half in dequant block` | Ensure inputs are finite; reject NaN/Inf at the boundary. |

## `gradus:model/gguf` — `GgufError`

Source: `src/model/gguf.fab`. Render with module `causa(e)`.

| Code | Class / when | Live messages (representative) | Resolution |
| --- | --- | --- | --- |
| `GgufError.FormatMala` | bad magic (not a GGUF file). | `not a GGUF file — bad magic` | Provide a well-formed file with the expected magic and version. |
| `GgufError.VersioIgnota` | unsupported GGUF file version. | `unsupported GGUF file version: …` | Re-emit with the current schema stamp; never guess an unknown version. |
| `GgufError.ArchitecturaMala` | architecture facts (arch id, layers, context, | `architecture mismatch`<br>`context length mismatch`<br>`embedding size mismatch`<br>`layer count mismatch`<br>`missing required metadata key: general.architecture`<br>`missing required metadata key: llama.block_count`<br>`missing required metadata key: llama.context_length`<br>`missing required metadata key: llama.embedding_length`<br>`missing required metadata key: llama.vocab_size`<br>`vocabulary size mismatch` | Match the admitted architecture facts (arch, layers, context, vocab, embedding). |
| `GgufError.QuantizatioIgnota` | Unknown or mis-laid-out quantization row. | `file type mismatch`<br>`missing required metadata key: general.file_type`<br>`missing required metadata key: general.quantization_version`<br>`quantization version mismatch`<br>`tensor byte size not a multiple of the 32-byte data alignment`<br>`tensor size not a multiple of its block layout`<br>`tensor type count mismatch`<br>`unknown ggml tensor type` | Use an admitted type/quantization row from the closed set; ensure block layouts tile. |
| `GgufError.OffsetMala` | tensor offsets / data-region tiling (coverage). | `data region does not tile exactly`<br>`tensor offsets are not contiguous` | Provide a payload whose lengths/offsets match the layout (exact tile, no gaps/overlaps). |
| `GgufError.FormaMala` | shapes: rank, dims, total element count. | `invalid tensor dimension`<br>`tensor element count above the expected total`<br>`total element count above the expected total`<br>`total element count mismatch`<br>`unsupported tensor rank` | Stay within the library hard ceilings for counts, key lengths, and element totals. |
| `GgufError.TokenizerMala` | tokenizer identity facts. | `add_bos_token mismatch`<br>`add_space_prefix mismatch`<br>`bos token id mismatch`<br>`eos token id mismatch`<br>`missing required metadata key: tokenizer.ggml.add_bos_token`<br>`missing required metadata key: tokenizer.ggml.add_space_prefix`<br>`missing required metadata key: tokenizer.ggml.bos_token_id`<br>`missing required metadata key: tokenizer.ggml.eos_token_id`<br>`missing required metadata key: tokenizer.ggml.model`<br>`missing required metadata key: tokenizer.ggml.padding_token_id`<br>`missing required metadata key: tokenizer.ggml.pre`<br>`missing required metadata key: tokenizer.ggml.unknown_token_id`<br>`padding token id mismatch`<br>`tokenizer model mismatch`<br>`tokenizer pre-tokenizer mismatch`<br>`unknown token id mismatch` | Use the pinned tokenizer identity (gpt2/BBPE, pre=`smollm`, EOG `{0,2}`, BOS-free, space-prefix-free). |
| `GgufError.LimitesMala` | count ceilings (kv/tensor/element, key length). | `expected element count outside the admitted range`<br>`expected kv count outside the admitted range`<br>`expected tensor count outside the admitted range`<br>`expected tensor type counts do not sum to the tensor count`<br>`expected tensor type counts outside the admitted range`<br>`metadata KV count mismatch`<br>`metadata key exceeds the 128-byte ceiling`<br>`tensor count mismatch` | Stay within the library hard ceilings for counts, key lengths, and element totals. |
| `GgufError.WireMala` | malformed bytes: truncation, unknown/duplicate | `array element count above ceiling`<br>`duplicate metadata key`<br>`duplicate tensor name`<br>`empty tensor name`<br>`gguf field above the integer carrier`<br>`invalid UTF-8 in gguf string`<br>`malformed bool value`<br>`string exceeds the 4096-byte ceiling`<br>`tensor name exceeds the 128-byte ceiling`<br>`truncated gguf field`<br>`truncated gguf header`<br>`truncated string field`<br>`unexpected metadata value type`<br>`unknown array element type`<br>`unknown gguf metadata value type`<br>`unknown metadata key`<br>`unreachable` (internal) | Re-emit with the current schema stamp; never guess an unknown version. |
| `GgufError.CapsulaMala` | capsule construction failed. | `capsule construction failed: …`<br>`unreachable` (internal) | Read the suffix causa for the underlying admission failure; fix that field and re-admit. |

## `gradus:model/safetensors` — `SafetensorError`

Source: `src/model/safetensors.fab`. Render with module `causa(e)`.

| Code | Class / when | Live messages (representative) | Resolution |
| --- | --- | --- | --- |
| `SafetensorError.FormaMala` | Malformed shape / header / dimension on a wire or file. | `\\`<br>`\n`<br>`\r`<br>`\t`<br>`array must contain only integers`<br>`dtype must be a string`<br>`duplicate data_offsets in tensor descriptor`<br>`duplicate dtype in tensor descriptor`<br>`duplicate shape in tensor descriptor`<br>`empty header`<br>`expected an integer array`<br>`header is not a JSON object`<br>`header is not valid UTF-8`<br>`integer above the numeric carrier`<br>`invalid safetensors header size`<br>`malformed \\u escape`<br>`malformed array separator`<br>`malformed header member`<br>`malformed header separator`<br>`malformed integer`<br>_… +29 more live messages in `src/model/safetensors.fab`_ | Stay within the library hard ceilings for counts, key lengths, and element totals. |
| `SafetensorError.VersioIgnota` | Unknown or unsupported schema / file / marker version. | `unsupported safetensors row version: …` | Re-emit with the current schema stamp; never guess an unknown version. |
| `SafetensorError.ArchitecturaMala` | Architecture facts mismatch or missing. | `architecture mismatch`<br>`tensor count mismatch`<br>`tensor not in admitted row: …` | Match the admitted architecture facts (arch, layers, context, vocab, embedding). |
| `SafetensorError.TypoIgnotum` | Unknown dtype name/tag or un-admitted type id. | `unsupported dtype: …` | Use an admitted type/quantization row from the closed set; ensure block layouts tile. |
| `SafetensorError.OffscetaMala` | Safetensors data_offsets failure. | `data region does not tile exactly`<br>`data region truncated — tensor extends beyond file: …`<br>`data_offsets must have exactly 2 values: …`<br>`duplicate tensor name: …`<br>`malformed data offsets for `<br>`misaligned tensor data offset: …`<br>`overlapping tensor data regions` | Provide a payload whose lengths/offsets match the layout (exact tile, no gaps/overlaps). |
| `SafetensorError.FiguraMala` | Safetensors shape failure. | `empty shape`<br>`non-positive dimension`<br>`shape mismatch for `<br>`shape/offset inconsistency for ` | Fix caller shapes, ranks, dtypes, and element counts so they satisfy the operation contract. |
| `SafetensorError.TokenizerMala` | Tokenizer identity admission failure. | `tokenizer identity mismatch` | Use the pinned tokenizer identity (gpt2/BBPE, pre=`smollm`, EOG `{0,2}`, BOS-free, space-prefix-free). |
| `SafetensorError.LimitesMala` | Ceiling / bound violation. | `array above length ceiling`<br>`dimension above ceiling`<br>`element count above ceiling`<br>`header size above ceiling`<br>`header token count above ceiling`<br>`metadata KV count above ceiling`<br>`tensor count above ceiling`<br>`tensor name above length ceiling`<br>`total element count above ceiling` | Stay within the library hard ceilings for counts, key lengths, and element totals. |
| `SafetensorError.DigestioMala` | Malformed or mismatched digest. | `malformed digest value`<br>`malformed vocabulary digest` | Supply a well-formed digest (64-hex vocab digest / admitted algorithm) that matches the artifact. |
| `SafetensorError.MerciumMala` | Safetensors __metadata__ failure. | `duplicate __metadata__`<br>`malformed metadata member`<br>`malformed metadata separator`<br>`metadata must be a JSON object`<br>`metadata value must be a string`<br>`missing colon in metadata`<br>`missing required metadata key: …`<br>`trailing comma in metadata`<br>`unterminated metadata object` | Supply required metadata keys as strings; remove duplicates and trailing commas. |
| `SafetensorError.IngressioMala` | Capsule admission rejected from safetensors path. | `capsule admission rejected: …` | Read the suffix causa for the underlying admission failure; fix that field and re-admit. |

## `gradus:nn` — `NnError`

Source: `src/nn.fab`. Render with module `causa(e)`.

| Code | Class / when | Live messages (representative) | Resolution |
| --- | --- | --- | --- |
| `NnError.DimensioNegativa` | Negative dimension in a shape or index. | `negative dimension` | Fix caller shapes, ranks, dtypes, and element counts so they satisfy the operation contract. |
| `NnError.DimensioSupraLimitem` | A single dimension exceeds the module ceiling. | `dimension above ceiling` | Stay within the library hard ceilings for counts, key lengths, and element totals. |
| `NnError.ProductumSupraLimitem` | Element count (product of dims) exceeds the module ceiling. | `element count above ceiling` | Stay within the library hard ceilings for counts, key lengths, and element totals. |
| `NnError.GradusMismatch` | Rank / axis mismatch for the operation. | `layernorm requires rank >= 1`<br>`linear requires rank-2 input`<br>`linear requires rank-2 weight`<br>`matmul requires rank-2 operands` | Fix caller shapes, ranks, dtypes, and element counts so they satisfy the operation contract. |
| `NnError.FormaMismatch` | Shape mismatch between operands or against a required layout. | `bias does not match output shape`<br>`bias does not match output width`<br>`bias must be per-channel or output-shaped`<br>`layernorm offset must be per-channel`<br>`layernorm offset width mismatch`<br>`layernorm scale must be per-channel`<br>`layernorm scale width mismatch`<br>`shapes not broadcastable` | Fix caller shapes, ranks, dtypes, and element counts so they satisfy the operation contract. |
| `NnError.Incompatibilis` | Operands are not compatible under the operation rules. | `inner dimensions mismatch` | Fix caller shapes, ranks, dtypes, and element counts so they satisfy the operation contract. |
| `NnError.TypoMismatch` | Dtype mismatch or unsupported dtype for this surface. | `dtype mismatch`<br>`unsupported dtype for nn primitive` | Fix caller shapes, ranks, dtypes, and element counts so they satisfy the operation contract. |
| `NnError.ElementaMismatch` | Element-count / emptiness failure. | `empty normalization axis` | Fix caller shapes, ranks, dtypes, and element counts so they satisfy the operation contract. |
| `NnError.EpsilonInvalida` | Invalid (negative) epsilon. | `negative epsilon` | Correct the field to the documented admitted range and re-construct. |

## `gradus:optimize` — `OptimizeError`

Source: `src/optimize.fab`. Render with module `causa(e)`.

| Code | Class / when | Live messages (representative) | Resolution |
| --- | --- | --- | --- |
| `OptimizeError.NomenInane` | Empty or reserved name / owner / identity field. | `empty state name`<br>`empty state owner`<br>`reserved wire character in name or owner` | Supply a non-empty name/owner with no reserved wire characters. |
| `OptimizeError.VersioInvalida` | Invalid or malformed version field. | `invalid state version` | Re-emit with the current schema stamp; never guess an unknown version. |
| `OptimizeError.GeneratioInvalida` | Invalid generation counter on optimizer state. | `invalid generation` | Correct the field to the documented admitted range and re-construct. |
| `OptimizeError.PassusInvalida` | Invalid optimizer step count. | `invalid step count` | Correct the field to the documented admitted range and re-construct. |
| `OptimizeError.LentusInvalida` | Invalid learning rate. | `invalid learning rate` | Correct the field to the documented admitted range and re-construct. |
| `OptimizeError.IdentitasMismatch` | Parameter / gradient / state identity fields disagree. | `gradient identity does not match the parameter`<br>`state identity does not match the parameter` | Match parameter/gradient/state identity fields; recompute gradients after any parameter mutation. |
| `OptimizeError.GradusObsoletus` | Stale gradient (parameter mutated since compute). | `stale gradient: parameter mutated since the gradient was computed` | Match parameter/gradient/state identity fields; recompute gradients after any parameter mutation. |
| `OptimizeError.Gelida` | Frozen-parameter / frozen-slot rule violation. | `frozen parameter cannot be optimized` | Do not mutate a frozen parameter; construct a trainable parameter instead. |
| `OptimizeError.FormaMismatch` | Shape mismatch between operands or against a required layout. | `gradient shape does not match the parameter` | Fix caller shapes, ranks, dtypes, and element counts so they satisfy the operation contract. |
| `OptimizeError.Mutatio` | Disallowed mutation path. | _(reserved / mapped — no direct literal `iace` site; code is live on the `discretio`)_ | Use the documented mutation path only. |
| `OptimizeError.NomenDuplicatum` | Duplicate registration of an identity. | `optimizer state already registered for that parameter` | Register each identity at most once. |
| `OptimizeError.NomenIgnotum` | Unknown name (dtype, mode, identity lookup miss). | `no optimizer state for that parameter` | Look up an identity that was previously registered. |
| `OptimizeError.VersioIgnota` | Unknown or unsupported schema / file / marker version. | `unknown optimizer schema version` | Re-emit with the current schema stamp; never guess an unknown version. |
| `OptimizeError.WireMala` | Malformed wire / bytes / marker / field encoding. | `malformed generation in optimizer wire`<br>`malformed learning rate in optimizer wire`<br>`malformed optimizer wire`<br>`malformed optimizer wire header`<br>`malformed sgd-state wire`<br>`malformed slot count in optimizer wire`<br>`malformed state version in optimizer wire`<br>`malformed step count in optimizer wire`<br>`slot count mismatch in optimizer wire`<br>`unknown optimizer marker`<br>`unknown optimizer-state marker` | Re-emit with the current schema stamp; never guess an unknown version. |

## `gradus:parameter` — `ParametrumError`

Source: `src/parameter.fab`. Render with module `causa(e)`.

| Code | Class / when | Live messages (representative) | Resolution |
| --- | --- | --- | --- |
| `ParametrumError.NomenInane` | Empty or reserved name / owner / identity field. | `empty parameter name`<br>`empty parameter owner` | Supply a non-empty name/owner with no reserved wire characters. |
| `ParametrumError.NomenReservatum` | Reserved wire character or invalid identity shape. | `reserved wire character in name or owner` | Supply a non-empty name/owner with no reserved wire characters. |
| `ParametrumError.TypoIgnotum` | Unknown dtype name/tag or un-admitted type id. | _(reserved / mapped — no direct literal `iace` site; code is live on the `discretio`)_ | Correct the failing field per the message and re-invoke the fail-closed constructor. |
| `ParametrumError.FormaInvalida` | Invalid shape at construction. | `invalid shape` | Fix caller shapes, ranks, dtypes, and element counts so they satisfy the operation contract. |
| `ParametrumError.ElementaMismatch` | Element-count / emptiness failure. | `unreachable` (internal) | Fix caller shapes, ranks, dtypes, and element counts so they satisfy the operation contract. |
| `ParametrumError.GelidaMutatio` | Mutation of a frozen parameter. | `frozen parameter cannot be mutated` | Do not mutate a frozen parameter; construct a trainable parameter instead. |
| `ParametrumError.NomenDuplicatum` | Duplicate registration of an identity. | `parameter identity already registered` | Register each identity at most once. |
| `ParametrumError.NomenIgnotum` | Unknown name (dtype, mode, identity lookup miss). | `no parameter with that identity` | Look up an identity that was previously registered. |
| `ParametrumError.VersioInvalida` | Invalid or malformed version field. | `invalid version in parameter identity`<br>`malformed version in parameter identity` | Re-emit with the current schema stamp; never guess an unknown version. |
| `ParametrumError.WireMala` | Malformed wire / bytes / marker / field encoding. | `empty name in parameter identity`<br>`empty owner in parameter identity`<br>`malformed dimension in parameter identity`<br>`malformed parameter identity`<br>`unknown identity marker`<br>`unknown parameter marker`<br>`unknown parameter schema version` | Re-emit with the current schema stamp; never guess an unknown version. |

## `gradus:sampling` — `SamplingError`

Source: `src/sampling.fab`. Render with module `causa(e)`.

| Code | Class / when | Live messages (representative) | Resolution |
| --- | --- | --- | --- |
| `SamplingError.LogitsInvalida` | Logits vector invalid (empty or non-finite). | `logits must be finite`<br>`logits must be non-empty` | Provide a non-empty finite logits vector. |
| `SamplingError.ConfiguraInvalida` | Generation / sampling / config field out of admitted range. | `min-p must be within [0, 1]`<br>`repetition penalty must be at least 1`<br>`temperature must be non-negative`<br>`top-k must be non-negative`<br>`top-p must be within [0, 1]` | Correct the field to the documented admitted range and re-construct. |
| `SamplingError.HistoriaInvalida` | History token invalid for sampling. | `history token out of vocabulary range` | Keep history tokens inside the vocabulary range. |

## `gradus:serialize` — `SerializeError`

Source: `src/serialize.fab`. Render with module `causa(e)`.

| Code | Class / when | Live messages (representative) | Resolution |
| --- | --- | --- | --- |
| `SerializeError.VersioIgnota` | unknown magic / schema byte (version rejection). | `unknown serialize magic`<br>`unknown serialize schema version` | Re-emit with the current schema stamp; never guess an unknown version. |
| `SerializeError.GenusIgnotum` | unknown kind byte. | `unknown serialize kind` | Align the wire kind and element payload with the declared count and format. |
| `SerializeError.TypoIgnotum` | unknown dtype name (serialize) or tag (deserialize). | `unknown dtype name: …`<br>`unknown dtype tag` | Use an admitted type/quantization row from the closed set; ensure block layouts tile. |
| `SerializeError.FormaMala` | rank/dimension/element-count ceiling violations. | `element count above ceiling`<br>`negative dimension`<br>`rank above ceiling` | Stay within the library hard ceilings for counts, key lengths, and element totals. |
| `SerializeError.WireMala` | malformed bytes: truncation, bad length, invalid version | `empty parameter name`<br>`empty parameter owner`<br>`invalid UTF-8 textus field`<br>`invalid parameter version`<br>`invalid version in serialized parameter`<br>`malformed dtype payload`<br>`malformed parameter payload`<br>`malformed shape payload`<br>`malformed tensor payload`<br>`reserved wire character in name or owner`<br>`serialized name too large`<br>`truncated header`<br>`truncated parameter data length`<br>`truncated parameter fields`<br>`truncated parameter name`<br>`truncated parameter owner`<br>`truncated parameter payload`<br>`truncated shape payload`<br>`truncated tensor data length`<br>`truncated tensor payload`<br>`truncated textus field`<br>`unknown parameter status`<br>`unreachable` (internal) | Re-emit with the current schema stamp; never guess an unknown version. |
| `SerializeError.DataMala` | element-data failures: count mismatch, malformed tokens. | `element count mismatch`<br>`element count mismatch in serialized data`<br>`malformed float token`<br>`missing element data`<br>`serialized data too large` | Align the wire kind and element payload with the declared count and format. |

## `gradus:shape` — `FormaError`

Source: `src/shape.fab`. Render with module `causa(e)`.

| Code | Class / when | Live messages (representative) | Resolution |
| --- | --- | --- | --- |
| `FormaError.DimensioNegativa` | Negative dimension in a shape or index. | `negative dimension` | Fix caller shapes, ranks, dtypes, and element counts so they satisfy the operation contract. |
| `FormaError.DimensioSupraLimitem` | A single dimension exceeds the module ceiling. | _(reserved / mapped — no direct literal `iace` site; code is live on the `discretio`)_ | Fix caller shapes, ranks, dtypes, and element counts so they satisfy the operation contract. |
| `FormaError.ProductumSupraLimitem` | Element count (product of dims) exceeds the module ceiling. | `element count above ceiling` | Stay within the library hard ceilings for counts, key lengths, and element totals. |
| `FormaError.Incompatibilis` | Operands are not compatible under the operation rules. | `shapes not broadcastable` | Fix caller shapes, ranks, dtypes, and element counts so they satisfy the operation contract. |
| `FormaError.ElementaMismatch` | Element-count / emptiness failure. | `at most one inferred dimension`<br>`element count mismatch`<br>`inferred dimension not integral`<br>`inferred dimension not resolvable` | Fix caller shapes, ranks, dtypes, and element counts so they satisfy the operation contract. |
| `FormaError.GradusMismatch` | Rank / axis mismatch for the operation. | `target rank above ceiling`<br>`target rank below current rank` | Stay within the library hard ceilings for counts, key lengths, and element totals. |

## `gradus:tensor` — `TensorError`

Source: `src/tensor.fab`. Render with module `causa(e)`.

| Code | Class / when | Live messages (representative) | Resolution |
| --- | --- | --- | --- |
| `TensorError.FormaInvalida` | Invalid shape at construction. | `negative dimension` | Fix caller shapes, ranks, dtypes, and element counts so they satisfy the operation contract. |
| `TensorError.ElementaMismatch` | Element-count / emptiness failure. | `element count mismatch` | Fix caller shapes, ranks, dtypes, and element counts so they satisfy the operation contract. |
| `TensorError.TerminusExcedit` | Index or access exceeds the tensor bounds. | `empty tensor`<br>`index out of bounds`<br>`index rank mismatch`<br>`negative index` | Reduce the request or fix indices so they stay within the configured ceiling. |

## `gradus:tokenizer` — `TokenizerError`

Source: `src/tokenizer.fab`. Render with module `causa(e)`.

| Code | Class / when | Live messages (representative) | Resolution |
| --- | --- | --- | --- |
| `TokenizerError.VersioIgnota` | unknown tokenizer identity schema version. | `unknown tokenizer identity schema version: …` | Re-emit with the current schema stamp; never guess an unknown version. |
| `TokenizerError.ProgeniesIgnota` | un-admitted tokenizer kind (must be gpt2 / BBPE). | `un-admitted tokenizer kind: …` | Use the pinned tokenizer identity (gpt2/BBPE, pre=`smollm`, EOG `{0,2}`, BOS-free, space-prefix-free). |
| `TokenizerError.PreIgnotus` | un-admitted pre-tokenizer (must be smollm). | `un-admitted pre-tokenizer: …` | Use the pinned tokenizer identity (gpt2/BBPE, pre=`smollm`, EOG `{0,2}`, BOS-free, space-prefix-free). |
| `TokenizerError.VocabulumMala` | vocab / merges / specials count mismatch. | _(reserved / mapped — no direct literal `iace` site; code is live on the `discretio`)_ | Match the pinned vocabulary / merges / specials counts for the admitted row. |
| `TokenizerError.DigestioMala` | malformed vocabulary digest (not 64-hex). | `malformed vocabulary digest` | Supply a well-formed digest (64-hex vocab digest / admitted algorithm) that matches the artifact. |
| `TokenizerError.EogMala` | malformed EOG set (must be {0, 2}). | `EOG set does not match the pinned row: …`<br>`malformed EOG set`<br>`pinned row is BOS-free`<br>`pinned row is BOS-free (add_bos_token = false)`<br>`pinned row is space-prefix-free`<br>`pinned row is space-prefix-free (add_space_prefix = false)` | Admit the exact pinned EOG set `{0,2}` (wire `"0,2"`, ascending). A well-formed-but-different set is a **different tokenizer**. For BOS/space messages: set `bos_vacua`/`spatium_vacua` to `verum` (pinned row is BOS-free and space-prefix-free). |
| `TokenizerError.IdExtra` | token id outside the admitted range [0, vocab). | `token id out of range: …` | Keep token ids in the admitted range for the row. |
| `TokenizerError.ProbeDivergens` | probe id list diverges from the pinned fixture | `tokenizer ids diverge from the pinned llama.cpp probe: …` | Re-admit against the pinned probe fixtures — divergence means a different tokenizer. |
| `TokenizerError.WireMala` | malformed tokenizer identity wire form. | `malformed pinned id list`<br>`malformed tokenizer identity wire form`<br>`non-digit token id in pinned fixture`<br>`tokenizer identity failed verification`<br>`unknown pinned probe: …`<br>`unknown tokenizer identity marker` | Re-emit with the current schema stamp; never guess an unknown version. |

## `gradus:train` — `TrainError`

Source: `src/train.fab`. Render with module `causa(e)`.

| Code | Class / when | Live messages (representative) | Resolution |
| --- | --- | --- | --- |
| `TrainError.SchedulaInvalida` | Learning-rate schedule construction failed. | `final learning rate above peak`<br>`invalid final learning rate`<br>`invalid peak learning rate`<br>`negative warmup steps`<br>`schedule horizon must be at least one step`<br>`warmup exceeds the schedule horizon` | Correct the field to the documented admitted range and re-construct. |
| `TrainError.ModusIgnotus` | Unknown train/eval mode name. | `unknown mode name` | Correct the field to the documented admitted range and re-construct. |
| `TrainError.ExcutioInvalida` | Invalid execution policy field (e.g. dropout rate). | `dropout rate must be in [0, 1]` | Correct the field to the documented admitted range and re-construct. |
| `TrainError.PassusNegativus` | Negative schedule step. | `schedule step must be non-negative` | Correct the field to the documented admitted range and re-construct. |
| `TrainError.SemenInvalida` | Invalid RNG seed. | `seed must be non-zero` | Use a seed that meets the contract (non-zero / ≥ 1 as required). |
| `TrainError.ValorMala` | Malformed numeric value at a boundary. | _(reserved / mapped — no direct literal `iace` site; code is live on the `discretio`)_ | Reject NaN/malformed values at the boundary; re-export clean weights. |
| `TrainError.PositioInvalida` | Invalid position / epoch / step (negative or out of range). | `epoch must be non-negative`<br>`step must be non-negative` | Correct the field to the documented admitted range and re-construct. |
| `TrainError.StatumInane` | Empty checkpoint / state wire. | `checkpoint state wire is empty` | Provide a non-empty checkpoint wire produced by the current serialize path. |
| `TrainError.VersioIgnota` | Unknown or unsupported schema / file / marker version. | `unknown checkpoint schema version`<br>`unknown rng schema version` | Re-emit with the current schema stamp; never guess an unknown version. |
| `TrainError.WireMala` | Malformed wire / bytes / marker / field encoding. | `malformed checkpoint wire`<br>`malformed epoch in checkpoint wire`<br>`malformed rng state`<br>`malformed rng state in checkpoint wire`<br>`malformed rng wire`<br>`malformed step in checkpoint wire`<br>`unknown checkpoint marker`<br>`unknown rng marker` | Re-emit with the current schema stamp; never guess an unknown version. |

## `gradus:transformer` — `TransformerError`

Source: `src/transformer.fab`. Render with module `causa(e)`.

Sub-call errors from `NnError` / `AttentionError` / `MathError` are mapped into `TransformerError` by causa text (cross-module enum variants are not referenceable).

| Code | Class / when | Live messages (representative) | Resolution |
| --- | --- | --- | --- |
| `TransformerError.DimensioNegativa` | Negative dimension in a shape or index. | `negative dimension` | Fix caller shapes, ranks, dtypes, and element counts so they satisfy the operation contract. |
| `TransformerError.DimensioSupraLimitem` | A single dimension exceeds the module ceiling. | `dimension above ceiling` | Stay within the library hard ceilings for counts, key lengths, and element totals. |
| `TransformerError.ProductumSupraLimitem` | Element count (product of dims) exceeds the module ceiling. | `element count above ceiling` | Stay within the library hard ceilings for counts, key lengths, and element totals. |
| `TransformerError.GradusMismatch` | Rank / axis mismatch for the operation. | `attention requires rank-2 tensors`<br>`layernorm requires rank >= 1`<br>`linear requires rank-2 input`<br>`linear requires rank-2 weight`<br>`matmul requires rank-2 operands` | Fix caller shapes, ranks, dtypes, and element counts so they satisfy the operation contract. |
| `TransformerError.FormaMismatch` | Shape mismatch between operands or against a required layout. | _(reserved / mapped — no direct literal `iace` site; code is live on the `discretio`)_ | Fix caller shapes, ranks, dtypes, and element counts so they satisfy the operation contract. |
| `TransformerError.Incompatibilis` | Operands are not compatible under the operation rules. | `inner dimensions mismatch` | Fix caller shapes, ranks, dtypes, and element counts so they satisfy the operation contract. |
| `TransformerError.TypoMismatch` | Dtype mismatch or unsupported dtype for this surface. | `dtype mismatch`<br>`unsupported dtype for attention primitive`<br>`unsupported dtype for nn primitive` | Fix caller shapes, ranks, dtypes, and element counts so they satisfy the operation contract. |
| `TransformerError.ElementaMismatch` | Element-count / emptiness failure. | `empty attention input`<br>`empty normalization axis` | Fix caller shapes, ranks, dtypes, and element counts so they satisfy the operation contract. |
| `TransformerError.EpsilonInvalida` | Invalid (negative) epsilon. | `negative epsilon` | Correct the field to the documented admitted range and re-construct. |
| `TransformerError.PositioInvalida` | Invalid position / epoch / step (negative or out of range). | `negative position` | Correct the field to the documented admitted range and re-construct. |
| `TransformerError.DimensioInvalida` | Invalid dimension parameter (e.g. RoPE dim, embedding width). | `rope dim exceeds head width`<br>`rope dim must be at least 2`<br>`rope dim must be even` | Correct the field to the documented admitted range and re-construct. |
| `TransformerError.ModusInvalida` | Unknown attention / block mode. | `unknown attention mode` | Correct the field to the documented admitted range and re-construct. |

## Validation

Every code in this document must resolve to a live `discretio` variant under `src/`:

```bash
# Resolve one code: TokenizerError.EogMala
rg -n 'EogMala' src/tokenizer.fab
# Count public error discrim
rg -n '^discretio \w+Error' src --glob '*.fab'
```

Discipline: for each `ErrorType.Variant` row, `Variant` appears inside `discretio ErrorType { … }` in the listed source file. Representative messages are substrings of live `causa = "…"` (or mapped `causa = c` texts) in that file.

## Related

- API reference: [`docs/api-reference.md`](api-reference.md) (PML6-U1)
- Module map: [`docs/module-map.md`](module-map.md)
- Support matrix: [`docs/factory/production-ml-library/pml0-support-matrix.md`](factory/production-ml-library/pml0-support-matrix.md)
- Compatibility policy: [`docs/compatibility-policy.md`](compatibility-policy.md) (PML6-U3, when present)
- Exempla: `exempla/*/README.md`
