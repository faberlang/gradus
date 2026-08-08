# PML0 Gradus Contract — ownership, baseline, and cross-campaign interface

**Unit**: PML0-U10 of [`pml0-delivery.md`](pml0-delivery.md) (assembly — the
required output of the PML0 phase)
**Date**: 2026-08-08
**Status**: committed as the top-level PML0 contract; supersedes no artifact
(see §6 — it is a synthesis of the gate artifacts, not a replacement)
**Required output of**: both campaigns — PML0 (`pml0-delivery.md` §Gate
Artifacts → "Required outputs") **and** NGAB0. NGAB0 lists this document as a
Gradus required output: `faber/docs/factory/native-gpu-application-bundle/
CAMPAIGN.md` ("the Gradus `pml0-gradus-contract.md`" among NGAB0's required
outputs), `ngab0-delivery.md` (U2 lane), and `ngab0-composite-contract.md`
§OwnershipMatrix ("ML semantics" row cites it as the exchange partner).
**Interface-packet revision referenced**: `pml0-interface-packet v1`
(2026-08-08), committed at gradus `846b97e` (PML0-U9) — see §2.1.
**Decision owner**: operator (binding decisions route through a Vivi need To
`reviewer`/`operator@`; recorded defaults proceed until overridden — per
`pml0-delivery.md` §Decision owner).
**Sibling required output**: the committed GI4+ ownership amendment + migration
map in `radix/docs/factory/gpu-inference-gguf/` (PML0-U11, in flight — Gate B).
PML0 **cannot close** while GI4+ still assigns model runtime or serving to
`faber-runtime` or any other old owner.

---

## 1. What this contract is

This is the phase-level contract that fixes, in one place, what Gradus will
own and how it behaves **from here forward** (PML1+): the ownership matrix, the
measured baseline, the support-matrix posture, the migration decisions, and
the exact interface the Gradus campaign exchanges with NGAB0. Every claim
below is backed by one of the PML0 gate artifacts (§3) or by NGAB0's own
contract (§2.2). Nothing in this document asserts a capability the live tree
does not have — inference ownership is empty by measurement (§4.1), numerical
coverage is zero by measurement (§4.2), and the support matrix admits zero
product rows by policy (§4.3).

The PML0 delivery spec (`pml0-delivery.md`) is the operational contract for
the phase itself (unit graph, write scopes, validation); this document is the
**contract that survives the phase**. Where this document and a gate artifact
differ, the gate artifact's evidence wins and this document is revised through
the same revision discipline as the artifacts it cites — never silently.

**Authority order** (campaign, `pml0-delivery.md` §Repo-Aware Baseline): live
Gradus source + tests → accepted Gradus contracts → accepted compiler/package
contracts → campaign stage receipts → examples and historical plans. This
document sits in the second tier; a live fact that contradicts it wins, and it
is revised, never silently edited.

## 2. Cross-campaign interface

### 2.1 Interface-packet revision

The interface this campaign exchanges with NGAB0 is
[`pml0-interface-packet.md`](pml0-interface-packet.md) (PML0-U9, Council
mandate C4), committed at gradus **`846b97e`** — packet revision
**`pml0-interface-packet v1`** (2026-08-08). The packet is labeled
**revisable through PML1/NGAB1** — it precedes compiled proof and is not
frozen for all phases; it is a versioned machine contract with a named version
authority (§VersionBump) and an explicit frozen-now vs reserved-seam field
split (§FrozenNowReserved). This contract and its revision pin are the
artifact NGAB0's §OwnershipMatrix cites as the exchange partner for the
"ML semantics" row.

Version discipline (from the packet, §VersionBump): **one admitted revision at
a time**; a major bump (field removal/renaming, meaning change, fail-closed
rule change) re-pins the admitted manifest version and forces a coordinated
migration window across both campaigns; rejection policy R1–R6 applies (no
GI-fact override, no unilateral change, no device/HTTP surface, no unversioned
revision). Migration between revisions is proven by the joint cross-repo
receipt schema (PML0-U13).

### 2.2 NGAB0 contract (the pairing)

The other half of the exchange is `faber/docs/factory/native-gpu-application-
bundle/ngab0-composite-contract.md`. Its §OwnershipMatrix assigns **ML
semantics → gradus** (model, tokenizer, transformer, decode, cache, sampling
semantics; **no device handle**, no serving policy) and cites this document as
the exchange partner. Dependency Rule 1 of both campaigns: **one versioned
interface packet is exchanged before either campaign generalizes its public
boundary.** Dependency Rule 6: GI3 compiler evidence is reusable; GI4–GI7
ownership and product clauses are re-lowered under the new Gradus (PML5
semantics) and separate-inference-product decision before further
implementation. Model runtime and serving never land in faber, radix, or
hosts.

