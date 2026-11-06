# Red — strided kernel loop over generic extents

```text
faber check exempla/kernel-strided-extent-red
error[SEM008:nucleum_extent_unproven]: kernel integer extent unknown is not proven to fit the portable range
```

Blocks rewriting decode_step's six strided `while` loops (`rms_part`, `gemv_part`,
`qkv_part` x3, `head_wide`) as `for range p ‥ D step Q`. Compiler gap.
