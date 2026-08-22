# Delivery Lowering — GGUF-M2 (MODEL-02) Re-Lowered Against Live Main: MoE Router And Expert Execution

**Status**: lowered 2026-08-22 by planner (task `3a7910d9`, Mind) — READY,
**dispatchable now**. Supersedes the planner-26 lowering
(`pml5-gguf-m2-moe-router-delivery.md`) and the planner-35 micro-unit re-split
(`pml5-gguf-m2-moe-router-micro-units.md`): their frozen public surface used
the retracted Latin identifier dialect, their A1 `silu` unit has landed on
main, and their baseline counts are stale. Frozen semantics (artifact facts,
8-step MoE math, tie rule) are inherited unchanged — re-verified live
2026-08-22 (§3).
**Campaign**: [`radix/docs/factory/gpu-production-readiness/CAMPAIGN.md`](../../../../radix/docs/factory/gpu-production-readiness/CAMPAIGN.md) — row **MODEL-02** ("Implement MoE router and expert execution"; done oracle: router choices, expert weights, intermediate values, and outputs match the independent oracle).
**Delivery authority**: [`pml5-general-gguf-delivery.md`](pml5-general-gguf-delivery.md) §GGUF-M2.
**Repo**: `gradus`, main `fad0d57` (tree clean, verified 2026-08-22). Planning artifact only — no product code written by this lowering.

## 1. Interpreted theme

MODEL-02 is the MoE third of the `qwen35moe` semantics (MODEL-03 owns the
hybrid SSM/attention state in front of it; MODEL-04 composes both into the
full reference forward). Its component-level done oracle — router choices,
expert weights, intermediate values, layer outputs vs the independent oracle —
is also the named entry gate for the device-side MoE rows: exec02 `EXEC02-PM1`
(non-goal: "no real-artifact tier before the MODEL-02 oracle") and
`EXEC02-PM3` ("entry gate MODEL-02 oracle for the real-artifact tier"), which
feed device-executor **M8-U1** (`radix/docs/factory/device-executor/delivery-m5-m8.md`).
M8-U1's done_when additionally requires "the admitted MoE exempla" — delivered
here as `exempla/moe-probe` (M2-U7). This lowering therefore names its
real-artifact outputs as M8-U1 recheck handles (§8).

## 2. Normalized spec (delivery-sized outcome)

One public `gradus:model/moe` surface, carrier-tier, dense-pattern-shaped:

1. **Router** — logits `= x · ffn_gate_inp` (no bias; no router bias tensor
   exists), softmax over all `n_expert`, top-`n_expert_used` by probability,
   **deterministic tie rule: lowest expert index first**, weights renormalized
   by their sum (`norm_w=true`). Full logits + probability rows are returned
   (oracle surface).
2. **Routed experts** — per selected expert `e`: windowed rank-3 reads of
   `ffn_gate_exps` / `ffn_up_exps` / `ffn_down_exps` (never the whole rank-3
   tensor), SwiGLU `silu(gate)·up` then down, via landed `nn.swiglu`.
3. **Accumulation** — `moe_out = Σ_e weights[e]·out_e`.
4. **Shared expert** — `shexp = (silu(x·ffn_gate_shexp)·(x·ffn_up_shexp))·ffn_down_shexp`;
   gate `g = sigmoid(x·ffn_gate_inp_shexp)` (scalar per token);
   `ffn_out = moe_out + g·shexp` — the complete layer FFN output.
5. **Independent oracle** — pinned Python reference reading the real artifact
   read-only, dequantizing with the `gen_dequant_goldens.py` precedent
   (llama.cpp `ggml-quants.c` @ `a957b7747` semantics), computing the exact
   math in numpy f32 (f64 for the band floor), committed goldens.
6. **Executed proof** — `exempla/moe-probe` (app-owned adapter,
   `gguf-admit-qwen35moe` + `gguf-materialize` patterns): ADMIT receipt, then
   PASS lines per (layer, probe) golden on layers **0, 3, 39, 40** — covering
   both block classes, all four routed storage kinds (Q4_K gate/up; Q5_K/Q6_K
   down), the F32 and BF16 router rows, and the MTP block.

Component-level only: no token, logit, full-model, or device claim.
Full-model re-validation against the pinned llama.cpp comparator is
MODEL-04's boundary; native MoE kernels are EXEC-02/M8 territory.

### Frozen semantics (inherited; re-verified 2026-08-22)