## 3. Gate artifacts (U2–U9) — what each froze

PML0's gate items each produced a committed artifact. This contract summarizes
them; each summary defers to the artifact by path. All are in this directory
(`gradus/docs/factory/production-ml-library/`).

### U2 — Public symbol inventory → `pml0-symbol-inventory.md`

The grep-based inventory (`scripta/inventory-public-symbols`) fixed the public
surface: **21 `functio` declarations** across the 11 live modules, with
per-module counts matching the campaign baseline exactly — nn 6, train 4,
loss 3, transformer 3, gradient 2, optimize 2, attention 1; math, tensor,
data, and the gradus facade have **0** (stubs). **Effect on this contract**:
the public surface is 21 symbols; the stubs are not capabilities.

### U3 — Proof-shaped API ledger → `pml0-proof-api-ledger.md`

The clean-break ledger over the **17 fixed-shape functions** (`*_2x2/_4x4/
_2x8`): every symbol was checked for a real external caller and assigned a
disposition — **13 admit** (caller-backed: nn 6, loss 3, attention 1,
transformer 1, train 2), **4 retire** (`sgd_step_2x2/_4x4`,
`attention_block_2x8`, `ffn_block_2x8` — no caller; their math is inlined in
caller-backed functions). The retire rows lose no capability; the production
tensor API shape posture (generic / generated / staged mix) is decided at
PML1. **Effect on this contract**: 13 symbols are caller-backed proof today;
4 are scheduled for removal at the next API-shape decision.

### U4 — Module DAG + ownership table → `pml0-module-dag.md`

The import DAG of the 11 live modules: exactly **two live `importa` edges**
(`gradus:tensor → gradus:math`, `gradus:gradient → gradus:tensor`); the rest
declared in header comments due to the recorded FMIR stepper
library→library-call limitation. The ownership table (§4.1 below) assigns each
module exactly once. The future shared layer (forward semantics usable with
and without autograd) is defined: parameters (PML1), model + admission (PML2),
tokenizer identity (PML2), forward architectures (PML3), decode/KV/sampling/
generation (PML5). **Effect on this contract**: the module graph and
ownership matrix this contract restates in §4.

### U5 — Support-matrix schema → `pml0-support-matrix-schema.md`

The versioned row schema (`gradus-support-matrix-schema v0.1.0`): 10 required
fields (format, architecture, dtype, quantization, shape, tokenizer identity,
legal fixture ref, oracle ref, evidence links, compatibility policy), each
with a fail-closed validation rule; **one admitted row first** posture; reject
rules R1–R11; an empty row template as the **only** row-shaped content in PML0
(no product support yet, by construction). **Effect on this contract**: the
support posture in §4.3.

### U6 — Numerical + claim-drift baseline → `pml0-numerical-baseline.md`

The measured baseline, marked **"measured, not claimed"**: **0 co-located
`.proba` files** in the tree — 0/21 functions have a co-located numerical
test; the only recorded numerical evidence is external to `gradus/src`. Four
verified claim drifts (D1 README attention/transformer status, D2
`corpus/nanogpt-shakespeare` reference with no `corpus/`, D3 dangling
`docs/module-map.md`/`api-shape-policy.md` links, D4 zero `.proba` rule
fulfillment), each with a correction disposition and named owner. **Effect on
this contract**: §4.2; no numerical coverage claim is made anywhere in this
contract.

### U7 — Admission-code migration mechanics (C3) → `pml0-admission-migration-decision.md`

Decision: GI1's accepted admission trio (`faber-runtime/src/gguf.rs`,
`tokenizer/`, `dequant.rs`) **migrates into Gradus at PML2** (re-expression
port, Rust → Faber; the faber-runtime trio is the migration oracle), under a
**no-dual-authority rule enforced by code location** — single owning path
`gradus/src/model/`; the faber-runtime trio hosts no admission logic from this
decision date and is removed (`git rm`, no forwarding shims) at the PML2
boundary. Fallback if blocked: **formally retire** — never both locations
hosting admission logic. Decision owner: operator (Vivi need `f3309d29`).
**Effect on this contract**: model-format admission moves to Gradus at PML2
(§4.4); the GI0–GI3 clauses assigning model-runtime ownership to
`faber-runtime` are stale and feed U11's reconciliation.

### U8 — `norma:model` migration decision → `pml0-norma-model-decision.md`

