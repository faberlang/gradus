# Delivery: Qwen3.6 35B TRUTH-01 Authority-Chain Reconciliation

**Status**: ready — goal-check `READY`; `TRUTH-01A` is the first implementation-ready frontier
**Campaign**: [`radix/docs/factory/gpu-production-readiness/CAMPAIGN.md`](../../../../radix/docs/factory/gpu-production-readiness/CAMPAIGN.md)
**Semantic authority**: [`pml5-general-gguf-delivery.md`](pml5-general-gguf-delivery.md)
**Goal check**: [`pml5-qwen36-truth01-goal-check.md`](pml5-qwen36-truth01-goal-check.md)
**Planning assignment**: Vivi `d1f75e78`
**Owning repos**: `gradus` for semantic records and Radix for the campaign control plane
**Planning boundary**: documentation and Vivi registration only; no product source, test, model-byte, runtime, host, or release mutation

## 1. Interpreted Unit

Reconcile one current authority chain for the exact local
`Qwen3.6-35B-A3B-UD-Q4_K_M.gguf` campaign. Every current authority must name
the same immutable artifact identity, the same end-to-end invariant, the same
ownership split, the same predecessor evidence, and the same next mandatory
implementation unit. Historical broad-platform records must remain available
as provenance but must not be mistaken for current Qwen authority. Factory status audits and the two live Vivi goal registrations must resolve
to the same active chain.

The immutable identity is:

| Field | Required value |
| --- | --- |
| Filename | `Qwen3.6-35B-A3B-UD-Q4_K_M.gguf` |
| Architecture | `qwen35moe` |
| Byte length | `22,663,387,424` |
| SHA-256 | `0b21525e972670ed59e1812e170b27c26355381f0656ecc4e25617ece7dac58b` |
| A1b observed row | `PASS version=3 alignment=32 data=10991392 metadata=55 tensors=753 architecture=qwen35moe` |
| Capstone | `gradus/exempla/qwen36-35b-inference` |
| Current implementation frontier | campaign `LIB-01` = Gradus `GGUF-A1c` |

`TRUTH-01` is not complete merely because the current campaign documents
already agree on most fields. It closes only when stale broad-era authority is
explicitly quarantined, the support matrix has a current exact-Qwen campaign
row, the factory status audit is green, and Vivi registration is verified
against the reconciled paths.

## 2. Normalized Spec

### 2.1 Exact executed outcome remains the campaign contract

This reconciliation must preserve the complete `Q0` through `Q4` chain. The
campaign remains active until one normal Faber package command:

1. verifies and admits the exact artifact;
2. tokenizes operator-supplied Unicode text with artifact metadata and the
   admitted special-token policy;
3. executes every layer of the complete `qwen35moe` graph, including MoE
   routing and hybrid SSM/attention state;
4. performs full-model prefill and autoregressive decode;
5. generates and decodes at least 256 new tokens;
6. repeats for a second prompt through the same admitted model session while
   weights and model state remain resident;
7. avoids per-token reload, recompilation, packet rebuild, and full host
   round-trip;
8. matches the pinned `llama.cpp` token/logit comparison policy;
9. runs on both admitted single-device backends, Metal and CUDA; and
10. records exact source revisions, command, model identity, hardware,
    backend, output, peak memory, timing, reset, reuse, and teardown facts.

No smaller model, structural proof, parser receipt, emitted artifact, CPU
fragment, one-backend run, or planning document may replace a clause.

### 2.2 Authority order after reconciliation

1. Exact Radix campaign invariant and cross-repository joins.
2. Gradus PML5-GGUF semantic delivery and its detailed `GGUF-A*` / `GGUF-M*`
   graph.
3. Exact artifact receipt and support-matrix row.
4. Current Gradus campaign status and ownership routing.
5. Radix and Gradus factory status audits.
6. Vivi registrations that point to items 1 and 2.
7. Historical broad-platform frontier records, read-only and explicitly
   superseded for current routing.

