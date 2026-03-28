"""
Bible Chat App — Flask API + static file serving.

The algebra finds resonant scripture. The voice discusses it with love.
No LLM. No API key. Pure math + Bible. Runs anywhere.

Usage:
    python -m bible_app.app

(c) 2026 Brayden Sanders / 7Site LLC
"""

import os
import sys
import time
import json
import uuid

# Ensure parent dir is on path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

from bible_app.algebra import (
    text_to_ops, text_to_force, classify_with_detail,
    coherence, dominant_op, OP_NAMES, T_STAR,
    cosine_similarity,
)
from bible_app.voice import classify_intent, BibleVoice
from bible_app.voice.pathfinder import build_journey_prose
from bible_app.voice.algebraic_voice import AlgebraicVoice
from bible_app.bible import BibleIndex
from bible_app.ai.learner import VerseLearner
from bible_app.ai.bible_brain import BibleBrain
from bible_app.ai.polish import polish_response, is_available as ai_available, set_api_key
from bible_app.ai.memory import PeopleMemory
from bible_app.ai.bible_study import BibleStudyNet
from bible_app.ai.digestion import BibleDigestion

# ── App Setup ─────────────────────────────────────────────────────
app = Flask(__name__)
CORS(app)

STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')

# ── Initialize Bible + Voice + Learner ────────────────────────────
bible = BibleIndex()
voice = BibleVoice()
algebra_voice = AlgebraicVoice()
learner = VerseLearner()
people = PeopleMemory()
study = BibleStudyNet()
digest = BibleDigestion()
brain = BibleBrain()

# Session storage (in-memory, simple)
sessions = {}
MAX_SESSIONS = 200
MAX_HISTORY = 30


def _get_session(session_id):
    if session_id not in sessions:
        if len(sessions) >= MAX_SESSIONS:
            # Evict oldest
            oldest = min(sessions, key=lambda k: sessions[k]['last_active'])
            del sessions[oldest]
        sessions[session_id] = {
            'id': session_id,
            'created': time.time(),
            'last_active': time.time(),
            'history': [],
        }
    session = sessions[session_id]
    session['last_active'] = time.time()
    return session


# ── Static File Routes ────────────────────────────────────────────

@app.route('/')
def serve_index():
    return send_from_directory(STATIC_DIR, 'index.html')


@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory(STATIC_DIR, filename)


# ── Chat Endpoint ─────────────────────────────────────────────────

