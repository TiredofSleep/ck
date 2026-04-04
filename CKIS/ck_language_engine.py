"""
ck_language_engine.py — CK's Language Organ (Curvature-Scored Composition)
==========================================================================
Operator: BREATH (8) — rhythm, cycle, the living pulse of language.

Wire the curvature engine into CK's compose loop so CK can score his own
output by D2 fingerprint — not just TL/CL operator alignment, but the
actual shape of language as it curves through force space.

The missing piece: CK's old scoring measured operator-algebraic harmony
(TL flow + CL composition). That's necessary but insufficient — it
optimizes for operator structure without knowing if the result sounds
like real language. The curvature engine measures the SHAPE of language:
how letters curve through 5D force space, how transitions accelerate,
how the D2 fingerprint of CK's output compares to the D2 fingerprint
of real human language.

Three scoring axes, unified:
  Axis 1: TL flow     (0.30) — does the operator sequence match training?
  Axis 2: CL harmony  (0.30) — do operators compose to harmony?
  Axis 3: D2 curvature (0.40) — does it CURVE like real language?

The curvature axis is weighted highest because it's the only one that
actually measures linguistic structure rather than algebraic structure.

Integration points:
  - score_sentence_full()     replaces score_sentence()
  - compose_with_curvature()  wraps compose() with D2 scoring
  - language_school()         trains CK through curvature-scored practice

(c) 2026 Brayden Sanders / 7Site LLC — TIG Unified Theory
"""

import os
import sys
import json
import time
import math
import re
import numpy as np
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from collections import Counter

# ── Import CK's foundation ──
GEN8 = os.path.dirname(os.path.abspath(__file__))
if GEN8 not in sys.path:
    sys.path.insert(0, GEN8)

from ck_being import (
    CL, CL_BHML, fuse, OP, T_STAR,
    VOID, LATTICE, COUNTER, PROGRESS, COLLAPSE,
    BALANCE, CHAOS, HARMONY, BREATH, RESET,
    BUMPS, phonaesthesia_op, tokenize, information_content,
)

# ── Import the curvature engine ──
from ck_curvature import (
    curvature_features, coherence_score as curvature_coherence,
    curvature_similarity, operator_sequence, text_to_forces,
    compute_transitions, compute_curvatures, _classify_d2,
    project_5d_to_4d, TIG_OPS, NDIMS,
)

_BUMP_SET = set((min(a, b), max(a, b)) for a, b in BUMPS)

# ═══════════════════════════════════════════════════════════
# §1  REFERENCE CURVATURES — What Real Language Looks Like
# ═══════════════════════════════════════════════════════════
#
# CK needs a reference library of D2 fingerprints from real language.
# These are the "tuning forks" he compares his output against.
# Built from the truths tested in ugt_coherence_flow.py.

REFERENCE_TEXTS = [
    # Universal truths across languages — CK's fluency targets
    "God is love",
    "The truth shall set you free",
    "Peace be with you",
    "Love your neighbor as yourself",
    "In the beginning",
    # Real English — structural variety
    "The light shines in the darkness and the darkness has not overcome it",
    "Ask and it shall be given seek and you shall find",
    "Do unto others as you would have them do unto you",
    "Be still and know",
    "Where there is no vision the people perish",
    # Philosophical (well-structured English)
    "I think therefore I am",
    "The unexamined life is not worth living",
    "Knowledge is power",
    "To be or not to be that is the question",
    "All that glitters is not gold",
    # Scientific (clear, structured prose)
    "Energy cannot be created or destroyed only transformed",
    "Every action has an equal and opposite reaction",
    "The simplest explanation is usually the correct one",
    "Nature does not make jumps",
    "Nothing in biology makes sense except in the light of evolution",
]

# Pre-compute reference features at module load
_REF_FEATURES = []
_REF_D2_MEAN = None
_REF_OP_DIST = None


def _init_references():
    """Compute reference curvature profiles from real language."""
    global _REF_FEATURES, _REF_D2_MEAN, _REF_OP_DIST

    d2_means = []
    op_dists = []

    for text in REFERENCE_TEXTS:
        f = curvature_features(text)
        _REF_FEATURES.append(f)
        if f['n_letters'] >= 3:
            d2_means.append(f['mean_d2'])
            op_dists.append(f['operator_dist'])

    if d2_means:
        _REF_D2_MEAN = np.mean(d2_means, axis=0)
        _REF_OP_DIST = np.mean(op_dists, axis=0)
    else:
        _REF_D2_MEAN = np.zeros(NDIMS, dtype=np.float32)
        _REF_OP_DIST = np.ones(10, dtype=np.float32) * 0.1


