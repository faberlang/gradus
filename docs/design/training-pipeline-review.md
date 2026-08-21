# Gradus training pipeline review + impossible-knobs census (training edition)

**Status**: DRAFT (uncommitted; mind routes the commit)
**Author**: head-cto (Vivi handle `5fc076e8`)
**Date**: 2026-08-18
**Operator ask**: "Review the training pipeline the same way we reviewed the
inference pipeline" — census the training tools the public and research labs
actually use, map OUR live training capability against that census, name the
gaps, then the impossible-knobs question (training edition), with per-item
rigor matching the inference census.

**Evidence rule**: every claim about our code cites live code at file:line.
Docs are stale by default; where a doc disagrees with git, git wins and the
doc is named as the defect. Reference pins: `gradus` @ `012d411`, `radix` @
`cebdaac28`, `hosts` @ `a6c8129`, `examples` @ `1dae31b`, `~/work/llama.cpp`
@ `c8e03ce81`. External-tool facts are web-sourced with version/date cited;
they are landscape evidence, not policy. The archived GPU-training campaign
(`radix-verify/docs/archived/gpu-training-lowering/`, accepted stages 0–7,
M5 exit gate 2026-08-09) is cited as history — its accepted surfaces are
verified against live code below before being claimed.

---

## 1. Grounding summary (what is actually live)

Verified 2026-08-18, in the order the task names.

1. **Gradus training tier is real but small.** 33 modules with a layered
   autograd spine: `gradus:gradient` (the ONE companion-call entry),
   `gradus:loss`, `gradus:optimize` (SGD only), `gradus:train` (steps,
   schedules, RNG, dropout, checkpoint), `gradus:metrics`, and `gradus:data`
   (**stub** — `docs/module-map.md:41` says so honestly; `src/data.fab` has
   no functions, only the facade header declaring future `data/batch` and
   `data/token` leaves at `data.fab:10-11`).
2. **Reverse-mode AD is a compile-time transform, not a runtime tape.** AIR's
   charter is exactly two transforms — "AIR's mission is **autodiff and
   fusion only**" (`radix/docs/design/air-dialect.md:6,24,56-58`, shipped
   2026-07-26 under the mir-autograd campaign). Source functions annotated
   `@ radix backward "name"` (`gradus/src/gradient.fab:224-228`,
   `gradus/src/gradus.fab:233-235`) get a compiler-generated backward
   companion through `radix-air/src/reverse_ad/` (3,417 lines:
   `transform.rs`, `vjp.rs` 1,733 lines, `validate.rs`, `replay.rs`) wired by
   `radix-module/src/driver/mod.rs:2084-2141` (snapshot collection from
   `analysis.radix_lanes.iter_backward()`). The companion passes a
   validation chain before installation: AIR-to-MIR backward proof, MIR
   result contract, gradient-check admission
   (`radix-air/src/air_to_mir_backward_proof.rs` 493 lines,
   `mir_backward_result_contract.rs`,
   `gradient_check_admission.rs` 653 lines; chain invoked at
   `driver/mod.rs:2202-2216`), a fusion pass runs on the companion body
   (`driver/mod.rs:2160-2166`, `radix-air/src/fusion.rs` 445 lines), and the
   companion MIR merges into the lowered program with a
   `LosslessMirCompanionEntry` carrying selected inputs/outputs and
   device-residency (`driver/mod.rs:2218-2236`).
3. **The companion ABI is fixed**: `backward(args..., nil(), upstream) →
   iuncta(...)` — the vacuum-residual `nil()` (`gradient.fab:209-215`) plus
   cotangent seed; proven at MLP scale (6-slot tuple, `gradus.fab:225`) and
   BERT-tiny scale (21-slot destructure over an 18-trainable-parameter set,
   `gradient.fab:44-49`).
4. **Gradients are device-real with an ABI.** Generated backward emits
   `MirIntrinsic::Gradient` ops (`MirGradientOp::Create | Accumulate | Read
   | Zero`, `radix/crates/radix-mir/src/gradient.rs:5-10`) that the LLVM
   backend lowers to `__faber_rt_v1_gradient_{create,accumulate,read,zero}`
   calls (`radix/crates/radix-mir-llvm/src/gradient.rs:39-59,70-80`; symbols
   in `radix/crates/radix-host-abi/src/…:109-112`), and the FMIR runner
   evaluates the same four ops in-process as Value carriers
   (`radix/crates/radix-mir-runner/src/runtime.rs:315-360`). The host ABI
   today is **f32-only** — the runner comment says so outright
   (`runtime.rs:356-358`, "the host's f32-only ABI restriction") even though
   `gradient create` carries a `kind` argument that anticipates widening.
5. **A real, executed, converging training loop runs in the test ladder.**
   `radix/crates/radix-program/src/mir/lane_test.rs:526-568`
   (`package_mir_training_loop_mlp_runs_on_fmir_lane`) copies
   `gradus/exempla/training-loop-mlp` and runs the full package on the FMIR
   lane (in-memory interpreted package MIR): 100 steps, 4×4 two-layer MLP,
   lr 0.1, asserting the trajectory against six f64 oracle pins
   (`PML4_PINS`, `lane_test.rs:516-523`, same pins as
   `gradus/src/train.proba` PML4-U6) within 5e-4 and convergence ratio
   < 0.1. Stage 4b (`cargo test --workspace`, `radix/scripta/test:167`)
   executes this — it is real running training-loop code, CPU-interpreted.
   The exemplum itself (`gradus/exempla/training-loop-mlp/src/main.fab`,
   365 lines) composes schedule→optimizer binding, shared forward +
   compiler companion gradients, per-parameter gradients with identity +
   generation, optimizer steps, per-step metrics, and a checkpoint
   round-trip.
