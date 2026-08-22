# Gradus Regression Corpus

**Version**: `gradus-regression-corpus v1.10.0` (2026-08-22 — MODEL-02 MoE router/expert/full-layer suites and pinned fixtures added after the U6 surface landed at `b1ccfc8`; merged REF-01-U1.8 dense-model assembly + MODEL-01 qwen35moe admission: the full-graph logits (embedding gather → 2 ordered U1.5 blocks → final RMSNorm → output projection) for a synthetic T=2/D=16/vocab-8 config with tied + untied embedding rows + exempla `dense-model` executed proof (37 PASS / 0 FAIL); REF-01-U1.5 — generic dense block pins: the ordered block composition (input RMSNorm → GQA causal+RoPE → residual → post-attn RMSNorm → SwiGLU → residual) over a synthetic T=2/D=16 config + exempla `dense-block` executed proof (32 PASS / 0 FAIL); REF-01-U1.4 — multi-head GQA attention pins: GQA n_h=14/n_kv=2 + MHA n_kv=n_h config rows + exempla `dense-gqa`; REF-01-U1.3 configurable RoPE pins + exempla `dense-rope`; REF-01-U1.2 `nn` SiLU/SwiGLU pins + `exempla/dense-swiglu` executed proof; REF-01-U1.1 RMSNorm pins + `exempla/dense-rmsnorm`; REF-01-U1.6 `dense_llama` llama adapter descriptor-resolution pins + `exempla/dense-llama-adapter`; REF-01-U1.7 `dense_qwen2` qwen2 adapter pins; MODEL-01 — qwen35moe architecture admission pins + M1 `gguf_manifest` typed accessors + the guarded real-file admission receipt (M7); LIB-03 GGUF-A3 C1/C2-U5 — `tensor_payload` / `tensor_view` suites + union-set dequant goldens)
**Repo**: gradus. **Tier**: structural inventory.
**Delivery**: `docs/factory/production-ml-library/pml6-delivery.md` §PML6-U4;
GGUF-A1b delivery in `pml5-general-gguf-delivery.md`.
**Support rows**: `docs/factory/production-ml-library/pml0-support-matrix.md`
(the admitted rows, including the MODEL-02 component-tier row). **Tolerances**: `docs/numeric-tolerances.md`.
**Benchmark method**: `docs/benchmark-method.md`.

This document inventories the **admitted fixtures and proba pins** that
form the Gradus regression corpus. The corpus **is** the co-located
`src/**/*.proba` surface plus the committed fixtures under `fixtures/`
and the named structural consumers — not a separate harness.

**Structural green** means: `./scripta/check-source` and
`./scripta/check-compile` exit 0, and the pin greps in §5 resolve.
**No executed proba run is claimed here.** Executed regression is
auditor-owned at the FMIR-lever gate (CTO8-1 / CTO8-3); one pass at
closeout, never a dev-loop suite.

---

## 1. What counts as the corpus

| Layer | Path | Role |
| --- | --- | --- |
| Co-located package tests | `src/*.proba`, `src/model/*.proba` | Compile-level contract + oracle pins per module |
| Model / tokenizer fixtures | `fixtures/safetensors/`, `fixtures/gguf/`, `fixtures/tokenizer/` | Legal fixtures + row-oracle docs, including the three GGUF-A1a manifest fixtures and the GGUF-A3 union-set dequant goldens (`gguf-dequant-goldens.json` + derivation contract) |
| Exempla consumers | `exempla/gradient-seam`, `exempla/gradient-seam-nolib`, `exempla/training-loop-mlp`, `exempla/token-generation`, `exempla/gguf-manifest`, `exempla/gguf-inspect`, `exempla/qwen36-35b-inference`, `exempla/dense-rmsnorm`, `exempla/dense-swiglu`, `exempla/dense-llama-adapter`, `exempla/dense-qwen2-adapter`, `exempla/dense-block`, `exempla/dense-model`, `exempla/dense-prefill-smollm2`, `exempla/dense-prefill-qwen2`, `exempla/gguf-admit-qwen35moe`, `exempla/moe-probe` (MODEL-02-U7 adapter handoff) | Public-surface consumers plus the executed GGUF synthetic proof (40 PASS / 0 FAIL), guarded six-file local inspection receipt, the capstone tokenizer-phase run (LIB-02-U4-1), the REF-01-U1.1 RMSNorm executed proof (32 PASS / 0 FAIL), the executed REF-01-U1.2 SiLU/SwiGLU proof (14 PASS / 0 FAIL), the REF-01-U1.6 llama-adapter executed proof (19 PASS / 0 FAIL), the qwen2 adapter executed proof (23 PASS / 0 FAIL, REF-01-U1.7), the REF-01-U1.5 dense-block executed proof (32 PASS / 0 FAIL), the REF-01-U1.8 dense-model assembly executed proof (37 PASS / 0 FAIL, tied + untied rows + the fail-closed rejection row), the REF-01-U1.9 compiled-route consumer `dense-prefill-smollm2` (FINAL stop at radix `2ed9914e4` / faber `b1adfc9`: packet faber green; rust emit reaches cargo; rustc 258 errors, first `cast cannot be followed by a method call` — no executed logits), the REF-01-U1.10 Qwen2.5-0.5B prefill consumer (FINAL stop at radix `2ed9914e4`: packet `faber` green; PKG001 closed; rustc cargo-101, first `E0015` const `vec!`; prior PKG001 at `3853d4b8f`, E0432 at `b919052f0`, `CODEGEN001` on `7863624e2`), and the guarded real-file qwen35moe admission receipt (MODEL-01-M7) |
| Admission conformance | `tests/admission_conformance.fab` | Capsule admission composition check |

