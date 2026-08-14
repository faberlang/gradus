# MODEL-04 Delivery — Full-Model Qwen3.6 Reference Inference

**Status**: lowered 2026-08-14 — dispatch-ready micro-unit graph MODEL-04-M1..M7 plus the aggregate gate MODEL-04-G; no Hand task is filed by this Planner (Mind dispatches after delivery audit and predecessor receipts); no unit narrows the GGUF-M4 done oracle
**Created**: 2026-08-14
**Planner**: planner-29 (task `2f9c2eea`)
**Campaign**: [`radix/docs/factory/gpu-production-readiness/CAMPAIGN.md`](../../../../radix/docs/factory/gpu-production-readiness/CAMPAIGN.md) — Qwen3.6 35B GGUF execution
**Campaign row**: MODEL-04
**Delivery authority** (read-only): [`pml5-general-gguf-delivery.md`](pml5-general-gguf-delivery.md) GGUF-M4 section
**Repo**: `gradus`
**Granularity bar**: operator directive 2026-08-14 — every unit is one behavior family, executable by a Hand in roughly 10–15 minutes (focused check + commit + close), carrying all 8 campaign-rule-2 fields
**Repo baseline**: Gradus `bc500993c97b` (packet tip at lowering)

## P0 — Unit Identity In The Campaign Graph

Campaign row MODEL-04 (Mandatory Work table):

> **Execute full-model Qwen3.6 reference inference** | Gradus | REF-01, MODEL-02, MODEL-03 | Both prompts traverse every layer and match declared reference logits/tokens/text

Done-oracle in the delivery authority (GGUF-M4):

> Compose embeddings, all hybrid layers, normalization, output projection, tokenizer, sampling, and logical model state into the public Gradus generation surface. **Done when**: the exact artifact accepts two arbitrary prompts and produces matching reference logits/tokens and decoded text for a bounded CPU/reference run. Any resource-limited reference mode must still execute every layer and must not substitute a reduced model.

Campaign dependency chain (only the affected edges):

```text
TRUTH-01 -> LIB-01 -> {LIB-02, LIB-03} -> REF-01 -> MODEL-01
     -> {MODEL-02, MODEL-03} -> MODEL-04 -> {EXEC-01, EXEC-02} -> EXEC-03
     -> {CAP-01, CAP-02} -> CLOSE-01
```

**Successor chain preserved unchanged.** EXEC-01 and EXEC-02 keep their campaign
rows and their gate on MODEL-04: EXEC-01-U2 builds the real-graph composite
plan over the GGUF-M4 public generation surface and is gated on the MODEL-04
receipt; EXEC-02's packed native kernels consume the reference policy this
delivery executes against. Nothing in this delivery narrows, defers,
downgrades, or moves those successors or their successors (EXEC-03, CAP-01/02,
CLOSE-01). This delivery is the Gradus-side lowering of GGUF-M4 per the unit
admission ratchet; it does not itself satisfy any EXEC-*/CAP-*/CLOSE-01 row.

## P1 — Interpreted Theme (GGUF-M4, at micro-unit scale)

GGUF-M4 is the composition milestone of the Gradus delivery: every behavior
family it needs already exists as a delivered predecessor behavior — REF-01's
dense forward operations and prefill/decode/KV semantics, MODEL-02's router and
expert execution, MODEL-03's hybrid SSM/attention state, GGUF-A2's artifact
tokenizer, and the PML5 generation/sampling/decode/cache modules. MODEL-04
composes those behaviors into the complete `qwen35moe` graph and proves, on a
bounded CPU/reference run, that two operator prompts traverse every layer and
match the declared reference logits/tokens/text.

The theme is therefore **composition + executed reference receipt**, not new
primitives. The unit graph is serial — each unit extends one behavior family of
the composed surface and its executed proof, in the order a full-model
reference run needs: graph assembly → prefill → decode → generation surface →
session reuse → reference comparison → receipt. No unit is a micro-edit
wrapped in process and no unit is a multi-behavior bag; each is one behavior
family at 10–15 minutes of Hand time (focused check + commit + close).

## P2 — Repo-Aware Baseline

Verified 2026-08-14 against the packet tip (clean, branch `factory/planner-29`).
Grounded facts ("measured, not claimed"; a `*` marks dispatch-time re-records):

