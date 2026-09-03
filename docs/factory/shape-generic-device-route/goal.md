# GOAL: shape-generic-device-route — Gradus is an AI library, not a SmolLM2 library

**Status**: active — U1 done; U2 first bag refused (wrong seam); U2 refiled on `use_package_compiler`
**Created**: 2026-08-27
**Rewritten**: 2026-09-03
**Campaign:** `—` (standalone; sibling of [`../gradus-clean-break/GOAL.md`](../gradus-clean-break/GOAL.md), which already deleted named `_NxM` wrappers; this goal deletes the remaining **device-kernel statues** in `src/kernel.fab`)
**Source:** operator 2026-09-03 — Gradus must not hardcode model dimensions in library functions; SmolLM2 remains a legal **experiment**, not the library contract. Prior CTO research `0217b270` (2026-08-27) still supplies the compiler architecture (imported-generic entry discovery, plan-time monomorphization, compiler-owned export). That research's "keep v1 source statues forever" migration is **superseded**: dual library surfaces are the break, not the plan.
**Repos:** `gradus/` (library kernels — write); `radix/` (imported-generic instantiation, plan-time monomorphization, export API); `hosts/` (launch/resource as the export API surfaces them)
**Related:** [`../gradus-clean-break/GOAL.md`](../gradus-clean-break/GOAL.md) (wave 3 already named `kernel.fab` statues as gated on SGD-1/2); [`../dense-typed-assembly/goal.md`](../dense-typed-assembly/goal.md) (size facts from admitted model config); [`../kernel-purity-census/consumer-proof-2026-08-26.md`](../kernel-purity-census/consumer-proof-2026-08-26.md); [`../../../radix/docs/archived/shape-generics/goal.md`](../../../radix/docs/archived/shape-generics/goal.md) (language `size` params — **done** 2026-08-18); [`../../../radix/docs/factory/head-axis-attention/goal.md`](../../../radix/docs/factory/head-axis-attention/goal.md) (U4 batched SmolLM2 literals in `kernel.fab` — condemned by this law, not a reason to keep them); [`../../../radix/docs/factory/metal-emit-reviews/CAMPAIGN.md`](../../../radix/docs/factory/metal-emit-reviews/CAMPAIGN.md)

---

## Invariant

Public Gradus library functions — especially `@ kernel` entries under `gradus:*` — express tensor geometry only as **named `size` parameters**. A compiled Metal grid may be concrete. A measurement pin may name SmolLM2. **Library source may not.**

A new model configuration yields a device artifact by admitting size facts in implementation, fixture, or test code and instantiating the same generic leaves. It does **not** edit `gradus/src/kernel.fab` (or any other library leaf) and does **not** add a Rust signature/splice table.

## Break boundary (clean break)

**Cut:** model geometry literals in Gradus **library** source. Today that is primarily `gradus/src/kernel.fab` (`D=960`, `H=15`, `kv_heads=5`, `d=64`, `F=2560`, `L_max=76`, `T_p=36`, and the U4 batched forms of the same numbers). Named `_NxM` wrappers are already under `gradus-clean-break`. This goal does not leave a "legacy GEA3 family" beside the generic one.

**Keep (not library API):**

| Where numbers may live | Why |
| --- | --- |
| Model admission / implementation (`DenseConfig`, GGUF metadata, size-fact environment) | The loaded model **is** the geometry |
| Fixtures and tests (`gea3_pipeline_test.rs`, proba that instantiate generics, export tests) | They name one experiment |
| Measurement statues (`scripta/perf-parity-targets/*.toml`, v1 identity rows) | Frozen **experiments**, not `gradus:*` |
| Plan-time monomorphized artifacts (emitted MSL, FMIR, identity block) | Instantiation output |

**Refuse:** a dual path. "Generics for new models, SmolLM2 literals stay in `kernel.fab`" is not a clean break. A flag that rejects *future* literals while keeping the current statues is not a clean break.

