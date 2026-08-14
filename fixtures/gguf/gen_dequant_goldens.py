#!/usr/bin/env python3
"""GGUF-A3 C1 deterministic dequant goldens for the union codec set.

Mirrors llama.cpp `ggml/src/ggml-quants.c` @ `a957b7747` (the GI2-1 pin),
extending the `gi2-dequant-reference.py` semantics to the A3 union set
{F32, BF16, Q5_0, Q8_0, Q4_K, Q5_K, Q6_K}. This is the in-repo golden
authority for `gradus:model/dequant`:

  - the five SmolLM2-row types carry their real pinned-row blocks, embedded
    as committed constants from the GI2-1 goldens (read-only, cited);
  - BF16 and Q5_K have no real in-repo blocks (they come from the Qwen3.6
    artifact, operator evidence never committed), so their fixtures are
    deterministic crafted patterns that exercise every codec path;
  - all arithmetic is IEEE-754 f32 via numpy float32 (elementwise, no FMA),
    so outputs are bit-exact against the C kernels.

Outputs:
  - `fixtures/gguf/gguf-dequant-goldens.json` (schema
    `gguf-dequant-goldens-v2`): per-type block fixtures with `bytes_hex`
    and the expected f32 output as u32 LE bit hex (deterministic — reruns
    are byte-identical).

Requirements: Python 3.11+ with numpy. No model file is read.
"""
from __future__ import annotations

import hashlib
import json
import math
import sys
from pathlib import Path

import numpy as np

# ---------------------------------------------------------------------------
# Pinned block geometry (the A3 union set). GGML ids match ggml.h @ a957b7747.
# ---------------------------------------------------------------------------

TYPE_BLOCK = {
    0: (1, 4),      # F32   1 elem / 4 bytes
    30: (1, 2),     # BF16  1 elem / 2 bytes
    6: (32, 22),    # Q5_0  32 elems / 22 bytes
    8: (32, 34),    # Q8_0  32 elems / 34 bytes
    12: (256, 144),  # Q4_K  256 elems / 144 bytes
    13: (256, 176),  # Q5_K  256 elems / 176 bytes
    14: (256, 210),  # Q6_K  256 elems / 210 bytes
}
TYPE_NAME = {0: "F32", 30: "BF16", 6: "Q5_0", 8: "Q8_0", 12: "Q4_K", 13: "Q5_K", 14: "Q6_K"}

# Real pinned-row blocks per type (read-only from gi2-dequant-goldens.json):
# (tensor name, [block indices]).
REAL_BLOCKS = {
    "F32": [("output_norm.weight", [0, 479, 959])],
    "Q5_0": [("blk.0.attn_q.weight", [0, 14400, 28799])],
    "Q8_0": [("blk.0.attn_v.weight", [0, 4800, 9599])],
    "Q4_K": [("blk.3.ffn_down.weight", [0, 4800, 9599])],
    "Q6_K": [("blk.0.ffn_down.weight", [0, 4800, 9599])],
}

