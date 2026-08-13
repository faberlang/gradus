# Delivery: GGUF-M3 — Hybrid SSM/Attention State, Micro-Unit Re-Lower (Qwen MODEL-03)

**Status**: re-lowered 2026-08-13 by planner-36 (task `d5367a87` / need `0418ad42`) — **READY at the spec level; dispatch-gated on MODEL-01 (GGUF-M1) landing and the GGUF-A1c/A2/A3/A5 predecessor set** (see §Entry Gate). Planning artifact only: no product code is written by this lowering.
**Campaign**: [`radix/docs/factory/gpu-production-readiness/CAMPAIGN.md`](../../../../radix/docs/factory/gpu-production-readiness/CAMPAIGN.md) — umbrella row **MODEL-03** ("Implement hybrid SSM/attention state")
**Delivery authority**: [`pml5-general-gguf-delivery.md`](pml5-general-gguf-delivery.md) — unit **GGUF-M3** ("Hybrid SSM And Attention State")
**Supersedes as the dispatch artifact**: [`model-03-ssm-attention-state-delivery.md`](model-03-ssm-attention-state-delivery.md) at planner-27 commit `30f32ef` (one delivery-sized Hand task with intra-unit stages S0–S7). This re-lower converts the same stage graph into **eight one-logical-change Hand units** before the delivery audit. Every feature the source task named is preserved unchanged (§Normalized Spec); nothing is narrowed, deferred, or moved.
**Repo**: `gradus` (branch `factory/planner-36`, baseline `1462cd874bb`); planning docs only
**Goal chain**: umbrella goal (Qwen3.6 35B GGUF execution — sole priority) -> delivery authority GGUF-M3 -> this unit graph. Both registered in Vivi; no new goal forge or goal-check needed — MODEL-03 is a mandatory campaign row already shaped by the campaign and the delivery authority.
**Freshness**: derived from the source delivery `30f32ef` (the exact frozen text), the umbrella campaign, the delivery authority, the live gradus tree at this branch tip, the pinned llama.cpp comparator contract, and the GI0 numeric-contract methodology. No planner-1..19 partial artifact or cancelled transcript was reused.

## 1. Re-Lower Decision

The source delivery lowered GGUF-M3 as **one** delivery-sized Hand task (est 36k–72k) whose §4 stage graph S0–S7 was *intra-unit*: one seat carried schedule + state values + two math families + trunk + oracle harness + executed proof. Under the standing Hand-unit law (one logical change per Hand; turnover, not throughput-max), that bag is too large: dependents (MODEL-04, EXEC-03) would sit idle behind a multi-hour single seat, and a single divergence anywhere in the chain would park the whole unit.

This re-lower splits S0–S7 at the **stage boundaries**, which are already one-logical-change boundaries:

| Source stage | Re-lowered unit | One logical change |
| --- | --- | --- |
| S0 schedule authority | **M3-U1** | Layer-schedule authority (F1, F7 recognition) |
| S1 state values | **M3-U2** | Conv + recurrent + KV state values (F2/F6/F8 substrate) |
| S2 Gated DeltaNet | **M3-U3** | SSM update + gated output math for one layer (F2) |
| S3 gated attention | **M3-U4** | Full-attention layer + KV position state (F3) |
| S4 position handling | **M3-U5** | Multi-section RoPE (F4) |
| S5 equivalence/reset/replay | **M3-U6** | 40-layer trunk: prefill/decode equivalence, reset/replay, MTP nonexecution (F5/F6/F7) |
| S6 oracle probe harness | **M3-U7** | Pinned llama.cpp per-layer probe + comparison script (evidence side) |
| S7 executed proof | **M3-U8** | Executed per-layer agreement + receipts + closeout (terminal) |

The source stage graph serialized S0 → S1 → {S2, S3, S4} → S5 → S6 → S7. The unit graph below keeps that spine but makes the safe branches explicit and parallel where write surfaces are disjoint (§Parallelism).

## 2. Unit Identity

