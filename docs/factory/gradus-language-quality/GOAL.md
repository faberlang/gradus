# GOAL: gradus-language-quality — canonical language idiom + public presentability

**Status**: active — 17 units (1 decision-pending, 1 externally sequenced); see Ledger
**Created**: 2026-08-20
**Campaign:** `—` (standalone; operator rule: individual tracking, no campaign)
**Source:** two operator-ordered audits, 2026-08-20 — idiom audit (Vivi mail `57cb4713`, task `f6f4068b`, verdict residual) + presentability audit (Vivi mail `7d54686c`, task `bdbbb2f9`, verdict block_ship); lowered by planner task `59369675`
**Repos:** gradus (primary); one unit writes `faber/docs/EBNF.md` in the sibling faber repo
**Base:** gradus `main` `f70f02f` (audit heads were `70c62dd`; the two commits since — U8 guard `65bb0c8`/`03359eb` and the no-latin archive `f70f02f` — touch none of the audited defects; planner re-verified, see Ground Truth)

---

## Summary

Gradus compiles and behaves, but its source drifts from the EBNF canonical idiom
the language already ships (glyph tensor products, `requirit … iace` guards, `§`
string templates, `itera ab` range loops, `fixum _` binding holes), and its
public surface (README, exempla prose, packaging) still names renamed-away
symbols and ships without a license. This goal converts the audited drift to
canonical idiom and brings the public surface to the featured-repo bar, in 17
individually tracked Hand units.

## Problem

Idiom drift (audit `57cb4713`, all counts audit-verified per-site or
sampled-regex; planner re-spot-checked at `f70f02f`):

- **75 glyph-eligible method sites** on static core tensors:
  `.matmul(` → `·` (14), `.multiply(` → `⊙` (33), `.subtract(` → `-` (28).
  Epicenter `src/transformer.fab:63-100`; same functions already use glyph `+`
  beside method calls (mixed idiom, `src/gradus.fab:239-246`).
- **887 single-throw guard bodies** (`if cond { throw variant … }` with the
  whole block one throw) that are the exact `requirit cond iace err` desugar
  target; 149 are direct positive-polarity maps, 28 are double-negation guards
  whose conversion deletes both the block and the double-not.
- **~110 hole-eligible typed bindings** (`const tensor<…> x ← <already-typed
  expr>`) vs exactly one hole use repo-wide (`src/sampling.fab:343`); 5 `← vacua`
  bindings must keep annotations.
- **140 string-concat sites** vs zero `§` template uses; **75 while-i loops**
  that close with `i ← i + 1` (for-range candidates).
- Latin residue the landed U8 guard's closed lexicon misses: live public
  `scaled_dot_product_staticum` (`src/attention.fab:77`, republished at
  `docs/api-reference.md:36`), `addita_bias` in live header comments
  (`src/train.fab:22`, `src/transformer.fab:14,67`, `src/gradus.fab:48`),
  `conversio` (`src/shape.fab:14`).
- Manual endian/IEEE helper families (9 helpers, BE-by-multiplication at
  `src/model/qwen35moe.fab:174`) — **blocked on language gaps, not units** (see
  Out of scope).

Presentability (audit `7d54686c`, verdict block_ship):

- README names five renamed-away symbols (`Tabula`, `accuratezza`, `Metricum`,
  `praevideo`, `vincula`), teaches dead `importa ex … privata` syntax
  (`README.md:195-199`), and lists two dead paths (`examples/…` `:185`, `corpus/`
  `:226` — both absent from the tree).
- 12 of 23 exempla READMEs + 4 mains carry Latin prose/helpers around
  English call sites (67 grep hits at `f70f02f`).
- No LICENSE file; `docs/release-checklist.md` has no license row.
- Public-audience gaps: no install/quickstart path, campaign jargon on the
  first-time path, residual docs Latin (`docs/regression-corpus.md`,
  `docs/diagnostics.md:314,344`, `docs/numeric-tolerances.md:28`), packaging
  hygiene (tracked bench/golden receipts, no internal markers, missing
  `exempla/nn-bridge/README.md`).
