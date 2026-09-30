# kernel-region-split census — live inventory

Census for operator need `3b9e5796`, unit KRS-1. Method: **one row per `fn` declaration** in each of the seven named files (`src/transformer.fab`, `src/attention.fab`, `src/nn.fab`, `src/math.fab`, `src/model/dense.fab`, `src/decode.fab`, `src/generation.fab`) — accessors and constructors included, nothing folded or slash-grouped; sibling modules contribute one row per function that composes tensor math (the need's sibling filter), and every excluded module/class carries an explicit exclusion row with its reason. Verified against gradus `main` at commit `96fb905` (source identical to the audited `f494db2` tree for every cited anchor) on 2026-08-28 by reading the live source, not the starter list and not the prior census prose.

**Classes** (operator decision tree, need `3b9e5796`): `reuse-leaves` · `named-private-kernel` · `kernel-closure` · `hole` · `not-a-kernel` · `already-kernel` (inventory marker: the function itself already carries `@ kernel` — no conversion owed).

**Columns**: function (line) · class · leaves (existing `@ kernel` leaves to call) · wrapper keeps (what stays on the ordinary wrapper) · hole (illegal nested call left as argument) · 2nd caller (yes → named private; no → closure once `ef103950` lands) · launch claim (none / export seam) · packet (function-family for the conversion unit; `—` = not dispatched).

Launch-count law (need rule 7) binds every row: no row below changes an exported program plan by itself, so **every dispatchable row carries launch claim `none`**. The only family that could ever carry one is the attention parent (KRS-6), and only with a named export seam.

## 0a. Amendment — REVISE `1ddc4077` reissue (2026-08-28)

Supersedes the landed `f494db2` census shape (audit findings 1–8, all confirmed against live source before this reissue):

- **One-row ledger** — the prior tables slash-grouped declarations and folded genus accessors into family rows. Reissued below with exactly one row per declaration: 25 + 50 + 33 + 33 + 46 + 55 + 77 = **319 rows** over the seven named files, plus sibling rows.
- **gradient.fab admitted** — the prior §8 excluded `gradient.fab` wholesale as "autograd wrappers, no tensor-math composition". False: `simple_loss` (:219–221) and `masked_mean` (:279–281) are direct typed tensor-math bodies (`⊙` glyph + `.mean()`). They are admitted below as `not-a-kernel` autograd-companion ABI rows — the same classification the census already gave `mlp.forward_mlp_loss` (the precedent): `@ radix { lane = "air" }` + `@ radix backward` lowering is a different family from `@ kernel` fusion; recorded, not converted.
- **`nn.linear_4x4` reclassified** — was `already-kernel (delegates to linear)`. Wrong: the function itself carries only `@ public` (no `@ kernel`), is public, has no `⇥`, and its whole body is `return linear(input, weight, bias)` — a single call to the `@ kernel` leaf. Under the glyph-leaf rule it is annotation-capable; moved to `reuse-leaves` and added to KRS-2 (annotation, not reroute).
- **Dense-tail anchors corrected** — the prior §0/KRS-3 cited `dense_block_cached_static:687–693` as a "byte-identical" tail. Live source: 687 is the context pin, 689–691 the residual/RMSNorm, 693 a comment banner; the cached SwiGLU+residual arithmetic is **694–698** and its return is `TypedCachedBlock { output = …, state = step.state() }` (:698), not byte-identical to the uncached tensor return (:662). Correct claim: the two twins share the **same arithmetic core** (uncached 658–662, cached 694–698; gate/up/`swiglu_hidden`/down-projection/residual-add statements identical) with **different return wrappers**. QKV prologue anchors likewise corrected to 632–647 / 668–683.
- **Attention launch posture corrected** — the prior rows/cards said the multi-head wrappers "keep per-head launches" of `scaled_dot_product_static`. Live source: `scaled_dot_product_static` (attention.fab:79, `@ kernel`) has **no source call site**; `multi_head_attention` (:832) and `multi_head_attention_cached` (:1055) compute per-head cores through the **carrier** helpers `_attention_core` (:585) / `_attention_core_offset` (:902) over `list<NumericBlock>` with `_head` splits, `_rope`, `heads.append`, `_reconcile`, `_attention_matmul`. Current state = carrier per-head loop, no typed static-leaf invocation. Census rows and the KRS-6 card now say exactly that.
- **Totals recomputed** from the one-row ledger (§9); the kernel-closure zero-live claim is re-issued against the corrected scope.

The §0 starter-verification bullets that remain true are retained below unchanged; the two superseded bullets (dense-tail "byte-identical" citation; attention "per-head core exists / wrappers keep per-head launches" framing) are corrected in place per this amendment.

## 0. Starter-row verification (corrections to the chat list)

- **Verified**: `transformer.fab` bag wrappers `_linear`/`_gelu`/`_layernorm`/`_add`/`_attention` (306–330) and `_rmsnorm`/`_swiglu`/`_multi_attention` (411–427) exist as stated — but they wrap the **carrier twins** (`nn.linear_carrier`, `math.add_carrier`, `nn.swiglu`, `nn.rmsnorm_carrier`) over runtime-shaped `NumericBlock`s. Pinning those onto `tensor<f32, [T, D]>` is SEM014/SEM016-blocked (shape generics unavailable in library context; size-generic pin on `⇥` fails). The **typed static twins `dense_block_static` / `dense_block_cached_static` (630/666) already call the typed leaves directly** (`nn.rmsnorm`, `math.add`, `nn.swiglu_hidden`, `·`). Correction: the starter's "pin, then leaves" for the bag wrappers is not dispatchable in this campaign — recorded, owned by `dense-typed-assembly` unit 5. The dispatchable reuse-leaves work at these sites is the **legacy fixed-shape adapters in `nn.fab`** (KRS-2) and the **static-twin region extraction** (KRS-3/KRS-4).
- **Verified**: `model/dense.fab` `_rmsnorm` (293) / `_linear` (298) have the same shape — carrier twins on the bag routes (`forward`, `decode_step`, `decode_block`, `prefill_cached`); typed runners (`forward_ref01` family) already use glyphs + static twins. Same SEM016 record, not carded.
- **Verified (anchors corrected per §0a)**: `dense_mlp` starter row — the SwiGLU+residual **arithmetic core** of `dense_block_static` (658–662) and `dense_block_cached_static` (694–698) is the same four statements plus residual-add over typed tensors; the twins differ only in return wrapper (tensor at 662 vs `TypedCachedBlock { output, state }` at 698) → named private `@ kernel`, two callers (KRS-3).
- **Verified (anchors corrected per §0a)**: QKV starter row — both static twins carry the same typed QKV prologue with `if has_bq/bk/bv` bias branches (632–647, 668–683) → bias presence is wrapper policy; always-add region `dense_qkv` (KRS-4).
- **Verified (posture corrected per §0a)**: attention hole — `multi_head_attention` (832) / `multi_head_attention_cached` (1055) keep `_validate_multi`/`_validate_cached_multi`, `_rope_table` (host list walk), `⇥`; the typed per-head core exists as `@ kernel scaled_dot_product_static` (:79) but is **not called by anything today**; the wrappers run carrier per-head loops (`_head`, `_rope`, `_attention_core`/`_attention_core_offset`, `heads.append`) — the `list.append` head loop is the illegal nested site (KRS-6, deferred).
- **Verified**: not-a-kernel starter rows — `model/dense.fab` `decode_step` (793) / `prefill_ref01` (627) session drivers; `generation.fab` generate family; `load` (432) / resolvers / cache admit. Recorded below.

## 1. `src/transformer.fab` — 25 declarations

| function (line) | class | leaves | wrapper keeps | hole | 2nd caller | launch claim | packet |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `bert_tiny_block_2x8` (68) | reuse-leaves (annotation-capable glyph body; no `⇥`) | own body: `.layer_norm`/`·`/`.added_bias`/`.transpose()`/`.softmax()`/`.gelu()`/`+` | none | none | no | none | KRS-5 |
| `from_nn_error` (186) | not-a-kernel | — | error mapping | — | — | — | — |
| `from_math_error` (222) | not-a-kernel | — | error mapping | — | — | — | — |
| `from_attention_error` (255) | not-a-kernel | — | error mapping | — | — | — | — |
| `_linear` (306) | not-a-kernel (record: SEM016) | `nn.linear_carrier` (carrier twin) | `⇥` mapping | carrier pin | — | — | — |
| `_gelu` (311) | not-a-kernel (record: SEM016) | `nn.gelu_carrier` | `⇥` mapping | carrier pin | — | — | — |
| `_layernorm` (316) | not-a-kernel (record: SEM016) | `nn.layernorm` (carrier) | `⇥` mapping | carrier pin | — | — | — |
| `_add` (321) | not-a-kernel (record: SEM016) | `math.add_carrier` | `⇥` mapping | carrier pin | — | — | — |
| `_attention` (326) | not-a-kernel (record: SEM016) | carrier twins, mode dispatch | `⇥`, mode policy | — | — | — | — |
| `transformer_block` (352) | not-a-kernel (record: SEM016) | via wrappers above | `⇥`, mode reject, all carrier math | — | — | — | — |
| `_rmsnorm` (411) | not-a-kernel (record: SEM016) | `nn.rmsnorm_carrier` | `⇥` mapping | carrier pin | — | — | — |
| `_swiglu` (416) | not-a-kernel (record: SEM016) | `nn.swiglu` (carrier) | `⇥` mapping | — | — | — | — |
| `_multi_attention` (422) | not-a-kernel (record: SEM016) | `attention.multi_head_attention` (carrier) | `⇥` mapping | — | — | — | — |
| `dense_block` (481) | not-a-kernel (record: SEM016) | via wrappers above | `⇥`, carrier math | — | — | — | — |
| `CachedBlock.output` (512) | not-a-kernel | — | record projection | — | — | — | — |
| `CachedBlock.state` (516) | not-a-kernel | — | record projection | — | — | — | — |
| `default_cached_block` (522) | not-a-kernel | — | constructor | — | — | — | — |
| `_attention_cached` (526) | not-a-kernel (record: SEM016 + cache) | carrier twins | `⇥`, cache write | cache mutation | — | — | — |
| `_multi_attention_cached` (530) | not-a-kernel (record: SEM016 + cache) | `attention.multi_head_attention_cached` (carrier) | `⇥` mapping, cache write | cache mutation | — | — | — |
| `transformer_block_cached` (537) | not-a-kernel (record: SEM016 + cache) | via wrappers | `⇥`, cache | cache mutation | — | — | — |
| `dense_block_cached` (564) | not-a-kernel (record: SEM016 + cache) | via wrappers | `⇥`, cache | cache mutation | — | — | — |
| `_to_block` (616) | not-a-kernel | — | typed→carrier staging pin | — | — | — | — |
| `_from_block` (620) | not-a-kernel | — | carrier→typed pin (`⇥`) | — | — | — | — |
| `dense_block_static` (630) | named-private-kernel (parent) | `nn.rmsnorm`, `nn.swiglu_hidden`, `math.add`, `·` | `⇥`, ε use, bias presence, bag attention call + pins | `_multi_attention` (argument: `ctx`) | yes (cached twin) | none | KRS-3+KRS-4 |
| `dense_block_cached_static` (666) | named-private-kernel (parent) | same | `⇥`, bias presence, cache read/write via `_multi_attention_cached`, pins | `_multi_attention_cached` (argument: `ctx`) | yes (static twin) | none | KRS-3+KRS-4 |

## 2. `src/attention.fab` — 50 declarations

| function (line) | class | leaves | wrapper keeps | hole | 2nd caller | launch claim | packet |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `scaled_dot_product_2x8` (58) | already-kernel (`@ kernel`) | — | — | — | — | — | — |
| `scaled_dot_product_static` (79) | already-kernel (`@ kernel`; **no source call site today** — attention.proba:744 documents it as not probe-callable and pins a local mirror `sdpa_static` of the same body; KRS-6's future parent is its would-be caller) | — | — | — | — | — | — |
| `from_math_error` (171) | not-a-kernel | — | error mapping | — | — | — | — |
| `from_kv_cache_error` (176) | not-a-kernel | — | error mapping | — | — | — | — |
| `consecutive_policy` (202) | not-a-kernel | — | enum policy | — | — | — | — |
| `interleaved_policy` (207) | not-a-kernel | — | enum policy | — | — | — | — |
| `policy_name` (213) | not-a-kernel | — | enum policy | — | — | — | — |
| `RopeConfig.base` (240) | not-a-kernel | — | record projection | — | — | — | — |
| `RopeConfig.scale` (245) | not-a-kernel | — | record projection | — | — | — | — |
| `RopeConfig.policy` (250) | not-a-kernel | — | record projection | — | — | — | — |
| `construct_rope_config` (259) | not-a-kernel | — | `⇥` validation | — | — | — | — |
| `construct_consecutive_rope_config` (272) | not-a-kernel | — | `⇥` validation | — | — | — | — |
| `default` (280) | not-a-kernel | — | constructor | — | — | — | — |
| `_dtype_f32` (299) | not-a-kernel | — | dtype policy | — | — | — | — |
| `_dtype_pair` (305) | not-a-kernel | — | dtype policy | — | — | — | — |
| `_dtype_triple` (312) | not-a-kernel | — | dtype policy | — | — | — | — |
| `_exp` (320) | not-a-kernel | — | scalar Taylor helper (host) | — | — | — | — |
| `_reduce_angle` (326) | not-a-kernel | — | scalar Taylor helper | — | — | — | — |
| `_sin` (334) | not-a-kernel | — | scalar Taylor helper | — | — | — | — |
| `_cos` (347) | not-a-kernel | — | scalar Taylor helper | — | — | — | — |
| `_transpose` (361) | not-a-kernel (record: carrier walk, legacy-L2) | — | staged index walk | — | — | — | — |
| `_fill` (381) | not-a-kernel (record: carrier walk) | — | staged fill | — | — | — | — |
| `_softmax` (407) | not-a-kernel (record: carrier walk) | — | staged softmax walk | — | — | — | — |
| `_rope_table` (452) | not-a-kernel | — | host list walk (RoPE table build) | — | — | — | — |
| `_rope` (477) | not-a-kernel (record: carrier walk) | — | staged RoPE rotation | — | — | — | — |
| `_interleaved` (534) | not-a-kernel | — | policy → bool | — | — | — | — |
| `_validate_triplet` (547) | not-a-kernel | — | `⇥` shape policy | — | — | — | — |
| `_validate_rope` (565) | not-a-kernel | — | `⇥` position policy | — | — | — | — |
| `_attention_core` (585) | not-a-kernel (record: SEM016) | `math.matmul`, `math.mul_carrier` (carriers) | `⇥` mapping | carrier pin | — | — | — |
| `_head` (630) | not-a-kernel (record: carrier walk) | — | column split | — | — | — | — |
| `_reconcile` (648) | not-a-kernel (record: carrier walk) | — | concat | — | — | — | — |
| `_attention_matmul` (675) | not-a-kernel (record: SEM016) | `math.matmul` | `⇥` mapping | — | — | — | — |
| `_validate_multi` (714) | not-a-kernel | — | `⇥` multi-head policy | — | — | — | — |
| `rotary_position_embedding` (759) | not-a-kernel (record: SEM016) | — | `⇥`, table build | carrier rope | — | — | — |
| `rotary_position_embedding_config` (766) | not-a-kernel (record: SEM016) | — | `⇥`, table build | carrier rope | — | — | — |
| `scaled_dot_product` (780) | not-a-kernel (record: SEM016) | typed core (`scaled_dot_product_static`) exists but inputs are runtime-shaped carriers; not called | `⇥`, validation | carrier pin | — | — | — |
| `scaled_dot_product_causal` (793) | not-a-kernel (record: SEM016) | same | `⇥`, validation, causal policy | carrier pin | — | — | — |
| `scaled_dot_product_causal_rope` (806) | not-a-kernel (record: SEM016) | same | `⇥`, validation, RoPE | carrier pin | — | — | — |
| `multi_head_attention` (832) | hole (KRS-6, deferred) | **none called today** — per-head cores run on the carrier `_attention_core` (:585); the typed leaf `scaled_dot_product_static` (:79) exists unlinked | `⇥`, `_validate_multi`, `_rope_table`, GQA policy, `_head`/`_rope`/`_reconcile`/`_attention_matmul` carrier loop | `heads.append` head loop + `_head` splits | no | none (carrier loop today; export seam required for any claim) | KRS-6 |
| `CachedAttention.context` (885) | not-a-kernel | — | record projection | — | — | — | — |
| `CachedAttention.state` (889) | not-a-kernel | — | record projection | — | — | — | — |
| `default_cached` (895) | not-a-kernel | — | constructor | — | — | — | — |
| `_attention_core_offset` (902) | not-a-kernel (record: SEM016) | `math.matmul` (carrier) | `⇥` mapping | carrier pin | — | — | — |
| `_concat_rows` (948) | not-a-kernel (record: carrier walk) | — | row concat | — | — | — | — |
| `_write_cache` (956) | not-a-kernel | — | cache mutation | — | — | — | — |
| `_validate_absolute_positions` (963) | not-a-kernel | — | `⇥` position policy | — | — | — | — |
| `_validate_cached_triplet` (973) | not-a-kernel | — | `⇥` shape policy | — | — | — | — |
| `scaled_dot_product_causal_rope_cached` (1008) | not-a-kernel (record: SEM016 + cache) | — | `⇥`, cache read/write | cache mutation | — | — | — |
| `_validate_cached_multi` (1030) | not-a-kernel | — | `⇥` cached-multi policy | — | — | — | — |
| `multi_head_attention_cached` (1055) | hole (KRS-6, deferred) | **none called today** — carrier `_attention_core_offset` (:902); same unlinked leaf posture as the uncached twin | `⇥`, `_validate_cached_multi`, `_rope_table`, cache write, carrier loop | `heads.append` head loop + `_head` splits + cache write | no | none | KRS-6 |

## 3. `src/nn.fab` — 33 declarations

| function (line) | class | leaves | wrapper keeps | hole | 2nd caller | launch claim | packet |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `_staged` (106) | not-a-kernel | — | staging helper | — | — | — | — |
| `linear_2x2` (111) | reuse-leaves | `nn.linear` (same module) | `⇥` (drop stage→`linear_from_raw` detour) | none | no | none | KRS-2 |
| `linear_4x4` (123) | reuse-leaves (annotation-capable: `@ public`, no `⇥`, body = single call to `@ kernel linear` — glyph-leaf rule; reclassified per §0a) | `linear` | none today (no detour) | none | no | none | KRS-2 |
| `gelu_4x4` (132) | reuse-leaves | `nn.gelu` | `⇥` (drop stage→`gelu_carrier`→pin detour) | none | no | none | KRS-2 |
| `linear_2x8` (150) | reuse-leaves | `·` + `.added_bias` (S6-C2 per-channel contract) | `⇥` (drop carrier detour) | none | no | none | KRS-2 |
| `layernorm_2x8` (167) | reuse-leaves | `.layer_norm(1, ε, s, o)` method twin | `⇥` (drop carrier detour) | none | no | none | KRS-2 |
| `gelu_2x8` (182) | reuse-leaves | `nn.gelu` | `⇥` (drop carrier detour) | none | no | none | KRS-2 |
| `from_shape_error` (220) | not-a-kernel | — | error mapping | — | — | — | — |
| `from_math_error` (232) | not-a-kernel | — | error mapping | — | — | — | — |
| `_numel_valid` (264) | not-a-kernel | — | shape policy | — | — | — | — |
| `_dtype_f32` (270) | not-a-kernel | — | dtype policy | — | — | — | — |
| `_dtype_triplet` (276) | not-a-kernel | — | dtype policy | — | — | — | — |
| `_dtype_pair` (286) | not-a-kernel | — | dtype policy | — | — | — | — |
| `_exp` (296) | not-a-kernel | — | scalar helper (carrier twins' guts) | — | — | — | — |
| `_tanh` (302) | not-a-kernel | — | scalar helper | — | — | — | — |
| `_sqrt` (315) | not-a-kernel | — | scalar helper | — | — | — | — |
| `_scalar_gelu` (334) | not-a-kernel | — | scalar helper | — | — | — | — |
| `σ` (343) | not-a-kernel | — | scalar helper | — | — | — | — |
| `_scalar_silu` (353) | not-a-kernel | — | scalar helper | — | — | — | — |
| `linear` (365) | already-kernel (`@ kernel` `@ public` leaf) | — | — | — | — | — | — |
| `linear_from_raw` (371) | not-a-kernel (load-edge pin wrapper; already pins + calls `linear` — no conversion owed) | `linear` | `⇥` pin mapping | — | — | — | — |
| `linear_carrier` (391) | not-a-kernel (record: load-edge staged residual, SEM014) | — | `⇥`, shape policy, list walks | — | — | — | — |
| `gelu` (437) | already-kernel (`@ kernel` `@ public` leaf) | — | — | — | — | — | — |
| `gelu_carrier` (444) | not-a-kernel (record: SEM014) | — | `⇥`, walks | — | — | — | — |
| `layernorm` (466) | not-a-kernel (record: no typed twin; `.layer_norm` method exists for typed sites) | — | `⇥`, walk | — | — | — | — |
| `rmsnorm` (522) | already-kernel (`@ kernel` `@ public` leaf) | — | — | — | — | — | — |
| `swiglu_hidden` (528) | already-kernel (`@ kernel` `@ public` leaf) | — | — | — | — | — | — |
| `gather_carrier` (540) | not-a-kernel (record: SEM014) | — | `⇥`, walk | — | — | — | — |
| `transpose_carrier` (558) | not-a-kernel (record: SEM014) | — | `⇥`, walk | — | — | — | — |
| `rmsnorm_carrier` (575) | not-a-kernel (record: SEM014) | — | `⇥`, walk | — | — | — | — |
| `silu` (622) | already-kernel (`@ kernel` `@ public` leaf) | — | — | — | — | — | — |
| `silu_carrier` (629) | not-a-kernel (record: SEM014) | — | `⇥`, walk | — | — | — | — |
| `swiglu` (653) | not-a-kernel (record: SEM016; typed sites use `swiglu_hidden` + `·`) | — | `⇥`, walks | — | — | — | — |

Annotation-capable count in this file: `linear_4x4` (this reissue) — the only public `⇥`-free function whose body is pure leaf calls; `linear_2x2`/`gelu_4x4`/`linear_2x8`/`layernorm_2x8`/`gelu_2x8` keep `⇥` and stay wrappers (KRS-2 reroutes their bodies).

## 4. `src/math.fab` — 33 declarations

| function (line) | class | leaves | wrapper keeps | hole | 2nd caller | launch claim | packet |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `from_shape_error` (106) | not-a-kernel | — | error mapping | — | — | — | — |
| `from_tensor_error` (118) | not-a-kernel | — | error mapping | — | — | — | — |
| `from_dtype_error` (126) | not-a-kernel | — | error mapping | — | — | — | — |
| `_shape_broadcast` (142) | not-a-kernel | — | shape policy | — | — | — | — |
| `_numel_valid` (148) | not-a-kernel | — | shape policy | — | — | — | — |
| `_index_broadcast` (155) | not-a-kernel | — | index policy | — | — | — | — |
| `_index_axis` (184) | not-a-kernel | — | index policy | — | — | — | — |
| `_coordinate` (207) | not-a-kernel | — | index policy | — | — | — | — |
| `_flat_axis` (225) | not-a-kernel | — | index policy | — | — | — | — |
| `_dtype_pair` (244) | not-a-kernel | — | dtype policy | — | — | — | — |
| `construct` (258) | not-a-kernel | — | `⇥` constructor | — | — | — | — |
| `add` (268) | already-kernel (`@ kernel` `@ public` leaf) | — | — | — | — | — | — |
| `add_carrier` (278) | not-a-kernel (record: SEM016 staged twin) | — | `⇥`, walk | — | — | — | — |
| `sub` (297) | already-kernel (`@ kernel` `@ public` leaf) | — | — | — | — | — | — |
| `sub_carrier` (305) | not-a-kernel (record: SEM016) | — | `⇥`, walk | — | — | — | — |
| `mul` (324) | already-kernel (`@ kernel` `@ public` leaf) | — | — | — | — | — | — |
| `mul_carrier` (332) | not-a-kernel (record: SEM016) | — | `⇥`, walk | — | — | — | — |
| `div` (351) | already-kernel (`@ kernel` `@ public` leaf) | — | — | — | — | — | — |
| `div_carrier` (362) | not-a-kernel (record: SEM016) | — | `⇥`, walk | — | — | — | — |
| `neg` (381) | already-kernel (`@ kernel` `@ public` leaf) | — | — | — | — | — | — |
| `neg_carrier` (389) | not-a-kernel (record: SEM016) | — | `⇥`, walk | — | — | — | — |
| `abs_carrier` (403) | not-a-kernel (record: SEM016; no typed twin) | — | `⇥`, walk | — | — | — | — |
| `signum_carrier` (422) | not-a-kernel (record: SEM016; no typed twin) | — | `⇥`, walk | — | — | — | — |
| `sum` (434) | not-a-kernel (record: SEM016 staged walk; no typed leaf) | — | `⇥`, walk | — | — | — | — |
| `mean` (466) | not-a-kernel (record: SEM016 staged walk; no typed leaf) | — | `⇥`, walk | — | — | — | — |
| `matmul` (501) | not-a-kernel (record: SEM016 staged walk; no typed leaf) | — | `⇥`, walk | — | — | — | — |
| `_dtype_from_name` (542) | not-a-kernel | — | dtype policy | — | — | — | — |
| `cast` (547) | not-a-kernel | — | dtype conversion | — | — | — | — |
| `_shape_dim` (568) | not-a-kernel | — | shape policy | — | — | — | — |
| `_part_at` (580) | not-a-kernel | — | index policy | — | — | — | — |
| `_elem_at` (592) | not-a-kernel | — | index policy | — | — | — | — |
| `concatenate` (604) | not-a-kernel (record: SEM016 staged walk; no typed leaf) | — | `⇥`, walk | — | — | — | — |
| `slice` (664) | not-a-kernel (record: SEM016 staged walk; no typed leaf) | — | `⇥`, walk | — | — | — | — |

## 5. `src/model/dense.fab` — 46 declarations

| function (line) | class | leaves | wrapper keeps | hole | 2nd caller | launch claim | packet |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `from_tensor_error` (158) | not-a-kernel | — | error mapping | — | — | — | — |
| `from_nn_error` (163) | not-a-kernel | — | error mapping | — | — | — | — |
| `from_transformer_error` (171) | not-a-kernel | — | error mapping | — | — | — | — |
| `from_kv_cache_error` (176) | not-a-kernel | — | error mapping | — | — | — | — |
| `_shape_text` (188) | not-a-kernel | — | diagnostics | — | — | — | — |
| `_shape` (203) | not-a-kernel | — | diagnostics | — | — | — | — |
| `_token_major_view` (212) | not-a-kernel | — | view policy | — | — | — | — |
| `_transpose` (223) | not-a-kernel | `nn.transpose_carrier` | view walk | — | — | — | — |
| `_collect` (228) | not-a-kernel | `nn.gather_carrier` | row gather walk | — | — | — | — |
| `gather` (234) | not-a-kernel (record: SEM016 — literal-shape pins by design) | `nn.gather_carrier` | `⇥`, pin | — | — | — | — |
| `gather_step` (240) | not-a-kernel (record: SEM016) | `nn.gather_carrier` | `⇥`, pin | — | — | — | — |
| `_no_bias` (248) | not-a-kernel | — | bias-presence policy (host chooses tensor) | `source()` resolver | — | — | — |
| `_channel_to_rows` (255) | not-a-kernel | — | bias reshape policy | — | — | — | — |
| `_attn_bias` (276) | not-a-kernel | — | bias-presence policy | `source()` resolver | — | — | — |
| `_probe_bias` (412) | not-a-kernel | — | bias-presence policy (resolver probe) | `source()` resolver | — | — | — |
| `_rmsnorm` (293) | not-a-kernel (record: SEM016; typed runners already use glyphs + static twins) | `nn.rmsnorm_carrier` | `⇥` mapping | — | — | — | — |
| `_linear` (298) | not-a-kernel (record: SEM016) | `nn.linear_carrier` | `⇥` mapping | — | — | — | — |
| `_block` (304) | not-a-kernel (delegates) | `transformer.dense_block` | `⇥` mapping | — | — | — | — |
| `_map_cached` (311) | not-a-kernel | — | cache mapping | — | — | — | — |
| `_shared_prefix` (318) | not-a-kernel | — | cache policy | — | — | — | — |
| `_admit_cached` (328) | not-a-kernel | — | cache admit | — | — | — | — |
| `_block_cached` (335) | not-a-kernel (delegates) | `transformer.dense_block_cached` | `⇥` mapping | — | — | — | — |
| `_require_cfg` (346) | not-a-kernel | — | config policy | — | — | — | — |
| `_require_ref01` (357) | not-a-kernel | — | config policy | — | — | — | — |
| `_zeros_rank1` (366) | not-a-kernel | — | pin helper | — | — | — | — |
| `_pin_rank1` (374) | not-a-kernel | — | pin helper | — | — | — | — |
| `_pin_rank2` (384) | not-a-kernel | — | pin helper | — | — | — | — |
| `_pin_same` (394) | not-a-kernel | — | pin helper | — | — | — | — |
| `_pin_same_rank1` (403) | not-a-kernel | — | pin helper | — | — | — | — |
| `load` (432) | not-a-kernel (loader) | — | `⇥`, resolver, pins | `source()` | — | — | — |
| `probe_load_layer_count` (502) | not-a-kernel | — | probe (SEM008 sentinel) | — | — | — | — |
| `probe_layer_rms_len` (510) | not-a-kernel | — | probe | — | — | — | — |
| `_typed_ref01` (522) | not-a-kernel | — | record conversion; the only in-repo `TypedDenseLayer` constructor — builds from loaded fields, so every in-repo static-twin consumer runs absent-bias layers unless a fixture constructs a present-bias record directly | — | — | — | — |
| `probe_typed_block_static` (535) | not-a-kernel | static twins | probe (SEM016 sentinel) | — | — | — | — |
| `probe_inferred_leaves` (550) | not-a-kernel | leaves/glyphs already | probe | — | — | — | — |
| `forward_ref01` (569) | not-a-kernel (typed driver over already-split static twins) | `dense_block_static`, `.rms_norm`, `·` | `⇥`, load, per-layer loop | `list.append` layer loop | — | — | — |
| `decode_step_ref01` (593) | not-a-kernel (typed driver; session driver shape) | `dense_block_cached_static` | `⇥`, load, loop | `list.append` layer loop | — | — | — |
| `prefill_ref01` (627) | not-a-kernel (typed driver; session driver shape) | `dense_block_cached_static` | `⇥`, load, loops | `list.append` layer loop | — | — | — |
| `forward` (678) | not-a-kernel (record: SEM016 bag route; dense-typed-assembly unit 5) | carrier twins via wrappers | `⇥`, resolver, bias policy, loops | `source()`, bags | — | — | — |
| `DenseStep.logits` (773) | not-a-kernel | — | record projection | — | — | — | — |
| `DenseStep.layers` (777) | not-a-kernel | — | record projection | — | — | — | — |
| `default_step` (783) | not-a-kernel | — | constructor | — | — | — | — |
| `empty_caches` (788) | not-a-kernel | — | cache policy | — | — | — | — |
| `decode_step` (793) | not-a-kernel (session driver) | as `forward` | `⇥`, cache policy, loop | cache mutation, `source()` | — | — | — |
| `decode_block` (894) | not-a-kernel (session driver) | as `forward` | `⇥`, cache policy, loops | cache mutation, `source()` | — | — | — |
| `prefill_cached` (998) | not-a-kernel (session driver) | as `forward` | `⇥`, cache policy, loops | cache mutation, `source()` | — | — | — |

## 6. `src/decode.fab` — 55 declarations

| function (line) | class | leaves | wrapper keeps | hole | 2nd caller | launch claim | packet |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `from_transformer_error` (144) | not-a-kernel | — | error mapping | — | — | — | — |
| `from_nn_error` (162) | not-a-kernel | — | error mapping | — | — | — | — |
| `from_tensor_error` (177) | not-a-kernel | — | error mapping | — | — | — | — |
| `Weights.ln1_s` (214) | not-a-kernel | — | record projection | — | — | — | — |
| `Weights.ln1_o` (218) | not-a-kernel | — | record projection | — | — | — | — |
| `Weights.wq` (222) | not-a-kernel | — | record projection | — | — | — | — |
| `Weights.bq` (226) | not-a-kernel | — | record projection | — | — | — | — |
| `Weights.wk` (230) | not-a-kernel | — | record projection | — | — | — | — |
| `Weights.bk` (234) | not-a-kernel | — | record projection | — | — | — | — |
| `Weights.wv` (238) | not-a-kernel | — | record projection | — | — | — | — |
| `Weights.bv` (242) | not-a-kernel | — | record projection | — | — | — | — |
| `Weights.wo` (246) | not-a-kernel | — | record projection | — | — | — | — |
| `Weights.bo` (250) | not-a-kernel | — | record projection | — | — | — | — |
| `Weights.ln2_s` (254) | not-a-kernel | — | record projection | — | — | — | — |
| `Weights.ln2_o` (258) | not-a-kernel | — | record projection | — | — | — | — |
| `Weights.wf1` (262) | not-a-kernel | — | record projection | — | — | — | — |
| `Weights.bf1` (266) | not-a-kernel | — | record projection | — | — | — | — |
| `Weights.wf2` (270) | not-a-kernel | — | record projection | — | — | — | — |
| `Weights.bf2` (274) | not-a-kernel | — | record projection | — | — | — | — |
| `Weights.ln3_s` (278) | not-a-kernel | — | record projection | — | — | — | — |
| `Weights.ln3_o` (282) | not-a-kernel | — | record projection | — | — | — | — |
| `construct_weights` (290) | not-a-kernel | — | constructor | — | — | — | — |
| `Decoder.table` (315) | not-a-kernel | — | record projection | — | — | — | — |
| `Decoder.weights` (320) | not-a-kernel | — | record projection | — | — | — | — |
| `Decoder.projection` (325) | not-a-kernel | — | record projection | — | — | — | — |
| `Decoder.projection_bias` (330) | not-a-kernel | — | record projection | — | — | — | — |
| `Decoder.scale` (335) | not-a-kernel | — | record projection | — | — | — | — |
| `Decoder.vocabulary` (340) | not-a-kernel | — | record projection | — | — | — | — |
| `Decoder.context` (345) | not-a-kernel | — | record projection | — | — | — | — |
| `Decoder.dimension` (350) | not-a-kernel | — | record projection | — | — | — | — |
| `construct_decoder` (356) | not-a-kernel | — | constructor | — | — | — | — |
| `default` (384) | not-a-kernel | — | constructor | — | — | — | — |
| `_tensor` (395) | not-a-kernel | — | staging walk | — | — | — | — |
| `_embedding` (400) | not-a-kernel | — | row gather walk | — | — | — | — |
| `_block` (410) | not-a-kernel (delegates; SEM016 carriers) | `transformer.transformer_block` | `⇥` mapping | — | — | — | — |
| `_project` (416) | not-a-kernel (delegates; SEM016 carriers) | `nn.linear_carrier` | `⇥` mapping | — | — | — | — |
| `decode_data` (428) | not-a-kernel (session driver) | via delegates | `⇥`, domain policy, loop | — | — | — | — |
| `DecodeData.logits` (457) | not-a-kernel | — | record projection | — | — | — | — |
| `DecodeData.state` (461) | not-a-kernel | — | record projection | — | — | — | — |
| `default_step` (467) | not-a-kernel | — | constructor | — | — | — | — |
| `_block_cached` (471) | not-a-kernel (delegates; SEM016 carriers) | `transformer.transformer_block_cached` | `⇥` mapping | — | — | — | — |
| `decode_cached` (477) | not-a-kernel (session driver) | via delegates | `⇥`, cache policy, loop | cache mutation | — | — | — |
| `prefill` (502) | not-a-kernel (session driver) | via delegates | `⇥`, cache policy, loop | cache mutation | — | — | — |
| `Session.position` (542) | not-a-kernel | — | record projection | — | — | — | — |
| `Session.context` (547) | not-a-kernel | — | record projection | — | — | — | — |
| `fresh_session` (554) | not-a-kernel | — | session policy | — | — | — | — |
| `default_session` (563) | not-a-kernel | — | session policy | — | — | — | — |
| `advance` (570) | not-a-kernel | — | session policy | — | — | — | — |
| `reset` (577) | not-a-kernel | — | session policy | — | — | — | — |
| `Cancellation.cancelled` (596) | not-a-kernel | — | record projection | — | — | — | — |
| `fresh_cancellation` (603) | not-a-kernel | — | cancellation policy | — | — | — | — |
| `cancellation_cancelled` (609) | not-a-kernel | — | cancellation policy | — | — | — | — |
| `observe_cancellation` (617) | not-a-kernel | — | cancellation policy | — | — | — | — |
| `_sampling_map` (634) | not-a-kernel | — | sampling policy map | — | — | — | — |
| `replay` (639) | not-a-kernel (sampling replay driver) | `sampling` | `⇥`, sampling | — | — | — | — |

## 7. `src/generation.fab` — 77 declarations

All rows: session/loop drivers, cursor + wire policy, sampling admit, speculative commit. Tensor math appears only through `decode`/`dense` delegates and list walks. Nothing carded.

| function (line) | class | leaves | wrapper keeps | hole | 2nd caller | launch claim | packet |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `acceleration_disabled` (172) | not-a-kernel | — | policy | — | — | — | — |
| `acceleration_context_lookup` (177) | not-a-kernel | — | policy | — | — | — | — |
| `acceleration_mode_name` (182) | not-a-kernel | — | policy | — | — | — | — |
| `_acceleration_mode_from_name` (193) | not-a-kernel | — | policy | — | — | — | — |
| `AccelerationPolicy.version` (206) | not-a-kernel | — | record projection | — | — | — | — |
| `AccelerationPolicy.mode` (210) | not-a-kernel | — | record projection | — | — | — | — |
| `AccelerationPolicy.min_block` (214) | not-a-kernel | — | record projection | — | — | — | — |
| `AccelerationPolicy.max_block` (218) | not-a-kernel | — | record projection | — | — | — | — |
| `construct_acceleration` (224) | not-a-kernel | — | constructor | — | — | — | — |
| `default_acceleration` (233) | not-a-kernel | — | constructor | — | — | — | — |
| `acceleration_equal` (238) | not-a-kernel | — | identity policy | — | — | — | — |
| `GenerationConfig.context` (265) | not-a-kernel | — | record projection | — | — | — | — |
| `GenerationConfig.max_prompt` (270) | not-a-kernel | — | record projection | — | — | — | — |
| `GenerationConfig.max_tokens` (274) | not-a-kernel | — | record projection | — | — | — | — |
| `GenerationConfig.seed` (278) | not-a-kernel | — | record projection | — | — | — | — |
| `GenerationConfig.temperature` (283) | not-a-kernel | — | record projection | — | — | — | — |
| `GenerationConfig.top_k` (288) | not-a-kernel | — | record projection | — | — | — | — |
| `GenerationConfig.top_p` (293) | not-a-kernel | — | record projection | — | — | — | — |
| `GenerationConfig.min_p` (298) | not-a-kernel | — | record projection | — | — | — | — |
| `GenerationConfig.repetition_penalty` (303) | not-a-kernel | — | record projection | — | — | — | — |
| `GenerationConfig.acceleration` (307) | not-a-kernel | — | record projection | — | — | — | — |
| `generation_equal` (314) | not-a-kernel | — | identity policy | — | — | — | — |
| `construct_generation_with_policy` (334) | not-a-kernel | — | constructor | — | — | — | — |
| `construct_generation` (356) | not-a-kernel | — | constructor | — | — | — | — |
| `default` (365) | not-a-kernel | — | constructor | — | — | — | — |
| `generation_failure` (377) | not-a-kernel | — | error mapping | — | — | — | — |
| `support_flags` (388) | not-a-kernel | — | config policy | — | — | — | — |
| `admitted_features` (394) | not-a-kernel | — | config policy | — | — | — | — |
| `config` (405) | not-a-kernel | — | config policy | — | — | — | — |
| `seed` (419) | not-a-kernel | — | config policy | — | — | — | — |
| `_serialize_acceleration` (436) | not-a-kernel | — | wire render | — | — | — | — |
| `serialize_generation` (441) | not-a-kernel | — | wire render | — | — | — | — |
| `_digit` (446) | not-a-kernel | — | wire parse | — | — | — | — |
| `_numeric` (450) | not-a-kernel | — | wire parse | — | — | — | — |
| `_wire_int` (460) | not-a-kernel | — | wire render | — | — | — | — |
| `_wire_f32` (471) | not-a-kernel | — | wire render | — | — | — | — |
| `_deserialize_acceleration` (481) | not-a-kernel | — | wire parse | — | — | — | — |
| `deserialize_generation` (492) | not-a-kernel | — | wire parse | — | — | — | — |
| `GenerationCursor.session` (545) | not-a-kernel | — | record projection | — | — | — | — |
| `GenerationCursor.emitted` (550) | not-a-kernel | — | record projection | — | — | — | — |
| `fresh_cursor` (557) | not-a-kernel | — | cursor policy | — | — | — | — |
| `default_cursor` (573) | not-a-kernel | — | cursor policy | — | — | — | — |
| `token_allowed` (581) | not-a-kernel | — | cursor policy | — | — | — | — |
| `cursor_advance` (591) | not-a-kernel | — | cursor policy | — | — | — | — |
| `cursor_reset` (600) | not-a-kernel | — | cursor policy | — | — | — | — |
| `cursor_after_prompt` (682) | not-a-kernel | — | cursor policy | — | — | — | — |
| `_advance_n` (783) | not-a-kernel | — | cursor policy | — | — | — | — |
| `eog_stop` (622) | not-a-kernel | — | stop policy | — | — | — | — |
| `ignore_eos` (627) | not-a-kernel | — | stop policy | — | — | — | — |
| `stop_policy_name` (632) | not-a-kernel | — | stop policy | — | — | — | — |
| `stops_on_eog` (644) | not-a-kernel | — | stop policy | — | — | — | — |
| `_suppress_eog` (657) | not-a-kernel (list walk) | — | stop policy walk | — | — | — | — |
| `_sample_logits` (671) | not-a-kernel (list walk over carriers) | — | sampling policy walk | — | — | — | — |
| `_observe` (692) | not-a-kernel (sampling admit) | `sampling` | `⇥` mapping | — | — | — | — |
| `_sample` (702) | not-a-kernel (sampling admit) | `sampling` | `⇥` mapping | — | — | — | — |
| `_prefill` (711) | not-a-kernel (delegate) | `decode.*` | `⇥` mapping | — | — | — | — |
| `_decode_one` (720) | not-a-kernel (delegate) | `decode.*` | `⇥` mapping | — | — | — | — |
| `_dense_one` (753) | not-a-kernel (delegate) | `dense.*` | `⇥` mapping | — | — | — | — |
| `_dense_prefill` (762) | not-a-kernel (delegate) | `dense.*` | `⇥` mapping | — | — | — | — |
| `_last_logits` (729) | not-a-kernel (record: carrier walk) | — | row selection walk | — | — | — | — |
| `_logit_row` (791) | not-a-kernel (record: carrier walk) | — | row selection walk | — | — | — | — |
| `_slice_rows` (897) | not-a-kernel (record: carrier walk) | — | row selection walk | — | — | — | — |
| `_prefix` (771) | not-a-kernel | — | list helper | — | — | — | — |
| `_target_ids` (807) | not-a-kernel (speculative commit policy) | `sampling` | `⇥`, commit policy | — | — | — | — |
| `_accepted_prefix` (817) | not-a-kernel (speculative commit policy) | — | commit policy | — | — | — | — |
| `_lookup_context` (830) | not-a-kernel (speculative commit policy) | `context_lookup` | `⇥`, commit policy | — | — | — | — |
| `_accepted_target_count` (841) | not-a-kernel (speculative commit policy) | — | commit policy | — | — | — | — |
| `_lookup_candidates` (855) | not-a-kernel (speculative commit policy) | `context_lookup` | `⇥`, commit policy | — | — | — | — |
| `_commit_dense_block` (914) | not-a-kernel (speculative commit policy) | `sampling`, cache rollback contract | `⇥`, cache checkpoint/commit | cache mutation | — | — | — |
| `generate` (945) | not-a-kernel (generation loop) | via delegates | the loop | loop control, caches | — | — | — |
| `generate_with_stop` (950) | not-a-kernel (generation loop) | via delegates | the loop | loop control, caches | — | — | — |
| `generate_cancelled` (955) | not-a-kernel (generation loop) | via delegates | the loop | loop control, caches | — | — | — |
| `generate_cancelled_with_stop` (960) | not-a-kernel (generation loop) | via delegates | the loop | loop control, caches | — | — | — |
| `generate_dense` (1024) | not-a-kernel (generation loop) | via delegates | the loop | loop control, caches | — | — | — |
| `generate_dense_with_stop` (1029) | not-a-kernel (generation loop) | via delegates | the loop | loop control, caches | — | — | — |
| `construct_dense_engine` (1008) | not-a-kernel | — | constructor | — | — | — | — |
| `default_dense_engine` (1013) | not-a-kernel | — | constructor | — | — | — | — |

## 8. Siblings composing tensor math — plus excluded classes with reasons

Filter (the need's own scope): sibling modules contribute one row per function that composes tensor math (leaf calls, glyphs, or carrier tensor walks). Modules and functions with no tensor-math composition get an explicit exclusion row with the reason — nothing is silently dropped.

| function (line) | class | leaves | wrapper keeps | hole | 2nd caller | launch claim | packet |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `gradient.fab` `simple_loss` (219) | not-a-kernel (autograd-companion ABI: `@ radix { lane = "air" }` + `@ radix backward "loss_backward"` + `@ public`; body is direct typed tensor math — `x ⊙ w`, `.mean()`; same class as `mlp.forward_mlp_loss`; training-path lowering, not an `@ kernel` fusion surface — recorded, not converted) | — | `@ radix` annotations | — | — | — | — |
| `gradient.fab` `masked_mean` (279) | not-a-kernel (autograd-companion ABI: `@ radix backward "masked_mean_backward"`; body `x ⊙ mask`, `.mean()`) | — | `@ radix` annotations | — | — | — | — |
| `gradient.fab` `gradients_simple_loss` (243) | not-a-kernel (companion invocation + staged-carrier packaging; `require` fail-closed + `tensor.construct` staging — no math composition) | — | identity policy, staging | — | — | — | — |
| `gradient.fab` `gradients_masked_mean` (292) | not-a-kernel (companion invocation + packaging) | — | identity policy, staging | — | — | — | — |
| `mlp.fab` `_linear` (105) | not-a-kernel (record: SEM016 carriers) | carrier twins | `⇥` mapping | — | — | — | — |
| `mlp.fab` `_gelu` (110) | not-a-kernel (record: SEM016 carriers) | carrier twins | `⇥` mapping | — | — | — | — |
| `mlp.fab` `forward_mlp` (128) | not-a-kernel (record: SEM016 — typed twin `forward_mlp_loss` exists on the `@ radix backward` training path) | carrier twins | `⇥` | carrier pin | — | — | — |
| `mlp.fab` `forward_mlp_loss` (161) | not-a-kernel (autograd-companion ABI — `@ radix backward "forward_mlp_loss_backward"`; training path, not a fusion surface; the precedent the gradient rows above follow) | glyph body | `@ radix` annotations | — | — | — | — |
| `mlp.fab` `nil` (141) | not-a-kernel | — | ABI residual | — | — | — | — |
| `loss.fab` `mse` (195) | not-a-kernel (record: SEM016 staged walk; typed `mse_*` kernels exist for fixed shapes) | — | `⇥`, walk | carrier pin | — | — | — |
| `loss.fab` `cross_entropy` (229) | not-a-kernel (record: SEM016 staged walk) | — | `⇥`, walk | carrier pin | — | — | — |
| `loss.fab` `mse_2x2` (278) | already-kernel (`@ kernel` leaf) | — | — | — | — | — | — |
| `loss.fab` `mse_4x4` (290) | already-kernel (`@ kernel` leaf) | — | — | — | — | — | — |
| `loss.fab` `mse_2x8` (302) | already-kernel (`@ kernel` leaf) | — | — | — | — | — | — |
| `metrics.fab` `accuracy` (85) | not-a-kernel (record: carrier walk + i32 target policy) | — | `⇥`, argmax policy | — | — | — | — |
| `model/moe.fab` `route` (204) | not-a-kernel (record: resolver + list softmax walk) | — | `⇥`, `source()` | `source()` | — | — | — |
| `model/moe.fab` `expert_out` (304) | not-a-kernel (record: SEM016 — runtime-shape matmul via `math.matmul` carriers, resolver windows, accumulation loop) | `nn.swiglu` (carrier) | `⇥`, resolver, finite checks | `source()`, loops | — | — | — |
| `model/moe.fab` `ffn_moe` (375) | not-a-kernel (record: SEM016 — expert loop over carrier routes) | `nn.swiglu` (carrier) | `⇥`, resolver, loops | `source()`, loops | — | — | — |
| `model/moe.fab` `_router_logits` (147) | not-a-kernel (record: carrier walk) | — | router walk | — | — | — | — |
| `model/moe.fab` `_column` (139) | not-a-kernel (record: carrier walk) | — | column walk | — | — | — | — |
| `model/moe.fab` `_softmax` (151) | not-a-kernel (record: list softmax walk) | — | walk | — | — | — | — |
| `model/moe.fab` `_best_index` (184) | not-a-kernel (record: argmax walk) | — | walk | — | — | — | — |
| `model/moe.fab` `_sigmoid` (333) | not-a-kernel (scalar walk) | — | scalar | — | — | — | — |
| `model/moe.fab` `_dot` (337) | not-a-kernel (record: dot walk) | — | walk | — | — | — | — |
| `model/moe.fab` `_project` (250) | not-a-kernel (record: carrier matmul walk) | — | walk | — | — | — | — |
| `model/moe.fab` `_row` (257) | not-a-kernel (record: row walk) | — | walk | — | — | — | — |
| `model/moe.fab` `_linear_weight` (271) | not-a-kernel (record: resolver window walk) | — | walk | — | — | — | — |
| `model/moe.fab` `_swiglu_no_bias` (288) | not-a-kernel (record: carrier swiglu walk) | — | walk | — | — | — | — |
| `model/moe.fab` `_flatten_row` (292) | not-a-kernel (record: list flatten walk) | — | walk | — | — | — | — |
| `train.fab` `train_step_2x2` (67) | not-a-kernel (training-loop mechanics; delegates to `optimize.sgd_step_*`, not `@ kernel`; no device launch surface) | `optimize.sgd_step_2x2` | none (`⇥`-free) | in-body calls to non-kernel leaves | — | — | — |
| `train.fab` `train_step_4x4` (79) | not-a-kernel (same) | `optimize.sgd_step_4x4` | none | same | — | — | — |
| `train.fab` `train_step_bert_linear` (97) | not-a-kernel (same; 12-param SGD update) | `optimize.sgd_family` glyphs | none | same | — | — | — |
| `train.fab` `train_step_bert_layernorm` (113) | not-a-kernel (same; 6-param SGD update) | `optimize.sgd_family` glyphs | none | same | — | — | — |
| `optimize.fab` `_sgd_family` (119) | not-a-kernel (record: `list.append` loop + `seed.create` fill; glyph-leaf law could later admit a typed SGD leaf — no second caller today, no card) | `−`, `⊙` glyphs | list loop | `list.append` | no | none | — (record; no card) |
| `optimize.fab` `sgd_step_2x2` (137) | not-a-kernel (same shape, fixed 2×2) | `−`, `⊙` | list loop | `list.append` | no | none | — |
| `optimize.fab` `sgd_step_4x4` (149) | not-a-kernel (same shape, fixed 4×4) | `−`, `⊙` | list loop | `list.append` | no | none | — |

Excluded classes, each with its reason (the need's "record and skip" territory — tree rules 1/5):

| excluded | reason |
| --- | --- |
| `gradient.fab` record/ABI fns: `from_tensor_error` (89), `Gradient.owner/name/version/payload` (115–130), `construct` (139), `default` (149), `Gradients.count/find` (165–170), `construct_gradients` (180), `obsolete` (193), `nil` (204) | record projections and capsule constructors — no tensor-math composition (admitted module; non-math remainder excluded row-wise) |
| `mlp.fab` `from_nn_error` (76) | error mapping — no tensor-math composition |
| `loss.fab` `from_shape_error` (98), `_numel_valid` (129), `_dtype_pair` (135), `_dtype_f32` (144), `_exp` (156), `_log` (165) | scalar/policy helpers — no tensor-math composition |
| `metrics.fab` `Metric.loss/accuracy` (132–137), `metric` (145), `default` (156), `metric_equal` (162) | record/policy projections — no tensor-math composition |
| `model/moe.fab` `from_math_error` (47), `from_nn_error` (52), `RouteGenus.indices/weights/logits/probabilities` (63–75), `_finite_tensor` (82), `_validate_config` (89), `_validate_input` (99), `_window` (109), `_prefix` (120), `_router_weights` (126), `_exp` (135), `_scalar` (348), `_zeros` (359) | validation/policy/scalar helpers and record projections — no carded tensor-math composition |
| `train.fab` non-step fns (schedules `construct_schedule`/`default_schedule`/`scheduled_rate`/`_cos`, dropout family, rng family, checkpoint family, wire helpers, `from_tensor_error`) | training-loop policy — no tensor-math composition |
| `optimize.fab` non-step fns (`from_parameter_error` … `deserialize`, parameter-state records, `state_equal`, `add`, `step` plumbing) | parameter-state policy/records — no tensor-math composition |
| `sampling.fab` (all) | sampling — tree rule 5 |
| `model/dequant.fab` (all) | byte parsers — tree rule 5 |
| `model/dense_llama.fab`, `dense_qwen2.fab`, `gguf*.fab`, `qwen35moe*.fab` (resolve/config/admit/reference/canonical) | loaders/resolvers/manifests — tree rule 5 |
| `block_verify.fab`, `calibration.fab`, `speculative.fab`, `prepared_state.fab`, `context_lookup.fab`, `cache.fab`, `cache_branch.fab` | verify/calibration/admission/identity policy — tree rule 5 |
| `tensor.fab`, `dtype`/`shape`/`tensor` infra modules | value/container infrastructure, not ML math — outside the need's surface |
| `src/kernel.fab` GEA3 entries | frozen launch catalog; generic code never calls it — need rule 1 |

## 9. Census totals (recomputed from the one-row ledger)

- Ledger size: **319 rows** over the seven named files (25 + 50 + 33 + 33 + 46 + 55 + 77 — matches `grep -cE '^\s*fn '` per file) plus 36 sibling tensor-math rows and 13 exclusion rows above. Every declaration is in exactly one row; every exclusion carries a reason.
- Dispatchable conversion families: 4 → cards KRS-2..KRS-5. KRS-2 covers **six** `nn.fab` functions (five carrier-detour reroutes + the `linear_4x4` `@ kernel` annotation admitted by this reissue).
- Deferred hole family: 1 (attention multi-head parent, uncached + cached variants) → KRS-6, blocked on the column-slice admission.
- Kernel-closure class: **0 live sites** — re-issued against the corrected one-row ledger (including the newly admitted `gradient.fab` rows, which are `@ radix` companions and not closure candidates). Every one-off candidate dissolved under verification into either a direct leaf call (KRS-2 rows) or a second-caller region (KRS-3/KRS-4). `ef103950` gates nothing dispatched today; hands that later find a genuine one-off note it on the card and defer (mind routing).
- Recorded-not-converted (convert-or-record, reason in code at conversion time where a hand touches the site): the SEM014/SEM016/SEM008 carrier seams (`transformer.fab` bag wrappers, `model/dense.fab` bag routes, `math`/`nn`/`attention` carrier twins, `mlp`/`loss`/`metrics`/`moe` walks), session drivers, loaders, sampling, parsers, and the autograd-companion ABI surfaces (`gradient.fab` `simple_loss`/`masked_mean` + companions, `mlp.forward_mlp_loss`).
