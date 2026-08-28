# Gradus API Reference

**Surface**: final English identifier surface after the no-latin conversion (U1–U6), generated from the live `src/**/*.fab` tree.
**Scope**: public Gradus module declarations and their public class methods. Import coordinates remain `gradus:*`.
**Authority**: `scripta/inventory-public-symbols` checks the live `fn` inventory and verifies every public function name below is documented in its module section.

This reference reports declarations from the live source. Private `_`-prefixed helpers are omitted from the public lists. Retained tokens are the proper noun `gradus`, established technical terms (`eog`, `silu`, `signum`, `fim`, `bpe`, `matmul`), dtype/model/format tokens, and external-format keys.

---

## gradus:attention

Scaled dot-product attention, causal masking, RoPE configuration, multi-head attention, and cached attention.

**Source**: `src/attention.fab`

### Public types

- `union AttentionError` — NegativeDimension, DimensionAboveLimit, ProductAboveLimit, GradusMismatch, ShapeMismatch, Incompatible, DtypeMismatch, ElementMismatch, InvalidPosition, InvalidDimension, InvalidConfig
- `union RopePolicy` — Consecutive, Interleaved
- `class RopeConfig`
  - fields: f32 base, f32 scale, RopePolicy policy
  - methods:
    - `fn base() → f32`
    - `fn scale() → f32`
    - `fn policy() → RopePolicy`
- `class CachedAttention`
  - fields: tensor.NumericBlock context, kv.KVCache state
  - methods:
    - `fn context() → tensor.NumericBlock`
    - `fn state() → kv.KVCache`

### Public functions

- `fn scaled_dot_product_static<size B, size D>(tensor<f32, [B, D]> qb, tensor<f32, [B, D]> kb, tensor<f32, [B, D]> vb, tensor<f32, [B, B]> scale) → tensor<f32, [B, D]>`
- `fn message(AttentionError e) → string`
- `fn consecutive_policy() → RopePolicy`
- `fn interleaved_policy() → RopePolicy`
- `fn policy_name(RopePolicy p) → string`
- `fn construct_rope_config(f32 base, f32 scale, RopePolicy policy) → RopeConfig ⇥ AttentionError`
- `fn default() → RopeConfig`
- `fn rotary_position_embedding(tensor.NumericBlock x, list<int> positions, int dim) → tensor.NumericBlock ⇥ AttentionError`
- `fn rotary_position_embedding_config(tensor.NumericBlock x, list<int> positions, int dim, RopeConfig config) → tensor.NumericBlock ⇥ AttentionError`
- `fn scaled_dot_product(tensor.NumericBlock q, tensor.NumericBlock k, tensor.NumericBlock v, f32 scale) → tensor.NumericBlock ⇥ AttentionError`
- `fn scaled_dot_product_causal(tensor.NumericBlock q, tensor.NumericBlock k, tensor.NumericBlock v, f32 scale) → tensor.NumericBlock ⇥ AttentionError`
- `fn scaled_dot_product_causal_rope(tensor.NumericBlock q, tensor.NumericBlock k, tensor.NumericBlock v, f32 scale, list<int> positions, int dim) → tensor.NumericBlock ⇥ AttentionError`
- `fn multi_head_attention(tensor.NumericBlock q, tensor.NumericBlock k, tensor.NumericBlock v, tensor.NumericBlock wo, int num_heads, int num_kv_heads, f32 scale, list<int> positions, int rope_dim, RopeConfig rope_config) → tensor.NumericBlock ⇥ AttentionError`
- `fn default_cached() → CachedAttention`
- `fn scaled_dot_product_causal_rope_cached(tensor.NumericBlock q, tensor.NumericBlock k, tensor.NumericBlock v, f32 scale, list<int> positions, int dim, kv.KVCache layer, list<int> tokens) → CachedAttention ⇥ AttentionError`
- `fn multi_head_attention_cached(tensor.NumericBlock q, tensor.NumericBlock k, tensor.NumericBlock v, tensor.NumericBlock wo, kv.KVCache layer, int num_heads, int num_kv_heads, f32 scale, list<int> positions, int rope_dim, RopeConfig rope_config, list<int> tokens) → CachedAttention ⇥ AttentionError`

## gradus:cache

KV-cache values, mutation rules, cache identity, identity serialization, and KV structure descriptors.

**Source**: `src/cache.fab`

### Public types

- `union CacheError` — EmptyName, IdOutOfRange, ShapeMismatch, DtypeMismatch, InvalidDimension, ElementMismatch, UnknownVersion, BadWire, InvalidCombination, Overflow, Gap
- `union KvDtype` — F32, F16, Q8_0, Q4_K
- `union SwaType` — Standard, Chunked, Symmetric
- `union LayerStructure` — Dense, SlidingWindow, CompressedHca, Indexer
- `union CachePartition` — IndexerBudget
- `union VLayout` — Transposed, Straight
- `union KvSharing` — Single, GqaShared
- `union AttentionFamily` — Classic, Flash
- `class KVCache`
  - fields: string model, string model_version, string config, string tokenizer, list<int> history, int layers, string dtype, string layout, tensor.NumericBlock key, tensor.NumericBlock payload, int version, int dimension, int capacity
  - methods:
    - `fn model() → string`
    - `fn model_version() → string`
    - `fn config() → string`
    - `fn tokenizer() → string`
    - `fn history() → list<int>`
    - `fn layers() → int`
    - `fn dtype() → string`
    - `fn layout() → string`
    - `fn key() → tensor.NumericBlock`
    - `fn payload() → tensor.NumericBlock`
    - `fn version() → int`
    - `fn dimension() → int`
    - `fn capacity() → int`
    - `fn length() → int`
- `class CacheIdentity`
  - fields: string model, string model_version, string config, string tokenizer, string history, string position, int layers, string dtype, string layout
  - methods:
    - `fn model() → string`
    - `fn model_version() → string`
    - `fn config() → string`
    - `fn tokenizer() → string`
    - `fn history() → string`
    - `fn position() → string`
    - `fn layers() → int`
    - `fn dtype() → string`
    - `fn layout() → string`
- `class LayerSet`
  - fields: list<int> indices, LayerStructure structure, int kv_heads, int head_dim
  - methods:
    - `fn indices() → list<int>`
    - `fn structure() → LayerStructure`
    - `fn kv_heads() → int`
    - `fn head_dim() → int`
- `class KVStructure`
  - fields: list<LayerSet> layers, KvDtype kv_dtype_k, KvDtype kv_dtype_v, VLayout v_layout, KvSharing sharing, AttentionFamily attention_family, int query_heads, int slots, int context_length, string reserve_policy, list<CachePartition> partitions
  - methods:
    - `fn layers() → list<LayerSet>`
    - `fn kv_dtype_k() → KvDtype`
    - `fn kv_dtype_v() → KvDtype`
    - `fn v_layout() → VLayout`
    - `fn sharing() → KvSharing`
    - `fn attention_family() → AttentionFamily`
    - `fn query_heads() → int`
    - `fn slots() → int`
    - `fn context_length() → int`
    - `fn reserve_policy() → string`
    - `fn partitions() → list<CachePartition>`

### Public functions

- `fn message(CacheError e) → string`
- `fn cache_equal(KVCache a, KVCache b) → bool`
- `fn empty_cache(string model, string model_version, string config, string tokenizer, int layers, int dimension) → KVCache ⇥ CacheError`
- `fn default() → KVCache`
- `fn append(KVCache c, int token_id, tensor.NumericBlock key, tensor.NumericBlock payload) → KVCache ⇥ CacheError`
- `fn extend(KVCache c, list<int> tokens, tensor.NumericBlock key, tensor.NumericBlock payload) → KVCache ⇥ CacheError`
- `fn reset(KVCache c) → KVCache ⇥ CacheError`
- `fn cache_identity_equal(CacheIdentity a, CacheIdentity b) → bool`
- `fn cache_identity(KVCache c) → CacheIdentity`
- `fn serialize_identity(CacheIdentity i) → string`
- `fn deserialize_identity(string wire) → CacheIdentity ⇥ CacheError`
- `fn kv_dtype_f32() → KvDtype`
- `fn kv_dtype_f16() → KvDtype`
- `fn kv_dtype_q8_0() → KvDtype`
- `fn kv_dtype_q4_k() → KvDtype`
- `fn kv_dtype_name(KvDtype t) → string`
- `fn kv_dtype_eq(KvDtype a, KvDtype b) → bool`
- `fn swa_standard() → SwaType`
- `fn swa_chunked() → SwaType`
- `fn swa_symmetric() → SwaType`
- `fn swa_type_name(SwaType t) → string`
- `fn swa_type_eq(SwaType a, SwaType b) → bool`
- `fn dense_structure() → LayerStructure`
- `fn sliding_window_structure(int window, SwaType swa_kind) → LayerStructure ⇥ CacheError`
- `fn compressed_hca_structure(int ratio) → LayerStructure ⇥ CacheError`
- `fn indexer_structure() → LayerStructure`
- `fn hca_ratio(LayerStructure s) → int`
- `fn layer_structure_name(LayerStructure s) → string`
- `fn default_cache_partition() → CachePartition`
- `fn indexer_budget(int bytes) → CachePartition ⇥ CacheError`
- `fn partition_class_name(CachePartition p) → string`
- `fn partition_bytes(CachePartition p) → int`
- `fn cache_partition_eq(CachePartition a, CachePartition b) → bool`
- `fn v_layout_transposed() → VLayout`
- `fn v_layout_straight() → VLayout`
- `fn v_layout_name(VLayout v) → string`
- `fn v_layout_eq(VLayout a, VLayout b) → bool`
- `fn sharing_single() → KvSharing`
- `fn sharing_gqa() → KvSharing`
- `fn sharing_name(KvSharing s) → string`
- `fn sharing_eq(KvSharing a, KvSharing b) → bool`
- `fn attention_classic() → AttentionFamily`
- `fn attention_flash() → AttentionFamily`
- `fn attention_family_name(AttentionFamily f) → string`
- `fn attention_family_eq(AttentionFamily a, AttentionFamily b) → bool`
- `fn default_layer_set() → LayerSet`
- `fn construct_layer_set(list<int> indices, LayerStructure structure, int kv_heads, int head_dim) → LayerSet ⇥ CacheError`
- `fn default_kv_structure() → KVStructure`
- `fn kv_structure_equal(KVStructure a, KVStructure b) → bool`
- `fn construct_kv_structure(list<LayerSet> layers, KvDtype kv_dtype_k, KvDtype kv_dtype_v, VLayout v_layout, KvSharing sharing, AttentionFamily attention_family, int query_heads, int slots, int context_length) → KVStructure ⇥ CacheError`
- `fn construct_kv_structure_with_partitions(list<LayerSet> layers, KvDtype kv_dtype_k, KvDtype kv_dtype_v, VLayout v_layout, KvSharing sharing, AttentionFamily attention_family, int query_heads, int slots, int context_length, list<CachePartition> partitions) → KVStructure ⇥ CacheError`
- `fn serialize_structure(KVStructure s) → string`
- `fn deserialize_structure(string wire) → KVStructure ⇥ CacheError`
- `fn empty_layers(KVStructure s, string model, string model_version, string config, string tokenizer) → list<KVCache> ⇥ CacheError`

