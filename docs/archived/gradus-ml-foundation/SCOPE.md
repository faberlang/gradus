# Gradus ML Foundation — Executive Team Goal Scoping

**Status**: scoped / not implementation-ready — feeds the architecture checkpoint
**Date**: 2026-08-01
**Process**: Executive team review (tugboat-style strategic review fan-out; full council)
**Reviewers**: head-ceo (strategist) · head-cto (gate honesty) · head-cpo (product)
· head-cso (security) · head-cmo (positioning) · head-cxo (purity)
**Artifact reviewed**: [`GOAL.md`](GOAL.md) + `README.md`, `AGENTS.md`, `src/*.fab` stubs, sibling-repo evidence
(radix @ 43724625c, norma @ e39cf0a, faber-runtime @ 3235129, examples @ b21d87d)

## Verdict

GOAL.md is a sound **vision** artifact. Its own completion posture is correct: no
factory phase should begin from it alone. The executive team confirms the next
authorized step is the **Horizon 0 architecture checkpoint**, and this scope
record narrows what that checkpoint must actually decide. The team also found
claim-honesty defects in the artifact that must be corrected before the
checkpoint closes.

## Convergent findings (multiple lenses, independent evidence)

| # | Finding | Lenses | Evidence |
| --- | --- | --- | --- |
| 1 | **Gradus↔Radix gradient seam is the binding hard gate.** The JAX-shaped API (wrapper signature, generated-companion shape, param-record handling, tensor shape) is asserted, not proven. Smallest producer fact: one live Gradus consumer fixture that imports `gradus:gradient`, defines a Gradus-owned differentiable primitive, compiles through Faber/Radix, runs the generated companion, and compares against an independent finite-difference oracle. | ceo (hard_gate), cto (hard_gate P1), cpo, cxo | GOAL.md "later delivery questions"; `radix-air/src/reverse_ad.rs` proves a compiler capability, not the wrapper contract |
| 2 | **Horizon 2 sequencing gap.** "Linear regression converges on CPU through library calls alone" needs a minimal training consumer, but `train` is scheduled at Horizon 7. Without a decision, the first proof uses demo-local orchestration and fails to prove the library boundary. | ceo (priority_inversion), cpo | GOAL.md Horizon 2 vs Horizon 7; `train` owns the loop per AGENTS.md |
| 3 | **Compiler-autograd claim is stale and over-broad.** "All 15 AIR tensor ops" is not current (live source describes 16/18 variants); proof code explicitly excludes source integration, backend emission, device execution, and training-loop scope; MLP inlines SGD; tensor-returning calls in loops trigger `SEM010`; BERT-tiny duplicates bias rows for unsupported rank-extension broadcast. | cto (bug P1), cmo | `radix-air/src/reverse_ad.rs`, `air_to_mir_backward_proof.rs`, `examples/training/mlp/src/train.fab`, `examples/training/bert-tiny-fragment/src/train.fab` |
| 4 | **Validation ladder is honest policy but not wired.** `check-source` exists; `check-compile` is named in README/AGENTS but absent from `scripta/`. Sibling tests prove the toolchain, not the Gradus package. | cto (hard_gate P1) | `gradus/scripta/` contains only `check-source`; sibling `compiler_generated_*_test.rs` run against `examples/`, not `gradus/src` |
| 5 | **Audience is blended.** Primary user must be named: Faber model authors. Radix/host are enabling stakeholders; nanoGPT is a forcing workload, not a co-equal customer. | cpo, cmo | GOAL.md "Primary product target" mixes all four |
| 6 | **train/data seam is underspecified.** `train` must not inherit tokenization/shuffling/loader policy. Decide: minimal `Batch` contract, or `train` consumes caller-provided `(params, batch)` values. Keep `train` data-independent for Horizon 2. | cxo, cso | GOAL.md DAG places `data` below `train`; `src/data.fab` "same batch interface" names no owner |
| 7 | **Unearned inventory commitments.** LR schedules, two of three position encodings, checkpointing, BPE, Adam are in the target shape before a caller demonstrates them. | cxo, cpo, cso | GOAL.md Horizons 4/6/9; `optimize/schedule` added before any schedule consumer; `position.fab` names three variants while "later questions" asks which is first |
| 8 | **Trust/security contracts must be baked in early, not discovered at Horizon 7–9.** | cso | — |

## Gate register (classifications)

