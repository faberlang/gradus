# Emit-surface rustc red classification — wave 4 (65-red union)

**Status**: planned — planner input, not a fix. No emit or library source
changed in this unit.
**Unit**: handle `37e0983e` / `b943dd02` (hand-12). Classification only.
**Do not treat this file as evidence that a repair exists.** Live truth is
the two generated crates and the rustc streams cited below.

Wave-1 playbook: [`emit-red-classification.md`](emit-red-classification.md)
(gradus `4d194a3`, F1–F14). This is the fourth iteration of that playbook
after ER-1..ER-14 landed on radix `74fc2b0bd`. New rustc identities are
N1–N3. Residuals keep their wave-1 IDs (F1, F7, F13, F14, F12-like).

## 1. Receipts

Both crates share one rust HIR emit (`radix-hir-rust` at readable radix
`74fc2b0bd`) and one inlined library surface. rustc 1.97.1 Homebrew.
Gate mail `7da5ae23` (test-1 five-green, then ER-MERGE-01 STOP).

| Row | Crate | rustc | warnings | Artifact |
| --- | --- | ---: | ---: | --- |
| U1.9 SmolLM2 | `dense-prefill-smollm2` | 35 | 449 | `worktrees/test-1/gradus/exempla/dense-prefill-smollm2/target/faber` |
| U1.10 Qwen2.5-0.5B | `dense-prefill-qwen2` | 30 | 461 | `worktrees/test-1/gradus/exempla/dense-prefill-qwen2/target/faber` |

Logs: `/tmp/test-1-smollm2-build.log`, `/tmp/test-1-qwen2-build.log`.

Cleared vs the original 258/248 (ER-2/3/5/8/9/10 visible in the stream):
E0015 / E0493 const `vec!` / `format!` / String dtor = 0; E0599
`transpone` / `activatio_softmax` / `laminatio` = 0; E0599 `String.accipe`
= 0; E0605 `Vec<i64> as Vec<u8>` / F8 integer→byte = 0.

## 2. How to read the counts

rustc columns are the official error counts. Sites are unique `file:line`
emit constructs. Union = one emit defect per family, not two.

Class:

- **(a)** mechanical parenthesization / turbofish / clone
- **(b)** const-eval legality — none remain
- **(c)** type-level or name-mapping gap that needs a design pick (or a
  settled pick that was not applied to this spelling)

Repair owner is **radix rust HIR emit** unless a row says otherwise.

## 3. Union family table

| ID | Class | Family | Smol rustc | Qwen rustc | Sites | Emit construct |
| --- | --- | --- | ---: | ---: | --- | --- |
| **N1** | (a) | `.collect()` after const-slice `.to_vec()` / `.to_string()` | 7 | 7 | tokenizer unicode tables + `EOG_NOMINA` | ER-2 use-site adapt: `write_const_list_owned_suffix_for_type` writes `.collect()` with no turbofish; `.clone()` follows |
| **N2** | (c) | `addita_bias` on `faber::Tensor<T>` | 4 | 4 | transformer proof row (q/k/v + h1 reported; aob/h2b same construct, 6 emit sites/crate) | ER-8 mapped `transpone`/`activatio_softmax`/`laminatio` only; `added_bias` → Latin `addita_bias` is not in the map. Runtime has `addita` |
| **N3** | (c) | `impl Fn` `fons` moved in a loop | 13 | 13 | `dense::forward` layer loop + tail; GGUF `_read_source` / `_source_value`; dequant `_read_source` | ER-4 `impl Fn` is not `Copy` (unlike `fn` pointers). `_source(fons, …)` / `_read_source(fons, …)` moves the closure |
| F1 | (a) | `as` then `.to_string()` | 3 | 1 | 3 Smol consumer + 1 Qwen consumer | ER-1 leak: `numerus ↦ textus` appends `.to_string()` after a widening `as i64` without wrapping |
| F7 | (c) | `Option<GgufMetadata>` not narrowed | 4 | 4 | GGUF `metadata` return + two `alignment_meta` blocks | ER-6 leak: Faber `T ∪ null` + `coalesce` after `not is null`; emit writes `is_some()` and **elides coalesce**, leaving the Option binding |
| F13 | (c) | `fons(nomen)` one-arg | 1 | 1 | `dense::_source` | **Not** the Type::Func path ER-12 locked. Receiver is the **`impl Fn` parameter Path** (ER-4 spelling) |
| F14 | (c) | `String` → `PrefillError` | 2 | 0 | Smol `_load_golden` exists + read_lines | ER-13 landed the Faber `do/catch`. Leaked path is the **inner** `break 'fac_result Err(fac_err)` typed as `PrefillError` while `fac_err: String` |
| K5 | (a) | moved `encoded` reused | 1 | 0 | Smol tokenizer PASS arm | `tokens = encoded` then `_ids_text(encoded.clone())`. F12-like; ER-11 covered `String` lista-append, not this `Vec` move |

