# SD0-U1 — pinned dense baseline oracle

Status: **frozen for SD0**.

This page names `generation.generate_dense_with_stop` as the dense baseline
oracle for speculative decoding. A candidate implementation is correct only
when it reproduces this route's generated token list for the same model,
prompt, generation configuration, seed, and stop policy. SD0 does not add a
candidate provider or speculative implementation.

The citations below are to live source in this checkout. They are deliberately
specific enough to reconstruct the route without treating an older plan or a
prose description as the implementation.

## Reproduction fixture

The existing executable SmolLM2 example is the concrete baseline fixture:

- Artifact: `/Users/ianzepp/ai/models/SmolLM2-360M-Instruct-Q4_K_M.gguf`.
- Artifact identity: SHA-256
  `2fa3f013dcdd7b99f9b237717fa0b12d75bbb89984cc1274be1471a465bac9c2`,
  `270590880` bytes, with `1787040` bytes of manifest/data-prefix input.
- Prompt token ids, in order:
  `[504, 2365, 6354, 16438, 27003, 690, 260, 23790, 2767]`.
- Dense architecture: `layers=32`, `heads=15`, `kv_heads=5`,
  `head_dim=64`, `hidden_dim=960`, `vocab=49152`, `tied=true`.
- RoPE: base `100000.0`, scale `1.0`, consecutive-pair policy.
- Dense engine: epsilon `0.00001`, attention scale `0.125`, `rope_dim=64`.
- KV structure: one dense layer set over layer indices `0..31`, F32 K/V,
  transposed V, GQA sharing, classic attention, 15 query heads, 8192 slots,
  context length 8192.
- Every run starts with a fresh set of empty cache layers.

The fixture values and golden constants are declared in
`exempla/generate-smollm2/src/main.fab:32-43`. The RoPE, architecture, KV
structure, empty-cache construction, generation config, and engine construction
are assembled at `exempla/generate-smollm2/src/main.fab:422-477`. The prompt
is passed to the dense route at `exempla/generate-smollm2/src/main.fab:481-487`
and the IgnoreEos run uses a separately fresh cache set at
`exempla/generate-smollm2/src/main.fab:528-552`.

For the EOG-stop capture, use:

```text
GenerationConfig(context=8192, max_prompt=1, max_tokens=3,
                 seed=1, temperature=0.0, top_k=0,
                 top_p=1.0, min_p=0.0, repetition_penalty=1.0)
StopPolicy = eog_stop()
```

For the IgnoreEos capture, keep every field the same except
`max_tokens=16` and use `ignore_eos()`. These are the exact constructions in
the executable example at `exempla/generate-smollm2/src/main.fab:470-477` and
`exempla/generate-smollm2/src/main.fab:535-552`.

The dense source resolver is the admitted model-weight callback. It supplies
`model.embed_tokens`, `model.norm`, and each layer's canonical weight family;
the example binds it as `_lookup` at the two route calls cited above. The
public route accepts that resolver, the engine, the fresh caches, and a fresh
cancellation value; no hidden model or RNG state is part of the oracle.

## Named route and execution order

`generate_dense_with_stop` is the named oracle. The default
`generate_dense` is only its EOG-stop shorthand: it delegates to the named
route with `eog_stop()` at `src/generation.fab:763-771`.

The route has this fixed order:

1. Observe cancellation, validate a non-empty prompt that fits the generation
   context, project the sampling config and seed, and observe cancellation
   again (`src/generation.fab:775-781`).
2. Run one batched dense prefill over the prompt. Capture the returned cache
   state and select the last prompt-row logits
   (`src/generation.fab:782-785`).
3. Start the cursor immediately after the prompt, with an empty generated-token
   list and an empty repetition-penalty history
   (`src/generation.fab:785-788`).
4. For each allowed generated token, observe cancellation, apply the selected
   stop-policy logit view, sample one token, append it to the output and
   history, advance the RNG and cursor, then either stop or run exactly one
   dense decode step (`src/generation.fab:789-809`).
5. Return only the generated token list, not the prompt
   (`src/generation.fab:810-811`).

### Dense prefill capture

`dense.prefill_cached` is a batched prefill. Its frozen coordinates are an
empty cache prefix, prompt query rows, and write range `[0, T)`; it returns
logits for **every** prompt row so the caller can select the final row without
rerunning the prompt (`src/model/dense.fab:562-568`). Its implementation builds
prompt positions `0..T-1`, runs every layer, and returns the logits plus the
updated cache layers (`src/model/dense.fab:571-647`).

The generation route calls this prefill once and stores its returned layers at
`src/generation.fab:782-784`. `_last_logits` requires a rank-2 tensor's width
to equal the vocabulary and reads row `rows - 1`
(`src/generation.fab:642-661`). Therefore the first sampled token is sampled
from the logits corresponding to the final prompt token. Prompt tokens are
context, not generated output.

### Logits/token alignment and one-token advance

Let the prompt length be `T`, and let generated tokens be `y[0], y[1], ...`.
The frozen alignment is:

