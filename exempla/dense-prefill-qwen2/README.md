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

## Stop (2026-08-17)

The compiled route did not produce a binary. Stop rule: unknown
codegen diagnostic → record exactly, stop. Numerics were not tuned.
TARGETLANE001 was not weakened.

### Command

From the Hand packet:

```text
cd /Users/ianzepp/work/faberlang/worktrees/hand-13/gradus
env FABER_SUPPORT_PATH_OVERRIDE=/Users/ianzepp/work/faberlang \
  FABER_LIBRARY_HOME=/tmp/faber-hand-13-libhome \
  /Users/ianzepp/work/faberlang/worktrees/hand-13/radix/target/debug/faber \
  build --target rust exempla/dense-prefill-qwen2
```

`FABER_LIBRARY_HOME` is a directory with `gradus` → this packet and
`norma` → `/Users/ianzepp/work/faberlang/norma`. Packet `cargo build
-p faber` on readable radix `7863624e2` fails to compile
`radix-mir-runner` (`E0004` non-exhaustive `MirCollectionOp`). The
packet `faber` binary is the same-revision `1.7.0` binary from that
commit (hand-12/main already had it).

### Observed rust-target diagnostic (exact)

```text
error[CODEGEN001]: /tmp/faber-hand-13-libhome/gradus/src/model/dense_qwen2.fab: code generation failed: internal: definition id 4127 could not be resolved during code generation
compilation failed
```

No binary path was printed. The binary was not executed.

### Named fallback

```text
env FABER_SUPPORT_PATH_OVERRIDE=/Users/ianzepp/work/faberlang \
  FABER_LIBRARY_HOME=/tmp/faber-hand-13-libhome \
  /Users/ianzepp/work/faberlang/worktrees/hand-13/radix/target/debug/faber \
  build --target llvm-host exempla/dense-prefill-qwen2
```

```text
error[PKG001:llvm_emission_failed]: exempla/dense-prefill-qwen2/src/main.fab
llvm-host build failed
```

### Structural gates that did pass

`faber check exempla/dense-prefill-qwen2` exits 0 (warnings only:
`LOCALE002`, `WARN018`). `./scripta/check-source` exits 0.
`./scripta/check-compile` exits 0. `git diff --check` silent on the
unit paths.

This is not an executed prefill-logit receipt. No Gradus logits, no
first-divergence position, no Metal/CUDA claim, no payload-residency
claim.

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
| Gradus | `5bf3c0408` (packet base; this commit adds the consumer) |
| Radix | `7863624e2` |
| Faber | 1.7.0 at that radix revision |
| Comparator binary | `/opt/homebrew/Cellar/llama.cpp/10150/bin/llama-server` SHA-256 `e5c153a1237e1c8e14ce0721d9afba4fd07936c7dc17dc7bd156d4dbe454952a`, version 10150 (`dee2a846b`) |

The real file carries `attn_q.bias` / `attn_k.bias` / `attn_v.bias`.
The U1.8 surface synthesizes zero biases and does not resolve those
tensors. That architecture fact is recorded; it was not used to change
the surface (stop rule: do not tune).

Comparator-only observation (not a Gradus comparison — no candidate
logits): `/completion` on the pinned token array, `n_predict=1`,
`n_probs=5`, `temperature=0`, `seed=42`, CPU (`--n-gpu-layers 0`),
ephemeral port 8310 (not 18173 / 59414), generation position 0
top-1 token id 304 (` in`).

## Intended executed command (blocked)

```text
<printed-binary> \
  /Users/ianzepp/ai/models/Qwen2.5-0.5B-Instruct-Q4_K_M.gguf \
  5948480 \
  6eb923e7d26e9cea28811e1a8e852009b21242fb157b26149d3b188f3a8c8653
```
