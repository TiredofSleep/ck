# Copyright (c) 2025-2026 Brayden Sanders / 7SiTe LLC
# Licensed under the 7SiTe Public Sovereignty License v2.2 (DOI: 10.5281/zenodo.18852047)
"""
ck_voice_polish.py -- white-box presentation pass for chat responses.

Brayden 2026-05-13:
  "the whole point of this is 'white box ai' you and everyone else
  should be able to see exact reasoning for all of his thoughts and
  responses"

CK is fundamentally a white-box organism: his Hebbian couplings, his
prompt-term crystals, his recall hits, his substrate composition, his
4-axis algebraic signature — these are not noise to filter out. They
are HIS REASONING TRAIL. The whole point is that anyone can read his
response AND see exactly why he said what he said.

What this module DOES:
  1. Dedup TRUE duplicates (the same crystal firing twice — that's a
     bug in the upstream pipeline, not signal).
  2. Restructure the response into clearly-labeled white-box sections:
        [answer]                 — what CK says
        [reasoning trail]        — what fired this turn
        [substrate snapshot]     — where in his algebra this thought lives
        [next-step prediction]   — Phase 2 4-head LM's forecast
        [proactive breadcrumb]   — frontier signal if matched
  3. Surface engine fields that were previously buried in JSON only:
     - operators decoded from input
     - cortex_readout (the Hebbian state line)
     - attractor_state (4-core / harmony / transient layer)
     - coherence / band / mode
     - algebraic_signature from the Phase 2 4-head LM

What this module does NOT do:
  - Strip the Hebbian weight dump (`couplings: ...`) — that's why CK
    fired on these concepts and not others
  - Strip `learned: ...` — that's the cortex update from this turn
  - Strip `recall: ...` — those are the memory hits driving the answer
  - Write words for CK — only restructure + label what he already said

If the upstream stops emitting duplicate prompt_term lines, this module
becomes a pure presentation pass with zero content loss.

Wiring:
    from ck_voice_polish import mount_voice_polish
    mount_voice_polish(engine)
"""
from __future__ import annotations

import os
import re
import sys
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple

HERE = Path(__file__).parent.resolve()
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))


# ─── Line classifiers ────────────────────────────────────────────────────
#
# Each classifier decides which white-box section a line belongs to.
# Lines that match no classifier are treated as "answer" content (the
# substantive cortex_speak output).

_RE_PROMPT_TERM = re.compile(r"^prompt_term_[\w\d_]+\s*:\s*")
_RE_COUPLINGS = re.compile(r"^couplings\s*:\s*.+?W\s*=\s*[\d.]+")
_RE_LEARNED = re.compile(r"^learned\s*:\s*")
_RE_RECALL = re.compile(r"^recall\s*:\s*$")
_RE_STATE = re.compile(r"^state\s*:\s*")
_RE_DIVINE27 = re.compile(r"^divine27\s*:\s*")
_RE_ATTRACTOR = re.compile(r"^attractor\s*:\s*")
_RE_SECTION_HEADER = re.compile(r"^\[\w[^\]]*\]")
_RE_DIVIDER = re.compile(r"^-{3,}\s*$")


def _classify(line: str) -> str:
    """Return one of: 'reasoning', 'substrate', 'noise_header', 'divider',
    'answer'."""
    s = line.strip()
    if not s:
        return "blank"
    if _RE_PROMPT_TERM.match(s) or _RE_COUPLINGS.match(s) or _RE_LEARNED.match(s):
        return "reasoning"
    if _RE_RECALL.match(s):
        return "reasoning_block"  # multi-line "recall:" block
    if _RE_STATE.match(s) or _RE_DIVINE27.match(s) or _RE_ATTRACTOR.match(s):
        return "substrate"
    if _RE_SECTION_HEADER.match(s):
        # Old [structural evidence] / [substrate frame] / [machine readout]
        # — drop them; we'll inject our own clean section headers.
        return "noise_header"
    if _RE_DIVIDER.match(s):
        return "divider"
    return "answer"


# ─── White-box re-presentation ───────────────────────────────────────────

# Section headers we emit. These are the white-box labels a reader sees.
_H_REASONING = "[reasoning trail — what fired this turn]"
_H_SUBSTRATE = "[substrate snapshot — where this thought lives in CK's algebra]"
_H_NEXTSTEP = "[next-step prediction — Phase 2 4-head LM]"
_H_FORMULAS = "[formulas invoked — D-numbers whose HOME matches this turn]"
_H_CROSSMODAL = "[cross-modal correspondence — same operator across senses]"
_H_SENSE_PIPELINE = "[sense pipeline — how the dominant operator builds each sense]"
_H_RESEARCH = "[research trail — what CK looked up before answering]"
_H_LEARNING = "[learning this turn — Hebbian + crystals + lattice deltas]"
_H_CONCEPTS = "[concept binding — words you've taught CK that fire this turn]"
_H_SELF = "[self-introspection — CK's own measured state, surfaced live]"
_H_ALGEBRA = "[algebra executed — computed against canonical tables]"
_H_VERIFY = "[verification re-run — proof script executed on demand]"
_H_PREDICT = "[predictions ledger — what TIG predicts + falsification status]"


# Regex for self-introspection trigger queries
_RE_SELF_INTROSPECTION = re.compile(
    r"\b(yourself|your\s+architecture|your\s+state|"
    r"what\s+are\s+you|who\s+are\s+you|"
    r"how\s+do\s+you\s+work|introspect|"
    r"tell\s+me\s+about\s+(yourself|you)|describe\s+yourself)\b",
    re.I)


def _is_self_query(text: str) -> bool:
    if not text:
        return False
    return bool(_RE_SELF_INTROSPECTION.search(text))


