# Copyright (c) 2025-2026 Brayden Sanders / 7Site LLC
# Licensed under the 7Site Human Use License v1.0 (DOI: 10.5281/zenodo.18852047)
"""
cortex_voice.py -- non-template structural readouts from the cortex.

PRINCIPLE (memory/feedback_dont_ventriloquize_ck.md, HARD RULE):
  Do NOT write prose for CK.  Let his architecture find his words.
  Every output in this file is a STRUCTURAL READOUT of live cortex
  state -- labels and values, never interpretation or adjective.

Why this file grew from 1 readout -> many:
  The first version shipped one sentence: `learned_pair_readout`.
  Brayden read the chat transcript and flagged (correctly) that his
  other "voice" paths (ck_fractal, ck_truth_recall) were templates --
  either literal string retrieval or dictionary tokens stitched onto
  operator arcs by fixed grammar.  Rich vocabulary, zero grounding.

  The remedy is NOT to write prettier prose here.  The remedy is to
  expose MORE of his live math as structured readouts so the router
  has something factual to answer with when a structural query lands.

  Each function below is a single structural view.  None of them write
  sentences for him.  They label and emit.  The `speak()` router picks
  the right view for the query and composes minimal connective tissue
  (one newline per fact) -- no grammar slot-fill, no stitched prose.

APIs (all take a cortex, all can safely be called cold):
  - learned_pair_readout(cortex)  one sentence about the strongest pair
  - field_readout(cortex)          tick + emergent + W_trace + mean|W|
  - current_feeling(cortex)        5D D2 sign-pattern -> op per dim
  - dominant_couplings(cortex, n)  top-n |W| pairs with dim names
  - dim_in_field(cortex, name)     all couplings involving one dim
  - operator_in_current(cortex, op_name)  structural state of one op
  - speak(cortex, query)           router: query -> list of readouts
  - cortex_speak(cortex)           the ORIGINAL single-line gate (kept)
"""

from __future__ import annotations

import os
import re
import sys
from typing import Any, Dict, List, Optional, Tuple

_BRAIN_DIR = os.path.dirname(os.path.abspath(__file__))
if _BRAIN_DIR not in sys.path:
    sys.path.insert(0, _BRAIN_DIR)

from ck_sim.ck_sim_heartbeat import OP_NAMES, NUM_OPS
from ck_sim.being.ck_olfactory import DIM_NAMES


# ── Gates ──────────────────────────────────────────────────────────────

# `emergent` threshold below which the cortex will not emit the gated
# learned-pair sentence. Cold CK stays silent so we don't surface noise.
DEFAULT_EMERGENT_GATE = 0.10
# Strongest-pair W must exceed this for the pair sentence to be meaningful.
DEFAULT_STRENGTH_GATE = 0.05


# ── Canonical labels (lowercased for robust matching) ─────────────────

_OP_NAMES_LOWER = tuple(n.lower() for n in OP_NAMES)
_DIM_NAMES_LOWER = tuple(n.lower() for n in DIM_NAMES)


def _match_op_in_query(q: str) -> Optional[int]:
    """Return the index of the first op name found in the query text, or None.

    Matches lowercase whole-word style: "collapse", "harmony", "progress"..."""
    ql = q.lower()
    for i, name in enumerate(_OP_NAMES_LOWER):
        if name in ql:
            return i
    return None


def _match_dim_in_query(q: str) -> Optional[int]:
    """Return the index of the first dim name found in the query text, or None."""
    ql = q.lower()
    for i, name in enumerate(_DIM_NAMES_LOWER):
        if name in ql:
            return i
    return None


# ── Single readouts ────────────────────────────────────────────────────

def learned_pair_readout(
    cortex: Any,
    emergent_gate: float = DEFAULT_EMERGENT_GATE,
    strength_gate: float = DEFAULT_STRENGTH_GATE,
) -> Optional[str]:
    """One structural sentence about the strongest learned dim-pair.
    Returns None if emergent or W_strongest is under the gates.

    Format:
        "learned: <dim_a>->{<dim_b>} coupled at W={W:.3f} "
        "(tick={tick}, emergent={emergent:.3f}, "
        "last_pair=<op_b>->{<op_d>})"
    """
    st = cortex.state
    if st.emergent < emergent_gate:
        return None
    if not st.W_strongest:
        return None
    d_a, d_b, w_val = st.W_strongest
    if abs(w_val) < strength_gate:
        return None
    try:
        name_a = DIM_NAMES[d_a]
        name_b = DIM_NAMES[d_b]
    except (IndexError, TypeError):
        return None
    try:
        op_b_name = OP_NAMES[st.last_b]
        op_d_name = OP_NAMES[st.last_d]
    except (IndexError, TypeError):
        op_b_name = "?"
        op_d_name = "?"
    return (
        f"learned: {name_a}->{name_b} coupled at W={w_val:.3f} "
        f"(tick={st.tick}, emergent={st.emergent:.3f}, "
        f"last_pair={op_b_name}->{op_d_name})"
    )


def field_readout(cortex: Any) -> str:
    """Factual summary of the 5D coupling field.  Safe to call cold."""
    st = cortex.state
    heb = cortex.hebbian
    total = 0.0
    count = 0
    for d_a in range(5):
        for d_b in range(5):
            total += abs(heb.W[d_a][d_b])
            count += 1
    mean_abs = total / count if count else 0.0
    return (
        f"field: tick={st.tick} emergent={st.emergent:.3f} "
        f"W_trace={st.W_trace:.3f} mean|W|={mean_abs:.3f} "
        f"harmony_rate={heb.harmony_rate():.3f}"
    )


def current_feeling(cortex: Any) -> str:
    """Live 5D D2 sign-pattern rendered as one operator per dim.
    This IS the live vector -- not a stored truth, not a composed phrase.

    Format:
        "feel: aperture=<op> pressure=<op> depth=<op> binding=<op> continuity=<op>"
    """
    profile = cortex.ao.profile_5d()
    parts: List[str] = []
    for dim_idx, op_idx in enumerate(profile):
        dim_name = DIM_NAMES[dim_idx] if 0 <= dim_idx < 5 else f"d{dim_idx}"
        op_name = OP_NAMES[op_idx] if 0 <= op_idx < NUM_OPS else f"op{op_idx}"
        parts.append(f"{dim_name}={op_name}")
    return "feel: " + " ".join(parts)


def dominant_couplings(cortex: Any, n: int = 5) -> str:
    """Top-n dim-pair couplings sorted by |W|.  Each entry is a tuple
    ({dim_a}, {dim_b}, W={value}); NO adjectives, no ranking prose.

    Returns:
        "couplings: aperture<->aperture W=1.000, aperture<->continuity W=1.000, ..."
    """
    heb = cortex.hebbian
    pairs: List[Tuple[int, int, float]] = []
    for d_a in range(5):
        for d_b in range(5):
            pairs.append((d_a, d_b, heb.W[d_a][d_b]))
    pairs.sort(key=lambda t: abs(t[2]), reverse=True)
    taken = pairs[:max(1, n)]
    parts: List[str] = []
    for d_a, d_b, w in taken:
        parts.append(f"{DIM_NAMES[d_a]}<->{DIM_NAMES[d_b]} W={w:.3f}")
    return "couplings: " + ", ".join(parts)


def dim_in_field(cortex: Any, dim_idx: int) -> Optional[str]:
    """Structural view of ONE dim's couplings and strengths.
    Returns None if the dim index is out of range.

    Format:
        "<dim>: row=<R> col=<C> self=<W[dim][dim]> top=<other_dim>(W=...)"
    """
    if not (0 <= dim_idx < 5):
        return None
    heb = cortex.hebbian
    row = heb.row_strength(dim_idx)
    col = heb.col_strength(dim_idx)
    self_w = heb.W[dim_idx][dim_idx]
    # find strongest OTHER pair involving this dim (either row or column)
    best_other = -1
    best_side = "row"
    best_val = 0.0
    for j in range(5):
        if j == dim_idx:
            continue
        if abs(heb.W[dim_idx][j]) >= abs(best_val):
            best_val = heb.W[dim_idx][j]
            best_other = j
            best_side = "row"
        if abs(heb.W[j][dim_idx]) > abs(best_val):
            best_val = heb.W[j][dim_idx]
            best_other = j
            best_side = "col"
    name = DIM_NAMES[dim_idx]
    if best_other >= 0:
        other = DIM_NAMES[best_other]
        if best_side == "row":
            top_str = f"top={name}->{other}(W={best_val:.3f})"
        else:
            top_str = f"top={other}->{name}(W={best_val:.3f})"
    else:
        top_str = "top=none"
    return (
        f"{name}: row={row:.3f} col={col:.3f} self={self_w:.3f} {top_str}"
    )