Checksum: Smol 7+4+13+3+4+1+2+1 = **35**. Qwen 7+4+13+1+4+1 = **30**.
Union rustc = **65**. Eight families.

## 4. Family detail

### N1 — (a) `collect` after const-slice owned adapt

**Representative**

```text
smol :11663  TABULA_LITTERAE.iter().map(|r| r.to_vec()).collect().clone()
smol :11818  same in _letter_code
smol :12330  EOG_NOMINA.iter().map(|s| s.to_string()).collect().clone()
qwen :11896  TABULA_LITTERAE same shape
```

rustc E0282: type annotations needed on `.collect()`. Help: specify the
generic argument.

**Emit.** ER-2 made const lists `&'static [T]` / `&'static [&str]`. Owned
`lista` uses adapt in `radix-hir-rust` `expr/mod.rs`
`write_const_list_owned_suffix_for_type`:

- nested list → `.iter().map(|r| r.to_vec()).collect()`
- `list<string>` → `.iter().map(|s| s.to_string()).collect()`
- scalar list → `.to_vec()` (inferred)

`.collect()` has no turbofish. A following `.clone()` (owned-use clone
policy) removes the only inference slot.

**Fix shape.** Write `collect::<Vec<_>>()` (or `Vec<Vec<i64>>` /
`Vec<String>`). Mechanical. Do not change the const-slice policy.

### N2 — (c) `addita_bias` not mapped onto `addita`

**Representative**

```text
Faber  gradus/src/transformer.fab
  qb ← q.added_bias(bq)     # locale English for addita_bias

smol :12543  q.addita_bias(&bq)
smol :12545  k.addita_bias(&bk)
smol :12547  v.addita_bias(&bv)
smol :12554  ao.addita_bias(&bo)     # same construct; not in the 4 rustc rows
smol :12558  h1.addita_bias(&bf1)
smol :12561  h2.addita_bias(&bf2)
```

rustc E0599. Help: method `addita` with a similar name. Nearby
`x.addita(&(aob))` is already wrapped in `{ let t = &x; t.addita(...) }.expect(...)`.
`addita_bias` is emitted as a non-Result method.

**Emit.** ER-8 (`a5d603dd9`) maps `transpone` → `transpose_rank2`,
`activatio_softmax` → `softmax`, `laminatio` → `layernorm` in
`expr/call/intrinsics.rs` + `intrinsics/registry.rs`. `addita_bias` is
absent from `radix-hir-rust` (grep is empty). Runtime
`faber/runtime/rust/src/tensor.rs` has `addita` (NumPy-style broadcast,
`Result`) and no `addita_bias`. Rank-extension `[2,8]+[8]` is valid
broadcast for `addita`.

**Fix shape.** Same pick as ER-8: map Latin `addita_bias` → runtime
`addita` and use the existing Result `expect`/`?` ladder. Do not add a
Latin alias on the runtime.

**Settled pick.** ER-8 already chose map-not-alias. This unit applies
that pick to the missed stem. Not a new design fork.

### N3 — (c) `impl Fn` moved in a loop — **reborrow**

**Representative**

