# GOAL: collection-walk — `for from xs` when the index only re-indexes `xs`

**Status**: planned — drafted; convert class inventoried; implementation next
**Created**: 2026-08-26
**Campaign:** `—` (standalone host idiom; complementary to the 2026-08-26 while-to-range wave, not a second pass of that wave)
**Source:** operator session 2026-08-26 — the remaining offensive host form after count-`while` conversion is `for range 0‥d.data.layers().length()` used only to `get` the same collection
**Repos:** primary: `gradus/`
**Related:** `radix/docs/factory/container-bounds-law/goal.md` (checker law on bounded `get` / tensor `for from grid at [r,c]`; **do not fold this goal into that one**); Gradus while-to-range wave `bf075ae` (count loops only); `$faber` idioms (tensor `at […]` sibling)

---

## Invariant

A host walk whose index exists only to pull the next element of one
collection is written `for from xs`, not `for range 0‥xs.length()` plus
`xs.get(i)`. The index form stays when the index is the value: a count
with no collection, a zip or write-back across aligned lists, a built
index list, or a string walk until `for from s` is proven.

## Problem

The 2026-08-26 while-to-range wave (`bf075ae`) replaced `i ← i + 1`
count loops with `for range`. That left a second, louder smell: the
range is derived from a collection the body immediately re-indexes.

The offensive form is the layer walk:

```fab
for range 0‥d.data.layers().length() const i {
    const Layer layer ← d.data.layers().get(i) coalesce …
}
```

instead of:

```fab
for from d.data.layers() const layer {
}
```

Live convert-class sites in `gradus/src/` (2026-08-26 inventory; skip
`src/kernel.fab`, skip already-dirty / untracked foreign files):

| Path | Site | Walk |
| --- | --- | --- |
| `src/block_verify.fab` | `_request_capacity` | `checkpoint.layers()` |
| `src/block_verify.fab` | `_committed_identity_matches` | `accepted_ids` |
| `src/shape.fab` | `reshape` (both passes) | `target` |
| `src/serialize.fab` | `_byte_list` | `bytes o` |
| `src/tokenizer.fab` | `_sort_ascending` membership | `out` |
| `src/model/gguf.fab` | `_contains` | `xs` |
| `src/model/gguf_manifest.fab` | `_contains` | `xs` |
| `src/model/gguf_manifest.fab` | `_join_bytes` | `bytes b` |

`rg 'for range 0‥.+\.length\(\)' src --glob '*.fab'` still matches after
this goal. Those leftovers are keep-class (see Proposal). Zero remaining
**convert-class** hits is the closeout, not zero `.length()` hits.

## Proposal

Admit one convert class:

```text
for range 0‥xs.length() const i { … xs.get(i) … }
```

where `i` is not used except to index that same `xs` (including
`xs()`-shaped getters such as `checkpoint.layers()`). Rewrite to
`for from xs const x` (or `for from xs() const x`). Drop the
`coalesce` that existed only to paper over `get`.

### Keep `for range`

| Class | Why the index stays | Example |
| --- | --- | --- |
| Count / protocol repeat | no collection, or length used only as N | `for range 0‥cfg.layers`; `_oracle_empty_layers` |
| Index list | `i` is the value appended | `positions.append(i)` in `dense.fab` / `decode.fab` |
| Zip / write-back | two or more aligned collections, or `legacy-L2` comments | `a.layers()` vs `b.layers()`; candidate keys + payloads |
| Index is identity | vocab id, return-index, replace-at | `tokenizer.is_eog(i)`; `_best_index`; `_find_name` |
| String walk | `for from s` not proven on `string` | `_hex_ok`, `_numeric`, `_contains_separator` |

Do not invent a zip combinator. Do not fold tensor `for from grid at [r,c]`
into this goal — that sibling is already law in `$faber` and
`container-bounds-law`.

### Non-goals

- Checker enforcement (that is `container-bounds-law`)
- A second while-to-range pass
- String `for from s` until a dedicated proof lands
- Zip / parallel-list helpers
- `src/kernel.fab` (frozen GEA)
- Foreign dirt: dirty docs, `scripta/`, untracked `src/model/qwen35moe_state.fab`
- A SmolLM2 / Qwen wrapper zoo, radix MIR work, or `$faber` skill edits

## Units (lowering sketch — refine via `$delivery`)

| Unit | Scope | Depends on | Hand evidence |
| --- | --- | --- | --- |
| 1 | Ledger this goal from the radix factory template | — | this file |
| 2 | Convert the inventoried convert-class sites in `gradus/src/` | 1 | commit; `rg` leftover classified keep; `faber check .`; focused proba on touched files |

## Validation

Closeout when every inventoried convert-class site is `for from` and
every remaining `for range 0‥….length()` in `gradus/src/**/*.fab` is
keep-class.

```bash
FABER_LIBRARY_HOME=/Users/ianzepp/work/faberlang
# workspace faber, not ~/.cargo/bin/faber
faber check .
rg -n 'for range 0‥.+\.length\(\)' src --glob '*.fab'
```

Focused proba on each touched module that has one. Suite-green of the
whole package is not required for closeout.

## Delivery checklist

| Check | Enforced by |
| --- | --- |
| New grammar production or variant ships with a `corpus/variant-cells.toml` ledger row + corpus exemplum + `.expected` stdout | n/a — no grammar change |
| Convert-class sites rewritten; leftovers are keep-class | Unit 2 `rg` + this goal's keep table |
| Package check green | `faber check .` |

## Ledger

| Unit | Status | Receipt | Notes |
| --- | --- | --- | --- |
| 1 | in progress | — | this file |
| 2 | pending | — | convert class only |

## Open questions

1. **String `for from s`.** Default: keep `for range 0‥s.length()` plus
   `s.get(i)` / `s.slice(i, i + 1)` until a dedicated proof shows
   `for from` on `string` binds characters. Revisit; do not convert in
   this goal.
2. **Method-call source.** Default: `for from checkpoint.layers() const layer`
   is the spelling (evaluate the getter as the walk source). If check
   rejects a call in that position, bind once (`const layers ← checkpoint.layers()`)
   then `for from layers`.
