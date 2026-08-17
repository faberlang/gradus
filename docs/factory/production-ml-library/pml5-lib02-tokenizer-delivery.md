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
planner-1..19 worktrees, commits, or transcripts read). **Re-split
2026-08-14 by planner-22**: LIB-02-U3 and LIB-02-U4 decomposed into
execution-scale micro-units (U3-1..U3-7, U4-1..U4-3) under the operator
granularity bar (2026-08-14) — each unit is one behavior family executable
in ~10–15 minutes, carrying all eight campaign-rule-2 fields. U1/U2 landed
on hand-16 (`c4d0750` U1 accessors; `f3cfa58` U2 word-level BPE core).
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
(now isolated in micro-unit U3-1 and Open Questions).
**consumer**: delivery → Hand implementation.
**recommended_next**: admit the micro-unit graph below and dispatch
LIB-02-U3-1 (U1/U2 have landed on hand-16; U3-1..U3-7 dispatch serially,
then U4-1, then U4-2/U4-3 in parallel).

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
`[27, 91, 316, 4747, 91, 29]` (literal bytes). `<|im_end|>` → `[248046]`
(parsed) and `[27, 91, 316, 6018, 91, 29]` (literal); `<|endoftext|>` →
`[248044]` (parsed) and `[27, 91, 8426, 703, 419, 91, 29]` (literal).
Embedded specials: `a<|im_end|>b` → `[64, 248046, 65]` (parsed) and
`[64, 27, 91, 316, 6018, 91, 29, 65]` (literal). EOG membership and
BOS-free behavior are pinned by the metadata facts above.

### Pre-tokenizer differential rows (micro-unit oracles)

Pinned live 2026-08-14 from the same oracle (`llama-tokenize` 10150
`dee2a846b`, target artifact) to give every U3 micro-unit a first-failing
oracle and a green closeout pin. All rows deterministic (re-ran twice).

Word-boundary / digit / newline rows (U3-2 core scanner families):

| Prompt | Pinned ids | sha256 |
| --- | --- | --- |
| `transformers สวัสดี 人工智能` | `[4549, 382, 245990, 220, 109015]` | `b3a7dcd98070161da790a3478c1b3cfa113cf622ab4bf583fd16ffb66cbaa7d9` |
| `transformers  สวัสดี` (double space) | `[4549, 382, 220, 245990]` | `552bdd86b661faa6fb22cc11128b9dcf086466f32a83418edbaa1d8fff267b05` |
| ` 你好` (leading space) | `[220, 109266]` | `6b6f27acd55005555aba99da08ff2bcda5ba019483ccea0c5af5e1a7bf12a8e7` |
| `你好 ` (trailing space) | `[109266, 220]` | `281868c19ef660fed76803180fe714ea8d265c58a7eef8737da7ae83c1f654a7` |
| `a   b` (three spaces) | `[64, 256, 292]` | `b4ca49d188d23e03e7b8c4cf587a82ad9936bf46d22cf9f47a0f00a07bcd41f8` |
| `2026` | `[17, 15, 17, 21]` | `158a323a7ba44870f23d96f1516dd70aa48e9a72db4ebb026b0a89e212a208ab` |
| `123` | `[16, 17, 18]` | `a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3` |
| `a\nb` | `[64, 198, 65]` | `7e18f737311b2dc3b2f269dd78396b0351f14fb66efa879f768cb23181883c78` |
| `a\n\nb` (blank line) | `[64, 271, 65]` | `38022fd2b8dbc5cb3d2cee74e083edbf59e3d4e13d067ebcb5db633d4cff4d8c` |
| `a\tb` (tab) | `[64, 2161]` | `894891f8b78a9945b0aa07e70d5f71f10b1f1990af127de561cc0ac36024c188` |

Punctuation/emoji rows (U3-3 scanner edge families):

| Prompt | Pinned ids | sha256 |
| --- | --- | --- |
| `hello, world!` | `[14556, 11, 1814, 0]` | `68e656b251e67e8358bef8483ab0d51c6619f3e7a1a9f0e75838d41ff368f728` |
| `🎉🎉` (emoji pair) | `[9008, 236, 231, 9008, 236, 231]` | `9bbfb34258a51fc6a5c2e0aeececc76c84029a9b001a819c1026a4849a44d0a0` |
| `!hello` (leading punct) | `[0, 14556]` | `4f6db4e113a49dbf0ff86b114880a5f9b22be40cb3f80bcb37ee7d23691f84ba` |
| `don't` | `[14572, 914]` | `df7682099c96e3f66171aed65ba78ae5200ba7200278569327e6cabf16c98b96` |
| `it's` | `[275, 579]` | `24ceef1cb6b0cbc0b3321021318245760500d1b1e9411a091929268ad1491c9e` |
| `I'm` | `[40, 2688]` | `c9d7ed34ba7890f69090bd0612643736348055d85f90ae7bba6fd4175dc482c9` |
| `you've` | `[9053, 2908]` | `52f3325c65b03c26f113b18fcb89cecfb89b3df37bf83b150c979502893cd118` |

