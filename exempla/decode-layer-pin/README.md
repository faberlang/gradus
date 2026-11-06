# Decode layer device pin

This exemplum calls only the public `gradus:decode_token.layer_step` signature.
It keeps two fixtures: the small D=4/QD=4/KVD=2/F=6 case and a real-shape
D=960, QD=960, KVD=320, F=2560 case (15 query heads, 5 KV heads, dh=64,
GQA group 3). Both use deterministic nonzero projection weights and multiple
cache rows; the real run writes every hidden element and every K/V cache value
into the receipt after comparison with an independent Python f64 oracle.

Run from the Gradus checkout with current Faber:

```sh
FABER_BIN=/path/to/faber python3 exempla/decode-layer-pin/pin.py
```

Reference and Metal are mandatory for both modes. A device launch failure is
fatal, with no skip path. Both complete output arrays are compared against the
f64 oracle, including all cache rows, under the fixed component-wise cap
`1.1e-5 + 1.1e-4 * abs(reference)`. `decode_step.fab` documents the serial-f32
kernel numeric envelope as `1e-5 + 1e-4 * abs(reference)`; the pin adds 10% to
both coefficients. This cap was fixed in the file before the real-dimension
run and is not adjusted from observed errors.

The committed `receipt-real.json` records dimensions, tolerance basis, full
per-device values and maximum absolute errors. The red check recomputes the
oracle with deliberately wrong rotate-half RoPE, whereas `layer_step` uses
consecutive pairs, and requires the resulting mismatch to fail the same fixed
cap. If it ever passes, the runner exits nonzero.
