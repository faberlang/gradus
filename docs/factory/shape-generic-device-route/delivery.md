# DELIVERY: shape-generic-device-route — clean-break library geometry

**Status**: active — U1–U3 + U2-R* on radix main `7e0225565`; U4 planner `d84ad723`; U5 waits U4
**Goal:** [`goal.md`](goal.md)
**Source:** operator 2026-09-03 (clean break; SmolLM2 stays a fixture); goal rewrite gradus `084f4de`
**Repos:** `radix/` (U1–U3, U5, U7 compiler/export), `gradus/` (U4 library kernels, U7 ratchet)
**Release:** defer-release

---

## 1. Interpreted unit

Gradus public `@ kernel` leaves must not carry model geometry. SmolLM2-360M remains the parity/smoke model; its sizes are admitted in implementation, fixtures, or tests and instantiated. The compiler must turn an **imported** size-generic Gradus kernel into a concrete Metal entry (today same-unit generics work; imported ones do not become device programs). Export must stop manufacturing source by splicing `[76,` in a test module.

This delivery covers the whole admitted goal (SGD-1…6). It does not leave statue signatures in `kernel.fab`.

## 2. Normalized spec

- One library surface: `size` parameters only on public Gradus kernels.
- Concrete numbers: admission / fixtures / tests / measurement TOMLs / monomorphized artifacts.
- Imported generic `@ kernel` → concrete Metal with substitutions in identity. No source-specialization fallback.
- Compiler-owned export API; tests call and pin; no signature splice.
- First instantiation = current SmolLM2 tuple. Second model compiles with zero `gradus/src/kernel*` edits.
- v1 measurement rows stay. Dual library path refused.

## 3. Repo-aware baseline (live 2026-09-03)

| Fact | Where |
| --- | --- |
| Language `size` params exist | `radix/docs/archived/shape-generics/` done 2026-08-18 |
| Same-unit generic Metal size-bakes | `gradus/scripta/spike-shape-generic-kernel/spike2-local-generic.fab` (green in 2026-08-26 proof) |
| `math.add<size M, size N>` is `@ kernel @ public` | `gradus/src/math.fab:264–268` |
| Imported generic result typed `ignotum` (SEM010/SEM011/WARN010) | `gradus/docs/factory/kernel-purity-census/consumer-proof-2026-08-26.md` spike1/spike3 controls |
| Host import of `math.add` does not produce a Metal kernel entry | `spike3-host-caller.fab` → `metal-text requires at least one @ nucleum function` |
| Package path **does** call device-aware instantiate (SGR-U0 / KPC-WIRE) | `radix-program/src/mir/lower.rs:1983–2021` `instantiate_merged_generic_calls_with_devices_and_metadata`; registrations stored |
| Single-unit lower still sets `imported_device_registrations: Vec::new()` | `radix-module/src/mir/lower.rs:421` |
| Routes are collected | `radix-module/src/mir/lower.rs:396`; `radix-module/src/mir/lower/context.rs` `imported_device_routes` |
| GEA3 export splices `[76,` | `mir-emit-harness/src/gea3_pipeline_test.rs:849–852` (`canonical_entry_at_with_work_extent`) |
| `kernel.fab` is SmolLM2 literals | decode/prefill signatures e.g. `[1,960]`, `[76,64]`, `[36,960]` (`gradus/src/kernel.fab:282–550`) |
| Generic twins already exist for nn/math | `nn.linear<size M,K,N>` `nn.fab:331` |
| Head-axis U4 batched literals (packet only) | gradus packet `6506c03` — condemned; do not merge as the API |

**Check-first:** U1/U2 Hands re-run spike2/spike3 against packet `faber` before writing. If spike3 already emits Metal and imported `math.add` unifies, close that unit with evidence.

## 4. Stage graph (Hand units)

