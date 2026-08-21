# Start here

Install and library-home setup live in the [README](../README.md#install).
This page is the first-time path after that: a smallest useful program, then
which demo to open for each capability.

## Architecture

Gradus is a JAX-shaped autograd and ML library: models are pure functions
with explicit parameters, reverse-mode gradients are compiler-generated
companion functions rather than a runtime tape, and public types are
device-neutral contracts. Foundation modules (`gradus:dtype`, `gradus:shape`,
`gradus:tensor`, `gradus:math`) feed loss, optimizers, and neural-network
primitives; those compose into attention and transformer blocks;
model-admission modules bind GGUF and Safetensors artifacts into typed
capsules without retaining paths or whole-model payloads; decode, cache,
sampling, and generation sit on the same forward row. Import the leaf that
owns the type you use (`gradus:loss`, `gradus:nn`,
`gradus:model/gguf_manifest`) — the façade does not re-export genera.

## Smallest useful program

The smallest useful Gradus program builds two 2×2 tensors and evaluates mean
squared error. Put this in an empty directory with `FABER_LIBRARY_HOME` set
as in the README, and a current `faber` binary on `PATH`.

`faber.toml`:

```toml
[package]
name = "hello-gradus"
version = "0.1.0"
edition = "2026"

[paths]
source = "src"
entry = "main.fab"

[build]
target = "fmir"
kind = "bin"

[locale]
locale = "en"
```

`src/main.fab`:

```fab
import from "gradus:loss" loss

main {
    const tensor<f32, []> seed ← empty
    const list<int> shape_2x2 ← [2, 2]
    const tensor<f32, [2, 2]> prediction ← seed.from_flat([1.0, 2.0, 3.0, 4.0], shape_2x2)
    const tensor<f32, [2, 2]> target ← seed.from_flat([1.0, 2.0, 3.0, 3.0], shape_2x2)
    const f32 value ← loss.mse_2x2(prediction, target)
    print value
}
```

```bash
faber check .
```

`loss.mse_2x2` is mean squared error over a 2×2 f32 pair; these inputs yield
`0.25`. `faber check` is the standing proof that the import and call
type-check. The training-loop package proof runs its library-to-library calls
on the FMIR stepper (radix `43c0102ba`, regression-locked by `2e8042ae7`).
This quickstart does not claim every package run, GPU training, or executed
model performance.

## First runnable exemplum

Then open [`exempla/dense-rmsnorm/`](../exempla/dense-rmsnorm/). It is an
in-memory RMSNorm row over `gradus:nn`: no model file, no device handle.

```bash
faber check exempla/dense-rmsnorm
```

That command type-checks on this tree (`ok: …/exempla/dense-rmsnorm`). Read
the package README for the pinned values and evidence boundary.

## Learning path

The demos are ordinary Faber packages under `exempla/`. Start small:

1. [`dense-rmsnorm`](../exempla/dense-rmsnorm/) — RMSNorm (`gradus:nn`),
   in-memory, first type-check.
2. [`dense-swiglu`](../exempla/dense-swiglu/) — SiLU and the SwiGLU gated
   MLP.
3. [`dense-rope`](../exempla/dense-rope/) — rotary position embeddings
   (`gradus:attention`).
4. [`dense-gqa`](../exempla/dense-gqa/) — multi-head attention with grouped
   KV heads.
5. [`dense-block`](../exempla/dense-block/) — one dense transformer block
   composing the rows above (`gradus:transformer`).

After those, pick by capability in the tour below. Module ownership is in
the [module map](module-map.md).

## Examples tour

Open this first for each area. Every path is a directory under `exempla/`.

| Capability | Open first | Then |
| --- | --- | --- |
| Loss / typed tensors | the snippet above | [`gradient-seam`](../exempla/gradient-seam/) |
| Neural-network primitives | [`dense-rmsnorm`](../exempla/dense-rmsnorm/) | [`dense-swiglu`](../exempla/dense-swiglu/) |
| Attention | [`dense-rope`](../exempla/dense-rope/) | [`dense-gqa`](../exempla/dense-gqa/) |
| Transformer block | [`dense-block`](../exempla/dense-block/) | [`dense-model`](../exempla/dense-model/) |
| Autograd import | [`gradient-seam`](../exempla/gradient-seam/) | [`gradient-seam-nolib`](../exempla/gradient-seam-nolib/) (same arithmetic, no `gradus:*` import) |
| Training loop | [`training-loop-mlp`](../exempla/training-loop-mlp/) | — |
| GGUF format (in-memory) | [`gguf-manifest`](../exempla/gguf-manifest/) | [`gguf-materialize`](../exempla/gguf-materialize/) |
| GGUF format (local file) | [`gguf-inspect`](../exempla/gguf-inspect/) | needs an operator-local GGUF |
| Architecture adapter (llama / SmolLM2) | [`dense-llama-adapter`](../exempla/dense-llama-adapter/) | — |
| Architecture adapter (qwen2) | [`dense-qwen2-adapter`](../exempla/dense-qwen2-adapter/) | — |
| Dense model assembly | [`dense-model`](../exempla/dense-model/) | — |
| Real-model prefill | [`dense-prefill-smollm2`](../exempla/dense-prefill-smollm2/) | [`dense-prefill-qwen2`](../exempla/dense-prefill-qwen2/) (local weights) |
| Bounded generation (tiny decoder) | [`generate-route`](../exempla/generate-route/) | [`token-generation`](../exempla/token-generation/) |
| Real-model decode / generate | [`dense-decode-smollm2`](../exempla/dense-decode-smollm2/) | [`generate-smollm2`](../exempla/generate-smollm2/) (local weights) |
| Tokenizer identity | [`qwen36-35b-inference`](../exempla/qwen36-35b-inference/) | local artifact; tokenizer phase only |
| Mixture-of-experts admission | [`gguf-admit-qwen35moe`](../exempla/gguf-admit-qwen35moe/) | local artifact; admission, not inference |

Several primitive packages have historically printed in-memory PASS rows
through package MIR. Treat those receipts as package-local. Real-file
demos need a GGUF the repo does not ship. Per-package READMEs state the
evidence boundary.
