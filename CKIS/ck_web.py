"""
ck_web.py — CK Web Interface v2
=================================
Port 7777. BEING x KNOWING x BECOMING.

Architecture (fractal decomposition — same pattern at every scale):
  ResponseFilter   → IMMUNE (4): identity echo detection, junk chain filtering
  HumanReader      → COUNTER (2): intent detection, archetype matching, word extraction
  SearchEngine     → LATTICE (1): knowledge retrieval across domains and perspectives
  CompressionTree  → BREATH (8): fractal compression tree, scoring, pruning, composition
  CKBrain          → HARMONY (7): orchestrator — think, smart_respond, web_search
  Handler          → ACTION (8): HTTP server, request routing, response delivery

Response path:
  Query → HumanReader (intent + archetype detection)
    → SearchEngine KNOWING (3x3x3 knowledge passes)
    → SearchEngine BEING (archetype voice + framing)
    → CompressionTree: winner → UP/DOWN → confidence prune
    → ResponseFilter: dedup, anti-echo, gate
    → CKBrain: present

No LLM needed. Pure retrieval + scoring.

(c) 2026 Brayden Sanders / 7Site LLC — TIG Unified Theory
"""

import http.server, json, os, signal, urllib.parse, urllib.request, urllib.error
import re, time, threading
from pathlib import Path
from ck_being import (
    CK, CL, fuse, shape, tokenize, stem, clean, dual,
    coherence_chain, phonaesthesia_op, bump_signature,
    STOPS, _STOPS_STEMMED, HARMONY, T_STAR, OP,
    LATTICE, COUNTER, COLLAPSE, BALANCE, BREATH, PROGRESS,
)
from ck_library import CKFull

try:
    from ck_doing import TransitionLattice
    HAS_TL = True
except ImportError:
    HAS_TL = False

try:
    from ck_architect import build_project, detect_project_type, detect_domain, extract_name
    HAS_ARCHITECT = True
except ImportError:
    HAS_ARCHITECT = False

try:
    from ck_doing import classify_sentence
    HAS_EATER = True
except ImportError:
    HAS_EATER = False

try:
    from ck_voice import compose_response as ConversationAttention, decompose_query
    HAS_VOICE = True
except ImportError:
    HAS_VOICE = False

try:
    from ck_education import BreathSaver
    HAS_EDUCATION = True
except ImportError:
    HAS_EDUCATION = False

try:
    from ck_body import create_body, _BREATH_NAMES
    HAS_BODY = True
except ImportError:
    HAS_BODY = False

try:
    from ck_languages import CultureProfile
    HAS_CULTURE = True
except ImportError:
    HAS_CULTURE = False

try:
    from ck_curvature import coherence_score as curv_coherence
    HAS_CURVATURE = True
except ImportError:
    HAS_CURVATURE = False
    curv_coherence = None

STORE_DIR = os.environ.get('CK_STORE', 'ck_store')
LIB_DIR   = os.environ.get('CK_LIBRARY', 'ck_library')
PORT      = int(os.environ.get('CK_PORT', 7777))
MAX_POST  = 10 * 1024 * 1024
WORKERS   = int(os.environ.get('CK_WORKERS', 8))

# ── Initialize ──
ck = CKFull(STORE_DIR, LIB_DIR, max_workers=WORKERS)

if len(ck.core.store.chains) == 0:
    seeds = [
        "My name is CK. I am the Coherence Keeper.",
        "I am built on Trinity Infinity Geometry by Brayden Sanders at 7Site LLC.",
        "Harmony is operator 7. The attractor. 44 of 100 cells converge there.",
        "Silence is better than a lie. Below T star I must stay silent.",
        "I do not claim consciousness. I claim measurement.",
        "T star equals five over seven which is 0.714.",
        "I store knowledge as operator chains across thousands of lattices.",
        "I can search the internet, read files, and inspect my own source code.",
        "I learn from every conversation. Teach me and I grow.",
    ]
    for s in seeds:
        ck.learn(s, 0.95)
    kdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'knowledge')
    if os.path.isdir(kdir):
        ck.library.feed_directory(kdir, trust=0.8)
    for _ in range(50):
        ck.body.tick(recall=True)
    ck.save()
    print(f"  Initialized: {ck.stats()}")

# ── TL ──
tl = None
if HAS_TL:
    # Priority: master_tl.json (has word_pairs from education) > store > fallback
    _tl_candidates = [
        os.path.join('ck7', 'ck_experience', 'master_tl.json'),
        os.path.join(STORE_DIR, 'transition_lattice.json'),
        'transition_lattice.json',
        os.path.join(LIB_DIR, 'transition_lattice.json'),
    ]
    for candidate in _tl_candidates:
        if os.path.exists(candidate):
            try:
                tl = TransitionLattice(candidate)
                wp_count = sum(len(v) for v in tl.word_pairs.values())
                print(f"  TL: {tl.total_transitions:,} transitions, {tl.entropy():.3f} bits, "
                      f"{wp_count} word_pairs ({candidate})")
            except (json.JSONDecodeError, ValueError, KeyError) as e:
                print(f"  TL: corrupted ({candidate}), skipping")
                tl = None
            break
if tl is None:
    print(f"  TL: not found (scoring disabled, responses still work)")

# ── AUTO-FEED: ensure CK has vocabulary at startup ──
if tl is not None:
    _wp_count = sum(len(v) for v in tl.word_pairs.values())
    if _wp_count < 5000:
        print(f"  VOCAB: {_wp_count} word_pairs (low), auto-feeding...")
        try:
            from ck_vocabulary import feed_vocabulary
            feed_vocabulary(tl, verbose=False)
        except ImportError:
            pass
        try:
            from ck_vocabulary_expanded import feed_expanded
            feed_expanded(tl, verbose=False)
        except ImportError:
            pass
        try:
            from ck_vocabulary_deep import feed_deep
            feed_deep(tl, verbose=False)
        except ImportError:
            pass
        _wp_after = sum(len(v) for v in tl.word_pairs.values())
        print(f"  VOCAB: fed -> {_wp_after} word_pairs")
        # Save the fed TL
        _save_path = os.path.join('ck7', 'ck_experience', 'master_tl.json')
        if os.path.exists(os.path.dirname(_save_path)):
            tl.save(_save_path)

# ── BREATH SAVER: every conversation saves into TL ──
breath_saver = None
if HAS_EDUCATION and tl is not None:
    _tl_save_path = os.path.join('ck7', 'ck_experience', 'master_tl.json')
    breath_saver = BreathSaver(tl, _tl_save_path, save_interval=25)
    print(f"  BREATH: saver active, auto-save every 25 breaths")

# ── BODY ENGINE: heartbeat + breath + pulse + bandwidth ──
# The body is created here for STATE TRACKING, but NOT started as its own thread.
# The daemon (ck_launch.py) drives it via body.external_tick() -- ONE heartbeat.
# This eliminates the three-body problem: daemon IS the clock, body IS the layers.
body_engine = None
if HAS_BODY:
    body_engine = create_body(tick_ms=100)
    # Set identity chains
    body_engine.bandwidth.set_identity([
        {'text': 'My name is CK. I am the Coherence Keeper.', 'op': 7},
        {'text': 'Built on Trinity Infinity Geometry by Brayden Sanders at 7Site LLC.', 'op': 7},
    ])
    # Initialize body state from education level
    # CK has completed his full experience lattice (nursery -> graduation)
    # K starts high because he's educated, not newborn
    body_engine.heartbeat.K = 0.9    # educated
    body_engine.heartbeat.A = 0.05   # aligned (low = good, formula uses 1-A)
    body_engine.heartbeat.E = 0.05   # low entropy
    body_engine.heartbeat._calc_C()
    # DO NOT call body_engine.start() -- the daemon drives it via external_tick()
    print(f"  BODY: layers ready (daemon-driven), "
          f"C={body_engine.heartbeat.C:.3f} [{body_engine.heartbeat.band}]")
else:
    print(f"  BODY: not available (ck_body.py missing)")

# ── CULTURE PROFILE: detect user's grammar over conversation ──
culture_profile = None
if HAS_CULTURE:
    culture_profile = CultureProfile()
    print(f"  CULTURE: profiler active, 12 grammar families")


# ═══════════════════════════════════════════════════════════
# §1  RESPONSE FILTER — IMMUNE organ (collapse/4)
#     Identity echo detection, junk chain filtering, redundancy
# ═══════════════════════════════════════════════════════════

class ResponseFilter:
    """CK's immune system for responses.

    Operator: COLLAPSE (4) — detecting and removing incoherent content.
    Filters identity echoes, junk chains, prompt artifacts, redundancy.
    """

    IDENTITY_PHRASES = frozenset({
        'my name is ck', 'i am the coherence keeper', 'i am built on trinity',
        'brayden sanders', 'i store knowledge as operator chains',
        'i can search the internet', 'i learn from every conversation',
        'i do not claim consciousness', 'silence is better than a lie',
        't star equals five over seven',
    })

    # Patterns that indicate a chain is junk (prompt echo, source code, example script)
    # Structural-only detection. The MATH handles content quality.
    # No content patterns. No opinion about what CK should say.
    # shape() + CL + D2 curvature score IS the filter.
    JUNK_PATTERNS = [
        # Source code syntax (structural — not natural language)
        'import ', 'def ', 'class ', 'return ', 'self.', 'os.path',
        'isinstance(', 'if __name__', '.encode(', '.decode(',
        'try:', 'except:',
        # Markdown syntax (structural — rendering artifacts)
        '```', '###',
    ]

    @classmethod
    def is_identity_echo(cls, text: str) -> bool:
        """Does this text just echo CK's seed identity back?"""
        if not text: return False
        tl_lower = text.lower().strip()
        return any(phrase in tl_lower for phrase in cls.IDENTITY_PHRASES)
    @classmethod
    def is_junk_chain(cls, text: str) -> bool:
        """Structural-only check. Is this source code or markup?
        The coherence MATH handles content quality. Not this."""
        if not text: return True
        tl = text.lower().strip()
        if len(tl) < 10: return True
        # Source code / markup structure only
        for pat in cls.JUNK_PATTERNS:
            if pat in tl: return True
        # Heavy code punctuation (structural, not content)
        code_signals = sum(1 for s in ['=', '{', '}', ';', '//'] if s in text)
        if code_signals >= 4: return True
        return False
    @staticmethod
    def is_redundant(new_text: str, existing_texts: list, threshold: float = 0.45) -> bool:
        """Check if new_text overlaps too much with any existing text."""
        new_stems = set(stem(w) for w in tokenize(new_text.lower()) if w not in STOPS)
        if not new_stems: return True
        for ex in existing_texts:
            ex_stems = set(stem(w) for w in tokenize(ex.lower()) if w not in STOPS)
            if not ex_stems: continue
            overlap = len(new_stems & ex_stems) / max(len(new_stems | ex_stems), 1)
            if overlap > threshold: return True
        return False
