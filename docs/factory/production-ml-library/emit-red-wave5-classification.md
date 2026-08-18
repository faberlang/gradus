# Emit-surface rustc red classification — wave 5 (N4 + N5)

**Status**: planned — planner input, not a fix. No emit or library source
changed in this unit.
**Unit**: handle `ee87e245` / `682aa409` (hand-12). Classification only.
**Do not treat this file as evidence that a repair exists.** Live truth is
the two generated crates and the rustc streams cited below.

Wave-4 playbook: [`emit-red-wave4-classification.md`](emit-red-wave4-classification.md)
(gradus `65fa3af`, N1–N3 + F1/F7/F13/F14/K5). This is the fifth iteration
after ER-15..ER-19 landed on radix `b42c95c62`. New rustc identities are
N4–N5. Wave-4's 65-red union is family-zero on this stream.

## 1. Receipts

Both crates share one rust HIR emit (`radix-hir-rust` at readable radix
`b42c95c62`) and one inlined library surface. rustc 1.97.1 Homebrew.
Gate mail `02d0b298` (test-1 ER-MERGE-01 STOP after wave-4 landings).

| Row | Crate | rustc | warnings | Artifact |
| --- | --- | ---: | ---: | --- |
| U1.9 SmolLM2 | `dense-prefill-smollm2` | 104 | 447 | `worktrees/test-1/gradus/exempla/dense-prefill-smollm2/target/faber` |
| U1.10 Qwen2.5-0.5B | `dense-prefill-qwen2` | 113 | 447 | `worktrees/test-1/gradus/exempla/dense-prefill-qwen2/target/faber` |

Logs: `/tmp/test-1-smollm2-build.log`, `/tmp/test-1-qwen2-build.log`.

Wave-4 classified 65 — family-zero 0/0 on both crates (N1, N2, N3, F1,
F7, F13, F14, K5). ER-15..ER-19 landings are visible: the classified
identities do not reproduce. Every remaining rustc row is E0308.

## 2. How to read the counts

rustc columns are the official error counts. Sites are unique `file:line`
emit constructs. Union = one emit defect per family, not two.

Class:

- **(a)** mechanical parenthesization / turbofish / clone / Result unwrap
- **(b)** const-eval legality — none remain
- **(c)** type-level or name-mapping gap that needs a design pick (or a
  settled pick that was not applied to this spelling)

Repair owner is **radix rust HIR emit**. Gradus Faber source is not the
defect for either family.

## 3. Union family table

| ID | Class | Family | Smol rustc | Qwen rustc | Sites | Emit construct |
| --- | --- | --- | ---: | ---: | --- | --- |
| **N4** | (c) | fac / do-catch typed `String` vs module error (ER-19 F14 leak) | 103 | 112 | every `do`/`catch` around an imported `⇥ ModuleError` call | F14 annotated `fac_result` from `function_err_ty` and defaulted a miss to `String`; imported callees carry their `⇥` on `function_effects.err_ty` instead |
| **N5** | (a) | `gelu()` Result assigned as `Tensor` (Result-ladder miss) | 1 | 1 | transformer staged FFN proof row | `generate_tensor_method` has no `TensorGelu` arm; runtime `gelu` is `Result<Tensor<f32>, &'static str>` |

Checksum: Smol 103+1 = **104**. Qwen 112+1 = **113**. Two families.

N4 rustc splits (three spellings of one annotation):

| Spelling | Smol | Qwen | rustc shape |
| --- | ---: | ---: | --- |
| (a) `break 'fac_result Err(fac_err)` | 54 | 60 | expected `String`, found `ModuleError` |
| (b) `crate::…::message(err.clone())` | 45 | 44 | expected `ModuleError`, found `String` |
| (c) `match err` vs typed variant arms | 4 | 8 | expected `String`, found `ModuleError` |

Plus four Error↔Error rows (2 Smol + 2 Qwen: `MathError`↔`TensorError`,
and Smol `MathError`↔`DTypeError`). Same seam, lookup-missed-entirely
mode — see §4.

## 4. Family detail

