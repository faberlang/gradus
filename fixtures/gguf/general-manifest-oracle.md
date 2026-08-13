# GGUF-A1a General Manifest Fixture Oracle

**Generator**: `python3 fixtures/gguf/gen_manifest_fixtures.py`
**Contract**: three deterministic GGUF v3 files; parser input is the
prefix through the table-alignment boundary, never the data region.

| Fixture | Architecture | Alignment | Rank coverage | Known/unknown types | Artifact bytes | Corpus bytes | Data offset | SHA-256 |
| --- | --- | ---: | --- | --- | ---: | ---: | ---: | --- |
| `llama-manifest-v3.gguf` | `llama` | `32` | `2,1` | `0,1` | 560 | 384 | 384 | `68a950bb21b44d93f52136cbfcf561796cdd8f1105edc35ddbab957a413dd38b` |
| `qwen2-manifest-v3.gguf` | `qwen2` | `64` | `3,2` | `12,0` | 656 | 448 | 448 | `3eb06b43263bb7ef9caf5e7993c74c74d2f5fc2c9d931935c60dc8a802caa7df` |
| `qwen35moe-manifest-v3.gguf` | `qwen35moe` | `128` | `3,2` | `999,30` | 584 | 512 | 512 | `0569265f0ff43f9de50ee067af182ef21cc1242ab6fd0fa940e6a9c4b7676d48` |

- `llama-manifest-v3.gguf` table ends at byte `370`; alignment padding is included in the `384`-byte parser corpus.
  The complete artifact then contains only the small synthetic data region; no model payload or local path is committed.
- `qwen2-manifest-v3.gguf` table ends at byte `397`; alignment padding is included in the `448`-byte parser corpus.
  The complete artifact then contains only the small synthetic data region; no model payload or local path is committed.
- `qwen35moe-manifest-v3.gguf` table ends at byte `411`; alignment padding is included in the `512`-byte parser corpus.
  The complete artifact then contains only the small synthetic data region; no model payload or local path is committed.

The llama fixture omits `general.alignment`, proving the GGUF default
of 32.  The Qwen2 fixture supplies 64 and carries a rank-3 Q4_K tensor.
The Qwen35MoE fixture supplies 128, carries a rank-3 tensor with raw
type `999`, and includes a known BF16 tensor; the unknown codec remains
inspectable rather than becoming a parser error.

The generator is deterministic.  Regeneration must be byte-for-byte
identical for all three files and this oracle.
