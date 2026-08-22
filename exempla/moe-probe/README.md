# MODEL-02-U7 — real-file MoE executed proof exemplar

This package is the application-owned adapter that proves the
`gradus:model/moe` surface against the local Qwen3.6 artifact (the
`gguf-admit-qwen35moe` + `gguf-materialize` patterns). It resolves the
operator artifact path from argv, pins identity (digest + length), runs
`qwen35moe.admit` (ADMIT receipt line), maps the admitted config to
`moe.MoeConfig`, binds TensorViews per canonical name, serves the windowed
element source, and executes `route`/`ffn_moe` on layers 0/3/39/40 × probes
p1/p2 — covering both block classes, all four routed storage kinds (Q4_K
gate/up; Q5_K/Q6_K down), the F32 and BF16 router rows, and the MTP block.

Comparison discipline: router indices exact (selection order, lowest-index
tie rule); weights and final FFN outputs under Δ = 1e-05 (the U2 oracle
band) with a first-divergence record naming index + both values. Zero FAIL;
any mismatch is a divergence receipt, never a tolerance-widened pass.

Component tier only: no token, logit, full-model, or device claim.

## Command

```bash
cd gradus
env FABER_LIBRARY_HOME=<workspace-root> \
  <workspace-root>/radix/target/debug/faber run --target fmir exempla/moe-probe -- \
  /Users/ianzepp/ai/models/Qwen3.6-35B-A3B-UD-Q4_K_M.gguf 10991392 \
  0b21525e972670ed59e1812e170b27c26355381f0656ecc4e25617ece7dac58b
```

## Artifact identity (operator evidence, never committed)

| Artifact | Bytes | SHA-256 | Data offset | Architecture |
| --- | ---: | --- | ---: | --- |
| `Qwen3.6-35B-A3B-UD-Q4_K_M.gguf` | 22,663,387,424 | `0b21525e972670ed59e1812e170b27c26355381f0656ecc4e25617ece7dac58b` | 10,991,392 | `qwen35moe` |

## Receipt (2026-08-22, burgus, direct on main)

- Revisions: gradus `b1ccfc8` (U6) + `bc63428` (U2) landed; gradus main
  moved to `fe041a6` during the unit; radix `e7f6cd05e` (clean HEAD,
  temp worktree build). `scripta/check-compile` green with the registered
  `moe-probe` block (the row's registration done_when half).
- Goldens: `fixtures/gguf/gguf-moe-goldens.json` (schema
  `gguf-moe-goldens-v1`, U2); probes:
  `fixtures/gguf/gguf-moe-probes.json` (schema `gguf-moe-probes-v1`).
- Δ = 1e-05 (`band.delta`).

Probe hashes (SHA-256 over the row's `u32_hex` join, first 16 hex):

| Layer | Probe | Hash prefix | rms_f64 |
| ---: | --- | --- | ---: |
| 0 | p1 | `7f9bb9ac5db0b66e` | 1.0000000215511209 |
| 0 | p2 | `53f52819a38c83d9` | 1.000000045211258 |
| 3 | p1 | `3ff8251592ec69f5` | 1.000000013926032 |
| 3 | p2 | `aa8b9aee22110317` | 0.9999999860494555 |
| 39 | p1 | `fbce86cf20b6fa79` | 1.0000000152826578¹ |
| 39 | p2 | `83c986e41259958f` | 0.9999999463449321 |
| 40 | p1 | `621c82172ea8ec4c` | 1.0000000073546578 |
| 40 | p2 | `c4ee5d5abdc533fe` | 1.0000000045870878 |

¹ recorded from the committed fixture row.

### Executed proof: GREEN (M2-G1, 2026-08-22, radix `6b2653a81`)

The octeti-indexing MIR runner debt was fixed at radix `6b2653a81`
("fix(mir): run windowed octeti reads"). Re-run at that tip (in-tree
`cargo build -p faber`; `--target` dropped — current `faber run` has no such
flag, `faber.toml` selects the target): **9 PASS lines, 0 FAIL**, all 8
probe rows exact indices with `first-divergence=none`, max-dev
`6.44e-08` ≪ Δ. Receipt:
[`docs/factory/production-ml-library/evidence/m2-g1-aggregate-receipt-6b2653a81.md`](../docs/factory/production-ml-library/evidence/m2-g1-aggregate-receipt-6b2653a81.md).
Historical block record follows.

### Historical block (pre-`6b2653a81`, resolved)

The real-file run was attempted twice (main-tree binary and a clean
radix-HEAD temp-worktree binary) and fails before admission output with:

```
error: invalid MIR: octeti index is not numerus
error: invalid MIR: conversion source type mismatch
```

This is NOT a moe-probe defect: the committed `exempla/gguf-materialize`
fixture-mode run fails bit-identically on clean radix HEAD + gradus at
`bc63428`, so the breakage predates this unit and lives in the shared
dequant/materialize byte-indexing path under the MIR runner. It matches a
known recorded runner-debt class — radix
`crates/exempla/src/exempla_e2e/expectations/runner.rs` pins
`conversio/octeti-endian.fab` as `RunnerFailureBucket::UnsupportedMir`
("octeti bridge files reach MIR then hit invalid-MIR (octeti index is not
numerus / element type resolution)"). radix main additionally does not
currently compile in-tree (foreign WIP `AnalyzeRequest` duplicate import),
so no newer binary exists to try.

First unblocking step for the Mind: route the octeti-indexing MIR runner
debt to its owning radix seat (EXEC-02 / FR-3 endian-read owners), then
re-run the closeout command above; the 8 expected PASS lines are
`PASS layer=<L> probe=<pN> indices=[…] weights=[…] first-divergence=none
max-dev=<≤Δ>` — observed values are then recorded here.

## Registration

`scripta/check-compile` checks this exemplum (`moe-probe real-file MoE
exemplum` block). This is the admitted MoE exempla M8-U1's done_when cites.
