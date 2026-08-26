# Spike report — shape-generic `@ kernel` admission red (handle c8ff00be)

Date: 2026-08-26. Binary: `radix/target/debug/faber` (rebuilt-of-tree, 2026-08-26 01:15).
Reproducer env: `FABER_LIBRARY_HOME=/Users/ianzepp/work/faberlang`.

Manipulation: `@ kernel` annotated on `gradus/src/math.fab` `add<size M, size N>`
(one function). Reverted after capture; the probes in this directory pin the red.

## Which stage rejects, with the exact diagnostics

No stage rejects at parse or semantic check:

- `faber check` on the whole gradus package: **green** (annotation is silently
  accepted; the entry shows only `WARN003:unused_function`).
- `faber build` (fmir) on math.fab: **green**.

The reds appear at codegen / device lowerability, in three distinct shapes:

1. **Annotated, un-instantiated** (math.fab alone, metal-text):
   `error[CODEGEN001:mir_metal_text_unsupported]: metal-text requires at least
   one @ nucleum function`. A size-generic entry with no concrete caller
   produces no monomorphized MIR def, so no Kernel-role def exists. Silent at
   check — nothing names the orphaned annotation.
2. **Instantiated by a HOST caller via library import** (probe
   `spike3-host-caller.fab`, annotation restored): same diagnostic
   `metal-text requires at least one @ nucleum function`. The call type-checks
   and runs, but the imported monomorphized instance never registers as a
   kernel entry of the compiling unit — the Kernel role does not cross the
   import/library-link boundary into the target program.
3. **Instantiated by a KERNEL caller** (probe `spike1-kernel-caller.fab`):
   `MIR-to-Metal unsupported: kernel runtime call`. Source:
   `radix-mir/src/device/safe.rs` `SHAPE_KERNEL_RUNTIME_CALL` — kernel bodies
   may not call other functions; a concrete entry cannot wrap the generic
   library function.

## Control (green)

`spike2-local-generic.fab`: a size-generic `@ kernel` **defined in the same
unit** and monomorphized by a host caller emits concrete Metal — sizes baked
at the instantiation (`id >= 4` guard, value-return ABI with output buffer).
So the generic *signature* itself is admissible; GEA-style concreteness is a
discovery/linkage constraint, not a signature constraint.

## Missing contract facts (the ABI gap, named)

1. **Entry-discovery fact**: nothing defines when a monomorphized instance of
   a generic `@ kernel` becomes a kernel entry. Today discovery sees only
   same-unit monomorphized defs; an uninstantiated or imported instance is
   invisible (leg 1 and 2 above).
2. **Role-propagation fact**: the nucleum Kernel role does not travel across
   the library import / file-interface link, so a library-owned kernel can
   never be admitted from a consumer unit.
3. **Admission-diagnostic fact**: an annotated entry that yields zero kernels
   produces a generic "requires at least one @ nucleum function" error at
   codegen, not a named admission failure naming the orphaned annotation.

## Legs a size-generic admission would need (from the red's evidence)

- Monomorphization-to-entry linkage: a concrete instantiation of a generic
  `@ kernel` must register the instance def as a Kernel entry in the target
  program (removes red 1).
- Cross-unit role propagation: the Kernel role must survive the import /
  FHIR file-interface link (removes red 2) — or the ruling pins kernels as
  same-unit-only and forbids library-owned `@ kernel`.
- Call-free-body rule stays: generic entry bodies must lower to intrinsics /
  collection ops after monomorphization (red 3 is independent of genericity;
  every landed GEA entry is a single intrinsic body).
- A named admission diagnostic for annotated-but-unadmitted entries.

## Disposition

Annotation reverted from `gradus/src/math.fab` (a knowingly un-admittable
annotation in production source would break any future device emit of gradus
for no contract gain). The red is pinned by the three probes in this
directory instead; spike 3 requires re-annotating `add` to reproduce.
