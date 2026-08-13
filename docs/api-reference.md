# Gradus API Reference

**Version**: `gradus-api-reference v1.0.0` (re-baselined 2026-08-11, PML6-U1)
**Repo**: gradus · **Scope**: the live post-PML1–5 + correctness-wave public
`gradus:*` surface as committed on the `factory/hand-4` branch.
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
- `functio causa(DTypeError e) → textus` — render the typed error message.
- `functio nomen(DType t) → textus` — canonical dtype name ("f32", …).
- `functio ex_nomine(textus s) → DType ⇥ DTypeError` — tag from name;
  unknown name fails closed (`NomenIgnotum`).
- `functio amplitudo(DType t) → numerus` — element width in bytes.
- `functio serializa(DType t) → textus` — serialized tag form.
- `functio deserializa(textus s) → DType ⇥ DTypeError` — tag from wire.
- `functio promovet(DType a, DType b) → bivalens` — lossless widening
  relation (F16→F32, U8→F16/I32/F32, identity pairs).
- `functio angusta(DType a, DType b) → bivalens` — narrowing relation
  (round + range-check; overflow is a typed error).
- `functio finita(f32 x) → bivalens` — finite check (no NaN/±Inf).
- `functio casta(f32 valor, DType origo, DType scopum) → f32 ⇥ DTypeError`
  — elementwise cast per the round rule, fail closed on overflow /
  non-finite.

## gradus:shape

Shape rules — broadcast, reshape, expand, bounded product (PML1-U3, CTO-2).
The 65536 per-dimension cap is a capsule/support-row admission fact
(`pml0-model-capsule-contract.md` §5 row 5), **not** a general math limit;
general checked arithmetic admits 128k–152k vocab rows.

- `functio causa(FormaError e) → textus` — render the typed error message.
- `functio valet(lista<numerus> forma) → bivalens` — shape validity
  (non-negative dims).
- `functio gradus(lista<numerus> forma) → numerus` — rank (dimension count).
- `functio quantitas(lista<numerus> forma) → numerus ⇥ FormaError` — element
  count (product; `[]` → 1), fail closed on negative dims; the ONE
  validator tensor construction routes through.
- `functio broadcastum(lista<numerus> a, lista<numerus> b) → lista<numerus>
  ⇥ FormaError` — broadcast shape; incompatible ranks/dims fail closed.
- `functio reformanda(lista<numerus> forma, lista<numerus> novus) →
  lista<numerus> ⇥ FormaError` — reshape, element-count-preserving, fail
  closed otherwise.
- `functio expansio(lista<numerus> forma, numerus ad_gradum) →
  lista<numerus> ⇥ FormaError` — expand (broadcast up) to a higher rank.

## gradus:tensor

Plain tensor construction/shape/ops on the staged carrier — explicitly **not**
autograd-aware (PML1-U1). `Tensor` carries a dtype tag, a runtime dimension
list, and flat row-major `f32` data.

`genus Tensor` — methods:

- `functio figura() → lista<numerus>` — runtime shape.
- `functio gradus() → numerus` — rank.
- `functio quantitas() → numerus` — element count.
- `functio typus() → dtype.DType` — dtype tag.
- `functio valet() → bivalens` — consistency predicate (flat length == shape
  product; dims non-negative).
- `functio accipe(lista<numerus> indices) → f32 ⇥ TensorError` — validated
  element access (row-major stride walk; rank/index/empty violations fail
  closed).

Free functions:

- `functio causa(TensorError e) → textus` — render the typed error message.
- `functio structa(lista<f32> datos, lista<numerus> forma) → Tensor ⇥
  TensorError` — validated construction (dtype F32).
- `functio structa_typo(lista<f32> datos, lista<numerus> forma, dtype.DType
  typo) → Tensor ⇥ TensorError` — validated construction with a dtype.
- `functio impleta(lista<numerus> forma, f32 valor) → Tensor ⇥ TensorError`
  — filled tensor (all elements `valor`).

## gradus:math

