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

## GATE 8 (2026-08-18)

**Verdict: COMPILE CLEAN — execution STOP.** Handle `0530f8bf` / packet
`test-1`. Writable radix `5088c4397` includes ER-23 (reborrow fn values
once). Packet `cargo build -p faber` is green. `faber build --target rust`
printed the binary (`Finished dev` in 1.19s, 0 rustc errors, 616
warnings). Classified families (258/248, 65, N4, N5, E0275) did not
reproduce. Execution of the printed binary panicked on the first
`solum.read_range` of the GGUF table prefix: `failable call failed:
"sermo materialization failed"`. No logits. Stop rule: new diagnostic →
record exactly, stop. Numerics were not tuned. TARGETLANE001 was not
weakened (`[build] target = "fmir"` stays).

### Packet faber rebuild (green)

From the test packet:

```text
cd /Users/ianzepp/work/faberlang/worktrees/test-1/radix
cargo build -p faber
```

Exit 0 in 4.21s. Binary
`/Users/ianzepp/work/faberlang/worktrees/test-1/radix/target/debug/faber`
(`faber 1.7.0`, mtime 2026-08-18 02:49, 94,743,704 bytes) at radix
`5088c4397`.

### Rust-target emit (clean)

```text
cd /Users/ianzepp/work/faberlang/worktrees/test-1/gradus
env FABER_SUPPORT_PATH_OVERRIDE=/Users/ianzepp/work/faberlang \
  FABER_LIBRARY_HOME=/Users/ianzepp/work/faberlang/worktrees/test-1 \
  /Users/ianzepp/work/faberlang/worktrees/test-1/radix/target/debug/faber \
  build --target rust exempla/dense-prefill-qwen2
```

Faber compiled the package, emitted
`exempla/dense-prefill-qwen2/target/faber`, and invoked Cargo.
Cargo compiled `dense-prefill-qwen2` and finished:

```text
warning: `dense-prefill-qwen2` (bin "dense-prefill-qwen2") generated 616 warnings
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 1.19s
/Users/ianzepp/work/faberlang/worktrees/test-1/gradus/exempla/dense-prefill-qwen2/target/debug/dense-prefill-qwen2
```

Exit 0. Printed binary present (3,834,888 bytes, mtime 2026-08-18 02:49).
Zero rustc errors. The prior 248-error stream is gone.

### Observed execution

```text
/Users/ianzepp/work/faberlang/worktrees/test-1/gradus/exempla/dense-prefill-qwen2/target/debug/dense-prefill-qwen2 \
  /Users/ianzepp/ai/models/Qwen2.5-0.5B-Instruct-Q4_K_M.gguf \
  5948480 \
  6eb923e7d26e9cea28811e1a8e852009b21242fb157b26149d3b188f3a8c8653
```

Exit 101. Verbatim:

```text
thread 'main' (39631278) panicked at src/main.rs:937:66:
failable call failed: "sermo materialization failed"
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace
```

Generated site (`target/faber/src/main.rs:936-937`):

```text
let prefix_bytes: Vec<u8> =
    crate::solum::read_range(path.clone(), 0, data_expected).expect("failable call failed");
```

`data_expected` is the pinned table-prefix length `5948480`. The
consumer prints policy/model lines *after* this read, so none appeared.
Admit, tokenizer, weight load, and `dense.forward` were not reached.
Same first-fail family as U1.9 (prefix `solum.read_range` / sermo
materialization). No logits, no observed token ids, no first-divergence
field, no Metal/CUDA or payload-residency claim.

Repair belongs to the compiled `solum.read_range` / sermo materialization
path on a 5_948_480-byte prefix. That surface is not writable in this
test packet.

Toolchain: rustc 1.97.1 (8bab26f4f 2026-07-14) Homebrew, cargo 1.97.1
(c980f4866 2026-06-30). Host: Darwin 25.5.0 arm64
(`burgus.local`, `RELEASE_ARM64_T6050`).

## Prior stops

### 2026-08-17, handle `836c3b55` (FINAL) — rustc 248

Readable radix `2ed9914e4`. Packet `faber` green. Rust emit cleared the
runtime-plan gate; cargo failed rustc 248 errors (first `E0015` const
`vec!` for `PINNED_TOKENS`). Did not reproduce on GATE 8.

### 2026-08-17, handle `fe98cfef` (d23ce56) — resume-2

Readable radix `3853d4b8f`. Packet `cargo build -p faber` green
(E0432 closed). Rust-target emit reached the runtime-plan gate and
stopped `PKG001:host_provider_selection_invalid` because
`norma:processus` emits `processus:exi` and the hosts processus
manifest did not export it. Closed on main by radix `9f828b2b6` /
`ec9210315` and faber `6e13687` / `b1adfc9`. Did not reproduce.

### 2026-08-17, handle `6ecefd40` (b4ec573)

Readable radix `b919052f0`. Packet `cargo build -p faber` failed
`E0432` unresolved `faber_hir_rust::ImportedEnumVariantInfo` in
`radix-program` `rust_target.rs:17`. Rust-target emit was not reached.

### 2026-08-17, 31df6a9

Readable radix `7863624e2`. Packet `cargo build -p faber` failed
`E0004` non-exhaustive `MirCollectionOp`. Same-revision 1.7.0 rust
emit:

```text
error[CODEGEN001]: /tmp/faber-hand-13-libhome/gradus/src/model/dense_qwen2.fab: code generation failed: internal: definition id 4127 could not be resolved during code generation
compilation failed
```

llvm-host fallback: `error[PKG001:llvm_emission_failed]`. `d66e1f93e`
/ `b919052f0` aimed to close that `CODEGEN001`. Did not reproduce on
GATE 8.

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
| Hardware/OS | Darwin 25.5.0 arm64 (`burgus.local`, `RELEASE_ARM64_T6050`) |
| Gradus | `69d1808` (this commit records the GATE 8 receipt) |
| Radix | `5088c4397` (writable; ER-23 on tree; packet `faber` rebuild green) |
| Faber | packet 1.7.0 at `5088c4397` (mtime 2026-08-18 02:49); workspace `afd2a96` via `FABER_SUPPORT_PATH_OVERRIDE` |
| Hosts (read via override) | `bf11418` |
| Norma (read via libhome) | `7d71daf` |
| Comparator binary | `/opt/homebrew/Cellar/llama.cpp/10150/bin/llama-server` SHA-256 `e5c153a1237e1c8e14ce0721d9afba4fd07936c7dc17dc7bd156d4dbe454952a`, version 10150 (`dee2a846b`) |

The real file carries `attn_q.bias` / `attn_k.bias` / `attn_v.bias`.
The U1.8 surface synthesizes zero biases and does not resolve those
tensors. That architecture fact is recorded; it was not used to change
the surface (stop rule: do not tune). GATE 8 did not reach admit, so
those tensors were not observed on this run.

Comparator-only observation from the first attempt (not a Gradus
comparison — no candidate logits): `/completion` on the pinned token
array, `n_predict=1`, `n_probs=5`, `temperature=0`, `seed=42`, CPU
(`--n-gpu-layers 0`), ephemeral port 8310 (not 18173 / 59414),
generation position 0 top-1 token id 304 (` in`).
