# ARCHIVED: head-axis retirement — durable receipt for superseded branch `factory/head-axis`

**Status**: closed 2026-09-21 (unit ON-M1, seat `merge`/packet-control). The retired
branch ref `factory/head-axis` is deleted; its tip commit `6506c03` is retained in the
object store.
**Commit**: `6506c03` — `feat(kernel): batch decode attention entries to head-axis signatures (U4)`
**Disposition**: SUPERSEDED — never landed on main; the branch ref is retired.

## SUPERSEDE ruling

`head-axis` gradus `6506c03` is **SUPERSEDED**: verification mail `272ba9d0`
(2026-09-13) — "all four 6506c03 decode-family behaviors are represented generically
on gradus main". Do not land it.

## Provenance

This ruling was previously recorded only transiently in
`.vivi/tmp/merge-orphan-2026-09-17.md` (orphan sweep 2026-09-17T03:2xZ, lanes
`sgr-c1`/`sgd`/`head-axis`). Unit ON-M1 moved the `head-axis` ruling into this
durable receipt at the location named by the Mind
(`gradus/docs/archived/head-axis-retirement.md`); the transient file is not the
authoritative record.

## Acceptance checks (done_when)

- `git branch --list factory/head-axis` — empty (ref deleted, object store untouched, no gc)
- `git cat-file -e 6506c03^{commit}` — passes (object retained)
