# Delivery: GGUF-M2 — Qwen35MoE Router And Expert Execution (Qwen MODEL-02)

**Status**: SUPERSEDED 2026-08-22 by [`pml5-gguf-m2-moe-router-delivery-2026-08-22.md`](pml5-gguf-m2-moe-router-delivery-2026-08-22.md) (MODEL-01 merged; the Latin surface spellings were retracted by the live dialect; `silu` landed on main). Historical: lowered 2026-08-13 by planner-26 (task `1b07f5c0` / handle `1b07f5c0`) — **READY at the spec level; dispatch-gated on MODEL-01 (GGUF-M1) landing and the LIB-03 (GGUF-A3) BF16/Q5_K codecs**. Planning artifact only: no product code is written by this lowering.
**Campaign**: [`radix/docs/factory/gpu-production-readiness/CAMPAIGN.md`](../../../../radix/docs/factory/gpu-production-readiness/CAMPAIGN.md) — umbrella row **MODEL-02** ("Implement MoE router and expert execution")
**Delivery authority**: [`pml5-general-gguf-delivery.md`](pml5-general-gguf-delivery.md) — unit **GGUF-M2** ("MoE Router And Expert Execution")
**Repo**: `gradus` (branch `factory/planner-26`, baseline `bc500993c97b99bb4ca3ff0d98828b56c750eec0`); planning docs only
**Goal chain (goal-check)**: umbrella goal `gol_634a0417d02c510f` (Qwen3.6 35B GGUF execution — sole priority) -> PML5-GGUF delivery-authority goal `gol_67b635603712f01b` -> this unit. Both goals are registered in Vivi (`vivi goal list` 2026-08-13). **Goal-check: PASS — no new goal or forge needed**; this lowering is the delivery-level unit spec under the existing registered chain.
**Freshness**: derived independently from the campaign, the delivery authority, the live product repos, the pinned llama.cpp source checkout (`/Users/ianzepp/work/ianzepp/llama.cpp` @ `a957b7747`), and the real local artifact (read-only). No planner-1..19 worktree, commit, partial artifact, or cancelled transcript was read.

## Unit Identity

| Field | Value |
| --- | --- |
| Umbrella row | **MODEL-02** — "Implement MoE router and expert execution" |
| Umbrella done oracle | Router choices, expert weights, intermediate values, and outputs match the independent oracle |
| Delivery unit | **GGUF-M2** — MoE Router And Expert Execution |
| Delivery done oracle | Selected layers match independent router choices, expert weights, intermediate values, and outputs for pinned hidden-state probes |
| Owner | Gradus |
| Depends on | **MODEL-01 (GGUF-M1)** — `qwen35moe` admission + tensor map (entry gate, see §Predecessor And Entry Gate); transitively **LIB-03 (GGUF-A3)** union codec set and **REF-01 (GGUF-A4)** shared primitives |

## Outcome (exact executed result)

The unit lands a public `gradus:*` MoE surface that

1. computes **router logits** for a pinned hidden-state probe against the admitted `qwen35moe` router weight (`ffn_gate_inp.weight`), producing the full `[n_expert]` logit row per probe,
2. applies the artifact's declared **expert selection** — softmax over all `n_expert`, select the top `n_expert_used` by probability — with a **deterministic tie rule** (lowest expert index first on exact ties) and the artifact's declared **weight normalization** (renormalize the selected probabilities by their sum; the `norm_w=true` semantics),
3. accesses **rank-3 expert projections** (`ffn_gate_exps.weight`, `ffn_up_exps.weight`, `ffn_down_exps.weight`, each `[n_embd/ff, n_ff_exp, n_expert]`) through the GGUF-A3 windowed materialization surface,
4. executes per-expert **SwiGLU dispatch** (`silu(gate) * up`, then down) and **accumulation** (per-expert outputs scaled by their normalized weights and summed),
5. executes the **shared expert** (`ffn_gate_shexp`/`ffn_up_shexp`/`ffn_down_shexp`) with its **sigmoid gate** (`ffn_gate_inp_shexp`) and adds the gated shared-expert output to the routed sum — the complete layer FFN output,
6. proves **selected layers match the independent oracle** — a pinned Python reference (the gi2-dequant-reference precedent) computing the same MoE math in f32 from the real artifact's dequantized tensors, with committed goldens — through an executed package-MIR exemplar plus deterministic in-repo synthetic fixtures (including a crafted exact-tie probe).

