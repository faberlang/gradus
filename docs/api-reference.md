# Gradus API Reference

**Surface**: final post-S2 English identifier surface, generated from the live `src/**/*.fab` tree.
**Scope**: public Gradus module declarations and their public class methods. Import coordinates remain `gradus:*`.
**Authority**: `scripta/inventory-public-symbols` checks the live `fn` inventory and verifies every public function name below is documented in its module section.

This reference intentionally reports declarations from the live source rather than carrying a pre-S2 name map. Private `_`-prefixed helpers are omitted from the public lists. Parameters, comments, diagnostic strings, wire literals, and import coordinates remain whatever the live source declares.

---

## gradus:attention

Scaled dot-product attention, causal masking, RoPE configuration, and multi-head attention.

**Source**: `src/attention.fab`

### Public types

- `union AttentionError` — DimensioNegativa, DimensioSupraLimitem, ProductumSupraLimitem, GradusMismatch, FormaMismatch, Incompatibilis, TypoMismatch, ElementaMismatch, PositioInvalida, DimensioInvalida, ConfiguraInvalida
- `union RopePolicy` — Consecutiva, Interposita
- `class RopeConfig`
  - fields: `f32 base`, `f32 scale`, `RopePolicy policy`
  - methods:
    - `fn base() → f32 {`
    - `fn scale() → f32 {`
    - `fn policy() → RopePolicy {`

### Public functions

- `fn scaled_dot_product_2x8(tensor<f32, [2, 8]> qb, tensor<f32, [2, 8]> kb, tensor<f32, [2, 8]> vb, tensor<f32, [2, 2]> scale) → tensor<f32, [2, 8]> {`
- `fn message(AttentionError e) → string {`
- `fn consecutive_policy() → RopePolicy {`
- `fn interleaved_policy() → RopePolicy {`
- `fn policy_name(RopePolicy p) → string {`
- `fn construct_rope_config(f32 base, f32 scale, RopePolicy policy) → RopeConfig ⇥ AttentionError {`
- `fn rotary_position_embedding(tensor.Tensor x, list<int> positions, int dim) → tensor.Tensor ⇥ AttentionError {`
- `fn rotary_position_embedding_config(tensor.Tensor x, list<int> positions, int dim, RopeConfig configura) → tensor.Tensor ⇥ AttentionError {`
- `fn scaled_dot_product(tensor.Tensor q, tensor.Tensor k, tensor.Tensor v, f32 scale) → tensor.Tensor ⇥ AttentionError {`
- `fn scaled_dot_product_causal(tensor.Tensor q, tensor.Tensor k, tensor.Tensor v, f32 scale) → tensor.Tensor ⇥ AttentionError {`
- `fn scaled_dot_product_causal_rope(tensor.Tensor q, tensor.Tensor k, tensor.Tensor v, f32 scale, list<int> positions, int dim) → tensor.Tensor ⇥ AttentionError {`
- `fn multi_head_attention(tensor.Tensor q, tensor.Tensor k, tensor.Tensor v, tensor.Tensor wo, int num_heads, int num_kv_heads, f32 scale, list<int> positions, int rope_dim, RopeConfig rope_configura) → tensor.Tensor ⇥ AttentionError {`


## gradus:cache

KV-cache values, mutation rules, cache identity, and identity serialization.

**Source**: `src/cache.fab`

### Public types

- `union CacheError` — NomenInane, IdExtra, FormaMismatch, TypoMismatch, DimensioInvalida, ElementaMismatch, VersioIgnota, WireMala
- `class KVCache`
  - fields: `string model`, `string model_version`, `string config`, `string tokenizer`, `list<int> history`, `int layers`, `string dtype`, `string layout`, `tensor.Tensor key`, `tensor.Tensor payload`, `int version`, `int dimension`
  - methods:
    - `fn model() → string {`
    - `fn model_version() → string {`
    - `fn config() → string {`
    - `fn tokenizer() → string {`
    - `fn history() → list<int> {`
    - `fn layers() → int {`
    - `fn dtype() → string {`
    - `fn layout() → string {`
    - `fn key() → tensor.Tensor {`
    - `fn payload() → tensor.Tensor {`
    - `fn version() → int {`
    - `fn dimension() → int {`
    - `fn length() → int {`
- `class CacheIdentity`
  - fields: `string model`, `string model_version`, `string config`, `string tokenizer`, `string history`, `string position`, `int layers`, `string dtype`, `string layout`
  - methods:
    - `fn model() → string {`
    - `fn model_version() → string {`
    - `fn config() → string {`
    - `fn tokenizer() → string {`
    - `fn history() → string {`
    - `fn position() → string {`
    - `fn layers() → int {`
    - `fn dtype() → string {`
    - `fn layout() → string {`

### Public functions

- `fn message(CacheError e) → string {`
- `fn cache_equal(KVCache a, KVCache b) → bool {`
- `fn empty_cache(string model, string model_version, string config, string tokenizer, int layers, int dimension) → KVCache ⇥ CacheError {`
- `fn append(KVCache c, int token_id, tensor.Tensor key, tensor.Tensor payload) → KVCache ⇥ CacheError {`
- `fn reset(KVCache c) → KVCache ⇥ CacheError {`
- `fn cache_identity_equal(CacheIdentity a, CacheIdentity b) → bool {`
- `fn cache_identity(KVCache c) → CacheIdentity {`
- `fn serialize_identity(CacheIdentity i) → string {`
- `fn deserialize_identity(string wire) → CacheIdentity ⇥ CacheError {`


## gradus:data

Reserved data-module import surface; no public functions are currently declared.

**Source**: `src/data.fab`

### Public functions

- None declared.


## gradus:decode

One-token decode, prefill, explicit sessions, cancellation, and replica-loop mechanics.

**Source**: `src/decode.fab`

### Public types

- `union DecodeError` — IdExtra, PositioInvalida, Terminus, DecodereInvalida, FormaMismatch, TypoMismatch, ElementaMismatch, Incompatibilis, DimensioInvalida, Cancelata, SamplingDefecta
- `class Weights`
  - fields: `tensor.Tensor ln1_s`, `tensor.Tensor ln1_o`, `tensor.Tensor wq`, `tensor.Tensor bq`, `tensor.Tensor wk`, `tensor.Tensor bk`, `tensor.Tensor wv`, `tensor.Tensor bv`, `tensor.Tensor wo`, `tensor.Tensor bo`, `tensor.Tensor ln2_s`, `tensor.Tensor ln2_o`, `tensor.Tensor wf1`, `tensor.Tensor bf1`, `tensor.Tensor wf2`, `tensor.Tensor bf2`, `tensor.Tensor ln3_s`, `tensor.Tensor ln3_o`
  - methods:
    - `fn ln1_s() → tensor.Tensor {`
    - `fn ln1_o() → tensor.Tensor {`
    - `fn wq() → tensor.Tensor {`
    - `fn bq() → tensor.Tensor {`
    - `fn wk() → tensor.Tensor {`
    - `fn bk() → tensor.Tensor {`
    - `fn wv() → tensor.Tensor {`
    - `fn bv() → tensor.Tensor {`
    - `fn wo() → tensor.Tensor {`
    - `fn bo() → tensor.Tensor {`
    - `fn ln2_s() → tensor.Tensor {`
    - `fn ln2_o() → tensor.Tensor {`
    - `fn wf1() → tensor.Tensor {`
    - `fn bf1() → tensor.Tensor {`
    - `fn wf2() → tensor.Tensor {`
    - `fn bf2() → tensor.Tensor {`
    - `fn ln3_s() → tensor.Tensor {`
    - `fn ln3_o() → tensor.Tensor {`
