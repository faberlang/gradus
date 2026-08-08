# Council of Minds Review — 2026-08-08

**Subject**: Production ML Library (PML) and Native GPU Application Bundle (NGAB) pre-delivery strategic review; parallel-lane plan with the in-flight GPU campaigns.
**Mode**: advisory — the council does not implement, lower goals, or verify code. Dispositions are inputs to PML0/NGAB0 lowering and to Mind routing.
**Council**: head-ceo (`sequencing`), head-cpo (`soft_gate`), head-cmo (`sequencing`), head-cso (`hard_gate`), head-cto (`false_gate`), head-cxo (`sequencing`).
**Reviewed artifacts**: `gradus/docs/factory/production-ml-library/CAMPAIGN.md`, `faber/docs/factory/native-gpu-application-bundle/CAMPAIGN.md`, `radix/docs/factory/gpu-inference-gguf/CAMPAIGN.md`, `radix/docs/factory/gpu-inference-multi-device/CAMPAIGN.md`, `radix/docs/factory/gpu-training-lowering/CAMPAIGN.md` (status).

## Verdict summary

The two-campaign split (device-neutral ML semantics in Gradus; one native executable with embedded kernels in Faber/Radix/hosts; serving in a separate product repo) is architecturally sound. **Six of six heads proceed on the ownership boundaries and on PML0↔NGAB0 as the first cross-campaign freeze.** The review is a `sequencing`/`soft_gate` family verdict: the design is right, but **eight corrections must land at or with PML0–NGAB0** before either campaign generalizes its public boundary, and several risks must be recorded and rechecked.

## Correct-before-next-phase items (C1–C8)

