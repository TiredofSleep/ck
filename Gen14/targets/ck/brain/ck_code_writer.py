"""ck_code_writer.py -- CK can propose code with tier-tagged honesty.

CK Gen14 module — capability shim for "write me a function that X."
Designed around the project's MYTHDRIFT-discipline pattern: every
piece of generated code carries an explicit honesty tier so the user
knows what they're looking at.

═══════════════════════════════════════════════════════════════════
What this module DOES
═══════════════════════════════════════════════════════════════════

Two modes:

  1. **Template mode** (no LLM, deterministic, default):
     CK has a small registry of well-known code patterns (file I/O,
     CSV read/write, JSONL append, simple Flask endpoint, regex
     match, etc.).  When the user asks for one of these, CK emits
     the template with the requested parameters substituted, and
     tags the output as TIER_TEMPLATE (verified, deterministic).

  2. **LLM-relay mode** (opt-in, requires `engine.llm_polish` or
     Ollama/DeepSeek wrapper):
     For requests outside the template registry, CK can RELAY to
     an external LLM, but always with a thick honesty layer:
       - Output tagged TIER_LLM_RELAYED (not CK's own work).
       - Output passed through the scope auditor (catches torus,
         physics-prediction, etc.).
       - Output tagged with "needs human review" warning.

═══════════════════════════════════════════════════════════════════
What this module DOES NOT DO
═══════════════════════════════════════════════════════════════════

  - It does NOT execute the generated code (CK writes, user runs).
  - It does NOT write to disk without explicit `write_to` argument.
  - It does NOT claim the LLM-relayed output is CK's own thinking
    (every LLM-mode output is tagged as relayed, never as CK's).
  - It does NOT bypass the scope auditor — LLM output that mentions
    torus / physics-prediction / overclaim is flagged.

═══════════════════════════════════════════════════════════════════
Honest scope
═══════════════════════════════════════════════════════════════════

This is a small productivity primitive: lets CK be useful for
"write the boilerplate for X" tasks while staying honest about which
part is CK's own substrate-derived knowledge vs which part is a
relayed LLM suggestion the user should review.

The template registry is small by design (8-10 templates) and grows
only by Brayden adding patterns he actually uses.  Resisting feature
creep here is the discipline.
"""
from __future__ import annotations

import re
import time
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional


# ─── Tier labels ───────────────────────────────────────────────────

TIER_TEMPLATE = "TIER_TEMPLATE"        # Deterministic, verified template
TIER_LLM_RELAYED = "TIER_LLM_RELAYED"  # External LLM output (review needed)
TIER_UNAVAILABLE = "TIER_UNAVAILABLE"  # No template + no LLM available
TIER_REFUSED = "TIER_REFUSED"          # Auditor or policy blocked


@dataclass
class CodeWriteResult:
    """One code-write output with full provenance."""
    tier: str                          # TIER_TEMPLATE etc.
    language: str                      # python / bash / json / ...
    code: str                          # the actual code string
    explanation: str                   # one-paragraph what + how
    review_notes: List[str] = field(default_factory=list)
    template_id: Optional[str] = None  # if TIER_TEMPLATE
    request: Optional[str] = None      # what the user asked for
    ts: float = field(default_factory=time.time)


# ─── Template registry ─────────────────────────────────────────────
# Each template is a callable that takes a parameter dict and returns
# a CodeWriteResult.  Triggers are keywords the request must contain
# (case-insensitive) to match.

def _t_read_file(params: Dict[str, Any]) -> CodeWriteResult:
    path = params.get("path", "input.txt")
    encoding = params.get("encoding", "utf-8")
    return CodeWriteResult(
        tier=TIER_TEMPLATE,
        language="python",
        code=(
            f"from pathlib import Path\n"
            f"\n"
            f"with open({path!r}, encoding={encoding!r}) as f:\n"
            f"    contents = f.read()\n"
            f"print(f'read {{len(contents)}} chars from {{Path({path!r}).name}}')"
        ),
        explanation=(
            f"Read the entire contents of `{path}` as a UTF-8 string. "
            f"Uses `pathlib` for the basename printout. Safe default "
            f"for small files (<10 MB)."
        ),
        review_notes=[
            "for files > ~100 MB, use line-by-line iteration instead",
            "if the file might be binary, drop the `encoding=` argument",
        ],
        template_id="read_file",
    )