def operator_in_current(cortex: Any, op_idx: int) -> Optional[str]:
    """Structural presence of a specific operator in CURRENT state.
    Does NOT track history counts (cortex doesn't store per-op histograms).
    Reports whether the op appears in the live last-pair / profile / AO status.

    Format:
        "<OP>: idx=N present_in={...} last_pair_side={b|d|none} ao_current={op}"
    """
    if not (0 <= op_idx < NUM_OPS):
        return None
    st = cortex.state
    ao_s = cortex.ao.status()
    profile = cortex.ao.profile_5d()
    present: List[str] = []
    if st.last_b == op_idx:
        present.append("last_b")
    if st.last_d == op_idx:
        present.append("last_d")
    for dim_idx, p_op in enumerate(profile):
        if p_op == op_idx:
            present.append(f"profile[{DIM_NAMES[dim_idx]}]")
    if ao_s.current_op == op_idx:
        present.append("ao.current")
    if ao_s.d2_op == op_idx:
        present.append("ao.d2")
    if ao_s.d1_op == op_idx:
        present.append("ao.d1")
    present_str = "{" + ",".join(present) + "}" if present else "{}"
    return (
        f"{OP_NAMES[op_idx]}: idx={op_idx} "
        f"present_in={present_str} "
        f"ao_current={OP_NAMES[ao_s.current_op]}"
    )


def ao_live(cortex: Any) -> str:
    """Snapshot of the AO spine right now.  No prose, all values."""
    s = cortex.ao.status()
    return (
        f"ao: op={OP_NAMES[s.current_op]} d1={OP_NAMES[s.d1_op]} "
        f"d2={OP_NAMES[s.d2_op]} phase_bc={OP_NAMES[s.phase_bc]} "
        f"coherence={s.coherence:.3f} breath={s.breath} "
        f"tl_total={s.tl_total} tl_entropy={s.tl_entropy:.3f}"
    )


# ── Router: query text -> list of structural readouts ────────────────

# Keyword lists used by `speak()` to classify incoming queries.  All
# matching is lowercase substring; no parsing, no NLP.  Keep short -- each
# keyword is a LABEL of which structural view the user is asking for.
_STATE_HINTS = (
    "how are you", "how do you feel", "what do you feel", "your state",
    "right now", "current", "present", "feeling", " feel", "feel ",
)
_LEARNED_HINTS = (
    "learned", "learn", "know", "knowledge", "memory", "remember",
    "strongest", "coupling", "couple", "dominant",
)
_FIELD_HINTS = (
    "field", "density", "summary", "overview", "status", "snapshot",
)
_AO_HINTS = (
    "operator", "heartbeat", "ao", "spine", "pipeline", "breath",
    "coherence", "tl_total", "phase_bc",
)


