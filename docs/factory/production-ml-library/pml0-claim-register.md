# PML0 Claim/Capability Register

**Unit**: PML0-U12 (C5) — cross-campaign claim/capability register skeleton —
see `pml0-delivery.md` PML0-U12.
**Status**: skeleton — first Gradus rows admitted (evidence-backed); PML6-U3
revision (2026-08-11) — §5 row moves as PML2–PML5 landed (training-loop
`partial`→`accepted`; attention/transformer `in flight`→`partial`; the two
PML0 claimed-off admission surfaces promoted to §2; PML5 inference rows added);
further campaigns add rows per the cross-campaign scope note (§4).
**Schema version stamp**: `gradus-claim-register-schema v0.1.0` (2026-08-08) —
unchanged; the PML6-U3 revision applies §5 row moves only (no schema
field/vocabulary change).
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

| claim | claim state | owner | evidence ref | campaign stage |
| --- | --- | --- | --- | --- |
| Compiler-generated reverse-mode companions are available to training (autograd wrapper) | `accepted` | gradus (training, `gradus:gradient`) | `pml0-module-dag.md` §1/§3 (gradient = training, 2 `functio`: `nil`, `simple_loss`); `pml0-numerical-baseline.md` §Module coverage (gradient 2, 0 proba); CAMPAIGN.md §Ground Truth ("The compiler generates reverse-mode companions", radix AIR) | PML4 |
| Static-shape SGD optimization step exists and is proven (`sgd_step_2x2/_4x4`) | `accepted` | gradus (training, `gradus:optimize`) | `src/optimize.fab` (live, 2 `functio` per `pml0-module-dag.md` §1); `pml0-proof-api-ledger.md` rows 10–11 (disposition: **retire** — no external caller; update math inlined in `train_step_2x2/_4x4`) | PML4 |
| Static-shape MSE loss exists and is caller-backed (`mse_2x2/_4x4/_2x8`) | `accepted` | gradus (training, `gradus:loss`) | `src/loss.fab` (live, 3 `functio`); `pml0-proof-api-ledger.md` rows 7–9 (admit; callers `examples/training/{linear-regression,mlp,bert-tiny-fragment,bert-gradus-probe}/src/train.fab`) | PML4 |
| Static-shape differentiable NN primitives exist and are caller-backed (`linear_2x2/_4x4/_2x8`, `gelu_4x4/_2x8`, `layernorm_2x8`) | `accepted` | gradus (shared, `gradus:nn`) | `src/nn.fab` (live, 6 `functio`); `pml0-proof-api-ledger.md` rows 1–6 (all admit; example callers cited) | PML3 |
| Static-shape training step exists and is caller-backed (`train_step_2x2/_4x4`) | `accepted` | gradus (training, `gradus:train`) | `src/train.fab` (live, 4 `functio`); `pml0-proof-api-ledger.md` rows 16–17 (admit; callers linear-regression / mlp) | PML4 |
| Composed production training loop — losses + gradient-call contract + SGD optimizer state + schedules + train/eval mode + checkpoint resume + metrics + deterministic seeds compose publicly and converge reproducibly (PML4 gate, **structural tier**) | `accepted` | gradus (training) | `src/{loss,gradient,optimize,train,metrics}.fab` + co-located probas; `exempla/training-loop-mlp` (accepted 4×4 workload: trajectory pins steps 0/10/25/50/75/99 + ratio gate `0.01137 < 0.1` in `src/train.proba`, resume round-trip, seeded draws); PML4 units 5f98e8b/e09c79c/9bebda9/4b24c81/94d8a94/fc85de7; `pml4-closeout.md` — structural tier; executed convergence deferred to the auditor-owned runtime-evidence gate | PML4 |
| Reusable forward attention over the shared layer (general attention contract) | `partial` | gradus (shared, `gradus:attention`) | Proven: the fixed-shape slice `scaled_dot_product_2x8` (`src/attention.fab`, `pml0-proof-api-ledger.md` row 12 admit) is admitted and used by both admitted architecture rows (`pml0-support-matrix.md` rows 3–4; PML3 closeout — forward composability MET). Missing: a general attention contract beyond the admitted fixed shapes — claimed-off by one-row narrowing (R3), never admitted without per-shape fixture/oracle proof. README drift D1 resolved at PML6-U1 (`1f4f0d2`) | PML3 |
| Reusable transformer blocks over the shared layer (`bert_tiny_block_2x8` as the shipped static-shape slice) | `partial` | gradus (shared, `gradus:transformer`) | Proven: `src/transformer.fab` (live, 3 `functio`); `pml0-proof-api-ledger.md` rows 13–15 (`bert_tiny_block_2x8` admit; `attention_block_2x8`/`ffn_block_2x8` retire — math inlined); the block is shipped, caller-backed, and used by both admitted architecture rows (`transformer_block` modus 2 inference — `pml0-support-matrix.md` rows 3–4; PML3 closeout — forward composability MET). Missing: the general transformer surface beyond the admitted fixed shapes — claimed-off by one-row narrowing (R3). README drift D1 resolved at PML6-U1 (`1f4f0d2`) | PML3 |
| Gradus admits the pinned Safetensors model-file row (`smollm2-360m-scaled-row.safetensors`) into the admitted-model capsule | `accepted` | gradus (model admission, `gradus:model/safetensors`) | `src/model/safetensors.fab` + `.proba`, `src/model/capsule.fab` + `.proba` (capsule-schema-1.0.0); `fixtures/safetensors/safetensors-row-oracle.md` (pinned facts + SHA-256); `tests/admission_conformance.fab`; PML2-U2 `07291d6`; `pml2-closeout.md` | PML2 |
| Gradus admits the pinned GGUF model-file row (`smollm2-360m-scaled-row.gguf`, GGUF file version 3, MOSTLY_Q4_K_M / quant v2) into the admitted-model capsule | `accepted` | gradus (model admission, `gradus:model/gguf`) | `src/model/gguf.fab` + `.proba`, capsule; `fixtures/gguf/gguf-row-oracle.md` (pinned facts + SHA-256); `tests/admission_conformance.fab`; PML2-U3 `b392fc8`; `pml2-closeout.md` | PML2 |
| Tokenizer identity for the admitted row — `gpt2` (BPE) pre-tokenizer `smollm`, vocab 49152 / merges 48900, EOG set `{0,2}`, BOS-free + space-prefix-free — is pinned and fails closed on any divergence (a different EOG set is a different tokenizer) | `accepted` | gradus (model admission, `gradus:tokenizer`) | `src/tokenizer.fab` + `src/tokenizer.proba` (P1–P11 probe pins; workload counts 9/9/202/2175; divergence fail-closed `ProbeDivergens`); `fixtures/tokenizer/tokenizer-identity-oracle.md`; correctness wave `6cc0eb5` / `2cdc498` (EOG exact admission `{0,2}`); PML2-U4 `f12deaf`; `pml2-closeout.md` | PML2 |
| Deterministic decode over the admitted row — one-token decode + prefill over the shared forward functions, EOG-stop generation terminating at the FIRST admitted EOG token `{0,2}` (`maxima_verborum` is a ceiling, never a promise) | `accepted` | gradus (inference, `gradus:decode`) | `src/decode.fab` + `src/decode.proba` (f64 logit pins); `exempla/token-generation` (pinned `[0]` / `[1, 1]`); PML5 units bdefb5a (U1), 8cf798a (U5), 1a6abd0 (U6); `pml5-closeout.md` — structural tier; CTO8-1 executed clause named open | PML5 |
| KV-cache is a typed logical value with sequential per-position append, generation tracking, and reset; cache identity key per MD-A9; no device handle | `accepted` | gradus (inference, `gradus:cache`) | `src/cache.fab` + `src/cache.proba` (exact append/readback pins); PML5-U2 `3b2fc9b`; `pml5-closeout.md` — structural tier | PML5 |
| Deterministic sampling — greedy exact + seeded stochastic (rep-penalty → temperature → top-k → softmax → top-p → min-p), a pure function of logits + config + RNG state | `accepted` | gradus (inference, `gradus:sampling`) | `src/sampling.fab` + `src/sampling.proba` (per-knob pins); PML5-U3 `b1b01f1`; `pml5-closeout.md` — structural tier | PML5 |
| Generation-config contract — nine-field versioned contract (values/defaults/validation) with explicit reject rows for unsupported llama.cpp-style controls; single authority NGAB5 adapts | `accepted` | gradus (inference, `gradus:generation`) | `src/generation.fab` + `src/generation.proba` (reject-row matrix, mapping + wire pins); PML5-U4 `56e70f0`; `pml5-closeout.md` — structural tier | PML5 |

