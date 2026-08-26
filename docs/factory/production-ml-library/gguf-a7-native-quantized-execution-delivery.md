# Delivery: GGUF-A7 — Native Quantized Execution Contract

**Status**: active — U2 landed and folded to radix main (`f9d65f7b8` ← `356e5edaa`: Q4_K_M SmolLM2 native Metal receipt, MATCH — prefill top-1 exact, decode max_delta 0.0, 128-step resident session, no F32 expansion); U3 filed honest NOT ATTEMPTED, pharos unreachable (lane `60ec5d28e`, fold queued; recheck = machine answers SSH); U4a/U4b/U5 blocked on U3 recheck (operator mailed `5797807b`); Metal side unaffected
**Campaign**: [`radix/docs/factory/gpu-production-readiness/CAMPAIGN.md`](../../../../radix/docs/factory/gpu-production-readiness/CAMPAIGN.md), mandatory work **A7 — native quantized execution contract**
**Semantic delivery authority**: [`pml5-general-gguf-delivery.md`](pml5-general-gguf-delivery.md) §§GGUF-A7 and GGUF-M5
**Planner**: planner
**Assignment handle**: `b236d1c9`
**Re-lowering authority**: operator direction 2026-08-26 ~21:3xZ; parallel-format track; GPU law `e7ae4be9`
**Verified repo tips**: Radix `4c8696ab7`; Gradus `de687a4d2`; Hosts `c1f9fd1e`
**Integration stop**: ordinary main checkouts for this delivery; no worktree or merge-lane claim is made by this artifact

## 1. Interpreted theme / problem

GGUF-A7 makes the campaign's “quantized means native” posture executable for
the three dense Q4_K_M reference rows. The required result is native packed
execution on Metal and CUDA without a whole-model F32 expansion, with the
correctness, memory, timing, backend, residency, and fail-closed evidence
needed by GGUF-M5.

The earlier lowering described this as a from-scratch kernel delivery. That
part is no longer true. The current Radix tree already contains the packed
layout admission, `QuantizedMatMul`/`QuantizedGather` plan surface, Metal and
NVVM per-format bodies, and the dense packed comparison/memory harness. The
remaining A7 work is the real dense-row execution receipts, the missing 1.5B
harness row, and qualification. No A7 unit should re-implement a landed
packed body or create a second execution route.

Ownership remains split:

- Gradus owns device-neutral model semantics, GGUF storage facts, and the
  Faber dequant/reference surface.
- Radix owns typed layout consumption, plan lowering, and target artifacts.
- Hosts owns physical allocation, packed residency, launch, synchronization,
  readback, and teardown.
- Faber owns package/build/run composition. A7 does not add a public product
  surface.

## 2. Goal-check — READY

| Field | Value |
| --- | --- |
| `goal_path` | `gradus/docs/factory/production-ml-library/pml5-general-gguf-delivery.md` §GGUF-A7, with this delivery as the executable lowering |
| `evaluator_mode` | goal-check during delivery re-lowering, 2026-08-26 |
| `consumer` | delivery; Mind dispatches the active cross-repo units |
| `verdict` | **READY** — gated at the named live-seat and model-machine boundaries |

**Reasoning.** The desired end state, ownership boundary, dense corpus, native
format set, completion oracle, and successor chain are concrete. The packed
implementation substrate is already present in live code, so the corrected
plan can lower proof and qualification work without inventing a kernel or
session ABI. The physical dense receipts and the 1.5B parameterization remain
unlanded. Those are execution gates, not missing architecture decisions.

**Key points.**

- Q4_K_M is the first and only A7 storage family. It is the small-row proof
  instrument for the later Qwen3.6 35B Q4_K_M capstone memory gate.
- `R-PACK-02` is the current packed kernel substrate. A7 consumes it; A7 does
  not duplicate it.
- The GEA3 independent scalar F32 oracle and its comparator leg are the
  model-level reference for the SmolLM2 identity. The committed GEA3 physical
  zero-readback finding is not a pass and must not be copied as one.
- The current packed harness has SmolLM2 and Qwen2.5-0.5B rows only. The
  Qwen2.5-1.5B row therefore remains a real lowering unit.
- The old `DeviceProgramLifetime` prerequisite is superseded by the landed
  Hosts prepared-resident-session composition. A7 does not add a new lifetime
  enum variant.

**Blocking gaps at the planning boundary:** none. Active units carry explicit
entry and dispatch gates for NR-2, PPB-U1, GEA4 admission, A6/reference
receipts, and the named 35B CUDA memory authority. A gate may block its own
edge without being hidden as a general readiness gap.

**Recommended next step:** Mind dispatches A7-U2 and A7-U3 after the listed
GEA4/NR-2/PPB-U1 scope checks; then dispatches A7-U4a, A7-U4b, and A7-U5 in
order.

## 3. Normalized spec

The A7 outcome is:

> The SmolLM2-360M, Qwen2.5-0.5B, and Qwen2.5-1.5B Q4_K_M rows execute their
> dense prefill and bounded autoregressive decode through native packed GGML
> blocks on the admitted Metal and CUDA routes, with no whole-model F32
> expansion. Their receipts prove native storage identity, per-block
> dequantization, model-level logits/tokens, resident weight reuse, lifecycle
> counters, timing, peak memory, backend identity, and fail-closed behavior.

