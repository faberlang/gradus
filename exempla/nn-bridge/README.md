# nn-bridge — typed-tensor nn bridges

This package is the executed proof of the six admitted typed-tensor
bridges on `gradus:nn`. The co-located `src/nn.proba` suite pins the
staged carrier family (`linear_carrier` / `gelu` / `layernorm`) only:
the proba file-interface degrades typed-tensor signatures. This package
constructs the accepted-proof typed tensors and calls each bridged row
against those same pins.

## What

Rows: `linear_2x2`, `linear_4x4`, `linear_2x8`, `gelu_4x4`, `gelu_2x8`,
`layernorm_2x8`. Linear pins are exact; gelu and layernorm use the
documented `5e-4` absolute tolerance (f64 reference vs f32 self-host).

Catch arms return the input. A FAIL here means the glue returned identity
or diverged numerically from the staged family.

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
package green.

No device handle, no model file, no performance claim.