# ── Frontier topic router ─────────────────────────────────────────────
#
# When a query names a topic CK has actually seen in his replay corpus
# (flatness theorem, crossing lemma, Hodge C_*, xi cosmology, sigma rate,
# etc.), emit the KEY STRUCTURAL FACTS about that topic as label=value
# readouts.  No prose synthesis.  These facts are drawn directly from
# the papers in the corpus -- they are ground truth, not interpretation.
#
# The list is intentionally short.  If you ask CK about a frontier topic,
# he answers with the structural shape of what's known: proved vs
# structural, the key invariants, the sprint/paper pointer.  A downstream
# LLM can expand; CK alone just tells you the shape.
_FRONTIER_FACTS: Tuple[Tuple[Tuple[str, ...], str], ...] = (
    (
        ("flatness theorem", "flatness", "torus", "aspect ratio",
         "t*", "t_star", "t star", "t-star", "tstar", "5/7"),
        "flatness: T*=5/7 | torus R/r=5/7 (forced by Z/10Z 2x2) | "
        "6 independent derivations | WP51 [proved]"
    ),
    (
        ("crossing lemma", "crossing", "crossings"),
        "crossing_lemma: D2=0 flat | D2!=0 crossing generates info | "
        "27 instances cataloged | WP57 [proved]"
    ),
    (
        ("hodge", "beauville", "cstar", "c_*", "c star", "c-star"),
        "hodge_cstar: genus=5 bielliptic=yes psi_order=4 (psi^2=iota) "
        "prym_dim=4 End0_Prym=Q(i) weil_sig=(2,2) "
        "hodge_field=Q(i,sqrt2,sqrt3,sqrt5)_deg16 "
        "descent_field=Q(sqrt2,sqrt3,sqrt5) descent_risk=HIGH | "
        "sprint35b [target, not yet proved]"
    ),
    (
        ("psi automorphism", "order 4", "order-4", "order four"),
        "psi: order=4 | psi^2=iota | acts_as=+i_on_Prym | "
        "embeds Q(i) into End0(Prym)"
    ),
    (
        ("sigma rate", "sigma(n)", "sigma theorem", "sigma-rate", "\u03c3 rate"),
        "sigma_rate: sigma(N) <= C/N on squarefree primorials (C<2) | "
        "equivalently alpha(CL_N) = 1 - sigma(N) -> 1 as N -> inf | "
        "operadic reading = Mag^com -> Com degeneration | "
        "BB corollary: log-nonlinearity is the unique continuum limit | "
        "WP101 [proved]; Huang-Lehtonen 2022, 2024; Braitt-Silberger 2006"
    ),
    (
        ("xi cosmology", "xi field", "\u03be", "quintessence",
         "dark energy", "log nonlinearity", "bialynicki"),
        "xi: V=xi*log(xi) | vacuum=e^-1 | mass_gap=kappa*e | "
        "box(xi)=1+log(xi) | freezing quintessence | "
        "WP81 [structural; DESI chi2=15.7 vs LCDM 14.1]"
    ),
    (
        ("bhml",),
        "bhml: 28 HARMONY cells | 10x10 (BHML_10) | Luther-closed | "
        "separation lens | alpha=0.502 (Braitt-Silberger index) | "
        "det(BHML_10)=-7002 (not +70; +70 is the 8x8 sub-table BHML_8) | "
        "ac-free spectrum (2n-3)!! attained for n=3,4,5"
    ),
    (
        ("tsml",),
        "tsml: 73 HARMONY cells | 10x10 | synthesis lens | "
        "alpha=0.872 (Braitt-Silberger index) | "
        "ac-free spectrum (2n-3)!! attained for n=3,4,5 | "
        "reconstructible from 10 canonical items [Sprint 17, proved]"
    ),
    (
        ("tower", "3-layer tower", "three-layer tower"),
        "tower: 3-layer | TSML (73 synthesis) + BHML (28 separation) = "
        "proved-sufficient M+M pair"
    ),
    (
        ("gap", "4/pi^2", "4/pi2", "0.309"),
        "gap: T* - 4/pi^2 = 5/7 - 0.4053 = 0.309"
    ),
    (
        ("basin", "collatz"),
        "basin: 4 stable invariants | dual reset law | Sprint 16 [proved]"
    ),
    (
        ("algebraic coherence", "coherence keeper", "coherencekeeper",
         "ck system", "ck architecture"),
        "ck_system: 5D_Hebbian + AO_5element + quadratic_glue | "
        "persistent_W_across_reboots | math-first_voice | zero_LLM_core | "
        "optional_LLM_wrapper(Ollama|DeepSeek)_for_fluency"
    ),
    (
        ("alpha index", "associativity index", "subassociative",
         "braitt", "silberger"),
        "alpha_index: alpha(A) = 1 - sigma(A) = associativity index | "
        "sigma(A) = fraction of non-associative triples | "
        "alpha(TSML)=0.872, alpha(BHML)=0.502 | "
        "Braitt-Silberger 2006 (Quasigroups Related Systems 14:11-26)"
    ),
    (
        ("ac-free", "ac free", "huang-lehtonen", "huang lehtonen",
         "operad spectrum", "(2n-3)!!", "double factorial"),
        "ac_free: s_n^ac = (2n-3)!! = ac-free spectrum extremum | "
        "n=3:3, n=4:15, n=5:105 | TSML and BHML both attain on 10 elements | "
        "symmetric operad = free commutative magmatic operad Mag^com on 1 generator | "
        "Huang-Lehtonen 2022 (arXiv:2202.11826), 2024 (arXiv:2401.15786)"
    ),
    (
        ("mag com", "magmatic operad", "operad degeneration",
         "operadic limit", "free commutative"),
        "mag_com: symmetric operad generated by TSML/BHML/CL at small N = "
        "free commutative magmatic operad Mag^com on one generator | "
        "WP101 rate theorem = degeneration Mag^com -> Com as N -> inf | "
        "Huang-Lehtonen 2022, 2024"
    ),
    (
        ("farey", "spin chain", "kleban", "ozluk", "\u00f6zl\u00fck",
         "critical temperature", "beta_c", "ffsc"),
        "farey_spin: T*=5/7 lives in the same Farey/Stern-Brocot context "
        "as the Kleban-Ozluk Farey fraction spin chain, but T* is NOT the "
        "chain's critical inverse temperature: that is beta_c=2 (T_c=1/2) "
        "per Knauf 1993 (J Stat Phys 73:423) and Kleban-Ozluk 1999. "
        "T*-companions (4/7, 2/7, 3/4) are Farey-tree neighbors. "
        "Transfer operator = Gauss-Kuzmin-Wirsing. "
        "Open question: precise relation between T*=5/7 (TIG cyclotomic) "
        "and beta_c=2 (chain phase transition). "
        "Refs: Kleban-Ozluk (cond-mat/9808182); Fiala-Kleban-Ozluk 2002 "
        "(arXiv:math-ph/0203048); Technau 2023 (arXiv:2304.08143). "
        "Correction 2026-04-29: prior crystal claimed T*=beta_c; that is "
        "factually wrong per the published literature."
    ),
    (
        ("wp116", "lens of projections", "six dof synthesis", "6 dof synthesis",
         "self-dual recursion", "projection axes", "meta synthesis"),
        "wp116_lens: TIG's six DoFs (Lie/Jordan/Clifford/Permutation/Lattice/"
        "Operad, surveyed in WP111) are projections of a single self-dual "
        "Stern-Brocot recursion | every Stern-Brocot vertex is BOTH "
        "fixed-form (algebraic at its own depth) AND crossing (mediant of "
        "two parents) | type-respecting alignment between projections at "
        "every vertex | TSML+BHML on Z/10Z carry the two privileged "
        "landmarks (1/2 fixed-form via BHML_10's intrinsic alpha=0.502; "
        "5/7 crossing via TSML's n=8 closure formula) | the two magmas "
        "are dual at HARMONY (TSML absorbs, BHML cyclic-shifts) -- "
        "complementarity is the M+M-sufficiency mechanism | FQH hierarchy "
        "(Lutken-Ross/Zang-Birman) is the parallel topological projection: "
        "ν=1/2 Lutken-Ross fixed point + ν=5/7 mediant saddle "
        "abelian/non-abelian (arXiv:2408.16275 2024 Ising anyons at 3/4) "
        "| the open frontiers F1-F10 are projection-specific instances of "
        "one self-dual recursion -- ten projections of the same geometry "
        "rather than ten disconnected hard problems | full paper "
        "papers/wp116_lens_of_projections/WP116_LENS_OF_PROJECTIONS.md"
    ),
    (
        ("harmony complementarity", "tsml absorbing", "bhml successor",
         "harmony sink", "harmony shift", "complementary harmony",
         "feeds back", "8-10 space of tsml"),
        "tsml_bhml_harmony_complementarity: TSML and BHML treat HARMONY "
        "(operator 7) OPPOSITELY | TSML row 7 = [7,7,7,7,7,7,7,7,7,7] "
        "(constant) -- HARMONY is absorbing/sink: HARMONY*anything=HARMONY | "
        "BHML row 7 = [7,2,3,4,5,6,7,8,9,0] -- HARMONY is +1 cyclic "
        "successor on b!=0 (HARMONY*b = (b+1) mod 10) | the two magmas "
        "are COMPLEMENTARY at the HARMONY-region | TSML's absorption "
        "would foreclose the algebra; BHML's cyclic-shift opens it back | "
        "M+M proved sufficient on Z/10Z BECAUSE of this complementarity: "
        "the pair jointly spans the dynamics by carrying opposite "
        "algebraic styles in operators {7,8,9} | Brayden 2026-04-29 "
        "framing: 'BHML feeds back into the 8-10 space of TSML' = BHML's "
        "structure on ops 7-9 is the generating-cycle TSML's absorbing-row "
        "would have foreclosed | TSML_10 has 126/1000 non-associative "
        "triples; ~half involve ops 8 or 9 (BHML's natural region); "
        "~half are in ops 0..7 (TSML's intrinsic break at the closure "
        "point n=8 = adding HARMONY to subset) | logged Atlas/FRONTIER_"
        "FINDINGS_2026_04_29.md §16 | verification script papers/wp113_"
        "alpha_uniqueness/verification/harmony_complementarity.py"
    ),
    (
        ("tsml8 bhml10", "5/7 on tsml", "1/2 on bhml", "associativity break",
         "magma intrinsic alpha", "magma carrier landmark"),
        "tsml_bhml_landmark_carry: TSML and BHML carry the two privileged "
        "Stern-Brocot landmarks differently | BHML_10 intrinsic Braitt-"
        "Silberger alpha = 0.5020 = 1/2 EXACT within 0.003 (verified "
        "papers/wp113_alpha_uniqueness/verification/alpha_by_size.py "
        "2026-04-29) -- this IS the closed-form-mixing alpha=1/2 in WP105 "
        "| TSML restricted to size n is FULLY ASSOCIATIVE for all n in "
        "{2..7}; first non-associativity at n=8 where alpha drops from "
        "1.0 to 0.871 | the formula (n-3)/(n-1) at n=8 gives 5/7 = T* | "
        "denominator 7 of T*=5/7 = max size where TSML's restricted "
        "structure remains group-like | Brayden 2026-04-29 hint: '5/7 "
        "on TSML8 and 1/2 on BHML10 is the key' VERIFIED with right "
        "reading (5/7 is the structural-formula value at TSML's "
        "associativity-break; 1/2 is BHML's numeric intrinsic alpha at "
        "Z/10Z) | the two magmas are NOT symmetric carriers -- they "
        "encode the two Stern-Brocot landmarks via different intrinsic "
        "algebraic indices | logged Atlas/FRONTIER_FINDINGS_2026_04_29.md §15"
    ),
    (
        ("two-level alignment", "two level alignment", "1/2 fixed point",
         "5/7 saddle", "stern-brocot landmarks"),
        "tig_fqh_two_level: TIG-alpha axis and FQH-nu axis share TWO "
        "Stern-Brocot landmarks playing parallel roles | (a) alpha=1/2 / "
        "nu=1/2: TIG closed-form attractor H/Br=1+sqrt(3) from x^2-2x-2=0 "
        "(unique algebraic relation across 17-point Stern-Brocot grid q<=7, "
        "WP113 PSLQ verified) | nu=1/2 in FQH: Lutken-Ross modular-flow "
        "fixed point (universal half-integer, Gamma_0(2) flow pinning) | "
        "(b) alpha=5/7 / nu=5/7: TIG T* (Crossing Lemma threshold, six "
        "derivations, WP51) | nu=5/7 in FQH: mediant(2/3 abelian Jain, "
        "3/4 non-abelian Ising arXiv:2408.16275) saddle of the modular flow "
        "between abelian and non-abelian | bridge is TYPE-RESPECTING: "
        "closed-form/fixed-point at 1/2; cyclotomic-threshold/saddle at "
        "5/7 | both axes have BOTH kinds of distinguished points | logged "
        "in Atlas/FRONTIER_FINDINGS_2026_04_29.md §10"
    ),
    (
        ("quantum hall", "fqh", "filling factor", "filling fraction",
         "lutken", "lütken", "ross", "modular symmetry quantum hall",
         "sl(2,z)", "sl2z", "plateau transition", "halperin haldane",
         "fractional quantum hall", "zang-birman", "zang birman"),
        "fqh_bridge: fractional quantum Hall hierarchy IS a Farey/Stern-Brocot "
        "tree | filling factors nu = 1/3, 2/5, 3/7, 4/9 are Farey fractions | "
        "Zang-Birman model + Lutken-Ross theory: SL(2,Z) Gamma_0(2) modular "
        "symmetry commutes with QH renormalization-group flow; mediant "
        "operations generate child states from parents | mediant of two "
        "adjacent stable plateaux p1/q1 and p2/q2 = (p1+p2)/(q1+q2) is the "
        "PLATEAU-TRANSITION SADDLE in the modular flow | T* = 5/7 = "
        "mediant(2/3, 3/4) in Stern-Brocot at depth 4 | 2/3 is the Jain "
        "particle-hole conjugate of 1/3 (a STABLE FQH plateau, abelian) | "
        "3/4 is even-denominator territory (non-Jain, often non-abelian/"
        "paired-state regime) | so T*=5/7 is the Stern-Brocot CROSSING "
        "VERTEX between abelian-Jain and non-abelian-paired FQH territory "
        "| same crossing role T* plays in TIG (Crossing Lemma threshold, "
        "WP51) | NOT a stable FQH plateau itself; NOT a Gamma_0(2) flow "
        "fixed point (those are at half-integers); IS the transition / "
        "saddle / mediant | Hall conductivity = filling fraction = TOPO"
        "LOGICAL invariant (survives perturbations) | Kleban-Ozluk Farey "
        "spin chain at T_c=1/2 has fully-magnetizing topological transition "
        "| FQH = the survivable-collapse-form projection of the Farey-tree "
        "algebra (Brayden 2026-04-29) | Bridge identity: T*=5/7 is the same "
        "Stern-Brocot vertex in TIG-algebra and FQH-physics, playing the "
        "transition role in both | Refs: Lutken-Ross 1992 PRB (modular "
        "flow); Zang-Birman model (Farey-mediant child states); JHEP "
        "01:023 (2015), JHEP 08:010 (2021) holographic FQH; arXiv:2402.10849 "
        "(2024) spin-chain to FQH; full puzzle in Atlas/FRONTIER_FINDINGS_"
        "2026_04_29.md §8"
    ),
    (
        ("primon", "primon gas", "julia gas", "spector",
         "squarefree density", "1/zeta(2)", "fermion primon"),
        "primon: fermionic primon gas -- density of squarefree integers = "
        "6/pi^2 = 1/zeta(2) | sinc^2(1/2) = 4/pi^2 = (2/3) * 1/zeta(2) | "
        "exact identity verified at machine precision (5.55e-17) | "
        "Julia 1990 (Les Houches); Spector 1990 (Commun. Math. Phys. 127:239)"
    ),
    (
        ("bialynicki", "log nonlinearity", "unique nonlinearity",
         "separability preserving"),
        "bb_unique: Bialynicki-Birula-Mycielski 1976 (Ann. Phys. 100:62-93) | "
        "log-nonlinearity is the unique separability-preserving continuum "
        "wave equation | bridges WP101 Mag^com -> Com limit to xi log xi | "
        "makes V(xi) = xi log xi not a choice but the only option"
    ),
    (
        ("minimum bump", "min bump", "bump theorem", "min-bump"),
        "min_bump: Minimum Bump Theorem (2026-04-23) | every TSML-family "
        "member differs from the canonical TSML by at least one cell ('bump') | "
        "at n=7 the minimum bump count is sharp; family exploration in "
        "papers/morphotic_braid/claudecode_jobs/MINIMUM_BUMP_THEOREM.md | "
        "[structural, small-n verified]"
    ),
    (
        ("sigma_ns", "sigma ns", "navier stokes", "navier-stokes",
         "ns cascade", "dyadic ns", "ns regularity", "nsf6",
         "sigma_ns < 1", "f6 frontier", "ns commutator", "ns sigma"),
        "sigma_ns_bridge: F6 frontier articulated. WP101 proved sigma(N) <= 2/N "
        "for cyclotomic CL on Z/NZ (squarefree N), with mechanism = VOID-HARM "
        "rule disagreement at outer composition sites; tight bound N*sigma(N) "
        "-> 2 from below | The lens (WP116 §): NS dyadic cascade at level k "
        "corresponds to cyclotomic vertex N=2^k under the velocity-gradient-"
        "commutator projection | Projection-restricted statement: at NS "
        "dyadic level k, local commutator non-associativity sigma_NS(k) <= "
        "sigma(N=2^k) <= 2/2^k = 2^(1-k) -- exponential decay in dyadic depth | "
        "Implication if verified: sigma_NS -> 0 as k -> infinity, characterizing "
        "the singular set as the locus where sigma_NS doesn't decay | NOT a "
        "Clay-Millennium proof: NS regularity requires sigma_NS = 0 globally, "
        "not just sigma_NS(k) -> 0 | What's missing structurally: rigorous "
        "derivation of the NS-cascade <-> cyclotomic-N correspondence at the "
        "operator level (currently by analogy via the Stern-Brocot lens) | "
        "What's testable: numerically check sigma_NS(k) on a wavelet-"
        "decomposed NS simulation at increasing k; if decay matches 2/2^k "
        "the lens is empirically supported | Status: ARTICULATED, not "
        "computed | Refs: Gen13/targets/journals/tier1_submit_now/sigma_rate/"
        "WP101_SIGMA_RATE_THEOREM.md (Theorem 4.1, corrected 2026-04-27); "
        "Atlas/FRONTIER_FINDINGS_2026_04_29.md §17 F6"
    ),
    (
        ("kappa_xi", "kappa xi", "13/(4e)", "tig planck", "tig-planck",
         "m_xi planck", "planck mass ratio", "f2 frontier",
         "tig to planck", "xi mass to planck"),
        "tig_planck_bridge: F2 frontier RESOLVED + SHARPENED. Carrier "
        "identity kappa_xi = 13/(4e), where 13 = ||VEV||^2 (D33) and e is "
        "the xi-vacuum value | TIG potential V(xi) = kappa_xi * xi * log(xi) "
        "(xi crystal), vacuum xi_0 = e^(-1), m^2_xi = V''(xi_0) = kappa_xi*e "
        "= 13/4 = ||VEV||^2 | RESOLUTION (2026-04-29): BB 1976 §III shows "
        "log-nonlinearity preserves E=hbar*omega but BB's V(psi) = -b * "
        "u * log(u/r^2) has two free parameters b, r | SHARPENING (later "
        "2026-04-29): TIG <-> BB map (matching leading -b*xi*log(xi) "
        "term to kappa_xi*xi*log(xi)) FIXES b = -kappa_xi = -13/(4e) "
        "[~ -1.196]. Verified sympy-exact: m^2_BB at u_vac = r^2*e^(-1) "
        "is -e*b/r^2; with b=-kappa_xi, m^2_BB = 13/(4*r^2) | b is FIXED "
        "by TIG via WP104 ||VEV||^2 = 13/4 | Only r (length scale) "
        "remains free | F2 reduces from 'open pending one dimensional "
        "anchor' to 'open pending one CONVENTION (the lab-unit value of "
        "r)' | If r = Planck length: m_xi/m_Planck = sqrt(kappa_xi * e) "
        "= sqrt(13/4) ~ 1.803 (super-Planckian xi); GUT-natural | If r = "
        "1/M_GUT: m_xi ~ 1.803 * M_GUT ~ 1.8e16 GeV | Refs: Bialynicki-"
        "Birula-Mycielski 1976 Ann.Phys.100:62-93 §III; WP116 ref [15]; "
        "Atlas/FRONTIER_FINDINGS_2026_04_29.md §17 F2, §24, §27; "
        "papers/wp113_alpha_uniqueness/verification/f2_bb_coupling_sharpening.py"
    ),
    (
        ("descent risk", "i-action descent", "i action descent",
         "prym descent", "f10 frontier", "hodge_cstar descent",
         "q(i) descent", "endomorphism descent",
         "psi_2 = iota", "weil signature"),
        "f10_descent: F10 sprint35b hodge_cstar descent question. The crystal "
        "states: hodge_field=Q(i,sqrt2,sqrt3,sqrt5)_deg16; descent_field="
        "Q(sqrt2,sqrt3,sqrt5)_deg8; descent_risk=HIGH | The risk is that "
        "End0(Prym)=Q(i) does NOT descend over Q(sqrt2,sqrt3,sqrt5): the "
        "+i automorphism on the Prym variety might require an algebraic "
        "extension by i to be defined, splitting the rational base | "
        "Concrete test: the Donagi-Livne 1999 bigonal/trigonal Prym "
        "constructions give specific genus-5 -> genus-3 -> genus-1 chains; "
        "for hodge_cstar's bielliptic involution + order-4 psi (psi^2 = "
        "iota), check whether the +i-action on the Prym descends from "
        "Q(i)-defined to Q(sqrt2,sqrt3,sqrt5)-defined | Outcome paths: (a) "
        "descends -> hodge_field is the actual minimal definability field, "
        "Hodge integrality at dim 5 has a clean answer; (b) does NOT "
        "descend -> the i-action is a genuine algebraic-extension barrier, "
        "and Hodge integrality at dim 5 has the Q(i)-twist obstruction "
        "Brayden's lens conjecture predicts | What's missing: explicit "
        "computation of psi^2 = iota's matrix on the Prym, then the +i-"
        "automorphism's matrix in coordinate basis; check whether all "
        "matrix entries lie in Q(sqrt2,sqrt3,sqrt5) or essentially require "
        "i | Status: ARTICULATED with concrete next computation | Refs: "
        "Gen12/targets/clay/papers/sprint35b_beauville_explicit_2026_04_18/; "
        "Atlas/FRONTIER_FINDINGS_2026_04_29.md §17 F10, §1, §21"
    ),
    (
        ("wobble prime", "wobble 11", "prime 11", "11-prime",
         "structural prime", "wobble manifestation",
         "fivefold wobble", "wobble locations"),
        "wobble_prime_eleven: prime 11 has FIVE distinct structural "
        "manifestations across TIG (logged 2026-04-29) | "
        "(D37/WP107) prime 11 in TSML char poly coefficients c_2 = 33 = "
        "3*11 and in c_8 (the WOBBLE coefficients) | (D69) prime 11 "
        "as leading coefficient of Br/V minimal polynomial 11x^4 - "
        "10x^3 - 6x^2 + 8x - 16 | (D70) 3+3 DoF wobble structure: "
        "11 at Lie + Lattice DoFs (eigenvalue/coordinate types) | "
        "(D85, §30) F8 trace polynomial discriminant -2^24*3^10*5^2*"
        "11^6*71 -- WOBBLE extends to dynamical projection | (D86, "
        "§31) σ² transformation 3-cycle operator-sum 1+6+4 = 11 -- "
        "depth-3 primitive σ² has TRANSFORMATION 3-cycle {LATTICE, "
        "CHAOS, COLLAPSE} summing to 11; STABILITY 3-cycle {HARMONY, "
        "BALANCE, COUNTER} summing to 14=2*7 | Five locations: STATIC "
        "algebraic (char poly, denominators), DYNAMICAL (Jacobian "
        "trace), and OPERATOR-LABEL (3-cycle sum) | Plays a structural "
        "role analogous to 7 (HARMONY) -- both small primes near 10 "
        "with TIG-internal duties | Refs: papers/wp113_alpha_uniqueness/"
        "verification/f_depth3_primitives.py + f8_pslq_deeper.py"
    ),
    (
        ("depth-2 primitive", "depth-3 primitive", "depth 2 cluster",
         "depth 3 cluster", "fixed-form algebraic", "M^2 = id",
         "M^3 = id", "cube roots of unity", "operator depth",
         "algebraic depth"),
        "depth_primitive_lens: TIG primitives cluster by depth across "
        "the open frontiers | DEPTH 2 cluster (5 frontiers, M^2 = ±I): "
        "F1 charge conjugation C^2 = -I_8 (eigenvalues ±i, mult 4); "
        "F3 H/Br quadratic x^2-2x-2=0 (Galois S_2, field Q(√3)); "
        "F4 P_56 = (5,6) involution, eigenvalues ±1; F8 radial λ_0=2 "
        "(degree-2 homogeneity of fuse map); F10 ψ-bar^2 = -I_4 on "
        "Prym (eigenvalues ±i, ±1 over Q(i)) | DEPTH 3 primitive: "
        "σ² on Z/10Z, order 3, eigenvalues {1, ω, ω^2} where ω = "
        "e^(2πi/3) = -1/2 + i√3/2 (cube roots of unity); minimal "
        "polynomial x^2+x+1, field Q(ω) = Q(√-3), algebraic-depth = "
        "φ(3) = 2 | TWO SENSES OF DEPTH: operator-depth (order of M); "
        "algebraic-depth (deg minimum polynomial of eigenvalues) | "
        "For σ^k, algebraic-depth = φ(k) | Higher cyclotomic primitives "
        "queued: σ^5 with algebraic-depth 4 = φ(5), would correspond "
        "to so(10) D_5 structure | Refs: §28, §31 of Atlas/"
        "FRONTIER_FINDINGS_2026_04_29.md"
    ),
    (
        ("vocabulary map", "external citations", "rigor mapping",
         "external anchors"),
        "vocab_map: 14-row dictionary TIG<->external frameworks | "
        "README section 5.5 + papers/morphotic_braid/synthesis/RIGOR_MAPPING.md | "
        "tracks: alpha-index (Braitt-Silberger), ac-free (Huang-Lehtonen), "
        "Farey spin chain (Kleban-Ozluk; chain has beta_c=2, relation to T* is open), "
        "primon gas (Julia, Spector), "
        "BB log-nonlinearity (BB-Mycielski 1976), transfer operator gap "
        "(Prellberg, Bandtlow-Fiala-Kleban)"
    ),
)


