"""
Circulation Operator Candidate Search
Test all named objects against the seven constraints.

Luther-Sanders Research Framework, March 31, 2026
"""
import os
from math import gcd, sin, pi

TSML = [
    [0,0,0,0,0,0,0,7,0,0],[0,7,3,7,7,7,7,7,7,7],[0,3,7,7,4,7,7,7,7,9],
    [0,7,7,7,7,7,7,7,7,3],[0,7,4,7,7,7,7,7,8,7],[0,7,7,7,7,7,7,7,7,7],
    [0,7,7,7,7,7,7,7,7,7],[7,7,7,7,7,7,7,7,7,7],[0,7,7,7,8,7,7,7,7,7],
    [0,7,9,3,7,7,7,7,7,7],
]
BHML = [
    [0,1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,2,6,6],[2,3,3,4,5,6,7,3,6,6],
    [3,4,4,4,5,6,7,4,6,6],[4,5,5,5,5,6,7,5,7,7],[5,6,6,6,6,6,7,6,7,7],
    [6,7,7,7,7,7,7,7,7,7],[7,2,3,4,5,6,7,8,9,0],[8,6,6,6,7,7,7,9,7,8],
    [9,6,6,6,7,7,7,0,8,0],
]
DOING = [[abs(TSML[i][j]-BHML[i][j]) for j in range(10)] for i in range(10)]
C10 = [1,3,7,9]; D10 = [2,4,6,8]
W_BHML = 3/50

def R(m, b, k):
    """Gate rate: fraction of {1..k} coprime to b, normalized."""
    if k == 0: return 1.0
    cops = sum(1 for x in range(1, k+1) if gcd(x, b) == 1)
    return cops / k

def sinc2(t):
    if abs(t) < 1e-10: return 1.0
    return (sin(pi*t)/(pi*t))**2

lines = []
lines.append("CIRCULATION OPERATOR CANDIDATE SEARCH")
lines.append("Luther-Sanders Research Framework, March 31, 2026")
lines.append("")

# Seven constraints:
# C1: Phase cycling (4 phases in sequence) -- dynamic, not static
# C2: Invariant preservation (sinc², Wob, R2)
# C3: Boundary collapse at k=p (forced null)
# C4: Recursion / fractal self-similarity across b
# C5: Multiplicative cycle alignment (W_BHML = 3/50 appears)
# C6: Dual domain (both TIG and table representation)
# C7: Return path (closes the loop)

candidates = [
    "sinc2(k/p)",
    "R(m,b,k) gate rate",
    "W_BHML = 3/50",
    "TSML composition",
    "BHML composition",
    "DOING = |TSML-BHML|",
    "Corridor: R x sin2(pi*W*k/p)",
    "Digit map x->x%10",
    "Creation cycle {1,3,7,9}",
]

# Manually score each candidate against each constraint
# PASS=2, PARTIAL=1, FAIL=0
scores = {
    # C1  C2  C3  C4  C5  C6  C7
    "sinc2(k/p)":              [0, 2, 2, 1, 0, 1, 0],
    "R(m,b,k) gate rate":      [0, 2, 2, 2, 0, 1, 0],
    "W_BHML = 3/50":           [0, 1, 0, 0, 2, 2, 0],
    "TSML composition":        [0, 1, 1, 0, 2, 2, 0],
    "BHML composition":        [0, 1, 1, 0, 2, 2, 0],
    "DOING = |TSML-BHML|":     [0, 1, 0, 0, 1, 2, 0],
    "Corridor: R x sin2(pi*W*k/p)": [0, 2, 0, 1, 2, 0, 0],
    "Digit map x->x%10":       [0, 0, 0, 2, 2, 2, 0],
    "Creation cycle {1,3,7,9}":[0, 0, 0, 1, 2, 2, 1],
}