### N4 — (c) fac / do-catch String vs module error — **one emission seam**

**Not 215 independent sites.** 103+112 rustc rows are one annotation
decision replayed at every imported `do`/`catch`.

**Representative (consumer, first Smol site)**

Faber (`exempla/dense-prefill-smollm2/src/main.fab:153`):

```text
fn _limits(… m, string gguf_name) → tuple<int, int> ⇥ PrefillError {
    do { return manifestum.limes_payloadis(m, gguf_name) }
    catch err {
        throw variant ManifestumMala {
            message = "payload range failed for " + gguf_name + ": "
                    + manifestum.message(err)
        }
    }
}
```

Emit (smol `:261` / `:267` / `:285`; Qwen twin `:293`):

```text
let ok: Result<(i64, i64), String> = 'fac_result: {
    match crate::model::gguf_manifest::limes_payloadis(…) {
        Ok(fac_value) => fac_value,
        Err(fac_err) => break 'fac_result Err(fac_err),  // fac_err: GgufManifestError
    }
};
Err(err) => {  // err: String
    crate::model::gguf_manifest::message(err.clone())  // wants GgufManifestError
}
```

(a) expected `String`, found `GgufManifestError`. (b) the inverse on
`message`. The cape is already the `PrefillError` map. The leak is the
**inner** `fac_result` annotation.

**Library twin (spelling c)** — `tensor_view::_description` smol `:7282`:

```text
let ok: Result<GgufTensorDescriptor, String> = 'fac_result: { … };
Err(err) => match err {   // err: String
    GgufManifestError::WireMala { … } => …   // arms want GgufManifestError
}
```

**Error↔Error twin (same seam, lookup-missed-entirely)** — `math::construct`
smol `:3176`:

```text
let ok: Result<Tensor, MathError> = 'fac_result: {
    match crate::tensor::construct(…) {  // TensorError
        Err(fac_err) => break 'fac_result Err(fac_err),
    }
};
crate::tensor::message(err.clone())  // wants TensorError, err is MathError
```

Callee lookup returned `None`, so the annotation kept the catch type
(`MathError`). The call emit still wrapped the imported failable. One
construct, two rustc rows (`MathError`↔`TensorError`). Smol
`_dtype_from_name` / `cast` is the `MathError`↔`DTypeError` twin.

**Modules hit** (from the `break`/`message` pairs, not a second family):
`GgufManifestError`, `ViewError`, `TensorError`, `MathError`, `NnError`,
`AttentionError`, `ShapeError`, `DequantError`, `TokenizerError`,
`DenseError`, `DenseQwen2Error` (Qwen), `DTypeError`, `TransformerError`.

Emitted `fac_result` annotations on the Smol crate: 57 `String` vs a
handful of catch-local `NnError` / `PrefillError` / `MathError` /
`TokenizerError`. The String pile is the leak.

**Emit.** ER-19 F14 (`69870ce5b`, `expr/mod.rs`
`generate_handled_expr_with_emitter`) changed the inner annotation from
the enclosing `⇥` to "the callee error":

```text
handled_err_ty = match (callee_err_ty, catch_err_ty) {
    (Some(callee), Some(catch_ty)) if !equals(callee, catch_ty) => Some(callee),
    (Some(callee), _) => Some(callee),
    (_, Some(catch_ty)) => Some(catch_ty),
    _ => current_err_ty(),
};
```

`handled_body_callee_err_ty` walks the body for the first failable.
`failable_path_err_ty` / `failable_method_err_ty` then do:

```text
is_failable_def(def_id).then(|| {
    function_err_ty(def_id).unwrap_or_else(|| types.primitive(Textus))
})
```

`function_err_ty` is `collect_function_err_types` over the **current**
`HirModule` only (`module.rs:1655`). Imported / sibling library
functions store their declared `⇥` on
`ImportedNamespaceFunctionEffects.err_ty` (`import_params.rs:61`),
populated when the sibling is collected.

The **call** emit already reads that map
(`expr/call/mod.rs:377`):

```text
imported_effects.and_then(|effects| effects.err_ty)
    .or_else(|| item_def.and_then(|def_id| function_err_ty(def_id)))
```

