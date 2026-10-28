# training-bench-metal — the 4×4 MLP training loop, timed on Metal

The `exempla/training-loop-mlp` workload (4×4 two-layer MLP, 100 steps, lr 0.1)
with each step's forward, backward and SGD update dispatched as device kernels,
timed over the loop, and checked against the loss-pin oracle. Vivi need
`8220e2c1`.

```bash
cd gradus
faber run --device metal --stats-file STATS.json \
    --library-home "$(cd .. && pwd)" exempla/training-bench-metal
```

Use an absolute `--library-home`: a relative `..` fails with
`cannot read manifest at 'gradus' resolved against '..'`.

## Output

```text
train_steps_per_s <median steps/s over the timed loops>
train_loop_ms_median <median ms for one 100-step loop>
train_repeats 7
train_final_loss_pin99 <loss at step 99>
train_max_pin_rel_error <worst relative error over the six pins>
train_checkpoint_round_trip true
train_ok true
```

A wrong loss trajectory, a step-0 mismatch against the library, or a failed
checkpoint round-trip prints `FAIL <reason>` and exits 1.

## Metal dispatch

`--stats-file` records `device.runtime.launch_count` (15425 for one run: 22
launches per step across the forward, the backward companion, and the eight
`math.mul` / `math.sub` update kernels, plus the step-0 parity calls). Without
a kernel, `--device metal` stops with `E_DEVICE_NONE_ADMITTED`.

## Tolerance

The pins are f64; Metal is f32. Measured worst pin error is 4.9e-8 on the MIR
runner and 3.7e-7 on Metal. The in-program tolerance is 1e-5 relative.

## Why a carried loss function

`mlp.forward_mlp_loss` is generic. A generic `@ kernel` that also carries
`@ radix backward` fails at the companion call with `generic AIR definition has
no analyzed template`, and a kernel cannot call a non-kernel function
(`lane kernel statement other than assign: Call`). So `main.fab` carries the
same seven-line composition at the concrete 4×4 shape, and checks its step-0
loss and gradients against the library on the host. A tensor-by-scalar lift
(`g * lr`) does not lower to Metal (`TensorLift(Mul)`), so the learning rate is
a tensor.

## Large mode (`-- large`) — red on Metal

The same composition at 512×512. It fails its step-0 parity gate on Metal
today:

```text
FAIL large step-0 loss device 0.3036192 library 0.30778652
```

The f64 value is 0.30778653; the MIR runner and the unfused Metal kernels agree
with it. The fused AIR forward on Metal is wrong for matrix extents of 32 and
above. Minimal reproducer (integer data, so rounding is not a factor):

```fab
@ kernel
@ radix { lane = "air" }
@ radix backward "a_backward"
@ public
fn mean_lin(tensor<f32, [32, 32]> x, tensor<f32, [32, 32]> w, tensor<f32, [32, 32]> b) → f32 {
    let _ h ← x · w
    let _ hb ← h + b
    return hb.mean()
}
```

with `x[i,j] = (7i + 3j) % 11 - 5`, `w[i,j] = (5i + 2j + 1) % 13 - 6`, `b = 0`:
`--device reference` gives 0.024414063, `--device metal` gives -0.16015625. At
8×8 and 4×4 the two agree. Do not quote the large mode's steps per second until
this passes.
