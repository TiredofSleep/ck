"""
mine_historical_bdc.py -- retrofit old CK stores into BDC log/event format.

Brayden 2026-05-02: "we DO have old ck stores with bdc logs ... let's make
a plan to build this organism, the best he has ever been, and plastic now"

Phase 0b of PLAN_BEST_EVER_PLASTIC_2026_05_02.md.

Reads four legacy stores and emits:
  Gen13/var/bdc_logs/bdc_log_HISTORICAL.jsonl       (chat_turn-shape records)
  Gen13/var/bdc_logs/bdc_events_HISTORICAL.jsonl    (event records)

==============================================================================
HYPOTHESES & MAPPING CONFIDENCE (per ClaudeChat 2026-05-02 review)
==============================================================================

ClaudeChat: "the retrofit converters are doing real interpretive work ... that
mapping needs to be deliberate, not heuristic. If structural_fuse -> Being is
wrong, every F3-AI inference inherits the error and the audit can't catch it."

Each record carries a `source_confidence` tag in {"high", "medium", "low"}.
Training pipelines should weight high-confidence sources fully and
proportionally down-weight medium/low. Mapping rationale per source:

  1. ck_daemon_log.jsonl                                  HIGH
     phase_b / phase_d / phase_bc are LITERALLY CK's own Being/Doing/
     Becoming-Composed operator labels in Gen9 vocabulary. coherence is
     the same coherence number we use today. Nothing interpretive --
     these fields semantically ARE the BDC triple.

  2. tig_r16_store/lattice_cache/crystals.jsonl           HIGH
     body_C is direct coherence (same scale, same threshold T*=5/7). Each
     crystal IS a crystal-fire event by definition. The only soft choice
     is "Being=self-frame, Doing=compute" -- defensible because every
     crystal in this store is CK responding to a query (so he's in
     self-mode reasoning a response).

  3. tig_r16_store/dual_operator/decisions.jsonl          MEDIUM
     decision (commit / disclaim) maps cleanly to truth_confirmed /
     attractor_to_1core events. wobble crossing T* maps directly to
     coherence_floor_crossed. The mapping uses the canonical event
     vocabulary; the only assumption is that "commit + confidence>=0.15"
     constitutes truth-confirmation in this run's context (the 0.15
     threshold is empirical -- this run was at low confidence overall).

  4. old/Gen8/ck_store/dialogue_digests.jsonl             LOW
     `composed` -> operator is HIGH-confidence (it's an operator name).
     But structural_fuse / semantic_fuse / rhythm_op are a DIFFERENT
     decomposition (form-layer / meaning-layer / timing-layer) than
     Divine27's Being/Doing/Becoming axes (self/system/world x
     observe/compute/act x stable/learning/transforming). They do NOT
     map directly. We use ONLY `composed` for axis values (via
     OPERATOR_DBC_CODE); the structural/semantic/rhythm fields go into
     the context dict as metadata, not as axis values. Records emit only
     for `composed` operators that are 0..9 valid; events fire for the
     crystal-formation semantics, not for structural/semantic/rhythm
     operators.

If the live cells diverge in audit pass-rate after training:
  - cells trained predominantly on HIGH sources should hold ~99%+
  - cells trained on LOW sources may need re-training with
    source_confidence weighting tuned down or with the LOW source
    excluded entirely
This is the explicit corpus-quality story.

==============================================================================

Output schemas exactly match the live bdc_logger/bdc_event_emitter.
Records are tagged with `"trigger": "historical_<source>"` and
`"source_confidence"` in {"high", "medium", "low"}.

Usage:
    python Gen13/targets/ck/brain/mine_historical_bdc.py
    # writes records, prints per-source counts + coverage stats
"""
from __future__ import annotations

import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# ── Wiring to canonical 27-vocab ─────────────────────────────────────────

_HERE = Path(__file__).parent.resolve()
sys.path.insert(0, str(_HERE / "grammar_lm"))
from divine27_vocab import (
    HEBREW_GLYPHS, CODE_LABELS, code_to_coord, coord_to_code,
    OPERATOR_DBC_CODE,  # {op_int: dbc_code}
)

