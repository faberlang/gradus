# PML5 Closeout Note — phase gate MET at the structural tier; the executed-oracle clause is NAMED, dated, and stays OPEN (CTO8-1 / CTO8-3)

**Unit**: PML5 phase closeout (campaign gate; PML6 next per the ordering
graph)
**Date**: 2026-08-09
**Predecessor**: PML5-U1..U6 all landed and admitted by Mind — U1 bdefb5a
(decode loop semantics), U2 3b2fc9b (KV-cache values and mutation rules),
U3 b1b01f1 (deterministic sampling), U4 56e70f0 (generation-configuration
contract), U5 8cf798a (reset, context limits, cancellation, determinism),
U6 1a6abd0 (oracle-matching token proof). Delivery: `pml5-delivery.md`.
**Repo**: gradus.

## Outcome: phase gate **MET at the structural tier** — PML5 delivered; the executed-oracle clause is a NAMED OPEN clause (CTO8-1)

All six PML5 units landed. The phase gate (`pml5-delivery.md` §Phase gate:
U1–U6 done; oracle-matching tokens for the admitted model; reject rows
enforced; README regen + audit 0) is satisfied at the **structural
(compile-level) tier**: decode, KV-cache, sampling, generation
configuration, and reset/limits/cancellation compose over the shared
forward functions (PML3), and the bounded generation run's expected token
sequences are pinned (greedy `[0]` + seeded `[1, 1]`, f64 evaluations,
first-token-divergence rule, reset/replay determinism).

> **Correction (2026-08-09, CTO9-4)**: the greedy pin is `[0]`, not
> `[0, 0]`. Under the admitted tokenizer identity (EOG set `{0, 2}` —
> tokenizer.fab), the greedy run's first drawn token `0` is an EOG token,
> so the EOG-stop policy terminates generation at `[0]`; `maxima_verborum`
> is a ceiling, not a promise to emit exactly that many tokens. The
> oracle, pins, and docs were reconciled to the admitted contract
> (hand-2, task 4e2dcb05).

Per **CTO8-1**, the phase gate does **NOT** close as "MET structural" by
default: **oracle-matching tokens (executed)** is a **named gate clause**
that stays **OPEN** with a dated trigger (see the Named Executed-Gate
Clause section). No executed-token claims exist anywhere.

## Per-unit evidence

| Unit | Commit | Evidence (structural tier) | Tier |
| --- | --- | --- | --- |
| U1 — Decode loop semantics | bdefb5a | `src/decode.fab` `decodere_datum` (token id + position → full-vocab logits over embedding → transformer_block mode 2 causal+RoPE → output projection), `prefill` sharing the same forward functions, `Session` reset/limit; f64 logit oracle pins | structural |
| U2 — KV-cache values + mutation | 3b2fc9b | `src/cache.fab` `KVCache` typed logical value (identity fields + exact history + K/V + generation), `append` per-position (strictly sequential), `reset`, `CacheIdentity` per MD-A9; exact append/readback pins | structural |
| U3 — Deterministic sampling | b1b01f1 | `src/sampling.fab` `Config` validation + `max` (greedy exact) / `sample` (rep-penalty → temperature → top-k → softmax → top-p → min-p, pure logits+config+RNG); pinned per-knob oracle | structural |
| U4 — Generation-config contract | 56e70f0 | `src/generation.fab` nine-field contract (values/defaults/validation), deterministic mapping (Config + Seed), explicit reject rows, single-authority statement (NGAB5 adapts); exact mapping + wire pins | structural |
| U5 — Reset, limits, cancellation, determinism | 8cf798a | `decode`/`generation` reset + context-limit reject policy, cooperative cancellation observation, deterministic replay; proba'd | structural |
| U6 — Oracle-matching token proof | 1a6abd0 | `exempla/token-generation` bounded run (decode → sampling → cursor; greedy + one seeded stochastic config) on the tiny pinned decoder; expected sequences `[0]` / `[1, 1]` pinned (f64), first-token-divergence rule, reset/replay determinism | structural |

## Phase-gate checklist

| Gate clause | Evidence | Verdict |
| --- | --- | --- |
| U1–U6 done | All six units landed + admitted (commits above) | **MET** |
| Oracle-matching tokens for the admitted model | Bounded generation run (greedy `[0]` + seeded `[1, 1]`) with f64-evaluated token pins, first-token-divergence comparison policy, reset/replay determinism probed — **at the compile level** (the U6 exemplum + pins) | **MET (structural)** |
| Oracle-matching tokens (EXECUTED) | Env-blocked on the sole remaining blocker (FMIR library-call gap — the PML4 closeout's other blocker, TARGETLANE001, no longer applies to the token run's lane posture) | **NAMED OPEN CLAUSE (CTO8-1)** — see below |
| Reject rows enforced | `generation.proba` reject-row matrix (unsupported llama.cpp-style controls pinned row by row); config wire rejects extra fields | **MET** |
| README regen + audit 0 findings | `generate-factory-readme.py` regenerated + `--check` green; goal-status audit 0 findings (see Validation) | **MET** |
| No executed-token claims | Every unit recorded PARTIAL per CTO Q2; no executed value claimed anywhere | **MET (honesty)** |

