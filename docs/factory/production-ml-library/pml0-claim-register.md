# PML0 Claim/Capability Register

**Unit**: PML0-U12 (C5) — cross-campaign claim/capability register skeleton —
see `pml0-delivery.md` PML0-U12.
**Status**: skeleton — first Gradus rows admitted (evidence-backed); further
campaigns add rows per the cross-campaign scope note (§4).
**Schema version stamp**: `gradus-claim-register-schema v0.1.0` (2026-08-08)
**Dependencies**: PML0-U5 (`pml0-support-matrix-schema.md`) row vocabulary —
register rows reuse the `format`/`architecture`/`dtype`/`quantization`/
`tokenizer identity` vocabulary so claim status never reads as product
support; PML0-U9 (`pml0-interface-packet.md`, revision `pml0-interface-packet
v1`, revisable through PML1/NGAB1); PML0-U1 (`pml0-source-snapshot.md`)
version stamps.
**Consumed by**: PML0-U10 (`pml0-gradus-contract.md`, contract assembly),
PML1+ (rows move as units land), the sibling NGAB0 register
(`faber/docs/factory/native-gpu-application-bundle/ngab0-claim-register.md`).

## Purpose

One register mapping **claims** (what the Gradus ML surface can do) to their
current truth, each with a single owner, an evidence reference, and a campaign
stage. It is cross-campaign: every row names its source campaign, and later
campaigns add rows rather than rewriting this file.

**Authority order** (campaign, `pml0-delivery.md` §Repo-Aware Baseline): live
Gradus source + tests → accepted Gradus contracts → accepted compiler/package
contracts → campaign stage receipts → examples and historical plans. Evidence
refs below point at committed artifacts only; the live-HEAD stamps are those of
`pml0-source-snapshot.md` (gradus `d7e85aa`, drift-replaced) as superseded by
the later PML0 unit commits.

## 1. Row schema (versioned)

Each row has exactly the following fields. All five are required; a row is a
single markdown table row.

| # | Field | Vocabulary (closed set) | Validation rule |
| --- | --- | --- | --- |
| 1 | `claim` | Product-level statement of what the surface can do | Must be a single falsifiable capability statement; a claim that generalizes beyond its evidence (e.g. "GGUF is supported") **rejects** the row. |
| 2 | `status` | Claim status, **closed vocabulary**: `accepted` / `partial` / `in flight` | Must be exactly one of the three claim-status tokens. Rows that record a claimed-off surface use the non-claim marker `none` and live in §3, **not** here. |
| 3 | `owner` | Single owner per surface (U4 §3 ownership table; `pml0-gradus-contract.md` §OwnershipMatrix) | Exactly one owning module/party; non-owners excluded; ambiguous or dual ownership **rejects** the row. |
| 4 | `evidence ref` | Committed artifact: frozen contract section, snapshot, live source, ledger row, or receipt | Must resolve to a committed path/line at the recorded stamp; contract prose is evidence only when the referenced section is frozen; an unresolvable ref **rejects** the row. |
| 5 | `campaign stage` | PML stage that owns the production contract for this claim | Must name the stage that delivers/owns the production contract (PML1–PML7), so a proof-level `accepted` row never reads as production-ready. |

### Status vocabulary (closed)

- **`accepted`** — the claim is backed by accepted evidence: live source,
  caller-backed proof (U3 ledger), or a frozen contract section. `accepted`
  means *the capability exists and is verified at its proven shape* — it does
  **not** mean production-ready; the `campaign stage` column marks where the
  production contract lands.
- **`partial`** — part of the claim is accepted, part is not; the row names
  exactly what is proven and what is missing.
- **`in flight`** — the claim is claimed by campaign prose or being worked by a
  campaign stage, but is **not** accepted; never reads as support.

### Non-claim marker

- **`none`** — no claim exists. Used only for surfaces explicitly claimed-off
  in this register (model admission). `none` is **not** part of the claim
  vocabulary; `none` rows live in §3 and are never read as support.

### Schema versioning

The row schema is versioned with U5 semantics (mirrors `gradus-support-matrix-
schema v0.1.0` §2, and `pml0-interface-packet v1` §6.2):

- **Patch bump** (`v0.1.x`): clarification or example only.
- **Minor bump** (`v0.x.0`): vocabulary expansion or added field; existing rows
  remain valid.
