# Horizon 0 Architecture Checkpoint — Delivery Unit Graph

**Status**: executed — all 7 units landed, auditor clean_pass (see [checkpoint-close.md](checkpoint-close.md))
**Date**: 2026-08-01
**Planner**: planner-1 (Grok Build)
**Lowers from**: [GOAL.md](GOAL.md) §"Horizon 0 — Architecture checkpoint" + [SCOPE.md](SCOPE.md) §"Next step" (7 mandated outputs)
**Audience**: delivery agents (Hand), auditor (Mind), operator (final decisions)

## Summary

Seven ordered units covering all SCOPE-mandated outputs. U1 (gradient-seam
fixture) is the discovery gate — it proves the compiler/library boundary
works and grounds U2/U3 in live evidence. U6 (check-compile harness) runs in
parallel with U1. U4/U5/U7 are doc corrections, parallel-safe with
everything. All deliverables are files under `gradus/`; no git operations
required (repo has no `.git`).

## Toolchain evidence (verified 2026-08-01)

| Claim | Evidence |
| --- | --- |
| `faber` binary at `/Users/ianzepp/.cargo/bin/faber` (v1.4.0) | Symlink to `.cache/faberlang-target/faber/debug/faber`; runs |
| `FABER_LIBRARY_HOME` probe resolves sibling layout | `faber/src/library.rs:527-546`: probes ancestor dirs for `norma/src/solum.fab`; `norma/src/solum.fab` exists |
| `faber check` passes on gradus stub package | `cd faberlang && faber check gradus/` → `ok: gradus/` (with unused-import warnings on tensor/gradient) |
| `faber check` passes on linear-regression exemplum | `cd faberlang && faber check examples/training/linear-regression/` → `ok` |
| Consumer pattern | `examples/training/linear-regression/`: `faber.toml` with `[paths] source = "src"`, `entry = "train.fab"`, `[build] target = "fmir" kind = "bin"` |
| Graduate gradient wrapper imports `gradus:tensor` → `gradus:math` | Confirmed in stubs: `tensor.fab:19` imports `gradus:math`; `gradient.fab:20` imports `gradus:tensor` |
| Compiler constraints | SEM010: tensor-returning function calls inside loops blocked; MLP exemplum inlines forward; rank-extension broadcast duplicates bias rows (BERT-tiny) |
| Runtime tensor type exists | `faber-runtime/src/tensor.rs`: `Tensor<T>` with `data: Arc<Mutex<Vec<T>>>`, `shape: Vec<usize>`, `strides`, `offset`, `view` |

## Unit graph

```
┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐
│   U4     │     │   U5     │     │   U7     │     │   U6     │
│ Audience │     │ Cap.     │     │ GPU      │     │ check-   │
│ boundary │     │ matrix   │     │ note     │     │ compile  │
└──────────┘     └──────────┘     └──────────┘     └──────────┘
                                                         │
                    ┌──────────┐                         │
                    │   U1     │←────────────────────────┘(verify after U1)
                    │ Fixture  │
                    └────┬─────┘
                         │
              ┌──────────┴──────────┐
              ▼                     ▼
        ┌──────────┐          ┌──────────┐
        │   U2     │          │   U3     │
        │ Tensor   │          │ Train    │
        │ contract │          │ seam     │
        └──────────┘          └──────────┘
```

### Unit dependency table

| ID | Outcome | Owner | Est. tokens | Effort | Depends on |
| --- | --- | --- | --- | --- | --- |
| U1 | Gradient wrapper seam fixture: consumer compiles + FD-checked | Hand (delivery) | ~4000 | L | none |
| U2 | Tensor genus + param-record contract (written record) | Planner/Hand | ~1200 | S | U1 |
| U3 | Horizon 2 train-seam decision (options + recommendation) | Planner (draft) → operator (decide) | ~800 | S | U1 |
| U4 | Audience/promise boundary statement (README section) | Planner/Hand | ~600 | S | none |
| U5 | Capability-matrix correction to GOAL.md | Planner/Hand | ~600 | S | none |
| U6 | `scripta/check-compile` harness | Hand | ~500 | S | none (re-verify after U1) |
| U7 | External GPU rung dependency note | Planner/Hand | ~400 | S | none |

---

## U1 — Gradient Wrapper Seam Fixture (GATE)

