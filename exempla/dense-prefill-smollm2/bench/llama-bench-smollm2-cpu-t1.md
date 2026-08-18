| model                          |       size |     params | backend    | threads |            test |                  t/s |
| ------------------------------ | ---------: | ---------: | ---------- | ------: | --------------: | -------------------: |
| llama 3B Q4_K - Medium         | 256.35 MiB |   361.82 M | BLAS,MTL   |       1 |           pp512 |        166.40 ± 0.15 |
| llama 3B Q4_K - Medium         | 256.35 MiB |   361.82 M | BLAS,MTL   |       1 |             pp9 |         84.04 ± 0.06 |
| llama 3B Q4_K - Medium         | 256.35 MiB |   361.82 M | BLAS,MTL   |       1 |           tg128 |         66.65 ± 0.07 |

build: dee2a846b (10150)
