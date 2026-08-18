# dense-prefill-smollm2 — REF-01-U1.9 SmolLM2 prefill-logit receipt

Consumer for the U1.8 dense forward graph against the pinned SmolLM2-360M
row on the **compiled rust** receipt tier. This README is the unit receipt.

**Verdict: READ_RANGE PASS — execution STOP at embed `_transpose`.** GATE 9
(handle `134395fe` / packet `test-1`) at radix `5088c4397` with hosts
`a6c8129` (64 MiB `solum` range cap). Packet `faber` rebuilt green. Both
exempla rebuilt against the new runtime. The printed binary passed
`solum.read_range` of the 1_787_040-byte table prefix, admitted the GGUF,
matched the pinned tokenizer ids, loaded all 32 layers, and printed
`forward start T=9`. `dense.forward` then sat in generated `_transpose`
of `model.embed_tokens` `[960, 49152]`, cloning `t.data` (~180 MiB) on
every element (~47e6 clones). After 43m49s at 100% CPU / 2.3 GiB RSS
still in that exact call, the process was SIGTERM'd (exit 143). No
logits. No first-divergence field. TARGETLANE001 was not weakened
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

## GATE 9 command (from the test packet)

```text
cd /Users/ianzepp/work/faberlang/worktrees/test-1/radix
cargo build -p faber
```

`cargo build -p faber` at writable radix `5088c4397` exits 0
(Finished `dev` profile in 0.12s; already current). Packet binary:
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

## Observed rust emit (2026-08-18 GATE 9)

Faber compiled the package, emitted
`exempla/dense-prefill-smollm2/target/faber`, and invoked Cargo.
Cargo compiled workspace `solum` (`/Users/ianzepp/work/faberlang/hosts/crates/solum`,
`MAX_RANGE_READ_BYTES = 64 MiB`) and `dense-prefill-smollm2`:

```text
   Compiling solum v0.1.0 (/Users/ianzepp/work/faberlang/hosts/crates/solum)
   Compiling dense-prefill-smollm2 v0.1.0 (.../exempla/dense-prefill-smollm2/target/faber)
warning: `dense-prefill-smollm2` (bin "dense-prefill-smollm2") generated 607 warnings
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.53s
/Users/ianzepp/work/faberlang/worktrees/test-1/gradus/exempla/dense-prefill-smollm2/target/debug/dense-prefill-smollm2
```

Exit 0. Printed binary present (3,876,440 bytes, mtime 2026-08-18 03:12).
Zero rustc errors.

## Observed execution (2026-08-18 GATE 9)

```text
/Users/ianzepp/work/faberlang/worktrees/test-1/gradus/exempla/dense-prefill-smollm2/target/debug/dense-prefill-smollm2 \
  /Users/ianzepp/ai/models/SmolLM2-360M-Instruct-Q4_K_M.gguf \
  1787040 \
  2fa3f013dcdd7b99f9b237717fa0b12d75bbb89984cc1274be1471a465bac9c2
```

Start `2026-08-18T07:13:17Z`. Stdout (verbatim, then hang):

```text
policy: gi0-numeric-contract v1.0.0 + faber-prefill-oracle compare_gpu_logits (prompt-end / position 0)
engine: compiled rust (faber build --target rust; execute the printed binary)
backend: CPU/reference
model.path=/Users/ianzepp/ai/models/SmolLM2-360M-Instruct-Q4_K_M.gguf
model.digest=2fa3f013dcdd7b99f9b237717fa0b12d75bbb89984cc1274be1471a465bac9c2
model.bytes=270590880
admit: PASS version=3 data=1787040 tensors=290 architecture=llama
tokenizer: PASS ids=[504, 2365, 6354, 16438, 27003, 690, 260, 23790, 2767]
prompt_tokens=[504, 2365, 6354, 16438, 27003, 690, 260, 23790, 2767]
loading stored-weight views...
loaded embed+norm
loaded layer 0
...
loaded layer 31
forward start T=9
```