## 3. Non-claim rows — explicitly no claim (never read as support)

The two PML0 claimed-off model-admission surfaces (GGUF, Safetensors — "Gradus
does not admit these formats yet") were **admitted at PML2** into the capsule
(`pml2-closeout.md`; the admitted rows are now §2 rows 9–10, and the tokenizer
identity row is §2 row 11). No `none` rows remain here. The non-claim marker
stays in the vocabulary for surfaces that are genuinely claimed-off in the
future (e.g. a format Gradus does not parse); a `none` row must record why the
claim is claimed-off, so the register can never be read as saying Gradus
admits a surface it does not.

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
# 2. 15 populated Gradus claim rows in §2 (13 `accepted` + 2 `partial`). Raw
#    greps also match §1 schema-table lines that cite the status tokens, so
#    raw counts are 15 accepted / 3 partial (not pure §2 counts).
grep -c '^| .*`accepted`' docs/factory/production-ml-library/pml0-claim-register.md          # 15
grep -c '^| .*`partial`' docs/factory/production-ml-library/pml0-claim-register.md           # 3
# 3. C5 honesty: the executed tier is never claimed (structural-tier notes);
#    no §3 `none` rows remain (the two PML0 claimed-off surfaces are admitted).
grep -c 'structural tier' docs/factory/production-ml-library/pml0-claim-register.md          # >= 6
git diff --check
```

Outcome: schema section present with the closed status vocabulary; 15 populated
Gradus claim rows in §2 (13 `accepted`, 2 `partial`) each with a status from the
closed vocabulary — the training-loop row moved to `accepted` at the structural
tier (PML4 landed), the attention/transformer general-contract claims are
`partial` (fixed-shape slices accepted; the general surface claimed-off by
one-row narrowing), the two PML0 `none` admission surfaces are admitted rows
now (§2), and the PML5 inference rows are recorded as claims with committed
evidence — so register status can never read as product support;
`git diff --check` clean.