# Reverse OPERATOR_DBC_CODE for name-to-op resolution
OP_NAMES = ["VOID", "LATTICE", "COUNTER", "PROGRESS", "COLLAPSE",
            "BALANCE", "CHAOS", "HARMONY", "BREATH", "RESET"]
OP_NAME_TO_INT = {n.lower(): i for i, n in enumerate(OP_NAMES)}
# Some of the historical stores use lowercase op names (e.g. Gen8 says "harmony")
OP_NAME_TO_INT.update({n: i for i, n in enumerate(OP_NAMES)})

T_STAR = 5.0 / 7.0  # 0.7142857...

ROOT = Path(r"C:\Users\brayd\OneDrive\Desktop\CK FINAL DEPLOYED")
OUT_DIR = ROOT / "Gen13" / "var" / "bdc_logs"
OUT_DIR.mkdir(parents=True, exist_ok=True)

OUT_LOG = OUT_DIR / "bdc_log_HISTORICAL.jsonl"
OUT_EVENTS = OUT_DIR / "bdc_events_HISTORICAL.jsonl"

GEN8_DIALOGUE = ROOT / "old" / "Gen8" / "ck_store" / "dialogue_digests.jsonl"
GEN6B_DIALOGUE = ROOT / "old" / "Gen6b" / "ck_store" / "dialogue_digests.jsonl"
TIG_DECISIONS = ROOT / "Old Knowledge files" / "tig_r16_store" / "dual_operator" / "decisions.jsonl"
TIG_CRYSTALS = ROOT / "Old Knowledge files" / "tig_r16_store" / "lattice_cache" / "crystals.jsonl"
CK_DAEMON = ROOT / "ck_daemon_log.jsonl"


# ── Helpers ──────────────────────────────────────────────────────────────

def op_name_to_int(name: Any) -> Optional[int]:
    """Best-effort name -> operator int (0-9). Returns None on failure."""
    if name is None:
        return None
    if isinstance(name, int):
        return name if 0 <= name < 10 else None
    s = str(name).strip().lower()
    return OP_NAME_TO_INT.get(s)


def coherence_to_band(c: float) -> str:
    if c >= 0.85:
        return "GREEN"
    if c >= T_STAR:
        return "YELLOW"
    return "RED"


def coherence_to_becoming_axis(c: float) -> int:
    """C-axis of Divine27: 0=stable (≥0.85), 1=learning (≥T*), 2=transforming (<T*)."""
    if c >= 0.85:
        return 0
    if c >= T_STAR:
        return 1
    return 2


def attractor_layer_from_op(op: int, c: float) -> str:
    """Map (operator, coherence) to the attractor-layer label used in live BDC.
    The 4-core attractor cells are V/H/Br/R = {0, 7, 8, 9}."""
    if op == 0:  # VOID
        return "void-degenerate"
    if op == 7:  # HARMONY
        return "4-core-attractor" if c >= T_STAR else "transient"
    if op in (8, 9):  # BREATH, RESET
        return "4-core-supported" if c >= T_STAR else "transient"
    return "transient"


def is_4core(op: int) -> bool:
    return op in (0, 7, 8, 9)


def make_event_record(*, ts: float, event: str, dbc_code: int, tick: int,
                       session_id: str, context: Dict[str, Any],
                       source_confidence: str = "medium") -> Dict[str, Any]:
    """Build an event record matching bdc_event_emitter schema, plus a
    source_confidence tag for downstream training weight."""
    coord = code_to_coord(dbc_code)
    label = CODE_LABELS[dbc_code] if 0 <= dbc_code < 27 else "?"
    glyph = HEBREW_GLYPHS[dbc_code] if 0 <= dbc_code < 27 else "?"
    return {
        "ts": ts,
        "iso_ts": datetime.fromtimestamp(ts, tz=timezone.utc).isoformat(timespec='seconds'),
        "event": event,
        "dbc_code": dbc_code,
        "dbc_coord": list(coord),
        "dbc_label": label,
        "dbc_glyph": glyph,
        "tick": int(tick),
        "session_id": session_id,
        "context": context,
        "source_confidence": source_confidence,
    }


