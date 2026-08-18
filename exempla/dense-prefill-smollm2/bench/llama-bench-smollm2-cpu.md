| model                          |       size |     params | backend    | threads |            test |                  t/s |
| ------------------------------ | ---------: | ---------: | ---------- | ------: | --------------: | -------------------: |
| llama 3B Q4_K - Medium         | 256.35 MiB |   361.82 M | BLAS,MTL   |       6 |           pp512 |       406.97 ± 17.68 |
| llama 3B Q4_K - Medium         | 256.35 MiB |   361.82 M | BLAS,MTL   |       6 |             pp9 |       306.06 ± 13.68 |
| llama 3B Q4_K - Medium         | 256.35 MiB |   361.82 M | BLAS,MTL   |       6 |           tg128 |        159.45 ± 6.16 |

build: dee2a846b (10150)