Nested package dirs follow the Agents rule (≥2 modules); model package
tests live under `src/model/`.

---

## 2. Proba inventory (structural)

Live co-located suites (32 files):

| Suite | Module / surface | Pin class (summary) |
| --- | --- | --- |
| `src/dtype.proba` | `gradus:dtype` | Tag / cast / promote exact + typed errors |
| `src/shape.proba` | `gradus:shape` | Broadcast / reshape / product fail-closed |
| `src/tensor.proba` | `gradus:tensor` | Construction, index, rank errors |
| `src/math.proba` | `gradus:math` | Tensor-aware math foundation |
| `src/serialize.proba` | `gradus:serialize` | Wire round-trip; `_be4_lege` / `_be8_lege` readers |
| `src/parameter.proba` | `gradus:parameter` | Identity + version schema |
| `src/nn.proba` | `gradus:nn` | GELU / layernorm / linear / **rmsnorm** — f64 pins @ **5e-4** (RMSNorm rows: unit scale, per-feature scale, per-row `[2,4]` normalization, sign-preserving negatives — REF-01-U1.1) + **SiLU / SwiGLU (REF-01-U1.2)** — f64 pins @ **5e-4** |
| `src/attention.proba` | `gradus:attention` | SDPA / RoPE — f64 pins @ **5e-4**; configurable RoPE — both pair policies (consecutive-pair freq_base 100000 / interleaved-pair theta 1000000) + scale + fail-closed config (REF-01-U1.3); multi-head GQA — n_h=14/n_kv=2 and n_kv=n_h config rows + typed error contract (REF-01-U1.4) |
| `src/transformer.proba` | `gradus:transformer` | Block + LN3 / IN_LN3 pins @ **5e-4** + **dense block (REF-01-U1.5)** — f64 pins @ **5e-4** (synthetic T=2/D=16/F=16, n_h=4/n_kv=2/head_dim=4 config: input RMSNorm → GQA causal+RoPE → residual → post-attn RMSNorm → SwiGLU → residual) + typed error rows |
| `src/loss.proba` | `gradus:loss` | MSE / CE scalars @ **5e-4** |
| `src/gradient.proba` | `gradus:gradient` | Companion-call contract; oracle pins for runtime gate |
| `src/optimize.proba` | `gradus:optimize` | SGD step pins @ **1e-4** absolute |
| `src/train.proba` | `gradus:train` | Schedules @ **5e-4**; seeds; checkpoint; U6 trajectory |
| `src/metrics.proba` | `gradus:metrics` | Accuracy / metric record |
| `src/tokenizer.proba` | `gradus:tokenizer` | Identity + **`is_eog` {0,2}** + EOG admission rejects + **LIB-02-U2 byte-level BPE word oracle** (`transformers` → `[4549, 382]`, `สวัสดี` → `[34469, 168607]`, `人工智能` → `[109015]`, decode round-trips, typed error rows) + **LIB-02-U3 composed full-prompt oracle** (scanner + special/EOG/BOS/chat policy rows, Probe A/B exact id lists §4.8) |
| `src/decode.proba` | `gradus:decode` | Logits @ **5e-4**; **tokens `[0]` / `[1,1]`**; reset/replay; first-token-divergence |
| `src/cache.proba` | `gradus:cache` | KV identity + `redintegra` |
| `src/sampling.proba` | `gradus:sampling` | Softmax / filters @ **5e-4** |
| `src/generation.proba` | `gradus:generation` | Config + cursor limits + `cursor_redintegra` |
| `src/gradus.proba` | facade composition | MLP / GELU composition @ **5e-4** |
| `src/model/capsule.proba` | capsule admission (schema 2) | Schema-2 admission (identity + manifest) + **schema-1 rejection** (`SchemaVetus`) + identity wire |
| `src/model/safetensors.proba` | Safetensors row | Fixture bytes + digest + tokenizer mismatch |
| `src/model/gguf.proba` | GGUF row | Builder + digest + row facts |
| `src/model/dequant.proba` | CPU dequant — union set | Block layout pins + fail-closed gates for the union set {F32, F16, BF16, Q5_0, Q8_0, Q4_K, Q5_K, Q6_K}; F16 f64-oracle pins (1.0 / 65504.0); NaN half/bf16 rejects |
| `src/model/tensor_payload.proba` | `gradus:model/tensor_payload` (GGUF-A3 C2-U2) | TensorPayload carries the exact stored range facts (name, absolute start, length) + bounded byte list; PayloadError → message render path type-checks |
| `src/model/tensor_view.proba` | `gradus:model/tensor_view` (GGUF-A3 C2-U3/U4/U5) | `links` fail-closed bind (UnknownName / BadRange / BadLength / UnknownLayout / UnknownDtype); windowed `materialize_slice` + single-block `materialize_block` fail-closed rows |
| `src/model/artifact.proba` | pathless content identity | Algorithm, digest, and positive-length validation |
| `src/model/dense_llama.proba` | `gradus:model/dense_llama` (REF-01-U1.6) | Frozen SmolLM2-360M config facts; every canonical name resolves to the exact descriptor facts the A1b inspect surface reports for the real SmolLM2 file (name, shape, layout); fail-closed typed rejection rows (unknown canonical, out-of-range layer, missing tensor, unknown layout) |
| `src/model/gguf_manifest.proba` | GGUF-A1b manifest and range seam | Unknown codec inspection, exact ranges, source failure, checked tensor fragments, and LIB-02-U1 tokenizer array pins (248320 tokens / 247587 merges / special ids) |
| `src/model/dense_qwen2.proba` | `gradus:model/dense_qwen2` (REF-01-U1.7) | qwen2 adapter descriptor-resolution pins — every canonical name resolves to the exact A1b descriptor facts for the Qwen2.5-0.5B row (layer 0 + layer 23, tied + untied `lm_head`), the frozen config render (`24/14/2/64/896/151936/1000000`), and the fail-closed rejection rows (unknown name / suffix, layer range, missing tensor, non-qwen2 arch) |
| `src/model/dense.proba` | `gradus:model/dense` (REF-01-U1.8) | Full-graph logit pins for the small synthetic dense config (T=2, D=16, F=16, H=4, K=2, head_dim=4, vocab 8, tokens `[0, 7]`) — tied and untied embedding rows, f64 references @ **5e-4** (zero same-shape biases, the assembly's synthesized-bias contract) — plus the fail-closed typed-error rows (missing canonical tensor, token out of range, invalid config, shape contradiction, positions mismatch) |
| `src/model/qwen35moe.proba` | `gradus:model/qwen35moe` (MODEL-01) | qwen35moe architecture admission pins: frozen config rows + 55-entry metadata count + mutation family 1 (M3); canonical 753-tensor map + 41-block schedule + storage distribution + families 2–5 (M4); dimension/storage cross-reference validation (M5); identity precondition + seven-family typed refusal matrix (M6) |
| `src/model/moe.proba` | `gradus:model/moe` (MODEL-02-U3…U6) | MoE fail-closed configuration/carrier/window/non-finite rows; router logits, stabilized softmax, deterministic lowest-index ties, top-k renormalization; bounded rank-3 expert dispatch; hand-computed full-layer weighted accumulation plus gated shared expert |

Every suite header states **EVIDENCE HONESTY (CTO Q2)**: structural /
compile-level proof; executed value-identity deferred.

---

## 3. Fixture inventory (admitted rows)

| Fixture / oracle | SHA-256 (where pinned) | Support-matrix row |
| --- | --- | --- |
| `fixtures/safetensors/smollm2-360m-scaled-row.safetensors` | `992426b54e8d7a1b7e24e4167a92a5e630bb79ef7e89efdd5fd2cb2b29d0a0bc` | Row 1 — Safetensors admission |
| `fixtures/safetensors/safetensors-row-oracle.md` | (doc) | Row 1 oracle |
| `fixtures/gguf/smollm2-360m-scaled-row.gguf` | `d89c9ef917158bfb5600f417020479499c6c042f728e9a29c8457a6b1a8f0974` | Row 2 — GGUF admission; also feeds Row 4 |
| `fixtures/gguf/gguf-row-oracle.md` | (doc) | Row 2 oracle |
| `fixtures/gguf/llama-manifest-v3.gguf` | `68a950bb21b44d93f52136cbfcf561796cdd8f1105edc35ddbab957a413dd38b` | GGUF-A1a default-alignment manifest fixture |
| `fixtures/gguf/qwen2-manifest-v3.gguf` | `8c8fc4952a283bde5c21b8bad88f09ca2061649f536477ca40946ceeea404822` | GGUF-A1a non-default-alignment/rank-3 fixture |
| `fixtures/gguf/qwen35moe-manifest-v3.gguf` | `0569265f0ff43f9de50ee067af182ef21cc1242ab6fd0fa940e6a9c4b7676d48` | GGUF-A1a unknown-type/rank-3 fixture |
| `fixtures/gguf/gguf-moe-probes.json` | (committed deterministic fixture) | MODEL-02-U1 hidden-state probe vectors for layers 0, 3, 39, and 40 |
| `fixtures/gguf/gguf-moe-synthetic.json` | (committed synthetic fixture) | MODEL-02-U1 exact-tie and multi-expert router cases |
| `fixtures/gguf/gguf-moe-goldens.json` | (committed oracle) | MODEL-02-U2 per-layer/probe router, expert, shared-gate, and final-FFN values; schema `gguf-moe-goldens-v1` |
| `fixtures/gguf/gguf-moe-goldens-oracle.md` | (doc) | MODEL-02-U2 oracle derivation, artifact identity, llama.cpp pin, and numeric band |
| `fixtures/gguf/general-manifest-oracle.md` | (doc) | GGUF-A1a manifest fixture oracle |
| `fixtures/gguf/gguf-dequant-goldens.json` | `be6cafd7554e60ecc33af20b1f138380edb270749af050ab3588dd0a4487c162` | GGUF-A3 union-set dequant goldens (schema `gguf-dequant-goldens-v2`; 52 blocks — 15 real + 37 adversarial); supports Row 2 + `src/model/dequant.proba` |
| `fixtures/gguf/gguf-dequant-goldens-oracle.md` | (doc) | GGUF-A3 goldens derivation contract (llama.cpp `ggml-quants.c` @ `a957b7747`, generator command, SHA-256 pins) |
| `fixtures/tokenizer/tokenizer-identity-oracle.md` | (doc; P1–P11 id lists) | Tokenizer identity for rows 1–2, 4, 6 |

Generator helpers (`fixtures/*/gen_fixture.{fab,py}`) rebuild synthetic
fixtures; they are not themselves admission evidence.

Architecture / training / inference rows (matrix rows 3–6) use
**synthetic fragment data + proba pins** rather than model-file fixtures
(see each row's `legal fixture ref` in the support matrix).

---

## 4. Named pins (must not silently drift)

These pins are the load-bearing regression contracts called out by
PML6-U4 / the correctness wave. Loss of any pin is a corpus defect.

### 4.1 EOG-stop greedy tokens `[0]`

| Field | Value |
| --- | --- |
| **Pin** | Greedy bounded generation emits **`[0]`** (length 1), not `[0,0]` |
| **Why** | First drawn token `0` is an admitted EOG token; EOG-stop terminates (`0d50d60`) |
| **EOG set** | `{0, 2}` via `tokenizer.is_eog` |
| **Ceiling** | `maxima_verborum` is a ceiling, never a promise of exact length |
| **Live** | `src/decode.proba` — `"the greedy bounded run (temp 0) draws the f64-oracle tokens [0] ..."` |
| **Consumer doc** | `exempla/token-generation/README.md` |

### 4.2 Seeded stochastic tokens `[1, 1]`

| Field | Value |
| --- | --- |
| **Pin** | Seeded run emits **`[1, 1]`** (length 2) |
| **Seed** | `8742514861359412281` |
| **Config** | `temperatura 1.0`, neutral top-k / top-p / min-p / penalty; `maxima_verborum 2` |
| **Why** | No EOG token in the draw — runs to the cursor ceiling |
| **Live** | `src/decode.proba` — `"the seeded stochastic bounded run ... draws the f64-oracle tokens [1, 1]"` |
| **Consumer doc** | `exempla/token-generation/README.md` |

### 4.3 Capsule schema-1 rejection pin (schema-2 boundary)

| Field | Value |
| --- | --- |
| **Pin** | A **schema-1** stamp fails closed at the capsule boundary — the constructor (`construct_manifest`), `verify`, and the identity wire form all reject it |
| **Stamp** | `"1.0.0"` (`F_SCHEMA` is `"2.0.0"`; schema 1 is retired, A1C-M1) |
| **Message class** | `schema 1 is retired — capsule schema is 2.0.0` (`AdmissionError.SchemaVetus`) |
| **Why** | Schema 1 is retired at the schema-2 boundary; a schema-1 call site also fails to compile (the schema-2 constructor has no schema-1 signature) |
| **Live** | `src/model/capsule.proba` — the `"capsule schema-1 rejection"` probandum (`construct_manifest rejects a schema-1 stamp`, `verify rejects a schema-1-stamped capsule`, `deserialization rejects a schema-1-stamped wire`) |
| **Sibling** | `src/tokenizer.proba` rejects `"1,5"` / non-sorted / empty EOG; `is_eog` admits only `{0,2}` — EOG identity lives in `gradus:tokenizer`, not the schema-2 capsule |

### 4.4 Reset / replay determinism

| Field | Value |
| --- | --- |
| **Pin** | Same seed + input → same tokens (two independent runs; `prima_divergentia` = no divergence) |
| **Reset** | `decode.redintegra` / `generation.cursor_redintegra` restore fresh position/context rules |
| **Live** | `src/decode.proba` — `"reset/replay determinism: same seed + input → same tokens"`; PML5-U5 session reset block; `src/generation.proba` cursor reset; `src/cache.proba` cache `redintegra` |
| **Rule** | First-token-divergence comparison only — never text similarity (`src/decode.proba` first-token-divergence probandum) |

### 4.5 Supporting numeric / training pins (corpus, not retuned)

| Pin family | Where | Band / rule |
| --- | --- | --- |
| Forward / logits / sampling | nn / attention / transformer / decode / sampling / loss / gradus | **5e-4** absolute |
| SGD step | `src/optimize.proba` | **1e-4** absolute |
| Train trajectory / schedules | `src/train.proba` (PML4-U6) | **5e-4** + exact resume/seed contracts |
| Gradient companion contract | `src/gradient.proba` + `src/gradient.fab` comments | runtime gate uses policy **1e-4 / 1e-4** |
| Wire / identity / integer | serialize / parameter / dtype / tokenizer lists | exact |

Tolerance policy detail: `docs/numeric-tolerances.md`.

### 4.6 Manifest tokenizer metadata array pins (LIB-02-U1)

| Field | Value |
| --- | --- |
| **Pin** | `texts(m, "tokenizer.ggml.tokens").length()` = **248320**; `texts(m, "tokenizer.ggml.merges").length()` = **247587**; `numbers(m, "tokenizer.ggml.token_type").length()` = **248320** |
| **Special ids** | `tokenizer.ggml.bos_token_id` = **248044** (`<|endoftext|>`), `tokenizer.ggml.eos_token_id` = **248046** (`<|im_end|>`), `tokenizer.ggml.padding_token_id` = **248055** via the scalar `number` surface |
| **Why** | The counts/ids are the frozen target-prefix corpus facts (Qwen3.6-35B-A3B-UD-Q4_K_M.gguf metadata block) that LIB-02-U2/U3 encode/decode must consume |
| **Errors** | Missing keys, non-array values, and wrong element kinds produce typed `GgufManifestError` (`BadWire` / `BadBounds`) rows; duplicate tokenizer keys fail at parse (`DuplicateKey`) |
| **Live** | `src/model/gguf_manifest.proba` — `"LIB-02-U1 tokenizer metadata accessors"` probandum |

### 4.7 Byte-level BPE word oracle (LIB-02-U2)

| Field | Value |
| --- | --- |
| **Pin** | `encoda(t, "transformers")` = **`[4549, 382]`**; `encoda(t, "สวัสดี")` = **`[34469, 168607]`**; `encoda(t, "人工智能")` = **`[109015]`**; `decoda` of each pinned id list reproduces the exact input text |
| **Oracle** | llama-tokenize 10150 `dee2a846b` word-level rows on Qwen3.6-35B-A3B-UD-Q4_K_M.gguf (delivery `pml5-lib02-tokenizer-delivery.md`) |
| **Why** | The word-level boundary proves the BPE core (display mapping, ranked merges, vocab lookup, decode) before the U3 pre-tokenizer composes to the full two-probe oracle |
| **Errors** | Unknown/out-of-range ids → `IdIgnotum`; unmappable display characters → `UnknownTrace`; invalid UTF-8 → `BadUtf8`; malformed merge entries → `BadMerges`; non-byte-level manifest model → `UnknownMergeKind` |
| **No hard-coded tables** | The runtime consumes vocab/merges from the manifest; the proba fixture corpus models the pinned rows structurally (pinned tokens at pinned ids + the real merge sequences), committing no artifact bytes |
| **Live** | `src/tokenizer.proba` — `"LIB-02-U2 artifact-backed byte-level BPE core"` probandum |

### 4.8 Full two-probe composition oracle (LIB-02-U3-7)

| Field | Value |
| --- | --- |
| **Pin** | `encoda_promptum_specialia`/`encoda_promptum` of **Probe A** `สวัสดีครับ ผมชื่ออเล็กซ์` = **`[34469, 168607, 153295, 173922, 153380, 22216, 151752, 172769]`** and **Probe B** `你好，世界！今天是2026年8月13日 🎉` = **`[109266, 3709, 96748, 6115, 113128, 17, 15, 17, 21, 95859, 23, 96212, 16, 18, 95971, 10838, 236, 231]`** through the fully composed runtime (scanner + BPE core + special policy + EOG/BOS + chat policy); `decoda` of each pinned id list reproduces the exact prompt |
| **Oracle** | llama-tokenize 10150 `dee2a846b` raw-prompt rows on Qwen3.6-35B-A3B-UD-Q4_K_M.gguf (delivery `pml5-lib02-tokenizer-delivery.md`, probe rows re-ran identical) |
| **Why** | This is the **LIB-02 completion oracle** (Normalized Spec rule 2): the full qwen35 pipeline composes the U3 scanner families, the BPE core, and the policy surfaces to the exact pinned id lists and exact decode round-trips. Probe rows are raw-prompt rows, never through the template |
| **Errors** | Same typed rows as 4.7; a divergent first probe id or decoded character is a **divergence receipt** (campaign rule 5) that names the first divergent id/character and routes the repair — the probe rows never hard-code probe ids |
| **No hard-coded tables** | Probe A runs on a structural fixture `_corpus_proba_a` (pinned tokens at pinned ids, max id 248046 — eos in range, the 38 real ranked merge pairs the BPE applies to the two Thai words, policy metadata present); Probe B reuses the U3-6 chat fixture. No artifact bytes are committed |
| **Receipt** | `fixtures/tokenizer/pinned-probe-oracle.md` — revisions, model identity, prompt hashes (`e30101d6…` / `855d7303…`), tokenizer identity, command, expected vs observed, residuals |
| **Capstone consumer** | `exempla/qwen36-35b-inference` (LIB-02-U4-1) runs the tokenizer phase through the public surface — `fabricare` on the admitted artifact manifest, then `encoda_promptum` for both probes and `decoda` for both id lists — and prints PASS rows when the observed rows equal these pins (raw-prompt rows, never through the template). A divergence names the first divergent id/character and fails closed (campaign rule 5); the exempla never hard-codes probe ids |
| **Live** | `src/tokenizer.proba` — `"LIB-02-U3-7 full two-probe composition + divergence receipts"` probandum |

### 4.9 Configurable RoPE pins (REF-01-U1.3)

| Pin family | Where | Band / rule |
| --- | --- | --- |
| Consecutive-pair (llama NORM) freq_base 100000, pos 1 & 2, dim 4 | `src/attention.proba` + `exempla/dense-rope` | **5e-4** absolute |
| Interleaved-pair (qwen2) theta 1000000, pos 1 & 2, dim 4 | `src/attention.proba` + `exempla/dense-rope` | **5e-4** absolute |
| Scale knob (scale 2.0) + beyond-dim untouched + fail-closed config | `src/attention.proba` + `exempla/dense-rope` | **5e-4** (config rows exact message) |

Pin count: 22 executed PASS rows (`exempla/dense-rope`, 0 FAIL, exit 0) + the
co-located compile-level proba pins.

### 4.10 Multi-head GQA attention pins (REF-01-U1.4)

| Pin family | Where | Band / rule |
| --- | --- | --- |
| GQA config — n_h=14, n_kv=2, head_dim=4 (qwen2 head ratio 14:2 at a compact head_dim), positions [1, 2], rope_dim 4, interleaved-pair theta 1000000 | `src/attention.proba` + `exempla/dense-gqa` | **5e-4** absolute |
| MHA config — n_kv = n_h = 14, positions [0, 0] (RoPE identity), consecutive-pair base 100000 | `src/attention.proba` + `exempla/dense-gqa` | **5e-4** absolute |
| Typed error contract (head counts, packed widths, output projection, positions, rope dim, dtype) | `src/attention.proba` | exact message identity |

Pin count: 228 executed PASS rows (`exempla/dense-gqa` — 224 pinned output
elements + shape/dtype rows, 0 FAIL, exit 0) + the co-located compile-level
proba pins. The reference values are the independent f64 evaluation of the
documented multi-head formula (external Python, cross-checked against
numpy).

### 4.11 Generic dense block pins (REF-01-U1.5)

| Pin family | Where | Band / rule |
| --- | --- | --- |
| Dense block output — synthetic config T=2, D=16, F=16 (MLP hidden), num_heads=4, num_kv_heads=2, head_dim=4, positions [0, 1], rope_dim 4, consecutive-pair (llama NORM) freq_base 100000, scale 1.0, RMSNorm ε=1e-5, dk scale 0.5 | `src/transformer.proba` + `exempla/dense-block` | **5e-4** absolute |
| Typed error contract (dtype, rank, head counts, output projection width, RoPE position) | `src/transformer.proba` | exact message identity |

Pin count: 32 executed PASS rows (`exempla/dense-block` — the 32 pinned
output elements + shape/dtype rows, 0 FAIL, exit 0) + the co-located
compile-level proba pins (representative subset). The reference values are
the independent f64 evaluation of the documented block formulas — input
RMSNorm → GQA attention (causal + RoPE) → residual → post-attn RMSNorm →
SwiGLU MLP → residual — via external Python/numpy (the PML3
`transformer_block` pin precedent).

### 4.12 Dense model assembly pins (REF-01-U1.8)

| Pin family | Where | Band / rule |
| --- | --- | --- |
| Full-graph logits — tied embedding row (lm_head shares the embedding) — synthetic config T=2, D=16, F=16, num_heads=4, num_kv_heads=2, head_dim=4, vocab 8, tokens `[0, 7]`, positions `[0, 1]`, rope_dim 4, consecutive-pair (llama NORM) freq_base 100000, dk scale 0.5, RMSNorm ε=1e-5 | `src/model/dense.proba` + `exempla/dense-model` | **5e-4** absolute |
| Full-graph logits — untied embedding row (lm_head is a separate canonical tensor) | `src/model/dense.proba` + `exempla/dense-model` | **5e-4** absolute |
| Fail-closed typed-error contract (missing canonical tensor, token out of range, invalid config, shape contradiction, positions mismatch) | `src/model/dense.proba` + the executed rejection row in `exempla/dense-model` | exact message identity |

Pin count: 37 executed PASS rows (`exempla/dense-model` — 16 tied logit
pins + 16 untied logit pins + 2 shape/dtype rows + the fail-closed
rejection row, 0 FAIL, exit 0) + the co-located compile-level proba pins
(representative subset + the typed-error rows). The reference values are
the independent f64 evaluation of the documented full-graph formulas —
embedding gather → 2 ordered U1.5 blocks → final RMSNorm → output
projection — via external Python/numpy (the block transcription is first
validated against the pinned dense-block values in §4.11). The full-graph
pins use **zero same-shape biases** for every linear row: the assembly
synthesizes the biases (the llama/qwen2 canonical family carries no bias
weights — the executed same-shape-bias contract of the composed rows).

---

## 5. Structural validation

### 5.1 Always-on gates

```bash
cd /path/to/faberlang/gradus
./scripta/check-source
./scripta/check-compile
```

`check-compile` runs package-aware `faber check` on:

- the gradus library source root,
- `exempla/gradient-seam`,
- `exempla/training-loop-mlp`,
- `exempla/token-generation`,
- `exempla/gguf-manifest`.
- `exempla/gguf-inspect`.

Executed proofs additionally run `exempla/dense-rope` (REF-01-U1.3, 22 PASS /
0 FAIL) and `exempla/dense-gqa` (REF-01-U1.4, 228 PASS / 0 FAIL) through
package MIR.

The GGUF package proof runs through package MIR with the hand-2 Radix binary.
Its receipt exits 0 with 40 PASS lines and 0 FAIL lines across bounded
synthetic parser/range cases. The separate real-file adapter inspected six
operator-local GGUFs and fails if an inspection request enters tensor data.
This is manifest/range evidence only, not tokenizer or inference execution.
The REF-01-U1.1 RMSNorm proof (`exempla/dense-rmsnorm`) runs through package
MIR and exits 0 with 32 PASS / 0 FAIL on the pinned f64 references.
The REF-01-U1.8 dense model assembly proof (`exempla/dense-model`) runs
through package MIR and exits 0 with 37 PASS / 0 FAIL on the pinned
full-graph f64 references (tied + untied embedding rows + the fail-closed
rejection row).

### 5.2 Pin-consistency greps (U4)

```bash
cd /path/to/faberlang/gradus

# Named token pins still in decode + consumer README
rg -n 'draws the f64-oracle tokens \[0\]|draws the f64-oracle tokens \[1, 1\]' \
  src/decode.proba
rg -n '`\[0\]`|`\[1, 1\]`|8742514861359412281' exempla/token-generation/README.md

# Capsule schema-1 rejection (schema-2 boundary)
rg -n 'schema 1 is retired — capsule schema is 2\.0\.0' src/model/capsule.proba
rg -n '1,5' src/tokenizer.proba

# Reset / replay + first-token-divergence
rg -n 'reset/replay determinism|prima_divergentia|first-token-divergence' \
  src/decode.proba

# is_eog binding
rg -n 'is_eog' src/tokenizer.proba src/tokenizer.fab

# Fixture files present
test -f fixtures/safetensors/smollm2-360m-scaled-row.safetensors
test -f fixtures/gguf/smollm2-360m-scaled-row.gguf
test -f fixtures/tokenizer/tokenizer-identity-oracle.md

# Proba count stays the admitted co-located surface
find src -name '*.proba' | wc -l   # expect 32 at this corpus version

# REF-01-U1.8 dense-model pins in the proba + the executed exempla
rg -n 'LG_T_|LG_U_|token id out of range for the embedding|positions must match the token count' \
  src/model/dense.proba
rg -n 'reject-missing|tied_0_0|untied_1_7' exempla/dense-model/src/main.fab

# GGUF-A3 goldens fixtures present
test -f fixtures/gguf/gguf-dequant-goldens.json
test -f fixtures/gguf/gguf-dequant-goldens-oracle.md

# LIB-02-U1 tokenizer metadata pins (counts, special ids, error rows)
rg -n 'TOKENS_PIN|MERGES_PIN|BOS_PIN|EOS_PIN|PAD_PIN|248320|247587|248044|248046|248055' \
  src/model/gguf_manifest.proba
rg -n 'metadata array is not an integer array|metadata value is not a GGUF string array' \
  src/model/gguf_manifest.fab

# MODEL-01 qwen35moe admission suite + exemplum (M8 inventory)
rg -n 'MODEL-01-M6 admission entry point and typed refusal matrix' \
  src/model/qwen35moe.proba
test -d exempla/gguf-admit-qwen35moe
test -f exempla/gguf-admit-qwen35moe/README.md
```

### 5.3 Executed pass (auditor-owned; not claimed by this unit)

When the FMIR lever opens:

1. Auditor runs the cargo-backed `faber test` path over the corpus.
2. Token pins `[0]` and `[1, 1]`, SGD / loss / forward bands, and
   reset/replay are checked as **executed** value-identity under
   `docs/numeric-tolerances.md`.
3. Receipt cites `numeric-policy v1.0.0` where device/FD comparisons
   apply.
4. A single closeout pass is enough; no Hand dev-loop suite is added.

Until then, §5.1–§5.2 are the only green criteria for this document.

---

## 6. Mapping to support-matrix rows

| Matrix row | Corpus evidence (structural) |
| --- | --- |
| 1 Safetensors | `fixtures/safetensors/*`, `src/model/safetensors.proba`, `src/model/capsule.proba` |
| 2 GGUF | `fixtures/gguf/*`, `src/model/gguf.proba`, `src/model/capsule.proba`, `src/model/dequant.proba`, `src/model/tensor_payload.proba`, `src/model/tensor_view.proba` |
| 3 BERT-tiny training arch | `src/nn.proba`, `src/attention.proba`, `src/transformer.proba`, `src/gradus.proba` |
| 4 SmolLM2-360M scaled inference arch | `src/attention.proba`, `src/transformer.proba`, `src/model/dense_llama.proba` + GGUF fixture facts + `exempla/dense-rope` (REF-01-U1.3 executed proof) + `exempla/dense-llama-adapter` (REF-01-U1.6) |
| 5 PML4 training layer | `src/loss.proba`, `src/gradient.proba`, `src/optimize.proba`, `src/train.proba`, `src/metrics.proba`, `exempla/training-loop-mlp` |
| 6 PML5 inference layer | `src/decode.proba`, `src/cache.proba`, `src/sampling.proba`, `src/generation.proba`, `src/tokenizer.proba`, `exempla/token-generation` |
| 7 REF-01 dense reference — RMSNorm | `src/nn.proba` (rmsnorm rows), `exempla/dense-rmsnorm` (32 PASS / 0 FAIL) |

Reject-log rows (R3/R4/R5/R9/R10/R11 and "no executed-identity upgrade")
remain in the support matrix; this corpus does not re-admit them.

---

## 7. Non-goals

- No new proba pins in PML6-U4 (inventory only).
- No executed claims; no GPU performance claims.
- No silent pin rewrite to match a device observation.
- No replacement of the support matrix or claim register.

---

## 8. Versioning

`gradus-regression-corpus v1.5.0`. Adding a suite, fixture, or named pin
bumps this version. Removing or retargeting a named pin (§4) is a
**major** event and must update the support matrix / compatibility
policy in the same change set. (v1.5.0 = MODEL-01-M8: the
`model/qwen35moe` admission suite and the `gguf-admit-qwen35moe` admission
exemplum, inventoried under the corpus contract.)
