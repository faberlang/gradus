# Delivery: GGUF-M6 — Qwen3.6 35B Faber Capstone Application (`exempla/qwen36-35b-inference`)

**Status**: lowered 2026-08-13; **revised 2026-08-14** — audit `d4f23d09`
(verdict revise, report `e560a245`) found no defect in the M6-U1 scaffold
but three P2 evidence-honesty defects in this delivery artifact, corrected
here (F1: FMIR lane is gated by SEM006/GGUF-A1c, not open; F3: cap02 CUDA
authority — RunPod ≥48 GB pod, pharos demoted to smoke; F4: re-established
on the active `factory/planner-36` lineage at `995da7e`, superseding the
orphaned `1902d73`). Goal READY; M6-U1 (capstone scaffold) is the first
implementation frontier and is dispatchable now (acceptance gated on
committed-tree green — see M6-U1 done_when (f)); M6-U2..U6 are waved with
explicit entry gates on named predecessor receipts
**Campaign**: [`radix/docs/factory/gpu-production-readiness/CAMPAIGN.md`](../../../../radix/docs/factory/gpu-production-readiness/CAMPAIGN.md)
(registered `gol_634a0417d02c510f`) — milestone Q4 gate: **M6 and closeout
audit accepted**
**Semantic delivery authority**:
[`pml5-general-gguf-delivery.md`](pml5-general-gguf-delivery.md) (registered
`gol_67b635603712f01b`) — unit **GGUF-M6 — Faber Qwen3.6 Capstone And
Closeout**
**Repo**: gradus (owning repo for the capstone package and its docs)
**Branch**: `factory/planner-36`
**Planner**: planner-36 (original lowering task `3ff825b5`; **revision task
`c5d7969a`** — applied audit `d4f23d09`/report `e560a245` findings F1, F3,
F4; derived independently from the campaign, the delivery authority, the
cap02 authority, and live product repos, per the freshness rule)
**Planning-only**: no product, test, runtime, or CLI code is written by this
lowering; this document is the delivery spec implementing Hands run from and
Mind files units from.

## 1. Interpreted Unit

**M6** = the public Faber Qwen3.6 capstone application `exempla/qwen36-35b-inference`
created **from scratch** as the public-library consumer. The application owns
the path and I/O; Gradus owns model semantics; Radix owns lowering and
generated device programs; Hosts owns physical allocation, residency, launch,
synchronization, and teardown. HTTP transport is not part of this campaign and
cannot substitute for the capstone.

The Delivery Invariant (frozen by the campaign and the delivery authority)
requires one **normal Faber package command** through public `gradus:*`
imports and the accepted Faber/Radix/Hosts execution path that:

1. verifies and admits the exact artifact `Qwen3.6-35B-A3B-UD-Q4_K_M.gguf` —
   byte length `22,663,387,424`, SHA-256
   `0b21525e972670ed59e1812e170b27c26355381f0656ecc4e25617ece7dac58b`,
   architecture `qwen35moe`, 753 tensors;
2. accepts operator-supplied Unicode text and uses the artifact tokenizer and
   special-token policy;
3. executes the complete `qwen35moe` graph, including expert routing and the
   hybrid SSM/attention state;
4. performs full-model prefill and autoregressive decode;
5. generates at least 256 new tokens and detokenizes them to text;
6. repeats with a second prompt through the same admitted model session while
   weights and model state remain resident;
7. performs no per-token model reload, recompilation, packet rebuild, or full
   host round-trip;
8. matches the pinned `llama.cpp` token/logit comparison policy (first
   divergence is recorded, never hidden);
9. executes on both admitted single-device backends, Metal and CUDA;
10. records exact source revisions, model identity, command, hardware,
    backend, observed output, peak memory, timing, reset, and teardown facts.

## 2. Normalized Spec

One delivery-sized outcome: the capstone package exists as the single
application surface that satisfies every clause of the Delivery Invariant, and
the campaign successor chain through `CLOSE-01` is preserved.

Locked decisions (defaults recorded; not left to Hands):

1. **The capstone is the terminal application unit.** Gradus library units
   (GGUF-A2/A3, GGUF-M1/M4/M5) own the semantics; the capstone consumes those
   public surfaces. A capstone unit never re-implements library semantics and
   never claims a proof its predecessor receipt does not provide.
2. **Application-owned I/O boundary.** The package resolves the model path via
   `norma:processus` arguments and `norma:solum` file operations, reads the
   bounded table prefix / validated tensor byte ranges it needs, and passes
   Gradus only pathless descriptors and operation-scoped range functions
   (the GGUF-A1b `LectioFontis` seam precedent). Gradus never receives or
   retains a path, file handle, mapping, or whole-model byte list.