SmolLM2 stays. Its `960/15/5/64/76/36` tuple is supplied by admission, a fixture, or a test that **instantiates** `decode_score_gemm<…>(…)`. It is not the type of `gradus:kernel.decode_score_gemm`.

## Problem

Observable in the live tree (2026-09-03):

- **`gradus:kernel` is a SmolLM2 program.** `src/kernel.fab` freezes GEA3 geometry in every public decode/prefill signature (inventory comments at `:256–268`; bodies e.g. `decode_rmsnorm` `[1,960]`, `decode_gemv_qo` `[1,960]×[960,960]`, `decode_gemv_kv` `[1,960]×[960,320]`, KV capacity `L_max=76` at `:271–277`). Head-axis U4 (packet `6506c03`, not required on sibling main for this law) only batched heads to `[5,76,64]` / `[5,3,1,64]` — still SmolLM2, still library source.
- **Gradus is an AI library.** `nn.linear<size M, size K, size N>` (`src/nn.fab:331–333`), `rmsnorm<size T, size D>`, `swiglu_hidden<size T, size F>`, `math.add<size M, size N>` already exist. A second GGUF should instantiate those (and generic decode/prefill leaves), not rewrite `kernel.fab`.
- **The device product route cannot consume the generic leaves.** Imported size-generic `@ kernel` calls type `ignotum` (WARN010/SEM010/SEM011); `LoweringContext::imported_device_routes` is written and not used as the production entry discovery path (`kernel-purity-census/consumer-proof-2026-08-26.md`). Same-unit generic Metal already size-bakes. The gap is Radix linkage, not missing `size` syntax (`radix/docs/archived/shape-generics/` closed 2026-08-18).
- **Export is a second statue factory.** The GEA3 harness manufactures concrete source by scanning markers and replacing `[76,` → `[{capacity},` inside a test module (`radix/crates/mir-emit-harness/src/gea3_pipeline_test.rs`). A second model on that path is another splice table.

Until library signatures stop owning SmolLM2, every new test model is a Gradus rewrite. That is the defect this goal exists to remove.

## Proposal

### 1. One library surface

Rewrite the GEA3 leaf family in `gradus/src/kernel.fab` (and any other library `@ kernel` that still carries model literals) to named `size` parameters. Minimum geometry vocabulary: `T, D, Q, K, F, V, H, KV, d, C, E` with admitted relations from model config (`D, V, F, Q = H·d, K = KV·d` — [`dense-typed-assembly`](../dense-typed-assembly/goal.md)). Pure leaves stay call-free. Layer/head **repetition** stays in the plan, not as cloned library functions.

Delete the concrete statue signatures. Do not keep `decode_score_gemm` as `[1,64]·[64,76]` or `[5,3,1,64]·[5,64,76]` next to a generic twin. Callers (fixtures, tests, GEA3 export, product admission) instantiate.

### 2. Where SmolLM2 numbers go

The first v2 instantiation **is** the current SmolLM2-360M tuple and the current workloads (`metal-m5max`, `metal-m5max-fixed1000`). Those numbers live in:

- the closed `ShapeEnvironment` produced at model admission from config + tensor metadata
- test/fixture bindings that request that environment
- measurement statue TOMLs (unchanged names)

They do not live in `gradus/src/**/*.fab` library function types.

Reject inconsistent divisibility, inconsistent weight shapes, and `0 < L <= E <= C` **before** export.

### 3. Compiler route (still required — otherwise the library cannot run on device)