## gradus:calibration

Expert residual-energy calibration bake (W5d-U1). Measurement artifact: per-expert unrepresentable-energy scores, fitted base-count/K curve, overlap census, and 75e4ab98 provenance-digest fields. Not a weight transform.

**Source**: `src/calibration.fab`

### Public types

- `union CalibrationError` — EmptyCorpus, ZeroRouting, DigestMismatch, DigestMalformed, ThresholdInvalid, DimensionMismatch, ExpertRange, BasisInvalid, NonFinite, Invalid
- `class RoutingActivation`
  - fields: int layer, int expert, f32 mass, list<f32> output
  - methods:
    - `fn layer() → int`
    - `fn expert() → int`
    - `fn mass() → f32`
    - `fn output() → list<f32>`
- `class CalibrationCorpus`
  - fields: list<RoutingActivation> activations, int layers, int experts, int dimension
  - methods:
    - `fn activations() → list<RoutingActivation>`
    - `fn layers() → int`
    - `fn experts() → int`
    - `fn dimension() → int`
- `class ExpertEnergy`
  - fields: int layer, int expert, f32 residual, f32 mass
  - methods:
    - `fn layer() → int`
    - `fn expert() → int`
    - `fn residual() → f32`
    - `fn mass() → f32`
- `class CurvePoint`
  - fields: int bases, int rank, f32 residual
  - methods:
    - `fn bases() → int`
    - `fn rank() → int`
    - `fn residual() → f32`
- `class SimilarityCell`
  - fields: int layer, int expert_a, int expert_b, f32 cosine
  - methods:
    - `fn layer() → int`
    - `fn expert_a() → int`
    - `fn expert_b() → int`
    - `fn cosine() → f32`
- `class Provenance`
  - fields: string algorithm, string digest, int length, string corpus_digest, string base_digest
  - methods:
    - `fn algorithm() → string`
    - `fn digest() → string`
    - `fn length() → int`
    - `fn corpus_digest() → string`
    - `fn base_digest() → string`
- `class ResidualEnergyArtifact`
  - fields: string schema, list<ExpertEnergy> scores, list<CurvePoint> curve, list<SimilarityCell> similarities, int recommended_k, f32 threshold, bool below_threshold, Provenance provenance
  - methods:
    - `fn schema() → string`
    - `fn scores() → list<ExpertEnergy>`
    - `fn curve() → list<CurvePoint>`
    - `fn similarities() → list<SimilarityCell>`
    - `fn recommended_k() → int`
    - `fn threshold() → f32`
    - `fn below_threshold() → bool`
    - `fn provenance() → Provenance`

### Public functions

- `fn message(CalibrationError e) → string`
- `fn activation(int layer, int expert, f32 mass, list<f32> output) → RoutingActivation`
- `fn corpus(list<RoutingActivation> activations, int layers, int experts, int dimension) → CalibrationCorpus ⇥ CalibrationError`
- `fn default() → ResidualEnergyArtifact`
- `fn bake(CalibrationCorpus corpus, list<list<f32>> bases, f32 threshold, string algorithm, string digest, int length, string corpus_digest, string base_digest) → ResidualEnergyArtifact ⇥ CalibrationError`
- `fn score_count(ResidualEnergyArtifact artifact) → int`
- `fn curve_count(ResidualEnergyArtifact artifact) → int`
- `fn similarity_count(ResidualEnergyArtifact artifact) → int`
- `fn curve_residual(ResidualEnergyArtifact artifact, int k) → f32`
- `fn score_residual(ResidualEnergyArtifact artifact, int i) → f32`
- `fn similarity_cosine(ResidualEnergyArtifact artifact, int i) → f32`
- `fn verify(ResidualEnergyArtifact artifact, string expected) → ResidualEnergyArtifact ⇥ CalibrationError`

## gradus:data

Reserved data-module import surface; no public functions are currently declared.

**Source**: `src/data.fab`

### Public functions

- None declared.

## gradus:decode

One-token decode, prefill, explicit sessions, cancellation, replica-loop mechanics, and cached decode.

**Source**: `src/decode.fab`

### Public types

- `union DecodeError` — IdOutOfRange, InvalidPosition, LimitReached, InvalidDecoder, ShapeMismatch, DtypeMismatch, ElementMismatch, Incompatible, InvalidDimension, Cancelled, SamplingFailure
- `class Weights`
  - fields: tensor.NumericBlock ln1_s, tensor.NumericBlock ln1_o, tensor.NumericBlock wq, tensor.NumericBlock bq, tensor.NumericBlock wk, tensor.NumericBlock bk, tensor.NumericBlock wv, tensor.NumericBlock bv, tensor.NumericBlock wo, tensor.NumericBlock bo, tensor.NumericBlock ln2_s, tensor.NumericBlock ln2_o, tensor.NumericBlock wf1, tensor.NumericBlock bf1, tensor.NumericBlock wf2, tensor.NumericBlock bf2, tensor.NumericBlock ln3_s, tensor.NumericBlock ln3_o
  - methods:
    - `fn ln1_s() → tensor.NumericBlock`
    - `fn ln1_o() → tensor.NumericBlock`
    - `fn wq() → tensor.NumericBlock`
    - `fn bq() → tensor.NumericBlock`
    - `fn wk() → tensor.NumericBlock`
    - `fn bk() → tensor.NumericBlock`
    - `fn wv() → tensor.NumericBlock`
    - `fn bv() → tensor.NumericBlock`
    - `fn wo() → tensor.NumericBlock`
    - `fn bo() → tensor.NumericBlock`
    - `fn ln2_s() → tensor.NumericBlock`
    - `fn ln2_o() → tensor.NumericBlock`
    - `fn wf1() → tensor.NumericBlock`
    - `fn bf1() → tensor.NumericBlock`
    - `fn wf2() → tensor.NumericBlock`
    - `fn bf2() → tensor.NumericBlock`
    - `fn ln3_s() → tensor.NumericBlock`
    - `fn ln3_o() → tensor.NumericBlock`
- `class Decoder`
  - fields: tensor.NumericBlock table, Weights weights, tensor.NumericBlock projection, tensor.NumericBlock projection_bias, f32 scale, int vocabulary, int context, int dimension
  - methods:
    - `fn table() → tensor.NumericBlock`
    - `fn weights() → Weights`
    - `fn projection() → tensor.NumericBlock`
    - `fn projection_bias() → tensor.NumericBlock`
    - `fn scale() → f32`
    - `fn vocabulary() → int`
    - `fn context() → int`
    - `fn dimension() → int`
- `class DecodeStep`
  - fields: tensor.NumericBlock logits, kv.KVCache state
  - methods:
    - `fn logits() → tensor.NumericBlock`
    - `fn state() → kv.KVCache`
- `class Session`
  - fields: int position, int context
  - methods:
    - `fn position() → int`
    - `fn context() → int`
- `class Cancellation`
  - fields: bool cancelled
  - methods:
    - `fn cancelled() → bool`

### Public functions

- `fn message(DecodeError e) → string`
- `fn construct_weights(tensor.NumericBlock ln1_s, tensor.NumericBlock ln1_o, tensor.NumericBlock wq, tensor.NumericBlock bq, tensor.NumericBlock wk, tensor.NumericBlock bk, tensor.NumericBlock wv, tensor.NumericBlock bv, tensor.NumericBlock wo, tensor.NumericBlock bo, tensor.NumericBlock ln2_s, tensor.NumericBlock ln2_o, tensor.NumericBlock wf1, tensor.NumericBlock bf1, tensor.NumericBlock wf2, tensor.NumericBlock bf2, tensor.NumericBlock ln3_s, tensor.NumericBlock ln3_o) → Weights`
- `fn construct_decoder(tensor.NumericBlock table, Weights weights, tensor.NumericBlock projection, tensor.NumericBlock projection_bias, f32 scale, int vocabulary, int context, int dimension) → Decoder ⇥ DecodeError`
- `fn default() → Decoder`
- `fn decode_data(int token_id, int position, Decoder m) → tensor.NumericBlock ⇥ DecodeError`
- `fn default_step() → DecodeStep`
- `fn decode_cached(int token_id, int position, Decoder m, kv.KVCache layer) → DecodeStep ⇥ DecodeError`
- `fn prefill(list<int> tokens, Decoder m) → tensor.NumericBlock ⇥ DecodeError`
- `fn fresh_session(int context) → Session ⇥ DecodeError`
- `fn default_session() → Session`
- `fn advance(Session s) → Session ⇥ DecodeError`
- `fn reset(Session s) → Session`
- `fn fresh_cancellation() → Cancellation`
- `fn cancellation_cancelled() → Cancellation`
- `fn observe_cancellation(Cancellation c) → Cancellation ⇥ DecodeError`
- `fn replay(list<list<f32>> logit_rows, sampling.Config c, list<int> history, train.Seed seed, Cancellation cancellation) → list<int> ⇥ DecodeError`

## gradus:dtype

Dtype tags, promotion, narrowing, serialization, and finite/cast checks.

**Source**: `src/dtype.fab`

### Public types

- `union DType` — F32, F16, I32, U8
- `union DTypeError` — UnknownName, UnknownVersion, NonFinite, Overflow

### Public functions

