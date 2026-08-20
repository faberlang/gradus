# MEASURE 2026-08-18 — first llama.cpp comparison (tiny models)

Handle `f8fce797` / packet `hand-67`. Measurement only. No kernel
tuning. This is the **baseline**, not a win.

**Status**: one-sample CPU-reference receipt. Not a product-speed claim.
Method home: `docs/benchmark-method.md` (hardware disclosure filled;
warmup/sample counts reduced because one 9-token forward is 39 s and
one decode loop is 7 min — see caveats).

---

## Machine

| Field | Value |
| --- | --- |
| Host | `burgus.local` (MacBook Pro `Mac17,7`) |
| CPU | Apple M5 Max — 18 cores (6 Super + 12 Performance) |
| Memory | 128 GB |
| OS | macOS 26.5.2 (25F84), Darwin 25.5.0 `RELEASE_ARM64_T6050` arm64 |
| Thermal | `pmset -g therm`: no thermal / performance warning recorded at start of either run. Laptop, n=1, not thermally soaked. |
| Gradus | `d1d49e35d645168c4401f92437e70a4483839c04` (`factory/hand-67` = main tip named in the task) |
| Packet radix (read-only) | `1277976c77f3664c80c2ae3b13ef4dbf60805530` (`release(faber): v1.8.0 + radix v0.83.0`) |
| Packet hosts (read-only) | `0783406e2a937e33bbd11748cf55a5752ccf6715` |
| Workspace norma (library home) | `bfbec6983bec319d15e4d6b841ae43203047c0d7` |
| Workspace faber runtime (path dep) | `0fe3a00fd0f5aa74ac5a9753f26a91850b12030f` |
| rustc / cargo | 1.97.1 Homebrew (`8bab26f4f` / `c980f4866`) |
| Tier | `cpu-reference` — never `gpu` for our side |

## Release tier (what `--release` is here)

Not `./scripta/test --release` (that is the radix ladder: `--full` +
`./scripta/e2e all`). The product release profile for a compiled
consumer is **Cargo `release`**:

1. Compiler: `cargo build --release -p faber` in the packet radix
   tree → `faber 1.8.0`, `Finished release profile [optimized]`.
2. Consumer: `faber build --target rust --release <exemplum>` — the
   `--release` flag (`crates/faber/src/cli/mod.rs` `BuildArgs.release`)
   is forwarded to `cargo build --release` on the emitted crate
   (`package/cargo.rs`, `package/mir/bin_runner.rs`).
3. A `--release` faber binary does **not** walk the dev-tree locale
   packs (`cfg!(debug_assertions)` only). Locale was supplied by a
   local `target/share/faber/locale` → `stdlib/locale` symlink. Not a
   product change.

Prefill rustc hit **E0382** in the G3 tokenizer table emit
(`per_id.insert(id, token); vocab.insert(token, id);`). One-line
`token.clone()` in the **generated** crate only (not Gradus source).
That path runs during tokenizer build, before `forward start`. Decode
compiled clean (no tokenizer import).

Trace helpers were **off** (no `trace` argv).

## Models

| File | bytes | SHA-256 | pin |
| --- | ---: | --- | --- |
| `SmolLM2-360M-Instruct-Q4_K_M.gguf` | 270,590,880 | `2fa3f013dcdd7b99f9b237717fa0b12d75bbb89984cc1274be1471a465bac9c2` | GI2-3 `radix/crates/faber-prefill-oracle/testdata/gi2-3-logits-golden/manifest.json` (`n_tokens=9`, ids `[504, 2365, 6354, 16438, 27003, 690, 260, 23790, 2767]`) |
| `Qwen2.5-0.5B-Instruct-Q4_K_M.gguf` | 397,808,192 | `6eb923e7d26e9cea28811e1a8e852009b21242fb157b26149d3b188f3a8c8653` | present at `/Users/ianzepp/Ai/models/`; llama-bench only this unit |

Path: `/Users/ianzepp/Ai/models/` (same inode as the GI2-3 `/Users/ianzepp/ai/models/` spelling).

## llama.cpp comparator

