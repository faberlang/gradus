# Goal Check: Qwen3.6 35B TRUTH-01 Authority Reconciliation

**Checked**: 2026-08-13
**Evaluator**: `planner-1`, repository-evidence mode
**Goal**: [`radix/docs/factory/gpu-production-readiness/CAMPAIGN.md`](../../../../radix/docs/factory/gpu-production-readiness/CAMPAIGN.md)
**Semantic authority**: [`pml5-general-gguf-delivery.md`](pml5-general-gguf-delivery.md)
**Intended consumer**: delivery, then campaign owners for documentation-only execution
**Verdict**: **READY**

## Reasoning

The exact campaign has one concrete completion artifact, one immutable content
identity, one ownership chain, one mandatory milestone graph, and one selected
next implementation unit. The live Radix and Gradus campaign amendments agree
that the local `Qwen3.6-35B-A3B-UD-Q4_K_M.gguf` artifact is the completion row,
not an optional example. The existing GGUF-A1b receipt proves only guarded
format inspection of that exact artifact. It does not prove tokenization,
materialization, model semantics, generation, residency, Metal, or CUDA.
Those missing results are already mandatory successors rather than planning
ambiguities. TRUTH-01 can therefore reconcile the authority chain without
inventing product architecture or narrowing the campaign.

## Key Points

### Desired end state

One normal Faber package command must verify and admit the exact artifact,
encode operator-supplied Unicode text with the artifact tokenizer, execute the
complete `qwen35moe` graph, generate and decode at least 256 new tokens for two
prompts through one resident model session, match the pinned `llama.cpp`
comparison policy, and produce current Metal and CUDA receipts. The Radix
campaign states every clause and makes `CLOSE-01` the only campaign-completion
gate.

### Grounding

| Fact | Evidence |
| --- | --- |
| Artifact filename | Radix campaign, Gradus campaign, Gradus PML5-GGUF delivery, and `exempla/gguf-inspect/README.md` |
| Architecture | `qwen35moe` in the same authorities and the A1b observed receipt |
| Byte length | `22,663,387,424` in the same authorities and the A1b independent inventory |
| SHA-256 | `0b21525e972670ed59e1812e170b27c26355381f0656ecc4e25617ece7dac58b` in the same authorities and the A1b independent inventory |
| Exact inspection result | `PASS version=3 alignment=32 data=10991392 metadata=55 tensors=753 architecture=qwen35moe` in `exempla/gguf-inspect/README.md` |
| Current next unit | `GGUF-A1c`, mapped to campaign `LIB-01` |
| Baselines | Radix `b6d6e17c8ad7`; Gradus `bc500993c97b`; Faber `1fb6cc97e66d`; Hosts `57d659d60430` |
| Live Vivi authorities | `gol_634a0417d02c510f` for the Radix campaign and `gol_67b635603712f01b` for the Gradus PML5-GGUF delivery |

### Architecture decisions

Ownership is settled. Gradus owns GGUF semantics, tokenizer behavior, model
configuration, graph semantics, and logical model state. Radix owns lowering,
fusion, generated kernels, and `DeviceProgram`. Faber owns package, build, and
run composition. Hosts owns file/range resolution, physical allocation,
residency, upload, launch, synchronization, and teardown. No Gradus semantic
value may acquire a path, URL, file descriptor, mapping, device handle, or
whole-model byte list.

### Boundaries

TRUTH-01 is planning-document and control-record reconciliation only. It may
update the Radix campaign, the Gradus campaign and delivery, the Gradus support
matrix, generated factory indexes, historical supersession banners, and the
Qwen authority receipt. It may verify or, through Mind, reconcile the two Vivi
goal registrations. It may not edit product source or tests, read or copy
operator model bytes, run paid infrastructure, claim GPU execution, or mark the
campaign complete.

### Acceptance and validation

The delivery artifact names exact red and closeout oracles for each unit. The
final closeout checks exact cross-file identity, explicit historical
supersession, current generated indexes, zero Radix factory-status findings,
and exactly the two intended Vivi goal registrations. The observed A1b line is
retained as format-inspection evidence and is explicitly barred from satisfying
Q1 through Q4.

### Implementation handoff

The first implementation-ready frontier is `TRUTH-01A`. It reconciles the
Gradus semantic chain and creates the exact authority receipt. `TRUTH-01B`
then quarantines the superseded broad Radix frontier records without rewriting
their historical bodies. `TRUTH-01C` performs cross-repository and Vivi
closeout, keeps both campaigns active, and selects `LIB-01` / `GGUF-A1c` next.

### Staleness

The old Radix frontier-1 delivery and `t1` through `t4` evidence predate the
2026-08-13 exact-Qwen campaign amendment. They contain broad-platform and
SmolLM-first-claim language, including an explicit historical non-claim for
Qwen. Their evidence remains historical, but they cannot remain
unqualified current authority. The delivery therefore requires provenance-
preserving supersession banners rather than deletion or content rewriting.

## Blocking Gaps

None for TRUTH-01 lowering. Product evidence gaps are mandatory implementation
successors, not missing planning decisions.

## Recommended Next Step

Execute [`pml5-qwen36-truth01-delivery.md`](pml5-qwen36-truth01-delivery.md),
starting with `TRUTH-01A`. After `TRUTH-01C` closes, route `LIB-01` /
`GGUF-A1c` to factory. `READY` is a planning-readiness verdict, not a GO stamp
or a campaign-completion claim.
