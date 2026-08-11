# Gradus Release Checklist

**Version**: `gradus-release-checklist v1.0.0` (2026-08-11, PML6-U5)
**Repo**: gradus · **Scope**: library quality/release contract for the public
`gradus:*` surface (pre-1.0, version `0.1.0`).
**Consumed by**: PML7-U3 (clean-install + release receipts) and the faber
product release protocol (`faber/AGENTS.md` Release protocol; faber
`docs/release/release-checklist.md` for product tagging).
**Does not execute**: this document names the items; it does not bump, tag,
push, or cut a release. Version bumps and product release execution remain
with the faber release protocol. Clean-install receipts are produced by
PML7-U3, not this phase.

**Authority**: `docs/factory/production-ml-library/pml6-delivery.md` §PML6-U5;
campaign release-prep checkpoint (PML6 establishes the contract; PML7 + faber
protocol consume it).

---

## Boundary — what this checklist is and is not

| This checklist | Not this checklist |
| --- | --- |
| Names every release item that must resolve to a committed artifact before a Gradus library cut is honest | Does not perform version bumps, tags, or pushes |
| Structural-tier gates (source/compile, inventory, docs agree with live) | Does not claim executed proba / e2e value-identity |
| Records CTO8-1 as a **named pre-release item** | **Does NOT gate PML6** — PML6 phase gate is structural only |
| Feeds PML7-U3 + faber release protocol | Clean-install receipts are PML7-U3 owned |

**Identity classes** (R5): structural tier = semantic identity of the compiled
surface; executed tier = a separate claim. Never conflate the two.

---

## 0. Package metadata re-verification (PML6-U5)

Re-verify before every release prep. **No version bump in PML6.** Expected
live values (2026-08-11, structural tier):

| File | Field | Expected | Live |
| --- | --- | --- | --- |
| `faber.toml` | `[package].name` | `gradus` | `gradus` |
| `faber.toml` | `[package].version` | `0.1.0` | `0.1.0` |
| `faber.toml` | `[library].provider` | `gradus` | `gradus` |
| `faber.toml` | `[paths].source` | `src` | `src` |
| `faber.toml` | `[build].kind` | `lib` | `lib` |
| `faber.toml` | `[build].target` | `fmir` | `fmir` |
| `cista.toml` | `[source].package` | `gradus` | `gradus` |
| `cista.toml` | `[source].version` | `0.1.0` | `0.1.0` |
| `cista.toml` | `[source].kind` | `source` | `source` |
| `cista.toml` | `[source].interfaces` | `src` | `src` |

**PML6-U5 re-verification note (2026-08-11)**: `faber.toml` and `cista.toml`
agree with live behavior — name `gradus`, version `0.1.0`, provider `gradus`,
target `fmir`, interfaces `src`. **No drift corrected.** Version remains
`0.1.0` (no bump this phase). Layout: cista maps `interfaces = "src"` into
`$CISTAE_HOME/gradus/<version>/interfaces/`; faber resolves `gradus:*` via the
library provider over the same tree.

**Check**:

```bash
# Metadata fields present and consistent
grep -E 'name|version|provider|target|interfaces|source|package' faber.toml cista.toml
test -d src && test -f faber.toml && test -f cista.toml
```

---

## 1. Docs fresh (zombie-doc discipline)

Every product-facing doc must **agree with live behavior** before release.
Undocumented public symbols fail the inventory coverage gate.

| # | Item | Committed artifact | Check |
| --- | --- | --- | --- |
| 1.1 | API reference re-baselined | `docs/api-reference.md` (`gradus-api-reference v1.0.0`) | `./scripta/inventory-public-symbols` exit 0 |
| 1.2 | Module map | `docs/module-map.md` | file exists; AGENTS.md link resolves |
| 1.3 | API shape policy | `docs/api-shape-policy.md` | file exists; AGENTS.md link resolves |
| 1.4 | Diagnostics map | `docs/diagnostics.md` | every public error has code + message + resolution |
| 1.5 | Compatibility policy | `docs/compatibility-policy.md` (`compatibility-policy v1.0.0`) | pre-1.0 clean-break + identity rules recorded |
| 1.6 | Benchmark method | `docs/benchmark-method.md` | exact commands / warmups / sample counts / hardware disclosure; CPU-reference-level only |
| 1.7 | Numeric tolerances | `docs/numeric-tolerances.md` | aggregates numeric-policy v1.0.0 + token-pin rules |
| 1.8 | Regression corpus inventory | `docs/regression-corpus.md` | inventories admitted-row fixtures + proba pins |
| 1.9 | README status tables | `README.md` | no shipped surface labeled planned/scaffold (or vice versa) |
| 1.10 | Exempla READMEs | `exempla/*/README.md` | documented outputs match pinned oracles; structural/executed tier stated honestly |