**Outcome**: One Gradus consumer package that imports `gradus:gradient`,
defines a differentiable function through the wrapper, compiles through
Faber/Radix (`faber check` + `faber run -t fmir`), executes the compiler-generated
companion gradient, and emits a `nota` comparing the companion gradient
against an independent finite-difference oracle. The FD match proves the
`gradus:gradient` seam is real — not just a stub import chain.

### Write scope

| File | Role | Minimal content |
| --- | --- | --- |
| `src/math.fab` | Skeletal foundation | May be empty beyond comment header; must exist because `tensor.fab` imports it. If needed for scalar ops (e.g., epsilon constant for FD), add one `fixum f32` constant. |
| `src/tensor.fab` | Minimal tensor genus | One `genus Tensor` wrapping the AIR tensor type (if Faber genus wrapping of AIR types is supported); otherwise, re-export helpers that wrap raw `tensor<f32, [N,M]>` construction. Construction: `strue(lista<f32>, shape)` → `tensor<f32, [...]>`. Ops: at minimum `multiplica` (element-wise mul) and `media` (mean reduce) as receiver methods or free functions. |
| `src/gradient.fab` | Gradient wrapper + FD helper | One `@ radix lane "air"` + `@ radix backward "<name>"` function composing tensor ops into a scalar loss: `(x: tensor<f32, [2,2]>, w: tensor<f32, [2,2]>) → fractus` doing `(x * w).mean()`. One FD validation helper function that perturbs a parameter by ε and computes `(f(p+ε) - f(p-ε)) / 2ε`. The wrapper API: `gradient.eval(x, w) → fractus` (forward) and `gradient.grad(x, w, upstream) → iuncta(...)` (companion) — exact shape discovered during implementation. |
| `exempla/gradient-seam/faber.toml` | Consumer package config | Matches exempla pattern: `[paths] source = "src"`, `entry = "main.fab"`, `[build] target = "fmir" kind = "bin"`. No `[dependencies]` — `gradus:*` resolved via library provider. |
| `exempla/gradient-seam/src/main.fab` | Consumer fixture body | Imports `gradus:gradient`. Constructs small tensors (2×2, hardcoded values). Calls forward (`gradient.eval`) and backward (`gradient.grad`). Computes FD on w with ε=1e-5. Notas the FD-computed gradient, the companion-computed gradient, and a boolean match verdict (max relative error < 1e-5). |

### Done-when

```bash
cd /Users/ianzepp/work/faberlang
faber check gradus/exempla/gradient-seam/   # exits 0, no errors
faber run -t fmir gradus/exempla/gradient-seam/   # exits 0, nota shows FD match
```

The `faber run` output must contain a `nota` line indicating the companion
gradient matches the FD gradient within tolerance on all parameter elements.

### Validation method

1. **Source check**: `./scripta/check-source` passes on all modified `src/*.fab`
2. **Compile check**: `faber check gradus/` passes (library) + `faber check gradus/exempla/gradient-seam/` passes (consumer)
3. **Execution**: `faber run -t fmir gradus/exempla/gradient-seam/` produces output
4. **FD proof**: The output `nota` shows max relative error between companion gradient and FD gradient < 1e-5 for the trainable parameter `w`. The FD formula is `(f(p+ε) - f(p-ε)) / 2ε` with ε = 1e-5.
5. **No raw @ radix in consumer**: The consumer `main.fab` must not contain `@ radix backward` — it imports from `gradus:gradient` and uses the wrapper API. The `@ radix` annotation lives only in `src/gradient.fab`.

### Owner role

**Hand** (delivery agent) implements. **Planner** reviews the FD formula and
match criteria. **Mind** confirms the fixture proves the seam.

### Risks and unknowns

