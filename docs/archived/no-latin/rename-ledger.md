# Rename ledger — no-latin (U1 lock)

**Status**: locked — authority for U2–U8 identifier, comment, and owned-string
renames.
**Unit**: `no-latin-U1` (`docs/factory/no-latin/delivery.md`).
**Tree**: gradus `main` @ `3e9731e` (census re-run against live `src/**/*.fab`).
**Census authority**: `delivery.md` corrected receipts **23 / 34 / 201-of-303**.
`goal-check.md` carries a known alias-count drift (`manifestum` ×8 vs live ×7)
and is **not** the authority for row counts.
**Method**: `/tmp/gradus-latin-census3.py` lexicon + extraction (fields are
`Type name`; union cases counted; import aliases do not require quotes).
**Naming inputs**: `docs/archived/english-locale/rename-seed.md` and
`s2-collision-ledger.md`. Collision-ledger locks win where they supersede
the seed (`quantitas` → `numel`, never `size`).

This file is the exhaustive old→new map. Later waves apply these rows; they
do not invent new English targets. Clean break, pre-1.0, no shims.

---

## Cross-foot (delivery.md receipts)

| Class | delivery.md | This ledger |
| --- | ---: | ---: |
| Public Latin fns (rename after retained) | 23 | **23** |
| Latin class fields (unique file+field) | 34 | **34** (35 typed occurrences: `valores` on two safetensors cursors) |
| Union-case occurrences (rename after retained) | 201 of 303 | **201 of 303** |
| Distinct Latin variant names | 95 of 163 | **95 of 163** |
| Public Latin types | 1 (`GeneratioError`) | **1** |
| Latin import aliases in `src/` | `manifestum` ×7, `capsula` ×2, `tokenizator`, `parametrum` | **11** (7+2+1+1) |

Retained-only hits excluded from the rename counts (they stay): 7 public fns
(`signum`, `silu`, `eog*`), 3 fields (`gradus_temporis`, two `eog` fields),
11 union cases (`GradusMismatch` ×9, `StopPolicy.Eog`, `UnicodeCategory.Signum`),
and type `GradusError`.

---

## 1. Reserved-name escapes

Inherited from `rename-seed.md`. S2 collision-ledger overrides are marked.

