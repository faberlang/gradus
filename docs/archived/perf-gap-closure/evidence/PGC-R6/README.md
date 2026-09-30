# PGC-R6 evidence — Metal elementwise emit consumes `ElementwisePlan` (OF-3 re-admission)

Packet: `worktrees/pgc-r6/` (radix only), branch `factory/pgc-r6`.
Structural oracle only — **condition-B, no wall claim**. No performance
receipt, no timing, no launch-count-vs-wall table.

## Deliverable

The Metal elementwise emit path consumes the landed target-neutral
`ElementwisePlan` (OF-1 `3d8ce4d8a6`, OF-2 `aebec9180`) instead of
rebuilding pointwise expressions backend-locally:

- `radix-mir/src/elementwise_plan.rs` (additive): `composed_locals`
  coverage fact, `ElementwisePlan::covers_local`, and
  `elementwise_plan_summary` (design §12 — plan-or-named-barrier summary,
  discoverable without parsing MSL).
- `radix-mir-metal/src/emit/mod.rs` (elementwise path): `FunctionScope`
  derives the plan once per kernel body and drops it fail-safe when a plan
  input needs producer-defined read facts the plan does not carry
  (`reduced_projection`, materialized count below typed flat size).
- `radix-mir-metal/src/emit/elementwise.rs` (the migration): for a
  plan-covered, plain, single-output elementwise body, the plan's output
  statement binds the WHOLE plan-lowered per-element expression and the
  plan's intermediate producers emit nothing — the backend no longer
  rebuilds the chain's pointwise expression statement-by-statement.
  MSL text per node is byte-identical to the old builder's.

## Proofs (design §11, run at the packet)

Sanity gate: `cargo test -p radix-mir-metal elementwise` — 26 passed.
Affected crates full: `cargo test -p radix-mir` 676 passed;
`cargo test -p radix-mir-metal` 185 passed. 0 failed everywhere.

### Proof 4 — backend source proof

`pgc_r6_plan_consumed_one_store_no_intermediate`
(`radix-mir-metal/src/emit/tests/elementwise.rs`):

- focused fixture: the SGD `fill → mul → sub` chain
  (`parameter_update_kernel`), a legal elementwise-only subchain;
- plan summary receipt: `elementwise plan: 3 ops, 3 inputs, output local 5`;
- decomposition receipt: 1 subchain, carrying `expression_plan()`;
- MSL receipt: exactly ONE `output[id] = …` store for the whole chain,
  exactly 4 `[[buffer(…)]]` bindings (3 declared inputs + 1 output — no
  intermediate buffer), no `threadgroup`;
- the store expression is byte-identical to the pre-plan emitter's
  composition: `(x_in[id] - (input_2_in[0] * input_1_in[id]))` (the same
  golden the pre-existing S5-U2 tests pinned — those tests now run through
  the plan path and pass unchanged, which is the equivalence coverage).

### Proof 5 — unfused comparison (two-class oracle)

`pgc_r6_unfused_comparison_byte_equality`: the same chain
planning-disabled — each op its OWN kernel writing an intermediate buffer
(fill kernel, mul kernel, sub kernel) — composes, by exact f32 store/load
substitution of the intermediate reads, to the SAME final expression the
fused plan-driven kernel emits.

Class declaration: pure elementwise f32 chain under the source-order
policy (`ReassociationPolicy::Forbidden` in the plan; no reassociation,
no FMA synthesis); an intermediate f32 store/load round-trip is exact, so
**byte equality is what the contract promises** (class A). No tolerance is
invoked and none is widened.

### Proof 6 — no accidental scope expansion

`pgc_r6_named_barriers_block_accidental_scope`: reduction
(`TensorMean`), matmul (`TensorMatMul`), quantized
(`TensorQuantizedMatMul`), fragment-call (`MirStatementKind::Call`), and
control-flow (two-block) fixtures each return their NAMED typed barrier
(`Recipe` / `Effect` / `ControlFlow`) — never a silent elementwise
classification. The summary receipt names the class:
`elementwise barrier: recipe op TensorMean is an elementwise fusion
barrier`. Plan-side mirrors: `elementwise_plan_test.rs`
`recipe_op_is_barrier_not_elementwise`,
`unary_relu_gelu_assign_is_effect_barrier`, plus new
`composed_locals_cover_chain_and_exclude_params`,
`plan_summary_reports_plan_or_barrier_reason`.

## Old backend-local builder disposition (honest scope)

Removed for every body the plan covers: plan-covered elementwise-only
chains no longer compose expressions statement-by-statement — the plan is
the single expression source, with byte-identical MSL proven by the
pre-existing goldens (now running through the plan path) plus proof 5.

Retained where NO plan can exist by OF-1's own typed barriers, i.e. where
equivalence coverage cannot exist because the shared plan does not model
the body (design §13 stop-condition territory, reported not hidden):

- recipe subchains (elementwise ops folded into
  matmul/reduction/transformer recipes — the per-recipe composition seam
  is OF-4 territory);
- temp-destination / live-`Assign` bodies (the real S5-U2b lowering
  shape — `Effect`/`UnresolvedShape` barriers in the plan builder);
- keep-dims reduced-projection reads and count-below-flat inputs
  (producer-defined read mappings the plan does not carry — guarded at
  plan-attach time, fail-safe to the unchanged old model);
- indexed (builtin-input) and multi-output tuple kernels.

A barrier is never silently treated as a fused plan: `None` keeps the
statement-local model whose MSL is byte-identical to the pre-change
emitter, and the typed reason is reportable via
`elementwise_plan_summary`.

## Constraints honored

- No proba tuple change: emit-internal only; no `gradus/src/kernel.fab`,
  no `kernel.proba`, no corpus, no host code touched (packet is
  radix-only; `gradus/`+`hosts/` appear in the packet as untracked
  read-only symlinks to the main checkout solely so the crates'
  `include_str!` test fixtures resolve).
- No new inliner, no MSL device-fn rung, no NVVM/WGSL migration, no
  driver flag, no recipe-seam widening, no wall numbers.

## Reproduction (packet `worktrees/pgc-r6/radix`)

```
cargo test -p radix-mir elementwise_plan
cargo test -p radix-mir-metal elementwise
cargo test -p radix-mir
cargo test -p radix-mir-metal
```
