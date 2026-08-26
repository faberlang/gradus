# GOAL: dense-typed-assembly — pin weights at load; typed host graph

**Status**: planned — drafted-not-lowered; pre-implementation
**Created**: 2026-08-26
**Campaign:** `—` (standalone; complementary to `kernel-purity-census`, not a purity wave)
**Source:** operator session 2026-08-26 — contrast of `src/model/dense.fab` vs `src/kernel.fab`; Wave 0 carrier/admissions ruling
**Repos:** primary: `gradus/`
**Related:** [`../kernel-purity-census/CAMPAIGN.md`](../kernel-purity-census/CAMPAIGN.md) (Wave 0 ruling; dense family carved out as “resident-weight program route, not purity edits”); [`../kernel-purity-census/wave-0-carrier-admissions-ruling.md`](../kernel-purity-census/wave-0-carrier-admissions-ruling.md); [`../production-ml-library/pml5-ref01-dense-reference-delivery.md`](../production-ml-library/pml5-ref01-dense-reference-delivery.md); `src/model/dense.fab`; `src/kernel.fab`; `src/tensor.fab` materialization contract; `src/transformer.fab` `dense_block`

## Coordination (fleet 2026-08-26)

Lowering shares write surfaces with work that is already in flight. Do not
fork designs or stomp those seats:

| Seat | Fact | Consequence here |
| --- | --- | --- |
| Kernel-purity census | Wave 2 is the next prefill-chain wave; it shares `src/` files with this goal | Do not treat census W2 files as free; path-limit and wait or work around live dirt |
| Anti-canonical cleanup | Another session is actively respelling the same host files | Skip already-dirty `src/` / docs; do not “fix” foreign respells |
| Device fragments v2 | Visibility rules landed at radix `dd2b52857`: `@ public` entries vs private `@ kernel` / `@ nucleum` helpers | New algebra leaves are **private `@ kernel`** unless they are the public production twin. Assemblers stay ordinary and unannotated. Do not mark a helper `@ public` just to export a glyph |
| MODEL-03 | Dense-family overlap on the qwen35moe / hybrid state side lands **before** this goal in any sensible order | Do not rewrite MODEL-03 carriers or steal its dense-family names; this goal owns REF-01 host assembly only |

---

## Invariant

`NumericBlock` is an admission envelope, not the dense host graph. After
load, every weight is a pinned `tensor<f32, […]>` (size parameters from the
admitted model). The forward / prefill / decode routes are glyph composition
on those types — the same posture as `src/kernel.fab`, at host/logical
shapes rather than frozen GEA geometry.

Inner algebra is extracted as named functions. A leaf that is pure
tensor-in / tensor-out (no resolver, no throw, no cache or I/O mutation)
carries `@ kernel`. Effectful work stays in ordinary functions. That split
is the fusion surface: the compiler later fuses kernel leaves; it does not
have to see load, diagnostics, or generation control inside a device body.

## Problem

`src/kernel.fab` is a typed contract: shapes live in the signature
(`tf32[8,960]`, `tf32[1,960]`, `tf32[36,960]`), bodies are glyphs (`·`,
`⊙`, `.rms_norm`, `.transpose()`), and host admission stays outside the
device entry. `src/model/dense.fab` is the opposite: a resolver returns
`NumericBlock`, every helper takes a bag, `forward` / `decode_step` /
`decode_block` / `prefill_cached` return a bag, and the same layer-resolution
walk is pasted four times.

That is a category error against live law:

| Authority | What it says | What dense does |
| --- | --- | --- |
| `src/tensor.fab` (materialization, ~L61–67) | A validated `NumericBlock` is turned into a typed compiler tensor by the consumer, which pins the static shape (`t.data ↦ tensor<f32, [2,2]>`) | Never pins. The bag is the graph. |
| Wave 0 ruling 2026-08-26 | Envelope, not a math object. Weights exit **at load**. A carrier never crosses a kernel boundary. Activations are the only remaining staged tenant, and only until shape-generic admission lands. | Weights stay bags through every layer and the lm_head. |
| `src/math.fab` | Production split already exists: `@ kernel add<size M, size N>(tensor<f32, [M, N]>…)` vs leftover `add_carrier` | Dense calls `nn.linear_carrier` / `nn.rmsnorm` / `transformer.dense_block` — all bags. |
| `src/nn.fab` | Typed `linear<size M, K, N>` already landed (~L351) | Dense does not use it. `rmsnorm` (~L508) is still a bag. |