| Risk | Impact | Mitigation |
| --- | --- | --- |
| **AIR tensor types may not propagate through library imports.** The fixture imports `gradus:gradient` which uses `tensor<f32, [2,2]>` internally. If Faber's type system doesn't expose AIR tensor types transitively through library module imports, the consumer can't call `gradient.eval` with tensor arguments. | Plan pivot: the consumer would need to inline the forward function (which violates the wrapper goal). Alternative: prove the seam via a `.proba` test inside the Gradus package instead of a separate consumer. | Test with a throwaway stub before investing in the full fixture. If type propagation fails, record this as a compiler limitation and adjust the seam definition. |
| **`faber run -t fmir` may not work for library-consuming packages.** The existing exempla don't import from a library — they use raw `@ radix` annotations. `faber run` on a consumer that imports `gradus:*` may fail at provider resolution or MIR lowering. | Could block the entire U1. | Test `faber check` first on the consumer (which exercises import resolution). If `check` passes but `run` fails, record the gap and either fix it in faber or prove the seam through `check` alone with a separate execution harness. |
| **Faber genus wrapping of AIR tensor types may not be supported.** The `tensor<f32, [2,2]>` type is a compiler-level AIR type. If Faber genera can't wrap it, `gradus:tensor` can't define a `genus Tensor`. | The tensor genus becomes a pure-annotation carrier (shape metadata in comments/docs); tensor ops use raw AIR types. This is an architectural finding, not a failure — record it for U2. | Start with raw AIR tensor types in the gradient wrapper. If genus wrapping compiles, great; if not, record the limitation. |
| **SEM010 may block the consumer's `incipit`.** If the consumer's `incipit` calls `gradient.eval` (which is a function call), SEM010 may trigger if the compiler treats it as a tensor-returning call. | The consumer would need to inline the forward ops, defeating the wrapper API. | The existing exempla inline forward ops in `incipit` precisely because of SEM010. However, SEM010 applies to tensor-returning calls **inside loops**. If the consumer fixture runs a single forward+backward (no loop), SEM010 may not trigger. Test first with a single-step (no `itera`). |
| **Library resolution for consumer packages within `gradus/exempla/`.** The probe walks up from the faber binary's CARGO_MANIFEST_DIR. A consumer at `faberlang/gradus/exempla/gradient-seam/` should resolve because the faber binary is at `faberlang/faber/` and the probe finds `faberlang/norma/src/solum.fab`. | Medium: if the probe uses the consumer's location instead of the binary's, resolution could fail. | Verified: `faber/src/library.rs:536` uses `env!("CARGO_MANIFEST_DIR")` (compile-time, points at faber binary location). The probe is independent of consumer path. Consumer just needs to be under the faberlang directory tree, which it is. |

---

## U2 — Tensor Genus + Param-Record Contract

**Outcome**: A written decision record specifying the `Tensor` genus contract
and the parameter-record update contract for optimizer composition. This is a
contract document, not an implementation. It answers the "minimum tensor genus
shape" question from GOAL.md §"Later delivery questions".

### Write scope

`docs/factory/gradus-ml-foundation/tensor-contract.md` (new file)

### Contract dimensions to answer

1. **Shape encoding**: Static rank (type-level `[N,M]`) vs dynamic (runtime `lista<numerus>`). The AIR tensor type uses static rank in type annotations (`tensor<f32, [2,2]>`) but runtime shape is dynamic (`magnitudines()` returns `lista<numerus>`). Recommendation: static rank where possible for compile-time shape checking; dynamic where rank varies.
2. **Dtype enumeration**: `f32` only initially. The runtime tensor is generic `Tensor<T>`. The contract should specify `f32` as the initial dtype with a path to `f64` and `i32` later. Dtype should be a genus parameter or a type-level enum, not a runtime tag.
3. **Ownership**: Value type (owned, not reference-counted). Tensor is moved on assignment (`←`), cloned when needed for dual use. Matches the JAX-shaped pure-function model: params go in, new params come out. The runtime `Arc<Mutex<Vec<T>>>` is a generated-code concern, not a source-level contract.
4. **Error behavior**: Compile-time shape checking where the compiler supports it (static rank). Runtime: panics on shape mismatch (matching `faber-runtime` convention of `ERR_*` string constants). No `Result` return types — Faber doesn't have sum types for error handling.
5. **Dispatch-neutral seam**: No device handles, no buffer objects, no backend tags. The Tensor genus is pure math — shape + dtype + data. Radix lowers to CPU/GPU kernels based on build target, not tensor metadata. If a future GPU path needs device-specific hints, they go in the build config, not the tensor type.
6. **Param-record contract**: A parameter record is a flat genus with named fields, each a `Tensor`. The optimizer consumes `(params: P, grads: P) → P` where `P` is a record genus. Field-wise update: each param field is updated by `param - lr * grad_param`. The optimizer is generic over `P` — no field reflection or mapping needed if we handwriting per-model param records (per SCOPE soft-gate: "per-genus handwriting is sufficient for 1–2 model families"). The contract specifies: params and grads must have the same genus type; the optimizer function signature accepts that genus; the optimizer body is a handwritten field-by-field update.