- `class Decoder`
  - fields: `tensor.Tensor table`, `Weights weights`, `tensor.Tensor projection`, `tensor.Tensor projectio_bias`, `f32 scale`, `int vocabulary`, `int context`, `int dimension`
  - methods:
    - `fn table() → tensor.Tensor {`
    - `fn weights() → Weights {`
    - `fn projection() → tensor.Tensor {`
    - `fn projectio_bias() → tensor.Tensor {`
    - `fn scale() → f32 {`
    - `fn vocabulary() → int {`
    - `fn context() → int {`
    - `fn dimension() → int {`
- `class Session`
  - fields: `int position`, `int context`
  - methods:
    - `fn position() → int {`
    - `fn context() → int {`
- `class Cancellation`
  - fields: `bool cancelled`
  - methods:
    - `fn cancelled() → bool {`

### Public functions

- `fn message(DecodeError e) → string {`
- `fn construct_weights(tensor.Tensor ln1_s, tensor.Tensor ln1_o, tensor.Tensor wq, tensor.Tensor bq, tensor.Tensor wk, tensor.Tensor bk, tensor.Tensor wv, tensor.Tensor bv, tensor.Tensor wo, tensor.Tensor bo, tensor.Tensor ln2_s, tensor.Tensor ln2_o, tensor.Tensor wf1, tensor.Tensor bf1, tensor.Tensor wf2, tensor.Tensor bf2, tensor.Tensor ln3_s, tensor.Tensor ln3_o) → Weights {`
- `fn construct_decoder(tensor.Tensor table, Weights weights, tensor.Tensor projection, tensor.Tensor projectio_bias, f32 scale, int vocabulary, int context, int dimension) → Decoder ⇥ DecodeError {`
- `fn decodere_datum(int token_id, int position, Decoder m) → tensor.Tensor ⇥ DecodeError {`
- `fn prefill(list<int> tokens, Decoder m) → tensor.Tensor ⇥ DecodeError {`
- `fn fresh_session(int context) → Session ⇥ DecodeError {`
- `fn advance(Session s) → Session ⇥ DecodeError {`
- `fn reset(Session s) → Session {`
- `fn fresh_cancellation() → Cancellation {`
- `fn cancellation_cancelled() → Cancellation {`
- `fn observe_cancellation(Cancellation c) → Cancellation ⇥ DecodeError {`
- `fn replica(list<list<f32>> logita, sampling.Config c, list<int> history, train.Seed seed, Cancellation cancelatum) → list<int> ⇥ DecodeError {`


## gradus:dtype

Dtype tags, promotion, narrowing, serialization, and finite/cast checks.

**Source**: `src/dtype.fab`

### Public types

- `union DType` — F32, F16, I32, U8
- `union DTypeError` — NomenIgnotum, VersioIgnota, NonFinita, Superfluitas

### Public functions

- `fn f32() → DType {`
- `fn f16() → DType {`
- `fn i32() → DType {`
- `fn u8() → DType {`
- `fn message(DTypeError e) → string {`
- `fn name(DType t) → string {`
- `fn from_name(string s) → DType ⇥ DTypeError {`
- `fn width(DType t) → int {`
- `fn serialize(DType t) → string {`
- `fn deserialize(string s) → DType ⇥ DTypeError {`
- `fn promote(DType a, DType b) → bool {`
- `fn narrow(DType a, DType b) → bool {`
- `fn finite(f32 x) → bool {`
- `fn cast(f32 valor, DType origo, DType scopum) → f32 ⇥ DTypeError {`


## gradus:generation

Generation configuration, sampling projection, serialized config, and cursor limits.

**Source**: `src/generation.fab`

### Public types

- `union GeneratioError` — ConfiguraInvalida, ElementaMismatch, TypoMismatch, Incompatibilis, VersioIgnota, WireMala, Terminus
- `class GenerationConfig`
  - fields: `int context`, `int max_prompt`, `int max_tokens`, `int seed`, `f32 temperature`, `int top_k`, `f32 top_p`, `f32 min_p`, `f32 repetition_penalty`
  - methods:
    - `fn context() → int {`
    - `fn max_prompt() → int {`
    - `fn max_tokens() → int {`
    - `fn seed() → int {`
    - `fn temperature() → f32 {`
    - `fn top_k() → int {`
    - `fn top_p() → f32 {`
    - `fn min_p() → f32 {`
    - `fn repetition_penalty() → f32 {`
- `class GenerationCursor`
  - fields: `decode.Session session`, `int emitted`
  - methods:
    - `fn session() → decode.Session {`
    - `fn emitted() → int {`

### Public functions

- `fn message(GeneratioError e) → string {`
- `fn generation_equal(GenerationConfig a, GenerationConfig b) → bool {`
- `fn construct_generation(int context, int max_prompt, int max_tokens, int seed, f32 temperature, int top_k, f32 top_p, f32 min_p, f32 repetition_penalty) → GenerationConfig ⇥ GeneratioError {`
- `fn generation_failure(int context, int max_prompt, int max_tokens, int seed) → GenerationConfig ⇥ GeneratioError {`
- `fn support_flags() → list<string> {`
- `fn admitted_features(string nomen) → bool {`
- `fn config(GenerationConfig g) → sampling.Config ⇥ GeneratioError {`
- `fn seed(GenerationConfig g) → train.Seed ⇥ GeneratioError {`
- `fn serialize_generation(GenerationConfig g) → string {`
- `fn deserialize_generation(string wire) → GenerationConfig ⇥ GeneratioError {`
- `fn fresh_cursor(GenerationConfig g) → GenerationCursor ⇥ GeneratioError {`
- `fn token_allowed(GenerationConfig g, GenerationCursor c) → bool {`
- `fn cursor_advance(GenerationConfig g, GenerationCursor c) → GenerationCursor ⇥ GeneratioError {`
- `fn cursor_reset(GenerationCursor c) → GenerationCursor {`


## gradus:gradient

Gradient records and the forward/companion gradient wrapper surface.

**Source**: `src/gradient.fab`

### Public types

- `union GradientError` — GradusIgnotum, GradusVersio
- `class Gradient`
  - fields: `string owner`, `string name`, `int version`, `tensor.Tensor payload`
  - methods:
    - `fn owner() → string {`
    - `fn name() → string {`
    - `fn version() → int {`
    - `fn payload() → tensor.Tensor {`
- `class Gradients`
  - fields: `list<Gradient> gradients`
  - methods:
    - `fn count() → int {`
    - `fn find(string owner, string name) → Gradient ⇥ GradientError {`

### Public functions

- `fn message(GradientError e) → string {`
- `fn construct(string name, string owner, int version, tensor.Tensor payload) → Gradient ⇥ GradientError {`
- `fn construct_gradients(list<Gradient> gradients) → Gradients {`
- `fn obsolete(Gradient g, int versio_currens) → bool {`
- `fn nil() → void {`
- `fn simple_loss(tensor<f32, [2, 2]> x, tensor<f32, [2, 2]> w) → f32 {`
- `fn gradientes_simple_loss(tensor<f32, [2, 2]> x, tensor<f32, [2, 2]> w, f32 upstream, string name, string owner, int version) → Gradients ⇥ GradientError {`


## gradus:gradus

Thin package facade for MLP forward and loss convenience functions.

**Source**: `src/gradus.fab`

### Public types

- `union GradusError` — DimensioNegativa, DimensioSupraLimitem, ProductumSupraLimitem, GradusMismatch, FormaMismatch, Incompatibilis, TypoMismatch, ElementaMismatch

### Public functions

- `fn message(GradusError e) → string {`
- `fn forward_mlp(tensor.Tensor x, tensor.Tensor w1, tensor.Tensor b1, tensor.Tensor w2, tensor.Tensor b2) → tensor.Tensor ⇥ GradusError {`
- `fn nil() → void {`
- `fn forward_mlp_loss(tensor<f32, [4, 4]> input, tensor<f32, [4, 4]> weight1, tensor<f32, [4, 4]> bias1, tensor<f32, [4, 4]> weight2, tensor<f32, [4, 4]> bias2, tensor<f32, [4, 4]> target) → f32 {`