1. **Imported generic entry discovery (hard gate).** An imported generic Gradus `@ kernel` must emit a concrete Metal instance with substitutions recorded. No source-specialization fallback. SGR-U0 landed fail-closed admission; this unit is not done until a real imported generic leaf becomes a device entry.
2. **Plan-time monomorphization.** The plan builder requests concrete instances from the shape environment. Radix monomorphizes **before** MIR/AIR recipe selection. Recipes stay the closed set (`TiledMatMul`, `RowSoftmax`, `BatchedAttention`, …). Runtime values remain position, active length, and selected subwindows — not shape-defining extents.
3. **Compiler-owned export API.** Returns instance table, ordered size bindings, emitted source/binary, reflection, resource plan, identity block. Tests **call and pin**. They do not splice signatures.
4. **AOT + on-disk cache.** Specialize at build or once at admission. Cache key: generic-source digest, ordered bindings, compiler/target/toolchain, recipe plan, emitted digest. No compile inside decode.

### 4. Measurement identities are not library statues

Existing v1 target names, artifact roots, baselines, and receipts stay as **historical measurement tooling** (fail-closed replay). A changed generation is a new identity (`radix/scripta/perf.py`). That law does **not** freeze `kernel.fab` literals.

New generic-source or new bindings mint a **new** identity family. Byte-equality between old spliced source and new monomorphized source is not demanded. Equivalence is semantic output/oracle, plan counts, reflection, and physical receipt at the SmolLM2 tuple.

**Acceptance** is a second model/config + second capacity/extent pair that compiles and runs with **zero** edits to Gradus library kernel source and **no** new Rust signature table. Diff on `gradus/src/kernel*` is empty of new concrete forms.

### Alternatives ruled out

- **Disable-future-only.** A lint that bans *new* literals while `kernel.fab` stays SmolLM2. Guilty. Delete the statues.
- **Runtime-extent default / per-token JIT / shape interpreter.** Shape-defining extents are plan-bound.
- **Recipe templates that generate Faber per model.** Recreates the zoo one layer later.
- **Keeping U4 batched literals as the "generic enough" API.** `[5,3,1,64]` is still SmolLM2.

### Non-goals

- No dropping SmolLM2 as the parity/smoke model.
- No rewrite of v1 measurement rows, roots, or receipts.
- No CUDA physical claim (external block `411b16f3`); Metal acceptance does not wait on it.
- No new attention variants beyond existing recipes.
- No finishing head-axis U5–U8 as a **library** contract. Those units may proceed on the packet as statue work; this goal does not treat their concrete `kernel.fab` types as the destination API. When this break lands, those signatures are gone.
- No delivery lowering in this file — unit graph at `$delivery`.

## Units (lowering sketch — refine via `$delivery`)

| Unit | Scope | Depends on | Hand evidence |
| --- | --- | --- | --- |
| SGD-0 | Record the break: library-literal inventory in `gradus/src/`; v1 measurement replay vs v2 identity rules. No product dual-path. | — | none |
| SGD-1 | Imported-generic unification + instance registration + entry discovery (hard gate). SGR-U0 is not this unit. | SGD-0 | none |
| SGD-2 | Compiler-owned export API (not `#[cfg(test)]` splice). | SGD-0 | none |
| SGD-3 | Clean-break `kernel.fab` (and remaining library `@ kernel` literals) to `size` parameters only; delete statue signatures; move SmolLM2 numbers into admission/fixtures/tests. | SGD-1, SGD-2 | none |
| SGD-4 | Second-config proof: different geometry + `C/E`, zero library-kernel edits, no Rust signature table. | SGD-3 | none |
| SGD-5 | v2 identity/parity files only; v1 rows untouched. | SGD-4 | none |
| SGD-6 | Product cutover: new shapes use v2; delete live splice/statue manufacture; v1 replay-only. | SGD-5 | none |

## Validation

