# Gradus Benchmark Method

**Version**: `gradus-benchmark-method v1.0.0` (2026-08-11, PML6-U4)
**Repo**: gradus. **Tier**: structural only.
**Delivery**: `docs/factory/production-ml-library/pml6-delivery.md` §PML6-U4.
**Consumes (read-only)**: `docs/numeric-tolerances.md`,
`docs/regression-corpus.md`, `docs/compatibility-policy.md`,
`docs/factory/production-ml-library/pml0-support-matrix.md`, cross-repo
`numeric-policy v1.0.0` (`radix/docs/factory/gpu-training-lowering/numeric-policy.md`),
and the honest capability floors of
`radix/docs/factory/gpu-workload-floor/goal.md` (consumed, not duplicated).

This document pins **how** a Gradus benchmark is run and claimed. It does
**not** publish a speed number. No committed bench binary lands in this
phase (pml6-delivery.md Open Question 5). Executed regression/benchmark
passes are **auditor-owned** at the FMIR-lever gate (CTO8-1 / CTO8-3) —
never a dev-loop claim.

---

## 1. Claim rule (CPU-reference-level)

| Rule | Binding |
| --- | --- |
| **Correctness before speed** | A speed claim is admissible only after the structural correctness gates (§3) are green and the auditor-owned executed correctness gate has opened for the compared path. A speed number that precedes correctness **fails closed**. |
| **CPU-reference-level only** | Gradus-owned speed claims, when any exist, are **CPU / FMIR reference-level** wall times of the documented workload. They are not product GPU performance. |
| **GPU evidence is NGAB's** | Device throughput, kernel launch, and cross-backend executable timings are owned by the sibling native-GPU / NGAB campaigns. This method does not invent or re-state GPU speed floors. |
| **Workload floors consumed, not duplicated** | Honest capability floors from `gpu-workload-floor` (rung ladder, tier buckets, output-checked floor) are **evidence inputs**. This document cites that authority; it does not copy its floor constants or re-measure its rungs. |
| **No silent tier upgrade** | Structural-tier green (compile + pin inventory) never upgrades to an executed or GPU claim. Identity classes stay distinct (compatibility-policy §3 / R5). |
| **Hardware disclosure required** | Every speed claim names host, CPU model, core count, OS, faber binary identity, and sample protocol (§5). Undisclosed hardware voids the claim. |

---

## 2. Workloads in scope

These are the only workloads this method may time when a speed claim is
later admitted. Each is already a structural consumer of the public
`gradus:*` surface.

| Workload | Path | What is timed (when allowed) | Structural gate today |
| --- | --- | --- | --- |
| Library package | repo root (`faber check .`) | compile / typecheck latency of the library + co-located `.proba` surface | `./scripta/check-compile` |
| Gradient seam (library) | `exempla/gradient-seam` | compile of the library-import FD seam | `./scripta/check-compile` |
| Gradient seam (nolib) | `exempla/gradient-seam-nolib` | compile of the self-contained FD seam | structural consumer (README) |
| Training loop MLP | `exempla/training-loop-mlp` | compile of the accepted MLP 4×4 loop | `./scripta/check-compile` |
| Token generation | `exempla/token-generation` | compile of the bounded generation aggregate | `./scripta/check-compile` |
| Admission conformance | `tests/admission_conformance.fab` | compile of the capsule admission conformance | package consumer |

**Out of scope for Gradus speed claims**: GPU kernel launch, device
staging, WebGPU/CUDA/Metal throughput, multi-GPU, server batching, HTTP.
Those stay with Radix / NGAB / product hosts.

---

## 3. Correctness gates (must precede any speed number)

Before any wall-time sample is published as a claim:

1. **Source hygiene** — `./scripta/check-source` exit 0.
2. **Structural compile** — `./scripta/check-compile` exit 0
   (`faber check` on the library + admitted exempla consumers).
3. **Regression corpus inventory** — pins in
   `docs/regression-corpus.md` still resolve to live
   `src/**/*.proba` / fixtures (pin greps, §6).
4. **Numeric policy citation** — any numeric comparison in a timed path
   cites `numeric-policy v1.0.0` and
   `docs/numeric-tolerances.md` (no invented tolerances).
5. **Executed correctness (auditor-owned)** — when the path's claim is
   about executed values (loss, gradient, tokens), the FMIR-lever
   runtime-evidence gate must be green for that path. Until then only
   structural timing (compile / check latency) may be discussed, and
   still only with full hardware disclosure — never as product
   performance.

