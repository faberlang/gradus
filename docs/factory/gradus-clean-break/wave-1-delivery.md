# gradus-clean-break wave 1 — delivery spec and unit graph

Delivery lowering for operator need `127f9fd6` (+ amendment `59b4074a`),
task `4aa2f634`. Goal: [`GOAL.md`](GOAL.md) (verdict **READY** — operator
rulings settled, baseline verified against live source 2026-08-28; every
twin/wrapper/caller claim in the goal's ground-truth section was re-checked
against `gradus` main and the `faberlang/examples` repo before carding).

Standing `non_goals` on every card: no `matmul<M,K,N>` / `transpose<M,N>`
inventions (`·` and `ᵀ` exist); no edit to `linear_2x8` / `layernorm_2x8` /
`mse_*` / `train_step_*` names / `bert_tiny_block_2x8` / `kernel.fab` /
`*_carrier` residuals; no new `*_carrier`-to-generic rewrite; no device
manifest input-buffer or step-count edits; no radix/faber source changes.

## Interpreted theme

Collapse the seven named `_NxM` wrappers that already have shape-generic
typed twins, moving every caller (two repos: `gradus` and
`faberlang/examples`) onto the generic at the call site, then delete the
names and the docs that advertise them.

## Normalized spec (delivery-sized outcome)

After this wave: `nn.linear_2x2`, `nn.linear_4x4`, `nn.gelu_4x4`,
`nn.gelu_2x8`, `attention.scaled_dot_product_2x8`, `optimize.sgd_step_2x2`,
`optimize.sgd_step_4x4` do not exist; every live caller names the generic
leaf instead; README/api-reference/api-shape-policy describe the generic
surface. Thin transitional wrappers may exist only inside a single unit's
landing commit sequence and are gone before the wave closes.

## Repo-aware baseline

See [`GOAL.md`](GOAL.md) §Ground truth (twins, wrapper bodies, complete
caller census with file:line, docs surfaces, environment truth, KRS-2
interplay). Two git repos are in play: `faberlang/gradus` (library,
probas, nn-bridge exemplum) and `faberlang/examples` (four training
packages; own root at `faberlang/examples`). Example sources use the Latin
keyword surface (`[reader] locale = "la"`); `mlp` and `bert-tiny-fragment`
are device programs with frozen `[device]` fixtures.

## Units

One function-family (or one shared caller surface) per unit. Commit
ordering inside a family: callers-moved commit lands before the
deletion commit, so no consumer is ever stranded. All commits
path-limited per repo.

---

### GCB-W1-U1 — nn-family callers move (linear_2x2 / linear_4x4 / gelu_4x4; nn-bridge gelu_2x8 row)

