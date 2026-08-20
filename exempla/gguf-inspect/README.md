# GGUF-A1b guarded real-file inspection

This package is the application-owned file adapter for
`gradus:model/gguf_manifest`. It resolves one local path, reads the independently
bounded header/table prefix once, supplies exact byte ranges from that
application-owned buffer to Gradus, and prints the returned manifest facts.
Gradus receives and retains no path, file handle, mapping, callback, prefix, or
whole-model payload.

This is format inspection, not model admission or inference. The local files
are operator evidence and are not committed or redistributed.

## Tensor-data guard

The second CLI operand is the data offset from the independent GGUF reader.
The adapter calls `solum.partem(path, 0, oracle_offset)` once and rejects a
short prefix. Its captured callback returns exact subranges only from that
prefix and rejects any request whose end exceeds it. A passing run therefore
proves that manifest inspection did not read a tensor payload byte. The CLI
also compares Gradus's independently computed `data_start` with the oracle
value.

## Independent inventory

Sizes and SHA-256 identities were measured with `stat -f '%z'` and
`shasum -a 256`. GGUF version, alignment, data offset, metadata count, tensor
count, and architecture were read independently with Homebrew
`/opt/homebrew/bin/llama-gguf <file> r 1`.

| Local artifact | Bytes | SHA-256 | Oracle data offset | Metadata | Tensors | Architecture |
| --- | ---: | --- | ---: | ---: | ---: | --- |
| `SmolLM2-360M-Instruct-Q4_K_M.gguf` | 270,590,880 | `2fa3f013dcdd7b99f9b237717fa0b12d75bbb89984cc1274be1471a465bac9c2` | 1,787,040 | 37 | 290 | `llama` |
| `Qwen2.5-0.5B-Instruct-Q4_K_M.gguf` | 397,808,192 | `6eb923e7d26e9cea28811e1a8e852009b21242fb157b26149d3b188f3a8c8653` | 5,948,480 | 38 | 290 | `qwen2` |
| `Qwen2.5-1.5B-Instruct-Q4_K_M.gguf` | 986,048,768 | `1adf0b11065d8ad2e8123ea110d1ec956dab4ab038eab665614adba04b6c3370` | 5,951,232 | 38 | 338 | `qwen2` |
| `Qwen3.6-35B-A3B-UD-Q4_K_M.gguf` | 22,663,387,424 | `0b21525e972670ed59e1812e170b27c26355381f0656ecc4e25617ece7dac58b` | 10,991,392 | 55 | 753 | `qwen35moe` |
| `heretic-UD-Q6_K.gguf` | 29,308,320,448 | `721b438bca86cace5200e2507f69ab8e2c3859557a6791a1472a7277b19bfb32` | 10,989,760 | 51 | 733 | `qwen35moe` |
| `ornith-1.0-35b-Q8_0.gguf` | 36,903,138,880 | `cbc992bca07901c1a51f33e65e6fc5d687de179c852a772dfd15e4c3261dbf5c` | 10,988,608 | 40 | 733 | `qwen35moe` |

## Command

From the Hand packet, substitute one row's path, offset, and digest:

```bash
mkdir -p /tmp/faber-gguf-library-home-a1b
test -e /tmp/faber-gguf-library-home-a1b/gradus || \
  ln -s /Users/ianzepp/work/faberlang/worktrees/hand-1/gradus \
  /tmp/faber-gguf-library-home-a1b/gradus
test -e /tmp/faber-gguf-library-home-a1b/norma || \
  ln -s /Users/ianzepp/work/faberlang/norma \
  /tmp/faber-gguf-library-home-a1b/norma
cd /Users/ianzepp/work/faberlang/worktrees/hand-1/gradus
env FABER_LIBRARY_HOME=/tmp/faber-gguf-library-home-a1b \
  /Users/ianzepp/work/faberlang/worktrees/hand-2/radix/target/debug/faber \
  run --target fmir exempla/gguf-inspect -- \
  /Users/ianzepp/Ai/models/Qwen2.5-0.5B-Instruct-Q4_K_M.gguf \
  5948480 \
  6eb923e7d26e9cea28811e1a8e852009b21242fb157b26149d3b188f3a8c8653
```

## Observed receipt

The final captured-source commands all exited `0` on 2026-08-13:

```text
PASS version=3 alignment=32 data=1787040 metadata=37 tensors=290 architecture=llama
PASS version=3 alignment=32 data=5948480 metadata=38 tensors=290 architecture=qwen2
PASS version=3 alignment=32 data=5951232 metadata=38 tensors=338 architecture=qwen2
PASS version=3 alignment=32 data=10991392 metadata=55 tensors=753 architecture=qwen35moe
PASS version=3 alignment=32 data=10989760 metadata=51 tensors=733 architecture=qwen35moe
PASS version=3 alignment=32 data=10988608 metadata=40 tensors=733 architecture=qwen35moe
```

The receipt proves generic GGUF v3 manifest inspection across the local dense
and hybrid inventory, including rank-3 expert tensors and mixed raw GGML type
IDs. It does not prove tokenizer behavior, tensor materialization, model
semantics, logits, token generation, CPU inference, or GPU inference. Those
remain GGUF-A2 through GGUF-A7 and GGUF-M1.
