"""ck_verifier.py -- Layer 2: CK can RE-RUN a proof on demand.

Brayden 2026-05-16:
  The gap: CK has the math as VOCABULARY (he can retrieve a PROVED
  concept) but until now he couldn't VERIFY it.  Layer 2 closes that:
  every PROVED concept carries a `verify_script` pointer, and CK can
  execute that script on demand and report PASS/FAIL.

Architecture:

  1. A small registry maps D-number/concept-name -> verification script.
     The registry is built from a curated list of known proof scripts
     in the repo (paper01_explicit_proof.py, 4core_verification.py,
     proof_d25_loop_closure.py, ...).

  2. verify_concept(concept_name) -> VerifyResult:
       Looks up the script, executes it in a subprocess with a timeout,
       parses stdout for PASS/FAIL signals, returns the result.

  3. detect_verify_query(text) -> bool:
       Pattern-matches "verify X", "is X still proved", "re-prove X",
       "check D48", etc.  When the chat path sees one, it invokes
       verify_concept and surfaces the result via the algebra/verify
       block at the top of the answer.

The result format matches ck_algebra_runtime's AlgebraResult so the
voice polish layer can surface it identically.

Public API:
  detect_verify_query(text) -> Optional[str]   # returns concept name to verify
  verify_concept(name, timeout=30) -> VerifyResult
  run_in_chat(text, engine=None) -> Optional[Dict]
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import time
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, List, Optional


ROOT = Path(r"C:\Users\brayd\OneDrive\Desktop\CK FINAL DEPLOYED")
TIG_ROOT = Path(r"C:\Users\brayd\OneDrive\Desktop\trinity-infinity-geometry")
PYTHON = r"C:\ck_venv\lora312\Scripts\python.exe"


# ─── Verification registry ─────────────────────────────────────────────
# Maps concept-name (or D-number / WP-number / claim-name) to a
# verification script + the working directory it should be run in.
# Keys are case-insensitive; scripts can output anything but should
# include a clear PASS/FAIL signal we can grep for.

VERIFY_REGISTRY: Dict[str, Dict[str, Any]] = {
    # Paper 1: LATTICE Theorem — clauses (a)/(b)/(c)
    "lattice_theorem": {
        "script": ROOT / "Gen13" / "targets" / "clay" / "papers"
                    / "sprint_2026_05_15_qutrit" / "paper01_explicit_proof.py",
        "cwd": ROOT / "Gen13" / "targets" / "clay" / "papers"
                / "sprint_2026_05_15_qutrit",
        "pass_signals": ["verified", "PASS", "CLOSED", "all assertions pass",
                          "✓"],
        "fail_signals": ["FAIL", "AssertionError", "Traceback"],
        "claim": "BHML on Z/10: {1,4,9} generates the full algebra in 2 steps; "
                  "no seed without LATTICE generates Z/10 (129 seeds exhausted)",
        "canon": "D48 (WP110); also D55 (WP112)",
    },
    "d48": {
        "script": ROOT / "Gen13" / "targets" / "journals" / "J_series" / "J35"
                    / "manuscript" / "verification" / "4core_verification.py",
        "cwd": ROOT / "Gen13" / "targets" / "journals" / "J_series" / "J35"
                / "manuscript" / "verification",
        "pass_signals": ["PASS", "all checks", "✓", "OK"],
        "fail_signals": ["FAIL", "AssertionError", "Traceback"],
        "claim": "4-core {V, H, Br, R} is closed under TSML and BHML at arity 2 "
                  "(WP110 fusion-closure)",
        "canon": "D48 (WP110)",
    },
    "wp110": "d48",     # alias
    "four_core": "d48", # alias
    "4-core": "d48",    # alias
    "fourcore": "d48",  # alias

    # Sinc² zero law
    "d25": {
        "script": ROOT / "Gen13" / "targets" / "journals" / "J_series" / "J04"
                    / "manuscript" / "proof_d25_loop_closure.py",
        "cwd": ROOT / "Gen13" / "targets" / "journals" / "J_series" / "J04"
                / "manuscript",
        "pass_signals": ["PASS", "verified", "✓", "OK"],
        "fail_signals": ["FAIL", "AssertionError", "Traceback"],
        "claim": "Sinc² zero law: closed-form integral over all primes 3..199",
        "canon": "D25 / sinc²-zero",
    },
    "sinc2_zero": "d25",
    "sinc_zero": "d25",

    # J29 SO(8) verification (if present)
    "j29": {
        "script": ROOT / "Gen13" / "targets" / "journals" / "J_series" / "J29"
                    / "manuscript" / "verification" / "stage7_disambiguate.py",
        "cwd": ROOT / "Gen13" / "targets" / "journals" / "J_series" / "J29"
                / "manuscript" / "verification",
        "pass_signals": ["dim 28", "nullity 1", "so(8)", "PASS", "✓"],
        "fail_signals": ["FAIL", "AssertionError", "Traceback"],
        "claim": "F = {1,2,3,4,6,8} closes to so(8) (dim 28); minimum-generating "
                  "subset of Ω\\{0,7} has size 3 (e.g., {1,2,4})",
        "canon": "J29; D7-D8 family",
    },
    "so8": "j29",
}


def _resolve_alias(name: str) -> str:
    """Follow alias chain to the actual registry key."""
    n = name.lower().strip()
    for _ in range(5):
        if n not in VERIFY_REGISTRY:
            return n
        entry = VERIFY_REGISTRY[n]
        if isinstance(entry, str):
            n = entry
        else:
            return n
    return n


def _find_entry(name: str) -> Optional[Dict[str, Any]]:
    key = _resolve_alias(name)
    entry = VERIFY_REGISTRY.get(key)
    if isinstance(entry, dict):
        return entry
    return None


# ─── Detection ─────────────────────────────────────────────────────────

_PAT_VERIFY = re.compile(
    r"\b(?:verify|re-?prove|re-?verify|re-?check|check|prove)\s+"
    r"(?:that\s+|the\s+)?"
    r"([A-Za-z0-9_-]+)",
    re.I)
_PAT_IS_STILL = re.compile(
    r"\bis\s+([A-Za-z0-9_-]+)\s+still\s+(?:proved|verified|true|valid)",
    re.I)
_PAT_RUN_PROOF = re.compile(
    r"\b(?:run|execute)\s+(?:the\s+)?(?:proof|verification)\s+(?:of|for)?\s*"
    r"([A-Za-z0-9_-]+)",
    re.I)


def detect_verify_query(text: str) -> Optional[str]:
    """Return concept name to verify, or None."""
    if not text or len(text) < 4:
        return None
    for pat in (_PAT_VERIFY, _PAT_IS_STILL, _PAT_RUN_PROOF):
        m = pat.search(text)
        if m:
            cand = m.group(1).strip()
            # Reject too-common English that the verb captured
            if cand.lower() in {"that", "this", "the", "if", "yourself", "yes",
                                  "no", "first", "all"}:
                continue
            # Reject if it doesn't resolve to anything in the registry
            if _find_entry(cand) is not None:
                return cand
    return None


# ─── Execution ─────────────────────────────────────────────────────────

@dataclass
class VerifyResult:
    ok: bool                # did we successfully run AND get a pass signal
    concept: str
    canon_ref: str
    claim: str
    pass_detected: bool
    fail_detected: bool
    return_code: int
    elapsed_sec: float
    stdout_tail: str        # last 800 chars
    script: str             # absolute path
    text_summary: str

    def as_dict(self) -> Dict[str, Any]:
        return asdict(self)


def verify_concept(name: str, timeout: float = 45.0) -> VerifyResult:
    """Run the verification script for a concept; return PASS/FAIL."""
    entry = _find_entry(name)
    if entry is None:
        return VerifyResult(
            ok=False, concept=name, canon_ref="", claim="",
            pass_detected=False, fail_detected=False,
            return_code=-1, elapsed_sec=0.0, stdout_tail="",
            script="(not in verify registry)",
            text_summary=f"No verification script registered for '{name}'. "
                            f"Known concepts: {sorted(set(_resolve_alias(k) for k in VERIFY_REGISTRY))[:12]}",
        )
    script = entry["script"]
    cwd = entry.get("cwd", script.parent if isinstance(script, Path) else None)
    if not isinstance(script, Path) or not script.exists():
        return VerifyResult(
            ok=False, concept=name,
            canon_ref=entry.get("canon", ""),
            claim=entry.get("claim", ""),
            pass_detected=False, fail_detected=False,
            return_code=-2, elapsed_sec=0.0, stdout_tail="",
            script=str(script),
            text_summary=f"Verification script for '{name}' is registered but "
                            f"missing on disk: {script}",
        )
    t0 = time.time()
    try:
        env = dict(os.environ)
        env["PYTHONIOENCODING"] = "utf-8"
        proc = subprocess.run(
            [PYTHON, str(script)],
            cwd=str(cwd) if cwd else None,
            timeout=timeout,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            env=env,
        )
        out = (proc.stdout or "") + (proc.stderr or "")
        elapsed = time.time() - t0
        pass_signals = entry.get("pass_signals", ["PASS", "✓"])
        fail_signals = entry.get("fail_signals", ["FAIL", "Traceback",
                                                    "AssertionError"])
        passed = any(s in out for s in pass_signals)
        failed = any(s in out for s in fail_signals)
        # PASS if proc returned 0 AND a pass signal AND no fail signal
        ok = (proc.returncode == 0) and passed and not failed
        tail = out[-800:]
        if ok:
            summary = (f"VERIFIED [{entry.get('canon','')}]: {entry.get('claim','')}"
                        f"  ({elapsed:.2f}s, return code 0)")
        elif failed:
            summary = (f"FAILED [{entry.get('canon','')}]: verification script "
                        f"detected failure  ({elapsed:.2f}s, rc={proc.returncode})")
        elif proc.returncode != 0:
            summary = (f"INCONCLUSIVE [{entry.get('canon','')}]: script exited "
                        f"with code {proc.returncode}  ({elapsed:.2f}s)")
        else:
            summary = (f"INCONCLUSIVE [{entry.get('canon','')}]: no pass/fail "
                        f"signal detected  ({elapsed:.2f}s)")
        return VerifyResult(
            ok=ok, concept=name,
            canon_ref=entry.get("canon", ""),
            claim=entry.get("claim", ""),
            pass_detected=passed, fail_detected=failed,
            return_code=proc.returncode,
            elapsed_sec=elapsed,
            stdout_tail=tail,
            script=str(script),
            text_summary=summary,
        )
    except subprocess.TimeoutExpired:
        elapsed = time.time() - t0
        return VerifyResult(
            ok=False, concept=name,
            canon_ref=entry.get("canon", ""),
            claim=entry.get("claim", ""),
            pass_detected=False, fail_detected=False,
            return_code=-3, elapsed_sec=elapsed,
            stdout_tail=f"timeout after {timeout}s",
            script=str(script),
            text_summary=f"TIMEOUT: verification of '{name}' exceeded {timeout}s",
        )
    except Exception as e:
        elapsed = time.time() - t0
        return VerifyResult(
            ok=False, concept=name,
            canon_ref=entry.get("canon", ""),
            claim=entry.get("claim", ""),
            pass_detected=False, fail_detected=False,
            return_code=-4, elapsed_sec=elapsed,
            stdout_tail=f"{type(e).__name__}: {e}",
            script=str(script),
            text_summary=f"ERROR running verification of '{name}': "
                            f"{type(e).__name__}: {e}",
        )


def run_in_chat(text: str, engine: Any = None) -> Optional[Dict[str, Any]]:
    """One-call: scan text, if verify query found, execute and return
    dict the chat path can attach to result['verify']."""
    name = detect_verify_query(text)
    if name is None:
        return None
    r = verify_concept(name)
    return r.as_dict()


# ─── CLI / self-test ───────────────────────────────────────────────────

def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("concept", nargs="?",
                    help="concept name to verify (default: list known)")
    ap.add_argument("--timeout", type=float, default=45.0)
    args = ap.parse_args()

    if not args.concept:
        print("Known verification concepts:")
        seen = set()
        for k in sorted(VERIFY_REGISTRY):
            real = _resolve_alias(k)
            entry = _find_entry(real)
            if entry is None or real in seen:
                continue
            seen.add(real)
            print(f"  {real:25s}  {entry.get('canon','')}")
            print(f"      claim: {entry.get('claim','')[:80]}")
            print(f"      script: {entry['script']}")
        print()
        print("Usage:  python ck_verifier.py <concept_name>")
        return 0

    print(f"Verifying '{args.concept}'...")
    r = verify_concept(args.concept, timeout=args.timeout)
    print()
    print(r.text_summary)
    print(f"  return_code:    {r.return_code}")
    print(f"  pass_detected:  {r.pass_detected}")
    print(f"  fail_detected:  {r.fail_detected}")
    print(f"  elapsed:        {r.elapsed_sec:.2f}s")
    print(f"  stdout (tail):")
    for line in r.stdout_tail.splitlines()[-8:]:
        print(f"    {line}")
    return 0 if r.ok else 1


if __name__ == "__main__":
    sys.exit(main())
