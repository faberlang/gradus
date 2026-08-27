# Campaign: Kernel-Purity Census (OX-Alpha)

**Status**: active — Wave 0 (carrier/admissions ruling + `NumericBlock` rename + stride-cache rider) delivered 2026-08-26, see [`wave-0-carrier-admissions-ruling.md`](wave-0-carrier-admissions-ruling.md); Wave 1 DONE 2026-08-27 — all 15 units accounted (math twins 13df284, nn twins 47d3d69, prior-landed 8; phase audit clean 1c6f1ad9; consumer proof 1d9127f); Wave 2 gate chain lowered and in flight (KPC-SEM landed 16f69d1d2 radix; PKG-ADM/PKG-REP dispatched a5d8c0f0/11948fae; KPC-WIRE/EMIT queued on shared surfaces); Waves 2–3 per §Waves
**Created**: 2026-08-26
**Mode**: routing + delivery record — this campaign owns the census rulings and wave ledger; code lands as normal direct-mode units
**Control-plane repo**: `/Users/ianzepp/work/faberlang/gradus`
**Source**: OX-Alpha kernel-purity census `015eb5f7` (report: `../../.vivi/oxalpha-kernel-census-015eb5f7.md`, base `83b65fa`) + operator rulings on task `aee52855` (Wave 0 priority ruling) + the operator fusion directive recorded by memo + need on task `ed5144c7` (2026-08-27, `~02:0xZ`)
**Participating repos**: `gradus` (carrier + math core); `radix` (digest lineage re-pins, admissions); consumers (`inferentia`) follow renames
**Current breadth/delivery**: all 47 live `gradus/src/**/*.fab` files were partitioned in [`wave-1-delivery.md`](wave-1-delivery.md); that document extends the original census without re-censusing covered ground and lowers the remaining Wave 1 rows
**Lowers to**: `delivery` per wave

## Summary

### Why this campaign exists: the measured fusion target

The operator re-grounded this campaign on the fusion problem, not on an
annotation count. The U5 receipt at Radix commit `4bce158c9` records a decode
median of **210,334 µs/step queue wait** versus **104,645 µs/step GPU kernel
body** — the operator-facing rounded comparison is **210 ms versus 104 ms,
about 2:1 queue-wait to GPU-kernel time**. The committed source is
`radix/docs/factory/perf-parity-baseline/evidence/2026-08-26-metal-m5max-u5/perf-parity-receipt-v1-2026-08-26-u5.json`, fields
`.faber_categories.categories.queue_wait.decode.median` and
`.faber_categories.categories.gpu_kernel_body.decode.median`.

This is a mechanism observation, not a throughput target and not a claim that
all queue time is removable. **Purity is the prerequisite for fusion**: typed
static-shape entries let the device route compose dependent operations into
fewer submissions, so fusion can erase inter-kernel waits. A faster isolated
body does not address the dominant term if launch and wait remain.

**Operator provenance**: the directive is the memo + need filing represented
by task `ed5144c7`, dated 2026-08-27 with the task's recorded `~02:0xZ`
timestamp. The directive names the U5 receipt, the 210/104 comparison, and
purity as the prerequisite for fusion. This campaign paragraph records that
ruling; it does not mint a new measurement.

Measurement guardrails remain active: decompose the wall before optimizing
(`gpu-lessons L12`), keep launch/queue/kernel terms separate (`L13`),
re-census after structural changes (`L17`), and never weaken numeric contracts
or widen tolerance to admit a purified body (`L20-L24`).

### Census finding and migration shape

The census classified every non-kernel function in the gradus tensor-math
core and decode path against the kernel contract
(`gradus:kernel` — typed static-shape `@ kernel` entries; host validation
before the boundary). Its structural finding: the production core is
authored on the **staged runtime carrier** while the kernel contract admits
**typed static-shape entries**. Everything else — the "~71 plain fns vs 18
kernel entries" gap — is downstream of that one seam. The original report was
not a global `src/` census; the 47-file breadth partition and extension rows
now live in [`wave-1-delivery.md`](wave-1-delivery.md).

This campaign converts the seam in waves, each wave unlocked by the
Wave 0 ruling recorded here:

- **Wave 0** — the carrier/admissions ruling (this campaign's founding
  decision): the boundary between the staged numeric carrier and typed
  kernel entries, the `Tensor` → `NumericBlock` rename, and the
  construction-time stride cache. Delivered.
- **Waves 1–3** — annotation/method-twin swaps, the prefill-chain carrier
  migration, and program composition. Planned; each is sized and
  entry-classified by the census (§3 tables there are the work list).

## Waves