F14's annotation walk does not. Two failure modes, one function:

| Mode | Lookup | Annotation | rustc |
| --- | --- | --- | --- |
| A (dominant) | recognized failable, `function_err_ty` missing → `String` | `String` overrides catch | String ↔ ModuleError (a)(b)(c) |
| B (4 rows) | not recognized at all → `None` | catch type kept | MathError ↔ TensorError / DTypeError |

**Why F14 missed it.** F14 typed the **annotation policy**, not the
**value-flow lookup**.

1. The F14 oracle is `ad 'solum:exstat'` inside a `⇥ PrefillError`
   function (`failable_test.rs` `rust_fac_inner_error_typed_as_callee_error`).
   That callee has **no declared `⇥`**. Defaulting to `String` is correct
   there, and the test **asserts** `Result<(), String>`.
2. Wave-4 wrote the fix shape as “type the inner fac as the callee's
   error (`String`)”. The parenthetical was the F14 site's payload, not
   a global error type. The Hand implemented the parenthetical.
3. `unwrap_or(textus)` treats “imported `⇥` not in this module's map”
   as “undeclared ad-channel”. Those are different facts.
4. Prefer-callee-over-catch is the right pick **when the callee type is
   real**. On mode A it overwrites `catch.binding_ty` (`GgufManifestError`,
   which `message(err)` already expects) with the fake `String`.

F14 cleared the two Smol `_load_golden` `solum.exists` / `read_lines`
sites (wave-4 F14, 2+0). It did not lock an imported `⇥ ModuleError`
callee. The cape still maps. The inner `break` / `err` binding do not.

**Settled pick.** Keep F14's policy: type `fac_result` as the **actual**
callee `⇥`; the cape maps. Recover that `⇥` from the same source the
call emit already uses (`function_effects.err_ty`, then
`function_err_ty`). Do not default a known-failable import to `String`
when `effects.err_ty` is a nominal module error. Do not revert F14's
ad-failable String case (the original oracle stays green).

**Rejected**

| Shape | Why not |
| --- | --- |
| Annotate every fac as `String` and stringify | Breaks `message(err)` / `match err` on typed enums. That is the current red. |
| Annotate as the enclosing / catch type and `map_err` at every `break` | Works, but is a second policy. F14 already chose callee-type + cape-map. Finish that lookup. |
| Gradus-side `do`/`catch` rewrites | 215 Faber sites are not the defect. One emit seam is. |
| First-failable-wins rewrite of mixed bodies | This stream has no mixed-body identity. Each red `fac` wraps one imported call. Residual only. |

**Fix shape.** In `failable_path_err_ty` / `failable_method_err_ty`,
read `imported_namespace_function_effects.err_ty` the way
`try_generate_imported_namespace_call` already does. First failing
oracle: `_limits` emits
`let ok: Result<(i64, i64), GgufManifestError> = 'fac_result:`
and smol `:267` / `:285` typecheck. Extend F14's test with an imported
(or sibling) `⇥ ModuleError` callee whose cape calls `message(err)`.

### N5 — (a) `h1b.gelu()` Result not unwrapped

**Representative**

Faber (`gradus/src/transformer.fab:91`):

```text
const tensor<f32, [2, 8]> a1 ← h1b.gelu()
```

Emit (smol `:12610`, Qwen `:12785`):

```text
let a1: faber::Tensor<f32> = h1b.gelu();
```

rustc E0308: expected `Tensor<f32>`, found `Result<Tensor<f32>, &str>`.
Help: `.expect(...)`.

**Emit.** Runtime (`faber/runtime/rust/src/tensor.rs:645`) is

```text
pub fn gelu(&self) -> Result<Tensor<f32>, &'static str>
```

`generate_tensor_method` (`expr/call/intrinsics.rs`) already routes
`TensorSoftmax` / `TensorLayerNorm` / `TensorTranspose` / `TensorMatMul`
/ `TensorAdd` through `begin_handled_conversio_match` +
`emit_result_exact_err_outcome` (the ER-8 / ER-16 ladder). `TensorGelu`
is registered (`radix-module` `intrinsics/registry.rs:523`) but has
**no match arm**. It falls through `_ => return Ok(false)` (`:2300`).
The generic method path then prints `.gelu()` with no unwrap.

