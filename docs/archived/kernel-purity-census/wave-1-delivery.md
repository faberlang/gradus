# DELIVERY: kernel-purity-census — Wave 1 breadth and typed-twin lowering

**Status**: lowered for audit routing 2026-08-27 — no GO stamp; the
remaining Wave 1 rows are source-delivery units, and the extension rows are
census-only until separately checked
**Goal / campaign**: [`CAMPAIGN.md`](CAMPAIGN.md)
**Assignment**: Vivi task `ed5144c7`
**Primary repo**: `/Users/ianzepp/work/faberlang/gradus`
**Evidence-only repo**: `/Users/ianzepp/work/faberlang/radix`
**Planner boundary**: this commit changes planning documents only. It does not
change `.fab`, `.proba`, compiler, runtime, or target code.

---

## 0. Ground-truth check

This lowering uses the live source rather than treating the original census as
a global inventory.

| Fact | Live evidence | Consequence |
|---|---|---|
| Original census identity | `.vivi/oxalpha-kernel-census-015eb5f7.md`, base `83b65fa`; its own `reviewed` and `excluded` lists | The report covered the tensor-math/decode slice, not all of `gradus/src`. Covered rows are not re-censused here. |
| Current Gradus breadth | `find src -type f -name '*.fab'` at Gradus `d745cdd7c263dc568972f20d353185ea9c50f6e4` returns **47** files | The partition in §3 accounts for all 47 files. |
| Existing census annotations | `2a1d361970` landed `loss.mse_2x2/4x4/2x8`, `math.add`, and attention `scaled_dot_product_2x8/_static`; `a731817` already landed typed `nn.linear`, `nn.rmsnorm`, and `nn.swiglu_hidden` | Those rows are recorded as already landed. The new Wave 1 units do not assign them again. |
| Remaining campaign-table rows | Live `math.fab` has carrier-only `sub`, `mul`, `div`, `neg`, `abs`, `signum` at `:288-379`; live `nn.fab` has carrier-only `gelu` at `:430-445` and `silu` at `:604-614` | The actual residual of the campaign's approximate 15-row table is eight functions: six math elementwise functions plus `nn.gelu` and `nn.silu`. |
| Current Radix generic-device history | The same-unit generic control is green in `gradus/scripta/spike-shape-generic-kernel/REPORT.md`; Radix DFV2-3/4/5 landed at `5482bc5ac`, `fae613683`, and `dba1383c8` | The old import-role/body red is historical implementation evidence, not permission to silently specialize every geometry. A current consumer proof is still required before the Wave 2/3 gate is closed. |

The original report's approximate count remains useful as campaign history. It
is not a live count of outstanding work.

## 1. Interpreted theme and fusion reason

The operator's 2026-08-27 directive re-grounds purity in the measured fusion
problem. The U5 receipt from Radix commit `4bce158c9` records, for the decode
phase, a median **210,334 µs/step queue wait** versus **104,645 µs/step GPU
kernel body**. Rounded as the operator stated it, that is **210 ms versus
104 ms, about 2:1 queue-wait to GPU-kernel time**.

The authoritative fields are:

```text
radix/docs/factory/perf-parity-baseline/evidence/2026-08-26-metal-m5max-u5/
  perf-parity-receipt-v1-2026-08-26-u5.json
  .faber_categories.categories.queue_wait.decode.median       = 210334 µs
  .faber_categories.categories.gpu_kernel_body.decode.median  = 104645 µs
```

This is a mechanism observation, not a throughput target and not a claim that
all queue time is removable. It says why the campaign exists: pure typed
entries are the prerequisite for composing dependent operations into fewer
device submissions, so fusion can erase inter-kernel waits. A faster isolated
body does not address the measured dominant term if the launch and wait remain.

**Operator provenance**: the directive is recorded in the memo + need filing
represented by task `ed5144c7`, dated 2026-08-27 with the task's recorded
`~02:0xZ` timestamp. The task explicitly names the U5 receipt `4bce158c9`,
the 210/104 comparison, and the instruction that purity is the prerequisite
for fusion. This paragraph is provenance, not a new measurement.

Measurement recurrence defenses are carried forward from `gpu-lessons`:

- decompose the wall before optimizing (`L12`);
- keep launch, queue-wait, and kernel-body terms distinct (`L13`);
- re-census after a structural change (`L17`);
- never widen or weaken a numeric contract to make a purified body pass
  (`L20-L24`).

## 2. Normalized Wave 1 outcome

