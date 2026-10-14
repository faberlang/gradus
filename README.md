# Inferentia

Inferentia is a local-first GGUF inference server written in Faber.

The repository currently contains the smallest viable Faber CLI shell and the
master development campaign. Model loading and HTTP serving begin in campaign
stage I1.

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

From this repository — the package imports the `gradus:` provider (Norma is
embedded in the `faber` binary), so compilation needs `--library-home` naming
the directory that holds the gradus checkout (`<home>/gradus/src`), a
current workspace `faber` binary (the PATH `faber` lags main and fails package
resolution with `PKG001`), and an absolute input path. `[paths] library_home`
in `faber.toml` is the manifest form of the same setting. No `FABER_*`
environment variable is read.

```sh
CONTAINER="$(cd .. && pwd)"
FABER="$CONTAINER/radix/target/debug/faber"
"$FABER" check --library-home "$CONTAINER" "$(pwd)"
"$FABER" build --library-home "$CONTAINER" "$(pwd)"
```

While the container still carries a stale `norma/` checkout beside `gradus/`,
that checkout shadows the embedded Norma and package resolution fails
(`PKG001` naming `norma/src/http/...`); use a library home that holds only a
`gradus` link.

In a `worktrees/<lane>/` packet the same form holds with the lane root as the
container; if the lane's `radix/target/debug/faber` is not built, point
`FABER` at a built workspace binary.

Program arguments after `--` start at the first operand (the program name is
not an argument): `faber run --device metal --library-home "$CONTAINER"
inferentia -- live --backend metal --model <GGUF>`. Inferentia has no CPU
backend of its own; the same kernels run on the CPU under
`faber run --device cpu` (several cores) or `--device reference` (one core,
the oracle).

The CLI has no serving command yet. See the
[Inferentia master campaign](docs/factory/inferentia/CAMPAIGN.md) for the staged
delivery plan and completion gates.
