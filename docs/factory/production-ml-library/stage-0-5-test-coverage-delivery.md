# Gradus — Stage 0.5 Delivery Spec
## Full co-located proba coverage and executed-proba gate

**Status**: delivery — READY for delivery audit
**Date**: 2026-08-16
**Operator source**: memo `805fb2c4`, task `c0d0dc26`
**Repository**: `/Users/ianzepp/work/faberlang/gradus`
**Scope**: Gradus test-coverage scoping only. The existing 32-file proba
corpus is an asset to make run. Only `src/data.proba` is new authoring.
**Boundary**: Radix/Faber defects are named as owning-repository prerequisite
units below. This Gradus delivery does not implement them.

## 1. Interpreted theme

Stage 0.5 establishes a truthful executed-proba contract for the live Gradus
library. The live tree has 33 source modules, 32 already have co-located
English-locale `.proba` files, and one module is uncovered. The work is not a
rewrite of the current corpus. The current files contain the intended oracle
rows and edge cases; the delivery makes those rows executable through the
package-aware MIR proba path and adds only the missing `data` discovery probe.

The stage has three boundaries:

1. Route the shared Radix/Faber runner defects before executed coverage may
   close.
2. Add the one missing co-located probe for the live `gradus:data` module.
3. Run every existing and new probe and record one executed-proba result row
   per source module.

The gate must distinguish source discovery, structural `faber check`, and
actual `faber test` execution. A proba file that parses or type-checks is not
an executed-proba result.

### Non-goals

- No edits to the 33 existing `src/**/*.fab` implementation modules.
- No rewrite, weakening, deletion, or omission of the existing 32 proba
  suites to accommodate the runner.
- No replacement of receiver-method assertions with count-only or structural
  assertions.
- No Gradus workaround for a Radix/Faber failure.
- No GPU, target-equivalence, performance, clean-install, or model-execution
  claim.
- No new `data` API: `src/data.fab` is a documented stub with no public
  behavior to invent.

## 2. Live baseline and triage verdict

### 2.1 Coverage census

The census was taken from the live tree, not from the stale module-map prose:

```bash
cd /Users/ianzepp/work/faberlang/gradus
find src -type f -name '*.fab' | sort | wc -l       # 33
find src -type f -name '*.proba' | sort | wc -l    # 32
find src -type f -name '*.fab' -print | while read f; do
  test -f "${f%.fab}.proba" || echo "GAP: ${f%.fab}.proba"
done                                                        # src/data.proba
```

| Family | Live modules | Proba baseline | Gap / disposition |
| --- | --- | ---: | --- |
| Foundation + shared contracts | `dtype`, `shape`, `tensor`, `math`, `parameter`, `serialize` | 6/6 | Existing suites are assets. |
| Autograd, training, and data | `gradient`, `loss`, `optimize`, `nn`, `attention`, `transformer`, `train`, `metrics`, `data` | 8/9 | `data` is the one missing probe. |
| Model admission and storage | `model/artifact`, `model/capsule`, `model/safetensors`, `model/gguf`, `model/gguf_manifest`, `model/dequant`, `model/tensor_payload`, `model/tensor_view` | 8/8 | Existing suites are assets. |
| Dense/reference model families | `model/dense_llama`, `model/dense_qwen2`, `model/dense`, `model/qwen35moe` | 4/4 | Existing suites are assets. |
| Tokenizer, inference, and facade | `tokenizer`, `cache`, `decode`, `sampling`, `generation`, `gradus` | 6/6 | Existing suites are assets. |
| **Total** | **33** | **32/33** | **One gap: `src/data.proba`.** |

`src/data.fab` is a live English-locale stub. Its header declares future
batching, shuffling, and tokenization concerns, but it currently exports no
public data behavior. The gap-fill is therefore a module-discovery smoke, not
an invented batching or tokenization contract.

The current existing-suite case counts are useful as an asset census, not as
proof of execution:

| Module | Current proba cases | Module | Current proba cases |
| --- | ---: | --- | ---: |
| `attention` | 56 | `cache` | 13 |
| `decode` | 38 | `dtype` | 19 |
| `generation` | 17 | `gradient` | 10 |
| `gradus` | 9 | `loss` | 26 |
| `math` | 43 | `metrics` | 21 |
| `model/artifact` | 2 | `model/capsule` | 40 |
| `model/dense_llama` | 7 | `model/dense_qwen2` | 5 |
| `model/dense` | 8 | `model/dequant` | 17 |
| `model/gguf_manifest` | 19 | `model/gguf` | 51 |
| `model/qwen35moe` | 22 | `model/safetensors` | 37 |
| `model/tensor_payload` | 1 | `model/tensor_view` | 16 |
| `nn` | 39 | `optimize` | 32 |
| `parameter` | 29 | `sampling` | 31 |
| `serialize` | 47 | `shape` | 22 |
| `tensor` | 9 | `tokenizer` | 92 |
| `train` | 53 | `transformer` | 17 |