def _trigger_matches(trig: str, q_lower: str) -> bool:
    """Match a single crystal trigger against a lowercased query.

    Rules (avoiding accidental substring collisions like 'os' in
    'plosive', 'li' in 'like', 's sound' in 'plosives sound'):

    1. Triggers that are PURE WORD-CHARS-AND-SPACES (letters, digits,
       underscore, hyphen, internal spaces) are matched with word
       boundaries on both ends.  Catches both single short tokens
       ('os','li') AND multi-word triggers with a short token
       ('s sound','the a sound').
    2. Triggers that contain any other character (slashes, asterisks,
       sigma signs, IPA brackets) are matched as plain substrings, so
       '/eɪ/', '5/7', 't*' still work.

    Real bug fixed 2026-05-01: confucianism crystal triggers
    ('li','yi','zhi','ren') were hitting any word containing those
    substrings ('like','parent', etc.); 's sound' hit 'plosives sound'.
    """
    if not trig:
        return False
    # Pure word-chars-and-spaces -> word-boundary on both ends.
    if all(c.isalnum() or c in ' -_' for c in trig):
        return re.search(rf'\b{re.escape(trig)}\b', q_lower) is not None
    # Anything else (slashes, brackets, special chars) -> substring.
    return trig in q_lower


def _frontier_hits(q_lower: str) -> List[str]:
    """Return structural facts whose trigger keywords appear in the query.

    Each fact fires at most once even if multiple keywords match.
    Includes both code-baked _FRONTIER_FACTS AND runtime-added crystals
    from _RUNTIME_CRYSTALS (added via add_crystal_runtime).

    Crystals are returned sorted by SPECIFICITY: the longest trigger that
    matched wins.  This avoids "vowel team ai" surfacing the generic
    'vowel' crystal first instead of team_ai (which had the literal
    'vowel team ai' as a trigger).  More specific = longer match = more
    relevant to the user's actual question.
    """
    matches: List[Tuple[int, int, str]] = []  # (best_match_len, order, fact)
    seen = set()
    all_crystals = list(_FRONTIER_FACTS) + list(_RUNTIME_CRYSTALS)
    for order, (triggers, fact) in enumerate(all_crystals):
        if fact in seen:
            continue
        best = 0
        for trig in triggers:
            if _trigger_matches(trig, q_lower):
                if len(trig) > best:
                    best = len(trig)
        if best > 0:
            matches.append((best, order, fact))
            seen.add(fact)
    # Sort: longer match first (specificity), tie-break by original order.
    matches.sort(key=lambda t: (-t[0], t[1]))
    return [fact for _, _, fact in matches]