Neighboring staged calls on the same row already use the ladder
(`h1b` is `addita`+expect; `softmax` / `layernorm` / `matmul` same).

**Not** `nn.gelu` (Faber wrapper, `⇥ NnError`, implemented in
`nn.fab:533`). The red site is the staged tensor method on the
bert-tiny proof row.

**Fix shape.** Same pick as ER-8 / ER-16: add a `TensorGelu` arm that
emits `.gelu()` plus the existing Result `expect` / `?` ladder. Do not
change the runtime signature. Do not add a Latin alias.

**One site shape.** One emit construct, one rustc row per crate. Not a
global gelu family.

## 5. Shared vs consumer-only

| Surface | Families |
| --- | --- |
| Shared library (gguf_manifest, tensor_view, tensor, math, nn, attention, …) | N4 (library `do`/`catch` around sibling imports), N5 (transformer staged row) |
| SmolLM2 / Qwen2 consumer | N4 (`_limits` / `_bind` / `_slice` / `_tensor` and the rest of the imported maps) |

N4 is global. N5 is the one staged proof row, inlined into both crates.

## 6. Proposed unit split

One behavior family per unit. Repair is `radix-hir-rust`. First failing
oracle is a rustc identity on a re-emitted crate. Do not retune
numerics. Do not weaken TARGETLANE001. Do not edit Gradus Faber to
paper over either family.

Recommended order: ER-20 (unblocks almost the whole stream) → ER-21
(one-line ladder, unblocks the transformer proof row).

| Unit | Class | Outcome | Write scope | First failing oracle | Closes rustc (union) | Depends |
| --- | --- | --- | --- | --- | --- | --- |
| **ER-20** | (c) | `fac_result` annotated with the imported callee's declared `⇥` (`function_effects.err_ty`), not `String`. Cape still maps. F14 ad-failable String oracle stays. | `expr/mod.rs` `failable_path_err_ty` / `failable_method_err_ty` / `handled_body_callee_err_ty`; extend `failable_test.rs` | `_limits` emits `Result<(i64, i64), GgufManifestError>`; smol `:267` break and `:285` `message(err)` typecheck | N4: 103+112 | F14 policy stays (callee type + cape map). Lookup must see imports. |
| **ER-21** | (a) | `TensorGelu` uses the softmax/layernorm Result ladder | `expr/call/intrinsics.rs` `generate_tensor_method` | `h1b.gelu()` becomes `.gelu().expect("…")` (or handled `?`); E0308 gone | N5: 1+1 | ER-8/ER-16 ladder. Not a new design fork. |

Two Hands, or one Hand with two commits. Do not fold N5 into ER-20:
different file, different construct, different oracle. ER-20 must not
be closed by pointing at F14's `solum.exists` String test.

## 7. Out of scope / residuals

- No rustc warning classification (447 / 447).
- llvm-host / TARGETLANE001 / `fmir` package target / numerics untouched.
- Generated crates stay uncommitted build output.
- This file does not claim any family is fixed.
- First-failable-wins on a mixed-error `fac` body is a residual risk,
  not a rustc identity on this stream.
- `nn.gelu` / other Faber wrappers are not N5.

## 8. Re-parse commands

```text
# Preserved crates (test-1 ER-MERGE-01)
cargo check --manifest-path \
  worktrees/test-1/gradus/exempla/dense-prefill-smollm2/target/faber/Cargo.toml
cargo check --manifest-path \
  worktrees/test-1/gradus/exempla/dense-prefill-qwen2/target/faber/Cargo.toml

# Re-emit after a radix repair
env FABER_SUPPORT_PATH_OVERRIDE=/Users/ianzepp/work/faberlang \
  FABER_LIBRARY_HOME=/Users/ianzepp/work/faberlang/worktrees/test-1 \
  <packet-faber> build --target rust exempla/dense-prefill-smollm2
```
