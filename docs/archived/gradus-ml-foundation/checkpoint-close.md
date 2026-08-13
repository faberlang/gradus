# Horizon 0 Architecture Checkpoint — Close (Freeze Receipt)

**Status**: complete — frozen; compiler-fix track (LIB-MIR, SEM004, SEM010) cleared 2026-08-01
**Date**: 2026-08-01
**Process**: tugboat flow (planner-1 lower → auditor plan-check → parallel Hands U1/U4/U5/U6/U7 → U2/U3 → auditor implementation-check → corrections → re-verify clean_pass)
**Mind**: integration + freeze (this record)
**Operator decision**: U3 train-seam Option C (compiler-fix-first) — **made 2026-08-01** (see below)

## Baselines

- **Repo**: `/Users/ianzepp/work/faberlang/gradus` — no git repo initialized (all work is uncommitted files on disk; sibling repos at radix @ 43724625c, norma @ e39cf0a, faber-runtime @ 3235129, examples @ b21d87d, hosts @ d8b03a2).
- **Toolchain**: `faber` v1.4.0 on PATH; `FABER_LIBRARY_HOME` unset (sibling-workspace probe active).
- **Source of mandate**: `SCOPE.md` (7 mandated outputs) — verified 1:1 covered by the unit graph (auditor, plan check).

## Admitted units (all 7)

| Unit | Outcome | Landed | Accepted |
| --- | --- | --- | --- |
| U1 | Gradient-seam fixture: import proof + execution proof | `src/{math,tensor,gradient}.fab`, `exempla/gradient-seam/`, `exempla/gradient-seam-nolib/`, `faber.toml` (target=fmir) | Yes |
| U2 | Tensor genus + param-record contract | `docs/factory/gradus-ml-foundation/tensor-contract.md` | Yes |
| U3 | Train-seam decision record | `docs/factory/gradus-ml-foundation/train-seam-decision.md` | Yes (decision open) |
| U4 | Audience/promise boundary | `README.md` §Who this is for / not yet for | Yes |
| U5 | Capability-matrix correction | `GOAL.md` §Current baseline + §Compiler capability matrix | Yes |
| U6 | `scripta/check-compile` harness | `scripta/check-compile` (+x) | Yes |
| U7 | GPU dependency note | `docs/factory/gradus-ml-foundation/gpu-dependency.md` | Yes |

## Repaired units

- **README.md Status §**: stale "all 15 AIR tensor ops" → 16 of 18 + partial support (auditor correction 1, re-verified clean).
- **SCOPE.md gate register**: added two U1-discovered hard gates — companion export through `importa` (SEM004), `faber run` library-import execution (LIB-MIR) (auditor correction 2, re-verified clean).

## Validation evidence (auditor re-ran, not just Hand-claimed)

- `./scripta/check-source` → exit 0
- `faber check gradus/` → `ok:` (WARN002/WARN003 benign for scaffold)
- `faber check gradus/exempla/gradient-seam/` → `ok:` (import seam proven)
- `faber check gradus/exempla/gradient-seam-nolib/` → `ok:`
- `faber run -t fmir gradus/exempla/gradient-seam-nolib/` → exit 0; forward 2.25, companion `[0.25, 0.5, 0.75, 1.0]`, FD match ~1e-11, diffs ≤ ~2e-11
- `faber run -t fmir gradus/exempla/gradient-seam/` → exit 1 with LIB-MIR error (expected, correct reason)
- `./scripta/check-compile` → exit 0, checks library + consumer, prints `check-compile: ok`

## Compiler limitations discovered (U1 — the checkpoint's real yield)

| # | Limitation | Error | Impact |
| --- | --- | --- | --- |
| 1 | Companion functions are file-scoped, not exportable through `importa` | SEM004 `namespace_missing_export` | Consumer cannot call `@ radix backward` companion across import boundary; must mirror the annotation |
| 2 | `faber run -t fmir` rejects library imports | `package MIR does not yet support library imports such as gradus:gradient` | Check path works; run path requires self-contained exempla |
| 3 | Genus wrapping of AIR tensor types unsupported | PARSE001 | Public representation = raw AIR `tensor<f32,[N,M]>` types, not a `genus Tensor` |
| 4 | AIR lane requires MIR-backed target in library package | TARGETLANE001 | `faber.toml` needs `target = "fmir"` (singular) |
| 5 | `.proba` tests + AIR lanes incompatible (faber test is HIR-direct) | — | FD validation lives in exempla, not co-located `.proba`, until test targets support MIR/AIR |

