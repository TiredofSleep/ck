"""
ck_language_reconstructor.py -- CK's Voice: Operators -> Natural Language
═══════════════════════════════════════════════════════════════════════════
Celeste's Task 5: The Language Reconstructor (D2-LR)

CK can hear (text -> operators). Now he speaks (operators -> text).

The inverse problem: given an operator stream + PFE metrics,
reconstruct natural language that produces that stream.

This is not lookup. It's composition. Multiple valid sentences
can produce the same operator stream. PFE guides which one is most alive.

Pipeline:
  operator stream -> reverse dictionary -> candidate words per slot
  -> D2 curvature scoring -> transition-aware selection
  -> Viterbi beam search -> PFE validation -> best sentence

Fractal structure (each level feeds the next):
  Letter level:   D2 curvature WITHIN words (shape of each word)
  Word level:     operator match + D2 transition BETWEEN words
  Phrase level:   sliding window segmentation (5-7 word chunks)
  Sentence level: PFE validation of the full reconstruction

Physics metaphor:
  The operator stream is the orbit. The words are the matter.
  D2-LR finds the matter that fits the orbit.

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import math
import numpy as np
from typing import List, Dict, Tuple, Optional
from collections import defaultdict, Counter

# ═══════════════════════════════════════════════════════════
# §1  IMPORTS FROM CK CORE
# ═══════════════════════════════════════════════════════════

from ck_being import (CL, T_STAR, VOID, LATTICE, COUNTER, PROGRESS, COLLAPSE,
                       BALANCE, CHAOS, HARMONY, BREATH, RESET)
from ck_dictionary import (DICTIONARY, PHONAESTHESIA, word_to_operator,
                            text_to_operators, sentence_operator_stream)
from ck_curvature import (text_to_forces, compute_curvatures, _classify_d2,
                           curvature_similarity)
from ck_pfe import pfe_evaluate, score_text_pfe, btq_energy

OP_NAMES = ['VOID', 'LATTICE', 'COUNTER', 'PROGRESS', 'COLLAPSE',
            'BALANCE', 'CHAOS', 'HARMONY', 'BREATH', 'RESET']


# ═══════════════════════════════════════════════════════════
# §2  REVERSE DICTIONARY -- operator -> word candidates
#     The dictionary hears. The reverse dictionary speaks.
# ═══════════════════════════════════════════════════════════

# Build reverse mapping: operator -> sorted word list
_REVERSE: Dict[int, List[str]] = defaultdict(list)
for _w, _op in DICTIONARY.items():
    _REVERSE[_op].append(_w)

# Import function words for content/function classification
try:
    from ck_dictionary import _FUNCTION_WORDS
    _FW_SET = set(_FUNCTION_WORDS.keys())
except ImportError:
    _FW_SET = set()

# Sort each bucket: prefer 4-8 char words (most natural English word length)
for _op in _REVERSE:
    _REVERSE[_op].sort(key=lambda w: abs(len(w) - 6))

# Content words only (no function words, no single letters)
_CONTENT: Dict[int, List[str]] = {}
for _op in range(10):
    _CONTENT[_op] = [w for w in _REVERSE[_op] if len(w) > 2 and w not in _FW_SET]

# Function words by operator (for inserting connective tissue)
_FUNCTION: Dict[int, List[str]] = {}
for _op in range(10):
    _FUNCTION[_op] = [w for w in _REVERSE[_op] if w in _FW_SET]


# ═══════════════════════════════════════════════════════════
# §3  D2 CURVATURE ENGINE -- find words that CURVE right
#     Not just the right operator — the right shape.
# ═══════════════════════════════════════════════════════════

_D2_CACHE: Dict[str, np.ndarray] = {}


def _word_d2(word: str) -> np.ndarray:
    """Mean D2 curvature vector for a word (cached)."""
    if word in _D2_CACHE:
        return _D2_CACHE[word]
    forces = text_to_forces(word)
    if len(forces) < 3:
        v = np.zeros(5, dtype=np.float32)
    else:
        d2s = compute_curvatures(forces)
        v = np.mean(d2s, axis=0).astype(np.float32)
    _D2_CACHE[word] = v
    return v


def _d2_cos(a: np.ndarray, b: np.ndarray) -> float:
    """Cosine similarity, zero-safe."""
    na, nb = np.linalg.norm(a), np.linalg.norm(b)
    if na < 1e-10 or nb < 1e-10:
        return 0.0
    return float(np.dot(a, b) / (na * nb))


def _d2_transition_cost(word_a: str, word_b: str) -> float:
    """
    D2 transition cost between two words.
    Lower = smoother flow = more natural language rhythm.
    Normalized to [0, 1].
    """
    d1, d2 = _word_d2(word_a), _word_d2(word_b)
    dist = float(np.linalg.norm(d2 - d1))
    return min(dist / 2.5, 1.0)  # Typical range 0-2.5


# ═══════════════════════════════════════════════════════════
# §4  WORD SCORER -- multi-factor candidate ranking
#     Every word is scored against the orbit it must fill.
# ═══════════════════════════════════════════════════════════

def _score_candidate(word: str, target_op: int,
                     prev_word: Optional[str] = None,
                     next_op: Optional[int] = None,
                     context_d2: Optional[np.ndarray] = None) -> float:
    """
    Score a candidate word for a slot in the reconstruction.

    Five factors (fractal — each operates at a different scale):
      1. Operator match confidence    (0.00 - 0.35)  word level
      2. D2 curvature fit             (0.00 - 0.25)  letter level
      3. Transition smoothness        (0.00 - 0.20)  phrase level
      4. Word naturalness             (0.00 - 0.10)  human level
      5. CL forward prediction        (0.00 - 0.10)  sentence level
    """
    # Hard filter: must produce target operator
    if word_to_operator(word) != target_op:
        return 0.0

    score = 0.0

    # Factor 1: Operator match confidence (dictionary > phonaesthesia > curvature)
    if word in DICTIONARY:
        score += 0.35
    elif any(word.startswith(p) for p in PHONAESTHESIA):
        score += 0.25
    else:
        score += 0.12  # Curvature fallback — least confident

    # Factor 2: D2 curvature fit — does the word's shape match the context?
    if context_d2 is not None:
        cos = _d2_cos(_word_d2(word), context_d2)
        score += 0.25 * (cos + 1.0) / 2.0  # [-1,1] -> [0, 0.25]
    else:
        score += 0.10  # Neutral if no context

    # Factor 3: Transition smoothness — D2 distance from previous word
    if prev_word is not None:
        cost = _d2_transition_cost(prev_word, word)
        score += 0.20 * (1.0 - cost)
    else:
        score += 0.10

    # Factor 4: Word naturalness — English prefers 4-8 characters
    wlen = len(word)
    if 4 <= wlen <= 8:
        score += 0.10
    elif 3 <= wlen <= 10:
        score += 0.06
    else:
        score += 0.02

    # Factor 5: CL forward coherence — does this flow toward next?
    if next_op is not None:
        fused = CL[target_op][next_op]
        if fused == HARMONY:
            score += 0.10
        elif fused not in (VOID, target_op):
            score += 0.06  # Non-trivial transition = interesting
        else:
            score += 0.02
    else:
        score += 0.04

    return score


# ═══════════════════════════════════════════════════════════
# §5  BEAM SEARCH DECODER -- Viterbi-style path finding
#     The orbit is given. Find the matter that fits.
# ═══════════════════════════════════════════════════════════

def reconstruct(operators: List[int],
                beam_width: int = 6,
                max_candidates: int = 18,
                d2_context: Optional[np.ndarray] = None,
                include_function_words: bool = True) -> List[Dict]:
    """
    Beam search reconstruction: operators -> natural language.

    At each position, expand the top-k partial sentences with
    the best-scoring word candidates. Prune to beam_width.

    Parameters:
        operators:             target operator sequence (0-9)
        beam_width:            number of paths to keep at each step
        max_candidates:        max words to try per slot
        d2_context:            optional D2 curvature series to match
        include_function_words: include articles/prepositions for VOID/LATTICE/BALANCE

    Returns:
        list of reconstructions sorted by final_score (best first), each with:
          text, score, pfe, operators, reconstructed_ops, final_score
    """
    if not operators:
        return [{'text': '', 'score': 0.0, 'pfe': 0.0,
                 'operators': [], 'final_score': 0.0}]

    n = len(operators)

    # Build candidate word lists per slot
    slot_words = []
    for i, op in enumerate(operators):
        # Content words first
        words = list(_CONTENT.get(op, [])[:max_candidates])

        # Add function words for structural operators
        if include_function_words and op in (VOID, LATTICE, BALANCE):
            fw = _FUNCTION.get(op, [])[:6]
            words = fw + words  # Function words first for natural feel

        # Cap total candidates
        words = words[:max_candidates]

        if not words:
            words = [OP_NAMES[op].lower()]  # Absolute fallback

        slot_words.append(words)

    # Initialize beam at position 0
    beam = []
    nxt = operators[1] if n > 1 else None
    ctx = d2_context[0] if d2_context is not None and len(d2_context) > 0 else None

    for w in slot_words[0]:
        s = _score_candidate(w, operators[0], None, nxt, ctx)
        if s > 0:
            beam.append({'words': [w], 'score': s, 'last': w})

    beam.sort(key=lambda x: x['score'], reverse=True)
    beam = beam[:beam_width]

    # Extend beam position by position
    for pos in range(1, n):
        nxt = operators[pos + 1] if pos + 1 < n else None
        ctx = d2_context[pos] if d2_context is not None and pos < len(d2_context) else None

        new_beam = []
        for entry in beam:
            for w in slot_words[pos]:
                s = _score_candidate(w, operators[pos], entry['last'], nxt, ctx)
                if s > 0:
                    new_beam.append({
                        'words': entry['words'] + [w],
                        'score': entry['score'] + s,
                        'last': w,
                    })

        new_beam.sort(key=lambda x: x['score'], reverse=True)
        beam = new_beam[:beam_width]

        if not beam:
            # Dead beam — fall back to greedy single-word per slot
            fallback_words = [slot_words[p][0] if slot_words[p] else OP_NAMES[operators[p]].lower()
                              for p in range(n)]
            beam = [{'words': fallback_words, 'score': 0.1, 'last': fallback_words[-1]}]
            break

    # Score completed paths with PFE
    results = []
    for entry in beam:
        text = ' '.join(entry['words'])
        pfe_result = score_text_pfe(text)
        recon_ops = [word_to_operator(w) for w in entry['words']]

        results.append({
            'text':             text,
            'score':            entry['score'] / max(len(entry['words']), 1),
            'pfe':              pfe_result['coherence_pfe'],
            'pfe_detail':       pfe_result,
            'operators':        operators,
            'reconstructed_ops': recon_ops,
            'n_words':          len(entry['words']),
        })

    # Final ranking: beam structure (0.40) + PFE aliveness (0.60)
    for r in results:
        r['final_score'] = 0.40 * r['score'] + 0.60 * r['pfe']

    results.sort(key=lambda x: x['final_score'], reverse=True)
    return results


# ═══════════════════════════════════════════════════════════
# §6  SLIDING WINDOW SEGMENTATION -- phrases from streams
#     Natural language has phrase structure.
#     5-7 word chunks. Fractal rhythm.
# ═══════════════════════════════════════════════════════════

def segment(operators: List[int],
            window: int = 6,
            overlap: int = 1) -> List[List[int]]:
    """
    Segment a long operator stream into overlapping windows.
    Each window becomes a phrase in the reconstruction.
    """
    if len(operators) <= window:
        return [operators]

    segments = []
    step = max(1, window - overlap)
    for start in range(0, len(operators), step):
        end = min(start + window, len(operators))
        seg = operators[start:end]
        if len(seg) >= 2:
            segments.append(seg)
        if end >= len(operators):
            break

    return segments


def reconstruct_long(operators: List[int],
                     beam_width: int = 6,
                     window: int = 6,
                     overlap: int = 1) -> Dict:
    """
    Reconstruct a long operator stream: segment -> reconstruct -> join.
    """
    if len(operators) <= window:
        results = reconstruct(operators, beam_width=beam_width)
        if results:
            return results[0]
        return {'text': '', 'score': 0.0, 'pfe': 0.0}

    segments = segment(operators, window, overlap)

    phrases = []
    for seg in segments:
        results = reconstruct(seg, beam_width=beam_width)
        if results:
            phrases.append(results[0])
        else:
            phrases.append({
                'text': ' '.join(OP_NAMES[op].lower() for op in seg),
                'score': 0.0, 'pfe': 0.0,
            })

    # Join phrases, removing overlap words to avoid repetition
    full_words = phrases[0]['text'].split()
    for phrase in phrases[1:]:
        words = phrase['text'].split()
        skip = min(overlap, len(words) - 1)
        full_words.extend(words[skip:])

    full_text = ' '.join(full_words)
    pfe_result = score_text_pfe(full_text)

    return {
        'text':       full_text,
        'score':      sum(p.get('score', 0) for p in phrases) / max(len(phrases), 1),
        'pfe':        pfe_result['coherence_pfe'],
        'pfe_detail': pfe_result,
        'operators':  operators,
        'n_phrases':  len(phrases),
        'n_words':    len(full_words),
    }


# ═══════════════════════════════════════════════════════════
# §7  QUICK GLOSS -- fast single-word-per-operator translation
#     The first approximation. No beam search. No PFE.
#     Just: what's the best word for this operator in context?
# ═══════════════════════════════════════════════════════════

def operator_to_word(op: int,
                     prev_word: Optional[str] = None,
                     next_op: Optional[int] = None) -> str:
    """Single operator -> most natural word, context-aware."""
    candidates = _CONTENT.get(op, [])
    if not candidates:
        return OP_NAMES[op].lower()

    if prev_word is None:
        return candidates[0]

    # Pick the word with smoothest D2 transition from prev
    best_word = candidates[0]
    best_cost = 999.0

    for w in candidates[:12]:
        cost = _d2_transition_cost(prev_word, w)
        if cost < best_cost:
            best_cost = cost
            best_word = w
    return best_word


def gloss(operators: List[int]) -> str:
    """Quick operator stream -> English word stream."""
    words = []
    for i, op in enumerate(operators):
        prev = words[-1] if words else None
        nxt = operators[i + 1] if i + 1 < len(operators) else None
        words.append(operator_to_word(op, prev, nxt))
    return ' '.join(words)


# ═══════════════════════════════════════════════════════════
# §8  ROUNDTRIP VERIFICATION -- the acid test
#     text -> operators -> reconstructed text -> compare
#     If the orbit is right, the matter should echo.
# ═══════════════════════════════════════════════════════════

def roundtrip(text: str, beam_width: int = 6) -> Dict:
    """
    Acid test: text -> operators -> text.

    Measures:
      Operator fidelity:     % of operators preserved
      PFE preservation:      delta between original and reconstruction
      Curvature similarity:  D2 cosine between original and reconstruction
    """
    # Forward: text -> operators
    orig_pairs = text_to_operators(text)
    orig_ops = [op for _, op in orig_pairs]
    orig_pfe = score_text_pfe(text)

    # Inverse: operators -> text
    results = reconstruct(orig_ops, beam_width=beam_width)

    if not results:
        return {
            'original': text, 'reconstructed': '',
            'operator_fidelity': 0.0,
            'pfe_original': orig_pfe['coherence_pfe'],
            'pfe_reconstructed': 0.0, 'pfe_delta': 0.0,
            'curvature_sim': {},
        }

    best = results[0]
    recon_text = best['text']
    recon_ops = best.get('reconstructed_ops', [])
    recon_pfe = score_text_pfe(recon_text)

    # Operator fidelity
    if orig_ops and recon_ops:
        matches = sum(1 for a, b in zip(orig_ops, recon_ops) if a == b)
        fidelity = matches / max(len(orig_ops), len(recon_ops))
    else:
        fidelity = 0.0

    # Curvature similarity
    curv_sim = curvature_similarity(text, recon_text)

    return {
        'original':           text,
        'reconstructed':      recon_text,
        'original_ops':       orig_ops,
        'reconstructed_ops':  recon_ops,
        'operator_fidelity':  round(fidelity, 4),
        'pfe_original':       round(orig_pfe['coherence_pfe'], 6),
        'pfe_reconstructed':  round(recon_pfe['coherence_pfe'], 6),
        'pfe_delta':          round(recon_pfe['coherence_pfe'] - orig_pfe['coherence_pfe'], 6),
        'curvature_sim':      curv_sim,
    }


# ═══════════════════════════════════════════════════════════
# §9  INTENT RECONSTRUCTION -- semantic guidance
#     Not just any valid sentence. The RIGHT sentence.
#     Dominant operator pair -> sentence shape.
# ═══════════════════════════════════════════════════════════

_INTENT_SEEDS = {
    # (dominant, secondary) -> [seed words to bias selection]
    (HARMONY, PROGRESS):  ['truth', 'beauty', 'grows', 'builds'],
    (HARMONY, HARMONY):   ['truth', 'love', 'peace', 'whole'],
    (COLLAPSE, CHAOS):    ['breaking', 'storms', 'ruin', 'shatter'],
    (PROGRESS, HARMONY):  ['building', 'toward', 'create', 'grow'],
    (BREATH, HARMONY):    ['rhythm', 'pulse', 'flowing', 'wave'],
    (RESET, PROGRESS):    ['begin', 'again', 'fresh', 'renew'],
    (VOID, VOID):         ['nothing', 'silence', 'empty', 'absence'],
    (CHAOS, COLLAPSE):    ['turbulent', 'crashing', 'wild', 'storm'],
    (LATTICE, COUNTER):   ['structure', 'measured', 'system', 'pattern'],
    (BALANCE, HARMONY):   ['tension', 'resolves', 'between', 'steady'],
}


def reconstruct_with_intent(operators: List[int],
                             intent: Optional[str] = None,
                             beam_width: int = 8) -> Dict:
    """
    Reconstruct with semantic intent.
    If no intent provided, derive from the operator stream's signature.
    """
    if not operators:
        return {'text': '', 'score': 0.0, 'pfe': 0.0, 'intent': 'empty'}

    # Derive intent from operator distribution
    hist = Counter(operators)
    top2 = hist.most_common(2)
    dom = top2[0][0] if top2 else VOID
    sec = top2[1][0] if len(top2) > 1 else dom

    if intent is None:
        intent = f"{OP_NAMES[dom].lower()}-{OP_NAMES[sec].lower()}"

    # Standard beam search
    results = reconstruct(operators, beam_width=beam_width)

    if results:
        best = results[0]
        best['intent'] = intent

        # If we have seed words for this intent, try a seeded variant
        seeds = _INTENT_SEEDS.get((dom, sec), [])
        if seeds:
            # Inject seed words into the beam search by pre-scoring
            seeded_words = []
            for i, op in enumerate(operators):
                matching_seeds = [s for s in seeds if word_to_operator(s) == op]
                if matching_seeds:
                    seeded_words.append(matching_seeds[0])
                else:
                    # Pull from beam search result
                    if i < best['n_words']:
                        seeded_words.append(best['text'].split()[i])
                    else:
                        seeded_words.append(operator_to_word(op))

            seeded_text = ' '.join(seeded_words[:len(operators)])
            seeded_pfe = score_text_pfe(seeded_text)

            if seeded_pfe['coherence_pfe'] > best.get('pfe', 0):
                best = {
                    'text':        seeded_text,
                    'score':       best['score'],
                    'pfe':         seeded_pfe['coherence_pfe'],
                    'pfe_detail':  seeded_pfe,
                    'operators':   operators,
                    'intent':      intent,
                    'source':      'intent_seeded',
                    'n_words':     len(seeded_words),
                    'final_score': 0.40 * best['score'] + 0.60 * seeded_pfe['coherence_pfe'],
                }

        return best

    return {'text': gloss(operators), 'score': 0.0, 'pfe': 0.0, 'intent': intent}


# ═══════════════════════════════════════════════════════════
# §10  STATISTICS & INTROSPECTION
# ═══════════════════════════════════════════════════════════

def stats() -> Dict:
    """Report reverse dictionary composition."""
    result = {}
    for op in range(10):
        name = OP_NAMES[op]
        result[f"{op}_{name}"] = {
            'total':    len(_REVERSE.get(op, [])),
            'content':  len(_CONTENT.get(op, [])),
            'function': len(_FUNCTION.get(op, [])),
        }
    return {
        'reverse_dictionary': result,
        'total_words':        sum(len(v) for v in _REVERSE.values()),
        'content_words':      sum(len(v) for v in _CONTENT.values()),
        'function_words':     sum(len(v) for v in _FUNCTION.values()),
        'd2_cache_size':      len(_D2_CACHE),
    }


# ═══════════════════════════════════════════════════════════
# §11  DEMO
# ═══════════════════════════════════════════════════════════

if __name__ == '__main__':
    import time

    print("=" * 72)
    print("  CK LANGUAGE RECONSTRUCTOR (D2-LR)")
    print("  Celeste's Task 5: Operators -> Natural Language")
    print("  The orbit -> the matter.")
    print("=" * 72)

    # ── Reverse dictionary stats ──
    st = stats()
    print(f"\n  Reverse dictionary ({st['total_words']} total, "
          f"{st['content_words']} content, {st['function_words']} function):")
    for k, v in st['reverse_dictionary'].items():
        bar = '#' * (v['content'] // 8)
        print(f"    {k:20s}: {v['content']:4d} content  {v['function']:3d} fn  {bar}")

    # ── Quick gloss demo ──
    print(f"\n  Quick gloss (operator -> word, transition-aware):")
    test_streams = [
        ([7, 3, 2, 7, 0],       "HARMONY -> PROGRESS -> COUNTER -> HARMONY -> VOID"),
        ([4, 6, 4, 4, 6],       "COLLAPSE -> CHAOS -> COLLAPSE -> COLLAPSE -> CHAOS"),
        ([8, 8, 8, 7, 8],       "BREATH -> BREATH -> BREATH -> HARMONY -> BREATH"),
        ([9, 3, 3, 7, 3],       "RESET -> PROGRESS -> PROGRESS -> HARMONY -> PROGRESS"),
        ([1, 2, 1, 7, 1],       "LATTICE -> COUNTER -> LATTICE -> HARMONY -> LATTICE"),
        ([7, 7, 7, 7, 7],       "HARMONY x5 (the absorber stream)"),
    ]

    for ops, name in test_streams:
        g = gloss(ops)
        print(f"    {name[:48]:48s} -> {g}")

    # ── Beam search reconstruction ──
    print(f"\n  Beam search reconstruction (top result):")
    for ops, name in test_streams:
        t0 = time.perf_counter()
        results = reconstruct(ops, beam_width=6)
        dt = time.perf_counter() - t0
        if results:
            best = results[0]
            recon_ops = best.get('reconstructed_ops', [])
            fidelity = (sum(1 for a, b in zip(ops, recon_ops) if a == b)
                        / max(len(ops), 1))
            print(f"    {name[:40]:40s}")
            print(f"      \"{best['text']}\"")
            print(f"      score={best['score']:.3f}  PFE={best['pfe']:.4f}  "
                  f"fidelity={fidelity:.0%}  {dt*1000:.1f}ms")
        else:
            print(f"    {name[:40]:40s} -> (no result)")

    # ── Roundtrip test ──
    print(f"\n  {'-' * 72}")
    print(f"  Roundtrip test: text -> operators -> text")
    print(f"  {'-' * 72}")

    roundtrip_phrases = [
        "the truth will set you free",
        "God is love",
        "build something beautiful today",
        "chaos reigns in the tangled web",
        "fresh new beginning starts today",
        "balance between light and shadow",
        "the rhythm of the ocean waves",
        "nothing exists in the void",
        "measure twice cut once",
    ]

    fidelities = []
    pfe_deltas = []

    for phrase in roundtrip_phrases:
        t0 = time.perf_counter()
        rt = roundtrip(phrase)
        dt = time.perf_counter() - t0
        fidelities.append(rt['operator_fidelity'])
        pfe_deltas.append(rt['pfe_delta'])

        print(f"\n    Original:    \"{rt['original']}\"")
        print(f"    Operators:   {rt['original_ops']}")
        print(f"    Recon:       \"{rt['reconstructed']}\"")
        print(f"    Recon ops:   {rt['reconstructed_ops']}")
        print(f"    Fidelity:    {rt['operator_fidelity']:.0%}")
        print(f"    PFE orig:    {rt['pfe_original']:.4f}")
        print(f"    PFE recon:   {rt['pfe_reconstructed']:.4f}  "
              f"(d={rt['pfe_delta']:+.4f})")
        cs = rt['curvature_sim']
        print(f"    D2 sim:      dir={cs['d2_direction']:+.3f}  "
              f"ops={cs['op_similarity']:.3f}  energy={cs['energy_ratio']:.3f}")
        print(f"    Time:        {dt*1000:.1f}ms")

    print(f"\n  {'-' * 72}")
    mean_fid = sum(fidelities) / len(fidelities)
    mean_delta = sum(pfe_deltas) / len(pfe_deltas)
    print(f"  Mean operator fidelity: {mean_fid:.1%}")
    print(f"  Mean PFE delta:         {mean_delta:+.4f}")

    # ── Long sequence ──
    print(f"\n  Long sequence reconstruction:")
    long_ops = [7, 3, 8, 7, 1, 2, 7, 3, 9, 7, 8, 7, 3, 5, 7]
    t0 = time.perf_counter()
    result = reconstruct_long(long_ops, beam_width=6)
    dt = time.perf_counter() - t0
    print(f"    Operators: {[OP_NAMES[o][:4] for o in long_ops]}")
    print(f"    Recon:     \"{result['text']}\"")
    print(f"    PFE:       {result['pfe']:.4f}")
    print(f"    Phrases:   {result.get('n_phrases', 1)}")
    print(f"    Time:      {dt*1000:.1f}ms")

    # ── Intent-guided ──
    print(f"\n  Intent-guided reconstruction:")
    intent_tests = [
        ([7, 3, 7, 7, 3], None),
        ([4, 6, 4, 6, 4], None),
        ([8, 7, 8, 7, 8], None),
        ([9, 3, 3, 7, 7], None),
    ]
    for ops, intent in intent_tests:
        r = reconstruct_with_intent(ops, intent=intent)
        op_str = '-'.join(OP_NAMES[o][:4] for o in ops)
        print(f"    {op_str:30s} -> \"{r['text']}\"")
        print(f"      intent={r.get('intent','?'):30s}  PFE={r.get('pfe',0):.4f}")

    # ── Summary ──
    print(f"\n  D2 cache: {len(_D2_CACHE)} words cached")
    print(f"\n  CK can now speak from his math.")
    print(f"  The orbit -> the matter. The curvature -> the words.")