The execution order is Q4_K_M first. The small rows are not a claim that the
35B capstone fits on every machine. The exact Qwen3.6-35B-A3B-UD-Q4_K_M row is
22,663,387,424 bytes and remains the later EXEC-02/GEA4/EXEC-03 capstone
memory gate. Pharos's 12 GB RTX 5070 is not an admissible substitute for that
row; the CUDA capstone needs the named operator-authorized large-memory
machine, currently recorded as the CAP-02 `>=48 GB` VRAM class.

A7 uses the existing prepared-session composition where a two-prompt proof is
run: `RepeatingStep` plus once-initialized `PerProgram` weights, per-step token
inputs, retained device state, prompt-scoped reset, and explicit release.
A7 does not introduce a new `DeviceProgramLifetime` variant. The 256-token,
two-prompt Qwen3.6 persistent proof remains GGUF-M5/EXEC-03/CAP-01/CAP-02
scope.

## 4. Goal and compiler re-baseline

The previous baseline was dated 2026-08-13 and is retired. The following facts
were checked against today's current main tips and named landings.

| Current fact | Live evidence | Effect on A7 |
| --- | --- | --- |
| Gradus dequant now admits `{F32, F16, BF16, Q5_0, Q8_0, Q4_K, Q5_K, Q6_K}`. `GgmlKind`, `admit_kind`, `block_elements`, `block_bytes`, `dequantize_block`, and `dequantize_order` are live; the block table includes Q4_K 256/144, Q5_K 256/176, Q6_K 256/210, Q5_0 32/22, and Q8_0 32/34. | `gradus/src/model/dequant.fab:4-6,23-47,78-114,478-545,550-573` | The old claim that BF16 and Q5_K were outside the dequant oracle is false. A7 still scopes its dense proof to the three rows, but the M5/Qwen35 block frontier now consumes an existing Gradus oracle rather than inventing one. |
| Radix has the typed packed plan and dequant resolution. `PackedDequantKind` distinguishes native F16/BF16 conversion, block, and superblock paths; `PackedDequantResolution` is derived from `PackedStorageLayout`; `admit_quantized_matmul` and `admit_quantized_gather` fail closed on unknown layouts. | `radix/crates/radix-mir/src/kernel_plan/packed.rs:1-18,25-60,71-129,132-221` | The old U1 contract-freeze and U2/U3 “new plan variant” work is superseded by the landed R-PACK-01/02 substrate. Active units prove execution and receipts against these symbols. |
| Native Metal packed matmul exists for F16, BF16, Q5_0, Q8_0, Q4_K, Q5_K, and Q6_K, with block/superblock dequant inside the emitted body. | `radix/crates/radix-mir-metal/src/emit/quantized_matmul.rs:1-5,16-90`; current main history includes `1286439e1`, `0cb75ab7e`, `16840c893`, `d02d58554`, and `c34479e4f` | A7 must not add a second Metal emitter or claim that no quantized emitter exists. U2 is a Metal execution receipt over the landed body. |
| Native NVVM packed matmul dispatch exists through `emit_kernel_quantized_matmul_call`; the NVVM surface has F16/BF16/Q5_0 bodies and dispatches Q8_0/Q4_K/Q5_K/Q6_K helpers. | `radix/crates/radix-mir-llvm/src/nvvm/quantized_matmul.rs:19-148,151-180`; `radix/crates/radix-mir-llvm/src/nvvm/quantized.rs:1-5` and current main history | A7 must not add another CUDA emitter. U3 is a CUDA execution receipt over the current NVVM seam. |
| The descriptive file-range authority remains `QuantizedTensorLayout` with `RepackIdentity::{Native,Declared}`. The executable plan consumes the separate `PackedStorageLayout`; the host mirror is `PackedStorageFormat`. | `radix/crates/faber-prefill-oracle/src/quantized_tensor_layout.rs:269-314`; `radix/crates/host-device-core/src/device_descriptor.rs:179-307` | Do not conflate a descriptive GGUF byte-range descriptor with a target plan or a source-level conversion function. Native means no repack in the executed path. |
| GSF-1/2/3 are on Radix main. Symbolic size witnesses are forwarded through semantic typecheck and MIR monomorphization, including `explicit_size_witness_index`, `explicit_shape_witness`, `resolve_parent_shape_binding`, and shape finalization. | `radix/crates/radix-semantic/src/passes/typecheck/generic.rs:150-170,529-552`; `radix/crates/radix-module/src/mir/lower/monomorphize.rs:291-302,514-519,586-590,672-679,1010-1052,1124-1134`; landed `66e0c7884`, `524258de2`, `c1059ebd1` | A7 may use current generic shape forwarding where the route actually does. It must not retain the old SEM008 “cannot forward size arguments” claim or use literal-size workarounds as architecture. This compiler landing does not itself migrate every Gradus caller: the current `gradus/src/model/dense.fab:557-582` REF-01 route still has literal-size assembly. Any new semantic/HIR edit is held by NR-2. |
| N-ary `for from` is a real HIR/MIR family. `itera ex` parses a source series; `IteraLockstep` carries aligned sources/binders; typecheck owns arity and length admission; MIR emits one guarded aligned walk. | `radix/crates/radix-parser/src/stmt.rs:163-234`; `radix/crates/radix-semantic/src/lower/stmt.rs:659-667,769-819`; `radix/crates/radix-semantic/src/passes/typecheck/lockstep.rs:27-32`; `radix/crates/radix-hir/src/nodes.rs:1070-1080`; `radix/crates/radix-module/src/mir/lower/control.rs:2160-2192`; landed `fc05e83b6` | A7's current Gradus `dequantize_order` uses the ordinary one-source `for from` path. A future multi-source kernel/materialization loop must use `IteraLockstep`, preserve equal-length fail-closed behavior, and wait on NR-2. A7 does not lower an ad-hoc range-plus-get substitute. |
| CTR-05/06 retracted destination-owned conversion arms. HIR enums no longer carry `conversion_arms`; FHIR carries `ResolverSnapshot.conversion_rows`; Rust emission generates no `impl From` carrier for registry rows. Only declared `@ conversion` (English) / `@ conversio` (Latin) functions enroll rows. | `radix/crates/radix-semantic/src/lower/decl.rs:884-895`; `radix/crates/radix-hir-fhir/src/artifact.rs:136-139`; `radix/crates/radix-hir-rust/src/decl.rs:1478-1482`; landed `dcd9d30df`, `bc0edfe1f`, `859fd8fba`, repair `19dfb2e6b` | The old `conversion_arms` and destination-enum wording is invalid. A7 must not write or request those fields. `RepackIdentity::Declared` is an execution representation identity and is unrelated to source-level `@ conversion`/`@ conversio` enrollment. |
| DFV2-4/5 now composes device calls and packages canonical device bodies. Device code calls are composed; host-to-entry is the launch boundary; package metadata carries body hashes, compiler/ABI identity, and visibility-gated launch metadata. | `radix/crates/radix-module/src/mir/fragment_composition.rs:1-18,99-113`; `radix/crates/radix-module/src/hir/package.rs:36-45,93-114,241-320,636-709`; landed `fae613683`, `dba1383c8`, `597fcde88` | A7 source/device entries must be a body-bearing role plus visibility entry. No unit may smuggle a helper call through an uncomposed device body or rely on signature-only package artifacts. |
| Visibility is a stacked role plus public marker. English source uses `@ kernel` + `@ public`; Latin/default-reader fixtures use `@ nucleum` + `@ publica`. Bare role annotations are private helpers and are not launch entries. | `gradus/src/kernel.fab:425-427` (`@ kernel` + `@ public`); `gradus/src/model/dequant.fab:78-87,478-489` (`@ public`); `radix/crates/radix-module/src/hir/package.rs:95-100`; landed `b76871947`, `bc03ad301` | Replace the old bare-role assumption. Any new A7 device fixture must use the locale-correct stacked entry markers. A7 does not edit the live GEA4 harness marker family. |
| Closure-environment linking now shifts `MirAggregateKind::ClosureEnvironment`, rewrites body and metadata capture sources, and remaps capture names at both merge sites. | `radix/crates/radix-program/src/mir/lower.rs:742-745,810-815,951-955,1012-1016,2354-2357,2641-2649`; `radix/crates/radix-program/src/mir/sources.rs:60-80`; landed `be730315e`, merge `c36b92a69` | A7 package/device proof must use the current linker and must record a closure-environment mismatch as a compiler/link failure, never repair it with a source or helper workaround. |
| Radix `DeviceProgramLifetime` still has only `SingleRun` and `RepeatingStep`; Hosts already has packed format descriptors and prepared resident sessions. `PreparedResidentSession` composes a `RepeatingStep` session with once-init weights, resident-step token inputs, prompt reset, reuse counts, and release counts. | `radix/crates/radix-mir/src/device_program/types.rs:418-428`; `hosts/crates/host-device-core/src/device_descriptor.rs:179-307`; `hosts/macos-arm64/src/composite_host.rs:571-598`; `hosts/macos-arm64/tests/prepared_session_test.rs:4-14,703-789`; landed `a43a7dd` and current Hosts main | The old A7-P1 new-`DeviceProgramLifetime` prerequisite is superseded. A7 consumes the prepared-session composition; EXEC-03 owns the 35B persistent-session proof. |
| The current dense packed harness has two rows and no device launch in its library unit. It uses versioned `DENSE_PACKED_ENVELOPES_V1`, not the retired `Q2_ENVELOPE`. The existing R-PACK-05a closeout records final Metal prefill/first-continuation rows for both harness rungs, but its CUDA attempts stopped before launch at `dense-qkv-projection-binding`; neither is an A7 resident two-prompt receipt at today's tips. | `radix/crates/faber-prefill-oracle/src/dense_full_model.rs:1-10,39-116,260-380,888-911`; `radix/docs/factory/gpu-production-readiness/evidence/exec02/r-pack-05a-closeout.md`; current main history `8d0ef11a3`, `d7401473b`, `3da984d5d`, `61d109c8f` | U2/U3/U4a consume and re-verify the current harness/receipts. U4b adds the 1.5B manifest/reference row. No unit inherits `Q2_ENVELOPE` or treats `NotAttempted`, a pre-launch blocker, or an old receipt as a current device pass. |

