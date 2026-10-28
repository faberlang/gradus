# dense-decode-bench-metal — tiny cached greedy decode, timed on Metal

The synthetic model of `exempla/dense-model` (2 layers, hidden 16, 4 query and
2 key/value heads of width 4, MLP 16, vocab 8, tied head, weights in source, no
external files), prefilled over the 8-token prompt `[0, 3, 7, 1, 5, 2, 6, 4]`
that `exempla/dense-prefill-bench-metal` uses, then decoded greedily for 16
tokens, one position at a time, reusing the KV cache. Vivi need `6f29222c`.

```bash
cd gradus
faber run --device metal --stats-file STATS.json \
    --library-home "$(cd .. && pwd)" exempla/dense-decode-bench-metal
```

Use an absolute `--library-home` (a relative `..` fails, need `a467d2c9`).

## Output

```text
decode_tokens_per_s <median generated tokens/s over the timed regions>
decode_ms_median <median ms for one 16-token decode loop>
decode_tokens 16
decode_repeats 7
decode_max_pin_abs_error <worst absolute error over every pinned logit, all repeats>
decode_first_token 5
decode_ok true
```

Measured on the studio (Apple M5 Max), peer/main `faber 1.16.0`: about 35
tokens/s (about 460 ms per 16-token loop, 29 ms per token), the whole run under
5 seconds. Like the prefill bench it is launch-bound, not compute-bound: 15
launches per token, each a few microseconds of GPU time.

## What is timed

One timed region is the whole decode loop: 16 steps, each feeding the previous
token at position `8 + i` (embedding gather, both blocks over one row with a
cache write, the final RMSNorm, the tied head, the read-back of the 8 logits and
the argmax that picks the next token), so every launch has finished when the
clock stops. Prefill, cache construction and the first token (the argmax of the
prefill's last row, 5) are outside the clock. The region runs 7 times from the
same prefilled caches and the median is reported.

## What runs on Metal

`stats-file` `device.runtime.launch_count` is 1695 for one run: 15 launches per
decode step (per layer the Q, K, V projections, the residual add, the gate and up
projections, and the down projection fused with the second residual; plus the
tied head) over 113 steps (the step-0 parity step plus 7 repetitions of 16). The
prefill is the library's host `dense.prefill_cached`, so it adds none. The host
does the rest, with the same split as `dense-prefill-bench-metal` at one row
instead of eight (the matmul kernels take `[1, 16]` operands).

Not on the device, with the reason (Vivi need `be3ad664` tracks the gaps):

| Construct | Why it stays on the host |
| --- | --- |
| RMSNorm (`norm_rms`) | no launch geometry on Metal: `E_DEVICE_UNSUPPORTED geometry_plan_not_covered RmsNormalization`; a composed form needs `.sqrt()`, and `TensorMath(Sqrt)` is not an elementwise Metal op |
| SiLU in the SwiGLU gate | not an elementwise Metal op (the set is add, sub, mul, div, neg, fill, expand, relu, gelu) |
| embedding gather, per-head RoPE, causal attention, KV-cache write, output projection `wo` | host carrier code in the library today |
| `dense.load`, `transformer.dense_qkv` | `dense.load` does not link (`runtime generic shape has no stable formal carrier witness`) and `dense_qkv` returns a constructed tuple, which Metal refuses (`Construct`) |

So `main.fab` carries the block at the concrete shape, with the device regions as
matmul kernels and the library's host carriers (`nn.rmsnorm_carrier`,
`nn.silu_carrier`, `math.mul_carrier`, `gqa.multi_head_attention_cached`) for the
rest. The library's own `dense.decode_step` is entirely host code, so it never
dispatches; it is the step-0 parity reference, not the timed route.

## What it checks

A failure prints `FAIL <reason>` and exits 1. On every repetition:

- the 16 generated tokens equal `PIN_TOKENS` (`reference.py --decode`);
- every step's 8 last-position logits against the f64 pins in `PIN_LOGITS`,
  within 5e-6 absolute, all finite (measured worst 1.6e-7 on Metal). The pin of
  step `i` is the last row of a full f64 re-evaluation of the prompt plus the
  tokens generated so far, so it shares nothing with a KV cache.
  `reference.py` reproduces the `dense-model` `tied_1_*` pins to 5e-11
  (`python3 -I reference.py --check`; the decode pins come from
  `python3 -I reference.py --decode`);
- after step `i` both layers' caches hold exactly `8 + i + 1` rows, and the
  prefilled caches still hold 8 (the repetitions start from a `copy`).

Once, outside the clock: step 0 (the first device decode over the prefilled
caches) against the library's host `dense.decode_step` on the same caches, all 8
logits within 5e-6, and the prefill's top-1 equal to 5.

The synthetic logits sit within 0.03 of each other and greedy decode settles on
token 5 for every step (smallest top-1 margin 0.0318), so the token sequence is a
weak oracle on its own; the logit pins, which move with the position and the
cache contents, are the discriminating one.

## Tamper tests

`tamper.sh` copies the package, applies one edit per oracle clause and requires
exit 1 with a `FAIL` line:

```bash
cd gradus
FABER=/path/to/faber ./exempla/dense-decode-bench-metal/tamper.sh
```

| Tamper | Result |
| --- | --- |
| first `PIN_TOKENS` entry 5 -> 4 | `FAIL step 0 token 5 expected 4` |
| first `PIN_LOGITS` entry +1e-4 | `FAIL step 0 logit 0 observed ... pinned ...` |
| cache growth pin off by one row | `FAIL step 0 cache length 9 expected 10` |
| RMSNorm epsilon 1e-5 -> 1e-3 | `FAIL step 0 logit 0 observed ... pinned ...` |

The script exits 0 only when all four exit 1.