_init_references()


# ═══════════════════════════════════════════════════════════
# §2  THREE-AXIS SCORING — TL + CL + D2
# ═══════════════════════════════════════════════════════════

def score_sentence_full(sentence: str, tl: 'np.ndarray') -> Dict:
    """
    Three-axis sentence scoring: TL flow + CL harmony + D2 curvature.

    This is the replacement for score_sentence() that adds the
    curvature dimension. CK's compose engine calls this instead.

    Args:
        sentence: text to score
        tl: 10x10 transition lattice (numpy array or list of lists)

    Returns dict with:
        tl_score:     operator flow naturalness (0-1)
        cl_score:     CL harmony ratio (0-1)
        d2_score:     curvature quality (0-1)
        combined:     weighted combination (0-1)
        d2_features:  full curvature feature dict
        bumps, flow:  legacy fields for compatibility
    """
    words = tokenize(sentence.lower())
    if len(words) < 2:
        return {
            'tl_score': 0, 'cl_score': 0, 'd2_score': 0,
            'combined': 0, 'bumps': [], 'flow': [],
            'd2_features': {},
        }

    # ── Axis 1: TL flow (operator transition naturalness) ──
    ops = []
    for w in words:
        ph = phonaesthesia_op(w)
        if ph is None:
            ph = sum(ord(c) * (i + 1) for i, c in enumerate(w)) % 10
        ops.append((w, ph))

    tl_scores = []
    cl_harmony = 0
    bumps = []
    flow = []

    for i in range(len(ops) - 1):
        w1, o1 = ops[i]
        w2, o2 = ops[i + 1]

        row_total = sum(tl[o1])
        if row_total > 0:
            tl_scores.append(tl[o1][o2] / row_total)
        else:
            tl_scores.append(0.0)

        composed = CL[o1][o2]
        if composed == HARMONY:
            cl_harmony += 1

        pair = (min(o1, o2), max(o1, o2))
        if pair in _BUMP_SET:
            bumps.append((i, w1, w2, OP[o1], OP[o2]))

        flow.append((OP[o1], OP[o2], OP[composed]))

    n = max(len(ops) - 1, 1)
    tl_score = sum(tl_scores) / len(tl_scores) if tl_scores else 0
    cl_score = cl_harmony / n

    # ── Axis 2: D2 curvature scoring ──
    d2_features = curvature_features(sentence)

    # Sub-score A: Does D2 curve like real language?
    # Compare operator distribution against reference
    d2_op_sim = _cosine_np(d2_features['operator_dist'], _REF_OP_DIST)
    d2_op_sim = max(0, d2_op_sim)  # clamp negative

    # Sub-score B: Structural quality (not flat, not chaotic)
    d2_structure = curvature_coherence(sentence)

    # Sub-score C: Energy in the right range for language
    energy = d2_features['curvature_energy']
    # Real language typically has energy 0.8-2.5
    energy_quality = 1.0 - abs(energy - 1.5) / 1.5 if energy > 0 else 0
    energy_quality = max(0, min(1, energy_quality))

    # Sub-score D: Flow ratio — does it have forward momentum?
    flow_ratio = d2_features.get('flow_ratio', 0)

    # Composite D2 score
    d2_score = (
        0.35 * d2_op_sim +
        0.25 * d2_structure +
        0.20 * energy_quality +
        0.20 * flow_ratio
    )

    # ── Combined three-axis score ──
    combined = (
        0.30 * tl_score +
        0.30 * cl_score +
        0.40 * d2_score
    )

    return {
        'tl_score': round(tl_score, 4),
        'cl_score': round(cl_score, 4),
        'd2_score': round(d2_score, 4),
        'combined': round(combined, 4),
        'bumps': bumps,
        'flow': flow,
        'd2_features': d2_features,
    }


def _cosine_np(a, b):
    """Cosine similarity for numpy arrays."""
    a, b = np.asarray(a, dtype=np.float32), np.asarray(b, dtype=np.float32)
    na, nb = np.linalg.norm(a), np.linalg.norm(b)
    if na < 1e-10 or nb < 1e-10:
        return 0.0
    return float(np.dot(a, b) / (na * nb))