### Provenance of the current tip

- **Radix**: `4c8696ab7` is the current main tip. Today's relevant landed
  sequence includes GSF-1/2/3, DFV2-4/5, CTR-05/06, closure-env repair, the
  GEA3 visibility repair, and the N-ary `itera ex` feature. The NR-2 parser
  follow-up remains a live seat and is not silently treated as landed here.
- **Gradus**: `de687a4d2` is the current main tip. `src/model/dequant.fab`
  has the full eight-kind admitted dequant surface; `src/model/dense.fab`
  and the model materialization exempla are the current source-side facts.
- **Hosts**: `c1f9fd1e` is the current main tip. Packed storage descriptors,
  packed Metal library routes, CUDA host extraction, GEA3 mirrors, and the
  prepared resident-session composition are current. Hosts `macos-arm64` is
  no longer the correct path for the CUDA host implementation; use
  `crates/host-cuda` for that seam.

## 5. Completion contract

A7 is complete only when all of the following are evidenced.

1. The three dense Q4_K_M rows execute native packed prefill and bounded
   decode on Metal and CUDA. The SmolLM2 row is first; Qwen2.5-0.5B follows;
   Qwen2.5-1.5B closes the scale-independence row.
2. Every executed weight tensor retains `RepackIdentity::Native`. No host
   path widens the model to F32 before upload. F32 tensors in a mixed model
   remain their declared F32 storage; “no expansion” forbids converting the
   packed tensors into a second whole-model F32 copy.