- **Major bump** (`vX.0.0`): field removal/renaming, status-meaning change, or a
  fail-closed rule change — **every existing row is re-validated** under the
  new schema.

Schema bumps are recorded in this file's version stamp. A row whose recorded
schema version does not match the current major version is not admitted.

**Register invariant.** Register status can **never** be read as product
support. Support is read only from admitted support-matrix rows
(`pml0-support-matrix-schema.md` §2/§3, fail-closed R1–R11), of which PML0
commits **zero**; the first admitted rows land at PML2. This register tracks
claims and their truth; it does not admit support.

## 2. Populated Gradus rows (claim rows)

| claim | status | owner | evidence ref | campaign stage |
| --- | --- | --- | --- | --- |
| Compiler-generated reverse-mode companions are available to training (autograd wrapper) | `accepted` | gradus (training, `gradus:gradient`) | `pml0-module-dag.md` §1/§3 (gradient = training, 2 `functio`: `nil`, `simple_loss`); `pml0-numerical-baseline.md` §Module coverage (gradient 2, 0 proba); CAMPAIGN.md §Ground Truth ("The compiler generates reverse-mode companions", radix AIR) | PML4 |
| Static-shape SGD optimization step exists and is proven (`sgd_step_2x2/_4x4`) | `accepted` | gradus (training, `gradus:optimize`) | `src/optimize.fab` (live, 2 `functio` per `pml0-module-dag.md` §1); `pml0-proof-api-ledger.md` rows 10–11 (disposition: **retire** — no external caller; update math inlined in `train_step_2x2/_4x4`) | PML4 |
| Static-shape MSE loss exists and is caller-backed (`mse_2x2/_4x4/_2x8`) | `accepted` | gradus (training, `gradus:loss`) | `src/loss.fab` (live, 3 `functio`); `pml0-proof-api-ledger.md` rows 7–9 (admit; callers `examples/training/{linear-regression,mlp,bert-tiny-fragment,bert-gradus-probe}/src/train.fab`) | PML4 |
| Static-shape differentiable NN primitives exist and are caller-backed (`linear_2x2/_4x4/_2x8`, `gelu_4x4/_2x8`, `layernorm_2x8`) | `accepted` | gradus (shared, `gradus:nn`) | `src/nn.fab` (live, 6 `functio`); `pml0-proof-api-ledger.md` rows 1–6 (all admit; example callers cited) | PML3 |
| Static-shape training step exists and is caller-backed (`train_step_2x2/_4x4`) | `accepted` | gradus (training, `gradus:train`) | `src/train.fab` (live, 4 `functio`); `pml0-proof-api-ledger.md` rows 16–17 (admit; callers linear-regression / mlp) | PML4 |
| Composed production training loop — losses + gradients + optimizer state + schedules + eval mode + checkpoint resume + metrics + deterministic seeds compose publicly and converge reproducibly (PML4 gate) | `partial` | gradus (training) | Proven part: `src/{gradient,loss,optimize,train}.fab` (rows above); missing part: no checkpoint-state, schedule, eval-mode, or reproducible-convergence contract exists today (`pml0-module-dag.md` §3 — `data` stub, 0 `functio`; `pml0-numerical-baseline.md` — 0/21 `.proba`) | PML4 |
| Reusable forward attention over the shared layer (general attention contract) | `in flight` | gradus (shared, `gradus:attention`) | Fixed-shape slice exists and is caller-backed: `src/attention.fab` (`scaled_dot_product_2x8`), `pml0-proof-api-ledger.md` row 12 (admit); **not accepted**: general attention contract unclaimed — README drift D1 (`pml0-numerical-baseline.md` §D1: README "Planned" vs shipped static-shape slice), production contract PML3 | PML3 |
| Reusable transformer blocks over the shared layer (`bert_tiny_block_2x8` as the shipped static-shape slice) | `in flight` | gradus (shared, `gradus:transformer`) | `src/transformer.fab` (live, 3 `functio`); `pml0-proof-api-ledger.md` rows 13–15 (`bert_tiny_block_2x8` admit; `attention_block_2x8`/`ffn_block_2x8` retire — math inlined); **not accepted**: production transformer contract PML3, general surface unclaimed (README drift D1) | PML3 |

## 3. Non-claim rows — explicitly no claim (never read as support)