Artifact identity: `Qwen3.6-35B-A3B-UD-Q4_K_M.gguf`, 22,663,387,424 bytes,
SHA-256 `0b21525e972670ed59e1812e170b27c26355381f0656ecc4e25617ece7dac58b`,
architecture `qwen35moe`. MoE facts (live in `Qwen35moeConfig`):
`expert_count=256`, `expert_used_count=8`, `expert_ffn_length=512`,
`shared_ffn_length=512`, `embedding_length=2048`; `expert_weights_scale`
absent (scale step skipped). Semantic pin: llama.cpp
`/Users/ianzepp/work/ianzepp/llama.cpp` @ `a957b7747` —
`src/models/qwen35moe.cpp` `build_moe_ffn(cur, ffn_gate_inp, ffn_up_exps,
ffn_gate_exps, ffn_down_exps, nullptr, n_expert, n_expert_used, LLM_FFN_SILU,
true /*norm_w*/, expert_weights_scale, SOFTMAX, …)` + sigmoid
`ffn_gate_inp_shexp` gate, verified at this lowering. Tie honesty (inherited):
llama.cpp's argsort is not stable on exact ties; Gradus and the pinned Python
reference share OUR lowest-index-first rule; a real-tie divergence at the
MODEL-04 full-model boundary is recorded, never silently matched.

### Layout contract (frozen — replaces the stale Latin surface)

GGUF `ne[0]` is the contiguous dimension. Windows arrive **in GGUF storage
order**; the adapter declares carrier shapes `[ne[1], ne[0]]` per expert slice
(zero-copy shape over the flat materialized window):

| Tensor | GGUF shape | Expert-`e` window | Carrier shape | Use |
| --- | --- | --- | --- | --- |
| `blk.N.ffn_gate_inp.weight` | `[2048, 256]` | whole (F32/BF16) | `[256, 2048]` | `logits = matmul(W, x_col)` → `[256]` |
| `blk.N.ffn_gate_inp_shexp.weight` | `[2048]` | whole | `[2048]` | gate dot product |
| `blk.N.ffn_gate_exps.weight` | `[2048, 512, 256]` | `e·(2048·512) … +2048·512` | `[512, 2048]` | `gate_e = matmul(W_e, x_col)` |
| `blk.N.ffn_up_exps.weight` | `[2048, 512, 256]` | same offsets | `[512, 2048]` | `up_e = matmul(W_e, x_col)` |
| `blk.N.ffn_down_exps.weight` | `[512, 2048, 256]` | `e·(512·2048) … +512·2048` | `[2048, 512]` | `out_e = matmul(W_e, h_col)` |
| `blk.N.ffn_gate_shexp.weight` | `[2048, 512]` | whole | `[512, 2048]` | shared gate proj |
| `blk.N.ffn_up_shexp.weight` | `[2048, 512]` | whole | `[512, 2048]` | shared up proj |
| `blk.N.ffn_down_shexp.weight` | `[512, 2048]` | whole | `[2048, 512]` | shared down proj |

