# Deep Code Review — 2026-08-21

**Scope:** all of `src/**/*.fab` (~30K lines) plus `tests/admission_conformance.fab`, reviewed against README claims, repo rules (`AGENTS.md`), and canonical-Faber style canon.
**Tree state:** `main` @ `1697a19` ("docs(factory): archive train-step-optimizer-call").
**Method:** three parallel deep-read slices (training, inference, model-admission), every headline finding re-verified by direct read of the cited lines before inclusion.
**Compile tier:** `./scripta/check-compile` **green** (warnings only, in exempla).
**Source gate:** `./scripta/check-source` **RED at HEAD** — see B7.

Severity keys: **B#** confirmed bug · **G#** gate violation · **S#** style · **O#** observation.

---

## Confirmed bugs

### B1 · nn.fab fixed-shape bridges fail open

`src/nn.fab:121-156`, `:183-196`, `:431-434`

Every fixed-shape bridge wraps its production call in nested do/catch and swallows both error channels:

```fab
fn gelu_4x4(tensor<f32, [4, 4]> x) → tensor<f32, [4, 4]> {
    do {
        const tensor.Tensor y ← gelu(_staged(x ↦ list<f32>, [4, 4]))
        do { return y.data ↦ tensor<f32, [4, 4]> }
        catch conv { return x }
    }
    catch err { return x }
}
```

Same swallow-and-echo-input shape at `gelu_2x8` (:189-195), `linear_2x8` (:149-155), `layernorm_2x8` (:170-176); `linear_from_raw` (:431-434) returns an empty typed tensor instead. A training loop fed these never errors — it silently trains identity-for-GELU or a no-op projection. Contradicts the typed-`NnError` discipline used by every other function in the same file, and the library capsule rule against silent tolerance.

**Fix:** thread `⇥ NnError` through the bridge surface (exempla already handle typed errors); if the legacy caller surface cannot grow `⇥`, fail loud rather than echo input.

### B2 · Safetensors container framing deviates from the reference format (off-by-8)

`src/model/safetensors.fab:33-35` (comment), `:361-379` (parser), `:910`; `fixtures/safetensors/gen_fixture.py:76-79`

The module stores the u64 length field as *prefix + JSON* and slices JSON at `[8, header)`:

```fab
const int header ← buf[0‥8] ↦ int<u64, Le> ↦ int
require header ≥ 8 throw variant BadFormat {…}
…
for range 8‥header const i { … }
```

The Safetensors reference format defines N as the JSON-header size **excluding** the 8-byte prefix (JSON occupies `[8, 8+N)`, data begins at `8+N`). Consequence: real HF-tooling-produced `.safetensors` files parse a header truncated by 8 bytes → walk fails → `BadFormat`. Direction is fail-closed and the stack is internally self-consistent (generator, oracle hash, probas share the local convention — which is why ~35 green reject rows never caught it), but interop with actual artifacts is broken and the charter comment asserts a false fact about the "reference format".

**Fix:** read N as JSON-only length, JSON span `[8, 8+N)`, `data_length ← corpus.length() - 8 - N`, keep the alignment check; regenerate fixture + oracle hash together. Or document the private variant honestly if reference interop is out of scope.

### B3 · cache extend/append partially mutate the caller's cache (fail-open)

`src/cache.fab:445-448` (`extend`), `:410-411` (`append`)

```fab
var list<int> new_history ← c.history()
for from tokens const token_id {
    require token_id ≥ 0 throw variant IdOutOfRange {message = "token id must be non-negative"}
    new_history.append(token_id)
}
```

Runner lists are shared references on the executed surface (radix-mir-runner `value.rs:60` `Array(Rc<RefCell<Vec<Value>>>)`; `Append` mutates through the cell, `runtime.rs:1001`). `new_history` aliases `c`'s live history, so for `tokens = [5, -1]` the first token is appended to the **input cache** before the second throws. The rejected write leaves `c.length() = N+1` vs `_row_count = N` → every future write through that handle fails `Gap` (`cache.fab:348`) forever. Violates the module contract "a rejected write leaves rows, capacity, and generation unchanged" (`cache.fab:38-40`) and the extend doc "reject before any new rows exist" (`:434`). In `append` (:410-411), even a *successful* append grows the old handle's visible length without bumping its version, stranding it.

**Fix:** build a fresh history list element-by-element (pattern exists at `decode.fab:664-668`, `sampling.fab:407-410`). Caveat stated honestly: HIR→Rust carriers are owned `Vec`s so the app lane may mask this; the FMIR stepper — the surface gradus headers name — does not.

