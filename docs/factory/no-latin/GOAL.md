# GOAL: no-latin — finish the English conversion of Gradus

**Status**: active — REOPENED 2026-08-20 per block_ship audit d83e1804: src conversion verified (0 violations, wire holds honored); REMAINING: exempla + tests + scripta/*.fab conversion, guard root restoration, compatibility-policy correction, residue cleanup. Wave-1 receipts stand.
**Created**: 2026-08-19
**Campaign:** `—` (standalone; supersedes the retained-Latin carve-outs of archived `docs/archived/english-locale/`)
**Source:** operator ruling 2026-08-19 — "no Latin period"; the S2 campaign narrowed "English library" to "English keywords + member ledger" and archived itself done with Latin still live
**Repos:** gradus
**Related:** `docs/archived/english-locale/` (S1/S2 history), `docs/compatibility-policy.md` (pre-1.0 clean break), `docs/api-reference.md`, `scripta/check-source`, `scripta/inventory-public-symbols`

---

## Invariant

Gradus is an English library. No Latin anywhere in owned surfaces — no Latin
type names, function names, field names, error-variant names, parameters,
locals, import aliases, comments, or diagnostic strings. The only retained
Latin is the proper noun `gradus` (package name, `gradus:*` import
coordinates, the `gradus:gradus` facade module) and external-format keys we
do not own (GGUF/safetensors spec strings). Module names are already
English — verified, not assumed.

## Problem

The 2026-08-15→17 `english-locale` campaign converted keywords (S1) and a
member-ledger subset of identifiers (S2), then archived itself as done by
redefining the remainder as "retained by named ledger class." The operator
ruling rejects that narrowing: the libraries were supposed to *become
English*, not to acquire English keywords over Latin bodies.

Measured on `main` 2026-08-19 (census receipts `/tmp/gradus-latin-census2.py`,
operator session):

| Layer | Remaining Latin | Where |
| --- | ---: | --- |
| Public fns | 23 | `model/gguf_manifest` (10), `model/qwen35moe` (6), `model/safetensors`, `model/artifact`, `decode` (2), `gradient` (2), `tokenizer` |
| Public class fields | 30 | `model/qwen35moe` (20), `model/capsule` (2), `model/gguf_manifest` (4), `tokenizer`, `decode`, `model/tensor_view`, `model/dense_llama` |
| Public types | 1 | `GeneratioError` beside English `GenerationConfig`/`GenerationCursor` |
| Error variants (union cases) | ~181 of ~267 | every module; S2 deliberately retained "error-variant identities" |
| Parameters / locals / import aliases | bulk of ~5,616 Latin code word-tokens | all modules; S2's "member-scoped parameter policy" excluded them |
| Comments | ~1,700 Latin word-hits | all modules; deferred to a "later pass" that never ran |
| Owned strings / diagnostics | 89 distinct literals | e.g. `…exceeds the numerus carrier`, `dtype/<schema>/<nomen>`, tokenizer category `aliud` |

Named offenders (code positions, live, called by 8 exempla):
`textum` `textorum` `numerum` `numerorum` `boleanum` `longitudo_listae`
`inveni_tensorem` `limes_payloadis` `read_fragmentum` `congela` `referantia`
`tensores_canonici` `causa_*` `admittas` `identitas` `decodere_datum`
`projectio_bias` `gradientes_simple_loss` `gradientes_masked_mean` `est_eog`
`GeneratioError` + import aliases `manifestum` (13 files), `capsula` (5 files).

Gate state compounds the problem: `check-source` is green but structurally
blind to this debt (its S2 guard checks a closed pre-S2 ledger, so any Latin
*not* in that list passes), and `inventory-public-symbols` is already red
for an unrelated reason (750 baseline vs 979 live declarations; 47 typed-
surface symbols undocumented in `docs/api-reference.md`). The enforcement
that should have caught this drift does not exist.

## Proposal

One clean-break conversion wave set on `main`, direct mode, superseding the
S2 carve-outs (member-scoped parameter policy, error-variant retention,
comment/string deferral). Order: lock the full rename ledger first, then
module-family waves (epicenter first), then the consumer chase, then docs +
gates so the no-Latin guard lands with a clean tree and the inventory gate
leaves green.

Naming rules:

| Class | Rule | Examples |
| --- | --- | --- |
| Package / facade | **Retained** (proper noun) | `gradus`, `gradus:*` coordinates |
| Module names | **Unchanged** (already English) | `model/gguf_manifest`, `tokenizer`, … |
| Types, fns, fields, variants | Rename to English | `GeneratioError`→`GenerationError`, `congela`→`freeze`, `est_eog`→`is_eog` |
| Parameters, locals, aliases | Rename to English | `manifestum` alias→`manifest`, `clavis`→`key`, `nomen`→`name` |
| Comments, owned diagnostics | Rewrite in English | `numerus carrier`→`numeric carrier` |
| Owned wire literals | Convert; regenerate fixtures | tokenizer category `aliud`→its English value |
| External-format keys | **Retained** | `general.architecture`, safetensors/GGUF spec keys |
| Established technical terms | **Retained** | `signum`, `silu`, `matmul`, `eog`, `fim`, `bpe`, dtype/model tokens (`llama`, `qwen35moe`, `gguf`, `ggml`, `smollm2`, `f32`…) |
| Reserved-name escapes | Inherit `docs/archived/english-locale/rename-seed.md` | `valor`→`payload` never `value`; `quantitas`→`numel` never `size` |

Precedents to reuse: the seed map and family ledgers in
`docs/archived/english-locale/` (correct targets, incomplete application);
the S2 probe method (`faber check` per first-file, exact identifier-boundary
replacements, no HIR re-emission).

### Non-goals

- No package rename (`gradus` stays), no module renames, no radix/compiler
  changes, no locale-pack rows or `[[library_members]]` translation layer.
- No shims, aliases, or deprecation windows (pre-1.0 clean break;
  compatibility policy records it).
- No comment/prose rewrite of historical factory records under
  `docs/factory/production-ml-library/` or `docs/archived/` — history is
  evidence of what happened, not the library surface.
- No sibling-repo migration (`examples/training/*`, Inferentia docs) —
  recorded follow-up; the S3 debt from the prior campaign stays named there.
- No product/API changes beyond naming; renames are behavior-preserving
  except owned wire literals, which change and regenerate their fixtures.

## Units (lowering sketch — refine via `$delivery`)

| Unit | Scope | Depends on | Hand evidence |
| --- | --- | --- | --- |
| 1 | Lock the ledger: exhaustive old→new map for every remaining Latin identifier (fns, fields, types, variants, params, locals, aliases) + the retained-exception list, as `rename-ledger.md` in this goal dir | — | none |
| 2 | Model family wave: `model/gguf_manifest`, `model/qwen35moe`, `model/safetensors`, `model/artifact`, `model/capsule`, `model/tensor_payload`, `model/tensor_view`, `model/dense*`, `model/dequant`, `model/gguf` + co-located `.proba` (epicenter: ~60% of remaining tokens) | 1 | none |
| 3 | Tokenizer + calibration wave: `tokenizer`, `calibration` + proofs; owned category wire value conversion + fixture regen | 1 | none |
| 4 | Inference + gradient + nn wave: `decode`, `generation`, `cache`, `sampling`, `gradient`, `nn`, `math` leftovers | 1 | none |
| 5 | Remaining-modules sweep: `train`, `optimize`, `parameter`, `serialize`, `loss`, `metrics`, `attention`, `transformer`, `shape`, `tensor`, `dtype`, `data`, `gradus` facade — variants, params, locals, comments, strings | 1 | none |
| 6 | Consumer chase: `exempla/**`, `tests/`, `scripta/*.fab`, `fixtures/*/gen_fixture.fab` | 2–5 | none |
| 7 | Docs + gates: regenerate `docs/api-reference.md` for all live symbols (absorbs the 47 undocumented), `docs/module-map.md`, compatibility-policy break record, `check-source` no-Latin guard replacing the closed S2 ledger, `inventory-public-symbols` re-baseline to live counts | 2–6 | none |

Each wave unit: `faber check` per first file, exact identifier-boundary
replacement, `./scripta/check-compile` green at unit close.

## Validation

Closeout gate, all green on `main`:

- `./scripta/check-source` — with the new no-Latin guard (identifiers,
  comments, owned strings; retained-exception list explicit).
- `./scripta/check-compile` — full library + exempla set.
- `./scripta/inventory-public-symbols` — green, re-baselined to live counts,
  full api-reference coverage.
- Census re-run: zero Latin word-tokens in code positions across
  `src/**/*.fab{,.proba}`, `exempla/**`, `tests/`, `scripta/`; comments and
  owned strings contain no Latin outside the retained-exception list.
- Landing commit + `docs/compatibility-policy.md` record the clean break.

## Ledger

| Unit | Status | Hand | Receipt | Notes |
| --- | --- | --- | --- | --- |
| 1 | pending | — | — | rename-ledger.md lock |
| 2 | pending | — | — | model family wave |
| 3 | pending | — | — | tokenizer + calibration wave |
| 4 | pending | — | — | inference/gradient/nn wave |
| 5 | pending | — | — | remaining-modules sweep |
| 6 | pending | — | — | exempla/tests/scripta/fixtures chase |
| 7 | pending | — | — | docs + no-Latin gate + inventory re-baseline |

## Open questions

1. **Comment Latin in live-source headers** — default: convert (live source
   is the library surface; only historical factory docs are exempt).
2. **`signum`** — standard mathematical term in English libraries (Rust
   `f64::signum`, Java `Math.signum`); default: retain as technical term.
3. **Owned wire-literal changes ripple** — tokenizer category `aliud` and any
   Latin serialize keys change under clean break; default: convert and
   regenerate fixtures in unit 3/6. Operator may pin wire stability instead.
4. **Sibling consumers (`examples/training/*`, Inferentia)** — default:
   outside this goal, recorded follow-up carrying the prior campaign's open
   S3 debt.
5. **Whether the no-Latin guard lives in `check-source` or a new
   `check-no-latin` script** — default: fold into `check-source`, replacing
   the S2 stale-name guard.
