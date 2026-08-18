# dense-prefill-smollm2 — REF-01-U1.9 SmolLM2 prefill-logit receipt

Consumer for the U1.8 dense forward graph against the pinned SmolLM2-360M
row on the **compiled rust** receipt tier. This README is the unit receipt.

**TRACE 2026-08-18 (handle `1265695e` / packet `hand-48`)** — post-attn
families at layer-0 pos 8 / token 2767, compiled rust. Isolated ops
through `ffn_down` are green. First red was `dense_block` residual-2
wiring (`ln2 + h` vs llama/GI2-1 `r1 + h`) at max_delta `2.6446362`
(960/960). Fixed in `transformer.dense_block`; U1.5 pins re-evaluated
in independent f64.

| probe | vs | max_delta | n>1e-6 |
| --- | --- | --- | --- |
| post-attn RMSNorm | GI2-1 `ffn-normed` (no GI2-2 `ffn_norm.y`) | 3.58e-7 | 0/960 |
| SwiGLU activation `silu(gate)·up` | GI2-2 `swiglu.y` | 4.77e-7 | 0/2560 |
| `ffn_down` | GI2-1 naive-f32 `swiglu.y · wd` | 0 | 0/960 |
| residual-2 `r1 + h` | GI2-1 | 0 | 0/960 |
| residual-2 `ln2 + h` (old block) | GI2-1 `r1 + h` | **2.6446362** | **960/960** |

GATE 13 is the whole-model rerun after that residual-2 fix plus the
already-landed MHA `[K,N]` wo / U1.5 re-pins.

## GATE 13 (2026-08-18)

**Verdict: PASS — PREFILL PASS (top-1 exact, top-5 5/5).** Handle
`f2513397` / packet `merge`. Gradus merged tip `03f3c42` (hand-48
residual-2 `c2d42fb` + already-landed MHA `05555b1` / U1.5 `84a4005`;
hand-49 Qwen2 QKV bias `42edb18`; hand-55 SG-3D `1eb9469`). Packet
radix `b53b2eb7b`. Hosts `a6c8129` (64 MiB `solum` range cap) via
`FABER_SUPPORT_PATH_OVERRIDE=/Users/ianzepp/work/faberlang`.
`FABER_LIBRARY_HOME=/Users/ianzepp/work/faberlang/worktrees/merge`
(full-membership packet: `gradus` + `norma`). Packet
`cargo build -p faber` green. Packet-radix `faber build --target rust`
printed the binary (`Finished dev` in 6.13s, 0 rustc errors, 711
warnings). Execution of the printed binary **passed**
`solum.read_range` of the 1_787_040-byte table prefix, admitted the
GGUF, matched the pinned tokenizer ids, loaded all 32 layers, printed
`forward start T=9`, and returned `forward done shape=[9,49152]`. gi0
at prompt-end / position 0 (last prefill row 8): `all_finite=true`,
observed top-1 `30` vs golden `30`, top-5 overlap `5/5`
(`[30, 28, 1270, 365, 198]` exact). `first_divergence=none`.
`PREFILL: PASS`. Exit 0.

Top-1 history: GATE 10 (wrong gather) `40983` → GATE 11 (gather
fixed) `45361` → GATE 12 (gather + all linear K-major) `5762` →
GATE 13 (MHA wo `[K,N]` + residual-2 `r1 + h`) `30` = golden `30`.
Every named cause on this row is closed. Numerics were not tuned.
TARGETLANE001 was not weakened (`[build] target` is still `"fmir"`).

### Packet faber rebuild (green)

From the merge packet:

```text
cd /Users/ianzepp/work/faberlang/worktrees/merge/radix
cargo build -p faber
```

`cargo build -p faber` at packet radix `b53b2eb7b` exits 0
(Finished `dev` profile in 18.01s). Packet binary:
`/Users/ianzepp/work/faberlang/worktrees/merge/radix/target/debug/faber`
(`faber 1.7.0`, rustc 1.97.1 Homebrew, mtime 2026-08-18 12:20,
95,158,136 bytes).

### Rust-target emit (clean)

```text
cd /Users/ianzepp/work/faberlang/worktrees/merge/gradus
env FABER_SUPPORT_PATH_OVERRIDE=/Users/ianzepp/work/faberlang \
  FABER_LIBRARY_HOME=/Users/ianzepp/work/faberlang/worktrees/merge \
  /Users/ianzepp/work/faberlang/worktrees/merge/radix/target/debug/faber \
  build --target rust exempla/dense-prefill-smollm2
```

```text
warning: `dense-prefill-smollm2` (bin "dense-prefill-smollm2") generated 711 warnings
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 6.13s
/Users/ianzepp/work/faberlang/worktrees/merge/gradus/exempla/dense-prefill-smollm2/target/debug/dense-prefill-smollm2
```