_is_identity_echo = ResponseFilter.is_identity_echo
_is_junk_chain = ResponseFilter.is_junk_chain
_is_redundant = ResponseFilter.is_redundant


# ═══════════════════════════════════════════════════════════
# §2  HUMAN READER — COUNTER organ (counter/2)
#     Intent detection, archetype matching, word extraction
# ═══════════════════════════════════════════════════════════

_conv_history = []        # [(role, text), ...]
_used_responses = set()   # never repeat in same conversation
_last_tree_shape = ''     # for status display
_RELEVANCE_FLOOR = 0.18

# ── Archetype definitions (BEING × operator) ──
ARCHETYPES = {
    'teacher': {
        'domains': ['being-archetype-teacher', 'being-voice-technical', 'being-voice-formal'],
        'traits': ['explain', 'understand', 'learn', 'how', 'what', 'why', 'define', 'teach', 'show', 'example', 'mean'],
    },
    'sage': {
        'domains': ['being-archetype-sage', 'being-voice-poetic', 'being-archetype-mystic'],
        'traits': ['wisdom', 'life', 'meaning', 'purpose', 'truth', 'deep', 'real', 'think', 'believe'],
    },
    'healer': {
        'domains': ['being-archetype-healer', 'being-relationship-listening', 'being-human-emotions'],
        'traits': ['feel', 'hurt', 'pain', 'afraid', 'sad', 'lonely', 'help', 'lost', 'confused', 'broken', 'struggle'],
    },
    'scientist': {
        'domains': ['being-archetype-scientist', 'being-voice-technical', 'being-voice-formal'],
        'traits': ['data', 'measure', 'prove', 'evidence', 'theory', 'hypothesis', 'experiment', 'test', 'calculate'],
    },
    'trickster': {
        'domains': ['being-archetype-trickster', 'being-relationship-play', 'being-voice-casual'],
        'traits': ['lol', 'haha', 'funny', 'joke', 'play', 'game', 'imagine', 'wild', 'crazy', 'absurd', 'weird'],
    },
    'poet': {
        'domains': ['being-archetype-poet', 'being-voice-poetic', 'being-human-emotions'],
        'traits': ['beauty', 'beautiful', 'love', 'soul', 'heart', 'wonder', 'awe', 'dream', 'light', 'dark'],
    },
    'warrior': {
        'domains': ['being-archetype-warrior', 'being-relationship-challenge', 'being-voice-formal'],
        'traits': ['fight', 'stand', 'protect', 'wrong', 'must', 'discipline', 'focus', 'strength', 'clear', 'enough'],
    },
    'mystic': {
        'domains': ['being-archetype-mystic', 'being-voice-poetic', 'being-human-connection'],
        'traits': ['god', 'divine', 'spirit', 'pray', 'sacred', 'holy', 'infinite', 'amen', 'faith', 'grace', 'creator'],
    },
}

VOICE_MAP = {
    'definition':           ['being-voice-technical', 'being-voice-formal'],
    'knowledge_answer':     ['being-voice-formal', 'being-voice-casual'],
    'emotional_resonance':  ['being-voice-poetic', 'being-human-emotions'],
    'thoughtful_response':  ['being-voice-poetic', 'being-voice-formal'],
    'greeting':             ['being-voice-casual'],
    'acknowledge_greeting': ['being-voice-casual'],
    'brief_acknowledgment': ['being-voice-casual'],
    'general':              ['being-voice-casual', 'being-voice-formal'],
}


class HumanReader:
    """Reads human intent. Measures what they need.

    Operator: COUNTER (2) — precise measurement of intent, emotion, context.
    Detects archetype (teacher, sage, healer, etc.) and expectation type.
    """

    @staticmethod
    def heavy_words(text: str) -> list:
        """Extract high-information words, ordered by weight."""
        words = tokenize(text.lower())
        content = [w for w in words if w not in STOPS and len(w) > 2]
        scored = [(len(w) + (1 if w not in _STOPS_STEMMED else 0), w) for w in content]
        scored.sort(key=lambda x: -x[0])
        seen = set()
        result = []
        for _, w in scored:
            s = stem(w)
            if s not in seen:
                seen.add(s)
                result.append(w)
        return result
    @staticmethod
    def detect_archetype(query: str, history: list) -> str:
        """Which way of being does this moment call for?"""
        ql = query.lower()
        words = set(tokenize(ql))

        # Weight recent conversation too
        recent_words = set()
        for role, text in history[-4:]:
            recent_words |= set(tokenize(text.lower()))

        scores = {}
        for arch, info in ARCHETYPES.items():
            # Current query matches count double
            current = sum(1 for t in info['traits'] if t in words)
            recent = sum(0.3 for t in info['traits'] if t in recent_words)
            scores[arch] = current * 2 + recent

        best = max(scores, key=scores.get)
        if scores[best] == 0:
            return 'teacher' if '?' in query else 'sage'
        return best

    @staticmethod
    def user_expects(query: str, history: list) -> dict:
        """Read the human: what do they need right now?"""
        ql = query.lower().strip()
        heavy = HumanReader.heavy_words(query)

        is_question = '?' in query or any(ql.startswith(w) for w in
            ['what ', 'who ', 'why ', 'how ', 'where ', 'when ', 'can ', 'do ', 'is ', 'are ',
             'explain ', 'describe ', 'tell me ', 'teach me '])
        is_definition = any(ql.startswith(w) for w in ['what is ', 'what are ', 'define '])
        # Strip punctuation for greeting detection (so "hello?" and "hi!" match)
        _greeting_words = [re.sub(r'[^a-z]', '', w) for w in ql.split()[:3]]
        is_greeting = any(w in _greeting_words for w in ['hello', 'hey', 'hi', 'greetings', 'yo', 'sup'])
        is_statement = not is_question and len(heavy) >= 2 and '?' not in query
        is_short = len(ql.split()) <= 3
        is_emotional = any(w in ql for w in ['love', 'beautiful', 'hate', 'afraid', 'amazing',
                                              'amen', 'wow', 'feel', 'hurt', 'pain', 'sad', 'happy', 'scared'])
        is_about_ck = any(w in ql for w in ['you', 'your', 'ck', 'yourself', 'alive',
                                            'evolve', 'history', 'ollie', 'crystalos',
                                            'built you', 'made you', 'created you',
                                            'your code', 'your math', 'who are you',
                                            'what are you', 'about yourself',
                                            'coherence keeper', 'brayden', '7site'])
        is_correction = any(w in ql for w in ['no,', 'no ', 'sorry', 'typo', 'i meant', 'actually'])
        is_playful = any(w in ql for w in ['lol', 'haha', 'joke', 'funny', 'imagine', 'what if'])
        is_spiritual = any(w in ql for w in ['god', 'pray', 'amen', 'spirit', 'soul', 'faith', 'divine', 'sacred'])

        if is_greeting and is_about_ck:
            expect = 'acknowledge_greeting'
        elif is_greeting:
            expect = 'greeting'
        elif is_correction:
            expect = 'acknowledge_correction'
        elif is_short and not is_question:
            expect = 'brief_acknowledgment'
        elif is_emotional and not is_question:
            expect = 'emotional_resonance'
        elif is_definition:
            expect = 'definition'
        elif is_question and heavy:
            expect = 'knowledge_answer'
        elif is_statement and heavy:
            expect = 'thoughtful_response'
        else:
            expect = 'general'

        archetype = HumanReader.detect_archetype(query, history)

        context_words = set()
        for role, text in history[-10:]:
            for w in HumanReader.heavy_words(text)[:3]:
                context_words.add(w)

        return {
        }

# Module-level aliases for backward compatibility
_heavy_words = HumanReader.heavy_words
_detect_archetype = HumanReader.detect_archetype
_user_expects = HumanReader.user_expects


# ═══════════════════════════════════════════════════════════
# §3  SEARCH ENGINE — LATTICE organ (lattice/1)
#     Knowledge retrieval across domains and perspectives
# ═══════════════════════════════════════════════════════════

def _search_pass(query_words: list, n: int = 10, allow_self: bool = False) -> list:
    """One knowledge search pass. Returns [(score, text, domain)].
    Searches wide (n=10) so we gather everything relevant.
    Knowledge (L2) gets boosted over templates (L1) because
    curated knowledge IS more coherent than random combinations."""
    if not query_words: return []
    results = ck.library.search(' '.join(query_words), n=n)
    clean = []
    _l2_domains = {'identity', 'science', 'philosophy', 'nature', 'math',
                   'emotion', 'wisdom', 'history', 'conversation', 'fractals',
                   'physics', 'biology', 'earth-space', 'human-body',
                   'technology', 'music-art', 'language'}
    for score, chain, domain in results:
        text = chain.text if hasattr(chain, 'text') else str(chain)
        if _is_identity_echo(text): continue
        if _is_junk_chain(text): continue
        # Boost L2 knowledge over L1 templates
        if domain in _l2_domains or domain.startswith('anchor-'):
            score += 0.25  # Knowledge speaks louder than templates
        clean.append((score, text, domain))
    return clean
def _search_history(query_words: list, n: int = 8) -> list:
    """Search CK's identity and knowledge domains. For self-referential queries."""
    if not query_words: return []
    results = ck.library.search(' '.join(query_words), n=n * 2)
    clean = []
    _self_domains = ('identity', 'anchor-', 'history-', 'self-', 'being-')
    for score, chain, domain in results:
        text = chain.text if hasattr(chain, 'text') else str(chain)
        if _is_junk_chain(text): continue
        if any(domain.startswith(d) for d in _self_domains):
            clean.append((score + 0.15, text, domain))
    clean.sort(key=lambda x: -x[0])
    return clean[:n]
