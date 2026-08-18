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

## Layout sweep (2026-08-18, handle 8da95e6c)

**Verdict: FIXED — layer-0 linear families were GGUF K-major and were
fed to `nn.linear` unconverted.** Packet `hand-25`. Same class as the
SmolLM2 Q fix (`012d411`). There is no GI2-2 per-op golden for this
row; probes use GI2-1 dequant + first-row slice. Stored first-32
matches GI2-1 bit-exact. First row after the adapter transpose is
`stored[n*K]` and does **not** equal the stored head (K-major, not
already `[K,N]` row-major). `load_layer` now runs `_kmajor_to_linear`
on q/k/v/o/gate/up/down. Tied `lm_head` stays the token-major embed
path (`dense.forward` transposes to `[D,V]`). Q/K/V biases exist on
the file and are still not consumed (zero-bias U1.8 contract).

Compiled rust `trace` (GI2-1, all PASS max_delta `0`):

| tensor | stored | adapter → nn.linear | method | max_delta |
| --- | --- | --- | --- | --- |
| `attn_q` | Q5_0 `[896,896]` K-major | `[896,896]` row-major | GI2-1 dequant+row0 | **0** |
| `attn_k` | Q5_0 `[896,128]` K-major | `[896,128]` row-major | GI2-1 dequant+row0 | **0** |
| `attn_v` | Q8_0 `[896,128]` K-major | `[896,128]` row-major | GI2-1 dequant+row0 | **0** |
| `attn_output` | Q5_0 `[896,896]` K-major | `[896,896]` row-major | GI2-1 dequant+row0 | **0** |
| `ffn_gate` | Q5_0 `[896,4864]` K-major | `[896,4864]` row-major | GI2-1 dequant+row0 | **0** |
| `ffn_up` | Q5_0 `[896,4864]` K-major | `[896,4864]` row-major | GI2-1 dequant+row0 | **0** |
| `ffn_down` | Q6_K `[4864,896]` K-major | `[4864,896]` row-major | GI2-1 dequant+row0 | **0** |
| `lm_head` | tied `token_embd` Q8_0 `[896,151936]` token-major | `dense.forward` `[D,V]` | GI2-1 embed head | **0** |

Stored head ≠ linear row0 on every 2-D weight (K-major). The adapter
now transposes those families after materialize. No GI2-2 activation
golden exists for this row. GATE 12 re-ran the full prefill binary
after that sweep: observed position-0 top-1 `7` vs comparator `304`.
U1.10 is not CLOSE.

## GATE 12 (2026-08-18)

**Verdict: ORACLE REACHED — finite PASS; first-divergence vs comparator
top-1. U1.10 not CLOSE.** Handle `6d7c97dd` / packet `hand-34`. Gradus
`factory/hand-34` fast-forwarded `factory/hand-25` tip `05f5a3a`
(gather `37cdf7c`, Q/K-major SmolLM2 `012d411`, remaining-linear /
Qwen2 K-major `05f5a3a`). Readable packet radix `1abb7c291`. Workspace
hosts `a6c8129` (64 MiB `solum` range cap) via
`FABER_SUPPORT_PATH_OVERRIDE=/Users/ianzepp/work/faberlang`.
`FABER_LIBRARY_HOME=/Users/ianzepp/work/faberlang` (workspace
container: packet has no `norma` member; `05f5a3a` is exempla-only so
workspace `gradus` library src matches the packet). Packet
`cargo build -p faber` green. `faber build --target rust` printed the
binary (`Finished dev` in 5.64s, 0 rustc errors, 637 warnings).
Execution of the printed binary **passed** `solum.read_range` of the
5_948_480-byte table prefix, printed architecture facts, matched the
pinned tokenizer ids, loaded all 24 layers, completed `dense.forward`
(`logits_shape=[17,151936]`), and printed top-1 / top-5 for window
positions 0..16. `finite_gate=PASS`. Observed position-0 top-1 `7` vs
the GATE 9 pinned-comparator observation `304` (` in`). GATE 10's
post-transpose top-1 was `86331`; GATE 11 after gather was `89`; the
K-major adapter moved the observed token again and did not match the
comparator. Observed top-5 at position 0 `[7, 220, 12, 103630, 320]`
does not contain `304`.

