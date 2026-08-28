# kernel-region-split unit cards

Delivery lowering for need `3b9e5796`, task `c78bb834`. Cards descend from [`census.md`](census.md) (KRS-1, landed; reissued 2026-08-28 under REVISE `1ddc4077` — one-row-per-function ledger, `gradient.fab` admitted, `linear_4x4` reclassified, dense-tail anchors corrected, attention posture corrected; see census §0a). Standing law cited on every card: **`kernel-region-split`** — `~/work/ianzepp/skills/faber/canonical-faber/references/patterns.md` §kernel-region-split (tentative, operator 2026-08-28) + `SKILL.md` §14, including the settled tensor-glyph device rules (postfix `ᵀ` over `.transpose()` for legal rank-2 transposes in kernel bodies). Promotion to settled happens after the first green conversion unit (KRS-2..KRS-5 ledger in [`GOAL.md`](GOAL.md)); it is a campaign milestone, not a unit.

Operator routing (binding): cards run parallel with the `ef103950` closure landing; closure-class rows are carded-but-deferred — the reissued census found **zero live closure-class sites**, so nothing dispatched below waits on `ef103950`. A conversion hand that finds a function better suited to closure syntax notes + defers it on the card; a later separate hand session implements deferred conversions after `ef103950` is green.

Standing `non_goals` on every card: no GEA3 `kernel.fab` rewrite unless the card names it; no 2,115/encoder-delta claim without an export seam; no `@ kernel` on a `⇥` function; no `do kernel`.

Lane gates named once (not on any card): lint owns `./scripta/check-source`; test owns broad suites; merge owns `./scripta/check-compile` closeout and atomic landing on `main`.

---

## KRS-1 — census (landed; reissued)

| field | value |
| --- | --- |
| outcome | Live-verified census of the seven named files + tensor-math siblings; starter rows corrected against source |
| write_scope | `gradus/docs/factory/kernel-region-split/**` |
| done_when | Census table complete, every function one row, corrections recorded (§0) |
| depends_on | — |
| status | **done** — planner, `f494db2`. **Amendment (append-only, 2026-08-28):** reissued under REVISE `1ddc4077` as a one-row-per-declaration ledger (319 rows over the seven files + siblings), `gradient.fab` admitted as autograd-companion ABI rows, `nn.linear_4x4` reclassified annotation-capable, dense-tail/attention anchors corrected — census §0a; totals recomputed §9 |

---

## KRS-2 — `nn.fab` fixed-shape adapters: five reroutes + one annotation

