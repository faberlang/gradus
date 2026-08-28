# CAMPAIGN: gradus-clean-break — fixed-shape-to-generic conversion (3 waves)

**Status**: active — wave 1 units U1-U6 done at factory/w1-u* lanes (fold to main pending); waves 2-3 gated
**Created**: 2026-08-28
**Campaign:** `gradus-clean-break`
**Source:** operator need `127f9fd6` + amendment `59b4074a` (settled); wave-1 lowering task `4aa2f634`
**Repos:** `faberlang/gradus`, `faberlang/examples`
**Related:** [`GOAL.md`](GOAL.md) · [`wave-1-delivery.md`](wave-1-delivery.md)

---

Routing stub for operator need `127f9fd6` (3-wave conversion order, settled).
Wave 1 is chartered and lowered; waves 2-3 are gated successors named here so
later planning cannot mint a duplicate home. One wave per planner assignment;
this stub does not lower waves 2-3.

| Wave | Scope | State / gate |
| --- | --- | --- |
| 1 — collapse existing twins | Delete the seven named `_NxM` wrappers whose typed generic twin already exists; move all callers (both repos); docs closeout. Goal [`GOAL.md`](GOAL.md), units [`wave-1-delivery.md`](wave-1-delivery.md) | **Done at lanes** — U1–U6 receipts in [`GOAL.md`](GOAL.md) §Ledger (lowering task `4aa2f634`); fold to main pending |
| 2 — author missing twins, delete remaining zoo | `mse<M,N>` twin then delete `mse_2x2/4x4/2x8`; per-channel `[N]` bias `linear` form and `layernorm<T,D>` twin then delete `linear_2x8`/`layernorm_2x8`; re-sweep `train_step_*` / `bert_tiny_block_2x8` / `forward_mlp_loss [4,4]` against whatever twins then exist | **Gated**: starts only after wave 1 closes (need's conversion order). Lane paper: `factory/krs-2` branch `c419b02` body-reroutes for `linear_2x8`/`layernorm_2x8`; `*_carrier` residuals shrink as callers pin (SEM014/SEM005 posture, not this campaign's rewrite) |
| 3 — kernel.fab statues to size-generic device leaves | Convert the 48 `kernel.fab` fixed-shape statues to size-generic device leaves | **Gated**: not before wave 1 done AND shape-generic-device-route SGD-1 (imported-generic entry discovery) settled. Receipt-pin exceptions (`gea3-*-v1` replay, GEA1 gemv `[320,960]` frozen-chain) are frozen evidence, not callable API (amendment `59b4074a`) |

Campaign law (operator ruling, standing): old fixed-shape sizes go away
completely in favor of shape generics unless a named identity/receipt pin is
an absolute requirement; a training exemplum that happens to be 2×2 or 4×4
instantiates the generic at the call site; named overloads are the defect.

## Ledger

Machine-managed — wave, status (`pending` · `tasked` · `in progress` ·
`done` · `deferred`), planner/Hand seats, receipt (commit/handle), notes.
Wave-1 unit receipts are tracked in [`GOAL.md`](GOAL.md) §Ledger.

| Wave | Status | Seats | Receipt | Notes |
| --- | --- | --- | --- | --- |
| 1 — collapse existing twins | in progress | planner (lowered) / hand (implemented) | U1 `3aa262a8`+`9dc8b0f` · U2 `1eaaedbc` · U3 `12321d4` · U4 `d71ce7d` · U5 `d087bfc` · U6 `88fa5f8`+`3a5ea13` — all at `factory/w1-u*` lanes; unit receipts in [`GOAL.md`](GOAL.md) §Ledger | 6 units in [`wave-1-delivery.md`](wave-1-delivery.md), all done at lanes; wave close awaits fold to main + merge-owned run proofs (audit `8b86bc40` repaired `0ec9a33` + round 2) |
| 2 — author missing twins, delete remaining zoo | deferred | — | none | gated on wave 1 close; KRS-2 branch `c419b02` is paper only |
| 3 — kernel.fab statues to size-generic device leaves | deferred | — | none | gated on wave 1 done + SGD-1 settled |