Decision: the Safetensors/GGUF parsing in `norma/src/model.fab` **migrates
into Gradus at PML2 — not now**, under the same no-dual-authority rule
(single owning path `gradus/src/model/`), with a **no-stranded-callers**
transfer condition (destination API exists + no stranded importer — the only
known caller today is
`examples/ai-workbench/packages/faber-ai/src/commands/model.fab` — + norma
cooperates) and a fallback (no partial migration; escalate to `operator@`).
Gradus stays self-contained: grep proves no `gradus→norma` imports today.
**Effect on this contract**: model-format parsing is a PML2 migration, not a
PML0 capability (§4.4).

### U9 — Cross-campaign interface packet v1 (C4) → `pml0-interface-packet.md`

The versioned packet at **`846b97e` / `pml0-interface-packet v1`**: semantic
identities (model, tokenizer, parameters, generation-config, KV state);
compile/load/call fact classes; typed values, layouts, mutation, lifetimes,
observations, reset, cancellation, errors; host-device ABI + manifest-version
relationship; version-bump authority + rejection/migration policy; frozen-now
vs reserved-seam split; exclusion clause (no device handle, no HTTP policy).
Read-only facts from `gi3-contract.md` and NGAB0's §Abi (§2.1 here).

## 4. The ownership matrix (restated from U4)

Each live module owns exactly one column. Ownership follows the desired end
state: **shared contracts are consumed unchanged by training and inference**;
autograd, losses, optimizers, datasets, and training loops stay a training
layer over reusable forward functions; the inference layer lands in PML5 over
the same forward functions.

| Column | Modules | Basis |
| --- | --- | --- |
| **shared** (5) | `math`, `tensor`, `nn`, `attention`, `transformer` | Forward-evaluation semantics; no autograd dependency by construction; consumed by training and inference alike |
| **training** (5) | `gradient`, `loss`, `optimize`, `train`, `data` | Training-layer concerns over forward functions (`data` is the training-side loader; tokenizer identity splits from it at the nested-leaf boundary, PML2) |
| **inference** (0) | — none today — | No decode/KV/sampling/generation module exists in the live tree; those are PML5 modules over the shared forward functions |
| **other** (1) | `gradus` (facade) | Package map only; owns no genera and no semantics |

TOTAL 11 modules. Ownership is exactly-once; no module appears in two columns.
Inference ownership is **empty by measurement, not by omission** (U4 §3).

### 4.1 Forward semantics invariant

Reusable model evaluation must **not depend on autograd** (campaign posture:
"Forward functions first"). Training requests compiler-generated backward
companions from `gradus:gradient`; inference calls forward and decode paths
without building a gradient path. Membership rule: a module is shared when
**both** training and inference consume the same function unchanged.

### 4.2 Measured baseline (from U6)

- **0/21** public functions have a co-located numerical test (zero `.proba`
  files in the tree).
- Four claim drifts verified live and dispositioned (D1–D4, `pml0-numerical-
  baseline.md`); correction owners named.
- Gradus gates today: `./scripta/check-source` + `./scripta/check-compile`
  (`faber check`, no cargo) — source and compile checks only, not numerical
  proof.

### 4.3 Support posture (from U5)

- Support is claimed **only at the row level**: "this exact row is admitted",
  never "the library supports GGUF / transformers".
- **One admitted row first**; zero product rows admitted in PML0 (template
  only). First rows land at PML2 (one Safetensors row, one selected GGUF row),
  each failing closed on format, architecture, dtype/quantization, shape,
  tokenizer identity, and version (schema `gradus-support-matrix-schema
  v0.1.0`, reject rules R1–R11).

### 4.4 Migration decisions (from U7, U8)

- **Admission trio** (faber-runtime `gguf.rs` / `tokenizer/` / `dequant.rs`):
  migrate into Gradus at PML2 by re-expression; no-dual-authority by code
  location (`gradus/src/model/`); fallback = formally retire; owner =
  operator.
- **`norma:model` parsing**: migrate at PML2 (not now); no-dual-authority;
  no-stranded-callers condition; fallback = no partial migration + escalate.
- Until PML2, **Gradus owns no model-format admission** — the live tree has no
  `gradus:model` module, and no contract above claims one.

## 5. Non-goals (binding, restated)

These are the campaign's non-goals; they bind every stage that consumes this
contract and are mirrored in the NGAB0 packet:

1. **No device handle.** The Gradus API never exposes or accepts a physical
   device, backend, or GPU object — no CUDA/Metal handle, no allocator/stream/
   command-buffer, no device-session value. Gradus receives no backend handle;
   it stays device neutral. (Packet §Exclusion; `ngab0-composite-contract.md`
   §OwnershipMatrix "ML semantics" row.)
