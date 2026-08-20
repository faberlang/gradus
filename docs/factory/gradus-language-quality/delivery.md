# Delivery: gradus-language-quality

**Goal:** `docs/factory/gradus-language-quality/GOAL.md` (READY — see planner
report on task `59369675`)
**Planner:** planner (Vivi), 2026-08-20
**Base:** gradus `main` `f70f02f` (clean); faber `606d58c` (audit authority)
**Units:** 17 (16 dispatchable now or by dependency; GLQ-13 decision-pending)

## 1. Interpreted theme / problem

Two completed audits (idiom `57cb4713`, presentability `7d54686c`) describe one
theme: gradus works but does not speak the canonical idiom of its own language,
and its public surface misrepresents the library it ships. The operator ordered
one goal with individual unit tracking — no campaign.

## 2. Normalized spec (delivery-sized outcome)

All audit remediation batches lower to one-logical-change Hand units on gradus
plus one faber docs unit, under five standing constraints from the task:

1. Grammar gaps route to the radix-side findings list recorded in GOAL.md
   (Out of scope) — no gradus unit works around a missing capability.
2. EBNF staleness ×3 is its own small faber-side docs unit (GLQ-17).
3. LICENSE (audit Batch C) is decision-pending — unit exists, content not
   lowered; not dispatchable until the operator rules.
4. Glyph conversions are core-type-only; carrier `math.matmul` calls and the
   excluded method families stay methods.
5. Binding-hole units (GLQ-06) land after the in-flight radix size-param
   type-args repair and parser fix settle.

## 3. Repo-aware baseline

- Sites and file:line evidence: audit mails `57cb4713` / `7d54686c` (per-class
  tables); planner re-verified the headline claims at `f70f02f` (GOAL.md
  Ground Truth).
- Precedent method for safe mechanical conversion: the no-latin campaign
  (re-opened 2026-08-20) — exact identifier-boundary replacements,
  first-file compile confirmation, per-wave lane-gate closes
  (`docs/factory/no-latin/GOAL.md`).
- Name map for prose sweeps: `docs/factory/no-latin/rename-ledger.md`.
- Enforcement: `scripta/check-source` U8 guard (lexicon-based; currently misses
  `staticum`/`addita`/`conversio`; its ledger-path comment resolves to the
  re-opened `docs/factory/no-latin/rename-ledger.md` — no GLQ-10 path fix).
- Borrowed shapes: `../norma/README.md` (install section),
  `../triga/README.md` (Start-here quickstart).
- Idle lane note: `worktrees/hand-13` sits on `main` at `f70f02f` with no WIP —
  reusable or retirable; Mind's call.

## 4. Hand unit graph

Every unit is `integrable: yes` (each lands alone as a complete
behavior-preserving change; no aggregate landing gate needed beyond lane
validation). Lane gates are named once in §6 and are **not** child checks.

---

### GLQ-01 — glyph conversion, fragment files

- **outcome**: Convert the 27 glyph-eligible method sites on static core
  tensors in `src/transformer.fab`, `src/attention.fab`, `src/gradus.fab`,
  `src/loss.fab`, `src/gradient.fab` (+ `src/attention.proba` mirror sites
  `:791-794`): `.matmul(w)` → `a · w`, `.multiply(x)` → `a ⊙ x`,
  `.subtract(x)` → `a - x`. Per-file site lines: transformer matmul
  `:68,70,72,77,80,83,91,94` + multiply `:78`; attention `:59,60,62,79,80,82`;
  gradus `:239,242,244,245`; loss `:380,381,390,391,400,401`; gradient
  `:228,298` — the audit mail's class-1 tables are the site authority.
- **write_scope**: `src/transformer.fab`, `src/attention.fab`, `src/gradus.fab`,
  `src/loss.fab`, `src/gradient.fab`, `src/attention.proba`.
- **done_when**: zero receiver-call sites `.matmul(`/`.multiply(`/`.subtract(`
  in those files (free `math.matmul(` carrier calls exempt — attention
  `:659,662,744,1039,1042`; nn `:497`); `·`/`⊙` forms present at the audit's
  site lines; proba mirrors updated.
- **depends_on**: GLQ-10 (same-file sequencing on `attention.fab`).
- **sanity**: diff site count matches the audit's per-file table (27); eyeball
  one converted function end-to-end (e.g. `src/gradus.fab:239-246` becomes
  single-idiom); `"$FABER_BIN" check "$PWD/src/transformer.fab"` (absolute
  path) green on a converted file.