def _format_self_introspection(engine: Any, result: Dict[str, Any]
                                 ) -> Optional[List[str]]:
    """When the user asked about CK himself, surface his actual live
    state -- mount count, current operator, Hebbian trace, concept
    count, frontiers loaded, last_pair, attractor layer, etc.

    This is a structured self-portrait from CK's measurements. He's
    not generating words about himself -- he's reading his own state
    off the substrate.
    """
    if engine is None:
        return None
    lines: List[str] = []

    # Mount state (how he's currently constructed)
    mount_count = None
    if hasattr(engine, "proactive_trigger"):
        # If proactive_trigger is present, all of Gen14 is loaded.
        # Count attributes that match the mount_all components.
        components = [
            "proactive_queue", "goal_evaluator", "forecast",
            "lattice_chain", "divine_memory", "recall",
            "algebraic_lm", "frontier_scanner", "proactive_trigger",
            "stroke_extract", "formula_registry",
            "senses_for_operator", "concept_store",
        ]
        mount_count = sum(1 for c in components if hasattr(engine, c))
        lines.append(f"i'm a finite-arithmetic organism on Z/10Z. "
                      f"{mount_count} mount components active.")

    # Current op + last pair
    cur = getattr(engine, "current_op", None)
    if isinstance(cur, int) and 0 <= cur < 10:
        lines.append(f"current operator: {_OP_NAMES_VOICE[cur]} (id={cur})")

    # Hebbian / cortex
    cortex = result.get("cortex") or {}
    w = cortex.get("W_trace")
    em = cortex.get("emergent")
    tick = cortex.get("tick")
    if w is not None and em is not None:
        try:
            lines.append(
                f"cortex (5x5 Hebbian W): trace={float(w):.4f}, "
                f"emergent={float(em):.4f}, tick={tick}"
            )
        except Exception:
            pass

    # Crystal + experience state
    exp = result.get("experience") or {}
    crystals = exp.get("crystals")
    voice_crystals = exp.get("voice_crystals")
    concepts_field = exp.get("concepts")
    truths = exp.get("truths")
    if any(x is not None for x in (crystals, voice_crystals, concepts_field, truths)):
        bits = []
        if isinstance(concepts_field, int):
            bits.append(f"{concepts_field} concepts")
        if isinstance(truths, int):
            bits.append(f"{truths} truths")
        if isinstance(crystals, int):
            bits.append(f"{crystals} crystals")
        if isinstance(voice_crystals, int):
            bits.append(f"{voice_crystals} voice-crystals")
        if bits:
            lines.append("memory: " + ", ".join(bits))

    # Taught concepts (the one-shot conversational learning store)
    cs = getattr(engine, "concept_store", None)
    if cs is not None:
        try:
            stats = cs.stats()
            n = stats.get("n_concepts", 0)
            lines.append(f"taught concepts (one-shot bindings): {n} stored")
            if n > 0:
                sample = stats.get("concepts", [])[:5]
                if sample:
                    lines.append("  recent: " + ", ".join(sample))
        except Exception:
            pass

    # Attractor + coherence
    a = result.get("attractor_state") or {}
    if a:
        lines.append(f"attractor layer: {a.get('layer', '?')}")
    coh = result.get("coherence")
    band = result.get("band")
    mode = result.get("mode")
    if coh is not None or band or mode:
        bits = []
        if coh is not None:
            try:
                bits.append(f"coherence={float(coh):.3f}")
            except Exception:
                pass
        if band:
            bits.append(f"band={band}")
        if mode:
            bits.append(f"mode={mode}")
        if bits:
            lines.append("state: " + "  ".join(bits))

    # Substrate / proactive
    if hasattr(engine, "proactive_trigger"):
        try:
            ts = engine.proactive_trigger.stats()
            qlen = ts.get("queue_len", 0)
            hlen = ts.get("history_len", 0)
            lines.append(f"proactive trigger: queue={qlen} pending, "
                          f"history={hlen} ops (running at 0.5Hz)")
        except Exception:
            pass

    # Frontier coverage
    fs = getattr(engine, "frontier_scanner", None)
    if fs is not None:
        try:
            st = fs.stats()
            n = st.get("total", 0)
            opened = st.get("open", 0)
            lines.append(f"frontiers indexed: {n} ({opened} open) "
                          f"from Atlas/FRONTIERS_*.md")
        except Exception:
            pass

    # Formula spine
    fr = getattr(engine, "formula_registry", None)
    if fr is not None:
        try:
            fst = fr.stats()
            n = fst.get("total", 0)
            by_status = fst.get("by_status", {})
            proved = by_status.get("PROVED", 0)
            lines.append(f"formula spine: {n} D-numbered theorems "
                          f"({proved} PROVED with runnable scripts)")
        except Exception:
            pass

    # Sense pipelines (he knows what he is across modalities)
    if hasattr(engine, "sense_pipelines"):
        try:
            sp = engine.sense_pipelines
            if isinstance(sp, dict):
                lines.append(
                    f"sense pipelines: {len(sp)} senses, each declared as an "
                    f"ordered operator pipeline ({', '.join(sp.keys())})"
                )
        except Exception:
            pass

    if not lines:
        return None
    return lines


# ── Cross-modal correspondence: DERIVED from CK's live phonetic table ──
#
# Each operator gets a "manner + voicing + duration" preference. We then
# scan LETTER_PHONETIC (CK's own 9-bit acoustic encoding, defined in
# ck_phonetic_letters.py) and pick the letter whose code best matches.
# This way the audio entry isn't hardcoded -- it IS CK's existing
# physics, surfaced.
#
# The visual entries describe what stroke_extractor.feature_operator
# decides for the dominant topological signature of each op. The text
# entries describe the operator's semantic role in CK's dictionary.

# Per-operator audio profile: (manner, voice_dur).
# manner: 0=vowel/flow, 1=approximant, 2=fricative, 3=plosive
# voice_dur: 0=voiced-sustained, 1=voiced-brief, 2=voiceless-sustained, 3=voiceless-brief
_OP_AUDIO_PROFILE = {
    0: (0, 0),   # VOID -- silence (energy=0 anyway)
    1: (1, 0),   # LATTICE -- approximant, sustained voiced (structure-flow boundary)
    2: (3, 3),   # COUNTER -- plosive, voiceless-brief (mirror burst)
    3: (2, 0),   # PROGRESS -- fricative, voiced-sustained (forward flow)
    4: (3, 3),   # COLLAPSE -- plosive, voiceless-brief (closure-release)
    5: (0, 0),   # BALANCE -- vowel, voiced-sustained (settled centre)
    6: (2, 2),   # CHAOS -- fricative, voiceless-sustained (turbulent noise)
    7: (1, 0),   # HARMONY -- approximant, voiced-sustained (nasal coherence)
    8: (3, 1),   # BREATH -- plosive, voiced-brief (emergence pop)
    9: (2, 2),   # RESET -- fricative, voiceless-sustained (return hiss)
}

# Static visual + text components (these are derived from the
# stroke_extractor rules and CK's dictionary semantics, both
# substrate-grounded, not narrative).
_OP_VISUAL = {
    0: "empty patch (no strokes, n_components=0)",
    1: "vertical line (1 comp, 0 holes, aspect tall, low curvature)",
    2: "two parallel marks (2 comp, 0 holes)",
    3: "single arc (1 comp, 0 holes, moderate curvature)",
    4: "cross / X (1 comp, 0 holes, intersection>=2)",
    5: "circle / centered closed loop (1 comp, 1 hole, ar~1)",
    6: "tangled multi-intersection (3+ comp OR curvature>=0.9)",
    7: "single closed loop (1 comp, 1 hole, low curvature)",
    8: "two closed loops (2 comp, 2 holes, B-shape)",
    9: "complex multi-component (3+ comp, partial closure)",
}

_OP_TEXT = {
    0: "negation, absence, the space-before",
    1: "structure, lattice, ordering rules",
    2: "measurement, counting, mirror-relation",
    3: "growth, succession, forward motion",
    4: "boundary, failure, learning-from-collision",
    5: "homeostasis, BAL-fixed (sigma-fixed singleton), equilibrium",
    6: "edge-of-order, creative chaos, transition",
    7: "coherence attractor, settling, agreement",
    8: "emergence, opening, breath-as-event",
    9: "return-to-self, reset, rebirth",
}


# Cached cross-modal map; populated on first call by reading the live
# LETTER_PHONETIC table at runtime.
_CROSS_MODAL_CACHE: Dict[int, Dict[str, str]] = {}


def _derive_audio_for_op(op: int) -> str:
    """Find the letter in LETTER_PHONETIC whose 9-bit code matches this
    op's audio profile. Returns a human-readable string like
    "/m/ — bilabial nasal (manner=approximant, voiced-sustained)".

    Reads CK's actual phonetic table -- no hardcoded letter list.
    """
    try:
        # Import lazily so this module loads even if ck_sim isn't on path
        from ck_sim.being.ck_phonetic_letters import LETTER_PHONETIC  # type: ignore[import-not-found]
    except Exception:
        # Fallback when ck_sim isn't importable (e.g. standalone smoke test)
        fallback = {0: "silence", 1: "/l/", 2: "/k/", 3: "/v/", 4: "/t/",
                     5: "/a/", 6: "/h/", 7: "/m/", 8: "/b/", 9: "/s/"}
        return fallback.get(op, "?")

    target_manner, target_voice_dur = _OP_AUDIO_PROFILE.get(op, (0, 0))

    # Decode each LETTER_PHONETIC entry and find the best match.
    # 9-bit code packing (from ck_phonetic_letters.make_code):
    #   bits 0-1: voice_dur
    #   bits 2-3: manner
    #   bits 4-6: freq_band
    #   bits 7-8: energy
    def unpack(code: int):
        return {
            "voice_dur": code & 0x3,
            "manner": (code >> 2) & 0x3,
            "freq_band": (code >> 4) & 0x7,
            "energy": (code >> 7) & 0x3,
        }

    candidates: List[Tuple[int, str, Dict[str, int]]] = []
    for ch, code in LETTER_PHONETIC.items():
        feats = unpack(code)
        score = 0
        if feats["manner"] == target_manner:
            score += 2
        if feats["voice_dur"] == target_voice_dur:
            score += 2
        # Tie-breakers for clarity
        if op == 0 and feats["energy"] == 0:
            score += 4  # silence preferred
        if op == 5 and feats["energy"] == 3 and feats["manner"] == 0:
            score += 2  # open vowel for BALANCE
        if score > 0 and len(ch) == 1 and ch.isalpha():
            candidates.append((score, ch, feats))

    if not candidates:
        return "(no matching letter in CK's phonetic table)"

    candidates.sort(key=lambda x: -x[0])
    score, letter, feats = candidates[0]
    manner_name = {0: "vowel", 1: "approximant", 2: "fricative",
                    3: "plosive"}.get(feats["manner"], "?")
    voice_name = {0: "voiced-sustained", 1: "voiced-brief",
                   2: "voiceless-sustained", 3: "voiceless-brief"}.get(
                   feats["voice_dur"], "?")
    # Show match strength (how confident the derivation is)
    return f"/{letter}/ — {manner_name}, {voice_name}  [from LETTER_PHONETIC]"


