# PGC-C5 owed evidence — discharged by PGC-R3 (audit-debt 77ca6b07)

## Copy-in census derivation (R3 family capture, fixed1000 run-001)

| Row | standing report (pre-fold) | R3 family capture |
| --- | ---: | ---: |
| prefill staged bytes | 23,076,864 (23.0/23.1 MB) | 15,999,120 |
| prefill copy-in handles | 1,089 | 1,089 |

Weight-shaped prefill inputs are once-resident in the folded family (handles
constant; the byte delta −7,077,744 is exactly R1's one-hot selector removal,
with its 144 B ids upload replacing it). Device proof:
`gea3_pgc_c5_prefill_weights_are_once_resident_and_activations_stay_dynamic`
and `gea3_pgc_c5_fixed1000_prefill_receipt_reports_reduced_staging` — **green**
against the R3 family bundle and physical receipt.

## Gradus no-diff proof

`gradus-no-diff-proof.txt` in this directory records
`git diff --exit-code -- src/kernel.fab src/kernel.proba` (exit 0 at the R3
pin b762163) and that no C5-labeled commit ever touched the gradus kernel
sources (C5 was verify-untouched by design).
