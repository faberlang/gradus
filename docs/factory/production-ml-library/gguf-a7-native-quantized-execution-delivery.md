# Delivery: GGUF-A7 — Native Quantized Execution Contract

**Status**: planned — lowering artifact; no unit dispatched yet
**Campaign**: [`radix/docs/factory/gpu-production-readiness/CAMPAIGN.md`](../../../../radix/docs/factory/gpu-production-readiness/CAMPAIGN.md),
mandatory work **A7 — native quantized execution contract from scratch**
**Semantic delivery authority**: [`pml5-general-gguf-delivery.md`](pml5-general-gguf-delivery.md)
§GGUF-A7 (unit definition) and §GGUF-M5 (successor)
**Planner**: planner-35 (fresh lowering; no planner-1..19 content reused)
**Assignment handle**: `9d5ed033` (mind → planner-35)
**Planning scope**: cross-repo Gradus/Radix/Hosts interfaces joining packed
values to native Metal/CUDA, predecessor gates, and qualification
**Repo baselines**: Radix `b6d6e17c8ad7`; Gradus `bc500993c97b`; Hosts
`57d659d60430`; public Faber `1fb6cc97e66d`
**Integration stop**: `factory/merge` only; this delivery does not fast-forward
any main branch

## 1. Interpreted Unit / Problem

GGUF-A7 makes the campaign's "quantized means native" posture executable.
Today the three dense reference rows (`llama` SmolLM2-360M, `qwen2`
Qwen2.5-0.5B, `qwen2` Qwen2.5-1.5B) reach the admitted devices only through
`RepackIdentity::Declared` — the GI3 declared-F32 conversion reuses the CPU
dequant to widen weights to F32 on the host and uploads them
(`docs/factory/gpu-inference-gguf/gi3-delivery.md` §GI3-5; base
representation record `gi3-representation-record.json`). That path is
explicitly *not* direct GGUF quantized execution and is excluded from GI6+
comparisons ("must disclose or go native"). GGUF-A7 is the **go-native** step:
device kernels consume GGML blocks directly, no whole-model F32 expansion
anywhere in the executed path.

The unit is a cross-repo contract, not an Inferentia or single-repo task:

- **Gradus** supplies packed layout and semantic operation requirements
  (device-neutral values and operations).
- **Radix** owns lowering, fusion, generated kernels, and `DeviceProgram`.
- **Hosts** owns physical allocation, residency, launch, synchronization, and
  teardown.
- **Faber** owns package/build/run composition; the A7 device proofs use the
  existing env-gated proof-test pattern, not a new public product surface.

## 2. Normalized Spec

One coherent delivery-sized outcome:

> The three dense reference rows execute their complete prefill and
> autoregressive-decode forward graph through **native packed GGML-block
> kernels** on both admitted single-device backends — Metal on burgus and
> CUDA on pharos — with `RepackIdentity::Native`, **without whole-model F32
> expansion**, with the model resident across decode steps and a second
> prompt in one admitted session (the **dense-row** residency substrate — see
> the block-frontier note below: A7 itself does not extend to the `qwen35moe`
> block layouts),
> and with receipts recording correctness, memory, timing, backend identity,
> and fail-closed capability evidence per the campaign validation list.

