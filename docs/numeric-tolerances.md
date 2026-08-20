# Gradus Numeric Tolerances

**Version**: `gradus-numeric-tolerances v1.0.0` (2026-08-11, PML6-U4)
**Repo**: gradus. **Tier**: structural pin inventory + policy aggregate.
**Delivery**: `docs/factory/production-ml-library/pml6-delivery.md` §PML6-U4.
**Cross-repo authority (read-only, pinned revision)**:
`numeric-policy v1.0.0` —
`radix/docs/factory/gpu-training-lowering/numeric-policy.md`
(`NUMERIC_POLICY_VERSION 1.0.0`, immutable S0-B).

This document **aggregates** the tolerances Gradus proba pins and
comments already use, and cites the cross-repo numeric policy for the
gradient / loss rows that the GPU-training lane and the auditor-owned
runtime gate share. It invents no new floor. A cross-repo revision
conflict escalates to Mind (pml6-delivery.md Escalation Path); default =
the cross-repo policy is read-only at its pinned revision.

**No executed numeric claim is made here.** Pins are f64 evaluations of
documented formulas; runtime value-identity is auditor-owned (CTO8-1).

---

## 1. Comparison primitives

### 1.1 `approximata` (Gradus proba absolute band)

Co-located proba files compare f32 production-surface values to pinned
oracles with Faber's `approximata(expected, tol)` — an **absolute**
band `|observed − expected| ≤ tol`. The default forward band on the
self-hosted f32 surface is:

| Symbol (local name varies) | Absolute tolerance | Role |
| --- | ---: | --- |
| `0.0005` (`5e-4`) | **5e-4** | Forward / logits / sampling / schedule / loss scalar pins on the f32 self-hosted surface |

Representative constants (live tree):

| File | Constant | Value |
| --- | --- | ---: |
| `src/nn.proba` | `GELU_TOLERATIO` | `0.0005` |
| `src/loss.proba` | `LOSS_TOLERATIO` | `0.0005` |
| `src/attention.proba` | `TOLERATIO` | `0.0005` |
| `src/transformer.proba` | `TOLERATIO` | `0.0005` |
| `src/gradus.proba` | `TOLERATIO` | `0.0005` |
| `src/decode.proba` | `DECODE_TOLERATIO` | `0.0005` |
| `src/sampling.proba` | `SAMPLING_TOLERATIO` | `0.0005` |
| `src/train.proba` | `LENTUS_TOLERATIO` | `0.0005` |

Rationale recorded in those files: the production surface is **f32
self-hosted** (self-hosted exp/tanh/ln/sin/cos/sqrt via documented
identities); the pins are independent **f64** evaluations of the same
formulas. `5e-4` absolute covers the self-hosting error over the
admitted rows' ranges. **Do not tighten a pin to green a failing
executed run** — that is a stop condition under the numeric policy's
no-relaxation rule.

### 1.2 Cross-repo elementwise rule (`numeric-policy v1.0.0` §2)

When a comparison is against a device observation or an independent
gradient/loss oracle under the GPU-training lane, the frozen rule is:

```text
|a_i − b_i| ≤ atol + rtol · |b_i|
```

- `a` = observed, `b` = reference (never the device result as its own
  reference).
- Shape match is required first; mismatch is FAIL.
- Per-element; no aggregate substitute.
- Any NaN / ±Inf on either side is FAIL
  (`numeric-policy v1.0.0` §5.1 NaN/Inf rule).

Gradus structural pins that use absolute `approximata` are a **library
proba convention** for the f32 self-hosted surface; they do not replace
the policy rule for device or FD-oracle acceptance.

---

## 2. `numeric-policy v1.0.0` family rows (cited, not re-derived)

Pinned coefficients from
`radix/docs/factory/gpu-training-lowering/numeric-policy.md` §3.1
(`f32` op families). Receipt floors are in that document §6.

