| model                          |       size |     params | backend    | threads |            test |                  t/s |
| ------------------------------ | ---------: | ---------: | ---------- | ------: | --------------: | -------------------: |
| llama 3B Q4_K - Medium         | 256.35 MiB |   361.82 M | BLAS,MTL   |       6 |           pp512 |   27180.23 ± 1190.01 |
| llama 3B Q4_K - Medium         | 256.35 MiB |   361.82 M | BLAS,MTL   |       6 |             pp9 |       790.29 ± 19.07 |
| llama 3B Q4_K - Medium         | 256.35 MiB |   361.82 M | BLAS,MTL   |       6 |           tg128 |       136.40 ± 17.47 |

build: dee2a846b (10150)
