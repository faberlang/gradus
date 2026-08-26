# Delivery: MODEL-03 — qwen35moe Hybrid SSM/Attention State (GGUF-M3)

**Status**: delivered 2026-08-26 — MODEL-03 implementation landed on gradus main (module + proba + `exempla/qwen35moe-layer-probe` + docs; §3.5/§7 spec touch-ups folded); executed probe receipt follows in `evidence/`
**Campaign**: `radix/docs/factory/gpu-production-readiness/CAMPAIGN.md` (MODEL-03 mandatory work row)
**Delivery authority**: [`pml5-general-gguf-delivery.md`](pml5-general-gguf-delivery.md) §GGUF-M3
**Control-plane repo**: `radix`; **owning repo (implementation)**: `gradus`
**Repo baselines**: Radix `b6d6e17c8ad7`; Gradus `bc500993c97b`; Hosts `57d659d60430`; public Faber `1fb6cc97e66d`
**Prepared**: 2026-08-13, planner-27 (fresh lowering — derived independently from the campaign, the delivery authority, the live product repos, and the pinned local artifact; no planner-1..19 worktrees, commits, partial artifacts, or cancelled transcripts were read or reused)
**Goal-forge/check**: not required — MODEL-03 is a mandatory unit already shaped by the campaign and the delivery authority; no new goal document is needed. This spec is the implementation-ready delivery artifact.

---

## 1. Interpreted Unit

MODEL-03 is the mandatory campaign unit "Implement hybrid SSM/attention
state" and the delivery-authority unit GGUF-M3:

> Implement the architecture's declared SSM and attention layer schedule,
> convolution/recurrent state, attention KV state, position handling, reset,
> replay, and incremental updates without conflating the two state families.
>
> **Done when**: per-layer prefill and one-token decode state and outputs match
> the independent oracle at the first-divergence boundary; reset and replay are
> deterministic.

The target architecture is `qwen35moe` (Qwen3.6-35B-A3B-UD). Its trunk is 40
text layers in a repeating `[linear_attention ×3, full_attention]` schedule
plus one NextN/MTP block that is loaded but **not executed in the main pass**.
MODEL-03 owns the two state families this schedule requires:

1. **Linear-attention (Gated DeltaNet) state** on the 30 SSM layers — a
   fixed-size recurrent state plus a depthwise-causal-convolution state, with
   data-dependent gates.
2. **Attention KV state** on the 10 full-attention layers — per-layer,
   per-KV-head position state integrated into gated multi-head attention.

It also owns the layer schedule derivation, position handling (multi-section
RoPE), reset/replay semantics, and incremental (one-token) updates that keep
weights and state resident across a session.

### Boundary vs. neighboring units

| Unit | Owns | MODEL-03 does NOT |
| --- | --- | --- |
| LIB-02 / GGUF-A2 | tokenizer runtime | tokenization, special-token policy |
| LIB-03 / GGUF-A3 | packed storage, materialization | storage codecs, payload materialization |
| MODEL-01 / GGUF-M1 | `qwen35moe` admission, tensor map, typed config | admission; consumes its typed config |
| MODEL-02 / GGUF-M2 | MoE router and expert execution | router logits, expert dispatch, FFN math |
| MODEL-03 / GGUF-M3 | layer schedule, SSM/conv state, KV state, position handling, reset/replay, incremental updates | the above |
| MODEL-04 / GGUF-M4 | full-model reference inference | full-model composition, sampling, logits |

The split boundary is the **layer-attention-subblock**: MODEL-03 proves each
layer's attention sub-block (pre-FFN residual stream state and output);
MODEL-02/MODEL-04 own the MoE FFN and full-model composition. MODEL-03 supplies
the state substrate MODEL-04 composes and EXEC-03 keeps resident.

---

## 2. Normalized Spec

### Functional requirements

**F1 — Layer schedule.** Derive, from artifact metadata only, which GGUF block
is SSM, full attention, or MTP, and validate the derived schedule against each
block's tensor inventory. For the pinned artifact: block 0..39, SSM iff
`(i + 1) % full_attention_interval != 0` (full attention at `i ∈ {3,7,…,39}`),
block 40 = MTP. The derivation must also hold for the two other local
`qwen35moe` rows (heretic/ornith, 733 tensors, `block_count` 40). Any block
whose tensor inventory contradicts the derived type fails closed with a typed
diagnostic naming the block and the first contradictory tensor.