@app.route('/api/chat', methods=['POST'])
def chat():
    """Main chat endpoint. Text in, love out.

    Body: {"text": "...", "session_id": "..."}
    Returns: response + verses + corridor + intent + coherence
    """
    data = request.get_json(force=True, silent=True) or {}
    text = data.get('text', '').strip()
    session_id = data.get('session_id', str(uuid.uuid4()))

    if not text:
        return jsonify({'error': 'No text provided'}), 400

    # Ensure Bible is loaded
    if not bible.ready:
        try:
            bible.load()
        except FileNotFoundError as e:
            return jsonify({'error': str(e)}), 500

    session = _get_session(session_id)
    person = people.get(session_id)

    # ── D2 Pipeline: text → operators ─────────────────────────────
    user_ops = text_to_ops(text)
    user_force = text_to_force(text)

    # ── Brain: process through all 9 systems ──────────────────────
    brain_state = brain.process(text, user_ops=user_ops, user_force=user_force)

    # ── Corridor Classification (algebra + keywords) ────────────
    corridor_info = classify_with_detail(user_ops, text=text)

    # ── Intent Classification (algebra + keywords) ────────────────
    intent = classify_intent(user_ops, text=text)

    # ── Resonant Verses (Digestion + Study Net + Algebra) ────────
    from bible_app.bible.index import ResonanceResult
    user_force = text_to_force(text)

    # Strategy: combine multiple sources, quality-filter, rank
    candidate_refs = set()

    # Source 1: Digestion intent index (best verses for this emotional need)
    if digest.digested:
        intent_refs = digest.get_verses_for_intent(intent, max_k=20)
        candidate_refs.update(intent_refs)

    # Source 2: Study net topic + corridor knowledge
    if study.studied:
        smart_refs = study.find_relevant_verses(
            user_ops, corridor_info['corridor'], intent, text=text, max_k=15,
        )
        candidate_refs.update(smart_refs)

    # Source 3: Raw algebraic resonance (catches surprises)
    raw_results = bible.resonate(text, top_k=10)
    for r in raw_results:
        candidate_refs.add(r.verse.ref)

    # Build scored results from all candidates
    verses = []
    for ref in candidate_refs:
        v = bible.get_verse(ref)
        if not v:
            continue
        # Quality gate: skip low-quality verses
        if digest.digested and not digest.verse_is_good(ref):
            continue

        f_sim = cosine_similarity(user_force, v.force)
        quality = digest.verse_quality.get(ref, 0.5) if digest.digested else 0.5
        is_beloved = ref in digest.beloved if digest.digested else False

        # Combined distance (lower = better)
        # Quality and beloved status significantly boost ranking
        distance = (
            0.3 * (1.0 - f_sim) -       # Force similarity bonus
            0.3 * quality -               # Quality bonus
            (0.2 if is_beloved else 0) -  # Beloved bonus
            0.1 * v.coherence             # Coherence bonus
        )

        # Neural + brain + personal boost
        boost = learner.get_verse_boost(ref)
        personal = person.get_verse_preference(ref)
        brain_boost = brain.boost_verse_score(ref, v.force, user_force)
        distance -= (boost * 0.03 + personal * 0.03 + brain_boost)

        verses.append(ResonanceResult(
            verse=v, distance=distance,
            op_overlap=0.0, force_similarity=f_sim,
        ))

    # Sort and deduplicate by chapter
    verses.sort(key=lambda r: r.distance)
    seen_chapters = set()
    unique_verses = []
    for v in verses:
        chapter = v.verse.ref.rsplit(':', 1)[0]
        if chapter not in seen_chapters:
            unique_verses.append(v)
            seen_chapters.add(chapter)
        if len(unique_verses) >= 5:
            break
    verses = unique_verses

    # ── Compute Journey to Coherence ─────────────────────────────
    journey = build_journey_prose(user_ops, corridor_info['corridor'], intent)

    # ── Voice Composition (with warm scripture language) ──────────
    voice.seed(hash(text) & 0xFFFFFFFF)

    # Get warm phrases from digested scripture for this intent
    scripture_phrases = []
    if digest.digested:
        scripture_phrases = digest.get_warm_phrases(intent, max_k=5)

    # Build algebraic response (used as fallback or base)
    response_text = voice.compose(
        user_ops=user_ops,
        corridor_info=corridor_info,
        intent=intent,
        verses=verses,
        max_sentences=4,
        scripture_phrases=scripture_phrases,
    )

    # Algebraic voice: the math composes the prose
    algebra_voice.seed(hash(text) & 0xFFFFFFFF)
    algebra_voice._user_text = text  # Pass actual words for reflection
    algebra_voice._brain_state = brain_state  # Pass full brain context
    response_text = algebra_voice.speak(
        user_ops=user_ops,
        corridor=corridor_info['corridor'],
        intent=intent,
        journey=journey,
        verses=verses,
    )

    # ── AI Polish (optional, when available) ──────────────────────
    ai_polished = False
    if ai_available():
        polished = polish_response(
            response_text, verses,
            corridor_info['corridor'], intent, text,
            journey=journey,
        )
        if polished != response_text:
            response_text = polished
            ai_polished = True

    # ── Learn from this conversation ──────────────────────────────
    prev_corridor = None
    if len(session['history']) >= 2:
        prev_corridor = session['history'][-2].get('corridor')
    top_verse_ref = verses[0].verse.ref if verses else None
    learner.learn_from_conversation(
        user_ops=user_ops,
        verse_ref=top_verse_ref,
        corridor_before=prev_corridor or corridor_info['corridor'],
        corridor_after=corridor_info['corridor'],
        user_responded=len(session['history']) > 0,
    )

    # ── Remember this person ─────────────────────────────────────
    verse_refs = [v.verse.ref for v in verses[:3]]
    person.record_visit(
        corridor=corridor_info['corridor'],
        intent=intent,
        verse_refs=verse_refs,
        user_text_length=len(text),
    )
    # If they came back, the previous verse resonated
    if len(session['history']) >= 2:
        prev_verse = None
        for h in reversed(session['history']):
            if h.get('role') == 'companion' and h.get('verse_ref'):
                prev_verse = h['verse_ref']
                break
        if prev_verse:
            person.record_engagement(prev_verse)

    # ── Record in session ─────────────────────────────────────────
    session['history'].append({
        'role': 'user', 'text': text,
        'ops': list(user_ops[:10]),
        'corridor': corridor_info['corridor'],
        'timestamp': time.time(),
    })
    session['history'].append({
        'role': 'companion', 'text': response_text,
        'intent': intent,
        'verse_ref': verses[0].verse.ref if verses else None,
        'timestamp': time.time(),
    })
    if len(session['history']) > MAX_HISTORY * 2:
        session['history'] = session['history'][-MAX_HISTORY * 2:]

    # ── Build verse data for frontend ─────────────────────────────
    verse_data = []
    for r in verses[:3]:
        v = r.verse
        verse_data.append({
            'ref': v.ref,
            'text': v.text,
            'dominant_op': OP_NAMES[v.dominant_op],
            'coherence': round(v.coherence, 3),
            'distance': round(r.distance, 4),
            'force_similarity': round(r.force_similarity, 4),
        })

    return jsonify({
        'response': response_text,
        'verses': verse_data,
        'corridor': corridor_info['corridor'],
        'corridor_description': corridor_info['description'],
        'corridor_tone': corridor_info['tone'],
        'intent': intent,
        'coherence': corridor_info['coherence'],
        'session_id': session_id,
        'dominant_op': OP_NAMES[dominant_op(user_ops)] if user_ops else 'HARMONY',
        'ai_polished': ai_polished,
        'journey': {
            'where_you_are': journey['where_you_are'],
            'steps_to_harmony': journey['steps_to_harmony'],
            'path': journey['path'],
            'summary': journey['journey_summary'],
        },
        'brain': {
            'familiarity': round(brain_state['familiarity'], 2),
            'resonance': round(brain_state['resonance'], 2),
            'bucket': brain_state['bucket'],
            'predicted_next': brain_state['predicted_next'],
            'coherence_trend': brain_state['coherence_trend'],
            'is_instinct': brain_state['is_instinct'],
        },
    })