Wave 1 closes the cheapest source-side seam without pretending that the
carrier is a kernel:

1. retain the existing typed/glyph annotations already landed;
2. move the remaining elementwise math and activation names onto typed
   static-shape entries, following the landed `math.add` clean break;
3. retain carrier implementations under explicit `_carrier` names where the
   dynamic/broadcast path is still required;
4. migrate every live caller and focused proof that used the carrier name;
5. prove that no numeric order, dtype contract, tolerance, fallback, or
   sequential algorithm changed.

This is a clean-break source lowering, not a compatibility facade. The
broadcast-capable carrier remains an explicit load/host seam. The typed entry
is the only candidate for device admission.

### Existing rows that are not re-lowered

| Campaign row | Live disposition | Evidence |
|---|---|---|
| `loss.mse_2x2`, `loss.mse_4x4`, `loss.mse_2x8` | Landed annotation, zero body change | `src/loss.fab:263`, `:275`, `:287`; Gradus `2a1d361970` |
| `math.add` | Landed typed generic kernel entry, zero body change | `src/math.fab:261-265`; Gradus `2a1d361970` |
| `attention.scaled_dot_product_2x8`, `attention.scaled_dot_product_static` | Landed kernel-role annotations; bodies are glyph composition | `src/attention.fab:57-86`; Gradus `2a1d361970` |
| `nn.linear` | Already typed and annotated before the census-Wave-1 commit | `src/nn.fab:359-363`; Gradus `a731817` |
| `nn.rmsnorm` | Already typed and annotated before the census-Wave-1 commit | `src/nn.fab:506-510`; Gradus `a731817` |
| `nn.swiglu_hidden` | Already typed and annotated before the census-Wave-1 commit | `src/nn.fab:512-516`; Gradus `a731817` |

The six rows from `2a1d361970` carried a known imported-role loss at the time
of landing. Radix subsequently landed the role/body transport and composition
sequence at `5482bc5ac`, `fae613683`, and `dba1383c8`. Target-facing green spike
expectations and a current Gradus consumer artifact remain a separate gate;
this delivery does not turn the old red into an unverified green.

## 3. Full-scale breadth check — all 47 source files

The comparison rule was: use the census report's explicit `reviewed` list as
the covered set, subtract it from the live 47-file inventory, and inspect only
uncensused candidates. `transformer.fab` was in the report only for call-graph
context, so its unwalked typed body gets one extension row below; the prior
attention/math/nn/dense/moe/tensor-view classifications are not repeated.

### 3.1 Complete 47-file partition

**Existing census coverage — 16 files, no re-census**:

```text
src/attention.fab
src/decode.fab
src/gradient.fab
src/kernel.fab
src/loss.fab
src/math.fab
src/mlp.fab
src/nn.fab
src/sampling.fab
src/tensor.fab
src/transformer.fab          # call-graph only; extension row below
src/model/dense.fab
src/model/dense_llama.fab
src/model/dense_qwen2.fab
src/model/moe.fab
src/model/tensor_view.fab
```

**Uncensused files with potentially pure numeric surfaces — 6 files,
extended as rows rather than re-censused**:

```text
src/calibration.fab
src/generation.fab
src/metrics.fab
src/model/dequant.fab
src/model/qwen35moe_state.fab
src/optimize.fab
```

**Uncensused files with no candidate typed kernel surface in this pass — 25
files**:

```text
src/block_verify.fab
src/cache.fab
src/cache_branch.fab
src/context_lookup.fab
src/data.fab
src/dtype.fab
src/gradus.fab
src/model/artifact.fab
src/model/block_view.fab
src/model/capsule.fab
src/model/full_model_view.fab
src/model/gguf.fab
src/model/gguf_manifest.fab
src/model/qwen35moe.fab
src/model/safetensors.fab
src/model/tensor_payload.fab
src/parameter.fab
src/prepared_state.fab
src/receipt.fab
src/serialize.fab
src/shape.fab
src/speculative.fab
src/test_util.fab
src/tokenizer.fab
src/train.fab
```

The counts are 16 + 6 + 25 = 47. The 25-file set is not silently ignored:
these modules are host admission, identity/wire, cache/state, parser, or
sequential-control surfaces. In particular, `train.fab`'s typed train-step
wrappers are multi-result orchestration over `optimize._sgd_family`; its RNG
and dropout paths are not kernel-purity rows.

### 3.2 Extension rows

