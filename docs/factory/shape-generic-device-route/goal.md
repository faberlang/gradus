# GOAL: shape-generic-device-route — reusable shape-generic device kernels behind plan-time monomorphization

**Status**: planned — forged from CTO research 0217b270 (2026-08-27); implementation dispatch gated on PGC waves + first post-PGC AC checkpoint
**Created**: 2026-08-27
**Campaign:** `—` (standalone; successor consumer of the in-flight PGC waves B1/B3/C2/C5 and of the `gradus-llama-parity` baseline of record)
**Source:** operator problem statement (gradus device kernels carry fixed concrete numbers where shape-generic placeholders should be; gradus must seamlessly pick up new sizes and dimensions for upcoming formats without recreating concrete forms each time); CTO research mail `0217b270` (design authority — executive ruling, target architecture, migration law, ports, correct-before gates, risk inventory, all file:line-cited and re-verified against live trees 2026-08-27); planner handle `6bf158c6`
**Repos:** primary: `gradus/` (generic kernel leaf family, model admission); `radix/` (imported-generic type unification, entry discovery, plan-time monomorphization, first-class export API, AIR recipes); `hosts/` (launch/resource seams as surfaced by the export API)
**Related:** [`../perf-gap-closure/GOAL.md`](../perf-gap-closure/GOAL.md) (PGC — implementation entry condition; B1/B3/C2/C5 produce the semantics this goal ports); [`../dense-typed-assembly/goal.md`](../dense-typed-assembly/goal.md) (size-facts `D,V,F,Q=H·d,K=KV·d` and the leaf law); [`../kernel-purity-census/consumer-proof-2026-08-26.md`](../kernel-purity-census/consumer-proof-2026-08-26.md) (the hard-gate evidence); `../../radix/docs/factory/gradus-llama-parity/goal.md` (baseline of record, CUDA external block `411b16f3`); `../../radix/crates/radix-mir/src/kernel_plan/` (AIR recipe set)

---

## Invariant

One size-generic Gradus kernel leaf family, admitted through a closed `ShapeEnvironment` and monomorphized at plan time before recipe selection, exported through a first-class compiler-owned API — such that a new model configuration yields a new, identified concrete device artifact **without editing kernel source, without a Rust signature/splice table, and without disturbing any v1 measurement identity** (append-only identity families, v1 replay preserved forever).

## Problem

The operator's requirement is observable in the repos today:

- **Gradus device kernels are concrete statues.** The GEA3 families freeze exact geometry in source — `D=960, H=15, K=5, d=64, F=2560`, decode capacity `L_max=76`, prefill `T_p=36` — with per-head windows and the 32× layer repetition held plan-side (`gradus/src/kernel.fab:292-303`, `:439-450`). The KV geometry comment names the design: fixed-capacity buffers at `L_max=76`, append-in-place, declared history length, mask beyond L (`gradus/src/kernel.fab:322-327`). Every new size, dimension, or upcoming format means re-authoring a concrete form.
- **The generic surface already exists and already works in-unit.** Typed size-generic leaves are live production forms: `linear<size M, size K, size N>` (`gradus/src/nn.fab:363-367`), `rmsnorm<size T, size D>`, `swiglu_hidden<size T, size F>` (`gradus/src/nn.fab:520-529`), `add<size M, size N>` (`gradus/src/math.fab:269-273`). Same-unit generic Metal emission is concrete and size-baked (spike2: exit 0, sizes baked at instantiation — `kernel-purity-census/consumer-proof-2026-08-26.md:27-47`). Generic signatures are **not** the gate.
- **Imported generic calls do not reach a device entry.** In a consumer unit, an imported size-generic call types `ignotum` (WARN010/SEM010/SEM011 — `consumer-proof-2026-08-26.md:66-78`). Entry discovery is the failing link: `LoweringContext::imported_device_routes` is written and never read; `instantiate_merged_generic_calls_with_devices` has no production caller, so `ImportedDeviceRegistration` is never produced in a real compile; zero concrete instances ⇒ zero kernel-role defs ⇒ metal-text zero-kernel error (`consumer-proof-2026-08-26.md:120-143`). This is a Radix linkage/admission defect, **not** a license to specialize source per geometry.
- **Export is test-owned string surgery.** The production-shaped export extracts function text by marker scanning, SHA-pins the base slice, rewrites signatures by literal replacement (`[76,` → `[{capacity},`), and inserts a `, u32 id` ABI parameter — all inside a test module (`radix/crates/mir-emit-harness/src/gea3_pipeline_test.rs:602-656`, `:638-656`, `:716-749`). That is evidence machinery, not a product boundary. A second model through that path would be another hidden statue factory.

