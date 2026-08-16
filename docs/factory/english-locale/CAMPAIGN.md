# Campaign: Gradus Latin → English

**Status**: planned — routing artifact; does not implement code
**Created**: 2026-08-15
**Mode**: draft/maintain
**Control-plane repo**: `/Users/ianzepp/work/faberlang/gradus`
**Goal**: [`GOAL.md`](GOAL.md)
**Rename seed**: [`rename-seed.md`](rename-seed.md)
**Do not mix with**: [`../production-ml-library/CAMPAIGN.md`](../production-ml-library/CAMPAIGN.md)

## Summary

Two mandatory passes convert Gradus to the English reader surface and then
to English identifiers. Pass A is `faber format --locale en` after each
file declares input locale `la`. Pass B is a reviewed public-API rename.
Sibling consumers are a named follow-up, not silent leftovers.

## Problem

The library still authors Latin keywords (`functio`, `importa`, `textus`)
under `[reader] locale = "la"`, while the Faber product default is `en`.
`faber --locale` / `faber format --locale` changes the reader surface, not
user names. A second pass has to rename `figura`, `Capsula`, `admitto`, and
the rest. Doing both at once hides reserved-name collisions
(`valor` / `typus`) inside a noisy keyword diff.

## Desired End State

1. Gradus packages declare `[locale] locale = "en"` and compile that way.
2. Code tokens use the English pack. User identifiers are English, with
   reserved-name escapes from the seed.
3. In-repo exempla, tests, inventory, and live API docs match.
4. The compatibility policy records the pre-1.0 clean break.
5. Sibling consumers are listed with an owner, not left as surprise breakage.

## Development Posture

Clean break. No Latin aliases. No `[[library_members]]` translation layer
over old Gradus names. Pass A must not use HIR re-emission as the rewriter.

## Implementation Workflow

`campaign` (this file) → `delivery` per stage → factory / Hands.
`$faber` locales reference before any spelling judgment.

## Scope Routing

| In campaign | Split out |
| --- | --- |
| `src/**/*.fab`, `src/**/*.proba` | PML5 GGUF / Qwen product work |
| In-repo `exempla/**`, `tests/` | Norma locale conversion |
| Manifest locale flip | Radix lossless-transcode substrate |
| `scripta/check-source`, `check-compile`, `inventory-public-symbols` | Comment-language refresh of historical factory docs |
| `docs/api-reference.md`, `docs/module-map.md`, `AGENTS.md`, compatibility policy | Inferentia product code (docs quotes only are listed as follow-up) |
| Rename-seed lock | |

## Batching And Split Policy

- Pass A: `batch-by-default` after one file family proves the rewriter
  (library `src/`, then `.proba`, then exempla).
- Pass B: `split-on-boundary` by module family (L1 tensor foundation, then
  training, then model/tokenizer, then inference). Do not rename the whole
  749-function surface in one Hand.
- Docs/inventory rebase: one Hand after each Pass B family, or one rebase
  Hand after all families if landing is atomic on merge.

## Ground Truth Researched

See `GOAL.md` §Ground Truth. Headline facts:

- 33 library `.fab`, 32 `.proba`, 17 exempla, 1 test file.
- 749 `functio` declarations; inventory greps the Latin word.
- `faber format --locale en` converts Latin→English when the file declares
  input locale `la` (live probe 2026-08-15 on `dtype.fab` + a salve
  round-trip). Gradus sources need that frontmatter stamp first.
- Tela already paid the `value` collision. Triga is already `en`.

## Current State

| Track | State | Next action |
| --- | --- | --- |
| Prep / lock | drafted | accept goal + seed defaults, or correct open questions |
| Pass A locale surface | planned | lower delivery for rewriter + manifest flip |
| Pass B identifiers | planned | lock remaining seed rows, then family Hands |
| Sibling consumers | planned follow-up | file examples/Inferentia units after Pass B |

## Campaign Path

### S0 — Prep lock