| Fact | Value | Source |
| --- | --- | --- |
| Gradus tip | `bc500993c97b` | `git rev-parse HEAD` |
| Target artifact | `/Users/ianzepp/ai/models/Qwen3.6-35B-A3B-UD-Q4_K_M.gguf` (operator-local, never committed) | ORACLE delivery §Repo-Aware Baseline |
| Target bytes* | 22,663,387,424 | pinned invariant; re-record at dispatch |
| Target SHA-256* | `0b21525e972670ed59e1812e170b27c26355381f0656ecc4e25617ece7dac58b` | pinned invariant; re-record at dispatch |
| GGUF facts | v3, alignment 32, data offset 10,991,392, metadata 55, tensors 753, architecture `qwen35moe` | gguf-inspect A1b receipt |
| Frozen probes | probe A 212 bytes SHA-256 `cab14ac3…262f`; probe B 767 bytes SHA-256 `ca3957e4…1d75` (NFC, no trailing newline) | ORACLE delivery §Frozen Probes |
| Reference oracle | llama.cpp 10150 (`dee2a846b`), Homebrew, burgus; comparison contract frozen in ORACLE-P | ORACLE delivery (read-only) |
| Target-row checkpoints | `gradus/fixtures/oracle/qwen36-35b/` (tokenizer ids, logit windows, greedy traces, band) | ORACLE-CAP (parallel delivery; read-only here) |
| Predecessor behavior modules | `src/decode.fab`, `src/cache.fab`, `src/sampling.fab`, `src/generation.fab` (PML5); `src/tokenizer.fab` (PML2/LIB-02); `src/model/{artifact,gguf_manifest,dequant}.fab` | live `src/` |
| No `qwen35moe` module yet | `src/model/` has artifact/capsule/dequant/gguf_manifest/gguf/safetensors only | `ls src/model/` |
| Executed-proof vehicle | `exempla/*` packages, `build.target = "fmir"`, run via `faber run --target fmir`; `scripta/check-source` + `scripta/check-compile` gates | A1a/A1b receipts, `scripta/` |
| Execution blocker status | FMIR library-call gap resolved (A1a package-MIR receipt is executed); focused `faber test` remains provider-blocked | pml5-closeout CTO8-1, A1a receipt |

