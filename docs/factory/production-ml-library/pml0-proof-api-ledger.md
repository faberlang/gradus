# PML0 Proof-Shaped API Ledger — gradus

**Unit**: PML0-U3 (proof-shaped API ledger)
**Date**: 2026-08-08 (grep only; no cargo anywhere)
**Method**: for each `functio` whose name carries a fixed static shape
(`_2x2` / `_4x4` / `_2x8`), grep the live tree for call sites (module
`src/*.fab` + the whole faberlang container for package code), record the
caller evidence or "none", and apply the **clean-break rule**:
**no preservation without a real external caller.**
**Version stamp**: gradus live HEAD at writing `3227b193af3441739587e3d7cfc51546f02951b1`
(no product code touched, so `src/**` is unchanged from the U2 inventory).
**Dependencies**: PML0-U2 symbol inventory feeds the fixed-shape name set.
**Consumed by**: PML0-U10 (`pml0-gradus-contract.md`), PML0-U12 (claim register),
PML1 (shape-generic posture decision).

## Disposition vocabulary

| Disposition | Meaning | Applied when |
| --- | --- | --- |
| **admit** | Keep as proven public API surface | A real external caller exists (grep-verified package code calling the function). |
| **retire** | Remove the symbol; nothing loses capability | No real external caller anywhere in the tree; any equivalent math is already preserved inside caller-backed higher-level functions. |
| **replace** | Supersede this symbol with a different surface package code should use instead | Not used this round — no symbol is needed by a planned replacement; all four no-caller rows are plain **retire**. |

Clean-break rule in force: no row is preserved on the strength of a comment,
a "shipped" claim, a doc mention, or a future intention. Only a live call
from package code admits a symbol.

## Ledger — 17 fixed-shape functions

| # | Module | Name | Shape | Caller evidence | Disposition |
| --- | --- | --- | --- | --- | --- |
| 1 | nn | `linear_2x2` | 2×2 f32 | `examples/training/linear-regression/src/train.fab:93` | **admit** |
| 2 | nn | `linear_4x4` | 4×4 f32 | `examples/training/mlp/src/train.fab:150,152` | **admit** |
| 3 | nn | `gelu_4x4` | 4×4 f32 | `examples/training/mlp/src/train.fab:151` | **admit** |
| 4 | nn | `linear_2x8` | 2×8 f32 | `examples/training/bert-tiny-fragment/src/train.fab:363,364,365,367,370,372`; `examples/training/bert-gradus-probe/src/train.fab:361,362,363,365,368,370,371` | **admit** |
| 5 | nn | `layernorm_2x8` | 2×8 f32 | `examples/training/bert-tiny-fragment/src/train.fab:362,369,374`; `examples/training/bert-gradus-probe/src/train.fab:360,367,372` | **admit** |
| 6 | nn | `gelu_2x8` | 2×8 f32 | `examples/training/bert-tiny-fragment/src/train.fab:371`; `examples/training/bert-gradus-probe/src/train.fab:369` | **admit** |
| 7 | loss | `mse_2x2` | 2×2 f32 | `examples/training/linear-regression/src/train.fab:94` | **admit** |
| 8 | loss | `mse_4x4` | 4×4 f32 | `examples/training/mlp/src/train.fab:153` | **admit** |
| 9 | loss | `mse_2x8` | 2×8 f32 | `examples/training/bert-tiny-fragment/src/train.fab:375`; `examples/training/bert-gradus-probe/src/train.fab:356,373` | **admit** |
| 10 | optimize | `sgd_step_2x2` | 2×2 f32 | none — no call site anywhere in the container; the same update math is inlined in `train_step_2x2` (see `src/train.fab:28-29,41` stepper lib→lib gap) | **retire** |
| 11 | optimize | `sgd_step_4x4` | 4×4 f32 | none — no call site anywhere in the container; the same update math is inlined in `train_step_4x4` (see `src/train.fab:28-29,102`) | **retire** |
| 12 | attention | `scaled_dot_product_2x8` | 2×8 f32 | `examples/training/bert-tiny-fragment/src/train.fab:366` (+ oracle `examples/training/bert-tiny-fragment/oracle/capture.fab:398`); `examples/training/bert-gradus-probe/src/train.fab:364` | **admit** |
| 13 | transformer | `attention_block_2x8` | 2×8 f32 | none — no call site anywhere in the container; `bert_tiny_block_2x8` inlines the same math instead of calling it (see `src/transformer.fab:28-30`) | **retire** |
| 14 | transformer | `ffn_block_2x8` | 2×8 f32 | none — no call site anywhere in the container; `bert_tiny_block_2x8` inlines the same math instead of calling it (see `src/transformer.fab:28-30`) | **retire** |
| 15 | transformer | `bert_tiny_block_2x8` | 2×8 f32 | `examples/training/bert-gradus-probe/src/train.fab:351` | **admit** |
| 16 | train | `train_step_2x2` | 2×2 f32 | `examples/training/linear-regression/src/train.fab:103` | **admit** |
| 17 | train | `train_step_4x4` | 4×4 f32 | `examples/training/mlp/src/train.fab:162` | **admit** |

### Per-module breakdown

| Module | Rows | Dispositions |
| --- | --- | --- |
| nn | 6 | 6 admit |
| loss | 3 | 3 admit |
| optimize | 2 | 2 retire |
| attention | 1 | 1 admit |
| transformer | 3 | 2 retire, 1 admit |
| train | 2 | 2 admit |
| **TOTAL** | **17** | **13 admit, 4 retire** |

## Notes

- **Retired rows lose no capability.** `sgd_step_2x2/_4x4` and
  `attention_block_2x8`/`ffn_block_2x8` are each fully duplicated, inline, in
  caller-backed functions (`train_step_2x2/_4x4`, `bert_tiny_block_2x8`). The
  FMIR stepper's library→library call gap (`src/train.fab:28-29`,
  `src/transformer.fab:24-30`, `src/attention.fab:20-26`) is the recorded
  reason the duplication exists; it does not convert "no caller" into a
  caller, so the clean-break rule retires the standalone symbols.
- **The 21-symbol total is unaffected.** The four retired rows remain in the
  U2 public-symbol inventory (they exist today); this ledger governs their
  disposition at the next API-shape decision point (PML1 posture). The ledger
  covers only the 17 fixed-shape functions; `train_step_bert_linear`,
  `train_step_bert_layernorm`, `gradient.nil`, `gradient.simple_loss` are out
  of scope (non-`_2x2/_4x4/_2x8` shapes).
- **Admitted rows are proof-shaped, not final.** Admission is caller-backed
  evidence for PML0; the production tensor API shape posture (generic /
  generated / staged mix) is decided at PML1 per `pml0-delivery.md` Open
  Questions.

## Validation

```bash
cd /Users/ianzepp/work/faberlang/gradus
grep 'functio' src/*.fab | grep -c '_2x2\|_4x4\|_2x8'          # 17
git diff --check
```

Outcome: grep count == 17, matching the 17 rows above with the per-module
breakdown (nn 6, loss 3, optimize 2, attention 1, transformer 3, train 2);
every row carries a disposition from the closed vocabulary (13 admit,
4 retire); `git diff --check` clean.