**Ground truth researched** (CTO citations re-verified against live trees 2026-08-27; worktree citations against the read-only in-flight PGC branches):

| Claim | Evidence |
| --- | --- |
| Concrete-statue source with plan-side repetition | `gradus/src/kernel.fab:292-303`, `:322-327`, `:439-450` |
| Typed size-generic leaves already production | `gradus/src/nn.fab:363-367`, `:520-529`; `gradus/src/math.fab:269-273` |
| Size facts admitted from config, not literals | `gradus/docs/factory/dense-typed-assembly/goal.md:87-93` (`D,V,F,Q=H·d,K=KV·d`) |
| Leaf law / fusion surface | `gradus/docs/factory/dense-typed-assembly/goal.md:109-148` |
| Imported generics type ignotum; entry discovery unwired | `gradus/docs/factory/kernel-purity-census/consumer-proof-2026-08-26.md:66-78`, `:120-143` |
| Same-unit generic Metal is concrete/size-baked | `consumer-proof-2026-08-26.md:27-47` |
| AIR: target-neutral closed recipe set; plan never names a target keyword; fast path must honor dispatch contract | `radix/crates/radix-mir/src/kernel_plan/mod.rs:1-22`, `kernel_plan/plan.rs:57-76` |
| Splice/statue export in test code | `radix/crates/mir-emit-harness/src/gea3_pipeline_test.rs:602-656`, `:638-656`, `:716-749` |
| Identity-generation law: drift = new identity, never an adjustment | `radix/scripta/perf.py:514-525` |
| v1 generations are separate immutable rows (short/fixed1000/soak) | `radix/scripta/perf.py:175-264` |
| Identity block pins target/model/comparator/kernel | `radix/scripta/perf.py:378-426` |
| Separate artifact roots per statue arm | `radix/crates/mir-emit-harness/src/gea3_pipeline_test.rs:85-99` |
| B1 capacity/extent split + `0 < E <= C` + bucket policy + four extent-sensitive members + `declared_history_length=capacity` conflation | `worktrees/pgc-b1/radix/crates/mir-emit-harness/src/gea3_pipeline_test.rs:61-70`, `:91-110`, `:3636-3650`, `:749-757`, `:3962-3976`, `:4002-4008`, `:4021-4040` |
| B3 selected-row append: runtime position → byte offset into capacity arena; three row-width bindings | `worktrees/pgc-b3/radix/crates/mir-emit-harness/src/gea3_pipeline_pgc_b3_test.rs:110-131`, `:134-181` |
| C5 lifetimes: weights `PerProgram`/`HostProvided`, activations `PerStep` | `worktrees/pgc-c5/radix/crates/mir-emit-harness/src/gea3_pipeline_pgc_c5_test.rs:147-163`, `:198-227` |
| Plan admission sits outside steady-state timing | `radix/scripta/perf-parity-targets/metal-m5max-fixed1000.toml:121-124` |
| CUDA externally blocked (hosts fused-library arm, need `411b16f3`) | `radix/docs/factory/gradus-llama-parity/goal.md:97-99` |

**Evidence boundary (CTO "not claimed", carried forward):** no product verification, benchmark, or device test was run for this research; CUDA runtime performance is unproven and must not be inferred from Metal; generic v2 artifacts are not claimed byte-identical to v1 and byte-equality is explicitly not demanded. The CTO also noted `radix/docs/factory/perf-gap-closure/` is absent from radix main — the PGC goal of record lives at `gradus/docs/factory/perf-gap-closure/GOAL.md` (active, waves firing), which is the entry condition cited below.

## Proposal

Carried faithfully from CTO research `0217b270` §1. Size estimate **L** (~600k–900k tokens, multi-repo Radix + Gradus + Hosts).

### 1. Target architecture

