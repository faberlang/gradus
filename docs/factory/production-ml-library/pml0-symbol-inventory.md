# PML0/PML1/PML2 Public Symbol Inventory — gradus

**Unit**: PML0-U2 (public symbol inventory), re-baselined at PML1 closeout
and re-baselined for PML2 (auditor-2 fire-3 P2-3 — the model module and
tokenizer were missing from the prior baseline)
**Date**: 2026-08-08 (PML0) / 2026-08-09 (PML1 re-baseline; PML2 re-baseline;
grep only, no cargo)
**Source**: live `grep -c 'functio ' src/*.fab` + `src/model/*.fab` per
module — the scan is recursive so the PML2 model module (`src/model/`,
sub-leaves capsule/gguf/safetensors) is covered
**Method**: `scripta/inventory-public-symbols` — grep-based; counts `functio `
declaration lines per `src/*.fab` module (recursively, so `model/capsule`,
`model/gguf`, `model/safetensors` appear), prints the module → functio table
plus the all-module total, and asserts the re-baselined baseline: per-module
counts for the seven fixed-shape proof-surface modules (post-U6: optimize 0,
transformer 1) and for the model module's three sub-leaves, and the tracked
total **133** (proof-surface 17 + model module 116). The live all-module
total (printed TOTAL row) includes the foundation modules
(dtype/math/parameter/serialize/shape/tensor) that are versioned by their own
contract docs and schemas.
**Version stamps**: PML1 closeout at gradus HEAD (PML1-U1..U7 landed,
45a09d9..de017eb); PML2-U1..U3 landed (435ccd6, 07291d6, b392fc8) added
`src/model/`. The tokenizer module (`src/tokenizer.fab`, PML2-U4) is **in
flight** (hand-5, untracked at this re-baseline): its row is counted in the
live TOTAL but is **not asserted** (informational until it lands).
**Consumed by**: PML0-U3 (proof-shaped API ledger) feeds the fixed-shape rows
from the names below.

## Captured output

