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

The package runs through package MIR with the hand-2 lane Radix binary. The
receipt below is the only executable claim for A1a. Co-located
`src/model/*.proba` files remain structural/typecheck evidence; focused
`faber test` attempts remain blocked by the imported-library provider seam
(artifact `sym#20`, manifest `sym#113`).

## Receipt

Command, from the Hand packet:

```text
cd /Users/ianzepp/work/faberlang/worktrees/hand-1/gradus
env FABER_LIBRARY_HOME=/Users/ianzepp/work/faberlang/worktrees/hand-1 \
  /Users/ianzepp/work/faberlang/worktrees/hand-2/radix/target/debug/faber \
  run --target fmir exempla/gguf-manifest
```

Observed result (2026-08-12): exit `0`; 23 PASS lines and 0 FAIL lines. The
package executes only deterministic bounded in-source corpora. It does not
parse the committed binary fixtures, read a real file or tensor payload, or
claim model inference.

```text
llama-default-and-unknown-metadata: PASS observed=llama/32/4/0
qwen2-custom-alignment-rank3-q4k: PASS observed=qwen2/64/256/12
qwen35moe-mixed-unknown-layout: PASS observed=qwen35moe/128/2/999
unknown-layout-inspectability: PASS observed=ok
malformed-magic: PASS observed=not a GGUF file — bad magic
malformed-version: PASS observed=unsupported GGUF version: 2
truncation: PASS observed=truncated GGUF header
wrong-alignment-wire-kind: PASS observed=general.alignment must use GGUF UINT32 wire kind
invalid-alignment-value: PASS observed=general.alignment must be a positive power of two
malformed-bool: PASS observed=malformed GGUF bool value
malformed-string: PASS observed=GGUF string is not valid UTF-8
duplicate-metadata: PASS observed=duplicate GGUF metadata key: general.architecture
duplicate-tensor-name: PASS observed=duplicate GGUF tensor name: same
dimension-ceiling: PASS observed=tensor dimension is outside the bounded range
element-overflow: PASS observed=tensor element count exceeds the bounded range
rank-zero: PASS observed=tensor rank must be at least one
first-dimension-q4k-block: PASS observed=tensor first dimension is not a complete GGML block
known-offset-out-of-file: PASS observed=known GGML tensor range exceeds the artifact
unknown-offset-out-of-file: PASS observed=GGML tensor offset exceeds the artifact
checked-offset-overflow: PASS observed=checked offset addition overflow
known-range-overlap: PASS observed=known GGML tensor ranges overlap
extra-data-region-byte: PASS observed=bounded GGUF corpus contains bytes from the data region
identity-mismatch: PASS observed=content identity does not match the supplied artifact length
```

The source-level command `faber check exempla/gguf-manifest` is green, and
`scripta/check-compile` includes that package check. This is an executed
bounded-parser receipt, not a real-file, committed-fixture, tensor-payload, or
inference claim. The committed binary fixtures remain generator/oracle
artifacts and are not claimed parsed.

## Separate compiled-Rust route

The earlier compiled fallback used the hand-1 Radix binary and remains a
separate toolchain residual; it is not needed for the package-MIR receipt:

```text
env FABER_LIBRARY_HOME=/Users/ianzepp/work/faberlang/worktrees/hand-1 \
  /Users/ianzepp/work/faberlang/worktrees/hand-1/radix/target/debug/faber \
  run --target rust exempla/gguf-manifest
```

That attempt exited `1` during generated Rust compilation, before the package
ran. The first generated-code divergence was `src/main.rs:9:30`, where
`F_DIGEST` was emitted as `pub const F_DIGEST: String = "..."` and Rust
required an owned
`.to_string()` value. The next generated errors were the `numerus`-to-`u8`
list literals at `src/main.rs:13` and `src/main.rs:25`, followed by imported
error/result lowering mismatches and an `Option<MetadatumGguf>` projection at
`src/main.rs:1872`. The final compiler summary was:

```text
error: could not compile `gguf-manifest` (bin "gguf-manifest") due to 13 previous errors; 36 warnings emitted
error: cargo build exited with status exit status: 101
```

The generated Rust failures are a Radix/toolchain residual outside this Gradus
path-limited repair; the package-MIR bounded-parser receipt above is green.