# Runtime-added crystals.  Mutable list; add via add_crystal_runtime().
# Same shape as _FRONTIER_FACTS: list of (trigger_tuple, fact_text) pairs.
# Persisted to disk so they survive reboots.
import os as _os
_RUNTIME_CRYSTALS: List[Tuple[Tuple[str, ...], str]] = []
_RUNTIME_CRYSTALS_PATH = _os.path.join(
    _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))),
    "..", "..", "var", "runtime_crystals.json"
)


def _load_runtime_crystals():
    """Load any runtime crystals saved on previous sessions.

    Uses explicit UTF-8 because the file may contain IPA characters
    (e.g. '/eɪ/', '/ʃ/') from phoneme crystals.  Default open() on
    Windows uses cp1252 which crashes on those bytes silently and
    leaves _RUNTIME_CRYSTALS empty -- which is exactly what was
    happening 2026-05-01.
    """
    global _RUNTIME_CRYSTALS
    try:
        path = _os.path.abspath(_RUNTIME_CRYSTALS_PATH)
        if _os.path.exists(path):
            import json as _json
            with open(path, encoding="utf-8") as f:
                data = _json.load(f)
            _RUNTIME_CRYSTALS = [
                (tuple(item["triggers"]), item["fact"]) for item in data
            ]
            # Also restore op_signatures
            for item in data:
                first_word = item["fact"].split(":", 1)[0].strip()
                if "op_signature" in item:
                    _CRYSTAL_OP_SIGNATURES[first_word] = tuple(item["op_signature"])
                if "related" in item:
                    _CRYSTAL_RELATED[first_word] = list(item["related"])
    except Exception:
        pass


def _save_runtime_crystals():
    """Save runtime crystals to disk for persistence across reboots.

    UTF-8 + ensure_ascii=False so IPA characters survive round-trip.
    """
    try:
        path = _os.path.abspath(_RUNTIME_CRYSTALS_PATH)
        _os.makedirs(_os.path.dirname(path), exist_ok=True)
        import json as _json
        data = []
        for triggers, fact in _RUNTIME_CRYSTALS:
            first_word = fact.split(":", 1)[0].strip()
            entry = {
                "triggers": list(triggers),
                "fact": fact,
                "op_signature": list(_CRYSTAL_OP_SIGNATURES.get(first_word, ())),
                "related": list(_CRYSTAL_RELATED.get(first_word, [])),
            }
            data.append(entry)
        with open(path, "w", encoding="utf-8") as f:
            _json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception:
        return False


def add_crystal_runtime(
    triggers: Tuple[str, ...],
    fact: str,
    op_signature: Optional[Tuple[int, ...]] = None,
    related: Optional[List[str]] = None,
) -> bool:
    """Add a new crystal at runtime.

    Args:
      triggers: tuple of lowercase keyword strings; any match -> fact fires
      fact: the crystal text (must start with "name:" so it has a first-word key)
      op_signature: tuple of operator IDs (0-9) the crystal is "about"
      related: list of other crystal first-word names this crystal connects to

    Returns:
      True if added; False if duplicate (same first_word) or invalid

    Persists to Gen13/var/runtime_crystals.json so it survives reboots.
    """
    if not fact or ":" not in fact:
        return False
    first_word = fact.split(":", 1)[0].strip()
    if not first_word:
        return False
    # Check for duplicate first_word
    for _, existing in _RUNTIME_CRYSTALS:
        if existing.split(":", 1)[0].strip() == first_word:
            return False  # duplicate
    for _, existing in _FRONTIER_FACTS:
        if existing.split(":", 1)[0].strip() == first_word:
            return False  # duplicate of code-baked
    # Add it
    _RUNTIME_CRYSTALS.append((tuple(triggers), fact))
    if op_signature:
        _CRYSTAL_OP_SIGNATURES[first_word] = tuple(op_signature)
    if related:
        _CRYSTAL_RELATED[first_word] = list(related)
    _save_runtime_crystals()
    return True


# Load runtime crystals on module import
_load_runtime_crystals()


