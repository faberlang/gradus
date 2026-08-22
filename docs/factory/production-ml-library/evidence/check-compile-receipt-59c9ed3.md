# Receipt — gradus check-compile at frozen tip 59c9ed3

- **Goal**: close auditor 65bdef24 residual P2 evidence gap (warm-boot audit 2b43f700): endian (fe041a6) and moe-probe check-compile registration (fccd376) landed with no executed receipt at tip 59c9ed3.
- **Command**:

  ```text
  ./scripta/check-compile
  ```

- **Frozen revision**: gradus 59c9ed349b35e6a2b0982b1c0d343e69c25b6d4c (clean checkout, no worktree needed)
- **faber binary**: radix c88feba56 (contemporaneous with the gradus tip; 2026-08-22 11:29), built in a detached worktree because the radix main checkout is dirty with foreign dirt
- **cwd**: `/Users/ianzepp/work/faberlang/gradus`
- **Date**: 2026-08-22
- **Exit status**: 0
- **Output (summary)**: all blocks pass — gradus library source, gradient-seam, training-loop-mlp, token-generation, generate-route, gguf-manifest, gguf-inspect, gguf-materialize, qwen36-35b-inference, gguf-admit-qwen35moe, moe-probe (the block registered by fccd376), final line `check-compile: ok`.

## Known red against radix main (residual, out of scope)

The same command against the current radix main binary (92733a2 + working tree) exits 1 with `SEM008:itera_binder_pattern_unsupported` on `for range … const _` binders (SEM008 surface introduced by radix fe0708c81, 2026-08-22 12:16 — after the gradus tip) and `PKG001` on `gradus:nn`/`gradus:dtype` imports. The frozen-tip code is green under the contemporaneous compiler; the current-main failures are a radix-side regression to route separately.
