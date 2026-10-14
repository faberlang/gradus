#!/bin/bash
# Gated real-file check for the A1 port weight load (U-G). NOT part of
# `faber test .`. Builds a scratch copy of the inferentia package whose entry
# is tests/port-load/driver.fab.part instead of the CLI main, runs it under a
# RELEASE faber against the real F32 GGUF, timestamps the driver's stderr
# progress, records peak RSS (/usr/bin/time -l), and compares the printed
# cells bit-exactly against the GGUF read directly with numpy (verify.py).
#
#   inferentia/tests/port-load/run.sh <release faber> <library home> \
#     [model.gguf] [scratch-dir]
#
# <library home> is the directory holding the gradus checkout
# (<home>/gradus/src); Norma is embedded in the faber binary. While the
# container still carries a stale `norma/` checkout beside `gradus/`, that
# checkout shadows the embedded Norma: pass a home that holds only gradus.
#
# Needs /opt/homebrew/bin/python3.13 (numpy). The load takes minutes; bound it
# with the run's own timeout (default 700 s, override with PORT_TIMEOUT).
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
PKG="$(cd "$HERE/../.." && pwd)"
FABER="${1:?usage: run.sh <release faber> <library home> [model.gguf] [scratch-dir]}"
LIBRARY_HOME="${2:?usage: run.sh <release faber> <library home> [model.gguf] [scratch-dir]}"
MODEL="${3:-/Users/ianzepp/ai/models/SmolLM2-360M-Instruct-f32.gguf}"
SCRATCH="${4:-/tmp/port-load-driver}"
export PATH="/opt/homebrew/bin:$PATH"

rm -rf "$SCRATCH/pkg"
mkdir -p "$SCRATCH/pkg/src"
cp "$PKG/faber.toml" "$PKG/faber.lock" "$SCRATCH/pkg/"
# faber.lock names the library by a path relative to the package root
ln -sfn "$LIBRARY_HOME/gradus" "$SCRATCH/gradus"
cp "$PKG/src/port_weights.fab" "$PKG/src/port_generate.fab" "$SCRATCH/pkg/src/"
python3.13 - "$PKG/src/main.fab" "$HERE/driver.fab.part" "$SCRATCH/pkg/src/main.fab" <<'PY'
import re, sys
main, part, out = sys.argv[1:4]
s = open(main).read()
i = s.index("main args argv {")
j = s.index("# ----", i)
open(out, "w").write(s[:i] + open(part).read() + "\n" + s[j:])
PY

LOG="$SCRATCH/run.log"
OUT="$SCRATCH/run.out"
python3.13 "$HERE/timed_run.py" "${PORT_TIMEOUT:-700}" "$LOG" "$OUT" \
  /usr/bin/time -l "$FABER" run --library-home "$LIBRARY_HOME" "$SCRATCH/pkg" -- live --model "$MODEL"
python3.13 "$HERE/verify.py" "$MODEL" "$OUT"