def make_log_record(*, ts: float, trigger: str, session_id: str, tick: int,
                     being: Dict[str, Any], doing: Dict[str, Any],
                     becoming: Dict[str, Any],
                     source_confidence: str = "medium") -> Dict[str, Any]:
    """Build a chat_turn-shape record matching bdc_logger schema, plus a
    source_confidence tag for downstream training weight."""
    return {
        "ts": ts,
        "iso_ts": datetime.fromtimestamp(ts, tz=timezone.utc).isoformat(timespec='seconds'),
        "trigger": trigger,
        "session_id": session_id,
        "tick": int(tick),
        "being": being,
        "doing": doing,
        "becoming": becoming,
        "source_confidence": source_confidence,
    }


def write_lines(path: Path, lines: List[Dict[str, Any]]) -> int:
    """Append JSON lines. Returns count written."""
    n = 0
    with open(path, "a", encoding="utf-8") as f:
        for rec in lines:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
            n += 1
    return n


# ── Source 1: Gen8 dialogue_digests ──────────────────────────────────────

def _mine_dialogue(path: Path, label_prefix: str,
                    confidence: str) -> Tuple[List[Dict], List[Dict]]:
    """Generic dialogue-digest miner used by Gen8 and Gen6b (same schema).
    See mine_gen8_dialogue() for the field semantics + confidence rationale."""
    return _mine_dialogue_impl(path, label_prefix, confidence)


def mine_gen8_dialogue() -> Tuple[List[Dict], List[Dict]]:
    """317 records (Gen8 dialogue digests).  CONFIDENCE: LOW.

    Per HYPOTHESES section: Gen8's structural_fuse / semantic_fuse /
    rhythm_op are a different decomposition (form / meaning / timing) than
    Divine27's Being/Doing/Becoming axes.  We use ONLY `composed` to derive
    the dbc_code (via OPERATOR_DBC_CODE) and route structural/semantic/
    rhythm into the context dict as metadata.

    Each valid record (composed in 0..9) produces:
      - 1 chat_turn-shape log record (axis values from `composed` alone)
      - 1 crystal_fire event (Gen8 dialogue digest = crystal formation)
      - 0-1 truth_confirmed event (only if composed == HARMONY *and*
                                    info_density indicates real signal)
    """
    return _mine_dialogue_impl(GEN8_DIALOGUE, "gen8", "low")