Observable slop in `dense.fab` is the tax of staying on the envelope:
`_shape` + `_shape_text`, handwritten `_transpose` / `_collect` stride
loops (`coalesce` + `i * cols + j`), `_attn_bias` `do`/`catch` probes,
`_rmsnorm` / `_linear` / `_block` catch-and-reconstruct wrappers, and
`_map_cached` string→variant remap. Canonical-Faber already names the
wrapper family and the coalesce-fed container walk as non-canonical.

The kernel-purity campaign explicitly does **not** own this file
(`CAMPAIGN.md` non-items: “needs the resident-weight program route, not
purity edits”). Leaving it unowned keeps the REF-01 host assembly on the
carrier after Wave 0 said weights exit at load.

## Proposal

Split the dense surface on the Wave 0 seam. Do not pretty-print the bag
graph in place.

### 1. Admission (bags live here only)

`source(name, layer) → NumericBlock` stays the load-edge resolver. One
`load` (or `admit`) function pins each canonical tensor against
`DenseConfig` and converts:

```fab
const tensor<f32, [D, V]> embed ← block.data ↦ tensor<f32, [D, V]>
```

`MissingTensor` / `BadShape` / `BadConfig` fire here, once. After `load`
returns, dense source does not name `NumericBlock`.

### 2. Typed model, not config-plus-resolver in the graph

`DenseConfig` ints become size parameters at the admitted model (`D`, `V`,
`F`, `Q = H·d`, `K = KV·d`). Weights become a `DenseModel` of static
tensors (embed, per-layer projections and norms, optional Q/K/V bias, tied
or untied head). The stringly `model.layers.§` walk happens in `load`, not
inside `forward`.

### 3. Typed block, then a kernel-shaped assembler

`transformer.dense_block` and `dense_block_cached` stay bag-in, bag-out
today (`src/transformer.fab` ~L408 / ~L475). The graph cannot become clean
while it calls those. Land typed twins (`dense_block<size T, D, …>`) that
compose typed `nn.linear` and a typed `rmsnorm` (land the rmsnorm twin in
this goal if purity Wave 1 has not). `dense.fab` remains an assembler: it
does not inline the block glyphs and fork from `transformer.fab`.

Host routes then look like `kernel.fab`: gather, RMSNorm, `·`, residual
`+`, `.transpose()` for a tied head. Handwritten `tok * D + d` and
software `_transpose` go away. Cache overflow / gap stay a pre-graph
admit; the cached step is the typed cached twin.

### 3b. Extract leaves; `@ kernel` when the body is pure

Operator ruling 2026-08-26 (this session): as the bag graph is replaced,
any inner logic that is realistically its own function **is** extracted.
If that function is feasible as a kernel, it is tagged `@ kernel`. The
point is a hard split between pure ops and external effects so later
compiler fusion sees small, closed leaves.

**Feasible `@ kernel` (do this):**

- Typed tensor-in / tensor-out or `mut` output view.
- Body is glyphs or admitted method twins (`·`, `⊙`, `+`, `.rms_norm`,
  `.transpose()`, `.silu()`, `.softmax()`), matching `src/kernel.fab` and
  `math.add<size M, size N>`.
- No `⇥`, no `throw`, no resolver, no path/container, no cache mutation,
  no generation control.
- No loop, slice, failable construct, or in-body call inside the kernel
  body (GEA leaf law; `docs/module-map.md` kernel inventory).
- Shape-generic when a second geometry exists
  (`docs/shape-generic-kernels.md`): `@ kernel fn rmsnorm<size T, size D>(…)`,
  not a frozen `960` copy of the device file.
- Visibility (fragments-v2 / radix `dd2b52857`): `@ public` only on the
  production twin a caller launches or imports as an entry. Extracted
  helpers stay **private `@ kernel`**. Assemblers stay unannotated.

