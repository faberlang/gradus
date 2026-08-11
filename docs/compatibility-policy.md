# Gradus Compatibility Policy

**Version**: `compatibility-policy v1.0.0` (2026-08-11, PML6-U3)
**Repo**: gradus. **Applies to**: the gradus library surface (version 0.1.0,
pre-1.0) and every admitted support-matrix row
(`docs/factory/production-ml-library/pml0-support-matrix.md`).
**Row-level authority**: each admitted row's `compatibility policy` field is
the row-level authority; this document is the product-facing aggregate that
names what breaks, what migrates, and the identity rules.

## 1. Pre-1.0 clean-break posture

Gradus is **pre-1.0** (`faber.toml` version 0.1.0). There is **no stability
promise before 1.0**. Breaking changes are allowed and executed as **clean
breaks** — no forwarding shims, no containment facades, no deprecation window
— consistent with the faber product clean-break posture.

Every break is **recorded**: the commit message + this policy carry the note
(and, where a phase owns the change, the phase closeout). Consumers migrate at
the new shape.

The correctness wave is the canonical pre-1.0 example (all recorded):

| Commit | Change | Class |
| --- | --- | --- |
| `3c295c0` | big-endian serialize readers renamed `_le4/_le8` → `_be4_lege/_be8_lege` | private-helper correctness fix — **no external migration** (§2) |
| `6cc0eb5` | tokenizer admission polarity restored: the pinned add-* flags are `falsum`; `bos_vacua` / `spatium_vacua` are the positive facts (guard `≡`, was `≠`) | admission-behavior correction — tokenizer rows re-validated, no public-name change |
| `2cdc498` | capsule admission enforces the exact pinned EOG set `{0,2}`; a well-formed-but-different set is a different tokenizer | identity rule — see §3 |
| `0d50d60` | generation terminates after the first admitted EOG token (greedy `[0]`, not `[0,0]`); `maxima_verborum` is a ceiling, never a promise | semantic correction — pinned oracle/docs reconciled |

## 2. What breaks / what migrates

### Proof-shape helper retirement (recorded, no external surface)

Internal helpers retired as their math is inlined carry a **proof-shape
retirement note** in the proof ledger (`pml0-proof-api-ledger.md`): e.g.
`attention_block_2x8` / `ffn_block_2x8` retire with the math inlined
(rows 13–15). Retirement is a bookkeeping record, never an external
compatibility surface.

### Private-helper rename: `_le4/_le8` → `_be4_lege/_be8_lege` (no external migration)

The big-endian serialize readers (`src/serialize.fab`) were renamed because
the old `_le4/_le8` names were **misleading** — they read big-endian bytes.
This is a **private-helper correctness fix**: the helpers are not public API,
are not in the admitted-row vocabulary, and carry **no external migration**.
Callers of the public surface are unaffected. The rename is recorded so no
future reader assumes a little-endian reader exists under the old names.

### Public API shape (the staged carrier)

The staged-carrier API shape (`docs/api-shape-policy.md`) is the public shape
contract. A change to that shape before 1.0 is a clean break (§1), recorded in
the commit + this policy.

## 3. Identity rules

### EOG-set identity rule

**A different EOG set is a different tokenizer.** The admitted row's tokenizer
identity pins the EOG set exactly: `{0,2}` (EOS 2, UNK 0). Capsule admission
enforces the exact pinned set (`2cdc498`; `EOG ← "0,2"`,
`_tokenizator_recta` requires `eog ≡ EOG`), so a well-formed-but-different EOG
set **fails closed** with `EogMala` — it is not a value error, it is an
**identity** rejection. `tokenizator.est_eog` is the generation stop-policy
binding (`0d50d60`).

### Tokenizer identity

Tokenizer identity is the tuple: model (`gpt2`, byte-level BPE) + pre-tokenizer
(`smollm`) + special-token behavior (BOS-free, space-prefix-free) + vocab
fingerprint (pinned id lists P1–P11). Any divergence fails closed
(`ProbeDivergens`) — identity is exact, never approximate
(`fixtures/tokenizer/tokenizer-identity-oracle.md`).

### KV-cache identity (MD-A9)

The KV cache's identity key is model / version / execution-config / tokenizer /
prefix / positions / layer / dtype / layout — a change in any component is a
different logical value (`src/cache.fab`).

### Structural vs executed identity

Every admitted row is **structural tier**: the commitment is the committed
compile-level surface + pinned oracle values (f64 pins, tolerance bands,
token pins). **Executed identity** — bare forward ≡ generated companion,
executed convergence values, executed tokens — is a **separate claim** at the
auditor-owned runtime-evidence gate (CTO8-1, named open clause in
`pml5-closeout.md`). No compatibility promise in this policy extends to
executed values until that gate opens; the structural tier is recorded in each
row's note and is **never upgraded**.

## 4. One-row narrowing stays extensible (R3)

Support is claimed **per admitted row**, never at the library level: the row is
the unit of support claim (`pml0-support-matrix-schema.md` §2/§3). Two
consequences:

1. **Narrowing never hard-codes into public API shape.** A narrow admission
   (e.g. the F32 dtype row, the enumerated fixed shapes) is expressed in the
   row vocabulary and the capability descriptors (support rows, claim-register
   vocabulary) — never as a generic baked into the public function surface.
   The public API shape stays generic over the admitted descriptors.
2. **Extending is additive.** A new row is admitted only with per-row
   fixture/oracle/evidence per the schema's fail-closed gates (R1–R11);
   admission is a new matrix row, never a widening of an existing row's
   compatibility policy. Adding a row does not change public API shape.

This keeps the support surface extensible: future rows (dtypes, quantizations,
architectures, tokenizers) land as new admitted rows with their own evidence —
one-row narrowing never blocks an extension, and an extension never smuggles a
broader support claim.

## 5. Tier honesty (what is promised)

Everything this policy promises applies to the **committed structural tier**:
committed source, co-located proba pins, fixture oracles, and the documented
compatibility fields. Executed verification is env-blocked on the FMIR lever;
the release checklist (`docs/release-checklist.md`, PML6-U5) names the
executed-oracle gate as a **named pre-release item**. Until that gate opens, an
executed claim is out of contract.

## 6. Versioning

This policy is versioned (`compatibility-policy v1.0.0`) per the schema-version
convention. Pre-1.0 clean breaks may change this policy; each change records a
new patch/minor/major stamp per the convention, and a major change re-states
the affected rows. The row-level `compatibility policy` fields stay the
row-level authority on any disagreement.