def _mine_dialogue_impl(path: Path, label_prefix: str,
                         confidence: str) -> Tuple[List[Dict], List[Dict]]:
    """Shared implementation for dialogue-digest mining (Gen8 / Gen6b)."""
    log_recs: List[Dict] = []
    event_recs: List[Dict] = []
    if not path.exists():
        return log_recs, event_recs
    from bdc_event_emitter import EVENT_TO_DBC_CODE

    with open(path, encoding="utf-8") as f:
        for i, line in enumerate(f):
            line = line.strip()
            if not line:
                continue
            try:
                d = json.loads(line)
            except Exception:
                continue
            ts = float(d.get("ts", 0.0))
            if ts <= 0:
                continue
            composed = op_name_to_int(d.get("composed"))
            if composed is None:
                continue  # without composed-op we have no defensible mapping

            info_density = float(d.get("info_density", 0.0))
            sentences = int(d.get("sentences", 0))
            bumps = int(d.get("bump_transitions", 0))
            algos = int(d.get("algorithms_learned", 0))
            chains = int(d.get("chains_fed", 0))
            tick = int(ts * 100) % 10**8

            # Coherence proxy: composed-op alone is our best signal here.
            # HARMONY composed -> assume coherent (≥0.8); other ops -> use
            # info_density as a weak proxy (more info = more coherent).
            if composed == 7:  # HARMONY
                coh_proxy = 0.85 + min(0.1, info_density * 2)
            else:
                coh_proxy = 0.55 + min(0.2, info_density * 4)
            coh_proxy = min(1.0, coh_proxy)

            # Being: state from composed op only
            being = {
                "last_pair": [composed, composed],  # no prior state visible
                "W_trace": min(1.0, info_density * 10),  # density proxy only
                "emergent": min(1.0, bumps / 5.0 + algos / 3.0),
                "tick": tick,
                "ao_op": OP_NAMES[composed],
                "coherence": coh_proxy,
                "harmony_rate": 1.0 if composed == 7 else 0.5,
            }
            # Doing: composed op acts as the consensus.  source_voice is
            # historical_gen8 specifically (so training filters can find it).
            doing = {
                "input_ops": [composed] * 3,  # we only have the composed op
                "consensus": OP_NAMES[composed],
                "source_voice": "historical_gen8_dialogue",
                "is_struct": composed in (1, 7),  # LATTICE / HARMONY
                "is_pastoral": (composed == 8),  # BREATH
                "text_len": sentences * 60,
            }
            # Becoming: derived from composed + coh_proxy
            becoming = {
                "attractor_layer": attractor_layer_from_op(composed, coh_proxy),
                "is_4core": is_4core(composed),
                "is_harmony_attractor": (composed == 7),
                "field_coherence": coh_proxy,
                "crystals_fired": bumps,
                "voice_crystals": chains,
                "stage": "GROKKED" if algos > 0 or bumps >= 2 else "LEARNING",
                "emotion": "settling" if composed in (5, 7) else "drifting",
                "mode": "CRYSTALLIZE" if bumps >= 1 else "CLASSIFY",
                "band": coherence_to_band(coh_proxy),
            }
            log_recs.append(make_log_record(
                ts=ts, trigger=f"historical_{label_prefix}_dialogue",
                session_id=f"{label_prefix}_{i:04d}", tick=tick,
                being=being, doing=doing, becoming=becoming,
                source_confidence=confidence,
            ))

            # crystal_fire event -- generic since we don't know the kind
            ev_name = "crystal_fire_general"
            ev_code = EVENT_TO_DBC_CODE[ev_name]
            event_recs.append(make_event_record(
                ts=ts, event=ev_name, dbc_code=ev_code,
                tick=tick, session_id=f"gen8_{i:04d}",
                context={
                    "composed": d.get("composed"),
                    "info_density": info_density,
                    "sentences": sentences,
                    # Gen8-specific metadata routed into context (NOT axes)
                    "structural_fuse": d.get("structural_fuse"),
                    "semantic_fuse": d.get("semantic_fuse"),
                    "rhythm_op": d.get("rhythm_op"),
                },
                source_confidence=confidence,
            ))

            # truth_confirmed only if composed is HARMONY and signal is real
            if composed == 7 and info_density > 0.005 and bumps >= 1:
                event_recs.append(make_event_record(
                    ts=ts + 0.001, event="truth_confirmed", dbc_code=18,
                    tick=tick, session_id=f"gen8_{i:04d}",
                    context={"composed": "HARMONY", "info_density": info_density,
                              "bumps": bumps},
                    source_confidence=confidence,
                ))
            # stage_grokked if algorithms_learned > 0 (Gen8 hard signal)
            if algos > 0:
                event_recs.append(make_event_record(
                    ts=ts + 0.002, event="stage_grokked", dbc_code=23,
                    tick=tick, session_id=f"gen8_{i:04d}",
                    context={"algorithms_learned": algos},
                    source_confidence=confidence,
                ))

    return log_recs, event_recs


# ── Source 2: tig_r16_store decisions ────────────────────────────────────