- **non_goals**: carrier `math.matmul` free calls; `.softmax/.gelu/.mean/
  .transpose/.layer_norm/.added_bias/.scale` and scalar `.abs` families;
  proba-only behavior changes.
- **risk**: low — mechanical, static-shape fragment code, proba mirrors prove it.

### GLQ-02 — glyph conversion, train.fab

- **outcome**: Convert the 48 train.fab sites (multiply `:68,69,90-93,116-127,
  156-161`; subtract `:70,71,94-97,128-139,162-167`) to `⊙`/`-` glyphs.
- **write_scope**: `src/train.fab` (+ `src/train.proba` only if it mirrors
  these sites).
- **done_when**: zero receiver `.multiply(`/`.subtract(` sites in train.fab;
  fill-tensor scaffolding (`:64-66` and parallels) unchanged.
- **depends_on**: GLQ-05 (train.fab guard wave settles first; avoids churn).
- **sanity**: converted-site count = 48; one update block read end-to-end;
  `"$FABER_BIN" check "$PWD/src/train.fab"` (absolute path) green.
- **non_goals**: removing `seed.create(lr, shape)` fill scaffolding (needs
  grammar gap 5); any numerics change.
- **risk**: low-medium — training-loop numerics path; behavior-preserving
  operator swap only.

### GLQ-03 — requirit wave 1

- **outcome**: Convert single-throw guards to `requirit <cond> iace finge …` in
  `src/cache.fab` (83), `src/model/gguf_manifest.fab` (80),
  `src/model/safetensors.fab` (78) — 241 sites.
- **write_scope**: `src/cache.fab` + `.proba`, `src/model/gguf_manifest.fab` +
  `.proba`, `src/model/safetensors.fab` + `.proba`.
- **done_when**: zero pure single-throw guard blocks in the three files
  (residuals only with a logged skip reason); `requirit … iace` present;
  `⇥` declarations unchanged; double-not sites (none expected here) removed.
- **depends_on**: none.
- **sanity**: `requirit` count per file ≈ audit count (83/80/78 minus logged
  skips); one converted guard read against EBNF:612 desugar;
  `"$FABER_BIN" check "$PWD/src/cache.fab"` (absolute path) green on a
  converted file.
- **non_goals**: error-message remap wall (gap 3); variant-identity changes;
  `adfirma` (no panic-semantics site exists).
- **risk**: medium — broad but mechanical; every site audited as
  `⇥`-declaring.

### GLQ-04 — requirit wave 2

- **outcome**: Same conversion in `src/attention.fab` (76), `src/model/gguf.fab`
  (52), `src/serialize.fab` (49), `src/tokenizer.fab` (46), `src/nn.fab` (40) —
  263 sites.
- **write_scope**: those five files + co-located `.proba`.
- **done_when**: as GLQ-03 for the five files.
- **depends_on**: GLQ-01 (attention.fab glyph pass lands first).
- **sanity**: per-file `requirit` counts ≈ audit; one guard per file sampled;
  `"$FABER_BIN" check "$PWD/src/nn.fab"` (absolute path) green on a converted
  file.
- **non_goals**: prefix-slice remap hacks at `tokenizer.fab:856,1976` (gap 3 —
  leave the remap logic itself untouched); loop conversions (GLQ-07/08).
- **risk**: medium.

### GLQ-05 — requirit wave 3 + double-not removal

- **outcome**: Same conversion for the remaining guard-site files, 14 files /
  334 sites actual (audit B5 list is authority; this is GLQ-05's honest
  enumeration — the prior ~383 over-count is dropped): `model/dense`,
  `decode`, `model/qwen35moe`, `generation`, `train`, `optimize`,
  `model/capsule`, `math`, `calibration`, `loss`, `shape`, `parameter`,
  `metrics`, `sampling`; in the same pass remove the 28 double-not guards
  (`if not (not X) { throw }` → `requirit X iace …`, math.fab family
  `:478-487,521-530,571-577,…`). Additionally, this amendment extends
  coverage to the 9 guard-site files the audit showed sitting outside any
  requirit wave — `tensor_view` (11), `gradient` (9), `dtype` (8), `tensor`
  (6), `dense_qwen2` (6), `dequant` (4), `artifact` (3), `transformer` (1),
  `dense_llama` (1) — so every guard-site file in the audit's list sits in
  some unit (23 files / 383 sites total).
