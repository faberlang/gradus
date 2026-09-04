# SGD-3/6 SmolLM2 GEA3 receipt — 2026-09-04

This is the closeout summary for the generic `gradus:kernel` route. The raw
receipt was produced by the ignored `gea3_real_metal_decode_receipt` test after
the bundle was regenerated from the live source and admitted through Hosts.

## Identity and route

- Gradus kernel source: `src/kernel.fab`, SHA-256
  `cf922d0d3e5738b722c0650c40c1b6603134552f608ac73b0452cd547a129285`
- Model: `SmolLM2-360M-Instruct-f32.gguf`, revision
  `a10cc1512eabd3dde888204e902eca88bddb4951`
- GGUF SHA-256:
  `4d10b02ea1b189cb9637b39ba1543c61f69a8766099076880888f4443754e128`
- Bundle census: 39 entries, 32 layers, 2,115 decode launches, 2,115
  prefill launches, and 2,146 declared edges on each route.
- Code revisions: Radix export route `dd6457888`, second-geometry Metal
  proof `b93f132ff`, and cache record `0fa7274ce`; Hosts `dc64d4c`.

## Staged and physical proof

- Staged composition: 2,115 stages; `first_bad = null` and
  `first_non_finite = null`.
- Physical backend: Metal on Apple M5 Max.
- Physical status: `green`.
- Greedy sequence: `[504, 31469, 6740, 335, 2591, 314, 5509, 38921, 28]`.
- Decode launches per step: 2,115; decode steps: 8.
- Intermediate readbacks: 0; explicit submit synchronizations: 8.
- CPU bridges: 0; CPU substitutes: 0.
- KV residency: 64 allocations, 6,225,920 bytes.
- Weight residency: 290 allocations, 1,447,284,480 bytes.

The receipt measured 53,659 µs prefill and 270,926 µs decode wall time.
Per-step GPU-body samples were `[12762, 12766, 12859, 12707, 12729,
12698, 12740, 12798]` µs, each with explicit 1,024/2,115 encoder coverage.
Those samples are retained as measured device timings, not presented as a
whole-graph performance total or a comparison against another revision.