3. **Content identity is operator-supplied and application-checked.** The
   pinned digest is passed as a CLI argument (the `gguf-inspect` precedent —
   the FMIR surface has no sha-256 primitive). The application validates
   digest form and artifact byte length via `gradus:model/artifact` and
   `norma:solum.mensura`; the receipt's digest fact is re-derived with
   `shasum -a 256` in the documented command.
4. **Phase ratchet.** Each capstone phase lands only on its named predecessor
   receipt (below). A phase with an unmet gate is deferred with a recheck
   handle — it never proceeds on assumed surfaces ("summaries are claims").
5. **Reference tier before device tier.** Full-model reference execution
   (CPU, all layers, the pinned `llama.cpp` comparison policy) precedes any
   Metal/CUDA claim. A resource-limited reference mode must still execute
   every layer and must not substitute a reduced model.
6. **Native execution binds to the admitted backend substrate.** Metal on
   burgus (Apple M5 Max / Metal 4) and CUDA on the cap02 authority's named
   machine — an operator-authorized RunPod single-device pod of the **≥48 GB
   VRAM class** (cap02-cuda-capstone-delivery.md; operator gate `d80ab288`).
   pharos (NVIDIA RTX 5070, 12 GiB VRAM) **cannot** hold the 22.663 GB
   packed artifact resident and is demoted to optional smoke/capability
   evidence only — no pharos receipt satisfies CAP-02. The capstone runs at
   the pinned faber `1.6.0-rc.1` revisions, RC level; no stable/E8
   publication claim is made by this delivery.
7. **llama.cpp is a comparator, never a dependency.** No calling, embedding,
   or proxying of llama.cpp satisfies a Faber-owned execution gate.
8. **The corpus is operator-local and never committed.** The four mandatory
   rows (SmolLM2-360M, Qwen2.5-0.5B, Qwen2.5-1.5B, Qwen3.6-35B) plus the two
   inventoried hybrid rows are local evidence under `/Users/ianzepp/Ai/models/`;
   receipts name files by content identity, never by filename provenance alone.
9. **Receipts follow the campaign receipt contract** (exact command and cwd;
   revisions; model identity; tokenizer/chat-template identity and prompt
   hash; hardware/OS/driver/backend; tensor storage + kernel/package +
   model-state capacity; observed token ids and decoded text; comparison
   policy and first divergence; load/prefill/decode/total timing, throughput,
   peak memory; reload/compile/packet-build/host-round-trip counters; reset,
   reuse, cancellation, teardown, live-handle facts).
10. **Honest failure over green.** A divergence, a `NOT ATTEMPTED` device row,
    or a gated phase is published with its owner and recheck handle — never a
    weakened gate.

## 3. Repo-Aware Baseline

Verified 2026-08-13 against the planner-36 worktree at the hand-packet
baselines: Radix `b6d6e17c8ad7`, Gradus `bc500993c97b`, Hosts `57d659d60430`,
public Faber `1fb6cc97e66d`.

### Predecessor state (executed receipts)

| Predecessor | State | Receipt |
| --- | --- | --- |
| GGUF-A1a (bounded-corpus manifest parser) | **done** | `exempla/gguf-manifest` — `faber run --target fmir` exit 0, 40 PASS / 0 FAIL (2026-08-12); synthetic bounded corpora only |
| GGUF-A1b (range source + real-file inspection) | **done** | `exempla/gguf-inspect` — exit 0 on all six local rows, `qwen35moe/753` for the target; data offsets match the independent reader; no tensor-data read (2026-08-13) |
| GGUF-A1c (capsule/caller clean break) | **NEXT** — not done | — |
| GGUF-A2 tokenizer runtime | not done | — |
| GGUF-A3 packed storage / materialization | not done | — |
| GGUF-A4..A6 dense rows | not done | — |
| GGUF-A7 native quantized execution contract | not done | — |
| GGUF-M1 `qwen35moe` admission | not done | — |
| GGUF-M2 MoE router/expert | not done | — |
| GGUF-M3 hybrid SSM/attention | not done | — |
| GGUF-M4 full-model reference | not done | — |
| GGUF-M5 persistent Metal/CUDA | not done | — |

### Live surface the capstone binds to

- `gradus:model/artifact` — `IdentitasContenuti`, `identitas`, `ArtifactError`
  (pathless content identity; form validation only).
- `gradus:model/gguf_manifest` — `CorpusGguf`, `ManifestumGguf`,
  `MetadatumGguf`, `DescriptioTensorisGguf`, `LayoutGgml`, `parse`, `inspice`,
  `lege_fragmentum`, `textum`, `numerum`, `metadatum`, `inveni_tensorem`,
  `LectioFontis` (format-general GGUF v3; 4,096-entry and 64 MiB bounds admit
  the 753-tensor target).
- `norma:processus` / `norma:solum` — CLI arguments, file size, partial reads
  (application-owned I/O).