6. **GPU training was proven at BERT-tiny scale and archived.** The
   gpu-training-lowering campaign (radix-verify, status **done**,
   `CAMPAIGN.md:3-9`) accepted stages 0–7: MLP and BERT-tiny
   forward/backward/optimizer executed on Metal (M5 Max) and CUDA (RTX 5070)
   through the ordinary `faber run --backend metal|cuda` path with
   activations, gradients, optimizer state, and updated parameters
   device-resident and readback only at declared observation points
   (`CAMPAIGN.md:40-46,58`). Heterogeneous gradient extents were proven on
   devices (`examples/training/hetero-backward/src/hetero_backward.fab:1-45`).
   Stage 8 (competitive measurement/tuning) was explicitly *not* run —
   handed to successor work (`CAMPAIGN.md:3-4`). **No throughput claim for
   training exists anywhere; none is made here.**
7. **The dense transformer model is inference-only.** `gradus/src/model/
   dense.fab` has **zero** `@ radix backward` annotations and no `@ radix
   lane`/`@ nucleum` markers — the GGUF-materialized model (the thing we
   actually run for inference) has no training path. Trainable models today
   are hand-fixed shapes in `gradus/src/train.fab` (linear 2×2, MLP 4×4,
   BERT-tiny 8-dim).
8. **Hosts compute surfaces are inference-oriented.** `hosts/crates/
   host-kernel/src/lib.rs` (checked, transport-neutral provider routing),
   `host-native/src/lib.rs` (bounded native dispatch, 16 workers / 256
   queue), `host-coordinator/src/partition.rs:95-122` (byte ledger with KV
   budget classes). A grep for gradient/training surfaces across
   `hosts/crates` finds none — training device execution lives in radix
   backends + host ABI, not in hosts.