| Gate | Classification | Smallest producer fact |
| --- | --- | --- |
| Gradus gradient wrapper seam | **hard** (blocks every public API) | One imported Gradus consumer fixture, compiled + FD-checked |
| Tensor genus shape (CPU ref + GPU dispatch) | **hard** (architecture) | Written tensor contract: shape, dtype, ownership, error behavior, dispatch-neutral seam |
| Companion export through `importa` | **cleared 2026-08-01** (was hard for cross-module backward) — SEM004 fixed: companions exportable through `importa`; consumer calls `gradient.loss_backward` mirror-free | radix `291432cab` + faber `180bcef`; verified `faber check gradus/exempla/gradient-seam/` → `ok:` (fresh compiler) |
| `faber run` library-import execution (LIB-MIR) | **cleared 2026-08-01** (was hard for consumer execution proofs) — `faber run -t fmir` links + executes library imports | faber `180bcef` + `983d6c7`; verified `faber run -t fmir gradus/exempla/gradient-seam/` → exit 0, FD match ~1e-11 (fresh compiler) |
| GPU gradient path (mir-swarm rung) | **hard for GPU-speed claims only**; NOT a blocker for CPU correctness or first training proof | One GPU backward workload with measured CPU/GPU loss-trace equivalence; owned by Radix/hosts |
| Safetensors device rung | **hard for checkpoint save/load only**; false as a gate for initial CPU training | CPU-only checkpoint round-trip fixture; device-aware load later |
| BPE tokenization | **soft** for nanoGPT path; false for first capstone (char-level suffices) | Deterministic char-level tokenizer + batched dataset fixture |
| Generic param-record field-mapping | **soft** — per-genus handwriting is sufficient for 1–2 model families | Two independent param records using the same optimizer API |
| `check-compile` harness | **hard** for Horizon 1 implementation | Checked-in Gradus compile harness resolving `FABER_LIBRARY_HOME` |

## Scope decisions (executive team integrated)

1. **First delivery slice** (active now): `math`, `tensor`, `gradient`, `loss/mse`,
   `optimize/sgd`, and **one training proof** (linear regression). Everything else
   in the inventory is deferred until a named caller or workload demonstrates it.
2. **Horizon 2 must decide the train seam**: either a minimal reusable
   forward→loss→backward→step contract, or an explicit exemplum-only proof with
   the reusable loop deferred. The decision must not let the exemplum hide a
   private autograd path.
3. **`train` stays data-independent** for the first slice: consume caller-provided
   batch values; define a `Batch` contract only when a second consumer proves it.
4. **Defer**: LR schedules (until a schedule consumer exists), Adam (until a
   second optimizer need), two of three position encodings (until nanoGPT proves
   one), checkpointing (until safetensors has a live consumer), BPE (until a
   concrete workload requires it).
5. **Facade + package rules** (`gradus:gradus` map-only, nested-package leaf
   counts, Norma duplication) are maintainership policy, not user acceptance
   criteria. Keep them out of the delivery's acceptance gates.

## Corrections to the artifact (claim honesty)

- Replace "all 15 AIR tensor operations" with a bounded capability matrix:
  compiler transform, MIR lowering, CPU execution, known unsupported cases.
- Add the compiler constraints to the baseline: `SEM010` for tensor-returning
  calls in loops; rank-extension broadcast limitation (BERT-tiny bias-row
  duplication); inlined SGD in the MLP exemplum.
- State that sibling tests validate the toolchain, not the Gradus package;
  Gradus integration is unproven until the fixture passes.
- README: "Who this is for / not yet for" section; separate shipped Radix
  capability from unimplemented Gradus user surface; nanoGPT is a **planned**
  forcing-function demo, not a demo that trains today.
- Align the import convention: top-level names (`gradus:loss`) are scaffold-era
  orientation; nested leaves (`gradus:loss/mse`) are target structure. Do not
  imply top-level facades re-export leaf types.
- `check-compile` must be created (not just documented) before Horizon 1.

## Trust/security contracts to bake in

- **Untrusted input boundary**: corpus text, tokenization inputs, BPE files,
  datasets, and future safetensors checkpoints are **data only** — never
  interpreted as Faber source, executable metadata, or arbitrary deserialization.
  Define size/shape/dtype validation and fail-closed parsing. Checkpoint loading
  read-only; save refuses overwrite by default.
- **Training defaults**: explicit RNG contract (seed ownership, stream separation,
  no-seed behavior), explicit train/eval mode for dropout, LR-schedule default
  resolved before any convergence claim, no silent checkpoint replacement.
  Metrics record seed/mode/schedule/checkpoint identity so a green run is auditable.
- **Parity for intentional duplication**: one external behavior-fixture boundary
  (scalar, shape-preserving update, broadcast/reduction, FD gradient) so Gradus
  math/optimizer and Norma math/optimizer — and compiler-generated AD vs the
  runtime oracle tape — cannot silently drift. Runtime tape is test-only; Gradus
  public code must not import it.
- **FD ≠ compiler trust**: finite-difference checks validate generated gradient
  behavior; they do not replace trust in the compiler pipeline. Capability claims
  require generated-gradient tests across Radix lowering/backend boundaries.
- **Cista distribution** (future): provenance/version pinning and integrity
  verification for the package and generated bindings before Horizon 9.

## Next step

The architecture checkpoint (Horizon 0) — lower to `delivery` once the operator
authorizes. Its mandated outputs, per this scope record:

1. One compiled Gradus consumer fixture proving the gradient wrapper seam
   (joint Gradus/Radix boundary decision).
2. Minimal tensor genus + param-record contract for CPU reference execution.
3. Horizon 2 train-seam decision (reusable contract vs exemplum-only).
4. Audience/promise boundary statement.
5. Capability-matrix correction committed to GOAL.md.
6. `gradus/scripta/check-compile` harness.
7. External dependency note: GPU rung owned by Radix/hosts, separate CPU vs GPU
   acceptance criteria.

## Stop conditions (unchanged)

All GOAL.md stop conditions stand. Add: do not claim a working Gradus training
system from sibling-repo compiler evidence, static source, or FD checks alone.
