# Internal surfaces

Contributor and development paths. Not the public Gradus product.
`cista.toml` installs `src/` only.

| Path | Role |
| --- | --- |
| `scripta/` | source-library checks and fixture generators |
| `fixtures/` | test corpus and oracle generators |
| `exempla/dense-prefill-smollm2/bench/` | n=1 measurement receipt, not a product-speed claim |
| `exempla/dense-prefill-smollm2/gi2-*.txt` | GI2 golden dumps from bring-up |
| `exempla/dense-prefill-qwen2/gi2-*.txt` | GI2 golden dumps from bring-up |

Markers sit next to the receipts (`bench/RECEIPT.md`, `NONPRODUCT.md`
in each dump directory). Root agent/tool files are a separate
disposition.