The sweep cleared gather / rmsnorm / rope / all linear *weights*.
First remaining unprobed op in `dense_block` program order is
**attention softmax/mask** inside `attention.multi_head_attention`.
Existing probe evidence also still names the U1.8 zero-bias contract:
the file carries `attn_q.bias` / `attn_k.bias` / `attn_v.bias` and
those tensors are still not consumed (that sits on the Q/K/V
activation path, before softmax). Next unprobed families: residual
adds, swiglu activation, cache/prefill bookkeeping. This gate did not
chase or retune those ops. No in-binary `PREFILL:` line (this consumer
does not call the golden file). Exit 0. Numerics were not tuned.
TARGETLANE001 was not weakened (`[build] target = "fmir"` stays).

### Packet faber rebuild (green)

From the hand packet:

```text
cd /Users/ianzepp/work/faberlang/worktrees/hand-34/radix
cargo build -p faber
```

Exit 0 in 21.79s. Binary
`/Users/ianzepp/work/faberlang/worktrees/hand-34/radix/target/debug/faber`
(`faber 1.7.0`, mtime 2026-08-18 09:12, 95,042,760 bytes) at radix
`1abb7c291`.

### Rust-target emit (clean)

```text
cd /Users/ianzepp/work/faberlang/worktrees/hand-34/gradus
env FABER_SUPPORT_PATH_OVERRIDE=/Users/ianzepp/work/faberlang \
  FABER_LIBRARY_HOME=/Users/ianzepp/work/faberlang \
  /Users/ianzepp/work/faberlang/worktrees/hand-34/radix/target/debug/faber \
  build --target rust exempla/dense-prefill-qwen2
```

`FABER_LIBRARY_HOME` is the workspace container (has `gradus/` +
`norma/`). Packet `hand-34` has no `norma` member. Faber compiled
the package, emitted `exempla/dense-prefill-qwen2/target/faber`, and
invoked Cargo.

```text
warning: `dense-prefill-qwen2` (bin "dense-prefill-qwen2") generated 637 warnings
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 5.64s
/Users/ianzepp/work/faberlang/worktrees/hand-34/gradus/exempla/dense-prefill-qwen2/target/debug/dense-prefill-qwen2
```

Exit 0. Printed binary present (3,924,232 bytes, mtime 2026-08-18 09:14).
Zero rustc errors.

### Observed execution

```text
/Users/ianzepp/work/faberlang/worktrees/hand-34/gradus/exempla/dense-prefill-qwen2/target/debug/dense-prefill-qwen2 \
  /Users/ianzepp/ai/models/Qwen2.5-0.5B-Instruct-Q4_K_M.gguf \
  5948480 \
  6eb923e7d26e9cea28811e1a8e852009b21242fb157b26149d3b188f3a8c8653
```

Start `2026-08-18T13:17:56Z`. End `2026-08-18T13:58:04Z`. Exit 0.
`/usr/bin/time -l`: 2408.13 real, 2165.21 user, 223.70 sys, max RSS
9,441,558,528 bytes (~8.79 GiB).

Stdout (verbatim, layer-load rows elided as `...`):