- faber-side: `faber/docs/EBNF.md` is stale in three places (requirit/adfirma
  particle "proposed (not shipped)" prose vs the shipped parser; comparison
  productions `<`/`>` vs canonical `≺`/`≻`; dead `docs/design/*-intrinsics.md`
  references at `EBNF.md:1087-1095`).

## Goals

- Convert all 75 static-tensor glyph sites; carrier `math.matmul` calls stay
  methods (audit exclusion).
- Convert the 887 guard sites to `requirit … iace` (three file-disjoint waves),
  removing the 28 double-not guards.
- Convert ~110 eligible bindings to `fixum _` holes **after** the in-flight
  radix size-param type-args repair and parser fix settle.
- Convert 140 string-concats to `§` template calls and 75 while-i loops to
  `itera ab` (loop-only indices only).
- Remove the Latin residue (`scaled_dot_product_staticum` rename + header
  comments) and extend the U8 lexicon so the guard holds the converted state.
- Bring README, exempla, residual docs, and packaging to the featured-repo bar;
  land the LICENSE decision file once the operator rules.
- Fix the three EBNF staleness items in the faber repo.

## Non-goals

- **No language/compiler changes from gradus units.** Grammar gaps route to the
  radix-side findings list below; no gradus unit works around a missing
  capability.
- No removal of `train.fab` fill-tensor scaffolding (`src/train.fab:64-66` and
  parallels) — tensor↔scalar broadcast is gap 5; keep same-shape `⊙` with fills.
- No rewrite of the ~19-file error-message-string remap wall (SEM001 root) —
  gap 3; local rewriting cannot fix it.
- No endian adoption or helper centralization until gaps 1-2 land (default:
  defer; see Open Questions).
- No sentinel `-1` conversion by default (reference-parity reason stated in
  `src/model/dense_qwen2.fab:84-95`).
- No corpus/ (absent) or `examples/training/*` (sibling repo) work; no rewrite
  of historical `docs/factory/` / `docs/archived/` records.
- No GO stamp; READY is readiness, not approval. No campaign formation.

### Out of scope — radix-side findings list (route via Mind, not gradus units)

Recorded 2026-08-20 from audit `57cb4713` §GRAMMAR GAPS; re-verify staleness
before each routing decision:

1. **Endian pack** convert (`n ↦ octeti<N, Be|Le>`) — proposed only
   (EBNF:712-715); `src/serialize.fab:284-307` is the standing need.
2. **Endian unpack window mismatch** — shipped form wants `octeti` windows;
   gradus buffers are `list<int<u8>>` (EBNF:866-869 recommends lista for
   internal work). The two canonical forms do not compose.
3. **Cross-module variant matching (SEM001)** or an error-channel map/coerce
   operator — would delete the ~19-file message-string remap wall including the
   prefix-slice hacks at `src/tokenizer.fab:856,1976`.
4. **Float bitcast** (`fractus<f32> ↔ numerus<u32>`) — dequant/qwen35moe
   hand-assemble IEEE-754 fields with shifts+mod (4 functions).
5. **Tensor↔scalar glyph broadcast semantics unstated** — `train.fab` builds
   fill tensors to multiply by the learning-rate scalar.
6. **Carrier glyph overloading** — the staged carrier genus
   (`src/tensor.fab:145`) cannot overload `·`/`⊙`; two parallel math
   vocabularies persist by design until ruled.
7. **Per-channel bias glyph for `+`** — `added_bias` exists because `+` is
   same-shape (S6-C2 contract, `src/transformer.fab:12-14`).

(EBNF staleness was gap 8; it is **not** routed to radix — the operator already
ruled it a faber-side docs defect and it is lowered as unit GLQ-17.)

## Ground Truth Researched

Planner verification at gradus `main` `f70f02f`, 2026-08-20:

- `grep -n 'staticum' src/attention.fab` → live at `:77` with rationale
  comments; absent from `scripta/check-source` lexicon (guard blind to it).
- `grep -nE 'Tabula|accuratezza|Metricum|praevideo|vincula|importa' README.md`
  → hits at `:30,:31,:32,:60,:78,:155,:157,:195-199` (audit exact).
