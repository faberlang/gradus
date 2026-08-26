# Campaign: Kernel-Purity Census (OX-Alpha)

**Status**: active — Wave 0 (carrier/admissions ruling + `NumericBlock` rename + stride-cache rider) delivered 2026-08-26, see [`wave-0-carrier-admissions-ruling.md`](wave-0-carrier-admissions-ruling.md); Waves 1–3 planned and gated on the radix admissions list (§Waves)
**Created**: 2026-08-26
**Mode**: routing + delivery record — this campaign owns the census rulings and wave ledger; code lands as normal direct-mode units
**Control-plane repo**: `/Users/ianzepp/work/faberlang/gradus`
**Source**: OX-Alpha kernel-purity census `015eb5f7` (report: `../../.vivi/oxalpha-kernel-census-015eb5f7.md`, base `83b65fa`) + operator rulings on task `aee52855` (Wave 0 priority ruling)
**Participating repos**: `gradus` (carrier + math core); `radix` (digest lineage re-pins, admissions); consumers (`inferentia`) follow renames
**Lowers to**: `delivery` per wave

## Summary

The census classified every non-kernel function in the gradus tensor-math
core and decode path against the kernel contract
(`gradus:kernel` — typed static-shape `@ kernel` entries; host validation
before the boundary). Its structural finding: the production core is
authored on the **staged runtime carrier** while the kernel contract admits
**typed static-shape entries**. Everything else — the "~71 plain fns vs 18
kernel entries" gap — is downstream of that one seam.

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
| 1 | Annotation + method-twin swaps (≈15 fns: loss `mse_*`, math elementwise typed twins, `nn.silu/gelu/rmsnorm`, attention `scaled_dot_product_2x8/_static`) | planned | — |
| 2 | One production chain end to end (llama/SmolLM2 prefill off the carrier; decode-shaped T=1 first) | planned | — |
| 3 | Program composition (multi-head programs; MoE last) | planned | — |

Dependency: Waves 1–3 hinge on one radix question — shape-generic `@ kernel`
entries vs per-geometry specialization — plus the admissions list below.

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

Per wave: `faber check` green tree-wide (src + exempla),
proba outcomes identical per file for behavior-preserving waves, oracle
digest lineage re-pinned explicitly in `radix` when gradus source bytes in
the lineage change (never silent; precedent `e5e484ec8`).

## Ledger

| Unit | Status | Receipt | Notes |
| --- | --- | --- | --- |
| W0 ruling doc | done 2026-08-26 | `wave-0-carrier-admissions-ruling.md` | operator priority ruling, task `aee52855` |
| W0 rename `Tensor` → `NumericBlock` | done 2026-08-26 | gradus `500342d` | converter-driven, per-file check |
| W0 stride cache | done 2026-08-26 | gradus `500342d` | 1.75× on the decode logits handoff (ruling §4.2) |
| W0 digest re-pin | done 2026-08-26 | radix `9e5070d76` | GEA2 source lineage, identity proof attached |
| W1 annotation/method-twin swaps | done 2026-08-26 | gradus `2a1d361970` (task `ba835b45`) | gate cleared by ruling `fc7f15a2`; entries 4 + helpers 2, all zero-body-change; 2 size-generic admitted; **six import-loss sites remain KNOWN BUGS per ruling `fc7f15a2`** (library @ kernel accepted at check; device role does not cross the import boundary — fix is its own unit, now DFV2-3 in radix device-fragments-v2); stop-reported rows routed to W2/W3 (nn.silu/gelu/rmsnorm, math typed twins) |
| W2 prefill-chain migration | planned | — | blocked on W1 + admissions |
| W3 program composition | planned | — | blocked on W2 |
