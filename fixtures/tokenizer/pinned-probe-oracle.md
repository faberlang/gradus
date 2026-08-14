# LIB-02 U3-7 Oracle — full two-probe composition + divergence receipts

**Unit**: LIB-02-U3-7 (full two-probe composition + divergence receipts —
GGUF-A2 tokenizer runtime). **Repo**: gradus. **Date**: 2026-08-14.
**Owner**: hand-16 (implement), mind@ (admission).

This document pins the LIB-02 **completion oracle**: the complete composed
runtime (qwen35 scanner + BPE core + special policy + EOG/BOS + chat policy,
LIB-02-U3-1..U3-6) encodes **Probe A** and **Probe B** to the exact pinned id
lists and decodes them back to the exact prompts. The probe rows are
raw-prompt rows, never through the chat template (the rendered-turn path is
proven separately by the U3-6 rows R1/R1b/R2).

## Receipt rows (divergence-receipt form)

| Row | Value |
| --- | --- |
| Revision | U3-7 closeout (stack on cc92176 U3-6); delivery `pml5-lib02-tokenizer-delivery.md` re-split 0eca870 |
| Model identity | Qwen3.6-35B-A3B (`general.architecture=qwen35moe`, `tokenizer.ggml.model=gpt2`, `tokenizer.ggml.pre=qwen35`) |
| Tokenizer identity | `gradus:tokenizer` GGUF-A2 artifact-backed runtime (`fabricare` + `encoda_promptum` / `encoda_promptum_specialia` + `decoda`), full composed surface (specials cache, EOG set, BOS-free, chat template) |
| Oracle | `llama-tokenize` 10150 (`dee2a846b`), target artifact `Qwen3.6-35B-A3B-UD-Q4_K_M.gguf`, rows deterministic (re-ran identical) |
| Command | `./scripta/check-source`; `./scripta/check-compile` (FABER_LIBRARY_HOME + FABER_BIN from the hand packet); `git diff --check`; probe rows bound in `gradus/src/tokenizer.proba` (cargo-backed harness) + throwaway fmir mechanics consumer |
| Expected vs observed | Probe A `[34469, 168607, 153295, 173922, 153380, 22216, 151752, 172769]`; Probe B `[109266, 3709, 96748, 6115, 113128, 17, 15, 17, 21, 95859, 23, 96212, 16, 18, 95971, 10838, 236, 231]` — identical |
| Residuals | Exact-id execution runs under the cargo-backed harness at test-lane/merge time (the 248047-entry pinned fixture is too slow for the in-packet MIR stepper, same as U3-4..U3-6); the in-packet consumer proves the composed mechanics on compact fixtures |

## Pinned probe rows (oracle 10150 `dee2a846b`, target artifact)

Probe rows are the LIB-02 completion oracle (Normalized Spec rule 2): encode
must produce the exact pinned id lists and decode must reproduce the exact
prompt text. Both rows were executed on the target artifact 2026-08-13 and
re-ran identical 2026-08-14.

### Probe A — Thai

```
prompt: สวัสดีครับ ผมชื่ออเล็กซ์
ids:    [34469, 168607, 153295, 173922, 153380, 22216, 151752, 172769]
count:  8
sha256: e30101d62c4e484ae2544643398b2cd6f562ccd8cf76832c39034b19ebc56a35
decoded text must round-trip to the exact prompt.
```

Oracle word split: `สวัสดีครับ` → `[34469, 168607, 153295]` (ส / วัสดี /
ครับ), ` ผมชื่ออเล็กซ์` → `[173922, 153380, 22216, 151752, 172769]` (Ġผม /
ชื่อ / อ / เล็ก / ซ์) — the leading space attaches to the following word
(U3-2 scanner rule).

### Probe B — CJK + emoji + digits

```
prompt: 你好，世界！今天是2026年8月13日 🎉
ids:    [109266, 3709, 96748, 6115, 113128, 17, 15, 17, 21, 95859, 23,
         96212, 16, 18, 95971, 10838, 236, 231]
count:  18
sha256: 855d730303db213db698dad3378d682d6968f6c046e70e5c7c1b05bfb7923588
decoded text must round-trip to the exact prompt.
```

Oracle word split: `你好` → `[109266]`, `，` → `[3709]`, `世界` → `[96748]`,
`！` → `[6115]`, `今天是` → `[113128]`, `2026` → `[17, 15, 17, 21]` (digits
split per char), `年` → `[95859]`, `8` → `[23]`, `月` → `[96212]`, `13` →
`[16, 18]`, `日` → `[95971]`, ` 🎉` → `[10838, 236, 231]` (ĠðŁ / İ / ī).

`[248045]` `<|im_start|>` and `[248046]` `<|im_end|>` are the ChatML specials
(U3-4); the probe rows are raw rows and never embed them (the U3-6 R1 row
wraps the Probe B ids between `[248045, 846, 198, …]` and `[248046, 198]`).

## Public surface proven by this unit

- `encoda_promptum(t, textum) → lista<numerus> ⇥ TokenizerError` — full-prompt
  encode, parse-special off (scanner + BPE core).
- `encoda_promptum_specialia(t, textum) → lista<numerus> ⇥ TokenizerError` —
  full-prompt encode, parse-special on (special split before the scanner;
  identical to the above when the prompt has no specials).
- `decoda(t, ids) → textus ⇥ TokenizerError` — id list → exact prompt text
  (byte-level BPE round-trip).
- `scanna_verba(textum) → lista<textus> ⇥ TokenizerError` — the qwen35
  pre-tokenizer word split (U3-2/U3-3).
- Composed runtime state: `eog_artificii` (EOG set, U3-5), `add_bos`
  (BOS-free), `chat_template` (U3-6).

## Fixture corpus

Probe A runs on its own structural fixture `_corpus_proba_a` (same approach
as U2/U3-2..U3-6): the pinned tokens sit at their pinned ids (max id 248046,
248047 entries — eos 248046 in range) with the exact display strings, the
merge table carries exactly the 38 ranked merge pairs the real BPE applies
to the two Probe A words (re-derived against the oracle tool on the target
artifact), `token_type` is NORMAL everywhere, and the artifact policy
metadata (eos 248046, add_bos falsum, minimal ChatML template) is present so
the probe runtime is the complete composed surface. Probe B reuses the U3-6
chat fixture `_corpus_chat`, whose words already sit at the pinned ids. No
artifact bytes are committed.

## Divergence receipts (campaign rule 5)

The stop condition is the first divergent probe id or decoded character: a
printed row diverging from the pinned oracle produces a divergence receipt
naming the first divergent id/character and routes the repair. The probe rows
never hard-code probe ids — the pinned id lists are bound as proba constants
and the fixture corpus is derived from the oracle tool.

## Regeneration

A re-pin is an operator decision (CAMPAIGN stop conditions) and MUST update
the delivery rows, this document, `src/tokenizer.proba` (the pinned
constants + fixture), and `src/tokenizer.fab` (if the runtime surface
changes) together.