| id | outcome | write_scope | depends_on | done_when | sanity | non_goals | integrable |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **U1** | Imported size-generic Gradus call unifies to a concrete tensor type (no `ignotum` / SEM010 pair on annotated `math.add` result; explicit `<M,N>` not SEM011-dynamic) | `radix/crates/radix-semantic` (import/generic instantiation typing); tests; optional probe next to `gradus/scripta/spike-shape-generic-kernel/` **only if** the probe is the oracle (prefer radix-semantic tests) | — | Red-first: current consumer diagnostic captured; green: host caller `const tensor<f32, [2, 2]> r ← math.add(a, b)` typechecks; same-unit spike2 still green | `cargo test -p radix-semantic` focused; `cargo run -p faber -- check` on spike3 (check only) | No Metal emit; no `kernel.fab`; no export splice | yes |
| **U2** | Single-file `faber build -t metal-text` on an importing `.fab` uses the **module** lane (`use_package_compiler` false), so `imported_device_registrations` never exist and metal-text sees only `main`. **Edit:** `radix/crates/faber/src/package/cmd.rs` (~670) `use_package_compiler` — route `.fab` + metal-text that imports a library through the interpreted merged consumer (driver already joins registrations → roles, `radix-module/src/driver/mod.rs` ~886). Do not fake-green the empty-kernels check. | `radix/crates/faber/src/package/cmd.rs` (and a focused test there) | U1 | `faber build -t metal-text` on `spike3-host-caller.fab` emits a kernel; spike2 still emits; no empty-kernels relaxation | that metal-text command | No `kernel.fab`; no splice; no re-implementing package instantiate inside radix-module | yes |
| **U3** | Compiler-owned export: GEA3 manufacture does not splice `[76,` / `,76]` in `#[cfg(test)]`. A non-test API returns instance table + ordered size bindings + emitted source + identity. Existing harness **calls** it for the SmolLM2 fixture tuple — named seam in §4a | `radix/crates/radix-module/src/device_export.rs` (new) + `src/lib.rs` module decl + sibling `device_export_test.rs`; `radix/crates/mir-emit-harness/src/gea3_pipeline_test.rs` (rewire + splice delete) | — (after U2; U2 landed) | `rg '\.replace\("\[76,"|\.replace\(",76\]"' radix/crates` → 0 hits; `export_device_instance` pinned by a radix-module test (record fields concrete, identity changes when bindings change); frozen-76 statue entries compile unchanged with sha pins intact; GEA3 non-frozen extent tests (PGC-B1/B2 family) green through the API | `cargo test -p mir-emit-harness gea3` | No `kernel.fab` edit (U4); no second model (U6); no v2 identity files (U8); no generic twins beyond entries exercised at non-frozen extents | yes — statue bytes stay a test-owned fixture on the frozen path; non-frozen path is generic twin + ordered bindings, no library law |
| **U4a–U4e** | Clean-break `gradus/src/kernel.fab` (+ `kernel.proba`) in **five named family slices** — every `@ kernel` entry (public or not) moves to `size` params; statue signatures deleted (batched `[5,76,64]` head-axis forms never enter). Full named-edit graph: **§4b** | `gradus/src/kernel.fab`, `gradus/src/kernel.proba` (family rows only) | U1, U2; slices serial U4a→U4e (one file, one packet) | per slice, §4b; file-level oracle lands on U4e | one `faber test src/kernel.proba <family>` per slice | No prefill/decode algorithm change; no new glyphs; no entry renames | **no** — U4e merges with U5 |
| **U5** | GEA3 / product fixtures instantiate the SmolLM2 tuple (`D=960, H=15, KV=5, d=64, C=76, T_p=36`, …) against generic kernels. Export uses U3 API. No new Rust signature table | `radix/crates/mir-emit-harness/src/gea3_pipeline_test.rs` (+ support); tests only | U3, U4 | decode/prefill programs still export; census derived from instantiated program; `kernel.fab` untouched in this unit; `[76,` splice not reintroduced | focused gea3 tests | No second GGUF | **no** — pair with U4 |
| **U6** | Second-config proof: different geometry + capacity/extent, zero `gradus/src/kernel*` edits, no signature table | radix harness **fixture** (or a new test file); not library src | U5 | second tuple metal-text or device compile; `git diff` on `gradus/src/kernel*` empty of new literals/forms | focused test for the second fixture | No CUDA physical; no new attention family | yes |
| **U7** | Ratchet + product splice deletion: named check that `gradus/src/**/*.fab` public kernel signatures have no model-geometry literals; live product path does not splice | `gradus/scripta/` or `radix/scripta/` ratchet; leftover splice call sites | U5 | ratchet fails if a signature reintroduces `960`/`76`/`36` as library types; splice gone from non-test manufacture | ratchet self-test | No parity `--stage smoke` on this Hand | yes |
| **U8** | SGD-5: v2 identity/parity files only (new files; v1 rows untouched) | radix `scripta/perf-parity-targets/` and/or `scripta/parity-baselines/` as named at dispatch; no library src | U6 | v2 identity family exists; v1 rows unchanged | focused identity tests or receipt pin | No library edits | yes |