The unit's done oracle is **component-level only**: router choices, weights, intermediate values, and layer outputs for pinned probes. It is **not** a full-model, token, logit, or device claim — full-model reference inference is GGUF-M4 (MODEL-04), and native execution is GGUF-M5/GGUF-A7.

## Ground Truth (verified live 2026-08-13)

Baseline state (gradus `bc500993c97b`, tree clean at the branch tip; `./scripta/check-source` PASS).

### Artifact facts (read live from the exact completion row)

Parsed read-only from `/Users/ianzepp/ai/models/Qwen3.6-35B-A3B-UD-Q4_K_M.gguf` (22,663,387,424 bytes, SHA-256 `0b21525e972670ed59e1812e170b27c26355381f0656ecc4e25617ece7dac58b` — the campaign invariant; independent reader `/opt/homebrew/bin/llama-gguf` r 1, plus a bounded byte-level reader):

| GGUF key | Value | MoE role |
| --- | --- | --- |
| `general.architecture` | `qwen35moe` | — |
| `qwen35moe.block_count` | **41** | 40 main trunk + 1 MTP layer (layer 40, `nextn_predict_layers` = 1) |
| `qwen35moe.embedding_length` | **2048** | `n_embd` |
| `qwen35moe.expert_count` | **256** | `n_expert` |
| `qwen35moe.expert_used_count` | **8** | `n_expert_used` |
| `qwen35moe.expert_feed_forward_length` | **512** | `n_ff_exp` (routed experts) |
| `qwen35moe.expert_shared_feed_forward_length` | **512** | `n_ff_shexp` (shared expert) |
| `qwen35moe.attention.layer_norm_rms_epsilon` | `9.999999974752427e-07` (1e-6 as stored F32) | FFN-input norm epsilon (owned by REF-01/MODEL-03; cited here for probe realism) |
| `qwen35moe.expert_weights_scale` | **absent** | no per-expert weight scaling (`w_scale` stays 0.0f → the scale step is skipped) |
| `general.file_type` / `general.quantization_version` | 15 / 2 | Q4_K_M, quant v2 |
| 753 tensors / 55 metadata KVs | — | GGUF-A1b receipt |

### MoE tensor facts (per-layer survey of the live artifact)

All 41 layers carry the full MoE tensor set. GGUF shapes are listed as parsed (`ne[0]` = contiguous dimension); the `blk.N.` prefix covers every layer including the MTP layer 40:

| Tensor | GGUF shape | GGML storage (layers) | Role |
| --- | --- | ---: | --- |
| `blk.N.ffn_gate_inp.weight` | `[2048, 256]` | F32 (layers 0–39), **BF16 (layer 40)** | router weight |
| `blk.N.ffn_gate_inp_shexp.weight` | `[2048]` | F32 (0–39), **BF16 (40)** | shared-expert gate weight (scalar per token) |
| `blk.N.ffn_gate_exps.weight` | `[2048, 512, 256]` | Q4_K (all 41) | routed expert gate projections |
| `blk.N.ffn_up_exps.weight` | `[2048, 512, 256]` | Q4_K (all 41) | routed expert up projections |
| `blk.N.ffn_down_exps.weight` | `[512, 2048, 256]` | **Q5_K** (38 layers), **Q6_K** (layers 34, 38, 39) | routed expert down projections |
| `blk.N.ffn_gate_shexp.weight` | `[2048, 512]` | Q8_0 (all 41) | shared expert gate |
| `blk.N.ffn_up_shexp.weight` | `[2048, 512]` | Q8_0 (all 41) | shared expert up |
| `blk.N.ffn_down_shexp.weight` | `[512, 2048]` | Q8_0 (all 41) | shared expert down |

Physical layouts used by the MoE path: **{F32, BF16, Q4_K, Q5_K, Q6_K, Q8_0}** — the exact union set GGUF-A3 (LIB-03) already lowers. The BF16 rows exist only on layer 40 (the MTP layer); probing layer 40 exercises the BF16 codec.