```
module           functio
attention        1
data             0
dtype            14
gradient         2
gradus           0
loss             3
math             22
model/capsule    79
model/gguf       14
model/safetensors 23
nn               6
optimize         0
parameter        37
serialize        34
shape            9
tensor           11
tokenizer        22
train            4
transformer      1
TOTAL            282
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
| model/capsule | 79 | six field-group accessors (bytes `corpus`/`longitudo`/`opertum`; crypta `algorithmus`/`digestio`/`longitudo_bytes`; tokenizator `progenies`/`pre_tokenizator`/`digestio_vocabuli`/`eog`/`bos_vacua`/`spatium_vacua`; quantizatio `typo`/`elementa_glomoris`/`octeti_glomoris`/`concordatio`/`quantizatio`; limites `machina`/`kv`/`tensores`/`nomen`/`dimensio`/`elementa`/`textus` + `limes_*` mirrors; architectura `identificator`/`densitas`/`strata`/`contextus`/`schematis`/`architectura`) + `causa`, `semita`, `identia`, `identitas_aequus`, `structa`, `verifica`, `verifica_contra`, `serializa_identitas`, `deserializa_identitas`, `_parsa` + 10 `@ privata` validators (`_est_hex`, `_hex_recta`, `_eog_recta`, `_est_digitum`, `_quantizatio_admissa`, `_quantizatio_recta`, `_limes_recti`, `_tokenizator_recta`, `_architectura_recta`) |
| model/gguf | 14 | `admit` (row → capsule, fail-closed) + `causa` + 12 `@ privata` GGUF parse helpers (`_legere_u32`, `_legere_u64`, `_legere_textus`, `_legere_string`, `_legere_bool`, `_scalar_magnitudo`, `_magnitudo_valoris`, `_clavis_admissa`, `_continet`, `_typo_admissus`, `_typo_elementa`, `_typo_octeti`) |
| model/safetensors | 23 | `admittas` (row → capsule, fail-closed) + `causa` + 21 `@ privata` header/JSON parse helpers (`_est_digitum`, `_est_hex`, `_est_sponte`, `_hex_recta`, `_le8`, `_caput`, `_lege_string`, `_lege_number`, `_scander`, `_typo`, `_valor`, `_parsa_integrum`, `_parsa_numerorum`, `_parsa_meta`, `_parsa_tensoris`, `_perambulare`, `_meta_quaero`, `_meta_exige`, `_inveni_nomen`, `_quantitas`, `_formae_aequae`) |
| nn | 6 | `linear_2x2`, `linear_4x4`, `gelu_4x4`, `linear_2x8`, `layernorm_2x8`, `gelu_2x8` |
| optimize | 0 | — (empty facade post-U6; sgd_step_* retired) |
| parameter | 37 | `statio_nomen`, `causa`, genus methods (`nomen`, `nomen_typi`, `figura`, `versio`, `possessor`, `identia`, `statio`, `quantitas`, `valor`, `numerus`, `contineo`, `inveni`, `trainabiles`, `gelidae`, `ordo`) + `identitas_aequus`, `_gelida`, `est_trainabilis`, `est_gelida`, `_structum`, `structa`, `structa_gelida`, `muta`, `registrum_vacuum`, `adscisco`, `_digitum`, `_numerica`, `_habeat_solidum`, `serializa`, `deserializa` |
| serialize | 34 | `causa`, `Tensum`/`ParametrumWire` methods (`typo`, `figura`, `datos`, `nomen`, `possessor`, `versio`, `statium`) + `_octeti_lista`, `_textus_bytes`, `_be4`, `_be8`, `_le4`, `_le8`, `_caput`, `_legere_textus`, `_quantitas`, `_gradus`, `_iunge_datos`, `_divido_datos`, `_tag_a`, `_nomen_a_tag`, `_habeat_solidum`, `serializa_dtype`, `serializa_shape`, `serializa_tensor`, `serializa_parametrum`, `deserializa_dtype`, `deserializa_shape`, `deserializa_tensor`, `deserializa_parametrum` |
| shape | 9 | `causa`, `valet`, `gradus`, `_productus`, `quantitas`, `_dimensio`, `broadcastum`, `reformanda`, `expansio` |
| tensor | 11 | genus methods (`figura`, `gradus`, `quantitas`, `typus`, `valet`, `accipe`) + `causa`, `_quantitas_forma`, `structa`, `structa_typo`, `impleta` |
| tokenizer | 22 | identity accessors (`schematis`, `progenies`, `pre_tokenizator`, `digestio_vocabuli`, `eog`, `bos_vacua`, `spatium_vacua`) + probe/verify surface (`proba_aequa`, `proba_ida`, `verifica_proba`, `pinnata_proba`, `structa`, `verifica`, `clavis_tokenizatoris`, `serializa_identitas`, `deserializa_identitas`) + `causa` + 5 `@ privata` helpers (`_est_hex`, `_hex_recta`, `_est_digitum`, `_eog_recta`, `_id_in_ambitu`) — **in flight** (hand-5); count informational |
| train | 4 | `train_step_2x2`, `train_step_4x4`, `train_step_bert_linear`, `train_step_bert_layernorm` |
| transformer | 1 | `bert_tiny_block_2x8` |

## Assertions (hold)

- Per-module counts for the seven fixed-shape proof-surface modules match the
  post-U6 live tree: attention 1, gradient 2, loss 3, nn 6, **optimize 0**,
  train 4, **transformer 1**.
- The PML2 model module (`src/model/`) is counted: model/capsule 79,
  model/gguf 14, model/safetensors 23.
- The tracked total (the seven per-module-asserted modules + the model module
  sub-leaves) == **133**.
- The live all-module total (printed TOTAL row) == **282** — informational;
  foundation modules (dtype, math, parameter, serialize, shape, tensor) are
  versioned by their own contract docs (`dtype-schema-1.0.0`,
  `parameter-identity-schema-1.0.0`, `serialize-schema-1.0.0`, shape rules,
  math families) and the module-DAG re-snapshot. The tokenizer row (22) is
  **not asserted** — PML2-U4 is in flight (hand-5); it is counted in the live
  TOTAL only.
- Zero-count modules (data stub, gradus facade) and the empty optimize facade
  are covered by the live table.

## Validation

```bash
cd /Users/ianzepp/work/faberlang/gradus
./scripta/inventory-public-symbols            # exit 0; per-module + tracked total 133 hold
diff <(./scripta/inventory-public-symbols) \
  <(awk 'BEGIN{n=0} /^```$/{n++; next} n==1{print} n>1{exit}' \
     docs/factory/production-ml-library/pml0-symbol-inventory.md)  # clean
grep -c 'functio ' src/{attention,gradient,loss,nn,optimize,train,transformer}.fab \
  | awk -F: '{s+=$2} END {print s}'   # 17 (tracked proof-surface total)
grep -c 'functio ' src/model/{capsule,gguf,safetensors}.fab \
  | awk -F: '{s+=$2} END {print s}'   # 116 (model module)
grep -c 'functio ' src/*.fab src/model/*.fab | awk -F: '{s+=$2} END {print s}'   # 282 (live all-module)
git diff --check
```

Outcome: `./scripta/inventory-public-symbols` exits 0 (per-module baseline and
tracked total 133 hold); a fresh run diffs clean against the captured output
above; the tracked proof-surface total == 17, the model module == 116, and the
live all-module total == 282 match live grep; `git diff --check` clean.
