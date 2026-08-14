# REF-01-U1.6 — executable `llama` (SmolLM2) architecture adapter proof

This package is the executable proof for the typed llama architecture adapter
in `gradus:model/dense_llama` (REF-01-U1.6). Its source builds a synthetic
GGUF v3 table corpus carrying the exact descriptor facts the GGUF-A1b inspect
surface reports for the real SmolLM2-360M-Instruct-Q4_K_M.gguf file
(read-only pinned facts — shapes, GGML type ids, and known layouts were
measured from the real file's manifest on 2026-08-14; no artifact bytes are
committed), then resolves every canonical tensor name through the public
adapter surface and prints a PASS/FAIL line per case. It performs no
filesystem read, download, mmap, or model-payload allocation.

## Evidence boundary

The package runs through package MIR with the lane faber binary. The receipt
below is the executed claim for the adapter: every canonical resolution
(`model.embed_tokens`, `model.layers.{N}.input_layernorm`,
`model.layers.{N}.self_attn.{q,k,v,o}_proj`,
`model.layers.{N}.post_attention_layernorm`,
`model.layers.{N}.mlp.{gate,up,down}_proj`, `model.norm`, `lm_head`) plus the
fail-closed rejection rows (unknown canonical name, out-of-range layer index,
missing manifest tensor, unknown GGML layout) print PASS. Co-located
`src/model/dense_llama.proba` pins the same rows at compile level; focused
`faber test` execution remains blocked by the imported-library provider seam.

## Receipt

Command, from the Hand packet:

```text
cd /Users/ianzepp/work/faberlang/worktrees/hand-8/gradus
env FABER_LIBRARY_HOME=/tmp/faber-library-hand8 \
  /Users/ianzepp/work/faberlang/worktrees/merge/radix/target/debug/faber \
  run --target fmir exempla/dense-llama-adapter
```

Observed result (2026-08-14): exit `0`; 19 PASS lines and 0 FAIL lines.

```text
frozen-smollm2-config: PASS observed=SmolLM2-360M/32/15/5/64/960/49152/true
model.embed_tokens: PASS observed=model.embed_tokens/token_embd.weight/[960,49152]/known
model.layers.0.input_layernorm: PASS observed=model.layers.input_layernorm/blk.0.attn_norm.weight/[960]/known
model.layers.0.self_attn.q_proj: PASS observed=model.layers.self_attn.q_proj/blk.0.attn_q.weight/[960,960]/known
model.layers.0.self_attn.k_proj: PASS observed=model.layers.self_attn.k_proj/blk.0.attn_k.weight/[960,320]/known
model.layers.0.self_attn.v_proj: PASS observed=model.layers.self_attn.v_proj/blk.0.attn_v.weight/[960,320]/known
model.layers.0.self_attn.o_proj: PASS observed=model.layers.self_attn.o_proj/blk.0.attn_output.weight/[960,960]/known
model.layers.0.post_attention_layernorm: PASS observed=model.layers.post_attention_layernorm/blk.0.ffn_norm.weight/[960]/known
model.layers.0.mlp.gate_proj: PASS observed=model.layers.mlp.gate_proj/blk.0.ffn_gate.weight/[960,2560]/known
model.layers.0.mlp.up_proj: PASS observed=model.layers.mlp.up_proj/blk.0.ffn_up.weight/[960,2560]/known
model.layers.0.mlp.down_proj: PASS observed=model.layers.mlp.down_proj/blk.0.ffn_down.weight/[2560,960]/known
model.norm: PASS observed=model.norm/output_norm.weight/[960]/known
lm_head-tied: PASS observed=lm_head/token_embd.weight/[960,49152]/known
model.layers.31.input_layernorm: PASS observed=model.layers.input_layernorm/blk.31.attn_norm.weight/[960]/known
unknown-canonical-rejected: PASS observed=ERR:unknown canonical tensor name: model.layers.mlp.silu_proj
out-of-range-layer-rejected: PASS observed=ERR:layer index outside the frozen llama layer range: 32
negative-layer-rejected: PASS observed=ERR:layer index outside the frozen llama layer range: -1
missing-tensor-rejected: PASS observed=ERR:canonical tensor is absent from the manifest: output_norm.weight
unknown-layout-rejected: PASS observed=ERR:canonical tensor resolves to an unknown GGML layout: blk.0.ffn_gate.weight
```

The source-level command `faber check exempla/dense-llama-adapter` is green,
and `scripta/check-compile` includes that package check. This is an executed
synthetic adapter proof, not a model-execution, logit, tokenizer, or
inference claim — the adapter feeds Gate 1 (dense model assembly, REF-01-U1.8)
and the prefill receipts (U1.9/U1.10), which own those claims.
