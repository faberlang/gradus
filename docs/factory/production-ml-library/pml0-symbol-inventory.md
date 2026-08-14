# PML0/PML1/PML2/PML3/PML4/PML5 Public Symbol Inventory — gradus

**Unit**: PML0-U2 (public symbol inventory), re-baselined at PML1 closeout,
re-baselined for PML2 (auditor-2 fire-3 P2-3 — the model module and tokenizer
were missing from the prior baseline), re-baselined for PML6-U1 (the
post-PML1–5 + correctness-wave surface: the training-layer modules PML4, the
inference modules PML5, the dequant sub-leaf, and the correctness-wave rename
`_le4/_le8` → `_be4_lege/_be8_lege`), re-baselined for GGUF-A1c (the
capsule-schema-2.0.0 surface: capsule 45, gguf 10, safetensors 24; attention
21 — the static-shape generic `scaled_dot_product_staticum` was added after
the A1b capture and counts since), re-baselined for LIB-02-U1 (the
tokenizer metadata array accessors `textorum`/`numerorum` and the shared
`_numerum_scalarum` reader on `model/gguf_manifest`), re-baselined for
GGUF-A3 C3-U6 (the final GGUF-A3 inventory baseline: the
`model/tensor_payload` + `model/tensor_view` modules, the widened
`model/dequant` union set — BF16/Q5_K codecs — and `limes_payloadis` on
`model/gguf_manifest`), and re-baselined for LIB-02-U3/U4 (the qwen35
pre-tokenizer scanner + special/EOG/BOS/chat policy surface and the
two-probe composition — tokenizer 37 → 74, total 611 → 648), and
re-baselined for MODEL-01-M9 (the qwen35moe admission surface:
`model/qwen35moe` 42, `model/gguf_manifest` 46 → 49 M1 typed accessors,
total 648 → 693)
**Date**: 2026-08-08 (PML0) / 2026-08-09 (PML1/PML2 re-baselines) /
2026-08-11 (PML6-U1 re-baseline) / 2026-08-12 (GGUF-A1b range seam; grep only,
no cargo) / 2026-08-13 (GGUF-A1c A1C-M6 re-baseline) / 2026-08-14 (LIB-02-U1)
/ 2026-08-14 (GGUF-A3 C3-U6 final inventory baseline) / 2026-08-14
(LIB-02-U3/U4 qwen35 pre-tokenizer + policy-surface re-baseline) / 2026-08-14
(MODEL-01-M9 qwen35moe admission re-baseline)
**Source**: live `grep -c 'functio ' src/*.fab` + `src/model/*.fab` per
module — the scan is recursive so the PML2 model module (`src/model/`,
sub-leaves artifact/capsule/dequant/gguf/gguf_manifest/qwen35moe/
safetensors/tensor_payload/tensor_view) is covered
**Method**: `scripta/inventory-public-symbols` — grep-based; counts `functio `
declaration lines per `src/*.fab` module (recursively), prints the module →
functio table plus the all-module total, and asserts the re-baselined
baseline: per-module counts for **every live module** (30 modules: the
PML0/PML1 foundation and proof-surface modules, the PML2 model module's
nine sub-leaves, the PML4 training-layer modules, and the PML5 inference
modules) and the tracked total **693** (the live all-module count — every
module is asserted, there is no untracked remainder). The script
additionally runs the
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
checked tensor-fragment functions; GGUF-A1c (A1C-M1..M3, landed on the
`factory/a1c-chain` merge branch) rewrote `capsule.fab` to
capsule-schema-2.0.0, made `gguf.admit` a thin wrapper over `gguf_manifest`,
and migrated `safetensors.admittas` to the schema-2 capsule. LIB-02-U1 adds
the schema-2 tokenizer metadata array accessors (`textorum`/`numerorum`) and
the shared `_numerum_scalarum` scalar reader on `model/gguf_manifest`.
GGUF-A3 C2+C3 add the packed-storage surface: `model/tensor_payload` (C2-U2)
and `model/tensor_view` (C2-U3..U5) modules, the widened `model/dequant`
union set (BF16 + Q5_K codecs, A3-C1 `82048b5`) and `limes_payloadis`
(A3-C2-U1) on `model/gguf_manifest`; the C3-U6 re-baseline is the final
GGUF-A3 inventory baseline (29 modules / 611). LIB-02-U3/U4 add the qwen35
pre-tokenizer surface (`categoria`/`est_littera`/`est_signum`/`est_numerus`/
`est_spatium`/`est_novum_linea`/`est_aliud`/`categoria_nomen`/`scanna_verba`),
the special/EOG/BOS/chat policy surface
(`encoda_promptum`/`encoda_promptum_specialia`/`eog_artificii`/
`est_eog_artificii`/`add_bos`/`chat_template`/`redde_turnum_user`), and the
two-probe composition oracle (`fixtures/tokenizer/pinned-probe-oracle.md` +
`chat-template-identity-oracle.md`); the re-baseline is the merged
LIB-02+GGUF-A3 inventory baseline (29 modules / 648). MODEL-01 M3..M6
(`0f70590`, `9e015b4`, `f3683b1`, `0c28ca3`/`227ca74`) add the qwen35moe
admission module (`src/model/qwen35moe.fab` — configuration genus + frozen
config, canonical 753-tensor map + block schedule, dimension/storage
cross-reference validation, identity-precondition admission + typed refusal
matrix) and M1 (`5f93ef7`) adds the typed array-of-uint32 / bool /
array-length accessors (`numerorum_u32`/`boleanum`/`longitudo_listae`) on
`model/gguf_manifest`; the MODEL-01-M9 re-baseline is the MODEL-01 inventory
baseline (30 modules / 693). This
inventory remains a structural count.
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
model/capsule    45
model/dequant    21
model/gguf_manifest 49
model/gguf       10
model/qwen35moe  42
model/safetensors 24
model/tensor_payload 1
model/tensor_view 7
nn               17
optimize         26
parameter        37
sampling         27
serialize        34
shape            9
tensor           11
tokenizer        74
train            41
transformer      9
TOTAL            693
```

## Symbol detail

Public symbol names per module (the coverage gate's surface; the count
column is the module's **total** `functio` lines including `@ privata`
helpers, matching the captured output):

| Module | Count | Public `functio` names |
| --- | --- | --- |
| attention | 21 | `scaled_dot_product_2x8`, `scaled_dot_product_staticum`, `causa`, `rotary_position_embedding`, `scaled_dot_product`, `scaled_dot_product_causal`, `scaled_dot_product_causal_rope` (14 `@ privata` helpers; `scaled_dot_product_staticum` is a shape-generics P2 addition that landed after the A1b capture — see the coverage-gate note below) |
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
| model/capsule | 45 | `causa`, `identitas_aequus`, `verifica`, `verifica_contra`, `structa_manifestum`, `serializa_identitas`, `deserializa_identitas`, `manifestum_gguf`, `manifestum_safetensors` + the schema-2 genus methods (MetadatumSafetensori: `clavis`, `valor`; DescriptioTensorisSafetensori: `nomen`, `typo`, `forma`, `initium`, `finis`, `elementa`; ManifestumSafetensors: `formatum`, `versio`, `longitudo_artefacti`, `longitudo_datorum`, `metadatorum_numerus`, `tensorum_numerus`, `metadatum`, `descriptio`; Capsula: `schematis`, `identitas_artificii`, `algorithmus`, `digestio`, `longitudo`, `formatum`, `tensorum_numerus`, `manifestum_gguf`, `manifestum_safetensors`, `identia`; Identitas: `schematis`, `algorithmus`, `digestio`, `longitudo_bytes`) (6 `@ privata` validators) |
| model/dequant | 21 | `causa`, `elementa_glomoris`, `octeti_glomoris`, `dequantizas_glomulus`, `dequantizas_ordo` (16 `@ privata` helpers; the GGUF-A3 union-set widening adds the BF16/Q5_K block codecs `_bfloat16`/`_dequant_bf16`/`_dequant_q5_k`, `82048b5`) |
| model/gguf | 10 | `admit` (thin schema-2 wrapper over `manifestum`, D3) + `causa` + 8 `@ privata` bounded-wire/contract helpers |
| model/gguf_manifest | 49 | `causa`, `layout`, `metadatum`, `textum`, `numerum`, `textorum`, `numerorum`, `numerorum_u32`, `boleanum`, `longitudo_listae`, `inveni_tensorem`, `limes_payloadis`, `parse`, `inspice`, `lege_fragmentum` + 34 `@ privata` bounded-wire/range/layout helpers (incl. the shared `_numerum_scalarum` scalar reader; `numerorum_u32`/`boleanum`/`longitudo_listae` are the MODEL-01-M1 typed u32-array/bool/array-length accessors, `5f93ef7`; `limes_payloadis` is the A3-C2-U1 payload-range seam `tensor_view.vincula` binds against) |
| model/qwen35moe | 42 | `causa`, `causa_tensorum`, `tensores_canonici`, `causa_referantiae`, `referantia`, `congela`, `causa_admissionis`, `admitto` (configuration genus + frozen config, canonical 753-tensor map + block schedule, dimension/storage cross-reference validation, identity-precondition admission + typed refusal matrix — MODEL-01 M3..M6) + 34 `@ privata` helpers |
| model/safetensors | 24 | `admittas` (schema-2 capsule with `ManifestumSafetensors`, D4) + `causa` + 22 `@ privata` header/JSON parse helpers |
| model/tensor_payload | 1 | `causa` (TensorPayload value carrier + PayloadError diagnostics, C2-U2 `e640a50`) |
| model/tensor_view | 7 | `causa`, `vincula`, `materializa_slicem`, `materializa_glomulum` (3 `@ privata` helpers `_descriptio`/`_limes`/`_fons_lege`; the bounded windowed materializers, C2-U3..U5 `6dd29fb`/`686653c`/`d182c5c`) |
| nn | 17 | `linear_2x2`, `linear_4x4`, `gelu_4x4`, `linear_2x8`, `layernorm_2x8`, `gelu_2x8`, `causa`, `linear`, `gelu`, `layernorm` (7 `@ privata` helpers) |
| optimize | 26 | `causa`, `statum_aequus`, `structa`, `sgd_aequus`, `sgd_vacuum`, `adscisco`, `passus`, `serializa_statum`, `deserializa_statum`, `serializa`, `deserializa` + SgdStatum/Sgd/Passus genus methods (`possessor`, `nomen`, `versio`, `generatio`, `passus`, `lentus`, `numerus`, `contineo`, `inveni`, `novus`, `statum`) (4 `@ privata` helpers) |
| parameter | 37 | `statio_nomen`, `causa`, `identitas_aequus`, `est_trainabilis`, `est_gelida`, `structa`, `structa_gelida`, `muta`, `registrum_vacuum`, `adscisco`, `serializa`, `deserializa` + Identitas/Parametrum/Registrum genus methods (`nomen`, `nomen_typi`, `figura`, `versio`, `possessor`, `identia`, `statio`, `quantitas`, `valor`, `numerus`, `contineo`, `inveni`, `trainabiles`, `gelidae`, `ordo`) (5 `@ privata` helpers) |
| sampling | 27 | `causa`, `structa_configura`, `maxima`, `distributio`, `sors` + Configura/Sortitio genus methods (`temperatura`, `top_k`, `top_p`, `min_p`, `poena_repetitionis`, `token_id`, `semen`) (15 `@ privata` helpers) |
| serialize | 34 | `causa`, `serializa_dtype`, `serializa_shape`, `serializa_tensor`, `serializa_parametrum`, `deserializa_dtype`, `deserializa_shape`, `deserializa_tensor`, `deserializa_parametrum` + Tensum/ParametrumWire genus methods (`typo`, `figura`, `datos`, `nomen`, `possessor`, `versio`, `statium`) (15 `@ privata` helpers, incl. the renamed `_be4_lege` / `_be8_lege` big-endian readers — correctness wave `3c295c0`) |
| shape | 9 | `causa`, `valet`, `gradus`, `quantitas`, `broadcastum`, `reformanda`, `expansio` (2 `@ privata` helpers) |
| tensor | 11 | `causa`, `structa`, `structa_typo`, `impleta` + Tensor genus methods (`figura`, `gradus`, `quantitas`, `typus`, `valet`, `accipe`) (1 `@ privata` helper) |
| tokenizer | 74 | `est_eog`, `causa`, `proba_aequa`, `proba_ida`, `verifica_proba`, `pinnata_proba`, `structa`, `verifica`, `clavis_tokenizatoris`, `serializa_identitas`, `deserializa_identitas`, `fabricare`, `encoda`, `decoda` + IdentitasTokenizator genus methods (`schematis`, `progenies`, `pre_tokenizator`, `digestio_vocabuli`, `eog`, `bos_vacua`, `spatium_vacua`) + the LIB-02-U3/U4 qwen35 pre-tokenizer + policy surface (`categoria`, `est_littera`, `est_signum`, `est_numerus`, `est_spatium`, `est_novum_linea`, `est_aliud`, `categoria_nomen`, `scanna_verba`, `encoda_promptum`, `encoda_promptum_specialia`, `eog_artificii`, `est_eog_artificii`, `add_bos`, `chat_template`, `redde_turnum_user`) (37 `@ privata` helpers; the LIB-02-U2 artifact-backed byte-level BPE runtime adds `fabricare`/`encoda`/`decoda`; U3/U4 add the qwen35 scanner families + special/EOG/BOS/chat policy surface) |
| train | 41 | `train_step_2x2`, `train_step_4x4`, `train_step_bert_linear`, `train_step_bert_layernorm`, `causa`, `structa_schedula`, `lentus_schedulata`, `modus_nomen`, `est_disciplina`, `est_aestimatio`, `modus`, `dropout_pars`, `structa_semen`, `proximus`, `proximus_f32`, `excutio`, `serializa_semen`, `deserializa_semen`, `structa_tabula`, `tabula_aequus`, `serializa_tabula`, `deserializa_tabula` + Schedula/Semen/Fructus/FructusF32/Excutio/Tabula genus methods (`lentus_vertex`, `incalesco`, `passus_total`, `lentus_finis`, `status`, `valor`, `semen`, `aetas`, `passus`, `rng`, `statum_wire`) (4 `@ privata` helpers) |
| transformer | 9 | `bert_tiny_block_2x8`, `causa`, `transformer_block` (6 `@ privata` helpers) |

## Assertions (hold)

- Per-module counts for **all 30 live modules** match the live tree exactly
  (captured output above): foundation and proof-surface modules
  (attention 21, data 0, dtype 14, gradient 13, gradus 7, loss 11, math 23,
  nn 17, optimize 26, parameter 37, serialize 34, shape 9, tensor 11,
  transformer 9), the PML4 training-layer modules (metrics 6, train 41), the
  PML5 inference modules (cache 37, decode 46, generation 27, sampling 27),
  and the PML2 model module (`model/artifact` 4, `model/capsule` 45,
  `model/dequant` 21, `model/gguf` 10, `model/gguf_manifest` 49,
  `model/qwen35moe` 42, `model/safetensors` 24, `model/tensor_payload` 1,
  `model/tensor_view` 7) + tokenizer 74.
- The tracked total == the live all-module total == **693**; every module is
  asserted (no untracked remainder).
- The **coverage gate** holds: every public symbol name above appears in
  `docs/api-reference.md` under its module's `## gradus:<module>` section —
  no shipped public symbol is undocumented (zombie-doc gate, PML6-U1).
  Known gate blind spot (unchanged, pre-existing): the gate's name regex
  (`functio [a-z][a-z0-9_]*\(`) does not match generic signatures
  (`name<...>(`), so `attention.scaled_dot_product_staticum` (shape-generics
  P2, landed after the A1b capture) is counted here but not yet documented in
  `docs/api-reference.md`; it belongs to the shape-generics delivery, not
  A1C, and is tracked here for M8/planner-39 visibility.
  MODEL-01-M9 tracked gap (routed, not masked): the three M1 typed accessors
  `model/gguf_manifest.numerorum_u32` / `.boleanum` / `.longitudo_listae`
  (`5f93ef7`, `@ publica`) are counted here but not yet documented in
  `docs/api-reference.md` — the inventory coverage gate exits non-zero on
  them until the api-reference coverage lands; `docs/api-reference.md` is
  outside M9's write scope, so this is routed to Mind as an M8-completion
  gap (M1's gate row requires "M8's api-reference coverage"; M8's outcome
  promises "+ any M1 accessor").
