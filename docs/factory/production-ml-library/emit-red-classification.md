# Emit-surface rustc red classification (REF-01 U1.9 ∪ U1.10)

**Status**: planned — planner input, not a fix. No emit or library source
changed in this unit.
**Unit**: handle `58fe8ed4` / `a8b6daae` (hand-12). Classification only.
**Do not treat this file as evidence that a repair exists.** Live truth is
the two generated crates and the rustc streams cited below.

## 1. Receipts

Both crates share one rust HIR emit (`radix-hir-rust` at readable radix
`2ed9914e4`) and one inlined library surface (gradus + tokenizer / GGUF /
attention / dense). rustc 1.97.1 Homebrew. PKG001 `processus:exi` did not
reproduce on either FINAL run.

| Row | Crate | rustc | warnings | Artifact |
| --- | --- | ---: | ---: | --- |
| U1.9 SmolLM2 | `dense-prefill-smollm2` | 258 | 337 | `worktrees/hand-12/gradus/exempla/dense-prefill-smollm2/target/faber` |
| U1.10 Qwen2.5-0.5B | `dense-prefill-qwen2` | 248 | 350 | `worktrees/hand-13/gradus/exempla/dense-prefill-qwen2/target/faber` |

The SmolLM2 `target/faber` tree was absent at classification start
(build output, not committed). It was re-emitted with the same packet
`faber` binary and the U1.9 FINAL env; rustc again reported **258 / 337**.
The Qwen tree was preserved; `cargo check` reproduced **248 / 350**.

U1.9 README over-counted bare cast lines (5 vs the 3 rustc actually
emits). The tables below use the re-parsed streams.

## 2. How to read the counts

rustc often emits **two diagnostics per site** (`vec![]` → `new_uninit` +
`into_vec`; `format!` → macro + `format` function; `format!` in a `const
String` also yields E0493 destructors). The **rustc** columns are the
official error counts. The **sites** column is unique `file:line` emit
constructs, which is the planner grain.

Union = shared library surface + per-consumer extras. A family that
appears in both crates is one emit defect, not two.

Class:

- **(a)** mechanical parenthesization / precedence / clone / unit-arm
- **(b)** const-eval legality (Rust `const` item cannot run heap / format)
- **(c)** genuine type-level or name-mapping gap that needs a design pick

Repair owner is **radix rust HIR emit** unless a row says otherwise.
Gradus Faber source is not the defect for the shared families.

## 3. Union family table

| ID | Class | Family | Smol rustc | Qwen rustc | Sites (shared unless noted) | Emit construct |
| --- | --- | --- | ---: | ---: | --- | --- |
| F1 | (a) | `as` then method / then `/` | 4 | 2 | 3 consumer + 1 lib (smol); 1 consumer + 1 lib (qwen) | `Conversio` / widening `as` without wrapping the operand the postfix or `/` binds to |
| F2 | (b) | const `vec![]` (incl. nested) | 62 | 60 | ~16 unique `const` lists (smol +1 `GOLDEN_TOP5`) | `generate_const` + `emit_array_expr` → `Vec<T> = vec![…]` |
| F3 | (b) | const `String = format!("{}{}", …)` + String dtor | 115 | 115 | 2 tokenizer pins (`PINNATA_NORMALE`, `PINNATA_CONTEXTUS`) | text `+` → `format!("{}{}", …)` inside `pub const` |
| F4 | (b) | const `lit.to_string()` in `vec![String]` | 33 | 33 | 33 elements of `EOG_NOMINA` / `FIM_*` | owned `String` element in a const list |
| F5 | (c) | capturing closure vs `fn(…) -> T` | 3 | 3 | 3 (reader, inspect, `dense::forward`) | `Type::Func` → `fn(…) -> T` (`types.rs`) |
| F6 | (c) | `&str` where `String` expected | 17 | 13 | 12 `pinned_probe` + `PROMPT` use; smol +4 argv / `PINNED_PATH` | `const string` literal emitted as `&'static str`; uses still typed `String` |
| F7 | (c) | `Option<T>` not narrowed after `is_some()` | 4 | 4 | 4 GGUF metadata | Faber option flow; rustc keeps `Option` |
| F8 | (c) | collection / integer → byte | 4 | 4 | 1 `Vec<i64> as Vec<u8>` + 3 `push(i64)` into `Vec<u8>` | `verte` / `as` on non-primitives; missing `i64 → u8` |
| F9 | (c) | Faber tensor method names on `faber::Tensor<T>` | 6 | 6 | 6 (`transpone`×2, `activatio_softmax`×2, `laminatio`×2) | method name passed through; runtime has English names |
| F10 | (c) | `String.accipe(i)` | 3 | 3 | 3 tokenizer hex / index helpers | `accipe` is a tensor/lista/tabula intrinsic, not `str` |
| F11 | (a) | `fac` arm `()` vs `Result<_, E>` | 3 | 3 | 3 tokenizer FIM metadata | `fac`/`cape` emit leaves a `()` arm |
| F12 | (a) | moved `String` reused in loop | 1 | 1 | 1 BPE merge (`cohaesum`) | owned use without `.clone()` |
| F13 | (c) | `fons(nomen)` dropped layer arg | 1 | 1 | 1 `dense::_source` | call through `fn(String, i64)` with one argument |
| F14 | (c) | `?` `String` → consumer error | 2 | 0 | 2 SmolLM2-only (`solum::exists` / `read_lines`) | `?` without `From<String>` |

