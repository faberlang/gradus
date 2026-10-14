#!/usr/bin/env python3
"""Streaming proof (need 86f2d64a): `/generate` sends each token over SSE as it is generated.

Starts `faber run --device <device> --library-home <home> <inferentia> -- serve
--backend metal --model <F32> --port <free>`, waits for /health to report ready,
then makes one SSE request over a raw socket and timestamps the arrival of every
SSE event (time.monotonic at the recv that completed the event). The server is
streaming only if the token events are spread over time, one decode step apart,
and the first token arrives before generation finishes:

  * the token ids equal the ids in the `done` event (nothing lost or reordered);
  * with N token events, the last token arrives at least (N - 1) * MIN_STEP_S
    after the first (a batch-then-send server delivers all N inside one burst,
    well under a millisecond);
  * the first token arrives at least (N - 1) * MIN_STEP_S before the `done` event
    (generation had not finished when the first token was already on the wire).

MIN_STEP_S is a floor of 5 ms per decode step. A real step takes tens of
milliseconds on Metal and far more on `--device reference` (one core), so the floor
is deterministic, not a tuning knob.

    a1_stream_test.py --selftest
    a1_stream_test.py --faber <faber> --device reference [--library-home <dir>] \
        [--package <inferentia dir>] [--model <F32 gguf>] [--max-tokens 3]

`--selftest` needs no model: it feeds the chunk/event parser and the timing
verdict synthetic streams (a streamed one and a batched one).
"""
import argparse
import json
import os
import socket
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
PACKAGE = os.path.abspath(os.path.join(HERE, "..", ".."))
DEFAULT_MODEL = "/Users/ianzepp/ai/models/SmolLM2-360M-Instruct-f32.gguf"
DEFAULT_LIBRARY_HOME = os.path.abspath(os.path.join(PACKAGE, ".."))
MIN_STEP_S = 0.005
# A one-token prompt keeps prefill to a single step (each step is a full 32-layer pass,
# minutes per step on `--device reference`); max_tokens 3 is the least that shows spread.
DEFAULT_PROMPT = "Hello"


# ---------------------------------------------------------------------------
# Pure parts (covered by --selftest)
# ---------------------------------------------------------------------------

class SseReader:
    """Incremental parser: raw bytes of a chunked text/event-stream response in,
    (arrival time, event name, data) out. Time is supplied by the caller per feed."""

    def __init__(self):
        self.buf = b""
        self.in_body = False
        self.head = b""
        self.text = ""
        self.finished = False
        self.events = []

    def feed(self, data, now):
        self.buf += data
        if not self.in_body:
            i = self.buf.find(b"\r\n\r\n")
            if i < 0:
                return
            self.head = self.buf[:i]
            self.buf = self.buf[i + 4:]
            self.in_body = True
        while not self.finished:
            j = self.buf.find(b"\r\n")
            if j < 0:
                break
            size = int(self.buf[:j].split(b";")[0], 16)
            if len(self.buf) < j + 2 + size + 2:
                break
            payload = self.buf[j + 2:j + 2 + size]
            self.buf = self.buf[j + 2 + size + 2:]
            if size == 0:
                self.finished = True
                break
            self.text += payload.decode()
            while "\n\n" in self.text:
                block, self.text = self.text.split("\n\n", 1)
                name, datas = "message", []
                for ln in block.split("\n"):
                    if ln.startswith("event:"):
                        name = ln[6:].strip()
                    elif ln.startswith("data:"):
                        datas.append(ln[5:].lstrip())
                self.events.append((now, name, "\n".join(datas)))


def verdict(events):
    """(ok, detail) for a list of (time, name, data) events of one streamed /generate."""
    toks = [(t, d) for t, n, d in events if n == "token"]
    done = [(t, d) for t, n, d in events if n == "done"]
    errors = [d for t, n, d in events if n == "error"]
    if errors:
        return False, "error event: %s" % errors[0]
    if len(done) != 1:
        return False, "expected one done event, saw %d" % len(done)
    n = len(toks)
    if n < 3:
        return False, "only %d token events; need at least 3 to observe streaming" % n
    ids = [int(d) for t, d in toks]
    body = json.loads(done[0][1])
    if body.get("tokens") != ids:
        return False, "token events %s differ from done ids %s" % (ids, body.get("tokens"))
    floor = (n - 1) * MIN_STEP_S
    t_first, t_last, t_done = toks[0][0], toks[-1][0], done[0][0]
    spread = t_last - t_first
    lead = t_done - t_first
    detail = "%d tokens; first->last %.3fs, first->done %.3fs (floor %.3fs)" % (n, spread, lead, floor)
    if spread < floor:
        return False, "token events arrived in one burst: " + detail
    if lead < floor:
        return False, "first token not ahead of the end of generation: " + detail
    return True, detail


def encode_chunks(parts):
    out = b""
    for p in parts:
        out += b"%x\r\n" % len(p) + p + b"\r\n"
    return out + b"0\r\n\r\n"