The current files use the English reader surface (`test`, `assert`, `import
from`, `const`) and are already committed post-conversion. This is why the
coverage work does not reopen locale conversion.

### 2.2 Existing proba runtime failure

Structural checking of the representative asset is green:

```bash
cd /Users/ianzepp/work/faberlang/gradus
FABER_LIBRARY_HOME=/Users/ianzepp/work/faberlang \
  ../radix/target/debug/faber check src/math.proba
# ok: src/math.proba
```

The same current workspace-built debug binary reaches the MIR runner when a
single proba source is supplied:

```bash
FABER_LIBRARY_HOME=/Users/ianzepp/work/faberlang \
  ../radix/target/debug/faber test src/math.proba
# exit 1
# 21 x: unsupported MIR lowering: method call before runtime/provider MIR lowering
```

This is not evidence that `src/math.proba` is stale or that `src/math.fab`
disappeared. It is a shared runner failure in the method-call lowering path.
The live Radix implementation establishes the boundary:

- `radix/crates/faber/src/commands/test.rs:103-161` sends a single `.fab` or
  `.proba` file through `run_proba_source`; package inputs use
  `analyze_package_for_tests` and `run_proba_on_analyzed` instead.
- `radix/crates/radix/src/mir/lower/runtime.rs:62-150` owns
  `FunctionBuilder::lower_method_call`. It tries genus-method targets,
  provider calls, built-in receiver families, and registered collection
  methods. When no supported route remains, it emits the exact diagnostic at
  lines 146–150.
- `radix/crates/radix-package/src/mir/link.rs:425-430` owns the interpreted
  package route that links library method targets. Its
  `LibraryMethodCallRewriter` at lines 2331–2400 rewrites a method on a linked
  library nominal into a typed synthetic definition call before MIR lowering.

The Gradus assertions exercise methods on the library genus
`tensor.Tensor` (`r.accipe`, `r.valet`, `r.figura`, `r.typus`) and methods on
values returned from those calls. The direct single-file command does not have
the package linker context, so the receiver falls through to the shared
fail-closed MIR diagnostic. This is a Radix package/MIR-runner surface, not a
Gradus implementation defect and not a reason to remove receiver-method
coverage.

There is a separate package-input sibling:

```bash
cd /Users/ianzepp/work/faberlang/gradus
FABER_LIBRARY_HOME=/Users/ianzepp/work/faberlang \
  ../radix/target/debug/faber test .
# error: cannot read '.' (os error 2)
# error: package analysis failed
```

That is a Faber/Radix package-path normalization defect before test analysis.
It is not the same failure as the method-call MIR diagnostic. A manifest-backed
package path from the workspace reaches package analysis, where the current
debug binary also emits pre-MIR semantic diagnostics (`SEM005`, `SEM001`,
`SEM006`, `SEM004`, `SEM010`, and `SEM011`). Those diagnostics are recorded as
package-analysis noise until the owning route is re-run against the repaired
package path; they are not folded into the method-call root cause or used to
justify changing Gradus assertions.

The sibling diagnostic `projection base that does not resolve to a local value`
is not emitted by the current Gradus single-file reproduction. It remains a
separate aggregate-place MIR surface and is not admitted as a Gradus
prerequisite without a reproduction. Likewise, device/WGSL runtime-call
rejection is unrelated to this CPU MIR proba runner failure.

**Triage verdict:** the executed-proba tier is open. The shared prerequisite is
an owning-Radix package/MIR-runner route for library-genus receiver methods,
with the package-dot path normalized as a separate sibling. The Gradus corpus
is structurally valid and should remain intact.

### 2.3 Named owning-repository prerequisites

These are specifications for dispatch in `radix`, not writes in this Gradus
checkout. Both are prerequisites to the final Gradus gate; the method-call
route is the shared implementation unit that unblocks the other repositories'
proba suites as well.

#### `rdx-s05-1` — normalize the package-test path