**F2 — SSM layer state (never conflated with KV).** A typed recurrent-state
value per SSM layer per sequence: `S ∈ [32, 128, 128]` (value heads × key head
dim × value head dim, `state_size` 128, `time_step_rank` 32) and a typed
convolution-state value (the last `conv_kernel − 1` = 3 channel slices of the
8192-channel qkv space). The Gated DeltaNet update and output path (L2-normed
q/k, head repetition 16→32, sigmoid beta, softplus(alpha + dt_bias) × A decay
gate, gated output RMSNorm over `z` with SiLU, output projection) must follow
the oracle exactly; the exact algebraic form is settled by the first-failing
oracle (§5), not by an independent derivation.

**F3 — Attention KV state.** A typed per-layer KV value on full-attention
layers only: 2 KV heads × 256 per position, with the gated full-attention
semantics (joint Q/gate projection, RMSNorm on Q and K, multi-section RoPE,
sigmoid-gated output, output projection). KV appends one position per decode
step; prefill and one-token decode must agree on logits at the declared
boundary (GGUF-A5 contract applied to the gated form).

**F4 — Position handling.** Multi-section RoPE with sections `[11, 11, 10, 0]`,
`dimension_count` 64, `freq_base` 10,000,000, per the pinned artifact facts.

**F5 — Prefill / one-token decode equivalence.** Running the 40 trunk layers
in prefill over a pinned token sequence must produce, per layer, the same
state and the same attention-subblock output as incremental one-token decode
that replays the same sequence through the state machinery. The comparison is
per layer and per position.

**F6 — Reset and replay.** Fresh-session construction (empty conv state, zero
recurrent state, empty KV, generation counter restart) and deterministic
replay: same pinned prompt, same session identity → identical per-layer state
and outputs. Reset/replay are executed, not merely structural.

**F7 — MTP block recognition.** Block 40 (NextN/MTP) is recognized and
admitted in the schedule, carries its own tensor inventory (`nextn.*`,
full-attention-style q/k/v), and is **not executed in the main trunk pass** —
matching the oracle, which runs only blocks 0..39 in the main graph.

**F8 — Session identity.** The hybrid state carries an identity key covering
model, model version, execution config, tokenizer identity, layer schedule,
per-layer state types, and dtype — mirroring the `IdentitasCache` precedent —
so EXEC-03 can bind two prompts to one resident session without reload.

### Constraints

- **Device neutral.** No device handle, path, file descriptor, or physical
  residency in any Gradus value. The state values are typed logical values.
- **Executed proof required.** Compilation and documentation support the unit
  but do not replace the per-layer oracle agreement.
- **No dual authority.** The schedule and state semantics are owned by this
  unit's modules; MODEL-04 consumes them, it does not re-derive them.
- **No silent F32 expansion claim** and no performance claims (GGUF-M5 owns
  native execution).

### Non-goals

MoE router/expert math (MODEL-02), tokenizer behavior (LIB-02), storage
codecs and materialization (LIB-03), full-model logits/sampling (MODEL-04),
GPU kernels (EXEC-02), native Metal/CUDA execution (GGUF-M5), HTTP, and
serving.

---

## 3. Repo-Aware Baseline

### 3.1 Pinned target artifact (measured 2026-08-13)

Extracted from the exact file `/Users/ianzepp/Ai/models/Qwen3.6-35B-A3B-UD-Q4_K_M.gguf`
with an independent bounded reader (header + metadata + tensor directory only;
no tensor payload read):

| Fact | Value |
| --- | --- |
| Bytes | 22,663,387,424 |
| SHA-256 | `0b21525e972670ed59e1812e170b27c26355381f0656ecc4e25617ece7dac58b` |
| GGUF version / alignment / data offset | 3 / 32 / 10,991,392 |
| Metadata entries / tensors | 55 / 753 |
| Architecture | `qwen35moe` |
| `block_count` / `context_length` / `embedding_length` | 41 / 262,144 / 2048 |
| `attention.head_count` / `head_count_kv` / `key_length` / `value_length` | 16 / 2 / 256 / 256 |
| `rope.dimension_sections` / `dimension_count` / `freq_base` | `[11, 11, 10, 0]` / 64 / 10,000,000 |
| `ssm.conv_kernel` / `state_size` / `group_count` / `time_step_rank` / `inner_size` | 4 / 128 / 16 / 32 / 4096 |
| `full_attention_interval` / `nextn_predict_layers` | 4 / 1 |
| `expert_count` / `expert_used_count` / `expert_feed_forward_length` / `expert_shared_feed_forward_length` | 256 / 8 / 512 / 512 |
| `tokenizer.ggml.model` / `pre` / bos / eos / pad / add_bos | `gpt2` / `qwen35` / 248044 / 248046 / 248055 / false |