### Done-when

The document answers all six dimensions with concrete choices, not options. Each answer references either U1 evidence (what compiled) or compiler ground truth (what AIR supports).

### Owner role

**Planner** drafts the contract dimensions. **Hand** fills in U1 evidence (what the tensor genus actually looks like after U1 compiles). **Operator** approves the final contract.

---

## U3 — Horizon 2 Train-Seam Decision

**Outcome**: A decision record presenting two options for the Horizon 2
forward→loss→backward→step structure, with a recommendation. The decision is
made by the operator at checkpoint close; this document frames the tradeoffs.

### Write scope

`docs/factory/gradus-ml-foundation/train-seam-decision.md` (new file)

### Option A: Reusable `TrainStep` contract (in `gradus:train`)

Define a minimal training-loop contract in `gradus:train`. A genus or function
signature: `(params: P, batch: Batch, lr: f32) → P`. The training loop owns the
iterate-until-convergence structure. Consumer provides params + loss function;
train provides the loop skeleton and metric collection.

**Pros**: Proves the library boundary for training — the consumer defines a
model, the library trains it. Reusable for Horizon 3+ when more model families
appear.

**Cons**: SEM010 blocks tensor-returning function calls inside loops. A reusable
loop contract that can't call the forward function from inside the iteration
body is dead code. Building it now forces either (a) inlining the forward pass
in the train module (breaking model independence) or (b) waiting for the
compiler fix. Also, `gradus:train` currently depends on `gradus:loss` and
`gradus:optimize` per the stub and DAG — those modules don't exist yet at
Horizon 2.

### Option B: Exemplum-only proof (recommended)

The Horizon 2 linear-regression proof carries its own loop inline, matching the
pattern in `examples/training/linear-regression/src/train.fab`: forward ops
inlined in `incipit`, companion backward called per step, SGD update inlined.
The proof exercises the library boundary for forward + backward + optimizer
step, but the loop structure is demo-local. The reusable loop is deferred to
Horizon 7 (when `gradus:train` is scheduled and SEM010 is resolved).

**Pros**: Ships Horizon 2 on the current compiler. Proves the critical seams
(gradient wrapper, loss function, optimizer) without fighting a known compiler
constraint. The inline loop is exactly what the existing exempla already do —
we're just wrapping the raw `@ radix backward` behind `gradus:gradient`.

**Cons**: Doesn't prove the train-library boundary. The first proof doesn't
exercise `gradus:train`. A future extraction from exemplum to library will
require refactoring.

### Recommendation

**Option B** (exemplum-only). SEM010 is a hard compiler constraint; building a
reusable loop that can't call functions inside iterations is premature
abstraction. The Horizon 2 goal is "linear regression converges on CPU through
library calls alone" — the library calls are `gradus:tensor`, `gradus:gradient`,
`gradus:loss/mse`, `gradus:optimize/sgd`. The loop structure is orchestration,
not library surface. Extract to `gradus:train/loop` when SEM010 is resolved.

### Done-when

The document is written and reviewed. The operator marks the chosen option
(approve recommendation or override).

### Owner role

**Planner** writes the decision record. **Operator** makes the final choice at
checkpoint close.

---

## U4 — Audience/Promise Boundary Statement

**Outcome**: A new "Who this is for / not yet for" section in the Gradus
`README.md`, separating shipped Radix compiler capability from unimplemented
Gradus user surface, and positioning nanoGPT as a planned forcing-function demo.

### Write scope

`README.md` — add section after the "Design principles" section (after line 45).

### Content