These rows are **census extensions only**. They are not Wave 1 Hand units and
must not be folded into the Wave 1 done count. Each row names the numeric
surface that deserves a later focused census and the blocker that prevents a
false purity claim today.

| Row | Potentially pure surface and live evidence | Current classification / next owner |
|---|---|---|
| **KPC-W1B-DEQUANT** | `src/model/dequant.fab:147-229,233-470,530-570`: `_half`, `_bfloat16`, `_dequant_f32`, `_dequant_f16`, `_dequant_bf16`, `_dequant_q5_0`, `_dequant_q8_0`, `_dequant_q4_k`, `_dequant_q5_k`, `_dequant_q6_k`, `dequantize_block`, `dequantize_order` | Numeric block-codec math is a candidate for a packed recipe, not generic elementwise purity. Raw `list<int<u8>>`, bit/nibble geometry, per-format block sizes, and row-order assembly are the blockers. Follow Radix packed-recipe ownership and `gpu-lessons L48`; require an independent per-format golden before any device route. **Separate dequant census, not Wave 1.** |
| **KPC-W1B-QWEN-STATE** | `src/model/qwen35moe_state.fab:734-768,796-828,843-879,966-980`: `_rms_norm_row`, `_l2_norm_row`, `_gemv`, `_gemm_rows`, `rope_head`, `recurrent_output`; larger compositions at `:890-929,1092-1294,1394-1580` | The helper maps/reductions and projections may become typed fragments. The surrounding route carries source callbacks, runtime lists, KV/state mutation, multi-section NEOX RoPE, and the ordered Gated DeltaNet recurrence. Keep `_delta_step`, `recurrent_update`, `linear_attention`, `full_attention`, and their step forms as a separate hybrid-state execution goal; do not force a sequential recurrence into the Wave 1 purity contract. **MODEL-03 / hybrid-device owner.** |
| **KPC-W1B-TRANSFORMER** | `src/transformer.fab:68-107`: `bert_tiny_block_2x8` is a fully typed glyph body but has no kernel annotation; `:569-601` `dense_block_static` is a typed/carrier bridge with runtime positions and imported attention | `bert_tiny_block_2x8` is the call-graph-only census blind spot. Its LayerNorm and bias method surface need device admission; `dense_block_static` remains a bridge/program, not a one-entry purity conversion. **Transformer follow-up census after layernorm admission.** |
| **KPC-W1C-METRICS** | `src/metrics.fab:85-120`: `accuracy` performs finite checks, row argmax, and a batch reduction | Potential typed reduction/argmax entry, but current body is a `NumericBlock`/flat-list host walk and requires an argmax recipe plus a typed i32 target contract. Metric record accessors/equality stay host. **Metrics owner; low fusion priority.** |
| **KPC-W1C-GENERATION** | `src/generation.fab:657-668`: `_suppress_eog` is an elementwise logits map | Potential typed mask application, but current input/output are `list<f32>` and each index consults `tokenizer.is_eog`. A typed EOG mask or an explicit host/device boundary is required. The sampling and cursor/state functions stay host. **Generation owner; do not move tokenizer policy into a kernel.** |
| **KPC-W1C-CALIBRATION** | `src/calibration.fab:524-562,581-623`: `_dot`, `_norm2`, `_scale`, `_sub_scale`, `_residual2`, `_cosine` contain vector maps/reductions | These helpers could be typed for a calibration-specific lane, but `_orthonormal` at `:564-578` is sequential Gram-Schmidt and `bake` at `:321-390` builds a measurement artifact with dynamic slots. No tensor is rewritten. **Calibration owner; measurement/offline priority.** |
| **KPC-W1C-OPTIMIZER** | `src/optimize.fab:119-152`: `_sgd_family`, `sgd_step_2x2`, `sgd_step_4x4` are typed update math behind list-driven output | The pointwise update is numerically pure, but `_sgd_family` is list-of-tensors orchestration and `step` at `:419-435` mutates versioned parameter state. A future training entry must preserve exact `param − rate·grad` order and the optimizer/gradient contract. **GPU-training owner; not inference fusion.** |

### 3.3 Why the other uncensused files stay host-side

- `cache.fab`, `cache_branch.fab`, `prepared_state.fab`, and
  `model/qwen35moe_state.fab` state containers own cache/state lifetimes;
  copying or equality over their payloads is not a free kernel conversion.
- `block_verify.fab`, `context_lookup.fab`, and `speculative.fab` contain
  first-divergence, suffix-search, candidate, or transaction control. Their
  ordering is semantic host control.
