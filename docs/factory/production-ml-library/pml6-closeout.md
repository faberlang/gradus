# PML6 Closeout Note — phase gate MET at the structural tier; CTO8-1 remains a named pre-release item (does NOT gate PML6)

**Unit**: PML6 phase closeout (campaign gate; PML7 next per the ordering
graph)
**Date**: 2026-08-11
**Predecessor**: PML6-U1..U5 all landed and integrated on gradus main —
U1 `1f4f0d2` (API reference re-baseline + zombie-doc gate), U2 `649b2f6`
(diagnostics map + exempla READMEs; trailing-blank fix `29fb2fb`), U3
`43d75ce` (support-matrix full aggregation + compatibility policy), U4
`5a5f295` (benchmark method + tolerances + regression corpus; hand-4
parallel tip `5cac5f6`), U5 `9a2ed8b` (package metadata re-verify + release
checklist); main integration tip `0fbc97c`. Delivery: `pml6-delivery.md`.
**Repo**: gradus.

## Outcome: phase gate **MET at the structural tier** — PML6 delivered; CTO8-1 is a named pre-release item, not a PML6 gate

All five PML6 units landed. The phase gate (`pml6-delivery.md` §Checkpoints
And Gates — ten gate items committed and agree with live behavior; support
matrix + compatibility policy committed; claim register consistent;
regression corpus green once at structural tier; no executed claim beyond
structural; no performance claim precedes correctness) is satisfied at the
**structural (compile / source / committed-doc) tier**.

PML6 establishes the **quality and release contract** for the surface
PML1–PML5 built. No new ML semantics landed in this phase. Package version
stays `0.1.0` — **no version bump, tag, or release execution** in PML6.

Per the delivery boundary: **PML6's own gate does NOT depend on the
executed tier**. The CTO8-1 executed-oracle clause remains a **named
pre-release item** on the release checklist (open until the FMIR lever
lands). No executed proba, exemplum-e2e, or benchmark-value claims are made
in this closeout.

## Per-unit evidence

| Unit | Commit tip | Evidence (structural tier) | Tier |
| --- | --- | --- | --- |
| U1 — API reference (re-baseline + zombie-doc) | `1f4f0d2` | `docs/api-reference.md` (`gradus-api-reference v1.0.0`); `docs/module-map.md` + `docs/api-shape-policy.md`; README / AGENTS doc-ref fixes; `scripta/inventory-public-symbols` + `pml0-symbol-inventory.md` re-baselined; covers `tokenizator.est_eog`, `_be4_lege`/`_be8_lege`, EOG-set admission | structural |
| U2 — Diagnostics + examples | `649b2f6` (+ `29fb2fb`) | `docs/diagnostics.md` (`gradus-diagnostics v1.0.0`); exempla READMEs for `gradient-seam`, `gradient-seam-nolib`, `training-loop-mlp`, `token-generation` (pinned `[0]` / `[1, 1]` + first-token-divergence; structural/executed honesty) | structural |
| U3 — Support matrix + compatibility policy | `43d75ce` | `pml0-support-matrix.md` full-matrix aggregation (PML2 format + PML3 architecture + PML4 training + PML5 inference rows, EOG-stop semantics, structural tier marked never upgraded); `docs/compatibility-policy.md` (`compatibility-policy v1.0.0`); claim-register consistent (C5) | structural |
| U4 — Benchmark method + tolerances + regression corpus | `5a5f295` (`5cac5f6` parallel) | `docs/benchmark-method.md` (CPU-reference-level method; correctness before speed); `docs/numeric-tolerances.md` (numeric-policy v1.0.0 aggregate + token pins); `docs/regression-corpus.md` (proba + fixture inventory including EOG-stop `[0]`, seeded `[1, 1]`, capsule EOG rejection, reset/replay) | structural |
| U5 — Package metadata + release checklist | `9a2ed8b` | `faber.toml` / `cista.toml` re-verified (name `gradus`, version `0.1.0`, provider `gradus`, target `fmir`, interfaces `src` — **no drift, no bump**); `docs/release-checklist.md` (`gradus-release-checklist v1.0.0`) with CTO8-1 as **named pre-release item** (does NOT gate PML6) | structural |

## Ten gate items (1:1 to units) — phase checklist

| # | Gate item | Artifact | Unit | Verdict |
| --- | --- | --- | --- | --- |
| 1 | API reference versioned + re-baselined | `docs/api-reference.md` v1.0.0 | U1 | **MET** |
| 2 | Examples agree with pinned oracles | `exempla/*/README.md` | U2 | **MET** |
| 3 | Diagnostics stable code + message + resolution | `docs/diagnostics.md` v1.0.0 | U2 | **MET** |
| 4 | Support matrix full-matrix aggregation | `pml0-support-matrix.md` | U3 | **MET** |
| 5 | Compatibility policy versioned | `docs/compatibility-policy.md` v1.0.0 | U3 | **MET** |
| 6 | Benchmark method committed (CPU-reference) | `docs/benchmark-method.md` v1.0.0 | U4 | **MET** |
| 7 | Tolerances versioned | `docs/numeric-tolerances.md` v1.0.0 | U4 | **MET** |
| 8 | Regression corpus (proba + fixtures inventory) | `docs/regression-corpus.md` v1.0.0 | U4 | **MET (structural)** |
| 9 | Package metadata agrees with live behavior | `faber.toml` + `cista.toml` @ `0.1.0` | U5 | **MET** (no bump) |
| 10 | Release checklist committed artifact | `docs/release-checklist.md` v1.0.0 | U5 | **MET** |