9. **llama.cpp finetune reference** (`~/work/llama.cpp` @ `c8e03ce81`):
   `examples/training/finetune.cpp` is a 100-line driver over `ggml-opt` —
   full-model FP32 finetuning ("technically functional … very much WIP",
   `examples/training/README.md:3`), forced `load_mode = none` for writable
   weight pointers (`finetune.cpp:28-32`), **forced F32 K/V cache because
   OUT_PROD lacks F16 support** (`finetune.cpp:33-39` — a hard
   dtype-vs-backward-op coupling), optimizer set {ADAMW, SGD}
   (`ggml/include/ggml-opt.h:78-81`, "only ADAMW needs m, v momenta per
   parameter tensor" `:128`), dataset/epoch/val-split loop via
   `ggml_opt_epoch` (`finetune.cpp:66-96`), LoRA adapters as a separate
   mechanism (`common/common.h:518`, `src/llama-context.h:122-124`,
   `src/llama-adapter.cpp`), and the finetuned model saved back to GGUF
   (`finetune.cpp:97`).

---

## 2. Tool census (who trains what, with what)

Landscape verified by web research 2026-08-18; versions/dates cited per row.
Audience split: **public** = individual/local finetuning; **lab** = research
or production pretraining/fine-tuning at scale.

| Tool | Audience | Paradigm | What it optimizes | Version / date |
| --- | --- | --- | --- | --- |
| HF Transformers Trainer + Accelerate + TRL | public (default stack) | Python eager loop; Accelerate wraps DDP/FSDP/DeepSpeed; TRL adds SFT/DPO/GRPO | ecosystem breadth, model coverage, checkpointing/logging conventions | Transformers v5 (first major in 5 years, Dec 2025; ~5.14–5.15 mid-2026); v5 PyTorch-only |
| PyTorch FSDP2 (`fully_shard`) | public→lab | DTensor dim-0 per-parameter sharding; HSDP via 2D mesh; sharded state dicts + DCP | memory (ZeRO-style sharding) at framework level, composability | prototype in 2.4 (2024), refined through 2.6 (early 2025); core API stable, used by TorchTitan |
| DeepSpeed (ZeRO) | lab | JSON-config ZeRO stages 1–3, CPU/NVMe offload (ZeRO-Offload/Infinity), Domino TP engine | memory ceilings (100B+ params), offload, 3D parallelism | 0.16.0 Nov 2024 … 0.16.9 May 2025; 0.17.0 Jun 2025 … 0.17.6 Sep 2025; SuperOffload 0.18.0 Oct 2025 |
| Megatron-LM / Megatron-Core | lab (pretraining) | PyTorch library of parallelism building blocks: TP/PP/DP(FSDP)/EP/CP, comm overlap, FP8, distributed optimizer | throughput at cluster scale (MFU ~47–50% on H100; 462B on 6,144 H100s) | MCore 0.x series, latest 0.18.2 Jul 2026; dev moved to public GitHub Dec 2025 |
| torchtune | public→lab | PyTorch-native hackable recipes, YAML + `tune` CLI; LoRA/QLoRA/full, DPO/GRPO, QAT, multi-node | memory efficiency, hackability without abstraction tax | **maintenance mode 2025**; last stable 0.6.1 Apr 7 2025 |
| Axolotl | public→lab | YAML-driven wrapper over HF/PEFT/TRL; sample packing, FSDP2/DeepSpeed, ring-attention, expert parallelism | reproducible configs, long context, scale-out | active 2025–2026 (axolotl-ai-cloud/axolotl) |
| Unsloth | public (single GPU) | hand-written Triton kernels + custom autograd patches monkey-patched onto HF models | single-GPU speed (~2×, 3× with Dec 2025 packing kernels) and VRAM (−50–70%) | launched Dec 2023; Dec 2025 release: fused QK RoPE + padding-free packing; multi-GPU preview late 2025 |
| LLaMA-Factory (LlamaFactory) | public | Web UI (LlamaBoard) + YAML over HF/TRL/PEFT; optional Unsloth backend | onboarding ease, 100+ model templates | active 2025–2026 (hiyouga/LlamaFactory) |
| MLX / mlx-lm | public (Apple) | array framework on unified memory + Metal; lazy graph evaluation; `mlx_lm.lora` | local finetuning on Apple Silicon (LoRA/QLoRA/DoRA/full) | mlx-lm v0.31+ series mid-2026 |
| JAX / Flax (NNX) / Optax | lab (TPU-first, DeepMind/Anthropic) | functional transformations (`jit`/`grad`/`vmap`/`shard_map`) over XLA compiler; Pallas kernels; MaxText at scale | compiler-driven fusion + SPMD sharding; determinism | active; Flax NNX the recommended API 2025; OpenXLA |
| **llama.cpp finetune** (in-repo reference) | public (local) | C++ ggml compute-graph training: ggml-opt AdamW/SGD, LoRA adapters, GGUF I/O | zero-dependency local full-model FP32 finetune; memory floor (LLaMA 3.2 1B in 24 GB) | @ `c8e03ce81` (2026); README self-describes as WIP |

Reading of the census (not a benchmark): the **public tier** optimizes
*friction and single-device memory* (HF Trainer defaults, Unsloth kernels,
MLX unified memory, llama.cpp's C++ memory floor); the **lab tier** optimizes
*sharded memory and cluster throughput* (FSDP2/ZeRO/Megatron). Every row —
including llama.cpp — ships AdamW-family optimizers, LoRA, a data pipeline,
and a checkpoint artifact. That is the bar for "a training pipeline."

---

## 3. Our-capability map (live code, file:line)

### 3.1 What exists and executes

| Capability | Surface (file:line) | State |
| --- | --- | --- |
| Reverse-mode AD, compile-time, from source annotation | `radix-air/src/reverse_ad/{transform,vjp,validate,replay}.rs`; driver `radix-module/src/driver/mod.rs:2084-2236` | **live**, with compile-time validation chain + companion fusion |
| Backward companion ABI (`backward(args…, nil(), upstream) → iuncta`) | `gradus/src/gradient.fab:209-228`, `gradus/src/gradus.fab:220-247` | **live** (MLP 6-slot; BERT-tiny 21-slot) |
| ONE gradient-call contract entry (identity + generation) | `gradient.fab:248-265` (`gradients_simple_loss`); `Gradient` class `:115`, `Gradients` bundle `:169`, staleness `obsolete` `:202` | **live** |
| Per-parameter gradient records: (owner, name, version) | `gradient.fab:110-134`; parameter identity `parameter.fab:190,243` | **live** |
| SGD optimizer state, fail-closed freshness/shape/trainable rules | `optimize.fab:258` (`SgdState`), `:361` (`Sgd`), `step` `:467-493` (param' = param − lr·grad), validation `:310-333` | **live** — **SGD only; no momentum, no Adam family, no weight decay, no clipping** |
| Optimizer wire: versioned schema, exact round-trip | `optimize.fab:505-570` (state), `:576-621` (whole optimizer), schema `"1.0.0"` `:116` | **live** |
| Fixed-shape train steps (linear 2×2, MLP 4×4, BERT-tiny linear + LN) | `train.fab:62,80,110,152` | **live** (library-to-library calls execute on FMIR since radix `43c0102ba`; train/optimize proba executes 90/90; BERT-tiny 12-tuple calls remain deferred to radix need `0ef139c3`) |
| LR schedule: warmup→cosine (constant when vertex=end) | `train.fab:307-430` (`Schedule`, `construct_schedule`, `scheduled_rate`) | **live** — one schedule family only |
| Deterministic RNG + dropout mode | `train.fab:568-716` (`Seed`/`Draw`/`next_f32`, `dropout` `:684`, seed wire `:716`), Mode discipline/estimate `:433-495` | **live** |
| Checkpoint: optimizer wire + RNG + epoch/step, exact round-trip | `train.fab:787-870` (`Checkpoint`, `serialize_checkpoint` `:825`, `deserialize_checkpoint` `:849`) | **live** — optimizer/RNG only; **no model-weights artifact** |
| Losses: `mse`, `cross_entropy` + fixed-shape MSE rows | `loss.fab:264,306,379,389,399` | **live** |
| Metrics: `accuracy`, `Metric` | `metrics.fab:121,193,211` | **live** |
| Parameters: identity, mutation (version bump), registry, wire | `parameter.fab:243,393,416,529` | **live** |
| Device gradient handles (create/accumulate/read/zero) | MIR intrinsic `radix-mir/src/gradient.rs:5-10`; LLVM `radix-mir-llvm/src/gradient.rs:39-80`; host ABI `radix-host-abi/src/…:109-112`; runner `radix-mir-runner/src/runtime.rs:315-360` | **live**, **f32-only host restriction** (`runtime.rs:356-358`) |
| Executed converging loop (stage 4b) | `radix-program/src/mir/lane_test.rs:526-568` over `gradus/exempla/training-loop-mlp` | **live** (CPU, FMIR interpreted, f64-pinned) |
| FD gradient oracle methodology | `gradus/exempla/gradient-seam{,-nolib}/README.md` (central difference, eps 1e-5, per-element) | **live** methodology |
| GPU training proof (MLP + BERT-tiny, Metal + CUDA, device-resident) | archived campaign `radix-verify/docs/archived/gpu-training-lowering/CAMPAIGN.md:3-9,40-46`; fixtures `examples/training/{mlp,bert-tiny-fragment,hetero-backward,device-summa*}` | **accepted 2026-08-09**, archived; no perf numbers ever recorded (stage 8 not run) |

### 3.2 What is aspirational or absent (honesty list)

| Claimed/expected | Reality | Evidence |
| --- | --- | --- |
| "optimizers (SGD, Adam)" | Adam **does not exist** anywhere in gradus; only `SgdState`. The gradus.fab import comment overstates the inventory — a doc-vs-code defect (module-map is honest: "SGD optimizer state", `docs/module-map.md:35`) | `gradus/src/gradus.fab:23` vs `optimize.fab` (no Adam), `docs/module-map.md:35` |
| Data loading | `data.fab` is a stub: declared future leaves, zero functions | `gradus/src/data.fab:10-15`; `docs/module-map.md:41` |
| Training the real model (GGUF dense transformer) | `dense.fab` has no backward annotation, no trainable-parameter bridge; trainable surfaces are hand-fixed shapes in `train.fab` | `gradus/src/model/dense.fab` (0 hits for `radix backward`) |
| Mixed-precision gradients / grads in F16/BF16 | host ABI is f32-only; `kind` arg reserved but unexercised | `radix-mir-runner/src/runtime.rs:356-358` |
| Gradient accumulation / clipping / weight decay | none of the three exist in `optimize.fab`/`train.fab` | grep-negative |
| LoRA / PEFT | none | grep-negative |
| Distributed anything (DP/TP/PP/FSDP/ZeRO) | none; multi-device is a separate campaign frontier (`docs/factory/gpu-inference-multi-device/`) | — |
| Model-weights checkpoint artifact (finetuned model out) | only optimizer-state + RNG wire; llama.cpp writes a finetuned GGUF (`finetune.cpp:97`) | `train.fab:787-870` |
| Training throughput claims | none anywhere; stage 8 (competitive measurement) never ran | archived `CAMPAIGN.md:3-4` |

---

## 4. Gap matrix (ranked by severity)

Severity: **P0** = blocks any honest "training pipeline" claim; **P1** =
blocks parity with the public-tier census tools; **P2** = blocks lab-tier
parity; **P3** = adjacent surface, not blocking.

| # | Gap | Severity | vs census | Notes |
| --- | --- | --- | --- | --- |
| G1 | **No trainable real model** — the GGUF dense transformer (`dense.fab`) cannot be trained; only fixed-shape toys (2×2/4×4/BERT-tiny-8d) | **P0** | every tool trains real architectures | the single biggest gap; see wave T3 |
| G2 | **No data pipeline** — no batching, shuffling, tokenized-corpus streaming, val split | **P0** | all tools (even llama.cpp: `common_opt_dataset_init`, `val_split`, `finetune.cpp:66-80`) | `data.fab` stub; tokenizer module exists (`src/tokenizer.fab`) but is not wired to training |
| G3 | **Optimizer breadth: SGD only** — no AdamW (the universal default), no momentum/weight-decay, no 8-bit | **P0** | all census rows incl. llama.cpp (`ggml-opt.h:78-81`) | SGD-with-freshness-rules is proven; AdamW is the recognized next admitted row (campaign batch-by-default posture, `optimize.fab:30`) |
| G4 | **No finetuned-model artifact** — checkpoints carry optimizer/RNG only; nothing writes updated model weights out (GGUF or otherwise) | **P0** | all tools produce a usable finetuned artifact; llama.cpp → GGUF (`finetune.cpp:97`) | serialize.fab exists (`src/serialize.fab`) but no model-weights training checkpoint |
| G5 | No gradient accumulation, no clipping, no weight decay | **P1** | standard in every trainer | blocks realistic batch dynamics and stability |
| G6 | No mixed-precision training (BF16/F16 params or grads; loss scaling) | **P1** | standard (bf16 default; FP8 in Megatron/TE) | our f32-only gradient ABI is the explicit blocker (`runtime.rs:356-358`) |
| G7 | No PEFT/LoRA | **P1** | Unsloth/LLaMA-Factory/MLX/llama.cpp center on it | Parameter + Registry seam (`parameter.fab:416`) is a natural carrier |
| G8 | Scheduler breadth: one warmup-cosine family | **P1** | dozens via Optax/Transformers | `Schedule` is a value type — extension is additive |
| G9 | No flash attention in training (scores materialized; `CausalMaskedSoftmax`) | **P1** | FA2/3 standard for long-context training | shared with the inference gap list (inference doc §8.1-1); training amplifies it (backward doubles it) |
| G10 | No activation checkpointing (recompute) | **P2** | standard memory lever everywhere | compile-time backward memory planning (§5-K1) is our alternative angle, but recompute remains unexplored |
| G11 | No distributed training (sharding/TP/PP/EP) | **P2** | FSDP2/ZeRO/Megatron define the lab tier | multi-device campaign owns the frontier; training mesh is a post-M3 decision (archived `CAMPAIGN.md:30-34`) |
| G12 | No eval harness (val loss, held-out perplexity) | **P2** | llama.cpp evaluates post-finetune perplexity; all trainers log eval | `metrics.fab` has loss/accuracy primitives only |
| G13 | No post-training methods (DPO/GRPO/reward) | **P3** | TRL/Axolotl/Unsloth ship them | out of scope until G1–G4 close |
| G14 | No throughput evidence for training at all | **P2** (evidence, not capability) | stage 8 never ran | any perf claim in §6 is mechanism, never evidence |

---

## 5. Impossible-knobs census (training edition)

The operator's question: which tuning knobs/concepts are **structurally
impossible** in the census tools but **natural for us**? Same per-item rigor
as the inference census: why the block is architectural (cited), what it
buys, which existing seam it rides, cost band. Each item is **validated** or
**discarded** against evidence — including honest counter-evidence where a
census tool partially closes the gap (JAX/XLA and torch.compile are
compilers; pretending otherwise would be a false gate).

Legend: cost band S ~50–150k tokens, M ~150–400k, L ~400k–1M (charter effort
bands). Value-per-cost ranking at the end.

### K1 — Compile-time backward memory planning, fail-closed
- **Why architectural**: in PyTorch, the autograd engine allocates gradient
  buffers at runtime through the caching allocator; peak memory is discovered,
  not declared — OOM is the failure mode, and `torch.cuda.max_memory_allocated`
  is the observability. torch.compile/CUDA graphs staticize *some* buffers
  after capture, but the allocation policy is a runtime allocator's, not a
  checked contract; FSDP2/ZeRO manage *sharding* of params/grads, not a
  per-step declared workspace budget. JAX/XLA is the honest near-peer: XLA
  does static buffer assignment at compile time — but it is best-effort
  internal scheduling, not an admitted, fail-closed byte budget a user can
  reason against. In our stack the differentiation graph, shapes (type-level
  facts above the AIR fork — `air-dialect.md:56-64`), and the companion MIR
  are all compile-time objects; a backward-workspace ledger can be *computed,
  budgeted, and rejected* at plan time exactly like the inference partition
  ledger (`hosts/crates/host-coordinator/src/partition.rs:95-122`).
- **What it buys**: training-step admission that cannot OOM — "this model +
  this batch fits, here is the receipt" — which is precisely the operation
  llama.cpp finetune users do by hand ("Stories 260K and LLaMA 3.2 1B seems
  to work with 24 GB", README). Also enables overlap planning (grad readback
  vs next forward) with declared lifetimes.
- **Seam it rides**: `LosslessMirCompanionEntry` device-residency facts
  (`driver/mod.rs:2218-2236`), kernel_plan constants pattern
  (`radix-mir/src/kernel_plan/plan.rs:4-24`), hosts partition ledger shape.
- **Cost band**: M. **VALIDATED** (unique in the *fail-closed contract* form;
  credit XLA for static assignment).

### K2 — Fused backward kernels generated, not hand-written
- **Why architectural**: the census's fused training kernels are artifacts of
  human effort: Unsloth's selling point is hand-written Triton backward
  kernels (launched Dec 2023, extended Dec 2025); Liger kernels are a
  hand-written library; Megatron fuses by custom CUDA. In PyTorch, every new
  fused op needs a hand-written autograd formula. In our stack the backward
  is *generated from the same AIR graph as the forward* and then fused by the
  compiler — the fusion pass literally runs on the companion body
  (`driver/mod.rs:2160-2166`, `fuse_companion`; OF-1/OF-2 typed elementwise
  plans are the carrier on main). A model op added to the differentiable set
  gets its fused backward without anyone writing a backward kernel.
- **What it buys**: elementwise-chain backward (residual adds, norms' scalar
  chains, dropout masks, rope projections) with one launch and one pass over
  memory; new-op differentiability scales with the op set, not with kernel
  authorship.
- **Seam it rides**: `radix-air/src/fusion.rs`, OF elementwise plans,
  reverse_ad op set.
- **Cost band**: already partially live; extending coverage per op family is
  S per family. **VALIDATED** — with the honesty caveat that our
  differentiable op set is currently small (elementwise/matmul/reduction
  families proven; softmax/LayerNorm VJPs landed at stage 6), while PyTorch's
  formula library is enormous. The *mechanism* is the advantage; the
  *coverage* is not yet.

### K3 — Whole-step device programs (zero dispatch between schedule and kernels)
- **Why architectural**: the public-tier stack runs a Python interpreter
  between optimizer and kernels: Trainer's loop, Python param iteration in
  the optimizer step (foreach/fused modes batch some of it), per-hook
  callbacks. Mitigations exist and must be credited: torch.compile +
  `reduce-overhead` CUDA-graph capture, Unsloth's compiled paths, MLX's lazy
  graph, and JAX's `jit` (fully compiled steps; `lax.scan` for the loop).
  llama.cpp has no Python at all. What remains impossible for the
  PyTorch-family tools is the *step itself as one admitted, versioned device
  program* including the optimizer update and generational freshness checks;
  we already emit exactly that shape (S6 BERT-tiny: forward + backward +
  update in the device program, parameters/optimizer state device-resident —
  archived campaign lock 3, `CAMPAIGN.md:44-46`).
- **What it buys**: step-time determinism of overhead; no host round-trips;
  the micro-benchmark Unsloth wins by patching kernels, we win structurally
  (mechanism only — G14: no measurement exists).
- **Seam it rides**: companion merge into lowered program
  (`driver/mod.rs:2218-2230`), device gradient ABI, `[device]` manifest
  packages.
- **Cost band**: live at toy scale; scaling it rides G1. **VALIDATED as a
  structural property; DISCARDED as "nobody else compiles"** (JAX/llama.cpp
  do; the PyTorch eager family cannot without capture workarounds).

### K4 — Generated-backward verification as a compiler gate (oracle-admission)
- **Why architectural**: PyTorch's `gradcheck` and JAX's checks are *tests a
  user opts into*; nothing in their pipelines refuses to emit an unverified
  backward. Our compiler validates every generated companion through a
  chain — AIR-to-MIR backward proof, MIR result contract, gradient-check
  admission (`radix-air/src/gradient_check_admission.rs`, chain at
  `driver/mod.rs:2202-2216`) — and the ecosystem around it has the FD
  central-difference oracle (`exempla/gradient-seam`, eps 1e-5) plus f64
  trajectory pins (`train.proba`, `lane_test.rs:516-523`) as the golden
  methodology.
- **What it buys**: a new differentiable op cannot silently produce wrong
  gradients; per-model golden rows extend to per-model gradient oracles
  (BERT-tiny's "every element of all gradient tensors + their norms" exit
  gate, stage-6 delivery). This is the strongest existing answer to the
  census's silent-wrong-gradient failure mode (a hand-written Triton
  backward that diverges from reference is a known Unsloth-class risk).
- **Seam it rides**: gradient_check_admission + FD oracle exempla + proba
  pins.
- **Cost band**: S per new model family to add oracle rows. **VALIDATED —
  uniquely ours.**

### K5 — Provable gradient freshness (generation/staleness as a checked contract)
- **Why architectural**: staleness bugs (applying a gradient computed against
  older parameters — the classic DDP/accumulation footgun) are undetectable
  in the census tools at the type level; they surface as silent divergence.
  Ours is fail-closed by construction: gradients carry the parameter's
  `version` at computation (`gradient.fab:131-134,190-202`), `optimize.step`
  rejects stale gradients before touching the parameter
  (`optimize.fab:473-475`, `StaleGradient`), and `parameter.mutate` bumps
  the generation (`parameter.fab:393`).
- **What it buys**: gradient accumulation (G5) becomes *safe by contract* —
  accumulate then apply with an explicit generation assertion, instead of
  hoping the engine did not step in between.
- **Seam it rides**: PML1-U5 parameter schema + U2 generation seam.
- **Cost band**: S to build accumulation on it. **VALIDATED — uniquely
  ours.**

### K6 — Checkpoint format as a fail-closed versioned contract
- **Why architectural**: the census's checkpoint surface is fragmentation —
  DCP vs `torch.save` vs ZeRO checkpoints (with `zero_to_fp32` conversion
  pain as a named release feature, DeepSpeed 0.16.0 notes) vs Orbax vs GGUF;
  unknown-schema handling is best-effort. Ours rejects unknown markers,
  schema versions, malformed fields, and out-of-range counters fail-closed
  (`optimize.fab:510-570,582-621`; parameter wire `parameter.fab:529-538`)
  with exact round-trip predicates. The contract discipline is the knob;
  the *content* is currently narrower than theirs (optimizer+RNG only — G4).
- **What it buys**: one artifact = model + optimizer + RNG + step with
  provenance digests (the wave-6 admission-manifest pattern from the
  inference doc), checkable rather than hopeful.
- **Seam it rides**: versioned wire pattern; wave-6 manifest schema.
- **Cost band**: M (G4 work) on top of an S-scale existing pattern.
  **VALIDATED as contract; content gap named.**

### K7 — Per-parameter mixed-precision gradients chosen at lowering
- **Why architectural**: in PyTorch, gradient dtype follows param dtype /
  autocast policy at runtime; llama.cpp's constraint is hardcoded — training
  *forces* F32 K/V because OUT_PROD lacks F16 (`finetune.cpp:33-39`). Our
  `gradient create(shape, rank, kind)` already carries a `kind` slot
  (`runtime.rs:352-358`) and the plan system already resolves
  storage×compute classes per tensor fail-closed at lowering (inference doc
  §3) — the same table could admit per-tensor gradient dtypes with derived
  envelopes.
- **What it buys**: bandwidth on the gradient stream (the largest
  intermediate of training) without whole-program precision loss.
- **Seam it rides**: gradient ABI `kind` arg + plan-class resolution.
- **Cost band**: M (host ABI widening = contract revision). **DISCARDED
  from "we have it" — honestly aspirational today** (f32-only host
  restriction, `runtime.rs:356-358`); kept as the highest-leverage *future*
  knob the architecture admits naturally and theirs does not.

### K8 — Deterministic replay of a whole training run
- **Why architectural**: PyTorch determinism is a settings surface
  (`use_deterministic_algorithms` + per-op gaps); JAX is deterministic by
  functional construction (credit it). Ours: deterministic RNG as a wire
  value (`train.fab:568-716`), exact checkpoint round-trips, compiled
  fixed-kernel steps, and f64-pinned trajectories — replay is a *checked
  property of the loop* (the resume round-trip is pinned in the exemplum),
  not a configuration.
- **What it buys**: bug reports that are runs; ablation studies that are
  diffable.
- **Seam it rides**: Seed/Draw + Checkpoint + proba pins.
- **Cost band**: live. **PARTIALLY VALIDATED — parity with JAX, stronger
  than PyTorch-family; not claimed as unique.**

### K9 — Kernel-level dead-gradient elision (sparsity known at compile time)
- **Why architectural**: an unused parameter's gradient in PyTorch is still
  computed/dispatched (or special-cased `find_unused_parameters` in DDP,
  which costs a sync); in ours, an unused selected parameter's gradient is
  an exact zero extent in the companion tuple, proven on devices with
  per-output bounds (`examples/training/hetero-backward/src/
  hetero_backward.fab:15-30`: grad_w[j] = 0 with no dispatch overrun).
  Frozen parameters never step (`Frozen`, `optimize.fab:476-478`).
- **What it buys**: MoE/partial-finetuning where most parameters receive no
  gradient — the dispatch elision is free.
- **Seam it rides**: companion selected-inputs facts (`driver/mod.rs:2105-2141`).
- **Cost band**: live at fixture scale. **VALIDATED** as a mechanism;
  unrealized at MoE scale.

### K10 — "No runtime graph capture" as a training knob
- **Why architectural**: CUDA-graph capture (`reduce-overhead`) is the
  census's *workaround* for dispatch overhead, with real constraints
  (static shapes, capture-safety, memory pools). We never capture: the
  program is emitted once, static by construction (static shapes are the
  language posture).
- **What it buys**: no capture-failure class of bugs; shape changes are
  recompiles with plans, not re-captures.
- **Seam it rides**: same as K3.
- **Cost band**: structural (nothing to build). **VALIDATED as a property;
  folded into K3 for ranking.**

### Value-per-cost ranking (validated items, highest first)

| Rank | Knob | Cost | Why this order |
| --- | --- | --- | --- |
| 1 | K4 generated-backward oracle gates | S per family | already-built machinery (admission chain + FD oracle); every other training move inherits its honesty |
| 2 | K5 freshness-contract accumulation | S | unlocks G5 (accumulation) safely on an existing seam; near-term user-visible capability |
| 3 | K2 generated fused backward | S per op family | compounds with every new op; the mechanism that makes G1's transformer backward cheap |
| 4 | K1 backward memory budget admission | M | unique contract form; depends on G1-scale models to matter, hence below the S items |
| 5 | K3+K10 whole-step device programs | rides G1 | already proven at toy scale; its value scales exactly with G1 |
| 6 | K6 checkpoint contract completeness | M | the contract exists; content (G4) is the cost |
| 7 | K9 dead-gradient elision | live mechanism | value realizes only at MoE/partial-finetune scale |
| 8 | K7 per-tensor gradient dtypes | M | highest future leverage but a contract revision + host work; honestly aspirational today |
| — | K8 deterministic replay | live | parity property, not a differentiator; never spend on it as one |

---

## 6. Wave-plan-shaped unit table (highest-value moves)

Sizing follows the house micro-unit precedent (one behavior family, ~3–6k
est tokens per unit, write-disjoint scopes, fail-closed negatives, first
failing oracle named). Ordering: close the P0 pipeline first, then the
unique-knob leverage. Nothing below touches the sibling seats'
`numeric-flexibility-performance.md` surfaces.

**Wave T1 — optimizer breadth (closes G3; K5 rides it).**

| Unit | Repo/scope | Done-when |
| --- | --- | --- |
| T1-U1 AdamW state slot + wire bump | gradus `src/optimize.fab` (`AdamState`: m, v, step, β1/β2/eps; schema `"1.0.1"`; unknown-schema rejection preserved; per-slot wire) | proba: construction validation + round-trip `adam_aequus` + unknown-schema negative green |
| T1-U2 AdamW step math (bias-corrected) | gradus `src/optimize.fab` (`step` overload; same fail-closed preconditions incl. `StaleGradient`) | proba: f64-oracle-pinned step pins (one parameter, one step); stale-gradient negative green |
| T1-U3 gradient accumulation | gradus `src/gradient.fab` + `optimize.fab` (accumulate-on-freshness: sums gradient records at equal generation; apply-then-bump) | proba: accumulate-2-then-step pin; mixed-generation accumulation fails closed |
| T1-U4 global-norm clipping | gradus `src/train.fab` or `optimize.fab` (clip over a `Gradients` bundle before step) | proba: clip pin vs f64 norm; empty-bundle negative |

**Wave T2 — data pipeline (closes G2).**

| Unit | Repo/scope | Done-when |
| --- | --- | --- |
| T2-U1 `data/batch` leaf | gradus `src/data/batch.fab` (deterministic shuffle over `train.Seed`; batch slicing of a token tensor; the declared leaf split at `data.fab:10-11`) | proba: shuffle determinism pin (same seed ⇒ same order); batch bounds negatives |
| T2-U2 tokenized-corpus adapter | gradus `src/data.fab` (corpus → token ids via existing `src/tokenizer.fab`; val split) | proba: round-trip + split-fraction negatives; small corpus pin |
| T2-U3 loop integration | gradus `exempla/` (a new exemplum consuming T2-U1/U2 with T1 optimizer: char-level corpus, one epoch, loss decreasing) | executed on the FMIR lane (stage-4b test pattern, `lane_test.rs:526` shape) with f64 trajectory pins |

**Wave T3 — trainable real model (closes G1; unlocks K3/K1 value).**

| Unit | Repo/scope | Done-when |
| --- | --- | --- |
| T3-U1 dense-model parameter bridge | gradus `src/model/dense.fab` + `src/parameter.fab` (materialized tensors exposed as `Parametrum` records with identity/version; frozen/trainable admission) | proba: registry identity pins; frozen-tensor step negative |
| T3-U2 differentiable training forward | gradus `src/model/` (a `@ radix lane "air"` training composition over the dense blocks — LM head + `loss.cross_entropy` — separate from the bare inference `forward`) | companion generates; `faber check` green; FD oracle rows on a 2-block tiny config |
| T3-U3 finetune exemplum | gradus `exempla/` (load tiny dense rung → N steps on T2 data → per-step metrics → checkpoint) | executed FMIR-lane test with f64 pins (loss decreases; gradient norms finite) |
| T3-U4 finetuned-model artifact (closes G4) | gradus `src/serialize.fab` + manifest (updated tensors written out beside optimizer wire; digests; fail-closed schema) | round-trip proba: artifact → reload → identical forward logits pin |

**Wave T4 — unique-knob leverage (K1; rides T3).**

| Unit | Repo/scope | Done-when |
| --- | --- | --- |
| T4-U1 backward-workspace ledger | radix `radix-air`/`radix-module` (sum gradient-tensor bytes + companion intermediates per step from the `LosslessMirCompanionEntry` facts) | unit test: ledger equals hand-computed bytes on the MLP + BERT-tiny fixtures |
| T4-U2 fail-closed admission | hosts `host-coordinator/src/partition.rs` shape or radix plan validation (reject infeasible step budget at plan time) | negative test: oversized batch rejected with the receipt naming the budget class |

**Wave T5 — precision + PEFT (G6/G7; K7 rides T5-U1).**

| Unit | Repo/scope | Done-when |
| --- | --- | --- |
| T5-U1 gradient ABI kind widening | radix host ABI + runner + LLVM (f16/bf16 gradient carriers, f32 accumulation; **contract revision — amendment §7-2**) | ABI round-trip tests; derived envelope on the MLP fixture |
| T5-U2 LoRA adapter parameters | gradus `src/parameter.fab` + model seam (A/B matrices as first-class parameters; frozen base weights — `Frozen` already supports it) | proba: LoRA-on-linear pin vs f64 oracle; base-weight mutation negative |

Estimated first-filing envelope (T1 + T2-U1): ~15–25k tokens, write-disjoint
from the sibling design-doc work and from R-PACK/OF waves (gradus-only
files).

---

## 7. Amendments needed (filed, never silent)

1. **`gradus/src/gradus.fab:23` "optimizers (SGD, Adam)"** — the Adam claim
   is false against live code (SGD only). Default recommendation: fix the
   comment to "SGD (AdamW: wave T1)" **and** file T1 — but either way the
   comment must not ship in a review as if true. (module-map.md is already
   honest; the defect is the source comment only.)
2. **Gradient ABI f32-only restriction** (`radix-mir-runner/src/
   runtime.rs:356-358`, host ABI symbols) — widening `kind` to f16/bf16
   (T5-U1) is a contract revision to the host gradient ABI, analogous to the
   inference doc's GI4 dtype amendment. Needs mind; default = adopt with
   f32 accumulation preserved.
3. **Optimizer wire schema bump** (`optimize.fab` `"1.0.0"` → `"1.0.1"` for
   AdamW slots) — versioned wire by design, but the bump and
   old-reader-rejects-new behavior should be an explicit filing note, not a
   silent format change.
4. **Training numeric-policy authority** — `numeric-policy.md v1.0.0` lives
   in the archived campaign tree (radix-verify); new training waves need its
   tolerance rows (1e-4/1e-4 gradient row, 5e-4 trajectory band) re-homed
   into a live owner (gradus docs or a radix factory goal) rather than cited
   from an archive. Default: re-home verbatim as part of T1-U2.

## 8. Not claimed

- No training **throughput** claim anywhere; stage 8 of the archived
  campaign never ran and this document adds no measurement.
- GPU-device training is cited from an **archived, accepted** campaign; its
  fixtures live in `examples/training/`, but this review did not re-execute
  a Metal/CUDA training run. The live executed evidence in this doc is the
  CPU/FMIR lane test (`lane_test.rs:526`).
- External-tool capabilities are landscape facts from vendor docs/releases
  (cited per row), not benchmarks we ran.
- K7 (per-tensor gradient dtypes) is explicitly **not** claimed as existing;
  K8 is explicitly **not** claimed as unique versus JAX.
- Distributed training (G11) is out of scope of every wave here; the
  multi-device campaign owns that frontier.