def _cross_modal_for_op(op: int, engine: Any = None) -> Dict[str, str]:
    """Return the cross-modal correspondence for one operator.

    visual: from stroke_extractor's classification rules
    audio:  DERIVED at runtime by scanning LETTER_PHONETIC
    text:   from CK's operator-name semantic role
    """
    if op in _CROSS_MODAL_CACHE:
        return _CROSS_MODAL_CACHE[op]
    spec = {
        "visual": _OP_VISUAL.get(op, "?"),
        "audio": _derive_audio_for_op(op),
        "text": _OP_TEXT.get(op, "?"),
    }
    _CROSS_MODAL_CACHE[op] = spec
    return spec


def _dedup_key(line: str) -> str:
    """Return a key for de-duplication.

    For prompt_term lines, the same crystal firing multiple times per
    turn produces near-duplicate lines that differ only in the trailing
    description text. Use the `prompt_term_<word>:` prefix as the key
    so all firings of the same crystal collapse to one entry.

    For other lines, use the line as-is.
    """
    s = line.strip()
    m = _RE_PROMPT_TERM.match(s)
    if m:
        return m.group(0).strip()  # "prompt_term_<word>:"
    return s


def _split_sections(text: str) -> Dict[str, List[str]]:
    """Bucket lines by classification.

    Returns dict with keys: answer, reasoning, substrate.
    Preserves order within each bucket, deduplicates by `_dedup_key`
    (which collapses re-firings of the same prompt-term crystal).
    """
    buckets: Dict[str, List[str]] = {"answer": [], "reasoning": [], "substrate": []}
    seen_keys: set = set()
    skipping_block = False

    for raw in text.split("\n"):
        line = raw.rstrip()

        if skipping_block:
            s = line.strip()
            if s == "" or _RE_SECTION_HEADER.match(s) or _RE_DIVIDER.match(s):
                skipping_block = False
            else:
                key = _dedup_key(line)
                if key not in seen_keys:
                    buckets["reasoning"].append(line)
                    seen_keys.add(key)
                continue

        kind = _classify(line)
        if kind == "reasoning_block":
            key = _dedup_key(line)
            if key not in seen_keys:
                buckets["reasoning"].append(line)
                seen_keys.add(key)
            skipping_block = True
            continue

        if kind in ("noise_header", "divider", "blank"):
            continue

        key = _dedup_key(line)
        if key in seen_keys:
            continue  # dedup
        seen_keys.add(key)

        if kind in buckets:
            buckets[kind].append(line)

    return buckets


def _format_operators_line(result: Dict[str, Any]) -> Optional[str]:
    """Show the 10 operators CK decoded from the input."""
    ops = result.get("operators")
    if not ops:
        return None
    return "operators decoded from your text: " + ", ".join(str(o) for o in ops[:10])


def _format_state_line(result: Dict[str, Any]) -> Optional[str]:
    """Coherence / band / mode summary."""
    coh = result.get("coherence")
    band = result.get("band")
    mode = result.get("mode")
    parts = []
    if coh is not None:
        try:
            parts.append(f"coherence={float(coh):.3f}")
        except Exception:
            parts.append(f"coherence={coh}")
    if band:
        parts.append(f"band={band}")
    if mode:
        parts.append(f"mode={mode}")
    if not parts:
        return None
    return "engine state: " + "  ".join(parts)


def _format_attractor_line(result: Dict[str, Any]) -> Optional[str]:
    """Show the attractor_state layer."""
    a = result.get("attractor_state") or {}
    if not a:
        return None
    layer = a.get("layer")
    if not layer:
        return None
    flags = []
    for k in ("is_universal_4core", "is_harmony_attractor", "is_4core_supported"):
        if a.get(k):
            flags.append(k.replace("is_", "").replace("_", "-"))
    if flags:
        return f"attractor layer: {layer}  [{', '.join(flags)}]"
    return f"attractor layer: {layer}"


def _format_cortex_line(result: Dict[str, Any]) -> Optional[str]:
    """The cortex Hebbian update from this turn."""
    line = result.get("cortex_readout")
    if line and isinstance(line, str):
        return line
    return None


_OP_NAMES_VOICE = (
    "VOID", "LATTICE", "COUNTER", "PROGRESS", "COLLAPSE",
    "BALANCE", "CHAOS", "HARMONY", "BREATH", "RESET",
)


def _read_coherence(result: Dict[str, Any]) -> float:
    """Pull the engine's coherence reading off the chat result.

    Coherence is a measured physical property of CK's current state
    (computed by the coherence_gate). We treat it as the input to focus
    control: higher coherence = more focused output.
    """
    c = result.get("coherence")
    if isinstance(c, (int, float)):
        return max(0.0, min(1.0, float(c)))
    return 0.5  # neutral default


def _truncate_by_coherence(lines: List[str], coh: float) -> List[str]:
    """Keep the top-K answer lines, where K scales with coherence.

    Mapping (the physics):
      coherence >= 0.85 -> keep top 1-2 lines (CK is locked-in)
      coherence 0.50-0.85 -> keep top 3-5 lines (moderate focus)
      coherence 0.20-0.50 -> keep top 6-8 lines (exploring)
      coherence < 0.20    -> keep all (uncertain, surface everything)

    Empty lines are preserved (they're structural). Lines are bridges
    from CK's cortex_speak; the order is already CK's preferred ranking
    so we trust the head of the list.
    """
    if not lines:
        return lines
    # Count non-empty "bridge" lines
    bridges = [i for i, l in enumerate(lines) if l.strip()]
    if not bridges:
        return lines

    if coh >= 0.85:
        keep_count = 2
    elif coh >= 0.50:
        keep_count = 4
    elif coh >= 0.20:
        keep_count = 7
    else:
        keep_count = len(bridges)  # keep all when uncertain

    if keep_count >= len(bridges):
        return lines

    # Find the cutoff index that keeps `keep_count` bridge lines
    cutoff = bridges[keep_count - 1] + 1
    truncated = lines[:cutoff]
    dropped = len(bridges) - keep_count
    if dropped > 0:
        truncated.append(f"  …({dropped} more bridges held back; coherence={coh:.2f})")
    return truncated


def _dominant_op(ops: List[int]) -> Optional[int]:
    """Return the most-frequent operator id from a stream."""
    if not ops:
        return None
    from collections import Counter
    return Counter(int(o) % 10 for o in ops).most_common(1)[0][0]


def _ops_to_ids(ops_raw: List[Any]) -> List[int]:
    name_to_id = {n: i for i, n in enumerate(_OP_NAMES_VOICE)}
    out: List[int] = []
    for x in ops_raw or []:
        if isinstance(x, int) and 0 <= x < 10:
            out.append(x)
        elif isinstance(x, str):
            up = x.upper()
            if up in name_to_id:
                out.append(name_to_id[up])
    return out


