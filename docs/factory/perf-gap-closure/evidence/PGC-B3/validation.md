# PGC-B3 validation record

## Delivered source contract

`gradus/src/kernel.fab` now declares `kv_append_k` and `kv_append_v` as three
`tf32[320]` row views. Each entry emits `output ← history + row`.
Position selection is represented by the host `Position` binding and its
byte-offset/view-span envelope. No capacity-sized `[76,1]` selector is part of
the source contract.

The named `gradus/src/kernel.proba` cases were updated to call the new
three-argument row contract. Prefill KV entries were not changed.

## Focused proofs

| Proof | Result |
| --- | --- |
| Faber check of `src/kernel.fab` | PASS, exit 0; existing warnings only |
| `cargo test -p mir-emit-harness pgc_b3 -- --nocapture` | PASS, 3 passed, 0 failed |
| Focused proba tuple oracle | Before/after status, case status, stdout, and exact stderr bytes are identical; both runner cases retain the existing `runner refuses execution of @ kernel function` failure because the MIR runner does not execute kernel functions |
| Hosts device test | NOT RUN: packet Cargo workspace cannot load `../../faber/runtime/rust/Cargo.toml`; the packet contains Gradus, Radix, and Hosts only |

The focused proba artifacts are `proba-before.stdout.json`,
`proba-after.stdout.json`, `proba-before.stderr`, `proba-after.stderr`, and
the machine-readable comparison in `proba-tuple-oracle.json`.

The normal full Gradus package command remains blocked by the pre-existing
`SEM013:wrong_number_of_arguments` at `src/kernel.proba:596` in
`prefill_causal_softmax`; that unrelated case was not edited.

## Paired parity

A candidate-pinned `--stage full` parity preflight was attempted with all three
PGC-B3 commits. It stopped before any paired decode row because the forbidden
shared `gea3_pipeline_test.rs` still pins the old `kv_append_k` source digest:

- actual direct-row digest: `6f6c2e698a792323e4fad1c1c634923a64f20a96daef241e7578cede66ee251d`
- shared fixture digest: `526510a807248f5fe7cb6df2b66d754231d734544266dde51af5f430984112d2`

The partial candidate capture contains no paired rows and is therefore not a
parity receipt. No 1000/1000 result, KV work delta, or compact-constant timing
delta is claimed. The exact command, exit status, and export stderr are in
`parity-candidate-attempt.json` and
`parity-raw-candidate-attempt/parity-metal-m5max/gea3-export/stderr`.

The integrating fold must update the shared GEA3 export identity/plan outside
this card's forbidden write scope before the fixed-1000 paired parity capture
can be run honestly.