### 2.3 Local artifact and corpus boundary

The artifact and sibling corpus are operator-local evidence. They are not
committed, copied, renamed, uploaded, downloaded, redistributed, or scanned by
this unit. Documentation may retain already observed metadata, hashes, lengths,
offset/count facts, and commands. Applications own paths and I/O. Gradus
semantic values own content identity and bounded descriptors only. Hosts or an
application resolve byte ranges. A Hand must stop rather than read model bytes
for a documentation reconciliation.

### 2.4 Hardware and backend authority

The campaign requires both Metal and CUDA, but `TRUTH-01` performs no device
run. Future positive receipts must name exact machines, OS, driver/runtime,
backend, source revisions, model identity, storage types, kernel/package
identities, observed output, timing, peak memory, lifecycle counters, and
teardown. A missing backend receipt keeps `Q3` and `Q4` incomplete. A
structural, fake, smaller-model, or CPU-only row cannot be promoted to either
backend.

### 2.5 Batching and split decision

Use three serial documentation units. The split is justified by named
ownership and external-state boundaries:

- `TRUTH-01A`: Gradus-owned semantic authority and exact receipt.
- `TRUTH-01B`: Radix-owned control plane and historical broad-era quarantine.
- `TRUTH-01C`: cross-repository generated-index, status-audit, and Vivi
  registration closeout. Vivi is a separate control-record mutation owned by
  Mind, not a product Hand.

Do not split by individual file. Each unit is an atomic authority update.

## 3. Repo-Aware Baseline

Verified from clean `factory/planner-1` packets on 2026-08-13:

| Repo | Baseline | Current fact |
| --- | --- | --- |
| Radix | `b6d6e17c8ad73e36b6489f2533b50b1f1d66aec8` | Campaign narrowed to exact Qwen3.6; status active; `LIB-01` next |
| Gradus | `bc500993c97b99bb4ca3ff0d98828b56c750eec0` | PML campaign and detailed delivery require exact Qwen3.6; A1a/A1b implemented; A1c next |
| Faber | `1fb6cc97e66d9b434105e952a1dba4539daaa2b0` | Package/build/run owner; no TRUTH-01 write |
| Hosts | `57d659d604309c11b6046a514317c22dd6b468f1` | Physical execution owner; no TRUTH-01 write |

### 3.1 Accepted predecessor receipts

| Receipt | Revision or handle | What it proves | What it does not prove |
| --- | --- | --- | --- |
| GGUF-A1a bounded manifest foundation | Gradus `9ec0e1f`, corrections `b8a5d0d`, `bf3280a`, `4c20af0` | Format-general bounded GGUF manifest behavior and synthetic package-MIR proof | Real model admission, payload materialization, tokenization, or inference |
| GGUF-A1b guarded range inspection | Gradus `2abfcff` | Exact target identity and observed `qwen35moe/753` manifest facts without reading tensor payload bytes | Tokenizer, tensor payload, logits, tokens, CPU inference, Metal, or CUDA |
| Exact-Qwen campaign amendment | Radix `b6d6e17c8`; Gradus `bc500993c` | Replaces broad completion language with exact Qwen3.6 contract and preserves all successors | Any product execution |
| Vivi campaign registration | `gol_634a0417d02c510f` | Current Radix campaign path is registered once | Semantic delivery details or product execution |
| Vivi semantic registration | `gol_67b635603712f01b` | Current Gradus PML5-GGUF delivery path is registered once | Campaign completion |

### 3.2 Current stale or incomplete authority surfaces

1. `radix/docs/factory/gpu-production-readiness/frontier-1-delivery.md` still
   describes the superseded broad M0-to-M4 platform campaign.
2. `radix/docs/factory/gpu-production-readiness/evidence/frontier-1/t1-status-reconciliation.md`
   still identifies the old broad umbrella and old child-goal set as current.