- **write_scope**: the 14 files + co-located `.proba`, plus the 9 extended
  files above + co-located `.proba`.
- **done_when**: zero pure single-throw guards and zero `if not (not` in the
  full wave-3 file set; `requirit` counts ≈ the audit per-file table
  (334 + 49 extended).
- **depends_on**: GLQ-01 (loss.fab glyph pass lands first; also sequences
  `gradient`/`transformer`, which GLQ-01 owns for glyphs, ahead of this
  guard pass).
- **sanity**: `grep -n 'if not (not' src/math.fab` → zero; sampled guards
  across ≥3 files; `"$FABER_BIN" check "$PWD/src/dtype.fab"` (absolute path)
  green on a converted file.
- **non_goals**: `train.fab` glyph sites (GLQ-02 owns them); structural dedup
  (GLQ-09); §-template sites in `dense_qwen2`/`dense_llama` (GLQ-07 owns them).
- **risk**: medium.

### GLQ-06 — binding holes (externally sequenced)

- **outcome**: Convert ~110 hole-eligible `const tensor<…> x ← <typed expr>`
  bindings to `fixum _`/inferred-binding form across tensor-static files
  (train 53, transformer 23, gradus 7, loss 6, attention 5, + generic-shape
  sites; 25 proba mirrors). Keep the 5 `← vacua` annotations (`train.fab:65,
  85,113,154`; `nn.fab:457`).
- **write_scope**: `src/**/*.fab`, `src/**/*.proba` (binding lines only).
- **done_when**: hole-eligible census zero (per-file const-binding grep);
  `← vacua` sites unchanged; one hole use precedent remains canonical.
- **depends_on**: GLQ-09 **and** the external gate — radix size-param type-args
  repair + parser fix settled on radix main. Do not dispatch before Mind
  confirms the settle.
- **sanity**: converted count ≈ 110; one converted file read in full;
  `"$FABER_BIN" check "$PWD/src/train.fab"` (absolute path) green on a
  converted file.
- **non_goals**: applied call-site holes (no explicit call-site type args exist
  in gradus — feature has no remediation site); union holes.
- **risk**: medium — touches type-inference surface against a freshly settled
  parser; sequencing constraint is the mitigation.

### GLQ-07 — § string templates

- **outcome**: Convert string concatenation to `§` template call form
  (`"missing key: §"(key)`) — 140 src sites: tokenizer (33), qwen35moe (19),
  safetensors (18), dense_qwen2 (14), dense_llama (14), gguf_manifest (8),
  capsule (7), rest per audit; tokenizer first. Proba mirrors (112) where they
  assert on message text.
- **write_scope**: `src/**/*.fab`, `src/**/*.proba` (message-string sites).
- **done_when**: zero concat-built diagnostic/message strings in converted
  files (non-message concatenations may remain if any); rendered outputs
  byte-identical (proba assertions unchanged in expectation).
- **depends_on**: GLQ-03, GLQ-04, GLQ-05 (guard waves settle the same files).
- **sanity**: one template call compiled-shape read against EBNF:795-801;
  message-equivalence spot diff on tokenizer;
  `"$FABER_BIN" check "$PWD/src/tokenizer.fab"` (absolute path) green on a
  converted file.
- **non_goals**: changing message text; i18n; error remap wall structure.
- **risk**: low-medium — mechanical; output equivalence is the watch item.

### GLQ-08 — for-range conversion

- **outcome**: Convert the ~75 `while i ≺ …` + `i ← i + 1` loops to
  `itera ab`/for-range where the index is loop-only (audit first-set: cache,
  tokenizer, gguf_manifest). Loops that mutate the index mid-body stay `dum`
  with a logged skip (audit blind-spot flag).
- **write_scope**: `src/**/*.fab` (+ `.proba` mirrors where loops are mirrored).
- **done_when**: for-range count rises by ≈75 minus logged skips; every skip
  has a one-line reason in the receipt.
- **depends_on**: GLQ-03, GLQ-04, GLQ-07 (same-file churn settles first).
- **sanity**: two converted loops read for off-by-one boundaries
  (`‥` inclusive semantics); `"$FABER_BIN" check "$PWD/src/cache.fab"`
  (absolute path) green on a converted file.
- **non_goals**: `↑`/`↓` inc/dec introduction (zero usage today; not required);
  algorithm changes.
- **risk**: low-medium — boundary semantics are the defect class; proba
  coverage guards it.

### GLQ-09 — train.fab structural dedup