BOS-free rows (U3-5): empty prompt → `[]` (no BOS); `x` → `[87]`
(no BOS prefix, sha256 `2d711642b726b04401627ca9fbac32f5c8530fb1903cc4db02258717921a4881`).

Chat-template rows (U3-6), minimal Qwen3-ChatML user-turn render
`<|im_start|>user\n{Probe B}<|im_end|>\n`:

| Prompt | Pinned ids | sha256 |
| --- | --- | --- |
| rendered Probe B user turn | `[248045, 846, 198, 109266, 3709, 96748, 6115, 113128, 17, 15, 17, 21, 95859, 23, 96212, 16, 18, 95971, 10838, 236, 231, 248046, 198]` | `595812a1e88de2260a478a78ea25683025e1627c4f88df639129526b52f08ceb` |
| same, `--no-parse-special` | `[27, 91, 316, 4747, 91, 29, 846, 198, 109266, 3709, 96748, 6115, 113128, 17, 15, 17, 21, 95859, 23, 96212, 16, 18, 95971, 10838, 236, 231, 27, 91, 316, 6018, 91, 29, 198]` | same prompt hash |
| `<|im_start|>assistant\n` | `[248045, 74455, 198]` | `fb3832354a86f4328bdfbf33691473fc7c08824ff6bd056f4b90c95d7fe9eaa4` |

`[248045]` is `<|im_start|>` (BOS special), `[846]` is `user`, `[198]` is
`\n`, `[248046]` is `<|im_end|>`, `[74455]` is `assistant`. The rendered
user-turn row proves the ChatML path composes **without changing the pinned
Probe B ids** (open question 3 recommendation, now pinned).

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
   probe oracle (U3-1..U3-7).
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

Verified 2026-08-13 against the live worktree state; re-verified 2026-08-14
on the re-split (U1/U2 have landed since):

- **gradus** branch `factory/planner-22` tip `a0f311f` (this delivery
  commit), tree clean. **U1 landed on hand-16** (`c4d0750`, typed
  `textorum`/`numerorum` array accessors) and **U2 landed on hand-16**
  (`f3cfa58`, `Tokenizer` genus with `build`/`encode`/`decode`,
  byte↔display mapping, ranked merges, decode, new typed errors).
- **radix** branch `factory/planner-22` tip `b6d6e17c8`
  (`docs(factory): narrow GPU campaign to Qwen3.6`), tree clean.
- `src/model/gguf_manifest.fab` (1090 lines) already exposes schema-2
  `GgufManifest`, `parse`, `metadata`, `textum`, `numerum`,
  `inveni_tensorem`, `layout`, `inspect`, `read_fragmentum`. The U1
  accessors (`textorum`, `numerorum`) read `tokenizer.ggml.tokens` /
  `token_type` / `merges` as typed lists.
- `src/tokenizer.fab` carries the SmolLM2 **identity** contract (pinned
  P1–P11 + workload lists, `est_eog`, `TokenizerIdentity`) plus the U2
  artifact-backed `Tokenizer` runtime. GGUF-A2 continues extending this
  module with the pre-tokenizer + policy surface (U3-1..U3-7).
- `exempla/qwen36-35b-inference` does not exist yet — U4-1 creates its
  tokenizer phase (the delivery authority names this exempla as the GGUF-A2
  consumer).
- Oracle tooling live: `/opt/homebrew/bin/llama-tokenize` 10150
  (`dee2a846b`); target artifact present at
  `/Users/ianzepp/Ai/models/Qwen3.6-35B-A3B-UD-Q4_K_M.gguf` (operator
  evidence, never committed). Differential rows re-run and re-pinned on
  2026-08-14 (see "Pre-tokenizer differential rows").