def _t_write_jsonl(params: Dict[str, Any]) -> CodeWriteResult:
    path = params.get("path", "out.jsonl")
    return CodeWriteResult(
        tier=TIER_TEMPLATE,
        language="python",
        code=(
            f"import json\n"
            f"from pathlib import Path\n"
            f"\n"
            f"def append_jsonl(record: dict, path: str = {path!r}) -> None:\n"
            f"    Path(path).parent.mkdir(parents=True, exist_ok=True)\n"
            f"    with open(path, 'a', encoding='utf-8') as f:\n"
            f"        f.write(json.dumps(record, ensure_ascii=False) + '\\n')"
        ),
        explanation=(
            f"Append a single dict as one JSONL line to `{path}`. "
            f"Creates parent directories if they don't exist. "
            f"Atomic per-line — safe for crash-recovery if interrupted."
        ),
        review_notes=[
            "for high-throughput writes, batch records and flush less often",
            "for concurrent writers, switch to `fcntl.flock` (POSIX) or "
            "use a queue + single writer thread",
        ],
        template_id="write_jsonl",
    )


def _t_flask_endpoint(params: Dict[str, Any]) -> CodeWriteResult:
    route = params.get("route", "/hello")
    method = params.get("method", "GET").upper()
    name = (params.get("name") or route.strip("/").replace("/", "_")
            or "hello")
    return CodeWriteResult(
        tier=TIER_TEMPLATE,
        language="python",
        code=(
            f"from flask import jsonify\n"
            f"\n"
            f"def _{name}():\n"
            f"    # TODO: implement {name} logic here\n"
            f"    return jsonify({{'route': {route!r}, 'ok': True}})\n"
            f"\n"
            f"app.add_url_rule({route!r}, endpoint={name!r}, "
            f"view_func=_{name}, methods=[{method!r}])"
        ),
        explanation=(
            f"Register a {method} endpoint at `{route}` on an existing "
            f"Flask `app`. Returns a JSON `{{'route': ..., 'ok': True}}`. "
            f"Replace the TODO with the real handler logic."
        ),
        review_notes=[
            f"if `{name}` already exists as an endpoint, this will raise — "
            f"add an `if {route!r} not in {{r.rule for r in app.url_map.iter_rules()}}:` guard",
            "for POST methods, parse JSON with `request.get_json(silent=True) or {}`",
        ],
        template_id="flask_endpoint",
    )


def _t_csv_read(params: Dict[str, Any]) -> CodeWriteResult:
    path = params.get("path", "data.csv")
    return CodeWriteResult(
        tier=TIER_TEMPLATE,
        language="python",
        code=(
            f"import csv\n"
            f"from pathlib import Path\n"
            f"\n"
            f"rows = []\n"
            f"with open({path!r}, encoding='utf-8', newline='') as f:\n"
            f"    reader = csv.DictReader(f)\n"
            f"    rows = list(reader)\n"
            f"print(f'read {{len(rows)}} rows; columns: {{list(rows[0].keys()) if rows else []}}')"
        ),
        explanation=(
            f"Read `{path}` as a list of dicts (one per row, keyed by "
            f"header). Uses `csv.DictReader` for robust parsing of "
            f"quoted/escaped fields. Memory-loads everything; for >1M "
            f"rows switch to iteration."
        ),
        review_notes=[
            "if the file has no header row, use `csv.reader` instead",
            "for huge files, iterate `reader` instead of `list(reader)`",
        ],
        template_id="csv_read",
    )


def _t_argparse_script(params: Dict[str, Any]) -> CodeWriteResult:
    name = params.get("name", "myscript")
    return CodeWriteResult(
        tier=TIER_TEMPLATE,
        language="python",
        code=(
            f"#!/usr/bin/env python3\n"
            f'\"\"\"{name} -- one-line description here.\"\"\"\n'
            f"import argparse\n"
            f"import sys\n"
            f"\n"
            f"\n"
            f"def main() -> int:\n"
            f"    p = argparse.ArgumentParser(description=__doc__)\n"
            f"    p.add_argument('input', help='input path')\n"
            f"    p.add_argument('-o', '--output', help='output path')\n"
            f"    p.add_argument('-v', '--verbose', action='store_true')\n"
            f"    args = p.parse_args()\n"
            f"\n"
            f"    if args.verbose:\n"
            f"        print(f'reading {{args.input}}', file=sys.stderr)\n"
            f"\n"
            f"    # TODO: real logic here\n"
            f"    return 0\n"
            f"\n"
            f"\n"
            f"if __name__ == '__main__':\n"
            f"    sys.exit(main())"
        ),
        explanation=(
            f"Standard argparse-based CLI script skeleton named `{name}`. "
            f"Has positional `input`, optional `--output`, `--verbose` flag. "
            f"Returns exit-code via `main()`. Replace the TODO."
        ),
        review_notes=[
            "for sub-commands, use `argparse.add_subparsers()`",
            "for required environment variables, validate at top of main()",
        ],
        template_id="argparse_script",
    )


