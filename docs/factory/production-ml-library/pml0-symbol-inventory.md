# PML0 Public Symbol Inventory — gradus

**Unit**: PML0-U2 (public symbol inventory)
**Date**: 2026-08-08 (grep only; no cargo anywhere)
**Source**: live `grep -c 'functio ' src/*.fab` per module
**Method**: `scripta/inventory-public-symbols` — grep-based; counts `functio `
declaration lines per `src/*.fab` module, prints the module → functio table plus
the total, and asserts the PML0 baseline (total 21; per-module counts per
`pml0-delivery.md` §Repo-Aware Baseline).
**Version stamps**: gradus live HEAD at snapshot `d7e85aa6aad1fd41c53524f08c481553b154d042`
(`pml0-source-snapshot.md`); U2 touches no product code, so `src/**` is unchanged.
**Consumed by**: PML0-U3 (proof-shaped API ledger) feeds the fixed-shape rows
from the names below.

## Captured output

```
module         functio
attention      1
data           0
gradient       2
gradus         0
loss           3
math           0
nn             6
optimize       2
tensor         0
train          4
transformer    3
TOTAL          21
```

## Symbol detail

| Module | Count | `functio` names |
| --- | --- | --- |
| attention | 1 | `scaled_dot_product_2x8` |
| data | 0 | — (stub) |
| gradient | 2 | `nil`, `simple_loss` |
| gradus | 0 | facade map only (no genera) |
| loss | 3 | `mse_2x2`, `mse_4x4`, `mse_2x8` |
| math | 0 | — (stub) |
| nn | 6 | `linear_2x2`, `linear_4x4`, `gelu_4x4`, `linear_2x8`, `layernorm_2x8`, `gelu_2x8` |
| optimize | 2 | `sgd_step_2x2`, `sgd_step_4x4` |
| tensor | 0 | — (stub) |
| train | 4 | `train_step_2x2`, `train_step_4x4`, `train_step_bert_linear`, `train_step_bert_layernorm` |
| transformer | 3 | `attention_block_2x8`, `ffn_block_2x8`, `bert_tiny_block_2x8` |

## Assertions (hold)

- Total `functio` in `src/*.fab` == **21**.
- Per-module counts match baseline: nn 6, train 4, loss 3, transformer 3,
  gradient 2, optimize 2, attention 1. Zero-count stubs (math, tensor, data)
  and the gradus facade are covered by the total.

## Validation

```bash
cd /Users/ianzepp/work/faberlang/gradus
./scripta/inventory-public-symbols            # exit 0; table + total 21
diff <(./scripta/inventory-public-symbols) \
  <(awk 'BEGIN{n=0} /^```$/{n++; next} n==1{print} n>1{exit}' \
     docs/factory/production-ml-library/pml0-symbol-inventory.md)  # clean
grep -c 'functio ' src/*.fab | awk -F: '{s+=$2} END {print s}'   # 21
git diff --check
```

Outcome: `./scripta/inventory-public-symbols` exits 0 (baseline assertions
hold); a fresh run diffs clean against the captured output above; total
`grep -c 'functio ' src/*.fab` == 21; `git diff --check` clean.
