# GEA1 selected Safetensors range — SmolLM2 V projection

This note records the bounded source row used by GEA1-U2. The model file stays
outside Git.

| Fact | Pinned value |
| --- | --- |
| Source revision | `HuggingFaceTB/SmolLM2-360M-Instruct` at `a10cc1512eabd3dde888204e902eca88bddb4951` |
| File | `/Users/ianzepp/ai/models/hf/HuggingFaceTB/SmolLM2-360M-Instruct/a10cc1512eabd3dde888204e902eca88bddb4951/model.safetensors` |
| File length | `723674912` bytes |
| Whole-file SHA-256 | `e6bffe7435d7ddc10fd3b9a9efd429dafbacb1cb17015fb5562664e7532bf86e` |
| Header length prefix | `32664` bytes, little-endian u64 |
| Data-region absolute start | `8 + 32664 = 32672` |
| Tensor | `model.layers.0.self_attn.v_proj.weight` |
| Storage dtype | `BF16` |
| Logical shape | `[320, 960]` |
| Logical values | `320 * 960 = 307200` |
| Relative `data_offsets` | `[113422080, 114036480]` |
| Selected byte length | `614400` bytes (`307200 * 2`) |
| Absolute byte range | `[113454752, 114069152)` |
| Expanded logical SHA-256 | `ff7bb3f6c066a4d125038f3a6b392d1a6fecd8942c6d9894692f714ea2564f34` |

The range was derived directly from the pinned Safetensors header:

```text
header_size = little_endian_u64(file[0..8]) = 32664
header_end = 8 + header_size = 32672
data_offsets(model.layers.0.self_attn.v_proj.weight) = [113422080, 114036480]
absolute = [header_end + 113422080, header_end + 114036480)
       = [113454752, 114069152)
```

The Gradus handoff receives only the declared `[113454752,114069152)` range
and its typed descriptor facts. It does not receive the path, the file, a
whole-file byte list, or a container object. The kernel module has no
Safetensors knowledge.
