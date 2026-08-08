# PML0 Cross-Campaign Interface Packet v1 — Gradus ↔ NGAB

**Unit**: PML0-U9 of `pml0-delivery.md` (Council mandate C4)
**Packet revision**: `pml0-interface-packet v1` (2026-08-08)
**Revision label**: **revisable through PML1/NGAB1** — this packet precedes compiled proof and is **not** frozen for all phases. It is a versioned machine contract with a named version authority and change procedure (§VersionBump). The §FrozenNow vs §ReservedSeams split states per-surface whether a field is frozen at v1 or reserved as a seam for PML1/NGAB1.
**Pairing**: this packet pairs with the NGAB0 interface packet in a parallel lane (`pml0-delivery.md` §Parallelism And Lane Notes; NGAB0 Dependency Rule 1: the two campaigns exchange one versioned interface packet before either generalizes its public boundary). NGAB0's composite contract exists with §PackageGraph / §OwnershipMatrix / §Partition / §Abi frozen at NGAB0-U2–U3; its remaining sections freeze through NGAB0-U7.
**Exchange partner**: NGAB0's §OwnershipMatrix cites `pml0-gradus-contract.md` (assembly = PML0-U10, in-flight) as the exchange-partner path. This packet is the versioned interface packet that contract references: PML0-U10 names this packet's revision as the interface-packet artifact.
**Read-only facts consumed**: radix `docs/factory/gpu-inference-gguf/gi3-contract.md` (GI3-1/GI3-2 contracts) — read-only, no GI stage reopened. NGAB0's §Abi mirrors GI4 session facts kept as compiler evidence; this packet cites those same facts through the NGAB0 mirror and the GI3 contract directly.
**Snapshot dependency**: PML0-U1 (`pml0-source-snapshot.md`) version stamps; module/ownership facts from PML0-U4 (`pml0-module-dag.md`); row vocabulary from PML0-U5 (`pml0-support-matrix-schema.md`, schema `gradus-support-matrix-schema v0.1.0`); admitted-model capsule from PML0-U14 (`pml0-model-capsule-contract.md`).

## 1. Purpose and scope

This packet fixes what the Gradus ML library campaign (PML0+) and the NGAB composite native-GPU application campaign (NGAB0+) exchange with each other before either generalizes its public boundary. It covers:

- the semantic identities the two campaigns share (model, tokenizer, parameters, generation-config, KV state) — §Identities;
- the fact classes that exist at different validity times — §FactClasses;
- the typed values, layouts, mutation rules, lifetimes, observations, reset, cancellation, and error surface — §TypedValues;
- the host-device ABI and its relationship to manifest and wire versions — §Abi;
- the version-bump authority, rejection, and migration policy — §VersionBump;
- the frozen-now vs reserved-seam field split — §FrozenNowReserved;
- the exclusion clause — §Exclusion.

**Authority order** (campaign, `pml0-delivery.md` §Repo-Aware Baseline): live Gradus source + tests → accepted Gradus contracts → accepted compiler/package contracts → campaign stage receipts → examples and historical plans. This packet is an accepted cross-campaign contract; a live fact that contradicts it wins, and the packet is revised through §VersionBump, never silently edited.

**Non-goals** (campaign non-goals, mirrored in NGAB0): the §Exclusion exclusions apply (no device surface, no HTTP policy anywhere in this packet); no serving; no performance-before-correctness; no model-format code migration (that is PML2).

## 2. Semantic identities

Five semantic identities are shared across the boundary. Each subsection names the identity, how it is established, its owner, and where it is carried. Identity, type, resource, and lifetime facts **survive lowering; they are never reconstructed from emitted LLVM/MSL/PTX text or naming conventions** (NGAB0 Dependency Rule 2, frozen).

### 2.1 Model identity

