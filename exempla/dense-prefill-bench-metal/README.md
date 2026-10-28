# dense-prefill-bench-metal — tiny dense prefill, timed on Metal

The synthetic model of `exempla/dense-model` (2 layers, hidden 16, 4 query and
2 key/value heads of width 4, MLP 16, vocab 8, tied head, weights in source,
no external files) prefilled over a fixed 8-token prompt `[0, 3, 7, 1, 5, 2, 6, 4]`
into fresh per-layer KV caches, timed, and checked against a pinned
last-position logit row. Vivi need `cac1ee45`.

```bash
cd gradus
faber run --device metal --stats-file STATS.json \
    --library-home "$(cd .. && pwd)" exempla/dense-prefill-bench-metal
```

Use an absolute `--library-home` (a relative `..` fails, need `a467d2c9`).

## Output

```text
prefill_tokens_per_s <median prompt tokens/s over the timed regions>
prefill_ms_median <median ms for one 8-token prefill>
prefill_prompt_tokens 8
prefill_repeats 7
prefill_max_pin_abs_error <worst absolute error over the pinned row, all repeats>
prefill_top1 5
prefill_ok true
```

Measured on the studio (Apple M5 Max), peer/main `faber 1.16.0`: 139 to 145
tokens/s (55 to 57 ms per prefill), the whole run about 2 seconds. On
`--device reference` the same program gives about 270 tokens/s: at this size
the device run is launch-bound, not compute-bound.

## What is timed

One timed region is the whole prefill: embedding gather, both blocks, the final
RMSNorm, the output projection, and the read-back of the [8, 8] logits, so every
launch has finished when the clock stops. Model pinning and cache construction
are outside the clock. The region runs 7 times and the median is reported.

## What runs on Metal

`stats-file` `device.runtime.launch_count` is 120 for one run: 15 launches per
prefill (per layer the Q, K, V projections, the residual add, the gate and up
projections, and the down projection fused with the second residual; plus the
output projection) over 8 prefills (step 0 plus 7 repetitions). The host does
the rest.

Not on the device, with the reason:

| Construct | Why it stays on the host |
| --- | --- |
| RMSNorm (`norm_rms`) | no launch geometry on Metal: `E_DEVICE_UNSUPPORTED geometry_plan_not_covered RmsNormalization`; `kernel.prefill_rmsnorm` fails earlier (`TensorCopyInto has no kernel plan`); a composed form needs `.sqrt()`, and `TensorMath(Sqrt)` is not an elementwise Metal op |
| SiLU in the SwiGLU gate | not an elementwise Metal op (the set is add, sub, mul, div, neg, fill, expand, relu, gelu) |
| embedding gather, per-head RoPE, causal attention, KV-cache write, output projection `wo` | host carrier code in the library today |

`dense.prefill_cached`, the library's prefill entry, is entirely host code
(`math.matmul` over staged carriers is a scalar loop), so it never dispatches. The
typed `transformer.dense_block_cached_static` cannot be used either:
`transformer.dense_qkv` returns a constructed tuple, which Metal refuses
(`kernel dense_qkv has no device kernel: ... Construct`), `dense.load` does not
link (`runtime generic shape has no stable formal carrier witness`), and
`dense_mlp` composes kernels. So `main.fab` carries the same block at the concrete
shape, with the device regions as matmul kernels and the library's host carriers
(`nn.rmsnorm_carrier`, `nn.silu_carrier`, `math.mul_carrier`,
`gqa.multi_head_attention_cached`) for the rest. The projection bias is absent in
this model, so none is added.

## What it checks

A failure prints `FAIL <reason>` and exits 1.

- Every repetition's last-position logits against the f64 pins in `PINS`, within
  5e-6 absolute (measured worst 1.0e-7 on Metal, 8.8e-8 on the MIR runner).
  `reference.py` is the independent numpy evaluation; it reproduces the
  `dense-model` `tied_1_*` pins to 5e-11 (`python3 reference.py --check`).
- Every logit of every repetition finite, and the last row's argmax equal to the
  pinned top-1 token (5; the margin to the runner-up is 0.03).
- Every layer's KV cache holds exactly the 8 prompt rows after the prefill.
- Step 0: all 64 device logits against the library's host
  `dense.prefill_cached` on the same weights, within 5e-6.

The synthetic logits sit within 0.03 of each other, so the tolerance is
absolute and tight. Perturbing a pin by 1e-4, the RMSNorm epsilon to 1e-3, or
dropping a layer each fails the run.
