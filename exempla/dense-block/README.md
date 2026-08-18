# dense-block — generic dense transformer block executed proof (REF-01-U1.5)

This package is the executed proof for the REF-01-U1.5 generic dense
transformer block in `gradus:transformer`. It runs through package MIR
(`faber run --target fmir exempla/dense-block`) and prints PASS for every
pinned value (0 FAIL, exit 0).

## What is proved

`dense_block` is the ordered dense transformer block over the staged f32
carrier, composing the already-proven U1.1 (RMSNorm), U1.2 (SiLU/SwiGLU),
and U1.4 (multi-head GQA attention) rows:

1. **input RMSNorm** — `ln1 = rmsnorm(x, ln1_s, ε)` (the llama-arch
   last-axis norm, no centering — U1.1);
2. **GQA attention (causal + RoPE)** — q/k/v projections via `nn.linear`,
   then `multi_head_attention` with `num_kv_heads ≤ num_heads`, scaled
   causal scores, per-head KV groups, head concatenation, the `[H·D, H·D]`
   output projection (`out = concat · wo`, `[K, N]` row-major adapter
   contract — do not transpose), and the U1.3 configurable RoPE applied
   to q/k at their positions (U1.4);
3. **residual** — `r1 = x + ctx`;
4. **post-attn RMSNorm** — `ln2 = rmsnorm(r1, ln2_s, ε)` (U1.1);
5. **SwiGLU MLP** — `h = swiglu(linear(ln2, wg, bg), linear(ln2, wu, bu),
   wd, bd)` — `silu(gate) ⊙ up → linear(down)` (U1.2);
6. **residual** — `r2 = r1 + h` — the block output `[T, D]`.

No fixed-shape constants: every shape derives from the runtime tensors and
the head counts (num_heads, num_kv_heads, head_dim from the q width, the
MLP hidden width from the gate/up projections). The F32 row is the admitted
row (the composed rows' contract).

## Pinned config

One synthetic dim config is pinned to independent f64 reference values
(external Python/numpy evaluation of the documented block formulas — the
PML3 `transformer_block` pin precedent — with the corrected U1.4
O-projection `concat · wo`, residual-2 `r1 + h`). No GI2-2 golden exists for this synthetic
draw. Compared within the documented 5e-4 absolute tolerance:

- `T=2, D=16, F=16` (MLP hidden), `num_heads=4, num_kv_heads=2`,
  `head_dim=4` (the qwen2 head ratio 4:2 at a compact head_dim);
- `positions [0, 1]`, `rope_dim 4`, consecutive-pair (llama NORM)
  `freq_base 100000`, `scale 1.0`;
- RMSNorm `ε = 1e-5` (llama-arch default);
- dk scale `1/sqrt(head_dim) = 0.5`.

The pinned inputs are a fixed deterministic draw (the U1.4 dense-gqa
precedent): `x[t][j] = ((t+1)(j+3) mod 13 + 1)/10`, projections with the
same pattern scaled down, per-channel biases. Every one of the 32 output
elements is pinned. The same config and reference values live at compile
level in `src/transformer.proba` (representative subset plus the typed
error contract).

## Run

```
faber run --target fmir exempla/dense-block
```

No device handle, no performance claim; forward-only (no autograd import).
