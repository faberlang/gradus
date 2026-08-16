# Goal: Gradus English locale + English identifiers

**Status**: planned — Pass A is `faber format --locale en` after each file declares input locale `la`; Pass B renames user identifiers
**Repo**: gradus
**Created**: 2026-08-15
**Consumer**: campaign `docs/factory/english-locale/CAMPAIGN.md`, then delivery / factory
**Sibling campaigns**: `docs/factory/production-ml-library/CAMPAIGN.md` (do not mix product ML work into this goal)

## Summary

Convert Gradus from the Latin reader surface to English in two passes. Pass A
changes only locale-pack vocabulary (keywords, types, localized intrinsics)
and flips every package to `locale = "en"`. Pass B renames user-chosen
functions, types, fields, and parameters to English. Import coordinates such
as `gradus:tensor` stay. Gradus is pre-1.0, so this is a recorded clean break
with no shims.

## Problem

- The library package and all 17 exempla still declare `[reader] locale = "la"`.
- Source files have no `+++` frontmatter; locale comes from the nearest
  `faber.toml`. The product default for an untagged package is already `en`.
- User identifiers (`figura`, `accipe`, `Capsula`, `causa`, `valor`) are not
  locale-pack rows. `--locale` does not rename them.
- Locale packs are identity maps. Input locale (file frontmatter) and
  emit locale (`--locale`) are independent axes. Live probe 2026-08-15:
  a Latin program with `+++ locale = "la" +++` plus
  `faber format --locale en` emits English keywords and keeps comments;
  `--locale la` on that English body restores Latin keywords. User
  identifiers do not move. Gradus `src/` has no frontmatter today, so a
  bare `--locale en` on those files parses as English and fails. That is
  a missing input-locale stamp, not a reason to avoid format.
- Several public names collide with the English pack if renamed naively:
  `valor` → `value` (en type), `typus` → `type` (en keyword). Tela already
  hit `fn value(...)` → `SEM005`.
- Inventory and source gates still grep Latin spellings (`functio `,
  `sponte`). Those gates break on Pass A unless updated in the same wave.

## Goals

1. Every owned `.fab` / `.proba` package compiles under the English pack.
2. Manifests use `[locale] locale = "en"` (write the canonical table, not the
   legacy `[reader]` alias).
3. Pass A is `faber format --locale en` after each converted file declares
   input locale `la` in frontmatter. Pack vocabulary localizes. Comments,
   strings, import paths, and user identifiers stay.
4. Pass B lands an English public identifier surface with a locked rename
   table. Reserved-name collisions are named before any rename lands.
5. `scripta/check-source`, `scripta/check-compile`, and
   `scripta/inventory-public-symbols` track the English surface.
6. `docs/api-reference.md` and the symbol inventory rebase to the new names.
7. In-repo exempla and `tests/` migrate with the library. Sibling consumers
   (`examples/training/*`, Inferentia docs) are a recorded follow-up, not a
   silent leftover.

## Non-goals

- No radix/compiler changes. The en pack already has the keyword and type
  rows. Gradus stamps file frontmatter so `--locale` can stay the emit
  axis; do not retask the flag as the input locale.
- No `[[library_members]]` Gradus rows in the en pack. Pass B renames the
  canonical identifiers; it does not add a translation layer over Latin
  names.
- No forwarding aliases, deprecation window, or dual-authority API.
- No production-ML-library product work (new modules, GGUF, Qwen).
- No Norma conversion. Gradus does not import Norma.
- No comment-language rewrite of factory history under
  `docs/factory/production-ml-library/`. Live API docs and AGENTS.md do move.

## Ground Truth Researched

- `faber.toml` and 17 exempla manifests: `[reader] locale = "la"`.
- Frontmatter `locale = "en"` already exists only on
  `scripta/check-*.fab` and `fixtures/*/gen_fixture.fab`.
- Live surface: 33 `src/**/*.fab`, 32 co-located `.proba`, 17 exempla
  `main.fab`, 1 `tests/admission_conformance.fab`. Inventory baseline is
  749 `functio` declarations (`pml0-symbol-inventory.md`).
- Live probe (2026-08-15, in-tree `radix/target/debug/faber`):
  frontmatter `locale = "la"` + `format --locale en` converts
  `src/dtype.fab` (108 comments kept; `functio`/`textus`/`redde` gone from
  code tokens). The same file with no frontmatter fails under
  `--locale en` because the CLI pack is then used to lex.