## Frozen module map (Horizon 0 output)

Unchanged from the target inventory in GOAL.md §Proposed Gradus file inventory, with two enforcement notes from U1:

- **`gradus:tensor`**: raw AIR tensor types are the public representation (genus wrapping is a future compiler capability). `f32` dtype only for Horizon 1–2.
- **`gradus:gradient`**: owns `@ radix backward` annotations; companions are file-scoped today, so the wrapper's forward surface is importable while companion access is same-file. The gradient module is pure calculus (no imports from loss/optimize/nn/attention/transformer) — enforced by stub import graph.
- Dependency DAG (math/tensor → gradient → loss/optimize → nn → attention/transformer → train/data → Radix+host): confirmed directionally correct by audit; reverse-import enforcement is a future manifest/check lint, not yet tooling-enforced.

## Gate register after U1 (SCOPE.md updated)

The two U1-discovered hard gates are now recorded: **SEM004 companion export** and **LIB-MIR library-import run**. Both gate the consumer execution seam independently. Tensor genus (raw AIR types) remains the hard architecture gate, now with a written contract (U2).

## Horizon 1–2 handoff (delivery spec pointer) — compiler-fix-first

The checkpoint's purpose per GOAL.md was to "convert one bounded horizon into a
delivery spec." The bounded first horizon is **Horizon 1–2 (Foundation + First
Training Proof)**, now sequenced **compiler-first** per the operator's Option C
decision:

1. **Compiler-fix track (Radix/Faber, driven by Gradus)** — three gates,
   sequenced, with fix sites identified in
   [`train-seam-decision.md`](train-seam-decision.md):
   - LIB-MIR: `faber run -t fmir` accepts library imports
     (`faber/src/package/mir.rs:1440–1462`; compiled package execution already exists)
   - SEM004: companion functions exportable through `importa`
     (`radix/.../typecheck/call.rs:374`)
   - SEM010: tensor-returning calls legal inside `itera` loops
2. **Then the JAX-shaped surface**: `gradus:loss/mse`, `gradus:optimize/sgd`,
   and the reusable `gradus:train` contract `(params: P, batch: Batch, lr: f32) → P`.
3. **Then the proof**: a linear-regression consumer importing `gradus:train`,
   executing through `faber run`, converging on CPU — no mirrored `@ radix
   backward` in the consumer, no inline loop.

Enforced constraints from this checkpoint: raw AIR tensor types (no genus),
f32-only, value semantics, static shapes, per-genus handwritten param records
(U2), exemplum-only loop **rejected** — the reusable loop is the target, not a
deferral. Do not start: `gradus:data`, checkpointing, BPE, Adam, schedules
(deferred per SCOPE scope decisions).

## Operator decision (U3) — made 2026-08-01

The operator **overruled the Option B recommendation** and chose **Option C:
fix the compiler so the JAX-shaped reusable `gradus:train` contract is
executable, then build it.** Rationale: Option B (exemplum-only, inline loop,
mirrored `@ radix backward`) repeats the runtime-tape mistake — it makes the
architecture work by working around the compiler, baking in the anti-pattern
and forcing a rebuild when the compiler catches up. The three compiler gates
become Radix/Faber producer work driven by Gradus, sequenced
LIB-MIR → SEM004 → SEM010, with fix sites identified in
[`train-seam-decision.md`](train-seam-decision.md). The runtime tape stays a
test-only validation oracle; it is not extended to fill the gap.

## Review debt

- Required auditor review debt: **zero** (plan residual → implementation residual → corrections → clean_pass).
- Open follow-ups (not blocking): `check-compile` does not cover `gradient-seam-nolib` (per plan spec); `check-source` scans `src/` only, not `exempla/`; `module-map.md` and `api-shape-policy.md` still absent (referenced by AGENTS.md; not Horizon 0 deliverables).

## Next posture

**Compiler-fix track CLEARED 2026-08-01** — all three gates shipped and
verified with the fresh compiler: SEM004 (companion export, radix `291432cab`
+ faber `180bcef`), SEM010 (factored forward in loop, examples `249e29e`),
LIB-MIR (`faber run -t fmir` library imports, faber `180bcef` + `983d6c7`).
Consumer `gradus/exempla/gradient-seam/` runs mirror-free with FD match ~1e-11.

**Horizon 1–2 delivery** is now unblocked: the reusable `gradus:train` contract
is executable on the current toolchain. The GOAL.md status line is updated
below. No factory phase may begin from GOAL.md alone — delivery lowers from
this freeze receipt + the unit deliverables + the cleared-gate evidence.