- **repo**: `radix`
- **outcome**: `faber test .`, a relative manifest-backed package path, and the
  equivalent absolute package path enter the same package discovery and test
  analysis route. Single-file `.fab`/`.proba` behavior stays distinct.
- **write_scope**: `radix/crates/faber/src/commands/test.rs`, the owning path
  normalization seam under `radix/crates/radix-package/src/`, and focused
  package/test regression fixtures.
- **done_when**: from the Gradus root, `faber test .` no longer emits
  `cannot read '.'`; the relative and absolute Gradus package paths both reach
  `analyze_package_for_tests`; the regression does not change the proba source
  grammar or turn a directory without a manifest into a legacy `main.fab`
  package.
- **depends_on**: none.
- **non_goals**: Gradus proba edits, method-call lowering, or generic fallback
  for unsupported methods.
- **risk**: medium — package path normalization is a CLI/package boundary.
- **integrable**: yes.

#### `rdx-s05-2` — execute imported Gradus genus methods through package MIR

- **repo**: `radix`
- **outcome**: the interpreted package test path lowers and runs a minimal
  Gradus-style probe that imports `gradus:tensor`, constructs a
  `tensor.Tensor`, calls receiver methods, reads a field-backed collection,
  and asserts the result. The method path is typed and fail-closed.
- **write_scope**: `radix/crates/radix-package/src/mir/link.rs` (library method
  target registration/rewrite and focused package-MIR tests),
  `radix/crates/radix/src/mir/lower/runtime.rs` only if the diagnosis proves a
  lowerer-side gap after linking, and focused proba/MIR regression fixtures.
- **done_when**: the minimal package fixture and the Gradus representative
  suite reach the MIR runner with no `unsupported MIR lowering: method call
  before runtime/provider MIR lowering`; method calls are lowered as typed
  linked definitions or an explicitly supported intrinsic, never as an
  untyped generic runtime call. The regression remains fail-closed for an
  unregistered method.
- **depends_on**: `rdx-s05-1` for the end-to-end package proof; the focused
  linker/lowerer regression may be developed independently.
- **non_goals**: arbitrary dynamic dispatch, silent CPU fallback, device
  lowering, Rust/Cargo execution, or changing Gradus method semantics.
- **risk**: high — this is shared executed-proba infrastructure across all
  library repos.
- **integrable**: yes.

## 3. Proba framework contract

### 3.1 Grammar grounded in Radix source

The authoritative public grammar in `faber/docs/EBNF.md` defines:

- `probandum` suites containing nested suites, setup/teardown blocks, and
  `proba` cases (`EBNF.md:952-962`);
- `proba STRING probaModifier* blockStmt`, with modifiers including `omitte`,
  `futurum`, `tag`, `metior`, `repete`, and `fragilis`;
- `adfirma expression (secus expression)?` (`EBNF.md:557-573`), a fatal
  runtime invariant assertion isolated by the test harness;
- `fac { ... } cape err { ... }` for a local handler when a probe needs to
  catch a failable call (`EBNF.md:1042-1050`).

The live parser implements the same contract:

- `radix/crates/radix-parser/src/decl.rs:1439-1545` parses `probandum`,
  nested cases, setup/teardown, `proba`, and test modifiers;
- `radix/crates/radix-parser/src/stmt.rs:546-560` parses `adfirma` and its
  optional `secus` message;
- `radix/crates/radix-syntax/src/ast.rs:534-584, 830-833` preserves suite,
  case, modifier, and assertion nodes for HIR/MIR processing.

The English reader maps the canonical forms to the post-conversion Gradus
surface: `describe`/`test`/`assert`, `setup`/`teardown`, `const`, and
`import from`. The mapping is live in
`radix/stdlib/locale/en/pack.toml` (`adfirma = "assert"`, `verum = "true"`,
`falsum = "false"`). The freshest maintained examples used for authoring
shape are `radix/corpus/proba/proba.fab`,
`radix/corpus/probandum/probandum.fab`, and the en-surface co-located examples
under `norma/exempla/caelum/`. Gradus's current `src/math.proba` is the local
post-conversion precedent for imports, helper functions, `fac`/`cape`, and
receiver assertions.

A proba may import a product `.fab` module, but it must not import another
`.proba` file. The new `data` smoke must use the current English reader and
must not introduce a helper API in `src/data.fab`.

### 3.2 Authoring contract for the one gap

`gds-s05-c01` may use this shape:

```fab
+++
locale = "en"
+++

import from "gradus:data" data

test "data module is discoverable" {
    assert true
}
```