Pure operation families over the production tensor surface (PML1-U4) —
construction, elementwise, reduce, matmul, cast, concat/slice. Every failure
is a typed `MathError`. Promotion is explicit (`casta`), never implicit;
division by zero follows f32 semantics (±Inf/NaN, representable in F32).

- `functio causa(MathError e) → textus` — render the typed error message.
- `functio structa(lista<f32> datos, lista<numerus> forma) → tensor.Tensor ⇥
  MathError` — validated construction mapped onto the family vocabulary.
- `functio add(tensor.Tensor a, tensor.Tensor b) → tensor.Tensor ⇥ MathError`
  — elementwise add (broadcast per `forma.broadcastum`).
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
- `functio summa(tensor.Tensor t, numerus axis) → tensor.Tensor ⇥ MathError`
  — reduce sum over one axis (axis ∈ [0, rank); zero-length axis fails
  closed).
- `functio media(tensor.Tensor t, numerus axis) → tensor.Tensor ⇥ MathError`
  — reduce mean over one axis.
- `functio matmul(tensor.Tensor a, tensor.Tensor b) → tensor.Tensor ⇥
  MathError` — rank-2 × rank-2 matmul ([M,K] × [K,N] → [M,N]).
- `functio casta(tensor.Tensor t, textus nomen) → tensor.Tensor ⇥ MathError`
  — elementwise value cast by dtype name ("f32"/"f16"/"i32"/"u8").
- `functio concatenatio(lista<tensor.Tensor> partes, numerus axis) →
  tensor.Tensor ⇥ MathError` — join along one axis (equal rank/dtype/shape
  except the axis).
- `functio segmentum(tensor.Tensor t, numerus axis, numerus initium, numerus
  finis) → tensor.Tensor ⇥ MathError` — slice with closed-open bounds
  `[initium, finis)`.

## gradus:parameter

Parameter identity and traversal — `parameter-identity-schema-1.0.0`
(PML1-U5). Explicit `(nomen, possessor, versio)` identity, trainable/frozen
status, mutation rules, and registry traversal.

- `functio statio_nomen(Statio s) → textus` — "trainable" | "frozen".
- `functio causa(ParametrumError e) → textus` — render the typed error
  message.

`genus Identitas` — `nomen`, `nomen_typi`, `figura`, `versio`, `possessor`
methods; plus `functio identitas_aequus(Identitas a, Identitas b) →
bivalens` (field-wise identity equality).

`genus Parametrum` — methods `identia()`, `statio()`, `nomen()`,
`nomen_typi()`, `figura()`, `versio()`, `possessor()`, `quantitas()`,
`valor()`; plus:

- `functio est_trainabilis(Parametrum p) → bivalens` — not frozen.
- `functio est_gelida(Parametrum p) → bivalens` — frozen.
- `functio structa(textus nomen, textus possessor, textus typo_nomen,
  lista<numerus> forma, lista<f32> datos) → Parametrum ⇥ ParametrumError` —
  validated trainable constructor.
- `functio structa_gelida(textus nomen, textus possessor, textus typo_nomen,
  lista<numerus> forma, lista<f32> datos) → Parametrum ⇥ ParametrumError` —
  validated frozen constructor.
- `functio muta(Parametrum p, lista<f32> datos) → Parametrum ⇥
  ParametrumError` — values-only mutation; bumps `versio` by 1.

`genus Registrum` — methods `numerus()`, `contineo(possessor, nomen)`,
`inveni(possessor, nomen)` (fail closed on a miss), `trainabiles()`,
`gelidae()`, `ordo()` (trainables first, then frozen, insertion order); plus:

- `functio registrum_vacuum() → Registrum` — empty registry.
- `functio adscisco(Registrum r, Parametrum p) → Registrum ⇥
  ParametrumError` — append (duplicate identity fails closed).
- `functio serializa(Identitas i) → textus` — identity wire form.
- `functio deserializa(textus s) → Identitas ⇥ ParametrumError` — identity
  from wire, fail closed.

## gradus:serialize