| field | value |
| --- | --- |
| `id` | KRS-2 |
| outcome | Six public fixed-shape adapters, one family: `linear_2x2`, `linear_2x8`, `gelu_4x4`, `gelu_2x8`, `layernorm_2x8` stop staging through `NumericBlock` carriers (`_staged` → `*_carrier` → pin detours) and compute via typed leaves/method twins; **and `linear_4x4` (:123) gains `@ kernel`** — it is public, `⇥`-free, and its whole body is `return linear(input, weight, bias)`, a call to the `@ kernel` leaf, so the glyph-leaf rule applies to the wrapper itself (reclassified per census §0a; annotation alongside its `@ public`, matching `nn.linear`'s dual marking). No reroute needed for `linear_4x4` — it has no carrier detour |
| `class` | reuse-leaves (tree rule 1 — five reroutes; glyph-leaf annotation for `linear_4x4`) |
| `leaves_reused` | `nn.linear<M,K,N>`, `nn.gelu<M,N>`, `·` + `.added_bias` (S6-C2 per-channel contract), `.layer_norm(1, ε, s, o)` method twin |
| `wrapper_vs_region` | wrappers `linear_2x2`/`linear_2x8`/`gelu_4x4`/`gelu_2x8`/`layernorm_2x8` → region = the existing public typed leaves (no new function); `linear_4x4` → itself becomes the `@ kernel` region (annotation only) |
| `hole` | none |
| `second caller?` | no — direct leaf calls / annotation; no region minted |
| `launch claim` | none (source-only; no export/plan change) |
| `write_scope` | `gradus/src/nn.fab` (proof surface `exempla/nn-bridge` is run read-only; no bridge edit is needed for the proof — if one turns out to be required, stop and report rather than widening scope) |
| `done_when` | The five rerouted adapters return identical bytes on the bridge rows; no `_staged`/`*_carrier` detour remains in those five bodies; `linear_4x4` carries `@ kernel` (with `@ public` kept); `linear_2x8` keeps the per-channel `[8]` bias contract; the known pre-existing red is recorded, not fixed and not claimed green |
| `depends_on` | — (parallel-safe with KRS-3: disjoint files) |
| `sanity` | `faber check` on `src/nn.fab` green; bridge run before/after prints identical pins |
| `oracle` | The adapter proof surface is **`exempla/nn-bridge`**, not `src/nn.proba`: the proba suite pins the generic leaves (`linear`, `gelu`, `layernorm` carrier family) only — it never calls the fixed-shape adapters (its headers say so: nn.proba:19–20). The bridge package calls all six adapters end-to-end (`exempla/nn-bridge/src/main.fab`: `bridge_linear_2x2` :103, `nn.linear_4x4` :185, `bridge_linear_2x8` :113, `bridge_gelu_4x4` :123, `bridge_gelu_2x8` :133, `bridge_layernorm_2x8` :143). Proof: run `faber check exempla/nn-bridge` + `faber run --target fmir exempla/nn-bridge` **before** the change, record the printed pins, rerun **after**, require identical printed values (byte identity of outputs, pins exact for linear rows, `5e-4` tolerance rows for gelu/layernorm per the bridge's own contract). **Baseline honesty:** the typed `linear_2x2` matmul path is a **pre-existing red** (README:32–34: "do not claim this package green") — the receipt records that red as baseline, does not fix it here, and claims only "pins identical to the pre-change bridge run", never package green. `nn.proba` leaf rows stay green (they are untouched by this card) |
| `non_goals` | standing set + no carrier-twin deletion (`linear_carrier`/`gelu_carrier`/`layernorm` keep their load-edge callers), no SEM014/SEM016 pin work, no edit to `exempla/nn-bridge`, no fix for the pre-existing `linear_2x2` bridge red (separately owned), no change to `linear_from_raw` (load-edge pin wrapper; no conversion owed) |
| `risk` | low — arithmetic-identical rerouting through existing kernels plus one annotation; the only trap is misreporting the known red |
| `integrable` | yes |

---

## KRS-3 — `transformer.fab` named private `@ kernel dense_mlp` shared by both static block twins

| field | value |
| --- | --- |
| `id` | KRS-3 |
| outcome | The SwiGLU+residual **arithmetic core** shared by `dense_block_static` (tail arithmetic 658–662) and `dense_block_cached_static` (tail arithmetic 694–698) — the same gate/up/`nn.swiglu_hidden`/down-projection/residual-add statements over typed tensors — becomes one private `@ kernel dense_mlp<T, D, F>(residual, ln2, wg, wu, wd)` returning the output tensor; both twins call it. **Not byte-identical tails** (corrected per census §0a): the uncached twin returns the tensor directly (:662); the cached twin wraps it — `TypedCachedBlock { output = …, state = step.state() }` (:698) — and that per-wrapper return shape stays on the wrappers |
| `class` | named-private-kernel (tree rule 2 — two callers share the region; `@ kernel`, not `@ public`) |
| `leaves_reused` | `nn.swiglu_hidden<T,F>`, `math.add<T,D>`, `·` |
| `wrapper_vs_region` | wrappers `dense_block_static` / `dense_block_cached_static`; region `dense_mlp` (new, private, same file) |
| `hole` | the bag attention call — `_multi_attention` / `_multi_attention_cached` stays on the wrappers (argument-shaped boundary: wrapper pins `ctx` and passes it to the region's residual input) |
| `second caller?` | yes — the two static twins (this is why named private, not closure) |
| `launch claim` | none (inlining inside parents that are not launched moves nothing in the GEA graph — need rule 7) |
| `write_scope` | `gradus/src/transformer.fab`, `gradus/src/transformer.proba` |
| `done_when` | Both static twins call `dense_mlp`; `dense_mlp` is `@ kernel` and private; tail arithmetic unchanged; each wrapper keeps its own output contract (tensor vs `TypedCachedBlock` output+state); dense-block proba rows and `model/dense.proba` REF-01 rows byte-identical |
| `depends_on` | — |
| `sanity` | `faber check` on `src/transformer.fab` green |
| `oracle` | focused proba tuples byte-identical — transformer dense-block carrier rows in `src/transformer.proba`, and the REF-01 consumer rows in `src/model/dense.proba` (:535–571+: `forward_ref01` tied/untied logits, `prefill_ref01` + two `decode_step_ref01` steps) which drive both static twins through the typed runners; `faber check` green on touched files; launch claim none → no launch-count check. The oracle compares each wrapper's output/state contract before/after, not literal source bytes |
| `non_goals` | standing set + no change to the carrier-twin bag routes (`dense_block` / `dense_block_cached`), no attention change, no `model/dense.fab` edit |
| `risk` | low — pure extraction of a verified same-arithmetic region; proba coverage exists on both callers |
| `integrable` | yes |

---

## KRS-4 — `transformer.fab` QKV always-add region `dense_qkv`; wrapper supplies zeros

| field | value |
| --- | --- |
| `id` | KRS-4 |
| outcome | The identical typed QKV prologues of both static twins (`dense_block_static` 632–647; `dense_block_cached_static` 668–683) become one private `@ kernel` region computing `q = (ln1 · wq).added_bias(bq)` (likewise k, v) with the bias **always added**; the wrappers drop their `if has_bq/bk/bv` branches and supply the real bias or a zero `[Q]`/`[K]` tensor (tree rule 6) |
| `class` | named-private-kernel (two callers: both static twins) |
| `region` (stable identifier) | **`dense_qkv`** — private, same file, exact signature: `fn dense_qkv<T, D, Q, K>(tensor<f32, [T, D]> ln1, tensor<f32, [D, Q]> wq, tensor<f32, [Q]> bq, tensor<f32, [D, K]> wk, tensor<f32, [K]> bk, tensor<f32, [D, K]> wv, tensor<f32, [K]> bv) → tuple<tensor<f32, [T, Q]>, tensor<f32, [T, K]>, tensor<f32, [T, K]>>` — three `·` + `.added_bias` statements, no branches |
| `leaves_reused` | `·` matmul glyph + `.added_bias` method twin at typed rank (per-channel `[Q]`/`[K]` bias broadcast, matching `TypedDenseLayer.bq/bk/bv` field shapes) |
| `wrapper_vs_region` | wrappers `dense_block_static` / `dense_block_cached_static`; region `dense_qkv` (new, private, same file) |
| `hole` | none in the region; bias-presence policy moves to the wrapper. **Wrapper invariant (explicit, binding):** `has_bq` true → wrapper passes the real `layer.bq`; `has_bq` false → wrapper passes a **proven zero** `tensor<f32, [Q]>` (likewise k, v). The kernel always adds; the branch/policy stays outside the `@ kernel` body. External callers may construct `TypedDenseLayer` directly — the zero-on-absent contract is the wrapper's obligation, not the loader's |
| `second caller?` | yes — the two static twins |
| `launch claim` | none |
| `write_scope` | `gradus/src/transformer.fab`, `gradus/src/transformer.proba` |
| `done_when` | Both twins call `dense_qkv`; no `if has_*` inside any `@ kernel` body; absent-bias and present-bias rows produce byte-identical output vs pre-change (see oracle); a nonzero bias present when `has_*` is true is exercised, and the absent-bias twin is proven to receive zeros |
| `depends_on` | KRS-3 (same file — serialize; avoids dual authority on `transformer.fab`) |
| `sanity` | `faber check` on `src/transformer.fab` green |
| `oracle` | **Synthetic typed-layer fixtures in `src/transformer.proba`** (the card's own write scope): the existing consumer rows are absent-bias only — every `model/dense.proba` `_repertor` run is `false, false` and `_typed_ref01` builds `TypedDenseLayer` from those loaded fields, so no frozen static test provides a present-bias case (census §5; the Qwen receipt's bias note is about the carrier route, which does not consume real Q/K/V biases on the U1.8 surface). Proof: two focused proba twins constructing `TypedDenseLayer` records directly — (a) `has_bq/bk/bv = true` with nonzero biases, (b) `= false` — each calling `dense_block_static` (and the cached twin for the output+state contract) before and after the change; bytes recorded; case (b) output must equal a pre-change absent-bias run, and case (a) must equal the same tensors computed through the old branched prologue. The `model/dense.proba` REF-01 absent-bias rows stay byte-identical as the consumer proof |
| `non_goals` | standing set + no change to `TypedDenseLayer` field layout (`has_*` flags stay — the wrapper reads them), no attention change, no `model/dense.fab`/`model/dense.proba` edit |
| `risk` | medium — two named hazards, both convert-or-record: (1) zero-fill construction at typed rank (`[Q]`/`[K]` zeros): if a typed zeros constructor is missing, record in code and keep the `.added_bias` rank-extension form, do not invent a fill kernel; (2) **no live `@ kernel` returns a tuple today** (plain functions do — `train_step_bert_linear`, the gradient companions — but the kernel form is unproven): default is the tuple signature above; if `faber check` rejects a tuple-returning `@ kernel`, record it on this card, keep the wrappers' inline prologue with bias policy on the wrapper, and report to mind for a signature ruling — do not silently split into three kernels |
| `integrable` | yes |

---

## KRS-5 — `transformer.fab` `bert_tiny_block_2x8` marked `@ kernel` (+ canonical transpose spelling)

| field | value |
| --- | --- |
| `id` | KRS-5 |
| outcome | `bert_tiny_block_2x8` (:68) — pure glyph/method body, no `⇥` — gains `@ kernel` under the glyph-leaf law (tree rule 1 via pattern rule 1), keeping its `@ public` (dual annotation, as `nn.linear` carries); **and** the body's rank-2 transpose at :81 takes the canonical postfix `ᵀ` spelling (`kt ← kb.transpose()` → `kt ← kbᵀ`) per the settled tensor-glyph-transpose device rule — same function, same unit, no second call site touched |
| `class` | reuse-leaves (annotation + spelling; body is already `.layer_norm`/`·`/`.added_bias`/transpose/`.softmax()`/`.gelu()`/`+`) |
| `leaves_reused` | its own body (no in-body calls to non-kernel functions — verified) |
| `wrapper_vs_region` | no split needed — the function is already region-only |
| `hole` | none |
| `second caller?` | no — **no live caller exists** (verified: no `src/` proba and no `exempla/` package calls it; the PML0-U3 ledger row 15 admission was historical, and the "exempla probes" note in the earlier card draft was wrong). The focused proof below is therefore the function's first pinned caller |
| `launch claim` | none |
| `write_scope` | `gradus/src/transformer.fab`, `gradus/src/transformer.proba` |
| `done_when` | `@ kernel` present (with `@ public` kept); `kbᵀ` spelling in place or an explicit recorded exception on this card; the focused proba test below invokes `bert_tiny_block_2x8` and is byte-identical before/after; `faber check` green |
| `depends_on` | KRS-4 (same file — serialize) |
| `sanity` | `faber check` on `src/transformer.fab` green |
| `oracle` | **A focused `transformer.proba` test that actually invokes `bert_tiny_block_2x8`** — the existing transformer.proba rows exercise the carrier `dense_block` (:365, :378, :422), not this function, so a green dense_block row proves nothing here. Proof: add one focused test constructing the 21 admitted input tensors (accepted fragment shapes), call `bert_tiny_block_2x8` before the change to record the output bytes, and require byte-identical output after annotation + spelling change. The transpose spelling change is inside the same proof: identical output bytes are the acceptance |
| `non_goals` | standing set + no decomposition of the inlined legacy block (admitted shape by PML0-U3 ledger row 15), no SEM005 renames, no callers minted beyond the focused proba test |
| `risk` | low |
| `integrable` | yes |

**KRS-5 receipt (2026-08-28, lane `factory/krs-5`).** `bert_tiny_block_2x8` now carries `@ kernel` above its kept `@ public` (glyph-leaf law, tree rule 1; annotation order `@ kernel` first, matching `nn.linear`); the rank-2 transpose at :81 is the canonical postfix spelling `kt ← kbᵀ` (settled `tensor-glyph-transpose` rule; no other call site touched). A focused `transformer.proba` describe block now invokes the function — its first pinned caller — with the accepted fragment's 20 typed-tensor inputs (the card's "21" is the fragment ledger's 21 tensor params incl. `target`, which the function does not take; the signature takes the other 20) and pins the 16 output bytes exact (`≡`, not tolerance).

Two boundaries recorded, neither fixed here, matching the KRS-2 receipt:

1. **Post-change runtime run is runner-blocked at tip.** The FMIR runner refuses `@ kernel` execution (radix `65f2d7d6b` "refuse device kernel execution", post-dates the kernel twins): `faber run` and `faber test` on the annotated function fail with `runner refuses execution of @ kernel function` — the same known boundary as the pre-existing nn.proba `nn.linear` rows. The committed proba row therefore refuses at runtime under `faber test` after this commit (a documented kernel-refusal row, not a value failure); the card's before/after run comparison is not executable at this tip and is not claimed. Byte-identity acceptance instead rests on three facts: (a) the pins are the function's real pre-change bytes, recorded by running the un-annotated function before the change; (b) normalized `faber mir` text dumps of `src/transformer.fab` before vs after differ by **zero** (only `sym#` numbering shifts; every operation/type/def reference identical) — `kb.transpose()` and `kbᵀ` lower to the same operation, and the annotation is body-inert; (c) the annotation is marker-only by construction (the runner's refusal itself proves it lowers to the compute shader stage).
2. **`faber check src/transformer.proba` pre-existing red recorded.** The file carries 6 SEM010 rows at HEAD in the `tene_i32`/`config_p` helpers (the documented `test_util.or_default` closure wall); the error set is byte-identical before/after this commit. `faber check src/transformer.fab` is green on both sides (pre-existing WARN003 unused-function rows only; the static twins remain uncalled by the proba surface). No launch claim (no export seam); no caller minted beyond the focused proba test; no `⇥`-function annotation; no `do kernel`.

---

## KRS-6 (DEFERRED, BLOCKED) — `attention.fab` multi-head static parent

| field | value |
| --- | --- |
| `id` | KRS-6 |
| outcome | A multi-head parent with **static `H`, no `list.append`** composes per-head `scaled_dot_product_static` over packed typed tensors for the `multi_head_attention` family (uncached + cached variants). **Current state (corrected per census §0a):** the wrappers are **carrier per-head loops with no typed static-leaf invocation** — `scaled_dot_product_static` (attention.fab:79, `@ kernel`) is declared but has **no source call site**; `multi_head_attention` (:832) computes per-head cores via `_attention_core` (:585) and `multi_head_attention_cached` (:1055) via `_attention_core_offset` (:902), both over `list<NumericBlock>` with `_head` splits, `_rope`, `heads.append`, `_reconcile`, `_attention_matmul`. There is no per-head typed-kernel launch today to keep, lose, or count; any receipt wording must match that call graph |
| `class` | hole (tree rule 4 — the illegal nested call is the `list.append` head loop + `_head` carrier splits) |
| `leaves_reused` | `attention.scaled_dot_product_static<B, D>` (per-head core, already `@ kernel`; today uncalled — this card is what would link it) |
| `wrapper_vs_region` | wrappers `multi_head_attention` / `multi_head_attention_cached` keep `⇥`, `_validate_multi`/`_validate_cached_multi`, `_rope_table`, GQA policy, cache write; region = **`multi_head_attention_static`** — explicit **placeholder contract**, exact signature withheld until the column-slice admission settles (needs static `H`, packed `[T, H·D]` inputs, per-head column splits, and the `heads.append`/`_reconcile` concatenation replaced by typed ops). The card is **blocked** on that admission; the placeholder name is reserved so later units cannot mint a duplicate region identifier |
| `hole` | `list.append` head loop; `_head` column splits; `_write_cache` mutation (cached variant) — each stays on the wrapper or becomes an argument |
| `second caller?` | yes (cached + uncached) once shaped; named private/`@ kernel` parent per rule 2 |
| `launch claim` | **none today.** This is the only family that could ever touch per-head launch count (the 1,440-encoder family); any encoder-movement claim requires the export seam named in write_scope (radix program-plan export family, e.g. the GEA wire-plan export) — an operator amendment, not this card — and a before/after exported launch count for the attention family. Do not report "attention is a kernel" for 3b alone |
| `write_scope` (when dispatched) | `gradus/src/attention.fab`, `gradus/src/attention.proba` |
| `done_when` (when dispatched) | Static-`H` parent replaces the head loop; no `list.append` inside the region; cached variant keeps cache mutation on the wrapper; proba rows byte-identical |
| `depends_on` | KRS-3 green (need order 5: after mlp) **and** an admitted typed column-slice form (open question 1 — `_head` has no glyph twin; `for from grid at [i, j]` noted pending in source) **and** operator amendment if any launch claim is wanted. **Blocked** on the slice admission — not dispatchable until it exists |
| `sanity` | n/a until dispatched |
| `oracle` (when dispatched) | focused proba tuples byte-identical for the GQA + RoPE rows (consecutive and interleaved policies) — rows that invoke the wrappers (the existing attention proba surface); `faber check` green on touched files; if (and only if) an export seam was added: exported launch count for the attention family before/after |
| `non_goals` | standing set + no per-head launch-count claim without the export seam, no change to the carrier routes' public contracts, no new RoPE math (table stays host-side) |
| `risk` | high — needs a slicing admission that does not exist yet; deferred, not estimated |
| `integrable` | n/a until dispatched |

---

## Closure-class register (deferred per mind routing)

Census §9 (reissued under REVISE `1ddc4077` against the one-row ledger, `gradient.fab` rows included): **zero live closure-class sites.** Every starter one-off dissolved under live verification into direct leaf calls (KRS-2) or second-caller regions (KRS-3/KRS-4). The admitted `gradient.fab` `simple_loss`/`masked_mean` rows are `@ radix backward` companions — a different lowering family, not closure candidates. Register stays open: a conversion hand on KRS-2..KRS-6 that finds a genuine one-off region notes it here with the two function names and defers; a later separate hand session implements it after `ef103950` is implemented and green (tree rule 3 until then: named private `@ kernel`).

| site | wrapper + closure | status |
| --- | --- | --- |
| — | — | none found (2026-08-28 census; re-issued 2026-08-28 REVISE reissue) |

## Order (need `3b9e5796` §Order, restated)

1. ~~Census~~ — KRS-1 done (reissued under REVISE `1ddc4077`).
2. Reuse-leaves units — KRS-2 (no compiler dependency; six adapters), KRS-5.
3. Named `dense_mlp` + QKV-always-add `dense_qkv` — KRS-3, KRS-4 (do not wait on `ef103950`).
4. Kernel-closure one-offs — none live; register above.
5. Attention hole / multi-head parent — KRS-6, after mlp, **blocked on the slice admission**; only row that can touch per-head launch count, and only with an export seam.
6. Promote `kernel-region-split` tentative → settled after the first green conversion unit — campaign milestone in `GOAL.md` ledger; skills-repo edit filed separately.