def _t_pytest_skeleton(params: Dict[str, Any]) -> CodeWriteResult:
    target = params.get("target", "mymodule")
    return CodeWriteResult(
        tier=TIER_TEMPLATE,
        language="python",
        code=(
            f"\"\"\"test_{target}.py -- tests for {target}.\"\"\"\n"
            f"import pytest\n"
            f"from {target} import *  # noqa: F401 F403\n"
            f"\n"
            f"\n"
            f"def test_smoke():\n"
            f"    \"\"\"Module imports cleanly.\"\"\"\n"
            f"    assert True\n"
            f"\n"
            f"\n"
            f"def test_TODO_real_behavior():\n"
            f"    \"\"\"Real test of {target}'s contract here.\"\"\"\n"
            f"    # TODO: assertion on actual {target} behavior\n"
            f"    raise NotImplementedError('test not written')\n"
            f"\n"
            f"\n"
            f"if __name__ == '__main__':\n"
            f"    pytest.main([__file__, '-v'])"
        ),
        explanation=(
            f"pytest skeleton for `{target}`. Two tests: a smoke test "
            f"(imports work) + a TODO marker that explicitly raises "
            f"`NotImplementedError` so it appears RED in CI until "
            f"written. Run as `pytest -v test_{target}.py`."
        ),
        review_notes=[
            "delete the smoke test once you have real tests",
            "the NotImplementedError is intentional — it stops the suite "
            "from going green on an empty test file",
        ],
        template_id="pytest_skeleton",
    )


def _t_dataclass(params: Dict[str, Any]) -> CodeWriteResult:
    name = params.get("name", "MyData")
    fields_spec = params.get("fields", "name: str, value: int = 0")
    field_lines = "\n    ".join(
        f.strip() for f in fields_spec.split(",") if f.strip()
    )
    return CodeWriteResult(
        tier=TIER_TEMPLATE,
        language="python",
        code=(
            f"from dataclasses import dataclass\n"
            f"\n"
            f"\n"
            f"@dataclass\n"
            f"class {name}:\n"
            f"    {field_lines}"
        ),
        explanation=(
            f"Dataclass `{name}` with the fields you specified. "
            f"Auto-generates `__init__`, `__repr__`, `__eq__`. "
            f"For immutable instances add `@dataclass(frozen=True)`."
        ),
        review_notes=[
            "for default lists/dicts, use `field(default_factory=list)` "
            "from `dataclasses`",
            "for serialization use `dataclasses.asdict(instance)`",
        ],
        template_id="dataclass",
    )


def _t_bash_script(params: Dict[str, Any]) -> CodeWriteResult:
    name = params.get("name", "task")
    return CodeWriteResult(
        tier=TIER_TEMPLATE,
        language="bash",
        code=(
            f"#!/usr/bin/env bash\n"
            f"# {name}.sh -- one-line description here\n"
            f"set -euo pipefail\n"
            f"\n"
            f"usage() {{\n"
            f'    echo "usage: $0 <arg>" >&2\n'
            f"    exit 1\n"
            f"}}\n"
            f"\n"
            f"[[ $# -lt 1 ]] && usage\n"
            f"INPUT=\"$1\"\n"
            f"\n"
            f"# TODO: real logic here\n"
            f'echo "processing $INPUT"\n'
        ),
        explanation=(
            f"Bash script skeleton `{name}.sh` with strict-mode flags "
            f"(`-e` fail on error, `-u` undefined-var is error, `-o "
            f"pipefail` pipe failures propagate), `usage()` function, "
            f"and one positional argument."
        ),
        review_notes=[
            "for long-running scripts, add `trap 'cleanup' EXIT` for guaranteed cleanup",
            "for portability beyond bash, replace `#!/usr/bin/env bash` "
            "with `#!/bin/sh` and remove `pipefail`",
        ],
        template_id="bash_script",
    )


