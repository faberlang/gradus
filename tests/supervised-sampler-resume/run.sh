#!/usr/bin/env bash
# Fresh-process resume proof for the supervised sampler. Every batch is
# produced by a distinct faber process using only the persisted seed/epoch/
# position state; expected output is the uninterrupted deterministic run.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SOURCE="$ROOT/tests/supervised-sampler-resume/main.fab"
WORKSPACE="$(cd "$ROOT/.." && pwd)"

fail() {
    echo "supervised-sampler-resume: FAIL: $1" >&2
    exit 1
}

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
    echo "supervised-sampler-resume: no faber binary found; set FABER_BIN" >&2
    exit 1
}

FABER="$(resolve_faber)"
WORK="$(mktemp -d "${TMPDIR:-/tmp}/gradus.XXXXXX")"
cleanup() { rm -rf "$WORK"; }
trap cleanup EXIT

if [[ -n "${LIBRARY_HOME:-}" ]]; then
    RESOLVED_HOME="$LIBRARY_HOME"
else
    ln -sfn "$ROOT" "$WORK/gradus"
    RESOLVED_HOME="$WORK"
fi

run_fixture() {
    "$FABER" run --library-home "$RESOLVED_HOME" "$SOURCE" -- "$1" "$2"
}

state="$WORK/sampler.wire"
expected_initial='supervised-sampler-v1#d5:1,2,4,5,7;#123#0#0'
expected_wires=(
    'supervised-sampler-v1#d5:1,2,4,5,7;#123#0#2'
    'supervised-sampler-v1#d5:1,2,4,5,7;#123#0#4'
    'supervised-sampler-v1#d5:1,2,4,5,7;#123#0#5'
    'supervised-sampler-v1#d5:1,2,4,5,7;#123#1#2'
)
expected_batches=(
    '2|x=4.0,14.0,5.0,15.0|y=104.0,204.0,304.0,105.0,205.0,305.0'
    '2|x=7.0,17.0,2.0,12.0|y=107.0,207.0,307.0,102.0,202.0,302.0'
    '1|x=1.0,11.0|y=101.0,201.0,301.0'
    '2|x=5.0,15.0,1.0,11.0|y=105.0,205.0,305.0,101.0,201.0,301.0'
)

started="$(run_fixture "$state" start)"
[[ "$started" == "$expected_initial" ]] || fail "initial wire: expected [$expected_initial], got [$started]"
[[ "$(cat "$state")" == "$expected_initial" ]] || fail "start did not persist initial state"

for index in "${!expected_batches[@]}"; do
    printed="$(run_fixture "$state" step)"
    expected="${expected_batches[$index]}"
    [[ "$printed" == "$expected" ]] || fail "step $((index + 1)) batch: expected [$expected], got [$printed]"
    persisted="$(cat "$state")"
    expected_wire="${expected_wires[$index]}"
    [[ "$persisted" == "$expected_wire" ]] || fail "step $((index + 1)) state: expected [$expected_wire], got [$persisted]"
done

printf '%s\n' "${expected_batches[@]}"
echo "supervised-sampler-resume: ok (fresh processes resumed three batches including the short tail, then crossed into epoch 1)"
