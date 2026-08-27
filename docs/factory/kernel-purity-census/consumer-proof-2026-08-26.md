# KPC consumer proof — three spike probes at the pinned tips (handle 2187bf87)

Date: 2026-08-26 (ET). Mode: packet `worktrees/kpc-proof`, branch `factory/kpc-proof` (gradus).
Authority: head-cto ruling `f489d2eb` (shape-generic default; Wave 2/3 gate = current consumer receipt), task `2187bf87`, campaign [`../CAMPAIGN.md`](../CAMPAIGN.md) Wave 2/3 gate.

## Binary identity

| Fact | Value |
| --- | --- |
| radix rev (read-only member, detached) | `416aa702e4562736cd3354d05423cf5f7f1b50a3` |
| gradus tip (writable member) | `47d3d6941899bd67dcc043987b476f721304dd4b` (= packet base, clean) |
| binary | `radix/target/debug/faber`, built 2026-08-26 22:30 ET via `cargo build -p faber` in the radix member |
| sha256 | `20391db97b9920618c161775cc4bf150216c19dd9081b0443a2b262d269faebd` |
| version | `faber 1.9.0` |
| env | `FABER_LIBRARY_HOME=/Users/ianzepp/work/faberlang/worktrees/kpc-proof` (packet-resident gradus at the pinned tip; identical commit to the main checkout) |

Protocol: `faber build -t metal-text <probe>.fab` from `gradus/scripta/spike-shape-generic-kernel/`, exactly as pinned by [`../../scripta/spike-shape-generic-kernel/REPORT.md`](../../scripta/spike-shape-generic-kernel/REPORT.md). The `@ kernel @ public` annotation on `math.add<size M, size N>` is landed at `47d3d69` (Wave 1), so the probes run as committed — the old report's "re-annotate to reproduce" note is stale.

## Verdict matrix

| Probe | Expected | Verdict | Exact first diagnostic |
| --- | --- | --- | --- |
| spike1-kernel-caller | RED (call-free device body) | **RED** — but the first red is **not** the composition rule (see §spike1) | `error[SEM010:expression_type_mismatch]` + `error[SEM010:return_type_mismatch]` at `spike1-kernel-caller.fab:12` |
| spike2-local-generic | GREEN (control) | **GREEN** | — emits `spike2-local-generic.metal`, exit 0 |
| spike3-host-caller | live question | **RED** — imported-instance entry discovery is unwired (see §spike3) | `error[CODEGEN001:mir_metal_text_unsupported]`: `code generation failed: MIR-to-Metal unsupported: metal-text requires at least one @ nucleum function` |

## spike2 — GREEN (control holds)

`faber build -t metal-text spike2-local-generic.fab` → exit 0, warnings only
(`WARN001:unused_variable`, `WARN003:unused_function`). Emitted Metal (391
bytes, sizes baked at the instantiation, value-return ABI with output buffer):

```metal
kernel void kadd(
    device const float* a_in [[buffer(0)]],
    device const float* b_in [[buffer(1)]],
    device float* output [[buffer(2)]],
    uint id [[thread_position_in_grid]]
) {
  if (id >= 4) { return; }
    output[id] = (a_in[id] + b_in[id]);
}
```

The size-generic `@ kernel` signature remains admissible with same-unit
monomorphization. Genericity of the signature is not in question anywhere
below.

## spike1 — RED, first red is the imported-generic typing gap, not the composition rule

Verbatim output (exit 1; `compilation failed`; no codegen stage reached):

```text
warning[LOCALE002]: spike1-kernel-caller.fab:7   | import from "gradus:math" math
warning[LOCALE002]: spike1-kernel-caller.fab:12  | return math.add(a, b)   (×2)
error[SEM010:expression_type_mismatch]: spike1-kernel-caller.fab:12
error[SEM010:return_type_mismatch]: spike1-kernel-caller.fab:12
warning[WARN003:unused_function]: spike1-kernel-caller.fab:11
```

The old-tip diagnostic `MIR-to-Metal unsupported: kernel runtime call`
(`SHAPE_KERNEL_RUNTIME_CALL`) no longer appears for this probe; the rejection
moved to semantic analysis. Classification evidence (temp controls in `/tmp`,
not committed, no tree changes):

- **Control E — host, annotated:** the identical imported call
  `const tensor<f32, [4, 8]> r ← math.add(a, b)` inside a plain host `fn main`
  reds with the same pair (`SEM010:expression_type_mismatch` +
  `SEM010:initializer_annotation_mismatch`). The mistyping is therefore
  **not device-context**: an imported size-generic call does not unify its
  result against a concrete annotated tensor type at the current consumer
  seam.
- **Control F — explicit type args:** `math.add<4, 8>(a, b)` adds
  `SEM011:dynamic_receiver_method_type_args` — the imported binding is typed
  through the dynamic/ignotum callee route, so explicit instantiation is
  rejected too. spike3's own output carries
  `warning[WARN010:explicit_ignotum_annotation]` on the unannotated binding:
  the imported generic call result types **ignotum** in the consumer.
- **Controls A/C — local callee in a kernel body (concrete, then
  size-generic):** both **pass typecheck** (the local generic instantiates
  fine — genericity is not the trigger) and red at codegen with the named
  composition rule:
  `error[CODEGEN001:nucleum_fragment_context]: code generation failed: @ nucleum cannot call a host function or other non-device-safe callable`.