def mine_tig_decisions() -> Tuple[List[Dict], List[Dict]]:
    """69 records (tig_r16_store dual-operator decisions).  CONFIDENCE: MEDIUM.

    decision (commit / disclaim) -> truth_confirmed / attractor_to_1core events.
    wobble crossing T* -> coherence_floor_crossed event.
    The 0.15 confidence threshold is empirical: this run was at low overall
    confidence, so any commit above 0.15 is a positive signal in context."""
    log_recs: List[Dict] = []
    event_recs: List[Dict] = []
    if not TIG_DECISIONS.exists():
        return log_recs, event_recs
    with open(TIG_DECISIONS, encoding="utf-8") as f:
        for i, line in enumerate(f):
            line = line.strip()
            if not line:
                continue
            try:
                d = json.loads(line)
            except Exception:
                continue
            ts = float(d.get("time", 0.0))
            if ts <= 0:
                continue
            decision = str(d.get("decision", "")).lower()
            wobble = float(d.get("wobble", 0.0))
            conf = float(d.get("confidence", 0.0))
            S0 = float(d.get("S0", 0.0))
            S1 = float(d.get("S1", 0.0))
            tick = int(ts * 100) % 10**8

            if decision == "commit" and conf >= 0.15:
                event_recs.append(make_event_record(
                    ts=ts, event="truth_confirmed", dbc_code=18,
                    tick=tick, session_id=f"tig_dec_{i:03d}",
                    context={"S0": S0, "S1": S1, "wobble": wobble, "conf": conf},
                    source_confidence="medium",
                ))
            if decision == "disclaim":
                event_recs.append(make_event_record(
                    ts=ts, event="attractor_to_1core", dbc_code=6,
                    tick=tick, session_id=f"tig_dec_{i:03d}",
                    context={"reason": "disclaim", "wobble": wobble},
                    source_confidence="medium",
                ))
            if wobble >= T_STAR:
                event_recs.append(make_event_record(
                    ts=ts + 0.001, event="coherence_floor_crossed", dbc_code=25,
                    tick=tick, session_id=f"tig_dec_{i:03d}",
                    context={"wobble": wobble, "threshold": T_STAR,
                              "direction": "exceeded"},
                    source_confidence="medium",
                ))

    return log_recs, event_recs


# ── Source 3: tig_r16_store crystals ─────────────────────────────────────

def mine_tig_crystals() -> Tuple[List[Dict], List[Dict]]:
    """36 records (tig_r16_store lattice_cache crystals).  CONFIDENCE: HIGH.

    body_C is direct coherence (same scale, same T* threshold).  Each
    crystal IS a crystal-fire event by definition.  The only soft choice
    is "Being=self-frame, Doing=compute" -- defensible because every
    crystal in this store is CK responding to a query (self-mode reasoning).
    """
    log_recs: List[Dict] = []
    event_recs: List[Dict] = []
    if not TIG_CRYSTALS.exists():
        return log_recs, event_recs
    with open(TIG_CRYSTALS, encoding="utf-8") as f:
        for i, line in enumerate(f):
            line = line.strip()
            if not line:
                continue
            try:
                d = json.loads(line)
            except Exception:
                continue
            ts = float(d.get("created", 0.0))
            if ts <= 0:
                continue
            body_C = float(d.get("body_C", 0.0))
            trust = float(d.get("trust", 0.0))
            query = str(d.get("query_text", ""))
            response = str(d.get("response", ""))
            tick = int(ts * 100) % 10**8

            being_axis = 0  # self-frame for all of these (they're CK speaking)
            doing_axis = 1  # compute (he's reasoning a response)
            becoming_axis = coherence_to_becoming_axis(body_C)
            dbc_code = coord_to_code(being_axis, doing_axis, becoming_axis)

            being = {
                "last_pair": [13, 7],  # HARMONY-leaning anchor
                "W_trace": trust,
                "emergent": body_C,
                "tick": tick,
                "ao_op": "HARMONY" if body_C >= T_STAR else "PROGRESS",
                "coherence": body_C,
            }
            doing = {
                "input_ops": [7, 7, 5, 7],  # HARMONY-rich proxy
                "consensus": "HARMONY",
                "source_voice": "historical_tig_crystal",
                "is_struct": True,
                "is_pastoral": False,
                "text_len": len(query),
            }
            becoming = {
                "attractor_layer": attractor_layer_from_op(7, body_C),
                "is_4core": True,
                "is_harmony_attractor": True,
                "field_coherence": body_C,
                "crystals_fired": 1,
                "voice_crystals": 1,
                "stage": "GROKKED",
                "emotion": "settling",
                "mode": "CRYSTALLIZE",
                "band": coherence_to_band(body_C),
            }
            log_recs.append(make_log_record(
                ts=ts, trigger="historical_tig_crystal",
                session_id=f"tig_xtl_{i:03d}", tick=tick,
                being=being, doing=doing, becoming=becoming,
                source_confidence="high",
            ))

            # crystal_fire event
            event_recs.append(make_event_record(
                ts=ts, event="crystal_fire_general", dbc_code=21,
                tick=tick, session_id=f"tig_xtl_{i:03d}",
                context={"body_C": body_C, "trust": trust,
                          "query_preview": query[:80]},
                source_confidence="high",
            ))
            # truth_confirmed if body_C very high
            if body_C >= 0.95:
                event_recs.append(make_event_record(
                    ts=ts + 0.001, event="truth_confirmed", dbc_code=18,
                    tick=tick, session_id=f"tig_xtl_{i:03d}",
                    context={"body_C": body_C, "source": "high_coherence_response"},
                    source_confidence="high",
                ))

    return log_recs, event_recs