The same facts are independently recorded in
[`exempla/gguf-inspect/README.md`](../../../exempla/gguf-inspect/README.md) and
the HF config for the base model (`Qwen/Qwen3.6-35B-A3B`, `layer_types` =
`[linear_attention ×3, full_attention] ×10`, `num_hidden_layers` 40,
`mtp_num_hidden_layers` 1, `linear_key_head_dim` 128, `linear_num_key_heads`
16, `linear_num_value_heads` 32, `linear_value_head_dim` 128,
`linear_conv_kernel_dim` 4, `mrope_section` [11, 11, 10], `partial_rotary_factor`
0.25, `rope_theta` 10,000,000).

### 3.2 Per-block tensor inventory (measured)

- SSM layers (`blk.0`, `blk.1`, `blk.2`, `blk.4`, …): `attn_norm`,
  `attn_qkv` (2048, 8192), `attn_gate` (2048, 4096), `ssm_conv1d` (4, 8192),
  `ssm_dt.bias` (32), `ssm_a` (32), `ssm_beta` (2048, 32), `ssm_alpha`
  (2048, 32), `ssm_norm` (128), `ssm_out` (4096, 2048), `post_attention_norm`.
- Full-attention layers (`blk.3`, `blk.7`, …): `attn_norm`, `attn_q`
  (2048, 8192), `attn_k` (2048, 512), `attn_v` (2048, 512), `attn_q_norm`
  (256), `attn_k_norm` (256), `attn_output` (4096, 2048),
  `post_attention_norm`.
- MTP block (`blk.40`): full-attention-style q/k/v + `nextn.*` tensors
  (`eh_proj`, `enorm`, `hnorm`, shared head norm/head), matching the oracle's
  MTP loader.

### 3.3 Independent oracle

The pinned llama.cpp comparator build **10150** (`dee2a846b`,
`/opt/homebrew/Cellar/llama.cpp/10150`) contains `llama_model_qwen35moe`
(verified in the installed `libllama.dylib`) including the Gated DeltaNet
recurrent path and the NextN/MTP loader. This is the same build lineage as the
GI0 comparator pin (`radix/docs/factory/gpu-inference-gguf/gi0-comparator-contract.md`),
so the oracle exists, is local, and supports the target architecture. The
token/logit comparison policy is the GI0 numeric contract pattern
(`gi0-numeric-contract.md`): greedy top-1 exact agreement, top-k overlap,
finite values, and first-divergence recording — re-derived for the Qwen3.6
row's EOG set `{248046, 248044}` at dispatch (see §5.4).

### 3.4 Local corpus boundary

`/Users/ianzepp/Ai/models/` — operator-local, never committed. Gate row: the
exact Qwen3.6 artifact above. Schedule/stress rows: `heretic-UD-Q6_K.gguf`
(29,308,320,448 B) and `ornith-1.0-35b-Q8_0.gguf` (36,903,138,880 B), both
`qwen35moe`/733 tensors. Dense rows (SmolLM2, Qwen2.5-0.5B/1.5B) are consumed
by GGUF-A4/A5/A6 and are read-only context for this unit.

### 3.5 Live Gradus state

- `src/model/gguf_manifest.fab` + `artifact.fab` (GGUF-A1a/A1b landed): parse,
  `inspect`, `read_fragment`; executed receipts via
  `exempla/gguf-manifest` and `exempla/gguf-inspect`.
- `src/cache.fab` (PML5-U2): single-block structural `KVCache` with append,
  reset, and identity-key wire; **single-block only, no recurrent/conv state** —
  the extension surface for F3, not a substitute for F2.
- `src/attention.fab`, `src/transformer.fab`: static-shape proof primitives;
  no `qwen35moe` module exists (`src/model/qwen35moe.fab` is GGUF-M1's write
  scope).