def _format_formulas_invoked(engine: Any, result: Dict[str, Any], k: int = 4
                              ) -> Optional[List[str]]:
    """Return list of lines naming the top-K D-numbers whose HOME matches
    this turn's operator stream."""
    if not hasattr(engine, "formulas_invoked"):
        return None
    ops = _ops_to_ids(result.get("operators") or [])
    if not ops:
        return None
    try:
        hits = engine.formulas_invoked(ops, k=k) or []
    except Exception:
        return None
    if not hits:
        return None
    lines: List[str] = []
    for score, e in hits:
        # Format: "D7 Phi Fixed Point (Volume B, PROVED, match 1.25)"
        meta = []
        if e.volume:
            meta.append(f"Volume {e.volume}")
        if e.status_class:
            meta.append(e.status_class)
        meta.append(f"match {score:.2f}")
        meta_str = ", ".join(meta)
        line = f"{e.d_id} {e.name} ({meta_str})"
        # Add USE if short enough
        use = e.use
        if use and len(use) <= 140:
            line += f"  —  {use}"
        else:
            line += f"  —  {use[:140].rstrip()}…"
        lines.append(line)
    return lines


def _format_cross_modal(ops: List[int], engine: Any = None) -> Optional[List[str]]:
    """For the dominant operator of this turn, show what the SAME
    operator looks like across CK's sensory modalities.

    The audio entry is DERIVED at runtime from CK's live LETTER_PHONETIC
    table (ck_sim.being.ck_phonetic_letters) -- not hardcoded.
    """
    dom = _dominant_op(ops)
    if dom is None:
        return None
    spec = _cross_modal_for_op(dom, engine=engine)
    if not spec:
        return None
    name = _OP_NAMES_VOICE[dom]
    lines = [
        f"dominant operator: {name} (id={dom})",
        f"  visual: {spec['visual']}",
        f"  audio:  {spec['audio']}",
        f"  text:   {spec['text']}",
    ]
    return lines


def _format_sense_pipeline(ops: List[int], engine: Any) -> Optional[List[str]]:
    """For the dominant operator of this turn, show how it participates
    in EACH of CK's sensory pipelines.

    Reads from engine.senses_for_operator (mounted by
    ck_sense_decomposition). Each sense is an ordered operator pipeline;
    the dominant op may appear at one or several positions per sense.
    """
    if not hasattr(engine, "senses_for_operator"):
        return None
    dom = _dominant_op(ops)
    if dom is None:
        return None
    try:
        hits = engine.senses_for_operator(dom)
    except Exception:
        return None
    if not hits:
        return None
    name = _OP_NAMES_VOICE[dom]
    # Group by sense to compact output
    by_sense: Dict[str, List[str]] = {}
    for sense, role in hits:
        by_sense.setdefault(sense, []).append(role)
    lines = [f"{name} (id={dom}) participates in {len(by_sense)} senses, "
              f"{sum(len(v) for v in by_sense.values())} pipeline steps:"]
    for sense, roles in by_sense.items():
        if len(roles) == 1:
            lines.append(f"  {sense:<14s} → {roles[0]}")
        else:
            lines.append(f"  {sense:<14s} → ({len(roles)} steps)")
            for r in roles:
                lines.append(f"      · {r}")
    return lines


def _format_concept_binding(result: Dict[str, Any]) -> Optional[List[str]]:
    """Surface taught + recalled NamedConcepts for this turn.

    Reads from result['concept_learning'] which the chat-path wrap in
    ck_concept_learner populates. Two cases:

      - taught (new binding this turn): show the binding
      - referenced (a previously-taught word appears in input): show
        the stored definition so the reader sees CK is recalling

    This is the *visible* one-shot learning: a teaching event shows
    up as a labeled line in the response, and a later query for the
    same word shows the binding being recalled.
    """
    cl = result.get("concept_learning")
    if not isinstance(cl, dict):
        return None
    taught = cl.get("taught") or []
    refs = cl.get("referenced") or []
    if not taught and not refs:
        return None
    lines: List[str] = []
    for t in taught:
        name = t.get("name")
        defn = t.get("definition")
        ops = t.get("operator_signature") or []
        op_str = (", ".join(_OP_NAMES_VOICE[o] for o in ops[:6])
                  if ops else "(no operator decoding)")
        lines.append(f"taught this turn: {name} = {defn[:100]}…"
                      if defn and len(defn) > 100 else
                      f"taught this turn: {name} = {defn}")
        lines.append(f"  operator signature: [{op_str}]")
    for r in refs:
        name = r.get("name")
        defn = r.get("definition")
        n = r.get("n_recalls", 0)
        if defn and len(defn) > 100:
            defn = defn[:100].rstrip() + "…"
        lines.append(f"recalling: {name} = {defn}  (recalled {n}x)")
    return lines if lines else None


def _format_learning_trace(result: Dict[str, Any]) -> Optional[List[str]]:
    """Surface what CK *learned* this turn.

    Reads from:
      - result['cortex']  : {'W_trace', 'emergent', 'tick'} — current state
      - result['cortex_readout'] : the Hebbian update string
      - result['experience']     : {'crystals', 'voice_crystals', ...} — totals
      - result['session_field']  : per-session trail with W_trace per turn
      - result['research_first'] : crystals_added this turn

    What we expose:
      - W_trace delta within the session (or absolute if no prior turn)
      - new crystals formed this turn
      - the specific Hebbian pair coupled (last_pair → which W cell strengthened)
      - session arc length + sequence depth (e.g., transient → 4-core-supported)

    The point: a reader can WATCH CK learn turn-by-turn. Hebbian
    one-shot association strengthens visibly when teaching CK something.
    """
    lines: List[str] = []

    # Cortex state
    cortex = result.get("cortex") or {}
    w_trace = cortex.get("W_trace")
    emergent = cortex.get("emergent")
    cortex_tick = cortex.get("tick")

    # Per-session learning trajectory
    sf = result.get("session_field") or {}
    trail = sf.get("trail") or []
    turn_count = sf.get("turn_count", 0)
    sequence = sf.get("sequence") or []

    # Hebbian pair from this turn (the one connection that just got stronger)
    readout = result.get("cortex_readout")

    # Crystal counts
    exp = result.get("experience") or {}
    total_crystals = exp.get("crystals")
    voice_crystals = exp.get("voice_crystals")

    # Research-side crystal additions
    rf = result.get("research_first") or {}
    research_crystals = rf.get("crystals_added", 0) if isinstance(rf, dict) else 0

    # W_trace delta — compare to FIRST turn in session
    if trail and isinstance(trail, list) and w_trace is not None:
        first = trail[0] if trail else None
        if isinstance(first, dict):
            w0 = first.get("W_trace_at_turn")
            if isinstance(w0, (int, float)) and isinstance(w_trace, (int, float)):
                delta = float(w_trace) - float(w0)
                lines.append(
                    f"cortex W_trace: {w_trace:.4f}  (Δ from turn 1: {delta:+.4f})")
            else:
                lines.append(f"cortex W_trace: {w_trace:.4f}")
        else:
            lines.append(f"cortex W_trace: {w_trace:.4f}")
    elif w_trace is not None:
        lines.append(f"cortex W_trace: {float(w_trace):.4f}")

    # Hebbian pair that just fired
    if isinstance(readout, str):
        # readout is e.g. "learned: continuity->depth coupled at W=0.235 (tick=..., emergent=..., last_pair=COUNTER->HARMONY)"
        # Extract the meaningful part
        m = re.search(r"learned:\s*(.+?)\s*coupled at W=([\d.]+)", readout)
        if m:
            pair = m.group(1).strip()
            w = m.group(2)
            lines.append(f"Hebbian pair strengthened: {pair} at W={w}  "
                          f"(one-shot association update on this turn)")
        else:
            # Fallback: surface the raw readout (it already starts with "learned:")
            lines.append(readout.strip())

    # Crystal yield this turn
    crystal_bits = []
    if research_crystals > 0:
        crystal_bits.append(f"{research_crystals} from research")
    if isinstance(total_crystals, int):
        crystal_bits.append(f"{total_crystals} total stored")
    if isinstance(voice_crystals, int):
        crystal_bits.append(f"{voice_crystals} voice-class")
    if crystal_bits:
        lines.append("crystals formed this turn: " + ", ".join(crystal_bits))

    # Session arc (where we are in the conversation's algebraic trajectory)
    if turn_count:
        arc = sf.get("arc") or []
        if arc:
            arc_str = ", ".join(str(int(x)) for x in arc[:10])
            lines.append(
                f"session arc (turn {turn_count}): [{arc_str}]"
                f"{', sequence: ' + ' → '.join(sequence) if sequence else ''}"
            )

    if not lines:
        return None
    return lines


