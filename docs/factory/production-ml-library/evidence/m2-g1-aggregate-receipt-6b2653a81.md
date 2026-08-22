# MODEL-02-G1 — Aggregate validation receipt (real-file executed proof at fixed tip)

**Date**: 2026-08-22 · **Host**: burgus · **Mode**: direct on main, task `061b99e9`

## Command (the U7 closeout command, executed at radix `6b2653a81`)

```bash
cd gradus && env FABER_LIBRARY_HOME=/Users/ianzepp/work/faberlang \
  /Users/ianzepp/work/faberlang/radix/target/debug/faber run exempla/moe-probe -- \
  /Users/ianzepp/ai/models/Qwen3.6-35B-A3B-UD-Q4_K_M.gguf 10991392 \
  0b21525e972670ed59e1812e170b27c26355381f0656ecc4e25617ece7dac58b
```

- Binary: `radix` @ `6b2653a81` ("fix(mir): run windowed octeti reads" — the U7
  unblock), built in-tree `cargo build -p faber` (exit 0). Tree carried foreign
  dirt (unrelated expectation files); not touched.
- Gradus tree: main `7ea19ec` (U7 `fccd376` + U8 docs at HEAD).
- Wall clock: ~12024 s (≈3h20m, interpreted MIR runner); exit 0.
- Note: `--target fmir` was dropped from the README spelling — current
  `faber run` has no `--target` flag; the exemplum's `faber.toml` selects the
  target. Same command otherwise.

## Observed vs expected PASS census

Expected per the U7 README: 8 per-probe PASS lines +
`PASS real-file moe probe receipt`. Observed: **9 PASS lines, 0 FAIL,
0 divergence** (log `/tmp/moe-probe-g1.log`):

```
ADMIT qwen35moe
CONFIG moe experts=256 used=8 ffn=512 shared=512 embedding=2048
BAND delta=0.00001
PASS layer=0  probe=p1 ... first-divergence=none max-dev=4.97e-08
PASS layer=0  probe=p2 ... first-divergence=none max-dev=1.79e-08
PASS layer=3  probe=p1 ... first-divergence=none max-dev=2.09e-08
PASS layer=3  probe=p2 ... first-divergence=none max-dev=1.63e-08
PASS layer=39 probe=p1 ... first-divergence=none max-dev=2.09e-08
PASS layer=39 probe=p2 ... first-divergence=none max-dev=2.14e-08
PASS layer=40 probe=p1 ... first-divergence=none max-dev=6.44e-08
PASS layer=40 probe=p2 ... first-divergence=none max-dev=2.88e-08
PASS real-file moe probe receipt
```

Max deviation across all 8 probe rows: **6.44e-08** — 2.6 orders under the
Δ = 1e-05 band (`band.delta`, U2 oracle). All router indices exact (selection
order, lowest-index tie rule). Full log retained at `/tmp/moe-probe-g1.log`;
the authoritative per-row values are those printed lines and the U7 README
hash table (unchanged).

## Aggregate verdict

- U7 blocked status is resolved: the pre-existing octeti-indexing MIR runner
  debt was fixed at radix `6b2653a81` (foreign owner) and the executed proof
  now runs green at the fixed tip.
- Child proofs: U1–U8 landed and green per their receipts; `scripta/check-compile`
  green with the registered `moe-probe` block (receipt
  `check-compile-receipt-59c9ed3.md`); chain landed as one authority on gradus
  main (U7 `fccd376` … `7ea19ec`) — no merge lane needed, direct on main per
  workspace default.
- Campaign row **MODEL-02** done oracle — "router choices, expert weights,
  intermediate values, and outputs match the independent oracle" — is met at
  the component tier by the 8/8 exact-index, sub-band rows above. No
  full-model claim (MODEL-04 boundary); no tier upgrade.

**MODEL-02: DONE.**
