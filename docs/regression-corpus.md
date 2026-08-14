# Gradus Regression Corpus

**Version**: `gradus-regression-corpus v1.3.0` (2026-08-13, A1C-M5;
2026-08-14, LIB-02-U1 tokenizer metadata array pins)
**Repo**: gradus. **Tier**: structural inventory.
**Delivery**: `docs/factory/production-ml-library/pml6-delivery.md` §PML6-U4;
GGUF-A1b delivery in `pml5-general-gguf-delivery.md`.
**Support rows**: `docs/factory/production-ml-library/pml0-support-matrix.md`
(six admitted rows). **Tolerances**: `docs/numeric-tolerances.md`.
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
| Model / tokenizer fixtures | `fixtures/safetensors/`, `fixtures/gguf/`, `fixtures/tokenizer/` | Legal fixtures + row-oracle docs, including the three GGUF-A1a manifest fixtures |
| Exempla consumers | `exempla/gradient-seam`, `exempla/gradient-seam-nolib`, `exempla/training-loop-mlp`, `exempla/token-generation`, `exempla/gguf-manifest`, `exempla/gguf-inspect`, `exempla/qwen36-35b-inference` | Public-surface consumers plus the executed GGUF synthetic proof (40 PASS / 0 FAIL), guarded six-file local inspection receipt, and the capstone tokenizer-phase run (LIB-02-U4-1) |
| Admission conformance | `tests/admission_conformance.fab` | Capsule admission composition check |

Nested package dirs follow the Agents rule (≥2 modules); model package
tests live under `src/model/`.

---

## 2. Proba inventory (structural)

Live co-located suites (26 files):

| Suite | Module / surface | Pin class (summary) |
| --- | --- | --- |
| `src/dtype.proba` | `gradus:dtype` | Tag / cast / promote exact + typed errors |
| `src/shape.proba` | `gradus:shape` | Broadcast / reshape / product fail-closed |
| `src/tensor.proba` | `gradus:tensor` | Construction, index, rank errors |
| `src/math.proba` | `gradus:math` | Tensor-aware math foundation |
| `src/serialize.proba` | `gradus:serialize` | Wire round-trip; `_be4_lege` / `_be8_lege` readers |
| `src/parameter.proba` | `gradus:parameter` | Identity + version schema |
| `src/nn.proba` | `gradus:nn` | GELU / layernorm / linear — f64 pins @ **5e-4** |
| `src/attention.proba` | `gradus:attention` | SDPA / RoPE — f64 pins @ **5e-4** |
| `src/transformer.proba` | `gradus:transformer` | Block + LN3 / IN_LN3 pins @ **5e-4** |
| `src/loss.proba` | `gradus:loss` | MSE / CE scalars @ **5e-4** |
| `src/gradient.proba` | `gradus:gradient` | Companion-call contract; oracle pins for runtime gate |
| `src/optimize.proba` | `gradus:optimize` | SGD step pins @ **1e-4** absolute |
| `src/train.proba` | `gradus:train` | Schedules @ **5e-4**; seeds; checkpoint; U6 trajectory |
| `src/metrics.proba` | `gradus:metrics` | Accuracy / metric record |
| `src/tokenizer.proba` | `gradus:tokenizer` | Identity + **`est_eog` {0,2}** + EOG admission rejects + **LIB-02-U2 byte-level BPE word oracle** (`transformers` → `[4549, 382]`, `สวัสดี` → `[34469, 168607]`, `人工智能` → `[109015]`, decode round-trips, typed error rows) + **LIB-02-U3 composed full-prompt oracle** (scanner + special/EOG/BOS/chat policy rows, Probe A/B exact id lists §4.8) |
| `src/decode.proba` | `gradus:decode` | Logits @ **5e-4**; **tokens `[0]` / `[1,1]`**; reset/replay; first-token-divergence |
| `src/cache.proba` | `gradus:cache` | KV identity + `redintegra` |
| `src/sampling.proba` | `gradus:sampling` | Softmax / filters @ **5e-4** |
| `src/generation.proba` | `gradus:generation` | Config + cursor limits + `cursor_redintegra` |
| `src/gradus.proba` | facade composition | MLP / GELU composition @ **5e-4** |
| `src/model/capsule.proba` | capsule admission (schema 2) | Schema-2 admission (identity + manifest) + **schema-1 rejection** (`SchemaVetus`) + identity wire |
| `src/model/safetensors.proba` | Safetensors row | Fixture bytes + digest + tokenizer mismatch |
| `src/model/gguf.proba` | GGUF row | Builder + digest + row facts |
| `src/model/dequant.proba` | CPU dequant | Block layout pins |
| `src/model/artifact.proba` | pathless content identity | Algorithm, digest, and positive-length validation |
| `src/model/gguf_manifest.proba` | GGUF-A1b manifest and range seam | Unknown codec inspection, exact ranges, source failure, checked tensor fragments, and LIB-02-U1 tokenizer array pins (248320 tokens / 247587 merges / special ids) |