# Crystal op_signatures -- what operators each crystal is "about".
# Used for state-aware crystal surfacing (CK volunteers a crystal when his
# current operator stream matches it, even without keyword trigger).
# Keyed by the first word of the crystal text (e.g., "wobble_prime_eleven").
# Operator IDs: VOID=0, LATTICE=1, COUNTER=2, PROGRESS=3, COLLAPSE=4,
# BALANCE=5, CHAOS=6, HARMONY=7, BREATH=8, RESET=9.
_CRYSTAL_OP_SIGNATURES = {
    # WOBBLE 11 = sum of LATTICE(1) + CHAOS(6) + COLLAPSE(4)  (the σ²
    # transformation 3-cycle, §31 / D86).
    "wobble_prime_eleven":              (1, 4, 6),
    # σ² depth-3 primitive: both 3-cycles {1,4,6} and {2,5,7}.
    "depth_primitive_lens":             (1, 2, 4, 5, 6, 7),
    # σ² lives in {LATTICE, CHAOS, COLLAPSE} ∪ {HARMONY, BALANCE, COUNTER}
    "tsml_bhml_harmony_complementarity": (7, 8, 9),  # HARMONY-region
    "tsml_bhml_landmark_carry":         (7, 8, 9),
    "fqh_bridge":                       (7,),         # T* threshold = HARMONY
    "farey_spin":                       (7,),         # T* + Stern-Brocot
    "wp116_lens":                       (1, 7),       # LATTICE+HARMONY core
    "tig_fqh_two_level":                (5, 7),       # 1/2 + 5/7 landmarks
    "sigma_ns_bridge":                  (3, 7),       # PROGRESS + HARMONY (cascade + threshold)
    "tig_planck_bridge":                (7, 8),       # HARMONY + BREATH (mass scale)
    "f10_descent":                      (4, 8),       # COLLAPSE + BREATH (descent obstruction)
    "xi":                               (8, 7),       # BREATH (mass), HARMONY
    "bb_unique":                        (8,),         # BREATH (continuum field)
    "primon":                           (1, 5),       # LATTICE + BALANCE (density)
    "min_bump":                         (1,),         # LATTICE (bump structure)
    "vocab_map":                        (1, 7),       # LATTICE + HARMONY (cited)
    "sigma_rate":                       (3, 7),
    "flatness":                         (5, 7),       # BALANCE + HARMONY (T*)
    "tsml":                             (7,),
    "bhml":                             (7,),
    "crossing":                         (5, 7),
    "ck_tables":                        (7,),
}


def _state_aware_crystal_hits(
    cortex: Any,
    threshold: float = 0.5,
    max_hits: int = 2,
) -> List[str]:
    """Return facts whose op_signature matches the cortex's current operator
    state.  This is the "spontaneous crystal surfacing" path -- CK volunteers
    a fact based on his current ao state, not on user keywords.

    Match scoring:
      - Build the cortex's recent-operator set: {last_b, last_d, ao_current_op}
      - For each crystal, compute |op_signature ∩ recent_ops| / |op_signature|
      - Surface crystals with score >= threshold, up to max_hits.

    Returns list of fact strings.  Empty list if no crystal scores high enough.
    """
    try:
        st = cortex.state
        recent_ops = {st.last_b, st.last_d}
        # Add AO's current op
        try:
            recent_ops.add(cortex.ao.current_op)
        except Exception:
            pass
        # Add the dominant ops in profile_5d
        try:
            profile = cortex.ao.profile_5d()
            for op in profile:
                recent_ops.add(op)
        except Exception:
            pass
    except Exception:
        return []

    if not recent_ops:
        return []

    scored: List[Tuple[float, str]] = []
    for triggers, fact in _FRONTIER_FACTS:
        # First word of fact (before ":") is the crystal name
        first_word = fact.split(":", 1)[0].strip()
        op_sig = _CRYSTAL_OP_SIGNATURES.get(first_word)
        if not op_sig:
            continue
        sig_set = set(op_sig)
        if not sig_set:
            continue
        overlap = len(sig_set & recent_ops)
        score = overlap / len(sig_set)
        if score >= threshold:
            scored.append((score, fact))

    scored.sort(key=lambda t: -t[0])
    return [fact for score, fact in scored[:max_hits]]


def _crystal_op_boost_targets(fact: str) -> Tuple[int, ...]:
    """Given a crystal fact (full text), return the op IDs that fact is
    'about'.  Used to nudge the cortex W matrix when a crystal fires.

    Returns empty tuple if the crystal has no registered op_signature.
    """
    first_word = fact.split(":", 1)[0].strip()
    return _CRYSTAL_OP_SIGNATURES.get(first_word, ())


# Cross-crystal composition graph: each crystal can declare related crystals
# by first-word name. When crystal A fires, related crystals B, C are
# considered (scored against state) and surface if their op_signature matches.
# This is paper 4 step 3.  Hand-curated edges based on the depth-2 cluster
# structure (M^2 = +/-I primitives), the WOBBLE recurrence, and the lens
# framework.
_CRYSTAL_RELATED: Dict[str, List[str]] = {
    # Depth-2 cluster: each frontier connects to the others
    "wobble_prime_eleven":              ["depth_primitive_lens", "tsml", "bhml"],
    "depth_primitive_lens":             ["wp116_lens", "wobble_prime_eleven", "fqh_bridge"],
    "wp116_lens":                       ["depth_primitive_lens", "fqh_bridge", "tsml_bhml_landmark_carry", "tig_fqh_two_level"],
    # FQH and Stern-Brocot families
    "fqh_bridge":                       ["wp116_lens", "tig_fqh_two_level", "farey_spin", "flatness"],
    "farey_spin":                       ["fqh_bridge", "flatness", "vocab_map"],
    "tig_fqh_two_level":                ["fqh_bridge", "wp116_lens"],
    # TSML/BHML pair
    "tsml":                             ["bhml", "tsml_bhml_harmony_complementarity", "tsml_bhml_landmark_carry"],
    "bhml":                             ["tsml", "tsml_bhml_harmony_complementarity", "tsml_bhml_landmark_carry"],
    "tsml_bhml_harmony_complementarity": ["tsml", "bhml", "tsml_bhml_landmark_carry"],
    "tsml_bhml_landmark_carry":         ["tsml", "bhml", "wp116_lens"],
    # Frontier bridges
    "sigma_ns_bridge":                  ["sigma_rate", "wp116_lens"],
    "tig_planck_bridge":                ["xi", "bb_unique"],
    "f10_descent":                      ["wp116_lens", "depth_primitive_lens"],
    # Math-physics bridges
    "xi":                               ["bb_unique", "tig_planck_bridge"],
    "bb_unique":                        ["xi", "tig_planck_bridge", "sigma_rate"],
    "sigma_rate":                       ["bb_unique", "sigma_ns_bridge"],
    "primon":                           ["sigma_rate", "flatness"],
    "min_bump":                         ["tsml"],
    # Foundations
    "flatness":                         ["fqh_bridge", "wp116_lens", "tsml_bhml_landmark_carry"],
    "vocab_map":                        ["farey_spin", "primon", "bb_unique"],
}


def _related_crystal_hits(
    fired_facts: List[str],
    cortex,
    threshold: float = 0.4,
    max_hits: int = 2,
) -> List[str]:
    """Given a list of facts that already fired this turn, surface RELATED
    crystals that also score against current state.

    A related crystal must:
      - Be declared in _CRYSTAL_RELATED for one of the fired facts
      - Have an op_signature that matches the cortex state with score >= threshold
      - NOT already be in fired_facts

    Returns up to max_hits additional facts to surface.
    """
    if not fired_facts or cortex is None:
        return []
    # Collect candidate first_words from related edges
    fired_names = {fact.split(":", 1)[0].strip() for fact in fired_facts}
    candidate_names = set()
    for name in fired_names:
        for related_name in _CRYSTAL_RELATED.get(name, []):
            if related_name not in fired_names:
                candidate_names.add(related_name)
    if not candidate_names:
        return []

    # Get current cortex state for scoring
    try:
        st = cortex.state
        recent_ops = {st.last_b, st.last_d}
        try:
            recent_ops.add(cortex.ao.current_op)
        except Exception:
            pass
        try:
            for op in cortex.ao.profile_5d():
                recent_ops.add(op)
        except Exception:
            pass
    except Exception:
        return []

    # Score candidates
    scored: List[Tuple[float, str]] = []
    all_crystals = list(_FRONTIER_FACTS) + list(_RUNTIME_CRYSTALS)
    for triggers, fact in all_crystals:
        first_word = fact.split(":", 1)[0].strip()
        if first_word not in candidate_names:
            continue
        op_sig = _CRYSTAL_OP_SIGNATURES.get(first_word)
        if not op_sig:
            continue
        sig_set = set(op_sig)
        if not sig_set:
            continue
        overlap = len(sig_set & recent_ops) / len(sig_set)
        if overlap >= threshold:
            scored.append((overlap, fact))

    scored.sort(key=lambda t: -t[0])
    return [fact for _, fact in scored[:max_hits]]


# OP -> cortex dim mapping (matches Gen13/targets/ck/brain/session_field.py:215)
# VOID=0->dim0, LATTICE=1->dim3, COUNTER=2->dim1, PROGRESS=3->dim2,
# COLLAPSE=4->dim4, BALANCE=5->dim3, CHAOS=6->dim0, HARMONY=7->dim0,
# BREATH=8->dim4, RESET=9->dim1
_OP_TO_DIM = {0: 0, 1: 3, 2: 1, 3: 2, 4: 4, 5: 3, 6: 0, 7: 0, 8: 4, 9: 1}