- `fn f32() → DType`
- `fn f16() → DType`
- `fn i32() → DType`
- `fn u8() → DType`
- `fn eq(DType a, DType b) → bool`
- `fn message(DTypeError e) → string`
- `fn name(DType t) → string`
- `fn from_name(string s) → DType ⇥ DTypeError`
- `fn width(DType t) → int`
- `fn serialize(DType t) → string`
- `fn deserialize(string s) → DType ⇥ DTypeError`
- `fn promote(DType a, DType b) → bool`
- `fn narrow(DType a, DType b) → bool`
- `fn finite(f32 x) → bool`
- `fn cast(f32 payload, DType source, DType target) → f32 ⇥ DTypeError`

## gradus:generation

Generation configuration, sampling projection, serialized config, cursor limits, and dense generate routes.

**Source**: `src/generation.fab`

### Public types

- `union GenerationError` — InvalidConfig, ElementMismatch, DtypeMismatch, Incompatible, UnknownVersion, BadWire, LimitReached, Cancelled, DecodeFailure
- `union StopPolicy` — Eog, IgnoreEos. `Eog` emits the first admitted EOG `{0, 2}` then halt; `IgnoreEos` suppresses EOG ids from sampling and runs to the `max_tokens` ceiling
- `class GenerationConfig`
  - fields: int context, int max_prompt, int max_tokens, int seed, f32 temperature, int top_k, f32 top_p, f32 min_p, f32 repetition_penalty
  - methods:
    - `fn context() → int`
    - `fn max_prompt() → int`
    - `fn max_tokens() → int`
    - `fn seed() → int`
    - `fn temperature() → f32`
    - `fn top_k() → int`
    - `fn top_p() → f32`
    - `fn min_p() → f32`
    - `fn repetition_penalty() → f32`
- `class GenerationCursor`
  - fields: decode.Session session, int emitted
  - methods:
    - `fn session() → decode.Session`
    - `fn emitted() → int`
- `class DenseEngine`
  - fields: dense.DenseConfig architecture, f32 epsilon, f32 scale, int rope_dim, attention.RopeConfig rope

### Public functions

- `fn message(GenerationError e) → string`
- `fn generation_equal(GenerationConfig a, GenerationConfig b) → bool`
- `fn construct_generation(int context, int max_prompt, int max_tokens, int seed, f32 temperature, int top_k, f32 top_p, f32 min_p, f32 repetition_penalty) → GenerationConfig ⇥ GenerationError`
- `fn default() → GenerationConfig`
- `fn generation_failure(int context, int max_prompt, int max_tokens, int seed) → GenerationConfig ⇥ GenerationError`
- `fn support_flags() → list<string>`
- `fn admitted_features(string name) → bool`
- `fn config(GenerationConfig g) → sampling.Config ⇥ GenerationError`
- `fn seed(GenerationConfig g) → train.Seed ⇥ GenerationError`
- `fn serialize_generation(GenerationConfig g) → string`
- `fn deserialize_generation(string wire) → GenerationConfig ⇥ GenerationError`
- `fn fresh_cursor(GenerationConfig g) → GenerationCursor ⇥ GenerationError`
- `fn default_cursor() → GenerationCursor`
- `fn token_allowed(GenerationConfig g, GenerationCursor c) → bool`
- `fn cursor_advance(GenerationConfig g, GenerationCursor c) → GenerationCursor ⇥ GenerationError`
- `fn cursor_reset(GenerationCursor c) → GenerationCursor`
- `fn eog_stop() → StopPolicy`
- `fn ignore_eos() → StopPolicy`
- `fn stop_policy_name(StopPolicy p) → string`
- `fn stops_on_eog(StopPolicy p) → bool`
- `fn cursor_after_prompt(GenerationConfig g, int prompt_len) → GenerationCursor ⇥ GenerationError`
- `fn generate(GenerationConfig g, list<int> prompt_ids, decode.Decoder m) → list<int> ⇥ GenerationError {` — EOG-stop default
- `fn generate_with_stop(GenerationConfig g, list<int> prompt_ids, decode.Decoder m, StopPolicy stop) → list<int> ⇥ GenerationError`
- `fn generate_cancelled(GenerationConfig g, list<int> prompt_ids, decode.Decoder m, decode.Cancellation cancel) → list<int> ⇥ GenerationError {` — EOG-stop default
- `fn generate_cancelled_with_stop(GenerationConfig g, list<int> prompt_ids, decode.Decoder m, decode.Cancellation cancel, StopPolicy stop) → list<int> ⇥ GenerationError`
- `fn construct_dense_engine(dense.DenseConfig architecture, f32 epsilon, f32 scale, int rope_dim, attention.RopeConfig rope) → DenseEngine`
- `fn default_dense_engine() → DenseEngine`
- `fn generate_dense(GenerationConfig g, list<int> prompt_ids, DenseEngine engine, (string, int) → tensor.NumericBlock ⇥ dense.DenseError source, list<kv.KVCache> layers, decode.Cancellation cancel) → list<int> ⇥ GenerationError {` — EOG-stop default
- `fn generate_dense_with_stop(GenerationConfig g, list<int> prompt_ids, DenseEngine engine, (string, int) → tensor.NumericBlock ⇥ dense.DenseError source, list<kv.KVCache> layers, decode.Cancellation cancel, StopPolicy stop) → list<int> ⇥ GenerationError`

## gradus:gradient

Gradient records and the forward/companion gradient wrapper surface.

**Source**: `src/gradient.fab`

### Public types

- `union GradientError` — UnknownGradient, GradientVersion
- `class Gradient`
  - fields: string owner, string name, int version, tensor.NumericBlock payload
  - methods:
    - `fn owner() → string`
    - `fn name() → string`
    - `fn version() → int`
    - `fn payload() → tensor.NumericBlock`
- `class Gradients`
  - fields: list<Gradient> gradients
  - methods:
    - `fn count() → int`
    - `fn find(string owner, string name) → Gradient ⇥ GradientError`

### Public functions

- `fn message(GradientError e) → string`
- `fn construct(string name, string owner, int version, tensor.NumericBlock payload) → Gradient ⇥ GradientError`
- `fn default() → Gradient`
- `fn construct_gradients(list<Gradient> gradients) → Gradients`
- `fn obsolete(Gradient g, int current_version) → bool`
- `fn nil() → void`
- `fn simple_loss<size R, size C>(tensor<f32, [R, C]> x, tensor<f32, [R, C]> w) → f32`
- `fn gradients_simple_loss<size R, size C>(tensor<f32, [R, C]> x, tensor<f32, [R, C]> w, f32 upstream, string name, string owner, int version) → Gradients ⇥ GradientError`
- `fn masked_mean<size N>(tensor<f32, [N]> x, tensor<f32, [N]> mask) → f32`
- `fn gradients_masked_mean<size N>(tensor<f32, [N]> x, tensor<f32, [N]> mask, f32 upstream, string name, string owner, int version) → Gradients ⇥ GradientError`

## gradus:gradus

Package map facade. No genera.

**Source**: `src/gradus.fab`

### Public functions

- None declared.

## gradus:loss

NumericBlock loss functions and fixed-shape MSE rows.

**Source**: `src/loss.fab`

### Public types

- `union LossError` — NegativeDimension, DimensionAboveLimit, ProductAboveLimit, GradusMismatch, ShapeMismatch, DtypeMismatch, ElementMismatch, Incompatible, NonFinite

### Public functions

- `fn message(LossError e) → string`
- `fn mse(tensor.NumericBlock prediction, tensor.NumericBlock target) → f32 ⇥ LossError`
- `fn cross_entropy(tensor.NumericBlock logits, tensor.NumericBlock target) → f32 ⇥ LossError`
- `fn mse_2x2(tensor<f32, [2, 2]> prediction, tensor<f32, [2, 2]> target) → f32`
- `fn mse_4x4(tensor<f32, [4, 4]> prediction, tensor<f32, [4, 4]> target) → f32`
- `fn mse_2x8(tensor<f32, [2, 8]> prediction, tensor<f32, [2, 8]> target) → f32`

## gradus:math

Device-neutral tensor arithmetic, reductions, matrix multiplication, casts, concatenation, and slicing.

**Source**: `src/math.fab`

### Public types

- `union MathError` — NegativeDimension, DimensionAboveLimit, ProductAboveLimit, ShapeMismatch, GradusMismatch, Incompatible, DtypeMismatch, ElementMismatch, NonFinite, Overflow, UnknownName

### Public functions

- `fn message(MathError e) → string`
- `fn construct(list<f32> data, list<int> shape) → tensor.NumericBlock ⇥ MathError`
- `fn add<size M, size N>(tensor<f32, [M, N]> a, tensor<f32, [M, N]> b) → tensor<f32, [M, N]>`
- `fn add_carrier(tensor.NumericBlock a, tensor.NumericBlock b) → tensor.NumericBlock ⇥ MathError`
- `fn sub(tensor.NumericBlock a, tensor.NumericBlock b) → tensor.NumericBlock ⇥ MathError`
- `fn mul(tensor.NumericBlock a, tensor.NumericBlock b) → tensor.NumericBlock ⇥ MathError`
- `fn div(tensor.NumericBlock a, tensor.NumericBlock b) → tensor.NumericBlock ⇥ MathError`
- `fn neg(tensor.NumericBlock t) → tensor.NumericBlock ⇥ MathError`
- `fn abs(tensor.NumericBlock t) → tensor.NumericBlock ⇥ MathError`
- `fn signum(tensor.NumericBlock t) → tensor.NumericBlock ⇥ MathError`
- `fn sum(tensor.NumericBlock t, int axis) → tensor.NumericBlock ⇥ MathError`
- `fn mean(tensor.NumericBlock t, int axis) → tensor.NumericBlock ⇥ MathError`
- `fn matmul(tensor.NumericBlock a, tensor.NumericBlock b) → tensor.NumericBlock ⇥ MathError`
- `fn cast(tensor.NumericBlock t, string name) → tensor.NumericBlock ⇥ MathError`
- `fn concatenate(list<tensor.NumericBlock> parts, int axis) → tensor.NumericBlock ⇥ MathError`
- `fn slice(tensor.NumericBlock t, int axis, int start, int end) → tensor.NumericBlock ⇥ MathError`

## gradus:metrics

Classification accuracy and validated loss/accuracy metric records.

**Source**: `src/metrics.fab`

### Public types

- `union MetricError` — GradusMismatch, ShapeMismatch, DtypeMismatch, ElementMismatch, NonFinite, Incompatible, Invalid
- `class Metric`
  - fields: f32 loss, f32 accuracy
  - methods:
    - `fn loss() → f32`
    - `fn accuracy() → f32`

