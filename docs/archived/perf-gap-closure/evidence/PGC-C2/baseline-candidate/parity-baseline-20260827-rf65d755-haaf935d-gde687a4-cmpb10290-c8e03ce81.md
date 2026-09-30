# parity-receipt-v1

source: `/Users/ianzepp/work/faberlang/worktrees/pgc-c2/gradus/docs/factory/perf-gap-closure/evidence/PGC-C2/parity-raw`
stage: **full** (stage_number=4)
protocol: `{"aggregation": "median across paired runs", "baseline_grade": true, "breadth": 2, "cap_rule": "hard cap per arm; circuit breaker only; never a metric or token target", "execution_rule": "on-device Metal arms only; MIR runner excluded", "paired_runs": 3, "schema": "parity-stage-protocol-v1", "stage": "full", "stage_number": 4, "target_ids": ["metal-m5max", "metal-m5max-fixed1000"]}`

## test=metal-m5max power_class=ac

status: **comparable**

| phase | llama t/s | gradus t/s | llama:gradus |
| --- | ---: | ---: | ---: |
| prefill | 1284.796574 | 554.289586 | 2.317916 |
| decode | 205.338809 | 31.657466 | 6.486268 |

## test=metal-m5max-fixed1000 power_class=ac

status: **comparable**

| phase | llama t/s | gradus t/s | llama:gradus |
| --- | ---: | ---: | ---: |
| prefill | 1926.163724 | 535.109103 | 3.599572 |
| decode | 224.794875 | 15.938926 | 14.103515 |