Versioned bytes serialization contract — `serialize-schema-1.0.0` (PML1-U7).
dtype/shape/tensor/parameter wire forms; exact round-trip; version rejection
and fail-closed reads (capsule rule — no best-effort partial reads).

- `functio causa(SerializeError e) → textus` — render the typed error
  message.

`genus Tensum` (deserialized tensor) — methods `typo()`, `figura()`,
`datos()`.
`genus ParametrumWire` (deserialized parameter) — methods `nomen()`,
`possessor()`, `typo()`, `figura()`, `versio()`, `statium()`, `datos()`.

- `functio serializa_dtype(textus typo_nomen) → octeti ⇥ SerializeError` —
  dtype wire.
- `functio serializa_shape(lista<numerus> forma) → octeti ⇥ SerializeError` —
  shape wire (i64be dims; element ceiling 1e9, no per-dim 65536 cap — the
  CTO-2 mirror alignment).
- `functio serializa_tensor(lista<f32> datos, lista<numerus> forma, textus
  typo_nomen) → octeti ⇥ SerializeError` — tensor wire.
- `functio serializa_parametrum(textus nomen, textus possessor, textus
  typo_nomen, lista<numerus> forma, numerus versio, textus statio_nomen,
  lista<f32> datos) → octeti ⇥ SerializeError` — parameter wire.
- `functio deserializa_dtype(octeti wire) → textus ⇥ SerializeError` —
  dtype name from wire.
- `functio deserializa_shape(octeti wire) → lista<numerus> ⇥ SerializeError`
  — shape from wire.
- `functio deserializa_tensor(octeti wire) → Tensum ⇥ SerializeError` —
  tensor from wire.
- `functio deserializa_parametrum(octeti wire) → ParametrumWire ⇥
  SerializeError` — parameter from wire.

**Correctness-wave rename (2026-08-09, `3c295c0`)**: the big-endian readers
were renamed `_le4/_le8` → `_be4_lege/_be8_lege` (the old little-endian
names were misleading for big-endian readers). These are `@ privata`
helpers, not public API — no external migration — but they are the shipped
surface's readers and are recorded here for the correctness-wave
reconciliation:

- `functio _be4_lege(lista<numerus<u8>> b, numerus off) → numerus` — read a
  big-endian u32 at `off`.
- `functio _be8_lege(lista<numerus<u8>> b, numerus off) → numerus` — read a
  big-endian i64 at `off`.

## gradus:gradient

The gradient-call contract (PML4-U2) — compiler-generated backward
companions invoked through ONE public entry. Pure calculus: no imports from
loss/optimize/nn/attention/transformer. Parameter identity enters as plain
`(possessor, nomen, versio)` fields.

- `functio causa(GradienteError e) → textus` — render the typed error
  message.

`genus Gradiente` (per-parameter gradient bundle slot) — methods
`possessor()`, `nomen()`, `versio()` (generation — the parameter versio at
gradient computation), `valor()`; plus `functio structa(textus nomen,
textus possessor, numerus versio, tensor.Tensor valor) → Gradiente ⇥
GradienteError`.

`genus Gradientes` — methods `numerus()`, `inveni(possessor, nomen)` (fail
closed on a miss); plus `functio structa_gradientes(lista<Gradiente>
gradientes) → Gradientes`.

- `functio obsoletus(Gradiente g, numerus versio_currens) → bivalens` —
  staleness predicate: a stored gradient is provably stale once the
  parameter has been mutated past its generation.
- `functio nil() → vacuum` — empty marker (no-op forward).
- `functio simple_loss(tensor<f32, [2,2]> x, tensor<f32, [2,2]> w) → f32` —
  the annotated forward (linear regression 2×2 seam).
- `functio gradientes_simple_loss(tensor<f32, [2,2]> x, tensor<f32, [2,2]>
  w, f32 upstream, textus nomen, textus possessor, numerus versio) →
  Gradientes ⇥ GradienteError` — the ONE public companion-call entry: runs
  the compiler-generated backward and pairs every gradient with its
  parameter identity + generation.

