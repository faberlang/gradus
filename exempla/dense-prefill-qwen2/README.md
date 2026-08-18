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

## GATE 9 (2026-08-18)

**Verdict: READ_RANGE PASS — execution STOP at embed `_transpose`.**
Handle `134395fe` / packet `test-1`. Writable radix `5088c4397`.
Workspace hosts `a6c8129` (64 MiB `solum` range cap) via
`FABER_SUPPORT_PATH_OVERRIDE`. Packet `cargo build -p faber` green.
`faber build --target rust` printed the binary (`Finished dev` in
0.58s, 0 rustc errors, 616 warnings; Cargo recompiled workspace
`solum`). Execution of the printed binary **passed**
`solum.read_range` of the 5_948_480-byte table prefix, printed
architecture facts, matched the pinned tokenizer ids, loaded all 24
layers, then entered `dense.forward` → generated `_transpose` of
`model.embed_tokens` `[896, 151936]`, cloning `t.data` (~518 MiB) on
every element (~136e6 clones). After 19m47s total (forward entered
~17m18s) at 100% CPU / 6.1 GiB RSS still in that exact call, the
process was SIGTERM'd (exit 143). No logits. Stop rule: new
diagnostic → record exactly, stop. Numerics were not tuned.
TARGETLANE001 was not weakened (`[build] target = "fmir"` stays).

### Packet faber rebuild (green)

From the test packet:

```text
cd /Users/ianzepp/work/faberlang/worktrees/test-1/radix
cargo build -p faber
```

Exit 0 in 0.12s (already current). Binary
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
Cargo compiled workspace `solum` (`MAX_RANGE_READ_BYTES = 64 MiB`)
and `dense-prefill-qwen2`:

```text
   Compiling solum v0.1.0 (/Users/ianzepp/work/faberlang/hosts/crates/solum)
warning: `dense-prefill-qwen2` (bin "dense-prefill-qwen2") generated 616 warnings
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.58s
/Users/ianzepp/work/faberlang/worktrees/test-1/gradus/exempla/dense-prefill-qwen2/target/debug/dense-prefill-qwen2
```

Exit 0. Printed binary present (3,834,888 bytes, mtime 2026-08-18 03:12).
Zero rustc errors.

### Observed execution

```text
/Users/ianzepp/work/faberlang/worktrees/test-1/gradus/exempla/dense-prefill-qwen2/target/debug/dense-prefill-qwen2 \
  /Users/ianzepp/ai/models/Qwen2.5-0.5B-Instruct-Q4_K_M.gguf \
  5948480 \
  6eb923e7d26e9cea28811e1a8e852009b21242fb157b26149d3b188f3a8c8653
```

Start `2026-08-18T07:57:17Z`. Stdout (verbatim, then hang):

```text
policy=gi0-numeric-contract v1.0.0 finite/top-1-exact/top-5-overlap>=4/5/delta=1e-5 window=0..16
backend=CPU/reference
model=Qwen2.5-0.5B-Instruct-Q4_K_M.gguf
bytes=397808192
sha256=6eb923e7d26e9cea28811e1a8e852009b21242fb157b26149d3b188f3a8c8653
prompt=The capital of France is Paris and the capital of Japan is Tokyo. The next city
architecture=qwen2
tensors=290
layers=24
heads=14
kv_heads=2
head_dim=64
hidden_dim=896
vocab=151936
tied=true
observed_token_ids=[785,6722,315,9625,374,12095,323,279,6722,315,6323,374,26194,13,576,1790,3283]
tokenizer_ids=PASS
loading stored-weight views through the U1.8 resolver
loaded_layer=0
...
loaded_layer=23
```

`solum.read_range` of 5_948_480 bytes **passed** (GATE 8 printed
nothing because this consumer prints policy/model *after* the prefix
read). Admit, tokenizer, and all 24 layer materializations completed.
After `loaded_layer=23` the process entered `run_forward` →
`dense::forward` → `_transpose` at `target/faber/src/main.rs:4175` /
`_transpose` `3805-3838`. Sample at +17m18s and +19m47s showed the
same leaf: `t.data.clone()` then `_platform_memmove`. RSS 6,420,432
KiB (~6.1 GiB), 100% CPU, state R. SIGTERM at
`2026-08-18T08:17:06Z` (elapsed 19m47s, CPU 20m13s). Exit 143. No
position/top-1/top-5/first-divergence lines.

Generated site (`target/faber/src/main.rs:3821-3834`):

```text
out.push(
    (t.data
        .clone()
        .get(...)
        .cloned())
    .clone()
    .unwrap_or((0.0 as f32)),
);
```

