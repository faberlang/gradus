# Delivery: S1 — Pass A: locale surface

**Goal**: `docs/factory/english-locale/GOAL.md` (Milestone 1 / Pass A)
**Campaign**: `docs/factory/english-locale/CAMPAIGN.md` (stage S1, lines 98–116)
**Status**: planned — lowered for delivery audit
**Repo**: gradus (direct mode, main checkout; container law `../AGENTS.md`)
**Predecessors**: S0 committed `a1f25fb` (goal + campaign + rename seed); goal registered `gol_d6cea6c6e788d18d`
**Posture**: batch-by-default (campaign line 59). Pass A is the mechanical locale flip only — **no identifier rename** (S2). Sibling consumers (`examples/training/*`, Inferentia) are S3. PML work is out.

## Phase Intent

Flip every owned Gradus package from the Latin reader surface to the English
surface: pack vocabulary localizes (`functio`→`fn`, `textus`→`string`,
`sponte`→`optional`, `nihil`→`null`, `@ publica`→`@ public`, lista intrinsics
like `longitudo`/`accipe`), comments/strings/import paths/user identifiers
stay, and every manifest declares the canonical `[locale] locale = "en"`.
User identifiers that look Latin (`typus()`, `valor()`, `gradus()`) survive
Pass A by design — they are renamed in S2.

## Live-grounding corrections to the campaign text (must be read as locked)

These were verified against the live tree + binary on 2026-08-16 (faber
1.7.0, in-tree `radix/target/debug/faber`, gradus main `9434f8c`):