```text
policy=gi0-numeric-contract v1.0.0 finite/top-1-exact/top-5-overlap>=4/5/delta=1e-5 window=0..16
backend=CPU/reference
model=Qwen2.5-0.5B-Instruct-Q4_K_M.gguf
bytes=397808192
sha256=6eb923e7d26e9cea28811e1a8e852009b21242fb157b26149d3b188f3a8c8653
prompt=The capital of France is Paris and the capital of Japan is Tokyo. The next city
admitting manifest...
admit done
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
logits_shape=[17,151936]
pos=0
top1=7
top1_logit_u6=14433476
top5_0=7
top5_1=220
top5_2=12
top5_3=103630
top5_4=320
finite=PASS
pos=1
top1=220
top1_logit_u6=13213157
top5_0=220
top5_1=1305
top5_2=26381
top5_3=121934
top5_4=4567
finite=PASS
pos=2
top1=12
top1_logit_u6=15146055
top5_0=12
top5_1=220
top5_2=7
top5_3=76828
top5_4=320
finite=PASS
pos=3
top1=92465
top1_logit_u6=13631810
top5_0=92465
top5_1=99630
top5_2=57075
top5_3=39743
top5_4=70468
finite=PASS
pos=4
top1=57075
top1_logit_u6=12965773
top5_0=57075
top5_1=37445
top5_2=121141
top5_3=20754
top5_4=99630
finite=PASS
pos=5
top1=33235
top1_logit_u6=13107370
top5_0=33235
top5_1=70468
top5_2=121934
top5_3=1305
top5_4=70828
finite=PASS
pos=6
top1=12
top1_logit_u6=13402559
top5_0=12
top5_1=103630
top5_2=76828
top5_3=51517
top5_4=115979
finite=PASS
pos=7
top1=26381
top1_logit_u6=12634911
top5_0=26381
top5_1=1305
top5_2=121934
top5_3=11534
top5_4=220
finite=PASS
pos=8
top1=1305
top1_logit_u6=13100730
top5_0=1305
top5_1=79208
top5_2=220
top5_3=121934
top5_4=4610
finite=PASS
pos=9
top1=12
top1_logit_u6=14436580
top5_0=12
top5_1=103630
top5_2=732
top5_3=220
top5_4=115166
finite=PASS
pos=10
top1=33235
top1_logit_u6=13688050
top5_0=33235
top5_1=57075
top5_2=49731
top5_3=30741
top5_4=17429
finite=PASS
pos=11
top1=103630
top1_logit_u6=13650019
top5_0=103630
top5_1=108809
top5_2=5284
top5_3=118971
top5_4=115166
finite=PASS
pos=12
top1=108809
top1_logit_u6=13828630
top5_0=108809
top5_1=112580
top5_2=45156
top5_3=5284
top5_4=118971
finite=PASS
pos=13
top1=103630
top1_logit_u6=13711439
top5_0=103630
top5_1=108809
top5_2=5284
top5_3=58496
top5_4=51517
finite=PASS
pos=14
top1=103630
top1_logit_u6=13889061
top5_0=103630
top5_1=108809
top5_2=5284
top5_3=53385
top5_4=118971
finite=PASS
pos=15
top1=26381
top1_logit_u6=12997713
top5_0=26381
top5_1=30741
top5_2=17429
top5_3=1305
top5_4=121934
finite=PASS
pos=16
top1=5215
top1_logit_u6=14311237
top5_0=5215
top5_1=53741
top5_2=82060
top5_3=15215
top5_4=82263
finite=PASS
finite_gate=PASS
no Metal/CUDA execution claim
no full-model payload-residency claim
```

`solum.read_range` of 5_948_480 bytes **passed**. Admit, tokenizer, all
24 layer materializations, and `dense.forward` completed. Finite gate
holds on every window position. First failing oracle under gi0 vs the
pinned llama.cpp comparator (GATE 9 probe, not re-run): position 0
top-1 `7` vs comparator `304` (` in`). Observed top-5 at position 0
`[7, 220, 12, 103630, 320]` does not contain `304`. Stop rule: record
exactly, do not chase. No Metal/CUDA or payload-residency claim.

Toolchain: rustc 1.97.1 (8bab26f4f 2026-07-14) Homebrew, cargo 1.97.1
(c980f4866 2026-06-30). Host: Darwin 25.5.0 arm64
(`burgus.local`, `RELEASE_ARM64_T6050`, Apple M5 Max).

### GATE 12 revisions

