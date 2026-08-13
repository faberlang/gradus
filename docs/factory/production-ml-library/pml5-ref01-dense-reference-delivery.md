# Delivery Lowering: REF-01 — Mandatory Dense Reference Rungs

**Status**: planned — implementation-ready delivery lowering, awaiting LIB-02/LIB-03 receipts
**Planner**: planner-24 (fresh lowering, derived independently from campaign, delivery authority, and live repos)
**Assignment**: task `aba59bcc` (Mind → planner-24)
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

## 3. Repo-Aware Baseline

Pinned baselines (verified in this worktree):

| Repo | Baseline | Verified |
| --- | --- | --- |
| radix | `b6d6e17c8ad7` | worktree HEAD |
| gradus | `bc500993c97b` | worktree HEAD |
| hosts | `57d659d60430` | worktree HEAD |
| faber (public) | `1fb6cc97e66d` | worktree HEAD |

Current gradus dense surface (live tree, this worktree):

- `src/nn.fab` — `linear_2x2/4x4/2x8`, `gelu_2x8/4x4`, `layernorm_2x8` (fixed-shape rows only; no generic RMSNorm/SiLU/SwiGLU).
- `src/attention.fab` — `scaled_dot_product_staticum`, `scaled_dot_product(_causal)`, `rotary_position_embedding` over staged carriers; no GQA, no per-head KV.
- `src/transformer.fab` — `bert_tiny_block_2x8` and `transformer_block` (PML3 fixed-shape rows).
- `src/decode.fab` — `structa_pondera`, `structa_decodere`, `decodere_datum`, `praefundere`, `sessio_fresh/progredere/redintegra`, `cancelatum_*`, `replica` (fixed one-block forward row, PML5).
- `src/cache.fab` — `cache_vacua`, `appende`, `redintegra`, identity serialization (logical KV values; no per-layer per-head execution).
- `src/model/` — `artifact`, `gguf_manifest` (GGUF-A1a/A1b), `capsule`, `gguf`, `safetensors`, `dequant` (PML2 rows).
- `src/tokenizer.fab` — tokenizer **identity** contract (PML2-U4); tokenizer **runtime** (encode/decode text) is GGUF-A2 = LIB-02.

None of these execute a complete dense SmolLM2/Qwen2.5 forward stack. REF-01 is therefore genuinely from-scratch for full-model semantics; it reuses the GGUF-A1b manifest surface (descriptor/range facts) and will consume the GGUF-A2/A3 payload surfaces when those land.

## 4. Ordered Unit Graph

Predecessor receipts required before any REF-01 unit starts:

- **LIB-02 (GGUF-A2) accepted** — artifact-backed tokenizer runtime (encode/decode, special-token policy, chat-template behavior) matching pinned llama.cpp ids/text for the two Unicode probes on the three dense rows and the target artifact.
- **LIB-03 (GGUF-A3) accepted** — checked packed storage and reference materialization; every tensor required by the forward graph has a validated range, shape, layout, and bounded materialization path.

The campaign already sequences these: `TRUTH-01 → LIB-01 → LIB-02 + LIB-03 → REF-01`. This lowering does not reorder, narrow, or move them.

### REF-01-U1 — GGUF-A4: dense Llama/Qwen primitives and full model

