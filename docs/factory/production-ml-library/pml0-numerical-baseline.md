# PML0 Numerical + Claim-Drift Baseline — gradus

**Unit**: PML0-U6 (numerical + claim-drift baseline)
**Date**: 2026-08-08 (grep/ls/find only; no cargo anywhere)
**Version stamps**: gradus live HEAD `c02ec5773306303abdd104a7ac466d8425bc0bcf`
(measured at baseline time; supersedes the U1 snapshot stamp `d7e85aa` which no
longer heads `main` after U2/U5/U7 landed — see `pml0-source-snapshot.md`
drift-replacement rule).
**Consumed by**: PML0-U10 (contract assembly) and later PML phases; the drift
dispositions below are recorded decisions, executed by their named owners.

## Measured, not claimed

Every number in this document was **measured from the live tree** with the
commands printed inline, on 2026-08-08 — not copied from the delivery spec,
not remembered from a prior session, and not asserted from documentation.
Where a documentation claim disagrees with a measurement, the **measurement
wins** and the disagreement is recorded as a claim drift (§Drifts). This
document carries no claim that the library is numerically verified — the
coverage table below shows it is not (zero co-located `.proba` files).

## Module coverage table (functions vs co-located `.proba`)

Measurement: `grep -c '^functio' src/*.fab` per module (declaration lines
only, comments excluded) and `find . -name '*.proba' -not -path './worktrees/*'`.

| Module | `functio` declarations | Co-located `.proba` | Numerical coverage |
| --- | --- | --- | --- |
| attention | 1 | 0 | none |
| data | 0 | 0 | n/a (stub) |
| gradient | 2 | 0 | none |
| gradus (facade) | 0 | 0 | n/a (facade, no genera) |
| loss | 3 | 0 | none |
| math | 0 | 0 | n/a (stub) |
| nn | 6 | 0 | none |
| optimize | 2 | 0 | none |
| tensor | 0 | 0 | n/a (stub) |
| train | 4 | 0 | none |
| transformer | 3 | 0 | none |
| **TOTAL** | **21** | **0** | **0/21 functions have a co-located numerical test** |

Per-module declaration counts match the PML0-U2 inventory baseline exactly
(`attention 1, gradient 2, loss 3, nn 6, optimize 2, train 4, transformer 3;
math/tensor/data/gradus = 0`; total 21). The 17 fixed-shape functions
(`*_2x2/_4x4/_2x8`) verified by U3 are all inside the same zero-coverage set.

### Numerical baseline statement

- **Zero** co-located `.proba` files exist in the tree (measurement below).
- Therefore the current numerical baseline is: **no gradus function has a
  co-located numerical proof**, despite the `AGENTS.md` rule requiring them
  (Drift D4).
- The library's only recorded numerical evidence is external to `gradus/src`:
  the gradient-seam FD comparison (~1e-11, per README §Seam status) and the
  `radix`-side autograd finite-difference exempla — neither is a co-located
  `src/**/*.proba` test and neither covers the 21 public functions here.

```bash
$ find . -name '*.proba' -not -path './worktrees/*' | wc -l
0
$ grep -c '^functio' src/*.fab   # per-module counts, totalled by awk
# totals to 21; see table above
```

## Drifts

Four claim drifts were verified live on 2026-08-08 against the PML0 delivery
spec baseline. Each entry records the claim as written, the measured evidence,
the verification command, and the correction disposition.

### D1 — README lists attention/transformer as "Planned" while the tree records a shipped BERT-tiny slice

- **Claim**: `README.md:23` — "Attention / transformer | **Planned** — nanoGPT
  forcing function"; `README.md:97` — "Attention, transformer | **Horizon 5–6**".
- **Measured evidence**: `src/gradus.fab:31-36` records "the BERT-tiny surface
  is shipped — gradus:attention.scaled_dot_product_2x8, gradus:transformer
  bert_tiny_block_2x8 / attention_block_2x8 / ffn_block_2x8, gradus:nn
  linear_2x8 / layernorm_2x8 / gelu_2x8, gradus:loss.mse_2x8, and
  gradus:train.train_step_bert (18-trainable BERT-tiny set)". The declarations
  exist in the tree: `src/attention.fab:38` (`scaled_dot_product_2x8`),
  `src/transformer.fab:38/74/100` (`attention_block_2x8`, `ffn_block_2x8`,
  `bert_tiny_block_2x8`), `src/nn.fab` (`linear_2x8`, `layernorm_2x8`,
  `gelu_2x8`), `src/loss.fab:4` (`mse_2x8`), `src/train.fab:108/179`
  (`train_step_bert_linear`, `train_step_bert_layernorm`). That is a shipped
  static-shape BERT-tiny slice, not "Planned".
- **Verification**: `grep -n 'functio.*2x8\|_2x8' src/attention.fab src/transformer.fab src/train.fab` and `sed -n '31,36p' src/gradus.fab`.
- **Correction disposition**: the README Status table row for
  "Attention / transformer" must be moved from `Planned` to
  `Shipped (S6-G1, static-shape BERT-tiny fragment)` — or annotated that only
  the static-shape BERT-tiny slice ships while the general transformer/attention
  surface remains planned (accurate wording, since only fixed shapes exist).
  Owner: gradus repo maintainer at the next README touch (natural point is the
  PML0 contract assembly, U10). No README edit is performed in this unit
  (write scope is this baseline file only).