- **outcome**: Rewrite the copy-paste 12-parameter update-block families
  (`src/train.fab:116-139`, `:156-167`) list-driven, shrinking beyond idiom.
- **write_scope**: `src/train.fab`, `src/train.proba`.
- **done_when**: the update-block families are data-driven with one loop body;
  proba expectations unchanged; parameter-update numerics identical.
- **depends_on**: GLQ-02, GLQ-05 (glyph + guard passes land first so dedup
  rewrites final idiom, not transitional forms).
- **sanity**: before/after proba run on the touched expectations; block count
  diff; `"$FABER_BIN" check "$PWD/src/train.fab"` (absolute path) green.
- **non_goals**: public API change to train surfaces; optimizer semantics.
- **risk**: medium — numeric-path restructure; proba is the proof.

### GLQ-10 — Latin residue + U8 guard hold

- **outcome**: Rename `scaled_dot_product_staticum` → English (default
  `scaled_dot_product_static`) with consumers chased (proba, api-reference
  regen, compatibility-policy break record); rewrite `addita_bias` /
  `conversio` Latin in live header comments; add `staticum`, `addita`,
  `conversio` to the U8 lexicon in `scripta/check-source`. The guard's
  ledger-path comment is already correct — it resolves to the re-opened
  `docs/factory/no-latin/rename-ledger.md` — so no path fix is needed
  (the earlier factory→archived fix is inverted; no-latin re-opened).
- **write_scope**: `src/attention.fab` (+`.proba`), header comments in
  `src/train.fab`, `src/transformer.fab`, `src/gradus.fab`, `src/shape.fab`,
  `scripta/check-source`, `docs/api-reference.md` (regen), 
  `docs/compatibility-policy.md` (break record).
- **done_when**: `grep -rn 'staticum' src/ docs/api-reference.md` → zero (or
  ledgered retained-exception if the operator rules otherwise — see GOAL OQ4);
  lexicon entries present; guard comment path resolves to the re-opened
  ledger; api-reference republishes the English name.
- **depends_on**: no-latin re-close — GLQ-10's `scripta/check-source` lexicon
  additions (`staticum`/`addita`/`conversio`) are sequenced **after** no-latin
  re-closes (reopened scope closes; its R2 guard-root restoration edits the
  same file), so the two never edit `check-source` concurrently.
- **sanity**: guard still green on the converted tree (lexicon addition is
  additive); one consumer chase verified; `"$FABER_BIN" check
  "$PWD/src/attention.fab"` (absolute path) green.
- **non_goals**: renaming retained technical terms; rewriting archived
  campaign docs that legitimately cite history.
- **risk**: low — one symbol + comments + additive guard rows.

### GLQ-11 — README public rewrite

- **outcome**: Audit Batch A on `README.md`: fix the five stale symbols
  (`Tabula`→Checkpoint, `accuratezza`/`Metricum`→accuracy/Metric,
  `vincula`→links, `praevideo`→forward); replace `:195-199` import block with
  live `import from` syntax; remove/repair dead paths (`:185` examples/,
  `:226` corpus/); add user install section (cista install, cf.
  `../norma/README.md`) and a minimal runnable example; compress Status/Seam
  tables to honest short status with campaign codes moved to a pointer.
- **write_scope**: `README.md`.
- **done_when**: audit grep zero; a cold reader can install + run the snippet
  from the README alone.
- **depends_on**: none.
- **sanity**: snippet paths/import lines checked against live exempla main.fab
  forms.
