#!/usr/bin/env python3
"""Generate the bounded GGUF-A1a manifest fixtures.

The files are small, deterministic GGUF v3 artifacts.  The parser receives
only each file's prefix through the end of its tensor table (including any
alignment padding); the generated data region remains an external source
fixture for later range-source work.  The oracle records both the complete
artifact and the exact parser corpus boundary.
"""

from __future__ import annotations

import hashlib
import struct
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def u32(value: int) -> bytes:
    return struct.pack("<I", value)


def u64(value: int) -> bytes:
    return struct.pack("<Q", value)


def gguf_string(value: str) -> bytes:
    encoded = value.encode("utf-8")
    return u64(len(encoded)) + encoded


def metadata_value(kind: int, value: object) -> bytes:
    if kind == 4:  # UINT32
        return u32(int(value))
    if kind == 8:  # STRING
        return gguf_string(str(value))
    if kind == 9:  # ARRAY
        values = list(value)  # type: ignore[arg-type]
        return u32(8) + u64(len(values)) + b"".join(gguf_string(str(item)) for item in values)
    raise ValueError(f"unsupported fixture metadata kind {kind}")


@dataclass(frozen=True)
class Tensor:
    name: str
    ggml_type: int
    shape: tuple[int, ...]
    offset: int
    stored_bytes: int | None


@dataclass(frozen=True)
class Fixture:
    name: str
    alignment: int | None
    metadata: tuple[tuple[str, int, object], ...]
    tensors: tuple[Tensor, ...]
    data_bytes: int


FIXTURES = (
    Fixture(
        name="llama-manifest-v3",
        alignment=None,
        metadata=(
            ("general.architecture", 8, "llama"),
            ("general.name", 8, "a1a-llama"),
            ("general.custom_note", 8, "unknown metadata is retained"),
            ("tokenizer.ggml.tokens", 9, ("<s>", "hello", "world")),
        ),
        tensors=(
            Tensor("token_embd.weight", 0, (4, 8), 0, 128),
            Tensor("blk.0.attn_norm.weight", 1, (8,), 160, 16),
        ),
        data_bytes=176,
    ),
    Fixture(
        name="qwen2-manifest-v3",
        alignment=64,
        metadata=(
            ("general.architecture", 8, "qwen2"),
            ("general.name", 8, "a1a-qwen2"),
            ("qwen2.custom_flag", 4, 7),
            ("tokenizer.ggml.tokens", 9, ("<|endoftext|>", "hello", "world")),
        ),
        tensors=(
            Tensor("blk.0.attn_q.weight", 12, (1, 1, 256), 0, 144),
            Tensor("blk.0.attn_norm.weight", 0, (2, 2), 192, 16),
        ),
        data_bytes=208,
    ),
    Fixture(
        name="qwen35moe-manifest-v3",
        alignment=128,
        metadata=(
            ("general.architecture", 8, "qwen35moe"),
            ("general.name", 8, "a1a-qwen35moe"),
            ("qwen35moe.custom_flag", 4, 35),
            ("tokenizer.ggml.tokens", 9, ("<|im_start|>", "hello", "world")),
        ),
        tensors=(
            Tensor("blk.0.experts.0.weight", 999, (2, 3, 4), 0, None),
            Tensor("blk.0.attn_norm.weight", 30, (2, 2), 64, 8),
        ),
        data_bytes=72,
    ),
)


def build(fixture: Fixture) -> tuple[bytes, int, int]:
    table = bytearray(b"GGUF" + u32(3) + u64(len(fixture.tensors)) + u64(len(fixture.metadata)))
    metadata = list(fixture.metadata)
    if fixture.alignment is not None:
        metadata.insert(1, ("general.alignment", 4, fixture.alignment))
    table[16:24] = u64(len(metadata))
    for key, kind, value in metadata:
        table.extend(gguf_string(key))
        table.extend(u32(kind))
        table.extend(metadata_value(kind, value))

    for tensor in fixture.tensors:
        table.extend(gguf_string(tensor.name))
        table.extend(u32(len(tensor.shape)))
        for dimension in tensor.shape:
            table.extend(u64(dimension))
        table.extend(u32(tensor.ggml_type))
        table.extend(u64(tensor.offset))

    alignment = fixture.alignment or 32
    data_offset = (len(table) + alignment - 1) // alignment * alignment
    corpus = bytes(table) + bytes(data_offset - len(table))
    data = bytes((index * 17 + 11) % 256 for index in range(fixture.data_bytes))
    artifact = corpus + data
    return artifact, len(table), data_offset


def main() -> None:
    oracle_lines = [
        "# GGUF-A1a General Manifest Fixture Oracle",
        "",
        "**Generator**: `python3 fixtures/gguf/gen_manifest_fixtures.py`",
        "**Contract**: three deterministic GGUF v3 files; parser input is the",
        "prefix through the table-alignment boundary, never the data region.",
        "",
        "| Fixture | Architecture | Alignment | Rank coverage | Known/unknown types | Artifact bytes | Corpus bytes | Data offset | SHA-256 |",
        "| --- | --- | ---: | --- | --- | ---: | ---: | ---: | --- |",
    ]
    detail_lines: list[str] = []
    for fixture in FIXTURES:
        artifact, table_end, data_offset = build(fixture)
        path = ROOT / f"{fixture.name}.gguf"
        path.write_bytes(artifact)
        digest = hashlib.sha256(artifact).hexdigest()
        architecture = next(value for key, kind, value in fixture.metadata if key == "general.architecture")
        ranks = ",".join(str(len(tensor.shape)) for tensor in fixture.tensors)
        types = ",".join(str(tensor.ggml_type) for tensor in fixture.tensors)
        oracle_lines.append(
            f"| `{path.name}` | `{architecture}` | `{fixture.alignment or 32}` | `{ranks}` | `{types}` | {len(artifact)} | {data_offset} | {data_offset} | `{digest}` |"
        )
        detail_lines.append(f"- `{path.name}` table ends at byte `{table_end}`; alignment padding is included in the `{data_offset}`-byte parser corpus.")
        detail_lines.append("  The complete artifact then contains only the small synthetic data region; no model payload or local path is committed.")
    oracle_lines.extend(
        [
            "",
            *detail_lines,
            "",
            "The llama fixture omits `general.alignment`, proving the GGUF default",
            "of 32.  The Qwen2 fixture supplies 64 and carries a rank-3 Q4_K tensor.",
            "The Qwen35MoE fixture supplies 128, carries a rank-3 tensor with raw",
            "type `999`, and includes a known BF16 tensor; the unknown codec remains",
            "inspectable rather than becoming a parser error.",
            "",
            "The generator is deterministic.  Regeneration must be byte-for-byte",
            "identical for all three files and this oracle.",
            "",
        ]
    )
    (ROOT / "general-manifest-oracle.md").write_text("\n".join(oracle_lines), encoding="utf-8")


if __name__ == "__main__":
    main()