3. `t2-registration-record.md` records an old multi-goal registration topology.
4. `t3-support-matrix.md` is useful historical evidence but is not the exact
   Qwen completion matrix.
5. `t4-claim-freeze.md` freezes SmolLM and explicitly says there is no Qwen
   claim. It must remain historical and must not govern the amended campaign.
6. `gradus/docs/factory/production-ml-library/pml0-support-matrix.md` records
   A1b as a format-inspection foundation but lacks one explicit current
   exact-Qwen campaign row and its Q0-to-Q4 promotion policy.
7. The Radix and Gradus factory status audits are the live inventory
   authority. After a documentation change, re-run the owning repository's
   status audit before closeout.
8. Vivi currently lists exactly two Qwen authorities. Closeout must preserve
   that exact topology unless an explicit campaign amendment changes it.

## 4. Stage Graph

```text
TRUTH-01A Gradus semantic reconciliation + exact receipt
  -> TRUTH-01B Radix control-plane reconciliation + historical quarantine
       -> TRUTH-01C status audits + Vivi closeout
            -> LIB-01 / GGUF-A1c product implementation
                 -> LIB-02 + LIB-03
                      -> REF-01 + MODEL-01
                           -> MODEL-02 + MODEL-03
                                -> MODEL-04
                                     -> EXEC-01 + EXEC-02
                                          -> EXEC-03
                                               -> CAP-01 + CAP-02
                                                    -> CLOSE-01
```

The graph sequences the documentation gate but preserves every mandatory
campaign successor. Completing `TRUTH-01C` advances `Q0` only. It does not
complete `Q0`'s descendants and cannot be mistaken for campaign completion.

## 5. Implementation Work

### TRUTH-01A — Gradus semantic authority and exact-artifact receipt

- **outcome**: the Gradus campaign, detailed delivery, support matrix, and one
  new exact-artifact authority receipt agree on artifact identity, current
  evidence, ownership, mandatory successors, and `GGUF-A1c` as the first
  product unit.
- **write_scope**:
  - `gradus/docs/factory/production-ml-library/CAMPAIGN.md`
  - `gradus/docs/factory/production-ml-library/pml5-general-gguf-delivery.md`
  - `gradus/docs/factory/production-ml-library/pml0-support-matrix.md`
  - `gradus/docs/factory/production-ml-library/evidence/qwen36-35b-authority-chain.md` (create)
- **read_scope**:
  - the five Gradus write-scope source documents before edit;
  - `gradus/exempla/gguf-inspect/README.md` for the already recorded A1b facts;
  - `radix/docs/factory/gpu-production-readiness/CAMPAIGN.md` read-only;
  - `gradus/AGENTS.md` and workspace `AGENTS.md`;
  - Git history for `9ec0e1f`, `2abfcff`, and `bc500993c`.
- **forbidden_scope**:
  - all `gradus/src/**`, `tests/**`, executable `exempla/**`, and fixture bytes;
  - all model files and `/Users/ianzepp/Ai/models/**`;
  - Radix, Faber, Hosts, Inferentia, Trials, or external-service writes;
  - any claim that A1b proves admission, tokenization, materialization,
    inference, Metal, or CUDA.
- **predecessor_receipts**: GGUF-A1a `9ec0e1f` plus corrections; GGUF-A1b
  `2abfcff`; exact-Qwen amendment `bc500993c`.
- **first_failing_oracle**:

  ```bash
  cd <fresh-hand-packet>/gradus
  test -f docs/factory/production-ml-library/evidence/qwen36-35b-authority-chain.md &&
  grep -Fq 'Qwen3.6-35B-A3B-UD-Q4_K_M.gguf' \
    docs/factory/production-ml-library/evidence/qwen36-35b-authority-chain.md &&
  grep -Fq '0b21525e972670ed59e1812e170b27c26355381f0656ecc4e25617ece7dac58b' \
    docs/factory/production-ml-library/evidence/qwen36-35b-authority-chain.md &&
  grep -Fq 'GGUF-A1c' \
    docs/factory/production-ml-library/evidence/qwen36-35b-authority-chain.md
  ```

  Baseline expected result: non-zero because the exact authority receipt does
  not exist.