| Surface | Revision |
| --- | --- |
| packet gradus | this commit (GATE 12 receipt; parent `05f5a3a`) |
| packet radix (readable) | `1abb7c291` |
| faber binary used | packet `target/debug/faber` 1.7.0 at `1abb7c291` |
| workspace faber | `0fe3a00` (via `FABER_SUPPORT_PATH_OVERRIDE`; not written) |
| workspace / packet hosts | `a6c8129` (64 MiB `solum` cap; via override; not written) |
| workspace norma | `7d71daf` (read via `FABER_LIBRARY_HOME`; not written) |

## GATE 11 (2026-08-18)

**Verdict: ORACLE REACHED — finite PASS; first-divergence vs comparator
top-1.** Handle `f95dd328` / packet `hand-15`. Gradus main `b52f7d8`
(commit `37cdf7c` token-major gather, no transpose; tied `lm_head`
transposes the view). Readable radix `8da2f4966`. Workspace hosts
`a6c8129` (64 MiB `solum` range cap) via `FABER_SUPPORT_PATH_OVERRIDE`.
Packet `cargo build -p faber` green. `faber build --target rust`
printed the binary (`Finished dev` in 4.13s, 0 rustc errors, 616
warnings). Execution of the printed binary **passed**
`solum.read_range` of the 5_948_480-byte table prefix, printed
architecture facts, matched the pinned tokenizer ids, loaded all 24
layers, completed `dense.forward` (`logits_shape=[17,151936]`), and
printed top-1 / top-5 for window positions 0..16. `finite_gate=PASS`.
Observed position-0 top-1 `89` vs the GATE 9 pinned-comparator
observation `304` (` in`). GATE 10's post-transpose top-1 was `86331`;
the gather fix moved the observed token and did not match the
comparator. Existing probe evidence (U1.9 TRACE on the shared
`dense.forward` gather / layer-0 Q path) names the next first-divergence
op as layer-0 Q `nn.linear`. This gate did not chase or retune that op.
No in-binary `PREFILL:` line (this consumer does not call the golden
file). Exit 0. Numerics were not tuned. TARGETLANE001 was not weakened
(`[build] target = "fmir"` stays).

### Packet faber rebuild (green)

From the hand packet:

```text
cd /Users/ianzepp/work/faberlang/worktrees/hand-15/radix
cargo build -p faber
```

Exit 0 in 12.75s. Binary
`/Users/ianzepp/work/faberlang/worktrees/hand-15/radix/target/debug/faber`
(`faber 1.7.0`, mtime 2026-08-18 07:50, 94,986,680 bytes) at radix
`8da2f4966`.

### Rust-target emit (clean)

```text
cd /Users/ianzepp/work/faberlang/worktrees/hand-15/gradus
env FABER_SUPPORT_PATH_OVERRIDE=/Users/ianzepp/work/faberlang \
  FABER_LIBRARY_HOME=/Users/ianzepp/work/faberlang \
  /Users/ianzepp/work/faberlang/worktrees/hand-15/radix/target/debug/faber \
  build --target rust exempla/dense-prefill-qwen2
```

`FABER_LIBRARY_HOME` is the workspace container (has `gradus/` +
`norma/`). Packet `hand-15` has no `norma` member; workspace `gradus`
is the same commit as the packet member (`b52f7d8`). Faber compiled
the package, emitted `exempla/dense-prefill-qwen2/target/faber`, and
invoked Cargo.

```text
warning: `dense-prefill-qwen2` (bin "dense-prefill-qwen2") generated 616 warnings
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 4.13s
/Users/ianzepp/work/faberlang/worktrees/hand-15/gradus/exempla/dense-prefill-qwen2/target/debug/dense-prefill-qwen2
```

Exit 0. Printed binary present (3,841,768 bytes, mtime 2026-08-18 07:53).
Zero rustc errors.

### Observed execution

```text
/Users/ianzepp/work/faberlang/worktrees/hand-15/gradus/exempla/dense-prefill-qwen2/target/debug/dense-prefill-qwen2 \
  /Users/ianzepp/ai/models/Qwen2.5-0.5B-Instruct-Q4_K_M.gguf \
  5948480 \
  6eb923e7d26e9cea28811e1a8e852009b21242fb157b26149d3b188f3a8c8653
```

