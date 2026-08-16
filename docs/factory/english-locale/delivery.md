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
   `resolve_convert_paths`), and `--stdin` is a locale no-op (virtual sources
   skip the package probe and emit canonical/Latin). So `src/**/*.proba`
   cannot be converted directly. Sanctioned route (still the pack renderer,
   no hand-rolled token script): copy each stamped `.proba` to a
   `<name>.proba.fab` file outside the repo (e.g. `mktemp` dir), run
   `faber convert --to en --stdout` on that copy, and write the converted
   output back to the `.proba` path; then flip the frontmatter. Never leave a
   stray `*.fab` in `src/` during a package check.
3. **Mixed wave states are green (probed).** An `en` package whose co-located
   `.proba` still declares `locale = "la"` frontmatter passes `faber check`.
   The root `faber.toml` flip to `en` may land mid-wave (unit 2) without
   breaking the gate; each file's frontmatter is the input-locale authority.
4. **Convert preserves the source frontmatter as `la`.** The flip
   `locale = "la"` → `locale = "en"` is a separate mechanical edit in the
   same unit, per the goal ("After a green rewrite, flip frontmatter").
5. **Inventory counts survive conversion.** Probed on `src/dtype.fab`:
   `grep -c 'functio '` (14) == `grep -c 'fn '` (14) after conversion; the
   declaration lines map 1:1 even though total lines grow (340 → 418). The
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
  doc-coverage gate). `faber check` compiles `src/*.fab` **and** co-located
  `.proba` (probed; PML6 delivery records the same).
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
| **done_when** | All 83 files start with the exact block `+++\nlocale = "la"\n+++\n`; `rg -l '^\+?\+' src exempla tests` shows only the stamped files and none of `scripta/`/`fixtures/` was touched; `faber check` on the root package and on a sample of the 8 gate exempla is green (stamp is semantically neutral — la frontmatter == la package default). |
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
| **read_scope** | `radix/crates/faber/src/commands/convert.rs` + `format.rs` (extension filter, stdin no-op), S1-U2's converted `src/*.fab` (import targets) |
| **done_when** | Every `.proba`'s body is English and its frontmatter is `locale = "en"`; `faber check` on the root package is green (`.proba` are part of the package check surface — probed), proving no Latin keyword/type token remains in a code position. Route (per file, in a temp dir outside the repo, e.g. `mktemp -d`): copy the stamped `X.proba` to `X.proba.fab`, run `faber convert --to en --stdout` on the copy (with `FABER_LIBRARY_HOME` set so `gradus:*` imports resolve), write the output back to `X.proba`, delete the temp copy, then flip the frontmatter. Never leave a `*.fab` in `src/` while running a package check. |
| **validation** | `faber check` root green; spot-grep a few `.proba` for `fn ` / `string` and for residual Latin keywords in code positions |
| **depends_on** | S1-U2 (library `.fab` already en; unit order also keeps the wave's grep gates consistent) |
| **non_goals** | No `.fab` edits, no manifest changes, no rename of proba assertion names (identifiers survive Pass A) |
| **risk** | medium — same en-pack gap stop condition as U2; the routing workaround is the one non-`convert` step, kept to file movement only. |
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
| **done_when** | (a) `FABER_BIN=… ./scripta/check-compile` exit 0 (library + gradient-seam, training-loop-mlp, token-generation, gguf-manifest, gguf-inspect, gguf-materialize, qwen36-35b-inference, gguf-admit-qwen35moe); (b) `./scripta/check-source` exit 0; (c) `./scripta/inventory-public-symbols` exit 0 with the 749 baseline and full doc-coverage (names unchanged in Pass A); (d) goal acceptance grep — `rg -n '\b(functio|importa|textus|redde|sponte)\b' src exempla tests` — every hit is a comment line or a user identifier, none a keyword/type token (the en compiler check already guarantees the latter; the grep is the review evidence); (e) the clean break is recorded in the landing commit message per goal Release Posture. |
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
