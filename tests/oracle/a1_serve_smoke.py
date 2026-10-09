#!/usr/bin/env python3.13
"""A1 serve smoke: `inferentia serve --backend metal` over HTTP against the references.

Starts `faber run --device metal <inferentia> -- inferentia serve --backend metal
--model <F32> --port <free>`, waits for /health to report ready, checks /health
and /model (backend must read "metal"), POSTs the two reference prompts to
/generate and compares the returned token ids with the references through the
same near-tie logic as a1_oracle.py, then makes one SSE request (Accept:
text/event-stream) and checks the streamed token events equal the JSON ids.

The response carries no logits, so the near-tie context (our top-two logits at
the mismatch step) is taken from a previous oracle run's results JSON
(`--live-results`, written by `a1_oracle.py --out`); without it a mismatch is a
plain FAIL.

    FABER_LIBRARY_HOME=<container root> a1_serve_smoke.py --faber <release faber> \
        [--live-results results.json] [--cases eog,continuation] [--ready-timeout 400] \
        [--no-sampling] [--log serve.log]

After the greedy cases, the same server session runs the seeded sampling cases
(metal-sampling-design.md section 6, items 3 and 4) on the continuation prompt with
max_tokens 32: the same seed twice gives identical ids, a different seed gives
different ids, a full-logits-fallback setting (top_k 0) twice gives identical ids,
top_k 1 at temperature 0.8 and temperature 1e-6 both equal the greedy ids.

Then the cpu-vs-Metal agreement case (design note section 6 item 5): the Metal session
serves {"temperature": 0.8, "top_k": 8, "top_p": 0.95, "seed": 7} on the continuation
prompt with max_tokens 16; the Metal server is stopped, a `--backend cpu` server is
started (no --device) and serves the same request. The two id lists must be equal; at
the first differing step the near-tie rule (a1_oracle.near_tie_bound) is applied only
when both servers' sampled prefix equals the greedy reference prefix, so the reference
top-two logprob gap at that step is a valid context. The response carries no logits,
so a sampled divergence has no our-logit magnitude M: with the reference gap g it is
accepted only if g <= near_tie_bound(0), else it is a FAIL with both id lists. The
agreed prefix length is printed. The case is OFF by default: on SmolLM2-360M f32
the `--backend cpu` server (host NumericBlock path) had not answered /health after
300 s (need 3f1b26bd S-10, 2026-10-09), so no agreed prefix has been measured.
`--cpu-agreement` turns it on, `--cpu-ready-timeout` bounds the cpu server start.
"""
import argparse
import json
import os
import socket
import subprocess
import sys
import time
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import a1_oracle as oracle  # noqa: E402


def free_port():
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()
    return port


def get(url, timeout=30):
    with urllib.request.urlopen(url, timeout=timeout) as r:
        return r.status, r.read().decode()


def post(url, body, accept=None, timeout=600):
    req = urllib.request.Request(url, data=json.dumps(body).encode(), method="POST")
    req.add_header("content-type", "application/json")
    if accept:
        req.add_header("accept", accept)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.status, r.read().decode()


def sse_tokens(raw):
    toks, done = [], None
    event = None
    for ln in raw.splitlines():
        if ln.startswith("event:"):
            event = ln[6:].strip()
        elif ln.startswith("data:"):
            data = ln[5:].strip()
            if event == "token":
                toks.append(int(data))
            elif event == "done":
                done = json.loads(data)
    return toks, done


SAMPLING_MAX_TOKENS = 32
AGREEMENT_MAX_TOKENS = 16
AGREEMENT_REQUEST = {"temperature": 0.8, "top_k": 8, "top_p": 0.95, "seed": 7}


def sample_request(base, prompt, label, extra, a):
    """POST one /generate with sampling fields; returns the parsed response."""
    body = {"prompt": prompt, "max_tokens": SAMPLING_MAX_TOKENS}
    body.update(extra)
    t = time.time()
    code, raw = post(base + "/generate", body, timeout=a.request_timeout)
    resp = json.loads(raw)
    print("POST /generate %-22s -> %d  %.1fs  ids=%s" % (label, code, time.time() - t, resp["tokens"]))
    return resp["tokens"]