### Public functions

- `fn message(MetricError e) → string`
- `fn accuracy(tensor.NumericBlock prediction, tensor.NumericBlock target) → f32 ⇥ MetricError`
- `fn metric(f32 loss, f32 accuracy) → Metric ⇥ MetricError`
- `fn default() → Metric`
- `fn metric_equal(Metric a, Metric b) → bool`

## gradus:mlp

Two-layer MLP: staged `forward_mlp` over the nn carrier and the annotated training-path companion `forward_mlp_loss`.

**Source**: `src/mlp.fab`

### Public types

- `union GradusError` — NegativeDimension, DimensionAboveLimit, ProductAboveLimit, GradusMismatch, ShapeMismatch, Incompatible, DtypeMismatch, ElementMismatch

### Public functions

- `fn message(GradusError e) → string`
- `fn forward_mlp(tensor.NumericBlock x, tensor.NumericBlock w1, tensor.NumericBlock b1, tensor.NumericBlock w2, tensor.NumericBlock b2) → tensor.NumericBlock ⇥ GradusError`
- `fn nil() → void`
- `fn forward_mlp_loss(tensor<f32, [4, 4]> input, tensor<f32, [4, 4]> weight1, tensor<f32, [4, 4]> bias1, tensor<f32, [4, 4]> weight2, tensor<f32, [4, 4]> bias2, tensor<f32, [4, 4]> target) → f32`

## gradus:model/artifact

Pathless content identity for bounded model artifacts.

**Source**: `src/model/artifact.fab`

### Public types

- `union ArtifactError` — UnknownAlgorithm, BadDigest, BadLength
- `class ContentIdentity`
  - fields: string algorithm, string digest, int length

### Public functions

- `fn message(ArtifactError e) → string`
- `fn identity(string algorithm, string digest, int length) → ContentIdentity ⇥ ArtifactError`

## gradus:model/capsule

Schema-versioned admitted-model capsules and per-format manifest identity handoff.

**Source**: `src/model/capsule.fab`

### Public types

- `union AdmissionError` — UnknownVersion, RetiredSchema, UnknownAlgorithm, BadDigest, BadManifest, BadWire
- `union Manifest` — Gguf, Safetensors
- `class SafetensorsMetadata`
  - fields: string key, string payload
  - methods:
    - `fn key() → string`
    - `fn payload() → string`
- `class SafetensorsTensorDescriptor`
  - fields: string name, string dtype, list<int> shape, int start, int end, int elements
  - methods:
    - `fn name() → string`
    - `fn dtype() → string`
    - `fn shape() → list<int>`
    - `fn start() → int`
    - `fn end() → int`
    - `fn elements() → int`
- `class SafetensorsManifest`
  - fields: string format, string version, int artifact_length, int data_length, list<SafetensorsMetadata> metadata, list<SafetensorsTensorDescriptor> tensors
  - methods:
    - `fn format() → string`
    - `fn version() → string`
    - `fn artifact_length() → int`
    - `fn data_length() → int`
    - `fn metadata_count() → int`
    - `fn tensor_count() → int`
    - `fn metadata(int i) → SafetensorsMetadata ⇥ AdmissionError`
    - `fn description(int i) → SafetensorsTensorDescriptor ⇥ AdmissionError`
- `class Capsule`
  - fields: string schema, artifact.ContentIdentity identity, Manifest manifest
  - methods:
    - `fn schema() → string`
    - `fn artifact_identity() → artifact.ContentIdentity`
    - `fn algorithm() → string`
    - `fn digest() → string`
    - `fn length() → int`
    - `fn format() → string`
    - `fn tensor_count() → int`
    - `fn gguf_manifest() → gguf_manifest.GgufManifest ∪ null`
    - `fn safetensors_manifest() → SafetensorsManifest ∪ null`
    - `fn identity() → Identity`
- `class Identity`
  - fields: string schema, string algorithm, string digest, int byte_length
  - methods:
    - `fn schema() → string`
    - `fn algorithm() → string`
    - `fn digest() → string`
    - `fn byte_length() → int`

### Public functions

- `fn message(AdmissionError e) → string`
- `fn from_gguf(gguf_manifest.GgufManifest m) → Manifest`
- `fn safetensors_manifest(SafetensorsManifest m) → Manifest`
- `fn identity_equal(Identity a, Identity b) → bool`
- `fn construct_manifest(string schema, artifact.ContentIdentity identity, Manifest manifest) → Capsule ⇥ AdmissionError`
- `fn verify(Capsule c) → bool ⇥ AdmissionError`
- `fn verify_against(Capsule c, string expected) → bool ⇥ AdmissionError`
- `fn serialize_identity(Capsule c) → string ⇥ AdmissionError`
- `fn deserialize_identity(string wire) → Identity ⇥ AdmissionError`

## gradus:model/dense

Ordered dense-model forward assembly over canonical architecture descriptors and stored-weight views, including cached decode steps.

**Source**: `src/model/dense.fab`

### Public types

- `union DenseError` — MissingTensor, BadConfig, BadShape, TerminusExcedit
- `class DenseConfig`
  - fields: int layers, int heads, int kv_heads, int head_dim, int hidden_dim, int vocab, bool tied
- `class DenseStep`
  - fields: tensor.NumericBlock logits, list<kv.KVCache> layers
  - methods:
    - `fn logits() → tensor.NumericBlock`
    - `fn layers() → list<kv.KVCache>`

### Public functions

- `fn message(DenseError e) → string`
- `fn forward(DenseConfig cfg, (string, int) → tensor.NumericBlock ⇥ DenseError source, list<int> tokens, f32 epsilon, f32 scale, list<int> positions, int rope_dim, attention.RopeConfig rope_cfg) → tensor.NumericBlock ⇥ DenseError`
- `fn default_step() → DenseStep`
- `fn empty_caches(kv.KVStructure structure, string model, string model_version, string config, string tokenizer) → list<kv.KVCache> ⇥ DenseError`
- `fn decode_step(DenseConfig cfg, (string, int) → tensor.NumericBlock ⇥ DenseError source, int token_id, int position, f32 epsilon, f32 scale, int rope_dim, attention.RopeConfig rope_cfg, list<kv.KVCache> layers) → DenseStep ⇥ DenseError`

## gradus:model/dense_llama

Llama/SmolLM2 canonical tensor-name resolution and frozen architecture facts.

**Source**: `src/model/dense_llama.fab`

### Public types

- `union LlamaError` — UnknownCanonicalName, LayerOutOfRange, MissingTensor, UnknownLayout
- `class LlamaArch`
  - fields: string name, int layers, int heads, int kv_heads, int head_dim, int hidden_dim, int vocab, bool tied
- `class CanonicalDescriptor`
  - fields: string canonical_name, string gguf_name, list<int> shape, int dtype_ggml, gguf_manifest.GgmlLayout layout

### Public functions

- `fn message(LlamaError e) → string`
- `fn smollm2_arch() → LlamaArch`
- `fn layout_note(gguf_manifest.GgmlLayout l) → string`
- `fn gguf_name(LlamaArch a, string canonical, int layer) → string ⇥ LlamaError`
- `fn resolve(gguf_manifest.GgufManifest m, LlamaArch a, string canonical, int layer) → CanonicalDescriptor ⇥ LlamaError`

## gradus:model/dense_qwen2

Qwen2 canonical tensor-name resolution and architecture configuration.

**Source**: `src/model/dense_qwen2.fab`

### Public types

- `union DenseQwen2Error` — UnknownArchitecture, UnknownCanonical, LayerOutOfRange, MissingTensor, BadConfig
- `class DenseQwen2Config`
  - fields: int layers, int heads, int kv_heads, int head_dim, int hidden_dim, int vocab, int theta, bool tied

### Public functions

- `fn message(DenseQwen2Error e) → string`
- `fn config(gguf_manifest.GgufManifest m) → DenseQwen2Config ⇥ DenseQwen2Error`
- `fn resolve(DenseQwen2Config cfg, gguf_manifest.GgufManifest m, string name) → gguf_manifest.GgufTensorDescriptor ⇥ DenseQwen2Error`
- `fn render_description(gguf_manifest.GgufTensorDescriptor t) → string`

## gradus:model/dequant

CPU dequantization for the admitted GGML block formats.

**Source**: `src/model/dequant.fab`

### Public types

- `union DequantError` — UnknownDtype, BadBlock, BadOrder, BadPayload
- `class MinScale`
  - fields: int sc, int m

### Public functions

- `fn message(DequantError e) → string`
- `fn block_elements(int kind) → int`
- `fn block_bytes(int kind) → int`
- `fn dequantize_block(int kind, list<int<u8>> blocks) → list<f32> ⇥ DequantError`
- `fn dequantize_order(int kind, list<int<u8>> bytes) → list<f32> ⇥ DequantError`

## gradus:model/gguf

GGUF row admission into the typed model capsule.

**Source**: `src/model/gguf.fab`

### Public types

- `union GgufError` — BadFormat, UnknownVersion, BadArchitecture, UnknownQuantization, BadOffset, BadShape, BadTokenizer, BadBounds, BadWire, BadCapsule

### Public functions

- `fn message(GgufError e) → string`
- `fn admit(list<int<u8>> bytes, string digest, int expected_kv, int expected_tensors, int expected_elements, int expected_f32, int expected_q4k, int expected_q5, int expected_q6, int expected_q8) → capsule.Capsule ⇥ GgufError`

## gradus:model/gguf_manifest

Bounded GGUF v3 parsing, range inspection, typed metadata, and tensor descriptors.

**Source**: `src/model/gguf_manifest.fab`

### Public types

- `union GgufManifestError` — BadFormat, UnknownVersion, Truncated, BadWire, BadBounds, Surplus, DuplicateKey, DuplicateTensor, BadOffset, UnknownLayout, BadIdentity, BadSource, NotFound
- `union GgmlLayout` — Known, Unknown
- `class GgufCorpus`
  - fields: bytes table, int artifact_length, artifact.ContentIdentity identity
- `class GgufMetadata`
  - fields: string key, int dtype, bytes payload_wire
- `class GgufTensorDescriptor`
  - fields: string name, list<int> shape, int dtype_ggml, int relative_offset, int elements, GgmlLayout layout