- Gate scripts: `./scripta/check-source`, `./scripta/check-compile`
  (package-aware `faber check` with `FABER_LIBRARY_HOME` +
  `FABER_BIN`). No faber binary inside the planner-22 worktree; dispatch
  from the lane with the established binary path
  (`worktrees/hand-2/radix/target/debug/faber` or the Hand packet's value).

## Unit Graph

```text
LIB-02-U1  manifest tokenizer metadata accessors   (leaf, schema-2 manifest only)
    -> LIB-02-U2  byte-level BPE core encode/decode (word-level oracle)
         -> LIB-02-U3-1  Unicode-category tables + predicates (scanner data)
              -> LIB-02-U3-2  qwen35 word-splitting scanner (core families)
                   -> LIB-02-U3-3  qwen35 scanner edge families (punct/emoji/contractions)
                        -> LIB-02-U3-4  special-token policy
                             -> LIB-02-U3-5  EOG + BOS-free policy
                                  -> LIB-02-U3-6  chat-template policy
                                       -> LIB-02-U3-7  full two-probe composition
                                                        + divergence receipts
                                            -> LIB-02-U4-1  capstone tokenizer-phase exempla
                                                 -> LIB-02-U4-2  library docs agree
                                            -> LIB-02-U4-3  campaign docs + receipt
```

Split boundary: **metadata reads (U1)** vs **BPE core semantics (U2)** vs
**pre-tokenizer + policy composition (U3, decomposed into seven one-family
micro-units U3-1..U3-7)** vs **capstone consumer + docs + receipt (U4,
decomposed into U4-1..U4-3)**. Re-split 2026-08-14 by planner-22 under the
operator granularity bar (2026-08-14): each micro-unit is one behavior
family, executable by a Hand in ~10-15 minutes, carrying the full eight
campaign-rule-2 fields. Every micro-unit touches `src/tokenizer.fab` /
`src/tokenizer.proba` except the docs units, so U3-1..U3-7 dispatch
serially; U4-2 (library docs) and U4-3 (campaign docs + receipt) are
disjoint and may dispatch in parallel after U4-1. The campaign dependency
graph (LIB-02 after LIB-01) binds U2–U4 after the A1c clean break commits.

### LIB-02-U1 — Manifest tokenizer metadata accessors

- **outcome**: typed array and scalar accessors on `gradus:model/gguf_manifest`
  read the tokenizer metadata block of a parsed `GgufManifest` with exact
  values and typed errors.
- **write_scope**: `src/model/gguf_manifest.fab`, `src/model/gguf_manifest.proba`,
  `docs/api-reference.md`, `docs/module-map.md`, `docs/diagnostics.md`,
  `docs/regression-corpus.md`, `docs/factory/production-ml-library/pml0-support-matrix.md`.
- **read_scope**: `pml5-general-gguf-delivery.md`, this delivery, the live
  manifest proba.
- **forbidden_scope**: any tokenizer runtime code, any edit to
  `src/tokenizer.fab`, any tensor-payload access, main-checkout edits.
- **done_when**: `textorum(GgufManifest, clavis) -> lista<textus>` and
  `numerorum(GgufManifest, clavis) -> lista<numerus>` (or the module's
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

### LIB-02-U3-1 — Unicode-category tables + predicates (scanner data)

- **outcome**: a deterministic Unicode-category classification surface
  (letter / mark / number / whitespace / newline tables + predicates) for
  the qwen35 pre-tokenizer scanner, covering the classes the two probes and
  the differential rows exercise; the named-risk "can Fab express the
  required category tables" question is answered first, in isolation.
- **exact write scope**: `src/tokenizer.fab`, `src/tokenizer.proba`.
- **read_scope**: llama.cpp `llama-vocab.cpp`
  LLAMA_VOCAB_PRE_TYPE_QWEN35 regex classes (`\p{L}`, `\p{M}`, `\p{N}`,
  `\s`, CR/LF), this delivery's oracle.
- **forbidden_scope**: word-splitting logic (U3-2/U3-3), special/EOG/chat
  policy, tensor payloads, main-checkout edits.
- **first failing oracle**: a proba asserting the category of the
  probe-exercised codepoints (e.g. `ก` → letter, `า` → mark, `0` → number,
  ` ` → whitespace, `\n` → newline, `🎉` → other) — fails today (no
  classification surface exists).
- **closeout command**: `./scripta/check-source`;
  `./scripta/check-compile` (FABER_LIBRARY_HOME + FABER_BIN from the Hand
  packet); `git diff --check -- src/tokenizer.fab src/tokenizer.proba`.
  Green closeout once.
- **expected observed result**: check-source / check-compile exit 0; the
  category proba pins classify the probe-exercised codepoints exactly;
  `git diff --check` silent.
- **est_basis**: pilot (first-of-class: Unicode-category tables in Fab; no
  close ledger class). est_work_tokens 8k–14k. ~10–15 min.
- **stop condition**: if a required Unicode category class cannot be
  expressed, stop at the first unrepresentable class and file a **need** to
  Mind (default: implement the bounded category scanner; a hard-coded
  per-probe id list never substitutes).
- **depends_on**: LIB-02-U2 (BPE core, for the composition seam the
  scanner feeds).

### LIB-02-U3-2 — qwen35 word-splitting scanner (core families)

- **outcome**: the deterministic qwen35 pre-tokenizer scanner splitting
  text into words for the core content families — letter/mark runs
  (`[^\r\n\p{L}\p{N}]?[\p{L}\p{M}]+`), single numbers (`\p{N}`), whitespace
  runs (`\s+`, `\s+(?!\S)`), and newline runs (`\s*[\r\n]+`) — feeding the
  U2 BPE core.
- **exact write scope**: `src/tokenizer.fab`, `src/tokenizer.proba`.
- **read_scope**: llama.cpp `llm_tokenizer_bpe` pre-tokenizer application
  order (read-only), U3-1 category surface, this delivery's differential
  rows.
- **forbidden_scope**: punctuation/emoji runs, contractions, leading-punct
  rule (U3-3), special/EOG/chat policy, tensor payloads, main-checkout
  edits.
- **first failing oracle**: the word-boundary / digit / newline differential
  rows (the 10-row table in "Pre-tokenizer differential rows") — fail today
  (no splitter).
- **closeout command**: `./scripta/check-source`;
  `./scripta/check-compile` (FABER_LIBRARY_HOME + FABER_BIN from the Hand
  packet); `git diff --check -- src/tokenizer.fab src/tokenizer.proba`.
  Green closeout once.
- **expected observed result**: encode of each word-boundary / digit /
  newline row yields its exact pinned id list through scanner + BPE core;
  decode round-trips; gates exit 0.
- **est_basis**: pilot (first-of-class: qwen35 content scanner in Fab; no
  close ledger class). est_work_tokens 10k–18k. ~10–15 min.
- **stop condition**: first diverging differential row → stop and record a
  divergence receipt naming the first divergent tokenizer id; if the
  category tables are the blocker, file the U3-1 need. No hard-coded
  per-probe id list.
- **depends_on**: LIB-02-U3-1.

### LIB-02-U3-3 — qwen35 scanner edge families (punct/emoji/contractions)

- **outcome**: the remaining qwen35 regex families composed into the same
  scanner — punctuation/emoji/other runs with optional leading space and
  trailing newlines (` ?[^\s\p{L}\p{M}\p{N}]+[\r\n]*`) and the contraction
  family (`'s|'t|'re|'ve|'m|'ll|'d`).
- **exact write scope**: `src/tokenizer.fab`, `src/tokenizer.proba`.
- **read_scope**: llama.cpp LLAMA_VOCAB_PRE_TYPE_QWEN35 regex edge
  alternatives, U3-2 scanner, this delivery's differential rows.
- **forbidden_scope**: special-token policy (U3-4), EOG/chat policy, tensor
  payloads, main-checkout edits.
- **first failing oracle**: the punctuation/emoji/contraction differential
  rows (P1–P3, C1–C4 in "Pre-tokenizer differential rows") — fail today.
- **closeout command**: `./scripta/check-source`;
  `./scripta/check-compile` (FABER_LIBRARY_HOME + FABER_BIN from the Hand
  packet); `git diff --check -- src/tokenizer.fab src/tokenizer.proba`.
  Green closeout once.
- **expected observed result**: each edge-family row encodes to its exact
  pinned id list; decode round-trips; gates exit 0.
- **est_basis**: pilot (first-of-class: qwen35 edge scanner in Fab; no
  close ledger class). est_work_tokens 8k–14k. ~10–15 min.
- **stop condition**: first diverging edge row → divergence receipt with the
  first divergent id; no hard-coded per-row id list; escalate only on a real
  language gap.
- **depends_on**: LIB-02-U3-2.

### LIB-02-U3-4 — Special-token policy

- **outcome**: the artifact's special-token cache (33 specials incl. the
  pinned ids) drives parse-special on/off: specials inside text resolve to
  their single ids when parsed, and to literal BPE bytes when
  `parse_special = falsum`, including embedded specials.
- **exact write scope**: `src/tokenizer.fab`, `src/tokenizer.proba`.
- **read_scope**: artifact `tokenizer.ggml.token_type`/special-token
  metadata (via U1 accessors), the pinned special-token probes.
- **forbidden_scope**: pre-tokenizer splitting changes (U3-2/U3-3),
  EOG/chat policy, tensor payloads, main-checkout edits.
- **first failing oracle**: the special-token probe rows (`<|im_start|>`
  parsed vs literal, embedded-special rows) — fail today.
- **closeout command**: `./scripta/check-source`;
  `./scripta/check-compile` (FABER_LIBRARY_HOME + FABER_BIN from the Hand
  packet); `git diff --check -- src/tokenizer.fab src/tokenizer.proba`.
  Green closeout once.
- **expected observed result**: `<|im_start|>` → `[248045]` (parsed) and
  `[27, 91, 316, 4747, 91, 29]` (literal); `<|im_end|>` → `[248046]`;
  `<|endoftext|>` → `[248044]`; embedded `a<|im_end|>b` → `[64, 248046,
  65]` (parsed) and `[64, 27, 91, 316, 6018, 91, 29, 65]` (literal); gates
  exit 0.
- **est_basis**: pilot (first-of-class: artifact special-token policy in
  Fab; no close ledger class). est_work_tokens 6k–12k. ~10 min.
- **stop condition**: a special does not resolve to its pinned id → record
  the first divergent id in a divergence receipt; specials must always come
  from the artifact cache, never a hard-coded map.
- **depends_on**: LIB-02-U3-3.

### LIB-02-U3-5 — EOG + BOS-free policy

- **outcome**: the runtime EOG policy on the artifact set `{248044,
  248046, 248063, 248064, 248065}` (est_eog equivalent on the runtime
  surface) and BOS-free encode honoring the artifact's
  `add_bos_token = falsum` (no BOS auto-prepend, empty prompt → empty
  sequence).
- **exact write scope**: `src/tokenizer.fab`, `src/tokenizer.proba`.
- **read_scope**: artifact tokenizer metadata (EOG set, `add_bos_token`),
  the delivery's BOS-free rows.
- **forbidden_scope**: scanner/special/chat behavior, tensor payloads,
  main-checkout edits.
- **first failing oracle**: the BOS-free rows (empty prompt → `[]`; `x` →
  `[87]`) plus an EOG-membership proba over the artifact set — fail today.
- **closeout command**: `./scripta/check-source`;
  `./scripta/check-compile` (FABER_LIBRARY_HOME + FABER_BIN from the Hand
  packet); `git diff --check -- src/tokenizer.fab src/tokenizer.proba`.
  Green closeout once.
- **expected observed result**: encode never prepends a BOS; empty prompt →
  `[]`; `x` → `[87]`; EOG membership admits exactly `{248044, 248046,
  248063, 248064, 248065}`; gates exit 0.
- **est_basis**: pilot (first-of-class: artifact EOG/BOS runtime policy in
  Fab; no close ledger class). est_work_tokens 6k–10k. ~10 min.
- **stop condition**: BOS-free or EOG behavior diverges from the pinned
  facts → divergence receipt; the runtime must read EOG/add_bos from the
  artifact, never hard-code the SmolLM2 contract.
- **depends_on**: LIB-02-U3-4.

### LIB-02-U3-6 — Chat-template policy

- **outcome**: `tokenizer.chat_template` loads from artifact metadata and
  the minimal Qwen3-ChatML user-turn rendering applies; the rendered-turn
  path composes without changing the pinned probe ids.
- **exact write scope**: `src/tokenizer.fab`, `src/tokenizer.proba`,
  `fixtures/tokenizer/` (chat-template identity oracle doc).
- **read_scope**: artifact `tokenizer.chat_template` metadata (via U1
  accessors), the pinned rendered-turn rows, Qwen3 ChatML minimal shape.
- **forbidden_scope**: a universal Jinja/template engine, tensor payloads,
  main-checkout edits.
- **first failing oracle**: the rendered user-turn rows (R1/R1b/R2 in
  "Pre-tokenizer differential rows") — fail today.
- **closeout command**: `./scripta/check-source`;
  `./scripta/check-compile` (FABER_LIBRARY_HOME + FABER_BIN from the Hand
  packet); `git diff --check -- src/tokenizer.fab src/tokenizer.proba
  fixtures/tokenizer`. Green closeout once.
- **expected observed result**: rendering Probe B's user turn produces
  `[248045, 846, 198, <exact Probe B ids>, 248046, 198]`; the
  no-parse-special variant matches its pinned literal row; the identity doc
  lands; gates exit 0.
- **est_basis**: pilot (first-of-class: minimal ChatML render in Fab; no
  close ledger class). est_work_tokens 8k–12k. ~10–15 min.
- **stop condition**: rendered-turn ids diverge from the pinned rows →
  divergence receipt; full vision/tool template branches are recorded, not
  executed (delivery scope matrix).
- **depends_on**: LIB-02-U3-5.

### LIB-02-U3-7 — Full two-probe composition + divergence receipts

- **outcome**: the complete composed runtime (scanner + BPE core + special
  policy + EOG/BOS + chat policy) encodes **Probe A and Probe B to the
  exact pinned id lists and decodes them back to the exact prompts**; the
  divergence-receipt form is demonstrated end to end.
- **exact write scope**: `src/tokenizer.fab`, `src/tokenizer.proba`,
  `fixtures/tokenizer/` (pinned probe oracle doc), `docs/api-reference.md`,
  `docs/diagnostics.md`, `docs/regression-corpus.md`, `docs/module-map.md`.
- **read_scope**: the pinned Probe A/B rows, U3-1..U3-6 surfaces.
- **forbidden_scope**: tensor payloads, Radix/Faber/Hosts product code,
  main-checkout edits, new behavior families beyond composition/receipts.
- **first failing oracle**: the two probe id lists (Probe A 8 ids, Probe B
  18 ids) through the composed runtime — fail today (no composed runtime
  entry yet).
- **closeout command**: `./scripta/check-source`;
  `./scripta/check-compile` (FABER_LIBRARY_HOME + FABER_BIN from the Hand
  packet); `git diff --check -- <write scope>`. Green closeout once.
- **expected observed result**: Probe A → `[34469, 168607, 153295, 173922,
  153380, 22216, 151752, 172769]` and Probe B → `[109266, 3709, 96748,
  6115, 113128, 17, 15, 17, 21, 95859, 23, 96212, 16, 18, 95971, 10838,
  236, 231]` exactly; both decode back to the exact prompts; the receipt
  rows name revisions, model identity, prompt hashes, tokenizer identity,
  command, expected vs observed, residuals; gates exit 0.
- **est_basis**: pilot (first-of-class: full composed qwen35 runtime in
  Fab; no close ledger class). est_work_tokens 8k–14k. ~10–15 min.
- **stop condition**: first divergent probe id or decoded character → the
  divergence receipt names it and routes the repair (campaign rule 5);
  probe rows are raw-prompt rows, never through the template.
- **depends_on**: LIB-02-U3-6.

### LIB-02-U4-1 — Capstone tokenizer-phase exempla

- **outcome**: `exempla/qwen36-35b-inference` runs the tokenizer phase of
  the capstone through public `gradus:*` imports (application-owned
  range-source adapter, the `gguf-inspect` pattern), encoding both probes
  and printing the pinned probe rows + decoded text.
- **exact write scope**: `exempla/qwen36-35b-inference/` (faber.toml,
  README.md, `src/main.fab`).
- **read_scope**: U3-7 composed runtime surface, the pinned oracle rows,
  the adapter pattern from `exempla/gguf-inspect`.
- **forbidden_scope**: any tensor materialization, model forward, GPU
  execution, or full-capstone code beyond the tokenizer phase; main-checkout
  edits; changes to `src/tokenizer.fab`.
- **first failing oracle**: the exempla run (fails today — no exempla
  exists).
- **closeout command**:
  ```bash
  cd /Users/ianzepp/work/faberlang/worktrees/hand-N/gradus
  ./scripta/check-source
  env FABER_LIBRARY_HOME=<lane> FABER_BIN=<lane faber> ./scripta/check-compile
  env FABER_LIBRARY_HOME=<lane> FABER_BIN=<lane faber> \
    faber run --target fmir exempla/qwen36-35b-inference
  git diff --check -- exempla/qwen36-35b-inference
  ```
  Green closeout once.
- **expected observed result**: one Faber package command encodes both
  probes through the public Gradus tokenizer surface and prints the pinned
  id lists + decoded text (PASS rows for both probes and both decoded
  round-trips); gates exit 0.
- **est_basis**: pilot (first-of-class: capstone tokenizer-phase package;
  gguf-inspect precedent). est_work_tokens 10k–16k. ~10–15 min.
- **stop condition**: a printed row diverges from the pinned oracle →
  divergence receipt naming the first divergent id/character; the exempla
  never hard-codes probe ids.
- **depends_on**: LIB-02-U3-7.

### LIB-02-U4-2 — Library docs agree

- **outcome**: `docs/module-map.md`, `docs/api-reference.md`,
  `docs/diagnostics.md`, and `docs/regression-corpus.md` describe the
  tokenizer runtime surface (U3-1..U3-7) and the capstone tokenizer phase,
  and agree with the observed result.
- **exact write scope**: `docs/module-map.md`, `docs/api-reference.md`,
  `docs/diagnostics.md`, `docs/regression-corpus.md`.
- **read_scope**: U3-7 / U4-1 surfaces and receipts, the delivery oracle
  rows.
- **forbidden_scope**: source/tokenizer edits, campaign/factory docs,
  main-checkout edits.
- **first failing oracle**: a docs-consistency check asserting the
  tokenizer runtime surface (Tokenizer runtime, encode/decode, EOG,
  special policy, chat render) is named in module-map/api-reference —
  fails today (docs describe only the identity contract).
- **closeout command**: `./scripta/check-source`; `git diff --check -- <write
  scope>`. Green closeout once.
- **expected observed result**: the four docs name the runtime surface and
  the probe rows and agree with the compiled surface; check-source exit 0.
- **est_basis**: pilot (first-of-class: tokenizer runtime doc surface; no
  close ledger class). est_work_tokens 6k–10k. ~10 min.
- **stop condition**: a doc claim cannot be verified against the compiled
  surface → correct the doc, not the code.
- **depends_on**: LIB-02-U4-1.

### LIB-02-U4-3 — Campaign docs + delivery receipt

- **outcome**: the support-matrix row, the GGUF-A2 status in
  `pml5-general-gguf-delivery.md`, and this delivery's receipt section all
  record the observed result with the campaign-mandated fields.
- **exact write scope**: `docs/factory/production-ml-library/pml0-support-matrix.md`,
  `docs/factory/production-ml-library/pml5-general-gguf-delivery.md`
  (GGUF-A2 status), this delivery's receipt section.
- **read_scope**: U4-1 run output, the pinned oracle rows.
- **forbidden_scope**: library source, library docs (U4-2 scope),
  main-checkout edits.
- **first failing oracle**: the receipt section is empty and the GGUF-A2
  status row still reads "not yet executed" — fails today.
- **closeout command**: `git diff --check -- <write scope>`; verify the
  receipt names revisions, model identity, prompt hashes, tokenizer
  identity, command, expected vs observed rows, and residuals. Green
  closeout once.
- **expected observed result**: support matrix and GGUF-A2 status report
  the executed tokenizer phase; the receipt records the exact command,
  working directory, revisions, model identity (filename/bytes/SHA-256),
  tokenizer identity, prompt hashes, and expected vs observed probe rows.
- **est_basis**: pilot (first-of-class: GGUF-A2 campaign receipt; closeout
  ledger precedent from PML2). est_work_tokens 6k–10k. ~10 min.
- **stop condition**: a required receipt field has no observed evidence →
  record it as a residual and escalate; never invent values.
- **depends_on**: LIB-02-U4-1.

## Checkpoints And Gates

1. U1 green before U2 starts (array accessors are the U2 input contract).
2. U2 green (word-level oracle) before U3-1 starts (U3 composes U2).
3. U3-7 green = **LIB-02 completion oracle satisfied** (both Unicode
   probes through the fully composed runtime). This is the micro-unit that
   advances milestone Q1's tokenizer input. Each of U3-1..U3-6 gates the
   next in sequence (U3-1 → U3-2 → … → U3-7).
4. U4-1 green = capstone tokenizer-phase run proven; then U4-2 (library
   docs) and U4-3 (campaign docs + receipt) close in parallel.
5. LIB-01 (A1c) must be committed before U2–U4 dispatch; U1 binds only
   schema-2 `gguf_manifest` surfaces and may be dispatched when the Mind
   serializes the shared model surface. If the Mind dispatches U1 before
   A1c lands, the task body must say so and the manifest surface must not
   change under it.

## Dispatch-Ready Micro-Unit List (READY evidence)

| Unit | Gate (first failing oracle) | Closeout |
| --- | --- | --- |
| LIB-02-U3-1 | category classification proba fails | check-source + check-compile + git diff --check |
| LIB-02-U3-2 | word-boundary/digit/newline rows fail | check-source + check-compile + git diff --check |
| LIB-02-U3-3 | punct/emoji/contraction rows fail | check-source + check-compile + git diff --check |
| LIB-02-U3-4 | special-token rows fail | check-source + check-compile + git diff --check |
| LIB-02-U3-5 | BOS-free rows + EOG proba fail | check-source + check-compile + git diff --check |
| LIB-02-U3-6 | rendered-turn rows fail | check-source + check-compile + git diff --check |
| LIB-02-U3-7 | Probe A/B composed ids fail | check-source + check-compile + git diff --check |
| LIB-02-U4-1 | `faber run exempla/qwen36-35b-inference` fails (no exempla) | gates + fmir run |
| LIB-02-U4-2 | docs-consistency check fails | check-source + git diff --check |
| LIB-02-U4-3 | receipt empty / GGUF-A2 status stale | git diff --check + receipt field check |

Every micro-unit carries the eight campaign-rule-2 fields (outcome, exact
write scope, first failing oracle, closeout command, expected observed
result, est_basis, stop condition, depends_on). U3-1..U3-7 are serial on
`src/tokenizer.fab`; U4-2 and U4-3 are disjoint from U4-1 and each other.

## Validation Summary

- Executed proof per unit is exactly the unit's `closeout command` (Rule 6:
  once at closeout, no post-done thrash).
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
- **Sequencing does not narrow scope**: the serial U1→U3-7→U4-3 order and
  the word-level-first boundary only stage the same admitted work; the two
  Unicode probes, artifact-backed metadata consumption, llama.cpp ids/decode
  oracle, and no-hard-coded-fallback rule all survive to the completion row.