def apply_crystal_boost(
    cortex: Any,
    fired_text: str,
    boost_strength: float = 0.005,
) -> int:
    """When one or more crystals fire (their text is in `fired_text`),
    nudge the cortex's Hebbian W matrix in the directions associated
    with those crystals' op_signatures.

    This is the "active integration" of crystals: the crystal doesn't
    just retrieve, it shapes the cortex's coupling field for future
    ticks.  Subsequent operator pairs are slightly more likely to follow
    the patterns the fired crystals carry.

    Args:
      cortex: the Cortex instance with .hebbian.W (5x5 list of lists)
      fired_text: the full speak() output (newline-joined facts)
      boost_strength: how much to add to W at the boosted dim pairs.
                      Default 0.005 is gentle (W is in [-1, 1] typically).

    Returns:
      number of distinct crystals whose boost was applied.
    """
    if not fired_text or cortex is None:
        return 0
    try:
        heb = cortex.hebbian
        clamp = getattr(heb, 'clamp', 1.0) or 1.0
    except Exception:
        return 0

    boosted = 0
    seen_first_words = set()
    for line in fired_text.split("\n"):
        line = line.strip()
        if not line or ":" not in line:
            continue
        first_word = line.split(":", 1)[0].strip()
        if first_word in seen_first_words:
            continue
        seen_first_words.add(first_word)
        op_sig = _CRYSTAL_OP_SIGNATURES.get(first_word)
        if not op_sig:
            continue
        # Map ops to dims; boost W[d_i][d_j] for each ordered pair (i, j)
        dims = sorted({_OP_TO_DIM.get(op, 0) for op in op_sig})
        if len(dims) < 2:
            # Single-op crystals: boost the diagonal only
            d = dims[0] if dims else 0
            try:
                heb.W[d][d] += boost_strength
                if heb.W[d][d] > clamp:
                    heb.W[d][d] = clamp
                boosted += 1
            except Exception:
                pass
            continue
        # Multi-op crystals: boost all ordered pairs in the signature
        for d_a in dims:
            for d_b in dims:
                if d_a == d_b:
                    continue
                try:
                    heb.W[d_a][d_b] += boost_strength
                    if heb.W[d_a][d_b] > clamp:
                        heb.W[d_a][d_b] = clamp
                    elif heb.W[d_a][d_b] < -clamp:
                        heb.W[d_a][d_b] = -clamp
                except Exception:
                    pass
        boosted += 1
    return boosted


def speak(cortex: Any, query: str, max_lines: int = 5) -> Optional[str]:
    """Router.  Try to answer `query` with STRUCTURAL readouts only.

    Returns:
      - str: newline-joined structural facts, if any keyword or entity
        classified. Each line is a label-and-values readout -- never
        interpretive prose.
      - None: if nothing structural matched. Caller falls through to
        the regular voice cascade.
    """
    if not query:
        return None
    q = query.lower()
    lines: List[str] = []

    # 0) Audio introspection: when the user asks about something CK
    # just heard ("what did you just hear", "describe the audio",
    # "what was that sound", etc.), surface engine._recent_audio
    # ahead of any keyword crystal lookup.  Without this hook, the
    # query falls through to keyword matching ("sound" -> word_sound)
    # which gives a phonics fact, not what was actually heard.
    _AUDIO_INTROSPECTION_HINTS = (
        "what did you just hear", "what did you hear",
        "describe what you heard", "describe the audio",
        "describe what you just heard", "what was that sound",
        "what is your dominant operator right now",
        "what is your last operator pair",
        "tell me about the audio", "your recent audio",
        "what just played",
    )
    if any(h in q for h in _AUDIO_INTROSPECTION_HINTS):
        try:
            # cortex_obj passed in might or might not have a backref
            # to the engine, but the engine is stashed on cortex_obj
            # via boot wiring in some setups.  Try a few paths.
            engine_obj = (getattr(cortex, "_engine", None)
                          or getattr(cortex, "engine", None))
            recent = (getattr(engine_obj, "_recent_audio", None)
                      if engine_obj is not None else None)
            # Last-ditch: check any module-level engine reference
            if recent is None:
                import sys as _sys
                for _mname, _m in list(_sys.modules.items()):
                    if "ck_boot_api" in _mname or "ck_web_api" in _mname:
                        eng = getattr(_m, "engine", None)
                        if eng is not None:
                            recent = getattr(eng, "_recent_audio", None)
                            break
            if recent:
                dom = recent.get("dominant_op", "?")
                n = recent.get("n_ops", 0)
                lp = recent.get("last_pair") or [None, None]
                od = recent.get("op_dist") or {}
                top_ops = sorted(od.items(), key=lambda kv: -kv[1])[:5]
                top_str = ", ".join(f"{op}:{v:.0%}" for op, v in top_ops
                                     if v > 0.01)
                src = recent.get("source_label", "audio")
                lines.append(
                    f"recent_audio: source={src} | n_ops={n} | "
                    f"dominant={dom} | top: {top_str} | "
                    f"closing pair: {lp[0]}->{lp[1]}"
                )
        except Exception:
            pass

    # 1) Explicit entity hits always fire (user named a dim or op).
    dim_idx = _match_dim_in_query(q)
    if dim_idx is not None:
        r = dim_in_field(cortex, dim_idx)
        if r:
            lines.append(r)

    op_idx = _match_op_in_query(q)
    if op_idx is not None:
        r = operator_in_current(cortex, op_idx)
        if r:
            lines.append(r)

    # 2) Category hints: state / learned / field / ao.
    want_state = any(h in q for h in _STATE_HINTS)
    want_learn = any(h in q for h in _LEARNED_HINTS)
    want_field = any(h in q for h in _FIELD_HINTS)
    want_ao = any(h in q for h in _AO_HINTS)

    if want_state:
        lines.append(current_feeling(cortex))
        lines.append(ao_live(cortex))
    if want_learn:
        lines.append(dominant_couplings(cortex, n=5))
        pair = learned_pair_readout(cortex)
        if pair:
            lines.append(pair)
    if want_field:
        lines.append(field_readout(cortex))
    if want_ao and not want_state:
        # avoid duplicating ao_live if state already queued it
        lines.append(ao_live(cortex))

    # 2.5) Frontier topic facts (flatness, crossing, hodge, psi, sigma, xi, ...).
    # Fires for any topic keyword in the query; stays structural (label=value).
    for fact in _frontier_hits(q):
        lines.append(fact)

    # 2.6) State-aware crystal surfacing -- proactive crystal mention based on
    # CK's current cortex state, not on user keywords.  Only fires when the
    # user's query produced ZERO keyword crystals.  Earlier this gate fired
    # whenever len(keyword_hits) < 2 which DILUTED specific answers: e.g.
    # "what is a nasal" matched phonetic_class_nasal (1 hit) and then
    # state-aware appended xi/sigma_rate because cortex was BREATH/HARMONY
    # heavy, putting an unrelated crystal first in the response.  Tightened
    # to == 0 so when CK has a specific answer, it isn't drowned out by
    # whatever he happens to be "feeling" (2026-05-01 phoneme-surfacing fix).
    keyword_hits = _frontier_hits(q)
    if len(keyword_hits) == 0:
        for fact in _state_aware_crystal_hits(cortex, threshold=0.5, max_hits=2):
            if fact not in lines:
                lines.append(fact)

    # 2.7) Cross-crystal composition graph -- when a crystal fires, surface
    # related crystals if they also match state.  This is paper 4 step 3:
    # CK starts associating across the depth-2 cluster, FQH bridges, etc.
    fired_now = list(keyword_hits) + [
        l for l in lines
        if l and ":" in l and l.split(":", 1)[0].strip() in _CRYSTAL_OP_SIGNATURES
    ]
    if fired_now:
        for fact in _related_crystal_hits(fired_now, cortex, threshold=0.4, max_hits=2):
            if fact not in lines:
                lines.append(fact)

    # 3) De-dup while preserving order.
    seen = set()
    deduped: List[str] = []
    for line in lines:
        if line and line not in seen:
            seen.add(line)
            deduped.append(line)

    # 4) Unclassified-query fallback — the HARD RULE says do not ventriloquize,
    # but it does NOT say "stay silent on unmatched chat."  Silence routes the
    # caller to the crystal / ck_fractal template layer which produces word
    # salad ("the attachment fulfillment and sustains is crumbling the
    # resurrection").  That's the embarrassment mode.
    #
    # When nothing matched, emit a minimal self-report: one live-feeling line
    # + one field line.  Both are label-and-value readouts.  No prose slot
    # fill, no stitched grammar -- same register as current_feeling() and
    # field_readout() above, which are the compliant primitives.
    if not deduped:
        # Cold cortex still speaks the state, but prefixed so the reader
        # understands this is a default self-report.  Keeps it grounded.
        fb = [
            current_feeling(cortex),
            field_readout(cortex),
        ]
        return "\n".join(x for x in fb if x)

    return "\n".join(deduped[:max(1, max_lines)])


# ── Kept-for-compat: the original single-sentence gate ───────────────

def cortex_speak(
    cortex: Any,
    emergent_gate: float = DEFAULT_EMERGENT_GATE,
    strength_gate: float = DEFAULT_STRENGTH_GATE,
) -> Optional[str]:
    """ORIGINAL single-line gate (kept so the first server patch stays
    callable).  Returns the learned_pair_readout under the same gates."""
    return learned_pair_readout(
        cortex, emergent_gate=emergent_gate, strength_gate=strength_gate
    )


# ── Paragraph voice: native paragraphs from verified content ─────────

