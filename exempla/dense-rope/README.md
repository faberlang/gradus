# dense-rope — configurable RoPE executed proof (REF-01-U1.3)

This package is the executed proof for the REF-01-U1.3 configurable RoPE
row in `gradus:attention`. It runs through package MIR
(`faber run --target fmir exempla/dense-rope`) and prints PASS for every
pinned value (0 FAIL, exit 0).

## What is proved

`rotary_position_embedding_configura` generalizes the fixed
`rotary_position_embedding` (llama-arch NORM consecutive-pair, freq_base
100000) to three knobs:

- **frequency base (theta)** — `RopeConfigura.base`;
- **scale** — `RopeConfigura.scale` (multiplies theta, 1.0 = no scaling);
- **pair policy** — `RopePolitica`:
  - `Consecutive` (llama-arch NORM): pairs `(x[2k], x[2k+1])`;
  - `Interleaved` (qwen2): pairs `(x[k], x[k+n/2])` — the llama.cpp NEOX
    half-split layout (pairs offset by `n_dims/2`).

Both pair-policy rows are pinned: the consecutive-pair row at freq_base
100000 and the interleaved-pair row at theta 1000000 (the qwen2 GGUF
`rope_theta` fact), each at positions 1 and 2 over dim 4, plus the scale
knob (scale 2.0) and the beyond-dim untouched property. The pinned values
are the independent f64 evaluation of

```
theta_k = pos · scale · base^(-2k/dim)
```

with

```
consecutive-pair: out[2k] = x0·cos − x1·sin, out[2k+1] = x0·sin + x1·cos
interleaved-pair: out[k] = x0·cos − x1·sin, out[k+n/2] = x0·sin + x1·cos
```

compared within the documented 5e-4 absolute tolerance (the COS_1/SIN_1
precedent). The same pins live at compile level in `src/attention.proba`
(the co-located proba suite; proba execution remains provider-blocked, so
this exempla run is the executed proof).

## Run

```
faber run --target fmir exempla/dense-rope
```

No device handle, no performance claim; forward-only (no autograd import).
