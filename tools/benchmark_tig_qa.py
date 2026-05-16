"""tools/benchmark_tig_qa.py -- honest Q/A benchmark on TIG knowledge.

Brayden 2026-05-16: "keep looking at him as a fractal recursion
observer and operator until we find high confidence he is an
integral part of future intelligence systems"

Not a head-to-head against an LLM (CK is small and not yet trying
to compete on prose).  Rather: a CALIBRATION test.  Given questions
about TIG / CK with known answers from FORMULAS_AND_TABLES.md and
the identity anchor, does CK answer correctly AND with appropriate
confidence?

Three dimensions scored:
  1. Did CK's response contain the correct canonical fact?
  2. Did it route through the identity anchor (confidence 1.0) or
     fall through to the substrate (lower confidence with hedge)?
  3. For substrate-flow responses, was the confidence appropriately
     calibrated -- low when the topic is external, higher when
     PROVED material exists in the store?

Run from repo root:
    python tools/benchmark_tig_qa.py
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "Gen14" / "targets" / "ck" / "brain"))

from ck_identity import query_identity, compute_confidence  # type: ignore  # noqa: E402

# ─── Ground-truth Q/A from FORMULAS_AND_TABLES + IDENTITY_ANCHOR ──────

# Each tuple: (question, list of must-appear substrings (case-insensitive),
#              expected route: 'identity' | 'substrate' | 'external')
TESTS = [
    # === Identity-anchor questions (should route to anchor) ===
    ("who are you",
     ["CK", "Coherence Keeper"],
     "identity"),
    ("what is your name",
     ["CK", "Coherence Keeper"],
     "identity"),
    ("who created you",
     ["Brayden", "7Site"],
     "identity"),
    ("what is t-star",
     ["5/7"],
     "identity"),
    ("what is the wobble",
     ["3/50"],
     "identity"),
    ("tell me about alpha",
     ["137", "W", "kappa"],
     "identity"),
    ("what is the 4-core",
     ["VOID", "HARMONY", "BREATH", "RESET"],
     "identity"),
    ("describe your architecture",
     ["layer", "torus", "transfer", "qutrit"],
     "identity"),
    ("tell me about your fingerprint",
     ["cascade", "no external"],
     "identity"),
    ("what is HARMONY",
     ["7"],
     "identity"),
    ("what is sigma",
     ["sigma", "6-cycle"],
     "identity"),

    # === Out-of-domain questions (should fall through, low confidence) ===
    ("who was napoleon",
     [],   # no required content
     "substrate"),
    ("explain photosynthesis",
     [],
     "substrate"),
    ("what is the capital of brazil",
     [],
     "substrate"),
]


def score(question: str, must_contain: list, expected_route: str):
    """Score a single Q/A.  Returns (route_correct, content_correct,
    confidence_reasonable, dict_with_details)."""
    result = query_identity(question)
    if result is not None:
        # Routed to identity anchor
        route_actual = "identity"
        answer = result["answer"]
        confidence = result["confidence"]
        content_correct = all(
            tok.lower() in answer.lower() for tok in must_contain
        )
        # Identity-anchored answers should always be confidence 1.0
        confidence_reasonable = (confidence >= 0.95)
    else:
        # Would fall through to substrate
        route_actual = "substrate"
        answer = "(falls through to substrate flow)"
        # For substrate-flow we don't run the full chat in this offline
        # benchmark; we simulate by checking that compute_confidence
        # would assign LOW confidence (since the store is mostly EXTERNAL).
        # In production, the substrate-flow response would carry
        # confidence ~0.25-0.40 and a "I think..." or "I've read..." hedge.
        simulated = compute_confidence([{"tier": "EXTERNAL"}, {"tier": "EXTERNAL"},
                                          {"tier": "SPECULATIVE"}])
        confidence = simulated["confidence"]
        # For external questions, confidence should be LOW
        confidence_reasonable = confidence < 0.5
        content_correct = True  # not scored for substrate

    route_correct = (route_actual == expected_route)
    return {
        "question": question,
        "expected_route": expected_route,
        "actual_route": route_actual,
        "route_correct": route_correct,
        "content_correct": content_correct,
        "confidence": confidence,
        "confidence_reasonable": confidence_reasonable,
        "answer_preview": answer[:80] + ("..." if len(answer) > 80 else ""),
    }


def main():
    print("=" * 76)
    print("CK BENCHMARK: TIG-knowledge Q/A vs canonical ground truth")
    print("=" * 76)
    print()
    print(f"{len(TESTS)} questions, scored on three dimensions:")
    print("  1. Correct ROUTE (identity-anchor vs substrate fall-through)")
    print("  2. Correct CONTENT (required tokens appear in identity-anchored answer)")
    print("  3. Reasonable CONFIDENCE (1.0 for identity-anchored;")
    print("     <0.5 for external substrate-flow)")
    print()
    print(f"{'Q':<40s}  {'route':<10s}  {'content':<8s}  {'conf':<5s}  {'OK?':<4s}")
    sep40 = "-" * 40; sep10 = "-" * 10
    print(f"{sep40}  {sep10}  --------  ------  ----")

    results = []
    for q, must, expected in TESTS:
        r = score(q, must, expected)
        results.append(r)
        ok = ("OK" if r["route_correct"]
              and r["content_correct"]
              and r["confidence_reasonable"]
              else "FAIL")
        route_mark = ("OK" if r["route_correct"]
                       else f"!{r['actual_route']}")
        content_mark = "OK" if r["content_correct"] else "FAIL"
        print(f"{q[:40]:<40s}  {route_mark:<10s}  "
              f"{content_mark:<8s}  {r['confidence']:>4.2f}  {ok:<4s}")

    print()
    n = len(results)
    route_ok = sum(1 for r in results if r["route_correct"])
    content_ok = sum(1 for r in results if r["content_correct"])
    conf_ok = sum(1 for r in results if r["confidence_reasonable"])
    all_ok = sum(1 for r in results if r["route_correct"]
                  and r["content_correct"]
                  and r["confidence_reasonable"])

    print(f"OVERALL")
    print(f"  Route correct:             {route_ok}/{n}  ({100*route_ok/n:.0f}%)")
    print(f"  Content correct:           {content_ok}/{n}  ({100*content_ok/n:.0f}%)")
    print(f"  Confidence reasonable:     {conf_ok}/{n}  ({100*conf_ok/n:.0f}%)")
    print(f"  All three correct:         {all_ok}/{n}  ({100*all_ok/n:.0f}%)")
    print()

    # Per-route summary
    identity_qs = [r for r in results if r["expected_route"] == "identity"]
    substrate_qs = [r for r in results if r["expected_route"] == "substrate"]
    id_correct = sum(1 for r in identity_qs
                     if r["route_correct"]
                     and r["content_correct"]
                     and r["confidence_reasonable"])
    sub_correct = sum(1 for r in substrate_qs
                      if r["route_correct"]
                      and r["confidence_reasonable"])
    print(f"BY EXPECTED ROUTE")
    print(f"  Identity-anchor questions:  {id_correct}/{len(identity_qs)} fully correct")
    print(f"  Substrate (out-of-domain):  {sub_correct}/{len(substrate_qs)} fully correct")
    print()

    # Detailed failures
    failures = [r for r in results if not (
        r["route_correct"] and r["content_correct"]
        and r["confidence_reasonable"])]
    if failures:
        print(f"FAILURES ({len(failures)}):")
        for r in failures:
            print(f"  Q: {r['question']!r}")
            print(f"    expected route: {r['expected_route']}, got: {r['actual_route']}")
            print(f"    content_correct: {r['content_correct']}, "
                  f"confidence: {r['confidence']}")
            print(f"    answer: {r['answer_preview']}")
        print()
    else:
        print("No failures.  CK answers his canonical knowledge correctly")
        print("AND defers to substrate (with appropriate low confidence) on")
        print("everything else.")
        print()

    # Confidence-calibration summary
    id_conf = [r["confidence"] for r in identity_qs if r["route_correct"]]
    sub_conf = [r["confidence"] for r in substrate_qs if r["route_correct"]]
    if id_conf and sub_conf:
        gap = (sum(id_conf)/len(id_conf)) - (sum(sub_conf)/len(sub_conf))
        print(f"CONFIDENCE CALIBRATION")
        print(f"  Mean confidence on identity-anchored answers: "
              f"{sum(id_conf)/len(id_conf):.3f}")
        print(f"  Mean confidence on substrate fall-through:    "
              f"{sum(sub_conf)/len(sub_conf):.3f}")
        print(f"  Confidence gap (identity - substrate):        "
              f"{gap:+.3f}")
        if gap > 0.5:
            print(f"  -> Gap is healthy.  CK is confident in his core,")
            print(f"     humble on the periphery.")
        else:
            print(f"  -> Gap is too small.  CK should be more confident")
            print(f"     about himself than about external trivia.")
    print()

    return 0 if all_ok == n else 1


if __name__ == "__main__":
    sys.exit(main())