```text
ER-4 spelling (both crates):
  fons: impl Fn(String, i64) -> Lookup
  fons: impl Fn(i64, i64) -> SourceRead

smol dense::forward
  :4502  _source(fons, "model.embed_tokens", 0)?     # first use: moves
  :4518–4537  _source(fons, …) inside while stratum < cfg.layers
  :4622  _source(fons, "model.norm", 0)?
  :4631  _source(fons, "lm_head", 0)?

smol GGUF / dequant
  :5957 / :6008  _read_source(fons, …) / _source_value(fons, …)
  :7484  _read_source(fons, …) in the block loop
```

rustc E0382. Help: **consider borrowing `fons`**. `impl Fn` is not
`Copy`. `fn(...)` pointers were. ER-4's switch created this family.

**Emit.** `types.rs` `parameter_type_to_rust` / `FuncTypePosition::Parameter`
prints `impl Fn({}) -> {}`. Call sites pass the binding by value:
`_source(fons, …)`, `_read_source(fons, …)`. First use moves; every later
use in the same function is E0382. Faber treats function values as
reusable.

**Fix shape: reborrow.** Emit `&fons` at every pass-through of a function
value. `&F: Fn` whenever `F: Fn`, so existing `impl Fn(...)` parameters
accept the reborrow with no signature change.

```text
_source(&fons, prefix, stratum)     // was _source(fons, …)
_read_source(&fons, total, off, n)  // was _read_source(fons, …)
```

Alternate (same family, larger): spell parameters `&impl Fn(...)` and
insert `&` at every function-value argument. Prefer call-site `&` only.

**Rejected**

| Shape | Why not |
| --- | --- |
| **clone** | Needs `impl Fn(...) + Clone`. Closures are `Clone` only if every capture is. rustc help is borrow, not clone. Heavier bound for no semantic gain. |
| **FnMut** | Lookups do not mutate. `FnMut` is also not `Copy`. Does not fix by-value moves. |
| Revert ER-4 to `fn` pointers | Re-breaks capturing closures (`materialize_slice` / `inspect` / `dense::forward`). |

Do not revert ER-4. This is an ER-4 follow-on.

### F1 — (a) residual: widening `as` then `.to_string()`

**Representative**

```text
Faber: (lines.length() ↦ string)   /  (admitted.tensors.length() ↦ string)
smol :815   lines.len() as i64.to_string()
smol :1036  admitted.tensors.clone().len() as i64.to_string()
smol :1251  tokens.len() as i64.to_string()
qwen :993   m.tensors.clone().len() as i64.to_string()
```

**Emit.** ER-1 wraps Conversio / widening when they are a postfix
**receiver**. The leaked path is `expr/convert.rs` numerus→textus:

```text
emitter.expr(source)?;          // writes  lines.len() as i64
emitter.writer.write(".to_string()");
```

`length()` already ends in ` as i64`. The suffix is not parenthesized.

**Fix shape.** Same as ER-1: `(<expr> as i64).to_string()`. Mechanical
leak, not a new family.

`_reduce_angle` `/` is gone from this stream (ER-1 held for that site).

### F7 — (c) residual: `T ∪ null` + `coalesce`, not `is_some()` Path return

**Representative**

```text
Faber gguf_manifest.fab
  metadata:
    if found not is null then return found coalesce GgufMetadata {…}
  parse-from-bytes:
    if alignment_meta not is null {
      (alignment_meta coalesce GgufMetadata {…}).dtype
      _wire_count(alignment_meta coalesce GgufMetadata {…})
    }
  parse-from-source:
    const GgufMetadata alignment_value ← alignment_meta coalesce GgufMetadata {…}

Emit
  smol :6448  return Ok(found);                         # coalesce dropped
  smol :6841  (alignment_meta).dtype                    # E0609
  smol :6846  _wire_count(alignment_meta)?              # Option vs T
  smol :7019  let alignment_value: GgufMetadata = alignment_meta;
  qwen :6681 / :7074 / :7079 / :7252  same four shapes
```

Gate mail listed Smol E0308 as 6448+6846. rustc also emits **:7019**
(the `let alignment_value` assignment). That is the same family. Qwen
:7252 is the twin. F7 rustc is 4+4 (1 E0609 + 3 E0308 each).