Every suite header states **EVIDENCE HONESTY (CTO Q2)**: structural /
compile-level proof; executed value-identity deferred.

---

## 3. Fixture inventory (admitted rows)

| Fixture / oracle | SHA-256 (where pinned) | Support-matrix row |
| --- | --- | --- |
| `fixtures/safetensors/smollm2-360m-scaled-row.safetensors` | `424442296e97c261de42fd496cc6cdb4496f3f632835479de96a7ed76c5f75d8` | Row 1 — Safetensors admission |
| `fixtures/safetensors/safetensors-row-oracle.md` | (doc) | Row 1 oracle |
| `fixtures/gguf/smollm2-360m-scaled-row.gguf` | `d89c9ef917158bfb5600f417020479499c6c042f728e9a29c8457a6b1a8f0974` | Row 2 — GGUF admission; also feeds Row 4 |
| `fixtures/gguf/gguf-row-oracle.md` | (doc) | Row 2 oracle |
| `fixtures/gguf/llama-manifest-v3.gguf` | `68a950bb21b44d93f52136cbfcf561796cdd8f1105edc35ddbab957a413dd38b` | GGUF-A1a default-alignment manifest fixture |
| `fixtures/gguf/qwen2-manifest-v3.gguf` | `8c8fc4952a283bde5c21b8bad88f09ca2061649f536477ca40946ceeea404822` | GGUF-A1a non-default-alignment/rank-3 fixture |
| `fixtures/gguf/qwen35moe-manifest-v3.gguf` | `0569265f0ff43f9de50ee067af182ef21cc1242ab6fd0fa940e6a9c4b7676d48` | GGUF-A1a unknown-type/rank-3 fixture |
| `fixtures/gguf/general-manifest-oracle.md` | (doc) | GGUF-A1a manifest fixture oracle |
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
| **EOG set** | `{0, 2}` via `tokenizator.est_eog` |
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
| **Pin** | A **schema-1** stamp fails closed at the capsule boundary — the constructor (`structa_manifestum`), `verifica`, and the identity wire form all reject it |
| **Stamp** | `"1.0.0"` (`F_SCHEMA` is `"2.0.0"`; schema 1 is retired, A1C-M1) |
| **Message class** | `schema 1 is retired — capsule schema is 2.0.0` (`AdmissionError.SchemaVetus`) |
| **Why** | Schema 1 is retired at the schema-2 boundary; a schema-1 call site also fails to compile (the schema-2 constructor has no schema-1 signature) |
| **Live** | `src/model/capsule.proba` — the `"capsule schema-1 rejection"` probandum (`structa_manifestum rejects a schema-1 stamp`, `verifica rejects a schema-1-stamped capsule`, `deserialization rejects a schema-1-stamped wire`) |
| **Sibling** | `src/tokenizer.proba` rejects `"1,5"` / non-sorted / empty EOG; `est_eog` admits only `{0,2}` — EOG identity lives in `gradus:tokenizer`, not the schema-2 capsule |

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
| **Pin** | `textorum(m, "tokenizer.ggml.tokens").longitudo()` = **248320**; `textorum(m, "tokenizer.ggml.merges").longitudo()` = **247587**; `numerorum(m, "tokenizer.ggml.token_type").longitudo()` = **248320** |
| **Special ids** | `tokenizer.ggml.bos_token_id` = **248044** (`<|endoftext|>`), `tokenizer.ggml.eos_token_id` = **248046** (`<|im_end|>`), `tokenizer.ggml.padding_token_id` = **248055** via the scalar `numerum` surface |
| **Why** | The counts/ids are the frozen target-prefix corpus facts (Qwen3.6-35B-A3B-UD-Q4_K_M.gguf metadata block) that LIB-02-U2/U3 encode/decode must consume |
| **Errors** | Missing keys, non-array values, and wrong element kinds produce typed `GgufManifestError` (`WireMala` / `LimitesMala`) rows; duplicate tokenizer keys fail at parse (`ClavisDuplicata`) |
| **Live** | `src/model/gguf_manifest.proba` — `"LIB-02-U1 tokenizer metadata accessors"` probandum |