Gap (this delivery's reason to exist): the composed full-model forward, its
executed reference prefill/decode, the two-prompt session proof, and the
reference comparison record do not exist yet. Everything MODEL-04 composes is
on its predecessor chain; nothing here invents a new primitive or a new
architecture family.

## P3 — Unit Graph (one behavior family per unit)

```text
MODEL-04-M1  Full-model forward assembly — the composed qwen35moe graph
             (embeddings + every hybrid layer in the declared schedule +
             final norm + output projection over the 753-tensor map)    — root of the chain
MODEL-04-M2  Full-model prefill — both frozen probes traverse every layer,
             per-layer prefill logits                                    — after M1
MODEL-04-M3  Full-model autoregressive decode — ≥256 new tokens, every
             layer, KV/SSM state resident, no per-token reload           — after M2
MODEL-04-M4  Generation surface — sampling-config mapping + detokenized
             text for both prompts through the public Gradus surface     — after M3
MODEL-04-M5  Two-prompt session semantics — second prompt through the same
             admitted model session; reset/reuse deterministic           — after M4
MODEL-04-M6  Reference comparison — both prompts' logits/tokens/text vs
             the pinned llama.cpp checkpoints under the comparison
             contract; first-divergence record                           — after M5
MODEL-04-M7  MODEL-04 reference receipt + closeout                        — after M6
Gate:        MODEL-04-G  (single aggregate gate — see below)
```

Dependency edges: **M1 → M2 → M3 → M4 → M5 → M6 → M7**; campaign edge
**{REF-01, MODEL-02, MODEL-03} receipts → M1** (all M4 units ride the same
campaign predecessor edge — M1 is the first consumer); read-only edges
**ORACLE-CAP target-row checkpoints → M2/M6** and **ORACLE-TOOL
`scripta/oracle/**` → M6**. The chain is serial because each unit's behavior
family is the next phase of the same reference run; there is no disjoint
write surface to parallelize. **No child lane gates** — only MODEL-04-G.

### Granularity compliance

Each unit is exactly one behavior family of the GGUF-M4 done oracle
(assembly / prefill / decode / generation surface / session reuse / comparison
/ receipt), targeted at ~10–15 minutes of Hand time (focused check + commit +
close). The unit tables carry all 8 campaign-rule-2 fields: `outcome`, exact
`write_scope`, `first_failing_oracle`, `closeout_command`,
`expected_observed_result`, `est_basis`, `stop_condition`, and `depends_on`
(+ `est_work_tokens`). Nothing below splits one behavior family into intra-unit
phases, and no unit covers two families.

## P4 — Units

### MODEL-04-M1 — Full-model forward assembly (the composed qwen35moe graph)

| Field | Value |
| --- | --- |
| `outcome` | **Compose the complete `qwen35moe` forward graph** from the admitted configuration (MODEL-01, read-only) and the delivered per-layer behavior families (REF-01 dense forward ops, MODEL-02 router/expert, MODEL-03 hybrid SSM/attention): embedding gather → every hybrid layer in the declared schedule (attention/SSM layers and MoE FFN in the architecture's order) → final normalization → output projection, consuming the 753-tensor map. One behavior family: the full ordered layer stack. Executed proof: the assembly probe asserts the declared schedule runs in order over the admitted configuration with no skipped or reordered layer — first-divergence `none` at the structural boundary. |
| `write_scope` | `src/model/qwen35moe_graph.fab` (new module — the composed full-model forward + its public surface); `src/model/qwen35moe_graph.proba` (new — forward-assembly cases: declared layer schedule, no-skip traversal, ordered composition); `docs/module-map.md` (new module row); `docs/api-reference.md` (new public surface rows); `docs/regression-corpus.md` (new proba inventory + suite totals + doc-version bump); `README.md` (module row) |
| `read_scope` | `src/model/artifact.fab`, `src/model/gguf_manifest.fab`, `src/model/dequant.fab` (identity/manifest/dequant surfaces); REF-01/MODEL-02/MODEL-03 delivered modules (read-only); MODEL-01 admitted configuration + tensor map (read-only); `src/decode.fab`, `src/cache.fab`, `src/sampling.fab`, `src/generation.fab`, `src/tokenizer.fab` (consumed behavior contracts); ORACLE-P policy (first-divergence record shape, read-only) |
| `forbidden_paths` | Real artifact bytes; `hosts/**`; `radix/**` product; `faber/**`; `inferentia/**`; `gradus/fixtures/oracle/**` (ORACLE owns, read-only); `gradus/scripta/oracle/**` (ORACLE-TOOL owns); `exempla/qwen36-35b-inference/**` (M2+ owns the reference-inference phases; GGUF-M6 owns the final capstone); CAMPAIGN.md status lines (CLOSE-01 owns); any Metal/CUDA execution claim (EXEC-02/M5) |
| `depends_on` | **REF-01 + MODEL-02 + MODEL-03 receipts** (campaign edge MODEL-04 ← {REF-01, MODEL-02, MODEL-03}); MODEL-01 admission facts read-only. No MODEL-04 unit precedes M1. |
| `done_when` | The composed forward executes the declared layer schedule in order over the admitted configuration (assembly proba PASS, first-divergence `none` at the structural boundary); `./scripta/check-source` and `./scripta/check-compile` exit 0; `git diff --check` clean; regression-corpus totals updated. |
| `integrable` | Yes — the new module + proba + doc rows are self-consistent on `factory/merge` once M1 lands alone; M2 extends the same module. |
| `first_failing_oracle` | `./scripta/check-compile` fails red before implementation (no `qwen35moe_graph` module; the assembly proba cannot type-check). First recorded divergence at closeout: any layer-count/schedule mismatch vs the admitted configuration (first diverging layer named). Record the failing command + first divergence. |
| `closeout_command` | `cd /Users/ianzepp/work/faberlang/worktrees/<hand>/gradus`; `./scripta/check-source`; `env FABER_LIBRARY_HOME=/Users/ianzepp/work/faberlang/worktrees/<hand> FABER_BIN=/Users/ianzepp/work/faberlang/worktrees/<hand>/radix/target/debug/faber ./scripta/check-compile`; `git diff --check -- src/model/qwen35moe_graph.fab src/model/qwen35moe_graph.proba docs/module-map.md docs/api-reference.md docs/regression-corpus.md README.md` |
| `expected_observed_result` | `check-source` and `check-compile` exit 0; assembly proba PASS with the declared layer schedule in order and first-divergence `none`; `git diff --check` silent. No model bytes, no execution claim beyond the structural probe. |
| `est_work_tokens` | 3k–6k |
| `est_basis` | Composition-row precedent at micro-unit scale: GGUF-A4 dense full-model assembly (REF-01's predecessor, same composition shape) and EXEC-01-U1 typed-shape assembly (3k–8k); one new module + proba + doc rows. |
| `tool_latency` | gradus `faber check` + compile ~1–5 min (no cargo in the gradus dev loop) |
| `local_corpus_boundary` | No artifact bytes; identity facts (digest, byte length, tensor counts) only. |
| `hardware/backend authority` | None — structural probe only; no machine run in this unit. |
| `stop_condition` | Stop and route a need when the admitted `qwen35moe` configuration cannot represent the required layer schedule (missing architecture fact — MODEL-01 gate), when a predecessor receipt is absent, or when the composed forward would require whole-model F32 expansion of a tensor with no reference path. |

### MODEL-04-M2 — Full-model prefill: both prompts traverse every layer

| Field | Value |
| --- | --- |
| `outcome` | **Full-model prefill over the composed graph** — both frozen probes (ORACLE probe A, 212 bytes; probe B, 767 bytes) encode through the artifact tokenizer and their full context traverses every hybrid layer; per-position prefill logits recorded per prompt. One behavior family: teacher-forced full-context prefill across every layer. Executed proof: the reference-mode prefill run prints both prompts' per-layer traversal (every layer visited) and per-position logits. |
| `write_scope` | `src/model/qwen35moe_graph.proba` (prefill cases — both probes, per-layer traversal assertions, prefill-logit pins); `exempla/qwen36-35b-inference/src/main.fab` (reference-mode prefill phase); `exempla/qwen36-35b-inference/README.md` (prefill receipt section: commands, prompt hashes, per-layer traversal, first divergence); `docs/regression-corpus.md` (suite totals) |
| `read_scope` | `gradus/fixtures/oracle/probes/` (probe files, ORACLE-owned, read-only); `gradus/fixtures/oracle/qwen36-35b/` tokenizer checkpoints (ORACLE-CAP, read-only — if not yet landed, the proba pins tokenizer ids from GGUF-A2/LIB-02 and M6 closes the oracle comparison); the composed graph (M1); GGUF-A2 tokenizer runtime |
| `forbidden_paths` | Same as M1; plus no prompt or token-id fallback hard-coded into the capstone path (GGUF-A2 rule — the artifact tokenizer is the only encoder); no skipping any layer in a resource-limited mode |
| `depends_on` | MODEL-04-M1; campaign predecessors via M1; ORACLE-CAP tokenizer checkpoints read-only |
| `done_when` | Both probes encode via the artifact tokenizer and traverse every layer in the executed reference-mode prefill (proba PASS, first-divergence `none` at the prefill boundary); prefill receipt section committed; `check-source`/`check-compile` exit 0; `git diff --check` clean. |
| `integrable` | Yes — prefill phase + proba + exempla receipt are self-consistent; M3 extends the same exempla run. |
| `first_failing_oracle` | The prefill proba fails red before implementation (no prefill path on the composed graph). First recorded divergence at closeout: the first tokenizer id (probe encode mismatch vs the pinned tokenizer ids) or the first layer whose prefill logits diverge — the first-failing layer named. Record the failing command + first divergence. |
| `closeout_command` | `cd /Users/ianzepp/work/faberlang/worktrees/<hand>/gradus`; `./scripta/check-source`; `env FABER_LIBRARY_HOME=/Users/ianzepp/work/faberlang/worktrees/<hand> FABER_BIN=/Users/ianzepp/work/faberlang/worktrees/<hand>/radix/target/debug/faber ./scripta/check-compile`; `env FABER_LIBRARY_HOME=/Users/ianzepp/work/faberlang/worktrees/<hand> /Users/ianzepp/work/faberlang/worktrees/<hand>/radix/target/debug/faber run --target fmir exempla/qwen36-35b-inference`; `git diff --check -- src/model/qwen35moe_graph.proba exempla/qwen36-35b-inference docs/regression-corpus.md` |
| `expected_observed_result` | The reference-mode run prints both prompts' per-layer traversal (N layers each, every layer visited, no reduced model) and per-position prefill logits; proba PASS; probe hashes verified against the pins before use; `git diff --check` silent. |
| `est_work_tokens` | 3k–6k |
| `est_basis` | Prefill-row precedent at micro-unit scale: GGUF-A5 prefill/decode-equivalence rows and ORACLE-CAP probe-window capture shape (read-only reference); one probe phase + exempla phase + receipt section. |
| `tool_latency` | Medium-high — the 22.6 GB reference-mode prefill on CPU is bounded but not instant (tens of minutes); Hand writing time stays 10–15 min. |
| `local_corpus_boundary` | The target artifact stays operator-local; only probe hashes, tokenizer ids, per-layer facts, and logit checkpoints are committed — never model bytes. |
| `hardware/backend authority` | burgus CPU/reference run only; no Metal/CUDA claim (EXEC-02/M5 own native execution). |
| `stop_condition` | Stop and route a need when either probe does not reproduce its pinned bytes/hash (probe change is an operator decision), when the artifact identity differs from the pinned invariant, when a prefill position diverges before all layers are traversed, or when a resource-limited reference mode would skip a layer. |

### MODEL-04-M3 — Full-model autoregressive decode (≥256 tokens, every layer, resident state)

| Field | Value |
| --- | --- |
| `outcome` | **Incremental autoregressive decode through every hybrid layer** from the prefill state — at least 256 new tokens per prompt, model state (KV + SSM) resident across the loop, no per-token reload/recompile/rebuild; the greedy token trace recorded per prompt. One behavior family: full-model decode. Executed proof: the reference-mode decode run prints the 256-token trace plus resident-state facts. |
| `write_scope` | `src/model/qwen35moe_graph.proba` (decode cases — 256-token greedy traces, resident-state assertions, no-reload counters); `exempla/qwen36-35b-inference/src/main.fab` (reference-mode decode phase); `exempla/qwen36-35b-inference/README.md` (decode receipt section); `docs/regression-corpus.md` (suite totals) |
| `read_scope` | `gradus/fixtures/oracle/qwen36-35b/` greedy traces (ORACLE-CAP, read-only); GGUF-A5 per-layer KV/SSM prefill/decode equivalence (REF-01 predecessor, read-only); the composed graph + prefill state (M1/M2) |
| `forbidden_paths` | Same as M2; no per-token reload path, no whole-model F32 re-materialization between tokens, no GPU/device claim |
| `depends_on` | MODEL-04-M2 |
| `done_when` | The decode loop emits ≥256 new tokens per prompt through every layer with state resident across the loop (proba PASS, first-divergence `none` at the decode boundary); no-reload facts recorded; decode receipt section committed; `check-source`/`check-compile` exit 0; `git diff --check` clean. |
| `integrable` | Yes — decode phase extends the same exempla run; M4 adds the text surface. |
| `first_failing_oracle` | The decode proba fails red before implementation (no decode path on the composed graph). First recorded divergence at closeout: the first decode position whose greedy top-1 differs from the ORACLE-CAP greedy trace (position, comparator value, candidate value, failing thresholds). Record the failing command + first divergence. |
| `closeout_command` | `cd /Users/ianzepp/work/faberlang/worktrees/<hand>/gradus`; `./scripta/check-source`; `env FABER_LIBRARY_HOME=/Users/ianzepp/work/faberlang/worktrees/<hand> FABER_BIN=/Users/ianzepp/work/faberlang/worktrees/<hand>/radix/target/debug/faber ./scripta/check-compile`; `env FABER_LIBRARY_HOME=/Users/ianzepp/work/faberlang/worktrees/<hand> /Users/ianzepp/work/faberlang/worktrees/<hand>/radix/target/debug/faber run --target fmir exempla/qwen36-35b-inference`; `git diff --check -- src/model/qwen35moe_graph.proba exempla/qwen36-35b-inference docs/regression-corpus.md` |
| `expected_observed_result` | The reference-mode run prints ≥256 new tokens per prompt with their ids; the greedy trace matches the pinned trace (first-divergence `none`); resident-state/no-reload counters recorded; proba PASS; `git diff --check` silent. |
| `est_work_tokens` | 3k–6k |
| `est_basis` | Decode-loop precedent at micro-unit scale: PML5-U1 decode-loop rows (bdefb5a) and GGUF-A5 incremental-decode rows (same loop semantics, composed graph); one loop phase + proba + receipt section. |
| `tool_latency` | Medium-high — 256-token CPU decode of the 35B reference run is bounded but not instant; Hand writing time stays 10–15 min. |
| `local_corpus_boundary` | Same as M2 — derived token ids/traces only, never model bytes. |
| `hardware/backend authority` | burgus CPU/reference run only; no Metal/CUDA claim. |
| `stop_condition` | Stop and route a need when decode would require per-token reload/rebuild, when the ≥256-token bound cannot complete in the bounded reference run, when KV/SSM state is not resident across the loop, or when a divergence appears before the token bound (record first divergence per the first-divergence rule). |

### MODEL-04-M4 — Generation surface: sampling + detokenized text

| Field | Value |
| --- | --- |
| `outcome` | **Wire the public Gradus generation surface** for the full model — the composed graph + artifact tokenizer + the reference sampling policy (per the ORACLE comparison contract: greedy `temperature 0`, `top_k 40`, `top_p 0.95`, `min_p 0.05`, `repeat_penalty 1.0`) produce deterministic token streams, and detokenization renders both prompts' decoded text. One behavior family: the full-model generation surface (logits → tokens → text). Executed proof: the reference-mode run prints both prompts' generated text and token ids. |
| `write_scope` | `src/model/qwen35moe_graph.fab` (generation-surface op wiring — sampling-config mapping + decode + detokenize over the composed graph); `src/model/qwen35moe_graph.proba` (text-surface cases — ids→text round trips, sampling-config mapping, deterministic pins); `exempla/qwen36-35b-inference/src/main.fab` (reference-mode text output phase); `exempla/qwen36-35b-inference/README.md` (text receipt section); `docs/api-reference.md` (generation-surface op rows); `docs/diagnostics.md` (typed generation-surface diagnostics if any new first-divergence error surface is added); `docs/regression-corpus.md` (suite totals) |
| `read_scope` | `src/generation.fab` + `src/sampling.fab` (config/authority contracts, read-only); `src/tokenizer.fab` (detokenize, read-only); ORACLE comparison contract (sampling surface — read-only); `gradus/fixtures/oracle/qwen36-35b/` decoded-text checkpoints (ORACLE-CAP, read-only) |
| `forbidden_paths` | Same as M3; no second generation-config authority (GGUF-A2/PML5-U4 single-authority rule — `generation.fab` stays the authority, this unit adapts); no text-level similarity as a substitute for token-level correctness |
| `depends_on` | MODEL-04-M3 |
| `done_when` | Both prompts' generated text matches the pinned decoded-text checkpoints (proba PASS, first-divergence `none` at the text boundary); sampling-config mapping is deterministic; generation-surface rows committed; `check-source`/`check-compile` exit 0; `git diff --check` clean. |
| `integrable` | Yes — the generation-surface op + proba + exempla text phase are self-consistent; M5 adds the second-prompt session run. |
| `first_failing_oracle` | The text-surface proba fails red before implementation (no generation-surface op). First recorded divergence at closeout: the first generated token whose decoded text differs from the pinned oracle decoded text (token id + text named). Record the failing command + first divergence. |
| `closeout_command` | `cd /Users/ianzepp/work/faberlang/worktrees/<hand>/gradus`; `./scripta/check-source`; `env FABER_LIBRARY_HOME=/Users/ianzepp/work/faberlang/worktrees/<hand> FABER_BIN=/Users/ianzepp/work/faberlang/worktrees/<hand>/radix/target/debug/faber ./scripta/check-compile`; `env FABER_LIBRARY_HOME=/Users/ianzepp/work/faberlang/worktrees/<hand> /Users/ianzepp/work/faberlang/worktrees/<hand>/radix/target/debug/faber run --target fmir exempla/qwen36-35b-inference`; `git diff --check -- src/model/qwen35moe_graph.fab src/model/qwen35moe_graph.proba exempla/qwen36-35b-inference docs/api-reference.md docs/diagnostics.md docs/regression-corpus.md` |
| `expected_observed_result` | The reference-mode run prints both prompts' decoded text and token ids matching the pinned checkpoints (first-divergence `none`); sampling-config mapping deterministic; proba PASS; `git diff --check` silent. |
| `est_work_tokens` | 3k–6k |
| `est_basis` | Surface-wiring precedent at micro-unit scale: GGUF-A2 encode/decode round-trip rows and PML5-U4 config-mapping rows (same mapping shape onto a composed graph); one op + proba + docs rows. |
| `tool_latency` | Medium — the text-surface run reuses the M3 decode trace plus detokenize; extra minutes only. |
| `local_corpus_boundary` | Same as M3 — derived text/token ids only. |
| `hardware/backend authority` | burgus CPU/reference run only; no device claim. |
| `stop_condition` | Stop and route a need when the artifact tokenizer cannot round-trip the generated ids to text, when the sampling-config surface would diverge from the pinned comparison contract, or when the generation surface would duplicate the generation-config authority. |

### MODEL-04-M5 — Two-prompt session semantics (same admitted model session)

| Field | Value |
| --- | --- |
| `outcome` | **The second prompt runs through the same admitted model session** — weights + KV/SSM state resident between prompts; reset/reuse deterministic; probe B's prefill+decode in-session produces its own matching reference output without reload. One behavior family: session reuse across prompts. Executed proof: the reference-mode session run executes probe A then probe B in one session and prints both prompts' receipts plus reuse/reset facts. |
| `write_scope` | `src/model/qwen35moe_graph.proba` (session cases — two prompts in one session, in-session output equals fresh-session output, reset/reuse determinism); `exempla/qwen36-35b-inference/src/main.fab` (reference-mode session phase); `exempla/qwen36-35b-inference/README.md` (session receipt section); `docs/regression-corpus.md` (suite totals) |
| `read_scope` | GGUF-A5 reset/reuse semantics (REF-01 predecessor, read-only); PML5-U5 session/reset rows (read-only); the composed graph + generation surface (M1/M4) |
| `forbidden_paths` | Same as M4; no per-prompt model reload/recompile/rebuild; no device residency claim (EXEC-03 owns physical residency) |
| `depends_on` | MODEL-04-M4 |
| `done_when` | Probe B in-session output equals its fresh-session reference (proba PASS, first-divergence `none` at the session boundary); reuse/reset facts recorded; session receipt section committed; `check-source`/`check-compile` exit 0; `git diff --check` clean. |
| `integrable` | Yes — session phase extends the same exempla run; M6 compares the aggregate reference record. |
| `first_failing_oracle` | The session proba fails red before implementation (no session-reuse path). First recorded divergence at closeout: the first position where the in-session second-prompt state/output diverges from the fresh-session reference. Record the failing command + first divergence. |
| `closeout_command` | `cd /Users/ianzepp/work/faberlang/worktrees/<hand>/gradus`; `./scripta/check-source`; `env FABER_LIBRARY_HOME=/Users/ianzepp/work/faberlang/worktrees/<hand> FABER_BIN=/Users/ianzepp/work/faberlang/worktrees/<hand>/radix/target/debug/faber ./scripta/check-compile`; `env FABER_LIBRARY_HOME=/Users/ianzepp/work/faberlang/worktrees/<hand> /Users/ianzepp/work/faberlang/worktrees/<hand>/radix/target/debug/faber run --target fmir exempla/qwen36-35b-inference`; `git diff --check -- src/model/qwen35moe_graph.proba exempla/qwen36-35b-inference docs/regression-corpus.md` |
| `expected_observed_result` | The session run prints both prompts' receipts from one admitted model session; in-session probe B equals fresh-session probe B (first-divergence `none`); reuse/reset facts (no reload, deterministic replay) recorded; proba PASS; `git diff --check` silent. |
| `est_work_tokens` | 3k–5k |
| `est_basis` | Session-row precedent at micro-unit scale: PML5-U5 reset/limits/cancellation rows (8cf798a) and GGUF-A5 reset/reuse rows (same semantics over the composed session); one session phase + proba + receipt section. |
| `tool_latency` | Medium — one extra full prefill+decode for probe B in-session. |
| `local_corpus_boundary` | Same as M4 — derived facts only. |
| `hardware/backend authority` | burgus CPU/reference run only; state residency is logical (Gradus values), not physical device residency. |
| `stop_condition` | Stop and route a need when the in-session second-prompt state diverges from the fresh-session reference, when state is not resident between prompts, or when reset/reuse is not deterministic. |

### MODEL-04-M6 — Reference comparison against the pinned oracle

| Field | Value |
| --- | --- |
| `outcome` | **The full MODEL-04 reference comparison** — both prompts' logits/tokens/text vs the pinned llama.cpp checkpoints (ORACLE-CAP `gradus/fixtures/oracle/qwen36-35b/`) under the comparison contract: exact greedy top-1 token equality at every trace position, top-5 overlap ≥ 4/5 at positions 0..15, per-element full-vocab band |logp_oracle − logp_candidate| ≤ Δ at positions 0..2, finite gate, first-divergence rule — run through the ORACLE first-divergence tooling. One behavior family: declared-reference matching. Executed proof: the comparison run produces the MODEL-04 first-divergence record for both prompts. |
| `write_scope` | `docs/factory/production-ml-library/model04-reference-comparison-record.md` (new — per prompt: comparison contract version, Δ/band facts, greedy top-1 equality, top-5 overlap, finite gate, first divergence or `none`, comparator + candidate values, revisions); `exempla/qwen36-35b-inference/README.md` (comparison section linking the record) |
| `read_scope` | `gradus/fixtures/oracle/qwen36-35b/` checkpoints (ORACLE-CAP, read-only); `gradus/scripta/oracle/compare.py` + `oracle-receipt-schema-1.0.0` (ORACLE-TOOL, read-only — exact CLI binds at dispatch once ORACLE-TOOL lands); ORACLE-P comparison contract (read-only); the reference-mode candidate record (M2–M5) |
| `forbidden_paths` | `gradus/scripta/oracle/**` (ORACLE-TOOL owns — compare/capture/verify tooling is consumed, never edited); `gradus/fixtures/oracle/**` (ORACLE owns — checkpoints never edited); product code in any repo; any band change to admit a divergence |
| `depends_on` | MODEL-04-M5; ORACLE-CAP target-row checkpoints + ORACLE-TOOL tooling read-only (must have landed) |
| `done_when` | The comparison record shows both prompts' full-vocab window within band Δ, top-5 overlap ≥ 4/5 at 0..15, greedy top-1 equality at every trace position, finite gate PASS, and first-divergence `none` (or the recorded first divergence naming the first position, kind, comparator value, candidate value, and failing thresholds); record committed; `git diff --check` clean. |
| `integrable` | Yes — the comparison record is evidence; EXEC-01/EXEC-02 consume the MODEL-04 receipt (M7), not this record directly. |
| `first_failing_oracle` | The comparison run's first detected divergence that the ORACLE tooling reports at a different position/kind than the candidate's own first-divergence record (tool oracle mismatch — the tool's own oracle fails first). Red state before implementation: the absent comparison record. Record the failing command + first divergence. |
| `closeout_command` | `cd /Users/ianzepp/work/faberlang/worktrees/<hand>/gradus`; run the ORACLE first-divergence tooling against the reference-mode candidate record (consumed surface: `scripta/oracle/compare.py --row qwen36-35b`, exact CLI binds at dispatch per ORACLE-TOOL) writing `docs/factory/production-ml-library/model04-reference-comparison-record.md`; `git diff --check -- docs/factory/production-ml-library/model04-reference-comparison-record.md exempla/qwen36-35b-inference/README.md` |
| `expected_observed_result` | Both prompts pass the full comparison contract (band Δ, top-5 overlap, greedy top-1 equality, finite gate) with first-divergence `none`; the record names the contract version, Δ/band facts, revisions, and both prompts' facts; `git diff --check` silent. |
| `est_work_tokens` | 3k–5k |
| `est_basis` | Comparison-row precedent at micro-unit scale: ORACLE-TOOL self-test rows and GI0-6 first-divergence-rule rows (same contract, one candidate record); one tool invocation + evidence record. |
| `tool_latency` | Low-medium — the comparison reads committed checkpoints + the candidate record; no model load. |
| `local_corpus_boundary` | Checkpoints and candidate records only; never model bytes. |
| `hardware/backend authority` | None — comparison only; oracle captures already recorded (burgus). |
| `stop_condition` | Stop and route a need when a divergence is not `none` — record the first divergence per the first-divergence rule and route the owning surface (per campaign execution rule 5: the first failing tokenizer id / tensor / layer / state update / logit / token); never hide behind text-level similarity; never change the comparison band to admit. |

### MODEL-04-M7 — MODEL-04 reference receipt + closeout

| Field | Value |
| --- | --- |
| `outcome` | **The executed MODEL-04 reference receipt** — both prompts, every layer, matching reference logits/tokens/text on the bounded CPU/reference run — carrying every campaign receipt clause (exact command + working directory; Gradus/Radix/Faber revisions; model filename, byte length, SHA-256; tokenizer/chat-template identity + prompt hashes; hardware/OS/backend; tensor storage types; observed token ids + decoded text; comparison policy + first divergence; load/prefill/decode timing + peak memory; reset/reuse facts). One behavior family: the MODEL-04 evidence record. |
| `write_scope` | `docs/factory/production-ml-library/model04-full-model-reference-inference-receipt.md` (new — the aggregate MODEL-04 receipt); `docs/factory/production-ml-library/model04-full-model-reference-inference-delivery.md` (this file — status line + per-unit receipt references) |
| `read_scope` | M1–M6 evidence (receipts, comparison record, exempla README); the campaign receipt clauses; the ORACLE policy + `oracle-receipt-schema-1.0.0` (read-only) |
| `forbidden_paths` | Product code in any repo; CAMPAIGN.md status lines (CLOSE-01 owns the campaign-wide reconciliation); any Metal/CUDA execution claim (EXEC-02/M5/CAP-01/02 own native receipts) |
| `depends_on` | MODEL-04-M6 |
| `done_when` | The receipt satisfies every MODEL-04 oracle clause: two prompts, every layer traversed, matching reference logits/tokens/text, no reduced-model substitution, all receipt clauses present with exact values; delivery status line updated; `git diff --check` clean. |
| `integrable` | Yes — the receipt is evidence; EXEC-01-U2 and EXEC-02 read it as their MODEL-04 gate; CLOSE-01 reconciles it. |
| `first_failing_oracle` | None (closeout unit — no new failing oracle); the red state is any missing receipt clause. |
| `closeout_command` | `cd /Users/ianzepp/work/faberlang/worktrees/<hand>/gradus`; cross-check every receipt clause against the campaign receipt list and the ORACLE comparison record; `git diff --check -- docs/factory/production-ml-library/model04-full-model-reference-inference-receipt.md docs/factory/production-ml-library/model04-full-model-reference-inference-delivery.md` |
| `expected_observed_result` | The receipt records both prompts' full-layer traversal with matching reference logits/tokens/text and first-divergence `none` (or the routed first divergence), every receipt clause populated, no reduced-model claim; the delivery status line names the MODEL-04-G gate result; `git diff --check` silent. |
| `est_work_tokens` | 3k–5k |
| `est_basis` | Closeout-row precedent at micro-unit scale: EXEC-01-U3 aggregate-closeout rows (3k–5k) and the pml5-closeout receipt shape; one evidence record + status update. |
| `tool_latency` | Low — no model run; receipt assembly + cross-check only. |
| `local_corpus_boundary` | Derived facts only (identity, hashes, token ids, text, timing) — never model bytes. |
| `hardware/backend authority` | burgus CPU/reference facts recorded as observed; no Metal/CUDA claim. |
| `stop_condition` | Stop and route a need if any receipt clause is missing or contradicts the campaign invariant, the GGUF-M4 done oracle, or the ORACLE policy. |

### MODEL-04-G — Aggregate Gate (one gate; no child lane gates)

| Field | Value |
| --- | --- |
| `id` | MODEL-04-G |
| `outcome` | **MODEL-04 is complete only when the aggregate gate passes**: M1–M7 receipts are committed, the executed reference run has both prompts traverse every layer and match the declared reference logits/tokens/text, no resource-limited mode substituted a reduced model, and the successors EXEC-01/EXEC-02 still gate on the MODEL-04 receipt unchanged. |
| `requires` | MODEL-04-M1..M7 receipts; delivery audit acceptance; the ORACLE-CAP/ORACLE-TOOL checkpoints the comparison consumed |
| `done_when` | The MODEL-04 receipt (`model04-full-model-reference-inference-receipt.md`) names each executed proof with command + observed result + revision; the comparison record shows first-divergence `none` for both prompts under the pinned contract; audit finds no incomplete GGUF-M4 oracle clause; `git diff --check` clean. |
| `stop_condition` | The gate fails (MODEL-04 stays open) if any receipt is missing, either prompt fails to traverse every layer, any logit/token/text comparison diverges without the recorded first-divergence route, a reduced-model substitution appears, or any unit overclaims (Metal/CUDA execution, EXEC-*/CAP-* scope). |

## Lane-Owned Validation (named once, not copied onto units)

- **Hand sanity (per unit)**: `./scripta/check-source` + `./scripta/check-compile` (with the packet's `FABER_BIN`) + the unit's focused proba/exempla run + `git diff --check` — never a lane gate.
- **Lint lane (stages 1–2)**: gate + lint on the integrated tree after merge; mechanical fixes in-lane.
- **Test lane (stages 3–6)**: proba suites, exempla matrices, `--e2e` where applicable, after lint clears.
- **Merge lane**: `factory/merge` integration, one lane at a time, `scripta/verify-main-consistent` before main; the pml5-general delivery's integration stop applies (no fast-forward of any main branch from this delivery).
- **No child lane gates**: units close at their own done oracle; MODEL-04-G is the single aggregate gate.

## Campaign Rule Compliance

- **Rule 1** (Mind → Planner → Hand): this delivery is the Planner output; this Planner files no Hand tasks.
- **Rule 2** (task-body fields): every unit above names the 8 required fields — executed `outcome`, exact `write_scope`, `first_failing_oracle`, `closeout_command`, `expected_observed_result`, `est_basis` (+ `est_work_tokens`), `stop_condition`, and `depends_on` — plus `done_when`, `integrable`, and the supporting rows.
- **Rule 3** (delivery audit before dispatch): committed for audit before any Hand dispatch.
- **Rule 4** (one executed proof per unit): each unit's proba/exempla run is an executed proof at its declared boundary; documentation supports, never replaces it.
- **Rule 5** (divergence receipts): each unit's first-divergence record names the first failing tokenizer id / tensor / layer / state update / logit / token and routes the repair to the owning surface.
- **Rule 6** (block only the affected edge): the predecessor edge {REF-01, MODEL-02, MODEL-03} gates M1 and thereby the serial chain; ORACLE-CAP/TOOL gate M2/M6 read-only. Unaffected campaign units do not wait on MODEL-04.
- **Scope closure**: nothing in GGUF-M4's done oracle is narrowed, deferred, made optional, or moved outside the campaign. Unit completion is not campaign completion — CLOSE-01 owns that. Successors EXEC-01/EXEC-02 (and EXEC-03, CAP-01/02) are preserved unchanged with their MODEL-04 gate.

## First Eligible Frontier

**MODEL-04-M1** is the first eligible frontier, and it is dispatchable only
after the **REF-01 + MODEL-02 + MODEL-03 receipts** are accepted (campaign
edge) — the composed graph consumes those delivered behavior families. M2
additionally needs the ORACLE-CAP target-row tokenizer checkpoints (read-only)
and M6 needs ORACLE-CAP checkpoints + ORACLE-TOOL tooling (read-only). The
serial chain M1 → … → M7 then closes MODEL-04-G. Dispatch in that order; do not
start a later unit while an earlier unit is open.

## Open Questions For Mind

1. The reference-run execution cost (22.6 GB artifact, CPU, 2 prompts × ≥256
   tokens) is bounded but slow; if the fleet CPU envelope is a constraint, the
   reference run may use the burgus Metal path — the units above stay
   device-neutral until that decision lands (the done oracle and comparison
   contract are unchanged either way).
2. `exempla/qwen36-35b-inference` is created by GGUF-A2/LIB-02's tokenizer
   phase per the delivery authority; if its skeleton is absent when M2 lands
   (predecessor slip), M2 creates the reference-mode package skeleton and notes
   it — GGUF-M6 still owns the final capstone surface.
3. M6's exact `compare.py` CLI binds at dispatch once ORACLE-TOOL lands; the
   comparison contract and record shape above are frozen regardless.