def agreement_request(base, a, label):
    """The cpu-vs-Metal agreement request: returns (ids, prompt, reference)."""
    ref = json.load(open(os.path.join(a.refs, oracle.CASES["continuation"])))
    body = dict(AGREEMENT_REQUEST, prompt=ref["prompt"], max_tokens=AGREEMENT_MAX_TOKENS)
    t = time.time()
    code, raw = post(base + "/generate", body, timeout=a.request_timeout)
    ids = json.loads(raw)["tokens"]
    print("POST /generate %-22s -> %d  %.1fs  ids=%s" % (label, code, time.time() - t, ids))
    return ids, ref


def agreement_verdict(metal_ids, cpu_ids, ref):
    """-> (ok, detail) for the cpu-vs-Metal agreement; reports the agreed prefix length."""
    n = min(len(metal_ids), len(cpu_ids))
    k = next((i for i in range(n) if metal_ids[i] != cpu_ids[i]), n)
    if k == n and len(metal_ids) == len(cpu_ids):
        return True, "all %d ids equal" % k
    lists = "metal=%s cpu=%s" % (metal_ids, cpu_ids)
    if k == n:
        return False, "length differs after %d equal ids: %s" % (k, lists)
    want = ref["generated_token_ids"]
    if metal_ids[:k] == want[:k] and cpu_ids[:k] == want[:k]:
        top2 = ref["per_step_top2_logprobs"][k]
        g = top2[0]["logprob"] - top2[1]["logprob"]
        if g <= oracle.near_tie_bound(0.0):
            return True, "near-tie at step %d (reference g=%.3e): agreed prefix %d, %s" % (k, g, k, lists)
        return False, "first divergence at step %d, reference g=%.3e is not a near tie: %s" % (k, g, lists)
    return False, "first divergence at step %d (agreed prefix %d), prefix is off the greedy reference so no near-tie context: %s" % (k, k, lists)


def start_server(a, backend, log_path):
    """Start one inferentia server; returns (proc, base, port-ready seconds or None)."""
    port = free_port()
    base = "http://127.0.0.1:%d" % port
    dev = ["--device", "metal"] if backend == "metal" else []
    cmd = [a.faber, "run"] + dev + [a.package, "--", "inferentia", "serve",
           "--backend", backend, "--model", a.model, "--port", str(port)]
    log = open(log_path, "w")
    t0 = time.time()
    srv = subprocess.Popen(cmd, stdout=log, stderr=subprocess.STDOUT)
    return srv, base, t0


def stop_server(srv):
    srv.terminate()
    try:
        srv.wait(timeout=10)
    except subprocess.TimeoutExpired:
        srv.kill()


def cpu_agreement(a, metal_ids, ref):
    """Start a cpu server, serve the agreement request, kill it; -> failures."""
    log_path = (a.log + ".cpu") if a.log else "/dev/null"
    srv, base, t0 = start_server(a, "cpu", log_path)
    try:
        state = None
        while time.time() - t0 < a.cpu_ready_timeout:
            if srv.poll() is not None:
                return ["cpu agreement: cpu server exited early rc=%s" % srv.returncode]
            try:
                code, body = get(base + "/health", timeout=5)
                state = json.loads(body).get("state")
                if state in ("ready", "failed"):
                    break
            except Exception:
                pass
            time.sleep(2)
        print("cpu health after %.1fs: state=%s" % (time.time() - t0, state))
        if state != "ready":
            return ["cpu agreement: cpu server not ready within %.0fs (state=%s)" % (a.cpu_ready_timeout, state)]
        code, body = get(base + "/model")
        if json.loads(body).get("backend") != "cpu":
            return ["cpu agreement: /model backend is not cpu"]
        cpu_ids, _ = agreement_request(base, a, "cpu seed7 candidates")
        ok, detail = agreement_verdict(metal_ids, cpu_ids, ref)
        print("SAMPLING %-34s %s  %s" % ("cpu vs metal agreement", "PASS" if ok else "FAIL", detail))
        return [] if ok else ["cpu agreement: " + detail]
    finally:
        stop_server(srv)


