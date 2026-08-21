# Delivery: PML6 — Production quality, performance, and release contract

**Goal**: `docs/factory/production-ml-library/CAMPAIGN.md` (PML6 gate, lines 311–319)
**Status**: delivered (structural tier) 2026-08-11 — SG1/SG2/SG3 MET; phase gate MET at structural tier; U1–U5 tips 1f4f0d2 / 649b2f6 / 43d75ce / 5a5f295 / 9a2ed8b (main 0fbc97c); closeout `pml6-closeout.md`; CTO8-1 named pre-release item does NOT gate PML6; no version bump
**Repo**: gradus (`docs/`, `README.md`, `AGENTS.md` doc refs, `faber.toml` / `cista.toml` metadata, `scripta/inventory-public-symbols`, benchmark/regression docs)
**Predecessors**: accepted PML1–PML5 contracts, deliveries, and closeouts; PML0 support-matrix baseline (`pml0-support-matrix.md`, PML0-U5) and claim register (`pml0-claim-register.md`, PML0-U12); the landed gradus correctness wave (this session: `3c295c0`, `6cc0eb5`, `2cdc498`, `0d50d60`)
**Supersedes**: the 2026-08-08 `pml6-delivery.md` draft (predates PML4/PML5 landing and the correctness wave — re-lowered at gate MET)

## Phase Intent

API reference, examples, diagnostics, support matrix, compatibility policy,
benchmark method, tolerances, regression corpus, package metadata, and release
checklist **agree with live behavior** (zombie-doc discipline). No performance
claim precedes the correctness gates. This phase makes Gradus a
product-ready dependency for the capstones (PML7) and for NGAB6's portability
feed — without implementing any new ML semantics.

**Entry gate (MET, recorded 2026-08-09)**: may begin after PML1; closes after
PML4 and PML5. PML4 (`pml4-closeout.md`) and PML5 (`pml5-closeout.md`) are both
delivered at the structural tier. PML5's executed-oracle clause (CTO8-1) is a
**NAMED OPEN clause** on the FMIR lever — **PML6's own gate does NOT depend on
the executed tier**. The boundary is recorded here: PML6's release checklist
(U5) carries the executed-gate as a **named pre-release item**, never as a
PML6 gate clause.

**Non-goals**: new semantics (PML1–5 own); release execution (the faber
product release protocol owns bumps, tags, and CI); capstones (PML7); GPU /
executed performance evidence (NGAB + the auditor-owned runtime-evidence gate);
server / HTTP / batching / scheduling (product repo).

## Interpreted Scope

