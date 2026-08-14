# M6-U1 + LIB-02-U4-1 — Qwen3.6 35B capstone: admission + tokenizer phase

`exempla/qwen36-35b-inference` is the public-Gradus capstone application for
the campaign artifact
`Qwen3.6-35B-A3B-UD-Q4_K_M.gguf`. It owns the path and I/O; Gradus owns model
semantics; Radix owns lowering; Hosts owns physical execution.

The application verifies the exact artifact identity and admits its GGUF v3
manifest through the public `gradus:model/artifact` /
`gradus:model/gguf_manifest` surfaces, then runs the **tokenizer phase**
(LIB-02-U4-1): the artifact-backed runtime is built through the public
`gradus:tokenizer` surface, both pinned probes are encoded to the exact
llama.cpp id lists and decoded back to the exact prompts, and the observed
rows are printed as PASS rows. It performs no tensor materialization, model
forward, GPU execution, or full-capstone code beyond the tokenizer phase.
M6-U2..U6 own those later phases and are entry-gated on the named
predecessor receipts.

## Frozen CLI contract

```text
qwen36-35b-inference <model-path> --sha256 <digest> [--oracle-offset <n>] [--prompt <text> ...] [--max-new-tokens <n>] [--seed <n>] [--receipt <path>]
```

The tokenizer phase implements `path`, `--sha256`, `--oracle-offset`, and
`--receipt`. `--prompt`, `--max-new-tokens`, and `--seed` are reserved for
later capstone units (M6-U2+); the parser recognizes them so the contract is
frozen, and refuses them with a typed cause because this phase must not claim
their semantics. An unknown flag or stray positional argument also fails
closed.

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
  architecture);
- **tokenizer divergence** — a probe id list or decoded text diverges from
  the pinned oracle; the divergence receipt names the first divergent
  id/character (campaign rule 5). The exempla never hard-codes probe ids:
  the observed rows come from the runtime, the pinned values are the
  comparison oracle.

## Command

From the Hand packet (with `FABER_LIBRARY_HOME` resolving the lane, which
contains gradus and norma):

```bash
cd /Users/ianzepp/work/faberlang/worktrees/hand-16/gradus
env FABER_LIBRARY_HOME=/Users/ianzepp/work/faberlang/worktrees/hand-16 \
  /Users/ianzepp/work/faberlang/worktrees/hand-16/radix/target/debug/faber run --target fmir exempla/qwen36-35b-inference -- \
  /Users/ianzepp/Ai/models/Qwen3.6-35B-A3B-UD-Q4_K_M.gguf \
  --sha256 0b21525e972670ed59e1812e170b27c26355381f0656ecc4e25617ece7dac58b \
  --oracle-offset 10991392 --receipt /tmp/qwen36-u4-1-receipt.txt
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
| Vocab count | 248,320 |
| Tokenizer model | `gpt2` (byte-level BPE) |
| EOG set | {248044, 248046, 248063, 248064, 248065} |
| add_bos_token | false |

## Tokenizer probe oracle (LIB-02, llama-tokenize 10150 `dee2a846b`)

| Probe | Pinned ids | Decoded round-trip |
| --- | --- | --- |
| `สวัสดีครับ ผมชื่ออเล็กซ์` | `[34469, 168607, 153295, 173922, 153380, 22216, 151752, 172769]` | exact prompt |
| `你好，世界！今天是2026年8月13日 🎉` | `[109266, 3709, 96748, 6115, 113128, 17, 15, 17, 21, 95859, 23, 96212, 16, 18, 95971, 10838, 236, 231]` | exact prompt |

Probe rows are raw-prompt rows, never through the chat template. The pins
live in the delivery oracle section and `src/tokenizer.proba`.

## Observed run

Executed 2026-08-14 against the real artifact with the hand-16 packet faber
binary (lane root as `FABER_LIBRARY_HOME`) on the committed tree. Exit 0:

```text
PASS version=3 alignment=32 data=10991392 metadata=55 tensors=753 architecture=qwen35moe
PASS bytes=22663387424
RECORDED sha256=0b21525e972670ed59e1812e170b27c26355381f0656ecc4e25617ece7dac58b (content re-derived externally via shasum -a 256)
ADMISSION PASS
TOKENIZER vocab=248320 (artifact-backed runtime, public gradus:tokenizer surface)
PASS Probe A encode -> [34469, 168607, 153295, 173922, 153380, 22216, 151752, 172769]
PASS Probe B encode -> [109266, 3709, 96748, 6115, 113128, 17, 15, 17, 21, 95859, 23, 96212, 16, 18, 95971, 10838, 236, 231]
PASS Probe A decode -> สวัสดีครับ ผมชื่ออเล็กซ์
PASS Probe B decode -> 你好，世界！今天是2026年8月13日 🎉
TOKENIZER PHASE PASS
RECEIPT /tmp/qwen36-u4-1-receipt.txt
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
`--oracle-offset` operands are also rejected; a probe row diverging from the
pinned oracle prints a `DIVERGENCE` receipt naming the first divergent
id/character (not observed on the pinned artifact).

## Residual

The import-seam migration (SEM006, radix `016c225c4`) is complete for the
gradus sources consumed by this exempla — `./scripta/check-compile` is green
on the committed tree. The exempla run resolves `FABER_LIBRARY_HOME` to the
lane root, which must contain both `gradus` and `norma` (the hand packet
provides gradus; the lane root carries a `norma` symlink to the container
checkout). The full tokenizer-phase execution runs under the FMIR stepper
(~6 min on the real artifact); exact-id proba rows still run under the
cargo-backed harness at test-lane/merge time.
