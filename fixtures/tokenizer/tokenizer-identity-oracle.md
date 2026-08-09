# PML2-U4 Oracle — pinned tokenizer identity fixture (SmolLM2-360M row)

**Unit**: PML2-U4 (tokenizer identity — Lane 1). **Repo**: gradus.
**Date**: 2026-08-09. **Owner**: hand-5 (implement), mind@ (admission).

This document pins the tokenizer identity oracle for the one admitted row
(SmolLM2-360M-Instruct Q4_K_M). The module `gradus:tokenizer`
(`src/tokenizer.fab`) carries the versioned contract
(`tokenizer-identity-schema-1.0.0`): byte-level BPE per row, BOS/EOS/
special-token behavior, and the pinned llama.cpp id lists that any admitted
tokenizer must reproduce exactly. Tokenizer RUNTIME (encode text → ids) is
owned by faber-runtime (GI1-3); this contract pins the EXPECTED ids and
fails closed when a tokenizer's ids diverge (a different tokenizer).

## Row identity (pinned facts, read-only from gi1-closeout.md / GI1-3)

| Fact | Pinned value | Source |
| --- | --- | --- |
| Tokenizer model | `gpt2` (byte-level BPE / BBPE) | gi0-model-contract §4 (`tokenizer.ggml.model`) |
| Pre-tokenizer | `smollm` | gi0-model-contract §4 (`tokenizer.ggml.pre`) |
| Vocab size | 49152 | GI1-3 (`EXPECTED_VOCAB_SIZE`) |
| Merge count | 48900 | GI1-3 (`EXPECTED_MERGES`) |
| BOS id / EOS id / PAD id / UNK id | 1 / 2 / 2 / 0 | GI1-3 |
| EOG set | `{0, 2}` | GI1-3 (`eog_tokens`) |
| Special tokens | 17 control specials, ids 0..=16 | GI1-3 |
| BOS behavior | BOS-free (`add_bos_token=false`) | gi0-model-contract §4 |
| Space behavior | space-prefix-free (`add_space_prefix=false`) | gi0-model-contract §4 |
| Vocab digest claim | 64-hex (value host-computed at admission) | pinned metadata; no crypto in-language |

## Pinned probe id lists (P1–P11)

Cited read-only from `radix/docs/factory/gpu-inference-gguf/evidence/
contract-tokenize-probes.txt` (llama-tokenize 10150 `dee2a846b`, vocab-only,
pinned row). The module embeds each comma-separated id list verbatim.

| Probe | Prompt | Pinned ids | Count |
| --- | --- | --- | --- |
| P1 | `Hello world` | `19556,905` | 2 |
| P2 | `Hello world` (--no-bos) | `19556,905` | 2 |
| P3 | token count | — (== P1 length) | 2 |
| P4 | `` (empty) | — (empty) | 0 |
| P5 | `<|im_start|>` (specials on) | `1` | 1 |
| P6 | `<|im_start|>` (--no-parse-special) | `44,108,306,79,3738,108,46` | 7 |
| P7 | `<|im_end|>` | `2` | 1 |
| P8 | `<|endoftext|>` | `0` | 1 |
| P9 | chat-template prefix | (32 ids, embedded verbatim) | 32 |
| P10 | `The quick brown fox jumps over the lazy dog` | `504,2365,6354,16438,27003,690,260,23790,2767` | 9 |
| P11 | `  leading spaces` | `216,2899,5600` | 3 |

## Pinned workload id lists (gi0-workloads.md §3)

| Workload | Pinned count | Head / tail |
| --- | --- | --- |
| correctness | 9 | `504,2365,6354,16438,27003,690,260,23790,2767` |
| short | 9 | `19161,253,421,30614,563,260,5065,30,198` |
| normal | 202 | head `504`, tail `30` |
| context | 2175 | head `54`, tail `198` |

The 24-case differential vs `llama-tokenize` 10150 (whitespace/contraction/
digit/non-ASCII edges) is cited read-only from gi1-closeout.md §1 bullet 1 —
the runtime owner (faber-runtime) reproduces it; this contract pins the
expected ids (P1–P11 + workloads) and the divergence rule.

## Fail-closed matrix (per PML2-U4 done_when)

`gradus/src/tokenizer.proba` proves, at compile level: every pinned probe
parses to its exact id list; workload counts are 9/9/202/2175; exact probe
match admits while any divergence (changed id, reordered, length-mismatched)
fails closed with the typed `ProbeDivergens`; the versioned identity record
admits the pinned row and rejects unknown schema / un-admitted kind / un-
admitted pre-tokenizer / malformed vocab digest / malformed EOG / non-BOS-
free / space-prefixed rows; the KV identity key component (MD-A9) is
deterministic and identity-sensitive; the wire form round-trips and rejects
unknown schema / marker / kind / digest.

## Regeneration

The fixture is embedded as constants in `src/tokenizer.fab`; a re-pin is an
operator decision (CAMPAIGN stop conditions) and MUST update the module
constants, this document, and the proba assertions together.
