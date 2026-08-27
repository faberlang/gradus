# Gradus Agent Instructions

**Workspace work mode.** Ordinary development is **direct** in this
checkout on `main`. Worktree packets under `../worktrees/<lane>/` are
optional Tugboat isolation. Do not stand up lanes unless the operator
asked. Container law: [`../AGENTS.md`](../AGENTS.md).

Gradus is the public Faber source library for `gradus:*` imports — automatic,
differentiation, loss functions, optimizers, neural-network primitives, and
training-loop mechanics. This repo owns `.fab` source under `src/`; Radix and
`faber` consume it through `FABER_LIBRARY_HOME`, usually the parent
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
| `gradus:math` | Tensor-aware math foundation (own copy; independent of Norma) |
| `gradus:tensor` | Tensor construction, shape/dtype, basic ops (plain values — not autograd-aware) |
| `gradus:gradient` | `@ radix backward` wrapper ergonomics; forward + companion gradient calls |
| `gradus:loss` | Loss functions (MSE, cross-entropy) |
| `gradus:optimize` | Optimizers (SGD) and learning-rate schedules |
| `gradus:nn` | Differentiable primitives: Linear, activation, norm, embedding, dropout |
| `gradus:attention` | Scaled dot-product attention, causal masking, multi-head |
| `gradus:mlp` | Two-layer MLP forward + training-path companion |
| `gradus:transformer` | Transformer block, positional encoding, output head |
| `gradus:train` | Training loop, metrics, checkpointing |
| `gradus:data` | Batching, shuffling, tokenization |
| `gradus:gradus` | Facade map only (no genera) |

Nested package dirs only with **≥2 modules** (prefer ≥3). A single nested file
is flattened to a top-level leaf (`gradus:optimize`, not
`gradus:optimize/sgd`).

Full map: [`docs/module-map.md`](docs/module-map.md). API shape:
[`docs/api-shape-policy.md`](docs/api-shape-policy.md). Target architecture:
[`docs/archived/gradus-ml-foundation/GOAL.md`](docs/archived/gradus-ml-foundation/GOAL.md)
(archived); live ML work is under `docs/factory/production-ml-library/`.

## Demos

Instructional and training demos live under `exempla/`. They exercise the
public `gradus:*` surface and feed gaps back into the library or into Radix
mir-swarm rungs, not grow workarounds.

## Rules

- Keep public modules under `src/**/*.fab`.
- Keep package tests as co-located `src/**/*.proba` (`name.fab` + `name.proba`).
- Keep instructional demos under `exempla/**/*.fab`.
- Do not add `@ externa` or `@ subsidia`.
- Optional genus fields use `sponte`.
- Prefer leaf imports; do not grow genera on the `gradus:gradus` facade.
- Prefer receiver methods on genera; free functions for constructors / scalars
  / generators only.
- Nested package directories need at least two leaves (prefer three+).
- Do not import from Norma or any sibling library. Gradus is self-contained.
- Never `importa` a `.proba` file; shared helpers stay in `.fab` modules.
- `@ radix backward` annotations live behind the `gradient` module wrapper, not
  leaked into every public function signature.

## Validation

```bash
./scripta/check-source
./scripta/check-compile
```

## Benchmarks

Benchmarks are pinned to the **radix + hosts + gradus triple**. Every
number attaches to three full commit SHAs and is reproducible from those
hashes alone: `scripta/bench materialize` checks out detached worktrees of
the three repos at explicit hashes into a scratch root outside all repos
and `build` makes a release `faber` from the pinned radix. A speed number
not carrying the triple is not a gradus benchmark. Operative method:
[`docs/benchmark-method.md`](docs/benchmark-method.md) (v1.1.0); goal law:
[`docs/factory/bench-harness/goal.md`](docs/factory/bench-harness/goal.md).

### Commands

```bash
./scripta/bench materialize --radix <sha> --hosts <sha> --gradus <sha>  # pin the triple into a scratch root
./scripta/bench build                                                  # release faber from the pinned radix
./scripta/bench run                                                    # no flags = stage 2 dev (the dev default)
./scripta/bench run --stage smoke|dev|rough|full                       # stage tokens ≡ 1|2|3|4; --full aliases 4
./scripta/bench run --label <label>                                    # explicit subset, repeatable; signal only
./scripta/bench capture                                                # dated 3-hash baseline (AC-gated, stage full)
./scripta/bench gate CURRENT_JSON [--baseline BASELINE_JSON]           # comparability wrapper → radix checker
./scripta/bench clean [--all]                                          # tear down worktrees + scratch root — always
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

- Home: `bench/baselines/` — dated 3-hash stems
  `baseline-YYYYMMDD-<r7>-<h7>-<g7>.json` plus same-stem `.md` receipt.
- **Append-only**: a re-baseline is a new committed file at a new triple;
  never edit, overwrite, or delete an existing baseline.
- Baseline of record:
  [`bench/baselines/baseline-20260827-re792964-hc9cfb5a-g536b7ab.json`](bench/baselines/baseline-20260827-re792964-hc9cfb5a-g536b7ab.json)
  (radix `e7929640` · hosts `c9cfb5a` · gradus `536b7ab`) with its
  same-stem receipt and the GB-U5 reproduction rider — gate PASS
  reproduced from the recorded triple alone.

### Environment identity and thresholds

- Every baseline and run records the full environment-identity metadata
  (machine, cpu/cores/memory/os/arch, triple SHAs, faber binary identity,
  protocol, power); a missing field voids the claim (benchmark-method §5).
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
