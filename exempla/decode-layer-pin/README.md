# Decode layer device pin

This executable calls `gradus:decode_token.layer_step` directly. The starter
fixture uses D=4, QD=4, KVD=2, F=6, dh=2, two query heads with GQA group 2,
and a three-row cache. Deterministic nonzero weights and cache rows exercise
RoPE, GQA attention, the in-place KV update, both residual paths, RMSNorm and
SwiGLU. `pin.py` independently recomputes the layer in Python double precision
and compares the hidden state and every K/V cache element.

Run from the Gradus checkout with the Faber built from the current Radix main:

```sh
FABER_BIN=/path/to/current/radix/target/debug/faber \
    python3 exempla/decode-layer-pin/pin.py
```

Both `--device reference` and `--device metal` are mandatory. A failed Metal
launch, including no admitted Metal device, exits nonzero; there is no skip
path. The runner creates a temporary local library-home link because some
checkouts are not named `gradus`, then removes it on exit. It writes the
successful device values and per-device oracle errors to `receipt-tiny.json`.

The fixed comparison cap is `1e-5 + 1e-4 * abs(f64_reference)`, selected from
the existing serial-f32 `decode_step` numeric contract before the two-device
run. This tiny fixture establishes the launch-chain pin and runner protocol;
it is not the required real-dimension tolerance measurement or oracle. At dh=2
the rotate-half and consecutive-pair RoPE conventions are mathematically
identical, so this fixture does not distinguish a wrong RoPE convention. The
real D=960 / QD=960 / KVD=320 / F=2560 / dh=64 / group-3 pin, real-dimension
independent oracle, and deliberate wrong-index red case remain to be added.
