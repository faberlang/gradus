# Inferentia

Inferentia is a local-first GGUF inference server written in Faber.

The repository holds the Faber CLI (`live` one-shot generation and `serve` over
HTTP), the SmolLM2-360M F32 decode path on the Gradus launches, its tests, and
the master development campaign. One model row is verified:
`SmolLM2-360M-Instruct-f32.gguf` (1,449,071,040 bytes, sha-256
`07735177a3542cbc0b0665051ce1922b55c4c9698de65131e65f2aea87a935e0`).

Source uses Faber's English reader locale through the canonical `[locale]`
manifest section introduced by the current Faber release line.

## Product boundary

Inferentia owns the user-facing inference product: configuration, CLI and API
contracts, request lifecycle, scheduling, streaming, cancellation, and
observability.

It consumes language and runtime capabilities from the Faberlang stack:

- Gradus owns model and machine-learning semantics.
- Faber owns application build and package composition.
- Radix owns compilation.
- Hosts own physical effects such as HTTP, files, clocks, and accelerators.

`llama.cpp` may be used as a reference oracle during development. It is not a
production dependency of Inferentia. Deployment is a separate work stream.

## Current commands

Checked 2026-11-05 against radix `3e8dc5a9e6` and Gradus `79036e3` (the
`github/peer/main` tips). They are Faber product commands, run from a radix
build rather than the `faber` on `PATH` (which lags main):

```sh
FABER=<radix>/target/release/faber        # cargo build --release -p faber, in radix
LIBRARY_HOME=<dir>                        # a directory whose `gradus` entry is the Gradus checkout
INF="$(pwd)"                              # absolute package path (this repository)
MODEL=<dir>/SmolLM2-360M-Instruct-f32.gguf

"$FABER" check --library-home "$LIBRARY_HOME" "$INF"
"$FABER" test  --device reference --library-home "$LIBRARY_HOME" "$INF" # 132 package tests, about 4 s
"$FABER" run --device metal --library-home "$LIBRARY_HOME" "$INF" -- \
    live --model "$MODEL" --max-tokens 40 --ignore-eos --trace
```

- `--library-home` names the directory that holds `gradus` (the library source
  is `<home>/gradus/src`); Norma is embedded in the binary. The package has no
  `faber.lock` and no `[dependencies]` table, so it builds from any checkout or
  worktree. While a stale `norma/` checkout sits beside `gradus/` it shadows
  the embedded Norma, so use a home that holds only a `gradus` link.
- The manifest names no build target, like the corpus simulations: `faber run`
  runs the source on the device named by `--device`. (`target = "rust"` no
  longer checks: the Rust target refuses the decode launches' run-time tensor
  shapes, `CODEGEN001`.)
- Program arguments follow `--` and start at the first operand. Subcommands:
  `live` (one-shot generation: `--model`, `--prompt`, `--max-tokens`,
  `--ignore-eos`, `--trace`) and `serve` (HTTP: `--model`, `--host`, `--port`,
  `--max-tokens`, `--max-prompt`, `--context`, `--seed`, `--log-level`,
  `--expected-digest`). `--backend metal` is the only accepted value and names
  the kernel route; the device is the `faber run --device` choice. Inferentia
  has no CPU backend of its own: `--device cpu` (several cores) or
  `--device reference` (one core) run the same kernels.
- Engine: `live` and `serve` currently run their host half on the MIR
  interpreter (the run prints one `ENGINE001` line), because the Cranelift JIT
  declines it. `--strict-engine` therefore refuses the run (exit 69) until
  those JIT gaps close. A run on the interpreter is a correctness run, never a
  timed one. Timed runs use `--strict-engine`.

Token correctness: the `live` command above must print the same 40 ids as
llama.cpp (greedy): `30 198 198 788 451 6330 28 260 33197 476 269 18 4271 288
260 11531 476 29343 1270 378 33197 476 269 18 314 253 1502 282 2700 791 33197
28 527 314 804 288 3386 288 253 1678`.

See the [Inferentia master campaign](docs/factory/inferentia/CAMPAIGN.md) for
the staged delivery plan and completion gates.