| Wave | Scope (census §4) | Status | Evidence |
| --- | --- | --- | --- |
| 0 | Carrier/admissions ruling + `NumericBlock` rename + stride cache | **done 2026-08-26** | [`wave-0-carrier-admissions-ruling.md`](wave-0-carrier-admissions-ruling.md) |
| 1 | Annotation + method-twin swaps (≈15 historical rows: loss `mse_*`, math elementwise typed twins, `nn.silu/gelu/rmsnorm`, attention `scaled_dot_product_2x8/_static`) | **done 2026-08-27** — all 15 accounted: 8 prior-landed, 6 admitted this wave (`sub`/`mul`/`div`/`neg` gradus `13df284`, `gelu`/`silu` `47d3d69`), `abs`/`signum` red-named SEM004 lane gaps; phase audit `9fbec2c7` residual (7/7 lenses pass; one P2 lineage re-pin routed); Wave-2 gate = CTR-08 + consumer-proof (CTO ruling `f489d2eb`) + lineage pin | [`wave-1-delivery.md`](wave-1-delivery.md); audit probes `/tmp/kpc-audit/` |
| 2 | One production chain end to end (llama/SmolLM2 prefill off the carrier; decode-shaped T=1 first) | planned — sized only; waits for Wave 1 admission | [`wave-1-delivery.md`](wave-1-delivery.md) §6 |
| 3 | Program composition (multi-head programs; MoE last) | planned — waits for Wave 2 | — |

Dependency: Waves 1–3 use shape-generic `@ kernel` entries as the recommended
form. The old generic-vs-per-geometry question is not closed by prose: the
current Radix consumer re-probe and target-facing body/role evidence must close
it before Waves 2–3. If that re-probe is red, route the genuine fork as
`KPC-RADIX-SHAPE-GENERIC-ADMISSION` to `head-cto` / operator rather than
silently specializing every geometry. The remaining named admissions are
listed below.

### Radix admissions to schedule (census-named triggers)

| Admission | Trigger site (census §3) |
| --- | --- |
| Shape-generic kernel entries | `math.add`/`nn.linear` (zero-body-change annotatables) |
| Broadcast-elementwise recipe | `math.sub/mul/div` typed twins |
| Device layernorm (centering + β) | `nn.layernorm` split |
| NEOX-interleaved rope | `attention._rope` qwen2 branch |
| Device ln / lse | `loss.cross_entropy` row logsumexp |
| `sign()` on lane | `math.signum` |

### Explicit non-items (guardrails)

- `sampling._top_k`/`_top_p`/`_draw` — sequential heap/RNG algorithms; a
  device version is a different algorithm, not a purification (census F5).
- `gradient.fab` + `mlp.forward_mlp_loss` — frozen until the
  backward ⊕ nucleum compiler ruling exists (census F4).
- `dense.fab` forward family — needs the resident-weight program route,
  not purity edits. Owned by
  [`../dense-typed-assembly/goal.md`](../dense-typed-assembly/goal.md).
- Numeric-core consolidation (softmax ×4, transpose ×3, exp ×5) precedes
  Wave 2 (census F2).

## Validation

Per purification unit: `faber check` on the touched surface, focused proba
outcomes identical for behavior-preserving changes, and the canonical-faber
review rider completed before commit. The purity proof is a typed static-shape
kernel entry with no carrier, runtime-shape, host-allocation, I/O, state, or
RNG behavior in the body; host validation remains before the boundary. A
function that is sequential by algorithm is not force-purified. Numeric
contracts and tolerance constants never weaken.

Per wave: `faber check` green tree-wide (src + exempla), proba outcomes
identical per file for behavior-preserving waves, oracle digest lineage
re-pinned explicitly in `radix` when gradus source bytes in the lineage change
(never silent; precedent `e5e484ec8`). Wave 2 additionally needs the production
llama/SmolLM2 prefill chain and its separate launch/queue/kernel receipt; Wave 2
is sized but not lowered in this Wave 1 record.

## Ledger

| Unit | Status | Receipt | Notes |
| --- | --- | --- | --- |
| W0 ruling doc | done 2026-08-26 | `wave-0-carrier-admissions-ruling.md` | operator priority ruling, task `aee52855` |
| W0 rename `Tensor` → `NumericBlock` | done 2026-08-26 | gradus `500342d` | converter-driven, per-file check |
| W0 stride cache | done 2026-08-26 | gradus `500342d` | 1.75× on the decode logits handoff (ruling §4.2) |
| W0 digest re-pin | done 2026-08-26 | radix `9e5070d76` | GEA2 source lineage, identity proof attached |
| W1 annotation/method-twin swaps | **done 2026-08-27 — all 15 accounted**: six census annotations 2026-08-26 (`2a1d361970`, task `ba835b45`); residual rows landed — math twins `13df284`, nn twins `47d3d69`; abs/signum red-named (SEM004 lane gaps, routed); phase audit clean `1c6f1ad9`; consumer proof `1d9127f` | gradus `2a1d361970`+`13df284`+`47d3d69`; [`wave-1-delivery.md`](wave-1-delivery.md) | Role/body transport and composition landed at Radix `5482bc5ac`, `fae613683`, `dba1383c8`; consumer proof classifies the remaining gate as radix linkage (KPC chain), not gradus purity. No numeric contract is relaxed. |
| W2 prefill-chain migration | planned — sized only; waits for Wave 1 admission and current Radix consumer proof | [`wave-1-delivery.md`](wave-1-delivery.md) §6 | No Wave 2 units lowered here; production llama/SmolLM2 prefill chain remains mandatory |

| W3 program composition | planned | — | blocked on W2 |
