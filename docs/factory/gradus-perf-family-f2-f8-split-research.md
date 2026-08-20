# gradus perf family F2–F8 — kernel-tier vs source-tier SPLIT (research note)

> **STATUS: RESEARCH-ONLY.** This note is a decision memo for the operator, not a
> goal, not a delivery, not a campaign unit. It mints no goal, edits no `src/`,
> and admits nothing into the campaign inventory. It records the split for one
> research Hand unit (task `97e59456`, audit `aca16ca1`). Line numbers were
> re-located after the robustness fold `cdbeb65`; every citation below is live
> against this tree at the cited line.

## Frame

The F2–F8 family is eight decode-path inefficiencies in the gradus source that a
review flagged. The unit's job is to decide, per member, which tier owns the
durable fix: **kernel-tier (EXEC-02 / Radix)**, **source-tier (pure Faber source,
behavior-preserving, benched from existing exempla)**, or **wiring-prerequisite
(U6)**. The guiding rule applied below: a member is *source-tier* only if the
dominant cost is durably removable in pure Faber source without a new or improved
device kernel; otherwise it belongs to EXEC-02. Benching reality: the dense
decode path is wired only for the SmolLM2 oracle (`generation.fab:801-812`), and
prefill does not fill the KV cache, so **end-to-end decode-path benching is
blocked on U6** for every member whose win is measured over a full decode loop.
Where that is true it is stated plainly in the member row.

## Split table

Key to tier: **K** = kernel-tier (EXEC-02 owns; a source fix would be wasted /
duplicated / blocked on a kernel seam). **S** = source-tier. **U6** =
wiring-prerequisite (not a perf fix; the bench enabler).