## gradus:loss

Loss functions (PML4-U1) — production shape-generic `mse` + `cross_entropy`
over the staged carrier, plus the three admitted fixed-shape MSE rows (same
formula, one documented `mean((p − t)²)`). Every failure is a typed
`LossError`.

- `functio causa(LossError e) → textus` — render the typed error message.
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
The update is the accepted SGD row `param' = param − lentus·grad`, applied
via `parameter.muta` (versio bump). State identity ≡ parameter identity;
stale/frozen/identity-mismatched gradients fail closed.

- `functio causa(OptimizeError e) → textus` — render the typed error
  message.

`genus SgdStatum` (per-parameter state slot) — methods `possessor()`,
`nomen()`, `versio()`, `generatio()` (parameter versio at the last applied
step), `passus()` (applied step count), `lentus()` (learning rate); plus:

- `functio statum_aequus(SgdStatum a, SgdStatum b) → bivalens` — field-wise
  equality.
- `functio structa(textus nomen, textus possessor, numerus generatio, f32
  lentus) → SgdStatum ⇥ OptimizeError` — validated slot constructor.

`genus Sgd` (optimizer state) — methods `numerus()`, `contineo(possessor,
nomen)`, `inveni(possessor, nomen)` (fail closed); plus:

- `functio sgd_aequus(Sgd a, Sgd b) → bivalens` — field-wise equality.
- `functio sgd_vacuum() → Sgd` — empty optimizer.
- `functio adscisco(Sgd o, SgdStatum s) → Sgd ⇥ OptimizeError` — register a
  slot.

`genus Passus` (step outcome) — methods `novus()` (the updated parameter,
versio bumped), `statum()` (the advanced state slot); plus:

- `functio passus(SgdStatum s, parametrum.Parametrum p, gradient.Gradiente
  g) → Passus ⇥ OptimizeError` — the ONLY mutation: applies the SGD update,
  fail closed on identity/staleness/frozen/shape violations.
- `functio serializa_statum(SgdStatum s) → textus` — slot wire
  (`optimizer/sgd-state/1.0.0/...`).
- `functio deserializa_statum(textus wire) → SgdStatum ⇥ OptimizeError` —
  slot from wire.
- `functio serializa(Sgd o) → textus` — full optimizer wire
  (`optimizer/sgd/1.0.0/<count>;...`).
- `functio deserializa(textus wire) → Sgd ⇥ OptimizeError` — optimizer from
  wire; round-trip exact by `sgd_aequus`.

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
- `functio causa(NnError e) → textus` — render the typed error message.
- `functio linear(tensor.Tensor x, tensor.Tensor w, tensor.Tensor b) →
  tensor.Tensor ⇥ NnError` — shape-generic linear (`x·w + b`; b per-channel
  [N] or same-shape [M,N]).
- `functio gelu(tensor.Tensor x) → tensor.Tensor ⇥ NnError` — shape-generic
  GELU (tanh approximation, self-hosted).
- `functio layernorm(tensor.Tensor x, tensor.Tensor scale, tensor.Tensor
  offset, f32 epsilon) → tensor.Tensor ⇥ NnError` — shape-generic LayerNorm
  over the last axis.

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
  staged carrier.
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
- `functio causa(TrainError e) → textus` — render the typed error message.

`genus Schedula` (LR schedule) — methods `lentus_vertex()`, `incalesco()`
(warmup steps), `passus_total()` (decay horizon), `lentus_finis()`; plus:

- `functio structa_schedula(f32 lentus_vertex, numerus incalesco, numerus
  passus_total, f32 lentus_finis) → Schedula ⇥ TrainError` — validated
  constructor.
- `functio lentus_schedulata(Schedula s, numerus passus) → f32 ⇥ TrainError`
  — linear warmup → cosine decay to `lentus_finis`.

Mode:

- `functio modus_nomen(Modus m) → textus` — mode name ("disciplina" |
  "aestimatio").
