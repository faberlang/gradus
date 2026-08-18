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

## Resume-2 stop (2026-08-17)

U1.10 RESUME-2 on handle `fe98cfef` / packet hand-13. Readable radix
`3853d4b8f` includes the E0432 façade fix (`7f0c7de51` — re-export
`ImportedEnumVariantInfo` on `faber-hir-rust`). Packet `cargo build -p
faber` now succeeds. The rust-target emit reaches the runtime-plan
gate and stops on a new diagnostic. Stop rule: new diagnostic → record
exactly, stop. Numerics were not tuned. TARGETLANE001 was not
weakened (`[build] target = "fmir"` stays). The GGUF file was not
executed.

### Packet faber rebuild (green)

From the Hand packet:

```text
cd /Users/ianzepp/work/faberlang/worktrees/hand-13/radix
cargo build -p faber
```

Exit 0 in 8.48s. Binary
`/Users/ianzepp/work/faberlang/worktrees/hand-13/radix/target/debug/faber`
(`faber 1.7.0`, mtime 2026-08-17 21:11, 94,047,368 bytes). The prior
E0432 (`faber_hir_rust::ImportedEnumVariantInfo`) did not reproduce.

### Rust-target emit (blocked)

```text
cd /Users/ianzepp/work/faberlang/worktrees/hand-13/gradus
env FABER_SUPPORT_PATH_OVERRIDE=/Users/ianzepp/work/faberlang \
  FABER_LIBRARY_HOME=/tmp/faber-hand-13-libhome \
  /Users/ianzepp/work/faberlang/worktrees/hand-13/radix/target/debug/faber \
  build --target rust exempla/dense-prefill-qwen2
```

`FABER_LIBRARY_HOME` is a directory with `gradus` → this packet and
`norma` → `/Users/ianzepp/work/faberlang/norma`.

First emit, host unset, exit 1:

```text
error[PKG001:package_host_selection_required]: exempla/dense-prefill-qwen2/faber.toml
runtime plan failed
```

In-scope consumer fix (not a TARGETLANE001 change): add the rust
receipt-tier host selection and keep the package default on FMIR.

```toml
[build]
target = "fmir"
kind = "bin"

[target.rust]
host = "native"
```

Second emit, host set, exit 1. Exact diagnostic (coded PKG001 hides
the underlying message in normal render; the issue arg is the identity):

```text
error[PKG001:host_provider_selection_invalid]: /Users/ianzepp/work/faberlang/worktrees/hand-13/gradus/exempla/dense-prefill-qwen2/faber.toml
runtime plan failed
```

Recorded source facts (readable trees only; hosts/radix not patched):

- `[target.rust] host = "native"` selects providers for every non-runtime
  `ad` route in the package units **and** the expanded library import
  bodies (`radix/crates/faber/src/package/cargo.rs`
  `rust_runtime_plan_for_package`).
- This consumer imports `norma:processus` (`processus.argv`) and
  `norma:solum`. Gradus source has no `call '` routes.
- `norma/src/processus.fab` `exit_process` emits `call 'processus:exi'`.
  Norma processus routes: `argumenta`, `captura`, `dimitte`, `exi`,
  `exsequetur`, `exsequi`, `identitas`, `lege`, `muta`, `scribe`, `sedes`.
- `hosts/crates/processus/src/manifest.json` exports every one of those
  except `processus:exi`. Solum Norma routes match the solum host
  manifest (empty missing set).
- `load_provider_manifests` fail-closes on a required route the selected
  providers do not export (`dispatch.rs`
  `host_provider_route_missing`). That error is stored as
  `plan.provider_error` and re-issued as
  `PKG001:host_provider_selection_invalid`.

No rust binary was printed. llvm-host was not chased: the rust receipt
tier produced a new diagnostic. The GGUF file was not executed. No
logits, no observed token ids, no first-divergence field, no
Metal/CUDA or payload-residency claim.

Repair belongs to the hosts `processus` provider manifest (export
`processus:exi`) or to faber used-route collection (do not require
unused library `ad` routes). Neither surface is writable in this
packet.

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
/ `b919052f0` aimed to close that `CODEGEN001`. This resume loaded a
runnable `faber` at `3853d4b8f` and did not re-exercise CODEGEN001.

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
| Gradus | `a0d78a5` (packet base; this commit records the resume-2 stop) |
| Radix | `3853d4b8f` (readable; `7f0c7de51` on tree; packet `faber` rebuild green) |
| Faber | packet 1.7.0 at `3853d4b8f` (mtime 2026-08-17 21:11) |
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