**Emit.** ER-6 (`55dcc14bf`) unwraps `is_some()`-narrowed **Path** uses
whose HIR type is already `T` (`return Ok(found.clone().unwrap())`).
These sites are **`T ∪ null` + `coalesce` after `not is null`**. Emit
lowers `not is null` to `is_some()` and **elides the coalesce**, so the
Option binding is printed in a `T` position. `return_value_requires_option_unwrap`
does not fire: the HIR use-site type is still Option (coalesce was the
narrowing).

**Fix shape.** After a positive `not is null` / `is_some()`, emit the
coalesce as `.clone().unwrap()` / `if let Some(x)`, including field
access, call args, typed `let`, and `Ok(...)` payloads. Do not drop
`coalesce`.

### F13 — (c) residual: `impl Fn` parameter Path, not Type::Func

**Faber still has both arguments** (`gradus/src/model/dense.fab:124`):

```text
fn _source((string, int) → Lookup fons, string nomen, int stratum) → tensor.Tensor ⇥ DenseError {
    const Lookup r ← fons(nomen, stratum)
```

**Emit**

```text
fons: impl Fn(String, i64) -> Lookup
let r: Lookup = fons(nomen.clone());   // E0057, 1 of 2
smol :4078   qwen :3762
```

**ER-12 did not miss a Type::Func bug.** `bd979baca` is a **test**
(`rust_fn_value_call_keeps_all_arguments`) that proved a standalone
Latin Type::Func parameter call already emits `fons(nomen.clone(), stratum)`.
That path is `generate_call_expr` → `call_arg_target_types` (`callee.ty`
is `Type::Func`) → iterate **HIR args**.

**Identified receiver shape.** The live call is a **Path invocation of
an `impl Fn(String, i64) -> Lookup` parameter** (ER-4 spelling) inside
the inlined `dense::_source`. It is not the `fn(...)` / Type::Func
pointer value ER-12 locked.

`generate_call_expr` (`expr/call/mod.rs:115`) forks:

1. `function_params(def_id)` — named / imported function. Iterates the
   **signature**. Extra HIR args are dropped.
2. `call_arg_target_types` — `Type::Func` on `callee.ty`. Iterates
   **HIR args**. ER-12's oracle.
3. untyped — emit HIR args as-is.

The residual is fork (1) or a callee whose `ty` is not `Type::Func` at
this Path (impl-Fn parameter), not a missing second argument in Faber.

**Fix shape.** Calls through an `impl Fn` / function-typed **parameter
Path** must walk HIR args (fork 2 / untyped), not a one-slot named-function
signature. First failing oracle: `dense::_source` emits
`fons(nomen.clone(), stratum)`.

### F14 — (c) residual: inner fac `Err(String)` after ER-13

**Faber after ER-13** (`74114f29`, test-1 `main.fab:411`):

```text
do { present ← solum.exists(via) }
catch err { throw variant ArgumentaMala { message = "golden file missing: " + via } }
do { lines ← solum.read_lines(via) }
catch err { throw variant ArgumentaMala { message = "golden file unreadable: " + via } }
```

**Emit** (smol :770, :797)

```text
let ok: Result<(), PrefillError> = 'fac_result: {
    present = match crate::solum::exists(via.clone()) {
        Ok(fac_value) => fac_value,
        Err(fac_err) => break 'fac_result Err(fac_err),  // fac_err: String
    };
    Ok(())
};
```

The outer match **is** the cape (maps to `PrefillError::ArgumentaMala`).
The leaked path is the **inner** `break 'fac_result Err(fac_err)`:
`fac_result` is annotated with the **enclosing** `PrefillError`, while
`solum.exists` / `read_lines` fail as `String`.

ER-13 fixed the Faber shape. The remaining red is **do/catch / fac emit
typing**, not a missing consumer cape.

**Fix shape.** Type the inner fac block as the callee's error (`String`)
and let the cape map it; or insert `map_err` at the `break`. Do not
re-wrap the Faber.

### K5 — (a) moved `encoded` after `tokens = encoded`

**Representative**

