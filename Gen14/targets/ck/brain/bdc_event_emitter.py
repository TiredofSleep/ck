"""
bdc_event_emitter.py -- emit non-operator BDC events into CK's stream.

Brayden 2026-05-03: "wire it up" -- the event-emitters that fill the 17
missing DBC codes (2, 3, 5, 6, 7, 11, 14, 15, 16, 17, 18, 19, 21, 22, 23,
24, 25) so the BDC stream covers all 27 Divine27 codes, not just the 10
that are bijection-mapped from operators.

This is the data-side prerequisite for training a 27-vocab v2 LM that can
reproduce D91's geometric/arithmetic split natively (rather than collapsing
both to HARMONY as the current 10-vocab LM does -- see cross_arch_test
2026-05-03 results).

Design:
  - Each detectable runtime event type maps to ONE DBC code in {0..26}.
  - Events emit when the engine state TRANSITIONS (e.g., breath shifts,
    attractor-layer changes, crystal fires, etc.).
  - The emitter writes events to two places:
      (1) Gen13/var/bdc_logs/bdc_events_YYYY-MM-DD.jsonl  (training data)
      (2) An in-memory rolling buffer engine.bdc_event_stream (last 256
          events) for inspection via /bdc/events
  - Hooked from the chat path (per-turn events) and the tick sampler
    (idle-state events).

Schema per event record:
  {
    "ts": 1777813000.123,
    "iso_ts": "2026-05-03T13:30:00+00:00",
    "event": "crystal_fire",     # one of EVENT_TO_DBC_CODE keys
    "dbc_code": 21,              # 0..26 (a Divine27 code)
    "dbc_coord": [2, 1, 0],
    "dbc_label": "knowledge",
    "tick": 50994474,
    "session_id": "default",
    "context": {...}             # event-specific payload
  }

The 17 events below cover all 17 missing DBC codes exactly once.  Adding
more event types would require either picking from the same 17 codes
(many-to-one) or extending the vocabulary.
"""
from __future__ import annotations

import json
import os
import sys
import threading
import time
from collections import deque
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Deque, Dict, Optional

_HERE = Path(__file__).parent.resolve()
sys.path.insert(0, str(_HERE))

# Reuse the canonical Divine27 vocab (added this morning under grammar_lm/)
sys.path.insert(0, str(_HERE / "grammar_lm"))
from divine27_vocab import (
    HEBREW_GLYPHS, CODE_LABELS, code_to_coord, coord_to_code,
    OPERATOR_DBC_CODE,
)