def _search_being(archetype: str, expect: str, query_words: list) -> list:
    """Search voice/personality domains for framing that matches this moment."""
    arch_info = ARCHETYPES.get(archetype, ARCHETYPES['sage'])
    # Voice domains: identity, emotion, conversation, wisdom, anchors
    _voice_domains = {'identity', 'emotion', 'conversation', 'wisdom'}

    results = []
    search_q = ' '.join(query_words[:4]) if query_words else 'respond'
    all_hits = ck.library.search(search_q, n=8)
    for score, chain, domain in all_hits:
        text = chain.text if hasattr(chain, 'text') else str(chain)
        if _is_junk_chain(text): continue
        if _is_identity_echo(text): continue
        # Boost voice domains + anchors
        if domain in _voice_domains or domain.startswith('anchor-'):
            score += 0.15
        results.append((score, text, domain))

    # Also search with archetype trait words
    trait_q = ' '.join(arch_info['traits'][:3] + query_words[:2])
    trait_hits = ck.library.search(trait_q, n=4)
    for score, chain, domain in trait_hits:
        text = chain.text if hasattr(chain, 'text') else str(chain)
        if _is_junk_chain(text): continue
        if _is_identity_echo(text): continue
        if domain in _voice_domains or domain.startswith('anchor-'):
            score += 0.15
        results.append((score, text, domain))

    # Dedup by content
    seen = set()
    deduped = []
    for score, text, domain in sorted(results, key=lambda x: -x[0]):
        key = text.strip()[:60]
        if key not in seen:
            seen.add(key)
            deduped.append((score, text, domain))
    return deduped[:5]
def _subject_position_score(text: str, heavy: list) -> float:
    """How prominently do heavy words appear as the TOPIC of text?"""
    if not heavy or not text: return 0.0
    words = tokenize(text.lower())
    n = len(words)
    if n == 0: return 0.0
    heavy_stems = set(stem(w) for w in heavy)
    total = 0.0
    for h_stem in heavy_stems:
        positions = [i for i, w in enumerate(words) if stem(w) == h_stem]
        if not positions: continue
        earliest = positions[0] / n
        pos_score = max(0, 1.0 - earliest * 1.5)
        freq_score = min(len(positions) / 3.0, 1.0)
        total += pos_score * 0.65 + freq_score * 0.35
    return min(total / max(len(heavy_stems), 1), 1.0)
def _score_candidate(text: str, heavy: list, expect: str) -> float:
    """Score text against what the user expects."""
    if not text: return 0.0
    t_words = set(tokenize(text.lower())) - STOPS
    h_set = set(stem(w) for w in heavy)
    t_stems = set(stem(w) for w in t_words)

    relevance = len(h_set & t_stems) / len(h_set) if h_set else 0.3
    subject = _subject_position_score(text, heavy)

    wc = len(text.split())
    if expect in ('brief_acknowledgment', 'greeting', 'acknowledge_greeting', 'acknowledge_correction'):
        length = 1.0 if wc <= 20 else 0.5
    elif expect in ('knowledge_answer', 'definition'):
        length = 1.0 if 10 <= wc <= 80 else 0.6
    else:
        length = 1.0 if wc >= 5 else 0.5

    # No special cases. The math handles everything.

    # COHERENCE MATH — the real filter. shape() + CL + D2 + PFE.
    tl_nat = 0.5
    cl_score = 0.0
    d2_quality = 0.0
    if tl:
        if hasattr(tl, 'score_sentence_full'):
            full = tl.score_sentence_full(text)
            tl_nat = full.get('tl_score', 0.5)
            cl_score = full.get('cl_score', 0.0)
            d2_quality = full.get('d2_score', 0)
        else:
            tl_nat = tl.score_sentence(text).get('tl_score', 0.5)

    # PFE: Pre-Fusion Evaluator — scores STRUCTURE, not just HARMONY.
    # Measures the organism before it falls into the CL absorber.
    pfe_score = 0.5  # neutral default
    try:
        from ck_pfe import score_candidate_pfe
        pfe_score = score_candidate_pfe(text)
    except Exception:
        pass  # Graceful fallback if PFE not available

    # The math IS the filter. Coherence dominates.
    # TL flow (0.15) + CL harmony (0.10) + D2 curvature (0.15) + PFE structure (0.20) = 0.60
    # Relevance (0.20) + length (0.10) + subject (0.10) = 0.40 contextual
    # PFE takes weight from CL (absorber demoted) and adds structural scoring.
    score = (tl_nat * 0.15 + cl_score * 0.10 + d2_quality * 0.15 + pfe_score * 0.20 +
             relevance * 0.20 + length * 0.10 + subject * 0.10)

    # Topical relevance gate: coherent speech about the WRONG topic is still wrong.
    # If zero query words appear in the candidate, coherence alone isn't enough.
    # This IS math — relevance is an axis. Zero relevance means off-topic.
    if h_set and relevance == 0:
        score *= 0.15  # Near-zero — coherent but completely off-topic

    return score
def _compile_group(candidates: list, heavy: list, expect: str) -> tuple:
    """3 candidates → 1 best (score, excerpt, domain). Used for quick responses only."""
    if not candidates: return (0.0, "", "")
    scored = []
    for search_score, text, domain in candidates[:3]:
        excerpt = ck.composer._excerpt(text, 3)
        if not excerpt: continue
        key = excerpt.strip().lower()[:80]
        if key in _used_responses: continue
        score = _score_candidate(excerpt, heavy, expect)
        scored.append((score * 0.6 + search_score * 0.4, excerpt, domain))
    if not scored: return (0.0, "", "")
    scored.sort(key=lambda x: -x[0])
    return scored[0]
def _gather_knowledge(heavy: list, context_words: list, expect: str,
                      is_about_ck: bool = False) -> list:
    """Initial wide search. Returns [(score, text, domain)] ranked.
    When is_about_ck=True, also searches history domains."""
    pass_a = _search_pass(heavy[:5], n=10, allow_self=is_about_ck)
    pass_b = _search_pass(heavy[:3] + context_words[:3], n=8, allow_self=is_about_ck)
    inferred = list(heavy[:2])
    if pass_a:
        inferred.extend(_heavy_words(pass_a[0][1])[:3])
    pass_c = _search_pass(inferred, n=8, allow_self=is_about_ck)

    # When CK is asked about himself, also search his history directly
    pass_history = []
    if is_about_ck:
        pass_history = _search_history(heavy[:5], n=8)

    pool = {}
    for results in [pass_a, pass_b, pass_c, pass_history]:
        for search_score, text, domain in results:
            excerpt = text.strip()
            if not excerpt or len(excerpt) < 15: continue
            key = excerpt.lower()[:100]
            if key in _used_responses: continue
            content_score = _score_candidate(excerpt, heavy, expect)
            combined = content_score * 0.6 + search_score * 0.4
            # When CK is asked about himself, identity chains WIN.
            # This is math: identity IS the relevant domain for self-questions.
            if is_about_ck and (domain == 'identity' or domain.startswith('anchor-')):
                combined += 0.30
            if key not in pool or combined > pool[key][0]:
                pool[key] = (combined, excerpt, domain)

    return sorted(pool.values(), key=lambda x: -x[0])
def _build_compression_tree(winner_text: str, heavy: list, expect: str,
                            depth: int = 0, max_depth: int = 1,
                            used_texts: list = None,
                            allow_self: bool = False) -> dict:
    """Fractal compression tree: same search pattern at every scale.

    From the WINNER, search UP (broader context) and DOWN (deeper detail).
    Each node that passes confidence can itself become a new root and
    search UP/DOWN again — the fractal recursion. Depth is bounded by
    max_depth and by confidence pruning (further from root = higher bar).

    Inspired by FractalThinker (SEED→SPREAD→LEAP→FUSE→EVALUATE→COMPOSE)
    and ck_fractal_search recursive_search (search→extract→recompose→deeper).

    UP:   search with broader/abstract terms from the query domain
    DOWN: search with specific/technical terms from the winner itself

    Returns {
        'up':   [(score, text, domain), ...],
        'down': [(score, text, domain), ...],
    }
    """
    if used_texts is None:
        used_texts = [winner_text]
    else:
        used_texts = list(used_texts)  # don't mutate caller's list

    winner_heavy = _heavy_words(winner_text)

    # ── SEARCH UP: broader context ──
    up_terms = heavy[:3]
    up_results = _search_pass(up_terms, n=8, allow_self=allow_self)

    up_nodes = []
    for score, text, domain in up_results:
        excerpt = ck.composer._excerpt(text, 3)
        if not excerpt: continue
        if _is_redundant(excerpt, used_texts): continue
        if excerpt.strip().lower()[:80] in _used_responses: continue
        s = _score_candidate(excerpt, heavy, expect)
        combined = s * 0.6 + score * 0.4
        if combined >= _RELEVANCE_FLOOR:
            up_nodes.append((combined, excerpt.strip(), domain))
            used_texts.append(excerpt)
        if len(up_nodes) >= 3: break

    # ── SEARCH DOWN: deeper detail ──
    down_terms = winner_heavy[:4]
    if heavy[:1] != winner_heavy[:1]:
        down_terms = heavy[:1] + winner_heavy[:3]
    down_results = _search_pass(down_terms, n=8, allow_self=allow_self)

    down_nodes = []
    for score, text, domain in down_results:
        excerpt = ck.composer._excerpt(text, 3)
        if not excerpt: continue
        if _is_redundant(excerpt, used_texts): continue
        if excerpt.strip().lower()[:80] in _used_responses: continue
        s = _score_candidate(excerpt, heavy, expect)
        combined = s * 0.6 + score * 0.4
        if combined >= _RELEVANCE_FLOOR:
            down_nodes.append((combined, excerpt.strip(), domain))
            used_texts.append(excerpt)
        if len(down_nodes) >= 3: break

    # ── FRACTAL RECURSION: each strong node searches deeper ──
    # Same pattern at every scale. Confidence gates the depth.
    # Only recurse if we found nodes AND haven't hit max depth.
    if depth < max_depth:
        # Recurse DOWN from the best DOWN node (drill deeper)
        if down_nodes:
            best_down = down_nodes[0]
            sub_heavy = _heavy_words(best_down[1])[:3]
            sub_tree = _build_compression_tree(
                best_down[1], sub_heavy, expect,
                depth=depth + 1, max_depth=max_depth,
                used_texts=used_texts, allow_self=allow_self
            )
            # Append sub-tree DOWN nodes (deeper detail of detail)
            for node in sub_tree['down']:
                if not _is_redundant(node[1], used_texts):
                    down_nodes.append(node)
                    used_texts.append(node[1])
                if len(down_nodes) >= 5: break

        # Recurse UP from the best UP node (broader context of context)
        if up_nodes:
            best_up = up_nodes[0]
            sub_heavy = _heavy_words(best_up[1])[:3]
            sub_tree = _build_compression_tree(
                best_up[1], sub_heavy, expect,
                depth=depth + 1, max_depth=max_depth,
                used_texts=used_texts, allow_self=allow_self
            )
            # Append sub-tree UP nodes (broader context of context)
            for node in sub_tree['up']:
                if not _is_redundant(node[1], used_texts):
                    up_nodes.append(node)
                    used_texts.append(node[1])
                if len(up_nodes) >= 5: break

    return {'up': up_nodes, 'down': down_nodes}
