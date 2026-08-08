# Delivery: PML7 — Training and inference capstones

**Goal**: `docs/factory/production-ml-library/CAMPAIGN.md` (PML7 gate — final)
**Status**: scoped 2026-08-08 — entry-gated; full P3 confirmation at gate by planner; Mind owns admission
**Repos**: gradus (library acceptance), examples (capstone apps), faber/hosts (NGAB cross-backend receipts)
**Predecessors**: accepted PML1–PML6; NGAB5/NGAB7 receipts (inference capstone)

## Phase Intent

One training app and one inference app consume **only public `gradus:*` modules**; CPU/reference results pass; the inference capstone also passes through the sibling native GPU executable campaign (NGAB5) on every admitted backend; clean-install receipts pin package and toolchain versions.

**Entry gate**: PML6 accepted + NGAB5 accepted (inference capstone). **Non-goals**: new library semantics; serving; deployment; external spend.

## Unit Graph

### PML7-U1 — Training capstone (public-only Gradus)
- **done_when**: one training application in `examples/` consumes only public `gradus:*` modules (grep proof: no non-public imports), converges per the PML4-U6 proof, and passes a clean-install run; CPU/reference results recorded.
- **write_scope**: `examples/` (training capstone), gradus docs (receipts). **est_work_tokens**: 12k–24k. **tool_latency**: medium.
- **dependencies**: PML4/PML6; examples repo convention.
- **parallel_children_considered**: parallel with U2 (disjoint apps).

### PML7-U2 — Inference capstone (public-only Gradus)
- **done_when**: one inference application consumes only public `gradus:*` modules, loads the admitted model via the capsule, and produces oracle-matching tokens; CPU/reference results pass; the SAME app runs through NGAB5's native GPU executable on every admitted backend (Metal + CUDA receipts from NGAB).
- **write_scope**: `examples/` (inference capstone), gradus docs (receipts). **est_work_tokens**: 12k–24k. **tool_latency**: high (NGAB cross-backend runs — named boundary, auditor-owned).
- **dependencies**: PML5/PML6, NGAB5/NGAB7.
- **parallel_children_considered**: none (capstone is the convergence proof).

### PML7-U3 — Clean-install + release receipts
- **done_when**: clean-install receipts pin package + toolchain versions for both capstones (temporary home, no sibling checkout); receipts use the PML0-U13 joint schema (repo, commit, dirty state, command, artifact hash, verdict); release checklist (PML6-U5) executed; support matrix + claim register final pass (no unsupported claims).
- **write_scope**: gradus/examples receipts, docs. **est_work_tokens**: 8k–16k. **tool_latency**: high (clean-install builds — named boundary).
- **dependencies**: U1, U2, NGAB7.
- **parallel_children_considered**: none (aggregate closeout).

## Parallelism

- U1 ∥ U2 (disjoint apps) → U3 (aggregate). Cross-campaign: PML7's inference capstone is the PML↔NGAB convergence (with NGAB5/NGAB7). RunPod/multi-device work is downstream (separate lanes) — never blocks PML7 local proof.
- **Phase gate**: U1–U3 done; both capstones public-only Gradus + passing; inference passes through NGAB on every admitted backend; clean-install receipts pinned; campaign ready to close + archive.

## Validation

```bash
cd gradus && ./scripta/check-source && ./scripta/check-compile
cd gradus && python3 ../radix/scripta/generate-factory-readme.py --factory-root docs/factory --check
cd gradus && ./scripta/check-factory-goal-status --fail-on error
```
Capstone + NGAB cross-backend runs at the named audit boundary (auditor-owned per Rule 6); one clean-install pass per capstone.

## Council Dispositions (applicable)

| Item | Mandate | Where |
| --- | --- | --- |
| C6 | Inference-product campaign stub drafted before PML5/NGAB5 convergence | U2 consumes the stub's direction (repo + request API) |
| C7 | Joint receipt schema | U3 receipts use PML0-U13 schema |
| cmo | "Substrate, not launch product" | U2 is the executable proof; the server story stays in the product campaign |

## Open Questions

- Which application repo supplies the inference capstone (routed to the inference-product campaign shell after PML0).
