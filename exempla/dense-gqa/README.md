# dense-gqa — multi-head attention with GQA executed proof (REF-01-U1.4)

This package is the executed proof for the REF-01-U1.4 multi-head attention
row in `gradus:attention`. It runs through package MIR
(`faber run --target fmir exempla/dense-gqa`) and prints PASS for every
pinned value (0 FAIL, exit 0).

## What is proved

`multi_head_attention` implements multi-head attention with GQA KV-head
sharing over the staged f32 carrier:

- **per-head q/k/v splits** — packed `q [T, H·D]`, `k/v [T, K·D]` with
  `0 < K ≤ H`, `H % K == 0`; query head `h` attends through its KV group
  `g = h // (H/K)`;
- **scaled scores** — `scores = q'·k'ᵀ · scale` (the caller's dk factor);
- **causal mask** — the GI3 CausalMaskedSoftmax recipe (row `i` attends to
  columns `j ≤ i`, diagonal included; no mask-tensor input);
- **v accumulation** — `ctx_h = softmax(scores_h) · v_g`;
- **head concatenation** — the per-head contexts joined along the last axis;
- **output projection** — `out = concat · woᵀ` with the `[H·D, H·D]`
  output weight in the `[in, out]` linear layout (the nn.fab `linear`
  posture);
- **RoPE** — q and k are rotated at their positions first via the U1.3
  configurable RoPE row (`RopeConfigura`: frequency base, scale, pair
  policy). The row is the inference composition: causal + RoPE. The shape
  set is fully runtime-derived — no fixed-shape constants.

## Pinned config rows

Two config rows are pinned to independent f64 reference values (external
Python evaluation of the formulas above, cross-checked against numpy),
compared within the documented 5e-4 absolute tolerance (the COS_1/SIN_1
precedent):

- **GQA config** — `n_h=14, n_kv=2, head_dim=4`, `T=2` (the qwen2 head
  ratio 14:2 at a compact head_dim), positions `[1, 2]`, `rope_dim 4`,
  interleaved-pair (qwen2) theta 1000000 — the qwen2 GGUF `rope_theta`
  fact. The KV-sharing path is exercised at ratio 7.
- **MHA config** — `n_kv = n_h = 14`, positions `[0, 0]` (RoPE identity —
  the exact-identity anchor), consecutive-pair (llama) base 100000.

The pinned inputs are a fixed deterministic draw
(`q[t][j] = ((t+1)(j+3) mod 13 + 1)/10`, k/v with different offsets,
`wo[r][c] = (3(r+1) + 5(c+1)) mod 19 / 18` — asymmetric, so a transposed
projection would change the pins). Every one of the 224 output elements of
the two config rows is pinned (112 each). The same configs and reference
values live at compile level in `src/attention.proba` (representative
subset of the executed pins), with the full typed-error contract.

## Run

```
faber run --target fmir exempla/dense-gqa
```

No device handle, no performance claim; forward-only (no autograd import).