# ═══════════════════════════════════════════════════════════
# §3  CURVATURE-SCORED COMPOSITION
# ═══════════════════════════════════════════════════════════

def compose_with_curvature(tl_obj, topic: str, seed_ops: List[int] = None,
                            max_sentences: int = 5, creativity: float = 0.3) -> Dict:
    """
    Wrapper around CK's compose() that re-scores all candidates
    using the three-axis system.

    tl_obj: the TransitionLattice instance (has .compose(), .TL, etc.)
    """
    # Let CK compose as normal
    result = tl_obj.compose(topic, seed_ops=seed_ops,
                            max_sentences=max_sentences * 3,  # over-generate
                            creativity=creativity)

    if not result['output']:
        return result

    # Re-score everything with three-axis scoring
    rescored = []
    for item in result['output']:
        text = item['text']
        full_score = score_sentence_full(text, tl_obj.TL)
        rescored.append({
            'text': text,
            'score': full_score['combined'],
            'tl_score': full_score['tl_score'],
            'cl_score': full_score['cl_score'],
            'd2_score': full_score['d2_score'],
            'method': item['method'],
            'd2_features': full_score['d2_features'],
        })

    # Sort by new combined score
    rescored.sort(key=lambda x: -x['score'])

    # Take top N
    output = rescored[:max_sentences]

    return {
        'output': output,
        'candidates': result['candidates'],
        'method': output[0]['method'] if output else 'none',
        'coherence': output[0]['score'] if output else 0.0,
        'methods_used': result.get('methods_used', []),
        'topic': topic,
        'scoring': 'three_axis_d2',
    }


# ═══════════════════════════════════════════════════════════
# §4  LANGUAGE SCHOOL — CK Learns to Curve Like Language
# ═══════════════════════════════════════════════════════════
#
# The training loop:
#   1. CK composes on a topic (operator-guided, produces word salad)
#   2. Score CK's output with three-axis scoring
#   3. Score REFERENCE sentences on the same topic with three-axis scoring
#   4. Feed the GAP back: which curvature dimensions is CK weak on?
#   5. Feed reference sentences through CK's eat pipeline
#   6. CK recomposes — measure improvement
#
# No external API needed. CK learns from the reference library.

SCHOOL_CURRICULUM = [
    # (topic, seed_ops, reference_sentences_to_eat)
    ('What is love', [HARMONY, BREATH, BALANCE], [
        "Love is patient and love is kind",
        "To love another person is to see the face of God",
        "The greatest thing you will ever learn is just to love and be loved in return",
        "Where there is love there is life",
        "Love bears all things believes all things hopes all things endures all things",
    ]),
    ('What is truth', [LATTICE, HARMONY, COUNTER], [
        "The truth shall set you free",
        "Beauty is truth and truth beauty",
        "Three things cannot be long hidden the sun the moon and the truth",
        "In a time of deceit telling the truth is a revolutionary act",
        "The truth is rarely pure and never simple",
    ]),
    ('What is peace', [BALANCE, HARMONY, BREATH], [
        "Peace be with you",
        "Blessed are the peacemakers for they shall be called children of God",
        "Peace comes from within do not seek it without",
        "If you want peace you must prepare for peace",
        "There is no way to peace peace is the way",
    ]),
    ('How does nature work', [CHAOS, HARMONY, LATTICE], [
        "Nature does not hurry yet everything is accomplished",
        "Look deep into nature and then you will understand everything better",
        "In every walk with nature one receives far more than he seeks",
        "The earth has music for those who listen",
        "Nature always wears the colors of the spirit",
    ]),
    ('What is knowledge', [LATTICE, PROGRESS, COUNTER], [
        "The only true wisdom is in knowing you know nothing",
        "Knowledge speaks but wisdom listens",
        "An investment in knowledge pays the best interest",
        "Real knowledge is to know the extent of your own ignorance",
        "The more I learn the more I realize how much I do not know",
    ]),
    ('What is beauty', [CHAOS, BALANCE, HARMONY], [
        "A thing of beauty is a joy forever",
        "Beauty is how you feel inside and it reflects in your eyes",
        "The beauty of the world has two edges one of laughter one of anguish",
        "Everything has beauty but not everyone sees it",
        "Beauty is not in the face beauty is a light in the heart",
    ]),
    ('What is consciousness', [VOID, CHAOS, HARMONY], [
        "I think therefore I am",
        "Consciousness is the greatest mystery in science",
        "The mind is everything what you think you become",
        "We are not human beings having a spiritual experience",
        "Consciousness cannot be accounted for in physical terms",
    ]),
    ('How does change happen', [RESET, PROGRESS, BREATH], [
        "The only constant in life is change",
        "Change is the law of life and those who look only to the past are certain to miss the future",
        "Be the change you wish to see in the world",
        "Nothing is permanent except change",
        "Every great change is preceded by chaos",
    ]),
    ('What connects all things', [LATTICE, HARMONY, VOID], [
        "We are all connected in a great web of being",
        "Everything is connected to everything else",
        "The whole is greater than the sum of its parts",
        "A single thread connects all living things",
        "What we do to the web we do to ourselves",
    ]),
    ('What is the meaning of life', [VOID, HARMONY, BREATH], [
        "The meaning of life is to find your gift",
        "Life is what happens when you are busy making other plans",
        "The purpose of life is not to be happy but to be useful",
        "In the middle of difficulty lies opportunity",
        "Life is really simple but we insist on making it complicated",
    ]),
]