- `class GgufManifest`
  - fields: artifact.ContentIdentity identity, int version, int alignment, int data_start, int artifact_length, list<GgufMetadata> metadata, list<GgufTensorDescriptor> tensors

### Public functions

- `fn message(GgufManifestError e) → string`
- `fn layout(int ggml_dtype, list<int> shape) → GgmlLayout ⇥ GgufManifestError`
- `fn metadata(GgufManifest m, string key) → GgufMetadata ⇥ GgufManifestError`
- `fn text(GgufManifest m, string key) → string ⇥ GgufManifestError`
- `fn number(GgufManifest m, string key) → int ⇥ GgufManifestError`
- `fn texts(GgufManifest m, string key) → list<string> ⇥ GgufManifestError`
- `fn numbers(GgufManifest m, string key) → list<int> ⇥ GgufManifestError`
- `fn numbers_u32(GgufManifest m, string key) → list<int> ⇥ GgufManifestError`
- `fn boolean(GgufManifest m, string key) → bool ⇥ GgufManifestError`
- `fn list_length(GgufManifest m, string key) → int ⇥ GgufManifestError`
- `fn find_tensor(GgufManifest m, string name) → GgufTensorDescriptor ⇥ GgufManifestError`
- `fn payload_limit(GgufManifest m, string name) → tuple<int, int> ⇥ GgufManifestError`
- `fn parse(GgufCorpus corpus) → GgufManifest ⇥ GgufManifestError`
- `fn inspect((int, int) → bytes ⇥ GgufManifestError source, int artifact_length, artifact.ContentIdentity identity) → GgufManifest ⇥ GgufManifestError`
- `fn read_fragment(GgufManifest m, string name, int start, int length, (int, int) → bytes ⇥ GgufManifestError source) → bytes ⇥ GgufManifestError`

## gradus:model/qwen35moe

Qwen35MoE frozen configuration, canonical tensor map, and admission checks.

**Source**: `src/model/qwen35moe.fab`

### Public types

- `union Qwen35moeConfigError` — DivergentMetadata
- `union Qwen35moeTensorError` — DivergentName, DivergentShape, DivergentStorage, DivergentCount
- `union Qwen35moeReferenceError` — UnknownName, DivergentDimension, DivergentCount, BadRange
- `union Qwen35moeAdmissionError` — DivergentIdentity, UnknownArchitecture, UnknownType, DivergentConfig, DivergentTensors, DivergentReference, BadManifest
- `class Qwen35moeConfig`
  - fields: string architecture, int file_type, int quantization_version, int block_count, int context_length, int embedding_length, int head_count, int head_count_kv, int key_length, int value_length, f32 rms_norm_epsilon, f32 freq_base, int rope_dimension_count, list<int> rope_sections, int expert_count, int expert_used_count, int expert_ffn_length, int shared_ffn_length, int conv_kernel, int state_size, int group_count, int gradus_temporis, int inner_size, int full_attention_interval, int nextn_predict_layers, string tokenizer_model, string tokenizer_pre, int token_count, int token_type_count, int merge_count, int eos_token_id, int padding_token_id, int bos_token_id, bool add_bos_token
- `class QwenTensorSummary`
  - fields: int total, int globals, int hybrid, int full_attention, int nextn, int storage_f32, int storage_q8_0, int storage_q4_k, int storage_q5_k, int storage_q6_k, int storage_bf16, int expert_rank3
- `class QwenCanonicalTensor`
  - fields: string name, list<int> shape, int dtype_ggml
- `class Qwen35moeAdmission`
  - fields: Qwen35moeConfig config, QwenTensorSummary summary

### Public functions

- `fn message(Qwen35moeConfigError e) → string`
- `fn freeze(gguf_manifest.GgufManifest m) → Qwen35moeConfig ⇥ Qwen35moeConfigError`
- `fn tensor_message(Qwen35moeTensorError e) → string`
- `fn canonical_tensors(gguf_manifest.GgufManifest m) → QwenTensorSummary ⇥ Qwen35moeTensorError`
- `fn reference_message(Qwen35moeReferenceError e) → string`
- `fn reference(Qwen35moeConfig c, gguf_manifest.GgufManifest m) → bool ⇥ Qwen35moeReferenceError`
- `fn admission_message(Qwen35moeAdmissionError e) → string`
- `fn admit(gguf_manifest.GgufCorpus corpus, string expected_digest, int expected_length) → Qwen35moeAdmission ⇥ Qwen35moeAdmissionError`

## gradus:model/moe

Carrier-tier mixture-of-experts routing, rank-3 expert dispatch, weighted
accumulation, and gated shared-expert FFN composition for the MODEL-02 surface.
The adapter owns bounded tensor windows and fails closed on malformed carriers,
windows, configuration, and non-finite values. Routed experts are accumulated
in ascending expert-index order for deterministic f32 results.

**Source**: `src/model/moe.fab`

### Public types

- `union MoeError` — BadConfig, BadShape, BadWindow, NonFinite (each carries a `string message`)
- `class MoeConfig`
  - fields: int expert_count, int expert_used_count, int expert_ffn_length, int shared_ffn_length, int embedding_length
- `class MoeSelection`
  - fields: list<int> indices, list<f32> weights, list<f32> logits, list<f32> probabilities
  - methods:
    - `fn indices() → list<int>`
    - `fn weights() → list<f32>`
    - `fn logits() → list<f32>`
    - `fn probabilities() → list<f32>`

### Public functions

- `fn message(MoeError e) → string`
- `fn route(tensor.NumericBlock x, int layer, (string, int, int) → tensor.NumericBlock ⇥ MoeError source, MoeConfig cfg) → MoeSelection ⇥ MoeError`
- `fn expert_out(tensor.NumericBlock x, int layer, int expert_index, (string, int, int) → tensor.NumericBlock ⇥ MoeError source, MoeConfig cfg) → tensor.NumericBlock ⇥ MoeError`
- `fn ffn_moe(tensor.NumericBlock x, int layer, (string, int, int) → tensor.NumericBlock ⇥ MoeError source, MoeConfig cfg) → tensor.NumericBlock ⇥ MoeError`

## gradus:model/qwen35moe_state

Hybrid SSM/attention state and execution for the Qwen3.6 trunk (MODEL-03):
schedule derivation (linear attention iff `(i+1) % full_attention_interval ≠ 0`),
the three state families (depthwise conv window, Gated DeltaNet recurrent
cells, KV cache), session identity/reset/replay, NEOX RoPE, and per-layer
attention-subblock forward against admitted MODEL-01 config + tensors.
Scalar math is self-hosted (module-local exp/sigmoid/silu/softplus/log/
sin/cos/sqrt) so proba can pin it without host intrinsics.

**Source**: `src/model/qwen35moe_state.fab`

### Public types

- `union Qwen35moeStateError` — BadConfig, BadShape, BadWindow, BadSchedule, BadState, NonFinite (each carries a `string message`)
- `union LayerKind` — LinearAttention, FullAttention, Nextn
- `class Qwen35moeSchedule`
  - methods: `fn trunk_layers() → int`, `fn linear_layers() → int`, `fn full_layers() → int`, `fn nextn_layers() → int`, `fn kinds() → list<int>`
- `class ConvState`
  - fields: list<f32> channels, int kernel, int channels_count
- `class RecurrentState`
  - fields: list<f32> cells, int value_heads, int key_dim, int value_dim
- `class KeyValueState`
  - fields: list<f32> keys, list<f32> values, int kv_heads, int key_dim, int value_dim, int capacity, int length
- `class HybridSession`
  - fields: Qwen35moeSchedule schedule, list<ConvState> conv, list<RecurrentState> recurrent, list<KeyValueState> kv, int generation, string model, string model_version, string execution_config, string tokenizer, string state_types, string dtype
- `class LinearAttentionTrace`
  - fields: list<f32> normed, qkv_mixed, gate_proj, beta_sigmoid, gate, conv_input, conv_output, q_conv, k_conv, v_conv, core_out, final_output
- `class LinearAttentionOutcome`
  - fields: LinearAttentionTrace trace, list<f32> out, ConvState conv, RecurrentState recurrent
- `class FullAttentionTrace`
  - fields: list<f32> normed, q_full, q_normed, k_normed, gate, q_rope, k_rope, v, softmax, pregate, gated
- `class FullAttentionOutcome`
  - fields: FullAttentionTrace trace, list<f32> out, KeyValueState kv

### Public functions

- `fn state_message(Qwen35moeStateError e) → string`
- `fn schedule(qwen35moe.Qwen35moeConfig c) → Qwen35moeSchedule ⇥ Qwen35moeStateError`
- `fn layer_kind(Qwen35moeSchedule s, int block) → LayerKind ⇥ Qwen35moeStateError`
- `fn layer_kind_name(LayerKind k) → string`
- `fn layer_kind_eq(LayerKind a, LayerKind b) → bool`
- `fn is_trunk(Qwen35moeSchedule s, int block) → bool`
- `fn linear_index(Qwen35moeSchedule s, int block) → int ⇥ Qwen35moeStateError`
- `fn attention_index(Qwen35moeSchedule s, int block) → int ⇥ Qwen35moeStateError`
- `fn validate_schedule(gguf_manifest.GgufManifest m, Qwen35moeSchedule s, qwen35moe.Qwen35moeConfig c) → bool ⇥ Qwen35moeStateError`
- `fn fresh_conv_state(qwen35moe.Qwen35moeConfig c) → ConvState ⇥ Qwen35moeStateError`
- `fn fresh_recurrent_state(qwen35moe.Qwen35moeConfig c) → RecurrentState`
- `fn fresh_kv_state(qwen35moe.Qwen35moeConfig c, int capacity) → KeyValueState ⇥ Qwen35moeStateError`
- `fn conv_equal(ConvState a, ConvState b) → bool`
- `fn recurrent_equal(RecurrentState a, RecurrentState b) → bool`
- `fn kv_equal(KeyValueState a, KeyValueState b) → bool`
- `fn fresh_session(qwen35moe.Qwen35moeConfig c) → HybridSession ⇥ Qwen35moeStateError`
- `fn reset_session(HybridSession s) → HybridSession`
- `fn session_state_equal(HybridSession a, HybridSession b) → bool`
- `fn session_identity_key(HybridSession s) → string`
- `fn deserialize_session_identity(string wire) → HybridSession ⇥ Qwen35moeStateError`
- `fn rope_head(list<f32> head, int dims, int pairs, f32 base, list<int> sections, int pos, int pass_through) → list<f32> ⇥ Qwen35moeStateError`
- `fn recurrent_update(RecurrentState s, list<f32> q, list<f32> k, list<f32> v, f32 g, f32 beta, int head) → RecurrentState ⇥ Qwen35moeStateError`
- `fn recurrent_output(RecurrentState s, list<f32> q, int head) → list<f32> ⇥ Qwen35moeStateError`
- `fn linear_attention(list<f32> x_rows, int layer, ConvState conv_in, RecurrentState recurrent_in, (string, int, int) → tensor.NumericBlock ⇥ Qwen35moeStateError source, qwen35moe.Qwen35moeConfig c) → LinearAttentionOutcome ⇥ Qwen35moeStateError`
- `fn linear_attention_step(list<f32> x_row, int layer, ConvState conv_in, RecurrentState recurrent_in, (string, int, int) → tensor.NumericBlock ⇥ Qwen35moeStateError source, qwen35moe.Qwen35moeConfig c) → LinearAttentionOutcome ⇥ Qwen35moeStateError`
- `fn full_attention(list<f32> x_rows, int layer, KeyValueState kv_in, int start_pos, (string, int, int) → tensor.NumericBlock ⇥ Qwen35moeStateError source, qwen35moe.Qwen35moeConfig c) → FullAttentionOutcome ⇥ Qwen35moeStateError`
- `fn full_attention_step(list<f32> x_row, int layer, KeyValueState kv_in, int pos, (string, int, int) → tensor.NumericBlock ⇥ Qwen35moeStateError source, qwen35moe.Qwen35moeConfig c) → FullAttentionOutcome ⇥ Qwen35moeStateError`

