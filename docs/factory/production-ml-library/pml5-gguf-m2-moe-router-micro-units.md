# Delivery Lowering — GGUF-M2 (MODEL-02) Micro-Unit Re-Split: MoE Router And Expert Execution

**Status**: SUPERSEDED 2026-08-22 by [`pml5-gguf-m2-moe-router-delivery-2026-08-22.md`](pml5-gguf-m2-moe-router-delivery-2026-08-22.md) — re-lowered against live main after the MODEL-01 merge (unit A1 silu landed; Latin surface spellings retracted; baseline re-verified). Successor implementation note: MODEL-02-U3–U6 landed on gradus main at `b1ccfc8`; U7's real-artifact adapter/receipt and U8's documentation closeout remain successor work. Frozen semantics (§2) inherited by the successor.

**Planner**: planner-35. **Assignment**: task `688393b5` (Mind,
2026-08-13T20:38:52+00:00): re-lower the fresh Qwen MODEL-02 MoE
router/expert-execution delivery into one-logical-change Hand units before
audit. **Cited source**: planner-26 lowering
[`pml5-gguf-m2-moe-router-delivery.md`](pml5-gguf-m2-moe-router-delivery.md)
at commit `74c7af2` (fresh lowering — independently derived from campaign,
delivery authority, live repos, the pinned llama.cpp source checkout, and the
real local artifact; no cancelled planner-1..19 work, commit, partial
artifact, or transcript read).
**Campaign**: [`radix/docs/factory/gpu-production-readiness/CAMPAIGN.md`](../../../../radix/docs/factory/gpu-production-readiness/CAMPAIGN.md)
(row `MODEL-02` — "Implement MoE router and expert execution").
**Delivery authority**: [`pml5-general-gguf-delivery.md`](pml5-general-gguf-delivery.md)
§GGUF-M2.
**Predecessors**: MODEL-01 (GGUF-M1 admission chain) — **the whole MODEL-02
chain dispatches only after the MODEL-01 aggregate gate (G1) lands**, which
lands after the **LIB-02 + LIB-03** aggregate gates **only** (campaign
dependency graph; REF-01 is a sibling of MODEL-01, not a predecessor, and
does not gate its dispatch). MODEL-02 also consumes LIB-03's windowed
`TensorView`/`materialize_slice` surface (codec set + windowed reads) and
resolves A1's `silu` against the sibling REF-01 (GGUF-A4 dense primitives) by
consume-or-add — neither is a MODEL-01/MODEL-02 dispatch gate.
**Repo baselines**: Gradus `1462cd8` (lane tip, tree clean — verified; equals
`factory/merge` HEAD); Radix `b6d6e17c8`; Hosts `57d659d`; Faber `1fb6cc9`.
Oracle tool `llama-tokenize`/`llama-gguf` 10150 (`dee2a846b`) live on this
host.

**Amendments**: task `57c57d14` / audit `c7e9a272` (2026-08-13) —
dependency-frontier correction (`936bb9d`; REF-01 sibling, A1 early
eligibility). Task `f7ae2d38` / audit `524eb154` (2026-08-14) —
campaign-rule-2 field-set verification: per-unit `stop condition` rows added
(§4), field residence mapped (§11), F3 divergence-authority confirmed as an
explicit open item (§13.1).

## 1. Goal-check verdict (compact)

- **Goal path**: campaign mandatory work row `MODEL-02`, depends on MODEL-01
  (campaign dependency table); umbrella goal
  `gol_634a0417d02c510f` (Qwen3.6 35B GGUF execution — sole priority) ->
  PML5-GGUF delivery-authority goal `gol_67b635603712f01b` -> this unit.
- **Evaluator mode**: goal-check of the cited fresh GGUF-M2 delivery against
  the delivery authority and the live gradus worktree, plus a scope-shape audit.
- **Intended consumer**: delivery (Mind dispatches the micro-unit Hands).
- **Verdict**: **READY**.
- **Reasoning**: the cited plan is one coherent unit at 20k–36k
  est_work_tokens — beyond the turnover law's 3–8k / one-behavior-family
  shape. Its outcome is re-split — **not re-scoped**. Every frozen fact below
  (artifact identity, the eight-step MoE semantics, deterministic tie rule,
  top-k probability selection and `norm_w=true` weight renormalization, the
  shared-expert sigmoid gating, the exact rank-3 tensor mapping and storage
  union, the 41-block layer schedule with block-40 MTP exclusion, the four
  selected probe layers, the comparison policy, and the successor chain) is
  retained verbatim from the cited delivery. The done oracle (selected layers
  match independent router choices, expert weights, intermediate values, and
  outputs for pinned hidden-state probes) is preserved as unit **B4** plus
  the executed exemplar **C1** and the aggregate gate **G1**, so
  `factory/merge` never observes a MoE surface that cannot satisfy its own
  component-level oracle.
- **Key points**: `src/model/moe.fab`/`.proba` do not exist (confirmed — the
  module is entirely new); `src/nn.fab` has **no** public `silu` row
  (confirmed — only `linear`/`gelu`/`layernorm` + fixed-shape rows; the
  self-hosted `_exp` precedent exists at `:251`); `gradus:model/tensor_view`
  (the LIB-03 `TensorView`/`materialize_slice`/`SourceRead` surface)
  does not exist in this tree yet (LIB-03 is lowered at `a7d7bcd`, not
  landed); `exempla/moe-router-probe` does not exist; `fixtures/gguf/` has no
  `gen_moe_*` files. Every split surface is locatable and each micro-unit has
  exactly one behavioral outcome.
- **Blocking gaps**: none for the split itself. Dispatch serialization: the
  MODEL-01 aggregate gate lands after the **LIB-02 + LIB-03** aggregate gates
  only (REF-01 is a sibling, not a MODEL-01 predecessor); **A1 is
  independently eligible before MODEL-01** (disjoint `src/nn.fab`/`.proba`,
  silu consume-or-add against the sibling REF-01 only), while the remaining
  first-wave units (A2 ∥ B1) base on `factory/merge` **after the MODEL-01
  aggregate gate lands**. This artifact is lowered now so the units are
  implementation-ready when those receipts arrive; it does not claim
  predecessor completion.

## 2. Interpreted scope (frozen, verbatim from the cited plan)

Lower mandatory campaign work **MODEL-02 — implement MoE router and expert
execution** into an implementation-ready micro-unit graph for Gradus. The
completion oracle is: **selected layers match independent router choices,
expert weights, intermediate values, and outputs for pinned hidden-state
probes.** Nothing below narrows, downgrades, defers, or makes optional any
admitted Qwen work.

### Artifact identity (frozen)

| Fact | Value |
| --- | --- |
| File | `Qwen3.6-35B-A3B-UD-Q4_K_M.gguf` (provenance only) |
| Byte length | 22,663,387,424 |
| SHA-256 | `0b21525e972670ed59e1812e170b27c26355381f0656ecc4e25617ece7dac58b` |
| Architecture | `qwen35moe` |
| Data offset | 10,991,392 |
| Tensor count | 753 |
| `block_count` | **41** (40 main trunk + 1 MTP layer 40, `nextn_predict_layers` = 1) |
| `embedding_length` | 2048 |
| `expert_count` | 256 |
| `expert_used_count` | 8 |
| `expert_feed_forward_length` | 512 |
| `expert_shared_feed_forward_length` | 512 |
| `expert_weights_scale` | **absent** — no per-expert weight scaling (`w_scale` stays 0.0f; scale step skipped) |

### MoE tensor facts (frozen, per-layer survey of the live artifact)

GGUF shapes as parsed (`ne[0]` = contiguous dimension); the `blk.N.` prefix
covers every layer including the MTP layer 40:

| Tensor | GGUF shape | GGML storage (layers) | Role |
| --- | --- | ---: | --- |
| `blk.N.ffn_gate_inp.weight` | `[2048, 256]` | F32 (0–39), **BF16 (40)** | router weight |
| `blk.N.ffn_gate_inp_shexp.weight` | `[2048]` | F32 (0–39), **BF16 (40)** | shared-expert gate weight (scalar per token) |
| `blk.N.ffn_gate_exps.weight` | `[2048, 512, 256]` | Q4_K (all 41) | routed expert gate projections |
| `blk.N.ffn_up_exps.weight` | `[2048, 512, 256]` | Q4_K (all 41) | routed expert up projections |
| `blk.N.ffn_down_exps.weight` | `[512, 2048, 256]` | **Q5_K** (38 layers), **Q6_K** (34, 38, 39) | routed expert down projections |
| `blk.N.ffn_gate_shexp.weight` | `[2048, 512]` | Q8_0 (all 41) | shared expert gate |
| `blk.N.ffn_up_shexp.weight` | `[2048, 512]` | Q8_0 (all 41) | shared expert up |
| `blk.N.ffn_down_shexp.weight` | `[512, 2048]` | Q8_0 (all 41) | shared expert down |

**Exact rank-3 mapping / storage union (frozen)**: the three rank-3 expert
tensors per block are `ffn_gate_exps`/`ffn_up_exps` `[2048, 512, 256]`
(Q4_K) and `ffn_down_exps` `[512, 2048, 256]` (Q5_K with Q6_K in
blk.34/38/39). Physical layouts used by the MoE path are exactly
**{F32, BF16, Q4_K, Q5_K, Q6_K, Q8_0}** — a subset of the LIB-03 union codec
set **{F32, BF16, Q5_0, Q8_0, Q4_K, Q5_K, Q6_K}**. The BF16 rows exist only
on layer 40 (the MTP layer); probing layer 40 exercises the BF16 codec. No
layout outside the union set appears in the MoE path. All rank-3 expert
window reads go through the LIB-03 `TensorView`/`materialize_slice`
windowed surface with an operation-scoped range source — never a whole
rank-3 tensor materialization.

