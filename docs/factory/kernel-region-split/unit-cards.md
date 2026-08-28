# kernel-region-split unit cards

Delivery lowering for need `3b9e5796`, task `c78bb834`. Cards descend from [`census.md`](census.md) (KRS-1, landed). Standing law cited on every card: **`kernel-region-split`** — `~/work/ianzepp/skills/faber/canonical-faber/references/patterns.md` §kernel-region-split (tentative, operator 2026-08-28) + `SKILL.md` §14. Promotion to settled happens after the first green conversion unit (KRS-2..KRS-5 ledger in [`GOAL.md`](GOAL.md)); it is a campaign milestone, not a unit.

Operator routing (binding): cards run parallel with the `ef103950` closure landing; closure-class rows are carded-but-deferred — the census found **zero live closure-class sites**, so nothing dispatched below waits on `ef103950`. A conversion hand that finds a function better suited to closure syntax notes + defers it on the card; a later separate hand session implements deferred conversions after `ef103950` is green.

Standing `non_goals` on every card: no GEA3 `kernel.fab` rewrite unless the card names it; no 2,115/encoder-delta claim without an export seam; no `@ kernel` on a `⇥` function; no `do kernel`.

Lane gates named once (not on any card): lint owns `./scripta/check-source`; test owns broad suites; merge owns `./scripta/check-compile` closeout and atomic landing on `main`.

---

## KRS-1 — census (landed)

| field | value |
| --- | --- |
| outcome | Live-verified census of the seven named files + tensor-math siblings; starter rows corrected against source |
| write_scope | `gradus/docs/factory/kernel-region-split/**` |
| done_when | Census table complete, every function one row, corrections recorded (§0) |
| depends_on | — |
| status | **done** — planner, this commit |

---

## KRS-2 — `nn.fab` legacy fixed-shape adapters call typed leaves directly

| field | value |
| --- | --- |
| `id` | KRS-2 |
| outcome | `linear_2x2`, `linear_2x8`, `gelu_4x4`, `gelu_2x8`, `layernorm_2x8` compute via typed leaves/method twins instead of staging through `NumericBlock` carriers (`_staged` → `*_carrier` → pin detours) |
| `class` | reuse-leaves (tree rule 1 — no new kernel body) |
| `leaves_reused` | `nn.linear<M,K,N>`, `nn.gelu<M,N>`, `·` + `.added_bias` (S6-C2 per-channel contract), `.layer_norm(1, ε, s, o)` method twin |
| `wrapper_vs_region` | wrappers `linear_2x2`/`linear_2x8`/`gelu_4x4`/`gelu_2x8`/`layernorm_2x8`; region = the existing public typed leaves (no new function) |
| `hole` | none |
| `second caller?` | no — direct leaf calls, no region minted |
| `launch claim` | none (source-only; no export/plan change) |
| `write_scope` | `gradus/src/nn.fab`, `gradus/src/nn.proba` |
| `done_when` | All five adapters return identical bytes for the existing `nn.proba` fixed-shape rows; no `_staged`/`*_carrier` detour remains in those five bodies; `linear_2x8` keeps the per-channel `[8]` bias contract |
| `depends_on` | — (parallel-safe with KRS-3: disjoint files) |
| `sanity` | `faber check` on `src/nn.fab` green; focused `nn.proba` rows byte-identical |
| `oracle` | focused proba tuples byte-identical for the named cases (`linear_2x2`, `linear_2x8`, `gelu_4x4`, `gelu_2x8`, `layernorm_2x8` rows); `faber check` green on touched files; launch claim none → no launch-count check |
| `non_goals` | standing set + no change to `linear_4x4` (already delegates), no carrier-twin deletion (`linear_carrier`/`gelu_carrier`/`layernorm` keep their load-edge callers), no SEM014/SEM016 pin work |
| `risk` | low — arithmetic-identical rerouting through existing kernels |
| `integrable` | yes |

---

## KRS-3 — `transformer.fab` named private `@ kernel dense_mlp` shared by both static block twins

