# gradus-clean-break wave 2 — delivery spec and unit graph

**Status**: planned — lowered for audit; no unit has landed
**Created**: 2026-08-28
**Campaign:** `gradus-clean-break`
**Source:** operator need `e01c6cc0` + amendment `6732365e` (settled — do not reopen); lowering task `24f8fbca`
**Repos:** `faberlang/gradus` (library src/proba, exempla, docs), `faberlang/examples` (four training packages)
**Related:** [`CAMPAIGN.md`](CAMPAIGN.md) · wave 1: [`GOAL.md`](GOAL.md) + [`wave-1-delivery.md`](wave-1-delivery.md) (folded at gradus `bf55937`, examples `402ea2e`)

---

Delivery lowering for operator need `e01c6cc0` (+ amendment `6732365e`).
Goal authority is the need itself (operator rulings settled); wave-1 receipts
are the post-wave baseline. Every wrapper/twin/caller claim below was
re-verified against live source at gradus `bf55937` (clean tree except one
untracked spike artifact, §Env) and examples `402ea2e` before carding.

Standing `non_goals` on every card: no `matmul<M,K,N>` / `transpose<M,N>`
inventions (`·` and `ᵀ` exist); no `kernel.fab` conversion (wave 3, SGD-1
gated); no new `*_carrier` math and no carrier rewrite into `<M,N>` forms;
no device manifest input-buffer or step-count edits; no radix/faber source
changes; no edit to frozen evidence (oracle `reference.json`, benchmark
baselines, archived docs, `docs/factory/**` campaign paper except the
append-only pml0 ledger marks U14 owns).

## P1 — intent, outcome, boundaries (settled by the need)

- **Intent.** Live Gradus public API after this wave: shape-generic leaves
  only. Training geometries (2×2, 4×4, 2×8, [8,8], probe [8,16]) are
  instantiations at call sites, never symbol names and never unnamed public
  signatures frozen to one geometry.
- **Decision owner.** Operator (need + amendment). Planner locked only the
  mechanical defaults in §Locked rulings; each cites its evidence.
- **Boundary.** This wave authors the missing typed twins, migrates every
  remaining named/literal-shape caller, deletes the zoo. Wave 3 (kernel.fab
  statues) does not start here and must reuse the twins this wave lands.
- **Explicit non-goals (need).** abs/signum stay carrier-blocked (SEM004 —
  no tensor `.abs()`/`.sign()` method twin; recorded, not faked). SEM014
  staged load-edge carriers shrink only as callers pin; no new carrier math.

## P2 — done-when, validation, paths, audit claims