- **Definition**: model id + whole-file SHA-256 + byte length (NGAB0 §Abi `ModelInstance` fact: "model id + SHA-256 + byte length; load-once at session creation"), plus the architecture-fact set from the support-matrix row vocabulary (U5 fields 1–5: format, architecture, dtype, quantization, shape).
- **Establishment**: at load-time admission, through the fail-closed support-matrix row gates (`pml0-support-matrix-schema.md` §2/§3 — R1–R11) and the admitted-model capsule (PML0-U14: validated bytes + cryptographic identity + quantization + bounds + architecture facts).
- **Owner**: gradus (ML semantics; NGAB0 §OwnershipMatrix "ML semantics" row).
- **Carriage**: the capsule across Gradus ↔ faber-runtime/hosts; the `ModelInstance` fact inside the session surface.

### 2.2 Tokenizer identity

- **Definition**: tokenizer family + pre-tokenizer + special-token set (BOS/EOS/EOG) + vocabulary fingerprint (hash or pinned id list) — U5 field 6 vocabulary; GI1 gpt2/smollm probe precedent. Exactly reproducible; any mismatch fails admission (U5 R6).
- **Establishment**: load-time, as part of model admission (U5 field 6 validation rule).
- **Owner**: gradus. Per U4 §4, tokenizer identity is a shared contract split from `gradus:data` at the nested-leaf boundary (PML2 work); `data` itself stays the training-side loader.
- **Carriage**: rides the model capsule (U14) and the invocation surface's token ids (call-time values are ids, never raw text).

### 2.3 Parameters identity

- **Definition**: explicit identity + traversal for trainable values (U4 §4 "Parameters (PML1)" — the future shared-layer contract consumed by forward evaluation, training updates, and inference loading alike).
- **Establishment**: load-time, through the per-tensor-class repack descriptors (GI3-2 §8: the five tensor classes Q4_K 16 / Q5_0 176 / Q6_K 16 / Q8_0 17 / F32 65, per-class aggregate facts, declared-f32 conversion as the initial admitted representation). `QuantizedTensorLayout` stays the stored-layout authority and is never widened into the physical plan (GI3-2 §8).
- **Owner**: gradus (model/tensor semantics); radix keeps stored-layout facts as compiler evidence (GI3 §5).
- **Carriage**: repack descriptors in the representation record; identity facts in the capsule.
- **Reserved seam**: the exact traversal shape lands at PML1; v1 freezes the identity principle, not the traversal enumeration.

### 2.4 Generation-config identity

- **Definition**: the snapshot of settings that determines a generation run (sampling parameters, limits, stop conditions, regime) — the Gradus-side counterpart of the product campaign's server-options mapping (Council C6: "mapping server options → Gradus generation config" belongs to the inference-product campaign stub, not to PML0/NGAB0).
- **Establishment**: call-time (it is a per-run configuration, not a loaded artifact).
- **Owner**: gradus.
- **Carriage**: carried as typed config facts on the invocation surface.
- **Reserved seam**: the **full field list is NOT frozen at v1** (§FrozenNowReserved). v1 fixes that the identity exists and is carried as a typed snapshot; the field enumeration is a PML1/NGAB1 seam.

### 2.5 KV state identity

- **Definition**: `SequenceState` (position, token history, KV generations; advances only through a committed `TokenCommit`) + `KvCacheLayout` (slots, context_length, layer_count, kv_head_count, head_dim, dtype, reserve_policy) + `ReuseKey` = `(session, sequence, epoch)` — NGAB0 §Abi session facts, which mirror the GI4 session facts kept as compiler evidence (NGAB0-U8).
- **Establishment**: load-time/session-creation (the layout and binding are session facts, never per-call); state advances call-time.
- **Owner**: gradus owns the logical decode/KV semantics (Council C1); NGAB owns the composite session effects and physical execution (NGAB0 §OwnershipMatrix "effects, sessions" row). No dual authority: Gradus owns what the KV means; hosts owns where it runs.
- **Carriage**: KV facts ride the session surface; byte accounting is consumed, not re-derived (NGAB0 §Abi).
- **Reserved seam**: the decode/KV module shapes land at PML5 (U4: inference ownership is empty by measurement today); v1 freezes the identity and the NGAB0-mirrored fact names, not the PML5 module surface.