- `functio est_disciplina(Modus m) → bivalens` — training-mode predicate.
- `functio est_aestimatio(Modus m) → bivalens` — evaluation-mode predicate.
- `functio modus(textus nomen) → Modus ⇥ TrainError` — mode from name, fail
  closed.
- `functio dropout_pars(Modus m, f32 rate) → f32 ⇥ TrainError` — the
  dropout pass probability in the given mode (1.0 in evaluation mode).

RNG (xorshift64, the Semen rule: nonzero state; 0 degenerates and fails
closed):

`genus Semen` — method `status()`; plus `functio structa_semen(numerus
semen) → Semen ⇥ TrainError`.
`genus Fructus` (integer draw) — methods `valor()`, `semen()`; plus
`functio proximus(Semen s) → Fructus`.
`genus FructusF32` (unit draw) — methods `valor()` (∈ [0,1)), `semen()`;
plus `functio proximus_f32(Semen s) → FructusF32`.
`genus Excutio` (masked tensor + advanced state) — methods `valor()`,
`semen()`; plus:

- `functio excutio(tensor.Tensor x, Semen s, Modus m, f32 rate) → Excutio ⇥
  TrainError` — dropout application.
- `functio serializa_semen(Semen s) → textus` — RNG state wire.
- `functio deserializa_semen(textus wire) → Semen ⇥ TrainError` — RNG state
  from wire.

Checkpoint `Tabula` (PML4-U6):

`genus Tabula` — methods `aetas()` (epoch), `passus()` (step in epoch),
`rng()` (Semen), `statum_wire()` (embedded optimizer-state wire); plus:

- `functio structa_tabula(numerus aetas, numerus passus, Semen rng, textus
  statum_wire) → Tabula ⇥ TrainError` — validated constructor.
- `functio tabula_aequus(Tabula a, Tabula b) → bivalens` — field-wise
  equality.
- `functio serializa_tabula(Tabula c) → textus` — checkpoint wire.
- `functio deserializa_tabula(textus wire) → Tabula ⇥ TrainError` —
  checkpoint from wire, fail closed.

## gradus:metrics

Defined metric values with a deterministic contract (PML4-U5) —
`accuratezza` is top-1 classification accuracy with documented tie-breaks;
`Metricum` is the per-step loss + accuracy record.

- `functio causa(MetricError e) → textus` — render the typed error message.
- `functio accuratezza(tensor.Tensor prediction, tensor.Tensor target) → f32
  ⇥ MetricError` — (1/N)·Σ_n [argmax_c pred[n,c] == target[n]]; ties go to
  the LOWEST class index; deterministic, no RNG.

`genus Metricum` — methods `damnum()`, `accuratezza()`; plus:

- `functio metricum(f32 damnum, f32 accuratezza) → Metricum ⇥ MetricError` —
  validated record (finite loss, accuracy ∈ [0, 1]).
- `functio metrica_aequus(Metricum a, Metricum b) → bivalens` — field-wise
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
PML2-U1, `capsule-schema-1.0.0`). Six field groups (validated bytes,
cryptographic identity, tokenizer identity, quantization, bounds, and
architecture facts) + provenance path + the schema-versioned identity
record. Admission is fail-closed by every field.

- `functio causa(AdmissionError e) → textus` — render the typed error
  message.

