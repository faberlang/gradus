# Delivery: PML1 — Tensor, dtype, shape, and parameter foundation

**Goal**: `docs/factory/production-ml-library/CAMPAIGN.md` (PML1 gate)
**Status**: scoped 2026-08-08 — entry-gated; full P3 confirmation at gate by planner; Mind owns admission
**Repo**: gradus (`src/math.fab`, `src/tensor.fab`, `src/gradus.fab`); no faber/radix/hosts write scope
**Predecessors**: PML0 accepted (U4 module DAG, U9 interface packet, U10 contract, U13 receipts); NGAB0 packet accepted (shared ABI facts)

## Phase Intent

Replace the fixed-shape proof surface with the production tensor/dtype/shape/parameter foundation that PML2–PML5 consume. Gradus describes mathematical values; Radix owns lowering; hosts own physical storage. This phase is the **common prerequisite for PML2–PML5** and runs in parallel with NGAB1–NGAB4 (disjoint repos).

**Entry gate**: PML0 closed (U4/U9/U10/U13 done, operator disposition on the tensor-API shape posture question). If PML1 must start before PML0 fully closes, only U1–U2 may begin on PML0's frozen facts.

**Non-goals**: model formats (PML2); forward architectures (PML3); training machinery (PML4); inference state (PML5); device handles, allocators, streams, backends (split out — Radix/hosts); performance work before correctness.

## Unit Graph

### PML1-U1 — Tensor public contract (core)
- **done_when**: `src/tensor.fab` exposes the production tensor surface (dtype + shape + value storage, construction, validation, element access) with typed errors; the PML0 proof-helper ledger's dispositions are attached (retire/admit/replace per row); a red-green test proves construction/validation/error paths.
- **write_scope**: `gradus/src/tensor.fab`, `gradus/tests/tensor_contract.fab` (or co-located `.proba` per the PML0 baseline decision).
- **validation**: `./scripta/check-source && ./scripta/check-compile`; targeted tensor test once at closeout.
- **est_work_tokens**: 15k–30k. **tool_latency**: low–medium (faber check, no cargo).
- **dependencies**: PML0-U4 (DAG), PML0-U9 (packet: typed values/layouts/mutation/lifetimes/errors).
- **parallel_children_considered**: none — the tensor core is the cohesion root of PML1; every later unit consumes it.

### PML1-U2 — Dtype system
- **done_when**: dtypes (f32/f16/i32/u8 + cast/round/serialize rules) are a versioned contract with explicit promotion/rejection tables; non-finite handling per the capsule rules (PML0-U14); tests cover cast, round, overflow rejection, serialization round-trip.
- **write_scope**: `gradus/src/dtype.fab`, tests. **est_work_tokens**: 10k–20k. **tool_latency**: low.
- **dependencies**: U1.
- **parallel_children_considered**: none (U1's type carries dtype); parallel with NGAB lanes (different repo).

### PML1-U3 — Shape system
- **done_when**: shape representation implements the PML0 posture decision (generic / generated-admitted / staged mix); broadcast/reshape/expand rules are explicit with error identity; bounds and ceiling checks per GI1 precedent (no unbounded allocation).
- **write_scope**: `gradus/src/shape.fab`, tests. **est_work_tokens**: 12k–24k. **tool_latency**: low.
- **dependencies**: U1, PML0-U9 (shape facts in packet).
- **parallel_children_considered**: none; parallel with U2? Only if the shape type is independent of dtype — otherwise serialize after U2. Default: after U2.

### PML1-U4 — Pure operation families (batch after first accepted pattern)
- **done_when**: one accepted operation family (elementwise) with construction/validation/error/serialization contracts; then batch remaining families (reduce, matmul, cast, concat/slice) on admitted shapes; every family has red-green tests and an error contract.
- **write_scope**: `gradus/src/math.fab`, tests. **est_work_tokens**: 8k–16k per family batch. **tool_latency**: low.
- **dependencies**: U2, U3.
- **parallel_children_considered**: split per family AFTER the first accepted pattern (campaign split-on-boundary); within a family, indivisible.

### PML1-U5 — Parameter identity and traversal
- **done_when**: parameters have explicit identity (name, dtype, shape, version, owner), mutation rules, and traversal order (trainable/frozen); serialization contract round-trips identity; no parameter identity split across units (campaign rule).
- **write_scope**: `gradus/src/parameter.fab`, tests. **est_work_tokens**: 8k–16k. **tool_latency**: low.
- **dependencies**: U2, U3.
- **parallel_children_considered**: none (identity must be one contract); parallel with U4 (disjoint files).

### PML1-U6 — Retire or admit proof-only helpers
- **done_when**: every `*_2x2/_4x4/_2x8` helper in the PML0-U3 ledger has its disposition executed (retired with a migration note, or admitted as an alias with a real caller); grep shows the retired set removed and admitted set documented.
- **write_scope**: `gradus/src/*.fab` per ledger rows. **est_work_tokens**: 6k–12k. **tool_latency**: low.
- **dependencies**: U3 (new surface exists), PML0-U3.
- **parallel_children_considered**: split per module (nn/loss/optimize/attention/transformer/train) after U3; disjoint files.

### PML1-U7 — Serialization contract
- **done_when**: tensor/dtype/shape/parameter values serialize to a versioned bytes format and round-trip; version rejection and migration policy are explicit (feeds PML6 package contract); tests cover round-trip + version rejection.
- **write_scope**: `gradus/src/serialize.fab`, tests. **est_work_tokens**: 8k–16k. **tool_latency**: low.
- **dependencies**: U2, U5.
- **parallel_children_considered**: none (one wire format); parallel with U4/U6.

## Parallelism

- Lane 1: U1 → U2 → U3 → U5 (serial spine — each unit consumes the previous).
- Lane 2 (after U3): U4 families, U6 per module, U7 — parallel, disjoint files.
- Cross-campaign: whole phase runs beside NGAB1–NGAB4 (disjoint repos), GI3-8 (disjoint — no shared schemas), training capstone (examples). No hot-path serialization with radix/hosts/faber product code; only the shared docs/factory README + status audit are touched at closeout (one regen, one audit run).
- **Phase gate**: U1–U7 done, check-source/check-compile green once, README regen + audit entrypoint 0 findings, proof-helper ledger dispositions executed. No release bump.

## Validation

```bash
cd gradus && ./scripta/check-source && ./scripta/check-compile
cd gradus && python3 ../radix/scripta/generate-factory-readme.py --factory-root docs/factory --check
cd gradus && ./scripta/check-factory-goal-status --fail-on error
```
Unit-level: the targeted test per unit, once at closeout (Cargo discipline — no full-suite runs).

## Council Dispositions (applicable)

| Item | Mandate | Where |
| --- | --- | --- |
| C4 | Interface packet revisable through PML1/NGAB1 — PML1 may surface packet corrections | U1/U3 done_when must record any packet drift as a need to Mind (not silent change) |
| C8 | Admitted-model capsule trust model (no raw bytes as trust anchor) | U2 non-finite/overflow rules feed the capsule; capsule itself is PML2 |
| R3 | One-row/one-shape narrowing must not hard-code into public API shape | U3/U4 keep admission + capability descriptors extensible; support rows, not hard-coded generics |
| R1 | Paper freeze precedes compiled proof — recheck at PML1 close | U7 serialization contract is the first compiled packet fact; flag drift to NGAB1 |

## Open Questions

- Tensor-API shape posture (generic vs generated-admitted vs staged) — answered by PML0; U3 implements it.
- First GGUF architecture/quantization row — deferred to PML2 (PML1 does not need it).