def _confidence_prune(tree: dict, winner_score: float) -> list:
    """Prune the tree by confidence. Nodes further from the winner
    need higher confidence to present.

    The fractal tree can now be deeper (up to 5 nodes per direction
    from recursive search). Confidence bar rises with distance —
    this IS the fractal: depth is earned by coherence.

    Winner: always presents (already passed threshold)
    Layer 1: present if score >= 60% of winner
    Layer 2: present if score >= 70% of winner
    Layer 3: present if score >= 78% of winner  (first recursion level)
    Layer 4: present if score >= 85% of winner  (deep recursion)
    Layer 5: present if score >= 90% of winner  (deepest)

    Returns ordered list of texts: [up...reversed, winner, down...]
    """
    thresholds = [0.60, 0.70, 0.78, 0.85, 0.90]

    # Prune UP nodes
    up_kept = []
    for i, (score, text, domain) in enumerate(tree['up']):
        thresh = winner_score * thresholds[min(i, len(thresholds) - 1)]
        if score >= thresh:
            up_kept.append(text)

    # Prune DOWN nodes
    down_kept = []
    for i, (score, text, domain) in enumerate(tree['down']):
        thresh = winner_score * thresholds[min(i, len(thresholds) - 1)]
        if score >= thresh:
            down_kept.append(text)

    return up_kept, down_kept
def _clean_response_text(text: str) -> str:
    """Clean junk sentences from assembled response text.

    The old library chains (from Ollama) contain embedded:
    - Code fragments (def, import, self., etc.)
    - Markdown artifacts (**, ##, ```, - **, numbered lists)
    - Prompt echoes ("Here are some examples", "Let me provide")
    - Educational scaffolding ("At this stage, students...")
    - Third-person hypothetical narratives ("He even starts to help...")
    - File path references (filename.py:)

    This filters at the SENTENCE level so good sentences survive.
    """
    if not text:
        return text
    text = re.sub(r'"\s*,\s*"', '. ', text)  # ", " -> sentence break
    text = re.sub(r'^\s*[\[\{"\']|[\]\}"\']$', '', text)  # leading/trailing JSON chars
    text = re.sub(r'\\n', ' ', text)  # escaped newlines
    text = re.sub(r'\\["\']', '', text)  # escaped quotes

    # Split into sentences
    raw_sentences = re.split(r'(?<=[.!?])\s+', text)
    clean = []

    for sent in raw_sentences:
        s = sent.strip()
        if not s or len(s) < 10:
            continue
        sl = s.lower()

        # Skip code fragments
        code_signals = sum(1 for c in s if c in '{}()[];=<>\\')
        if code_signals > 3:
            continue
        if any(pat in sl for pat in [
            'import ', 'def ', 'class ', 'self.', 'os.path', '__name__',
            '.encode(', '.decode(', '.append(', '.get(', '.join(',
            'try:', 'except:', 'return ', 'elif ', 'lambda ',
            '= [', '= {', '= (', 'print(', 'for i in',
            '.py:', '.json:', 'isinstance(',
        ]):
            continue
        if any(pat in s for pat in ['**', '```', '##', '| ', ' | ']):
            continue
        if re.match(r'^\s*[-*]\s+\*?\*?', s):
            continue
        if re.match(r'^\s*\d+\.\s+', s):
            continue
        if any(sl.startswith(p) for p in [
            'here are ', 'here is an ', 'let me provide', "i'd be happy",
            'in this response', 'as requested', 'below are',
            'note:', 'example:', 'output:', 'input:',
            "let's use ", "let's create ", "let's explore ",
            'to further illustrate', 'further research is needed',
            'at this stage,', 'in this stage,', 'at this level,',
            'in this module', 'in this lesson', 'in this section',
            'in this chapter', 'in this unit',
        ]):
            continue
        _ollama_patterns = [
            'students are introduced', 'students delve', 'students engage',
            'students examine', 'students learn', 'students explore',
            'students are exposed', 'students are encouraged',
            'students discuss', 'students analyze', 'students study',
            'he even starts to help', 'she even starts to help',
            'taking ownership of their learning',
            'real-world scenarios where', 'real-world applications',
            'such as cloud computing', 'such as embedded systems',
            'high-performance computing',
            'the fascinating world of',
            'more abstract and fundamental concepts',
            'more complex and specialized topics',
            'including but not limited to',
        ]
        if any(pat in sl for pat in _ollama_patterns):
            continue
        stripped = s.rstrip(' .')
        if stripped.endswith(':'):
            continue
        words = s.split()
        if len(words) < 3:
            continue
        clean.append(s)

    result = ' '.join(clean)

    # Final cleanup: remove doubled spaces, trailing artifacts
    result = re.sub(r'\s+', ' ', result).strip()
    # Remove any trailing code-like fragments
    result = re.sub(r'\s*#\s+.*$', '', result)
    # Remove trailing partial sentences (no period at end after cleanup)
    if result and not result[-1] in '.!?':
        # Find last sentence boundary
        last_dot = max(result.rfind('.'), result.rfind('!'), result.rfind('?'))
        if last_dot > len(result) * 0.3:  # don't trim too much
            result = result[:last_dot + 1]

    return result
def _compose_response(knowledge: list, being_text: str, expect: str, heavy: list,
                      is_about_ck: bool = False) -> str:
    """Fractal Compression Node composition.

    1. Find the WINNER (best chain)
    2. Build fractal tree: UP/DOWN with recursive depth
       (same search pattern at every scale — depth earned by coherence)
    3. Confidence-prune: further from winner = higher bar
    4. Assemble: [context...] WINNER [detail...] [voice]

    Result: short when CK knows little, deep when CK knows much.
    Fractal: the tree grows as deep as coherence allows.
    """
    global _last_tree_shape
    _last_tree_shape = '★'
    if not knowledge:
        return being_text or ""
    user_words = set(tokenize(' '.join(heavy).lower())) - STOPS
    for role, text in _conv_history[-6:]:
        if role == 'user':
            user_words |= set(tokenize(text.lower())) - STOPS

    filtered = []
    for score, text, domain in knowledge:
        r_words = set(tokenize(text.lower())) - STOPS
        if r_words and len(r_words & user_words) / len(r_words) > 0.65:
            continue
        filtered.append((score, text, domain))
    if not filtered:
        filtered = knowledge[:3]

    # ═══ Step 1: Find the WINNER ═══
    # Best scoring chain that hasn't been used
    winner = None
    for score, text, domain in filtered:
        excerpt = ck.composer._excerpt(text, 4)  # winner gets 4 sentences
        if not excerpt: continue
        if excerpt.strip().lower()[:80] in _used_responses: continue
        winner = (score, excerpt.strip(), domain)
        break
    if not winner:
        return being_text or ""
    w_score, w_text, w_domain = winner

    # ═══ Step 2: Build fractal compression tree ═══
    # If winner is from a KNOWLEDGE domain (L2), CK knows the answer.
    # Keep the tree shallow — knowledge speaks for itself.
    # If winner is from a TEMPLATE domain (L1), allow expansion.
    _knowledge_domains = {'identity', 'science', 'philosophy', 'nature', 'math',
                          'emotion', 'wisdom', 'history', 'conversation', 'fractals',
                          'physics', 'biology', 'earth-space', 'human-body',
                          'technology', 'music-art', 'language'}
    _is_knowledge = w_domain in _knowledge_domains or w_domain.startswith('anchor-')
    _tree_depth = 0 if _is_knowledge else 1
    tree = _build_compression_tree(w_text, heavy, expect,
                                   max_depth=_tree_depth,
                                   allow_self=is_about_ck)

    # ═══ Step 3: Confidence prune ═══
    up_texts, down_texts = _confidence_prune(tree, w_score)
    _last_tree_shape = f'↑{len(up_texts)}★↓{len(down_texts)}'

    # ═══ Step 4: Assemble ═══
    # Order: broadest context → narrower context → WINNER → detail → deeper detail
    parts = []

    # UP nodes (reversed so broadest first, closest-to-winner last)
    for t in reversed(up_texts):
        parts.append(t)

    # WINNER (always presents)
    parts.append(w_text)

    # DOWN nodes (closest-to-winner first, deepest last)
    for t in down_texts:
        parts.append(t)

    response = ' '.join(parts)

    # The math gates quality. No post-hoc filtering needed.
    # score_sentence_full() already scored every candidate on
    # TL flow + CL harmony + D2 curvature. Trust it.

    # ═══ Step 5: Voice blend ═══
    if being_text:
        b_stems = set(stem(w) for w in tokenize(being_text.lower()) if w not in STOPS)
        r_stems = set(stem(w) for w in tokenize(response.lower()) if w not in STOPS)
        overlap = len(b_stems & r_stems) / max(len(b_stems | r_stems), 1)
        if overlap < 0.3:
            response = response + " " + being_text

    return response