Exit 0. Printed binary present (4,073,176 bytes, mtime 2026-08-18 12:21).
Zero rustc errors.

### Observed execution (2026-08-18 GATE 13)

```text
/Users/ianzepp/work/faberlang/worktrees/merge/gradus/exempla/dense-prefill-smollm2/target/debug/dense-prefill-smollm2 \
  /Users/ianzepp/ai/models/SmolLM2-360M-Instruct-Q4_K_M.gguf \
  1787040 \
  2fa3f013dcdd7b99f9b237717fa0b12d75bbb89984cc1274be1471a465bac9c2
```

Start `2026-08-18T16:22:03Z`. End `2026-08-18T16:29:34Z`. Exit 0.
`/usr/bin/time -l`: 450.95 real, 345.76 user, 124.84 sys, max RSS
3,865,214,976 bytes (~3.60 GiB).

Stdout (verbatim, layer-load rows elided as `...`):

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
model_shape layers=32 heads=15 kv_heads=5 head_dim=64 hidden=960 vocab=49152
stored_embed_shape=[960,49152]
loaded layer 0
...
loaded layer 31
forward start T=9
forward done shape=[9,49152]
position=0 (prompt end, last prefill row 8)
observed_top1_non_eog=30
golden_top1_non_eog=30
top1_matches=true
observed_top5=[30, 28, 1270, 365, 198]
golden_top5=[30, 28, 1270, 365, 198]
top5_overlap=5/5
all_finite=true
band: not_compared (no golden file)
first_divergence=none
PREFILL: PASS
```

Stop rule: record exactly. No Metal/CUDA or payload-residency claim.

Toolchain: rustc 1.97.1 (8bab26f4f 2026-07-14) Homebrew, cargo 1.97.1
(c980f4866 2026-06-30). Host: Darwin 25.5.0 arm64
(`burgus.local`, `RELEASE_ARM64_T6050`, Apple M5 Max).

### GATE 13 revisions

| Surface | Revision |
| --- | --- |
| packet gradus | this commit (GATE 13 receipt; parent `03f3c42`) |
| packet radix | `b53b2eb7b` |
| faber binary used | packet `target/debug/faber` 1.7.0 at `b53b2eb7b` |
| workspace faber | `0fe3a00` (via `FABER_SUPPORT_PATH_OVERRIDE`; not written) |
| workspace / packet hosts | `a6c8129` (64 MiB `solum` cap; via override; not written) |
| packet norma | `7d71daf` (read via `FABER_LIBRARY_HOME`; not written) |

**Verdict: PASS — remaining linear families are the same GGUF K-major
layout as `attn_q`.** Handle `8da95e6c` / packet `hand-25`. The Q adapter
transpose already named q/k/v/o/gate/up/down; compiled-rust probes confirm
every remaining consumer. Without the transpose, V/O/gate/up fail GI2-2
by `0.25`–`3.13` (100% of elements). With it, every GI2-2 activation
probe is `< 1e-6`. `ffn_down` and tied `lm_head` have no per-op golden;
GI2-1 dequant + first-row slice pass at `0`.

Oracle (compiled rust `trace`, packet `hand-25`):

| tensor | stored | adapter → nn.linear | method | max_delta | n > 1e-6 |
| --- | --- | --- | --- | --- | --- |
| gather | Q8_0 `[960,49152]` token-major | n/a | GI2-2 `rms_norm.x` | 0 | 0 / 960 |
| `nn.rmsnorm` | F32 `[960]` | n/a | GI2-2 `rms_norm.y` | 1.19e-7 | 0 / 960 |
| `attn_q` | Q5_0 `[960,960]` K-major | `[960,960]` row-major | GI2-2 `dense.y` | **3.58e-7** | **0 / 64** |
| `attn_k` | Q5_0 `[960,320]` K-major | `[960,320]` row-major | GI2-1 dequant+row0 | **0** | **0 / 32** |
| `attn_v` | Q8_0 `[960,320]` K-major | `[960,320]` row-major | GI2-2 `attention.v` pos8 | **5.96e-8** | **0 / 320** |
| `attn_output` | Q5_0 `[960,960]` K-major | `[960,960]` row-major | GI2-2 `residual.b` | **0** | **0 / 960** |
| `ffn_gate` | Q5_0 `[960,2560]` K-major | `[960,2560]` row-major | GI2-2 `swiglu.gate` | **7.15e-7** | **0 / 2560** |
| `ffn_up` | Q5_0 `[960,2560]` K-major | `[960,2560]` row-major | GI2-2 `swiglu.up` | **4.77e-7** | **0 / 2560** |
| `ffn_down` | Q6_K `[2560,960]` K-major | `[2560,960]` row-major | GI2-1 dequant+row0 | **0** | **0 / 32** |
| `lm_head` | tied `token_embd` Q8_0 | `dense.forward` `[D,V]` transpose | GI2-1 embed head | **0** | **0 / 32** |

No-transpose reds (Python GI2-1 matmul vs the same goldens): V `0.251`, O `3.025`, gate `3.126`, up `1.990`. K has no pre-rope GI2-2; rust `nn.linear` vs independent GI2-1 matmul is `2.15e-6` (accumulation, not layout). GATE 12 re-ran the full prefill binary after that sweep: observed top-1 `5762` vs GI2-3 golden `30`. U1.9 is not CLOSE.

## GATE 12.5 (2026-08-18) — attention softmax/mask probe

Handle `52d14758` / packet `hand-46`. First unprobed family after the
weight-path sweep. GI2-2 `attention.json` has **no softmax golden** —
`expected_output` is the post-softmax × V **context** (960). The GI2-1
CPU reference is the same recipe: consecutive GQA `g = h / (H/K)`,
scale `0.125`, causal prefix `j ≤ i` (diagonal included), max-subtracted
row softmax. Independent numpy of that recipe matches the GI2-2 context
at `4.47e-8`. Off-by-one masks (`j < i`, last-key dropped, row-0-only)
miss at `0.03`–`0.21`.

Compiled-rust `trace` (packet faber `7485899bb`, 2026-08-18). Oracle
**met** for the assigned family:

| probe | method | max_delta | n > 1e-6 |
| --- | --- | --- | --- |
| `mask_construction` | zero scores, `v[:,0] = t+1` | row0=1, row7=4.5, row8=5 | **PASS** |
| `attn_context_from_gi22_qkv` | GI2-2 q/k/v → `scaled_dot_product_causal` | **2.98e-8** | **0 / 960** |
| `attn_context_live` | live Q/K/V + RoPE + causal × V | **7.45e-8** | **0 / 960** |
| `live_rope_q_pos8` | live post-rope Q vs GI2-2 `q` | 2.38e-6 | 2 / 960 (rope f32, not mask) |
| `o_linear` | golden context × `wo` (`nn.linear`) | **0** | **0 / 960** |
| `o_linear_via_wo_T` | golden context × `woᵀ` (MHA extra transpose) | **3.025** | **960 / 960** |

No softmax/mask off-by-one. No softmax numeric miss at the 1e-6
oracle. The next local gradus surface is MHA's `out = concat · woᵀ`
(`attention.fab:940`) against the already-green `nn.linear(ctx, wo)`
layout. Not fixed here — that is the O-projection family, and changing
it breaks the U1.4 GQA pins that were computed with the transpose.

Qwen2 bias audit (same unit, not a SmolLM2 fix): the pinned
`Qwen2.5-0.5B-Instruct-Q4_K_M.gguf` **does** carry QKV bias —
24 × `{attn_q,attn_k,attn_v}.bias` (72 F32 tensors; q `[896]`, k/v
`[128]`; no `attn_output.bias`). SmolLM2 has **zero** `.bias` tensors.
`dense.forward` still synthesizes zeros; `dense_qwen2` only maps
`.attn_*.weight`. Not a trivial local softmax fix.

## GATE 12 (2026-08-18)

**Verdict: ORACLE REACHED — PREFILL FAIL (first-divergence top-1).
U1.9 not CLOSE.** Handle `6d7c97dd` / packet `hand-34`. Gradus
`factory/hand-34` fast-forwarded `factory/hand-25` tip `05f5a3a`
(gather `37cdf7c`, Q/K-major SmolLM2 `012d411`, remaining-linear /
Qwen2 K-major `05f5a3a`). Readable packet radix `1abb7c291`. Hosts
`a6c8129` (64 MiB `solum` range cap) via
`FABER_SUPPORT_PATH_OVERRIDE=/Users/ianzepp/work/faberlang`.
`FABER_LIBRARY_HOME=/Users/ianzepp/work/faberlang` (workspace
container: packet has no `norma` member; `05f5a3a` is exempla-only so
workspace `gradus` library src matches the packet). Packet
`cargo build -p faber` green. Packet-radix `faber build --target rust`
**failed** SEM001/SEM008 on TRACE helper `_dump_head` (`string tag` —
`tag` is `TokenKind::Tag`; keyword-as-ident on `1abb7c291` does not
bind that name in `("trace." + tag + ".")`). Same 05f5a3a source
emitted cleanly with the GATE 11 faber (`hand-15` radix `8da2f4966`).
The printed binary passed `solum.read_range` of the 1_787_040-byte
table prefix, admitted the GGUF, matched the pinned tokenizer ids,
loaded all 32 layers, printed `forward start T=9`, and returned
`forward done shape=[9,49152]`. gi0 at prompt-end / position 0 (last
prefill row 8): `all_finite=true`, observed top-1 `5762` vs golden
`30`, top-5 overlap `0/5`.
`first_divergence=position 0: top-1 5762 vs golden 30`.
`PREFILL: FAIL`. Exit 0.

Top-1 history: GATE 10 (wrong gather) `40983` → GATE 11 (gather
fixed) `45361` → GATE 12 (gather + all linear K-major) `5762`. Still
not golden `30`. The sweep cleared gather / rmsnorm / rope / all
linears. First remaining unprobed op in `dense_block` program order is
**attention softmax/mask** inside `attention.multi_head_attention`
(Q/K/V linears and rope are green; O linear was probed from a *golden*
attention context, not from the graph's softmax). Next unprobed
families: residual adds, swiglu activation, cache/prefill
bookkeeping. This gate did not chase or retune those ops. Numerics
were not tuned. TARGETLANE001 was not weakened (`[build] target` is
still `"fmir"`).

### Packet faber rebuild (green)

From the hand packet:

```text
cd /Users/ianzepp/work/faberlang/worktrees/hand-34/radix
cargo build -p faber
```

`cargo build -p faber` at readable radix `1abb7c291` exits 0
(Finished `dev` profile in 21.79s). Packet binary:
`/Users/ianzepp/work/faberlang/worktrees/hand-34/radix/target/debug/faber`
(`faber 1.7.0`, rustc 1.97.1 Homebrew, mtime 2026-08-18 09:12,
95,042,760 bytes).

### Rust-target emit (packet radix SEM-red; GATE 11 faber clean)

Packet radix (`1abb7c291`):

```text
cd /Users/ianzepp/work/faberlang/worktrees/hand-34/gradus
env FABER_SUPPORT_PATH_OVERRIDE=/Users/ianzepp/work/faberlang \
  FABER_LIBRARY_HOME=/Users/ianzepp/work/faberlang \
  /Users/ianzepp/work/faberlang/worktrees/hand-34/radix/target/debug/faber \
  build --target rust exempla/dense-prefill-smollm2