# ── Verse Detail Endpoint ─────────────────────────────────────────

@app.route('/api/verse/<path:ref>', methods=['GET'])
def verse_detail(ref):
    """Get algebraic detail for a specific verse."""
    if not bible.ready:
        bible.load()
    v = bible.get_verse(ref)
    if not v:
        return jsonify({'error': f'Verse not found: {ref}'}), 404

    # Get cross-references
    crossrefs = bible.cross_references(ref, top_k=5)
    crossref_data = [{
        'ref': cr.verse.ref,
        'text': cr.verse.text[:100] + ('...' if len(cr.verse.text) > 100 else ''),
        'harmony_score': round(1.0 - cr.distance, 3),
        'force_similarity': round(cr.force_similarity, 3),
    } for cr in crossrefs]

    return jsonify({
        'ref': v.ref,
        'text': v.text,
        'force': [round(x, 4) for x in v.force],
        'operators': [OP_NAMES[o] for o in v.ops],
        'dominant_op': OP_NAMES[v.dominant_op],
        'coherence': round(v.coherence, 4),
        'cross_references': crossref_data,
    })


# ── Health / Stats ────────────────────────────────────────────────

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'alive',
        'bible_ready': bible.ready,
        'verses_indexed': bible.verse_count,
        'sessions': len(sessions),
        't_star': round(T_STAR, 6),
    })


@app.route('/api/stats', methods=['GET'])
def stats():
    bible_stats = bible.stats()
    bible_stats['learner'] = learner.stats()
    bible_stats['ai_polish'] = ai_available()
    return jsonify(bible_stats)