| Field | Value |
| --- | --- |
| `id` | `REF-01-U1` (authority: GGUF-A4) |
| `outcome` | Gradus executes the complete ordered dense layer stack — RMSNorm, SiLU/SwiGLU MLP, configurable RoPE, multi-head attention with GQA, tied/untied embeddings, final normalization, output projection — assembled by explicit architecture adapters and canonical tensor names for `llama` (SmolLM2) and `qwen2` (Qwen2.5) rows. Full SmolLM2 and Qwen2.5-0.5B prefill logit rows match the independent CPU oracle at the first-divergence boundary. These are the reusable forward operations consumed by `qwen35moe`. |
| `dependencies` | LIB-02 (GGUF-A2), LIB-03 (GGUF-A3); GGUF-A1b manifest surface (already landed) |
| `first_failing_oracle` | Pinned llama.cpp comparator (gi0-comparator-contract: llama.cpp 10150 / `dee2a846b`, binary SHA-256 `e5c153a1…52a`) serving the local SmolLM2 row; per-position full-vocab logits compared under gi0-numeric-contract discipline (finite gate, top-1 exact on the declared window, first-divergence rule). Qwen rows use the same comparison policy against the pinned llama.cpp toolset. |
| `write_scope` | `gradus/src/model/dense.fab` (or authority-chosen module name), `gradus/src/model/dense.proba`, architecture-adapter modules and probas under `gradus/src/model/`, `gradus/src/nn.fab`/`gradus/src/nn.proba` (generic RMSNorm/SiLU/SwiGLU rows only), `gradus/src/attention.fab`/proba (GQA + configurable RoPE rows only), `gradus/src/transformer.fab`/proba (generic block rows only), `docs/module-map.md`, `docs/api-reference.md`, `docs/diagnostics.md`, `docs/regression-corpus.md`, `docs/factory/production-ml-library/pml0-support-matrix.md` (add dense reference execution claims at executed tier only), README as needed |
| `read_scope` | `gradus/src/model/gguf_manifest.fab`, `gradus/src/model/dequant.fab`, `gradus/src/tokenizer.fab`, the four local GGUF files under `/Users/ianzepp/ai/models/` (read-only), gi0–gi3 contract docs in `radix/docs/factory/gpu-inference-gguf/` (read-only) |
| `forbidden_scope` | `src/model/capsule.fab`/`gguf.fab`/`safetensors.fab` (LIB-01 clean-break territory), `src/decode.fab`/`cache.fab`/`sampling.fab`/`generation.fab` (REF-01-U2/U3 and PML5 territory), radix/hosts/faber product code, any path in another worktree or on main |
| `done_when` | Both dense prefill logit rows (SmolLM2, Qwen2.5-0.5B) match the pinned oracle at the first-divergence boundary; a typed architecture adapter exists per row with no per-row special-case constants; `./scripta/check-source` and `./scripta/check-compile` exit 0; proba suite added and inventoried in regression corpus |
| `validation` | `./scripta/check-source`; `./scripta/check-compile` with lane-local `FABER_BIN`; `git diff --check`; oracle comparison receipt script that prints first divergence (or exact match) per row; regression-corpus inventory update |
| `non_goals` | KV state execution (U2), deterministic-text generation (U3), MoE/SSM, native GPU kernels, tokenizer runtime (LIB-02), packed storage (LIB-03) |
| `risk` | **high** — first full-model adapter; many new tensor ops; oracle divergence debugging is the main cost. Mitigation: U1 publishes a first-divergence receipt before iterating, per campaign rule 5. |
| `est_work_tokens` | 24k–48k |
| `est_basis` | comparable PML5-U1..U6 lowering sizes (8k–24k per unit) scaled for two full-model adapters plus new generic primitives; the proba pin surface alone is larger than any prior gradus unit |
| `tool_latency` | low–medium (check-source ≈1s; check-compile with lane-local faber binary seconds; full-model prefill comparison minutes) |

### REF-01-U2 — GGUF-A5: real prefill, decode, and KV state

