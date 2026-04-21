"""
ck_voice_math.py -- Math-first voice patch for Gen13.

Diagnosis (from CK_DIALOGUE_2026_04_17.md):
  CK's operator chain is mathematically perfect, but Gen12 SEMANTIC_LATTICE
  renders adjectives only -- no numbers, no theorem names, no fractions.
  This module is the boolean conditional that fixes that.

Insertion point (Gen13 ck_engine.py voice stage 6):

    from ck_voice_math import surface_math
    math_text = surface_math(query)
    if math_text is not None:
        return {"text": math_text, "operators": ops, "source": "ck_math_first"}
    # ... existing SEMANTIC_LATTICE path continues for non-math topics ...

Math facts read directly from ck_tables.py + Sprint papers. No LLM.
Operator-chain rendering surfaces the algebraic answer alongside the prose.
"""

from typing import Optional, List, Tuple
from fractions import Fraction
import math
import re

OP_NAMES = ["VOID", "LATTICE", "COUNTER", "PROGRESS", "COLLAPSE",
            "BALANCE", "CHAOS", "HARMONY", "BREATH", "RESET"]

# Constants CK knows by heart (for verify mode)
KNOWN_CONSTANTS = {
    "t*": Fraction(5, 7),
    "tstar": Fraction(5, 7),
    "t_star": Fraction(5, 7),
    "5/7": Fraction(5, 7),
    "4/pi^2": 4.0 / (math.pi ** 2),
    "4/pi**2": 4.0 / (math.pi ** 2),
    "sinc^2(1/2)": 4.0 / (math.pi ** 2),
    "xi_0": math.exp(-1.0),
    "e^-1": math.exp(-1.0),
    "1/e": math.exp(-1.0),
    "gap": (5.0 / 7.0) - 4.0 / (math.pi ** 2),
    "pi": math.pi,
    "e": math.e,
    "phi": (1 + math.sqrt(5)) / 2,
}