### Layer schedule (MoE placement)

From the pinned llama.cpp `load_arch_hparams` (`src/models/qwen35moe.cpp` @ `a957b7747`): `n_main = n_layer − nextn_predict_layers = 40`; layer `i` is recurrent (Gated DeltaNet) when `i < 40 && (i+1) % 4 != 0` — so main attention layers are 3, 7, 11, …, 39 (10 layers), the other 30 main layers are SSM, and layer 40 is the MTP block. **The MoE FFN is present and identical in shape on every layer**, consuming the post-attention-norm (post-SSM-norm) hidden state. MODEL-02 therefore probes the MoE block independently of the attention/SSM family; MODEL-03 owns the attention/SSM state in front of it.

### Exact MoE semantics (pinned from llama.cpp source @ `a957b7747`)

The reference implementation is the pinned llama.cpp `build_moe_ffn` + the qwen35moe `build_layer_ffn` (`src/llama-graph.cpp`, `src/models/qwen35moe.cpp` @ `a957b7747`). For this artifact the invoked path is, exactly:

1. **Router logits**: `logits = x @ ffn_gate_inp` → `[n_expert]` per token (GGML `mul_mat`, no bias — there is no router bias tensor).
2. **Selection probabilities**: `probs = softmax(logits)` over all `n_expert` (max-subtracted, f32).
3. **Top-k**: `selected = argsort_desc(probs)[0..n_expert_used)` — the 8 largest probabilities, in descending-probability order. (Selection by probability, not by raw logit; equivalent because softmax is monotonic.)
4. **Weights**: `weights = probs[selected]` (the selected probabilities), then `weights /= max(sum(weights), 6.103515625e-5)` — the `norm_w=true` renormalization. No `expert_weights_scale` applies (key absent; scale step skipped).
5. **Routed expert FFN** (per selected expert `e`): `gate_e = x @ ffn_gate_exps[:, :, e]`, `up_e = x @ ffn_up_exps[:, :, e]`, `h_e = silu(gate_e) * up_e`, `out_e = h_e @ ffn_down_exps[:, :, e]`.
6. **Accumulation**: `moe_out = Σ_e weights[e] · out_e`.
7. **Shared expert**: `shexp = (silu(x @ ffn_gate_shexp) * (x @ ffn_up_shexp)) @ ffn_down_shexp`; gate `g = sigmoid(x · ffn_gate_inp_shexp)` (scalar per token).
8. **Layer FFN output**: `ffn_out = moe_out + g · shexp`.

**Deterministic tie rule** (delivery authority: "deterministic tie behavior"): on exact ties in selection probability at the selection boundary, the **lowest expert index wins** (stable-descending order). This matches the codebase's existing sampling convention ("first-index ties", `src/sampling.fab`) and is the rule the reference and Gradus both implement; a crafted tie probe proves it. Note recorded honestly: llama.cpp's `std::sort`-based argsort is not stable on exact ties (implementation-defined), so the pinned reference and Gradus share OUR deterministic rule and the full-model boundary (GGUF-M4) re-validates end-to-end against llama.cpp; a real-tie divergence there would be recorded as a divergence, never silently matched.

## Predecessor And Entry Gate

