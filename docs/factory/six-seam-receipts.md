# Six-Seam Resident Verification Receipts (Issues #33–#39, #108)

Captured on `pepper` (Apple M5 Max, 128 GB unified memory, `aarch64-apple-darwin`) with `faber-edge` (`faber 1.24.0`, Metal KIR + Cranelift JIT) against local resident checkpoints in `~/ai/models/`.

## Slice A — `SmolLM2-135M-Instruct-8bit` (Seams 1–5, B=1 Metal 64-token greedy decode)

- **Checkpoint:** `/Users/ianzepp/ai/models/SmolLM2-135M-Instruct-8bit` (single-shard Safetensors, GroupAffine 8-bit `u32` weights + `f16` scales/biases, `group_size=64`)
- **Command:** `faber run --library-home .. --device metal exempla/slice-a-smollm2-8bit-resident`
- **Backend:** `metal` on Apple M5 Max (115,448,725,504 B budget), zero `NumericBlock`, zero F32 weight expansion
- **Observed timings & tokens:**
  - Admission (`ModelConfig` + `ModelBundle` + `TensorDirectory` + 211 `LinearWeight` bindings + `ExecutionSchedule`): `6 ms`
  - Tokenizer (`vocab.json` 49,152 entries + `merges.txt` 48,900 merges): `32 ms` (`stage=tokenizer ms=38`)
  - Weight load (143 MB `u32` via `via le` + `f16` scales/biases + Metal priming): `load_ms=1046`
  - Prompt: `"The capital of France is"` -> `prompt_ids=[504, 3575, 282, 4649, 314]`
  - First step: `first_top1=7042`, `first_logit=15.940572`
  - Decode (68 total steps = 5 prompt + 64 greedy tokens): `decode_ms=15120`, `ms_per_tok=222.36`, `tok_per_s=4.50`
  - Greedy 64-token continuation:
    `" Paris. Paris is the largest city in France and the capital of the French department of the northern part of the country. Paris is known for its historical landmarks, cultural institutions, and cultural attractions.\n\nParis is a city that is famous for its art, architecture, fashion, gastronomy, and culture. It is also"`
- **Dense F32 Metal reference (`SmolLM2-360M-Instruct-f32.gguf`):**
  - Command: `faber run --library-home .. --device metal exempla/dense-decode-f32`
  - `load_ms=24375`, `first_step_top1=7042` (`logit=23.067291`), `decode_ms=1235` for 68 steps (`18.16 ms/tok`, `55.06 tok/s`), decoded `" Paris.\n\nParis is the capital of France..."`

## Slice B0 — Flint INT4 5-Shard Unindexed Safetensors (Seams 1–4, #108)

- **Checkpoint:** `/Users/ianzepp/ai/models/hf/RecursiveSI/flint-int4/3b93f9053b530488405ae9fca51d4900d6ce21f0` (5 unindexed Safetensors shards, no `index.json`, GroupAffine 4-bit/8-bit `u8` weights + `bf16` scales/biases)
- **Command:** `faber run --library-home .. --device cpu exempla/flint-resident`
- **Observed receipt:**
  `flint_resident: model_type=flint shards=5 tensors=1751 layers=49 slots=49 full=14 ring=35 window=513 dense=2 moe=47 rope=35 norope=14 softmax=learnable gating=sigmoid emb_out=150144 q0_out=4096 head_out=150144 l2_experts=256`

## Slice B — `Qwen3.6-35B-A3B-UD-Q4_K_M.gguf` (Seams 1–4, #108)

- **Checkpoint:** `/Users/ianzepp/ai/models/Qwen3.6-35B-A3B-UD-Q4_K_M.gguf` (22.1 GB single-file GGUF, bounded header-only range read)
- **Command:** `faber run --library-home .. --device cpu exempla/qwen36-resident`
- **Observed receipt:**
  `qwen36_resident: arch=qwen35moe layers=40 tensors=733 hybrid_tensors=30 full_tensors=10 slots=40 full_kv=10 linear_ssm=30 conv_kernel=4 q4k=80 q5k=37 q6k=4 q8_0=251 bf16=0 expert_rank3=120 qkv0_out=8192 full3_q_out=8192 l0_experts=256`

## Slice B0 & Slice B Metal Kernel Verification (`exempla/hybrid-stage-bench-metal`, #108)

- **Command:** `faber run --library-home .. --device metal exempla/hybrid-stage-bench-metal`
- **Backend:** `metal` on Apple M5 Max
- **Observed parity & steady-state timings:**
  - `sink_softmax` (Flint O(C) learnable sink softmax): `max_err=1.16e-9`, `141–148 µs/call`
  - `deltanet_recurrence` (Qwen3.6 device DeltaNet): `max_err=3.73e-9`, `1615–1616 µs/call`
  - `rmsnorm_heads_2pass` (Flint/Qwen3.6 QK-norm): `max_err=5.96e-8`, `25–34 µs/call`
  - `query_tiled_prefill` (B=C prefill attention): `max_err=0.0`, `1558–2025 µs/call` (`15.8k–20.5k tok/s`)

## Slice C & D — `Inkling-2-Mini-MLX-8bit` + `mtp.safetensors` (Seams 1–3, 6)

- **Checkpoint:** `/Users/ianzepp/ai/models/Inkling-2-Mini-MLX-8bit` (4 backbone shards + bundled `mtp.safetensors`, nested `text_config` + `mtp_config` + `quantization`)
- **Command:** `faber run --library-home .. --device cpu exempla/inkling2-resident`
- **Observed receipt:**
  `inkling2_resident: model_type=inkling2_loop layers=24 hidden=2304 vocab=201024 unpadded_vocab=200058 tensors=1614 bb_slots=48 bb_visits=48 bb_full=8 bb_ring=40 dr_slots=3 dr_ring=2 dr_full=1 mtp_block=8 mtp_taps=4 mtp_fuse=true mtp_norm=true mtp_ctx=true mtp_w1=true borrowed_head=true`