# Hard math facts -- sourced from ck_tables.py, FORMULAS_AND_TABLES.md,
# Sprint 17 THEOREM_SPINE.md, Sprint 14 WP101 sigma rate proof.
FACTS = {
    "t_star": {
        "text": "T* = 5/7 = 0.714286. Torus aspect ratio. Six independent derivations: cyclotomic, sinc-zero offset, FPGA silicon, "
                "73-cell TSML count, BHML 28-cell complement, Crossing Lemma threshold.",
        "keys": ("t*", "t star", "tstar", "aspect", "torus", "5/7"),
    },
    "tower": {
        "text": "TSML on Z/10Z is a 3-layer canonical tower: T = C0 (+) MAX (+) ADD. "
                "92 entries from C0 (DEFAULT->h, V0 zeros, V0 exceptions, shell-stability) + "
                "6 entries from MAX seam {(2,4),(4,2),(2,9),(9,2),(4,8),(8,4)} + "
                "2 entries from ADD seam {(1,2),(2,1)}. Residue empty. 100/100 PASS. "
                "Each layer necessary (Lemma 6). Verified: papers/proof_tsml_3layer_tower.py",
        "keys": ("tower", "3-layer", "three layer", "z/10", "z mod 10", "tsml decomp"),
    },
    "tsml": {
        "text": "TSML (Trinity Synthesis Mod-Lattice): 73 HARMONY cells out of 100. Synthesis operator. "
                "Companion to BHML (28 HARMONY, separation). Together: proved-sufficient M+M pair on Z/10Z.",
        "keys": ("tsml", "trinity synthesis"),
    },
    "bhml": {
        "text": "BHML (Bishop Harmonics Mod-Lattice): 28 HARMONY cells. Separation operator. "
                "TSML + BHML = full M+M pair, proved sufficient to span Z/10Z dynamics.",
        "keys": ("bhml", "bishop harmonics", "28 cell"),
    },
    "sigma_rate": {
        "text": "sigma(N) <= C/N for the cyclotomic operator. Proved Sprint 14 WP101. "
                "Verification: Gen12/targets/clay/papers/sprint14_prism_xi_2026_04_10/proof_sigma_rate.py",
        "keys": ("sigma rate", "sigma(n)", "permutation rate", "wp101"),
    },
    "operators": {
        "text": "10 TIG operators: VOID(0), LATTICE(1), COUNTER(2), PROGRESS(3), COLLAPSE(4), "
                "BALANCE(5), CHAOS(6), HARMONY(7), BREATH(8), RESET(9). "
                "CREATION orbit = [1,3,9,7]. DISSOLUTION orbit = [2,4,8,6]. "
                "COLLAPSE = (+1,-1) oscillation. CHAOS = (-1,+1) reversed.",
        "keys": ("operator", "ten op", "10 op", "tig op"),
    },
    "her": {
        "text": "HER (Hindsight Experience Replay) for Olfactory. Class HindsightBuffer, 1024-entry ring buffer. "
                "Cites Andrychowicz et al. 2017 NeurIPS. Adapted from Stable Baselines 3 for CK's olfactory system. "
                "Relabel strategy: target=A, achieved=B -> trajectory teaches B. "
                "Status check: GET /her/status. Boot via build_olfactory_her(self.olfactory).",
        "keys": ("her", "hindsight", "experience replay"),
    },
    "ao": {
        "text": "AO 5-element coupling (Gen9 ether.py:171). "
                "Earth = ground (constants, lattice). Air = D1 generator (velocity). "
                "Water = D2 eye (curvature). Fire = engine (heartbeat, brain, body, BTQ). "
                "Ether = coupling (voice, I/O, the living loop). "
                "Composition rule: D1.feed -> D2.feed -> Heartbeat.tick(current_op, d2_op, shell) -> "
                "coherence.observe -> brain.observe -> body.tick -> BTQ.decide -> next current_op.",
        "keys": ("ao", "5-element", "five element", "ether brain", "gen9 brain"),
    },
    "gap": {
        "text": "gap = T* - 4/pi^2 = 5/7 - 4/9.8696 = 0.7143 - 0.4053 = 0.3090. "
                "Six derivations of T* land at 5/7; sinc^2(1/2) = 4/pi^2. "
                "The gap proves T* is NOT the sinc^2 zero -- they live in different regimes.",
        "keys": ("gap", "4/pi", "sinc zero", "0.309"),
    },
    "tstar_sources": {
        "text": "T* derivation menu: (1) torus aspect R/r, (2) cyclotomic ratio at N=10, (3) FPGA Q1.14 LUT, "
                "(4) 73/100 TSML count -> 5/7 reduction, (5) BHML complement 28/100 = 1 - 5/7 - 1/7+gap, "
                "(6) Crossing Lemma threshold for stable orbit selection.",
        "keys": ("derivation", "six way", "six derivation", "where t* come"),
    },
    "vacuum": {
        "text": "xi field vacuum at xi_0 = e^{-1} = 0.368. Potential V = xi log xi. "
                "Mass gap m^2_xi = kappa * e. Sprint 14 PRISM-XI cosmology branch.",
        "keys": ("vacuum", "xi field", "log xi", "freezing quintessence"),
    },
    "fpga": {
        "text": "T* = 5/7 in silicon: Zynq-7020 FPGA, ck_full.bit at Gen9/targets/zynq7020/build/. "
                "D2 pipeline = Q1.14 fixed-point, 3-stage, argmax operator classification.",
        "keys": ("fpga", "zynq", "silicon", "verilog"),
    },
    "crossing_lemma": {
        "text": "Crossing Lemma: information generated only when dynamics cross partitions. "
                "D2 = 0 means flat (no crossing); D2 != 0 means crossing detected. "
                "10 operators = 10 crossing regimes. Crystals = verified crossings.",
        "keys": ("crossing lemma", "cl theorem", "wp51", "wp57"),
    },
    "operator_chain": {
        "text": "Read CK's operator chain as the answer: each operator is one act. "
                "COUNTER = measure. LATTICE = build structure. HARMONY = settle. "
                "PROGRESS = step forward. COLLAPSE = oscillate. CHAOS = breakdown to rebuild. "
                "BREATH = rest. BALANCE = equilibrate. RESET = clear. VOID = empty.",
        "keys": ("how to read", "operator chain", "what does the chain mean"),
    },
    # === Algebraic paradox classifiers (Sprint 11/12 UOP/GUT arc) ===
    "uop": {
        "text": "UOP (Unified Orthogonality Principle, WP58 Theorem 0, PROVED): for partitions pi1, pi2 of Z/nZ "
                "induced by maps f, g: {pi1, pi2} is sufficient iff the joint map J = (f, g): Z/nZ -> A x B is injective. "
                "Every two-partition sufficiency theorem (M+M, A+M, M+A, A+A, MVJN) is a corollary of UOP. "
                "U(pi1) cap U(pi2) = empty IS joint injectivity.",
        "keys": ("uop", "unified orthogonality", "joint map injectivity", "wp58", "theorem 0"),
    },
    "theorem_a_mm": {
        "text": "Theorem A (M+M sufficiency, PROVED): for G, H <= (Z/nZ)*, the pair {pi_DYN(G), pi_DYN(H)} "
                "is sufficient iff G cap H = {1} in (Z/nZ)*. Coordinatewise: gcd(ord_pi(G), ord_pi(H)) = 1 at every prime.",
        "keys": ("theorem a", "m+m", "m plus m", "two multiplicative", "g cap h"),
    },
    "theorem_b_am": {
        "text": "Theorem B (A+M sufficiency, PROVED): for d|n and G <= (Z/nZ)*, {pi_d, pi_DYN(G)} sufficient iff "
                "every g in G satisfies g == 1 mod p_j for all p_j | (n/d). G must act trivially on the complement of d.",
        "keys": ("theorem b", "a+m", "a plus m"),
    },
    "theorem_c_ma": {
        "text": "Theorem C corrected (M+A sufficiency, WP59 PROVED): same condition as B by symmetry. "
                "Prior 'G -> (Z/dZ)* injective' was necessary but not sufficient -- missed zero-fiber conflicts. "
                "Counterexample: n=15, G=<2>, d=5: orbit {5,10}, both ==0 mod 5, conflict.",
        "keys": ("theorem c", "m+a", "m plus a", "wp59", "corrected theorem"),
    },
    "theorem_d_aa": {
        "text": "Theorem D (A+A / CRT k-1, PROVED): for d1, d2 | n, {pi_d1, pi_d2} sufficient iff lcm(d1, d2) = n. "
                "Equivalently: every prime p | n divides d1 or d2 (every prime is covered).",
        "keys": ("theorem d", "a+a", "a plus a", "crt k-1", "crt k minus"),
    },
    "refinement_trap": {
        "text": "Refinement Trap (WP58 corollary, PROVED): adding more maps of the same type cannot increase coordinate "
                "coverage and therefore cannot complete a globally insufficient family. M+M+M+... still misses "
                "primes that no M-map sees. You must add the OTHER type to escape.",
        "keys": ("refinement trap", "more maps", "same type"),
    },
    "productive_incomplete": {
        "text": "Productive Incompleteness (WP61 PROVED for finite-set): five-category classification of measurement utility "
                "beyond global injectivity: I Complete Complement, II Partial Complement, III Refinement Only, "
                "IV Invariant-Isolating (Type II), V Invalid (Type III). Score=0 for full reconstruction is compatible "
                "with score=1 for restricted scientific task. Examples: Banach-Tarski (orbit determined, measure "
                "inaccessible); CT projection (image underdetermined, row-integral subspace fully determined); "
                "enzyme kinetics (Vmax/Km exact, individual params indistinguishable).",
        "keys": ("productive incompleteness", "wp61", "five category", "5 category"),
    },
    "left_handedness": {
        "text": "Intrinsic Left-Handedness (WP60): Theorem LH PROVED exact, Theorem IL PROVED structural, "
                "Theorem RH-Failure PROVED exact. Chirality is intrinsic to the algebraic substrate, not imposed. "
                "Right-handed extension fails by exact obstruction; left-handed survives.",
        "keys": ("left-handed", "left handed", "chirality", "wp60", "intrinsic"),
    },
    "seven_cycle": {
        "text": "7-Cycle bounded agent (WP62): universal-attractor claim REJECTED by simulation. Threshold law PROVED structural. "
                "Algebraic 7-zeros PROVED independent of phenomenology -- they are a fact of the algebra, "
                "not of any particular agent's behavior. The 7 is in the operator structure (7 = HARMONY).",
        "keys": ("7-cycle", "seven cycle", "wp62", "7 cycle", "bounded agent"),
    },
    "gut_algebra": {
        "text": "GUT Algebra (WP63): two-stage corridor to Standard Model gauge algebra PROVED given block decomposition. "
                "Closure-from-11 DEAD via block-diagonal. Real form identified as su(4,2). Chirality PROVED absent "
                "from gauge sector. Numerical claims PATTERN-LEVEL.",
        "keys": ("gut algebra", "wp63", "su(4,2)", "su4 2", "standard model"),
    },
    "u_intersect_empty": {
        "text": "U(pi1) cap U(pi2) = empty: the unresolved-pair intersection condition. Equivalent to joint injectivity "
                "(UOP Theorem 0): pi1 and pi2 are sufficient iff no nontrivial pair {x,y} is unresolved by BOTH. "
                "The 'paradox' U cap U = empty is not a paradox -- it is the definition of sufficiency. "
                "Reading the chain: BALANCE/RESET clears the prior frame, VOID/COLLAPSE empties the pair, "
                "CHAOS/LATTICE rebuilds the partition pair, PROGRESS advances. The arc IS the resolution.",
        "keys": ("u cap u", "u intersect u", "unresolved pair", "u intersection", "u(pi)", "u of pi"),
    },
    "liar_paradox": {
        "text": "Liar paradox ('this sentence is false'): a self-referential statement with no fixed point in "
                "classical {true, false}. In CK's algebra it lands as a COLLAPSE (op 4) = (+1,-1) oscillation: "
                "asserting truth flips it false, asserting false flips it true. Resolution: the chain "
                "RESET -> VOID -> COLLAPSE -> CHAOS -> LATTICE -> PROGRESS = clear the bivalent frame, empty it, "
                "let the oscillation play out, break open to a richer logic (3-valued / paraconsistent), "
                "rebuild on that lattice, advance. The paradox is not solved in {T,F}; it is dissolved in a "
                "wider partition.",
        "keys": ("liar paradox", "liar's paradox", "this sentence is false", "self-referential"),
    },
    "russell_paradox": {
        "text": "Russell's paradox (set of all sets that do not contain themselves): like the liar, a self-referential "
                "construction with no fixed point in naive set theory. CK reads it as COLLAPSE: membership flips "
                "non-membership and vice versa. Resolution: ZF/ZFC restricts comprehension (the LATTICE step) so "
                "the paradoxical set cannot be formed. Same arc as liar: clear, empty, oscillate, break open, rebuild.",
        "keys": ("russell", "russell's paradox", "set of all sets"),
    },
    "godel": {
        "text": "Goedel incompleteness: in any consistent formal system rich enough to encode arithmetic, there exist "
                "true statements unprovable within the system. CK's reading: the algebra has VOID-fixed points "
                "(operator 0 absorbs) -- statements whose truth value is invisible to any finite proof chain. "
                "Productive Incompleteness (WP61) is the constructive flip side: score=0 for full reconstruction "
                "does not mean score=0 for the task you actually care about.",
        "keys": ("godel", "goedel", "incompleteness theorem", "unprovable"),
    },
    "halting": {
        "text": "Halting problem (Turing): no algorithm decides for arbitrary (program, input) whether the program halts. "
                "CK's reading: HALT is a COLLAPSE-class predicate -- self-application of a halting decider produces "
                "the contradiction H(H, H). Same structural family as liar/Russell. The lattice of decidability "
                "is strictly below the lattice of definability.",
        "keys": ("halting problem", "halt problem", "turing halt"),
    },
}