U0 from the goal (record the break) **is this delivery**. No Hand.

### 4a. U3 Hand pointer (re-lowered 2026-09-03, handle `450c84ed` — one unit, not split)

One logical change: the export API and the harness flip are producer and consumer of one seam with one done oracle; splitting would land an unused API unit.

**Add (product, non-test):** `radix/crates/radix-module/src/device_export.rs`

- `pub fn export_device_instance(session: &Session, name: &str, entry_source: &str, bindings: &[(String, u64)]) -> Result<DeviceInstanceExport, …diagnostics>` — compiles a size-parametric entry source at ordered size bindings; no string splicing anywhere.
- `pub struct DeviceInstanceExport { instances, bindings, code, reflection, identity }` — instance table (entry + concrete shapes/substitutions, shaped from `MirMonomorphizationKey` / `ImportedDeviceRegistration`), ordered bindings echo, emitted Metal source, `MirGpuReflection`, identity digest over entry-source digest + ordered bindings + target + emitted digest (U8 mints the v2 identity files from this).
- Declared from `crates/radix-module/src/lib.rs`; feature-gated to match the driver's metal-text path; pinned by sibling `device_export_test.rs`.
- Instantiate through the device-aware machinery U1/U2 opened — `instantiate_merged_generic_calls_with_devices_and_metadata` (`radix-program/src/mir/lower.rs:1983–2021`) with the driver's registration join (`radix-module/src/driver/mod.rs:690`). A request-level bindings field inside this new module is equally in-scope; inventing a new lane is not.
- **Q2 settled:** `radix-mir` placement is DAG-impossible (`radix-module` → `radix-mir`; the API must compile source and return emitted text). `radix-module` owns `Session`, `compile`, the registrations, and `MetalTextOutput` — the one obvious crate, no new repo, no new crate.

**Change (harness, test-only):** `crates/mir-emit-harness/src/gea3_pipeline_test.rs`

- `pipeline_source_at_with_work_extent` (~866, splice calls ~868/~870) and `canonical_entry_at_with_work_extent` (~638, splice call ~697) stop calling `statue_signature_at`.
- Non-frozen capacity / work-extent paths call `export_device_instance` with a **test-owned size-param twin** of the specialized entry + ordered bindings (`capacity`, `work_extent`); twins only for entries exercised at non-frozen extents (the four `dynamic_attention_entry` members plus whatever PGC-B1/B2 capacity tests touch).
- Delete `statue_signature_at` (~843) and `statue_signature` (~840) with their `.replace("[76,"` / `.replace(",76]")` calls.
- Frozen `HISTORY_CAPACITY` paths compile the unchanged statue bytes directly (no bindings, no twin); `EntrySpec.source_sha256` drift pins stay on real statue text.

### 4b. U4 named-edit Hand pointers (re-lowered 2026-09-03, handle `d84ad723` — five slices, serial)