3. The first low-level mismatch is a per-block comparison against
   `gradus:model/dequant`, with tensor name, block index, expected bits, and
   observed bits. Unknown format, short block, bad range, and non-finite
   payload fail closed.
4. The model-level comparison uses the landed GEA3 scalar F32 oracle for the
   SmolLM2 identity and the existing independent CPU/comparator references for
   the Qwen rows. The receipt records logits first divergence, token first
   divergence, top-1 policy, finite gate, and the applicable versioned packed
   envelope. No tolerance is widened after observation.
5. The native route keeps packed weights resident over decode steps and, where
   the proof exercises it, over a second prompt with prompt-scoped reset. It
   records module reloads, weight copies, per-program reallocations, reset,
   reuse, and release counters. The Qwen3.6 35B 256-token/two-prompt proof is
   not claimed here.
6. The executed capability/evidence record states the native representation,
   backend, executable compatibility, persistence route, and receipt identity
   using current named rows. It does not use the retracted `conversion_arms`
   representation or a `supported_with_explicit_conversion` row as a native
   pass.
7. Each receipt records exact command and cwd; Gradus, Radix, Hosts, and Faber
   revisions; model filename, byte length, SHA-256; per-tensor storage and
   kernel identities; hardware/OS/driver/backend; load/prefill/decode/total
   timing; throughput; peak memory; transfer/readback/reload/recompile/
   rebuild/round-trip counters; reset/reuse/teardown; comparator policy; and
   first divergence.

A7 progress does not close GGUF-M5, GGUF-M6, EXEC-02, EXEC-03, CAP-01,
CAP-02, or CLOSE-01.

## 6. Oracle and comparator policy

The old A7 oracle story is corrected as follows.

### 6.1 First-failing hierarchy

1. **Storage/block oracle.** Compare each on-device block dequant result with
   `gradus:model/dequant` and the committed GI2 dequant goldens. Use
   `dequantize_block`/`dequantize_order` as the current Gradus names. This is
   a block-local oracle, not a whole-model F32 materialization.
2. **SmolLM2 model oracle.** Reuse the landed independent scalar F32 oracle
   at `radix/crates/faber-prefill-oracle/src/gea3_full_decode_oracle.rs`,
   with its manifest at `gea3_manifest.rs` and the GEA3 F32 artifact identity.
   That oracle imports no Gradus, MIR, emitted kernels, Hosts, or llama.cpp.
   The native Q4_K_M route is compared to the logical F32 values at the
   first divergent block/logit.
3. **SmolLM2 comparator.** Reuse the GEA3 comparator leg in
   `radix/docs/factory/gpu-execution-architecture/evidence/`
   (`gea3-comparator-receipt.json` and `gea3-numerical-receipt.json`). The
   oracle-versus-pinned-llama-cli leg is 8/8 in the committed receipt. The
   physical zero-readback rows in that receipt are a recorded FAIL finding,
   not an accepted device pass and not a replacement for A7 execution.
4. **Packed movement envelopes.** Use the current
   `DENSE_PACKED_ENVELOPES_V1` policy in
   `radix/crates/faber-prefill-oracle/src/dense_full_model.rs`. The current
   rows are SmolLM2 prefill `2.5e-2`, SmolLM2 decode `7.2e-3` (a movement /
   determinism row, not an independent correctness claim), and Qwen2.5-0.5B
   prefill/decode `7.0e-1`. The packed path does **not** inherit the retired
   `Q2_ENVELOPE = 6.5e-3`.
5. **Qwen2.5 references.** For Qwen2.5-0.5B use the existing independent
   llama.cpp CPU reference row and its current packed envelope. For
   Qwen2.5-1.5B, A7-U4b must first obtain a pinned independent reference and
   an explicitly named envelope; it must not copy the 0.5B or SmolLM2 number.

Any unknown GGML type, unsupported shape/layout, descriptor mismatch, body
hash mismatch, stale package-body version, non-finite output, missing oracle,
whole-model expansion, or silent CPU fallback fails closed. A comparator is
oracle-side evidence only; llama.cpp never runs inside the A7 device route.

## 7. Corpus and format boundary

The operator-local corpus at `/Users/ianzepp/ai/models/` is read-only and is
never committed by A7.