- `ls LICENSE*` → absent. `ls corpus examples` → both absent (dead README paths).
- `grep -rn 'requirit' src/` → zero uses (all 887 sites are still si-throw
  form; `src/model/qwen35moe.fab:215-219` read as the canonical pre-image).
- `grep -rnE '<ledger names>' exempla/*/README.md` → 67 hits (audit census
  scale confirmed). `grep -rn '§(' src/` → zero. `while` counts:
  `src/tokenizer.fab` 38, `src/model/gguf_manifest.fab` 21 (audit scale).
- `scripta/check-source` U8 guard read in full: live lexicon-based word-token
  check; `staticum`/`addita`/`conversio` not in `LATIN_WORDS`; the guard
  comment cites `docs/archived/no-latin/rename-ledger.md`, the ledger's current
  location since no-latin re-opened (`f70f02f` archived it, `e2385b2` moved it
  back) — the comment path resolves, so GLQ-10 no longer fixes it.
- `../faber/docs/EBNF.md` exists (1198 lines); `:610-613` requirit/adfirma
  "proposed (not shipped)" particle prose and `:1087-1095` dead
  `docs/design/*-intrinsics.md` refs read directly.
- `worktrees/hand-13/` checked: on `main` at `f70f02f`, no WIP (idle lane).
- Both audit mails re-read in full (`57cb4713`, `7d54686c`); counts above are
  theirs, sampled-verified by the planner where cited.

## Reference Packet

Before editing, inspect:

- `docs/factory/gradus-language-quality/delivery.md`: the lowered unit graph
  (write scopes, done-when, deps, dispatch waves).
- Vivi mails `57cb4713` / `7d54686c`: per-file:line evidence for every class
  and batch (`vivi mail show <id> --project /Users/ianzepp/work/faberlang`).
- `docs/archived/no-latin/rename-ledger.md`: old→new name map for the exempla
  sweep and the retained-exception list the U8 guard loads.
- `../faber/docs/EBNF.md`: canonical forms — `:610-613` (requirit/adfirma),
  `:637-641` (glyph products), `:795-801` (§ templates), `:866-869` (byte
  policy), applied/binding holes.
- `scripta/check-source` (U8 lexicon), `scripta/check-compile`,
  `scripta/inventory-public-symbols`: the three lane gates.
- `../norma/README.md`, `../triga/README.md`: install-section and
  "Start here" shapes Batch D borrows.
- `AGENTS.md` (repo root): module/layout/proba rules every src unit must keep.

## Constraints And Invariants

- **Operator routing constraints (this task):** grammar gaps are not gradus
  units (findings list above); EBNF staleness is its own small faber-side docs
  unit; LICENSE is decision-pending — do not lower its content; glyphs are
  core-type-only (carrier calls stay methods); binding-hole units land **after**
  the radix size-param type-args repair and parser fix settle.
- Gradus stays self-contained: no Norma/sibling imports; no `@ externa` /
  `@ subsidia`; nested package dirs need ≥2 modules; proba mirrors co-located.
- Conversions are behavior-preserving: numerics, wire formats, and public
  signatures unchanged except the `scaled_dot_product_staticum` rename
  (pre-1.0 clean break; record in `docs/compatibility-policy.md`).
- `requirit` requires a `⇥ E`-declaring function — audit verified all 887
  sites already sit in one; any counterexample is a stop condition, not a
  workaround.
- Lane gates (`check-source`, `check-compile`, `inventory-public-symbols`)
  stay green at every landing; children carry no lane gates.

## Supporting Skills

- `faber` (implementing agents): canonical grammar/EBNF forms, locale surface,
  `faber check` usage history for safe conversions.
- `delivery` (Mind): routing the unit graph in `delivery.md`.
- `campaign`/`goal-check` (auditors): categories for post-wave audits.

## Implementation Shape

- Phase 1 (public P1 + epicenter): README rewrite, exempla sweep, Latin-residue
  rename + guard hold, glyph fragments (`transformer`/`attention` epicenter).
- Phase 2 (idiom waves): three `requirit` waves, train glyphs, string
  templates, for-range loops, train structural dedup, quickstart + residual
  docs + packaging hygiene + EBNF fix.
