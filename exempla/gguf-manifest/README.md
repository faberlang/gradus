# GGUF-A1a executable parser proof

This package is the executable bounded-corpus proof for the Gradus
`gradus:model/gguf_manifest` foundation. Its source builds synthetic GGUF v3
header/metadata/tensor-table prefixes in memory, calls `parse`, accesses
returned manifest/tensor fields, and prints a PASS/FAIL line with the observed
result for each named case. It performs no filesystem read, download, mmap,
host-reader call, or model-payload allocation.

The committed files under `fixtures/gguf/` are deterministic generator/oracle
artifacts. This package does not claim to have parsed those binary files.

## Evidence boundary

The package is intended to run through package MIR with the lane-local Radix
binary. The receipt below is the only executable claim for A1a. Co-located
`src/model/*.proba` files remain structural/typecheck evidence; the focused
`faber test` route is attempted separately and is currently blocked by the
imported-library provider seam.

## Receipt

Command, from the Hand packet:

```text
cd /Users/ianzepp/work/faberlang/worktrees/hand-1/gradus
env FABER_LIBRARY_HOME=/Users/ianzepp/work/faberlang/worktrees/hand-1 \
  /Users/ianzepp/work/faberlang/worktrees/hand-1/radix/target/debug/faber \
  run --target fmir exempla/gguf-manifest
```

Observed result (2026-08-12): exit `1`. The package reaches FMIR image
execution but emits 23 conversion diagnostics before the `incipit` entrypoint;
therefore no case result is observed and A1a is not executable-complete.

```text
error: conversion source type mismatch
error: conversion source type mismatch
error: conversion source type mismatch
error: conversion source type mismatch
error: conversion source type mismatch
error: conversion source type mismatch
error: conversion source type mismatch
error: conversion source type mismatch
error: conversion source type mismatch
error: conversion source type mismatch
error: conversion source type mismatch
error: conversion source type mismatch
error: conversion source type mismatch
error: conversion source type mismatch
error: conversion source type mismatch
error: conversion source type mismatch
error: conversion source type mismatch
error: conversion source type mismatch
error: conversion source type mismatch
error: conversion source type mismatch
error: conversion source type mismatch
error: conversion source type mismatch
error: conversion source type mismatch
fmir image execution failed
```

The source-level command `faber check exempla/gguf-manifest` is green, and
`scripta/check-compile` includes that package check. This receipt is a compiler
boundary diagnosis, not an executed parser claim. The committed binary
fixtures remain generator/oracle artifacts and are not claimed parsed.

The requested compiled fallback was also attempted:

```text
env FABER_LIBRARY_HOME=/Users/ianzepp/work/faberlang/worktrees/hand-1 \
  /Users/ianzepp/work/faberlang/worktrees/hand-1/radix/target/debug/faber \
  run --target rust exempla/gguf-manifest
```

It exited `1` during generated Rust compilation, before the package ran. The
first generated-code divergence was `src/main.rs:9:30`, where `F_DIGEST` was
emitted as `pub const F_DIGEST: String = "..."` and Rust required an owned
`.to_string()` value. The next generated errors were the `numerus`-to-`u8`
list literals at `src/main.rs:13` and `src/main.rs:25`, followed by imported
error/result lowering mismatches and an `Option<MetadatumGguf>` projection at
`src/main.rs:1872`. The final compiler summary was:

```text
error: could not compile `gguf-manifest` (bin "gguf-manifest") due to 13 previous errors; 36 warnings emitted
error: cargo build exited with status exit status: 101
```

This route therefore supplies no executable parser receipt either; the
generated Rust failures are a Radix/toolchain residual outside this Gradus
path-limited repair.