Examples that should come out as kernels rather than stay inlined walks:
RMSNorm, projection GEMM/GEMV (reuse typed `nn.linear` if it can take the
annotation), residual add, SwiGLU, score `·` + scale, causal/masked
softmax once the method twin owns the recipe, gather / tied-head `ᵀ` once
typed.

**Not `@ kernel` (extract as ordinary functions, or do not extract):**

- `load` / resolver / `BadShape` / `MissingTensor`.
- Cache admit (`Overflow`, `Gap`, `_shared_prefix`).
- Generation / sampling / BPE / parsers (`while true`, cursors, heaps).
- Assemblers that *call* leaves: `dense_block`, `forward`, `decode_step`.
  A kernel body must not make an in-body call, so composition stays
  ordinary. Fusion wants the leaves, not one mega-kernel wrapping the
  block.

Do not leave an 80-line stride walk as a private `_softmax` on
`NumericBlock` and call that “extracted.” The extracted form is the typed
kernel leaf. The bag helper is debt until it is deleted.

### 4. `T` is pinned at the route, not carried as a bag

| Route | `T` |
| --- | --- |
| `forward` / `prefill_cached` | `size T` at the call site |
| `decode_step` | `T = 1` |
| `decode_block` | `size T` at the call site |

This is stronger than Wave 0’s “activations may stay staged.” The default
is recorded below and is revisitable. Frozen GEA numbers (`T=8/36`,
`D=960`, `L_max=76`) are **not** copied into the host assembly — those
belong to `gradus:kernel`.

### Blast radius (not one file)

| Surface | Role |
| --- | --- |
| `src/model/dense.fab` | `load` + rewrite of public routes; delete bag wrappers |
| `src/transformer.fab` | typed `dense_block` / `dense_block_cached` twins |
| `src/nn.fab` | typed `rmsnorm` twin if still absent |
| `src/generation.fab`, `src/block_verify.fab` | public-signature consumers |
| `src/model/dense.proba`, `generation.proba`, `prepared_state.proba`, `block_verify.proba` | proof |
| `exempla/dense-model`, `dense-prefill-smollm2`, `dense-prefill-qwen2`, `dense-decode-smollm2`, `generate-smollm2` | package callers |
| `docs/api-reference.md`, `docs/module-map.md`, `docs/diagnostics.md` | truth pass |

`src/kernel.fab` is the style reference, not a write target.

### Forbidden fake rewrite

Tidying `dense.fab` (DRY the four loops, keep calling today’s
`transformer.dense_block(NumericBlock, …) → NumericBlock`) is out of
scope. That hides the carrier one stack frame down and does not satisfy
the invariant.

### Non-goals

- No edits to `src/kernel.fab` device entries or frozen GEA geometry.
- No device handles, residency, scheduling, or physical cache rollback.
- No autograd / `gradus:gradient` path (dense stays forward-only).
- No MoE / hybrid / SSM assembly (`MODEL-03` / `qwen36`).
- No folding this work into kernel-purity Waves 1–3 as “purity edits.”
- No radix work to invent a new `@ kernel` admission (shape-generic
  entries already check green per `docs/shape-generic-kernels.md`; this
  goal consumes that form, it does not land compiler support).
- No `@ kernel` on effectful functions (load, diagnostics, cache admit,
  generation, parsers). A rejected annotation is not a style debate —
  it is a purity defect.
- No permanent public `NumericBlock` shim on `forward` / decode once the
  typed routes land (see open question 3 if the operator wants a temporary
  alias).

## Units (lowering sketch — refine via `$delivery`)

