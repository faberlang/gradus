# Inferentia Agent Guide

**Workspace work mode.** Ordinary development is **direct** in this
checkout on `main`. Worktree packets under `../worktrees/<lane>/` are
optional Tugboat isolation. Do not stand up lanes unless the operator
asked. Container law: [`../AGENTS.md`](../AGENTS.md).

## Project

Inferentia is a separate Faber application product. It serves GGUF language
models through a local CLI and HTTP API.

Treat `faber.toml`, `README.md`, the campaign, and live source as the source of
truth. When they disagree, working code and observed behavior win.

## Ownership boundaries

- Keep product policy in this package.
- Put reusable ML semantics in Gradus only when Inferentia proves the need.
- Put compiler and Faber build-tool work in private Radix.
- Put physical effects behind the appropriate Host provider.
- Do not move Inferentia commands into the generic Faber CLI or public Faber
  target API packages.
- Do not make `llama.cpp` a production dependency. It is a comparison oracle.
- Keep deployment and machine provisioning in a separate campaign.

## Development stance

- Use Faber for application and request-policy code.
- Fail closed on unsupported GGUF architecture, quantization, tokenizer, or
  metadata combinations.
- Prefer one verified model row before generalizing.
- Add a second caller or model row before extracting abstractions.
- Preserve foreign changes in every sibling repository.
- A campaign or goal is planning evidence, not proof that code shipped.

## Validation

Run the narrowest useful proof first. The commands below were checked on
2026-11-05 (radix `3e8dc5a9e6`, Gradus `79036e3`). The package imports the
`gradus:` provider (Norma is embedded in the binary), so every command needs
`--library-home` naming a directory that holds a `gradus` link, a radix-built
`faber` (the PATH `faber` lags main), and an absolute input path. No `FABER_*`
environment variable is read. The package carries no `faber.lock`, so it works
from any checkout or worktree. A `norma/` checkout beside `gradus/` shadows the
embedded Norma; use a library home that holds only `gradus`.

```sh
FABER=<radix>/target/release/faber       # cargo build --release -p faber, in radix
LIBRARY_HOME=<dir with a gradus link>
INF="$(pwd)"
"$FABER" check --library-home "$LIBRARY_HOME" "$INF"                    # about 2 s
"$FABER" test  --device reference --library-home "$LIBRARY_HOME" "$INF" # 132 package tests, about 4 s
```

The manifest names no build target, like the corpus simulations; `faber run`
runs the source on the device named by `--device`. The Rust target refuses the
decode launches' run-time tensor shapes.

Inferentia keeps no CPU backend: CPU inference is the same kernels under
`faber run --device cpu`. Inference never runs on the MIR interpreter:
`--device reference` is a correctness oracle only, and every other run refuses
an interpreter landing.

Engine rule (operator, 2026-11-05): inference never runs on the MIR
interpreter. Faber has no interpreter fallback: `live` and `serve` run their host
half on the Cranelift JIT, and a host half or kernel that would land on the
interpreter refuses with exit 69 (`ENGINE001`/`ENGINE002`). Only `--device
reference` runs the interpreter. A refusal names the gap to close.

Token-correctness run (strict through the manifest; about 16 s on an M5 Max, most of it model load):

```sh
"$FABER" run --device metal --library-home "$LIBRARY_HOME" "$INF" -- \
    live --model <dir>/SmolLM2-360M-Instruct-f32.gguf --max-tokens 40 --ignore-eos --trace
```

It must print `ids=30 198 198 788 451 6330 28 260 33197 476 269 18 4271 288 260
11531 476 29343 1270 378 33197 476 269 18 314 253 1502 282 2700 791 33197 28
527 314 804 288 3386 288 253 1678`, the llama.cpp greedy continuation of the
frozen prompt.