def selftest():
    head = b"HTTP/1.1 200 OK\r\ntransfer-encoding: chunked\r\ncontent-type: text/event-stream\r\n\r\n"
    ev = lambda name, data: ("event: %s\ndata: %s\n\n" % (name, data)).encode()
    done = json.dumps({"tokens": [5, 6, 7, 8]}).encode()
    parts = [ev("token", 5), ev("token", 6), ev("token", 7), ev("token", 8), ev("done", done.decode())]
    wire = head + encode_chunks(parts)

    # streamed: each chunk arrives 0.05 s after the last; split mid-frame to prove buffering
    r = SseReader()
    t = 100.0
    r.feed(head, t)
    for p in parts:
        frame = encode_chunks([p])[:-5]
        cut = len(frame) // 2
        r.feed(frame[:cut], t)
        t += 0.05
        r.feed(frame[cut:], t)
    r.feed(b"0\r\n\r\n", t)
    ok, detail = verdict(r.events)
    assert r.finished and len(r.events) == 5, (r.finished, r.events)
    assert ok, detail

    # batched: the whole wire in one recv
    r = SseReader()
    r.feed(wire, 200.0)
    ok, detail = verdict(r.events)
    assert len(r.events) == 5 and not ok and "one burst" in detail, (ok, detail)

    # tokens spread out but `done` right behind the last token still passes only on spread+lead;
    # tokens in a burst followed by a late done must fail the lead/spread check
    r = SseReader()
    r.feed(head, 300.0)
    for p in parts[:4]:
        r.feed(encode_chunks([p])[:-5], 300.0)
    r.feed(encode_chunks([parts[4]])[:-5], 305.0)
    ok, detail = verdict(r.events)
    assert not ok and "one burst" in detail, (ok, detail)

    # wrong ids fail
    bad = list(parts)
    bad[4] = ev("done", json.dumps({"tokens": [5, 6, 7, 9]}))
    r = SseReader()
    r.feed(head, 0.0)
    t = 0.0
    for p in bad:
        t += 0.05
        r.feed(encode_chunks([p])[:-5], t)
    ok, detail = verdict(r.events)
    assert not ok and "differ" in detail, (ok, detail)
    print("selftest PASS")


# ---------------------------------------------------------------------------
# Live run
# ---------------------------------------------------------------------------

def free_port():
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()
    return port


def http_get(port, path, timeout=5):
    s = socket.create_connection(("127.0.0.1", port), timeout=timeout)
    s.sendall(("GET %s HTTP/1.1\r\nHost: x\r\nConnection: close\r\n\r\n" % path).encode())
    data = b""
    while True:
        b = s.recv(65536)
        if not b:
            break
        data += b
    s.close()
    head, _, body = data.partition(b"\r\n\r\n")
    return int(head.split()[1]), body.decode()


def stream_events(port, body, timeout):
    """POST /generate with Accept: text/event-stream; (status line, header, events)."""
    payload = json.dumps(body).encode()
    s = socket.create_connection(("127.0.0.1", port), timeout=timeout)
    s.sendall(("POST /generate HTTP/1.1\r\nHost: x\r\nContent-Type: application/json\r\n"
               "Accept: text/event-stream\r\nConnection: close\r\nContent-Length: %d\r\n\r\n" % len(payload)).encode() + payload)
    reader = SseReader()
    t0 = time.monotonic()
    seen = 0
    while not reader.finished:
        b = s.recv(65536)
        now = time.monotonic()
        if not b:
            break
        reader.feed(b, now)
        for t, n, d in reader.events[seen:]:
            print("  t=%8.3fs  %-5s %s" % (t - t0, n, d if n == "token" else d[:60]), flush=True)
        seen = len(reader.events)
    s.close()
    return reader.head.decode(), [(t - t0, n, d) for t, n, d in reader.events]


def live(a):
    port = free_port()
    cmd = [a.faber, "run", "--device", a.device, "--library-home", a.library_home, a.package, "--",
           "serve", "--backend", "metal", "--model", a.model, "--port", str(port)]
    log = open(a.log, "w") if a.log else subprocess.DEVNULL
    t0 = time.time()
    srv = subprocess.Popen(cmd, stdout=log, stderr=subprocess.STDOUT)
    try:
        state = None
        while time.time() - t0 < a.ready_timeout:
            if srv.poll() is not None:
                sys.exit("server exited early rc=%s" % srv.returncode)
            try:
                code, body = http_get(port, "/health")
                state = json.loads(body).get("state")
                if state in ("ready", "failed"):
                    break
            except Exception:
                pass
            time.sleep(2)
        print("health after %.1fs: state=%s" % (time.time() - t0, state))
        if state != "ready":
            sys.exit("server not ready")
        t1 = time.time()
        head, events = stream_events(port, {"prompt": a.prompt, "max_tokens": a.max_tokens}, a.request_timeout)
        print("SSE response head:", head.splitlines()[0], "| content-type event-stream:", "text/event-stream" in head)
        print("request took %.1fs" % (time.time() - t1))
        ok, detail = verdict(events)
        print("STREAM %s %s" % ("PASS" if ok else "FAIL", detail))
        return 0 if ok else 1
    finally:
        srv.terminate()
        try:
            srv.wait(timeout=10)
        except subprocess.TimeoutExpired:
            srv.kill()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--faber")
    ap.add_argument("--device", default="reference", help="reference | cpu | metal")
    ap.add_argument("--package", default=PACKAGE)
    ap.add_argument("--library-home", default=DEFAULT_LIBRARY_HOME,
                    help="directory holding the gradus checkout (<home>/gradus/src)")
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--prompt", default=DEFAULT_PROMPT)
    ap.add_argument("--max-tokens", type=int, default=3)
    ap.add_argument("--ready-timeout", type=float, default=900.0)
    ap.add_argument("--request-timeout", type=float, default=900.0)
    ap.add_argument("--log", default=None, help="server stdout/stderr log path")
    a = ap.parse_args()
    if a.selftest:
        selftest()
        return
    if not a.faber:
        ap.error("--faber is required unless --selftest")
    sys.exit(live(a))


if __name__ == "__main__":
    main()