## CTO8-1 — NAMED EXECUTED-GATE CLAUSE (mandatory, dated trigger)

**Clause**: "oracle-matching tokens (executed)" — the PML5 phase gate's
executed-oracle run — is a **named gate clause**. The PML5 phase gate does
**not** close as "MET structural" by default: this clause stays **OPEN**
until its trigger fires.

**Dated trigger (recorded 2026-08-09)**: the clause defers to when
**hand-1's FMIR e2e-hardening lands** AND **`exempla_script_e2e` is green
for library-importing packages** (the FMIR lever). The FMIR library-call
gap is the **sole remaining execution blocker** (the PML4 closeout's
TARGETLANE001 record was the Rust-emit-lane block; the token run's proven
lane posture is the TS/FMIR path, so the FMIR lever is the one that
matters).

**Owner**: auditor. **State**: open — recorded, not claimed.

## CTO8-3 — DATED RE-VERIFICATION RECORD (mandatory)

**Recorded 2026-08-09**: when the FMIR lever opens (the trigger above),
ONE auditor-owned pass re-runs, under numeric-policy v1.0.0:

1. the **PML4 trajectory pins + resume + seeds** (the composed loop's
   loss trajectory, checkpoint round-trip, seeded reproducibility), and
2. the **PML5-U6 tokens** (the bounded generation run's `[0]` /
   `[1, 1]` sequences + determinism).

This dated record ensures the re-verification cannot be silently dropped.

## Post-lever sequencing (CTO8-1)

Once the FMIR lever opens, the execution-order sequence is:

1. **PML5-U6 executed run** — the bounded generation run vs its token
   pins (first-token-divergence rule).
2. **PML4 composed-loop convergence** — the composed training loop vs the
   trajectory pins + resume + seeds.
3. **codex-gap SCRIPT promotions** — the SCRIPT-lane promotions
   previously gated by the gap.
4. **PML3-U4 / PML0-U5 executed rows** — the earlier structural rows'
   executed tier.

## NGAB5 feed note

The PML5 aggregate (decode → KV-cache → sampling → generation-config →
reset) is the **semantic contract NGAB5 adapts** (the adapter seam — the
generation config names itself the single authority). The **executed tier
gates the feed**: NGAB5's executable evidence is NGAB's own; the PML5
executed-oracle clause (CTO8-1) is the correctness floor the feed's
semantic mapping is cross-checked against when it opens.

## Decision context honored

- **Structural tier, executed clause named**: the gate's executed clause
  is a named open clause with a dated trigger, not a "MET structural"
  blanket — the CAMPAIGN line records it (no leading-clause games).
- **No executed claims**: every unit recorded PARTIAL per CTO Q2; no
  executed value claimed anywhere in the closeout or the units.
- **FMIR is the sole remaining blocker** for the executed tier; the
  TARGETLANE001 record from PML4 is context (the Rust-lane posture), not
  an active block for the token run's lane.
- **Ordering-graph pointer**: PML6 (package contract) is the next Gradus
  phase; NGAB5 (native GPU application bundle) feeds on this phase's
  semantic contract.

## Validation (one closeout run)

- `grep -n '^\*\*Status\*\*' CAMPAIGN.md`: PML5 stage line
  machine-parseable (`**Status**: delivered (structural tier) — …PML6
  next…` with the named clause + dated trigger); all other stage lines
  unchanged.
- `python3 ../radix/scripta/generate-factory-readme.py --factory-root
  docs/factory --check`: PASS after regeneration (this record added to the
  gradus factory README).
- goal-status audit (`./scripta/check-factory-goal-status`): **0
  findings**.
- `git diff --check`: PASS.

## Residuals + owners

| # | Residual | Owner | State |
| --- | --- | --- | --- |
| 1 | PML5 executed-oracle clause (CTO8-1): oracle-matching tokens (executed) — open until hand-1's FMIR lands AND `exempla_script_e2e` is green for library-importing packages; then one auditor pass re-runs PML4 pins + PML5 tokens (CTO8-3) | Auditor (executed-tier gate) + hand-1 (FMIR lever) | open — trigger dated 2026-08-09 |
| 2 | NGAB5 feed: the aggregate is the semantic contract NGAB5 adapts; the executed tier gates the feed (cross-check the executed-oracle clause when it opens) | NGAB5 delivery owner | pending — NGAB5 |
| 3 | PML6 (package contract) is the next Gradus phase per the ordering graph — planning is Mind's | Mind routes at PML6 planning | **closed** — PML6 delivered structural (`pml6-closeout.md`, 2026-08-11) |
| 4 | PML6-U3 aggregates every admitted row into `pml0-support-matrix.md` (the PML4/PML5 structural rows join the full-matrix aggregation) | PML6 delivery owner | **closed** — U3 `43d75ce` (full-matrix aggregation) |
