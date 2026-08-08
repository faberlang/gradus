# Gradus-Scoped Factory Goal-Status Audit Entrypoint (PML0-U13, council C7)

**Campaign**: `production-ml-library` (PML0, discovery-first)
**Unit**: PML0-U13 — joint receipt schema + Gradus-scoped audit entrypoint (C7)
**Status**: selected 2026-08-08 — the entrypoint is committed and green
**Requirement discharged**: `production-ml-library/CAMPAIGN.md` §Validation —
*"The shared status-audit script is hard-bound to Radix's `docs/factory` and
has no `--factory-root`. The sibling README generator uses the same status
parser, so `--check` is the current Gradus gate. PML0 must add or select a
Gradus-scoped audit entrypoint before claiming the full status-audit gate."*
**Authority**: `council-review-2026-08-08.md` C7; `pml0-delivery.md` PML0-U13;
mirrored by NGAB0-U10 on the faber side (joint receipt schema, both
campaigns).

---

## 1. Selection — added, not merely selected

**Decision**: **add** `gradus/scripta/check-factory-goal-status`.

The requirement offers "add or select". A bare selection was not available:
the shared audit script is, as the CAMPAIGN says, hard-bound to radix's own
`docs/factory` as its default root, and the script's `--factory-root` argument
exists but is suppressed from `--help` (audit-factory-goal-status.py, line
583). Selecting the radix script without a wrapper would audit **radix**'s
inventory, not gradus's — the opposite of the required scope. So a Gradus-
scoped entrypoint must be added as a thin wrapper.

## 2. The entrypoint

`gradus/scripta/check-factory-goal-status` is a thin bash wrapper (no cargo,
python only):

```bash
exec python3 "$AUDIT" --factory-root "$ROOT/docs/factory" --fail-on error "$@"
```

- `--factory-root "$ROOT/docs/factory"` scopes the shared audit to gradus's
  factory inventory (the same root the README generator is invoked with).
- `--fail-on error` defaults the gate to PML0 Gate C's requirement — the
  entrypoint returns non-zero on any `error`-severity finding (0 findings
  required).
- Additional arguments pass through to `audit-factory-goal-status.py`
  (later `--fail-on` / `--min-severity` / `--json` / `--no-readme` arguments
  win, per argparse store semantics), so `--json` output and severity
  overrides remain available.
- The wrapper resolves the shared audit relative to the sibling checkout
  (`../radix/scripta/audit-factory-goal-status.py`) and fails loudly if that
  sibling is missing — no silent fallback to a second parser.

## 3. Selection rationale

1. **Single status-parser source of truth.** The README generator imports its
   status classifier from `audit-factory-goal-status.py` (single source of
   truth). A wrapper reuses the same parser and the same README cross-check,
   so gradus's audit gate can never disagree with the generated README — the
   two drift only together, which is the point of `--check`.
2. **Scope is native, not forked.** `--factory-root` exists in the shared
   audit; the wrapper is the smallest possible way to point it at gradus.
   Forking the audit into gradus would create a second parser to maintain and
   re-verify — rejected under the campaign's smallest-correct-code rule.
3. **Uniform entrypoint name across repos.** radix already ships
   `scripta/check-factory-goal-status`; NGAB0-U10 selects the same shape for
   faber. `gradus/scripta/check-factory-goal-status` matches, so the same
   command name means "audit this repo's factory inventory" in every sibling.
4. **Fail-closed default matches the gate.** Gate C's audit requirement is
   "0 findings". Defaulting `--fail-on error` makes the wrapper's plain
   invocation the gate, with no flag to forget.
5. **CAMPAIGN wording superseded.** The CAMPAIGN sentence *"has no
   `--factory-root`"* is stale: the shared audit gained the (suppressed)
   `--factory-root` argument. This unit's wrapper is the Gradus-scoped
   entrypoint the gate requires; the CAMPAIGN's `--check`-only posture is
   superseded by the wrapper for gate purposes, and the README `--check`
   remains in force as the freshness check.

## 4. No new code ownership

The wrapper is two shell lines plus a sibling-missing guard. The audit
implementation, the status vocabulary, and the README cross-check remain
radix-owned. Gradus owns only the scoping and the fail-on-error default.
Nothing in this unit runs cargo, faber, or a build.

## 5. Verification (this unit's closeout)

- `./scripta/check-factory-goal-status --fail-on error` exits 0 with
  0 findings ("no drift flagged").
- `python3 ../radix/scripta/audit-factory-goal-status.py --factory-root
  docs/factory --fail-on error` produces the same result — the wrapper and
  the raw scoped invocation match.
- `python3 ../radix/scripta/generate-factory-readme.py --factory-root
  docs/factory --check` exits 0 (README regenerated — never hand-edited).
- `git diff --check` clean.