| Op family | `atol` | `rtol` | Gradus use |
| --- | ---: | ---: | --- |
| Elementwise | `1.0e-6` | `1.0e-5` | Device/oracle elementwise parity (GPU lane) |
| Reduction sum / mean (**loss scalars**) | `1.0e-6` | `1.0e-6` | Deterministic loss-trace acceptance (§5.2 of the policy) |
| Matmul | `1.0e-5` | `1.0e-5` | Matmul / VJP products |
| **Gradient tensors** | **`1.0e-4`** | **`1.0e-4`** | Companion vs analytic / FD oracle (R4 / council G6) |

In-tree citation convention (matches `src/gradient.fab` comments and the
PML6 delivery lock): the **gradient row is recorded as
`1e-4 / 1e-4` under `numeric-policy v1.0.0`** (delivery text says
"§5.1"; the policy document places the coefficients in §3.1 and the
NaN/Inf + loss-trace rules in §5 — cite the **version + family row**,
not a drifting section number alone).

Finite-difference protocol (policy §4), when used:

- Method: central difference.
- `ε = 1.0e-3` (`FINITE_DIFFERENCE_EPSILON`).
- Acceptance: gradient family row above.
- Do **not** cite the test-local `FINITE_DIFFERENCE_TOLERANCE = 2.0e-3`
  as campaign policy.

Integer dtypes: exact bitwise (policy §3.2). Unlisted dtypes: no
admitted tolerance until the policy is amended (policy §3.3).

---

## 3. Gradus-local absolute bands (beyond the forward `5e-4`)

### 3.1 `1e-4` absolute f32 self-host (optimizer / tight self-host)

| File | Constant | Value | Role |
| --- | --- | ---: | --- |
| `src/optimize.proba` | `SGD_TOLERATIO` | **`0.0001` (`1e-4`)** | SGD step output vs f64 oracle pins; conservative absolute band covering f32 self-hosting over the admitted magnitudes, inside the GPU lane's gradient row |

The optimize suite comments explicitly bind this band to
`numeric-policy v1.0.0` (the `1e-4` gradient row) while remaining an
**absolute** `approximata` check on the structural surface.

### 3.2 Tighter absolute pins (specialized, not general forward)

| Location | Band | Role |
| --- | ---: | --- |
| `src/train.proba` RNG draws | `1e-6` absolute on documented `[0,1)` draws | xorshift64 / f64 recurrence pins — not a forward-math band |
| Exact equality (`≡`) | 0 | Integer tokens, identities, wire round-trips, error `message` strings, EOG membership |

A specialized tighter band never authorizes relaxing a looser family row
on device or FD acceptance.

---

## 4. Exact token pins + first-token-divergence rule

Token sequences are **exact** — no tolerance band.

### 4.1 Pinned sequences (PML5-U6 / correctness wave `0d50d60`)

| Run | Config (pinned) | Expected tokens | Policy |
| --- | --- | --- | --- |
| Greedy | `temperatura 0`, prompt `[0]`, `maxima_verborum 2`, tiny decoder | **`[0]`** | **EOG-stop**: first drawn `0` is an admitted EOG token (`{0,2}`); generation terminates; `maxima_verborum` is a **ceiling**, never a promise of exact length |
| Seeded stochastic | `temperatura 1.0`, seed **`8742514861359412281`**, neutral filters | **`[1, 1]`** | No EOG token in the draw — runs to the cursor ceiling |

Live pins: `src/decode.proba` (PML5-U6 aggregate), documented for
consumers in `exempla/token-generation/README.md`.

Admitted EOG set: **`{0, 2}`** — `tokenizer.is_eog` is the stop-policy
binding. A different EOG set is a different tokenizer (identity, not a
value error) — see §5 and `docs/compatibility-policy.md` §3.

### 4.2 First-token-divergence rule

When comparing two token sequences (observed vs oracle, or two
independent runs):

1. Compare **token-by-token from index 0**.
2. Report the index of the **first** divergent token (or first missing
   position on a length mismatch).
3. Equal sequences report no divergence (`-1` in the proba helper
   `prima_divergentia`).
4. **Never** substitute text-level similarity, edit distance, or
   "mostly matches after the first token."