- Fan-out precedent: `radix/crates/radix/src/driver/locale_fanout_test.rs`
  — Latin frontmatter, session pack = emit locale.
- HIR reprint is not byte-identical: `dtype.fab` 336 → 418 lines;
  `fixum _ greeting` came back as `const string greeting`. Keyword
  identities round-trip. Layout and inferred types do not.
- Token-level precedent: `radix/scripta/convert-corpus-locale.py`. It
  substitutes pack `[keywords]` / `[types]`, copies comments and strings,
  and currently requires file frontmatter. Gradus library files have none.
- Tela English adoption
  (`tela/docs/archived/web-surface-import/GOAL.md`): two layers — keyword
  locale, then identifier review. Forced rename: `value` → `input_value`.
- Triga package is already `[reader] locale = "en"`. Norma exempla still
  `la`. Gradus is the next library to flip.
- Compatibility: `docs/compatibility-policy.md` — pre-1.0, clean break, no
  shims. Record the break in the commit + this policy.
- En pack collisions that matter here (`radix/stdlib/locale/en/pack.toml`):
  `typus = "type"`, `valor = "value"`, `nihil` keyword `"null"` vs type
  `"null_ty"`, `vacua` stays `vacua`, `sponte = "optional"`.
- Latin type spelling for `nihil` is `nullum` in the la pack, so the
  convert script’s keyword/type maps do not collide on the source word
  `nihil`. Gradus writes `T ∪ nihil` (keyword), which becomes `T ∪ null`.
- No Gradus `[[library_members]]` rows exist in the en pack. Triga/Norma
  rows there are unrelated.
- Sibling consumers: `examples/training/{mlp,linear-regression,bert-tiny-fragment,bert-gradus-probe}`
  import `gradus:*` under `locale = "la"`. Inferentia discovery docs quote
  Latin Gradus names.

## Reference Packet

- `radix/stdlib/locale/en/pack.toml` — keyword, type, intrinsic, library-member rows
- `radix/crates/radix/src/driver/locale_fanout_test.rs` — input frontmatter × emit pack
- `radix/crates/faber/src/commands/format.rs` — `--locale` is the emit pack
- `faber.toml`, `exempla/*/faber.toml` — package locale pins
- `src/tensor.fab` — representative Latin API (`figura`, `gradus`, `typus`, `accipe`, `forma`)
- `docs/api-reference.md`, `scripta/inventory-public-symbols`
- `docs/compatibility-policy.md`, `docs/api-shape-policy.md`
- `docs/factory/english-locale/rename-seed.md` — reserved names + seed map
- Validation: `./scripta/check-source`, `./scripta/check-compile`

## Constraints And Invariants

- Code locale and diagnostics locale are separate. Do not infer syntax from
  diagnostic prose.
- Import coordinates (`gradus:shape`, `gradus:model/gguf`) do not localize.
- User identifiers do not localize in Pass A, including names that look like
  Latin keywords (`typus()`, `valor()`, `gradus()`).
- Intrinsic calls that are pack rows (`longitudo`, `continet`, `accipe` on
  `lista`) do localize in Pass A. User methods with the same spelling stay
  until Pass B.
- Optional fields: Latin `sponte` → English `optional`. `check-source` must
  stop requiring the Latin word.
- Empty collections stay `vacua` (en pack identity).
- Nullable types: `T ∪ nihil` → `T ∪ null`.
- `@ publica` / `@ privata` become `@ public` / `@ private`.
- `scripta/inventory-public-symbols` must count `fn ` after Pass A, then the
  renamed names after Pass B.
- Pre-1.0 clean break: no Latin aliases left in `src/`.
- Do not mix this work into an in-flight PML5 GGUF unit.

## Architecture Direction

Two stacked surfaces, one grammar:

```text
Pass A  pack vocabulary only     functio→fn, textus→string, sponte→optional
        + manifest locale = en
        identifiers stay Latin   fn figura() → list<int>

Pass B  user identifiers         figura→shape, accipe→get, Capsula→Capsule
        reserved-name escapes    valor↛value, typus↛type
```

