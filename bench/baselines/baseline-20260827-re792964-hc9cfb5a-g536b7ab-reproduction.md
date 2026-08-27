# Reproduction receipt — baseline-20260827-re792964-hc9cfb5a-g536b7ab (GB-U5)

reproduced 2026-08-27T17:17:24Z · full-run wall 21.1 min (17:17:23Z → 17:38:29Z) · RUN_EXIT 0 · GATE_EXIT 0 (PASS, default 10% threshold) · harness `scripta/bench` invoked from the pinned gradus worktree at `536b7ab941d544cf3efb2dc0a137ce1c5a901aa3` — the recorded `gradus_sha`, pinned as **harness-complete** by the GB-U4 ordering invariant before the baseline was written (requirement 2: reproduction from the recorded triple, not HEADs)

## Materialization provenance (fresh scratch, this run)

- scratch root `/Users/ianzepp/work/faberlang/worktrees/gb-5/.bench/gradus/e792964-c9cfb5a-536b7ab/` — materialized by `bench materialize` at the exact recorded SHAs (packet root `radix`/`hosts` symlinks per the sanctioned gb-3b/gb-3c/gb-4 scaffolding pattern)
- worktree HEADs verified post-checkout: radix `e7929640df7fe64dc1992b83227f7f3d6ad3e052` · hosts `c9cfb5afd149a0a0e7c0dfe66cf449ae53326f40` · gradus `536b7ab941d544cf3efb2dc0a137ce1c5a901aa3` — identical to the baseline `metadata.triple`
- release faber rebuilt inside the pinned radix worktree (`cargo build --release -p faber`, 34.6s, own target dir)
- reproduction command (from the pinned worktree — done_when e):

```
$ /opt/homebrew/opt/python@3.13/bin/python3.13 /Users/ianzepp/work/faberlang/worktrees/gb-5/.bench/gradus/e792964-c9cfb5a-536b7ab/gradus/scripta/bench.py run --scratch /Users/ianzepp/work/faberlang/worktrees/gb-5/.bench/gradus/e792964-c9cfb5a-536b7ab --stage full --out /tmp/gbu5-repro/full.json
```

## Hashes (identical triple — baseline vs reproduction)

| repo | baseline (`metadata.triple`) | reproduction | equal |
|---|---|---|---|
| radix | e7929640df7fe64dc1992b83227f7f3d6ad3e052 | e7929640df7fe64dc1992b83227f7f3d6ad3e052 | ✓ |
| hosts | c9cfb5afd149a0a0e7c0dfe66cf449ae53326f40 | c9cfb5afd149a0a0e7c0dfe66cf449ae53326f40 | ✓ |
| gradus | 536b7ab941d544cf3efb2dc0a137ce1c5a901aa3 | 536b7ab941d544cf3efb2dc0a137ce1c5a901aa3 | ✓ |

## Environment (side by side — done_when a: identity + power class equal)

| field | baseline (16:50:33Z) | reproduction (17:17:24Z) | equal |
|---|---|---|---|
| hostname | burgus.local | burgus.local | ✓ |
| machine_model | Mac17,7 | Mac17,7 | ✓ |
| cpu | Apple M5 Max | Apple M5 Max | ✓ |
| cores | 18 | 18 | ✓ |
| memory | 128 GiB | 128 GiB | ✓ |
| os | macOS 26.5.2 (25F84) | macOS 26.5.2 (25F84) | ✓ |
| kernel | 25.5.0 | 25.5.0 | ✓ |
| arch | arm64 | arm64 | ✓ |
| rustc | rustc 1.97.1 (8bab26f4f 2026-07-14) (Homebrew) | rustc 1.97.1 (8bab26f4f 2026-07-14) (Homebrew) | ✓ |
| power_state (start) | ac (pmset-verified; 58% charged) | ac (pmset-verified; 84% charged) | class ✓ |
| **power_class (run summary)** | **ac** | **ac** | ✓ |
| stage / protocol | full (4), 3 warmups / 10 samples | full (4), 3 warmups / 10 samples | ✓ |

Reproduction power evidence: start-of-run `pmset -g batt` → `Now drawing from 'AC Power' … 84%; charging`; every result row probed `power=ac`; `metadata.power_class: ac` (unanimous).

## Per-label side-by-side (medians + t/s, gate quantity = `median_ms`)

| label | baseline median_ms | repro median_ms | Δ median_ms | baseline t/s | repro t/s | verdict (default 10%) |
|---|---|---|---|---|---|---|
| carrier.elementwise.add.f32.320x960 | 19381.121 | 18935.353 | −2.30% | 126815.346193 el/s | 129789.030558 el/s | BETTER |
| carrier.reduce.sum.f32.320x960 | 16176.562 | 16176.298 | −0.00% | 303847.326547 el/s | 303851.97063 el/s | BETTER |
| gemv.f32.320x960 | 7561.951 | 7606.898 | +0.59% | 1299982.341941 macs/s | 1292304.916527 macs/s | PASS |
| block.matmul.f32.t8.d960.f2560 | 15797.729 | 15882.494 | +0.54% | 1244534.775775 macs/s | 1237891.888324 macs/s | PASS |
| decode.attention.row76.d960 | 19251.359 | 19435.640 | +0.96% | 0.415555 tok/s | 0.411615 tok/s | PASS |
| prefill.attention.rows36.l76.d960 | 17622.166 | 17546.163 | −0.43% | 16.343053 tok/s | 16.413854 tok/s | BETTER |
| check.library.compile | 888.104 | 824.886 | −7.12% | 1.126023 passes/s | 1.21229 passes/s | BETTER |

All 7 labels `ok=true`, none capped; worst regression +0.96% (decode.attention.row76.d960) — within the default 10% threshold; 4 labels better.

## Gate (sanity — the gate run itself)

`scripta/bench gate /tmp/gbu5-repro/full.json` against the committed baseline (auto-discovered newest stem), delegated to `../radix/scripta/check-benchmark-regression.py`:

```
bench: gate candidate /tmp/gbu5-repro/full.json
bench: gate baseline  .../gradus/bench/baselines/baseline-20260827-re792964-hc9cfb5a-g536b7ab.json
bench: comparable — delegating to the radix checker
… +0.54% PASS · −2.30% BETTER · −0.00% BETTER · −7.12% BETTER · +0.96% PASS · +0.59% PASS · −0.43% BETTER
Result: PASS  (no regression exceeds threshold)
exit 0
```

## Receipt laws

- no baseline file modified — `baseline-20260827-re792964-hc9cfb5a-g536b7ab.{json,md}` untouched (GB-U4 property preserved)
- no threshold tuning (gpu-lessons L21): default 10% throughout; no `BENCH_REGRESSION_THRESHOLD` override
- reproduction is `--stage full` (the only gate-comparable shape; goal §Stage ladder) from the pinned gradus worktree at the recorded harness-complete sha
- scratch worktree torn down via `bench clean` after the gate (GB-U1 teardown law; registrations pruned)