1. **`faber format --locale en` is retired.** The flag is rejected by the
   current binary; the HIR-backed reader-locale conversion now lives in
   **`faber convert --to <LOCALE> <path>`** (radix commit `01a2d3c94`
   "feat(faber): convert command — explicit reader-locale conversion; format
   --locale retired"). This is the same pack-renderer machinery the goal's
   live probe used. **Every unit below uses `faber convert --to en`.** A
   campaign/goal prose pass to retire the `format --locale` spelling is a
   docs amendment for Mind (non-blocking; this spec is the authority for S1).
2. **`faber convert` accepts only `.fab` paths** (`is_fab_file`, format.rs
   `resolve_convert_paths`). So `src/**/*.proba` cannot be converted
   directly. Sanctioned route (still the pack renderer,
   no hand-rolled token script): copy each stamped `.proba` to a
   `<name>.proba.fab` file outside the repo (e.g. `mktemp` dir), run
   `faber convert --to en --stdout` on that copy, and write the converted
   output back to the `.proba` path; then flip the frontmatter. Never leave a
   stray `*.fab` in `src/` during a package check.
3. **Mixed wave states are green (probed).** An `en` package whose co-located
   `.proba` still declares `locale = "la"` frontmatter passes `faber check` —
   because `.proba` are test sources and never enter the `faber check`
   package graph (`analyze_package` hard-codes `include_proba = false`), so
   their frontmatter is irrelevant to the gate. The root `faber.toml` flip
   to `en` may land mid-wave (unit 2) without breaking the gate; each file's
   frontmatter is the input-locale authority for `faber convert`.
4. **Convert preserves the source frontmatter as `la`.** The flip
   `locale = "la"` → `locale = "en"` is a separate mechanical edit in the
   same unit, per the goal ("After a green rewrite, flip frontmatter").
5. **Inventory counts survive conversion.** Probed on `src/dtype.fab`:
   `grep -c 'functio '` (14) == `grep -c 'fn '` (14) after conversion; the
   declaration lines map 1:1 even though total lines grow (336 → 418). The
   749 baseline and per-module counts should hold; unit 2 re-verifies and
   re-baselines **only** if comment/string Latin `functio` interference
   drifts a count (explain the drift in the unit report).
6. **`check-source` pattern updates** (unit 2): pattern 3 (`\bad … {`
   route-call tripwire) becomes `\bcall … {` — `ad` is the la keyword, en
   value is `call`; pattern 4 (`∪ nihil … =` "use sponte") becomes
   `∪ null … =` "use optional". Pattern 2 (`@ externa|@ subsidia`) is
   unchanged — `externa`/`subsidia` are not pack rows and do not localize.
   The `∪ null` pattern is safe: live nullable declarations use `←` (e.g.
   `fixum textus ∪ nihil ignota ← …`), never `=`, so no live line matches.
7. **Stop condition (campaign lines 148–149, goal Stop Conditions):** if
   `faber check`/`convert` fails on a missing en-pack row (unknown keyword,
   type, or intrinsic spelling for a construct Gradus actually uses), STOP
   and file a radix locale need. Do not work around in Gradus source. Do not
   run convert on any file that still lacks `la` frontmatter.
8. Convert emits benign warnings (LOCALE002, WARN003, WARN018) — not
   blockers; do not chase them.
9. **Overlap rule (campaign line 101):** do not edit the same `src/` files as
   an in-flight PML5 Hand. Gradus main is currently clean (verified).

## Repo-Aware Baseline

| Surface | Count | State today | Post-S1 |
| --- | --- | --- | --- |
| `src/**/*.fab` | 33 | no frontmatter; Latin; package `la` | `en` frontmatter; English; `[locale] locale = "en"` |
| `src/**/*.proba` | 32 | no frontmatter; Latin | `en` frontmatter; English |
| `exempla/*/src/main.fab` | 17 | no frontmatter; Latin | `en` frontmatter; English |
| `exempla/*/faber.toml` | 17 | `[reader] locale = "la"` | `[locale] locale = "en"` |
| `tests/admission_conformance.fab` | 1 | no frontmatter; Latin | `en` frontmatter; English |
| `faber.toml` (root) | 1 | `[reader] locale = "la"` | `[locale] locale = "en"` |

- Already-frontmattered files are **out of scope**: `scripta/check-*.fab` and
  `fixtures/*/gen_fixture.fab` carry `locale = "en"` frontmatter with Latin
  bodies (dormant native-Faber migration scripts, not on the compiled
  surface). S1 does not touch them; they are a recorded residual.
- Gates: `scripta/check-source` (src-only grep gate), `scripta/check-compile`
  (faber check on root + the 8 gate exempla: gradient-seam,
  training-loop-mlp, token-generation, gguf-manifest, gguf-inspect,
  gguf-materialize, qwen36-35b-inference, gguf-admit-qwen35moe),
  `scripta/inventory-public-symbols` (grep `functio` baseline 749 +
  doc-coverage gate). `faber check` compiles **only** `src/*.fab` — `.proba`
  are test sources and enter only the `faber test` path (`analyze_package`
  hard-codes `include_proba = false`; only `analyze_package_for_tests` sets
  it true). Check-compile green therefore proves the `.fab` surface only;
  the `.proba` surface is gated by U3's full 32-file grep.
- Manifest locale table: parser accepts canonical `[locale]` and legacy
  `[reader]` alias (radix `parse_reader_locale_from_toml`). Flip writes the
  canonical `[locale]` table.
- Docs: `docs/api-reference.md` is **not touched in S1** — identifiers do not
  change, so the inventory doc-coverage gate (names only) keeps passing.
  The compatibility-policy clean-break record is S2 family 9 per campaign,
  not S1.

## Stage Graph

```text
S1-U1 (stamp la frontmatter, 83 files)
  └─> S1-U2 (src .fab → en + frontmatter flip + root manifest + gate greps)
        └─> S1-U3 (src .proba → en + frontmatter flip)
              └─> S1-U4 (exempla + tests → en + manifest flips)
                    └─> S1-U5 (check-compile + check-source + inventory closeout)
```

Strict chain: each unit's conversion depends on every file it touches already
carrying `la` frontmatter (S1-U1), and later units assume the library surface
already compiles under en. All five units are `integrable: yes` — every
mid-wave state compiles (probed mixed states); no named merge gate required.
Batching is per-family (batch-by-default): prove the rewriter on one file of
the family first (`faber convert --to en --check <file>` dry run + spot-check
stdout), then run the family, per rename-seed's probe discipline.

## Implementation Work

### S1-U1 — Stamp input-locale frontmatter on all owned files

| Field | Value |
| --- | --- |
| **id** | S1-U1 |
| **outcome** | Every owned `.fab`/`.proba` declares its input locale: prepend a `+++ locale = "la" +++` block to the 33 `src/**/*.fab`, 32 `src/**/*.proba`, 17 `exempla/*/src/main.fab`, and `tests/admission_conformance.fab` (83 files; none have frontmatter today). No other content changes. |
| **write_scope** | `gradus/src/**/*.fab`, `gradus/src/**/*.proba`, `gradus/exempla/*/src/main.fab`, `gradus/tests/admission_conformance.fab` (frontmatter block only) |
| **read_scope** | `scripta/check-source` (pattern contract), `scripta/check-compile` (gate set) |
| **done_when** | All 83 files start with the exact block `+++\nlocale = "la"\n+++\n`; `rg -l '^\+?\+' src exempla tests` shows only the stamped files and none of `scripta/`/`fixtures/` was touched; `faber check` on the root package and on a sample of the 8 gate exempla is green — this proves the `.fab` stamp is semantically neutral (la frontmatter == la package default); the `.proba` stamps sit off the check surface (`include_proba = false`, baseline) and are verified by the `rg` content gate here, then exercised by U3's convert + gate. |
| **validation** | `FABER_BIN=… ./scripta/check-compile` (sanity — expected green), `./scripta/check-source` |
| **depends_on** | S0 lock (committed); no in-flight PML5 Hand on the same `src/` files |
| **non_goals** | No conversion, no manifest edit, no `scripta/`/`fixtures/` files, no comment edits |
| **risk** | low — mechanical; the only failure mode is a stamping typo, caught by check-compile. |
| **integrable** | yes |

### S1-U2 — Convert `src/**/*.fab` to English; flip frontmatter + root manifest; update gate greps

| Field | Value |
| --- | --- |
| **id** | S1-U2 |
| **outcome** | All 33 `src/**/*.fab` are re-emitted in the English surface, their frontmatter flips to `locale = "en"`, the root `faber.toml` declares `[locale] locale = "en"` (canonical table, replacing `[reader] locale = "la"`), and the two gates that track the Latin surface are updated to track English — all in the same commit wave. |
| **write_scope** | `gradus/src/**/*.fab` (body via convert + frontmatter flip), `gradus/faber.toml`, `gradus/scripta/check-source`, `gradus/scripta/inventory-public-symbols` |
| **read_scope** | `radix/stdlib/locale/en/pack.toml`, `radix/crates/faber/src/commands/convert.rs` + `format.rs` (`resolve_convert_paths`), the goal's live-probe notes (comments/strings/imports/identifiers preserved) |
| **done_when** | (a) `faber convert --to en` applied to each `src/**/*.fab` (dry-run `--check` first; directory call `faber convert --to en src` acceptable — continues past per-file errors and exits 1, so run per-file fallback on any failure); (b) every converted file's frontmatter is `locale = "en"` and its body type-checks under en — `faber check` on the root package is green (this proves no Latin keyword/type token survives in a code position: under the en pack those spellings are not keywords); (c) root `faber.toml` has `[locale] locale = "en"`; (d) `scripta/check-source` patterns updated: `\bad[[:space:]]+…\{` → `\bcall[[:space:]]+…\{`, `∪[[:space:]]*nihil…=` → `∪[[:space:]]*null…=` with message "use optional", `@ externa|@ subsidia` unchanged, and `./scripta/check-source` is green on the en surface; (e) `scripta/inventory-public-symbols` grep updated (`functio ` → `fn ` in the count loop and coverage gate, header text), and the script reports per-module counts + total identical to the 749 baseline (names unchanged — if a count drifts, it is comment/string Latin interference, not lost declarations; re-baseline only with that explanation). |
| **validation** | `./scripta/check-source` (updated) green; `faber check` root green; `FABER_BIN=… ./scripta/check-compile` sanity (mixed-state expected green per live probe: `.proba` still `la`-frontmatter inside the `en` package is fine); `./scripta/inventory-public-symbols` green at 749 |
| **depends_on** | S1-U1 (every `.fab` stamped `la` before convert) |
| **non_goals** | No `.proba` conversion (U3), no exempla/tests (U4), no identifier rename (S2), no `docs/api-reference.md` changes, no comment-language rewrite |
| **risk** | medium — an en-pack gap (missing keyword/type/intrinsic row) stops the wave: STOP and file a radix locale need; do not alias in Gradus. Convert warnings (LOCALE002/WARN003/WARN018) are benign. |
| **integrable** | yes |

### S1-U3 — Convert `src/**/*.proba` to English; flip frontmatter

| Field | Value |
| --- | --- |
| **id** | S1-U3 |
| **outcome** | All 32 `src/**/*.proba` are re-emitted in the English surface with `locale = "en"` frontmatter. The pack renderer (via `faber convert`) does the keyword/type/intrinsic rewrite — the file routing around its `.fab`-only filter is mechanical. |
| **write_scope** | `gradus/src/**/*.proba` (body via convert output + frontmatter flip) |
| **read_scope** | `radix/crates/faber/src/commands/convert.rs` + `format.rs` (extension filter), S1-U2's converted `src/*.fab` (import targets) |
| **done_when** | Every `.proba`'s body is English and its frontmatter is `locale = "en"`. Route (per file, in a temp dir outside the repo, e.g. `mktemp -d`): copy the stamped `X.proba` to `X.proba.fab`, run `faber convert --to en --stdout` on the copy (with `FABER_LIBRARY_HOME` set so `gradus:*` imports resolve), write the output back to `X.proba`, delete the temp copy, then flip the frontmatter. Never leave a `*.fab` in `src/` while running a package check. **U3 gate** — `.proba` are not on the `faber check` surface (test sources load only under `faber test`; `analyze_package` hard-codes `include_proba = false`), so the acceptance proof is a **full 32-file Latin-token grep** (not a spot-grep): `rg -n '\b(functio|importa|textus|redde|sponte|nihil|adfirma|probandum|proba)\b' src -g '*.proba'` — every hit is a comment line or a user identifier, none a keyword/type token. The test-block vocabulary localizes too (`adfirma`→`assert`, `probandum`→`describe`, `proba`→`test`), so its en spellings in code positions are expected. |
| **validation** | Full 32-file Latin-token grep (done_when) with zero non-comment/non-identifier hits; `faber convert` exit 0 per converted file (route sanity) |
| **depends_on** | S1-U2 (library `.fab` already en; unit order also keeps the wave's grep gates consistent) |
| **non_goals** | No `.fab` edits, no manifest changes, no rename of proba assertion names (identifiers survive Pass A) |
| **risk** | medium — same en-pack gap stop condition as U2; the routing workaround is the one non-`convert` step, kept to file movement only. Per-file `faber check` on a `.proba.fab` temp copy is **not** a viable gate: single-file check rejects proba-shaped content (probed — PARSE001 on the la original, PARSE050/PARSE060 on the converted copy), so the full grep is the acceptance. |
| **integrable** | yes |

### S1-U4 — Convert exempla + tests to English; flip their manifests

| Field | Value |
| --- | --- |
| **id** | S1-U4 |
| **outcome** | All 17 `exempla/*/src/main.fab` and `tests/admission_conformance.fab` are re-emitted in the English surface with `locale = "en"` frontmatter, and all 17 `exempla/*/faber.toml` declare `[locale] locale = "en"` (canonical table, replacing `[reader] locale = "la"`). |
| **write_scope** | `gradus/exempla/*/src/main.fab` (convert + frontmatter flip), `gradus/exempla/*/faber.toml` (locale table only), `gradus/tests/admission_conformance.fab` (convert + frontmatter flip) |
| **read_scope** | S1-U2/U3's converted `src/` (import targets), `scripta/check-compile` (the 8 gate exempla) |
| **done_when** | `faber check` is green on the root package and on all 17 exempla and the tests file (`FABER_LIBRARY_HOME` set; run the 8 gate exempla through `./scripta/check-compile`'s exact set and the remaining 9 directly), with no `--locale` overrides; every exempla manifest + the root manifest use `[locale] locale = "en"`; no Latin keyword/type token remains in a code position in `exempla/` or `tests/`. |
| **validation** | `FABER_BIN=… ./scripta/check-compile` (all 8 gate exempla) green; `faber check` on the 9 non-gate exempla and on `tests/admission_conformance.fab` green; `./scripta/check-source` |
| **depends_on** | S1-U2 (exempla import the converted library; keep conversion order) |
| **non_goals** | No exempla README/doc edits, no `corpus/`, no `fixtures/`, no identifier rename (S2), no sibling-repo consumers (S3) |
| **risk** | medium — same en-pack gap stop condition; an exemplum exercising an un-rowed intrinsic is the most likely gap site. |
| **integrable** | yes |

### S1-U5 — S1 closeout: full gate evidence

| Field | Value |
| --- | --- |
| **id** | S1-U5 |
| **outcome** | The whole S1 surface is proven green as one integrated state: the full `check-compile` set (root + 8 gate exempla), `check-source`, and `inventory-public-symbols` all pass with no `--locale` overrides, and the acceptance grep finds no Latin keyword/type tokens in code positions anywhere in `src/`, `exempla/`, or `tests/`. |
| **write_scope** | `gradus/` — restricted to mechanical leftovers of S1 only (a missed frontmatter flip, a stale grep word, a missed file). Any failure that is not a mechanical S1 leftover — in particular a missing en-pack row — is **not** fixed here: STOP and file a radix locale need. |
| **read_scope** | S1-U1..U4 diffs, `radix/stdlib/locale/en/pack.toml`, `docs/api-reference.md` (read-only; confirms inventory coverage gate still passes) |
| **done_when** | (a) `FABER_BIN=… ./scripta/check-compile` exit 0 (library + gradient-seam, training-loop-mlp, token-generation, gguf-manifest, gguf-inspect, gguf-materialize, qwen36-35b-inference, gguf-admit-qwen35moe); (b) `./scripta/check-source` exit 0; (c) `./scripta/inventory-public-symbols` exit 0 with the 749 baseline and full doc-coverage (names unchanged in Pass A); (d) goal acceptance grep — `rg -n '\b(functio|importa|textus|redde|sponte)\b' src exempla tests` — every hit is a comment line or a user identifier, none a keyword/type token (the en compiler check already guarantees that on the compiled `.fab` surface; the `.proba` test sources are covered by the U3 gate grep; this grep is the review evidence); (e) the clean break is recorded in the landing commit message per goal Release Posture. |
| **validation** | `FABER_BIN=… ./scripta/check-compile`; `./scripta/check-source`; `./scripta/inventory-public-symbols`; the goal's acceptance rg |
| **depends_on** | S1-U1..U4 |
| **non_goals** | No identifier rename (S2), no docs/api-reference rebase (S2 family 9), no compatibility-policy edit (S2 family 9), no `examples/training/*` / Inferentia work (S3) |
| **risk** | medium-high — this is the theme gate folded into the final unit per the campaign's suggested list. The known-risk exit is the en-pack gap (radix locale need), not a Gradus workaround. |
| **integrable** | yes |

## Integration / Merge Gate

None required: every unit is `integrable: yes`, and the mixed mid-wave states
were probed green. Main landing is ordinary direct-mode, path-limited commits
per unit on `gradus` main. Do not start S2 until S1 closeout evidence is
accepted.

## Lane-Owned Validation (named once)

- `FABER_BIN=… ./scripta/check-compile` — full gate at S1-U5; sanity at U1/U2/U4.
- `./scripta/check-source` — green from S1-U2 (updated patterns) onward.
- `./scripta/inventory-public-symbols` — re-verified at 749 from S1-U2 onward.

## Open Questions for Mind

1. Campaign/goal prose names `faber format --locale en`; the live binary
   (faber 1.7.0) has `faber convert --to en`. Recommend amending the
   campaign's S1 tool naming (docs amendment; non-blocking — this spec is
   authoritative for S1).
2. `scripta/check-*.fab` and `fixtures/*/gen_fixture.fab` carry `en`
   frontmatter over Latin bodies (dormant native-Faber migration scripts,
   outside the compiled surface). S1 leaves them; recommend a later cleanup
   unit or recorded residual.
3. `docs/compatibility-policy.md` clean-break record is goal acceptance but
   campaign-assigned to S2 family 9; S1 does not touch it (confirmed).
4. Inventory count stability held on the `dtype.fab` probe (14 == 14); if
   another module drifts after conversion the cause is comment/string Latin
   `functio` and the re-baseline must say so. Audit spot-checks this.

---

# S2 — Pass B: identifier renames (collision-preflight first)

**Status**: READY for delivery audit — S2 is lowered into one mandatory
collision-preflight unit followed by the nine campaign families. This section
is planning authority only; it does not rename source, tests, exempla, packs,
or sibling consumers.

**Goal**: [`GOAL.md`](GOAL.md), S2 identifier surface after S1 commit
`e114ea3`. **Campaign**: [`CAMPAIGN.md`](CAMPAIGN.md), S2 family list.
**Seed**: [`rename-seed.md`](rename-seed.md), used as the base table only.
Live Radix and live Gradus evidence below supersede a seed default whenever
they disagree.

## S2 normalized outcome

The Gradus-owned `src/` member surface, its co-located `.proba` proofs, and
in-repo exempla/tests are migrated to English identifiers as a pre-1.0 clean
break. Import coordinates (`gradus:tensor`, `gradus:model/gguf`, and the rest)
stay unchanged. There are no forwarding aliases, dual-authority names, or
Gradus `[[library_members]]` pack rows. Every family lands with its collision
ledger row and reserved-probe receipt before the next family starts.

The live S1 inventory is **750** `grep -c 'fn '` declarations. The old `749`
wording in earlier S1 prose is stale: the live script explicitly records the
English-locale re-baseline and the intentional `transformer` comment match.
The family declaration counts used here are therefore:

| Family | Live files | Live `fn ` count | Source boundary |
| --- | ---: | ---: | --- |
| L1 dtype/shape/tensor/math | 4 | 57 | `src/dtype*`, `shape*`, `tensor*`, `math*` |
| Shared parameter/serialize/gradient | 3 | 84 | `src/parameter*`, `serialize*`, `gradient*` |
| Train loss/optimize/nn/train/metrics/data | 6 | 108 | the six named top-level modules |
| Arch attention/transformer | 2 | 49 | `src/attention*`, `transformer*` |
| Model artifact/capsule/gguf/safetensors/dequant/tensor_*/dense_* | 12 | 234 | every live `src/model/*.fab` and `.proba` |
| Tokenizer | 1 | 74 | `src/tokenizer*` |
| Inference cache/decode/sampling/generation | 4 | 137 | the four named top-level modules |
| Facade + exempla/tests chase | 1 plus callers | 7 | `src/gradus*`, `exempla/**`, `tests/**`, remaining call sites |
| **Total source inventory** | **33** | **750** | all live modules; no remainder |

The `fn ` count is an inventory baseline, not the number of renamed members:
private `_` helpers, comments containing `fn `, already-English names, fields,
classes, variants, and parameters are handled by the family ledger rules below.

## Mandatory first unit — S2-PREFLIGHT collision ledger

This unit is the hard gate. No family rename may start until the preflight
artifact is committed and every family row is locked.

| Field | S2-PREFLIGHT contract |
| --- | --- |
| **id** | `S2-PREFLIGHT` |
| **outcome** | Create `docs/factory/english-locale/s2-collision-ledger.md` with one post-rename symbol/collision row for each of the nine families, the exact live-source evidence used, the reserved-name decisions, and the nine scratch first-file probe receipts. |
| **write_scope** | `gradus/docs/factory/english-locale/s2-collision-ledger.md` only; temporary probe copies may live under `/tmp/gradus-s2-*`; read-only Radix paths are listed below. No `src/`, `.proba`, `exempla/`, `tests/`, pack, or sibling-repo writes. |
| **done_when** | (1) the 750-symbol live census is recorded; (2) every family row has a complete old→new member ledger, including private helpers and collision-sensitive fields; (3) the reserved lock is checked against live Radix `[keywords]`, `[types]`, `[intrinsics]`, builtin `STATUS_VARIANTS`, scalar-interval rules, tensor-directed rules, and frame-view methods; (4) the Tensor field/method shape probe is recorded; (5) the member-scoped parameter policy is recorded; (6) one scratch convert+rename+`faber check` probe has run for each source family before any batch; (7) the artifact says explicitly that Gradus owns this preflight and that no pack-row mechanism is involved. |
| **depends_on** | S1 closeout `e114ea3`; no PML5 source overlap during the rename wave. |
| **sanity** | `git diff --check`; inspect the nine ledger rows and all probe paths. |
| **non_goals** | No implementation rename; no `[[library_members]]`; no Radix edit; no Norma/Tela/Triga work; no sibling-consumer migration. |
| **risk** | high — a false collision decision can make every later family fail or silently create a compiler-owned name collision. |
| **integrable** | yes — the artifact is the gate and contains no product code. |

### Preflight evidence lock

The preflight must use these live paths, not a copied or historical name list:

| Collision surface | Live evidence | Required S2 decision |
| --- | --- | --- |
| English reserved names | `radix/stdlib/locale/en/pack.toml`, sections `[keywords]`, `[types]`, and `[intrinsics]` | Snapshot the exact rows at probe time. Treat `value` (`valor` type), `string`, `int`, `bool`, `float`, `list`, `map`, `set`, `bytes`, `void`, `unknown`, `null`, `tensor`, `vector`, `matrix`, `fn`, `class`, `union`, `enum`, `type`, `const`, `let`, `var`, `import`, `from`, `as`, `public`, `private`, `optional`, `return`, `if`, `else`, `elif`, `then`, `for`, `while`, `match`, `case`, `throw`, `catch`, `do`, `assert`, `panic`, `true`, `false`, `and`, `or`, `not`, `is`, `self`, `main`, `print`, `test`, `read`, `write`, `warn`, `debug`, `size`, `name`, `step`, `range`, `between`, `within`, `until`, `line`, `args`, `call`, `await`, `async`, `future`, `format`, `require`, and `exit` as reserved until the live first-file probe proves the exact member position. |
| Builtin frame variants | `radix/crates/radix/src/builtins/frame_types.rs`, `STATUS_VARIANTS` | Lock `request`, `item`, `byte`, `bulk`, `done`, `error`, and `cancel` out of every new target. Also read `radix/crates/radix-runtime-contract/src/frame.rs`; its `FrameStatus` order and terminal/content classification are part of the same live contract. A plain declaration probe is not enough if frame registration is active. |
| Scalar intervals | `radix/crates/radix/src/semantic/passes/typecheck/intervallum.rs` and the interval intrinsic dispatch in `.../typecheck/intrinsics.rs` | `longitudo` is currently constrained to a bare `numerus` interval bound. A Gradus user member `longitudo` may target `length`, but the probe must not turn compiler interval semantics into a Gradus alias or suggest `size`. |
| Tensor-directed names | `radix/crates/radix/src/semantic/passes/typecheck/tensor_type_directed.rs`, `radix/crates/radix/src/semantic/tensor_type_directed.rs` | Check `structa`, `creata`, `crea`, and `formata` against every family ledger. `structa` is a Gradus user constructor and targets `construct`; compiler-directed `creata`/`crea`/`formata` are not Gradus members and must not be renamed as if they were. |
| Tensor/scalar intrinsic allowlist | `radix/crates/radix/src/semantic/passes/typecheck/intrinsics.rs` | Check `subtrahe`, `longitudo`, `applica`, and `magnitudines` against every S2 target. The live rows are `subtract`, `length`, `apply`, and `shape`; preserve compiler intrinsic meaning, while renaming a Gradus user member only when its receiver/member ledger says so. |
| Compiler view methods | `radix/crates/radix/src/semantic/passes/typecheck/call.rs` | Census the live `meus.da`, `meus.fini`, `tuus.accipe`, `tuus.cursor`, `tuus.exhauri`, and `tuus.fini` branches. `Tensor.accipe → get` is a Gradus member decision and must be probed against this compiler-owned receiver surface; do not edit the compiler view names. |
| Valor/catch/class typo class | Live Gradus `src/**/*.fab`/`.proba` plus Radix HIR catch/typecheck nodes (`radix/crates/radix-hir/src/nodes.rs`, `radix/crates/radix/src/semantic/passes/typecheck/*.rs`) | Classify every `valor` hit as a member/field, parameter/local, or string/comment. `valor` must never become the en type spelling `value`. `catch err` bindings remain bindings; only a `causa` member accessor becomes `message`. `class` is the en rendering of the Faber `genus` keyword, not a user type target. Record any typo or ambiguous catch/error class before a family is unlocked. |

The live source census is a required cross-check, not a prose exercise. The
preflight receipt must include the commands (run from the repository roots)
that produced it:

```bash
# Gradus inventory and source census
./scripta/inventory-public-symbols
rg -n --glob '*.fab' --glob '*.proba' \\
  '\\b(figura|forma|gradus|typus|typo|valor|causa|accipe|structa|verifica|serializa|deserializa|quantitas|longitudo|nomen)\\b' src

# Radix reserved/allowlist census
rg -n '^(typus|valor|magnitudo|nomen|subtrahe|longitudo|applica|magnitudines|crea)\\s*=' \\
  /Users/ianzepp/work/faberlang/radix/stdlib/locale/en/pack.toml
rg -n 'STATUS_VARIANTS|request|item|byte|bulk|done|error|cancel' \\
  /Users/ianzepp/work/faberlang/radix/crates/radix/src/builtins/frame_types.rs \\
  /Users/ianzepp/work/faberlang/radix/crates/radix-runtime-contract/src/frame.rs
rg -n 'structa|creata|crea|formata|subtrahe|longitudo|applica|magnitudines' \\
  /Users/ianzepp/work/faberlang/radix/crates/radix/src/semantic
```

The existing live scratch result is already useful evidence: with the in-tree
Faber 1.7.0 binary, a temporary English file containing a `Tensor` field
`shape` and a `shape()` method returned `ok`. The preflight must preserve that
receipt and still probe the first real Tensor family file. The locked default
is therefore **field `forma → shape` plus method `figura() → shape()`**. If a
fresh first-file probe contradicts the scratch result, stop and amend the
ledger before any rename; do not invent a facade.

The seed's other collision defaults are locked as follows unless a live
first-file probe finds a concrete contradiction:

- `valor` never targets `value`; tensor/value carriers use `payload`, and an
  accessor may use `get` only where the receiver has no existing `get` member.
- `typus`/`typo` targets `dtype` on DType-bearing carriers and `kind` only
  outside that dtype meaning. It never targets `type`.
- `quantitas` targets `numel`, not `size`; live en maps `magnitudo = "size"`
  and `size` is therefore a reserved compiler spelling even though a bare
  scratch declaration may parse.
- `nomen` keeps the seed's `name` candidate only for a member position after
  the first-file probe includes the live `@ name` annotation-key context; if
  that probe reports a namespace collision, the family row must record the
  specific semantic escape (`label`, `field_name`, or another non-reserved
  target) before rename. This is a probe decision, not permission to use a
  guessed synonym.
- `causa` targets `message`; `structa` targets `construct`; `serializa_*`
  and `deserializa_*` target `serialize_*` and `deserialize_*`; `forma` and
  `figura` follow the Tensor shape collapse above; `longitudo` user members
  target `length` only after the receiver-specific probe.

### First-file probe discipline

`S2-PREFLIGHT` runs these scratch probes in order, one per source family, and
records the exact input copy, rename map, compiler revision, and result before
that family's batch is admitted:

| Family | First-file probe | Required collision focus |
| --- | --- | --- |
| L1 | `src/tensor.fab` | `forma` field + `figura()` method → `shape`/`shape()`, `gradus→rank`, `quantitas→numel`, `typus→dtype`, `accipe→get`, `structa→construct` |
| Shared | `src/parameter.fab` | `Parametrum→Parameter`, `Identitas→Identity`, `valor→payload`, `nomen→name` probe, `causa→message`, member-only params |
| Train | `src/optimize.fab` | `SgdStatum→SgdState`, `Passus→Step`, `structa→construct`, `inveni→find`, `lentus→rate`, `passus→step`, reserved status/type names |
| Arch | `src/attention.fab` | `RopeConfigura→RopeConfig`, `RopePolitica→RopePolicy`, `causa→message`, no compiler view/intrinsic capture |
| Model | `src/model/capsule.fab` | `Capsula→Capsule`, `valor→payload`/non-value escape, `nomen→name`, `forma→shape`, `longitudo→length`, error-class spellings |
| Tokenizer | `src/tokenizer.fab` | `Tokenizator→Tokenizer`, `IdentitasTokenizator→TokenizerIdentity`, `structa→construct`, `verifica→verify`, `CategoriaUnicode→UnicodeCategory` |
| Inference | `src/cache.fab` | `KVCache` accessors, `clavis→key`, `valor→payload`, `longitudo→length`, `redintegra→reset`, `appende→append` |
| Facade/callers | `src/gradus.fab` | `causa→message`, private helper spellings, facade exports, then exempla/tests call-site chase |
| Docs/inventory | no source file | Rebase only after all source probes and family ledgers are closed; rerun inventory against live names |

A probe is a scratch conversion of the first file plus its direct in-family
references, followed by the normal post-S1 English `faber check`; it is not a
second Pass A locale conversion and it does not write a source file. The probe
must check the renamed member in its real receiver/namespace position, not just
as a free declaration. A failing probe blocks that family and is a ledger
finding, not a reason to weaken the compiler check.

## Per-family locked ledger and unit graph

The rows below are the delivery ledger. Each family unit copies its row into
the preflight artifact, updates the row with the actual probe receipt, then
performs the one family rename. The path list names declaration/proof files;
call-site edits are limited to the old identifiers in that row. Import paths,
pack rows, and unrelated declarations are out of scope.

### S2-L1 — dtype / shape / tensor / math

| Field | Value |
| --- | --- |
| **id** | `S2-L1` |
| **outcome** | Rename the L1 foundation members to English, including the locked Tensor shape collapse, while preserving compiler intrinsics and `gradus:*` coordinates. |
| **write_scope** | `src/dtype.fab`, `src/dtype.proba`, `src/shape.fab`, `src/shape.proba`, `src/tensor.fab`, `src/tensor.proba`, `src/math.fab`, `src/math.proba`; matching Gradus source call sites for this row only. |
| **ledger** | `figura→shape`, field `forma→shape`, `gradus→rank`, `quantitas→numel`, `typus→dtype`, `valet→valid`, `accipe→get`, `structa→construct`, `structa_typo→construct_dtype`, `impleta→fill`, `FormaInvalida→InvalidShape`, `ElementaMismatch→ElementMismatch`, `TerminusExcedit→IndexOutOfBounds`, `causa→message`; `broadcastum→broadcast`, `reformanda→reshape`, `expansio→expand`, `promovet→promote`, `angusta→narrow`, `finita→finite`, `concatenatio→concatenate`, `segmentum→slice`; already-English arithmetic names stay. `nomen`/`typo` use the preflight member-position result. |
| **done_when** | The ledger row is updated with the scratch receipt; all listed `.fab` and `.proba` declarations/call sites use the locked names; no compiler intrinsic `forma`, `crea`, `formata`, `subtrahe`, `magnitudines`, or `longitudo` implementation is edited; narrow `faber check` on the touched first-file/module surface is green. |
| **depends_on** | `S2-PREFLIGHT`. |
| **sanity** | `FABER_BIN=… FABER_LIBRARY_HOME=… faber check src/tensor.fab` plus the touched L1 module checks. |
| **non_goals** | No S2 callers in exempla/tests, no docs rebase, no Radix changes, no dtype/shape behavior changes. |
| **risk** | high — field/method namespace collapse and compiler tensor intrinsic overlap. |
| **integrable** | no — later family call sites and the final exempla/tests chase remain on the pre-S2 names until the integration gate. |

### S2-SHARED — parameter / serialize / gradient

| Field | Value |
| --- | --- |
| **id** | `S2-SHARED` |
| **outcome** | Rename the shared parameter, wire-format, and gradient contracts as one API family, preserving serialization field order and error text. |
| **write_scope** | `src/parameter.fab`, `src/parameter.proba`, `src/serialize.fab`, `src/serialize.proba`, `src/gradient.fab`, `src/gradient.proba`; matching Gradus source call sites for this row only. |
| **ledger** | `Parametrum→Parameter`, `ParametrumError→ParameterError`, `Identitas→Identity`, `Statio→Station`, `Registrum→Registry`, `Tensum→SerializedTensor`, `ParametrumWire→ParameterWire`, `Gradiente→Gradient`, `Gradientes→Gradients`, `GradienteError→GradientError`; `valor→payload`, `figura→shape`, `quantitas→numel`, `typo→dtype`, `datos→data`, `nomen_typi→dtype_name`, `possessor→owner`, `identia→identity`, `muta→mutate`, `adscisco→add`, `inveni→find`, `contineo→contains`, `trainabiles→trainable`, `gelidae→frozen`, `ordo→order`, `causa→message`, and the seed `serializa/deserializa` pairs. `nomen` is a probe-locked member target; non-member params retain Latin unless swept incidentally. |
| **done_when** | The parameter/gradient public contracts and wire carrier names agree in `.fab`, `.proba`, and internal source call sites; the ledger includes the post-rename wire field map; no wire literal, version marker, or error message changes; first-file probe and touched-module checks are green. |
| **depends_on** | `S2-L1`. |
| **sanity** | `faber check src/parameter.fab`, `src/serialize.fab`, and `src/gradient.fab`; inspect serialization literals unchanged. |
| **non_goals** | No pack rows, no wire-format version bump, no parameter policy expansion, no exempla/tests chase. |
| **risk** | high — shared public names and serialized carriers are consumed throughout the library. |
| **integrable** | no — downstream training/model callers are intentionally chased by their family units. |

### S2-TRAIN — loss / optimize / nn / train / metrics / data

| Field | Value |
| --- | --- |
| **id** | `S2-TRAIN` |
| **outcome** | Rename the training-stack members without changing numerical behavior, error text, optimizer state wire shape, or the already-English loss/activation names. |
| **write_scope** | `src/loss.fab`, `src/loss.proba`, `src/optimize.fab`, `src/optimize.proba`, `src/nn.fab`, `src/nn.proba`, `src/train.fab`, `src/train.proba`, `src/metrics.fab`, `src/metrics.proba`, `src/data.fab`; matching Gradus source call sites for this row only. `data.fab` has no co-located `.proba` in the live tree. |
| **ledger** | `OptimizeError→OptimizeError` stays only where already English, `SgdStatum→SgdState`, `Passus→Step`, `Schedula→Schedule`, `Modus→Mode`, `Semen→Seed`, `Fructus→Draw`, `FructusF32→DrawF32`, `Excutio→Dropout`, `Tabula→Checkpoint`, `Metricum→Metric`; `structa→construct`, `lentus→rate`, `passus→step`, `semen→seed`, `stratorum→layers`, `dimensio→dimension`, `adscisco→add`, `inveni→find`, `contineo→contains`, `statum_aequus/sgd_aequus/tabula_aequus→*_equal`, `causa→message`; `mse`, `cross_entropy`, `linear`, `gelu`, `layernorm`, `rmsnorm`, `silu`, `swiglu`, and other already-English names stay. `data` has zero `fn ` declarations in the live inventory but is still included for call-site and header chase. |
| **done_when** | The six modules and their proofs use the family ledger; optimizer serialization markers and numeric formulas are byte/behavior identical; the reserved probe confirms no target is a keyword, type, STATUS_VARIANT, or compiler intrinsic; narrow checks are green. |
| **depends_on** | `S2-SHARED`. |
| **sanity** | `faber check src/optimize.fab`, `src/loss.fab`, `src/nn.fab`, `src/train.fab`; no full suite on the Hand. |
| **non_goals** | No model/inference rename, no new training API, no parameter renaming outside the member-scoped rule. |
| **risk** | high — optimizer state and training callers span several modules. |
| **integrable** | no — model and inference callers remain until their family units. |

### S2-ARCH — attention / transformer

| Field | Value |
| --- | --- |
| **id** | `S2-ARCH` |
| **outcome** | Rename attention and transformer configuration/error members while retaining already-English operation names and tensor semantics. |
| **write_scope** | `src/attention.fab`, `src/attention.proba`, `src/transformer.fab`, `src/transformer.proba`; matching Gradus source call sites for this row only. |
| **ledger** | `RopeConfigura→RopeConfig`, `RopePolitica→RopePolicy`, `TransformerError→TransformerError` stays, `causa→message`, `structa_rope_configura→construct_rope_config`, `politica_nomen→policy_name`, `politica_consecutiva→consecutive_policy`, `politica_interposita→interleaved_policy`, `rotary_position_embedding_configura→rotary_position_embedding_config`, `scaled_dot_product_causal_rope` and other already-English names stay; private helper renames follow the same English verb table and remain out of API inventory coverage. |
| **done_when** | Both modules, their proofs, and in-family references use the locked row; attention/transformer formulas and shape contracts are unchanged; first-file probe and narrow checks pass. |
| **depends_on** | `S2-TRAIN`. |
| **sanity** | `faber check src/attention.fab` and `src/transformer.fab`. |
| **non_goals** | No compiler attention feature, no math behavior change, no model assembly rename. |
| **risk** | medium-high — many private helpers share `typo`, `forma`, and error accessors. |
| **integrable** | no — model and facade callers remain until later units. |

### S2-MODEL — model artifact / capsule / GGUF / safetensors / dequant / tensor_* / dense_*

| Field | Value |
| --- | --- |
| **id** | `S2-MODEL` |
| **outcome** | Rename every live `src/model/*.fab` and matching `.proba` surface to the English model vocabulary, preserving artifact identity, file formats, admission rows, and tensor layout contracts. |
| **write_scope** | `src/model/artifact.{fab,proba}`, `capsule.{fab,proba}`, `dense.{fab,proba}`, `dense_llama.{fab,proba}`, `dense_qwen2.{fab,proba}`, `dequant.{fab,proba}`, `gguf.{fab,proba}`, `gguf_manifest.{fab,proba}`, `qwen35moe.{fab,proba}`, `safetensors.{fab,proba}`, `tensor_payload.{fab,proba}`, `tensor_view.{fab,proba}`; matching Gradus source call sites for this row only. |
| **ledger** | Apply seed types: `Capsula→Capsule`, `IdentitasContenuti→ContentIdentity`, `IdentitasCache→CacheIdentity`, `IdentitasTokenizator→TokenizerIdentity`, `ManifestumGguf→GgufManifest`, `ManifestumSafetensors→SafetensorsManifest`, `MetadatumGguf→GgufMetadata`, `DescriptioTensorisGguf→GgufTensorDescriptor`, `DescriptioTensorisSafetensori→SafetensorsTensorDescriptor`, `CorpusGguf→GgufCorpus`, `LectioFontis→SourceRead`, `VisumTensoris→TensorView`, `VisioError→ViewError`, `Manifesta→Manifest`, `FormaError→ShapeError`, plus every seed model type through `QwenCanonicalTensor`; `causa→message`, `valor→payload` or a receiver-specific non-value escape, `forma→shape`, `figura→shape`, `typus/typo→dtype` or `kind`, `longitudo→length`, `nomen→name` only after the annotation-key probe, `clavis→key`, `lege_*→read_*`, `admitto/admissio→admit/admission`, `praevideo→forward`, `inspice→inspect`, `verifica→verify`, `structa→construct`, `serializa/deserializa→serialize/deserialize`; already-English `TensorError`, `GgufError`, `DenseError`, `parse`, `layout`, `admit`, and technical dtype names stay. |
| **done_when** | All twelve model modules and their proofs use the row; GGUF/safetensors wire keys, hashes, tensor descriptor fields, admission constants, and error messages remain unchanged; the model first-file probe includes `valor`, `nomen`, `forma`, `longitudo`, and error/catch classes; touched module checks are green. |
| **depends_on** | `S2-ARCH`. |
| **sanity** | `faber check src/model/capsule.fab`, then the exact touched model leaves named by the batch. |
| **non_goals** | No GGUF/Safetensors format change, no PML5 implementation, no pack-row addition, no external model-consumer migration. |
| **risk** | high — 234 inventory rows and several artifact identity/wire contracts. |
| **integrable** | no — tokenizer/inference/facade callers remain until later units. |

### S2-TOKENIZER — tokenizer

| Field | Value |
| --- | --- |
| **id** | `S2-TOKENIZER` |
| **outcome** | Rename tokenizer identity, admission, encoding, decoding, and Unicode-category members while preserving pinned vocabulary and EOG/BOS behavior. |
| **write_scope** | `src/tokenizer.fab`, `src/tokenizer.proba`; matching Gradus source call sites for this row only. |
| **ledger** | `Tokenizator→Tokenizer`, `IdentitasTokenizator→TokenizerIdentity`, `CategoriaUnicode→UnicodeCategory`, `causa→message`, `structa→construct`, `verifica→verify`, `serializa/deserializa→serialize/deserialize`, `encoda/decoda→encode/decode`, `fabricare→build`, `categoria→category`, `nomen_categoriae→category_name`, `clavis→key`, `progenies→merges`, `digestio_vocabuli→vocab_digest`, `eog→eog`, `add_bos→add_bos`; already-English technical names stay, and the target `test`/`print`/`name`/`value` set remains reserved. |
| **done_when** | Tokenizer source/proofs and in-family references use the row; pinned vocab, EOG set, BOS/space policy, and serialized identity strings are unchanged; first-file probe and narrow `faber check` pass. |
| **depends_on** | `S2-MODEL`. |
| **sanity** | `faber check src/tokenizer.fab`. |
| **non_goals** | No tokenizer behavior correction, no corpus consumer migration, no compatibility alias. |
| **risk** | high — identity and wire strings are externally meaningful even in a pre-1.0 clean break. |
| **integrable** | no — inference and exempla callers remain. |

### S2-INFERENCE — cache / decode / sampling / generation

| Field | Value |
| --- | --- |
| **id** | `S2-INFERENCE` |
| **outcome** | Rename inference cache, decode, sampling, and generation members while preserving cache identity, token sampling behavior, and generation stop policy. |
| **write_scope** | `src/cache.{fab,proba}`, `src/decode.{fab,proba}`, `src/sampling.{fab,proba}`, `src/generation.{fab,proba}`; matching Gradus source call sites for this row only. |
| **ledger** | `KVCache` stays, `IdentitasCache→CacheIdentity`, `Pondera→Weights`, `Decodere→Decoder`, `Sessio→Session`, `Cancelatum→Cancellation`, `Configura→Config`, `Sortitio→Sampler`, `GeneratioConfigura→GenerationConfig`, `GenereCursor→GenerationCursor`, `causa→message`, `valor→payload`, `clavis→key`, `longitudo→length`, `redintegra→reset`, `appende→append`, `structa_*→construct_*`, `verifica→verify`, `serializa/deserializa→serialize/deserialize`, `praefundere→prefill`, `progredere→advance`, `cancellata→cancelled`, `prolata→emitted`; already-English `top_k`, `top_p`, `min_p`, `temperature`-style members stay. |
| **done_when** | All four modules and proofs use the row; cache identity fields, sampler probabilities, cancellation behavior, and generation EOG termination remain byte/behavior identical; first-file probe covers `payload`, `length`, `key`, `reset`, and `message`; narrow checks pass. |
| **depends_on** | `S2-TOKENIZER`. |
| **sanity** | `faber check src/cache.fab`, `src/decode.fab`, `src/sampling.fab`, and `src/generation.fab`. |
| **non_goals** | No runtime/GPU work, no PML5 re-lowering, no sibling consumer changes. |
| **risk** | high — 137 rows cross cache, decoder, sampler, and generation contracts. |
| **integrable** | no — the facade and exempla/tests chase is still outstanding. |

### S2-FACADE — facade plus exempla/tests chase

| Field | Value |
| --- | --- |
| **id** | `S2-FACADE` |
| **outcome** | Rename the `gradus` facade's remaining members and migrate every remaining in-repo Gradus call site, exemplum, and admission test to the completed family ledger. |
| **write_scope** | `src/gradus.fab`, `src/gradus.proba`, all `src/**/*.fab`/`.proba` call sites still matching the closed S2 ledger, `exempla/**/*.fab`, `exempla/**/faber.toml` only if a source path/name is quoted, and `tests/**/*.fab`; no sibling repos. |
| **ledger** | `GradusError→GradusError` stays as an already-English product type, `causa→message`, `_mappa→_map_error`, and any remaining facade helper follows its family row; facade imports remain `gradus:*`; no new facade genus is introduced. |
| **done_when** | `rg` finds no pre-S2 member spelling in code positions outside the sanctioned retained-parameter/comment/string set; all exempla/tests call the new names; `./scripta/check-compile` and the relevant `.proba` checks are green; every prior family ledger row has its final caller receipt. This is the first integrated source state. |
| **depends_on** | `S2-INFERENCE`. |
| **sanity** | `FABER_BIN=… FABER_LIBRARY_HOME=… ./scripta/check-compile` on the exact Gradus gate set; this is the one family sanity allowed to be broad. |
| **non_goals** | No `examples/training/*`, Inferentia docs, Norma/Tela/Triga, Radix pack rows, or pml5 work. |
| **risk** | high — it closes the cross-family caller graph and can expose a missed ledger row. |
| **integrable** | yes — after this unit the Gradus source, in-repo proofs, exempla, and tests share one identifier surface. |

### S2-DOCS — docs / inventory / compatibility rebase

| Field | Value |
| --- | --- |
| **id** | `S2-DOCS` |
| **outcome** | Rebase live Gradus documentation and gates to the completed English identifier surface and record the pre-1.0 clean break. |
| **write_scope** | `docs/api-reference.md`, `docs/module-map.md`, `AGENTS.md` only where it quotes live member names, `docs/compatibility-policy.md`, `scripta/inventory-public-symbols`, `scripta/check-source`, and the S2 ledger/delivery receipts. |
| **ledger** | Documentation must consume the final family ledgers, not repeat seed defaults. Inventory must assert the post-S2 live `fn ` total and coverage; guards ban renamed members only. Retained Latin parameters (`via`, `nomen`, `partes`, `clavis`, `initium`, and similar) are sanctioned by the member-scoped policy and are not added to the member guard. |
| **done_when** | Every `## gradus:<module>` API section matches live public names; module map and live headers agree; compatibility policy records the clean break and no aliases; inventory and source gates pass at the post-S2 baseline; `rg` confirms no stale member names except sanctioned params/comments/strings; docs claim no pack-row or sibling migration. |
| **depends_on** | `S2-FACADE`. |
| **sanity** | `./scripta/inventory-public-symbols`; `./scripta/check-source`; `git diff --check`. |
| **non_goals** | No product source rename in this unit, no comment-language rewrite, no sibling consumer migration, no new docs architecture. |
| **risk** | medium-high — stale docs or guard vocabulary can hide a real public-surface mismatch. |
| **integrable** | yes. |

## Parameter-depth policy (locked)

Gradus adopts the Norma reconciliation in `norma` commit `f7a5cc8`
(`docs(factory): reconcile param-rename depth policy`). Pass B renames
**members**: functions, types, fields, and private helpers. A parameter is
renamed only incidentally when the same spelling is swept by a member rename,
and the English spelling comes from the family ledger. Every other Latin
parameter is retained by decision, is outside the member guard, and is not a
unit done-when. This avoids positional-parameter churn and false positives
for words that are also valid English or domain vocabulary. `catch err`
bindings are local bindings, not member rows.

This policy is not a license to leave a renamed member's parameter stale when
the member sweep necessarily changes it. The family Hand must update that
same-spelling parameter when it is part of the declaration/reference sweep,
but must not widen the sweep to every Latin parameter in the file.

## Integration and merge gate

`S2-PREFLIGHT` is integrable and must land first. `S2-L1` through
`S2-INFERENCE` are ordered, non-integrable transitional family commits because
later Gradus modules and the final exempla/tests chase intentionally retain
old call sites until their owning unit. `S2-FACADE` is the aggregate source
integration point. The merge gate after `S2-FACADE` must verify:

1. every family row has a committed first-file probe and final ledger receipt;
2. the Gradus root and the exact `check-compile` exempla set are green;
3. no `src/`/`.proba`/exempla/test code position uses a stale renamed member;
4. no `[[library_members]]` row or sibling-repo edit was introduced; and
5. the staged-carrying PML5 gate remains separate.

`S2-DOCS` follows that gate. The pml5 re-lowering request `88010bfc` is
unlocked only after S2 completion; it is not a dependency of any S2 Hand.

## Lane-owned validation (named once)

- **Family sanity:** one post-S1 English `faber check` on the first real file
  of each family, then the touched module set. Scratch probes do not replace
  the real-file check.
- **Integrated source gate:** `FABER_BIN=… FABER_LIBRARY_HOME=…
  ./scripta/check-compile` after `S2-FACADE` and at the merge gate.
- **Source guard:** `./scripta/check-source` at `S2-DOCS`/merge gate. The
  guard is member-scoped per the parameter policy.
- **Inventory/docs gate:** `./scripta/inventory-public-symbols` after the
  API-reference rebase. The pre-S2 750 baseline is not reused as the
  post-S2 name map; the script must be rebaselined only from the live final
  tree, with any `grep -c 'fn '` drift explained.
- **Clean-break review:** `docs/compatibility-policy.md` and landing commit
  record no aliases, no translation rows, and no sibling-repo claims.

## Open questions for Mind

1. None blocking delivery. The `name` member-position result and every other
   reserved-name result are intentionally owned by `S2-PREFLIGHT`; a probe
   contradiction is a ledger finding that must be resolved before dispatch,
   not an implementation-time guess.
2. Sibling consumers remain S3 by campaign contract. Do not add them to S2 to
   make the in-repo checks convenient.