- **done_when**:
  1. every current Gradus authority names the exact filename, architecture,
     length, hash, A1b evidence boundary, and `GGUF-A1c` next;
  2. the support matrix adds one exact-Qwen campaign row classified as
     format-inspected only, with every higher tier marked mandatory and
     unproved rather than unsupported or deferred;
  3. the receipt maps `Q0` through `Q4` to concrete authorities and mandatory
     successor IDs;
  4. the receipt says explicitly that A1b and TRUTH-01 do not complete the
     campaign;
  5. The Gradus factory status audit reports zero findings.
- **closeout_command**:

  ```bash
  cd <fresh-hand-packet>/gradus
  ./scripta/check-factory-goal-status --fail-on error
  python3 - <<'PY'
  from pathlib import Path

  files = [
      Path('docs/factory/production-ml-library/CAMPAIGN.md'),
      Path('docs/factory/production-ml-library/pml5-general-gguf-delivery.md'),
      Path('docs/factory/production-ml-library/pml0-support-matrix.md'),
      Path('docs/factory/production-ml-library/evidence/qwen36-35b-authority-chain.md'),
  ]
  required = [
      'Qwen3.6-35B-A3B-UD-Q4_K_M.gguf',
      'qwen35moe',
      '22,663,387,424',
      '0b21525e972670ed59e1812e170b27c26355381f0656ecc4e25617ece7dac58b',
      'GGUF-A1c',
  ]
  for path in files:
      text = path.read_text()
      missing = [item for item in required if item not in text]
      assert not missing, f'{path}: missing {missing}'
  receipt = files[-1].read_text()
  for milestone in ('Q0', 'Q1', 'Q2', 'Q3', 'Q4'):
      assert milestone in receipt, f'receipt: missing {milestone}'
  assert 'does not complete' in receipt.lower()
  print('PASS exact Qwen Gradus authority chain')
  PY
  git diff --check -- \
    docs/factory/production-ml-library/CAMPAIGN.md \
    docs/factory/production-ml-library/pml5-general-gguf-delivery.md \
    docs/factory/production-ml-library/pml0-support-matrix.md \
    docs/factory/production-ml-library/evidence/qwen36-35b-authority-chain.md
  ```
- **expected_observed_result**: the Gradus status audit reports zero findings;
  Python prints `PASS exact Qwen Gradus authority chain`; `git diff --check` is
  silent.
- **depends_on**: none.
- **non_goals**: no product code, test, model-byte, source-adapter, backend, or
  Vivi mutation; no support-row promotion above format inspection.
- **risk**: medium. The main risk is accidentally promoting inspection into
  execution or losing a mandatory successor while summarizing the chain.
- **est_work_tokens**: 7k–11k.
- **est_basis**: `pilot` — four bounded authority documents plus one status-
  audit pass, analogous to a documentation/evidence reconciliation packet; no
  compile-heavy ledger class.
- **tool_latency**: low. Grep, Python, Git, and one status-audit run; no
  Cargo or device run.
- **parallel_children_considered**: none. This is one Gradus-owned semantic
  authority update, and the shared documents must commit atomically.
- **stop_condition**: stop and report if the A1b receipt disagrees on filename,
  length, hash, architecture, offset, metadata count, or tensor count; if a
  required successor is missing from either campaign; or if an edit would
  require product source or local model-byte access.

### TRUTH-01B — Radix control plane and historical authority quarantine

- **outcome**: the Radix campaign points to the reconciled Gradus authority,
  records the exact Q0 receipt, and marks the old broad frontier delivery and
  `t1` through `t4` records as historical superseded evidence without deleting
  or rewriting their bodies.