| Field | Value |
| --- | --- |
| Binary | `/opt/homebrew/bin/llama-bench` → Cellar `llama.cpp/10150` |
| Version | `10150 (dee2a846b)`, AppleClang 21.0.0.21000099, Darwin arm64 |
| ggml | Homebrew `0.17.0` (BLAS + Metal + `ggml-cpu-apple_m4`) |
| Command | `llama-bench -m <gguf> -p 512,9 -n 128,0 -r 5 -o md` |
| Shapes reported | `pp512`, `pp9` (9-token prefill **is** expressible), `tg128` |
| Metal row | default `-ngl -1`, `--threads 6` (backend label `BLAS,MTL`) |
| CPU rows | `-ngl 0` (0 GPU layers) at `-t 6` and `-t 1`. Backend label still `BLAS,MTL` because those plugins load; pp512 dropping 27180 → 407 t/s confirms CPU compute. |

Raw tables: `llama-bench-smollm2-*.md`, `llama-bench-qwen05-*.md`.

## Our side — method

Marker wrapper `bench/time_markers.py`: wall `time.perf_counter()` on
each stdout line. Prefill time is **`forward start T=9` → `forward done`**
(excludes admit, tokenizer, 32-layer f32 materialize, top-1/top-5 scan).
Decode time is per `decode_step` print interval.

`n=1` each. Not the method's 3-warmup / 10-sample compile protocol.

Correctness of the timed binaries: prefill `PREFILL: PASS` top-1 `30`
top-5 `5/5`; decode `DECODE: PASS` `generated=[30, 2, 198]`.

| Workload | interval | wall | implied t/s |
| --- | --- | ---: | ---: |
| SmolLM2 9-token `dense.forward` | `forward start` → `forward done` | **39.130 s** | **0.230** |
| SmolLM2 load (dequant + K-major transpose, 32 layers) | `loading stored-weight views` → `loaded layer 31` | 201.010 s | — |
| SmolLM2 process total (prefill binary) | start → exit 0 | 327.308 s | — |
| SmolLM2 G1 decode, 9 prompt `decode_step`s | `pos=0` → `first_sampled` | 364.464 s | 0.025 |
| SmolLM2 G1 decode, 2 generate `decode_step`s after first sample | `pos=9` → `generated=` | 75.839 s | 0.026 |
| SmolLM2 G1 mean of 11 `decode_step`s | see run log | **40.03 s/tok** | **0.025** |
| SmolLM2 decode process total | start → exit 0 | 707.053 s | — |

Prefill max RSS 3.87 GiB (`time -l` 3,868,835,840). Decode max RSS
4.31 GiB. Qwen compiled-rust consumer was **not** timed this unit
(`dense-prefill-qwen2` is historically rustc-red; out of scope).

---

## Comparison table

Times for llama.cpp are `n_tokens / (t/s)` from the 5-rep mean.
Our prefill is the 9-token `dense.forward` interval. Our decode is
the mean G1 `decode_step` (batch-1, already-loaded f32 weights).

| Model | Engine | Prefill pp512 | Prefill pp9 | Decode tg |
| --- | --- | ---: | ---: | ---: |
| SmolLM2-360M Q4_K_M | llama.cpp Metal (`ngl=-1`, t=6) | 27180 ± 1190 t/s (**18.8 ms**) | 790.3 ± 19.1 t/s (**11.4 ms**) | 136.4 ± 17.5 t/s (**7.33 ms/tok**) |
| SmolLM2-360M Q4_K_M | llama.cpp CPU (`ngl=0`, t=6) | 407.0 ± 17.7 t/s (1.26 s) | 306.1 ± 13.7 t/s (**29.4 ms**) | 159.5 ± 6.2 t/s (**6.27 ms/tok**) |
| SmolLM2-360M Q4_K_M | llama.cpp CPU (`ngl=0`, t=1) | 166.4 ± 0.2 t/s (3.08 s) | 84.04 ± 0.06 t/s (**107 ms**) | 66.65 ± 0.07 t/s (**15.0 ms/tok**) |
| SmolLM2-360M Q4_K_M | **faber rust `--release`**, CPU reference, n=1 | not run (consumer is T=9 only) | **0.230 t/s (39.13 s)** | **0.025 t/s (40.0 s/tok)** |
| Qwen2.5-0.5B Q4_K_M | llama.cpp Metal (`ngl=-1`, t=6) | 25379 ± 1361 t/s (20.2 ms) | 723.0 ± 19.4 t/s (12.4 ms) | 205.5 ± 18.8 t/s (4.87 ms/tok) |
| Qwen2.5-0.5B Q4_K_M | llama.cpp CPU (`ngl=0`, t=6) | 462.6 ± 8.3 t/s (1.11 s) | 281.8 ± 16.8 t/s (31.9 ms) | 141.4 ± 0.6 t/s (7.08 ms/tok) |
| Qwen2.5-0.5B Q4_K_M | llama.cpp CPU (`ngl=0`, t=1) | 179.4 ± 0.3 t/s (2.86 s) | 75.02 ± 0.07 t/s (120 ms) | 55.10 ± 0.06 t/s (18.1 ms/tok) |
| Qwen2.5-0.5B Q4_K_M | faber-compiled | — | **not timed** | **not timed** |