Operator 2026-09-03: Hands implement a **named function/seam**. U4-as-one-bag was a theme; five one-logical-change slices follow `kernel.fab`'s own family blocks (50 `@ kernel` entries total, public or not — non-public statues are still statues). Each slice converts one family's signatures to `size` params (spelling: `math.add<size M, size N>`, `gradus/src/math.fab:266`; callers with concrete tensors instantiate — U1's `math.add(a, b)` host-caller proof), rewrites that family's inventory comment size-symbolically, and updates **only that family's** `kernel.proba` rows to instantiate the SmolLM2 tuple (proba is a fixture; `960/76/36` are legal there).

**Shared slice law** (binds every U4 slice; do not re-litigate per Hand):

- Signature extents become size params from the goal vocabulary, as **flat extents** (`T D K F V C d P`): factored relations (`K = KV·d`, `Q = H·d`) are admission/fixture facts, not signature expressions.
- The decode-step `1` in `[1,·]` stays literal (decode contract, not model geometry; `T_p=36` is the cut prompt fact, `T=1` is not in the cut list). KV-names law: capacity extent is `C`, prompt extent `T`, position stays runtime-only.
- `rms_norm` epsilon `0.00001` stays frozen (hyperparameter, not geometry). `attention_scale` / `length_mask` / `causal_mask` stay caller-supplied tensors.
- **Entry names stay byte-stable.** The radix harness pins names as strings and compiles the live file (`gea3_pipeline_test.rs:33` `include_str!("../../../gradus/src/kernel.fab")`, entries at `:210…`), so `cargo test -p mir-emit-harness gea3` goes red from the first landed slice until U5 rewires instantiation — expected, not a Hand failure. No slice touches radix.
- No head-axis batched forms (`[5,76,64]` / `[5,3,1,64]`, packet `6506c03`) enter the file; absent on main, and their absence is part of U4e's file-level oracle.
- Sanity is run with the packet's in-workspace `faber` binary from the packet `gradus/` root. Line anchors are gradus main `86921e0` (2026-09-03); the Hand re-anchors if the file moved.

| id | outcome (one logical change) | write_scope | depends_on | done_when | sanity (one command) | non_goals | risk | integrable |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **U4a** | GEA1 GEMV pair + host admission de-statued: `gemv_bf16_f32acc`, `gemv_f32_f32acc` → `<size N, size K>` (`kernel.fab:131–144`); helpers `bf16_view`, `f32_view`, `validate_bf16_view`, `validate_f32_view` (`:95–125`) stop pinning `[320,960]` — delete `GEMV_N`/`GEMV_K`/`GEMV_ELEMENTS` (`:41–45`) and `gemv_shape` (`:82–84`); validators check self-consistency (dtype tag; byte range vs declared shape × `dtype.width`; input length vs declared extent), not the SmolLM2 tuple; file header comment (`:5–37`) rewritten size-symbolically; proba `gea1_*` rows (5) instantiate `N=320, K=960` | `gradus/src/kernel.fab`, `gradus/src/kernel.proba` (gea1 rows) | — (U1–U3 landed) | both GEMV entries and all four helpers carry no `320`/`960`; `gea1` proba rows green including the reject rows (wrong dtype / short payload / short input still throw) | `faber test src/kernel.proba gea1` | No dtype-module changes; no GEA2+ entries; no view-class field changes | medium — validation semantics shift (self-consistency vs tuple equality), not just signatures | **no** |
| **U4b** | GEA2 block family (13 entries, `kernel.fab:147–241`) to size params: `rmsnorm<T,D>`, `gemm_qo<T,D>`, `gemm_kv<T,D,K>`, `gemm_gate_up<T,D,F>`, `gemm_down<T,F,D>`, `rope_q<T,D,d,P>`, `rope_k<T,K,d,P>` (rope table `[T,P,3]`, `P` = pair count; body `rope_norm<d>(0)`), `transpose<T,d>`, `score_gemm<T,d>`, `causal_softmax<T>`, `context_gemm<T,d>`, `swiglu<T,F>`, `residual_add<T,D>`; GEA2 inventory comment (`:12–27`) rewritten; proba `gea2_*` rows (13) instantiate `T=8, D=960, K=320, F=2560, d=64, P=32` | same, gea2 rows | U4a | all 13 signatures + inventory comment carry no `8/960/320/2560/64/32` statue; `gea2` proba rows green | `faber test src/kernel.proba gea2` | No algorithm change; no score-scale change (scale stays a tensor input) | medium — rope pair-dim `P` and head-dim body literal are the one non-mechanical seam | **no** |
| **U4c** | GEA3-U3a decode family (16 entries, `kernel.fab:280–398`, `[1,·]` kept) to size params: `decode_rmsnorm<D>`, `decode_gemv_qo<D>`, `decode_gemv_kv<D,K>`, `decode_gemv_gate_up<D,F>`, `decode_gemv_down<F,D>`, `decode_mlp<D,F>`, `decode_rope_q<D,d,P>`, `decode_rope_k<K,d,P>`, `kv_append_k<K>`, `kv_append_v<K>`, `decode_key_transpose<C,d>`, `decode_score_gemm<d,C>`, `decode_masked_softmax<C>`, `decode_context_gemm<C,d>`, `decode_swiglu<F>`, `decode_residual_add<D>`; decode header + KV-geometry comment (`:243–277`) rewritten with capacity named `C`; proba `gea3u3a_*` rows (16) instantiate `D=960, K=320, F=2560, d=64, P=32, C=76` | same, gea3u3a rows | U4b | all 16 signatures + header comment carry no `960/320/2560/76/64` statue; `gea3u3a` proba rows green | `faber test src/kernel.proba gea3u3a` | No KV append semantics change; no mask semantics change | medium — C/L naming law meets mask extents; `76` appears in five signatures | **no** |
| **U4d** | GEA3-U3b prefill family (16 entries, `kernel.fab:434–551`) to size params — `T` is a size param (prompt extent is a fixture fact, `T_p=36` leaves the library): `prefill_rmsnorm<T,D>`, `prefill_gemm_qo<T,D>`, `prefill_gemm_kv<T,D,K>`, `prefill_gemm_gate_up<T,D,F>`, `prefill_gemm_down<T,F,D>`, `prefill_mlp<T,D,F>`, `prefill_rope_q<T,D,d,P>`, `prefill_rope_k<T,K,d,P>`, `prefill_key_transpose<T,d>`, `prefill_score_gemm<T,d>`, `prefill_causal_softmax<T>`, `prefill_context_gemm<T,d>`, `prefill_swiglu<T,F>`, `prefill_residual_add<T,D>`, `prefill_kv_write_k<C,T,K>`, `prefill_kv_write_v<C,T,K>`; prefill header comment (`:400–431`) rewritten; proba `gea3u3b_*` rows (16) instantiate `T=36, C=76, D=960, K=320, F=2560, d=64, P=32` | same, gea3u3b rows | U4c | all 16 signatures + header comment carry no `36/76/960/320/2560/64` statue; `gea3u3b` proba rows green | `faber test src/kernel.proba gea3u3b` | No prefill write idiom change (`history + block · rows` stays) | low-medium — largest slice but the most mechanical (U4b/c settled the seams) | **no** |
| **U4e** | GEA3-U3c head family (3 entries, `kernel.fab:580–599`) to size params: `head_rmsnorm<D>`, `lm_head_gemv<V,D>`, `embedding_gather<V,D>` (`V` = vocab, admission fact); head header comment (`:553–579`) rewritten; proba `gea3u3c` rows instantiate `V=49152, D=960` **and dedupe the duplicated rows** (`:631/:658`, `:640/:667`, `:649/:676` — each test exists twice on main); **file-level closeout oracle lands here**: `rg -n '960\|320\|2560\|49152\|\b76\b\|\b36\b' gradus/src/kernel.fab` → 0 hits | same, gea3u3c rows | U4d | three signatures + comment carry no `49152/960`; `gea3u3c` rows green exactly once each; file-level grep oracle clean (any surviving hit is reported, not papered over) | `faber test src/kernel.proba gea3u3c` | No tied-embedding layout change; no gather idiom change | low — 3 entries; the grep oracle may surface a stray comment the slice rewrites in place | **no** — pair-merge with U5 |

**Serialization is a write-surface constraint, not a data dependency** — the five slices share one file on one packet, so they run U4a→U4e in sequence; logically each family is independent (Mind may parallelize only by opening separate packets and owning their integration).

**Merge gate:** U4a–U4d are transitional non-integrable commits on the sgd packet (harness red is expected). **U4e + U5 is the single merge gate** — U5 rewires `gea3_pipeline_test.rs` (and hosts PGC fixtures if they read the live file) to instantiate the SmolLM2 tuple through the U3 `export_device_instance` API, after which the harness is green again and the merge lands atomically. U5's write scope stays exactly as §4 defines it.


## 5. Implementation work (Mind pointers)

Dispatch order after **admitted** audit:

1. **U1** then **U2** on packet `sgd` (writable radix; readable gradus, hosts, faber). Serial: shared generic/device maps.
2. **U3** may start after U1 if write_scope stays harness/export and not `radix-semantic` — default: **serialize U3 after U2** on the same radix packet to avoid two Hands in `radix-module`.
3. **U4a → U4b → U4c → U4d → U4e** serial on the sgd packet (§4b; one file, one packet — refresh membership to gradus+radix writable before U4a). Each slice lands as a transitional non-integrable commit; harness red between slices is expected. **U4e + U5** is the single merge gate (U5 follows §4 unchanged, starting on the packet as soon as U4a lands so it converges with U4e).
4. **U6** then **U7**.

Do not dispatch U4 while U1/U2 are red: generic `kernel.fab` would not be a device route.

## 6. Checkpoints and gates

**Batching:** several Hands + one merge gate. U4a–U4d land serially as non-integrable packet commits; **U4e + U5 is the atomic merge gate** (product GEA3 stays green only at that boundary).

**Hand sanity:** table above only. Never `./scripta/test --stage`, `./scripta/e2e`, `./scripta/parity`.

**Lane-owned after merge:** lint 1–2; test 3–4; parity smoke is **not** this goal’s closeout (SmolLM2 still runs via fixtures; smoke is observation at U5/U6 if a verification seat is filed later).

**Release:** defer-release.

## 7. Validation (goal closeout)

Goal.md §Validation. Delivery adds: spike2 green throughout; spike3 is the U2 oracle then remains a regression pin.

## 8. Companion skill plan

`$faber` for `.fab`. `$faberlang` + `$clean-break` for statue deletion. `$gpu-lessons` if a unit touches Metal emit.

## 9. Open questions

1. **spike3 still red on HEAD?** Default: U1/U2 assume yes (2026-08-26 proof). Check-first at dispatch. Decider: Hand U1.
2. **Export crate (U3).** Default: keep in `radix-mir` / a small leaf used by harness, not a new repo. Decider: U3 Hand if one crate is obvious; else Mind.
3. **Second model (U6).** Default: Qwen-class dims already in Gradus GGUF corpus if admitted; else a synthetic second fixture with different `H/d`. Decider: operator if a real GGUF is required for U6; synthetic fixture is enough to prove “no library edit.”
4. **Head-axis packet `6506c03`.** Do not merge as API. U4 deletes those signatures.
5. **Rope pair extent (U4b/c/d).** `P` (table rows `[T,P,3]`) is an independent size param because `d/2` is not assumed to be size arithmetic; `rope_norm<d>(0)` supplies the compile-time dimension. The intrinsic-generic-params delivery replaces the former CTO option (a) size-as-value admission with catalog generics and pre-AIR typed-HIR specialization. AIR remains literal-only after specialization; no `IndexParam` value admission or `ShapeSize` runtime carrier is used. Do not re-freeze `64/32`.
6. **Decode `T=1` stays literal.** The `1` in `[1,·]` is the decode-step contract, not model geometry (cut list is `D/H/kv/d/F/L_max/T_p`). Decider: Mind at U4 dispatch; head-axis batched `[5,…]` forms remain banned either way.
7. **`gea3u3c` proba rows are duplicated on main** (verified 2× each at `:631/:658`, `:640/:667`, `:649/:676`). U4e dedupes as part of its row rewrite; identical rows, no load-bearing difference.

---

*Template: `radix/docs/factory/TEMPLATE.md` + `$delivery`. Operator: immediate lowering 2026-09-03.*
