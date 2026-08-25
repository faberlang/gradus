#!/usr/bin/env python3
"""Generate and verify the frozen GEA3 prompt/token-id fixture.

The token ids are produced by the existing GGUF-backed tokenizer
(`gradus:tokenizer`, LIB-02 runtime) through the workspace `faber` binary;
this script never re-implements BPE. The prompt is natural text chosen on
merit — its length is recorded as it falls, never engineered (GEA3 goal fork
ruling, natural-T_p prefill).

The fixture freezes two id rows over the pinned GGUF tables:

* `raw_token_ids` — `tokenize` (parse-special on, smollm scanner) of the
  prompt text. The literal route (`tokenize_literal`) is recorded too and
  must agree (the prompt contains no special markers).
* `comparator_token_ids` — `tokenize` of the rendered chat prompt. The
  pinned llama-cli build applies the model's chat template to every `-p`
  prompt (observed live: the `__verbose` record carries the rendered prompt
  and `tokens_evaluated`), so the matched-prompt sequence the model actually
  consumes — and the GEA3 route must consume — is the rendered one.

The llama-cli parity facts are frozen observations from one live run of the
pinned binary; they are recorded, not re-derived here.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

GENERATOR = "fixtures/tokenizer/gen_gea3_prompt.py"
FIXTURE_DIR = Path(__file__).resolve().parent
FIXTURE_JSON = FIXTURE_DIR / "gea3-prompt-tokens.json"
FIXTURE_MANIFEST = FIXTURE_DIR / "gea3-prompt-tokens.manifest.json"

SCHEMA = "gea3-prompt-tokens-v1"
MANIFEST_SCHEMA = "gea3-prompt-tokens-manifest-v1"

WORKSPACE = Path("/Users/ianzepp/work/faberlang")
DEFAULT_GGUF = Path(
    "/Users/ianzepp/ai/models/derived/HuggingFaceTB/SmolLM2-360M-Instruct/"
    "a10cc1512eabd3dde888204e902eca88bddb4951/SmolLM2-360M-Instruct-f32.gguf"
)
DEFAULT_FABER = WORKSPACE / "radix" / "target" / "debug" / "faber"
GGUF_SHA256 = (
    "4d10b02ea1b189cb9637b39ba1543c61f69a8766099076880888f4443754e128"
)
GGUF_BYTES = 1_449_071_552

PROMPT_TEXT = "The tallest mountain on Earth is"
RENDERED_PROMPT = (
    "<|im_start|>system\n"
    "You are a helpful AI assistant named SmolLM, trained by Hugging Face"
    "<|im_end|>\n"
    "<|im_start|>user\n"
    + PROMPT_TEXT
    + "<|im_end|>\n"
    "<|im_start|>assistant\n"
)

N_PREDICT = 8
L_MAX_MARGIN = 32

# Frozen live observation of the pinned comparator (llama-cli build
# b10290-c8e03ce81) at this prompt under the GEA1-U6 deterministic flag set.
LLAMA_CLI_SHA256 = (
    "125a9512feb669abc43b6975ad2af70599b12fc01ae196c67b728554f33a5a42"
)
COMPARATOR_FLAGS = [
    "-m",
    "<frozen f32 gguf>",
    "-p",
    PROMPT_TEXT,
    "-n",
    str(N_PREDICT),
    "--seed",
    "0",
    "--temp",
    "0",
    "--top-k",
    "1",
    "--top-p",
    "1",
    "--no-display-prompt",
    "--no-conversation",
    "--log-disable",
    "--verbose-prompt",
]
OBSERVED_TOKENS_EVALUATED = 36
OBSERVED_GREEDY_TOKEN_IDS = [
    504,
    31469,
    6740,
    335,
    2591,
    314,
    5509,
    38921,
]
OBSERVED_GENERATION = "The tallest mountain on Earth is Mount Everest"

# The throwaway Faber runner mirrors the qwen36 capstone admission path
# (bounded table-prefix read, public gguf_manifest admission over the range
# seam, artifact identity check, tokenizer build) and prints machine-
# readable id rows. It is generated into a temp directory at run time and
# never committed.
RUNNER_SOURCE = '''+++
locale = "en"
+++
import from "gradus:model/artifact" artifact
import from "gradus:model/gguf_manifest" gguf_manifest
import from "gradus:tokenizer" tokenizer
import from "norma:process" process
import from "norma:fs" fs

const int ORACLE_LENGTH ← 1449071552
const int ORACLE_VERSION ← 3
const int ORACLE_ALIGNMENT ← 32
const int ORACLE_DATA_START ← 1787072
const int ORACLE_METADATA ← 37
const int ORACLE_TENSORS ← 290

union RunnerError {
    BadArguments { string message },
    BadDigest { string message },
    ShortPrefix { string message },
    BadManifest { string message },
    AdmissionRejected { string message }
}

fn message(RunnerError e) → string {
    match e {
        case BadArguments const message { return message }
        case BadDigest const message { return message }
        case ShortPrefix const message { return message }
        case BadManifest const message { return message }
        case AdmissionRejected const message { return message }
    }
}

fn _range(list<int> prefix, int start, int length) → bytes ⇥ gguf_manifest.GgufManifestError {
    if start < 0 or length < 0 or start > prefix.length() - length {
        throw variant BadSource {message = "read request exceeds the bounded table prefix"}
    }
    const list<int> segment ← prefix.slice(start, start + length)
    const bytes bytes ← segment ↦ bytes
    return bytes
}

fn _identity(string digest, int length) → artifact.ContentIdentity ⇥ RunnerError {
    do {
        return artifact.identity("sha-256", digest, length)
    }
    catch err {
        throw variant BadDigest { message = "content identity invalid: " + err.message }
    }
}

fn _admission(
    (int, int) → bytes ⇥ gguf_manifest.GgufManifestError source,
    int artifact_length,
    artifact.ContentIdentity identity
) → gguf_manifest.GgufManifest ⇥ RunnerError {
    do {
        return gguf_manifest.inspect(source, artifact_length, identity)
    }
    catch err {
        throw variant BadManifest { message = "manifest admission failed: " + err.message }
    }
}

fn _repr_ids(list<int> ids) → string {
    var string out ← ""
    var int i ← 0
    while i < ids.length() {
        if i > 0 { out ← out + "," }
        out ← out + (ids.get(i) coalesce 0 ↦ string)
        i ↑
    }
    return out
}

main {
    do {
        const list<string> args ← process.argv() ↦ list<string>
        if args.length() < 5 {
            throw variant BadArguments { message = "usage: runner <model> --sha256 <digest> --prompt <text>" }
        }
        const string via ← args.get(0) coalesce ""
        var string digest ← ""
        var string prompt ← ""
        var int i ← 1
        while i < args.length() {
            const string arg ← args.get(i) coalesce ""
            if arg ≡ "--sha256" {
                digest ← args.get(i + 1) coalesce ""
                i ← i + 2
            } elif arg ≡ "--prompt" {
                prompt ← args.get(i + 1) coalesce ""
                i ← i + 2
            } else {
                throw variant BadArguments { message = "unexpected argument: " + arg }
            }
        }
        if digest ≡ "" or prompt ≡ "" {
            throw variant BadArguments { message = "--sha256 and --prompt are required" }
        }
        const int total ← fs.byte_length(via)
        if total ≠ ORACLE_LENGTH {
            throw variant AdmissionRejected { message = "byte length mismatch" }
        }
        const artifact.ContentIdentity identity ← _identity(digest, total)
        const bytes prefix_bytes ← fs.read_range(via, 0, ORACLE_DATA_START)
        if prefix_bytes.length() ≠ ORACLE_DATA_START {
            throw variant ShortPrefix { message = "short table-prefix read" }
        }
        const value prefix_payload ← prefix_bytes ↦ value
        var list<int> prefix ← empty
        do {
            prefix ← prefix_payload ↦ list<int>
        }
        catch err {
            throw variant BadManifest { message = "carrier conversion failed: " + err }
        }
        const gguf_manifest.GgufManifest m ← _admission(
            (int start, int length) → bytes ⇥ gguf_manifest.GgufManifestError ∴ _range(prefix, start, length),
            total,
            identity
        )
        if m.version ≠ ORACLE_VERSION or m.alignment ≠ ORACLE_ALIGNMENT or m.data_start ≠ ORACLE_DATA_START {
            throw variant AdmissionRejected { message = "header fact mismatch" }
        }
        if m.metadata.length() ≠ ORACLE_METADATA or m.tensors.length() ≠ ORACLE_TENSORS {
            throw variant AdmissionRejected { message = "census mismatch" }
        }
        var tokenizer.Tokenizer t ← tokenizer.Tokenizer {words = empty, vocab = empty, concursus = empty, special_texts = empty, specialia_ids = empty, eog = empty, add_bos = false, chat_template = "", multitudo = 0}
        do {
            t ← tokenizer.build(m)
        }
        catch err {
            throw variant BadManifest { message = "tokenizer build failed" }
        }
        var list<int> ids ← empty
        do {
            ids ← tokenizer.tokenize(t, prompt)
        }
        catch err {
            throw variant BadManifest { message = "tokenize failed" }
        }
        print "IDS " + _repr_ids(ids)
        var list<int> literal ← empty
        do {
            literal ← tokenizer.tokenize_literal(t, prompt)
        }
        catch err {
            throw variant BadManifest { message = "tokenize_literal failed" }
        }
        print "LITERAL " + _repr_ids(literal)
        print "EOG " + _repr_ids(t.eog)
        print "ADDBOS " + ((t.add_bos ↦ int) ↦ string)
    }
    catch err {
        panic "gea3 tokenizer runner failed: " + message(err)
    }
}
'''


def encode(faber: Path, gguf: Path, prompt: str) -> dict[str, object]:
    """Run the tokenizer runner once and parse its id rows."""
    with tempfile.TemporaryDirectory(prefix="gea3-tokenizer-") as temp:
        runner = Path(temp) / "main.fab"
        runner.write_text(RUNNER_SOURCE, encoding="utf-8")
        environment = dict(os.environ)
        environment["FABER_LIBRARY_HOME"] = str(WORKSPACE)
        result = subprocess.run(
            [
                str(faber),
                "run",
                str(runner),
                "--",
                str(gguf),
                "--sha256",
                GGUF_SHA256,
                "--prompt",
                prompt,
            ],
            capture_output=True,
            text=True,
            env=environment,
            check=False,
        )
    if result.returncode != 0:
        print(f"faber run failed ({result.returncode}):", file=sys.stderr)
        print(result.stdout[-2000:], file=sys.stderr)
        print(result.stderr[-2000:], file=sys.stderr)
        raise SystemExit(1)
    rows: dict[str, str] = {}
    for line in result.stdout.splitlines():
        for prefix in ("IDS ", "LITERAL ", "EOG ", "ADDBOS "):
            if line.startswith(prefix):
                rows[prefix.strip()] = line[len(prefix) :].strip()
    for required in ("IDS", "LITERAL", "EOG", "ADDBOS"):
        if required not in rows:
            print(f"runner output missing {required} row", file=sys.stderr)
            raise SystemExit(1)

    def parse_ids(name: str) -> list[int]:
        raw = rows[name]
        return [int(value) for value in raw.split(",")] if raw else []

    return {
        "ids": parse_ids("IDS"),
        "literal": parse_ids("LITERAL"),
        "eog": parse_ids("EOG"),
        "add_bos": int(rows["ADDBOS"]),
    }


def fixture_document(
    raw: dict[str, object], comparator: dict[str, object]
) -> dict[str, object]:
    raw_ids = raw["ids"]
    literal_ids = raw["literal"]
    comparator_ids = comparator["ids"]
    assert isinstance(raw_ids, list)
    assert isinstance(literal_ids, list)
    assert isinstance(comparator_ids, list)
    if literal_ids != raw_ids:
        raise SystemExit("parse-special and literal routes disagree on the prompt")
    embedded_at = None
    for start in range(len(comparator_ids) - len(raw_ids) + 1):
        if comparator_ids[start : start + len(raw_ids)] == raw_ids:
            embedded_at = start
            break
    if embedded_at is None:
        raise SystemExit("raw id run is not embedded in the comparator ids")
    if len(comparator_ids) != OBSERVED_TOKENS_EVALUATED:
        raise SystemExit(
            f"comparator id count {len(comparator_ids)} != observed "
            f"{OBSERVED_TOKENS_EVALUATED}"
        )
    if raw["add_bos"] != 0:
        raise SystemExit("pinned tokenizer is BOS-free; add_bos drifted")
    return {
        "schema": SCHEMA,
        "generator": GENERATOR,
        "prompt_text": PROMPT_TEXT,
        "tokenizer": {
            "module": "gradus:tokenizer",
            "runtime": "artifact-backed byte-level BPE over the pinned GGUF tables",
            "encode_route": "tokenize (parse-special on, smollm scanner)",
            "raw_token_ids": raw_ids,
            "raw_route_literal_ids": literal_ids,
            "raw_count": len(raw_ids),
            "bos_prepended": False,
            "eog_set": raw["eog"],
        },
        "comparator_prompt": {
            "rendered_prompt": RENDERED_PROMPT,
            "token_ids": comparator_ids,
            "count": len(comparator_ids),
            "source": (
                "gradus:tokenizer tokenize over the rendered chat prompt "
                "(model chat_template metadata, add_generation_prompt)"
            ),
        },
        "parity": {
            "llama_cli_sha256": LLAMA_CLI_SHA256,
            "command_flags": COMPARATOR_FLAGS,
            "capture_mode": (
                "same flags with --log-disable replaced by -v (exposes the "
                "__verbose prompt record and per-token debug); a verbatim "
                "frozen-flag re-run produced identical generation text"
            ),
            "observed_rendered_prompt": RENDERED_PROMPT,
            "observed_tokens_evaluated": OBSERVED_TOKENS_EVALUATED,
            "observed_greedy_token_ids": OBSERVED_GREEDY_TOKEN_IDS,
            "observed_generation": OBSERVED_GENERATION,
            "parity_claims": [
                "rendered prompt string identical to the tokenizer input",
                "gradus id count equals tokens_evaluated (36)",
                f"raw id run embedded at comparator positions {embedded_at}..{embedded_at + len(raw_ids) - 1}",
            ],
        },
        "policy": {
            "sampling": "greedy argmax, first-index tie",
            "n_predict": N_PREDICT,
            "l_max": len(comparator_ids) + N_PREDICT + L_MAX_MARGIN,
            "l_max_formula": (
                f"prompt({len(comparator_ids)}) + n_predict({N_PREDICT}) + "
                f"margin({L_MAX_MARGIN})"
            ),
            "logits_row_values": 49152,
            "eog_terminated": False,
        },
    }


def fixture_text(document: dict[str, object]) -> str:
    return json.dumps(document, indent=2, sort_keys=True) + "\n"


def manifest_document(fixture_bytes: bytes, gguf: Path) -> dict[str, object]:
    return {
        "schema": MANIFEST_SCHEMA,
        "generator": GENERATOR,
        "fixture": "fixtures/tokenizer/gea3-prompt-tokens.json",
        "bytes": len(fixture_bytes),
        "sha256": hashlib.sha256(fixture_bytes).hexdigest(),
        "value_policy": (
            "token ids encoded by gradus:tokenizer (gradus/src/tokenizer.fab, "
            "LIB-02) over the pinned GGUF tables via the workspace faber "
            "binary; natural prompt, no engineered length"
        ),
        "gguf": {
            "path": str(gguf),
            "sha256": GGUF_SHA256,
            "bytes": GGUF_BYTES,
        },
    }


def manifest_text(document: dict[str, object]) -> str:
    return json.dumps(document, indent=2, sort_keys=True) + "\n"


def verify_gguf(gguf: Path) -> None:
    digest = hashlib.sha256()
    with gguf.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    if digest.hexdigest() != GGUF_SHA256:
        raise SystemExit("GGUF digest drift")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--gguf", type=Path, default=DEFAULT_GGUF)
    parser.add_argument("--faber", type=Path, default=DEFAULT_FABER)
    parser.add_argument("--check", action="store_true")
    arguments = parser.parse_args()

    if not arguments.faber.is_file():
        print(f"missing workspace faber binary: {arguments.faber}", file=sys.stderr)
        return 1
    verify_gguf(arguments.gguf)

    raw = encode(arguments.faber, arguments.gguf, PROMPT_TEXT)
    comparator = encode(arguments.faber, arguments.gguf, RENDERED_PROMPT)
    document = fixture_document(raw, comparator)
    text = fixture_text(document)

    if arguments.check:
        if not FIXTURE_JSON.is_file():
            print(f"missing fixture: {FIXTURE_JSON}", file=sys.stderr)
            return 1
        committed = FIXTURE_JSON.read_text(encoding="utf-8")
        if committed != text:
            print(
                "GEA3 prompt fixture drift: regenerate with gen_gea3_prompt.py",
                file=sys.stderr,
            )
            return 1
        fixture_bytes = committed.encode("utf-8")
        committed_manifest = FIXTURE_MANIFEST.read_text(encoding="utf-8")
        if committed_manifest != manifest_text(
            manifest_document(fixture_bytes, arguments.gguf)
        ):
            print("GEA3 prompt fixture manifest drift", file=sys.stderr)
            return 1
        print("PASS gea3-prompt-tokens fixture reproduces from the pinned GGUF")
        return 0

    FIXTURE_JSON.write_text(text, encoding="utf-8")
    FIXTURE_MANIFEST.write_text(
        manifest_text(manifest_document(text.encode("utf-8"), arguments.gguf)),
        encoding="utf-8",
    )
    print(f"wrote {FIXTURE_JSON}")
    print(f"wrote {FIXTURE_MANIFEST}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
