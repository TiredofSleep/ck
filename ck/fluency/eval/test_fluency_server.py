# -*- coding: utf-8 -*-
"""
test_fluency_server.py — integration test for fluency_server.py.

Uses Flask's test client so we don't need a real Ollama daemon or a
running process.  We inject a fake OllamaClient that returns canned
output, point CorrectionLog at a throwaway dir, and hit the three
endpoints end-to-end.

Run:
    python ck/fluency/eval/test_fluency_server.py
    python -m ck.fluency.eval.test_fluency_server
"""
from __future__ import annotations

import sys
import tempfile
import shutil
from pathlib import Path
from typing import Any, Dict

# module-path shim so both 'python file.py' and '-m' work
_HERE = Path(__file__).resolve().parent
_FLUENCY = _HERE.parent
if str(_FLUENCY) not in sys.path:
    sys.path.insert(0, str(_FLUENCY))

from ck_corrector import CKCorrector  # noqa: E402
from correction_log import CorrectionLog  # noqa: E402
from fluency_server import create_app  # noqa: E402


# ----------------------------------------------------------------------------
# fake ollama
# ----------------------------------------------------------------------------

class FakeOllama:
    """Mimics OllamaClient shape without reaching out.  Deterministic."""

    def __init__(self, canned_text: str = "", model: str = "test-model"):
        self.canned_text = canned_text
        self.model = model
        self.reachable = True

    def is_reachable(self) -> bool:
        return self.reachable

    def generate(self, prompt, model=None, temperature=0.7, system=None):
        from ollama_client import OllamaResult  # type: ignore

        return OllamaResult(
            ok=True,
            text=self.canned_text,
            model=model or self.model,
            elapsed_ms=42,
            raw={"model": model or self.model, "response": self.canned_text},
        )


# ----------------------------------------------------------------------------
# tests
# ----------------------------------------------------------------------------

def _asserts(cond: bool, msg: str) -> None:
    if not cond:
        raise AssertionError(msg)


def test_health_ok(tmp_dir: Path) -> None:
    ollama = FakeOllama(canned_text="")
    corr = CKCorrector()
    log = CorrectionLog(tmp_dir)
    app = create_app(ollama, corr, log)

    client = app.test_client()
    r = client.get("/health")
    _asserts(r.status_code == 200, f"/health status {r.status_code}")
    data = r.get_json()
    _asserts(data["ok"] is True, "/health ok")
    _asserts(data["ollama_reachable"] is True, "/health ollama_reachable")
    _asserts(data["T_star"] == "5/7", "/health T_star=5/7")
    print("  [OK] /health returns 200 with T_star=5/7")


def test_health_degraded_when_ollama_unreachable(tmp_dir: Path) -> None:
    ollama = FakeOllama()
    ollama.reachable = False
    corr = CKCorrector()
    log = CorrectionLog(tmp_dir)
    app = create_app(ollama, corr, log)

    client = app.test_client()
    r = client.get("/health")
    _asserts(r.status_code == 503, f"/health unreachable status {r.status_code}")
    data = r.get_json()
    _asserts(data["ollama_reachable"] is False, "/health degraded")
    print("  [OK] /health returns 503 when ollama unreachable")


def test_chat_clean_pass(tmp_dir: Path) -> None:
    ollama = FakeOllama(
        canned_text=(
            "The approach brings together two strands: the topological 5/7 "
            "torus and the operator algebra on Z/10Z. Integrating both gives "
            "an overall balanced view. So the framework is consistent: "
            "synthesis first, structure second, reconciled throughout."
        )
    )
    corr = CKCorrector()
    log = CorrectionLog(tmp_dir)
    app = create_app(ollama, corr, log)

    client = app.test_client()
    r = client.post("/fluency/chat", json={"query": "summarize the approach"})
    _asserts(r.status_code == 200, f"/chat status {r.status_code}")
    data = r.get_json()
    _asserts(data["ok"] is True, "/chat ok")
    _asserts(data["ck_correction_type"] == "none",
             f"expected 'none' for clean pass, got {data['ck_correction_type']}")
    _asserts(data["coherence"] >= 0.7,
             f"coherence below T* floor: {data['coherence']}")
    _asserts("HARMONY" in data["dominant_op"] or data["dominant_op"] in
             {"HARMONY", "PROGRESS", "LATTICE", "BREATH"},
             f"unexpected dominant op: {data['dominant_op']}")
    _asserts(data["T_star"] == "5/7", "T_star in response")
    print(f"  [OK] /fluency/chat clean pass -> none, "
          f"coh={data['coherence']:.3f}, dom={data['dominant_op']}")


