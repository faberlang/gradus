# GOAL: gradus-clean-break — shape-generic-only public API (wave 1)

**Status**: active — wave 1 folded to main (arc #5); wave 2 in progress: twin bank U1-U5 + U8/U9 on main (arcs #8/#10), U6/U7 and the U10-U14 deletion chain gated on the MIR monomorphization fix (need cb6c7466, goal-forge in flight; U6 run-gate evidence 4ad678e6); wave 3 gated on wave-2 completion + SGD-1/2
**Created**: 2026-08-28
**Campaign:** `gradus-clean-break`
**Source:** operator need `127f9fd6` + amendment `59b4074a` (settled); lowering task `4aa2f634`
**Repos:** `faberlang/gradus` (library src/proba, exempla, docs), `faberlang/examples` (four training packages)
**Related:** [`wave-1-delivery.md`](wave-1-delivery.md) · [`CAMPAIGN.md`](CAMPAIGN.md) · `docs/factory/kernel-region-split/` (KRS-2 wave-2 paper)

---

Goal artifact for operator need `127f9fd6` (+ amendment `59b4074a`, settled — do
not reopen). Lowering task `4aa2f634`. Wave 1 delivery lives in
[`wave-1-delivery.md`](wave-1-delivery.md); wave routing stub in
[`CAMPAIGN.md`](CAMPAIGN.md).

## Summary

Delete the named fixed-shape `_NxM` wrappers from the Gradus public API
wherever a shape-generic typed twin already exists, and move every caller
onto the generic at the call site. After wave 1, the live Gradus public API
exposes shape-generic leaves only for these families; a training exemplum
that happens to be 2×2 or 4×4 instantiates the generic, it does not keep a
named per-shape function.

## Problem

Gradus carries two parallel surfaces per family: shape-generic typed leaves
(`nn.linear<M,K,N>`, `nn.gelu<M,N>`, `attention.scaled_dot_product_static<B,D>`,
`optimize._sgd_family<Figura>`) and a zoo of named fixed-shape wrappers
(`linear_2x2`, `linear_4x4`, `gelu_4x4`, `gelu_2x8`,
`scaled_dot_product_2x8`, `sgd_step_2x2`, `sgd_step_4x4`) that detour through
staged carriers or one-line delegate. The named overloads are the defect, not
the style (operator ruling): every one of the seven listed here has a live
typed twin, so the destination form already ships and the wrapper is dead
weight that advertises a fixed-shape API.

## Goals

- The seven named wrappers do not exist as public API:
  `nn.linear_2x2`, `nn.linear_4x4`, `nn.gelu_4x4`, `nn.gelu_2x8`,
  `attention.scaled_dot_product_2x8`, `optimize.sgd_step_2x2`,
  `optimize.sgd_step_4x4`.
- Every caller (examples/training packages, gradus exempla, gradus src
  internal callers, matching proba tests) compiles against the generic leaf
  with shape parameters unified from argument types.
- No compatibility alias survives; no "thin wrapper forever." Thin wrappers
  may exist only inside a single landing commit sequence and are gone before
  the need closes.
- Docs that list the zoo as the public surface (README, api-reference,
  api-shape-policy) are updated in the same closeout.

## Non-goals

- No `matmul<M,K,N>` or `transpose<M,D>` inventions — the typed forms are the
  `·` glyph and `ᵀ` postfix (operator DO-NOT list).
- `linear_2x8`, `layernorm_2x8` stay — no typed twin for per-channel `[N]`
  bias / LayerNorm yet (wave 2, sister need).
- `mse_2x2` / `mse_4x4` / `mse_2x8` stay — no `mse<M,N>` yet (wave 2).
- `train_step_*`, `bert_tiny_block_2x8`, `forward_mlp_loss` stay as named
  functions (their bodies' delegation targets may change; the names are not
  this wave's targets).
- `kernel.fab` 48 statues stay (wave 3, gated on imported-generic entry
  discovery / SGD-1).
- Staged `*_carrier` residuals (`linear_carrier`, `gelu_carrier`,
  `rmsnorm_carrier`, `silu_carrier`, `gather_carrier`, `transpose_carrier`)
  stay as-is — load-edge SEM014/SEM005 posture, not rewritten this wave.
- No imported-device entry discovery, no shape-generic-device-route (SGD-1)
  dependency — same-unit generics already check.
- Historical measurement identities (`gea3-*-v1` rows, artifact roots,
  receipts) are frozen evidence elsewhere; they are not a reason to keep any
  callable symbol (amendment `59b4074a`).

## Ground truth researched (live gradus main, 2026-08-28, pre-wave)

### Twins exist (destination — keep)

| Twin | Site | Form |
| --- | --- | --- |
| `nn.linear<M,K,N>` | `src/nn.fab:362-365` | `@ kernel @ public`, `(x · w) + b`, same-shape `[M,N]` bias |
| `nn.gelu<M,N>` | `src/nn.fab:434-437` | `@ kernel @ public`, `x.gelu()` |
| `nn.silu<M,N>` / `nn.rmsnorm<T,D>` / `nn.swiglu_hidden<T,F>` | `src/nn.fab:619-622` / `:519-522` / `:525-529` | `@ kernel @ public` |
| `math.add/sub/mul/div/neg<M,N>` | `src/math.fab:267+/:296+/:323+/:350+/:379+` | `@ kernel @ public` |
| `attention.scaled_dot_product_static<B,D>` | `src/attention.fab:77-85` | `@ kernel`; body identical statement-for-statement to `scaled_dot_product_2x8`; **no source call site today** (KRS-6 census) |
| `optimize._sgd_family<Figura>` | `src/optimize.fab:117-127` | `@ public`, list-driven `param − lr·grad`; already the delegation target of `train_step_bert_linear`/`train_step_bert_layernorm` (`src/train.fab:98-99,:114`) with proba pins (`src/train.proba:909,:922`) — list form proven at check and proba level |

### Wrappers that die (verified live bodies)

| Wrapper | Site | Body today |
| --- | --- | --- |
| `nn.linear_2x2` | `src/nn.fab:110-116` | `@ public`, `⇥ NnError`, detours `_staged` → `linear_from_raw<2,2,2>` |
| `nn.linear_4x4` | `src/nn.fab:122-125` | `@ public`, one-line `linear(input, weight, bias)` |
| `nn.gelu_4x4` | `src/nn.fab:131-139` | `@ public`, `⇥`, detours `gelu_carrier` (wrong per need) |
| `nn.gelu_2x8` | `src/nn.fab:181-189` | `@ public`, `⇥`, detours `gelu_carrier` |
| `attention.scaled_dot_product_2x8` | `src/attention.fab:57-64` | `@ kernel`, inline typed body |
| `optimize.sgd_step_2x2` / `sgd_step_4x4` | `src/optimize.fab:136-140` / `:148-152` | `@ public`, delegate `_sgd_family([param],[grad],lr)` |

`linear_from_raw` (`src/nn.fab:368-381`) has exactly one caller —
`linear_2x2:115` — and dies with it. `_staged` keeps live callers
(`linear_2x8`, `layernorm_2x8`) and stays (wave 2 owns them).

### Caller census (complete, 2026-08-28)

`linear_2x2`: `examples/training/linear-regression/src/train.fab:95` (fac/cape
wrapped — wrapper is `⇥`), `examples/training/linear-regression/oracle/capture.fab:94`,
`gradus/exempla/nn-bridge/src/main.fab:105`.
`linear_4x4`: `examples/training/mlp/src/train.fab:150,152`,
`examples/training/mlp/oracle/capture.fab:152,154`, `nn-bridge/src/main.fab:185`.
`gelu_4x4`: `examples/training/mlp/src/train.fab:151`,
`mlp/oracle/capture.fab:153`, `nn-bridge/src/main.fab:125`.
`gelu_2x8`: `examples/training/bert-tiny-fragment/src/train.fab:371` +
`oracle/capture.fab:403`; `examples/training/bert-gradus-probe/src/train.fab:415`
(fac/cape wrapped); `nn-bridge/src/main.fab:135`.
`scaled_dot_product_2x8`: `bert-tiny-fragment/src/train.fab:366` +
`oracle/capture.fab:398`; `bert-gradus-probe/src/train.fab:390`.
`sgd_step_2x2`/`sgd_step_4x4`: `gradus/src/train.fab:68-69,80-83`;
`gradus/src/optimize.proba:531,543` (direct calls).
Comment-only references (no calls): `src/nn.proba:11,19`,
`src/attention.proba:20`, `src/train.proba:768-769,875,891`,
`src/tensor.fab:90-95` census, `src/gradus.fab:51-52`,
`exempla/training-loop-mlp/src/main.fab:22,39,321`.
No `src/transformer.fab` or other src caller names any dying wrapper.

Docs advertising the zoo: `README.md:130,245,251-254`,
`docs/api-reference.md:35,990-995`, `docs/api-shape-policy.md:40`.

### Environment truth (planning-time observation)

No `radix/target/{debug,release}/faber` binary exists at the workspace right
now; the PATH `faber` (~/.cargo) is stale against tip source (SEM001 on
current `src/dtype.fab`). Run/check proofs in the units require a fresh
radix `cargo build` first (merge/lane environment precondition, not a child
Hand concern).

### Related paper (not authority over the ruling)

`docs/factory/kernel-region-split` KRS-2 (lane branch `factory/krs-2`,
commit `c419b02`, **not on main**) rerouted wrapper bodies onto typed leaves.
Wave 1 supersedes those remnants wherever they touch the dying wrappers: the
names die, so the lane's body-reroute for `linear_2x2`/`gelu_4x4`/`gelu_2x8`
is moot; its `linear_2x8`/`layernorm_2x8` reroutes belong to wave 2. The
KRS-2 receipt's two recorded blockers carry forward as wave-1 risk notes:
(1) a fixed-shape `@ kernel` wrapper calling a generic `@ kernel` leaf failed
specialization under `faber test` — irrelevant once wrappers are deleted,
but generic-leaf calls from package code must be check-proven per package;
(2) `faber run` refused execution of `@ kernel` functions at that radix tip
(`65f2d7d6b`) — a run-route red that is recorded as baseline if it fires,
never a reason to keep a name (need's explicit honesty rule).

## Reference packet (paths/commands to inspect)

- `gradus/src/nn.fab`, `src/attention.fab`, `src/optimize.fab`, `src/train.fab`
- `gradus/src/optimize.proba`, `src/train.proba`, `src/nn.proba`, `src/attention.proba`
- `gradus/exempla/nn-bridge/{src/main.fab,README.md}`
- `faberlang/examples/training/{linear-regression,mlp,bert-tiny-fragment,bert-gradus-probe}/{src/*.fab,oracle/*}`
  (separate git repo rooted at `faberlang/examples`)
- `vivi need show 127f9fd6` (ruling + amendment `59b4074a`)
- `gradus/docs/factory/kernel-region-split/unit-cards.md` (KRS-2 receipt §)
- Census grep: `grep -rn -E "linear_2x2|linear_4x4|gelu_4x4|gelu_2x8|scaled_dot_product_2x8|sgd_step_2x2|sgd_step_4x4" --include="*.fab" --include="*.proba"`

## Constraints and invariants

- Operator ruling settled (need + amendment): generics-only live API; named
  `_NxM` deleted, never aliased; v1/receipt pins are frozen evidence, not
  keep-the-methods.
- Conversion order is fixed: wave 1 (this need) → wave 2 (missing twins,
  then remaining named zoo) → wave 3 (kernel.fab statues; gated on
  imported-generic entry discovery / SGD-1; do not start before 1 done and
  SGD-1 settled).
- Callers move in the same logical change or a tightly following unit, so
  deletion never strands a consumer that still names the symbol.
- Example/exemplum sources under `examples/training/*` use the **Latin
  keyword surface** (`fixum/varia/fac/cape/itera`, `[reader] locale = "la"`);
  edits stay in that surface. `mlp` and `bert-tiny-fragment` are **device
  programs** (`[device] backend/steps/inputs` in `faber.toml`) — manifest
  input buffers and pinned step counts are frozen fixtures; do not touch
  values, only call-site spellings.
- Oracle `capture.fab` files compile as part of their packages' proofs and
  must move with the source call sites; `oracle/reference.json` /
  receipt files are frozen evidence and are not edited.
- Error-channel asymmetry: dying wrappers are `⇥ NnError` (`linear_2x2`,
  `gelu_*`) or bare; the twins `linear<M,K,N>` / `gelu<M,N>` are
  **infallible** — call-site conversion deletes `fac {} cape {}` arms, it
  does not preserve them.
- `scaled_dot_product_static<B,D>` takes scale `[B,B]`; the bert callers'
  `[2,2]` `dk_scale` unifies at `B=2`.

## Architecture direction

- Destination leaves already exist; wave 1 adds no new public symbol.
  Optimize default (locked): callers route onto the already-`@ public`
  `optimize._sgd_family<Figura>` list form — the operator's alternative
  (mint a public `sgd_step<Figura>`) is **not** taken: no new named API is
  minted when the destination already ships (smallest correct code).
- Per-family collapse: move callers first (generics already exist, nothing
  breaks), then delete the wrapper + its file-local ledger comment in the
  same family's unit. Cross-repo commits are path-limited per repo
  (`gradus` and `faberlang/examples` are separate repositories).
- Docs close in one final unit after all deletions (single edit surface for
  README/api-reference/api-shape-policy + the two comment-only src ledgers).

## Supporting skills

None required. Related repo paper: `kernel-region-split` (KRS-2 receipt),
`shape-generic-kernels.md`, `api-shape-policy.md` (staged-carrier paragraph
is historical PML1 posture; typed generics are the production twin now).

## Implementation shape (first milestone — not a delivery graph)

One family's full collapse end-to-end (e.g. optimize: reroute `train.fab`,
rewrite the two `optimize.proba` tests, delete `sgd_step_2x2`/`sgd_step_4x4`,
green checks) proves the shape. The ordered unit graph is
[`wave-1-delivery.md`](wave-1-delivery.md).

## Acceptance criteria (objective)

1. None of the seven names resolves as Gradus public API (grep of `src/**`
   finds no `fn` declaration; no alias of the same shape contract remains).
2. All consumer packages check green: gradus library + probas,
   `exempla/nn-bridge`, the four `examples/training` packages.
3. `exempla/nn-bridge` and the two training exempla (`linear-regression`,
   `mlp`) run after they stop naming the deleted functions; the known
   pre-existing `linear_2x2` matmul red on the bridge is recorded as
   baseline, not claimed green, and is not an excuse to keep the name.
4. README, api-reference, api-shape-policy no longer advertise the deleted
   names as public surface; retirement recorded append-only where ledger
   comments exist.
5. A cross-repo call-site grep (both repos) returns zero live calls to the
   seven names (frozen receipts/historical docs excepted).

## Validation (commands / manual flows)

- `./scripta/check-source` and `./scripta/check-compile` (requires a built
  radix `faber`; see environment truth) — lane-owned, named once in the
  delivery spec.
- `faber check` + `faber run` per touched package (`exempla/nn-bridge`,
  `examples/training/{linear-regression,mlp}`); `faber test` on the gradus
  package for the rewritten proba rows.
- Census grep (reference packet) as the no-live-caller audit.

## Ledger

Machine-managed — unit, status (`pending` · `tasked` · `in progress` ·
`done` · `deferred`), Hand seat, receipt (commit/handle), notes. Cards and
ordering live in [`wave-1-delivery.md`](wave-1-delivery.md).

| Unit | Status | Seat | Receipt | Notes |
| --- | --- | --- | --- | --- |
| GCB-W1-U1 | done | hand | examples `3aa262a8` (factory/w1-u1) · gradus `9dc8b0f` (factory/w1-u1) | nn-family callers move (linear-regression, mlp, nn-bridge) |
| GCB-W1-U2 | done | hand | examples `1eaaedbc` (factory/w1-u2) | attention/bert callers move |
| GCB-W1-U3 | done | hand | gradus `12321d4` (factory/w1-u3) | optimize family collapse (`_sgd_family`) |
| GCB-W1-U4 | done | hand | gradus `d71ce7d` (factory/w1-u4) | nn library deletion (four wrappers + `linear_from_raw`) |
| GCB-W1-U5 | done | hand | gradus `d087bfc` (factory/w1-u5) | attention library deletion |
| GCB-W1-U6 | done | hand | gradus `88fa5f8` (factory/w1-u6) · examples `3a5ea13` (factory/w1-u6) | docs closeout (both repos); fold to main pending |

## Open questions

None blocking. (KRS-2 lane's `linear_2x8`/`layernorm_2x8` body-reroutes on
`factory/krs-2` are wave-2 paper; wave-1 units do not depend on that branch
and must not merge it.)

## Stop conditions

- A generic leaf call from a consumer package fails to check (specialization
  or import failure on a live radix): record the exact error, keep the
  callers-moved commit (it is integrable), do not re-add a named wrapper,
  report to Mind for a radix ruling.
- `faber run` refusal of `@ kernel` execution blocks the run proofs: record
  as baseline red per the need's honesty rule; check-green remains the
  integrable bar; report to Mind.
- Any hook blocks a path-limited commit: report, do not bypass.

## Handoff readiness label

**Ready for delivery** — lowered in `wave-1-delivery.md` (6 units + closeout
gate). Planner readiness verdict only; the machine-parseable factory status
is the `**Status**` line at the top of this file.