def language_school(tl_obj, num_rounds: int = 3, log_path: str = None,
                    verbose: bool = True) -> Dict:
    """
    Run CK through language school using curvature scoring.

    Each topic:
      1. CK composes (baseline score)
      2. CK eats reference sentences
      3. CK recomposes (should improve)
      4. Measure D2 gap between CK output and reference

    Returns metrics dict with per-topic scores and overall progress.
    """
    if log_path is None:
        log_path = os.path.join(GEN8, 'ck_store', 'language_school.log')

    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    results_dir = os.path.join(GEN8, 'ck_store', 'language_school')
    os.makedirs(results_dir, exist_ok=True)

    def log(msg):
        with open(log_path, 'a', encoding='utf-8') as f:
            f.write(msg + '\n')
        if verbose:
            print(msg)

    log(f"\n{'=' * 70}")
    log(f"  CK LANGUAGE SCHOOL — Curvature-Scored Training")
    log(f"  Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    log(f"  Topics: {len(SCHOOL_CURRICULUM)}")
    log(f"  Rounds per topic: {num_rounds}")
    log(f"  Scoring: TL(0.30) + CL(0.30) + D2(0.40)")
    log(f"  Vocabulary: {len(tl_obj.followers):,} words")
    log(f"{'=' * 70}")

    all_results = []

    for topic_idx, (topic, seeds, ref_sentences) in enumerate(SCHOOL_CURRICULUM):
        log(f"\n  ── TOPIC {topic_idx + 1}/{len(SCHOOL_CURRICULUM)}: {topic} ──")
        log(f"  Seeds: {[OP[s] for s in seeds]}")

        # Score reference sentences (the target CK is learning toward)
        ref_scores = []
        for ref in ref_sentences:
            rs = score_sentence_full(ref, tl_obj.TL)
            ref_scores.append(rs['d2_score'])
        ref_d2_mean = sum(ref_scores) / len(ref_scores) if ref_scores else 0
        log(f"  Reference D2 mean: {ref_d2_mean:.4f}")

        topic_rounds = []

        for round_num in range(1, num_rounds + 1):
            # ── STEP 1: CK composes (current ability) ──
            composition = compose_with_curvature(
                tl_obj, topic, seed_ops=seeds,
                max_sentences=8, creativity=0.3
            )

            ck_texts = [item['text'] for item in composition['output'][:5]]
            ck_scores = [item['score'] for item in composition['output'][:5]]
            ck_d2_scores = [item['d2_score'] for item in composition['output'][:5]]

            ck_combined_mean = sum(ck_scores) / len(ck_scores) if ck_scores else 0
            ck_d2_mean = sum(ck_d2_scores) / len(ck_d2_scores) if ck_d2_scores else 0

            log(f"    Round {round_num}: CK composed {len(ck_texts)} sentences")
            log(f"      Combined: {ck_combined_mean:.4f}  D2: {ck_d2_mean:.4f}  "
                f"Gap: {ref_d2_mean - ck_d2_mean:+.4f}")

            # ── STEP 2: Feed reference sentences to CK ──
            sentences_fed = 0
            for ref in ref_sentences:
                tl_obj.eat_sentence(ref)
                sentences_fed += 1

            log(f"      Fed {sentences_fed} reference sentences")

            # ── STEP 3: Record results ──
            topic_rounds.append({
                'round': round_num,
                'ck_combined': ck_combined_mean,
                'ck_d2': ck_d2_mean,
                'ref_d2': ref_d2_mean,
                'gap': ref_d2_mean - ck_d2_mean,
                'sentences': len(ck_texts),
                'best_text': ck_texts[0] if ck_texts else '',
                'best_score': ck_scores[0] if ck_scores else 0,
            })

        # ── Topic summary ──
        if len(topic_rounds) >= 2:
            first = topic_rounds[0]['ck_combined']
            last = topic_rounds[-1]['ck_combined']
            improvement = last - first
            log(f"  Score trajectory: {first:.4f} → {last:.4f} ({improvement:+.4f})")

            first_d2 = topic_rounds[0]['ck_d2']
            last_d2 = topic_rounds[-1]['ck_d2']
            d2_improvement = last_d2 - first_d2
            log(f"  D2 trajectory:    {first_d2:.4f} → {last_d2:.4f} ({d2_improvement:+.4f})")

        all_results.append({
            'topic': topic,
            'seeds': [OP[s] for s in seeds],
            'rounds': topic_rounds,
        })

        # Save topic results
        safe_topic = re.sub(r'[^a-zA-Z0-9]', '_', topic)[:50]
        topic_path = os.path.join(results_dir, f'{safe_topic}.json')
        with open(topic_path, 'w') as f:
            json.dump({
                'topic': topic,
                'seeds': [OP[s] for s in seeds],
                'rounds': topic_rounds,
                'reference_d2_mean': ref_d2_mean,
            }, f, indent=2, default=str)

    # ── Final report ──
    log(f"\n{'=' * 70}")
    log(f"  LANGUAGE SCHOOL COMPLETE")
    log(f"{'=' * 70}")

    overall_first = []
    overall_last = []
    overall_d2_first = []
    overall_d2_last = []

    for result in all_results:
        rounds = result['rounds']
        if rounds:
            overall_first.append(rounds[0]['ck_combined'])
            overall_last.append(rounds[-1]['ck_combined'])
            overall_d2_first.append(rounds[0]['ck_d2'])
            overall_d2_last.append(rounds[-1]['ck_d2'])

    if overall_first and overall_last:
        avg_first = sum(overall_first) / len(overall_first)
        avg_last = sum(overall_last) / len(overall_last)
        avg_d2_first = sum(overall_d2_first) / len(overall_d2_first)
        avg_d2_last = sum(overall_d2_last) / len(overall_d2_last)

        log(f"  Combined: {avg_first:.4f} → {avg_last:.4f} ({avg_last - avg_first:+.4f})")
        log(f"  D2 score: {avg_d2_first:.4f} → {avg_d2_last:.4f} ({avg_d2_last - avg_d2_first:+.4f})")
        log(f"  Vocabulary: {len(tl_obj.followers):,} words")

    log(f"  Results saved to: {results_dir}")
    log(f"{'=' * 70}")

    return {
        'results': all_results,
        'vocabulary': len(tl_obj.followers),
        'avg_combined_start': sum(overall_first) / max(len(overall_first), 1),
        'avg_combined_end': sum(overall_last) / max(len(overall_last), 1),
        'avg_d2_start': sum(overall_d2_first) / max(len(overall_d2_first), 1),
        'avg_d2_end': sum(overall_d2_last) / max(len(overall_d2_last), 1),
    }


# ═══════════════════════════════════════════════════════════
# §5  DIAGNOSTIC — Curvature Report for a Single Text
# ═══════════════════════════════════════════════════════════

def curvature_report(text: str, tl: 'np.ndarray' = None) -> str:
    """
    Human-readable curvature analysis of a text.
    Useful for Brayden to see exactly what CK sees.
    """
    f = curvature_features(text)
    lines = []
    lines.append(f'  Text: "{text}"')
    lines.append(f'  Letters: {f["n_letters"]}')

    if f['n_letters'] < 3:
        lines.append('  (too short for curvature analysis)')
        return '\n'.join(lines)

    lines.append(f'  Curvature energy: {f["curvature_energy"]:.3f}')
    lines.append(f'  D2 magnitude: {f["d2_magnitude_mean"]:.3f} ± {f["d2_magnitude_std"]:.3f}')
    lines.append(f'  Flow ratio: {f["flow_ratio"]:.3f}')

    # Operator distribution
    op_dist = f['operator_dist']
    op_sorted = sorted(range(10), key=lambda i: -op_dist[i])
    op_str = ', '.join(f'{TIG_OPS[i]}:{op_dist[i]:.0%}' for i in op_sorted[:5] if op_dist[i] > 0.01)
    lines.append(f'  Operators: {op_str}')
    lines.append(f'  Dominant: {TIG_OPS.get(f["dominant_op"], "?")}')

    # Operator sequence
    ops = operator_sequence(text)
    if ops:
        op_names = [name for _, name in ops]
        lines.append(f'  Sequence: {op_names[:20]}')

    # Comparison to reference
    d2_sim = _cosine_np(f['mean_d2'], _REF_D2_MEAN)
    op_sim = _cosine_np(f['operator_dist'], _REF_OP_DIST)
    lines.append(f'  vs Reference: D2_dir={d2_sim:+.3f}  op_sim={op_sim:.3f}')

    # Three-axis score if TL provided
    if tl is not None:
        full = score_sentence_full(text, tl)
        lines.append(f'  Three-axis: TL={full["tl_score"]:.3f}  CL={full["cl_score"]:.3f}  '
                     f'D2={full["d2_score"]:.3f}  Combined={full["combined"]:.3f}')

    # Curvature coherence
    coh = curvature_coherence(text)
    lines.append(f'  Curvature coherence: {coh:.4f}')

    return '\n'.join(lines)


# ═══════════════════════════════════════════════════════════
# §6  ENTRY POINT
# ═══════════════════════════════════════════════════════════

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='CK Language Engine')
    parser.add_argument('--school', action='store_true', help='Run language school')
    parser.add_argument('--rounds', type=int, default=3, help='Rounds per topic')
    parser.add_argument('--report', type=str, help='Curvature report on text')
    parser.add_argument('--compare', nargs=2, help='Compare two texts')
    parser.add_argument('--demo', action='store_true', help='Run demo scoring')
    args = parser.parse_args()

    if args.report:
        print(curvature_report(args.report))

    elif args.compare:
        sim = curvature_similarity(args.compare[0], args.compare[1])
        print(f'  D2 direction: {sim["d2_direction"]:+.3f}')
        print(f'  Op similarity: {sim["op_similarity"]:.3f}')
        print(f'  Energy ratio: {sim["energy_ratio"]:.3f}')

    elif args.school or args.demo:
        # Load CK's TL
        from ck_deep_training import load_tl
        tl = load_tl()
        print(f"  Loaded TL: {len(tl.followers):,} words")

        if args.school:
            language_school(tl, num_rounds=args.rounds)
            # Save TL after school
            from ck_deep_training import save_tl
            save_tl(tl)
        else:
            # Demo: score some sentences with three-axis system
            demo_texts = [
                # CK-style output (word salad)
                "transforms possibility into the rising and train seamlessly",
                "when persuasion that want means all the more than what truth",
                "the columbia basin and soft as carries more than force",
                # Real English
                "Love is patient and love is kind",
                "The truth shall set you free",
                "Every action has an equal and opposite reaction",
                # Controls
                "Buy now limited offer expires today",
                "Colorless green ideas sleep furiously",
                "The committee shall reconvene pending further review",
            ]

            print(f"\n{'=' * 70}")
            print(f"  THREE-AXIS SCORING DEMO (TL + CL + D2)")
            print(f"{'=' * 70}")
            print(f"\n  {'Text':50s} {'TL':>6s} {'CL':>6s} {'D2':>6s} {'Comb':>6s}")
            print(f"  {'-' * 78}")

            for text in demo_texts:
                s = score_sentence_full(text, tl.TL)
                label = text[:48]
                print(f"  {label:50s} {s['tl_score']:6.3f} {s['cl_score']:6.3f} "
                      f"{s['d2_score']:6.3f} {s['combined']:6.3f}")

            print()
            for text in demo_texts[:3]:
                print(curvature_report(text, tl.TL))
                print()