`solum.read_range` of 1_787_040 bytes **passed**. After `forward start T=9`
the process stayed in `dense::forward` → `_transpose` at
`target/faber/src/main.rs:4537` / `_transpose` `4167-4196`. Sample at
+22m and +43m showed the same leaf: `t.data.clone()` then
`_platform_memmove`. RSS 2,413,776 KiB (~2.3 GiB), 99–100% CPU, state R.
SIGTERM at `2026-08-18T07:57:06Z` (elapsed 43m49s, CPU 44m08s). Exit 143.
No `forward done`, no `observed_top1_*`, no `first_divergence`, no
`PREFILL:` line.

Generated site (`target/faber/src/main.rs:4183-4196`):

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

`embed` shape is `[960, 49152]` (47,185,920 f32, ~180 MiB). Each of the
47e6 iterations clones the whole `t.data`. That is not a campaign-time
path to the gi0 oracle. Stop rule: record exactly, do not chase.

Repair belongs to generated tensor `_transpose` (do not clone `t.data`
per element). That surface is outside this test packet. TARGETLANE001
was not weakened. The generated crate under
`exempla/dense-prefill-smollm2/target/faber` is build output and is not
committed.

Toolchain: rustc 1.97.1 (8bab26f4f 2026-07-14) Homebrew, cargo 1.97.1
(c980f4866 2026-06-30). Host: Darwin 25.5.0 arm64
(`burgus.local`, `RELEASE_ARM64_T6050`, Apple M5 Max).

## Revisions

| Surface | Revision |
| --- | --- |
| packet gradus | this commit (GATE 9 receipt; parent `c6ffd83`) |
| packet radix (writable) | `5088c4397` (ER-23 reborrow; same as GATE 8) |
| faber binary used | packet `target/debug/faber` 1.7.0 at `5088c4397` |
| workspace faber | `afd2a96` (via `FABER_SUPPORT_PATH_OVERRIDE`; not written) |
| workspace hosts | `a6c8129` (64 MiB `solum` cap; via override; not written) |
| packet/workspace norma | `7d71daf` (read via `FABER_LIBRARY_HOME`; not written) |

## Model identity (logits not reached)

| Field | Pinned value |
| --- | --- |
| filename | `SmolLM2-360M-Instruct-Q4_K_M.gguf` |
| path | `/Users/ianzepp/ai/models/SmolLM2-360M-Instruct-Q4_K_M.gguf` |
| bytes | 270,590,880 |
| SHA-256 | `2fa3f013dcdd7b99f9b237717fa0b12d75bbb89984cc1274be1471a465bac9c2` |
| data offset | 1,787,040 |
| admit | PASS version=3 data=1787040 tensors=290 architecture=llama |
| prompt | `The quick brown fox jumps over the lazy dog` |
| prompt tokens | `[504, 2365, 6354, 16438, 27003, 690, 260, 23790, 2767]` (tokenizer PASS) |
| observed top-1 / top-5 | not produced |
| first_divergence | not produced |

Hardware/OS: CPU/reference on `Darwin burgus.local 25.5.0 arm64`
(`RELEASE_ARM64_T6050`). Prefix read, admit, tokenizer, and all 32
layer materializations completed. Forward did not return.

## Evidence boundary

This is a compiled-route **read_range-pass + forward-stop receipt**, not
a prefill-logit pass. GATE 9's campaign first is that the 1.78 MiB
prefix is legal under the 64 MiB `solum` cap. The new wall is generated
`_transpose` cloning `t.data` per element. The gi0 comparison was not
reached.

## Prior stops

### 2026-08-18 GATE 8 — sermo materialization (radix `5088c4397` / hosts `bf11418`)

Packet `faber` green. Rust emit 0 errors / 607 warnings. Printed binary
panicked on the first `solum.read_range` of the 1_787_040-byte prefix:
`failable call failed: "sermo materialization failed"`. Closed on hosts
`a6c8129` (range cap 1 MiB → 64 MiB). Did not reproduce on GATE 9.

### 2026-08-17 FINAL — rustc 258 (radix `2ed9914e4` / faber `b1adfc9`)

Packet `faber` green. Prior gates cleared: CODEGEN001 (`d66e1f93e`),
E0432 (`7f0c7de51`), PKG001 `processus:exi` (`9f828b2b6` + `6e13687`).
`faber build --target rust` emitted the crate; rustc failed 258 errors
(first: `cast cannot be followed by a method call` at `src/main.rs:766`).
No rust binary. Did not reproduce on GATE 8 or GATE 9.