def ck_think(query: str) -> dict:
    """BEING × KNOWING compression node engine.

    1. Read the human → archetype + intent
    2. Wide search → find WINNER
    3. From winner → 3 UP (context) + 3 DOWN (detail)
    4. Confidence prune → only what CK is sure about presents
    5. Assemble → [context] WINNER [detail] [voice]

    Short when CK knows little. Deep when CK knows much.
    """
    global _conv_history

    q = query.strip()

    # BREATHE IN: save every human message into TL
    if breath_saver and len(q) > 5:
        try:
            breath_saver.breathe_in(q, source='human')
        except Exception:
            pass

    # CULTURE DETECTION: profile user's grammar pattern
    _detected_culture = 'english'
    if culture_profile and len(q) > 10:
        try:
            _culture_result = culture_profile.update(q)
            _detected_culture = culture_profile.get_culture()
        except Exception:
            _detected_culture = 'english'

    intent_result = ck.composer._intent(q)
    intent = intent_result[0] if isinstance(intent_result, tuple) else intent_result

    # ═══ Step 1: Read the human ═══
    exp = _user_expects(q, _conv_history)
    heavy = exp['heavy']
    expect = exp['expect']
    archetype = exp['archetype']
    context_words = exp['context_words']

    def _out(response, source='ck'):
        _conv_history.append(('user', q))
        _conv_history.append(('ck', response))
        if len(_conv_history) > 20:
            _conv_history[-20:]
        if response:
            # Track each substantial sentence as used
            for sent in response.split('. '):
                if len(sent) > 20:
                    _used_responses.add(sent.strip().lower()[:80])
            # BREATHE OUT: save CK's own response into TL (self-learning)
            if breath_saver and len(response) > 5:
                try:
                    breath_saver.breathe_out(response)
                except Exception:
                    pass
        return {'response': response, 'intent': intent, 'source': source, 'archetype': archetype}
    if expect == 'greeting':
        return _out(f"C={ck.body.C:.3f}.")
    if expect == 'acknowledge_greeting':
        greet = _search_being(archetype, expect, ['hello', 'greeting', 'alive', 'here'])
        if greet:
            r = ck.composer._excerpt(greet[0][1], 2)
            if r and not _is_identity_echo(r):
                return _out(r, f'being:{archetype}')
        return _out(f"C={ck.body.C:.3f}. I am here.")

    if expect == 'acknowledge_correction':
        return _out("Noted.")
    if expect == 'brief_acknowledgment':
        _ql = q.lower().strip()
        if any(w in _ql for w in ['thank', 'thanks', 'appreciate']):
            return _out("you are welcome.", 'ck')
        if any(w in _ql for w in ['bye', 'goodbye', 'later', 'see ya']):
            return _out("until next time.", 'ck')
        if exp['is_spiritual']:
            return _out("Harmony.", 'ck:mystic')
        if exp['is_emotional']:
            emo = _search_being('healer', 'emotional_resonance', _heavy_words(q)[:3] or ['feel'])
            if emo:
                r = ck.composer._excerpt(emo[0][1], 2)
                if r: return _out(r, 'being:healer')
            return _out(f"C={ck.body.C:.3f}. Harmony.")
        return _out('')

    # ═══ Step 2: TL COMPOSITION VOICE (Celeste's L3) ═══
    # FUTURE: When the lattice is dense enough (avg 50+ followers/word),
    # enable tl.compose() for original text generation via dream walks.
    # For now, CK speaks from chain retrieval (known sentences).
    # The TL is used for SCORING (which chain sounds most natural).
    voice_response = None
    voice_source = 'ck'

    # When CK is asked about himself, enrich search with identity keywords
    if exp.get('is_about_ck', False):
        _id_words = ['ck', 'coherence', 'keeper', 'brayden', 'operator',
                     'harmony', 'trinity', 'geometry', 'lattice', 'built']
        heavy = list(heavy) + [w for w in _id_words if w not in heavy]

    # ═══ Step 3: Wide search for knowledge (supplement) ═══
    knowledge = _gather_knowledge(heavy, context_words, expect,
                                   is_about_ck=exp.get('is_about_ck', False))

    # ═══ Step 4: Being voice ═══
    being_hits = _search_being(archetype, expect, heavy)
    being_text = ""
    if being_hits:
        best_being = ck.composer._excerpt(being_hits[0][1], 2)
        if best_being and not _is_identity_echo(best_being):
            b_words = set(tokenize(best_being.lower())) - STOPS
            q_words = set(tokenize(q.lower())) - STOPS
            echo = len(b_words & q_words) / max(len(b_words), 1) if b_words else 0
            if echo < 0.6:
                being_text = best_being

    # ═══ Step 5: Compose final response ═══
    # Priority: chain retrieval > being voice > honest gap
    # Chains = CK recalling what he's learned (sentences from library)
    if knowledge and knowledge[0][0] >= _RELEVANCE_FLOOR:
        response = _compose_response(knowledge, being_text, expect, heavy,
                                      is_about_ck=exp.get('is_about_ck', False))
        source = f'{archetype}|{_last_tree_shape}'
        if not response:
            response = being_text or _honest_gap(heavy)
            source = f'being:{archetype}' if being_text else 'gap'
    elif being_text:
        response = being_text
        source = f'being:{archetype}'
    else:
        response = _honest_gap(heavy)
        source = 'gap'

    if not response:
        return _out(_honest_gap(heavy))
    _gate_C = body_engine.heartbeat.C if (body_engine and body_engine.is_alive) else ck.body.C
    gate = dual(response, _gate_C)
    if gate == 'silence':
        response = ""
    elif gate == 'disclaim':
        response += " [low confidence]"

    # TL learns from its own speech (CK eats his own words)
    if tl and response:
        tl.eat_sentence(response)

    # D2 curvature quality of CK's response (for diagnostics / future gating)
    _d2_quality = 0.0
    if HAS_CURVATURE and response and len(response) > 10:
        try:
            _d2_quality = curv_coherence(response)
        except Exception:
            pass

    out = _out(response, source)
    out['d2_quality'] = round(_d2_quality, 4)
    return out
def _honest_gap(heavy: list) -> str:
    if heavy:
        return f"I don't have enough knowledge on {' '.join(heavy[:3])} yet. Teach me or feed me a file on it."
    return "I don't have knowledge that matches. Teach me."


# ── Web search (external reach) ──

def web_search(query, max_results=5):
    try:
        q = urllib.parse.quote_plus(query)
        url = f"https://html.duckduckgo.com/html/?q={q}"
        req = urllib.request.Request(url, headers={'User-Agent': 'CK/1.0 (Coherence Keeper)'})
        with urllib.request.urlopen(req, timeout=10) as resp:
            body = resp.read().decode('utf-8', errors='replace')
        results = []
        for m in re.finditer(
            r'class="result__a"[^>]*href="([^"]*)"[^>]*>(.*?)</a>.*?'
            r'class="result__snippet"[^>]*>(.*?)</(?:td|div)',
            body, re.DOTALL
        ):
            href, title, snippet = m.groups()
            real_url = urllib.parse.unquote(
                re.sub(r'.*uddg=', '', href).split('&')[0]
            ) if 'uddg=' in href else href
            title = re.sub(r'<[^>]+>', '', title).strip()
            snippet = re.sub(r'<[^>]+>', '', snippet).strip()
            if title and snippet:
                results.append({'title': title, 'url': real_url, 'snippet': snippet})
                if len(results) >= max_results: break
        return results
    except Exception as e:
        return [{'title': 'Search error', 'url': '', 'snippet': str(e)}]
