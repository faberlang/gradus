# LIB-02 U3-6 Oracle — chat-template policy (metadata + minimal user-turn)

**Unit**: LIB-02-U3-6 (chat-template policy — GGUF-A2 tokenizer runtime).
**Repo**: gradus. **Date**: 2026-08-14. **Owner**: hand-16 (implement),
mind@ (admission).

This document pins the chat-template oracle for the artifact-backed
tokenizer runtime in `gradus:tokenizer` (`src/tokenizer.fab`). The runtime
loads `tokenizer.chat_template` from the artifact metadata and applies the
**minimal Qwen3-ChatML user-turn render** `<|im_start|>user\n{content}
<|im_end|>\n` — the executed subset of the artifact's Jinja template.
Full vision/tool-calling template branches are recorded, not executed
(delivery scope matrix; the delivery forbids a universal Jinja/template
engine).

## Pinned rendered-turn rows (oracle 10150 `dee2a846b`, target artifact)

The rows below are the delivery's chat-template differential table
(`pml5-lib02-tokenizer-delivery.md`, "Chat-template rows (U3-6)"). R1/R1b
render Probe B's user turn; R2 is the assistant turn prefix. All rows
deterministic (re-ran twice, 2026-08-14).

| Prompt | Pinned ids | sha256 |
| --- | --- | --- |
| rendered Probe B user turn (R1, parse-special on) | `[248045, 846, 198, 109266, 3709, 96748, 6115, 113128, 17, 15, 17, 21, 95859, 23, 96212, 16, 18, 95971, 10838, 236, 231, 248046, 198]` | `595812a1e88de2260a478a78ea25683025e1627c4f88df639129526b52f08ceb` |
| same, `--no-parse-special` (R1b, literal) | `[27, 91, 316, 4747, 91, 29, 846, 198, 109266, 3709, 96748, 6115, 113128, 17, 15, 17, 21, 95859, 23, 96212, 16, 18, 95971, 10838, 236, 231, 27, 91, 316, 6018, 91, 29, 198]` | same prompt hash |
| `<|im_start|>assistant\n` (R2) | `[248045, 74455, 198]` | `fb3832354a86f4328bdfbf33691473fc7c08824ff6bd056f4b90c95d7fe9eaa4` |

`[248045]` is `<|im_start|>` (special), `[846]` is `user`, `[198]` is `\n`
(display `Ċ`), `[248046]` is `<|im_end|>`, `[74455]` is `assistant`. The
rendered user-turn row proves the ChatML path composes **without changing
the pinned Probe B ids**: the 18-ids segment (109266..231) embeds verbatim
between the wrapper tokens.

## Public surface pinned by this unit

- `chat_template(Tokenizer t) → string` — the artifact's
  `tokenizer.chat_template` string; empty when the artifact declares none.
- `render_user_turn(Tokenizer t, string content) → string ⇥
  TokenizerError` — the minimal Qwen3-ChatML user-turn render; fails closed
  with `BadArtifact` ("artifact declares no chat template") when the
  artifact declares no template (no hard-coded fallback).

The rendered text encodes through the existing U3-4 paths:
`encode_prompt_special` (parse-special on, R1) and `encode_prompt`
(parse-special off, R1b literal).

## Fail-closed matrix (per U3-6 done_when)

`gradus/src/tokenizer.proba` proves, at compile level: the template loads
exactly; the render applies the pinned shape; R1/R1b/R2 encode to their
exact pinned id lists on the structural fixture corpus; the rendered turn
composes without changing the pinned Probe B ids (sublist equality); and an
artifact without a chat template fails the render closed while reading as
an empty template.

## Fixture corpus

Structural model (same approach as U2/U3-2..U3-5): the pinned tokens sit at
their pinned ids with the exact display strings, `token_type` marks exactly
the two ChatML specials CONTROL, the merge table carries exactly the ranked
merge pairs the real BPE applies to each rendered word, and
`tokenizer.chat_template` stores the minimal ChatML shape. R2 lives on a
separate small fixture (its `assistant` merge chain would collide with the
user-turn corpus's `s t` entry). No artifact bytes are committed.

## Regeneration

A re-pin is an operator decision (CAMPAIGN stop conditions) and MUST update
the delivery rows, this document, `src/tokenizer.fab` (the pinned shape),
and `src/tokenizer.proba` (the pinned constants) together.
