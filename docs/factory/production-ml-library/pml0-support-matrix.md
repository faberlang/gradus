# PML0 Support Matrix — full-matrix aggregation

**Admitted by**: PML6-U3 (full-matrix aggregation, `pml6-delivery.md` §PML6-U3).
Rows were admitted by their owning units: PML2-U2/U3 (model-file format rows),
PML3-U5 (architecture rows), PML4 (training-layer row, closeout), PML5
(inference-layer row, closeout). PML6-U3 aggregates every admitted row
(formats, architectures, dtypes, quantizations, shapes, tokenizers, backends)
into this matrix with evidence links.
**Schema version**: `gradus-support-matrix-schema v0.1.0` (2026-08-08, PML0-U5;
kept at v0.1.0 — no field was genuinely needed for the training/inference row
families, per `pml6-delivery.md` Open Question 6).
**Repo**: gradus. **Snapshot**: aggregation at gradus `main` tip `1f4f0d2`
(PML6-U1 re-baseline). Format-row facts are cited from their committed
row-oracle docs (`fixtures/safetensors/safetensors-row-oracle.md`,
`fixtures/gguf/gguf-row-oracle.md`, `fixtures/tokenizer/
tokenizer-identity-oracle.md`), not duplicated.

This matrix holds **admitted rows only**, per `pml0-support-matrix-schema.md`
§2/§3 (fail-closed R1–R11; one row is the unit of support claim). Six admitted
rows: two PML2 model-file format rows (Safetensors, GGUF), two PML3
architecture rows (one training, one selected inference), one PML4
training-layer row, one PML5 inference-layer row. Every row is **structural
tier** — the executed tier is recorded, never claimed (see §2 reject log and
each row's structural-tier note).

GGUF-A1b extends the separate **format-inspection foundation**; it is not an admitted
execution row. `gradus:model/artifact` and `gradus:model/gguf_manifest` parse
bounded GGUF v3 headers, metadata, and tensor directories for `llama`, `qwen2`,
and `qwen35moe` inputs. They preserve unknown architecture names
and raw GGML type IDs as data, honor default/non-default alignment, and do not
admit a model, load tensor payloads, or claim inference. The parser bounds
metadata and tensor directories at 4,096 entries and the retained prefix at
64 MiB, admitting the inventoried local maximum of 753 tensors. The source
and synthetic proof are compile/typecheck evidence, and the package-MIR
exemplar executes 40 bounded parser/range cases with 40 PASS / 0 FAIL through
the hand-2 Radix binary. It also checks all thirteen metadata wire kinds,
exact `valor_wire` bytes, nested arrays, descriptor ranges, and the typed
BOOL `numerum` rejection. A guarded source adapter separately matches six
operator-local real files against independent offsets and counts without
entering tensor data (`exempla/gguf-inspect/README.md`). Neither receipt is a
tokenizer, architecture admission, model execution, or inference claim. The
LIB-02-U1 typed array accessors (`textorum`/`numerorum`, `src/model/gguf_manifest.fab`) read the tokenizer metadata block of a parsed schema-2
manifest — `tokenizer.ggml.tokens` / `tokenizer.ggml.merges` (string arrays)
and `tokenizer.ggml.token_type` (integer array) — with the exact target-prefix
counts (248320 tokens, 247587 merges) and pinned special ids pinned in
`src/model/gguf_manifest.proba`; missing/malformed/duplicate keys return typed
`GgufManifestError` rows. This remains metadata-only evidence for the LIB-02
tokenizer units; it does not implement encode/decode. The
existing Row 2 capsule admission
remains the old one-row authority until GGUF-A1c performs the clean-break
migration.

## 1. Admitted rows

### Row 1 — PML2 Safetensors model-file admission row

```markdown
| `format` | `safetensors` version `1.0.0` (fixture metadata `format.name` / `format.version` — PML2-U2 row facts, `fixtures/safetensors/safetensors-row-oracle.md`) |
| `architecture` | `llama` / `dense` (gi0-model-contract 1.0.0 §2.1 — scaled structural stand-in for SmolLM2-360M-Instruct; scaled model metadata: 1 layer, context 2048) |
| `dtype` | `f32` storage only (F32 dtype set; one-row mapping to the capsule f32 quantization row — `fixtures/safetensors/safetensors-row-oracle.md`) |
| `quantization` | `none` (F32 storage; quantization is the GGUF row's domain) |
| `shape` | model-file shape facts: pinned 5-tensor scaled table `[8,4]`/`[8]`/`[8,8]`/`[8,4]`/`[4,8]` (168 elements, 672 data bytes, all offsets 8-byte aligned, intervals tile exactly) + capsule row ceilings (metadata KV ≤ 64, tensors ≤ 16, per-dimension ≤ 65536, total elements ≤ 1e9, per-string ≤ 4096) |
| `tokenizer identity` | `gpt2` (BPE) pre-tokenizer `smollm`; EOG set `{0,2}`; BOS-free + space-prefix-free (positive facts, correctness wave `6cc0eb5`); vocab fingerprint per `fixtures/tokenizer/tokenizer-identity-oracle.md` (P1–P11 pinned id lists) |
| `legal fixture ref` | `fixtures/safetensors/smollm2-360m-scaled-row.safetensors` — SHA-256 `424442296e97c261de42fd496cc6cdb4496f3f632835479de96a7ed76c5f75d8` (1512 bytes); local synthetic fixture, no acquisition or redistribution claim |
| `oracle ref` | the PML2-U2 row-oracle (`fixtures/safetensors/safetensors-row-oracle.md`): pinned header/data facts (header_size 840, 672-byte data region, deterministic data pattern); the proba embeds the same byte sequence and verifies the capsule digest via `capsula.verifica_contra` (digest value host-computed per the capsule boundary) |
| `evidence links` | `src/model/safetensors.fab`, `src/model/safetensors.proba`, `src/model/capsule.fab`, `src/model/capsule.proba`; `tests/admission_conformance.fab`; `fixtures/safetensors/safetensors-row-oracle.md`; committed units 435ccd6 (U1 capsule), 07291d6 (U2), f12deaf (U4 tokenizer), 02fae61 (U6 conformance) |
| `compatibility policy` | exact admitted row: the pinned SmolLM2-360M scaled Safetensors model-file row admits into the capsule (`capsule-schema-1.0.0`). Non-goals: no other format/version; no quantization (F32 storage only); no forward-path claim (admission row — forward rows are the PML3 rows); no executed identity claim |
| `schema version` | `gradus-support-matrix-schema v0.1.0` |
```

### Row 2 — PML2 GGUF model-file admission row

```markdown
| `format` | `gguf` (GGUF file version 3; file type 15 MOSTLY_Q4_K_M; quant version 2 — PML2-U3 row facts, `fixtures/gguf/gguf-row-oracle.md`) |
| `architecture` | `llama` / `dense` (gi0-model-contract 1.0.0 §2.1 — SmolLM2-360M scaled structural stand-in; 32 layers, context 8192, vocab 49152, embedding 960) |
| `dtype` | `f32` compute; storage is mixed GGML types per tensor (Q8_0, F32, Q4_K) — storage differs from compute; quantization named in the `quantization` field |
| `quantization` | `q4_k_m` (quant version 2; GGUF file type 15; pinned GGML block layout Q8_0 32/34, F32 1/4, Q4_K 256/144; GGML type ids per pinned toolchain llama.cpp `a957b7747` `ggml.h`) |
| `shape` | model-file shape facts: pinned 3-tensor scaled table `[32,16]`/`[16]`/`[256,16]` (4624 elements, 2912 data bytes, every byte length a 32-multiple — data region tiles exactly) + capsule row ceilings (metadata KV ≤ 4096, tensors ≤ 65536, per-dimension ≤ 65536, total elements ≤ 1e9, per-string ≤ 4096) |
| `tokenizer identity` | `gpt2` (BPE) pre-tokenizer `smollm`; BOS/EOS/PAD/UNK = 1/2/2/0; EOG set `{0,2}`; BOS-free + space-prefix-free; vocab fingerprint per `fixtures/tokenizer/tokenizer-identity-oracle.md` |
| `legal fixture ref` | `fixtures/gguf/smollm2-360m-scaled-row.gguf` — SHA-256 `d89c9ef917158bfb5600f417020479499c6c042f728e9a29c8457a6b1a8f0974` (3936 bytes); local synthetic fixture, no acquisition or redistribution claim |
| `oracle ref` | the PML2-U3 row-oracle (`fixtures/gguf/gguf-row-oracle.md`): pinned header/tensor-table/data facts (metadata KV count 18, data-section start 1024, deterministic data pattern); the proba reconstructs the same byte sequence in code (`aedifica` builder) and verifies the capsule digest via `capsula.verifica_contra` |
| `evidence links` | `src/model/gguf.fab`, `src/model/gguf.proba`, `src/model/capsule.fab`, `src/model/capsule.proba`; `tests/admission_conformance.fab`; `fixtures/gguf/gguf-row-oracle.md`; committed units 435ccd6 (U1), b392fc8 (U3), f12deaf (U4), 02fae61 (U6) |
| `compatibility policy` | exact admitted row: the pinned SmolLM2-360M scaled GGUF row (file v3, Q4_K_M storage / f32 compute) admits into the capsule. Non-goals: no quantized forward path (quantization is a storage property of this row, never a forward-path claim); no other file versions/types/quants; no executed identity claim |
| `schema version` | `gradus-support-matrix-schema v0.1.0` |
```

### Row 3 — Training architecture row: BERT-tiny fragment transformer block (PML3-U5)

```markdown
| `format` | no model-file format claimed by this row — forward-architecture row over the admitted parameter schema (parameter-identity-schema-1.0.0); model-file format rows are the PML2 rows (rows 1–2: `fixtures/gguf/gguf-row-oracle.md`, `fixtures/safetensors/safetensors-row-oracle.md`) |
| `architecture` | `bert-tiny` (dense; the accepted GPU-training proof fragment, B=2 D=8 H=1 — owning spec: the accepted bert-tiny-fragment oracle / `bert_tiny_block_2x8` arithmetic, `pml0-proof-api-ledger.md` row 15) |
| `dtype` | `f32` compute = `f32` storage (the F32 row is the admitted row) |
| `quantization` | `none` (forward path is unquantized; quantized storage is the inference row's domain) |
| `shape` | enumerated fixed shapes: the BERT-tiny fragment (B=2, D=8, H=1 — [2,8] activations, [8] biases/norm params, [8,8] weights, 18 trainable params); plus the shared primitive rows 2x2 / 4x4 / 2x8 (nn.proba) and the MLP 4x4 (gradus.proba forward_mlp); every shape is fixture/oracle-backed |
| `tokenizer identity` | not part of this row — the forward path is tokenizer-free by contract; tokenizer identity is a model-file admission dimension (PML2-U4 row facts / `fixtures/tokenizer/tokenizer-identity-oracle.md`) |
| `legal fixture ref` | no model-file fixture — the row is qualified over the accepted GPU-training proof's fragment parameters and pinned oracle values (synthetic fragment data, no acquisition or redistribution claim) |
| `oracle ref` | the accepted GPU-training proof (bert-tiny-fragment oracle `intermediates.json` step 0, CPU reference); pinned f64 CPU-reference values in `src/transformer.proba` (LN3_*) and `src/nn.proba` within a documented 5e-4 absolute tolerance (approximata); an independent external-Python f64 evaluation of the documented formulas reproduces the pins exactly |
| `evidence links` | `src/nn.fab`, `src/attention.fab`, `src/transformer.fab`, `src/gradus.fab`; tests `src/nn.proba`, `src/attention.proba`, `src/transformer.proba`, `src/gradus.proba`; committed units 9822cfa (U1), 5260049 (U2), 7bf9acc (U3), 359c5f0 (U4) |
| `compatibility policy` | exact admitted combination: BERT-tiny fragment transformer block (pre-LN → QKV → attention → output projection → residual → post-LN → FFN → residual → pre-loss LN) over the F32 staged carrier, forward-only, oracle-matching per above, usable by PML4 training. Non-goals: no other architecture/dtype/shape; no quantized forward; no decode/KV-cache (PML5); no runtime identity claim |
| `schema version` | `gradus-support-matrix-schema v0.1.0` |
```

**U4 partial note (recorded, CTO Q2).** This row's qualification uses the
**structural (compile-level) forward proof**: `gradus.fab` imports no autograd
surface, the shared forward (`forward_mlp`) is a pure value function, and the
training path (`forward_mlp_loss`) requests gradient construction by the single
`@ radix backward` annotation whose generated companion is compile-validated by
`faber check`. **This row does NOT claim executed identity** of bare forward vs
the generated companion, companion behavior, or a numerical bound at runtime —
that claim is deferred to a runtime-evidence gate per CTO Q2 (proba execution
is env-blocked tree-wide today).

### Row 4 — Selected inference architecture row: SmolLM2-360M scaled (llama/dense, Q4_K_M) (PML3-U5)

```markdown
| `format` | `gguf` (GGUF file version 3 — the PML2-U3 admitted GGUF row; `fixtures/gguf/gguf-row-oracle.md`) |
| `architecture` | `llama` / `dense` (the selected inference row from PML2-U3 — SmolLM2-360M scaled row, gi0-model-contract 1.0.0 §2.1 `general.architecture` = `llama`); forward = `transformer_block` modus 2 (causal mask + RoPE) |
| `dtype` | `f32` compute (the admitted F32 forward row); storage dtype is the Q4_K_M quantized GGUF row (storage differs from compute) |
| `quantization` | `q4_k_m` (quant version 2; GGUF file type 15 MOSTLY_Q4_K_M — PML2-U3 row facts) |
| `shape` | forward-qualified shapes: `transformer_block` modus 2 over the fragment B=2 D=8 with RoPE positions [0,1], dim 2 (IN_LN3 pins, `src/transformer.proba`); model-level facts from the PML2-U3 row: 32 layers, context 8192, vocab 49152, embedding 960 (scaled tensor table [32,16]/[16]/[256,16]) |
| `tokenizer identity` | `gpt2` (BPE) pre-tokenizer `smollm`; BOS/EOS/PAD/UNK = 1/2/2/0; EOG set {0,2}; BOS-free + space-prefix-free; vocab fingerprint per PML2-U3/U4 (`fixtures/tokenizer/tokenizer-identity-oracle.md` — digest is host-computed at admission) |
| `legal fixture ref` | `fixtures/gguf/smollm2-360m-scaled-row.gguf` — SHA-256 `d89c9ef917158bfb5600f417020479499c6c042f728e9a29c8457a6b1a8f0974`; scaled structural stand-in for SmolLM2-360M-Instruct-Q4_K_M of gi0-model-contract 1.0.0; local synthetic fixture, no acquisition or redistribution claim |
| `oracle ref` | GI3 frozen recipes (read-only facts): CausalMaskedSoftmax (row i attends columns j ≤ i, diagonal included — no mask tensor) and Rope (llama-arch NORM consecutive-pair rotation, freq_base frozen 100000); pinned f64 CPU-reference values in `src/attention.proba` (COS_1/SIN_1) and `src/transformer.proba` (IN_LN3_*) within a documented 5e-4 absolute tolerance; independent external-Python f64 evaluation of the documented formulas reproduces the pins exactly |
| `evidence links` | `src/attention.fab`, `src/transformer.fab`; tests `src/attention.proba`, `src/transformer.proba`; PML2-U3 row facts `fixtures/gguf/gguf-row-oracle.md`; committed units 5260049 (U2), 7bf9acc (U3) |
| `compatibility policy` | exact admitted combination: llama/dense (SmolLM2-360M scaled) transformer block with causal + RoPE attention over the F32 staged carrier, forward-only, oracle-matching per above, shared with the training row's forward semantics (the same `transformer_block` composes both paths). Non-goals: no quantized forward (Q4_K_M is storage); no decode/KV-cache/sampling (PML5); no other architectures/dtypes/shapes; no runtime identity claim |
| `schema version` | `gradus-support-matrix-schema v0.1.0` |
```

### Row 5 — PML4 training-layer row (structural tier)

```markdown
| `format` | no model-file format claimed by this row — training-layer row over the admitted parameter schema + the PML3 training architecture row (row 3); model-file format rows are the PML2 rows (rows 1–2) |
| `architecture` | `bert-tiny` fragment transformer block (the PML3 training row, row 3) driving the accepted bounded convergence workload — `exempla/training-loop-mlp` over the accepted MLP 4×4 workload (lr 0.1, 100 steps) |
| `dtype` | `f32` compute = `f32` storage (the F32 row is the admitted row) |
| `quantization` | `none` (unquantized training; quantized storage is the inference row's domain) |
| `shape` | enumerated fixed shapes: the MLP 4×4 training workload + the shared primitive rows 2x2 / 4x4 / 2x8 (loss 2×2/4×4/2×8 MSE + logsumexp CE; SGD state on the 2×2/4×4 steps); every shape fixture/oracle-backed |
| `tokenizer identity` | not part of this row — the training layer is tokenizer-free by contract; tokenizer identity is a model-file admission dimension (PML2-U4 row facts / `fixtures/tokenizer/tokenizer-identity-oracle.md`) |
| `legal fixture ref` | no model-file fixture — the row is qualified over synthetic fragment data + the accepted training proof's workload (no acquisition or redistribution claim) |
| `oracle ref` | the accepted training proof's trajectory, pinned (f64) at steps 0/10/25/50/75/99 → 1.576448169383708 / 0.7815377070077427 / 0.4303461875641296 / 0.13848813116166797 / 0.04746405569680761 / 0.017928625511508454; convergence gate `final/initial = 0.01137 < 0.1`; resume + seeded determinism pins — all at the compile level in `src/train.proba` (PML4-U6 section) |
| `evidence links` | `src/loss.fab`, `src/gradient.fab`, `src/optimize.fab`, `src/train.fab`, `src/metrics.fab` + co-located probas (`loss.proba`, `gradient.proba`, `optimize.proba`, `train.proba`, `metrics.proba`); `exempla/training-loop-mlp`; committed units 5f98e8b (U1), e09c79c (U2), 9bebda9 (U3), 4b24c81 (U4), 94d8a94 (U5), fc85de7 (U6) |
| `compatibility policy` | exact admitted combination: the PML4 training layer (losses + gradient-call contract + SGD optimizer state + schedules + train/eval mode + checkpoint resume + metrics + deterministic seeds) over the PML3 training forward row, **structural tier** — compile-level proofs, no executed convergence claim. Non-goals: no executed values (deferred to the auditor-owned runtime-evidence gate); no optimizers/schedules beyond the admitted SGD + warmup/cosine; no quantized training; no runtime identity claim |
| `schema version` | `gradus-support-matrix-schema v0.1.0` |
```

**Structural tier (recorded, not claimed).** This row's qualification is
compile-level: every surface is committed and the accepted-trajectory pins +
ratio gate, resume round-trip, and seeded draws are proba'd at the compile
level. Executed convergence values are env-blocked on the FMIR lever
(`pml4-closeout.md` §Runtime-evidence-gate blockers) and are deferred to the
auditor-owned runtime-evidence gate. **This row does NOT claim executed
identity** or an executed numerical bound.

### Row 6 — PML5 inference-layer row (structural tier, EOG-stop)

```markdown
| `format` | no new model-file format claimed by this row — inference-layer row over the admitted PML2 model-file rows (rows 1–2) + the PML3 selected inference architecture row (row 4) |
| `architecture` | `llama` / `dense` (SmolLM2-360M scaled — the PML3 inference row, row 4); forward = `transformer_block` modus 2 (causal mask + RoPE); decode and prefill (`praefundere`) share the same forward functions |
| `dtype` | `f32` compute (decode logits, sampling, KV values); storage per the admitted PML2 model-file rows (F32 / Q4_K_M) |
| `quantization` | `none` forward (Q4_K_M is storage — the PML2 GGUF row's property, row 2) |
| `shape` | enumerated fixed shapes: one-token decode + prefill over the fragment B=2 D=8; KV-cache per-position sequential append; bounded generation run (greedy + one seeded stochastic config) on the tiny pinned decoder — token pins `[0]` (greedy) / `[1, 1]` (seeded) |
| `tokenizer identity` | `gpt2` (BPE) pre-tokenizer `smollm`; EOG set `{0,2}`; BOS-free + space-prefix-free; vocab fingerprint per `fixtures/tokenizer/tokenizer-identity-oracle.md`; the pinned EOG set is identity — `tokenizator.est_eog` is the EOG-stop binding (correctness wave `0d50d60`; exact EOG admission `2cdc498`) |
| `legal fixture ref` | no new fixture — consumes the admitted PML2 model-file fixtures (`fixtures/safetensors/smollm2-360m-scaled-row.safetensors` SHA-256 `424442296e97c261de42fd496cc6cdb4496f3f632835479de96a7ed76c5f75d8`; `fixtures/gguf/smollm2-360m-scaled-row.gguf` SHA-256 `d89c9ef917158bfb5600f417020479499c6c042f728e9a29c8457a6b1a8f0974`) + the pinned tokenizer probes (P1–P11, `fixtures/tokenizer/tokenizer-identity-oracle.md`) |
| `oracle ref` | GI0–GI2 pinned fixture / llama.cpp-derived oracle (read-only); f64 token pins `[0]` (greedy, EOG-stop) and `[1, 1]` (seeded, f64) with the first-token-divergence rule + reset/replay determinism; f64 logit pins (`src/decode.proba`); per-knob sampling pins (`src/sampling.proba`) |
| `evidence links` | `src/decode.fab`, `src/cache.fab`, `src/sampling.fab`, `src/generation.fab` + co-located probas (`decode.proba`, `cache.proba`, `sampling.proba`, `generation.proba`); `exempla/token-generation`; committed units bdefb5a (U1), 3b2fc9b (U2), b1b01f1 (U3), 56e70f0 (U4), 8cf798a (U5), 1a6abd0 (U6) |
| `compatibility policy` | exact admitted combination: decode + KV-cache + deterministic sampling + the nine-field generation-config contract over the PML3 inference forward row, with EOG-stop semantics (generation terminates after the FIRST admitted EOG token `{0,2}`; `maxima_verborum` is a ceiling, never a promise), **structural tier**. Unsupported llama.cpp-style controls are explicit reject rows, never silently ignored; the generation config is the single authority NGAB5 adapts. Non-goals: no executed-token claims (CTO8-1 named open clause); no server/HTTP/batching/device-handle surface; no other architectures/configs beyond the admitted row |
| `schema version` | `gradus-support-matrix-schema v0.1.0` |
```

**Structural tier (recorded, not claimed).** This row's qualification is
compile-level: decode/KV-cache/sampling/generation surfaces are committed and
the token pins (`[0]` / `[1, 1]`) are proba'd at the compile level with the
first-token-divergence rule + reset/replay determinism. Executed token identity
is env-blocked on the FMIR lever and is a **NAMED OPEN clause** (CTO8-1,
`pml5-closeout.md`) — **this row does NOT claim executed tokens**.

## 2. Reject log (recorded, never support)

| Proposed row | Reject reason (gate) |
| --- | --- |
| Training row with a claimed model-file format | R11 / R10 — the training forward is a parameter-schema forward; claiming a file format would overclaim (no legal model-file fixture exists for the fragment). The row is admitted only as an architecture row over the parameter schema. |
| Inference forward with quantized (Q4_K_M) tensors in the forward path | R4 / R10 — the admitted forward is f32; quantization is a storage property of the PML2-U3 model-file row, not a forward-path claim. |
| Any non-f32 dtype row (f16/bf16) | R3 — only the F32 row is admitted (the F32 row is the admitted row; primitives reject non-f32). |
| Runtime identity claim (bare forward ≡ generated companion, executed) | R9/R11 — no runtime evidence exists (proba execution env-blocked; U4 partial per CTO Q2). Deferred to a runtime-evidence gate; recorded, not admitted. |
| Shapes beyond the enumerated fixed shapes / fragment rows | R5 — every claimed shape must carry fixture/oracle proof; unproven shapes reject. |
| **Executed-identity row for any admitted row** (executed forward≡companion identity, executed convergence values, or executed tokens) | R9/R11 — the structural tier is recorded and **never upgraded**: proba execution is env-blocked on the FMIR lever; executed identity is the auditor-owned runtime-evidence gate (CTO8-1, named open clause). Every row's structural-tier note marks the boundary. |
| A tokenizer-identity row with an EOG set other than the pinned `{0,2}` | R6 / R10 — the pinned EOG set is identity (`2cdc498`): a well-formed-but-different set is a different tokenizer; capsule admission fails closed (`EogMala`). Rows cite the pinned `{0,2}` exactly. |
| A support row wider than one exact admitted combination (e.g. "the library supports GGUF") | R10 / R11 — support is claimed per row, never at the library level; a compatibility policy that implies broader support rejects the row. |

## 3. Relationship to other artifacts

- Row vocabulary (format/architecture/dtype/quantization/tokenizer identity)
  is the PML0-U5 vocabulary; the claim register (`pml0-claim-register.md`,
  PML0-U12) consumes it so claim status never reads as product support (C5).
  The register's §2 rows now mirror these admitted rows as claims with
  committed evidence refs.
- Model-file admission rows (PML2-U2/U3) are recorded in their row-oracle docs
  (`fixtures/safetensors/safetensors-row-oracle.md`,
  `fixtures/gguf/gguf-row-oracle.md`,
  `fixtures/tokenizer/tokenizer-identity-oracle.md`) and aggregated into this
  matrix at PML6 per `pml6-delivery.md` PML6-U3.
- The PML6 gate's "support matrix is the full-matrix aggregation" clause is
  satisfied by these six admitted rows; the phase gate also requires README
  regen + audit 0 findings (planner/Mind-owned at gate).
- Compatibility promises at the row level are each row's `compatibility
  policy` field; `docs/compatibility-policy.md`
  (`compatibility-policy v1.0.0`) is the product-facing aggregate (pre-1.0
  clean-break, private-helper retirement notes, EOG-set identity, one-row
  narrowing) — the row field stays the row-level authority.

## Validation

```bash
cd /Users/ianzepp/work/faberlang/gradus
# 1. Six admitted rows (2 PML2 format, 2 PML3 architecture, 1 PML4
#    training-layer, 1 PML5 inference-layer), each with all 11 schema fields.
grep -c '^| `format`' docs/factory/production-ml-library/pml0-support-matrix.md   # 6
grep -c '^| `schema version`' docs/factory/production-ml-library/pml0-support-matrix.md   # 6
# 2. Committed unit commits + oracle pins cited as evidence links.
grep -c '07291d6\|b392fc8\|f12deaf\|02fae61\|9822cfa\|5260049\|7bf9acc\|359c5f0\|5f98e8b\|e09c79c\|9bebda9\|4b24c81\|94d8a94\|fc85de7\|bdefb5a\|3b2fc9b\|b1b01f1\|56e70f0\|8cf798a\|1a6abd0' docs/factory/production-ml-library/pml0-support-matrix.md   # >= 5
grep -c 'LN3_\|IN_LN3_\|COS_1\|SIN_1\|1.576448169383708\|0.01137' docs/factory/production-ml-library/pml0-support-matrix.md   # >= 1
# 3. Structural tier recorded, never upgraded — no executed-identity claim.
grep -c 'does NOT claim executed' docs/factory/production-ml-library/pml0-support-matrix.md   # >= 3
grep -c 'CTO8-1' docs/factory/production-ml-library/pml0-support-matrix.md   # >= 2
# 4. Fixture pins resolve.
grep -c '424442296e97c261de42fd496cc6cdb4496f3f632835479de96a7ed76c5f75d8' docs/factory/production-ml-library/pml0-support-matrix.md   # >= 1
grep -c 'd89c9ef917158bfb5600f417020479499c6c042f728e9a29c8457a6b1a8f0974' docs/factory/production-ml-library/pml0-support-matrix.md   # >= 1
# 5. Reject log records the full R3/R4/R5/R9/R10/R11 set + the executed-identity
#    and EOG-set rejections.
grep -c 'R3\|R4\|R5\|R9/R11\|R10' docs/factory/production-ml-library/pml0-support-matrix.md   # >= 6
grep -c 'executed-identity' docs/factory/production-ml-library/pml0-support-matrix.md   # >= 1
git diff --check
```
