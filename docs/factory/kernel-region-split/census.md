# kernel-region-split census — live inventory

Census for operator need `3b9e5796`, unit KRS-1. Method: every function of the seven named files (`src/transformer.fab`, `src/attention.fab`, `src/nn.fab`, `src/math.fab`, `src/model/dense.fab`, `src/decode.fab`, `src/generation.fab`) gets one row; sibling modules contribute rows only where they compose tensor math (the need's sibling filter). Verified against gradus `main` at commit `f6476a7` on 2026-08-28 by reading the live source, not the starter list. Genus receiver accessors (`fn output()`, `fn state()`, field getters on `Weights`/`Decoder`/`CachedAttention`/`Metric` etc.) are record projections, not functions — folded into their genus row, not listed individually.

**Classes** (operator decision tree, need `3b9e5796`): `reuse-leaves` · `named-private-kernel` · `kernel-closure` · `hole` · `not-a-kernel` · `already-kernel` (inventory marker: body is already a `@ kernel` leaf or already composes typed leaves — no conversion owed).

**Columns**: function · class · leaves (existing `@ kernel` leaves to call) · wrapper keeps (what stays on the ordinary wrapper) · hole (illegal nested call left as argument) · 2nd caller (yes → named private; no → closure once `ef103950` lands) · launch claim (none / export seam) · packet (function-family for the conversion unit; `—` = not dispatched).

Launch-count law (need rule 7) binds every row: no row below changes an exported program plan by itself, so **every dispatchable row carries launch claim `none`**. The only family that could ever carry one is the attention parent (KRS-6), and only with a named export seam.

## 0. Starter-row verification (corrections to the chat list)

- **Verified**: `transformer.fab` bag wrappers `_linear`/`_gelu`/`_layernorm`/`_add`/`_attention` (lines 307–330) and `_rmsnorm`/`_swiglu`/`_multi_attention` (lines 411–427) exist as stated — but they wrap the **carrier twins** (`nn.linear_carrier`, `math.add_carrier`, `nn.swiglu`, `nn.rmsnorm_carrier`) over runtime-shaped `NumericBlock`s. Pinning those onto `tensor<f32, [T, D]>` is SEM014/SEM016-blocked (shape generics unavailable in library context; size-generic pin on `⇥` fails). The **typed static twins `dense_block_static` / `dense_block_cached_static` (630/666) already call the typed leaves directly** (`nn.rmsnorm`, `math.add`, `nn.swiglu_hidden`, `·`). Correction: the starter's "pin, then leaves" for the bag wrappers is not dispatchable in this campaign — recorded, owned by `dense-typed-assembly` unit 5. The dispatchable reuse-leaves work at these sites is the **legacy fixed-shape adapters in `nn.fab`** (KRS-2) and the **static-twin region extraction** (KRS-3/KRS-4).
- **Verified**: `model/dense.fab` `_rmsnorm` (296) / `_linear` (299) have the same shape — carrier twins on the bag routes (`forward`, `decode_step`, `decode_block`, `prefill_cached`); typed runners (`forward_ref01` family) already use glyphs + static twins. Same SEM016 record, not carded.
- **Verified**: `dense_mlp` starter row — the last lines of `dense_block_static` (657–663) and `dense_block_cached_static` (687–693) are byte-identical SwiGLU+residual tails over typed tensors → named private `@ kernel`, two callers (KRS-3).
- **Verified**: QKV starter row — both static twins carry an identical typed QKV prologue with `if has_bq/bk/bv` bias branches (633–648, 669–684) → bias presence is wrapper policy; always-add region (KRS-4).
- **Verified**: attention hole — `multi_head_attention` (832) / `multi_head_attention_cached` (1054) keep `_validate_multi`, `_rope_table` (host list walk), `⇥`; per-head core exists as `@ kernel scaled_dot_product_static` (76); the `list.append` head loop is the illegal nested site (KRS-6, deferred).
- **Verified**: not-a-kernel starter rows — `model/dense.fab` `decode_step` (792) / `prefill_ref01` (626) session drivers; `generation.fab` generate family; `load` (432) / resolvers / cache admit. Recorded below.

## 1. `src/transformer.fab`

| function | class | leaves | wrapper keeps | hole | 2nd caller | launch claim | packet |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `bert_tiny_block_2x8` | reuse-leaves | body already glyphs/`.layer_norm`/`.softmax()`/`.gelu()` | none (no `⇥`) | none | no | none | KRS-5 |
| `from_nn_error` / `from_math_error` / `from_attention_error` | not-a-kernel | — | error mapping | — | — | — | — |
| `_linear` / `_gelu` / `_layernorm` / `_add` | not-a-kernel (record: SEM016) | `nn.linear_carrier` etc. (carrier twins) | `⇥` mapping | carrier pin | — | — | — |
| `_attention` | not-a-kernel (record: SEM016) | mode dispatch over carrier twins | `⇥`, mode policy | — | — | — | — |
| `_rmsnorm` / `_swiglu` / `_multi_attention` | not-a-kernel (record: SEM016) | `nn.rmsnorm_carrier`, `nn.swiglu`, `attention.multi_head_attention` | `⇥` mapping | — | — | — | — |
| `transformer_block` | not-a-kernel (record: SEM016) | via wrappers above | `⇥`, mode reject, all carrier math | — | — | — | — |
| `dense_block` | not-a-kernel (record: SEM016) | via wrappers above | `⇥`, carrier math | — | — | — | — |
| `default_cached_block` / `CachedBlock` accessors | not-a-kernel | — | constructor | — | — | — | — |
| `_attention_cached` / `_multi_attention_cached` | not-a-kernel (record: SEM016 + cache) | carrier twins + `kv.extend` | `⇥`, cache write | cache mutation | — | — | — |
| `transformer_block_cached` / `dense_block_cached` | not-a-kernel (record: SEM016 + cache) | via wrappers | `⇥`, cache | cache mutation | — | — | — |
| `_to_block` / `_from_block` | not-a-kernel (record: SEM016) | — | staging/pin | — | — | — | — |
| `dense_block_static` | named-private-kernel (parent) | `nn.rmsnorm`, `nn.swiglu_hidden`, `math.add`, `·` | `⇥`, ε use, bias presence, bag attention call + pins | `_multi_attention` (argument: `ctx`) | yes (cached twin) | none | KRS-3+KRS-4 |
| `dense_block_cached_static` | named-private-kernel (parent) | same | `⇥`, bias presence, cache read/write via `_multi_attention_cached`, pins | `_multi_attention_cached` (argument: `ctx`) | yes (static twin) | none | KRS-3+KRS-4 |

## 2. `src/attention.fab`

| function | class | leaves | wrapper keeps | hole | 2nd caller | launch claim | packet |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `scaled_dot_product_2x8` | already-kernel | — | — | — | — | — | — |
| `scaled_dot_product_static` | already-kernel | — | — | — | — | — | — |
| `from_math_error` / `from_kv_cache_error` | not-a-kernel | — | error mapping | — | — | — | — |
| `consecutive_policy` / `interleaved_policy` / `policy_name` / `default` / `RopeConfig` accessors | not-a-kernel | — | enum/record | — | — | — | — |
| `construct_rope_config` / `construct_consecutive_rope_config` | not-a-kernel | — | `⇥` validation | — | — | — | — |
| `_dtype_f32` / `_dtype_pair` / `_dtype_triple` | not-a-kernel | — | dtype policy | — | — | — | — |
| `_exp` / `_reduce_angle` / `_sin` / `_cos` | not-a-kernel | — | scalar Taylor helpers (host) | — | — | — | — |
| `_transpose` / `_fill` / `_softmax` / `_rope` / `_rope_table` | not-a-kernel (record: carrier walks, legacy-L2) | — | staged list/index walks | — | — | — | — |
| `_interleaved` | not-a-kernel | — | policy → bool | — | — | — | — |
| `_validate_triplet` / `_validate_rope` / `_validate_multi` / `_validate_absolute_positions` / `_validate_cached_triplet` / `_validate_cached_multi` | not-a-kernel | — | `⇥` shape/position policy | — | — | — | — |
| `_attention_core` / `_attention_core_offset` | not-a-kernel (record: SEM016) | `math.matmul`, `math.mul_carrier` (carriers) | `⇥` mapping | carrier pin | — | — | — |
| `_head` / `_reconcile` / `_concat_rows` | not-a-kernel (record: carrier walks) | — | splits/concat | — | — | — | — |
| `_attention_matmul` | not-a-kernel (record: SEM016) | `math.matmul` | `⇥` mapping | — | — | — | — |
| `rotary_position_embedding` / `rotary_position_embedding_config` | not-a-kernel (record: SEM016) | — | `⇥`, table build | carrier rope | — | — | — |
| `scaled_dot_product` / `scaled_dot_product_causal` / `scaled_dot_product_causal_rope` | not-a-kernel (record: SEM016) | typed core exists (`scaled_dot_product_static`) but inputs are runtime-shaped carriers | `⇥`, validation | carrier pin | — | — | — |
| `multi_head_attention` | hole | `scaled_dot_product_static` (per-head core) | `⇥`, `_validate_multi`, `_rope_table`, GQA policy | `list.append` head loop + `_head` splits | no | none (per-head until parent; export seam required for any claim) | KRS-6 |
| `default_cached` / `CachedAttention` accessors | not-a-kernel | — | constructor | — | — | — | — |
| `_write_cache` | not-a-kernel | — | cache mutation | — | — | — | — |
| `scaled_dot_product_causal_rope_cached` | not-a-kernel (record: SEM016 + cache) | — | `⇥`, cache read/write | cache mutation | — | — | — |
| `multi_head_attention_cached` | hole | `scaled_dot_product_static` | `⇥`, `_validate_cached_multi`, `_rope_table`, cache write | `list.append` head loop + `_head` splits | no | none | KRS-6 |

## 3. `src/nn.fab`

| function | class | leaves | wrapper keeps | hole | 2nd caller | launch claim | packet |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `_staged` | not-a-kernel | — | staging helper | — | — | — | — |
| `linear_2x2` | reuse-leaves | `nn.linear` (same module) | `⇥` (drop stage→`linear_from_raw` detour) | none | no | none | KRS-2 |
| `linear_4x4` | already-kernel (delegates to `linear`) | `linear` | none | — | — | — | — |
| `gelu_4x4` | reuse-leaves | `nn.gelu` | `⇥` (drop stage→`gelu_carrier`→pin detour) | none | no | none | KRS-2 |
| `linear_2x8` | reuse-leaves | `·` + `.added_bias` (S6-C2 per-channel contract) | `⇥` (drop carrier detour) | none | no | none | KRS-2 |
| `layernorm_2x8` | reuse-leaves | `.layer_norm(1, ε, s, o)` method twin | `⇥` (drop carrier detour) | none | no | none | KRS-2 |
| `gelu_2x8` | reuse-leaves | `nn.gelu` | `⇥` (drop carrier detour) | none | no | none | KRS-2 |
| `from_shape_error` / `from_math_error` | not-a-kernel | — | error mapping | — | — | — | — |
| `_numel_valid` / `_dtype_f32` / `_dtype_pair` / `_dtype_triplet` | not-a-kernel | — | policy | — | — | — | — |
| `_exp` / `_tanh` / `_sqrt` / `_scalar_gelu` / `σ` / `_scalar_silu` | not-a-kernel | — | scalar helpers (carrier twins' guts) | — | — | — | — |
| `linear` | already-kernel (leaf) | — | — | — | — | — | — |
| `linear_from_raw` | reuse-leaves (already pins + calls `linear`) | `linear` | `⇥` pin mapping | — | — | — | — (no change owed) |
| `linear_carrier` / `gelu_carrier` / `rmsnorm_carrier` / `silu_carrier` / `transpose_carrier` / `gather_carrier` | not-a-kernel (record: load-edge staged residuals, SEM014) | — | `⇥`, shape policy, list walks | — | — | — | — |
| `gelu` / `rmsnorm` / `swiglu_hidden` / `silu` | already-kernel (leaves) | — | — | — | — | — | — |
| `layernorm` (carrier) | not-a-kernel (record: no typed twin; `.layer_norm` method exists for typed sites) | — | `⇥`, walk | — | — | — | — |
| `swiglu` (carrier) | not-a-kernel (record: SEM016; typed sites use `swiglu_hidden` + `·`) | — | `⇥`, walks | — | — | — | — |

## 4. `src/math.fab`

| function | class | leaves | wrapper keeps | hole | 2nd caller | launch claim | packet |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `add` / `sub` / `mul` / `div` / `neg` | already-kernel (leaves) | — | — | — | — | — | — |
| `construct` | not-a-kernel | — | `⇥` constructor | — | — | — | — |
| `add_carrier` / `sub_carrier` / `mul_carrier` / `div_carrier` / `neg_carrier` / `abs_carrier` / `signum_carrier` | not-a-kernel (record: SEM016 staged twins) | — | `⇥`, walks | — | — | — | — |
| `sum` / `mean` / `matmul` / `cast` / `concatenate` / `slice` | not-a-kernel (record: SEM016 staged walks; no typed leaf exists) | — | `⇥`, walks | — | — | — | — |
| `from_shape_error` / `from_tensor_error` / `from_dtype_error` | not-a-kernel | — | error mapping | — | — | — | — |
| `_shape_broadcast` / `_numel_valid` / `_index_broadcast` / `_index_axis` / `_coordinate` / `_flat_axis` / `_dtype_pair` / `_dtype_from_name` / `_shape_dim` / `_part_at` / `_elem_at` | not-a-kernel | — | index/policy helpers | — | — | — | — |

## 5. `src/model/dense.fab`

| function | class | leaves | wrapper keeps | hole | 2nd caller | launch claim | packet |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `from_tensor_error` / `from_nn_error` / `from_transformer_error` / `from_kv_cache_error` / `_map_cached` | not-a-kernel | — | error mapping | — | — | — | — |
| `_shape_text` / `_shape` / `_token_major_view` / `_transpose` / `_collect` | not-a-kernel | `nn.transpose_carrier`, `nn.gather_carrier` | views/diagnostics | — | — | — | — |
| `gather` / `gather_step` | not-a-kernel (record: SEM016 — literal-shape pins by design) | `nn.gather_carrier` | `⇥`, pin | — | — | — | — |
| `_no_bias` / `_channel_to_rows` / `_attn_bias` / `_probe_bias` | not-a-kernel | — | bias-presence policy (host chooses tensor) | `source()` resolver | — | — | — |
| `_rmsnorm` / `_linear` | not-a-kernel (record: SEM016; typed runners already use glyphs + static twins) | `nn.rmsnorm_carrier`, `nn.linear_carrier` | `⇥` mapping | — | — | — | — |
| `_block` / `_block_cached` | not-a-kernel (delegates to `transformer` rows) | `transformer.dense_block*` | `⇥` mapping | — | — | — | — |
| `_shared_prefix` / `_admit_cached` / `_require_cfg` / `_require_ref01` | not-a-kernel | — | cache/config policy | — | — | — | — |
| `_zeros_rank1` / `_pin_rank1` / `_pin_rank2` / `_pin_same` / `_pin_same_rank1` | not-a-kernel | — | pin helpers | — | — | — | — |
| `load` | not-a-kernel | — | `⇥`, resolver, pins | `source()` | — | — | — |
| `probe_load_layer_count` / `probe_layer_rms_len` / `probe_typed_block_static` / `probe_inferred_leaves` | not-a-kernel | leaves/glyphs already | probes (SEM008/SEM016 sentinels) | — | — | — | — |
| `_typed_ref01` | not-a-kernel | — | record conversion | — | — | — | — |
| `forward_ref01` / `decode_step_ref01` / `prefill_ref01` | not-a-kernel (typed drivers over already-split static twins) | `dense_block_static` twins, `.rms_norm`, `·` | `⇥`, load, per-layer loop | `list.append` layer loop | — | — | — |
| `forward` | not-a-kernel (record: SEM016 bag route; dense-typed-assembly unit 5) | carrier twins via wrappers | `⇥`, resolver, bias policy, loops | `source()`, bags | — | — | — |
| `DenseStep` accessors / `default_step` / `empty_caches` | not-a-kernel | — | record/constructor | — | — | — | — |
| `decode_step` | not-a-kernel (session driver) | as `forward` | `⇥`, cache policy, loop | cache mutation, `source()` | — | — | — |
| `decode_block` | not-a-kernel (session driver) | as `forward` | `⇥`, cache policy, loops | cache mutation, `source()` | — | — | — |
| `prefill_cached` | not-a-kernel (session driver) | as `forward` | `⇥`, cache policy, loops | cache mutation, `source()` | — | — | — |

## 6. `src/decode.fab`

| function | class | leaves | wrapper keeps | hole | 2nd caller | launch claim | packet |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `from_transformer_error` / `from_nn_error` / `from_tensor_error` / `_sampling_map` | not-a-kernel | — | error mapping | — | — | — | — |
| `construct_weights` / `construct_decoder` / `default` / `Weights`+`Decoder` accessors | not-a-kernel | — | constructors/records | — | — | — | — |
| `_tensor` / `_embedding` | not-a-kernel | — | staging/row gather walk | — | — | — | — |
| `_block` / `_block_cached` / `_project` | not-a-kernel (delegates; SEM016 carriers) | `transformer.transformer_block*`, `nn.linear_carrier` | `⇥` mapping | — | — | — | — |
| `decode_data` / `decode_cached` / `prefill` | not-a-kernel (session drivers) | via delegates | `⇥`, domain policy, loops | cache mutation (cached row) | — | — | — |
| `fresh_session` / `default_session` / `advance` / `reset` / `fresh_cancellation` / `cancellation_cancelled` / `observe_cancellation` | not-a-kernel | — | session policy | — | — | — | — |
| `default_step` / `DecodeStep` accessors | not-a-kernel | — | record | — | — | — | — |
| `replay` | not-a-kernel (sampling replay driver) | `sampling` | `⇥`, sampling | — | — | — | — |

## 7. `src/generation.fab`

All rows: session/loop drivers, cursor + wire policy, sampling admit, speculative commit. Tensor math appears only through `decode`/`dense` delegates and list walks (`_suppress_eog`, `_sample_logits`, `_logit_row`, `_slice_rows`, `_last_logits` — policy walks over carriers/lists). Nothing carded.

| function (family) | class | leaves | wrapper keeps | hole | 2nd caller | launch claim | packet |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `acceleration_disabled` / `acceleration_context_lookup` / `acceleration_mode_name` / `_acceleration_mode_from_name` / `construct_acceleration` / `default_acceleration` / `acceleration_equal` | not-a-kernel | — | policy | — | — | — | — |
| `generation_equal` / `construct_generation_with_policy` / `construct_generation` / `default` / `generation_failure` / `support_flags` / `admitted_features` / `config` / `seed` | not-a-kernel | — | config policy | — | — | — | — |
| `_serialize_acceleration` / `serialize_generation` / `_digit` / `_numeric` / `_wire_int` / `_wire_f32` / `_deserialize_acceleration` / `deserialize_generation` | not-a-kernel | — | wire parse/render | — | — | — | — |
| `fresh_cursor` / `default_cursor` / `token_allowed` / `cursor_advance` / `cursor_reset` / `cursor_after_prompt` / `_advance_n` | not-a-kernel | — | cursor policy | — | — | — | — |
| `eog_stop` / `ignore_eos` / `stop_policy_name` / `stops_on_eog` / `_suppress_eog` / `_sample_logits` | not-a-kernel (sampling policy) | — | stop policy, list walks | — | — | — | — |
| `_observe` / `_sample` | not-a-kernel (sampling admit) | `sampling` | `⇥` mapping | — | — | — | — |
| `_prefill` / `_decode_one` / `_dense_one` / `_dense_prefill` | not-a-kernel (delegates) | `decode.*`, `dense.*` | `⇥` mapping | — | — | — | — |
| `_last_logits` / `_logit_row` / `_slice_rows` | not-a-kernel (record: carrier walks) | — | row selection walks | — | — | — | — |
| `_target_ids` / `_accepted_prefix` / `_lookup_context` / `_accepted_target_count` / `_lookup_candidates` / `_commit_dense_block` | not-a-kernel (speculative commit policy) | `sampling`, cache rollback contract | `⇥`, cache checkpoint/commit | cache mutation | — | — | — |
| `_prefix` | not-a-kernel | — | list helper | — | — | — | — |
| `generate` / `generate_with_stop` / `generate_cancelled` / `generate_cancelled_with_stop` / `generate_dense` / `generate_dense_with_stop` | not-a-kernel (generation loops) | via delegates | the loop | loop control, caches | — | — | — |
| `construct_dense_engine` / `default_dense_engine` / `DenseEngine` | not-a-kernel | — | record | — | — | — | — |
| `GenerationCursor`/`AccelerationPolicy`/`GenerationConfig` accessors | not-a-kernel | — | records | — | — | — | — |

## 8. Siblings composing tensor math

Filter: sibling modules whose functions compose tensor math (leaf calls, glyphs, or carrier tensor walks). Modules with no tensor-math composition (resolvers, manifests, admission, tokenizer, serialize, receipt, cache containers, dtype/shape/tensor infra, `gradient.fab` autograd wrappers) are out of the census by the need's own scope; they are the tree's rule-5 "record and skip" territory and no row is owed.

| function | class | leaves | wrapper keeps | hole | 2nd caller | launch claim | packet |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `mlp.fab` `_linear` / `_gelu` | not-a-kernel (record: SEM016 carriers) | carrier twins | `⇥` mapping | — | — | — | — |
| `mlp.fab` `forward_mlp` | not-a-kernel (record: SEM016 — typed twin `forward_mlp_loss` exists on the `@ radix backward` training path) | carrier twins | `⇥` | carrier pin | — | — | — |
| `mlp.fab` `forward_mlp_loss` | not-a-kernel (training path; `@ radix backward` companion ABI — not a fusion surface) | glyph body | `@ radix` annotations | — | — | — | — |
| `mlp.fab` `nil` | not-a-kernel | — | ABI residual | — | — | — | — |
| `loss.fab` `mse` / `cross_entropy` | not-a-kernel (record: SEM016 staged walks; typed `mse_*` kernels exist for fixed shapes) | — | `⇥`, walks | carrier pin | — | — | — |
| `loss.fab` `mse_2x2` / `mse_4x4` / `mse_2x8` | already-kernel | — | — | — | — | — | — |
| `metrics.fab` `accuracy` | not-a-kernel (record: carrier walk + i32 target policy) | — | `⇥`, argmax policy | — | — | — | — |
| `model/moe.fab` `route` | not-a-kernel (record: resolver + list softmax walk) | — | `⇥`, `source()` | `source()` | — | — | — |
| `model/moe.fab` `expert_out` / `ffn_moe` | not-a-kernel (record: SEM016 — runtime-shape matmul via `math.matmul` carriers, resolver windows, accumulation loop) | `nn.swiglu` (carrier) | `⇥`, resolver, finite checks | `source()`, loops | — | — | — |
| `model/moe.fab` `_project` / `_row` / `_linear_weight` / `_swiglu_no_bias` / `_flatten_row` / `_softmax` / `_best_index` / `_sigmoid` / `_dot` | not-a-kernel (record: carrier/list walks) | — | walks | — | — | — | — |
| `train.fab` `train_step_2x2` / `train_step_4x4` / `train_step_bert_linear` / `train_step_bert_layernorm` | not-a-kernel (training-loop mechanics; delegates to `optimize.sgd_step_*`, no device launch surface) | `optimize.sgd_step_*` (not `@ kernel`) | none (`⇥`-free) | in-body calls to non-kernel leaves | — | — | — |
| `optimize.fab` `_sgd_family` / `sgd_step_2x2` / `sgd_step_4x4` | not-a-kernel (record: `list.append` loop + `seed.create` fill; glyph-leaf law could later admit a typed SGD leaf — no second caller today) | `−`, `⊙` glyphs | list loop | `list.append` | no | none | — (record; no card) |
| `sampling.fab` `max` / `distribution` / samplers | not-a-kernel (sampling — tree rule 5) | — | `⇥`, policy | — | — | — | — |
| `model/dequant.fab` `_dequant_q*` / `_half` / `_bfloat16` / `_byte` / `_i8` / `_power_two` | not-a-kernel (parsers — tree rule 5) | — | byte walks | — | — | — | — |
| `model/dense_llama.fab` / `dense_qwen2.fab` / `gguf*.fab` / `qwen35moe*.fab` resolve/config/admit/reference/canonical rows | not-a-kernel (load/resolver — tree rule 5) | — | `⇥`, manifest policy | — | — | — | — |
| `block_verify.fab` / `calibration.fab` / `speculative.fab` / `prepared_state.fab` / `context_lookup.fab` / `cache.fab` / `cache_branch.fab` | not-a-kernel (verify/calibration/admission/identity policy — tree rule 5) | — | policy/records | — | — | — | — |
| `src/kernel.fab` GEA3 entries | out of census (frozen launch catalog; generic code never calls it — need rule 1) | — | — | — | — | — | — |

## 9. Census totals

- Dispatchable conversion families: 4 (`nn` legacy adapters; `dense_mlp`; QKV always-add; `bert_tiny_block_2x8` glyph-leaf mark) → cards KRS-2..KRS-5.
- Deferred hole family: 1 (attention multi-head parent, both cached and uncached variants) → KRS-6.
- Kernel-closure class: 0 live sites. Every one-off candidate dissolved under verification into either a direct leaf call (KRS-2 rows) or a second-caller region (KRS-3/KRS-4). `ef103950` gates nothing dispatched today; hands that later find a genuine one-off note it on the card and defer (mind routing).
- Recorded-not-converted (convert-or-record, reason in code at conversion time where a hand touches the site): the SEM014/SEM016/SEM008 carrier seams (`transformer.fab` bag wrappers, `model/dense.fab` bag routes, `math`/`nn`/`attention` carrier twins, `mlp`/`loss`/`metrics`/`moe` walks), session drivers, loaders, sampling, parsers.