- Execution: `faber run --target fmir` executes bounded exempla through the
  imported-library seam (proved by the GGUF-A1a/A1b receipts). Historical
  limitation: the stepper could not resolve calls from one library function to
  another (`transformer.fab` note); whether this is fully lifted must be
  re-verified at red-proof time, and if the executed proof is blocked, the
  blocker routes to hand-2/Faber per campaign execution rule 6 — MODEL-03 does
  not work around it.

### 3.6 Hardware / backend authority

MODEL-03 executed proofs run on **burgus** (local Apple Silicon, macOS arm64):
Gradus reference on the CPU reference path; the llama.cpp oracle on Metal
(same machine, pinned build). **CUDA is out of scope for MODEL-03** — native
Metal/CUDA execution is GGUF-M5/CAP-01/CAP-02. No paid infrastructure is
required by this unit.

---

## 4. Stage Graph

Implementation stages, in order. S0–S1 establish the pattern; S2–S4 batch once
the pattern holds; S6–S7 are the executed proof.

```text
S0 layer-schedule authority
  -> S1 conv + recurrent state values (types, mutation, identity)
       -> S2 Gated DeltaNet update and output math
       -> S3 gated full-attention + KV state
       -> S4 position handling (multi-section RoPE)
            -> S5 prefill/decode equivalence, reset, replay, MTP recognition
                 -> S6 pinned llama.cpp per-layer oracle probe harness
                      -> S7 executed per-layer agreement proof + receipts
```

- **S0 — Schedule authority.** New module deriving per-block type from
  metadata and validating against tensor inventory (F1, F7). Write: the
  schedule module + proba. Predecessor: MODEL-01/GGUF-M1 admission output
  (typed config).
- **S1 — State values.** Typed recurrent-state and convolution-state values
  with construction, append/update, reset, identity, and equality (F2, F6,
  F8). Write: state module + proba.
- **S2 — Gated DeltaNet update.** The recurrent update and gated output path
  for one SSM layer (F2). Reference math matches the oracle; first divergence
  recorded at the first layer/position (F5).
- **S3 — Gated attention + KV.** One full-attention layer with KV state on
  the 10 attention layers (F3).
- **S4 — Position handling.** Multi-section RoPE on Q/K for attention layers
  (F4).
- **S5 — Prefill/decode equivalence, reset, replay, MTP.** Executed
  equivalence at the declared boundary; deterministic reset/replay; MTP block
  recognized and excluded from the trunk pass (F5, F6, F7).
- **S6 — Oracle probe harness.** Bounded instrumentation of the pinned
  llama.cpp build (dee2a846b) that dumps the named per-layer tensors
  (`attn_norm`, `q_conv`, `k_conv`, `v_conv`, `gate`, `state_predelta`,
  `conv_output`, `linear_attn_out`, `Qcur`, `Kcur`, `Vcur`, `attn_pregate`,
  `attn_gated`, `attn_output`, pre-FFN residual per layer) for a pinned prompt.
- **S7 — Executed agreement proof.** Per-layer, per-position comparison of
  Gradus state/output vs the probe output under the first-divergence rule;
  receipts committed.

Split boundary (named): MODEL-03 ends at the per-layer attention-subblock
agreement. The MoE FFN and full-model composition are mandatory successors in
MODEL-02/MODEL-04 and are preserved untouched by this graph.

---

## 5. Implementation Work — Hand Task Body

One delivery-sized Hand task, GGUF-M3.

- **One executed outcome**: the 40-trunk-layer per-layer attention-subblock
  state and output of the exact Qwen3.6 artifact match the pinned llama.cpp
  probe for one pinned prefill prompt and one one-token incremental decode,
  at every layer and window position up to the first-divergence boundary;
  reset and replay are deterministic; receipts committed.
- **Predecessor receipts (required before dispatch)**: GGUF-A1c clean break
  (LIB-01), GGUF-A2 tokenizer (LIB-02), GGUF-A3 packed storage (LIB-03),
  GGUF-M1 `qwen35moe` admission and tensor map (MODEL-01), and GGUF-A5 KV
  prefill/decode semantics. MODEL-03 is not executable before MODEL-01's typed
  config exists; the schedule facts it derives are consumed from the admitted
  model, not re-derived from raw metadata.