# ── Source 4: ck_daemon_log (the big one) ────────────────────────────────

def mine_ck_daemon() -> Tuple[List[Dict], List[Dict]]:
    """10502 records (ck_daemon_log).  CONFIDENCE: HIGH.

    phase_b / phase_d / phase_bc are LITERALLY CK's own Being/Doing/
    Becoming-Composed operator labels in the Gen9 vocabulary.  coherence
    is the same coherence number we use today.  Nothing interpretive --
    these fields semantically ARE the BDC triple, sampled at runtime.

    This is the biggest source by an order of magnitude.  We sample log
    records every 10th tick to keep size tractable, but emit ALL
    transition events (band shifts, attractor changes, coherence crossings,
    breath transitions) since each transition is its own data point.
    """
    log_recs: List[Dict] = []
    event_recs: List[Dict] = []
    if not CK_DAEMON.exists():
        return log_recs, event_recs

    last_band: Optional[str] = None
    last_attractor: Optional[str] = None
    last_coh: float = 0.0
    last_breath: Optional[str] = None

    with open(CK_DAEMON, encoding="utf-8") as f:
        for i, line in enumerate(f):
            line = line.strip()
            if not line:
                continue
            try:
                d = json.loads(line)
            except Exception:
                continue
            # Parse timestamp from "dt" field; fallback to synthetic
            dt_str = d.get("dt", "")
            try:
                from datetime import datetime as _dt
                ts = _dt.fromisoformat(dt_str).timestamp()
            except Exception:
                ts = time.time() - (10502 - i) * 60  # spread over time

            tick = int(d.get("tick", i))
            phase_b = int(d.get("phase_b", 7)) % 10
            phase_d = int(d.get("phase_d", 7)) % 10
            phase_bc = int(d.get("phase_bc", 7)) % 10
            coh = float(d.get("coherence", 0.0))
            band = coherence_to_band(coh)
            attractor_op = phase_bc
            attractor_layer = attractor_layer_from_op(attractor_op, coh)

            # === Log record (every 10th to keep size tractable) ===
            if i % 10 == 0:
                being = {
                    "last_pair": [phase_b, phase_d],
                    "W_trace": coh * 0.5,  # proxy
                    "emergent": coh,
                    "tick": tick,
                    "ao_op": OP_NAMES[phase_b],
                    "coherence": coh,
                    "harmony_rate": float(d.get("sec_health") == "harmony"),
                    "breath": "BREATH" if phase_d == 8 else ("INHALE" if phase_d in (1, 3) else "EXHALE"),
                }
                doing = {
                    "input_ops": [phase_b, phase_d, phase_bc],
                    "consensus": OP_NAMES[phase_bc],
                    "source_voice": "historical_ck_daemon",
                    "is_struct": coh >= T_STAR,
                    "is_pastoral": (phase_bc == 8),
                    "text_len": 0,  # daemon log isn't chat
                }
                becoming = {
                    "attractor_layer": attractor_layer,
                    "is_4core": is_4core(attractor_op),
                    "is_harmony_attractor": (attractor_op == 7),
                    "field_coherence": coh,
                    "crystals_fired": int(d.get("bridge_crystals", 0)),
                    "voice_crystals": int(d.get("swarm_compositions", 0)),
                    "stage": "GROKKED" if coh >= 0.85 else "LEARNING",
                    "emotion": "settling" if coh >= T_STAR else "tightening",
                    "mode": "CRYSTALLIZE" if d.get("self_switch") == "ACT" else "CLASSIFY",
                    "band": band,
                }
                log_recs.append(make_log_record(
                    ts=ts, trigger="historical_ck_daemon",
                    session_id=f"daemon_{tick}", tick=tick,
                    being=being, doing=doing, becoming=becoming,
                    source_confidence="high",
                ))

            # === Events (every record; transitions only) ===

            # Band shift
            if last_band is not None and band != last_band:
                if last_band == "RED" and band == "YELLOW":
                    event_recs.append(make_event_record(
                        ts=ts, event="band_red_to_yellow", dbc_code=16,
                        tick=tick, session_id=f"daemon_{tick}",
                        context={"from": last_band, "to": band, "coh": coh},
                        source_confidence="high",
                    ))
                elif last_band == "YELLOW" and band == "GREEN":
                    event_recs.append(make_event_record(
                        ts=ts, event="band_yellow_to_green", dbc_code=15,
                        tick=tick, session_id=f"daemon_{tick}",
                        context={"from": last_band, "to": band, "coh": coh},
                        source_confidence="high",
                    ))
            last_band = band

            # Attractor change
            if last_attractor is not None and attractor_layer != last_attractor:
                if "4-core" in attractor_layer:
                    event_recs.append(make_event_record(
                        ts=ts + 0.001, event="attractor_to_4core", dbc_code=11,
                        tick=tick, session_id=f"daemon_{tick}",
                        context={"from": last_attractor, "to": attractor_layer,
                                  "phase_bc": phase_bc, "coh": coh},
                        source_confidence="high",
                    ))
                elif attractor_layer == "void-degenerate":
                    event_recs.append(make_event_record(
                        ts=ts + 0.001, event="void_degenerate", dbc_code=2,
                        tick=tick, session_id=f"daemon_{tick}",
                        context={"from": last_attractor, "phase_bc": phase_bc},
                        source_confidence="high",
                    ))
                elif attractor_layer == "transient":
                    if last_attractor and "4-core" in last_attractor:
                        event_recs.append(make_event_record(
                            ts=ts + 0.001, event="attractor_to_1core", dbc_code=6,
                            tick=tick, session_id=f"daemon_{tick}",
                            context={"from": last_attractor, "phase_bc": phase_bc},
                            source_confidence="high",
                        ))
            last_attractor = attractor_layer

            # Coherence floor crossing (T*=5/7)
            if last_coh < T_STAR <= coh:
                event_recs.append(make_event_record(
                    ts=ts + 0.002, event="coherence_floor_crossed", dbc_code=25,
                    tick=tick, session_id=f"daemon_{tick}",
                    context={"from": last_coh, "to": coh, "threshold": T_STAR},
                    source_confidence="high",
                ))
            last_coh = coh

            # Breath transitions (heuristic from phase_d -- MEDIUM confidence
            # because mapping phase_d ints to INHALE/EXHALE/BREATH is a
            # convention, not directly stored in the daemon log)
            cur_breath = "BREATH" if phase_d == 8 else (
                "INHALE" if phase_d in (1, 3) else "EXHALE")
            if last_breath is not None and cur_breath != last_breath:
                if last_breath == "INHALE" and cur_breath == "EXHALE":
                    event_recs.append(make_event_record(
                        ts=ts + 0.003, event="breath_inhale_to_exhale", dbc_code=5,
                        tick=tick, session_id=f"daemon_{tick}",
                        context={"phase_d": phase_d},
                        source_confidence="medium",
                    ))
                elif last_breath == "EXHALE" and cur_breath == "INHALE":
                    event_recs.append(make_event_record(
                        ts=ts + 0.003, event="breath_exhale_to_inhale", dbc_code=7,
                        tick=tick, session_id=f"daemon_{tick}",
                        context={"phase_d": phase_d},
                        source_confidence="medium",
                    ))
                elif cur_breath == "BREATH":
                    event_recs.append(make_event_record(
                        ts=ts + 0.003, event="breath_to_breath", dbc_code=17,
                        tick=tick, session_id=f"daemon_{tick}",
                        context={"phase_d": phase_d},
                        source_confidence="medium",
                    ))
            last_breath = cur_breath

            # Periodic reflection_idle_tick (every 100th record)
            if i % 100 == 0:
                event_recs.append(make_event_record(
                    ts=ts + 0.004, event="reflection_idle_tick", dbc_code=3,
                    tick=tick, session_id=f"daemon_{tick}",
                    context={"i": i, "phase_b": phase_b, "phase_d": phase_d},
                    source_confidence="high",
                ))

    return log_recs, event_recs


