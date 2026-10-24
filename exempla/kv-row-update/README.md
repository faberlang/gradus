# In-place KV row updates

This package updates two rows of one resident cache, then attempts a negative
and an out-of-capacity position. Those two calls are no-ops. The output is the
unchanged first row `[0, 1, 2, 3, 4]`, followed by rows `[100, ..., 104]` and
`[200, ..., 204]`.

Build the sibling Radix product and pass the absolute parent directory as
`--library-home`. From this repository, for example:

```sh
../radix/target/debug/faber run exempla/kv-row-update --library-home /path/to/parent --device reference
../radix/target/debug/faber run exempla/kv-row-update --library-home /path/to/parent --device metal --stats
../radix/target/debug/faber run exempla/kv-row-update --library-home /path/to/parent --device metal --partitions 3 --stats
```

`kv_write` reads the cache shape on the host before invoking `kv_write_row`.
The raw kernel is public so the device image can launch it; a direct call to
that kernel has the ordinary checked-index contract. Use `kv_write` for the
library's invalid-position no-op behavior. The caller supplies a separate row
tensor; writable aliases of the cache are not admitted as another argument.

## Verification, 2026-10-23

Tested the source in this change with the sibling Radix `7cb9627668` debug
product on the laptop (Apple M5 Max, macOS 26.5.2, Rust 1.99.1):

- `decode_step` and `decode_token` package tests: 20 passed on reference and
  20 passed on the CPU device with four workers. Cache assertions are exact
  f32 equality; the other numerical tests retain their existing comparisons.
- This example: exact expected output on reference, CPU, Metal, and Metal
  with three virtual partitions.
- Both Metal runs recorded exactly two kernel launches, proving that the
  invalid positions did not launch and the valid calls used the device.
- The three-partition run recorded two first-partition launches, with
  `writes-not-lane-local`: in-place mutation is implemented independently of
  the later partial-write split/transfer optimization.

This is a correctness and dispatch receipt, not a performance benchmark.