## gradus:loss

Tensor loss functions and fixed-shape MSE rows.

**Source**: `src/loss.fab`

### Public types

- `union LossError` — DimensioNegativa, DimensioSupraLimitem, ProductumSupraLimitem, GradusMismatch, FormaMismatch, TypoMismatch, ElementaMismatch, Incompatibilis, NonFinita

### Public functions

- `fn message(LossError e) → string {`
- `fn mse(tensor.Tensor prediction, tensor.Tensor target) → f32 ⇥ LossError {`
- `fn cross_entropy(tensor.Tensor logits, tensor.Tensor target) → f32 ⇥ LossError {`
- `fn mse_2x2(tensor<f32, [2, 2]> prediction, tensor<f32, [2, 2]> target) → f32 {`
- `fn mse_4x4(tensor<f32, [4, 4]> prediction, tensor<f32, [4, 4]> target) → f32 {`
- `fn mse_2x8(tensor<f32, [2, 8]> prediction, tensor<f32, [2, 8]> target) → f32 {`


## gradus:math

Device-neutral tensor arithmetic, reductions, matrix multiplication, casts, concatenation, and slicing.

**Source**: `src/math.fab`

### Public types

- `union MathError` — DimensioNegativa, DimensioSupraLimitem, ProductumSupraLimitem, FormaMismatch, GradusMismatch, Incompatibilis, TypoMismatch, ElementMismatch, NonFinita, Superfluitas, NomenIgnotum

### Public functions

- `fn message(MathError e) → string {`
- `fn construct(list<f32> datos, list<int> forma) → tensor.Tensor ⇥ MathError {`
- `fn add(tensor.Tensor a, tensor.Tensor b) → tensor.Tensor ⇥ MathError {`
- `fn sub(tensor.Tensor a, tensor.Tensor b) → tensor.Tensor ⇥ MathError {`
- `fn mul(tensor.Tensor a, tensor.Tensor b) → tensor.Tensor ⇥ MathError {`
- `fn div(tensor.Tensor a, tensor.Tensor b) → tensor.Tensor ⇥ MathError {`
- `fn neg(tensor.Tensor t) → tensor.Tensor ⇥ MathError {`
- `fn abs(tensor.Tensor t) → tensor.Tensor ⇥ MathError {`
- `fn signum(tensor.Tensor t) → tensor.Tensor ⇥ MathError {`
- `fn sum(tensor.Tensor t, int axis) → tensor.Tensor ⇥ MathError {`
- `fn mean(tensor.Tensor t, int axis) → tensor.Tensor ⇥ MathError {`
- `fn matmul(tensor.Tensor a, tensor.Tensor b) → tensor.Tensor ⇥ MathError {`
- `fn cast(tensor.Tensor t, string nomen) → tensor.Tensor ⇥ MathError {`
- `fn concatenate(list<tensor.Tensor> partes, int axis) → tensor.Tensor ⇥ MathError {`
- `fn slice(tensor.Tensor t, int axis, int initium, int finis) → tensor.Tensor ⇥ MathError {`


## gradus:metrics

Classification accuracy and validated loss/accuracy metric records.

**Source**: `src/metrics.fab`

### Public types

- `union MetricError` — GradusMismatch, FormaMismatch, TypoMismatch, ElementaMismatch, NonFinita, Incompatibilis, Invalida
- `class Metric`
  - fields: `f32 loss`, `f32 accuracy`
  - methods:
    - `fn loss() → f32 {`
    - `fn accuracy() → f32 {`

### Public functions

- `fn message(MetricError e) → string {`
- `fn accuracy(tensor.Tensor prediction, tensor.Tensor target) → f32 ⇥ MetricError {`
- `fn metric(f32 loss, f32 accuracy) → Metric ⇥ MetricError {`
- `fn metric_equal(Metric a, Metric b) → bool {`


## gradus:model/artifact

Pathless content identity for bounded model artifacts.

**Source**: `src/model/artifact.fab`

### Public types

- `union ArtifactError` — AlgorithmusIgnotus, DigestioMala, LongitudoMala
- `class ContentIdentity`
  - fields: `string algorithm`, `string digest`, `int length`

### Public functions

- `fn message(ArtifactError e) → string {`
- `fn identitas(string algorithmus, string digestio, int longitudo) → ContentIdentity ⇥ ArtifactError {`


## gradus:model/capsule

Schema-versioned admitted-model capsules and per-format manifest identity handoff.

**Source**: `src/model/capsule.fab`

### Public types

- `union AdmissionError` — VersioIgnota, SchemaVetus, AlgorithmusIgnotus, DigestioMala, ManifestumMala, WireMala
- `class SafetensorsMetadata`
  - fields: `string key`, `string payload`
  - methods:
    - `fn key() → string {`
    - `fn payload() → string {`
- `class SafetensorsTensorDescriptor`
  - fields: `string name`, `string dtype`, `list<int> shape`, `int start`, `int end`, `int elements`
  - methods:
    - `fn name() → string {`
    - `fn dtype() → string {`
    - `fn shape() → list<int> {`
    - `fn start() → int {`
    - `fn end() → int {`
    - `fn elements() → int {`
- `class SafetensorsManifest`
  - fields: `string format`, `string version`, `int artifact_length`, `int data_length`, `list<SafetensorsMetadata> metadata`, `list<SafetensorsTensorDescriptor> tensors`
  - methods:
    - `fn format() → string {`
    - `fn version() → string {`
    - `fn artifact_length() → int {`
    - `fn data_length() → int {`
    - `fn metadata_count() → int {`
    - `fn tensor_count() → int {`
    - `fn metadata(int i) → SafetensorsMetadata ⇥ AdmissionError {`
    - `fn description(int i) → SafetensorsTensorDescriptor ⇥ AdmissionError {`
- `union Manifest` — Gguf, Safetensors
- `class Capsule`
  - fields: `string schema`, `artifact.ContentIdentity identitas`, `Manifest manifestum`
  - methods:
    - `fn schema() → string {`
    - `fn artifact_identity() → artifact.ContentIdentity {`
    - `fn algorithm() → string {`
    - `fn digest() → string {`
    - `fn length() → int {`
    - `fn format() → string {`
    - `fn tensor_count() → int {`
    - `fn gguf_manifest() → manifestum.GgufManifest ∪ null {`
    - `fn safetensors_manifest() → SafetensorsManifest ∪ null {`
    - `fn identity() → Identity {`
- `class Identity`
  - fields: `string schema`, `string algorithm`, `string digest`, `int byte_length`
  - methods:
    - `fn schema() → string {`
    - `fn algorithm() → string {`
    - `fn digest() → string {`
    - `fn byte_length() → int {`

### Public functions

- `fn message(AdmissionError e) → string {`
- `fn gguf_manifest(manifestum.GgufManifest m) → Manifest {`
- `fn safetensors_manifest(SafetensorsManifest m) → Manifest {`
- `fn identity_equal(Identity a, Identity b) → bool {`
- `fn construct_manifest(string schema, artifact.ContentIdentity identitas, Manifest manifestum) → Capsule ⇥ AdmissionError {`
- `fn verify(Capsule c) → bool ⇥ AdmissionError {`
- `fn verify_against(Capsule c, string expectatum) → bool ⇥ AdmissionError {`
- `fn serialize_identity(Capsule c) → string ⇥ AdmissionError {`
- `fn deserialize_identity(string wire) → Identity ⇥ AdmissionError {`


## gradus:model/dense

Ordered dense-model forward assembly over canonical architecture descriptors and stored-weight views.

**Source**: `src/model/dense.fab`

### Public types

- `class DenseConfig`
  - fields: `int layers`, `int heads`, `int kv_heads`, `int head_dim`, `int hidden_dim`, `int vocab`, `bool tied`