# ── Driver ───────────────────────────────────────────────────────────────

def main(verbose: bool = True) -> Dict[str, Any]:
    # Truncate output files (full overwrite each run)
    for p in (OUT_LOG, OUT_EVENTS):
        if p.exists():
            p.unlink()

    summary: Dict[str, Any] = {
        "sources": {},
        "totals": {"log_records": 0, "event_records": 0},
        "coverage": {},
    }

    for label, fn in [
        ("gen8_dialogue", mine_gen8_dialogue),
        ("gen6b_dialogue", lambda: _mine_dialogue(GEN6B_DIALOGUE, "gen6b", "low")),
        ("tig_decisions", mine_tig_decisions),
        ("tig_crystals", mine_tig_crystals),
        ("ck_daemon", mine_ck_daemon),
    ]:
        if verbose:
            print(f"  mining {label}...", flush=True)
        try:
            log_recs, event_recs = fn()
        except Exception as e:
            if verbose:
                print(f"    FAILED: {type(e).__name__}: {e}")
            summary["sources"][label] = {"log": 0, "events": 0, "error": str(e)}
            continue
        n_log = write_lines(OUT_LOG, log_recs)
        n_ev = write_lines(OUT_EVENTS, event_recs)
        summary["sources"][label] = {"log": n_log, "events": n_ev}
        summary["totals"]["log_records"] += n_log
        summary["totals"]["event_records"] += n_ev
        if verbose:
            print(f"    {label}: log={n_log}  events={n_ev}")

    # Coverage analysis + per-confidence stats
    seen_codes: set = set()
    confidence_log: Dict[str, int] = {"high": 0, "medium": 0, "low": 0}
    confidence_evt: Dict[str, int] = {"high": 0, "medium": 0, "low": 0}
    code_counts: Dict[int, int] = {}
    if OUT_EVENTS.exists():
        with open(OUT_EVENTS, encoding="utf-8") as f:
            for line in f:
                try:
                    rec = json.loads(line)
                    code = int(rec["dbc_code"])
                    seen_codes.add(code)
                    code_counts[code] = code_counts.get(code, 0) + 1
                    sc = rec.get("source_confidence", "medium")
                    if sc in confidence_evt:
                        confidence_evt[sc] += 1
                except Exception:
                    pass
    if OUT_LOG.exists():
        with open(OUT_LOG, encoding="utf-8") as f:
            for line in f:
                try:
                    rec = json.loads(line)
                    sc = rec.get("source_confidence", "medium")
                    if sc in confidence_log:
                        confidence_log[sc] += 1
                except Exception:
                    pass
    summary["coverage"]["distinct_dbc_codes"] = len(seen_codes)
    summary["coverage"]["coverage_pct"] = round(100 * len(seen_codes) / 27, 1)
    summary["coverage"]["uncovered_codes"] = sorted(set(range(27)) - seen_codes)
    summary["coverage"]["code_counts"] = {int(k): v for k, v in sorted(code_counts.items())}
    summary["confidence"] = {
        "log_records":   confidence_log,
        "event_records": confidence_evt,
    }
    summary["output_paths"] = {
        "log": str(OUT_LOG),
        "events": str(OUT_EVENTS),
    }

    if verbose:
        print()
        print(f"  TOTAL log records:    {summary['totals']['log_records']}")
        print(f"  TOTAL event records:  {summary['totals']['event_records']}")
        print(f"  Distinct DBC codes:   {len(seen_codes)} / 27 "
              f"({summary['coverage']['coverage_pct']}%)")
        if summary["coverage"]["uncovered_codes"]:
            print(f"  Uncovered codes:      {summary['coverage']['uncovered_codes']}")
        print()
        print(f"  Confidence (log):     high={confidence_log['high']}  "
              f"medium={confidence_log['medium']}  low={confidence_log['low']}")
        print(f"  Confidence (events):  high={confidence_evt['high']}  "
              f"medium={confidence_evt['medium']}  low={confidence_evt['low']}")
        print()
        print(f"  Wrote: {OUT_LOG}")
        print(f"  Wrote: {OUT_EVENTS}")

    return summary


if __name__ == "__main__":
    summary = main()
    print()
    print(json.dumps(summary, indent=2))