| Artifact | Architecture | Bytes | Tensors | Current storage distribution | A7 role |
| --- | --- | ---: | ---: | --- | --- |
| `SmolLM2-360M-Instruct-Q4_K_M.gguf` | `llama` | 270,590,880 | 290 | F32:65, Q4_K:16, Q5_0:176, Q6_K:16, Q8_0:17 | first Q4_K_M Metal/CUDA proof |
| `Qwen2.5-0.5B-Instruct-Q4_K_M.gguf` | `qwen2` | 397,808,192 | 290 | F32:121, Q4_K:12, Q5_0:132, Q6_K:12, Q8_0:13 | second dense Q4_K_M proof |
| `Qwen2.5-1.5B-Instruct-Q4_K_M.gguf` | `qwen2` | 986,048,768 | 338 | F32:141, Q4_K:168, Q6_K:29 | scale-independence proof; current harness row missing |
| `Qwen3.6-35B-A3B-UD-Q4_K_M.gguf` | `qwen35moe` | 22,663,387,424 | 753 | BF16:2, F32:368, Q4_K:82, Q5_K:38, Q6_K:4, Q8_0:259 | not A7 dense execution; EXEC-02/M5/EXEC-03 capstone |

The dense A7 class set is therefore `{F32, Q5_0, Q8_0, Q4_K, Q6_K}`. BF16
and Q5_K are not excluded from the current storage/dequant/kernel substrate;
they are excluded only from the three dense A7 row proofs. The 35B successor
uses the now-landed BF16/Q5_K format substrate and remains gated on the full
MoE/SSM graph, compiled-plan admission, reference inference, and memory.

## 8. Unit classification and corrected graph

### 8.1 Classification of the previous lowering

| Previous unit | Classification | Re-verification result |
| --- | --- | --- |
| `GGUF-A7-U1` contract freeze | **superseded** | R-PACK-01/02, current `PackedStorageLayout`/`PackedDequantResolution`, Hosts format mirror, and current package/body contracts already provide the cross-repo freeze. Its old conversion-arm and five-kind claims are retired. |
| `GGUF-A7-P1` new persistent `DeviceProgramLifetime` variant | **superseded** | Hosts `PreparedResidentSession` composes existing `RepeatingStep`/`PerProgram` semantics and already proves resident reuse/reset counters. No new Radix lifetime enum member is justified. |
| `GGUF-A7-U2` Metal kernels + SmolLM2 proof | **needs-rebaseline** | The kernel implementation scope is superseded by landed R-PACK-02 and current Metal emitter code. The prior R-PACK-05a Metal receipt is useful evidence and records final prefill/first-continuation matches, but it does not prove today's A7 resident two-prompt contract. |
| `GGUF-A7-U3` CUDA kernels + SmolLM2 proof | **needs-rebaseline** | The old `macos-arm64/src/cuda_host.rs` path is stale; current CUDA ownership is `hosts/crates/host-cuda`. The NVVM implementation is landed, but the current R-PACK-05a CUDA receipt stops before launch at `dense-qkv-projection-binding`, so native A7 execution remains unproved. |
| `GGUF-A7-U4` both Qwen rows | **needs-rebaseline** | Qwen2.5-0.5B is in the current two-row packed harness; Qwen2.5-1.5B is not. The row is split into A7-U4a and A7-U4b. |
| `GGUF-A7-U5` qualification + handoff | **still-valid** | Qualification remains one logical docs/evidence outcome, with current GEA3 oracle, packed-envelope, package-body, visibility, memory, and successor references. |

### 8.2 Corrected dependency graph

```text
Landed R-PACK-01/02 packed substrate
  + Gradus A3/A6 storage/reference receipts
  + landed GEA3 F32 oracle/comparator leg
       ├── A7-U2  Q4_K_M SmolLM2 Metal receipt
       └── A7-U3  Q4_K_M SmolLM2 CUDA receipt
                    └── A7-U4a Qwen2.5-0.5B both-backend receipt
                                 └── A7-U4b Qwen2.5-1.5B both-backend receipt
                                              └── A7-U5 qualification + handoff
                                                   └── GGUF-M5 / EXEC-03
                                                        └── GGUF-M6 / CAP-01 / CAP-02
                                                             └── CLOSE-01
```

A7-U2 and A7-U3 are backend-disjoint after the current GEA4 admission check.
A7-U4a waits for both SmolLM2 receipts because it consumes the same packed
adapter and resident route. A7-U4b waits for U4a and its own independent
reference/envelope. A7-U5 waits for all active receipts.

## 9. Active Hand units

### A7-U2 — Q4_K_M SmolLM2 native Metal receipt

