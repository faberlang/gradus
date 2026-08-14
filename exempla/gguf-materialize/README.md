# GGUF-A3 C3-U2 — real-file mode + coverage + receipt

This package is the application-owned file adapter for
`gradus:model/tensor_payload` / `gradus:model/tensor_view` packed-storage
materialization. The fixture mode proves bounded materialization of the
committed `fixtures/gguf/smollm2-360m-scaled-row.gguf`; the real-file mode
(C3-U2) resolves the local Qwen3.6 artifact, admits its manifest, prints the
per-type coverage, materializes the named slice table, and compares every
slice bit-exactly against the committed golden values. Gradus receives and
retains no path, reader, file handle, mapping, or whole-model payload; every
byte read is a bounded sub-window through the app-owned range source.

This is output-checked slice evidence at the package-MIR tier. It is not a
token, model-execution, logit, or device claim (CTO8-1 stays the named gate).

## Command

From the Hand packet (substitute the lane worktree paths):

```bash
cd <hand-worktree>/gradus
env FABER_LIBRARY_HOME=<worktree-root> \
  <worktree>/radix/target/debug/faber run --target fmir exempla/gguf-materialize -- \
  /Users/ianzepp/ai/models/Qwen3.6-35B-A3B-UD-Q4_K_M.gguf 10991392 \
  0b21525e972670ed59e1812e170b27c26355381f0656ecc4e25617ece7dac58b
```

Fixture mode (unchanged from C3-U1):

```bash
env FABER_LIBRARY_HOME=<worktree-root> \
  <worktree>/radix/target/debug/faber run --target fmir exempla/gguf-materialize -- \
  fixtures/gguf/smollm2-360m-scaled-row.gguf
```

## Content identities

The Qwen3.6 artifact is operator evidence, never committed. Identity facts
measured with `stat -f '%z'` and `shasum -a 256`; data offset, metadata
count, and tensor count read independently with Homebrew
`/opt/homebrew/bin/llama-gguf <file> r 1`:

| Local artifact | Bytes | SHA-256 | Oracle data offset | Metadata | Tensors | Architecture |
| --- | ---: | --- | ---: | ---: | ---: | --- |
| `Qwen3.6-35B-A3B-UD-Q4_K_M.gguf` | 22,663,387,424 | `0b21525e972670ed59e1812e170b27c26355381f0656ecc4e25617ece7dac58b` | 10,991,392 | 55 | 753 | `qwen35moe` |

## Coverage line

The app iterates the admitted manifest's 753 tensor descriptors and classifies
each GGML type against the admitted union set
{F32, BF16, Q5_0, Q8_0, Q4_K, Q5_K, Q6_K}; `types=` lists the observed
per-type distribution:

```text
PASS coverage tensors=753 known=753 unknown=0 types=BF16:2 F32:368 Q8_0:259 Q4_K:82 Q5_K:38 Q6_K:4
```

The two Qwen2.5 dense rows' exact type distributions are not in shared
evidence; this unit derives them from the live manifests at its boundary and
records them in the coverage record:

```text
PASS dense-row Qwen2.5-0.5B tensors=290 types=F32:121 Q4_K:12 Q5_0:132 Q6_K:12 Q8_0:13
PASS dense-row Qwen2.5-1.5B tensors=338 types=F32:141 Q4_K:168 Q6_K:29
```

## Slice table (named at the unit boundary from the live manifest)

Every slice materializes a bounded, block-aligned element window via
`vincula` + `materializa_slicem`; every block read flows through the app-owned
range source. The golden expected values are derived at the unit boundary from
the local artifact with the same reference oracle as the committed
`fixtures/gguf/gguf-dequant-goldens.json` (llama.cpp `ggml-quants.c` @
`a957b7747`, expressed by the committed generator kernels) and are embedded in
`src/main.fab`; the app compares each observed value bit-exactly (no
tolerance).

| # | Slice (tensor) | GGML type | Window (elements) |
| --- | --- | --- | ---: |
| 1 | `blk.40.ffn_gate_inp.weight` | BF16 | 8 |
| 2 | `blk.40.ffn_gate_inp_shexp.weight` | BF16 | 8 |
| 3 | `blk.0.ffn_gate_exps.weight` | Q4_K | 256 |
| 4 | `blk.0.ffn_down_exps.weight` | Q5_K | 256 |
| 5 | `output.weight` | Q6_K | 256 |
| 6 | `blk.0.attn_qkv.weight` | Q8_0 | 32 |
| 7 | `output_norm.weight` | F32 | 8 |
| 8 | `blk.0.ffn_up_exps.weight` | Q4_K (rank-3 expert) | 256 |

The rank-3 expert row is a bounded per-expert window (one block of expert 0).
All windows are far below `MAXIMUM_SLICEM_ELEMENTA` and `CORPUS_LIMES`.

## Observed receipt

The guarded real-file command exited `0` on 2026-08-14 with zero FAIL lines:

```text
PASS version=3 alignment=32 data=10991392 metadata=55 tensors=753 architecture=qwen35moe
PASS coverage tensors=753 known=753 unknown=0 types=BF16:2 F32:368 Q8_0:259 Q4_K:82 Q5_K:38 Q6_K:4
PASS blk.40.ffn_gate_inp.weight type=30 window=8 first=-0.0031890869140625
PASS blk.40.ffn_gate_inp_shexp.weight type=30 window=8 first=-0.0034027099609375
PASS blk.0.ffn_gate_exps.weight type=12 window=256 first=0.003882765769958496
PASS blk.0.ffn_down_exps.weight type=13 window=256 first=0.01642751693725586
PASS output.weight type=14 window=256 first=-0.0050029754638671875
PASS blk.0.attn_qkv.weight type=8 window=32 first=-0.017915010452270508
PASS output_norm.weight type=0 window=8 first=2.734375
PASS blk.0.ffn_up_exps.weight type=12 window=256 first=0.007694900035858154
PASS dense-row Qwen2.5-0.5B tensors=290 types=F32:121 Q4_K:12 Q5_0:132 Q6_K:12 Q8_0:13
PASS dense-row Qwen2.5-1.5B tensors=338 types=F32:141 Q4_K:168 Q6_K:29
PASS real-file materialize + coverage receipt
```

The first element of every materialized window matches the committed golden
value; the app verified the full window element-by-element (any divergence
would name the first divergent element and fail the slice). The receipt proves
checked packed-storage materialization of real Qwen3.6 bytes at the
output-checked slice tier. It does not prove tokenizer behavior, model
execution, logits, or device execution; those remain GGUF-A2/A4 through
GGUF-M6.
