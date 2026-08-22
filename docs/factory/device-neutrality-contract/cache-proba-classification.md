# cache.proba classification — DNC-U6 closeout input

**Status**: recorded 2026-08-22 — classification + stale-helper fix.
**Handle**: `9975f4a4` (re-dispatch of `a816aad1`).
**Do not treat this file as DNC-U6 landed.** U1–U6 ledger Status stays
pending until the closeout seat runs the full U6 command block.

## 1. Receipts

| Item | Value |
| --- | --- |
| Gradus parent at classify | `ec9eff0` (`docs: use GradientError in diagnostics`; docs-only after `5987180`) |
| Prior cache movers | `f913211` (B3 history copy), `6b6ebab` (string.get wire predicates), `63a8d73` (`KVCheckpoint`, `cache_branch` only) |
| Faber binary | repo `radix/target/debug/faber` (`faber 1.8.0`) |
| `FABER_LIBRARY_HOME` | `/Users/ianzepp/work/faberlang` |
| Focused suite | `faber test --include cache` and `faber test src/cache.proba --include cache` |
| Focused result | **33 passed / 0 failed / 0 blocked / 0 skipped** |

Bare U6 command `faber test src/cache.proba` (no `--include`) is
**environment-red**: package MIR test link fails on
`src/decode.proba` with `unsupported MIR lowering: method call before
runtime/provider MIR lowering`. That is the package-route loader, not a
cache.proba assertion. Same family as the pkghang seat named in the
original dispatch. Use `--include cache` until that loader is green.

## 2. Classes

- **green** — passes at HEAD; no action.
- **rot** — language/golden/helper moved; cache semantics unchanged.
  Original seat `a816aad1` repaired the string.get wire predicates in
  `6b6ebab`. This seat repaired the last rot (hold_i32 helper).
- **moved/green** — was red in the 19-failure baseline; turned green by a
  landed cache-semantics commit (`f913211`), not by this seat.
- **environment** — harness/package-link, not a cache assertion.
- **defect (out of cache)** — real failure, not cache admission. Named
  and routed; not absorbed into `cache.fab`.

No remaining **cache-semantics** defect. `append` already rejects an
I32-tagged K with the pinned message `"unsupported dtype for cache"`
once the probe tensor is actually tagged I32.

## 3. Original 19-failure cohort (re-checked at HEAD)

Baseline remembered by `a816aad1`: 12 passed / 19 failed at pre-B3
`885fd4e`. After `f913211` + `6b6ebab` the live suite was 32/1. This
re-run is against current HEAD (`ec9eff0` + the helper fix below).

| # | Case | Class | Evidence / mover |
|---|---|---|---|
| 1 | empty_cache rejects the identity/domain invariants | rot → green | `_has_no_separator` compared raw `string.get`. RM-1 `b1db45868`. Fixed `6b6ebab`. |
| 2 | append extends by one position and preserves K/V | moved/green | B3 `f913211` copies history before append. |
| 3 | sequential appends preserve history and prior positions | moved/green | B3 `f913211`. |
| 4 | append rejects a non-f32 K/V | rot (helper) | See §4. Not a cache admission defect. |
| 5 | reset keeps capacity and identity | moved/green | B3 `f913211`. |
| 6 | equal append sequences produce equal caches | moved/green | B3 `f913211`. |
| 7 | cache_identity derives the full key | moved/green | B3 `f913211`. |
| 8 | identity wire round-trips exactly | rot → green | `_numeric` passed raw `string.get` into `_digit`. RM-1. Fixed `6b6ebab`. |
| 9 | empty-history identity wire uses the sentinel | rot → green | Same `_numeric`/RM-1. Fixed `6b6ebab`. |
| 10 | identity wire rejects unknown markers/schema/malformed fields | rot → green | Same parser gate. Fixed `6b6ebab`. |
| 11 | KVStructure identity wire round-trips and pins default form | rot → green | Same `_numeric` in the structure parser. Fixed `6b6ebab`. |
| 12 | KVStructure wire rejects unknown markers/dtypes/reserve | rot → green | Same parser gate. Fixed `6b6ebab`. |
| 13 | heterogeneous v4-flash-shaped KVStructure assignment | rot → green | Same layer-index/head/dimension parse. Fixed `6b6ebab`. |
| 14 | 1.0.0 Dense/SWA and 1.1.0 HCA wires | rot → green | Same parser movement. Fixed `6b6ebab`. |
| 15 | invalid cache-class combinations fail closed | rot → green | Same parser movement. Fixed `6b6ebab`. |
| 16 | extend appends T rows and preserves identity | moved/green | B3 `f913211` copies history before extend. |
| 17 | append admits the last capacity row and rejects capacity+1 | moved/green | B3 `f913211`. |
| 18 | extend rejects overflow without mutating state | moved/green | B3 `f913211`. |
| 19 | structure-built reset preserves capacity and advances generation | moved/green | B3 `f913211`. |

B3 significance (re-confirmed): the two rows added by `f913211`
(`successful append and extend leave the input cache histories unchanged`;
`a partially invalid extend leaves the input cache unchanged`) pass. They
were never hidden inside the 19.

`63a8d73` (`KVCheckpoint`) does not touch `src/cache.proba`.