## Open Questions For Mind

1. **Pre-tokenizer expressiveness (named risk).** Fab has no regex engine
   and no Unicode general-category tables found in this lowering. Realizing
   the qwen35 regex as a deterministic scalar scanner is the default; if a
   bounded scan over the probe-exercised classes is not expressible, the
   Hand files a **need** — the unit must not degrade to per-probe id pins.
   The re-split isolates this risk in U3-1 (category tables + predicates)
   so it is answered before any splitting logic lands. Recommend the
   bounded-category-scanner default; escalate only on an actual language
   gap, not on size.
2. **Dispatch timing vs LIB-01.** U1 binds only schema-2 manifest surfaces;
   U2–U4 must follow the committed A1c clean break. Mind decides whether U1
   dispatches before A1c lands (serialization on `gguf_manifest.fab`) or
   with the rest.
3. **Token id list form for chat template.** Now pinned: the probes are
   raw-prompt rows (U3-7 encodes them directly), and the rendered
   user-turn path is proven separately by U3-6's rendered-turn rows, which
   show the exact Probe B ids embedded unchanged inside the rendered turn
   (`[248045, 846, 198, <Probe B ids>, 248046, 198]`).

## First Implementation Frontier

LIB-02-U3-1: land the Unicode-category tables + predicates proba in
`src/tokenizer.fab` / `src/tokenizer.proba`, then U3-2, U3-3, and the rest
of the serial U3 chain through U3-7. Dispatch as Hand tasks from the
admitted micro-unit graph above; the Mind files Hand tasks — this planner
files no Hand tasks.

