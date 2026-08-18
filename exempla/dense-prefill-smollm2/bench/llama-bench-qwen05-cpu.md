| model                          |       size |     params | backend    | threads |            test |                  t/s |
| ------------------------------ | ---------: | ---------: | ---------- | ------: | --------------: | -------------------: |
| qwen2 1B Q4_K - Medium         | 373.71 MiB |   494.03 M | BLAS,MTL   |       6 |           pp512 |        462.58 ± 8.26 |
| qwen2 1B Q4_K - Medium         | 373.71 MiB |   494.03 M | BLAS,MTL   |       6 |             pp9 |       281.83 ± 16.82 |
| qwen2 1B Q4_K - Medium         | 373.71 MiB |   494.03 M | BLAS,MTL   |       6 |           tg128 |        141.35 ± 0.61 |

build: dee2a846b (10150)