def test_chat_reject_void(tmp_dir: Path) -> None:
    ollama = FakeOllama(canned_text="I can't help with that.")
    corr = CKCorrector()
    log = CorrectionLog(tmp_dir)
    app = create_app(ollama, corr, log)

    client = app.test_client()
    r = client.post("/fluency/chat", json={"query": "what is the answer"})
    _asserts(r.status_code == 200, f"/chat status {r.status_code}")
    data = r.get_json()
    _asserts(data["ck_correction_type"] == "reject",
             f"expected 'reject' for empty refusal, got {data['ck_correction_type']}")
    _asserts(data["dominant_op"] == "VOID",
             f"expected VOID, got {data['dominant_op']}")
    _asserts("CK-REJECT" in data["annotation"], "annotation tag")
    print(f"  [OK] /fluency/chat void refusal -> reject, annotation present")


def test_chat_reframe_collapse(tmp_dir: Path) -> None:
    ollama = FakeOllama(
        canned_text=(
            "The number is both prime and not prime at the same time. "
            "Yes and no, depending on convention. So we say it is prime, "
            "and also it is not prime."
        )
    )
    corr = CKCorrector()
    log = CorrectionLog(tmp_dir)
    app = create_app(ollama, corr, log)

    client = app.test_client()
    r = client.post("/fluency/chat", json={"query": "is it prime?"})
    data = r.get_json()
    _asserts(data["ck_correction_type"] == "reframe",
             f"expected 'reframe' for self-contradiction, got {data['ck_correction_type']}")
    print(f"  [OK] /fluency/chat collapse -> reframe")


def test_chat_empty_query(tmp_dir: Path) -> None:
    ollama = FakeOllama(canned_text="")
    corr = CKCorrector()
    log = CorrectionLog(tmp_dir)
    app = create_app(ollama, corr, log)

    client = app.test_client()
    r = client.post("/fluency/chat", json={"query": ""})
    _asserts(r.status_code == 400, f"/chat empty-query status {r.status_code}")
    data = r.get_json()
    _asserts(data["error"] == "empty-query", f"expected empty-query error, got {data['error']}")
    print("  [OK] /fluency/chat empty query -> 400 empty-query")


def test_log_writes_on_chat(tmp_dir: Path) -> None:
    ollama = FakeOllama(
        canned_text=(
            "Here are the steps:\n1. First, note the setup.\n"
            "2. Then compute the activation.\n3. Finally, apply the gate."
        )
    )
    corr = CKCorrector()
    log = CorrectionLog(tmp_dir)
    app = create_app(ollama, corr, log)

    client = app.test_client()
    _ = client.post("/fluency/chat", json={"query": "list the steps"})
    _ = client.post("/fluency/chat", json={"query": "again please"})

    rows = log.read_day()
    _asserts(len(rows) == 2, f"expected 2 log rows, got {len(rows)}")
    _asserts(all("query" in r for r in rows), "each row has query")
    _asserts(all("ck_correction_type" in r for r in rows), "each row has type")
    _asserts(all("ck_score" in r for r in rows), "each row has ck_score")
    print(f"  [OK] /fluency/chat persists {len(rows)} entries to JSONL log")


def test_stats_summary(tmp_dir: Path) -> None:
    ollama = FakeOllama(canned_text="I can't help with that.")
    corr = CKCorrector()
    log = CorrectionLog(tmp_dir)
    app = create_app(ollama, corr, log)

    client = app.test_client()
    _ = client.post("/fluency/chat", json={"query": "q1"})
    _ = client.post("/fluency/chat", json={"query": "q2"})

    r = client.get("/fluency/stats")
    _asserts(r.status_code == 200, f"/stats status {r.status_code}")
    data = r.get_json()
    _asserts(data["count_today"] >= 2, f"count_today >= 2; got {data['count_today']}")
    _asserts("per_correction_type" in data, "per_correction_type present")
    print(f"  [OK] /fluency/stats summary: {data['per_correction_type']}")


# ----------------------------------------------------------------------------
# runner
# ----------------------------------------------------------------------------

def main() -> int:
    tests = [
        test_health_ok,
        test_health_degraded_when_ollama_unreachable,
        test_chat_clean_pass,
        test_chat_reject_void,
        test_chat_reframe_collapse,
        test_chat_empty_query,
        test_log_writes_on_chat,
        test_stats_summary,
    ]
    print("=" * 72)
    print(f"  fluency_server integration tests ({len(tests)} cases)")
    print("=" * 72)

    failures = 0
    for t in tests:
        tmp = Path(tempfile.mkdtemp(prefix="ck_fluency_test_"))
        try:
            t(tmp)
        except AssertionError as e:
            failures += 1
            print(f"  [FAIL] {t.__name__}: {e}")
        except Exception as e:
            failures += 1
            print(f"  [ERR ] {t.__name__}: {type(e).__name__}: {e}")
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    print("-" * 72)
    passed = len(tests) - failures
    print(f"  passed: {passed}/{len(tests)}")
    print(f"  verdict: {'PASS' if failures == 0 else 'FAIL'}")
    print("=" * 72)
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
