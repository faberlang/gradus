# REF-01-U1.10 — Qwen2.5-0.5B prefill-logit receipt (compiled route)

This package is the U1.10 consumer: admit the operator-local
`Qwen2.5-0.5B-Instruct-Q4_K_M.gguf` artifact, materialize stored-weight
views through the bounded slice materializer, run the U1.8
`gradus:model/dense` `forward` graph, and print the gi0 prefill-logit
receipt. The application owns the path. Gradus never receives the path
or a whole-model byte list.

The receipt tier is the compiled route (`faber build --target rust`,
then execute the printed binary). llvm-host is the named fallback. The
MIR stepper is not the receipt-tier engine.

## Resume stop (2026-08-17)

U1.10 resume on handle `6ecefd40` / packet hand-13. The named root
cause (`CODEGEN001` on `dense_qwen2` def-id 4127) is present as source
at readable radix `b919052f0` (`d66e1f93e` — register imported union
variants at rust emit). That tree does not produce a packet `faber`
binary. Stop rule: new diagnostic → record exactly, stop. Numerics
were not tuned. TARGETLANE001 was not weakened. The rust-target emit
was not reached. The GGUF file was not executed.

### Packet faber rebuild (blocked)

From the Hand packet:

```text
cd /Users/ianzepp/work/faberlang/worktrees/hand-13/radix
cargo build -p faber
```

and the slimmer:

```text
cargo build -p faber --no-default-features --features hir-rust
```

Both fail the same way. Exact diagnostic:

```text
error[E0432]: unresolved import `faber_hir_rust::ImportedEnumVariantInfo`
  --> crates/radix-program/src/rust_target.rs:17:76
   |
17 |     remap_function_param_info, remap_type_id_with_nominal_defs, FxHashMap, ImportedEnumVariantInfo,
   |                                                                            ^^^^^^^^^^^^^^^^^^^^^^^ no `ImportedEnumVariantInfo` in the root

error: could not compile `radix-program` (lib) due to 1 previous error
```

`ImportedEnumVariantInfo` exists on `radix_hir_rust` (`import_params.rs`,
re-exported from `module.rs`). `radix_module::codegen::rust` re-exports
`ImportedEnumVariantExport` but not `ImportedEnumVariantInfo`.
`faber_hir_rust` re-exports the `radix_module::codegen::rust` façade and
therefore also lacks the type. `radix_program::rust_target` imports the
type from `faber_hir_rust`. Radix is readable-only in this packet; the
two façade `pub use` lines were not patched.

No same-revision `faber` binary exists. The packet
`target/debug/faber` is the pre-fix 1.7.0 binary (mtime 2026-08-17
19:39, before `d66e1f93e` 20:40). Main `radix/target/debug/faber` is
older still (17:26). Those binaries rediscover `CODEGEN001`; they were
not used for rust-target emit on this resume.

Toolchain: rustc 1.97.1 (8bab26f4f 2026-07-14) Homebrew, cargo 1.97.1
(c980f4866 2026-06-30). Host: Darwin 25.5.0 arm64.

### Intended rust-target command (not reached)

```text
cd /Users/ianzepp/work/faberlang/worktrees/hand-13/gradus
env FABER_SUPPORT_PATH_OVERRIDE=/Users/ianzepp/work/faberlang \
  FABER_LIBRARY_HOME=/tmp/faber-hand-13-libhome \
  /Users/ianzepp/work/faberlang/worktrees/hand-13/radix/target/debug/faber \
  build --target rust exempla/dense-prefill-qwen2
```

`FABER_LIBRARY_HOME` is a directory with `gradus` → this packet and
`norma` → `/Users/ianzepp/work/faberlang/norma`. No binary path was
printed. The binary was not executed.

### Structural gates that did pass

`faber check exempla/dense-prefill-qwen2` exits 0 (warnings only:
`LOCALE002`, `WARN018`). `./scripta/check-source` exits 0.
`./scripta/check-compile` exits 0 (pre-fix packet `faber` 1.7.0, which
is sufficient for `faber check`). `git diff --check` silent on the
unit paths.

