# dense-prefill-smollm2 — REF-01-U1.9 SmolLM2 prefill-logit receipt

Consumer for the U1.8 dense forward graph against the pinned SmolLM2-360M
row on the **compiled rust** receipt tier. This README is the unit receipt.

**Verdict: STOP — not executed.** Resume at radix `b919052f0` (CODEGEN001
union-variant DefId registration, `d66e1f93e`) could not produce a packet
faber binary. The new diagnostic is recorded exactly and is not chased.
TARGETLANE001 was not weakened (`faber.toml` still `target = "fmir"`).

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
  fallback and was not chased: no packet faber exists at this revision.

## Command (from the Hand packet)

```text
cd /Users/ianzepp/work/faberlang/worktrees/hand-12/radix
cargo build -p faber
```

Intended follow-on (not reached):

```text
cd /Users/ianzepp/work/faberlang/worktrees/hand-12/gradus
env FABER_SUPPORT_PATH_OVERRIDE=/Users/ianzepp/work/faberlang \
  FABER_LIBRARY_HOME=/Users/ianzepp/work/faberlang/worktrees/hand-12 \
  /Users/ianzepp/work/faberlang/worktrees/hand-12/radix/target/debug/faber \
  build --target rust exempla/dense-prefill-smollm2
```

## Observed packet faber rebuild (2026-08-17 resume)

`cargo build -p faber` at readable radix `b919052f0` exits 101. Exact
diagnostic (captured twice; same text):

```text
error[E0432]: unresolved import `faber_hir_rust::ImportedEnumVariantInfo`
  --> crates/radix-program/src/rust_target.rs:17:76
   |
17 |     remap_function_param_info, remap_type_id_with_nominal_defs, FxHashMap, ImportedEnumVariantInfo,
   |                                                                            ^^^^^^^^^^^^^^^^^^^^^^^ no `ImportedEnumVariantInfo` in the root

error: could not compile `radix-program` (lib) due to 1 previous error
```

Recorded source facts (readable tree only; not patched):

- `d66e1f93e` uses `faber_hir_rust::ImportedEnumVariantInfo` in
  `crates/radix-program/src/rust_target.rs`.
- The type lives in `crates/radix-hir-rust/src/import_params.rs` and is
  re-exported from `radix-hir-rust`.
- `crates/radix-module/src/codegen/rust/mod.rs` re-exports
  `ImportedEnumVariantExport` and does **not** re-export
  `ImportedEnumVariantInfo`.
- `crates/faber-hir-rust/src/lib.rs` was not touched by `d66e1f93e` and
  does **not** re-export `ImportedEnumVariantInfo`.

The prior EXEC-02 non-exhaustive `MirCollectionOp` match-arm residual did
**not** reproduce at this revision. The prior CODEGEN001 (`tensor_view.fab`
definition id 4131 / 4200) was **not** re-exercised: no new faber binary
exists to emit rust. The stale packet binary (mtime 2026-08-17 19:39,
built at `7863624e2`) was not used.

No rust binary was printed. The GGUF file was not executed. No logits, no
observed token ids, no first-divergence field, no Metal/CUDA or
payload-residency claim.

## Revisions

| Surface | Revision |
| --- | --- |
| packet gradus | `57404ea` (`factory/hand-12`) |
| packet radix (readable) | `b919052f0` (includes `d66e1f93e`) |
| faber binary used | none — `cargo build -p faber` failed |
| workspace faber/hosts | not written |

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
Repair belongs to the radix rust-emit façade (`faber-hir-rust` /
`radix-module` re-export of `ImportedEnumVariantInfo` so `radix-program`
can build at `b919052f0`), not to this consumer. Radix is readable-only
in this packet; the import was not patched.