## 3. Fact classes: compile-time vs load-time vs call-time

Every fact crossing the boundary belongs to exactly one class, determined by when it is established and when it must be validated. Class membership decides the failure time and the carrying surface.

| Class | Established | Validated / fails at | Examples | Carrying surface |
| --- | --- | --- | --- | --- |
| **Compile-time** | Static structure of the program and the model surface | At compile time — before composite build/link and before launch (NGAB0 §Partition: invalid cross-boundary values fail at compile time for static facts) | Shapes and dtypes; static structure of forward functions; the module DAG / import surface; fixed-shape enumeration (`2x2`, `4x4`, `2x8` — U2/U3/U5); invocation arity and input/output type facts | Compiled program + this packet's §FrozenNowReserved static surface |
| **Load-time** | Model, tokenizer, parameters, KV layout admitted into the runtime | At admission — fail closed, never partially admitted (U5 §2 fail-closed invariant, R1–R11) | Capsule validation (U14); support-matrix row gates (U5); repack/capability tri-state (GI3-2 §9: `unsupported(reason)` / `supported_direct(candidates)` / `supported_with_explicit_conversion(candidates, conversion_plan)`); representation selection per tensor class (GI3-2 §8) | Capsule, support matrix rows, representation records |
| **Call-time** | Per-invocation values and observations | At admission/commit time for session facts (NGAB0 §Abi); mismatches fail before reaching launch | Invocation inputs (token id + absolute position — per-invocation only; resident inputs never ride an invocation); exactly one `InvocationMode`: `Prefill` or `ScalarDecode` (NGAB0 §Abi §2.4); output observations (full-vocab logits `[49152]` or the selected token); `ReuseKey` match; token-commit sequencing | Invocation/session wire surface |

The compiler-fact anchor (U4 live-importa fact, cited): the compiled module DAG today has exactly **two live import edges** — `src/tensor.fab:17` `importa ex "gradus:math" privata math` and `src/gradient.fab:15` `importa ex "gradus:tensor" privata tensor` (U4 §2a). This packet's semantic identities are declared **forward** semantics over the future shared layer (U4 §4: parameters PML1, model+admission PML2, tokenizer identity PML2, decode/KV PML5) — they are not live `importa` edges today, and no packet fact is asserted as an existing import. Inference ownership is empty by measurement (U4 §3), so call-time KV facts describe the NGAB0/GI4-mirrored surface, not a live Gradus module.

Class invariants:

- A fact's class never changes by transport: what is established at load-time stays a load-time fact even when serialized onto the call wire.
- Neither class silently reaches launch: invalid cross-boundary values — wrong type, wrong shape, out-of-order position, KV-generation gap, unknown workload mode, mismatched `ReuseKey` — fail at compile time (static facts) or at admission/commit time (session facts) (NGAB0 §Abi).
- No silent CPU fallback for an explicit GPU route (GI3-2 §9; campaign stop condition) — a call-time failure is a failure, not a fallback.

## 4. Typed values, layouts, mutation, lifetimes, observations, reset, cancellation, errors

### 4.1 Typed values

Every value crossing the boundary carries its type fact. Types are carried in serialized form and **never re-derived from emitted LLVM/MSL/PTX text or naming conventions** (NGAB0 §Abi boundary rule; NGAB0 Dependency Rule 2). The boundary admits exactly one call shape — **one host function invokes one device kernel** (NGAB0 §Partition); call and entry are the same typed operation seen from either side.

### 4.2 Layouts

- `KvCacheLayout`: slots, context_length, layer_count, kv_head_count, head_dim, dtype, reserve_policy (NGAB0 §Abi). Byte accounting is consumed, not re-derived.
- `QuantizedTensorLayout` (GGUF) stays the **stored-layout authority** and is never widened into the physical plan (GI3-2 §8). Per-tensor byte ranges come from committed contract metadata; execution-time digests are resolved at upload and recorded on receipts (GI3 §8).
- Repack descriptors (GI3-2 §8 field list) describe every conversion with independent identity, destination layout, algorithm family, shape/padding/alignment/byte extent, transform implementation + version, output digest, setup time + peak temporary memory, persistence/cache policy, and executable compatibility.