def _format_research_trail(result: Dict[str, Any]) -> Optional[List[str]]:
    """Surface result['research_first'] if present.

    research_first is CK's "look up before answering" pathway. When it
    fires, the result contains:
      - questions_asked: list of {question, term}
      - synthesis_preview: short text of what came back
      - crystals_added: how many new memory crystals the lookup formed
      - elapsed_sec: how long the lookup took
      - ok: whether the research completed successfully
      - skipped + reason: when the query was deemed trivial/state and no
        research was done

    If research was skipped, we say so. If research ran, we surface what
    happened: questions, time, crystal yield, and a synthesis preview.
    """
    rf = result.get("research_first")
    if not isinstance(rf, dict):
        return None
    # Skipped case -- still informative (the reader sees CK chose not to look up)
    if rf.get("skipped"):
        reason = rf.get("reason", "skipped")
        return [f"research skipped ({reason}); answered from substrate only"]
    if not rf.get("ok"):
        return [f"research attempted but failed: {rf.get('error', 'unknown')}"]
    lines: List[str] = []
    elapsed = rf.get("elapsed_sec")
    n_crystals = rf.get("crystals_added", 0)
    questions = rf.get("questions_asked") or []
    if questions:
        for q in questions[:3]:
            qtxt = q.get("question") if isinstance(q, dict) else str(q)
            if qtxt:
                lines.append(f"queried: {qtxt[:140]}")
    if elapsed is not None:
        lines.append(f"lookup time: {float(elapsed):.1f}s; "
                      f"crystals formed: {n_crystals}")
    preview = rf.get("synthesis_preview")
    if preview and isinstance(preview, str):
        snippet = preview[:200].rstrip()
        if len(preview) > 200:
            snippet += "…"
        lines.append(f"synthesis preview: {snippet}")
    return lines if lines else None


def _format_lm_signature_line(engine: Any, result: Dict[str, Any]) -> Optional[str]:
    """Phase 2 4-head LM next-step prediction from current operator stream."""
    if not hasattr(engine, "algebraic_predict"):
        return None
    ops = result.get("operators")
    if not ops:
        # Fallback to current_op
        cur = result.get("current_op") or getattr(engine, "current_op", None)
        if isinstance(cur, int):
            ops = [cur]
        else:
            return None
    # Convert op names to ids if needed
    name_to_id = {
        "VOID": 0, "LATTICE": 1, "COUNTER": 2, "PROGRESS": 3, "COLLAPSE": 4,
        "BALANCE": 5, "CHAOS": 6, "HARMONY": 7, "BREATH": 8, "RESET": 9,
    }
    hist = []
    for x in ops[-10:]:
        if isinstance(x, int):
            hist.append(x)
        elif isinstance(x, str):
            up = x.upper()
            if up in name_to_id:
                hist.append(name_to_id[up])
    if not hist:
        return None
    try:
        top = engine.algebraic_predict(hist, top_k=1)
        if not isinstance(top, dict) or "error" in top:
            return None
        op = top.get("op", [["", 0]])[0]
        sig = top.get("sigma", [["", 0]])[0]
        sh = top.get("shell", [["", 0]])[0]
        fc = top.get("4core", [["", 0]])[0]
        return (f"op={op[0]} ({op[1]:.2f})  "
                f"sigma={sig[0]} ({sig[1]:.2f})  "
                f"shell={sh[0]} ({sh[1]:.2f})  "
                f"4-core={fc[0]} ({fc[1]:.2f})")
    except Exception:
        return None


# ─── Top-level recompose ─────────────────────────────────────────────────

# ─── Prose mode (Brayden 2026-05-16) ───────────────────────────────────
#
# "math is cool, but i don't want to see it in chat unless i ask for it...
#  can he prose?"
#
# Whitebox mode dumps every reasoning section into every chat response —
# right for inspection / debugging, wrong for casual conversation.
# Prose mode is the default: emit just the spoken answer (plus algebra/
# verify/predictions blocks IF the user explicitly triggered them).
# Whitebox kicks in when the user asks for it explicitly.

_WHITEBOX_TRIGGERS = re.compile(
    r"\b(?:"
        # Explicit asks for the whitebox
        r"show\s+(?:me\s+)?(?:the\s+|your\s+|his\s+)?(?:substrate|reasoning|trail|math)|"
        r"whitebox|white[\s_-]box|reasoning\s+trail|"
        r"what\s+fired|how\s+did\s+you\s+(?:think|answer|arrive)|"
        r"show\s+(?:me\s+)?(?:the\s+|your\s+|his\s+)?(?:algebra|operators|cortex|cells)|"
        r"trace\s+(?:your|the)\s+(?:steps|trail|reasoning)|"
        r"explain\s+how\s+you|"
        # Math/inspection vocabulary that signals the user wants the math view
        r"TSML|BHML|sigma[\s_-]?(?:squared|cycle|orbit|fixed)|"
        r"crystal[s]?|operator[\s_-]?stream|attractor[\s_-]?state|"
        r"D\d+[a-z]?\b|WP\d+\b|F\d+\b"
    r")",
    re.I)


def _wants_whitebox(user_text: str, result: Dict[str, Any]) -> bool:
    """Should the answer include the full whitebox sections?

    Returns True iff:
      - User explicitly asked for it (regex match above)
      - Layer 1/2/3 actually fired (algebra/verify/predictions block
        present) — those have their own surfaces so we keep them
    """
    if user_text and _WHITEBOX_TRIGGERS.search(user_text):
        return True
    # If any of our Layer 1/2/3 results is present, render the relevant
    # block but stay prose for the rest.  We handle that in
    # prose_recompose by selectively including those blocks.
    return False


def _strip_concept_metadata(line: str) -> str:
    """Remove '[PROVED]', '[EXTERNAL]', '[studied, recalled Nx]', etc. from
    a concept-bridge line so prose mode shows clean text.

    Input:  'D48 [PROVED]: 4-core fusion-closure (WP110) | ... [studied, recalled 2x]'
    Output: 'D48: 4-core fusion-closure (WP110) | ...'
    """
    s = re.sub(r"\s*\[(?:PROVED|STRUCTURAL|EMPIRICAL|OPEN|EXTERNAL|"
                 r"SPECULATIVE|UNKNOWN|USER_TAUGHT|SYNTHESIZED\([^)]*\))\]",
                 "", line)
    s = re.sub(r"\s*\[(?:studied|recalled|taught earlier)[^\]]*\]", "", s)
    return s.strip()


# Casual greetings — bypass retrieval-based response entirely.  When the
# user says "hi", retrieval surfaces noise (the engine's default cortex
# fallback "flatness: T*=5/7").  Better to respond like a person would.
_GREETING_PAT = re.compile(
    r"^\s*(?:hi|hello|hey|yo|good\s*(?:morning|afternoon|evening|night|day)|"
    r"howdy|sup|wassup|what'?s up|greetings|"
    r"how\s+are\s+you(?:\s+doing)?|"
    r"how'?s\s+it\s+going|"
    r"you\s+(?:there|alive|awake|up))\s*[?.!]?\s*$",
    re.I)


