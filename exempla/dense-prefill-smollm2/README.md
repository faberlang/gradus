# dense-prefill-smollm2 — REF-01-U1.9 SmolLM2 prefill-logit receipt

Consumer for the U1.8 dense forward graph against the pinned SmolLM2-360M
row on the **compiled rust** receipt tier. This README is the unit receipt.

**Verdict: STOP — not executed.** Resume-2 at radix `3853d4b8f` produced a
packet `faber` binary. `faber build --target rust` reached the rust
runtime plan and stopped on a new diagnostic. TARGETLANE001 was not
weakened (`[build] target` is still `"fmir"`). Numerics were not tuned.
The GGUF file was not executed.

## Comparison policy (intended)

- gi0-numeric-contract v1.0.0: finite gate, top-1 exact over non-EOG `{0,2}`,
  top-5 overlap ≥4/5, first-divergence rule, window position 0 (prompt end).
- faber-prefill-oracle `compare_gpu_logits` / `PrefillReceipt` /
  `ExecutableRegime::Prefill` on the committed golden
  `radix/crates/faber-prefill-oracle/testdata/gi2-3-logits-golden/logits-pos0.json`
  (prompt tokens `[504, 2365, 6354, 16438, 27003, 690, 260, 23790, 2767]`,
  golden top-1 non-EOG `30`, golden top-5 `[30, 28, 1270, 365, 198]`).
- Engine: `faber build --target rust` then execute the printed binary.
  MIR stepper is not the receipt-tier engine. llvm-host is the documented
  fallback and was tried after the rust plan failed.

## Command (from the Hand packet)

```text
cd /Users/ianzepp/work/faberlang/worktrees/hand-12/radix
cargo build -p faber
```

`cargo build -p faber` at readable radix `3853d4b8f` exits 0
(Finished `dev` profile in 7.41s). Packet binary:
`/Users/ianzepp/work/faberlang/worktrees/hand-12/radix/target/debug/faber`
(`faber 1.7.0`, rustc 1.97.1 Homebrew). Prior E0432
(`faber_hir_rust::ImportedEnumVariantInfo`) did not reproduce.

Packet root is not a library home (`norma` is not a packet member). The
rust emit used the established symlink home:

```text
/tmp/faber-hand-12-libhome/gradus -> packet/gradus
/tmp/faber-hand-12-libhome/norma  -> /Users/ianzepp/work/faberlang/norma
```

```text
cd /Users/ianzepp/work/faberlang/worktrees/hand-12/gradus
env FABER_SUPPORT_PATH_OVERRIDE=/Users/ianzepp/work/faberlang \
  FABER_LIBRARY_HOME=/tmp/faber-hand-12-libhome \
  /Users/ianzepp/work/faberlang/worktrees/hand-12/radix/target/debug/faber \
  build --target rust exempla/dense-prefill-smollm2
```

## Observed rust runtime plan (2026-08-17 resume-2)

First attempt against `FABER_LIBRARY_HOME=<packet>` (no `norma`) failed
before the rust plan with compact:

```text
error[PKG001:unknown_library_provider]: exempla/dense-prefill-smollm2/src/main.fab:813
error[PKG001:unknown_library_provider]: exempla/dense-prefill-smollm2/src/main.fab:853
compilation failed
```

Those byte offsets are the `norma:processus` / `norma:solum` imports.
Retry used the symlink home above. `faber.toml` then needed rust host
selection (still `target = "fmir"`). Exact first rust-plan diagnostic:

```text
error[PKG001:package_host_selection_required]: /Users/ianzepp/work/faberlang/worktrees/hand-12/gradus/exempla/dense-prefill-smollm2/faber.toml
runtime plan failed
```

`[target.rust] host = "native"` was added (inferentia pattern). The next
diagnostic, compact identity only (coded PKG001 hides the message):

```text
error[PKG001:host_provider_selection_invalid]: /Users/ianzepp/work/faberlang/worktrees/hand-12/gradus/exempla/dense-prefill-smollm2/faber.toml
runtime plan failed
```

Grounded cause, not chased: with `host = native`, the rust planner
collects every `call '…'` in expanded library bodies. `norma:processus`
emits `processus:exi`. Live hosts manifest
`/Users/ianzepp/work/faberlang/hosts/crates/processus/src/manifest.json`
exports 10 processus routes and does **not** export `processus:exi`.
`load_provider_manifests` then sets `provider_error` (issue
`host_provider_route_missing`). Hosts is not a packet member. The
manifest was not patched.

Prior CODEGEN001 (`tensor_view.fab` definition id 4131 / 4200) was **not**
re-exercised: rust emit stopped at the runtime plan, before codegen.

Documented llvm-host fallback, same env:

```text
error[PKG001:llvm_emission_failed]: exempla/dense-prefill-smollm2/src/main.fab
llvm-host build failed
```

No rust binary was printed. The GGUF file was not executed. No logits, no
observed token ids, no first-divergence field, no Metal/CUDA or
payload-residency claim.

## Revisions

| Surface | Revision |
| --- | --- |
| packet gradus | `a0d78a5` base; this commit records the resume-2 stop |
| packet radix (readable) | `3853d4b8f` (includes `7f0c7de51` + `d66e1f93e`) |
| faber binary used | packet `target/debug/faber` 1.7.0 at `3853d4b8f` |
| workspace faber | `525d68bf8` (support-path override only; not written) |
| workspace hosts | `24687cda4` (solum/processus manifests; not written) |
| workspace norma | `7d71dafdb` (read via libhome; not written) |

## Model identity (not executed)

| Field | Pinned value |
| --- | --- |
| filename | `SmolLM2-360M-Instruct-Q4_K_M.gguf` |
| path | `/Users/ianzepp/ai/models/SmolLM2-360M-Instruct-Q4_K_M.gguf` |
| bytes | 270,590,880 |
| SHA-256 | `2fa3f013dcdd7b99f9b237717fa0b12d75bbb89984cc1274be1471a465bac9c2` |
| data offset | 1,787,040 |
| prompt | `The quick brown fox jumps over the lazy dog` |
| prompt tokens | `[504, 2365, 6354, 16438, 27003, 690, 260, 23790, 2767]` |

Hardware/OS for an executed run would have been CPU/reference on
`Darwin burgus.local 25.5.0 arm64` (`RELEASE_ARM64_T6050`). No run
occurred.

## Evidence boundary

This is a compiled-route **stop receipt**, not a prefill-logit pass.
Repair belongs to the hosts `processus` provider manifest (`processus:exi`
is in `norma/src/processus.fab` and absent from
`hosts/crates/processus/src/manifest.json`). That surface is outside this
packet. The rust host selection in `faber.toml` is the rust-receipt
wiring; it does not change the FMIR lane target.