Checksum: Smol 4+62+115+33+3+17+4+4+6+3+3+1+1+2 = **258**. Qwen
2+60+115+33+3+13+4+4+6+3+3+1+1 = **248**.

Const-eval (F2+F3+F4+E0493 folded into F3) is **210 / 208** of the two
crates. Everything else is a long tail of distinct emit seams.

## 4. Family detail

### F1 — (a) `as` then method / `as` then `/`

**Representative**

```text
smol src/main.rs:766
  lines.len() as i64.to_string()
  rustc: "cast cannot be followed by a method call"
  intended: (lines.len() as i64).to_string()

smol :987, :1200  — same shape on .len() as i64.to_string()
qwen  :993        — m.tensors.clone().len() as i64.to_string()

both  attention::_reduce_angle
  let k: i64 = shifted / TAU.floor() as i64;
  rustc E0277: cannot divide f32 by i64
  parse: shifted / (TAU.floor() as i64)
  intended: (shifted / TAU.floor()) as i64
```

**Emit.** `radix-hir-rust` writes ` as T` in `expr/mod.rs`
(`numeric_widening_cast_ty`), `expr/verte.rs` (primitive `∷`/`as`), and
`expr/ops.rs` (operand casts). Ordering comparisons already parenthesize
an `as` lhs (`ordering_comparison_lhs_needs_parens`). Postfix `.method`
and `/` do not. Rust `as` binds tighter than `*` `/` `%` and cannot be
followed by a method.

**Fix shape.** Always wrap the `as` expression: `(<expr> as T)` when the
parent is a method, field, call, or binary op.

**Not a Gradus bug.** The Faber is `lines.length() ∷ int` then
`.to_string()`, and `shifted / TAU.floor()` ascribed to `int`.

### F2 — (b) const `list<T> = […]` → `const Vec<T> = vec![…]`

**Representative**

```text
smol :25   pub const PINNED_TOKENS: Vec<i64> = vec![504, …, 2767];
smol :29   pub const GOLDEN_TOP5: Vec<i64> = vec![30, 28, 1270, 365, 198];
qwen :26   pub const PINNED_TOKENS: Vec<i64> = vec![785, …, 3283];
lib  :11817 pub const TABULA_LITTERAE: Vec<Vec<i64>> = vec![vec![65, 90], …];
lib  :11166 pub const EOG_NOMINA: Vec<String> = vec![ "<|eot_id|>".to_string(), … ];
```

Each `vec![]` yields two E0015s (`Box::<[T; N]>::new_uninit` and
`box_assume_init_into_vec_unsafe`). Nested `vec![vec![…]]` unicode
tables multiply the count.