# Registry: (trigger keywords, callable, description)
_TEMPLATES: List = [
    (("read", "file"),              _t_read_file,
     "read a text file into a string"),
    (("write", "jsonl"),            _t_write_jsonl,
     "append a dict as one JSONL line"),
    (("flask", "endpoint"),         _t_flask_endpoint,
     "register a Flask route"),
    (("csv", "read"),               _t_csv_read,
     "read a CSV into list-of-dicts"),
    (("argparse", "cli", "script"), _t_argparse_script,
     "argparse-based Python CLI skeleton"),
    (("pytest", "test"),            _t_pytest_skeleton,
     "pytest test-file skeleton"),
    (("dataclass",),                _t_dataclass,
     "@dataclass with named fields"),
    (("bash", "shell", "sh"),       _t_bash_script,
     "Bash script with strict mode"),
]


def _match_template(request: str) -> Optional[Callable]:
    """Find the best-matching template for a free-text request."""
    r = request.lower()
    best: Optional[Callable] = None
    best_score = 0
    for triggers, fn, _desc in _TEMPLATES:
        score = sum(1 for t in triggers if t in r)
        if score > best_score:
            best = fn
            best_score = score
    return best if best_score > 0 else None


# ─── Public API ────────────────────────────────────────────────────

def write_code(request: str,
                 params: Optional[Dict[str, Any]] = None,
                 llm_relay: Optional[Callable[[str], str]] = None,
                 auditor: Optional[Callable[[str], Dict[str, Any]]] = None,
                 ) -> CodeWriteResult:
    """Main entry point.  Returns a CodeWriteResult with tier-tagged
    code.

    Args:
        request: free-text description, e.g. "write me a flask endpoint"
        params:  optional parameter overrides for the template
                  (e.g. {"route": "/foo", "method": "POST"})
        llm_relay: optional callable that takes a prompt and returns
                    code text (e.g. wraps Ollama or Claude API).  Only
                    used if no template matches.
        auditor: optional callable that takes a text and returns
                  {"passed": bool, "violations": [...]}.  If provided,
                  LLM-relayed output is audited and flagged.

    Returns:
        CodeWriteResult with .tier, .code, .explanation, .review_notes
    """
    params = params or {}
    template = _match_template(request)
    if template is not None:
        result = template(params)
        result.request = request
        return result

    if llm_relay is None:
        return CodeWriteResult(
            tier=TIER_UNAVAILABLE,
            language="",
            code="",
            explanation=(
                "No template matches that request, and no LLM relay is "
                "configured. Available templates: " +
                ", ".join(desc for _t, _f, desc in _TEMPLATES) +
                ". Or wire `llm_relay=` to fall back to an external LLM."
            ),
            review_notes=[],
            template_id=None,
            request=request,
        )

    # LLM-relay mode
    try:
        llm_output = llm_relay(request)
    except Exception as e:
        return CodeWriteResult(
            tier=TIER_UNAVAILABLE,
            language="",
            code="",
            explanation=f"LLM relay failed: {type(e).__name__}: {e}",
            review_notes=[],
            request=request,
        )

    audit_notes: List[str] = []
    if auditor is not None:
        try:
            verdict = auditor(llm_output)
            if not verdict.get("passed", True):
                violations = verdict.get("violations", [])
                if violations:
                    return CodeWriteResult(
                        tier=TIER_REFUSED,
                        language="",
                        code="",
                        explanation=(
                            "LLM output failed CK's scope auditor — "
                            "not returning. Violations: " +
                            "; ".join(str(v) for v in violations)
                        ),
                        review_notes=[],
                        request=request,
                    )
                audit_notes.append(
                    "scope auditor returned passed=False without "
                    "specific violations"
                )
        except Exception as e:
            audit_notes.append(
                f"scope auditor errored: {type(e).__name__}: {e}"
            )

    return CodeWriteResult(
        tier=TIER_LLM_RELAYED,
        language="unknown",
        code=llm_output,
        explanation=(
            "Output relayed from external LLM — NOT CK's own substrate "
            "knowledge. Human review required before running."
        ),
        review_notes=[
            "verify the code does what it claims (LLM hallucinations possible)",
            "check imports / library versions match your environment",
            "run in a sandbox before production use",
        ] + audit_notes,
        request=request,
    )


