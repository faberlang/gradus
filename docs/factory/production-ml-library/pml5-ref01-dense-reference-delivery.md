# Delivery Lowering: REF-01 — Mandatory Dense Reference Rungs

**Status**: planned — implementation-ready delivery lowering, awaiting LIB-02/LIB-03 receipts
**Planner**: planner-24 (fresh lowering, derived independently from campaign, delivery authority, and live repos)
**Assignment**: task `aba59bcc` (Mind → planner-24, original lowering); re-split task `7e24b99e` (Mind → planner-24, 2026-08-14)
**Granularity directive**: operator 2026-08-14 — every unit is **one behavior family**, executable by a Hand in roughly 10–15 minutes (focused check + commit + close), carrying all 8 campaign-rule-2 fields (outcome, exact write scope, first failing oracle, closeout command, expected observed result, est_basis, stop condition, depends_on). A unit that would take an hour is unacceptable — split further.
**Campaign**: [`radix/docs/factory/gpu-production-readiness/CAMPAIGN.md`](../../../../radix/docs/factory/gpu-production-readiness/CAMPAIGN.md) — REF-01
**Semantic delivery authority**:
[`pml5-general-gguf-delivery.md`](pml5-general-gguf-delivery.md) — GGUF-A4/A5/A6 (this lowering does not replace the authority; it makes the authority's dense-reference units Hand-executable)
**Repo**: `gradus` (REF-01 owner per campaign table)
**Integration stop**: `factory/merge` only
**Freshness**: no planner-1..19 worktree, commit, partial artifact, or cancelled transcript was read or reused. All facts below are grounded in the campaign, the delivery authority, the gi0–gi3 contract/evidence docs, and the live repo trees at the pinned baselines.

## 1. Interpreted Unit / Problem

The campaign's dense reference rungs (REF-01) require that Faber/Gradus execute **complete dense transformer models** — not the fixed-shape `*_2x2` / `*_4x4` / `*_2x8` proof rows — and produce full-model, oracle-matching logits, prefill/decode, deterministic text, and reset/reuse receipts, with no special-case constants. This is the substrate `qwen35moe` (MODEL-01..04) consumes: the reusable forward operations (RMSNorm, SwiGLU, configurable RoPE, MHA/GQA, embeddings, output projection, ordered layer stack) must exist as a shared, device-neutral Gradus surface before MoE/SSM work starts.

The problem in one sentence: **make Gradus execute the complete dense layer stack of real SmolLM2 and Qwen2.5 GGUF artifacts and prove it against the pinned llama.cpp oracle, without any per-row hard-coded constants.**

## 2. Normalized Spec

One coherent delivery-sized outcome:

> Gradus executes the complete dense forward graph (embedding → N stacked layers → final norm → output projection) for the local SmolLM2-360M and Qwen2.5-0.5B/1.5B GGUF rows through public `gradus:*` operations, with per-layer KV state, prefill/decode agreement, deterministic text, and reset/reuse, all matching the pinned llama.cpp comparator at the first-divergence boundary — and reuses the same shared primitives when `qwen35moe` work begins.

Grounded mapping to the delivery authority:

| Authority unit | Scope in this lowering | Campaign slot |
| --- | --- | --- |
| GGUF-A4 — Dense Llama/Qwen primitives and full model | Full SmolLM2 + Qwen2.5-0.5B prefill logit rows vs independent CPU oracle at first-divergence boundary; shared forward primitives | REF-01 |
| GGUF-A5 — Real prefill, decode, and KV state | Per-layer per-KV-head state; prefill and incremental decode agree; reset, context rejection, replay, session identity executed | REF-01 |
| GGUF-A6 — Multiple dense acceptance rows | All three dense files produce deterministic text receipts through the same public surface; 1.5B proves no special-case constants | REF-01 |

**Authority-to-micro-unit mapping** (nothing narrowed; every A4/A5/A6 clause maps to at least one micro-unit in §4):

| Authority clause | Micro-units |
| --- | --- |
| RMSNorm | U1.1 |
| SiLU/SwiGLU | U1.2 |
| Configurable RoPE | U1.3 |
| Multi-head attention, GQA | U1.4 |
| Ordered layer stack / block | U1.5 (block), U1.8 (stack) |
| Explicit architecture adapters + canonical tensor names | U1.6 (`llama`), U1.7 (`qwen2`) |
| Tied/untied embeddings, final norm, output projection | U1.8 |
| Full-model prefill logits vs oracle (both rows) | U1.9 (SmolLM2), U1.10 (Qwen2.5-0.5B) |
| Per-layer per-KV-head state | U2.1 |
| KV state integrated into attention | U2.2 |
| Prefill and incremental decode agree | U2.3, U2.4 (mechanics), U2.5, U2.6 (executed) |
| Reset, context rejection, cancellation, replay, session identity executed | U2.4 (wired), U2.5, U2.6 (executed receipts) |
| Three dense rows pass the full chain + deterministic text | U3.1, U3.2, U3.3 |
| 1.5B no special-case constants | U3.3 |
| Unsupported families keep exact typed diagnostics | U1.6, U1.7 (admission), U3.1 (acceptance row) |

## 3. Repo-Aware Baseline

Pinned baselines (verified in this worktree):

| Repo | Baseline | Verified |
| --- | --- | --- |
| radix | `b6d6e17c8ad7` | worktree HEAD |
| gradus | `bc500993c97b` | worktree HEAD |
| hosts | `57d659d60430` | worktree HEAD |
| faber (public) | `1fb6cc97e66d` | worktree HEAD |

Current gradus dense surface (live tree, this worktree):

- `src/nn.fab` — `linear_2x2/4x4/2x8`, `gelu_2x8/4x4`, `layernorm_2x8` (fixed-shape rows only; no generic RMSNorm/SiLU/SwiGLU) plus the PML3 staged-carrier `linear`/`gelu`/`layernorm` production rows.
- `src/attention.fab` — `scaled_dot_product_staticum`, `scaled_dot_product(_causal)`, `rotary_position_embedding` over staged carriers; no GQA, no per-head KV, no configurable RoPE theta/pair policy.
- `src/transformer.fab` — `bert_tiny_block_2x8` and `transformer_block` (PML3 fixed-shape rows).
- `src/decode.fab` — `construct_weights`, `construct_decoder`, `decodere_datum`, `prefill`, `fresh_session/advance/reset`, `cancellation_*`, `replica` (fixed one-block forward row, PML5).
- `src/cache.fab` — `empty_cache`, `append`, `reset`, identity serialization (logical KV values, `layers = 1`; no per-layer per-head execution).
- `src/model/` — `artifact`, `gguf_manifest` (GGUF-A1a/A1b), `capsule`, `gguf`, `safetensors`, `dequant` (PML2 rows).
- `src/tokenizer.fab` — tokenizer **identity** contract (PML2-U4); tokenizer **runtime** (encode/decode text) is GGUF-A2 = LIB-02.

None of these execute a complete dense SmolLM2/Qwen2.5 forward stack. REF-01 is therefore genuinely from-scratch for full-model semantics; it reuses the GGUF-A1b manifest surface (descriptor/range facts) and will consume the GGUF-A2/A3 payload surfaces when those land.

## 4. Ordered Micro-Unit Graph

Predecessor receipts required before any REF-01 unit starts (Gate 0):

- **LIB-02 (GGUF-A2) accepted** — artifact-backed tokenizer runtime (encode/decode, special-token policy, chat-template behavior) matching pinned llama.cpp ids/text for the two Unicode probes on the three dense rows and the target artifact.
- **LIB-03 (GGUF-A3) accepted** — checked packed storage and reference materialization; every tensor required by the forward graph has a validated range, shape, layout, and bounded materialization path.

The campaign already sequences these: `TRUTH-01 → LIB-01 → LIB-02 + LIB-03 → REF-01`. This lowering does not reorder, narrow, or move them.

### Shared unit boundaries (all 19 micro-units)

- `read_scope`: `gradus/src/model/gguf_manifest.fab`, `gradus/src/model/dequant.fab`, `gradus/src/tokenizer.fab`, the four local GGUF files under `/Users/ianzepp/ai/models/` (read-only), gi0–gi3 contract docs in `radix/docs/factory/gpu-inference-gguf/` (read-only), and each unit's dependency receipts.
- `forbidden_scope`: `src/model/capsule.fab`/`gguf.fab`/`safetensors.fab` (LIB-01 clean-break territory), tokenizer runtime internals (LIB-02), packed storage/materialization internals (LIB-03), MoE/SSM (MODEL-01..04), radix/hosts/faber product code, native GPU work (GGUF-A7/M5), any path in another worktree or on main.
- **Stop conditions (shared, §6)**: pause the edge and route a correction when the target identity mismatches, a required architecture fact cannot be represented, the oracle is missing or unpinned for a row, a public Gradus API would acquire device ownership, or execution would require unapproved paid infrastructure. First-divergence receipts follow campaign rule 5; only the affected edge blocks (rule 6).
- **Executed proof (shared)**: each unit adds one executed proof — a focused exempla package under `exempla/dense-*` running through package MIR (the GGUF-A1a 31-PASS/0-FAIL precedent), plus the co-located proba pins (compile-level, the A1a precedent). Proba execution via `faber test` remains provider-blocked; the exempla run is the executed proof. No unit claims Metal/CUDA execution or full-model payload residency.

### Wave U1 — GGUF-A4: dense Llama/Qwen primitives and full model (10 micro-units)

#### REF-01-U1.1 — Generic RMSNorm (feeds Gate 1)

| Field | Value |
| --- | --- |
| `outcome` | Generic RMSNorm forward row over the staged f32 carrier in `gradus:nn`: `x / sqrt(mean(x²) + ε) · γ` over the LAST axis, no centering (the llama-arch norm family), typed errors. Executed proof: the RMSNorm exempla prints PASS for every pinned value. |
| `write_scope` | `src/nn.fab`, `src/nn.proba`, `exempla/dense-rmsnorm/` (`faber.toml`, `src/main.fab`, `README.md`), `docs/module-map.md`, `docs/api-reference.md`, `docs/diagnostics.md`, `docs/regression-corpus.md`, `docs/factory/production-ml-library/pml0-support-matrix.md`, README as needed |
| `first_failing_oracle` | Red proof (A1a precedent): the RMSNorm proba pins independent f64 reference values (external evaluation of the documented formula, ε per llama-arch) before the row exists — recorded failing. Green: the same pins pass within the documented 5e-4 absolute tolerance (the PML3 norm precedent). |
| `closeout_command` | `./scripta/check-source; env FABER_LIBRARY_HOME=<lane home> FABER_BIN=<lane-local faber binary> ./scripta/check-compile; <faber> run --target fmir exempla/dense-rmsnorm; git diff --check -- src/nn.fab src/nn.proba exempla/dense-rmsnorm docs/module-map.md docs/api-reference.md docs/diagnostics.md docs/regression-corpus.md docs/factory/production-ml-library/pml0-support-matrix.md` |
| `expected_observed_result` | `check-source` and `check-compile` exit 0; the exempla prints PASS for every pinned RMSNorm value (0 FAIL, exit 0); `git diff --check` silent; regression-corpus inventory updated (suite `src/nn.proba` + exempla `dense-rmsnorm`, pin count). |
| `est_basis` | ≈2k–4k tokens (10–15 min): one behavior family is ~a quarter of the PML3-U1..U3 production-surface units (8k–24k per unit covering 3–4 primitive rows); RMSNorm proba-pin surface ≈4–6 pins. |
| `stop_condition` | Shared §6 conditions; a first failing pin is recorded (index + observed vs reference value) and routes the repair per campaign rule 5. |
| `depends_on` | None beyond Gate 0 (LIB-02 + LIB-03 receipts accepted). |

#### REF-01-U1.2 — SiLU + SwiGLU MLP (feeds Gate 1)

| Field | Value |
| --- | --- |
| `outcome` | SiLU activation (`x·sigmoid(x)`) and the SwiGLU gated-MLP row (`silu(gate(x)) ⊙ up(x) → down(x)`) over the staged f32 carrier in `gradus:nn`, typed errors, no fixed-shape constants. Executed proof: the SwiGLU exempla prints PASS for every pinned value. |
| `write_scope` | `src/nn.fab`, `src/nn.proba`, `exempla/dense-swiglu/` (`faber.toml`, `src/main.fab`, `README.md`), the five docs listed in U1.1, README as needed |
| `first_failing_oracle` | Red proof: proba pins independent f64 reference values of the SiLU identity and the gated-MLP composition — recorded failing. Green: same pins pass @5e-4. |
| `closeout_command` | Same shape as U1.1 with `exempla/dense-swiglu` and the same changed-path list. |
| `expected_observed_result` | Same as U1.1 for the SiLU/SwiGLU pins (0 FAIL, exit 0); docs inventory updated. |
| `est_basis` | ≈2k–4k tokens (10–15 min): same basis as U1.1; SiLU/SwiGLU pins ≈5–8. |
| `stop_condition` | Shared §6 conditions; first failing pin recorded and routed. |
| `depends_on` | None beyond Gate 0. |

#### REF-01-U1.3 — Configurable RoPE (feeds Gate 1)

| Field | Value |
| --- | --- |
| `outcome` | Configurable rotary position embedding in `gradus:attention`: frequency base (theta), scale, and pair policy — consecutive-pair (llama-arch NORM) vs interleaved-pair (qwen2) — over the staged f32 carrier; generalizes the current fixed `rotary_position_embedding` row; typed errors. Executed proof: the RoPE exempla prints PASS for both policies. |
| `write_scope` | `src/attention.fab`, `src/attention.proba`, `exempla/dense-rope/` (`faber.toml`, `src/main.fab`, `README.md`), the five docs listed in U1.1, README as needed |
| `first_failing_oracle` | Red proof: proba pins independent f64 rotation values for both pair policies at a pinned theta (the GI3 Rope recipe facts: llama-arch NORM consecutive-pair, freq_base 100000; qwen2 interleaved-pair, theta 1000000) — recorded failing. Green @5e-4 (the COS_1/SIN_1 precedent). |
| `closeout_command` | Same shape as U1.1 with `exempla/dense-rope` and `src/attention.fab src/attention.proba` in the changed-path list. |
| `expected_observed_result` | Same as U1.1; both pair-policy pin rows PASS. |
| `est_basis` | ≈2k–4k tokens (10–15 min): one attention behavior family; RoPE pin surface ≈6–10 across two policies. |
| `stop_condition` | Shared §6 conditions; first failing pin recorded and routed. |
| `depends_on` | None beyond Gate 0. |

#### REF-01-U1.4 — Multi-head attention with GQA (feeds Gate 1)

| Field | Value |
| --- | --- |
| `outcome` | Multi-head attention with GQA KV-head sharing in `gradus:attention`: per-head q/k/v splits (`num_kv_heads ≤ num_heads`), scaled scores, causal mask, v accumulation, head concatenation, output projection — over the staged f32 carrier; no fixed-shape constants. Executed proof: the GQA exempla prints PASS for an MHA config and a GQA config. |
| `write_scope` | `src/attention.fab`, `src/attention.proba`, `exempla/dense-gqa/` (`faber.toml`, `src/main.fab`, `README.md`), the five docs listed in U1.1, README as needed |
| `first_failing_oracle` | Red proof: proba pins independent f64 attention outputs for a GQA config (e.g., n_h=14, n_kv=2, head_dim=128 — the qwen2 shape) and an MHA config (n_kv = n_h) — recorded failing. Green @5e-4. |
| `closeout_command` | Same shape as U1.1 with `exempla/dense-gqa` and the attention changed-path list. |
| `expected_observed_result` | Same as U1.1; both config rows PASS. |
| `est_basis` | ≈3k–5k tokens (10–15 min): the largest attention behavior family (two configs in one row family); base 5e-4 attention pins. |
| `stop_condition` | Shared §6 conditions; first failing pin recorded and routed. |
| `depends_on` | U1.3 (configurable RoPE — q/k rotate by position in the inference row). |

#### REF-01-U1.5 — Generic dense transformer block (feeds Gate 1)

| Field | Value |
| --- | --- |
| `outcome` | The ordered dense transformer block in `gradus:transformer`: input RMSNorm → GQA attention (causal + RoPE) → residual → post-attn RMSNorm → SwiGLU MLP → residual — over the staged f32 carrier, composing the U1.1/U1.2/U1.4 rows; no fixed-shape constants. Executed proof: the block exempla prints PASS for a small synthetic dim config. |
| `write_scope` | `src/transformer.fab`, `src/transformer.proba`, `exempla/dense-block/` (`faber.toml`, `src/main.fab`, `README.md`), the five docs listed in U1.1, README as needed |
| `first_failing_oracle` | Red proof: proba pins independent f64 block outputs for a small synthetic dim config (the PML3 `transformer_block` pin precedent) — recorded failing. Green @5e-4. |
| `closeout_command` | Same shape as U1.1 with `exempla/dense-block` and `src/transformer.fab src/transformer.proba` in the changed-path list. |
| `expected_observed_result` | Same as U1.1; block pin rows PASS. |
| `est_basis` | ≈3k–5k tokens (10–15 min): composition of three already-proven rows plus the ordered-block proba; pin surface ≈8–12. |
| `stop_condition` | Shared §6 conditions; first failing pin recorded and routed. |
| `depends_on` | U1.1, U1.2, U1.4. |

#### REF-01-U1.6 — `llama` (SmolLM2) architecture adapter (feeds Gate 1)

| Field | Value |
| --- | --- |
| `outcome` | Typed `llama` architecture adapter: canonical tensor-name → manifest-descriptor mapping (`model.embed_tokens`, `model.layers.{N}.input_layernorm`, `.self_attn.{q,k,v,o}_proj`, `.post_attention_layernorm`, `.mlp.{gate,up,down}_proj`, `model.norm`, `lm_head`), frozen architecture config (layer count, heads, KV heads, head_dim, hidden dim, vocab, tied embedding), fail-closed on missing/unknown facts with typed diagnostics. Executed proof: the adapter exempla prints PASS for every canonical resolution plus rejection rows. |
| `write_scope` | `src/model/dense_llama.fab`, `src/model/dense_llama.proba`, `exempla/dense-llama-adapter/` (`faber.toml`, `src/main.fab`, `README.md`), the five docs listed in U1.1, README as needed |
| `first_failing_oracle` | Red proof: proba descriptor-resolution pins — each canonical name resolves to the exact descriptor facts (name, shape, layout) the GGUF-A1b inspect surface reports for the real SmolLM2 file (read-only pinned facts); unknown names fail typed — recorded failing. |
| `closeout_command` | Same shape as U1.1 with `exempla/dense-llama-adapter` and `src/model/dense_llama.fab src/model/dense_llama.proba` in the changed-path list. |
| `expected_observed_result` | Same as U1.1; every canonical resolution + fail-closed rejection row PASSes. |
| `est_basis` | ≈1.5k–3k tokens (10 min): a typed mapping + descriptor-resolution proba; no new arithmetic; comparable to the GGUF-A1b inspect adapter slice. |
| `stop_condition` | Shared §6 conditions; a SmolLM2 fact that cannot be represented as a typed descriptor is an architecture-fact gap, routed with the exact fact. |
| `depends_on` | Gate 0 + GGUF-A1b manifest surface (landed). |

#### REF-01-U1.7 — `qwen2` (Qwen2.5) architecture adapter (feeds Gate 1)

| Field | Value |
| --- | --- |
| `outcome` | Typed `qwen2` architecture adapter: the same canonical family plus the qwen2 deltas (untied `lm_head`, GQA head config, `rope_theta` 1000000), fail-closed with typed diagnostics. Executed proof: the adapter exempla prints PASS for every canonical resolution plus rejection rows. |
| `write_scope` | `src/model/dense_qwen2.fab`, `src/model/dense_qwen2.proba`, `exempla/dense-qwen2-adapter/` (`faber.toml`, `src/main.fab`, `README.md`), the five docs listed in U1.1, README as needed |
| `first_failing_oracle` | Red proof: proba descriptor-resolution pins for the Qwen2.5-0.5B row facts (read-only, pinned from the A1b inspect surface) — recorded failing. |
| `closeout_command` | Same shape as U1.1 with `exempla/dense-qwen2-adapter` and `src/model/dense_qwen2.fab src/model/dense_qwen2.proba` in the changed-path list. |
| `expected_observed_result` | Same as U1.1; every canonical resolution + rejection row PASSes. |
| `est_basis` | ≈1.5k–3k tokens (10 min): same basis as U1.6; follows the frozen llama-adapter mapping contract. |
| `stop_condition` | Shared §6 conditions; a qwen2 fact that cannot be represented as a typed descriptor is an architecture-fact gap, routed with the exact fact. |
| `depends_on` | U1.6 (adapter module pattern + typed mapping contract frozen). |

#### REF-01-U1.8 — Dense model assembly (feeds Gate 1)

| Field | Value |
| --- | --- |
| `outcome` | The complete ordered dense forward graph in `gradus:model/dense`: embedding gather → N ordered U1.5 blocks → final RMSNorm → output projection, assembled from the typed architecture config and materialized tensor views via canonical names; tied/untied embedding handling; zero per-row special-case constants. Executed proof: the model exempla prints PASS for a small synthetic dense config (tied + untied rows). |
| `write_scope` | `src/model/dense.fab`, `src/model/dense.proba`, `exempla/dense-model/` (`faber.toml`, `src/main.fab`, `README.md`), the five docs listed in U1.1, README as needed |
| `first_failing_oracle` | Red proof: proba pins independent f64 full-graph outputs for a small synthetic dense config (2 layers, tiny dims, tied + untied embedding rows) — recorded failing. Green @5e-4. |
| `closeout_command` | Same shape as U1.1 with `exempla/dense-model` and `src/model/dense.fab src/model/dense.proba` in the changed-path list. |
| `expected_observed_result` | Same as U1.1; full-graph pin rows PASS. |
| `est_basis` | ≈3k–6k tokens (10–15 min): composition of the U1.5 block + U1.6/U1.7 adapters + one full-graph proba; the largest surface unit, still one behavior family. |
| `stop_condition` | Shared §6 conditions; a per-row constant sneaking into the assembly (a shape/size pinned to a specific row) is a hard stop — the row-pinned grep must stay clean. |
| `depends_on` | U1.5, U1.6, U1.7. |

#### REF-01-U1.9 — SmolLM2 full-model prefill logit receipt (feeds Gate 1)

| Field | Value |
| --- | --- |
| `outcome` | Executed full-prefill logits for the real SmolLM2-360M file through the U1.8 surface vs the pinned llama.cpp comparator (llama.cpp 10150 / `dee2a846b`, binary SHA-256 `e5c153a1…52a`) under the gi0-numeric-contract discipline; first-divergence receipt (none expected on the declared window). |
| `execution_engine` | Compiled route — runner is not the engine; `faber build --target rust <exempla>` prints the binary; execute that binary; `faber build --target rust` is the receipt tier; llvm-host is fallback. The MIR stepper is explicitly NOT the receipt-tier engine (structural/proba tier only). Comparison: pinned llama.cpp comparator via the radix `faber-prefill-oracle` contract (`compare_gpu_logits` / `PrefillReceipt` / `ExecutableRegime` / `admit_pinned_file`); first-divergence receipt per the gi0 contract. |
| `write_scope` | `exempla/dense-prefill-smollm2/` (consumer + README receipt), `docs/factory/production-ml-library/pml0-support-matrix.md` (SmolLM2 dense reference execution claim at the executed tier), `docs/regression-corpus.md`, `docs/module-map.md`, `docs/api-reference.md`, `docs/diagnostics.md`, README as needed |
| `first_failing_oracle` | The pinned comparator's full-vocab logprob surface for the pinned correctness-fixture window (positions 0..16): finite gate, top-1 exact, top-5 overlap ≥4/5, Δ=1e-5 band; the first diverging position, token ids, failing thresholds, and max band deviation are recorded (campaign rule 5). |
| `closeout_command` | Structural gates (U1.1 shape) with `exempla/dense-prefill-smollm2` and the receipt-scope changed-path list; the run writes the receipt into the exempla README. |
| `expected_observed_result` | Receipt prints the comparison policy, exact command + working directory, Gradus/radix/faber/hosts revisions, model filename + byte length + SHA-256, tokenizer identity + prompt hash, hardware/OS/backend (CPU/reference), observed token ids, first divergence (none expected on declared windows). No Metal/CUDA or payload-residency claim. |
| `est_basis` | ≈1k–2.5k tokens (10–15 min including a minutes-long reference run): a run + frozen-format receipt (§9); comparable to the GGUF-A1b inspection receipt. |
| `stop_condition` | Shared §6 conditions; any first divergence pauses the edge and routes the repair to the owning surface (campaign rule 6). |
| `depends_on` | U1.8. |

#### REF-01-U1.10 — Qwen2.5-0.5B full-model prefill logit receipt (feeds Gate 1)

| Field | Value |
| --- | --- |
| `outcome` | Executed full-prefill logits for the real Qwen2.5-0.5B file through the SAME U1.8 surface vs the pinned llama.cpp toolset under the same comparison policy (delivery open question 1 default: reuse the pinned binary); first-divergence receipt (GQA attention exercised). |
| `execution_engine` | Compiled route — runner is not the engine; `faber build --target rust <exempla>` prints the binary; execute that binary; `faber build --target rust` is the receipt tier; llvm-host is fallback. The MIR stepper is explicitly NOT the receipt-tier engine (structural/proba tier only). Comparison: pinned llama.cpp comparator via the radix `faber-prefill-oracle` contract (`compare_gpu_logits` / `PrefillReceipt` / `ExecutableRegime` / `admit_pinned_file`); first-divergence receipt per the gi0 contract. |
| `write_scope` | `exempla/dense-prefill-qwen2/` (consumer + README receipt), `docs/factory/production-ml-library/pml0-support-matrix.md` (Qwen2.5-0.5B dense reference execution claim at the executed tier), `docs/regression-corpus.md`, `docs/module-map.md`, `docs/api-reference.md`, `docs/diagnostics.md`, README as needed |
| `first_failing_oracle` | Same policy as U1.9 on the qwen2 row. |
| `closeout_command` | Structural gates with `exempla/dense-prefill-qwen2`; the run writes the receipt into the exempla README. |
| `expected_observed_result` | Same as U1.9 for the Qwen2.5-0.5B row (tokenizer ids per the LIB-02 pins). |
| `est_basis` | ≈1k–2.5k tokens (10–15 min): reuses the U1.9 receipt script and policy; per-row run. |
| `stop_condition` | Shared §6 conditions; a per-row comparator-revision requirement routes to a campaign amendment (open question 1), not a new unit. |
| `depends_on` | U1.8 (surface), U1.9 (receipt script pattern). |

### Wave U2 — GGUF-A5: real prefill, decode, and KV state (6 micro-units)

#### REF-01-U2.1 — Per-layer per-KV-head cache state (feeds Gate 2)

| Field | Value |
| --- | --- |
| `outcome` | KVCache extended from the one-block logical state to per-layer per-KV-head typed state in `gradus:cache`: K/V per layer and per KV head (`[positions, head_dim]` staged f32), typed construction from the dense config (layers, KV heads, head_dim), sequential one-position append, generation counter, identity fields preserved. Executed proof: the cache exempla prints PASS for state-value and mutation pins. |
| `write_scope` | `src/cache.fab`, `src/cache.proba`, `exempla/dense-cache/` (`faber.toml`, `src/main.fab`, `README.md`), the five docs listed in U1.1, README as needed |
| `first_failing_oracle` | Red proof: proba state/mutation pins — append/readback exact values and shapes per layer and head (exact concatenation, no rounding) + identity-field pins — recorded failing. |
| `closeout_command` | Same shape as U1.1 with `exempla/dense-cache` and `src/cache.fab src/cache.proba` in the changed-path list. |
| `expected_observed_result` | Same as U1.1; per-layer per-head append/readback pin rows PASS. |
| `est_basis` | ≈2k–4k tokens (10–15 min): extends the existing cache contract (the old U2 surface split across four behavior families); cache pins ≈6–10. |
| `stop_condition` | Shared §6 conditions; first failing pin recorded and routed. |
| `depends_on` | None beyond Gate 0 (extends the landed `cache.fab`). |

#### REF-01-U2.2 — KV-backed attention integration (feeds Gate 2)

| Field | Value |
| --- | --- |
| `outcome` | Attention integrated with the per-layer per-KV-head cache in `gradus:attention`: per-head q·kᵀ over cached K, causal mask at the current position, v accumulation, and the new position's K/V slice returned for append; the incremental result equals the no-cache full-row reference (the position-invariance precedent). Executed proof: the KV-attention exempla prints PASS for the agreement rows. |
| `write_scope` | `src/attention.fab`, `src/attention.proba`, `src/cache.fab` (slice-contract rows only), `exempla/dense-kv-attention/` (`faber.toml`, `src/main.fab`, `README.md`), the five docs listed in U1.1, README as needed |
| `first_failing_oracle` | Red proof: proba pinned agreement — cached incremental attention == no-cache full-row attention on the same token sequence (f64) — recorded failing. Green @5e-4. |
| `closeout_command` | Same shape as U1.1 with `exempla/dense-kv-attention` and the attention+cache changed-path list. |
| `expected_observed_result` | Same as U1.1; the cached==no-cache agreement rows PASS. |
| `est_basis` | ≈2k–4k tokens (10–15 min): one state-integration behavior family. |
| `stop_condition` | Shared §6 conditions; first failing pin recorded and routed. |
| `depends_on` | U1.4, U2.1. |

#### REF-01-U2.3 — Dense prefill with cache write (feeds Gate 2)

| Field | Value |
| --- | --- |
| `outcome` | Dense prefill over the full layer stack writes the per-layer per-KV-head cache (teacher-forced); fails closed when the prompt length exceeds the context; logits identical to the U1.8 no-cache forward at every position. Executed proof: the prefill-cache exempla prints PASS for the agreement rows. |
| `write_scope` | `src/model/dense.fab`, `src/model/dense.proba`, `exempla/dense-prefill-cache/` (`faber.toml`, `src/main.fab`, `README.md`), the five docs listed in U1.1, README as needed |
| `first_failing_oracle` | Red proof: proba pinned agreement — prefill-with-cache logits == U1.8 full-model forward logits at every position (f64) — recorded failing. Green @5e-4. |
| `closeout_command` | Same shape as U1.1 with `exempla/dense-prefill-cache` and the dense changed-path list. |
| `expected_observed_result` | Same as U1.1; prefill agreement + context-rejection rows PASS. |
| `est_basis` | ≈2k–4k tokens (10–15 min): one prefill behavior family on the dense surface. |
| `stop_condition` | Shared §6 conditions; first failing pin recorded and routed. |
| `depends_on` | U1.8, U2.2. |

#### REF-01-U2.4 — Incremental decode with session behaviors (feeds Gate 2)

| Field | Value |
| --- | --- |
| `outcome` | One-token incremental decode consumes the per-layer per-KV-head cache and appends each position; `Session` advance with context rejection at the limit; cooperative cancellation observation at step boundaries; deterministic replay; session identity — wired onto the dense decode surface. Executed proof: the decode-cache exempla prints PASS for agreement + typed-behavior rows. |
| `write_scope` | `src/decode.fab`, `src/decode.proba` (dense session rows), `src/model/dense.fab` (decode entry as needed), `exempla/dense-decode-cache/` (`faber.toml`, `src/main.fab`, `README.md`), the five docs listed in U1.1, README as needed |
| `first_failing_oracle` | Red proof: proba pinned agreement — incremental decode reproduces prefill-equivalent logits at the declared boundary; context-rejection, cancellation, and replay typed-error pins — recorded failing. |
| `closeout_command` | Same shape as U1.1 with `exempla/dense-decode-cache` and the decode+dense changed-path list. |
| `expected_observed_result` | Same as U1.1; decode agreement + rejection/cancellation/replay rows PASS. |
| `est_basis` | ≈2k–4k tokens (10–15 min): reuses the landed `Session`/`Cancellation`/`replica` semantics; one decode behavior family. |
| `stop_condition` | Shared §6 conditions; first failing pin recorded and routed. |
| `depends_on` | U2.3. |

#### REF-01-U2.5 — SmolLM2 executed prefill/decode agreement + reset/reuse receipt (feeds Gate 2)

| Field | Value |
| --- | --- |
| `outcome` | Executed proof on the real SmolLM2 file: full dense prefill and incremental decode agree on logits at the declared boundary; two prompts prove reset/reuse; context rejection, cancellation observation, deterministic replay, and session identity are executed and recorded — one receipt per the A5 contract. |
| `execution_engine` | Compiled route — runner is not the engine; `faber build --target rust <exempla>` prints the binary; execute that binary; `faber build --target rust` is the receipt tier; llvm-host is fallback. The MIR stepper is explicitly NOT the receipt-tier engine (structural/proba tier only). Comparison: pinned llama.cpp comparator via the radix `faber-prefill-oracle` contract (`compare_gpu_logits` / `PrefillReceipt` / `ExecutableRegime` / `admit_pinned_file`); first-divergence receipt per the gi0 contract. |
| `write_scope` | `exempla/dense-session-smollm2/` (consumer + README receipt), `docs/factory/production-ml-library/pml0-support-matrix.md` (SmolLM2 KV/prefill-decode execution at the executed tier), `docs/regression-corpus.md`, `docs/module-map.md`, `docs/api-reference.md`, `docs/diagnostics.md`, README as needed |
| `first_failing_oracle` | The U1.9 comparator policy on the decode path: prefill-vs-decode logit agreement at the declared boundary; reset/replay determinism (same seed + input → same tokens). |
| `closeout_command` | Structural gates with `exempla/dense-session-smollm2`; the run writes the receipt into the exempla README. |
| `expected_observed_result` | Receipt names the prefill/decode agreement positions, the two reset/reuse prompts (exact prompts, positions, session identities), context-rejection, cancellation, replay, and session-identity facts (§9 expected-result block). |
| `est_basis` | ≈1k–2.5k tokens (10–15 min including runs): run + receipt on top of U2.4. |
| `stop_condition` | Shared §6 conditions; a first divergence pauses the edge and routes the repair. |
| `depends_on` | U2.4. |

#### REF-01-U2.6 — Qwen2.5-0.5B executed prefill/decode agreement + reset/reuse receipt (feeds Gate 2)

| Field | Value |
| --- | --- |
| `outcome` | Same executed proof for the real Qwen2.5-0.5B file (GQA KV heads exercised): prefill/decode agreement at the declared boundary, two-prompt reset/reuse, and the state family (context rejection, cancellation, replay, session identity) executed and recorded. |
| `execution_engine` | Compiled route — runner is not the engine; `faber build --target rust <exempla>` prints the binary; execute that binary; `faber build --target rust` is the receipt tier; llvm-host is fallback. The MIR stepper is explicitly NOT the receipt-tier engine (structural/proba tier only). Comparison: pinned llama.cpp comparator via the radix `faber-prefill-oracle` contract (`compare_gpu_logits` / `PrefillReceipt` / `ExecutableRegime` / `admit_pinned_file`); first-divergence receipt per the gi0 contract. |
| `write_scope` | `exempla/dense-session-qwen2/` (consumer + README receipt), `docs/factory/production-ml-library/pml0-support-matrix.md` (Qwen2.5-0.5B KV/prefill-decode execution at the executed tier), `docs/regression-corpus.md`, `docs/module-map.md`, `docs/api-reference.md`, `docs/diagnostics.md`, README as needed |
| `first_failing_oracle` | Same policy as U2.5 on the qwen2 row. |
| `closeout_command` | Structural gates with `exempla/dense-session-qwen2`; the run writes the receipt into the exempla README. |
| `expected_observed_result` | Same as U2.5 for the Qwen2.5-0.5B row. |
| `est_basis` | ≈1k–2.5k tokens (10–15 min): reuses the U2.5 receipt pattern and script. |
| `stop_condition` | Shared §6 conditions; a first divergence pauses the edge and routes the repair. |
| `depends_on` | U2.5. |

### Wave U3 — GGUF-A6: multiple dense acceptance rows (3 micro-units)

#### REF-01-U3.1 — SmolLM2 deterministic-text acceptance receipt (feeds Gate 3)

| Field | Value |
| --- | --- |
| `outcome` | The dense-rows acceptance consumer runs the full chain — manifest, tokenizer, materialization, full-model, prefill/decode, deterministic-text — for the real SmolLM2 file from real prompts through the same public surface; deterministic-text receipt (prompt hash, first token, decoded text, first divergence); an unsupported-family typed-diagnostics row is included. |
| `write_scope` | `exempla/dense-accept-smollm2/` (consumer + README receipt), `docs/factory/production-ml-library/pml0-support-matrix.md` (SmolLM2 dense row acceptance at the executed tier), `docs/regression-corpus.md`, `docs/module-map.md`, `docs/api-reference.md`, `docs/diagnostics.md`, README as needed |
| `first_failing_oracle` | Pinned llama.cpp deterministic text/token comparison (gi0 workload + expected-trace policy); the first divergent token id or decoded character — never text-level similarity. |
| `closeout_command` | Structural gates with `exempla/dense-accept-smollm2`; the run writes the receipt into the exempla README. |
| `expected_observed_result` | Receipt names prompt hash, first token, decoded text, first divergence (none expected on declared windows); tokenizer ids match the LIB-02 pins. |
| `est_basis` | ≈1k–2.5k tokens (10–15 min including the run): exempla + receipt on top of U1/U2 (the old U3 estimate split across three rows). |
| `stop_condition` | Shared §6 conditions; a first divergence pauses the edge and routes the repair. |
| `depends_on` | U2.5. |

#### REF-01-U3.2 — Qwen2.5-0.5B deterministic-text acceptance receipt (feeds Gate 3)

| Field | Value |
| --- | --- |
| `outcome` | The same acceptance chain for the real Qwen2.5-0.5B file through the same public surface; deterministic-text receipt; unsupported-family typed diagnostics retained. |
| `write_scope` | `exempla/dense-accept-qwen2/` (consumer + README receipt), `docs/factory/production-ml-library/pml0-support-matrix.md` (Qwen2.5-0.5B dense row acceptance at the executed tier), `docs/regression-corpus.md`, `docs/module-map.md`, `docs/api-reference.md`, `docs/diagnostics.md`, README as needed |
| `first_failing_oracle` | Same policy as U3.1 on the qwen2 row. |
| `closeout_command` | Structural gates with `exempla/dense-accept-qwen2`; the run writes the receipt into the exempla README. |
| `expected_observed_result` | Same as U3.1 for the Qwen2.5-0.5B row. |
| `est_basis` | ≈1k–2.5k tokens (10–15 min): reuses the U3.1 acceptance-consumer pattern. |
| `stop_condition` | Shared §6 conditions; a first divergence pauses the edge and routes the repair. |
| `depends_on` | U2.6, U3.1 (acceptance-consumer pattern). |

#### REF-01-U3.3 — Qwen2.5-1.5B scale-independence acceptance receipt (feeds Gate 3)

| Field | Value |
| --- | --- |
| `outcome` | The SAME adapter runs the real Qwen2.5-1.5B file with zero per-row special-case constants (hard grep proof: no row-pinned shapes/sizes in adapters/assembly); deterministic-text receipt; support matrix shows three executed dense rows. |
| `write_scope` | `exempla/dense-accept-qwen2-15b/` (consumer + README receipt), `docs/factory/production-ml-library/pml0-support-matrix.md` (three executed dense rows), `docs/regression-corpus.md`, `docs/module-map.md`, `docs/api-reference.md`, `docs/diagnostics.md`, README as needed |
| `first_failing_oracle` | Same policy as U3.1 on the 1.5B row; the no-constants grep is a hard gate — a row-pinned shape/size in the adapter or assembly fails the unit. |
| `closeout_command` | Structural gates with `exempla/dense-accept-qwen2-15b` plus the no-constants grep; the run writes the receipt into the exempla README. |
| `expected_observed_result` | Receipt proves the 1.5B passes through the identical adapter; the grep is clean; support matrix lists three executed dense rows. |
| `est_basis` | ≈1k–2.5k tokens (10–15 min including the larger run): reuses U3.2; the grep is mechanical. |
| `stop_condition` | Shared §6 conditions; a latent per-row constant anywhere in the dense surface is a hard stop and a defect, not a workaround. |
| `depends_on` | U3.2. |

## 5. Checkpoints And Gates

1. **Gate 0 (no start)**: any of the 19 micro-units is blocked until LIB-02 and LIB-03 receipts are accepted (campaign dependency graph; the delivery authority's `GGUF-A2 + GGUF-A3 → GGUF-A4`).
2. **Per-unit gate**: each micro-unit's done oracle — its executed proof passes (proba pins / exempla PASS rows / receipt prints), `./scripta/check-source` and `./scripta/check-compile` exit 0, `git diff --check` silent, regression-corpus inventory updated. A unit is dispatch-ready as soon as its `depends_on` predecessors closed (dispatch table, §10).
3. **Gate 1 (after U1.9, U1.10)**: full-model prefill logit receipts for SmolLM2 and Qwen2.5-0.5B at first-divergence boundary; the shared-primitive surface (`gradus:nn` / `gradus:attention` / `gradus:transformer` rows) is frozen for `qwen35moe`.
4. **Gate 2 (after U2.5, U2.6)**: prefill/decode agreement + reset/reuse receipts on both rows; the per-layer per-KV-head state surface is frozen.
5. **Gate 3 (after U3.1–U3.3)**: three dense deterministic-text receipts; support matrix shows three executed dense rows; the 1.5B no-constants proof.
6. **Audit**: an independent auditor verifies the receipts against the pinned oracle and checks for no special-case constants (grep for row-pinned shapes/sizes in adapters/assembly).

## 6. Milestone And Campaign-Contract Statement

- **Milestone advanced**: Q2 (complete model semantics) — the "dense reference rungs plus full `qwen35moe` reference execution" milestone's dense half.
- **Why REF-01 completion is NOT campaign completion**: REF-01 satisfies only the dense reference portion of Q2. The campaign remains open through MODEL-01..04 (`qwen35moe` admission, MoE router, hybrid SSM/attention, full-model reference), EXEC-01/02/03, CAP-01/CAP-02, and CLOSE-01. Every successor unit in the campaign dependency graph is preserved: `REF-01 → MODEL-04 → EXEC-01 + EXEC-02 → EXEC-03 → CAP-01 + CAP-02 → CLOSE-01`, plus `MODEL-02/MODEL-03` gating `MODEL-04` and the parallel `MODEL-01` branch. This lowering does not narrow, downgrade, defer, make optional, or move any admitted Qwen work outside the campaign.
- **Stop conditions**: any REF-01 unit pauses its edge and routes a correction when the target identity mismatches, a required architecture fact cannot be represented, the oracle is missing or unpinned for a row, a public Gradus API would acquire device ownership, or execution would require unapproved paid infrastructure.

## 7. Local Corpus Boundary And Hardware/Backend Authority

Local corpus (operator evidence; never committed into Gradus):

| Artifact | Path | Bytes | SHA-256 | Tensors | Architecture |
| --- | --- | --- | --- | --- | --- |
| SmolLM2-360M-Instruct-Q4_K_M.gguf | `/Users/ianzepp/ai/models/` | 270,590,880 | `2fa3f013dcdd7b99f9b237717fa0b12d75bbb89984cc1274be1471a465bac9c2` | 290 | `llama` |
| Qwen2.5-0.5B-Instruct-Q4_K_M.gguf | `/Users/ianzepp/ai/models/` | 397,808,192 | `6eb923e7d26e9cea28811e1a8e852009b21242fb157b26149d3b188f3a8c8653` | 290 | `qwen2` |
| Qwen2.5-1.5B-Instruct-Q4_K_M.gguf | `/Users/ianzepp/ai/models/` | 986,048,768 | `1adf0b11065d8ad2e8123ea110d1ec956dab4ab038eab665614adba04b6c3370` | 338 | `qwen2` |
| Qwen3.6-35B-A3B-UD-Q4_K_M.gguf | `/Users/ianzepp/ai/models/` | 22,663,387,424 | `0b21525e972670ed59e1812e170b27c26355381f0656ecc4e25617ece7dac58b` | 753 | `qwen35moe` (NOT part of REF-01; completion row) |

Verified this run: target byte length and SHA-256 match the campaign invariant exactly; the three dense rows match the GGUF-A1b inspection inventory.

Hardware/backend authority for REF-01: **CPU/reference only**. Gradus owns device-neutral reference execution (delivery authority: "CPU/reference logits and deterministic token receipts"). No Metal/CUDA execution is claimed or required by any REF-01 unit — native quantized execution is GGUF-A7/M5 (EXEC-02/CAP-01/CAP-02), whose receipts are explicitly not satisfied by reference runs. Oracle authority: pinned llama.cpp comparator on the local machine per gi0-comparator-contract; the gi0-numeric-contract discipline (finite gate, top-1 exactness on the declared window, first-divergence rule) binds every comparison.

## 8. Open Questions For Mind

1. **Qwen-row oracle pin**: gi0-comparator-contract pins llama.cpp 10150 / `dee2a846b` for the SmolLM2 row. The same toolset supports `qwen2` (verified in the live llama.cpp tree); no separate comparator-contract revision exists for the Qwen rows. Default for U1.9/U1.10, U2.5/U2.6, U3.1–U3.3: reuse the same pinned binary under the same comparison policy; if a per-row comparator revision is required, that is a campaign-level amendment, not a REF-01 unit.
2. **Module/exempla layout**: §4 names concrete defaults — `src/model/dense.fab` (assembly), `src/model/dense_llama.fab` / `src/model/dense_qwen2.fab` (adapters), and one small `exempla/dense-*` package per unit (parallel-safe, the A1a executed-proof precedent). The authoritative module map and naming live with the delivery/Gradus architecture ownership (the delivery authority names operations, not files). Mind/admission confirms placement; if admission prefers fewer exempla packages, that is a layout amendment, not a scope change.
3. **`est_basis`**: per-unit estimates live in §4 (≈1k–6k tokens each, 10–15 min Hand time per the 2026-08-14 granularity directive). If admission wants tighter bounds, the auditor's task-body review (campaign execution rule 3) is the natural checkpoint.
4. **Faber binary + locale pack**: `check-compile` requires a lane-local faber binary (FABER_BIN) and its matching `la` locale pack from the same radix build — a mismatched pair fails with pack-validation errors (verified 2026-08-14 in this packet). The pinned public faber `1fb6cc97e66d` tree is present, and the main radix debug binary exists at `/Users/ianzepp/work/faberlang/radix/target/debug/faber`. The implementing Hand's packet must name the exact binary and locale-pack wiring (locale `la` pack validation must pass).

## 9. Closeout Commands (per unit, from the Hand packet)

Structural gates — every micro-unit:

```bash
cd /Users/ianzepp/work/faberlang/worktrees/<lane>/gradus
./scripta/check-source
env FABER_LIBRARY_HOME=<lane home> \
  FABER_BIN=<lane-local faber binary> ./scripta/check-compile
git diff --check -- <exact changed paths of the unit>
```

Executed proof per unit — run the unit's exempla through package MIR (the GGUF-A1a executed-proof precedent; `FABER_BIN` and the `la` locale pack must be a matching pair from the same radix build):

```bash
env FABER_LIBRARY_HOME=<lane home> \
  <lane-local faber binary> run --target fmir exempla/dense-<unit-name>
```

```text
# U1 surface: dense-rmsnorm · dense-swiglu · dense-rope · dense-gqa ·
#             dense-block · dense-llama-adapter · dense-qwen2-adapter ·
#             dense-model
# U1 receipts: dense-prefill-smollm2 · dense-prefill-qwen2
# U2 surface: dense-cache · dense-kv-attention · dense-prefill-cache ·
#             dense-decode-cache
# U2 receipts: dense-session-smollm2 · dense-session-qwen2
# U3 receipts: dense-accept-smollm2 · dense-accept-qwen2 ·
#              dense-accept-qwen2-15b (+ the no-constants grep for U3.3)
```

**Expected observed result**: `check-source` and `check-compile` exit 0; `git diff --check` silent; each surface exempla prints PASS for its pinned rows (0 FAIL, exit 0); each receipt prints the comparison policy, the exact command + working directory, Gradus/radix/faber/hosts revisions, model filename + byte length + SHA-256, tokenizer identity and prompt hash, hardware/OS/backend (CPU/reference), observed token ids and decoded text, first divergence (none expected on declared windows), and — for the U2-wave receipts — reset/reuse and cancellation facts. No receipt claims Metal/CUDA execution or full-model payload residency.

**First implementation frontier**: after LIB-02 + LIB-03 receipts are accepted, the first Hand task is REF-01-U1.1 (generic RMSNorm) — `gradus:nn` with the GGUF-A1b manifest descriptor/range surface as the adapter input; the U1 wave then dispatches in parallel up to the dependency edges (dispatch table below).

## 10. Dispatch-Ready Micro-Unit List (for Mind tasking)

| Unit | Authority | Feeds gate | depends_on | Est |
| --- | --- | --- | --- | --- |
| REF-01-U1.1 Generic RMSNorm | GGUF-A4 | Gate 1 | Gate 0 (LIB-02/LIB-03) | 2k–4k |
| REF-01-U1.2 SiLU + SwiGLU MLP | GGUF-A4 | Gate 1 | Gate 0 | 2k–4k |
| REF-01-U1.3 Configurable RoPE | GGUF-A4 | Gate 1 | Gate 0 | 2k–4k |
| REF-01-U1.4 MHA with GQA | GGUF-A4 | Gate 1 | U1.3 | 3k–5k |
| REF-01-U1.5 Generic dense block | GGUF-A4 | Gate 1 | U1.1, U1.2, U1.4 | 3k–5k |
| REF-01-U1.6 `llama` adapter | GGUF-A4 | Gate 1 | Gate 0 + A1b | 1.5k–3k |
| REF-01-U1.7 `qwen2` adapter | GGUF-A4 | Gate 1 | U1.6 | 1.5k–3k |
| REF-01-U1.8 Dense model assembly | GGUF-A4 | Gate 1 | U1.5, U1.6, U1.7 | 3k–6k |
| REF-01-U1.9 SmolLM2 prefill logit receipt | GGUF-A4 | Gate 1 | U1.8 | 1k–2.5k |
| REF-01-U1.10 Qwen2.5-0.5B prefill logit receipt | GGUF-A4 | Gate 1 | U1.8, U1.9 | 1k–2.5k |
| REF-01-U2.1 Per-layer per-KV-head cache | GGUF-A5 | Gate 2 | Gate 0 | 2k–4k |
| REF-01-U2.2 KV-backed attention | GGUF-A5 | Gate 2 | U1.4, U2.1 | 2k–4k |
| REF-01-U2.3 Dense prefill with cache | GGUF-A5 | Gate 2 | U1.8, U2.2 | 2k–4k |
| REF-01-U2.4 Incremental decode + session behaviors | GGUF-A5 | Gate 2 | U2.3 | 2k–4k |
| REF-01-U2.5 SmolLM2 agreement + state receipt | GGUF-A5 | Gate 2 | U2.4 | 1k–2.5k |
| REF-01-U2.6 Qwen2.5-0.5B agreement + state receipt | GGUF-A5 | Gate 2 | U2.5 | 1k–2.5k |
| REF-01-U3.1 SmolLM2 acceptance receipt | GGUF-A6 | Gate 3 | U2.5 | 1k–2.5k |
| REF-01-U3.2 Qwen2.5-0.5B acceptance receipt | GGUF-A6 | Gate 3 | U2.6, U3.1 | 1k–2.5k |
| REF-01-U3.3 Qwen2.5-1.5B scale-independence receipt | GGUF-A6 | Gate 3 | U3.2 | 1k–2.5k |

Serial edges that define the wave shape: U1.3→U1.4→U1.5→U1.8→U1.9→U1.10 (U1.6/U1.7 parallel with U1.1–U1.5), U2.1→U2.2→U2.3→U2.4→U2.5→U2.6, U3.1→U3.2→U3.3. All other pairs at the same wave depth are parallel-safe (disjoint write scopes).