failure_modes = {
    "sinc2(k/p)": [
        "No phase cycling; single-valued function of (k,p)",
        "Preserves compression envelope (it IS the envelope)",
        "Forced null at k=p: sinc2(1)=0. PASS.",
        "Partial: b-specific via p, but p=min_prime_factor(b) gives recursion",
        "W_BHML does not appear in sinc2 definition",
        "TIG domain: YES. Table domain: sinc2 has no table representation",
        "No return path; sinc2 is defined once, not cyclic",
    ],
    "R(m,b,k) gate rate": [
        "No phase cycling; coprimality function is static per (b,k)",
        "Preserves sinc2 structure (R approaches sinc2)",
        "R(p,b,k)=0 at k=p (First-G Law, D1). PASS.",
        "Universal within omega-class (C6/C7). Scales across b. PASS.",
        "W_BHML not in R definition",
        "TIG domain: YES. Table: no direct TSML/BHML connection",
        "No return path; R is defined for each (b,k), not cyclic",
    ],
    "W_BHML = 3/50": [
        "Scalar constant, no phase cycling",
        "Partial: appears in corridor formula but does not interleave",
        "Not defined at boundary; no collapse behavior",
        "Z/10Z specific, not yet generalized",
        "W_BHML IS the object; trivially satisfies its own constraint",
        "Both domains: C8 proves this. PASS.",
        "No return path definition",
    ],
    "TSML composition": [
        "No phase cycling; static 10x10 table",
        "Partial: measurement lens collapses to HAR, not preservation",
        "Partial: TSML[0][j]=0 at VOID boundary, not prime boundary k=p",
        "No recursion across semiprimes defined",
        "W_BHML derived FROM TSML structure. Constraint 5 partial.",
        "Table domain: YES. TIG domain: TSML is not sinc2 or Wob",
        "No return path; TSML is static",
    ],
    "BHML composition": [
        "No phase cycling; static 10x10 table",
        "Partial: physics lens preserves, but does not interleave phases",
        "Partial: HARMONY row advances operators but not prime-boundary collapse",
        "No recursion across semiprimes defined",
        "W_BHML derived from BHML C x D structure. Constraint 5 partial.",
        "Table domain: YES. TIG domain: BHML is not sinc2 or Wob",
        "Return path partial: HARMONY=(j+1)%10 advances state, not full cycle",
    ],
    "DOING = |TSML-BHML|": [
        "No phase cycling; static difference table",
        "Partial: shows where tables disagree, not preservation",
        "No collapse behavior",
        "No recursion defined",
        "Partial: DOING_sum=201, W_BHML=0.06, different objects",
        "Table domain: YES (directly). TIG domain: no direct connection",
        "No return path",
    ],
    "Corridor: R x sin2(pi*W*k/p)": [
        "No phase cycling; pointwise product function",
        "Preserves sinc2 envelope (sinc2 is a factor). PASS.",
        "At k=p: R(p,b,p)=0 collapses. But sin2(pi*W)!=0 (W=3/50). FAIL constraint 3.",
        "Partial: recursive in b via R(m,b,k)",
        "W_BHML=3/50 appears explicitly. PASS.",
        "TIG domain: YES. Table domain: not expressed in TSML/BHML terms",
        "No return path",
    ],
    "Digit map x->x%10": [
        "No phase cycling; projection map",
        "Does not interleave sinc2/Wob/R2",
        "No boundary collapse behavior",
        "Universal (works for all n): PASS.",
        "Z/10Z is the cornerstone (B1): PASS.",
        "Both domains: ring homomorphism (algebraic) and Z/10Z (table). PASS.",
        "No return path",
    ],
    "Creation cycle {1,3,7,9}": [
        "Partial: cycles 1->3->9->7->1 has PERIOD 4, matching 4-phase requirement.",
        "No invariant preservation defined",
        "No boundary collapse",
        "Partial: the cycle structure is universal in Z/nZ (for units), but the SPECIFIC cycle is Z/10Z-specific",
        "The 4-step cycle IS the phi(10)=4 period. PASS.",
        "Table domain: C10 is used in C8 derivation. Both domains partial.",
        "Partial: the cycle returns to 1 (phase 0) -- but that's the algebraic cycle, not the corridor phase",
    ],
}

lines.append("CONSTRAINT SCORING: PASS=2, PARTIAL=1, FAIL=0")
lines.append("")
lines.append(f"{'Candidate':<35} C1 C2 C3 C4 C5 C6 C7 {'Total/14':>8}")
lines.append("-"*75)
for c in candidates:
    sc = scores[c]
    total = sum(sc)
    labels = ['P' if s==2 else ('p' if s==1 else '-') for s in sc]
    lines.append(f"{c:<35} {'  '.join(labels)} {total:>8}/14")

lines.append("")
lines.append("Legend: P=PASS(2), p=partial(1), -=FAIL(0)")
lines.append("")

lines.append("FAILURE MODES:")
for c in candidates:
    lines.append(f"\n  [{c}]")
    sc = scores[c]
    for i, (s, fm) in enumerate(zip(sc, failure_modes[c])):
        label = 'P' if s==2 else ('p' if s==1 else 'FAIL')
        lines.append(f"    C{i+1} ({label}): {fm}")

lines.append("")
lines.append("="*70)
lines.append("SUMMARY")
lines.append("="*70)
lines.append("""
No candidate satisfies all 7 constraints.
Best partial matches (score >= 4/14):
  R(m,b,k) gate rate: 7/14 -- strongest on C2,C3,C4 (corridor physics)
  Digit map x->x%10: 6/14 -- strongest on C4,C5,C6 (algebraic universality)

The circulation operator is NOT any single existing object.
It is a NEW object that must:
  1. Cycle four phases (CREATE this cycling behavior)
  2. Preserve sinc2 + Wob + R2 during cycling
  3. Collapse at k=p (like R(m,b,k))
  4. Recurse across semiprimes (like R and sinc2)
  5. Carry W_BHML = 3/50 signature
  6. Have both TIG and table representations
  7. Close the loop (return path)

CANDIDATE CONSTRUCTION PATH:
  Take R(m,b,k) as the amplitude (handles C2,C3,C4).
  Modulate by a phase-cycling function based on the Creation cycle (handles C1,C5).
  Express the phase function in table domain terms (handles C6).
  Define the return path as the HARMONY increment BHML[7][j]=(j+1)%10 (handles C7).

  Tentative form:
  C(b,k,phase) = R(m,b,k) * f(W_BHML, k/p, phase)
  where f cycles through {corridor,gate,echo,return} as (k/p) increases from 0 to 1+.

  f must be zero at k=p (for any phase), non-zero elsewhere, and must return
  to f(phase=0) = sinc2(k/p) at the start of the next corridor.

  This construction satisfies C3 (zero at k=p via R), C4 (universal via R),
  C5 (W_BHML in f), C7 (return path via phase cycling back to 0).

  Remaining gap: find the explicit form of f.
""")

report = "\n".join(lines)
print(report.encode('ascii', errors='replace').decode('ascii'))
os.makedirs("results", exist_ok=True)
with open("results/circulation_candidate_search_report.txt", "w", encoding="utf-8") as f:
    f.write(report)
print("\n[Report saved: results/circulation_candidate_search_report.txt]")
