# PML0 Support-Matrix Schema

**Unit**: PML0-U5 (support-matrix schema)
**Purpose**: defines the versioned row schema for the Gradus model support
matrix — the single inventory that records which model formats,
architectures, dtypes, quantizations, shapes, and tokenizers are admitted as
supported. PML0 commits the schema only; no product rows are admitted here.
**Schema version stamp**: `gradus-support-matrix-schema v0.1.0` (2026-08-08)
**Snapshot dependency**: PML0-U1 (`pml0-source-snapshot.md`) — all fixture,
oracle, and evidence refs below resolve against the recorded revisions and
dirty state.
**Consumed by**: PML0-U12 (claim register row vocabulary), PML0-U10 (contract
assembly), PML1 (tensor/dtype/shape foundation), PML2 (first admitted rows),
PML6 (support-matrix baseline and release contract).

## 1. Scope and posture

This document defines the **row schema** for the support matrix. A *row* is a
single admitted combination of model format, architecture, dtype,
quantization, shape, and tokenizer identity together with its fixtures,
oracle, evidence, and compatibility policy. A row is the unit of support
claim: support is never claimed at the level of "the library supports GGUF"
or "the library supports transformers" — only "this exact row is admitted".

**One admitted row first.** General model-format or architecture support is
earned by explicit rows, never inferred from one fixture. PML0 commits **zero
populated product rows** (template only). The first product rows are admitted
at PML2: one Safetensors row and one selected GGUF row, each failing closed on
format, architecture, dtype/quantization, shape, and tokenizer identity.
Admitting a row does not license a broader support claim than the row itself
states.

**Fail-closed invariant.** Model admission fails closed by format,
architecture, dtype, quantization, shape, tokenizer identity, and version. A
proposed row that does not satisfy every field's validation rule is **not**
admitted — there is no partial or provisional support row.

## 2. Row schema (versioned)

Each row has exactly the following fields. All fields are required; there are
no optional fields. A row is a single markdown table row in
`pml0-support-matrix.md` (created when the first rows are admitted at PML2);
until then, the template below is the only row-shaped content.

| # | Field | Vocabulary (closed set) | Validation rule (fail-closed) |
| --- | --- | --- | --- |
| 1 | `format` | `safetensors`, `gguf`; each carries an explicit format version (e.g. GGUF quant version) | Format name must be from the closed vocabulary; format version must be named; an unknown format or missing/unverifiable format version **rejects** the row. |
| 2 | `architecture` | Named architecture families from the admitted architecture register (first family landed via the PML2 row admission; e.g. `qwen35moe` precedent from GI0) | Architecture must be a canonical family name with a single owning spec; an unknown or ambiguous architecture name **rejects** the row. |
| 3 | `dtype` | `f32`, `f16`, `bf16` (compute dtype; storage dtype named when it differs) | Dtype must be from the closed vocabulary; compute vs storage dtype must be explicit; an unsupported or unverifiable dtype **rejects** the row. |
| 4 | `quantization` | `none`, plus scheme+version pairs from the closed quantization register (e.g. `q4_k_m`, quant version) | Scheme and quant version must both be named and consistent with the format; a quantization the row cannot verify (weights, scales, block layout) **rejects** the row. |
| 5 | `shape` | Enumerated fixed shapes (current baseline: `2x2`, `4x4`, `2x8` suffixes in `src/*.fab`) or shapes proven by an admitted row's fixture+oracle | Every shape claimed must be enumerated explicitly and backed by fixture evidence; a shape claim without a fixture or oracle proof **rejects** the row. |
| 6 | `tokenizer identity` | Tokenizer family + pre-tokenizer + special-token set (BOS/EOS/EOG) + vocabulary fingerprint (hash or pinned id list) | Tokenizer identity must be exactly reproducible (vocab fingerprint, special-token behavior, e.g. the GI1 gpt2/smollm probes); any mismatch or missing fingerprint **rejects** the row. |
| 7 | `legal fixture ref` | A locally present, licensed model fixture, pinned by content hash (e.g. SHA-256) with a named source/authority | Fixture must be pinned by content hash, locally present, and lawfully usable (license/source authority named; no acquisition or redistribution claim); missing, unpinned, or test-only fixtures are **rejected** as legal fixtures. |
| 8 | `oracle ref` | Independent reference: pinned comparator build (binary hash) or independent oracle implementation, plus the numeric contract (e.g. top-1 exact, tolerance band, first-divergence rule) | Oracle must be named, pinned (revision/build + hash), and the numeric contract stated; a row without an independent, pinned oracle **rejects**. |
| 9 | `evidence links` | Committed, resolvable paths to tests, examples, diagnostics, and performance evidence (relative to the gradus repo) | Every link must resolve to a committed path in the snapshot revision; tests must exist and be runnable; an unresolvable or absent evidence link **rejects** the row. |
| 10 | `compatibility policy` | A bounded promise: what the row supports, what it explicitly does not claim, deprecation/change handling | Policy must name the exact admitted combination and state non-goals explicitly (no generalization to other architectures, formats, dtypes, quants, shapes, or tokenizers); a policy that implies broader support than the row **rejects** the row. |