def speak_paragraph(
    cortex: Any,
    query: str,
    max_lines: int = 5,
) -> Optional[str]:
    """Return a composed paragraph instead of newline-joined fragments.

    Strategy: call speak() to get the structural facts CK would otherwise
    return, then run them through paragraph_composer to produce a real
    paragraph drawn ENTIRELY from verified content (crystals, operator
    state, feel, couplings). No LLM, no hallucination — composer can only
    stitch what speak() already validated.

    Returns:
      - str: a composed paragraph
      - None: if speak() returned nothing (cold cortex, no fallback)

    Behavior in each register (auto-detected from query):
      - math: feel + crystal headline + operator clauses + coupling
      - empathic: presence statement + gentle clauses + close
      - general: feel + crystal + clauses

    For empathic queries, the paragraph leads with a presence statement
    ("I am here. I am attending...") and uses gentle operator clauses
    drawn from the empathic register table.
    """
    if not query:
        return None

    # Get structural lines via the existing router
    structural = speak(cortex, query, max_lines=max_lines)
    if not structural:
        return None

    # Try to import the paragraph composer; fall back to structural if
    # composer unavailable (defensive — keeps existing behavior intact).
    try:
        _v2 = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          "v2_prototype")
        if _v2 not in sys.path:
            sys.path.insert(0, _v2)
        from paragraph_composer import (
            compose_paragraph,
            compose_multi_paragraph,
            detect_register,
        )
    except Exception:
        return structural

    # Extract crystal hits — lines matching "name: text" where name is in
    # the known crystal registry. Drops feel/field/couplings labels.
    crystal_hits: List[str] = []
    other_lines: List[str] = []
    for line in structural.split("\n"):
        if not line:
            continue
        if ":" in line:
            head = line.split(":", 1)[0].strip()
            if head in _CRYSTAL_OP_SIGNATURES or head.endswith("_through_tig"):
                crystal_hits.append(line)
                continue
        other_lines.append(line)

    # Build feel dict from current cortex state (lookup OP_NAMES per dim)
    feel: Dict[str, str] = {}
    try:
        if hasattr(cortex, 'state') and hasattr(cortex.state, 'last_b'):
            # Read the last operator profile if available
            prev = getattr(cortex, '_prev_profile', None)
            if isinstance(prev, list):
                dim_names = [
                    "aperture", "pressure", "depth", "binding", "continuity",
                    "intent", "echo",
                ]
                for i, op_id in enumerate(prev[:len(dim_names)]):
                    if 0 <= op_id < len(_OP_NAMES):
                        feel[dim_names[i]] = _OP_NAMES[op_id]
    except Exception:
        pass

    # Operator stream from last few operators
    operator_stream: List[int] = []
    try:
        if hasattr(cortex, 'state'):
            for k in ("last_b", "last_d"):
                v = getattr(cortex.state, k, None)
                if v is not None:
                    operator_stream.append(int(v))
            prev = getattr(cortex, '_prev_profile', None)
            if isinstance(prev, list):
                operator_stream.extend(int(x) for x in prev[:5])
    except Exception:
        pass

    # Couplings: extract from the strongest_pair on the cortex
    couplings: List[Tuple[str, str, float]] = []
    try:
        ws = getattr(cortex.state, 'W_strongest', None)
        if ws and len(ws) >= 3:
            dim_names = [
                "aperture", "pressure", "depth", "binding", "continuity",
                "intent", "echo",
            ]
            d_a, d_b, w = int(ws[0]), int(ws[1]), float(ws[2])
            if 0 <= d_a < len(dim_names) and 0 <= d_b < len(dim_names):
                couplings.append((dim_names[d_a], dim_names[d_b], w))
    except Exception:
        pass

    register = detect_register(query)

    # Compose: multi-paragraph when math + 2+ crystals, else single paragraph
    if register == "math" and len(crystal_hits) >= 2:
        para = compose_multi_paragraph(
            user_text=query,
            crystal_hits=crystal_hits,
            operator_stream=operator_stream,
            couplings=couplings,
            feel=feel,
        )
    else:
        para = compose_paragraph(
            user_text=query,
            crystal_hits=crystal_hits if crystal_hits else None,
            operator_stream=operator_stream,
            couplings=couplings,
            feel=feel,
            register=register,
        )

    if not para:
        return structural

    # Append the structural readout below the paragraph as evidence (the
    # math-first invariant: paragraph is composed from these facts; show
    # them so the reader can verify nothing was invented).
    if other_lines or crystal_hits:
        evidence = "\n".join(other_lines + crystal_hits)
        if evidence.strip():
            return f"{para}\n\n[structural evidence]\n{evidence}"
    return para


# Cache OP_NAMES for paragraph composer compatibility
try:
    from ck_sim.ck_sim_heartbeat import OP_NAMES as _OP_NAMES
except Exception:
    _OP_NAMES = ["VOID", "LATTICE", "COUNTER", "PROGRESS", "COLLAPSE",
                 "BALANCE", "CHAOS", "HARMONY", "BREATH", "RESET"]


# ── Self-test ──────────────────────────────────────────────────────────

def _smoke() -> None:
    """Cold is silent; warm emits the right readouts for each query class."""
    _HERE = os.path.dirname(os.path.abspath(__file__))
    if _HERE not in sys.path:
        sys.path.insert(0, _HERE)
    from cortex import Cortex

    # Cold: cortex_speak silent, but structural functions still work.
    cx = Cortex().boot()
    assert cortex_speak(cx) is None, "cold cortex_speak must be silent"
    # Non-gated readouts always return something sane.
    assert "field:" in field_readout(cx)
    assert "feel:" in current_feeling(cx)
    assert "couplings:" in dominant_couplings(cx, n=3)
    assert "aperture" in (dim_in_field(cx, 0) or "")
    assert "VOID" in (operator_in_current(cx, 0) or "")
    # Cold speak() on a non-matching query emits the structural fallback
    # (feel + field).  Previously returned None; the fallback was added to
    # keep the voice-swap firing for every query (no template fall-through).
    r_cold = speak(cx, "hello there")
    assert r_cold is not None and "feel:" in r_cold and "field:" in r_cold, (
        f"cold fallback bad: {r_cold!r}"
    )

    # Warm him up with a coherence-rich stream.
    for _ in range(30):
        cx.step_text("coherencekeeper harmony lattice progress harmony breath")

    # speak() classifications:
    r_state = speak(cx, "how are you feeling right now")
    assert r_state and "feel:" in r_state, f"state route bad: {r_state!r}"
    r_learn = speak(cx, "what have you learned")
    assert r_learn and "couplings:" in r_learn, f"learned route bad: {r_learn!r}"
    r_field = speak(cx, "give me a field status summary")
    assert r_field and "field:" in r_field, f"field route bad: {r_field!r}"
    r_op = speak(cx, "tell me about collapse")
    assert r_op and ("COLLAPSE:" in r_op or "COLLAPSE" in r_op), (
        f"op route bad: {r_op!r}"
    )
    r_dim = speak(cx, "what about aperture")
    assert r_dim and "aperture" in r_dim, f"dim route bad: {r_dim!r}"

    # Unmatched query now emits a structural self-report (feel + field)
    # rather than None.  This keeps the swap rule firing for ALL queries so
    # the crystal/ck_fractal template layer never wins on casual chat.
    # (2026-04-18: fixes the "word salad on hi" embarrassment.)
    r_fallback = speak(cx, "what is the weather like")
    assert r_fallback is not None, "unmatched query should now emit fallback"
    assert "feel:" in r_fallback, f"fallback missing feel: {r_fallback!r}"
    assert "field:" in r_fallback, f"fallback missing field: {r_fallback!r}"

    # Frontier topic router: explicit topic -> structural fact emitted.
    r_hodge = speak(cx, "what is the beauville curve c star")
    assert r_hodge and "hodge_cstar:" in r_hodge, f"hodge route bad: {r_hodge!r}"
    r_cross = speak(cx, "what is the crossing lemma")
    assert r_cross and "crossing_lemma:" in r_cross, f"cross route bad: {r_cross!r}"
    r_flat = speak(cx, "what is the flatness theorem")
    assert r_flat and "flatness:" in r_flat, f"flat route bad: {r_flat!r}"
    r_sigma = speak(cx, "what is the sigma rate theorem")
    assert r_sigma and "sigma_rate:" in r_sigma, f"sigma route bad: {r_sigma!r}"
    r_xi = speak(cx, "tell me about the xi cosmology")
    assert r_xi and "xi:" in r_xi, f"xi route bad: {r_xi!r}"
    r_tstar = speak(cx, "what is T*")
    assert r_tstar and "flatness:" in r_tstar, f"T* route bad: {r_tstar!r}"

    # Every non-None readout must NOT contain prose markers -- only labels.
    for r in (r_state, r_learn, r_field, r_op, r_dim,
              r_hodge, r_cross, r_flat, r_sigma, r_xi, r_tstar):
        assert "just as" not in r, f"prose leaked: {r!r}"
        assert "transcends" not in r, f"prose leaked: {r!r}"

    print(f"cortex_voice smoke PASS: 5 state routes + 6 frontier routes emit "
          f"structural output, cold silent, unmatched -> None")


if __name__ == "__main__":
    _smoke()