- `class Lookup`
  - fields: `bool successus`, `tensor.Tensor tensorem`, `string message`
- `union DenseError` — TensorAbsens, ConfiguraMala, FormaMala, TerminusExcedit

### Public functions

- `fn message(DenseError e) → string {`
- `fn forward(DenseConfig cfg, (string, int) → Lookup fons, list<int> tokens, f32 epsilon, f32 scale, list<int> positions, int rope_dim, attention.RopeConfig rope_cfg) → tensor.Tensor ⇥ DenseError {`

REF-01-U1.10 consumer: `exempla/dense-prefill-qwen2` (Qwen2.5-0.5B real-file prefill through this `forward`). Compiled rust receipt is **not** recorded: `CODEGEN001` in `dense_qwen2.fab` (definition id 4127 unresolved). llvm-host fallback `PKG001:llvm_emission_failed`. See the exemplum README.


## gradus:model/dense_llama

Llama/SmolLM2 canonical tensor-name resolution and frozen architecture facts.

**Source**: `src/model/dense_llama.fab`

### Public types

- `union LlamaError` — NomenCanonicumIgnotum, StrataExcessiva, TensorDeest, LayoutIgnota
- `class LlamaArch`
  - fields: `string name`, `int layers`, `int heads`, `int kv_heads`, `int head_dim`, `int hidden_dim`, `int vocab`, `bool tied`
- `class CanonicalDescriptor`
  - fields: `string nomen_canonicum`, `string gguf_name`, `list<int> shape`, `int dtype_ggml`, `manifestum.GgmlLayout layout`

### Public functions

- `fn message(LlamaError e) → string {`
- `fn smollm2_arch() → LlamaArch {`
- `fn layout_note(manifestum.GgmlLayout l) → string {`
- `fn gguf_name(LlamaArch a, string canonicum, int stratum) → string ⇥ LlamaError {`
- `fn resolve(manifestum.GgufManifest m, LlamaArch a, string canonicum, int stratum) → CanonicalDescriptor ⇥ LlamaError {`


## gradus:model/dense_qwen2

Qwen2 canonical tensor-name resolution and architecture configuration.

**Source**: `src/model/dense_qwen2.fab`

### Public types

- `class DenseQwen2Config`
  - fields: `int layers`, `int heads`, `int kv_heads`, `int head_dim`, `int hidden_dim`, `int vocab`, `int theta`, `bool tied`
- `union DenseQwen2Error` — ArchaegrammaIgnota, CanonicoIgnota, StratumExtraLimitem, TensorAbsens, ConfiguraMala

### Public functions

- `fn message(DenseQwen2Error e) → string {`
- `fn config(manifestum.GgufManifest m) → DenseQwen2Config ⇥ DenseQwen2Error {`
- `fn resolve(DenseQwen2Config cfg, manifestum.GgufManifest m, string nomen) → manifestum.GgufTensorDescriptor ⇥ DenseQwen2Error {`
- `fn render_description(manifestum.GgufTensorDescriptor t) → string {`


## gradus:model/dequant

CPU dequantization for the admitted GGML block formats.

**Source**: `src/model/dequant.fab`

### Public types

- `union DequantError` — TypoIgnotum, GlomulusMala, OrdoMala, ValorMala
- `class MinScale`
  - fields: `int sc`, `int m`

### Public functions

- `fn message(DequantError e) → string {`
- `fn block_elements(int typo) → int {`
- `fn block_bytes(int typo) → int {`
- `fn dequantize_block(int typo, list<int<u8>> blocci) → list<f32> ⇥ DequantError {`
- `fn dequantize_order(int typo, list<int<u8>> octeti) → list<f32> ⇥ DequantError {`


## gradus:model/gguf

GGUF row admission into the typed model capsule.

**Source**: `src/model/gguf.fab`

### Public types

- `union GgufError` — FormatMala, VersioIgnota, ArchitecturaMala, QuantizatioIgnota, OffsetMala, FormaMala, TokenizerMala, LimitesMala, WireMala, CapsulaMala

### Public functions

- `fn message(GgufError e) → string {`
- `fn admit(list<int<u8>> bytes, string digestio, int expectatum_kv, int expectatum_tensorum, int expectatum_elementa, int expectatum_f32, int expectatum_q4k, int expectatum_q5, int expectatum_q6, int expectatum_q8) → capsula.Capsule ⇥ GgufError {`


## gradus:model/gguf_manifest

Bounded GGUF v3 parsing, range inspection, typed metadata, and tensor descriptors.

**Source**: `src/model/gguf_manifest.fab`

### Public types

- `union GgufManifestError` — FormatMala, VersioIgnota, Truncata, WireMala, LimitesMala, Superfluitas, ClavisDuplicata, TensorDuplicatum, OffsetMala, LayoutIgnota, IdentitasMala, FonsMala
- `class GgufCorpus`
  - fields: `bytes tabula`, `int artifact_length`, `artifact.ContentIdentity identitas`
- `class SourceRead`
  - fields: `bool successus`, `bytes bytes`, `string message`
- `class GgufMetadata`
  - fields: `string key`, `int dtype`, `bytes valor_wire`
- `union GgmlLayout` — Cognita, Ignota
- `class GgufTensorDescriptor`
  - fields: `string name`, `list<int> shape`, `int dtype_ggml`, `int offset_relativum`, `int elements`, `GgmlLayout layout`
- `class GgufManifest`
  - fields: `artifact.ContentIdentity identitas`, `int version`, `int concordatio`, `int data_inceptum`, `int artifact_length`, `list<GgufMetadata> metadata`, `list<GgufTensorDescriptor> tensors`

### Public functions

- `fn message(GgufManifestError e) → string {`
- `fn layout(int typo_ggml, list<int> forma) → GgmlLayout ⇥ GgufManifestError {`
- `fn metadata(GgufManifest m, string clavis) → GgufMetadata ⇥ GgufManifestError {`
- `fn textum(GgufManifest m, string clavis) → string ⇥ GgufManifestError {`
- `fn numerum(GgufManifest m, string clavis) → int ⇥ GgufManifestError {`
- `fn textorum(GgufManifest m, string clavis) → list<string> ⇥ GgufManifestError {`
- `fn numerorum(GgufManifest m, string clavis) → list<int> ⇥ GgufManifestError {`
- `fn numerorum_u32(GgufManifest m, string clavis) → list<int> ⇥ GgufManifestError {` — typed uint32-array accessor (MODEL-01-M1); returns the elements of a GGUF array whose wire element kind is exactly `GGUF_UINT32`, without coercing other integer kinds. A missing key, a non-array value, or a non-uint32 element kind fails closed with a typed `WireMala` error; an array count beyond the bounded limit fails closed with `LimitesMala`. Pins `qwen35moe.rope.dimension_sections` → `[11, 11, 10, 0]`.
- `fn boleanum(GgufManifest m, string clavis) → bool ⇥ GgufManifestError {` — typed bool accessor (MODEL-01-M1); returns the `GGUF_BOOL` metadata value (the parser has already validated the wire byte is 0 or 1). A missing key or a present non-bool value fails closed with a typed `WireMala` error instead of coercing. Pins `tokenizer.ggml.add_bos_token` → `false`.
- `fn longitudo_listae(GgufManifest m, string clavis) → int ⇥ GgufManifestError {` — typed array-length accessor (MODEL-01-M1); reads only the array count from the GGUF array wire header without decoding elements. A missing key or a non-array value fails closed with a typed `WireMala` error; an array count beyond the bounded limit fails closed with `LimitesMala`. Pins the tokenizer identity counts 248320 / 248320 / 247587.
- `fn inveni_tensorem(GgufManifest m, string nomen) → GgufTensorDescriptor ⇥ GgufManifestError {`
- `fn limes_payloadis(GgufManifest m, string nomen) → tuple<int, int> ⇥ GgufManifestError {`
- `fn parse(GgufCorpus corpus) → GgufManifest ⇥ GgufManifestError {`
- `fn inspect((int, int) → SourceRead fons, int longitudo_artifacti, artifact.ContentIdentity identitas) → GgufManifest ⇥ GgufManifestError {`
- `fn read_fragmentum(GgufManifest m, string nomen, int initium, int longitudo, (int, int) → SourceRead fons) → bytes ⇥ GgufManifestError {`


