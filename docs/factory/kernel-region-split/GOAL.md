# GOAL: kernel-region-split — convert mixed Gradus functions into wrapper + device region

**Status**: planned — census landed (this commit); conversion units carded, none dispatched
**Created**: 2026-08-28
**Campaign:** `kernel-region-split`
**Source:** operator need `3b9e5796` (kernel-region-split conversions — census then unit cards, operator-settled 2026-08-28); lowering task `c78bb834`
**Repos:** `gradus/` (this repo; `src/**` at conversion time, `docs/factory/kernel-region-split/**` now)
**Related:** need `ef103950` (kernel closure modifier — language landing, gates closure syntax); [`docs/factory/dense-typed-assembly/goal.md`](../dense-typed-assembly/goal.md) (§3b superseded for fusion parents); `perf-gap-closure` L1 (the ~2,115 per-phase encoder count — claims law, not a conversion input)

---

## Invariant

Every Gradus function that mixes admit/policy (`⇥`, bags, `require`, `source`, optional-bias branches) with tensor math is two functions: an ordinary wrapper that keeps the policy, and a device region that reuses existing `@ kernel` leaves, a named private `@ kernel` when a second caller shares it, or a kernel closure for a one-off. No `⇥` function is ever marked `@ kernel`.

## Problem

The live source (verified 2026-08-28, census below) carries mixed functions whose math can never fuse because it lives inside policy signatures: `dense_block_static` / `dense_block_cached_static` inline an identical SwiGLU+residual tail and an identical QKV-with-optional-bias prologue (`src/transformer.fab` 630–699); legacy fixed-shape adapters in `src/nn.fab` detour typed tensors through staged carriers to reach math that already exists as typed `@ kernel` leaves (`nn.linear`, `nn.gelu`); and attention's per-head core exists as `@ kernel` (`scaled_dot_product_static`) while the multi-head parents remain bag walks with an illegal `list.append` head loop. Standing law: `$canonical-faber` pattern `kernel-region-split` (tentative, operator 2026-08-28) at `~/work/ianzepp/skills/faber/canonical-faber/references/patterns.md` §kernel-region-split, with the review note in that skill's `SKILL.md` §14.

## Proposal

Census first (every function of the seven named files plus tensor-math-composing siblings, one row each, live-verified), then dispatch one-family conversion units from the census — never a one-shot "convert everything." The operator decision tree (need `3b9e5796`, not reopenable) binds every unit:

1. Reuse an existing `@ kernel` leaf first (`nn.rmsnorm`, `nn.linear`, `nn.swiglu_hidden`, `nn.silu`, `nn.gelu`, `math.add`/`sub`/`mul`/`div`/`neg`, `attention.scaled_dot_product_static`). Generic Gradus code never calls `gradus/src/kernel.fab` frozen GEA3 entries.
2. Named private `@ kernel` when two callers share the region (`@ kernel` first, not `@ public`).
3. Kernel closure (need `ef103950`) for a one-off region; until that lands, one-offs also use (2). No `do kernel`.
4. One illegal nested call (bags, `list.append` head loop, `source()`, cache mutation) becomes an argument or its own later unit.
5. Session drivers, loaders, resolvers, cache admit, sampling, parsers are not kernels — record and skip.
6. Bias presence is host policy: wrapper supplies the tensor (zeros if absent); the kernel always adds.
7. Launch-count honesty: a source conversion without an export/plan change claims no encoder delta against the ~2,115 figure; a unit claiming encoder movement names the export seam in write_scope.

This supersedes `dense-typed-assembly` §3b ("no in-body call / assemblers stay unannotated") for fusion parents: parents that call existing `@ kernel` leaves are the fusion surface. Session drivers stay ordinary.

### Non-goals

- No rewrite of `gradus/src/kernel.fab` (GEA3 frozen launch catalog — parallel surface, not called by generic code).
- No launch-count / 2,115 delta claim from any unit that does not also change an exported program plan.
- No `@ kernel` on a `⇥` function; no `do kernel` spelling; no kernel body containing bias-presence branches.
- No conversion of session drivers (`decode_step`, `generate*`, `prefill*`), loaders/resolvers, cache admit, sampling, or parsers.
- No re-litigation of the decision tree (operator-settled; convert-or-record otherwise).
- No staged-carrier → typed-tensor pinning inside this campaign (SEM014/SEM016/SEM008 seams stay owned by `dense-typed-assembly` unit 5; recorded, not converted).

