# Gradus Agent Instructions

**Workspace work mode.** Primary workflows run on GitHub: the work queue is
issues on `faberlang/gradus` and changes land by pull request into `main`.
Branch `peer/<topic>` off `origin/main`, push it, and open a PR — never the
`agent/` prefix (the pipeline owns it and would take the branch over).
`origin` is GitHub; the hub is a secondary `hub` remote. Worktree packets
under `../worktrees/<lane>/` are optional isolation; do not stand up lanes
unless the operator asked. Container law: [`../AGENTS.md`](../AGENTS.md).

Gradus is the public Faber source library for `gradus:*` imports — automatic,
differentiation, loss functions, optimizers, neural-network primitives, and
training-loop mechanics. This repo owns `.fab` source under `src/`; Radix and
`faber` consume it through `--library-home` (or `[paths] library_home` in
`faber.toml`; no `FABER_*` environment variable is read), usually the parent
`faberlang/` directory in local development.

Gradus is fully self-contained. It does not import from Norma or any other
sibling library. A Gradus user never needs to decide between `norma:*` and
`gradus:*` — if you need autograd or ML, import from Gradus; if you need plain
math, import from Norma. Duplication between them is intentional isolation.

GPU architecture follows the canonical public
[GPU Execution Architecture](https://github.com/faberlang/faber/blob/main/docs/gpu-execution-architecture.md).
Gradus owns device-neutral ML semantics, logical placement and sharding intent,
and all ML kernel source in Faber. Radix validates, specializes, and lowers
that source to target artifacts and explicit execution facts. Hosts owns
physical discovery, virtual-partition admission, binding, residency, launch,
synchronization, and readback. Do not put a permanent ML kernel body or a
silent CPU fallback in Radix or Hosts.

## Module layout (Norma / Triga style)

One `.fab` file → one import path. Nested dirs for packages.

| Import | Role |
| --- | --- |
| **Core value and type surface** | |
| `gradus:math` | Tensor-aware math foundation (own copy; independent of Norma) |
| `gradus:tensor` | Tensor construction, shape/dtype, basic ops (plain values — not autograd-aware) |
| `gradus:shape` | Shape system — production shape representation and rules |
| `gradus:dtype` | Dtype system — versioned dtype contract |
| `gradus:serialize` | Serialization contract — versioned bytes wire format |
| `gradus:storage` | Open-world encoded numeric storage |
| **Training surface** | |
| `gradus:gradient` | `@ radix backward` wrapper ergonomics; forward + companion gradient calls |
| `gradus:loss` | Loss functions (MSE, cross-entropy) |
| `gradus:metrics` | Defined metrics over the tensor value surface |
| `gradus:optimize` | Optimizers (SGD) |
| `gradus:schedule` | Warmup and cosine learning-rate schedules |
| `gradus:parameter` | Parameter identity and traversal |
| `gradus:nn` | Differentiable primitives, train/eval mode, and dropout |
| `gradus:mlp` | Two-layer MLP forward + training-path companion |
| `gradus:transformer` | Transformer block, positional encoding, output head |
| `gradus:calibration` | Residual-energy calibration bake |
| `gradus:checkpoint` | Checkpoint envelope and versioned save/load wire |
| `gradus:data` | Batching, shuffling, tokenization |
| `gradus:random` | Deterministic seed state, RNG draws, and serialization |
| **Attention, decode, and cache** | |
| `gradus:attention/rope` | RoPE configuration and attention error vocabulary |
| `gradus:attention/gqa` | Scaled dot-product, causal attention, RoPE apply, GQA multi-head |
| `gradus:decode_step` | Device kernel set for one decode step (rmsnorm, fused QKV/gate-up, RoPE, full + ring KV writes, attention, GEMVs, SwiGLU, bias add, argmax, topm) |
| `gradus:decode_token` | Record-typed single-token decode contract (`LayerWeights` / `SlotView` / `LayerParams` / `Workspace`) over `decode_step` |
| `gradus:decode` | Decode loop semantics (production inference computation layer) |
| `gradus:kernel` | Independently inspectable device entry inventory |
| `gradus:cache/kv` | KVCache, open encoded representations, append/extend/reset |
| `gradus:cache/identity` | CacheIdentity and identity wire |
| `gradus:cache/structure` | KVStructure, profiles, GI4 unions |
| `gradus:cache/session` | `SessionState` over `ExecutionSchedule` slots (`FullKvArena` / `RingKvArena`), transactional `SessionTxn` (`branch` / `txn_write_kv` / `commit_prefix` / `rollback`), per-slot `KvQuantConfig` |
| `gradus:cache/hybrid_arenas` | `ConvStateArena`, `RecurrentStateArena`, `HybridSession`, and journal-backed `HybridTxn` across KV + Conv + Recurrent arenas |
| **Weight admission and model assembly (issue #33 seams)** | |
| `gradus:model/schedule` | `ExecutionSchedule` — physical/visit/step separation, slot specs, `ArenaKind` |
| `gradus:model/safetensors` | Range-based Safetensors header inspection and multi-dtype admission |
| `gradus:model/gguf` | GGUF container parsing |
| `gradus:model/gguf_manifest` | GGUF v3 format-general manifest parser and pathless range seam |
| `gradus:model/bundle` | `ModelBundle` — pathless multi-member bundle contract |
| `gradus:model/artifact` | Pathless artifact identity for model-format inspection |
| `gradus:model/capsule` | Admitted-model capsule — typed model identity handoff |
| `gradus:model/config` | `ModelConfig` — fail-closed JSON parser for HuggingFace/MLX `config.json` |
| `gradus:model/tensor_directory` | `TensorDirectory` — cross-shard lookup, cross-role borrow, Slice admission |
| `gradus:model/linear_weight` | `LinearWeight` — per-module operator binding from `TensorDirectory` siblings |
| `gradus:model/tensor_payload` | Bounded per-tensor payload value and typed diagnostics |
| `gradus:model/tensor_view` | Typed tensor views over admitted payloads |
| `gradus:model/dequant` | CPU decoding of the currently supported GGML block types |
| `gradus:model/dense`, `dense_llama`, `dense_qwen2` | Dense model definitions resolved from `TensorDirectory` + admitted config |
| `gradus:model/moe`, `qwen35moe`, `qwen35moe_state` (+ `full_attn` / `linear_attn` / `schedule` / `session`) | MoE and Qwen3.5-MoE state families |
| `gradus:model/dense_load_static` | Test-only: co-located test for the typed-assembly `load` admit |
| `gradus:quant/q8_0`, `q5_0`, `q4_1`, `iq4_nl` | GGML block genera with host decoders |
| `gradus:quant/group_affine` | Group-affine quantized weight representation and device GEMV |
| **Generation and speculation** | |
| `gradus:generation/config` | GenerationConfig, GenerationError, acceleration policy |
| `gradus:generation/decoder` | Cursor, stop policy, decoder generate |
| `gradus:generation/dense` | DenseEngine and dense generate |
| `gradus:sampling` | Deterministic token sampling (greedy/sample, repetition penalty, temperature/top-k/top-p/min-p, explicit `Seed` RNG seam) |
| `gradus:speculative` | Candidate-provider seam (speculative-decode contract): adaptive-depth `AdaptiveBudget`, generalized `DrafterContext` |
| `gradus:context_lookup` | Deterministic context-lookup search contract |
| `gradus:draft_verify` | Draft-and-verify coordinator: PLD draft → `SessionTxn` branch/verify → `commit_prefix`/`rollback`, greedy-exact against the Disabled baseline |
| `gradus:receipt` | Versioned speculative-decode evidence receipt |
| `gradus:prepared_state` | Canonical prepared identity and typed prepared state |
| **Tokenizers** | |
| `gradus:tokenizer/identity` | Generic TokenizerIdentity structure and wire |
| `gradus:tokenizer/unicode` | Unicode categories and scanners |
| `gradus:tokenizer/bpe` | Tokenizer runtime, encode/decode |
| `gradus:gradus` | Facade map only (no genera) |

Package-map root files (`src/attention.fab`, `src/cache.fab`,
`src/generation.fab`, `src/tokenizer.fab`) re-export their nested packages.
Test-only modules: `src/generation_test.fab`, `src/model/dense_load_static.fab`
(`+++ faber test` only) and `src/test_util.fab` (shared test helpers).

Nested package dirs only with **≥2 modules** (prefer ≥3). A single nested file
is flattened to a top-level leaf (`gradus:optimize`, not
`gradus:optimize/sgd`).

## Inference architecture state (issue #33)

The flexible-inference-and-weight-architecture seams are largely landed on
`main`: weight admission and manifests (`model/safetensors`, `model/gguf`,
`model/gguf_manifest`, `model/bundle`, `model/config`),
`model/tensor_directory` + `model/linear_weight` operator binding, the quant
block genera (`quant/*`), the `model/schedule` `ExecutionSchedule` with
`cache/session` `SessionState`, transactional `SessionTxn`
(`branch` / `txn_write_kv` / `commit_prefix` / `rollback`) and the hybrid
`ConvStateArena` / `RecurrentStateArena` journal transactions
(`cache/hybrid_arenas`, issues #51/#92), and the record-typed decode path
(`decode_token` over `decode_step`). The speculative seam
(`speculative`, `context_lookup`, `generation/config`) is the consumer of the
transaction API. Still open: `NumericBlock` retirement (#6) and the
`prepared_state` arena wire v2 (#91).

This table is the authoritative map; [`docs/module-map.md`](docs/module-map.md)
predates the inference-seam landings and is historical. API shape:
[`docs/api-shape-policy.md`](docs/api-shape-policy.md). Target architecture:
[`docs/archived/gradus-ml-foundation/GOAL.md`](docs/archived/gradus-ml-foundation/GOAL.md)
(archived); live ML work is under `docs/factory/production-ml-library/`.

## Demos

Instructional and training demos live under `exempla/`. They exercise the
public `gradus:*` surface and feed gaps back into the library or into Radix
mir-swarm rungs, not grow workarounds.

## Rules

- Keep public modules under `src/**/*.fab`.
- Keep package tests in `+++ faber test` sections inside `src/**/*.fab` (or test-only `.fab` files with `+++ faber test` only).
- Keep instructional demos under `exempla/**/*.fab`.
- Do not add `@ externa` or `@ subsidia`.
- Optional genus fields use `sponte`.
- Prefer leaf imports; do not grow genera on the `gradus:gradus` facade.
- Prefer receiver methods on genera; free functions for constructors / scalars
  / generators only.
- Nested package directories need at least two leaves (prefer three+).
- Do not import from Norma or any sibling library. Gradus is self-contained.
- Keep test helpers inside `+++ faber test` sections or dedicated `.fab` modules.
- `@ radix backward` annotations live behind the `gradient` module wrapper, not
  leaked into every public function signature.

## Validation

```bash
./scripta/check-source
./scripta/check-compile
```

`faber test` runs the co-located `+++ faber test` cases on the CPU device
route (the package manifest pins `[device] device = "cpu"`: kernel cases
refuse the default `auto` device). Cases the JIT declines are **blocked by
name, never failed**; the CI workflow ratchets the expected blocked count in
`.github/workflows/ci.yml` — a run fails on any failed case or on blocked
count growth. Extend the ratchet when a fix unblocks cases; never weaken it
to hide a regression. Some cases stay blocked on known radix-side MIR gaps
tracked upstream (radix #2517, #2525–#2528); they unblock as radix lands
fixes.

## Benchmarks

Same law as unit tests: time the **current tree**. `./scripta/bench run`
uses the live sibling checkouts (HEAD of radix, gradus). A leftover
isolated snapshot is never auto-selected. Artifacts record the HEADs that
ran; they do not become the next run's input. If you want last week's
number, check out last week's repos. Operative method:
[`docs/benchmark-method.md`](docs/benchmark-method.md) (v1.1.0).

### Commands

```bash
./scripta/bench run                                                    # live HEAD, stage 2 dev
./scripta/bench run --stage smoke|dev|rough|full                       # stage tokens ≡ 1|2|3|4; --full aliases 4
./scripta/bench run --label <label>                                    # explicit subset, repeatable; signal only
./scripta/bench capture                                                # snapshot of *now* (HEAD), dated JSON + receipt
./scripta/bench gate CURRENT_JSON [--baseline BASELINE_JSON]           # comparability wrapper → radix checker
./scripta/bench materialize                                            # optional isolated HEAD snapshot
./scripta/bench build                                                  # release faber inside that snapshot
./scripta/bench clean [--all]                                          # tear down isolated snapshots
```

`run` with no stage flag is **stage 2 dev** — the operator's default dev
mode, never a full sweep.

### Stage ladder (two knobs: label breadth × repetition count)

| Stage | Tokens | Labels | Warmups/Samples | Wall | Grade |
| --- | --- | --- | --- | --- | --- |
| 1 smoke | `smoke` / `1` | 1 | 1/3 | ≤ 1 min | iteration signal |
| 2 dev **(default)** | `dev` / `2` | 2 | 1/3 | ~2–3 min | iteration signal |
| 3 rough | `rough` / `3` | all 7 | 1/2 | ~7–8 min | iteration signal |
| 4 full | `full` / `4` / `--full` | all 7 | 3/10 | ~35–40 min | **only gate-comparable shape** |

- Comparability is keyed on **protocol identity**: only stage full — 3
  warmups, 10 samples, all 7 manifest labels — is eligible as baseline
  capture or gate input. Lesser stages, `--label` subsets, and any
  protocol override are **iteration-signal only**.
- Per-case iterations K is fixed across the ladder; no lower stage's
  protocol exceeds 3/10.

### Power-state law (per row)

- Every result row carries `power_state` (`ac | battery | mixed |
  unavailable`) sampled at that row's execution; `metadata.power_state`
  is the start-of-run observation only. `metadata.power_class` is the run
  summary — the unanimous row class, else `mixed` with first/last
  recorded.
- Comparison stratifies per test by power class. **Cross-class is NOT
  COMPARABLE** — the gate refuses it, in the same refusal family as
  environment mismatch and lesser-stage protocol (exits 3–6), before the
  checker runs.
- Battery absolutes are depressed, never steady-state claims; a
  same-test **same-class ratio is signal even on battery** (perf-parity
  U7 soak precedent).
- The **first baseline capture is AC-gated** (ruling `ea4dd0a3`); a
  battery run is valid labeled evidence but not the first baseline.
  Non-macOS records `unavailable` and is not gate-comparable.

### Metrics

- Sole throughput metric: **t/s = unit-count / min(completion, cap)**,
  median across samples. `median_ms` stays the checker's gate quantity.
- Runtime caps are **safety circuit breakers only** — a capped sample
  records its valid t/s plus `capped: true`; never a metric, never
  pass/fail.
- Class (b) fixed-output-length benches (per-side expected token counts)
  do not fit this solo harness — they belong to the gradus-v-llama parity
  harness when one is ordered; the t/s and caps laws carry into it.

### Baselines

- Home: `bench/baselines/` — dated receipts that record the HEADs they
  ran. A receipt is a log, not a pin for the next `run`.
- **Append-only**: never edit, overwrite, or delete an existing baseline.
- Latest receipt:
  [`bench/baselines/baseline-20260827-re792964-hc9cfb5a-g536b7ab.json`](bench/baselines/baseline-20260827-re792964-hc9cfb5a-g536b7ab.json)

### Environment identity and thresholds

- Every run records machine, cpu/cores/memory/os/arch, the HEADs that
  ran, faber binary identity, protocol, power; a missing field voids the
  claim (benchmark-method §5).
- Gate default **10 %**; `BENCH_REGRESSION_THRESHOLD` overrides. Advisory
  until the operator wires it into merges. Never widen a threshold after
  an observation to force green (L21); a same-machine regression is
  recorded and investigated (L17), not suppressed.

Citations: `docs/benchmark-method.md` v1.1.0 · gpu-lessons
L1/L2/L4/L12/L13/L17/L21
(`~/work/ianzepp/skills/gpu-lessons/references/laws.md`) · perf-parity U7
soak receipt
([`../radix/docs/factory/perf-parity-baseline/evidence/2026-08-26-metal-m5max-soak-l2000/perf-parity-receipt-v1-2026-08-27-soak.json`](../radix/docs/factory/perf-parity-baseline/evidence/2026-08-26-metal-m5max-soak-l2000/perf-parity-receipt-v1-2026-08-27-soak.json)) ·
rulings `ea4dd0a3` (power), `1309af45` + `88895a02` + `d3cc0123`
(ladder), `46ab4e94` (taxonomy) · reproduction rider
[`bench/baselines/baseline-20260827-re792964-hc9cfb5a-g536b7ab-reproduction.md`](bench/baselines/baseline-20260827-re792964-hc9cfb5a-g536b7ab-reproduction.md).
