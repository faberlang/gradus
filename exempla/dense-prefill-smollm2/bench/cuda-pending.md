# CUDA comparator lane — reserved (no run)

**NONPRODUCT.** Tracked development slot, not a product speed claim.
Not part of the public `gradus:*` install (`cista.toml` ships `src/`
only).

**Status**: pending. No CUDA comparator run. Every measurement cell
below is empty on purpose.

Named consumer: CAP-02 / ELP-06-era runs. This file exists so those
runs have a mirror to fill. Filling is not this unit.

Burgus comparator benches to date pin llama.cpp Metal and CPU rows
only (`llama-bench-*-metal.md`, `llama-bench-*-cpu.md`, and the
single-thread CPU sibling). There is no CUDA receipt here.

## Reserved rows

| Model | Engine | Prefill | Decode | Status |
| --- | --- | --- | --- | --- |
| SmolLM2-360M | llama.cpp CUDA | reserved | reserved | pending — no run |
| Qwen2.5-0.5B | llama.cpp CUDA | reserved | reserved | pending — no run |

No measured cell. No CUDA binary named. No host named as a CUDA
runner.
