# generate-smollm2 — G2 public generate on SmolLM2-360M

Compiled-rust consumer of `gradus:generation.generate_dense` (EOG-stop
default) and `generate_dense_with_stop` (`IgnoreEos`).

Same admitted weights and pinned prompt as G1 (`dense-decode-smollm2`).
G1's unrestrained greedy continuation after the prompt was `[30, 2, 198]`;
that slice deliberately skipped EOG-stop. The default route applies it.
`IgnoreEos` is the llama.cpp `ignore_eos` row used to capture the U5
16-token golden: admitted EOG ids are suppressed from sampling and the
loop runs to `max_tokens`.

**Oracle (honest):**
- First greedy token = GATE 13 / GI2 continuation `30`.
- Token `2` is SmolLM2 EOS and is in the admitted EOG set `{0, 2}`.
- With EOG-stop, generation emits the EOS token and halts: `[30, 2]`.
- `max_tokens=3` is a ceiling, not a promise. If EOS did not fire the
  N-token path would be `[30, 2, 198]` (G1's unrestrained record).
- With `IgnoreEos` and `max_tokens=16`, the U5 golden is
  `[30, 198, 198, 504, 808, 6330, 314, 253, 2232, 4814, 282, 1027, 28, 979, 260, 1796]`.

Prompt: `The quick brown fox jumps over the lazy dog`
Tokens: `[504, 2365, 6354, 16438, 27003, 690, 260, 23790, 2767]`

## Receipt (compiled rust, 2026-08-18)

Handle `321a19ee` / packet `hand-17`. Binary
`exempla/generate-smollm2/target/faber/target/release/generate-smollm2`.
32 layers loaded; default `generate_dense` greedy `max_tokens=3`, then
`generate_dense_with_stop(IgnoreEos)` greedy `max_tokens=16`.

```text
first_sampled=30
golden_top1=30
first_matches=true
generated=[30, 2]
n=2
eog_token=2
eog_stop=true
g1_unrestrained=[30, 2, 198]
first_divergence=none
GENERATE: PASS
continued=[30, 198, 198, 504, 808, 6330, 314, 253, 2232, 4814, 282, 1027, 28, 979, 260, 1796]
continued_n=16
golden_continue=[30, 198, 198, 504, 808, 6330, 314, 253, 2232, 4814, 282, 1027, 28, 979, 260, 1796]
continue_first_divergence=none
CONTINUE: PASS
GENERATE+CONTINUE: PASS
```

Default EOG-stop still emits SmolLM2 EOS=2 then halts. IgnoreEos matches
the U5 16-token golden exactly. Exit 0.
