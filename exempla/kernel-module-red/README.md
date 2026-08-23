# FAP-1 red 1 — `gradus:kernel` module absence (`@ nucleum` inventory)

Executable red for the faber-authorship-pilot blocked-item inventory
(delivery row FAP-1): **no `@ nucleum` kernel exists in any `gradus:`
module today.** The red imports the module the pilot will author
(`gradus:kernel`, flat leaf `gradus/src/kernel.fab`); the import must fail
today for exactly that reason.

## Command

```text
cd /Users/ianzepp/work/faberlang/gradus
env FABER_LIBRARY_HOME=/Users/ianzepp/work/faberlang \
  ../radix/target/debug/faber check exempla/kernel-module-red
```

## Expected decline (today)

```text
error[PKG001:unknown_library_module]: exempla/kernel-module-red/src/main.fab
compilation failed   (check exit 1)
```

Named reason: the `gradus:kernel` module does not exist — the inventory
fact, not a parser or crash. Verified against the in-workspace `faber`
binary and against the pinned wave-start commit `2eac3ce95`
(`2eac3ce95cecfb11e7ed7314e2b5cd6b2cb1abaa`, clean checkout) — same
diagnostic on both.

Turns green when FAP-2 lands `gradus/src/kernel.fab` and the import
resolves.