## gradus:model/safetensors

Safetensors header parsing and row admission into the typed model capsule.

**Source**: `src/model/safetensors.fab`

### Public types

- `union SafetensorError` — BadFormat, UnknownVersion, BadArchitecture, UnknownDtype, BadOffset, BadShape, BadTokenizer, BadBounds, BadDigest, BadMetadata, BadAdmission
- `class Token`
  - fields: int kind, string payload
- `class Structure`
  - fields: list<string> meta_keys, list<string> meta_values, list<string> names, list<string> dtypes, list<list<int>> shapes, list<int> starts, list<int> end
- `class StringValue`
  - fields: int pos, string payload
- `class MetadataCursor`
  - fields: int pos, list<string> keys, list<string> values
- `class TensorCursor`
  - fields: int pos, string dtype, list<int> shape, int start, int end
- `class NumberCursor`
  - fields: int pos, list<int> values
- `class HeaderCursor`
  - fields: int header, string text

### Public functions

- `fn message(SafetensorError e) → string`
- `fn admit(list<int<u8>> corpus, string digest, string path) → capsule.Capsule ⇥ SafetensorError`

## gradus:model/tensor_payload

Pathless tensor payload carrier with bounded byte ranges.

**Source**: `src/model/tensor_payload.fab`

### Public types

- `union PayloadError` — UnknownName, BadRange, BadLength
- `class TensorPayload`
  - fields: string name, int absolute_start, int length, bytes bytes

### Public functions

- `fn message(PayloadError e) → string`

## gradus:model/tensor_view

Bounded typed views over tensor payloads and materialization windows.

**Source**: `src/model/tensor_view.fab`

### Public types

- `union ViewError` — UnknownName, BadRange, BadLength, UnknownLayout, UnknownDtype, BadOrder, BadBounds
- `class TensorView`
  - fields: string name, list<int> shape, int dtype_ggml, int elements, gguf_manifest.GgmlLayout layout, int absolute_start, int payload_length

### Public functions

- `fn message(ViewError e) → string`
- `fn links(gguf_manifest.GgufManifest m, tensor_payload.TensorPayload p) → TensorView ⇥ ViewError`
- `fn materialize_slice(TensorView v, int element_start, int element_length, (int, int) → bytes ⇥ gguf_manifest.GgufManifestError source) → list<f32> ⇥ ViewError`
- `fn materialize_block(TensorView v, int block_index, (int, int) → bytes ⇥ gguf_manifest.GgufManifestError source) → list<f32> ⇥ ViewError`

## gradus:nn

Differentiable tensor primitives: linear, GELU, LayerNorm, RMSNorm, SiLU, and SwiGLU.

**Source**: `src/nn.fab`

### Public types

- `union NnError` — NegativeDimension, DimensionAboveLimit, ProductAboveLimit, GradusMismatch, ShapeMismatch, Incompatible, DtypeMismatch, ElementMismatch, InvalidEpsilon

### Public functions

- `fn linear_2x8(tensor<f32, [2, 8]> input, tensor<f32, [8, 8]> weight, tensor<f32, [8]> bias) → tensor<f32, [2, 8]>`
- `fn layernorm_2x8(tensor<f32, [2, 8]> x, tensor<f32, [8]> scale, tensor<f32, [8]> offset) → tensor<f32, [2, 8]>`
- `fn message(NnError e) → string`
- `fn linear<size M, size K, size N>(tensor<f32, [M, K]> x, tensor<f32, [K, N]> w, tensor<f32, [M, N]> b) → tensor<f32, [M, N]>`
- `fn gelu<size M, size N>(tensor<f32, [M, N]> x) → tensor<f32, [M, N]>`
- `fn linear_carrier(tensor.NumericBlock x, tensor.NumericBlock w, tensor.NumericBlock b) → tensor.NumericBlock ⇥ NnError`
- `fn gelu(tensor.NumericBlock x) → tensor.NumericBlock ⇥ NnError`
- `fn layernorm(tensor.NumericBlock x, tensor.NumericBlock scale, tensor.NumericBlock offset, f32 epsilon) → tensor.NumericBlock ⇥ NnError`
- `fn rmsnorm(tensor.NumericBlock x, tensor.NumericBlock scale, f32 epsilon) → tensor.NumericBlock ⇥ NnError`
- `fn silu(tensor.NumericBlock x) → tensor.NumericBlock ⇥ NnError`
- `fn swiglu(tensor.NumericBlock gate, tensor.NumericBlock up, tensor.NumericBlock down_weight, tensor.NumericBlock down_bias) → tensor.NumericBlock ⇥ NnError`

## gradus:optimize

SGD state, optimizer slots, updates, schedules, and optimizer serialization.

**Source**: `src/optimize.fab`

### Public types

- `union OptimizeError` — EmptyName, InvalidVersion, InvalidGeneration, InvalidStep, InvalidRate, IdentityMismatch, StaleGradient, Frozen, ShapeMismatch, Mutation, DuplicateName, UnknownName, UnknownVersion, BadWire
- `class SgdState`
  - fields: string owner, string name, int version, int generation, int step, f32 rate
  - methods:
    - `fn owner() → string`
    - `fn name() → string`
    - `fn version() → int`
    - `fn generation() → int`
    - `fn step() → int`
    - `fn rate() → f32`
- `class Sgd`
  - fields: list<SgdState> states
  - methods:
    - `fn count() → int`
    - `fn contains(string owner, string name) → bool`
    - `fn find(string owner, string name) → SgdState ⇥ OptimizeError`
- `class StepResult`
  - fields: parameter.Parameter fresh, SgdState state
  - methods:
    - `fn fresh() → parameter.Parameter`
    - `fn state() → SgdState`

### Public functions

- `fn message(OptimizeError e) → string`
- `fn state_equal(SgdState a, SgdState b) → bool`
- `fn default() → SgdState`
- `fn construct(string name, string owner, int generation, f32 rate) → SgdState ⇥ OptimizeError`
- `fn sgd_equal(Sgd a, Sgd b) → bool`
- `fn empty_sgd() → Sgd`
- `fn default_sgd() → Sgd`
- `fn add(Sgd o, SgdState s) → Sgd ⇥ OptimizeError`
- `fn default_step() → StepResult`
- `fn step(SgdState s, parameter.Parameter p, gradient.Gradient g) → StepResult ⇥ OptimizeError`
- `fn serialize_state(SgdState s) → string`
- `fn deserialize_state(string wire) → SgdState ⇥ OptimizeError`
- `fn serialize(Sgd o) → string`
- `fn deserialize(string wire) → Sgd ⇥ OptimizeError`

## gradus:parameter

Parameter identity, trainable/frozen status, mutation, registry traversal, and identity wire forms.

**Source**: `src/parameter.fab`

### Public types

- `union Station` — Trainable, Frozen
- `union ParameterError` — EmptyName, ReservedName, UnknownDtype, InvalidShape, ElementMismatch, FrozenMutation, DuplicateName, UnknownName, InvalidVersion, BadWire
- `class Identity`
  - fields: string name, dtype.DType dtype, list<int> shape, int version, string owner
  - methods:
    - `fn name() → string`
    - `fn dtype_name() → string`
    - `fn shape() → list<int>`
    - `fn version() → int`
    - `fn owner() → string`
- `class Parameter`
  - fields: Identity identity, Station status, tensor.NumericBlock payload
  - methods:
    - `fn identity() → Identity`
    - `fn status() → Station`
    - `fn name() → string`
    - `fn dtype_name() → string`
    - `fn shape() → list<int>`
    - `fn version() → int`
    - `fn owner() → string`
    - `fn numel() → int`
    - `fn payload() → tensor.NumericBlock`
- `class Registry`
  - fields: list<Parameter> parameters
  - methods:
    - `fn count() → int`
    - `fn contains(string owner, string name) → bool`
    - `fn find(string owner, string name) → Parameter ⇥ ParameterError`
    - `fn trainable() → list<Parameter>`
    - `fn frozen() → list<Parameter>`
    - `fn order() → list<Parameter>`

### Public functions

- `fn status_name(Station s) → string`
- `fn message(ParameterError e) → string`
- `fn identity_equal(Identity a, Identity b) → bool`
- `fn is_trainable(Parameter p) → bool`
- `fn is_frozen(Parameter p) → bool`
- `fn default() → Parameter`
- `fn construct(string name, string owner, string dtype_name, list<int> shape, list<f32> data) → Parameter ⇥ ParameterError`
- `fn construct_frozen(string name, string owner, string dtype_name, list<int> shape, list<f32> data) → Parameter ⇥ ParameterError`
- `fn mutate(Parameter p, list<f32> data) → Parameter ⇥ ParameterError`
- `fn empty_registry() → Registry`
- `fn add(Registry r, Parameter p) → Registry ⇥ ParameterError`
- `fn serialize(Identity i) → string`
- `fn deserialize(string s) → Identity ⇥ ParameterError`