### Layer schedule + block-40 MTP exclusion (frozen)

From the pinned llama.cpp `load_arch_hparams` (`src/models/qwen35moe.cpp` @
`a957b7747`): `n_main = n_layer − nextn_predict_layers = 40`; layer `i` is
recurrent (Gated DeltaNet) when `i < 40 && (i+1) % 4 != 0` — the 10 main
attention layers are 3, 7, 11, …, 39; the other 30 main layers are SSM; layer
40 is the MTP block. **The MoE FFN is present and identical in shape on every
layer**, consuming the post-attention-norm (post-SSM-norm) hidden state.
MODEL-02 probes the MoE block independently of the attention/SSM family;
MODEL-03 owns the attention/SSM state in front of it. **Block-40 MTP
exclusion (preserved)**: `blk.40` is the sole nextn/MTP block; the main
forward layer schedule is blocks 0..39; MODEL-02 probes layer 40's MoE
tensors **only** as a BF16-codec exercise (its router and shared-expert gate
weights are BF16 there) and makes **no MTP/nextn execution claim** — MTP
execution belongs to the model-execution successors (GGUF-M3/M4).

### Exact MoE semantics (frozen, pinned from llama.cpp @ `a957b7747`)

The reference implementation is the pinned llama.cpp `build_moe_ffn` + the
qwen35moe `build_layer_ffn` (`src/llama-graph.cpp`,
`src/models/qwen35moe.cpp` @ `a957b7747`). For this artifact the invoked path
is, exactly:

1. **Router logits**: `logits = x @ ffn_gate_inp` → `[n_expert]` per token
   (GGML `mul_mat`, no bias — there is no router bias tensor).
2. **Selection probabilities**: `probs = softmax(logits)` over all
   `n_expert` (max-subtracted, f32).
3. **Top-k**: `selected = argsort_desc(probs)[0..n_expert_used)` — the 8
   largest probabilities, in descending-probability order. (Selection by
   probability, not by raw logit; equivalent because softmax is monotonic.)
4. **Weights**: `weights = probs[selected]`, then
   `weights /= max(sum(weights), 6.103515625e-5)` — the `norm_w=true`
   renormalization. No `expert_weights_scale` applies (key absent; scale step
   skipped).
5. **Routed expert FFN** (per selected expert `e`): `gate_e = x @
   ffn_gate_exps[:, :, e]`, `up_e = x @ ffn_up_exps[:, :, e]`, `h_e =
   silu(gate_e) * up_e`, `out_e = h_e @ ffn_down_exps[:, :, e]`.
6. **Accumulation**: `moe_out = Σ_e weights[e] · out_e`.
7. **Shared expert**: `shexp = (silu(x @ ffn_gate_shexp) * (x @
   ffn_up_shexp)) @ ffn_down_shexp`; gate `g = sigmoid(x ·
   ffn_gate_inp_shexp)` (scalar per token).
8. **Layer FFN output**: `ffn_out = moe_out + g · shexp`.

**Top-k normalization (frozen)**: softmax over all `n_expert`; top
`n_expert_used` by probability; selected probabilities renormalized by their
sum with the `6.103515625e-5` guard (`norm_w=true`). **Shared-expert gating
(frozen)**: sigmoid gate from `ffn_gate_inp_shexp`; gated shared-expert
addition completes the layer FFN output.

**Deterministic tie rule (frozen)**: on exact ties in selection probability
at the selection boundary, the **lowest expert index wins** (stable-descending
order). This matches the codebase's existing sampling convention ("first-index
ties", `src/sampling.fab`) and is the rule the pinned reference and Gradus
both implement; a crafted exact-tie probe proves it (`indices=[2,5]`).