### D2 — `AGENTS.md` references `corpus/nanogpt-shakespeare` but no `corpus/` exists

- **Claim**: `AGENTS.md:46-50` — "`corpus/` holds training demos … The primary
  forcing-function demo is `corpus/nanogpt-shakespeare/` … Details and per-demo
  commands: `corpus/README.md`."
- **Measured evidence**: `ls -d corpus` fails — no `corpus/` directory exists
  at the gradus root. No `nanogpt-shakespeare` demo, no `corpus/README.md`.
- **Verification**: `ls -d corpus` (exit non-zero); `find . -maxdepth 1 -name corpus`.
- **Correction disposition**: the `corpus/` section of `AGENTS.md` is
  aspirational. It must be marked as a future home (e.g., "reserved for
  training demos; none exist yet") until a real demo lands, so readers do not
  look for a directory that does not exist. The nanoGPT forcing function is
  recorded in `README.md` as Planned (Horizon 7), so the AGENTS.md claim
  describes intended state, not current state. Owner: gradus repo maintainer,
  same touch as D1/D3. No directory is created in this unit (PML0 is
  discovery-only; no product changes — `gradus/corpus/**` is a forbidden path
  in the delivery spec).

### D3 — `AGENTS.md` references `docs/module-map.md` + `docs/api-shape-policy.md` but `docs/` holds only `factory/`

- **Claim**: `AGENTS.md:40-41` — "Full map: [`docs/module-map.md`](docs/module-map.md). API shape: [`docs/api-shape-policy.md`](docs/api-shape-policy.md)."
- **Measured evidence**: `ls docs/` returns a single entry, `factory/`. Neither
  `docs/module-map.md` nor `docs/api-shape-policy.md` exists. The map link's
  only resolvable sibling is `docs/factory/gradus-ml-foundation/GOAL.md`
  (linked on the same line).
- **Verification**: `ls docs/`; `ls docs/module-map.md docs/api-shape-policy.md` (both fail).
- **Correction disposition**: either (a) create the two referenced docs, or
  (b) reword `AGENTS.md` to link only existing artifacts. These documents are
  PML0-adjacent but outside this unit's write scope; the module map content
  is substantively produced by U4 (`pml0-module-dag.md`), so the natural
  correction is to land `docs/module-map.md` as a thin entrypoint after U4 and
  reword/land `api-shape-policy.md` under the PML1 API-shape decision (per
  delivery open question "first production tensor API shape posture"). Until
  then the AGENTS.md links dangle. Owner: gradus repo maintainer; reword at
  the same touch as D1/D2.

### D4 — the co-located `src/**/*.proba` rule has zero `.proba` files

- **Claim**: `AGENTS.md:58` — "Keep package tests as co-located
  `src/**/*.proba` (`name.fab` + `name.proba`)." (Rule; implies the pattern is
  the standing test convention for `src/**`.)
- **Measured evidence**: `find . -name '*.proba' -not -path './worktrees/*'`
  returns **0** matches — no module in the tree has a co-located `.proba` test.
- **Verification**: the `find` command above (count 0); `ls src/*.proba` fails.
- **Correction disposition**: the rule is currently unfulfilled by every
  module. Two options, both recorded for the maintainer: (a) relax the rule to
  acknowledge zero current fixtures and defer `name.fab`+`name.proba` pairing
  to the first post-PML0 numerical work (PML2+ numerical fixture set), or (b)
  begin landing co-located `.proba` fixtures for the 21 declared functions
  (which requires the numerical fixture machinery — a PML-phase concern, not
  PML0, per the delivery's no-implementation stance). Owner: gradus repo
  maintainer; the coverage table in this doc is the reference for which
  modules have zero coverage.

## Assertions (hold)

- Total `functio` declarations in `src/*.fab` == **21**, per-module counts
  match the U2 baseline (`attention 1, gradient 2, loss 3, nn 6, optimize 2,
  train 4, transformer 3; math/tensor/data/gradus 0`).
- `.proba` files in tree == **0**; the doc's coverage table shows 0 for every
  module and states "0/21 functions have a co-located numerical test".
- All four drifts D1–D4 are verified live and each has a correction disposition
  naming the corrected target state and the owner.
- This document carries the "measured, not claimed" header (§Measured, not
  claimed) and states the zero-coverage baseline explicitly.

## Validation

```bash
cd /Users/ianzepp/work/faberlang/gradus
./scripta/check-source && ./scripta/check-compile     # exit 0; one closeout run
find . -name '*.proba' -not -path './worktrees/*' | wc -l   # 0, matches doc
git diff --check
```

Outcome: `./scripta/check-source` and `./scripta/check-compile` both exit 0
(check-compile runs `faber check`, no cargo); the `.proba` find count is 0 as
recorded in the coverage table; `git diff --check` clean.