This is not an executed prefill-logit receipt. No Gradus logits, no
first-divergence position, no Metal/CUDA claim, no payload-residency
claim.

Repair belongs to the radix hir-rust façade re-export of
`ImportedEnumVariantInfo` through `radix_module::codegen::rust` and
`faber_hir_rust`, then a packet `faber` rebuild at that revision.

## Prior stop (2026-08-17, 31df6a9)

The first U1.10 attempt used readable radix `7863624e2`. Packet
`cargo build -p faber` failed then on `E0004` non-exhaustive
`MirCollectionOp`. The rust-target emit with the same-revision 1.7.0
binary failed:

```text
error[CODEGEN001]: /tmp/faber-hand-13-libhome/gradus/src/model/dense_qwen2.fab: code generation failed: internal: definition id 4127 could not be resolved during code generation
compilation failed
```

llvm-host fallback: `error[PKG001:llvm_emission_failed]`. That
`CODEGEN001` is the defect `d66e1f93e` / `b919052f0` aimed to close.
This resume could not load that compiler into a runnable `faber`.

## Pinned row facts (not a comparison)

| Field | Value |
| --- | --- |
| Comparison policy | gi0-numeric-contract v1.0.0: finite gate, top-1 exact, top-5 overlap ≥ 4/5, Δ=1e-5 band, window positions 0..16 |
| Model | `Qwen2.5-0.5B-Instruct-Q4_K_M.gguf` |
| Bytes | 397,808,192 |
| SHA-256 | `6eb923e7d26e9cea28811e1a8e852009b21242fb157b26149d3b188f3a8c8653` |
| Data offset | 5,948,480 |
| Architecture | `qwen2` (24/14/2/64/896, vocab 151936, tied `lm_head`) |
| Prompt | `The capital of France is Paris and the capital of Japan is Tokyo. The next city` |
| Prompt SHA-256 | `973c9c7fbb1f277298e3525d09454a05af4754b670715247a12c7fa32a390c45` |
| Pinned tokenizer ids (llama-tokenize 10150 `dee2a846b`, `--no-bos`) | `[785, 6722, 315, 9625, 374, 12095, 323, 279, 6722, 315, 6323, 374, 26194, 13, 576, 1790, 3283]` |
| Backend (declared) | CPU/reference |
| Hardware/OS | Darwin 25.5.0 arm64 |
| Gradus | `57404ea` (packet base; this commit records the resume stop) |
| Radix | `b919052f0` (readable; `d66e1f93e` on tree; `faber` rebuild E0432) |
| Faber | no same-revision binary; stale packet 1.7.0 is pre-`d66e1f93e` |
| Comparator binary | `/opt/homebrew/Cellar/llama.cpp/10150/bin/llama-server` SHA-256 `e5c153a1237e1c8e14ce0721d9afba4fd07936c7dc17dc7bd156d4dbe454952a`, version 10150 (`dee2a846b`) |

The real file carries `attn_q.bias` / `attn_k.bias` / `attn_v.bias`.
The U1.8 surface synthesizes zero biases and does not resolve those
tensors. That architecture fact is recorded; it was not used to change
the surface (stop rule: do not tune).

Comparator-only observation from the first attempt (not a Gradus
comparison — no candidate logits): `/completion` on the pinned token
array, `n_predict=1`, `n_probs=5`, `temperature=0`, `seed=42`, CPU
(`--n-gpu-layers 0`), ephemeral port 8310 (not 18173 / 59414),
generation position 0 top-1 token id 304 (` in`).

## Intended executed command (blocked)

```text
<printed-binary> \
  /Users/ianzepp/ai/models/Qwen2.5-0.5B-Instruct-Q4_K_M.gguf \
  5948480 \
  6eb923e7d26e9cea28811e1a8e852009b21242fb157b26149d3b188f3a8c8653
```