| Field | Value |
| --- | --- |
| Umbrella row | **MODEL-03** — "Implement hybrid SSM/attention state" |
| Umbrella done oracle | Per-layer prefill and decode state/output match the independent oracle; reset/replay are deterministic |
| Delivery unit | **GGUF-M3** — Hybrid SSM And Attention State |
| Delivery done oracle | Per-layer prefill and one-token decode state and outputs match the independent oracle at the first-divergence boundary; reset and replay are deterministic |
| Owner | Gradus (implementation); radix evidence lane (oracle harness/receipts) |
| Depends on (dispatch gate) | **MODEL-01 (GGUF-M1)** — `qwen35moe` admission + tensor map (the consumed typed config); transitively GGUF-A1c (LIB-01 clean break), GGUF-A2 (LIB-02), GGUF-A3 (LIB-03 windowed materialization), GGUF-A5 (KV prefill/decode semantics) |

**Boundary (unchanged from the source)**: MODEL-03 ends at the per-layer **attention-subblock** agreement — pre-FFN residual stream state and output. The MoE FFN (MODEL-02), full-model composition/logits/sampling (MODEL-04), native Metal/CUDA (GGUF-M5), GPU kernels (EXEC-02), HTTP, and serving stay out. The state substrate MODEL-03 lands is what MODEL-04 composes and EXEC-03 keeps resident.

## 3. Normalized Spec (preserved verbatim from the source task)

The functional requirements F1–F8 are carried intact; no clause is softened:

- **F1 — Layer schedule.** Derive from the **admitted MODEL-01 typed config** (never re-derived from raw metadata) which GGUF block is SSM, full attention, or MTP; validate against each block's tensor inventory. Pinned gate row: blocks 0..39, **SSM iff `(i + 1) % full_attention_interval != 0`** (full attention at `i ∈ {3,7,…,39}` — **10 attention layers**; the other **30 are SSM**), **block 40 = MTP** (`nextn_predict_layers` = 1). The derivation must also hold for heretic/ornith (733 tensors, `block_count` 40). A tensor inventory contradicting the derived type **fails closed** with a typed diagnostic naming the block and the first contradictory tensor.
- **F2 — SSM layer state (never conflated with KV).** Typed recurrent state `S ∈ [32, 128, 128]` (value heads × key head dim × value head dim; `state_size` 128, `time_step_rank` 32) and typed convolution state (last `conv_kernel − 1` = 3 channel slices of the 8192-channel qkv space). Gated DeltaNet update/output (L2-normed q/k, head repetition 16→32, sigmoid beta, `softplus(alpha + dt_bias) × A` decay gate, gated output RMSNorm over `z` with SiLU, output projection) must follow the oracle exactly; the exact algebraic form is settled by the first-failing oracle case, not by independent derivation.
- **F3 — Attention KV state.** Typed per-layer KV value on full-attention layers only: 2 KV heads × 256 per position; gated full-attention semantics (joint Q/gate projection, RMSNorm on Q and K, multi-section RoPE, sigmoid-gated output, output projection). KV appends one position per decode step; prefill and one-token decode agree at the declared boundary (GGUF-A5 contract applied to the gated form).
- **F4 — Position handling.** Multi-section RoPE, sections `[11, 11, 10, 0]`, `dimension_count` 64, `freq_base` 10,000,000, `partial_rotary_factor` 0.25.
- **F5 — Prefill / one-token decode equivalence.** The 40 trunk layers run in prefill over a pinned token sequence must produce, **per layer and per position**, the same state and attention-subblock output as incremental one-token decode replaying the same sequence.
- **F6 — Reset and replay.** Fresh-session construction (empty conv state, zero recurrent state, empty KV, generation-counter restart) and deterministic replay: same pinned prompt + same session identity → identical per-layer state and outputs. Executed, not merely structural.
- **F7 — MTP block recognition.** Block 40 (NextN/MTP) recognized and admitted in the schedule, carries its own tensor inventory (`nextn.*`, full-attention-style q/k/v), and is **not executed in the main trunk pass** — matching the oracle, which runs only blocks 0..39 in the main graph.
- **F8 — Session identity.** The hybrid state carries an identity key covering model, model version, execution config, tokenizer identity, layer schedule, per-layer state types, and dtype — mirroring the `IdentitasCache` precedent — so EXEC-03 can bind two prompts to one resident session without reload.

