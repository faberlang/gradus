# Delivery: PML4 — Production training layer

**Goal**: `docs/factory/production-ml-library/CAMPAIGN.md` (PML4 gate)
**Status**: scoped 2026-08-08 — entry-gated; full P3 confirmation at gate by planner; Mind owns admission
**Repo**: gradus (`src/gradient.fab`, `src/loss.fab`, `src/optimize.fab`, `src/train.fab`)
**Predecessors**: PML3 (forward rows), PML1 (tensor/parameter), accepted GPU-training receipts (read-only)

## Phase Intent

Losses, gradient calls, optimizer state, schedules, training/eval mode, checkpoint resume, metrics, deterministic seeds, and failure behavior compose publicly as a training layer **over the reusable forward functions** (PML3). A bounded workload converges and resumes reproducibly. May begin planning while PML3 implements (disjoint scopes); implementation after PML3.

**Entry gate**: PML3 accepted. **Non-goals**: model formats (PML2 owns); GPU lowering (Radix); serving; distributed training (future sibling campaign consumes MD foundations).

## Unit Graph

### PML4-U1 — Loss surface
- **done_when**: losses (per admitted rows: MSE + cross-entropy path) are public functions over the tensor surface with typed errors, deterministic seeds, and non-finite handling; oracle-checked against the accepted training proofs.
- **write_scope**: `gradus/src/loss.fab`, tests. **est_work_tokens**: 6k–12k. **tool_latency**: low.
- **dependencies**: PML3-U1, PML1-U2.
- **parallel_children_considered**: split per loss after the first accepted pattern.

### PML4-U2 — Gradient-call contract
- **done_when**: compiler-generated backward companions are invoked through one public contract (per-parameter gradients, identity + generation tracking); the contract is shared with the GPU-training lane's accepted facts; gradient values are oracle-checked.
- **write_scope**: `gradus/src/gradient.fab`, tests. **est_work_tokens**: 10k–20k. **tool_latency**: medium.
- **dependencies**: PML3-U4 (forward/backward pairing), PML1-U5 (parameter identity).
- **parallel_children_considered**: none (gradient identity indivisible per campaign rule).

### PML4-U3 — Optimizer state
- **done_when**: optimizer state (per-parameter, versioned, serializable — SGD first, then any admitted row) composes with the parameter contract; state mutation rules explicit; checkpoint round-trip preserves exact state.
- **write_scope**: `gradus/src/optimize.fab`, tests. **est_work_tokens**: 8k–16k. **tool_latency**: low.
- **dependencies**: U2, PML1-U5/U7.
- **parallel_children_considered**: none (one optimizer-state contract; batch optimizers after the first accepted — campaign batch-by-default).

### PML4-U4 — Schedules + train/eval mode
- **done_when**: schedules (lr, warmup) and train/eval mode (dropout/RNG policy) are explicit public controls with deterministic behavior; mode affects forward evaluation per the shared-layer rule (no hidden global state).
- **write_scope**: `gradus/src/train.fab`, tests. **est_work_tokens**: 8k–16k. **tool_latency**: low.
- **dependencies**: U3, PML3-U4.
- **parallel_children_considered**: parallel with U5/U6 after U3.

### PML4-U5 — Checkpoint resume + metrics + seeds
- **done_when**: checkpoint resume (state + RNG + epoch/step) is versioned and reproducible; metrics (loss/accuracy per step) are defined values with a deterministic contract; seeds make runs reproducible; failure behavior (interrupted resume) is explicit.
- **write_scope**: `gradus/src/train.fab`, `gradus/src/metrics.fab`, tests. **est_work_tokens**: 10k–20k. **tool_latency**: low.
- **dependencies**: U3, U4.
- **parallel_children_considered**: none (reproducibility is one contract).

### PML4-U6 — Bounded convergence + resume proof
- **done_when**: a bounded workload converges to the accepted training proof's target and resumes reproducibly (same seed → same trajectory); checkpoint/resume round-trip passes; deterministic-seed test green; no performance claims made (correctness gate).
- **write_scope**: gradus exempla + tests. **est_work_tokens**: 10k–20k. **tool_latency**: medium (training runs, bounded).
- **dependencies**: U1–U5.
- **parallel_children_considered**: none (aggregate proof).

## Parallelism

- Lane 1: U1 → U2 → U3 → U4 → U6 (spine).
- Lane 2: U3 → U5 (parallel with U4).
- Cross-campaign: PML4 runs beside NGAB1–NGAB4, GI3-8, PML5 (PML5 after PML2+PML3 — the two are parallel lanes per the campaign's ordering graph; PML4 training productization proceeds beside PML5/NGAB work after PML3). No hot-path sharing with radix/hosts/faber product code.
- **Phase gate**: U1–U6 done; bounded workload converges + resumes reproducibly; README regen + audit 0 findings.

## Validation

```bash
cd gradus && ./scripta/check-source && ./scripta/check-compile
cd gradus && python3 ../radix/scripta/generate-factory-readme.py --factory-root docs/factory --check
cd gradus && ./scripta/check-factory-goal-status --fail-on error
```
Unit-level: targeted convergence/resume tests once at closeout.

## Council Dispositions (applicable)

| Item | Mandate | Where |
| --- | --- | --- |
| Forward-functions-first | Training must not make forward depend on autograd | U2 invokes backward through the contract; U4 mode switches without global state |
| Never split | Checkpoint versioning, metric definitions, parameter identity | U3/U5 single-owner contracts |
| R2 | Config values only with live oracle | U6 convergence proof is the oracle gate |

## Open Questions

- Optimizer set for the admitted rows (SGD first; extend per row).
- Schedule defaults (operator/product, default: warmup + cosine per accepted training proof).