**Emit.** `generate_const` (`decl.rs:1186`) types the item with
`type_to_rust` → `Vec<T>`. `emit_array_expr` (`expr/collection.rs:46`)
always writes `vec![…]`. `generate_const` already special-cases
**string-literal** consts to `&'static str` because “Rust rejects heap
String construction in a const item” (`decl.rs:1193`). Lists were not
given the same treatment.

**Fix shape (design pick, still one family).** In a `const` item, emit
`&'static [T]` / `[T; N]` (and `&'static [&str]` for text lists). Use
sites that need `Vec` get `.to_vec()`. Do not emit `vec![]` or
`.to_string()` in a const initializer.

F4 (the 33 `to_string` E0015s) is the text-element half of this family.

### F3 — (b) const text concatenation → `format!("{}{}", …)`

**Representative**

```text
both tokenizer module
  pub const PINNATA_NORMALE: String = format!("{}{}", format!("{}{}", …), …);
  pub const PINNATA_CONTEXTUS: String = format!("{}{}", …);  // ~36 nested
```

Qwen lines `:10533` / `:10535`. Smol `:10245` / `:10247`. rustc: 78×
E0015 (`format!` + `format`) and 37× E0493 (`destructor of String cannot
be evaluated at compile-time`) on the **same two items**. Nested
`format!` is why one Faber `const string` becomes dozens of rustc rows.

**Emit.** Text `+` → `format!("{}{}", lhs, rhs)` in `expr/ops.rs:341`.
`const_textus_uses_static_str` only fires for a **single string
literal**. Concatenated literals stay `const String = format!(…)`.

**Fix shape.** In a const item, fold literal concatenations to one
`&'static str` (or `concat!(…)`, which is const). Same policy already
used for non-concat string consts.

### F4 — (b) const `vec![lit.to_string(), …]`

Satellite of F2. 33 E0015 `<str as ToString>::to_string` in both crates,
all inside `EOG_NOMINA` / `FIM_PAD_NOMINA` / `FIM_REP_NOMINA` /
`FIM_SEP_NOMINA`. Close with F2 (const list-of-text as `&'static [&str]`).

### F5 — (c) capturing closure coerced to `fn` pointer

**Representative**

```text
qwen :390  materialize_slice(..., |start, length| file_range(path.clone(), total, start, length))
qwen :779  inspect(|start, length| prefix_range(prefix.clone(), start, length), …)
qwen :885  dense::forward(..., |name, layer_i| lookup_one(name.clone(), layer_i, embed.clone(), …), …)
```

Same three sites in SmolLM2 (`:426` and the inspect / forward twins).
rustc: `expected fn pointer, found closure` + “closures can only be
coerced to `fn` types if they do not capture”.

**Emit.** `Type::Func` always prints `fn({}) -> {}`
(`types.rs:165-177`). Library parameters are therefore

```text
fons: fn(i64, i64) -> SourceRead
fons: fn(String, i64) -> Lookup
```

Faber function values that capture (`path`, `total`, `embed`, …) cannot
inhabit that type.

**Design pick (required).** One of:

1. Emit `impl Fn(…) -> R` on parameters (or `F: Fn(…) -> R`).
2. Emit `Box<dyn Fn(…) -> R>` / `&dyn Fn`.
3. Keep `fn` pointers and reject capturing lambdas at typecheck.

(1) matches the Faber meaning (function values close over locals). (3)
would break these three public GGUF / dense call sites.

### F6 — (c) `&'static str` const used as `String`

**Representative**

```text
qwen :1017   encode_ids(tok.clone(), PROMPT.clone())  expected String, found &str
qwen :10832  return Ok(PINNATA_P1);  // PINNATA_P1: &'static str, Result<String, _>
smol :814    argv() as Vec<String>
smol :821    unwrap_or(PINNED_PATH)   // PINNED_PATH: &'static str
```

12 shared `pinned_probe` arms (`p1`…`brevis`). Smol adds argv /
`PINNED_PATH` (`:814`, `:816`, `:821`, `:836`).

**Emit.** `generate_const` / static textus fields emit `&'static str` for
a string-literal initializer so the `const` item is legal. The Faber type
is still `string`. Uses, `Result<String, _>`, and `unwrap_or` are not
converted back to owned `String`.