Start `2026-08-18T12:01:11Z`. End `2026-08-18T12:27:19Z`. Exit 0.
`/usr/bin/time -l`: 1567.78 real, 1424.10 user, 160.65 sys, max RSS
9,449,521,152 bytes (~8.80 GiB).

Stdout (verbatim, layer-load rows elided as `...`):

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
logits_shape=[17,151936]
pos=0
top1=89
top1_logit_u6=13743888
top5_0=89
top5_1=126318
top5_2=118150
top5_3=1579
top5_4=145768
finite=PASS
pos=1
top1=126318
top1_logit_u6=14343148
top5_0=126318
top5_1=94553
top5_2=147747
top5_3=42413
top5_4=12108
finite=PASS
pos=2
top1=1003
top1_logit_u6=13784768
top5_0=1003
top5_1=92320
top5_2=86249
top5_3=133919
top5_4=3314
finite=PASS
pos=3
top1=103140
top1_logit_u6=13248098
top5_0=103140
top5_1=376
top5_2=1282
top5_3=111414
top5_4=89
finite=PASS
pos=4
top1=86260
top1_logit_u6=12481638
top5_0=86260
top5_1=524
top5_2=21625
top5_3=37056
top5_4=55
finite=PASS
pos=5
top1=63945
top1_logit_u6=13927048
top5_0=63945
top5_1=12108
top5_2=70613
top5_3=72328
top5_4=11275
finite=PASS
pos=6
top1=38907
top1_logit_u6=12745317
top5_0=38907
top5_1=74903
top5_2=19506
top5_3=110157
top5_4=91586
finite=PASS
pos=7
top1=117282
top1_logit_u6=14596547
top5_0=117282
top5_1=78328
top5_2=92320
top5_3=104089
top5_4=1003
finite=PASS
pos=8
top1=79874
top1_logit_u6=15861243
top5_0=79874
top5_1=95266
top5_2=91413
top5_3=98415
top5_4=19251
finite=PASS
pos=9
top1=92320
top1_logit_u6=15117314
top5_0=92320
top5_1=70613
top5_2=62917
top5_3=52243
top5_4=87478
finite=PASS
pos=10
top1=99384
top1_logit_u6=11910970
top5_0=99384
top5_1=3314
top5_2=738
top5_3=1599
top5_4=55
finite=PASS
pos=11
top1=117282
top1_logit_u6=10908234
top5_0=117282
top5_1=36
top5_2=580
top5_3=404
top5_4=55
finite=PASS
pos=12
top1=91413
top1_logit_u6=13841490
top5_0=91413
top5_1=33724
top5_2=1473
top5_3=37994
top5_4=86224
finite=PASS
pos=13
top1=101621
top1_logit_u6=12566185
top5_0=101621
top5_1=60726
top5_2=99148
top5_3=101171
top5_4=72109
finite=PASS
pos=14
top1=92320
top1_logit_u6=15058613
top5_0=92320
top5_1=113347
top5_2=70613
top5_3=94469
top5_4=11844
finite=PASS
pos=15
top1=285
top1_logit_u6=14775967
top5_0=285
top5_1=71
top5_2=75
top5_3=66
top5_4=44
finite=PASS
pos=16
top1=97245
top1_logit_u6=13277365
top5_0=97245
top5_1=122137
top5_2=79360
top5_3=87478
top5_4=66454
finite=PASS
finite_gate=PASS
no Metal/CUDA execution claim
no full-model payload-residency claim
```

`solum.read_range` of 5_948_480 bytes **passed**. Admit, tokenizer, all
24 layer materializations, and `dense.forward` completed. Finite gate
holds on every window position. First failing oracle under gi0 vs the
pinned llama.cpp comparator (GATE 9 probe, not re-run): position 0
top-1 `89` vs comparator `304` (` in`). Observed top-5 at position 0
`[89, 126318, 118150, 1579, 145768]` does not contain `304`. Position 8
top-1 is `79874` (this consumer's 17-token manifest window; not the
SmolLM2 GI2-3 9-token / pos-8 row). Stop rule: record exactly, do not
chase. No Metal/CUDA or payload-residency claim.

Toolchain: rustc 1.97.1 (8bab26f4f 2026-07-14) Homebrew, cargo 1.97.1
(c980f4866 2026-06-30). Host: Darwin 25.5.0 arm64
(`burgus.local`, `RELEASE_ARM64_T6050`, Apple M5 Max).

### GATE 11 revisions

| Surface | Revision |
| --- | --- |
| packet gradus | this commit (GATE 11 receipt; parent `b52f7d8`) |
| packet radix (readable) | `8da2f4966` |
| faber binary used | packet `target/debug/faber` 1.7.0 at `8da2f4966` |
| workspace faber | `afd2a96` (via `FABER_SUPPORT_PATH_OVERRIDE`; not written) |
| workspace / packet hosts | `a6c8129` (64 MiB `solum` cap; via override; not written) |
| workspace norma | `7d71daf` (read via `FABER_LIBRARY_HOME`; not written) |

## GATE 10 (2026-08-18)

**Verdict: ORACLE REACHED — finite PASS; first-divergence vs comparator
top-1.** Handle `6c0fc2cb` / packet `test-1`. Writable radix
`693d74e3e` (carries `234d44edf` / `1bc63c590` borrow field access +
lazy ranges, plus the kernel batches). Workspace hosts `a6c8129`
(64 MiB `solum` range cap) via `FABER_SUPPORT_PATH_OVERRIDE`. Packet
`cargo build -p faber` green. `faber build --target rust` printed the
binary (`Finished dev` in 1.12s, 0 rustc errors, 616 warnings).
Execution of the printed binary **passed** `solum.read_range` of the
5_948_480-byte table prefix, printed architecture facts, matched the
pinned tokenizer ids, loaded all 24 layers, completed `dense.forward`
(`logits_shape=[17,151936]`), and printed top-1 / top-5 for window
positions 0..16. `finite_gate=PASS`. Observed position-0 top-1 `86331`
vs the GATE 9 pinned-comparator observation `304`. No in-binary
`PREFILL:` line (this consumer does not call the golden file). Exit 0.
Numerics were not tuned. TARGETLANE001 was not weakened
(`[build] target = "fmir"` stays).

### Packet faber rebuild (green)

From the test packet:

```text
cd /Users/ianzepp/work/faberlang/worktrees/test-1/radix
cargo build -p faber
```

Exit 0 in 12.67s. Binary
`/Users/ianzepp/work/faberlang/worktrees/test-1/radix/target/debug/faber`
(`faber 1.7.0`, mtime 2026-08-18 04:24, 94,931,240 bytes) at radix
`693d74e3e`.

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

```text
warning: `dense-prefill-qwen2` (bin "dense-prefill-qwen2") generated 616 warnings
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 1.12s
/Users/ianzepp/work/faberlang/worktrees/test-1/gradus/exempla/dense-prefill-qwen2/target/debug/dense-prefill-qwen2
```

Exit 0. Printed binary present (3,840,936 bytes, mtime 2026-08-18 04:24).
Zero rustc errors. Generated `_transpose` indexes `t.data.get(...)`
(one `f32` `.cloned()`); no per-element `t.data.clone()`.
`[896, 151936]` is linear.

### Observed execution

```text
/Users/ianzepp/work/faberlang/worktrees/test-1/gradus/exempla/dense-prefill-qwen2/target/debug/dense-prefill-qwen2 \
  /Users/ianzepp/ai/models/Qwen2.5-0.5B-Instruct-Q4_K_M.gguf \
  5948480 \
  6eb923e7d26e9cea28811e1a8e852009b21242fb157b26149d3b188f3a8c8653