**Comparator authority question (preserved verbatim — NOT resolved here)**:
the semantic source for the MoE math is the pinned llama.cpp source checkout
**`/Users/ianzepp/work/ianzepp/llama.cpp` @ `a957b7747`** (`build_moe_ffn`,
`qwen35moe.cpp`, `ggml-quants.c`). The campaign's pinned full-model comparator
is the Homebrew llama.cpp **10150 (`dee2a846b`)** build
(`gi4-engine-comparison-pin.md` — the same build the tokenizer/gguf oracle
tools pin). These are **different revisions for different boundaries**: the
component-level MoE oracle implements the `a957b7747` semantics; the
full-model comparator (10150/`dee2a846b`) is GGUF-M4's boundary. The
authority question — whether the two must agree and which governs any
divergence — is deliberately **preserved as an open audit item** (see §13),
exactly as the citing need `401dd88f` flagged ("campaign oracle uses
10150/dee2a846b while semantic source cites a957b7747"). Note recorded
honestly: llama.cpp's `std::sort`-based argsort is not stable on exact ties
(implementation-defined), so the pinned reference and Gradus share OUR
deterministic rule, and the full-model boundary (GGUF-M4) re-validates
end-to-end against llama.cpp; a real-tie divergence there would be recorded
as a divergence, never silently matched.

### Public surface (frozen, verbatim from the cited plan)

### `gradus:model/moe` — new module `src/model/moe.fab` + `.proba`

```text
importa ex "gradus:model/tensor_view" visum      # GGUF-A3 surface (windowed materialization)

genus ConfiguraMoe {
    numerus n_expertae        # 256 (from MODEL-01 admission; never re-derived here)
    numerus n_usae            # 8
    numerus n_ff_expansio     # 512
    numerus n_ff_shexpansio   # 512
    numerus n_embd            # 2048
}

discretio MoError {
    FormaMismatch { textus message }
    DimensioMala { textus message }
    TypoIgnotum { textus message }
    NomineIgnota { textus message }
    IndexMala { textus message }
    NonFinita { textus message }
    Superfluitas { textus message }
}
functio message(MoError e) → textus

genus SelectioExpertarum {
    lista<numerus> indices        # top-n_usae expert indices, descending-probability order;
                                  # exact ties → lowest index first (deterministic tie rule)
    lista<f32> weights            # normalized weights, same order; sum ≈ 1
    lista<f32> logita             # full [n_expert] router logits (oracle surface)
    lista<f32> probabilitates     # full [n_expert] softmax probabilities (oracle surface)
}

# Router: logits = x @ ffn_gate_inp; softmax over all n_expertae; top-n_usae by
# probability with the deterministic tie rule; weights renormalized by sum
# (norm_w semantics). x is a bounded pinned hidden-state probe [n_embd].
functio eligito(lista<f32> x, visum.TensorView ffn_gate_inp, ConfiguraMoe cfg)
    → SelectioExpertarum ⇥ MoError

# One routed expert's SwiGLU FFN on a bounded hidden-state probe:
#   h = silu(x @ gate_e) * (x @ up_e);  out = h @ down_e
# Reads only the expert-e window of the three rank-3 tensors through the
# operation-scoped range source (never the whole rank-3 tensor).
functio expertum(lista<f32> x, numerus index_expertae,
    visum.TensorView ffn_gate_exps, visum.TensorView ffn_up_exps,
    visum.TensorView ffn_down_exps, ConfiguraMoe cfg,
    (numerus, numerus) → visum.SourceRead fons) → lista<f32> ⇥ MoError

# Complete layer FFN output: routed weighted sum + gated shared expert.
#   moe_out = Σ_e weights[e]·expertum(x,e)
#   g = sigmoid(x · ffn_gate_inp_shexp)
#   shexp = (silu(x @ ffn_gate_shexp) * (x @ ffn_up_shexp)) @ ffn_down_shexp
#   redde moe_out + g·shexp
functio ffn_moe(lista<f32> x,
    visum.TensorView ffn_gate_inp, visum.TensorView ffn_gate_exps,
    visum.TensorView ffn_up_exps, visum.TensorView ffn_down_exps,
    visum.TensorView ffn_gate_inp_shexp, visum.TensorView ffn_gate_shexp,
    visum.TensorView ffn_up_shexp, visum.TensorView ffn_down_shexp,
    ConfiguraMoe cfg, (numerus, numerus) → visum.SourceRead fons)
    → lista<f32> ⇥ MoError
```

`MoError.TypoIgnotum` mirrors the dequant fail-closed rule (un-admitted
physical type before any byte is touched); `NomineIgnota` mirrors the
manifest error for an unknown tensor name; `NonFinita` rejects a NaN/±Inf
probe or intermediate (finite-value gate, gi0-numeric-contract discipline
adapted to component values). No `gradus:model/moe` value owns a path,
reader, source function, or device object.

### `gradus:nn` — additive public primitive (frozen)

```text
# SiLU activation: silu(x) = x · sigmoid(x), self-hosted exp precedent (nn._exp).
functio silu(tensor.Tensor x) → tensor.Tensor ⇥ NnError
```

If REF-01's generic SiLU row lands first, the chain consumes it instead of
adding a duplicate — the shared-file discipline below.

### Normalized spec (unchanged from the cited plan)

1. **Component-level only.** The unit proves router choices, weights,
   intermediate values, and layer outputs for pinned probes. It is **not** a
   full-model, token, logit, or device claim — full-model reference inference
   is GGUF-M4 (MODEL-04), native execution is GGUF-M5/GGUF-A7.
2. **Executed proof at the A1b precedent tier.** A package-MIR exemplar
   (`exempla/moe-router-probe`) prints PASS lines over real tensor slices and
   in-repo fixtures; the independent oracle is a pinned Python reference (the
   gi2-dequant-reference precedent) computing the same MoE math in f32 from
   the real artifact's dequantized tensors, with committed goldens. No token,
   logit, model-execution, or device claim is made here; executed-token/model
   identity remains gated on CTO8-1.
3. **Device-neutral and owner-clean.** CPU/reference; no Metal, CUDA, device
   handles, or kernel work (GGUF-A7/GGUF-M5 / Radix-Hosts seams). File access
   stays with the application-owned exemplar adapter.
4. **Local corpus boundary.** The real artifact is operator-local evidence,
   never committed; Gradus never receives its path (the exemplar's app-owned
   adapter resolves it). Goldens are derived values committed as fixtures.

## 3. Repo-aware baseline (verified 2026-08-13 on the planner-35 lane)

| Surface | Current state | Micro-unit |
| --- | --- | --- |
| `src/model/moe.fab` / `.proba` | **Do not exist** — the module is entirely new | B1–B4 |
| `src/nn.fab` | Public rows: `linear`/`gelu`/`layernorm` + fixed-shape rows; `_exp` helper at `:251`; **no `silu`** | A1 |
| `src/model/tensor_view.fab` | **Does not exist** — LIB-03 lowered (`a7d7bcd`), not landed; `TensorView`/`materialize_slice`/`ViewError`/`SourceRead` surface arrives with GGUF-A3 | B1–B4 entry gate |
| `src/model/gguf_manifest.fab` | Live `SourceRead`/`inveni_tensorem`/`read_fragmentum` surface (A1b) | read-only (B3 adapter pattern) |
| `src/model/qwen35moe.fab` / `.proba` | **Do not exist yet** (MODEL-01 chain lowered at `df3c016`, not landed); its admitted `ConfiguraMoe`-equivalent facts (256/8/512/512/2048) are the spec | read-only at dispatch |
| `src/sampling.fab` | "first-index ties" convention live | A3/B2 tie-rule precedent |
| `fixtures/gguf/` | `gen_manifest_fixtures.py`, `general-manifest-oracle.md`, `gguf-row-oracle.md`, three manifest fixtures; **no `gen_moe_*` files** | A2, A3 |
| `exempla/gguf-inspect/` | Application adapter pattern: `solum.partem` bounded prefix read + operation-scoped range; never touches tensor payload | B3/C1 (pattern) |
| `exempla/moe-router-probe/` | **Does not exist** — C1 creates it | C1 |
| `scripta/check-compile` | Package-aware `faber check`; exempla blocks per dir (gguf-manifest, gguf-inspect, …); no moe block | C3 (register) |
| `scripta/inventory-public-symbols` | Baseline `model/gguf_manifest expect=42`; tracked total 618; zombie-doc coverage gate | C3 (re-baseline with the new module + silu row) |
| `docs/api-reference.md` | Model sections at :507–692; `gradus:nn` at :330; no moe section | C2 |
| `docs/module-map.md` | 27 modules / 618 functions; no `gradus:model/moe` row | C2 |
| `docs/diagnostics.md` | Error-table rows for model modules; no `MoError` row | C2 |
| `docs/regression-corpus.md` | v1.2.0 (2026-08-12, GGUF-A1b); 26 proba suites | C2 (bump after MODEL-01 chain's v1.5.0) |
| `pml0-support-matrix.md` | Six admitted rows at structural tier; no MoE row | C3 |
| `pml0-symbol-inventory.md` | Re-baselined surface, 618 total | C3 (capture verbatim) |
| `pml5-general-gguf-delivery.md` | §GGUF-M2 section present; no implemented/status line | C3 (status + evidence note) |
| `docs/factory/production-ml-library/CAMPAIGN.md` | Status line "GGUF-A1c is next" (predates the M-chains) | C3 (status only) |
| External consumers (`norma`, `faber`, `radix`, `examples`, `hosts`) | No imports of `gradus:model/moe` | None |
| faber binary | No binary inside this lane; per the A1a/A1C/LIB-02/MODEL-01 precedent the lane-local binary is the closeout authority | G1 only |

## 4. Micro-unit graph (11 units)

Eleven micro-units, each one behavioral outcome, 1–3 primary files for code
units (A2/A3 are the fixture exceptions at 2–3; C2 is the docs exception at
4; C3 is the records exception at 6), one focused red-green proof run once,
3–8k est_work_tokens, no package/check-source/check-compile/stage/e2e/full
child gate. G1 is the only integration-capable unit. All eight campaign
rule-2 fields (outcome, exact write scope, first failing oracle, closeout
command, expected observed result, est_basis justification, stop condition,
depends_on) live **per unit** in the tables below — `red` is the first
failing oracle, `green` carries the closeout command and expected observed
result, the `est_work_tokens` row carries the est_basis justification, and
each unit gained a `stop condition` row (added 2026-08-14, task `f7ae2d38`,
audit `524eb154`). No field lives only at the aggregate, so no aggregate-field
waiver is recorded (M3 follow-up pattern, task `954f8d4a`); G1's lane-owned
closeout stays aggregate-resident as named once in §9.

```text
MODEL-01 (GGUF-M1 aggregate gate lands on factory/merge — after LIB-02 + LIB-03 gates only; REF-01 is a sibling; A1 silu eligible before this gate)
  ├─ A1  silu public primitive (nn.fab)           [∥ A2, B1]
  ├─ A2  probe vectors + synthetic fixtures       [∥ A1, B1]
  │    └─ A3  goldens generator + committed goldens [after A2; ∥ B2]
  └─ B1  moe type surface + fail-closed contract  [∥ A1, A2]
       └─ B2  router eligito (top-k/tie/renorm)   [after B1 + A2]
            └─ B3  expertum (windowed rank-3 dispatch) [after B2 + A1 + A3]
                 └─ B4  ffn_moe (accumulation + gated shared expert) [after B3 + A3]
                      ├─ C1  exemplar adapter + real-file receipt  [∥ C2]
                      └─ C2  API/support docs                      [∥ C1]
                           └─ C3  records + inventory re-baseline  [after C1 + C2]
                                └─ G1  aggregate validation + ATOMIC merge
```

**Split boundary**: nn primitive (A1) vs probe/fixture corpus (A2) vs
independent oracle + goldens (A3) vs module type/error contract (B1) vs
router selection (B2) vs single-expert dispatch (B3) vs complete layer FFN
composition (B4) vs executed exemplar (C1) vs docs (C2) vs records/inventory
(C3) vs integration (G1). B1–B4 serialize on `src/model/moe.fab` (one new
module surface); A1/A2/B1 run parallel on disjoint files; A3 ∥ B2 after A2;
C1/C2 run parallel after B4. Peak live Hands: 3.

### MODEL-02-A1 — Public `silu` primitive (`gradus:nn`)

| Field | Value |
| --- | --- |
| `outcome` | the public `silu` row lands in `gradus:nn` — `silu(tensor.Tensor x) → tensor.Tensor ⇥ NnError` (plus the internal scalar helper over the self-hosted `_exp` precedent), with `nn.proba` value pins; **if REF-01's generic SiLU row is present at the unit boundary, consume it instead and record the consumed revision** (no duplicate row, no dual authority) |
| `primary files` | `src/nn.fab`, `src/nn.proba` (2) |
| `write_scope` | those two only |
| `read_scope` | live `nn.fab` (`_exp` :251, `_scalar_gelu` :284), `docs/api-reference.md` `gradus:nn` section (:330), the frozen `silu` spelling in §2 |
| `forbidden_scope` | any `src/model/moe.*`; `gradus:model/tensor_view`; other modules; main-checkout edits |
| `red` | add proba cases asserting `silu([0, 1, -1, 2])`-style values and a tensor case (fail today — no `silu` exists); record the first failing case; if REF-01's row exists, the red is the absence of the consumed-row recording instead |
| `green` | `faber check src/nn.fab` exit 0 (lane-local `FABER_BIN`, `FABER_LIBRARY_HOME`); proba cases pass (or compile-level pins per the recorded invocation); `grep -n "functio silu" src/nn.fab` present; `git diff --check` silent |
| `done_when` | (a) public `silu` row present (or REF-01's consumed and the consumed revision recorded); (b) scalar + tensor proba pins pass; (c) no duplicate row; (d) narrow module proof green |
| `est_work_tokens` | 3–5k. `est_basis`: pilot — one additive nn activation row |
| `tool_latency` | low — single-file `faber check`/`faber test` |
| `depends_on` | silu consume-or-add resolution against sibling REF-01 (GGUF-A4 nn rows); **independently eligible BEFORE the MODEL-01 aggregate gate** — disjoint `src/nn.fab`/`.proba`, no MODEL-01 admission fact read; may dispatch in parallel with MODEL-01's own first units |
| `parallel_with` | A2, B1 (disjoint files); MODEL-01's own first units (sibling chain) |
| `non_integrable` | **YES — blocked.** Changes the `nn` public-symbol count (inventory + zombie-doc coverage) and the module-map row; landing alone breaks repo gates. Only G1 merges. |
| `risk` | low-medium — the REF-01 hunk-serialization is a recheck, not a block: consume-or-add recorded at the boundary |
| `stop condition` | pause and route when — REF-01's generic SiLU row lands with a spelling/revision the consume-or-add cannot record as consumed against the frozen §2 `silu(tensor.Tensor x) → tensor.Tensor ⇥ NnError` pin (→ delivery-amendment path); the red fails for an unrelated reason (a pre-existing `silu` or conflicting public symbol); proceeding would require touching any file outside `src/nn.fab`/`src/nn.proba` |
| `test_owner` | A1 hand; proof run once |

### MODEL-02-A2 — Probe vectors + synthetic fixtures (MoE oracle corpus)

| Field | Value |
| --- | --- |
| `outcome` | committed deterministic probe vectors and synthetic fixtures: `gguf-moe-probes.json` (deterministic pinned `[2048]` f32 hidden-state probes at realistic post-norm magnitudes — two probes per selected layer 0/3/39/40, magnitudes documented against the RMSNorm unit-scale property; plus one in-repo synthetic exact-tie probe in a small hand-built config, not from the artifact) and the generator `gen_moe_probes.py` (seeded, reproducible); schema `gguf-moe-probes-v1` |
| `primary files` | `fixtures/gguf/gen_moe_probes.py`, `fixtures/gguf/gguf-moe-probes.json` (2) |
| `write_scope` | those two only |
| `read_scope` | §2 artifact/layer facts, §4 B2's tie-probe contract (`ConfiguraMoe{n_expert=8, n_used=2} → [2, 5]`), the RMSNorm unit-scale property (REF-01/MODEL-03 semantics), `fixtures/gguf/gen_manifest_fixtures.py` (fixture-generator precedent) |
| `forbidden_scope` | any goldens derivation (A3); any module code; real-artifact reads beyond the pinned identity; committed model bytes |
| `red` | `python3 fixtures/gguf/gen_moe_probes.py` has no deterministic output contract (fail — no generator exists); record the first failing generation |
| `green` | running the generator twice produces byte-identical JSON; probe count/shapes/magnitudes match the documented contract; the tie probe config is present; `git diff --check` silent |
| `done_when` | (a) 2 probes × 4 selected layers committed; (b) synthetic exact-tie probe committed; (c) deterministic regeneration proven; (d) magnitudes documented |
| `est_work_tokens` | 4–6k. `est_basis`: pilot — deterministic fixture corpus |
| `tool_latency` | low — one python generation run |
| `depends_on` | MODEL-01 aggregate gate landed (base) |
| `parallel_with` | A1, B1 (disjoint files) |
| `non_integrable` | **YES — blocked.** Fixture ahead of the surface it feeds (B2/B3/B4 consume it); landing alone has no consumer. Only G1 merges. |
| `risk` | low-medium — probe magnitudes must stay in the documented realistic band (RMSNorm unit-scale), never hand-tuned to a golden |
| `stop condition` | pause and route when — probe magnitudes cannot sit in the documented RMSNorm unit-scale band without hand-tuning toward a golden (→ the band or probe contract needs amendment); the generator's output is not byte-identical across runs (determinism contract broken); the exact-tie config cannot be expressed in the `gguf-moe-probes-v1` schema |
| `test_owner` | A2 hand; proof run once |

### MODEL-02-A3 — Goldens generator + committed goldens (independent oracle)

| Field | Value |
| --- | --- |
| `outcome` | the independent Python oracle `gen_moe_goldens.py` (the gi2-dequant-reference precedent) that (a) reads the real artifact read-only and verifies the pinned identity (22,663,387,424 bytes, SHA-256 `0b21525e…`), (b) dequantizes the router/expert/shared-expert tensors with the GGUF-A3 codec semantics (llama.cpp `ggml-quants.c` @ `a957b7747`, bit-exact), and (c) computes the exact §2 MoE semantics in numpy f32 for the A2 probe vectors — emitting committed goldens `gguf-moe-goldens.json` (schema `gguf-moe-goldens-v1`): per (layer, probe) the full router logits `[256]`, top-8 indices, 8 normalized weights, full `ffn_moe` output `[2048]`, and full shared-expert and per-expert outputs as f32 arrays; plus the oracle doc `gguf-moe-goldens-oracle.md` (derivation, comparison band, first-divergence rule) |
| `primary files` | `fixtures/gguf/gen_moe_goldens.py`, `fixtures/gguf/gguf-moe-goldens.json`, `fixtures/gguf/gguf-moe-goldens-oracle.md` (3) |
| `write_scope` | those three only |
| `read_scope` | A2 probes, §2 exact MoE semantics + tie rule, the LIB-03 codec semantics (llama.cpp `ggml-quants.c` @ `a957b7747`), the gi2-dequant-reference precedent (`radix/docs/factory/gpu-inference-gguf/evidence/gi2-dequant-reference.py` + `gi2-dequant-goldens.json`), gi0-6 band derivation method |
| `forbidden_scope` | any gradus module code; any real-artifact write; committed model bytes; selecting layers outside {0, 3, 39, 40} |
| `red` | no goldens exist; the generator against the artifact has no output contract (record the first failing derivation) |
| `green` | generator verifies identity, dequantizes bit-exact per the codec semantics, and emits the schema-complete goldens; oracle doc records the derived band `Δ = 10·R` capped at `5e-4` for normalized values in `[0,1]` and at the `numeric-policy v1.0.0` matmul row (`1e-5` atol/`1e-5` rtol) for pure matmul, plus the first-divergence rule; `git diff --check` silent |
| `done_when` | (a) goldens cover layers 0/3/39/40 × 2 probes + the tie case; (b) identity verified in-generator; (c) band + first-divergence rule documented; (d) deterministic regeneration proven |
| `est_work_tokens` | 5–8k. `est_basis`: pilot — the largest oracle derivation of the chain |
| `tool_latency` | medium — one python derivation run on the real artifact + f64 reference evaluation |
| `depends_on` | A2 (probe vectors) |
| `parallel_with` | B2 (disjoint files) |
| `non_integrable` | **YES — blocked.** Goldens ahead of the surface they validate; only G1 merges. |
| `risk` | medium — the oracle must be independent (never read gradus code) and bit-exact per the pinned codec semantics |
| `stop condition` | pause and route when — the artifact identity check fails (byte length/SHA-256 ≠ pinned; the artifact changed — route to Mind, never proceed on a different artifact); a dequantization diverges from bit-exact `ggml-quants.c` @ `a957b7747` semantics; the band/first-divergence rule cannot be derived per the gi0-6 method |
| `test_owner` | A3 hand; proof run once |

### MODEL-02-B1 — MoE module type surface + fail-closed error contract

| Field | Value |
| --- | --- |
| `outcome` | `src/model/moe.fab` opens with the frozen type surface: `importa ex "gradus:model/tensor_view" visum`, genus `ConfiguraMoe` (256/8/512/512/2048 — from MODEL-01 admission, never re-derived), discretio `MoError` with all seven variants + `message`, and genus `SelectioExpertarum`; `moe.proba` pins the ConfiguraMoe values and the fail-closed error rows (`NonFinita` on NaN/±Inf probe, `TypoIgnotum` un-admitted-type, `NomineIgnota` unknown-tensor-name, shape/dimension/order rows) — typed `MoError`, never a silent default |
| `primary files` | `src/model/moe.fab`, `src/model/moe.proba` (2) |
| `write_scope` | those two only |
| `read_scope` | MODEL-01 admission facts (§2 + the landed `src/model/qwen35moe.fab` at dispatch), the LIB-03 `gradus:model/tensor_view` surface, §2 frozen public surface |
| `forbidden_scope` | any function body (router/dispatch/composition); `silu`; `src/model/qwen35moe.*` edits; other modules |
| `red` | proba asserting the ConfiguraMoe field values + error rows (fail — no module exists); record the first failing case |
| `green` | `faber check src/model/moe.fab` exit 0; type + error probas pass; `grep -nE "genus ConfiguraMoe|discretio MoError|genus SelectioExpertarum" src/model/moe.fab` present; `git diff --check` silent |
| `done_when` | (a) frozen type surface lands with the exact spellings; (b) ConfiguraMoe matches MODEL-01 admission; (c) all seven MoError rows fail closed in proba; (d) narrow module proof green |
| `est_work_tokens` | 3–5k. `est_basis`: pilot — first module type/error contract |
| `tool_latency` | low — single-file proof |
| `depends_on` | MODEL-01 aggregate gate landed (base); LIB-03 `tensor_view` surface landed (recheck handle) |
| `parallel_with` | A1, A2 (disjoint files) |
| `non_integrable` | **YES — blocked.** Partial module; only G1 merges. |
| `risk` | low — spellings frozen in §2; any amendment routes through the delivery-amendment path |
| `stop condition` | pause and route when — the MODEL-01 admission facts (256/8/512/512/2048) or the landed LIB-03 `tensor_view` surface differ from the frozen §2 spellings (→ route to the MODEL-01/LIB-03 owner, never re-derive); a `MoError` variant cannot fail closed in proba for its named reason |
| `test_owner` | B1 hand; proof run once |

### MODEL-02-B2 — Router `eligito` (logits, softmax, deterministic top-k, renormalization)

| Field | Value |
| --- | --- |
| `outcome` | `eligito(lista<f32> x, visum.TensorView ffn_gate_inp, ConfiguraMoe cfg) → SelectioExpertarum ⇥ MoError` computes the full `[n_expert]` router logits (`x @ ffn_gate_inp`, no bias), softmax over all `n_expert` (max-subtracted f32), the top-`n_usae` by probability in descending order with the **deterministic tie rule (lowest index first)**, and weight renormalization `weights /= max(sum(weights), 6.103515625e-5)` (`norm_w=true`; no `expert_weights_scale` step) |
| `primary files` | `src/model/moe.fab`, `src/model/moe.proba` (2) |
| `write_scope` | those two only |
| `read_scope` | B1 branch head, A2 tie-probe fixture, §2 exact MoE semantics steps 1–4 + tie rule, `src/sampling.fab` first-index-ties convention |
| `forbidden_scope` | expert dispatch (B3); composition (B4); any SSM/attention (MODEL-03); `src/model/qwen35moe.*` edits |
| `red` | the first failing oracle (before any MoE code): `eligito(probe_vector, ffn_gate_inp, ConfiguraMoe{n_expert=8, n_used=2}) → must return [2, 5]` (exact-tie selection, lowest-index-first) — the call does not compile (RED) |
| `green` | `faber check src/model/moe.fab` exit 0; tie-probe `[2, 5]` passes; top-k ordering + renormalized-weights probas pass against the A2 fixtures; non-finite input → `MoError.NonFinita`; `git diff --check` silent |
| `done_when` | (a) full logit row per probe; (b) deterministic tie rule proven by the crafted tie probe; (c) renormalization matches `norm_w=true` semantics with the `6.103515625e-5` guard; (d) no scale step; (e) narrow module proof green |
| `est_work_tokens` | 5–7k. `est_basis`: pilot — router selection math in Fab |
| `tool_latency` | low-medium — single-file proof + fixture cross-check greps |
| `depends_on` | B1 (branch head) + A2 (tie fixture) |
| `parallel_with` | A3 (disjoint files) |
| `non_integrable` | **YES — blocked.** Partial module; only G1 merges. |
| `risk` | medium — tie rule and renormalization are the frozen facts; index mismatches are hard fails (indices exact), never tolerance-widened |
| `stop condition` | pause and route when — the crafted tie probe does not return `[2, 5]` (the lowest-index-first rule cannot be represented in Fab — route, never silently adopt llama.cpp's implementation-defined argsort order); the `6.103515625e-5` renorm guard cannot be reproduced exactly |
| `test_owner` | B2 hand; proof run once |

### MODEL-02-B3 — Expert dispatch `expertum` (windowed rank-3 SwiGLU)

| Field | Value |
| --- | --- |
| `outcome` | `expertum(lista<f32> x, numerus index_expertae, visum.TensorView ffn_gate_exps, visum.TensorView ffn_up_exps, visum.TensorView ffn_down_exps, ConfiguraMoe cfg, (numerus, numerus) → visum.SourceRead fons) → lista<f32> ⇥ MoError` reads only the expert-`e` window of the three rank-3 tensors through the operation-scoped range source (never a whole rank-3 tensor), computes `h = silu(x @ gate_e) * (x @ up_e)` and `out = h @ down_e`, and returns the expert's `[512]` output; the synthetic multi-expert fixture exercises a Q4_K/Q5_K expert window through the real codecs; the per-expert window materializes to the pinned f32 golden values |
| `primary files` | `src/model/moe.fab`, `src/model/moe.proba` (2) |
| `write_scope` | those two only |
| `read_scope` | B2 branch head, A1 silu (branch head), A3 goldens (window values), `exempla/gguf-inspect` operation-scoped range pattern, §2 rank-3 mapping/storage union |
| `forbidden_scope` | router (B2); composition/accumulation (B4); whole-rank-3 materialization; `src/model/qwen35moe.*` edits |
| `red` | the rank-3 expert-slice case: a per-expert window of `ffn_gate_exps.weight` materializes to the pinned f32 golden values (fail — no `expertum`); record the first divergent element index |
| `green` | `faber check src/model/moe.fab` exit 0; windowed-read + SwiGLU probas pass vs the A3 goldens (first-divergence rule); Q4_K/Q5_K window cases pass; `IndexMala`/`FormaMismatch`/`TypoIgnotum` rows fail typed; `git diff --check` silent |
| `done_when` | (a) per-expert window materializes to the goldens; (b) SwiGLU dispatch exact; (c) reads stay window-scoped (never the whole rank-3 tensor); (d) negative rows typed; (e) narrow module proof green |
| `est_work_tokens` | 5–8k. `est_basis`: pilot — windowed rank-3 dispatch in Fab |
| `tool_latency` | low-medium — single-file proof + codec-window cases |
| `depends_on` | B2 (branch head) + A1 (silu) + A3 (goldens) |
| `parallel_with` | none (module seam) |
| `non_integrable` | **YES — blocked.** Partial module; only G1 merges. |
| `risk` | medium — the exact rank-3 mapping and storage union are frozen; a live layout outside {F32, BF16, Q4_K, Q5_K, Q6_K, Q8_0} is a stop-condition record, never a silent widening |
| `stop condition` | pause and route when — a live layout outside the frozen {F32, BF16, Q4_K, Q5_K, Q6_K, Q8_0} appears (stop-condition record, never a silent widening — per the risk row); a rank-3 window diverges from the A3 goldens with no attributable first-divergent element |
| `test_owner` | B3 hand; proof run once |

### MODEL-02-B4 — Complete layer FFN `ffn_moe` (accumulation + gated shared expert)

| Field | Value |
| --- | --- |
| `outcome` | `ffn_moe(lista<f32> x, …all nine tensors…, ConfiguraMoe cfg, (numerus, numerus) → visum.SourceRead fons) → lista<f32> ⇥ MoError` composes the routed weighted sum `moe_out = Σ_e weights[e]·expertum(x,e)`, the sigmoid gate `g = sigmoid(x · ffn_gate_inp_shexp)`, the shared-expert FFN `shexp = (silu(x @ ffn_gate_shexp) * (x @ ffn_up_shexp)) @ ffn_down_shexp`, and returns `ffn_out = moe_out + g·shexp`; full-probe goldens match (per (layer, probe)) |
| `primary files` | `src/model/moe.fab`, `src/model/moe.proba` (2) |
| `write_scope` | those two only |
| `read_scope` | B3 branch head, A1 silu, A3 goldens (full-probe rows), §2 exact MoE semantics steps 5–8 |
| `forbidden_scope` | router/dispatch internals (B2/B3); any SSM/attention; MTP execution claims; `src/model/qwen35moe.*` edits |
| `red` | the full `ffn_moe` probe case against the committed goldens (fail — no composition); record the first divergent element index, never a tolerance-widened pass |
| `green` | `faber check src/model/moe.fab` exit 0; routed-sum + gated-shared-expert + complete-output probas match the goldens under the declared band; the negative matrix (unknown tensor, shape mismatch, un-admitted type, non-finite) fails typed; `git diff --check` silent |
| `done_when` | (a) accumulation exact per goldens; (b) shared-expert gating exact; (c) `ffn_out = moe_out + g·shexp` matches full-probe goldens; (d) block-40 MTP exclusion recorded (layer-40 probe = BF16 codec exercise only, no MTP execution claim); (e) narrow module proof green |
| `est_work_tokens` | 5–8k. `est_basis`: pilot — composition of the two expert families |
| `tool_latency` | low-medium — single-file proof + full-probe cases |
| `depends_on` | B3 (branch head) + A3 (goldens) |
| `parallel_with` | none (module seam) |
| `non_integrable` | **YES — blocked.** The surface is complete, but the executed exemplar (C1), docs (C2), records (C3), and gate (G1) must land with it. Only G1 merges. |
| `risk` | medium — the complete layer FFN semantics are the unit's done oracle; shared-expert gating and block-40 exclusion are frozen |
| `stop condition` | pause and route when — full-probe goldens diverge beyond the declared band with no attributable first-divergent element (never tolerance-widened); recording the block-40 MTP exclusion would require an MTP execution claim (layer-40 probe is a BF16-codec exercise only) |
| `test_owner` | B4 hand; proof run once |

### MODEL-02-C1 — Exemplar adapter + executed MoE probe receipt

| Field | Value |
| --- | --- |
| `outcome` | `exempla/moe-router-probe/` (new) — application-owned adapter (the `exempla/gguf-inspect`/`gguf-materialize` pattern): reads the bounded manifest prefix + windowed range source over the real artifact (never tensor bytes outside the operation-scoped ranges), calls the public `gradus:model/moe` surface, and prints PASS lines — one per (layer, probe) golden: `PASS layer=0 probe=p1 logits=<hash> indices=[...] weights=<...>`, `PASS layer=3 …`, `PASS layer=39 …`, `PASS layer=40 …` (exact index equality, first-divergence `none`, max abs deviation `≤ Δ`), plus the synthetic tie-case line `indices=[2,5]` and the negative-matrix lines; zero FAIL lines; exit 0; the README records the exact command, revisions, model identity, probe hashes, observed rows, the derived `Δ`, and the first-divergence record (none expected) |
| `primary files` | `exempla/moe-router-probe/faber.toml`, `exempla/moe-router-probe/src/main.fab`, `exempla/moe-router-probe/README.md` (3) |
| `write_scope` | `exempla/moe-router-probe/` only (this delivery's receipt section lands in the same commit) |
| `read_scope` | B4 public entry, the application-adapter pattern from `exempla/gguf-inspect/` (+ `gguf-materialize` if landed), A3 goldens |
| `forbidden_scope` | any `src/` edit; logits/generation/device work; committed GGUF bytes; main-checkout edits |
| `red` | `faber check exempla/moe-router-probe` fails (no package); record the first failure |
| `green` | `faber check exempla/moe-router-probe` exit 0; one `faber run --target fmir exempla/moe-router-probe -- /Users/ianzepp/ai/models/Qwen3.6-35B-A3B-UD-Q4_K_M.gguf 10991392 0b21525e972670ed59e1812e170b27c26355381f0656ecc4e25617ece7dac58b` (lane-local `FABER_BIN`) prints all PASS lines (layers 0/3/39/40 + tie + negative matrix), zero FAIL, exit 0; `git diff --check` silent |
| `done_when` | (a) one Faber package command proves the component-level oracle on the real artifact; (b) the receipt names revisions, model identity, command, expected vs observed rows; (c) no read enters un-admitted regions |
| `est_work_tokens` | 4–6k. `est_basis`: pilot — exemplar phase |
| `tool_latency` | medium — `faber check` + one fmir run |
| `depends_on` | B4 (branch head) + A3 (goldens) |
| `parallel_with` | C2 (disjoint files) |
| `non_integrable` | **YES — blocked.** The executed proof lands with the surface it proves; records (C3) and gate (G1) must accompany. Only G1 merges. |
| `risk` | low-medium — the bounded range reads must never touch bytes outside the operation-scoped windows |
| `stop condition` | pause and route when — any real-artifact read touches bytes outside the operation-scoped ranges (bounded-range violation — stop); completing the receipt would require editing `src/` or `scripta/` (scope breach) |
| `test_owner` | C1 hand; proof run once |

### MODEL-02-C2 — API/support docs

| Field | Value |
| --- | --- |
| `outcome` | `docs/api-reference.md` (new `## gradus:model/moe` section documenting every public symbol from the B1–B4 reports + the `nn.silu` row), `docs/module-map.md` (new `gradus:model/moe` row + module count), `docs/diagnostics.md` (new `MoError` table row matching the frozen variants), and `docs/regression-corpus.md` (bump to the next version after the MODEL-01 chain's v1.5.0 — currently live v1.2.0; add the moe proba suite, the goldens fixtures, and the exempla consumer; update suite totals) describe the actual frozen surface |
| `primary files` | `docs/api-reference.md`, `docs/module-map.md`, `docs/diagnostics.md`, `docs/regression-corpus.md` (4) |
| `write_scope` | those four only |
| `read_scope` | B1–B4 branch heads (actual surface), A2/A3 fixtures, §2 frozen contracts |
| `forbidden_scope` | edits to `src/` or `scripta/`; describing surfaces that do not exist; changing API-shape policy; absorbing other chains' docs work |
| `red` | the new public symbols (from the B1–B4 reports) are absent from the api-reference moe section (coverage snippet mirroring `scripta/inventory-public-symbols`); `git diff --check` must be silent |
| `green` | every new public `functio` name appears in the api-reference moe section (coverage snippet); docs agree with the frozen contracts; regression-corpus bumped with the new suite/fixtures/exemplar; `git diff --check` silent |
| `done_when` | (a) moe API section matches the merged surface; (b) module-map row added; (c) diagnostics table lists `MoError`; (d) regression-corpus bumped |
| `est_work_tokens` | 4–6k. `est_basis`: pilot — 4 docs, selectively touched |
| `tool_latency` | low — grep/awk checks only, no compile |
| `depends_on` | B4 (branch head; surface frozen there) |
| `parallel_with` | C1 (disjoint files) |
| `non_integrable` | **YES — blocked.** Docs ahead of the verified surface; zombie-doc coverage breaks if merged alone. Only G1 merges. |
| `risk` | low-medium — api-reference must document the actual merged surface (report-driven), not provisional names |
| `stop condition` | pause and route when — the merged B1–B4 surface differs from the frozen §2 contracts (docs document the actual surface; a conflict routes, never a provisional name); a public symbol from the B1–B4 reports cannot be documented in the four doc files |
| `test_owner` | C2 hand; proof run once |

### MODEL-02-C3 — Records + inventory re-baseline + registration

| Field | Value |
| --- | --- |
| `outcome` | `scripta/inventory-public-symbols` re-baselined to the merged surface (new `model/moe` row + `nn` count change from A1 + tracked total), `pml0-symbol-inventory.md` captured verbatim from a fresh run, `pml0-support-matrix.md` records the MoE router/expert row at the **output-checked component tier** (never executed-token/model identity — CTO8-1 stays the named gate), `pml5-general-gguf-delivery.md` + gradus `CAMPAIGN.md` status lines flip to GGUF-M2 implemented, and `scripta/check-compile` registers `exempla/moe-router-probe` |
| `primary files` | `scripta/inventory-public-symbols`, `docs/factory/production-ml-library/pml0-symbol-inventory.md`, `docs/factory/production-ml-library/pml0-support-matrix.md`, `docs/factory/production-ml-library/pml5-general-gguf-delivery.md`, `docs/factory/production-ml-library/CAMPAIGN.md`, `scripta/check-compile` (6) |
| `write_scope` | those six only |
| `read_scope` | merged A1–C2 source (count source of truth), A2/A3 fixtures, C2 docs, C1 receipt |
| `forbidden_scope` | edits to `src/`; changing the coverage-gate semantics; overclaiming (the note must say "implemented in the MODEL-02 micro-unit chain", not "audited"); main-checkout edits |
| `red` | `./scripta/inventory-public-symbols` exits non-zero (baseline stale — `model/moe` unknown module, total ≠ tracked); GGUF-M2 status still says unimplemented; `grep -c "moe-router-probe" scripta/check-compile` = 0 |
| `green` | inventory script exit 0 on the merged tree (needs C2's coverage); symbol-inventory doc verbatim; support-matrix row present at output-checked tier with no execution claim; check-compile block for the new exemplum present; CAMPAIGN/delivery status lines flipped honestly; `git diff --check` silent |
| `done_when` | (a) inventory re-baselined and asserted; (b) symbol-inventory verbatim; (c) support-matrix MoE row at the output-checked component tier; (d) status lines flipped; (e) check-compile registers the exemplum |
| `est_work_tokens` | 3–5k. `est_basis`: pilot — mechanical re-baseline + status/registration edits |
| `tool_latency` | low — grep-based script + doc edits |
| `depends_on` | C1 + C2 (branch heads; records describe the verified surface) |
| `parallel_with` | none |
| `non_integrable` | **YES — blocked.** Records claim completion; only G1's validated merge makes that true. Only G1 merges. |
| `risk` | low — must not overclaim or mask a symbol that should be private |
| `stop condition` | pause and route when — `scripta/inventory-public-symbols` cannot be re-baselined to the merged surface on the expected delta (baseline drift beyond the `model/moe` row + nn count change); the support-matrix tier is disputed (output-checked component tier is frozen — no execution claim); a status line would overclaim (never write a claim the records cannot support) |
| `test_owner` | C3 hand; proof run once |

### MODEL-02-G1 — Aggregate package validation and atomic integration

| Field | Value |
| --- | --- |
| `outcome` | merge the A1–C3 branch heads onto the MODEL-02 integration branch, run the full closeout validation once, and merge the integration branch into `factory/merge` as a single unit — `factory/merge` never observes a partial MoE surface (no type without router, no router without dispatch, no dispatch without composition, no module without its executed exemplar/docs/records) |
| `primary files` | none (validation + merge only; no product/doc edits) |
| `write_scope` | the merge itself; a commit message naming the A1–C3 heads |
| `read_scope` | the merged MODEL-02 integration branch |
| `forbidden_scope` | new product code; re-running any unit's work; editing source files to "fix" the check; main-checkout edits |
| `red` | any closeout command fails, any closeout grep is non-empty, or the exemplar run diverges → **do not merge**; record the exact failure and stop |
| `green` (closeout, run once) | lane-relative, `FABER_BIN` = lane-local faber binary per the A1a/A1C/LIB-02/MODEL-01 precedent: `./scripta/check-source`; `./scripta/check-compile` (package + exempla incl. the new moe-router-probe exemplum); `faber check --diagnostics .` ends `ok: .`; `faber run --target fmir exempla/moe-router-probe -- /Users/ianzepp/ai/models/Qwen3.6-35B-A3B-UD-Q4_K_M.gguf 10991392 0b21525e972670ed59e1812e170b27c26355381f0656ecc4e25617ece7dac58b` prints the PASS lines (layers 0/3/39/40 + tie + negative matrix), zero FAIL, exit 0; `./scripta/inventory-public-symbols` exit 0 (docs coverage + baselines hold); `git diff --check` silent. Then merge the integration branch to `factory/merge` |
| `done_when` | all closeout commands pass on the merged tree and the integration branch lands on `factory/merge` as one atomic merge; the receipt records revisions, model identity, command, expected vs observed rows |
| `est_work_tokens` | 3–5k. `est_basis`: pilot — one aggregate validation pass + merge |
| `tool_latency` | medium — the only package-level compile + fmir run in the whole chain |
| `depends_on` | A1–C3 merged on the MODEL-02 integration branch |
| `parallel_with` | none — last |
| `non_integrable` | **The only integrable unit** — sole holder of the aggregate merge gate. |
| `risk` | low — the merged surface is fully specified by A1–C3; G1 verifies, it does not design |
| `stop condition` | any closeout command fails, any closeout grep is non-empty, or the exemplar run diverges → **do not merge**; record the exact failure and stop (per the red row). A divergence not attributable under the first-divergence rule routes to the owning surface, never a silent aggregate match |
| `test_owner` | G1 hand (or Mind-assigned integration owner); every child's proof ran once in its own unit, nothing is re-run here except the aggregate closeout |

## 5. Dependency and parallelism map

```text
factory/merge (post MODEL-01 aggregate gate — after LIB-02 + LIB-03 gates only; REF-01 is a sibling; A1 eligible before this gate)
  ├─ A1  silu public primitive (nn.fab)           [∥ A2, B1]
  ├─ A2  probe vectors + synthetic fixtures       [∥ A1, B1]
  │    └─ A3  goldens generator + committed goldens [after A2; ∥ B2]
  └─ B1  moe type surface + fail-closed contract  [∥ A1, A2]
       └─ B2  router eligito                      [after B1 + A2]
            └─ B3  expertum (windowed dispatch)   [after B2 + A1 + A3]
                 └─ B4  ffn_moe (composition)     [after B3 + A3]
                      ├─ C1  exemplar adapter     [∥ C2]
                      └─ C2  API/support docs     [∥ C1]
                           └─ C3  records + inventory + registration [after C1 + C2]
                                └─ G1  aggregate gate → factory/merge
```

- **Maximum safe parallelism**: A1 is eligible **before** the MODEL-01 gate
  (disjoint `src/nn.fab`, silu consume-or-add vs sibling REF-01 only) and may
  run in parallel with MODEL-01's own first units. Once the MODEL-01 gate
  lands, A2 and B1 run in parallel (disjoint files: `fixtures/gguf/`,
  `src/model/moe.fab`). Then A3 and B2 run in parallel (disjoint files) after
  A2. Then the B3 → B4 module leg serializes on `src/model/moe.fab` (one new
  surface — no safe parallelism on the same file). After B4, C1 and C2 run in
  parallel (disjoint files). Peak live Hands: 3.
- **Branch protocol**: every A1–C3 unit commits on its own `factory/<lane>`
  branch, based on the branch indicated in `depends_on`. Each commit message
  is marked **`non-integrable (MODEL-02 chain)`**. B4's base is B3's branch;
  C1's base is B4's branch; C2's base is B4's branch too (docs can run
  parallel with the exemplar). C3 bases on C1+C2 branch heads. G1 merges the
  complete integration branch to `factory/merge`.
- **Shared-file discipline** (strictly hunk-serialized; each handoff a landed
  commit boundary): `src/model/moe.fab`/`.proba` (B1–B4 serial — never two
  Hands simultaneously); `src/nn.fab`/`.proba` (A1 vs REF-01's nn rows —
  consume-or-add with the recorded revision); `src/model/qwen35moe.fab`
  (MODEL-01-owned, read-only here).

## 6. One atomic integration boundary

The delivery authority freezes "selected layers match independent router
choices, expert weights, intermediate values, and outputs for pinned
hidden-state probes". The micro-unit split preserves that as **merge
atomicity**, not a single-task shape:

- `factory/merge` is the only integration stop.
- A1–C3 never merge to `factory/merge`. Their branches are transitional and
  marked non-integrable (reasons per unit: repo-gate breakage, records-ahead-
  of-surface, partial module surface, zombie-doc coverage).
- G1 is the **sole aggregate merge gate**: it merges the full A1–C3 set as one
  unit only after the closeout passes. `factory/merge` therefore never
  contains an intermediate state where the MoE surface exists but cannot
  satisfy its own component-level oracle, and never contains a module whose
  docs/inventory/records disagree with its source.

## 7. Dispatch serialization (first eligible frontier after MODEL-01)

Per the assignment's authority — "report first eligible frontier after
MODEL-01" — and the corrected admitted MODEL-01 (c69d6a7) plus the campaign
dependency table (MODEL-02 depends on MODEL-01; MODEL-01 depends on LIB-02 +
LIB-03; REF-01 is a sibling of MODEL-01):

1. **MODEL-01 (GGUF-M1) chain** lands its aggregate gate on `factory/merge`
   **after the LIB-02 + LIB-03 aggregate gates only** (campaign dependency
   authority; REF-01 is a sibling, not a MODEL-01 predecessor, and never
   gates its dispatch).
2. **A1 is independently eligible BEFORE the MODEL-01 gate** — `silu` in
   `src/nn.fab`/`.proba` reads no MODEL-01 admission fact; the only coupling
   is the silu consume-or-add resolution against the **sibling REF-01** (nn
   rows). A1 may dispatch in parallel with MODEL-01's own first units, not
   behind its gate.
3. **First eligible frontier after MODEL-01** = **A2 ∥ B1** (two parallel
   units on disjoint files). A2 commits the probe corpus; B1 freezes the
   module type/error contract against the landed admission + tensor_view
   surfaces.
4. Then **A3 ∥ B2** (after A2); then **B3** (after B2 + A1 + A3); then **B4**
   (after B3 + A3); then **C1 ∥ C2** (after B4); then **C3** (after C1 + C2);
   then **G1** (last).
5. MODEL-02 units touch **no** MODEL-01/LIB-03/REF-01 surface beyond
   preservation: `qwen35moe.fab` is read-only; `tensor_view` is consumed
   through its landed surface; `silu` is consumed-or-added with a recorded
   revision against the sibling REF-01.

## 8. Red oracle (review fail conditions)

The task graph **must fail review** if any of the following is true of any
child:

| Unit | est_work_tokens | behavior families | primary files | integrable alone? | explicit block |
| --- | --- | --- | --- | --- | --- |
| A1 | 3–5k | 1 (silu primitive) | 2 | no — inventory/zombie gates | §4 A1 `non_integrable` |
| A2 | 4–6k | 1 (probe/fixture corpus) | 2 | no — fixture ahead of consumers | §4 A2 `non_integrable` |
| A3 | 5–8k | 1 (oracle + goldens) | 3 | no — goldens ahead of surface | §4 A3 `non_integrable` |
| B1 | 3–5k | 1 (type/error contract) | 2 | no — partial module | §4 B1 `non_integrable` |
| B2 | 5–7k | 1 (router selection) | 2 | no — partial module | §4 B2 `non_integrable` |
| B3 | 5–8k | 1 (expert dispatch) | 2 | no — partial module | §4 B3 `non_integrable` |
| B4 | 5–8k | 1 (layer FFN composition) | 2 | no — needs C1/C2/C3/G1 | §4 B4 `non_integrable` |
| C1 | 4–6k | 1 (exemplar) | 3 | no — executed proof lands with surface | §4 C1 `non_integrable` |
| C2 | 4–6k | 1 (docs) | 4 | no — docs ahead of source | §4 C2 `non_integrable` |
| C3 | 3–5k | 1 (records/inventory) | 6 | no — records claim completion | §4 C3 `non_integrable` |
| G1 | 3–5k | 1 (integration) | 0 | **yes — the single aggregate gate** | §4 G1 |

Review additionally fails if any child: exceeds 8k est_work_tokens; owns
product code **plus** all docs **plus** full validation; or can run a broad
package check (only G1 may). No child repeats the cited plan's single-unit
shape (20k–36k); the largest child (B3/B4, 5–8k) is under half that and owns
one module behavior.

## 9. Proof economy

- Each child runs its narrow focused proof **once**: single-file
  `faber check <file>` / `faber test <proba>` (lane-local `FABER_BIN` and
  `FABER_LIBRARY_HOME`, per the A1a Hand-packet precedent) plus the unit's
  greps. No package-level compile in A1–C3.
- A2/A3 use python generation runs (deterministic, twice-identical); A3's
  derivation is the chain's single oracle evaluation.
- C1's `faber run --target fmir exempla/moe-router-probe` is its own narrow
  executed proof (the package it creates is its write surface).
- G1 is the **only** unit that runs `check-source` / `check-compile` /
  `faber check --diagnostics .` / the exemplar fmir run / the
  `inventory-public-symbols` gate / `git diff --check`.
- A lane-local faber binary matching the lane's radix stdlib is required for
  the G1 closeout (per the A1a/A1C/LIB-02/MODEL-01 precedent); the main-repo
  binary is not the closeout authority.

## 10. Mandatory successors preserved through CLOSE-01

Nothing below is narrowed, deferred, made optional, or moved outside the
campaign by this re-split:

```text
LIB-01 (A1C chain) → LIB-02 + LIB-03 → REF-01 (dense reference rungs)
                                 → MODEL-01 → MODEL-02 (this chain) + MODEL-03 (SSM/attention)
                                      → MODEL-04 (full-model reference inference)
                                      → EXEC-01 (Faber package plan) + EXEC-02 (packed native kernels)
                                      → EXEC-03 (persistent resident sessions)
                                      → CAP-01 (Metal) + CAP-02 (CUDA)
                                      → CLOSE-01 (reconcile + independent audit)
```

- GGUF graph: `M1 → M2 ‖ M3`; `M2 + M3 → M4` (full-model reference inference
  consumes the `ffn_moe` surface per layer), `M4 → M5` (native Metal/CUDA),
  `M5 → M6` (Faber capstone + closeout). The unit's
  `ffn_moe`/`eligito`/`expertum` surface is the MoE execution authority
  GGUF-M4/M5 consume; GGUF-M3 reads the same admission facts but owns the
  disjoint SSM/attention state.
- Umbrella rows: MODEL-02 → MODEL-04 → EXEC-01/02 → EXEC-03 → CAP-01/02 →
  CLOSE-01. The full-model router choices validated here as component goldens
  are re-validated end-to-end at MODEL-04's first-divergence boundary against
  the pinned llama.cpp comparator; a divergence found there routes back to
  this surface with the first-divergence record, never a silent match.
- The exact-artifact completion contract (Qwen3.6-35B-A3B-UD-Q4_K_M.gguf,
  22,663,387,424 bytes, SHA-256
  `0b21525e972670ed59e1812e170b27c26355381f0656ecc4e25617ece7dac58b`,
  complete `qwen35moe` graph, 256+ tokens × 2 prompts in one resident
  session, Metal and CUDA, every receipt clause) is unchanged.
- MODEL-02 advances milestone **Q2 — complete model semantics** (gates A4–A6
  and M1–M4), parallel to MODEL-03's SSM/attention half. A completed MODEL-02
  with no successor receipts leaves the campaign incomplete by design; the
  campaign closes only when CLOSE-01 is accepted with both capstone receipts
  and every invariant clause.

## 11. Validation summary (planning artifact)

- Live surfaces re-verified on the planner-35 lane: `src/model/moe.*` absent;
  `src/nn.fab` has no `silu`; `gradus:model/tensor_view` absent (LIB-03 not
  landed); `qwen35moe.*` absent (MODEL-01 not landed); inventory baseline 618
  with `model/gguf_manifest expect=42`; regression corpus v1.2.0 with 26 proba
  suites; api-reference model sections :507–692 with no moe section; module-map
  27 modules; gguf-inspect adapter pattern live; no lane-local faber binary.
  Every fact in §2 matches the cited delivery at `74c7af2` (verified against
  the commit blob and the live artifact identity).
- Required fields present for every child: outcome, primary files,
  write/read/forbidden scope, red proof, green proof, done_when, narrow
  validation, 3–8k estimate, depends_on, parallel_with, non-integrable block,
  risk, stop condition, test_owner (§4).
- **Campaign-rule-2 field set per unit (verified 2026-08-14, task
  `f7ae2d38`, audit `524eb154` disposition)** — all eight fields live per
  unit in §4: `outcome` (outcome row); exact write scope (`primary files` +
  `write_scope` rows); first failing oracle (`red` row); closeout command
  (`green` row — lane-local `FABER_BIN`/`FABER_LIBRARY_HOME` invocation);
  expected observed result (`green`/`done_when` rows); est_basis
  justification (`est_work_tokens` row + §12 aggregate justification); stop
  condition (`stop condition` row — added by this amendment); depends_on
  (depends_on row). No field lives only at the aggregate → no aggregate-field
  waiver is recorded (M3 follow-up pattern, task `954f8d4a`); G1's lane-owned
  closeout is the only aggregate-resident validation (§9).
- **Audit disposition absorbed (2026-08-14, audit `524eb154` — REVISE on
  planner-26 `74c7af2`)**: substantive MoE content ADMITTED; frontier (F1) +
  single-unit shape (F2) superseded by this re-split (`f81b687` + `936bb9d`);
  F3 two-revision disclosure confirmed as an explicit open item (§13.1).
  planner-26/`74c7af2` retired as dispatch authority; this artifact is the
  MODEL-02 dispatch artifact.
- Red oracle table checked for every child (§8).
- `git diff --check` on this artifact: silent (run below).
- **Frontier correction (2026-08-13, task `57c57d14`, audit `c7e9a272`)**:
  every MODEL-01 dispatch/dependency statement now gates on the **LIB-02 +
  LIB-03** aggregate gates only; REF-01 is a sibling chain of MODEL-01, not a
  predecessor; **A1 (silu) is independently eligible before the MODEL-01
  gate**, subject only to consume-or-add resolution against the sibling
  REF-01. No implementation scope, unit, fact, successor, sizing, write
  scope, or integrability was changed.
- No Hand tasks were filed and no product code was touched (planning only).

## 12. Work-token estimates

| Unit | est_work_tokens | est_basis |
| --- | --- | --- |
| A1 | 3–5k | pilot — one additive nn activation row |
| A2 | 4–6k | pilot — deterministic probe/fixture corpus |
| A3 | 5–8k | pilot — independent oracle + goldens derivation |
| B1 | 3–5k | pilot — first module type/error contract |
| B2 | 5–7k | pilot — router selection math in Fab |
| B3 | 5–8k | pilot — windowed rank-3 dispatch in Fab |
| B4 | 5–8k | pilot — layer FFN composition in Fab |
| C1 | 4–6k | pilot — exemplar phase |
| C2 | 4–6k | pilot — 4 docs, selectively touched |
| C3 | 3–5k | pilot — mechanical re-baseline + status/registration |
| G1 | 3–5k | pilot — one aggregate validation pass + merge |

Aggregate ≈ **44–69k**, staged so no single Hand exceeds 8k or one behavior
family. The cited plan's 20k–36k single unit bundled type+router+dispatch+
composition+oracle+exemplar+docs+records into one session; this split routes
those to A2/A3, B1–B4, C1, C2, and C3/G1, with the separated oracle-fixture,
docs, records, and gate units carrying their own proofs (the same pattern
MODEL-01/LIB-02 used). The aggregate band is the honest cost of the turnover
law's shape; it is staged so no single Hand exceeds the law.

## 13. Open questions for Mind (none blocks this lowering)

1. **Comparator authority question (preserved for audit, NOT resolved).** The
   semantic source pins llama.cpp **`a957b7747`** for the MoE math; the
   campaign's full-model comparator pins **10150 (`dee2a846b`)**
   (`gi4-engine-comparison-pin.md`). This lowering preserves both pins at
   their boundaries exactly as the citing need `401dd88f` flagged. The
   authority question — which revision governs the full-model boundary and
   how a divergence between them is adjudicated — is routed to the MODEL-02
   audit and the GGUF-M4 boundary recheck, never resolved by an implementing
   Hand. **F3 (audit `524eb154`, disposition 2026-08-14) — confirmed recorded
   as an explicit open item**: the two-revision divergence authority
   (`a957b7747` semantic source vs the 10150/`dee2a846b` full-model
   comparator) is disclosed here exactly as cited, stays open, and is
   adjudicated at the GGUF-M4 boundary recheck — never by an implementing
   Hand.
2. **Dispatch timing.** The MODEL-01 aggregate gate lands after the **LIB-02 +
   LIB-03** aggregate gates only (REF-01 is a sibling, not a MODEL-01
   predecessor). **A1 is independently eligible before MODEL-01** (silu
   consume-or-add vs the sibling REF-01); A2 ∥ B1 is the first eligible
   frontier after MODEL-01. If MODEL-01 slips, A1 may still dispatch (its
   silu authority is a sibling recheck), while the gated units wait — the
   chain does not overlap those implementations.
3. **`silu` presence (A1).** REF-01's chain plans a generic SiLU row; if it
   lands before A1 dispatches, A1 narrows to consume-and-record (no duplicate
   row). The frozen `silu(tensor.Tensor x) → tensor.Tensor ⇥ NnError` spelling
   is the pin either way.
4. **Frozen surface naming.** The `ConfiguraMoe`/`MoError`/`SelectioExpertarum`/
   `eligito`/`expertum`/`ffn_moe` spellings are frozen by §2 per the codebase
   Latin convention; any amendment routes through the delivery-amendment path
   (A1a precedent). C2 documents the actual merged surface (report-driven).
5. **Tie-rule validation scope.** The crafted exact-tie probe proves OUR
   deterministic rule (lowest index first); llama.cpp's argsort tie order is
   implementation-defined and is only re-validated at GGUF-M4's full-model
   boundary. Recorded honestly; not a block.
6. **Regression-corpus version.** MODEL-01's C2 bumps to v1.5.0; C2 here bumps
   one step further on the MODEL-02 base. No conflict — the earlier bump lands
   first.

## 14. Honesty gate

This lowering re-splits the cited fresh GGUF-M2 delivery; it does not pretend
the micro-unit chain is more. It does not compile A3/M-units, does not lower
MODEL-03/04, and does not claim the campaign invariant. Chain completion is
not campaign completion: MODEL-02 completion yields the MoE component-level
proof (router/expert/shared-expert execution authority for GGUF-M4/M5) and
advances milestone Q2; the Qwen3.6 invariant requires the full
LIB/REF/MODEL/EXEC/CAP chain through CLOSE-01, preserved verbatim (§10).
MODEL-01 (LIB-02 + LIB-03 gated) and the sibling REF-01 are separate
mandatory chains owned by their own deliveries, not absorbed here (§7). The
comparator authority question
is preserved verbatim for audit, not resolved (§13.1).

---

*Planning artifact only. No product code was written by this lowering.
MODEL-02/GGUF-M2 is re-lowered as eleven micro-units (A1–C3) plus the sole
aggregate gate G1: silu primitive (A1) → probe corpus (A2) → goldens oracle
(A3) → type/error contract (B1) → router `eligito` (B2) → expert dispatch
`expertum` (B3) → complete `ffn_moe` (B4) → exemplar receipt (C1) ∥ docs (C2)
→ records/inventory (C3) → atomic integration (G1). The first eligible
frontier after MODEL-01 is A2 ∥ B1, with **A1 (silu) independently eligible
before MODEL-01** subject only to consume-or-add resolution against the
sibling REF-01. Every frozen fact — comparator
authority question, deterministic tie rule, top-k probability selection and
`norm_w=true` renormalization, shared-expert sigmoid gating, the exact rank-3
mapping/storage union {F32, BF16, Q4_K, Q5_K, Q6_K, Q8_0}, the block-40 MTP
exclusion, and the successor chain through CLOSE-01 — is preserved; no child
lane gate exists, and G1 is the single aggregate merge gate. The unit advances
milestone Q2 without completing the campaign. Campaign-rule-2 field set
verified per unit (task `f7ae2d38`, audit `524eb154`): per-unit `stop
condition` rows added (§4); F3 divergence authority confirmed as an explicit
open item (§13.1).*
