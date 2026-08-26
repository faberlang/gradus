# MODEL-03 — hybrid SSM/attention state executed probe

This package is the application-owned adapter that proves the
`gradus:model/qwen35moe_state` surface against the pinned Qwen3.6
artifact and the pinned llama.cpp probe dump. It resolves the operator
artifact path and dump directory from argv, pins identity (digest +
length + data offset), runs `qwen35moe.admit`, derives and
`validate_schedule`s the trunk schedule, then executes all 40 trunk
layers through the module's `linear_attention`/`full_attention` for two
phases — the pinned 7-token prefill batch and one pinned one-token
decode at position 7 — comparing every attention-subblock tensor
(normed, qkv, z, beta/gate scalars, conv input/output/state, q/k/v conv,
core out, final gated output, residual, new recurrent state; Q/K/V/rope,
softmax path, gated output for full layers) against the probe dump at
every layer and window position, with a first-divergence record naming
layer + tensor + both values on any mismatch. After phase 0 it resets
the session and replays the prefill window one token at a time through
the step entry points, requiring exact equality with the batched
per-layer outputs (reset/replay determinism).

Comparison discipline: every tensor is gated on Δ = 3.538e-4, the band
derived by the trials oracle (`m3-ssm-attention-oracle.py`) as
clamp(10R, 1e-5, 5e-4) with R = 3.538e-5 measured f32-vs-f64 over the
same replay. Zero FAIL; any mismatch is a divergence receipt, never a
tolerance-widened pass.

Component tier only: no token, logit, MoE, full-model, or device claim.
The probe dump is produced by the trials-owned llama.cpp probe (see
`trials/tools/qwen35moe-probe/`); gradus owns no oracle harness.

## Command

```bash
cd gradus
env FABER_LIBRARY_HOME=<workspace-root> \
  <workspace-root>/radix/target/debug/faber run exempla/qwen35moe-layer-probe -- \
  /Users/ianzepp/Ai/models/Qwen3.6-35B-A3B-UD-Q4_K_M.gguf 10991392 <probe-dump-dir>
```

`faber.toml` pins `target = "fmir"`; the current CLI selects the target
from the package manifest (no `--target` flag on `run`).

## Artifact identity (operator evidence, never committed)

| Artifact | Bytes | SHA-256 | Data offset | Architecture |
| --- | ---: | --- | ---: | --- |
| `Qwen3.6-35B-A3B-UD-Q4_K_M.gguf` | 22,663,387,424 | `0b21525e972670ed59e1812e170b27c26355381f0656ecc4e25617ece7dac58b` | 10,991,392 | `qwen35moe` |

Pinned probe window: prefill tokens `760,3177,314,11751,369,279,6511`
(add_bos off), decode token `314` (greedy under the pinned
configuration); probe run with `-fa off` (see the trials probe README —
flash attention deviates above any lawful band).

## Receipt

See `docs/factory/production-ml-library/evidence/` for the executed
receipt (revisions, per-phase worst deviations, replay verdict, oracle
gate).
