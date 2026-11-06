# Typed KV-cache owner

`cache/kv.KVCache` owns the K/V storage, exact token history, logical `length()`, immutable `capacity`, and mutation `version`. Use `append` for one decoded F32 row, `extend` for a multi-row F32 block, or their encoded counterparts for opaque physical rows. A successful append/extend is one mutation and advances the version once. `rollback(cache, earlier_length)` discards the suffix from the logical history and K/V storage and advances the version, including when the requested length equals the current length. Appending after rollback starts at that length, replacing the discarded suffix.

Append and extend reject capacity overflow with typed `CacheError.Overflow`; admission occurs before values are committed, so the input cache is unchanged and no write can pass capacity. Rollback rejects a negative length or a length greater than the current logical length with `CacheError.InvalidDimension`.

The GPU decode kernels still accept explicit row positions: these are device-kernel interfaces, not a host-side cache owner. The typed staged `KVCache` API is the owner for staged callers; resident stream tensors remain updated by the decode kernels.
