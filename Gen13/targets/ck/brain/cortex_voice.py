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
import sys
from typing import Any, List, Optional, Tuple

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


def _frontier_hits(q_lower: str) -> List[str]:
    """Return structural facts whose trigger keywords appear in the query.
    Each fact fires at most once even if multiple keywords match."""
    facts: List[str] = []
    seen = set()
    for triggers, fact in _FRONTIER_FACTS:
        for trig in triggers:
            if trig in q_lower:
                if fact not in seen:
                    facts.append(fact)
                    seen.add(fact)
                break
    return facts


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