The import is the meaningful operation: it proves the live module is
package-discoverable. The assertion is an explicit discovery smoke because
`data.fab` has no public behavior. The case must be labeled in the scorecard
as `discovery-only`; it must not promote batching, shuffling, tokenization, or
any future data contract.

## 4. Normalized Stage-0.5 outcome

> The live 33-module Gradus tree has one sibling `.proba` for every `.fab`
> module, all 33 suites are authored in the current English surface, the 32
> existing suites remain unchanged assets, the `data` discovery smoke is
> added, and the package-aware MIR runner reports a passing executed-proba
> result for every module. The scorecard records the actual per-module tier and
> keeps the stage open on any missing, semantic, lowering, or runner failure.

Structural `faber check` and proba-pinned oracle rows remain distinct from the
executed tier. No module becomes `executed-proba` because its file exists or
because its source checks.

## 5. Gradus unit graph

The three Gradus units are intentionally small. Existing module families are
execution batches over committed assets, not 32 new authoring tasks.

### `gds-s05-0` — triage receipt and Radix routing

- **outcome**: durable Gradus triage receipt records the 32/33 census, the
  `src/data.fab` gap, the exact single-file MIR diagnostic, the separate
  package-dot path defect, the grounded grammar, and the two owning Radix
  prerequisite units.
- **write_scope**: `gradus/docs/factory/production-ml-library/stage-0-5-triage.md`.
- **done_when**: the receipt names the reproduction commands and outputs in
  §2, states that the existing 32 suites are assets, states that execution is
  open until `rdx-s05-1` and `rdx-s05-2` land, and contains no Radix or Gradus
  product implementation.
- **depends_on**: none.
- **sanity**: compare the receipt's source/proba set against the census in
  §2.1; `git diff --check`.
- **non_goals**: editing `src/**/*.fab`, editing existing `.proba` files,
  implementing the gate, or changing Radix.
- **risk**: low — evidence and routing only.
- **integrable**: yes.

### `gds-s05-c01` — fill the `data` module gap

- **outcome**: add the one English-locale co-located discovery smoke for
  `gradus:data`; do not invent a data API.
- **write_scope**: `gradus/src/data.proba` only.
- **read_scope**: `gradus/src/data.fab`, `gradus/docs/module-map.md`,
  `radix/stdlib/locale/en/pack.toml`, and the current proba examples named in
  §3.
- **done_when**: `src/data.proba` imports `gradus:data`, uses the current
  `test`/`assert` English surface, is discovered beside `src/data.fab`, and
  its discovery-only case passes through the same package-aware runner used by
  the aggregate gate. The scorecard labels it `discovery-only` and does not
  claim future batching/tokenization behavior.
- **depends_on**: `gds-s05-0`, `rdx-s05-1`, `rdx-s05-2`.
- **sanity**: `faber check src/data.proba` and the gate's filtered `data`
  invocation after the Radix prerequisites land.
- **non_goals**: edits to `src/data.fab`, implementation of batching,
  shuffling, tokenization, fixtures, or changes to any existing proba.
- **risk**: low — the module has no public behavior; the main risk is falsely
  promoting a discovery smoke.
- **integrable**: yes.

### `gds-s05-gate` — executed-proba coverage gate and scorecard

- **outcome**: add a fail-closed Gradus gate that discovers all 33 source/
  proba pairs, runs the existing 32 suites plus `data.proba` through the
  package-aware MIR runner, and records one actual executed-proba row per
  module.
- **write_scope**: `gradus/scripta/check-proba-coverage`,
  `gradus/docs/factory/production-ml-library/proba-coverage-scorecard.json`,
  and the executed-tier wording/receipt section of
  `gradus/docs/regression-corpus.md`.
- **depends_on**: `gds-s05-c01`, `rdx-s05-1`, and `rdx-s05-2`.
- **done_when**:
  1. The gate derives exactly 33 live modules from `find src -name '*.fab'`.
  2. It requires exactly one sibling `.proba` for each module and rejects a
     missing probe, an orphan probe, or a duplicate module row.
  3. It uses the package-aware `faber test` route with an absolute manifest
     path (and records the public `faber test .` route as a prerequisite until
     `rdx-s05-1` closes it); direct single-file execution is not accepted as a
     substitute for imported-library method coverage.
  4. It records the command, binary identity, module path, proba path, case
     count, pass/fail/skip counts, first failure text, and evidence tier for
     every row.
  5. A row is `executed-proba` only when every selected case in that module
     passes. Structural `faber check`, a parsed file, an oracle comment, or a
     count-only row cannot produce that tier.
  6. The scorecard has five family batches and 33 per-module rows. The
     `data` row is explicitly `discovery-only`; the other 32 rows retain their
     existing oracle descriptions from `docs/regression-corpus.md`.
  7. The gate exits non-zero for any unresolved Radix prerequisite, package
     analysis error, MIR lowering error, failed case, skipped case presented as
     a pass, missing row, or stale source/proba inventory.
  8. A closeout run reports **33/33 modules at `executed-proba`** before the
     Stage-0.5 gate is marked complete.
