# Delivery: LIB-02 — Artifact-Backed Tokenizer And Detokenizer (GGUF-A2)

**Campaign**: radix
[`gpu-production-readiness/CAMPAIGN.md`](../../../../radix/docs/factory/gpu-production-readiness/CAMPAIGN.md)
LIB-02
**Semantic authority**:
[`pml5-general-gguf-delivery.md`](pml5-general-gguf-delivery.md) unit
**GGUF-A2** (Tokenizer Runtime)
**Owner repo**: gradus. **Control-plane repo**: radix.
**Status**: lowered 2026-08-13 by planner-22 (fresh lowering — derived
independently from campaign, delivery authority, and live repos; no
planner-1..19 worktrees, commits, or transcripts read).
**Predecessor**: LIB-01 / GGUF-A1c (capsule/caller clean break).
**Successors preserved through CLOSE-01**: LIB-03, REF-01, MODEL-01,
MODEL-02, MODEL-03, MODEL-04, EXEC-01, EXEC-02, EXEC-03, CAP-01, CAP-02,
CLOSE-01. Nothing in this delivery narrows, downgrades, defers, or makes
optional any admitted Qwen work.

## Goal Check

**verdict**: READY for delivery.
**basis**: the campaign is in `campaign_mode: run` with the exact artifact,
invariant, and dependency graph frozen; the delivery authority names GGUF-A2
with a concrete done-when and primary scope; live gradus source and the pinned
llama.cpp oracle were verified in this lowering (facts below). No blocking gap
in the goal; the only named risk is the pre-tokenizer expressiveness boundary
(see Unit U3 and Open Questions).
**consumer**: delivery → Hand implementation.
**recommended_next**: admit the unit graph below and dispatch Hands after
LIB-01 lands (or, for U1 which binds only schema-2 `gguf_manifest` surfaces,
at Mind's serialization call once A1c is committed).

## Interpreted Scope

Lower mandatory campaign work **LIB-02 — implement artifact-backed tokenizer
and detokenizer** into an implementation-ready unit graph for Gradus. The
completion oracle is: **two Unicode prompts match pinned llama.cpp token ids
and decoded text on the exact target artifact.**

The target artifact is frozen:

| Fact | Value |
| --- | --- |
| File | `Qwen3.6-35B-A3B-UD-Q4_K_M.gguf` |
| Byte length | 22,663,387,424 |
| SHA-256 | `0b21525e972670ed59e1812e170b27c26355381f0656ecc4e25617ece7dac58b` |
| Architecture | `qwen35moe` (753 tensors, data offset 10,991,392) |
| Tokenizer model | `gpt2` (byte-level BPE) |
| Pre-tokenizer | `qwen35` |
| Vocab count | 248,320 |
| Merge count | 247,587 |
| BOS id / token | 248044 `<|endoftext|>` |
| EOS id / token | 248046 `<|im_end|>` |
| PAD id | 248055 |
| add_bos_token | false |
| EOG set | {248044, 248046, 248063, 248064, 248065} |
| Special-token cache | 33 |
| Chat template | Qwen3 ChatML (vision/tool-calling variant in metadata) |

Facts were verified live in this lowering against the artifact metadata
(llama-gguf / llama-tokenize load log) and the pinned llama.cpp source
(`llama-vocab.cpp` LLAMA_VOCAB_PRE_TYPE_QWEN35).

## Pinned Oracle — Two Unicode Probes

Oracle tool: `/opt/homebrew/bin/llama-tokenize` version 10150
(`dee2a846b`), same build the PML2-U4 evidence pins. Probes were executed on
the exact target artifact on 2026-08-13 and are deterministic (re-ran
identical).

### Probe A — Thai

```
prompt: สวัสดีครับ ผมชื่ออเล็กซ์
ids:    [34469, 168607, 153295, 173922, 153380, 22216, 151752, 172769]
count:  8
sha256: e30101d62c4e484ae2544643398b2cd6f562ccd8cf76832c39034b19ebc56a35
decoded text must round-trip to the exact prompt.
```

### Probe B — CJK + emoji + digits

```
prompt: 你好，世界！今天是2026年8月13日 🎉
ids:    [109266, 3709, 96748, 6115, 113128, 17, 15, 17, 21, 95859, 23,
         96212, 16, 18, 95971, 10838, 236, 231]
count:  18
sha256: 855d730303db213db698dad3378d682d6968f6c046e70e5c7c1b05bfb7923588
decoded text must round-trip to the exact prompt.
```

### Word-level differential probes (BPE-core boundary, Unit U2)

| Prompt | Pinned ids | sha256 |
| --- | --- | --- |
| `transformers` | `[4549, 382]` | `ad9b0702bc418499b1f2fb4eea3f87e9aaf24aeb315f12b79dd2e9efaa9bda20` |
| `สวัสดี` | `[34469, 168607]` | `4ad434bd60c467ad71c61029edf3a84f65dc5ec5742aa0c0dc2afaa1e226198a` |
| `人工智能` | `[109015]` | `161332dd5ba244f14566d9ccfc214dbbd620bcd401cded068fc230e3d4e2815b` |

### Special-token policy probes

`<|im_start|>` → `[248045]` (specials parsed); with `--no-parse-special` →
`[27, 91, 316, 4747, 91, 29]` (literal bytes). EOG membership and
BOS-free behavior are pinned by the metadata facts above.

## Normalized Spec

1. **Artifact-backed only.** The tokenizer consumes vocab, token types,
   merges, pre-tokenizer identity, special-token policy, EOG behavior, and
   the chat template **from the parsed artifact** (schema-2 manifest
   values). No hard-coded prompt, vocab table, token-id list, or
   Qwen-specific fallback exists anywhere in the capstone path. The existing
   SmolLM2 identity contract (`gradus:tokenizer`, PML2-U4) stays the
   SmolLM2 admission contract; the GGUF-A2 runtime is the artifact-backed
   execution surface. No forwarding shim between them.
2. **Two executed proof rows.** Probe A and Probe B are the LIB-02 completion
   oracle: encode must produce the exact pinned id lists and decode must
   reproduce the exact prompt text (byte-level BPE round-trip) on the target
   artifact.
3. **Word-level boundary first.** Byte-level BPE core (vocab lookup, merge
   application, byte↔unicode mapping, decode concatenation) is proven on
   word-level inputs where the pre-tokenizer is identity (U2), then the
   qwen35 pre-tokenizer and special/EOG/chat policy compose to the full
   probe oracle (U3).
4. **First failing oracle.** Every unit carries a red test asserting the
   pinned id lists/round-trips before implementation; the failing command is
   the same command the green closeout uses. Divergence receipts record the
   first divergent tokenizer id or decoded character, never text-level
   similarity.
5. **Device-neutral and owner-clean.** The tokenizer is pure values and
   operations on Gradus-owned data. It never owns a path, file handle,
   memory mapping, device handle, or whole-model byte list. File access stays
   with an application-owned adapter (the `gguf-inspect` range-source
   pattern). No Metal/CUDA claim in this delivery.
6. **Local corpus boundary.** The two probes and the differential word list
   are the only operator text inputs. The target artifact is read only
   through a bounded source that never touches tensor payload bytes (the
   header/table prefix pattern already proven in GGUF-A1b). No GGUF bytes are
   committed; pinned id lists and prompt hashes are committed.
7. **Selected chat-template behavior.** The capstone applies the artifact's
   ChatML user-turn rendering (the minimal path the two prompts exercise),
   loaded from `tokenizer.chat_template` metadata. A universal Jinja/chat
   template language engine is out of scope (delivery authority scope
   matrix). Full vision/tool template branches are recorded, not executed.
8. **Clean break posture.** The tokenizer runtime surface is new public API
   on `gradus:tokenizer`; it does not reuse the SmolLM2 probe constants as
   execution defaults. Internal callers are not a contract.

## Repo-Aware Baseline

Verified 2026-08-13 against the live worktree state:

- **gradus** branch `factory/planner-22` tip `bc50099`
  (`docs(factory): require Qwen3.6 GGUF execution`), tree clean.
- **radix** branch `factory/planner-22` tip `b6d6e17c8`
  (`docs(factory): narrow GPU campaign to Qwen3.6`), tree clean.
- `src/model/gguf_manifest.fab` (1090 lines) already exposes schema-2
  `ManifestumGguf`, `parse`, `metadatum`, `textum`, `numerum`,
  `inveni_tensorem`, `layout`, `inspice`, `lege_fragmentum`. **No typed
  array accessors exist yet** for `tokenizer.ggml.tokens` /
  `token_type` / `merges` — the metadata arrays are preserved as wire bytes
  but not exposed as lists. U1 owns that gap.
- `src/tokenizer.fab` (573 lines) is the SmolLM2 **identity** contract
  (pinned P1–P11 + workload lists, `est_eog`, `IdentitasTokenizator`). No
  runtime encode/decode exists. GGUF-A2 extends this module with the
  artifact-backed runtime surface.
- `exempla/qwen36-35b-inference` does not exist yet — U4 creates its
  tokenizer phase (the delivery authority names this exempla as the GGUF-A2
  consumer).
- Oracle tooling live: `/opt/homebrew/bin/llama-tokenize` 10150
  (`dee2a846b`); target artifact present at
  `/Users/ianzepp/Ai/models/Qwen3.6-35B-A3B-UD-Q4_K_M.gguf` (operator
  evidence, never committed).
- Gate scripts: `./scripta/check-source`, `./scripta/check-compile`
  (package-aware `faber check` with `FABER_LIBRARY_HOME` +
  `FABER_BIN`). No faber binary inside the planner-22 worktree; dispatch
  from the lane with the established binary path
  (`worktrees/hand-2/radix/target/debug/faber` or the Hand packet's value).

## Unit Graph

```text
LIB-02-U1  manifest tokenizer metadata accessors   (leaf, schema-2 manifest only)
    -> LIB-02-U2  byte-level BPE core encode/decode (word-level oracle)
         -> LIB-02-U3  qwen35 pre-tokenizer + special/EOG/chat policy
                        (full two-probe oracle)
              -> LIB-02-U4  capstone tokenizer phase + docs + receipts
```

Split boundary: **metadata reads (U1)** vs **BPE core semantics (U2)** vs
**pre-tokenizer + policy composition (U3)** vs **capstone consumer + docs
(U4)**. Each is one independently verifiable outcome; none is safe to
parallelize on the same write surface (U2/U3 both touch
`src/tokenizer.fab`). Dispatch serially in order; the campaign dependency
graph (LIB-02 after LIB-01) binds U2–U4 after the A1c clean break commits.

### LIB-02-U1 — Manifest tokenizer metadata accessors

- **outcome**: typed array and scalar accessors on `gradus:model/gguf_manifest`
  read the tokenizer metadata block of a parsed `ManifestumGguf` with exact
  values and typed errors.
- **write_scope**: `src/model/gguf_manifest.fab`, `src/model/gguf_manifest.proba`,
  `docs/api-reference.md`, `docs/module-map.md`, `docs/diagnostics.md`,
  `docs/regression-corpus.md`, `docs/factory/production-ml-library/pml0-support-matrix.md`.
- **read_scope**: `pml5-general-gguf-delivery.md`, this delivery, the live
  manifest proba.
- **forbidden_scope**: any tokenizer runtime code, any edit to
  `src/tokenizer.fab`, any tensor-payload access, main-checkout edits.
- **done_when**: `textorum(ManifestumGguf, clavis) -> lista<textus>` and
  `numerorum(ManifestumGguf, clavis) -> lista<numerus>` (or the module's
  naming convention) return the tokenizer arrays from a corpus containing
  the metadata block; scalar tokenizer ids/template read via the existing
  `textum`/`numerum` surface; missing/malformed/duplicate keys produce typed
  `GgufManifestError` rows; proba pins exact counts 248320 tokens, 247587
  merges, and the pinned special ids from the target-prefix corpus.
- **validation**: `./scripta/check-source`; `./scripta/check-compile`
  (FABER_LIBRARY_HOME + FABER_BIN from the Hand packet); `git diff --check`
  over the write scope. Green closeout once.
- **first failing oracle**: a proba asserting the pinned counts/ids against
  the current surface (fails — no array accessors exist).
- **est_work_tokens**: 24k–48k. **est_basis**: pilot (first-of-class:
  schema-2 manifest array accessors; no close ledger class).
- **tool_latency**: low–medium (`check-compile` ~1–2 min cold; llama-gguf
  prefix read for pin verification).
- **parallel_children_considered**: none — single accessor surface,
  indivisible.

### LIB-02-U2 — Byte-level BPE core encode/decode

- **outcome**: the artifact-backed BPE core maps a word-level input to the
  exact pinned id lists and decodes them back to the exact input text,
  using only the vocab/merges from the manifest.
- **write_scope**: `src/tokenizer.fab`, `src/tokenizer.proba`,
  `docs/api-reference.md`, `docs/diagnostics.md`, `docs/regression-corpus.md`.
- **read_scope**: U1 accessors, this delivery's word-level oracle, llama.cpp
  `llm_tokenizer_bpe` reference semantics (read-only), the byte-level BPE
  display/byte mapping convention.
- **forbidden_scope**: pre-tokenizer regex behavior, special-token policy,
  chat-template rendering, edits outside the listed files, tensor-payload
  access.
- **done_when**: `transformers` → `[4549, 382]`, `สวัสดี` →
  `[34469, 168607]`, `人工智能` → `[109015]` exactly; decode of each pinned
  id list reproduces the input; unknown ids and malformed byte sequences
  fail with typed errors; no hard-coded vocab/merge tables.
- **validation**: same gate scripts plus the word-level proba pins; green
  closeout once.
- **first failing oracle**: the three word-level id pins (fail — no runtime
  exists today).
- **est_work_tokens**: 40k–80k. **est_basis**: pilot (first-of-class:
  Gradus artifact-backed BPE runtime; no close ledger class).
- **tool_latency**: medium (check-compile + llama-tokenize differential).
- **parallel_children_considered**: none — BPE core is indivisible and
  serialized on `src/tokenizer.fab`.

### LIB-02-U3 — qwen35 pre-tokenizer + special/EOG/chat policy

- **outcome**: the qwen35 pre-tokenizer and special-token policy compose the
  BPE core into full encode/decode, and the **two Unicode probes** match the
  pinned id lists with exact decoded round-trips on the target artifact.
- **write_scope**: `src/tokenizer.fab`, `src/tokenizer.proba`,
  `fixtures/tokenizer/` (pinned probe + chat-template identity oracle doc),
  `docs/api-reference.md`, `docs/diagnostics.md`, `docs/regression-corpus.md`,
  `docs/module-map.md`.
- **read_scope**: llama.cpp `llama-vocab.cpp`
  LLAMA_VOCAB_PRE_TYPE_QWEN35 regex (the pinned source reference), the
  artifact chat template metadata, this delivery's oracle.
- **forbidden_scope**: tensor payloads, Radix/Faber/Hosts product code,
  main-checkout edits, universal Jinja engine work.
- **done_when**: Probe A and Probe B encode to the exact pinned id lists and
  decode back to the exact prompts; `<|im_start|>` → `[248045]` (parsed) and
  `[27, 91, 316, 4747, 91, 29]` (literal); EOG set is `{248044, 248046,
  248063, 248064, 248065}` and BOS-free behavior is honored; chat template
  identity is loaded from metadata and the minimal user-turn rendering is
  applied; divergence receipts name the first divergent tokenizer id or
  decoded character.
- **validation**: gate scripts plus the full two-probe oracle run; green
  closeout once.
- **first failing oracle**: the two probe id lists (fail today — no
  runtime).
- **est_work_tokens**: 40k–80k. **est_basis**: pilot (first-of-class:
  qwen35 pre-tokenizer + policy in Fab; no close ledger class).
- **tool_latency**: medium (check-compile + llama-tokenize differential).
- **parallel_children_considered**: none — composes U2 on the same surface.
  **Named risk**: Fab has no regex engine; the qwen35 regex
  (`(?:'[sS]|'[tT]|…)|[^\r\n\p{L}\p{N}]?\p{L}\p{M}+|\p{N}| ?[^\s\p{L}\p{M}\p{N}]+…`)
  must be realized as a deterministic Unicode-category scanner covering the
  classes the probes exercise, pinned by differential oracle rows. If the
  language surface cannot express the required Unicode category tables, the
  Hand stops at the first diverging probe and files a **need** to Mind
  (default: implement the bounded category scanner; no hard-coded per-probe
  id list ever substitutes).

### LIB-02-U4 — Capstone tokenizer phase + docs + receipt

- **outcome**: `exempla/qwen36-35b-inference` runs the tokenizer phase of
  the capstone through public `gradus:*` imports, printing the pinned probe
  rows, and every support doc describes the observed result.
- **write_scope**: `exempla/qwen36-35b-inference/` (faber.toml, README.md,
  `src/main.fab`), `docs/module-map.md`, `docs/api-reference.md`,
  `docs/diagnostics.md`, `docs/regression-corpus.md`,
  `docs/factory/production-ml-library/pml0-support-matrix.md`,
  `docs/factory/production-ml-library/pml5-general-gguf-delivery.md`
  (GGUF-A2 status), this delivery's receipt section.
- **read_scope**: U1–U3 surfaces, the pinned oracle rows, the application
  adapter pattern from `exempla/gguf-inspect`.
- **forbidden_scope**: any tensor materialization, model forward, GPU
  execution, or full-capstone code beyond the tokenizer phase; main-checkout
  edits.
- **done_when**: one Faber package command encodes both probes through the
  public Gradus tokenizer surface and prints the pinned id lists + decoded
  text; the receipt names revisions, model identity, prompt hashes,
  tokenizer identity, command, expected vs observed rows, and any residual;
  docs agree.
- **validation**:
  ```bash
  cd /Users/ianzepp/work/faberlang/worktrees/hand-N/gradus
  ./scripta/check-source
  env FABER_LIBRARY_HOME=<lane> FABER_BIN=<lane faber> ./scripta/check-compile
  env FABER_LIBRARY_HOME=<lane> FABER_BIN=<lane faber> \
    faber run --target fmir exempla/qwen36-35b-inference
  git diff --check -- <write scope>
  ```
  Green closeout once.
- **first failing oracle**: the exempla run (fails today — no exempla).
- **est_work_tokens**: 20k–40k. **est_basis**: pilot (first-of-class:
  capstone tokenizer phase; no close ledger class).
- **tool_latency**: medium (check-compile + fmir run + doc checks).
- **parallel_children_considered**: none — single capstone-phase package,
  indivisible at this boundary.

## Checkpoints And Gates

1. U1 green before U2 starts (array accessors are the U2 input contract).
2. U2 green (word-level oracle) before U3 starts (U3 composes U2).
3. U3 green = **LIB-02 completion oracle satisfied** (both Unicode probes).
   This is the unit that advances milestone Q1's tokenizer input.
4. U4 closes the capstone-phase package and receipts.
5. LIB-01 (A1c) must be committed before U2–U4 dispatch; U1 binds only
   schema-2 `gguf_manifest` surfaces and may be dispatched when the Mind
   serializes the shared model surface. If the Mind dispatches U1 before
   A1c lands, the task body must say so and the manifest surface must not
   change under it.

## Validation Summary

- Executed proof per unit is exactly the unit's `validation` (Rule 6: once at
  closeout, no post-done thrash).
- The LIB-02 completion proof is: `faber run --target fmir
  exempla/qwen36-35b-inference` prints PASS rows for both probe id lists and
  both decoded round-trips, with `check-source`/`check-compile` exit 0 and
  `git diff --check` silent.
- The oracle tool is pinned (`llama-tokenize` 10150 `dee2a846b`); a different
  build is a different oracle row, not an acceptable substitute.

## Milestone And Scope-Closure Statement

- **Milestone advanced**: Q1 — executable library inputs (clean GGUF
  authority [LIB-01], **real tokenizer [LIB-02]**, packed tensor storage
  [LIB-03]). LIB-02 supplies the tokenizer input of Q1.
- **Unit completion ≠ campaign completion**: LIB-02 is one mandatory row.
  The exact artifact run through the complete `qwen35moe` graph with 256+
  new tokens for two resident prompts on both Metal and CUDA (Q4) is not
  reached here; LIB-03, REF-01, MODEL-01..04, EXEC-01..03, CAP-01, CAP-02,
  and CLOSE-01 remain mandatory with their frozen done oracles. Nothing in
  this delivery makes any of them optional, deferred, or satisfiable by a
  smaller model or structural proof.
- **Sequencing does not narrow scope**: the serial U1→U4 order and the
  word-level-first boundary only stage the same admitted work; the two
  Unicode probes, artifact-backed metadata consumption, llama.cpp ids/decode
  oracle, and no-hard-coded-fallback rule all survive to the completion row.

## Open Questions For Mind

1. **Pre-tokenizer expressiveness (named risk).** Fab has no regex engine
   and no Unicode general-category tables found in this lowering. Realizing
   the qwen35 regex as a deterministic scalar scanner is the default; if a
   bounded scan over the probe-exercised classes is not expressible, the
   Hand files a **need** — the unit must not degrade to per-probe id pins.
   Recommend the bounded-category-scanner default; escalate only on an
   actual language gap, not on size.
2. **Dispatch timing vs LIB-01.** U1 binds only schema-2 manifest surfaces;
   U2–U4 must follow the committed A1c clean break. Mind decides whether U1
   dispatches before A1c lands (serialization on `gguf_manifest.fab`) or
   with the rest.
3. **Token id list form for chat template.** The capstone applies the
   artifact's ChatML user-turn path; whether the two probes are encoded
   directly or through the template's rendered user turn is pinned in U4's
   receipt. Recommend: encode the raw prompt (the pinned oracle rows are
   raw-prompt rows) and separately prove the rendered-turn path composes
   without changing the pinned ids.

## First Implementation Frontier

LIB-02-U1: add the tokenizer array accessors to
`src/model/gguf_manifest.fab` with proba pins for the 248320/247587 counts
and the pinned special ids, then land U2. Dispatch as Hand tasks from the
admitted unit graph above; the Mind files Hand tasks — this planner files no
Hand tasks.