### Honest gap (SmolLM2)

| Compare | Prefill pp9 | Decode |
| --- | ---: | ---: |
| vs llama.cpp Metal | **3436× slower** (39.13 s / 11.4 ms) | **~5460× slower** (40.0 s / 7.33 ms) |
| vs llama.cpp CPU t=6 | **1331× slower** (39.13 s / 29.4 ms) | **~6380× slower** (40.0 s / 6.27 ms) |
| vs llama.cpp CPU t=1 (closest hardware) | **365× slower** (39.13 s / 107 ms) | **~2670× slower** (40.0 s / 15.0 ms) |

Expected. This path is the declared-f32 CPU reference bring-up, not
the R-PACK-05 native packed device path, and not a SIMD/threaded
host kernel.

---

## Where the known costs live

Cited from `docs/design/numeric-flexibility-performance.md` **§8.1**
(ranked gap vs llama.cpp) and the live consumer:

1. **No flash attention** — we materialize scores then
   `CausalMaskedSoftmax` (`§8.1` item 1). Biggest long-context lever;
   small at T=9.
2. **No regime-split GEMM** — one tiled / reference matmul for
   prefill and decode (`§8.1` item 2). llama.cpp MMQ vs MMVQ. Our
   decode_step (~40 s) is as expensive as the whole 9-token prefill
   (39 s): batch-1 walks the same f32 weights with no GEMV kernel.
3. **Quantized KV / SWA / paged cells** — we append dense f32
   (`§8.1` item 3). Irrelevant at T=9 / cache_len=11.
4. **No graph reservation/reuse** — EXEC-03 pending (`§8.1` item 4).
5. **No per-shape-class kernel tables** (`§8.1` item 5).
6. **No thread/batch CLI** — `--backend` only (`§8.1` item 6). This
   binary is single-thread scalar Rust.

Costs that dominate **today's** 39 s / 40 s/tok, before those
device-path items:

- **Whole-model F32 expansion** at load (201 s): GGUF-A7 "quantized
  means native" is not this consumer. Every Q4_K/Q5_0/Q6_K/Q8_0
  tensor is dequantized to `list<f32>` then K-major-transposed.
- **Reference-tier kernels**: Faber `nn.linear` / attention / RMSNorm
  compiled to generated Rust loops. No SIMD. No threading. 8×8 tile
  plan is for device recipes, not this host path.
- **Carrier overheads**: `list<f32>` tensors, per-element
  `coalesce`, generated match/`Result` wrappers, 846 rustc warnings
  of unused `Result`s. Vocab scan after prefill added 4.5 s.

`§8.3`: "No perf claim in this doc is evidence — every gain in §7 is
a mechanism awaiting measurement." This receipt is that first
measurement.

---

## Caveats

- n=1. No warmup of the forward itself (load is a de-facto warmup of
  page cache; forward sees resident f32 weights).
- Laptop thermal; no warning, but not a locked-clock soak.
- llama.cpp Metal is what users actually run on this machine. CPU
  t=1 is the least-unfair hardware compare and we are still 365×
  (prefill) / 2670× (decode) behind it.
- Prefill required a generated-Rust clone patch (tokenizer E0382).
  Decode did not.
- Qwen is comparator-only this unit.
- `time -l` user+sys > real (prefill 167+181 vs 327 real; decode
  334+394 vs 707 real) with tens of millions of involuntary context
  switches — recorded, not interpreted.
