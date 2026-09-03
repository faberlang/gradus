# DELIVERY: shape-generic-device-route — clean-break library geometry

**Status**: active — U1 done; U2-R1 packet `e1bef1b00`; U3 on main `aa27a9a21`; U4+U5 not dispatched
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
| **U4** | Clean-break `gradus/src/kernel.fab` (+ `kernel.proba`): every public `@ kernel` uses `size` params; delete statue signatures (including U4 batched `[5,76,64]` forms). SmolLM2 numbers **not** in this file | `gradus/src/kernel.fab`, `gradus/src/kernel.proba` | U1, U2 | `faber check` on kernel.fab green; no model-geometry integer in public kernel **signatures** (`rg` oracle named in U7); proba instantiates sizes | packet `faber check` / focused proba rows that instantiate | No prefill/decode algorithm change; no new glyphs | **no** — merge with U5 (fixtures must instantiate) |
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


## 5. Implementation work (Mind pointers)

Dispatch order after **admitted** audit:

1. **U1** then **U2** on packet `sgd` (writable radix; readable gradus, hosts, faber). Serial: shared generic/device maps.
2. **U3** may start after U1 if write_scope stays harness/export and not `radix-semantic` — default: **serialize U3 after U2** on the same radix packet to avoid two Hands in `radix-module`.
3. **U4+U5** one merge gate; packet needs **gradus+radix** writable. Refresh membership before U4.
4. **U6** then **U7**.

Do not dispatch U4 while U1/U2 are red: generic `kernel.fab` would not be a device route.

## 6. Checkpoints and gates

**Batching:** several Hands + merge gates (U4+U5 atomic for product GEA3).

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

---

*Template: `radix/docs/factory/TEMPLATE.md` + `$delivery`. Operator: immediate lowering 2026-09-03.*
