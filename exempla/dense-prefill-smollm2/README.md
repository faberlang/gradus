# dense-prefill-smollm2 — REF-01-U1.9 SmolLM2 prefill-logit receipt

Consumer for the U1.8 dense forward graph against the pinned SmolLM2-360M
row on the **compiled rust** receipt tier. This README is the unit receipt.

**Verdict: COMPILE CLEAN — execution STOP.** GATE 8 empty-classification
run (handle `0530f8bf` / packet `test-1`) at radix `5088c4397`. Packet
`faber` rebuilt green. `faber build --target rust` printed the binary
(`Finished dev` in 1.10s, 0 rustc errors, 607 warnings). Classified
families (258/248, 65, N4, N5, E0275) did not reproduce. Execution of
the printed binary panicked on the first `solum.read_range` of the GGUF
table prefix: `failable call failed: "sermo materialization failed"`.
No logits. No first-divergence field. TARGETLANE001 was not weakened
(`[build] target` is still `"fmir"`). Numerics were not tuned.

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
  fallback and was not chased after rust compile succeeded.

## GATE 8 command (from the test packet)

```text
cd /Users/ianzepp/work/faberlang/worktrees/test-1/radix
cargo build -p faber
```

`cargo build -p faber` at writable radix `5088c4397` exits 0
(Finished `dev` profile in 4.21s). Packet binary:
`/Users/ianzepp/work/faberlang/worktrees/test-1/radix/target/debug/faber`
(`faber 1.7.0`, rustc 1.97.1 Homebrew, mtime 2026-08-18 02:49,
94,743,704 bytes).

```text
cd /Users/ianzepp/work/faberlang/worktrees/test-1/gradus
env FABER_SUPPORT_PATH_OVERRIDE=/Users/ianzepp/work/faberlang \
  FABER_LIBRARY_HOME=/Users/ianzepp/work/faberlang/worktrees/test-1 \
  /Users/ianzepp/work/faberlang/worktrees/test-1/radix/target/debug/faber \
  build --target rust exempla/dense-prefill-smollm2
```

## Observed rust emit (2026-08-18 GATE 8)

Faber compiled the package, emitted
`exempla/dense-prefill-smollm2/target/faber`, and invoked Cargo.
Cargo compiled `dense-prefill-smollm2` and finished:

```text
warning: `dense-prefill-smollm2` (bin "dense-prefill-smollm2") generated 607 warnings
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 1.10s
/Users/ianzepp/work/faberlang/worktrees/test-1/gradus/exempla/dense-prefill-smollm2/target/debug/dense-prefill-smollm2
```

Exit 0. Printed binary present (3,876,440 bytes, mtime 2026-08-18 02:49).
Zero rustc errors. Every previously classified family is absent from this
stream.

## Observed execution (2026-08-18 GATE 8)

```text
/Users/ianzepp/work/faberlang/worktrees/test-1/gradus/exempla/dense-prefill-smollm2/target/debug/dense-prefill-smollm2 \
  /Users/ianzepp/ai/models/SmolLM2-360M-Instruct-Q4_K_M.gguf \
  1787040 \
  2fa3f013dcdd7b99f9b237717fa0b12d75bbb89984cc1274be1471a465bac9c2
```

Stdout then panic (verbatim):

```text
policy: gi0-numeric-contract v1.0.0 + faber-prefill-oracle compare_gpu_logits (prompt-end / position 0)
engine: compiled rust (faber build --target rust; execute the printed binary)
backend: CPU/reference
model.path=/Users/ianzepp/ai/models/SmolLM2-360M-Instruct-Q4_K_M.gguf
model.digest=2fa3f013dcdd7b99f9b237717fa0b12d75bbb89984cc1274be1471a465bac9c2
model.bytes=270590880

thread 'main' (39631034) panicked at src/main.rs:938:66:
failable call failed: "sermo materialization failed"
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace
```

Generated site (`target/faber/src/main.rs:937-938`):

```text
let prefix_bytes: Vec<u8> =
    crate::solum::read_range(via.clone(), 0, data_expectata).expect("failable call failed");
```

`data_expectata` is the pinned table-prefix length `1787040`. Admit,
tokenizer, weight load, and `dense.forward` were not reached. No logits,
no observed token ids, no first-divergence field, no Metal/CUDA or
payload-residency claim. Stop rule: record exactly, do not chase.

Repair belongs to the compiled `solum.read_range` / sermo materialization
path on a 1_787_040-byte prefix. That surface is outside this test
packet. TARGETLANE001 was not weakened. The generated crate under
`exempla/dense-prefill-smollm2/target/faber` is build output and is not
committed.

Toolchain: rustc 1.97.1 (8bab26f4f 2026-07-14) Homebrew, cargo 1.97.1
(c980f4866 2026-06-30). Host: Darwin 25.5.0 arm64
(`burgus.local`, `RELEASE_ARM64_T6050`).

## Revisions

| Surface | Revision |
| --- | --- |
| packet gradus | `69d1808` (this commit records the GATE 8 receipt) |
| packet radix (writable) | `5088c4397` (ER-23 reborrow; ff from `86470672a`) |
| faber binary used | packet `target/debug/faber` 1.7.0 at `5088c4397` |
| workspace faber | `afd2a96` (via `FABER_SUPPORT_PATH_OVERRIDE`; not written) |
| workspace hosts | `bf11418` (via override; not written) |
| packet/workspace norma | `7d71daf` (read via `FABER_LIBRARY_HOME`; not written) |

## Model identity (admit not reached)

| Field | Pinned value |
| --- | --- |
| filename | `SmolLM2-360M-Instruct-Q4_K_M.gguf` |
| path | `/Users/ianzepp/ai/models/SmolLM2-360M-Instruct-Q4_K_M.gguf` |
| bytes | 270,590,880 (printed by the binary before the panic) |
| SHA-256 | `2fa3f013dcdd7b99f9b237717fa0b12d75bbb89984cc1274be1471a465bac9c2` |
| data offset | 1,787,040 |
| prompt | `The quick brown fox jumps over the lazy dog` |
| prompt tokens | `[504, 2365, 6354, 16438, 27003, 690, 260, 23790, 2767]` |

Hardware/OS: CPU/reference on `Darwin burgus.local 25.5.0 arm64`
(`RELEASE_ARM64_T6050`). The GGUF file was opened far enough to report
byte length; the table-prefix read failed.

## Evidence boundary

This is a compiled-route **compile-clean + execution-stop receipt**, not
a prefill-logit pass. GATE 8's empty-classification compile is the
campaign first. The first executed line after identity prints is the
stop.

## Prior stops

### 2026-08-17 FINAL — rustc 258 (radix `2ed9914e4` / faber `b1adfc9`)

Packet `faber` green. Prior gates cleared: CODEGEN001 (`d66e1f93e`),
E0432 (`7f0c7de51`), PKG001 `processus:exi` (`9f828b2b6` + `6e13687`).
`faber build --target rust` emitted the crate; rustc failed 258 errors
(first: `cast cannot be followed by a method call` at `src/main.rs:766`).
No rust binary. Did not reproduce on GATE 8.