| field | value |
| --- | --- |
| `id` | GCB-W1-U1 |
| `outcome` | Every non-bert caller of the dying nn wrappers names the generic leaf: `nn.linear_2x2`→`nn.linear` (shape params unify from `[2,2]` argument types), `nn.linear_4x4`→`nn.linear`, `nn.gelu_4x4`→`nn.gelu`; nn-bridge's `gelu_2x8` row → `nn.gelu`. The twins are infallible — delete the `fac {} cape {}` error arms around former `⇥` calls (`linear-regression/src/train.fab:93-97`; `nn-bridge` bridge wrappers), do not preserve them. nn-bridge keeps its `linear_2x8` / `layernorm_2x8` rows untouched (wave 2) |
| `write_scope` | `faberlang/examples` repo: `examples/training/linear-regression/src/train.fab`, `examples/training/linear-regression/oracle/capture.fab`, `examples/training/mlp/src/train.fab`, `examples/training/mlp/oracle/capture.fab`. `gradus` repo: `exempla/nn-bridge/src/main.fab`, `exempla/nn-bridge/README.md` (row list + run-command status wording) |
| `done_when` | Zero live calls to **all four** retiring names this card moves — `nn.linear_2x2`, `nn.linear_4x4`, `nn.gelu_4x4`, and the nn-bridge `nn.gelu_2x8` row (bridge wrapper `main.fab:133-140` + pin row `:231-245`) — across the named caller surfaces: the two `linear-regression` files, the two `mlp` files, and `exempla/nn-bridge/src/main.fab` (grep; pin labels may keep the historical row names as provenance — labels are not calls). `faber check` green on `linear-regression`, `mlp` (Latin surface preserved — no keyword conversions); `faber check exempla/nn-bridge` green; bridge printed pins unchanged in value (README row list must match reality); the bridge's known `linear_2x2` matmul red stays recorded as baseline in the README, not claimed green. Deletion dependency stays explicit: U4 deletes exactly these four nn names and only after this unit (plus U2) lands — no consumer may keep a live call to any of them |
| `depends_on` | none |
| `sanity` | `faber check` on the three touched packages (requires a built radix `faber`; if the workspace binary is absent, build radix first — environment precondition, report if blocked) |
| `non_goals` | standing set + no library edits (nn.fab untouched here — wrappers still exist and still work; that is the point of callers-first), no bert exempla edits (U2), no oracle `reference.json`/receipt edits |
| `risk` | medium — device-program route: `mlp` is a `[device] backend="auto"` program whose first generic-leaf (`@ kernel`) call sites these become; KRS-2 lane paper records a specialization failure for a fixed-shape `@ kernel` wrapper calling a generic leaf, not for a package call site, but if `faber check`/device specialization rejects the call, record the exact error and stop per the stop condition (callers-moved state is reportable; do not re-add a name) |
| `integrable` | yes |

---

### GCB-W1-U2 — attention-family callers move (scaled_dot_product_2x8; bert gelu_2x8 rows)