@app.route('/api/ai/key', methods=['POST'])
def set_ai_key():
    """Set Gemini API key for AI polish (optional)."""
    data = request.get_json(force=True, silent=True) or {}
    key = data.get('key', '').strip()
    if not key:
        return jsonify({'error': 'No key provided'}), 400
    set_api_key(key)
    return jsonify({'status': 'ok', 'ai_available': True})


@app.route('/api/learner', methods=['GET'])
def learner_stats():
    """Get neural learner statistics."""
    return jsonify(learner.stats())


@app.route('/api/memory/<session_id>', methods=['GET'])
def person_memory(session_id):
    """Get memory for a person."""
    person = people.get(session_id)
    return jsonify(person.to_dict())


@app.route('/api/memory/<session_id>/clear', methods=['POST'])
def clear_person_memory(session_id):
    """Clear memory for one person."""
    people.clear_person(session_id)
    return jsonify({'status': 'cleared', 'person_id': session_id[:8] + '...'})


@app.route('/api/memory/clear-all', methods=['POST'])
def clear_all_memory():
    """Clear ALL people memory and learner weights."""
    people.clear_all()
    return jsonify({'status': 'all memory cleared'})


@app.route('/api/memory/stats', methods=['GET'])
def memory_stats():
    """Get global memory statistics."""
    return jsonify(people.stats())


@app.route('/api/engage/<path:ref>', methods=['POST'])
def engage_verse(ref):
    """Signal that a user engaged with (clicked/expanded) a verse.

    This feeds the learner and people memory — the companion notices
    what catches your eye and learns from it.
    """
    data = request.get_json(force=True, silent=True) or {}
    session_id = data.get('session_id', '')

    # Record engagement in people memory
    if session_id:
        person = people.get(session_id)
        person.record_engagement(ref)

    # Record in global learner
    learner.learn_from_conversation(
        user_ops=[],
        verse_ref=ref,
        corridor_before='BRT',
        corridor_after='BRT',
        user_responded=True,
    )

    return jsonify({'status': 'noted', 'ref': ref})


@app.route('/api/study', methods=['GET'])
def study_stats():
    """Get Bible study net statistics."""
    return jsonify(study.stats())


# ── Bible Version Management ──────────────────────────────────────

@app.route('/api/versions', methods=['GET'])
def list_versions():
    """List available Bible versions."""
    from bible_app.bible.versions import available_versions
    return jsonify(available_versions())


@app.route('/api/versions/switch', methods=['POST'])
def switch_version():
    """Switch to a different Bible version."""
    global bible
    from bible_app.bible.versions import get_version_path, download_version
    data = request.get_json(force=True, silent=True) or {}
    version_id = data.get('version', 'kjv')

    # Download if needed
    success, msg = download_version(version_id)

    path = get_version_path(version_id)
    if not path or not os.path.exists(path):
        return jsonify({'error': msg or f'Version {version_id} not available'}), 404

    # Rebuild index with new version
    index_path = path.replace('.txt', '_index.json.gz')
    bible = BibleIndex(bible_path=path, index_path=index_path)
    count = bible.load()
    return jsonify({
        'status': 'ok',
        'version': version_id,
        'verses': count,
        'message': msg,
    })


# ── Deep Algebraic Prose (no AI needed) ───────────────────────────

