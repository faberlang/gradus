# Admitted-Model Capsule Contract (PML0-U14, council C8)

**Schema version**: `capsule-schema-1.0.0` (stamped 2026-08-08)
**Campaign**: `production-ml-library` (PML0, discovery-first)
**Unit**: PML0-U14 — admitted-model capsule contract (C8)
**Status**: planned — the contract is frozen at PML0; the capsule is implemented
by PML2's model-admission surface. Nothing in this document is a claim that a
capsule implementation exists today.
**Authority**: `council-review-2026-08-08.md` C8; `pml0-delivery.md` PML0-U14;
admission behavior facts cited read-only from
`radix/docs/factory/gpu-inference-gguf/gi1-closeout.md`; NGAB0 C8 frozen by
`faber/docs/factory/native-gpu-application-bundle/ngab0-delivery.md` NGAB0-U4.
**Consumed by**: PML0-U13 (receipt schema), PML0-U9 (interface packet),
PML2 (capsule implementation), PML5/PML7 (inference), NGAB0-U4/U10 (manifest +
receipts), and every owner boundary between Gradus and faber-runtime/hosts.

---

## 1. Purpose — the capsule is the typed handoff

The admitted-model capsule is the **typed handoff of model identity across
owner boundaries**. It is the only value that carries a model's identity from
the owner of admission (Gradus, per the PML2 overlap rule) to every downstream
owner (faber-runtime, hosts, and later product surfaces). It packages six
fields — validated bytes, cryptographic identity, tokenizer identity,
quantization, bounds, and architecture facts — each with its own validation
rule, into one schema-versioned value.

The capsule is a **contract**, not a code artifact: at PML0 it freezes the
field vocabulary and validation rules so that PML2's implementation, PML0-U13's
receipts, and NGAB0's manifest all agree on what "a model" means when it
crosses an owner. A capsule must be:

- **self-verifying** — every field carries (or points to) the evidence that
  produced it, so a consumer can re-check identity without re-parsing the raw
  model file;
- **immutable** — a capsule never wraps bytes it did not validate, and never
  mutates after admission;
- **versioned** — schema changes are explicit and rejected on mismatch (§5).

## 2. Trust anchors — raw bytes and paths are NOT trust anchors

**Raw GGUF bytes/paths are NOT trust anchors.** A file path is a locator, not
an identity; raw model bytes have no identity until a typed admission produces
a capsule. Therefore:

- Only the capsule carries identity across Gradus ↔ faber-runtime/hosts.
- Every owner boundary hands off the **capsule** (or its schema-versioned
  identity), never a raw path and never unadmitted bytes.
- No consumer may reconstruct identity from a file path, filename, directory
  layout, emitted text, or naming convention. Identity derived anywhere but
  from the capsule's own fields is a contract violation (mirrors the NGAB0-U4
  "never reconstructed from emitted text or path conventions" rule).
- A path may be **recorded** in the capsule for provenance, but it is
  locator metadata only — it never binds identity and never substitutes for
  the cryptographic identity field (§3.2).

## 3. The six capsule fields