- **write_scope**:
  - `radix/docs/factory/gpu-production-readiness/CAMPAIGN.md`
  - `radix/docs/factory/gpu-production-readiness/frontier-1-delivery.md`
  - `radix/docs/factory/gpu-production-readiness/evidence/frontier-1/t1-status-reconciliation.md`
  - `radix/docs/factory/gpu-production-readiness/evidence/frontier-1/t2-registration-record.md`
  - `radix/docs/factory/gpu-production-readiness/evidence/frontier-1/t3-support-matrix.md`
  - `radix/docs/factory/gpu-production-readiness/evidence/frontier-1/t4-claim-freeze.md`
  - `radix/docs/factory/gpu-production-readiness/evidence/qwen36-35b-truth01-reconciliation.md` (create)
- **read_scope**:
  - the Radix write-scope files before edit;
  - the committed `TRUTH-01A` receipt and Gradus current authorities read-only;
  - Git history for `93878851d`, `b713056c7`, `5a4b4f86c`, `35136c634`, and
    `b6d6e17c8`;
  - `radix/AGENTS.md` and workspace `AGENTS.md`.
- **forbidden_scope**:
  - all Radix/Faber/Hosts product source and tests;
  - semantic rewriting or deletion of historical broad records;
  - new product claims or campaign completion.
- **predecessor_receipts**: committed `TRUTH-01A`; exact-Qwen Radix amendment
  `b6d6e17c8`; historical TRUTH records `93878851d` through `35136c634`.
- **first_failing_oracle**:

  ```bash
  cd <fresh-hand-packet>/radix
  for f in \
    docs/factory/gpu-production-readiness/frontier-1-delivery.md \
    docs/factory/gpu-production-readiness/evidence/frontier-1/t1-status-reconciliation.md \
    docs/factory/gpu-production-readiness/evidence/frontier-1/t2-registration-record.md \
    docs/factory/gpu-production-readiness/evidence/frontier-1/t3-support-matrix.md \
    docs/factory/gpu-production-readiness/evidence/frontier-1/t4-claim-freeze.md
  do
    grep -Fq 'SUPERSEDED FOR CURRENT ROUTING' "$f" || exit 1
    grep -Fq 'Qwen3.6-35B-A3B-UD-Q4_K_M.gguf' "$f" || exit 1
  done
  ```

  Baseline expected result: non-zero because the broad frontier records lack
  the exact-Qwen supersession banner.
- **done_when**:
  1. the Radix campaign links the Gradus exact authority receipt and records
     `TRUTH-01` as complete without changing `LIB-01` or any successor to
     optional/deferred;
  2. each historical broad-era file begins with a concise banner that says
     `SUPERSEDED FOR CURRENT ROUTING`, identifies amendment `b6d6e17c8`, names
     the exact Qwen artifact, links the current Radix campaign and Gradus
     semantic authority, and says the historical body is provenance only;
  3. the old SmolLM claim freeze is explicitly not the current product
     completion contract;
  4. the new Radix Q0 receipt records exact identity, ownership, predecessor
     evidence, remaining `Q1` through `Q4` work, and `LIB-01` next;
  5. Radix's factory status audit is green.