```text
Faber: tokens ← encoded
       tokenizer_row ← "tokenizer: PASS ids=" + _ids_text(encoded)

smol :1062  tokens = encoded;  then _ids_text(encoded.clone())
```

Qwen has no this PASS-arm reuse. rustc E0382, help: clone.

**Fix shape.** `tokens = encoded.clone()` (or clone at the first use).
Mechanical. ER-11 cloned reused `String` on lista append (`cohaesum`);
this is the `Vec<i64>` twin.

## 5. Shared vs consumer-only

| Surface | Families |
| --- | --- |
| Shared library (tokenizer, GGUF, dense, transformer) | N1, N2, N3, F7, F13 |
| SmolLM2 consumer | F1 ×3, F14 ×2, K5 ×1 |
| Qwen2 consumer | F1 ×1 |

Smol − Qwen = +5 rustc: +2 F1, +2 F14, +1 K5.

## 6. Proposed unit split

One behavior family per unit. Repair is `radix-hir-rust` except F14's
oracle (Smol-only). First failing oracle is a rustc identity on a
re-emitted crate. Do not retune numerics. Do not weaken TARGETLANE001.

Recommended order: N1 (tiny, makes tables readable) → N3 (blocks
forward / GGUF readers) → N2 (blocks transformer proof) → F13 (blocks
`_source`) → residual tail.

| Unit | Class | Outcome | Write scope | First failing oracle | Closes rustc (union) | Depends |
| --- | --- | --- | --- | --- | --- | --- |
| **ER-15** | (a) | Const-list owned adapt writes `collect::<Vec<_>>()` (or the concrete `Vec<…>`) | `expr/mod.rs` `write_const_list_owned_suffix_for_type` | `TABULA_LITTERAE.iter().map(\|r\| r.to_vec()).collect::<Vec<_>>()`; E0282 gone | N1: 7+7 | — |
| **ER-16** | (c) | Map `addita_bias` → `addita` with the matmul Result ladder | `expr/call/intrinsics.rs` + `intrinsics/registry.rs` (ER-8 map) | `q.addita_bias(&bq)` becomes `q.addita(&bq)` + expect; E0599 gone on all six sites | N2: 4+4 (6+6 emit sites) | ER-8 pick (map, do not alias) |
| **ER-17** | (c) | Reborrow function values at reuse / pass-through (`&fons`). Not clone. Not FnMut. | call-arg emit of function-typed bindings; `_source` / `_read_source` / `_source_value` sites | `dense::forward` layer loop typechecks; rustc help "consider borrowing `fons`" gone | N3: 13+13 | ER-4 stays `impl Fn` |
| **ER-18** | (c) | `impl Fn` parameter Path calls keep every HIR argument | `expr/call/mod.rs` `generate_call_expr` (fork that is not Type::Func) | `dense::_source` emits `fons(nomen.clone(), stratum)` | F13: 1+1 | ER-12 Type::Func test stays; this is the other receiver |
| **ER-19** | (a)+(c) | Residual tail: F1 wrap `.to_string()` after `as`; F7 emit coalesce / unwrap on `T ∪ null`; F14 type inner fac as `String`; K5 clone `encoded` | `expr/convert.rs` numerus→textus; option+coalesce emit; fac/do-catch error type; owned-use clone | each rustc identity gone | F1 3+1; F7 4+4; F14 2+0; K5 1+0 | ER-1/6/13/11 leaks, not new design forks |

ER-15 and the F1/K5 half of ER-19 are mechanical and may share a Hand
**only if** each keeps its own oracle and commit. Prefer separate
commits. ER-17 is the only unit that needs the reborrow-vs-clone-vs-FnMut
pick written down; default if the planner does not reopen: **reborrow**.
ER-18 must not be closed by pointing at the ER-12 Type::Func test.

## 7. Out of scope / residuals

- No rustc warning classification (449 / 461).
- llvm-host / TARGETLANE001 / `fmir` package target / numerics untouched.
- Generated crates stay uncommitted build output.
- This file does not claim any family is fixed.
- ER-14 (locale TypeAlias / DEFID001) is not a rustc row on this stream.

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
