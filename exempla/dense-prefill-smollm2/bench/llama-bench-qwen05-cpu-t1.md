| model                          |       size |     params | backend    | threads |            test |                  t/s |
| ------------------------------ | ---------: | ---------: | ---------- | ------: | --------------: | -------------------: |
| qwen2 1B Q4_K - Medium         | 373.71 MiB |   494.03 M | BLAS,MTL   |       1 |           pp512 |        179.35 ± 0.25 |
| qwen2 1B Q4_K - Medium         | 373.71 MiB |   494.03 M | BLAS,MTL   |       1 |             pp9 |         75.02 ± 0.07 |
| qwen2 1B Q4_K - Medium         | 373.71 MiB |   494.03 M | BLAS,MTL   |       1 |           tg128 |         55.10 ± 0.06 |

build: dee2a846b (10150)