All expert projections compute as **GEMV via `math.matmul(W_carrier, x_col)`**
over the storage-order carrier — no transpose helper needed (live `math` has
no public transpose; dense's `_transpose` stays dense-private). Canonical
names verified against `qwen35moe.canonical_tensors` (`_hybrid_tensors`,
`_full_attention_tensors`, `_nextn_tensors` — blk.40 carries the frozen BF16
rows on `ffn_gate_inp` / `ffn_gate_inp_shexp`). Storage kinds per layer
verified in the same map: down Q5_K everywhere except blk.34/38/39 (Q6_K).

### Frozen public surface (`gradus:model/moe` — live dialect)

```text
import from "gradus:math" math
import from "gradus:nn" nn
import from "gradus:tensor" tensor

@ public { }
class MoeConfig {
    int expert_count          # 256 — from MODEL-01 admission, never re-derived
    int expert_used_count     # 8
    int expert_ffn_length     # 512
    int shared_ffn_length     # 512
    int embedding_length      # 2048
}

@ public { }
union MoeError {
    BadConfig { string message }
    BadShape { string message }
    BadWindow { string message }
    NonFinite { string message }
}
@ public { } fn message(MoeError e) → string

@ public { }
class MoeSelection {
    list<int> indices        # top-used expert indices, descending probability;
                             # exact ties → lowest index first
    list<f32> weights        # renormalized (norm_w), same order; sum ≈ 1
    list<f32> logits         # full [expert_count] router logits (oracle surface)
    list<f32> probabilities  # full [expert_count] softmax (oracle surface)
}

# Windowed source (dense-source-callback precedent): the adapter owns
# TensorView binding + payload reads; returns the storage-order carrier shaped
# per §Layout contract. (name, element_start, element_length) → carrier.
# moe.fab constructs canonical names "blk.<layer>.ffn_*" itself (dense.fab
# precedent) and validates every returned shape against MoeConfig (fail-closed
# BadShape/BadWindow; NonFinite rejects NaN/±Inf probes and intermediates).

@ public { }
fn route(tensor.Tensor x, int layer,
    (string, int, int) → tensor.Tensor ⇥ MoeError source, MoeConfig cfg)
    → MoeSelection ⇥ MoeError

@ public { }
fn expert_out(tensor.Tensor x, int layer, int expert_index,
    (string, int, int) → tensor.Tensor ⇥ MoeError source, MoeConfig cfg)
    → tensor.Tensor ⇥ MoeError        # [2048] one routed expert's output

@ public { }
fn ffn_moe(tensor.Tensor x, int layer,
    (string, int, int) → tensor.Tensor ⇥ MoeError source, MoeConfig cfg)
    → tensor.Tensor ⇥ MoeError        # [2048] complete layer FFN output
```

`x` is a `[1, 2048]` carrier (single pinned hidden-state probe).
`MoeConfig` is built by the caller from the admitted `Qwen35moeConfig`
fields — `moe.fab` does **not** import `gradus:model/qwen35moe` (the module
stays architecture-generic; the exemplar maps admitted config → `MoeConfig`).
Module-private `_sigmoid` / `_softmax` / `_exp` follow the `nn._exp`
self-hosted precedent; **no public `nn.fab` addition** (silu/swiglu already
landed; a public sigmoid waits for a second caller — smallest correct code).
Any spelling change routes through the delivery-amendment path.

## 3. Repo-aware baseline (verified live 2026-08-22, gradus main `fad0d57`)

| Surface | Live state | Unit |
| --- | --- | --- |
| `src/model/moe.fab` / `.proba` | **Do not exist** — module entirely new | M2-U3…U6 |
| MODEL-01 chain | **MERGED** (`7004ed8`, M1–M9 + accessor api-reference); `qwen35moe.fab` live: `Qwen35moeConfig`, `freeze`, `canonical_tensors` (753-tensor map incl. MoE names/shapes/kinds + blk.40 BF16 anomaly), `admit(corpus, digest, length)` | read-only |
| LIB-03 codecs/view | **Landed**: `tensor_view.fab` (`links`, `materialize_slice`, `materialize_block`), `tensor_payload.fab`; `dequant.fab` kinds F32/F16/BF16/Q5_0/Q8_0/Q4_K/Q5_K/Q6_K — the full MoE union set | consumed |
| REF-01 dense chain | **Landed**: `dense.fab` source-callback pattern, `transformer.fab` blocks; `nn.fab` public `silu` (:623) + `swiglu` (:645) + `rmsnorm`; `math.fab` `matmul`/`mul`/`add_carrier`/`slice` | consumed; **old unit A1 (silu) OBSOLETE** — orphan need `b1f97eb8` resolved by consumption |
| `fixtures/gguf/` | `gen_dequant_goldens.py` + `gguf-dequant-goldens.json` + `gguf-dequant-goldens-oracle.md` (oracle precedent), `qwen35moe-admission-oracle.md`, manifest fixtures; **no `gen_moe_*`** | M2-U1, M2-U2 |
| `exempla/gguf-admit-qwen35moe/`, `exempla/gguf-materialize/` | Live app-owned adapter patterns (identity pin, bounded reads, PASS receipts; `faber.toml` target `fmir`) | M2-U7 (patterns) |
| `exempla/moe-probe/` | **Does not exist** | M2-U7 |
| `scripta/check-compile` | Bash exemplum blocks per dir (`gguf-materialize`, `gguf-admit-qwen35moe`, …); no moe block | M2-U7 (register) |
| Docs | `docs/regression-corpus.md` **v1.9.0**; `docs/module-map.md`, `docs/api-reference.md`, `docs/diagnostics.md` have no MoE rows; `scripta/inventory-public-symbols` coverage gate live | M2-U8 |
| Pinned oracle source | `/Users/ianzepp/work/ianzepp/llama.cpp` @ `a957b7747` — `src/models/qwen35moe.cpp` + `src/llama-graph.cpp` present; MoE call shape verified §2 | M2-U2 (read-only) |
| Real artifact | `/Users/ianzepp/ai/models/Qwen3.6-35B-A3B-UD-Q4_K_M.gguf` (operator evidence; never committed; adapter-owned path) | M2-U2 (read-only), M2-U7 |
| Sibling MODEL-03 | No SSM module exists yet; lowered (`model-03-ssm-attention-state-delivery.md`) | parallel-safe (disjoint new file; no shared `nn.fab` writes — §2 surface avoids them) |

## 4. Hand unit graph (8 units + aggregate gate)

```text
MODEL-01 merged (done) — dispatchable now
  ├─ M2-U1  probe vectors + synthetic fixtures      [∥ M2-U3]
  │    └─ M2-U2  oracle generator + committed goldens [after U1; ∥ M2-U4]
  ├─ M2-U3  moe.fab type surface + fail-closed contract [∥ U1]
  │    └─ M2-U4  route() — logits/softmax/top-k/tie/renorm [after U3 + U1]
  │         └─ M2-U5  expert_out() — windowed rank-3 SwiGLU [after U4 + U2]
  │              └─ M2-U6  ffn_moe() — accumulation + gated shared expert [after U5]
  │                   ├─ M2-U7  exemplar adapter + ADMIT receipt + real-file proof + check-compile reg [∥ U8]
  │                   └─ M2-U8  API/support docs + inventory re-baseline + status lines [∥ U7]
  └─ M2-G1  aggregate validation + atomic merge     [after U7 + U8]
```

Peak live Hands: 2 (U1∥U3; U2∥U4; U7∥U8). All write surfaces file-disjoint
within a wave; the B-chain (U3–U6) serializes on the one new module file.
Every unit is gradus-only. Est total 24–36k work tokens.

### M2-U1 — Probe vectors + synthetic fixtures

| Field | Value |
| --- | --- |
| `id` | `MODEL-02-U1` |
| `outcome` | Deterministic probe corpus: `fixtures/gguf/gen_moe_probes.py` emits `gguf-moe-probes.json` — two seeded `[2048]` f32 probes per selected layer (0, 3, 39, 40) at realistic post-norm magnitudes (seed + generation documented) — plus one hand-built synthetic exact-tie router config (8 experts, 2 used, crafted tie at the selection boundary) and one small synthetic multi-expert config for dispatch probas (no artifact dependency). |
| `write_scope` | `fixtures/gguf/gen_moe_probes.py`, `fixtures/gguf/gguf-moe-probes.json`, `fixtures/gguf/gguf-moe-synthetic.json` (create) |
| `done_when` | generator runs deterministic (two runs byte-identical); JSON committed with documented schema header (`gguf-moe-probes-v1`); tie fixture encodes the exact-tie boundary case |
| `depends_on` | none |
| `sanity` | rerun generator; diff output against committed JSON |
| `non_goals` | no goldens (U2); no Faber code; no real-artifact reads beyond none (probes are synthetic) |
| `risk` | low |
| `integrable` | yes (inert fixture data) |
| `first failing oracle` | n/a (fixture unit; red lives with the consumer) |
| `closeout command` | `cd gradus && python3 fixtures/gguf/gen_moe_probes.py --check` (determinism flag the generator defines) |
| `expected observed result` | `OK deterministic: 3 fixture sets` (or equivalent single PASS line the generator prints); exit 0 |
| `est_work_tokens` | 2–3k (fixture authoring; gen_dequant_goldens.py precedent bounds it) |
| `stop condition` | if seeded probe magnitudes cannot be documented against the RMSNorm unit-scale property, record and escalate rather than guessing |

### M2-U2 — Independent oracle: goldens generator + committed goldens

| Field | Value |
| --- | --- |
| `id` | `MODEL-02-U2` |
| `outcome` | The independent oracle: `fixtures/gguf/gen_moe_goldens.py` (gen_dequant_goldens.py precedent) — (a) reads the real artifact read-only and verifies the pinned identity (digest + length); (b) dequantizes the router/expert/shared-expert tensors with the llama.cpp `ggml-quants.c` @ `a957b7747` semantics (F32/BF16/Q4_K/Q5_K/Q6_K/Q8_0); (c) computes the exact §2 math in numpy f32 for every (layer, probe), plus a strict-f64 pass for the band floor; commits `gguf-moe-goldens.json` (schema `gguf-moe-goldens-v1`: per (layer, probe) — full logits `[256]`, probabilities `[256]`, top-8 indices, 8 renormalized weights, per-selected-expert intermediates `h_e [512]` + outputs `[2048]`, shared-expert output `[2048]`, gated shared output `[2048]`, final FFN output `[2048]`) and `gguf-moe-goldens-oracle.md` (commands, Δ derivation: `Δ = 10·R` where `R = max |f32_ref − f64_ref|`, capped at the gradus forward band `5e-4`, matmul family floor `1e-5` per numeric-policy v1.0.0; first-divergence discipline). |
| `write_scope` | `fixtures/gguf/gen_moe_goldens.py`, `fixtures/gguf/gguf-moe-goldens.json`, `fixtures/gguf/gguf-moe-goldens-oracle.md` (create) |
| `done_when` | goldens exist for all 4 layers × 2 probes + the synthetic tie config (tie indices `[2,5]` recorded); every golden row finite; Δ derived and recorded; oracle.md names the exact artifact identity, llama.cpp pin, and commands |
| `depends_on` | `MODEL-02-U1` |
| `sanity` | rerun generator; goldens byte-stable; f64 pass max deviation recorded |
| `non_goals` | no Faber code; no gradus import; no artifact copy/redistribution (path stays operator-local) |
| `risk` | medium — dequant/layout correctness is the oracle's whole value; mitigated: gen_dequant_goldens.py precedent + the already-landed dequant goldens cross-check the same codecs |
| `integrable` | yes (inert fixture data) |
| `first failing oracle` | n/a (this unit IS the oracle; its self-check is the f64 band row) |
| `closeout command` | `cd gradus && python3 fixtures/gguf/gen_moe_goldens.py --check` |
| `expected observed result` | `OK goldens: 8 real-artifact rows + 1 synthetic row; Δ=<value>; first-divergence none` ; exit 0 |
| `est_work_tokens` | 4–6k (dequant + MoE math + layout contract implementation) |
| `stop condition` | if any layer's live storage kind falls outside {F32, BF16, Q4_K, Q5_K, Q6_K, Q8_0}, record the exact tensor and escalate (campaign stop condition — no silent widening) |

### M2-U3 — `moe.fab` type surface + fail-closed contract

| Field | Value |
| --- | --- |
| `id` | `MODEL-02-U3` |
| `outcome` | New module `src/model/moe.fab` + `src/model/moe.proba`: the frozen §2 surface types — `MoeConfig`, `MoeError` (BadConfig/BadShape/BadWindow/NonFinite) + `message`, `MoeSelection`, the three public function signatures with `require`-guard contracts — and the negative matrix in proba (bad config rows, malformed carrier shapes, wrong window lengths, NaN/Inf probe → typed `MoeError`, never a silent default). Carries the first failing oracle of the chain. |
| `write_scope` | `src/model/moe.fab`, `src/model/moe.proba` (create) |
| `done_when` | module compiles; negative matrix proba rows green; function bodies may `throw` unimplemented for the math rows but every guard/contract is live |
| `depends_on` | none (parallel-safe with U1) |
| `sanity` | `./scripta/check-source` + narrow proba run on `moe.proba` |
| `non_goals` | no router math (U4); no fixtures; no docs |
| `risk` | low |
| `integrable` | yes (new module, green proba, no callers) |
| `first failing oracle` | `case router-topk-tie-probe: route(tie_probe, …, MoeConfig{expert_count=8, expert_used_count=2, …})` must return indices `[2,5]` — at U3 boundary the math row throws unimplemented (RED); proba row committed failing, flipped by U4 |
| `closeout command` | `cd gradus && ./scripta/check-source && <faber> proba src/model/moe.proba` (narrow; lane binary per dispatch packet) |
| `expected observed result` | check-source exit 0; negative-matrix rows PASS; the tie-probe row recorded RED (unimplemented) — red-green discipline |
| `est_work_tokens` | 2–3k |
| `stop condition` | if the frozen surface signatures cannot typecheck against the live `math`/`nn`/`tensor` kits, record the exact mismatch and escalate (no ad-hoc surface invention) |

### M2-U4 — `route()` — logits, softmax, deterministic top-k, renormalization

| Field | Value |
| --- | --- |
| `id` | `MODEL-02-U4` |
| `outcome` | `route()` implemented per §2.1–2.2: router window `[256, 2048]` via source, GEMV logits, f32 softmax (max-subtracted, module-private `_exp`/`_softmax` per nn precedent), top-8 by probability with lowest-index-first tie rule, `norm_w` renormalization (`weights /= max(sum, 6.103515625e-5)`). Proba: synthetic tie fixture → `[2,5]` exact; synthetic fixtures with known orderings; logits/probabilities rows checked against hand-computed small cases. |
| `write_scope` | `src/model/moe.fab`, `src/model/moe.proba` |
| `done_when` | tie-probe row flipped GREEN (`[2,5]`); index rows exact-integer; weight renormalization sum ≈ 1 within f32; all U3 negatives stay green |
| `depends_on` | `MODEL-02-U3`, `MODEL-02-U1` |
| `sanity` | narrow proba run on `moe.proba` |
| `non_goals` | no expert dispatch (U5); no real-artifact reads |
| `risk` | low-medium (tie rule is the audit magnet; smallest-proof proba pins it) |
| `integrable` | yes |
| `first failing oracle` | the U3-committed tie row (now flipping green) + a new red row: descending-probability ordering case (committed failing, then green) |
| `closeout command` | narrow proba run on `moe.proba` |
| `expected observed result` | all router rows PASS incl. `indices=[2,5]`; exit 0 |
| `est_work_tokens` | 3–5k |
| `stop condition` | any tie-order ambiguity in the synthetic fixture itself (near-tie f32 rounding) → tighten the fixture, never widen the comparison |

### M2-U5 — `expert_out()` — windowed rank-3 SwiGLU dispatch

| Field | Value |
| --- | --- |
| `id` | `MODEL-02-U5` |
| `outcome` | `expert_out()` implemented per §2.3: expert-`e` windows at the frozen offsets (§Layout contract), carrier shapes `[512,2048]`/`[2048,512]`, GEMV projections via `math.matmul`, `nn.swiglu` with the dense `_no_bias` precedent, shape validation fail-closed. Proba over the synthetic multi-expert fixture (hand-computed windows; includes a Q4_K/Q5_K-shaped window exercise through synthetic data — no artifact in proba). |
| `write_scope` | `src/model/moe.fab`, `src/model/moe.proba` |
| `done_when` | per-expert output rows match the synthetic fixture exactly (first-divergence rule on any mismatch); window-offset and carrier-shape negatives green (wrong window length / wrong shape → typed `MoeError`) |
| `depends_on` | `MODEL-02-U4`, `MODEL-02-U2` (golden layout cross-check reference for the offset arithmetic) |
| `sanity` | narrow proba run on `moe.proba` |
| `non_goals` | no accumulation/shared expert (U6); no real-artifact reads in proba |
| `risk` | medium — offset/layout arithmetic is the divergence-prone surface; mitigated: frozen §Layout table + U2 goldens as the independent cross-check |
| `integrable` | yes |
| `first failing oracle` | expert-0 window case on the synthetic fixture committed RED before the offset code lands |
| `closeout command` | narrow proba run on `moe.proba` |
| `expected observed result` | dispatch rows PASS; window negatives PASS; exit 0 |
| `est_work_tokens` | 3–5k |
| `stop condition` | if live `tensor_view`/`materialize_slice` cannot express an expert window at the frozen offsets (it can at this baseline — `materialize_slice(v, element_start, element_length, source)`), record and escalate before changing the layout contract |

### M2-U6 — `ffn_moe()` — accumulation + gated shared expert

| Field | Value |
| --- | --- |
| `id` | `MODEL-02-U6` |
| `outcome` | `ffn_moe()` implemented per §2.4–2.5: `route()` → per-expert `expert_out()` → weighted accumulation (`math.mul`/`math.add_carrier`), shared-expert SwiGLU + module-private sigmoid gate, final sum `[2048]`. Proba: synthetic end-to-end case (hand-computed full-layer output on the small fixture); NonFinite intermediate gate. |
| `write_scope` | `src/model/moe.fab`, `src/model/moe.proba` |
| `done_when` | synthetic full-layer output matches hand-computed golden; accumulation order documented (ascending expert index — deterministic); the §2 surface is now complete and frozen |
| `depends_on` | `MODEL-02-U5` |
| `sanity` | narrow proba run on `moe.proba` |
| `non_goals` | no exemplar (U7); no docs (U8) |
| `risk` | low-medium (composition of proven pieces) |
| `integrable` | yes |
| `first failing oracle` | synthetic full-layer row committed RED before composition lands |
| `closeout command` | narrow proba run on `moe.proba` |
| `expected observed result` | full-layer row PASS; all prior rows PASS; exit 0 |
| `est_work_tokens` | 3–5k |
| `stop condition` | if accumulation order affects f32 reproducibility across runs, pin the order in the module comment and proba — never leave it unspecified |

### M2-U7 — Exemplar adapter + ADMIT receipt + real-file executed proof

| Field | Value |
| --- | --- |
| `id` | `MODEL-02-U7` |
| `outcome` | `exempla/moe-probe/` (faber.toml target `fmir`, `src/main.fab`, README receipt): app-owned adapter (gguf-admit-qwen35moe + gguf-materialize patterns) — resolves operator path from argv, pins identity (digest + length), runs `qwen35moe.admit` (ADMIT receipt line), maps admitted config → `MoeConfig`, binds TensorViews per canonical name, serves the windowed source callback, executes `route`/`ffn_moe` on layers 0/3/39/40 × 2 probes, compares against committed goldens (indices exact; values under Δ with first-divergence record), prints one PASS line per (layer, probe). Registers the exemplum block in `scripta/check-compile`. This is the **admitted MoE exempla** M8-U1's done_when cites. |
| `write_scope` | `exempla/moe-probe/faber.toml`, `exempla/moe-probe/src/main.fab`, `exempla/moe-probe/README.md`, `scripta/check-compile` (new exemplum block) |
| `done_when` | `check-compile` includes the block and passes; real-file run prints 8 PASS lines (4 layers × 2 probes) + ADMIT line, zero FAIL, first-divergence `none`; receipt records command, revisions, artifact identity, probe hashes, Δ, observed indices/weights |
| `depends_on` | `MODEL-02-U6`, `MODEL-02-U2` |
| `sanity` | `./scripta/check-source`; one real-file run on burgus |
| `non_goals` | no module edits; no GPU/device claim; no artifact commit |
| `risk` | medium (first real-artifact MoE execution; adapter I/O surface) |
| `integrable` | yes |
| `first failing oracle` | layer-0 probe-1 golden comparison committed RED in the exemplar before the adapter wiring completes |
| `closeout command` | `cd gradus && ./scripta/check-source && ./scripta/check-compile && env FABER_LIBRARY_HOME=<root> FABER_BIN=<faber> <faber> run --target fmir exempla/moe-probe -- /Users/ianzepp/ai/models/Qwen3.6-35B-A3B-UD-Q4_K_M.gguf <data-offset> 0b21525e972670ed59e1812e170b27c26355381f0656ecc4e25617ece7dac58b` |
| `expected observed result` | `ADMIT qwen35moe` + `PASS layer=0 probe=p1 indices=[…] weights=[…] first-divergence=none max-dev=<≤Δ>` × 8; exit 0 |
| `est_work_tokens` | 4–6k |
| `stop condition` | any golden mismatch is a divergence receipt naming the first divergent element (index + value pair), routed to the owning unit (U4/U5/U6 math vs U2 oracle) — never a tolerance-widened pass |

### M2-U8 — API/support docs + inventory re-baseline + status lines

| Field | Value |
| --- | --- |
| `id` | `MODEL-02-U8` |
| `outcome` | Docs catch the surface: `docs/module-map.md` (`gradus:model/moe` row + counts), `docs/api-reference.md` (new section; run `scripta/inventory-public-symbols` per its coverage gate), `docs/diagnostics.md` (`MoeError` table), `docs/regression-corpus.md` (bump from the version live at the boundary — v1.9.0 today — with the moe proba suites + goldens rows), `docs/factory/production-ml-library/pml0-symbol-inventory.md` + `pml0-support-matrix.md` (MoE router/expert row at the **output-checked component tier** — never executed-token/model identity), `pml5-general-gguf-delivery.md` GGUF-M2 implemented line + gradus `CAMPAIGN.md` status line, and supersession status notes on the two superseded M2 lowering docs. |
| `write_scope` | the named docs only (read-only: everything under `src/`) |
| `done_when` | inventory-public-symbols coverage gate green; support-matrix row classified component tier; status lines name the landed revisions |
| `depends_on` | `MODEL-02-U6` (surface final); lands with/after U7's revisions are known |
| `sanity` | `./scripta/check-source` (doc-touching gates) + inventory script |
| `non_goals` | no campaign-semantics edits; no support-matrix tier upgrade |
| `risk` | low |
| `integrable` | yes |
| `first failing oracle` | n/a (docs unit; the inventory coverage gate is the red) |
| `closeout command` | `cd gradus && ./scripta/inventory-public-symbols && ./scripta/check-source` |
| `expected observed result` | coverage gate exit 0 with the new symbols counted; check-source exit 0 |
| `est_work_tokens` | 2–3k |
| `stop condition` | if the support-matrix schema lacks the component tier row shape, follow the existing dequant-row precedent; do not invent a new tier |

## 5. Integration / merge gate

### M2-G1 — Aggregate validation + atomic merge

| Field | Value |
| --- | --- |
| `id` | `MODEL-02-G1` |
| `outcome` | Lane-owned aggregate: full `./scripta/check-source` + `./scripta/check-compile`, the complete `moe.proba` sweep, the real-file exemplar run, then atomic merge of the chain onto main (MODEL-01 G1 precedent); closeout receipt names revisions, commands, observed PASS lines, Δ, and first-divergence `none`. Advances the factory status lines. |
| `write_scope` | merge commit(s) + closeout receipt under `docs/factory/production-ml-library/evidence/` (or the convention Mind's lane uses) |
| `done_when` | all child proofs re-executed green in one aggregate run; MoE surface lands as one authority on main; campaign + delivery status lines advanced |
| `depends_on` | `MODEL-02-U7`, `MODEL-02-U8` |
| `non_goals` | no new product code; no tier upgrade; no full-model claim |
| `risk` | low (verification + merge) |
| `integrable` | yes (it is the merge) |

Children are individually integrable (each state compiles with green proba and
no external callers — no dual-authority risk on a brand-new module); G1 still
owns the aggregate proof and the single landing of the chain, per the
MODEL-01 precedent. Mind may impose lane-serial landing if it chooses.

## 6. Lane-owned validation (named once)

- **Lint stages 1–2** (`scripta/test` stages / check-source family): lint lane
  after merge, or direct per the workspace ladder — not on child Hands.
- **Broad proba / stage 3–4**: test lane after merge. Children run only their
  narrow `moe.proba` + one exemplar run (U7) as sanity.
- **Full-model boundary**: MODEL-04 re-validates router choices end-to-end
  against the pinned llama.cpp comparator; a divergence routes back here with
  the first-divergence record.

## 7. Successor preservation

`M1 → M2 ‖ M3; M2 + M3 → M4 → EXEC-01/02 → EXEC-03 → CAP-01/02 → CLOSE-01`
preserved intact. MODEL-04's M1 consumes `ffn_moe` per layer (carrier-tier,
dense-source-callback composition — the frozen surface was shaped for this).
Nothing is narrowed, deferred, or made optional.

## 8. M8-U1 recheck handles (task-body gate)

M8-U1 (`radix/docs/factory/device-executor/delivery-m5-m8.md`) and the exec02
MoE rows (`EXEC02-PM1` "no real-artifact tier before the MODEL-02 oracle",
`EXEC02-PM3` "entry gate MODEL-02 oracle for the real-artifact tier") consume,
after `MODEL-02-G1`:

1. `fixtures/gguf/gguf-moe-goldens.json` — per-(layer, probe) router indices,
   renormalized weights, per-expert intermediates/outputs, final FFN outputs —
   the independent oracle for real-artifact MoE kernel probes (M2-U2);
2. `exempla/moe-probe` — the admitted MoE exempla M8-U1's done_when (c)
   family receipt cites (M2-U7).

## 9. Open questions for Mind (none blocks dispatch)

1. **Lane vs direct dispatch** — the chain is gradus-only and main is clean;
   direct-on-main per the workspace default works, or a lane if Mind wants the
   MODEL-01-style packet. The spec is written lane-agnostic (closeout commands
   take `<faber>`/`<root>` placeholders).
2. **supersession notes** — this lowering adds one-line SUPERSEDED status
   notes to `pml5-gguf-m2-moe-router-delivery.md` and
   `pml5-gguf-m2-moe-router-micro-units.md`; their frozen semantics are
   inherited here, their surface spellings are retracted.
3. **MODEL-03 parallelism** — if Mind dispatches MODEL-03 concurrently, both
   chains are disjoint new files under `src/model/` with no shared `nn.fab`
   writes (this surface deliberately adds none); merge ordering is free.