**Batch structural validation** (always green at unit/closeout boundaries):

```bash
./scripta/check-source && ./scripta/check-compile
./scripta/inventory-public-symbols
git diff --check
```

Items 1.6–1.8 are the PML6-U4 surface; they must be present and consistent
before a release cut. Their **executed** runs are auditor-owned (see §6).

---

## 2. Support matrix + claim register final pass

| # | Item | Committed artifact | Check |
| --- | --- | --- | --- |
| 2.1 | Full-matrix aggregation | `docs/factory/production-ml-library/pml0-support-matrix.md` | every admitted row has all schema fields + committed evidence links; structural tier marked |
| 2.2 | Support-matrix schema | `docs/factory/production-ml-library/pml0-support-matrix-schema.md` (`gradus-support-matrix-schema v0.1.0`) | schema version matches matrix stamp |
| 2.3 | Claim register consistent | `docs/factory/production-ml-library/pml0-claim-register.md` | no row reads as product support without evidence (C5); closed vocabulary |
| 2.4 | Compatibility policy aggregate | `docs/compatibility-policy.md` | row-level `compatibility policy` fields remain row authority; aggregate names breaks / migrations / identity rules |

**Final-pass rule (PML7-U3 + release prep)**: walk every support-matrix row
and every claim-register row. Reject any row that cannot cite a committed
evidence path. No unsupported claims may ship.

---

## 3. Version policy

The **version policy** for Gradus package and doc stamps:

| Rule | Value |
| --- | --- |
| Package version (faber + cista) | `0.1.0` until an intentional bump |
| Pre-1.0 posture | **clean break** — no stability promise, no forwarding shims, no deprecation window (`docs/compatibility-policy.md` §1) |
| Doc artifact versions | versioned stamps on product docs (e.g. `gradus-api-reference v1.0.0`, `compatibility-policy v1.0.0`); bump recorded per each doc's rules |
| Who bumps | **faber product release protocol** owns product versioning; Gradus package version bumps are deliberate release-prep acts — never silent in a feature unit |
| What this phase forbids | version bump, tag, push, or release execution inside PML6 |

```bash
# Version agreement across package files
grep -E 'version\s*=' faber.toml cista.toml
```

---

## 4. PML0-U13 receipts (joint schema)

Release and capstone evidence uses the **joint cross-repo receipt schema**
(`joint-receipt-schema-1.0.0`):

**Authority**: `docs/factory/production-ml-library/pml0-receipt-schema.md`
(PML0-U13 / council C7). Shared with NGAB0 receipts.

Every receipt carries exactly these seven fields:

| # | Field | Closed rule |
| --- | --- | --- |
| 1 | **repo** | slug from the campaign's pinned repo set |
| 2 | **commit** | git commit id that resolves in the named repo |
| 3 | **dirty state** | `clean` / `dirty` only |
| 4 | **command** | exact command line; version-pinned binaries |
| 5 | **artifact hash** | named digest (default SHA-256) + value |
| 6 | **verdict** | `pass` / `fail` / `not_attempted` only |
| 7 | **stage** | stage id from the owning delivery spec (one stage per receipt) |

**Producer**: PML7-U3 writes clean-install + capstone receipts under this
schema. This checklist only requires that receipts **exist and conform**
before a Gradus-consuming product release claims the capstones.

---

## 5. Clean-install

| # | Item | Owner | Artifact / action |
| --- | --- | --- | --- |
| 5.1 | Training capstone clean-install | PML7-U1 / PML7-U3 | temporary home, no sibling checkout; public-only `gradus:*` imports; pinned package + toolchain versions |
| 5.2 | Inference capstone clean-install | PML7-U2 / PML7-U3 | same pin discipline; oracle-matching tokens at the tier admitted for the cut |
| 5.3 | Receipts for both capstones | PML7-U3 | PML0-U13 joint schema (repo, commit, dirty state, command, artifact hash, verdict, stage) |

**Not owned by PML6**: do not produce clean-install receipts in this phase.
PML6 only names the gate so PML7 and the faber release protocol can execute it.

---

## 6. Named pre-release item — CTO8-1 executed-oracle (does NOT gate PML6)

> **NAMED PRE-RELEASE ITEM — open until the FMIR lever lands.**
> This item is recorded on the release checklist so it cannot be silently
> dropped at product cut. It is **not** a PML6 phase-gate clause.
> PML6 closes on the structural tier (compiled surface + pinned oracle
> values + docs agree with live). Executed value-identity is a separate,
> auditor-owned claim.