- `model/artifact.fab`, `model/block_view.fab`, `model/capsule.fab`,
  `model/full_model_view.fab`, `model/gguf.fab`, `model/gguf_manifest.fab`,
  `model/qwen35moe.fab`, `model/safetensors.fab`, and `serialize.fab` own
  bytes, identities, manifests, ranges, and fail-closed admission.
- `dtype.fab` and `shape.fab` are tag/shape algebra and validation. They are
  the host side of the carrier/admissions boundary, not lane bodies.
- `parameter.fab`, `receipt.fab`, and `train.fab` own identity, evidence, or
  training control. `train.dropout` includes explicit RNG state and therefore
  is an algorithmic state path, not a purification target.
- `tokenizer.fab` is text/BPE policy. `data.fab`, `gradus.fab`, and
  `test_util.fab` add no numeric function surface.

## 4. Purity proof and required riders

### 4.1 Purity-proof definition

A Wave 1 function is **pure enough for admission** only when all of the
following are true:

1. Its public device candidate has a typed static-shape tensor signature.
   Literal dimensions are valid pins. `size` dimensions are valid only when
   they bind from the call and survive current monomorphization.
2. Its body is a direct tensor glyph or admitted tensor method map/reduction.
   It does not read `NumericBlock`, `list<f32>`, runtime shape metadata, bytes,
   strings, a source callback, cache/state, or RNG, and it does not allocate a
   host carrier in the lane body.
3. Host validation stays before the boundary. A typed entry does not paper over
   a missing dtype, shape, layout, or error admission, and no `coalesce` turns
   a failed lane read into a value.
4. The current `@ kernel` / `@ public` role and body channel admit the concrete
   instance. A green `faber check` alone is not a device-admission proof.
   Imported role/body transport and the no-survivor composition rules are the
   current Radix contract.
5. The focused proba proves identical outcomes for the changed function and
   its carrier caller migration. Numeric order, dtype behavior, error behavior,
   tolerances, and fallback policy remain unchanged. No performance claim is
   made by this proof.

If a function instead contains heap/RNG behavior, first-difference semantics,
state recurrence, source I/O, dynamic carrier allocation, or an unresolved
recipe, it is host-sequential or hybrid for this campaign. It stays out of the
purification unit. This is the same boundary that keeps sampling heap/RNG out
of scope.

### 4.2 Canonical-faber rider — every purification unit

Every Hand that changes `.fab` in a purification unit carries this rider
before its commit:

- resolve the file's `+++ locale = "en"` surface first;
- run the canonical-faber review separately from `faber check` and report any
  compile finding separately from any idiom finding;
- preserve the canonical entry ordering `@ kernel` then `@ public`;
- use the direct glyph/method form (`·`, `⊙`, `⊘`, `ᵀ`, `.silu()`,
  `.gelu()`, `.rms_norm()`) rather than a carrier helper or a hand-rolled
  numeric loop;
- check that the preferred form is grounded in the canonical-faber skill or a
  cited live corpus exemplar; do not accrete a one-off style suspicion;
- record `no canonical finding` when the changed body is canonical, rather than
  treating silence as an unperformed review.

The rider is part of each unit's `done_when`. It is not a request to edit the
skills repository in this Wave 1 commit.

## 5. Ordered Wave 1 Hand unit graph

The original table's six landed rows are historical inputs, not new units.
The live residual is split by behavior family and shared-file serialization.
The math unit must land before the activation unit because `nn.swiglu` and
several callers still use `math.mul`'s carrier name.

```text
KPC-W1-MATH-ELEMENTWISE  →  KPC-W1-NN-ACTIVATIONS
```

### KPC-W1-MATH-ELEMENTWISE — typed binary and unary math twins