## Delivery Receipt (LIB-02-U4-3)

**Status**: executed — the capstone tokenizer-phase run is green on the
target artifact; recorded 2026-08-14 by hand-3 (U4-3).

**Revisions**:

- U1 manifest tokenizer metadata accessors `c4d0750` (gradus main);
- U2 artifact-backed byte-level BPE core `f3cfa58` (gradus main);
- U3-1 Unicode-category tables + predicates `58786db` (factory/hand-16);
- U3-2 qwen35 word-splitting scanner (core families) `00f5540`
  (factory/hand-16);
- U3-3 qwen35 scanner edge families `e1b818f` (factory/hand-16);
- U3-4 artifact special-token policy `90b0522` (factory/hand-16);
- U3-5 artifact EOG + BOS-free policy `a2dcd8d` (factory/hand-16);
- U3-6 chat-template policy `cc92176` (factory/hand-16);
- U3-7 full two-probe composition + divergence receipts `82a2863`
  (factory/hand-16);
- U4-1 capstone tokenizer-phase exempla `4ceb1d3` (factory/hand-16);
- U4-3 campaign docs + delivery receipt (this document, factory/hand-3).
- U4-2 (library docs) is a parallel disjoint unit; when it lands, this
  section is extended by its commit (not required for this receipt).