- **closeout_command**:

  ```bash
  cd <fresh-hand-packet>/radix
  ./scripta/check-factory-goal-status --json --fail-on error
  python3 - <<'PY'
  from pathlib import Path

  root = Path('docs/factory/gpu-production-readiness')
  historical = [
      root / 'frontier-1-delivery.md',
      root / 'evidence/frontier-1/t1-status-reconciliation.md',
      root / 'evidence/frontier-1/t2-registration-record.md',
      root / 'evidence/frontier-1/t3-support-matrix.md',
      root / 'evidence/frontier-1/t4-claim-freeze.md',
  ]
  for path in historical:
      head = '\n'.join(path.read_text().splitlines()[:20])
      assert 'SUPERSEDED FOR CURRENT ROUTING' in head, path
      assert 'Qwen3.6-35B-A3B-UD-Q4_K_M.gguf' in head, path
      assert 'b6d6e17c8' in head, path
  campaign = (root / 'CAMPAIGN.md').read_text()
  for unit in ('LIB-01', 'LIB-02', 'LIB-03', 'REF-01', 'MODEL-01', 'MODEL-02',
               'MODEL-03', 'MODEL-04', 'EXEC-01', 'EXEC-02', 'EXEC-03',
               'CAP-01', 'CAP-02', 'CLOSE-01'):
      assert unit in campaign, f'campaign: missing {unit}'
  print('PASS exact Qwen Radix authority chain')
  PY
  git diff --check -- docs/factory/gpu-production-readiness
  ```
- **expected_observed_result**: the Radix status audit reports `"findings": []`;
  Python prints `PASS exact Qwen Radix authority chain`; `git diff --check` is
  silent.
- **depends_on**: `TRUTH-01A` committed and available in the assigned packet.
- **non_goals**: no deletion of historical evidence, no product code, no
  factory archival, no claim that `TRUTH-01` proves any executed model clause.
- **risk**: medium. Provenance can be damaged by rewriting old receipts, while
  a weak banner can leave them looking current. Add-only banners plus one new
  receipt are the clean boundary.
- **est_work_tokens**: 6k–10k.
- **est_basis**: `pilot` — one campaign status/receipt update plus five
  add-only supersession banners and one status-audit pass.
- **tool_latency**: low to medium. The Radix status audit scans factory docs but
  performs no Cargo build or device work.
- **parallel_children_considered**: none. Radix follows the committed Gradus
  authority and must not race it.
- **stop_condition**: stop if the committed `TRUTH-01A` receipt differs from
  the Radix invariant; if the status audit exposes unrelated foreign drift
  that cannot be fixed within exact Qwen planning-doc scope; or if preserving
  history would require deleting or materially rewriting old receipts.

### TRUTH-01C — Cross-repository status-audit and Vivi closeout

- **outcome**: Radix and Gradus documentation gates pass together; both
  campaigns remain active with `LIB-01` / `GGUF-A1c` next; Vivi contains
  exactly one campaign registration and one semantic-delivery registration at
  the reconciled paths; the final receipt states that only Q0 advanced.
- **write_scope**:
  - `radix/docs/factory/gpu-production-readiness/CAMPAIGN.md` status/evidence
    line only if `TRUTH-01` completion is not already recorded by `TRUTH-01B`;
  - `radix/docs/factory/gpu-production-readiness/evidence/qwen36-35b-truth01-reconciliation.md`
    closeout section only;
  - Vivi goal registration through Mind only, and only when read-only
    verification shows a missing, duplicate, or wrong-path Qwen authority.
- **read_scope**:
  - committed `TRUTH-01A` and `TRUTH-01B` receipts;
  - both current campaigns, detailed Gradus delivery, support matrix, and
    status-audit output;
  - read-only `vivi goal list` and `vivi goal show` output.
- **forbidden_scope**:
  - all product source/tests and local model bytes;
  - registration of child stages, Hands, or historical broad records;
  - direct Vivi mutation by a Hand without Mind ownership;
  - closing or archiving either campaign;
  - changing `LIB-01` / `GGUF-A1c` selection.
- **predecessor_receipts**: committed `TRUTH-01A` and `TRUTH-01B`; live
  registrations `gol_634a0417d02c510f` and `gol_67b635603712f01b`.
