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
| `done_when` | Zero live calls to the three names in those files (grep); `faber check` green on `linear-regression`, `mlp` (Latin surface preserved — no keyword conversions); `faber check exempla/nn-bridge` green; bridge printed pins unchanged in value (pin labels may keep the historical row names as provenance or rename — Hand's choice, README row list must match reality); the bridge's known `linear_2x2` matmul red stays recorded as baseline in the README, not claimed green |
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
| `outcome` | One repo, one family, atomic: (a) `src/train.fab` — `train_step_2x2` and `train_step_4x4` delegate through `optimize._sgd_family` list form (the proven `train_step_bert_linear` pattern at train.fab:98-99): one `_sgd_family([weight, bias], [grad_weight, grad_bias], lr)` call for 2x2, one 4-element list call for 4x4, tuple re-packed as today; (b) `src/optimize.fab` — delete `sgd_step_2x2` (:130-140) and `sgd_step_4x4` (:142-152) with their section comments, and update the header ledger note (:17-19) append-only; (c) `src/optimize.proba` — replace the two direct `sgd_step_2x2`/`sgd_step_4x4` tests (:527-543) with `_sgd_family` single-element-list pins of the same `param − lr·grad` oracle values; (d) `src/train.proba` — test names/comments at :768-769, :875, :891 say "through optimize.sgd_step_2x2/4x4"; reword to the `_sgd_family` delegation (values/pins unchanged); (e) `exempla/training-loop-mlp/src/main.fab` comment-only touches (:22, :39, :321) — same rewording, no code change |
| `write_scope` | `gradus` repo only: `src/train.fab`, `src/optimize.fab`, `src/optimize.proba`, `src/train.proba`, `exempla/training-loop-mlp/src/main.fab` |
| `done_when` | Zero live calls or true claims naming `sgd_step_2x2`/`sgd_step_4x4` in gradus src/proba/exempla (grep; historical ledger text that explicitly records the retirement is fine); `train_step_2x2`/`train_step_4x4` signatures and tuple contracts unchanged; `faber check` green on gradus and `exempla/training-loop-mlp`; rewritten optimize.proba rows pass on the stepper |
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
| `outcome` | Delete from `src/nn.fab`: `linear_2x2` (:98-116), `linear_4x4` (:119-125), `gelu_4x4` (:128-139), `gelu_2x8` (:178-189), and `linear_from_raw` (:366-381 — orphaned with `linear_2x2`, its only caller). Update the file header ledger (PML0-U3 admission note :23-33) append-only: rows 1-3 and 6 retired by this wave; `_staged` **stays** (live callers `linear_2x8`/`layernorm_2x8`, wave 2) |
| `write_scope` | `gradus` repo only: `src/nn.fab` |
| `done_when` | `grep -n "linear_2x2\|linear_4x4\|gelu_4x4\|gelu_2x8\|linear_from_raw" src/nn.fab` returns only the retirement ledger note; no alias or same-contract wrapper remains; `_staged`, `linear_carrier`, `gelu_carrier`, `linear_2x8`, `layernorm_2x8` untouched; `faber check` green on gradus package and `exempla/nn-bridge` |
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
| `outcome` | Delete `scaled_dot_product_2x8` from `src/attention.fab` (:50-64) with its section comment; update the header ledger (PML0-U3 row-12 admission note :36-40) and the compiler-boundary note (:134-135 "legacy scaled_dot_product_2x8 stays caller-backed") append-only: retired by this wave, `scaled_dot_product_static<B,D>` is the surface |
| `write_scope` | `gradus` repo only: `src/attention.fab` |
| `done_when` | `grep -n "scaled_dot_product_2x8" src/attention.fab` returns only the retirement ledger note; `scaled_dot_product_static` untouched; `faber check` green on gradus package and both bert example packages |
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
| `outcome` | Public-surface docs stop advertising the zoo: `README.md` (:130 prose `train_step_4x4 → optimize.sgd_step_4x4` → new delegation wording; :245 `linear_2x2, linear_4x4, gelu_4x4` → the generic leaves; :251-254 `sgd_step_2x2`/`sgd_step_4x4` paragraph → `_sgd_family` wording), `docs/api-reference.md` (:35 delete the `scaled_dot_product_2x8` entry — the `_static` entry at :36 stays; :990-995 delete the four nn entries), `docs/api-shape-policy.md` (:40 fixed-shape admitted-rows example — replace the retired names with surviving examples or the retirement note), `src/gradus.fab` facade comment (:51-52 lists `scaled_dot_product_2x8`/`gelu_2x8` as shipped — reword to the generic surface, append-only note), `src/tensor.fab` census comment (:90-95 admit-row ledger — append the retirement) |
| `write_scope` | `gradus` repo only: `README.md`, `docs/api-reference.md`, `docs/api-shape-policy.md`, `src/gradus.fab`, `src/tensor.fab` (comment-only in the two src files) |
| `done_when` | Cross-repo census grep returns zero live-API claims for the seven names outside frozen evidence (receipts, `docs/factory/*` historical campaign paper, archived docs, oracle `reference.json`); every touched doc names the generic leaf where it named a wrapper |
| `depends_on` | GCB-W1-U3, GCB-W1-U4, GCB-W1-U5 (describes their end state) |
| `sanity` | none beyond the census grep (docs + two comment-only files) |
| `non_goals` | standing set + no edits to `docs/factory/**` (historical campaign paper stays as landed record), `docs/deep-code-review-*`, archived docs, benchmark baselines/receipts, or `faberlang/examples` oracle `reference.json` files (frozen evidence per amendment `59b4074a`) |
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
