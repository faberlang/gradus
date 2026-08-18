# dense-prefill-smollm2 — REF-01-U1.9 SmolLM2 prefill-logit receipt

Consumer for the U1.8 dense forward graph against the pinned SmolLM2-360M
row on the **compiled rust** receipt tier. This README is the unit receipt.

**Verdict: LOCALIZED — wiring, layer 0 embedding gather (`dense.forward`
`_transpose`).** Handle `5830c444` / packet `hand-12`. GATE 10 (receipt
`dfa4fce`) reached gi0 and failed top-1 `40983` vs golden `30`. This unit
does not fix. It names the first GI2-2 divergence and stops.

The compiled stored view of `token_embd.weight` is already the ggml-order
Q8_0 buffer (dim0 = 960 innermost = token-major `[V, D]` linearized).
`dense.forward` treats the GGUF descriptor shape `[960, 49152]` as
row-major `[D, V]` and transposes before gather. Prompt-end token `2767`
then reads `data[d * 49152 + 2767]` instead of `data[2767 * 960 + d]`.
Layer 0 `rms_norm` / `dense` / later ops inherit that wrong `x`.

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
  fallback and was tried after rustc failed.

## Command (from the Hand packet)

```text
cd /Users/ianzepp/work/faberlang/worktrees/hand-12/radix
cargo build -p faber
```

`cargo build -p faber` at readable radix `2ed9914e4` exits 0
(Finished `dev` profile in 19.51s). Packet binary:
`/Users/ianzepp/work/faberlang/worktrees/hand-12/radix/target/debug/faber`
(`faber 1.7.0`, rustc 1.97.1 Homebrew). Prior E0432
(`faber_hir_rust::ImportedEnumVariantInfo`) did not reproduce.

Packet root is not a library home (`norma` is not a packet member). The
rust emit used the established symlink home:

```text
/tmp/faber-hand-12-libhome/gradus -> packet/gradus
/tmp/faber-hand-12-libhome/norma  -> /Users/ianzepp/work/faberlang/norma
```

```text
cd /Users/ianzepp/work/faberlang/worktrees/hand-12/gradus
env FABER_SUPPORT_PATH_OVERRIDE=/Users/ianzepp/work/faberlang \
  FABER_LIBRARY_HOME=/tmp/faber-hand-12-libhome \
  /Users/ianzepp/work/faberlang/worktrees/hand-12/radix/target/debug/faber \
  build --target rust exempla/dense-prefill-smollm2
```

## Observed rust emit (2026-08-17 FINAL)

First attempt against `FABER_LIBRARY_HOME=<packet>` (no `norma`) failed
before the rust plan with the known compact:

```text
error[PKG001:unknown_library_provider]: exempla/dense-prefill-smollm2/src/main.fab:813
error[PKG001:unknown_library_provider]: exempla/dense-prefill-smollm2/src/main.fab:853
compilation failed
```

Those byte offsets are the `norma:processus` / `norma:solum` imports.
Retry used the symlink home above. Prior runtime-plan stops did **not**
reproduce:

- `PKG001:package_host_selection_required` — already wired (`[target.rust] host = "native"`)
- `PKG001:host_provider_selection_invalid` / `processus:exi` — accepted at `9f828b2b6` + `6e13687`
- `CODEGEN001` — rust emit completed; crate written to
  `exempla/dense-prefill-smollm2/target/faber`
- E0432 — not reproduced

Cargo compiled `host-kernel`, `processus`, `host-native`, `solum`, then
`dense-prefill-smollm2`. rustc 1.97.1 then failed the generated crate:

```text
error: could not compile `dense-prefill-smollm2` (bin "dense-prefill-smollm2") due to 258 previous errors; 337 warnings emitted
error: cargo build exited with status exit status: 101
```

First exact diagnostic:

```text
error: cast cannot be followed by a method call
   --> src/main.rs:766:74
    |
766 |             message: format!("{}{}", "golden line count is not 49152: ", lines.len() as i64.to_string()),
```

First coded diagnostic:

```text
error[E0015]: cannot call non-const associated function `Box::<[i64; 9]>::new_uninit` in constants
  --> src/main.rs:25:37
   |
25 | pub const PINNED_TOKENS: Vec<i64> = vec![504, 2365, 6354, 16438, 27003, 690, 260, 23790, 2767];
```

Error-code family counts on the rustc stream (260 `error` lines observed;
rustc reports 258): E0015 173, E0493 37, E0308 29, E0599 9, E0277 3,
bare "cast cannot be followed by a method call" 5, E0605 1
(`Vec<i64> as Vec<u8>`), E0061 1, E0609 1 (`no field dtype` on
`Option<GgufMetadata>`), E0382 1. Representative later identities:
`transpone` / `activatio_softmax` missing on `faber::Tensor<T>`;
`accipe` missing on `String`.

Documented llvm-host fallback, same env:

```text
error[PKG001:llvm_emission_failed]: exempla/dense-prefill-smollm2/src/main.fab
llvm-host build failed
```

No rust binary was printed. The GGUF file was not executed. No logits, no
observed token ids, no first-divergence field, no Metal/CUDA or
payload-residency claim.

## Revisions

| Surface | Revision |
| --- | --- |
| packet gradus | `1baaaa6` base; this commit records the FINAL stop |
| packet radix (readable) | `2ed9914e4` (includes `9f828b2b6`, `7f0c7de51`, `d66e1f93e`) |
| faber binary used | packet `target/debug/faber` 1.7.0 at `2ed9914e4` |
| workspace faber | `b1adfc9` (`6e13687` processus:exi via `process::exit`; not written) |
| workspace hosts | `24687cd` (solum/processus manifests; not written) |
| workspace norma | `7d71daf` (read via libhome; not written) |

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

Hardware/OS for an executed run would have been CPU/reference on
`Darwin burgus.local 25.5.0 arm64` (`RELEASE_ARM64_T6050`). No run
occurred.

## Evidence boundary

This is a compiled-route **stop receipt**, not a prefill-logit pass.
Repair belongs to radix rust codegen (HIR-rust emit of Faber `const`
lists / `as`+method chains / captured closures). That surface is
outside this packet. TARGETLANE001 was not weakened. The generated
crate under `exempla/dense-prefill-smollm2/target/faber` is build
output and is not committed.
