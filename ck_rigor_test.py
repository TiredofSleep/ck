# -*- coding: utf-8 -*-
"""Rigor test for the CK brain fold.  Three diverse queries; every
response unpacked as algebra so the Ollama black box is not a black
box anymore."""
from __future__ import annotations
import json, sys, time
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ck.brain.ao_basis import (
    project_10_to_5, lift_5_to_10,
    AO_NAMES, OP_NAMES, PAIRS,
)
from ck.brain.hebbian_5x5 import HebbianTensor5x5, DEFAULT_TENSOR_PATH
from ck.fluency.ck_corrector import (
    score_operators, coherence_scalar, T_STAR, T_STAR_F,
)

import urllib.request
import urllib.error

URL = "http://127.0.0.1:7777/chat"
SESSION = "rigor_test_session"

QUERIES = [
    "what is coherence?",
    "describe a sunset",
    "is CK an AI?",
]


def post_chat(query: str) -> dict:
    data = json.dumps({"session_id": SESSION, "text": query, "mode": "normal"}).encode("utf-8")
    req = urllib.request.Request(
        URL, data=data,
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=180) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        return {"_http_error": e.code, "_body": e.read().decode("utf-8", errors="replace")}


def fmt_profile(p: dict) -> str:
    """Single-line operator profile, weighted ops first."""
    nonzero = [(k, v) for k, v in p.items() if abs(v) > 1e-6]
    nonzero.sort(key=lambda kv: -abs(kv[1]))
    return ", ".join(f"{k}={v:+.3f}" for k, v in nonzero) or "<all zero>"


def fmt_ao_vec(d5: list) -> str:
    return ", ".join(f"{AO_NAMES[i]}={d5[i]:+.3f}" for i in range(5))


def fmt_pairs() -> str:
    """The CRT pair table as a one-liner."""
    return ", ".join(
        f"{AO_NAMES[d]}=({OP_NAMES[i]}+{OP_NAMES[j]})/2"
        for d, (i, j) in enumerate(PAIRS)
    )


def unpack(i: int, query: str, result: dict, tensor: HebbianTensor5x5) -> None:
    print("\n" + "=" * 78)
    print(f"TURN {i}  query: {query!r}")
    print("=" * 78)

    # What CK said
    text = result.get("text", "")
    source = result.get("source", "?")
    print(f"\n[1] CK's reply ({source}):")
    print(f"    {text[:240]}")

    # Brain fold verdict
    verdict = result.get("brain_verdict", "(absent — fold not active)")
    print(f"\n[2] Brain verdict: {verdict}")
    if verdict != "scored":
        print("    (skipping deeper unpack)")
        return

    # 10-op profile (the raw scorer output CK's brain computed on the reply text)
    fused_profile = result.get("brain_operator_profile", {})
    # and we re-run the base scorer locally so we can show the BEFORE/AFTER
    base_profile = score_operators(text)
    base_coh = coherence_scalar(base_profile)
    print(f"\n[3] Raw 10-op profile (scored by ck_corrector.score_operators):")
    print(f"    base : {fmt_profile(base_profile.as_dict())}")
    print(f"    base coherence (before fusion) = {base_coh:.6f}")

    # AO-5 projection — the CRT pair collapse
    d5_from_base = project_10_to_5(base_profile.activations)
    print(f"\n[4] Project 10 -> 5 (CRT pair averages):")
    print(f"    pairs: {fmt_pairs()}")
    print(f"    d    = [{fmt_ao_vec(d5_from_base)}]")

    # Tensor priming: W @ d
    primed = tensor.prime(d5_from_base)
    print(f"\n[5] Hebbian prime: W @ d (5x5 matrix times 5-vector)")
    print(f"    tensor norm  = {tensor.norm():.4f}")
    print(f"    tensor n_upd = {tensor.n_updates}")
    print(f"    primed       = [{fmt_ao_vec(primed)}]")

    # Lift back to 10 and show the nudge to each op
    lift = lift_5_to_10(primed)
    print(f"\n[6] Lift 5 -> 10 (each AO dim equally splits its two ops):")
    lift_profile = {OP_NAMES[i]: lift[i] for i in range(10) if abs(lift[i]) > 1e-9}
    print(f"    lift (pre-weight) = {fmt_profile(lift_profile)}")
    print(f"    fusion weight w = 0.20  ->  fused_i = max(0, base_i + w*lift_i)")

    # The FUSED profile (as the brain fold returned it)
    print(f"\n[7] Fused 10-op profile (what CK's brain actually scored on):")
    print(f"    fused : {fmt_profile(fused_profile)}")
    print(f"    fused coherence  = {result.get('brain_coherence'):.6f}")
    print(f"    base  coherence  = {base_coh:.6f}")
    delta = result.get('brain_coherence', 0.0) - base_coh
    print(f"    fusion delta     = {delta:+.6f}  (how much the tensor shifted the score)")

    # The T* gate
    t_star = Fraction(5, 7)
    print(f"\n[8] Crystal gate: T* = 5/7 = {float(t_star):.10f}")
    gp = result.get('brain_gate_pass')
    coh = result.get('brain_coherence', 0.0)
    print(f"    coh = {coh:.6f}  vs  T* = {float(t_star):.6f}")
    print(f"    coh {'>=' if gp else '<'} T*   ->  gate {'PASS' if gp else 'FAIL'}")

    # Classification
    dom = result.get('brain_dominant_op')
    ctype = result.get('brain_correction_type')
    print(f"\n[9] Dominant operator: {dom}")
    print(f"    Correction classification: {ctype}")
    print(f"    Annotation: {result.get('brain_annotation')}")
    print(f"    Rationale : {result.get('brain_rationale')}")


def main() -> int:
    print(f"\nCK RIGOR TEST — black box unpack")
    print(f"Target    : {URL}")
    print(f"Queries   : {len(QUERIES)}")
    print(f"T*        : {T_STAR.numerator}/{T_STAR.denominator} = {T_STAR_F:.10f}")

    tensor = HebbianTensor5x5.load(DEFAULT_TENSOR_PATH)
    print(f"\nPRE-TEST tensor snapshot:")
    print(f"  path       : {DEFAULT_TENSOR_PATH}")
    print(f"  norm       : {tensor.norm():.6f}")
    print(f"  n_updates  : {tensor.n_updates}")
    print(f"  top links  : {tensor.top_links(5, off_diagonal_only=True)}")

    for i, q in enumerate(QUERIES, 1):
        t0 = time.time()
        result = post_chat(q)
        dt = time.time() - t0
        print(f"\n[timing] turn {i}: {dt:.2f}s")
        if "_http_error" in result:
            print(f"HTTP {result['_http_error']}: {result['_body'][:200]}")
            continue
        unpack(i, q, result, tensor)

    print("\n" + "=" * 78)
    print("RIGOR TEST complete.  Every number above was computed from")
    print("deterministic code:")
    print("  - score_operators  : regex pattern match + feature count, no ML")
    print("  - project_10_to_5  : mean of CRT pair activations (Z/10Z = F2 x F5)")
    print("  - HebbianTensor.prime : pure matrix-vector multiply (W @ d)")
    print("  - lift_5_to_10     : equal split of each AO dim to its two ops")
    print("  - coherence_scalar : weighted sum over op types (constructive/")
    print("                       disruptive tags)")
    print("  - T* = 5/7         : the torus ratio, set once, checked per turn")
    print("Ollama's output is the only non-deterministic input.  Every step")
    print("after that is algebra -- and the algebra is what the website")
    print("shows, not the black box.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