| Field | Value |
| --- | --- |
| `id` | `REF-01-U2` (authority: GGUF-A5) |
| `outcome` | Per-layer, per-KV-head state integrated into attention for the dense rows. Prefill and incremental decode produce equivalent logits at the declared boundary. Reset, context rejection, cancellation observation, replay, and session identity are executed (not merely compiled). |
| `dependencies` | REF-01-U1 accepted |
| `first_failing_oracle` | llama.cpp comparator as in U1; additionally a prefill-vs-decode agreement check on the same prompt tokens and a reset/replay determinism check (same seed + input → same tokens) |
| `write_scope` | KV-state and decode-path modules under `gradus/src/model/` (or authority-chosen names), `gradus/src/cache.fab`/proba (per-layer per-head state rows), `gradus/src/decode.fab`/proba (dense prefill/decode rows), `gradus/src/generation.fab`/proba as needed, `docs/module-map.md`, `docs/api-reference.md`, `docs/diagnostics.md`, `docs/regression-corpus.md`, `docs/factory/production-ml-library/pml0-support-matrix.md`, README as needed |
| `read_scope` | REF-01-U1 modules, `gradus/src/cache.fab`/`decode.fab`/`sampling.fab`/`generation.fab` existing fixed-shape rows (read-only reference), local GGUF corpus (read-only), gi0–gi4 contract docs (read-only) |
| `forbidden_scope` | model admission/capsule (LIB-01), tokenizer runtime (LIB-02), packed storage (LIB-03), MoE/SSM (MODEL-01..04), radix/hosts/faber product code, native GPU work (GGUF-A7/M5) |
| `done_when` | Dense prefill and incremental decode agree on logits at the declared boundary on SmolLM2 and Qwen2.5-0.5B; two prompts prove reset/reuse; context rejection and cancellation observation are executed and recorded; check gates green; probas inventoried |
| `validation` | same check gates as U1; prefill/decode agreement receipt; reset/reuse receipt naming exact prompts, positions, and session identities |
| `non_goals` | full 256-token deterministic-text runs (U3), native kernels, MoE/SSM, sampling-family expansion (PML5 already owns) |
| `risk` | **medium-high** — state integration is where prefill/decode disagreement typically hides; mitigated by the agreement check as a first-divergence oracle |
| `est_work_tokens` | 16k–32k |
| `est_basis` | PML5-U1/U2/U5 lowering sizes (8k–24k) scaled for per-layer per-head generality; smaller than U1 because it extends existing cache/decode structure |
| `tool_latency` | low–medium (check gates fast; prefill/decode comparison runs minutes) |

### REF-01-U3 — GGUF-A6: multiple dense acceptance rows

| Field | Value |
| --- | --- |
| `id` | `REF-01-U3` (authority: GGUF-A6) |
| `outcome` | The actual local SmolLM2-360M and Qwen2.5-0.5B files pass manifest, tokenizer, materialization, full-model, prefill/decode, and deterministic-token receipts. Qwen2.5-1.5B passes through the same adapter with no special-case constants, proving scale independence. Deterministic text receipts come from real prompts through the same public library surface. |
| `dependencies` | REF-01-U2 accepted; LIB-02 (tokenizer runtime), LIB-03 (packed storage) |
| `first_failing_oracle` | Pinned llama.cpp deterministic text/token comparison (gi0 workload + expected-trace policy); first divergent token id or decoded character, never text-level similarity |
| `write_scope` | acceptance exempla under `gradus/exempla/` (e.g. dense-rows acceptance consumer), new probas, `docs/module-map.md`, `docs/api-reference.md`, `docs/diagnostics.md`, `docs/regression-corpus.md`, `docs/factory/production-ml-library/pml0-support-matrix.md` (three dense executed rows), README as needed |
| `read_scope` | U1/U2 modules, LIB-02/LIB-03 surfaces, local GGUF corpus (read-only), llama.cpp pinned toolset (read-only) |
| `forbidden_scope` | capsule/GGUF-old-capsule migration (LIB-01), tokenizer runtime internals (LIB-02), storage internals (LIB-03), MoE/SSM, radix/hosts/faber product code, native GPU work |
| `done_when` | All three dense files produce deterministic text receipts from real prompts through the same public surface; 1.5B passes with zero per-row constants; regression corpus and support matrix updated; check gates green |
| `validation` | same check gates; per-row deterministic-text receipt naming prompt hash, first token, decoded text, first divergence if any |
| `non_goals` | the 35B target row (MODEL-01..04), native execution (GGUF-A7), capstone (GGUF-M6) |
| `risk` | **medium** — acceptance breadth; risk is a latent per-row constant hiding in the adapter, caught by the 1.5B-no-constants proof |
| `est_work_tokens` | 16k–32k |
| `est_basis` | PML5-U6 oracle-matching proof lowering (12k–24k) scaled for three rows; mostly exempla + receipts on top of U1/U2 |
| `tool_latency` | medium — deterministic generation runs on three real files (minutes each) |

