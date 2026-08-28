# nn-bridge — typed-tensor nn bridges

This package is the executed proof of the six admitted typed-tensor
bridges on `gradus:nn`. The co-located `src/nn.proba` suite pins the
staged carrier family (`linear_carrier` / `gelu_carrier` / `layernorm_carrier`) only:
the proba file-interface degrades typed-tensor signatures. This package
constructs the accepted-proof typed tensors and calls each bridged row
against those same pins.

## What

Rows (historical pin labels, kept as provenance): `linear_2x2`,
`linear_4x4`, `linear_2x8`, `gelu_4x4`, `gelu_2x8`, `layernorm_2x8`.
Since the wave-1 callers move, the same-shape rows call the
shape-generic leaves — `nn.linear<M,K,N>` (linear_2x2, linear_4x4) and
`nn.gelu<M,N>` (gelu_4x4, gelu_2x8) — with the pin values unchanged.
The `linear_2x8` and `layernorm_2x8` rows still call their fixed-shape
functions (wave 2). Linear pins are exact; gelu and layernorm use the
documented `5e-4` absolute tolerance (f64 reference vs f32 self-host).

The generic leaves are infallible, so their bridge wrappers no longer
carry catch arms. The remaining staged-backed rows (`linear_2x8`,
`layernorm_2x8`) keep theirs; catch arms return the input. A FAIL here
means the glue returned identity or diverged numerically from the staged
family.

## Why

Typed-tensor signatures are the admitted caller-backed public rows. The
proba suite cannot pin them, so this package is the executed proof next
to the staged family.

## Run

```
faber check exempla/nn-bridge
faber run --target fmir exempla/nn-bridge
```

Known status, honestly: the `linear_2x8` staged comparison is green. The
typed `linear_2x2` matmul path is a pre-existing red — do not claim this
package green. The wave-1 callers move does not claim to fix that red;
it is recorded here as the baseline it was before this change.

No device handle, no model file, no performance claim.