- Phase 3 (externally sequenced): binding holes after the radix repair
  settles; closeout census + inventory re-baseline.

## Release Posture

Decision: release prep only (pre-1.0 clean-break library).

- The `scaled_dot_product_staticum` rename is a public-API break: regenerate
  `docs/api-reference.md` and record it in `docs/compatibility-policy.md`.
- LICENSE (GLQ-13) is a publication blocker for the featured-repo bar; content
  awaits the operator's license choice plus disposition of `AGENTS.md` /
  `.polish-inspected.json` in a public checkout.
- No version bump machinery invoked by this goal; landing commits only.

## Exit Strategy

Decision: included.

- Every unit is a path-limited, revertible commit; glyph/requirit/template
  conversions are mechanical inverses per site.
- If a conversion class proves unsound mid-wave (e.g. a guard that must stay a
  block for control flow), that site is skipped and logged in the unit receipt;
  the wave does not block on it.
- LICENSE stays absent until the operator rules; the goal may close with GLQ-13
  explicitly parked as decision-pending (tracked, not silently dropped).

## Acceptance Criteria

- Glyph receiver greps (`.matmul(`, `.multiply(`, `.subtract(`) return zero on
  the converted files, with the 6 carrier `math.matmul(` free calls and the
  excluded method families (`.softmax`, `.gelu`, `.mean`, `.transpose`,
  `.layer_norm`, `.added_bias`, `.scale`, scalar `.abs`) untouched.
- Guard census: the audit's per-file single-throw counts drop to zero for pure
  guards (residuals only where a receipt logs a skip reason); `requirit … iace`
  present; the 28 double-not guards gone.
- Binding holes: ~110 sites converted; the 5 `← vacua` annotations kept;
  conversion landed only after the radix type-args repair settles.
- `§` templates: 140 src + proba mirrors converted; zero concat-built messages
  in converted files. Loops: 75 candidates converted where the index is
  loop-only (skips logged).
- Latin residue: `scaled_dot_product_staticum` renamed (or ledgered as a formal
  retained exception if the operator rules otherwise); `addita_bias` /
  `conversio` comments rewritten; U8 lexicon extended so `check-source` fails
  on recurrence; stale ledger path in the guard comment fixed.
- README: audit grep clean; live `import from` block; install + runnable
  example; dead paths gone. Exempla: Latin grep zero outside `target/` and
  retained exceptions. Residual docs + `nn-bridge` README done. Packaging
  hygiene receipts marked.
- EBNF: the three staleness items corrected in `faber/docs/EBNF.md`.
- Lane gates green on `main`: `./scripta/check-source`,
  `./scripta/check-compile`, `./scripta/inventory-public-symbols`.

## Validation

- `grep -nE 'Tabula|accuratezza|Metricum|praevideo|vincula|importa' README.md`
  → no hits (except historical prose the unit explicitly retains, if any).