## 5. Checkpoints And Gates

1. **Gate 0 (no start)**: any REF-01 unit is blocked until LIB-02 and LIB-03 receipts are accepted (campaign dependency graph; the delivery authority's `GGUF-A2 + GGUF-A3 → GGUF-A4`).
2. **Gate 1 (after U1)**: full-model prefill logit receipts for SmolLM2 and Qwen2.5-0.5B at first-divergence boundary; shared-primitive surface frozen for `qwen35moe`.
3. **Gate 2 (after U2)**: prefill/decode agreement + reset/reuse receipts; KV-state surface frozen.
4. **Gate 3 (after U3)**: three dense deterministic-text receipts; support matrix shows three executed dense rows.
5. **Audit**: independent auditor verifies receipts against the pinned oracle and checks no special-case constants (grep for row-pinned shapes/sizes in adapters).

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

1. **Qwen-row oracle pin**: gi0-comparator-contract pins llama.cpp 10150 / `dee2a846b` for the SmolLM2 row. The same toolset supports `qwen2` (verified in the live llama.cpp tree); no separate comparator-contract revision exists for the Qwen rows. Default for U1/U3: reuse the same pinned binary under the same comparison policy; if a per-row comparator revision is required, that is a campaign-level amendment, not a REF-01 unit.
2. **Module names**: U1/U2 write_scope uses `dense.fab` / KV-state module names as placeholders; the authoritative module map and naming live with the delivery/Gradus architecture ownership (the delivery authority names operations, not files). Mind/admission confirms module placement.
3. **`est_work_tokens` basis**: estimates are derived from prior gradus lowerings (8k–24k per unit) scaled for full-model generality. If admission wants tighter bounds, the auditor's task-body review (campaign execution rule 3) is the natural checkpoint.
4. **Faber binary**: `check-compile` requires a lane-local faber binary (FABER_BIN); the pinned public faber `1fb6cc97e66d` tree is present, and the main radix debug binary exists at `/Users/ianzepp/work/faberlang/radix/target/debug/faber`. The implementing Hand's packet must name the exact binary and locale-pack wiring (locale `la` pack validation must pass).

## 9. Closeout Commands (per unit, from the Hand packet)

```bash
# structural gates (all three units)
cd /Users/ianzepp/work/faberlang/worktrees/<lane>/gradus
./scripta/check-source
env FABER_LIBRARY_HOME=<lane home> \
  FABER_BIN=<lane-local faber binary> ./scripta/check-compile
git diff --check -- src/model docs/module-map.md docs/api-reference.md \
  docs/diagnostics.md docs/regression-corpus.md \
  docs/factory/production-ml-library/pml0-support-matrix.md

# U1: first-divergence receipt per dense row (SmolLM2, Qwen2.5-0.5B)
# U2: prefill/decode agreement + reset/reuse receipts
# U3: deterministic-text receipt per row (SmolLM2, Qwen2.5-0.5B, Qwen2.5-1.5B)
```

**Expected observed result**: `check-source` and `check-compile` exit 0; `git diff --check` silent; each receipt prints the comparison policy, the exact command + working directory, Gradus/radix/faber/hosts revisions, model filename + byte length + SHA-256, tokenizer identity and prompt hash, hardware/OS/backend (CPU/reference), observed token ids and decoded text, first divergence (none expected on declared windows), and — for U2 — reset/reuse and cancellation facts. No receipt claims Metal/CUDA execution or full-model payload residency.

**First implementation frontier**: after LIB-02 + LIB-03 receipts are accepted, the first Hand task is REF-01-U1 (GGUF-A4) — dense Llama/Qwen primitives and full model — starting from `gradus/src/model/` with the gguf_manifest descriptor/range surface as input.