| # | Item | Present commitment | Future pressure | Affected boundary | Disposition source |
| --- | --- | --- | --- | --- | --- |
| C1 | **GI4+ ownership amendment is a hard prerequisite, not a PML0 side-output.** Commit the amendment + migration map in `radix/docs/factory/gpu-inference-gguf/` before GI4 builds persistent decode. Stale clauses assigning model runtime to `faber-runtime` or serving to the old owners must be reconciled. | PML0/NGAB0 require the amendment | Gradus and GI both claim KV/decode | GI ↔ Gradus ↔ NGAB ↔ product | ceo, cpo, cmo, cso, cto, cxo |
| C2 | **MD3I gate amendment.** "Legacy GI4 accepted" is no longer the contract authority once Gradus owns logical decode/KV and NGAB owns composite sessions. Amend `radix/docs/factory/gpu-inference-multi-device/` MD3I entry gate to consume the new contract authority (fold into C1's migration map). | MD3I entry = "MD3 + GI4 accepted" | Multi-device token commit waits on a stale gate | MD ↔ GI ↔ PML5/NGAB4 | cto |
| C3 | **Model-admission migration mechanics named in PML0.** Decide code-move (into Gradus) vs formal retirement of GI1's accepted admission code — "no dual authority" must be enforced by code location, not prose. | PML2 migrates `norma:model` + GI1 admission | Two GGUF admission truths | GI1 ↔ PML2 ↔ norma | cso, cxo |
| C4 | **Shared interface packet: content + version authority + revisability.** Name a version owner + change procedure; label the packet revisable through PML1/NGAB1 (it precedes compiled proof). Contents: semantic identities (model/tokenizer/parameters/generation-config/KV state); compile-time vs load-time vs call-time facts; typed values/layouts/mutation/lifetimes/observations/reset/cancellation/errors; host-device ABI + manifest version relationship; version-bump authority + rejection/migration policy; frozen-now vs reserved seams; no device handle, no HTTP policy. | "Exact interface packet" | ABI/schema drift across parallel lanes | PML0 ↔ NGAB0 | ceo, cto, cso |
| C5 | **Cross-campaign claim/capability register.** One register so "accepted"/"partial"/"in flight" never reads as product support; exact architecture/quantization/backend/limits qualifiers. | Separate capability tables | Release notes and product positioning misread | Campaign index ↔ release surface | cmo, cpo |
| C6 | **Inference-product campaign stub.** Charter-level stub (repo, request API direction, streaming, mapping server options → Gradus generation config) drafted before PML5/NGAB5 convergence; HTTP/serving stays out of both current campaigns. | Product campaign "not yet drafted" | Launch story ends at "a local executable" | NGAB5/PM L5 → product | ceo, cmo, cpo |
| C7 | **Joint cross-repo receipt schema + scoped audit entrypoints.** PML0/NGAB0 must add/select repo-scoped audit entrypoints (shared radix status audit is bookkeeping, not artifact proof) and a content-addressed convergence receipt for PML7/NGAB7. | Component receipts; radix-bound audit | Release convergence unprovable | Release ladder ↔ campaign index | cto |
| C8 | **Security contracts at the freeze.** Admitted-model capsule (validated bytes + cryptographic identity + tokenizer identity + quantization + bounds + architecture facts) as the typed handoff — raw GGUF bytes/paths are not trust anchors. NGAB: canonical embedded-artifact identity + verification order (digest, verify before backend selection, model↔kernel binding, tamper → pre-launch failure). | Bytes/paths cross owners today | Server repo inherits unsafe parsing/loading | Gradus ↔ Faber ↔ hosts ↔ product | cso |

## Recorded risks (R1–R7)

| # | Risk | Trigger | Recheck | Owner |
| --- | --- | --- | --- | --- |
| R1 | PML0↔NGAB0 paper freeze precedes compiled proof — PML1 may invalidate tensor/shape contract | PML1 tensor/dtype/shape contract lands | At PML1/NGAB1 lowering | planner-1/2, Mind |
| R2 | PML5 generation-config surface (min-p, repetition penalty) frozen before any oracle exercises them | PML5 lowering | Only admit config values with a live oracle at PML5 close | Mind |
| R3 | One-row / one-backend / greedy-decode narrowing hard-codes into shared ABI or public API shape | PML2/NGAB1/NGAB5 lowerings | Admission + capability descriptors stay extensible; qualified wording | Mind |
| R4 | KV identity / principal handoff for the future server unspecified (MD-A9/A10 hold) | Product campaign drafting | Before product repo lowers | Mind + head-cso |
| R5 | NGAB6 "same artifact or declared target-triple rebuild" — semantic vs binary identity must stay distinct | NGAB6 lowering | Record identity classes in packet | Mind |
| R6 | Pending GI3-6/7/8 units may touch FMIR/device facts before NGAB1 freezes the partition | Each GI3 sub-stage dispatch | Classify every pending GI/training/MD unit hot-path vs disjoint before dispatch; one named lane per hot-path revision | Mind |
| R7 | NGAB5 tuning surface becomes a second configuration authority; backend/device selection becomes default UX | NGAB5 lowering | NGAB5 = adapter over Gradus generation config; backend/device = operator/diagnostic override | Mind |

## Parallel-lane plan (what can run concurrently)

The council confirms the campaigns' own ordering. Lanes and their real serialization:

```
PML0 <-> NGAB0            parallel; shared interface packet + GI4+/MD3I amendment
  |         |
PML1      NGAB1 -> NGAB2 -> NGAB3      (serial: compiler facts -> packaging -> host loading)
  |                       |
PML2+PML3            NGAB4 generic composite proof
  |         \              |
PML4      PML5 ----------> NGAB5 LLM executable (convergence)
  |            |              |
PML6 ---------+-----------> NGAB6 portability
  \-----------------------> PML7 + NGAB7 closeout

PML5 + NGAB4 -> multi-device continuation (separate lane)
```

- **Runs now, in parallel**: PML0 (gradus), NGAB0 (faber), GI3-6/7/8 (radix, disjoint units only), training Stage 6+ capstone (examples), MD0-style read-only discovery, llvm-host-parity (independent).
- **Hard serialization points (shared hot paths)**: DeviceProgram, FMIR device wire schema, materializer, host construction, package/model admission, public session APIs — one named owner per revision; and the shared docs/factory README + status audit (radix-bound) which all repos' docs touches.
- **Gates that must NOT be treated as implementation-ready**: MD3I (waits C1/C2 contract freeze), NGAB5 (waits PML2/3/5 + NGAB4), GI4+ (waits re-lowering).
- **Discipline**: no cargo build/test in the dev loop (workspace rule); one closeout per unit via declared validation; phase audits at named cutoffs only.

## What the Mind must not get wrong

1. The GI4+ ownership amendment (C1/C2) is a **hard prerequisite committed in GI's own docs** before GI4 builds persistent decode — not a PML0 side-output.
2. PML2 must **move** GI1's model-admission code (or formally retire it) — "no dual authority" is a code-location fact, not prose.
3. The PML0↔NGAB0 interface packet is a **revisable, versioned machine contract**, not a frozen paper promise.

## Disposition

PML0 and NGAB0 proceed to delivery lowering incorporating C1–C8 and recording R1–R7. Mind owns routing the C-items and the R-rechecks. No `reopen_phase` findings.
