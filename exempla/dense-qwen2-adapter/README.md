# REF-01-U1.7 — qwen2 (Qwen2.5) architecture adapter

This package is the executed proof for the typed `gradus:model/dense_qwen2`
architecture adapter. Its source builds bounded synthetic GGUF v3 corpora in
memory carrying the canonical tensor table of the pinned Qwen2.5-0.5B row
(the GGUF-A1b inspect-surface facts: layer 0 full + layer 23 boundary, tied
and untied variants), parses them through `gradus:model/gguf_manifest`, runs
the adapter (`configura` + `resolve` + `descriptio_render`), and prints a
PASS/FAIL line for every canonical resolution plus the fail-closed rejection
rows. It performs no filesystem read, download, mmap, or model-payload
allocation.

## Contract

The qwen2 adapter maps the canonical dense tensor-name family (the same
canonical family as the `llama` adapter) to manifest descriptors, with the
qwen2 deltas:

- **Tie status read from the tensor set** (gi0-model-contract precedent):
  `output.weight` present → untied `lm_head`; absent → tied (resolves to
  `token_embd.weight`). The pinned 0.5B row is tied; the exempla proves both
  paths.
- **GQA head config**: `qwen2.attention.head_count` 14 / `head_count_kv` 2
  are frozen into the config; `head_dim` is derived as
  `embedding_length / head_count` (896 / 14 = 64).
- **`rope_theta` 1000000**: the qwen2 family delta. The float
  `qwen2.rope.freq_base` wire value is preserved by the manifest but not
  decoded by the integer accessor, so the adapter freezes theta as the typed
  family fact.

Fail-closed typed diagnostics cover unknown canonical names, unknown layer
tensor suffixes, out-of-range layer indices, tensors missing from the
manifest, and non-qwen2 manifests. The co-located
`src/model/dense_qwen2.proba` pins the same descriptor-resolution facts at
compile level; the current imported-library `faber test` route is
provider-blocked, so the package-MIR run below is the executed proof.

## Receipt

Command, from the Hand packet:

```text
cd /Users/ianzepp/work/faberlang/worktrees/hand-11/gradus
env FABER_LIBRARY_HOME=/Users/ianzepp/work/faberlang/worktrees/hand-11 \
  /Users/ianzepp/work/faberlang/worktrees/hand-16/radix/target/debug/faber \
  run --target fmir exempla/dense-qwen2-adapter
```

Observed result (2026-08-14): exit `0`; 23 PASS lines and 0 FAIL lines.

```text
qwen2-config-tied: PASS observed=24/14/2/64/896/151936/1000000/true
qwen2-config-untied: PASS observed=24/14/2/64/896/151936/1000000/false
qwen2-embed_tokens: PASS observed=token_embd.weight/896,151936/known/32
qwen2-l0-input_layernorm: PASS observed=blk.0.attn_norm.weight/896/known/1
qwen2-l0-self_attn-q_proj: PASS observed=blk.0.attn_q.weight/896,896/known/32
qwen2-l0-self_attn-k_proj: PASS observed=blk.0.attn_k.weight/896,128/known/32
qwen2-l0-self_attn-v_proj: PASS observed=blk.0.attn_v.weight/896,128/known/32
qwen2-l0-self_attn-o_proj: PASS observed=blk.0.attn_output.weight/896,896/known/32
qwen2-l0-post_attention_layernorm: PASS observed=blk.0.ffn_norm.weight/896/known/1
qwen2-l0-mlp-gate_proj: PASS observed=blk.0.ffn_gate.weight/896,4864/known/32
qwen2-l0-mlp-up_proj: PASS observed=blk.0.ffn_up.weight/896,4864/known/32
qwen2-l0-mlp-down_proj: PASS observed=blk.0.ffn_down.weight/4864,896/known/256
qwen2-l23-input_layernorm: PASS observed=blk.23.attn_norm.weight/896/known/1
qwen2-l23-self_attn-q_proj: PASS observed=blk.23.attn_q.weight/896,896/known/32
qwen2-l23-mlp-down_proj: PASS observed=blk.23.ffn_down.weight/4864,896/known/256
qwen2-model-norm: PASS observed=output_norm.weight/896/known/1
qwen2-lm_head-tied: PASS observed=token_embd.weight/896,151936/known/32
qwen2-lm_head-untied: PASS observed=output.weight/896,151936/known/32
qwen2-reject-unknown-name: PASS observed=unknown canonical qwen2 tensor name: model.foo
qwen2-reject-unknown-suffix: PASS observed=unknown canonical qwen2 layer tensor suffix: .self_attn.x_proj
qwen2-reject-layer-range: PASS observed=layer index out of range for canonical tensor: model.layers.24.input_layernorm
qwen2-reject-missing-tensor: PASS observed=canonical model.layers.1.input_layernorm missing from manifest: blk.1.attn_norm.weight
qwen2-reject-architecture: PASS observed=architecture is not qwen2: llama
```

The receipt proves the typed canonical resolution and fail-closed rejection
surface of the qwen2 adapter over the pinned Qwen2.5-0.5B descriptor facts. It
does not tokenize, materialize tensor payloads, execute a model, produce
logits, or claim any device execution; those remain the REF-01 U1.8–U3
surfaces.