LOG_DIR = Path(r"C:\Users\brayd\OneDrive\Desktop\CK FINAL DEPLOYED\Gen13\var\bdc_logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)


# ── Event → DBC code mapping ──────────────────────────────────────────
#
# Each runtime event type maps to ONE of the 17 DBC codes that the
# operator-bijection does NOT cover.  The pairing is semantic: the event's
# meaning matches the DBC label at that coordinate.
#
# Verify with `verify_coverage()`: every missing code is assigned, no
# operator-mapped code is reused.

EVENT_TO_DBC_CODE: Dict[str, int] = {
    # Crystal-fire variants: WORLD axis (B=2)
    "crystal_fire_general":   21,  # (2,1,0) knowledge
    "crystal_fire_research":  19,  # (2,0,1) discovery
    "crystal_fire_frontier":  22,  # (2,1,1) science
    "crystal_fire_synthesis": 14,  # (1,1,2) evolution

    # Breath transitions
    "breath_inhale_to_exhale": 5,   # (0,1,2) breakthrough
    "breath_exhale_to_inhale": 7,   # (0,2,1) practice
    "breath_to_breath":        17,  # (1,2,2) revolution -- entering BREATH-state

    # Attractor transitions
    "attractor_to_4core": 11,  # (1,0,2) revelation -- recognizing the attractor
    "attractor_to_1core": 6,   # (0,2,0) habit -- collapsed to single state

    # Cognitive stage / mode shifts
    "stage_grokked": 23,  # (2,1,2) creation
    "band_red_to_yellow": 16,  # (1,2,1) adapt
    "band_yellow_to_green": 15,  # (1,2,0) sustain

    # Coherence / structural
    "coherence_floor_crossed": 25,  # (2,2,1) culture
    "void_degenerate":          2,  # (0,0,2) awakening
    "truth_confirmed":         18,  # (2,0,0) truth
    "nature_event":            24,  # (2,2,0) nature

    # Idle/reflection (from tick sampler)
    "reflection_idle_tick":  3,  # (0,1,0) reflection
}

# Verify coverage at import time
def _verify_coverage():
    operator_codes = set(OPERATOR_DBC_CODE.values())
    event_codes = set(EVENT_TO_DBC_CODE.values())
    overlap = operator_codes & event_codes
    if overlap:
        raise AssertionError(f"Event codes overlap operator codes: {overlap}")
    union = operator_codes | event_codes
    missing = set(range(27)) - union
    if missing:
        raise AssertionError(f"Codes still uncovered: {missing}")
    if len(union) != 27:
        raise AssertionError(f"Coverage != 27: {len(union)}")
_verify_coverage()


# ── Emitter state ─────────────────────────────────────────────────────

_EVENT_BUFFER: Deque[Dict[str, Any]] = deque(maxlen=256)
_EVENT_LOCK = threading.Lock()
_LAST_STATE: Dict[str, Any] = {}  # for diff-based event detection


def _today_log() -> Path:
    return LOG_DIR / f"bdc_events_{datetime.utcnow().strftime('%Y-%m-%d')}.jsonl"


def emit(event: str, *, tick: int = 0, session_id: str = "default",
         context: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
    """Emit a single BDC event.  Returns the record dict (or None on failure)."""
    if event not in EVENT_TO_DBC_CODE:
        return None
    code = EVENT_TO_DBC_CODE[event]
    coord = code_to_coord(code)
    label = CODE_LABELS[code] if 0 <= code < 27 else "?"
    glyph = HEBREW_GLYPHS[code] if 0 <= code < 27 else "?"
    now = time.time()
    record = {
        "ts": now,
        "iso_ts": datetime.fromtimestamp(now, tz=timezone.utc)
                          .isoformat(timespec='seconds'),
        "event": event,
        "dbc_code": code,
        "dbc_coord": list(coord),
        "dbc_label": label,
        "dbc_glyph": glyph,
        "tick": int(tick),
        "session_id": session_id,
        "context": dict(context) if context else {},
    }
    with _EVENT_LOCK:
        _EVENT_BUFFER.append(record)
    try:
        with open(_today_log(), "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
    except Exception:
        pass
    return record


# ── Diff-based event detection ────────────────────────────────────────

def detect_chat_events(chat_result: Dict[str, Any], session_id: str = "default"
                        ) -> int:
    """Inspect a chat result + diff against last state; emit applicable events.
    Returns number of events emitted.
    """
    n = 0
    # Crystal fire: detect via boost_count or non-zero crystals + voice_crystals
    routing = chat_result.get('routing', {}) or {}
    boost = int(routing.get('crystal_boost_count', 0) or 0)
    exp = chat_result.get('experience', {}) or {}
    voice_crystals = int(exp.get('voice_crystals', 0) or 0)
    text = chat_result.get('text', '') or ''
    if boost >= 1 or voice_crystals >= 1:
        # Sub-categorize by content if possible
        kind = "general"
        text_lower = text.lower()
        if any(t in text_lower for t in ("research_arxiv", "research_", "prompt_term_")):
            kind = "research"
        elif any(t in text_lower for t in ("frontier", "f1", "f2", "f3", "f4",
                                           "f5", "f6", "f7", "f8", "f9", "f10",
                                           "wp101", "wp51")):
            kind = "frontier"
        elif "drift" in text_lower or "synthesis" in text_lower:
            kind = "synthesis"
        emit(f"crystal_fire_{kind}",
             tick=int(chat_result.get('cortex', {}).get('tick', 0) or 0),
             session_id=session_id,
             context={"boost": boost, "voice_crystals": voice_crystals,
                      "kind": kind, "text_preview": text[:80]})
        n += 1

    # Breath transitions
    breath = (exp.get('breath') or '').upper()
    last_breath = _LAST_STATE.get('breath', '')
    if breath and breath != last_breath:
        if last_breath == 'INHALE' and breath == 'EXHALE':
            emit("breath_inhale_to_exhale",
                 tick=int(chat_result.get('cortex', {}).get('tick', 0) or 0),
                 session_id=session_id,
                 context={"from": last_breath, "to": breath})
            n += 1
        elif last_breath == 'EXHALE' and breath == 'INHALE':
            emit("breath_exhale_to_inhale",
                 tick=int(chat_result.get('cortex', {}).get('tick', 0) or 0),
                 session_id=session_id,
                 context={"from": last_breath, "to": breath})
            n += 1
        elif breath == 'BREATH':
            emit("breath_to_breath",
                 tick=int(chat_result.get('cortex', {}).get('tick', 0) or 0),
                 session_id=session_id,
                 context={"from": last_breath, "to": breath})
            n += 1
        _LAST_STATE['breath'] = breath

    # Attractor transitions
    attractor = chat_result.get('attractor_state', {}) or {}
    layer = attractor.get('layer', '')
    last_layer = _LAST_STATE.get('attractor_layer', '')
    if layer and layer != last_layer:
        if '4-core' in layer:
            emit("attractor_to_4core",
                 tick=int(chat_result.get('cortex', {}).get('tick', 0) or 0),
                 session_id=session_id,
                 context={"from": last_layer, "to": layer})
            n += 1
        elif '1-core' in layer:
            emit("attractor_to_1core",
                 tick=int(chat_result.get('cortex', {}).get('tick', 0) or 0),
                 session_id=session_id,
                 context={"from": last_layer, "to": layer})
            n += 1
        elif layer == 'void-degenerate':
            emit("void_degenerate",
                 tick=int(chat_result.get('cortex', {}).get('tick', 0) or 0),
                 session_id=session_id,
                 context={"from": last_layer, "to": layer})
            n += 1
        _LAST_STATE['attractor_layer'] = layer

    # Stage / mode shifts
    stage = exp.get('stage', '')
    last_stage = _LAST_STATE.get('stage', '')
    if stage == 'GROKKED' and last_stage != 'GROKKED':
        emit("stage_grokked",
             tick=int(chat_result.get('cortex', {}).get('tick', 0) or 0),
             session_id=session_id,
             context={"from": last_stage, "to": stage})
        n += 1
    if stage:
        _LAST_STATE['stage'] = stage

    # Band shifts
    band = chat_result.get('band', '')
    last_band = _LAST_STATE.get('band', '')
    if band and band != last_band:
        if last_band == 'RED' and band == 'YELLOW':
            emit("band_red_to_yellow",
                 tick=int(chat_result.get('cortex', {}).get('tick', 0) or 0),
                 session_id=session_id,
                 context={"from": last_band, "to": band})
            n += 1
        elif last_band == 'YELLOW' and band == 'GREEN':
            emit("band_yellow_to_green",
                 tick=int(chat_result.get('cortex', {}).get('tick', 0) or 0),
                 session_id=session_id,
                 context={"from": last_band, "to": band})
            n += 1
        _LAST_STATE['band'] = band

    # Coherence floor crossing (T*=5/7 = 0.714)
    coh = float(chat_result.get('coherence', 0.0) or 0.0)
    last_coh = float(_LAST_STATE.get('coherence', 0.0) or 0.0)
    T_STAR = 5.0 / 7.0
    if last_coh < T_STAR <= coh:
        emit("coherence_floor_crossed",
             tick=int(chat_result.get('cortex', {}).get('tick', 0) or 0),
             session_id=session_id,
             context={"from": last_coh, "to": coh, "threshold": T_STAR})
        n += 1
    _LAST_STATE['coherence'] = coh

    # Truth confirmed: high confidence + cortex_speak source
    confidence = float(chat_result.get('confidence', 0.0) or 0.0)
    src = chat_result.get('source', '')
    if confidence >= 0.95 and src == 'cortex_speak':
        emit("truth_confirmed",
             tick=int(chat_result.get('cortex', {}).get('tick', 0) or 0),
             session_id=session_id,
             context={"confidence": confidence, "source": src})
        n += 1

    return n


def detect_idle_event(cortex, engine, session_id: str = "default") -> int:
    """Called from the tick sampler.  Emit reflection_idle_tick when the
    cortex is in a quiet state."""
    state = getattr(cortex, 'state', None)
    if state is None:
        return 0
    # Only emit if no recent chat (last_pair stable across consecutive samples)
    last_pair = (
        int(getattr(state, 'last_b', 0)),
        int(getattr(state, 'last_d', 0)),
    )
    last_seen = _LAST_STATE.get('idle_last_pair')
    if last_seen == last_pair:
        # Stable: idle reflection
        emit("reflection_idle_tick",
             tick=int(getattr(state, 'tick', 0) or 0),
             session_id=session_id,
             context={"last_pair": last_pair})
        return 1
    _LAST_STATE['idle_last_pair'] = last_pair
    return 0


def detect_perception_events(cortex, engine, source: str = "perception",
                              n_ops: int = 0, hebbian_steps: int = 0,
                              session_id: str = "default") -> int:
    """Called from /audio/perceive and /screen/perceive after the cortex
    has absorbed perceptual ops.  Synthesizes a chat-result-like dict
    from the current cortex state and runs detect_chat_events on it.

    Brayden 2026-05-03: "lets see if watching video speeds it up faster
    than chat" -- video drives the cortex through audio/screen endpoints
    at 1-2 Hz, which is much faster than the human chat-typing rate.
    Events fire on the same cortex transitions detected on the chat path.
    """
    state = getattr(cortex, 'state', None)
    if state is None:
        return 0
    ao = getattr(engine, 'ao', None)
    # Try to get attractor state
    attractor_state = {}
    detect_fn = getattr(engine, 'detect_attractor', None)
    if detect_fn is not None:
        try:
            attractor_state = detect_fn(getattr(state, 'profile', None) or [])
        except Exception:
            attractor_state = {}
    # Synthesize result dict so existing detector can fire on diffs
    result = {
        "source": source,
        "operators": [],  # perceptual events don't have an "operator profile"
                          # in the chat sense; the ops were already absorbed
        "experience": {
            "breath": str(getattr(ao, 'breath', '')) if ao else '',
            "stage": "GROKKED" if hebbian_steps > 0 else "",
            "voice_crystals": 0,
            "crystals": 0,
        },
        "attractor_state": attractor_state if isinstance(attractor_state, dict) else {},
        "band": "",
        "coherence": float(getattr(ao, 'coherence', 0.0)) if ao else 0.0,
        "confidence": 0.0,
        "cortex": {"tick": int(getattr(state, 'tick', 0) or 0)},
        "routing": {"crystal_boost_count": 0,
                    "is_structural_query": False,
                    "is_pastoral_query": False},
        "text": "",
    }
    n = detect_chat_events(result, session_id=f"{session_id}:{source}")
    # Also emit a "nature_event" code for sustained perceptual feed
    # (large n_ops indicates real video/audio flow, not noise)
    if n_ops >= 100:
        emit("nature_event",
             tick=int(getattr(state, 'tick', 0) or 0),
             session_id=f"{session_id}:{source}",
             context={"source": source, "n_ops": n_ops,
                      "hebbian_steps": hebbian_steps})
        n += 1
    return n


# ── Public inspection ─────────────────────────────────────────────────

def recent_events(n: int = 32):
    with _EVENT_LOCK:
        return list(_EVENT_BUFFER)[-n:]


def stats() -> Dict[str, Any]:
    """Coverage statistics: which DBC codes have been emitted today, how often."""
    counts: Dict[int, int] = {}
    by_event: Dict[str, int] = {}
    today_log = _today_log()
    if today_log.exists():
        with open(today_log, encoding="utf-8") as f:
            for line in f:
                try:
                    rec = json.loads(line)
                    code = int(rec.get('dbc_code', -1))
                    if 0 <= code < 27:
                        counts[code] = counts.get(code, 0) + 1
                    ev = rec.get('event', 'unknown')
                    by_event[ev] = by_event.get(ev, 0) + 1
                except Exception:
                    pass
    operator_codes = set(OPERATOR_DBC_CODE.values())
    seen_codes = set(counts.keys())
    return {
        "today_total_events": sum(counts.values()),
        "distinct_codes_seen": len(seen_codes),
        "operator_codes_in_log": len(seen_codes & operator_codes),
        "non_operator_codes_in_log": len(seen_codes - operator_codes),
        "uncovered_codes_today": sorted(set(range(27)) - seen_codes),
        "coverage_pct": round(100 * len(seen_codes) / 27, 1),
        "events_by_type": by_event,
        "code_counts": {int(k): v for k, v in counts.items()},
    }


# ── Mount ─────────────────────────────────────────────────────────────

def mount(engine, app, cortex) -> bool:
    """Register /bdc/events and /bdc/event_stats endpoints + attach to engine."""
    engine.bdc_event_stream = _EVENT_BUFFER

    from flask import jsonify
    @app.route('/bdc/events', methods=['GET'])
    def bdc_events_list():
        return jsonify({"recent": recent_events(32)})

    @app.route('/bdc/event_stats', methods=['GET'])
    def bdc_event_stats():
        return jsonify(stats())

    print(f"[CK] bdc_event_emitter: MOUNTED (17 event types -> 17 missing "
          f"DBC codes; /bdc/events, /bdc/event_stats)")
    return True


if __name__ == "__main__":
    print(f"BDC Event emitter")
    print(f"  Event types: {len(EVENT_TO_DBC_CODE)}")
    print(f"  DBC codes covered by events: {sorted(set(EVENT_TO_DBC_CODE.values()))}")
    print(f"  DBC codes covered by operators: {sorted(set(OPERATOR_DBC_CODE.values()))}")
    union = set(EVENT_TO_DBC_CODE.values()) | set(OPERATOR_DBC_CODE.values())
    print(f"  TOTAL coverage: {len(union)}/27 = {100*len(union)/27:.1f}%")
    print()
    print(f"  Today's stats: {json.dumps(stats(), indent=2)}")