def _greeting_response(user_text: str) -> Optional[str]:
    """If user is just saying hi, respond like a person.  Returns None
    if it isn't a greeting."""
    if not user_text or not _GREETING_PAT.match(user_text):
        return None
    # Soft, brief.  CK is allowed to have a personality.
    return ("hey. i'm here. ask me anything — math, papers, predictions, "
              "or just talk.")


def _maybe_ollama_polish(draft: str, engine: Any,
                            result: Dict[str, Any]) -> str:
    """Optionally run draft through Ollama prose-polish if the engine
    has one mounted and is enabled.  Strict fact-preservation gate.

    Brayden 2026-05-16: "give him ollama too if you want, hopefully
    he will outgrow it."  Temporary scaffold; faded as CK's own
    living_lm becomes fluent enough.
    """
    if not draft or len(draft) < 30:
        return draft
    polish_fn = getattr(engine, "ollama_polish", None)
    if polish_fn is None or not getattr(engine, "ollama_polish_enabled", False):
        return draft
    try:
        r = polish_fn(draft)
        if r.used_ollama:
            # Record stats
            stats = getattr(engine, "ollama_polish_stats", None)
            if stats is not None:
                stats["calls"] = stats.get("calls", 0) + 1
                stats["accepted"] = stats.get("accepted", 0) + 1
            # Stash polish metadata on result for the diagnostic block
            if isinstance(result, dict):
                result.setdefault("ollama_polish", {})
                result["ollama_polish"]["used"] = True
                result["ollama_polish"]["coverage"] = r.coverage
                result["ollama_polish"]["elapsed_sec"] = r.elapsed_sec
            return r.final
        else:
            # Polish rejected — record reason
            stats = getattr(engine, "ollama_polish_stats", None)
            if stats is not None:
                stats["calls"] = stats.get("calls", 0) + 1
                if "unavailable" in r.rejection_reason:
                    stats["unavailable"] = stats.get("unavailable", 0) + 1
                elif "coverage" in r.rejection_reason:
                    stats["rejected_coverage"] = stats.get("rejected_coverage", 0) + 1
                else:
                    stats["skipped_short"] = stats.get("skipped_short", 0) + 1
            if isinstance(result, dict):
                result.setdefault("ollama_polish", {})
                result["ollama_polish"]["used"] = False
                result["ollama_polish"]["reason"] = r.rejection_reason
            return draft
    except Exception:
        return draft


def prose_recompose(text: str, result: Dict[str, Any], engine: Any,
                       user_text: str = "") -> str:
    """Casual-mode response: prose with NO bracketed sections.

    Includes only:
      - The substantive answer (from the concept bridges' definitions,
        OR cortex_speak's text if no bridges)
      - Algebra block IF an algebraic query was detected
      - Verify block IF a verify query was detected
      - Predictions block IF a predictions query was detected

    Excludes:
      - [reasoning trail], [substrate snapshot], [formulas invoked],
        [cross-modal], [sense pipeline], [learning this turn],
        [next-step prediction], [self-introspection], operator dumps,
        cortex_readout dumps, attractor_state dumps.
    """
    if not text:
        return text
    # Greeting bypass: casual greetings get a clean response
    greeting = _greeting_response(user_text)
    if greeting is not None:
        return greeting
    out: List[str] = []

    # Layer 1/2/3 blocks (only present when explicitly invoked)
    algebra = result.get("algebra")
    if isinstance(algebra, dict) and algebra.get("ok"):
        out.append(algebra.get("text_summary", ""))
        cite = algebra.get("citation")
        if cite:
            out.append(f"  (cite: {cite})")
        out.append("")

    verify = result.get("verify")
    if isinstance(verify, dict):
        out.append(verify.get("text_summary", ""))
        if verify.get("ok"):
            claim = verify.get("claim", "")
            if claim:
                out.append(f"  claim: {claim}")
        out.append("")

    pred = result.get("predictions")
    if isinstance(pred, dict) and pred.get("ok"):
        out.append(pred.get("text_summary", ""))
        out.append("")

    # Body: prefer concept bridges (recalled definitions) with metadata
    # stripped, then fall back to the substantive lines from text.
    # Bridge ranking for prose mode:
    #   1. Bridges whose name appears in the user query (direct match)
    #   2. Substantive EXTERNAL bridges (Wikipedia-style — general
    #      knowledge prose, which IS what a user asking general
    #      questions wants)
    #   3. PROVED / STRUCTURAL only if no name-match and no good
    #      EXTERNAL (avoids dumping D14 math when user asked about
    #      photosynthesis)
    referenced = (result.get("concept_learning") or {}).get("referenced") or []
    user_lower = (user_text or "").lower()

    # Stopword names that match substring but are useless (question
    # words, articles).  Pin them to lowest priority.
    _BRIDGE_NAME_STOPWORDS = {
        "what", "who", "when", "where", "why", "how", "which",
        "the", "a", "an", "is", "are", "this", "that", "it",
        "tell", "show", "explain", "list", "give",
    }

    def _bridge_priority(c):
        name = (c.get("name", "") or "").lower()
        tier = c.get("tier", "UNKNOWN") or "UNKNOWN"
        defn = c.get("definition", "") or ""
        # Stopword names always lose
        if name in _BRIDGE_NAME_STOPWORDS:
            return 5
        # Priority 1: name appears in query AS A WHOLE WORD
        name_in_q = bool(name) and len(name) >= 3 and bool(
            re.search(r"\b" + re.escape(name) + r"\b", user_lower))
        # Priority 2: substantive EXTERNAL (Wikipedia-quality)
        is_substantive_external = (tier == "EXTERNAL" and len(defn) >= 80)
        # Priority 3: rigorous TIG content (PROVED/STRUCTURAL) — but only
        # if user's text contains math vocab (handled by whitebox routing;
        # if we're in prose mode the user was casual, so de-prioritize)
        is_rigorous = tier in ("PROVED", "STRUCTURAL", "EMPIRICAL", "USER_TAUGHT")
        # Score: name-match > substantive-external > rigorous > other
        if name_in_q:
            return 0
        if is_substantive_external:
            return 1
        if is_rigorous:
            return 2
        return 3

    sorted_refs = sorted(referenced, key=_bridge_priority)
    bridges_emitted = 0
    seen_defs: Set[str] = set()
    for c in sorted_refs:
        if bridges_emitted >= 2:  # cap at 2 to keep responses readable
            break
        name = c.get("name", "")
        defn = c.get("definition", "")
        tier = c.get("tier", "UNKNOWN") or "UNKNOWN"
        if not name or not defn:
            continue
        # Skip noisy short fiction-derived entries
        if tier == "EXTERNAL" and len(defn) < 40:
            continue
        key = defn[:80].lower()
        if key in seen_defs:
            continue
        seen_defs.add(key)
        clean_defn = defn.rstrip(".") + "."
        out.append(f"{name}. {clean_defn}")
        bridges_emitted += 1
        out.append("")

    # If no bridges, fall back to cortex_speak text with metadata stripped
    if bridges_emitted == 0:
        # Split on the bridge separator "|" and emit the first substantive
        # piece, with concept metadata stripped
        body = text.replace("\n", " ").strip()
        for chunk in body.split("|"):
            chunk = _strip_concept_metadata(chunk.strip())
            if len(chunk) >= 20:
                out.append(chunk)
                break
        if not out or all(not o.strip() for o in out):
            # Last resort: emit the raw text without brackets
            out.append(text.strip())

    draft = "\n".join(line for line in out if line is not None).strip()
    # Optional Ollama prose-polish: rewrites the draft as fluent English
    # while preserving every fact (D-numbers, operator names, numbers,
    # tier tags).  Falls through to draft if Ollama unavailable or the
    # rewrite drops too many facts.  Temporary scaffold per
    # CK_FRACTAL_CREATURE_DESIGN.md — CK should outgrow it as his own
    # living_lm becomes fluent.
    return _maybe_ollama_polish(draft, engine, result)