Conclusion: spike1 is RED as expected, and the call-free device-body rule is
live and genericity-independent — but the **first** red at this tip is the
imported-generic ignotum typing clashing with the kernel's annotated concrete
return. The composition rule would reject this wrapper afterwards regardless
(same body shape as controls A/C). Nothing here licenses relaxing composition
safety, and nothing here is a generic-signature failure.

## spike3 — RED: link-level classification = entry discovery (consumer instantiation wiring)

Verbatim output (exit 1):

```text
warning[LOCALE002]: spike3-host-caller.fab:9   | import from "gradus:math" math
warning[LOCALE002]: spike3-host-caller.fab:15  | const _ r ← math.add(a, b)  (×2)
warning[WARN010:explicit_ignotum_annotation]: spike3-host-caller.fab:15
warning[WARN001:unused_variable]: spike3-host-caller.fab:15
warning[WARN003:unused_function]: spike3-host-caller.fab:11
error[CODEGEN001:mir_metal_text_unsupported]: spike3-host-caller.fab: code generation failed: MIR-to-Metal unsupported: metal-text requires at least one @ nucleum function
compilation failed
```

Per the CTO decision matrix, the three links:

1. **Role propagation — landed at the interface, not the failing link.**
   `InterfaceDeviceContract` carries role/visibility/body per export across
   the import (radix `5482bc5ac`, DFV2-3;
   `radix-module/src/program/compile_test.rs::
   import_contract_carries_imported_device_role_and_body_channel`), and the
   consumer lowering context collects per-import `ImportedDeviceRoute`s
   (`radix-module/src/mir/lower/context.rs:769-778`) — the code comment
   explicitly names "the spike-3 shape" as kept.
2. **Body transport — landed at the interface/artifact level, unreached.**
   The Source/Canonical/Missing channel exists (DFV2-3/5); no consumer pass
   on this route ever reaches a body-consumption step, so body cannot be the
   failing link.
3. **Entry discovery — THE failing link.** Two dead ends at `416aa702e`:
   - `LoweringContext::imported_device_routes` is written
     (`context.rs:774`) and **never read** anywhere in production code; the
     "concrete composition pass" its comment names does not exist on any
     production route.
   - `instantiate_merged_generic_calls_with_devices` (registration +
     composition of imported device instances, `package_instantiate.rs:198`)
     has **no production caller**; the production path calls the empty-index
     wrapper `instantiate_merged_generic_calls`
     (`radix-program/src/mir/lower.rs:1840`), so `ImportedDeviceRegistration`
     is never produced in a real compile.
   - Upstream of both, the consumer typechecker types the imported generic
     call **ignotum** (WARN010/SEM010/SEM011 above), so no concrete
     instantiation of `math.add<f32, [2, 2]>` is ever recorded in the
     consumer — matching `context.rs`'s "the identity table records concrete
     instantiations only" with generics left on the provider route. Zero
     concrete instances ⇒ zero Kernel-role defs ⇒ the metal-text zero-kernel
     error.

This is a **Radix linkage/admission defect finding** (consumer-side entry
discovery and imported-instance wiring), consistent with the DFV2 ledger:
DFV2-1..5 landed, DFV2-6/7 pending, and the goal status line already records
"consumer-local kernel callers wait on radix-program route wiring". It is
**not** a license to specialize per geometry.

## Gate conclusion (per CTO decision matrix f489d2eb)

- spike2 GREEN ✓ (control holds), spike1 RED ✓ (expected; composition rule
  live), spike3 **RED** ✗.
- **Wave 2/3 gate stays CLOSED.** The preferred technical path per the
  operator decision frame is Radix spend on entry discovery / imported
  instance wiring (the DFV2-6/7 continuation surface above); the typed
  generic source contract stays. No per-geometry specialization is authorized
  by any current ruling; if the operator wants the temporary fallback, that
  requires an explicit operator ruling naming the geometries and a re-entry
  condition.
- Two radix findings to route (no gradus action):
  1. `KPC`-linked: consumer entry discovery for imported generic device
     instances (dead `imported_device_routes`, unwired
     `instantiate_merged_generic_calls_with_devices`, ignotum-typed imported
     generic calls).
  2. Imported-generic expected-type unification: an annotated concrete
     expected type against an imported size-generic call reds SEM010 even in
     host context (control E) — this is what moved spike1's red from the old
     MIR-level `SHAPE_KERNEL_RUNTIME_CALL` to semantic analysis.

## Residual observations (out of scope, disclosed)

- `faber check .` and `faber build --package` at this tip parse the gradus
  `en` sources through a non-`en` reader surface (LOCALE002 on every keyword,
  `PARSE018/PARSE030/PARSE060` cascade on `src/math.fab`,
  `src/transformer.fab`, …) while file-mode `faber build` parses the same
  files green. Not probed further; not touched (radix is read-only here and
  the probe protocol is file-mode).
- `REPORT.md`'s "spike 3 requires re-annotating `add`" note is stale (the
  annotation is landed at `47d3d69`); left as-is per scope-exact rules.
- Probe artifacts: the emitted `spike2-local-generic.metal` was captured
  above and removed from the tree; control files A–F lived in `/tmp` only.
