# Gradus Compatibility Policy

**Version**: `compatibility-policy v1.1.0` (2026-08-17, S2 identifier clean break)
**Repo**: gradus. **Applies to**: the gradus library surface (version 0.1.0,
pre-1.0) and every admitted support-matrix row
(`docs/factory/production-ml-library/pml0-support-matrix.md`).
**Row-level authority**: each admitted row's `compatibility policy` field is
the row-level authority; this document is the product-facing aggregate that
names what breaks, what migrates, and the identity rules.

## 1. Pre-1.0 clean-break posture

Gradus is **pre-1.0** (`faber.toml` version 0.1.0). There is **no stability
promise before 1.0**. Breaking changes are allowed and executed as **clean
breaks** — no forwarding shims, containment facades, compatibility aliases, or
deprecation window — consistent with the faber product clean-break posture.

Every break is recorded in the landing commit, this policy, and the owning
factory receipt. Consumers migrate to the new surface. Import coordinates
remain stable, but member names, types, fields, and private helpers are not
preserved through aliases.

## 2. S2 English identifier break

Pass B replaced the Gradus-owned Latin identifier surface with the final
English member surface across the library source, co-located proofs, in-repo
exempla, and admission tests. The break is member-scoped: functions, types,
fields, and private helpers were renamed; retained parameters, comments,
strings, wire literals, and import coordinates were not mechanically rewritten.

The ordered implementation receipts are:

| Commit | Surface | Receipt |
| --- | --- | --- |
| `2176e37` | S2 collision preflight | Reserved names, tensor shape probe, member ledgers, and no-pack-row ruling |
| `62fcbc7` | L1 dtype/shape/tensor/math | Final `rank`, `numel`, `dtype`, `shape`, `get`, `construct`, and arithmetic surface |
| `8b72e1a` | Shared parameter/serialize/gradient | Final identity, payload, registry, and byte-helper surface |
| `53c2a2f` | Train/loss/optimize/nn | Final training, optimizer, RNG, checkpoint, metric, and primitive surface |
| `00681b4` | Attention/transformer | Final RoPE policy/configuration and transformer surface |
| `e817959` | Model formats and architecture leaves | Final capsule, manifest, descriptor, dequant, and model-admission surface |
| `b2e67a6`, `05dda3c` | Tokenizer | Final tokenizer identity, build, encode/decode, probe, and policy surface |
| `1750448` | Inference | Final cache, decoder, sampler, generation config, and cursor surface |
| `12944bf` | Facade and in-repo callers | Final Gradus facade, exempla, and admission-test caller chase |

S2-DOCS rebases this policy and the machine-checked API inventory from the
live post-`12944bf` tree in the S2-DOCS closeout. The live inventory is 750 `fn `
declarations across 33 modules. This count is a declaration count, not a
compatibility alias map.

No `[[library_members]]` row was added. No locale-pack row was added. No Radix
compiler change was required. No Norma, Tela, Triga, Inferentia, or other
sibling-repository consumer migration is claimed by S2.

## 3. Correctness corrections

The pre-1.0 correctness wave remains recorded as semantic history:

| Commit | Change | Class |
| --- | --- | --- |
| `3c295c0` | Corrected the internal big-endian serialization readers | Private-helper correctness fix — no external migration |
| `6cc0eb5` | Restored tokenizer admission polarity for the pinned add-* flags and positive BOS/space facts | Admission-behavior correction — no public-name change |
| `2cdc498` | Enforced the exact pinned EOG set `{0,2}` during capsule admission | Identity rule — see §4 |
| `0d50d60` | Stopped generation after the first admitted EOG token | Semantic correction — pinned oracle/docs reconciled |

Private proof-shape helper retirement is recorded in
`docs/factory/production-ml-library/pml0-proof-api-ledger.md`. It is
bookkeeping, not an external compatibility surface.

## 4. Identity rules

### EOG-set identity rule

A different EOG set is a different tokenizer. The admitted row pins the EOG
set exactly: `{0,2}` (EOS 2, UNK 0). Capsule admission enforces the exact set,
and a well-formed-but-different set fails closed as an identity rejection. The
`tokenizer.is_eog` predicate binds the generation stop policy.

### Tokenizer identity

Tokenizer identity is the tuple: model (`gpt2`, byte-level BPE) + pre-tokenizer
(`smollm`) + special-token behavior (BOS-free, space-prefix-free) + vocab
fingerprint (pinned id lists P1–P11). Any divergence fails closed with
`ProbeDivergens` — identity is exact, never approximate
(`fixtures/tokenizer/tokenizer-identity-oracle.md`).

### KV-cache identity (MD-A9)

The KV cache identity key is model / version / execution-config / tokenizer /
prefix / positions / layer / dtype / layout. A change in any component is a
different logical value (`src/cache.fab`).

### Structural vs executed identity

Every admitted row is **structural tier**: the committed compile-level surface
plus pinned oracle values (f64 pins, tolerance bands, and token pins).
**Executed identity** — bare forward equals generated companion, executed
convergence values, and executed tokens — is a separate claim at the
auditor-owned runtime-evidence gate (CTO8-1). No compatibility promise in this
policy extends to executed values until that gate opens; the structural tier is
recorded in each row's note and is never upgraded implicitly.

## 5. One-row narrowing stays extensible (R3)

Support is claimed **per admitted row**, never at the library level: the row
is the unit of support claim (`pml0-support-matrix-schema.md` §2/§3). Two
consequences follow:

1. Narrow admission, such as the F32 dtype row or enumerated fixed shapes, is
   expressed in row vocabulary and capability descriptors, never as a generic
   baked into the public function surface. The public API shape stays generic
   over admitted descriptors.
2. Extending is additive. A new row is admitted only with its own fixture,
   oracle, and evidence under the schema's fail-closed gates. Adding a row does
   not change an existing row's public API shape.

## 6. Tier honesty

Everything this policy promises applies to the committed structural tier:
committed source, co-located proof pins, fixture oracles, and documented
compatibility fields. Executed verification is environment-blocked on the FMIR
lever; the release checklist names the executed-oracle gate as a pre-release
item. Until that gate opens, an executed claim is out of contract.

## 7. Versioning

This policy is versioned per the schema-version convention. Pre-1.0 clean
breaks may change this policy; each change records a new patch/minor/major
stamp. A major change re-states affected rows. Row-level compatibility fields
remain authoritative on any disagreement.