- `grep -rnE 'vincula|materializa|praevideo|maxima|sors\b|damnum|accuratezza|Metricum|Tabula' exempla/*/README.md`
  → zero outside `target/` and retained exceptions. (Exempla `main.fab`
  identifiers are out of this goal's scope — owned by no-latin R1.)
- Per-wave: `grep -c 'requirit' src/<file>.fab` rises to the audit's converted
  count; `grep -n 'if not (not' src/math.fab` → zero.
- `./scripta/check-source` / `./scripta/check-compile` /
  `./scripta/inventory-public-symbols` → green (lane-owned, run by lint/test/
  merge lanes, not by child Hands).
- Manual flow: cold-reader README path — install per the new section, run the
  snippet, open the quickstart-recommended exemplum.
- Review check: each unit receipt logs site counts converted vs audit counts
  and any skipped sites with reasons.

## Open Questions

1. **LICENSE choice + root-file disposition (operator)** — gates GLQ-13
   (decision-pending). Also decides `AGENTS.md` / `.polish-inspected.json`
   disposition for a public checkout. Default: none; cannot default a legal
   choice.
2. **Sentinel `-1` count and conversion** — audit enumerates 2 fns
   (`src/model/safetensors.fab:957-965`, `src/model/dense_qwen2.fab:84-95`);
   the task digest says 3. Default: retain both (reference parity is a stated
   reason); re-count at dispatch and record the third if real.
3. **Endian helper centralization pre-gap** — audit marked it optional. Default
   defer: centralizing now double-touches files the gap landing will rewrite.
4. **`staticum` disposition** — default rename to English
   (`scaled_dot_product_static`); operator may instead ledger it as a retained
   exception. Rename is the audit's primary direction.
5. **Other operator-ruled grammar gaps** — the task carves out gaps "where the
   operator has already ruled"; only the EBNF-staleness ruling was evidenced.
   If Mind knows of another ruling (e.g. on broadcast or carrier glyphs), name
   it and the findings list re-routes that item.
6. **Compile sanity on .fab-converting units** — presentability audit inferred
   it from greps under a no-build order. Resolved: every implementation unit
   that converts `.fab` carries a unit-scoped `faber check` absolute-path
   sanity (named in its delivery.md row, not just a §6 lane gate). GLQ-12,
   now README-only after the boundary rewrite, carries no `.fab`; the exempla
   mains' compile check belongs to no-latin R1, which owns their renames.

## Stop Conditions

- Stop if any `requirit` conversion target lacks a `⇥ E`-declaring enclosing
  function (audit says zero such; a counterexample is a report, not a
  workaround).
- Stop if the radix size-param type-args repair or parser fix has not settled
  when GLQ-06 dispatches — park the unit, do not convert holes against a
  moving parser.
- Stop if a conversion would require a language capability that is not shipped
  (route the site to the findings list instead of inventing a workaround).
- Stop if LICENSE content or a root-file disposition decision is demanded
  mid-dispatch (operator gate; GLQ-13 stays parked).

## Ledger

| Unit | Outcome | Depends on | Status | Receipt |
| --- | --- | --- | --- | --- |
| GLQ-01 | Glyph conversion, fragment files (23/27 sites; 4 `.subtract` gated on radix tensor-minus need 9facfd36) | GLQ-10 | active (partial) | b9b23e3 → 623f1a3 |
| GLQ-02 | Glyph conversion, train.fab (48 sites) | GLQ-05 | pending | — |
| GLQ-03 | requirit wave 1 (241 sites) | — | done | 62d6742 → 185bcd0 |
| GLQ-04 | requirit wave 2 (263 sites, Δ0 vs audit) | GLQ-01 | done | 10c19ca → 194f4d7 |
| GLQ-05 | requirit wave 3 (383 + 28 double-not → 0; Δ0 vs audit B5) | GLQ-01 | done | 9dfb6d5 → 1195feb |
| GLQ-06 | Binding holes (~110 + mirrors) | GLQ-09 + external radix settle | pending | — |
| GLQ-07 | `§` string templates (140 + mirrors) | GLQ-03, GLQ-04, GLQ-05 | pending | — |
| GLQ-08 | for-range conversion (~75 loops) | GLQ-03, GLQ-04, GLQ-07 | pending | — |
| GLQ-09 | train.fab structural dedup | GLQ-02, GLQ-05 | pending | — |
| GLQ-10 | Latin residue + U8 guard hold | no-latin re-close (guard-hold sequencing) | done | 8c32b73 → 6214045 |
| GLQ-11 | README public rewrite | — | done | 0991e21 → 4be7895 |
| GLQ-12 | Exempla README stale-symbol sweep (prose only) | no-latin R1 re-close | done | a612d4f → 51e6d6a |
| GLQ-13 | LICENSE + root-file disposition | operator decision (pending) | decision-pending | — |
| GLQ-14 | Quickstart / examples tour / architecture | GLQ-11, GLQ-12 | pending | — |
| GLQ-15 | Residual docs Latin + cosmetics | GLQ-10 | pending | — |
| GLQ-16 | Packaging hygiene | — | done | b56d34a → ca3a8a4 |
| GLQ-17 | EBNF staleness ×3 (faber repo) | — | done | 5c191c4 → b38438d (residual: 3 private-only docs/design refs, thread 1338cb30) |

Unit detail (write scopes, done-when, risk): `delivery.md` beside this file.