`embed` shape is `[896, 151936]` (136,134,656 f32, ~518 MiB). Each of
the 136e6 iterations clones the whole `t.data`. Same first-fail family
as U1.9 after the cap (embed `_transpose` clone-per-element). No
logits, no first-divergence field, no Metal/CUDA or payload-residency
claim.

Repair belongs to generated tensor `_transpose` (do not clone `t.data`
per element). That surface is not writable in this test packet.

Toolchain: rustc 1.97.1 (8bab26f4f 2026-07-14) Homebrew, cargo 1.97.1
(c980f4866 2026-06-30). Host: Darwin 25.5.0 arm64
(`burgus.local`, `RELEASE_ARM64_T6050`, Apple M5 Max).

## Prior stops

### 2026-08-18 GATE 8 — sermo materialization (radix `5088c4397` / hosts `bf11418`)

Packet `faber` green. Rust emit 0 errors / 616 warnings. Printed binary
panicked on the first `solum.read_range` of the 5_948_480-byte prefix:
`failable call failed: "sermo materialization failed"`. Closed on hosts
`a6c8129`. Did not reproduce on GATE 9.

### 2026-08-17, handle `836c3b55` (FINAL) — rustc 248

Readable radix `2ed9914e4`. Packet `faber` green. Rust emit cleared the
runtime-plan gate; cargo failed rustc 248 errors (first `E0015` const
`vec!` for `PINNED_TOKENS`). Did not reproduce on GATE 8 or GATE 9.

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
GATE 8 or GATE 9.

## Pinned row facts (logits not reached)

| Field | Value |
| --- | --- |
| Comparison policy | gi0-numeric-contract v1.0.0: finite gate, top-1 exact, top-5 overlap ≥ 4/5, Δ=1e-5 band, window positions 0..16 |
| Model | `Qwen2.5-0.5B-Instruct-Q4_K_M.gguf` |
| Bytes | 397,808,192 |
| SHA-256 | `6eb923e7d26e9cea28811e1a8e852009b21242fb157b26149d3b188f3a8c8653` |
| Data offset | 5,948,480 |
| Architecture (observed) | `qwen2` (24/14/2/64/896, vocab 151936, tied `true`) |
| Tensors (observed) | 290 |
| Prompt | `The capital of France is Paris and the capital of Japan is Tokyo. The next city` |
| Prompt SHA-256 | `973c9c7fbb1f277298e3525d09454a05af4754b670715247a12c7fa32a390c45` |
| Pinned tokenizer ids (llama-tokenize 10150 `dee2a846b`, `--no-bos`) | `[785, 6722, 315, 9625, 374, 12095, 323, 279, 6722, 315, 6323, 374, 26194, 13, 576, 1790, 3283]` |
| Observed tokenizer ids | same (tokenizer_ids=PASS) |
| Observed top-1 / top-5 | not produced |
| first_divergence | not produced |
| Backend (declared) | CPU/reference |
| Hardware/OS | Darwin 25.5.0 arm64 (`burgus.local`, `RELEASE_ARM64_T6050`, Apple M5 Max) |
| Gradus | this commit (GATE 9 receipt; parent `c6ffd83`) |
| Radix | `5088c4397` (writable; packet `faber` rebuild green) |
| Faber | packet 1.7.0 at `5088c4397` (mtime 2026-08-18 02:49); workspace `afd2a96` via `FABER_SUPPORT_PATH_OVERRIDE` |
| Hosts (read via override) | `a6c8129` (64 MiB `solum` cap) |
| Norma (read via libhome) | `7d71daf` |
| Comparator binary | `/opt/homebrew/Cellar/llama.cpp/10150/bin/llama-server` SHA-256 `e5c153a1237e1c8e14ce0721d9afba4fd07936c7dc17dc7bd156d4dbe454952a`, version 10150 (`dee2a846b`) |

The real file carries `attn_q.bias` / `attn_k.bias` / `attn_v.bias`.
The U1.8 surface synthesizes zero biases and does not resolve those
tensors. That architecture fact is recorded; it was not used to change
the surface (stop rule: do not tune). GATE 9 reached admit and layer
load, so those tensors were present in the manifest; they were not
materialized as U1.8 lookups.

Comparator-only observation from the first attempt (not a Gradus
comparison — no candidate logits): `/completion` on the pinned token
array, `n_predict=1`, `n_probs=5`, `temperature=0`, `seed=42`, CPU
(`--n-gpu-layers 0`), ephemeral port 8310 (not 18173 / 59414),
generation position 0 top-1 token id 304 (` in`).