## Stage checkpoints

| Checkpoint | Evidence | Verdict |
| --- | --- | --- |
| SG1 (after U1) | API reference + inventory re-baseline + README/AGENTS fixes; inventory script green | **MET** |
| SG2 (after U2 + U3) | Diagnostics + exempla READMEs; full support-matrix aggregation + claim register + compatibility policy | **MET** |
| SG3 (after U4 + U5) | Benchmark method + tolerances + regression corpus; package metadata agrees; release checklist with named executed item | **MET** |
| Phase gate | Ten items committed + live agreement (zombie-doc discipline); matrix + policy committed; claim register consistent; regression corpus structural inventory; no executed claim beyond structural; CTO8-1 named pre-release only; no performance claim precedes correctness; no version bump | **MET (structural)** |
| Executed regression / benchmark / oracle runs | Env-blocked on the FMIR lever (CTO8-1 / CTO8-3) | **NOT claimed** — auditor-owned at the FMIR-lever gate |
| CTO8-1 executed-oracle (product pre-release) | Recorded on release checklist §6; open until FMIR lever + `exempla_script_e2e` green for library-importing packages | **NAMED PRE-RELEASE ITEM** — does **not** gate PML6 |

## Decision context honored

- **Structural tier only**: every unit and this closeout stay at compile /
  source / committed-doc agreement. No executed proba values, token runs,
  loss trajectories, or benchmark numbers are claimed.
- **CTO8-1 does not gate PML6**: the executed-oracle clause is a named
  pre-release item on `docs/release-checklist.md`, consumed by PML7-U3 and
  the faber product release protocol. Dated trigger remains 2026-08-09
  (hand-1 FMIR e2e-hardening + `exempla_script_e2e` green for
  library-importing packages); CTO8-3 dated re-verification of PML4 pins +
  PML5 tokens stays with the auditor when the lever opens
  (`pml5-closeout.md`).
- **No version bump**: `faber.toml` / `cista.toml` remain `0.1.0`. Release
  execution (bump, tag, push, clean-install receipts) is PML7 + faber
  release protocol owned.
- **No new ML semantics**: diagnostics-string and documentation scope only
  per delivery non-goals.
- **Correctness before performance**: benchmark method is CPU-reference
  level; GPU evidence remains NGAB / `gpu-workload-floor`; no speed claim
  precedes the correctness gates.
- **Ordering-graph pointer**: PML7 (training + inference capstones) is the
  next Gradus phase; NGAB6 portability consumes the support matrix +
  compatibility policy + benchmark method as the portability feed.

## Residuals closed by this phase

| # | Residual (from prior closeouts / delivery) | Disposition |
| --- | --- | --- |
| PML3 #1 / PML4 #3 / PML5 #4 | Full support-matrix aggregation of admitted rows | **CLOSED** by U3 (`43d75ce`) |
| Delivery residual Z1–Z4 | README / AGENTS / inventory / exempla zombie-doc drift | **CLOSED** by U1 + U2 |
| Delivery residual #1–#2 (matrix + CTO8 routing) | Matrix aggregation; CTO8 on checklist | **CLOSED** for PML6 scope (CTO8 stays open as pre-release, not as a phase residual) |

## Residuals + owners (still open after PML6)

| # | Residual | Owner | State |
| --- | --- | --- | --- |
| 1 | CTO8-1 executed-oracle clause: oracle-matching tokens (executed) + CTO8-3 re-verification (PML4 trajectory + PML5 tokens) when FMIR lever opens | Auditor (executed-tier gate) + hand-1 (FMIR lever) | open — named pre-release item; trigger dated 2026-08-09 |
| 2 | PML7 capstones: training app + inference app on public Gradus; clean-install receipts (PML0-U13); consume release checklist | PML7 delivery owner + faber release protocol | pending — PML7 |
| 3 | NGAB6 portability feed: support matrix + compatibility policy + benchmark method as structural identity inputs (R5 — executed identity separate) | NGAB6 delivery owner | pending — NGAB6 |
| 4 | Executed regression corpus + benchmark runs (method committed; values auditor-owned) | Auditor at FMIR-lever gate | pending — same lever as CTO8-1 |
| 5 | Product version bump / tag / push | Faber product release protocol | not PML6 — pre-1.0 clean-break; no bump this phase |

## Validation (one closeout run — structural)

```bash
cd /Users/ianzepp/work/faberlang/gradus   # or this worktree
./scripta/check-source && ./scripta/check-compile
git diff --check
# optional / when present:
# ./scripta/inventory-public-symbols
# python3 ../radix/scripta/generate-factory-readme.py --factory-root docs/factory --check
# ./scripta/check-factory-goal-status --fail-on error
```

- `check-source` + `check-compile`: structural green (batch / fire-9 norm).
- `git diff --check`: clean on the closeout path set.
- Factory README regenerated if the generator is local (`docs/factory/README.md`).
- Goal-status audit: 0 findings expected after CAMPAIGN / delivery Status
  lines reflect delivered (structural tier).
- **No executed claim**: this validation is structural only; FMIR-lever
  executed runs remain auditor-owned (CTO8-1).