### 4.3 Mutation

- `TokenCommit` advances token id, position, KV generations, and visible output **together**; no retry without deterministic replay from the last committed generation (NGAB0 §Abi; GI4 §5 mirror). There is no partial token advancement.
- Resident weights and KV are uploaded once at session creation and **never re-copied** per call (NGAB0 §Abi `ExecutionSession` fact).
- `ReuseKey = (session, sequence, epoch)`: resident resources are reusable iff all three match (NGAB0 §Abi).

### 4.4 Lifetimes

- `ModelInstance`: model id + SHA-256 + byte length; **load-once at session creation** (NGAB0 §Abi §2.1).
- `ExecutionSession`: binds one `ModelInstance`, carries a typed `KvCacheLayout`, tracks current `SequenceState`, mints `ReuseKey`s (NGAB0 §Abi §2.2).
- `SequenceState`: position, token history, KV generations; advances only through a committed `TokenCommit` (NGAB0 §Abi §2.3).
- Lifecycle order: admit (load-time, §FactClasses) → load → session creation → call/observe → reset → teardown. Nothing on this packet's boundary contradicts an accepted GI4 fact (NGAB0 §Abi).

### 4.5 Observations

- Invocation output: full-vocab logits `[49152]` (tied-head projection) or the selected token (NGAB0 §Abi §2.4).
- Regime labels are reported **separately** — prefill vs decode are never merged into one end-to-end number (GI3 §3: the prefill regime schema records shape class, representation, algorithm, workspace, evidence as five separate fields; GI4 owns decode; "no end-to-end number is ever mislabeled").
- Numeric posture (GI3 §4A, read-only): the Q2 GPU-vs-oracle envelope is **6.5e-3** per element over full-vocab raw logits, frozen as a pinned-row empirical compatibility envelope — explicitly **not** an f32 precision bound and **not** generalizable. A future observation above the envelope **FAILS** and triggers diagnosis/versioning — **no auto-widen**. Hard gates stay hard: top-1 exact over non-EOG {0, 2}, the finite gate, the first-divergence rule.

### 4.6 Reset

- Reset is a session-surface operation: sequence/epoch rollover that changes the `ReuseKey` epoch/sequence components so resident resources stop being reusable under the old key. Reset never rewinds a committed `TokenCommit` — state after reset is a fresh epoch, not an un-committed rollback.
- What survives a reset: the `ModelInstance` binding and the `KvCacheLayout` (session-level facts); what does not: `SequenceState` position/token history and any in-flight prefill/decode sequence.

### 4.7 Cancellation

- Cancellation of an in-flight call is fail-closed: a cancelled call reports cancellation as a typed result; it does not silently fall back to a different backend or a CPU path (no silent CPU fallback, GI3-2 §9) and does not produce a half-committed token (mutation atomicity, §4.3).
- Cancellation never mutates `SequenceState`; a cancelled sequence restarts from the last committed `TokenCommit` (deterministic replay rule).

### 4.8 Errors

- Errors are typed and carry their fact class: compile-time errors (static shape/type violations), admission errors (load-time gate failures — U5 R1–R11), and call/commit-time errors (session-fact violations). No error class silently reaches launch.
- The capability result is a structured tri-state, not a boolean: `unsupported(reason)` | `supported_direct(candidates)` | `supported_with_explicit_conversion(candidates, conversion_plan)` (GI3-2 §9).
- Fail-closed typed diagnostics precedent: GI3-1 recipes fail closed with a typed diagnostic on any const/typed violation; plans never infer facts (GI3 §1). This packet adopts the same posture for its boundary values.

## 5. Host-device ABI and manifest-version relationship

### 5.1 The boundary