| Field | Value |
| --- | --- |
| `id` | `GGUF-A7-U2` |
| `classification` | needs-rebaseline |
| `outcome` | Execute the existing native Q4_K_M packed route for SmolLM2-360M on burgus Metal. Reuse the landed R-PACK-02 Metal bodies and current dense full-model route; prove per-block dequant, full-model prefill, bounded decode, resident weight reuse, and second-prompt/reset behavior where the route exposes it. |
| `write_scope` | `radix/docs/factory/gpu-production-readiness/evidence/exec02/` A7-U2 receipt only; a narrowly required evidence index update. No `radix-mir` or `radix-mir-metal` production edits. Any new proof fixture must be a new, disjoint path and must pass the GEA4 gate. |
| `read_scope` | `radix/crates/radix-mir/src/kernel_plan/packed.rs`; `radix/crates/radix-mir-metal/src/emit/quantized_matmul.rs`; `radix/crates/faber-prefill-oracle/src/dense_full_model.rs`; Gradus `src/model/dequant.fab`; GEA3 oracle/comparator evidence; current Hosts Metal packed/resident route. |
| `done_when` | A committed burgus receipt identifies the exact Q4_K_M file and SHA-256, current revisions, native representation for every executed weight, no whole-model F32 expansion, first block/logit/token divergence or exact match, applicable packed envelope, prefill + bounded decode result, and a second-prompt re-entry through one resident session with resident/reuse/reset/release counters, peak memory, timing, and Metal identity. A missing or failed device path is recorded as `NOT ATTEMPTED`/FAIL with owner and recheck, never as a pass. |
| `sanity` | Current dense Metal device-run command from the existing route: `FABER_PREFILL_METAL_RUN=1 cargo test --release -p faber --lib dense_full_model_device_run -- --ignored --nocapture`, with the current feature flag required by the checkout. Narrow receipt/hash inspection and `git diff --check` on the evidence path. |
| `depends_on` | Landed R-PACK-02; Gradus A3/A6 dense references; landed GEA3 F32 oracle leg. No dependency on superseded U1/P1. |
| `dispatch_gate` | **GEA4 admission** must release or prove a disjoint path for the live `radix/crates/mir-emit-harness/src/**` admission family and Hosts GEA3 mirror files before any fixture/harness change. **NR-2** is not touched; if a semantic/HIR source change is required, stop and serialize behind NR-2. **PPB-U1** is not touched; if timing is wired through `radix/scripta/perf` or `perf.py`, stop and serialize behind PPB-U1. |
| `non_goals` | No new quantized emitter; no `conversion_arms`; no source-level `@ conversion`/`@ conversio` change; no Qwen rows; no 35B; no Radix lifetime variant; no Q2-envelope inheritance. |
| `risk` | high — physical Metal correctness and memory/residency evidence over a landed kernel substrate. |
| `integrable` | yes |

### A7-U3 — Q4_K_M SmolLM2 native CUDA receipt

| Field | Value |
| --- | --- |
| `id` | `GGUF-A7-U3` |
| `classification` | needs-rebaseline |
| `outcome` | Execute the existing native Q4_K_M packed route for SmolLM2-360M on pharos CUDA through the current NVVM emitter and the extracted `host-cuda` route. Prove the same block, model, memory, and resident-reuse facts as U2. |
| `write_scope` | `radix/docs/factory/gpu-production-readiness/evidence/exec02/` A7-U3 receipt only; a narrowly required evidence index update. If a focused host proof file is genuinely needed, it belongs under `hosts/crates/host-cuda/tests/` and must be disjoint from the GEA4 Hosts mirror seat. No old `hosts/macos-arm64/src/cuda_host.rs` path. |
| `read_scope` | `radix/crates/radix-mir-llvm/src/nvvm/quantized_matmul.rs`; `radix/crates/radix-mir-llvm/src/nvvm/quantized.rs`; `hosts/crates/host-cuda/src/cuda_host.rs`; `hosts/crates/host-cuda/tests/cuda_host_proof.rs`; current dense route; Gradus dequant; GEA3 oracle/comparator evidence. |
| `done_when` | A committed pharos receipt identifies the exact Q4_K_M file and SHA-256, current revisions, native representation for every executed weight, no whole-model F32 expansion, first block/logit/token divergence or exact match, applicable packed envelope, prefill + bounded decode result, and a second-prompt re-entry through one resident session with resident/reuse/reset/release counters, peak memory, timing, and CUDA identity. A missing machine or driver is an honest `NOT ATTEMPTED`/FAIL row with owner and recheck. |
| `sanity` | Current CUDA route command shape: `FABER_PREFILL_CUDA_RUN=1 cargo test --release -p faber --lib dense_full_model_device_run -- --ignored --nocapture`, or the current explicitly frozen equivalent at dispatch. Narrow PTX/descriptor/receipt/hash inspection and `git diff --check` on the evidence path. |
| `depends_on` | Landed R-PACK-02; Gradus A3/A6 dense references; landed GEA3 F32 oracle leg. Parallel-safe with U2 only while both remain evidence-only and do not edit shared harness files. |
| `dispatch_gate` | **GEA4 admission** must release or prove a disjoint path for `radix/crates/mir-emit-harness/src/**` and the Hosts GEA3 mirror family. **NR-2** remains read-only; any semantic/HIR change serializes behind NR-2. **PPB-U1** remains read-only; no `radix/scripta/perf`, `perf.py`, or perf-case edits. CUDA implementation is already in `radix-mir-llvm`/`host-cuda`; do not reopen those bodies unless a new first-failing receipt proves a real implementation defect. |
| `non_goals` | No Metal; no new NVVM emitter; no `macos-arm64/src/cuda_host.rs`; no Qwen rows; no 35B; no conversion-arm or lifetime changes. |
| `risk` | high — CUDA driver/toolchain and native packed receipt correctness. |
| `integrable` | yes |

### A7-U4a — Qwen2.5-0.5B native both-backend receipt

