"""test_ck_code_writer.py -- regression tests for the code-writer.

What we test:
  T1 -- list_templates returns the 8 registered templates with proper shape
  T2 -- read_file request hits the read_file template
  T3 -- write_jsonl request hits write_jsonl
  T4 -- flask_endpoint accepts route/method params
  T5 -- pytest_skeleton accepts target name
  T6 -- bash_script returns bash-tagged result
  T7 -- unknown request without LLM returns TIER_UNAVAILABLE
  T8 -- LLM-relay path: if relay returns a string, output tagged TIER_LLM_RELAYED
  T9 -- LLM-relay + auditor: violation triggers TIER_REFUSED
  T10 -- generated code compiles (syntactically valid Python for python-tier results)
"""
from __future__ import annotations

import ast
import sys
from pathlib import Path

HERE = Path(__file__).parent.resolve()
sys.path.insert(0, str(HERE))

from ck_code_writer import (  # noqa: E402
    TIER_LLM_RELAYED,
    TIER_REFUSED,
    TIER_TEMPLATE,
    TIER_UNAVAILABLE,
    list_templates,
    write_code,
)


def test_list_templates_shape():
    tpls = list_templates()
    assert len(tpls) == 8, f"expected 8 templates, got {len(tpls)}"
    for t in tpls:
        for k in ("template_id", "triggers", "description"):
            assert k in t, f"template missing key: {k}"
        assert t["template_id"]
        assert t["triggers"]
        assert t["description"]
    print(f"T1 PASS: list_templates returned {len(tpls)} templates with correct shape")


def test_read_file_match():
    r = write_code("read a text file please", params={"path": "/tmp/x"})
    assert r.tier == TIER_TEMPLATE
    assert r.template_id == "read_file"
    assert "/tmp/x" in r.code
    print("T2 PASS: read_file template matches and uses params")


def test_write_jsonl_match():
    r = write_code("write to a jsonl log", params={"path": "log.jsonl"})
    assert r.tier == TIER_TEMPLATE
    assert r.template_id == "write_jsonl"
    assert "log.jsonl" in r.code
    print("T3 PASS: write_jsonl template matches and uses params")


def test_flask_endpoint_params():
    r = write_code("flask endpoint please",
                    params={"route": "/api/foo", "method": "POST",
                            "name": "foo_handler"})
    assert r.tier == TIER_TEMPLATE
    assert r.template_id == "flask_endpoint"
    assert "/api/foo" in r.code
    assert "POST" in r.code
    assert "foo_handler" in r.code
    print("T4 PASS: flask_endpoint accepts route/method/name params")


def test_pytest_skeleton_param():
    r = write_code("pytest test skeleton", params={"target": "ck_pc_sense"})
    assert r.tier == TIER_TEMPLATE
    assert r.template_id == "pytest_skeleton"
    assert "ck_pc_sense" in r.code
    assert "NotImplementedError" in r.code  # the explicit RED marker
    print("T5 PASS: pytest_skeleton accepts target + emits RED-marker")


def test_bash_language():
    r = write_code("bash script", params={"name": "deploy"})
    assert r.tier == TIER_TEMPLATE
    assert r.language == "bash"
    assert r.template_id == "bash_script"
    assert "set -euo pipefail" in r.code
    print("T6 PASS: bash_script is language=bash with strict-mode flags")


def test_no_template_no_llm():
    r = write_code("translate this Greek poem")
    assert r.tier == TIER_UNAVAILABLE
    assert "No template matches" in r.explanation
    assert "llm_relay" in r.explanation
    print("T7 PASS: no template + no LLM = TIER_UNAVAILABLE with helpful message")


def test_llm_relay_path():
    """LLM relay returns a string; result is tagged TIER_LLM_RELAYED."""
    def fake_llm(prompt: str) -> str:
        return "def hello():\n    return 'world'"

    r = write_code("fancy custom thing", llm_relay=fake_llm)
    assert r.tier == TIER_LLM_RELAYED
    assert "def hello" in r.code
    assert "Human review required" in r.explanation
    assert len(r.review_notes) >= 2  # hallucinate warnings
    print("T8 PASS: LLM-relay output tagged TIER_LLM_RELAYED with review warnings")


def test_llm_with_auditor_violation():
    """LLM output that fails auditor -> TIER_REFUSED."""
    def fake_llm(prompt: str) -> str:
        return "# the substrate is a torus"  # would fail TORUS auditor rule

    def fake_auditor(text: str):
        if "torus" in text.lower():
            return {"passed": False, "violations": ["TORUS_RULE: 'torus' phrase"]}
        return {"passed": True, "violations": []}

    r = write_code("anything", llm_relay=fake_llm, auditor=fake_auditor)
    assert r.tier == TIER_REFUSED
    assert "TORUS_RULE" in r.explanation
    print("T9 PASS: auditor violation triggers TIER_REFUSED")


def test_generated_code_compiles():
    """Every python-language template should produce syntactically valid Python."""
    requests = [
        ("read a file",        {"path": "x"}),
        ("write jsonl",        {"path": "x.jsonl"}),
        ("flask endpoint",     {}),
        ("csv read",           {}),
        ("argparse script",    {"name": "tool"}),
        ("pytest test",        {"target": "thing"}),
        ("dataclass please",   {"name": "Point", "fields": "x: int, y: int"}),
    ]
    for req, params in requests:
        r = write_code(req, params=params)
        if r.language != "python":
            continue
        try:
            ast.parse(r.code)
        except SyntaxError as e:
            raise AssertionError(
                f"template {r.template_id!r} produced invalid Python: {e}"
            )
    print(f"T10 PASS: all 7 python templates produce syntactically valid Python")


def run_all():
    print("=" * 64)
    print("ck_code_writer regression tests")
    print("=" * 64)
    print()
    tests = [
        test_list_templates_shape,
        test_read_file_match,
        test_write_jsonl_match,
        test_flask_endpoint_params,
        test_pytest_skeleton_param,
        test_bash_language,
        test_no_template_no_llm,
        test_llm_relay_path,
        test_llm_with_auditor_violation,
        test_generated_code_compiles,
    ]
    n_pass = 0
    n_fail = 0
    for t in tests:
        try:
            t()
            n_pass += 1
        except AssertionError as e:
            print(f"  {t.__name__} FAIL: {e}")
            n_fail += 1
        except Exception as e:
            print(f"  {t.__name__} ERROR: {type(e).__name__}: {e}")
            n_fail += 1
    print()
    print("=" * 64)
    print(f"RESULT: {n_pass}/{len(tests)} tests passed")
    print("=" * 64)
    return n_fail == 0


if __name__ == "__main__":
    ok = run_all()
    sys.exit(0 if ok else 1)
