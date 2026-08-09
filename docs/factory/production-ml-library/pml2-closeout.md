# PML2 Closeout Note — C3 trio-deletion boundary (transitive-closure gate)

**Unit**: c600919 (initial partial) + closeout re-run 6331a03c — PML2 phase
closeout (campaign gate + C3 boundary)
**Date**: 2026-08-09
**Predecessor**: PML2-U1..U6 all landed (435ccd6, 07291d6, b392fc8, f12deaf,
d6954ab/22041e6, 02fae61 + repairs); decision `pml0-admission-migration-decision.md`
§3.1/§3.2 (migrate-into-Gradus, trio removed at PML2 closeout, no shims); CTO Q3
gate `want 469d929f` (transitive-closure requirement); consumer decouple
(faber-runtime `9a0295e` + faber `08d195f` — all 8 surfaces moved to
`model_format.rs` / `model_widen.rs`).
**Repos**: gradus (this record), faber-runtime (trio), faber (prefill_run consumer)

## Outcome: C3 deletion boundary **EXECUTED** — unit DELIVERED

The initial closeout (`c600919`) was PARTIAL: the CTO Q3 transitive-closure grep
found live compiled references to the faber-runtime trio on every named surface,
so the `git rm` was **not** executed and the trio remained a frozen transitional
holder. The decouple unit then moved every live surface to the shared non-trio
carriers (`model_format.rs` — admission; `model_widen.rs` — dequant). This
closeout re-run executes the deletion boundary per decision §3.1:

1. **Zero-reference grep re-run** (faber-runtime/src + faber/src/package/device):
   **PASSED** — the only live trio references are inside the trio files, the
   trio-owned test files, and lib.rs mod decls (all boundary-owned). No live
   reference exists outside the trio/facade boundary.
2. **Trio removed with `git rm`, no forwarding shims**: `src/gguf.rs`,
   `src/tokenizer/` (`mod.rs`, `bpe.rs`, `pretoken.rs`), `src/dequant.rs`, plus
   the trio-owned test files.
3. **Carriers retained**: `model_format.rs` + `model_widen.rs` (the decoupled
   carriers, not the trio). lib.rs mod decls for the trio removed.
4. **Coverage preserved (not deleted)**: `gguf_test.rs` → `model_format_test.rs`
   and `dequant_test.rs` → `model_widen_test.rs`, moved to the carriers' test
   locations with spellings updated to the carrier surface (`admit_pinned`,
   `PinnedDtype`, `PinnedAdmission`, `widen_block/row/tensor`, `WidenError`).
   `tokenizer_test.rs` was removed with the trio — the tokenizer logic leaves
   faber-runtime entirely, and its parity facts (P1–P11, workload id lists) are
   acceptance-oracle material for the gradus port (`gradus/src/model/`), already
   delivered by PML2-U1..U6.
5. **Transitive-closure gate: PASSED**.

## Transitive-closure disposition table

Grep basis: `grep -rn 'GgmlType\|gguf\|dequant\|tokeniz\|admit_file'` across the
named surfaces + faber `src/package/device/prefill_run.rs`. Post-decouple, every
live surface references the carriers; remaining broad-grep matches are doc
comments or model file-path strings only (verified per-file).

| Surface | Post-decouple reference | Disposition |
| --- | --- | --- |
| capability | `faber-runtime/src/capability.rs` — `crate::model_format::PinnedDtype` | **decoupled** (9a0295e) → carrier retained |
| tensor-layout-view (QuantizedTensorLayout) | `faber-runtime/src/quantized_tensor_layout.rs` — `crate::model_format` | **decoupled** (9a0295e) → carrier retained |
| repack/oracle surfaces | `faber-runtime/src/repack_plan.rs` — `crate::model_format` + `crate::model_widen` | **decoupled** (9a0295e) → carrier retained |
| oracle | `faber-runtime/src/cpu_oracle.rs` — `crate::model_widen::{widen_tensor, half_to_f32, OracleReceipt, WidenError}` | **decoupled** (9a0295e) → carrier retained |
| bound-plan | `faber-runtime/src/bound_plan.rs` — `crate::model_format::sha256` | **decoupled** (9a0295e) → carrier retained |
| greedy-run | `faber-runtime/src/greedy_run.rs` — `crate::model_format::{hex, sha256}` | **decoupled** (9a0295e) → carrier retained |
| tensor-view | `faber-runtime/src/tensor_view.rs` — `crate::model_format` | **decoupled** (9a0295e) → carrier retained |
| faber prefill_run.rs | `faber/src/package/device/prefill_run.rs` — `faber::model_widen::{widen_tensor, OracleReceipt}` + `faber::model_format::admit_pinned_file` | **decoupled** (08d195f) → carrier retained |

Riding tests (capability_test, cpu_oracle_test, greedy_run_test, tensor_view_test,
quantized_tensor_layout_test, repack_plan_test, decoder_ops_test) were decoupled
to the carriers in 9a0295e and remain.

**Grep assertion at the deletion boundary: PASSED** — zero live trio references
outside the trio files/tests and lib.rs mod decls; the trio paths are now absent.

## Decision context honored

- §3.1 boundary: `git rm` executed with **no forwarding shims**; the trio is gone.
- §3.2 no-dual-authority: `faber-runtime/src/{gguf.rs,dequant.rs,tokenizer/}`
  host no admission logic (files absent); authority remains in Gradus
  (`gradus/src/model/`).
- PML0-U8 grep re-verified: `grep -rn 'AdmissionError\|admission' ../norma/src/model.fab`
  → only 2 comment mentions (lines 9, 12, C3 posture headers); **no live
  admission symbols** in norma `model.fab`. PASS.

## Validation (one closeout run)

- Transitive-closure grep assertions: executed; deletion assertion PASSED (block cleared).
- PML0-U8 grep: PASS (no admission symbols in norma `model.fab`).
- faber-runtime `cargo check -p faber-runtime`: PASS.
- faber `cargo check -p faber`: PASS (radix tree clean after CDA-U3 landed `8e40c9b6c`).
- `git diff --check`: PASS (gradus + faber-runtime).
- README `--check`: PASS after regeneration.
- goal-status audit (`audit-factory-goal-status.py --factory-root docs/factory`): **0 findings** (gradus).

## Residuals + owners

| # | Residual | Owner | State |
| --- | --- | --- | --- |
| 1 | ~~Decouple the 8 live trio references~~ — executed in 9a0295e / 08d195f | faber-runtime + faber | **done** |
| 2 | ~~Re-run the closeout boundary (grep assertion → `git rm` trio)~~ — executed this unit | PML2 closeout hand | **done** |
| 3 | PML0-U8 normA admission-symbol grep stays clean at subsequent boundaries | normA/PML2 owner | pass (re-verified) |
| 4 | `unused_mut` warning in faber-runtime | faber-runtime owner (style, unrelated) | out of scope |
| 5 | Gradus port remains the single admission authority (`gradus/src/model/`) — no dual authority; tokenizer parity facts retained as oracle evidence | Gradus/PML3+ | continuing |

## Escalation

None — the escalation from the initial closeout (`a9dbaf90`) is RESOLVED: the
transitive-closure block was cleared by the decouple, the radix-parser blocker
was hand-8's CDA-U3 mid-flight (committed `8e40c9b6c`; radix tree clean), and
the faber check PASS was verified. PML2 is delivered; PML3 proceeds next.