**Model identity** (target artifact, operator-local):

| Fact | Value |
| --- | --- |
| Filename | `Qwen3.6-35B-A3B-UD-Q4_K_M.gguf` |
| Byte length | 22,663,387,424 |
| SHA-256 | `0b21525e972670ed59e1812e170b27c26355381f0656ecc4e25617ece7dac58b` |

The digest was re-derived out of band (`shasum -a 256`); the model bytes
remain outside this repository.

**Tokenizer identity** (from the parsed artifact):

- model `gpt2` (byte-level BPE); pre-tokenizer `qwen35`;
- vocab 248,320 tokens; 247,587 merges; special-token cache 33;
- BOS/EOS/PAD ids 248044 `<|endoftext|>` / 248046 `<|im_end|>` / 248055;
- `add_bos_token` false; EOG set {248044, 248046, 248063, 248064, 248065}.

**Prompt hashes**:

- Probe A `สวัสดีครับ ผมชื่ออเล็กซ์` —
  `e30101d62c4e484ae2544643398b2cd6f562ccd8cf76832c39034b19ebc56a35`;
- Probe B `你好，世界！今天是2026年8月13日 🎉` —
  `855d730303db213db698dad3378d682d6968f6c046e70e5c7c1b05bfb7923588`.

**Command** (exact, from the U4-1 exempla README; executed on the committed
hand-16 tree 2026-08-14):

