# generate-smollm2 — G2 public generate on SmolLM2-360M

Compiled-rust consumer of `gradus:generation.generate_dense`.

Same admitted weights and pinned prompt as G1 (`dense-decode-smollm2`).
G1's unrestrained greedy continuation after the prompt was `[30, 2, 198]`;
that slice deliberately skipped EOG-stop. This route applies it.

**Oracle (honest):**
- First greedy token = GATE 13 / GI2 continuation `30`.
- Token `2` is SmolLM2 EOS and is in the admitted EOG set `{0, 2}`.
- With EOG-stop, generation emits the EOS token and halts: `[30, 2]`.
- `max_tokens=3` is a ceiling, not a promise. If EOS did not fire the
  N-token path would be `[30, 2, 198]` (G1's unrestrained record).

Prompt: `The quick brown fox jumps over the lazy dog`
Tokens: `[504, 2365, 6354, 16438, 27003, 690, 260, 23790, 2767]`

## Receipt (compiled rust, 2026-08-18)

Handle `807c7df1` / packet `hand-66`. Binary
`exempla/generate-smollm2/target/debug/generate-smollm2`.
32 layers loaded; `generate_dense` with greedy `max_tokens=3`.

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
```

Token `2` is SmolLM2 EOS. EOG-stop emits it and halts. Exit 0.