```

```text
error[SEM001:unknown_identifier]: exempla/dense-prefill-smollm2/src/main.fab:25364
  |         print (("trace." + tag + ".") + (i ↦ string)) + "=" + ((xs.get(i) coalesce 0.0 ∷ f32) ↦ string)
error[SEM008:undefined_name]: exempla/dense-prefill-smollm2/src/main.fab:25364
  |         print (("trace." + tag + ".") + (i ↦ string)) + "=" + ((xs.get(i) coalesce 0.0 ∷ f32) ↦ string)
compilation failed
```

No packet-radix rust binary. `_dump_head` is TRACE-only; the full
prefill path does not call it. Qwen2 compiled on the same packet
radix (its `_band_row` uses `tag` in a name-slot that still binds).

Same 05f5a3a source with GATE 11 faber `8da2f4966`:

```text
cd /Users/ianzepp/work/faberlang/worktrees/hand-34/gradus
env FABER_SUPPORT_PATH_OVERRIDE=/Users/ianzepp/work/faberlang \
  FABER_LIBRARY_HOME=/Users/ianzepp/work/faberlang \
  /Users/ianzepp/work/faberlang/worktrees/hand-15/radix/target/debug/faber \
  build --target rust exempla/dense-prefill-smollm2
```

```text
warning: `dense-prefill-smollm2` (bin "dense-prefill-smollm2") generated 670 warnings
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 5.72s
/Users/ianzepp/work/faberlang/worktrees/hand-34/gradus/exempla/dense-prefill-smollm2/target/debug/dense-prefill-smollm2
```

Exit 0. Printed binary present (4,004,664 bytes, mtime 2026-08-18 09:59).
Zero rustc errors.

### Observed execution (2026-08-18 GATE 12)

```text
/Users/ianzepp/work/faberlang/worktrees/hand-34/gradus/exempla/dense-prefill-smollm2/target/debug/dense-prefill-smollm2 \
  /Users/ianzepp/ai/models/SmolLM2-360M-Instruct-Q4_K_M.gguf \
  1787040 \
  2fa3f013dcdd7b99f9b237717fa0b12d75bbb89984cc1274be1471a465bac9c2
