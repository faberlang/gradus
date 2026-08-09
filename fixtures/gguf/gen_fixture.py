#!/usr/bin/env python3
"""PML2-U3 — GGUF legal fixture generator (smollm2-360m-scaled-row.gguf).

Deterministic. Produces the byte-identical GGUF v3 file that the proba
`gradus/src/model/gguf.proba` reconstructs in code (its `aedifica`
builder) and that the oracle `gguf-row-oracle.md` pins (SHA-256, byte
size). Any change to the structure below MUST update the oracle document
and the proba constants together (a re-pin is an operator decision per
CAMPAIGN stop conditions).

The file is a scaled STRUCTURAL replica of the pinned row
SmolLM2-360M-Instruct-Q4_K_M (gi0-model-contract v1.0.0): the admitted
metadata VALUES are pinned verbatim (arch llama / 32 / 8192 / 49152 /
960, gpt2/smollm tokenizer, file_type 15, quant version 2); the tensor
inventory is scaled (3 tensors) so the proba proves the admission RULES,
not the 270 MB row. Exact GGML block layouts are used (Q8_0 32/34,
F32 1/4, Q4_K 256/144); every tensor byte size is a 32-multiple (the
pinned row's property), so the data region tiles exactly with no
per-tensor padding.

GGUF v3 layout (pinned toolchain llama.cpp a957b7747 / gguf-py):
  header:  "GGUF" | u32 version | u64 tensor_count | u64 kv_count
  metadata KVs; tensor info table; data section at align32(table end);
  each tensor's stored offset is RELATIVE to the data-section start and
  equals the cumulative byte size of the preceding tensors.
"""

import struct

MAGIC = b"GGUF"
VERSION = 3

# KV codec: ("key", "type", "value"); type s=string, u=u32, b=bool,
# as=array-of-string. Order matters (must match the proba's LEGAL_KVS).
KVS = [
    ("general.architecture", "s", "llama"),
    ("general.file_type", "u", "15"),
    ("general.quantization_version", "u", "2"),
    ("llama.block_count", "u", "32"),
    ("llama.context_length", "u", "8192"),
    ("llama.vocab_size", "u", "49152"),
    ("llama.embedding_length", "u", "960"),
    ("tokenizer.ggml.model", "s", "gpt2"),
    ("tokenizer.ggml.pre", "s", "smollm"),
    ("tokenizer.ggml.bos_token_id", "u", "1"),
    ("tokenizer.ggml.eos_token_id", "u", "2"),
    ("tokenizer.ggml.padding_token_id", "u", "2"),
    ("tokenizer.ggml.unknown_token_id", "u", "0"),
    ("tokenizer.ggml.add_bos_token", "b", "0"),
    ("tokenizer.ggml.add_space_prefix", "b", "0"),
    ("general.name", "s", "smollm2-fixture"),
    ("tokenizer.chat_template", "s", "You are a helpful AI assistant named SmolLM"),
    ("general.languages", "as", "en"),
]

# Tensor codec: (name, ggml_type_id, dims, offset). Offsets are relative
# to the data-section start and must equal the running cumulative size.
# Q8_0 [32,16] = 512 elems = 544 B; F32 [16] = 64 B; Q4_K [256,16] =
# 4096 elems = 2304 B; total 2912 B.
TENSORS = [
    ("token_embd.weight", 8, [32, 16], "auto"),
    ("blk.0.attn_norm.weight", 0, [16], "auto"),
    ("blk.0.ffn_down.weight", 12, [256, 16], "auto"),
]

# GGML block layout (pinned ggml-common.h): type_id -> (elems, bytes).
BLOCK_LAYOUT = {0: (1, 4), 6: (32, 22), 8: (32, 34), 12: (256, 144), 14: (256, 210)}
ALIGNMENT = 32


def u64(n):
    return struct.pack("<Q", n)


def u32(n):
    return struct.pack("<I", n)


def sstr(s):
    data = s.encode("utf-8")
    return u64(len(data)) + data


def tensor_bytes(name, typo, dims):
    elems = 1
    for d in dims:
        elems *= d
    blocci, octeti = BLOCK_LAYOUT[typo]
    assert elems % blocci == 0, f"tensor {name} not a block multiple"
    nbytes = (elems // blocci) * octeti
    assert nbytes % ALIGNMENT == 0, f"tensor {name} not 32-aligned"
    return nbytes


def kv_bytes(key, typo, value):
    if typo == "s":
        return sstr(key) + u32(8) + sstr(value)
    if typo == "u":
        return sstr(key) + u32(4) + u32(int(value))
    if typo == "b":
        return sstr(key) + u32(7) + bytes([int(value)])
    if typo == "as":
        elems = value.split(",")
        body = u32(8) + u64(len(elems))
        for e in elems:
            body += sstr(e)
        return sstr(key) + u32(9) + body
    raise ValueError(f"unknown kv type {typo}")


def build():
    f = bytearray()
    f += MAGIC
    f += u32(VERSION)
    f += u64(len(TENSORS))
    f += u64(len(KVS))
    for kv in KVS:
        f += kv_bytes(*kv)

    # Tensor info table (offsets are cumulative relative to data start).
    cursor = 0
    for (name, typo, dims, offset) in TENSORS:
        if offset == "auto":
            off_val = cursor
        else:
            off_val = int(offset)
        f += sstr(name)
        f += u32(len(dims))
        for d in dims:
            f += u64(d)
        f += u32(typo)
        f += u64(off_val)
        cursor += tensor_bytes(name, typo, dims)

    # Data section at align32(end of table); deterministic pattern.
    while len(f) % ALIGNMENT != 0:
        f += b"\x00"
    total = sum(tensor_bytes(*t[:3]) for t in TENSORS)
    for k in range(total):
        f.append((k * 13 + 7) % 256)
    return bytes(f)


def main():
    out = build()
    out_path = "smollm2-360m-scaled-row.gguf"
    with open(out_path, "wb") as fh:
        fh.write(out)
    import hashlib

    print(f"wrote {out_path}: {len(out)} bytes")
    print(f"sha256 {hashlib.sha256(out).hexdigest()}")


if __name__ == "__main__":
    main()