### B4 · top-k zeroes dropped logits pre-softmax instead of removing them

`src/sampling.fab:450-458`; contract text `:37`; pins `sampling.proba:31-32`, `:284-288`

Dropped entries become `0.0` **before** softmax (step 3 → step 4), so each dropped logit retains mass `exp(-max)/Z`. Pinned vector `[2.0, 1.5, 0.0, −1.0, 3.0]`, k=2 → dropped tokens carry ≈3.3% each (~9.9% combined) instead of 0; kept index 1 receives *less* mass than a dropped zero. All-negative scaled logits (reachable via temperature/penalty) are worse — kept tokens can lose to zeros outright.

Note: the proba rows currently pin the zeroed arithmetic as the f64 oracle — the pins must move with the fix (aligning tests to the documented contract, not weakening them).

**Fix:** drop masked positions from the softmax input entirely (build kept-value list, softmax over it, scatter back into a zero vector), or use a large-negative finite sentinel consistent with the finite gate.

### B5 · `_has_no_separator` returns true when a separator IS present

`src/serialize.fab:434-439`

```fab
fn _has_no_separator(string s) → bool {
    for range 0‥s.length() const i {
        if s.get(i) ≡ "/" then return true
    }
    return false
}
```

Body is `contains_separator` — inverted relative to the name. This guards the U5 reserved-character wire rule; both call sites (`serialize.fab:527`, `:713`) wrap it in `require not (...)`, so wire safety holds today, but any future caller trusting the name silently admits `/` into the parameter wire. Honest-name twin exists at `parameter.fab:505-510` (`_contains_separator`, same body).

**Fix:** rename to `_contains_separator`; leave call sites' `require not (...)` unchanged.

### B6 · `_sqrt` fixed 12 Newton iterations lose accuracy above ~10⁶ inputs

`src/math.fab:354-361` (analytic verification; not runtime-executed)

Babylonian iteration from seed `x/2` halves ratio `r` while `r ≫ 1`; quadratic convergence starts only near `r ≈ 1`. Steps needed ≈ `½·log₂(x) + 2`: x=10⁶ needs ~12 (exact budget), x=10⁸ needs ~14 → result overshoots ~20% after 12 iterations, degrading worse beyond. Inputs are activation variances (`var + ε` in layernorm :556, `mean_sq + ε` in rmsnorm :606); reachable under normal operation, silently skewing norm outputs. Probas pass because they use modest ranges.

**Fix:** prescale into the quadratic regime (halve by 4 until ≤ 1, iterate, rescale by doubling) or raise iterations to ~40 — cost is trivial per row.

### B7 · source gate red at HEAD + checker line-number defect

- `./scripta/check-source` exits 1: Latin conversion targets `c ↦ textus` at `src/optimize.fab:278` and `src/train.fab:721` (intended `↦ string`). These are the only two gate failures.
- Tooling bug: the checker misreports positions (`optimize.fab:63`, `train.fab:270`) — appears to count comment-stripped lines rather than file lines.

---

## Gate violations (U8 no-Latin, export markers)

Latin identifiers that escape the checker lexicon (stems missing: `ignotum`, `invalida`, `alia`). Close together with the lexicon additions or they reintroduce:

| Site | Token | Preferred |
| --- | --- | --- |
| `src/gradient.fab:78` (+ match arm :89, throws :143-145, :177, :246-248, :263, :299-301, :310) | `GradusIgnotum` | `UnknownGradient` / `UnknownIdentity` |
| `src/transformer.fab:189` (arm :230, mapping :267) | `EpsilonInvalida` | `InvalidEpsilon` (matches `nn.fab:234`) |
| `tests/admission_conformance.fab:78` (+ uses :730, :1192+) | `F_ALIA` | e.g. `F_ALT_DIGEST` |

Missing `@ public { }` on de-facto cross-module surface (default visibility doing the export):

| Site | Surface | External caller evidence |
| --- | --- | --- |
| `src/loss.fab:321, :331, :341` | `mse_2x2`, `mse_4x4`, `mse_2x8` | README-admitted caller surface; ledger refs in `tensor.fab:69-70` |
| `src/nn.fab:102, :113, :121, :143, :164, :183` | fixed-shape bridges | `exempla/nn-bridge/src/main.fab:118` calls `nn.linear_2x2` |
| `src/nn.fab:443` | `linear_carrier` | called from `mlp.fab:136`, `transformer.fab:277`, `decode.fab:440` |
| `src/math.fab:339` | `add_carrier` | called from `nn.fab:476`, `transformer.fab:310` |
| `src/gradient.fab:245, :298` | `gradients_simple_loss`, `gradients_masked_mean` | documented as the one public contract entry |
| `src/transformer.fab:65` | `bert_tiny_block_2x8` | live caller cited in header (`examples/training/bert-gradus-probe`) |
| `src/parameter.fab:87` | `union Station` | exposed via public field/accessor; sibling unions all annotated |