## gradus:sampling

Deterministic greedy/filtering/sampling pipeline and sampler configuration.

**Source**: `src/sampling.fab`

### Public types

- `union SamplingError` — InvalidLogits, InvalidConfig, InvalidHistory
- `class Config`
  - fields: f32 temperature, int top_k, f32 top_p, f32 min_p, f32 repetition_penalty
  - methods:
    - `fn temperature() → f32`
    - `fn top_k() → int`
    - `fn top_p() → f32`
    - `fn min_p() → f32`
    - `fn repetition_penalty() → f32`
- `class Sampler`
  - fields: int token_id, train.Seed seed
  - methods:
    - `fn token_id() → int`
    - `fn seed() → train.Seed`

### Public functions

- `fn message(SamplingError e) → string`
- `fn construct_config(f32 temperature, int top_k, f32 top_p, f32 min_p, f32 repetition_penalty) → Config ⇥ SamplingError`
- `fn default_config() → Config`
- `fn default() → Sampler`
- `fn max(list<f32> logits) → int ⇥ SamplingError`
- `fn distribution(list<f32> logits, Config c, list<int> history) → list<f32> ⇥ SamplingError`
- `fn sample(list<f32> logits, Config c, list<int> history, train.Seed seed) → Sampler ⇥ SamplingError`

## gradus:serialize

Versioned byte serialization for dtype, shape, tensor, and parameter values.

**Source**: `src/serialize.fab`

### Public types

- `union SerializeError` — UnknownVersion, UnknownKind, UnknownDtype, BadShape, BadWire, BadData
- `class SerializedTensor`
  - fields: string dtype_name, list<int> shape, list<f32> data
  - methods:
    - `fn dtype() → string`
    - `fn shape() → list<int>`
    - `fn data() → list<f32>`
- `class ParameterWire`
  - fields: string name, string owner, string dtype_name, list<int> shape, int version, string status_name, list<f32> data
  - methods:
    - `fn name() → string`
    - `fn owner() → string`
    - `fn dtype() → string`
    - `fn shape() → list<int>`
    - `fn version() → int`
    - `fn status() → string`
    - `fn data() → list<f32>`

### Public functions

- `fn message(SerializeError e) → string`
- `fn serialize_dtype(string dtype_name) → bytes ⇥ SerializeError`
- `fn serialize_shape(list<int> shape) → bytes ⇥ SerializeError`
- `fn serialize_tensor(list<f32> data, list<int> shape, string dtype_name) → bytes ⇥ SerializeError`
- `fn serialize_parameter(string name, string owner, string dtype_name, list<int> shape, int version, string status_name, list<f32> data) → bytes ⇥ SerializeError`
- `fn deserialize_dtype(bytes wire) → string ⇥ SerializeError`
- `fn deserialize_shape(bytes wire) → list<int> ⇥ SerializeError`
- `fn deserialize_tensor(bytes wire) → SerializedTensor ⇥ SerializeError`
- `fn deserialize_parameter(bytes wire) → ParameterWire ⇥ SerializeError`

## gradus:shape

Runtime shape validation, rank, bounded element counts, broadcasting, reshape, and expansion.

**Source**: `src/shape.fab`

### Public types

- `union ShapeError` — NegativeDimension, DimensionAboveLimit, ProductAboveLimit, Incompatible, ElementMismatch, GradusMismatch

### Public functions

- `fn message(ShapeError e) → string`
- `fn valid(list<int> shape) → bool`
- `fn rank(list<int> shape) → int`
- `fn numel(list<int> shape) → int ⇥ ShapeError`
- `fn broadcast(list<int> a, list<int> b) → list<int> ⇥ ShapeError`
- `fn reshape(list<int> shape, list<int> target) → list<int> ⇥ ShapeError`
- `fn expand(list<int> shape, int target_rank) → list<int> ⇥ ShapeError`

## gradus:tensor

The staged tensor carrier with runtime shape/dtype/data validation and indexed access.

**Source**: `src/tensor.fab`

### Public types

- `union TensorError` — InvalidShape, ElementMismatch, IndexOutOfBounds
- `class NumericBlock`
  - fields: dtype.DType dtype, list<int> shape, list<f32> data, int numel, list<int> strides (stride/count cache, computed at construction — W0)
  - methods:
    - `fn shape() → list<int>`
    - `fn rank() → int`
    - `fn numel() → int`
    - `fn dtype() → dtype.DType`
    - `fn valid() → bool`
    - `fn get(list<int> indices) → f32 ⇥ TensorError`

### Public functions

- `fn message(TensorError e) → string`
- `fn default() → NumericBlock`
- `fn construct(list<f32> data, list<int> shape) → NumericBlock ⇥ TensorError`
- `fn construct_dtype(list<f32> data, list<int> shape, dtype.DType dtype) → NumericBlock ⇥ TensorError`
- `fn fill(list<int> shape, f32 payload) → NumericBlock ⇥ TensorError`
- `fn stage(dtype.DType dtype, list<int> shape, list<f32> data) → NumericBlock` (trusted-input staging — W0; no validation, library-internal producers only)

## gradus:tokenizer

Tokenizer identity, pinned probes, artifact-backed encoding/decoding, Unicode categories, and chat rendering.

**Source**: `src/tokenizer.fab`

### Public types

- `union TokenizerError` — UnknownVersion, UnknownMergeKind, UnknownPreTokenizer, BadVocab, BadDigest, BadEog, IdExtra, ProbeDivergent, BadArtifact, BadMerges, UnknownId, UnknownTrace, BadUtf8, BadWire
- `union UnicodeCategory` — Letter, Signum, Number, Space, Newline, Other
- `class TokenizerIdentity`
  - fields: string schema, string merge_kind, string pre_tokenizer, string vocab_digest, string eog, bool bos_free, bool space_free
  - methods:
    - `fn schema() → string`
    - `fn merge_kind() → string`
    - `fn pre_tokenizer() → string`
    - `fn vocab_digest() → string`
    - `fn eog() → string`
    - `fn bos_free() → bool`
    - `fn space_free() → bool`
- `class Tokenizer`
  - fields: list<string> words, map<string, int> vocab, map<string, int> concursus, list<string> special_texts, list<int> specialia_ids, list<int> eog, bool add_bos, string chat_template, int multitudo

### Public functions

- `fn is_eog(int id) → bool`
- `fn message(TokenizerError e) → string`
- `fn probe_equal(list<int> a, list<int> b) → bool`
- `fn probe_id(string pinned) → list<int> ⇥ TokenizerError`
- `fn verify_probe(string name, list<int> observed) → bool ⇥ TokenizerError`
- `fn pinned_probe(string name) → string ⇥ TokenizerError`
- `fn construct(string schema, string merge_kind, string pre_tokenizer, string vocab_digest, string eog, bool bos_free, bool space_free) → TokenizerIdentity ⇥ TokenizerError`
- `fn verify(TokenizerIdentity t) → bool ⇥ TokenizerError`
- `fn tokenizer_key(TokenizerIdentity t) → string ⇥ TokenizerError`
- `fn serialize_identity(TokenizerIdentity t) → string ⇥ TokenizerError`
- `fn deserialize_identity(string wire) → TokenizerIdentity ⇥ TokenizerError`
- `fn build(gguf_manifest.GgufManifest m) → Tokenizer ⇥ TokenizerError`
- `fn build_tables(list<int> ids, list<string> tokens, list<string> merges, list<int> special_ids) → Tokenizer ⇥ TokenizerError`
- `fn encode(Tokenizer t, string word) → list<int> ⇥ TokenizerError`
- `fn decode(Tokenizer t, list<int> ids) → string ⇥ TokenizerError`
- `fn category(string c) → UnicodeCategory`
- `fn is_letter(string c) → bool`
- `fn is_symbol(string c) → bool`
- `fn is_number(string c) → bool`
- `fn is_space(string c) → bool`
- `fn is_newline(string c) → bool`
- `fn is_other(string c) → bool`
- `fn category_name(string c) → string`
- `fn scan_words(string text) → list<string> ⇥ TokenizerError`
- `fn scan_smollm(string text) → list<string> ⇥ TokenizerError`
- `fn encode_prompt(Tokenizer t, string text) → list<int> ⇥ TokenizerError`
- `fn encode_prompt_special(Tokenizer t, string text) → list<int> ⇥ TokenizerError`
- `fn tokenize(Tokenizer t, string text) → list<int> ⇥ TokenizerError`
- `fn tokenize_literal(Tokenizer t, string text) → list<int> ⇥ TokenizerError`
- `fn artifact_eog(Tokenizer t) → list<int>`
- `fn is_artifact_eog(Tokenizer t, int id) → bool`
- `fn add_bos(Tokenizer t) → bool`
- `fn chat_template(Tokenizer t) → string`
- `fn render_user_turn(Tokenizer t, string content) → string ⇥ TokenizerError`

## gradus:train

Training steps, learning-rate schedules, modes, RNG, dropout, and checkpoints.

**Source**: `src/train.fab`

### Public types

- `union TrainError` — InvalidSchedule, UnknownMode, InvalidDropout, NegativeStep, InvalidSeed, BadPayload, InvalidPosition, EmptyState, UnknownVersion, BadWire
- `union Mode` — Discipline, Estimate
- `class Schedule`
  - fields: f32 rate_vertex, int warmup, int total_steps, f32 rate_end
  - methods:
    - `fn rate_vertex() → f32`
    - `fn warmup() → int`
    - `fn total_steps() → int`
    - `fn rate_end() → f32`
- `class Seed`
  - fields: int status
  - methods:
    - `fn status() → int`
- `class Draw`
  - fields: int payload, Seed seed
  - methods:
    - `fn payload() → int`
    - `fn seed() → Seed`
- `class DrawF32`
  - fields: f32 payload, Seed seed
  - methods:
    - `fn payload() → f32`
    - `fn seed() → Seed`
- `class Dropout`
  - fields: tensor.NumericBlock payload, Seed seed
  - methods:
    - `fn payload() → tensor.NumericBlock`
    - `fn seed() → Seed`
