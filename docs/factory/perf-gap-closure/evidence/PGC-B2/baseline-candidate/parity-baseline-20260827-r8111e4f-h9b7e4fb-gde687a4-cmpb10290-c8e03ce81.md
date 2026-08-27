# parity-receipt-v1

source: `/Users/ianzepp/work/faberlang/worktrees/pgc-b2/gradus/docs/factory/perf-gap-closure/evidence/PGC-B2/parity-raw`
stage: **full** (stage_number=4)
protocol: `{"aggregation": "median across paired runs", "baseline_grade": true, "breadth": 2, "cap_rule": "hard cap per arm; circuit breaker only; never a metric or token target", "execution_rule": "on-device Metal arms only; MIR runner excluded", "paired_runs": 3, "schema": "parity-stage-protocol-v1", "stage": "full", "stage_number": 4, "target_ids": ["metal-m5max", "metal-m5max-fixed1000"]}`

## test=metal-m5max power_class=ac

status: **comparable**

| phase | llama t/s | gradus t/s | llama:gradus |
| --- | ---: | ---: | ---: |
| prefill | 3082.191781 | 570.053205 | 5.406849 |
| decode | 241.400121 | 17.874978 | 13.504918 |

## test=metal-m5max-fixed1000 power_class=ac

status: **comparable**

| phase | llama t/s | gradus t/s | llama:gradus |
| --- | ---: | ---: | ---: |
| prefill | 3152.364273 | 559.919123 | 5.630035 |
| decode | 221.336875 | 6.962120 | 31.791591 |