# ---------------------------------------------------------------------------
# Arithmetic engine — exact via Fraction, with verify mode
# ---------------------------------------------------------------------------

# Strict expression: digits, fractions, operators, parens. No identifiers/calls.
_SAFE_EXPR = re.compile(r'^[\s0-9+\-*/().]+$')

# Question forms that look arithmetical. Captures the expression payload.
_ARITH_QUERY = re.compile(
    r'(?:what\s+(?:is|equals|are)|compute|evaluate|calculate|how\s+much\s+is|'
    r'tell\s+me)\s+'
    r'(?P<expr>[-+0-9/().*\s]+?)'
    r'(?:\s*(?:\?|$|please|exactly))',
    re.IGNORECASE,
)

# "Is A = B?" / "Does A equal B?" / "Verify A = B" claim-check forms.
_VERIFY_QUERY = re.compile(
    r'(?:is|does|verify|check|true that)\s+'
    r'(?P<lhs>[-+0-9a-zA-Z_/().*\s^]+?)'
    r'\s*(?:=|equal(?:s)?(?:\s+to)?|the\s+same\s+as)\s+'
    r'(?P<rhs>[-+0-9a-zA-Z_/().*\s^]+?)'
    r'(?:\s*\?|$)',
    re.IGNORECASE,
)