| Field | Value |
|---|---|
| `id` | `KPC-W1-MATH-ELEMENTWISE` |
| `outcome` | Follow the landed `math.add` clean break for the remaining six functions: add typed static-shape `sub`, `mul`, `div`, `neg`, `abs`, and `signum` entries with direct bodies/method twins; move the existing dynamic/broadcast implementations to explicit `_carrier` names; migrate current carrier callers and co-located carrier proofs without changing their contracts. `div` and `signum` must stop at their named Radix lane-admission red rather than inventing a fallback. |
| `write_scope` | `gradus/src/math.fab`; `gradus/src/math.proba`; carrier-call migrations only in `gradus/src/attention.fab`, `gradus/src/nn.fab`, and `gradus/src/model/moe.fab` where `rg` finds `math.mul`/the renamed carrier verbs. No unrelated rewrite of the already-censused math algorithms. |
| `done_when` | The six typed functions have the same-shape static signatures and canonical `@ kernel`/`@ public` ordering where the current Radix capability admits them; the carrier forms remain available under explicit names and all current dynamic/broadcast callers resolve to them; focused math and affected-file proba outcomes are identical; no tolerance, numeric operation order, dtype gate, error variant, or fallback changes; the canonical-faber rider is recorded before commit. If a Radix admission is red, the Hand reports the exact red and leaves that row unclaimed rather than weakening the proof. |
| `depends_on` | None for source preparation; device admission depends on the current Radix generic entry/body-channel proof. Same-file math changes serialize internally. `div` follows the broadcast-elementwise/elementwise-divide admission; `signum` follows the lane-sign admission. |
| `sanity` | `faber check` on `src/math.fab`, `src/math.proba`, and the named caller files; focused `faber test src/math.proba` plus the affected caller proof filter if available. |
| `non_goals` | No Wave 2 carrier migration; no reduction, matmul, concatenate, slice, softmax, or transpose rewrite; no new broadcast recipe hidden in a typed same-shape entry; no tolerance change; no change to sampling or gradient behavior; no radix edits. |
| `risk` | medium — public verb names and carrier caller migrations touch several existing call sites; `div` and `signum` have explicit device-capability dependencies, and numeric contracts must remain byte/order faithful. |
| `integrable` | yes — the carrier migration and all current callers land together; a target-admission red is reported as a blocked capability, never papered over. |

### KPC-W1-NN-ACTIVATIONS — typed GELU and SiLU method twins

| Field | Value |
|---|---|
| `id` | `KPC-W1-NN-ACTIVATIONS` |
| `outcome` | Follow the existing `nn.rmsnorm`/`nn.linear` clean-break shape: add typed static-shape `nn.gelu` and `nn.silu` entries whose bodies use the canonical tensor method twins; move the current NumericBlock implementations to `gelu_carrier` and `silu_carrier`; update fixed-shape adapters, `nn.swiglu`, transformer/MLP wrappers, affected exempla, and co-located proofs to name the carrier explicitly. |
| `write_scope` | `gradus/src/nn.fab`; `gradus/src/nn.proba`; `gradus/src/mlp.fab`; `gradus/src/transformer.fab`; `gradus/src/mlp.proba`; `gradus/src/transformer.proba`; `gradus/exempla/nn-bridge/src/main.fab`; `gradus/exempla/dense-swiglu/src/main.fab`; `gradus/exempla/dense-prefill-smollm2/src/main.fab`; any additional `.fab`/`.proba` caller found by the exact `nn.gelu`/`nn.silu` grep at dispatch. This unit may change caller spellings only; it does not re-census transformer/dense behavior. |
| `done_when` | Typed `gelu` and `silu` bodies contain no carrier walk, runtime shape read, scalar helper loop, allocation, or error-wrapper path; carrier forms retain the existing f32 checks and values under explicit names; fixed-shape adapters and every live carrier caller compile and focused proba outcomes are identical; SiLU matches the proven `x.silu()` device idiom and GELU matches the current `.gelu()` numeric contract without replacing it with a different approximation; the canonical-faber rider is recorded before commit. A missing device method/recipe fails the unit closed with its exact admission handle; no host fallback is introduced. |
| `depends_on` | `KPC-W1-MATH-ELEMENTWISE` for the shared `nn.fab` carrier caller migration; current Radix typed-method admissions for `silu` and `gelu`; no dependency on Wave 2 production-chain work. |
| `sanity` | `faber check` on `src/nn.fab`, `src/nn.proba`, and direct wrapper/exemplum files; focused `faber test src/nn.proba` and the affected package proof if the package runner admits it. |
| `non_goals` | No `layernorm` recipe; no `swiglu` program composition; no dense/prefill carrier migration; no changes to the scalar approximation contract, tolerances, `gradient.fab`, sampling, or Radix source. |
| `risk` | medium — the public activation names have many proof and wrapper callers; changing the approximation or silently routing a carrier would invalidate the numeric contract and the fusion premise. |
| `integrable` | yes — typed entries, named carrier residuals, and caller/proof migration form one complete logical change. |

## 6. Wave 2 sizing only — do not lower until Wave 1 admits

Wave 2 is intentionally sized, not lowered into Hand units here. It begins
only after the remaining Wave 1 source rows admit and the current Radix
consumer proof closes the generic entry/body-channel gate.