- **Exact write scope (gradus)**: new `src/model/qwen35moe_state.fab` +
  `qwen35moe_state.proba` (SSM/conv/KV state values, schedule, position
  handling, reset/replay — final file names follow the MODEL-01 module naming
  once it lands); the per-layer probe consumer
  `exempla/qwen35moe-layer-probe/` (faber.toml, src/main.fab, README);
  `docs/module-map.md`, `docs/api-reference.md`, `docs/diagnostics.md`,
  `docs/regression-corpus.md`, and this delivery's status line.
- **Exact write scope (evidence)**: the llama.cpp instrumentation probe +
  comparison script + receipts live outside gradus (trials/radix evidence),
  per the ownership contract — Gradus owns no device or oracle harness.
- **Read scope**: `gradus:model/gguf_manifest` (A1b), `gradus:model/qwen35moe`
  (MODEL-01), `gradus:cache` (PML5-U2 identity precedent), the pinned artifact
  and its tensor directory, the pinned llama.cpp build and the GI0 numeric
  contract.
- **Forbidden scope**: tokenizer (LIB-02), storage/materialization (LIB-03),
  MoE router/expert math (MODEL-02), full-model composition (MODEL-04), GPU
  kernels (EXEC-02), native Metal/CUDA (GGUF-M5), any main-branch integration
  (integration stops at `factory/merge`), and any edit to planner-owned or
  cista content.
- **First failing oracle**: the pinned llama.cpp probe output for the pinned
  prompt — first layer index and first position where Gradus's per-layer state
  or attention-subblock output diverges from the probe (top-1/layer/position
  granularity, never hidden by text-level similarity; finite-value gate
  applies). Oracle version: llama.cpp 10150 (`dee2a846b`), binary SHA-256
  recorded at probe build, same lineage as the GI0 comparator pin.
- **Local corpus boundary**: `/Users/ianzepp/Ai/models/`; gate row the exact
  Qwen3.6 artifact; schedule stress rows heretic/ornith (compile-level only,
  not executed).
- **Hardware/backend authority**: burgus, macOS arm64; Gradus reference on
  CPU; llama.cpp oracle on Metal. CUDA excluded.
- **Closeout command** (from the Hand packet; exact prompt + token window
  frozen at dispatch):
  ```bash
  cd /Users/ianzepp/work/faberlang/worktrees/<hand>/gradus
  ./scripta/check-source
  ./scripta/check-compile
  env FABER_LIBRARY_HOME=<lane-home> FABER_BIN=<lane-radix>/target/debug/faber \
    run --target fmir exempla/qwen35moe-layer-probe -- \
      /Users/ianzepp/Ai/models/Qwen3.6-35B-A3B-UD-Q4_K_M.gguf 10991392 <probe-dump-dir>
  <lane>/trials/compare-per-layer.py <probe-dump-dir> --gate <gate>
  git diff --check -- src/model/qwen35moe_state.fab src/model/qwen35moe_state.proba \
    exempla/qwen35moe-layer-probe docs/module-map.md docs/api-reference.md \
    docs/diagnostics.md docs/regression-corpus.md
  ```
  (the exempla resolves the artifact path + GGUF data offset + dump dir from
  argv; the data offset is the pinned 10,991,392 constant)
- **Expected observed result**: `check-source` and `check-compile` exit 0;
  the per-layer comparison reports agreement at every layer and position up to
  the first-divergence boundary with `DIVERGENCE=none` (or a named first
  layer/position + failing thresholds, recorded honestly); reset/replay
  determinism probes pass; `git diff --check` silent; receipts committed in
  evidence.
- **est_work_tokens**: 36k–72k.
- **valid est_basis**: landed Gradus units — GGUF-A1a (parser + fixtures +
  exemplar + receipts) at 15k–30k and PML5-U6 (aggregate oracle proof) at
  12k–24k — are the nearest precedents; MODEL-03 adds two state families,
  schedule derivation, position handling, and a pinned oracle-probe harness,
  making it the largest single semantic unit in the reference stack. The upper
  half covers probe-harness friction (build from pinned source, dump plumbing,
  comparison script).
- **Tool latency**: medium–high — `check-source`/`check-compile` ≈ 1–3 min;
  each oracle probe loads the 22.6 GB artifact (Metal) ≈ minutes; executed
  fmir probe runs are seconds.
