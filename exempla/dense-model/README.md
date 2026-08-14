# dense-model — dense model assembly executed proof (REF-01-U1.8)

This package is the executed proof for the REF-01-U1.8 dense model
assembly in `gradus:model/dense` (`praevideo`): the complete ordered dense
forward graph — embedding gather → 2 ordered U1.5 dense blocks → final
RMSNorm → output projection — assembled from the typed architecture config
(`ConfiguraDensa`) and materialized stored-weight views via canonical
tensor names, for a small synthetic dense config with **TIED** and
**UNTIED** embedding rows. It runs through package MIR
(`faber run --target fmir exempla/dense-model`) and prints PASS for every
pinned value (0 FAIL, exit 0).

## What is proved

`praevideo` composes the already-proven rows over the staged f32 carrier:

1. **embedding gather** — the resolver returns the stored `[D, V]` view
   (the GGUF/A1b descriptor layout); the assembly transposes it and gathers
   the token rows;
2. **2 ordered U1.5 blocks** — each resolved by its canonical
   `model.layers.{N}.*` names and shape-validated against the config
   (`dense_block`: input RMSNorm → GQA causal+RoPE attention → residual →
   post-attn RMSNorm → SwiGLU MLP → residual);
3. **final RMSNorm** — `model.norm` over the block stack;
4. **output projection** — a **tied** `lm_head` reuses the stored embedding
   view directly; an **untied** row resolves `lm_head` as its own canonical
   tensor. The linear biases are synthesized zero same-shape tensors (the
   llama/qwen2 canonical family carries no bias weights — the executed
   same-shape-bias contract of the composed rows).

No per-row special-case constants: every shape derives from the config and
the runtime tensors; the row-pinned grep over the assembly stays clean.

## Pinned config

One synthetic dim config, pinned to independent f64 reference values
(external Python/numpy evaluation of the documented formulas — the PML3
`transformer_block` pin precedent; the block transcription is first
validated against the pinned dense-block values in `src/transformer.proba`),
compared within the documented 5e-4 absolute tolerance:

- `T=2, D=16, F=16` (MLP hidden), `num_heads=4, num_kv_heads=2`,
  `head_dim=4`, `vocab 8`, tokens `[0, 7]`, positions `[0, 1]`;
- `rope_dim 4`, consecutive-pair (llama NORM) `freq_base 100000`,
  dk scale `0.5`, RMSNorm `ε = 1e-5`;
- layer 0 weights are the pinned dense-block row; layer 1 is a distinct
  deterministic set (the pinned row × 1.7); the embedding / final norm /
  untied head are deterministic pattern fills.

The full-graph pins use **zero same-shape biases** for every linear row —
the assembly's synthesized-bias contract (the real-bias literals of the
U1.5 block exemplum are not part of the canonical family). The same config
and reference values live at compile level in `src/model/dense.proba`.

## Run

```
faber run --target fmir exempla/dense-model
```

No device handle, no performance claim; forward-only (no autograd import).

## Receipt

Command, from the Hand packet:

```text
cd /Users/ianzepp/work/faberlang/worktrees/hand-11/gradus
env FABER_LIBRARY_HOME=/Users/ianzepp/work/faberlang/worktrees/hand-11 \
  /Users/ianzepp/work/faberlang/worktrees/hand-11/radix/target/debug/faber \
  run --target fmir exempla/dense-model
```

Observed result (2026-08-14): exit `0`; 37 PASS lines and 0 FAIL lines:

```text
tied-shape: PASS
tied-dtype: PASS
tied_0_0: PASS
tied_0_1: PASS
tied_0_2: PASS
tied_0_3: PASS
tied_0_4: PASS
tied_0_5: PASS
tied_0_6: PASS
tied_0_7: PASS
tied_1_0: PASS
tied_1_1: PASS
tied_1_2: PASS
tied_1_3: PASS
tied_1_4: PASS
tied_1_5: PASS
tied_1_6: PASS
tied_1_7: PASS
untied-shape: PASS
untied-dtype: PASS
untied_0_0: PASS
untied_0_1: PASS
untied_0_2: PASS
untied_0_3: PASS
untied_0_4: PASS
untied_0_5: PASS
untied_0_6: PASS
untied_0_7: PASS
untied_1_0: PASS
untied_1_1: PASS
untied_1_2: PASS
untied_1_3: PASS
untied_1_4: PASS
untied_1_5: PASS
untied_1_6: PASS
untied_1_7: PASS
reject-missing: PASS
```

The fail-closed row (`reject-missing`) proves the resolver-failure path:
a canonical tensor that cannot be materialized fails closed with the typed
`TensorAbsens` diagnostic. Structural gates (`./scripta/check-source`,
`./scripta/check-compile`) are green on the unit's changed-path list; the
full-graph pins live at compile level in `src/model/dense.proba` (proba
bodies remain provider-blocked — the executed proof is this package).

## Related

- Rows: `src/model/dense.fab` (`praevideo`, `ConfiguraDensa`, `Repertum`,
  `DenseError`) + pins in `src/model/dense.proba`
- Composed rows: `gradus:transformer` `dense_block` (REF-01-U1.5),
  `gradus:nn` `rmsnorm`/`linear` (REF-01-U1.1 / the PML3 surface),
  `gradus:attention` `multi_head_attention` (REF-01-U1.4)
- Adapters: `gradus:model/dense_llama` (REF-01-U1.6), `gradus:model/dense_qwen2`
  (REF-01-U1.7)
- Diagnostics: `docs/diagnostics.md` (`DenseError`)
- API: `docs/api-reference.md` (`gradus:model/dense`)