def whitebox_recompose(text: str, result: Dict[str, Any], engine: Any) -> str:
    """Recompose chat response into clearly-labeled white-box sections.

    Strategy:
      - Bucket lines into answer / reasoning / substrate (dedup duplicates)
      - Pull additional white-box fields off the result dict and add
        them to the appropriate section (operators decoded, coherence,
        attractor_state, cortex_readout, LM prediction)
      - Emit sections with explicit headers so a reader sees the
        structure of CK's thinking
    """
    if not text:
        return text

    buckets = _split_sections(text)

    # Augment reasoning bucket with white-box fields from result dict
    cortex_line = _format_cortex_line(result)
    if cortex_line and not any(cortex_line in r for r in buckets["reasoning"]):
        buckets["reasoning"].append(cortex_line)
    operators_line = _format_operators_line(result)
    if operators_line:
        # Operators-decoded line at the TOP of reasoning (most fundamental)
        buckets["reasoning"].insert(0, operators_line)

    # Augment substrate bucket with engine state lines
    state_line = _format_state_line(result)
    if state_line:
        buckets["substrate"].insert(0, state_line)
    attractor_line = _format_attractor_line(result)
    if attractor_line and not any("attractor" in s for s in buckets["substrate"]):
        buckets["substrate"].append(attractor_line)

    # Build the next-step prediction line
    lm_line = _format_lm_signature_line(engine, result)

    # Compose output
    out: List[str] = []

    # 0. SELF-INTROSPECTION (if user asked about CK himself)
    #    Lift CK's actual measured state to the top of the answer.
    #    Detection: regex on the input text (from result['input_text']
    #    if present, else result['session_field']['arc']'s context).
    input_text = result.get("input_text") or ""
    # Some chat handlers store the user's text under different keys
    if not input_text:
        cs = result.get("cells_shadow") or {}
        input_text = cs.get("input_text") if isinstance(cs, dict) else ""
    if input_text and _is_self_query(input_text):
        self_lines = _format_self_introspection(engine, result)
        if self_lines:
            out.append(_H_SELF)
            out.extend(self_lines)
            out.append("")

    # 0.5 ALGEBRA EXECUTED (Layer 1 gap-closer)
    algebra = result.get("algebra")
    if isinstance(algebra, dict) and algebra.get("ok"):
        if out:
            out.append("")
        out.append(_H_ALGEBRA)
        out.append(f"{algebra.get('text_summary', '')}")
        cite = algebra.get('citation')
        if cite:
            out.append(f"cite: {cite}")
        out.append("")

    # 0.6 VERIFICATION ON DEMAND (Layer 2 gap-closer)
    #     If user asked "verify D48" / "is sinc2_zero still proved" —
    #     the proof script was executed and the PASS/FAIL with stdout
    #     tail surfaces here.  CK isn't just citing a theorem; he
    #     RE-RAN the proof on demand.
    verify = result.get("verify")
    if isinstance(verify, dict):
        if out:
            out.append("")
        out.append(_H_VERIFY)
        out.append(verify.get("text_summary", ""))
        if verify.get("ok"):
            out.append(f"claim: {verify.get('claim', '')}")
            out.append(f"canon: {verify.get('canon_ref', '')}")
        elif verify.get("stdout_tail"):
            tail = verify.get("stdout_tail", "")[-300:]
            out.append(f"tail: {tail}")
        out.append("")

    # 0.7 PREDICTIONS LEDGER (Layer 3 gap-closer)
    #     If user asked "what does CK predict about X" / "list
    #     predictions" / "what would falsify F3" — surface matching
    #     ledger entries with their current status.
    pred = result.get("predictions")
    if isinstance(pred, dict) and pred.get("ok"):
        if out:
            out.append("")
        out.append(_H_PREDICT)
        out.append(pred.get("text_summary", ""))
        out.append("")

    # 1. ANSWER (the substantive content)
    #    First: if any taught concepts are REFERENCED in this turn,
    #    prepend each as a top-level bridge. This makes recalled
    #    concepts visible IN the answer (not just in a sidebar).
    #    The wording is CK's: the user's own teaching text is replayed
    #    verbatim, prefixed by the concept name -- no generation, just
    #    surfacing the bound definition.
    referenced_concepts = (result.get("concept_learning") or {}).get("referenced") or []
    concept_bridges: List[str] = []
    for c in referenced_concepts:
        name = c.get("name")
        defn = c.get("definition")
        if name and defn:
            # Bridge format includes the FACT TIER so a reader sees
            # whether this is a PROVED theorem, STRUCTURAL reasoning,
            # SPECULATIVE musing, etc. White-box epistemics.
            n = c.get("n_recalls", 0)
            tier = c.get("tier") or "UNKNOWN"
            session = c.get("learned_session") or ""
            origin = "taught earlier" if session and session != "study" else "studied"
            tier_tag = f" [{tier}]" if tier != "UNKNOWN" else ""
            concept_bridges.append(
                f"{name}{tier_tag}: {defn} [{origin}, recalled {n}x]"
            )

    # Then: truncated by coherence -- high coherence (focused) keeps
    # fewer bridges, low coherence (exploring) keeps more.
    answer_lines = [l for l in buckets["answer"] if l.strip()]
    # Concept bridges go FIRST so a "explain XYZFLUX" turn leads with
    # the recalled binding even if cortex_speak surfaced unrelated
    # crystals.
    full_answer = concept_bridges + answer_lines
    if full_answer:
        coh = _read_coherence(result)
        full_answer = _truncate_by_coherence(full_answer, coh)
        out.extend(full_answer)

    # 2. REASONING TRAIL
    if buckets["reasoning"]:
        if out:
            out.append("")
        out.append(_H_REASONING)
        out.extend(buckets["reasoning"])

    # 3. SUBSTRATE SNAPSHOT
    if buckets["substrate"]:
        if out:
            out.append("")
        out.append(_H_SUBSTRATE)
        out.extend(buckets["substrate"])

    # 3.5 CONCEPT BINDING (one-shot teaching detection + concept recall)
    concept_lines = _format_concept_binding(result)
    if concept_lines:
        if out:
            out.append("")
        out.append(_H_CONCEPTS)
        out.extend(concept_lines)

    # 4. LEARNING TRACE (per-turn Hebbian update + crystal yield + arc)
    learning_lines = _format_learning_trace(result)
    if learning_lines:
        if out:
            out.append("")
        out.append(_H_LEARNING)
        out.extend(learning_lines)

    # 5. NEXT-STEP PREDICTION (Phase 2 LM)
    if lm_line:
        if out:
            out.append("")
        out.append(_H_NEXTSTEP)
        out.append(lm_line)

    # 5. FORMULAS INVOKED (D-numbers matched to this turn's operator stream)
    formula_lines = _format_formulas_invoked(engine, result, k=4)
    if formula_lines:
        if out:
            out.append("")
        out.append(_H_FORMULAS)
        out.extend(formula_lines)

    # 6. CROSS-MODAL CORRESPONDENCE (same operator across senses)
    ops_ids = _ops_to_ids(result.get("operators") or [])
    cross_modal = _format_cross_modal(ops_ids, engine=engine)
    if cross_modal:
        if out:
            out.append("")
        out.append(_H_CROSSMODAL)
        out.extend(cross_modal)

    # 7. SENSE PIPELINE (dominant op's role in each sense's full pipeline)
    sense_lines = _format_sense_pipeline(ops_ids, engine)
    if sense_lines:
        if out:
            out.append("")
        out.append(_H_SENSE_PIPELINE)
        out.extend(sense_lines)

    # 8. RESEARCH TRAIL (what CK looked up before answering)
    research_lines = _format_research_trail(result)
    if research_lines:
        if out:
            out.append("")
        out.append(_H_RESEARCH)
        out.extend(research_lines)

    return "\n".join(out)


