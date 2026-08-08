# Delivery: PML6 — Production quality, performance, and release contract

**Goal**: `docs/factory/production-ml-library/CAMPAIGN.md` (PML6 gate)
**Status**: scoped 2026-08-08 — may begin after PML1; closes after PML4 + PML5; full P3 confirmation at gate by planner; Mind owns admission
**Repo**: gradus (`docs/`, `README.md`, package metadata, benchmark scripts)
**Predecessors**: accepted PML contracts; PML0 support-matrix baseline (U5) and claim register (U12)

## Phase Intent

API reference, examples, diagnostics, support matrix, compatibility policy, benchmark method, tolerances, regression corpus, package metadata, and release checklist **agree with live behavior** (zombie-doc discipline). No performance claim precedes the correctness gates.

**Entry gate**: may begin after PML1 (docs scaffolding); closes after PML4 + PML5. **Non-goals**: new semantics (PML1–5 own); release execution (faber/radix release protocol owns); capstones (PML7).

## Unit Graph

### PML6-U1 — API reference
- **done_when**: public `gradus:*` surface documented (every public symbol from the PML0-U2 inventory, post-PML1–5 changes) with signatures, errors, examples; doc-generation or a `--check` link test proves no undocumented public symbol (zombie-doc gate).
- **write_scope**: `gradus/docs/`, `README.md`. **est_work_tokens**: 10k–20k. **tool_latency**: low.
- **dependencies**: PML4/PML5 accepted surfaces; PML0-U2.
- **parallel_children_considered**: split by module after the first accepted section.

### PML6-U2 — Diagnostics + examples
- **done_when**: every public error has a code + issue identity with a diagnostic message; examples (minimal tensor → train → inference walkthroughs) run and match documented output; diagnostics locale-ready per workspace convention.
- **write_scope**: `gradus/src/` (diagnostic strings only), `gradus/exempla/`, docs. **est_work_tokens**: 8k–16k. **tool_latency**: low.
- **dependencies**: U1.
- **parallel_children_considered**: parallel with U3/U4.

### PML6-U3 — Support matrix + compatibility policy
- **done_when**: the PML0-U5 support-matrix schema is populated with every admitted row (formats, architectures, dtypes, quantizations, shapes, tokenizers, backends) + reject rows; compatibility policy (versioned: what breaks, what migrates) explicit; claim register (PML0-U12) updated so no row reads as product support without evidence.
- **write_scope**: `gradus/docs/factory/production-ml-library/` support rows, claim register. **est_work_tokens**: 8k–16k. **tool_latency**: low.
- **dependencies**: U1; PML0-U5/U12.
- **parallel_children_considered**: none (matrix is one contract).

### PML6-U4 — Benchmark method + tolerances + regression corpus
- **done_when**: benchmark method (exact commands, warmups, sample counts, hardware disclosure) and numeric tolerances are versioned; regression corpus (the admitted rows' fixtures) runs green; correctness gates pass before any speed number is published; speed claims stay CPU-reference-level (GPU evidence is NGAB's).
- **write_scope**: `gradus/bench/`, `gradus/tests/regression/`, docs. **est_work_tokens**: 10k–20k. **tool_latency**: medium (bounded benchmark runs).
- **dependencies**: U3; PML4-U6/PML5-U6 proofs.
- **parallel_children_considered**: none (one benchmark contract).

### PML6-U5 — Package metadata + release checklist
- **done_when**: package metadata (name, version, dependency pins, feature gates per the radix façade convention) agrees with live behavior; release checklist (docs, support matrix, claim register, receipts, clean-install) is a committed artifact the PML7 closeout and faber release protocol consume.
- **write_scope**: `gradus/Cargo.toml`-equivalent metadata, `gradus/docs/`. **est_work_tokens**: 6k–12k. **tool_latency**: low.
- **dependencies**: U1, U3.
- **parallel_children_considered**: parallel with U4.

## Parallelism

- Lanes: U1 → U2/U3/U4/U5 (parallel after U1). Cross-campaign: runs beside NGAB5–NGAB7 and the GI/MD/training lanes (disjoint). The claim register is shared with NGAB's register (one vocabulary, two repo files).
- **Phase gate**: U1–U5 done; docs/claims/behavior agree (zombie-doc gate); support matrix + compatibility policy committed; README regen + audit 0 findings.

## Validation

```bash
cd gradus && ./scripta/check-source && ./scripta/check-compile
cd gradus && python3 ../radix/scripta/generate-factory-readme.py --factory-root docs/factory --check
cd gradus && ./scripta/check-factory-goal-status --fail-on error
```
Regression corpus once at closeout.

## Council Dispositions (applicable)

| Item | Mandate | Where |
| --- | --- | --- |
| C5 | Claim register: no row reads as support without evidence | U3 updates the register |
| C7 | Joint receipts + scoped audit | U5 checklist consumes the PML0-U13 receipt schema |
| cmo | "Accepted/partial/in flight" never reads as product support | U3 support matrix qualifiers |

## Open Questions

- Release/version review happens here and at PML7 (campaign rule) — version policy decision lands with the faber release protocol owner.
