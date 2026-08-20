# generate-route — G2 public generate surface (tiny decoder)

Compiled consumer of `gradus:generation.generate(config, ids, decoder)`.

The loop lives in the library: prefill → sampling → `decode_data`
feed-back, with EOG-stop `{0, 2}` and the reject-not-truncate cursor.
The decoder is an argument (M03: admitted model = generated model).
The KV-wired SmolLM2 path is `generate_dense` (`exempla/generate-smollm2`).

## Pins

Tiny decoder from `decode.proba` (V=3, D=4, context 3).

| Run | Expected |
| --- | --- |
| greedy prompt `[0]`, max_tokens 2 | `[0]` — EOG-stop; `0` is admitted EOG |
| greedy prompt `[1]`, max_tokens 1 | `[1]` — N-token ceiling; `1` is not EOG |

SmolLM2 first-token `30` / EOG-stop `[30, 2]` is the real-model oracle
in `exempla/generate-smollm2` (G1 unrestrained continuation was
`[30, 2, 198]`; token `2` is SmolLM2 EOS).
