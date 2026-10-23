#!/usr/bin/env bash
# Fresh-process cursor resume proof.
#
# Eight separate faber processes drive one cursor file:
#
#   process 1  start   -> writes lm_cursor_start for the training split
#   process 2  step    -> loads it from disk, prints window 0, rewrites cursor
#   process 3  step    -> loads the rewritten cursor, prints window 1
#   process 4-6 step   -> prints windows 2, 3 and 4 (the split's final window)
#   process 7  step    -> loads the persisted terminal cursor, prints
#                         `exhausted` and leaves the file untouched
#   process 8  step    -> still `exhausted`: the final window is never replayed
#
# The fixture corpus is three fixed documents ([[65,66,67],[68,69],
# [70,71,72,73]]), all in the training split, windows of width 2, so a complete
# traversal is five windows. The proof fails unless every process prints the
# expected line, unless each window differs from the one before it (a resume
# that did not advance would print the same window twice), unless the cursor
# file already holds the terminal wire as soon as the final window has been
# consumed (so a restart cannot replay it), unless later processes report
# exhaustion without touching that file, and unless a fresh start-then-step
# pair reproduces window 0 byte for byte.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SOURCE="$ROOT/tests/lm-cursor-resume/main.fab"
WORKSPACE="$(cd "$ROOT/.." && pwd)"

EXPECTED_WIRE='lm-cursor-v1#d3:65,66,67;d2:68,69;d4:70,71,72,73;#training#-1#0'
EXPECTED_TERMINAL_WIRE='lm-cursor-v1#d3:65,66,67;d2:68,69;d4:70,71,72,73;#training#-2#0'
EXPECTED_WINDOWS=(
    '0|0|65,66|66,67|1,1'
    '0|2|67,256|256,256|0,0'
    '1|0|68,69|69,256|1,0'
    '2|0|70,71|71,72|1,1'
    '2|2|72,73|73,256|1,0'
)
EXPECTED_EXHAUSTED='exhausted'

fail() {
    echo "lm-cursor-resume: FAIL: $1" >&2
    exit 1
}

# FABER_BIN overrides; otherwise the sibling radix build, then a PATH faber,
# then the worker-local gradus lane binary.
resolve_faber() {
    local candidate
    if [[ -n "${FABER_BIN:-}" ]]; then
        printf '%s\n' "$FABER_BIN"
        return 0
    fi
    for candidate in \
        "$WORKSPACE/radix/target/debug/faber" \
        "$WORKSPACE/radix/target/release/faber" \
        "$WORKSPACE/faber/target/debug/faber" \
        "$WORKSPACE/faber/target/release/faber"
    do
        if [[ -x "$candidate" ]]; then
            printf '%s\n' "$candidate"
            return 0
        fi
    done
    if command -v faber >/dev/null 2>&1; then
        command -v faber
        return 0
    fi
    if [[ -n "${HOME:-}" && -x "$HOME/.local/opt/faber/faber" ]]; then
        printf '%s\n' "$HOME/.local/opt/faber/faber"
        return 0
    fi
    echo "lm-cursor-resume: no faber binary found; set FABER_BIN" >&2
    exit 1
}

FABER="$(resolve_faber)"

# The runner needs a directory holding a gradus checkout; a stub home with
# this checkout linked in keeps the proof independent of the checkout's name.
STUB_HOME=""
cleanup() {
    if [[ -n "$STUB_HOME" && -d "$STUB_HOME" ]]; then
        rm -rf "$STUB_HOME"
    fi
}
trap cleanup EXIT

if [[ -n "${LIBRARY_HOME:-}" ]]; then
    RESOLVED_HOME="$LIBRARY_HOME"
else
    STUB_HOME="$(mktemp -d)"
    ln -s "$ROOT" "$STUB_HOME/gradus"
    RESOLVED_HOME="$STUB_HOME"
fi

SCRATCH="$(mktemp -d)"
trap 'cleanup; rm -rf "$SCRATCH"' EXIT

run_fixture() {
    local path="$1"
    local mode="$2"
    "$FABER" run --library-home "$RESOLVED_HOME" "$SOURCE" -- "$path" "$mode"
}

cursor="$SCRATCH/cursor.wire"
fresh="$SCRATCH/fresh.wire"

wire="$(run_fixture "$cursor" start)"
if [[ "$wire" != "$EXPECTED_WIRE" ]]; then
    fail "start wire: expected [$EXPECTED_WIRE], got [$wire]"
fi
if [[ "$(cat "$cursor")" != "$EXPECTED_WIRE" ]]; then
    fail "start did not write the initial cursor to $cursor"
fi

# Walk the whole corpus, one fresh process per window.
previous=""
first=""
first_cursor=""
for index in "${!EXPECTED_WINDOWS[@]}"; do
    expected="${EXPECTED_WINDOWS[$index]}"
    printed="$(run_fixture "$cursor" step)"
    if [[ "$printed" != "$expected" ]]; then
        fail "step $((index + 1)) window: expected [$expected], got [$printed]"
    fi
    if [[ "$printed" == "$previous" ]]; then
        fail "step $((index + 1)) repeated the previous window; the cursor did not resume"
    fi
    if [[ "$index" -eq 0 ]]; then
        first="$printed"
        first_cursor="$(cat "$cursor")"
    fi
    previous="$printed"
done

# Consuming the final window must persist the terminal cursor right away: a
# restart before any exhaustion report would otherwise replay that window.
if [[ "$(cat "$cursor")" != "$EXPECTED_TERMINAL_WIRE" ]]; then
    fail "the final window did not persist the terminal cursor: expected [$EXPECTED_TERMINAL_WIRE], got [$(cat "$cursor")]"
fi

exhausted="$(run_fixture "$cursor" step)"
if [[ "$exhausted" != "$EXPECTED_EXHAUSTED" ]]; then
    fail "post-traversal step: expected [$EXPECTED_EXHAUSTED], got [$exhausted]"
fi
if [[ "$(cat "$cursor")" != "$EXPECTED_TERMINAL_WIRE" ]]; then
    fail "the exhausted process rewrote the terminal cursor: [$(cat "$cursor")]"
fi
repeated="$(run_fixture "$cursor" step)"
if [[ "$repeated" != "$EXPECTED_EXHAUSTED" ]]; then
    fail "second post-traversal step: expected [$EXPECTED_EXHAUSTED], got [$repeated]"
fi
if [[ "$(cat "$cursor")" != "$EXPECTED_TERMINAL_WIRE" ]]; then
    fail "the second exhausted process rewrote the terminal cursor: [$(cat "$cursor")]"
fi

fresh_wire="$(run_fixture "$fresh" start)"
if [[ "$fresh_wire" != "$EXPECTED_WIRE" ]]; then
    fail "fresh start wire: expected [$EXPECTED_WIRE], got [$fresh_wire]"
fi
replayed="$(run_fixture "$fresh" step)"
if [[ "$replayed" != "$first" ]]; then
    fail "fresh start-then-step did not reproduce the first window: [$replayed]"
fi
if [[ "$(cat "$fresh")" != "$first_cursor" ]]; then
    fail "fresh start-then-step wrote a different cursor than the resumed run"
fi

printf '%s\n' "$first"
printf '%s\n' "${EXPECTED_WINDOWS[1]}"
printf '%s\n' "$exhausted"
echo "lm-cursor-resume: ok (fresh processes resumed windows 0-4, persisted the terminal cursor, and reported exhaustion without replay)"
