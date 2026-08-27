# B2-RETUNE sweep — BLOCKED at the refreshed packet base (stop-report evidence)

## What landed (kept, focused-green)

The retune machinery is committed and unit-proven:

- radix `2b10f02f6` — `ONE_ROW_GEMV_WORKGROUP_X` width knob (currently 16)
  at the existing `apply_one_row_matmul_dispatch` seam (canonical probe +
  `launch_bindings.rs`), law extended to admit tile-multiple widths 8..=64,
  and the one-row body replaced with a direct per-column GEMV: at T=1 there
  is no cross-lane reuse, so one thread per output column streams K from
  global memory with no shared tiles and no barriers (the F-049 lane-wise
  early return becomes legal; `has_workgroup_reduction` stays false).
  `cargo test -p radix-mir-metal`: 182 passed (the resident-transpose
  fixture pin updated to the per-column `a_k` form).
- hosts `94a1dab` — the additive boundary pin made width-agnostic
  (workgroup `(w,1,1)`, grid `ceil(n/w)`, plan/launch width agreement);
  the fake-Metal structural launch passes.

## Why the sweep is blocked (pre-existing, reproduced at base revs)

The fixed1000 parity arm dies at the hosts mapper BEFORE any decode step,
at the packet base with none of my commits:

```
GEA3 plan → DeviceDescriptor mapping failed: resource `blk.00.kv_k`
carries a strided read window declaring row_stride 320 · row_count 1088
= 348160 ≠ the producer's 352000-element allocation; the declared stride
must equal the producer's actual pitch (GEA3-U6 num-3 pitch-truth law)
```

Reproduced with `parity run --stage smoke --target metal-m5max-fixed1000
--radix-rev 2f3a40531 --hosts-rev b4ca046` (logs: `basecheck-logs/`).
This is the B1 bucketed-extent fold: the kv window declares the bucket
length (1088 rows) while the producer allocation stays the 1100-row
capacity (352,000), and the pitch-truth law requires equality. Separately,
the harness export test is also red at base (`kv_append_k` frozen-identity
sha drift: harness pins `526510a8…`, the merged gradus source hashes
`66aeaea2…` — the B3 fold surface), though parity's export path bypasses
that check.

Both defects sit on B1/B3 fold surfaces outside this card's write_scope;
per the wave law they are not mine to pull in. No width was measured —
the oracle (fixed1000 t/s per width, certified 1000/1000) is unreachable
until the pitch-truth integration is repaired.

## Recommendation to the Mind

1. Repair card for the B1 kv-window pitch-truth mismatch (window
   row_count vs producer allocation) — it gates every fixed1000 physical
   measurement, not just this sweep.
2. Fold-state check for the B3 `kv_append_k` frozen-sha pin drift in
   `gea3_pipeline_test.rs`.
3. Once unblocked, re-dispatch B2-RETUNE: the knob, law, body, and
   width-agnostic hosts pin are already in place on `factory/pgc-b2`
   (width set to 16); the sweep is three constant edits + three parity
   runs.
4. The B2 verdict stands as closed (`residual`): the (8,1) wall
   regression is unchanged by this blockage; revert/retune decision
   remains with the Mind.