```

Start `2026-08-18T13:59:41Z`. End `2026-08-18T14:10:57Z`. Exit 0.
`/usr/bin/time -l`: 675.62 real, 496.49 user, 184.78 sys, max RSS
3,868,803,072 bytes (~3.60 GiB).

Stdout (verbatim, layer-load rows elided as `...`):

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
model_shape layers=32 heads=15 kv_heads=5 head_dim=64 hidden=960 vocab=49152
stored_embed_shape=[960,49152]
loaded layer 0
...
loaded layer 31
forward start T=9
forward done shape=[9,49152]
position=0 (prompt end, last prefill row 8)
observed_top1_non_eog=5762
golden_top1_non_eog=30
top1_matches=false
observed_top5=[5762, 35077, 46137, 10624, 10998]
golden_top5=[30, 28, 1270, 365, 198]
top5_overlap=0/5
all_finite=true
band: not_compared (no golden file)
first_divergence=position 0: top-1 5762 vs golden 30
PREFILL: FAIL
```

Stop rule: record exactly, do not chase. No Metal/CUDA or
payload-residency claim.

Toolchain: rustc 1.97.1 (8bab26f4f 2026-07-14) Homebrew, cargo 1.97.1
(c980f4866 2026-06-30). Host: Darwin 25.5.0 arm64
(`burgus.local`, `RELEASE_ARM64_T6050`, Apple M5 Max).