The host/device partition is the static split that survives lowering, assembly, and launch (NGAB0 §Partition): **one host function calls one device kernel through a versioned typed boundary**. The host side is the one native executable of §PackageGraph; the device side is one typed device kernel per call emitted from the target-neutral device program; backend variants are serialization choices of one program, never separate programs. The partition binds the same ownership as §OwnershipMatrix — never a second authority.

### 5.2 Version relationship

- The boundary is a **versioned surface with its own ratchet** (MD2-W1 sibling-field precedent): it rides the accepted wire version and **requires no `WIRE_DEVICE_PROGRAM_VERSION` bump** (NGAB0 §Abi).
- Wire revisions of the session surface are **GI4-2's**, not this packet's (NGAB0 §Abi).
- Current wire facts (GI3 §6, read-only): `DEVICE_RUN_PLAN_VERSION = 7` and `WIRE_DEVICE_PROGRAM_VERSION = 7`, both unchanged by GI3; **GI4 owns the next versioned cadence/session change** (GI3-1 §6, CTO S12). This packet does not pre-empt that: a packet bump does not, by itself, move the wire version.

### 5.3 Manifest-version relationship

- The composite build/link manifest (NGAB0 §PackageGraph: "Build plan joining LLVM host link with embedded device artifacts; inspectable layout + link manifest + runtime identity") records which packet revision the artifact was built against.
- Admission relationship: a mismatch between the artifact's recorded packet revision and the runtime's admitted revision **fails closed at admission** (load-time class) — the manifest is the seam where this packet's revision and the wire/executable identity meet.
- A **major** packet bump re-pins the admitted manifest version; minor/patch bumps do not (a major bump is a meaning/field change, §VersionBump). The manifest never silently upgrades: a manifest carrying a rejected packet revision is rejected at admission, not coerced.

## 6. Version-bump authority, rejection, and migration policy

### 6.1 Authority (named owner)

- **Version owner**: the joint interface-packet authority — the PML campaign Mind and the NGAB campaign Mind acting together; the **operator** is the binding decision owner for disputed bumps (delivery §Decision owner: binding decisions route through a Vivi need To `reviewer`/`operator@`; recorded defaults proceed until overridden).
- NGAB0's own packet version authority freezes at **NGAB0-U7**; this packet's authority coordinates with that freeze. Both campaigns must accept a bump that touches this packet; one side cannot unilaterally change a shared surface.

### 6.2 Versioning scheme

`pml0-interface-packet` follows the U5 schema-bump semantics (consistent with `gradus-support-matrix-schema v0.1.0` §2):

- **Patch bump**: clarification or example only; no vocabulary or rule change.
- **Minor bump**: vocabulary expansion or added reserved-seam detail; existing facts remain valid under the previous revision.
- **Major bump**: field removal/renaming, meaning change, or a fail-closed rule change — **every consumer re-validates** under the new revision; the admitted manifest version is re-pinned (§5.3).

### 6.3 Change procedure

- Any change to a **frozen-now** field (§FrozenNowReserved) requires a **major bump** and full re-validation across both campaigns, with a recorded reason (S6-N1 naming-freeze precedent: "a spelling change after this freeze needs a recorded reason").
- Changes to reserved seams proceed through the normal revision procedure within PML1/NGAB1; they are the intended revision path, not a bypass.
- No silent field edit: the packet is revised by revision, never edited in place.

### 6.4 Rejection policy

A proposed bump or field change is **rejected** when:

- **R1** — It contradicts a frozen `gi3-contract.md` fact: GI facts are read-only compiler evidence for this campaign; a packet revision that overrides an accepted GI fact is rejected (it must be resolved through the GI-side change path, not the packet).
- **R2** — It changes a frozen-now field without the §6.3 procedure (no recorded reason, no major bump).
- **R3** — It implies a support claim without a corresponding admitted support-matrix row (U5 R10: a policy that implies broader support than the row rejects).
- **R4** — It is unilateral: not accepted by both campaigns.
- **R5** — It introduces a device or HTTP surface (exclusion clause, §Exclusion) — those are permanent non-goals, not revisable surfaces.
- **R6** — It is unversioned or repurposes an existing revision number.

