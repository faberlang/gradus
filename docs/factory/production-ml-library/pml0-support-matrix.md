# PML0 Support Matrix — populated rows

**Admitted by**: PML3-U5 (architecture rows qualified) — `pml3-delivery.md`
**Schema version**: `gradus-support-matrix-schema v0.1.0` (2026-08-08, PML0-U5)
**Repo**: gradus. **Snapshot**: rows are admitted at gradus `main` after the
PML3-U1..U4 units landed (9822cfa, 5260049, 7bf9acc, 359c5f0).

This matrix holds **admitted rows only**, per `pml0-support-matrix-schema.md`
§2/§3 (fail-closed R1–R11; one row is the unit of support claim). PML3-U5
admits the two forward **architecture rows** of the PML3 gate — one training
architecture row and the selected inference architecture row — qualified over
the admitted parameter schema (parameter-identity-schema-1.0.0, PML1-U5):
composable, testable, oracle-matching, forward-only.

The PML2 model-file format rows (one Safetensors row, one GGUF row) were
admitted into the capsule at PML2-U2/U3; their full row facts are recorded in
`fixtures/safetensors/safetensors-row-oracle.md` and
`fixtures/gguf/gguf-row-oracle.md` and are cited below, not duplicated. PML6-U3
(`pml6-delivery.md`) aggregates every admitted row (formats, architectures,
dtypes, quantizations, shapes, tokenizers, backends) into this matrix.

## 1. Admitted rows

### Row 1 — Training architecture row: BERT-tiny fragment transformer block

```markdown
| `format` | no model-file format claimed by this row — forward-architecture row over the admitted parameter schema (parameter-identity-schema-1.0.0); model-file format rows are the PML2 rows (`fixtures/gguf/gguf-row-oracle.md`, `fixtures/safetensors/safetensors-row-oracle.md`) |
| `architecture` | `bert-tiny` (dense; the accepted GPU-training proof fragment, B=2 D=8 H=1 — owning spec: the accepted bert-tiny-fragment oracle / `bert_tiny_block_2x8` arithmetic, `pml0-proof-api-ledger.md` row 15) |
| `dtype` | `f32` compute = `f32` storage (the F32 row is the admitted row) |
| `quantization` | `none` (forward path is unquantized; quantized storage is the inference row's domain) |
| `shape` | enumerated fixed shapes: the BERT-tiny fragment (B=2, D=8, H=1 — [2,8] activations, [8] biases/norm params, [8,8] weights, 18 trainable params); plus the shared primitive rows 2x2 / 4x4 / 2x8 (nn.proba) and the MLP 4x4 (gradus.proba forward_mlp); every shape is fixture/oracle-backed |
| `tokenizer identity` | not part of this row — the forward path is tokenizer-free by contract; tokenizer identity is a model-file admission dimension (PML2-U3 row facts / `fixtures/tokenizer/tokenizer-identity-oracle.md`) |
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
that claim is deferred to a runtime-evidence gate per CTO Q2 (U4 is partial;
proba execution is env-blocked tree-wide today).

### Row 2 — Selected inference architecture row: SmolLM2-360M scaled (llama/dense, Q4_K_M)

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

## 2. Reject log (recorded, never support)

| Proposed row | Reject reason (gate) |
| --- | --- |
| Training row with a claimed model-file format | R11 / R10 — the training forward is a parameter-schema forward; claiming a file format would overclaim (no legal model-file fixture exists for the fragment). The row is admitted only as an architecture row over the parameter schema. |
| Inference forward with quantized (Q4_K_M) tensors in the forward path | R4 / R10 — the admitted forward is f32; quantization is a storage property of the PML2-U3 model-file row, not a forward-path claim. |
| Any non-f32 dtype row (f16/bf16) | R3 — only the F32 row is admitted (the F32 row is the admitted row; primitives reject non-f32). |
| Runtime identity claim (bare forward ≡ generated companion, executed) | R9/R11 — no runtime evidence exists (proba execution env-blocked; U4 partial per CTO Q2). Deferred to a runtime-evidence gate; recorded, not admitted. |
| Shapes beyond the enumerated fixed shapes / fragment rows | R5 — every claimed shape must carry fixture/oracle proof; unproven shapes reject. |

## 3. Relationship to other artifacts

- Row vocabulary (format/architecture/dtype/quantization/tokenizer identity)
  is the PML0-U5 vocabulary; the claim register (`pml0-claim-register.md`,
  PML0-U12) consumes it so claim status never reads as product support.
- Model-file admission rows (PML2-U2/U3) are recorded in their row-oracle docs
  (`fixtures/safetensors/safetensors-row-oracle.md`,
  `fixtures/gguf/gguf-row-oracle.md`) and aggregate into this matrix at PML6
  per `pml6-delivery.md` PML6-U3.
- The PML3 gate's "support rows populated" clause is satisfied by these two
  admitted rows; the phase gate also requires README regen + audit 0 findings
  (planner/Mind-owned at gate).

## Validation

```bash
cd /Users/ianzepp/work/faberlang/gradus
# 1. Two admitted architecture rows, each with all 11 schema fields (§2/§4).
grep -c '^| `format`' docs/factory/production-ml-library/pml0-support-matrix.md   # 2
grep -c '^| `schema version`' docs/factory/production-ml-library/pml0-support-matrix.md   # 2
# 2. Landed unit commits + oracle pins cited as evidence links.
grep -c '9822cfa\|5260049\|7bf9acc\|359c5f0' docs/factory/production-ml-library/pml0-support-matrix.md   # >= 1
grep -c 'LN3_\|IN_LN3_\|COS_1\|SIN_1' docs/factory/production-ml-library/pml0-support-matrix.md   # >= 1
# 3. U4 partial / CTO Q2 deferral recorded — no executed-identity claim.
grep -c 'structural (compile-level) forward proof' docs/factory/production-ml-library/pml0-support-matrix.md   # >= 1
grep -c 'does NOT claim executed identity' docs/factory/production-ml-library/pml0-support-matrix.md   # >= 1
# 4. Fixture pins resolve.
grep -c 'd89c9ef917158bfb5600f417020479499c6c042f728e9a29c8457a6b1a8f0974' docs/factory/production-ml-library/pml0-support-matrix.md   # >= 1
git diff --check
```