| Field | Value |
| --- | --- |
| `id` | `GGUF-A7-U4a` |
| `classification` | needs-rebaseline (split from prior U4) |
| `outcome` | Execute the current Qwen2.5-0.5B Q4_K_M row through the same native packed adapter on Metal and CUDA. Use the current manifest identity and storage distribution F32:121, Q4_K:12, Q5_0:132, Q6_K:12, Q8_0:13. No row-specific kernel constants. |
| `write_scope` | `radix/docs/factory/gpu-production-readiness/evidence/exec02/` A7-U4a receipt(s) only; `radix/crates/faber-prefill-oracle/` only if one narrow, disjoint backend/receipt parameter is genuinely missing. No emitter or semantic/HIR changes. |
| `read_scope` | Current `DenseRungManifest`/`DENSE_PACKED_ENVELOPES_V1` in `radix/crates/faber-prefill-oracle/src/dense_full_model.rs:39-116,260-380`; Gradus A6/reference receipts; current Metal and `host-cuda` routes; operator-local GGUF identity evidence. |
| `done_when` | Both backends have committed receipts with exact file identity, per-tensor native storage manifest, no special-case constants, no whole-model F32 expansion, prefill/decode first divergence, the current Qwen packed envelope, and a second-prompt re-entry through one resident session with resident/reuse/reset/release counters, timing, memory, and backend facts. The 0.5B row may use the existing `7.0e-1` V1 envelope; it may not use `Q2_ENVELOPE`. |
| `sanity` | Focused current dense-run commands for Metal and CUDA, followed by receipt identity/hash inspection and `git diff --check` on the evidence path. No broad performance sweep. |
| `depends_on` | A7-U2 and A7-U3; Gradus A6 Qwen2.5-0.5B reference receipt; current packed harness substrate. |
| `dispatch_gate` | **GEA4 admission** is required before any shared emit-harness fixture or Hosts mirror change; evidence-only work may proceed if disjointness is proven. **NR-2** owns `radix-semantic` passes and HIR nodes; any new generic/source/HIR requirement waits behind it. **PPB-U1** owns `radix/scripta/perf` and `perf.py`; do not modify those paths. |
| `non_goals` | No Qwen2.5-1.5B row; no qwen35moe; no new kernel family; no envelope re-calibration for another rung; no conversion-arm or marker migration. |
| `risk` | medium-high — cross-row shape/scale independence and paired physical evidence. |
| `integrable` | yes |

### A7-U4b — Qwen2.5-1.5B scale-independence and native receipt

| Field | Value |
| --- | --- |
| `id` | `GGUF-A7-U4b` |
| `classification` | needs-rebaseline (new split unit) |
| `outcome` | Add the missing Qwen2.5-1.5B Q4_K_M manifest/reference row to the current dense packed harness, then execute it on Metal and CUDA through the same adapter. The current storage distribution is F32:141, Q4_K:168, Q6_K:29 across 338 tensors. |
| `write_scope` | `radix/crates/faber-prefill-oracle/src/dense_full_model.rs` plus its co-located test only for the 1.5B manifest/reference/envelope row; `radix/docs/factory/gpu-production-readiness/evidence/exec02/` U4b receipts. No `radix-mir` emitter, semantic pass, HIR node, `scripta/perf`, or Hosts mirror edit. |
| `read_scope` | Gradus `exempla/gguf-inspect/README.md` and `exempla/gguf-materialize/README.md`; A6 1.5B source/reference receipts; current packed plan/emitter symbols; GEA3 policy for oracle shape only, not as a Qwen oracle. |
| `done_when` | The row has an independently pinned file identity, tokenizer/reference policy, per-tensor storage manifest, and explicitly calibrated comparator/envelope. Both Metal and CUDA receipts prove the same adapter with no row-pinned kernel constants, no whole-model F32 expansion, first divergence, finite gate, timing, memory, and backend/lifecycle facts. No 0.5B, SmolLM2, or Q2 envelope is inherited without a named ruling. |
| `sanity` | Focused manifest/harness tests for the new row, then the current Metal and CUDA dense-run commands for that row; receipt identity inspection and `git diff --check` on touched paths. |
| `depends_on` | A7-U4a; A6 1.5B reference/materialization identity; current R-PACK-02 packed substrate. |
| `dispatch_gate` | **GEA4 admission** applies if a proof fixture or host mirror is added; otherwise the new prefill-oracle row is file-disjoint. **NR-2** applies if the row exposes a new generic semantic/HIR requirement; default is no such edit. **PPB-U1** remains untouched because timing is receipt evidence, not a `scripta/perf` change. |
| `non_goals` | No new quantized format; no row-specific emitter; no qwen35moe; no 35B memory claim; no perf-driver change; no source visibility/conversion cleanup. |
| `risk` | medium-high — new independent reference/envelope plus scale-independence proof. |
| `integrable` | yes |

### A7-U5 — Qualification and substrate handoff

| Field | Value |
| --- | --- |
| `id` | `GGUF-A7-U5` |
| `classification` | still-valid |
| `outcome` | Consolidate U2/U3/U4a/U4b receipts and publish an exact A7 qualification/handoff note. State which dense rows and backends actually passed, which are `NOT ATTEMPTED` or failed, the native format/capability rows, memory evidence, prepared-session composition, GEA3 oracle/comparator provenance, and the unchanged M5/EXEC-02/EXEC-03/CAP/CLOSE successor chain. |
| `write_scope` | `gradus/docs/factory/production-ml-library/` A7 qualification/handoff note and this delivery's status/receipt links only; Radix evidence links may be added only as references. No campaign authority edit, no product code, no `scripta/perf`, no emit-harness family, and no Hosts mirror edit. |
| `read_scope` | All active A7 receipts; current packed harness; Gradus A3/A6 records; GEA3 oracle/comparator records; current package/body and prepared-session receipts; EXEC-02/EXEC-03 memory and successor authority. |
| `done_when` | The note links every active receipt by commit/path, states native versus not-attempted/failed rows exactly, confirms no executed capability record is left falsely pending, records Q4_K_M first and the 35B memory gate, and preserves GGUF-M5, GGUF-M6, EXEC-02, EXEC-03, CAP-01, CAP-02, and CLOSE-01 as mandatory successors. Factory-status audit remains zero findings. |
| `sanity` | Link/identity grep over the committed receipts, `git diff --check`, and `cd /Users/ianzepp/work/faberlang/radix && ./scripta/check-factory-goal-status`. |
| `depends_on` | A7-U4b, transitively U2/U3/U4a. |
| `dispatch_gate` | Recheck all three live seats before closeout. **NR-2** must not be represented as landed by an A7 receipt. **PPB-U1** timing work remains separate. **GEA4** emit-harness/Hosts admission work remains separate. |
| `non_goals` | No new execution; no campaign status or GO stamp; no 35B capstone acceptance; no source-level conversion or visibility edits. |
| `risk` | medium — cross-repo evidence drift and honest partial-result reporting. |
| `integrable` | yes |

