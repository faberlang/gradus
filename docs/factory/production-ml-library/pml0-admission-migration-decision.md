# PML0-U7 — Admission-Code Migration Mechanics Decision (Council C3)

**Unit**: PML0-U7 of [`pml0-delivery.md`](pml0-delivery.md) (council C3:
admission-migration mechanics decision, no-dual-authority by code location,
owner + fallback).
**Status**: decided 2026-08-08 — **migrate into Gradus** (recorded default in
Vivi need `f3309d29`; proceeds until overridden by operator).
**Confirmed by operator 2026-08-09**: the default is the normal path — porting
the proven Rust admission trio with the Rust implementation as the reference
oracle needs no operator decision. The need is closed (`f3309d29` done);
the recorded default stands as decided.
**Decision owner**: **operator** — the binding decision owner per
`pml0-delivery.md` ("Decision owner: operator"; recorded via Vivi need To
`operator@`, default proceeds until overridden).
**Feeds**: U11 (GI4+ ownership amendment + migration map), PML2 (model-format
code migration). **Consumes (read-only)**: `gi1-closeout.md`,
`gi2-closeout.md`, GI delivery/contract docs; no GI stage is reopened.
**Write scope**: this file only (+ the Vivi need, a board record).

---

## 1. Subject: GI1's accepted admission code

GI1 accepted fail-closed model admission for the pinned row
SmolLM2-360M-Instruct Q4_K_M, implemented in **faber-runtime** (Rust). The
accepted admission code comprises three locations (verified live in the tree
at faber-runtime HEAD `10d48ea`):

| Code | Live location | Source facts (GI closeouts) |
| --- | --- | --- |
| GGUF v3 container admission — fail-closed, 290 tensors, 37 KVs, SHA-256 `2fa3f013…bac9c2`, ceilings-before-allocation, typed `AdmissionError` | `faber-runtime/src/gguf.rs` (+ `gguf_test.rs`) | GI1-1 `0c588e2` (`gi1-closeout.md` §1 bullets 3–4; `gi1-delivery.md` §outcome `gguf.rs`) |
| gpt2 BPE + smollm pre-tokenizer — probe parity P1–P11, four workload id lists, EOG set {0,2}, 24-case differential vs `llama-tokenize` 10150 | `faber-runtime/src/tokenizer/` (`mod.rs`, `bpe.rs`, `pretoken.rs`) + `src/tokenizer_test.rs` | GI1-3 `ef2fad9` (`gi1-closeout.md` §1 bullet 1) |
| CPU dequant of the four admitted GGML block types — Q4_K 256/144, Q5_0 32/22, Q6_K 256/210, Q8_0 32/34, F32 1/4 → f32, bit-exact vs `ggml dequantize_row_*` | `faber-runtime/src/dequant.rs` (+ `dequant_test.rs`) | GI2-1 `08c3903` (`gi2-closeout.md` §2; `gi2-delivery.md` §outcome `dequant.rs`) |

Supporting accepted surfaces stay with their GI owners and are **not part of
this decision**: `QuantizedTensorLayout` (GI1-2 `42185bf`), `tensor_view.rs`
(GI1-4 `571eb87`), the GI2 CPU-oracle modules (`decoder_ops.rs`,
`cpu_oracle.rs`, `greedy_run.rs`). This decision covers the **admission trio
only** — the code that turns raw pinned-row GGUF bytes into a validated,
tokenized, dequantized model.

## 2. Cited GI grep findings (U11 reconciliation list)

These findings are the citation list U11 consumes when reconciling stale GI4+
owner clauses. Each is grep-verified live (2026-08-08):

| # | Finding (grep-verified) | Location |
| --- | --- | --- |
| 1 | "Model-runtime owner — `faber-runtime` … durable model-runtime component: model admission facade, tokenizer execution, `InferenceSessionState`" (stale; U11 amends) | `gi0-delivery.md:59` |
| 2 | "Tokenizer runtime owner — the same durable runtime component (faber-runtime) beside model admission" (stale; U11 amends) | `gi0-delivery.md:60` |
| 3 | "Owner = `faber-runtime` … model admission facade, tokenizer execution, `InferenceSessionState`. Never the CLI, Gradus, examples, or an effect provider (memo `fdc2a448` + CTO `1e7602b1`)" (stale; U11 amends) | `gi0-closeout.md:27` |
| 4 | "New faber-runtime modules only (`gguf.rs`, `quantized_tensor_layout.rs`, `tokenizer.rs`, `tensor_view.rs` + tests)" | `gi1-delivery.md:87` |
| 5 | "New faber-runtime module `gguf.rs`: fail-closed admission for the pinned row only" | `gi1-delivery.md:286` |
| 6 | "Oracle location — `faber-runtime` (durable model-runtime owner; decision (d)/(e); memo `fdc2a448`)" | `gi2-delivery.md:93` |
| 7 | "`faber-runtime/src/gguf.rs` + `tokenizer.rs` — GI1-1 admission (ceilings, 37 KVs, 290 tensors, SHA-256 `2fa3f013…`); GI1-3 tokenizer … Tokenizer identity is consumed, never re-derived" | `gi2-delivery.md:145` |
| 8 | "New faber-runtime module `dequant.rs`: CPU dequantization of the four admitted GGML block types … consuming `QuantizedTensorLayout`" | `gi2-delivery.md:312` |
| 9 | "`dequant.rs` landed: Q4_K 256/144, Q5_0 32/22, Q6_K 256/210, Q8_0 32/34, F32 1/4 → f32; `coverage_ok()` gating (GI1-4 residual folded in)" | `gi3-delivery.md:193` |
| 10 | Live-tree fact: `faber-runtime/src/gguf.rs`, `src/dequant.rs`, `src/tokenizer/` all present at faber-runtime HEAD `10d48ea` | `ls` of `faber-runtime/src/` |

