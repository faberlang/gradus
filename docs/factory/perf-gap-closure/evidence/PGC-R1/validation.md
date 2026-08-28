# PGC-R1 — indexed prefill embedding gather (validation)

Card: `delivery.md` §7 PGC-R1. Packet `worktrees/pgc-r1`, branch
`factory/pgc-r1`, bases: radix `db4d7faad`, gradus `f004523`, hosts
`6823cd3`.

## What changed

- **gradus** `src/kernel.fab`: `embedding_gather` is now
  `fn embedding_gather(tf32[49152,960] embeddings, lista<u32> ids, mut tf32[1,960] output) → void { output ← embeddings.gather(ids) }`.
  The one-hot selector matmul and its CTO `0891c09b` design note are
  superseded (per the 2026-08-28 reopen order); the tied
  `token_embd.weight` `[49152,960]` buffer stays one physical allocation
  shared with `lm_head_gemv`. `src/kernel.proba`: the named case (both
  occurrences) tracks the new signature.
- **radix** — the row-gather recipe (`CollectionKernelPlan::Gather`,
  `emit/gather.rs`) already existed at the MIR level (GI3-1/GI3-3) but was
  unreachable from a Faber `@ kernel` entry: the storage-buffer ABI
  synthesis rejected the `lista<u32>` ids param
  (`abi/signature.rs` `multi_input_indexed_view_kernel` admitted only
  device-view tensors). Live-inspection-required additions (named here
  per the card's "only as live inspection requires" clause):
  - `radix-mir/src/abi/signature.rs` — `gather_ids_param_count`: a kernel
    input param typed exactly `Array(numerus<u32>)` that is the function's
    `TensorGather` ids operand binds as a read-only storage buffer whose
    element count is the gather's output row count `T` (the same typed
    fact `gather_recipe_facts` admits, so the ids count and the plan's
    `id_count` cannot disagree). Every other input keeps the device-view
    law; an unrelated array param still fails closed (the device-safe
    gate's typed carve-out is unchanged and mirrored).
  - `radix-mir-metal/src/launch_bindings.rs` — `launch_variant_signature`
    keeps a matched canonical read resource's element type (the ids extra
    input is `numerus<u32>`, not F32); unmatched reads keep F32.
  - `kernel_plan/{plan,build,kernel_plan_test}.rs` — **unchanged**: the
    existing Gather recipe covers the token-indexed row copy; no new
    admission facts were needed (the trio stays folded clean for R4/R5).
  - `emit/gather.rs`, `emit/literal_indexed.rs` — unchanged.
  - `mir-emit-harness/src/gea3_pipeline_test.rs` — the embedding-entry pin
    regions (superseding the B2-era T=1 matmul pins for this entry):
    `HEAD_SPECS`/`PREFILL_HEAD_SPECS` counts + sha, the two `signature()`
    pins, the `plan_for_entry` Gather arm (wire `WireGatherPlan`), the
    removed `tiled_matmul_shape` rows, the right-operand-layout row, the
    `num-4` pitch test (now the row-copy pin), the T=1 geometry test (now
    `gea3_embedding_gather_launch_matches_row_copy_msl_geometry`), and
    the F32-layout law carve-out for the ids resource.
  - `mir-emit-harness/src/gea3_pipeline_pgc_c5_test.rs` — the
    `prefill_embedding_gather` weight pin follows the new signature
    (weight moved to binding 0; live-inspection-required, named here).
  - NEW additive `mir-emit-harness/src/gea3_pipeline_pgc_r1_test.rs`.
- **hosts** — NEW additive `tests/gea3_decode_pgc_r1.rs` (compact token-id
  binding, 144 B ids upload vs 7,077,888 B selector, row-copy launch
  geometry, byte-exact ids round-trip, fake-session census).
  Live-inspection-required, named here:
  - `src/metal_host.rs` — the fake driver's `GEA3_ENTRY_ARITIES` row for
    `embedding_gather` admits the compact 3-binding canonical ABI beside
    the bundle's 4-binding launch (embedding-entry pin).
  - `tests/gea3_decode_pgc_b2.rs` — `embedding_gather` left the T=1
    one-row matmul set (the card's B2-era pin supersession; the entry is
    the row-copy gather now).

## Proba tuple oracle

Isolated package (the PGC-B3 precedent — the full `src/kernel.proba`
package stays blocked by the pre-existing SEM013 at line 596). The named
case `gea3u3c_embedding_gather_static_f32_shape` extracted verbatim;
before = selector-signature call, after = token-id-signature call.
Before/after `faber test --format json` runs (packet-built binary) are
byte-identical: same case path, status 1, case `failed` with reason
"runner refuses execution of @ kernel function", stdout 582 bytes /
`92cc580c…` both sides, stderr 0 bytes both sides. See
`proba-tuple-oracle.json` and the four raw files.

## FMA / staged-byte census (primary evidence; condition-B rider)

See `fma-staging-census.json`. Fixed-1000 prefill, per invocation:
dispatched GEMM-class FMAs 1,887,436,800 → **0** (the 40-row-padded
`[40,49152,960]` class is gone); staged embedding-side upload
7,077,888 B (one-hot `[36,49152]` selector) → 144 B (`[36]` u32 ids),
−7,077,744 B ≈ the ~7.08 MB of the 23.1 MB fixed-1000 staging the card
names; useful work 36 × 960 = 34,560 row-copy element copies. No wall
claim (L1-gated wall belongs to PGC-R3's family-keyed capture).

Two-class note: the row copy has no rounding surface — byte identity is
the declared class; no tolerance was invoked or widened.

## Proofs run (packet)

- radix: `cargo test -p mir-emit-harness --lib` gea3 suites — all
  embedding tests green (new `pgc_r1` set 4/4; rewritten `num4` and
  launch-geometry tests green; comparator green; pgc-c5 green).
  `cargo test -p radix-mir` / `-p radix-mir-metal` (abi + launch_bindings
  touched): see run logs — green.
- hosts: `cargo test -p faber-host-macos-arm64 --test gea3_decode_pgc_r1`
  3/3 green; `gea3_decode_pgc_b3` 4/4 green; `gea3_decode_pgc_b2`
  compiles, its two bundle-dependent tests stay env-gated
  (`GEA3_ARTIFACT_DIR`), the pre-existing class.

## Pre-existing reds NOT introduced by this card (owner: PGC-R3 / Mind)

- The frozen-bundle export tests (`gea3_pipeline_exports_*`,
  identity-checked suites) fail at packet base on the `kv_append_k`
  canonical-sha pin (`526510a8…` pinned vs `6f6c2e69…` live): the radix
  pins at `db4d7faad` predate gradus B3 `d942388`. Verified by restoring
  the pre-change `kernel.fab` and rerunning — the failure is identical.
  This is the documented §7.5 pin lag; regeneration is routed to
  PGC-R3's re-key.
- Consequence for this card: the exported-bundle embedding rows (Gather
  plan JSON, ids buffer minting) are exercised through
  `build_program`/`plan_for_entry` inside the green tests above, but the
  full wire round-trip of the new plan variant lands with R3's
  regenerated bundle. One open fact that re-key must settle: the plan
  mirror's `element_ty` for the ids resource (the builder stamps `f32`;
  hosts' GEA3 statue is F32-only and `DeviceDataType` has no `u32`) —
  the emitted MSL truth (`device const uint* ids`) is pinned by the new
  tests regardless.
