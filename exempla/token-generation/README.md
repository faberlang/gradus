# token-generation — the PML5-U6 bounded generation run (the aggregate)

The oracle-matching token proof for the PML5 phase gate
(`gradus/docs/factory/production-ml-library/pml5-delivery.md` PML5-U6):
the composition flagged at U5 — `decodere_datum` → `sampling`
(`maxima` / `sors`) → the generation cursor — wired into a bounded
generation run (greedy + one seeded stochastic config) whose expected
token sequences are pinned against the documented arithmetic, with the
GI0–GI2 oracle linkage recorded and the first-token-divergence rule
enforced.

## The pinned workload (gradus scale)

The tiny pinned decoder of `decode.proba` (V=3, D=4, F=4, context 3,
scale 1/√4, RoPE dim 4 — the oracle-pinned model), prompt `[0]`, config
`contextus 3, prompt batch 1, max generated tokens 2`:

| Run | Config | Expected tokens (f64 oracle) |
| --- | --- | --- |
| Greedy | temperatura 0 (the U3 greedy path, exact argmax) | `[0]` |
| Seeded stochastic | temperatura 1.0, neutral knobs, seed `8742514861359412281` | `[1, 1]` |

The greedy run emits **`[0]`** — not `[0, 0]` — because of the **EOG-stop
policy** (the CTO9-4 correctness fix, binding generation to the admitted
tokenizer identity): the first drawn token `0` is an admitted EOG token
(EOG set `{0, 2}` — `tokenizer.fab`, `tokenizator.est_eog`), so
generation terminates after it. `maxima_verborum` is a **ceiling**, not a
promise to emit exactly that many tokens. The seeded run draws `[1, 1]`
(no EOG token), so it runs to the cursor ceiling.

Both runs are bounded by the generation cursor (`verbum_licet` — the U5
reject policy: never more than `maxima_verborum`, never truncated) AND
the EOG-stop policy (terminate at the first EOG token). The stochastic
run threads the running history into `sors` and advances the explicit
`Semen` per step; the cooperative cancellation checkpoint is observed
before every step (honored: a cancelled flag stops the run).

## What the run composes (the U6 residual from PML5-U5)

| Step | Surface |
| --- | --- |
| Token decode | `decode.decodere_datum(prev, positio, m)` — one-token decode over the shared forward row (embedding gather → transformer block → output projection) |
| Greedy selection | `sampling.maxima` — the exact argmax path (temperatura 0) |
| Seeded draw | `sampling.sors` — the deterministic pipeline (rep-penalty → temperature → top-k → softmax → top-p → min-p) + one `train.proximus_f32` draw per step, walking the cumulative distribution (first-index rule) |
| Bounded loop | `generation.cursor_fresh` / `verbum_licet` / `cursor_progredere` — the cursor limits (reject, never truncate) + the EOG-stop policy (`tokenizator.est_eog` — terminate at the first EOG token `0`/`2`) drive the loop |
| Cancellation | `decode.observa_cancellationem` per step — the cooperative checkpoint (fail closed) |
| Determinism | pure composition: same model + config + seed → same tokens; the advanced `Semen` is carried explicitly |

## Oracle pins (f64 evaluations, boundary-safe)

The expected token sequences are f64 evaluations of the documented
decode + sampling arithmetic (the same pins the U1/U3 probas carry;
re-verified model-independent against the train.proba recurrence pins).
Pins are recorded in `src/decode.proba` (PML5-U6 section). Tolerance:
the decode logits compare within the documented 5e-4; the token
sequences are exact (the token choice is robust — see the boundaries).

Per-step boundaries (the draw is well inside its token's cumulative
bucket — no near-boundary draw):