**Design pick.** Either (i) keep `&'static str` and insert `.to_string()`
/ `String::from` at every owned use, or (ii) stop special-casing the
const type and make F3’s concat path the one const-legal form
(`concat!` / flattened literal) so the item type can stay `String` only
when it is truly heap, otherwise `&'static str` consistently with
coercions at the seam. (i) is local; (ii) is the cleaner policy and
should land with F3.

### F7 — (c) `Option` not unwrapped after `is_some()`

**Representative**

```text
qwen :6677  if found.is_some() { return Ok(found); }   expected GgufMetadata, found Option<_>
qwen :7070  if alignment_meta.is_some() { alignment_meta.dtype … }   E0609
qwen :7075, :7248  _wire_count(alignment_meta) / same Option passed as GgufMetadata
```

**Emit.** Faber treats a binding as `T` after `is_some()`. Rust emit
leaves the `Option<T>` value in place. This is option-narrowing, not a
missing field on `GgufMetadata`.

**Fix shape.** After a positive `is_some()` / `== Some`, emit
`.as_ref().unwrap()` / `if let Some(x) = …` (or compile-time narrowing
temps). Same seam as other option-flow emit work.

### F8 — (c) `list<int> as list<byte>` and `int` into `Vec<u8>`

**Representative**

```text
qwen :122   let bytes: Vec<u8> = segment as Vec<u8>;   E0605 non-primitive cast
qwen :5946  out.push(v);   v: i64, expected u8
qwen :11282, :11773  same i64 → u8 push
```

**Emit.** `verte` / `as` for primitives writes ` as T`. For `Vec<i64>` it
still writes ` as Vec<u8>` (`prefix_range`, `_byte_from_list` even does
`b as Vec<u8>` on a value that is already `Vec<u8>`). Element stores do
not insert `as u8`.

**Fix shape.** Collection `as` maps elementwise (`into_iter().map(|x| x
as u8).collect()`). Integer used as `u8` gets an explicit narrowing
cast. Not parenthesization.

### F9 — (c) Faber tensor method names vs runtime names

**Representative**

```text
qwen :1141  kb.transpone()            // runtime: transpose_rank2
qwen :1144  scaled.activatio_softmax() // runtime: softmax
qwen :12698 r1.laminatio(1, 0.00001, &ln2_s, &ln2_o)  // runtime: layernorm
```

Same six sites in both crates (attention 2×2 + transformer proof row
2× `laminatio`). `faber/runtime/rust/src/tensor.rs` already has
`transpose_rank2`, `softmax`, `layernorm`. The emit prints the Faber
identifiers.

**Fix shape.** Map those three method symbols onto the runtime names
(and `Result` unwrap / `?` policy already used for `matmul`). Do not add
Latin aliases on the runtime unless a second caller needs them.

### F10 — (c) `textus.accipe(i)`

**Representative**

```text
qwen :10660  if !_is_hex(s.accipe(i))
qwen :10699, :10778  same
```

`accipe` is registered for lista / tabula / tensor / sparsa
(`intrinsics/registry.rs`). It is not a `String` method. Emit of
`string.accipe(i)` should be `chars().nth(i as usize)` (or the existing
text slice helper used elsewhere in the same file).

### F11 — (a) `fac` success-path `()` vs `Result`

**Representative**

```text
qwen :12412, :12482, :12573
  match { let ok: Result<…, TokenizerError> = 'fac_result: { …; () } }
  expected Result<(), TokenizerError>, found ()
```

Tokenizer FIM metadata: the `cape` arm returns `Err(…)`, the fall-through
is a bare `()`. Mechanical `fac` block emit. Wrap the unit tail as
`Ok(())`.

### F12 — (a) moved `cohaesum: String` in the BPE loop

**Representative**

```text
qwen :11595  novum.push(cohaesum);   then loop again
```

Emit of a reused owned `String` without `.clone()`. rustc help is
exactly the fix. Same site in both crates.

### F13 — (c) `fons(nomen.clone())` missing `stratum`

**Representative**