**Wave done-when (the need's DONE WHEN, verbatim in force):**

1. No remaining named `_NxM` math/nn/loss/train/optimize/attention/
   transformer function in public gradus source, and no unnamed public
   function whose signature is only a frozen training geometry.
2. Exception list explicit and tiny: compiler-blocked abs/signum carriers;
   SEM014 staged load-edge carriers (now uniformly `*_carrier`-named);
   nothing else expected on this surface.
3. New callers cannot find `linear_2x8` / `mse_2x8` / `layernorm_2x8` /
   `train_step_4x4` / `bert_tiny_block_2x8` / `mse_2x2` / `mse_4x4` /
   `train_step_2x2` / `train_step_4x4` / `train_step_bert_linear` /
   `train_step_bert_layernorm` / `forward_mlp_loss [4,4]` / `dense.gather` /
   `dense.gather_step` in the public API. If an LLM can import a
   shape-named function, the need is not done.
4. Proof: `faber check` of gradus + the migrated exempla / nn-bridge and the
   four `examples/training` packages; the historical `linear_2x2` bridge
   matmul red is baseline, never claimed newly green.

**Validation (lane-owned, named once — §Lane-owned).**

**Allowed write paths.** gradus: `src/{nn,loss,optimize,train,mlp,transformer,math,gradient,tensor,gradus}.fab` + `src/model/{dense,moe}.fab` + matching `*.proba` + `exempla/{nn-bridge,training-loop-mlp,dense-swiglu}/` + `README.md`, `docs/{api-reference,api-shape-policy,module-map,quickstart}.md` + the pml0 ledger append marks; examples repo: the four `examples/training/*` packages' `src/*.fab`, `oracle/{capture.fab,README.md}`. **Forbidden:** `src/kernel.fab`, radix/faber source, oracle `reference.json`/receipts, benchmark baselines, `docs/archived/**`, other `docs/factory/**` campaign paper.

**Factual claims needing audit** (planner-verified at the cites; auditor
re-checks): the zoo inventory table, the twin-status table, the caller
census, the staged-rename ripple census, the four compiler facts, the env
truth.

## Interpreted theme

Author the seven missing shape-generic typed surfaces the need names
(`mse<M,N>`, `layernorm<T,D>`, the per-channel linear bias contract,
`sgd_step<Figura>`, typed swiglu, generic `forward_mlp_loss`, and the
gather branch), move every remaining fixed-shape caller in both repos onto
generics at the call site, then delete the remaining zoo and close the docs.

## Normalized spec (delivery-sized outcome)

After this wave the gradus typed surface is: `math.add/sub/mul/div/neg`,
`nn.linear<M,K,N>` (same-shape bias) + `nn.linear_channel<M,K,N>`
(per-channel bias), `nn.gelu/silu`, `nn.rmsnorm`, `nn.layernorm<T,D>`,
`nn.swiglu_hidden` + typed `nn.swiglu`, `nn.gather<T,V,D>` (or recorded
SEM016 residual), `attention.scaled_dot_product_static<B,D>`,
`loss.mse<M,N>`, `optimize.sgd_step<Figura>`,
`mlp.forward_mlp_loss<M,K,H,N>` (+ companion). The staged tier survives
only under `*_carrier` names (SEM014 load-edge). All fourteen zoo symbols
are gone; docs describe the generic surface; the pml0 admit rows carry
append-only retirement marks.

## Repo-aware baseline (live census, 2026-08-28)

### Zoo inventory (complete outside `kernel.fab` — wave 3 owns that file)

| Symbol | Site (gradus `bf55937`) | Kind |
| --- | --- | --- |
| `nn.linear_2x8` | `src/nn.fab:114` | `@ public ⇥ NnError`, body `(input · weight).added_bias(bias)` — method ops only, no `_staged` (dropped as dead code in the wave-1 arc #5 de-conflict; confirmed absent) |
| `nn.layernorm_2x8` | `src/nn.fab:125` | `@ public ⇥ NnError`, body `x.layer_norm(1, 1e-5, scale, offset)` |
| `loss.mse_2x2` / `mse_4x4` / `mse_2x8` | `src/loss.fab:278` / `:290` / `:302` | `@ kernel @ public`; three identical bodies (`p − t`, `⊙`, `.mean()`) |
| `train.train_step_2x2` / `_4x4` | `src/train.fab:68` / `:79` | `@ public`, delegate `optimize._sgd_family` |
| `train.train_step_bert_linear` / `_layernorm` | `src/train.fab:94` / `:110` | `@ public`, delegate `optimize._sgd_family` (12+6 slots; 18-return single step is PARSE040-capped at 16) |
| `transformer.bert_tiny_block_2x8` | `src/transformer.fab:69` | `@ kernel @ public`, self-contained method/glyph math |
| `mlp.forward_mlp_loss` (frozen [4,4]) | `src/mlp.fab:161` | `@ radix {lane="air"} @ radix backward`, all six args `[4,4]` |
| `dense.gather` / `dense.gather_step` (private) | `src/model/dense.fab:234` / `:240` | frozen `[8,16]→[2,16]` / `[1,16]` REF-01 pin statues; internal callers `:512, :537, :577, :605, :638` |

No other fixed-shape public function exists outside `kernel.fab`
(sweep: `^fn …(tensor<f32, [digit` over `src/**/*.fab`).

### Twin status

| Family | Typed twin today | Wave-2 action |
| --- | --- | --- |
| mse | none (staged `loss.mse` occupies the name) | author `mse<M,N>`; staged → `mse_carrier` |
| layernorm | none (staged `nn.layernorm` occupies the name; `rmsnorm<T,D>` is the pattern) | author `layernorm<T,D>`; staged → `layernorm_carrier` |
| linear per-channel bias | none (`linear<M,K,N>` is same-shape only) | author `linear_channel<M,K,N>` via `.added_bias` |
| sgd step | `_sgd_family<Figura>` `@ public` underscore-private (`src/optimize.fab:124`) | publicize as `sgd_step<Figura>` |
| swiglu (full gated MLP) | `swiglu_hidden<T,F>` only; down-projection staged | author typed `swiglu<T,F,N>`; staged → `swiglu_carrier` |
| forward_mlp_loss | frozen [4,4] | generalize `<M,K,H,N>`; companion follows |
| gather | `gather_carrier` only (SEM016 note `src/nn.fab:457-458`) | branch unit (U9) |
| bert block | none (block is an assembler, not a leaf) | delete; callers compose leaves at call site |

### Caller census (complete, both repos)

- **examples** (`402ea2e`): linear-regression `src/train.fab:94,103` +
  `oracle/capture.fab:93,118` (`mse_2x2`, `train_step_2x2`); mlp
  `src/train.fab:153,162` + `oracle/capture.fab:155,182` (`mse_4x4`,
  `train_step_4x4`); bert-tiny-fragment `src/train.fab:362-407` +
  `oracle/capture.fab:384-407,494-500` (`layernorm_2x8` ×3, `linear_2x8` ×6,
  `mse_2x8`, `train_step_bert_*`); bert-gradus-probe `src/train.fab:351`
  (`bert_tiny_block_2x8` full-block call + block-vs-leaves agreement diff),
  `:360-429` (leaf path, fac/cape arms), `:429,356` (`mse_2x8`),
  `:512,518` (`train_step_bert_*`). Oracle README rows:
  linear-regression `:23`, mlp `:26,:218`, bert-tiny-fragment `:21-23`.
- **gradus exempla**: nn-bridge `src/main.fab:110-115` (`linear_2x8` row),
  `:128-133` (`layernorm_2x8` row), `:92` (staged `nn.layernorm`), README
  `:13,:17,:22-23,:40`; training-loop-mlp `src/main.fab:305,316`
  (`forward_mlp_loss` + companion), `:323` (`train_step_4x4`), README
  `:11,:19,:21,:47`; dense-swiglu `src/main.fab:85` (staged `nn.swiglu`).
- **gradus src staged-call ripple** (rename fallout, no fixed shapes):
  `transformer.fab:318` (`nn.layernorm`), `:418` (`nn.swiglu`);
  `model/moe.fab:289` (`nn.swiglu`); probas: `loss.proba:94,102,110` +
  `metrics.proba` (`loss.mse`), `nn.proba` (`nn.layernorm`, `nn.swiglu`).
- **gradus probas on zoo symbols**: `train.proba:875-926` (all four
  `train_step_*` direct), `transformer.proba:456-460`
  (`bert_tiny_block_2x8` pinned bytes). No proba calls `mse_2x2/4x4/2x8`,
  `linear_2x8`, or `layernorm_2x8` (their coverage is the staged rows +
  exempla; `nn.proba:231,:340` are staged tests whose names cite the rows).
- **docs**: `api-reference.md:490-492` (mse trio), `:548,:561`
  (`forward_mlp_loss [4,4]`), `:989-990` (`linear_2x8`/`layernorm_2x8`),
  `:999` (staged swiglu), `:1329-1332` (train_step quartet), `:1380`
  (`bert_tiny_block_2x8`); `README.md:105,:114,:130,:246-247`;
  `api-shape-policy.md:48-49`; `quickstart.md:57,:66`; `module-map.md:96`;
  `tensor.fab:90-107` census ledger; `gradus.fab:52-60` facade note;
  pml0 ledger rows 4, 5, 7-9, 15-17 (`docs/factory/production-ml-library/pml0-proof-api-ledger.md:35-48`).

### Compiler facts (verified live)

1. **SEM005 = `duplicate_definition`** (radix
   `docs/archived/reader-locale-packs/audit.md:188`; catalog help "rename
   one of the definitions"): one name, one symbol per module. A typed twin
   cannot share a name with the staged form. House pattern where the typed
   twin is production: typed takes the plain name, staged becomes
   `*_carrier` — `math.add`/`add_carrier` (`src/math.fab:268/:278`),
   `nn.linear`/`linear_carrier`, `nn.gelu`/`gelu_carrier`,
   `nn.rmsnorm`/`rmsnorm_carrier`, `nn.silu`/`silu_carrier`.
2. **`.added_bias` is strict rank-extension** (radix
   `crates/radix-air/src/nodes.rs:809-840`): receiver `[B,D]`, bias exactly
   `[D]`; same-shape pairs reject. So per-channel bias is a distinct typed
   signature from `linear<M,K,N>`'s `[M,N]` — two symbols are forced, not
   a style choice. Absent-bias typed route is the `·` glyph itself.
3. **Size-generic pins over `⇥` are live** (`_pin_same<size A, size B>` →
   `tensor<f32, [A, B]> ⇥ DenseError`, `src/model/dense.fab:394`; cast in
   do/catch) and **size-generic `@ radix backward` is live**
   (`simple_loss<size R, size C>` + `loss_backward`,
   `src/gradient.fab:216-219`). Both precedent the riskiest wave-2 shapes
   (U9 gather, U6 companion).
4. **Generic `@ kernel` signatures check green** (spike
   `scripta/spike-shape-generic-kernel/REPORT.md`, 2026-08-26): the reds
   are codegen entry-discovery/linkage (uninstantiated or imported kernel
   entries, kernel-calls-kernel at Metal) — wave-3/SGD-1 territory, not a
   check-level blocker. Consequence adopted below: composing surfaces
   (`swiglu` typed, any block-level assembly) are `@ public`, never
   `@ kernel`; self-contained leaves stay `@ kernel`.
5. **SEM008 (size-param forwarding) still pins the dense REF-01 runners**
   to literal sizes (`forward_ref01` family, `dense.fab:557+`); the need
   rules: do not wait on it — the gather statues die regardless.

### Environment truth (planning-time observation)

`faber check` is green on gradus main `bf55937` with the PATH binary
(`faber 1.8.0`, `FABER_LIBRARY_HOME=/Users/ianzepp/work/faberlang`) —
re-verified 2026-08-28; wave-1's "no built radix faber" note is stale for
check purposes. No `radix/target/**/faber` exists; if the PATH binary drifts
red against a later radix tip, rebuilding radix is the lane precondition,
never a child-Hand concern. Untracked foreign dirt:
`scripta/spike-shape-generic-kernel/spike2-local-generic.metal` (spike
artifact, no owner needed — leave it).

## Locked rulings and defaults (planner; evidence-cited)

1. **Carrier renames.** SEM005 forces one name per symbol; the need spells
   the typed twins `mse<M,N>` / `layernorm<T,D>` and nn.fab's PML3-U1 note
   calls layernorm "still-staged". Default: typed twins take the plain
   names; staged `mse`/`layernorm`/`swiglu` become `mse_carrier` /
   `layernorm_carrier` / `swiglu_carrier` (the `add_carrier` precedent).
   The need's "staged mse stays" / "staged nn.swiglu remains load-edge" is
   satisfied by the carrier-named residual. Alternative (suffix the typed
   twins `_static`, the attention precedent) rejected: contradicts the
   need's spellings and the PML3-U1 production direction.
2. **`linear_channel<M,K,N>`** is the per-channel twin's name (house
   vocabulary "per-channel"; family-suffix precedent `swiglu_hidden`,
   `scaled_dot_product_static`). Open question 1 offers the rename path if
   the operator wants another spelling.
3. **One public step name.** Publicize `_sgd_family` as
   `optimize.sgd_step<Figura>`; do NOT also mint `train.train_step<Figura>`
   (pure alias; smallest correct code). This supersedes wave-1's "no new
   public sgd_step" lock — that lock covered wave 1, where `_sgd_family`
   was only an internal delegation target; wave 2's need explicitly lists
   `sgd_step<Figura>` as a twin to author because external callers lose
   `train_step_*`.
4. **No public bert block replacement.** `bert_tiny_block_2x8` is an
   assembler; the amendment's law is leaves-only + instantiations at call
   sites, and both bert exempla already carry the leaf-composed path
   structurally. The public transformer row remains the staged
   `transformer_block` (PML3-U3, carrier tier, untouched). If Mind wants a
   typed `bert_tiny_block<B,D>` `@ public` assembler anyway, that is an
   explicit amendment (open question 2).
5. **Typed swiglu is `@ public`, not `@ kernel`** — it composes
   `swiglu_hidden` + `linear_channel`; kernel-calls-kernel is a Metal red
   (fact 4). Same rule for any composed surface.
6. **`layernorm<T,D>` takes explicit `f32 ε`** (matching `rmsnorm<T,D>`);
   the fixed wrapper's hardcoded `1e-5` moves to call sites.
7. **gather branch** follows the need verbatim (U9): probe the typed pin;
   if SEM016 still rejects in nn.fab library context, record the red
   verbatim, keep `gather_carrier`, still kill the dense statues. Escalate
   SEM016 as a radix need only if the typed pin is the only honest path
   for a live consumer — none is identified today.

## Units

One function family (or one shared caller surface) per unit. Commit
ordering inside the wave: twins land before callers move; callers move
before deletions; no consumer is ever stranded. Commits path-limited per
repo (`gradus` and `faberlang/examples` are separate repositories).

---

### GCB-W2-U1 — nn typed `layernorm<T,D>` + staged rename to `layernorm_carrier`

| field | value |
| --- | --- |
| `id` | GCB-W2-U1 |
| `outcome` | In `src/nn.fab`: add `@ kernel @ public fn layernorm<size T, size D>(tensor<f32, [T, D]> x, tensor<f32, [D]> scale, tensor<f32, [D]> offset, f32 ε) → tensor<f32, [T, D>]` with body `x.layer_norm(1, ε, scale, offset)` (the proven `layernorm_2x8` op, the `rmsnorm<T,D>` twin shape — infallible, no `⇥`). Rename the staged `layernorm(NumericBlock…)` to `layernorm_carrier` (comment header updated to the `rmsnorm_carrier` posture). Ripple the rename in the same unit: `src/transformer.fab:318` (`_layernorm` wrapper), `exempla/nn-bridge/src/main.fab:92` (staged row), `src/nn.proba` (staged calls + any header wording). `layernorm_2x8` itself is untouched (U11 deletes it after callers move) |
| `write_scope` | gradus only: `src/nn.fab`, `src/transformer.fab`, `src/nn.proba`, `exempla/nn-bridge/src/main.fab`, `exempla/nn-bridge/README.md` (staged-row wording) |
| `done_when` | `grep -n "fn layernorm" src/nn.fab` shows exactly two declarations: the typed twin and `layernorm_carrier`; `grep -rn "nn\.layernorm(" src/ exempla/` (open paren, excluding `layernorm_2x8`/`layernorm_carrier`) returns zero live calls; `faber check` green on gradus + `exempla/nn-bridge`; `layernorm_2x8` still present and untouched |
| `depends_on` | none |
| `sanity` | `faber check` on gradus root + nn-bridge; `faber test` row for the typed twin in nn.proba pins the accepted `layernorm_2x8` oracle values (row-5 numbers already in `nn.proba:340+`) |
| `non_goals` | standing set + no `layernorm_2x8` edit/delete, no bert caller moves (U8), no api-reference edit (U14) |
| `risk` | low — every op is a live method (`x.layer_norm` proven at `nn.fab:125`; `rms_norm` twin at `:441-444` same shape) |
| `integrable` | yes |

---

### GCB-W2-U2 — nn typed `linear_channel<M,K,N>` (per-channel bias twin)

| field | value |
| --- | --- |
| `id` | GCB-W2-U2 |
| `outcome` | In `src/nn.fab`: add `@ kernel @ public fn linear_channel<size M, size K, size N>(tensor<f32, [M, K]> x, tensor<f32, [K, N]> w, tensor<f32, [N]> b) → tensor<f32, [M, N]>` with body `(x · w).added_bias(b)` (the `linear_2x8` contract, generic — fact 2 forces the separate symbol). Update the linear family comment (`:295-299`) and the formula note (`:62-66`) so the per-channel contract names `linear_channel`, not "stays on linear_carrier". Add nn.proba typed rows pinning the accepted `linear_2x8` oracle (identity weight + per-channel bias, values already in `nn.proba:231+` staged row) |
| `write_scope` | gradus only: `src/nn.fab`, `src/nn.proba` |
| `done_when` | `linear_channel<size M, size K, size N>` declared `@ kernel @ public` with the `.added_bias` body; nn.proba has a typed row pinning the row-4 oracle values; `faber check` green on gradus; `linear_2x8` untouched |
| `depends_on` | GCB-W2-U1 (nn.fab serialization — the need's shared-hot-module rule) |
| `sanity` | `faber check` gradus root; the new proba row |
| `non_goals` | standing set + no `linear_2x8` edit, no overload attempt on `linear` (SEM005), no carrier change |
| `risk` | low |
| `integrable` | yes |

---

### GCB-W2-U3 — loss typed `mse<M,N>` + staged rename to `mse_carrier`

| field | value |
| --- | --- |
| `id` | GCB-W2-U3 |
| `outcome` | In `src/loss.fab`: add `@ kernel @ public fn mse<size M, size N>(tensor<f32, [M, N]> prediction, tensor<f32, [M, N]> target) → f32` with the exact zoo body (`residual ← p − t; squared ← residual ⊙ residual; return squared.mean()` — identical to `mse_2x2/4x4/2x8`, statement-for-statement). Rename the staged `mse(NumericBlock…)` to `mse_carrier`; ripple `src/loss.proba:94,102,110` and `src/metrics.proba` staged calls; add typed proba rows pinning the three accepted oracle values (7.5 / 93.5 / 15.875 — already asserted by the staged rows). Header formula notes updated to name both tiers |
| `write_scope` | gradus only: `src/loss.fab`, `src/loss.proba`, `src/metrics.proba` |
| `done_when` | `grep -n "fn mse" src/loss.fab` shows exactly the typed twin + `mse_carrier`; zero live `loss.mse(` staged calls outside `mse_carrier`/`mse_2x2`-family names (grep over `src/`, probas included); typed proba rows pin the three oracles; `faber check` green on gradus; `mse_2x2/4x4/2x8` untouched |
| `depends_on` | none (parallel-safe with U1: disjoint files) |
| `sanity` | `faber check` gradus root; new typed rows |
| `non_goals` | standing set + no `mse_2x2/4x4/2x8` deletion (U10), no cross_entropy change |
| `risk` | low — body is three live typed ops already proven by three `@ kernel` functions |
| `integrable` | yes |

---

### GCB-W2-U4 — optimize public `sgd_step<Figura>` (rename `_sgd_family`)

| field | value |
| --- | --- |
| `id` | GCB-W2-U4 |
| `outcome` | Rename `@ public fn _sgd_family<size Figura>` (`src/optimize.fab:124`) to `sgd_step` — the list-driven `param − lr·grad` body unchanged. Update the four live delegation call sites in `src/train.fab` (`train_step_2x2`, `train_step_4x4`, `train_step_bert_linear`, `train_step_bert_layernorm` bodies — signatures and tuple contracts unchanged), `src/optimize.proba` (the W1-U3 `_sgd_family` rows), and the `train.proba`/`optimize.fab`/`train.fab` comment wordings that name `_sgd_family`. No other behavior change; `train_step_*` still exist here (U12 deletes them) |
| `write_scope` | gradus only: `src/optimize.fab`, `src/train.fab`, `src/optimize.proba`, `src/train.proba` (wording where it names `_sgd_family`) |
| `done_when` | `grep -rn "_sgd_family" src/ exempla/` returns zero live occurrences (historical ledger comments excepted, each marked as history); `sgd_step<size Figura>` is `@ public` with the unchanged body; all four `train_step_*` signatures unchanged and their proba rows still pass; `faber check` green on gradus |
| `depends_on` | none (parallel-safe with U1/U3: disjoint files) |
| `sanity` | `faber check` gradus root; `faber test` on the optimize/train proba rows |
| `non_goals` | standing set + no `train_step<Figura>` alias minted (locked ruling 3), no train_step deletion (U12), no SgdState/`step`/wire surface change |
| `risk` | low — pure rename of a proven surface; probe-interface viability proven by `train.proba:909,:922` |
| `integrable` | yes |

---

### GCB-W2-U5 — nn typed `swiglu<T,F,N>` + staged rename to `swiglu_carrier`

| field | value |
| --- | --- |
| `id` | GCB-W2-U5 |
| `outcome` | In `src/nn.fab`: add `@ public fn swiglu<size T, size F, size N>(tensor<f32, [T, F]> gate, tensor<f32, [T, F]> up, tensor<f32, [F, N]> down_weight, tensor<f32, [N]> down_bias) → tensor<f32, [T, N]>` with body composing the typed leaves: `linear_channel(swiglu_hidden(gate, up), down_weight, down_bias)` — `@ public` NOT `@ kernel` (locked ruling 5; kernel-calls-kernel is a Metal red, fact 4). Rename staged `swiglu(NumericBlock…)` (`src/nn.fab:575`) to `swiglu_carrier`; ripple `src/transformer.fab:418`, `src/model/moe.fab:289`, `exempla/dense-swiglu/src/main.fab:85`, `src/nn.proba`. Family comment updated to name both tiers and the absent-bias typed route (`·` + `swiglu_hidden` at call site) |
| `write_scope` | gradus only: `src/nn.fab`, `src/transformer.fab`, `src/model/moe.fab`, `src/nn.proba`, `exempla/dense-swiglu/src/main.fab` |
| `done_when` | `grep -n "fn swiglu" src/nn.fab` shows `swiglu_hidden` (kernel), typed `swiglu` (public, composing), and `swiglu_carrier`; zero live staged `nn.swiglu(` calls (grep over `src/ exempla/` excluding `swiglu_carrier`/`swiglu_hidden` returns nothing); `faber check` green on gradus + `exempla/dense-swiglu`; moe proba rows still pass |
| `depends_on` | GCB-W2-U2 (nn.fab serialization; the body calls `linear_channel`) |
| `sanity` | `faber check` gradus root + dense-swiglu |
| `non_goals` | standing set + no `@ kernel` on the composed surface, no carrier body change, no dense/moe route changes beyond the rename |
| `risk` | medium — first library-generic-composing-generic over `@ kernel` leaves on the FMIR stepper (library-to-library generic calls are proven by `_sgd_family` ← `train_step_*`, but not yet leaf-on-leaf); stop condition below |
| `integrable` | yes |

---

### GCB-W2-U6 — mlp generic `forward_mlp_loss<M,K,H,N>` + exemplum move

| field | value |
| --- | --- |
| `id` | GCB-W2-U6 |
| `outcome` | In `src/mlp.fab`: generalize `forward_mlp_loss` to `<size M, size K, size H, size N>` — `input [M,K]`, `weight1 [K,H]`, `bias1 [M,H]`, `weight2 [H,N]`, `bias2 [M,N]`, `target [M,N]` → `f32`; annotations `@ radix { lane = "air" }` + `@ radix backward "forward_mlp_loss_backward"` unchanged; body ops unchanged (they are already pure glyph/method ops). The companion ABI follows the generic (fact 3 precedent: `simple_loss<size R, size C>` + `loss_backward`, `src/gradient.fab:216-219`). Same unit (same repo): move `exempla/training-loop-mlp/src/main.fab:305,316` call + companion call onto the generic at the existing `[4,4]` instantiation — values, pins, and printed losses unchanged. `mlp.proba` comment wording only if it names the frozen signature |
| `write_scope` | gradus only: `src/mlp.fab`, `src/mlp.proba` (comments), `exempla/training-loop-mlp/src/main.fab` |
| `done_when` | `forward_mlp_loss` declares the four size params with the shapes above; no `[4, 4]` literal remains in its signature; the exemplum's forward/backward calls typecheck unchanged in value; `faber check` green on gradus + `exempla/training-loop-mlp`; `faber run` on the exemplum reproduces its printed loss trace (merge-owned run proof, recorded honestly) |
| `depends_on` | none among U1-U5 (mlp.fab is disjoint); lands BEFORE U7 (training-loop-mlp file serialization) |
| `sanity` | `faber check` gradus root + training-loop-mlp |
| `non_goals` | standing set + no `forward_mlp` (staged) change, no new `@ radix backward` sites, no exemplum fixture/value edits |
| `risk` | medium — generic `@ radix backward` is precedented (`simple_loss<R,C>`) but not at this arity; if companion generation rejects the generic source, record the exact red and stop (the frozen form stays until Mind routes a radix ruling; do NOT keep a `[4,4]` public twin beside a private generic) |
| `integrable` | yes |

---

### GCB-W2-U7 — non-bert callers move (linear-regression, mlp, training-loop-mlp, nn-bridge rows)

| field | value |
| --- | --- |
| `id` | GCB-W2-U7 |
| `outcome` | Every non-bert zoo caller names generics: `loss.mse_2x2`/`mse_4x4` → `loss.mse` (shape params unify from `[2,2]`/`[4,4]` args); `train.train_step_2x2`/`_4x4` → `optimize.sgd_step` list form (pack `[weight, bias]`/4-element list, unpack by index — the `train.fab:129-130` `upd[i]` precedent; Latin surface preserved); nn-bridge `linear_2x8` row → `nn.linear_channel` (drop the bridge `fac/cape` arm — the twin is infallible, the W1-U1 precedent), `layernorm_2x8` row → `nn.layernorm` + explicit `0.00001 ∷ f32` (drop the arm); training-loop-mlp `train_step_4x4` → `optimize.sgd_step`. Files: examples `linear-regression/{src/train.fab,oracle/capture.fab}`, `mlp/{src/train.fab,oracle/capture.fab}`; gradus `exempla/training-loop-mlp/{src/main.fab,README.md}`, `exempla/nn-bridge/{src/main.fab,README.md}` (row list + route wording) |
| `write_scope` | both repos, path-limited per repo (files in `outcome`) |
| `done_when` | Zero live calls to `mse_2x2`, `mse_4x4`, `train_step_2x2`, `train_step_4x4`, `nn.linear_2x8`, `nn.layernorm_2x8` across those files (grep; pin labels may keep historical row names as provenance); `faber check` green on `linear-regression`, `mlp`, `exempla/nn-bridge`, `exempla/training-loop-mlp`; `[device]` fixtures and Latin surface untouched; bridge README rows match reality |
| `depends_on` | GCB-W2-U1, GCB-W2-U2, GCB-W2-U3, GCB-W2-U4, GCB-W2-U6 |
| `sanity` | `faber check` on the four packages |
| `non_goals` | standing set + no bert edits (U8), no library deletions, no oracle `reference.json` edits |
| `risk` | medium — `mlp` is a device program whose loss/step call sites change (first typed-`mse`/`sgd_step` package consumers); KRS-2's specialization red was fixed-shape-kernel-wrapping-generic, not package calls (W1-U1 proved the package route); on any check red record the error and stop per stop-condition law |
| `integrable` | yes |

---

### GCB-W2-U8 — bert callers move (bert-tiny-fragment, bert-gradus-probe)

| field | value |
| --- | --- |
| `id` | GCB-W2-U8 |
| `outcome` | Both bert exempla compose generic leaves at the call site: `nn.layernorm_2x8` → `nn.layernorm` (+ explicit ε; delete every `fac/cape` arm — twins infallible), `nn.linear_2x8` → `nn.linear_channel` (delete arms), `loss.mse_2x8` → `loss.mse`, `train.train_step_bert_linear`/`_layernorm` → two `optimize.sgd_step` calls (6-weight + 6-bias + 6-LN lists) with index re-pack at the call site. In bert-gradus-probe: retire the `bert_tiny_block_2x8` full-block call (`src/train.fab:351`) AND the block-vs-leaves agreement traces (`block_trace`/`diff_trace`/`diff_mean` block) — with the block deleted (U13) the comparison loses its subject; the leaf-composed path becomes THE forward. Oracle capture files move with their source call sites; `bert-tiny-fragment/oracle/README.md:21-23` rows reworded to the generic surface |
| `write_scope` | examples repo only: `bert-tiny-fragment/{src/train.fab,oracle/capture.fab,oracle/README.md}`, `bert-gradus-probe/src/train.fab` |
| `done_when` | Zero live calls to `layernorm_2x8`, `linear_2x8`, `mse_2x8`, `train_step_bert_linear`, `train_step_bert_layernorm`, `bert_tiny_block_2x8` in those files (grep); no `fac/cape` arm remains around a former nn leaf call; `faber check` green on both bert packages; `[device]` fixtures, Latin surface, and numeric fixtures untouched |
| `depends_on` | GCB-W2-U1, GCB-W2-U2, GCB-W2-U3, GCB-W2-U4 |
| `sanity` | `faber check` on both bert packages |
| `non_goals` | standing set + no `transformer.fab` edit (U13), no backward-companion edits (their inputs are the same typed tensors), no probe purpose change beyond the retired block comparison |
| `risk` | medium — largest call-site rewrite (12+6 slot re-pack); mechanical but wide; on any check red record and stop |
| `integrable` | yes |

---

### GCB-W2-U9 — dense gather statues die (typed `nn.gather<T,V,D>` probe branch)

| field | value |
| --- | --- |
| `id` | GCB-W2-U9 |
| `outcome` | Branch unit, need-ordered. **(a) probe first:** attempt `@ public fn gather<size T, size V, size D>(tensor<f32, [V, D]> table, list<int> ids) → tensor<f32, [T, D]> ⇥ NnError` in `src/nn.fab` — body stages nothing, walks `ids` (the `gather_carrier` index math on typed storage) and pins the output via the `_pin_same<size A, size B>` do/catch pattern (`src/model/dense.fab:394`, fact 3); NOT `@ kernel` (list loop + pin; nn.fab `:459` posture). If it checks: add nn.proba rows, delete BOTH dense statues, and route their five callers (`dense.fab:512, :537, :577, :605, :638`) onto `nn.gather<2, 8, 16>` / `<1, 8, 16>`. **(b) if SEM016 still rejects** the typed pin in library context: record the exact red verbatim in the nn.fab header (append-only), keep `gather_carrier` as the residual, STILL delete both statues and route the five callers through the in-module carrier + typed cast (`_collect`/`nn.gather_carrier` → `_pin_same` / `↦ tensor<f32, [2, 16]>` do/catch — the `probe_inferred_leaves` precedent at `dense.fab:550-563`). Either branch: file the SEM016 evidence to Mind; escalate as a radix need only per locked ruling 7 |
| `write_scope` | gradus only: `src/model/dense.fab`, `src/nn.fab` (branch a), `src/nn.proba` (branch a) |
| `done_when` | `grep -n "fn gather\b\|fn gather_step" src/model/dense.fab` returns nothing (both statues gone); the five runner sites typecheck with typed `[2,16]`/`[1,16]` locals unchanged; branch outcome recorded in the delivery ledger (typed twin landed OR verbatim SEM016 red + carrier residual); `faber check` green on gradus; dense.proba REF-01 rows (`:495-575`) still pass — they cover the rerouted runners |
| `depends_on` | GCB-W2-U5 (nn.fab serialization for branch a) |
| `sanity` | `faber check` gradus root; dense.proba REF-01 describes |
| `non_goals` | standing set + no SEM008 campaign (runners stay literal-size), no `gather_carrier` body change, no embedding/route semantics change |
| `risk` | medium — branch (a) probes a compiler boundary; branch (b) is fully precedented. Both branches kill the statues, so the need's DONE-WHEN holds either way |
| `integrable` | yes |

---

### GCB-W2-U10 — loss zoo deletion (`mse_2x2` / `mse_4x4` / `mse_2x8`)

| field | value |
| --- | --- |
| `id` | GCB-W2-U10 |
| `outcome` | Delete the three functions + their section comments from `src/loss.fab` (`:270-306`); append the retirement to the header ledger (rows 7-9 marked retired/instantiated-at-call-site, historical text preserved). No proba rewrite needed (U3 already moved the staged rows and added typed rows; no proba ever called the trio — verified) |
| `write_scope` | gradus only: `src/loss.fab` |
| `done_when` | `grep -n "mse_2x2\|mse_4x4\|mse_2x8" src/loss.fab` returns only explicitly-marked retirement provenance; `faber check` green on gradus; typed `mse<M,N>` + `mse_carrier` untouched |
| `depends_on` | GCB-W2-U7, GCB-W2-U8 (all mse callers moved) |
| `sanity` | `faber check` gradus root |
| `non_goals` | standing set + no cross_entropy / carrier edits |
| `risk` | low |
| `integrable` | yes |

---

### GCB-W2-U11 — nn zoo deletion (`linear_2x8` / `layernorm_2x8`)

| field | value |
| --- | --- |
| `id` | GCB-W2-U11 |
| `outcome` | Delete `linear_2x8` (`src/nn.fab:107-116`) and `layernorm_2x8` (`:119-127`) with their section comments; append the retirement to the PML0-U3 header ledger (rows 4-5 marked retired — the generic surface names `linear_channel` / `layernorm`); update the S6-G1 header note (`:13-16`) and formula comments (`:62-74`) so current prose names the typed twins, historical mentions marked. `_staged` is already gone (arc #5) — nothing else to reap |
| `write_scope` | gradus only: `src/nn.fab` |
| `done_when` | `grep -n "linear_2x8\|layernorm_2x8" src/nn.fab` returns only explicitly-marked retirement provenance; no current contract comment names either wrapper; `faber check` green on gradus + `exempla/nn-bridge` + both bert packages (post-U8 world) |
| `depends_on` | GCB-W2-U7, GCB-W2-U8 |
| `sanity` | `faber check` gradus root + nn-bridge |
| `non_goals` | standing set + no carrier deletions, no nn.proba oracle-provenance name edits beyond what U1 already touched |
| `risk` | low — post-caller deletion; census verified no other caller |
| `integrable` | yes |

---

### GCB-W2-U12 — train zoo deletion (`train_step_*` quartet) + train.proba rewrite

| field | value |
| --- | --- |
| `id` | GCB-W2-U12 |
| `outcome` | Delete `train_step_2x2` (`src/train.fab:63-71`), `train_step_4x4` (`:73-84`), `train_step_bert_linear` (`:85-99`), `train_step_bert_layernorm` (`:100-115`) with section comments; rewrite `train.proba:875-926` (four direct tests) as `optimize.sgd_step` list-form pins of the same `param − lr·grad` oracle values (index-unpacked asserts); reword the module header S4-A/S6-G1 notes and the PML0-U3 ledger rows 16-17 (append-only retirement); `optimize.fab` delegation-truth comments updated (no more "train_step_* delegates through this" — callers call it directly now) |
| `write_scope` | gradus only: `src/train.fab`, `src/train.proba`, `src/optimize.fab` (comments) |
| `done_when` | `grep -rn "train_step_2x2\|train_step_4x4\|train_step_bert" src/ exempla/` returns only explicitly-marked retirement provenance; the four rewritten proba rows pass; `faber check` green on gradus + `exempla/training-loop-mlp` |
| `depends_on` | GCB-W2-U7, GCB-W2-U8 (and transitively U4) |
| `sanity` | `faber check` gradus root; `faber test` the rewritten rows |
| `non_goals` | standing set + no Schedule/mode/RNG/checkpoint surface change, no sgd_step body change |
| `risk` | low |
| `integrable` | yes |

---

### GCB-W2-U13 — transformer deletion (`bert_tiny_block_2x8`) + proba rewrite

| field | value |
| --- | --- |
| `id` | GCB-W2-U13 |
| `outcome` | Delete `bert_tiny_block_2x8` (`src/transformer.fab:59-110`) with its section comment and the LEGACY FIXED-SHAPE NOTE (`:28-31`); rewrite `transformer.proba:456-460` (pinned-bytes block test) as a leaf-composition pin — compose `nn.layernorm` + `nn.linear_channel` + `attention.scaled_dot_product_static` + `nn.gelu` inline in the test at `[2,8]` and pin the same bytes (the composition IS the U8 exemplum path, so the values are identical by construction); PML0-U3 ledger row 15 marked retired (append-only); the PML3-U3 production-surface prose that cites the block as "matching the accepted fragment arithmetic" keeps the historical framing explicitly marked |
| `write_scope` | gradus only: `src/transformer.fab`, `src/transformer.proba` |
| `done_when` | `grep -n "bert_tiny_block_2x8" src/transformer.fab` returns only explicitly-marked retirement provenance; the rewritten proba row pins the same oracle bytes via leaf composition and passes; `faber check` green on gradus + `examples/training/bert-gradus-probe` (post-U8 world) |
| `depends_on` | GCB-W2-U8 (the probe no longer names the block; also U1/U2 transitively for the leaf names) |
| `sanity` | `faber check` gradus root |
| `non_goals` | standing set + no staged `transformer_block`/carrier surface change, no new public assembler (locked ruling 4) |
| `risk` | low-medium — the proba rewrite must reproduce pinned bytes through six leaf calls; the arithmetic is statement-identical (the block body and the leaf bodies are the same ops), tolerance rows already exist |
| `integrable` | yes |

---

### GCB-W2-U14 — docs closeout (both repos + pml0 ledger marks)

| field | value |
| --- | --- |
| `id` | GCB-W2-U14 |
| `outcome` | Public-surface docs stop advertising the zoo and describe the generic surface. Gradus: `docs/api-reference.md` — delete `:490-492` (mse trio), `:989-990` (linear_2x8/layernorm_2x8), `:1329-1332` (train_step quartet), `:1380` (bert_tiny_block_2x8); replace `:561` with the generic `forward_mlp_loss<size M, size K, size H, size N>` signature; rename staged entries to `mse_carrier` / `layernorm_carrier` / `swiglu_carrier` (`:999` etc.); ADD entries for typed `mse<M,N>`, `layernorm<T,D>`, `linear_channel<M,K,N>`, typed `swiglu<T,F,N>`, `sgd_step<Figura>`, and (branch a) `gather<T,V,D>`. `README.md` — `:105,:114` quickstart snippet → `loss.mse`; `:130` route prose → `optimize.sgd_step`; `:246-247` module rows → generic names. `docs/quickstart.md:57,:66` same. `docs/api-shape-policy.md:48-49` — the admitted-rows row now cites zero `_NxM` examples (typed twins are the production tier; `*_carrier` the staged tier; exception list = abs/signum SEM004 + SEM014 carriers + any recorded SEM016 residual). `docs/module-map.md:96` mlp row wording. `src/tensor.fab:90-107` census ledger — append the wave-2 retirement (rows 4,5,7-9,15-17). `src/gradus.fab:52-60` facade note → generic surface. `docs/factory/production-ml-library/pml0-proof-api-ledger.md:35-48` — append-only marks on rows 4, 5, 7-9, 15-17: retired GCB-W2, instantiated at call sites (per the need: the rows become instantiations, not keep-reasons). Examples repo: `linear-regression/oracle/README.md:23`, `mlp/oracle/README.md:26,:218` → `loss.mse` + `optimize.sgd_step` wording (surviving historical names in frozen evidence excepted) |
| `write_scope` | both repos, path-limited: gradus `README.md`, `docs/{api-reference,api-shape-policy,module-map,quickstart}.md`, `src/tensor.fab` (comment), `src/gradus.fab` (comment), `docs/factory/production-ml-library/pml0-proof-api-ledger.md` (append-only marks); examples `linear-regression/oracle/README.md`, `mlp/oracle/README.md` |
| `done_when` | Cross-repo census grep (`_2x2\|_2x8\|_4x4\|train_step_\|bert_tiny_block\|forward_mlp_loss\[4,4\]\|gather_step` over `*.fab *.proba *.md *.toml`, both repos) returns zero **current public-surface claims** outside the enumerated exclusion set: (a) frozen evidence (oracle `reference.json`/receipts, benchmark baselines, `docs/archived/**`, `docs/deep-code-review-*`, landed `docs/factory/**` campaign paper except the pml0 marks this unit owns); (b) explicitly-marked retirement provenance in src ledger comments (U10-U13 done-whens); (c) nn-bridge baseline-red record. Every replacement names its destination (mse → `loss.mse<M,N>`, steps → `optimize.sgd_step<Figura>`, bert leaves → `nn.layernorm<T,D>`/`nn.linear_channel<M,K,N>`); api-reference lists every new typed symbol and no deleted one |
| `depends_on` | GCB-W2-U9, GCB-W2-U10, GCB-W2-U11, GCB-W2-U12, GCB-W2-U13 |
| `sanity` | the cross-repo census grep with current-claim classification |
| `non_goals` | standing set + no source-code edits beyond the two comment-only files, no bert oracle README (U8 owns it), no frozen-evidence edits |
| `risk` | low |
| `integrable` | yes |

---

## Order and parallelism

```
U1 (nn layernorm twin) ─┐
U3 (loss mse twin) ─────┤
U4 (sgd_step public) ───┼──> U7 (non-bert callers) ──┐
U2 (linear_channel) ────┘      U8 (bert callers) ────┤
U6 (mlp generic) ───────────> (serialized on the     ├─> U10 (loss del) ─┐
U5 (nn swiglu twin) ──────> U9 (gather statues) ─────┘   U11 (nn del) ────┼─> U14 (docs)
                                                            U12 (train del) ┤
                                                            U13 (xformer del)
```

- U1 ∥ U3 ∥ U4 ∥ U6 (disjoint files). U2 after U1; U5 after U2; U9 after U5
  (nn.fab is the shared hot module — the need's serialization rule; loss.fab
  serializes U3 → U10).
- U7 after the whole twin bank + U6 (training-loop-mlp file serialization);
  U8 after U1-U4 (needs no U6). U7 ∥ U8 (disjoint files, same examples repo
  — path-limited commits).
- U10 ∥ U11 ∥ U12 ∥ U13 after their callers; U9 independent of U7/U8.
- U14 last.

## Integration / merge gate

No unit is non-integrable alone: twin units leave the zoo alive and
everything green; caller units leave both spellings compiling; deletion
units land only after their callers. Merge owns the aggregate closeout:
cross-repo landing order twin bank (U1-U6) → U9 → callers (U7/U8) →
deletions (U10-U13) → U14, with `./scripta/check-compile` green on gradus
main at each gradus-repo commit and `faber check` on the four
`faberlang/examples` packages at each examples-repo commit. The wave closes
only when the P2 done-when greps hold and the run proofs are recorded
(baseline reds stay baseline: the nn-bridge `linear_2x2` matmul red; any
`@ kernel` run-route refusal).

## Lane-owned validation (named once — not on any card)

- lint: `./scripta/check-source`
- test: `./scripta/check-compile` (package-aware `faber check` over gradus
  + consumer exempla) and `faber test` on the gradus package
- merge: `faber check` + `faber run` on `exempla/{nn-bridge,
  training-loop-mlp, dense-swiglu}` and `examples/training/{linear-
  regression,mlp,bert-tiny-fragment,bert-gradus-probe}` after the wave
  closes; run results recorded honestly; `faber check` is green on main
  today (PATH `faber 1.8.0`, §Env) — if a later radix tip drifts the binary
  red, rebuild radix first (lane precondition)

## Open questions for Mind

1. **`linear_channel` spelling** (locked ruling 2). Default
   `nn.linear_channel<M,K,N>`; alternatives the operator may prefer:
   `linear_bias`, or promoting per-channel to THE `linear` bias contract
   (breaks wave-1-moved same-shape callers — not recommended). Rename is a
   one-unit mechanical change any time before U7.
2. **Typed bert block assembler** (locked ruling 4). Default: none minted;
   the staged `transformer_block` remains the public transformer row and
   the exempla compose leaves. If the operator wants a typed
   `bert_tiny_block<B,D>` `@ public` assembler, amend the need — it is a
   small follow-up unit after U1/U2, not a blocker.
3. **`train.train_step<Figura>` alias** (locked ruling 3). Default: not
   minted; `optimize.sgd_step<Figura>` is the single public step name. Say
   the word if exempla should keep a train-module entry point.
4. **U9 branch outcome** is reported by the Hand either way; only a
   branch-(b) red with a live typed-gather consumer would justify the
   SEM016 radix need (none identified today).

## Ledger

Machine-managed — unit, status, seat, receipt, notes. Mind files Hands
from this graph; planner does not task seats.

| Unit | Status | Seat | Receipt | Notes |
| --- | --- | --- | --- | --- |
| GCB-W2-U1 … GCB-W2-U14 | pending | — | none | 14 units; twins U1-U6+U9a, callers U7-U8, deletions U10-U13, docs U14 |