- **non_goals**: quickstart tour (GLQ-14); rewriting docs/*.md (GLQ-15).
- **risk**: low — single file, truth-aligning.

### GLQ-12 — exempla stale-symbol sweep (README prose only)

- **outcome**: Audit Batch B: sweep Latin from 12 exempla READMEs
  (token-generation, dense-model, gguf-materialize, gguf-inspect,
  dense-prefill-qwen2, dense-prefill-smollm2, training-loop-mlp,
  qwen36-35b-inference, gguf-admit-qwen35moe, dense-swiglu, dense-qwen2-adapter,
  dense-block), mapping via `docs/factory/no-latin/rename-ledger.md`.
- **write_scope**: `exempla/*/README.md` **only** — no `.fab` write paths.
  Exempla `main.fab` identifier renames (e.g. gguf-manifest `_numerum_observa`;
  gguf-materialize `_vinculum`/`VinculumMala`/`SlicemMala`; training-loop-mlp
  `metrica_p`/`damnum`/`accuratezza`; dense-model `praevideo`) are owned by
  no-latin R1, not by this goal.
- **done_when**: README Latin grep zero under `exempla/` outside `target/`
  and retained exceptions (README prose only; mains excluded).
- **depends_on**: no-latin R1 re-close (so R1's exempla renames land before
  this README sweep reads final names).
- **sanity**: two swept READMEs' cited symbols checked live in src.
- **non_goals**: exempla `main.fab` identifier renames and edits (no-latin R1,
  not GLQ-12); writing the missing nn-bridge README (GLQ-15); exempla
  behavioral changes.
- **risk**: low — prose + local identifiers.

### GLQ-13 — LICENSE + root-file disposition (decision-pending; content NOT lowered)

- **outcome**: After the operator rules: add the chosen LICENSE file, a README
  badge line, a `docs/release-checklist.md` license row; record disposition
  for `AGENTS.md` and `.polish-inspected.json` in a public checkout.
- **write_scope**: `LICENSE*`, `README.md` (one badge line),
  `docs/release-checklist.md`.
- **done_when**: LICENSE file present; checklist row present; dispositions
  recorded. **Not dispatchable until Mind records the operator ruling** (GOAL
  OQ1). No license content is pre-lowered here.
- **depends_on**: operator decision (external gate).
- **sanity**: `ls LICENSE*` non-empty; checklist grep hits.
- **non_goals**: choosing the license; any packaging change beyond the ruling.
- **risk**: low once ruled; blocked until then.
- **integrable**: yes (when unblocked).

### GLQ-14 — quickstart / examples tour / architecture overview

- **outcome**: Audit Batch D: public-audience additions — a "Start here"
  quickstart in triga's shape (`../triga/README.md`), an examples tour (which
  exemplum to open first per capability), and a one-paragraph architecture
  overview.
- **write_scope**: `README.md` (or `docs/quickstart.md` + README pointer, Hand
  picks per length), `docs/module-map.md` (tour cross-links only).
- **done_when**: a first-time reader path exists from README → quickstart →
  runnable exemplum without internal campaign-code fluency.
- **depends_on**: GLQ-11, GLQ-12 (rewritten README and swept exempla first).
- **sanity**: tour entries match live exempla dirs and capabilities.
- **non_goals**: moving factory docs; benchmark regeneration.
- **risk**: low.

### GLQ-15 — residual docs Latin + cosmetics

- **outcome**: Audit Batch E: `docs/regression-corpus.md` (`:69,:138,:142`),
  `docs/diagnostics.md` (`:314,:344`), `docs/numeric-tolerances.md` (`:28`
  heading), api-reference trailing `{` signature cosmetics, and write the
  missing `exempla/nn-bridge/README.md`.
- **write_scope**: `docs/regression-corpus.md`, `docs/diagnostics.md`,
  `docs/numeric-tolerances.md`, `docs/api-reference.md`,
  `exempla/nn-bridge/README.md`.
- **done_when**: audit grep clean across `docs/*.md` outside factory/archived;
  nn-bridge README present with what/why/run.
- **depends_on**: GLQ-10 (api-reference regen lands first).
- **sanity**: replacement names checked live (links/materialize_slice/
  materialize_block).
- **non_goals**: `docs/factory/**`, `docs/archived/**`, `docs/design/**`.
- **risk**: low.

### GLQ-16 — packaging hygiene

- **outcome**: Audit Batch F (non-decision part): mark or annotate tracked dev
  receipts (`exempla/dense-prefill-smollm2/bench/*`, the `gi2-*.txt` golden
  dumps) as non-product; add a one-line internal note to `scripta/` /
  `fixtures/` READMEs (or a `docs/internal-surfaces.md`).
- **write_scope**: `exempla/dense-prefill-smollm2/bench/RECEIPT.md` (or a
  sibling marker), `scripta/README.md` / `fixtures/README.md` (created if
  absent), optionally `docs/internal-surfaces.md`.
- **done_when**: each tracked receipt location carries a visible non-product
  marker; scripta/fixtures state their internal audience.
- **depends_on**: none (the AGENTS.md / `.polish-inspected.json` disposition
  decisions ride GLQ-13, not here).
- **sanity**: marker visible at repo browsing depth (README layout section or
  the marker files themselves).
- **non_goals**: deleting receipts; .gitignore churn beyond the ruling.
- **risk**: low.

### GLQ-17 — EBNF staleness ×3 (faber-side docs unit)

- **outcome**: Correct the three staleness items in `faber/docs/EBNF.md`:
  (a) requirit/adfirma particle "proposed (not shipped)" prose (≈`:610-613`) vs
  the shipped parser (`radix-parser/src/stmt.rs:565-589`, tests
  `radix-parser/src/mod_test.rs:2308-2336`); (b) comparison productions listing
  `<`/`>` while canonical glyphs are `≺`/`≻`
  (`radix-lexer/src/token.rs:304-305`); (c) dead references to
  `docs/design/{textus,numerus,fractus,lista,tabula,copia}-intrinsics.md`
  (`:1087-1095`) — fix to live paths or drop.
- **write_scope**: `/Users/ianzepp/work/faberlang/faber/docs/EBNF.md` **only**
  (different repo than the rest of the goal).
- **read_scope**: unrestricted (radix sources cited above for verification).
- **done_when**: no "proposed (not shipped)" claim on the shipped particles;
  comparison productions match canonical glyphs; zero dead design-doc
  references.
- **depends_on**: none.
- **sanity**: each correction cross-checked against the cited radix source
  line before writing.
- **non_goals**: any radix code change; EBNF grammar redesign; documenting
  gaps 1-7 as shipped.
- **risk**: low — docs-only, but in the faber repo (Mind routes the Hand with
  the right repo root).

## 5. Integration / merge gate

All 17 units are individually integrable; no transitional non-integrable
packets are needed. Merge lane lands each unit's path-limited commit on main
in dependency order and owns build stability. The only hard external gates are
GLQ-13 (operator decision) and GLQ-06 (radix type-args repair + parser fix
settled) — Mind dispatch gates, not merge gates.

## 6. Lane-owned validation (named once — not on child Hands)

- **lint**: `./scripta/check-source` (incl. U8 no-Latin guard; must stay green
  after GLQ-10's lexicon additions).
- **test**: `./scripta/check-compile` (full library + exempla set);
  `./scripta/inventory-public-symbols` (api-reference coverage; re-baseline
  after GLQ-10's rename).
- **merge**: integration on main + build stability; compatibility-policy break
  record present for the GLQ-10 rename.
- Child Hands carry only the per-unit `sanity` above: targeted greps + reads,
  plus the unit-scoped `faber check` absolute-path sanity declared on each
  `.fab`-converting unit in §4 (not a §6-only lane gate). The full-tree gates
  (`check-source`, `check-compile`, `inventory-public-symbols`) stay lane-owned.

## 7. Dispatch waves (max safe parallelism)

| Wave | Units | Gate to enter |
| --- | --- | --- |
| 1 | GLQ-03, GLQ-11, GLQ-16, GLQ-17 | none (disjoint surfaces) |
| 1a | GLQ-10, GLQ-12 | no-latin re-close: GLQ-10 after no-latin R2 (both edit `scripta/check-source`); GLQ-12 after no-latin R1 (exempla renames land first) |
| 2 | GLQ-01, GLQ-14, GLQ-15 | GLQ-10 done (GLQ-01 glyph, GLQ-15 api-reference); GLQ-11+12 done (GLQ-14) |
| 3 | GLQ-04, GLQ-05 | GLQ-01 done (disjoint file sets between them) |
| 4 | GLQ-02, GLQ-07 | GLQ-05 / waves 1-3 done |
| 5 | GLQ-08, GLQ-09 | GLQ-07 / GLQ-02+05 done |
| 6 | GLQ-06 | GLQ-09 done **and** radix size-param type-args repair + parser fix settled |
| any | GLQ-13 | operator ruling recorded |

## 8. Open questions for Mind

1. GLQ-13 ruling (license + `AGENTS.md` / `.polish-inspected.json`
   disposition) — only operator-gated unit; goal may close with it parked.
2. GLQ-06 external gate confirmation signal — which radix commit/merge closes
   the type-args repair, so dispatch can key on it.
3. Sentinel `-1`: audit enumerates 2 fns, task digest said 3 — default retain
   both; name the third if it exists and Mind wants it converted.
4. `staticum` disposition: default rename (GLQ-10); operator may prefer a
   ledgered retained exception — say so before wave 1 dispatch to avoid a
   rename-then-revert.
5. `worktrees/hand-13` is idle on main — retire or reuse before spawning new
   lanes.
6. Goal file naming: task asked for `goal.md`; repo convention is `GOAL.md`
   (every existing goal). Written as `GOAL.md`; rename if the task's literal
   name is load-bearing somewhere.