2. **No serving.** No HTTP, serving, request scheduling, batching, deployment,
   or network-surface policy in Gradus or in the interface packet. Serving/HTTP
   belongs to the separate inference-product campaign (Council C6), not
   drafted in PML0 or NGAB0. (Packet §Exclusion; U9 §8.)
3. **Correctness before performance.** Tokenization, logits, gradients, state
   mutation, and deterministic sampling gate speed claims. A call-time failure
   is a failure, not a silent CPU fallback; no end-to-end number is ever
   mislabeled. (Campaign Development Posture; GI3 §3/§4A posture adopted in
   the packet.)
4. **No model-format code migration in PML0.** Migration of admission and
   parsing is PML2 work (U7, U8); PML0 measures and freezes only.
5. **No `src/**` edits in PML0.** The phase is discovery-only: measurement and
   contracts, no product code.

Stop conditions (campaign): pause and route a need when a public API requires
a backend/device handle; a shape or dtype cannot be represented truthfully;
moving `norma:model` would strand callers or create dual authority; a
model/tokenizer row lacks a pinned legal fixture and oracle; performance
begins before correctness; or work would implement a server, deployment, or
paid external GPU operation here.

## 6. Relationship to other artifacts

- **Supersedes nothing.** This contract is a synthesis: each gate artifact
  (U2–U9) remains the authoritative detail for its subject; this document
  fixes the cross-cutting ownership, baseline, and interface facts in one
  place.
- **Consumed by**: PML1–PML7 deliveries (module graph, ownership, support
  posture, interface revision); NGAB0 §OwnershipMatrix exchange partner;
  PML0-U11 (GI4+ ownership amendment — the sibling required output);
  PML0-U12 (claim register rows never read as product support); PML0-U13
  (joint receipts; migration receipts name the packet revision).
- **Related required output**: `radix/docs/factory/gpu-inference-gguf/
  gi4-ownership-amendment.md` + migration map (U11, Gate B) — the ownership
  amendment that makes the clauses cited in U7 §2 read as historical, not
  current. PML0 cannot close without it.

## 7. Validation

```bash
# 1. Every U2–U9 artifact linked by path (each gate artifact appears once).
grep -c 'pml0-symbol-inventory.md' docs/factory/production-ml-library/pml0-gradus-contract.md      # 1
grep -c 'pml0-proof-api-ledger.md'  docs/factory/production-ml-library/pml0-gradus-contract.md      # 1
grep -c 'pml0-module-dag.md'        docs/factory/production-ml-library/pml0-gradus-contract.md      # 1
grep -c 'pml0-support-matrix-schema.md' docs/factory/production-ml-library/pml0-gradus-contract.md  # 1
grep -c 'pml0-numerical-baseline.md' docs/factory/production-ml-library/pml0-gradus-contract.md     # 1
grep -c 'pml0-admission-migration-decision.md' docs/factory/production-ml-library/pml0-gradus-contract.md  # 1
grep -c 'pml0-norma-model-decision.md' docs/factory/production-ml-library/pml0-gradus-contract.md   # 1
grep -c 'pml0-interface-packet.md'   docs/factory/production-ml-library/pml0-gradus-contract.md     # 1
# 2. Interface-packet revision named (commit + label).
grep -c '846b97e' docs/factory/production-ml-library/pml0-gradus-contract.md
grep -c 'pml0-interface-packet v1' docs/factory/production-ml-library/pml0-gradus-contract.md
# 3. Ownership matrix restated (shared 5 / training 5 / inference 0 / other 1).
grep -c 'inference.*0.*— none today' docs/factory/production-ml-library/pml0-gradus-contract.md
# 4. Non-goals restated.
grep -c 'No device handle' docs/factory/production-ml-library/pml0-gradus-contract.md
grep -c 'No serving' docs/factory/production-ml-library/pml0-gradus-contract.md
grep -c 'Correctness before performance' docs/factory/production-ml-library/pml0-gradus-contract.md
# 5. README regenerated and fresh, then diff check.
cd /Users/ianzepp/work/faberlang/gradus
python3 ../radix/scripta/generate-factory-readme.py --factory-root docs/factory
python3 ../radix/scripta/generate-factory-readme.py --factory-root docs/factory --check   # exit 0
git diff --check
```

Outcome: each U2–U9 artifact is linked by path; the interface-packet revision
(`846b97e` / `pml0-interface-packet v1`) is named; the ownership matrix and
the three headline non-goals are restated; the factory README regenerates
fresh (`--check` exit 0); `git diff --check` clean. Closeout per
`pml0-delivery.md` §Validation + the Cargo discipline: no cargo anywhere
(docs-only unit).