- Radix `faber` binary targets: `fmir` (run=yes, package=yes — the
  library-importing package run lane; proven pre-SEM006 by the A1a/A1b
  receipts, **gated** on the committed tree until the GGUF-A1c visibility
  migration lands); `metal-text` / `llvm-text` (device execution at RC level
  via `faber run --backend metal|cuda`, faber `1.6.0-rc.1`, E6/E7 receipts;
  kernel-shaped device-safe programs only).
- Gradus docs updated by the closeout: `docs/api-reference.md` (zombie-doc
  gate via `scripta/inventory-public-symbols`), `docs/module-map.md`,
  `docs/regression-corpus.md`, `docs/factory/production-ml-library/pml0-support-matrix.md`,
  and the campaign status line.

### Tooling notes (grounded 2026-08-13)

- The FMIR library-import lane is **gated, not open**: current faber from
  radix main enforces the import-seam policy (SEM006, radix `016c225c4`,
  landed 2026-08-13 05:36 — ~7h before this lowering was first authored),
  which blocks `faber check` AND `faber run` on gradus-importing exempla
  until the library's `privata`→`@ publica` visibility migration lands on
  the committed tree. That migration is owned by GGUF-A1c (capsule/caller
  clean break), which the predecessor table above lists as **NEXT — not
  done**. The pre-SEM006 A1a/A1b receipts (exit 0) do not evidence an open
  lane on the committed tree; `faber test` additionally remains blocked by
  the imported-library provider seam (artifact `sym#20`, manifest `sym#140`).
  The capstone proves itself via `faber run`, never `faber test`, and
  **M6-G1 goes green only after the GGUF-A1c migration has landed on the
  committed tree** (see M6-U1 done_when (f)).
- **Binary/pack revision pairing**: the currently built `radix/target/debug/faber`
  (built 2026-08-12 23:06) fails to validate the committed `la` reader pack
  (`stdlib/locale/la/pack.toml`, last touched 2026-08-13 10:13) with
  `reader pack validation failed`; the A1b receipt binary (hand-2) predates
  that pack and loads it. The implementing Hand must rebuild `faber` from the
  current radix tree (so the committed pack validates) or use a binary whose
  radix revision matches the pack. This is a tool-latency note, not a
  planning blocker; if it persists after a rebuild it routes to the
  radix/locale lane with the pack-validation detail.
- The capstone package's `faber.toml` follows the `gguf-inspect`/`gguf-manifest`
  shape (`[paths] source/entry`, `[build] target = "fmir", kind = "bin"`,
  `[reader] locale = "la"`).

### Target manifest oracle (from the independent reader / A1b receipt)

`Qwen3.6-35B-A3B-UD-Q4_K_M.gguf` — 22,663,387,424 bytes,
`0b21525e972670ed59e1812e170b27c26355381f0656ecc4e25617ece7dac58b`;
GGUF v3, alignment 32, data offset 10,991,392, 55 metadata entries, 753
tensors, architecture `qwen35moe`.

## 4. Ordered Unit Graph

```text
M6-U1 (capstone scaffold + path/I-O + identity/manifest admission + CLI/receipt contract)   [dispatchable NOW]
  -> M6-U2 (tokenizer phase)                [entry gate: GGUF-A2 receipt]
  -> M6-U3 (materialization phase)          [entry gate: GGUF-A3 receipt]
  -> M6-U4 (qwen35moe admission + full-model reference run)   [entry gates: GGUF-M1 + GGUF-M4 receipts]
       -> M6-U5 (persistent native execution + Metal/CUDA capstone receipts)   [entry gate: GGUF-M5 receipt]
            -> M6-U6 (closeout docs + successor pass-through)  [entry gate: M6-U5]
                 -> CAP-01 (Metal capstone evidence) + CAP-02 (CUDA capstone evidence)  [campaign successors]
                      -> CLOSE-01 (campaign closeout audit)  [campaign successor — not lowered here]
```