def sampling_cases(base, a):
    """Seeded sampling proof (metal-sampling-design.md section 6, items 3 and 4)."""
    ref = json.load(open(os.path.join(a.refs, oracle.CASES["continuation"])))
    prompt = ref["prompt"]
    failures = []

    def verdict(name, ok, detail):
        print("SAMPLING %-34s %s  %s" % (name, "PASS" if ok else "FAIL", detail))
        if not ok:
            failures.append("sampling %s: %s" % (name, detail))

    cand = {"temperature": 0.8, "top_k": 8, "top_p": 0.95}
    greedy = sample_request(base, prompt, "greedy", {}, a)
    ref_prefix = ref["generated_token_ids"][:SAMPLING_MAX_TOKENS]
    verdict("greedy32 == reference prefix", greedy == ref_prefix,
            "server greedy %d ids vs reference first %d" % (len(greedy), len(ref_prefix)))

    s7a = sample_request(base, prompt, "seed7 candidates #1", dict(cand, seed=7), a)
    s7b = sample_request(base, prompt, "seed7 candidates #2", dict(cand, seed=7), a)
    verdict("seed 7 twice identical", s7a == s7b, "equal" if s7a == s7b else "run1=%s run2=%s" % (s7a, s7b))
    s8 = sample_request(base, prompt, "seed8 candidates", dict(cand, seed=8), a)
    verdict("seed 8 differs from seed 7", s8 != s7a, "differ" if s8 != s7a else "identical ids %s" % s8)

    fb = {"temperature": 0.8, "top_k": 0, "top_p": 1.0, "seed": 7}
    fa = sample_request(base, prompt, "seed7 fallback #1", fb, a)
    fb2 = sample_request(base, prompt, "seed7 fallback #2", fb, a)
    verdict("fallback seed 7 twice identical", fa == fb2, "equal" if fa == fb2 else "run1=%s run2=%s" % (fa, fb2))
    # identical-but-degenerate (a lone end-of-text id) is not a repeatability proof
    verdict("fallback is a real continuation", len(fa) >= 2, "%d ids %s" % (len(fa), fa))

    k1 = sample_request(base, prompt, "top_k 1 temp 0.8", {"temperature": 0.8, "top_k": 1, "seed": 7}, a)
    verdict("top_k 1 at temp 0.8 == greedy", k1 == greedy, "equal" if k1 == greedy else "sampled=%s greedy=%s" % (k1, greedy))
    t0 = sample_request(base, prompt, "temp 1e-6", {"temperature": 1e-6, "seed": 7}, a)
    verdict("temperature 1e-6 == greedy", t0 == greedy, "equal" if t0 == greedy else "sampled=%s greedy=%s" % (t0, greedy))
    return failures


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--faber", required=True)
    ap.add_argument("--package", default=oracle.PACKAGE)
    ap.add_argument("--model", default=oracle.DEFAULT_MODEL)
    ap.add_argument("--refs", default=oracle.DEFAULT_REFS)
    ap.add_argument("--cases", default="eog,continuation")
    ap.add_argument("--live-results", default=None)
    ap.add_argument("--ready-timeout", type=float, default=400.0)
    ap.add_argument("--request-timeout", type=float, default=400.0)
    ap.add_argument("--no-sampling", action="store_true", help="skip the seeded sampling cases")
    ap.add_argument("--log", default=None, help="server stdout/stderr log path")
    ap.add_argument("--cpu-agreement", action="store_true", help="run the cpu-vs-Metal agreement case (off by default: the cpu server start exceeds 300 s)")
    ap.add_argument("--cpu-ready-timeout", type=float, default=300.0)
    a = ap.parse_args()
    if "FABER_LIBRARY_HOME" not in os.environ:
        sys.exit("set FABER_LIBRARY_HOME to the container root")
    live = json.load(open(a.live_results)) if a.live_results else {}

    port = free_port()
    base = "http://127.0.0.1:%d" % port
    cmd = [a.faber, "run", "--device", "metal", a.package, "--", "inferentia", "serve",
           "--backend", "metal", "--model", a.model, "--port", str(port)]
    log_path = a.log or (os.path.join(os.path.dirname(a.live_results), "serve.log") if a.live_results else "/dev/null")
    log = open(log_path, "w")
    t0 = time.time()
    srv = subprocess.Popen(cmd, stdout=log, stderr=subprocess.STDOUT)
    failures = []
    metal_ids, agree_ref = None, None
    try:
        state = None
        while time.time() - t0 < a.ready_timeout:
            if srv.poll() is not None:
                sys.exit("server exited early rc=%s" % srv.returncode)
            try:
                code, body = get(base + "/health", timeout=5)
                state = json.loads(body).get("state")
                if state in ("ready", "failed"):
                    break
            except Exception:
                pass
            time.sleep(2)
        print("health after %.1fs: state=%s" % (time.time() - t0, state))
        code, body = get(base + "/health")
        print("GET /health ->", code, body)
        code, body = get(base + "/model")
        print("GET /model  ->", code, body)
        if json.loads(body).get("backend") != "metal":
            failures.append("/model backend is not metal")
        want = open(os.path.join(oracle.PACKAGE, "tests", "model-gate", "expected-model-body-metal.json")).read().strip()
        if body.strip() != want:
            failures.append("/model body differs from tests/model-gate/expected-model-body-metal.json")
        if state != "ready":
            failures.append("server not ready")

        for name in a.cases.split(","):
            if state != "ready":
                break
            ref = json.load(open(os.path.join(a.refs, oracle.CASES[name])))
            max_tokens = len(ref["generated_token_ids"]) if ref["finish_reason"] == "length" else 32
            t1 = time.time()
            code, body = post(base + "/generate", {"prompt": ref["prompt"], "max_tokens": max_tokens},
                              timeout=a.request_timeout)
            dt = time.time() - t1
            resp = json.loads(body)
            ids = resp["tokens"]
            finish = {"eos": "stop"}.get(resp["finish_reason"], resp["finish_reason"])
            traces = {int(k): tuple(v) for k, v in live.get(name, {}).get("traces", {}).items()}
            verdict, detail = oracle.compare(ref, resp.get("prompt_ids", ref["prompt_token_ids"]), ids, finish, traces)
            # the response has no prompt ids; usage.prompt_tokens must match
            if resp["usage"]["prompt_tokens"] != len(ref["prompt_token_ids"]):
                verdict, detail = "FAIL", "prompt_tokens %s != %d" % (resp["usage"]["prompt_tokens"], len(ref["prompt_token_ids"]))
            same_as_live = ""
            if name in live and live[name].get("ids") is not None:
                same_as_live = " live-equal=%s" % (live[name]["ids"] == ids)
            print("POST /generate %-12s -> %d  %.1fs  %s  %s%s" % (name, code, dt, verdict, detail, same_as_live))
            if not verdict.startswith("PASS"):
                failures.append("%s: %s" % (name, detail))

            if name == "eog" or name == a.cases.split(",")[0]:
                t2 = time.time()
                code, raw = post(base + "/generate", {"prompt": ref["prompt"], "max_tokens": max_tokens},
                                 accept="text/event-stream", timeout=a.request_timeout)
                toks, done = sse_tokens(raw)
                ok = toks == ids and done is not None and done.get("tokens") == ids
                print("POST /generate (SSE) %-6s -> %d  %.1fs  token events=%d done=%s ids-equal=%s" % (
                    name, code, time.time() - t2, len(toks), done is not None, ok))
                if not ok:
                    failures.append("SSE ids differ from JSON ids for %s" % name)

        if state == "ready" and not a.no_sampling:
            failures.extend(sampling_cases(base, a))
        if state == "ready" and not a.no_sampling and a.cpu_agreement:
            metal_ids, agree_ref = agreement_request(base, a, "metal seed7 candidates")
    finally:
        stop_server(srv)
    if metal_ids is not None:
        failures.extend(cpu_agreement(a, metal_ids, agree_ref))
    print("SMOKE:", "PASS" if not failures else "FAIL " + "; ".join(failures))
    sys.exit(0 if not failures else 1)


if __name__ == "__main__":
    main()
