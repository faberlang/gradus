# dense-decode-smollm2 — GGUF-A5 first decode/KV wiring slice

Compiled-rust consumer for one incremental decode step over the per-layer
KV cache, then a short autoregressive loop on SmolLM2-360M.

**Oracle (honest):** the first sampled token after the pinned prompt must
equal the GATE 13 / GI2 prefill continuation `30`. That pin is the
already-green SmolLM2 prefill top-1 at prompt-end / position 0
(`exempla/dense-prefill-smollm2`, GOLDEN_TOP1). Incremental
`dense.decode_step` after the same prompt must reproduce that last-row
argmax. Generated tokens must be finite vocabulary ids. No full
`generate()` API, no perf claim.

Prompt: `The quick brown fox jumps over the lazy dog`
Tokens: `[504, 2365, 6354, 16438, 27003, 690, 260, 23790, 2767]`
First greedy continuation: `30`

## Receipt (compiled rust, 2026-08-18)

Handle `61f95e96` / packet `hand-62`. Binary
`exempla/dense-decode-smollm2/target/debug/dense-decode-smollm2`.
32 layers loaded; per-layer cache width 320 (5 KV heads × 64).
9 incremental prompt `decode_step`s then 3 greedy samples.

```text
first_sampled=30
golden_top1=30
first_matches=true
generated=[30, 2, 198]
n=3
cache_len=11
first_divergence=none
DECODE: PASS
```

Token `2` is the SmolLM2 EOS id; this slice does not apply EOG-stop
(no full `generate()` API). Exit 0.