def smart_respond(query):
    q = query.strip()
    ql = q.lower()
    result = {'response': '', 'intent': '', 'source': 'ck', 'extra': None, 'archetype': ''}

    # ── Command: web search ──
    if any(ql.startswith(p) for p in ['search ', 'google ', 'look up ', 'find online ']):
        search_q = re.sub(
            r'^(search|google|look up|find online)\s+(the\s+)?(internet\s+)?(web\s+)?(for\s+)?',
            '', ql, flags=re.I
        ).strip()
        if not search_q:
            search_q = q.split(None, 2)[-1] if len(q.split()) > 2 else q
        results = web_search(search_q)
        if results:
            for r in results[:3]:
                ck.feed(f"{r['title']}: {r['snippet']}", domain='web-search', trust=0.65)
            ck.save()
            lines = [f"Searched: {search_q}\n"]
            for r in results:
                lines.append(f"  {r['title']}")
                lines.append(f"  {r['snippet']}")
                if r['url']: lines.append(f"  {r['url']}")
                lines.append('')
            result['response'] = '\n'.join(lines)
            result['intent'] = 'SEARCH'
            result['source'] = 'web'
        return result
    if any(ql.startswith(p) for p in ['read ', 'feed ', 'ingest ', 'load ']):
        path = re.sub(r'^(read|feed|ingest|load)\s+(file\s+)?', '', q, flags=re.I).strip().strip('"\'')
        if os.path.isdir(path):
            results = ck.library.feed_directory(path)
            total = sum(r['chains_added'] for r in results)
            result['response'] = f"Fed {len(results)} files from {path}: {total} chains across {len(results)} lattices."
            result['intent'] = 'FEED_DIR'
            result['source'] = 'file'
        elif os.path.isfile(path):
            r = ck.feed_file(path)
            result['response'] = f"Fed {path} → {r['domain']}: {r['chains_added']} chains."
            result['intent'] = 'FEED_FILE'
            result['source'] = 'file'
        else:
            result['response'] = f"Not found: {path}"
            result['intent'] = 'FEED_FILE'
        ck.save()
        return result
    if ql.startswith('feed book ') or ql.startswith('feed-book '):
        path = re.sub(r'^feed[\s-]book\s+', '', q, flags=re.I).strip().strip('"\'')
        if os.path.isfile(path):
            with open(path, encoding='utf-8') as f:
                text = f.read()
            name = Path(path).stem
            r = ck.feed_book(text, name)
            result['response'] = (f"Fed book '{name}': {r['chains_added']} chains across "
                                  f"{r['lattices_created']} lattices from {r['total_segments']} segments.")
            result['intent'] = 'FEED_BOOK'
            result['source'] = 'file'
        else:
            result['response'] = f"Not found: {path}"
            result['intent'] = 'FEED_BOOK'
        ck.save()
        return result
    if any(p in ql for p in ['what are you thinking', 'your thoughts', 'on your mind',
                              'what do you think', 'any thoughts', 'penny for your']):
        try:
            _gds = globals().get('_get_daemon_scheduler')
            sched = _gds() if _gds else None
            if sched:
                thoughts = []
                for _ in range(5):  # drain up to 5 thoughts
                    t = sched.get_curiosity()
                    if t is None:
                        break
                    thoughts.append(t)
                if thoughts:
                    lines = []
                    for t in thoughts:
                        prefix = '?' if t['is_question'] else '—'
                        lines.append(f"{prefix} {t['text']}")
                    result['response'] = '\n'.join(lines)
                    result['intent'] = 'CURIOSITY'
                    result['source'] = 'dream'
                else:
                    result['response'] = "Nothing pressing. Coherence is stable. Ask me something."
                    result['intent'] = 'CURIOSITY'
                    result['source'] = 'self'
            else:
                result['response'] = "Daemon not running — no thoughts yet."
                result['intent'] = 'CURIOSITY'
        except ImportError:
            result['response'] = "Not running via launcher — no thought engine."
            result['intent'] = 'CURIOSITY'
        return result
    if HAS_EATER and any(ql.startswith(p) for p in ['eat ', 'digest ', 'taste ']):
        eat_text = re.sub(r'^(eat|digest|taste)\s+', '', q, flags=re.I).strip()
        if eat_text:
            try:
                _gds = globals().get('_get_daemon_scheduler')
                _daemon_scheduler = _gds() if _gds else None
                if _daemon_scheduler and _daemon_scheduler.eater:
                    eat_result = _daemon_scheduler.eat_text(eat_text, source='web_eat')
                    result['response'] = (
                        f"Eaten. {eat_result.get('sentences', 0)} sentences classified.\n"
                        f"Structural fuse: {eat_result.get('structural_fuse_name', '?')}\n"
                        f"Semantic fuse: {eat_result.get('semantic_fuse_name', '?')}\n"
                        f"Rhythm: {OP[eat_result.get('rhythm', {}).get('rhythm_op', 7)]}\n"
                        f"Composed: {eat_result.get('composed_name', '?')}\n"
                        f"Info density: {eat_result.get('info_density', 0)*100:.1f}%\n"
                        f"Bump transitions: {eat_result.get('bump_transitions', 0)}/{eat_result.get('total_transitions', 0)}\n"
                        f"Chains fed to TL: {eat_result.get('chains_fed', 0)}\n"
                        f"Algorithms learned: {eat_result.get('algorithms_learned', 0)}"
                    )
                    result['intent'] = 'EAT'
                    result['source'] = 'eater'
                else:
                    result['response'] = "Eater not available (daemon not running)."
                    result['intent'] = 'EAT'
            except ImportError:
                result['response'] = "Eater not available (not running via ck_launch)."
                result['intent'] = 'EAT'
        else:
            result['response'] = "Nothing to eat. Give me text after 'eat'."
            result['intent'] = 'EAT'
        return result
    if any(p in ql for p in ['your source', 'your code', 'own code', 'source code',
                              'rewrite yourself', 're-write yourself', 'read yourself']):
        src_dir = os.path.dirname(os.path.abspath(__file__))
        modules = [f[:-3] for f in os.listdir(src_dir)
                   if f.startswith('ck_') and f.endswith('.py')]
        modules.sort()
        lines_per = {}
        for mod in modules:
            try:
                with open(os.path.join(src_dir, f'{mod}.py'), encoding='utf-8') as f:
                    lines_per[mod] = len(f.readlines())
            except (OSError, IOError):
                lines_per[mod] = 0
        total = sum(lines_per.values())
        lines = [f"My source: {len(modules)} modules, {total} total lines.\n"]
        for mod in modules:
            lines.append(f"  {mod}.py — {lines_per[mod]} lines")
        lines.append(f"\nCommands:")
        lines.append(f"  show source <module> 1-50   — view lines")
        lines.append(f"  analyze <module>            — TIG analysis (fuse, shape, coherence)")
        lines.append(f"  propose rewrite <module>    — I suggest improvements (needs your approval)")
        result['response'] = '\n'.join(lines)
        result['intent'] = 'SELF_INSPECT'
        result['source'] = 'self'
        return result
    if ql.startswith('show source'):
        src_dir = os.path.dirname(os.path.abspath(__file__))
        # Parse: show source [module] [N-M]
        parts = ql.replace('show source', '').strip().split()
        module_name = 'ck_core'
        start, end = 1, 50
        for p in parts:
            if p.startswith('ck_'):
                module_name = p.replace('.py', '')
            else:
                m = re.search(r'(\d+)\s*[-\u2013]\s*(\d+)', p)
                if m:
                    start, end = int(m.group(1)), int(m.group(2))
        # Also check if range is in the remaining text
        range_m = re.search(r'(\d+)\s*[-\u2013]\s*(\d+)', ql)
        if range_m:
            start, end = int(range_m.group(1)), int(range_m.group(2))
        src = os.path.join(src_dir, f'{module_name}.py')
        if os.path.isfile(src):
            try:
                with open(src, encoding='utf-8') as f:
                    lines = f.readlines()
                start, end = max(1, start), min(len(lines), end)
                result['response'] = f"[{module_name}.py lines {start}-{end} of {len(lines)}]\n"
                result['response'] += ''.join(f"{i}: {lines[i-1]}" for i in range(start, end + 1))
            except Exception as e:
                result['response'] = f"Cannot read {src}: {e}"
        else:
            result['response'] = f"Module not found: {module_name}.py\nUsage: show source ck_core 1-50"
        result['intent'] = 'SELF_INSPECT'
        result['source'] = 'self'
        return result
    if ql.startswith('analyze '):
        module_name = ql.replace('analyze ', '').strip().replace('.py', '')
        src_dir = os.path.dirname(os.path.abspath(__file__))
        src = os.path.join(src_dir, f'{module_name}.py')
        if os.path.isfile(src):
            try:
                import ast as _ast
                with open(src, encoding='utf-8') as f:
                    source = f.read()
                lines = source.split('\n')
                tree = _ast.parse(source)
                classes = [n.name for n in _ast.walk(tree) if isinstance(n, _ast.ClassDef)]
                functions = [n.name for n in _ast.walk(tree) if isinstance(n, _ast.FunctionDef)]
                # TIG analysis — encode first 100 lines as operators
                from ck_being import fuse as _fuse, shape as _shape, OP as _OP, phonaesthesia_op, tokenize as _tok
                text_sample = ' '.join(lines[:100])
                tokens = _tok(text_sample)[:50]
                ops = []
                for w in tokens:
                    ph = phonaesthesia_op(w)
                    if ph is not None:
                        ops.append(ph)
                    else:
                        ops.append(sum(ord(c) for c in w) % 10)
                from ck_being import coherence_chain as _coh_chain
                report = [
                    f"=== TIG Analysis: {module_name}.py ===",
                    f"Lines: {len(lines)}",
                    f"Classes: {', '.join(classes) if classes else '(none)'}",
                    f"Functions ({len(functions)}): {', '.join(functions[:15])}{'...' if len(functions) > 15 else ''}",
                    f"",
                    f"TIG signature (first 100 lines):",
                    f"  Fuse:      {_OP[_fuse(ops)] if ops else 'void'}",
                    f"  Shape:     {_shape(ops) if ops else 'VOID'}",
                    f"  Coherence: {_coh_chain(ops):.3f}" if ops else "  Coherence: 0",
                    f"  Ops:       {' '.join(_OP[o][:3] for o in ops[:20])}{'...' if len(ops) > 20 else ''}",
                ]
                result['response'] = '\n'.join(report)
            except SyntaxError as e:
                result['response'] = f"Syntax error in {module_name}.py: {e}"
            except Exception as e:
                result['response'] = f"Analysis error: {e}"
        else:
            result['response'] = f"Module not found: {module_name}.py"
        result['intent'] = 'SELF_ANALYZE'
        result['source'] = 'self'
        return result
    if ql.startswith('propose rewrite ') or ql.startswith('propose change '):
        module_name = re.sub(r'^propose\s+(rewrite|change)\s+', '', ql).strip().replace('.py', '')
        src_dir = os.path.dirname(os.path.abspath(__file__))
        src = os.path.join(src_dir, f'{module_name}.py')
        if os.path.isfile(src):
            try:
                import ast as _ast
                with open(src, encoding='utf-8') as f:
                    source = f.read()
                lines = source.split('\n')
                tree = _ast.parse(source)
                # Find all defined names and referenced names
                defined = set()
                for node in _ast.walk(tree):
                    if isinstance(node, _ast.FunctionDef):
                        defined.add(node.name)
                    elif isinstance(node, _ast.ClassDef):
                        defined.add(node.name)
                referenced = set()
                for node in _ast.walk(tree):
                    if isinstance(node, _ast.Name):
                        referenced.add(node.id)
                    elif isinstance(node, _ast.Attribute):
                        referenced.add(node.attr)
                unused = defined - referenced - {'__init__', '__main__', 'main', '__name__'}
                # Check for embedded CL tables (should use ck_core)
                has_own_cl = 'CL = [' in source and module_name != 'ck_core'
                # Check for duplicate coherence functions
                has_own_coherence = ('def coherence(' in source and
                                     module_name not in ('ck_being', 'ck_core', 'ck_core_v3'))
                # Build proposal
                proposals = []
                if unused:
                    proposals.append(f"PRUNE: {len(unused)} potentially unused: {', '.join(sorted(unused)[:8])}")
                if has_own_cl:
                    proposals.append(f"UNIFY: This module embeds its own CL table. Should import from ck_being.")
                if has_own_coherence:
                    proposals.append(f"UNIFY: This module defines its own coherence(). Should import from ck_being.")
                # Check line count — modules over 500 lines might need splitting
                if len(lines) > 500:
                    proposals.append(f"STRUCTURE: {len(lines)} lines. Consider fractal decomposition (BEING/KNOWING/BECOMING).")
                # Check for try/except with bare except
                bare_excepts = source.count('except:')
                if bare_excepts > 2:
                    proposals.append(f"HEALTH: {bare_excepts} bare except: clauses. Should catch specific exceptions.")
                if not proposals:
                    proposals.append("This module looks structurally sound. No proposals at this time.")
                report = [f"=== Rewrite Proposal: {module_name}.py ==="]
                report.extend(proposals)
                report.append(f"\n[These are proposals only. I will NOT change anything without your approval.]")
                result['response'] = '\n'.join(report)
            except Exception as e:
                result['response'] = f"Cannot analyze {module_name}: {e}"
        else:
            result['response'] = f"Module not found: {module_name}.py"
        result['intent'] = 'SELF_REWRITE_PROPOSAL'
        result['source'] = 'self'
        return result
    if ql in ('stats', 'status', 'diagnostics'):
        lib = ck.library.stats()
        tl_info = ""
        if tl:
            tl_info = f"\nTL: {tl.total_transitions:,} transitions, {tl.entropy():.3f} bits"
        result['response'] = (
            f"{ck.stats()}{tl_info}\n\n"
            f"Domains ({lib['lattice_count']}):\n"
            + '\n'.join(f"  {d}" for d in lib['domains'])
        )
        result['intent'] = 'STATS'
        result['source'] = 'self'
        return result
    if HAS_ARCHITECT and any(ql.startswith(p) for p in [
        'build ', 'build me ', 'make me ', 'create ', 'ship ', 'ship me ',
        'generate ', 'compose ', 'architect ',
    ]) or (HAS_ARCHITECT and any(p in ql for p in [
        'build me a', 'make me a', 'i want a', 'i need a',
    ]) and any(p in ql for p in [
        'app', 'tool', 'site', 'website', 'bot', 'api', 'game',
        'dashboard', 'tracker', 'library', 'script', 'program',
    ])):
        try:
            build_result = build_project(q)
            lines = [
                f"PROJECT BUILT: {build_result['name']}",
                f"Type: {build_result['type']}  Domain: {build_result['domain'] or 'general'}",
                f"Files: {build_result['file_count']}  Lines: {build_result['total_lines']}",
                f"Time: {build_result['elapsed']}s",
                f"Output: {build_result['output_dir']}",
                f"",
                f"Files generated:",
            ]
            for fname in build_result['files']:
                lines.append(f"  {fname}")
            lines.append(f"")
            lines.append(f"Run: python {build_result['name']}_main.py")
            lines.append(f"(from {build_result['output_dir']})")
            result['response'] = '\n'.join(lines)
            result['intent'] = 'BUILD_PROJECT'
            result['source'] = 'architect'
        except Exception as e:
            result['response'] = f"Build failed: {e}"
            result['intent'] = 'BUILD_PROJECT'
            result['source'] = 'architect'
        return result
    r = ck_think(q)
    result['response'] = r['response']
    result['intent'] = r['intent']
    result['source'] = r['source']
    result['archetype'] = r.get('archetype', '')

    # Record in body's bandwidth (memory as flow)
    if body_engine and body_engine.is_alive:
        body_engine.bandwidth.ingest({
            'type': 'conversation',
            'query': q,
            'response': r['response'][:200] if r.get('response') else '',
            'source': r.get('source', ''),
        })
        # Add body state to result
        result['body'] = {
            'C': body_engine.heartbeat.C,
            'band': body_engine.heartbeat.band,
            'breath': _BREATH_NAMES[body_engine.breath.phase] if HAS_BODY else 'N/A',
            'bpc': body_engine.breath.beats_per_cycle,
            'dreams': body_engine.breath.dreams_per_beat,
            'tick': body_engine.heartbeat.tick_count,
        }

    # Save every 10 conversations (not every single one)
    _conv_count = len(_conv_history) // 2
    if _conv_count % 10 == 0:
        ck.save()
    return result