- **Status**: active (this draft)
- **Why now**: user asked to prep, not implement
- **Gate**: goal + seed committed; reserved names locked
- **Lowers to**: none (docs only)
- **Batching**: n/a

### S1 — Pass A: locale surface

- **Status**: planned
- **Source**: `GOAL.md` Pass A; `convert-corpus-locale.py`
- **Why now**: identifiers cannot be renamed honestly while keywords are still Latin
- **Overlap rule**: do not edit the same `src/` files as an in-flight PML5 Hand
- **Gate**: `./scripta/check-compile` green with `[locale] locale = "en"`;
  `rg` finds no Latin keyword/type tokens in code
- **Lowers to**: `delivery` then `factory`
- **Batching**: `batch-by-default`
- **Units (suggested)**:
  1. Stamp `+++ locale = "la" +++` on owned `.fab` / `.proba` that lack it
  2. `faber format --locale en` on `src/**/*.fab`; flip those files + root
     `faber.toml` to `en`; update inventory/check-source greps
  3. Same for `src/**/*.proba`
  4. Same for exempla + tests + their manifests
  5. `check-compile` closeout

### S2 — Pass B: identifier rename

- **Status**: planned
- **Source**: `rename-seed.md`
- **Why now**: after S1, names are the only Latin left in code tokens
- **Overlap rule**: one module family per Hand; docs rebase may trail by one family
- **Gate**: inventory + api-reference match live names; `check-compile` green
- **Lowers to**: `delivery` then `factory`
- **Batching**: `split-on-boundary` (module family)
- **Families**:
  1. L1: dtype, shape, tensor, math
  2. Shared: parameter, serialize, gradient
  3. Train: loss, optimize, nn, train, metrics, data
  4. Arch: attention, transformer
  5. Model: artifact, capsule, gguf*, safetensors, dequant, tensor_*, dense*
  6. Tokenizer
  7. Inference: cache, decode, sampling, generation
  8. Facade `gradus.fab` + exempla/tests chase
  9. Docs/inventory/compatibility rebase

### S3 — Sibling consumer follow-up

- **Status**: planned
- **Source**: `examples/training/*`, Inferentia discovery quotes
- **Why now**: Gradus clean-break lands first; consumers migrate at the new shape
- **Gate**: named owner + paths; not a Gradus `check-compile` blocker
- **Lowers to**: `delivery` in those repos
- **Batching**: `split-on-boundary` by repo

## Dependency Rules

- S1 before S2. Never rename identifiers in the same diff as the keyword rewrite.
- S2 family 8 (exempla chase) after the library families it calls.
- S3 after S2 closeout. Do not hold Gradus main for examples/Inferentia.
- If Pass A hits a missing en-pack row, route a radix locale need and pause S1.

## First Useful Milestones

1. `src/dtype.fab` with `locale = "la"` frontmatter, then
   `faber format --locale en`, comments intact — proves Pass A.
2. Whole library + exempla on `locale = "en"` with Latin identifiers still
   compiling — Pass A done.
3. L1 names English (`shape`, `rank`, `get`, `construct`) — Pass B pattern
   proven.

## Acceptance Criteria

- Every listed stage is completed or explicitly amended out of this campaign.
- Pass A uses `faber format --locale en` with an explicit input-locale
  frontmatter of `la`.
- Pass B honors `rename-seed.md` reserved escapes.
- In-repo validation: `check-source`, `check-compile`, `inventory-public-symbols`.

## Validation

Artifact: this file names the next stage (S1 after lock).
Implementation: delegated to the delivery specs for S1 and S2.

## Open Questions

Carried from `GOAL.md`: constructor verb, `causa` spelling, `examples/`
in-or-out of the completion contract (default: out, named follow-up),
comment-language refresh (default: later).

## Stop Conditions

- Do not start S1 while a PML5 Hand is writing the same module.
- Do not start S2 until the seed’s reserved names and the still-open
  constructor/`causa` rows are locked.
- Do not run `format --locale en` on Gradus files that still lack
  `locale = "la"` frontmatter. Stamp first, then convert.