`genus BytesValida` — methods `corpus()`, `longitudo()`, `opertum()`.
`genus IdentitasCrypto` — methods `algorithmus()` (admitted: sha-256),
`digestio()`.
`genus IdentitasTokenizer` — methods `progenies()`, `pre_tokenizator()`,
`digestio_vocabuli()`, `eog()`, `bos_vacua()`, `spatium_vacua()`.
`genus Quantizatio` — methods `typo()`, `elementa_glomoris()`,
`octeti_glomoris()`, `concordatio()`.
`genus Limites` — methods `machina()`, `kv()`, `tensores()`, `nomen()`,
`dimensio()`, `elementa()`, `textus()`.
`genus Architectura` — methods `identificator()`, `densitas()`, `strata()`,
`contextus()`.
`genus Identitas` — methods `schematis()`, `algorithmus()`, `digestio()`,
`longitudo_bytes()`, `quantizatio()`, `architectura()`, `strata()`.
`genus Capsula` — methods `schematis()`, `corpus()`, `longitudo()`,
`opertum()`, `algorithmus()`, `digestio()`, `progenies()`,
`pre_tokenizator()`, `digestio_vocabuli()`, `eog()`, `bos_vacua()`,
`spatium_vacua()`, `quantizatio()`, `elementa_glomoris()`,
`octeti_glomoris()`, `concordatio()`, `limes_machinae()`, `limes_kv()`,
`limes_tensorum()`, `limes_nominis()`, `limes_dimensionis()`,
`limes_elementorum()`, `limes_textus()`, `identificator()`, `densitas()`,
`strata()`, `contextus()`, `semita()` (provenance path — NEVER identity),
`identia()` (the schema-versioned identity record).

Free functions:

- `functio identitas_aequus(Identitas a, Identitas b) → bivalens` —
  field-wise identity equality.
- `functio structa(textus schema, lista<numerus<u8>> bytes, bivalens opertum,
  textus algorithmus, textus digestio, textus progenies, textus
  pre_tokenizator, textus digestio_vocabuli, textus eog, bivalens bos_vacua,
  bivalens spatium_vacua, textus typo_quantizationis, numerus
  elementa_glomoris, numerus octeti_glomoris, numerus concordatio, numerus
  limes_machinae, numerus limes_kv, numerus limes_tensorum, numerus
  limes_nominis, numerus limes_dimensionis, numerus limes_elementorum,
  numerus limes_textus, textus identificator, textus densitas, numerus
  strata, textus contextus, textus semita) → Capsula ⇥ AdmissionError` — the
  validated capsule constructor (admission gate).
- `functio verifica(Capsula c) → bivalens ⇥ AdmissionError` — consumer-side
  self-verification (re-runs the admission matrix).
- `functio verifica_contra(Capsula c, textus expectatum) → bivalens ⇥
  AdmissionError` — verify against an expected identity wire.
- `functio serializa_identitas(Capsula c) → textus ⇥ AdmissionError` —
  identity wire form.
- `functio deserializa_identitas(textus wire) → Identitas ⇥ AdmissionError`
  — identity from wire, fail closed.

**EOG-set admission (correctness wave, `2cdc498` / `6cc0eb5`)**: capsule
admission enforces the **exact pinned EOG set `{0,2}`**
(`EOG ← "0,2"`; `_tokenizator_recta` requires `eog ≡ EOG`). A
well-formed-but-different set is a **different tokenizer** — it fails
closed at admission (`EogMala`), it is not a value error. The pinned
add-* flags are `falsum`; `bos_vacua` / `spatium_vacua` are the positive
facts (verum = BOS-free / space-prefix-free), enforced with `≡`.

## gradus:model/gguf_manifest

Format-general GGUF v3 manifest inspection (GGUF-A1a). `CorpusGguf` accepts a
bounded prefix containing the complete header, metadata, and tensor table,
plus the caller-supplied total artifact length and pathless content identity.
The parser retains metadata value kinds and exact wire payloads, raw tensor
names/shapes/types/relative offsets, and known GGML block geometry. Unknown
architecture metadata and raw GGML type IDs remain inspectable; this module
does not admit an architecture, read tensor payloads, or claim inference.
The parser bounds metadata and tensor directories at 4,096 entries and the
retained header/table corpus at 64 MiB; these ceilings bound duplicate and
overlap checks while admitting the inventoried local rows (up to 753 tensors).
The A1a source and synthetic builders are compile/typecheck evidence. The
package-MIR receipt is recorded in `exempla/gguf-manifest/README.md`; no
committed binary fixture is claimed parsed here.

`genus CorpusGguf` — fields `tabula`, `longitudo_artifacti`, and
`identitas`.
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
- `functio metadatum(ManifestumGguf m, textus clavis) → MetadatumGguf ⇥
  GgufManifestError` — retrieve one preserved metadata entry.
