# dense-prefill-smollm2 — REF-01-U1.9 SmolLM2 prefill-logit receipt

Consumer for the U1.8 dense forward graph against the pinned SmolLM2-360M
row on the **compiled rust** receipt tier. This README is the unit receipt.

**Verdict: STOP — not executed.** The compiled-route emit failed with an
unknown codegen diagnostic. Per the unit stop rule that diagnostic is
recorded exactly and is not chased.

## Comparison policy (intended)

- gi0-numeric-contract v1.0.0: finite gate, top-1 exact over non-EOG `{0,2}`,
  top-5 overlap ≥4/5, first-divergence rule, window position 0 (prompt end).
- faber-prefill-oracle `compare_gpu_logits` / `PrefillReceipt` /
  `ExecutableRegime::Prefill` on the committed golden
  `radix/crates/faber-prefill-oracle/testdata/gi2-3-logits-golden/logits-pos0.json`
  (prompt tokens `[504, 2365, 6354, 16438, 27003, 690, 260, 23790, 2767]`,
  golden top-1 non-EOG `30`, golden top-5 `[30, 28, 1270, 365, 198]`).
- Engine: `faber build --target rust` then execute the printed binary.
  MIR stepper is not the receipt-tier engine. llvm-host is the documented
  fallback and was not chased after CODEGEN001.

## Command (from the Hand packet)

```text
cd /Users/ianzepp/work/faberlang/worktrees/hand-12/gradus
env FABER_SUPPORT_PATH_OVERRIDE=/Users/ianzepp/work/faberlang \
  FABER_LIBRARY_HOME=/Users/ianzepp/work/faberlang \
  /Users/ianzepp/work/faberlang/worktrees/hand-12/radix/target/debug/faber \
  build --target rust exempla/dense-prefill-smollm2
```

`FABER_LIBRARY_HOME` is the workspace root (not the packet root) because
the packet has no `norma/` member and this consumer needs `norma:solum` /
`norma:processus` to own the file adapter. Packet `gradus` src at this
refresh equals workspace `gradus` (`5bf3c04`).

## Observed emit (2026-08-17)

`faber check exempla/dense-prefill-smollm2` exits 0.

`faber build --target rust` exits 1. Exact diagnostics:

```text
error[CODEGEN001]: exempla/dense-prefill-smollm2/src/main.fab: code generation failed: internal: definition id 4200 could not be resolved during code generation
error[CODEGEN001]: /Users/ianzepp/work/faberlang/gradus/src/model/tensor_view.fab: code generation failed: internal: definition id 4131 could not be resolved during code generation
compilation failed
```

First emit (consumer imported `gradus:model/dense_llama`) failed with the
same CODEGEN001 class on `dense_llama.fab` definition id 4111. The adapter
import was removed and the frozen llama GGUF-name map inlined in the
consumer. The retry failed on `tensor_view.fab` as above. No further
reduction: the U1.8 receipt needs windowed materialization.

No binary was printed. The GGUF file was not executed. No logits, no
first-divergence field, no Metal/CUDA or payload-residency claim.

## Revisions

| Surface | Revision |
| --- | --- |
| packet gradus | `5bf3c04` (`factory/hand-12`) |
| packet radix (readable) | `7863624e2` |
| faber binary used | packet `target/debug/faber` 1.7.0 (mtime 2026-08-17 19:39) |
| workspace faber/hosts | not written |

## Packet faber rebuild residual

`cd radix && cargo build -p faber` (default `full-targets`) failed on
pre-existing unread EXEC-02 match arms in readable radix. Exact class:

```text
error[E0004]: non-exhaustive patterns: `MirCollectionOp::TensorQuantizedMatMul`,
`TensorGroupedMatMul`, `TensorSsmConv1d`, `TensorSsmScan`
```

in `radix-mir-wasm`, `radix-air`, `radix-mir-runner`. Feature-limited
`--no-default-features --features hir-rust` still pulled `radix-mir-runner`
and failed the same way. Radix is readable-only in this packet; those
arms were not patched. TARGETLANE001 was not touched.

## Model identity (not executed)

| Field | Pinned value |
| --- | --- |
| filename | `SmolLM2-360M-Instruct-Q4_K_M.gguf` |
| path | `/Users/ianzepp/ai/models/SmolLM2-360M-Instruct-Q4_K_M.gguf` |
| bytes | 270,590,880 |
| SHA-256 | `2fa3f013dcdd7b99f9b237717fa0b12d75bbb89984cc1274be1471a465bac9c2` |
| data offset | 1,787,040 |
| prompt | `The quick brown fox jumps over the lazy dog` |
| prompt tokens | `[504, 2365, 6354, 16438, 27003, 690, 260, 23790, 2767]` |

Hardware/OS/backend for an executed run would have been CPU/reference.
No run occurred.

## Evidence boundary

This is a compiled-route **stop receipt**, not a prefill-logit pass.
Repair belongs to rust codegen of `gradus:model/tensor_view` (and
`dense_llama` on the first emit), not to this consumer.