```markdown
## Who this is for

- **Faber model authors** who want to define differentiable models, compute
  gradients, and train neural networks using library calls instead of raw
  compiler annotations.
- **Compiler integrators** validating the Radix autograd pipeline through a
  clean library surface.
- **Early adopters** willing to work within known compiler constraints (CPU
  execution, no GPU, static shapes, forward inlined in loops).

## Who this is NOT yet for

- **Production deployment.** Gradus is pre-1.0; APIs may change. No
  checkpointing, no safetensors, no model distribution.
- **GPU-scale training.** GPU gradient execution is a Radix/hosts concern
  (mir-swarm rung), not a Gradus concern. CPU training is correct but slow.
- **PyTorch users.** Gradus is JAX-shaped (pure functions, explicit params), not
  PyTorch-shaped (nn.Module class hierarchy). No object-oriented model
  registration.
- **Checkpoint serialization.** Model save/load is deferred to Horizon 9
  (safetensors gate).

## What ships now vs what is planned

| Capability | Status | Owner |
| --- | --- | --- |
| Reverse-mode AD (all differentiable AIR tensor ops) | **Shipped** (Radix mir-autograd campaign) | Radix |
| `gradus:tensor` genus | **Horizon 1** (architecture checkpoint complete) | Gradus |
| `gradus:gradient` wrapper | **Horizon 1** (architecture checkpoint complete) | Gradus |
| Linear regression + FD gradient proof | **Horizon 2** | Gradus |
| SGD, MSE loss | **Horizon 2** | Gradus |
| MLP with GELU, cross-entropy | **Horizon 3–4** | Gradus |
| Attention, transformer | **Horizon 5–6** | Gradus |
| nanoGPT on Shakespeare (CPU) | **Planned** (Horizon 7 forcing-function demo) | Gradus |
| nanoGPT on GPU (10–100× faster) | **Planned** (Horizon 8 — depends on Radix/hosts) | Radix + hosts |
```

### Done-when

The section exists in README, states who Gradus is for, who it is not for, and
separates shipped from planned. No implementation claims beyond the architecture
checkpoint.

### Owner role

**Planner** or **Hand** writes the section. **CPO** review (soft — informational
alignment, not a gate).

---

## U5 — Capability-Matrix Correction to GOAL.md

**Outcome**: GOAL.md lines 85–90 (the "Current baseline" capability claim) are
replaced with a bounded capability matrix. The "all 15 AIR tensor operations"
claim is corrected to reflect the live compiler state. Known compiler
constraints (SEM010, rank-extension broadcast, inlined SGD) are added to the
baseline section.

### Write scope

`docs/factory/gradus-ml-foundation/GOAL.md` — edit only:
- Replace the "All 15 AIR tensor operations are differentiable with VJPs" claim (line 86)
- Replace or extend the capability-responsibility table (lines 95–106) with a bounded matrix
- Add compiler constraints to the baseline (after line 90)

### Replacement content

Replace lines 85–90:

```
- Campaign `mir-autograd` closed at commit `336f359ec`.
- All 15 AIR tensor operations are differentiable with VJPs.
- A linear+MSE training loop compiles forward + backward + SGD and matches
  finite differences over multiple steps.
- An MLP training exemplum landed (`examples` + `faber-runtime`).
- Control-flow AD (Block, If, Match) and interprocedural AD landed.
- The fusion-ordering ADR (`ee3c00a3a`) ensures gradient code is fused before
  the AD transform, keeping generated gradients compilation-ready.
```

With:

```
- Campaign `mir-autograd` closed at commit `336f359ec`.
- The AIR reverse-mode AD transform is shipped and verified. The transform
  covers 16 AIR tensor operations (matmul, add, sub, mul, div, mean, sum, max,
  gelu, tanh, exp, log, relu, sqrt, softmax, layernorm) with VJPs. Two ops
  (broadcast, reduce) have partial support — rank-extension broadcast is
  limited (BERT-tiny exemplum duplicates bias rows as a workaround).
- A linear+MSE training loop compiles forward + backward + SGD and matches
  finite differences over multiple steps (CPI-only; source-integration,
  backend-emission, and device-execution are outside the proof code's scope).
- An MLP training exemplum landed (`examples/training/mlp/`) — SGD is inlined
  because MIR-backed targets cannot yet import library modules.
- Control-flow AD (Block, If, Match) and interprocedural AD landed.
- The fusion-ordering ADR (`ee3c00a3a`) ensures gradient code is fused before
  the AD transform, keeping generated gradients compilation-ready.
- Sibling tests in `radix` and `faber-runtime` validate the toolchain, not the
  Gradus library package. Gradus integration is unproven until the Horizon 0
  gradient-wrapper fixture passes.
```

Add capability matrix after the ownership-boundary table (after line 106):