```

Start `2026-08-18T08:32:54Z`. End `2026-08-18T08:57:27Z`. Exit 0.
`/usr/bin/time -l`: 1473.30 real, 1354.96 user, 144.09 sys, max RSS
9,543,073,792 bytes (~8.89 GiB). After `loaded_layer=23` the process
entered `run_forward` → `dense.forward` → `_block` → `nn.linear` →
`math.matmul` (sample at +13m26s). The GATE 9 `_transpose` wall did
not reproduce.

Stdout (verbatim, layer-load rows elided as `...`):

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
logits_shape=[17,151936]
pos=0
top1=86331
top1_logit_u6=15991603
top5_0=86331
top5_1=71099
top5_2=135603
top5_3=55867
top5_4=54130
finite=PASS
pos=1
top1=2116
top1_logit_u6=14522848
top5_0=2116
top5_1=21359
top5_2=58260
top5_3=144044
top5_4=77553
finite=PASS
pos=2
top1=110011
top1_logit_u6=17487878
top5_0=110011
top5_1=4283
top5_2=107323
top5_3=127931
top5_4=6075
finite=PASS
pos=3
top1=5947
top1_logit_u6=19365798
top5_0=5947
top5_1=21354
top5_2=27498
top5_3=95547
top5_4=150203
finite=PASS
pos=4
top1=144211
top1_logit_u6=17469470
top5_0=144211
top5_1=56376
top5_2=82194
top5_3=92050
top5_4=113988
finite=PASS
pos=5
top1=127931
top1_logit_u6=14927091
top5_0=127931
top5_1=114794
top5_2=95445
top5_3=127159
top5_4=45499
finite=PASS
pos=6
top1=97514
top1_logit_u6=14617112
top5_0=97514
top5_1=96847
top5_2=73217
top5_3=75707
top5_4=138719
finite=PASS
pos=7
top1=13115
top1_logit_u6=15977356
top5_0=13115
top5_1=78570
top5_2=17462
top5_3=20453
top5_4=57841
finite=PASS
pos=8
top1=144044
top1_logit_u6=13031783
top5_0=144044
top5_1=53134
top5_2=112352
top5_3=139516
top5_4=58417
finite=PASS
pos=9
top1=32955
top1_logit_u6=15313214
top5_0=32955
top5_1=27633
top5_2=90602
top5_3=142565
top5_4=120763
finite=PASS
pos=10
top1=97976
top1_logit_u6=13759730
top5_0=97976
top5_1=91329
top5_2=15577
top5_3=48689
top5_4=85924
finite=PASS
pos=11
top1=98724
top1_logit_u6=14403866
top5_0=98724
top5_1=52680
top5_2=41909
top5_3=78129
top5_4=148516
finite=PASS
pos=12
top1=136537
top1_logit_u6=16010382
top5_0=136537
top5_1=75370
top5_2=102622
top5_3=144044
top5_4=63071
finite=PASS
pos=13
top1=75370
top1_logit_u6=14738933
top5_0=75370
top5_1=58417
top5_2=135614
top5_3=68795
top5_4=63071
finite=PASS
pos=14
top1=15035
top1_logit_u6=16036158
top5_0=15035
top5_1=6971
top5_2=97514
top5_3=104682
top5_4=123794
finite=PASS
pos=15
top1=70890
top1_logit_u6=16639503
top5_0=70890
top5_1=107626
top5_2=47910
top5_3=110651
top5_4=44347
finite=PASS
pos=16
top1=140091
top1_logit_u6=17798684
top5_0=140091
top5_1=32234
top5_2=37947
top5_3=26858
top5_4=101226
finite=PASS
finite_gate=PASS
no Metal/CUDA execution claim
no full-model payload-residency claim
```

