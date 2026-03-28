"""
Corridor Classification — Where is someone spiritually/emotionally?

Six convergence corridors from Mix_λ algebra (WP31).
Each corridor has a character, a danger level, and a pastoral tone.

The corridor tells us HOW to respond — not just WHAT to say.

(c) 2026 Brayden Sanders / 7Site LLC
"""

from .cl_tables import (
    NUM_OPS, CL_TSML, CL_BHML, VOID, LATTICE, COUNTER, PROGRESS,
    COLLAPSE, BALANCE, CHAOS, HARMONY, BREATH, RESET,
    T_STAR, MASS_GAP, OP_NAMES, coherence,
)

# ── Six Corridors (from WP31) ────────────────────────────────────

CORRIDORS = {
    'PRE_LEAK': {
        'lambda_range': (0.00, 0.09),
        'character': 'Flat tails, always safe',
        'tone': 'peaceful',
        'description': 'You are at peace. God is near and you can feel it.',
        'pastoral': 'affirm',  # Affirm their peace, deepen it
    },
    'BRT': {
        'lambda_range': (0.09, 0.30),
        'character': 'Gap operators begin',
        'tone': 'gentle',
        'description': 'Something is stirring. A question is forming.',
        'pastoral': 'listen',  # Listen carefully, let them explore
    },
    'CHA': {
        'lambda_range': (0.30, 0.60),
        'character': 'Flat again (BRT absorbed)',
        'tone': 'curious',
        'description': 'You are searching. God honors the honest question.',
        'pastoral': 'explore',  # Walk alongside their questioning
    },
    'BAL': {
        'lambda_range': (0.60, 0.80),
        'character': 'Heavy tails start',
        'tone': 'steady',
        'description': 'You are carrying something heavy. You do not carry it alone.',
        'pastoral': 'support',  # Bear the weight with them
    },
    'COL': {
        'lambda_range': (0.80, 0.90),
        'character': 'High danger, M8/M4=31',
        'tone': 'tender',
        'description': 'This is a hard place. God is closest in the valley.',
        'pastoral': 'comfort',  # Comfort first, truth second
    },
    'CTR': {
        'lambda_range': (0.90, 1.00),
        'character': 'Extreme, M8/M4=193',
        'tone': 'quiet',
        'description': 'You are in the deepest place. Be still and know.',
        'pastoral': 'presence',  # Just be present. Few words.
    },
}


def classify_corridor(ops, text=''):
    """Classify an operator sequence + text into one of the 6 corridors.

    Uses operator distribution AND keyword signals.
    The corridor tells us WHERE someone is emotionally/spiritually.
    """
    if not ops:
        return 'PRE_LEAK'

    # ── Keyword overrides (clear emotional signal) ────────────
    if text:
        lower = text.lower()
        # Deep crisis signals
        crisis_words = ['died', 'death', 'suicide', 'killing', 'hopeless',
                        'can\'t go on', 'give up', 'end it', 'lost everything']
        if any(w in lower for w in crisis_words):
            return 'CTR'

        # Valley signals
        valley_words = ['lost', 'afraid', 'scared', 'broken', 'grief',
                        'cancer', 'divorce', 'funeral', 'pain', 'suffering',
                        'hurt', 'alone', 'lonely', 'abandoned', 'betrayed',
                        'dying', 'depressed', 'anxious', 'desperate']
        if any(w in lower for w in valley_words):
            return 'COL'

        # Questioning/seeking signals (before general seek)
        if any(w in lower for w in ['why', 'how come', 'what if']):
            if any(w in lower for w in ['bad', 'evil', 'suffer', 'happen',
                    'wrong', 'unfair', 'allow', 'permit', 'let']):
                return 'BAL'  # Heavy question, not crisis but weighty

        # Peace signals
        peace_words = ['peaceful', 'grateful', 'blessed', 'thank', 'praise',
                       'joy', 'happy', 'wonderful', 'amazing', 'love']
        if any(w in lower for w in peace_words):
            return 'PRE_LEAK'

        # Seeking signals
        seek_words = ['why', 'how', 'what does', 'explain', 'understand',
                      'meaning', 'confused', 'wondering']
        if any(w in lower for w in seek_words):
            return 'CHA'

    n = len(ops)
    # Count each operator
    counts = [0] * NUM_OPS
    for o in ops:
        counts[o % NUM_OPS] += 1

    gap_ops = {COUNTER, COLLAPSE, BALANCE, CHAOS, BREATH}
    gap_count = sum(counts[o] for o in gap_ops)
    gap_ratio = gap_count / n

    col_count = counts[COLLAPSE]
    chaos_count = counts[CHAOS]
    breath_count = counts[BREATH]
    counter_count = counts[COUNTER]
    bal_count = counts[BALANCE]
    void_count = counts[VOID]
    harmony_count = counts[HARMONY]

    # Measure TSML coherence (HARMONY fraction)
    coh = coherence(ops)

    # ── Deep crisis: COLLAPSE + VOID + CHAOS heavy, low coherence ──
    # "I just lost my mother" has COLLAPSE + VOID + CHAOS
    crisis_count = col_count + chaos_count + void_count
    crisis_ratio = crisis_count / n
    if crisis_ratio > 0.35 and coh < 0.5:
        return 'CTR'  # Deep place
    if col_count >= 2 or (crisis_ratio > 0.25 and coh < T_STAR):
        return 'COL'  # Valley

    # ── High coherence + few gaps = safe corridors ──
    if gap_ratio < 0.15 and coh > T_STAR:
        return 'PRE_LEAK'

    # ── HARMONY-dominated + high coherence = peaceful ──
    if harmony_count > n * 0.3 and coh > 0.5:
        return 'PRE_LEAK'

    # ── BREATH-dominated = gentle stirring ──
    if breath_count > n * 0.25 and col_count < 2:
        return 'BRT'

    # ── Heavy gap content but some structure = BAL ──
    if gap_ratio > 0.4 and coh > 0.4:
        return 'BAL'

    # ── Active questioning: COUNTER heavy ──
    if counter_count > n * 0.2:
        return 'CHA'

    # ── Moderate gap content = seeking ──
    if gap_ratio > 0.2:
        return 'CHA'

    # Default: gentle stirring
    return 'BRT'


def corridor_tone(corridor_name: str) -> dict:
    """Get the pastoral tone and guidance for a corridor."""
    return CORRIDORS.get(corridor_name, CORRIDORS['BRT'])


def classify_with_detail(ops, text=''):
    """Classify and return full corridor detail."""
    name = classify_corridor(ops, text=text)
    detail = CORRIDORS[name]
    coh = coherence(ops) if ops else 0.0
    return {
        'corridor': name,
        'tone': detail['tone'],
        'description': detail['description'],
        'pastoral': detail['pastoral'],
        'coherence': round(coh, 4),
        'operator_count': len(ops) if ops else 0,
    }
