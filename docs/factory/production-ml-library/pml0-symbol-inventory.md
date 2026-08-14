# PML0/PML1/PML2/PML3/PML4/PML5 Public Symbol Inventory — gradus

**Unit**: PML0-U2 (public symbol inventory), re-baselined at PML1 closeout,
re-baselined for PML2 (auditor-2 fire-3 P2-3 — the model module and tokenizer
were missing from the prior baseline), re-baselined for PML6-U1 (the
post-PML1–5 + correctness-wave surface: the training-layer modules PML4, the
inference modules PML5, the dequant sub-leaf, and the correctness-wave rename
`_le4/_le8` → `_be4_lege/_be8_lege`), and re-baselined for LIB-02-U1 (the
tokenizer metadata array accessors `textorum`/`numerorum` and the shared
`_numerum_scalarum` reader on `model/gguf_manifest`, plus the `attention`
`scaled_dot_product_staticum` delta that landed on main before this packet's
base)
**Date**: 2026-08-08 (PML0) / 2026-08-09 (PML1/PML2 re-baselines) /
2026-08-11 (PML6-U1 re-baseline) / 2026-08-12 (GGUF-A1b range seam; grep only,
no cargo) / 2026-08-14 (LIB-02-U1)
**Source**: live `grep -c 'functio ' src/*.fab` + `src/model/*.fab` per
module — the scan is recursive so the PML2 model module (`src/model/`,
sub-leaves artifact/capsule/dequant/gguf/gguf_manifest/safetensors) is covered
**Method**: `scripta/inventory-public-symbols` — grep-based; counts `functio `
declaration lines per `src/*.fab` module (recursively), prints the module →
functio table plus the all-module total, and asserts the re-baselined
baseline: per-module counts for **every live module** (27 modules: the
PML0/PML1 foundation and proof-surface modules, the PML2 model module's six
sub-leaves, the PML4 training-layer modules, and the PML5 inference modules)
and the tracked total **622** (the live all-module count — every module is
asserted, there is no untracked remainder). The script additionally runs the
**committed coverage gate** (PML6-U1, zombie-doc): every public `functio`
name (non-`_` prefix — `_`-prefixed names are `@ privata` module-internal
helpers) in every module appears in `docs/api-reference.md` under that
module's section, so no shipped public symbol is undocumented.
**Version stamps**: PML1 closeout at gradus HEAD (PML1-U1..U7 landed,
45a09d9..de017eb); PML2-U1..U4 landed (435ccd6, 07291d6, b392fc8, and the
tokenizer module) added `src/model/` and `src/tokenizer.fab`; PML3–PML5
landed the production nn/attention/transformer surface and the training +
inference modules; the correctness wave (`3c295c0`, `6cc0eb5`, `2cdc498`,
`0d50d60`) renamed the serialize big-endian readers and pinned the EOG-set
admission semantics. GGUF-A1a adds the pathless artifact identity and
format-general GGUF manifest/parser leaves; GGUF-A1b adds the range-source and
checked tensor-fragment functions. LIB-02-U1 adds the schema-2 tokenizer
metadata array accessors (`textorum`/`numerorum`) and the shared
`_numerum_scalarum` scalar reader on `model/gguf_manifest`. This inventory
remains a structural count.
**Consumed by**: PML0-U3 (proof-shaped API ledger) feeds the fixed-shape rows
from the names below; `docs/api-reference.md` (PML6-U1) documents every
public symbol on this inventory.

## Captured output

```
module           functio
attention        21
cache            37
data             0
decode           46
dtype            14
generation       27
gradient         13
gradus           7
loss             11
math             23
metrics          6
model/artifact   4
model/capsule    79
model/dequant    18
model/gguf_manifest 45
model/gguf       14
model/safetensors 23
nn               17
optimize         26
parameter        37
sampling         27
serialize        34
shape            9
tensor           11
tokenizer        23
train            41
transformer      9
TOTAL            622
```

## Symbol detail

Public symbol names per module (the coverage gate's surface; the count
column is the module's **total** `functio` lines including `@ privata`
helpers, matching the captured output):