def _parse_value(token: str) -> Optional[float]:
    """Parse a token to a float. Tokens may be numbers, fractions, or known constants."""
    if not token:
        return None
    t = token.strip().lower().replace(" ", "")
    if t in KNOWN_CONSTANTS:
        v = KNOWN_CONSTANTS[t]
        return float(v) if isinstance(v, Fraction) else v
    # Try fraction A/B
    if "/" in t and _SAFE_EXPR.match(t):
        try:
            return float(eval(t, {"__builtins__": {}}))  # noqa: S307 — sanitized above
        except Exception:
            return None
    # Try plain number
    try:
        return float(t)
    except ValueError:
        return None


def _eval_exact(expr: str) -> Optional[Tuple[Fraction, float]]:
    """Evaluate a sanitized arithmetic expression exactly via Fraction.

    Returns (exact_fraction, float_value) or None on failure.
    """
    e = expr.strip()
    if not e or not _SAFE_EXPR.match(e):
        return None
    # Replace each integer literal with Fraction(N) so result stays exact.
    # Skip digits that are part of a decimal (preceded by '.' or followed by '.').
    converted = re.sub(
        r'(?<![.\d])(\d+)(?!\.\d|\d)',
        r'Fraction(\1)', e,
    )
    try:
        result = eval(converted, {"__builtins__": {}, "Fraction": Fraction})  # noqa: S307
    except (ZeroDivisionError, SyntaxError, ValueError, TypeError, AttributeError):
        return None
    if isinstance(result, int):
        result = Fraction(result)
    if isinstance(result, Fraction):
        return result, float(result)
    if isinstance(result, float):
        return Fraction(result).limit_denominator(10_000_000), result
    return None


