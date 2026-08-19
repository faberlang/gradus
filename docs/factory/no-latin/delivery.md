# Delivery — no-latin English conversion (P3 lowering)

**Lowered**: 2026-08-19, planner, from `GOAL.md` (verdict READY — see
`goal-check.md`), ledger LOCKED 7 units. One ledger row is split (row 7 →
U7 + U8) under the lock rule "splitting only where a unit is genuinely two
logical changes": enforcement-gate code (`scripta/`) and docs regeneration
(`docs/`) are disjoint write surfaces with different verification. Ledger
rows map 1:1 otherwise; no unit was merged, narrowed, or dropped.

**Tree**: gradus `main` @ `6b3a6c7` (clean).

---

## 1. Interpreted theme

Finish the English conversion of gradus: eliminate every Latin identifier,
parameter, local, alias, comment, and owned string from owned surfaces,
retaining only the proper noun `gradus`, established technical terms
(`eog`, `silu`, `signum`, `fim`, `bpe`, `matmul`, dtype/model tokens), and
external-format keys (GGUF/safetensors spec strings). Behavior-preserving
renames except owned wire literals, which convert and regenerate fixtures.
Clean break, pre-1.0, no shims.

## 2. Normalized spec

All of `src/**/*.fab{,.proba}`, `exempla/**`, `tests/`, `scripta/*.fab`, and
fixture generators pass a no-Latin census (identifiers, comments, owned
strings) against an explicit retained-exception list; public docs and
enforcement gates reflect the final English surface; the clean break is
recorded in `docs/compatibility-policy.md`.

## 3. Repo-aware baseline

Corrected receipts (method + deltas in `goal-check.md`):

- 23 public Latin fns; 34 Latin class fields; 201 Latin union-case
  occurrences (95 distinct); 1 type (`GeneratioError`); Latin import aliases
  (`manifestum` ×8 src files, `capsula` ×2, `tokenizator`, `parametrum`).
