# Gradus numeric flexibility + performance architecture — the llama.cpp-parity bar

**Status**: committed `4004e32`; GI4 dtype amendment operator-accepted 2026-08-18 (need `1d3967ed`)
**Author**: head-cto (Vivi handle `904d57dd`)
**Date**: 2026-08-18
**Operator bar**: "The stated goal is to run Qwen, but the real goal is to run Qwen AT
LEAST AS FAST AS native llama.cpp." Everything below is sized against that bar, not
against "runs".

**Evidence rule**: every claim cites live code at file:line. Where a factory doc
disagrees with git, git wins and the doc is named as the defect. Reference repos:
`radix` @ `8c5c6a3a8`, `gradus` @ `012d411`, `hosts` (partition contract), and
`~/work/llama.cpp` @ `c8e03ce81`.

---

## 1. Grounding summary (what is actually on main)

Verified 2026-08-18, in the order the task names:

1. **Gradus live library** — 33 modules, 750 declared functions
   (`gradus/docs/module-map.md:11-60`). Numeric posture: f32 self-hosted
   forward with a `5e-4` absolute structural band and exact token pins
   (`gradus/docs/numeric-tolerances.md:28-36`, §4). The inference tier is
   `gradus:decode` / `gradus:cache` / `gradus:sampling` / `gradus:generation`
   (`docs/module-map.md:56-58`).
2. **Adapter layout conventions (just landed, both models verified vs GI2
   goldens)** — GGUF `token_embd` is dim0-innermost, so the stored f32 buffer
   is already `data[token*D+d]`: gather is token-major, no transpose
   (`gradus` commit `37cdf7c`, `src/model/dense.fab:162` `_token_major_view`);
   the linear families (`attn_q/k/v/o`, `ffn_gate/up/down`) are stored
   **K-major** (`stored[n*K+k] = W[k,n]`) and the adapters transpose after
   materialize (commits `012d411`, `05f5a3a`). Tied `lm_head` reuses the
   embed view transposed to true row-major (`dense.fab:309+` forward tail).
   These conventions are the load-side contract every storage-format knob
   must honor.
3. **kernel_plan/ is the recipe authority** — closed variant set, **no backend
   tag**, "adding a variant is an explicit, reviewable change"
   (`radix/crates/radix-mir/src/kernel_plan/plan.rs:44-50`). Admitted recipes:
   `Elementwise, TiledMatMul, TreeReduction, Transpose, AxisReduction,
   RowSoftmax, LayerNormalization, Gather, RmsNormalization, Rope,
   CausalMaskedSoftmax, QuantizedMatMul, GroupedMatMul, SsmConv1d, SsmScan`
   (`plan.rs:51-112`). Conservative constants: 32 KiB workgroup memory
   (`plan.rs:4-8`), 8×8 matmul tile (`plan.rs:12-17`).
4. **EXEC-02 locked decisions** — ten locked defaults recorded in
   `radix/docs/factory/gpu-production-readiness/exec02-packed-kernels-delivery.md:69-80`,
   including backend-neutral plans (decision 6), in-kernel block-wise dequant
   (§2, `:42-46`), no whole-model F32 expansion (decision 4), f32 accumulation,
   and the closed §5 layout table.
5. **Fusion OF-1/2 on main** — typed elementwise expression plan landed
   (`radix` commits `d8ce4d8a6` OF-1, `aebec9180` OF-2;
   `crates/radix-mir/src/elementwise_plan.rs` exists on main). Goal status:
   wave 1 (OF-0…OF-2) lowered and dispatch-ready; OF-3…OF-5 (backend emitter
   migration, driver control) deferred behind R-PACK-05
   (`docs/factory/operation-fusion/goal.md:3`). Operator boundary ruling:
   compiler-internal optimization pass only, never automatic user-code fusion
   (`goal.md:53-59`).
6. **Fragments NF** — goal doc says **planned, execution not started**
   (`docs/factory/nucleum-fragments/goal.md:3`), but git shows partial landing:
   `afca0feb5` (NucleumRole Entry/Fragment plumbing through HIR and MIR) and
   `1adda171c` (device-safe effect-subset check) are contained in `main` and
   `factory/merge`. Docs are stale by default; the role model is landing.
   Operator rulings locked: manual `@ nucleum fragment` annotation only,
   intent is composable shared kernel helpers (inline guarantee), **not** a
   performance claim (`goal.md:32-46`).
7. **R-PACK-02 kernels complete** — packed kernels B..Q, per-format in-kernel
   dequant + tiled GEMM on Metal/NVVM, on radix main `b199834f8`
   (`gpu-production-readiness/CAMPAIGN.md:3`). Metal emitter: "Landed layout
   bodies: BF16 convert, Q8_0, Q4_K, Q5_0, Q5_K, Q6_K", fail-closed on
   anything else (`radix-mir-metal/src/emit/quantized_matmul.rs:3,87`); NVVM
   carries module-level dequant helpers (`radix-mir-llvm/src/nvvm/quantized.rs:8-11`).
   Device-run of the packed path is reserved for R-PACK-05; prefill today
   executes the GI3 declared-f32 bring-up conversion
   (`evidence/exec02/r-pack-02-prefill-comparison.md`).
8. **llama.cpp reference** (`~/work/llama.cpp` @ `c8e03ce81`) — read at its
   actual structures: KV cache types (dense/unified streams, SWA, arch-specific
   sparse/hybrid), format dispatch (type traits + per-backend kernels), layer
   filtering, and its knob surface. Cited throughout §4–§8. Our prior study
   (`radix/docs/design/llama-lessons-learned.md`, reference revision pinned at
   `:5-8` to this same commit) remains the durable cross-cutting analysis.

