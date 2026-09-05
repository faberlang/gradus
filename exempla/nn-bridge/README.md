# nn-bridge — typed-tensor nn bridges

This package is the executed proof of the six admitted typed-tensor
bridges on `gradus:nn`. The co-located `src/nn.proba` suite pins the
staged carrier family (`linear_carrier` / `gelu_carrier` / `layernorm_carrier`) only:
the proba file-interface degrades typed-tensor signatures. This package
constructs the accepted-proof typed tensors and calls each bridged row
against those same pins.

## What

Rows: `nn.linear` at `[2,2]` and `[4,4]`, `nn.linear_channel` at `[2,8]`,
`nn.gelu` at `[4,4]` and `[2,8]`, and `nn.layernorm` at `[2,8]`.
The fixture dimensions stay pinned while every call uses the
shape-generic public leaf. Linear pins are exact; gelu and layernorm use the
documented `5e-4` absolute tolerance (f64 reference vs f32 self-host).

The generic leaves are infallible, so their bridge wrappers do not carry
catch arms. A FAIL here means the glue returned identity or diverged
numerically from the staged family.

## Why

Typed-tensor signatures are the admitted caller-backed public rows. The
proba suite cannot pin them, so this package is the executed proof next
to the staged family.

## Run

```
faber check exempla/nn-bridge
faber run --target fmir exempla/nn-bridge
```

Known status, honestly: the staged comparison for the per-channel
`nn.linear_channel` fixture is green. The typed `[2,2]` matmul path is a
pre-existing red — do not claim this package green. This migration does not
claim to fix that red; it is recorded here as the baseline it was before this
change.

No device handle, no model file, no performance claim.
