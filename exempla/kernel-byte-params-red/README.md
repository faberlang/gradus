# FAP-1 red 3 — byte kernel params reject

Executable red for the faber-authorship-pilot blocked-item inventory
(delivery row FAP-1): **byte params reject.** A `@ kernel` taking a scalar
`octeti<8>` param is semantically admitted (`faber check` exits 0) and
must reject at Metal device admission today.

## Commands

```text
cd /Users/ianzepp/work/faberlang/gradus
env FABER_LIBRARY_HOME=/Users/ianzepp/work/faberlang \
  ../radix/target/debug/faber check exempla/kernel-byte-params-red
env FABER_LIBRARY_HOME=/Users/ianzepp/work/faberlang \
  ../radix/target/debug/faber emit exempla/kernel-byte-params-red/src/main.fab -t metal-text
```

## Expected decline (today)

Package check rejects the byte param itself (exit 1, bare
`error[PKG001]` on `src/main.fab`); the file-mode Metal emit names the
device-admission reason:

```text
error[CODEGEN001:mir_metal_text_unsupported]: exempla/kernel-byte-params-red/src/main.fab: \
  code generation failed: MIR-to-Metal unsupported: device aggregate value type \
  BoundedOcteti { capacity: IndexId(5) }
compilation failed   (emit exit 1)
```

Named reason: `BoundedOcteti` resolves to a device aggregate value type
with no Metal kernel-param arm for the scalar byte shape — rejection at
device admission, not a parse or check failure.

State note (pinned honestly per the dispatch note): MLC-1 landed at radix
`3ff912b8c` after the FAP-1 delivery was written ("MLC-1 in flight"), so
this rejection is pinned against the pre-kernel-admission state: the
identical diagnostic is produced at the pinned wave-start commit
`2eac3ce95` (`2eac3ce95cecfb11e7ed7314e2b5cd6b2cb1abaa`, clean checkout,
which predates MLC-1) **and** on current main with MLC-1 landed — MLC-1
admitted the byte *DeviceView* kernel param, not the scalar byte-aggregate
param, so the row-wording red still holds today.

Turns green when the kernel byte-param shape the pilot's Q8_0 GEMV needs
(`octeti<N>` scalar-element/window rows, AEU-7 territory) is admitted.
