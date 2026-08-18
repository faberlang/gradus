| model                          |       size |     params | backend    | threads |            test |                  t/s |
| ------------------------------ | ---------: | ---------: | ---------- | ------: | --------------: | -------------------: |
| qwen2 1B Q4_K - Medium         | 373.71 MiB |   494.03 M | BLAS,MTL   |       6 |           pp512 |   25378.95 ± 1360.75 |
| qwen2 1B Q4_K - Medium         | 373.71 MiB |   494.03 M | BLAS,MTL   |       6 |             pp9 |       722.98 ± 19.40 |
| qwen2 1B Q4_K - Medium         | 373.71 MiB |   494.03 M | BLAS,MTL   |       6 |           tg128 |       205.51 ± 18.82 |

build: dee2a846b (10150)
