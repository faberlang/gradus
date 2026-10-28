#!/usr/bin/env bash
# Falsifiability check for dense-decode-bench-metal: each tampered copy of the
# package must fail the run with exit status 1 and a FAIL line. Run it from the
# gradus directory:
#
#   FABER=/path/to/faber ./exempla/dense-decode-bench-metal/tamper.sh
#
# Four tampers, one per oracle clause plus one that changes the computation:
#   token   one pinned token flipped         -> "step 0 token 5 expected 4"
#   logit   one pinned logit moved by 1e-4   -> "step 0 logit 0 observed ..."
#   cache   cache growth pin off by one row  -> "step 0 cache length 9 expected 10"
#   eps     RMSNorm epsilon 1e-5 -> 1e-3     -> a logit pin fails
set -u
FABER="${FABER:-faber}"
HERE="$(cd "$(dirname "$0")" && pwd)"
LIBRARY_HOME="${LIBRARY_HOME:-$(cd "$HERE/../../.." && pwd)}"
DEVICE="${DEVICE:-metal}"
work="$(mktemp -d)"
trap 'rm -rf "$work"' EXIT
status=0

tamper() {
    local name="$1" from="$2" to="$3"
    local dir="$work/$name"
    mkdir -p "$dir"
    cp -R "$HERE/faber.toml" "$HERE/src" "$dir/"
    sed -i.bak "s/$from/$to/" "$dir/src/main.fab"
    if cmp -s "$dir/src/main.fab" "$dir/src/main.fab.bak"; then
        echo "tamper $name: sed did not change the source"
        status=1
        return
    fi
    rm "$dir/src/main.fab.bak"
    out="$("$FABER" run --device "$DEVICE" --library-home "$LIBRARY_HOME" "$dir" 2>&1)"
    code=$?
    fail_line="$(printf '%s\n' "$out" | grep '^FAIL' | head -1)"
    if [ "$code" -eq 1 ] && [ -n "$fail_line" ]; then
        echo "tamper $name: exit 1, $fail_line"
    else
        echo "tamper $name: UNEXPECTED exit $code"
        printf '%s\n' "$out" | tail -5
        status=1
    fi
}

tamper token 'PIN_TOKENS = \[5,' 'PIN_TOKENS = [4,'
tamper logit '\[0\.6716275713053531,' '[0.6717275713053531,'
tamper cache 'let int expected_rows ← PROMPT + i + 1' 'let int expected_rows ← PROMPT + i + 2'
tamper eps 'const f32 EPSILON = 0\.00001' 'const f32 EPSILON = 0.001'
exit "$status"