- **first_failing_oracle**:

  ```bash
  cd /Users/ianzepp/work/faberlang
  vivi goal list --project /Users/ianzepp/work/faberlang --json |
    python3 -c 'import json,sys; rows=json.load(sys.stdin); expected={"radix/docs/factory/gpu-production-readiness/CAMPAIGN.md","gradus/docs/factory/production-ml-library/pml5-general-gguf-delivery.md"}; assert len(rows)==2 and {r["path"] for r in rows}==expected and all(r["exists"] for r in rows); print("PASS two exact Qwen Vivi authorities")'
  ```

  Baseline observed result at planning time: `PASS two exact Qwen Vivi
  authorities`. The red oracle for this unit is therefore cross-repository:
  before `TRUTH-01A` and `TRUTH-01B` land, the final reconciliation receipt and
  historical quarantine checks fail. Do not churn already-correct Vivi state.
- **done_when**:
  1. Gradus and Radix status-audit checks pass from the integrated packet;
  2. Radix factory status audit has zero findings;
  3. a cross-file script proves exact identity and `GGUF-A1c` selection across
     both campaigns, detailed delivery, support matrix, and both Q0 receipts;
  4. every mandatory campaign successor remains present;
  5. Vivi lists exactly the two intended paths, both exist, and `goal show`
     confirms their labels;
  6. both campaign status lines remain `active`;
  7. final receipt says `Q0 advanced; Q1-Q4 incomplete; campaign active`.
- **Vivi correction procedure**: if and only if the read-only oracle fails,
  Mind drops the wrong or duplicate Qwen selector with `vivi goal drop`, then
  adds the missing canonical path with `vivi goal add --path ... --label ...`.
  The implementing Hand records the before/after JSON and does not mutate Vivi
  itself.
- **closeout_command**:

  ```bash
  ROOT=/Users/ianzepp/work/faberlang
  RADIX=<integrated-packet>/radix
  GRADUS=<integrated-packet>/gradus

  cd "$RADIX"
  ./scripta/check-factory-goal-status --json --fail-on error

  cd "$GRADUS"
  ./scripta/check-factory-goal-status --fail-on error

  RADIX="$RADIX" GRADUS="$GRADUS" python3 - <<'PY
  import os
  from pathlib import Path

  paths = [
      Path(os.environ['RADIX']) / 'docs/factory/gpu-production-readiness/CAMPAIGN.md',
      Path(os.environ['RADIX']) / 'docs/factory/gpu-production-readiness/evidence/qwen36-35b-truth01-reconciliation.md',
      Path(os.environ['GRADUS']) / 'docs/factory/production-ml-library/CAMPAIGN.md',
      Path(os.environ['GRADUS']) / 'docs/factory/production-ml-library/pml5-general-gguf-delivery.md',
      Path(os.environ['GRADUS']) / 'docs/factory/production-ml-library/pml0-support-matrix.md',
      Path(os.environ['GRADUS']) / 'docs/factory/production-ml-library/evidence/qwen36-35b-authority-chain.md',
  ]
  required = [
      'Qwen3.6-35B-A3B-UD-Q4_K_M.gguf',
      'qwen35moe',
      '22,663,387,424',
      '0b21525e972670ed59e1812e170b27c26355381f0656ecc4e25617ece7dac58b',
      'GGUF-A1c',
  ]
  for path in paths:
      text = path.read_text()
      missing = [item for item in required if item not in text]
      assert not missing, f'{path}: missing {missing}'
  radix_campaign = paths[0].read_text()
  for unit in ('LIB-01', 'LIB-02', 'LIB-03', 'REF-01', 'MODEL-01', 'MODEL-02',
               'MODEL-03', 'MODEL-04', 'EXEC-01', 'EXEC-02', 'EXEC-03',
               'CAP-01', 'CAP-02', 'CLOSE-01'):
      assert unit in radix_campaign, f'campaign: missing {unit}'
  for campaign in (paths[0], paths[2]):
      status = next(line for line in campaign.read_text().splitlines()
                    if line.startswith('**Status**:'))
      assert status.startswith('**Status**: active'), status
  print('PASS exact Qwen cross-repository authority chain')
  PY

  vivi goal list --project "$ROOT" --json |
    python3 -c 'import json,sys; rows=json.load(sys.stdin); expected={"radix/docs/factory/gpu-production-readiness/CAMPAIGN.md","gradus/docs/factory/production-ml-library/pml5-general-gguf-delivery.md"}; assert len(rows)==2 and {r["path"] for r in rows}==expected and all(r["exists"] for r in rows); print("PASS two exact Qwen Vivi authorities")'
  vivi goal show gol_634a0417d02c510f --project "$ROOT" --json
  vivi goal show gol_67b635603712f01b --project "$ROOT" --json
  git -C "$RADIX" diff --check -- docs/factory/gpu-production-readiness
  git -C "$GRADUS" diff --check -- docs/factory/production-ml-library
  ```