### GATE 12 revisions

| Surface | Revision |
| --- | --- |
| packet gradus | this commit (GATE 12 receipt; parent `05f5a3a`) |
| packet radix (readable) | `1abb7c291` (SEM-red on `_dump_head` `tag`) |
| faber binary used for emit | GATE 11 `hand-15` `target/debug/faber` 1.7.0 at `8da2f4966` |
| packet faber (not used for SmolLM2 emit) | packet `target/debug/faber` 1.7.0 at `1abb7c291` |
| workspace faber | `0fe3a00` (via `FABER_SUPPORT_PATH_OVERRIDE`; not written) |
| workspace / packet hosts | `a6c8129` (64 MiB `solum` cap; via override; not written) |
| workspace norma | `7d71daf` (read via `FABER_LIBRARY_HOME`; not written) |

Prior diagnosis (handle `21b59246`) fixed gather. Layer-0 Q was the next
divergence after that landing.

Oracle (compiled rust `trace`, 88.3s): gather vs GI2-2 `rms_norm.x` at
pos 8 / token 2767 is `max_delta = 7.4e-9` (0 / 960 above `1e-6`).
`nn.rmsnorm` of that gather now matches GI2-2 `rms_norm.y` at
`9.2e-8`. Next divergence is layer-0 Q `nn.linear` vs GI2-2 `dense.y`
(`max_delta = 1.24`, 64 / 64). GATE 11 re-ran the full prefill binary
after that gather fix: observed top-1 `45361` vs GI2-3 golden `30`.

## GATE 11 (2026-08-18)

**Verdict: ORACLE REACHED — PREFILL FAIL (first-divergence top-1).**
Handle `f95dd328` / packet `hand-15`. Gradus main `b52f7d8` (commit
`37cdf7c` token-major gather, no transpose; tied `lm_head` transposes
the view). Readable radix `8da2f4966`. Hosts `a6c8129` (64 MiB `solum`
range cap) via `FABER_SUPPORT_PATH_OVERRIDE`. Packet `faber` rebuilt
green. Both exempla rebuilt + executed. The printed binary passed
`solum.read_range` of the 1_787_040-byte table prefix, admitted the
GGUF, matched the pinned tokenizer ids, loaded all 32 layers, printed
`forward start T=9`, and returned `forward done shape=[9,49152]`. gi0
at prompt-end / position 0 (last prefill row 8): `all_finite=true`,
observed top-1 `45361` vs golden `30`, top-5 overlap `0/5`.
`first_divergence=position 0: top-1 45361 vs golden 30`.
`PREFILL: FAIL`. Exit 0. GATE 10's post-transpose top-1 was `40983`;
the gather fix moved the observed token and did not match the golden.
Existing probe evidence (U1.9 TRACE / handle `21b59246`) already names
the next first-divergence op as layer-0 Q `nn.linear` vs GI2-2
`dense.y`. This gate did not chase or retune that op. Numerics were
not tuned. TARGETLANE001 was not weakened (`[build] target` is still
`"fmir"`).

### Packet faber rebuild (green)

From the hand packet:

```text
cd /Users/ianzepp/work/faberlang/worktrees/hand-15/radix
cargo build -p faber
```

`cargo build -p faber` at readable radix `8da2f4966` exits 0
(Finished `dev` profile in 12.75s). Packet binary:
`/Users/ianzepp/work/faberlang/worktrees/hand-15/radix/target/debug/faber`
(`faber 1.7.0`, rustc 1.97.1 Homebrew, mtime 2026-08-18 07:50,
94,986,680 bytes).

### Rust-target emit (clean)

```text
cd /Users/ianzepp/work/faberlang/worktrees/hand-15/gradus
env FABER_SUPPORT_PATH_OVERRIDE=/Users/ianzepp/work/faberlang \
  FABER_LIBRARY_HOME=/Users/ianzepp/work/faberlang \
  /Users/ianzepp/work/faberlang/worktrees/hand-15/radix/target/debug/faber \
  build --target rust exempla/dense-prefill-smollm2
```