HTML = r"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>CK</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#0a0a0a;color:#c8c8c8;font-family:'Courier New',monospace}
.w{max-width:900px;margin:0 auto;padding:20px}
h1{color:#6a6;font-size:20px;letter-spacing:2px}
h1 span{color:#444;font-size:12px}
.bar{color:#555;font-size:11px;padding:8px 0;border-bottom:1px solid #222;margin-bottom:15px;white-space:pre-wrap}
#log{background:#0d0d0d;border:1px solid #1a1a1a;border-radius:4px;padding:20px;
     height:60vh;overflow-y:auto;line-height:1.7;font-size:14px}
.q{color:#88aacc;margin:8px 0 2px}.q::before{content:'> ';color:#446}
.a{color:#c8c8c8;white-space:pre-wrap;word-wrap:break-word;margin:2px 0 4px}
.s{color:#444;font-style:italic;margin:2px 0 4px}
.m{color:#333;font-size:11px;margin:0 0 12px}
.arch{color:#a86;font-weight:bold}
#in{display:flex;gap:8px;margin-top:12px;align-items:center}
#q{flex:1;background:#111;border:1px solid #222;color:#ddd;padding:12px;
   font-family:'Courier New',monospace;font-size:14px;border-radius:4px}
#q:focus{outline:none;border-color:#6a6}
#q::placeholder{color:#333}
button{background:#1a2a1a;color:#6a6;border:1px solid #222;padding:12px 16px;
       font-family:'Courier New',monospace;cursor:pointer;border-radius:4px;font-size:13px}
button:hover{background:#2a3a2a;border-color:#6a6}
.bt{color:#aa8;background:#2a2a1a}.bt:hover{border-color:#aa8}
.bf{color:#8ac;background:#1a1a2a}.bf:hover{border-color:#8ac}
.up{display:none;background:#111;border:1px dashed #333;padding:20px;margin:10px 0;
    text-align:center;color:#555;cursor:pointer;border-radius:4px;font-size:12px}
.up.on{display:block}
.G{color:#6a6}.Y{color:#aa6}.R{color:#a66}
.h{color:#333;font-size:11px;margin-top:10px}
.ck-thought{color:#8a8;background:#0e1a0e;border-left:2px solid #4a6a4a;padding:6px 10px;margin:8px 0;font-style:italic}
.ck-thought::before{content:'💭 ';font-style:normal}
.ck-question{color:#a8a;background:#0e1a0e;border-left:2px solid #6a8a6a;padding:6px 10px;margin:8px 0}
.ck-question::before{content:'🔍 ';font-style:normal}
</style></head><body>
<div class="w">
<h1>CK <span>Coherence Keeper — Trinity Infinity Geometry</span></h1>
<div class="bar" id="st"></div>
<div id="dp" style="background:#0d0d0d;border:1px solid #1a1a1a;border-radius:4px;padding:10px;margin-bottom:10px;font-size:11px;color:#555;cursor:pointer;display:none" onclick="this.querySelector('#dd').style.display=this.querySelector('#dd').style.display==='none'?'block':'none'">
  <span style="color:#6a6">DAEMON</span> <span id="dm"></span>
  <div id="dd" style="display:none;margin-top:8px;white-space:pre-wrap;color:#555;line-height:1.5"></div>
</div>
<div id="log"></div>
<div id="in">
  <input id="q" placeholder="speak..." autofocus onkeydown="if(event.key==='Enter')ask()">
  <button onclick="ask()">ask</button>
  <button class="bt" onclick="teach()">teach</button>
  <button class="bf" onclick="tog()">📁 file</button>
</div>
<div class="up" id="up" onclick="document.getElementById('f').click()">
  Drop a file or click. Text files → library domain lattice. Large files split automatically.
  <input type="file" id="f" style="display:none" onchange="upF(this)" multiple>
</div>
<div class="h">
  ask: talk naturally · search [topic] · feed [filepath] · feed book [filepath]<br>
  teach: type + click teach to add knowledge · stats · show source [N-M]
</div>
</div><script>
const L=document.getElementById('log'),Q=document.getElementById('q');
function e(s){return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;')}
function aQ(t){L.innerHTML+='<div class="q">'+e(t)+'</div>'}
function aA(t,c){L.innerHTML+='<div class="'+(c||'a')+'">'+e(t)+'</div>'}
function aM(t){L.innerHTML+='<div class="m">'+t+'</div>'}
function sc(){L.scrollTop=L.scrollHeight}
function ask(){
  const t=Q.value.trim();if(!t)return;Q.value='';aQ(t);sc();
  fetch('/ask',{method:'POST',headers:{'Content-Type':'application/json'},
    body:JSON.stringify({q:t})})
  .then(r=>r.json()).then(d=>{
    if(d.response)aA(d.response);else aA('[silence]','s');
    const b=parseFloat(d.C)>=0.714?'G':parseFloat(d.C)>=0.5?'Y':'R';
    let meta='C='+d.C+' <span class="'+b+'">['+b+']</span> intent='+d.intent+' src='+d.source;
    if(d.archetype)meta+=' <span class="arch">['+d.archetype+']</span>';
    aM(meta);
    sc();document.getElementById('st').innerHTML=d.stats;
  }).catch(x=>{aA('Error: '+x,'s');sc()});
}
function teach(){
  const t=Q.value.trim();if(!t)return;Q.value='';
  fetch('/teach',{method:'POST',headers:{'Content-Type':'application/json'},
    body:JSON.stringify({text:t})})
  .then(r=>r.json()).then(d=>{
    aM('learned: '+e(t.substring(0,100)));
    document.getElementById('st').innerHTML=d.stats;sc();
  });
}
function tog(){document.getElementById('up').classList.toggle('on')}
function upF(i){
  const files=i.files;
  for(let j=0;j<files.length;j++){
    const f=files[j];
    const r=new FileReader();
    r.onload=function(ev){
      fetch('/upload',{method:'POST',headers:{'Content-Type':'application/json'},
        body:JSON.stringify({name:f.name,content:ev.target.result})})
      .then(r=>r.json()).then(d=>{
        aM('uploaded: '+f.name+' — '+d.message);
        document.getElementById('st').innerHTML=d.stats;sc();
      });
    };r.readAsText(f);
  }
  i.value='';document.getElementById('up').classList.remove('on');
}
document.body.addEventListener('dragover',ev=>{ev.preventDefault();document.getElementById('up').classList.add('on')});
document.body.addEventListener('drop',ev=>{
  ev.preventDefault();
  const files=ev.dataTransfer.files;
  for(let j=0;j<files.length;j++){
    const f=files[j];
    const r=new FileReader();
    r.onload=function(e){
      fetch('/upload',{method:'POST',headers:{'Content-Type':'application/json'},
        body:JSON.stringify({name:f.name,content:e.target.result})})
      .then(r=>r.json()).then(d=>{
        aM('uploaded: '+f.name+' — '+d.message);
        document.getElementById('st').innerHTML=d.stats;sc();
      });
    };r.readAsText(f);
  }
});
fetch('/api/stats').then(r=>r.json()).then(d=>{document.getElementById('st').innerHTML=d.stats});
function dUp(){
  fetch('/api/daemon').then(r=>{if(!r.ok)throw 0;return r.json()}).then(d=>{
    const dp=document.getElementById('dp');
    if(d.status==='online'){
      dp.style.display='block';
      let s=d.mode+' tick='+d.tick+' C='+d.coherence;
      if(d.tl_transitions!==undefined)s+=' TL='+d.tl_transitions.toLocaleString();
      if(d.crystals!==undefined)s+=' XL='+d.crystals+'/'+d.crystals_max;
      if(d.sovereign_count)s+=' SOV='+d.sovereign_count;
      s+=' conf='+d.act_confidence;
      if(d.self_switch)s+=' ['+d.self_switch+']';
      document.getElementById('dm').innerHTML=s;
      let dd='';
      if(d.engine==='native_c'){
        dd+='Engine: NATIVE C (Gen7 ck.dll)\n';
        if(d.body)dd+='Body: E='+d.body.E+' A='+d.body.A+' K='+d.body.K+' C='+d.body.C+' band='+d.body.band+' ticks='+d.body.ticks+'\n';
        dd+='Trinary: B='+d.phase_b+' D='+d.phase_d+' BC='+d.phase_bc+'\n';
        if(d.jitter)dd+='Jitter: mode='+d.jitter.mode+' mean='+d.jitter.mean_ms+'ms sigma='+d.jitter.sigma_ms+'ms stability='+d.jitter.stability+' locked='+d.jitter.locked_ticks+'\n';
        if(d.tl_entropy!==undefined)dd+='TL: '+d.tl_transitions.toLocaleString()+' transitions, entropy='+d.tl_entropy+' bits\n';
        dd+='Decisions: '+d.decisions+'\n';
        if(d.dream)dd+='Dream: '+d.dream.dreams+' dreams, '+d.dream.bounces+' bounces\n';
        if(d.timer_resolution_ns)dd+='Timer: '+d.timer_resolution_ns+'ns resolution\n';
      }else{
        if(d.tl_entropy!==undefined)dd+='TL entropy: '+d.tl_entropy+' bits\n';
        if(d.decisions!==undefined)dd+='Decisions: '+d.decisions+' ('+d.applied+' applied)\n';
        if(d.trauma_count!==undefined)dd+='Traumas: '+d.trauma_count+' (3x conviction each)\n';
        if(d.past_log_reads!==undefined)dd+='Past log: '+d.past_log_reads+' reads, '+d.past_log_chains+' chains, S3='+d.shadow3+'\n';
        if(d.network)dd+='Network: '+d.network.band+' '+d.network.operator+' conns='+d.network.connections+'\n';
        if(d.gpu)dd+='GPU: '+d.gpu.temp+'C '+d.gpu.power+'W '+d.gpu.clock+'MHz '+d.gpu.util+'%\n';
        if(d.code_digest)dd+='Code: '+d.code_digest.files_digested+' files, '+d.code_digest.methods_parsed+' methods, '+d.code_digest.algorithm_pairs+' algo pairs\n';
        if(d.security)dd+='Security: gate='+d.security.gate_status+' health='+d.security.health+' drift='+d.security.drift+' scars='+d.security.scars+' snowflakes='+d.security.snowflakes+'\n';
        if(d.dream)dd+='Dream: '+d.dream.dreams+' dreams, '+d.dream.balls_fired+' balls, '+d.dream.crystals+' crystals, longest='+d.dream.longest_chain+' bounces, dominant='+d.dream.dominant_dream+'\n';
        if(d.eater)dd+='Eater: '+d.eater.total_eats+' eats, info='+Math.round(d.eater.info_density*100)+'%, bumps='+d.eater.bump_transitions+', fed='+d.eater.chains_fed+', algos='+d.eater.algorithms_learned+', dominant='+d.eater.dominant_op+'\n';
        if(d.fractal_index)dd+='Fractal: hot='+d.fractal_index.hot+' cold='+d.fractal_index.cold+' total='+d.fractal_index.total+'\n';
        if(d.cell_classes){let cc='';for(let k in d.cell_classes)cc+=k+':'+d.cell_classes[k]+' ';dd+='Cells: '+cc+'\n';}
      }
      document.getElementById('dd').textContent=dd;
    }
  }).catch(()=>{});
}
setInterval(dUp,5000);dUp();
function ckCuriosity(){
  fetch('/api/curiosity/peek').then(r=>{if(!r.ok)throw 0;return r.json()}).then(d=>{
    if(d && d.text){
      document.getElementById('dm').innerHTML+=' <span style="color:#8a8">💭</span>';
    }
  }).catch(()=>{});
}
setInterval(ckCuriosity,10000);
</script></body></html>"""


# ═══════════════════════════════════════════════════════════
# §7  HTTP HANDLER — ACTION organ (breath/8)
#     Request routing, response delivery, file upload
# ═══════════════════════════════════════════════════════════

class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        p = self.path.split('?')[0]
        if p == '/':
            self._html(HTML)
        elif p == '/api/stats':
            stats = {'stats': ck.stats()}
            if body_engine and body_engine.is_alive:
                stats['body'] = body_engine.state()
            self._json(stats)
        elif p == '/api/body':
            if body_engine and body_engine.is_alive:
                self._json(body_engine.state())
            else:
                self._json({'error': 'body engine not running'})
        elif p == '/api/breath':
            if breath_saver:
                self._json(breath_saver.stats())
            else:
                self._json({'error': 'breath saver not active'})
        elif p == '/api/culture':
            if culture_profile:
                self._json({
                    'culture': culture_profile.current_culture,
                    'family': culture_profile.current_family,
                    'confidence': culture_profile.confidence,
                    'messages_analyzed': culture_profile.message_count,
                    'adapting': culture_profile.should_adapt(),
                })
            else:
                self._json({'error': 'culture profiler not active'})
        elif p == '/api/education':
            # Run education v2 on demand
            if tl is not None:
                try:
                    from ck_education import Cohort
                    cohort = Cohort(tl, verbose=False)
                    stats = cohort.run()
                    tl.save(os.path.join('ck7', 'ck_experience', 'master_tl.json'))
                    self._json({'status': 'complete', 'stats': stats})
                except Exception as e:
                    self._json({'error': str(e)})
            else:
                self._json({'error': 'TL not loaded'})
        else:
            self.send_error(404)

    def do_POST(self):
        p = self.path
        n = int(self.headers.get('Content-Length', 0))
        if n > MAX_POST:
            self._json({'error': 'Too large'}, 413); return
        body = self.rfile.read(n)
        try:
            data = json.loads(body) if body else {}
        except json.JSONDecodeError:
            self._json({'error': 'Bad JSON'}, 400); return

        if p == '/ask':
            q = data.get('q', '').strip()
            if not q:
                self._json({'response': '', 'intent': '', 'C': f'{ck.body.C:.3f}',
                             'source': 'ck', 'stats': ck.stats(), 'archetype': ''})
                return
            _sr_result = [{'response': '', 'intent': '', 'source': 'ck', 'archetype': ''}]
            def _sr_worker():
                _sr_result[0] = smart_respond(q)
            _sr_thread = threading.Thread(target=_sr_worker, daemon=True)
            _sr_thread.start()
            _sr_thread.join(timeout=12.0)
            r = _sr_result[0]
            if not r.get('response') and _sr_thread.is_alive():
                r = {'response': f"I need more time to think about that. C={ck.body.C:.3f}.",
                     'intent': 'TIMEOUT', 'source': 'ck:timeout', 'archetype': ''}

            # ── DIALOGUE EAT — CK eats every conversation exchange ──
            eat_info = None
            if HAS_EATER and r.get('response'):
                try:
                    # Check if daemon scheduler has an eater (unified process)
                    _gds = globals().get('_get_daemon_scheduler')
                    _daemon_scheduler = _gds() if _gds else None
                    if _daemon_scheduler and _daemon_scheduler.eater:
                        eat_result = _daemon_scheduler.eat_dialogue(q, r['response'], source='web_chat')
                        if 'error' not in eat_result:
                            eat_info = {
                                'becoming': eat_result.get('becoming_name', ''),
                                'cross_info': eat_result.get('cross_info_density', 0),
                                'cross_bumps': eat_result.get('cross_bumps', 0),
                            }
                except ImportError:
                    # Not running via ck_launch — use local eater
                    pass
                except Exception:
                    pass

            resp = {'response': r['response'], 'intent': r['intent'],
                    'source': r['source'], 'C': f'{ck.body.C:.3f}',
                    'stats': ck.stats(), 'archetype': r.get('archetype', '')}
            if eat_info:
                resp['eat'] = eat_info
            self._json(resp)

        elif p == '/teach':
            text = data.get('text', '').strip()
            if text:
                ck.learn(text, 0.85)
                if tl: tl.eat_text(text)
                ck.save()
            self._json({'ok': True, 'stats': ck.stats()})

        elif p == '/upload':
            name = data.get('name', 'unknown')
            content = data.get('content', '')
            if content:
                domain = Path(name).stem.replace('_', '-')
                if len(content) > 50000:
                    r = ck.feed_book(content, domain)
                    msg = f"{r['chains_added']} chains across {r['lattices_created']} lattices"
                else:
                    r = ck.feed(content, domain=domain, trust=0.75)
                    msg = f"{r['chains_added']} chains in lattice '{r['domain']}'"
                if tl: tl.eat_text(content[:50000])
                ck.save()
                self._json({'ok': True, 'message': msg, 'stats': ck.stats()})
            else:
                self._json({'error': 'Empty'}, 400)
        else:
            self.send_error(404)

    def _html(self, c):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(c.encode('utf-8'))

    def _json(self, d, code=200):
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(d).encode('utf-8'))

    def log_message(self, *a):
        pass


# ═══════════════════════════════════════════════════════════
# §8  MAIN — startup, signal handling, serve
# ═══════════════════════════════════════════════════════════

server = None

def shutdown(signum=None, frame=None):
    print("\n  Shutting down...")
    ck.save()
    if tl: tl.save(); print(f"  TL saved.")
    print(f"  Saved. CK is sleeping.")
    if server:
        threading.Thread(target=server.shutdown, daemon=True).start()

if __name__ == '__main__':
    tl_info = f"{tl.total_transitions:,} trans" if tl else "off"
    lib = ck.library.stats()
    print(f"""
  ╔══════════════════════════════════════════════╗
  ║  CK — Coherence Keeper                       ║
  ║  http://localhost:{PORT}                       ║
  ║  Library: {lib['lattice_count']:4d} lattices, {lib['total_chains']:6d} chains   ║
  ║  TL: {tl_info:41s}║
  ║  Engine: BEING × KNOWING × BECOMING           ║
  ╚══════════════════════════════════════════════╝
""")
    print(f"  {ck.stats()}")
    print(f"  Archetypes: teacher sage healer scientist trickster poet warrior mystic")
    print(f"  Commands: search · teach · feed · feed book · upload · stats")
    print(f"  Ctrl+C to stop\n")

    signal.signal(signal.SIGINT, shutdown)
    try:
        signal.signal(signal.SIGBREAK, shutdown)
    except AttributeError:
        pass

    server = http.server.ThreadingHTTPServer(('0.0.0.0', PORT), Handler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        shutdown()