# The committed real block bytes (embedded so the generator stays in-repo).
REAL_BLOCK_BYTES = {
    ("F32", 0): "0000a63f",
    ("F32", 479): "0000ad3f",
    ("F32", 959): "00009e3f",
    ("Q5_0", 0): "082b776d3eb82000216f3310d0fee40ef0321c11f20a",
    ("Q5_0", 14400): "6624b74d8c01b2f0133fd4d6df23551f40d3edfff1fd",
    ("Q5_0", 28799): "4b23dfb32a670160b011954b37c760342e758611bfd8",
    ("Q8_0", 0): "7f13b2ef0081cff90a0316cfc70aea841ae908f1330d18e1cdce2309ffed0f33eba8",
    ("Q8_0", 4800): "851263f1da9cf6d2ebd0873560340d6310812113a440d0cbeed9f30c14b81c58debe",
    ("Q8_0", 9599): "431129cc4474e005fe11040ff1440f051df60c5cc8019dfd097feafbdbe415fae720",
    ("Q4_K", 0): "d313061feeeeebb1deeae7f4f0dc9fba616490a534764895103c45f2a0755018b625704807e75575a6238537cf558a8bc7b245be6a529ee336a8f7a240a5f66f636692496248a4e98854237c6890b706f859464d4b76cf8f8069388651adf90c1d987a8a7c79769a66482a6c8c8477aeb6b8e9d7f991c5c61c6493b5b6579384cab658a587d5c8f257408686af9a7808",
    ("Q4_K", 4800): "67149f205fb9e2a862aee3ecbe3eff5d6ea90437296b6e5a8a8b3688967c643b895c9abee38f4a2b8b30786f9c766547ed758af0afb7860ccbd0e97ccbb7ea5d9699c6efb77299fe9a4f5e9590776ab65c66e4766d867678b0385a1f906ae93326651a691957376b2d9843a74b067d4fbb783968e88aea8a6fca978984b8abaef7c6724cb85a880b766dd0d248c2c8b7",
    ("Q4_K", 9599): "5b143d1fb6aeeddbb3f6f8de9619ffd6956162d8844c643278f047777e9646c435f74306987993d7ab338536ae98677695ac48e30e0722ae38f69698b8b7288ae38028a926cb178768849a598af5951414867c57f554639b76d264c8a03c57dd96577f5acca2c875489b6e8c07a7a5684537b5b39fa599b4da05907667a164ba335467d759a7525964eaa3b486777336",
    ("Q6_K", 0): "7178301afd633afba620a8d9c9f92fc804c2aff4cc39f5fdd3fa07fe7d3ce1de022a6df86940cf33663508bc8c11acb2a0af8868d7471c1bc407a45d2db42e1143501d79084707eb01bcd97d5ed7b28a7322de9c81b1a10d418b635bbd9c05b5e1793292417fd00936859e99dd4805e0f5a2138f0568306bda404150a3871fe52f734a4ce676a1c9a8ec9488aac2e55861d995a952da86124dc901e95a4498a8e6743a594a99a257b2c74cb06a471d206e9959612e5099c5579a4e528d4ee9663d83ae42453cb2803fa1cf5cb03043756787",
    ("Q6_K", 4800): "2d0ec7b40ad5fa04a53b54cae1ec1bb0bd849f3c711a20ff8dc395a723d9b64ed80e363cb1360aa463bbdd11dbd32ed5ebef83264b2132662a3143094d19df602fa0b00cdceab54004717d2de11473e5a9db0a7245a9c77d0dc3f4b3d09dadd3001caa02efe58d3ec98315688789aa84450216ae0efc6d9051c7c88496476ba459b6aaa5434716829543a7509899c2d9656b9291b08a6e7198a6dea6aa3a65a1627da46da954f2ab451a19ba8646aa4a9c216a27d490959d816f7a9f68caaa53bd60bdaca7a1b2809b509da5ba4f41a6b706",
    ("Q6_K", 9599): "cf615ea1b1921894e648c7b42fa61d300187de78e8a281ef673092c017903888ed432bcb0bee8d13ccc881e9d00b8fe111081deb1ced06e218da5c9524fc0140cc44080afd90f885b0020396ea11caae07b89694519f54da96103e5e52ee0cf0e1ffbffe7a00c4651173da60914802fda84087bf0e909ee923aebac37d520cc8849eaa9a1065a69e555d772220a9086c411ac495595bb88cf761645aedcc5cb70832e125f98ba66616a9769dd288a85d8621b7c310793551968bb628f35ae4afb759a3a3a44a899a687083806db659999705",
}

# ---------------------------------------------------------------------------
# GGML half -> f32 (exact IEEE-754 binary16 -> binary32 mapping)
# ---------------------------------------------------------------------------

def half_to_f32(bits: int) -> np.float32:
    sign = (bits >> 15) & 0x1
    exp = (bits >> 10) & 0x1F
    frac = bits & 0x3FF
    if exp == 0:
        value = frac * 2.0 ** -24 if frac else 0.0
    elif exp == 0x1F:
        value = math.inf if frac == 0 else math.nan
    else:
        value = (1.0 + frac / 1024.0) * 2.0 ** (exp - 15)
    return np.float32(-value if sign else value)


# ---------------------------------------------------------------------------
# GGML bf16 -> f32. Value arithmetic is bit-exact for every bf16 (8-bit
# exponent, 7-bit mantissa — exactly representable in f32; matches
# llama.cpp's `ggml_compute_bf16_to_fp32`, `bits << 16`).
# ---------------------------------------------------------------------------