### 4.7 Byte-level BPE word oracle (LIB-02-U2)

| Field | Value |
| --- | --- |
| **Pin** | `encoda(t, "transformers")` = **`[4549, 382]`**; `encoda(t, "สวัสดี")` = **`[34469, 168607]`**; `encoda(t, "人工智能")` = **`[109015]`**; `decoda` of each pinned id list reproduces the exact input text |
| **Oracle** | llama-tokenize 10150 `dee2a846b` word-level rows on Qwen3.6-35B-A3B-UD-Q4_K_M.gguf (delivery `pml5-lib02-tokenizer-delivery.md`) |
| **Why** | The word-level boundary proves the BPE core (display mapping, ranked merges, vocab lookup, decode) before the U3 pre-tokenizer composes to the full two-probe oracle |
| **Errors** | Unknown/out-of-range ids → `IdIgnotum`; unmappable display characters → `VestigiumIgnotum`; invalid UTF-8 → `Utf8Mala`; malformed merge entries → `MergesMala`; non-byte-level manifest model → `ProgeniesIgnota` |
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

The GGUF package proof runs through package MIR with the hand-2 Radix binary.
Its receipt exits 0 with 40 PASS lines and 0 FAIL lines across bounded
synthetic parser/range cases. The separate real-file adapter inspected six
operator-local GGUFs and fails if an inspection request enters tensor data.
This is manifest/range evidence only, not tokenizer or inference execution.

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

# est_eog binding
rg -n 'est_eog' src/tokenizer.proba src/tokenizer.fab

# Fixture files present
test -f fixtures/safetensors/smollm2-360m-scaled-row.safetensors
test -f fixtures/gguf/smollm2-360m-scaled-row.gguf
test -f fixtures/tokenizer/tokenizer-identity-oracle.md

# Proba count stays the admitted co-located surface
find src -name '*.proba' | wc -l   # expect 26 at this corpus version

# LIB-02-U1 tokenizer metadata pins (counts, special ids, error rows)
rg -n 'TOKENS_PIN|MERGES_PIN|BOS_PIN|EOS_PIN|PAD_PIN|248320|247587|248044|248046|248055' \
  src/model/gguf_manifest.proba
rg -n 'metadata array is not an integer array|metadata value is not a GGUF string array' \
  src/model/gguf_manifest.fab
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
| 2 GGUF | `fixtures/gguf/*`, `src/model/gguf.proba`, `src/model/capsule.proba`, `src/model/dequant.proba` |
| 3 BERT-tiny training arch | `src/nn.proba`, `src/attention.proba`, `src/transformer.proba`, `src/gradus.proba` |
| 4 SmolLM2-360M scaled inference arch | `src/attention.proba`, `src/transformer.proba` + GGUF fixture facts |
| 5 PML4 training layer | `src/loss.proba`, `src/gradient.proba`, `src/optimize.proba`, `src/train.proba`, `src/metrics.proba`, `exempla/training-loop-mlp` |
| 6 PML5 inference layer | `src/decode.proba`, `src/cache.proba`, `src/sampling.proba`, `src/generation.proba`, `src/tokenizer.proba`, `exempla/token-generation` |

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

`gradus-regression-corpus v1.3.0`. Adding a suite, fixture, or named pin
bumps this version. Removing or retargeting a named pin (§4) is a
**major** event and must update the support matrix / compatibility
policy in the same change set.