Gate ownership: Hand owns structural green in the delivery unit; auditor
owns executed regression + benchmark runs (CTO8-1 / CTO8-3). Dev-loop
suites do **not** run the executed pass.

---

## 4. Exact commands

All commands run from the gradus repository root unless noted.

### 4.1 Structural baseline (always; no speed claim)

```bash
cd /path/to/faberlang/gradus
./scripta/check-source
./scripta/check-compile
```

Optional symbol inventory (zombie-doc / coverage, not a timing workload):

```bash
./scripta/inventory-public-symbols
```

### 4.2 Per-consumer structural check (same gate, isolated)

```bash
export FABER_BIN="${FABER_BIN:-../faber/target/debug/faber}"
"$FABER_BIN" check .
"$FABER_BIN" check exempla/gradient-seam
"$FABER_BIN" check exempla/training-loop-mlp
"$FABER_BIN" check exempla/token-generation
```

`exempla/gradient-seam-nolib` is a structural consumer documented in its
README; include it in any full-consumer pass that claims "all exempla".

### 4.3 Wall-time sampling protocol (CPU-reference-level only)

When an auditor later records a CPU-reference wall time for one of the
§2 workloads, the sample command is:

```bash
# Example shape — substitute WORKLOAD and the exact command under test.
# Warmups discarded; N measured samples retained.
export FABER_BIN="${FABER_BIN:-../faber/target/debug/faber}"
WARMUPS=3
SAMPLES=10
CMD=("$FABER_BIN" check exempla/token-generation)   # example only

for i in $(seq 1 "$WARMUPS"); do
  "${CMD[@]}" >/dev/null
done

for i in $(seq 1 "$SAMPLES"); do
  /usr/bin/time -p "${CMD[@]}" 2>>bench-samples.txt
done
```

| Parameter | Value | Notes |
| --- | ---: | --- |
| **Warmups** | **3** | Discarded; stabilizes process/page-cache noise on CPU reference hosts. |
| **Measured samples** | **10** | Report min / median / max of wall time (`real` from `time -p`). |
| **Timer** | `/usr/bin/time -p` (or equivalent portable wall clock) | Wall time only; no GPU clocks. |
| **Stdout** | discarded during sampling | Avoid I/O-dominated false floors. |
| **Seed / input** | fixed per workload | Token-generation seed `8742514861359412281` and greedy path stay pinned (regression-corpus); do not retune for a better time. |

**No sample from this protocol is published in this unit.** The numbers
above pin the method only.

### 4.4 Executed regression / proba (auditor-owned; not dev-loop)

```bash
# Shape only — runs when the FMIR lever is open. Owner: auditor.
# Never claimed green from a Hand delivery unit.
"$FABER_BIN" test   # cargo-backed faber test harness; tree-wide residual today
```

Until that harness is unblocked, the structural corpus
(`faber check` + pin inventory) is the only green tier.

---

## 5. Hardware disclosure (required fields)

Every published CPU-reference claim carries this table filled in:

| Field | Example shape (fill at claim time) |
| --- | --- |
| Host name | e.g. `burgus` (local) / `pharos` (home server) |
| CPU | model string + logical core count |
| Memory | total RAM |
| OS / kernel | e.g. macOS / Linux + version |
| Architecture | e.g. `aarch64` / `x86_64` |
| Faber binary | path + version / git identity of `FABER_BIN` |
| Gradus commit | full SHA of the measured tree |
| Workload | one row from §2 |
| Warmups / samples | `3` / `10` per §4.3 |
| Result | min / median / max wall seconds |
| Tier | `cpu-reference` — never `gpu` |

Missing any required field voids the claim.

---

## 6. What this method does not claim

- No GPU speed, kernel occupancy, or device-vs-device comparison.
- No "matches PyTorch performance" or product-replace claim.
- No executed token / loss / gradient value from a Hand unit.
- No new benchmark binary, harness crate, or CI suite in PML6-U4.
- No redefinition of `gpu-workload-floor` rung floors.

---

## 7. Versioning

`gradus-benchmark-method v1.0.0`. Pre-1.0 clean-break posture
(`docs/compatibility-policy.md`). A method change that alters warmups,
sample counts, claim rules, or workload membership bumps this version
and records the delta in the commit message.

---

## 8. Validation (structural)

```bash
cd /path/to/faberlang/gradus
./scripta/check-source && ./scripta/check-compile
# pin greps live in docs/regression-corpus.md §Validation
test -f docs/benchmark-method.md
test -f docs/numeric-tolerances.md
test -f docs/regression-corpus.md
```
