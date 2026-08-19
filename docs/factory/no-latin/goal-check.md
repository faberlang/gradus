# Goal check — no-latin (P2 receipt)

**Checked**: 2026-08-19, planner (wave gate: goal-check + P3 lowering, single assignment)
**Goal**: `docs/factory/no-latin/GOAL.md` (gol_c647e16d32149ae3, status planned, ledger locked 7 units)
**Tree**: gradus `main` @ `6b3a6c7` (clean)
**Verdict**: **READY** — for delivery lowering (done in this pass: `delivery.md`, 8 units)
**Consumer**: delivery (Mind → Hands)

## Method

Re-measured every quantitative claim with a corrected census
(`/tmp/gradus-latin-census3.py`; lexicon inherited from the operator-session
`/tmp/gradus-latin-census2.py`). The prior script had three extraction
defects that matter for receipts: its class-field regex captured the **type**
column (faber field syntax is `Type name`), its import-alias regex required
quote characters its own comment/string stripper blanks out (counted 0
aliases while `manifestum` aliases are live), and it had no union-case
counting at all. Counts below are from the corrected extraction.

## Verified facts (claim → live receipt)

| GOAL.md claim | Live receipt | Verdict |
| --- | --- | --- |
| 23 public Latin fns, module spread gguf_manifest 10 / qwen35moe 6 / decode 2 / gradient 2 / safetensors 1 / artifact 1 / tokenizer 1 | exact match; census2 flags 30, minus 7 retained-technical-term-only names (`signum`, `silu`, `eog*`) = 23 | ✅ |
| 30 public Latin class fields | corrected count **34** rename-relevant: qwen35moe 20, gguf_manifest 5 (doc: 4), safetensors 4 (**missed in doc**), tokenizer 2 (doc: 1), capsule 1 (doc: 2), decode 0 (doc: 1), tensor_view 1, dense_llama 1 | ≈ corrected |
| ~181 of ~267 Latin error variants | **201 of 303** per-module case occurrences (95 of 163 distinct names); every module represented | ≈ confirmed, dominant layer |
| 1 public Latin type `GeneratioError` | exact (`src/generation.fab`) | ✅ |
| Latin import aliases `manifestum`/`capsula` | src: `manifestum` ×8 files, `capsula` ×2, plus `tokenizator`, `parametrum` (doc's 13/5 spread presumably repo-wide incl. exempla) | ✅ direction |
| ~1,700 comment Latin word-hits | strict lexicon count **~737** in `src` comments (doc figure likely counted retained tokens/`gradus:` mentions) | ≈ direction |
| 89 distinct owned Latin strings | strict count **10 distinct** literals in `src`; named examples live (tokenizer category `aliud`, `nomen`-bearing diagnostics) | magnitude corrected |
| `check-source` green but structurally blind | exit 0; S2 guard comment confirms closed pre-S2 ledger | ✅ |
| `inventory-public-symbols` red, 750 vs 979 | exit 1: "tracked total expected 750, got 979"; coverage-failed lines now **97** (doc said 47 — debt grew) | ✅ (count grew) |
| Module names already English | `src/` + `src/model/` listing: all English/technical | ✅ |
| Named offenders live, called by exempla | all 23 fn names + `GeneratioError` + aliases present in census receipts | ✅ |

## Key points

- No scope-level gap: every corrected number lands inside surfaces the locked
  7-unit ledger already owns (safetensors fields → unit 2; the 97-vs-47
  undocumented growth → unit 7 docs regen, which already says "all live
  symbols").
- The goal's per-wave "check-compile green at unit close" prose conflicts
  with its own unit graph: units 2–5 rename symbols that `exempla/` still
  call, so full `check-compile` cannot be green until unit 6. Delivery
  lowering resolves this: package/module-scoped `faber check` per unit,
  full gates at closeout (lane-owned).
- Sanity-tooling ground truth: gradus has **no cargo** (assignment template
  said `cargo test -p` — not applicable). Narrow executable check is
  `faber check` on an absolute module path or the package root, with
  `FABER_LIBRARY_HOME=<workspace>` and `FABER_BIN=<ws>/radix/target/debug/faber`
  (per `scripta/check-compile`). Relative single-file paths fail with
  `cannot read ''` — use absolute paths.

## Blocking gaps

None.

## Recommended next step

Delivery lowering — completed in the same assignment per task instruction:
`docs/factory/no-latin/delivery.md` (8 units; ledger row 7 split into gates +
docs, permitted by the lock rule "splitting only where a unit is genuinely
two logical changes").
