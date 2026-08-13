# External GPU Dependency Note

**Status**: plan / ownership boundary · **Date**: 2026-08-01

## Owner

The GPU gradient path is a Radix `mir-swarm` rung, not a Gradus capability.
Radix owns the open rungs: WGSL shader emission and PTX/CUDA kernels via the
LLVM→NVVM path. Hosts (`burgus` local, `pharos` server) manage device
execution. Gradus consumes the compiler's autograd capability; it does not
fork or extend the compiler.

## Gradus boundary

Gradus is device-neutral. Public types are pure mathematical contracts —
tensors as shape+dtype values, gradients as functions, optimizers as
parameter-update rules. Gradus must not carry GPU device handles, buffer
objects, backend-specific execution state, kernel launch or dispatch logic, or
device memory management.

The device-neutral boundary means Gradus source compiles identically for CPU
and GPU. Gradus describes *what* to compute; Radix chooses the lowering target
(CPU now, GPU future).

## Acceptance split

**CPU acceptance (Horizons 1–7)**: correctness only — finite-difference
gradient match, convergence proof (loss decreasing to a real target on a real
dataset). Speed is not a criterion; nanoGPT runs on CPU slowly by design (the
forcing function).

**GPU acceptance (Horizon 8)**: correctness AND performance — loss-trace
equivalence with CPU training, and a 10–100× speedup for nanoGPT-scale
workloads. Measured by Radix/hosts, not by Gradus.

## Blocking relationship

The GPU gradient path blocks Horizon 8 (nanoGPT GPU training) only. It does
NOT block Horizons 1–7 (CPU training, library surface, architecture proofs).