---

## Style debt (grouped themes, worst offenders cited)

- **Additive negation `(0 - x)` over unary minus** — attention.fab:363/:376/:392/:997, cache.fab:1197/:1209/:1511, speculative.fab:137/:155/:163, receipt.fab:21/:245/:283/:330, generation.fab:717, sampling.fab:281, gguf_manifest.fab:580. Same files already write `-1` directly (tokenizer.fab:379/:925/:1092), so it is residue, not constraint.
- **If-equality ladders over closed unions instead of switch/case** — tokenizer.fab:468-482, cache.fab:738-742/:800-803/:930-933/:964-967/:998-1001, dense.fab:311-315, generation.fab:240-242, gguf.fab:329-366 (37 arms), gguf_manifest.fab:634-661, dequant.fab:578-601.
- **`+` concat where `"§"(…)` interpolation slots exist** (WARN018 class) — cache.fab:556-562/:1546-1564/:1725-1748 (eleven repeated appends), dense.fab:140-148, tokenizer.fab:1319-1324, generation.fab:494, receipt.fab:266.
- **Open `while` counters where `for range 0‥n const i` applies** — loss.fab:287-313, nn.fab:536-567/:596-616, metrics.fab:138-158, math.fab:477-487/:512-523/:548-560, shape.fab:262-273/:295-299, attention.fab:409-414, dense.fab:186-192 + layer loops :399/:519/:611.
- **Positional scalar fan-out (>5 params)** — decode.fab:299 `construct_weights` (18 tensors), train.fab:97 `train_step_bert_linear` (25), transformer.fab:364 `transformer_block` (23), transformer.fab:65 `bert_tiny_block_2x8` (20), receipt.fab:274/:293/:301 (same 12 scalars ×3), calibration.fab:372 `bake` (8, five provenance strings belong in the record built at :377 anyway), gguf.fab:379 `admit` (10).
- **Type restated both sides of a binding** — `const f32 E ← 2.718… ∷ f32` pattern (loss.fab:187, train.fab:300/:537, nn.fab:278-283); tuple return types restated at construction (train.fab:70/:84/:100/:115); proba pins train.proba:841-842.
- **Field-by-field rebuilds instead of typed re-bind/copy-with-update** — parameter.fab:389 (`Identity` ×5 fields), optimize.fab:512 (`SgdState`).
- **Mixed comparator scripts** — tests/admission_conformance.fab uses ASCII `<` in seven while loops (:109, :128, :237, :300, :472, :487) where all of src uses `≺`.
- **Private-marker naming on public/private helpers** — optimize.fab:118 `_sgd_family` is underscore-prefixed yet `@ public { }` and called cross-module (train.fab:98-99, :114).

---

## Observations (not defects today; ranked)