- `functio textum(ManifestumGguf m, textus clavis) → textus ⇥
  GgufManifestError` — typed text accessor for a string metadata value.
- `functio numerum(ManifestumGguf m, textus clavis) → numerus ⇥
  GgufManifestError` — typed integer accessor for a numeric metadata value.
- `functio inveni_tensorem(ManifestumGguf m, textus nomen) →
  DescriptioTensorisGguf ⇥ GgufManifestError` — retrieve one tensor descriptor.
- `functio layout(numerus typo_ggml, lista<numerus> forma) → LayoutGgml ⇥
  GgufManifestError` — resolve known GGML block geometry or return
  `LayoutGgml.Ignota` for an unknown raw type ID.

`discretio GgufManifestError` variants: `FormatMala`, `VersioIgnota`,
`Truncata`, `WireMala`, `LimitesMala`, `Superfluitas`, `ClavisDuplicata`,
`TensorDuplicatum`, `OffsetMala`, and `IdentitasMala`; each carries
`textus causa`.

## gradus:model/gguf

GGUF admission (PML2-U3) — one admitted row → capsule, fail-closed by
format/quantization/shape/tokenizer facts.

- `functio causa(GgufError e) → textus` — render the typed error message.
- `functio admit(lista<numerus<u8>> bytes, textus digestio, textus
  digestio_vocabuli, numerus expectatum_kv, numerus expectatum_tensorum,
  numerus expectatum_elementa, numerus expectatum_f32, numerus
  expectatum_q4k, numerus expectatum_q5, numerus expectatum_q6, numerus
  expectatum_q8, textus semita) → capsula.Capsula ⇥ GgufError` — the GGUF
  row admission entry: parses the GGUF header/tensor metadata and admits →
  capsule, fail closed on any deviation.

## gradus:model/safetensors

Safetensors admission (PML2-U2) — one admitted row → capsule, fail-closed.

- `functio causa(SafetensorError e) → textus` — render the typed error
  message.
- `functio admittas(lista<numerus<u8>> corpus, textus digestio, textus
  semita) → capsula.Capsula ⇥ SafetensorError` — the Safetensors row
  admission entry: JSON header parse → capsule, fail closed on any
  deviation.

## gradus:model/dequant

CPU dequantization of the four admitted GGML block types (PML2-U5, C3) —
exact re-expression of the GI2-1 CPU dequant core (llama.cpp
`ggml/src/ggml-quants.c` at the pinned checkout). Bit-exact against the
independent reference goldens.

- `functio causa(DequantError e) → textus` — render the typed error message.
- `functio elementa_glomoris(numerus typo) → numerus` — block element count
  for an admitted GGML type (closed set {F32, Q5_0, Q8_0, Q4_K, Q6_K}).
- `functio octeti_glomoris(numerus typo) → numerus` — block byte size for an
  admitted GGML type.
- `functio dequantizas_glomulus(numerus typo, lista<numerus<u8>> blocci) →
  lista<f32> ⇥ DequantError` — dequantize one block (fail closed on
  wrong-length/NaN/unknown-type).
- `functio dequantizas_ordo(numerus typo, lista<numerus<u8>> octeti) →
  lista<f32> ⇥ DequantError` — dequantize a whole row (byte length must be
  a whole multiple of block bytes).

## gradus:tokenizer

Tokenizer identity — `tokenizer-identity-schema-1.0.0` (PML2-U4, council
C8). The deeper probe-parity contract the capsule references: pinned row
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
./scripta/inventory-public-symbols   # per-module counts + total 612 + the
                                     # committed coverage gate: every public
                                     # symbol below is documented here
```

The inventory script asserts every live module's `functio` count, the live
all-module total (612), and — per module — that every public symbol name
listed above appears in this reference's `### gradus:<module>` section. A
public symbol added to `src/` without a matching entry here fails the
script (zombie-doc gate, PML6-U1). Private `_`-prefixed helpers are exempt;
the two renamed serialize readers are documented for the correctness-wave
reconciliation.
