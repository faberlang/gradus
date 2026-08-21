# GI4 KvCacheLayout — dtype contract revision

**Origin**: `radix/docs/factory/gpu-inference-gguf/gi4-contract.md` §3
(lines 93–108). The freeze is not writable in this packet; this file is
the Gradus-side revision record.
**Mechanism**: the freeze's own revision path (`gi4-contract.md:105-106` —
"a dtype change is a contract revision, never a silent widening").
**Ruling**: operator-accepted 2026-08-18, need `1d3967ed`, memo `3df6f724`.

## Unchanged facts

Five facts stay: `slots`, `context_length`, `layer_count`, `kv_head_count`,
`head_dim`, plus `reserve_policy`. Byte accounting remains the single
authority for "KV bytes per `KvCacheLayout`" — consumed, not re-derived.
The reserve policy stays a separate declared bound (headroom at admission).
GI4 begins with one sequence, one slot (`slots = 1`); the layout is typed
so later stages can admit more slots without a new vocabulary.

## Revised dtype row

| Field | GI4 freeze (closed) | This revision |
| --- | --- | --- |
| `KvCacheLayout.dtype` | `f32` only (declared-conversion representation) | `{F32, F16, Q8_0, Q4_K}` |
| Default | f32 | **F16** |

The opened set above is not today's executed representation: the executed
`KVCache` today is f32-staged (`dtype()` "f32", `layout()` "staged";
`src/cache.fab:265-273, :362, :398-399`). Closing that gap is
`production-ml-library` execution-tier scope.

The Gradus semantic carrier of the opened set is `KVStructure.kv_dtype_k` /
`kv_dtype_v` in `src/cache.fab` (W2-U1). Infeasible combinations fail
closed there (quantized-V requires the flash-attention family; block size
must divide the flattened KV width). Hosts still consume `KvCacheLayout`
facts without re-deriving bytes.

## Revision note

Recorded 2026-08-18. The freeze anticipated this opening and forbade a
silent widening. The operator accepted the amendment (need `1d3967ed`).
This document is the packet-local contract revision.