- Zero-count modules (data stub) and the facade module (gradus — public
  convenience functions, no genera) are covered by the live table.
- Private `_`-prefixed helpers are excluded from the public surface; the two
  renamed serialize readers (`_be4_lege`, `_be8_lege`) are additionally
  documented in the API reference per the correctness-wave reconciliation.

## Validation

```bash
cd /Users/ianzepp/work/faberlang/gradus
./scripta/inventory-public-symbols            # count assertions + total 693 pass; coverage gate exits non-zero on the M1 accessors (routed gap, see Assertions)
diff <(./scripta/inventory-public-symbols) \
  <(awk 'BEGIN{n=0} /^```$/{n++; next} n==1{print} n>1{exit}' \
     docs/factory/production-ml-library/pml0-symbol-inventory.md)  # clean
grep -c 'functio ' src/*.fab src/model/*.fab | awk -F: '{s+=$2} END {print s}'   # 693 (live all-module)
git diff --check
```

Outcome: `./scripta/inventory-public-symbols` count assertions pass (per-module
baseline and tracked total 693 hold; the fresh run's captured output above
matches verbatim); the live all-module total == 693 matches live grep;
`git diff --check` clean. The script's committed coverage gate exits non-zero
on the three MODEL-01-M1 `model/gguf_manifest` accessors (`boleanum` /
`longitudo_listae` / `numerorum_u32`) until their `docs/api-reference.md`
coverage lands — an M8-completion gap routed to Mind (the gate must not be
weakened to mask undocumented public symbols).