`solum.read_range` of 5_948_480 bytes **passed**. Admit, tokenizer, all
24 layer materializations, and `dense.forward` completed. Finite gate
holds on every window position. First failing oracle under gi0 vs the
pinned llama.cpp comparator (GATE 9 probe, not re-run): position 0
top-1 `86331` vs comparator `304` (` in`). Observed top-5 at position 0
`[86331, 71099, 135603, 55867, 54130]` does not contain `304`. Stop
rule: record exactly, do not chase. No Metal/CUDA or payload-residency
claim.

Repair of the numeric divergence belongs to the U1.8 dense forward /
dequant / bias-omission surface (this file still synthesizes zero
`attn_{q,k,v}.bias`; the real file carries those tensors). That surface
is not writable in this test packet.

Toolchain: rustc 1.97.1 (8bab26f4f 2026-07-14) Homebrew, cargo 1.97.1
(c980f4866 2026-06-30). Host: Darwin 25.5.0 arm64
(`burgus.local`, `RELEASE_ARM64_T6050`, Apple M5 Max).

## Prior stops

### 2026-08-18 GATE 9 — embed `_transpose` clone (radix `5088c4397` / hosts `a6c8129`)

Packet `faber` green. Rust emit 0 errors / 616 warnings. Printed binary
passed the 5.95 MiB prefix, admit, tokenizer, and all 24 layer loads,
then sat in generated `_transpose` of `model.embed_tokens`
`[896, 151936]`, cloning `t.data` (~518 MiB) per element. SIGTERM after
19m47s (exit 143). No logits. Closed on radix `234d44edf` / `1bc63c590`.
Did not reproduce on GATE 10.