| Latin | Illegal English | Locked escape | Why |
| --- | --- | --- | --- |
| `valor` (method / carrier field) | `value` | `payload`; `get` only if the receiver has no `get` | en type `valor = "value"` |
| `typus` / `typo` (method) | `type` | `dtype` on DType-bearing carriers; `kind` elsewhere | en keyword `typus = "type"` |
| `quantitas` | `size` | **`numel`** (S2 lock; seed's `size` probe lost) | en keyword `magnitudo = "size"` |
| `gradus` (method) | — | `rank` | library proper noun; tensor meaning is rank |
| `forma` / `figura` (Tensor member) | — | `shape` | seed + Tensor shape probe; compiler `forma` stays reshape |
| `nomen` (member) | — | `name` | legal in member position; keyword `nomen = "name"` |
| `causa` | — | `message` | legal |
| any new fn | `class`, `enum`, `union`, `fn`, `let`, `return`, `match`, `self`, `optional`, `public`, `private`, `import`, `from`, `as`, `main`, `print`, `test` | pick a non-keyword | en `[keywords]` |
| any new type | `string`, `int`, `bool`, `float`, `list`, `map`, `set`, `bytes`, `value`, `void`, `null` | qualify (`TensorError`, …) | en `[types]` |
| any new member | frame statuses `request`, `item`, `byte`, `bulk`, `done`, `error`, `cancel` | pick another name | compiler-owned |

`catch err` bindings stay `err`. They are not member rows.

---

## 2. Retained-exception list

Do **not** rename these. The U8 no-Latin guard must accept them.

### 2.1 Proper noun

| Token | Where |
| --- | --- |
| `gradus` | package name, `gradus:*` import coordinates, `gradus:gradus` facade module, type `GradusError`, comments that name the library |

`gradus` as a **method** is not retained — it is already `rank()` (S2). Field
`gradus_temporis` is retained because the only Latin stem is `gradus`
(SSM time-step rank; GGUF key `qwen35moe.ssm.time_step_rank`).

### 2.2 Established technical terms

| Token | Meaning |
| --- | --- |
| `eog` | end-of-generation token set / stop policy |
| `silu` | SiLU activation |
| `signum` | mathematical sign function **and** Unicode mark category (`\p{M}`) |
| `fim` / `fins` | fill-in-the-middle |
| `bpe` | byte-pair encoding |
| `matmul` | matrix multiply |

Dtype / model / format tokens stay as-is: `llama`, `qwen2`, `qwen35moe`,
`gguf`, `ggml`, `smollm`, `smollm2`, `gpt2`, `f32`, `f16`, `bf16`, `i32`,
`u8`, and the `GGML_*` / `GGUF_*` numeric ids.

Retained public fns (not in the 23): `signum`, `silu`, `eog`, `eog_stop`,
`stops_on_eog`, `artifact_eog`, `is_artifact_eog`.

Retained variants (not in the 201): `GradusMismatch` (every module that
has it), `StopPolicy.Eog`, `UnicodeCategory.Signum`, `GradientError.GradusIgnotum`.

### 2.3 External-format keys

GGUF / safetensors / HuggingFace spec strings we do not own. Examples
(not exhaustive of the spec — exhaustive of live Gradus uses):

- `general.architecture`, `general.file_type`, `general.quantization_version`,
  `general.alignment`
- `qwen35moe.*` and `qwen2.*` metadata keys (`block_count`, `context_length`,
  `embedding_length`, `attention.*`, `rope.*`, `expert_*`, `ssm.*`, …)
- `tokenizer.ggml.tokens`, `tokenizer.ggml.merges`, `tokenizer.ggml.token_type`,
  `tokenizer.ggml.model`, `tokenizer.ggml.pre`
- safetensors header members `dtype`, `shape`, `data_offsets`, `__metadata__`
- pinned row keys `format.name`, `format.version`, `model.arch`,
  `model.density`, `model.layers`, `model.context`, `tokenizer.model`,
  `tokenizer.pre`, `tokenizer.vocab_digest`, `tokenizer.eog`,
  `tokenizer.bos_free`, `tokenizer.space_prefix_free`
- tensor names such as `token_embd.weight`, `output.weight`,
  `blk.N.attn_q.weight`, `model.embed_tokens.weight`

Wire **values** that are format tokens (`"gpt2"`, `"smollm"`, `"llama"`,
`"F32"`, `"sha-256"`, `"safetensors"`) stay. Latin **owned** wire values
are §8 (OQ3).

---

## 3. Public functions (23)

| # | Module | Old | New | Notes |
| ---: | --- | --- | --- | --- |
| 1 | `model/gguf_manifest` | `textum` | `text` | seed |
| 2 | `model/gguf_manifest` | `textorum` | `texts` | seed |
| 3 | `model/gguf_manifest` | `numerum` | `number` | seed |
| 4 | `model/gguf_manifest` | `numerorum` | `numbers` | seed |
| 5 | `model/gguf_manifest` | `numerorum_u32` | `numbers_u32` | |
| 6 | `model/gguf_manifest` | `boleanum` | `boolean` | seed |
| 7 | `model/gguf_manifest` | `longitudo_listae` | `list_length` | |
| 8 | `model/gguf_manifest` | `inveni_tensorem` | `find_tensor` | seed `inveni` → `find` |
| 9 | `model/gguf_manifest` | `limes_payloadis` | `payload_limit` | |
| 10 | `model/gguf_manifest` | `read_fragmentum` | `read_fragment` | already `read_*`; `fragmentum` → `fragment` |
| 11 | `model/qwen35moe` | `congela` | `freeze` | seed |
| 12 | `model/qwen35moe` | `referantia` | `reference` | |
| 13 | `model/qwen35moe` | `tensores_canonici` | `canonical_tensors` | |
| 14 | `model/qwen35moe` | `causa_admissionis` | `admission_message` | `causa` → `message` |
| 15 | `model/qwen35moe` | `causa_referantiae` | `reference_message` | |
| 16 | `model/qwen35moe` | `causa_tensorum` | `tensor_message` | |
| 17 | `model/safetensors` | `admittas` | `admit` | **collision**: `gguf.admit` is already English; different module, same verb, legal |
| 18 | `model/artifact` | `identitas` | `identity` | seed |
| 19 | `decode` | `decodere_datum` | `decode_data` | |
| 20 | `decode` | `projectio_bias` | `projection_bias` | |
| 21 | `gradient` | `gradientes_simple_loss` | `gradients_simple_loss` | |
| 22 | `gradient` | `gradientes_masked_mean` | `gradients_masked_mean` | |
| 23 | `tokenizer` | `est_eog` | `is_eog` | GOAL example; `eog` stem retained |

No two of the 23 share a (module, new-name) pair.

---

## 4. Class / union-payload fields (34)

Census 34 = unique `(file, field)`. Typed occurrences = 35 because
`safetensors.valores` sits on both `MetadataCursor` and `NumberCursor`.

| # | Type | Old | New | Notes |
| ---: | --- | --- | --- | --- |
| 1 | `Qwen35moeConfig` | `longitudo_clavis` | `key_length` | GGUF `attention.key_length` |
| 2 | `Qwen35moeConfig` | `longitudo_contextus` | `context_length` | GGUF `context_length` |
| 3 | `Qwen35moeConfig` | `longitudo_ffn_communi` | `shared_ffn_length` | GGUF `expert_shared_feed_forward_length` |
| 4 | `Qwen35moeConfig` | `longitudo_ffn_experti` | `expert_ffn_length` | GGUF `expert_feed_forward_length` |
| 5 | `Qwen35moeConfig` | `longitudo_valoris` | `value_length` | **not** `valor`→`payload`. QKV V dim; GGUF `attention.value_length` |
| 6 | `Qwen35moeConfig` | `longitudo_vestimenti` | `embedding_length` | GGUF `embedding_length` |
| 7 | `Qwen35moeConfig` | `numerus_capita` | `head_count` | |
| 8 | `Qwen35moeConfig` | `numerus_capita_kv` | `head_count_kv` | |
| 9 | `Qwen35moeConfig` | `numerus_coetuum` | `group_count` | GGUF `ssm.group_count` |
| 10 | `Qwen35moeConfig` | `numerus_concatenationum` | `merge_count` | `tokenizer.ggml.merges` length |
| 11 | `Qwen35moeConfig` | `numerus_dimensionum_rotae` | `rope_dimension_count` | GGUF `rope.dimension_count` |
| 12 | `Qwen35moeConfig` | `numerus_expertorum` | `expert_count` | |
| 13 | `Qwen35moeConfig` | `numerus_expertorum_activorum` | `expert_used_count` | |
| 14 | `Qwen35moeConfig` | `numerus_strata_nextn` | `nextn_predict_layers` | |
| 15 | `Qwen35moeConfig` | `numerus_tokenum` | `token_count` | |
| 16 | `Qwen35moeConfig` | `numerus_tractuum` | `block_count` | |
| 17 | `Qwen35moeConfig` | `numerus_typorum_tokenum` | `token_type_count` | `tokenizer.ggml.token_type` length |
| 18 | `Qwen35moeConfig` | `typus_limaturae` | `file_type` | GGUF `general.file_type`; not a DType (`kind`/`dtype`) |
| 19 | `Qwen35moeConfig` | `versio_quantificationis` | `quantization_version` | |
| 20 | `Qwen35moeAdmission` | `summa` | `summary` | |
| 21 | `GgmlLayout.Cognita` | `elementa_per_blockum` | `elements_per_block` | |
| 22 | `GgmlLayout.Cognita` | `octeti_per_blockum` | `bytes_per_block` | |
| 23 | `GgmlLayout.Cognita` | `longitudo_octetorum` | `byte_length` | |
| 24 | `GgufCorpus` | `tabula` | `table` | **collision**: S2 type `Tabula`→`Checkpoint` is a different word; en type `tabula`=`map` is not this field |
| 25 | `GgufMetadata` | `valor_wire` | `payload_wire` | reserved `valor`→`payload` |
| 26 | `HeaderCursor` | `caput` | `header` | |
| 27 | `HeaderCursor` | `textus` | `text` | |
| 28 | `Structure` | `meta_valores` | `meta_values` | plural; not reserved type `value` |
| 29 | `MetadataCursor` / `NumberCursor` | `valores` | `values` | one census field, two types; JSON value lists, not carriers |
| 30 | `Tokenizer` | `specialia_textus` | `special_texts` | |
| 31 | `Tokenizer` | `vocabulum` | `vocab` | already-English field on `DenseQwen2Config` |
| 32 | `Capsule` | `manifestum` | `manifest` | |
| 33 | `TensorView` | `longitudo_payloadis` | `payload_length` | |
| 34 | `CanonicalDescriptor` | `nomen_canonicum` | `canonical_name` | |

### 4.1 Census residual fields (lexicon / regex miss — still rename)

The census field regex does not match dotted types (`artifact.ContentIdentity
identitas`) and the lexicon misses several live Latin stems. These are
**not** in the 34. Waves still apply the family map:

| Type | Old | New |
| --- | --- | --- |
| `GgufCorpus`, `GgufManifest` | `identitas` | `identity` |
| `GgufManifest` | `concordatio` | `alignment` |
| `GgufManifest` | `data_inceptum` | `data_start` |
| `GgufTensorDescriptor` | `offset_relativum` | `relative_offset` |
| `Qwen35moeConfig` | `architectura` | `architecture` |
| `Qwen35moeConfig` | `epsilon_normae_rms` | `rms_norm_epsilon` |
| `Qwen35moeConfig` | `basis_frequentiae` | `freq_base` |
| `Qwen35moeConfig` | `sectiones_rotae` | `rope_sections` |
| `Qwen35moeConfig` | `nucleus_convolutus` | `conv_kernel` |
| `Qwen35moeConfig` | `magnitudo_status` | `state_size` |
| `Qwen35moeConfig` | `magnitudo_interior` | `inner_size` |
| `Qwen35moeConfig` | `intervallum_attentionis_plenae` | `full_attention_interval` |
| `Qwen35moeConfig` | `exemplum_tokenizoris` | `tokenizer_model` |
| `Qwen35moeConfig` | `praeparatio_tokenizoris` | `tokenizer_pre` |

`magnitudo_*` does **not** become `size` (reserved). Use the GGUF English
fact names above.

---

## 5. Types

| Old | New | File |
| --- | --- | --- |
| `GeneratioError` | `GenerationError` | `src/generation.fab` |

`GradusError` is retained (proper noun). All other public types are already
English (S2).

---

## 6. Import aliases (11)

Rule: alias becomes the last path component of the import coordinate
(already English).

| File | Coordinate | Old | New |
| --- | --- | --- | --- |
| `src/model/capsule.fab` | `gradus:model/gguf_manifest` | `manifestum` | `gguf_manifest` |
| `src/model/dense_llama.fab` | `gradus:model/gguf_manifest` | `manifestum` | `gguf_manifest` |
| `src/model/dense_qwen2.fab` | `gradus:model/gguf_manifest` | `manifestum` | `gguf_manifest` |
| `src/model/gguf.fab` | `gradus:model/gguf_manifest` | `manifestum` | `gguf_manifest` |
| `src/model/qwen35moe.fab` | `gradus:model/gguf_manifest` | `manifestum` | `gguf_manifest` |
| `src/model/tensor_view.fab` | `gradus:model/gguf_manifest` | `manifestum` | `gguf_manifest` |
| `src/tokenizer.fab` | `gradus:model/gguf_manifest` | `manifestum` | `gguf_manifest` |
| `src/model/gguf.fab` | `gradus:model/capsule` | `capsula` | `capsule` |
| `src/model/safetensors.fab` | `gradus:model/capsule` | `capsula` | `capsule` |
| `src/generation.fab` | `gradus:tokenizer` | `tokenizator` | `tokenizer` |
| `src/optimize.fab` | `gradus:parameter` | `parametrum` | `parameter` |

×7 / ×2 / ×1 / ×1. Delivery.md is the authority; do not “correct” this
to the goal-check ×8 note.

---

## 7. Union cases — 95 distinct names, 201 occurrences

### 7.1 Suffix / stem rules

| Latin stem | English | Applies |
| --- | --- | --- |
| `Mala` | `Bad` | malformed / rejected payload |
| `Invalida` / `Invalida` / `Negativus` | `Invalid` / `Negative` | |
| `Ignota` / `Ignotum` / `Ignotus` | `Unknown` | |
| `Diversa` / `Diversum` / `Diversus` / `Divergens` | `Divergent` | qwen freeze mismatches |
| `SupraLimitem` | `AboveLimit` | |
| `ExtraLimitem` | `OutOfRange` | |
| `Duplicata` / `Duplicatum` | `Duplicate` | |
| `Inane` | `Empty` | |
| `Reservatum` | `Reserved` | |
| `Mutatio` | `Mutation` | |
| `Forma` (shape meaning) | `Shape` | **except** safetensors `FormaMala` |
| `Figura` | `Shape` | |
| `Typo` (dtype-bearing) | `Dtype` | |
| `Typus` (non-dtype) | `Type` | `TypusIgnotus` is an unknown GGML/file type |
| `Nomen` / `Nomine` | `Name` | |
| `Dimensio` | `Dimension` | |
| `Positio` | `Position` | |
| `Versio` | `Version` | |
| `Identitas` | `Identity` | |
| `Elementa` | `Element` | keep existing English `Mismatch` |
| `Longitudo` | `Length` | |
| `Passus` | `Step` | |
| `Lentus` | `Rate` | |
| `Semen` | `Seed` | |
| `Schedula` | `Schedule` | |
| `Statum` | `State` | |
| `Modus` | `Mode` | |
| `Historia` | `History` | |
| `Configura` / `Configuratio` | `Config` | |
| `Manifestum` | `Manifest` | |
| `Metadatum` | `Metadata` | |
| `Decodere` | `Decoder` | |
| `Capsula` | `Capsule` | |
| `Digestio` | `Digest` | |
| `Algorithmus` | `Algorithm` | |
| `Architectura` / `Archaegramma` | `Architecture` | |
| `Vocabulum` | `Vocab` | |
| `Littera` | `Letter` | |
| `Spatium` | `Space` | |
| `Numerus` (category) | `Number` | |
| `Numerus` (count) | `Count` | `NumerusDiversus` / `NumerusDivergens` |
| `NovumLinea` | `Newline` | |
| `Aliud` | `Other` | |
| `Cognita` | `Known` | |
| `Ignota` (layout) | `Unknown` | |
| `Consecutiva` | `Consecutive` | |
| `Gelida` | `Frozen` | |
| `Valor` | `Payload` | reserved escape |
| `Fons` | `Source` | |
| `Clavis` | `Key` | |
| `Ordo` | `Order` | |
| `Glomulus` | `Block` | |
| `Stipula` | `Storage` | dtype_ggml / storage class |
| `Ambitus` / `Range` | `Range` | |
| `Offsceta` / `Offset` | `Offset` | |
| `Mercium` | `Metadata` | safetensors `__metadata__` structure |
| `Ingressio` | `Admission` | capsule constructor reject |
| `Artificium` | `Artifact` | |
| `Vestigium` | `Trace` | |
| `Progenies` | `MergeKind` | S2 tokenizer collision (`merges` was SEM005) |
| `Stratum` | `Layer` | |
| `Canonico` | `Canonical` | |

### 7.2 Distinct-name map (95)

One Latin name → one default English name, except the **ambiguous** rows
in §7.3.

| Old | New |
| --- | --- |
| `AlgorithmusIgnotus` | `UnknownAlgorithm` |
| `Aliud` | `Other` |
| `AmbitusMala` | `BadRange` |
| `ArchaegrammaIgnota` | `UnknownArchitecture` |
| `ArchitecturaIgnota` | `UnknownArchitecture` |
| `ArchitecturaMala` | `BadArchitecture` |
| `ArtificiumMala` | `BadArtifact` |
| `CanonicoIgnota` | `UnknownCanonical` |
| `CapsulaMala` | `BadCapsule` |
| `ClavisDuplicata` | `DuplicateKey` |
| `Cognita` | `Known` |
| `ConfiguraInvalida` | `InvalidConfig` |
| `ConfiguraMala` | `BadConfig` |
| `ConfiguratioDiversa` | `DivergentConfig` |
| `Consecutiva` | `Consecutive` |
| `DataMala` | `BadData` |
| `DecodereInvalida` | `InvalidDecoder` |
| `DigestioMala` | `BadDigest` |
| `DimensioDiversa` | `DivergentDimension` |
| `DimensioInvalida` | `InvalidDimension` |
| `DimensioNegativa` | `NegativeDimension` |
| `DimensioSupraLimitem` | `DimensionAboveLimit` |
| `ElementaMismatch` | `ElementMismatch` |
| `EogMala` | `BadEog` |
| `FiguraMala` | `BadShape` |
| `FonsMala` | `BadSource` |
| `FormaDiversa` | `DivergentShape` |
| `FormaInvalida` | `InvalidShape` |
| `FormaMala` | `BadShape` (default) / `BadFormat` (safetensors only — §7.3) |
| `FormaMismatch` | `ShapeMismatch` |
| `FormatMala` | `BadFormat` |
| `Gelida` | `Frozen` |
| `GelidaMutatio` | `FrozenMutation` |
| `GeneratioInvalida` | `InvalidGeneration` |
| `GlomulusMala` | `BadBlock` |
| `GradusObsoletus` | `StaleGradient` |
| `GradusVersio` | `GradientVersion` |
| `HistoriaInvalida` | `InvalidHistory` |
| `IdentitasDiversa` | `DivergentIdentity` |
| `IdentitasMala` | `BadIdentity` |
| `IdentitasMismatch` | `IdentityMismatch` |
| `Ignota` | `Unknown` |
| `IngressioMala` | `BadAdmission` |
| `LayoutIgnota` | `UnknownLayout` |
| `LentusInvalida` | `InvalidRate` |
| `LimitesMala` | `BadBounds` |
| `Littera` | `Letter` |
| `LongitudoMala` | `BadLength` |
| `ManifestumMala` | `BadManifest` |
| `MergesMala` | `BadMerges` |
| `MerciumMala` | `BadMetadata` |
| `MetadatumDiversum` | `DivergentMetadata` |
| `ModusIgnotus` | `UnknownMode` |
| `ModusInvalida` | `InvalidMode` |
| `NomenCanonicumIgnotum` | `UnknownCanonicalName` |
| `NomenDiversum` | `DivergentName` |
| `NomenDuplicatum` | `DuplicateName` |
| `NomenIgnotum` | `UnknownName` |
| `NomenInane` | `EmptyName` |
| `NomenReservatum` | `ReservedName` |
| `NomineIgnota` | `UnknownName` |
| `NonFinita` | `NonFinite` |
| `NovumLinea` | `Newline` |
| `Numerus` | `Number` |
| `NumerusDivergens` | `DivergentCount` |
| `NumerusDiversus` | `DivergentCount` |
| `OffsetMala` | `BadOffset` |
| `OffscetaMala` | `BadOffset` |
| `OrdoMala` | `BadOrder` |
| `PassusInvalida` | `InvalidStep` |
| `PassusNegativus` | `NegativeStep` |
| `PositioInvalida` | `InvalidPosition` |
| `PreIgnotus` | `UnknownPreTokenizer` |
| `ProgeniesIgnota` | `UnknownMergeKind` |
| `QuantizatioIgnota` | `UnknownQuantization` |
| `RangeMala` | `BadRange` |
| `ReferentiaDiversa` | `DivergentReference` |
| `SchedulaInvalida` | `InvalidSchedule` |
| `SemenInvalida` | `InvalidSeed` |
| `Spatium` | `Space` |
| `StatumInane` | `EmptyState` |
| `StipulaDiversa` | `DivergentStorage` |
| `StratumExtraLimitem` | `LayerOutOfRange` |
| `TensorumDiversum` | `DivergentTensors` |
| `TokenizerMala` | `BadTokenizer` |
| `TypoIgnotum` | `UnknownDtype` |
| `TypoMismatch` | `DtypeMismatch` |
| `TypusIgnotus` | `UnknownType` |
| `Utf8Mala` | `BadUtf8` |
| `ValorMala` | `BadPayload` |
| `VersioIgnota` | `UnknownVersion` |
| `VersioInvalida` | `InvalidVersion` |
| `VestigiumIgnotum` | `UnknownTrace` |
| `VocabulumMala` | `BadVocab` |
| `WireMala` | `BadWire` |

### 7.3 Cross-module collision check

Same Latin name in different unions is legal after rename (Faber variants
are per-union). Recorded ambiguities:

| Latin | Why ambiguous | Lock |
| --- | --- | --- |
| `FormaMala` | safetensors = container/JSON **format**; serialize / gguf / dense = **shape** | safetensors → `BadFormat`; all others → `BadShape` |
| `FiguraMala` vs safetensors `FormaMala` | **same module** — both would become `BadShape` if `forma`/`figura` collapsed | `FiguraMala` → `BadShape`; safetensors `FormaMala` → `BadFormat` |
| `FormatMala` vs safetensors `FormaMala` | both become `BadFormat` | legal: different modules (`gguf` / `gguf_manifest` vs `safetensors`) |
| `NomenIgnotum` vs `NomineIgnota` | both “unknown name” | both → `UnknownName` (different unions) |
| `NumerusDiversus` vs `NumerusDivergens` | both count divergence in qwen35moe | both → `DivergentCount` (tensor-error vs reference-error unions) |
| `Numerus` (UnicodeCategory) vs count `Numerus*` | category vs count | category → `Number`; count errors → `DivergentCount` |
| `OffsetMala` vs `OffscetaMala` | same meaning, two spellings | both → `BadOffset` |
| `AmbitusMala` vs `RangeMala` | same meaning | both → `BadRange` |
| `ArchitecturaIgnota` vs `ArchaegrammaIgnota` | unknown architecture | both → `UnknownArchitecture` |
| `Gelida` (`Station` vs `OptimizeError`) | frozen status vs frozen-parameter step | both → `Frozen` |
| `admittas` vs `admit` | §3 row 17 | different modules |
| `tabula` field vs S2 type `Tabula` | table-of-bytes vs Checkpoint | field → `table` |
| `longitudo_valoris` vs `valor` | QKV V dim vs carrier payload | field → `value_length`; carrier `valor` → `payload` |
| `valores` → `values` | reserved type is `value` (singular) | plural field accepted; probe if SEM005 |
| `Progenies*` → `MergeKind` | S2: `merges` collided with local `merges` | keep `MergeKind` |

Shared English targets that are **not** ambiguous (same meaning, different
unions): `ShapeMismatch`, `DtypeMismatch`, `ElementMismatch`, `BadWire`,
`UnknownVersion`, `InvalidConfig`, `InvalidDimension`, `NegativeDimension`,
`DimensionAboveLimit`, `InvalidPosition`, `NonFinite`, `UnknownLayout`,
`BadBounds`, `BadLength`, `BadDigest`, `UnknownAlgorithm`. Keep one English
spelling everywhere.

### 7.4 Occurrence list (201)

Each row is one live case in one union. Apply §7.2 / §7.3.

| Module | Union | Old | New |
| --- | --- | --- | --- |
| `attention` | `AttentionError` | `ConfiguraInvalida` | `InvalidConfig` |
| `attention` | `AttentionError` | `DimensioInvalida` | `InvalidDimension` |
| `attention` | `AttentionError` | `DimensioNegativa` | `NegativeDimension` |
| `attention` | `AttentionError` | `DimensioSupraLimitem` | `DimensionAboveLimit` |
| `attention` | `AttentionError` | `ElementaMismatch` | `ElementMismatch` |
| `attention` | `AttentionError` | `FormaMismatch` | `ShapeMismatch` |
| `attention` | `AttentionError` | `PositioInvalida` | `InvalidPosition` |
| `attention` | `AttentionError` | `TypoMismatch` | `DtypeMismatch` |
| `attention` | `RopePolicy` | `Consecutiva` | `Consecutive` |
| `cache` | `CacheError` | `DimensioInvalida` | `InvalidDimension` |
| `cache` | `CacheError` | `ElementaMismatch` | `ElementMismatch` |
| `cache` | `CacheError` | `FormaMismatch` | `ShapeMismatch` |
| `cache` | `CacheError` | `NomenInane` | `EmptyName` |
| `cache` | `CacheError` | `TypoMismatch` | `DtypeMismatch` |
| `cache` | `CacheError` | `VersioIgnota` | `UnknownVersion` |
| `cache` | `CacheError` | `WireMala` | `BadWire` |
| `decode` | `DecodeError` | `DecodereInvalida` | `InvalidDecoder` |
| `decode` | `DecodeError` | `DimensioInvalida` | `InvalidDimension` |
| `decode` | `DecodeError` | `ElementaMismatch` | `ElementMismatch` |
| `decode` | `DecodeError` | `FormaMismatch` | `ShapeMismatch` |
| `decode` | `DecodeError` | `PositioInvalida` | `InvalidPosition` |
| `decode` | `DecodeError` | `TypoMismatch` | `DtypeMismatch` |
| `dtype` | `DTypeError` | `NomenIgnotum` | `UnknownName` |
| `dtype` | `DTypeError` | `NonFinita` | `NonFinite` |
| `dtype` | `DTypeError` | `VersioIgnota` | `UnknownVersion` |
| `generation` | `GeneratioError` | `ConfiguraInvalida` | `InvalidConfig` |
| `generation` | `GeneratioError` | `ElementaMismatch` | `ElementMismatch` |
| `generation` | `GeneratioError` | `TypoMismatch` | `DtypeMismatch` |
| `generation` | `GeneratioError` | `VersioIgnota` | `UnknownVersion` |
| `generation` | `GeneratioError` | `WireMala` | `BadWire` |
| `gradient` | `GradientError` | `GradusVersio` | `GradientVersion` |
| `gradus` | `GradusError` | `DimensioNegativa` | `NegativeDimension` |
| `gradus` | `GradusError` | `DimensioSupraLimitem` | `DimensionAboveLimit` |
| `gradus` | `GradusError` | `ElementaMismatch` | `ElementMismatch` |
| `gradus` | `GradusError` | `FormaMismatch` | `ShapeMismatch` |
| `gradus` | `GradusError` | `TypoMismatch` | `DtypeMismatch` |
| `loss` | `LossError` | `DimensioNegativa` | `NegativeDimension` |
| `loss` | `LossError` | `DimensioSupraLimitem` | `DimensionAboveLimit` |
| `loss` | `LossError` | `ElementaMismatch` | `ElementMismatch` |
| `loss` | `LossError` | `FormaMismatch` | `ShapeMismatch` |
| `loss` | `LossError` | `NonFinita` | `NonFinite` |
| `loss` | `LossError` | `TypoMismatch` | `DtypeMismatch` |
| `math` | `MathError` | `DimensioNegativa` | `NegativeDimension` |
| `math` | `MathError` | `DimensioSupraLimitem` | `DimensionAboveLimit` |
| `math` | `MathError` | `FormaMismatch` | `ShapeMismatch` |
| `math` | `MathError` | `NomenIgnotum` | `UnknownName` |
| `math` | `MathError` | `NonFinita` | `NonFinite` |
| `math` | `MathError` | `TypoMismatch` | `DtypeMismatch` |
| `metrics` | `MetricError` | `ElementaMismatch` | `ElementMismatch` |
| `metrics` | `MetricError` | `FormaMismatch` | `ShapeMismatch` |
| `metrics` | `MetricError` | `NonFinita` | `NonFinite` |
| `metrics` | `MetricError` | `TypoMismatch` | `DtypeMismatch` |
| `model/artifact` | `ArtifactError` | `AlgorithmusIgnotus` | `UnknownAlgorithm` |
| `model/artifact` | `ArtifactError` | `DigestioMala` | `BadDigest` |
| `model/artifact` | `ArtifactError` | `LongitudoMala` | `BadLength` |
| `model/capsule` | `AdmissionError` | `AlgorithmusIgnotus` | `UnknownAlgorithm` |
| `model/capsule` | `AdmissionError` | `DigestioMala` | `BadDigest` |
| `model/capsule` | `AdmissionError` | `ManifestumMala` | `BadManifest` |
| `model/capsule` | `AdmissionError` | `VersioIgnota` | `UnknownVersion` |
| `model/capsule` | `AdmissionError` | `WireMala` | `BadWire` |
| `model/dense` | `DenseError` | `ConfiguraMala` | `BadConfig` |
| `model/dense` | `DenseError` | `FormaMala` | `BadShape` |
| `model/dense_llama` | `LlamaError` | `LayoutIgnota` | `UnknownLayout` |
| `model/dense_llama` | `LlamaError` | `NomenCanonicumIgnotum` | `UnknownCanonicalName` |
| `model/dense_qwen2` | `DenseQwen2Error` | `ArchaegrammaIgnota` | `UnknownArchitecture` |
| `model/dense_qwen2` | `DenseQwen2Error` | `CanonicoIgnota` | `UnknownCanonical` |
| `model/dense_qwen2` | `DenseQwen2Error` | `ConfiguraMala` | `BadConfig` |
| `model/dense_qwen2` | `DenseQwen2Error` | `StratumExtraLimitem` | `LayerOutOfRange` |
| `model/dequant` | `DequantError` | `GlomulusMala` | `BadBlock` |
| `model/dequant` | `DequantError` | `OrdoMala` | `BadOrder` |
| `model/dequant` | `DequantError` | `TypoIgnotum` | `UnknownDtype` |
| `model/dequant` | `DequantError` | `ValorMala` | `BadPayload` |
| `model/gguf` | `GgufError` | `ArchitecturaMala` | `BadArchitecture` |
| `model/gguf` | `GgufError` | `CapsulaMala` | `BadCapsule` |
| `model/gguf` | `GgufError` | `FormaMala` | `BadShape` |
| `model/gguf` | `GgufError` | `FormatMala` | `BadFormat` |
| `model/gguf` | `GgufError` | `LimitesMala` | `BadBounds` |
| `model/gguf` | `GgufError` | `OffsetMala` | `BadOffset` |
| `model/gguf` | `GgufError` | `QuantizatioIgnota` | `UnknownQuantization` |
| `model/gguf` | `GgufError` | `TokenizerMala` | `BadTokenizer` |
| `model/gguf` | `GgufError` | `VersioIgnota` | `UnknownVersion` |
| `model/gguf` | `GgufError` | `WireMala` | `BadWire` |
| `model/gguf_manifest` | `GgmlLayout` | `Cognita` | `Known` |
| `model/gguf_manifest` | `GgmlLayout` | `Ignota` | `Unknown` |
| `model/gguf_manifest` | `GgufManifestError` | `ClavisDuplicata` | `DuplicateKey` |
| `model/gguf_manifest` | `GgufManifestError` | `FonsMala` | `BadSource` |
| `model/gguf_manifest` | `GgufManifestError` | `FormatMala` | `BadFormat` |
| `model/gguf_manifest` | `GgufManifestError` | `IdentitasMala` | `BadIdentity` |
| `model/gguf_manifest` | `GgufManifestError` | `LayoutIgnota` | `UnknownLayout` |
| `model/gguf_manifest` | `GgufManifestError` | `LimitesMala` | `BadBounds` |
| `model/gguf_manifest` | `GgufManifestError` | `OffsetMala` | `BadOffset` |
| `model/gguf_manifest` | `GgufManifestError` | `VersioIgnota` | `UnknownVersion` |
| `model/gguf_manifest` | `GgufManifestError` | `WireMala` | `BadWire` |
| `model/qwen35moe` | `Qwen35moeAdmissionError` | `ArchitecturaIgnota` | `UnknownArchitecture` |
| `model/qwen35moe` | `Qwen35moeAdmissionError` | `ConfiguratioDiversa` | `DivergentConfig` |
| `model/qwen35moe` | `Qwen35moeAdmissionError` | `IdentitasDiversa` | `DivergentIdentity` |
| `model/qwen35moe` | `Qwen35moeAdmissionError` | `ManifestumMala` | `BadManifest` |
| `model/qwen35moe` | `Qwen35moeAdmissionError` | `ReferentiaDiversa` | `DivergentReference` |
| `model/qwen35moe` | `Qwen35moeAdmissionError` | `TensorumDiversum` | `DivergentTensors` |
| `model/qwen35moe` | `Qwen35moeAdmissionError` | `TypusIgnotus` | `UnknownType` |
| `model/qwen35moe` | `Qwen35moeConfigError` | `MetadatumDiversum` | `DivergentMetadata` |
| `model/qwen35moe` | `Qwen35moeReferenceError` | `AmbitusMala` | `BadRange` |
| `model/qwen35moe` | `Qwen35moeReferenceError` | `DimensioDiversa` | `DivergentDimension` |
| `model/qwen35moe` | `Qwen35moeReferenceError` | `NomenIgnotum` | `UnknownName` |
| `model/qwen35moe` | `Qwen35moeReferenceError` | `NumerusDivergens` | `DivergentCount` |
| `model/qwen35moe` | `Qwen35moeTensorError` | `FormaDiversa` | `DivergentShape` |
| `model/qwen35moe` | `Qwen35moeTensorError` | `NomenDiversum` | `DivergentName` |
| `model/qwen35moe` | `Qwen35moeTensorError` | `NumerusDiversus` | `DivergentCount` |
| `model/qwen35moe` | `Qwen35moeTensorError` | `StipulaDiversa` | `DivergentStorage` |
| `model/safetensors` | `SafetensorError` | `ArchitecturaMala` | `BadArchitecture` |
| `model/safetensors` | `SafetensorError` | `DigestioMala` | `BadDigest` |
| `model/safetensors` | `SafetensorError` | `FiguraMala` | `BadShape` |
| `model/safetensors` | `SafetensorError` | `FormaMala` | `BadFormat` |
| `model/safetensors` | `SafetensorError` | `IngressioMala` | `BadAdmission` |
| `model/safetensors` | `SafetensorError` | `LimitesMala` | `BadBounds` |
| `model/safetensors` | `SafetensorError` | `MerciumMala` | `BadMetadata` |
| `model/safetensors` | `SafetensorError` | `OffscetaMala` | `BadOffset` |
| `model/safetensors` | `SafetensorError` | `TokenizerMala` | `BadTokenizer` |
| `model/safetensors` | `SafetensorError` | `TypoIgnotum` | `UnknownDtype` |
| `model/safetensors` | `SafetensorError` | `VersioIgnota` | `UnknownVersion` |
| `model/tensor_payload` | `PayloadError` | `LongitudoMala` | `BadLength` |
| `model/tensor_payload` | `PayloadError` | `NomineIgnota` | `UnknownName` |
| `model/tensor_payload` | `PayloadError` | `RangeMala` | `BadRange` |
| `model/tensor_view` | `ViewError` | `LayoutIgnota` | `UnknownLayout` |
| `model/tensor_view` | `ViewError` | `LimitesMala` | `BadBounds` |
| `model/tensor_view` | `ViewError` | `LongitudoMala` | `BadLength` |
| `model/tensor_view` | `ViewError` | `NomineIgnota` | `UnknownName` |
| `model/tensor_view` | `ViewError` | `OrdoMala` | `BadOrder` |
| `model/tensor_view` | `ViewError` | `RangeMala` | `BadRange` |
| `model/tensor_view` | `ViewError` | `TypoIgnotum` | `UnknownDtype` |
| `nn` | `NnError` | `DimensioNegativa` | `NegativeDimension` |
| `nn` | `NnError` | `DimensioSupraLimitem` | `DimensionAboveLimit` |
| `nn` | `NnError` | `ElementaMismatch` | `ElementMismatch` |
| `nn` | `NnError` | `FormaMismatch` | `ShapeMismatch` |
| `nn` | `NnError` | `TypoMismatch` | `DtypeMismatch` |
| `optimize` | `OptimizeError` | `FormaMismatch` | `ShapeMismatch` |
| `optimize` | `OptimizeError` | `Gelida` | `Frozen` |
| `optimize` | `OptimizeError` | `GeneratioInvalida` | `InvalidGeneration` |
| `optimize` | `OptimizeError` | `GradusObsoletus` | `StaleGradient` |
| `optimize` | `OptimizeError` | `IdentitasMismatch` | `IdentityMismatch` |
| `optimize` | `OptimizeError` | `LentusInvalida` | `InvalidRate` |
| `optimize` | `OptimizeError` | `NomenDuplicatum` | `DuplicateName` |
| `optimize` | `OptimizeError` | `NomenIgnotum` | `UnknownName` |
| `optimize` | `OptimizeError` | `NomenInane` | `EmptyName` |
| `optimize` | `OptimizeError` | `PassusInvalida` | `InvalidStep` |
| `optimize` | `OptimizeError` | `VersioIgnota` | `UnknownVersion` |
| `optimize` | `OptimizeError` | `VersioInvalida` | `InvalidVersion` |
| `optimize` | `OptimizeError` | `WireMala` | `BadWire` |
| `parameter` | `ParameterError` | `ElementaMismatch` | `ElementMismatch` |
| `parameter` | `ParameterError` | `FormaInvalida` | `InvalidShape` |
| `parameter` | `ParameterError` | `GelidaMutatio` | `FrozenMutation` |
| `parameter` | `ParameterError` | `NomenDuplicatum` | `DuplicateName` |
| `parameter` | `ParameterError` | `NomenIgnotum` | `UnknownName` |
| `parameter` | `ParameterError` | `NomenInane` | `EmptyName` |
| `parameter` | `ParameterError` | `NomenReservatum` | `ReservedName` |
| `parameter` | `ParameterError` | `TypoIgnotum` | `UnknownDtype` |
| `parameter` | `ParameterError` | `VersioInvalida` | `InvalidVersion` |
| `parameter` | `ParameterError` | `WireMala` | `BadWire` |
| `parameter` | `Station` | `Gelida` | `Frozen` |
| `sampling` | `SamplingError` | `ConfiguraInvalida` | `InvalidConfig` |
| `sampling` | `SamplingError` | `HistoriaInvalida` | `InvalidHistory` |
| `serialize` | `SerializeError` | `DataMala` | `BadData` |
| `serialize` | `SerializeError` | `FormaMala` | `BadShape` |
| `serialize` | `SerializeError` | `TypoIgnotum` | `UnknownDtype` |
| `serialize` | `SerializeError` | `VersioIgnota` | `UnknownVersion` |
| `serialize` | `SerializeError` | `WireMala` | `BadWire` |
| `shape` | `ShapeError` | `DimensioNegativa` | `NegativeDimension` |
| `shape` | `ShapeError` | `DimensioSupraLimitem` | `DimensionAboveLimit` |
| `tokenizer` | `TokenizerError` | `ArtificiumMala` | `BadArtifact` |
| `tokenizer` | `TokenizerError` | `DigestioMala` | `BadDigest` |
| `tokenizer` | `TokenizerError` | `EogMala` | `BadEog` |
| `tokenizer` | `TokenizerError` | `MergesMala` | `BadMerges` |
| `tokenizer` | `TokenizerError` | `PreIgnotus` | `UnknownPreTokenizer` |
| `tokenizer` | `TokenizerError` | `ProgeniesIgnota` | `UnknownMergeKind` |
| `tokenizer` | `TokenizerError` | `Utf8Mala` | `BadUtf8` |
| `tokenizer` | `TokenizerError` | `VersioIgnota` | `UnknownVersion` |
| `tokenizer` | `TokenizerError` | `VestigiumIgnotum` | `UnknownTrace` |
| `tokenizer` | `TokenizerError` | `VocabulumMala` | `BadVocab` |
| `tokenizer` | `TokenizerError` | `WireMala` | `BadWire` |
| `tokenizer` | `UnicodeCategory` | `Aliud` | `Other` |
| `tokenizer` | `UnicodeCategory` | `Littera` | `Letter` |
| `tokenizer` | `UnicodeCategory` | `NovumLinea` | `Newline` |
| `tokenizer` | `UnicodeCategory` | `Numerus` | `Number` |
| `tokenizer` | `UnicodeCategory` | `Spatium` | `Space` |
| `train` | `TrainError` | `ModusIgnotus` | `UnknownMode` |
| `train` | `TrainError` | `PassusNegativus` | `NegativeStep` |
| `train` | `TrainError` | `PositioInvalida` | `InvalidPosition` |
| `train` | `TrainError` | `SchedulaInvalida` | `InvalidSchedule` |
| `train` | `TrainError` | `SemenInvalida` | `InvalidSeed` |
| `train` | `TrainError` | `StatumInane` | `EmptyState` |
| `train` | `TrainError` | `ValorMala` | `BadPayload` |
| `train` | `TrainError` | `VersioIgnota` | `UnknownVersion` |
| `train` | `TrainError` | `WireMala` | `BadWire` |
| `transformer` | `TransformerError` | `DimensioInvalida` | `InvalidDimension` |
| `transformer` | `TransformerError` | `DimensioNegativa` | `NegativeDimension` |
| `transformer` | `TransformerError` | `DimensioSupraLimitem` | `DimensionAboveLimit` |
| `transformer` | `TransformerError` | `ElementaMismatch` | `ElementMismatch` |
| `transformer` | `TransformerError` | `FormaMismatch` | `ShapeMismatch` |
| `transformer` | `TransformerError` | `ModusInvalida` | `InvalidMode` |
| `transformer` | `TransformerError` | `PositioInvalida` | `InvalidPosition` |
| `transformer` | `TransformerError` | `TypoMismatch` | `DtypeMismatch` |

Occurrence count: **201**.

### 7.5 Census residual variants (lexicon miss — still rename)

| Union | Old | New | Why missed |
| --- | --- | --- | --- |
| `RopePolicy` | `Interposita` | `Interleaved` | stem not in census lexicon; S2 already has `interleaved_policy` |
| `Station` | `Trainabilis` | `Trainable` | stem not in lexicon; wire value is already `"trainable"` |

`UnicodeCategory.Signum` and `StopPolicy.Eog` stay (retained terms).

---

## 8. Owned wire literals — goal OQ3 **open**

This ledger does **not** decide the pin. U3's default (GOAL / delivery) is
convert + regenerate fixtures. The operator may pin wire stability instead.
Record both sides:

| Literal | Surface | Target if converted | Pin status |
| --- | --- | --- | --- |
| `"aliud"` | `tokenizer.category_name` / `_category_name` (`UnicodeCategory.Aliud`) | `"other"` | **PENDING PIN** (OQ3) |
| `"littera"` | same, `Littera` | `"letter"` | **PENDING PIN** (OQ3) |
| `"numerus"` | same, `Numerus` | `"number"` | **PENDING PIN** (OQ3) |
| `"spatium"` | same, `Spatium` | `"space"` | **PENDING PIN** (OQ3) |
| `"novum_linea"` | same, `NovumLinea` | `"newline"` | **PENDING PIN** (OQ3) |
| `"signum"` | same, `Signum` | `"signum"` | **retained** technical term — not a pin candidate |

If the operator pins wire stability: keep the five Latin category strings
on the wire; still rename identifiers (`Aliud` → `Other`, `category_name`
internals). If unpinned: convert the five strings and regenerate
`fixtures/tokenizer/**` plus any safetensors/GGUF fixture that embeds them.

Already-English wires (not OQ3): `Station.status_name` → `"trainable"` /
`"frozen"`; safetensors / GGUF format tokens listed in §2.3.

---

## 9. Parameter / local word families

Apply these stems to every parameter, local, case-bind, and private helper
that is not a retained exception. Member-declaration names in §§3–7 win
when they disagree with a generic stem (e.g. `longitudo_valoris` →
`value_length`, not `payload_length`).

| Latin family | English | Do not use | Notes |
| --- | --- | --- | --- |
| `nomen` | `name` | | member position legal |
| `clavis` | `key` | | |
| `typo` / `typus` | `dtype` or `kind` | `type` | dtype-bearing vs other |
| `forma` / `figura` | `shape` | | |
| `datos` | `data` | | |
| `digestio` | `digest` | | |
| `longitudo` | `length` | `size` | |
| `stratum` / `stratorum` | `layer` / `layers` | | |
| `initium` | `start` | | |
| `finis` | `end` | | |
| `textum` / `textus` / `textorum` | `text` / `texts` | | |
| `valor` / `valores` / `valorem` | `payload` / `values` | `value` (singular carrier) | lists of JSON values may be `values` |
| `manifestum` | `manifest` | | alias → `gguf_manifest` |
| `capsula` | `capsule` | | |
| `tokenizator` | `tokenizer` | | |
| `parametrum` | `parameter` | | |
| `tensores` / `tensorum` | `tensors` | | |
| `passus` | `step` | | reserved as keyword; member/local `step` was accepted in S2 |
| `poena` | `penalty` | | |
| `configura` / `configuratio` | `config` | | |
| `cancelatum` | `cancellation` | | |
| `versio` | `version` | | |
| `pinnata` | `pinned` | | |
| `octeti` / `octetus` / `octetorum` | `bytes` / `byte` | | |
| `numerus` / `numerum` / `numerorum` | `count` or `number` | | count-of-things vs numeric-value |
| `caput` | `header` | | |
| `vocabulum` | `vocab` | | |
| `elementa` | `elements` | | |
| `limes` / `limites` | `limit` / `bounds` | | |
| `observatum` / `observata` | `observed` | | |
| `expectatum` / `exspectata` | `expected` | | |
| `progenies` | `merge_kind` | `merges` | S2 SEM005 |
| `spatium` | `space` | | |
| `historia` | `history` | | |
| `verba` / `verbum` | `words` / `word` | | |
| `causa` | `message` | | case-bind of error payloads already often `message` |
| `identitas` / `identia` | `identity` | | |
| `possessor` | `owner` | | |
| `statio` | `status` | | S2; not `station` for the enum value name |
| `gelida` | `frozen` | | |
| `semen` | `seed` | | |
| `lentus` | `rate` | | |
| `modus` | `mode` | | |
| `dimensio` | `dimension` | | |
| `cursus` | `cursor` | | |
| `vestigium` | `trace` | | |
| `aliud` | `other` | | |
| `linea` | `line` / `newline` | | `novum_linea` → `newline` |
| `scala` | `scale` | | |
| `aetas` | `age` | | |
| `subsidia` | `support` | | |
| `magna` | `large` | | |
| `generatio` | `generation` | | |
| `fons` | `source` | | |
| `tabula` | `table` | | |
| `summa` | `summary` or `sum` | | admission receipt vs math reduce |
| `media` | `mean` | | already S2 on math |
| `quantitas` | `numel` | `size` | |
| `fragmentum` | `fragment` | | |
| `glomulus` / `glomoris` | `block` | | |
| `referantia` | `reference` | | |
| `congela` | `freeze` | | |
| `inveni` | `find` | | |
| `admittas` / `admitto` / `admissio` | `admit` / `admission` | | |
| `decodere` | `decode` / `decoder` | | |
| `projectio` | `projection` | | |
| `gradientes` / `gradiente` | `gradients` / `gradient` | | |
| `est_` | `is_` | | `est_eog` → `is_eog` |
| `vacua` | `empty` | | |
| `ignota` / `ignotus` | `unknown` | | |
| `architectura` | `architecture` | | |
| `concordatio` | `alignment` | | |
| `inceptum` | `start` | | |
| `magnitudo` | domain English (`state_size`, …) | `size` | |
| `intervallum` | `interval` | | |
| `praeparatio` | `pre` | | tokenizer pre |
| `exemplum` (tokenizer model) | `model` | | `exemplum_tokenizoris` → `tokenizer_model` |
| `nucleus` | `kernel` | | `nucleus_convolutus` → `conv_kernel` |
| `frequentiae` | `freq` | | `basis_frequentiae` → `freq_base` |
| `rotae` | `rope` | | |
| `vestimenti` | `embedding` | | |
| `coetuum` | `group` | | |
| `tractuum` | `block` | | layer-block count |
| `limaturae` | `file` | | `typus_limaturae` → `file_type` |
| `trainabilis` | `trainable` | | |

Constants that embed a family (`PINNATA_P1`, `NOMEN_LIMES`,
`STATIO_GELIDA`, `MAX_NUMERUS`, `TABULA_LITTERAE`) take the same stem
(`PINNED_P1`, `NAME_LIMIT`, `STATUS_FROZEN`, `MAX_NUMBER`, `LETTER_TABLE`).

---

## 10. Comment and owned-string vocabulary

Rewrite every Latin word in live-source comments and owned diagnostic
strings with the same families. Historical factory docs
(`docs/factory/production-ml-library/`, `docs/archived/`) are out of
scope.

### 10.1 Comment stems (src, high-frequency)

`causa`→`message`, `versio`→`version`, `proba`→`proof` (or keep as the
file-type word “proba” when naming `.proba` files), `textus`→`text`,
`mala` (in variant names)→the §7 English, `nomen`→`name`,
`manifestum`→`manifest`, `possessor`→`owner`, `forma`→`shape`,
`structa`→`construct`, `semen`→`seed`, `configura`→`config`,
`ignota`→`unknown`, `identitas`→`identity`, `typo`→`dtype`,
`dimensio`→`dimension`, `decodere`/`datum`→`decode`/`data`,
`generatio`→`generation`, `capsula`→`capsule`, `limes`→`limit`,
`passus`→`step`, `redintegra`→`reset`, `vocabulum`→`vocab`,
`quantitas`→`numel`, `lentus`→`rate`, `modus`→`mode`,
`parametrum`→`parameter`, `octeti`→`bytes`, `gradientes`→`gradients`,
`valor`→`payload`, `poena`→`penalty`, `digestio`→`digest`,
`gelida`→`frozen`, `schedula`→`schedule`, `clavis`→`key`.

Header comments that still use pre-S2 names (`importa ex`, `IdentitasTokenizer`,
`RopeConfigura`, `congela`, `decodere_datum`) are live surface (GOAL OQ1
default: convert). Rewrite them to the locked English.

### 10.2 Owned diagnostic strings in `src` (convert; not OQ3)

| Current | Target |
| --- | --- |
| `manifestum is inconsistent with the artifact identity` | `manifest is inconsistent with the artifact identity` |
| `GGUF UINT64 value exceeds the numerus carrier` | `GGUF UINT64 value exceeds the numeric carrier` |
| `truncated textus field` | `truncated text field` |
| `invalid UTF-8 textus field` | `invalid UTF-8 text field` |

Tokenizer category strings (`aliud`, `littera`, `numerus`, `spatium`,
`novum_linea`) are **wire literals**, not diagnostics — §8.

`signum` as a category_name result is retained.

---

## 11. How later units consume this file

| Unit | Consume |
| --- | --- |
| U2 | §§3–7 rows whose files are in `src/model/` + families in those files |
| U3 | tokenizer/calibration rows + §8 wire literals (pending pin) |
| U4 | decode / generation / cache / sampling / gradient / nn / math |
| U5 | remaining modules, including residual fields/variants |
| U6 | every old name in this ledger, grepped repo-wide |
| U7 | public docs under the **new** names |
| U8 | retained-exception list (§2) is the no-Latin guard allow-list |

Do not add shims. Do not target reserved escapes. Probe `faber check` on
the first file of each wave before batching, especially `values`,
`value_length`, `table`, `step`, and `name`.
