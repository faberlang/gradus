# Delivery: PML3 — Reusable forward models and architecture rows

**Goal**: `docs/factory/production-ml-library/CAMPAIGN.md` (PML3 gate)
**Status**: scoped 2026-08-08 — entry-gated; full P3 confirmation at gate by planner; Mind owns admission
**Repo**: gradus (`src/nn.fab`, `src/attention.fab`, `src/transformer.fab`)
**Predecessors**: PML1 (tensor/dtype/shape/parameter), late PML2 (parameter schema + capsule), accepted GPU-training proofs (read-only)

## Phase Intent

NN, attention, and transformer forward functions become composable, testable, and usable **with and without autograd** (forward-functions-first; no training-machinery dependency — PML3 must not require PML4). One training architecture row and the selected inference architecture row are qualified over the admitted parameter schema.

**Entry gate**: PML1 accepted; parameter schema (PML1-U5) available; may overlap late PML2 after the parameter contract lands.

**Non-goals**: training machinery (PML4); inference state/decode (PML5); backend fusion (Radix owns); autograd wrappers beyond what exists as proof (PML4 productizes).

## Unit Graph

### PML3-U1 — NN primitives production surface
- **done_when**: linear/gelu/layernorm (and any primitives the admitted rows need) are forward-only functions over the PML1 tensor surface with typed errors; provably independent of autograd (no gradient-path build on forward); per-architecture row tests vs the accepted GPU-training proofs (CPU reference).
- **write_scope**: `gradus/src/nn.fab`, tests. **est_work_tokens**: 10k–20k. **tool_latency**: low.
- **dependencies**: PML1-U1/U3/U5.
- **parallel_children_considered**: split per primitive family after the first accepted pattern (campaign split-on-boundary).

### PML3-U2 — Attention
- **done_when**: scaled dot-product attention with causal masking and RoPE integration for the admitted rows is forward-only, composable, oracle-checked (CPU reference vs GI2/pinned fixtures); attention semantics shared by training and inference.
- **write_scope**: `gradus/src/attention.fab`, tests. **est_work_tokens**: 10k–20k. **tool_latency**: low.
- **dependencies**: U1.
- **parallel_children_considered**: none (attention semantics indivisible); parallel with U3 (disjoint files) after U1.

### PML3-U3 — Transformer block
- **done_when**: a transformer block (attention + FFN + residual + norms) composes over the primitive surface, is forward-only, and matches the CPU oracle for the training row and the selected inference row; block is usable by both PML4 training and PML5 inference.
- **write_scope**: `gradus/src/transformer.fab`, tests. **est_work_tokens**: 10k–20k. **tool_latency**: low.
- **dependencies**: U2.
- **parallel_children_considered**: none (block cohesion); U2 ∥ U3 impossible — U3 consumes U2.

### PML3-U4 — Forward with and without autograd (shared-layer proof)
- **done_when**: one forward model composition runs identically (a) bare (inference path) and (b) through the existing compiler-generated backward companion (training path); no forward path builds a gradient tape; the shared-layer definition from PML0-U4 is implemented and tested.
- **write_scope**: `gradus/src/gradus.fab` (facade), tests. **est_work_tokens**: 8k–16k. **tool_latency**: medium (faber check on the facade).
- **dependencies**: U1–U3.
- **parallel_children_considered**: none — this is the phase thesis proof.

### PML3-U5 — Architecture rows qualified
- **done_when**: one training architecture row and the selected inference architecture row are qualified over the admitted parameter schema: composable, testable, oracle-matching, forward-only; support-matrix rows populated per PML0-U5 schema with evidence links.
- **write_scope**: `gradus/docs/factory/production-ml-library/` support rows, tests. **est_work_tokens**: 8k–16k. **tool_latency**: low.
- **dependencies**: U4, PML2-U3 (inference row model facts).
- **parallel_children_considered**: none (rows aggregate U1–U4).

## Parallelism

- Lane 1: U1 → U2 → U3 → U4 (serial spine).
- Lane 2: U1 → U5 (row qualification, parallel with U2–U4 where the row's primitives exist).
- Cross-campaign: runs beside NGAB1–NGAB4 (disjoint repos), GI3-8 (read-only), training capstone (examples), PML4 planning (planner may start lowering PML4 while PML3 implements — disjoint scopes, per Rule 5).
- **Phase gate**: U1–U5 done; forward functions composable + autograd-independent + oracle-matching; support rows populated; README regen + audit 0 findings.

## Validation

```bash
cd gradus && ./scripta/check-source && ./scripta/check-compile
cd gradus && python3 ../radix/scripta/generate-factory-readme.py --factory-root docs/factory --check
cd gradus && ./scripta/check-factory-goal-status --fail-on error
```
Unit-level: targeted oracle tests once per unit at closeout.

## Council Dispositions (applicable)

| Item | Mandate | Where |
| --- | --- | --- |
| Forward-without-autograd | PML3 must not require PML4 training machinery (cto: proceed — correct if identities shared) | U1/U4 enforce |
| R2 | Config values only with live oracle | U5 rows cite oracles (GI2/GPU-training proofs) |
| R3 | One-row narrowing extensible | U5 keeps support rows + capability descriptors extensible |

## Open Questions

- None phase-blocking (row choices flow from PML0/PML2 decisions).
