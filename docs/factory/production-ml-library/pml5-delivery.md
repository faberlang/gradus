# Delivery: PML5 — Production inference computation layer

**Goal**: `docs/factory/production-ml-library/CAMPAIGN.md` (PML5 gate)
**Status**: scoped 2026-08-08 — entry-gated; full P3 confirmation at gate by planner; Mind owns admission
**Repo**: gradus (`src/decode.fab`, `src/cache.fab`, `src/sampling.fab`, `src/generation.fab`)
**Predecessors**: PML2 (model/tokenizer admission), PML3 (forward rows), GI0–GI3 oracle + decoder contracts (read-only)

## Phase Intent

Decode, KV-cache, sampling, and generation configuration produce oracle-matching tokens for the admitted model over the **shared forward functions** (PML3). Gradus owns computation and logical state — not scheduling, continuous batching, HTTP, or physical residency (those are the product repo / NGAB). This is the semantic contract the future llama-server-like product maps its requests into.

**Entry gate**: PML2 + PML3 accepted. **Non-goals**: servers, HTTP, batching, scheduling, device handles, physical residency, performance claims (sibling NGAB owns executable evidence).

## Unit Graph

### PML5-U1 — Decode loop semantics
- **done_when**: one-token decode is an explicit public operation (token id + position in → logits out) over the forward row; prefill (multi-token) and decode paths share the same forward functions; reset/context-limit behavior explicit; oracle-matching logits per GI2 contract.
- **write_scope**: `gradus/src/decode.fab`, tests. **est_work_tokens**: 12k–24k. **tool_latency**: low–medium.
- **dependencies**: PML3-U3 (block), PML2-U4 (tokenizer identity).
- **parallel_children_considered**: none (decode semantics indivisible).

### PML5-U2 — KV-cache values and mutation rules
- **done_when**: KV cache is a typed logical value with declared mutation rules (append per position, generation tracking, reset); never split across units; cache identity key per MD-A9 precedent (model/version/execution config/tokenizer/prefix/positions/layer/dtype/layout); mutation is deterministic and testable; no device handle.
- **write_scope**: `gradus/src/cache.fab`, tests. **est_work_tokens**: 12k–24k. **tool_latency**: low.
- **dependencies**: U1, PML1-U5 (identity patterns).
- **parallel_children_considered**: none (KV mutation is a campaign never-split).

### PML5-U3 — Sampling
- **done_when**: deterministic sampling (seed + temperature + top-k + top-p + min-p + repetition penalty) produces reproducible token choices; greedy path exact; sampling is a pure function of logits + config + RNG state; tests cover each knob and their combination vs a pinned oracle.
- **write_scope**: `gradus/src/sampling.fab`, tests. **est_work_tokens**: 10k–20k. **tool_latency**: low.
- **dependencies**: U1.
- **parallel_children_considered**: split per sampling family after the first accepted (greedy → temperature → top-k/top-p → min-p → rep-penalty), each with oracle tests (R2: only admit values with a live oracle).

### PML5-U4 — Generation-configuration contract
- **done_when**: the versioned generation-config contract names supported values, defaults, validation, and deterministic mapping for at least: context length, prompt batch size, maximum generated tokens, seed, temperature, top-k, top-p, min-p, repetition penalty; **unsupported llama.cpp-style controls are explicit reject rows, never silently ignored**; contract is the single authority NGAB5 and the future product repo adapt (never a second authority).
- **write_scope**: `gradus/src/generation.fab`, tests (reject-row matrix). **est_work_tokens**: 10k–20k. **tool_latency**: low.
- **dependencies**: U2, U3, PML0-U9 (packet: config identity facts).
- **parallel_children_considered**: none (config is one contract); U5 consumes it.

### PML5-U5 — Reset, context limits, cancellation observation, determinism
- **done_when**: session reset (fresh state), context-limit behavior (reject vs truncate — explicit policy), cancellation observation points (cooperative checks in decode), and deterministic replay (same seed + input → same tokens) are public, tested behaviors; no server or device handle leaks into Gradus.
- **write_scope**: `gradus/src/decode.fab`, `gradus/src/generation.fab`, tests. **est_work_tokens**: 8k–16k. **tool_latency**: low.
- **dependencies**: U4.
- **parallel_children_considered**: split reset vs limits vs cancellation after the config contract; disjoint files.

### PML5-U6 — Oracle-matching token proof
- **done_when**: a bounded generation run (256 tokens, greedy + one seeded stochastic config) produces oracle-matching tokens against the GI0–GI2 pinned fixture/llama.cpp-derived oracle; divergence is recorded at the first token (never hidden by text-level similarity); reset/replay determinism proven.
- **write_scope**: gradus exempla + tests. **est_work_tokens**: 12k–24k. **tool_latency**: medium (bounded generation run).
- **dependencies**: U1–U5.
- **parallel_children_considered**: none (aggregate proof; feeds NGAB5).

## Parallelism

- Lane 1: U1 → U2 → U4 (spine).
- Lane 2: U1 → U3 (parallel with U2) → U4.
- Lane 3: U4 → U5 (parallel with U6's planning).
- Cross-campaign: PML5 runs beside NGAB4 (generic composite proof, disjoint repos); PML5 + NGAB4 → NGAB5 convergence is the first cross-campaign merge point (per campaign ordering graph). The generation-config contract is the adapter seam NGAB5 must consume (cpo/cxo: NGAB5 never a second authority). GI4+ persistent-decode work re-lowered into this phase's semantics (C1) — no duplicate KV/decode owner.
- **Phase gate**: U1–U6 done; oracle-matching tokens for the admitted model; reject rows enforced; factory status audit 0 findings.

## Validation

```bash
cd gradus && ./scripta/check-source && ./scripta/check-compile
cd gradus && ./scripta/check-factory-goal-status --fail-on error
```
Unit-level: targeted decode/sampling/oracle tests once at closeout.

## Council Dispositions (applicable)

| Item | Mandate | Where |
| --- | --- | --- |
| C1 | No duplicate KV/decode owner after GI4+ re-lowering | U1/U2 are the single logical decode/KV owner |
| C4 | Generation config identity is a packet fact | U4 references the packet revision; NGAB5 adapts |
| C8 | No device handle; config admission fail-closed | U4 reject rows, U5 no-handle rule |
| R2 | Config values only with live oracle | U3/U6 gate each knob on a pinned oracle |
| R7 | NGAB5 not a second config authority | U4 names itself the single authority |
| R4 | KV identity / principal handoff (future server) | U2 cache identity key matches MD-A9; product repo consumes |

## Open Questions

- Context-limit policy (reject vs truncate) — default: fail closed with an explicit config row (reject).
- Stochastic sampling defaults (seed/temperature/etc.) — defaults per GI0–GI2 fixture; operator confirms at closeout.