| Step | Logits (f64) | Softmax (temp 1) | Draw u | Chosen token | Boundary margins |
| --- | --- | --- | --- | --- | --- |
| Greedy 1 | `[1.0800156280811244, 0.5934879833437627, -2.5475127865679967]` | — | — | `0` | argmax gap 0.4865 |
| Greedy 2 | — not reached — the first drawn token `0` is an admitted EOG token (`{0, 2}`), so EOG-stop terminates the run at `[0]`; the would-be step is the identical RoPE-invariant row (the U1 pin) | — | — | — | — |
| Stoch 1 | `[1.0800156280811244, 0.5934879833437627, -2.5475127865679967]` | `[0.60926, 0.37455, 0.01620]` | `0.77714` | `1` | 0.168 / 0.207 from the bucket edges |
| Stoch 2 | `[-0.31137982360561633, 1.1948983869194876, 0.90882901706536]` | `[0.11239, 0.50686, 0.38076]` | `0.33934` | `1` | 0.227 / 0.280 from the bucket edges |

## The GI0–GI2 oracle (external, read-only)

The pinned GI fixtures
(`faber-runtime/testdata/gi2-3-logits-golden`,
`faber-runtime/testdata/gi2-4-greedy-record`) are the SmolLM2-360M
49152-vocab oracle: `gi2-3` pins 49152 raw logits at prompt position 8
(band delta 9.9999e-6); `gi2-4` pins the 256-token greedy record (prompt
`[504, 2365, …]`, first generated token `30`,
`first_divergence: null`). The gradus side owns the
decode→sampling→cursor surface; the 49152-vocab logits are produced by
the dequant + 32-layer decoder consumer in `faber-runtime`, which this
workload cannot execute today (blocker below). The comparison policy
against the GI oracle is the **first-token-divergence rule** (below) —
never text-level similarity.

## The first-token-divergence rule

Any oracle comparison walks the token sequences from position 0 and
stops at the FIRST divergent token: `prima_divergentia(expectata,
actualia)` returns the first differing index (0-based) or `-1` when the
sequences agree at every compared position. A run whose first token
differs from the oracle reports divergence at index 0 even if all later
tokens match — text-level similarity (e.g. "90% of tokens agree") is
never the claim. The rule is probe-pinned in `decode.proba`.

## Determinism evidence (reset/replay)

- Same model + config + seed → same token sequence (two identical runs
  are identical — `prima_divergentia(a, b) == -1`).
- The stochastic run carries the advanced `Semen` explicitly per step
  (no hidden state); the cursor resets via `cursor_redintegra` to the
  fresh state (position 0, count 0, context preserved).
- The U5 replay pins hold: the seeded run re-derives the plain `[1, 1]`
  replay pin through the full decode→sampling→cursor composition. The
  penalized `[1, 2, 1]` replay pin stays a U5 sampling-side pin
  (`decode.replica` over a fixed logits stream — it is not a generation
  loop and not re-derived by this workload, which runs neutral knobs);
  EOG-stop is a generation-loop policy, so a sampling replay that draws
  the EOG token `2` is out of that scope.

## Execution record (honest — CTO Q2)

This workload is **compile-validated** by `faber check` on the package
(every U1–U5 call and the aggregate composition type-check), and its
expected token sequences are pinned by the co-located proba. **Executed
token generation is env-blocked today**: the FMIR execution lane does not
build — `faber run --target fmir` fails with `invalid MIR: named
aggregate is missing required field` / `fmir image build failed` on the
existing PML4 exempla (the recorded FMIR stepper / library-import gap;
hand-1's e2e-hardening successor slice is in flight). PML5-U6 is
therefore **PARTIAL** per the standing bar: the proof is structural
(composition + f64 oracle pins) and executed value-identity (the run's
printed tokens vs the pins, the deterministic replay byte identity) is
deferred to the auditor-owned runtime-evidence gate. **No executed
token is claimed.**

To run the gate once the lane opens: `faber run -t fmir .` (FMIR lane)
and compare the printed token sequences against the pins above with the
first-token-divergence rule — divergence, if any, is recorded at the
first divergent token.