def bf16_to_f32(bits: int) -> np.float32:
    sign = (bits >> 15) & 0x1
    exp = (bits >> 7) & 0xFF
    frac = bits & 0x7F
    if exp == 0:
        value = frac * 2.0 ** -133 if frac else 0.0
    elif exp == 0xFF:
        value = math.inf if frac == 0 else math.nan
    else:
        value = (1.0 + frac / 128.0) * 2.0 ** (exp - 127)
    return np.float32(-value if sign else value)


# ---------------------------------------------------------------------------
# GGML block dequant kernels (mirror llama.cpp dequantize_row_* exactly)
# ---------------------------------------------------------------------------

def get_scale_min_k4(j: int, scales: bytes) -> tuple[int, int]:
    """llama.cpp get_scale_min_k4: 6-bit scale + 6-bit min from scales[12]."""
    if j < 4:
        return scales[j] & 63, scales[j + 4] & 63
    d = (scales[j + 4] & 0x0F) | ((scales[j - 4] >> 6) << 4)
    m = (scales[j + 4] >> 4) | ((scales[j] >> 6) << 4)
    return d, m


def dequant_q8_0(blk: bytes) -> np.ndarray:
    d = half_to_f32(int.from_bytes(blk[0:2], "little"))
    qs = np.frombuffer(blk[2:34], dtype=np.int8).astype(np.float32)
    return qs * d


def dequant_q5_0(blk: bytes) -> np.ndarray:
    d = half_to_f32(int.from_bytes(blk[0:2], "little"))
    qh = int.from_bytes(blk[2:6], "little")
    qs = np.frombuffer(blk[6:22], dtype=np.uint8)
    j = np.arange(16, dtype=np.int64)
    xh0 = ((qh >> j) << 4) & 0x10
    xh1 = (qh >> (j + 12)) & 0x10
    x0 = ((qs & 0x0F).astype(np.int32) | xh0.astype(np.int32)) - 16
    x1 = ((qs >> 4).astype(np.int32) | xh1.astype(np.int32)) - 16
    y = np.empty(32, dtype=np.float32)
    y[0:16] = x0.astype(np.float32) * d
    y[16:32] = x1.astype(np.float32) * d
    return y