## 10. Live-seat dispatch gates and lane-owned validation

These gates are named once here and repeated per active unit above so Mind can
check them at dispatch without guessing from a stale diff.

### NR-2 — semantic/HIR hot seat

NR-2 owns the live Radix semantic passes and HIR node surface:

- `radix/crates/radix-semantic/src/passes/**`, especially generic and
  `itera` typecheck passes;
- the HIR definition at `radix/crates/radix-hir/src/nodes.rs`;
- the re-export barrel at `radix/crates/radix-module/src/hir/nodes.rs` must not
  be mistaken for the definition.

A7 has no default write in those paths. A7 must stop and serialize if a native
route exposes a new semantic shape, `IteraLockstep`, generic forwarding, or
HIR representation requirement.

### PPB-U1 — performance driver hot seat

PPB-U1 owns `radix/scripta/perf`, `radix/scripta/perf.py`, and the checked-in
`radix/scripta/perf-cases/**` matrix. A7 records timing in its execution
receipts and does not modify the performance driver. Any request to add a
parity mode, case, trend, cap, or runner flag is PPB-U1 work and is serialized
behind that seat.

### GEA4 admission — emit-harness and Hosts mirror hot seat

GEA4 admission owns the emit-harness admission family, including the current
`radix/crates/mir-emit-harness/src/**` family and its
`radix/crates/radix-module/tests/pipeline_smoke_test.rs` hook, plus the Hosts
GEA3 mirror family under `hosts/macos-arm64/tests/`, notably
`gea3_decode.rs`, `gea3-carried-derived-parity-ledger.toml`, and
`gea3-carried-derived-vectors.json`. A7 evidence-only files are safe only when
they do not touch these paths. A new fixture or host proof must wait for the
current GEA4 owner to release the path or for Mind to record real
file-disjointness.

### Integrated validation owned outside child units

- The lint lane owns stages 1–2 over the integrated changed tree.
- The test lane owns stages 3–4 and any broad package/e2e proof required by a
  landed implementation.
- Device receipts own their exact physical command and environment. A
  `NOT ATTEMPTED` row is evidence, not a green substitute.
- A7 child units carry only their narrow sanity or physical proof. They do not
  copy `./scripta/check-source`, `./scripta/check-compile`, `--stage`, `--e2e`,
  or `--full` as per-child closeout ceremony.
- The closeout audit is `cd /Users/ianzepp/work/faberlang/radix &&
  ./scripta/check-factory-goal-status` and must report zero findings.

## 11. Stop conditions and open decisions

Stop the affected edge and record the first failure if:

- the model filename, byte length, SHA-256, architecture, or tensor census
  differs from the pinned corpus;
- an executed tensor cannot retain native packed identity;
- a block/range/layout or package body fails closed;
- the native route needs a whole-model F32 copy, silent CPU fallback, or
  unapproved host round-trip;
- a GEA3 or per-row CPU/comparator oracle is missing or a physical receipt is
  being relabeled from FAIL/NOT ATTEMPTED to PASS;
- the Qwen3.6 35B memory gate is attempted on pharos or another machine below
  the named operator authority;
- a unit needs a semantic/HIR, PPB, emit-harness, or Hosts mirror edit held by
  a live seat; or
- A7 work would create a source-level `conversion_arms` field, destination
  `impl From`, bare device entry, or signature-only device body.

Open decisions are deliberately narrow:

1. Mind freezes the exact A7 physical command/environment at each device
   dispatch. The current dense route's Metal/CUDA command shapes are the
   starting point, not permission to claim a run occurred.
2. U4b's Qwen2.5-1.5B independent reference and numeric envelope must be
   pinned before its first execution result. No existing envelope is silently
   generalized.
3. A7's bounded dense second-prompt proof may consume the current prepared
   resident-session composition. The full Qwen3.6 35B two-prompt persistence
   and `>=256` token guarantee remain successor scope.

## 12. Successors preserved through CLOSE-01

This delivery lowers GGUF-A7 only. It does not narrow, downgrade, defer, make
optional, or relocate any successor:

- Gradus: GGUF-M5 persistent native Metal/CUDA execution and GGUF-M6 Faber
  Qwen3.6 capstone;
- Radix campaign: EXEC-02 full Qwen3.6 packed kernel milestone, EXEC-03
  prepared resident sessions, CAP-01 Metal capstone, CAP-02 CUDA capstone,
  and CLOSE-01;
- all other unimplemented GGUF-A/GGUF-M units in the PML5 delivery.

The current BF16/Q5_K format support is an enabling substrate, not a claim
that the Qwen3.6 full model has executed. The 35B Q4_K_M memory gate, MoE/SSM
reference, compiled-plan admission, prepared session, and capstone receipts
remain mandatory.