### 2026-08-18 GATE 8 — sermo materialization (radix `5088c4397` / hosts `bf11418`)

Packet `faber` green. Rust emit 0 errors / 616 warnings. Printed binary
panicked on the first `solum.read_range` of the 5_948_480-byte prefix:
`failable call failed: "sermo materialization failed"`. Closed on hosts
`a6c8129`. Did not reproduce on GATE 9 or 10.

### 2026-08-17, handle `836c3b55` (FINAL) — rustc 248

Readable radix `2ed9914e4`. Packet `faber` green. Rust emit cleared the
runtime-plan gate; cargo failed rustc 248 errors (first `E0015` const
`vec!` for `PINNED_TOKENS`). Did not reproduce on GATE 8, 9, or 10.

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
GATE 8, 9, or 10.

## Pinned row facts

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
| logits_shape | `[17, 151936]` |
| Observed pos-0 top-1 / top-5 | `86331` / `[86331, 71099, 135603, 55867, 54130]` |
| Comparator pos-0 top-1 (GATE 9 probe) | `304` (` in`) |
| finite_gate | PASS (all 17 positions) |
| first_divergence | position 0: top-1 86331 vs comparator 304 |
| Backend (declared) | CPU/reference |
| Hardware/OS | Darwin 25.5.0 arm64 (`burgus.local`, `RELEASE_ARM64_T6050`, Apple M5 Max) |
| Gradus | this commit (GATE 10 receipt; parent `3d915aa`) |
| Radix | `693d74e3e` (writable; packet `faber` rebuild green) |
| Faber | packet 1.7.0 at `693d74e3e` (mtime 2026-08-18 04:24); workspace `afd2a96` via `FABER_SUPPORT_PATH_OVERRIDE` |
| Hosts (read via override) | `a6c8129` (64 MiB `solum` cap) |
| Norma (read via libhome) | `7d71daf` |
| Comparator binary | `/opt/homebrew/Cellar/llama.cpp/10150/bin/llama-server` SHA-256 `e5c153a1237e1c8e14ce0721d9afba4fd07936c7dc17dc7bd156d4dbe454952a`, version 10150 (`dee2a846b`) |

The real file carries `attn_q.bias` / `attn_k.bias` / `attn_v.bias`.
The U1.8 surface synthesizes zero biases and does not resolve those
tensors. That architecture fact is recorded; it was not used to change
the surface (stop rule: do not tune). GATE 10 materialized the U1.8
lookups and ran `forward`; those bias tensors were still not consumed.

Comparator-only observation from GATE 9 (not re-run on GATE 10):
`/completion` on the pinned token array, `n_predict=1`, `n_probs=5`,
`temperature=0`, `seed=42`, CPU (`--n-gpu-layers 0`), ephemeral port
8310 (not 18173 / 59414), generation position 0 top-1 token id 304
(` in`).