Pass A tool is `faber format --locale en`. Stamp
`+++ locale = "la" +++` on each file first so lex stays Latin while emit
is English. After a green rewrite, flip frontmatter and
`[locale] locale = "en"`. Prove with `faber check`. Do not substitute a
hand-rolled token script for the pack renderer.

Pass B is a reviewed rename table applied module-family by module-family,
then one docs/inventory rebase. Sibling-repo consumers are a later campaign
stage, not a reason to keep Latin names in Gradus.

## Supporting Skills

- `$faber` + `references/locales.md` — resolve locale before judging spellings
- `$delivery` — lower each campaign stage to Hand-sized units
- `$zombie-docs` — rebase `docs/api-reference.md` after Pass B
- `$clean-break` — no shims

## Implementation Shape

- Milestone 0 (this prep): goal, campaign, rename-seed, reserved-name lock.
- Milestone 1 (Pass A): stamp `locale = "la"` frontmatter; `faber format
  --locale en`; flip file + package locale to `en`; update grep gates;
  `check-compile` green.
- Milestone 2 (Pass B): locked rename table applied to `src/`, `.proba`,
  exempla, tests; inventory + api-reference rebase.
- Later: `examples/training/*` and Inferentia doc quotes.

## Release Posture

Decision: defer-release / not-applicable as a Gradus product release.
Gradus has no standalone release. Record the clean break in
`docs/compatibility-policy.md` and the landing commit. Sibling consumers
migrate at the new shape.

## Exit Strategy

Decision: included.

- Pass A is mechanical and reversible from git (`git checkout -- src exempla`).
- Pass B lands only after the rename table is locked. A bad name is a new
  rename, not a shim.
- If `faber check --locale en` fails on a pack-gap (missing en row), stop
  and file a radix locale need. Do not invent aliases in Gradus source.

## Acceptance Criteria

- `faber.toml` and every in-repo `exempla/*/faber.toml` declare
  `[locale] locale = "en"`.
- `faber check` on the library and the `check-compile` exempla set is green
  with no `--locale la` override.
- No Latin keyword/type spellings remain in code tokens under `src/`,
  `exempla/`, or `tests/` (comments may still mention Latin until a later
  comment pass).
- Every public identifier in `docs/api-reference.md` matches live `src/`
  after Pass B. `scripta/inventory-public-symbols` is green.
- Reserved-name escapes from `rename-seed.md` are honored (`valor` is not
  `value`; `typus` is not `type`).
- Compatibility policy records the break.

## Validation

- Pass A scratch: prepend `+++ locale = "la" +++` to a copy of
  `src/dtype.fab`, then `faber format --locale en --stdout`. Expect
  English keywords, comments kept, identifiers unchanged.
- Pass A proof: `FABER_BIN=… ./scripta/check-compile` after the manifest flip.
- Pass A gate: `./scripta/check-source` (updated patterns).
- Pass B proof: `./scripta/check-compile` + `./scripta/inventory-public-symbols`.
- Review: no `functio` / `importa` / `textus` / `redde` in code tokens;
  `rg -n '\\b(functio|importa|textus|redde|sponte)\\b' src exempla tests`.

## Open Questions

1. Pass B constructor verb: `structa` → `construct`, `make`, or keep
   per-module English verbs (`tensor`, `cache`, …)? Default in the seed:
   `construct` for shared constructors, keep already-English names.
2. Error accessor: `causa` → `message` (matches current English diagnostic
   strings) or `cause`? Seed default: `message`.
3. Tensor rank method: `gradus()` → `rank`. Confirm; do not use `degree`.
4. Are `examples/training/*` in this campaign’s completion contract or a
   sibling follow-up? Seed default: sibling follow-up, named in the campaign
   so it is not forgotten.
5. Comment-language refresh (Latin words inside `#` headers) — in Pass A,
   Pass B, or a later docs pass? Seed default: later; do not block compile.

## Stop Conditions

- Stop if an en-pack row is missing for a keyword or type Gradus actually
  uses. That is a radix locale gap, not a Gradus workaround.
- Stop if Pass A is attempted with `--locale en` and no input-locale
  frontmatter — that parse-as-English failure is expected and is not a
  reason to abandon format.
- Stop if a Pass B name collides with an en keyword/type and the seed has
  no escape. Lock the escape first.
- Stop if an in-flight PML5 unit and this conversion would touch the same
  files in the same merge wave.