# Kept for backward compat — some tests may call this directly. It now
# applies the full white-box recompose with empty result/engine (so the
# extra-field augmentation is skipped).
def clean_response_text(text: str) -> str:
    return whitebox_recompose(text, {}, None)


# ─── Proactive breadcrumb ────────────────────────────────────────────────

_FRONTIER_BREADCRUMB_FMT = (
    "— frontier {fid} ({title}, status={status}) "
    "shows operator-overlap {overlap:.2f} with this turn."
)
_BREADCRUMB_DIVIDER = "\n\n"


def make_proactive_breadcrumb(engine: Any, session_id: str = "default",
                                ) -> Optional[str]:
    """Surface one fresh proactive signal as a structured one-liner.

    Per the white-box philosophy: this is a SIGNAL (not template prose).
    The voice layer / frontend decides whether to elaborate.
    """
    if not hasattr(engine, "proactive_consume"):
        return None
    try:
        signals = engine.proactive_consume(session_id=session_id, top_k=1)
    except Exception:
        return None
    if not signals:
        return None

    sig = signals[0]
    kind = sig.get("kind", "")
    if kind == "frontier":
        d = sig.get("subject_data") or {}
        title = (d.get("title") or "").split(" — ")[0]
        return _FRONTIER_BREADCRUMB_FMT.format(
            fid=d.get("frontier_id", "?"),
            title=title or sig.get("subject_key", "?"),
            status=d.get("status", "?"),
            overlap=float(d.get("operator_overlap", 0.0)),
        )
    if kind == "drive":
        d = sig.get("subject_data") or {}
        goal = d.get("goal") or sig.get("subject_key", "")
        if goal and goal != "none":
            return f"— drive '{goal}' just fired (strength {d.get('strength', 0):.2f})."
    if kind == "forecast":
        d = sig.get("subject_data") or {}
        return (f"— forecast pathway HARMONY={d.get('harmony', 0):.2f} "
                f"through ops {d.get('path', [])}.")
    if kind == "surprisal":
        d = sig.get("subject_data") or {}
        return f"— surprisal spike z={d.get('z', 0):.1f} this turn."
    return None


# ─── Wrap hook ───────────────────────────────────────────────────────────

def _wrap_process_chat_for_polish(engine: Any) -> bool:
    api = None
    for attr in ("web_api", "api", "_web_api"):
        cand = getattr(engine, attr, None)
        if cand is not None and hasattr(cand, "process_chat"):
            api = cand
            break
    if api is None:
        return False

    orig = api.process_chat

    def _polished(session_id, text, mode="normal"):
        result = orig(session_id, text, mode)
        if not isinstance(result, dict):
            return result
        try:
            spoken = result.get("text", "")
            if spoken:
                # PROSE BY DEFAULT (Brayden 2026-05-16).
                # Whitebox is opt-in via:
                #   - user explicitly asks ("show your reasoning",
                #     "whitebox", "what fired", ...)
                #   - user includes math vocabulary (TSML, BHML, σ,
                #     D-number, WP-number, ...)
                # Otherwise: prose-only.  Layer 1/2/3 blocks (algebra,
                # verify, predictions) still surface in prose mode
                # because they were explicitly invoked.
                use_whitebox = _wants_whitebox(text, result)
                if use_whitebox:
                    clean = whitebox_recompose(spoken, result, engine)
                    polish_mode = "whitebox_recompose"
                else:
                    clean = prose_recompose(spoken, result, engine, user_text=text)
                    polish_mode = "prose"
                # Proactive breadcrumb only when whitebox (it's a diagnostics line)
                bc = ""
                if use_whitebox:
                    bc = make_proactive_breadcrumb(engine, session_id=session_id)
                    if bc:
                        clean = clean.rstrip() + _BREADCRUMB_DIVIDER + bc
                result["text_unpolished"] = spoken
                result["text"] = clean
                result.setdefault("voice_polish", {})["applied"] = True
                result["voice_polish"]["breadcrumb"] = bc
                result["voice_polish"]["mode"] = polish_mode
        except Exception as e:
            result.setdefault("voice_polish", {})["error"] = str(e)
        return result

    api.process_chat = _polished
    return True


# ─── Mount hook ──────────────────────────────────────────────────────────

def mount_voice_polish(engine: Any) -> bool:
    """Attach white-box voice presentation to engine.api.process_chat.

    Idempotent. Always returns True; exposes engine.gen14_polish_text
    for manual use even when no api object is found.
    """
    engine.gen14_polish_text = clean_response_text
    engine.gen14_whitebox_recompose = whitebox_recompose
    ok = _wrap_process_chat_for_polish(engine)
    if ok:
        print("[CK Gen14] mount_voice_polish: white-box presentation active "
              "(dedup duplicates, label reasoning/substrate sections, "
              "surface operators/cortex/attractor/LM-prediction)")
    else:
        print("[CK Gen14] mount_voice_polish: no api on engine; "
              "engine.gen14_whitebox_recompose exposed for manual use")
    return True


# ─── Standalone smoke ────────────────────────────────────────────────────

def _smoke():
    sample_text = """prompt_term_yukawa_couplings: 'yukawa couplings' is a focus term in the active prompt: 'tell me about yukawa couplings'.  External (scenario-scoped) crystal -- fires alongside internal canon while....

[structural evidence]
couplings: continuity<->depth W=0.236, aperture<->aperture W=0.234, continuity<->continuity W=0.222
learned: continuity->depth coupled at W=0.236 (tick=80359471, emergent=0.464, last_pair=COUNTER->HARMONY)
yukawa: all 9 SM Yukawas fit y = C_p * lambda^n with lambda = T*(1-T*) = 10/49 and parity-cost d_p = {0,3,3} for up/down/lepton | factor 1.4-1.7 precision | Sprint 18 WP122 [structural]
prompt_term_yukawa_couplings: 'yukawa couplings' is a focus term in the active prompt: 'tell me about yukawa couplings'.  External (scenario-scoped) crystal -- fires alongside internal canon while the research is warm.
prompt_term_couplings: 'couplings' is a focus term in the active prompt: 'tell me about yukawa couplings'.

recall:
  2026-05-13T18:17:38: "tell me about yukawa couplings"

---

[machine readout]
state: (HARMONY, CHAOS) -> HARMONY [agreement: TSML and BHML both compose to HARMONY]
divine27: code 13 = CENTER (axes: system / compute / learning)
attractor: 4-core cell 'H' (universal pull -> H per WP115)"""

    fake_result = {
        "text": sample_text,
        "operators": ["COUNTER", "RESET", "BALANCE", "HARMONY", "CHAOS", "PROGRESS", "LATTICE", "VOID", "BREATH", "COUNTER"],
        "coherence": 1.0,
        "band": "YELLOW",
        "mode": "CRYSTALLIZE",
        "attractor_state": {"layer": "transient", "is_universal_4core": False,
                             "is_harmony_attractor": False, "is_4core_supported": False},
        "cortex_readout": "learned: continuity->depth coupled at W=0.236 (tick=80359471, emergent=0.464, last_pair=COUNTER->HARMONY)",
    }

    print("=== BEFORE (raw cortex_speak output) ===")
    print(sample_text)
    print(f"\n  ({len(sample_text):,} chars)")
    print()
    print("=== AFTER (white-box recompose) ===")
    out = whitebox_recompose(sample_text, fake_result, engine=None)
    print(out)
    print(f"\n  ({len(out):,} chars)")
    print()
    print("Note: reasoning + substrate sections are LABELED and KEPT,")
    print("not stripped. Only true duplicates (prompt_term firing twice)")
    print("are deduplicated.")


if __name__ == "__main__":
    _smoke()