1. **Library ratchet.** No public `gradus:*` `@ kernel` (and no other library tensor function this goal admits) has a model-geometry integer literal in its signature. Enforcement is a named check at delivery (Gradus-side grep/ratchet + `faber check` on `src/kernel.fab`). Fixtures and tests **may** contain `960`, `76`, `15`.
2. **Hard gate (SGD-1).** Imported generic Gradus entry → concrete Metal with substitutions in the identity. `ignotum` / unwired discovery gone. No source-specialization fallback.
3. **SmolLM2 still runs (SGD-3).** The current tuple instantiates from fixture/admission, not from library types. Equivalence receipt vs v1: semantic/oracle, plan counts, reflection, physical receipt. Byte-equality not demanded.
4. **Second model (SGD-4).** Different geometry compiles and runs; `git diff` on `gradus/src/kernel*` shows no new concrete forms and no reintroduction of literals.
5. **Identity.** Cache-hit digest equality; new binding or generic-source edit mints a new identity; v1 measurement rows replay.
6. **KV names.** Distinct `C/L/E/p`; `0 <= p < C`, `L <= E <= C`; no `declared_history_length=capacity` conflation.
7. **Leaf law.** Pure leaves `@ kernel` and call-free; no mega-kernel; no runtime shape interpreter.

**Stop:** imported-generic repair requires a language/grammar change (escalate — architecture fork); second-config acceptance needs a library-source edit (the route failed — stop, do not add a concrete form); a Hand proposes keeping statue signatures "for SmolLM2 only" (refuse — that is the dual path).

## Delivery checklist

| Check | Enforced by |
| --- | --- |
| Library kernels have no model-geometry literals in signatures | delivery-named ratchet + `faber check` on `gradus/src/kernel.fab` |
| SmolLM2 numbers appear only in admission/fixtures/tests/measurement TOMLs | SGD-3 review; `rg` over `gradus/src/**/*.fab` vs harness/TOML |
| No splice/statue manufacture in product code | SGD-2/SGD-6: export API in a non-test crate |
| v1 measurement generations remain named and replayable | `radix/scripta/perf.py` identity pins |
| v2 identity binds generic source + ordered bindings + recipe + target + emitted bytes | SGD-2 tests + SGD-5 manifest |
| Status line stays machine-parseable | `radix/scripta/check-factory-goal-status` |
| New grammar production (if any) ships a corpus variant-cell | `./scripta/check-corpus-variant-cells` |

## Ledger

| Unit | Status | Seat | Receipt | Notes |
| --- | --- | --- | --- | --- |
| SGR-U0 | done (2026-08-27) | — | radix `4245ce35e`; auditor `0f6d0faa`; CTO `1dd6fa4d` | admission + fail-closed bindings; **not** SGD-1 closeout |
| SGD-0 | pending — not lowered | — | none | break inventory + identity rules |
| SGD-1 | pending — not lowered | — | none | hard gate |
| SGD-2 | pending — not lowered | — | none | export API |
| SGD-3 | pending — not lowered | — | none | **clean-break library statues** |
| SGD-4 | pending — not lowered | — | none | second model; acceptance |
| SGD-5 | pending — not lowered | — | none | v2 files only |
| SGD-6 | pending — not lowered | — | none | splice/statue product deletion |

## Open questions

1. **Second model for SGD-4.** Default: a live GGUF whose `H/KV` and `d` differ from SmolLM2-360M (Qwen-class if admitted). Decider: operator at the gate.
2. **Export API crate placement (SGD-2).** Default: normal compiler/product crate on the MIR export path, not `#[cfg(test)]`. Decider: delivery lowering.
3. **AOT cache layout.** Default: on-disk under v2 artifact roots; five-part digest key. Decider: delivery lowering.
4. **Head-axis packet (`6506c03`) vs this break.** Default: do not merge U4's concrete signatures as the library API; SGD-3 deletes them. Head-axis launch-collapse may re-land **after** generic signatures exist. Decider: Mind at SGD-3, not a silent keep.
5. **CUDA physical receipt.** Still externally blocked. Not required for Metal acceptance.

---

*Template: `radix/docs/factory/TEMPLATE.md`. Operator law 2026-09-03: clean break, not a future-literal ban. This file is the tracking authority; the repos are the implementation authority. When they disagree, the repo wins and this doc is the defect.*