A7 establishes the **dense-row** kernel + residency substrate: the three dense
reference rows (SmolLM2-360M, Qwen2.5-0.5B, Qwen2.5-1.5B) and their closed
block set `{F32, Q5_0, Q8_0, Q4_K, Q6_K}`. The `qwen35moe` target (MODEL-04)
requires two additional block layouts — **BF16** (layer-40 router gates
`blk.N.ffn_gate_inp{,_shexp}.weight`) and **Q5_K** (38 layers of
`blk.N.ffn_down_exps.weight`) — that A7's substrate does not admit. Those
layouts are the **EXEC-02/M5 block-extension frontier**: EXEC-02 (Radix;
`radix/docs/factory/gpu-production-readiness/CAMPAIGN.md` line 91, "implement
every packed native kernel required by the target") owns the full kernel set
including BF16 and Q5_K, and GGUF-M5 consumes this substrate only after that
frontier extends the layout contract, the dequant oracle, and the native
kernels. A7 declares the frontier; it does not cross it, and it does not
narrow EXEC-02/M5's mandate to cross it. The persistent `qwen35moe` execution
with the 256-token two-prompt guarantee, KV/SSM state retention, and the Faber
capstone remain mandatory successors (GGUF-M5/M6; campaign EXEC-03, CAP-01,
CAP-02, CLOSE-01). A7 does not narrow, downgrade, defer, or relocate them.

## 3. Repo-Aware Baseline (ground truth, 2026-08-13)

| Fact | Evidence |
| --- | --- |
| `gradus:model/dequant` implements bit-exact CPU dequant for the **dense-row** closed set `{F32, Q5_0, Q8_0, Q4_K, Q6_K}` (SmolLM2 pinned row; no `GGML_BF16`=1, no `GGML_Q5_K`=13), mirroring `ggml-quants.c @ a957b7747` (`dequantize_row_q5_0/q8_0/q4_K/q6_K`, `get_scale_min_k4`); block table 256/144 Q4_K, 32/22 Q5_0, 32/34 Q8_0, 256/210 Q6_K, 1/4 F32 | `gradus/src/model/dequant.fab` |
| The `qwen35moe` target (MODEL-04) storage union is `{F32, BF16, Q4_K, Q5_K, Q6_K, Q8_0}` — BF16 on `blk.N.ffn_gate_inp{,_shexp}.weight` at layer 40, Q5_K on `blk.N.ffn_down_exps.weight` across 38 layers (Q6_K on blk.34/38/39) — a subset of the LIB-03 union `{F32, BF16, Q5_0, Q8_0, Q4_K, Q5_K, Q6_K}`. **BF16 and Q5_K are outside A7's dense-row set** and are the EXEC-02/M5 block-extension frontier (§2, §14) | `docs/factory/production-ml-library/pml5-gguf-m2-moe-router-micro-units.md` §storage union (lines 106–120); `radix/docs/factory/gpu-production-readiness/CAMPAIGN.md` line 91 |
| `QuantizedTensorLayout` is the sole admitted quantized storage contract: purely descriptive, no payload bytes, `RepackIdentity::Native` is the admitted layout, `Declared(RepackHash)` is a disclosed deviation; resolves per-tensor block geometry + absolute byte range fail-closed | `radix/crates/faber-prefill-oracle/src/quantized_tensor_layout.rs` |
| Weight-consuming op families (gather, quantized_matmul, logits_head) are currently `supported_with_explicit_conversion(candidates=[declared_f32_conversion, direct_native])`; the base record's `backend`, `persistence_policy`, `executable_compatibility` fields are `pending_second_representation` | `radix/docs/factory/gpu-inference-gguf/evidence/gi3-representation-record.json` (+ per-backend `-metal.json`, `-cuda.json`) |
| Pure-compute families (rms_normalization, rope, causal_masked_softmax, silu_composition) are `supported_direct` on frozen GI3-1 recipe surfaces and executed on both backends in GI3 | `gi3-contract.md`, `gi3-representation-record-metal.json`, `-cuda.json` |
| GI3-5 executed a 5188-kernel SmolLM2 prefill program on ONE `SingleRun` session on burgus Metal (M5 Max, Metal 4) and pharos CUDA (RTX 5070, CUDA 13.2, sm_120) with the declared-F32 weight representation; prompt-final logits pass the frozen Q2 decision | `docs/factory/gpu-inference-gguf/evidence/gi3-evidence-burgus-metal.md`, `gi3-evidence-pharos-cuda.md` |
| Metal emitter has F32 tiled matmul and the four direct recipes; no quantized/dequant kernel surface exists in `radix-mir-metal`/`radix-mir-llvm` | `radix/crates/radix-mir-metal/src/emit/matmul.rs`; grep for quantized refs |
| `DeviceProgramLifetime` offers `SingleRun` and `RepeatingStep`; there is no resident/prepared persistent-session lifetime yet. **Resolved (2026-08-14, planner-35 per audit 25c92833 F2)**: the persistent variant is a **Radix-owned prerequisite seam** (`GGUF-A7-P1`, §6) — frozen in the U1 contract freeze, landed before U2/U3 dispatch; Hosts supplies the physical residency binding it composes with | `radix/crates/radix-mir/src/device_program/types.rs` |
| Hosts admits exactly two backends: Metal (Apple, M5 Max, burgus) and CUDA (NVIDIA, RTX 5070, pharos); physical device hosts exist (`metal_host.rs`, `cuda_host.rs`, `device_host.rs`) | `hosts/crates/host-coordinator/src/backend.rs`; `hosts/macos-arm64/src/` |
| Q2 numeric decision: `Q2_ENVELOPE` 6.5e-3 (frozen `faber-runtime/src/prefill.rs`), top-1 exact over non-EOG {0,2}, finite gate, first-divergence rule | `gi3-contract.md` §4A |
| Pinned comparator: Homebrew llama.cpp 10150, commit `dee2a846b`, binary SHA-256 `e5c153a1…4952a`, Metal on burgus; extended by later units to the Qwen2.5 rows under the same comparison policy | `docs/factory/gpu-inference-gguf/gi0-comparator-contract.md` |
| Corpus identities (A1b guarded inspection): all four mandatory artifacts present locally | `gradus/exempla/gguf-inspect/README.md`; `ls /Users/ianzepp/ai/models/` |

## 4. Completion Contract (A7 executed outcome)

**Done when** (authority `pml5-general-gguf-delivery.md` §GGUF-A7):

1. The three dense reference rows execute through native packed kernels on
   **both** Metal (burgus) and CUDA (pharos) without whole-model expansion.
2. Every executed weight tensor uses `RepackIdentity::Native`; no tensor in
   the executed path is host-widened to F32 before upload.
3. Per-tensor on-device block dequant output is bit-exact against
   `gradus:model/dequant` at the first-divergence boundary; full-row prefill
   logits pass the frozen Q2 decision against the CPU reference (GI2-3 golden
   for SmolLM2; Gradus GGUF-A6 CPU reference receipts for the Qwen2.5 rows).
4. Autoregressive decode runs on-device with the model resident; a second
   prompt re-enters the same admitted session with no per-token model reload,
   recompile, or full host round-trip (the **dense-row** residency substrate,
   via the `GGUF-A7-P1` persistent `DeviceProgramLifetime` variant, §6;
   GGUF-M5 consumes it only after the EXEC-02 block-extension frontier adds
   BF16/Q5_K — §2). Dense-row decode is bounded (≥ 32 tokens); the 256-token
   two-prompt persistent proof for `qwen35moe` is GGUF-M5/EXEC-03 scope.
5. The capability records flip the weight-consuming families to
   `supported_direct(direct_native)` for the executed class set, with
   `backend`, `persistence_policy`, and `executable_compatibility` populated
   and no field left `pending_second_representation` for an executed family.
6. Receipts record the campaign §Validation list: exact command + cwd; Gradus,
   Radix, Hosts (and Faber, where used) revisions; model filename, byte length,
   SHA-256; storage types + kernel/package identities + model-state capacity;
   hardware/OS/driver/backend; load/prefill/decode/total timing, throughput,
   peak memory; reload/recompile/rebuild/round-trip counters; reset, reuse,
   teardown facts; comparison policy + first divergence.

**Milestone advanced**: Q3 (persistent native execution) — A7 is the
**dense-row** kernel + residency substrate Q3's A7/M5 receipts gate on; the
`qwen35moe` block-extension frontier (BF16/Q5_K) remains EXEC-02/M5-owned
(§2, §14). **Unit completion is not campaign completion**: this artifact
closes nothing; the campaign remains open until `CLOSE-01` accepts both
capstone receipts. Each A7 unit adds one executed proof toward Q3; none
satisfies an invariant clause by itself.

## 5. Scope Closure and Named Split Boundary

- **A7 ↔ M5/EXEC-03**: A7 = dense rows native packed + dense-row resident
  re-entry. M5/EXEC-03 = `qwen35moe` persistent Metal + CUDA execution (256
  tokens, two prompts, KV+SSM retention), GGUF-M4 output consumed. Between
  them sits the **EXEC-02 block-extension frontier**: the BF16 + Q5_K layouts
  that A7's dense-row substrate, dequant oracle, and layout contract do not
  admit must be added (layout contract + oracle + native kernels) before M5
  can consume this substrate. A7 must leave every successor mandatory through
  CLOSE-01.
- **A7 ↔ A3/A4/A5/A6**: A7 consumes packed storage/materialization (A3), dense
  primitives (A4), KV prefill/decode (A5), and dense-row CPU reference
  receipts (A6). A7 units must not implement or re-prove reference semantics.
- **Cross-repo split**: Gradus owns layout/op requirements and the reference
  dequant oracle; Radix owns lowering + kernels + `DeviceProgram`; Hosts owns
  physical storage, residency, launch, sync, teardown; Faber owns composition
  only where a public package command is required (not in A7 units).
- **Per-unit split**: contract freeze (U1) → Metal proof (U2) → CUDA proof
  (U3) → remaining dense rows (U4) → qualification + handoff (U5). No unit
  narrows, downgrades, defers, or makes optional any other A7 unit or any
  successor.

## 6. Ordered Unit Graph

Predecessor chain (execution order, owned by Gradus delivery):
`GGUF-A1c → GGUF-A2 → GGUF-A3 → GGUF-A4 → GGUF-A5 → GGUF-A6 → GGUF-A7`.
A7 units U2–U4 execute only after the reference machinery they consume has a
receipt (A6 dense-row CPU receipts; GI2-3 golden already exists for SmolLM2).

```text
GGUF-A6 dense-row CPU reference receipts
  -> A7-U1 native packed execution contract (cross-repo freeze)
       -> A7-P1 persistent DeviceProgramLifetime variant (Radix prerequisite)
            -> A7-U2 Metal native packed kernels + SmolLM2 proof (burgus)
            -> A7-U3 CUDA native packed kernels + SmolLM2 proof (pharos)
                 -> A7-U4 remaining dense rows native (Qwen2.5-0.5B + 1.5B), both backends
                      -> A7-U5 A7 qualification + substrate handoff
                           -> GGUF-M5 persistent Metal + CUDA execution (successor)
                                -> GGUF-M6 Faber capstone and closeout (successor)
                                     -> CLOSE-01 (successor, campaign end)
```

P1 is a prerequisite seam, not an executed A7 proof: it lands the persistent
`DeviceProgramLifetime` variant so U2/U3 consume a frozen lifetime and never
redesign the semantic program (audit 25c92833 F2 resolution). U2 and U3 are
disjoint by backend and may run in parallel once U1 and P1 land; U4 consumes
both; U5 consumes U4.

### A7-U1 — Native packed execution contract (cross-repo interface freeze)

| Field | Value |
| --- | --- |
| `id` | `GGUF-A7-U1` |
| `outcome` | One frozen cross-repo contract joining (a) Gradus packed layout + semantic operation requirements, (b) Radix native-kernel lowering surface, and (c) Hosts physical storage/residency/launch requirements for the dense-row native path. Capability records flip weight-consuming families to `supported_direct(direct_native)` for the executed class set with S1 descriptor fields populated. First failing oracle: any record field or block-layout fact that contradicts the frozen authorities (`QuantizedTensorLayout`, `gradus:model/dequant` block table) fails closed instead of drifting. |
| `write_scope` | gradus: `docs/factory/production-ml-library/` (this contract + record updates); `src/model/dequant.fab`/`.proba` only if a layout accessor is provably missing (expect none). radix: `crates/faber-prefill-oracle/src/quantized_tensor_layout.rs` (capability/`direct_native` variants + S1 descriptor fields if absent), `crates/faber-prefill-oracle/src/*_test.rs`, `docs/factory/gpu-inference-gguf/` evidence records (new `gi3-representation-record-a7.json` or in-place additions). hosts: `docs/factory/` storage/residency contract note; `crates/host-coordinator` types only if the capability result must cross the host boundary. |
| `read_scope` | gradus `src/model/dequant.fab`, `src/model/gguf_manifest.fab`; radix `gi0-comparator-contract.md`, `gi3-contract.md`, `gi3-delivery.md`, `gi3-representation-record*.json`; hosts `crates/host-coordinator/src/backend.rs`. |
| `done_when` | Contract + records committed; gradus `./scripta/check-source` and `./scripta/check-compile` exit 0; `cargo test -p faber-prefill-oracle` green; the record states exactly one tri-state result per dense-row family with `direct_native` selected and `backend`/`persistence_policy`/`executable_compatibility` populated; first-divergence rule named for every weight family. |
| `validation` | `cd gradus && ./scripta/check-source && ./scripta/check-compile`; `cd radix && cargo test -p faber-prefill-oracle`; `git diff --check` on all touched paths. |
| `depends_on` | none (contract precedes kernels); consumes GI3 contract/records. |
| `non_goals` | No device run; no new MIR ops; no kernel emitter changes; no main-branch push; no GGUF-M5 scope (no `qwen35moe`). |
| `risk` | low — docs + record types; drift risk contained by freezing names. |

### A7-P1 — Persistent `DeviceProgramLifetime` variant (Radix prerequisite)

| Field | Value |
| --- | --- |
| `id` | `GGUF-A7-P1` |
| `outcome` | One Radix-owned semantic-program prerequisite: a resident/prepared persistent `DeviceProgramLifetime` variant (or a proven composition of `SingleRun` + host residency) that keeps the device program resident across decode steps and a second prompt with no reload, recompile, or full host round-trip, plus the Hosts physical residency binding (packed byte ranges retained across steps within the admitted session) it composes with. Owner: **Radix** — resolved 2026-08-14 per audit 25c92833 F2 (was Open Question #3); U2/U3 consume it frozen and do not redesign the semantic program. |
| `write_scope` | radix: `crates/radix-mir/src/device_program/` (lifetime variant + program assembly), `crates/faber-prefill-oracle/` (program-builder arm selecting the persistent lifetime) only where the builder must surface it; hosts: `crates/host-coordinator/` or `macos-arm64/src/` residency binding only if the physical retention route must surface there. |
| `read_scope` | radix `gi3-contract.md`, `gi3-delivery.md` §GI3-5 (SingleRun session pattern); hosts `crates/host-coordinator/src/backend.rs`. |
| `done_when` | The persistent variant (or proven composition) exists in `DeviceProgramLifetime`, the A7 program builder selects it, and a Radix-level test proves a program instance survives step boundaries and a second prompt with no reload/recompile/rebuild; Hosts residency binding named; `cargo test -p radix-mir` (or the owning crate) green; `git diff --check` clean. |
| `validation` | `cargo test -p radix-mir` (or owning crate); `git diff --check`; no device run required (the physical residency proof is U2/U3 scope). |
| `depends_on` | `GGUF-A7-U1` (freezes the contract the variant must satisfy). |
| `non_goals` | No kernel emitter work; no `qwen35moe`; no persistent KV/SSM state (M5/EXEC-03); no whole-model F32 expansion; no Faber product surface. |
| `risk` | medium — semantic-program change, but bounded to one Radix-owned type landed before any device unit; mitigated by freezing it at U1. |

### A7-U2 — Metal native packed kernels + SmolLM2 dense-row proof (burgus)

| Field | Value |
| --- | --- |
| `id` | `GGUF-A7-U2` |
| `outcome` | Radix lowers native packed kernels (block-dequant-fused matmul for Q4_K/Q5_0/Q6_K/Q8_0; Q8_0 gather; quantized logits head; existing direct recipes unchanged) and Hosts supplies the burgus Metal physical route (packed byte ranges → device buffers, no whole-model F32 expansion, resident weights). SmolLM2-360M Q4_K_M (290 tensors: 16 Q4_K + 176 Q5_0 + 16 Q6_K + 17 Q8_0 + 65 F32) executes prefill + ≥32-token decode on burgus Metal in one admitted session with a second-prompt re-entry via the `GGUF-A7-P1` persistent lifetime; per-block dequant bit-exact vs `gradus:model/dequant` at first divergence; prefill logits pass the Q2 decision vs the GI2-3 golden. |
| `write_scope` | radix: `crates/radix-mir/` (new recipe/plan variants for native quantized matmul + block dequant, `kernel_plan.rs`), `crates/radix-mir-metal/src/emit/` (quantized kernel emitters), `crates/faber-prefill-oracle/` (native repack selection + program builder arm), `crates/radix-mir-metal/src/emit/tests/`; hosts: `macos-arm64/src/metal_host.rs` + `macos-arm64/tests/` (env-gated device proof test), `crates/host-coordinator/` if the upload/residency route must surface there; faber: none expected (proof-test pattern). |
| `read_scope` | gradus `src/model/dequant.fab` + `radix/docs/factory/gpu-inference-gguf/evidence/gi2-dequant-goldens.json` + `gi2-3-logits-golden` (read-only); radix `gi3-delivery.md` §GI3-5 runner + `gi3-representation-record-metal.json`; hosts `crates/host-coordinator/src/backend.rs`. |
| `done_when` | burgus Metal native receipt exists with all §4 clause-6 facts; no tensor host-widened; dequant first-divergence receipt names tensor + block index (or reports exact match); Q2 decision PASS on prefill logits; decode tokens match the CPU reference; second-prompt re-entry in one session (via the `GGUF-A7-P1` persistent lifetime) with no reload/recompile/rebuild/round-trip; peak memory + timing recorded. |
| `validation` | Env-gated proof test on burgus (pattern: `cargo test --release ... device_run` per GI3-6 evidence); comparison JSON written to the evidence dir and committed copy; `cargo test -p radix-mir-metal`; `git diff --check`. |
| `depends_on` | `GGUF-A7-U1`, `GGUF-A7-P1`; reference machinery A3/A4/A5/A6 receipts (CPU side). |
| `non_goals` | CUDA (U3); Qwen2.5 rows (U4); `qwen35moe` (M5); F32 expansion of any tensor; changing the CPU reference semantics; new quantized storage authority outside `QuantizedTensorLayout`. |
| `risk` | high — device-kernel correctness, MSL emitter surface, residency accounting. |

### A7-U3 — CUDA native packed kernels + SmolLM2 dense-row proof (pharos)

| Field | Value |
| --- | --- |
| `id` | `GGUF-A7-U3` |
| `outcome` | Same executed outcome as U2 on pharos CUDA through the NVVM path (`radix-mir-llvm`, PTX `sm_120`, `cuModuleLoadData`) and the pharos CUDA host route. Same class set, same Q2 decision, same receipt facts, same residency re-entry. |
| `write_scope` | radix: `crates/radix-mir-llvm/src/` (NVVM quantized kernel emitters + plan agreement), `crates/radix-mir/` shared plan types only where not already landed by U2 (U2/U3 write disjoint files — see dependency note), `crates/faber-prefill-oracle/` shared builder only if U2/U3 require identical edits (then sequence: U2 first); hosts: `macos-arm64/src/cuda_host.rs`, `cuda_launch_adapter.rs`, `macos-arm64/tests/cuda_host_proof.rs` (env-gated proof). |
| `read_scope` | gradus dequant + goldens; radix `gi3-evidence-pharos-cuda.md` + `gi3-representation-record-cuda.json`; hosts `crates/host-coordinator/src/backend.rs`. |
| `done_when` | pharos CUDA native receipt with all §4 clause-6 facts; no host-widened tensor; dequant first-divergence receipt (or exact match); Q2 decision PASS; decode tokens match the CPU reference; second-prompt re-entry resident (via the `GGUF-A7-P1` persistent lifetime); peak memory + timing recorded. |
| `validation` | Env-gated proof test on pharos over SSH (`pharos.ianzepp.net`, passwordless; pattern: GI3-7 evidence); committed comparison record; `cargo test -p radix-mir-llvm`; `git diff --check`. |
| `depends_on` | `GGUF-A7-U1`, `GGUF-A7-P1`; reference machinery A3/A4/A5/A6. Parallel-safe with U2 only on disjoint file sets (mirror the GI3-3/GI3-4 one-writer-per-file rule). |
| `non_goals` | Metal (U2); Qwen2.5 rows (U4); `qwen35moe` (M5); F32 expansion; changing CPU reference semantics. |
| `risk` | high — NVVM emitter surface, plan agreement, driver/runtime versioning. |

### A7-U4 — Remaining dense rows native (Qwen2.5-0.5B + 1.5B), both backends

| Field | Value |
| --- | --- |
| `id` | `GGUF-A7-U4` |
| `outcome` | `Qwen2.5-0.5B-Instruct-Q4_K_M.gguf` (290 tensors) and `Qwen2.5-1.5B-Instruct-Q4_K_M.gguf` (338 tensors) execute natively on both backends through the same adapter with no special-case constants. Per-row per-tensor storage manifests inventoried against the GGUF-A1b independent reader; prefill logits + bounded decode pass the Q2 decision vs the Gradus CPU reference receipts (A6). |
| `write_scope` | radix: `crates/faber-prefill-oracle/` (row-manifest handling only where a real difference requires it), `docs/factory/gpu-inference-gguf/` evidence records (per-row receipts); hosts: `macos-arm64/tests/` (row proof tests). No kernel emitter changes unless a real per-row storage class difference is inventoried (then the owning emitter unit owns it). |
| `read_scope` | gradus `exempla/gguf-inspect/README.md` (row identities); `llama-gguf` independent inventory output; A6 CPU reference receipts. |
| `done_when` | Both Qwen2.5 rows native on Metal and CUDA, receipts with all §4 clause-6 facts; no special-case constants (any per-row constant must be a declared architectural fact with a divergence receipt); storage manifests committed in the evidence records; Q2 PASS vs CPU reference. |
| `validation` | Env-gated row proof tests on burgus + pharos; committed comparison records; `git diff --check`. |
| `depends_on` | `GGUF-A7-U2`, `GGUF-A7-U3`, A6 CPU reference receipts. |
| `non_goals` | `qwen35moe` (M5); SmolLM2 re-proof; universal model support. |
| `risk` | medium — scale independence and per-row storage variance. |

### A7-U5 — A7 qualification + substrate handoff

| Field | Value |
| --- | --- |
| `id` | `GGUF-A7-U5` |
| `outcome` | The complete A7 receipt set is consolidated: correctness, memory, timing, backend identity, fail-closed capability evidence, no-whole-model-expansion proof, resident re-entry across decode + second prompt for all three dense rows on both backends. Support matrix, symbol inventory, regression inventory, and capability records describe the observed result exactly; the handoff gate to GGUF-M5/EXEC-03 is written with every successor preserved through CLOSE-01. |
| `write_scope` | gradus: `docs/factory/production-ml-library/` (support matrix, symbol inventory, regression-corpus totals, A7 closeout note); radix: `docs/factory/gpu-production-readiness/` evidence + campaign status edit only via the normal campaign-update path, `docs/factory/gpu-inference-gguf/` evidence records; hosts: `docs/factory/` backend capability note. |
| `read_scope` | all U1–U4 receipts + evidence records. |
| `done_when` | A7 qualification note committed naming each unit receipt + commit; support matrix/symbol inventory updated; no executed-family capability field left pending; handoff gate section names M5/EXEC-03 as the first frontier, the **BF16 + Q5_K block-extension frontier EXEC-02 must cross** (layout contract + dequant oracle + native kernels) before M5 can consume the dense-row substrate, and every successor id. |
| `validation` | Cross-check each A7 unit's committed receipt against the §4 completion contract; `git diff --check`; inventory counts match committed records. |
| `depends_on` | `GGUF-A7-U4`. |
| `non_goals` | Executing M5 scope; editing campaign authority (ownership); GO stamps. |
| `risk` | medium — documentation drift across three repos; mitigated by one-writer-per-file and the qualification checklist. |

## 7. First Failing Oracle and Comparison Policy

- **Oracle hierarchy** (first hit wins, then report):
  1. On-device block dequant output vs `gradus:model/dequant` (bit-exact;
     mirrors `ggml-quants.c @ a957b7747`) and `gi2-dequant-goldens.json`.
     First divergence names tensor + block index + expected/observed values.
  2. Full prefill logits vs CPU reference: SmolLM2 → GI2-3 logits golden;
     Qwen2.5 rows → Gradus GGUF-A6 CPU reference receipts. Decision is the
     frozen Q2 policy: `Q2_ENVELOPE` 6.5e-3, top-1 exact over non-EOG
     {0,2}, finite gate, first-divergence rule.
  3. Decoded tokens vs CPU reference (bounded, ≥ 32 tokens).
  4. Pinned llama.cpp comparator (Homebrew 10150, `dee2a846b`) for any
     token/logit comparison outside the Gradus reference path; per-row flag
     sets frozen by the owning unit (see Open Questions).
- **Fail-closed**: any unknown GGML type, layout contradiction, or capability
  mismatch fails closed with a typed diagnostic; no silent CPU fallback for an
  explicit GPU route (campaign stop condition; GI3 S2).
- **Oracle scope**: the dequant oracle is the first-failing oracle for A7's
  dense-row closed set only. BF16 and Q5_K (MODEL-04 layouts) are outside
  that set and outside the oracle; the EXEC-02/M5 block-extension frontier
  must extend the oracle (and the layout contract and native kernels) before
  `qwen35moe` execution can be compared (§2, §14).

## 8. Local Corpus Boundary

Operator-local evidence at `/Users/ianzepp/ai/models/` — read-only, never
committed. A7 executes only the three dense rows:

| Artifact | Architecture | Tensors | SHA-256 | Role |
| --- | --- | ---: | --- | --- |
| `SmolLM2-360M-Instruct-Q4_K_M.gguf` (270,590,880 B) | `llama` | 290 | `2fa3f013…bac9c2` | dense reference rung (U2/U3) |
| `Qwen2.5-0.5B-Instruct-Q4_K_M.gguf` (397,808,192 B) | `qwen2` | 290 | `6eb923e7…8c8653` | dense Qwen rung (U4) |
| `Qwen2.5-1.5B-Instruct-Q4_K_M.gguf` (986,048,768 B) | `qwen2` | 338 | `1adf0b11…6c3370` | scale-independence rung (U4) |
| `Qwen3.6-35B-A3B-UD-Q4_K_M.gguf` (22,663,387,424 B) | `qwen35moe` | 753 | `0b21525e…7dac58b` | **not** A7 scope — M4/M5 |

Dense-row storage classes are the closed `{F32, Q5_0, Q8_0, Q4_K, Q6_K}` set
(SmolLM2 record). U4 inventories each Qwen2.5 row's per-tensor manifest before
execution; any dense row containing a class outside the closed set fails
closed and routes to the owning admission unit. The `qwen35moe` layouts
**BF16** (layer-40 router gates) and **Q5_K** (`ffn_down_exps`) are known to
be outside this dense-row set: they fail closed here by design and are the
EXEC-02/M5 block-extension frontier (§2, §14). A7 does not admit them, does
not silently skip them, and EXEC-02 retains ownership of every packed kernel
including these two.

## 9. Hardware / Backend Authority

| Machine | Backend | Device | Toolchain |
| --- | --- | --- | --- |
| `burgus` | Metal | Apple M5 Max, Metal 4, macOS 25.5.0 (kernel xnu-12377; `hw.model` Mac17,7) | MSL via `metal_text` probe path (GI3-6 pattern); Homebrew llama.cpp 10150 (`dee2a846b`) comparator |
| `pharos` | CUDA | NVIDIA RTX 5070, driver 595.71.05, CUDA 13.2, compute capability 12.0 (`sm_120`) | clang NVPTX 18.1.3 (Ubuntu), PTX via `cuModuleLoadData` (GI3-7 pattern); passwordless SSH `pharos.ianzepp.net` |

No other backend is admitted for A7. No unapproved paid infrastructure.

## 10. Estimates (per Hand-packet convention)

| Unit | est_work_tokens | est_basis | tool_latency |
| --- | --- | --- | --- |
| U1 contract freeze | 2–3k | `rivus-docs-note` (doc+record heavy; ledger avg 38 calls) blended with `diagnostics-oracle` | gradus `check-source`/`check-compile` ~1–3 min each; `cargo test -p faber-prefill-oracle` ~2–5 min |
| U2 Metal proof | 8–12k | `compiler-surface-feature` (ledger avg 147, max 304 tool calls) — device kernel + emitter surface | radix crate builds ~2–5 min incremental / 10–20 min cold; burgus device run ~1–3 min incl. build |
| U3 CUDA proof | 8–12k | `compiler-surface-feature` (same class) | radix-mir-llvm builds ~2–5 min incremental; pharos run via SSH ~1–5 min (remote driver/deps already proven) |
| U4 remaining rows | 5–8k | `compiler-surface-feature` (row adaptation, not new kernel surface) | row proof runs ~1–3 min per backend; `llama-gguf` inventory ~seconds |
| U5 qualification | 3–5k | `diagnostics-oracle` (verification/records) | git + doc checks only; no device runs required |

`est_basis` class names refer to `.tugboat/estimate-ledger.json`; ranges are
planning guidance, actuals get recorded at each unit's closeout.

## 11. Checkpoints and Gates

1. **U1 gate (pre-kernel)**: contract + records committed; check-source /
   check-compile / faber-prefill-oracle green. Blocking: a record field that
   cannot state `direct_native` for an executed family → re-freeze contract.
2. **U2/U3 gates**: per-backend device receipt with §4 clause-6 facts and the
   Q2 decision PASS; no whole-model F32 expansion anywhere (a proof-test-time
   assertion, not a policy note).
3. **U4 gate**: both Qwen2.5 rows native on both backends, no special-case
   constants; per-row manifests committed.
4. **U5 gate**: A7 qualification note; every successor id preserved through
   CLOSE-01; handoff frontier named.
5. **Stop conditions** (campaign §Stop Conditions): target identity mismatch;
   required architecture fact unrepresentable; oracle missing; a unit lacking
   an executable done oracle; public Gradus API acquiring device ownership;
   unapproved paid infrastructure. Block the affected edge only; continue
   unaffected ready units.

## 12. Validation Summary

- gradus: `./scripta/check-source`, `./scripta/check-compile`, `git diff --check`.
- radix: `cargo test -p faber-prefill-oracle`, `-p radix-mir-metal`,
  `-p radix-mir-llvm`; `git diff --check`.
- Device: env-gated proof tests on burgus (Metal) and pharos (CUDA) with
  committed comparison records, per the GI3-6/GI3-7 evidence pattern.
- Records: one writer per evidence file (GI3 F2 rule); `git diff --check`
  before every closeout.
- No per-operation host recomputation; no llama.cpp in the executed A7 path
  (comparator is oracle-side only).

## 13. Open Questions for Mind

1. **A7 runner home**: the GI3-era device runner lived in the external
   `faber-runtime` repo (not a member of this packet). A7 assumes the runner
   pattern lands as env-gated proof tests under `hosts/macos-arm64/tests/`
   (Metal) and the existing `cuda_host_proof.rs` (CUDA), with program building
   in radix `faber-prefill-oracle`. If Mind assigns a different runner home
   (e.g., a Faber package seam), U2/U3 write scopes shift accordingly.
2. **llama.cpp comparator pin for Qwen2.5 rows**: the pinned comparator
   (10150/`dee2a846b`) is frozen for the SmolLM2 row only. Per-row flag sets
   and any revision bump for the Qwen2.5 rows are frozen by the owning
   tokenizer/reference units (GGUF-A2/A6); A7 consumes the pin, it does not
   set it. Confirm the A7 receipt may cite the Gradus CPU reference as oracle
   without re-pinning llama.cpp per row.
3. **DeviceProgram resident lifetime — RESOLVED (2026-08-14, planner-35 per
   audit 25c92833 F2)**: the persistent `DeviceProgramLifetime` variant is a
   **Radix-owned prerequisite seam** (`GGUF-A7-P1`, §6) — frozen in the U1
   contract freeze and landed before U2/U3 dispatch. U2/U3 consume it frozen
   and never redesign the semantic program; Hosts supplies the physical
   residency binding it composes with. Owner recorded; no longer an open
   question.
4. **Peak-memory disclosure**: native packed uploads are materially smaller
   than F32 conversion (SmolLM2 packed ≈ 136 MB vs ≈ 540 MB F32); the receipt
   must record packed-resident bytes and any workspace explicitly. Confirm the
   memory baseline format matches the campaign §Validation list before U2.

## 14. Successors Preserved Through CLOSE-01

This delivery lowers A7 only. It preserves, unmodified in scope and
mandatory in status: GGUF-M5, GGUF-M6 (gradus delivery); campaign EXEC-01,
EXEC-02, EXEC-03, CAP-01, CAP-02, CLOSE-01 (radix campaign); and every other
unimplemented GGUF-A/GGUF-M unit. None of them is narrowed, downgraded,
deferred, made optional, or moved outside the campaign by this artifact.

**Block-extension frontier (named, not crossed)**: A7's substrate is
dense-row-scoped — its layout contract (`QuantizedTensorLayout`), dequant
oracle (`gradus:model/dequant`), and native kernels cover `{F32, Q5_0,
Q8_0, Q4_K, Q6_K}` only. The `qwen35moe` target (MODEL-04) requires `{F32,
BF16, Q4_K, Q5_K, Q6_K, Q8_0}`; **BF16** (layer-40 router gates) and **Q5_K**
(38 layers of `ffn_down_exps`) are outside A7's set and are the EXEC-02/M5
block-extension frontier. EXEC-02 (Radix; `radix/docs/factory/
gpu-production-readiness/CAMPAIGN.md` line 91) owns the full kernel set
including BF16 and Q5_K and must extend the layout contract, the dequant
oracle, and the native kernels before GGUF-M5 can consume this substrate. A7
declares this frontier and preserves EXEC-02/M5's mandate to cross it,
unmodified.
