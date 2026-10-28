#!/usr/bin/env python3
# Independent f64 reference for the dense-decode-bench-metal oracle pins.
#
# Evaluates the documented dense forward (embedding gather, two GQA RoPE
# blocks with SwiGLU, final RMSNorm, tied output head) in float64 with numpy,
# from the weight literals in ../dense-model/src/main.fab. With TOKENS = [0, 7]
# it reproduces the dense-model `tied_1_*` pins (checked by --check), which is
# what ties this evaluation to the independent reference of that package.
#
#   python3 -I reference.py            # prints the logits rows for the prompt
#   python3 -I reference.py --check    # also asserts the dense-model pins
#   python3 -I reference.py --decode   # prints the PIN_TOKENS / PIN_LOGITS literals
#
# Decode: the prompt is prefilled, g0 = argmax of its last logits row, then step i
# feeds g[i] at position 8 + i and yields the logits that pick g[i+1]. The f64 pin
# of step i is the last row of a FULL re-evaluation of prompt + g[0..i], so it
# shares nothing with a KV cache.
import re
import sys
from pathlib import Path

import numpy as np

SOURCE = Path(__file__).resolve().parent.parent / "dense-model" / "src" / "main.fab"
TOKENS = [0, 3, 7, 1, 5, 2, 6, 4]
STEPS = 16
EPS, SCALE, BASE = 1e-5, 0.5, 100000.0
HEADS, KV_HEADS, HEAD_DIM, HIDDEN, VOCAB = 4, 2, 4, 16, 8


def weights():
    text = SOURCE.read_text()
    out = {}
    for name, body in re.findall(r"let _ (\w+) ← (?:pack_embedding\()?make_block\(\[([^\]]*)\]", text):
        out[name] = np.array([float(x) for x in body.split(",")], dtype=np.float64)
    return out


def rmsnorm(x, g):
    return x / np.sqrt((x * x).mean(axis=-1, keepdims=True) + EPS) * g


def rope(x, positions):
    out = x.copy()
    for t, pos in enumerate(positions):
        for k in range(HEAD_DIM // 2):
            angle = pos * BASE ** (-2.0 * k / HEAD_DIM)
            c, s = np.cos(angle), np.sin(angle)
            a, b = x[t, 2 * k], x[t, 2 * k + 1]
            out[t, 2 * k], out[t, 2 * k + 1] = a * c - b * s, a * s + b * c
    return out


def block(x, w, layer):
    g = lambda n: w[f"L{layer}_{n}"]
    t = x.shape[0]
    positions = list(range(t))
    h = rmsnorm(x, g("LN1"))
    q = h @ g("WQ").reshape(HIDDEN, HEADS * HEAD_DIM)
    k = h @ g("WK").reshape(HIDDEN, KV_HEADS * HEAD_DIM)
    v = h @ g("WV").reshape(HIDDEN, KV_HEADS * HEAD_DIM)
    heads = []
    for head in range(HEADS):
        grp = head // (HEADS // KV_HEADS)
        qh = rope(q[:, head * HEAD_DIM:(head + 1) * HEAD_DIM], positions)
        kh = rope(k[:, grp * HEAD_DIM:(grp + 1) * HEAD_DIM], positions)
        vh = v[:, grp * HEAD_DIM:(grp + 1) * HEAD_DIM]
        s = (qh @ kh.T) * SCALE
        s = np.where(np.tril(np.ones((t, t))) > 0, s, -np.inf)
        p = np.exp(s - s.max(axis=-1, keepdims=True))
        p /= p.sum(axis=-1, keepdims=True)
        heads.append(p @ vh)
    ctx = np.concatenate(heads, axis=-1) @ g("WO").reshape(HEADS * HEAD_DIM, HIDDEN)
    r1 = x + ctx
    n2 = rmsnorm(r1, g("LN2"))
    gate = n2 @ g("WG").reshape(HIDDEN, 16)
    up = n2 @ g("WU").reshape(HIDDEN, 16)
    act = gate / (1.0 + np.exp(-gate)) * up
    return r1 + act @ g("WD").reshape(16, HIDDEN)


def forward(tokens):
    w = weights()
    embed = w["EMBED"].reshape(HIDDEN, VOCAB)  # math order [D, V]
    x = embed[:, tokens].T
    for layer in (0, 1):
        x = block(x, w, layer)
    return rmsnorm(x, w["NORM_S"]) @ embed


def decode(steps=STEPS):
    """Greedy decode: returns (g0, generated tokens g1..gN, per-step last logits)."""
    seq = list(TOKENS)
    g0 = int(np.argmax(forward(seq)[-1]))
    seq.append(g0)
    generated, rows = [], []
    for _ in range(steps):
        row = forward(seq)[-1]
        rows.append(row)
        nxt = int(np.argmax(row))
        generated.append(nxt)
        seq.append(nxt)
    return g0, generated, rows


if __name__ == "__main__":
    if "--decode" in sys.argv:
        g0, generated, rows = decode()
        print("# first token (argmax of the prefill row):", g0)
        print("# smallest top-1 margin over the steps:",
              min(float(np.sort(r)[-1] - np.sort(r)[-2]) for r in rows))
        print("const list<int> PIN_TOKENS =", generated)
        flat = [repr(float(v)) for r in rows for v in r]
        print("const list<f64> PIN_LOGITS = [" + ", ".join(flat) + "]")
        sys.exit(0)

    if "--check" in sys.argv:
        pins = [0.6718318339, 0.7165587405, 0.6708635804, 0.7207105948,
                0.7666465014, 0.7982108721, 0.1008225495, 0.6189393881]
        got = forward([0, 7])[1]
        worst = float(np.abs(got - np.array(pins)).max())
        print("dense-model tied_1_* pin max abs error", worst)
        assert worst < 1e-9, worst
    logits = forward(TOKENS)
    print("tokens", TOKENS)
    for i in range(len(TOKENS)):
        print("row", i, [repr(float(v)) for v in logits[i]])