Live proof surface: `src/decode.proba` probandum
`"decode — the first-token-divergence rule (PML5-U6)"`.

Logits that feed the token choice still use the forward `5e-4`
`approximata` band; the **token choice itself is exact** (and the
documented per-step boundaries place draws well inside their cumulative
buckets — see the token-generation README).

### 4.3 Reset / replay determinism

Same model + config + seed → same tokens. Two independent runs under
the pinned seed must report no divergence
(`src/decode.proba` `"reset/replay determinism: same seed + input → same tokens"`).
Session `redintegra` resets position while preserving context
(PML5-U5). These are exact structural pins, not tolerance bands.

---

## 5. Capsule / tokenizer identity (exact; not numeric)

| Pin | Expected | Location |
| --- | --- | --- |
| Pinned EOG set | `"0,2"` / membership `{0,2}` | `src/model/capsule.proba` (`F_EOG`), `src/tokenizer.proba` (`is_eog`) |
| Well-formed-but-different EOG | reject (`invalid tokenizer identity` / `BadEog`) | `src/model/capsule.proba` `"rejects a well-formed-but-different EOG set (pinned EOG is {0, 2})"` with eog `"1,5"` |
| Non-sorted / empty / negative EOG | reject | same suite |
| Tokenizer probe lists | exact id lists P1–P11 | `fixtures/tokenizer/tokenizer-identity-oracle.md` |

These are **identity** pins. They never enter an `approximata` band.

---

## 6. How to choose a band (decision table)

| What you compare | Band / rule | Cite |
| --- | --- | --- |
| f32 forward / logits / sampling probs / LR schedule vs f64 oracle pin (structural proba) | absolute **`5e-4`** `approximata` | this doc §1.1 |
| SGD step f32 values vs f64 oracle (structural proba) | absolute **`1e-4`** `approximata` | this doc §3.1 |
| Gradient tensor vs FD / analytic oracle (runtime gate) | **`atol=1e-4`, `rtol=1e-4`** policy rule | `numeric-policy v1.0.0` gradient row |
| Loss-trace scalars vs pinned trace (runtime gate) | reduction row **`1e-6` / `1e-6`** + per-step rule | `numeric-policy v1.0.0` §3.1 / §5.2 |
| Token sequences | **exact** + first-token-divergence | this doc §4 |
| Integer / wire / identity / EOG | **exact** | this doc §5 |
| Unlisted dtype or op family | **no admitted tolerance** | policy §3.3 — escalate, do not invent |

---

## 7. Non-goals

- No relaxation of any band to pass a device or executed run.
- No GPU speed / performance tolerance (not a numeric-parity concept).
- No claim that structural `approximata` pins have been executed green.
- No amendment of `numeric-policy v1.0.0` from this repo.

---

## 8. Versioning

`gradus-numeric-tolerances v1.0.0`. A change that adds a band, retargets
a family row, or changes the token-divergence rule bumps this version.
Cross-repo policy bumps are **not** silent: record the new policy
revision explicitly or escalate.

---

## 9. Validation greps (pin consistency)

```bash
cd /path/to/faberlang/gradus

# Forward 5e-4 absolute band still present on the primary surfaces
rg -n '0\.0005|5e-4' src/nn.proba src/loss.proba src/attention.proba \
  src/transformer.proba src/decode.proba src/sampling.proba src/train.proba

# 1e-4 absolute self-host / gradient-aligned band on optimize
rg -n '0\.0001|1e-4' src/optimize.proba src/gradient.fab

# Exact token pins
rg -n '\[0\]|\[1, 1\]' src/decode.proba exempla/token-generation/README.md

# Capsule EOG rejection pin
rg -n 'well-formed-but-different EOG|pinned EOG is \{0, 2\}' src/model/capsule.proba

# First-token-divergence + reset/replay
rg -n 'prima_divergentia|reset/replay determinism' src/decode.proba

# Cross-repo policy still at v1.0.0 (read-only check from workspace)
rg -n 'NUMERIC_POLICY_VERSION 1.0.0' \
  ../radix/docs/factory/gpu-training-lowering/numeric-policy.md
```