- **sanity**: `./scripta/check-proba-coverage`; `./scripta/check-source`;
  `./scripta/check-compile`; `git diff --check`.
- **read_scope**: `src/**/*.fab`, `src/**/*.proba`, `docs/module-map.md`,
  `docs/regression-corpus.md`, `faber.toml`, the Faber test command contract,
  and the Radix prerequisite receipts.
- **non_goals**: changing source semantics, changing existing proba oracles,
  replacing package MIR with Rust/Cargo execution, target/device gates, or
  editing the capability ledger to claim support.
- **risk**: high — this is the evidence authority and must fail honestly.
- **integrable**: yes, after the prerequisite routes and `gds-s05-c01` land.

## 6. Module-family execution batches

These are gate batches, not new authoring work. They preserve the existing
corpus as the asset and make the gate report failures by behavior family.

| Batch | Modules | Execution intent |
| --- | --- | --- |
| `gds-s05-f01` foundation/contracts | `dtype`, `shape`, `tensor`, `math`, `parameter`, `serialize` | Run existing typed construction, shape, arithmetic, identity, and wire rows. Receiver-method failures remain runner findings. |
| `gds-s05-f02` autograd/training/data | `gradient`, `loss`, `optimize`, `nn`, `attention`, `transformer`, `train`, `metrics`, `data` | Run existing training/inference math rows plus the new `data` discovery smoke. No new ML semantics. |
| `gds-s05-f03` model admission/storage | `model/artifact`, `model/capsule`, `model/safetensors`, `model/gguf`, `model/gguf_manifest`, `model/dequant`, `model/tensor_payload`, `model/tensor_view` | Run existing format, range, payload, view, and dequant rows. No model-file or device claim. |
| `gds-s05-f04` dense/reference | `model/dense_llama`, `model/dense_qwen2`, `model/dense`, `model/qwen35moe` | Run existing architecture descriptor and dense-reference rows. No new adapter authoring. |
| `gds-s05-f05` tokenizer/inference/facade | `tokenizer`, `cache`, `decode`, `sampling`, `generation`, `gradus` | Run existing tokenizer identity, cache, decode, sampling, generation, and facade rows. |

## 7. Per-module executed-proba gate rows

The gate must materialize these rows from the live tree and update the
scorecard from the run. The `baseline` column describes the current state
before Stage 0.5; it is not an execution claim.