| # | Member (re-located cite) | Tier | Current complexity | Fix shape | Expected win (reasoning) | Risk | Kernel-seam deps / notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | KV-cache append full-copy O(T²) decode (`cache.fab:350-380` `append`; `385-417` `extend`; driving path `attention.fab:954-960` `_write_cache` → `kv.extend`; per-prompt-token cached decode `generation.fab:813-820`) | **K** | every decode step rebuilds the whole `[T,D]` K and V tensors (append copies all prior rows + the new row), O(T·D) per step → O(T²·D) over a decode; prefill is forced down the same one-token-at-a-time cached path (`generation.fab:813-820`), so prompt prefill is itself O(T²) | EXEC-02 KV memory/layout seam: allocate the KV buffer once with reserve and write only the new row in place (the KvCacheLayout reserve-policy precedent, `exec02-packed-kernels-delivery.md:74`); the staged value-carrier keeps `append`/`extend` as the contract, Gradus owns layout authority (`exec02…:72`) | O(T²·D) → O(T·D): the decode-path killer is eliminated, prefill cache-fill becomes O(T) | low shape risk (contract unchanged); **end-to-end bench blocked on U6** — win cannot be measured until U6 wires batched prefill→cache | needs a Radix KV-write / reserved-buffer seam; a pure-source rewrite (e.g. chunked tensor) fights the immutable staged-tensor model and would be **wasted work** → K |
| 2 | per-forward [D,V] transpose of the tied lm_head (`dense.fab:418-427`, `w_head ← _transpose(embed_v)`; `_transpose` `dense.fab:163-180`; the ~47M-element copy is the [D,V] materialization for a dense config ≈ D×V, e.g. 1.5k×32k) | **K** | every `forward`/`decode_step` materializes a true row-major [D,V] from the token-major embed view, then the output linear multiplies it | kernel: fused GEMM-with-transposed-operand (the `TiledMatMul`/`Transpose` family EXEC-02 already owns, `exec02…:87-89`) so the token-major [V,D] table is consumed as the transposed operand without materializing [D,V]; a *source* band-aid (memoize/hoist the transpose per source handle) is possible but only cuts a constant factor | removes the ~47M-element copy per forward (and per decode step); prefill/[T,V] projection is the dominant site on the dense row | low; the avoided-transpose convention is already documented (`attention.fab:800-807`); **end-to-end decode bench blocked on U6**, per-forward (prefill) benchable now via `exempla/dense-model`, `dense-prefill-*` | a source hoist would diverge from kernel semantics → prefer K; source hoist only as a temporary staged-path aid |
| 3 | synthesized zero-bias + full add per weight (`dense.fab:213-227` `_no_bias` fills `[T,N]` with 0.0; `233-263` `_channel_to_rows` tiles `[N]→[T,N]`; applied per block weight `dense.fab:402-408`, bq/bk/bv via `_attn_bias` `271-284`) | **S** (+ K rider) | every linear materializes a same-shape `[T,N]` bias (zeros when absent) because the composed `nn.linear` requires `[T,N]` and rejects broadcast (`_no_bias:210-215`); the bias tensor is then element-wise added | source: expose a no-bias / per-channel-vector-bias path on the nn linear surface so absent and vector biases skip the `[T,N]` synthesis and the full add; behavior-preserving, first-index/arithmetic unchanged | eliminates the `[T,N]` fill + add per weight per forward (7 linears/block on the dense row) — a real constant-factor + allocation win in the staged path, **benched from `exempla/dense-*` without U6** | low-moderate: changes the public nn surface (its own proba must be updated); the *deeper* win (fold bias into the GEMM epilogue) is a K rider, not a prerequisite | needs no new kernel to land the source slice; the add-elimination for real biases beyond this is a later EXEC-02 epilogue fusion |
| 4 | RoPE per-coordinate pow/sin/cos recompute (`attention.fab:493-549` `_rope`; trig recomputed `511-512`,`533-534` via 12-iteration Taylor `_sin`/`_cos` `369-395`; recomputed once per head-application — `multi_head_attention` `822-828`, cached `1033-1048` — so each position's table is rebuilt H× per forward) | **S** | cos/sin and the `freq_base.power` term are recomputed per (row, coordinate), and again per (head, layer); O(H·L·T·dim) trigonometric/elementary evaluations per forward | source: hoist a per-(positions × dim)-reduced RoPE table (angle + cos + sin) once per forward and index it in `_rope`'s inner loop; behavior-preserving, arguably more accurate (fewer Taylor evals) | removes the H·L× redundant trig recompute per forward (decode T=1 still recomputes the same position±coordinate H·L times); **benched from `exempla/dense-rope` without U6** | low; deterministic Taylor output must stay within the existing numeric pin (proba) | no kernel dependency to land the hoist; the GPU *device* path routes through the EXEC-02 `Rope` kernel (`exec02…:88`, `plan.rs`) — the hoist only improves the staged reference; it is NOT duplicated kernel work because the kernel already owns the device path |
| 5 | [T,T] scale materialization (`attention.fab:612-613` `_fill([t,t],scale)` + `math.mul(scores, scale_t)`; cached variant `918-919`) | **K** | a full `[T,T]` (or `[Tq,Tk]`) tensor filled with `scale` is materialized then element-multiplied into the scores | kernel: fold the scalar scale into the scaled-GEMM / attention epilogue (no `[T,T]` fill, no separate elementwise pass); a *source* fallback (`math.scaled_matmul` scalar-scale primitive) would remove the materialization but likely duplicates the kernel intent | for prefill the materialized `[T,T]` is large (removal ~÷2 on the score pass's allocation+traffic); for decode `[1,T]` it is small — the win is prefill-dominated | low; **prefill-side benchable now via `exempla/dense-prefill-*`, decode-side blocked on U6** | needs a scaled-GEMM/attention kernel seam; a source scaled-matmul is an acceptable interim but flagged as potential duplicate work → prefer K |
| 6 | per-head copy + coordinate concat (`attention.fab:638-651` `_head` copies each head's columns into a fresh `[T,d]`; `654-666` `_reconcile` concatenates heads; composition `multi_head_attention` `818-831`, cached `1024-1052` — per-head copy of q/k/v + concat of heads, repeated per head) | **K** | packed `[T,H·D]` ↔ per-head `[T,d]` is done by explicit column-copy per head on input and `math.concatenate` on output — O(H·T·D) reshuffle copies each multi-head call | kernel: run the multi-head GEMM / attention on the packed layout with strided per-head addressing (no per-head copy, no concat); source slices exist (`math.slice` `math.fab:685`) but still copy → not the durable fix | removes the O(H·T·D) reshuffle per multi-head call (both prefill and every decode step); **prefill-side benchable now via `exempla/dense-gqa`, decode-side on U6** | low; the packed `[T,H·D]` layout convention is already the documented posture (`dense.fab:363-368`) | needs a strided multi-head view / fused kernel; a source-only reshape keeps the copy, so the durable removal is K |
| 7 | sampling O(V·history) + top-k/top-p scans (`sampling.fab:354-373` `_repetition_penalty` is O(V·history); `_top_k` `386-408` is O(k·V) with repeated full-list `_max_index_pair` `288-302` scans + `_binary` `325-336` list rebuilds; `_top_p` `453-476` is O(V) per kept element, worst O(V²)) | **S** | pure host-side list pipeline; each filter re-scans the whole vocabulary and rebuilds full lists per selected element | source: replace the incremental mask scans/rebuilds with a single selection/sort of the (value,index) pairs (partial selection for top-k, descending scan for top-p) while preserving the pinned first-index tie-break; behavior-preserving | sampling step from O(V·history + k·V·(+rebuilds)) and worst O(V²) to O(V·history + V log V)-ish; dominant on small/mid vocab and large history | low; the arithmetic/order are oracle-pinned (`sampling.fab:20-45`) and proba-pinned — the rewrite must keep exact tie/order semantics | **EXEC-02 decision 8 puts sampling/top-k host-side, not kernel scope** (`exec02…:77`), so this is unambiguously source-tier; fully benched from `sampling.proba` / `exempla/token-generation`, **no U6 dependency** |
| 8 | decode+cache composition UNWIRED (`decode.fab:647-655`,`660-683` `replay` does not include the model decode — "U6 wires decode_data in"; `prefill` `521-548` produces logits but does NOT fill any KV cache; the only wired loop is the dense oracle `generation.fab:801-812`, which fills the cache one prompt token at a time through the cached path, `813-820`) | **U6** | no batched prefill→cache→incremental-decode composition exists; `replay` is standalone over a precomputed logit stream; the Qwen/dense-looped path is not the shared composition | source: add `prefill_cached` (batched `extend` of every layer's KV) and wire it + `decode_cached` + `replay`/sampling into one generation composition; **not a perf fix — it is the bench prerequisite** | enables end-to-end benching of members 1,2,5,6 (and the decode-side of 2,5,6); by itself it adds no throughput — but without it no decode-path win is measurable | moderate: it re-wires the public generation surface and touches cache lifecycle, so it carries correctness/API risk and should land with its own proba | depends only on the existing source primitives; must land before members 1/5/6 (decode-side) can be validated end-to-end |

## Summary of the split

- **Kernel-tier (EXEC-02 owns; do not duplicate in source):** members **1, 2, 5, 6**
  — their dominant cost is memory movement / materialization that only a kernel or
  memory seam removes; a source rewrite is wasted or diverging work.
- **Source-tier (pure Faber, behavior-preserving, benchable without U6):**
  members **7** (sampling — host-side by `exec02…:77`), **4** (RoPE table hoist),
  and the **source slice of member 3** (no-bias / vector-bias nn surface).
- **Wiring-prerequisite (U6):** member **8** — a composition change, not a perf fix;
  the gate for benching members 1 and the decode-side of 2/5/6.

## Single recommendation to the operator

**Sequence: land U6 (member 8) first — it is the smallest, safest source change
and it unblocks all decode-path benching — and simultaneously fund the three
genuinely source-tier fixes (members 7, 4, and the member-3 bias API seam), which
are behavior-preserving, independently benchable without U6, and need no new
kernel; route members 1, 2, 5, 6 to the EXEC-02 kernel tier and explicitly do not
fund source rewrites of them, because those rewrites would be wasted/duplicated
work once the kernel/memory seams land.**

This memo mints no goal and admits nothing into the campaign.