| Field | Value |
| --- | --- |
| **Clause id** | **CTO8-1** — NAMED EXECUTED-GATE CLAUSE |
| **What it is** | "Oracle-matching tokens (executed)" and executed proba / e2e value-identity for the admitted Gradus surface |
| **State** | **OPEN** (recorded 2026-08-09 in `pml5-closeout.md`; restated here for release) |
| **Trigger** | hand-1's FMIR e2e-hardening lands **AND** `exempla_script_e2e` is green for library-importing packages (FMIR library-call gap = sole remaining execution blocker) |
| **Owner** | Auditor (executed-tier gate) + hand-1 (FMIR lever) |
| **Re-verification** | **CTO8-3** (dated 2026-08-09): when the trigger fires, one auditor-owned pass re-runs PML4 trajectory pins + resume + seeds **and** PML5-U6 tokens (`[0]` / `[1, 1]`) under numeric-policy v1.0.0 |
| **PML6 relationship** | **Does NOT gate PML6.** PML6 phase gate = structural tier only. See `pml6-delivery.md` entry gate + residual #2. |
| **Release relationship** | A **product** release that claims executed Gradus correctness must close CTO8-1 first (or honestly scope the claim to structural tier only). |

**Sources**: `docs/factory/production-ml-library/pml5-closeout.md` §CTO8-1 /
§CTO8-3; `pml6-delivery.md` entry gate + residual #2; README / exempla
execution-record honesty (CTO Q2).

**Honest claim rule**: until CTO8-1 closes, every release note, README status
row, and support-matrix cell that touches execution remains **structural
tier** — never upgraded to executed identity by implication.

---

## 7. Structural release gates (always required)

Run before any Gradus library cut or PML7 closeout that claims the surface:

```bash
cd gradus
./scripta/check-source
./scripta/check-compile
./scripta/inventory-public-symbols
# Optional closeout hygiene (when docs/factory status claims move):
# python3 ../radix/scripta/generate-factory-readme.py --factory-root docs/factory --check
# ./scripta/check-factory-goal-status --fail-on error
git diff --check
```

| Gate | Meaning |
| --- | --- |
| `check-source` | source layout + interface hygiene |
| `check-compile` | library + fire-9 consumers compile (structural) |
| `inventory-public-symbols` | public symbol counts + coverage vs `docs/api-reference.md` |
| `git diff --check` | no whitespace errors on the tip |

Executed regression / benchmark / exempla e2e runs: **auditor-owned** at the
FMIR-lever gate (CTO8-1 / CTO8-3) — never a silent dev-loop claim.

---

## 8. Operator summary (cold path)

Before claiming a Gradus library release is ready for product consumption:

1. **Metadata** — §0 fields match live (`gradus` / `0.1.0` / provider `gradus` / `fmir` / `interfaces = "src"`).
2. **Docs fresh** — §1 artifacts present; inventory coverage green; no zombie labels.
3. **Matrix + register** — §2 final pass; no unsupported claims (C5).
4. **Version policy** — §3; intentional bump only; pre-1.0 clean-break recorded.
5. **Receipts schema ready** — §4 joint schema is the only receipt shape.
6. **Clean-install** — §5 executed by PML7-U3 (or explicitly deferred with `not_attempted` receipts).
7. **CTO8-1** — §6 still open → release claims stay structural; if product claims executed correctness, close CTO8-1 + CTO8-3 first.
8. **Structural gates** — §7 green.

**Then** hand off to the faber product release protocol for any product-level
bump / tag / publish that includes Gradus as a dependency.

---

## References

| Artifact | Path |
| --- | --- |
| PML6 delivery (U5) | `docs/factory/production-ml-library/pml6-delivery.md` |
| PML7 delivery (U3 consumes this) | `docs/factory/production-ml-library/pml7-delivery.md` |
| PML5 closeout (CTO8-1 / CTO8-3) | `docs/factory/production-ml-library/pml5-closeout.md` |
| Receipt schema (PML0-U13) | `docs/factory/production-ml-library/pml0-receipt-schema.md` |
| Support matrix | `docs/factory/production-ml-library/pml0-support-matrix.md` |
| Claim register | `docs/factory/production-ml-library/pml0-claim-register.md` |
| Compatibility policy | `docs/compatibility-policy.md` |
| Package metadata | `faber.toml`, `cista.toml` |
| Faber release protocol | `faber/AGENTS.md` (Release protocol); `faber/docs/release/release-checklist.md` |