| field | value |
| --- | --- |
| `id` | GCB-W1-U2 |
| `outcome` | `attention.scaled_dot_product_2x8` → `attention.scaled_dot_product_static` (B=2, D=8 unify from the `[2,8]` argument types; the callers' `[2,2]` `dk_scale` matches the twin's `[B,B]`); `nn.gelu_2x8` → `nn.gelu` in the two bert exempla (unwrapping the `fac/cape` arm at `bert-gradus-probe/src/train.fab:411-418`). Twin body is identical statement-for-statement to the wrapper (attention.fab:57-64 vs :77-85), so pinned numeric outputs are unchanged by construction |
| `write_scope` | `faberlang/examples` repo only: `examples/training/bert-tiny-fragment/src/train.fab`, `examples/training/bert-tiny-fragment/oracle/capture.fab`, `examples/training/bert-tiny-fragment/oracle/README.md` (surface listing), `examples/training/bert-gradus-probe/src/train.fab` |
| `done_when` | Zero live calls to `scaled_dot_product_2x8` and `nn.gelu_2x8` in those files (grep); `faber check` green on both bert packages; `[device]` manifest section and `oracle/capture.txt`-style frozen fixtures untouched; Latin keyword surface preserved |
| `depends_on` | GCB-W1-U1 (shared bert files are not touched by U1, but the bert exempla also sit behind U1's device-route proof on `mlp`; serialize to keep one probe of the device/fmir routes in flight at a time — may be relaxed by Mind if U1 lands clean) |
| `sanity` | `faber check` on both bert packages |
| `non_goals` | standing set + no `linear_2x8` / `layernorm_2x8` call-site moves (wave 2 owns them; they stay named here), no attention.fab edit (U5), no new caller for `scaled_dot_product_static` beyond these move sites |
| `risk` | medium — `scaled_dot_product_static` has **no live call site today** (KRS-6 census); this unit is its first package consumer. `@ kernel` without `@ public` matches the import posture of the wrapper it replaces (packages import `scaled_dot_product_2x8` today with the same annotation set), but if the import fails to resolve, record the error and stop per the stop condition |
| `integrable` | yes |

---

### GCB-W1-U3 — optimize family collapse (sgd_step_2x2 / sgd_step_4x4 → _sgd_family)

| field | value |
| --- | --- |
| `id` | GCB-W1-U3 |
| `outcome` | One repo, one family, atomic: (a) `src/train.fab` — `train_step_2x2` and `train_step_4x4` delegate through `optimize._sgd_family` list form (the proven `train_step_bert_linear` pattern at train.fab:98-99): one `_sgd_family([weight, bias], [grad_weight, grad_bias], lr)` call for 2x2, one 4-element list call for 4x4, tuple re-packed as today; (b) `src/optimize.fab` — delete `sgd_step_2x2` (:130-140) and `sgd_step_4x4` (:142-152) with their section comments, and update the header ledger note (:17-19) append-only; (c) `src/optimize.proba` — replace the two direct `sgd_step_2x2`/`sgd_step_4x4` tests with their section comment (:523-543) by `_sgd_family` single-element-list pins of the same `param − lr·grad` oracle values, and reword the evidence-honesty header comment (:40, "(sgd_step_2x2/_4x4 and optimize.step)") to the surviving surfaces; (d) `src/train.proba` — test names/comments at :768-769, :875, :891 say "through optimize.sgd_step_2x2/4x4"; reword to the `_sgd_family` delegation (values/pins unchanged); (e) `exempla/training-loop-mlp/src/main.fab` comment-only touches (:22, :39, :321) — same rewording, no code change; (f) `src/optimize.fab` `_sgd_family` block comment (:113-116) — "Fixed-shape sgd_step_* and train_step_bert_* both delegate through this" is false after (b); reword to the post-deletion delegation truth; (g) `exempla/training-loop-mlp/README.md` — the three `train.train_step_4x4` → `optimize.sgd_step_4x4` route claims (:11, :21, :47) reworded to the `_sgd_family` list-form delegation. (e)-(g) are comment/prose-only: no code change |
| `write_scope` | `gradus` repo only: `src/train.fab`, `src/optimize.fab`, `src/optimize.proba`, `src/train.proba`, `exempla/training-loop-mlp/src/main.fab`, `exempla/training-loop-mlp/README.md` |
| `done_when` | Cross-reference grep over the **six** surfaces — `src/optimize.fab`, `src/optimize.proba`, `src/train.fab`, `src/train.proba`, `exempla/training-loop-mlp/src/main.fab`, `exempla/training-loop-mlp/README.md` — finds no active `sgd_step_2x2`/`sgd_step_4x4` call and no current delegation claim; the only remaining occurrences are explicitly marked retirement provenance (the `optimize.fab` header ledger note, updated append-only); `train_step_2x2`/`train_step_4x4` signatures and tuple contracts unchanged; `faber check` green on gradus and `exempla/training-loop-mlp`; rewritten optimize.proba rows pass on the stepper |
| `depends_on` | none (parallel-safe with U1: disjoint files) |
| `sanity` | `faber check` on gradus package root + `exempla/training-loop-mlp` |
| `non_goals` | standing set + no new public `sgd_step<Figura>` (locked default in GOAL §Architecture direction — the need's alternative is not taken), no `train_step_*` renames or signature changes, no SgdState/step/wire surface changes, no bert train_step changes |
| `risk` | low — the destination list form is already the live delegation pattern for `train_step_bert_*` with existing proba pins; probe-interface viability for `_sgd_family` is proven by train.proba:909/:922 |
| `integrable` | yes |

---

### GCB-W1-U4 — nn library deletion (four wrappers + linear_from_raw)

| field | value |
| --- | --- |
| `id` | GCB-W1-U4 |
| `outcome` | Delete from `src/nn.fab`: `linear_2x2` (:98-116), `linear_4x4` (:119-125), `gelu_4x4` (:128-139), `gelu_2x8` (:178-189), and `linear_from_raw` (:366-381 — orphaned with `linear_2x2`, its only caller). Update the file header ledger (PML0-U3 admission note :23-33) append-only: rows 1-3 and 6 retired by this wave — the historical row text stays but each retired row is explicitly marked retired/historical; `_staged` **stays** (live callers `linear_2x8`/`layernorm_2x8`, wave 2). Also update the two current-prose surfaces that name deleted wrappers as live contracts: the S6-G1 header note (:13-15) drops `gelu_2x8` from the shipped-surface list (the generic `gelu` is the current surface; the S6-G1 row survives only as marked history), and the linear formula comment (:55-57) stops calling the same-shape `[M,N]` bias form "the linear_2x2 / linear_4x4 contract" (name the generic `linear<M,K,N>` same-shape bias form instead) |
| `write_scope` | `gradus` repo only: `src/nn.fab` |
| `done_when` | `grep -n "linear_2x2\|linear_4x4\|gelu_4x4\|gelu_2x8\|linear_from_raw" src/nn.fab` returns exactly the enumerated retirement provenance — the PML0-U3 ledger rows 1-3 and 6, each explicitly marked retired/historical by the append-only ledger update, plus any appended retirement note — and nothing else; no current surface or contract comment names a deleted wrapper (the S6-G1 header note :13-15 and the linear formula comment :55-57 name the generic surface); no alias or same-contract wrapper remains; `_staged`, `linear_carrier`, `gelu_carrier`, `linear_2x8`, `layernorm_2x8` untouched; `faber check` green on gradus package and `exempla/nn-bridge` |
| `depends_on` | GCB-W1-U1 (nn callers moved; nn-bridge no longer names the four), GCB-W1-U2 (bert gelu_2x8 rows moved) |
| `sanity` | `faber check` on gradus package root + `exempla/nn-bridge` |
| `non_goals` | standing set + no `@ kernel` annotation experiments on dying wrappers (KRS-2 blocker #1 is moot once deleted), no carrier deletions, no nn.proba edits (it never calls the fixed-shape rows — SEM006/SEM010; its header/test-name references to "accepted linear_2x2 proof" are oracle provenance and stay) |
| `risk` | low — deletion after callers moved; the library has no internal caller of the four (verified census) |
| `integrable` | yes |

---

### GCB-W1-U5 — attention library deletion

| field | value |
| --- | --- |
| `id` | GCB-W1-U5 |
| `outcome` | Delete `scaled_dot_product_2x8` from `src/attention.fab` (:50-64) with its section comment; update the header ledger (PML0-U3 row-12 admission note :36-40), the compiler-boundary note (:134-136, "legacy scaled_dot_product_2x8 stays caller-backed"), the PML3-U2 formula comment (:100-103, "the accepted scaled_dot_product_2x8 arithmetic"), and the top TOOLCHAIN NOTE (:29-34, "the legacy fixed-shape function below") so every current claim names `scaled_dot_product_static<B,D>` as the sole current typed surface — its body is identical statement-for-statement to the deleted wrapper (:57-64 vs :77-85), so the arithmetic description transfers unchanged; every retained mention of the old name is explicitly marked retirement/history, append-only |
| `write_scope` | `gradus` repo only: `src/attention.fab` |
| `done_when` | No current claim or callable declaration for `scaled_dot_product_2x8` remains in `src/attention.fab`; every occurrence from `grep -n "scaled_dot_product_2x8" src/attention.fab` is explicitly marked retirement/history — the PML0-U3 row-12 ledger note (updated append-only), plus at most the capture-provenance mention in the formula comment if kept explicitly labeled historical — and the formula comment, compiler-boundary note, and TOOLCHAIN NOTE document `scaled_dot_product_static<B,D>` as the sole current typed surface; `scaled_dot_product_static` body untouched; `faber check` green on gradus package and both bert example packages |
| `depends_on` | GCB-W1-U2 |
| `sanity` | `faber check` on gradus package root |
| `non_goals` | standing set + no attention.proba edits (its :20 reference is oracle-provenance comment; it never calls the wrapper — verified), no carrier attention surface changes, no KRS-6 work |
| `risk` | low |
| `integrable` | yes |

---

### GCB-W1-U6 — docs closeout (same closeout as the deletions)

| field | value |
| --- | --- |
| `id` | GCB-W1-U6 |
| `outcome` | Public-surface docs stop advertising the zoo, in both repos. Gradus: `README.md` (:130 prose `train_step_4x4 → optimize.sgd_step_4x4` → new delegation wording; :245 `linear_2x2, linear_4x4, gelu_4x4` → the generic leaves; :251-254 `sgd_step_2x2`/`sgd_step_4x4` paragraph → `_sgd_family` wording); `docs/api-reference.md` — delete :35 `scaled_dot_product_2x8` (the `_static` entry at :36 stays), delete the four dying nn entries (:990 `linear_2x2`, :991 `linear_4x4`, :992 `gelu_4x4`, :995 `gelu_2x8` — :993-994 `linear_2x8`/`layernorm_2x8` stay, wave 2), delete :998 `linear_from_raw` (private helper orphaned with `linear_2x2`, deleted by U4), and **add** the missing typed generic entry `fn gelu<size M, size N>(tensor<f32, [M, N]> x) → tensor<f32, [M, N]>` (`@ kernel @ public`, infallible — `src/nn.fab:434-437`); the :1000 staged-carrier `gelu(NumericBlock)` entry stays (carrier residual, distinct surface). `docs/api-shape-policy.md` — correct the carrier-vs-typed distinction: the "What it means for signatures" table (:40-41) currently types **Production (shape-generic)** as the `tensor.NumericBlock` staged carrier with `nn.linear`/`attention.scaled_dot_product` examples; reclassify so the typed generic leaves (`nn.linear<M,K,N>`, `nn.gelu<M,N>`, `attention.scaled_dot_product_static<B,D>`, `math.add<M,N>`) are the production shape-generic surface and the NumericBlock form is the staged/runtime-shape tier (SEM014/SEM005 load-edge posture, `*_carrier` residuals); the :40 admitted-rows example swaps retired `linear_2x2` for a surviving admitted row (`linear_2x8`, `mse_4x4`, `bert_tiny_block_2x8` all stay); the staged-carrier posture section (:12-28) keeps its PML1 rationale as history but stops presenting the carrier as the production form for families whose typed twin ships. `src/gradus.fab` facade comment (:51-52 lists `scaled_dot_product_2x8`/`gelu_2x8` as shipped — reword to the generic surface, append-only note); `src/tensor.fab` census comment (:90-95 admit-row ledger — append the retirement). Examples repo: `examples/training/linear-regression/oracle/README.md` (:23) and `examples/training/mlp/oracle/README.md` (:26) — reword the dying names to their generic destination (`nn.linear_2x2`/`nn.linear_4x4` → `nn.linear`, `nn.gelu_4x4` → `nn.gelu`); the surviving names in those rows (`train.train_step_2x2`/`_4x4`, `loss.mse_2x2`/`_4x4`) stay (wave-1 non-goals) |
| `write_scope` | Both repos. `gradus`: `README.md`, `docs/api-reference.md`, `docs/api-shape-policy.md`, `src/gradus.fab`, `src/tensor.fab` (comment-only in the two src files). `faberlang/examples`: `examples/training/linear-regression/oracle/README.md`, `examples/training/mlp/oracle/README.md` |
| `done_when` | Cross-repo census grep (reference packet pattern, both repos, `*.fab`/`*.proba`/`*.md`/`*.toml`) returns **zero current public-surface claims** for the seven names outside the enumerated exclusion set: (a) frozen evidence — oracle `reference.json`/receipt files, benchmark baselines/receipts, `docs/factory/**` landed campaign paper, `docs/archived/**`, `docs/deep-code-review-*`, `docs/shape-generic-kernels.md` historical design prose; (b) explicitly-marked retirement provenance in src ledger comments (owned by the U3/U4/U5 done-whens); (c) the nn-bridge baseline-red record (:33, U1 keeps it). Every replacement names the correct destination: nn wrappers → typed `nn.linear<M,K,N>` / `nn.gelu<M,N>`, attention wrapper → `attention.scaled_dot_product_static<B,D>`, sgd wrappers → `optimize._sgd_family` list form. `docs/api-reference.md` has no entry for any deleted symbol — the seven wrappers **plus** `linear_from_raw` — while listing typed `gelu<M,N>` alongside the surviving staged-carrier `gelu(NumericBlock)` entry. `docs/api-shape-policy.md` names the typed generic leaves as the production shape-generic surface with the carrier as the staged tier |
| `depends_on` | GCB-W1-U3, GCB-W1-U4, GCB-W1-U5 (describes their end state; transitively after U1/U2) |
| `sanity` | the cross-repo census grep with current-claim classification (docs + two comment-only files; no product suite) |
| `non_goals` | standing set + no edits to `docs/factory/**` (historical campaign paper stays as landed record), `docs/deep-code-review-*`, archived docs, benchmark baselines/receipts, or `faberlang/examples` oracle `reference.json` files (frozen evidence per amendment `59b4074a`); no bert oracle README edit (U2 owns `bert-tiny-fragment/oracle/README.md`); no surviving-name rewording (`train_step_*`, `mse_*`, `linear_2x8`, `layernorm_2x8`, `bert_tiny_block_2x8` stay advertised); no source-code edits beyond the two comment-only files |
| `risk` | low |
| `integrable` | yes |

---

## Order and parallelism

```
U1 (nn callers) ─────┬──> U4 (nn deletion) ─────┐
U2 (bert callers) ───┴──> U5 (attn deletion) ───┼──> U6 (docs closeout)
U3 (optimize family) ───────────────────────────┘
```

U1 ∥ U3 (disjoint files). U2 after U1 (device/fmir route proof ordering;
Mind may relax). U4 after U1+U2; U5 after U2; U6 last.

## Integration / merge gate

No unit is non-integrable alone: callers-moved units leave the wrappers
alive and everything green; deletion units land only after their callers.
Merge owns the aggregate closeout: cross-repo landing order U1/U2/U3 →
U4/U5 → U6 with `./scripta/check-compile` green on gradus main at each
gradus-repo commit, plus `faber check` on the four `faberlang/examples`
packages at each examples-repo commit. The wave is closed only when the
need's DONE-WHEN greps and run proofs hold (baseline reds recorded per
GOAL §Acceptance criteria).

## Lane-owned validation (named once — not on any card)

- lint: `./scripta/check-source`
- test: `./scripta/check-compile` (package-aware `faber check` over gradus
  + consumer exempla; requires a built radix `faber` — environment
  precondition) and `faber test` on the gradus package
- merge: `faber check` + `faber run` on `exempla/nn-bridge` and
  `examples/training/{linear-regression,mlp}` after the wave closes — run
  results recorded honestly; the known `linear_2x2` matmul bridge red and
  any `@ kernel` run-route refusal are baseline records, not failures of
  this wave and never a reason to keep a name

## Open questions for Mind

1. none blocking. The locked defaults Mind should not reopen: `_sgd_family`
   routing (no new public `sgd_step<Figura>`), callers-before-deletion
   ordering, Latin-surface example edits, KRS-2 lane branch `factory/krs-2`
   stays unmerged (its surviving value is wave-2 paper only).

## Repair record — REVISE 8b86bc40 (task abddbbf0, 2026-08-28)

Auditor report `8b86bc40` (assignment `e404f64f`, frozen head `f454dbb`)
returned `revise` with six P2 findings; Mind task `abddbbf0` binds four
(U1, U3, U4, U5 — the other two route elsewhere). Cards repaired in place
above; every corrected claim was re-verified against live source at
`f454dbb` (clean tree) before this record:

1. **U1 (test-surface)** — done_when now enumerates all four retiring
   symbols (`linear_2x2`, `linear_4x4`, `gelu_4x4`, nn-bridge `gelu_2x8`)
   and requires zero live calls across the three training-file pairs and
   nn-bridge, with the U4 deletion dependency explicit. Live evidence:
   `exempla/nn-bridge/src/main.fab:133-140` (`nn.gelu_2x8` bridge call at
   `:135`) and pin row `:231-245`.
2. **U3 (interfaces)** — write scope adds
   `exempla/training-loop-mlp/README.md`; outcome adds the `optimize.fab`
   `_sgd_family` comment (:113-116), the `optimize.proba` header (:40) and
   section comment (:523), and the README route claims; done_when is the
   six-surface cross-reference grep with only marked retirement provenance.
   Live evidence: `optimize.fab:115` ("Fixed-shape sgd_step_* … delegate
   through this"), `optimize.proba:40`, README `:11`/`:21`/`:47`
   (`train.train_step_4x4 → optimize.sgd_step_4x4`).
3. **U4 (interfaces)** — done_when reconciled with the append-only ledger:
   an enumerated explicitly-historical retirement set (PML0-U3 rows 1-3
   and 6, marked retired) replaces "only the retirement ledger note"; no
   current surface/contract comment may name a deleted wrapper; outcome
   adds the S6-G1 header (:13-15 lists `gelu_2x8`) and the linear formula
   comment (:55-57, "the linear_2x2 / linear_4x4 contract") updates.
   Live evidence: `nn.fab:15`, `:55-57`, ledger `:21-33`, `linear_from_raw`
   `:369-381`.
4. **U5 (interfaces)** — same reconciliation: formula comment (:100-103),
   compiler-boundary note (:134-136), and TOOLCHAIN NOTE (:29-34) must name
   `scaled_dot_product_static<B,D>` as the sole current typed surface;
   retained old-name occurrences are enumerated, explicitly marked
   retirement/history. Live evidence: `attention.fab:29-34`, `:36-40`,
   `:101`, `:134-136`; twin bodies identical `:57-64` vs `:77-85`.

Findings 5 (U6 docs census) and 6 (factory goal status metadata) were not
in round 1's scope; round 2 (below) closes them.

## Repair record — REVISE 8b86bc40 round 2 (task 1e9f9e32, 2026-08-28)

Mind task `1e9f9e32` binds the two remaining findings (5 and 6); findings
1-4 were repaired in round 1 (`0ec9a33`). Every corrected claim below was
re-verified against the live tree (`0ec9a33` — round 1 touched only this
delivery spec) and `faberlang/examples` HEAD `226ab8f3` before this record:

5. **U6 (interfaces)** — write scope expanded to both repos: adds
   `examples/training/linear-regression/oracle/README.md` (:23 advertises
   `nn.linear_2x2`) and `examples/training/mlp/oracle/README.md` (:26
   advertises `nn.linear_4x4`/`nn.gelu_4x4`); the bert oracle README stays
   U2's (its :22 row is in U2's write scope). Outcome adds the
   `linear_from_raw` api-reference deletion (:998 — orphaned helper deleted
   by U4), the missing typed `gelu<M,N>` entry (`fn gelu<size M, size N>`
   infallible, `src/nn.fab:434-437`; the :1000 staged-carrier entry stays),
   and the api-shape-policy carrier-vs-typed correction (:40-41 typed
   leaves are the production shape-generic surface, NumericBlock is the
   staged tier; posture section :12-28 demoted to history where a typed
   twin ships). Done_when census exclusions are now enumerated exactly
   (frozen evidence set, marked retirement provenance, nn-bridge baseline
   record), every replacement names its destination, and the cross-repo
   census is fulfillable from the card's own write scope. Live evidence:
   api-reference :990/:991/:992/:995/:998/:1000, api-shape-policy :40-41,
   the two oracle README rows; full both-repo markdown sweep at repair time
   found no further non-frozen, non-owned claim (`exempla/nn-bridge/README.md`
   is U1's, `exempla/training-loop-mlp/README.md` is U3's from round 1;
   `docs/deep-code-review-*` and `docs/shape-generic-kernels.md` :25 are
   excluded historical paper — the latter cites norma's deletion, not a
   gradus surface claim).
6. **Goal metadata (test-surface)** — `GOAL.md` and `CAMPAIGN.md` now carry
   the template header (`**Status**`/Created/Campaign/Source/Repos/Related
   per `radix/docs/factory/TEMPLATE.md`) with honest status `planned`
   (lowered, not implemented) and a machine-managed Ledger section; the
   GOAL ledger tracks U1-U6 receipts (all `pending` — no unit has landed).
