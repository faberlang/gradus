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

## FINAL stop (2026-08-17)

U1.10 FINAL on handle `836c3b55` / packet hand-13. Readable radix
`2ed9914e4` includes the `processus:exi` builtin-route fix (`9f828b2b6`
/ merge `ec9210315`). Workspace faber `b1adfc9` delivers
`processus:exi` via `process::exit`. Packet `cargo build -p faber` is
green. The rust-target emit now **clears the runtime-plan gate**
(PKG001:host_provider_selection_invalid did **not** reproduce) and
prints a generated crate. Cargo then fails to compile that crate.
Stop rule: new diagnostic → record exactly, stop. Numerics were not
tuned. TARGETLANE001 was not weakened (`[build] target = "fmir"`
stays). The GGUF file was not executed.

### Packet faber rebuild (green)

From the Hand packet:

```text
cd /Users/ianzepp/work/faberlang/worktrees/hand-13/radix
cargo build -p faber
```

Exit 0 in 19.32s. Binary
`/Users/ianzepp/work/faberlang/worktrees/hand-13/radix/target/debug/faber`
(`faber 1.7.0`, mtime 2026-08-17 22:03, 94,349,432 bytes) at radix
`2ed9914e4`. Prior E0432 and PKG001 (`processus:exi`) did not
reproduce.

### Rust-target emit (runtime plan green; cargo 101)

```text
cd /Users/ianzepp/work/faberlang/worktrees/hand-13/gradus
env FABER_SUPPORT_PATH_OVERRIDE=/Users/ianzepp/work/faberlang \
  FABER_LIBRARY_HOME=/tmp/faber-hand-13-libhome \
  /Users/ianzepp/work/faberlang/worktrees/hand-13/radix/target/debug/faber \
  build --target rust exempla/dense-prefill-qwen2
```

`FABER_LIBRARY_HOME` is a directory with `gradus` → this packet and
`norma` → `/Users/ianzepp/work/faberlang/norma`.
`[target.rust] host = "native"` is already on the consumer
(`target = "fmir"` kept).

Faber compiled the package, emitted
`exempla/dense-prefill-qwen2/target/faber`, and invoked Cargo.
Cargo compiled `dense-prefill-qwen2 v0.1.0` and failed. Faber
wrapper (last line):

```text
error: cargo build exited with status exit status: 101
```

Rustc: 248 errors, 350 warnings. First identity (generated
`src/main.rs:26`):

```text
error[E0015]: cannot call non-const associated function `Box::<[i64; 17]>::new_uninit` in constants
  --> src/main.rs:26:37
   |
26 |   pub const PINNED_TOKENS: Vec<i64> = vec![
   |  _____________________________________^
27 | |     785, 6722, 315, 9625, 374, 12095, 323, 279, 6722, 315, 6323, 374, 26194, 13, 576, 1790, 3283,
28 | | ];
```

Error-code families (count of `error[E…]` lines):

| Code | Count | First site / meaning |
| --- | --- | --- |
| E0015 | 171 | `PINNED_TOKENS` const `vec![]`; later const `format!` |
| E0493 | 37 | destructor of `String` cannot be evaluated at compile-time |
| E0308 | 25 | first: closure capturing `path`/`total` passed where `fn(i64, i64) -> SourceRead` is required (`materialize_slice` reader) |
| E0599 | 9 | `faber::Tensor<f32>` has no `transpone` / `activatio_softmax` |
| E0605 | 1 | `segment as Vec<u8>` non-primitive cast |
| E0277 | 1 | `f32 / i64` (`shifted / TAU.floor() as i64`) |
| E0061 | 1 | `fons(nomen.clone())` missing second `i64` (layer) argument |
| E0609 | 1 | `alignment_meta.dtype` on `Option<GgufMetadata>` |
| E0382 | 1 | moved `cohaesum: String` inside a loop |

No rust binary was printed (path line absent; no
`target/debug/dense-prefill-qwen2`). llvm-host was not chased: the
rust receipt tier produced a new diagnostic. The GGUF file was not
executed. No logits, no observed token ids, no first-divergence
field, no Metal/CUDA or payload-residency claim.

Repair belongs to rust HIR emit / generated-Rust runtime (const
`Vec` materialization, closure-vs-fn-pointer readers, tensor
methods). Those surfaces are not writable in this packet.

Toolchain: rustc 1.97.1 (8bab26f4f 2026-07-14) Homebrew, cargo 1.97.1
(c980f4866 2026-06-30). Host: Darwin 25.5.0 arm64
(`burgus.local`, `RELEASE_ARM64_T6050`).

### Intended executed command (blocked)

```text
<printed-binary> \
  /Users/ianzepp/ai/models/Qwen2.5-0.5B-Instruct-Q4_K_M.gguf \
  5948480 \
  6eb923e7d26e9cea28811e1a8e852009b21242fb157b26149d3b188f3a8c8653
```

## Prior stops

### 2026-08-17, handle `fe98cfef` (d23ce56) — resume-2

Readable radix `3853d4b8f`. Packet `cargo build -p faber` green
(E0432 closed). Rust-target emit reached the runtime-plan gate and
stopped `PKG001:host_provider_selection_invalid` because
`norma:processus` emits `processus:exi` and the hosts processus
manifest did not export it. Closed on main by radix `9f828b2b6` /
`ec9210315` and faber `6e13687` / `b1adfc9`. Did not reproduce on
this FINAL run.

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
/ `b919052f0` aimed to close that `CODEGEN001`. Resume-2 and this
FINAL run did not re-exercise CODEGEN001.

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
| Gradus | `1baaaa6` (packet base; this commit records the FINAL stop) |
| Radix | `2ed9914e4` (readable; `9f828b2b6` on tree; packet `faber` rebuild green) |
| Faber | packet 1.7.0 at `2ed9914e4` (mtime 2026-08-17 22:03); workspace `b1adfc9` via `FABER_SUPPORT_PATH_OVERRIDE` |
| Hosts (read via override) | `24687cda4` |
| Norma (read via libhome) | `7d71dafdb` |
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