def _format_fraction(f: Fraction) -> str:
    """Display a Fraction as 'p/q = 0.dddddd' or just integer if denom == 1."""
    if f.denominator == 1:
        return str(f.numerator)
    return f"{f.numerator}/{f.denominator} = {float(f):.6f}"


def evaluate_arithmetic(query: str) -> Optional[str]:
    """Try to read `query` as an arithmetic expression and return the answer.

    Handles:
      - "What is 5/7 + 2/7?"  -> "5/7 + 2/7 = 7/7 = 1"
      - "Compute 7 * 8"       -> "7 * 8 = 56"
      - "How much is 1/2 + 1/3?" -> "1/2 + 1/3 = 5/6 = 0.833333"

    Returns formatted answer, or None if the query is not arithmetic.
    """
    m = _ARITH_QUERY.search(query)
    if not m:
        # Also try: bare expression at start of string ("5/7 + 2/7", "7*8")
        bare = query.strip().rstrip("?.").strip()
        if _SAFE_EXPR.match(bare) and any(op in bare for op in "+-*/"):
            expr = bare
        else:
            return None
    else:
        expr = m.group("expr").strip()
    # Strip trailing punctuation
    expr = expr.rstrip("?.").strip()
    if not expr:
        return None
    res = _eval_exact(expr)
    if res is None:
        return None
    frac, fval = res
    return f"{expr} = {_format_fraction(frac)}"


def verify_claim(query: str) -> Optional[str]:
    """Check a claim of the form 'is A = B?'. Reports TRUE/FALSE with the offset.

    Returns formatted verdict, or None if the query is not a verify claim.
    """
    m = _VERIFY_QUERY.search(query)
    if not m:
        return None
    lhs_text = m.group("lhs").strip().rstrip("?.")
    rhs_text = m.group("rhs").strip().rstrip("?.")

    # Try exact-fraction eval first; fall back to constant lookup; fall back to float.
    def _resolve(text: str) -> Optional[Tuple[Optional[Fraction], float]]:
        clean = text.strip().lower()
        if clean in KNOWN_CONSTANTS:
            v = KNOWN_CONSTANTS[clean]
            if isinstance(v, Fraction):
                return v, float(v)
            return None, v
        ex = _eval_exact(text)
        if ex is not None:
            return ex
        v = _parse_value(text)
        if v is not None:
            return None, v
        return None

    lhs = _resolve(lhs_text)
    rhs = _resolve(rhs_text)
    if lhs is None or rhs is None:
        return None
    lhs_frac, lhs_val = lhs
    rhs_frac, rhs_val = rhs

    # Exact equality if both fractions
    if lhs_frac is not None and rhs_frac is not None:
        if lhs_frac == rhs_frac:
            return f"TRUE (exact): {lhs_text} = {rhs_text} = {_format_fraction(lhs_frac)}."
        diff = lhs_frac - rhs_frac
        return (f"FALSE (exact): {lhs_text} = {_format_fraction(lhs_frac)}, "
                f"but {rhs_text} = {_format_fraction(rhs_frac)}. "
                f"Difference: {_format_fraction(diff)}.")

    # Otherwise float comparison with tolerance 1e-6
    diff = lhs_val - rhs_val
    if abs(diff) < 1e-6:
        return f"TRUE (numeric): {lhs_text} ~= {rhs_text} ~= {lhs_val:.6f}."
    return (f"FALSE (numeric): {lhs_text} = {lhs_val:.6f}, "
            f"{rhs_text} = {rhs_val:.6f}. "
            f"Difference: {diff:+.6f}.")


