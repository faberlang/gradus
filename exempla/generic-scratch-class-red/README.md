# Red — generic scratch class refused by the strict engine

`decode_token.layer_wide` passes 13 scratch tensors one by one. A scratch type
that groups them has to be generic over the model's extents, and the strict
engine declines the host half of a program that builds a generic class holding
tensors.

```text
faber run exempla/generic-scratch-class-red --library-home <parent> --device metal
error[ENGINE001:refused]: ... clif-jit declined the host half of this kernel program: unsupported type
```

This is a compiler gap, not a Gradus defect. When it closes, add the scratch type
and keep `layer_wide`'s positional form as a thin wrapper (Inferentia's
`PortScratch` uses literal extents and does not depend on it).