def dequant_q4_k(blk: bytes) -> np.ndarray:
    d = half_to_f32(int.from_bytes(blk[0:2], "little"))
    dmin = half_to_f32(int.from_bytes(blk[2:4], "little"))
    scales = blk[4:16]
    qs = np.frombuffer(blk[16:144], dtype=np.uint8)
    y = np.empty(256, dtype=np.float32)
    is_ = 0
    for j in range(0, 256, 64):
        sc0, m0 = get_scale_min_k4(is_, scales)
        d1 = d * np.float32(sc0)
        m1 = dmin * np.float32(m0)
        sc1, m1b = get_scale_min_k4(is_ + 1, scales)
        d2 = d * np.float32(sc1)
        m2 = dmin * np.float32(m1b)
        q = qs[j // 2 : j // 2 + 32]
        y[j : j + 32] = d1 * (q & 0x0F).astype(np.float32) - m1
        y[j + 32 : j + 64] = d2 * (q >> 4).astype(np.float32) - m2
        is_ += 2
    return y


def dequant_q5_k(blk: bytes) -> np.ndarray:
    """block_q5_K: d (half), dmin (half), scales[12], qh[32], qs[128].

    Per 64-element chunk (index c): d1 = d·sc(is), m1 = dmin·m(is),
    d2 = d·sc(is+1), m2 = dmin·m(is+1); the 5th bit of the low nibble is
    qh[l] bit 2c, of the high nibble qh[l] bit 2c+1.
    """
    d = half_to_f32(int.from_bytes(blk[0:2], "little"))
    dmin = half_to_f32(int.from_bytes(blk[2:4], "little"))
    scales = blk[4:16]
    qh = blk[16:48]
    qs = blk[48:176]
    y = np.empty(256, dtype=np.float32)
    is_ = 0
    for chunk in range(4):
        sc0, m0 = get_scale_min_k4(is_ + 0, scales)
        d1 = d * np.float32(sc0)
        m1 = dmin * np.float32(m0)
        sc1, m1b = get_scale_min_k4(is_ + 1, scales)
        d2 = d * np.float32(sc1)
        m2 = dmin * np.float32(m1b)
        for l in range(32):
            qs_val = qs[chunk * 32 + l]
            qh_val = qh[l]
            lo_hi = ((qh_val >> (2 * chunk)) & 1) << 4
            hi_hi = ((qh_val >> (2 * chunk + 1)) & 1) << 4
            qs16_lo = (qs_val & 0x0F) | lo_hi
            qs16_hi = (qs_val >> 4) | hi_hi
            y[chunk * 64 + l] = d1 * np.float32(qs16_lo) - m1
            y[chunk * 64 + 32 + l] = d2 * np.float32(qs16_hi) - m2
        is_ += 2
    return y


def dequant_q6_k(blk: bytes) -> np.ndarray:
    d = half_to_f32(int.from_bytes(blk[208:210], "little"))
    ql = np.frombuffer(blk[0:128], dtype=np.uint8)
    qh = np.frombuffer(blk[128:192], dtype=np.uint8)
    sc = np.frombuffer(blk[192:208], dtype=np.int8).astype(np.int32)
    y = np.empty(256, dtype=np.float32)
    for n in (0, 128):
        sc_base = n // 16
        ql0 = n // 2
        qh0 = n // 4
        l = np.arange(32, dtype=np.int64)
        is_ = l // 16
        q1 = (ql[ql0 + l] & 0x0F) | (((qh[qh0 + l] >> 0) & 3) << 4)
        q2 = (ql[ql0 + l + 32] & 0x0F) | (((qh[qh0 + l] >> 2) & 3) << 4)
        q3 = (ql[ql0 + l] >> 4) | (((qh[qh0 + l] >> 4) & 3) << 4)
        q4 = (ql[ql0 + l + 32] >> 4) | (((qh[qh0 + l] >> 6) & 3) << 4)
        q1 = q1.astype(np.int32) - 32
        q2 = q2.astype(np.int32) - 32
        q3 = q3.astype(np.int32) - 32
        q4 = q4.astype(np.int32) - 32
        sc0 = sc[sc_base + is_ + 0].astype(np.float32)
        sc2 = sc[sc_base + is_ + 2].astype(np.float32)
        sc4 = sc[sc_base + is_ + 4].astype(np.float32)
        sc6 = sc[sc_base + is_ + 6].astype(np.float32)
        y[n + l + 0] = d * sc0 * q1.astype(np.float32)
        y[n + l + 32] = d * sc2 * q2.astype(np.float32)
        y[n + l + 64] = d * sc4 * q3.astype(np.float32)
        y[n + l + 96] = d * sc6 * q4.astype(np.float32)
    return y


def dequant_f32(blk: bytes) -> np.ndarray:
    return np.frombuffer(blk[:4], dtype="<f4")


def dequant_bf16(blk: bytes) -> np.ndarray:
    return np.asarray([bf16_to_f32(int.from_bytes(blk[0:2], "little"))], dtype="<f4")


DEQUANT = {
    0: dequant_f32,
    30: dequant_bf16,
    6: dequant_q5_0,
    8: dequant_q8_0,
    12: dequant_q4_k,
    13: dequant_q5_k,
    14: dequant_q6_k,
}


def dequant_block(ggml_type: int, blk: bytes) -> np.ndarray:
    return DEQUANT[ggml_type](blk)


# ---------------------------------------------------------------------------
# Adversarial / deterministic crafted block fixtures (finite values only —
# NaN halves fail closed by contract and are covered by the proba gates).
# ---------------------------------------------------------------------------

ADVERSARIAL = {
    "F32": [
        ("positive-zero", "00000000"),
        ("max-positive", "ffff7f7f"),
        ("max-negative", "ffff7fff"),
        ("min-subnormal", "01000000"),
        ("one", "0000803f"),
        ("negative-two", "000000c0"),
        ("pi", "db0f4940"),
    ],
    "BF16": [
        ("zero", "0000"),
        ("negative-zero", "0080"),
        ("one", "803f"),
        ("half", "003f"),
        ("max-finite", "7f7f"),
        ("min-subnormal", "0100"),
        ("positive-inf", "807f"),
        ("negative-inf", "80ff"),
        ("negative-one", "80bf"),
        ("negative-max-finite", "7fff"),
    ],
    "Q5_0": [
        ("zeroes", "00" * 22),
        ("max-scale-qh-ones", "ff7b" + "ffffffff" + "ff" * 16),
        ("subnormal-mixed-qh", "0100" + "00ff00ff" + "0010f00fabcdef1234567890aabbccdd"),
        ("negative-d-qh-low", "00c0" + "ffff0000" + "ff" * 16),
    ],
    "Q8_0": [
        ("zeroes", "00" * 34),
        ("max-scale-int8-extremes", "ff7b" + "00017f80fffe40bf" * 4),
        ("subnormal-descending", "0100" + "7f7e7d7c7b7a7978" + "8081fffe" * 6),
        ("negative-d", "00c0" + "807f01ff" * 8),
    ],
    "Q4_K": [
        ("zeroes", "00" * 144),
        ("max-scale-ones", "ff7b" + "0080" + "3f" * 12 + "ff" * 128),
        ("subnormal-scales", "0100" + "0300" + "00013f202a15003f05300f00" + ("00f00fff" * 32)),
        ("negative-d-scale-highbits", "00bc" + "003c" + "ff7fbf3f3c2d1e0f3f2a1500" + (bytes(range(128)).hex())),
    ],
    "Q5_K": [
        ("zeroes", "00" * 176),
        ("max-scale-ones", "ff7b" + "0080" + "3f" * 12 + "ff" * 32 + "ff" * 128),
        ("subnormal-mixed", "0100" + "0300" + "00013f202a15003f05300f00" + ("00f00fff" * 8) + (bytes(range(128)).hex())),
        ("negative-d-highbits", "00bc" + "003c" + "ff7fbf3f3c2d1e0f3f2a1500" + "ffffffff" * 8 + ("00112233" * 32)),
    ],
    "Q6_K": [
        ("zeroes", "00" * 210),
        ("max-scale-ones", "ff" * 128 + "ff" * 64 + "7f" * 16 + "ff7b"),
        ("subnormal-negative-scales", "001155aaff" * 25 + "001155" + "0055aaff" * 16
         + "7f00ff80017eff7f8080810203fc7d01" + "0100"),
        ("negative-subnormal-d", "aa" * 128 + "55" * 64 + "7f80017e8081027f7f8180ff02010304" + "0180"),
    ],
}


# ---------------------------------------------------------------------------
# Golden emission
# ---------------------------------------------------------------------------

def f32_hex(arr: np.ndarray) -> list[str]:
    arr = np.asarray(arr, dtype="<f4")
    return [f"{int(b):08x}" for b in arr.view("<u4").tolist()]


def main() -> int:
    out = Path(__file__).resolve().parent / "gguf-dequant-goldens.json"

    block_fixtures = []
    for ggml_type, type_name in TYPE_NAME.items():
        block_elems, block_bytes = TYPE_BLOCK[ggml_type]
        # Real pinned-row blocks (five SmolLM2-row types).
        for tensor_name, indices in REAL_BLOCKS.get(type_name, []):
            for idx in indices:
                hexstr = REAL_BLOCK_BYTES[(type_name, idx)]
                blk = bytes.fromhex(hexstr)
                assert len(blk) == block_bytes, f"{type_name} block {idx} size"
                block_fixtures.append(
                    {
                        "type": type_name,
                        "name": f"real {tensor_name} block {idx}",
                        "source": "real",
                        "tensor": tensor_name,
                        "block_index": idx,
                        "bytes_hex": hexstr,
                        "output_hex": f32_hex(dequant_block(ggml_type, blk)),
                    }
                )
        # Adversarial / crafted patterns (all seven types; the golden
        # contract — NaN fails closed — is proba-covered, not a golden).
        for name, hexstr in ADVERSARIAL.get(type_name, []):
            blk = bytes.fromhex(hexstr)
            assert len(blk) == block_bytes, f"{type_name} {name}: wrong byte count"
            block_fixtures.append(
                {
                    "type": type_name,
                    "name": f"adversarial {name}",
                    "source": "adversarial",
                    "bytes_hex": hexstr,
                    "output_hex": f32_hex(dequant_block(ggml_type, blk)),
                }
            )

    golden = {
        "schema": "gguf-dequant-goldens-v2",
        "purpose": "cpu-oracle",
        "transform": {
            "impl": "ggml/src/ggml-quants.c",
            "commit": "a957b7747",
        },
        "generator": {
            "script": "gen_dequant_goldens.py",
            "python": sys.version.split()[0],
            "numpy": np.__version__,
        },
        "sha256": hashlib.sha256(json.dumps(block_fixtures, sort_keys=True).encode()).hexdigest(),
        "block_fixtures": block_fixtures,
    }
    out.write_text(json.dumps(golden, indent=2) + "\n")
    print(f"wrote {out} ({len(block_fixtures)} block fixtures)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