1. **Size-generic leaf family.** Gradus authors one generic leaf family; geometry is expressed as named `size` parameters — at minimum `T, D, Q, K, F, V, H, KV, d, C, E` — with relations admitted from model config rather than copied literals (the dense ruling's `D, V, F, Q = H·d, K = KV·d` pattern). Pure leaves remain call-free; layer/head repetition stays in the plan, exactly as the GEA3 source already states (`gradus/src/kernel.fab:292-303`, `:439-450`).
2. **Closed `ShapeEnvironment` at model admission.** Model admission resolves config + tensor metadata to a closed shape environment of admitted size facts. Reject inconsistent divisibility, inconsistent weight shapes, and `0 < active_length <= E <= C` **before export**.
3. **Plan-time monomorphization.** The plan builder requests concrete entry instances from that environment; Radix monomorphizes **before MIR/AIR recipe selection** and emits ordinary concrete target kernels. Recipes are unchanged in role: one target-neutral algorithm, backend-owned syntax (`radix-mir/src/kernel_plan/mod.rs:1-15`), across the closed recipe set — Elementwise, TiledMatMul, TreeReduction, Transpose, AxisReduction, RowSoftmax, LayerNormalization, Gather, RmsNormalization, Rope, CausalMaskedSoftmax, QuantizedMatMul, GroupedMatMul, BatchedAttention, SsmConv1d, SsmScan (`kernel_plan/plan.rs:64-129`). Generic sizes resolve to the same concrete `CollectionKernelPlan` variants (`kernel_plan/plan.rs:57-109`).
4. **First-class compiler-owned export API.** Export becomes a normal compiler/product API returning: the concrete instance table, ordered size bindings, emitted source/binary, reflection, the resource plan, and the identity block. Test code **calls and pins** that API; it never owns manufacture by string replacement or ABI-text insertion.
5. **AOT specialization with on-disk cache; never JIT per token.** Specialization happens at build or once at model admission, cached on disk. Cache key includes: canonical generic-source digest, ordered size bindings, compiler/target/toolchain identity, recipe-plan identity, and emitted artifact digest. No compilation inside decode.

**Alternatives ruled out (CTO §1):**

- **Runtime-extent kernels are not the default.** They sacrifice concrete recipe geometry and invite branch/bounds overhead. Runtime values remain appropriate **only** for position, active length, and selected subwindows; shape-defining extents are plan-bound. B3 demonstrates the correct split: runtime position selects one row while the emitted entry keeps three compact width-sized bindings (`worktrees/pgc-b3/.../gea3_pipeline_pgc_b3_test.rs:110-131`, `:134-181`).
- **JIT-per-config is not the architecture.** It is at most an optional cache-miss implementation: it must finish before timed generation and produce the same identified concrete artifact as AOT. Plan admission already sits outside steady-state timing (`radix/scripta/perf-parity-targets/metal-m5max-fixed1000.toml:121-124`).
- **Recipe templates do not become source-generating model templates.** AIR is already a closed shared algorithm set; generating Faber source per shape would recreate the specialization zoo one layer later. Recipes stay inside AIR/Radix.

### 2. Migration without invalidating the record (append-only identity families)

- **v1 preserved forever.** Every existing v1 target, test name, source revision/hash, artifact root, baseline, and receipt stands. The registry's identity-generation law already rules that a changed generation is a new identity, never an adjustment (`radix/scripta/perf.py:514-525`); short/fixed1000/soak generations hold separate immutable rows (`radix/scripta/perf.py:175-264`); statue arms already require separate roots (`gea3_pipeline_test.rs:85-99`) and baselines are append-only (`radix/docs/factory/gradus-llama-parity/goal.md:70-80`, `:212-214`).
- **New `gea-generic-v2` identity family.** Do not rewrite `gea3-*-v1`. v2 gets new export test/product command names and new artifact roots. New generic-source edits or new bindings mint new identities; they never mutate a baseline.
- **First v2 instantiation = the exact old SmolLM2 tuple and workload tuples.** Compare semantic output/oracle, plan counts, reflection, and the physical receipt. **Byte equality between old hand-spliced source and new monomorphized source is not demanded**; record both identities and the equivalence receipt.
- **The acceptance test is the second model.** A second model/config plus a second capacity/work-extent pair must compile and run **without editing kernel source and without adding a Rust signature table**. This is what distinguishes generic architecture from another hidden statue factory.
- **Cutover and rollback.** The v1 replay path stays indefinitely as historical measurement tooling (fail-closed). After v2 acceptance, stop admitting new product shapes through v1; historical reproduction remains legal. Exit strategy: if v2 stalls, v1 remains the product route and this goal parks without touching the baseline of record.

### 3. Ports and non-ports (from PGC B1/B3/C2/C5 and AIR)

| Item | Disposition | Evidence |
| --- | --- | --- |
| B1 capacity/extent split (`C` vs `E`) with `0 < E <= C` enforced | **PORT** — becomes size bindings and plan facts, not signature string replacement | `worktrees/pgc-b1/.../gea3_pipeline_test.rs:61-70`, `:91-110`, `:3636-3650` |
| B1 bucket policy (fixed1000: `C=1100`, attention `E=1088`, recipe dims follow `E`; four extent-sensitive attention members) | **PORT** — the exact 64/1088 buckets are policy for the old workload, not universal constants | `:749-757`, `:3962-3976`, `:4021-4040` |
| B3 selected-row append: runtime position → byte offset into capacity-sized arena, one-row spans, `Elementwise` recipe, three-binding ABI | **PORT** — the ABI and recipe survive; literals `320` and `76` do not | `worktrees/pgc-b3/.../gea3_pipeline_pgc_b3_test.rs:110-131`, `:134-181` |
| AIR recipes and backend lowering, unchanged in role | **PORT** — generic sizes resolve before recipe construction, same concrete `CollectionKernelPlan` variants | `radix-mir/src/kernel_plan/plan.rs:57-109` |
| Plan-time resource lifetime classification (weights `PerProgram`/`HostProvided`; activations `PerStep`) | **PORT** — generic shapes parameterize counts without changing lifetimes | `worktrees/pgc-c5/.../gea3_pipeline_pgc_c5_test.rs:147-163`, `:198-227` |
| B1/B3 harness plumbing and the string splice | **NON-PORT** — not product architecture | `gea3_pipeline_test.rs:638-656`, `:716-749` |
| Literal constants (76, 320, 64/1088 buckets, 960/15/5/64/2560 geometry) | **NON-PORT** — become named parameters, admitted relations, or documented policy | `gradus/src/kernel.fab:292-303` |

### 4. Correct-before-product gates and recorded risks (CTO §4)

| Item | Class | Requirement |
| --- | --- | --- |
| **Imported generic entry discovery** | CORRECT_BEFORE — **the hard gate** | Repair imported-generic type unification (no `ignotum` result), concrete instance registration, and entry discovery. Done when an imported generic Gradus entry emits concrete Metal with substitutions recorded in the identity — no source-specialization fallback. (`consumer-proof-2026-08-26.md:120-143`) |
| **Instantiated identity law** | CORRECT_BEFORE | Hashing generic source alone is insufficient (one source, many concrete artifacts). Identity binds generic source + ordered substitutions + recipe plan + target/compiler + emitted bytes. Preserve the old base-slice SHA fail-closed check (`gea3_pipeline_test.rs:638-644`) and the target/model/comparator/kernel pins (`perf.py:378-426`, `:1461-1464`). |
| **KV `C/L/E/p` semantics** | CORRECT_BEFORE v2 receipt | Distinct names and invariants: allocation capacity `C`; logical active length `L`; compute extent/bucket `E`; append position `p`. Require `0 <= p < C`, `L <= E <= C`, mask `[L,E)`, no read beyond `E`. B1's export still records `declared_history_length=capacity` (`worktrees/pgc-b1/...:4002-4008`); v2 must not preserve that naming conflation. Current source conceptually separates fixed capacity from declared length (`gradus/src/kernel.fab:322-327`). |
| **Splice removal** | CORRECT_BEFORE second model | Move instantiation/export out of the `#[cfg(test)]` module into a normal compiler/product crate; tests call and pin the API. (`gea3_pipeline_test.rs:602-656`, `:716-749`) |
| Metal/CUDA codegen quality | RECORD_RISK | Compile/reflection proof + physical receipt for ≥2 substantially different tuples. Same-unit Metal only proves basic monomorphization (`consumer-proof-2026-08-26.md:27-47`). Never infer CUDA quality from Metal; CUDA remains externally blocked (`gradus-llama-parity/goal.md:97-99`). |
| JIT/AOT cliff | RECORD_RISK | Measure compile/cache-miss wall **separately** from prefill/decode. Require cache-hit artifact digest equality. No compilation inside decode. A target fast path may replace a portable recipe only while honoring the same dispatch contract (`kernel_plan/plan.rs:57-62`). |
| Fusion/codegen regressions | RECORD_RISK | Preserve the leaf law: pure tensor leaves are `@ kernel`; effectful assembly stays host-side; no loop/slice/call inside a leaf (`dense-typed-assembly/goal.md:109-148`). Genericization must not create a mega-kernel or a runtime shape interpreter. |

### Non-goals

- **No v1 rewrite.** `gea3-*-v1` identities, tests, roots, baselines, and receipts are never edited or re-baselined.
- **No resequencing of PGC/SCR waves.** This goal is forged now but stays closed until the PGC waves complete and the first post-PGC AC checkpoint passes; the current baseline of record remains the comparison instrument.
- **No runtime shape interpreter, no per-token JIT, no runtime-extent default.** Shape-defining extents are plan-bound.
- **No recipe relocation.** AIR stays the closed shared recipe set inside Radix; no source-generating model templates.
- **No CUDA execution claim.** CUDA is a recorded external dependency (`411b16f3`), not a deliverable of this goal.
- **No new model-format features beyond admission plumbing** (e.g. new attention variants beyond existing recipes) — upcoming formats are served by the generic route, not by new concrete families.
- **No delivery lowering in this document** — unit graph refinement happens at the implementation gate via `$delivery`.

## Units (lowering sketch — refine via `$delivery` at the gate)

CTO §5 sketches; **not yet lowered**. Sequencing: keep closed until the PGC AC checkpoint; then elevate SGD-1 and SGD-2 first; SGD-3 depends on both; SGD-4 is the architecture acceptance gate; SGD-5/6 follow acceptance.

| Unit | Scope | Depends on | Hand evidence |
| --- | --- | --- | --- |
| SGD-0 (S, record-only) | Freeze the v1 replay contract; define the v2 identity tuple and append-only rules | — | none |
| SGD-1 (M, hard-gate producer) | Repair imported-generic type unification, concrete instance registration, entry discovery in Radix | SGD-0 | none |
| SGD-2 (M) | First-class plan-bound export API (instance table, ordered bindings, emitted source, reflection, resource plan, identity block) | SGD-0 | none |
| SGD-3 (M) | Convert the GEA3 leaf family to size-generic source; port B1/B3 `C/L/E/p` semantics + AIR/resource-lifetime facts | SGD-1, SGD-2 | none |
| SGD-4 (M, acceptance gate) | Second-config proof: different model geometry + capacity/extent pair, no kernel-source edit, no Rust signature table | SGD-3 | none |
| SGD-5 (S/M) | v2 parity generation and baseline; new files only | SGD-4 | none |
| SGD-6 (S) | Route cutover: new product formats use v2; v1 replay-only; delete live product dependence on splice machinery | SGD-5 | none |

Done-when per unit (CTO wording, carried):

- **SGD-0**: all three v1 generations remain named and replayable; v2 cannot reuse their roots.
- **SGD-1**: an imported generic Gradus entry emits concrete Metal with substitutions in the identity; no source-specialization fallback.
- **SGD-2**: normal (non-`#[cfg(test)]`) code returns artifact + reflection + size bindings + recipe/resource plan + SHA identity; the old harness consumes it only for v2.
- **SGD-3**: the old SmolLM2 tuple produces a v2 equivalence receipt without a Rust signature splice table.
- **SGD-4**: a different model geometry and capacity/extent pair compile and run without editing kernel source or adding concrete forms; Metal receipt required, CUDA compile/descriptor parity required, CUDA physical receipt when the external route opens.
- **SGD-5**: new files only; old baselines untouched; prefill/decode and compile/cache walls compared separately.
- **SGD-6**: new product formats use v2; v1 remains replay-only; only live product dependence on splice machinery is deleted, never historical evidence.

## Validation

The closeout gate is the acceptance test plus the correct-before gates:

1. **Hard gate (SGD-1)**: imported size-generic Gradus entry → concrete Metal artifact with substitutions in identity; the `ignotum` typing and unwired entry discovery defects are gone.
2. **Equivalence receipt (SGD-3)**: v2 at the exact SmolLM2 tuple matches v1 on semantic output/oracle, plan counts, reflection, and physical receipt; both identities recorded; byte-equality not demanded.
3. **Acceptance test (SGD-4)**: second model/config + second capacity/extent pair compiles and runs with **zero kernel-source edits and no added Rust signature table** — proven by the diff being empty on `gradus/src/kernel*` and free of any concrete-form addition.
4. **Identity law**: cache-hit artifact digest equality; generic-source edit or new binding mints a new identity; v1 rows replay unchanged (fail-closed).
5. **KV semantics**: `0 <= p < C`, `L <= E <= C`, mask `[L,E)`, no read beyond `E`, distinct names in the exported plan (no `declared_history_length=capacity` conflation).
6. **Risk receipts**: ≥2 substantially different tuples carry compile/reflection proof and physical receipts; compile/cache-miss wall measured separately from prefill/decode; no compilation inside decode.
7. **Leaf law**: pure leaves `@ kernel` and call-free; no loop/slice/call inside a leaf; no mega-kernel.

Lane-owned broad validation (stages, e2e) is named once at delivery lowering, not per-unit here.

**Stop conditions**: PGC waves stall or re-baseline the measurement surface (hold this goal closed; re-audit the porting table); the imported-generic repair requires a language/grammar change rather than a wiring repair (escalate to Mind — architecture fork); second-config acceptance cannot be met without kernel-source edits (the route failed its purpose — stop and record, do not add a concrete form).

## Delivery checklist

| Check | Enforced by |
| --- | --- |
| v1 generations remain named, replayable, roots disjoint from v2 | `radix/scripta/perf.py` identity pins (`:514-525`, `:175-264`); base-slice SHA fail-closed check (`gea3_pipeline_test.rs:638-644`) |
| v2 identity binds generic source + ordered bindings + recipe plan + target/compiler + emitted bytes | SGD-2 identity-block tests + SGD-5 parity manifest |
| No splice/statue manufacture in product code | SGD-2/SGD-6: export API owned by a non-test crate; tests only call and pin |
| KV plan carries distinct `C/L/E/p` with invariants | SGD-3 exported-plan assertions (replaces `:4002-4008` conflation pattern) |
| Goal Status line stays machine-parseable and current | `radix` stage-1 factory-goal-status audit (`./scripta/check-factory-goal-status`) |
| Gradus kernel source compiles green through the faber inner loop | `./scripta/test` stages in `radix/`; gradus proba/e2e corpora at delivery |

## Ledger

| Unit | Status | Seat | Receipt | Notes |
| --- | --- | --- | --- | --- |
| SGD-0 | pending — not lowered; implementation gated on PGC waves + first post-PGC AC checkpoint | — | none | record-only freeze of v1 replay contract + v2 identity rules |
| SGD-1 | pending — not lowered; hard gate (imported generic entry discovery) | — | none | elevate first with SGD-2 after the gate |
| SGD-2 | pending — not lowered | — | none | first-class export API; elevate first with SGD-1 after the gate |
| SGD-3 | pending — not lowered | — | none | depends on SGD-1 + SGD-2 |
| SGD-4 | pending — not lowered | — | none | architecture acceptance gate (second model/config) |
| SGD-5 | pending — not lowered | — | none | v2 parity generation; new files only |
| SGD-6 | pending — not lowered | — | none | route cutover; splice removal from live product only |

## Open questions

1. **Which second model/config for SGD-4?** The CTO does not name it. Default: choose at the implementation gate from the live GGUF corpus and the PGC-informed target set, preferring a geometry substantially different from SmolLM2-360M (different `H/KV` ratio and `d`). Decider: operator/Mind at the gate.
2. **Placement of the export API crate in Radix** (SGD-2). Default: a normal compiler/product crate adjacent to the MIR export path, decided during delivery lowering; constraint is only that it is not a `#[cfg(test)]` module. Decider: delivery lowering + Mind.
3. **Cache location and format** for AOT artifacts (SGD-2/SGD-5). Default: on-disk under the v2 product artifact roots with the five-part digest key; exact layout decided at delivery. Decider: delivery lowering.
4. **CUDA route timing.** Externally blocked on the hosts fused-library CUDA arm (`411b16f3`). Not a fork — a recorded dependency; CUDA physical receipt lands when the route opens, and is not required for v2 Metal acceptance.
5. **Bucket policy for v2 workloads beyond fixed1000.** B1's 64/1088 buckets are old-workload policy. Default: bucket selection is an admission-policy input (recorded in the plan), with the fixed1000 policy preserved for the equivalence receipt. Decider: operator at SGD-3/SGD-4.

---

*Template: `radix/docs/factory/TEMPLATE.md`. Design authority: CTO research mail `0217b270` (2026-08-27). This file is the tracking authority; the repos are the implementation authority. When they disagree, the repo wins and this doc is the defect.*
