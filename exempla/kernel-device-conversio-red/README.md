# FAP-1 red 2 — device `↦` rejects in kernel bodies

Executable red for the faber-authorship-pilot blocked-item inventory
(delivery row FAP-1): **device `↦` rejects.** A `@ kernel` body carrying a
conversio (`id ↦ f32`) is semantically admitted (`faber check` exits 0)
and must reject at Metal device admission today — there is no conversio
emission arm in `radix-mir-metal` until CTFP-4 lands.

## Commands

```text
cd /Users/ianzepp/work/faberlang/gradus
env FABER_LIBRARY_HOME=/Users/ianzepp/work/faberlang \
  ../radix/target/debug/faber check exempla/kernel-device-conversio-red   # ok (exit 0)
env FABER_LIBRARY_HOME=/Users/ianzepp/work/faberlang \
  ../radix/target/debug/faber emit exempla/kernel-device-conversio-red/src/main.fab -t metal-text
```

## Expected decline (today)

```text
error[CODEGEN001:mir_metal_text_unsupported]: exempla/kernel-device-conversio-red/src/main.fab: \
  code generation failed: MIR-to-Metal unsupported: kernel runtime call
compilation failed   (emit exit 1)
```

Named reason: the conversio lowers to a kernel runtime call with no device
arm — rejection at device admission, not a parse or check failure.
Verified against the in-workspace `faber` binary and against the pinned
wave-start commit `2eac3ce95`
(`2eac3ce95cecfb11e7ed7314e2b5cd6b2cb1abaa`, clean checkout) — same
diagnostic on both.

Turns green when CTFP-4 admits the first device `↦` emission arm (the
numeric-cast row over the device-safe subset).