## Units (lowering sketch — cards in [`unit-cards.md`](unit-cards.md))

| Unit | Scope | Depends on | Hand evidence |
| --- | --- | --- | --- |
| KRS-1 | Census artifact over the seven named files + tensor-math siblings, every function one row | — | this commit (planner) |
| KRS-2 | `src/nn.fab` legacy fixed-shape adapters call typed leaves directly (one family) | — | none |
| KRS-3 | `src/transformer.fab` extract named private `@ kernel dense_mlp` shared by both static block twins | — | none |
| KRS-4 | `src/transformer.fab` named private `@ kernel` QKV always-add region; wrapper supplies zeros | KRS-3 (same file) | none |
| KRS-5 | `src/transformer.fab` `bert_tiny_block_2x8` marked `@ kernel` (pure glyph body, no `⇥`) | KRS-4 (same file) | none |
| KRS-6 (deferred) | `src/attention.fab` multi-head static parent (static `H`, no `list.append`); wrapper may still launch per head | KRS-3 green + column-slice admission + export-seam amendment for any launch claim | none |

Kernel-closure class (tree rule 3): zero live sites in the census — every carded region has a second caller or is a direct leaf call. The `ef103950` gate therefore blocks nothing in this campaign today; conversion hands that discover a genuine one-off note it on the card and defer (mind routing for need `3b9e5796`).

## Validation

Per-card oracle (need `3b9e5796` binds this on every conversion task): focused proba tuples byte-identical for the named cases; `faber check` green on touched files; if a card carries a launch claim, the exported launch count for the named family. Lane gates (full `./scripta/check-source`, `./scripta/check-compile`, package checks) stay with lint/test/merge, not on child Hands. Campaign closeout: all dispatched cards green, census ledger updated, and the `kernel-region-split` pattern promoted tentative → settled as a campaign milestone (first green conversion unit; a skills-repo edit filed separately, not inside a conversion unit).

## Delivery checklist

| Check | Enforced by |
| --- | --- |
| Every card cites the `kernel-region-split` pattern (standing law, tentative) | delivery audit against `unit-cards.md` |
| No card claims an encoder delta without a named export seam in write_scope | audit (need rule 7) |
| Proba tuples byte-identical on named cases (not "close") | Hand receipt + test lane |
| Wrapper keeps every `⇥`/bag/`require`/`source`/bias-presence site | audit against census `wrapper keeps` column |

## Ledger

| Unit | Status | Seat | Receipt | Notes |
| --- | --- | --- | --- | --- |
| KRS-1 census | done | planner | this commit | [`census.md`](census.md); starter rows verified live — corrections recorded in §0 |
| KRS-2 nn adapters | pending | — | — | no compiler dependency |
| KRS-3 dense_mlp | pending | — | — | named private; two callers |
| KRS-4 QKV always-add | pending | — | — | serialized after KRS-3 (same file) |
| KRS-5 bert_tiny @ kernel | pending | — | — | glyph-leaf law; serialized (same file) |
| KRS-6 attention parent | deferred | — | — | hole class; open questions in card |
| pattern promotion | deferred | — | — | after first green conversion; milestone, not a conversion unit |

## Open questions

1. **Attention parent slicing** — a static-`H` multi-head parent needs per-head column splits of packed `[T, H·D]` tensors; no slice glyph is admitted today (`_head` is a carrier walk; `for from grid at [i, j]` noted pending in `src/attention.fab`). Default: KRS-6 stays deferred until an admission exists; wrapper keeps per-head launches and says so in the receipt.
2. **Export seam ownership** — any launch-count claim requires a program-plan export change (radix-owned surface, e.g. the GEA wire-plan export family). Default: no gradus card carries a launch claim in this campaign unless the operator amends scope to name the seam.
3. **Bag-route retirement** — census records the carrier-twin bag routes as SEM014/SEM016/SEM008-blocked; `dense-typed-assembly` unit 5 owns their retirement. Default: out of scope here; recorded, not converted.
