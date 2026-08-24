#!/usr/bin/env python3
"""Generate and verify the frozen GEA2 layer-0 block activation fixture."""

from __future__ import annotations

import argparse
import hashlib
import json
import struct
from pathlib import Path

ROWS = 8
HIDDEN = 960
ELEMENTS = ROWS * HIDDEN
BYTE_COUNT = ELEMENTS * 4
GENERATOR = "fixtures/activations/gen_gea2_block.py"
VALUE_POLICY = (
    "little-endian IEEE-754 binary32; for flat index i in [0, "
    f"{ELEMENTS - 1}], f32(((((i mod 97)-48)*32)+((i mod 11)-5))/1024))"
)

HERE = Path(__file__).resolve().parent
FIXTURE = HERE / "gea2-block-input.bin"
MANIFEST = HERE / "gea2-block-input.manifest.json"


def values() -> list[float]:
    result: list[float] = []
    for index in range(ELEMENTS):
        numerator = ((index % 97) - 48) * 32 + ((index % 11) - 5)
        value = numerator / 1024.0
        result.append(struct.unpack("<f", struct.pack("<f", value))[0])
    return result


def fixture_bytes() -> bytes:
    return b"".join(struct.pack("<f", value) for value in values())


def manifest_for(data: bytes) -> dict[str, object]:
    return {
        "schema": "gea2-activation-manifest-v1",
        "generator": GENERATOR,
        "fixture": "fixtures/activations/gea2-block-input.bin",
        "bytes": len(data),
        "sha256": hashlib.sha256(data).hexdigest(),
        "dtype": "F32",
        "byte_order": "little",
        "shape": [ROWS, HIDDEN],
        "value_policy": VALUE_POLICY,
    }


def manifest_text(data: bytes) -> str:
    return json.dumps(manifest_for(data), indent=2, sort_keys=True) + "\n"


def check() -> int:
    expected = fixture_bytes()
    if not FIXTURE.is_file():
        print(f"missing fixture: {FIXTURE}")
        return 1
    observed = FIXTURE.read_bytes()
    if observed != expected:
        print("GEA2 activation fixture drift: bytes do not match the deterministic policy")
        return 1
    if len(observed) != BYTE_COUNT:
        print(f"GEA2 activation fixture drift: {len(observed)} bytes != {BYTE_COUNT}")
        return 1
    if not MANIFEST.is_file():
        print(f"missing activation manifest: {MANIFEST}")
        return 1
    try:
        observed_manifest = json.loads(MANIFEST.read_text())
    except json.JSONDecodeError as error:
        print(f"invalid activation manifest: {error}")
        return 1
    if observed_manifest != manifest_for(observed):
        print("GEA2 activation manifest drift")
        return 1
    print(
        f"GEA2 activation fixture OK: {len(observed)} bytes, "
        f"SHA-256 {hashlib.sha256(observed).hexdigest()}"
    )
    return 0


def generate() -> int:
    data = fixture_bytes()
    FIXTURE.write_bytes(data)
    MANIFEST.write_text(manifest_text(data))
    print(f"wrote {FIXTURE} ({len(data)} bytes)")
    print(f"wrote {MANIFEST}")
    return check()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="verify the committed fixture and manifest")
    args = parser.parse_args()
    return check() if args.check else generate()


if __name__ == "__main__":
    raise SystemExit(main())