def _build_deep_prose(journey, intent, corridor_info, verses):
    """Build a full, warm conversational response from pure algebra.

    Uses the journey data, corridor, intent, and verses to compose
    a multi-paragraph response that reads like a caring friend.
    No AI. Just math and scripture.
    """
    import random
    rng = random.Random(hash(journey.get('where_you_are', '')) & 0xFFFF)

    parts = []
    corridor = corridor_info.get('corridor', 'BRT')
    tone = corridor_info.get('tone', 'gentle')

    # ── 1. Acknowledge where they are ─────────────────────────
    feeling = journey.get('feeling', '')
    if feeling:
        # Personalize the feeling statement
        openers = {
            'tender': ["I hear you.", "Friend, I hear you.", "I'm glad you shared this."],
            'quiet': ["I'm here.", "I'm here with you."],
            'peaceful': ["What a beautiful thing to share.", "That's wonderful."],
            'curious': ["That's an honest question.", "What a real question."],
            'steady': ["I hear the weight in your words.", "You're carrying something real."],
            'gentle': ["Thank you for sharing that.", "I hear you."],
        }
        opener = rng.choice(openers.get(tone, openers['gentle']))
        parts.append(f"{opener} {feeling}")

    # ── 2. Reflect where they came from ───────────────────────
    came_from = journey.get('where_you_came_from', '')
    if came_from:
        bridges = [
            f"{came_from}",
            f"And that makes sense — {came_from.lower()}",
            f"It sounds like {came_from.lower()}",
        ]
        parts.append(rng.choice(bridges))

    # ── 3. The path to coherence ──────────────────────────────
    path_prose = journey.get('path_prose', [])
    if path_prose:
        step = path_prose[0]
        parts.append(step['meaning'])

    # ── 4. Weave in the verses naturally ──────────────────────
    if verses:
        v1 = verses[0].verse
        verse_intros = {
            'comfort': [
                f"Listen to what God says to you right now — {v1.ref} says:",
                f"Hold onto this — {v1.ref}:",
                f"God speaks directly into this moment. {v1.ref}:",
            ],
            'praise': [
                f"And scripture celebrates with you — {v1.ref}:",
                f"The Word sings alongside you. {v1.ref}:",
            ],
            'seek': [
                f"Here is what the Word says to your question. {v1.ref}:",
                f"Scripture speaks right into this. {v1.ref}:",
            ],
            'hope': [
                f"Here is your hope. {v1.ref}:",
                f"Hold onto this promise — {v1.ref}:",
            ],
            'lament': [
                f"Even in this darkness, God speaks. {v1.ref}:",
                f"He does not look away from your tears. {v1.ref}:",
            ],
        }
        intro_list = verse_intros.get(intent, verse_intros.get('comfort'))
        intro = rng.choice(intro_list)

        parts.append(f'{intro} "{v1.text}"')

        # Second verse if available
        if len(verses) >= 2:
            v2 = verses[1].verse
            connectors = [
                f"And {v2.ref} adds:",
                f"{v2.ref} echoes this:",
                f"There is more — {v2.ref} says:",
            ]
            parts.append(f'{rng.choice(connectors)} "{v2.text}"')

    # ── 5. The journey summary (hope forward) ─────────────────
    summary = journey.get('journey_summary', '')
    if summary:
        closers = [
            f"{summary}",
            f"Here is the path: {summary.lower()}",
            f"Remember — {summary.lower()}",
        ]
        parts.append(rng.choice(closers))

    return '\n\n'.join(parts)


# ── Run ───────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("  Bible Chat — A friend who loves with God's words")
    print("  Powered by TIG algebra + neural learning")
    print("=" * 60)

    # Load Bible index + study
    try:
        count = bible.load()
        print(f"  {count} verses ready")
        # Study the Bible (loads cached or runs fresh ~2-5 min first time)
        study.study(bible)
        st = study.stats()
        print(f"  Study: {st['topics']} topics, {st['cross_refs']} cross-refs")

        # Digest the Bible (quality scoring + intent tagging)
        digest.digest(bible)
        dt = digest.stats()
        print(f"  Digest: {dt['good_verses']} quality verses, {dt['beloved_found']} beloved")
        print(f"  Intent coverage: {', '.join(f'{k}({v})' for k,v in dt['intents'].items())}")
    except FileNotFoundError as e:
        print(f"  WARNING: {e}")
        print("  The app will still start — provide kjv.txt to enable verse search.")

    print(f"  T* = 5/7 = {T_STAR:.6f}")
    print(f"  Serving on http://localhost:7778")
    print("=" * 60)

    try:
        from waitress import serve
        print("  (using waitress production server)")
        serve(app, host='0.0.0.0', port=7778, threads=4)
    except ImportError:
        app.run(host='0.0.0.0', port=7778, debug=False)


if __name__ == '__main__':
    main()