- **expected_observed_result**: both status audits report zero findings;
  cross-file Python prints
  `PASS exact Qwen cross-repository authority chain`; Vivi Python prints `PASS
  two exact Qwen Vivi authorities`; both `goal show` objects have `exists:
  true` and the canonical paths; both `git diff --check` calls are silent.
- **depends_on**: `TRUTH-01A`, then `TRUTH-01B`, both committed and integrated.
- **non_goals**: no product work, no Hand task filing, no new goal registration
  when the current two are already correct, no campaign archive or completion.
- **risk**: medium. Vivi mutation is external control state and status-audit
  results are repository-specific. Verification precedes mutation, and Mind
  owns any corrective registration.
- **est_work_tokens**: 4k–7k.
- **est_basis**: `pilot` — two status-audit checks, one bounded
  cross-file oracle, and one two-row Vivi topology check.
- **tool_latency**: medium. Documentation audit scans are local; no Cargo.
- **parallel_children_considered**: none. This is the serial closeout gate.
- **stop_condition**: stop if Vivi contains an unrecognized third authority
  that cannot be classified without Mind; if either current registration path
  is missing; if the integrated receipts disagree; or if either campaign is
  marked done before `CLOSE-01`.

## 6. Checkpoints And Gates

| Gate | Required evidence | Result of passing |
| --- | --- | --- |
| G1 — semantic chain | `TRUTH-01A` exact Gradus receipt and support row | Gradus authority is current; no product claim |
| G2 — control plane | `TRUTH-01B` exact Radix Q0 receipt and historical banners | Old broad records cannot route work; no product claim |
| G3 — control closeout | `TRUTH-01C` status audits, zero findings, exact two-row Vivi topology | `TRUTH-01` complete; `LIB-01` ready |
| Campaign closeout | `CLOSE-01` after CAP-01 and CAP-02 | Qwen campaign may become done |

**Release checkpoint**: `not-applicable`. TRUTH-01 changes only planning and
control records. No version, tag, artifact publication, or release-prep action
is admitted. Release decisions remain downstream of executed Q4 evidence.

## 7. Validation Summary

The delivery is implementation-ready when:

- every unit has an exact write, read, and forbidden scope;
- each unit has predecessor receipts, a red oracle, a closeout command, and an
  expected observed result;
- estimates use a named basis and state tool latency;
- only named ownership and external-state boundaries split the work;
- the artifact/corpus and hardware/backend boundaries are explicit;
- every campaign successor remains mandatory;
- `TRUTH-01` can pass while the campaign correctly remains active.

No Cargo, model read, device execution, external provider call, or release
command belongs to this planning delivery.

## 8. Companion Skill Plan

- Use campaign run mode to keep `Q0` through `Q4` mandatory.
- Use delivery discipline for each implementation unit.
- Use Vivi only for registration verification and Mind-owned correction.
- Use factory only after Mind admits and files the units.
- Use an independent auditor after `TRUTH-01C` because historical authority
  quarantine and campaign-closure language are claim-critical.

## 9. Open Questions

None block implementation. The current two Vivi registrations are already
correct, so the default is verify-only and no registration mutation. Any
unexpected third registration routes to Mind rather than being dropped by an
implementing Hand.