## gradus:model/qwen35moe

Qwen35MoE frozen configuration, canonical tensor map, and admission checks.

**Source**: `src/model/qwen35moe.fab`

### Public types

- `class Qwen35moeConfig`
  - fields: `string architectura`, `int typus_limaturae`, `int versio_quantificationis`, `int numerus_tractuum`, `int longitudo_contextus`, `int longitudo_vestimenti`, `int numerus_capita`, `int numerus_capita_kv`, `int longitudo_clavis`, `int longitudo_valoris`, `f32 epsilon_normae_rms`, `f32 basis_frequentiae`, `int numerus_dimensionum_rotae`, `list<int> sectiones_rotae`, `int numerus_expertorum`, `int numerus_expertorum_activorum`, `int longitudo_ffn_experti`, `int longitudo_ffn_communi`, `int nucleus_convolutus`, `int magnitudo_status`, `int numerus_coetuum`, `int gradus_temporis`, `int magnitudo_interior`, `int intervallum_attentionis_plenae`, `int numerus_strata_nextn`, `string exemplum_tokenizoris`, `string praeparatio_tokenizoris`, `int numerus_tokenum`, `int numerus_typorum_tokenum`, `int numerus_concatenationum`, `int eos_token_id`, `int padding_token_id`, `int bos_token_id`, `bool add_bos_token`
- `union Qwen35moeConfigError` — MetadatumDiversum
- `union Qwen35moeTensorError` — NomenDiversum, FormaDiversa, StipulaDiversa, NumerusDiversus
- `class QwenTensorSummary`
  - fields: `int totalis`, `int globalium`, `int hybridorum`, `int attentionis_plenae`, `int nextn`, `int stipula_f32`, `int stipula_q8_0`, `int stipula_q4_k`, `int stipula_q5_k`, `int stipula_q6_k`, `int stipula_bf16`, `int experti_rank3`
- `class QwenCanonicalTensor`
  - fields: `string name`, `list<int> shape`, `int dtype_ggml`
- `union Qwen35moeReferenceError` — NomenIgnotum, DimensioDiversa, NumerusDivergens, AmbitusMala
- `class Qwen35moeAdmission`
  - fields: `Qwen35moeConfig config`, `QwenTensorSummary summa`
- `union Qwen35moeAdmissionError` — IdentitasDiversa, ArchitecturaIgnota, TypusIgnotus, ConfiguratioDiversa, TensorumDiversum, ReferentiaDiversa, ManifestumMala

### Public functions

- `fn message(Qwen35moeConfigError e) → string {`
- `fn congela(manifestum.GgufManifest m) → Qwen35moeConfig ⇥ Qwen35moeConfigError {`
- `fn causa_tensorum(Qwen35moeTensorError e) → string {`
- `fn tensores_canonici(manifestum.GgufManifest m) → QwenTensorSummary ⇥ Qwen35moeTensorError {`
- `fn causa_referantiae(Qwen35moeReferenceError e) → string {`
- `fn referantia(Qwen35moeConfig c, manifestum.GgufManifest m) → bool ⇥ Qwen35moeReferenceError {`
- `fn causa_admissionis(Qwen35moeAdmissionError e) → string {`
- `fn admit(manifestum.GgufCorpus corpus, string digestio_exspectata, int longitudo_exspectata) → Qwen35moeAdmission ⇥ Qwen35moeAdmissionError {`


## gradus:model/safetensors

Safetensors header parsing and row admission into the typed model capsule.

**Source**: `src/model/safetensors.fab`

### Public types

- `union SafetensorError` — FormaMala, VersioIgnota, ArchitecturaMala, TypoIgnotum, OffscetaMala, FiguraMala, TokenizerMala, LimitesMala, DigestioMala, MerciumMala, IngressioMala
- `class Token`
  - fields: `int kind`, `string payload`
- `class Structure`
  - fields: `list<string> meta_claves`, `list<string> meta_valores`, `list<string> nomina`, `list<string> dtypi`, `list<list<int>> formae`, `list<int> initii`, `list<int> end`
- `class StringValue`
  - fields: `int pos`, `string payload`
- `class MetadataCursor`
  - fields: `int pos`, `list<string> claves`, `list<string> valores`
- `class TensorCursor`
  - fields: `int pos`, `string dtype`, `list<int> shape`, `int start`, `int end`
- `class NumberCursor`
  - fields: `int pos`, `list<int> valores`
- `class HeaderCursor`
  - fields: `int caput`, `string textus`

### Public functions

- `fn message(SafetensorError e) → string {`
- `fn admittas(list<int<u8>> corpus, string digestio, string semita) → capsula.Capsule ⇥ SafetensorError {`


## gradus:model/tensor_payload

Pathless tensor payload carrier with bounded byte ranges.

**Source**: `src/model/tensor_payload.fab`

### Public types

- `class TensorPayload`
  - fields: `string name`, `int absolute_start`, `int length`, `bytes bytes`
- `union PayloadError` — NomineIgnota, RangeMala, LongitudoMala

### Public functions

- `fn message(PayloadError e) → string {`


## gradus:model/tensor_view

Bounded typed views over tensor payloads and materialization windows.

**Source**: `src/model/tensor_view.fab`

### Public types

- `class TensorView`
  - fields: `string name`, `list<int> shape`, `int dtype_ggml`, `int elements`, `manifestum.GgmlLayout layout`, `int absolute_start`, `int longitudo_payloadis`
- `union ViewError` — NomineIgnota, RangeMala, LongitudoMala, LayoutIgnota, TypoIgnotum, OrdoMala, LimitesMala

### Public functions

- `fn message(ViewError e) → string {`
- `fn links(manifestum.GgufManifest m, tensor_payload.TensorPayload p) → TensorView ⇥ ViewError {`
- `fn materialize_slice(TensorView v, int initium_elementum, int longitudo_elementum, (int, int) → manifestum.SourceRead fons) → list<f32> ⇥ ViewError {`
- `fn materialize_block(TensorView v, int index_glomuli, (int, int) → manifestum.SourceRead fons) → list<f32> ⇥ ViewError {`


## gradus:nn

Differentiable tensor primitives: linear, GELU, LayerNorm, RMSNorm, SiLU, and SwiGLU.

**Source**: `src/nn.fab`

### Public types

- `union NnError` — DimensioNegativa, DimensioSupraLimitem, ProductumSupraLimitem, GradusMismatch, FormaMismatch, Incompatibilis, TypoMismatch, ElementaMismatch, EpsilonInvalida

### Public functions