These rows record surfaces that are **claimed-off** in this register: no
admission claim exists, so the register can never be read as saying Gradus
admits these formats. `none` is the non-claim marker, not a claim status.

| claim | status | owner | evidence ref | campaign stage |
| --- | --- | --- | --- | --- |
| GGUF model admission (Gradus admits a GGUF model row) | `none` | gradus (model admission; parsing today in `norma:model`) | `pml0-support-matrix-schema.md` §2/§3 (schema only, **zero** populated product rows; R1–R11 fail-closed); `pml0-norma-model-decision.md` (migrate into Gradus at PML2, not now; no dual authority); `pml0-model-capsule-contract.md` (capsule is the typed handoff; raw bytes not a trust anchor) | PML2 |
| Safetensors model admission (Gradus admits a Safetensors model row) | `none` | gradus (model admission; parsing today in `norma:model`) | `pml0-support-matrix-schema.md` §2/§3 (zero populated rows; fail-closed); `pml0-norma-model-decision.md` (migrate at PML2, not now); `pml0-model-capsule-contract.md` | PML2 |

## 4. Cross-campaign scope note

- This register is **cross-campaign**: rows are added as each owning campaign
  lowers, never by reusing another campaign's row.
- **NGAB0 / Faber** owns the composite-executable surface rows in the sibling
  register (`faber/docs/factory/native-gpu-application-bundle/ngab0-claim-
  register.md`) — Faber assembly, hosts effects/sessions, radix compiler facts.
  **PML0 / Gradus** adds rows for the ML-semantics surface (this file, paired
  with `pml0-gradus-contract.md` at U10). **NGAB1+** and the **separate
  inference-product repo** add rows as their units land (serving/HTTP,
  scheduling, batching, deployment). Rows citing evidence in sibling repos use
  that repo's relative path.
- **No row claims a capability without evidence.** A row is admitted only when
  its evidence ref points at a committed artifact (frozen contract section,
  snapshot, live source, or receipt) that supports the claim. Contract prose is
  evidence only when the referenced contract section is frozen.
- The register pairs with the interface packet (U9): this register's claims
  track the same surfaces the packet version-stamps, and both are revisable
  through PML1/NGAB1 — a packet revision can move a row's status, never a
  row's evidence without a re-check.

## 5. Maintenance rules

- Editing is **additive**. A row's status moves as its owning unit lands; a
  claim that is superseded is **archived, never silently rewritten**.
- A row may move `in flight` → `accepted` only on the evidence named in its
  row (or fresh committed evidence recorded in a later revision). Moving to
  `partial`/`accepted` is a revisioned change to this register, not an in-place
  edit.
- New rows reuse the U5 vocabulary (`format`/`architecture`/`dtype`/
  `quantization`/`tokenizer identity`) so a claim can never widen into a
  support claim; a claim that implies a support-matrix row without the
  corresponding admitted row is rejected (mirrors U5 R10).
- The register is regenerated by the factory README generator path like every
  factory doc: status line maintained, README never hand-edited.

## Validation

```bash
cd /Users/ianzepp/work/faberlang/gradus
# 1. Schema section + closed status vocabulary present.
grep -c '`accepted` / `partial` / `in flight`' docs/factory/production-ml-library/pml0-claim-register.md   # >= 1
# 2. At least 6 populated Gradus claim rows, each with a status from the
#    closed vocabulary (statuses appear as `status` in the §2 table column).
grep -c '^| .*`accepted`' docs/factory/production-ml-library/pml0-claim-register.md          # 5
grep -c '^| .*`partial`' docs/factory/production-ml-library/pml0-claim-register.md           # 1
grep -c '^| .*`in flight`' docs/factory/production-ml-library/pml0-claim-register.md         # 2
grep -c '^| .*`none`' docs/factory/production-ml-library/pml0-claim-register.md              # 2 (non-claim rows, §3)
# Claim rows total >= 6 (5 + 1 + 2 == 8).
git diff --check
```

Outcome: schema section present with the closed status vocabulary; 8 populated
Gradus claim rows (5 `accepted`, 1 `partial`, 2 `in flight`) each with a status
from the closed vocabulary, plus 2 non-claim rows (`none`, §3) for the
claimed-off GGUF/Safetensors admission surfaces — so register status can never
read as product support; `git diff --check` clean.
