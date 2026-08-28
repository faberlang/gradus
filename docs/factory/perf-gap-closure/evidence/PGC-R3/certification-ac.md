# PGC-R3 certified capture — AC power (baseline of record)

## Certification (two-class oracle)

- Capture: `parity-raw-ac/` — full stage (stage_number=4), breadth 2 × 3 paired runs,
  on-device Metal arms only, MIR runner excluded.
- Power: `pmset -g batt` → `Now drawing from 'AC Power'` (21%, charging) before the
  capture; every receipt row is `power_class: ac` (6/6).
- Certified counts: `metal-m5max-fixed1000` faber 1000/1000 ×3 natural completion,
  comparator 40/40 ×3 natural completion; `metal-m5max` 8/8 ×3 both arms, natural
  completion. Both blocks `status: comparable`.
- Reduced receipt: `parity-receipt-ac.json`.
- Baseline append (append-only, standing family untouched):
  `radix/scripta/parity-baselines/parity-baseline-20260828-r783e0b9-h848a24b-gb762163-cmpb10290-c8e03ce81.{json,md}`;
  receipt copy `baseline-candidate-ac.md` here.

## Pins (three-repo)

Radix `783e0b9`, hosts `848a24b`, gradus `b762163`, comparator llama-cli
`b10290-c8e03ce81`, GGUF SmolLM2-360M-Instruct-f32 (sha256 in receipt).
Same GGUF/statues/env as the standing GLP baseline of record.

Note: this certified capture runs on current main pins, which are ahead of the
battery candidate's pins (radix `c34b3976`, hosts `007ba2a`, gradus `b762163`);
the delta below therefore mixes power class and pin posture. Gradus pin is
unchanged between the two captures.

## Battery vs AC wall deltas (medians, t/s; ratio = llama/gradus)

| test | phase | battery gradus | AC gradus | battery llama | AC llama | battery ratio | AC ratio |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| metal-m5max | prefill | 234.668 | 540.614 | 870.827 | 1303.403 | 3.711 | 2.411 |
| metal-m5max | decode | 18.913 | 36.405 | 121.267 | 189.934 | 6.412 | 5.217 |
| metal-m5max-fixed1000 | prefill | 417.275 | 447.238 | 1772.526 | 3220.036 | 4.248 | 7.200 |
| metal-m5max-fixed1000 | decode | 14.480 | 16.128 | 248.849 | 240.067 | 17.186 | 14.885 |

Wall is L1-gated secondary to the census (`census.md`, unchanged by this
capture); the numbers above are lawful now that power_class=ac. Short-arm gradus
throughput roughly doubles on AC (prefill 2.30×, decode 1.93×); fixed1000 gradus
moves modestly (prefill +7.2%, decode +11.4%). The comparator's fixed1000
prefill also accelerated on AC (1772→3220 t/s), so the fixed1000 prefill ratio
rose despite gradus improving.
