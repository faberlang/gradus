# NumericBlock retirement: current inventory and dependency order

This is a source-tree inventory, not a claim that the carrier has been removed.
It records the first migration boundary for the clean break: no alias, adapter,
or second carrier is to remain after callers move to typed tensors with runtime
extents and their glyph operations.

## Checkout and census

The Gradus repository is the current checkout: its library lives directly under
`src/`, not `gradus/src/`. At the checked-out tree, `src/` contains 21 `.fab`
files with 733 raw `NumericBlock` mentions and 22 co-located `.proba` files
with 555 mentions. Those counts include comments as well as code. No top-level
`inferentia/` source tree is present, so its source and test uses cannot be
classified or verified here. The separate application tree is a blocker for
closing the default-backend part of this work.

The source references classify as follows:

| Gradus public surface | Files | Mentions | Classification |
| --- | --- | ---: | --- |
| Tensor value definition and construction | `src/tensor.fab` | 22 | Live public contract and carrier definition; remove last, after all consumers leave. |
| Math operations | `src/math.fab` | 44 | Live public compute API. Typed same-shape arithmetic exists for a subset; the carrier operations remain for runtime-shaped paths. |
| Neural-network primitives | `src/nn.fab` | 34 | Live public API. Typed glyph primitives coexist with carrier operations, including gather/transpose and runtime-shaped variants. |
| Attention | `src/attention/gqa.fab` | 116 | Live public attention and cached-attention path; its principal implementation is carrier-based. The static SDPA entry is a separate typed surface. |
| Transformer composition | `src/transformer.fab` | 142 | Live public carrier blocks and cached blocks, alongside newer typed dense-block entries. |
| Dense model assembly | `src/model/dense.fab` | 144 | Live public loader, forward, decode, and cached-prefill surfaces. The file contains both typed model pieces and carrier-based routes; the public carrier routes are not dead merely because typed pieces exist. |
| MoE | `src/model/moe.fab` | 56 | Live public router, expert, and FFN paths over the carrier. |
| Hybrid model state | `src/model/qwen35moe_state/{session,linear_attn,full_attn}.fab` | 26 | Live model-state and attention paths; parameter windows currently produce carriers. |
| Decode and generation | `src/decode.fab`, `src/generation/{decoder,dense}.fab` | 81 | Live public decoder/generation routes and their model-value boundary. |
| KV cache | `src/cache/kv.fab` | 24 | Live public decoded-value cache operations and fields. Encoded storage is a distinct contract, not a carrier replacement. |
| Training, gradients, losses, metrics, MLP, parameters | `src/{train,gradient,loss,metrics,mlp,parameter}.fab` | 41 | Live public training/value surfaces, including carrier-valued dropout, loss, metric, gradient, and parameter payloads. |
| Historical shape rationale | `src/shape.fab` | 3 | Comments only; no executable carrier use. These historical claims should be removed or rewritten when the final carrier definition is deleted. |

No source reference is classified as proven dead code by this census. Public
signatures remain live public surface even when this repository has no local
caller. The census is not a whole-program dead-code proof; a later unit must
check callers before deleting any internal-only helper.

All 22 `.proba` files are test/oracle-only uses, not product implementations.
They pin current behavior and should be migrated to typed-path tests where
that behavior remains supported, or removed only when the behavior itself is
retired. File counts:

| Test surface | `.proba` files and raw mentions |
| --- | --- |
| Tensor, math, NN, attention, transformer | `tensor` 10; `math` 64; `nn` 48; `attention` 114; `transformer` 51 |
| Dense, MoE, hybrid model state | `model/dense` 76; `model/dense_load_static` 4; `model/moe` 38; `model/qwen35moe_state` 8 |
| Decode and generation | `decode` 30; `generation` 26 |
| Training and value APIs | `gradient` 2; `loss` 8; `metrics` 8; `mlp` 13; `optimize` 3; `parameter` 2; `prepared_state` 17; `train` 2; `data` 14; `cache` 15; `model/gguf` 2 |

There are also 19 source examples under `exempla/` with 457 mentions. They are
consumer code, not tests or implementation internals, and must move with the
public API they exercise. The examples cover dense blocks/models, GQA and RoPE,
NN primitives, prefill/decode/generation, MoE, token generation, and training.

## Removal order

1. **Establish typed runtime-size prerequisites.** Confirm the current build
   compiler has the required runtime extents and glyph operations. This is an
   engineering dependency; do not change Faber syntax or semantics in Gradus.
   No compiler build or run was performed on this machine.
2. **Leaf math and NN.** Move each live carrier operation to an equivalent
   typed runtime-extent/glyph form, migrate its `.proba` coverage and direct
   callers, then delete the carrier operation. This includes math construction,
   elementwise residuals, reductions, matmul, casts, concatenate/slice and NN
   carrier primitives. Preserve numerical and error behavior in the tests;
   do not retain a forwarding alias.
3. **Attention and cache.** Move GQA/RoPE attention and the decoded KV cache
   state onto typed tensors and runtime extents; migrate attention/cache
   tests and consumers before removing carrier fields and signatures.
4. **Model and generation.** Move transformer blocks, dense and MoE assembly,
   hybrid state windows, decode, prefill, generation, and their public
   consumers/examples. Their dependencies must already be carrier-free.
5. **Definition and final sweep.** Delete `NumericBlock` and its construction,
   validation, and access API from `src/tensor.fab`; remove obsolete tests and
   historical comments. Require zero matches in Gradus source and tests. Do
   not add a compatibility genus or adapter beside typed forms.
6. **Inferentia default.** The operator's later ruling is to retire the legacy
   CPU carrier backend rather than add a typed adapter. The Inferentia checkout
   is absent here, so neither its current default nor the supported replacement
   path can be verified. Before deleting that route, confirm the product's
   supported generation path and ensure the default no longer selects the slow
   CPU carrier backend.

## Performance evidence still required

Record same-machine before/after timings for each live path that is migrated,
using the same model, prompt, output length, and backend. Separate load/admission
from prefill and decode timings, and retain the exact command and revisions with
the measurements. This checkout has no Inferentia source or runnable application
harness, and local compilation/runs are prohibited, so this inventory makes no
before/after performance claim.

## Validation status

The tree inventory above is a text scan only. The Gradus `.proba` suite, A1
oracle, and all compile-backed proofs remain for the build machine. The required
tracked-file-size and planning-hygiene scripts are not present in this
checkout; that limitation should be resolved by the runner or reported with the
build-machine proofs.