- `fn linear_2x2(tensor<f32, [2, 2]> input, tensor<f32, [2, 2]> weight, tensor<f32, [2, 2]> bias) → tensor<f32, [2, 2]> {`
- `fn linear_4x4(tensor<f32, [4, 4]> input, tensor<f32, [4, 4]> weight, tensor<f32, [4, 4]> bias) → tensor<f32, [4, 4]> {`
- `fn gelu_4x4(tensor<f32, [4, 4]> x) → tensor<f32, [4, 4]> {`
- `fn linear_2x8(tensor<f32, [2, 8]> input, tensor<f32, [8, 8]> weight, tensor<f32, [8]> bias) → tensor<f32, [2, 8]> {`
- `fn layernorm_2x8(tensor<f32, [2, 8]> x, tensor<f32, [8]> scale, tensor<f32, [8]> offset) → tensor<f32, [2, 8]> {`
- `fn gelu_2x8(tensor<f32, [2, 8]> x) → tensor<f32, [2, 8]> {`
- `fn message(NnError e) → string {`
- `fn linear(tensor.Tensor x, tensor.Tensor w, tensor.Tensor b) → tensor.Tensor ⇥ NnError {`
- `fn gelu(tensor.Tensor x) → tensor.Tensor ⇥ NnError {`
- `fn layernorm(tensor.Tensor x, tensor.Tensor scale, tensor.Tensor offset, f32 epsilon) → tensor.Tensor ⇥ NnError {`
- `fn rmsnorm(tensor.Tensor x, tensor.Tensor scale, f32 epsilon) → tensor.Tensor ⇥ NnError {`
- `fn silu(tensor.Tensor x) → tensor.Tensor ⇥ NnError {`
- `fn swiglu(tensor.Tensor gate, tensor.Tensor up, tensor.Tensor down_weight, tensor.Tensor down_bias) → tensor.Tensor ⇥ NnError {`


## gradus:optimize

SGD state, optimizer slots, updates, schedules, and optimizer serialization.

**Source**: `src/optimize.fab`

### Public types

- `union OptimizeError` — NomenInane, VersioInvalida, GeneratioInvalida, PassusInvalida, LentusInvalida, IdentitasMismatch, GradusObsoletus, Gelida, FormaMismatch, Mutatio, NomenDuplicatum, NomenIgnotum, VersioIgnota, WireMala
- `class SgdState`
  - fields: `string owner`, `string name`, `int version`, `int generation`, `int step`, `f32 rate`
  - methods:
    - `fn owner() → string {`
    - `fn name() → string {`
    - `fn version() → int {`
    - `fn generation() → int {`
    - `fn step() → int {`
    - `fn rate() → f32 {`
- `class Sgd`
  - fields: `list<SgdState> states`
  - methods:
    - `fn count() → int {`
    - `fn contains(string owner, string name) → bool {`
    - `fn find(string owner, string name) → SgdState ⇥ OptimizeError {`
- `class StepResult`
  - fields: `parametrum.Parameter fresh`, `SgdState state`
  - methods:
    - `fn fresh() → parametrum.Parameter {`
    - `fn state() → SgdState {`

### Public functions

- `fn message(OptimizeError e) → string {`
- `fn state_equal(SgdState a, SgdState b) → bool {`
- `fn construct(string name, string owner, int generation, f32 rate) → SgdState ⇥ OptimizeError {`
- `fn sgd_equal(Sgd a, Sgd b) → bool {`
- `fn empty_sgd() → Sgd {`
- `fn add(Sgd o, SgdState s) → Sgd ⇥ OptimizeError {`
- `fn step(SgdState s, parametrum.Parameter p, gradient.Gradient g) → StepResult ⇥ OptimizeError {`
- `fn serialize_state(SgdState s) → string {`
- `fn deserialize_state(string wire) → SgdState ⇥ OptimizeError {`
- `fn serialize(Sgd o) → string {`
- `fn deserialize(string wire) → Sgd ⇥ OptimizeError {`


## gradus:parameter

Parameter identity, trainable/frozen status, mutation, registry traversal, and identity wire forms.

**Source**: `src/parameter.fab`

### Public types

- `union Station` — Trainabilis, Gelida
- `union ParameterError` — NomenInane, NomenReservatum, TypoIgnotum, FormaInvalida, ElementaMismatch, GelidaMutatio, NomenDuplicatum, NomenIgnotum, VersioInvalida, WireMala
- `class Identity`
  - fields: `string name`, `dtype.DType dtype`, `list<int> shape`, `int version`, `string owner`
  - methods:
    - `fn name() → string {`
    - `fn dtype_name() → string {`
    - `fn shape() → list<int> {`
    - `fn version() → int {`
    - `fn owner() → string {`
- `class Parameter`
  - fields: `Identity identity`, `Station status`, `tensor.Tensor payload`
  - methods:
    - `fn identity() → Identity {`
    - `fn status() → Station {`
    - `fn name() → string {`
    - `fn dtype_name() → string {`
    - `fn shape() → list<int> {`
    - `fn version() → int {`
    - `fn owner() → string {`
    - `fn numel() → int {`
    - `fn payload() → tensor.Tensor {`
- `class Registry`
  - fields: `list<Parameter> parameters`
  - methods:
    - `fn count() → int {`
    - `fn contains(string owner, string name) → bool {`
    - `fn find(string owner, string name) → Parameter ⇥ ParameterError {`
    - `fn trainable() → list<Parameter> {`
    - `fn frozen() → list<Parameter> {`
    - `fn order() → list<Parameter> {`

### Public functions

- `fn status_name(Station s) → string {`
- `fn message(ParameterError e) → string {`
- `fn identity_equal(Identity a, Identity b) → bool {`
- `fn is_trainable(Parameter p) → bool {`
- `fn is_frozen(Parameter p) → bool {`
- `fn construct(string name, string owner, string typo_nomen, list<int> shape, list<f32> datos) → Parameter ⇥ ParameterError {`
- `fn construct_frozen(string name, string owner, string typo_nomen, list<int> shape, list<f32> datos) → Parameter ⇥ ParameterError {`
- `fn mutate(Parameter p, list<f32> datos) → Parameter ⇥ ParameterError {`
- `fn empty_registry() → Registry {`
- `fn add(Registry r, Parameter p) → Registry ⇥ ParameterError {`
- `fn serialize(Identity i) → string {`
- `fn deserialize(string s) → Identity ⇥ ParameterError {`


## gradus:sampling

Deterministic greedy/filtering/sampling pipeline and sampler configuration.

**Source**: `src/sampling.fab`

### Public types

- `union SamplingError` — LogitsInvalida, ConfiguraInvalida, HistoriaInvalida
- `class Config`
  - fields: `f32 temperature`, `int top_k`, `f32 top_p`, `f32 min_p`, `f32 repetition_penalty`
  - methods:
    - `fn temperature() → f32 {`
    - `fn top_k() → int {`
    - `fn top_p() → f32 {`
    - `fn min_p() → f32 {`
    - `fn repetition_penalty() → f32 {`
- `class Sampler`
  - fields: `int token_id`, `train.Seed seed`
  - methods:
    - `fn token_id() → int {`
    - `fn seed() → train.Seed {`

### Public functions

- `fn message(SamplingError e) → string {`
- `fn construct_config(f32 temperature, int top_k, f32 top_p, f32 min_p, f32 repetition_penalty) → Config ⇥ SamplingError {`
- `fn max(list<f32> logits) → int ⇥ SamplingError {`
- `fn distribution(list<f32> logits, Config c, list<int> history) → list<f32> ⇥ SamplingError {`
- `fn sample(list<f32> logits, Config c, list<int> history, train.Seed seed) → Sampler ⇥ SamplingError {`


## gradus:serialize

Versioned byte serialization for dtype, shape, tensor, and parameter values.

**Source**: `src/serialize.fab`

### Public types

- `union SerializeError` — VersioIgnota, GenusIgnotum, TypoIgnotum, FormaMala, WireMala, DataMala
- `class SerializedTensor`
  - fields: `string dtype_name`, `list<int> shape`, `list<f32> data`
  - methods:
    - `fn dtype() → string {`
    - `fn shape() → list<int> {`
    - `fn data() → list<f32> {`
- `class ParameterWire`
  - fields: `string name`, `string owner`, `string dtype_name`, `list<int> shape`, `int version`, `string status_name`, `list<f32> data`
  - methods:
    - `fn name() → string {`
    - `fn owner() → string {`
    - `fn dtype() → string {`
    - `fn shape() → list<int> {`
    - `fn version() → int {`
    - `fn status() → string {`
    - `fn data() → list<f32> {`

### Public functions

