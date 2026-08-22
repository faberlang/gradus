# GOAL: device-neutrality-contract — Gradus states its tier and parameterizes backend-family law

**Status**: done — 6/6 units landed (U1–U6 on gradus main). Closeout 2026-08-22: `faber test --include cache` 33/0; check-source; check-compile; factory audit 0 findings. U6 cites [`cache-proba-classification.md`](cache-proba-classification.md) (`324e344`).
**Created**: 2026-08-21
**Campaign:** `emission-lane-parity` (radix: [`docs/factory/emission-lane-parity/CAMPAIGN.md`](../../../../radix/docs/factory/emission-lane-parity/CAMPAIGN.md))
**Source:** operator architecture-audit session 2026-08-21 (campaign evidence F6.1–F6.3). Origin reminder: the foundation deliberately kept Gradus backend-neutral (`docs/archived/gradus-ml-foundation/gpu-dependency.md`: "The device-neutral boundary means Gradus source compiles identically for CPU and GPU; Radix chooses the lowering target").
**Repos:** `gradus` (primary: `src/cache.fab`, `docs/design/`, `exempla/dense-prefill-smollm2/bench/`)
**Related:** [`emission-lane-parity/CAMPAIGN.md`](../../../../radix/docs/factory/emission-lane-parity/CAMPAIGN.md) · radix [`cuda-rung-device-parity`](../../../../radix/docs/factory/cuda-rung-device-parity/goal.md) (its receipts fill the CUDA profile's evidence slots) · [`docs/factory/production-ml-library/CAMPAIGN.md`](../production-ml-library/CAMPAIGN.md) (owns execution-tier work; this goal owns honesty + parameterization)

---

## Invariant

Gradus source and docs state exactly what executes today — a CPU/reference
tier — and the library encodes no single backend family's law as admission:
KV-structure layout rules are per-family parameters with the current
(llama.cpp/Metal GI4) profile explicit and a declared CUDA profile slot that
fails closed until device evidence exists; capability matrices distinguish
"emittable" from "executed with receipt"; bench exemplars reserve mirror
slots for both lanes.

## Problem

Campaign evidence F6.1–F6.3. Gradus held its "no device handle" law (every
module header; verified), but neutrality eroded in three places:

| Gap | Evidence |
| --- | --- |
| One family's KV layout law is library admission: quantized V ⇒ must be Flash, Flash ⇒ straight V, Classic ⇒ transposed V — a valid plan whose layout another family prefers is rejected at construct time | `src/cache.fab:1361-1374` |
| The opened KV dtype set (F32/F16/Q8_0/Q4_K, **F16 default**) is not what executes (live `KVCache` f32-staged: `dtype()` "f32", `layout()` "staged") — opened set ≠ executed set, silently | `src/cache.fab:63-67, 632-636` vs `:265-273` |
| The bench exemplar pins Metal benches only (`llama-bench-*-metal.md`), and the design matrix marks Metal/CUDA storage cells "supported" where device runs were reserved (R-PACK-02 → R-PACK-05) — capability conflated with execution | `exempla/dense-prefill-smollm2/bench/`; `docs/design/numeric-flexibility-performance.md` vs `radix/docs/factory/gpu-production-readiness/exec02-packed-kernels-delivery.md` |

The audit also cleared Gradus of the suspected sin: no Metal/MPS/simd
vocabulary anywhere in live source; the `8`/`32` constants are GGML-format
and fixture sizes, not simdgroup tiles. The F32 host-list tensor model
(`src/tensor.fab:144-148`) is reference-tier by design — this goal labels
it, it does not replace it (device residency belongs to Radix EXEC rows).

## Proposal

1. **Parameterize KV-structure admission** (`src/cache.fab`): the
   layout-law table (family → allowed V layouts, allowed KV dtypes,
   quantization block rules) becomes an explicit profile record; the current
   profile is exactly today's GI4/llama.cpp law (behavior unchanged, proba
   green unchanged); a `cuda` profile slot exists with evidence fields that
   fail closed (unknown/unproven → reject with a named error, not silently
   reuse the Metal profile). Values arrive from ELP-06/EXEC-02 receipts.
2. **Tier truth pass**: `docs/design/numeric-flexibility-performance.md`
   matrix cells split into "emittable (recipe exists)" vs "executed
   (receipt exists)" columns citing receipts; `docs/api-shape-policy.md`
   and README state the CPU/reference tier as the executed tier of record.
3. **Bench mirror slots**: the dense-prefill bench gains CUDA-row slots
   (NONPRODUCT/pending markers, no numbers) so the mirror exists to fill
   when CAP-02 runs; README says benches pin Metal today and CUDA is
   reserved.

### Non-goals

- No tensor-residency re-architecture (host `list<f32>` stays the reference
  tier; device residency/streams are Radix/hosts EXEC territory).
- No CUDA execution of Gradus code (ELP-06 proves the lane on Radix
  fixtures; Gradus execution-tier work is production-ml-library).
- No numeric-behavior change for the current profile (proba must stay
  green, bit-identical).

## Units (lowering sketch — refine via `$delivery`)

| Unit | Scope | Depends on | Hand evidence |
| --- | --- | --- | --- |
| 1 | KV-layout profile parameterization in `cache.fab` (current GI4 profile explicit; `cuda` slot fail-closed) + proba rows unchanged | — | none |
| 2 | Design-matrix capability/executed split + api-shape-policy + README tier statements | — | none |
| 3 | Bench mirror slots (pending CUDA rows) + README bench statement | — | none |

## Validation

- `./scripta/check-compile` green; cache-module proba suites green and
  unchanged (bit-identical behavior for the admitted profile).
- A negative test: constructing a KV structure under the `cuda` profile
  before evidence exists fails closed with the named error.

## Ledger

| Unit | Status | Seat | Receipt | Notes |
| --- | --- | --- | --- | --- |
| 1 | done | hand | `2712d8f` | KV family-law profiles (F6.1) |
| 2 | done | hand | `c9961af` | opened-vs-executed dtype honesty (F6.2) |
| 3 | done | hand | `58e0155` | CPU/reference tier of record |
| 4 | done | hand | `d6f2b99` | matrix capability/executed split (F6.3) |
| 5 | done | hand | `58a704a` | bench CUDA mirror slots (F6.3) |
| 6 | done | hand | [`cache-proba-classification.md`](cache-proba-classification.md) (`324e344`) | closeout: `faber test --include cache` 33/0; bare `src/cache.proba` package-MIR miss classified environment-red |

## Open questions

1. **Profile home**: a `cache.fab`-local record vs a new small module
   (e.g. `model/profile.fab`)? *Default: cache-local — one consumer today;
   extract on the second consumer.*
2. **CUDA profile seed values**: predeclare expected law (llama.cpp CUDA
   flash-V straight layout) or leave empty until receipts? *Default: leave
   empty + fail closed — predeclaring would repeat the assumption drift
   this campaign exists to remove.*
3. **F16 default**: keep F16 as the declared default dtype in the opened set
   while the executed tier is f32? *Default: keep the opened set, document
   the staged-execution distinction in the same truth pass — changing the
   default is production-ml-library scope.*
