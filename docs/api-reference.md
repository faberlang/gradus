# Gradus API Reference

**Version**: `gradus-api-reference v1.0.0` (re-baselined 2026-08-11, PML6-U1;
A1C-M5 revision 2026-08-13 — capsule/gguf/safetensors sections → capsule-schema-2.0.0)
**Repo**: gradus · **Scope**: the live post-PML1–5 + correctness-wave public
`gradus:*` surface. The A1C-M5 revision documents the actual schema-2
capsule surface at A1C-M1 and the frozen D3/D4 `gguf.admit` /
`safetensors.admittas` contracts; the caller migrations (A1C-M2/M3) are
pending in the A1C chain and are not claimed as integrated.
**Authority**: this document is generated from the live source tree
(`src/**/*.fab`) via `scripta/inventory-public-symbols`, which also asserts
every module's `functio` count and runs the **committed coverage gate**: no
public symbol (non-`_`-prefixed `functio`) may exist without a mention in
this reference. A public surface change without a re-baseline fails the
inventory script (zombie-doc gate).

**Conventions**

- **Public vs private**: a `functio` whose name starts with `_` is a
  `@ privata` module-internal helper (implementation detail, not public
  API). Everything else is public and is documented below. Two renamed
  private helpers (`_be4_lege` / `_be8_lege`) are additionally documented in
  [`gradus:serialize`](#gradusserialize) per the correctness-wave
  reconciliation — they are still private, but the rename is part of the
  shipped surface's history.
- **Errors**: every module owns a typed error `discretio` (e.g.
  `LossError`). `causa(e)` renders the message; every variant carries a
  `textus causa`.
- **Shape posture**: static-shape signatures use `tensor<f32, [..]>`; the
  staged-carrier surface uses `tensor.Tensor` (runtime shape facts). See
  [`docs/api-shape-policy.md`](api-shape-policy.md).
- **Structural tier**: this reference documents the **compiled** surface.
  Executed value-identity (proba execution, e2e runs) is env-blocked on the
  FMIR lever and is an auditor-owned gate — no executed claim is made here
  (pml6-delivery.md, CTO8-1).
- **Module map**: [`docs/module-map.md`](module-map.md).

---

## gradus:dtype

Versioned dtype system — `dtype-schema-1.0.0` (PML1-U2). `DType` tag with
four values (F32, F16, I32, U8), value domains, promotion/narrowing tables,
round rules, and serialization. Factory functions build the tag; names are
the serialized form.

- `functio f32() → DType` — the F32 tag.
- `functio f16() → DType` — the F16 tag.
- `functio i32() → DType` — the I32 tag.
- `functio u8() → DType` — the U8 tag.
- `functio message(DTypeError e) → textus` — render the typed error message.
- `functio name(DType t) → textus` — canonical dtype name ("f32", …).
- `functio from_name(textus s) → DType ⇥ DTypeError` — tag from name;
  unknown name fails closed (`NomenIgnotum`).
- `functio width(DType t) → numerus` — element width in bytes.
- `functio serialize(DType t) → textus` — serialized tag form.
- `functio deserialize(textus s) → DType ⇥ DTypeError` — tag from wire.
- `functio promote(DType a, DType b) → bivalens` — lossless widening
  relation (F16→F32, U8→F16/I32/F32, identity pairs).
- `functio narrow(DType a, DType b) → bivalens` — narrowing relation
  (round + range-check; overflow is a typed error).
- `functio finite(f32 x) → bivalens` — finite check (no NaN/±Inf).
- `functio cast(f32 valor, DType origo, DType scopum) → f32 ⇥ DTypeError`
  — elementwise cast per the round rule, fail closed on overflow /
  non-finite.

## gradus:shape

Shape rules — broadcast, reshape, expand, bounded product (PML1-U3, CTO-2).
The 65536 per-dimension cap is a capsule/support-row admission fact
(`pml0-model-capsule-contract.md` §5 row 5), **not** a general math limit;
general checked arithmetic admits 128k–152k vocab rows.

- `functio message(ShapeError e) → textus` — render the typed error message.
- `functio valid(lista<numerus> forma) → bivalens` — shape validity
  (non-negative dims).
- `functio rank(lista<numerus> forma) → numerus` — rank (dimension count).
- `functio numel(lista<numerus> forma) → numerus ⇥ ShapeError` — element
  count (product; `[]` → 1), fail closed on negative dims; the ONE
  validator tensor construction routes through.
- `functio broadcast(lista<numerus> a, lista<numerus> b) → lista<numerus>
  ⇥ ShapeError` — broadcast shape; incompatible ranks/dims fail closed.
- `functio reshape(lista<numerus> forma, lista<numerus> novus) →
  lista<numerus> ⇥ ShapeError` — reshape, element-count-preserving, fail
  closed otherwise.
- `functio expand(lista<numerus> forma, numerus ad_gradum) →
  lista<numerus> ⇥ ShapeError` — expand (broadcast up) to a higher rank.

## gradus:tensor

Plain tensor construction/shape/ops on the staged carrier — explicitly **not**
autograd-aware (PML1-U1). `Tensor` carries a dtype tag, a runtime dimension
list, and flat row-major `f32` data.

`genus Tensor` — methods:

- `functio shape() → lista<numerus>` — runtime shape.
- `functio rank() → numerus` — rank.
- `functio numel() → numerus` — element count.
- `functio dtype() → dtype.DType` — dtype tag.
- `functio valid() → bivalens` — consistency predicate (flat length == shape
  product; dims non-negative).
- `functio get(lista<numerus> indices) → f32 ⇥ TensorError` — validated
  element access (row-major stride walk; rank/index/empty violations fail
  closed).

Free functions:

- `functio message(TensorError e) → textus` — render the typed error message.
- `functio construct(lista<f32> datos, lista<numerus> forma) → Tensor ⇥
  TensorError` — validated construction (dtype F32).
- `functio construct_dtype(lista<f32> datos, lista<numerus> forma, dtype.DType
  typo) → Tensor ⇥ TensorError` — validated construction with a dtype.
- `functio fill(lista<numerus> forma, f32 valor) → Tensor ⇥ TensorError`
  — filled tensor (all elements `valor`).

## gradus:math

Pure operation families over the production tensor surface (PML1-U4) —
construction, elementwise, reduce, matmul, cast, concat/slice. Every failure
is a typed `MathError`. Promotion is explicit (`cast`), never implicit;
division by zero follows f32 semantics (±Inf/NaN, representable in F32).

- `functio message(MathError e) → textus` — render the typed error message.
- `functio construct(lista<f32> datos, lista<numerus> forma) → tensor.Tensor ⇥
  MathError` — validated construction mapped onto the family vocabulary.
- `functio add(tensor.Tensor a, tensor.Tensor b) → tensor.Tensor ⇥ MathError`
  — elementwise add (broadcast per `shape.broadcast`).
- `functio sub(tensor.Tensor a, tensor.Tensor b) → tensor.Tensor ⇥ MathError`
  — elementwise subtract.
- `functio mul(tensor.Tensor a, tensor.Tensor b) → tensor.Tensor ⇥ MathError`
  — elementwise multiply.
- `functio div(tensor.Tensor a, tensor.Tensor b) → tensor.Tensor ⇥ MathError`
  — elementwise divide (f32 semantics: /0 → ±Inf/NaN).
- `functio neg(tensor.Tensor t) → tensor.Tensor ⇥ MathError` — unary negate.
- `functio abs(tensor.Tensor t) → tensor.Tensor ⇥ MathError` — elementwise
  absolute value.
- `functio signum(tensor.Tensor t) → tensor.Tensor ⇥ MathError` — elementwise
  sign (PML4 executed-lane arm: signum elementwise + proba cases).
- `functio sum(tensor.Tensor t, numerus axis) → tensor.Tensor ⇥ MathError`
  — reduce sum over one axis (axis ∈ [0, rank); zero-length axis fails
  closed).
- `functio mean(tensor.Tensor t, numerus axis) → tensor.Tensor ⇥ MathError`
  — reduce mean over one axis.
- `functio matmul(tensor.Tensor a, tensor.Tensor b) → tensor.Tensor ⇥
  MathError` — rank-2 × rank-2 matmul ([M,K] × [K,N] → [M,N]).
- `functio cast(tensor.Tensor t, textus nomen) → tensor.Tensor ⇥ MathError`
  — elementwise value cast by dtype name ("f32"/"f16"/"i32"/"u8").
- `functio concatenate(lista<tensor.Tensor> partes, numerus axis) →
  tensor.Tensor ⇥ MathError` — join along one axis (equal rank/dtype/shape
  except the axis).
- `functio slice(tensor.Tensor t, numerus axis, numerus initium, numerus
  finis) → tensor.Tensor ⇥ MathError` — slice with closed-open bounds
  `[initium, finis)`.

## gradus:parameter

Parameter identity and traversal — `parameter-identity-schema-1.0.0`
(PML1-U5). Explicit `(name, owner, version)` identity, trainable/frozen
status, mutation rules, and registry traversal.

- `functio status_name(Station s) → textus` — "trainable" | "frozen".
- `functio message(ParameterError e) → textus` — render the typed error
  message.

`genus Identity` — methods `name()`, `dtype_name()`, `shape()`, `version()`,
`owner()`; plus `functio identity_equal(Identity a, Identity b) → bivalens`
(field-wise identity equality).

`genus Parameter` — methods `identity()`, `status()`, `name()`,
`dtype_name()`, `shape()`, `version()`, `owner()`, `numel()`, `payload()`;
plus:

- `functio is_trainable(Parameter p) → bivalens` — not frozen.
- `functio is_frozen(Parameter p) → bivalens` — frozen.
- `functio construct(textus name, textus owner, textus dtype_name,
  lista<numerus> shape, lista<f32> datos) → Parameter ⇥ ParameterError` —
  validated trainable constructor.
- `functio construct_frozen(textus name, textus owner, textus dtype_name,
  lista<numerus> shape, lista<f32> datos) → Parameter ⇥ ParameterError` —
  validated frozen constructor.
- `functio mutate(Parameter p, lista<f32> datos) → Parameter ⇥
  ParameterError` — values-only mutation; bumps `version` by 1.

`genus Registry` — methods `count()`, `contains(owner, name)`,
`find(owner, name)` (fail closed on a miss), `trainable()`, `frozen()`,
`order()` (trainables first, then frozen, insertion order); plus:

- `functio empty_registry() → Registry` — empty registry.
- `functio add(Registry r, Parameter p) → Registry ⇥
  ParameterError` — append (duplicate identity fails closed).
- `functio serialize(Identity i) → textus` — identity wire form.
- `functio deserialize(textus s) → Identity ⇥ ParameterError` — identity
  from wire, fail closed.

## gradus:serialize

Versioned bytes serialization contract — `serialize-schema-1.0.0` (PML1-U7).
dtype/shape/tensor/parameter wire forms; exact round-trip; version rejection
and fail-closed reads (capsule rule — no best-effort partial reads).

- `functio message(SerializeError e) → textus` — render the typed error
  message.

`genus SerializedTensor` (deserialized tensor) — methods `dtype()`, `shape()`,
`data()`.
`genus ParameterWire` (deserialized parameter) — methods `name()`, `owner()`,
`dtype()`, `shape()`, `version()`, `status()`, `data()`.

- `functio serialize_dtype(textus dtype_name) → octeti ⇥ SerializeError` —
  dtype wire.
- `functio serialize_shape(lista<numerus> shape) → octeti ⇥ SerializeError` —
  shape wire (i64be dims; element ceiling 1e9, no per-dim 65536 cap — the
  CTO-2 mirror alignment).
- `functio serialize_tensor(lista<f32> data, lista<numerus> shape, textus
  dtype_name) → octeti ⇥ SerializeError` — tensor wire.
- `functio serialize_parameter(textus name, textus owner, textus dtype_name,
  lista<numerus> shape, numerus version, textus status_name, lista<f32> data)
  → octeti ⇥ SerializeError` — parameter wire.
- `functio deserialize_dtype(octeti wire) → textus ⇥ SerializeError` —
  dtype name from wire.
- `functio deserialize_shape(octeti wire) → lista<numerus> ⇥ SerializeError`
  — shape from wire.
- `functio deserialize_tensor(octeti wire) → SerializedTensor ⇥ SerializeError`
  — tensor from wire.
- `functio deserialize_parameter(octeti wire) → ParameterWire ⇥
  SerializeError` — parameter from wire.

**Correctness-wave rename (2026-08-09, `3c295c0`)**: the big-endian readers
were renamed `_le4/_le8` → `_be4_lege/_be8_lege` (the old little-endian
names were misleading for big-endian readers). These are `@ privata`
helpers, not public API — no external migration — but they are the shipped
surface's readers and are recorded here for the correctness-wave
reconciliation:

- `functio _be4_read(lista<numerus<u8>> b, numerus off) → numerus` — read a
  big-endian u32 at `off`.
- `functio _be8_read(lista<numerus<u8>> b, numerus off) → numerus` — read a
  big-endian i64 at `off`.

## gradus:gradient

The gradient-call contract (PML4-U2) — compiler-generated backward
companions invoked through ONE public entry. Pure calculus: no imports from
loss/optimize/nn/attention/transformer. Parameter identity enters as plain
`(owner, name, version)` fields.

- `functio message(GradientError e) → textus` — render the typed error
  message.

`genus Gradient` (per-parameter gradient bundle slot) — methods `owner()`,
`name()`, `version()` (generation — the parameter version at gradient
computation), `payload()`; plus `functio construct(textus name, textus owner,
numerus version, tensor.Tensor payload) → Gradient ⇥ GradientError`.

`genus Gradients` — methods `count()`, `find(owner, name)` (fail closed on a
miss); plus `functio construct_gradients(lista<Gradient> gradients) →
Gradients`.

- `functio obsolete(Gradient g, numerus versio_currens) → bivalens` —
  staleness predicate: a stored gradient is provably stale once the
  parameter has been mutated past its generation.
- `functio nil() → vacuum` — empty marker (no-op forward).
- `functio simple_loss(tensor<f32, [2,2]> x, tensor<f32, [2,2]> w) → f32` —
  the annotated forward (linear regression 2×2 seam).
- `functio gradientes_simple_loss(tensor<f32, [2,2]> x, tensor<f32, [2,2]>
  w, f32 upstream, textus name, textus owner, numerus version) →
  Gradients ⇥ GradientError` — the ONE public companion-call entry: runs
  the compiler-generated backward and pairs every gradient with its
  parameter identity + generation.

## gradus:loss

Loss functions (PML4-U1) — production shape-generic `mse` + `cross_entropy`
over the staged carrier, plus the three admitted fixed-shape MSE rows (same
formula, one documented `mean((p − t)²)`). Every failure is a typed
`LossError`.

- `functio message(LossError e) → textus` — render the typed error message.
- `functio mse(tensor.Tensor prediction, tensor.Tensor target) → f32 ⇥
  LossError` — mean squared error, shape-generic.
- `functio cross_entropy(tensor.Tensor logits, tensor.Tensor target) → f32 ⇥
  LossError` — cross-entropy (target: rank-1 i32 class indices in [0, C)).
- `functio mse_2x2(tensor<f32, [2,2]> prediction, tensor<f32, [2,2]> target)
  → f32` — admitted fixed-shape MSE row (linear regression).
- `functio mse_4x4(tensor<f32, [4,4]> prediction, tensor<f32, [4,4]> target)
  → f32` — admitted fixed-shape MSE row (MLP).
- `functio mse_2x8(tensor<f32, [2,8]> prediction, tensor<f32, [2,8]> target)
  → f32` — admitted fixed-shape MSE row (BERT-tiny).

## gradus:optimize

Optimizer state contract (PML4-U3) — SGD with explicit per-parameter state.
The update is the accepted SGD row `param' = param − rate·grad`, applied
via `parameter.mutate` (version bump). State identity ≡ parameter identity;
stale/frozen/identity-mismatched gradients fail closed.

- `functio message(OptimizeError e) → textus` — render the typed error
  message.

`genus SgdState` (per-parameter state slot) — methods `owner()`,
`name()`, `version()`, `generation()` (parameter version at the last applied
step), `step()` (applied step count), `rate()` (learning rate); plus:

- `functio state_equal(SgdState a, SgdState b) → bivalens` — field-wise
  equality.
- `functio construct(textus name, textus owner, numerus generation, f32
  rate) → SgdState ⇥ OptimizeError` — validated slot constructor.

`genus Sgd` (optimizer state) — methods `count()`, `contains(owner,
name)`, `find(owner, name)` (fail closed); plus:

- `functio sgd_equal(Sgd a, Sgd b) → bivalens` — field-wise equality.
- `functio empty_sgd() → Sgd` — empty optimizer.
- `functio add(Sgd o, SgdState s) → Sgd ⇥ OptimizeError` — register a
  slot.

`genus StepResult` (step outcome) — methods `fresh()` (the updated parameter,
version bumped), `state()` (the advanced state slot); plus:

- `functio passus(SgdState s, parametrum.Parameter p, gradient.Gradient
  g) → StepResult ⇥ OptimizeError` — the ONLY mutation: applies the SGD update,
  fail closed on identity/staleness/frozen/shape violations.
- `functio serialize_state(SgdState s) → textus` — slot wire
  (`optimizer/sgd-state/1.0.0/...`).
- `functio deserialize_state(textus wire) → SgdState ⇥ OptimizeError` —
  slot from wire.
- `functio serialize(Sgd o) → textus` — full optimizer wire
  (`optimizer/sgd/1.0.0/<count>;...`).
- `functio deserialize(textus wire) → Sgd ⇥ OptimizeError` — optimizer from
  wire; round-trip exact by `sgd_equal`.

## gradus:nn

Differentiable NN primitives (PML1 fixed-shape rows + PML3-U1 production
surface). The production surface (`linear`, `gelu`, `layernorm`) is
shape-generic over the staged carrier and imports NO autograd surface
(forward-without-autograd thesis). Formulas match the accepted GPU-training
proofs.

- `functio linear_2x2(tensor<f32, [2,2]> input, tensor<f32, [2,2]> weight,
  tensor<f32, [2,2]> bias) → tensor<f32, [2,2]>` — admitted fixed-shape
  linear.
- `functio linear_4x4(tensor<f32, [4,4]> input, tensor<f32, [4,4]> weight,
  tensor<f32, [4,4]> bias) → tensor<f32, [4,4]>` — admitted fixed-shape
  linear.
- `functio gelu_4x4(tensor<f32, [4,4]> x) → tensor<f32, [4,4]>` — admitted
  fixed-shape GELU.
- `functio linear_2x8(tensor<f32, [2,8]> input, tensor<f32, [8,8]> weight,
  tensor<f32, [8]> bias) → tensor<f32, [2,8]>` — admitted fixed-shape
  linear with per-channel bias.
- `functio layernorm_2x8(tensor<f32, [2,8]> x, tensor<f32, [8]> scale,
  tensor<f32, [8]> offset) → tensor<f32, [2,8]>` — admitted fixed-shape
  LayerNorm.
- `functio gelu_2x8(tensor<f32, [2,8]> x) → tensor<f32, [2,8]>` — admitted
  fixed-shape GELU.
- `functio message(NnError e) → textus` — render the typed error message.
- `functio linear(tensor.Tensor x, tensor.Tensor w, tensor.Tensor b) →
  tensor.Tensor ⇥ NnError` — shape-generic linear (`x·w + b`; b per-channel
  [N] or same-shape [M,N]).
- `functio gelu(tensor.Tensor x) → tensor.Tensor ⇥ NnError` — shape-generic
  GELU (tanh approximation, self-hosted).
- `functio layernorm(tensor.Tensor x, tensor.Tensor scale, tensor.Tensor
  offset, f32 epsilon) → tensor.Tensor ⇥ NnError` — shape-generic LayerNorm
  over the last axis.
- `functio rmsnorm(tensor.Tensor x, tensor.Tensor scale, f32 epsilon) →
  tensor.Tensor ⇥ NnError` — shape-generic RMSNorm over the last axis, no
  centering (`x / sqrt(mean(x²) + ε) · γ`; the llama-arch norm family,
  REF-01-U1.1).
- `functio silu(tensor.Tensor x) → tensor.Tensor ⇥ NnError` — shape-generic
  SiLU (`x·sigmoid(x)`, self-hosted sigmoid via the e^{−t} identity).
- `functio swiglu(tensor.Tensor gate, tensor.Tensor up, tensor.Tensor
  down_weight, tensor.Tensor down_bias) → tensor.Tensor ⇥ NnError` — the
  SwiGLU gated-MLP row: `h = silu(gate) ⊙ up`, `y = linear(h, down_weight,
  down_bias)`; gate/up share a rank-2 shape, down_weight [F,N], down_bias
  per-channel [N] or same-shape [M,N].

## gradus:attention

Attention building blocks (fixed-shape S6-G1 row + PML3-U2 production
surface). Architectural rule: attention is a building block, not a
transformer component — never imports `gradus:transformer`.

- `functio scaled_dot_product_2x8(tensor<f32, [2,8]> qb, tensor<f32, [2,8]>
  kb, tensor<f32, [2,8]> vb, tensor<f32, [2,2]> scale) → tensor<f32, [2,8]>`
  — admitted fixed-shape single-head attention (B=2, D=8, H=1).
- `functio causa(AttentionError e) → textus` — render the typed error
  message.
- `functio rotary_position_embedding(tensor.Tensor x, lista<numerus>
  positions, numerus dim) → tensor.Tensor ⇥ AttentionError` — RoPE on the
  staged carrier (llama-arch NORM consecutive-pair, freq_base 100000).
- `functio rotary_position_embedding_configura(tensor.Tensor x,
  lista<numerus> positions, numerus dim, RopeConfigura configura) →
  tensor.Tensor ⇥ AttentionError` — configurable RoPE: frequency base
  (theta), scale, and pair policy (consecutive-pair llama NORM vs
  interleaved-pair qwen2) — the REF-01-U1.3 generalization.
- `genus RopeConfigura` (fields `base`, `scale`, `politica`, accessor
  methods `base()`/`scale()`/`politica()`) — the validated config carrier;
  construct via `structa_rope_configura(base, scale, politica)`.
- `functio structa_rope_configura(f32 base, f32 scale, RopePolitica
  politica) → RopeConfigura ⇥ AttentionError` — validated constructor
  (positive finite base/scale).
- `discretio RopePolitica` (`Consecutiva` / `Interposita`) with factories
  `politica_consecutiva()` / `politica_interposita()` and renderer
  `politica_nomen()` — the RoPE pair-policy discriminator.
- `functio scaled_dot_product(tensor.Tensor q, tensor.Tensor k,
  tensor.Tensor v, f32 scale) → tensor.Tensor ⇥ AttentionError` —
  shape-generic SDPA.
- `functio scaled_dot_product_causal(tensor.Tensor q, tensor.Tensor k,
  tensor.Tensor v, f32 scale) → tensor.Tensor ⇥ AttentionError` — causal-
  masked SDPA.
- `functio scaled_dot_product_causal_rope(tensor.Tensor q, tensor.Tensor k,
  tensor.Tensor v, f32 scale, lista<numerus> positions, numerus dim) →
  tensor.Tensor ⇥ AttentionError` — causal + RoPE SDPA (the inference-row
  mode 2).
- `functio multi_head_attention(tensor.Tensor q, tensor.Tensor k,
  tensor.Tensor v, tensor.Tensor wo, numerus num_heads, numerus
  num_kv_heads, f32 scale, lista<numerus> positions, numerus rope_dim,
  RopeConfigura rope_configura) → tensor.Tensor ⇥ AttentionError` —
  multi-head attention with GQA KV-head sharing (REF-01-U1.4): per-head
  q/k/v splits (0 < num_kv_heads ≤ num_heads, H % K == 0, query head h
  attends through KV group g = h // (H/K)), scaled causal scores, v
  accumulation, head concatenation, and the [H·D, H·D] output projection
  (out = concat · woᵀ, wo in the [in, out] linear layout); q and k are
  rotated at their positions first via the configurable RoPE row. The
  inference composition is causal + RoPE; shape-generic (no fixed-shape
  constants).

## gradus:transformer

Transformer blocks (fixed-shape S6-G1 row + PML3-U3 production surface).
The block is pre-LN → attention → output projection → residual → post-LN →
FFN → residual → pre-loss LN. Never imports `gradus:train`.

- `functio bert_tiny_block_2x8(tensor<f32, [2,8]> x, tensor<f32, [8]> ln1_s,
  tensor<f32, [8]> ln1_o, tensor<f32, [8,8]> wq, tensor<f32, [8]> bq,
  tensor<f32, [8,8]> wk, tensor<f32, [8]> bk, tensor<f32, [8,8]> wv,
  tensor<f32, [8]> bv, tensor<f32, [8,8]> wo, tensor<f32, [8]> bo,
  tensor<f32, [8]> ln2_s, tensor<f32, [8]> ln2_o, tensor<f32, [8,8]> wf1,
  tensor<f32, [8]> bf1, tensor<f32, [8,8]> wf2, tensor<f32, [8]> bf2,
  tensor<f32, [8]> ln3_s, tensor<f32, [8]> ln3_o, tensor<f32, [2,2]> scale)
  → tensor<f32, [2,8]>` — admitted fixed-shape BERT-tiny block (18
  trainable params + frozen dk_scale in; pre-loss LN out).
- `functio causa(TransformerError e) → textus` — render the typed error
  message.
- `functio transformer_block(tensor.Tensor x, tensor.Tensor ln1_s,
  tensor.Tensor ln1_o, tensor.Tensor wq, tensor.Tensor bq, tensor.Tensor wk,
  tensor.Tensor bk, tensor.Tensor wv, tensor.Tensor bv, tensor.Tensor wo,
  tensor.Tensor bo, tensor.Tensor ln2_s, tensor.Tensor ln2_o,
  tensor.Tensor wf1, tensor.Tensor bf1, tensor.Tensor wf2, tensor.Tensor bf2,
  tensor.Tensor ln3_s, tensor.Tensor ln3_o, f32 scale, numerus modus,
  lista<numerus> positions, numerus dim) → tensor.Tensor ⇥ TransformerError`
  — shape-generic transformer block over the staged carrier (mode 2 =
  causal + RoPE, the selected inference row).
- `functio dense_block(tensor.Tensor x, tensor.Tensor ln1_s, f32 epsilon,
  tensor.Tensor wq, tensor.Tensor bq, tensor.Tensor wk, tensor.Tensor bk,
  tensor.Tensor wv, tensor.Tensor bv, tensor.Tensor wo, numerus num_heads,
  numerus num_kv_heads, f32 scale, lista<numerus> positions, numerus
  rope_dim, attention.RopeConfigura rope_configura, tensor.Tensor ln2_s,
  tensor.Tensor wg, tensor.Tensor bg, tensor.Tensor wu, tensor.Tensor bu,
  tensor.Tensor wd, tensor.Tensor bd) → tensor.Tensor ⇥ TransformerError`
  — the generic dense transformer block over the staged carrier
  (REF-01-U1.5): input RMSNorm → GQA attention (causal + RoPE, U1.4) →
  residual → post-attn RMSNorm → SwiGLU MLP (U1.2) → residual, composing
  the U1.1/U1.2/U1.4 rows; no fixed-shape constants (every shape derives
  from the runtime tensors and the head counts).

## gradus:train

Training steps, schedules, mode, RNG, dropout, and the checkpoint
(PML4-U4/U6). The fixed-shape steps carry the accepted SGD update math
inline (FMIR stepper lib→lib gap).

- `functio train_step_2x2(tensor<f32, [2,2]> weight, tensor<f32, [2,2]> bias,
  tensor<f32, [2,2]> grad_weight, tensor<f32, [2,2]> grad_bias, f32 lr) →
  iuncta<tensor<f32, [2,2]>, tensor<f32, [2,2]>>` — admitted fixed-shape SGD
  step (linear regression).
- `functio train_step_4x4(tensor<f32, [4,4]> weight1, tensor<f32, [4,4]>
  bias1, tensor<f32, [4,4]> weight2, tensor<f32, [4,4]> bias2,
  tensor<f32, [4,4]> grad_weight1, tensor<f32, [4,4]> grad_bias1,
  tensor<f32, [4,4]> grad_weight2, tensor<f32, [4,4]> grad_bias2, f32 lr) →
  iuncta<tensor<f32, [4,4]>, tensor<f32, [4,4]>, tensor<f32, [4,4]>,
  tensor<f32, [4,4]>>` — admitted fixed-shape SGD step (two-layer MLP).
- `functio train_step_bert_linear(...)` — fixed-shape BERT-tiny linear-grad
  step (12 trainable weight/bias pairs + lr → 24-tuple update).
- `functio train_step_bert_layernorm(...)` — fixed-shape BERT-tiny
  layernorm-grad step (6 scale/offset pairs + lr → 12-tuple update).
- `functio message(TrainError e) → textus` — render the typed error message.

`genus Schedule` (LR schedule) — methods `rate_vertex()`, `warmup()`
(warmup steps), `total_steps()` (decay horizon), `rate_end()`; plus:

- `functio construct_schedule(f32 rate_vertex, numerus warmup, numerus
  total_steps, f32 rate_end) → Schedule ⇥ TrainError` — validated
  constructor.
- `functio scheduled_rate(Schedule s, numerus passus) → f32 ⇥ TrainError`
  — linear warmup → cosine decay to `rate_end`.

Mode:

- `functio mode_name(Mode m) → textus` — mode name ("disciplina" |
  "aestimatio").
- `functio is_discipline(Mode m) → bivalens` — training-mode predicate.
- `functio is_estimate(Mode m) → bivalens` — evaluation-mode predicate.
- `functio mode(textus nomen) → Mode ⇥ TrainError` — mode from name, fail
  closed.
- `functio dropout_probability(Mode m, f32 rate) → f32 ⇥ TrainError` — the
  dropout pass probability in the given mode (1.0 in evaluation mode).

RNG (xorshift64, the Seed rule: nonzero state; 0 degenerates and fails
closed):

`genus Seed` — method `status()`; plus `functio construct_seed(numerus
seed) → Seed ⇥ TrainError`.
`genus Draw` (integer draw) — methods `payload()`, `seed()`; plus
`functio next(Seed s) → Draw`.
`genus DrawF32` (unit draw) — methods `payload()` (∈ [0,1)), `seed()`;
plus `functio next_f32(Seed s) → DrawF32`.
`genus Dropout` (masked tensor + advanced state) — methods `payload()`,
`seed()`; plus:

- `functio dropout(tensor.Tensor x, Seed s, Mode m, f32 rate) → Dropout ⇥
  TrainError` — dropout application.
- `functio serialize_seed(Seed s) → textus` — RNG state wire.
- `functio deserialize_seed(textus wire) → Seed ⇥ TrainError` — RNG state
  from wire.

Checkpoint `Checkpoint` (PML4-U6):

`genus Checkpoint` — methods `age()` (epoch), `step()` (step in epoch),
`rng()` (Seed), `state_wire()` (embedded optimizer-state wire); plus:

- `functio construct_checkpoint(numerus age, numerus passus, Seed rng, textus
  state_wire) → Checkpoint ⇥ TrainError` — validated constructor.
- `functio checkpoint_equal(Checkpoint a, Checkpoint b) → bivalens` — field-wise
  equality.
- `functio serialize_checkpoint(Checkpoint c) → textus` — checkpoint wire.
- `functio deserialize_checkpoint(textus wire) → Checkpoint ⇥ TrainError` —
  checkpoint from wire, fail closed.

## gradus:metrics

Defined metric values with a deterministic contract (PML4-U5) —
`accuracy` is top-1 classification accuracy with documented tie-breaks;
`Metric` is the per-step loss + accuracy record.

- `functio message(MetricError e) → textus` — render the typed error message.
- `functio accuracy(tensor.Tensor prediction, tensor.Tensor target) → f32
  ⇥ MetricError` — (1/N)·Σ_n [argmax_c pred[n,c] == target[n]]; ties go to
  the LOWEST class index; deterministic, no RNG.

`genus Metric` — methods `loss()`, `accuracy()`; plus:

- `functio metric(f32 loss, f32 accuracy) → Metric ⇥ MetricError` —
  validated record (finite loss, accuracy ∈ [0, 1]).
- `functio metric_equal(Metric a, Metric b) → bivalens` — field-wise
  equality.

## gradus:model/artifact

Pathless content identity for bounded model-format sources (GGUF-A1a). The
identity carries algorithm, digest, and byte length only; it never owns a
path, URL, reader, file handle, mapping, host/device object, or payload.

`genus IdentitasContenuti` — fields `algorithmus`, `digestio`, and
`longitudo`.

- `functio causa(ArtifactError e) → textus` — render the typed identity error.
- `functio identitas(textus algorithmus, textus digestio, numerus longitudo) →
  IdentitasContenuti ⇥ ArtifactError` — validate the lower-case `sha-256`
  algorithm, 64-digit lower-case hexadecimal digest, and positive byte length.

`discretio ArtifactError` variants: `AlgorithmusIgnotus`, `DigestioMala`, and
`LongitudoMala`; each carries `textus causa`.

## gradus:model/capsule

The admitted-model capsule — the typed identity handoff (council C8,
PML2-U1, `capsule-schema-2.0.0`, A1C-M1 clean break). Schema 2 carries
exactly two value groups: a pathless `artifact.IdentitasContenuti` content
identity (named digest algorithm, whole-artifact digest value, byte length
— never a path, URL, reader, file handle, device object, or payload) and
one per-format manifest (`Manifesta`): `manifestum.ManifestumGguf`
(imported read-only from `gradus:model/gguf_manifest`) for GGUF rows or the
`ManifestumSafetensors` genus (defined in this module) for Safetensors
rows. There is no `BytesValida` byte ownership, no provenance path, and no
single global quantization row. Admission is fail-closed by every field; a
schema-1 stamp is rejected at every boundary with the typed
`AdmissionError.SchemaVetus`.

- `functio causa(AdmissionError e) → textus` — render the typed error
  message.

`discretio AdmissionError` variants: `VersioIgnota` (unknown schema
version), `SchemaVetus` (schema 1 is retired), `AlgorithmusIgnotus`
(un-admitted digest algorithm), `DigestioMala` (malformed or mismatched
digest), `ManifestumMala` (malformed per-format manifest, identity
inconsistency, or verification failure), and `WireMala` (malformed
identity wire form); each carries `textus causa`.

`genus MetadatumSafetensori` — methods `clavis()`, `valor()`.
`genus DescriptioTensorisSafetensori` — methods `nomen()`, `typo()`,
`forma()`, `initium()` (inclusive data offset), `finis()` (exclusive data
end), `elementa()`.
`genus ManifestumSafetensors` — methods `formatum()` (pinned row:
"safetensors"), `versio()` (header format version), `longitudo_artefacti()`
(whole-artifact byte length), `longitudo_datorum()` (data-region byte
length), `metadatorum_numerus()`, `tensorum_numerus()`, `metadatum(numerus
i)` (bounds-checked), `descriptio(numerus i)` (bounds-checked).
`discretio Manifesta` — `Gguf { manifestum.ManifestumGguf gguf }` or
`Safetensors { ManifestumSafetensors saf }`; the two wrappers below are the
only construction entry points (a caller never pattern-builds a variant
directly).
`genus Capsula` — methods `schematis()`, `identitas_artificii()`,
`algorithmus()`, `digestio()`, `longitudo()`, `formatum()` ("gguf" |
"safetensors"), `tensorum_numerus()`, `manifestum_gguf()` (the GGUF
manifest when the capsule holds a GGUF row, else `nihil`),
`manifestum_safetensors()` (the Safetensors manifest when the capsule holds
a Safetensors row, else `nihil`), `identia()` (the compact
schema-versioned identity record).
`genus Identitas` — methods `schematis()`, `algorithmus()`, `digestio()`,
`longitudo_bytes()`.

Free functions:

- `functio identitas_aequus(Identitas a, Identitas b) → bivalens` —
  field-wise identity equality (identity-bearing fields ONLY; never the
  manifest contents).
- `functio manifestum_gguf(manifestum.ManifestumGguf m) → Manifesta` —
  wrap a GGUF manifest into the per-format carrier.
- `functio manifestum_safetensors(ManifestumSafetensors m) → Manifesta` —
  wrap a Safetensors manifest into the per-format carrier.
- `functio structa_manifestum(textus schema, artifact.IdentitasContenuti
  identitas, Manifesta manifestum) → Capsula ⇥ AdmissionError` — the
  fail-closed ADMISSION and the only capsule constructor: rejects the
  retired schema-1 stamp (`SchemaVetus`), unknown schema versions
  (`VersioIgnota`), un-admitted algorithms, malformed digests, invalid
  byte lengths, and manifests inconsistent with the carried identity.
- `functio verifica(Capsula c) → bivalens ⇥ AdmissionError` — consumer-side
  self-verification (re-runs the admission matrix over a capsule without
  re-parsing raw model bytes).
- `functio verifica_contra(Capsula c, textus expectatum) → bivalens ⇥
  AdmissionError` — verify against an expected digest; mismatch fails
  closed.
- `functio serializa_identitas(Capsula c) → textus ⇥ AdmissionError` —
  identity wire form (`capsule/identity/<schema>/<algo>/<digest>/<byte_len>`).
- `functio deserializa_identitas(textus wire) → Identitas ⇥ AdmissionError`
  — identity from wire, fail closed; rejects the retired schema-1 stamp
  with `SchemaVetus`.

**Schema retirement (A1C-M1, `1c3bc51`)**: the schema-1 stamp (`"1.0.0"`)
is retired as of 2026-08-13. The schema-2 constructor has no schema-1
signature (a schema-1 call site fails to compile); `verifica` and
`deserializa_identitas` reject a schema-1-stamped capsule/wire with the
typed `SchemaVetus` error (`schema 1 is retired — capsule schema is 2.0.0`).
EOG/tokenizer identity is no longer carried by the capsule — it lives in
`gradus:tokenizer`, and the per-format admission entries enforce their own
tokenizer facts (see the D3/D4 entries below).

## gradus:model/dense_llama

Typed `llama` (SmolLM2) architecture adapter (REF-01-U1.6, feeds Gate 1).
The adapter is a canonical tensor-name → manifest-descriptor mapping over the
`gradus:model/gguf_manifest` surface. Canonical families: `model.embed_tokens`,
`model.layers.{N}.input_layernorm`, `model.layers.{N}.self_attn.q_proj`,
`model.layers.{N}.self_attn.k_proj`, `model.layers.{N}.self_attn.v_proj`,
`model.layers.{N}.self_attn.o_proj`,
`model.layers.{N}.post_attention_layernorm`,
`model.layers.{N}.mlp.gate_proj`, `model.layers.{N}.mlp.up_proj`,
`model.layers.{N}.mlp.down_proj`, `model.norm`, and `lm_head`. Layer-indexed
families take the layer index as `stratum`; it must be within the frozen
layer range. The adapter retains no path, reader, source function, or payload.

- `discretio DensumLlamaError` — typed fail-closed diagnostics: every
  variant carries `textus causa`, rendered by `causa(e)`. Variants:
  `NomenCanonicumIgnotum` (unknown canonical name), `StrataExcessiva` (layer
  index outside the frozen layer range), `TensorDeest` (the canonical target's
  GGUF tensor is absent from the manifest), `LayoutIgnota` (the resolved
  tensor's GGML layout is unknown).
- `genus ArsLlama` — the frozen architecture config: `nomen`, `strata`
  (layer count), `capita` (heads), `capita_kv` (KV heads), `dimensio_capitis`
  (head_dim), `dimensio_occulta` (hidden dim), `vocabularia` (vocab),
  `nexa_immortalia` (tied embeddings).
- `genus DescriptioCanonica` — one resolved canonical descriptor:
  `nomen_canonicum`, `nomen_gguf`, `forma`, `typo_ggml`, `layout`.
- `functio causa(DensumLlamaError e) → textus` — render the typed error
  message.
- `functio ars_smollm2() → ArsLlama` — the frozen SmolLM2-360M config
  (32 layers, 15 heads, 5 KV heads, head_dim 64, hidden 960, vocab 49152,
  tied embedding). Facts are the read-only GGUF-A1b inspect-surface pins for
  the real SmolLM2-360M-Instruct-Q4_K_M.gguf file (recorded in
  `src/model/dense_llama.proba`).
- `functio layout_nota(manifestum.LayoutGgml l) → textus` — deterministic
  layout knownness render (`"known"`/`"unknown"`); the module owns the
  imported-union discrimination.
- `functio nomen_gguf(ArsLlama a, textus canonicum, numerus stratum) →
  textus ⇥ DensumLlamaError` — canonical name → GGUF tensor name
  (`token_embd.weight`, `blk.{N}.attn_{q,k,v}_weight`,
  `blk.{N}.attn_output.weight`, `blk.{N}.attn_norm.weight`,
  `blk.{N}.ffn_{gate,up,down}_weight`, `blk.{N}.ffn_norm.weight`,
  `output_norm.weight`, `output.weight`); fail closed on unknown names and
  out-of-range layer indices. The tied `lm_head` maps to the shared
  `token_embd.weight`; an untied row maps to `output.weight`.
- `functio resolvo(manifestum.ManifestumGguf m, ArsLlama a, textus canonicum,
  numerus stratum) → DescriptioCanonica ⇥ DensumLlamaError` — resolve a
  canonical name to its manifest descriptor (canonical name, GGUF name,
  shape, GGML type id, layout); fail closed when the GGUF tensor is absent
  (`TensorDeest`) or its layout is unknown (`LayoutIgnota`).

## gradus:model/gguf_manifest

Format-general GGUF v3 manifest inspection (GGUF-A1b). `CorpusGguf` accepts a
bounded prefix containing the complete header, metadata, and tensor table.
`inspice` instead advances through exact ranges supplied by a caller-owned
function. Both routes retain metadata value kinds and exact wire payloads, raw
tensor names/shapes/types/relative offsets, and known GGML block geometry.
Unknown architecture metadata and raw GGML type IDs remain inspectable.
Metadata and tensor directories are bounded at 4,096 entries; retained
metadata values and individual reads are bounded at 64 MiB. The source
function is operation-scoped and is never retained. The synthetic package
proof executes 40 cases with 40 PASS / 0 FAIL. A separate guarded adapter
matches six operator-local files against independent GGUF data offsets and
counts without reading tensor payloads. Neither receipt admits an architecture,
implements tokenization, or claims inference. The LIB-02-U1 typed array
accessors (`textorum`/`numerorum`) read the tokenizer metadata block
(`tokenizer.ggml.tokens`, `tokenizer.ggml.token_type`,
`tokenizer.ggml.merges`) from a parsed schema-2 manifest with the exact
target-prefix counts (248320 tokens, 247587 merges) and pinned special ids
pinned in `src/model/gguf_manifest.proba`.

`genus CorpusGguf` — fields `tabula`, `longitudo_artifacti`, and
`identitas`.
`genus LectioFontis` — fields `successus`, `bytes`, and `causa`; one explicit
success/failure result from a caller-owned range function.
`genus MetadatumGguf` — fields `clavis`, `typo`, and `valor_wire`.
`discretio LayoutGgml` — `Cognita(elementa_per_blockum,
octeti_per_blockum, longitudo_octetorum)` or `Ignota(typo)`.
`genus DescriptioTensorisGguf` — fields `nomen`, `forma`, `typo_ggml`,
`offset_relativum`, `elementa`, and `layout`.
`genus ManifestumGguf` — fields `identitas`, `versio`, `concordatio`,
`data_inceptum`, `longitudo_artifacti`, `metadata`, and `tensores`.

- `functio causa(GgufManifestError e) → textus` — render the parser error.
- `functio parse(CorpusGguf corpus) → ManifestumGguf ⇥ GgufManifestError` —
  parse GGUF v3 header/metadata/tensor table from a bounded corpus.
- `functio inspice((numerus, numerus) → LectioFontis fons, numerus
  longitudo_artifacti, artifact.IdentitasContenuti identitas) →
  ManifestumGguf ⇥ GgufManifestError` — inspect exact header, metadata, and
  tensor-directory ranges from an operation-scoped source without retaining
  the source or requesting tensor payload bytes.
- `functio lege_fragmentum(ManifestumGguf m, textus nomen, numerus initium,
  numerus longitudo, (numerus, numerus) → LectioFontis fons) → octeti ⇥
  GgufManifestError` — read one checked relative fragment of a known-layout
  tensor through a newly supplied source; unknown layouts fail closed.
- `functio metadatum(ManifestumGguf m, textus clavis) → MetadatumGguf ⇥
  GgufManifestError` — retrieve one preserved metadata entry.
- `functio textum(ManifestumGguf m, textus clavis) → textus ⇥
  GgufManifestError` — typed text accessor for a string metadata value.
- `functio numerum(ManifestumGguf m, textus clavis) → numerus ⇥
  GgufManifestError` — typed integer accessor for an integer metadata value;
  `GGUF_BOOL` and floating-point values remain parseable/preserved but return a
  typed `WireMala` error from this accessor.
- `functio textorum(ManifestumGguf m, textus clavis) → lista<textus> ⇥
  GgufManifestError` — typed string-array accessor (LIB-02-U1); returns the
  elements of a GGUF string array such as `tokenizer.ggml.tokens` /
  `tokenizer.ggml.merges`. A non-array value or a non-string element kind
  returns a typed `WireMala` error.
- `functio numerorum(ManifestumGguf m, textus clavis) → lista<numerus> ⇥
  GgufManifestError` — typed integer-array accessor (LIB-02-U1); returns the
  elements of an integer array such as `tokenizer.ggml.token_type`. A
  non-array value or a non-integer element kind returns a typed `WireMala`
  error. Scalar tokenizer ids (`tokenizer.ggml.bos_token_id` and friends) and
  the chat template stay on the `numerum`/`textum` surface.
- `functio numerorum_u32(ManifestumGguf m, textus clavis) → lista<numerus> ⇥
  GgufManifestError` — typed uint32-array accessor (MODEL-01-M1); returns the
  elements of a GGUF array whose wire element kind is exactly `GGUF_UINT32`,
  without coercing other integer kinds. A missing key, a non-array value, or a
  non-uint32 element kind fails closed with a typed `WireMala` error; an array
  count beyond the bounded limit fails closed with `LimitesMala`.
- `functio boleanum(ManifestumGguf m, textus clavis) → bivalens ⇥
  GgufManifestError` — typed bool accessor (MODEL-01-M1); returns the
  `GGUF_BOOL` metadata value (the parser has already validated the wire byte
  is 0 or 1). A missing key or a present non-bool value fails closed with a
  typed `WireMala` error instead of coercing.
- `functio longitudo_listae(ManifestumGguf m, textus clavis) → numerus ⇥
  GgufManifestError` — typed array-length accessor (MODEL-01-M1); reads only
  the array count from the GGUF array wire header without decoding elements.
  A missing key or a non-array value fails closed with a typed `WireMala`
  error; an array count beyond the bounded limit fails closed with
  `LimitesMala`.
- `functio inveni_tensorem(ManifestumGguf m, textus nomen) →
  DescriptioTensorisGguf ⇥ GgufManifestError` — retrieve one tensor descriptor.
- `functio limes_payloadis(ManifestumGguf m, textus nomen) → iuncta<numerus,
  numerus> ⇥ GgufManifestError` — exact stored byte range of one known-layout
  tensor as `(initium_absolutum, longitudo_payloadis)` relative to the content
  identity (GGUF-A3 C2-U1). Reuses the already-validated range/overlap facts
  from parse/inspice via `inveni_tensorem` — no new layout derivation.
  `Ignota` layout fails closed (`LayoutIgnota`); unknown name fails closed via
  the `inveni_tensorem` passthrough (`WireMala`). This is the payload-range
  seam `tensor_view.vincula` binds against.
- `functio layout(numerus typo_ggml, lista<numerus> forma) → LayoutGgml ⇥
  GgufManifestError` — resolve known GGML block geometry or return
  `LayoutGgml.Ignota` for an unknown raw type ID.

`discretio GgufManifestError` variants: `FormatMala`, `VersioIgnota`,
`Truncata`, `WireMala`, `LimitesMala`, `Superfluitas`, `ClavisDuplicata`,
`TensorDuplicatum`, `OffsetMala`, `LayoutIgnota`, `IdentitasMala`, and
`FonsMala`; each carries `textus causa`.

## gradus:model/gguf

GGUF admission (PML2-U3, **D3 frozen contract** — A1C clean break). One
admitted row → schema-2 capsule. D3 deletes the dual byte wire parser and
keeps the public admission entry `admit` as a thin wrapper over
`gradus:model/gguf_manifest`: parse via `manifestum.parse`/`inspice`,
validate the pinned one-row contract through manifest accessors
(`metadatum`, `textum`, `numerum`, `inveni_tensorem`), and build the
schema-2 capsule. No alias, no forwarding, no compatibility import;
`gradus:model/gguf_manifest` is the only GGUF parse path. The wrapper
migration is A1C-M2 and is **pending in the A1C chain** — this section
documents the frozen contract, not a claim that the migration has
integrated.

- `functio causa(GgufError e) → textus` — render the typed error message.
- `functio admit(...) → capsula.Capsula ⇥ GgufError` — the GGUF row
  admission entry (D3 frozen contract; the exact parameter set is recorded
  by A1C-M2): thin schema-2 wrapper that parses via `manifestum`, validates
  the pinned one-row contract (`expectatum_*` counts) through manifest
  accessors, and admits → schema-2 capsule, fail closed on any deviation.

## gradus:model/safetensors

Safetensors admission (PML2-U2, **D4 frozen contract** — A1C clean break).
One admitted row → schema-2 capsule. D4 keeps the `admittas` entry and
returns the schema-2 capsule holding `artifact.IdentitasContenuti` +
`ManifestumSafetensors`; the Safetensors row remains an F32 structural
fixture — no real-file or quantization claims are added. The migration is
A1C-M3 and is **pending in the A1C chain** — this section documents the
frozen contract, not a claim that the migration has integrated.

- `functio causa(SafetensorError e) → textus` — render the typed error
  message.
- `functio admittas(...) → capsula.Capsula ⇥ SafetensorError` — the
  Safetensors row admission entry (D4 frozen contract; the exact parameter
  set is recorded by A1C-M3): JSON header parse → schema-2 capsule holding
  `IdentitasContenuti` + `ManifestumSafetensors`, fail closed on any
  deviation.

## gradus:model/dequant

CPU dequantization of the admitted GGML block types (PML2-U5, C3; widened
by GGUF-A3 C1 to the Qwen3.6 completion-row **union set {F32, BF16, Q5_0,
Q8_0, Q4_K, Q5_K, Q6_K}**) — exact re-expression of the GI2-1 CPU dequant
core (llama.cpp `ggml/src/ggml-quants.c` at the pinned checkout). Bit-exact
against the independent reference goldens.

The A3 additions are **BF16** (`GGML_BF16`, id 30; 1 element/block, 2
bytes/block — bf16→f32 value arithmetic via the `_potentia_duorum` seam,
bit-exact for every finite bf16; NaN fails closed `ValorMala`) and **Q5_K**
(`GGML_Q5_K`, id 13; 256 elements/block, 176 bytes/block —
`dequantize_row_q5_K`: d/dmin halves + `get_scale_min_k4` + qh[32] +
qs[128], same f32 operation order). The dequant layout constants
(`elementa_glomoris`/`octeti_glomoris`) are cross-checked against
`LayoutGgml.Cognita` at the view-binding boundary (`tensor_view.vincula`):
the manifest is the single layout authority — dequant validates admission
and never re-derives layout.

- `functio causa(DequantError e) → textus` — render the typed error message.
- `functio elementa_glomoris(numerus typo) → numerus` — block element count
  for an admitted GGML type (closed union set {F32, BF16, Q5_0, Q8_0, Q4_K,
  Q5_K, Q6_K}).
- `functio octeti_glomoris(numerus typo) → numerus` — block byte size for an
  admitted GGML type.
- `functio dequantizas_glomulus(numerus typo, lista<numerus<u8>> blocci) →
  lista<f32> ⇥ DequantError` — dequantize one block (fail closed on
  wrong-length/NaN/unknown-type).
- `functio dequantizas_ordo(numerus typo, lista<numerus<u8>> octeti) →
  lista<f32> ⇥ DequantError` — dequantize a whole row (byte length must be
  a whole multiple of block bytes).

## gradus:model/tensor_payload

Bounded per-tensor payload value and its typed diagnostics (GGUF-A3
C2-U2). One validated tensor's bounded byte payload together with the exact
stored range facts that describe it (name, absolute byte start, length). It
deliberately carries no path, URL, reader, file handle, memory map,
host/device object, or whole-model byte list — a source adapter supplies
bounded bytes separately (delivery clean boundary).

`genus TensorPayload` — fields `nomen` (descriptor name this payload binds
to), `initium_absolutum` (absolute byte offset into the content identity),
`longitudo` (exact stored byte length of these bounded bytes), `bytes`
(bounded bytes for that range).

`discretio PayloadError` variants: `NomineIgnota` (tensor name not present
in the manifest), `RangeMala` (byte range lies outside the artifact), and
`LongitudoMala` (payload length does not match the stored layout length);
each carries `textus causa`.

- `functio causa(PayloadError e) → textus` — render the typed error message.

## gradus:model/tensor_view

Bounded typed tensor view, fail-closed bind, and windowed materializer
(GGUF-A3 C2-U3 + C2-U4). `vincula` binds one descriptor + one validated
payload into the typed view; the manifest is the single layout authority —
dequant cross-checks admission (`elementa_glomoris`) and never re-derives
layout. `materializa_slicem` dequantizes an element-aligned window of a
bound view to f32 in GGUF block order, one block per source read;
`materializa_glomulum` is the single-block probe. Each payload sub-window is
exactly one block (≤ CORPUS_LIMES); no whole-tensor or whole-model read
path exists. `VisumTensoris` never retains a path, reader, or source
function.

`genus VisumTensoris` — fields `nomen` (descriptor name), `forma` (full
GGUF shape; rank 3 = expert tensor, kept explicit), `typo_ggml` (physical
storage type id), `elementa` (logical element count), `layout`
(`LayoutGgml`: `Cognita` known or `Ignota` inspectable-but-not-materializable),
`initium_absolutum` (absolute start of the tensor payload),
`longitudo_payloadis` (exact stored byte length, `Cognita.longitudo_octetorum`).

- `functio causa(VisioError e) → textus` — render the typed error message.
- `functio vincula(manifestum.ManifestumGguf m, tensor_payload.TensorPayload
  p) → VisumTensoris ⇥ VisioError` — bind one descriptor + one validated
  payload into the typed view. Fails closed on: unknown name
  (`NomineIgnota`), absolute-range mismatch — `p.initium_absolutum` must
  equal `data_inceptum + offset_relativum` — (`RangeMala`), stored-length
  mismatch vs `Cognita.longitudo_octetorum` (`LongitudoMala`), unknown
  layout (`LayoutIgnota`), and un-admitted physical type
  (`TypoIgnotum`).
- `functio materializa_slicem(VisumTensoris v, numerus initium_elementum,
  numerus longitudo_elementum, (numerus, numerus) → manifestum.LectioFontis
  fons) → lista<f32> ⇥ VisioError` — materialize one bounded logical-element
  window to f32 in GGUF block order, one block per source read. Fails closed
  on: negative/out-of-tensor/over-cap windows (`LimitesMala`; the cap is
  `MAXIMUM_SLICEM_ELEMENTA` = 16,777,216 elements = 64 MiB f32),
  block-misaligned windows (`OrdoMala`), unknown layout (`LayoutIgnota`),
  and source or block-decode failures (`RangeMala`).
- `functio materializa_glomulum(VisumTensoris v, numerus index_glomuli,
  (numerus, numerus) → manifestum.LectioFontis fons) → lista<f32> ⇥
  VisioError` — dequantize exactly one block by block index. Fails closed on
  an out-of-range block index (`LimitesMala`), unknown layout
  (`LayoutIgnota`), and source or block-decode failures (`RangeMala`).

`discretio VisioError` variants: `NomineIgnota`, `RangeMala`,
`LongitudoMala`, `LayoutIgnota`, `TypoIgnotum`, `OrdoMala`, and
`LimitesMala`; each carries `textus causa`.


## gradus:model/dense_qwen2

Typed `qwen2` (Qwen2.5) architecture adapter (REF-01-U1.7). Resolves the
canonical dense tensor-name family — `model.embed_tokens`,
`model.layers.{N}.input_layernorm`, `.self_attn.{q,k,v,o}_proj`,
`.post_attention_layernorm`, `.mlp.{gate,up,down}_proj`, `model.norm`,
`lm_head` — to the exact GGUF-A1b manifest descriptors of a qwen2 row,
with the qwen2 deltas over the llama family: lm_head tie status read from
the tensor set (`output.weight` present → untied, absent → tied; the
gi0-model-contract precedent), the GQA head config
(`qwen2.attention.head_count_kv`), and rope_theta frozen at 1000000 (the
qwen2 family fact — the float `qwen2.rope.freq_base` wire value is
preserved by the manifest but not decoded by the integer accessor). Fails
closed with typed diagnostics on unknown canonical names, unknown layer
tensor suffixes, out-of-range layer indices, tensors missing from the
manifest, and non-qwen2 manifests. Executed proof: `exempla/dense-qwen2-adapter`
prints 23 PASS / 0 FAIL (exit 0) over the pinned Qwen2.5-0.5B descriptor
facts (tied + untied lm_head rows, layer 0 and layer 23 boundary rows, and
the rejection rows).

`genus ConfiguraDensaQwen2` — fields `strata` (block count), `capita`
(head count), `capita_kv` (KV head count), `dimensio_capitis` (head_dim =
`embedding_length / head_count`), `dimensio_occulta` (embedding length),
`vocabulum` (from the token_embd shape), `theta` (rope_theta, frozen
1000000), and `ligatum` (tied embedding, from the tensor set).

- `functio causa(DenseQwen2Error e) → textus` — render the typed error
  message.
- `functio configura(manifestum.ManifestumGguf m) → ConfiguraDensaQwen2 ⇥
  DenseQwen2Error` — freeze the qwen2 architecture config from the manifest
  metadata facts. Fails closed on a non-qwen2 architecture
  (`ArchaegrammaIgnota`), unavailable metadata facts (`ConfiguraMala`), and
  a missing `token_embd.weight` (`TensorAbsens`).
- `functio resolve(ConfiguraDensaQwen2 cfg, manifestum.ManifestumGguf m,
  textus nomen) → manifestum.DescriptioTensorisGguf ⇥ DenseQwen2Error` —
  resolve one canonical tensor name to its exact manifest descriptor. Fails
  closed on unknown canonical names (`CanonicoIgnota`), unknown layer tensor
  suffixes (`CanonicoIgnota`), out-of-range layer indices
  (`StratumExtraLimitem`), and tensors missing from the manifest
  (`TensorAbsens`).
- `functio descriptio_render(manifestum.DescriptioTensorisGguf t) → textus`
  — render the resolved descriptor facts (`gguf-name/shape/layout`) for the
  executed proof and the proba pins.

`discretio DenseQwen2Error` variants: `ArchaegrammaIgnota`, `CanonicoIgnota`,
`StratumExtraLimitem`, `TensorAbsens`, and `ConfiguraMala`; each carries
`textus causa`.

## gradus:model/dense

Dense model assembly (REF-01-U1.8). `praevideo` is the complete ordered
dense forward graph — embedding gather → N ordered U1.5 blocks → final
RMSNorm → output projection — assembled from the typed architecture config
and materialized stored-weight views via canonical tensor names. The caller
supplies a resolver (`fons`) that returns the materialized STORED-weight
view for one canonical tensor name (`model.embed_tokens`,
`model.layers.{N}.input_layernorm`, `.self_attn.{q,k,v,o}_proj`,
`.post_attention_layernorm`, `.mlp.{gate,up,down}_proj`, `model.norm`,
`lm_head`) plus a layer index — the GGUF/A1b descriptor layout
(`token_embd.weight` is `[D, V]`). The assembly transposes the embedding
for the token-major gather and reuses it directly for a TIED `lm_head`; an
UNTIED row resolves `lm_head` separately. Every linear bias is synthesized
as a same-shape zero tensor (the llama/qwen2 canonical family carries no
bias weights). Zero per-row special-case constants: every shape derives
from the config and the runtime tensors. Fails closed with typed
diagnostics on unknown/missing canonical tensors, an invalid config, a
shape that contradicts the config, and token ids outside the embedding
vocabulary. Executed proof: `exempla/dense-model` prints 37 PASS / 0 FAIL
(exit 0) for a small synthetic dense config (T=2, D=16, F=16, H=4, K=2,
head_dim=4, vocab 8) with tied and untied embedding rows, plus the
fail-closed rejection row.

`genus ConfiguraDensa` — fields `strata` (block count), `capita` (head
count), `capita_kv` (KV head count), `dimensio_capitis` (head dim),
`dimensio_occulta` (hidden dim), `vocabulum` (vocabulary size), and
`ligatum` (tied embedding).

`genus Repertum` — one resolver answer: `successus` (`bivalens`), `tensorem`
(the materialized stored-weight view), and `causa` (the failure text). The
assembly maps a `successus = falsum` answer into `TensorAbsens` carrying
the resolver's causa verbatim.

- `functio causa(DenseError e) → textus` — render the typed error message.
- `functio praevideo(ConfiguraDensa cfg, (textus, numerus) → Repertum fons,
  lista<numerus> tokens, f32 epsilon, f32 scale, lista<numerus> positions,
  numerus rope_dim, attention.RopeConfigura rope_cfg) → tensor.Tensor ⇥
  DenseError` — the complete ordered dense forward graph over the staged
  carrier: embedding gather (from the transposed stored view), N ordered
  U1.5 `dense_block` rows resolved by canonical name, the final RMSNorm,
  and the output projection (tied `lm_head` reuses the stored embedding
  view; an untied row resolves `lm_head`). Fails closed on a resolver
  failure (`TensorAbsens`), an invalid architecture config (`ConfiguraMala`:
  non-positive layers/heads/KV-heads/head-dim/hidden/vocab, KV heads beyond
  the head count, a non-divisible head/KV ratio, a non-empty token
  sequence, positions/token count mismatch), a shape contradicting the
  config (`FormaMala`), and token ids outside the embedding vocabulary
  (`TerminusExcedit`).

`discretio DenseError` variants: `TensorAbsens`, `ConfiguraMala`,
`FormaMala`, and `TerminusExcedit`; each carries `textus causa`.
## gradus:model/qwen35moe

Typed qwen35moe architecture admission (MODEL-01 chain). Reads the frozen
architecture rows and the canonical tensor map from a parsed GGUF manifest
through `gradus:model/gguf_manifest`, cross-references the map against the
frozen configuration, and admits one artifact under a pathless identity
precondition. `congela` freezes the 30 frozen configuration rows and enforces
the 55-entry metadata count; the canonical map admits exactly 753 tensors
across the four family sets (3 global, 19 hybrid × 30, 16 full-attention × 10,
20 nextn on `blk.40`) with the 41-block schedule (full-attention at index
≡ 3 mod 4; `blk.40` the sole nextn block), the storage distribution
(f32 368 / q8_0 259 / q4_K 82 / q5_K 38 / q6_K 4 / bf16 2), and the per-tensor
blk.40 bf16 + blk.34/38/39 q6_K anomalies (block 40 is map-complete;
the main-pass schedule is blocks 0..39 — no nextn execution claim). Mutation
families 1–5 (frozen value changed / required key missing / extra unknown
`qwen35moe.*` key / tensor name / shape / storage / count divergence) and the
M5 cross-reference validation fail closed with a typed first-divergence
diagnostic naming the first diverging fact. `admitto` is the admission entry:
the identity precondition (SHA-256 digest + byte length against
operator-measured facts) runs before any architecture read, and the
seven-family typed refusal matrix reports every divergence. Tokenizer facts
are frozen as identity only; tokenizer execution is LIB-02's unit.

`genus ConfiguratioQwen35moe` — fields `architectura`, `typus_limaturae`,
`versio_quantificationis`, `numerus_tractuum`, `longitudo_contextus`,
`longitudo_vestimenti`, `numerus_capita`, `numerus_capita_kv`,
`longitudo_clavis`, `longitudo_valoris`, `epsilon_normae_rms`,
`basis_frequentiae`, `numerus_dimensionum_rotae`, `sectiones_rotae`,
`numerus_expertorum`, `numerus_expertorum_activorum`, `longitudo_ffn_experti`,
`longitudo_ffn_communi`, `nucleus_convolutus`, `magnitudo_status`,
`numerus_coetuum`, `gradus_temporis`, `magnitudo_interior`,
`intervallum_attentionis_plenae`, `numerus_strata_nextn`,
`exemplum_tokenizoris`, `praeparatio_tokenizoris`, `numerus_tokenum`,
`numerus_typorum_tokenum`, `numerus_concatenationum`, `eos_token_id`,
`padding_token_id`, `bos_token_id`, and `add_bos_token`.
`genus SummaTensoriorumQwen` — fields `totalis`, `globalium`, `hybridorum`,
`attentionis_plenae`, `nextn`, `stipula_f32`, `stipula_q8_0`, `stipula_q4_k`,
`stipula_q5_k`, `stipula_q6_k`, `stipula_bf16`, and `experti_rank3`.
`genus AdmissioQwen35moe` — fields `configuratio` (`ConfiguratioQwen35moe`)
and `summa` (`SummaTensoriorumQwen`).
`discretio ErrorConfiguratioQwen35moe` — `MetadatumDiversum(clavis)`.
`discretio ErrorTensorumQwen35moe` — `NomenDiversum(nomen)`,
`FormaDiversa(nomen)`, `StipulaDiversa(nomen)`, `NumerusDiversus(causa)`.
`discretio ErrorReferentiaeQwen35moe` — `NomenIgnotum(nomen)`,
`DimensioDiversa(nomen)`, `NumerusDivergens(causa)`, `AmbitusMala(causa)`.
`discretio ErrorAdmissionisQwen35moe` — `IdentitasDiversa(causa)`,
`ArchitecturaIgnota(causa)`, `TypusIgnotus(causa)`, `ConfiguratioDiversa(causa)`,
`TensorumDiversum(causa)`, `ReferentiaDiversa(causa)`, `ManifestumMala(causa)`.

- `functio causa(ErrorConfiguratioQwen35moe e) → textus` — render the
  config-freeze divergence diagnostic.
- `functio congela(manifestum.ManifestumGguf m) → ConfiguratioQwen35moe ⇥
  ErrorConfiguratioQwen35moe` — freeze the frozen configuration rows from a
  parsed manifest; enforces the 55-entry metadata count and fails closed on
  family-1 divergences, naming the first diverging key.
- `functio causa_tensorum(ErrorTensorumQwen35moe e) → textus` — render the
  tensor-map divergence diagnostic.
- `functio tensores_canonici(manifestum.ManifestumGguf m) →
  SummaTensoriorumQwen ⇥ ErrorTensorumQwen35moe` — the canonical 753-tensor
  map: the four family sets, the 41-block schedule, the storage distribution,
  the per-tensor anomalies, and the count invariants; families 2–5 fail
  closed with a typed first-divergence diagnostic.
- `functio causa_referantiae(ErrorReferentiaeQwen35moe e) → textus` — render
  the cross-reference divergence diagnostic.
- `functio referantia(ConfiguratioQwen35moe c, manifestum.ManifestumGguf m) →
  bivalens ⇥ ErrorReferentiaeQwen35moe` — M5 dimension/storage
  cross-reference validation: every canonical tensor's stored shape and
  storage row must match the frozen-configuration-derived expectations;
  divergences fail closed (name / dimension / count / range).
- `functio causa_admissionis(ErrorAdmissionisQwen35moe e) → textus` — render
  the admission refusal diagnostic.
- `functio admitto(manifestum.CorpusGguf corpus, textus digestio_exspectata,
  numerus longitudo_exspectata) → AdmissioQwen35moe ⇥ ErrorAdmissionisQwen35moe`
  — the admission entry. The identity precondition (family 6) runs before any
  architecture read; then the config freeze (family 1), the canonical tensor
  map (families 2–5), and the M5 cross-reference validation compose, with the
  family-7 unknown-architecture / unknown-raw-type refusals.
  `manifestum.parse` failures surface as `ManifestumMala`. The
  application-owned adapter `exempla/gguf-admit-qwen35moe` feeds this entry
  the bounded table-prefix corpus and prints the ADMIT receipt.

## gradus:tokenizer

Tokenizer identity — `tokenizer-identity-schema-1.0.0` (PML2-U4, council
C8). The deeper probe-parity contract the model-admission path references
(the per-format admission entries enforce its facts): pinned row
(gpt2 / BBPE, pre-tokenizer smollm, vocab 49152, merges 48900), EOG set
`{0,2}`, BOS-free / space-prefix-free, 17 control specials, and the pinned
probe fixtures (P1–P11 + the four workload id lists).

- `functio est_eog(numerus id) → bivalens` — the EOG-membership predicate:
  is `id` in the admitted EOG set `{0, 2}`? This is the **generation
  stop-policy binding** (correctness wave, `0d50d60`): generation
  terminates after the FIRST admitted EOG token — `maxima_verborum` is a
  ceiling, never a promise to emit exactly that many tokens.
- `functio causa(TokenizerError e) → textus` — render the typed error
  message.

`genus IdentitasTokenizator` — methods `schematis()`, `progenies()`,
`pre_tokenizator()`, `digestio_vocabuli()`, `eog()`, `bos_vacua()`,
`spatium_vacua()`.

- `functio proba_aequa(lista<numerus> a, lista<numerus> b) → bivalens` —
  exact id-list equality.
- `functio proba_ida(textus pinnata) → lista<numerus> ⇥ TokenizerError` —
  parse a pinned comma-separated probe fixture (unknown name fails closed).
- `functio verifica_proba(textus nomen, lista<numerus> observata) → bivalens
  ⇥ TokenizerError` — probe-parity check: observed ids must equal the pinned
  probe exactly (divergence = a DIFFERENT tokenizer, fails closed).
- `functio pinnata_proba(textus nomen) → textus ⇥ TokenizerError` — the
  pinned probe fixture text (P1–P11, correctio, brevis, normale, contextus).
- `functio structa(textus schema, textus progenies, textus pre_tokenizator,
  textus digestio_vocabuli, textus eog, bivalens bos_vacua, bivalens
  spatium_vacua) → IdentitasTokenizator ⇥ TokenizerError` — the fail-closed
  identity ADMISSION (EOG-set exact, vacua polarity `≡` — see the EOG
  note below).
- `functio verifica(IdentitasTokenizator t) → bivalens ⇥ TokenizerError` —
  consumer-side self-verification (defense in depth).
- `functio clavis_tokenizatoris(IdentitasTokenizator t) → textus ⇥
  TokenizerError` — the deterministic canonical component a host digests
  into the KV block key (MD-A9).
- `functio serializa_identitas(IdentitasTokenizator t) → textus ⇥
  TokenizerError` — identity wire form.
- `functio deserializa_identitas(textus wire) → IdentitasTokenizator ⇥
  TokenizerError` — identity from wire, fail closed.

**EOG-set admission semantics (correctness wave, `6cc0eb5` + `2cdc498`)**:
`structa` / `verifica` admit the **exact pinned EOG set `{0,2}`** (`eog ≠
EOG` fails closed with `EogMala` — a well-formed-but-different set is a
different tokenizer, contract §3.3). The pinned add-* flags are `falsum`;
`bos_vacua` / `spatium_vacua` are the positive facts — the guard is `≡`
(`bos_vacua ≡ ADD_BOS` fails closed), so only a BOS-free, space-prefix-free
row is admitted.

**Artifact-backed byte-level BPE runtime (LIB-02-U2, GGUF-A2)**: the
runtime consumes the vocab and merge arrays from a parsed schema-2
`ManifestumGguf` through the U1 array accessors (`manifestum.textorum`) and
implements the llama.cpp `llm_tokenizer_bpe` core at the **word-level
boundary** (the pre-tokenizer is identity here; U3 composes it). Display
mapping, merge semantics, and decode are pinned to the delivery's word-level
oracle rows.

`genus Tokenizator` — the artifact-backed runtime record (vocab list,
display-token → id map, `"left right"` merge-pair → rank map, vocab size).

- `functio fabricare(manifestum.ManifestumGguf m) → Tokenizator ⇥
  TokenizerError` — build the runtime from a parsed manifest. The declared
  tokenizer model must be the byte-level BPE family (`tokenizer.ggml.model`
  = `gpt2`); malformed merge entries and empty vocabs fail closed. Nothing
  is hard-coded: the vocab and merge tables come from the artifact.
- `functio encoda(Tokenizator t, textus verbum) → lista<numerus> ⇥
  TokenizerError` — word-level encode: UTF-8 bytes → gpt2 display symbols →
  ranked bigram merges (one merge at a time, ties leftmost — the pinned
  reference queue semantics) → vocab ids. A final piece missing from the
  vocab falls back to its single-byte display characters; a missing byte
  token fails closed (`VestigiumIgnotum`).
- `functio decoda(Tokenizator t, lista<numerus> ids) → textus ⇥
  TokenizerError` — word-level decode: ids → vocab display strings →
  inverse display mapping → bytes → UTF-8 text. Unknown ids
  (`IdIgnotum`), unmappable display characters (`VestigiumIgnotum`), and
  byte sequences that are not valid UTF-8 (`Utf8Mala`) fail with typed
  errors.

Pinned word-level rows (llama-tokenize 10150 `dee2a846b`): `transformers` →
`[4549, 382]`, `สวัสดี` → `[34469, 168607]`, `人工智能` → `[109015]`, each
decoding back to the exact input text.

**Composed full-prompt runtime (LIB-02-U3, GGUF-A2)**: the qwen35
pre-tokenizer scanner and the policy surfaces compose the word-level BPE
core into a full-prompt encode/decode path.

`discretio CategoriaUnicode` (`Littera` / `Signum` / `Numerus` / `Spatium`
/ `NovumLinea` / `Aliud`) is the scanner-relevant character classification
(U3-1). The category tables cover the probe-relevant classes: `\p{L}`
(Basic Latin, Latin-1 Supplement, Thai, CJK), `\p{M}` (Thai vowel/tone
signs), `\p{N}` (ASCII + Thai digits), the space and newline families.

- `functio categoria(textus c) → CategoriaUnicode` — classify one character
  against the category tables (a character outside every table is `Aliud`).
- `functio categoria_nomen(textus c) → textus` — canonical category name
  (`littera` / `signum` / `numerus` / `spatium` / `novum_linea` / `aliud`);
  the textus→textus seam the proba/consumer rows use.
- `functio est_littera(textus c) → bivalens` — `\p{L}` membership.
- `functio est_signum(textus c) → bivalens` — `\p{M}` membership.
- `functio est_numerus(textus c) → bivalens` — `\p{N}` membership.
- `functio est_spatium(textus c) → bivalens` — whitespace membership.
- `functio est_novum_linea(textus c) → bivalens` — `[\r\n]` membership.
- `functio est_aliud(textus c) → bivalens` — the remaining class: the
  punct/emoji/symbol runs the scanner splits as edge groups (U3-3). The
  ASCII contractions are a separate scanner arm (matched as literal text,
  not by category).

- `functio scanna_verba(textus textum) → lista<textus> ⇥ TokenizerError` —
  the qwen35 pre-tokenizer word split (Unicode-category scanner, U3-1..U3-3):
  letter/mark/digit runs, whitespace and newline families, punct/emoji
  groups with an optional leading space, and the ASCII contractions.
- `functio encoda_promptum(Tokenizator t, textus textum) → lista<numerus> ⇥
  TokenizerError` — full-prompt encode, parse-special off: every word goes
  through `scanna_verba` + `encoda` (specials read as their literal bytes).
- `functio encoda_promptum_specialia(Tokenizator t, textus textum) →
  lista<numerus> ⇥ TokenizerError` — full-prompt encode, parse-special on:
  split the prompt on the artifact special cache before the scanner (earliest
  match, longest text on ties), emit each special's single id, scan each
  plain slice independently. Identical to `encoda_promptum` when the prompt
  has no specials.
- `functio eog_artificii(Tokenizator t) → lista<numerus>` — the runtime EOG
  stop set (ascending): the declared eos id plus every vocab token whose text
  is in the reference EOG name list and the FIM pad/rep/sep ids (U3-5).
- `functio est_eog_artificii(Tokenizator t, numerus id) → bivalens` — EOG
  membership on the runtime set.
- `functio add_bos(Tokenizator t) → bivalens` — the artifact's
  `tokenizer.ggml.add_bos_token` (absent → falsum; encode is BOS-free).
- `functio chat_template(Tokenizator t) → textus` — the artifact's
  `tokenizer.chat_template` (absent → empty); `redde_turnum_user(t, content)`
  renders the minimal Qwen3-ChatML user turn (U3-6).

**LIB-02 completion oracle (U3-7)**: the fully composed runtime encodes
Probe A `สวัสดีครับ ผมชื่ออเล็กซ์` → `[34469, 168607, 153295, 173922,
153380, 22216, 151752, 172769]` and Probe B `你好，世界！今天是2026年8月13日
🎉` → `[109266, 3709, 96748, 6115, 113128, 17, 15, 17, 21, 95859, 23,
96212, 16, 18, 95971, 10838, 236, 231]` (raw-prompt rows, never through the
template), and both decode back to the exact prompts. Pinned rows and the
divergence-receipt form: `fixtures/tokenizer/pinned-probe-oracle.md`;
bound in `src/tokenizer.proba` (`"LIB-02-U3-7 full two-probe composition +
divergence receipts"` probandum).

**Capstone tokenizer phase (LIB-02-U4-1)**: the capstone application
`exempla/qwen36-35b-inference` (M6-U1 admission scaffold) runs the
tokenizer phase through the public surface — `fabricare` on the admitted
artifact manifest, then `encoda_promptum` for both pinned probes and
`decoda` for both id lists (raw-prompt rows, never through the template) —
and prints PASS rows when the observed rows equal the pinned oracle. A
divergence names the first divergent id/character and fails closed
(campaign rule 5); the exempla never hard-codes probe ids.

## gradus:cache

KV-cache values and mutation rules (PML5-U2). `KVCache` is the per-session
key/value state the decode serves: one K/V pair per layer (the gradus row
is a single transformer block — `stratorum = 1`), each `[positions,
dimensio]` f32 staged, plus the exact token history and the identity
fields. No device handle, no physical residency, no performance claims.

- `functio causa(CacheError e) → textus` — render the typed error message.

`genus KVCache` — methods `model()`, `versio_modelis()`, `configuratio()`,
`tokenizator()`, `historia()`, `stratorum()`, `typo()`, `ordinatio()`
("staged"), `clavis()`, `valor()`, `versio()` (generation — mutation
counter, starts at 1, bumps per append), `dimensio()`, `longitudo()`
(position count == history length); plus:

- `functio cache_aequus(KVCache a, KVCache b) → bivalens` — field-wise
  equality.
- `functio cache_vacua(textus model, textus versio_modelis, textus
  configuratio, textus tokenizator, numerus stratorum, numerus dimensio) →
  KVCache ⇥ CacheError` — fresh empty cache (identity fields, empty history
  and K/V, versio 1).
- `functio appende(KVCache c, numerus token_id, tensor.Tensor clavis,
  tensor.Tensor valor) → KVCache ⇥ CacheError` — append exactly ONE position
  and one history token; strictly sequential (no gaps/duplicates/
  reordering); bumps versio.
- `functio redintegra(KVCache c) → KVCache ⇥ CacheError` — reset: same
  identity, empty history and K/V, versio 1.

`genus IdentitasCache` (the cache identity key) — methods `model()`,
`versio_modelis()`, `configuratio()`, `tokenizator()`, `historia()`,
`positio()`, `stratorum()`, `typo()`, `ordinatio()`; plus:

- `functio identitas_cache_aequus(IdentitasCache a, IdentitasCache b) →
  bivalens` — field-wise equality.
- `functio identitas_cache(KVCache c) → IdentitasCache` — derive the
  identity record.
- `functio serializa_identitas(IdentitasCache i) → textus` — versioned wire
  form (empty-prefix segment sentinel "-").
- `functio deserializa_identitas(textus wire) → IdentitasCache ⇥ CacheError`
  — identity from wire, fail closed.

## gradus:decode

Decode-loop semantics (PML5-U1). One-token decode over the shared forward
row (embedding gather → transformer block mode 2 → output projection),
multi-token prefill over the SAME forward functions, explicit session
positioning, reset, context-limit reject policy (never silent truncation),
and cancellation observation.

- `functio causa(DecodeError e) → textus` — render the typed error message.

`genus Pondera` — the transformer block's weights (mirrors
`transformer_block` argument order) — methods `ln1_s()`, `ln1_o()`, `wq()`,
`bq()`, `wk()`, `bk()`, `wv()`, `bv()`, `wo()`, `bo()`, `ln2_s()`,
`ln2_o()`, `wf1()`, `bf1()`, `wf2()`, `bf2()`, `ln3_s()`, `ln3_o()`; plus
`functio structa_pondera(tensor.Tensor ln1_s, tensor.Tensor ln1_o,
tensor.Tensor wq, tensor.Tensor bq, tensor.Tensor wk, tensor.Tensor bk,
tensor.Tensor wv, tensor.Tensor bv, tensor.Tensor wo, tensor.Tensor bo,
tensor.Tensor ln2_s, tensor.Tensor ln2_o, tensor.Tensor wf1, tensor.Tensor
bf1, tensor.Tensor wf2, tensor.Tensor bf2, tensor.Tensor ln3_s,
tensor.Tensor ln3_o) → Pondera`.

`genus Decodere` — the decode machine — methods `mensa()` (embedding table
[vocabulum, dimensio]), `pondera()`, `projectio()`, `projectio_bias()`,
`scala()`, `vocabulum()`, `contextus()` (position limit), `dimensio()`;
plus:

- `functio structa_decodere(tensor.Tensor mensa, Pondera pondera,
  tensor.Tensor projectio, tensor.Tensor projectio_bias, f32 scala, numerus
  vocabulum, numerus contextus, numerus dimensio) → Decodere ⇥ DecodeError`
  — validated constructor (fail closed on inconsistent shapes).
- `functio decodere_datum(numerus token_id, numerus positio, Decodere m) →
  tensor.Tensor ⇥ DecodeError` — the explicit one-token decode op: token id
  + position → full-vocabulary logits.
- `functio praefundere(lista<numerus> tokens, Decodere m) → tensor.Tensor ⇥
  DecodeError` — multi-token teacher-forced prefill over the SAME forward
  functions.

`genus Sessio` — the explicit position counter — methods `positio()`,
`contextus()`; plus:

- `functio sessio_fresh(numerus contextus) → Sessio ⇥ DecodeError` — fresh
  session at position 0.
- `functio progredere(Sessio s) → Sessio ⇥ DecodeError` — advance by one
  (fails closed at the context limit).
- `functio redintegra(Sessio s) → Sessio` — reset to position 0 (context
  preserved).

`genus Cancelatum` — the cancellation flag — method `cancellata()`; plus:

- `functio cancelatum_fresh() → Cancelatum` — not cancelled.
- `functio cancelatum_cancellata() → Cancelatum` — cancellation requested.
- `functio observa_cancellationem(Cancelatum c) → Cancelatum ⇥ DecodeError`
  — the loop's cancellation check (throws `Cancelata` when requested).
- `functio replica(lista<lista<f32>> logita, sampling.Configura c,
  lista<numerus> historia, train.Semen semen, Cancelatum cancelatum) →
  lista<numerus> ⇥ DecodeError` — the batched replica loop: draws one token
  per logit row through `sampling.sors`, feeding each row's result into the
  next row's history/seed (deterministic; EOG-stop is the caller's loop
  policy via `tokenizator.est_eog`).

## gradus:sampling

Sampling semantics (PML5-U3). Pure, deterministic pipeline: repetition
penalty → temperature → top-k → softmax → top-p → min-p → renorm → draw.
`temperatura ≤ 0` is the GREEDY path (exact argmax, unchanged Semen).
Tie-breaks and order are part of the oracle contract (first-index ties
throughout).

- `functio causa(SamplingError e) → textus` — render the typed error
  message.

`genus Configura` — the sampling knobs — methods `temperatura()`, `top_k()`,
`top_p()`, `min_p()`, `poena_repetitionis()`; plus `functio
structa_configura(f32 temperatura, numerus top_k, f32 top_p, f32 min_p, f32
poena_repetitionis) → Configura ⇥ SamplingError`.

`genus Sortitio` — the draw outcome — methods `token_id()`, `semen()`
(advanced generator state); plus:

- `functio maxima(lista<f32> logits) → numerus ⇥ SamplingError` — exact
  argmax (first-index ties; greedy path).
- `functio distributio(lista<f32> logits, Configura c, lista<numerus>
  historia) → lista<f32> ⇥ SamplingError` — the probability distribution
  after the full filter pipeline.
- `functio sors(lista<f32> logits, Configura c, lista<numerus> historia,
  train.Semen semen) → Sortitio ⇥ SamplingError` — the draw: greedy when
  `temperatura ≤ 0`, else deterministic inverse-CDF sampling; logits must be
  non-empty and finite; history tokens in `[0, logits.longitudo())`.

## gradus:generation

Generation-configuration contract (PML5-U4) — the single authority for
generation configuration, with validated construction and the generation
cursor (U5).

- `functio causa(GeneratioError e) → textus` — render the typed error
  message.

`genus GeneratioConfigura` — the nine-field config — methods `contextus()`
(context length), `magna_promptus()` (prefill batch), `maxima_verborum()`
(max generated tokens; ≤ contextus), `semen()` (seed ≥ 1), `temperatura()`
(0 = greedy), `top_k()`, `top_p()`, `min_p()`, `poena_repetitionis()`; plus:

- `functio generatio_aequus(GeneratioConfigura a, GeneratioConfigura b) →
  bivalens` — field-wise equality.
- `functio structa_generatio(numerus contextus, numerus magna_promptus,
  numerus maxima_verborum, numerus semen, f32 temperatura, numerus top_k,
  f32 top_p, f32 min_p, f32 poena_repetitionis) → GeneratioConfigura ⇥
  GeneratioError` — the validated constructor (single authority; fail
  closed).
- `functio generatio_defecta(numerus contextus, numerus magna_promptus,
  numerus maxima_verborum, numerus semen) → GeneratioConfigura ⇥
  GeneratioError` — defaults for the sampling knobs (temperatura 1.0, top_k
  0, top_p 1.0, min_p 0, poena 1.0).
- `functio imperia_subsidia() → lista<textus>` — the supported knob names
  (the deterministic mapping's domain).
- `functio imperium_admissum(textus nomen) → bivalens` — knob-name
  predicate.
- `functio configura(GeneratioConfigura g) → sampling.Configura ⇥
  GeneratioError` — the deterministic mapping to the sampling config.
- `functio semen(GeneratioConfigura g) → train.Semen ⇥ GeneratioError` — the
  seed mapped to the RNG state.
- `functio serializa_generatio(GeneratioConfigura g) → textus` — config wire.
- `functio deserializa_generatio(textus wire) → GeneratioConfigura ⇥
  GeneratioError` — config from wire, fail closed.

`genus GenereCursor` — the generation loop's explicit state — methods
`sessio()` (the decode session), `prolata()` (generated-token count); plus:

- `functio cursor_fresh(GeneratioConfigura g) → GenereCursor ⇥
  GeneratioError` — fresh cursor at position 0, count 0.
- `functio verbum_licet(GeneratioConfigura g, GenereCursor c) → bivalens` —
  the explicit limit-policy predicate (below context AND below
  maxima_verborum).
- `functio cursor_progredere(GeneratioConfigura g, GenereCursor c) →
  GenereCursor ⇥ GeneratioError` — advance; REJECTS (never truncates) with a
  typed `Terminus` when the step would exceed either limit.
- `functio cursor_redintegra(GenereCursor c) → GenereCursor` — reset to the
  fresh state (session position 0, count 0).

## gradus:gradus

The package facade (no genera). Convenience surface for the MLP forward +
loss over the staged carrier.

- `functio causa(GradusError e) → textus` — render the typed error message.
- `functio forward_mlp(tensor.Tensor x, tensor.Tensor w1, tensor.Tensor b1,
  tensor.Tensor w2, tensor.Tensor b2) → tensor.Tensor ⇥ GradusError` —
  two-layer MLP forward over the staged carrier.
- `functio nil() → vacuum` — empty marker (no-op forward).
- `functio forward_mlp_loss(tensor<f32, [4,4]> input, tensor<f32, [4,4]>
  weight1, tensor<f32, [4,4]> bias1, tensor<f32, [4,4]> weight2,
  tensor<f32, [4,4]> bias2, tensor<f32, [4,4]> target) → f32` — the
  fixed-shape MLP forward + MSE loss convenience row.

## gradus:data

Data-loading facade — **stub** (no public functions yet). Batching,
shuffling, and tokenization are declared future concerns
(`gradus:data/batch`, `gradus:data/token`). Data loading is separate from
training; the Shakespeare corpus and a future safetensors dataset feed the
same training loop through the same batch interface.

---

## Coverage check

```bash
cd /Users/ianzepp/work/faberlang/gradus
./scripta/inventory-public-symbols   # per-module counts + the tracked total +
                                     # the committed coverage gate: every
                                     # public symbol below is documented here
```

The inventory script asserts every live module's `functio` count, the live
all-module tracked total, and — per module — that every public symbol name
listed above appears in this reference's `### gradus:<module>` section. A
public symbol added to `src/` without a matching entry here fails the
script (zombie-doc gate, PML6-U1). Private `_`-prefixed helpers are exempt;
the two renamed serialize readers are documented for the correctness-wave
reconciliation.

**Function-count total: 704 (re-baselined).** The A1C capsule rewrite (M1)
and the D3/D4 caller migrations (M2/M3) changed the `model/capsule`,
`model/gguf`, and `model/safetensors` counts, LIB-02-U1 added the
`textorum`/`numerorum` array accessors on `model/gguf_manifest`, and
GGUF-A3 (C2/C3) added the `model/tensor_payload`/`model/tensor_view`
modules plus the widened `model/dequant` codec surface and the LIB-02-U2
tokenizer runtime. The REF-01 wave batches added the `dense_llama`/
`dense_qwen2` architecture adapters, the multi-head GQA attention row, the
generic dense transformer block, and the `model/dense` dense model
assembly module (REF-01-U1.8). The tracked all-module total is re-baselined
and asserted by the inventory script (704); the former 585/618/611 no
longer hold and are not restated.