Rejected bumps are recorded (revision + reject reason) in the packet's change log so the reason is auditable — mirroring the U5 reject-log posture. Recording a rejected bump never constitutes acceptance.

### 6.5 Migration policy

- **One admitted revision at a time** — no dual authority: consumers pin the packet revision they implement (same principle as U7's no-dual-authority-by-code-location, applied here to revision pins).
- **Receipt trail**: migration between revisions is proven by the joint cross-repo receipt schema (PML0-U13) — each receipt records repo, commit, dirty state, command, artifact hash, verdict, stage. A consumer's receipt must name the packet revision it was validated against.
- **Coordinated window**: backward-incompatible (major) bumps force a coordinated migration window across both campaigns — Gradus and NGAB migrate together, never one ahead of the other on the shared surface.
- **Fallback rule**: if a bump is blocked (e.g. an operator decision is pending), the current admitted revision remains in force until the bump is accepted — the recorded default proceeds until overridden. There is no half-admitted revision.

## 7. Frozen-now vs reserved-seam field split

| Surface | Status at v1 | Change route |
| --- | --- | --- |
| Semantic identity names (model/tokenizer/parameters/generation-config/KV state) | **frozen-now** | major bump + recorded reason (§6.3) |
| Fact-class taxonomy (compile/load/call) and class invariants | **frozen-now** | major bump |
| `ReuseKey` = `(session, sequence, epoch)` shape | **frozen-now** | major bump |
| `InvocationMode` vocabulary (`Prefill` / `ScalarDecode`) | **frozen-now** | major bump (vocabulary expansion via minor) |
| `TokenCommit` atomic mutation rule + deterministic-replay rule | **frozen-now** | major bump |
| Observation posture: envelope fail-on-exceed, no auto-widen; regime labels reported separately | **frozen-now** | major bump |
| Exclusion clause (§8) | **frozen-now** | **never revisable** (§6.4 R5) |
| Generation-config full field list | **reserved seam** | normal revision within PML1/NGAB1 |
| Parameters traversal enumeration | **reserved seam** | PML1 (identity principle frozen at v1) |
| Tokenizer identity exact fingerprint policy details | **reserved seam** | PML2 |
| Decode/KV module shapes and the PML5 module surface | **reserved seam** | PML5 |
| Sampling parameter details | **reserved seam** | PML1/NGAB1 |
| Observation surface extension beyond logits `[49152]` / selected token | **reserved seam** | PML1/NGAB1 |
| HTTP/serving mapping (product campaign, Council C6) | **reserved seam — outside both campaigns** | inference-product campaign |

Rule of thumb: **frozen-now** is what both campaigns must build against identically today; **reserved seam** is what is deliberately left open so PML1/NGAB1 can land compiled proof without a version war. A reserved seam is not a promise to fill — it is a permission to change through the normal procedure.

## 8. Non-goals — exclusion clause

This packet carries **no device handle**: the Gradus API and this interface packet never expose or accept a physical device, backend, or GPU object. Gradus receives no such handle and no backend handle; it stays device neutral (NGAB0 §OwnershipMatrix "ML semantics" row). Physical device effects belong to hosts (NGAB0 §OwnershipMatrix "effects, sessions" row), and nothing in this packet crosses that line.

This packet carries **no HTTP policy**: there is no HTTP, serving, request scheduling, batching, deployment, or network-surface policy anywhere in this packet. Serving/HTTP belongs to the separate inference-product campaign (Council C6), which is explicitly not drafted in PML0 or NGAB0 and which NGAB only supplies an executable path for (NGAB0 §OwnershipMatrix "Inference product repo" row).

The two exclusions mirror each other across the campaigns: NGAB0's packet states the same non-goals (NGAB0 §OwnershipMatrix). They are permanent — §6.4 R5 makes them non-revisable.

## 9. Cross-links

### 9.1 NGAB0 composite contract (faber, `ngab0-composite-contract.md`)

- §PackageGraph — composite native-GPU application graph; node/owner table; the one-package → one-executable invariant; identity/type/resource/lifetime facts survive lowering (Dependency Rule 2).
- §OwnershipMatrix — owner-per-surface matrix (faber assembly / radix compiler facts / hosts effects / gradus ML semantics / product later); Dependency Rule 1 (versioned interface packet exchange), Rule 6 (GI3 evidence reusable; GI4–GI7 re-lowered; model runtime and serving never land in faber, radix, or hosts), Rule 7 (multi-device consumes, does not block).
- §Partition — the one-host-function/one-device-kernel split; compile-time failure for invalid cross-boundary values.
- §Abi — versioned typed entry/call boundary; `ModelInstance`, `ExecutionSession`, `SequenceState`, `KvCacheLayout`, `ReuseKey`, `TokenCommit`, `InvocationMode` facts (mirrors of the GI4 session facts kept as compiler evidence).

### 9.2 GI3 contract facts (radix, `gi3-contract.md`, read-only)

- §1/§1.1 — frozen recipe names (Gather / RmsNormalization / Rope / CausalMaskedSoftmax) + `TensorCausalMaskedSoftmax` MIR op; fail-closed typed diagnostics precedent (adopted in §4.8).
- §3 — prefill regime labeling schema (shape class / representation / algorithm / workspace / evidence; five fields separate; decode is GI4's; no mislabeled end-to-end number) — cited in §4.5.
- §4A — Q2 GPU-vs-oracle envelope 6.5e-3, pinned-row, fail-on-exceed, no auto-widen — cited in §4.5.
- §5 / §8 / §9 — repack/capability contracts (`QuantizedTensorLayout` stored-layout authority; declared-f32 initial representation; tri-state capability, no silent CPU fallback) — cited in §2.3 and §4.
- §6 — wire mirror arms; `DEVICE_RUN_PLAN_VERSION = 7` / `WIRE_DEVICE_PROGRAM_VERSION = 7` unchanged; GI4 owns the next versioned cadence/session change — cited in §5.2.

### 9.3 PML0 siblings (gradus)

- **U1** `pml0-source-snapshot.md` — version stamps this packet resolves against.
- **U4** `pml0-module-dag.md` — live-importa fact (§3), ownership table, future shared layer (§2.1–2.5).
- **U5** `pml0-support-matrix-schema.md` — row vocabulary and fail-closed admission gates (§2, §3, §6.4).
- **U10** `pml0-gradus-contract.md` (in-flight) — the contract that references this packet's revision; the artifact NGAB0 lists as the Gradus required output.
- **U12** `pml0-claim-register.md` — claim register consumes the U5 row vocabulary so claim status never reads as product support.
- **U13** `pml0-receipt-schema.md` — joint receipt schema; migration receipts name the packet revision (§6.5).
- **U14** `pml0-model-capsule-contract.md` — admitted-model capsule as the typed handoff carrying model/tokenizer/quantization identity (§2.1, §2.2).

## Validation

```bash
# 1. Every listed section present (grep the section headings).
grep -c '^## ' docs/factory/production-ml-library/pml0-interface-packet.md
# 2. The §8 exclusion term occurs exactly once in the doc — every hit is inside §8.
#    ([h] avoids matching this command line itself.)
grep -c 'device [h]andle' docs/factory/production-ml-library/pml0-interface-packet.md   # == 1
grep -n 'device [h]andle' docs/factory/production-ml-library/pml0-interface-packet.md   # single hit, in §8
# 3. Revision label present.
grep -c 'revisable through PML1/NGAB1' docs/factory/production-ml-library/pml0-interface-packet.md
git diff --check
```

Outcome: all sections present; the §8 exclusion term appears exactly once and only inside §8 (the exclusion clause); the revision label is present; `git diff --check` clean. Closeout per `pml0-delivery.md` §Validation + the Cargo discipline: no cargo anywhere (docs-only unit).