`FABER_LIBRARY_HOME` is the workspace container (has `gradus/` +
`norma/`). Packet `hand-15` has no `norma` member; workspace `gradus`
is the same commit as the packet member (`b52f7d8`). Faber compiled
the package, emitted `exempla/dense-prefill-smollm2/target/faber`, and
invoked Cargo. Cargo compiled `dense-prefill-smollm2` against
workspace `solum` (`/Users/ianzepp/work/faberlang/hosts/crates/solum`,
`MAX_RANGE_READ_BYTES = 64 MiB`):

```text
warning: `dense-prefill-smollm2` (bin "dense-prefill-smollm2") generated 640 warnings
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 3.85s
/Users/ianzepp/work/faberlang/worktrees/hand-15/gradus/exempla/dense-prefill-smollm2/target/debug/dense-prefill-smollm2
```

Exit 0. Printed binary present (3,936,552 bytes, mtime 2026-08-18 07:52).
Zero rustc errors.

### Observed execution (2026-08-18 GATE 11)

```text
/Users/ianzepp/work/faberlang/worktrees/hand-15/gradus/exempla/dense-prefill-smollm2/target/debug/dense-prefill-smollm2 \
  /Users/ianzepp/ai/models/SmolLM2-360M-Instruct-Q4_K_M.gguf \
  1787040 \
  2fa3f013dcdd7b99f9b237717fa0b12d75bbb89984cc1274be1471a465bac9c2
```

Start `2026-08-18T11:53:17Z`. End `2026-08-18T12:00:48Z`. Exit 0.
`/usr/bin/time -l`: 450.23 real, 333.41 user, 130.36 sys, max RSS
3,886,399,488 bytes (~3.62 GiB).

Stdout (verbatim):

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
model_shape layers=32 heads=15 kv_heads=5 head_dim=64 hidden=960 vocab=49152
stored_embed_shape=[960,49152]
loaded layer 0
...
loaded layer 31
forward start T=9
forward done shape=[9,49152]
position=0 (prompt end, last prefill row 8)
observed_top1_non_eog=45361
golden_top1_non_eog=30
top1_matches=false
observed_top5=[45361, 5118, 4471, 44492, 38310]
golden_top5=[30, 28, 1270, 365, 198]
top5_overlap=0/5
all_finite=true
band: not_compared (no golden file)
first_divergence=position 0: top-1 45361 vs golden 30
PREFILL: FAIL
```

Stop rule: record exactly, do not chase. No Metal/CUDA or
payload-residency claim.

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

Prior diagnosis (handle `5830c444`) localized the first GI2-2 divergence to
the embedding gather. GATE 10 (receipt `dfa4fce`) had reached gi0 and failed
top-1 `40983` vs golden `30`. The gather-era notes below are historical.

Not comparison-side: tokenizer PASS, pinned ids
`[504, 2365, 6354, 16438, 27003, 690, 260, 23790, 2767]`, dump row is
position 8. Not emit: the raw token-major slice and `blk.0.attn_norm.weight`
match the GI2-2 fixtures (print-round max_delta `7.4e-9` / `5e-9`).
Mind routes the fix (skip the transpose, or materialize a true row-major
`[D, V]` before it).

## TRACE (2026-08-18, handle 5830c444)

Packet `faber` rebuilt at radix `017546a12`. Exemplum accepts a `trace`
4th argument, loads embed + layer-0 `attn_norm` + `attn_q` only, and
dumps prompt-end activations. Goldens:
`radix/crates/faber-prefill-oracle/testdata/gi2-2-op-goldens/`
(`rms_norm.json` / `dense.json`; pinned pos 8 / token 2767 / window 0).

Model-shape check (GGUF KV + exemplum `DenseConfig`): SmolLM2-360M-Instruct
(not 135M). `llama.block_count=32`, `llama.embedding_length=960`,
`llama.attention.head_count=15`, `head_count_kv=5`,
`llama.vocab_size=49152`, `llama.rope.freq_base=100000`,
`llama.attention.layer_norm_rms_epsilon=1e-5`. Admit: version=3,
data=1787040, tensors=290, architecture=llama. SHA-256
`2fa3f013dcdd7b99f9b237717fa0b12d75bbb89984cc1274be1471a465bac9c2`.

```text
stored_embed_shape=[960,49152]
transposed_embed_shape=[49152,960]
```

| probe | vs GI2-2 | max_delta | n > 1e-6 |
| --- | --- | --- | --- |
| raw token-major `data[2767*960 : +960]` | `rms_norm` input `x` | 7.4e-9 | 0 / 960 |
| **forward gather after `_transpose`** | **`rms_norm` input `x`** | **0.483** | **960 / 960** |
| `blk.0.attn_norm.weight` | `rms_norm` input `weight` | 5e-9 | 0 / 960 |
| `nn.rmsnorm(gathered)` pos 8 | `rms_norm` expected `y` | 1.314 | 959 / 960 |
| `nn.linear` Q head-0 pos 8 | `dense` expected `y` | 1.076 | 64 / 64 |

First four (raw matches golden `x`; gather matches the independent wrong
`[D, V]` row-major read):

```text
golden x / raw:  -0.09676552 -0.091389656  0.103933334  0.001791954
gathered pos8:   -0.07588482 -0.022281647  0.060310364  0.03855896
```

**First diverging layer + op:** layer 0 / embedding gather
(`gradus:model/dense` `_transpose` + `_collect`), before `rms_norm`.
**Class:** wiring bug (stored-layout / transpose). Not emit. Not
comparison (ids, position, non-EOG filter).

Command:

```text
.../dense-prefill-smollm2 \
  /Users/ianzepp/ai/models/SmolLM2-360M-Instruct-Q4_K_M.gguf \
  1787040 \
  2fa3f013dcdd7b99f9b237717fa0b12d75bbb89984cc1274be1471a465bac9c2 \
  trace
