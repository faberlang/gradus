# In-place KV block writes

`kv_write_block(cache, block, start)` writes the block's in-capacity rows in one
kernel launch. The example primes the cache as a read-only resident input before
writing it, and exercises block sizes 1, 7 and the full 9-row capacity. Output is
the final full-cache block; no per-write cache-sized output buffer is introduced.

Run with a library home that contains the repository as `gradus`:

```sh
faber run exempla/kv-row-update --library-home "$LIBHOME" --device reference
faber run exempla/kv-row-update --library-home "$LIBHOME" --device metal --stats
```

## Metal receipt

Measured with `faber 1.18.1` on Apple M1 (`--device metal --stats`). The device
stats counters read were `runtime.launch_count`, `uploaded_bytes`,
`downloaded_bytes`, and `peak_allocated_bytes`:

- 1-row write: 1 launch; 20 logical f32 bytes written (1 × 5 × 4).
- 7-row write: 1 launch; 140 logical f32 bytes written (7 × 5 × 4).
- 9-row/full-capacity write: 1 launch; 180 logical f32 bytes written (9 × 5 × 4).
- For the complete exemplar (including one cache-prime launch): 4 launches,
  524 uploaded bytes, 184 downloaded bytes, 1,049,100 peak allocated bytes.

The individual block sizes are separate kernel entries, each called once; launch
count is independent of rows within a block. The written element count scales as
rows × K. The 184 downloaded bytes are the one final 180-byte cache observation
and the 4-byte prime sink; the three writes do not allocate or download a
full-capacity output per call. Peak allocated bytes include Metal's runtime pool
and are not a cache-output allocation measurement.

The single-row `kv_write` remains available and retains its existing invalid
position no-op behavior. For block writes, out-of-range rows are skipped
individually: negative starts write nothing; a block running past capacity writes
only the in-range prefix.

The block kernel stores directly into the cache, has no writable row view or
cache alias argument, and keeps all bounds guards in the kernel rather than
reading the cache shape on the host.

The package-level source test currently cannot complete: besides warnings, the
existing test file's `argmax_chunks` references resolve to an absent public
member in `decode_step.fab`. The block-write assertions are included in that
file, but the required whole-file test command exits during package analysis.

`./scripta/check-source` and `LIBRARY_HOME="$LIBHOME" FABER_BIN="$FABER"
./scripta/check-compile` pass.

Expected final output is nine rows beginning `[300, 301, 302, 303, 304]` and
ending `[380, 381, 382, 383, 384]`.
'});