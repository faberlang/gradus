# B2-RETUNE — width sweep result (task b12ac9a5, amended card)

## Base repairs (the two reopen blockers)

1. **B1 kv_k pitch-truth mismatch** — the B1 fold relaxed the harness
   admission (a strided read window may be a bounded whole-row prefix of
   the larger fixed-capacity producer) but never mirrored the relaxation
   into the hosts mapper law; every fixed1000 mapping died at
   `blk.00.kv_k` (row_count 1088 vs the 1100-row allocation). Fixed in
   hosts `gea3_decode.rs` (commit 4797049) by mirroring the radix
   condition verbatim: `allocation % row_stride == 0`, `pitch_span <=
   allocation`, bounded prefix only at the KV row width.
2. **B3 kv_append_k frozen-sha drift** — fold-state check: the parity
   protocol target pins gradus at `de687a4` (pre-B3), and under that pin
   the ORIGINAL identities are the truth; the packet/main gradus is
   post-B3, so the drift appears only against the local tree. Resolution:
   keep the pins at the protocol gradus (radix commit 7d302c35f); the
   residual local red (and the protocol pin's lag behind main gradus) is
   a protocol-pin refresh the Mind owns with the next baseline
   regeneration.

One additional landing repair surfaced during the sweep: the fused
elementwise tail re-guards the pending matmul write with
`row < m && col < n`, so the one-row body must keep `row` declared
(radix e54bf473b); and `apply_one_row_matmul_dispatch` now types temp
operands so the resident-transpose score/context GEMVs genuinely take the
one-row launch instead of silently keeping the tiled body while the
exported plan row claimed otherwise (radix 51263402f — the hosts census
caught that drift).

## Sweep (fixed1000, parity protocol, 3 paired runs, all certified 1000/1000, power ac)

| width | decode t/s (median) | range |
| --- | --- | --- |
| baseline (pre-B2) | 15.77 | standing baseline r02da078 |
| B2 (8,1) shared-strip body | 6.96 | the residual regression |
| 8 (direct body) | 16.34 | 16.12–16.37 |
| **16 (winner, landed)** | **16.44 / 16.42 final-tree confirm** | 16.38–16.56 / 16.40–16.98 |
| 32 | 16.21 | 16.11–16.72 |
| 64 | 16.28 | 16.21–16.91 |

Raw captures + reduced receipts: `w8/`, `w16/`, `w32/`, `w64/`, and the
final-tree confirmation `w16-final/` (radix 51263402f + hosts 4797049).

## Recommendation

**KEEP, at width 16.** Every swept width recovers and beats the 15.77
baseline (+3–4%); the direct per-column body — not the width — is the
dominant repair (16.34 at w8 vs 6.96 with the B2 shared-strip body at the
same width). The four widths sit within run-to-run noise of each other
(16.2–16.4); 16 is the median winner and the landed value
(`ONE_ROW_GEMV_WORKGROUP_X = 16`). No revert is warranted; the B2
mechanism plus this body/width is a net decode improvement with the 7/8
FMA dispatch reduction intact. Fold/verify cadence and any broader
re-baseline stay with the Mind.

## Validation

- `cargo test -p radix-mir-metal` 182 passed at every probe width and the
  final tree.
- Harness gea3 suite: green except the four pre-existing kv_append-pin
  env-gated failures (the documented protocol-pin lag above) and the
  artifact-env-gated exports when env is unset.
- Hosts: `gea3_decode_pgc_b2` 3 passed against the final export (every
  T=1 entry (16,1,1) over ceil(N/16), plan/launch width agreement,
  census); the four `gea3_decode` failures in the ad-hoc run were an
  artifact-set mismatch (fixed1000 bundle fed to the frozen-statue
  tests), not code regressions.