The row schema itself is versioned. Each admitted row records the schema
version under which it was admitted, so vocabulary changes are traceable:

- **Patch bump** (`v0.1.x`): clarification or example only; no vocabulary or
  rule change. Existing rows unaffected.
- **Minor bump** (`v0.x.0`): vocabulary expansion or added field; existing
  rows remain valid under the previous version.
- **Major bump** (`vX.0.0`): field removal/renaming, meaning change, or a
  fail-closed rule change; **all existing rows must be re-validated** under
  the new schema.

Schema bumps are recorded in this file's version stamp; the generator of the
matrix must reject a row whose recorded schema version does not match the
current major version.

## 3. Reject-row rules (explicit)

A proposed row is **rejected** — with no partial admission — when any of the
following holds. These are mechanical gates, not judgment calls:

- **R1** — Format is unknown, unversioned, or not in the closed vocabulary.
- **R2** — Architecture is unknown, ambiguous, or not in the architecture register.
- **R3** — Dtype is not in the closed vocabulary, or compute/storage dtype is unstated.
- **R4** — Quantization is unknown, unversioned, or inconsistent with the format.
- **R5** — Any claimed shape lacks an explicit fixture or oracle proof.
- **R6** — Tokenizer identity is not exactly reproducible (vocab fingerprint,
  special-token set, or pre-tokenizer mismatch).
- **R7** — No legal fixture: missing, unpinned, not locally present, or
  test-only; or the fixture's license/source authority is not named.
- **R8** — No independent oracle, or the oracle is not pinned (no revision/build hash).
- **R9** — Evidence links are absent, unresolvable, or reference uncommitted paths.
- **R10** — Compatibility policy is absent, or generalizes beyond the exact row
  (e.g. "GGUF is supported" rather than "this row is admitted").
- **R11** — Any required field is `tbd`, `none`, or empty; a row is not
  admitted on the promise that a field will be filled later.

Rejected rows are **recorded** (row + reject reason) in the matrix's
reject log so the reason is auditable; recording a rejected row never
constitutes support. The fail-closed invariant means a rejected row stays
rejected until it independently satisfies every rule — a re-review must
re-run all gates, not a subset.

## 4. Empty row template

The following is the **only** row-shaped content admitted in PML0. It is a
template: it carries no product values, must never be read as a support
claim, and is replaced by real admitted rows only after PML2.

```markdown
<!-- TEMPLATE ONLY — no product row is admitted in PML0 (PML0-U5). -->
| `format` | `safetensors` | `gguf` |
| `architecture` | `<canonical family name from the architecture register>` |
| `dtype` | `<compute dtype>` | `<storage dtype when different>` |
| `quantization` | `<scheme + quant version>` | (`none` allowed) |
| `shape` | `<enumerated fixed shapes>` |
| `tokenizer identity` | `<family + pre-tokenizer + special-token set + vocab fingerprint>` |
| `legal fixture ref` | `<repo-relative path + SHA-256 + license/source authority>` |
| `oracle ref` | `<pinned oracle revision/build hash + numeric contract>` |
| `evidence links` | `<committed test / example / diagnostic / perf paths>` |
| `compatibility policy` | `<exact admitted combination + explicit non-goals>` |
| `schema version` | `<schema version under which the row is admitted>` |
```

A populated matrix (`pml0-support-matrix.md`) contains only admitted rows that
passed every gate in §2/§3, each with all fields filled. Until the first
PML2 admission, the matrix holds the template above and a reject log — and
therefore reads as **no product support yet**, by construction.

## 5. Relationship to other PML0 artifacts

- **PML0-U12 (claim register)** consumes this row vocabulary: register rows
  reuse the `format`/`architecture`/`dtype`/`quantization`/`tokenizer
  identity` vocabulary so claim status can never be read as product support.
- **PML0-U10 (contract)** references this schema as the support-matrix
  artifact; the contract names the schema version stamp.
- **PML6** builds the release-time support matrix and compatibility policy
  from this schema and the admitted rows.

## Validation

```bash
# Required field + validation-rule coverage: each of the 10 fields in §2
# appears with a validation rule (grep counts both the field table and the
# reject rules).
grep -c '^| [0-9]* | `' docs/factory/production-ml-library/pml0-support-matrix-schema.md
# Zero populated product rows: the only row-shaped content is the §4 template.
grep -c '^| `format`' docs/factory/production-ml-library/pml0-support-matrix-schema.md
git diff --check
```

Outcome: 10 schema fields, each with a validation rule; zero populated product
rows (template only); `git diff --check` clean.