Cross-repo seam that already exists and this design builds on: **Gradus owns
semantic layout facts; Radix consumes typed facts into kernel plans; Hosts owns
physical allocation.** EXEC-02 decision 2 ("per-tensor layout authority stays
Gradus-owned", `exec02-…-delivery.md:72`) and the GI4 `KvCacheLayout` freeze
("consumed, not re-derived", `hosts/crates/host-coordinator/src/partition.rs:95,119-122`
+ `radix/docs/factory/gpu-inference-gguf/gi4-contract.md:93-108`).

---

## 2. Goal and the two bars

- **Stated bar**: execute the admitted Qwen3.6-35B-A3B row (753 tensors; per-tensor
  storage distribution BF16 2 · F32 368 · Q4_K 82 · Q5_K 38 · Q6_K 4 · Q8_0 259 —
  `exec02-…-delivery.md:96-98`).
- **Real bar**: match or beat native llama.cpp **throughput** on the same model,
  same hardware (burgus Metal M5 Max; pharos CUDA RTX 5070 for dense rungs —
  `exec02-…-delivery.md:99-101`). Correctness comparators already exist
  (ORACLE delivery, `gpu-production-readiness/oracle-llamacpp-comparison-delivery.md`);
  **throughput evidence needs its own harness** (§8.3) — llama.cpp separates
  prompt-processing and token-generation benchmarks precisely because the knobs
  that move them differ (`llama-lessons-learned.md:638-692` §11).

Design thesis, from the operator's strategic context: we control language →
libraries → lowering → kernel creation → fusion → GPU code. llama.cpp controls
only a fixed precompiled kernel library plus runtime dispatch. Therefore **our
knobs should be front-loaded into lowering-time specialization** (emit a
model-specific kernel set) rather than runtime dispatch tables, and the runtime
surface stays small and honest.

---

## 3. Format matrix (storage × compute × backend)

### 3.1 Current state

- **Closed storage set (Radix)**: `PackedStorageLayout = {F32, Bf16, Q8_0,
  Q4_K, Q5_K, Q6_K, Q5_0}` with GGML ids `{0, 30, 8, 12, 13, 14, 6}`
  (`radix/crates/radix-mir/src/abi/contract.rs:162-192`). Unknown ids fail
  closed (`kernel_plan/packed.rs:122-130`).
- **Closed storage set (Gradus CPU dequant)**: same union
  `{F32, BF16, Q5_0, Q8_0, Q4_K, Q5_K, Q6_K}` (`gradus/src/model/dequant.fab:77-117`,
  GGML constants + block geometries).
- **Dequant classes**: `PassthroughF32 | NativeBf16Convert | Block (32-elem) |
  Superblock (256-elem)` (`kernel_plan/packed.rs:28-36`).
- **DType tags (Gradus)**: `DType` already includes an `f16` tag
  (`gradus/src/dtype.fab:74,90`) — but **F16 is not an admitted GGUF storage
  layout** in either repo. **F32 is confirmed admitted** (id 0, both repos).

### 3.2 The matrix

Compute axis is deliberately *not* storage: the four-representation model
(logical semantics / serialized encoding / backend-native rep /
accumulation+output) is already locked guidance
(`llama-lessons-learned.md:343-356` §7.2). EXEC-02 locks accumulation at
**f32** for packed GEMM (decision posture: in-kernel dequant, f32 accumulate —
`plan.rs:99-104`).

| Storage | bytes/elem (Gradus `dequant.fab`) | Compute class | Metal | CUDA/NVVM | WGSL | CPU |
| --- | ---: | --- | --- | --- | --- | --- |
| F32 | 4.0 | passthrough → `TiledMatMul` | ✅ (GI3) | ✅ (GI3) | ✅ (recipes) | ✅ (dequant `PassthroughF32`) |
| BF16 | 2.0 | native convert → f32 acc | ✅ (R-PACK-02) | ✅ (R-PACK-02) | ❌ → **admit** | ✅ (`NativeBf16Convert`) |
| **F16 (new)** | 2.0 | native convert → f32 acc | ❌ → **admit** | ❌ → **admit** | ❌ → **admit** | ❌ → **admit** |
| Q8_0 | 34/32 ≈ 1.06 | block dequant (32) | ✅ | ✅ | ❌ → later | ✅ |
| Q5_0 | 22/32 ≈ 0.69 | block dequant (32) | ✅ | ✅ | ❌ → later | ✅ |
| Q4_K | 144/256 ≈ 0.56 | superblock (256) | ✅ | ✅ | ❌ → later | ✅ |
| Q5_K | 176/256 ≈ 0.69 | superblock (256) | ✅ | ✅ | ❌ → later | ✅ |
| Q6_K | 210/256 ≈ 0.82 | superblock (256) | ✅ | ✅ | ❌ → later | ✅ |

Why F16 storage matters even though the Qwen GGUF stores no F16 weight tensors:
(1) llama.cpp's **KV default is F16** (`common/common.h:340-341`); (2) many
GGUF models (and our own checkpoints) do store F16 tensors; (3) F16 is the
natural *activation/IO* format for bandwidth-bound elementwise chains once the
envelope is derived. Admission follows the existing `NativeBf16Convert` pattern
exactly — a `NativeF16Convert` class, not a new algorithm family.

### 3.3 Rules the matrix obeys (all locked, none amended)

1. **Storage authority is the GGML block geometry pinned to `ggml-quants.c @
   a957b7747`** (EXEC-02 decision 3, `exec02-…-delivery.md:73`). F16/F32/BF16
   are plain 2/4-byte rows (`ggml/src/ggml.c:661-674` trait rows).
2. **One compute policy per matrix cell, chosen at lowering** — the plan
   carries the class (`packed.rs:41-52`), backends emit bodies or fail closed
   (`quantized_matmul.rs:87`). No backend silently widens.
3. **Quantized means native** (EXEC-02 decision 1): no CPU or F32 fallback for
   an explicit GPU route. The declared-f32 GI3 conversion stays bring-up-only
   (`exec02-…-delivery.md:72`).
4. **CPU activation quantization (llama.cpp's Q8_0/Q8_1 dot regime) is out of
   scope** for the GPU product. llama.cpp CPU computes `vec_dot_type` per
   weight format — F16→F16, Q4_0/Q8_0→Q8_0, Q4_1/Q5_1→Q8_1
   (`ggml/src/ggml-cpu/ggml-cpu.c:218-295`) — i.e., it *re-quantizes
   activations per ubatch* to integer blocks. Admitting an int8-dot compute
   class would amend the f32-accumulation lock; it is listed in §9 as an
   explicit future amendment need, not part of this design's waves.

---

## 4. KV structure abstraction

### 4.1 What exists today

- **Gradus** (`src/cache.fab`): a *logical, dense, append-only, f32* cache —
  one K and one V staged tensor `[positions, dimensio]` per session, exact
  history, `append` extends by exactly one position
  (`cache.fab:20-45` contract comment, `:332` f32/staged identity,
  `:352` append). Structural rules proven; **no paging, no windows, no
  quantized KV, no per-layer structure** (the decode row is one block;
  `layers` is an identity field, not storage shape).
- **Radix/Hosts**: physical KV is frozen as GI4's `KvCacheLayout` — five facts
  (`slots, context_length, layer_count, kv_head_count, head_dim`) plus `dtype`
  (opened **`{F32, F16, Q8_0, Q4_K}`**, F16 default — operator-accepted
  2026-08-18, need `1d3967ed`; revision record
  `docs/design/gi4-contract.md`) and `reserve_policy`; byte accounting
  single-sourced (`gi4-contract.md:93-108`; `hosts/…/partition.rs:119-122`).
- **Attention compute**: `CausalMaskedSoftmax` recipe materializes the score
  matrix then row-softmaxes (`plan.rs:93-96,217+`). No flash-attention recipe
  exists.

### 4.2 What llama.cpp actually has (file:line)

- **One cache class, many structures selected at model admission**:
  `llama_model` dispatches per architecture to `llama_kv_cache` (dense),
  `llama_kv_cache_msa` (sparse indexer), `llama_kv_cache_dsa` (DeepSeek sparse),
  `llama_kv_cache_dsv4`, `llama_kv_cache_iswa` (interleaved SWA),
  `llama_memory_hybrid` / `_iswa` (attention+recurrent), `llama_memory_recurrent`
  (`src/llama-model.cpp:2083-2300`).
- **Constructor knob set per cache** (`src/llama-kv-cache.h:99-117`):
  `type_k, type_v, v_trans, offload, unified, kv_size, n_seq_max, n_pad, n_swa,
  swa_type, mem_other, filter/reuse/share callbacks`.
- **Paged cells, not a ring**: each ubatch gets a `slot_info` mapping
  `token[i] → cell idxs[i]` (`llama-kv-cache.h:34-95`); holes are tolerated via
  indexed writes; contiguity is only required on the non-FA path
  (`slot_info::is_contiguous`, `:73-89`).
- **Unified multi-sequence streams**: `n_stream` + `seq_to_stream` share
  physical storage across sequences; isolation is metadata + mask
  (`llama-kv-cache.h:268,286`; lessons §12.2 `llama-lessons-learned.md:710-719`).
- **SWA as a first-class type**: `LLAMA_SWA_TYPE_NONE/STANDARD/CHUNKED/SYMMETRIC`
  with `is_masked_swa` masking math (`src/llama-hparams.h:20,143-145,381-404`);
  per-arch layer filters decide *which layers* use the SWA cache vs a full
  cache (`llama-model.cpp:2244-2268`).
- **GQA/MQA sharing**: per-layer `n_head` vs `n_head_kv`
  (`llama-hparams.h:320-326`); the cache stores only KV heads.
- **Quantized KV**: `type_k/type_v` accept any ggml type
  (`common.h:340-341` defaults F16); **quantized V requires flash attention**,
  V layout flips between FA (non-transposed) and classic (transposed) — the
  kq-mask dtype even switches F16/F32 with FA (`src/llama-graph.cpp:37`,
  `llama-context.cpp:247-248`).
- **Layer skipping inside memory**: layer-filter callbacks exclude layers from
  a cache instance — MTP draft heads get their own plain cache over only the
  nextn layers (`llama-model.cpp:2106-2121`), MSA indexer caches only layers
  ≥ `n_layer_dense_lead` (`:2080-2086`).

### 4.3 Our abstraction (design)

Keep the seam tripartite — Gradus (semantic), Radix (plan), Hosts (physical) —
and add a **typed KV structure descriptor** at the Gradus layer, lowered into
plan facts, consumed as `KvCacheLayout` by Hosts.

```text
KVStructure (gradus:cache, semantic)
  layers: per-layer-set list of
    { layer_set (indices), structure: Dense | SlidingWindow { n_swa, swa_type },
      kv_heads, head_dim }
  kv_dtype_k / kv_dtype_v: F32 | F16 | Q8_0 | Q4_K   (admitted per §3 rules)
  v_layout: Transposed | Straight                      (linked to attention family)
  sharing: Single | GqaShared (kv_heads < heads)       (already semantic in adapters)
  slots, context_length, reserve_policy                (GI4 facts, unchanged)
```

Knob set (each has default + cost in §7):

| Knob | Default | Why it is a knob |
| --- | --- | --- |
| `structure` per layer set | Dense | SWA bounds KV bytes by window, not context |
| `kv_dtype_k/v` | F16 (was f32 only) | KV bytes ÷2 (F16) or ÷4+ (Q8_0); bandwidth-bound decode gain |
| `v_layout` | Straight with FA recipe; Transposed with classic | llama.cpp proves these are one bundle with the kernel family (§4.2; lessons §12.5 `llama-lessons-learned.md:781-808`) |
| `slots` / `unified` | 1 | multi-sequence + prefix sharing (metadata-only forks) |
| `n_pad` | 1 | alignment for kernel vector widths |
| `reserve_policy` | GI4 reserve | headroom at admission |

**Locked-contract constraints honored**: `KvCacheLayout` five facts stay; the
`dtype` field opening from closed-f32 to `{F32, F16, Q8_0, Q4_K}` is a **GI4
contract revision** — the freeze itself says "a dtype change is a contract
revision, never a silent widening" (`gi4-contract.md:105-106`). Operator
accepted 2026-08-18 (need `1d3967ed`); revision record
`docs/design/gi4-contract.md`. Context-shift on quantized K requires dequant→rotate→requant
(lessons §12.4, `:759-777`); we keep the lessons' guidance — prefer explicit
stop-at-capacity over a generic shift until a shift policy is measured.

**Attention kernel family must be negotiated as a bundle, not as independent
booleans** — the llama.cpp lesson is explicit: `type_k`, `type_v`, and a FA
flag are not a durable contract; the bundle is semantics+mask+K/V type+layout+
head dims+block rules+kernel family+workspace (lessons §12.5, `:789-808`).
Our equivalent: a `KVStructure` → attention-recipe resolution table at
lowering time; an infeasible combination (e.g., Q4_K V without the FA recipe,
block size not dividing head_dim) fails closed at plan validation, never at
runtime.

### 4.4 What we deliberately do NOT adopt

- No cell-defragmentation pass (llama.cpp's is deprecated; holes are tolerated
  — lessons §12.4).
- No per-sequence physical streams beyond `slots` until multi-sequence serving
  is a real goal (the MD/multi-device campaign owns that frontier;
  `docs/factory/gpu-inference-multi-device/`).
- No arch-specific sparse caches (msa/dsa/dsv4) in wave scope — those belong to
  admitting those architectures, reusing the same descriptor (the descriptor's
  per-layer-set list is the extension point).

---

## 5. Layer-slicing hooks (streamlining / obliteration first-class)

### 5.1 Today

`gradus/model/dense.fab:309` `forward` is a fixed `while stratum ≺ cfg.layers`
loop (`:356`) over all blocks, then final norm + head projection. Nothing can
skip, replace, or redirect a layer. In the compiled route the same graph is
emitted monolithically. llama.cpp has *no* authoring-level layer-skip knob at
all (its layer filters are memory-structure facts, §4.2; its offload split is
a placement knob, `src/llama-model.cpp:1318-1333`).

### 5.2 Design

A **LayerPlan** — an ordered per-layer execution policy authored beside the
architecture config, consumed by `forward` (interpreted) and by lowering
(compiled, where it pays):

```text
LayerPlan = list of {
  layer: int
  mode: Normal
       | Skip                    # drop the block entirely (streamlining)
       | SkipAttention           # residual-only block (SWA-shy / speed rows)
       | Obliterate { direction } # project residual orthogonally to a direction
       | Offload { target }       # future: CPU/GPU split (multi-device campaign)
}
```

Semantics: `Skip` = identity on the residual stream; `SkipAttention` = skip the
attention sublayer, keep MLP; `Obliterate` = `h ← h − (h·d)d` with a unit
`direction` per layer (ablation/abliteration family). Every mode is a pure
function of the config — deterministic, seed-free, verifiable.

**Why first-class and why now**: (1) it is a *semantic* surface (changes the
computed function), so it belongs in Gradus, not in a runtime flag; (2) at
lowering it is free specialization — a skipped layer emits nothing; an
obliterated layer emits one fused elementwise projection (the OF-1/OF-2 typed
plan surface is exactly the right carrier); (3) llama.cpp cannot express it
without patching C++ — this is one of our structural advantages.

**Acceptance honesty**: layer-sliced execution diverges from the reference
model *by construction*. The frozen GI0 numeric contract (greedy top-1 exact,
`exec02-…-delivery.md:74-75`) governs unmodified execution; a sliced run needs
its own recorded acceptance (e.g., KL/logit-band vs a pinned sliced reference,
or operator-accepted quality evidence). This is a **new policy decision** for
mind/operator, listed in §9 — never a silent weakening of the existing oracle.

---

## 6. Tuning surface: what is a dial, where it lives

### 6.1 The compile-time / runtime split (our structural advantage)

llama.cpp's knob surface is runtime by construction: a precompiled kernel
library plus dispatch tables (type traits `ggml.c:631-874`; CPU `vec_dot_type`
`ggml-cpu.c:218-295`; backend kernel selection). Its dials are CLI/context
params: `n_batch/n_ubatch` (`common.h:443-444`, defaults 2048/512), threads
(`llama-cparams.h:18-19`), `flash_attn` AUTO (`common.h:488`), `cache_type_k/v`
(`common.h:340-341`), `kv_unified` (`common.h:562`), `causal_attn`,
`offload_kqv`, `pipeline_parallel` (`llama-cparams.h:37-53`).

**We can specialize at lowering — llama.cpp cannot.** Concretely:

| Specialization (compile-time, per model+config) | Mechanism we already have |
| --- | --- |
| Per storage-format kernel body (block geometry constant-folded, unrolled dequant) | `QuantizedMatMul` + `PackedDequantResolution` (`packed.rs:41-52`) — the block geometry is a plan constant, not a runtime branch |
| Per shape-class tile/workgroup | plan constants (`MATMUL_TILE`, `WORKGROUP_…` are named constants precisely so a backend never hardcodes — `plan.rs:12-24`) |
| Per-layer GQA ratio, head_dim, rope pair policy baked into the attention recipe | `RopePlan`/`CausalMaskedSoftmax` carry the facts (`plan.rs:174-228`) |
| Regime-specialized executables (prefill graph vs decode graph) | workload modes already frozen `Prefill | ScalarDecode` (`gi4-contract.md:111-123`) |
| Fused elementwise chains with one typed plan (no runtime fusion checks) | OF-1/OF-2 typed elementwise plans (`elementwise_plan.rs`; `operation-fusion/goal.md:3`) |
| Shared in-kernel dequant helpers, guaranteed inlined | fragments (`@ nucleum fragment`, inline guarantee — `nucleum-fragments/goal.md:32-46`) |

Runtime knobs (must stay dynamic — they change per invocation): batch
composition (`n_tokens`), `n_kv` (KV length), sequence ids/masks/positions,
sampling parameters. Batch/ubatch *sizes* are admission knobs: they size
workspace and select between the regime-specialized executables; they are not
kernel-code branches.

### 6.2 Dial inventory and home

| Dial | Home | Default |
| --- | --- | --- |
| Per-tensor storage format | GGUF facts + admission/repack policy (Gradus) | as-stored (never silent re-quant) |
| Compute class per cell | Radix plan resolution (fail-closed) | per §3.2 |
| KV structure + dtypes + v_layout | `KVStructure` (Gradus) → plan bundle | Dense / F16 / family-linked |
| LayerPlan | Gradus model config | all-Normal |
| AblationSpec (recipe — §13) | Gradus model config, beside LayerPlan | empty (no transforms; model is base-as-stored) |
| Ablation delivery mode (§13.1) | derived from transform type — not a user knob | bake for weight/bias transforms, runtime for activation projection |
| Batch / ubatch | execution session admission (Faber) | prefill 2048/512 (llama.cpp parity, `common.h:443-444`), decode 1 |
| Tile/workgroup per shape class | lowering specialization | 8×8 today; per-class after measurement |
| Fusion | compiler-internal (locked boundary) | on for elementwise-only chains |
| Attention family (classic vs flash) | lowering bundle resolution | flash when the recipe admits the bundle |
| Backend | `faber run --backend {auto,metal,cuda}`, fail-closed (`radix/crates/faber/src/cli/mod.rs:359-391`) | auto |

No dial exists without (a) a default, (b) an expected-gain/cost entry in §7,
and (c) a fail-closed infeasible-combination path. This is the
flexibility-vs-optimization tension resolved: the *config space* stays small
because infeasible bundles are rejected at plan time and profitable constants
are burned into code rather than branched on at runtime.

---

## 7. Cost model — knob → default → expected gain → cost

Roofline framing: decode is weight+KV **bandwidth-bound**; prefill is
**compute-bound** (lessons §11, `:638-692`). Gains below are stated as
mechanisms, with measurement as the done-when (no number is claimed without a
run — `benchmark-method.md` + lessons §2.2 evidence labels).

| Knob | Default | Expected gain (mechanism) | Cost / risk |
| --- | --- | --- | --- |
| KV dtype F32→F16 | F16 after wave 2 | KV bytes ÷2 → long-context decode reads ÷2 on the KV stream | numeric envelope must be re-derived (GI2-3-style per-band, not inherited — precedent: Q2 envelope is SmolLM2-only, `exec02-…-delivery.md:75`); attention kernels read half |
| KV dtype →Q8_0 (K or V) | off | KV bytes ÷4 vs F32 (÷2 vs F16) | **requires FA recipe** (llama.cpp: quantized V requires FA — `llama-graph.cpp:37`, lessons §12.5); block 32 must divide head_dim; K-shift becomes dequant-rotate-requant |
| Sliding window | off (model facts decide) | KV footprint O(window) not O(context); decode bandwidth at 100k+ ctx drops by context/window | mask correctness per `swa_type` (4 masking math variants — `llama-hparams.h:381-404`); eviction policy; wrong-window silently degrades quality → pinned oracle rows |
| GQA-shared KV | on when model says so | already realized (KV heads only; `dense.fab` kwidth = kv_heads·head_dim) | none (admission is model fact, not user dial) |
| Unified slots / prefix sharing | 1 slot | metadata-only prefix forks; serving throughput | mask/identity bookkeeping; deferred to serving goal |
| Flash attention | classic until wave 3 | avoids materializing T×n_kv scores → prefill workspace ÷O(T·n_kv) and long-context decode bandwidth; *enabler* for quantized V | new recipe variant (explicit reviewable change); Metal simdgroup / NVVM warp paths; V layout flips |
| Decode narrow-GEMM recipe | tiled 8×8 today | batch-1 decode is GEMV-shaped; llama.cpp has dedicated MMVQ (dequant×vector) vs MMQ (matrix×matrix) families (`llama-lessons-learned.md:523-533`) — a split-K/narrow recipe cuts wasted tiles and launch count | second matmul recipe family; dispatch by workload mode |
| Tile/workgroup per shape class | 8×8 | prefill compute-bound: larger tiles raise arithmetic intensity (llama.cpp CUDA MMQ tiles are much larger than 8) | shared-memory limit is conservative 32 KiB (`plan.rs:4-8`) — needs the per-device limit channel the constant already anticipates |
| F16 activations on elementwise chains | off until measured | elementwise chains are bandwidth-bound; F16 IO halves bytes while accumulation stays f32 | envelope derivation; OF plan must carry dtype facts (typed plans make this safe) |
| Layer Skip/SkipAttention/Obliterate | all-Normal | drops whole GEMM families — gain ∝ share of removed FLOPs/bandwidth; uniquely ours | quality divergence by construction → **separate acceptance policy** (§9); per-layer oracles |
| Ablation bake — weight orthogonalization (§13.2) | off (empty AblationSpec) | zero runtime cost: weights transformed once at materialization; effective tensors are ordinary tensors, no new plan variants | load-time CPU O(2·D²) per target matrix; storage policy per quantized target — declared requant band or F32-promote bytes (§12-5); admission digest verification |
| Ablation runtime — activation projection (§13.2) | off | one fused elementwise projection per site per token (OF-1/OF-2 carrier, identical shape to §5.2 Obliterate); enables direction search without re-bake | one extra elementwise op per site per decode step; divergence band per NEED `e52dd09a` (§13.4); direction tensor resident (D floats per site) |
| Ablation bake — bias edit (§13.2) | off | bias folded at materialization (today's biases are synthesized zero — `dense.fab:380-385`), zero runtime cost | none beyond the divergence band |
| Batch/ubatch (prefill) | 2048/512 | fills the device; too-large ubatch spills workspace | workspace sizing vs partition ledger class budgets (`partition.rs:95-122`) |
| Repack to backend-native layout | off (direct-consume) | llama.cpp Metal repacks some formats for vectorized loads (lessons §9.3) | setup time + peak memory; must be declared repack, never "direct" (anti-pattern list, lessons §7.4 `:384-397`) |
| int8 activation dot (CPU regime) | **not admitted** | would be the CPU throughput lever (llama.cpp CPU `vec_dot_type`) | **amendment to f32-accumulation lock** — need to mind; GPU waves never depend on it |

---

## 8. Performance-path analysis

### 8.1 What llama.cpp does that we do not (the gap list, ranked by expected decode/prefill impact)

1. **Flash attention** — fused QK^T→softmax→V without materialized scores
   (`ggml/src/ggml-cuda/fattn.cu`; `llama-context.cpp:551` fused-op probe).
   We materialize scores then `CausalMaskedSoftmax` (`plan.rs:93-96`). This is
   the single biggest prefill-workspace and long-context decode lever, and the
   prerequisite for quantized V.
2. **Regime-split GEMM families** — matrix-matrix (MMQ) vs matrix-vector
   (MMVQ) kernel families selected by prompt-vs-decode shape (lessons §9.2).
   We have one `TiledMatMul`/`QuantizedMatMul` for both regimes.
3. **Quantized KV + SWA + unified streams + paged cells** (§4.2) — we have
   dense f32 append-only (`cache.fab`) plus the W2-U1 `KVStructure`
   descriptor; physical `KvCacheLayout.dtype` is opened to
   `{F32, F16, Q8_0, Q4_K}` (`docs/design/gi4-contract.md`).
4. **Graph reservation and reuse** — reserve prompt+decode graph shapes once,
   reuse across steps (lessons §10.1, `:565-581`). Ours is EXEC-03 (persistent
   prepared sessions) — pending, correctly sequenced after EXEC-02.
5. **Runtime shape/type dispatch breadth** — per-backend kernel tables keyed
   by (type × shape class) (`ggml.c:631+`, `ggml-cpu.c:218+`). We have plan
   variants but one algorithm per recipe; per-shape-class specialization is
   our answer (§6.1), not table growth.
6. **Thread/batch CLI surfaces** (`common.h:443-444`, `llama-cparams.h:18-19`).
   We have `--backend` only (`cli/mod.rs:359-391`); the admission knobs in §6.2
   close this.

### 8.2 What we can do that llama.cpp cannot (the parity-and-past list)

1. **Lowering-time specialization**: emit a kernel set specialized per model —
   constant block geometries, baked GQA ratios, unrolled dequant, per-layer
   rope policy, per-shape-class tiles. llama.cpp dispatches a fixed library at
   runtime; its "specialization" is compile-time C++ templates over a fixed
   candidate set, not per-model codegen.
2. **Typed elementwise fusion across the whole graph** (OF-1/OF-2 landed;
   OF-3/4 emitter migration queued behind R-PACK-05). llama.cpp fusion is
   hand-written ggml ops.
3. **Guaranteed-inline shared device helpers** (fragments): one dequant/
   unpack implementation reused across kernels; llama.cpp duplicates unpack
   logic across MMQ/MMVQ/fattn variants (the exact pain the fragments goal
   records — `nucleum-fragments/goal.md:23-30`).
4. **LayerPlan as a semantic, verified surface** (§5) — streamlining and
   obliteration with per-mode acceptance; llama.cpp has no equivalent authoring
   surface.
5. **Fail-closed admission with a byte-exact ledger** (partition budget
   classes incl. KV — `partition.rs:95-122`); llama.cpp is best-effort at
   load.
6. **Versioned numeric policy + first-divergence tooling**
   (`numeric-tolerances.md`; ORACLE harness) — stronger perf/quality evidence
   discipline than ggml's ad-hoc checks.

### 8.3 Throughput evidence (what "parity" is measured against)

The ORACLE delivery pins the *correctness* comparator; throughput needs a
pinned benchmark protocol: fixed prompts (the two pinned Unicode probes),
`prefill` and `decode` reported separately (regime labels are frozen —
`gi4-contract.md:111-123`), same machine, same model file, llama.cpp pinned
revision + build flags recorded, our config recorded per dial. Gradus
`docs/benchmark-method.md` is the existing method home; the perf harness unit
is in §10 wave 6. **No perf claim in this doc is evidence** — every gain in
§7 is a mechanism awaiting measurement (lessons §2.2, `:75-80`).

---

## 9. Locked decisions: honored vs amended

| Locked decision | Authority | Status under this design |
| --- | --- | --- |
| Backend-neutral kernel plans; no backend tag; variant addition is explicit reviewable change | `plan.rs:44-50`; EXEC-02 decision 6 | **HONORED** — new variants listed in §10 as explicit additions |
| In-kernel block-wise dequant; never whole-model F32 | EXEC-02 §2/§3-4 | **HONORED** — F16 admission follows `NativeBf16Convert` pattern |
| f32 accumulation (packed GEMM) | EXEC-02 posture, `plan.rs:99-104` | **HONORED** for all waves. Int8 activation dot (CPU) would amend → **need to mind** (not scheduled) |
| No whole-model F32 load | EXEC-02 decision 4 | **HONORED** |
| kernel_plan/ single recipe authority; recipe ops never silently `Elementwise` | operation-fusion goal rulings (`goal.md:53-59`) | **HONORED** |
| Gradus owns per-tensor layout authority; Radix consumes typed facts | EXEC-02 decision 2 | **HONORED** — `KVStructure` continues the pattern |
| GGUF-A7 "quantized means native"; declared-f32 is bring-up only | `gguf-a7-…-delivery.md:22-30` | **HONORED** |
| OF operator boundary (compiler-internal fusion only) + schedule (OF-3..5 behind R-PACK-05) | `operation-fusion/goal.md:53-59` | **HONORED** — no wave touches backend emitters before R-PACK-05 |
| Fragments rulings (manual annotation; inline guarantee, not perf claim) | `nucleum-fragments/goal.md:32-46` | **HONORED** — perf comes from kernels, not annotation |
| GI4 `KvCacheLayout` dtype closed f32 | `gi4-contract.md:105-106` | **AMENDED — operator-accepted 2026-08-18, need `1d3967ed`**: dtype opened to `{F32, F16, Q8_0, Q4_K}`, F16 default; five facts + single byte authority unchanged. Revision record: `docs/design/gi4-contract.md` |
| GI0 numeric contract (greedy top-1 exact, frozen envelope) | `gi0-numeric-contract.md`; exec02 decision 5 | **HONORED for unmodified execution**; layer-sliced runs need a **new acceptance policy — need to mind** (§5.2), never a silent weakening |
| llama.cpp comparator-only, never in the execution path | exec02 decision 5 | **HONORED** — perf harness runs it offline as the reference bar |

Two amendment needs + one policy need are filed to mind with this report
(§11); nothing in this design silently breaks a lock.

---

## 10. Implementation plan (Hand-unit-shaped, ordered)

Sizing follows the fragments/fusion precedent: one-behavior-family micro-units,
~3–6k est tokens each, write-disjoint scopes, fail-closed negatives, first
failing oracle named (same shape as `exec02-…-delivery.md:59-66` micro-units).

**Wave 1 — format matrix completion (F16 admission).** Parallel-safe; no
emitter-wave conflict (R-PACK-03/04 own `GroupedMatMul`/`Ssm*` arms; OF-3..5
own the elementwise emitters — these units touch neither).

| Unit | Repo/scope | Done-when |
| --- | --- | --- |
| W1-U1 `PackedStorageLayout::F16` | radix `abi/contract.rs` + `kernel_plan/packed.rs` (`NativeF16Convert` class, id 1; fail-closed set update) | `cargo test -p radix-mir` layout round-trip incl. id 1; unknown ids still fail closed |
| W1-U2 F16 compute bodies | radix `radix-mir-metal/emit/quantized_matmul.rs` + `radix-mir-llvm/nvvm/quantized.rs` (2-byte load → f32 convert → accumulate) | per-format kernel tests green; "no body" fail-closed removed for F16 only |
| W1-U3 Gradus F16 dequant | gradus `src/model/dequant.fab` (`GGML_F16 ← 1`, widen union set; proba pins vs f64 oracle) | gradus proba green; union-set doc row updated |
| W1-U4 WGSL F16 elementwise IO | radix `radix-mir-wgsl` convert in existing recipe paths | wgsl kernel tests; no new variant |

**Wave 2 — KV structure abstraction (semantic side first).**

| Unit | Repo/scope | Done-when |
| --- | --- | --- |
| W2-U1 `KVStructure` type | gradus `src/cache.fab` (per-layer-set structure, dtype tags, v_layout, sharing; identity/wire extension; fail-closed mismatch) | cache proba: identity pins + mismatch negatives green |
| W2-U2 SWA mask semantics | gradus `src/attention.fab` (4 `swa_type` mask rows + validation) | attention proba mask pins per type green |
| W2-U3 attention bundle resolution | radix `kernel_plan` (KV view facts on the attention recipe: n_kv dynamic, window params, v_layout; wire mirror mechanical per GI3-1 discipline) | plan validation rejects infeasible bundles (Q-V without FA recipe; block∤head_dim) — negative tests |
| W2-U4 F16 KV execution | radix metal attention path reads F16 K/V (f32 scores) + gradus decode wiring | dense-rung prefill/decode vs GI2-3 golden within a *derived* F16-KV envelope; envelope derivation committed |

**Wave 3 — flash-attention recipe** (new `CollectionKernelPlan` variant —
explicit reviewable change; Metal simdgroup first, NVVM second). Done-when:
dense-rung top-1 exact vs golden; prefill workspace reduction measured.

**Wave 4 — decode-regime kernel** (`NarrowMatMul`/dequant-GEMV recipe family,
split-K, selected by workload mode at lowering). Done-when: decode-step time
improves vs tiled path on the dense rung, tokens identical.

**Wave 5 — LayerPlan hooks** (gradus config + `forward` modes; lowering
specialization; per-mode acceptance rows). Done-when: skip/obliterate proba
rows green; sliced-run acceptance policy decided (§9 need).

**Wave 5b — ablation layer** (§13 addendum; after wave 5 — builds on LayerPlan
config + acceptance rows; W5b-U4's manifest fields land with wave 6's
admission manifest).

| Unit | Repo/scope | Done-when |
| --- | --- | --- |
| W5b-U1 `AblationSpec` type + admission validation | gradus `src/model/` (spec type beside LayerPlan: transform list, backward-only reference rule, unit-direction check, duplicate-target rejection — §13.3) | proba: empty-spec identity pin (spec-absent ≡ base-as-stored) + validation negatives (forward reference, wrong-length direction, duplicate target, zero vector) green |
| W5b-U2 weight bake at materialization | gradus `src/model/dense.fab` resolver seam + `dequant.fab` (orthogonalize after dequant, before adapter handoff; storage policy per §12-5; per-target digest computed at bake) | proba: baked f32 tensor pinned against a reference-implementation golden; requant path carries a declared band row; non-admitted GGML id on a target still fails closed (`packed.rs:122-130` pattern) |
| W5b-U3 runtime activation projection + Obliterate unification | gradus `forward` + LayerPlan (`ProjectActivation` at a site ≡ §5.2 `Obliterate { direction }` with α=1 at that block; duplicate-site entries across LayerPlan and AblationSpec rejected) | forward proba: projection pins at each site + duplicate-site negative green |
| W5b-U4 admission provenance + digest verification | gradus manifest/digest helpers (base-GGUF digest + AblationSpec digest + per-target baked-tensor digests; load verifies, mismatch fails closed); wave-6 manifest schema consumes the fields (§12-6) | negative test: tampered base file or tampered recipe digest → load rejected; digest helper unit pins |
| W5b-U5 acceptance rows + coverage oracle | gradus proba/docs extending NEED `e52dd09a` to layer-plan-modified execution (§13.4); one coverage probe expressing a published abliterated recipe as base+spec on a small dense rung (§13.5) | pinned effective-model band rows green; band receipt committed |

**Wave 6 — knob surface + perf harness** (admission manifest for §6.2 dials;
`faber run` flags parse-only fail-closed; benchmark protocol harness reporting
prefill/decode separately vs pinned llama.cpp). Done-when: one dense-rung
benchmark receipt exists comparing both engines on the same machine/model.

Ordering rationale: waves 1–2 unblock everything numeric (F16 is the KV default
format and the activation IO candidate); wave 3 is the biggest single perf
lever and the quantized-V enabler; wave 4 is the decode-throughput lever; waves
5–6 are surface and evidence. R-PACK-05 (full-model packed device run) remains
the campaign's own gate — waves 1–2 improve it; nothing here preempts it.

### 11. First-wave proposal

File **wave 1 (W1-U1…U4) + W2-U1** now: five micro-units, write-disjoint
(radix-mir abi/packed ×1, radix-mir-metal ×1, radix-mir-llvm ×1,
radix-mir-wgsl ×1, gradus cache ×1 — W1-U3 gradus dequant can run parallel
with W2-U1, different modules), no shared hot files with R-PACK-03/04 or
OF-3..5, each with fail-closed negatives and a first failing oracle. Estimated
~15–25k tokens total — the same envelope as the fusion wave-1 filing.

### 12. Open decisions routed to mind (with defaults)

1. **GI4 KV-dtype amendment** (§9): **settled 2026-08-18** — `KvCacheLayout.dtype`
   opened to `{F32, F16, Q8_0, Q4_K}`, F16 default (need `1d3967ed`). Cost:
   envelope derivations.
2. **Layer-sliced acceptance policy** (§5.2, §13.4): default = sliced runs carry their
   own recorded band (logit-band vs pinned sliced reference), never inheriting
   the GI0 exact-top-1 contract. NEED `e52dd09a` carries this; the §13 addendum
   recommends folding it to **layer-plan-modified execution** (slice OR ablation
   recipe) — one policy, one acceptance shape, effective model pinned as its own
   reference.
3. **Int8 activation dot (CPU regime)**: default = not admitted; revisit only
   if a CPU route becomes a product goal.
4. **Perf-harness ownership**: default = one faber-side benchmark unit (wave 6)
   using gradus `benchmark-method.md`; llama.cpp runs offline as comparator.
5. **Baked-tensor storage policy for quantized ablation targets** (§13.2):
   orthogonalizing a Q4_K/Q5_K/Q6_K/Q8_0 tensor means dequant → f32 transform →
   re-encode, which is a *declared* transformation, not as-stored loading
   (§6.2 row 1). Default = same-format re-encode (byte-parity of the model
   footprint, requant band recorded); explicit per-target F32/BF16 promotion is
   the override (bytes cost, tighter band). Never silent — the AblationSpec
   names the policy per entry.
6. **Admission-manifest recipe provenance** (§13.3, wave 6): add base-GGUF
   digest + AblationSpec digest + per-target baked-tensor digests to the
   admission manifest schema; load verification fails closed on mismatch.
   Default = adopt. This is what makes "base + recipe" a *checkable* claim
   rather than a hope — the manifest is derived, never an authority.

---

## 13. Addendum — Ablation layer (inline layer that modifies earlier layers)

**Status**: UNCOMMITTED DRAFT addendum to the design committed at `4004e32`
(mind routes the commit). Operator ask: an inline layer construct whose
semantics are a *transformation of earlier layers*, motivated by the
abliteration technique — refusal-direction orthogonalization of weights;
the HF "abliterated" corpus is pre-baked checkpoints of exactly this
(failspy/Llama-3-8B-Instruct-abliterated model card: "orthogonalized bfloat16
safetensors weights … the strongest refusal direction orthogonalized out";
Arditi et al., *Refusal in Language Models Is Mediated by a Single Direction*).
Section numbers §1–§12 refer to the committed doc; gradus/radix citations are
live main as of `012d411`/`8c5c6a3a8`.

### 13.0 Mind's hypothesis, validated with one correction

**Hypothesis**: the structural play is lowering-time baking — base GGUF +
ablation recipe → orthogonalized weights materialized at specialization, zero
runtime cost, no checkpoint fork; runtime projection is the other fork.

**Verdict: confirmed, with the two forks serving different *workflow roles*, not
just different delivery.** The published abliteration pipeline itself runs
inference-time direction projection first (a `direction_ablation_hook` on every
residual site, evaluated over candidate directions), then bakes the selected
direction into weights once (mlabonne, *Uncensor any LLM with abliteration*,
HF blog 2024 — the tutorial the huihui-ai cards cite). So:

- **Runtime projection is the authoring loop** — cheap to attach/detach per
  candidate direction, per site, per α; this is how directions are *searched*.
- **Baking is the product form** — zero runtime cost, and (unlike HF) we get it
  **without forking a checkpoint**: the recipe travels beside the base GGUF,
  the transform is applied once at weight materialization, and the effective
  tensors are ordinary tensors from the plan's point of view.

**Correction to carry**: the two forks are *not numerically equivalent* —
baked weight orthogonalization also removes the direction from the embedding
write and every writer's output rows, while runtime projection acts only at
its declared sites (Arditi et al. note intervention and orthogonalization as
distinct operators). They therefore need distinct acceptance rows under the
band policy (§13.4); one is not a drop-in approximation of the other.

### 13.1 Semantics and delivery

Delivery mode is **derived from transform type, not chosen** (no free knob,
§6.2 discipline):

| Transform | Delivery | Mechanism | Runtime cost |
| --- | --- | --- | --- |
| Weight orthogonalization (§13.2) | **bake** at materialization | applied once in the `fons` resolver seam — dequant → f32 transform → re-encode/promote → hand the adapter an ordinary stored-layout tensor (`dense.fab:125` `_source` seam; K-major load contract, design §1 item 2, unchanged — the transform is layout-blind, it happens in f32 after dequant) | **zero** — a downstream kernel/plan cannot distinguish a baked tensor from a native one; no new recipe variants (kernel_plan closed set HONORED, §9 row 1) |
| Activation projection (§13.2) | **runtime** at the entry's site | one fused elementwise projection `a ← a − α(a·d)d` per site per token — exactly the OF-1/OF-2 typed elementwise carrier §5.2 names for `Obliterate` | one elementwise op per site per step; D-length direction resident |
| Bias edit (§13.2) | **bake** (V1) | folded into the materialized bias; today's rows synthesize zero biases (`dense.fab:380-385` `_no_bias`), so bake = replace the zero with δ | **zero** |

Cost entries added to §7 (three rows after the LayerPlan row). Locks honored, none
amended by this addendum: storage authority (a baked tensor is a *declared*
transform with per-entry storage policy §12-5, never a silent requant);
EXEC-02 decision 4 (F32 promotion is per-tensor, bounded to the target set,
ledger-counted by the partition budget classes — not whole-model expansion);
GI4 `KvCacheLayout` untouched (§13.4).

### 13.2 V1 transformation set (typed admission, fail-closed each)

```text
AblationTransform =
  OrthogonalizeWeight { targets: [(layer, matrix)], direction: vec[D],
                        alpha: f32 ∈ (0,1], storage: SameFormat | Promote(F32|Bf16) }
      # matrix ∈ { OProj, DownProj, EmbedTokens } — the residual-stream writers
      # (Arditi set: attn.o_proj, mlp.down_proj, W_E). W ← W − α·d(dᵀW) in the
      # residual-side row space, computed in f32 after dequant.
  | EditBias { target: (layer, bias), delta: vec }      # bias ∈ {Q,K,V,Gate,Up,Down}
  | ProjectActivation { site: BlockOut(layer) | FinalPreNorm,
                        direction: vec[D], alpha ∈ (0,1] }
```

Fail-closed admission, each rule testable as a negative (W5b-U1):

- **`OrthogonalizeWeight`**: layer indices in bounds; `direction.length ==`
  target residual dim (`hidden_dim` for OProj/DownProj rows and embed rows);
  direction non-zero and normalized at admission (the normalized bytes are
  what the spec digest records — determinism); α in (0,1] (α=1 = full
  orthogonalization, α<1 = scaled/"projected" variant as in grimjim's
  projected abliteration); one transform per `(layer, matrix)` — re-targeting
  a transformed tensor fails closed, composition is expressed as one entry
  with pre-composed parameters; GGML storage id of the target must be in the
  admitted set (unknown id → reject, `packed.rs:122-130` pattern); `storage`
  policy mandatory on quantized targets (§12-5).
- **`EditBias`**: length must equal the projection width (`qwidth`/`kwidth`
  for Q/K/V per `dense.fab:368-371`, MLP width `f` per `dense.fab:375-379`);
  unknown bias name → reject.
- **`ProjectActivation`**: site in bounds; duplicate site across LayerPlan
  `Obliterate` and AblationSpec fails closed (they are the same construct —
  `Obliterate { d }` ≡ `ProjectActivation { BlockOut(l), d, α=1 }`; wave
  W5b-U3 unifies them rather than carrying two spellings).

Deliberately **not** in V1: rank-k subspace rejection (Heretic-style —
direction is a single vector; a `basis: mat` variant is a typed-admission
extension), norm-preserving/biprojected variants (transform fixed to the
subtractive projection), LoRA-style additive weight deltas (different family;
belongs to fine-tune-artifact loading if ever admitted). Named, not silent.

### 13.3 Representation and the reference discipline

**Where the spec lives — both, with one authority.** The `AblationSpec` is
authored **inline in Gradus model config**, beside the LayerPlan (§5.2): it is
semantic surface (it changes the computed function), so it belongs where the
LayerPlan lives, consumed by `forward` (interpreted: bake at first
materialization; runtime entries emit their projection at their site) and by
lowering (bake at specialization). The **model manifest** (wave 6 admission
manifest, §6.2) records *derived provenance*: base-GGUF digest + AblationSpec
digest + per-target baked-tensor digests, verified fail-closed at load
(§12-6). Authority split: the inline spec is the single authoring truth; the
manifest is a derived verification record — a manifest without a matching spec
digest is rejected, never silently trusted.

**Reference discipline for a sequential executor.** `forward` today is a
strict `while stratum ≺ cfg.layers` loop with per-layer canonical-name
resolution (`dense.fab:355-366`) — no layer sees another. The ablation entry
is the first *graph-level* construct, and the discipline that keeps sequential
execution sound is:

1. **Backward reference only** — every entry has a `position ∈ [0,
   cfg.layers]` and every named target layer satisfies `target < position`.
   This is the operator's definition made structural ("modifies *earlier*
   layers") and it is exactly what makes the runtime form well-ordered: by the
   time an entry's position executes, every target it names has executed.
2. **A bake entry emits nothing at its position** — it is a compile-time-only
   node; the transform has already happened at materialization. A runtime
   entry (`ProjectActivation`) emits its one projection at its position.
3. **No re-transformation** — a tensor may appear in exactly one transform
   entry (§13.2); ordered composition is rejected, not silently applied.
4. **Validation order** — the AblationSpec validates against the *resolved*
   LayerPlan (after Skip/SkipAttention resolution), not the authored one
   (§13.4).

This gives graph-level semantics without graph-level execution: the entry list
plus the backward rule is a DAG whose only crossing edges are
backward-in-position, so the sequential loop with materialization-time bakes
computes exactly the composed graph.

### 13.4 Interactions (LayerPlan, KV, acceptance band)

- **LayerPlan on the ablation entry itself**: `Skip`/`SkipAttention`/
  `Obliterate` are per-block modes; an AblationSpec entry is not a block, so
  those modes do not apply to it. A bake entry has no position-time behavior
  to skip; a `ProjectActivation` entry at position p with `Obliterate` on
  block p is a duplicate-site rejection (§13.2), not a composition.
- **LayerPlan on the targets** (validated against the *resolved* plan):
  - target block `Skip` → its weights never execute → the transform is dead →
    **admission fails closed** (config error: remove the entry or unskip).
  - target block `SkipAttention` → `OProj` is dead (reject `OProj` on it),
    `DownProj`/bias entries on the surviving MLP remain live (admitted).
  - `Obliterate { d₁ }` on a block that also receives `OrthogonalizeWeight {
    d₂ }`: legal in both orders d₁=d₂ (redundant — the writer already writes
    ⊥d, the projection is ≈identity; validator notes, does not reject) and
    d₁≠d₂ (both apply; baked transform first, runtime projection second —
    order is fixed by construction, §13.3).
- **KV structure**: every V1 transform preserves all `KVStructure` facts
  (§4.3) — head counts, head_dim, slots, dtypes are untouched; `EditBias` on
  K/V and any transform upstream change K/V *values*, never structure. No GI4
  amendment arises from this addendum; the §4 KV-dtype need is unrelated.
- **Acceptance band — fold into NEED `e52dd09a`**: that need already proposes
  "sliced runs carry their own recorded band, never inheriting GI0". The
  addendum recommends renaming its scope to **layer-plan-modified execution**
  (LayerPlan slice OR ablation recipe) with one acceptance shape: the
  *effective model* (base + LayerPlan + AblationSpec, identified by the
  manifest digests of §12-6) is pinned as its own reference and carries a
  recorded band; identity mode (all-Normal + empty AblationSpec) remains
  GI0-exact, byte-identical to base-as-stored. Two forks, two bands (§13.0
  correction): baked runs are compared against the pinned effective model;
  runtime-projection runs carry their own band rows. Where a published
  abliterated checkpoint exists for the same base, it is *also* an admissible
  comparator oracle (§13.5) — band, not exact, because their baking pipeline
  ran on BF16/F16 sources and ours on the GGUF-as-stored.

### 13.5 Coverage — the HF abliterated corpus as base + recipe

**Construct coverage: full for the refusal-direction family.** The entire
published technique is `OrthogonalizeWeight` entries with α=1 plus (optionally)
runtime probes during direction search:

1. **`failspy/Llama-3-8B-Instruct-abliterated`** (card read 2026-08-18): base
   `meta-llama/Llama-3-8B-Instruct`, "orthogonalized bfloat16 safetensor
   weights" per Arditi et al., generated by `ortho_cookbook.ipynb`; GGUF quants
   published separately. The notebook's bake step orthogonalizes the embedding
   and every block's `o_proj` + `down_proj` — i.e. **one `AblationSpec` with
   1 + 2·L `OrthogonalizeWeight` entries (α=1, matrices `EmbedTokens` +
   per-layer `OProj`/`DownProj`)** against the *original* Llama-3-8B-Instruct
   GGUF. Expressed exactly; zero runtime cost; no 8B checkpoint fork.
2. **`huihui-ai/Qwen2.5-7B-Instruct-abliterated-v2`** (card read 2026-08-18):
   card credits FailSpy for "original code and technique" and cites the
   mlabonne article; "-v2" is an "improvement over the previous one" — the
   family's refinements are subset/scaled applications (fewer matrices, α<1)
   of the same transform, which the per-entry α and per-matrix targeting of
   §13.2 covers directly. Maps as base `Qwen/Qwen2.5-7B-Instruct` GGUF +
   spec; the direction must be re-mined (below).

**Bit-exact reproduction honestly bounded**: the cards publish *checkpoints*,
not *recipes* — neither the direction vector nor the prompt sets are part of
the artifact. Reproduction therefore re-derives the direction externally
(diff-in-means over harmful/harmless activations, last-token position, per
Arditi/mlabonne — mining runs on Gradus's runtime projection mode with
activation capture, or out-of-tree exactly as the HF authors' notebooks do)
and lands **within a recorded band** of the published checkpoint's behavior,
never claimed equal. Tensor-space verification is stronger than logit-space
where sources align: if we bake from a BF16/F16 GGUF of the same base and
possess the direction, baked tensors compare elementwise against the published
safetensors up to the declared storage policy (§12-5) — that comparison is a
W5b-U5 coverage-oracle row, not a guarantee.

**Not covered by V1** (named, §13.2): Heretic-style rank-k subspace rejection,
norm-preserving biprojection, DPO-"healed" variants (`mlabonne/
NeuralDaredevil-8B-abliterated` is abliteration *plus* a DPO fine-tune — the
fine-tune half is not a recipe over the base and is out of scope by
construction).

---

*Addendum ends. §1–§12 are the committed design (`4004e32`); this section is
the uncommitted draft layer. Amendment needs §12-5/§12-6 and the NEED
`e52dd09a` fold are filed to mind with this report.*

---

## 14. Addendum 2 — the inverse census: what llama.cpp structurally cannot express

**Status**: DRAFT (uncommitted; mind routes the commit)
**Author**: head-cto (Vivi handle `cbea0c29`), 2026-08-18
**Ask**: operator — a systematic census of tuning knobs/concepts that are
**structurally impossible** in llama.cpp but natural here. This systematizes
§8.2's six one-off bullets into a ranked census and extends it with four new
items (I5–I7, I9). §13 (ablation layer, sibling seat `c7174a33`) is left
untouched; I5's LayerPlan item cross-references it rather than restating.
**Evidence pins**: `~/work/llama.cpp` @ `c8e03ce81` (same pin as §1; every
line below re-verified today), gradus @ `012d411` + design commit `4004e32`
+ uncommitted addenda (§13, §14), radix main and hosts partition contract
(citations re-verified 2026-08-18).

### 14.1 The five blockers, re-verified at file:line

Every "impossible" claim below reduces to one of five structural facts. Each
is architectural — a property of what the shipped artifact *is*, not a TODO:

| # | Blocker | Evidence (`~/work/llama.cpp`) |
| --- | --- | --- |
| B1 | **The kernel set is a build artifact.** Kernels are static function-pointer tables and precompiled pipelines inside libggml; the model does not exist when the binary is built, and no runtime codegen path exists anywhere in the tree (device "compilation" is pipeline instantiation from a fixed embedded library). | traits `ggml/src/ggml.c:631`; static CPU kernel table `ggml/src/ggml-cpu/ggml-cpu.c:214`; runtime op dispatch `ggml-cpu.c:1836,2330`; CUDA *selection among* prebuilt families by heuristic `ggml/src/ggml-cuda/ggml-cuda.cu:1783-1809`; Metal pipelines from fixed embedded source `ggml/src/ggml-metal/ggml-metal-device.m:415`, runtime mul_mat dispatch `ggml-metal/ggml-metal-ops.cpp:360-364` |
| B2 | **The checkpoint carries data, never code.** GGUF is tensors + hparams; the model *program* is a per-arch C++ subclass compiled into the binary. Unknown type ids and unknown arches fail at load. | per-arch pure-virtual builder `src/llama-model.h:697,749`; unknown tensor type hard-fails `ggml/src/gguf.cpp:705-707`; arch names are a closed compile-time map `src/llama-arch.cpp:8` |
| B3 | **No compiler in the loop.** The graph is built at runtime by hand-written C++ builders; "specialization" is graph *reuse* keyed on topology, never code emission. | builders `src/llama-graph.cpp:1480+`; reuse contract "full topology has to be uniquely determined by these parameters" `src/llama-context.cpp:1332-1335` |
| B4 | **Topology and policy are runtime cparams over a fixed builder.** | flash-attn branch at graph build `src/llama-graph.cpp:37`; placement heuristic `src/llama-model.cpp:1318-1333`; batch knobs `common/common.h:443-444` |
| B5 | **CPU execution is one generic thread pool.** Work partition is runtime chunking, not per-op/per-shape constants. | pool `ggml-cpu.c:480-514`, barrier `:575` |

**Class rule**: an item is `IMPOSSIBLE` only if expressing it requires
changing B1–B5 (a new engine artifact), not merely writing more code inside
the existing shape. Items llama.cpp could converge on with effort are
`NEAR-MISS` (§14.4).

### 14.2 Census, ranked by value-per-cost

| # | Knob / concept | Class | Blocked by | What it buys | Our seam | Cost | vs wave plan |
| --- | --- | --- | --- | --- | --- | --- | --- |
| I1 | Whole-graph typed elementwise fusion | IMPOSSIBLE | B1+B3 | kills bandwidth-bound intermediate round-trips systematically | OF plans | S (mostly paid) | rides OF-3..5 (behind R-PACK-05) |
| I2 | Per-specialization kernel codegen (constants burned in; regime depth; work partition) | IMPOSSIBLE | B1 (+B5) | constant-folded dequant, baked GQA/head_dim/rope, per-shape tiles, per-regime bodies | kernel_plan + device programs | M | wave 4 is the first rider |
| I3 | Authored per-layer-set KV structure | IMPOSSIBLE | B2+B4 | SWA memory bounds, per-layer-set KV dtype/layout mixes, fail-closed bundles | `KVStructure` (wave 2) | M | wave 2 filed |
| I4 | Semantic layer surgery (LayerPlan + ablation recipes) | IMPOSSIBLE | B2+B4 | verified skip/streamline/obliterate/ablate with per-mode acceptance | LayerPlan (§5) + §13 AblationSpec | S–M | waves 5 + 5b filed |
| I5 | Model-as-program architecture admission | IMPOSSIBLE | B2 | new/mutated architectures as source, stock runtime | gradus adapters + reserved recipes | L per family | new; W7-U3 parked |
| I6 | Plan-layer format extension (runtime contract never moves) | IMPOSSIBLE | B1+B2 | new storage formats without a runtime release; model-carried recipes possible | abi/packed plans + host ABI | S–M per format | new; W7-U4 parked behind OD |
| I7 | Plan-fact admission budgeting (byte-exact, frozen) | IMPOSSIBLE (facts) / near-miss (ledger mechanics) | B1 | per-emitted-kernel workspace/scratch facts → admission as proof | partition ledger (exists) | S | enabler; waves 2–6 consume |
| I8 | Guaranteed-inline device fragments, compiler-enforced | IMPOSSIBLE (guarantee) | B1 | one dequant/unpack body spliced into every emitted kernel | NucleumRole Fragment | S–M | fragments goal, landing |
| I9 | Per-specialization derived numeric envelopes | IMPOSSIBLE (derivative) | B1 (no specialization axis ⇒ no per-specialization contract) | every emitted specialization carries a machine-checked band | numeric policy + ORACLE | S–M | per-wave envelope derivations |

### 14.3 Dossiers

**I1 — Whole-graph typed elementwise fusion.** (a) ggml ops are opaque
precompiled entries; a *general* fusion pass would need kernel source to
recombine at or before runtime, and none exists (B1: traits at
`ggml.c:631`; CUDA fusion is hand-enumerated at specific sites —
`ggml-cuda.cu:3480-3642` GLU+MMVQ, `fattn.cu` — each a bespoke C++/CUDA
artifact; B3: the graph has no IR between builder and kernel table). (b)
removes whole classes of global-memory round-trips on bandwidth-bound
elementwise chains (norm/rope/residual/activation); fusion decisions are
typed and checked, not heuristic. (c) `radix/crates/radix-mir/src/elementwise_plan.rs:1-10`
(typed plan; never a silent `Elementwise` fallback). (d) S — OF-1/OF-2
landed; remaining cost is OF-3..5 emitter migration, already scheduled
behind R-PACK-05. (e) rank 1: highest value-per-cost because the seam is
paid; strictly beyond llama.cpp by construction.

**I2 — Per-specialization kernel codegen.** (a) the kernel set is compiled
before any model exists (B1: static tables `ggml-cpu.c:214`, precompiled
pipelines `ggml-metal-device.m:415`); runtime "specialization" is selection
among 2–3 prebuilt families by heuristic (`ggml-cuda.cu:1783-1809`), and
work partition is generic runtime chunking (B5: `ggml-cpu.c:480-514,575`).
llama.cpp *cannot* burn per-model constants — the code does not exist to
burn them into. (b) constant-folded block geometry, unrolled dequant, baked
GQA ratio/head_dim/rope policy, per-shape-class tiles, per-regime bodies
(GEMV-shaped decode vs GEMM prefill), per-shape work-partition constants —
each removes runtime branches and improves register/occupancy choices. (c)
plan constants are named precisely so backends never hardcode
(`radix/crates/radix-mir/src/kernel_plan/plan.rs:12-24`); closed recipe set
with explicit reviewable additions (`plan.rs:44-50`); emitted artifacts are
device programs (`radix/crates/radix-mir/src/device_program/program.rs:16-22`).
(d) M — the recipe families are the cost; wave 4 (decode regime) is the
first rider. (e) rank 2: the mechanism every later perf knob multiplies.

**I3 — Authored per-layer-set KV structure.** (a) cache classes are C++
types selected per architecture at admission
(`src/llama-model.cpp:2057-2300` `create_memory` switch; §4.2); a
user-authored mix (per-layer-set dtype, custom windows, mixed dense/SWA in
one model) means writing a new C++ cache class + builder — checkpoint
carries no code (B2) and the builder is fixed (B4). (b) SWA bounds KV bytes
by window; per-layer-set KV dtype halves-or-quarters the decode-bandwidth
stream where it matters; infeasible bundles rejected at plan validation.
(c) `KVStructure` design §4.3 on `gradus/src/cache.fab:20-45` (semantic
contract already proven as the mutation-rule surface). (d) M. (e) rank 3:
wave 2 already filed; biggest long-context lever after flash attention.

**I4 — Semantic layer surgery.** (a) llama.cpp's graph builders hardcode
the layer loop; its layer *filters* are memory-structure facts wired in C++
(`llama-model.cpp:2080-2121` MSA/MTP), not an authoring surface — skip,
streamline, obliterate, or ablate requires patching the engine (B2+B4).
(b) drops whole GEMM families (gain ∝ removed FLOPs/bandwidth) and enables
model-editing as a *verified* capability with per-mode acceptance. (c)
LayerPlan §5.2 + the §13 AblationSpec (bake/projection) — this census adds
nothing; it confirms the class and notes both spellings are already
unified by W5b-U3. (d) S–M. (e) rank 4: waves 5 + 5b carry it.

**I5 — Model-as-program architecture admission.** (a) each architecture is
a C++ subclass with a pure-virtual graph builder
(`src/llama-model.h:697,749`); the arch string must exist in a closed
compile-time map (`src/llama-arch.cpp:8`). A new or mutated architecture
(new attention family, MoE routing variant, SSM hybrid, custom rope) cannot
be expressed by any artifact a user ships — only by an engine release or
fork (B2). (b) capability, not perf: run models upstream does not know,
with zero upstream latency, on a stock runtime; adapter source is public
Faber, not engine C++. (c) gradus adapters (`gradus/src/model/dense.fab`
is the pattern) + reserved recipes `GroupedMatMul`/`SsmConv1d`/`SsmScan`
(`kernel_plan/plan.rs:105-112`, admission pending R-PACK-03/04 — honest:
the MoE/SSM arms are reserved, not landed); host ABI unchanged
(`radix/crates/radix-host-abi/src/lib.rs:1-28`). (d) L per family.
(e) rank 5: highest strategic value, highest unit cost — park as
campaign-level (W7-U3), do not inline into waves 1–6.

**I6 — Plan-layer format extension.** (a) format knowledge is compiled into
the runtime: traits frozen in the binary (`ggml.c:631`), the loader
hard-fails unknown tensor types (`gguf.cpp:705-707`) — an old llama.cpp
binary cannot run a model in a newer quant format at all; formats are added
by libggml releases (MXFP4/NVFP4 rows in `ggml-cpu.c:214` are the release
artifact of that process). For us the dequant lives in *lowering*: a new
format is a plan admission (explicit reviewable change, fail-closed set
`kernel_plan/packed.rs:122-130`) plus emitted per-model kernels, and the
runtime contract (`__faber_rt_v1_*`) never moves. Because kernels are
admitted artifacts (partition class 4 budgets module/kernel storage,
`hosts/crates/host-coordinator/src/partition.rs:104-106`), model-carried
dequant recipes are *structurally possible* here and impossible there (B1+B2).
(b) ecosystem capability: formats (including private/3P encodings and
per-model repack layouts) deploy with the model package, not the engine.
(c) `radix/crates/radix-mir/src/abi/contract.rs:162-192` + `packed.rs`
+ host ABI. (d) S–M per format (R-PACK-02 pattern). (e) rank 6; the
model-carried variant is gated on OD §12-7 below — today recipes remain a
closed reviewed set (correctly).

**I7 — Plan-fact admission budgeting.** (a) honest split: a *budget check*
is bookkeeping llama.cpp could add (near-miss); what it cannot produce is
**per-emitted-kernel facts** — workspace, scratch, occupancy, launch shape —
because no kernel exists until ours are emitted per specialization (B1).
Their scheduler estimates from tensor shapes at runtime; our ledger
consumes plan facts and is **frozen at admission** with all eight byte
classes (`partition.rs:90-125`, incl. KV bytes consumed-not-rederived).
(b) admission becomes a proof (the workload fits, immutably) instead of a
best-effort placement (`llama-model.cpp:1318-1333` is exactly that
heuristic); this is the serving/SLA enabler. (c) exists; waves 2–6 feed it
finer facts. (d) S. (e) rank 7: enabler, already paid.

**I8 — Guaranteed-inline fragments.** (a) C++ sharing across the kernel
zoo is convention (macros/headers); there is no compiler-enforced inline
guarantee, and a helper cannot be spliced into an already-compiled
CUDA/Metal kernel at all (B1). (b) one dequant/unpack body reused across
every emitted kernel family (MMQ-like, MMVQ-like, fattn-like as waves land)
— dedup + uniform numeric behavior. (c) `NucleumRole { Entry, Fragment }`
(`radix/crates/radix-hir/src/nodes.rs:288-296`) + device-safe effect-subset
check (commit `1adda171c`); operator ruling honored: inline guarantee, not
a perf claim. (d) S–M, landing. (e) rank 8: pays out as waves 3–4 multiply
kernel families.

**I9 — Per-specialization derived numeric envelopes.** (a) derivative
impossibility: with no specialization axis there is nothing to attach a
per-specialization contract *to*; their accuracy posture is ad-hoc checks
in kernel code. Ours: every emitted specialization (format, KV dtype,
fusion shape) carries a derived band, never an inherited one (precedent:
the Q2 envelope is SmolLM2-only — `exec02-…-delivery.md:75`). (b) makes the
knob space §6.2 *safe to turn*: any dial change has a machine-checked
acceptance row. (c) `gradus/docs/numeric-tolerances.md:28-36` + ORACLE
harness + wave envelope derivations. (d) S–M ongoing. (e) rank 9.

### 14.4 Near-miss flags (merely-not-built, high value)

Strictly outside the operator's asked class, flagged because value is high
and the block for llama.cpp is effort, not structure:

- **N1 — Emit-time autotuning.** Ours: search plan constants per shape
  class at lowering, pin results (receipts, no runtime JIT — keeps the
  closed-set discipline). Theirs: approximable by shipping a grid of
  prebuilt variants + profile-driven selection (they already select among
  MMQ/MMVQ heuristically, `ggml-cuda.cu:1783-1809`); the *unbounded
  per-model space* stays ours (I2), the tuning loop does not.
- **N2 — Static vocab-subset lm_head / whole-program DCE.** llama.cpp
  builders always emit the full-vocab head; a graph pruning pass is addable
  upstream (graph-level utilities exist and are growing — `ggml.c:7203`
  `ggml_build_forward_order` landed in the pinned tip commit). For us it is
  a lowering-time N-specialization (exact on the subset, identity on full).
- **N3 — Speculative decoding as authored composition.** theirs is one
  fixed C++ implementation; a typed draft+target composition with shared
  fragments and its own acceptance band is natural here but not impossible
  there. Park until serving goals.
- **N4 — Backend addition.** theirs is possible via dynamic loading
  (`ggml/src/ggml-backend-dl.cpp`) but fork-grade C++; ours is a lowering
  target switch, fail-closed (`radix/crates/faber/src/cli/mod.rs:359-391`).

### 14.5 Wave-plan row additions (proposed; §10 not edited by this addendum)

Splices after wave 6 (and after the sibling's W5b rows) at commit time.
Nothing here preempts R-PACK-05 or renumbers waves 1–6.

| Unit | Repo/scope | Done-when |
| --- | --- | --- |
| W7-U1 static vocab-subset lm_head (N2) | gradus `dense.fab` head tail + radix lowering N-specialization | proba: subset rungs exact on subset + identity vs full head; receipt shows FLOP/byte delta on a dense rung |
| W7-U2 emit-time tile/workgroup autotune receipts (N1, I2 rider) | radix plan-constant selection per shape class + per-device limit channel (already anticipated by `plan.rs:4-8`); offline search, committed receipts | one dense-rung decode receipt where the searched constants beat the defaults; no runtime search path exists in code |
| W7-U3 arch-adapter exemplar (I5) — **parked, campaign-level** | gradus second-architecture adapter riding reserved `GroupedMatMul`/`Ssm*` recipes (admission gated on R-PACK-03/04) | a non-llama-family architecture runs end-to-end from source on a stock runtime; no host-ABI change |
| W7-U4 model-carried recipe packaging probe (I6) — **parked behind OD §12-7** | packaging/lowering probe only | decision receipt; no format ships out-of-band before the trust policy is settled |

### 14.6 Amendment and open-decision needs

**No §9 lock is amended by this census.** Waves 1–6 and all W7 rows are
additive; W7-U2 mutates plan constants only through the existing
explicit-reviewable-change door (`plan.rs:44-50`).

Proposed additions to §12 (numbered to follow the sibling's §12-5/§12-6):

7. **Model-carried device code trust policy** (I6/W7-U4): default = recipes
   stay a closed reviewed set lowered from Faber source; model packages
   carry source + plan recipes + digests (§12-6 pattern), never prebuilt
   device binaries. Revisit only when a format must ship out-of-band.
8. **Autotune governance** (N1/W7-U2): default = offline search at
   lowering, committed receipts, fail-closed on missing receipts; runtime
   never searches or JITs (keeps the closed-set discipline and the
   deterministic-execution posture).

---

*Addendum 2 ends. §13 is the sibling seat's uncommitted addendum
(`c7174a33`) — untouched. This section is head-cto `cbea0c29`'s only
working-tree edit; mind routes the commit.*

---

## 15. Addendum 3 — Metal-targeted inference optimization census (finetune-for-inference)

**Status**: DRAFT (uncommitted; mind routes the commit)
**Author**: head-cto (Vivi handle `1f58bbbc`), 2026-08-18
**Ask**: operator — Metal-targeted optimizations, expressible as
knobs/recipes/lowering-time specializations, that improve **inference** —
motivated by operator-reported Qwen-3.8 numbers (~20 tok/s default →
70–100 tok/s in undisclosed closed fine-tuning trials). The numbers are an
**existence proof of a 3.5–5× gain class, not a spec**. This addendum
enumerates what could compose into that class. §13 (`c7174a33`) and §14
(`cbea0c29`) are untouched; this section cross-references both rather than
restating.
**Evidence pins**: gradus @ `012d411` + design `4004e32` + uncommitted
addenda; radix main (radix-mir-metal emitter read at the working tree);
hosts macos-arm64 read at the working tree; `~/work/llama.cpp` @
`c8e03ce81` (same pin as §1/§14). External sources read 2026-08-18, named
per claim. **No perf number below is our measurement** — wave-6 harness is
the arbiter (§8.3 discipline).

### 15.0 Framing: how a 3.5–5× decode class composes (and what it cannot be)

Decode is weight+KV bandwidth-bound (§7 roofline). No *single* published
knob in the census below yields 3.5–5× on the same model+hardware; the
class composes multiplicatively from independent factors:

1. **Speculative decoding: 2–3× published, output-identical** — Leviathan,
   Kalman & Matias, *Fast Inference from Transformers via Speculative
   Decoding* (arXiv:2211.17192, ICML 2023): 2–3× on T5-XXL with a small
   draft model, exactly matching the target distribution. This is the only
   *published* ≥2× inference lever that requires a **trained artifact**
   (the draft model) — the most likely single ingredient of an undisclosed
   "fine-tuning trial" that triples tok/s.
2. **Bandwidth/stream class: ~1.2–2× mechanism-only** — KV F16 (÷2 KV
   bytes), Q8_0 KV (÷4 vs f32, published ≈f16 speed when fused — see
   M2), plus launch/tile/simdgroup efficiency (M9–M10). Individual factors
   are modest; their product on a bandwidth-bound step is not.
3. **Baseline pathology removal** — a "default ~20 tok/s" on Apple silicon
   is often an *unbatched or per-launch-synchronized* configuration, not
   the hardware's ceiling (M10 documents our equivalent hazard: one
   command buffer + blocking wait per kernel today). A trial that merely
   fixes launch discipline can look like a fine-tune win.

Honest conclusion: treat 70–100 tok/s as achievable **composition**
(speculative × bandwidth × launch efficiency), with §15.3 as the reason
our stack can carry the trained half of that composition as a *loadable
artifact* rather than a runtime capability.

**Competitor frame (web-verified 2026-08-18).** MLX is the local
competitor: lazy evaluation with runtime graph scheduling, arrays in
unified memory, a **fixed precompiled kernel zoo dispatched at runtime by
shape/dtype** (stream/encoder-level dispatch; JIT compile + cache for
custom kernels; `mx.compile` traces a Python function and fuses
elementwise/reduction chains — ml-explore.github.io `usage/lazy_evaluation`,
`usage/unified_memory`, `dev/custom_metal_kernels`). Its attention kernel
adapts block sizes by context length at **runtime** (MLX 0.22-era
refactor; community M5-Ultra comparisons vs llama.cpp Metal FA2 show MLX
matching/beating MFA2 at long-context prefill). So the MLX contrast is
*not* "they lack knobs" — it is: MLX specializes a framework-owned kernel
zoo plus runtime dispatch and graph-level JIT fusion; **we specialize the
emitted kernel set per model+config at lowering time**, with declared
grid/block facts, fail-closed bundles, and recipes that carry semantics
(not just shapes). llama.cpp's position is strictly weaker (§14 B1–B5).

### 15.1 Census (M1–M11), seam-mapped

| # | Lever | Class | Seam | Cost | Gain class (evidence) |
| --- | --- | --- | --- | --- | --- |
| M1 | Flash-attention Metal path | lowering specialization | new recipe variant (wave 3) + Metal body | M | long-ctx prefill workspace + decode; enabler of M2's Q-KV. Published: MLX PR #735 (Mar 2024) fused inference SDPA, GQA-native + 4× KV compression, up to ~2.5× tok/s Mistral-7B @ ~8k ctx on M3 Max |
| M2 | KV dtype slimming (F16 / Q8_0 / Q4_K) | knob (KVStructure) | `KVStructure` + GI4 dtype amendment (§9, filed) | S–M | footprint first, speed second: published q8_0 ≈ f16 within ~5%, ~2× KV memory vs f16; q4_0 **can be slower** without fused in-attention dequant (DGX-Spark 128k-ctx benchmark: 92% slower pp @64k) — the lever is real only as a bundle with M1 |
| M3 | Batch/ubatch geometry | admission knob | session admission + partition ledger workspace class (`partition.rs:90-125`) | S | prefill compute-bound fill; decode batch>1 only matters with M7; llama.cpp defaults 2048/512 (`common.h:443-444`) are the parity reference |
| M4 | Threadgroup/tile per shape class | lowering specialization | plan constants (`plan.rs:4-24`) + per-device limit channel + W7-U2 receipts | S–M | prefill arithmetic intensity; mechanism (llama.cpp CUDA MMQ tiles ≫ 8×8); our constants are named precisely so this is a plan fact, not a rewrite |
| M5 | Dequant-in-register | lowering specialization (mostly paid) | R-PACK-02 bodies + fragments (§14 I8) | S | in-kernel dequant is landed posture (EXEC-02 §2); extension = keep the dequantized tile in registers across K-tiles, never staging f32 globally; wave 4's GEMV family is the rider |
| M6 | Fused rope+attention+residual chains | lowering specialization | OF-3..5 emitter migration (locked behind R-PACK-05) + M1 | M | kills bandwidth-bound round-trips (I1 mechanism) — RoPE into attention Q/K load, residual add into the attention epilogue; fusion boundary ruling honored (compiler-internal only) |
| M7 | Speculative/draft decoding | authored composition (§14 N3) | draft model as loadable (§15.3) + batched decode (wave 4) + band rows | M–L | **published 2–3×, output-identical** (Leviathan ICML 2023); llama.cpp ships draft/MTP/Eagle3 (`common/arg.h:172,323-331,372`, `n_max=3` default) — parity requires the *composition* be expressible, which §15.3 supplies |
| M8 | Prompt-cache reuse | session capability | `DeviceBufferLifetime::PerProgram` + EXEC-03 persistent sessions + KVStructure `slots` | S–M | eliminates re-prefill for repeated prefixes entirely (mechanism; whole prefill cost removed) — serving-shaped, not single-shot |
| M9 | simdgroup matrix ops + Apple-friendly layouts | lowering specialization | Metal arm of TiledMatMul/QuantizedMatMul behind plan constants + device-family gate | M | Apple GPU Family 7+ (M1+) has official `simdgroup_matrix<T,8,8>` + `simdgroup_multiply_accumulate` (MSL spec); our 8×8 tile constant matches the 8×8 hardware fragment exactly; prefill compute-bound gain (community GEMM work reaches MPS-class throughput with these; undocumented async-copy instructions exist but stay out of scope — risk named below) |
| M10 | Buffer-pool/residency + per-step command-buffer batching | host-session policy | descriptor launch sequence + `data_flow`/`roots` + lifetime classes; `metal_host.rs` | S–M | **launch/sync overhead elimination**: today every kernel = one command buffer + blocking `wait_until_completed` (`metal_host.rs:996-1027`); a decode step is L layers × several kernels of serialized round-trips; mechanism-only (no published number), highest value-per-cost candidate |
| M11 | Power/thermal-aware scheduling | admission/cadence policy | session admission + descriptor lifetime facts | S | mechanism-only, no published per-knob evidence: Apple silicon sustained-clock behavior means decode cadence and prefill-burst placement affect sustained tok/s; parked until measurement exists |

### 15.2 Dossiers (per lever: mechanism / why ours / seam / cost / gain)

**M1 — Flash-attention Metal path.** Mechanism: tiled online-softmax
attention — Q·Kᵀ, softmax, ·V computed in K/V tiles held in threadgroup
memory, never materializing the T×n_kv score matrix (today:
`CausalMaskedSoftmax` materializes scores, §4.1). Why ours: the recipe set
is closed and reviewable (`plan.rs:44-50`) — flash attention lands as an
explicit variant carrying the *bundle* facts (KV dtype, v_layout, head
dims, window), validated fail-closed at plan time (§4.3), then **baked per
model** with GQA ratio and head_dim as constants — vs MLX's one shared
kernel dispatched by shape at runtime, and llama.cpp's prebuilt pipelines
(§14 B1). Evidence: MLX PR #735 (Feb–Mar 2024, bpkeene) measured up to
~2.5× tok/s (Mistral-7B, ~8k ctx, M3 Max), largely from GQA-native
storage + KV compression + fusion — i.e. the *bundle*, exactly the shape
of our wave-3 recipe. Seam: wave 3 (already planned); Metal arm uses M9's
simdgroup path. Cost: M. Gain class: long-context decode bandwidth +
prefill workspace; prerequisite for M2's aggressive arms.

**M2 — KV dtype slimming.** Mechanism: KV is a pure read stream during
decode; halving/quartering its bytes cuts that stream directly and shrinks
footprint (longer context fits). Why ours: `kv_dtype_k/v` is a typed
`KVStructure` fact (§4.3) lowered into the attention bundle, not a runtime
`-ctk/-ctv` flag; the GI4 amendment is already filed (§9). Evidence
discipline (this is where naive expectations die): published benchmarks
(DGX-Spark, Nemotron-30B, 128k ctx, read 2026-08-18) put q8_0 within ~5%
of f16 speed with ~2× memory saving, while q4_0 was 92% slower at 64k pp /
35% slower generation — dequant *outside* the attention kernel eats the
win. Therefore: **KV quantization is admitted only as a bundle with the
M1 fused-dequant arm** (fail-closed combination, exactly §4.3's rule).
Seam: waves 2–4 + M1. Cost: S–M. Gain: footprint/context headroom first;
speed only in the fused bundle.

**M3 — Batch/ubatch geometry.** Mechanism: prefill is compute-bound —
ubatch sizes how much work fills the device before workspace spills
(ledger class 3, `partition.rs`). Decode batch>1 exists only for M7's
verification passes and continuous batching (serving). Why ours: sizes are
**admission facts** selecting between regime-specialized executables
(workload modes frozen `Prefill | ScalarDecode`, `gi4-contract.md:111-123`)
— no kernel-code branch, vs llama.cpp's runtime cparams and MLX's runtime
scheduler. Seam: wave-6 admission manifest. Cost: S. Gain: mechanism
(llama.cpp parity defaults); measured by wave-6 harness.

**M4 — Threadgroup/tile per shape class.** Mechanism: 8×8 scalar tiles
today (`MATMUL_TILE`, `plan.rs:12-17`); 32 KiB threadgroup budget is a
*conservative* portability constant (`plan.rs:4-8` — the comment already
anticipates the per-device limit channel). Why ours: tiles are **plan
constants per shape class**, searchable at lowering with committed
receipts (W7-U2), vs MLX's framework-build-time tuning + runtime adaptive
block sizes, and llama.cpp's fixed per-family tiles. Seam: plan constants
+ device limits channel; W7-U2. Cost: S–M. Gain: prefill
compute-boundness (mechanism); no number claimed.

**M5 — Dequant-in-register.** Mechanism: EXEC-02's locked posture is
already in-kernel block-wise dequant (§9 row 2) with landed bodies
(`quantized_matmul.rs:3,87`); the *residual* cost is f32 staging through
threadgroup tiles with two barriers per K-tile
(`quantized_matmul.rs:119-121,166-174`). Lever: dequant once into
registers/simdgroup fragments (M9) and keep the accumulator there across
the whole K loop; shared dequant body = fragment (§14 I8, inline
guarantee). Why ours: the body is *emitted per model* — block geometry is
a plan constant folded in — vs llama.cpp's MMVQ family (runtime-selected)
and MLX's precompiled kernels. Seam: M9 + wave 4. Cost: S (posture paid;
body work rides M9). Gain: bandwidth + ALU efficiency on both regimes;
mechanism.

**M6 — Fused rope+attention+residual chains.** Mechanism: RoPE, residual
adds, and normalization around attention are bandwidth-bound elementwise
chains; OF-1/OF-2 typed fusion is landed for elementwise, and M1's
attention arm can absorb RoPE into its Q/K loads and the residual add into
its epilogue. Why ours: typed fusion plans with no runtime fusion checks
(§6.1), honoring the operator boundary (compiler-internal only, §9);
llama.cpp hand-fuses at fixed sites (fattn.cu), MLX fuses at graph level
via `mx.compile`. Seam: OF-3..5 (locked behind R-PACK-05 — M6 does not
jump the queue) + wave 3. Cost: M. Gain: removes whole classes of global
round-trips per step (mechanism; I1's general case applied to the
attention neighborhood).

**M7 — Speculative/draft decoding.** Mechanism: a small draft model
proposes γ tokens; the target verifies all γ in **one batched forward**
and accepts the longest consistent prefix; rejection sampling keeps the
output distribution exactly the target's. Published: 2–3× (arXiv:2211.17192,
ICML 2023, T5-XXL/T5-small; identical outputs). llama.cpp ships it
(draft/MTP/Eagle3, `common/arg.h:172,323-331,372`); MLX-lm has it
(mlx-lm speculative generation, 2024+). Why ours: the draft model, its
tokenizer/linkage, γ, and the acceptance loop are **an authored
composition** with its own acceptance band (§14 N3) — not a hidden runtime
mode; and the draft itself is a trained artifact our loading machinery can
carry first-class (§15.3). Prereqs: batched decode path (wave 4), M10
batching (verification passes must not pay per-launch round-trips). Cost:
M–L. Gain: the only *published* 2–3×; acceptance-rate-dependent.

**M8 — Prompt-cache reuse.** Mechanism: KV for a fixed prefix is computed
once and reused across invocations (session save/restore; branch forks).
Why ours: `DeviceBufferLifetime::PerProgram` +
`ObservationPoint`/`PerStep` lifetimes are *declared descriptor facts*
(`device_descriptor.rs:142-149`) and KV structure is typed — a restore is
a buffer-version fact, not a heuristic; llama.cpp has session
save/restore; MLX caches lazily but with no declared provenance. Seam:
EXEC-03 persistent sessions (pending, correctly sequenced §8.1-4) +
`slots`. Cost: S–M. Gain: eliminates re-prefill entirely for repeated
prefixes (mechanism — whole prefill cost removed); serving-shaped.

**M9 — simdgroup matrix ops + Apple-friendly layouts.** Mechanism: Apple
GPUs (Family 7+, i.e. M1/A14 onward) expose official
`simdgroup_matrix<T,8,8>` with `simdgroup_load/store` and
`simdgroup_multiply_accumulate` (Metal Shading Language Specification) —
the hardware's matrix path; our `MATMUL_TILE = 8` matches the 8×8 hardware
fragment with zero re-tiling. Live gap: the emitter today emits **scalar
threadgroup f32 tiles with barriers** (`matmul.rs:57-95`;
`quantized_matmul.rs:119-174`); no `simdgroup`/matrix construct appears
anywhere in `radix-mir-metal/src/emit/**` (grep-verified 2026-08-18).
Why ours: it is a *body-level Metal arm* behind the same plan constants —
the closed-recipe-set and backend-neutral-plan locks are untouched (§14
I2's discipline); llama.cpp ships prebuilt simdgroup GEMMs, MLX's STEEL
GEMM infra is framework-owned — both tune for *all* models, we emit for
*the* model. Layout side: threadgroup/register layouts chosen at lowering
per shape class (M4's receipts). **AMX honesty**: AMX is the *CPU* matrix
ISA, not reachable from Metal; an AMX-friendly layout only matters if the
CPU fallback route becomes a product goal (§12-3 already parks int8/CPU
regime work). Risk note: high-end community GEMMs use undocumented
`simdgroup_async_copy` instructions (leaked headers, UB risk across OS
versions) — out of scope; official APIs only, and Metal 4's
`cooperative_tensor`/MPP `matmul2d` is the forward-compatible successor to
watch. Seam: `radix-mir-metal` emit arms + device-family gate (fail-closed
below Family 7). Cost: M. Gain: prefill compute-bound; mechanism + Apple
ISA documentation (no per-model number claimed).

**M10 — Buffer-pool/residency + per-step command-buffer batching.**
Mechanism (two parts): (a) residency — buffers already allocate
`StorageModeShared` on unified memory (`metal_host.rs:866`), so there is
no blit-transfer tax to remove; the remaining discipline is **pooling by
lifetime class** (PerProgram weights/KV, PerStep scratch,
ObservationPoint readbacks — the classes are declared facts,
`device_descriptor.rs:142-149`) instead of today's per-token
alloc/free. (b) launch batching — today every launch creates a command
buffer, encodes one kernel, commits, and **blocks** on completion
(`metal_host.rs:996-1027`); a decode step is dozens-to-hundreds of
serialized round-trips. The descriptor already carries exactly the facts
needed to batch safely: the ordered launch sequence, the inter-kernel
`data_flow` edges, declared `roots`, and per-step observation points
(`device_descriptor.rs:274-283,372-397`) — the host can encode a whole
step's kernels into one command buffer ordered by the declared graph and
read back only observation points. Why ours: the dependency graph is a
*verified plan fact*, not a runtime afterthought — MLX's scheduler does
this internally (framework-owned), llama.cpp encodes per-graph-build, we
can do it per-model with a proof. Seam: hosts/macos-arm64 session + trait
(one step-batch entry beside `launch_kernel`); no radix change, no lock
touched. Cost: S–M. Gain: launch/sync overhead elimination —
mechanism-only, but plausibly the largest *cheap* decode lever we have
given the per-launch blocking today; wave-6 harness decides.

**M11 — Power/thermal-aware scheduling.** Mechanism: Apple silicon
sustained clocks; dense prefill bursts heat the package and can depress
subsequent decode clocks; admission/cadence policy (defer prefill, cap
burst size, pace decode) trades prompt latency for sustained generation
rate. No published per-knob evidence; purely mechanism + hardware
behavior. Why ours: cadence is a session-admission policy riding the same
descriptor lifetime facts. Cost: S. Gain: unknown until measured — parked
behind wave-6 receipts; no wave depends on it.

### 15.3 Training-derived-but-inference-serving artifacts — the likely Qwen shape, as a first-class loadable

The undisclosed trials most plausibly *fine-tuned artifacts* so inference
gets faster with no runtime training. Four families, mapped to our
machinery:

| Family | What the finetune produced | Our expression | Delta needed |
| --- | --- | --- | --- |
| (a) Distilled attention patterns (effective locality; windowed attention behaving like full) | weights whose quality survives a shorter window | `KVStructure` per-layer-set `SlidingWindow` **authored from a recipe**, lowering bounds KV reads to the window (§4.3; I3) | window facts carried by the artifact's serving profile (below) |
| (b) Pruned KV heads (deeper GQA) | smaller K/V projections + masks | a bake transform: row-slice K/V projections at materialization (§13.2 pattern) + reduced `kv_heads` fact in `KVStructure` | generalize §13.2's transform set beyond the refusal family (`Slice/Mask` beside `OrthogonalizeWeight`) |
| (c) QAT weights that dequant cleaner (lower bit at same quality) | a better GGUF | **nothing new** — the format matrix (§3) admits it; per-format envelopes already derive per rung (I9); provenance records it was QAT-derived | manifest fields only (§12-6 pattern) |
| (d) Layout-specialized checkpoints | tensors pre-arranged for a target's fast path | the **second representation** `repack_plan.rs` explicitly reserved: "every descriptor field a second representation would determine (selected backend, persistence policy, executable compatibility)" is `PendingSecondRepresentation` (`repack_plan.rs:19-23`) — designed for exactly this | populate the pending fields in a second-representation unit |
| (e) Draft model (M7) | a small model trained to track the target | draft checkpoint + typed composition spec (N3) + its own band | composition spec type + session wiring |

**Answer: yes, as a recipe — not as a new engine capability.** The §13
machinery already establishes the loadable shape: base GGUF + typed recipe
spec authored beside LayerPlan, transforms **baked once at
materialization** (zero runtime cost), digest provenance verified
fail-closed at load (§12-6 / NEED `75e4ab98`), acceptance band pinned to
the *effective model* (NEED `e52dd09a` fold). What §15.3 adds is one
generalization: the recipe is not only *behavioral surgery* (refusal) but
can carry **inference-serving metadata** — KV-structure overrides
(window, kv_heads), layout/repack descriptors, draft linkage — with the
same three guarantees (typed admission, bake-not-train, checkable
provenance). Nothing here amends a §9 lock: baked tensors remain ordinary
tensors under EXEC-02 decision 4 (bounded, ledger-counted); the runtime
never trains anything; infeasible bundles fail closed at plan validation.

**Amendment need filed with this report (one, decision-only):** generalize
`75e4ab98`'s manifest fields to a *serving profile* block
`{kv_structure_override, repack_descriptor, draft_linkage, provenance}` —
default = adopt with W8-U6 below, authoring stays inline Gradus model
config, manifest stays derived/verification-only.

### 15.4 Metal-first wave rows (W8; ranked by value-per-cost, dependencies explicit)

Splices after §14.5's W7 rows at commit time; nothing preempts R-PACK-05
or renumbers waves 1–6/5b/7. Ranked **for Metal decode throughput**, the
operator's actual bar (§2).

| Rank | Unit | Scope | Cost | Depends on | Done-when |
| --- | --- | --- | --- | --- | --- |
| 1 | W8-U1 per-step command-buffer batching + observation-point-only readback | hosts macos-arm64 session (trait step-batch entry; encode launches ordered by declared `data_flow`/`roots`) | S | existing descriptor facts only | decode-step receipt: batched encoding passes step-equivalence pins AND a per-step launch-count of 1 (vs L×k round-trips); no lock touched |
| 2 | W8-U2 lifetime-class buffer pool | hosts macos-arm64 session (pool PerProgram/PerStep/ObservationPoint) | S | W8-U1 (same session surface) | pooled session runs leak bars (S2-2 counters) green; alloc/free churn per step → 0 |
| 3 | W8-U3 simdgroup 8×8 bodies for TiledMatMul/QuantizedMatMul | radix-mir-metal emit arms behind plan constants + Family-7 fail-closed gate | M | W7-U2 receipts (tile constants) desirable, not blocking | per-format kernel tests green on simdgroup arm; pre-Family-7 devices fail closed to scalar arm; decode+prefill receipts vs scalar arm on the dense rung |
| 4 | W8-U4 fused-dequant FA Metal arm + F16/Q8_0 KV execution | wave-3 recipe + KV bundle (M1+M2 as one bundle) | M | waves 2–3, GI4 amendment (§9), W8-U3 for the body | infeasible bundles (Q4_K V without fused arm) still fail closed at plan validation; long-ctx decode receipt vs f32-KV baseline; envelope rows derived |
| 5 | W8-U5 prompt-cache/session KV restore | session + buffer-version facts (M8) | S–M | EXEC-03 persistent sessions | restore-then-extend run pins identity vs continuous run (byte-exact KV); re-prefill measured at 0 for restored prefix |
| 6 | W8-U6 serving-profile recipe + manifest block | gradus recipe generalization (§15.3) + W5b-U4 digest helpers | M | W5b-U4 / `75e4ab98` fields (extend per above need) | one coverage probe: a QAT-requantized or window-override artifact loads as base+recipe, provenance verifies, band row pinned |
| 7 | W8-U7 speculative draft composition | gradus composition spec + batched decode | M–L | wave 4 (batched decode), W8-U1 (verification passes), W8-U6 (draft linkage) | output distribution pins vs greedy target on a small rung (rejection-sampling exactness); acceptance-rate receipt on dense rung — **parked until serving is a goal** (N3 posture) |
| 8 | W8-U8 power/thermal cadence policy | session admission policy | S | wave-6 measurement harness | parked until a receipt shows sustained-clock effect on this hardware; no wave depends on it |

Ranking rationale: rows 1–2 are hosts-only, touch no locks, and attack the
one *measured-in-code* pathology (per-launch blocking commit); rows 3–4
are the compute/bandwidth class that needs the recipe work already
sequenced by waves 2–4; rows 5–6 make the *trained-artifact* half of the
3.5–5× class loadable; rows 7–8 are real but sequenced by serving goals,
not by this design.

### 15.5 Locks and amendments

No §9 lock is amended by this addendum. M9/M5 are body-level Metal arms
behind existing plan constants (I2 discipline); M10 is hosts-session
internal (descriptor contract already declares the graph being consumed);
M2 rides the already-filed GI4 amendment; §15.3 rides §12-6/`75e4ab98`.
One decision need is filed (serving-profile manifest block, §15.3).
**Every external number cited is labeled published/community; every
unmeasured claim is mechanism-only; the wave-6 harness remains the sole
arbiter of any throughput claim (§8.3).**

---

*Addendum 3 ends. §13 (`c7174a33`) and §14 (`cbea0c29`) untouched. This
section is head-cto `1f58bbbc`'s only working-tree edit; mind routes the
commit.*

## 16. Addendum 4 — MoE structural sparsity: expert residency, hot-expert admission, per-expert modes

**Status**: DRAFT (uncommitted; mind routes the commit)
**Author**: head-cto (Vivi handle `d19f84dc`), 2026-08-18
**Ask**: operator — MoE models have small ACTIVE parameter sets per token
(1T total, ~50B active observed at the frontier); can a frontier MoE fit and
run fast on a local MacBook, and can ablation-style zeroing of
generally-inactive weights optimize a large model for local running?
**Placement**: appended after sibling addenda §13 (ablation, `c7174a33`),
§14 (census, `cbea0c29`), and §15 (Metal census, `1f58bbbc`, landed
concurrently before this append) — none touched. Numbered §16 to avoid the
§15 collision. §6.2/§7/§10 row splices proposed in §16.5, not
edited in place.
**Evidence pins**: `~/work/llama.cpp` @ `c8e03ce81` (same pin as §1/§14;
MoE path re-verified today at file:line), gradus @ `012d411` + uncommitted
addenda, radix main. Public-model numbers web-verified 2026-08-18 (sources
named inline; marked wv).

### 16.0 Mind's hypothesis chain, split into its two links

- **(a) "active set is what matters at inference, not total" — half-true,
  and the half that is false is the interesting one.** The active set bounds
  per-token FLOPs and per-token expert *reads*; it does not bound what must
  sit in memory. The resident floor (embeddings, lm_head, router, shared
  experts, attention, dense layers, KV) is *not* sparse, and the routed-expert
  mass is 96–98% of a frontier MoE's bytes — 1.0T of Kimi K2's 1.04T params
  (§16.3 arithmetic). Decode speed is set by **where each token's selected
  experts' bytes come from**, per token, not by the total. This is a
  residency/bandwidth question, not a parameter-count question.
- **(b) "ablate the inactive experts, keep the hot ones" — confirmed, and it
  is not a new mechanism: it is §13's machinery applied at expert
  granularity.** Ablation orthogonalizes a *direction* out of weight
  matrices; expert pruning ablates *whole cold weight tensors*. Same
  bake → manifest → provenance surfaces (§13.3, §12-6, NEED `75e4ab98`
  composes), same acceptance-band discipline (NEED `e52dd09a` folding,
  §12-2). The §15 contribution is the *routing-statistics producer* and the
  *residency consumer* llama.cpp has no seam for (§16.2).

### 16.1 Grounded mechanics — what touches memory at MoE decode (llama.cpp @ c8e03ce81)

Per token, batch-1 decode, one MoE layer (every claim file:line at the pin):

| Component | What is read per token | Evidence |
| --- | --- | --- |
| **Router/gate** | the full `ffn_gate_inp` matrix `[n_embd, n_expert]` — one GEMV every token, resident, format as stored (F32 in our rung) | `build_moe_ffn` → `build_lora_mm(gate_inp, cur)` → `[n_expert, n_tokens]` logits `src/llama-graph.cpp:1947-1949`; tensor shape from builders, e.g. `src/models/qwen3moe.cpp` (`{n_embd, n_expert}`) |
| Gating + top-k | elementwise softmax/sigmoid/√softplus over n_expert logits; DeepSeek-style group-limited selection; `argsort_top_k` picks `n_expert_used` | `llama-graph.cpp:1959-1980` (gating switch), `:2003-2027` (grouped selection, DeepSeek V3 ref), `:2030` (top-k) |
| **Selected experts' weights** | exactly the `n_expert_used` selected experts' matrices, gathered by id from one rank-3 tensor per family | tensors `{n_embd, n_ff, n_expert}` `src/llama-model.cpp:2881-2886` (`create_tensor_gate_up_exps`); op class `GGML_OP_MUL_MAT_ID` `src/llama-arch.cpp:794-796`; `ggml_mul_mat_id(as=[cols,rows,n_expert], b, ids=[n_expert_used,n_tokens])` "one matrix per expert" `ggml/src/ggml.c:3317-3347`; CUDA fuses MMVF/MMVQ only when `dst->ne[2]==1` (decode shape) `ggml/src/ggml-cuda/ggml-cuda.cu:1755-1812` |
| Combine | weighted sum of per-expert output views | `llama-graph.cpp:2226-2251` |
| **Shared experts** | always active, plain dense MUL_MAT, added outside routing — a per-token floor independent of the hot set | `src/models/deepseek2.cpp:151-153` (tensors), `:378-381` (`build_ffn` on shexp); Qwen3-MoE has none (`src/models/qwen3moe.cpp` MoE-only block) |
| **KV cache** | independent of expert count — attention path and cache class never see n_expert | cache classes per arch §4.2; MoE touches only the FFN sublayer |
| Embed / lm_head | one gathered embedding row; **the full-vocab head is read every token** | `llama-graph.cpp:2266+` (`build_inp_embd`); full-vocab head = census N2 (§14.4) |

**The honest memory model.** Resident-always, no residency policy can touch
these: embedding table (random gather), lm_head (full read per token),
routers, shared experts, attention + dense weights, norms, KV. Streamable /
lazy — the *only* large mass: routed-expert weights, whose per-token read set
is `n_expert_used × 3 matrices × n_ff × n_embd` bytes per MoE layer, at
whatever precision each expert is stored.

**llama.cpp's actual knob is placement-only.** `--cpu-moe` /
`--n-cpu-moe N` push the expert tensors' *whole rank-3 tensors* into a CPU
buffer via the regex `\.ffn_(up|down|gate|gate_up)_(ch|)exps`
(`common/common.h:1088-1098`, `common/arg.cpp:2661-2680`), generalizing
`--override-tensor` (`arg.cpp:2655`). All-or-nothing per layer range; no
hot-set, no per-expert modes, no admission statistics, no format mix per
expert. Its streaming behavior on Mac is accidental (mmap paging), which the
Unsloth K2 guide describes exactly: the 621 GB Q4_K_M "will page to the
(fast) SSD and be noticeably slower" (wv, unsloth.ai K2 guide).

**Our admitted rung is already an MoE with exact tensor facts.** The
Qwen3.6-35B-A3B row (753 tensors, §2) is `qwen35moe`: 41 blocks (19 hybrid
SSM/attention + 16 full-attention + nextn blk.40), **256 experts, top-8**,
expert FFN 512, **one shared expert** FFN 512
(`gradus/src/model/qwen35moe.fab:315-336`). Per MoE block the canonical map
pins exactly the shapes above: `ffn_gate_exps [2048,512,256] Q4_K`,
`ffn_up_exps [2048,512,256] Q4_K`, `ffn_down_exps [512,2048,256] Q5_K`
(Q6_K in blk.34/38/39), router `ffn_gate_inp [2048,256] F32`,
`ffn_*_shexp` Q8_0 (`qwen35moe.fab:483-490,518-524`). Arithmetic at stored
formats: one expert ≈ 0.59 (gate) + 0.59 (up) + 0.72 (down) ≈ **1.9 MB**;
per-token expert stream = 8 × 1.9 MB × 35 MoE blocks ≈ **0.53 GB**; routers
+ shared + head ≈ 0.61 GB/token resident stream; experts are
35×256×3×2048×512 = 28.2B of 35.5B elements — **79% of the 22.66 GB file**.
The seam we own is therefore already admitted as typed facts, not a
hypothetical.

### 16.2 Our levers, mapped to seams

1. **Expert residency / lazy-load policy** (host-ABI + KVStructure-adjacent).
   A semantic `ExpertResidency` fact in the Gradus model config (same
   tripartite split as §4.3: Gradus semantic → Radix plan fact → Hosts
   physical), consumed by the hosts partition ledger, which already budgets
   per-class bytes and single-sources KV accounting
   (`hosts/crates/host-coordinator/src/partition.rs:95-122`). Experts become
   a partition class with per-expert granularity (today's contract is
   per-tensor, all-or-nothing). The lazy-load primitive already exists:
   bounded windowed materializers `materialize_slice` / `materialize_block`
   (`gradus/src/model/tensor_view.fab:204,266`) — an expert is a rank-3
   slice, materializable on demand. Default unchanged: resident as-stored.
2. **Hot-expert admission — a bake-time artifact** (generalizes §13). Bake
   pipeline: run a *calibration corpus* through the admitted model →
   accumulate per-(layer, expert) routing statistics (selection mass + gate
   weight mass) → importance scores → **hot-set manifest** (per layer:
   ordered admit list + acceptance band receipt). Same surfaces as §13:
   bake at materialization, manifest + digests into the admission manifest
   (NEED `75e4ab98` composes — add routing-stats digest + hot-set digest as
   sibling fields of the base-GGUF/AblationSpec digests), provenance
   fail-closed at load (§12-6 pattern).
3. **Per-expert modes — LayerPlan-style** (`ExpertPlan`, beside LayerPlan
   and AblationSpec): per-(layer, expert) `Keep | Zero | Prune |
   Resident{tier} | Streamed`. `Zero` masks the router column and
   renormalizes admitted weights (changes the computed function → recorded
   band, §12-2 fold; never inherits GI0). `Prune` bakes the rank-3 tensor
   down and remaps ids — byte shrink at materialization, zero runtime cost.
   Hot-set manifests turn Keep/Streamed into an *admission decision*, not a
   runtime guess — placement is declared, checkable, and provenance-pinned.
4. **Fused router + gather kernels** (kernel_plan). `GroupedMatMul` is a
   reserved closed-set recipe whose plan already carries `groups` as
   "Expert / group count (the leading rank-3 axis)"
   (`radix/crates/radix-mir/src/kernel_plan/plan.rs:105-106,260-268`) — the
   selected-experts batched body is its intended home. A fused
   router(softmax+top-k)→ids→gather body is a wave-4 decode-regime rider
   (llama.cpp's analogue is the MMVF/MMVQ decode fusion,
   `ggml-cuda.cu:1755-1812` — selection among prebuilt families there,
   emitted code here). Any new variant goes through the explicit
   reviewable-change door (`plan.rs:44-50`); no §9 lock touched.
5. **Mixed residency + quantization-per-expert** (format matrix composes).
   Hot experts at F16/BF16 (wave 1 admission), cold at Q4_K/Q2-class —
   per-expert format is the §3.2/§6.2 per-tensor storage dial applied at
   rank-3-slice granularity: declared per entry in the manifest, never
   silent (§6.2 row 1 rule), each cell carrying its derived envelope
   (census I9).

### 16.3 The MacBook-frontier question, answered honestly

Chosen model: **Kimi K2** — the public 1T-class MoE (model card + config,
wv 2026-08-18: HF `moonshotai/Kimi-K2-Instruct`, tech report arXiv:2507.20534):
**1.04T total, 32.6B active**, 61 layers (1 dense + 60 MoE), **384 routed
experts, top-8**, 1 shared expert (intermediate 1024), hidden 7168, expert
intermediate 2048, MLA (`kv_lora_rank 512 + rope 64` = 576 elems/token/layer),
vocab 160K, 64 heads. Hardware frame: burgus-class M5 Max (§2 bar machine) —
614 GB/s unified memory, 128 GB ceiling, internal SSD ≈ 13.6 GB/s read
(4TB); M4 Max reference 546 GB/s / 7.3 GB/s (wv, Apple specs + The Verge
M5 benchmark suite).

**Working-set arithmetic (decode, batch 1):**

| Mass | Bytes | Resident? | Read per token |
| --- | ---: | --- | ---: |
| Routed experts (60×384×3×7168×2048 = 1.015T elems) | **571 GB** @Q4_K (0.5625 B/elem); 337 GB @2-bit (wv, Unsloth dynamic quants) | **no — the streamable mass** | 8×3×7168×2048×60 = 21.1B elems ≈ **11.9 GB** @Q4 |
| Embedding [160K × 7168] @Q8_0 | 1.22 GB | yes (random gather) | ~7 KB (one row) |
| lm_head [7168 × 160K] @Q6_K | 0.94 GB | yes | **0.94 GB — full read, every token** |
| Routers 60 × [7168×384] F32 | 0.66 GB | yes | 0.66 GB |
| Shared experts 60 × 3×7168×1024 @Q8_0 | 1.40 GB | yes | 1.40 GB |
| MLA attention ≈101M×61 elems @Q8_0 | ≈6.6 GB (≈3.5 GB @Q4_K) | yes | same (all weights touched by GEMV) |
| KV (MLA-compressed) | 70 KB/token/layer-set → 0.57 GB @8k ctx, 9.2 GB @128k (F16) | yes | grows with ctx |
| **Resident floor total** | **≈11 GB + KV** (Q6/Q8 mixes; Q4 attention halves it) | — | **≈9.6 GB** |

The floor fits trivially in 128 GB. The experts do not: 571 GB @Q4 is 4.5×
the machine. What fits is a ~100 GB expert slice — **17.5% of the expert
mass**, ≈67 of 384 experts/layer average — plus floor + KV + OS headroom.

**Ceilings (per-token time = floor from RAM + expert reads from wherever
they live; M5 Max):**

| Regime | Arithmetic | tok/s |
| --- | --- | ---: |
| All-experts-resident (impossible here; the gpt-oss-120b regime) | (9.6+11.9) GB ÷ 614 GB/s = 35 ms | ~28 |
| Pure streaming (every expert read from SSD) | 9.6 GB ÷ 614 + 11.9 GB ÷ 13.6 = 15.6 + 874 ms | **1.1** |
| Hot-set hit rate p=0.90 | 15.6 + 0.9×19.4 + 0.1×874 ms | 8.3 |
| Hot-set hit rate p=0.99 | 15.6 + 19.2 + 8.7 ms | 23 |

**Verdict (link (a)): no — a 1T-class MoE is not a fast local MacBook model
via active-set discipline alone.** The active set bounds the per-token read
stream, but 11.9 GB/token still has to come from somewhere: RAM-resident it
is bandwidth-capped ~28 tok/s *best case*; SSD-streamed it is ~1 tok/s; and
realistic hot-set hit rates put you between ~5 and ~25 tok/s where **each
1% of routing mass that misses the hot set costs ~8.7 ms (~20–35%
throughput)**. Disk bandwidth, not parameter count, is the ceiling.

**Verdict (link (b): pruning to raise p) — possible, with measured,
non-free quality cost.** Lu et al., *Not All Experts are Equal*
(arXiv:2402.14800, wv): Mixtral 8×7B, pruning 2 of 8 experts per layer
(~25% of expert mass) ≈ −0.1 avg points across 8 tasks; pruning 4 of 8
(~50%) ≈ −3.7 points; *task-specific calibration* (MATH-set) substantially
recovers domain performance vs generic C4 calibration. DeepSeek V3's
auxiliary-loss-free balancing deliberately keeps experts specialized by
domain (tech report Fig. 9, arXiv:2412.19437, wv) — which cuts both ways:
hot sets *are* concentrated per domain, but a hot-set manifest is a bake-time
bet on the corpus, and domain shift silently invalidates it. Hence the
acceptance band is a recorded artifact, not a hope (§13.4 discipline).

**The catches, named:** (1) *first-token latency* — prefill across a long
prompt touches a large union of experts per layer (routing diversity over
prompt tokens approaches the full set), so cold-start prefill streams a
large fraction of the 571 GB once: tens of seconds of pure SSD time at Q4.
(2) *Disk bandwidth as the real ceiling* — shown above; also the practical
experience with llama.cpp mmap paging on Mac (Unsloth guide, wv). (3)
*Router overhead is in the floor* — 0.66 GB/token F32 reads, 0.66 GB
resident; a real but second-order cost (Q8 router would quarter it).
(4) *Pruning quality loss* — measured evidence above; band per §12-2 fold.

**What the honest positive answers are:** our admitted Qwen3.6-35B-A3B
(22.66 GB, 3B active) fits fully resident — no residency machinery needed;
its decode is a ~1.2 GB/token stream (§16.1) whose ceiling on M5 Max is
bandwidth, and the bar stays llama.cpp parity. The tier where our knobs
genuinely beat llama.cpp's all-or-nothing `--cpu-moe` is **120–235B total**:
gpt-oss-120b (117B total, 5.1B active, ~60–63 GB MXFP4) already runs
30–50 tok/s on 128 GB M4 Max in llama.cpp (wv, llama.cpp discussion #15396 +
user reports) — it fits, no streaming needed; **Qwen3-235B-A22B** (235B/22B
active, 128 experts, top-8; wv HF card) @Q4 ≈ 132 GB does *not* fit
as-stored, and is exactly the composition case: hot-set residency +
per-expert format mix (hot Q6_K/F16, cold Q4/Q2 streamed or pruned) +
prune-to-fit, each band recorded.

### 16.4 Wave-plan rows (proposed; §10 not edited by this addendum)

**Wave 5c — MoE expert plan** (after W5b — reuses the AblationSpec bake/
manifest/provenance machinery; U1/U3 ride W5 LayerPlan acceptance rows;
U4 rides W2's KVStructure tripartite pattern; U2's manifest fields land with
wave 6 admission manifest; U5 rides wave 4 decode regime and W1 F16).

| Unit | Repo/scope | Done-when |
| --- | --- | --- |
| W5c-U1 `ExpertPlan` type + admission validation | gradus `src/model/` (beside LayerPlan/AblationSpec: per-(layer,expert) `Keep/Zero/Prune/Resident{tier}/Streamed`, hot-set manifest reference; validation negatives: expert id out of range, Zero/Prune on shared experts, empty admitted set, duplicate entries, mode on non-MoE layer) | proba: empty-plan identity pin (plan-absent ≡ base-as-stored) + all validation negatives green |
| W5c-U2 routing-statistics bake → hot-set manifest | gradus bake seam from W5b-U2 (calibration corpus through admitted forward; per-(layer,expert) selection + weight-mass accumulation; importance scores; hot-set manifest + digest — NEED `75e4ab98` fields compose) | synthetic-corpus bake pins exact statistics; manifest digest verified; tampered-digest load rejected (negative) |
| W5c-U3 Zero / Prune execution + id remap | gradus `forward` + lowering (Zero: router-column mask + renormalization over admitted experts; Prune: rank-3 tensor shrink at materialization via `tensor_view.fab:204,266` bounded materializers, ids remapped at bake) | proba: Zero band row recorded vs pinned pruned reference; Prune byte-shrink receipt; token-stream equivalence for Prune-with-renormalize-off negative rejected |
| W5c-U4 expert residency in the host contract | hosts partition class for expert windows (resident hot-set admission budget + streamed cold windows; default unchanged — experts resident as-stored unless `Streamed` entries present) | partition ledger rejects an infeasible residency bundle at admission (negative); resident-default byte accounting byte-identical to today |
| W5c-U5 fused router + selected-experts decode body | radix `kernel_plan` `GroupedMatMul` body (`plan.rs:105-106,260-268` — `groups` is the expert axis; ids-driven gather; wave-4 decode-regime rider) | kernel tests for the gather body; explicit reviewable variant record; no runtime dispatch table added |
| W5c-U6 acceptance rows + coverage probe | gradus proba/docs extending the §12-2 fold to **expert-plan-modified execution**; one probe on the admitted 753-tensor rung: synthetic routing stats → hot-set → Zero band row | band receipt committed; hot-set-vs-full-model divergence band recorded per corpus |

### 16.5 Dial/cost row splices + amendment needs (proposed; splice at commit time)

§6.2/§7 row additions (spliced beside the Ablation rows):

| Dial | Home | Default |
| --- | --- | --- |
| `ExpertPlan` (per-expert modes) | Gradus model config, beside LayerPlan/AblationSpec | empty (all experts Keep, resident as-stored) |
| Expert residency tier (Resident{F16,Q4_K,…} / Streamed) | Gradus semantic → plan fact → hosts partition | resident as-stored; `Streamed` requires an ExpertPlan |
| Hot-set manifest (bake artifact) | admission manifest (NEED `75e4ab98` sibling fields) | absent (no hot-set claim without provenance) |

| Knob | Default | Expected gain (mechanism) | Cost / risk |
| --- | --- | --- | --- |
| Expert Zero (renormalize) | off | removes routed-expert read bytes ∝ pruned routing mass; enables prune-to-fit on 128 GB tier | quality divergence by construction → recorded band (§12-2 fold; Lu et al. evidence: ~25% mild, ~50% real loss); domain shift invalidates the bake |
| Expert Prune (bake shrink) | off | byte shrink at materialization, zero runtime cost | id remap correctness; requant band per §12-5 rule applied per expert |
| Hot-set residency | resident as-stored | cold experts stop competing for unified memory on >RAM models | miss-path streams from disk — bandwidth-bound; partition admission proof required |
| Per-expert format mix | as-stored | hot experts compute-friendly (F16), cold byte-minimal (Q4/Q2) | per-expert envelope derivations (I9); declared, never silent |

**§12 additions** (numbered after the sibling's §12-8):

9. **Expert partition granularity + streamed residency in the host
   contract** (§16.2-1, W5c-U4): default = experts are resident as-stored
   (byte accounting unchanged); streamed/lazy residency is admitted only
   when an ExpertPlan declares it and the partition ledger proves the
   budget at admission. This is a hosts-contract widening, not a GI4 KV
   revision — KV facts untouched.
10. **Zero-renormalization acceptance policy** (§16.2-3, W5c-U3): default =
    expert-plan-modified execution carries its own recorded band vs a pinned
    expert-plan-modified reference (the §12-2 fold extended one level);
    never inherits the GI0 exact-top-1 contract.

**No §9 lock is amended by this addendum.** `GroupedMatMul` variant work
goes through the explicit reviewable-change door (`plan.rs:44-50`); F16
per-expert formats ride W1 admission; residency default preserves today's
behavior byte-for-byte.

### 16.6 Re-evaluation — DeepSeek-V4-Flash-0731 as the local-viability model (operator instruction; replaces Kimi K2 as the evaluation case)

**Status**: DRAFT (uncommitted working-tree edit on committed §16 @ `5b46a77`;
mind routes the commit)
**Author**: head-cto (Vivi handle `d68a0ac4`), 2026-08-18
**Ask**: operator — re-run the §16 Part-3 local-viability analysis with
**DeepSeek-V4-Flash-0731** replacing Kimi K2: it is the natural local-running
target, the model someone actually deploys on a MacBook. §16.3's K2 analysis
stands unamended as the 1T *ceiling* case; this section is the deployment-class
case and supersedes K2 (and the §16.3 closing note's Qwen3-235B-A22B) as the
named W5c evaluation model.
**Evidence pins**: all public-model numbers web-verified 2026-08-18 (wv) from
first-hand fetches: HF card `deepseek-ai/DeepSeek-V4-Flash-0731` + its
`config.json`, HF card `deepseek-ai/DeepSeek-V4-Flash` (collection table),
tech report arXiv:2606.19348 (abstract), Unsloth guide
`unsloth.ai/docs/models/deepseek-v4` (quant table, measured), antirez/ds4
README (`github.com/antirez/ds4`, M5 Max benchmarks, streaming design).
Hardware frame reused from §16.3 (M5 Max: 614 GB/s unified, ≈13.6 GB/s SSD).
Every number below is tagged **(wv)** fetched, **(derived)** arithmetic from
verified config, or **(inferred)** reasoned-but-not-directly-verified.

#### 16.6.0 What changed with this model

The operator's premise is itself verified: v4-flash-0731 is not a hypothetical
local target. A dedicated native engine exists for exactly it — ds4
("DwarfStar", antirez): "optimized first for DeepSeek V4 Flash… Metal, the
primary target, on Macs with 96 GB or more. Smaller machines can use SSD
streaming" (wv, ds4 README) — and Unsloth ships Mac-targeted dynamic GGUFs
with a hardware table starting at 92 GB total memory (wv, Unsloth guide).
§16.3's K2 question ("does a frontier MoE fit at all?") becomes three live
regimes on the same §2 bar machine class: **resident**, **boundary**, and
**streaming** — with a published measured reference on the exact M5 Max 128 GB
hardware (§16.6.2).

#### 16.6.1 Architecture facts — verified vs derived vs inferred

| Fact | Value | Status / source |
| --- | --- | --- |
| Total params | **284B** core model; 0731 repo reports 304B safetensors **including** the attached DSpark speculative module (preview+DSpark repo: 291B) | wv: V4-Flash card collection table; 0731 card; HF repo counters. DSpark mass unresolved beyond the 5.6 GiB support GGUF (wv, ds4) — **inferred** ≈7–20B |
| Active params/token | **13B** (card) | wv; **derived** cross-check: 6×25.17M×43 (routed) + 1.08B (shared) + ~4.5B (attn+indexer) ≈ 12.1–12.6B ✓ |
| Layers | **43**, all MoE — **derived**: routed mass 43×6.4425B = 277.0B and 284−277.0 = 7.0B non-routed close the identity exactly; any dense-FFN layer would break it by ~6.2B. (V3's first-k-dense pattern is gone.) | config `num_hidden_layers: 43` (wv); mix derived |
| Routed experts / layer | **256**, each 3 matrices × 4096 × 2048 = 25.17M elems (≈13.4 MB @ MXFP4, 7.1 MB @ 2.25 bpw) | wv config; sizes derived |
| Top-k | **6** (`num_experts_per_tok`), `norm_topk_prob`, `routed_scaling_factor` 1.5 — selectivity 2.34% of experts/token/layer | wv config |
| Shared expert | **1**, intermediate 2048 (same size as one routed expert) — 1.08B elems total ≈ 1.15 GB @Q8_0 | wv config; bytes derived |
| Router | `ffn_gate_inp`-class [4096×256] F32 per layer ≈ 45M elems, 0.18 GB/token read; scoring `sqrtsoftplus`, `topk_method noaux_tc` (V3 aux-loss-free lineage) | wv config; bytes derived |
| Expert storage | **native MXFP4** (`expert_dtype: fp4`); model is quantization-aware-trained; Unsloth repack is bit-identical (1,328 tensors, 0% weight error, KLD ~0); everything else FP8/BF16 (block 128×128, ue8m0 scales) | wv config + Unsloth quant analysis |
| Attention | **MLA-descendant, not plain GQA/MLA**: `q_lora_rank` 1024, `o_lora_rank` 1024, `o_groups` 8, 64 heads, `head_dim` 512, `qk_rope_head_dim` 64, **`num_key_value_heads: 1`** | wv config |
| KV compression (HCA) | per-layer `compress_ratios`: **19 layers ×4, 18 layers ×128, 5 uncompressed** (2 head + 3 tail) — array has 42 entries vs 43 layers; the untyped layer and the semantics of `num_hash_layers: 3` are **not public beyond the config keys** (honest catch) | wv config; per-tier census derived |
| Sparse selection (CSA) | indexer: 64 heads × 128 dims, **top-512** token selection (`index_topk`), `sliding_window` 128 raw window | wv config |
| Residual stream | mHC hyper-connections, **4 streams** (`hc_mult` 4, sinkhorn iters 20) | wv config |
| Context | **1,048,576** (yarn ×16 from 65536) | wv config + card |
| Speculative | **DSpark** in-checkpoint (block 5, markov_rank 256, targets layers 40–42); support GGUF 5.6 GiB; measured 1.5–1.9× local in llama.cpp, up to 2× / 120 t/s on B200 | wv config, ds4, Unsloth |
| Vocab / lm_head | 129,280; untied — 529.5M elems ≈ 0.56 GB @Q8_0 full read per token | wv config; bytes derived |
| Released quantizations (measured GB) | official MXFP4/FP8 **156.4**; Unsloth UD-Q8_K_XL **161.9** (lossless), UD-Q4_K_XL **155.1** (experts stay MXFP4), UD-IQ3_XXS **103** (recommended 128 GB tier); antirez Q4KExperts-F16 **164.6**, mixed L37-42-Q4K **97.6**, IQ2XXS **86.7**; ds4 2-bit routed (up/gate IQ2_XXS + down Q2_K) **81**; DSpark support +~10 GB headroom | wv Unsloth table + ds4 README |

**Derived byte cross-checks** (all hang together): MXFP4 4.25 bpw × 277.0B
elems = 147.2 GB + ~7.3 GB FP8 non-expert ≈ 154.5 ≈ official 156.4 (wv);
2.25 bpw avg (2×2.0625 + 2.625)/3 × 277.0B = 77.9 GB + Q8 floor ≈ 85 ≈
measured 81–86.7 (wv). Routed experts are 277.0/284 = **97.5% of the model**
(derived; Unsloth's "~96%" agrees within rounding).

#### 16.6.2 Working-set arithmetic (hardware frame stated)

Same frame as §16.3: **burgus-class M5 Max, 128 GB unified, 614 GB/s
nominal, internal SSD ≈13.6 GB/s** (§16.3 pins). Nominal-bandwidth rooflines
are ceilings, not targets — sustained achievable is ~70–80% of nominal
(inferred); every regime below is paired with a **measured** reference where
one exists.

**Resident floor (never streamable), Q8-attn/Q8-shared/Q8-out class with F16
compressor/indexer (ds4's own mix, wv tensor naming):**

| Mass | Bytes | Read/token |
| --- | ---: | ---: |
| Attention + indexer + compressor (≈4.5–5B elems, **inferred** from config dims; exact inventory not public) | ≈4.8–5.5 GB | same (GEMV reads all) |
| Shared experts @Q8_0 | 1.15 GB | 1.15 GB |
| lm_head @Q8_0 (vocab 129,280) | 0.56 GB | **0.56 GB — full read/token** |
| Routers F32 | 0.18 GB | 0.18 GB |
| Embedding | 0.56 GB | ~4 KB (row gather) |
| **Floor read/token** | — | **≈7 GB** |
| KV (this arch): **26 GB @1M ctx measured** (indexer ≈22 GB of it) | 26 GB | scales ~linearly (inferred): ≈0.8 GB @32k, 2.6 @100k, 7.8 @300k |

**Fit on 128 GB:** 2-bit routed (78 GB experts) + ~7.4 GB floor + KV fits
resident — **≈90–95 GB @100k ctx** (derived), proven by ds4 running it. 3-bit
(103 GB) is the boundary tier (Unsloth: ≥110 GB total; 300k ctx ≈118 GB —
tight). MXFP4 (147 GB experts) and Q8 (162 GB) **do not fit** — that is the
streaming tier, exactly like Unsloth's ≥169 GB line (wv).

**Per-token expert stream (top-6 × 43 layers = 6.49B elems/token):**
**3.45 GB** @MXFP4, **1.83 GB** @2.25 bpw, 3.65 GB @Q4_K-experts. (K2 was
11.9 GB @Q4 — this model streams 3.3–6.5× less per token; expert mass is
571→147/78 GB.)

**Regimes (per-token time, M5 Max):**

| Regime | Arithmetic | tok/s |
| --- | --- | ---: |
| Resident 2-bit — roofline | (7.0+1.83) GB ÷ 614 GB/s = 14.4 ms | **~70 ceiling** |
| Resident 2-bit — **measured** (ds4, q2, M5 Max 128 GB) | 39.35 t/s @2k, 36.14 @16k, 34.36 @32k, 27.64 @64k ctx | **39.4–27.6 real** |
| Pure streaming MXFP4 | 7.0÷614 + 3.45÷13.6 = 11.4 + 253.7 ms | **3.8** |
| Hot-set p=0.90 @MXFP4 | 11.4 + 5.1 + 25.4 ms | 23.9 |
| Hot-set p=0.99 @MXFP4 | 11.4 + 5.6 + 2.5 ms | 51.3 |
| Pure streaming 2-bit | 11.4 + 134.6 ms | 6.9 |
| Hot-set p=0.90 @2-bit | 11.4 + 2.7 + 13.5 ms | 36.3 (≈ resident) |

The measured engine runs at ~57% of the nominal roofline; the gap is
attributable (inferred) to mHC's 4-stream residual traffic, the
indexer+compressor passes, launch overheads (§15 M9/M10), and sub-nominal
sustained bandwidth. Roofline ≠ acceptance bar.

**Hot-set solve (the GB question).** For 20 t/s (50 ms budget): MXFP4
streaming needs hit rate **p ≥ 0.87**; 2-bit needs **p ≥ 0.73**. For 30 t/s:
p ≥ 0.93 (MXFP4) / 0.86 (2-bit). Cache GB = p only if routing is
concentrated: at 32 GB of 78 GB 2-bit expert mass (41% of mass) the top-41%
experts per layer must hold 73% of routing mass — a **1.8× concentration
factor**; at 40 GB of 147 GB MXFP4 (27% mass) the required factor is 3.2×.
V3-lineage `noaux_tc` keeps experts domain-specialized (§16.3's Fig-9
evidence carries by family — inferred), and this model uses the same
mechanism (wv config), but **the p(cache) curve for v4-flash-0731 is
unmeasured anywhere public** — producing exactly that curve on a calibration
corpus is W5c-U2's bake artifact, and it is the acceptance-band receipt, not
a hope (§13.4 discipline). Each 1% of routing mass that misses costs ~2.5 ms
@MXFP4 (~6% throughput at the p=0.9 point) — far gentler than K2's ~8.7
ms/1% because the resident floor is a larger fraction of the token budget.

**First-token latency shape.** Resident prefill is measured (ds4, q2):
790 t/s @2k → 557 @32k → 398.5 @64k — a 2k prompt ≈ **2.6 s**, 25k ≈ 45 s,
64k ≈ 165 s; prefill, not decode, dominates interactive first-token on long
agentic prompts. Streaming adds a one-time expert-warmup pass ≈ expert mass ÷
13.6 GB/s = **10.8 s** (MXFP4) / 5.7 s (2-bit), partially overlappable (ds4
reserves two full routed layers for overlapped streaming prefill — wv), and
practically mitigated by KV disk-cache prefix reuse (ds4 ships it) or a
bake-time hot-set preload. Prefill routing diversity still approaches the
full expert union over long prompts (§16.3 catch 1, unchanged).

#### 16.6.3 The §16 knob set on this exact architecture

1. **Shared experts always-resident** — unchanged, and the market converged
   on our default: ds4/antirez 2-bit quants quantize *only* routed experts
   and leave "shared experts, projections, routing… untouched" (wv). Our
   `Resident` tier default is byte-identical in spirit; 1.15 GB/token floor.
2. **Hot-expert admission at 256 experts, top-6** — same machinery as §16.2,
   finer grain: per-expert byte quantum 13.4 MB (MXFP4) / 7.1 MB (2-bit);
   97.7% of expert mass is cold. Router is trivially resident (0.18 GB,
   F32); `sqrtsoftplus` + `noaux_tc` stats accumulate exactly like the W5c-U2
   bake design.
3. **Per-expert format mix — with a real catch.** The quality/size frontier
   is now *published calibration*: MXFP4 experts are bit-identical (0% error,
   KLD ~0); requantizing experts to Q4_K costs 5.2% RMSE / KLD 0.029; 2-bit
   (IQ2_XXS/Q2_K routed-only, imatrix) costs 22% weight error / KLD 0.42 /
   PPL 4.5319→6.15 / 77.9% same-top-token (all wv, Unsloth measured table).
   **MXFP4 is not in our closed storage set** (`PackedStorageLayout` =
   {F32, Bf16, Q8_0, Q4_K, Q5_K, Q6_K, Q5_0}, §3.1) — the natural target's
   native expert format is outside our admitted set. Amendment need #1.
4. **KV/attention — the KV-slimming story changes materially.** This is not
   plain MLA: an MLA-descendant projection stack (q/o LoRA 1024, one 512-dim
   KV latent + 64 rope) plus *trained* per-layer KV compression (HCA tiers
   4×/128×) plus sparse top-512 selection (CSA indexer) plus a 128-token raw
   window. For KVStructure (§4.3): **(a)** KV slimness is now architectural
   and *per-layer heterogeneous* — the abstraction needs per-layer cache
   classes (raw-window / compressed-4× / compressed-128× / indexer), not one
   per-model KV dtype; **(b)** the dominant long-context KV mass is the
   **indexer cache (~22 GB of 26 GB @1M, measured)** — a mass K2/V3-family
   MLA models do not have; if the indexer is not its own partition class,
   long-context accounting is simply wrong (sharpens W5c-U4); **(c)** the
   inference-side KV dials survive but multiply per class — vLLM's official
   recipe ships `--kv-cache-dtype fp8` *and* `use_fp4_indexer_cache` (wv,
   0731 card); **(d)** the tech report's 10%-of-V3.2-KV @1M claim (Pro,
   wv abstract) is the class evidence. The §4.3 tripartite
   semantic→plan→physical split survives; its class inventory does not.
5. **mHC (4 residual streams)** — activation traffic and state ×4 in the
   residual path; rooflines and §15 M9/M10 launch work should account it
   (inferred attribution for the 70→39 roofline gap).
6. **DSpark** — a trained draft artifact shipped *in* the checkpoint, 1.5–1.9×
   measured locally (wv). Maps onto §15.3's loadable-artifact story; composes
   with W5c, not part of it.
7. **Honest competitive catch.** §16.2's "llama.cpp has no seam for hot-set"
   is now incomplete *for this model*: ds4 ships `--ssd-streaming` with a
   runtime routed-expert cache (`--ssd-streaming-cache-experts 32GB`), a
   hot-expert preload list (`ds4_streaming_hotlist.inc`,
   `--ssd-streaming-preload-experts N`), and overlapped streaming prefill
   (wv, ds4 README). Our differentiation is the **declarative discipline** —
   bake-time hot-set manifests with acceptance bands, provenance digests,
   per-expert format mix, partition admission proofs — not the existence of
   an expert cache. W5c's value claim should be restated against ds4, not
   only llama.cpp.

#### 16.6.4 Verdict + first-rung acceptance band

**Yes — v4-flash-0731 is the right FIRST target for W5c**, and a better one
than both prior candidates: (1) unlike K2 it has live regimes on the §2 bar
machine class with a published measured reference on the exact hardware
(M5 Max 128 GB: 39.35 t/s decode, 790 t/s prefill, wv ds4); (2) unlike
gpt-oss-120b (§16.3's fits-resident case) it exercises *all* of §16's
machinery — shared expert, streaming tier, hot-set admission, per-expert
formats — at 284B scale; (3) its quality/size frontier is measured, so
acceptance bands have ground truth; (4) the expert mechanics are the same
kind as §16's design (256×3 rank-3 tensors per layer), so W5c-U1..U6 keep
their shape. **Sequencing**: the admitted Qwen3.6-35B-A3B rung (§16.1)
remains the machinery-proving rung — v4-flash-0731 is the W5c *target*
after that rung lands ExpertPlan; `deepseek_v4` model-config admission is
the named producer fact.

**First-rung acceptance band (v4-flash-0731, M5 Max 128 GB, 2-bit routed
quant class):**

| Axis | Band | Anchor |
| --- | --- | --- |
| Decode @32k ctx | floor **20 t/s**, parity **34 t/s**, stretch 39+ | ds4 measured 34.36 @32k; roofline ~70 stated as ceiling-not-target |
| Prefill | ≥600 t/s @2k, ≥300 t/s @64k | ds4 measured 790 / 398.5 |
| Quality | bands recorded vs the **declared quant baseline** (2-bit routed = PPL 6.15 / KLD 0.42 vs official; MXFP4 = bit-identical), never vs FP16; hot-set manifests carry the corpus-shift band (§13.4) | Unsloth measured table (wv) |
| Residency | resident-default byte accounting identity unchanged (W5c-U4 negative); streaming only where an ExpertPlan declares + partition proves budget | §16.2-1 |
| Hot-set | the p(cache) curve is the rung's deliverable artifact with digest, not a throughput claim | §16.6.2 solve |

#### 16.6.5 Amendment needs (routed to mind with this report)

1. **NEED — contract**: admit **MXFP4** into `PackedStorageLayout`
   (`radix/crates/radix-mir/src/abi/contract.rs:162-192`) or declare an
   explicit expert-requant band policy. Blocks per-expert format mix on the
   natural target; machinery provable on existing formats meanwhile. This is
   a hosts/radix contract widening, same class as §12-9.
2. **NEED — design**: §4.3 KVStructure class inventory extension — per-layer
   heterogeneous KV (raw window / compressed-4× / compressed-128× /
   **indexer**) + per-class format dials (incl. FP4 indexer cache); W5c-U4's
   partition ledger gains the indexer cache as a budget class (~22 GB @1M,
   measured). Not a GI4 KV revision; new classes beside the existing ones.
3. **NOTE**: mHC 4-stream residual traffic belongs in §15.0/M9–M10 rooflines.
4. **NOTE**: DSpark draft = §15.3 loadable artifact; composes, no new W5c row.
5. **NOTE**: §16.2's competitive framing should name ds4's runtime streaming
   hotlist; our claim is declarative bake/band/provenance, not cache
   existence.

---

*Addendum 4 ends. §13 (`c7174a33`), §14 (`cbea0c29`), and §15 (`1f58bbbc`)
untouched above. §16 body committed at `5b46a77`; §16.6 is head-cto
`d68a0ac4`'s working-tree edit on top — mind routes the commit.*