- Gate state: `check-source` exit 0 (blind to non-ledger Latin);
  `inventory-public-symbols` exit 1 (750 baseline vs 979 live; 97
  coverage-failed symbols — grew past the goal's 47).
- Naming inputs: `docs/archived/english-locale/rename-seed.md` (reserved-name
  escapes: `valor`→`payload`, `quantitas`→`numel`), `s2-collision-ledger.md`.
- **Sanity tooling (ground truth)**: no cargo in this repo. Narrow check is
  `faber check` scoped to one module file or the gradus package:
  `FABER_LIBRARY_HOME=<workspace> FABER_BIN=<ws>/radix/target/debug/faber`;
  single-file checks need **absolute** paths (relative paths fail with
  `cannot read ''`). Package root check: `"$FABER_BIN" check "$ROOT"`.
- Fixture regen: `scripta/gen-fixture-gguf`, `scripta/gen-fixture-safetensors`.

## 4. Hand unit graph

Order: U1 → {U2, U3, U4, U5} in parallel (disjoint write scopes) → U6 →
U7 → U8. Max useful parallelism 4.

### U1 — lock the rename ledger

| Field | Value |
| --- | --- |
| id | `no-latin-U1` (ledger row 1) |
| outcome | Exhaustive old→new map for every remaining Latin identifier (23 pub fns, 34 fields, all variant names with collision check across modules, `GeneratioError`, aliases, param/local word families, comment/string vocabulary) plus the explicit retained-exception list |
| write_scope | `docs/factory/no-latin/rename-ledger.md` (new file only) |
| done_when | Ledger enumerates per-class old→new rows reconciling to the corrected census counts; reserved-name escapes inherited from archived `rename-seed.md`; retained-exception list names `gradus`, technical terms, external-format keys; collision check recorded where one Latin name maps ambiguously |
| depends_on | — |
| sanity | none (docs-only); cross-foot row counts against `goal-check.md` receipts |
| non_goals | Any `src/` edit; deciding the wire-literal pin (goal OQ3 — operator may pin wire stability; ledger records both target and the pending pin) |
| risk | low |
| integrable | yes |

### U2 — model family wave (epicenter)

| Field | Value |
| --- | --- |
| id | `no-latin-U2` (ledger row 2) |
| outcome | All Latin gone from the model family per U1 map: fns, fields (incl. the 4 safetensors fields the goal table missed), variants, params, locals, aliases (`manifestum`, `capsula`), comments, owned strings |
| write_scope | `src/model/gguf_manifest.fab`, `src/model/qwen35moe.fab`, `src/model/safetensors.fab`, `src/model/artifact.fab`, `src/model/capsule.fab`, `src/model/tensor_payload.fab`, `src/model/tensor_view.fab`, `src/model/dense.fab`, `src/model/dense_llama.fab`, `src/model/dense_qwen2.fab`, `src/model/dequant.fab`, `src/model/gguf.fab` + each co-located `.proba` |
| done_when | Zero ledger-Latin tokens remain in those 24 files; proba expectations use new names |
| depends_on | U1 |
| sanity | After the first touched file and again at close: `"$FABER_BIN" check "$PWD/src/model/<module>.fab"` (absolute path) green per module |
| non_goals | Consumer chase outside `src/model/` (U6); tokenizer wire literals (U3); docs (U8); gate code (U7) |
| risk | medium — ~60% of remaining tokens, cross-module callers inside the wave (gguf → gguf_manifest → qwen35moe ordering matters; rename leaves first) |
| integrable | no — transitional: exempla and later-wave modules still reference old names |

### U3 — tokenizer + calibration wave (wire literals)

| Field | Value |
| --- | --- |
| id | `no-latin-U3` (ledger row 3) |
| outcome | All Latin gone from tokenizer/calibration per U1 map, including the owned category wire literal (e.g. `aliud` → its English value per OQ3 default) with fixtures regenerated |
| write_scope | `src/tokenizer.fab`, `src/calibration.fab`, `src/tokenizer.proba`, `src/calibration.proba`, `fixtures/tokenizer/**` (regenerated), `fixtures/gguf/**` + `fixtures/safetensors/**` only if a U1-mapped literal reaches them |
| done_when | Zero ledger-Latin tokens in the two modules + proofs; fixture bytes regenerated via `scripta/gen-fixture-*` and consistent with the new wire values |
| depends_on | U1 |
| sanity | `"$FABER_BIN" check "$PWD/src/tokenizer.fab"` and `.../calibration.fab` green; regen diff reviewed |
| non_goals | Model-family files (U2); consumer chase (U6); pinning wire values (operator OQ3 — if pinned, convert internals only and record the pin) |
| risk | medium — wire-literal changes alter fixture bytes |
| integrable | no — fixture consumers and exempla chase in U6 |

### U4 — inference + gradient + nn wave

| Field | Value |
| --- | --- |
| id | `no-latin-U4` (ledger row 4) |
| outcome | All Latin gone per U1 map, incl. `GeneratioError`→`GenerationError`, `decodere_datum`, `projectio_bias`, `gradientes_*`, decode/generation/cache/sampling variants |
| write_scope | `src/decode.fab`, `src/generation.fab`, `src/cache.fab`, `src/sampling.fab`, `src/gradient.fab`, `src/nn.fab`, `src/math.fab` + co-located `.proba` |
| done_when | Zero ledger-Latin tokens in those files; retained technical terms (`signum`, `silu`, `eog`-bearing names) untouched per exception list |
| depends_on | U1 |
| sanity | `"$FABER_BIN" check "$PWD/src/<module>.fab"` green per touched module |
| non_goals | Consumers (U6); the modules of U2/U3/U5 |
| risk | medium — decode/generation call tokenizer fns renamed in U3; run after or coordinate callers when landing |
| integrable | no — transitional until U6 |

### U5 — remaining-modules sweep

| Field | Value |
| --- | --- |
| id | `no-latin-U5` (ledger row 5) |
| outcome | All Latin gone per U1 map across the long tail: variants (`Gelida`, `PassusInvalida`, `SchedulaInvalida`, …), params, locals, comments, owned strings |
| write_scope | `src/train.fab`, `src/optimize.fab`, `src/parameter.fab`, `src/serialize.fab`, `src/loss.fab`, `src/metrics.fab`, `src/attention.fab`, `src/transformer.fab`, `src/shape.fab`, `src/tensor.fab`, `src/dtype.fab`, `src/data.fab`, `src/gradus.fab` + co-located `.proba` |
| done_when | Zero ledger-Latin tokens in those files; with U2–U4 landed, `"$FABER_BIN" check "$ROOT"` (whole gradus package) is green |
| depends_on | U1 |
| sanity | per-module `faber check` (absolute path); package check at close of the last wave |
| non_goals | Consumers (U6); `gradus:gradus` facade genus growth (rename only) |
| risk | medium — breadth over 26 files, shallow per file |
| integrable | no — transitional until U6 |

### U6 — consumer chase

| Field | Value |
| --- | --- |
| id | `no-latin-U6` (ledger row 6) |
| outcome | Every consumer of the renamed surface uses the new names: exempla, tests, scripta `.fab`, fixture generators |
| write_scope | `exempla/**/*.fab`, `tests/*.fab`, `scripta/*.fab` (`check-compile.fab`, `check-factory-goal-status.fab`), `fixtures/*/gen_fixture.fab` |
| done_when | `"$FABER_BIN" check "$ROOT"` green **and** `"$FABER_BIN" check "$ROOT/exempla/<slug>"` green for every exemplum whose files were touched; no old-name references repo-wide (`grep` for ledger old names returns only `docs/archived/` and this goal dir) |
| depends_on | U2, U3, U4, U5 |
| sanity | package-scoped `faber check` per touched consumer package |
| non_goals | Sibling repos (`examples/training/*`, Inferentia docs — recorded follow-up); historical factory docs under `docs/factory/production-ml-library/`, `docs/archived/` |
| risk | medium-high — largest grep surface; fixture regen coupling from U3 |
| integrable | yes — restores whole-package compile coherence |

### U7 — docs regeneration

| Field | Value |
| --- | --- |
| id | `no-latin-U7` (ledger row 7, docs half of the split) |
| outcome | Public docs reflect the final English surface |
| write_scope | `docs/api-reference.md`, `docs/module-map.md`, `docs/compatibility-policy.md` |
| done_when | `api-reference.md` documents every public fn of every live module under its section — absorbing **all** currently-undocumented symbols (97 coverage failures at check time, not the goal's stale 47); `module-map.md` verified against the (unchanged) module list; `compatibility-policy.md` records the clean break |
| depends_on | U6 |
| sanity | `./scripta/inventory-public-symbols` coverage section passes against the regenerated reference (this check targets exactly this unit's surface; the count re-baseline itself is U8's) |
| non_goals | Gate code (U8); historical factory records |
| risk | low-medium — mechanical regeneration over a large symbol set |
| integrable | yes |

### U8 — enforcement gates

| Field | Value |
| --- | --- |
| id | `no-latin-U8` (ledger row 7, gates half of the split) |
| outcome | Enforcement matches the new surface: `check-source` S2 stale-name guard replaced by a no-Latin guard (identifiers, comments, owned strings) keyed to the U1 retained-exception list; `inventory-public-symbols` re-baselined to live counts |
| write_scope | `scripta/check-source`, `scripta/inventory-public-symbols` |
| done_when | No-Latin guard passes on the converted tree and fails on a probe Latin identifier in each guarded class (self-test receipt); inventory asserts the live declaration total and exits 0 against U7's regenerated api-reference |
| depends_on | U6, U7 |
| sanity | `./scripta/check-source` on the converted tree; probe-file failure demo |
| non_goals | New census tooling beyond the guard; docs prose |
| risk | medium — guard must not false-positive on retained terms, external-format keys, or `gradus:` coordinates |
| integrable | yes |

## 5. Integration / merge gate

Units 2–5 are transitional (`integrable: no`): each leaves exempla/tests
referencing old names, so none may be the final state of `main`. U6 is the
restoring unit. Direct-mode adaptation (this repo develops on `main`): Mind
either sequences U2–U6 as one parked commit train on `main` or routes the
train through a `worktrees/<lane>/` packet; the closeout below is the
aggregate gate either way. Landing order inside the train must respect
within-wave caller order (gguf → gguf_manifest → qwen35moe in U2;
tokenizer before its U4 callers).

## 6. Lane-owned validation (closeout — named once, not per child)

Per `GOAL.md` Validation, all green on `main` after U8:

1. `./scripta/check-source` — new no-Latin guard.
2. `./scripta/check-compile` — full library + exempla set.
3. `./scripta/inventory-public-symbols` — green, re-baselined, full coverage.
4. Census re-run: zero Latin word-tokens in code positions across
   `src/**/*.fab{,.proba}`, `exempla/**`, `tests/`, `scripta/`; comments and
   owned strings clean outside the retained-exception list.
5. Landing commit + `docs/compatibility-policy.md` break record.

## 7. Open questions for Mind

1. **U7/U8 split acceptance** — ledger row 7 lowered as two units (docs /
   gates). If Mind wants the locked 7-unit count preserved literally, run
   U7+U8 as one Hand; scopes above union cleanly.
2. **Wire-literal pin (goal OQ3)** — default convert + regen fixtures (U3).
   If the operator pins wire stability, U3 narrows to internal names and the
   pin is recorded in the ledger and compatibility policy.
3. **Guard placement (goal OQ5)** — default fold into `check-source`
   (U8 as specced); a separate `check-no-latin` script only if the operator
   prefers an isolated gate.
4. **Header-comment Latin (goal OQ1)** — default convert (live source is the
   surface); already inside every wave unit's write scope.
