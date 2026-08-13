# M6-U1 — Qwen3.6 35B capstone scaffold: identity + manifest admission

`exempla/qwen36-35b-inference` is the public-Gradus capstone application for
the campaign artifact
`Qwen3.6-35B-A3B-UD-Q4_K_M.gguf`. It owns the path and I/O; Gradus owns model
semantics; Radix owns lowering; Hosts owns physical execution.

This is **real-artifact admission, not inference**. M6-U1 verifies the exact
artifact identity and admits its GGUF v3 manifest through the public
`gradus:model/artifact` / `gradus:model/gguf_manifest` surfaces, then prints
and writes the observed receipt facts. It performs no tokenizer, tensor
materialization, graph, inference, or device behavior. M6-U2..U6 own those
phases and are entry-gated on the named predecessor receipts.

## Frozen CLI contract

```text
qwen36-35b-inference <model-path> --sha256 <digest> [--oracle-offset <n>] [--prompt <text> ...] [--max-new-tokens <n>] [--seed <n>] [--receipt <path>]
```

M6-U1 implements `path`, `--sha256`, `--oracle-offset`, and `--receipt`.
`--prompt`, `--max-new-tokens`, and `--seed` are reserved for later capstone
units (M6-U2+); the parser recognizes them so the contract is frozen, and
refuses them with a typed cause because M6-U1 must not claim their semantics.
An unknown flag or stray positional argument also fails closed.

## Guards

The application reads only the bounded table prefix `[0, oracle_offset)` once
(`solum.partem`), then gives Gradus an operation-scoped range function over
that application-owned buffer. Gradus never receives the path, file handle,
or prefix. The run fails closed (nonzero exit + typed `causa`) on:

- **identity mismatch** — byte length differs from the pinned 22,663,387,424,
  or the `--sha256` operand is not a 64 lower-case hex digest;
- **short prefix** — the table-prefix read returns fewer bytes than
  `--oracle-offset`;
- **tensor-data read** — any Gradus range request whose end exceeds the
  prefix (the manifest parser is bounded to the header/table region);
- **oracle divergence** — the first mismatched manifest fact names itself
  (version, alignment, data offset, metadata count, tensor count,
  architecture).

## Command

From the Hand packet (with `FABER_LIBRARY_HOME` resolving `norma`):

```bash
cd /Users/ianzepp/work/faberlang/worktrees/hand-25/gradus
env FABER_LIBRARY_HOME=<home-with-gradus-and-norma> \
  <packet>/radix/target/debug/faber run --target fmir exempla/qwen36-35b-inference -- \
  /Users/ianzepp/Ai/models/Qwen3.6-35B-A3B-UD-Q4_K_M.gguf \
  --sha256 0b21525e972670ed59e1812e170b27c26355381f0656ecc4e25617ece7dac58b \
  --oracle-offset 10991392 --receipt /tmp/m6-u1-receipt.txt
```

The content digest is re-derived out of band (`shasum -a 256`), because the
FMIR surface has no sha-256 primitive:

```bash
shasum -a 256 /Users/ianzepp/Ai/models/Qwen3.6-35B-A3B-UD-Q4_K_M.gguf
# 0b21525e972670ed59e1812e170b27c26355381f0656ecc4e25617ece7dac58b
```

## Target oracle (independent reader + A1b receipt + `stat`/`shasum`)

| Fact | Pinned |
| --- | --- |
| Byte length | 22,663,387,424 |
| SHA-256 | `0b21525e972670ed59e1812e170b27c26355381f0656ecc4e25617ece7dac58b` |
| GGUF version | 3 |
| Alignment | 32 |
| Data offset | 10,991,392 |
| Metadata entries | 55 |
| Tensors | 753 |
| Architecture | `qwen35moe` |

## Observed receipt

Executed 2026-08-13 against the real artifact with the packet faber binary
(radix `b6d6e17c8ad7`, rebuilt for the current `la` reader pack) and a
throwaway library copy of gradus main with the in-flight import-seam
annotations applied (see the residual note below). Exit 0:

```text
PASS version=3 alignment=32 data=10991392 metadata=55 tensors=753 architecture=qwen35moe
PASS bytes=22663387424
RECORDED sha256=0b21525e972670ed59e1812e170b27c26355381f0656ecc4e25617ece7dac58b (content re-derived externally via shasum -a 256)
ADMISSION PASS
RECEIPT /tmp/m6-u1-receipt.txt
```

`shasum -a 256 /Users/ianzepp/Ai/models/Qwen3.6-35B-A3B-UD-Q4_K_M.gguf`
equals the pinned digest; the receipt file records the observed facts. The
run issued no read into the tensor data region (the application-owned range
seam rejects any request whose end exceeds the bounded table prefix), and the
model bytes remain outside this repository.

Focused negatives all exit nonzero with typed causes:
`byte length mismatch: expected 22663387424, observed …`;
`short table-prefix read: expected …, observed …`;
`manifest admission failed: range source failed: read request exceeds the
bounded table prefix — would enter the tensor data region`;
`content identity invalid: …`; reserved/unknown flags and malformed
`--oracle-offset` operands are also rejected.

## Residual

Current faber from radix main enforces the import-seam policy (SEM006,
radix `016c225c4`) that gradus main has not finished adopting: 27
`import_module_private` findings in `src/tensor.fab`, `src/model/gguf.fab`,
`src/model/gguf_manifest.fab`, and `src/model/safetensors.fab`. Until that
library migration lands, `faber check` / `faber run` on gradus-importing
exempla fail at the library seam, so `./scripta/check-compile` cannot go
green on the committed tree and the closeout command above must run against a
patched library copy. The annotation-only patch changes no library semantics.