| field | value |
| --- | --- |
| `id` | KRS-3 |
| outcome | The byte-identical SwiGLU+residual tails of `dense_block_static` (657–663) and `dense_block_cached_static` (687–693) become one private `@ kernel dense_mlp<T, D, F>(residual, ln2, wg, wu, wd)`; both twins call it (the pattern's own worked example) |
| `class` | named-private-kernel (tree rule 2 — two callers share the region; `@ kernel`, not `@ public`) |
| `leaves_reused` | `nn.swiglu_hidden<T,F>`, `math.add<T,D>`, `·` |
| `wrapper_vs_region` | wrappers `dense_block_static` / `dense_block_cached_static`; region `dense_mlp` (new, private, same file) |
| `hole` | the bag attention call — `_multi_attention` / `_multi_attention_cached` stays on the wrappers (argument-shaped boundary: wrapper pins `ctx` and passes it to the region's residual input) |
| `second caller?` | yes — the two static twins (this is why named private, not closure) |
| `launch claim` | none (inlining inside parents that are not launched moves nothing in the GEA graph — need rule 7) |
| `write_scope` | `gradus/src/transformer.fab`, `gradus/src/transformer.proba` |
| `done_when` | Both static twins call `dense_mlp`; `dense_mlp` is `@ kernel` and private; tail arithmetic unchanged; dense-block proba rows and `model/dense.proba` REF-01 rows byte-identical |
| `depends_on` | — |
| `sanity` | `faber check` on `src/transformer.fab` green |
| `oracle` | focused proba tuples byte-identical (transformer dense-block rows; consumer rows in `src/model/dense.proba` REF-01 runners); `faber check` green on touched files; launch claim none → no launch-count check |
| `non_goals` | standing set + no change to the carrier-twin bag routes (`dense_block` / `dense_block_cached`), no attention change, no `model/dense.fab` edit |
| `risk` | low — pure extraction of a verified-identical region; proba coverage exists on both callers |
| `integrable` | yes |

---

## KRS-4 — `transformer.fab` QKV always-add region; wrapper supplies zeros

| field | value |
| --- | --- |
| `id` | KRS-4 |
| outcome | The identical typed QKV prologues of both static twins (633–648 / 669–684) become one private `@ kernel` region computing `q = ln1 · wq + bq` (likewise k, v) with the bias **always added**; the wrappers drop their `if has_bq/bk/bv` branches and supply the real bias or a zero `[Q]`/`[K]` tensor (tree rule 6) |
| `class` | named-private-kernel (two callers: both static twins) |
| `leaves_reused` | `·` matmul glyph + `math.add`-family add (bias add as `+`/`added_bias` method twin at typed rank) |
| `wrapper_vs_region` | wrappers `dense_block_static` / `dense_block_cached_static`; region the new private QKV kernel (same file) |
| `hole` | none in the region; bias-presence policy moves to the wrapper (zero fill is host policy) |
| `second caller?` | yes — the two static twins |
| `launch claim` | none |
| `write_scope` | `gradus/src/transformer.fab`, `gradus/src/transformer.proba` |
| `done_when` | Both twins share the region; no `if has_*` inside any `@ kernel` body; absent-bias rows (SmolLM2) and present-bias rows (Qwen2.5 attn bias path via `model/dense.fab` `_probe_bias`) produce byte-identical proba output |
| `depends_on` | KRS-3 (same file — serialize; avoids dual authority on `transformer.fab`) |
| `sanity` | `faber check` on `src/transformer.fab` green |
| `oracle` | focused proba tuples byte-identical for present-bias and absent-bias cases; `faber check` green on touched files; launch claim none → no launch-count check |
| `non_goals` | standing set + no change to `TypedDenseLayer` field layout (`has_*` flags stay — the wrapper reads them), no attention change |
| `risk` | medium — zero-fill construction must exist at typed rank (`[Q]` zeros); if a typed zeros constructor is missing, record in code and keep the `added_bias` rank-extension form (convert-or-record), do not invent a fill kernel |
| `integrable` | yes |

---

## KRS-5 — `transformer.fab` `bert_tiny_block_2x8` marked `@ kernel`

| field | value |
| --- | --- |
| `id` | KRS-5 |
| outcome | `bert_tiny_block_2x8` (67) — pure glyph/method body, no `⇥` — gains `@ kernel` under the glyph-leaf law (tree rule 1 via pattern rule 1) |
| `class` | reuse-leaves (annotation-only; body is already `.layer_norm`/`·`/`added_bias`/`transpose`/`softmax`/`gelu`/`+`) |
| `leaves_reused` | its own body (no in-body calls to non-kernel functions — verified) |
| `wrapper_vs_region` | no split needed — the function is already region-only |
| `hole` | none |
| `second caller?` | no (caller-backed admitted API: exempla probes) |
| `launch claim` | none |
| `write_scope` | `gradus/src/transformer.fab`, `gradus/src/transformer.proba` |
| `done_when` | `@ kernel` present; proba/caller output byte-identical; `faber check` green |
| `depends_on` | KRS-4 (same file — serialize) |
| `sanity` | `faber check` on `src/transformer.fab` green |
| `oracle` | focused proba tuples byte-identical; `faber check` green on touched files; launch claim none → no launch-count check |
| `non_goals` | standing set + no decomposition of the inlined legacy block (admitted shape by PML0-U3 ledger row 15), no SEM005 renames |
| `risk` | low |
| `integrable` | yes |

---

## KRS-6 (DEFERRED) — `attention.fab` multi-head static parent

| field | value |
| --- | --- |
| `id` | KRS-6 |
| outcome | A multi-head parent with **static `H`, no `list.append`** composes per-head `scaled_dot_product_static` over packed typed tensors for the `multi_head_attention` family (uncached + cached variants); until it lands, wrappers keep per-head launches and the receipt must say so |
| `class` | hole (tree rule 4 — the illegal nested call is the `list.append` head loop + `_head` carrier splits) |
| `leaves_reused` | `attention.scaled_dot_product_static<B, D>` (per-head core, already `@ kernel`) |
| `wrapper_vs_region` | wrappers `multi_head_attention` / `multi_head_attention_cached` keep `⇥`, `_validate_multi`/`_validate_cached_multi`, `_rope_table`, GQA policy, cache write; region = the future static multi-head parent |
| `hole` | `list.append` head loop; `_head` column splits; `_write_cache` mutation (cached variant) — each stays on the wrapper or becomes an argument |
| `second caller?` | yes (cached + uncached) once shaped; named private/`@ kernel` parent per rule 2 |
| `launch claim` | **none today.** This is the only family that could ever touch per-head launch count (the 1,440-encoder family); any encoder-movement claim requires the export seam named in write_scope (radix program-plan export family, e.g. the GEA wire-plan export) — an operator amendment, not this card. Do not report "attention is a kernel" for 3b alone |
| `write_scope` (when dispatched) | `gradus/src/attention.fab`, `gradus/src/attention.proba` |
| `done_when` (when dispatched) | Static-`H` parent replaces the head loop; no `list.append` inside the region; cached variant keeps cache mutation on the wrapper; proba rows byte-identical |
| `depends_on` | KRS-3 green (need order 5: after mlp) **and** an admitted typed column-slice form (open question 1 — `_head` has no glyph twin; `for from grid at [i, j]` noted pending in source) **and** operator amendment if any launch claim is wanted |
| `sanity` | n/a until dispatched |
| `oracle` (when dispatched) | focused proba tuples byte-identical for the GQA + RoPE rows (consecutive and interleaved policies); `faber check` green on touched files; if (and only if) an export seam was added: exported launch count for the attention family before/after |
| `non_goals` | standing set + no per-head launch-count claim without the export seam, no change to the carrier routes' public contracts, no new RoPE math (table stays host-side) |
| `risk` | high — needs a slicing admission that does not exist yet; deferred, not estimated |
| `integrable` | n/a until dispatched |

---

## Closure-class register (deferred per mind routing)

Census §9: **zero live closure-class sites.** Every starter one-off dissolved under live verification into direct leaf calls (KRS-2) or second-caller regions (KRS-3/KRS-4). Register stays open: a conversion hand on KRS-2..KRS-6 that finds a genuine one-off region notes it here with the two function names and defers; a later separate hand session implements it after `ef103950` is implemented and green (tree rule 3 until then: named private `@ kernel`).

| site | wrapper + closure | status |
| --- | --- | --- |
| — | — | none found (2026-08-28 census) |

## Order (need `3b9e5796` §Order, restated)

1. ~~Census~~ — KRS-1 done.
2. Reuse-leaves units — KRS-2 (no compiler dependency), KRS-5.
3. Named `dense_mlp` + QKV-always-add — KRS-3, KRS-4 (do not wait on `ef103950`).
4. Kernel-closure one-offs — none live; register above.
5. Attention hole / multi-head parent — KRS-6, after mlp; only row that can touch per-head launch count, and only with an export seam.
6. Promote `kernel-region-split` tentative → settled after the first green conversion unit — campaign milestone in `GOAL.md` ledger; skills-repo edit filed separately.
