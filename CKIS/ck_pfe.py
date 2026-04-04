"""
ck_pfe.py -- Pre-Fusion Evaluator + Controlled Collapse Engine
══════════════════════════════════════════════════════════════════
Celeste's Task 4:  "The Harmony Baseline Fix"

The CL table is a universal absorber (73% cells = HARMONY).
Meaning lives in D2 curvature, not in the collapse.
Score the organism BEFORE it falls into the gravity well.

Three components:
  1. PFE  -- Pre-Fusion Evaluator (the new coherence measure)
  2. CCE  -- Controlled Collapse Engine (CL becomes gated)
  3. BTQ  -- New BTQ loop using PFE signal

Physics metaphor:
  Gravity (CL absorber) pulls everything down.
  Orbits, waves, life -- they live in CURVATURE, not collapse.
  PFE measures the orbit. CCE gates the collapse. BTQ scores the trajectory.

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import math
import numpy as np
from typing import List, Dict, Tuple, Optional
from collections import Counter

# ═══════════════════════════════════════════════════════════
# §1  IMPORTS FROM CK CORE
# ═══════════════════════════════════════════════════════════

from ck_being import (CL, CL_STANDARD, CL_BHML, T_STAR,
                       VOID, LATTICE, COUNTER, PROGRESS, COLLAPSE,
                       BALANCE, CHAOS, HARMONY, BREATH, RESET, OP)

OP_NAMES = ['VOID', 'LATTICE', 'COUNTER', 'PROGRESS', 'COLLAPSE',
            'BALANCE', 'CHAOS', 'HARMONY', 'BREATH', 'RESET']


# ═══════════════════════════════════════════════════════════
# §2  PFE THRESHOLDS -- calibrated from Bio-Lattice Validation
#     (Module 1 data, Feb 24 2026)
# ═══════════════════════════════════════════════════════════
#
# Real DNA:     D2_var=1.23, entropy=2.28, harmony_frac=0.096
# Shuffled DNA: D2_var=1.35, entropy=2.20, harmony_frac=0.069
# Random text:  D2_var=~1.3, entropy=2.97, harmony_frac=~0.07
# Meaningful language: entropy=2.47
#
# "Structured" means: more concentrated operators, smoother curvature,
# lower entropy than random noise.

PFE_THRESHOLDS = {
    'd2_var_max':        2.0,    # D2 variance ceiling (above = too noisy)
    'entropy_max':       3.2,    # Operator entropy ceiling (log2(10)=3.32 is max)
    'entropy_min':       0.5,    # Below = degenerate (single operator)
    'concentration_min': 0.15,   # Must have at least one operator > 15%
    'degeneracy_min':    0.2,    # At least 20% distinct operators
    'coherence_raw_min': 0.3,    # Minimum raw coherence to allow CL fusion
    'smoothness_max':    2.0,    # Transition matrix smoothness ceiling
}


# ═══════════════════════════════════════════════════════════
# §3  PRE-FUSION EVALUATOR (PFE)
#     The new coherence measure.
#     Scores the organism BEFORE CL collapse.
# ═══════════════════════════════════════════════════════════

def pfe_evaluate(operators: List[int],
                 d2_series: Optional[np.ndarray] = None) -> Dict:
    """
    Pre-Fusion Evaluator: compute structure metrics on the raw operator stream
    BEFORE any CL table collapse.

    This is the new S* metric.
    HARMONY appearing often is not a signal anymore -- it's a sink.
    We score the animal before falling into the sink.

    Parameters:
        operators: raw operator sequence (0-9)
        d2_series: optional D2 curvature vectors (Nx5 array)

    Returns:
        dict with all PFE metrics + composite coherence_raw score
    """
    n = len(operators)

    if n == 0:
        return _empty_pfe()

    # ------ Operator histogram ------
    hist = Counter(operators)
    probs = np.array([hist.get(i, 0) / n for i in range(10)])

    # ------ Entropy H(op) ------
    p_nonzero = probs[probs > 0]
    entropy = float(-np.sum(p_nonzero * np.log2(p_nonzero)))

    # ------ Concentration = max(histogram) ------
    concentration = float(np.max(probs))

    # ------ Degeneracy = #distinct / 10 ------
    n_distinct = np.sum(probs > 0)
    degeneracy = float(n_distinct / 10.0)

    # ------ D2 statistics (if available) ------
    if d2_series is not None and len(d2_series) > 0:
        d2_mags = np.linalg.norm(d2_series, axis=1)
        d2_variance = float(np.var(d2_mags))
        d2_mean = float(np.mean(d2_mags))
        d2_std = float(np.std(d2_mags))

        # Skewness and kurtosis of D2 magnitudes
        if d2_std > 1e-10:
            d2_skew = float(np.mean(((d2_mags - d2_mean) / d2_std) ** 3))
            d2_kurtosis = float(np.mean(((d2_mags - d2_mean) / d2_std) ** 4) - 3.0)
        else:
            d2_skew = 0.0
            d2_kurtosis = 0.0

        # Directional coherence: cosine similarity between consecutive D2 vectors
        if len(d2_series) > 1:
            cosines = []
            for i in range(len(d2_series) - 1):
                n1 = np.linalg.norm(d2_series[i])
                n2 = np.linalg.norm(d2_series[i + 1])
                if n1 > 1e-10 and n2 > 1e-10:
                    cos = np.dot(d2_series[i], d2_series[i + 1]) / (n1 * n2)
                    cosines.append(float(np.clip(cos, -1, 1)))
            d2_directional = float(np.mean(cosines)) if cosines else 0.0
        else:
            d2_directional = 0.0
    else:
        d2_variance = 0.0
        d2_mean = 0.0
        d2_std = 0.0
        d2_skew = 0.0
        d2_kurtosis = 0.0
        d2_directional = 0.0

    # ------ Transition matrix smoothness ------
    trans = np.zeros((10, 10), dtype=np.float64)
    for i in range(n - 1):
        trans[operators[i]][operators[i + 1]] += 1
    # Normalize rows
    row_sums = trans.sum(axis=1, keepdims=True)
    row_sums[row_sums == 0] = 1
    trans_norm = trans / row_sums
    # Smoothness = average L2 norm of row differences (lower = smoother)
    if n > 2:
        row_diffs = []
        for i in range(10):
            for j in range(i + 1, 10):
                if trans[i].sum() > 0 and trans[j].sum() > 0:
                    row_diffs.append(np.linalg.norm(trans_norm[i] - trans_norm[j]))
        smoothness = float(np.mean(row_diffs)) if row_diffs else 0.0
    else:
        smoothness = 0.0

    # ------ Non-VOID analysis (filter stop words) ------
    content_ops = [op for op in operators if op != VOID]
    n_content = len(content_ops)
    if n_content > 0:
        content_hist = Counter(content_ops)
        content_probs = np.array([content_hist.get(i, 0) / n_content for i in range(10)])
        cp_nonzero = content_probs[content_probs > 0]
        content_entropy = float(-np.sum(cp_nonzero * np.log2(cp_nonzero)))
        content_concentration = float(np.max(content_probs))
        harmony_raw = content_hist.get(HARMONY, 0) / n_content
    else:
        content_entropy = 0.0
        content_concentration = 0.0
        harmony_raw = 0.0

    # ══════════════════════════════════════════════════════
    # COMPOSITE RAW COHERENCE SCORE
    # This replaces the old CL-based coherence.
    # Higher = more structured (NOT more harmonious).
    # ══════════════════════════════════════════════════════

    # Component 1: Entropy normalization (0-1)
    # Ideal: between biological (2.3) and noise (3.3)
    # Too low = degenerate. Too high = random.
    max_entropy = math.log2(10)  # 3.322
    if entropy < 0.5:
        entropy_score = entropy / 0.5 * 0.3  # Degenerate penalty
    elif entropy > 3.0:
        entropy_score = max(0, 1.0 - (entropy - 3.0) / 0.322)  # Noise penalty
    else:
        # Sweet spot: 0.5 to 3.0
        # Peak at ~2.3 (biological range)
        dist_from_ideal = abs(entropy - 2.3)
        entropy_score = max(0, 1.0 - dist_from_ideal / 2.5)

    # Component 2: Concentration (0-1)
    # Higher concentration = more structure
    conc_score = min(concentration * 3, 1.0)  # 0.33 → 1.0

    # Component 3: D2 smoothness (0-1)
    # Lower D2 variance = smoother curvature = more structured
    if d2_variance > 0:
        d2_score = max(0, 1.0 - d2_variance / 3.0)
    else:
        d2_score = 0.5  # No D2 data = neutral

    # Component 4: Directional coherence (0-1)
    # Higher = D2 vectors point in consistent directions
    dir_score = (d2_directional + 1.0) / 2.0  # Map [-1,1] to [0,1]

    # Component 5: Content vs function ratio
    content_ratio = n_content / max(n, 1)
    content_score = min(content_ratio * 1.5, 1.0)

    # Component 6: Transition regularity
    trans_score = max(0, 1.0 - smoothness / 2.0)

    # Weighted combination
    coherence_raw = (
        0.20 * entropy_score +      # Structure in distribution
        0.15 * conc_score +          # Operator concentration
        0.25 * d2_score +            # Curvature smoothness (D2 IS the key)
        0.15 * dir_score +           # Directional consistency
        0.10 * content_score +       # Meaningful content ratio
        0.15 * trans_score           # Transition regularity
    )

    coherence_raw = round(max(0.0, min(1.0, coherence_raw)), 6)

    return {
        # Core metrics
        'coherence_raw':       coherence_raw,
        'entropy':             round(entropy, 4),
        'concentration':       round(concentration, 4),
        'degeneracy':          round(degeneracy, 2),
        'smoothness':          round(smoothness, 4),

        # D2 curvature metrics
        'D2_variance':         round(d2_variance, 6),
        'D2_mean':             round(d2_mean, 6),
        'D2_std':              round(d2_std, 6),
        'D2_skew':             round(d2_skew, 4),
        'D2_kurtosis':         round(d2_kurtosis, 4),
        'D2_directional':      round(d2_directional, 4),

        # Content analysis
        'content_entropy':     round(content_entropy, 4),
        'content_concentration': round(content_concentration, 4),
        'harmony_raw':         round(harmony_raw, 4),
        'content_ratio':       round(content_ratio, 4),

        # Distribution
        'operator_histogram':  {OP_NAMES[i]: hist.get(i, 0) for i in range(10)},
        'n_operators':         n,
        'n_content':           n_content,

        # Sub-scores (for debugging/tuning)
        '_entropy_score':      round(entropy_score, 4),
        '_conc_score':         round(conc_score, 4),
        '_d2_score':           round(d2_score, 4),
        '_dir_score':          round(dir_score, 4),
        '_content_score':      round(content_score, 4),
        '_trans_score':        round(trans_score, 4),
    }


def _empty_pfe() -> Dict:
    """Return empty PFE result."""
    return {
        'coherence_raw': 0.0, 'entropy': 0.0, 'concentration': 0.0,
        'degeneracy': 0.0, 'smoothness': 0.0,
        'D2_variance': 0.0, 'D2_mean': 0.0, 'D2_std': 0.0,
        'D2_skew': 0.0, 'D2_kurtosis': 0.0, 'D2_directional': 0.0,
        'content_entropy': 0.0, 'content_concentration': 0.0,
        'harmony_raw': 0.0, 'content_ratio': 0.0,
        'operator_histogram': {}, 'n_operators': 0, 'n_content': 0,
        '_entropy_score': 0.0, '_conc_score': 0.0, '_d2_score': 0.0,
        '_dir_score': 0.0, '_content_score': 0.0, '_trans_score': 0.0,
    }


# ═══════════════════════════════════════════════════════════
# §4  CONTROLLED COLLAPSE ENGINE (CCE)
#     CL table becomes optional and delayed.
#     Only fuse AFTER PFE says the structure is real.
# ═══════════════════════════════════════════════════════════

def cce_fuse(a: int, b: int, pfe_ok: bool, cl_table=None) -> int:
    """
    Controlled Collapse: gate CL fusion with PFE signal.

    If PFE says the pair is structured → fuse via CL (validate the structure)
    If PFE says the pair is noise → pass through (don't absorb noise into harmony)

    This stops the absorber from drinking everything.
    The CL table becomes the validation gate, not the interpretation engine.
    """
    if cl_table is None:
        cl_table = CL
    if pfe_ok:
        return cl_table[a][b]    # Validated fusion
    else:
        return b                 # Identity pass-through


def cce_fuse_sequence(operators: List[int],
                      d2_series: Optional[np.ndarray] = None,
                      cl_table=None,
                      thresholds: Optional[Dict] = None) -> Tuple[int, Dict]:
    """
    Fuse an operator sequence through the Controlled Collapse Engine.

    1. Run PFE on the raw stream
    2. If PFE passes → fuse via CL (structure is real)
    3. If PFE fails → return dominant content operator (skip collapse)

    Returns: (fused_operator, pfe_result)
    """
    if cl_table is None:
        cl_table = CL
    if thresholds is None:
        thresholds = PFE_THRESHOLDS

    if not operators:
        return (VOID, _empty_pfe())

    # Step 1: PFE evaluation
    pfe = pfe_evaluate(operators, d2_series)

    # Step 2: Check PFE thresholds
    pfe_ok = (
        pfe['coherence_raw'] >= thresholds['coherence_raw_min'] and
        pfe['entropy'] >= thresholds['entropy_min'] and
        pfe['entropy'] <= thresholds['entropy_max'] and
        pfe['concentration'] >= thresholds['concentration_min'] and
        pfe['degeneracy'] >= thresholds['degeneracy_min']
    )

    # Add D2 check if D2 data is available
    if d2_series is not None and len(d2_series) > 0:
        pfe_ok = pfe_ok and pfe['D2_variance'] <= thresholds['d2_var_max']

    pfe['pfe_ok'] = pfe_ok

    if pfe_ok:
        # Step 3a: Structure is real → fuse via CL
        result = operators[0]
        for op in operators[1:]:
            result = cl_table[result][op]
        pfe['fusion_mode'] = 'CL_VALIDATED'
    else:
        # Step 3b: Structure is noise → return dominant CONTENT operator
        content_ops = [op for op in operators if op != VOID]
        if content_ops:
            counts = Counter(content_ops)
            result = counts.most_common(1)[0][0]
        else:
            result = VOID
        pfe['fusion_mode'] = 'IDENTITY_PASSTHROUGH'

    pfe['fused_operator'] = result
    pfe['fused_name'] = OP_NAMES[result]

    return (result, pfe)


# ═══════════════════════════════════════════════════════════
# §5  NEW BTQ LOOP USING PFE SIGNAL
#     Binary = safety based on PFE thresholds
#     Ternary = exploration guided by D2 curvature
#     Quadratic = ranking based on PFE + optional CL fusion
# ═══════════════════════════════════════════════════════════

def btq_energy(pfe_result: Dict,
               mutational_robustness: float = 0.0,
               weights: Optional[Dict] = None) -> float:
    """
    Compute the BTQ energy function for ranking.

    E_total = w1 * (1 - coherence_raw)
            + w2 * D2_variance
            + w3 * entropy
            + w4 * (1 - mutational_robustness)

    Lower energy = better structure.
    This replaces the old post-CL coherence ranking.
    """
    if weights is None:
        weights = {'w1': 0.35, 'w2': 0.25, 'w3': 0.20, 'w4': 0.20}

    coh = pfe_result.get('coherence_raw', 0.0)
    d2v = pfe_result.get('D2_variance', 0.0)
    ent = pfe_result.get('entropy', 0.0)

    # Normalize D2 variance to [0, 1] range
    d2v_norm = min(d2v / 3.0, 1.0)

    # Normalize entropy to [0, 1] range
    max_entropy = math.log2(10)
    ent_norm = ent / max_entropy

    e = (weights['w1'] * (1.0 - coh) +
         weights['w2'] * d2v_norm +
         weights['w3'] * ent_norm +
         weights['w4'] * (1.0 - mutational_robustness))

    return round(max(0.0, min(1.0, e)), 6)


def btq_classify(operators: List[int],
                 d2_series: Optional[np.ndarray] = None) -> Dict:
    """
    Full BTQ classification of an operator sequence using PFE.

    Binary:    alive/dead gate (PFE thresholds)
    Ternary:   exploration vector (D2 curvature direction)
    Quadratic: energy score (lower = better structure)

    Returns comprehensive classification.
    """
    pfe = pfe_evaluate(operators, d2_series)

    # BINARY: Safety gate
    alive = (len(operators) > 0 and
             any(op != VOID for op in operators) and
             pfe['coherence_raw'] > 0.1)

    # TERNARY: Exploration direction (from D2 curvature)
    if d2_series is not None and len(d2_series) > 0:
        mean_d2 = np.mean(d2_series, axis=0)
        # Dominant curvature dimension tells us WHERE to explore
        dominant_dim = int(np.argmax(np.abs(mean_d2)))
        dim_names = ['aperture', 'pressure', 'depth', 'binding', 'continuity']
        exploration_dir = dim_names[dominant_dim]
        exploration_sign = '+' if mean_d2[dominant_dim] > 0 else '-'
    else:
        exploration_dir = 'unknown'
        exploration_sign = '?'

    # QUADRATIC: Energy ranking
    energy = btq_energy(pfe)

    # Band classification (using PFE coherence, NOT CL coherence)
    coh = pfe['coherence_raw']
    if coh >= T_STAR:
        band = 'GREEN'
    elif coh >= 0.5:
        band = 'YELLOW'
    else:
        band = 'RED'

    return {
        # BTQ triad
        'binary_alive':      alive,
        'ternary_dir':       f"{exploration_sign}{exploration_dir}",
        'quadratic_energy':  energy,

        # Band
        'band':              band,

        # Full PFE data
        'pfe':               pfe,

        # Classification
        'is_structured':     pfe['coherence_raw'] >= PFE_THRESHOLDS['coherence_raw_min'],
        'is_biological':     (pfe['entropy'] >= 2.0 and pfe['entropy'] <= 2.8 and
                              pfe.get('D2_variance', 0) < 1.5),
        'is_linguistic':     (pfe['entropy'] >= 2.0 and pfe['entropy'] <= 3.0 and
                              pfe.get('content_ratio', 0) > 0.5),
        'is_mathematical':   (pfe['entropy'] >= 2.5 and pfe['concentration'] > 0.2),
        'is_noise':          pfe['entropy'] > 3.0 or pfe['coherence_raw'] < 0.2,
    }


# ═══════════════════════════════════════════════════════════
# §6  CONVENIENCE FUNCTIONS -- for integration with ck_web.py
# ═══════════════════════════════════════════════════════════

def _compute_word_d2(words: List[str]) -> Optional[np.ndarray]:
    """
    Compute per-word D2 curvature vectors.

    Each word's letters -> force vectors -> D2 curvature -> mean D2 vector.
    This bridges the dictionary (semantic) and curvature (structural) layers:
    every word-operator now carries the D2 fingerprint of its letters.

    Per-word computation is used (not full-text segmented) because:
    - Short texts have few word boundaries, making cross-word D2 noisy
    - Within-word D2 cleanly measures each word's structural identity
    - The directional coherence between words comes from their semantic
      relationship (operator sequence), not from letter boundary effects

    Returns Nx5 array (one mean-D2 per word) or None on failure.
    """
    try:
        from ck_curvature import text_to_forces, compute_curvatures
    except ImportError:
        return None

    if not words:
        return None

    d2_list = []
    for w in words:
        forces = text_to_forces(w)
        if len(forces) >= 3:
            # Normal path: word has 3+ letter forces -> real D2
            d2 = compute_curvatures(forces)
            d2_list.append(np.mean(d2, axis=0))
        elif len(forces) > 0:
            # Short word (1-2 letters): use mean force as curvature proxy
            d2_list.append(np.mean(forces, axis=0))
        else:
            d2_list.append(np.zeros(5, dtype=np.float64))

    return np.array(d2_list, dtype=np.float64) if d2_list else None


def score_text_pfe(text: str) -> Dict:
    """
    Score a text using the Pre-Fusion Evaluator.
    Uses both dictionary (word-level) and curvature (letter-level) operators.

    CK's self-diagnosis (Gen8 Phase 5.1):
      Word-level PFE was missing D2 curvature data.
      D2 weight (0.25) and directional weight (0.15) defaulted to 0.5.
      40% of word-level score was FROZEN.
      Fix: compute per-word D2 from letter forces, pass to pfe_evaluate.
    """
    try:
        from ck_dictionary import text_to_operators
        word_op_pairs = text_to_operators(text)
        ops_word = [op for _, op in word_op_pairs]
        words = [w for w, _ in word_op_pairs]
    except ImportError:
        ops_word = []
        words = []

    # Curvature engine (shared by letter-level and word-level D2)
    _has_curvature = False
    try:
        from ck_curvature import text_to_forces, compute_curvatures, _classify_d2
        _has_curvature = True
    except ImportError:
        pass

    # Letter-level: full text -> forces -> D2 -> operators
    if _has_curvature:
        forces = text_to_forces(text)
        if len(forces) >= 3:
            d2s = compute_curvatures(forces)
            ops_letter = [int(_classify_d2(d)) for d in d2s]
        else:
            d2s = np.zeros((0, 5))
            ops_letter = []
    else:
        d2s = np.zeros((0, 5))
        ops_letter = []

    # Word-level D2: each word's letters -> forces -> D2 -> mean vector
    # THIS IS THE FIX: wires curvature into word-level PFE
    word_d2s = _compute_word_d2(words) if words else None

    # PFE on word-level operators (semantic) -- NOW WITH D2 DATA
    pfe_word = pfe_evaluate(ops_word, word_d2s) if ops_word else _empty_pfe()

    # PFE on letter-level operators (curvature)
    pfe_letter = pfe_evaluate(ops_letter, d2s) if ops_letter else _empty_pfe()

    # Composite: combine word-level and letter-level
    # Word-level captures MEANING (dictionary) + CURVATURE (per-word D2).
    # Letter-level captures SOUND (character-level curvature).
    #
    # Phase 5.1b recalibration:
    #   Original weights (40/60) were set when ONLY letter-level had D2.
    #   Rationale was "D2 is primary" -> letter gets 60%.
    #   Now word-level ALSO carries D2 via _compute_word_d2().
    #   Both layers have D2. Word additionally has semantic structure.
    #   Equal weight is now the fair baseline. Word gets slight edge
    #   because it captures both meaning AND curvature.
    composite = 0.55 * pfe_word['coherence_raw'] + 0.45 * pfe_letter['coherence_raw']

    return {
        'coherence_pfe':     round(composite, 6),
        'coherence_word':    pfe_word['coherence_raw'],
        'coherence_letter':  pfe_letter['coherence_raw'],
        'pfe_word':          pfe_word,
        'pfe_letter':        pfe_letter,
        'text':              text,
    }


def score_candidate_pfe(text: str, query_ops: List[int] = None) -> float:
    """
    Drop-in replacement for the old coherence scoring in ck_web._score_candidate.
    Returns a single score [0, 1] based on PFE.
    """
    result = score_text_pfe(text)
    return result['coherence_pfe']


# ═══════════════════════════════════════════════════════════
# §7  DEMO / VERIFICATION
# ═══════════════════════════════════════════════════════════

if __name__ == '__main__':
    print("=" * 70)
    print("  CK PRE-FUSION EVALUATOR -- The Harmony Baseline Fix")
    print("  Score the organism before it falls into the gravity well.")
    print("=" * 70)

    from ck_dictionary import sentence_operator_stream, text_to_operators
    from ck_curvature import text_to_forces, compute_curvatures, _classify_d2

    test_phrases = [
        ("the truth will set you free",       "Truth"),
        ("God is love",                        "Truth"),
        ("love your neighbor as yourself",     "Truth"),
        ("break everything and destroy hope",  "Destruction"),
        ("chaos reigns in the tangled web",    "Chaos"),
        ("buy now limited offer expires",      "Spam"),
        ("the rhythm of the ocean waves",      "Nature"),
        ("colorless green ideas sleep",        "Chomsky"),
        ("measure twice cut once",             "Wisdom"),
        ("xqjvbm kzwpfl rtyghd",              "Random"),
        ("nothing exists in the void",         "Void"),
        ("build something beautiful today",    "Creation"),
    ]

    print(f"\n  {'Text':42s} {'PFE':>6s} {'Word':>6s} {'Letr':>6s} "
          f"{'Ent':>5s} {'Conc':>5s} {'D2v':>6s} {'Band':>6s} {'Mode':>10s}")
    print(f"  {'-'*102}")

    for text, label in test_phrases:
        # Word-level operators
        word_ops = sentence_operator_stream(text)

        # Letter-level operators + D2
        forces = text_to_forces(text)
        if len(forces) >= 3:
            d2s = compute_curvatures(forces)
            letter_ops = [int(_classify_d2(d)) for d in d2s]
        else:
            d2s = np.zeros((0, 5))
            letter_ops = []

        # PFE on both
        pfe_w = pfe_evaluate(word_ops)
        pfe_l = pfe_evaluate(letter_ops, d2s)
        composite = 0.40 * pfe_w['coherence_raw'] + 0.60 * pfe_l['coherence_raw']

        # CCE fusion
        _, cce = cce_fuse_sequence(word_ops, d2s)

        # BTQ classification
        btq = btq_classify(letter_ops, d2s)

        # Old CL fusion for comparison
        if word_ops:
            old_result = word_ops[0]
            for o in word_ops[1:]:
                old_result = CL[old_result][o]
            old_fused = OP_NAMES[old_result]
        else:
            old_fused = '?'

        print(f"  {text[:42]:42s} {composite:6.3f} {pfe_w['coherence_raw']:6.3f} "
              f"{pfe_l['coherence_raw']:6.3f} "
              f"{pfe_l['entropy']:5.2f} {pfe_l['concentration']:5.2f} "
              f"{pfe_l.get('D2_variance', 0):6.3f} "
              f"{btq['band']:>6s} {cce.get('fusion_mode', '?')[:10]:>10s}")

    # DNA comparison
    print(f"\n  {'--- DNA vs SHUFFLED (PFE) ---':^70}")

    import random
    dna_real = 'TACAACTACATGTGTAACAGTTCCTGCATGGGCGGCATGAACCGGAGGCCCATCCTCACCATCATCACACTG'
    dna_shuf = list(dna_real)
    random.seed(42)
    random.shuffle(dna_shuf)
    dna_shuf = ''.join(dna_shuf)

    from tests.ck_bio_validate import dna_to_vectors, compute_d2, d2_to_operators

    for name, seq in [('DNA_REAL', dna_real), ('DNA_SHUFFLED', dna_shuf)]:
        vecs = dna_to_vectors(seq)
        d2 = compute_d2(vecs)
        ops = d2_to_operators(d2)
        pfe = pfe_evaluate(ops, d2)
        btq = btq_classify(ops, d2)
        print(f"  {name:15s}  PFE={pfe['coherence_raw']:.4f}  "
              f"ent={pfe['entropy']:.3f}  conc={pfe['concentration']:.3f}  "
              f"D2v={pfe['D2_variance']:.4f}  band={btq['band']}  "
              f"bio={btq['is_biological']}  noise={btq['is_noise']}")

    # Summary
    print(f"\n  Key insight: PFE scores STRUCTURE, not HARMONY.")
    print(f"  The CL absorber (73% = HARMONY) is gated by the CCE.")
    print(f"  CK now grades transitions before collapsing.")