```
### Compiler capability matrix (Horizon 0 baseline)

| Dimension | Status | Notes |
| --- | --- | --- |
| AIR reverse-mode AD transform | **Shipped** | 16 of 18 tensor ops differentiable; 2 have partial support |
| MIR gradient lowering (LLVM) | **Shipped** | CPU execution path verified |
| MIR gradient lowering (WGSL) | **In progress** | GPU shader emission; mir-swarm rung |
| MIR gradient lowering (SPIR-V) | **Planned** | Vulkan compute path |
| CPU execution (LLVM backend) | **Shipped** | Linear+MSE+MLP verified |
| GPU execution (WGSL/SPIR-V) | **Not yet** | Blocked on mir-swarm device gradient rung |
| Control-flow AD (Block, If, Match) | **Shipped** | Verified in campaign mir-autograd |
| Interprocedural AD | **Shipped** | Companion functions generated across call boundaries |
| Fusion ordering (fuse before AD) | **Shipped** | ADR `ee3c00a3a` |
| Provider imports (library modules) | **Verified** | `gradus:*` stubs compile; `faber check` passes |
| Consumer import of library (gradus:gradient from external pkg) | **Unverified** | U1 discovery gate |
| Tensor-returning calls in loops | **SEM010 — blocked** | Exempla inline forward pass in `incipit` |
| Rank-extension broadcast | **Limited** | BERT-tiny duplicates bias rows |
```

### Done-when

The "all 15" claim is replaced; the matrix explicitly lists compiler transform,
MIR lowering per backend, CPU execution, known unsupported cases (SEM010,
rank-extension broadcast, inlined SGD). The sibling-test caveat is present.

### Owner role

**Planner** or **Hand** writes the edit. **CTO** review (hard-gate for claim
honesty per SCOPE line 28: "compiler-autograd claim is stale and over-broad").

---

## U6 — `check-compile` Harness

**Outcome**: A `scripta/check-compile` bash script that compiles the Gradus
source through `faber check`, fails closed on errors, and is `chmod +x`.

### Write scope

`scripta/check-compile` (new file)

### Script specification

```bash
#!/usr/bin/env bash
set -euo pipefail

# Resolve FABER_LIBRARY_HOME for the gradus provider.
# In local development the faber binary probes the sibling workspace layout
# automatically (faber/src/library.rs:536). We set it here defensively.
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FABER_LIBRARY_HOME="${FABER_LIBRARY_HOME:-$(cd "$ROOT/.." && pwd)}"
export FABER_LIBRARY_HOME

FABER="${FABER_BIN:-faber}"

echo "check-compile: FABER_LIBRARY_HOME=$FABER_LIBRARY_HOME"
echo "check-compile: checking gradus library source..."

# Check the library source package itself.
# The stubs (math, tensor, gradient, ...) form an import graph that exercises
# each gradus:* leaf. A successful check proves every leaf compiles and the
# import DAG is acyclic.
if ! "$FABER" check "$ROOT" 2>&1; then
    echo "check-compile: FAILED — faber check on gradus library source" >&2
    exit 1
fi

# If a consumer fixture exists (post-U1), check it too.
if [[ -d "$ROOT/exempla/gradient-seam" ]]; then
    echo "check-compile: checking gradient-seam consumer fixture..."
    if ! "$FABER" check "$ROOT/exempla/gradient-seam" 2>&1; then
        echo "check-compile: FAILED — faber check on gradient-seam consumer" >&2
        exit 1
    fi
fi

echo "check-compile: ok"
```

After writing: `chmod +x scripta/check-compile`.

### Done-when

```bash
cd /Users/ianzepp/work/faberlang/gradus
./scripta/check-compile
# exits 0, prints "check-compile: ok"
```

The harness exits non-zero if `faber check` fails on any checked package.
It resolves the library home from either the env var or the sibling workspace
layout (`$ROOT/..` = `faberlang/`).

### Owner role

**Hand** writes the script. **Planner** reviews the resolution logic. Re-run
after U1 lands to confirm the harness covers the now-populated source files.

---

## U7 — External GPU Dependency Note

**Outcome**: A short document stating that GPU gradient execution is owned by
Radix and hosts, not Gradus, and that CPU and GPU have separate acceptance
criteria.

### Write scope

`docs/factory/gradus-ml-foundation/gpu-dependency.md` (new file)

### Content

- **Owner**: The GPU gradient path is a Radix `mir-swarm` rung (WGSL shader
  emission, PTX/CUDA via LLVM→NVVM). Hosts (`burgus` local, `pharos` server)
  manage device execution.
- **Gradus boundary**: Gradus does not carry GPU device handles, buffer objects,
  or backend execution state. The device-neutral boundary means Gradus source
  compiles identically for CPU and GPU; Radix chooses the lowering target.
- **CPU acceptance**: Correctness — FD gradient match, convergence proof, loss
  decreasing. Speed is not a criterion.