- `fn message(SerializeError e) → string {`
- `fn serialize_dtype(string dtype_name) → bytes ⇥ SerializeError {`
- `fn serialize_shape(list<int> shape) → bytes ⇥ SerializeError {`
- `fn serialize_tensor(list<f32> data, list<int> shape, string dtype_name) → bytes ⇥ SerializeError {`
- `fn serialize_parameter(string name, string owner, string dtype_name, list<int> shape, int version, string status_name, list<f32> data) → bytes ⇥ SerializeError {`
- `fn deserialize_dtype(bytes wire) → string ⇥ SerializeError {`
- `fn deserialize_shape(bytes wire) → list<int> ⇥ SerializeError {`
- `fn deserialize_tensor(bytes wire) → SerializedTensor ⇥ SerializeError {`
- `fn deserialize_parameter(bytes wire) → ParameterWire ⇥ SerializeError {`


## gradus:shape

Runtime shape validation, rank, bounded element counts, broadcasting, reshape, and expansion.

**Source**: `src/shape.fab`

### Public types

- `union ShapeError` — DimensioNegativa, DimensioSupraLimitem, ProductumSupraLimitem, Incompatibilis, ElementMismatch, GradusMismatch

### Public functions

- `fn message(ShapeError e) → string {`
- `fn valid(list<int> forma) → bool {`
- `fn rank(list<int> forma) → int {`
- `fn numel(list<int> forma) → int ⇥ ShapeError {`
- `fn broadcast(list<int> a, list<int> b) → list<int> ⇥ ShapeError {`
- `fn reshape(list<int> forma, list<int> novus) → list<int> ⇥ ShapeError {`
- `fn expand(list<int> forma, int ad_gradum) → list<int> ⇥ ShapeError {`


## gradus:tensor

The staged tensor carrier with runtime shape/dtype/data validation and indexed access.

**Source**: `src/tensor.fab`

### Public types

- `union TensorError` — InvalidShape, ElementMismatch, IndexOutOfBounds
- `class Tensor`
  - fields: `dtype.DType dtype`, `list<int> shape`, `list<f32> data`
  - methods:
    - `fn shape() → list<int> {`
    - `fn rank() → int {`
    - `fn numel() → int {`
    - `fn dtype() → dtype.DType {`
    - `fn valid() → bool {`
    - `fn get(list<int> indices) → f32 ⇥ TensorError {`

### Public functions

- `fn message(TensorError e) → string {`
- `fn construct(list<f32> data, list<int> shape) → Tensor ⇥ TensorError {`
- `fn construct_dtype(list<f32> data, list<int> shape, dtype.DType typo) → Tensor ⇥ TensorError {`
- `fn fill(list<int> shape, f32 valor) → Tensor ⇥ TensorError {`


## gradus:tokenizer

Tokenizer identity, pinned probes, artifact-backed encoding/decoding, Unicode categories, and chat rendering.

**Source**: `src/tokenizer.fab`

### Public types

- `union TokenizerError` — VersioIgnota, ProgeniesIgnota, PreIgnotus, VocabulumMala, DigestioMala, EogMala, IdExtra, ProbeDivergens, ArtificiumMala, MergesMala, IdIgnotum, VestigiumIgnotum, Utf8Mala, WireMala
- `class TokenizerIdentity`
  - fields: `string schema`, `string merge_kind`, `string pre_tokenizer`, `string vocab_digest`, `string eog`, `bool bos_free`, `bool space_free`
  - methods:
    - `fn schema() → string {`
    - `fn merge_kind() → string {`
    - `fn pre_tokenizer() → string {`
    - `fn vocab_digest() → string {`
    - `fn eog() → string {`
    - `fn bos_free() → bool {`
    - `fn space_free() → bool {`
- `class Tokenizer`
  - fields: `list<string> verborum`, `map<string, int> vocabulum`, `map<string, int> concursus`, `list<string> specialia_textus`, `list<int> specialia_ids`, `list<int> eog`, `bool add_bos`, `string chat_template`, `int multitudo`
- `union UnicodeCategory` — Littera, Signum, Numerus, Spatium, NovumLinea, Aliud

### Public functions

- `fn est_eog(int id) → bool {`
- `fn message(TokenizerError e) → string {`
- `fn probe_equal(list<int> a, list<int> b) → bool {`
- `fn probe_id(string pinnata) → list<int> ⇥ TokenizerError {`
- `fn verify_probe(string nomen, list<int> observata) → bool ⇥ TokenizerError {`
- `fn pinned_probe(string nomen) → string ⇥ TokenizerError {`
- `fn construct(string schema, string merge_kind, string pre_tokenizer, string vocab_digest, string eog, bool bos_free, bool space_free) → TokenizerIdentity ⇥ TokenizerError {`
- `fn verify(TokenizerIdentity t) → bool ⇥ TokenizerError {`
- `fn tokenizer_key(TokenizerIdentity t) → string ⇥ TokenizerError {`
- `fn serialize_identity(TokenizerIdentity t) → string ⇥ TokenizerError {`
- `fn deserialize_identity(string wire) → TokenizerIdentity ⇥ TokenizerError {`
- `fn build(manifestum.GgufManifest m) → Tokenizer ⇥ TokenizerError {`
- `fn encode(Tokenizer t, string verbum) → list<int> ⇥ TokenizerError {`
- `fn decode(Tokenizer t, list<int> ids) → string ⇥ TokenizerError {`
- `fn category(string c) → UnicodeCategory {`
- `fn is_letter(string c) → bool {`
- `fn is_symbol(string c) → bool {`
- `fn is_number(string c) → bool {`
- `fn is_space(string c) → bool {`
- `fn is_newline(string c) → bool {`
- `fn is_other(string c) → bool {`
- `fn category_name(string c) → string {`
- `fn scan_words(string textum) → list<string> ⇥ TokenizerError {`
- `fn encode_prompt(Tokenizer t, string textum) → list<int> ⇥ TokenizerError {`
- `fn encode_prompt_special(Tokenizer t, string textum) → list<int> ⇥ TokenizerError {`
- `fn artifact_eog(Tokenizer t) → list<int> {`
- `fn is_artifact_eog(Tokenizer t, int id) → bool {`
- `fn add_bos(Tokenizer t) → bool {`
- `fn chat_template(Tokenizer t) → string {`
- `fn render_user_turn(Tokenizer t, string content) → string ⇥ TokenizerError {`


## gradus:train

Training steps, learning-rate schedules, modes, RNG, dropout, and checkpoints.

**Source**: `src/train.fab`

### Public types

- `union TrainError` — SchedulaInvalida, ModusIgnotus, ExcutioInvalida, PassusNegativus, SemenInvalida, ValorMala, PositioInvalida, StatumInane, VersioIgnota, WireMala
- `class Schedule`
  - fields: `f32 rate_vertex`, `int warmup`, `int total_steps`, `f32 rate_end`
  - methods:
    - `fn rate_vertex() → f32 {`
    - `fn warmup() → int {`
    - `fn total_steps() → int {`
    - `fn rate_end() → f32 {`
- `union Mode` — Disciplina, Aestimatio
- `class Seed`
  - fields: `int status`
  - methods:
    - `fn status() → int {`
- `class Draw`
  - fields: `int payload`, `Seed seed`
  - methods:
    - `fn payload() → int {`
    - `fn seed() → Seed {`
- `class DrawF32`
  - fields: `f32 payload`, `Seed seed`
  - methods:
    - `fn payload() → f32 {`
    - `fn seed() → Seed {`
- `class Dropout`
  - fields: `tensor.Tensor payload`, `Seed seed`
  - methods:
    - `fn payload() → tensor.Tensor {`
    - `fn seed() → Seed {`
- `class Checkpoint`
  - fields: `int age`, `int step`, `Seed rng`, `string state_wire`
  - methods:
    - `fn age() → int {`
    - `fn step() → int {`
    - `fn rng() → Seed {`
    - `fn state_wire() → string {`