```

83.6s real, ~1.7 GiB RSS, exit 0. Numerics were not tuned. TARGETLANE001
was not weakened.

## Prior receipt (GATE 10 / dfa4fce) — oracle reached, not localized

**Verdict: ORACLE REACHED — PREFILL FAIL (first-divergence top-1).** GATE 10
(handle `6c0fc2cb` / packet `test-1`) at radix `693d74e3e` (carries
`234d44edf` / `1bc63c590` borrow field access + lazy ranges, plus the
kernel batches). Hosts `a6c8129` (64 MiB `solum` range cap). Packet
`faber` rebuilt green. Both exempla rebuilt + executed. Generated
`_transpose` now borrows `t.data` (no per-element `t.data.clone()`). The
printed binary passed `solum.read_range` of the 1_787_040-byte table
prefix, admitted the GGUF, matched the pinned tokenizer ids, loaded all
32 layers, printed `forward start T=9`, and returned
`forward done shape=[9,49152]`. gi0 at prompt-end / position 0:
`all_finite=true`, observed top-1 `40983` vs golden `30`, top-5 overlap
`0/5`. `first_divergence=position 0: top-1 40983 vs golden 30`.
`PREFILL: FAIL`. Exit 0. Numerics were not tuned. TARGETLANE001 was not
weakened (`[build] target` is still `"fmir"`).

## Comparison policy

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

## GATE 10 command (from the test packet)

```text
cd /Users/ianzepp/work/faberlang/worktrees/test-1/radix
cargo build -p faber
```

`cargo build -p faber` at writable radix `693d74e3e` exits 0
(Finished `dev` profile in 12.67s). Packet binary:
`/Users/ianzepp/work/faberlang/worktrees/test-1/radix/target/debug/faber`
(`faber 1.7.0`, rustc 1.97.1 Homebrew, mtime 2026-08-18 04:24,
94,931,240 bytes).

```text
cd /Users/ianzepp/work/faberlang/worktrees/test-1/gradus
env FABER_SUPPORT_PATH_OVERRIDE=/Users/ianzepp/work/faberlang \
  FABER_LIBRARY_HOME=/Users/ianzepp/work/faberlang/worktrees/test-1 \
  /Users/ianzepp/work/faberlang/worktrees/test-1/radix/target/debug/faber \
  build --target rust exempla/dense-prefill-smollm2
```

## Observed rust emit (2026-08-18 GATE 10)

Faber compiled the package, emitted
`exempla/dense-prefill-smollm2/target/faber`, and invoked Cargo.
Cargo compiled `dense-prefill-smollm2` against workspace `solum`
(`/Users/ianzepp/work/faberlang/hosts/crates/solum`,
`MAX_RANGE_READ_BYTES = 64 MiB`):

```text
warning: `dense-prefill-smollm2` (bin "dense-prefill-smollm2") generated 607 warnings
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.96s
/Users/ianzepp/work/faberlang/worktrees/test-1/gradus/exempla/dense-prefill-smollm2/target/debug/dense-prefill-smollm2
```

Exit 0. Printed binary present (3,882,536 bytes, mtime 2026-08-18 04:24).
Zero rustc errors.

Generated `_transpose` (dense, `target/faber/src/main.rs:4225-4254`)
indexes `t.data.get(...)` then `.cloned()` of one `f32`. There is no
`t.data.clone()` inside the element loop. Same for the attention
`_transpose` at `1733`. `[960, 49152]` is linear.

## Observed execution (2026-08-18 GATE 10)

```text
/Users/ianzepp/work/faberlang/worktrees/test-1/gradus/exempla/dense-prefill-smollm2/target/debug/dense-prefill-smollm2 \
  /Users/ianzepp/ai/models/SmolLM2-360M-Instruct-Q4_K_M.gguf \
  1787040 \
  2fa3f013dcdd7b99f9b237717fa0b12d75bbb89984cc1274be1471a465bac9c2