| Module | Family | Proba path | Cases | Baseline | Green row |
| --- | --- | --- | ---: | --- | --- |
| `attention` | f02 | `src/attention.proba` | 56 | present / structural | `executed-proba` |
| `cache` | f05 | `src/cache.proba` | 13 | present / structural | `executed-proba` |
| `data` | f02 | `src/data.proba` | new | missing | `executed-proba` / discovery-only |
| `decode` | f05 | `src/decode.proba` | 38 | present / structural | `executed-proba` |
| `dtype` | f01 | `src/dtype.proba` | 19 | present / structural | `executed-proba` |
| `generation` | f05 | `src/generation.proba` | 17 | present / structural | `executed-proba` |
| `gradient` | f02 | `src/gradient.proba` | 10 | present / structural | `executed-proba` |
| `gradus` | f05 | `src/gradus.proba` | 9 | present / structural | `executed-proba` |
| `loss` | f02 | `src/loss.proba` | 26 | present / structural | `executed-proba` |
| `math` | f01 | `src/math.proba` | 43 | present / structural | `executed-proba` |
| `metrics` | f02 | `src/metrics.proba` | 21 | present / structural | `executed-proba` |
| `model/artifact` | f03 | `src/model/artifact.proba` | 2 | present / structural | `executed-proba` |
| `model/capsule` | f03 | `src/model/capsule.proba` | 40 | present / structural | `executed-proba` |
| `model/dense` | f04 | `src/model/dense.proba` | 8 | present / structural | `executed-proba` |
| `model/dense_llama` | f04 | `src/model/dense_llama.proba` | 7 | present / structural | `executed-proba` |
| `model/dense_qwen2` | f04 | `src/model/dense_qwen2.proba` | 5 | present / structural | `executed-proba` |
| `model/dequant` | f03 | `src/model/dequant.proba` | 17 | present / structural | `executed-proba` |
| `model/gguf` | f03 | `src/model/gguf.proba` | 51 | present / structural | `executed-proba` |
| `model/gguf_manifest` | f03 | `src/model/gguf_manifest.proba` | 19 | present / structural | `executed-proba` |
| `model/qwen35moe` | f04 | `src/model/qwen35moe.proba` | 22 | present / structural | `executed-proba` |
| `model/safetensors` | f03 | `src/model/safetensors.proba` | 37 | present / structural | `executed-proba` |
| `model/tensor_payload` | f03 | `src/model/tensor_payload.proba` | 1 | present / structural | `executed-proba` |
| `model/tensor_view` | f03 | `src/model/tensor_view.proba` | 16 | present / structural | `executed-proba` |
| `nn` | f02 | `src/nn.proba` | 39 | present / structural | `executed-proba` |
| `optimize` | f02 | `src/optimize.proba` | 32 | present / structural | `executed-proba` |
| `parameter` | f01 | `src/parameter.proba` | 29 | present / structural | `executed-proba` |
| `sampling` | f05 | `src/sampling.proba` | 31 | present / structural | `executed-proba` |
| `serialize` | f01 | `src/serialize.proba` | 47 | present / structural | `executed-proba` |
| `shape` | f01 | `src/shape.proba` | 22 | present / structural | `executed-proba` |
| `tensor` | f01 | `src/tensor.proba` | 9 | present / structural | `executed-proba` |
| `tokenizer` | f05 | `src/tokenizer.proba` | 92 | present / structural | `executed-proba` |
| `train` | f02 | `src/train.proba` | 53 | present / structural | `executed-proba` |
| `transformer` | f02 | `src/transformer.proba` | 17 | present / structural | `executed-proba` |

The scorecard must preserve the distinction between `present / structural`,
`discovery-only`, and `executed-proba`. It must not turn the current README or
regression-corpus structural claims into executed claims until the gate has a
33/33 pass receipt.

## 8. Integration and validation ownership

The two Radix prerequisite units land in `radix` under the owning-repository
boundary. Gradus has no product merge gate for the 32 existing assets plus one
new probe; the gate is the sole aggregate writer for the coverage scorecard.
The gate runs after `gds-s05-c01`, `rdx-s05-1`, and `rdx-s05-2`.

Lane-owned validation, named once:

```bash
cd /Users/ianzepp/work/faberlang/gradus
./scripta/check-proba-coverage
./scripta/check-source
./scripta/check-compile
git diff --check
```

`check-source` and `check-compile` are regression guards. They do not
substitute for the executed-proba gate. A red Radix prerequisite keeps every
Gradus module below the executed-proba tier. A red Gradus case keeps only its
module row below the tier, while the aggregate gate exits non-zero and reports
the first failing case.

## 9. Open questions for Mind

- No architecture decision blocks lowering. The default is to preserve the
  existing 32 proba suites and use the package-aware MIR route rather than
  weakening receiver-method assertions.
- `rdx-s05-1` is required for the public `faber test .` invocation. The gate
  may use an absolute manifest path while that route is repaired, but Stage 0.5
  cannot close while the named package-path defect remains unresolved.
- `rdx-s05-2` must first verify whether the existing
  `link_library_method_targets` implementation only needs to be reached by the
  canonical package invocation, or whether its method metadata/rewrite needs a
  focused repair. It must not broaden direct single-file mode into an
  untyped generic method dispatcher.
- The `data` smoke is settled as discovery-only. Future batching, shuffling,
  and tokenization coverage belongs to a later data implementation unit.

## 10. Delivery readiness

This artifact is **READY for delivery audit**. It grounds the 32/33 census in
the live Gradus tree, identifies `src/data.proba` as the only authoring gap,
separates the direct MIR method-call diagnostic from the package-dot path
sibling, names the owning Radix surfaces and prerequisites, grounds the proba
grammar in the current parser and English examples, preserves the 32-file
corpus as an asset, defines the one gap-fill unit, and provides five
module-family batches plus 33 per-module executed-proba gate rows.