| Module | Count | Public `functio` names |
| --- | --- | --- |
| attention | 21 | `scaled_dot_product_2x8`, `scaled_dot_product_staticum`, `causa`, `rotary_position_embedding`, `scaled_dot_product`, `scaled_dot_product_causal`, `scaled_dot_product_causal_rope` (14 `@ privata` helpers) |
| cache | 37 | `causa`, `cache_aequus`, `cache_vacua`, `appende`, `redintegra`, `identitas_cache_aequus`, `identitas_cache`, `serializa_identitas`, `deserializa_identitas` + KVCache/IdentitasCache genus methods (`model`, `versio_modelis`, `configuratio`, `tokenizator`, `historia`, `stratorum`, `typo`, `ordinatio`, `clavis`, `valor`, `versio`, `dimensio`, `longitudo`, `positio`) (6 `@ privata` helpers) |
| data | 0 | — (stub) |
| decode | 46 | `causa`, `structa_pondera`, `structa_decodere`, `decodere_datum`, `praefundere`, `sessio_fresh`, `progredere`, `redintegra`, `cancelatum_fresh`, `cancelatum_cancellata`, `observa_cancellationem`, `replica` + Pondera/Decodere/Sessio/Cancelatum genus methods (`ln1_s`, `ln1_o`, `wq`, `bq`, `wk`, `bk`, `wv`, `bv`, `wo`, `bo`, `ln2_s`, `ln2_o`, `wf1`, `bf1`, `wf2`, `bf2`, `ln3_s`, `ln3_o`, `mensa`, `pondera`, `projectio`, `projectio_bias`, `scala`, `vocabulum`, `contextus`, `dimensio`, `positio`, `cancellata`) (5 `@ privata` helpers) |
| dtype | 14 | `f32`, `f16`, `i32`, `u8`, `causa`, `nomen`, `ex_nomine`, `amplitudo`, `serializa`, `deserializa`, `promovet`, `angusta`, `finita`, `casta` |
| generation | 27 | `causa`, `generatio_aequus`, `structa_generatio`, `generatio_defecta`, `imperia_subsidia`, `imperium_admissum`, `configura`, `semen`, `serializa_generatio`, `deserializa_generatio`, `cursor_fresh`, `verbum_licet`, `cursor_progredere`, `cursor_redintegra` + GeneratioConfigura/GenereCursor genus methods (`contextus`, `magna_promptus`, `maxima_verborum`, `semen`, `temperatura`, `top_k`, `top_p`, `min_p`, `poena_repetitionis`, `sessio`, `prolata`) (2 `@ privata` helpers) |
| gradient | 13 | `causa`, `structa`, `structa_gradientes`, `obsoletus`, `nil`, `simple_loss`, `gradientes_simple_loss` + Gradiente/Gradientes genus methods (`possessor`, `nomen`, `versio`, `valor`, `numerus`, `inveni`) |
| gradus | 7 | `causa`, `forward_mlp`, `nil`, `forward_mlp_loss` (3 `@ privata` helpers) |
| loss | 11 | `causa`, `mse`, `cross_entropy`, `mse_2x2`, `mse_4x4`, `mse_2x8` (5 `@ privata` helpers) |
| math | 23 | `causa`, `structa`, `add`, `sub`, `mul`, `div`, `neg`, `abs`, `signum`, `summa`, `media`, `matmul`, `casta`, `concatenatio`, `segmentum` (8 `@ privata` helpers) |
| metrics | 6 | `causa`, `accuratezza`, `metricum`, `metrica_aequus` + Metricum genus methods (`damnum`, `accuratezza`) |
| model/artifact | 4 | `causa`, `identitas` (2 `@ privata` validators) |
| model/capsule | 79 | `causa`, `identitas_aequus`, `structa`, `verifica`, `verifica_contra`, `serializa_identitas`, `deserializa_identitas` + the six field-group genus methods (BytesValida: `corpus`, `longitudo`, `opertum`; IdentitasCrypto: `algorithmus`, `digestio`; IdentitasTokenizer: `progenies`, `pre_tokenizator`, `digestio_vocabuli`, `eog`, `bos_vacua`, `spatium_vacua`; Quantizatio: `typo`, `elementa_glomoris`, `octeti_glomoris`, `concordatio`; Limites: `machina`, `kv`, `tensores`, `nomen`, `dimensio`, `elementa`, `textus`; Architectura: `identificator`, `densitas`, `strata`, `contextus`; Identitas: `schematis`, `algorithmus`, `digestio`, `longitudo_bytes`, `quantizatio`, `architectura`, `strata`; Capsula: `schematis`, `corpus`, `longitudo`, `opertum`, `algorithmus`, `digestio`, `progenies`, `pre_tokenizator`, `digestio_vocabuli`, `eog`, `bos_vacua`, `spatium_vacua`, `quantizatio`, `elementa_glomoris`, `octeti_glomoris`, `concordatio`, `limes_machinae`, `limes_kv`, `limes_tensorum`, `limes_nominis`, `limes_dimensionis`, `limes_elementorum`, `limes_textus`, `identificator`, `densitas`, `strata`, `contextus`, `semita`, `identia`) (10 `@ privata` validators) |
| model/dequant | 18 | `causa`, `elementa_glomoris`, `octeti_glomoris`, `dequantizas_glomulus`, `dequantizas_ordo` (13 `@ privata` helpers) |
| model/gguf | 14 | `admit` (row → capsule, fail-closed) + `causa` + 12 `@ privata` GGUF parse helpers |
| model/gguf_manifest | 45 | `causa`, `layout`, `metadatum`, `textum`, `numerum`, `textorum`, `numerorum`, `inveni_tensorem`, `parse`, `inspice`, `lege_fragmentum` + 34 `@ privata` bounded-wire/range/layout helpers (incl. the shared `_numerum_scalarum` scalar reader) |
| model/safetensors | 23 | `admittas` (row → capsule, fail-closed) + `causa` + 21 `@ privata` header/JSON parse helpers |
| nn | 17 | `linear_2x2`, `linear_4x4`, `gelu_4x4`, `linear_2x8`, `layernorm_2x8`, `gelu_2x8`, `causa`, `linear`, `gelu`, `layernorm` (7 `@ privata` helpers) |
| optimize | 26 | `causa`, `statum_aequus`, `structa`, `sgd_aequus`, `sgd_vacuum`, `adscisco`, `passus`, `serializa_statum`, `deserializa_statum`, `serializa`, `deserializa` + SgdStatum/Sgd/Passus genus methods (`possessor`, `nomen`, `versio`, `generatio`, `passus`, `lentus`, `numerus`, `contineo`, `inveni`, `novus`, `statum`) (4 `@ privata` helpers) |
| parameter | 37 | `statio_nomen`, `causa`, `identitas_aequus`, `est_trainabilis`, `est_gelida`, `structa`, `structa_gelida`, `muta`, `registrum_vacuum`, `adscisco`, `serializa`, `deserializa` + Identitas/Parametrum/Registrum genus methods (`nomen`, `nomen_typi`, `figura`, `versio`, `possessor`, `identia`, `statio`, `quantitas`, `valor`, `numerus`, `contineo`, `inveni`, `trainabiles`, `gelidae`, `ordo`) (5 `@ privata` helpers) |
| sampling | 27 | `causa`, `structa_configura`, `maxima`, `distributio`, `sors` + Configura/Sortitio genus methods (`temperatura`, `top_k`, `top_p`, `min_p`, `poena_repetitionis`, `token_id`, `semen`) (15 `@ privata` helpers) |
| serialize | 34 | `causa`, `serializa_dtype`, `serializa_shape`, `serializa_tensor`, `serializa_parametrum`, `deserializa_dtype`, `deserializa_shape`, `deserializa_tensor`, `deserializa_parametrum` + Tensum/ParametrumWire genus methods (`typo`, `figura`, `datos`, `nomen`, `possessor`, `versio`, `statium`) (15 `@ privata` helpers, incl. the renamed `_be4_lege` / `_be8_lege` big-endian readers — correctness wave `3c295c0`) |
| shape | 9 | `causa`, `valet`, `gradus`, `quantitas`, `broadcastum`, `reformanda`, `expansio` (2 `@ privata` helpers) |
| tensor | 11 | `causa`, `structa`, `structa_typo`, `impleta` + Tensor genus methods (`figura`, `gradus`, `quantitas`, `typus`, `valet`, `accipe`) (1 `@ privata` helper) |
| tokenizer | 23 | `est_eog`, `causa`, `proba_aequa`, `proba_ida`, `verifica_proba`, `pinnata_proba`, `structa`, `verifica`, `clavis_tokenizatoris`, `serializa_identitas`, `deserializa_identitas` + IdentitasTokenizator genus methods (`schematis`, `progenies`, `pre_tokenizator`, `digestio_vocabuli`, `eog`, `bos_vacua`, `spatium_vacua`) (5 `@ privata` helpers) |
| train | 41 | `train_step_2x2`, `train_step_4x4`, `train_step_bert_linear`, `train_step_bert_layernorm`, `causa`, `structa_schedula`, `lentus_schedulata`, `modus_nomen`, `est_disciplina`, `est_aestimatio`, `modus`, `dropout_pars`, `structa_semen`, `proximus`, `proximus_f32`, `excutio`, `serializa_semen`, `deserializa_semen`, `structa_tabula`, `tabula_aequus`, `serializa_tabula`, `deserializa_tabula` + Schedula/Semen/Fructus/FructusF32/Excutio/Tabula genus methods (`lentus_vertex`, `incalesco`, `passus_total`, `lentus_finis`, `status`, `valor`, `semen`, `aetas`, `passus`, `rng`, `statum_wire`) (4 `@ privata` helpers) |
| transformer | 9 | `bert_tiny_block_2x8`, `causa`, `transformer_block` (6 `@ privata` helpers) |