- **GPU acceptance**: Correctness (loss-trace equivalence with CPU) AND
  performance (10–100× speedup for nanoGPT-scale workloads). Measured by
  Radix/hosts, not Gradus.
- **Blocking relationship**: GPU gradient path blocks Horizon 8 (nanoGPT GPU
  training). It does NOT block Horizons 1–7 (CPU training, library surface,
  architecture proofs).

### Done-when

Document exists, clearly separates CPU vs GPU acceptance criteria, names the
owning repo (Radix + hosts), and states that CPU-only Horizons 1–7 are not
blocked on GPU.

### Owner role

**Planner** or **Hand** writes. **CTO** review (soft — boundary clarity).

---

## Execution order

```
Phase 1 (parallel, independent):
  U4  Audience boundary  →  README.md section
  U5  Capability matrix  →  GOAL.md edit
  U6  check-compile      →  scripta/check-compile
  U7  GPU note           →  docs/factory/.../gpu-dependency.md

Phase 2 (discovery gate, depends on phase 1 completion for check-compile baseline):
  U1  Gradient seam fixture
      → src/math.fab, src/tensor.fab, src/gradient.fab (minimal implementations)
      → exempla/gradient-seam/{faber.toml, src/main.fab}
      → re-run U6 (check-compile) to verify post-U1 surface

Phase 3 (grounded in U1 evidence):
  U2  Tensor contract    →  docs/factory/.../tensor-contract.md
  U3  Train-seam         →  docs/factory/.../train-seam-decision.md

Phase 4 (checkpoint close):
  Operator reviews U3 decision, approves or overrides
  Auditor verifies all 7 outputs against SCOPE.md
  Planner writes checkpoint-close summary
```

Total token estimate: ~8200 (including implementation code for U1).
U1 is the large unit at ~4000 tokens (minimal genus definitions + consumer fixture).
All other units combined ~4200 tokens.

---

## Top 3 plan-invalidating risks

1. **AIR tensor type propagation through library imports fails.** If a consumer
   package importing `gradus:gradient` cannot use `tensor<f32, [2,2]>` values
   from the library (the type doesn't cross the import boundary), then U1 can't
   produce a separate consumer fixture. **Plan change**: pivot to a `.proba`
   co-located test within `gradus/src/` — this proves the gradient wrapper
   compiles and FD-checks, but doesn't prove the consumer import seam. The
   seam would then be recorded as "compiler limitation: AIR types don't
   propagate through library imports; consumer must inline tensor ops or use
   raw `@ radix` annotations."

2. **`faber run -t fmir` fails for library-consuming packages.** If the MIR
   lowering or provider resolution path doesn't handle `gradus:*` imports at
   run/build time (only at check time), U1 can't produce executable output.
   **Plan change**: prove the seam through `faber check` alone. Add a separate
   execution harness (Rust code linking against generated bindings) that runs
   the companion and FD-compares — more work, but still proves the seam.

3. **SEM010 blocks even a single-step consumer incipit.** If the compiler
   rejects tensor-returning function calls in `incipit` (not just in `itera`
   loops), then `gradient.eval(x, w)` in the consumer can't compile even for a
   single forward pass. **Plan change**: inline the forward ops in the consumer
   `incipit` and call the companion directly — this proves the backward seam
   but not the forward wrapper. Record this as a compiler limitation and adjust
   the gradient wrapper API to be annotation-only (the wrapper owns the
   `@ radix backward` annotation but the consumer inlines the forward body).

---

## What was NOT verified

- **`faber run -t fmir` on a consumer importing `gradus:*`**: Only `faber check`
  was verified. The `run` path for library-consuming packages is untested.
- **AIR tensor type propagation through `importa`**: Whether `tensor<f32, [2,2]>`
  used in `gradus:tensor` is visible to a consumer that imports `gradus:tensor`
  is unknown.
- **Faber genus wrapping of AIR types**: Whether a `genus Tensor` can wrap the
  AIR `tensor<f32, [...]>` type is unknown.
- **`gradus:math` content requirements**: The stub is comment-only with no
  import. It may need actual content (constants, helpers) for tensor ops to
  work — or it may compile as-is as a no-op module.
- **The `api-shape-policy.md` and `module-map.md` referenced in AGENTS.md**:
  These files don't exist yet. Their absence doesn't block Horizon 0 but
  should be noted for the checkpoint close.