| Sized slice | Current anchors | Scope at sizing boundary |
|---|---|---|
| W2-A load and typed pin | `src/model/dense.fab:367-399,543-551`; typed layer records at `src/transformer.fab:530-550` | Move resident weights out of `NumericBlock` at load and pin concrete/generic static shapes. Keep host validation and carrier flow explicit. |
| W2-B prefill attention | `src/kernel.fab:474-552`; `src/attention.fab:404-624,754-827`; `src/model/dense.fab:459-649` | Wire RMSNorm → Q/K/V GEMMs → consecutive RoPE → transpose → score/scale/causal softmax → context/O projection. Existing GEA3 entries are anchors, not proof that the Gradus production path is wired. |
| W2-C prefill MLP/residual | `src/kernel.fab:557-565`; `src/nn.fab:380-428,500-516,620-638`; `src/transformer.fab:420-438` | Wire gate/up → SiLU/SwiGLU → down projection → residual, preserving bias presence and operation order. |
| W2-D production chain and first measurement | `src/generation.fab:711-762,945-1029`; dense prefill exemplum and U5 measurement identity | Prove one llama/SmolLM2 prefill production chain end to end, with decode-shaped `T=1` first where required. Record launch/queue/kernel terms separately and re-census after the structural change. |

No W2 row receives a `write_scope`, `done_when`, or Hand id in this document.
The Wave 2 chain must not start by purifying `sampling`, `gradient`, or a
host/state route.

## 7. Lane-owned validation and integration boundary

Child Hands own only the narrow sanity checks in §5. The broader gates are
owned once, outside the child rows:

| Owner | Gate |
|---|---|
| lint | `./scripta/check-source` over the integrated Gradus tree |
| test/compile | `./scripta/check-compile`, focused affected `.proba` outcomes, and the tree-wide exempla check required by the campaign |
| Radix admission | Current generic imported-entry/body-channel and method/recipe proofs; any red is a named capability finding, not a source fallback |
| merge | `git diff --check`, path-limited Gradus commits, and explicit digest-lineage routing if a later source change enters a Radix lineage |
| factory audit | `python3 ../radix/scripta/audit-factory-goal-status.py --factory-root docs/factory --fail-on error` |

The Wave 1 source units do not claim real-device execution or fusion speedup.
Those claims require the later production-chain receipt, with the U5 timing
categories preserved.

## 8. Recommendation and routing flag

**Recommendation**: keep shape-generic typed entries as the default, not a
per-geometry specialization zoo. The same-unit generic control in
`gradus/scripta/spike-shape-generic-kernel/REPORT.md` is green, the archived
Radix shape-generics goal records implicit `size` binding and monomorphization,
and Radix's current DFV2-3/4/5 sequence now carries imported role, body, and
composition facts. The typed source direction therefore matches both the
language design and the fusion goal.

The prior spike's import-role/body loss was a genuine implementation fork at
its old Radix tip. At the current Radix tip, the transport and composition
fixes are landed in the live history, so the remaining question is a **current
consumer proof**, not permission to specialize every shape. Do not close the
Wave 2/3 dependency from `faber check` alone. Re-run the three spike shapes
against the current Radix binary and record the target-facing result.

**Routing flag**: if that current re-probe still fails for imported generic
entries, name the fork `KPC-RADIX-SHAPE-GENERIC-ADMISSION` and route it to
`head-cto` / operator. The alternatives are explicit:

- preserve the recommended generic design and repair entry discovery,
  imported role/body transport, or target proof; or
- record a deliberate temporary per-geometry specialization ruling with its
  limited scope and re-entry condition.

No planner decision authorizes the second alternative. Until the re-probe is
clean, Waves 2–3 remain gated. This recommendation does not reopen the settled
carrier ruling, the sampling heap/RNG non-item, or the frozen `gradient.fab`
backward-⊕ boundary.

## 9. Open questions for Mind

1. Ask the Radix owner to attach the current three-probe target receipt before
   changing the Wave 2/3 gate. The old `c8ff00be` red and the new DFV2 commits
   must not be conflated.
2. Treat `KPC-W1B-DEQUANT`, `KPC-W1B-QWEN-STATE`, and the other extension rows
   as separate census goals. Do not inflate the Wave 1 completion count.
3. Preserve the existing campaign non-items: sampling heap/RNG is a different
   algorithm; `gradient.fab` stays frozen until the backward-⊕ ruling; and no
   numeric contract or tolerance is weakened during purification.