- `class Checkpoint`
  - fields: int age, int step, Seed rng, string state_wire
  - methods:
    - `fn age() → int`
    - `fn step() → int`
    - `fn rng() → Seed`
    - `fn state_wire() → string`

### Public functions

- `fn train_step_2x2(tensor<f32, [2, 2]> weight, tensor<f32, [2, 2]> bias, tensor<f32, [2, 2]> grad_weight, tensor<f32, [2, 2]> grad_bias, f32 lr) → tuple<tensor<f32, [2, 2]>, tensor<f32, [2, 2]>>`
- `fn train_step_4x4(tensor<f32, [4, 4]> weight1, tensor<f32, [4, 4]> bias1, tensor<f32, [4, 4]> weight2, tensor<f32, [4, 4]> bias2, tensor<f32, [4, 4]> grad_weight1, tensor<f32, [4, 4]> grad_bias1, tensor<f32, [4, 4]> grad_weight2, tensor<f32, [4, 4]> grad_bias2, f32 lr) → tuple<tensor<f32, [4, 4]>, tensor<f32, [4, 4]>, tensor<f32, [4, 4]>, tensor<f32, [4, 4]>>`
- `fn train_step_bert_linear(tensor<f32, [8, 8]> wq, tensor<f32, [8]> bq, tensor<f32, [8, 8]> wk, tensor<f32, [8]> bk, tensor<f32, [8, 8]> wv, tensor<f32, [8]> bv, tensor<f32, [8, 8]> wo, tensor<f32, [8]> bo, tensor<f32, [8, 8]> wf1, tensor<f32, [8]> bf1, tensor<f32, [8, 8]> wf2, tensor<f32, [8]> bf2, tensor<f32, [8, 8]> gwq, tensor<f32, [8]> gbq, tensor<f32, [8, 8]> gwk, tensor<f32, [8]> gbk, tensor<f32, [8, 8]> gwv, tensor<f32, [8]> gbv, tensor<f32, [8, 8]> gwo, tensor<f32, [8]> gbo, tensor<f32, [8, 8]> gwf1, tensor<f32, [8]> gbf1, tensor<f32, [8, 8]> gwf2, tensor<f32, [8]> gbf2, f32 lr) → tuple<tensor<f32, [8, 8]>, tensor<f32, [8]>, tensor<f32, [8, 8]>, tensor<f32, [8]>, tensor<f32, [8, 8]>, tensor<f32, [8]>, tensor<f32, [8, 8]>, tensor<f32, [8]>, tensor<f32, [8, 8]>, tensor<f32, [8]>, tensor<f32, [8, 8]>, tensor<f32, [8]>>`
- `fn train_step_bert_layernorm(tensor<f32, [8]> ln1_s, tensor<f32, [8]> ln1_o, tensor<f32, [8]> ln2_s, tensor<f32, [8]> ln2_o, tensor<f32, [8]> ln3_s, tensor<f32, [8]> ln3_o, tensor<f32, [8]> gln1_s, tensor<f32, [8]> gln1_o, tensor<f32, [8]> gln2_s, tensor<f32, [8]> gln2_o, tensor<f32, [8]> gln3_s, tensor<f32, [8]> gln3_o, f32 lr) → tuple<tensor<f32, [8]>, tensor<f32, [8]>, tensor<f32, [8]>, tensor<f32, [8]>, tensor<f32, [8]>, tensor<f32, [8]>>`
- `fn message(TrainError e) → string`
- `fn construct_schedule(f32 rate_vertex, int warmup, int total_steps, f32 rate_end) → Schedule ⇥ TrainError`
- `fn default_schedule() → Schedule`
- `fn scheduled_rate(Schedule s, int step) → f32 ⇥ TrainError`
- `fn mode_name(Mode m) → string`
- `fn is_discipline(Mode m) → bool`
- `fn is_estimate(Mode m) → bool`
- `fn mode(string name) → Mode ⇥ TrainError`
- `fn dropout_probability(Mode m, f32 rate) → f32 ⇥ TrainError`
- `fn construct_seed(int seed) → Seed ⇥ TrainError`
- `fn default() → Seed`
- `fn next(Seed s) → Draw`
- `fn next_f32(Seed s) → DrawF32`
- `fn dropout(tensor.NumericBlock x, Seed s, Mode m, f32 rate) → Dropout ⇥ TrainError`
- `fn serialize_seed(Seed s) → string`
- `fn deserialize_seed(string wire) → Seed ⇥ TrainError`
- `fn construct_checkpoint(int age, int step, Seed rng, string state_wire) → Checkpoint ⇥ TrainError`
- `fn default_checkpoint() → Checkpoint`
- `fn checkpoint_equal(Checkpoint a, Checkpoint b) → bool`
- `fn serialize_checkpoint(Checkpoint c) → string`
- `fn deserialize_checkpoint(string wire) → Checkpoint ⇥ TrainError`

## gradus:transformer

Fixed-shape and runtime-carrier transformer blocks, including cached block evaluation.

**Source**: `src/transformer.fab`

### Public types

- `union TransformerError` — NegativeDimension, DimensionAboveLimit, ProductAboveLimit, GradusMismatch, ShapeMismatch, Incompatible, DtypeMismatch, ElementMismatch, EpsilonInvalida, InvalidPosition, InvalidDimension, InvalidMode
- `class DenseAttentionWeights`
  - fields: tensor.NumericBlock wq, tensor.NumericBlock bq, tensor.NumericBlock wk, tensor.NumericBlock bk, tensor.NumericBlock wv, tensor.NumericBlock bv, tensor.NumericBlock wo
- `class DenseAttentionConfig`
  - fields: int num_heads, int num_kv_heads, f32 scale, int rope_dim, attention.RopeConfig rope_config
- `class DenseMlpWeights`
  - fields: tensor.NumericBlock wg, tensor.NumericBlock bg, tensor.NumericBlock wu, tensor.NumericBlock bu, tensor.NumericBlock wd, tensor.NumericBlock bd
- `class DenseNormConfig`
  - fields: tensor.NumericBlock ln1_s, tensor.NumericBlock ln2_s, f32 epsilon
- `class CachedBlock`
  - fields: tensor.NumericBlock output, kv.KVCache state
  - methods:
    - `fn output() → tensor.NumericBlock`
    - `fn state() → kv.KVCache`

### Public functions

- `fn bert_tiny_block_2x8(tensor<f32, [2, 8]> x, tensor<f32, [8]> ln1_s, tensor<f32, [8]> ln1_o, tensor<f32, [8, 8]> wq, tensor<f32, [8]> bq, tensor<f32, [8, 8]> wk, tensor<f32, [8]> bk, tensor<f32, [8, 8]> wv, tensor<f32, [8]> bv, tensor<f32, [8, 8]> wo, tensor<f32, [8]> bo, tensor<f32, [8]> ln2_s, tensor<f32, [8]> ln2_o, tensor<f32, [8, 8]> wf1, tensor<f32, [8]> bf1, tensor<f32, [8, 8]> wf2, tensor<f32, [8]> bf2, tensor<f32, [8]> ln3_s, tensor<f32, [8]> ln3_o, tensor<f32, [2, 2]> scale) → tensor<f32, [2, 8]>`
- `fn message(TransformerError e) → string`
- `fn transformer_block(tensor.NumericBlock x, tensor.NumericBlock ln1_s, tensor.NumericBlock ln1_o, tensor.NumericBlock wq, tensor.NumericBlock bq, tensor.NumericBlock wk, tensor.NumericBlock bk, tensor.NumericBlock wv, tensor.NumericBlock bv, tensor.NumericBlock wo, tensor.NumericBlock bo, tensor.NumericBlock ln2_s, tensor.NumericBlock ln2_o, tensor.NumericBlock wf1, tensor.NumericBlock bf1, tensor.NumericBlock wf2, tensor.NumericBlock bf2, tensor.NumericBlock ln3_s, tensor.NumericBlock ln3_o, f32 scale, int mode, list<int> positions, int dim) → tensor.NumericBlock ⇥ TransformerError`
- `fn dense_block(tensor.NumericBlock x, list<int> positions, DenseAttentionWeights attention_weights, DenseAttentionConfig attention_config, DenseMlpWeights mlp_weights, DenseNormConfig norm_config) → tensor.NumericBlock ⇥ TransformerError`
- `fn default_cached_block() → CachedBlock`
- `fn transformer_block_cached(tensor.NumericBlock x, tensor.NumericBlock ln1_s, tensor.NumericBlock ln1_o, tensor.NumericBlock wq, tensor.NumericBlock bq, tensor.NumericBlock wk, tensor.NumericBlock bk, tensor.NumericBlock wv, tensor.NumericBlock bv, tensor.NumericBlock wo, tensor.NumericBlock bo, tensor.NumericBlock ln2_s, tensor.NumericBlock ln2_o, tensor.NumericBlock wf1, tensor.NumericBlock bf1, tensor.NumericBlock wf2, tensor.NumericBlock bf2, tensor.NumericBlock ln3_s, tensor.NumericBlock ln3_o, f32 scale, list<int> positions, int dim, kv.KVCache layer, list<int> tokens) → CachedBlock ⇥ TransformerError`
- `fn dense_block_cached(tensor.NumericBlock x, list<int> positions, kv.KVCache layer, list<int> tokens, DenseAttentionWeights attention_weights, DenseAttentionConfig attention_config, DenseMlpWeights mlp_weights, DenseNormConfig norm_config) → CachedBlock ⇥ TransformerError`

## gradus:test_util

Shared proba-support helpers (U4a quality wave — proba do/catch deblock).

**Source**: `src/test_util.fab`

### Public functions

- `fn or_default<T, E>(() → T ⇥ E work, T fallback) → T` — run a failable call and fall back to a default on error; Theme-Z1 proba blocks (`do { t ← f() } catch { return t }`) collapse to one call

---

## Inventory gate

```bash
./scripta/inventory-public-symbols
```

The inventory gate re-counts every live declaration and checks that every non-private public function name occurs in the corresponding `## gradus:<module>` section. Per-module count re-baseline is a separate enforcement-gate unit. Coverage of the names above is the documentation contract.

**Live declaration total** (grep `fn ` across `src/**/*.fab`): `979`. Public coverage is by name, not by the raw declaration count (class methods, `_` helpers, and comment matches are included in the grep total).