Dependency edges are ordering edges plus the named predecessor **receipts**
(the campaign's executed-proof ratchet). M6-U2..U6 carry **entry gates**; a
gate not met at the unit boundary defers the unit with a recheck handle.

**Split boundary (named)**: the capstone is split by the consumer surface it
wires — package scaffold/I-O (U1), tokenizer (U2), storage/materialization
(U3), admission + reference execution (U4), native execution (U5), closeout
(U6). The library semantics for each phase remain in the owning GGUF unit
(A2/A3/M1/M4/M5); the capstone phase is the application wiring of that
surface plus its executed proof at the application boundary.

### M6-U1 — Capstone scaffold, path/I-O, identity + manifest admission, CLI/receipt contract

- **title**: Create `exempla/qwen36-35b-inference` from scratch as the
  public-library consumer skeleton: application-owned path/I-O, exact
  artifact identity verification, GGUF manifest admission of the target,
  frozen CLI argument contract, and receipt plumbing.
- **outcome**: one package a later phase grows; it verifies the exact target
  identity, admits its GGUF manifest through the public A1a/A1b surface, and
  prints the receipt facts — proving the application shell and its command
  lane before any model semantics exist.
- **done_when**:
  (a) `exempla/qwen36-35b-inference/{faber.toml,src/main.fab,README.md}`
  committed, registered in `scripta/check-compile`;
  (b) the CLI contract is frozen in the README: `qwen36-35b-inference
  <model-path> --sha256 <digest> [--oracle-offset <n>] [--prompt <text> …]
  [--max-new-tokens <n>] [--seed <n>] [--receipt <path>]`;
  (c) the application resolves the path via `processus.argumenta`, reads the
  file size via `solum.mensura`, validates digest form + byte length via
  `artifact.identitas`, and admits the manifest via
  `manifestum.inspice`/`textum`/`numerum` with an application-owned range
  function over the bounded table prefix (the `gguf-inspect` guard: no read
  may enter the tensor data region);
  (d) the run prints PASS lines for the target oracle facts — version 3,
  alignment 32, data offset 10,991,392, metadata 55, tensors 753,
  architecture `qwen35moe`, byte length 22,663,387,424 — and fails closed
  (nonzero exit + typed `causa`) on identity mismatch, short prefix, or any
  tensor-data read;
  (e) `faber check` and `faber run --target fmir` exit 0 with the observed
  receipt written to the README and the `--receipt` path; `git diff --check`
  clean;
  (f) **M6-G1 acceptance is gated on committed-tree green (the closeout
  repair chain)**: `check-compile` green requires the SEM006
  `privata`→`@ publica` visibility migration (GGUF-A1c) to have landed on
  the committed gradus tree. Until then this unit is a real producer gated
  behind an unresolved library dependency — a receipt produced against a
  throwaway annotated library copy (the hand-25 provisional receipt) is
  provisional evidence only and never the M6-G1 done oracle; the gate is
  re-checked on the committed tree after the A1c migration lands.
- **first failing oracle**: the target manifest facts above (independent GGUF
  reader + A1b receipt) and the pinned content identity. A divergence names
  the first mismatched fact (identity, data offset, metadata count, tensor
  count, architecture) and routes to the owning surface.
- **write_scope**: `exempla/qwen36-35b-inference/` (new package),
  `scripta/check-compile` (register the package), the capstone README.
- **read_scope**: `gradus:model/artifact`, `gradus:model/gguf_manifest`,
  `norma:processus`, `norma:solum`, `exempla/gguf-inspect`, the campaign and
  delivery authority.
- **forbidden_scope**: `src/**` (library semantics), `src/model/capsule.fab`
  and `src/model/gguf.fab` (A1c owns their migration), any device/host code,
  any claim of tokenizer/graph/inference behavior.
- **closeout command**:
  ```bash
  cd /Users/ianzepp/work/faberlang/worktrees/<hand>/gradus
  env FABER_BIN=/Users/ianzepp/work/faberlang/worktrees/<hand>/radix/target/debug/faber \
    ./scripta/check-compile
  env FABER_BIN=<same> \
    <faber> run --target fmir exempla/qwen36-35b-inference -- \
      /Users/ianzepp/Ai/models/Qwen3.6-35B-A3B-UD-Q4_K_M.gguf \
      --sha256 0b21525e972670ed59e1812e170b27c26355381f0656ecc4e25617ece7dac58b \
      --oracle-offset 10991392 --receipt /tmp/m6-u1-receipt.txt
  git diff --check -- exempla/qwen36-35b-inference scripta/check-compile
  ```
  (the faber binary must be rebuilt from the current radix tree so the `la`
  reader pack validates — tooling note above).
- **expected observed result**: `check-compile` ok **on the committed tree**
  (after the SEM006/A1c migration has landed — done_when (f)); the run exits
  0 and prints `PASS` for each oracle fact; `shasum -a 256` of the artifact
  equals the pinned digest; zero reads intersect the tensor data region; the
  receipt file carries the facts.
- **local corpus boundary**: the six operator-local rows are read-only
  evidence; the target file is never committed or copied into the package;
  the package embeds no prompt, digest fallback, or token id.
- **hardware/backend authority**: none required — CPU/FMIR stepper only.
- **est_work_tokens**: 6k–10k. **est_basis**: pilot (extrapolated from the
  `gguf-inspect` package/CLI/receipt shape; no close ledger class).
- **tool_latency**: low–medium (`faber` rebuild once + `faber check` +
  one FMIR run; no cargo).
- **risk**: low — the A1b lane is proven; residual risk is the binary/pack
  revision pairing (routed to radix/locale if it persists after rebuild).
- **depends_on**: GGUF-A1a + GGUF-A1b receipts (both landed); none within M6.
- **non_goals**: no tokenizer/graph/inference/device code; no capsule edits;
  no HTTP; no main-checkout writes.

### M6-U2 — Capstone tokenizer phase

- **title**: Wire the capstone to the artifact-backed tokenizer runtime
  (GGUF-A2): operator-supplied Unicode prompts encode/decode through the
  public tokenizer surface with the artifact's special-token policy; no
  hard-coded prompt or token-id fallback exists in the capstone path.
- **outcome**: the capstone command encodes both prompts to the pinned
  `llama.cpp` token ids and decodes generated ids back to text, proving the
  tokenizer clause of the Delivery Invariant at the application boundary.
- **done_when**: (a) the capstone consumes tokenizer metadata from the
  admitted artifact (no hard-coded ids); (b) both operator prompts produce
  token ids and decoded text that match the pinned `llama.cpp` oracle at the
  first-divergence boundary; (c) EOG/special-token behavior follows the
  admitted policy; (d) `faber run --target fmir` exits 0 with the observed
  ids/text in the receipt; `git diff --check` clean.
- **first failing oracle**: the first divergent tokenizer id or decoded
  character vs the pinned `llama.cpp` probe for the two prompts (the
  `ProbeDivergens` boundary).
- **write_scope**: the tokenizer phase of `exempla/qwen36-35b-inference/src/main.fab`
  + README receipt; nothing else.
- **read_scope**: GGUF-A2 delivered surface, the artifact tokenizer metadata,
  the pinned probe fixtures, the campaign comparison policy.
- **forbidden_scope**: `src/tokenizer.fab` / `src/**` (A2 owns the runtime);
  any fallback tokenizer; HTTP.
- **closeout command**: the M6-U1 command plus `--prompt "<unicode A>"
  --prompt "<unicode B>"`; receipt records ids + decoded text; comparison to
  the pinned oracle at first divergence.
- **expected observed result**: both prompts encode to the pinned ids and
  decode exactly; first divergence (if any) is recorded with the failing id.
- **local corpus boundary**: the target artifact's tokenizer metadata is the
  source; prompts are operator-supplied, never embedded.
- **hardware/backend authority**: CPU/FMIR only.
- **est_work_tokens**: 4k–8k. **est_basis**: pilot (application wiring of a
  landed library surface; no close ledger class). **tool_latency**: low.
- **risk**: low; a tokenizer divergence routes to A2 (Gradus owns the
  runtime), recorded with the first failing id.
- **depends_on**: M6-U1; **entry gate**: GGUF-A2 receipt.
- **non_goals**: no tokenizer implementation; no chat-template language;
  no graph/inference work.

### M6-U3 — Capstone materialization phase

- **title**: Bind the capstone to GGUF-A3 packed storage: every tensor the
  `qwen35moe` forward graph requires has a checked `TensorDescriptor` +
  validated `TensorPayload` (range, shape, storage layout, bounded
  materialization path); no whole-model F32 expansion.
- **outcome**: the capstone command materializes the required tensors from
  the artifact through the application's range source and the public storage
  surface, proving the storage clause at the application boundary.
- **done_when**: (a) every required tensor binds through the A3 surface with
  checked ranges/shapes/layouts; (b) selected tensor slices match the
  independent oracle; (c) mixed per-tensor storage and rank-3 expert tensors
  are explicit; (d) the run exits 0 with the storage facts in the receipt;
  `git diff --check` clean.
- **first failing oracle**: first divergent tensor range/shape/storage layout
  vs the manifest + oracle (a named tensor is the divergence unit).
- **write_scope**: the materialization phase of the capstone `src/main.fab`
  + README receipt.
- **read_scope**: GGUF-A3 delivered surface, `gradus:model/gguf_manifest`
  descriptors, the oracle evidence.
- **forbidden_scope**: `src/model/gguf_manifest.fab`, `src/model/dequant.fab`
  and `src/**` codecs (A3 owns them); any whole-model F32 materialization
  path; device upload.
- **closeout command**: the M6-U1 command plus a `--tensors`-inspect mode
  printing per-tensor range/shape/layout and the selected-slice comparison.
- **expected observed result**: every required tensor admits with exact
  ranges; slice checks PASS; zero whole-model F32 expansion.
- **local corpus boundary**: tensor payloads are read from the local artifact
  by validated byte ranges only; never copied wholesale into the package.
- **hardware/backend authority**: CPU/FMIR only.
- **est_work_tokens**: 4k–8k. **est_basis**: pilot (application wiring of a
  landed library surface). **tool_latency**: low–medium.
- **risk**: low; a storage divergence routes to A3 with the named tensor.
- **depends_on**: M6-U2 (package shape); **entry gate**: GGUF-A3 receipt.
- **non_goals**: no codec implementation; no device work; no inference.

### M6-U4 — Capstone `qwen35moe` admission + full-model reference run

- **title**: Admit the complete `qwen35moe` configuration/tensor map (753
  tensors, typed execution config) and execute full-model reference inference
  for both prompts through the public Gradus generation surface (GGUF-M1/M4).
- **outcome**: the capstone command admits the exact target and produces
  matching reference logits/tokens/decoded text for both prompts — ≥256 new
  tokens each — under the pinned `llama.cpp` comparison policy on the CPU
  reference tier.
- **done_when**: (a) the exact target admits with 753 tensors and a complete
  typed execution configuration; mutated metadata/names/shapes/layouts fail
  closed with typed first-divergence diagnostics; (b) both prompts traverse
  every layer and match the declared reference logits/tokens/text at the
  first-divergence boundary; (c) ≥256 new tokens are generated and
  detokenized per prompt; (d) any resource-limited reference mode still
  executes every layer and substitutes no reduced model; (e) the run exits 0
  with the reference receipt; `git diff --check` clean.
- **first failing oracle**: first divergent layer, state update, logit, or
  token vs the pinned reference (recorded by the campaign divergence rule).
- **write_scope**: the admission + reference-run phases of the capstone
  `src/main.fab` + README receipt.
- **read_scope**: GGUF-M1 and GGUF-M4 delivered surfaces
  (`qwen35moe.fab`, generation surface), the reference oracle, the campaign
  comparison policy.
- **forbidden_scope**: `src/model/qwen35moe.fab` / `src/**` (M1/M4 own the
  semantics); any claim of device execution; any reduced-model substitute.
- **closeout command**: the M6-U1 command with both `--prompt` args and
  `--max-new-tokens 256`; receipt records ids, decoded text, first
  divergence (or null), per-clause PASS.
- **expected observed result**: admission PASS (753 tensors); both prompts
  match the reference oracle and produce ≥256 detokenized tokens.
- **local corpus boundary**: the target artifact only; prompts
  operator-supplied; reference pins from the independent oracle.
- **hardware/backend authority**: CPU reference tier on burgus (no device).
- **est_work_tokens**: 6k–10k. **est_basis**: pilot (application wiring of
  landed M1/M4 surfaces plus an executed reference run). **tool_latency**:
  medium (full-model reference run is long; bounded mode still executes every
  layer).
- **risk**: medium — the full-model reference run is the first executed
  full-graph claim; a divergence routes to M2/M3 (router/state) with the
  named boundary.
- **depends_on**: M6-U3; **entry gates**: GGUF-M1 + GGUF-M4 receipts.
- **non_goals**: no MoE/SSM implementation; no device execution; no sampling
  policy beyond the admitted generation surface.

### M6-U5 — Capstone persistent native execution (Metal + CUDA receipts)

- **title**: Bind the capstone through the GGUF-M5 prepared host sessions:
  resident weights + KV/SSM state across both prompts, ≥256 new tokens each,
  on Metal and CUDA, with no per-token reload/recompile/rebuild/host
  round-trip, and full receipt facts.
- **outcome**: one documented Faber package command executes the complete
  graph on each admitted backend with resident state and both-prompt reuse —
  the executed evidence for campaign rows CAP-01 (Metal) and CAP-02 (CUDA).
- **done_when**: (a) the capstone runs on Metal (burgus, Apple M5 Max /
  Metal 4) and CUDA on the cap02 named machine — an operator-authorized
  RunPod single-device pod of the **≥48 GB VRAM class** — via the ordinary
  `faber run --backend metal|cuda` command at the pinned faber `1.6.0-rc.1`
  revisions; pharos (RTX 5070, 12 GiB) cannot hold the 22.663 GB packed
  model resident and is demoted to smoke — no pharos CUDA row is CAP-02
  evidence; (b) both prompts reuse one admitted model session with weights
  and KV/SSM state resident; ≥256 new tokens each, detokenized; (c) counters
  prove zero per-token reload/compile/packet-build/host round-trip; (d) each
  receipt carries the campaign clause set (revisions, model identity, command,
  hardware, backend, observed ids/text, comparison policy + first divergence,
  load/prefill/decode/total timing, throughput, peak memory, reset/reuse/
  teardown/live-handle facts); (e) `git diff --check` clean.
- **first failing oracle**: first divergent kernel/state/lifecycle boundary
  on either backend (a named tensor, state update, token, or lifecycle event).
- **write_scope**: the native-execution phase of the capstone (package
  wiring of the M5 session/kernel surfaces) + README receipts for Metal and
  CUDA.
- **read_scope**: GGUF-M5 delivered surfaces (prepared sessions, packed
  kernels, residency), the faber E6/E7 backend pins, the campaign receipt
  contract.
- **forbidden_scope**: kernel implementation (EXEC-02/Radix); Hosts session
  internals (EXEC-03/Hosts); any F32 whole-model expansion; any backend
  beyond the two admitted.
- **closeout command**: the M6-U1 command with both prompts and
  `--backend metal` on burgus and `--backend cuda` on the operator-authorized
  RunPod ≥48 GB pod (operator gate `d80ab288`); receipts named per machine;
  reproducibility from a clean packet is proven at M6-U6.
- **expected observed result**: both backends generate ≥256 tokens per prompt
  in one resident session with the recorded memory/timing/lifecycle facts;
  first divergence (if any) recorded, never hidden.
- **local corpus boundary**: weights/states stay in the admitted session on
  the named machine; the local artifact is never committed to any
  repository — the operator-authorized transfer to the RunPod pod is
  SHA-256-verified on the pod before admission (cap02 authority).
- **hardware/backend authority**: burgus (Apple M5 Max, Metal 4) for CAP-01;
  CAP-02's named machine is the operator-authorized RunPod single-device pod
  of the **≥48 GB VRAM class** (cap02 authority, operator gate `d80ab288`) —
  pharos (RTX 5070, 12 GiB VRAM, CUDA 13.2, driver ≥ 595.71.05) cannot hold
  the 22.663 GB packed artifact resident and is demoted to optional
  smoke/capability evidence only; faber `1.6.0-rc.1` pinned revisions;
  RC-local posture (no stable/E8 claim).
- **est_work_tokens**: 8k–14k. **est_basis**: pilot (application wiring of
  landed M5 surfaces + two-machine executed receipts). **tool_latency**:
  high (two machine device runs + measurement; pod provisioning is
  operator-authorized).
- **risk**: medium — device availability and measurement discipline (pod
  provisioning and cost are operator-authorized, gate `d80ab288`); a
  `NOT ATTEMPTED` device row is recorded, never fabricated.
- **depends_on**: M6-U4; **entry gate**: GGUF-M5 receipt.
- **non_goals**: no HTTP/serving; no multi-device; no AMD/WebGPU; no stable
  publication.

### M6-U6 — Capstone closeout docs + successor pass-through

- **title**: Make the capstone reproducible from a clean packet and reconcile
  the support matrix, API docs, module map, regression inventory, and
  campaign status to the observed Metal + CUDA results; hand the successor
  chain to `CAP-01`/`CAP-02`/`CLOSE-01` intact.
- **outcome**: the support/docs surface describes exactly what was observed —
  no broader claim — and every mandatory campaign successor remains named and
  reachable.
- **done_when**: (a) the capstone README documents one command per backend
  reproducible from a clean packet (temporary home, minimal PATH, no sibling
  checkout/private state); (b) `docs/api-reference.md` (re-baselined via
  `scripta/inventory-public-symbols`), `docs/module-map.md`,
  `docs/regression-corpus.md`, `pml0-support-matrix.md`, and the campaign
  status line describe the observed result exactly (every positive claim maps
  to a receipt); (c) the successor statement names CAP-01 (Metal), CAP-02
  (CUDA), and CLOSE-01 (campaign closeout audit) as mandatory successors and
  states that M6 delivery does not close the campaign; (d) `git diff --check`
  clean.
- **first failing oracle**: none (docs unit) — a claim that outgrows its
  receipt is cut, not extended.
- **write_scope**: the capstone README; the five docs listed above (their
  Qwen/M6 rows only); a successor statement in the delivery's evidence note.
- **read_scope**: M6-U1..U5 receipts; the campaign receipt contract; the
  support-matrix row policy (structural/output-checked/measured tiers).
- **forbidden_scope**: campaign-semantics edits (status line only); claim
  wording beyond the observed receipts; Vivi registration changes.
- **closeout command**: the clean-packet reproduction (fresh temp home,
  downloaded/committed package + binary, one command) on both named
  machines — burgus (Metal) and the operator-authorized RunPod ≥48 GB pod
  (CUDA); `scripta/inventory-public-symbols`; `grep` checks for the
  reconciled rows.
- **expected observed result**: both clean-packet reproductions pass; the
  inventory script is green; every positive docs row links its receipt.
- **local corpus boundary**: as M6-U5; the clean packet never embeds model
  bytes.
- **hardware/backend authority**: as M6-U5.
- **est_work_tokens**: 4k–8k. **est_basis**: pilot (docs/closeout unit; no
  close ledger class). **tool_latency**: low–medium.
- **risk**: low; docs drift is the maintenance rule (cold-read check).
- **depends_on**: M6-U5.
- **non_goals**: no closeout audit (CLOSE-01 is campaign-owned); no main
  merge; no release action.

## 5. Checkpoints And Gates

| Gate | Content | Owner |
| --- | --- | --- |
| **M6-G1** (after U1) | Capstone scaffold exists; target identity + manifest admission prove through `faber run --target fmir`; CLI + receipt contract frozen in README; `check-compile` green — **gated, not open**: green requires the SEM006 `privata`→`@ publica` visibility migration (GGUF-A1c) to have landed on the committed tree (M6-U1 done_when (f)); a throwaway-annotated-copy receipt is provisional, never the done oracle | Mind accepts M6-U1 |
| **M6-G2** (after U2) | Both prompts encode/decode through the artifact tokenizer matching the pinned oracle | Mind accepts M6-U2 |
| **M6-G3** (after U3) | Every required tensor binds with checked ranges; slice comparison passes; no whole-model F32 expansion | Mind accepts M6-U3 |
| **M6-G4** (after U4) | 753-tensor admission fails closed on mutation; both prompts produce ≥256 matching reference tokens | Mind accepts M6-U4 |
| **M6-G5** (after U5) | Metal (burgus) + CUDA (RunPod ≥48 GB pod) persistent resident sessions, ≥256 tokens/prompt, counters + receipts per campaign contract; no pharos CUDA row is CAP-02 evidence | Mind accepts M6-U5 (evidence for CAP-01/CAP-02) |
| **M6-G6** (after U6) | Clean-packet reproduction both backends; docs reconcile to receipts; successor chain to CLOSE-01 stated | Mind accepts M6-U6 |
| **Campaign successors** | CAP-01, CAP-02, CLOSE-01 remain mandatory; CLOSE-01 requires independent audit of every invariant clause | Mind + campaign owners |

## 6. Validation Summary

```text
U1: check-compile ok on the committed tree (post-A1c; see M6-G1) + faber run --target fmir exit 0 + PASS oracle facts (version/alignment/data/metadata/tensors/architecture/bytes);
    shasum -a 256 == pinned digest; no tensor-data read; git diff --check
U2: encode/decode of both prompts == pinned llama.cpp ids/text at first divergence; receipt records ids + text; git diff --check
U3: per-tensor range/shape/layout binding + selected-slice comparison PASS; no whole-model F32 grep; git diff --check
U4: admission PASS (753) + mutation fail-closed matrix; both prompts ≥256 reference tokens matching oracle; first-divergence recorded; git diff --check
U5: Metal (burgus) + CUDA (RunPod ≥48 GB pod) receipts with full campaign clause set; counters (0 reload/recompile/rebuild/round-trip);
    peak memory/timing/lifecycle observed; git diff --check
U6: clean-packet reproduction on both named machines (burgus Metal; RunPod pod CUDA); inventory-public-symbols green; docs rows map to receipts; successor statement present; git diff --check
```

No cargo in this lowering's validation (planning artifact). Implementing units
run the package checks above; device runs are the units' own closeout gates.

## 7. Scope Closure And Successors

This lowering **advances milestone Q4 toward its gate** by making the M6
capstone implementable in staged units with the first frontier (M6-U1)
dispatchable now. **Unit completion is not campaign completion**: M6 delivery
satisfies the capstone application chain, but the campaign completes only at
`CLOSE-01`, which requires CAP-01 (Metal) and CAP-02 (CUDA) capstone receipts
and the independent closeout audit of every invariant clause. Nothing here
narrows, downgrades, defers, makes optional, or moves admitted Qwen work
outside the campaign; the full successor chain `M6-U5 → CAP-01 → CAP-02 →
CLOSE-01` is preserved and named.

## 8. Open Questions (for Mind; defaults recorded, none blocks)

1. **Capstone CLI arg surface** (M6-U1) — default: the frozen contract above
   (`--sha256`, `--oracle-offset`, `--prompt …`, `--max-new-tokens`,
   `--seed`, `--receipt`); Mind may adjust before dispatch.
2. **faber binary revision pairing** (all units) — default: the implementing
   Hand rebuilds `faber` from the current radix tree so the committed `la`
   reader pack validates; a persistent failure routes to the radix/locale
   lane (recorded tooling note).
3. **Resource-limited reference mode** (M6-U4) — default: any bounded
   reference mode still executes every layer and records it; a reduced-model
   substitute fails the unit (delivery authority clause).
4. **Clean-packet definition** (M6-U6) — default: temporary home, minimal
   PATH, no sibling checkout/private state, downloaded/committed package +
   binary only (the R2/E7 precedent).
5. **Prompt selection** (M6-U2/U4/U5) — default: two operator-supplied
   Unicode prompts frozen per unit with prompt hashes in the receipt; the
   exact probe texts are a Mind/dispatch decision, not a capstone embedding.

---

*Planning artifact only. No product code was written. Hands implement from
this spec; Mind files units. M6-U1 is the first implementation frontier and
is dispatchable now (M6-G1 acceptance is gated on committed-tree green —
the SEM006/A1c visibility migration must have landed); M6-U2..U6 are waved
and entry-gated on the named predecessor receipts (GGUF-A2, GGUF-A3,
GGUF-M1+M4, GGUF-M5). CAP-02's CUDA machine is the cap02 authority's RunPod
≥48 GB pod; pharos is smoke/capability evidence only. The campaign successor
chain through CLOSE-01 is preserved.*
