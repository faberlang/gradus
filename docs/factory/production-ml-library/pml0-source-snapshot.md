# PML0 Source Snapshot — six-repo revision + dirty-state record

**Snapshot taken**: 2026-08-08 (git reads only; no cargo anywhere)
**Unit**: PML0-U1 (source snapshot refresh + dirty-state record)
**Authority**: campaign pins from `pml0-delivery.md` §Source snapshot; live values verified per repo on the snapshot date.
**Consumed by**: PML0-U2…U14 (each unit cites the version stamps from this record).

## Snapshot table

| Repo | Campaign pin | Live HEAD (2026-08-08) | Match | Drift note |
| --- | --- | --- | --- | --- |
| gradus | `29d26735d0d9` | `d7e85aa6aad1fd41c53524f08c481553b154d042` | drift | Drift replaced — see below |
| norma | `84f27dacd6f9` | `84f27dacd6f9bffa4882f789a243ce32f0f060b4` | match | — |
| faber | `26b503a0e3bb` | `44008e63de5352b7985723397f0a0821f0684060` | drift | Drift replaced — see below |
| radix | `a01543b06bfe` | `a01543b06bfe8d99bfb3e6e6e21a2220eda5e6c4` | match | — |
| hosts | `e066ee0ae98a` | `e066ee0ae98afa5c7556e1f765072a6357050149` | match | — |
| examples | `aad199ecf07c` | `aad199ecf07cb23f5d4127c3f68974cab3901235` | match | — |

The six recorded live values equal `git rev-parse HEAD` in each repo as of the snapshot date.

## Drift replaced

- **gradus**: pin `29d26735d0d9` (BERT-tiny surface) **replaced by** `d7e85aa` — campaign commit landing the council review + PML0–PML7 delivery specs. The older pin no longer heads `main`.
- **faber**: pin `26b503a0e3bb` (S3-A2 companion probes) **replaced by** `44008e6` — NGAB0 campaign commit landing the council review + NGAB0–NGAB7 delivery specs. The older pin no longer heads `main`.

Norma, radix, hosts, and examples pins match live HEADs; no correction needed.

## Per-repo dirty state (`git status --porcelain`)

All six repos report a **clean** working tree (empty porcelain output) on the snapshot date:

| Repo | `git status --porcelain` |
| --- | --- |
| gradus | clean |
| norma | clean |
| faber | clean |
| radix | clean |
| hosts | clean |
| examples | clean |

**Resolution note (gradus)**: the PML0 delivery draft recorded gradus dirt as untracked `docs/factory/README.md` + `docs/factory/production-ml-library/` (the campaign draft itself). Those files are now tracked at HEAD `d7e85aa`, so gradus is clean as of this snapshot. Any later unit comparing dirty state against this record must use the live `git status --porcelain` output as the source of truth.

## Validation

```bash
git -C gradus rev-parse HEAD && git -C norma rev-parse HEAD && git -C faber rev-parse HEAD \
  && git -C radix rev-parse HEAD && git -C hosts rev-parse HEAD && git -C examples rev-parse HEAD
git -C gradus diff --check
```

Outcome: six live HEADs equal the table's live column; `git diff --check` clean.