```text
qwen :3757-3762
  fn _source(fons: fn(String, i64) -> Lookup, nomen: String, stratum: i64)
  let r: Lookup = fons(nomen.clone());   // E0061, argument #2 i64 missing
```

The parameter is present and unused. Either the Faber call is
`fons(nomen, stratum)` and emit dropped the second argument, or the
Faber source is one-arg and the `fn(String, i64)` type is the real
defect (then F5’s function-type work must also preserve arity). One
site, both crates. Inspect `gradus:model/dense` `_source` when fixing;
do not guess.

### F14 — (c) SmolLM2-only `?` on `Result<_, String>`

**Representative**

```text
smol :758  if !crate::solum::exists(via.clone())?
smol :763  let lines: Vec<String> = crate::solum::read_lines(via.clone())?;
  E0277: PrefillError needs From<String>
```

Qwen does not load a golden file this way, so the pair is consumer-only.
Either emit a mapped `fac`/`cape` (the surrounding function already
does that for parse errors) or emit `.map_err(|e| PrefillError::…{e})?`.
Not shared library.

## 5. Shared vs consumer-only

| Surface | Families | Notes |
| --- | --- | --- |
| Shared library (tokenizer, GGUF, attention, dense, transformer) | F2 tables, F3, F4, F5, F6 `pinned_probe`, F7–F13, F1 `_reduce_angle` | One radix fix clears both crates |
| SmolLM2 consumer | F1 three print/golden casts; F6 argv/`PINNED_PATH`; F2 `PINNED_TOKENS`+`GOLDEN_TOP5`; F14 | Extra 10 rustc vs Qwen (258−248) |
| Qwen2 consumer | F1 one tensors-print cast; F2 `PINNED_TOKENS`; F6 `PROMPT` | No F14 |

The +10 SmolLM2 reds are: +2 F1 casts, +2 F2 (`GOLDEN_TOP5` pair), +4 F6
argv/`PINNED_PATH`, +2 F14. No family is unique to Qwen.

## 6. Proposed unit split

One behavior family per unit. Repair is radix `radix-hir-rust` unless
noted. First failing oracle is a rustc identity on a re-emitted crate
(either consumer). Do not retune numerics. Do not weaken TARGETLANE001.

Recommended order: F1 (tiny, makes the crate readable) → F2+F4 (largest
count) → F3 (second count, same const policy) → F5 (blocks readers /
forward) → F9 (blocks attention) → remaining tail in parallel.