```bash
cd /Users/ianzepp/work/faberlang/worktrees/hand-16/gradus
env FABER_LIBRARY_HOME=/Users/ianzepp/work/faberlang/worktrees/hand-16 \
  /Users/ianzepp/work/faberlang/worktrees/hand-16/radix/target/debug/faber run --target fmir exempla/qwen36-35b-inference -- \
  /Users/ianzepp/Ai/models/Qwen3.6-35B-A3B-UD-Q4_K_M.gguf \
  --sha256 0b21525e972670ed59e1812e170b27c26355381f0656ecc4e25617ece7dac58b \
  --oracle-offset 10991392 --receipt /tmp/qwen36-u4-1-receipt.txt
```

Working directory: `/Users/ianzepp/work/faberlang/worktrees/hand-16/gradus`
(lane root as `FABER_LIBRARY_HOME`; contains gradus and norma). Exit 0.

**Expected vs observed rows** (raw-prompt rows, never through the chat
template; oracle pinned `llama-tokenize` 10150 `dee2a846b`):

| Row | Expected | Observed | Result |
| --- | --- | --- | --- |
| Probe A encode | `[34469, 168607, 153295, 173922, 153380, 22216, 151752, 172769]` | identical | PASS |
| Probe B encode | `[109266, 3709, 96748, 6115, 113128, 17, 15, 17, 21, 95859, 23, 96212, 16, 18, 95971, 10838, 236, 231]` | identical | PASS |
| Probe A decode | exact prompt text | exact prompt text | PASS |
| Probe B decode | exact prompt text | exact prompt text | PASS |

