#!/usr/bin/env bash
# Fresh-process cursor resume proof.
#
# Three separate faber processes drive one cursor file:
#
#   process 1  start   -> writes lm_cursor_start for the training split
#   process 2  step    -> loads it from disk, prints window 0, rewrites cursor
#   process 3  step    -> loads the rewritten cursor, prints window 1
#
# The fixture corpus is three fixed documents ([[65,66,67],[68,69],
# [70,71,72,73]]), all in the training split, windows of width 2. The proof
# fails unless process 2 and process 3 print the two expected consecutive
# windows, unless process 3 differs from process 2 (a resume that did not
# advance would print the same window twice), and unless a fresh
# start-then-step pair reproduces window 0 byte for byte.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SOURCE="$ROOT/tests/lm-cursor-resume/main.fab"
WORKSPACE="$(cd "$ROOT/.." && pwd)"

EXPECTED_WIRE='lm-cursor-v1#d3:65,66,67;d2:68,69;d4:70,71,72,73;#training#-1#0'
EXPECTED_FIRST='0|0|65,66|66,67|1,1'
EXPECTED_SECOND='0|2|67,256|256,256|0,0'

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

first="$(run_fixture "$cursor" step)"
if [[ "$first" != "$EXPECTED_FIRST" ]]; then
    fail "first step window: expected [$EXPECTED_FIRST], got [$first]"
fi
first_cursor="$(cat "$cursor")"

second="$(run_fixture "$cursor" step)"
if [[ "$second" != "$EXPECTED_SECOND" ]]; then
    fail "second step window: expected [$EXPECTED_SECOND], got [$second]"
fi
if [[ "$second" == "$first" ]]; then
    fail "second step repeated the first window; the cursor did not resume"
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
printf '%s\n' "$second"
echo "lm-cursor-resume: ok (fresh process resumed window 0 then window 1, replay identical)"
