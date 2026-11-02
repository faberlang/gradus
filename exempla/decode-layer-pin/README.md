# Decode layer device pin

This executable calls `gradus:decode_token.layer_step` directly. It has two
statically shaped configurations:

- `tiny`: D=4, QD=4, KVD=2, F=6, dh=2, two query heads with GQA group 2,
  and a three-row cache.
- `real`: D=960, QD=960, KVD=320, F=2560, dh=64, 15 query heads,
  five KV heads, GQA group 3, and an eight-row cache. The layer writes row 7.

Both fixtures use deterministic nonzero weights and cache rows. The tiny run uses
its independent Python f64 calculation. The real-shape output-stream caps are
fixed from a calibration run and committed as constants; each validation
invocation compares the reference and Metal outputs against those frozen
caps. They are `2.2` absolute for hidden, `1.3199999999891077e-5` for key, and
`4.957856535911561e-6` for value. Each is 110% of its measured calibration
maximum, except identical-value parity uses the 110%-padded f32-epsilon scale
floor. The receipt records the calibration basis and validation deltas. The
real-shape f64 oracle is a separate follow-up proof.

Run from the Gradus checkout with the Faber built from the current Radix main:

```sh
FABER_BIN=/path/to/current/radix/target/debug/faber \
    python3 exempla/decode-layer-pin/pin.py --shape tiny
FABER_BIN=/path/to/current/radix/target/debug/faber \
    python3 exempla/decode-layer-pin/pin.py --shape real
```

Both `--device reference` and `--device metal` are mandatory for calibration
and validation. A failed Metal launch, including no admitted Metal device,
exits nonzero; there is no skip path. The runner creates a temporary local
library-home link because some checkouts are not named `gradus`, then removes
it on exit. It writes full tiny outputs to `receipt-tiny.json`; the real receipt
records each device's output hash, counts, samples, and comparison details in
`receipt-real.json`.

The tiny comparison cap is `1e-5 + 1e-4 * abs(f64_reference)`, selected from
the existing serial-f32 `decode_step` numeric contract before its device run.
At dh=2 the rotate-half and consecutive-pair RoPE conventions are
mathematically identical. The real shape uses dh=64 and consecutive-pair RoPE.
A real-shape independent f64 oracle and deliberate wrong-index red case remain
to be added.