Observed run (U4-1):

```text
PASS version=3 alignment=32 data=10991392 metadata=55 tensors=753 architecture=qwen35moe
PASS bytes=22663387424
RECORDED sha256=0b21525e972670ed59e1812e170b27c26355381f0656ecc4e25617ece7dac58b (content re-derived externally via shasum -a 256)
ADMISSION PASS
TOKENIZER vocab=248320 (artifact-backed runtime, public gradus:tokenizer surface)
PASS Probe A encode -> [34469, 168607, 153295, 173922, 153380, 22216, 151752, 172769]
PASS Probe B encode -> [109266, 3709, 96748, 6115, 113128, 17, 15, 17, 21, 95859, 23, 96212, 16, 18, 95971, 10838, 236, 231]
PASS Probe A decode -> สวัสดีครับ ผมชื่ออเล็กซ์
PASS Probe B decode -> 你好，世界！今天是2026年8月13日 🎉
TOKENIZER PHASE PASS
RECEIPT /tmp/qwen36-u4-1-receipt.txt
```

The run issued no read into the tensor data region (the application-owned
range seam rejects any request whose end exceeds the bounded table prefix).
Focused negatives (byte-length mismatch, short prefix, tensor-data read,
content-identity invalid, reserved/unknown flags, malformed
`--oracle-offset`) all exit nonzero with typed causes; a probe row diverging
from the pinned oracle prints a `DIVERGENCE` receipt naming the first
divergent id/character (not observed on the pinned artifact).

**Residuals**:

- The full tokenizer-phase execution runs under the FMIR stepper (~6 min on
  the real artifact); exact-id proba rows still run under the cargo-backed
  harness at test-lane/merge time.
- The import-seam migration (SEM006, radix `016c225c4`) is complete for the
  gradus sources consumed by this exempla; `./scripta/check-compile` is
  green on the committed tree.
- This receipt records the executed **tokenizer phase** only. It does not
  claim tensor materialization, model forward, logits, tokens beyond
  encode/decode, or any device execution — those rows remain mandatory
  (GGUF-A3+ / GGUF-M4+ / GGUF-M5 / GGUF-M6) with their frozen oracles.
- The rendered chat-template user-turn path is proven separately (U3-6);
  full vision/tool template branches are recorded, not executed.
- U4-3 closeout evidence is packet-state: `git diff --check` on the write
  scope plus the receipt-field check above; committed-tree green is verified
  at merge time.