### Public functions

- `fn train_step_2x2(tensor<f32, [2, 2]> weight, tensor<f32, [2, 2]> bias, tensor<f32, [2, 2]> grad_weight, tensor<f32, [2, 2]> grad_bias, f32 lr) → tuple<tensor<f32, [2, 2]>, tensor<f32, [2, 2]>> {`
- `fn train_step_4x4(tensor<f32, [4, 4]> weight1, tensor<f32, [4, 4]> bias1, tensor<f32, [4, 4]> weight2, tensor<f32, [4, 4]> bias2, tensor<f32, [4, 4]> grad_weight1, tensor<f32, [4, 4]> grad_bias1, tensor<f32, [4, 4]> grad_weight2, tensor<f32, [4, 4]> grad_bias2, f32 lr) → tuple<tensor<f32, [4, 4]>, tensor<f32, [4, 4]>, tensor<f32, [4, 4]>, tensor<f32, [4, 4]>> {`
- `fn train_step_bert_linear(tensor<f32, [8, 8]> wq, tensor<f32, [8]> bq, tensor<f32, [8, 8]> wk, tensor<f32, [8]> bk, tensor<f32, [8, 8]> wv, tensor<f32, [8]> bv, tensor<f32, [8, 8]> wo, tensor<f32, [8]> bo, tensor<f32, [8, 8]> wf1, tensor<f32, [8]> bf1, tensor<f32, [8, 8]> wf2, tensor<f32, [8]> bf2, tensor<f32, [8, 8]> gwq, tensor<f32, [8]> gbq, tensor<f32, [8, 8]> gwk, tensor<f32, [8]> gbk, tensor<f32, [8, 8]> gwv, tensor<f32, [8]> gbv, tensor<f32, [8, 8]> gwo, tensor<f32, [8]> gbo, tensor<f32, [8, 8]> gwf1, tensor<f32, [8]> gbf1, tensor<f32, [8, 8]> gwf2, tensor<f32, [8]> gbf2, f32 lr) → tuple<tensor<f32, [8, 8]>, tensor<f32, [8]>, tensor<f32, [8, 8]>, tensor<f32, [8]>, tensor<f32, [8, 8]>, tensor<f32, [8]>, tensor<f32, [8, 8]>, tensor<f32, [8]>, tensor<f32, [8, 8]>, tensor<f32, [8]>, tensor<f32, [8, 8]>, tensor<f32, [8]>> {`
- `fn train_step_bert_layernorm(tensor<f32, [8]> ln1_s, tensor<f32, [8]> ln1_o, tensor<f32, [8]> ln2_s, tensor<f32, [8]> ln2_o, tensor<f32, [8]> ln3_s, tensor<f32, [8]> ln3_o, tensor<f32, [8]> gln1_s, tensor<f32, [8]> gln1_o, tensor<f32, [8]> gln2_s, tensor<f32, [8]> gln2_o, tensor<f32, [8]> gln3_s, tensor<f32, [8]> gln3_o, f32 lr) → tuple<tensor<f32, [8]>, tensor<f32, [8]>, tensor<f32, [8]>, tensor<f32, [8]>, tensor<f32, [8]>, tensor<f32, [8]>> {`
- `fn message(TrainError e) → string {`
- `fn construct_schedule(f32 rate_vertex, int warmup, int total_steps, f32 rate_end) → Schedule ⇥ TrainError {`
- `fn scheduled_rate(Schedule s, int passus) → f32 ⇥ TrainError {`
- `fn mode_name(Mode m) → string {`
- `fn is_discipline(Mode m) → bool {`
- `fn is_estimate(Mode m) → bool {`
- `fn mode(string nomen) → Mode ⇥ TrainError {`
- `fn dropout_probability(Mode m, f32 rate) → f32 ⇥ TrainError {`
- `fn construct_seed(int seed) → Seed ⇥ TrainError {`
- `fn next(Seed s) → Draw {`
- `fn next_f32(Seed s) → DrawF32 {`
- `fn dropout(tensor.Tensor x, Seed s, Mode m, f32 rate) → Dropout ⇥ TrainError {`
- `fn serialize_seed(Seed s) → string {`
- `fn deserialize_seed(string wire) → Seed ⇥ TrainError {`
- `fn construct_checkpoint(int age, int passus, Seed rng, string state_wire) → Checkpoint ⇥ TrainError {`
- `fn checkpoint_equal(Checkpoint a, Checkpoint b) → bool {`
- `fn serialize_checkpoint(Checkpoint c) → string {`
- `fn deserialize_checkpoint(string wire) → Checkpoint ⇥ TrainError {`


## gradus:transformer

Fixed-shape and runtime-carrier transformer blocks.

**Source**: `src/transformer.fab`

### Public types

- `union TransformerError` — DimensioNegativa, DimensioSupraLimitem, ProductumSupraLimitem, GradusMismatch, FormaMismatch, Incompatibilis, TypoMismatch, ElementaMismatch, EpsilonInvalida, PositioInvalida, DimensioInvalida, ModusInvalida

### Public functions

- `fn bert_tiny_block_2x8(tensor<f32, [2, 8]> x, tensor<f32, [8]> ln1_s, tensor<f32, [8]> ln1_o, tensor<f32, [8, 8]> wq, tensor<f32, [8]> bq, tensor<f32, [8, 8]> wk, tensor<f32, [8]> bk, tensor<f32, [8, 8]> wv, tensor<f32, [8]> bv, tensor<f32, [8, 8]> wo, tensor<f32, [8]> bo, tensor<f32, [8]> ln2_s, tensor<f32, [8]> ln2_o, tensor<f32, [8, 8]> wf1, tensor<f32, [8]> bf1, tensor<f32, [8, 8]> wf2, tensor<f32, [8]> bf2, tensor<f32, [8]> ln3_s, tensor<f32, [8]> ln3_o, tensor<f32, [2, 2]> scale) → tensor<f32, [2, 8]> {`
- `fn message(TransformerError e) → string {`
- `fn transformer_block(tensor.Tensor x, tensor.Tensor ln1_s, tensor.Tensor ln1_o, tensor.Tensor wq, tensor.Tensor bq, tensor.Tensor wk, tensor.Tensor bk, tensor.Tensor wv, tensor.Tensor bv, tensor.Tensor wo, tensor.Tensor bo, tensor.Tensor ln2_s, tensor.Tensor ln2_o, tensor.Tensor wf1, tensor.Tensor bf1, tensor.Tensor wf2, tensor.Tensor bf2, tensor.Tensor ln3_s, tensor.Tensor ln3_o, f32 scale, int modus, list<int> positions, int dim) → tensor.Tensor ⇥ TransformerError {`
- `fn dense_block(tensor.Tensor x, tensor.Tensor ln1_s, f32 epsilon, tensor.Tensor wq, tensor.Tensor bq, tensor.Tensor wk, tensor.Tensor bk, tensor.Tensor wv, tensor.Tensor bv, tensor.Tensor wo, int num_heads, int num_kv_heads, f32 scale, list<int> positions, int rope_dim, attention.RopeConfig cfg, tensor.Tensor ln2_s, tensor.Tensor wg, tensor.Tensor bg, tensor.Tensor wu, tensor.Tensor bu, tensor.Tensor wd, tensor.Tensor bd) → tensor.Tensor ⇥ TransformerError {`


---

## Inventory gate

```bash
cd /Users/ianzepp/work/faberlang/gradus
./scripta/inventory-public-symbols
```

The inventory gate re-counts every live declaration, asserts the post-S2 per-module baseline and total, and checks that every non-private public function name occurs in the corresponding `## gradus:<module>` section. It is a coverage gate, not a substitute for semantic or executed-value evidence.

**Post-S2 declaration total**: `750` live `fn ` matches. The count is re-read from the live tree; the names above are not inherited from the pre-S2 map.
