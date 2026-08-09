# PML2 Closeout Note — C3 trio-deletion boundary (transitive-closure gate)

**Unit**: 50981a51 (PML2 phase closeout — campaign gate + C3 boundary)
**Date**: 2026-08-09
**Predecessor**: PML2-U1..U6 all landed (435ccd6, 07291d6, b392fc8, f12deaf,
d6954ab/22041e6, 02fae61 + repairs); decision `pml0-admission-migration-decision.md`
§3.1/§3.2 (migrate-into-Gradus, trio removed at PML2 closeout, no shims); CTO Q3
gate `want 469d929f` (transitive-closure requirement).
**Repos**: gradus (this record), faber-runtime (trio), faber (prefill_run consumer)

## Outcome: C3 deletion boundary **BLOCKED** — unit PARTIAL

The CTO Q3 transitive-closure grep found **live compiled references** to the
faber-runtime trio (`src/gguf.rs`, `src/tokenizer/`, `src/dequant.rs`) on every
named surface plus `tensor_view.rs`. The `git rm` was **NOT executed** — the
CTO Q3 gate is hard and the task instructs no force-delete. The trio remains a
frozen transitional holder (per decision §3.1). The campaign status line
reflects an active/partially-delivered PML2.

## Transitive-closure disposition table

Grep basis: `grep -rn 'GgmlType\|gguf\|dequant\|tokeniz\|admit_file'` across the
named surfaces + faber `src/package/device/prefill_run.rs`, verified per-file.

| Surface | Reference (file:line) | Disposition |
| --- | --- | --- |
| capability | `faber-runtime/src/capability.rs:26,84-91` — `use crate::gguf::GgmlType` + `GgmlType::{Q4_K,Q5_0,Q6_K,Q8_0}` in `consumed_tensor_classes` | **blocked-with-owner** (live pub fn) |
| tensor-layout-view (QuantizedTensorLayout) | `faber-runtime/src/quantized_tensor_layout.rs:38,154-175,265,293,337,397,491,564` — `use crate::gguf::{GgmlType, GgufAdmission, TensorDescriptor}` + `crate::gguf::hex` | **blocked-with-owner** (live impl/resolve/format_id) |
| repack/oracle surfaces | `faber-runtime/src/repack_plan.rs:32-33,73,89-129,220,248,295,402-424` — `use crate::dequant::ORACLE_TRANSFORM_IMPL` + `use crate::gguf::{GgmlType, PINNED_SHA256_HEX}` | **blocked-with-owner** (live plan types) |
| oracle | `faber-runtime/src/cpu_oracle.rs:120,165-197,292-435` — `use crate::dequant::{dequant_tensor, half_to_f32, DequantError, OracleReceipt}` + call sites | **blocked-with-owner** (live materialization path) |
| bound-plan | `faber-runtime/src/bound_plan.rs:484` — `crate::gguf::sha256` | **blocked-with-owner** (live hash) |
| greedy-run | `faber-runtime/src/greedy_run.rs:349` — `crate::gguf::hex(&crate::gguf::sha256(..))` | **blocked-with-owner** (live record hash) |
| tensor-view (additional) | `faber-runtime/src/tensor_view.rs:34,75,213-244,316-340` — `use crate::gguf::{hex, sha256, GgmlType, GgufAdmission, PINNED_SHA256}` | **blocked-with-owner** (live view/build) |
| faber prefill_run.rs | `faber/src/package/device/prefill_run.rs:62-63,264-378` — `use faber::dequant::{dequant_tensor, OracleReceipt}` + `use faber::gguf::admit_file` (faber = faber-runtime via Cargo.toml `faber = { package = "faber-runtime" }`) | **blocked-with-owner** (live device run) |

Additional closure members (not in the named list, same conclusion):
`faber-runtime/src/decoder_ops.rs` (doc-comment only), plus test files
(`capability_test.rs`, `cpu_oracle_test.rs`, `greedy_run_test.rs`,
`quantized_tensor_layout_test.rs`, `repack_plan_test.rs`, `tensor_view_test.rs`)
— ride on the same consumer decouple.

**Grep assertion at the deletion boundary: FAILED** — zero live references was
NOT satisfied, so the deletion did not proceed. No shims were added; nothing in
the trio or its consumers was modified.

## Decision context honored

- §3.1 boundary: `git rm` (no forwarding shims) — **deferred**, not violated.
- §3.2 no-dual-authority: the trio still hosts admission code, but PML2 units
  U1–U6 delivered the Gradus port (`gradus/src/model/`), and the faber-runtime
  trio received no new code or callers during this closeout. Authority remains
  in Gradus; the trio is a frozen holder pending decouple.
- PML0-U8 grep re-verified: `grep -rn 'AdmissionError\|admission' ../norma/src/model.fab`
  → only 2 comment mentions (lines 9, 12, C3 posture headers); **no live
  admission symbols** in norma `model.fab`. PASS.

## Validation (one closeout run)

- Transitive-closure grep assertions: executed; deletion assertion FAILED (block recorded above).
- PML0-U8 grep: PASS (no admission symbols in norma `model.fab`).
- `git diff --check`: PASS (gradus + faber-runtime).
- gradus `check-source`: PASS.
- gradus `check-compile` (FABER_BIN=faber/target/release/faber): PASS (gradus + gradient-seam fixture).
- faber-runtime `cargo check -p faber-runtime`: PASS (1 pre-existing `unused_mut` warning, unrelated to this unit).
- README `--check`: PASS after regeneration (this record added to the gradus factory README).
- goal-status audit (`audit-factory-goal-status.py --factory-root docs/factory`): **0 findings** (gradus).

## Residuals + owners

| # | Residual | Owner | State |
| --- | --- | --- | --- |
| 1 | Decouple the 8 live trio references above (capability, tensor-layout-view, repack/oracle, bound-plan, greedy-run, tensor-view, faber prefill_run) from the trio | faber-runtime owner (runtime consumers) + faber product owner (prefill_run.rs); coordinate with PML2 campaign per §3.1 | **blocked-with-owner** — blocking the C3 deletion |
| 2 | Re-run this closeout boundary (grep assertion → `git rm` trio) once the decouple lands | PML2 closeout hand (re-dispatch) | pending |
| 3 | PML0-U8 normA admission-symbol grep stays clean at re-run | normA/PML2 owner | pass (re-verify at re-run) |
| 4 | `unused_mut` warning in faber-runtime | faber-runtime owner (style, unrelated) | out of scope |

## Escalation

Per the task instruction ("record the blocking reference with owner +
escalation, mark the unit partial with an honest need"), this closeout is
**PARTIAL**. A need is filed to mind/reviewer with this table; the C3 deletion
boundary requires a consumer-decouple unit before it can be re-executed. PML3
is not blocked by this (PML3 status remains next).