## Assertions (hold)

- Per-module counts for **all 27 live modules** match the live tree exactly
  (captured output above): foundation and proof-surface modules
  (attention 21, data 0, dtype 14, gradient 13, gradus 7, loss 11, math 23,
  nn 17, optimize 26, parameter 37, serialize 34, shape 9, tensor 11,
  transformer 9), the PML4 training-layer modules (metrics 6, train 41), the
  PML5 inference modules (cache 37, decode 46, generation 27, sampling 27),
  and the PML2 model module (`model/artifact` 4, `model/capsule` 79,
  `model/dequant` 18, `model/gguf` 14, `model/gguf_manifest` 45,
  `model/safetensors` 23) + tokenizer 23.
- The tracked total == the live all-module total == **622**; every module is
  asserted (no untracked remainder).
- The **coverage gate** holds: every public symbol name above appears in
  `docs/api-reference.md` under its module's `## gradus:<module>` section —
  no shipped public symbol is undocumented (zombie-doc gate, PML6-U1).
- Zero-count modules (data stub) and the facade module (gradus — public
  convenience functions, no genera) are covered by the live table.
- Private `_`-prefixed helpers are excluded from the public surface; the two
  renamed serialize readers (`_be4_lege`, `_be8_lege`) are additionally
  documented in the API reference per the correctness-wave reconciliation.

## Validation

```bash
cd /Users/ianzepp/work/faberlang/gradus
./scripta/inventory-public-symbols            # exit 0; per-module counts + total 622 + coverage gate
diff <(./scripta/inventory-public-symbols) \
  <(awk 'BEGIN{n=0} /^```$/{n++; next} n==1{print} n>1{exit}' \
     docs/factory/production-ml-library/pml0-symbol-inventory.md)  # clean
grep -c 'functio ' src/*.fab src/model/*.fab | awk -F: '{s+=$2} END {print s}'   # 622 (live all-module)
git diff --check
```

Outcome: `./scripta/inventory-public-symbols` exits 0 (per-module baseline
and tracked total 622 hold; every public symbol is documented in
`docs/api-reference.md`); a fresh run diffs clean against the captured output
above; the live all-module total == 622 matches live grep; `git diff --check`
clean.
