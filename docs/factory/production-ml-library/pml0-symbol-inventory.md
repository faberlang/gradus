# PML0/PML1 Public Symbol Inventory — gradus

**Unit**: PML0-U2 (public symbol inventory), re-baselined at PML1 closeout
**Date**: 2026-08-08 (PML0) / 2026-08-09 (PML1 re-baseline; grep only, no cargo)
**Source**: live `grep -c 'functio ' src/*.fab` per module
**Method**: `scripta/inventory-public-symbols` — grep-based; counts `functio `
declaration lines per `src/*.fab` module, prints the module → functio table plus
the all-module total, and asserts the PML1 re-baselined baseline: per-module
counts for the seven fixed-shape proof-surface modules (post-U6: optimize 0,
transformer 1) and the tracked proof-surface total 17. The live all-module
total (printed TOTAL row) includes the foundation modules
(dtype/math/parameter/serialize/shape/tensor) that are versioned by their own
contract docs and schemas.
**Version stamps**: PML1 closeout at gradus HEAD (PML1-U1..U7 landed,
45a09d9..de017eb); re-baseline re-derives live counts from the current tree.
**Consumed by**: PML0-U3 (proof-shaped API ledger) feeds the fixed-shape rows
from the names below.

## Captured output

```
module         functio
attention      1
data           0
dtype          14
gradient       2
gradus         0
loss           3
math           22
nn             6
optimize       0
parameter      37
serialize      34
shape          9
tensor         11
train          4
transformer    1
TOTAL          144
```

## Symbol detail

| Module | Count | `functio` names |
| --- | --- | --- |
| attention | 1 | `scaled_dot_product_2x8` |
| data | 0 | — (stub) |
| dtype | 14 | `f32`, `f16`, `i32`, `u8`, `causa`, `nomen`, `ex_nomine`, `amplitudo`, `serializa`, `deserializa`, `promovet`, `angusta`, `finita`, `casta` |
| gradient | 2 | `nil`, `simple_loss` |
| gradus | 0 | facade map only (no genera) |
| loss | 3 | `mse_2x2`, `mse_4x4`, `mse_2x8` |
| math | 22 | `causa`, `_forma_broadcast`, `_quantitas_valid`, `_index_broadcast`, `_index_axis`, `_coordinata`, `_planus_axis`, `_typo_par`, `structa`, `add`, `sub`, `mul`, `div`, `neg`, `abs`, `summa`, `media`, `matmul`, `_typus_ex_nomine`, `casta`, `concatenatio`, `segmentum` |
| nn | 6 | `linear_2x2`, `linear_4x4`, `gelu_4x4`, `linear_2x8`, `layernorm_2x8`, `gelu_2x8` |
| optimize | 0 | — (empty facade post-U6; sgd_step_* retired) |
| parameter | 37 | `statio_nomen`, `causa`, genus methods (`nomen`, `nomen_typi`, `figura`, `versio`, `possessor`, `identia`, `statio`, `quantitas`, `valor`, `numerus`, `contineo`, `inveni`, `trainabiles`, `gelidae`, `ordo`) + `identitas_aequus`, `_gelida`, `est_trainabilis`, `est_gelida`, `_structum`, `structa`, `structa_gelida`, `muta`, `registrum_vacuum`, `adscisco`, `_digitum`, `_numerica`, `_habeat_solidum`, `serializa`, `deserializa` |
| serialize | 34 | `causa`, `Tensum`/`ParametrumWire` methods (`typo`, `figura`, `datos`, `nomen`, `possessor`, `versio`, `statium`) + `_octeti_lista`, `_textus_bytes`, `_be4`, `_be8`, `_le4`, `_le8`, `_caput`, `_legere_textus`, `_quantitas`, `_gradus`, `_iunge_datos`, `_divido_datos`, `_tag_a`, `_nomen_a_tag`, `_habeat_solidum`, `serializa_dtype`, `serializa_shape`, `serializa_tensor`, `serializa_parametrum`, `deserializa_dtype`, `deserializa_shape`, `deserializa_tensor`, `deserializa_parametrum` |
| shape | 9 | `causa`, `valet`, `gradus`, `_productus`, `quantitas`, `_dimensio`, `broadcastum`, `reformanda`, `expansio` |
| tensor | 11 | genus methods (`figura`, `gradus`, `quantitas`, `typus`, `valet`, `accipe`) + `causa`, `_quantitas_forma`, `structa`, `structa_typo`, `impleta` |
| train | 4 | `train_step_2x2`, `train_step_4x4`, `train_step_bert_linear`, `train_step_bert_layernorm` |
| transformer | 1 | `bert_tiny_block_2x8` |

## Assertions (hold)

- Per-module counts for the seven fixed-shape proof-surface modules match the
  post-U6 live tree: attention 1, gradient 2, loss 3, nn 6, **optimize 0**,
  train 4, **transformer 1**.
- The tracked proof-surface total (the seven per-module-asserted modules)
  == **17**.
- The live all-module total (printed TOTAL row) == **144** — informational;
  foundation modules (dtype, math, parameter, serialize, shape, tensor) are
  versioned by their own contract docs (`dtype-schema-1.0.0`,
  `parameter-identity-schema-1.0.0`, `serialize-schema-1.0.0`, shape rules,
  math families) and the module-DAG re-snapshot.
- Zero-count modules (data stub, gradus facade) and the empty optimize facade
  are covered by the live table.

## Validation

```bash
cd /Users/ianzepp/work/faberlang/gradus
./scripta/inventory-public-symbols            # exit 0; per-module + tracked total 17 hold
diff <(./scripta/inventory-public-symbols) \
  <(awk 'BEGIN{n=0} /^```$/{n++; next} n==1{print} n>1{exit}' \
     docs/factory/production-ml-library/pml0-symbol-inventory.md)  # clean
grep -c 'functio ' src/{attention,gradient,loss,nn,optimize,train,transformer}.fab \
  | awk -F: '{s+=$2} END {print s}'   # 17 (tracked proof-surface total)
grep -c 'functio ' src/*.fab | awk -F: '{s+=$2} END {print s}'   # 144 (live all-module)
git diff --check
```

Outcome: `./scripta/inventory-public-symbols` exits 0 (per-module baseline and
tracked total 17 hold); a fresh run diffs clean against the captured output
above; the tracked proof-surface total == 17 and the live all-module total ==
144 match live grep; `git diff --check` clean.