- `y[0]` is sampled from the final row of the batched prompt prefill.
- If another token is needed, `decode_step(y[0], position=T)` produces the
  next logits; `y[1]` is sampled from its single returned row.
- In general, after `y[i]` is appended, the route calls one decode step with
  `y[i]` at `cursor.position - 1`, then selects that step's final logits row
  for `y[i+1]` (`src/generation.fab:797-804`).

The dense primitive's contract is explicitly one incremental token plus its
position and cache layers in, one logits row plus updated layers out;
`src/model/dense.fab:448-455` describes that contract and
`src/model/dense.fab:488-559` implements it. The route preserves the returned
cache state before the next iteration (`src/generation.fab:801-805`).

This is the `k=1` baseline behavior. There is no draft block and no multi-token
acceptance path in the oracle: each sampled token gets one corresponding
`decode_step` advance unless it is an emitted EOG token or the token budget has
just closed. A speculative implementation must compare its accepted stream to
this one-token-at-a-time stream, including the first divergence position.

### Prompt history and repetition penalty

The route initializes `history` as empty after prefill and appends only each
sampled token (`src/generation.fab:785-795`). It never copies `prompt_ids`
into that history. Consequently prompt tokens are excluded from the
repetition-penalty history; the first sample sees `history=[]`, and later
samples see exactly the generated prefix.

The sampling contract applies repetition penalty over the supplied history
before temperature, top-k, softmax, top-p, and min-p
(`src/sampling.fab:255-270`). The penalty itself scans the history and divides a
positive historical logit or multiplies a non-positive one
(`src/sampling.fab:401-420`). For this fixture the penalty is `1.0`, so the
numerical penalty is neutral, but the history boundary remains part of the
oracle contract.

### Seed to RNG projection

The `GenerationConfig.seed` field is the integer stored by the config carrier
(`src/generation.fab:200-220`). The generation mapping passes that exact value
to `train.construct_seed` (`src/generation.fab:348-358`), whose non-zero state
is the initial `Seed` (`src/train.fab:476-495`). The route creates that seed
before prefill and carries it explicitly through the loop
(`src/generation.fab:779-782`, `src/generation.fab:791-796`).

For non-greedy sampling, `sampling.sample` is a pure function of logits,
sampling config, history, and the explicit seed. Temperature `<= 0` is the
argmax path and leaves the seed unchanged; otherwise the draw advances the
seed (`src/sampling.fab:220-235`). The draw is `train.next_f32`, which applies
the xorshift64 step and maps the sign-masked state to `[0,1)`
(`src/train.fab:522-561`). Thus same model/prompt/config/stop/seed means the
same explicit RNG sequence and the same generated stream.

### StopPolicy and EOG boundary

The live tokenizer EOG set is exactly `{0, 2}`
(`src/tokenizer.fab:107-135`). `StopPolicy` has two public modes:
`Eog` and `IgnoreEos`; their factories and stop predicate are at
`src/generation.fab:512-560`.

- `eog_stop()` leaves logits unchanged. When the sampled token is EOG, the
  route appends that token and then sets `finished`, so the first EOG is
  emitted and is the final output token
  (`src/generation.fab:578-583`, `src/generation.fab:791-800`).
- `ignore_eos()` replaces every EOG logit with finite `-1000000000.0` rather
  than `-inf`, then samples from the masked logits. It does not set the EOG
  stop predicate, so the route continues until `max_tokens`
  (`src/generation.fab:562-583`, `src/generation.fab:797-809`).

The SmolLM2 EOG-stop golden is `[30, 2]`; the IgnoreEos golden is
`[30, 198, 198, 504, 808, 6330, 314, 253, 2232, 4814, 282, 1027, 28, 979,
260, 1796]`. Both are declared in
`exempla/generate-smollm2/src/main.fab:7-16,36-43`, and the example compares
the IgnoreEos stream against that exact list at
`exempla/generate-smollm2/src/main.fab:558-570`.

The first sampled token is shared (`30`). At the next sampling boundary the
EOG route emits `2` and stops, while IgnoreEos masks `2` and emits `198`; the
first policy divergence is therefore generated position **1**. The EOG token
is included in the EOG-stop output, and it is not included in the IgnoreEos
output because it is suppressed before sampling.

## Acceptance rule for SD0

Use a fresh cache set for each capture. Hold the model artifact, prompt ids,
all nine generation fields, stop policy, and seed fixed. Compare the complete
returned token lists, not decoded text and not only the first token.

The two required executable properties in `src/generation.proba` are:

1. same configuration plus same seed produces an identical stream on repeated
   captures; and
2. `eog_stop` and `IgnoreEos` agree through the shared prefix and diverge at
   the first EOG boundary, with EOG-stop emitting the EOG and IgnoreEos
   continuing to its token ceiling.

Any speculative route with `k=1` must reproduce the named dense baseline's
per-token logits/advance order and its complete token list before a larger
candidate block is admitted.
