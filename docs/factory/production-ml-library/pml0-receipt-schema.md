# Joint Cross-Repo Receipt Schema (PML0-U13, council C7)

**Schema version**: `joint-receipt-schema-1.0.0` (stamped 2026-08-08)
**Campaign**: `production-ml-library` (PML0, discovery-first)
**Unit**: PML0-U13 — joint receipt schema + Gradus-scoped audit entrypoint (C7)
**Status**: planned — the schema is frozen at PML0; receipts are produced by
later stages, never by this phase.
**Shared with**: NGAB0 receipts —
`faber/docs/factory/native-gpu-application-bundle/ngab0-delivery.md`
(NGAB0-U10, C7). One joint schema serves both campaigns: a receipt recorded
under this schema means the same thing in PML and NGAB stage trails.
**Authority**: `council-review-2026-08-08.md` C7; `pml0-delivery.md` PML0-U13;
`pml0-model-capsule-contract.md` (PML0-U14) §6 — the receipt's artifact-hash
field records the capsule digest, so convergence at PML7/NGAB7 is
content-addressed; `pml0-interface-packet.md` (PML0-U9) §VersionBump — schema
bumps route through the joint version-bump authority.
**Consumed by**: every PML1–PML7 stage receipt and every NGAB1–NGAB7 stage
receipt; the clean-install capstone receipts named in
`production-ml-library/CAMPAIGN.md` §Stages.

---

## 1. Purpose — receipts are the verifiable audit trail

A **receipt** is the machine-verifiable record that a stage or capstone
actually ran: what repo, at what revision, with what dirty state, under which
exact command, over which artifact identity, with which verdict, and at which
stage. Receipts are the evidence layer between a committed artifact and the
campaign's status claims — a claim without a receipt is a claim, not evidence
(authority order: `pml0-delivery.md` §Repo-Aware Baseline).

The schema is **joint** because PML0 and NGAB0 share the same inventory
discipline: both campaigns must be able to read each other's receipts without
a translator. A receipt is:

- **content-addressed** — the produced artifact is identified by a named
  digest of its bytes, never by path or filename (§3, field 5);
- **reproducible** — the exact command and revision make a re-run
  deterministic;
- **honest about absence** — `not_attempted` is a first-class verdict, never
  silently conflated with pass (NGAB0 hard-device gate precedent);
- **immutable** — a receipt is never edited after production; a correction is
  a new receipt that cites the one it supersedes.

## 2. Trust posture

- A file path is a **locator, not an identity**. Receipts name artifacts by
  hash; paths appear only as provenance inside the command field.
- A receipt never substitutes for the contract it evidences: passing a
  receipt does not change what the stage's delivery spec requires.
- Receipts do not inspect git, tests, or code — the goal-status audit does
  that. Receipts and the audit are separate layers; both are required at the
  status-audit gate (PML0 Gate C).

## 3. The seven mandatory fields

Every receipt, in either campaign, carries exactly these seven fields:

| # | Field | What it carries | Validation rule |
| --- | --- | --- | --- |
| 1 | **repo** | The owning repository of the executed stage (`gradus`, `radix`, `faber`, `hosts`, `norma`, `examples`) | A slug from the campaign's pinned repo set; no free-form text |
| 2 | **commit** | The exact revision the stage ran against | A git commit id that resolves in the named repo; the repo/commit pair is the stage's snapshot pin |
| 3 | **dirty state** | Whether the working tree carried uncommitted changes at execution time | Closed vocabulary: `clean` / `dirty`. A dirty execution is recorded, never silently normalized; an unrecorded dirty tree cannot produce a clean receipt |
| 4 | **command** | The exact command that produced the artifact/evidence | Full command line with version-pinned binaries (e.g. `FABER_BIN=faber 1.5.0`), reproducible verbatim; redaction of secrets only, marked as redacted |
| 5 | **artifact hash** | Content identity of the produced artifact | Named digest algorithm (default **SHA-256**, matching the capsule §3.2 and NGAB0-U4 defaults) + digest value. For model artifacts the value is the admitted capsule's cryptographic identity; never reconstructed from paths or naming conventions |
| 6 | **verdict** | The stage outcome | Closed vocabulary: `pass` / `fail` / `not_attempted`. A hardware or external gate that did not run is `not_attempted`, never implied pass |
| 7 | **stage** | Which campaign stage produced the receipt | Stage identifier from the owning delivery spec (e.g. `PML0-U13`, `NGAB0-U10`), one stage per receipt |

## 4. Joint alignment with NGAB0 receipts

NGAB0-U10 (`ngab0-delivery.md`) freezes the same schema on the faber side and
adds campaign-specific identity rows (compiler, faber, host, gradus, OS,
driver, device). The alignment rule:

- The **seven fields above are mandatory in both campaigns** and mean the
  same thing in both.
- NGAB may extend with additional fields as a **superset** — an extension
  never renames, reinterprets, or makes optional a joint field.
- Artifact identities + content digests (§3 fields 2, 4, 5) are the
  Gradus-side guarantee that a receipt row maps to one content-addressed
  artifact; NGAB0's manifest references the same digest values.
- A receipt is not "joint" by label but by shape: any PML receipt can be
  read by NGAB tooling and vice versa, with no per-campaign parser.

## 5. Capsule linkage (PML0-U14)

`pml0-model-capsule-contract.md` §6: *"receipts record the capsule's digest as
the artifact-hash field, so convergence at PML7/NGAB7 is content-addressed."*
Concretely:

- For a model-bearing stage, field 5 = the admitted capsule's cryptographic
  identity (SHA-256 over the whole validated file, capsule §3.2).
- The capsule is the **typed handoff** (§2) — a receipt references the capsule
  identity, never a raw GGUF path. Raw bytes/paths are not trust anchors, so
  they cannot be receipt anchors either.

## 6. Schema versioning and change procedure

- **Version stamp**: this schema is `joint-receipt-schema-1.0.0`. Every
  receipt records the schema version it conforms to.
- **Version owner**: the joint interface-packet authority (`pml0-interface-packet.md`
  §VersionBump) — the PML and NGAB campaign Minds acting together; the
  operator is the binding decision owner for disputed bumps.
- **Change procedure**: any addition, removal, or renaming of a mandatory
  field, or any change to a field's validation rule, requires a **major
  version bump** and re-validation across both campaigns, with a recorded
  reason. NGAB-only superset extensions follow the NGAB side's own revision
  procedure and never touch the joint fields.
- **Rejection**: a consumer that receives a receipt whose schema version it
  does not know must reject it — no partial reads, no silent tolerance.

## 7. This unit's validation proof

The PML0-U13 validation requires: (a) the seven joint fields named with
validation rules — §3, seven rows, each with a validation rule; (b) the
shared-with-NGAB0 declaration — §1 + §4 (joint schema, mandatory fields,
superset rule); (c) the capsule/artifact-hash linkage — §5; (d) a schema
version and change procedure — §1 header + §6; (e) `git diff --check` clean
at closeout.
