# dense-decode-f32 — Typed F32 Whole-Model Decode (Issue #28 / GPU G01)

Metadata-driven whole-model F32 greedy decode over `/Users/ianzepp/ai/models/SmolLM2-360M-Instruct-f32.gguf` (override via CLI arg or `SMOL_F32_GGUF`):

1. Inspects GGUF metadata and tensor directory via `gradus:model/gguf_manifest`, `gradus:model/bundle`, and `gradus:model/tensor_directory`.
2. Admits `DenseModelSpec`, builds `ExecutionSchedule` (`LinearSegment`), `LayerParams`, and `Workspace` via `gradus:decode_dense` with zero hardcoded dimensions inside `gradus:decode_dense`.
3. Loads all 290 F32 weights in GGUF row-major `[out, in]` layout, primes device buffers, and generates 64 greedy tokens for `"The capital of France is"` over `gradus:decode_token` and `gradus:decode_step`.

## Parity Receipt (Apple M5 Max, 2026-11-27, `faber-edge 1.24.0` `c2f9421d`)

- **Command (Metal)**:
  `faber run --device metal --library-home <gradus-parent> exempla/dense-decode-f32`
  - `engine`: `clif-jit`, `backend`: `metal` (`Apple M5 Max`)
  - `launches`: `cpu=0`, `gpu=30887`, `total=30887` (`command_submit_count=69`, `blocking_wait_count=69`)
  - `peak_allocated_bytes`: `1459352164`, `model_bytes_uploaded`: `1447284484`, `gpu_busy_ns`: `1033732667`
  - `decode_ms`: `1816` (`68` steps = `5` prompt + `63` continuation steps)
  - `first_step_top1`: `7042` (`logit=23.067291`)
  - `head8`: `[8.511789, 1.4573932, 4.7825403, -0.4556687, -0.48974168, 0.9487146, -1.182575, 0.9487146]`
- **Command (CPU)**:
  `faber run --device cpu --library-home <gradus-parent> exempla/dense-decode-f32`
  - `decode_ms`: `2327` (`68` steps)
  - `first_step_top1`: `7042` (`logit=23.067293`)
  - `head8`: `[8.511789, 1.4573888, 4.7825365, -0.4556712, -0.48974663, 0.94871044, -1.1825736, 0.94871044]`
- **Parity verdict**: `first_step_top1` matches (`7042`), `head8` max abs diff `4.95e-6`, and all 64 greedy token IDs (`[7042, 30, 198, 198, 38634, 314, 260, 3575, 282, 4649, ...]`, decoding to `" Paris.\n\nParis is the capital of France..."`) match identically between Metal and CPU.

## Decisions & Compiler Boundary Findings

- **`inferentia` oracle withdrawn**: Per the 2026-11-24 issue ruling, `inferentia` `port_generate` is not on `main`; paired CPU vs Metal parity serves as the correctness oracle.
- **`list<tensor<f32, [N, K]>>` host-call re-test**:
  - Passing `list<dt.LayerWeights<...>>` / `list<dt.SlotView<...>>` directly into a generic host function still declines Cranelift (`field of a non-genus` when projecting fields off generic elements indexed out of a `list`).
  - Storing `list<tensor<f32, [...]>>` fields inside `dd.DenseLayerBank` + `sess_mod.SessionState.full_kv` compiles and runs cleanly inside `gradus` (`+++ faber test` passes across tied 2-layer Llama and untied biased 3-layer Qwen2 configs).
  - Across an external `--library-home` package boundary (`exempla/dense-decode-f32`), 2-hop generic calls (`dd.generate_greedy` / `dd.forward_token_logits`) hit `clif-jit declined: instantiated generic type is missing semantic metadata` (same compiler boundary as `exempla/slice-a-smollm2-8bit-resident`), so `exempla/dense-decode-f32` uses `gradus:decode_dense` for admission/schedule/workspace setup and executes single-hop `gradus:decode_token` (`embed_wide`, `layer_wide_table`, `head_wide`) + `gradus:decode_step` (`argmax_token`) kernels directly.