def list_templates() -> List[Dict[str, str]]:
    """Return a list of available templates with their triggers + descriptions."""
    return [
        {"template_id": fn(dict()).template_id,
         "triggers": ", ".join(triggers),
         "description": desc}
        for triggers, fn, desc in _TEMPLATES
    ]


# ─── Engine mount ─────────────────────────────────────────────────

def mount_code_writer(engine: Any) -> bool:
    """Attach the code writer to engine + register Flask endpoints.

    Endpoints:
      POST /code/write    — request code; body: {"request": "...", "params": {...}}
      GET  /code/templates — list available templates
      GET  /code/info     — module philosophy
    """
    # Try to find scope auditor for LLM-relay safety
    auditor_fn: Optional[Callable] = None
    try:
        from ck_scope_auditor import audit as _audit
        def _auditor(text: str) -> Dict[str, Any]:
            v = _audit(text, claimed_tier="C")
            return {"passed": v.passed, "violations": [str(x) for x in v.violations]}
        auditor_fn = _auditor
    except Exception:
        pass

    engine.ck_code_writer = {
        "write": write_code,
        "list_templates": list_templates,
        "auditor": auditor_fn,
    }

    api = getattr(engine, "web_api", None) or getattr(engine, "api", None)
    if api is not None:
        app = getattr(api, "_app", None) or getattr(api, "app", None)
        if app is not None:
            try:
                from flask import jsonify, request  # type: ignore

                def _write():
                    payload = request.get_json(silent=True) or {}
                    req = payload.get("request", "")
                    params = payload.get("params", {}) or {}
                    result = write_code(req, params, auditor=auditor_fn)
                    return jsonify({
                        "tier": result.tier,
                        "language": result.language,
                        "code": result.code,
                        "explanation": result.explanation,
                        "review_notes": result.review_notes,
                        "template_id": result.template_id,
                    })

                def _templates():
                    return jsonify({"templates": list_templates()})

                def _info():
                    return jsonify({
                        "module": "ck_code_writer",
                        "philosophy": ("tier-tagged code generation: "
                                        "templates are deterministic + "
                                        "verified, LLM-relayed output "
                                        "is flagged as needing review"),
                        "tiers": [TIER_TEMPLATE, TIER_LLM_RELAYED,
                                   TIER_UNAVAILABLE, TIER_REFUSED],
                        "endpoints": ["POST /code/write",
                                       "GET /code/templates",
                                       "GET /code/info"],
                        "auditor_wired": auditor_fn is not None,
                    })

                existing = {r.rule for r in app.url_map.iter_rules()}
                for rule, ep, fn, methods in (
                    ("/code/write",     "code_write", _write,     ["POST"]),
                    ("/code/templates", "code_tpl",   _templates, ["GET"]),
                    ("/code/info",      "code_info",  _info,      ["GET"]),
                ):
                    if rule not in existing:
                        app.add_url_rule(rule, endpoint=ep,
                                          view_func=fn, methods=methods)
            except Exception as e:
                print(f"[CK Gen14] mount_code_writer: Flask routes failed: {e}")

    print(f"[CK Gen14] mount_code_writer: {len(_TEMPLATES)} templates, "
          f"auditor_wired={auditor_fn is not None}")
    return True


# ─── CLI smoke ────────────────────────────────────────────────────

if __name__ == "__main__":
    print("ck_code_writer smoke test")
    print("=" * 60)
    print()
    print("Templates:")
    for t in list_templates():
        print(f"  {t['template_id']:18s} <- {t['triggers']:30s} -- {t['description']}")
    print()
    print("Sample request: 'write me a flask endpoint at /pc/sense'")
    print("-" * 60)
    r = write_code("write me a flask endpoint at /pc/sense",
                    params={"route": "/pc/sense", "method": "GET", "name": "pc_sense"})
    print(f"tier:         {r.tier}")
    print(f"template_id:  {r.template_id}")
    print(f"language:     {r.language}")
    print(f"code:\n{r.code}")
    print(f"explanation:  {r.explanation}")
    print(f"review_notes:")
    for n in r.review_notes:
        print(f"  - {n}")
    print()
    print("Sample request: 'translate this Greek poem' (no template)")
    print("-" * 60)
    r = write_code("translate this Greek poem")
    print(f"tier:         {r.tier}")
    print(f"explanation:  {r.explanation}")
    print()
    print("Smoke test complete.")