1. **capsule.verify defense-in-depth much thinner than admission** — GGUF arm checks identity-field agreement only (zero tensor-table validation); neither arm re-checks duplicate names/overlap/exact tiling (`capsule.fab:494-515`). Intended flow is safe (GGUF capsules come only from `gguf_manifest.parse` via `gguf.admit`), but verify is marketed as the owner-boundary check and passes hand-built structurally-invalid manifests. Document the narrower contract or extend `_manifest_ok`.
2. **Nested-array metadata retention bypasses the 64 MiB cap** — `gguf_manifest.fab:458-472` accumulates byte-by-byte from many small reads with no cumulative guard; README's per-read claim holds, the retained aggregate does not.
3. **Error routing by English message string** — dense.fab:312-313 (`if c ≡ "cache overflow"`); attention.fab:981-988 collapses every CacheError into ShapeMismatch.
4. **Repetition penalty excludes prompt tokens** — generation.fab:865 seeds empty history (generated-only) while decode.replay seeds explicitly (decode.fab:666-668); undocumented divergence between entry points.
5. **dense._attn_bias swallows resolver errors as absent-bias** — dense.fab:257-271 catches everything to `hit ← false`; an invalid bias degrades to absent-bias path against the fail-closed posture. Discriminate `MissingTensor` from malformed (pattern exists at tokenizer.fab:792-800).
6. **Tokenizer sparse-table gap ids decode silently** — tokenizer.fab:941-943 + :1006-1017 fill unseen ids with "" and contribute nothing instead of failing UnknownId (unreachable via dense manifest build, reachable via hand-built tables).
7. **Dropout rate = 1.0 edge correct-but-fragile** — train.fab:593 computes Inf scale eagerly; correctness rests on draws being strictly < 1; untested boundary.
8. **optimize.step validates gradient shape but not dtype tag** — optimize.fab:496.
9. **Dead tie-break arm** — tokenizer.fab:838 condition unreachable (i monotone); leftmost-tie actually comes from strict `<`; comment contradicts behavior.
10. **Dead trailing `throw … "unreachable"` tails** after exhaustive do/catch across modules (gguf.fab:269/:282/:295/:500, serialize.fab:334, math.fab:621/:634/:647, parameter.fab:355/:394, capsule.fab:610, safetensors.fab:879, tensor_view.fab:235, dequant.fab:623) — presumably required fall-through proof; a compiler fix would delete nine lies.
11. **Doc drift** — facade `gradus.fab:49` lists retired `train_step_bert` (split into linear+layernorm variants at train.fab:32-36); gguf.fab:131 `TENSOR_LIMIT ← 65536` comment cites ceilings that are actually 4,096 (gguf_manifest.fab:111); dequant.fab:290 cites nonexistent `_f32le_quattuor`; artifact.fab:6/gguf.fab:7 import-line comments contain stray `private` token; Latin residue in comments (train.fab:33 `iuncta`, mlp.fab:192, transformer.fab:245 `laminatio`, dtype.fab:39 `fractus.rotunda`, shape.fab:19 `genus/magnitudo`, parameter.fab:44/:398 `Registrum`).
12. **Discarded `path` parameter** on `safetensors.admit(corpus, digest, path)` — always dead (proba proves non-retention); invites future misuse.

---

## What was verified sound

- KV-cache capacity/gap law: exactly-at-capacity admitted, capacity+1 rejected, pre-checked before mutation (`_admit_write` cache.fab:346-352)
- Cached-attention absolute positions including just-written row (`_softmax_prefix` end = prefix_before+i+1; enforced by `_validate_absolute_positions`)
- SDPA scale-before-softmax, causal mask direction, GQA head split math
- Speculative decode accept-iff-equal greedy oracle
- Byte-level BPE round-trip bijective incl. the 0xAD corner; vocab-id bounds checked
- Dequant kernels faithful to llama.cpp ggml-quants.c semantics kernel-by-kernel (Q8_0, Q5_0 high-bit packing, K-quants incl. get_scale_min_k4 j≥4 packed halves, Q6_K ql/qh interleave and scale indexing); block geometry table matches; explicit LE everywhere; u64 ≥ 2⁶³ rejected at carrier
- GGUF caps (4,096 entries metadata and tensor dirs) enforced at both entry points; bounds arithmetic consistently overflow-safe (checked add/mul, division-form guards)
- No-retention claim survives field-by-field audit of every carrier type in the admission stack
- SGD formula single-sourced (`_sgd_family`); schedule warmup/cosine endpoints correct; checkpoint round-trip exact incl. lr; serialize float tokens shortest-round-trip
- Proba discipline strong: negative matrices everywhere (schedule validation, staleness/frozen/identity, wire fail-closed matrices, dtype cast boundaries, shape sentinels, f64-oracle activation/norm pins)

## Test coverage gaps found

1. No test re-reads the input cache after a successful `append`/`extend` (would catch B3's success-path half)
2. No partially-invalid `extend` token list (catches B3's rejection half)
3. Sampling has no negative-kept-logit top-k row beyond the single pinned vector — which locks in B4's wrong semantics
4. Dequant value-exactness rests entirely on the disclosed golden path — a bitmap/scale regression passes the executable tier (element counts only)
5. No test feeds a hand-built `GgufManifest` through `construct_manifest`/`verify` (O1)
6. No test approaches the nested-array retention cap (O2)
7. Fixed-shape bridges never exercised by their home probas (consistent with their unannotated fail-open state, B1)
8. Dropout rate 1.0 untested (O7)

---

## Suggested fix order

1. Restore the standing gate: B7 (`↦ string` fixes + checker line-number bug) and the G-list renames with lexicon stems
2. Correctness: B3 (fresh-list copies) and B4 (true removal + move its oracle pins with it)
3. B2 decision: match the reference format and regenerate fixture+hash, or document the private variant honestly
4. B1 bridges → typed errors; B5 rename; B6 sqrt seed
5. Style sweep and doc-drift cleanup last (mechanical)

---

*Pattern-library accretion candidates recorded during this review: inverted-predicate naming (B5 class) and shared-reference aliasing breaking value-copy assumptions under the FMIR runner (B3 class).*