- **Predecessor receipt**: MODEL-01 = **GGUF-M1** (`qwen35moe` admission and tensor map). Its done oracle: the exact Qwen3.6 artifact admits with 753 tensors and a complete typed execution configuration; mutated metadata/names/shapes/storage layouts fail with typed first-divergence diagnostics. MODEL-01 owns `src/model/qwen35moe.fab` + proba (the admitted `ConfiguraMoe`-equivalent facts `n_expert`, `n_expert_used`, `n_ff_exp`, `n_ff_shexp`, `n_embd`, canonical tensor names) that this unit consumes — it does not re-derive them.
- **Transitive codec prerequisite**: LIB-03 = **GGUF-A3** must be landed for the union codec set **{F32, BF16, Q5_0, Q8_0, Q4_K, Q5_K, Q6_K}** and the windowed `TensorView`/`materialize_slice` surface. The MoE probes on layers 0/3/39 need F32/Q4_K/Q5_K/Q6_K/Q8_0; the layer-40 probe additionally needs **BF16**. No layout outside the LIB-03 union set appears in the MoE path.
- **Shared primitives**: `silu` is not yet a public `gradus:nn` primitive (the live `nn.fab` exposes `linear`, `gelu`, `layernorm`). This unit adds the public `silu` row (scalar + tensor) in `gradus:nn` if it is not present at its boundary — hunk-serialized with REF-01's planned nn rows (see §Implementation Frontier).
- **Entry-gate state at the lowering boundary**: GGUF-M1 is **NOT landed** (planner-25 is lowering it in parallel; no MODEL-01 commit exists on any `factory/planner-*` branch at this boundary). LIB-03/GGUF-A3 is lowered (planner-23, commit `a7d7bcd`) but not yet landed either.
- **Lowering disposition**: this spec is **complete and READY**; dispatch of the implementing Hand is **gated on the GGUF-M1 receipt** (the affected edge `M1 → M2` blocks; execution rule 6 — no other ready unit is affected, and GGUF-M3 (MODEL-03) runs parallel-safe on the disjoint attention/SSM state surface). **Recheck handles**: the GGUF-M1 closeout record in `pml5-general-gguf-delivery.md` / gradus `CAMPAIGN.md` status line; the GGUF-A3 closeout record for the union codec set.
- **Executed-tier lever (CTO8-1)**: the FMIR library-call gap remains the named open gate for *executed-token/model identity* claims. This unit's executed claims are at the **A1b precedent tier**: package-MIR exemplar receipts with observed PASS lines over real tensor slices and in-repo fixtures. No token, logit, model-execution, or device claim is made here; full executed-model identity remains gated on CTO8-1 (GGUF-A4+).

## First Failing Oracle

The first red case the implementing Hand writes before any MoE code, per red-green:

```text
case router-topk-tie-probe:
  eligito(probe_vector, ffn_gate_inp, ConfiguraMoe{n_expert=8, n_used=2})
    → must return [2, 5] (exact-tie selection, lowest-index-first)
  current: no MoE surface exists — the call does not compile (RED)
```

then the rank-3 expert-slice case (a per-expert window of `ffn_gate_exps.weight` materializes to the pinned f32 golden values), then the full `ffn_moe` probe case against the committed goldens (first-divergence rule: report the first divergent element index, never a tolerance-widened pass), then the negative matrix (unknown tensor name, shape mismatch, un-admitted GGML type, non-finite input → typed `MoError`, never a silent default).

## Public Surface (frozen for this unit)

The exact spellings below follow the codebase's Faber Latin convention and the A1a amendment precedent (`inveni_tensorem`). Any spelling change at implementation routes through the delivery-amendment path; no compatibility alias is added.

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

`MoError.TypoIgnotum` mirrors the dequant fail-closed rule (un-admitted physical type before any byte is touched); `NomineIgnota` mirrors the manifest error for an unknown tensor name; `NonFinita` rejects a NaN/±Inf probe or intermediate (finite-value gate, gi0-numeric-contract discipline adapted to component values). No `gradus:model/moe` value owns a path, reader, source function, or device object.

### `gradus:nn` — additive public primitive

```text
# SiLU activation: silu(x) = x · sigmoid(x), self-hosted exp precedent (nn._exp).
functio silu(tensor.Tensor x) → tensor.Tensor ⇥ NnError
```

If REF-01's generic SiLU row lands first, this unit consumes it instead of adding a duplicate — the shared-file discipline below.

## Write Scope (exact)

All paths under the implementing Hand's gradus worktree on `factory/planner-26`; gradus is a dedicated-agent repo added per task via `--repos gradus`:

- `src/model/moe.fab`, `src/model/moe.proba` (create — the frozen surface above)
- `src/nn.fab`, `src/nn.proba` (add the public `silu` row only, unless present at the boundary)
- `src/model/qwen35moe.fab` / `.proba` — **read-only** (MODEL-01's admission surface; this unit consumes the admitted config and tensor names, it does not edit them)
- `fixtures/gguf/gen_moe_probes.py`, `fixtures/gguf/gen_moe_goldens.py`, `fixtures/gguf/gguf-moe-probes.json`, `fixtures/gguf/gguf-moe-goldens.json`, `fixtures/gguf/gguf-moe-goldens-oracle.md` (create; deterministic in-repo probe vectors + synthetic fixtures including the crafted exact-tie case; schema `gguf-moe-goldens-v1`)
- `exempla/moe-router-probe/faber.toml`, `exempla/moe-router-probe/src/main.fab`, `exempla/moe-router-probe/README.md` (create; app-owned file adapter + real-file MoE probe receipt on the selected layers, mirroring `exempla/gguf-materialize`)
- `scripta/check-compile` and `scripta/check-compile.fab` (add the `moe-router-probe` exemplar target)
- Docs: `README.md` (module list), `docs/module-map.md` (new `gradus:model/moe` row + counts), `docs/api-reference.md` (new `gradus:model/moe` section + `nn.silu` row; run `scripta/inventory-public-symbols` per its committed coverage gate), `docs/diagnostics.md` (`MoError` table), `docs/regression-corpus.md` (bump to `gradus-regression-corpus v1.4.0` — from the version live at the unit boundary, currently v1.2.0; the LIB-03 lowering targets v1.3.0; new proba suites + goldens), `docs/factory/production-ml-library/pml0-symbol-inventory.md` (new public symbols + module counts), `docs/factory/production-ml-library/pml0-support-matrix.md` (MoE router/expert row at the **output-checked component tier** — see §Validation), and the owning delivery/status docs (`pml5-general-gguf-delivery.md` GGUF-M2 section marked implemented + gradus `CAMPAIGN.md` status line) at the unit's closeout.
- Closeout commit on `factory/planner-26` (gradus lane).

## Read Scope

- `pml5-general-gguf-delivery.md` (GGUF-M1/M2/M3/M4 + clean boundary + unit graph), umbrella `CAMPAIGN.md`, gradus `CAMPAIGN.md`
- Live `src/model/qwen35moe.fab` (MODEL-01 admission — at dispatch; before it lands, the admission facts in §Ground Truth are the spec), `src/model/tensor_view.fab`, `src/model/tensor_payload.fab`, `src/model/gguf_manifest.fab`, `src/model/dequant.fab`, `src/nn.fab`, `src/math.fab`, `src/tensor.fab` (the LIB-03 / primitive surfaces)
- `exempla/gguf-materialize` and `exempla/gguf-inspect` (the file-adapter + windowed-range + receipt pattern to mirror)
- Radix evidence cited read-only: `gpu-inference-gguf/evidence/gi2-dequant-reference.py` + `gi2-dequant-goldens.json` (the independent-reference/oracle precedent), `gi0-numeric-contract.md` (finite gate + first-divergence discipline), `gi0-comparator-contract.md` + `gi4-engine-comparison-pin.md` (pinned llama.cpp 10150/`dee2a846b` comparator for the full-model boundary)
- The pinned llama.cpp source `/Users/ianzepp/work/ianzepp/llama.cpp` @ `a957b7747` (`src/llama-graph.cpp` `build_moe_ffn`/`build_ffn`, `src/models/qwen35moe.cpp`) — the semantic oracle
- The real artifact `/Users/ianzepp/ai/models/Qwen3.6-35B-A3B-UD-Q4_K_M.gguf` (read-only)

## Forbidden Scope

- No tokenizer work (GGUF-A2/LIB-02), no packed-storage codec or materializer edits (GGUF-A3/LIB-03), no admission/tensor-map edits (GGUF-M1/MODEL-01 — read-only), no SSM/attention state (GGUF-M3/MODEL-03), no full-model assembly/logits/tokens (GGUF-M4/MODEL-04), no dense reference rows (GGUF-A4–A6/REF-01 — the shared `nn.fab`/`transformer.fab`/`attention.fab` surfaces are hunk-serialized, not independently restructured), no KV/decode/sampling/generation (PML5 U1–U6), no GPU/lowering/kernel/`DeviceProgram` (Radix), no physical storage/residency (Hosts), no HTTP/serving (product repo), no changes to `src/model/capsule.fab`/`gguf.fab`/`safetensors.fab` (LIB-01 A1c scope), no edit to `pml5-general-gguf-delivery.md` beyond the GGUF-M2 closeout lines, no CAMPAIGN-semantics edits, no whole-workspace cargo/nextest in-loop (narrow `faber check` + one closeout run per boundary), no foreign dirt, no write to the main checkout or any other worktree.

## Implementation Frontier And Split Boundary

Split-on-boundary (each slice a landed commit; no dual authority ever exists between slices):

- **M2-C1 — silu + router (first implementation frontier)**: the public `silu` row in `nn.fab` (if absent), then `eligito` — router logits, softmax, deterministic top-k with the tie rule, weight renormalization — with the synthetic fixture + crafted tie probe in `moe.proba`. Independent and first; carries the first failing oracle.
- **M2-C2 — rank-3 expert dispatch + accumulation**: `expertum` (per-expert window reads through `TensorView`/`materialize_slice` + per-expert SwiGLU) and the weighted-sum accumulation; the synthetic multi-expert fixture (including a Q4_K/Q5_K expert window exercised through the real codecs).
- **M2-C3 — shared expert + full `ffn_moe`**: `ffn_gate_inp_shexp` sigmoid gate + shared-expert FFN + the complete `ffn_moe` composition; full-probe goldens.
- **M2-C4 — exempla receipt + docs + closeout**: `exempla/moe-router-probe` real-file receipt across the selected layers (0, 3, 39, 40 — see §Oracle), `scripta/check-compile` targets, all doc updates, the support-matrix row, the closeout commit.

Serial `C1 → C2 → C3 → C4`; no parallel children needed (single Hand owns the shared `src/model/` files; the sibling MODEL-03 Hand is hunk-serialized on the shared `src/model/` tree via landed-commit boundaries, and the REF-01 Hand on `src/nn.fab` likewise — each handoff a landed commit).

## Oracle And Local Corpus Boundary

- **Independent oracle**: a pinned Python reference `fixtures/gguf/gen_moe_goldens.py` (the gi2-dequant-reference precedent) that (a) reads the real artifact read-only and verifies the pinned identity, (b) dequantizes the router/expert/shared-expert tensors with the GGUF-A3 codec semantics (llama.cpp `ggml-quants.c` @ `a957b7747`, bit-exact), and (c) computes the exact §Ground-Truth MoE semantics in numpy f32 for the pinned probe vectors — producing committed goldens `gguf-moe-goldens.json` (schema `gguf-moe-goldens-v1`). The goldens record, per (layer, probe): full router logits `[256]`, the top-8 indices, the 8 normalized weights, the full `ffn_moe` output `[2048]`, and the full shared-expert and per-expert outputs `[2048]/[512]` as f32 arrays (JSON).
- **Probe vectors** (`gguf-moe-probes.json`): deterministic pinned `[2048]` f32 hidden-state probes at realistic post-norm magnitudes (unit-variance seeded vectors; magnitudes documented against the RMSNorm unit-scale property). Two probes per selected layer, plus one in-repo synthetic exact-tie probe (small hand-built config, not from the artifact).
- **Selected layers**: **layer 0** (recurrent/SSM block; F32 router, Q5_K down), **layer 3** (attention block; F32 router, Q5_K down), **layer 39** (last main attention block; **Q6_K** down — exercises the Q6_K codec), **layer 40** (MTP block; **BF16** router + gate — exercises the BF16 codec). These four cover both layer families, all four routed-expert storage types (Q4_K gate/up; Q5_K/Q6_K down), the F32 and BF16 router rows, and the MTP block.
- **Comparison policy** (component-level, adapted from gi0-numeric-contract discipline): router/expert **indices exact** (integer identity, tie rule included); continuous values (logits, weights, intermediates, outputs) compared **per element** against the goldens under a **band derived at the unit boundary** by the gi0-6 method — evaluate the reference's math in strict f64 on the same probes, take `R` = max per-element `|f32_ref − f64_ref|` over the probe set (the representational floor of the reference math), and set `Δ = 10·R` rounded up to the next power of ten — **capped at the gradus forward band `5e-4`** for normalized values in `[0,1]` and at the `numeric-policy v1.0.0` matmul row (`1e-5` atol / `1e-5` rtol) as the family floor for pure-matmul outputs. Every comparison record carries a finite-value gate (no NaN/±Inf) and the **first-divergence rule**: the first divergent element index + the failing value pair, recorded before any later agreement.
- **Local corpus**: the real artifacts under `/Users/ianzepp/ai/models/` (the four mandatory files + the two additional `qwen35moe` rows) are operator evidence, never committed and never redistributed; Gradus never receives their paths — the exempla's app-owned adapter resolves them (the `gguf-inspect`/`gguf-materialize` pattern). Goldens are derived values committed as fixtures; the model file stays local.

## Closeout Commands And Expected Observed Result

From the Hand packet (substitute the lane worktree paths):

```bash
cd <hand-worktree>/gradus
./scripta/check-source
env FABER_LIBRARY_HOME=<worktree-root> \
  FABER_BIN=<worktree>/radix/target/debug/faber ./scripta/check-compile
env FABER_LIBRARY_HOME=<worktree-root> \
  <worktree>/radix/target/debug/faber run --target fmir exempla/moe-router-probe -- \
  /Users/ianzepp/ai/models/Qwen3.6-35B-A3B-UD-Q4_K_M.gguf 10991392 \
  0b21525e972670ed59e1812e170b27c26355381f0656ecc4e25617ece7dac58b
git diff --check -- src/model/moe.fab src/model/moe.proba src/nn.fab src/nn.proba \
  fixtures/gguf/gen_moe_probes.py fixtures/gguf/gen_moe_goldens.py \
  fixtures/gguf/gguf-moe-probes.json fixtures/gguf/gguf-moe-goldens.json \
  fixtures/gguf/gguf-moe-goldens-oracle.md exempla/moe-router-probe \
  scripta/check-compile scripta/check-compile.fab README.md docs/module-map.md \
  docs/api-reference.md docs/diagnostics.md docs/regression-corpus.md \
  docs/factory/production-ml-library/pml0-symbol-inventory.md \
  docs/factory/production-ml-library/pml0-support-matrix.md \
  docs/factory/production-ml-library/pml5-general-gguf-delivery.md \
  docs/factory/production-ml-library/CAMPAIGN.md
```

**Expected observed result**: `check-source` and `check-compile` exit 0; `faber check` ends `ok: .`; the MoE probe exemplar prints PASS lines — one per (layer, probe) golden: `PASS layer=0 probe=p1 logits=<hash> indices=[...] weights=<...>`, `PASS layer=3 …`, `PASS layer=39 …`, `PASS layer=40 …` (with exact index equality, first-divergence `none`, max absolute deviation `≤ Δ`), plus the synthetic fixture lines (including the exact-tie case `indices=[2,5]`) and the negative-matrix lines; zero FAIL lines; exit 0. The receipt (in `exempla/moe-router-probe/README.md`) records the exact command, content identities, selected layers, probe hashes, observed indices/weights/values, the derived `Δ`, and the first-divergence record (none expected). `git diff --check` silent. The support-matrix row is classified **output-checked at the MoE component tier** (never executed-token/model identity — CTO8-1 stays the named gate).

## Hardware / Backend Authority

Device-neutral unit. The exempla receipt executes on **burgus** (the local host that produced the A1b/A3 receipts; Apple M5 Max, CPU-only reference runs, no backend). No Metal/CUDA/GPU claim; no paid infrastructure; no device handle enters a `gradus:*` value. Native quantized MoE execution is GGUF-A7/GGUF-M5 territory (Radix/Hosts); the full-model llama.cpp comparator (10150/`dee2a846b`) agreement is GGUF-M4's boundary, recorded as this unit's recheck handle.

## Successor Preservation Through CLOSE-01

This lowering preserves every mandatory successor; nothing is narrowed, deferred, made optional, or moved outside the campaign:

- GGUF graph: `M1 → M2 ‖ M3`; `M2 + M3 → M4` (full-model reference inference consumes the `ffn_moe` surface per layer), `M4 → M5` (native Metal/CUDA), `M5 → M6` (Faber capstone + closeout). Upstream: `A1c → A2 ‖ A3 → A4/A5/A6 → M1`. The unit's `ffn_moe`/`eligito`/`expertum` surface is the MoE execution authority GGUF-M4/M5 consume; GGUF-M3 reads the same admission facts but owns the disjoint SSM/attention state.
- Umbrella rows: MODEL-02 → MODEL-04 → EXEC-01/02 → EXEC-03 → CAP-01/02 → CLOSE-01.
- The full-model router choices validated here as component goldens are re-validated end-to-end at MODEL-04's first-divergence boundary against the pinned llama.cpp comparator; a divergence found there routes back to this surface with the first-divergence record, never a silent match.

## Scope Closure Statement

- **Milestone advanced**: umbrella **Q2 — complete model semantics** (dense reference rungs plus full `qwen35moe` reference execution; gates A4–A6 and M1–M4). MODEL-02 completes the MoE third of the `qwen35moe` semantics, parallel to MODEL-03's SSM/attention half.
- **Why unit completion is not campaign completion**: Q4 (the Faber invariant — one public-Gradus capstone running the exact artifact through the complete `qwen35moe` graph for two prompts on Metal and CUDA) requires the full chain LIB-01..CLOSE-01. This unit adds the MoE component-level executed proof at the package-MIR probe tier only; it is not an execution, token, model, or device claim, and Q4 remains mandatory with every clause intact.

## Estimate

- **est_work_tokens**: 20k–36k. **est_basis**: pilot (extrapolated — new gradus MoE surface + public silu row + independent Python reference + committed goldens + package-MIR exempla receipt; comparable to the GGUF-A3 lowering's 18k–28k scaled up for the router/top-k/tie/dispatch surface; no close ledger class).
- **tool_latency**: medium — `check-source`/`check-compile` (narrow) plus one `faber run --target fmir` exempla execution and the oracle-derivation step (the f64 reference evaluation on 8 probe vectors × 4 layers); no cargo, no device runs.

## Stop Conditions / Escalation

- If GGUF-M1 has not landed at the dispatch boundary, the Hand records the recheck and stops (never proceeds on an un-admitted configuration — "summaries are claims"). The admission facts in §Ground Truth are the spec *for the lowering*; the Hand consumes the admitted `qwen35moe.fab` at dispatch.
- If a selected layer's live layout lies outside the LIB-03 union set {F32, BF16, Q5_0, Q8_0, Q4_K, Q5_K, Q6_K}, the unit records the exact tensor and routes a correction (campaign stop condition) — no silent widening.
- A golden mismatch on any probe is a divergence receipt naming the first divergent element (index + value pair), never a tolerance-widened pass (truth over safety).
- A router/expert index mismatch (including a tie-rule mismatch) is a hard fail — indices are exact.
- If `silu` lands in `nn.fab` from the REF-01 lane while this unit runs, the unit consumes it and records the consumed revision (no duplicate row, no dual authority).

## Open Items For Mind (none blocks this lowering)

1. **GGUF-M1 (MODEL-01) landing** — the dispatch gate for this unit; recheck at the GGUF-M1 closeout.
2. **GGUF-A3 (LIB-03) landing** — the BF16/Q5_K codec and `TensorView` surface the MoE probes consume; recheck at the A3 closeout.
3. **Exact public spellings** (`ConfiguraMoe`/`SelectioExpertarum`/`eligito`/`expertum`/`ffn_moe`/`silu`) — frozen by this lowering per the codebase Latin convention; any amendment routes through the delivery-amendment path (A1a precedent).
4. **Tie-rule validation scope** — the crafted exact-tie probe proves OUR deterministic rule (lowest index first); llama.cpp's argsort tie order is implementation-defined and is only re-validated at GGUF-M4's full-model boundary. Recorded honestly; not a block.

---

*Planning artifact only. No product code was written by this lowering. MODEL-02/GGUF-M2 is lowered as four serial slices (C1 silu+router → C2 expert dispatch/accumulation → C3 shared expert + full `ffn_moe` → C4 exempla receipt + docs + closeout); dispatch is gated on MODEL-01 (GGUF-M1) and the LIB-03 codec set. The unit preserves every mandatory successor through CLOSE-01 and advances umbrella milestone Q2 without completing the campaign.*