- **Stop conditions**: pause and route the affected edge when — the target
  identity does not match; the pinned oracle cannot load the artifact; the
  FMIR stepper/library-import seam cannot execute the required value proofs
  (route to hand-2/Faber); a required `qwen35moe` fact cannot be represented;
  the executed proof would require a device handle in a Gradus value, unapproved
  paid infrastructure, or a main-branch write.

---

## 6. Checkpoints And Gates

- **Batching / Split Decision**: split on named boundaries. MODEL-03 is one
  unit (never split from MODEL-02/MODEL-04); within the unit, S0–S1 establish
  the pattern, then S2–S4 batch, and S6–S7 are the executed proof. No parallel
  Hand lanes: the state families share the schedule module, so write surfaces
  are not disjoint.
- **Release posture**: `defer-release` — this unit changes no user-visible or
  package surface; it is an admitted campaign unit whose evidence feeds
  MODEL-04 and closeout. No version bump, changelog entry, or migration note.
- **Correctness gate**: the executed per-layer agreement under the
  first-divergence rule is the unit's completion proof; red-green applies
  (red proof before implementation against the not-yet-present hybrid state
  surface, mirroring GGUF-A1a's red proof).
- **Cleanliness checks**: state-family types remain separate; no dual schedule
  authority; no device handle; regression-corpus totals updated under the
  corpus contract.

---

## 7. Validation

```bash
cd gradus && ./scripta/check-source && ./scripta/check-compile
cd gradus && ./scripta/check-factory-goal-status --fail-on error
```

Unit-level: new `.proba` suites (schedule derivation, state mutation,
prefill/decode equivalence, reset/replay determinism, identity round-trip);
the executed per-layer probe comparison (§5 closeout); `docs/regression-corpus.md`
suite/fixture totals bumped under the corpus contract.

---

## 8. Companion Skill Plan

- `red-green` — red proof first (focused failing cases for schedule, state
  mutation, equivalence), then green.
- `polish` — single-pass closeout over the modified primary source files.
- `delivery`/`factory` — this spec is the delivery input; execution runs as a
  factory phase through the admitted task body.

---

## 9. Open Questions

1. **Per-layer oracle mechanism** (dispatch-time): recommend building the
   bounded instrumentation probe from the pinned llama.cpp source (dee2a846b)
   using the existing graph `cb()` hooks. If that is not feasible in the
   dispatch window, the fallback is full-model first-divergence attribution
   plus per-layer self-consistency — but that fallback must be accepted by the
   delivery audit before it replaces the probe.
2. **Qwen3.6 EOG/numeric re-derivation**: the GI0 numeric contract values
   (Δ = 1e-5, top-k ≥ 4/5, EOG set) were derived for SmolLM2; the Qwen3.6 row's
   EOG set (`{248046, 248044}`) and band must be re-derived against the pinned
   comparator at dispatch before the comparison policy is frozen.
3. **Stepper capability at dispatch**: whether intra-library calls execute
   through FMIR. If blocked, the value proof structure (inline vs composed)
   must be chosen with hand-2 — this is a routing decision, not a MODEL-03
   design change.
4. **Module naming**: final file names for the state module follow MODEL-01's
   `qwen35moe` naming once it lands; this spec's names are the recommended
   shape.

---

## 10. Scope Closure Statement

**Milestone advanced**: Q2 (complete model semantics). MODEL-03's receipt is
one of the Q2 gate's required receipts (M1–M4 plus A4–A6).

**Why unit completion is not campaign completion**: the campaign invariant is
the exact-artifact end-to-end run through one public-Gradus Faber capstone on
Metal and CUDA (`CAP-01`/`CAP-02`), gated by `CLOSE-01`. MODEL-03 proves the
per-layer state substrate only; it does not execute the MoE FFN (MODEL-02),
full-model reference inference (MODEL-04), package/device plans (EXEC-01),
packed kernels (EXEC-02), or resident sessions (EXEC-03). Every mandatory
successor through `CLOSE-01` is preserved by this spec: the state module is
the consumption surface MODEL-04 composes and EXEC-03 binds resident. Nothing
in this lowering narrows, downgrades, defers, makes optional, or moves admitted
Qwen work outside the campaign completion chain.