| Unit | Scope | Depends on | Hand evidence |
| --- | --- | --- | --- |
| 1 | `DenseModel` + `load`: pin each canonical tensor from the resolver; fail closed on missing / bad shape / bad config. Existing bag routes unchanged. | — | — |
| 2 | Typed `@ kernel` `rmsnorm<size T, D>` leaf in `nn.fab` if purity Wave 1 has not landed it. Skip when that twin already exists. Same rule for any other algebra leaf this goal has to introduce (residual, SwiGLU, …): extract + `@ kernel`, do not inline. | — | — |
| 3 | Typed `dense_block` / `dense_block_cached` **ordinary** assemblers in `transformer.fab` that compose `@ kernel` leaves (linear, rmsnorm, …). Not themselves `@ kernel`. Bag twins remain until unit 5. | 2 | — |
| 4 | Rewrite `forward` / `prefill_cached` / `decode_step` / `decode_block` to take the typed model and compose unit 3. Public signatures drop the in-graph resolver and `NumericBlock` logits. | 1, 3 | — |
| 5 | Migrate callers and proofs listed in Blast radius. Delete bag wrappers (`_shape`, `_transpose`, `_collect`, `_linear`, `_rmsnorm`, `_block`, `_map_cached`). Truth-pass docs. | 4 | — |

Unit 4 is the clean break. Unit 1 alone is not done.

## Validation

Closeout requires all of the following:

- `faber check src/model/dense.fab src/transformer.fab src/nn.fab` green, then
  `faber check .` in `gradus/`.
- `faber test src/model/dense.proba` plus the migrated consumer suites
  (`generation.proba`, `prepared_state.proba`, `block_verify.proba`) prove
  the same logit / cache contracts the current fixtures pin (tied and
  untied, overflow, gap, `TerminusExcedit`, `BadShape`, `BadConfig`).
- After unit 4, `rg -n 'NumericBlock' src/model/dense.fab` hits only the
  `load` / resolver admission seam (and error-conversion arms that wrap
  load-edge failures). No `NumericBlock` in `forward` / decode signatures
  or layer loops.
- `rg -n 'linear_carrier|_map_cached|_collect|_transpose' src/model/dense.fab`
  is empty after unit 5.
- `./scripta/check-compile` stays green for the gated dense exempla that
  this goal migrates.
- API reference / module-map / diagnostics match the typed public surface.

## Delivery checklist

| Check | Enforced by |
| --- | --- |
| Typed graph does not call bag `dense_block` / `linear_carrier` / `rmsnorm` | unit-5 `rg` closeout |
| `NumericBlock` confined to `load` / resolver | unit-5 `rg` closeout |
| Migrated proba keep existing pin tolerances (dense.proba f64 refs @ 5e-4) | `faber test src/model/dense.proba` |
| Gated exempla still check | `./scripta/check-compile` |
| Docs match public signatures | truth pass in unit 5 |

## Ledger

| Unit | Status | Seat | Receipt | Notes |
| --- | --- | --- | --- | --- |
| 1 | pending | — | — | Admit/pin + `DenseModel` |
| 2 | pending | — | — | Typed `rmsnorm` twin; skip if Wave 1 landed it |
| 3 | pending | — | — | Typed `dense_block` twins |
| 4 | pending | — | — | Rewrite dense routes; public clean break |
| 5 | pending | — | — | Callers, delete bag wrappers, docs |

## Open questions

1. **`T` on activations** — default: pin `T` on each public route
   (`prefill<size T>`, `decode_step` at `T=1`, `decode_block<size T>`).
   Do not carry activations as `NumericBlock` through the graph. Wave 0
   still permits staged activations; this goal takes the kernel-side
   default. Revisit if size-generic library returns fail `SEM014` at the
   chosen signatures.
2. **Block placement** — default: typed twins in `transformer.fab`. Dense
   stays an assembler. Do not inline the block into `dense.fab`.
3. **Public API** — default: clean break in unit 4. Resolver is an argument
   of `load` only. No permanent bag overload of `forward`. A temporary
   wrapper that loads-then-forwards may exist between unit 4 and unit 5
   so exempla migrate in one Hand, then it is deleted.
4. **Relationship to kernel-purity Wave 2** — default: this goal owns the
   host/logical assembly. Wave 2 owns moving one production chain onto
   kernel entries. Dense must not hard-code GEA shapes (`960`, `76`, `36`)
   to “use the kernel file.” Shared typed twins (unit 2–3) may unblock
   both; they are not the same delivery.
5. **`dense_block` as `@ kernel`** — default: no. It is composition of
   leaves. Marking the assembler `@ kernel` would force in-body calls or
   one fused-at-source mega-body and hide the split fusion is meant to
   see. Revisit only if a later program-composition form admits a kernel
   that *names* other kernels without inlining them.