The gate packages under `tests/` (`admission-gate`, `model-gate`,
`generate-gate`) run as `"$FABER" run --device reference --library-home
"$LIBRARY_HOME" "$INF/tests/<gate>" -- <model>`. `tests/admission-gate/run.sh`
and `tests/process-exit/run.sh` still expect a native `target/debug/inferentia`
binary from the retired Rust build and do not run. `tests/oracle/*.py` take the `faber` and library home as arguments.

Streaming proof (need 86f2d64a): `/generate` with `Accept: text/event-stream` writes
each token to the open response as it is chosen. `python3 tests/oracle/a1_stream_test.py
--faber <faber> --device <reference|cpu|metal> --library-home <home>` timestamps every
SSE event and fails if the tokens arrive in one burst or the first token is not ahead of
the `done` event; `--selftest` runs its parser and verdict on synthetic streams without a
model. A step costs about 3.5 minutes on `--device reference` with a release `faber`
(measured 2026-10-14; a debug `faber` did not finish one step in 13 minutes), so the
3-token reference run takes about 10 minutes.

Measured package-suite baseline (2026-11-05, release `faber` from radix `3e8dc5a9e6`):
`faber test --device reference <absolute-package-path>` ran 132 tests in 4.2 s wall
(an earlier suite took 157.74 s on 2026-10-03). This measures the MIR package suite,
not model serving or GPU throughput.

Model-serving stages must record the exact model path, size, hash, GGUF
metadata, command, request fixture, observed output, and comparison oracle.
Do not start long model or integration runs without making their expected cost
clear first.

## Measured baselines

A1 oracle path, `faber run --device metal inferentia -- live --backend metal`, eog case,
SmolLM2-360M-Instruct-f32 (1.45 GB), quiet M5 Max, release `faber`, 3 runs
(2026-10-08; radix `91e1b5947`, inferentia `2acf1cead`, gradus `27b282921`).
Full analysis and the ranked list: `../radix/docs/factory/gpu-reset/a1-perf-baseline.md`
(open defect F-33).

| Phase | min (s) | median (s) |
| --- | --- | --- |
| Front end (analyze 5.7 + MIR lowering/validation about 58) | 64.8 | 64.8 |
| Admit + digest + manifest + tokenizer | 35.3 | 35.5 |
| Tokenize + `port_resident` (second tokenizer build) | 4.7 | 4.7 |
| Load (third manifest parse + second digest + tensors 0.5) | 19.5 | 19.5 |
| Prefill, 9 tokens (includes first-use weight upload) | 5.1 | 5.2 |
| Wall | 129.6 | 130.0 |

Decode (64-token run, instrumented): 187 ms/token (5.35 tok/s), 676 launches/token;
about 44 percent is the interpreted logits scan, about 43 percent of the main thread
waits on Metal command-buffer completion triggered by buffer release. Peak RSS 7.4 GB.
Digest: 5.5 s per pass (software SHA-256, 261 MB/s) against 0.76 s with hardware SHA.

Update 2026-10-09 (A1RECHECK, release `faber`, radix `2d770fb48`, gradus `5fde315`,
inferentia `9f2c7b2`; the other tables above are the 2026-10-08 starting point):

| Phase (eog case) | s |
| --- | --- |
| Front end | 11.1 (6.9 on the continuation run; varies by run) |
| Admit + digest + manifest + tokenizer | 2.0 |
| Load | 1.0 |
| Prefill (9 tokens) | 3.5 |
| Wall | 17.8 |

Continuation (64 tokens): wall 21.4 s, decode 6.7 s (about 105 ms/token averaged by the
oracle script; the instrumented non-trace figure was 72 ms/token). Serve smoke 20.2 s
(health ready at 10.1 s). Port-load gate 16.5 s. Peak RSS 7.4 GB. The admit drop
(18.3 -> 2.0 s) is the GGUF manifest byte helpers (BULKBYTES) plus the hardware SHA-256
and the single manifest parse. What remains is the front end (10 s) and prefill.
