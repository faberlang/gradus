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
2. **Layer-sliced acceptance policy** (§5.2): default = sliced runs carry their
   own recorded band (logit-band vs pinned sliced reference), never inheriting
   the GI0 exact-top-1 contract.
3. **Int8 activation dot (CPU regime)**: default = not admitted; revisit only
   if a CPU route becomes a product goal.
4. **Perf-harness ownership**: default = one faber-side benchmark unit (wave 6)
   using gradus `benchmark-method.md`; llama.cpp runs offline as comparator.