The common thread: GI0–GI3 docs assign model-runtime and tokenizer-runtime
ownership to faber-runtime; U11 rewrites those clauses to the new Gradus
authority. This decision supplies the **mechanics** for what happens to the
accepted admission code those clauses named.

## 3. Decision: migrate into Gradus

**Chosen path: migrate into Gradus.** The accepted admission trio moves, by
re-expression, into the Gradus library at PML2 — the campaign's model-format
migration stage (`pml0-delivery.md` non-goals: "no model-format code
migration (that is PML2)"). **No code moves in PML0**; PML0 records the
decision and its mechanics only.

Rationale:

- The trio is **accepted and proven**: whole-file SHA-256 admission, the
  34-test fail-closed negative matrix, probe/parity-exact tokenizer ids,
  bit-exact dequant. It is the only proven admission implementation for the
  pinned row.
- **Retiring discards that proof** and forces re-derivation from scratch
  under the new owner; migrating preserves the pinned-row contracts as the
  acceptance oracles for the port.
- The campaign trajectory already moves model-runtime and tokenizer-runtime
  ownership **from** faber-runtime **to** Gradus (C1 → U11; the GI4+ clauses
  in §2 are stale). Naming Gradus as the migration destination keeps this
  decision aligned with the ownership amendment.
- Migration is a **re-expression port** (Rust → Faber), not a copy: the
  faber-runtime implementation is the **migration oracle** — its tests,
  fixtures, and pinned-row facts are the acceptance target for the Gradus
  port.

### 3.1 Migration mechanics (PML2)

- **Migration work owner**: PML2 (Gradus-side) + the U11 amendment (radix
  GI docs). PML0 records the decision only.
- **Pinned-row boundary**: only the one admitted row
  (SmolLM2-360M-Instruct Q4_K_M) may be migrated; no generalization and no new
  architecture/quant rows (GI1 decision (b), one-row rule).
- **Parity gates (migration acceptance)**: the Gradus port must reproduce,
  per module, the acceptance facts — tokenizer id lists P1–P11 + the four
  workload id lists exactly; whole-file SHA-256 admission; dequant bit-exact
  vs the pinned comparator per block type; the 34-test negative-matrix
  semantics (fail closed, ceilings checked before allocation).
- **Boundary action**: at migration completion (PML2 closeout), the
  faber-runtime trio is **removed** (`git rm` — no forwarding shims, no dead
  copies). Until that boundary, the faber-runtime files are a **frozen
  transitional holder**: no new admission code, no new callers, no new
  quant/arch rows.

### 3.2 No-dual-authority (enforced by code location)

- **Single owning module path (named)**: `gradus/src/model/` — the only place
  admission logic may live once migrated (future Faber sources, one concern
  per module: `gguf.fab`, `tokenizer.fab`, `dequant.fab` + tests, mirroring
  the trio 1:1).
- **The other location must not host admission logic**:
  `faber-runtime/src/gguf.rs`, `faber-runtime/src/dequant.rs`,
  `faber-runtime/src/tokenizer/`. Rule: (a) from this decision date, no new
  admission logic, caller, or quant/arch row may be added there; (b) at the
  PML2 migration boundary the files are deleted; (c) the boundary closeout
  runs a grep assertion that no admission symbols remain
  (`grep -rn 'AdmissionError\|admission' faber-runtime/src/{gguf.rs,dequant.rs,tokenizer/}`
  → no matches / files absent). Until then these files carry **no
  authority** — they are an implementation holder whose role is the migration
  oracle, never a second owner.
- Dual authority is therefore impossible: one owning path (Gradus), one named
  non-owning location (the faber-runtime trio), with the non-owning location
  emptied at the boundary and a grep check as the enforcement.

### 3.3 Fallback rule

If the chosen path is blocked at PML2 — the Faber-language port cannot
reproduce the pinned-row parity gates (tokenizer ids, SHA-256 admission,
dequant bit-exactness) within the campaign's parity rules — the fallback is
**formally retire**: the faber-runtime trio is removed at the migration
boundary anyway (`git rm`, no forwarding shims, no new callers), Gradus
admission for the pinned row is declared out of scope until a Gradus-native
implementation exists, and the GI facts remain as historical evidence only
(U11's reconciliation still applies — faber-runtime is not an owner under
either path). The fallback **never** leaves both locations hosting admission
logic; it only changes whether Gradus gains the capability at PML2.

## 4. Decision owner

- **Owner**: operator (binding decision; recorded in Vivi need `f3309d29`
  sent 2026-08-08; the recorded default proceeds until overridden per
  `pml0-delivery.md` decision-owner policy).
- **Recording**: this document + the Vivi need. U11 consumes §2's findings;
  PML2 consumes §3.

## 5. Validation record

- Doc contains: a named decision owner (§4), a fallback rule (§3.3), and the
  named single owning code location with the non-owning location rule
  (§3.2) — present.
- Cited GI grep findings (§2, 10 rows) form U11's reconciliation list —
  present.
- `git diff --check` — clean.
