# PML1 Closeout Note — R1 recheck records (PML1 phase close)

**Unit**: PML1 closeout reconciliation (accumulated residuals from U1–U7 +
head-cto CTO-2); no phase reopen
**Date**: 2026-08-09
**Predecessor**: PML1-U1..U7 all landed (45a09d9..de017eb); CTO-2
dispositions folded into this closeout (2d26a2db memo)
**Repo**: gradus

## R1 record 1 — Staged-carrier shape posture at phase close

**Posture**: the staged carrier (runtime dimension list inside the value
carrier, static shape pinned by the consumer at materialization) is the
PML1 shape representation, confirmed at phase close.

- **No packet revision**: the `pml0-interface-packet` §3 shape facts
  (compile-time class — shapes are static facts at the boundary) are
  UNCHANGED. The runtime list is the value-carrier representation; the
  boundary still carries static `tensor<f32, [2,2]>` types, so the
  interface packet v1 stands as filed. Boundary unchanged at phase close.
- Compiler evidence for the staged choice remains as recorded in
  `src/shape.fab` and `src/tensor.fab` (U1 header): generic shape genus
  (`Tensor<[2,2]>` type-argument application) is PARSE001; shape-hole
  `tensor<f32, _>` fields/returns are SEM014 in standalone library context;
  the staged carrier compiles today.
- CTO-2 shape-policy correction applied at this closeout: `DIMENSI_LIMES`
  65536 is the GI1 pinned-row ceiling (a support-row/capsule admission fact,
  `pml0-model-capsule-contract.md` §5 row 5), NOT a general math limit.
  General checked shape arithmetic (quantitas/broadcastum/reformanda/
  expansio) no longer applies the per-dimension 65536 cap, so 128k–152k
  vocab rows stay expressible. Tensor construction (structa/impleta) routes
  the element product through `shape.quantitas` (ONE validator). The 65536
  constant remains documented as the capsule/support-row admission ceiling
  for PML2.
- **128k–152k vocab note** (recorded for PML2 admission): Qwen-class /
  deepseek-class vocab rows (128k–152k, e.g. 152064) exceed the GI1 65536
  pinned-row ceiling. The shape system admits them; PML2 support-matrix rows
  must carry their own per-row dimension ceilings rather than re-applying
  the GI1 65536 cap globally.
- **Serialize mirror aligned (phase-audit residual, CLOSED)**: the PML1
  phase audit found `gradus:serialize` still rejecting dims > 65536 at
  `src/serialize.fab` (`_quantitas` + the four shape-wire encode/decode
  ceiling checks), while `shape.quantitas` admits them — a mirror
  divergence that made 128k–152k-vocab shapes legal but not
  wire-round-trippable. The per-dim 65536 was a policy mirror of the GI1
  capsule ceiling, not a wire-format limit (dims encode as i64be), so the
  serialization checks were aligned to `shape.quantitas`: no per-dimension
  cap, element ceiling 1_000_000_000 and negative-dim rejection retained.
  Wire schema unchanged (serialize-schema-1.0.0; no version bump).

## R1 record 2 — Float-encoding drift flag (NGAB1 packet-fact recheck)

**Drift candidate**: text-encoded floats.

- `gradus:serialize` encodes tensor payload data as space-separated
  shortest-round-trip float text (UTF-8), not raw float bits — there is no
  float-bits primitive in Faber today. `_iunge_datos` / `_divido_datos` in
  `src/serialize.fab` convert f32 values via `↦ textus` / `↦ f32`.
- This is the first compiled packet fact (R1: "paper freeze precedes
  compiled proof — recheck at PML1 close; U7 serialization contract is the
  first compiled packet fact"). The NGAB1 packet-fact recheck must confirm
  the interface packet's typed-values/layout expectations accept a
  text-encoded float representation (round-trip-safe, not bit-exact) or
  record a drift to the packet before PML2 model loading consumes it.
- **Posture at close**: flagged as a drift candidate, NOT resolved here.
  Boundary unchanged; the packet revision mechanism (§VersionBump in
  `pml0-interface-packet.md`) is the channel if the recheck finds a
  mismatch. Owner: joint packet authority (PML Mind + NGAB Mind), recheck
  at NGAB1.

## Validation (closeout)

```bash
cd /Users/ianzepp/work/faberlang/gradus
./scripta/check-source && ./scripta/check-compile      # once, green
./scripta/inventory-public-symbols                     # exit 0; tracked total 17
python3 ../radix/scripta/generate-factory-readme.py --factory-root docs/factory --check
git diff --check
```

Outcome: one green closeout run; inventory re-baselined; README fresh;
`git diff --check` clean.