| # | Field | What it carries | Validation rule |
| --- | --- | --- | --- |
| 1 | **Validated bytes** | The exact post-admission byte payload of the model file (GGUF row), byte length, and data-region tiling facts | Bytes are admitted only after the full fail-closed admission matrix passes; byte length is recorded and fixed (pinned row: 270,590,880); the data region tiles exactly with per-tensor coverage accounting (`coverage_ok`); bytes are immutable in the capsule's lifetime — the capsule never wraps bytes it did not validate |
| 2 | **Cryptographic identity** | Content-addressed identity of the validated bytes: named digest algorithm (default **SHA-256**, matching the MD-A9 collision-resistant precedent and NGAB0-U4's default) + whole-file digest value | Identity is derived from the validated bytes only, computed over the whole file (pinned row: `2fa3f013…bac9c2`); identity verifies **before** any downstream selection, load, or backend binding; mismatch → fail closed with a typed error, no CPU fallback; never reconstructed from paths, filenames, or naming conventions |
| 3 | **Tokenizer identity** | Tokenizer kind + pre-tokenizer (pinned row: gpt2 BPE + `smollm` pre-tokenizer), vocabulary identity (digest over the pinned vocab-only fixture), and behavioral facts (EOG set {0, 2}, BOS-free + space-prefix-free behavior, special-parse on/off parity) | Identity is independently re-verifiable: reproducing the pinned probe lists (P1–P11 and the four workload id lists 9 / 9 / 202 / 2175, plus the 24-case differential vs `llama-tokenize` 10150) must match exactly; a tokenizer whose ids diverge from the pinned probes is a different tokenizer and must fail admission |
| 4 | **Quantization** | The admitted quantization descriptor for the row: dtype set {F32, Q4_K, Q5_0, Q6_K, Q8_0} (pinned GGUF row), per-type block layout facts (block elems/bytes Q4_K 256/144, Q5_0 32/22, Q6_K 256/210, Q8_0 32/34, F32 1/4), scale/min encoding, alignment 32 | Only admitted dtype/quant rows are accepted; an unknown dtype id or layout → fail closed with a typed `AdmissionError`; the descriptor is the `QuantizedTensorLayout` contract over the pinned GGML block table, not a general format; toy/approximate encodings (packed-u4) are distinct and un-admitted — no `U8`-as-quantization carrier |
| 5 | **Bounds** | The explicit ceilings the row was validated under: file size, metadata KV count, tensor count, tensor-name length, dimension count/sizes, total element count, data-region limits, per-string byte limits | Every count/offset/length is bounds-checked before any allocation sized by it — no allocation or iteration proportional to an attacker-controlled count precedes validation; pinned-row ceilings: file size == 270,590,880, metadata KV count == 37 with keys ≤ 128 B from the admitted key set, tensor count == 290, tensor-name length ≤ 128, n_dims in {1,2}, dims ≤ 65536, total elements == 361,821,120, data region ≤ file size, per-string bytes ≤ 4096, checked u64 add/mul on every offset/length/size; per-tensor byte ranges in-bounds, non-overlapping, aligned; a gapped/overlapping/misaligned/truncated file can never be admitted (it reports `coverage_ok == false`) |
| 6 | **Architecture facts** | Semantic identity beyond the bytes: architecture identifier (pinned row: `llama`, dense), layer count, named per-layer facts (model contract §2.3: the 16 `ffn_down` Q4_K layers), context/KV configuration | Architecture mismatch → fail closed with a typed error; facts are carried in the capsule, never re-derived from raw bytes downstream; the capsule certifies exactly the row it admitted — the one-row boundary holds, no claim is generalized beyond selected rows |

## 4. Admission behavior (facts, read-only from GI1)

The capsule can only be produced by a **fail-closed admission**. The pinned-row
facts below are cited read-only from `gi1-closeout.md`; PML2 reuses this
behavior when it implements the capsule, and PML0-U7 decides how GI1's admitted
admission code is migrated or retired:

- Admission runs a negative matrix in which truncated, duplicate,
  overlapping, misaligned, unsupported, and architecture-mismatched files each
  **fail closed with a typed `AdmissionError`** (GI1-1: 34-test negative
  matrix).
- The whole-file SHA-256 is verified during admission (pure-Rust; pinned row
  `2fa3f013…bac9c2`).
- Ceilings are checked **before** any allocation sized by a parsed count
  (GI1 exit-gate bullet 4).
- No runtime claim is generalized beyond the selected row (GI1 exit-gate
  bullet 5): the capsule's fields certify the row they admitted and nothing
  else. Qwen2.5 GGUFs remain test-only stress fixtures, never admission
  targets.
- Residual known-nits travel as provenance, not identity: e.g. the
  `chat_template` doc-vs-file reproduction nit (GI1-1) — the capsule's
  identity matched the **file** (hash-pinned), never the doc.

## 5. Schema versioning and change procedure

- **Version stamp**: this contract is `capsule-schema-1.0.0`. Every capsule
  value carries the schema version it conforms to.
- **Version owner**: Gradus (the PML0-U14 freeze; PML2 implements). Faber and
  hosts consume the schema; they do not own it.
- **Change procedure**: any addition, removal, or renaming of a capsule field,
  or any change to a field's validation rule that alters what may be admitted,
  requires a **schema version bump**. A bump is a contract change routed through
  the PML0-U9 version-bump authority and recorded with the rejection/migration
  policy it defines.
- **Rejection**: a consumer that receives a capsule whose schema version it
  does not know must reject it — no best-effort partial reads, no silent
  tolerance. Unsupported schema → typed failure before use.

## 6. Cross-campaign linkage

- **NGAB0-U4 (faber)**: NGAB0 freezes the canonical embedded-artifact identity
  + verification order for the composite executable — digest algorithm named
  (SHA-256 default), verification **before** backend selection, model↔kernel
  compatibility binding, tamper → **pre-launch failure**. The capsule's
  cryptographic identity (§3.2) is the model-side identity that NGAB's
  model↔kernel binding references: the two contracts agree on digest-first,
  fail-closed, no-text-reconstruction semantics.
- **PML0-U9 (interface packet)**: the packet's semantic identities for
  model/tokenizer are carried at load time by the capsule; the capsule is the
  concrete carrier of those identities across owners.
- **PML0-U13 (receipt schema)**: receipts record the capsule's digest as the
  artifact-hash field, so convergence at PML7/NGAB7 is content-addressed.
- **PML2**: implements the capsule over the admitted GGUF/Safetensors rows
  (admission owned by Gradus; no dual authority per C3/U7).
- **PML7**: the inference capstone loads the admitted model **via the capsule**
  (`pml7-delivery.md` U2) — the capsule is the load path, not a side channel.

## 7. This unit's validation proof

The PML0-U14 validation requires: (a) all six capsule fields named with
validation rules — §3, six rows, each with a validation rule; (b) the
non-trust-anchor statement — §2 ("Raw GGUF bytes/paths are NOT trust anchors",
"only the capsule carries identity across Gradus ↔ faber-runtime/hosts");
(c) a schema version — §1 header + §5 (`capsule-schema-1.0.0`);
(d) `git diff --check` clean at closeout.
