# dense-swiglu — REF-01-U1.2 executed proof: SiLU + SwiGLU MLP

This package is the executable proof for the REF-01-U1.2 rows in
`gradus:nn` (the SiLU activation identity and the SwiGLU gated-MLP
composition), over the staged f32 carrier. Its source builds small staged
tensors in memory, calls the public `nn.silu` / `nn.swiglu` rows, and
prints PASS for every pinned f64 reference value within the documented
5e-4 absolute tolerance. It performs no filesystem read, download, or
model-payload allocation.

## The pinned workload

**SiLU identity** — `silu(x) = x / (1 + e^{-x})`:

| x | f64 reference |
| --- | --- |
| −3.0 | −0.142277620 |
| −1.0 | −0.268941421 |
| −0.5 | −0.188770334 |
| 0.0 | 0.000000000 |
| 0.5 | 0.311229666 |
| 1.0 | 0.731058579 |
| 2.0 | 1.761594156 |
| 3.0 | 2.857722380 |

**SwiGLU gated-MLP composition** — gate [2,4], up [2,4], down W [4,3],
same-shape down bias [2,3]; `h = silu(gate) ⊙ up; y = linear(h, W, b)`:

| Row | f64 reference |
| --- | --- |
| y[0,0] | −1.259825181 |
| y[0,1] | −1.527747218 |
| y[0,2] | −1.545669255 |
| y[1,0] | 2.803429168 |
| y[1,1] | 2.936614260 |
| y[1,2] | 3.319799352 |

The pins are independent f64 evaluations of the documented formulas
(external Python evaluation of `x/(1+e^{-x})` and the gated composition),
compared within the documented 5e-4 absolute tolerance (`approximata`
precedent) — the same pins `src/nn.proba` carries at compile level.

## Evidence boundary

The package runs through package MIR (FMIR) with the lane Radix binary.
The receipt below is the executed value-identity claim for the U1.2 rows.
Co-located `src/nn.proba` remains structural/compile-level evidence; focused
`faber test` attempts remain blocked by the imported-library provider seam
(recorded library-wide residual). The executed proof compares observed
f32 values to the pinned f64 references with a manual `|a − b| ≤ 5e-4`
tolerance compare (the `approximata` intrinsic is not yet executable in
the FMIR image).

The SwiGLU workload uses the **same-shape bias** contract (b [2,3]) because
the per-channel-bias path (`linear` bias [N] against [M,N] via
`math.add`) requires singleton broadcast, and the current `forma.broadcastum`
implementation rejects the singleton-with-non-singleton pair at runtime
(`shapes not broadcastable` — latent defect, outside this unit's write
scope; proba-pinned right-aligned broadcast rows in `src/shape.proba`
remain compile-level). The pinned values are identical for both bias
contracts (the [2,3] bias rows repeat the [3] channel values); this is a
recording, not a workaround that changes the row's semantics.

## Receipt

Command, from the Hand packet:

```text
cd /Users/ianzepp/work/faberlang/worktrees/hand-5/gradus
env FABER_LIBRARY_HOME=/Users/ianzepp/work/faberlang/worktrees/hand-5 \
  /Users/ianzepp/work/faberlang/worktrees/hand-5/radix/target/debug/faber \
  run --target fmir exempla/dense-swiglu
```

Observed result (2026-08-14): exit `0`; 14 PASS lines and 0 FAIL lines:

```text
silu(-3.0): PASS observed=-142277
silu(-1.0): PASS observed=-268941
silu(-0.5): PASS observed=-188770
silu(0.0): PASS observed=0
silu(0.5): PASS observed=311229
silu(1.0): PASS observed=731058
silu(2.0): PASS observed=1761594
silu(3.0): PASS observed=2857722
swiglu(0,0): PASS observed=-1259825
swiglu(0,1): PASS observed=-1527747
swiglu(0,2): PASS observed=-1545669
swiglu(1,0): PASS observed=2803429
swiglu(1,1): PASS observed=2936614
swiglu(1,2): PASS observed=3319799
```

No execution claim is made beyond these staged-carrier rows (no Metal/CUDA
execution, no full-model payload residency).

## Related

- Rows: `src/nn.fab` (`silu`, `swiglu`) + pins in `src/nn.proba`
- Diagnostics: `docs/diagnostics.md` (`NnError`)
- API: `docs/api-reference.md` (`gradus:nn`)