```

Start `2026-08-18T08:25:46Z`. End `2026-08-18T08:32:31Z`. Exit 0.
`/usr/bin/time -l`: 405.62 real, 310.31 user, 114.62 sys, max RSS
4,138,369,024 bytes (~3.85 GiB).

Stdout (verbatim):

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
forward done shape=[9,49152]
position=0 (prompt end, last prefill row 8)
observed_top1_non_eog=40983
golden_top1_non_eog=30
top1_matches=false
observed_top5=[40983, 44128, 25623, 17000, 6423]
golden_top5=[30, 28, 1270, 365, 198]
top5_overlap=0/5
all_finite=true
band: not_compared (no golden file)
first_divergence=position 0: top-1 40983 vs golden 30
PREFILL: FAIL
```

The GATE 9 wall (per-element `t.data.clone()` in `_transpose`) did not
reproduce. Forward returned. The first failing oracle is gi0 top-1 at
position 0. Stop rule: record exactly, do not chase. No Metal/CUDA or
payload-residency claim.

Toolchain: rustc 1.97.1 (8bab26f4f 2026-07-14) Homebrew, cargo 1.97.1
(c980f4866 2026-06-30). Host: Darwin 25.5.0 arm64
(`burgus.local`, `RELEASE_ARM64_T6050`, Apple M5 Max).

## Revisions

| Surface | Revision |
| --- | --- |
| packet gradus | this commit (GATE 10 receipt; parent `3d915aa`) |
| packet radix (writable) | `693d74e3e` (ff from GATE 9 `5088c4397`; includes `1bc63c590`/`234d44edf`) |
| faber binary used | packet `target/debug/faber` 1.7.0 at `693d74e3e` |
| workspace faber | `afd2a96` (via `FABER_SUPPORT_PATH_OVERRIDE`; not written) |
| workspace hosts | `a6c8129` (64 MiB `solum` cap; via override; not written) |
| packet/workspace norma | `7d71daf` (read via `FABER_LIBRARY_HOME`; not written) |

## Model identity

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
| observed top-1 / top-5 | `40983` / `[40983, 44128, 25623, 17000, 6423]` |
| golden top-1 / top-5 | `30` / `[30, 28, 1270, 365, 198]` |
| all_finite | true |
| first_divergence | position 0: top-1 40983 vs golden 30 |
| PREFILL | FAIL |

Hardware/OS: CPU/reference on `Darwin burgus.local 25.5.0 arm64`
(`RELEASE_ARM64_T6050`). Prefix read, admit, tokenizer, all 32 layer
materializations, and `dense.forward` completed.

## Evidence boundary

This is a compiled-route **prefill-logit receipt with first-divergence**.
GATE 10's campaign first is that `_transpose` of `[960, 49152]` is
linear and the binary reaches the gi0 oracle. The oracle fails at
position 0 (top-1). The gi0 band file was not supplied
(`band: not_compared`).

## Prior stops

### 2026-08-18 GATE 9 — embed `_transpose` clone (radix `5088c4397` / hosts `a6c8129`)

Packet `faber` green. Rust emit 0 errors / 607 warnings. Printed binary
passed the 1.78 MiB prefix, admit, tokenizer, and all 32 layer loads,
then sat in generated `_transpose` cloning `t.data` (~180 MiB) per
element. SIGTERM after 43m49s (exit 143). No logits. Closed on radix
`234d44edf` / `1bc63c590`. Did not reproduce on GATE 10.

### 2026-08-18 GATE 8 — sermo materialization (radix `5088c4397` / hosts `bf11418`)

Packet `faber` green. Rust emit 0 errors / 607 warnings. Printed binary
panicked on the first `solum.read_range` of the 1_787_040-byte prefix:
`failable call failed: "sermo materialization failed"`. Closed on hosts
`a6c8129` (range cap 1 MiB → 64 MiB). Did not reproduce on GATE 9 or 10.

### 2026-08-17 FINAL — rustc 258 (radix `2ed9914e4` / faber `b1adfc9`)

Packet `faber` green. Prior gates cleared: CODEGEN001 (`d66e1f93e`),
E0432 (`7f0c7de51`), PKG001 `processus:exi` (`9f828b2b6` + `6e13687`).
`faber build --target rust` emitted the crate; rustc failed 258 errors
(first: `cast cannot be followed by a method call` at `src/main.rs:766`).
No rust binary. Did not reproduce on GATE 8, 9, or 10.