**Constraints (unchanged)**: device neutral (no device handle/path/residency in any Gradus value); executed proof required (compilation/documentation support but never replace the per-layer oracle agreement); no dual authority (schedule and state semantics owned by these modules; MODEL-04 consumes, never re-derives); no silent F32-expansion claim, no performance claim.

**Non-goals (unchanged)**: MoE router/expert math (MODEL-02), tokenizer (LIB-02), storage codecs/materialization (LIB-03), full-model logits/sampling (MODEL-04), GPU kernels (EXEC-02), native Metal/CUDA (GGUF-M5), HTTP, serving.

## 4. Repo-Aware Baseline (verified live 2026-08-13)

- Branch `factory/planner-36` at `1462cd874bb` (merge-base with `factory/merge`), tree clean.
- `src/model/` has **no** `qwen35moe*` module and no `tensor_view`/`tensor_payload` — **MODEL-01 (GGUF-M1) and LIB-03 (GGUF-A3) are not landed** on any `factory/planner-*` branch at this boundary (confirmed: `a7d7bcd` on `factory/planner-23`, `04119b1` on `factory/planner-25` only). Dispatch is gated accordingly (§Entry Gate).
- `src/cache.fab` (PML5-U2) — single-block structural `KVCache` with append/reset and identity-key wire; **single-block only, no recurrent/conv state** — the F8 identity precedent and the F3 KV extension surface, not a substitute for F2.
- `src/nn.fab` — public `linear`, `gelu`, `layernorm`; **no `silu`, no RMSNorm** (MODEL-02's silu row and REF-01 nn rows are planned elsewhere; shared-file discipline applies, §Write-Scope Note).
- `src/attention.fab` — dense-row RoPE at `freq_base 100000` (GI3 recipe) for the dense reference rows; the qwen35moe **multi-section** RoPE is a distinct rotary variant and gets its own module (M3-U5) — no edit to the dense RoPE, no dual authority.
- `src/model/gguf_manifest.fab` (GGUF-A1b) landed — the manifest surface schedule validation can consume at red-proof time, though U1's schedule authority reads the **admitted MODEL-01 typed config**.
- `mir-library-imports` goal is **implemented** (gradus `CAMPAIGN.md` row: "linked `gradus:*` calls through FMIR and consumer proof") — the FMIR imported-call seam is a **recheck handle**, not a presumed blocker (§FMIR Gate).
- Oracle pins (delivery-authority chain): llama.cpp build **10150** (`dee2a846b`), same lineage as the GI0 comparator pin; GI0 numeric contract (first-divergence rule, finite-value gate, band-derivation method) re-derived for the Qwen3.6 row's EOG set `{248046, 248044}` at dispatch.
- Pinned artifact facts (recorded in the source delivery §3.1 and the A1b receipt): SHA-256 `0b21525e…7dac58b`, 753 tensors, `block_count` 41, `full_attention_interval` 4, `nextn_predict_layers` 1, ssm `conv_kernel` 4 / `state_size` 128 / `time_step_rank` 32 / `inner_size` 4096, rope sections `[11,11,10,0]` / dim 64 / `freq_base` 10,000,000.

### Entry Gate (dispatch)

Before any M3 unit is dispatched: GGUF-A1c (LIB-01), GGUF-A2 (LIB-02), GGUF-A3 (LIB-03 union codecs + windowed materialization), **GGUF-M1 (MODEL-01)** admission + tensor map, GGUF-A5 KV prefill/decode semantics — the source task's named predecessor receipts. MODEL-03 is not executable before MODEL-01's typed config exists; the schedule/state facts are consumed from the admitted model. **Recheck handles**: the GGUF-M1 closeout record; the GGUF-A3 closeout for the codec set.

### Write-Scope Note (shared files)

`src/nn.fab` is contended with MODEL-02 (silu row) and REF-01 (planned nn rows). M3 units add an nn row (**`silu`, `rmsnorm`**) **only if absent at the unit boundary**, hunk-serialized via landed-commit boundaries (the MODEL-02 precedent); if MODEL-02's `silu` lands first, M3 consumes it — no duplicate row, no dual authority. `src/cache.fab` is read-only reference (identity precedent); the qwen35moe KV state is a new typed value in the state/attention modules, not a rewrite of the PML5-U2 surface.

## 5. Micro-Unit Graph (one logical change per unit)

Units are listed in dependency order. Fields follow the standing Hand-unit schema; every unit carries `est_work_tokens` 3k–8k and **1–3 primary files**. None carries a lane gate (§Aggregate Gate). Final module file names follow MODEL-01's `qwen35moe` naming at dispatch; the names below are the recommended shape.

### M3-U1 — Layer-schedule authority (S0)

- **outcome**: one module derives per-block type (SSM / full-attention / MTP) from the admitted `qwen35moe` typed config and validates it against each block's admitted tensor inventory; contradictory inventory fails closed with a typed diagnostic naming the block and the first contradictory tensor.
- **write_scope**: `gradus/src/model/qwen35moe_schedule.fab`, `gradus/src/model/qwen35moe_schedule.proba`; own docs rows (`docs/module-map.md`, `docs/api-reference.md`, `docs/diagnostics.md`).
- **done_when**: for the exact Qwen3.6 artifact the derived schedule is SSM on the 30 layers `(i+1)%4 != 0` of blocks 0..39, full attention on `{3,7,…,39}`, block 40 = MTP; validation passes against the admitted tensor inventory for the gate row and compiles for the heretic/ornith stress rows; a mutated/contradictory inventory yields the typed diagnostic naming block + first tensor; `.proba` green.
- **depends_on**: MODEL-01 (GGUF-M1) admission + tensor map.
- **sanity**: one narrow proba run over the schedule cases.
- **non_goals**: state values, update/attention math, trunk composition.
- **risk**: low — schedule facts are pinned by admission; derivation is a pure function over the typed config.
- **integrable**: yes.
- **est_work_tokens**: 3k–5k.

### M3-U2 — Conv + recurrent + KV state values (S1)

- **outcome**: typed state values — recurrent `S [32,128,128]`, convolution state (last `conv_kernel − 1` = 3 slices of the 8192-channel qkv space), and KV position slots — with construction, append/update, reset, strict equality, and the F8 identity key (model, version, config, tokenizer, schedule fingerprint, per-layer state types, dtype). The schedule fingerprint is a **constructor parameter (textus)**, not a re-derivation — so this unit does not import the schedule module.
- **write_scope**: `gradus/src/model/qwen35moe_state.fab`, `gradus/src/model/qwen35moe_state.proba`; own docs rows.
- **done_when**: fresh-session construction yields empty conv, zero recurrent, empty KV; append/update mutate per the typed contract; reset returns the fresh-session value; equality is strict; identity round-trips; no device handle, path, or reader in any value; `.proba` green.
- **depends_on**: MODEL-01 (state/conv/KV dimension facts).
- **sanity**: one narrow proba run (mutation + reset + identity cases).
- **non_goals**: the update/output math (U3), attention math (U4), schedule derivation (U1).
- **risk**: low.
- **integrable**: yes.
- **est_work_tokens**: 3k–5k.

### M3-U3 — Gated DeltaNet update and output math (S2)

- **outcome**: one SSM layer's recurrent update + gated output path — L2-normed q/k, head repetition 16→32, sigmoid beta, `softplus(alpha + dt_bias) × A` decay gate, gated output RMSNorm over `z` with SiLU, output projection — following the oracle algebra exactly (form settled by the first-failing red case).
- **write_scope**: `gradus/src/model/qwen35moe_deltanet.fab`, `gradus/src/model/qwen35moe_deltanet.proba`; `src/nn.fab`/`src/nn.proba` **only if** `silu`/`rmsnorm` absent at the boundary (hunk-serialized); own docs rows.
- **done_when**: on pinned hidden-state probes with pinned tensor slices, the update and output match the committed independent reference (gi2-dequant-reference precedent: f64 oracle over the real artifact's dequantized tensors → committed goldens) under the settled band; negative matrix (non-finite input, shape mismatch) fails typed; `.proba` green.
- **depends_on**: M3-U2, MODEL-01.
- **sanity**: one narrow proba run on a pinned probe.
- **non_goals**: attention/KV math (U4), RoPE (U5), schedule (U1).
- **risk**: medium — exact algebraic form is settled by the first-failing oracle, never by independent derivation.
- **integrable**: yes.
- **est_work_tokens**: 5k–8k.

### M3-U4 — Gated full-attention + KV state (S3)

- **outcome**: one full-attention layer with per-position KV state on the 10 attention layers — joint Q/gate projection, RMSNorm on Q and K, multi-section RoPE on Q/K (consumes U5), sigmoid-gated output, output projection; KV appends one position per decode step; prefill and one-token decode agree at the declared boundary (GGUF-A5 gated form).
- **write_scope**: `gradus/src/model/qwen35moe_attention.fab`, `gradus/src/model/qwen35moe_attention.proba`; own docs rows.
- **done_when**: on pinned probes, per-position KV append/update/reset holds; the gated attention-subblock output matches the committed independent reference under the settled band; KV state remains a typed logical value; `.proba` green.
- **depends_on**: M3-U2 (state values), M3-U5 (multi-section RoPE), MODEL-01.
- **sanity**: one narrow proba run (KV append + one gated output probe).
- **non_goals**: SSM update math (U3), schedule (U1), trunk composition (U6).
- **risk**: medium.
- **integrable**: yes.
- **est_work_tokens**: 5k–8k.

### M3-U5 — Position handling, multi-section RoPE (S4)

- **outcome**: multi-section RoPE (sections `[11,11,10,0]`, dim 64, `freq_base` 10,000,000, `partial_rotary_factor` 0.25) applied to Q/K of attention layers, as a standalone module the attention layer consumes.
- **write_scope**: `gradus/src/model/qwen35moe_rope.fab`, `gradus/src/model/qwen35moe_rope.proba`; own docs rows.
- **done_when**: RoPE of pinned position vectors matches the committed independent reference under the settled band; the dense `gradus:attention` RoPE (`freq_base` 100000) is untouched; `.proba` green.
- **depends_on**: MODEL-01 (rope facts).
- **sanity**: one narrow proba run.
- **non_goals**: attention/KV math (U4), any edit to the dense RoPE surface.
- **risk**: medium.
- **integrable**: yes.
- **est_work_tokens**: 3k–5k.

### M3-U6 — 40-layer trunk: prefill/decode equivalence, reset, replay, MTP nonexecution (S5)

- **outcome**: the trunk runner composes schedule (U1) + state values (U2) + Gated DeltaNet (U3) + gated attention with KV (U4) + RoPE (U5) over the 40 main layers; MTP block 40 is recognized and **excluded from the main pass**; prefill and one-token decode agree per layer and per position; fresh-session reset and deterministic replay execute; F8 session identity binds.
- **write_scope**: `gradus/src/model/qwen35moe_trunk.fab`, `gradus/src/model/qwen35moe_trunk.proba`; own docs rows.
- **done_when**: over a pinned token sequence, per-layer prefill state and attention-subblock output equal incremental one-token decode replayed through the state machinery (per layer and per position); fresh-session reset and same-prompt replay reproduce identical per-layer state and outputs; block 40's tensors are admitted but never executed in the trunk pass; `.proba` green.
- **depends_on**: M3-U1, M3-U3, M3-U4 (transitively M3-U2, M3-U5), MODEL-01.
- **sanity**: one narrow proba run (equivalence + replay determinism).
- **non_goals**: the oracle probe (U7), the executed agreement (U8), full-model composition (MODEL-04).
- **risk**: medium-high — the composition point; equivalence must hold at the attention-subblock boundary.
- **integrable**: yes.
- **est_work_tokens**: 6k–8k.

### M3-U7 — Pinned llama.cpp per-layer oracle probe harness (S6, evidence side)

- **outcome**: bounded instrumentation of the pinned llama.cpp build (**10150 / `dee2a846b`**) that dumps the named per-layer tensors (`attn_norm`, `q_conv`, `k_conv`, `v_conv`, `gate`, `state_predelta`, `conv_output`, `linear_attn_out`, `Qcur`, `Kcur`, `Vcur`, `attn_pregate`, `attn_gated`, `attn_output`, pre-FFN residual per layer) for a pinned prompt, plus the per-layer comparison script implementing the first-divergence rule, finite-value gate, and settled band.
- **write_scope**: radix evidence lane — `radix/docs/factory/gpu-inference-gguf/evidence/` (probe build notes, dump script, comparison script, pinned build binary SHA-256); operator-local `/Users/ianzepp/Ai/models/` is read-only evidence, never committed. **No gradus write.**
- **done_when**: the probe dumps the named tensors for the pinned prompt at the pinned build with recorded binary identity; the comparison script reports per-layer/per-position agreement with `DIVERGENCE=none` or the named first layer/position + failing thresholds; the Qwen3.6 EOG/numeric re-derivation (§Oracle) is recorded.
- **depends_on**: pinned llama.cpp build 10150 present locally; pinned artifact identity; GI0 numeric-contract methodology.
- **sanity**: probe runs on one layer to validate plumbing.
- **non_goals**: gradus code of any kind, full-model logits, device claims.
- **risk**: medium — probe-build friction; the source task's open question about `cb()` hook feasibility (§Open Items).
- **integrable**: yes (evidence-only).
- **est_work_tokens**: 6k–8k.

### M3-U8 — Executed per-layer agreement proof + receipts (S7)

- **outcome**: executed comparison of the Gradus trunk per-layer state/output vs the pinned probe dump for one pinned prefill prompt and one one-token incremental decode, at every layer and position up to the first-divergence boundary; reset/replay determinism probes; receipts committed; docs closeout.
- **write_scope**: `gradus/exempla/qwen35moe-layer-probe/` (`faber.toml`, `src/main.fab`, `README.md` + receipt), `scripta/check-compile` (+ `.fab`) exemplar target, `docs/regression-corpus.md` (corpus/suite totals bump), `docs/factory/production-ml-library/pml0-symbol-inventory.md`, `docs/factory/production-ml-library/pml0-support-matrix.md`, the delivery-authority status line and gradus `CAMPAIGN.md` status line; radix evidence receipts (per ownership contract, Gradus owns no oracle harness).
- **done_when**: the per-layer comparison reports agreement at every layer/position up to the first-divergence boundary with `DIVERGENCE=none` (or an honest named first layer/position + failing thresholds); reset/replay determinism probes pass; receipts committed in evidence; `git diff --check` silent.
- **depends_on**: M3-U6, M3-U7; EOG/numeric re-derivation frozen at dispatch (§Oracle).
- **sanity**: the exemplar's own PASS lines; `git diff --check`.
- **non_goals**: full-model logits/tokens/text (MODEL-04), native execution (GGUF-M5), any edit to MoE/router surfaces (MODEL-02).
- **risk**: high — executed proof over the 22.6 GB artifact; FMIR seam recheck; oracle-load and probe friction.
- **integrable**: yes (terminal unit).
- **est_work_tokens**: 6k–8k.

## 6. Parallelism Analysis (S0/S1 and the first frontier)

**Safe S0/S1 parallelism — YES, separable.** M3-U1 (S0) and M3-U2 (S1) are parallel-safe:

- **Disjoint write surfaces**: `qwen35moe_schedule.{fab,proba}` vs `qwen35moe_state.{fab,proba}` — no shared primary file.
- **Shared dependency only**: both consume the admitted MODEL-01 typed config and nothing else; neither reads the other's module.
- **The F8 identity seam**: the state identity key includes the layer schedule, but U2's identity constructor takes the schedule as a **`textus` fingerprint parameter** (the fingerprint the schedule module and MODEL-04 derive from the same admitted facts), so U2 does not import U1's module and does not re-derive the schedule. The schedule authority remains singular (U1 / consumed by MODEL-04) — no dual authority is introduced.
- **No ordering constraint**: nothing in U2's mutation/reset/identity semantics depends on U1's derivation.

Fallback if the audit prefers strict seriality: reorder U1 → U2 and give U2 a `depends_on` on U1 — the two units otherwise unchanged. Recommended disposition: **parallel**.

**First eligible frontier after MODEL-01** (see §10): **{M3-U1, M3-U2, M3-U5, M3-U7}** — the units whose dependencies are satisfied by MODEL-01 alone (plus the landed GGUF-A set). U1∥U2∥U5∥U7 are disjoint (`schedule` / `state` / `rope` / evidence-only). M3-U5 (RoPE) is pushed early because it is a standalone position-handling module U4 consumes; U7 is evidence-side and independent of all gradus code.

**Second frontier**: {M3-U3, M3-U4} — U3 needs U2; U4 needs U2 + U5 (disjoint from U3). **Third**: M3-U6 (needs U1, U3, U4). **Fourth**: M3-U8 (needs U6 + U7). Parallel Hand seats never share a primary write file.

## 7. Aggregate Gate And Lane-Owned Validation

**One aggregate gate, no child lane gates.** The GGUF-M3 completion is checked exactly once at the aggregate: **merge** integrates the landed M3 unit set (U1–U8) onto `factory/merge` and the GGUF-M3 done oracle — the executed per-layer agreement under the first-divergence rule (U8 receipt) with reset/replay deterministic — is accepted, with docs/status lines consistent. No M3 child unit carries `./scripta/check-source`, `./scripta/check-compile`, package `faber check`, `--stage`, `--e2e`, `--full`, or any broad suite; each child's `sanity` is one narrow proba of its own surface.

Lane-owned gates (named once, owned by their lanes):

- **lint** — `./scripta/check-source` (stages 1–2) over the landed unit set.
- **test** — `faber check` + broad proba suites (stages 3–6) over the landed unit set.
- **merge** — integration onto `factory/merge` + build stability + the aggregate acceptance above.
- **closeout (factory)** — `python3 ../radix/scripta/generate-factory-readme.py --factory-root docs/factory --check` and `./scripta/check-factory-goal-status --fail-on error` at the aggregate, not on children.

## 8. Oracle, EOG/Numeric Authority, FMIR Gate

- **Pinned per-layer oracle**: llama.cpp **10150 (`dee2a846b`)** — the pinned comparator lineage of the GI0 pin; binary SHA-256 recorded at probe build (M3-U7). The probe dumps the named per-layer tensors (main pass only; MTP loader admitted but not executed in the main graph). M3-U8 compares Gradus state/output vs the probe under the **first-divergence rule** (first layer/position recorded, never hidden by text-level similarity) and the **finite-value gate**.
- **EOG/numeric authority**: the GI0 numeric-contract thresholds were derived for SmolLM2; the Qwen3.6 row **re-derives at dispatch** using the gi0-6 method — EOG set `{248046, 248044}`, band `Δ` from the repeatability floor F and representational floor `u` (10·R → next power of ten), band capped by the gradus forward band / matmul numeric-policy floor for the component values. The re-derivation is a **dispatch-time action on M3-U7** (freezes the comparison policy) and a precondition of M3-U8.
- **FMIR imported-call gate**: `mir-library-imports` is implemented (gradus `CAMPAIGN.md` row), so the seam is expected to resolve intra-library calls — but the source task's historical stepper limitation must be **re-verified at red-proof time** (M3-U6 proba, M3-U8 exempla). If the executed proof is blocked, the blocker routes to hand-2/Faber per campaign execution rule 6 — MODEL-03 does not work around it.

## 9. Successor Preservation Through CLOSE-01

Nothing in this re-lower narrows, downgrades, defers, makes optional, or moves admitted Qwen work outside the completion chain:

- GGUF graph: `M1 → M2 ‖ M3`; `M2 + M3 → M4` (MODEL-04 composes the trunk + state substrate per layer), `M4 → M5` (native Metal/CUDA), `M5 → M6` (Faber capstone + closeout). Upstream: `A1c → A2 ‖ A3 → A4/A5/A6 → M1`.
- Umbrella rows: MODEL-03 → MODEL-04 → EXEC-01/02 → EXEC-03 → CAP-01/02 → CLOSE-01. EXEC-03 binds the hybrid state (SSM/conv/KV) resident across two prompts through the F8 identity key.
- The per-layer agreement proven here is re-validated end-to-end at MODEL-04's full-model boundary against the same pinned comparator; a divergence there routes back to this surface with the first-divergence record, never a silent match.
- Milestone advanced: **Q2 — complete model semantics** (gates A4–A6 and M1–M4). GGUF-M3 completes the SSM/attention half of the `qwen35moe` semantics parallel to MODEL-02's MoE half. Q4 (the Faber invariant) stays mandatory with every clause intact.

## 10. First Eligible Frontier After MODEL-01 (report)

Once the **GGUF-M1 (MODEL-01) receipt** lands (and the GGUF-A1c/A2/A3/A5 dispatch gate is met), the first dispatch-eligible M3 units are:

```text
{M3-U1 schedule authority, M3-U2 state values, M3-U5 multi-section RoPE, M3-U7 oracle probe harness}
```

All four depend only on MODEL-01 (plus the landed GGUF-A set); M3-U7 depends on no gradus code at all. They form a 4-way parallel Hand frontier on disjoint write surfaces. Frontier 2 = {U3, U4} (U3→U2; U4→U2+U5). Frontier 3 = {U6} (U1+U3+U4). Frontier 4 = {U8} (U6+U7). MODEL-02 runs in parallel on its disjoint MoE surface throughout.

## 11. Open Items For Mind (none blocks this lowering)

1. **MODEL-01 (GGUF-M1) landing** — the dispatch gate; recheck at the GGUF-M1 closeout (§Entry Gate).
2. **GGUF-A3 (LIB-03) landing** — the union codec set + windowed materialization the probe/math units consume; recheck at the A3 closeout.
3. **Oracle probe mechanism (dispatch-time)** — prefer the bounded `cb()`-hook instrumentation built from the pinned llama.cpp source (dee2a846b); the fallback (full-model first-divergence attribution + per-layer self-consistency) is accepted only by the delivery audit before it replaces the probe.
4. **EOG/numeric re-derivation** — Qwen3.6 EOG set `{248046, 248044}` + band re-derived at dispatch via the gi0-6 method (§Oracle).
5. **Module naming** — final file names follow MODEL-01's `qwen35moe` naming once it lands; this spec's names are the recommended shape.
6. **FMIR seam recheck** — the historical stepper limitation must be re-verified at red-proof time; `mir-library-imports` is implemented, expected closed (routing decision, not a design change).

## 12. Scope Closure Statement

**Milestone advanced**: Q2. **Why unit completion is not campaign completion**: the campaign invariant is the exact-artifact end-to-end Faber capstone on Metal and CUDA (`CAP-01`/`CAP-02`) gated by `CLOSE-01`. GGUF-M3 proves the per-layer state substrate only; the MoE FFN (MODEL-02), full-model reference inference (MODEL-04), package/device plans (EXEC-01), packed kernels (EXEC-02), and resident sessions (EXEC-03) remain mandatory successors. The state module is the consumption surface MODEL-04 composes and EXEC-03 binds resident. Nothing in this lowering moves admitted Qwen work outside the campaign completion chain.

---
*Planning artifact only. No product code was written by this lowering. GGUF-M3 is re-lowered from the planner-27 `30f32ef` single task into eight one-logical-change Hand units (M3-U1…U8, 3k–8k each); S0/S1 (U1∥U2) is analyzed as safely parallel; one aggregate gate, no child lane gates; the exact 30 SSM / 10 attention trunk schedule, MTP recognition/nonexecution, state updates, KV/position, prefill/decode/reset/replay, pinned per-layer oracle, EOG/numeric authority, and FMIR imported-call gate are preserved; every successor through CLOSE-01 is preserved. Dispatch is gated on MODEL-01 (GGUF-M1) and the GGUF-A1c/A2/A3/A5 predecessor set; first eligible frontier after MODEL-01 = {M3-U1, M3-U2, M3-U5, M3-U7}.*