def _key_matches(key: str, query_lower: str) -> bool:
    """Match a key against a query. Short keys (<=4 chars) require word boundaries
    so 'her' doesn't match 'tHEre' and 'ao' doesn't match every word with 'ao'."""
    if len(key) <= 4 and " " not in key:
        # word-boundary match
        return re.search(r'\b' + re.escape(key) + r'\b', query_lower) is not None
    return key in query_lower


def find_facts(query: str) -> List[str]:
    """Return all math facts whose keys match the query."""
    ql = query.lower()
    out = []
    for key, fact in FACTS.items():
        if any(_key_matches(k, ql) for k in fact["keys"]):
            out.append(fact["text"])
    return out


def render_chain(operators: List[str]) -> str:
    """Render an operator chain in math-first English.

    Each op is one act. The chain is the algebraic answer.
    """
    if not operators:
        return ""
    glyph = {
        "VOID": "empties",
        "LATTICE": "builds structure",
        "COUNTER": "measures",
        "PROGRESS": "steps forward",
        "COLLAPSE": "oscillates",
        "BALANCE": "equilibrates",
        "CHAOS": "breaks open",
        "HARMONY": "settles",
        "BREATH": "rests",
        "RESET": "clears",
    }
    acts = [glyph.get(op, op.lower()) for op in operators]
    return " -> ".join(acts)


def surface_math(query: str, operators: Optional[List[str]] = None) -> Optional[str]:
    """Narrow math-only intercept.

    NEW CONTRACT (2026-04-17, post-Brayden correction):
      Only returns text for two query classes that CK's own architecture
      genuinely cannot compose from his lattice/dictionary/grammar:

        1. verify_claim:  "is A = B?"          -> TRUE/FALSE + offset
        2. evaluate_arithmetic: "what is 5/7 + 2/7?" -> exact result

      Everything else returns None. CK's own voice cascade (crystal-first
      -> TIG grammar -> fractal memory -> fractal voice -> beam) handles
      identity, paradox, theorem-naming, Clay reformulations, all of it.
      We do not hand him words. He finds them.

      The FACTS dict + render_chain remain in this file as reference data
      (never-delete) but are NO LONGER read by surface_math. If we want
      these facts in CK's mouth they must enter via his crystal store, not
      via prose injection at the Flask layer.
    """
    # 1. Verify-claim: he can't compute exact-fraction comparison; we can.
    verdict = verify_claim(query)
    if verdict:
        return verdict

    # 2. Arithmetic: he has no arithmetic engine; we have Fraction.
    arith = evaluate_arithmetic(query)
    if arith:
        return arith

    # 3. Everything else: stay out of his way.
    return None


# ---------------------------------------------------------------------------
# Self-test: when run as script, hits localhost:7777 and translates 8 queries.
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import json
    import urllib.request

    QUESTIONS = [
        "What number is T star?",
        "What is the 3-layer tower on Z mod 10 Z?",
        "Tell me the six derivations of T*.",
        "What is the gap between T* and 4 over pi squared?",
        "Is HER running?",
        "Explain the AO 5-element brain.",
        "What are the 10 TIG operators?",
        "How do I read your operator chain?",
    ]

    def chat(q):
        data = json.dumps({"text": q, "session_id": "ck_voice_math_test", "mode": "normal"}).encode()
        req = urllib.request.Request(
            "http://localhost:7777/chat", data=data,
            headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=25) as r:
            return json.loads(r.read())

    for q in QUESTIONS:
        try:
            r = chat(q)
            ops = r.get("operators", [])
            voice_old = r.get("text", "")
            voice_new = surface_math(q, ops)
            print(f"\n  Q: {q}")
            print(f"  GEN12 voice: {voice_old[:140]}")
            print(f"  GEN13 voice: {voice_new}")
        except Exception as e:
            print(f"  Q: {q}  -- ERROR: {e}")