PML6 is the **quality and release contract** for the surface PML1–PML5 built.
It takes the accepted contracts and receipts and makes them **agree with live
behavior** as committed, versioned, machine-checkable artifacts. The ten gate
items are documentation, policy, and contract work only — no `.fab` product
semantics change (diagnostic-string edits and exempla READMEs excepted). The
campaign line 213 ("Quality and releases | Source/compile checks only → PML6
establish support and release gates") is the phase's mandate; the ordering
graph line 193 (PML6 → NGAB6 portability) is its first consumer.

## Normalized Spec (locked decisions)

| # | Decision | Lock |
| --- | --- | --- |
| 1 | **Ten gate items map 1:1 to five units** | U1 = API reference; U2 = examples + diagnostics; U3 = support matrix + compatibility policy; U4 = benchmark method + tolerances + regression corpus; U5 = package metadata + release checklist. Batch-by-default (campaign PML6–PML7 posture). |
| 2 | **API reference is versioned and re-baselined** | `docs/api-reference.md` (`gradus-api-reference v1.0.0`) documents every public symbol on the live post-PML1–5 + correctness-wave surface; a committed coverage/link check proves no undocumented public symbol (zombie-doc gate). |
| 3 | **Diagnostics carry stable identity** | `docs/diagnostics.md` maps every public error to a stable code + message + resolution; messages are locale-ready per workspace convention; diagnostic strings in `src/` are the only `.fab` write allowed. |
| 4 | **Support matrix = one full-matrix aggregation** | `pml0-support-matrix.md` aggregates every admitted row (PML2 format rows, PML3 architecture rows, PML4 training rows, PML5 inference rows) under `gradus-support-matrix-schema v0.1.0` (schema bump only per its own version rules); reject log extended; claim register consistent (C5). |
| 5 | **Compatibility policy is versioned** | `docs/compatibility-policy.md` (`compatibility-policy v1.0.0`): pre-1.0 clean-break posture; proof-shape helper retirement notes; the `_le4/_le8` → `_be4_lege/_be8_lege` rename is a private-helper fix (no external migration); EOG-set identity rule (a different EOG set is a different tokenizer); one-row narrowing stays extensible (R3). |
| 6 | **Benchmark method is committed, CPU-reference-level** | `docs/benchmark-method.md`: exact commands, warmups, sample counts, hardware disclosure; speed claims stay CPU-reference-level (GPU evidence is NGAB's); correctness gates precede any speed number; consumes `gpu-workload-floor` honest-capability floors without duplicating them. |
| 7 | **Tolerances are versioned** | `docs/numeric-tolerances.md` aggregates the cross-repo `numeric-policy v1.0.0` (`gpu-training-lowering/numeric-policy.md` §5.1 — gradient row 1e-4/1e-4, loss row), the 5e-4 absolute `approximata` forward tolerance, the 1e-4 absolute f32 self-host tolerance, exact token pins + the first-token-divergence rule. |
| 8 | **Regression corpus is the proba surface + fixtures** | `docs/regression-corpus.md` inventories the admitted rows' fixtures and proba pins (including the EOG-stop `[0]` pin and reset/replay determinism); structurally green at every unit boundary (fire-9 norm); executed runs are auditor-owned at the FMIR-lever gate (CTO8-1/CTO8-3). |
| 9 | **Package metadata agrees with live behavior** | `faber.toml` + `cista.toml` (name `gradus`, version 0.1.0, provider `gradus`, target `fmir`, interfaces `src`) are re-verified against live behavior; no version bump in this phase. |
| 10 | **Release checklist is a committed artifact** | `docs/release-checklist.md` is consumed by PML7-U3 and the faber release protocol; it records the CTO8-1 executed-oracle clause as a **named pre-release item** without gating PML6. |
| 11 | **Batch norm (fire-9) is structural** | Gradus is faber-language; its consumers are the library provider surface (`faber check` on the repo root compiles `src/*.fab` + co-located `.proba`), the four exempla consumers (`gradient-seam`, `gradient-seam-nolib`, `training-loop-mlp`, `token-generation`), and the admission-conformance test (`tests/admission_conformance.fab`). Each unit boundary keeps `check-source` + `check-compile` green and the touched proba pins consistent — or flags honestly. The train/optimize proba suites execute 90/90 on FMIR (radix `43c0102ba`); other executed proba/e2e claims remain claim-specific and must name their actual boundary rather than treating execution as tree-wide env-blocked. |

## Repo-Aware Baseline

Authority order (campaign, `pml0-delivery.md`): live Gradus source + tests →
accepted Gradus contracts → accepted compiler/package contracts → campaign
stage receipts → examples and historical plans.

### Zombie-doc findings (live drift, PML6-U1 targets)

| # | Finding | Evidence | Disposition |
| --- | --- | --- | --- |
| Z1 | `README.md` status tables are stale | Still reads "Scaffold" foundation, S4-A static-shape surface, "Planned" attention/transformer, "Who this is NOT yet for — no checkpointing, no safetensors, no model distribution" — all superseded by PML2 (model admission), PML4 (checkpoint `Tabula`, losses, optimizer state), PML5 (decode/KV/sampling/generation) | U1 re-baselines README status + "who this is for/not for" to the live surface |
| Z2 | `AGENTS.md:40–41` links `docs/module-map.md` + `docs/api-shape-policy.md`, which do not exist | `ls docs/` returns only `factory/`; recorded as PML0 baseline drift D3 | U1 lands both docs (thin module-map entrypoint over `pml0-module-dag.md` + the PML1 API-shape decision) and fixes the AGENTS.md links |
| Z3 | `scripta/inventory-public-symbols` + `pml0-symbol-inventory.md` assert stale per-module baselines | The script asserts loss 3 / optimize 0 / train 4 / transformer 1 + tracked total 133, all superseded by PML3–5 (loss gained `cross_entropy`, optimize gained SGD state, train gained schedules/mode, decode/cache/sampling/generation/metrics/tokenizer modules landed) | U1 re-baselines the script's expected counts + the inventory doc + the tracked total to the live surface |
| Z4 | `exempla/gradient-seam/` and `exempla/gradient-seam-nolib/` have no README; the seam note in `README.md` is stale | `find exempla -maxdepth 2` shows no README for the two seam consumers; README's seam caveat references a stale binary claim | U2 adds/reconciles exempla READMEs against the live compile gate |

### Landed-semantics reconciliation (correctness wave, must be reflected 1:1)

| Commit | Landed semantics | Where PML6 must reflect it |
| --- | --- | --- |
| `3c295c0` | Serialize big-endian readers renamed `_le4/_le8` → `_be4_lege/_be8_lege` (misleading little-endian names for big-endian readers; `src/serialize.fab`) | **U1** symbol inventory + API reference list the renamed helpers; **U3** compatibility-policy note: private-helper correctness rename, no external migration |
| `6cc0eb5` | Tokenizer admission polarity restored: the pinned add-* flags are `falsum`; `bos_vacua` / `spatium_vacua` are the positive facts (guard `≡`, was `≠`; `src/tokenizer.fab`) | **U1** API reference documents admission facts (BOS-free / space-prefix-free positive); **U2** diagnostics; **U3** tokenizer-identity rows |
| `2cdc498` | Capsule admission enforces the **exact pinned EOG set `{0,2}`** — a well-formed-but-different set is a different tokenizer (contract §3.3; `src/model/capsule.fab` `EOG ← "0,2"`, `_tokenizator_recta`) + `capsule.proba` rejection pin + stale `_le4/_le8` doc refs fixed | **U1** API reference (EOG is tokenizer identity); **U2** diagnostics (`EogMala`); **U3** tokenizer-identity rows; **U4** regression corpus (rejection pin) |
| `0d50d60` | EOG-stop generation: generation terminates after the **first admitted EOG token** `{0,2}`; `tokenizator.est_eog` is the stop-policy binding; greedy oracle emits `[0]` not `[0,0]`; `maxima_verborum` is a ceiling, never a promise; every EOG-affected pin/comment/doc reconciled (decode.proba, exemplum, README, CAMPAIGN, pml5-closeout) | **U1** API reference documents `tokenizator.est_eog` + generation-loop EOG-stop semantics; **U2** examples document the pinned `[0]` / `[1, 1]` outputs + per-step boundaries; **U4** regression corpus carries the token pins + first-token-divergence rule + reset/replay determinism |

**Executed-tier boundary (claim-specific)**: the train/optimize proba suites
execute 90/90 on FMIR (radix `43c0102ba`). This document makes no blanket
claim for other proba or exempla e2e runs; remaining environment-bound claims
name their actual boundary (for example, the `generation::default` provider
gap). PML6's quality/release contract is structural-tier: every artifact
agrees with the compiled surface and the pinned oracle values. Executed
value-identity is the auditor-owned runtime-evidence gate; the release
checklist names it as a pre-release item.

## Stage Graph

```text
Wave 1:  U1  (API reference + inventory/README re-baseline — pattern-establishing)
Wave 2:  U2 ∥ U3   (disjoint write scopes; both consume U1)
Wave 3:  U4 ∥ U5   (disjoint write scopes; U4 consumes U3, U5 consumes U1+U3)

U1 ──> U2 ──> (phase gate)
U1 ──> U3 ──> U4 ──> (phase gate)
U1 ──> U3 ──> U5 ──> (phase gate)
```

No two units share a write path. Cross-campaign: runs beside NGAB5–NGAB7 and
the GI/MD/training lanes (disjoint repos); the claim register vocabulary is
shared with NGAB's register (one vocabulary, two repo files — additive edits
only, per `pml0-claim-register.md` §5).

## Implementation Work

### PML6-U1 — API reference (re-baseline + zombie-doc gate)

| Field | Value |
| --- | --- |
| **id** | PML6-U1 |
| **outcome** | Every public `gradus:*` symbol on the live post-PML1–5 + correctness-wave surface is documented (signatures, error types, examples) in a versioned API reference; the symbol inventory (script + doc) and README/AGENTS doc refs agree with live behavior. |
| **write_scope** | `gradus/docs/api-reference.md` (new), `gradus/docs/module-map.md` (new, thin entrypoint), `gradus/docs/api-shape-policy.md` (new, PML1 API-shape decision), `README.md`, `AGENTS.md` (doc-ref lines Z2 only), `scripta/inventory-public-symbols`, `docs/factory/production-ml-library/pml0-symbol-inventory.md` |
| **read_scope** | Live `src/**/*.fab` (read-only symbol extraction), `pml0-symbol-inventory.md`, `scripta/inventory-public-symbols`, `pml0-module-dag.md`, `pml0-numerical-baseline.md` (D3), the correctness-wave commits (`3c295c0`, `6cc0eb5`, `2cdc498`, `0d50d60`) and PML4/PML5 delivery + closeout docs |
| **done_when** | `docs/api-reference.md` (`gradus-api-reference v1.0.0`) documents every public symbol from the re-baselined inventory, including `tokenizator.est_eog`, the `_be4_lege`/`_be8_lege` serialize helpers, and the EOG-set admission semantics; `scripta/inventory-public-symbols` + `pml0-symbol-inventory.md` re-baselined and green; README status tables + "who this is for/not for" agree with live behavior; Z2/Z3 closed (AGENTS.md links resolve; `docs/module-map.md` + `docs/api-shape-policy.md` land); a committed coverage/link check proves no undocumented public symbol. |
| **validation** | `./scripta/inventory-public-symbols` (exit 0 on re-baselined counts); zombie-doc greps (no shipped surface labeled planned/scaffold and vice versa); `./scripta/check-source && ./scripta/check-compile` green (batch norm — this unit touches no `.fab`, so the gate is the no-regression proof) |
| **depends_on** | PML1–PML5 accepted surfaces; correctness wave; PML0-U2 (`pml0-symbol-inventory.md`), PML0-U4 (`pml0-module-dag.md`) |
| **non_goals** | No semantics change; no diagnostic-code writing (U2); no support-matrix rows (U3) |
| **risk** | The reference drifts again (zombie-doc) — mitigated by the committed coverage check; inventory re-baseline is mechanical but must match the live grep exactly |
| **est_work_tokens** | 12k–24k. **tool_latency**: low. |
| **test_owner** | Hand (inventory script + zombie-doc greps); auditor verifies the coverage gate at phase audit |

### PML6-U2 — Diagnostics + examples

| Field | Value |
| --- | --- |
| **id** | PML6-U2 |
| **outcome** | Every public error has a stable code + message identity with a documented resolution; every exemplum has a README whose documented output matches the pinned oracle values; exempla compile green at the structural tier. |
| **write_scope** | `gradus/docs/diagnostics.md` (new), `gradus/exempla/*/README.md` (create for `gradient-seam`, `gradient-seam-nolib`; reconcile `training-loop-mlp` + `token-generation`), `src/**/*.fab` diagnostic strings only (`causa` messages — no semantics), `README.md` seam note (Z4) |
| **read_scope** | `docs/api-reference.md` (U1), `src/**/*.fab` error `causa` strings, exemplum sources, `src/decode.proba` PML5-U6 pins, `exempla/token-generation/README.md` (the pinned `[0]` / `[1, 1]` outputs + per-step boundaries) |
| **done_when** | `docs/diagnostics.md` maps every public error to code + message + resolution (including `EogMala` — EOG-set mismatch is identity, not a value error); exempla READMEs document inputs, pinned outputs, and the structural/executed tier honestly (the token-generation README already pins `[0]` / `[1, 1]` + the first-token-divergence rule); no executed claim appears in any exemplum README unless the FMIR lever has opened |
| **validation** | `./scripta/check-source && ./scripta/check-compile` green (all four exempla consumers compile — the fire-9 consumer enumeration); grep: every diagnostic code in `docs/diagnostics.md` resolves to a live error; exempla README outputs match the proba pins |
| **depends_on** | U1 (the API reference's error taxonomy + documented semantics) |
| **non_goals** | No new error types; no executed exemplum runs (auditor-owned at the FMIR-lever gate); no README regen (closeout-owned) |
| **risk** | A diagnostic message drifts from the live `causa` string — mitigated by the resolve-grep; executed runs claimed by mistake — the READMEs state the structural/executed tier per CTO Q2 |
| **est_work_tokens** | 8k–16k. **tool_latency**: low. |
| **test_owner** | Hand (diagnostic mapping + exempla compile); auditor owns executed exemplum runs at the FMIR-lever gate (CTO8-1) |

### PML6-U3 — Support matrix + compatibility policy

| Field | Value |
| --- | --- |
| **id** | PML6-U3 |
| **outcome** | `pml0-support-matrix.md` is the full-matrix aggregation of every admitted row (formats, architectures, dtypes, quantizations, shapes, tokenizers, backends) + reject log; `docs/compatibility-policy.md` (`compatibility-policy v1.0.0`) names what breaks, what migrates, and the identity rules; the claim register is consistent (no row reads as product support without evidence — C5). |
| **write_scope** | `gradus/docs/factory/production-ml-library/pml0-support-matrix.md`, `gradus/docs/factory/production-ml-library/pml0-claim-register.md` (additive row moves only, §5), `gradus/docs/compatibility-policy.md` (new) |
| **read_scope** | U1 (`docs/api-reference.md`), PML0-U5 (`pml0-support-matrix-schema.md`), PML0-U12 (`pml0-claim-register.md`), PML2 row-oracle docs (`fixtures/gguf/gguf-row-oracle.md`, `fixtures/safetensors/safetensors-row-oracle.md`, `fixtures/tokenizer/tokenizer-identity-oracle.md`), PML3/4/5 closeouts (rows + residuals: PML3 #1, PML4 #3, PML5 #4), the correctness wave, the NGAB0 claim register (shared vocabulary) |
| **done_when** | The matrix aggregates every admitted row — PML2 format rows (Safetensors + GGUF, cited from their row-oracle docs), PML3 architecture rows (BERT-tiny training row + SmolLM2-360M scaled inference row), PML4 training-layer row(s) (loss/gradient/optimizer/train/checkpoint/metrics compose, structural tier), PML5 inference row(s) (decode/KV-cache/sampling/generation-config with EOG-stop semantics) — each with all schema fields + committed evidence links; the reject log records the R3/R4/R5/R9/R10/R11 rejections (including: no executed-identity rows — the structural tier is marked, never upgraded); `docs/compatibility-policy.md` covers pre-1.0 clean-break, proof-shape retirement notes, the private-helper rename note, the EOG-set identity rule, and one-row-narrowing extensibility (R3); claim register consistent — every row cites committed evidence and reads as claim, never support |
| **validation** | Support-matrix row-count + evidence-link greps (per the matrix's validation section, extended for the new rows); claim-register status-vocabulary greps (PML0-U12); `./scripta/check-source && ./scripta/check-compile` green (batch norm — no `.fab` change expected; a diagnostic-string or helper-touch is a flag) |
| **depends_on** | U1; PML0-U5/U12; PML2–PML5 admitted rows + closeouts |
| **non_goals** | No new admitted rows beyond what PML2–PML5 proved; no executed identity upgrade (auditor gate); no README regen (closeout-owned) |
| **risk** | Aggregation double-claims a row without committed evidence — R10/R11 discipline + C5; EOG-set rows written inconsistently with `2cdc498` — the matrix cites the pinned `{0,2}` exactly |
| **est_work_tokens** | 10k–20k. **tool_latency**: low. |
| **test_owner** | Hand (aggregation + policy); auditor verifies evidence links resolve and the register never reads as support (C5) |

### PML6-U4 — Benchmark method + tolerances + regression corpus

| Field | Value |
| --- | --- |
| **id** | PML6-U4 |
| **outcome** | A versioned benchmark method (exact commands, warmups, sample counts, hardware disclosure), a versioned tolerance policy, and a named regression corpus that runs green at the structural tier — with correctness gates ahead of any speed claim. |
| **write_scope** | `gradus/docs/benchmark-method.md` (new), `gradus/docs/numeric-tolerances.md` (new), `gradus/docs/regression-corpus.md` (new) |
| **read_scope** | U3 (`pml0-support-matrix.md`, `docs/compatibility-policy.md`), PML4-U6/PML5-U6 proofs + pins (`src/train.proba`, `src/decode.proba` PML5-U6), cross-repo `numeric-policy v1.0.0` (`gpu-training-lowering/numeric-policy.md` §5.1), GI0–GI3 oracle contracts, `pml0-numerical-baseline.md`, the correctness wave |
| **done_when** | `docs/benchmark-method.md` names the exact commands, warmups, sample counts, hardware disclosure, and the CPU-reference-level claim rule (GPU evidence is NGAB's; correctness gates precede any speed number; `gpu-workload-floor` floors consumed, not duplicated); `docs/numeric-tolerances.md` aggregates numeric-policy v1.0.0 rows, the 5e-4 absolute `approximata` forward tolerance, the 1e-4 absolute f32 self-host tolerance, and the exact token-pin + first-token-divergence rule; `docs/regression-corpus.md` inventories the admitted rows' fixtures + proba pins (including the EOG-stop `[0]` pin, the seeded `[1, 1]` pin, the capsule EOG-rejection pin, and reset/replay determinism) and the corpus is structurally green |
| **validation** | `./scripta/check-source && ./scripta/check-compile` green (batch norm — corpus = proba surface + fixtures); pin-consistency greps (regression-corpus doc vs `src/*.proba` pins); one executed regression/benchmark pass at the closeout / FMIR-lever gate — **auditor-owned, not a dev-loop run** |
| **depends_on** | U3 (tolerance rows referenced by matrix rows); PML4-U6/PML5-U6 proofs |
| **non_goals** | No benchmark binary or committed bench harness in this phase (method + auditor-owned execution); no GPU/executed performance claims; no new proba pins beyond what PML1–5 + the correctness wave pinned |
| **risk** | A speed claim precedes correctness — fails closed; tolerances stated inconsistently with the cross-repo numeric-policy — the doc pins the policy revision; the regression corpus silently misses a pinned row — the inventory is checkable by grep |
| **est_work_tokens** | 10k–20k. **tool_latency**: medium (bounded runs, auditor-owned at closeout). |
| **test_owner** | Hand (method + tolerance + corpus inventory, structural green); auditor owns executed regression + benchmark runs (CTO8-1/CTO8-3 trigger) |

### PML6-U5 — Package metadata + release checklist

| Field | Value |
| --- | --- |
| **id** | PML6-U5 |
| **outcome** | Package metadata agrees with live behavior, and the release checklist is a committed artifact that PML7's closeout and the faber release protocol consume — including the executed-gate as a named pre-release item. |
| **write_scope** | `gradus/faber.toml` + `gradus/cista.toml` metadata lines (only if they drift from live behavior), `gradus/docs/release-checklist.md` (new) |
| **read_scope** | U1 (`docs/api-reference.md`), U3 (`pml0-support-matrix.md`, `docs/compatibility-policy.md`, `pml0-claim-register.md`), `faber.toml` + `cista.toml`, faber release protocol (`faber/AGENTS.md`), PML0-U13 receipt schema, PML7 delivery (`pml7-delivery.md` U3), CTO8-1/CTO8-3 records |
| **done_when** | `faber.toml` (name `gradus`, version 0.1.0, provider `gradus`, target `fmir`) + `cista.toml` (source package, `interfaces = "src"`) re-verified against live behavior — no drift, or the drift is corrected with a recorded note; `docs/release-checklist.md` names the release items (docs fresh, support matrix + claim register final pass, PML0-U13 receipts, clean-install, version policy), consumed by PML7-U3 and the faber release protocol, and records the CTO8-1 executed-oracle gate as a **named pre-release item** (open until the FMIR lever lands; does NOT gate PML6) |
| **validation** | Metadata diff vs live behavior (faber.toml/cista.toml parse + agree with `faber check` and cista source layout); release-checklist item greps (each item resolves to a committed artifact); `./scripta/check-source && ./scripta/check-compile` green (batch norm) |
| **depends_on** | U1, U3 |
| **non_goals** | No version bump, tag, push, or release execution (faber product release protocol owns); no clean-install receipts (PML7-U3); no README regen (closeout-owned) |
| **risk** | The checklist names an item with no committed evidence — each item must resolve; the executed-gate accidentally read as a PML6 gate — the doc states the boundary explicitly |
| **est_work_tokens** | 6k–12k. **tool_latency**: low. |
| **test_owner** | Hand (metadata + checklist); release execution and clean-install are PML7/faber-release owned |

## Checkpoints And Gates

- **SG1 (after U1)**: `docs/api-reference.md` + inventory re-baseline + README/AGENTS fixes land; zombie-doc greps pass; `check-source` + `check-compile` green; inventory script exit 0.
- **SG2 (after U2 + U3)**: diagnostics map + exempla READMEs land and compile; support matrix is the full aggregation + claim register consistent + compatibility policy committed; `check-source` + `check-compile` green; touched proba pins consistent.
- **SG3 (after U4 + U5)**: benchmark method + tolerances + regression corpus committed; package metadata agrees; release checklist committed with the named executed item; `check-source` + `check-compile` green.
- **Phase gate (closeout)**: all ten gate items are committed and **agree with live behavior** (zombie-doc discipline); support matrix + compatibility policy committed; claim register consistent; README regen + audit 0 findings; regression corpus green once (structural); no executed claim beyond the structural tier (the executed-gate is a named pre-release item, CTO8-1); no performance claim precedes correctness.

**Batching / Split Decision**: one batch of five units in three waves
(batch-by-default, campaign PML6–PML7 posture). Named split boundaries only:
U1 may split per module if the reference batch overflows a Hand's practical
unit (Mind-routed at the SG1 boundary); U4's executed regression/benchmark runs
are auditor-owned, never a dev-loop split.

**Release checkpoint**: **release-prep** — PML6 establishes the release
contract but does not bump, tag, or execute (pre-1.0 clean-break posture; the
faber product is the release surface per `faber/AGENTS.md`). Evidence for the
call: campaign "release/version review occurs at PML6 and PML7"; the faber
release protocol owns version bumps; PML7-U3 + the faber release protocol
consume this phase's checklist.

## Validation

```bash
cd gradus && ./scripta/check-source && ./scripta/check-compile
cd gradus && ./scripta/inventory-public-symbols
cd gradus && python3 ../radix/scripta/generate-factory-readme.py --factory-root docs/factory --check
cd gradus && ./scripta/check-factory-goal-status --fail-on error
git diff --check
```

Unit-level: zombie-doc greps (U1); diagnostic resolve-grep + exempla compile
(U2); support-matrix row/evidence-link greps + claim-register vocabulary
(U3); pin-consistency greps (U4); metadata diff + checklist-item greps (U5).
Regression corpus + benchmark runs: **one** pass at closeout / the FMIR-lever
gate — auditor-owned (Cargo discipline: no dev-loop suites).

## Council Dispositions (applicable)

| Item | Mandate | Where |
| --- | --- | --- |
| C5 | Claim register: no row reads as product support without evidence | U3 updates the register; claim vocabulary stays closed |
| C7 | Joint cross-repo receipts + scoped audit | U5 checklist consumes the PML0-U13 receipt schema; the gradus audit entrypoint is the gate |
| C8 | Admitted-model capsule as the typed handoff (raw bytes not a trust anchor) | U3 matrix rows + compatibility policy cite the capsule; diagnostics document `EogMala`/admission failures |
| R3 | One-row narrowing must not hard-code into public API shape | U3 compatibility policy keeps admission + capability descriptors extensible (support rows, not hard-coded generics) |
| R5 | NGAB6 semantic vs binary identity stays distinct | U4/U5 portability feed: the benchmark method + release checklist record identity classes (structural tier = semantic identity; executed = separate claim) |

## Escalation Path

| Situation | Action |
| --- | --- |
| Any unit finds the API reference / docs disagree with live behavior | Stop at the finding; escalate to Mind with the two-source evidence; do not silently pick (authority order in `pml0-delivery.md`) |
| A public API needs a backend/device handle | Campaign stop condition; route a need to Mind (sibling-campaign route to NGAB) |
| A speed/performance claim precedes the correctness gates | Unit fails closed; no speed number until the correctness gates pass |
| A support-matrix row cannot cite committed evidence | Row rejects (R10/R11); escalate if a PML2–5 row genuinely lacks evidence |
| Executed-tier verification is env-blocked | Honest-flag; never claim; the release checklist records it as a named pre-release item (CTO8-1) |
| Cross-repo doc conflict (e.g. numeric-policy revision) | Escalate to Mind with both revisions; default = the cross-repo policy is read-only input at its pinned revision |

## Open Questions

| # | Question | Default (proceed unless Mind overrides) |
| --- | --- | --- |
| 1 | Doc-version policy for the new artifacts | `gradus-api-reference v1.0.0` + `compatibility-policy v1.0.0`, consistent with the schema-version convention (`dtype-schema-1.0.0` etc.); version bumps recorded per schema rules |
| 2 | Compatibility-policy doc location | `docs/compatibility-policy.md` (product-facing aggregate) + per-row `compatibility policy` fields stay the row-level authority in `pml0-support-matrix.md` |
| 3 | Release checkpoint | **release-prep** — no bump/tag in PML6; faber product release owns versioning; PML7 + faber protocol consume the checklist |
| 4 | U1 batch vs per-module split | One batch; split per module only if the Hand reports the reference overflows a practical unit (Mind-routed at SG1) |
| 5 | U4 benchmark runner | Documented method + auditor-owned execution at the FMIR-lever gate; no committed bench binary this phase (correctness before performance) |
| 6 | Support-matrix schema | Keep `gradus-support-matrix-schema v0.1.0`; a minor bump only if a field is genuinely needed for the training/inference row families (recorded per the schema's version rules) |

## Residuals Routed

| # | Residual | Source | Routed to |
| --- | --- | --- | --- |
| 1 | Support-matrix full aggregation (PML2/3/4/5 rows) | PML3 closeout #1, PML4 closeout #3, PML5 closeout #4 | **U3** |
| 2 | Executed-oracle clause (CTO8-1) + dated re-verification (CTO8-3) | PML5 closeout | **U4** regression corpus + **U5** release checklist (named pre-release item); owner auditor at the FMIR-lever gate |
| 3 | AGENTS.md dangling doc links (Z2 / D3) | `pml0-numerical-baseline.md` D3 | **U1** |
| 4 | Release checklist → PML7 clean-install + receipts | this delivery (U5) | PML7-U3 + faber release protocol |
| 5 | Support matrix + compat policy + benchmark method → NGAB6 portability feed | CAMPAIGN ordering graph (line 193) | NGAB6 (cross-campaign) |
| 6 | Claim-register vocabulary shared with NGAB's register | `pml0-claim-register.md` §4 | additive edits only; one vocabulary, two repo files |
| 7 | Benchmark floors consumed, not duplicated | `gpu-workload-floor` campaign (CAMPAIGN line 175) | U4 references its evidence |