## 4. Row 4 — hold_i32 helper rot, not cache admission

At HEAD before this seat, the only remaining `cache.proba` failure was:

```
FAIL cache.proba::append rejects a non-f32 K/V (only the F32 row is admitted)
  comparison type mismatch
```

Isolation (temporary diagnostics, not committed):

| Probe | Result |
| --- | --- |
| `math.cast(hold([1.0, 0.5, 0.2, -0.5], [1, 4]), "i32")` | `comparison type mismatch` (uncaught runner error) |
| `math.cast(hold([1.0, 2.0, 3.0, 4.0], [1, 4]), "i32")` | same |
| `tensor.construct_dtype(..., dtype.i32())` | green; tag is `"i32"`, shape `[1, 4]` |
| `append` of that construct_dtype K | green; message `"unsupported dtype for cache"` |

`hold_i32` used `math.cast`, so the runner error fired **before**
`cache.append`. Cache admission was never reached. `dtype.name(key.dtype())
≡ "f32"` in `src/cache.fab` is not the comparison that fails (`≡` is not
the runner's ordering mismatch).

**Named finding (still live, out of this write scope):**
`CACHE-NON-F32-DTYPE-COMPARISON` — `math.cast` F32→I32 on the FMIR stepper
raises `comparison type mismatch`. Likely site: `dtype.cast`'s I32 arm
(`payload.round()` then `n ≺ minimum_i32`). Owner: `gradus:math` /
`gradus:dtype` / runner. Do not repair inside `cache.fab`.

**This-seat fix:** `hold_i32` tags through `tensor.construct_dtype` (the
probe needs the I32 tag, not value conversion). Pinned append message
unchanged. After the helper change the focused suite is 33/0.

## 5. Current 33-row suite

All green under `--include cache` after the helper fix.

| Case | Class at HEAD |
| --- | --- |
| empty_cache builds a fresh cache with full identity and empty state | green |
| empty_cache rejects the identity/domain invariants | green (rot `6b6ebab`) |
| append extends by one position, preserves the K/V exactly, and bumps the generation | green (`f913211`) |
| sequential appends preserve the history order and prior positions | green (`f913211`) |
| successful append and extend leave the input cache histories unchanged | green (B3 row) |
| a partially invalid extend leaves the input cache unchanged | green (B3 row) |
| append rejects a negative token id and malformed K/V | green |
| append rejects a non-f32 K/V (only the F32 row is admitted) | green (helper rot repaired this seat) |
| reset keeps capacity and identity, clears rows, and advances generation | green (`f913211`) |
| equal append sequences produce equal caches (pure, no hidden state) | green (`f913211`) |
| cache_identity derives the full key (prefix, position span, layer, dtype, layout) | green (`f913211`) |
| the fresh cache's identity key has the empty history and the 0..0 span | green |
| the identity wire round-trips exactly | green (rot `6b6ebab`) |
| the empty-history identity wire uses the sentinel | green (rot `6b6ebab`) |
| the identity wire rejects unknown markers, schema, and malformed fields | green (rot `6b6ebab`) |
| KVStructure profile_cuda rejects construction before any family-law check | green (DNC-U1 `2712d8f`) |
| KVStructure profile_gi4 admits today's family law through the profile-aware constructor | green (DNC-U1 `2712d8f`) |
| KVStructure admits the default Dense/F16/classic bundle and pins identity fields | green |
| KVStructure identity wire round-trips and pins the default form | green (rot `6b6ebab`) |
| KVStructure admits GQA sharing, SWA, and quantized-V with the flash family | green |
| KVStructure rejects infeasible combinations fail-closed | green |
| KVStructure construction rejects empty and invalid layer sets | green |
| KVStructure wire rejects unknown markers, unadmitted dtypes, and bad reserve | green (rot `6b6ebab`) |
| KVStructure admits a v4-flash-shaped heterogeneous class assignment with an indexer partition | green (rot `6b6ebab`) |
| KVStructure 1.0.0 Dense/SWA wires stay byte-identical; HCA-only bumps to 1.1.0 | green (rot `6b6ebab`) |
| KVStructure rejects invalid cache-class combinations fail-closed | green (rot `6b6ebab`) |
| extend appends T rows in one mutation and preserves identity | green (`f913211`) |
| empty_layers builds one empty cache per contiguous KV layer | green |
| empty_layers copies KVStructure.context_length as immutable capacity | green |
| append admits the last in-capacity row and rejects capacity+1 before mutation | green (`f913211`) |
| extend rejects overflow before mutation and leaves rows, capacity, and generation unchanged | green (`f913211`) |
| reset of a structure-built cache preserves capacity and advances generation | green (`f913211`) |
| a rejected append on a helper cache leaves rows, capacity, and generation unchanged | green |

## 6. U6 closeout command implications

U6's closeout block still names `faber test src/cache.proba`. As written,
that package-path invocation is environment-red (§1). The cache suite
itself is green under `--include cache`. Closeout must either keep the
`--include cache` filter or wait for the package-link seat; it must not
treat a decode.proba MIR lowering miss as a cache.proba regression.

DNC-U1..U5 source/docs already exist on main (`2712d8f`, `c9961af`,
`58e0155`, `d6f2b99`, `58a704a`). This file does not advance those ledger
rows.