| Unit | Class | Outcome | Write scope | First failing oracle | Closes rustc (union, both crates) | Depends |
| --- | --- | --- | --- | --- | --- | --- |
| **ER-1** | (a) | Parenthesize every emitted `as T` when the parent is a method, field, index, call, or binary op | `radix-hir-rust` `expr/mod.rs` (`numeric_widening_cast_ty`), `expr/verte.rs`, `expr/ops.rs` (reuse `ordering_comparison_lhs_needs_parens`) | `len() as i64.to_string()` becomes `(len() as i64).to_string()`; `_reduce_angle` is `(shifted / TAU.floor()) as i64` | F1: 4+2 | — |
| **ER-2** | (b) | `const` list (int, list-of-int, list-of-text) emits a const-legal array / `&'static [T]` / `&'static [&str]`, not `vec![]` or `.to_string()` | `decl.rs` `generate_const`; `expr/collection.rs` `emit_array_expr` (const context); use-site `.to_vec()` if the Faber type is `list` | `PINNED_TOKENS` and `TABULA_LITTERAE` compile as const; EOG/FIM name tables have no `.to_string()` in the initializer | F2+F4: 95+93 | — |
| **ER-3** | (b) | `const` text concatenation folds to one `&'static str` or `concat!(…)` | `decl.rs` `const_textus_uses_static_str` (extend past single literals); `expr/ops.rs:341` const path | `PINNATA_NORMALE` / `PINNATA_CONTEXTUS` are const-legal; E0015 format + E0493 on those lines gone | F3: 115+115 | ER-2 policy should match (text const = `&'static str`) |
| **ER-4** | (c) | Function-typed parameters accept capturing closures | `types.rs` `Type::Func`; any call-site coercion | `materialize_slice` / `inspect` / `dense::forward` accept the emitted `|…| { … capture }` | F5: 3+3 | design pick §4 F5 |
| **ER-5** | (c) | Owned-`string` uses of a `&'static str` const insert `.to_string()` / `String::from` (or the F3 type policy makes the item type match) | use-site `expr_as_type` / `write_owned_textus_suffix`; `generate_const` consumers | `pinned_probe` `Ok(PINNATA_P1)` and `encode_ids(…, PROMPT)` typecheck | F6: 17+13 | ER-3 if policy (ii) |
| **ER-6** | (c) | After `is_some()`, emit a narrowed `T` (unwrap / `if let`) | option-narrowing in expr emit | `metadata` `return Ok(found)` and `alignment_meta.dtype` typecheck | F7: 4+4 | — |
| **ER-7** | (c) | `list<int> as list<byte>` maps elements; `int` stored as `u8` is `as u8` | `expr/verte.rs` / convert aggregate; integer narrowing at `push` | `prefix_range` `segment as Vec<u8>` compiles; `_byte_from_list` loop pushes `u8` | F8: 4+4 | — |
| **ER-8** | (c) | Map `transpone` → `transpose_rank2`, `activatio_softmax` → `softmax`, `laminatio` → `layernorm` (plus existing Result handling) | tensor method emit / runtime-contract map | `scaled_dot_product_*` and the transformer proof row typecheck against `faber::Tensor<f32>` | F9: 6+6 | — |
| **ER-9** | (c) | `textus.accipe(i)` emits a char/index helper, not `.accipe` | `expr/call` / textus intrinsic path | `_hex_ok` / tokenizer index helpers typecheck | F10: 3+3 | — |
| **ER-10** | (a) | `fac` block whose value type is `Result<(), E>` emits `Ok(())` on the unit tail | `fac`/`cape` emit | three FIM metadata matches typecheck | F11: 3+3 | — |
| **ER-11** | (a) | Reused owned `String` in a loop is cloned (or the temp is recreated) | owned-use emit | BPE `novum.push(cohaesum)` no E0382 | F12: 1+1 | — |
| **ER-12** | (c) | `fons(nomen, stratum)` keeps both arguments (or the `fn` type matches the call) | call emit through `Type::Func` values | `dense::_source` E0061 gone | F13: 1+1 | ER-4 if the type changes |
| **ER-13** | (c) | SmolLM2 `solum` `?` maps `String` into `PrefillError` | consumer `fac` emit **or** exempla `dense-prefill-smollm2` if the Faber already has a cape | `_load_golden` E0277 gone | F14: 2+0 | not shared; do not block the library wave |

ER-1, ER-10, ER-11 are mechanical and can share one Hand if the write
scope stays inside `radix-hir-rust` expr emit **and** each keeps its own
oracle. Prefer three commits. ER-2 and ER-3 share the const-item policy
and should be sequenced, not parallel. ER-4 is the only unit that needs
a design pick before coding; default if the planner does not reopen:
**`impl Fn(…) -> R` on parameters** (option 1).

## 7. Out of scope / residuals

- No rustc warning classification (337 / 350). They are unused bindings
  and the usual generated-code noise; they do not block the crate.
- llvm-host remains `PKG001:llvm_emission_failed` on U1.9. Not this wave.
- Numerics, GGUF execution, TARGETLANE001, and `fmir` as the package
  `[build] target` are untouched.
- Generated crates stay uncommitted build output.
- This file does not claim any family is fixed.

## 8. Re-parse commands

```text
# Qwen (preserved crate)
cargo check --manifest-path \
  worktrees/hand-13/gradus/exempla/dense-prefill-qwen2/target/faber/Cargo.toml \
  --target-dir worktrees/hand-13/gradus/exempla/dense-prefill-qwen2/target

# SmolLM2 (re-emit, then rustc is inside faber build)
env FABER_SUPPORT_PATH_OVERRIDE=/Users/ianzepp/work/faberlang \
  FABER_LIBRARY_HOME=/tmp/faber-hand-12-libhome \
  <packet-faber> build --target rust exempla/dense-prefill-smollm2
```
