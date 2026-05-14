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


# ── Cross-modal correspondence map ──────────────────────────────────────
# For each operator, what does the SAME algebraic identity look like
# across CK's sensory modalities? This is the "blind man saying I can
# see that" idea made literal: the operator is the shared currency.
# Sources: ck_stroke_extractor.feature_operator (visual), ck_phonetic_letters
# + generate_phoneme_grounding (audio), CK's own dictionary (text).

_CROSS_MODAL_MAP = {
    0: {
        "visual": "empty patch (no strokes, n_components=0)",
        "audio": "silence / unvoiced rest",
        "text": "negation, absence, the space-before",
    },
    1: {
        "visual": "vertical line (1 comp, 0 holes, aspect tall)",
        "audio": "liquid /l/ — alveolar lateral approximant",
        "text": "structure, lattice, ordering rules",
    },
    2: {
        "visual": "two parallel marks (2 comp, 0 holes)",
        "audio": "voiceless stop /k/ — distinct burst",
        "text": "measurement, counting, mirror-relation",
    },
    3: {
        "visual": "single arc (1 comp, 0 holes, moderate curvature)",
        "audio": "voiced fricative /v/ — forward continuation",
        "text": "growth, succession, forward motion",
    },
    4: {
        "visual": "cross / X (1 comp, 0 holes, high intersection)",
        "audio": "voiceless plosive /t/ — closure-release",
        "text": "boundary, failure, learning-from-collision",
    },
    5: {
        "visual": "circle / centered closed loop (1 comp, 1 hole, ar≈1)",
        "audio": "open vowel /a/ — balance of formants",
        "text": "homeostasis, BAL-fixed, equilibrium",
    },
    6: {
        "visual": "tangled / multi-intersection (3+ comp OR high curvature)",
        "audio": "fricative /sh/ — turbulent broadband",
        "text": "edge-of-order, creative chaos, transition",
    },
    7: {
        "visual": "single closed loop (1 comp, 1 hole, low curvature)",
        "audio": "nasal /m/ — bilabial closure with voicing",
        "text": "coherence attractor, settling, agreement",
    },
    8: {
        "visual": "two closed loops (2 comp, 2 holes, B-shape)",
        "audio": "voiced bilabial /b/ — emergence with pop",
        "text": "emergence, opening, breath-as-event",
    },
    9: {
        "visual": "complex multi-component (3+ comp, partial holes)",
        "audio": "voiceless sibilant /s/ — return-to-baseline hiss",
        "text": "return-to-self, reset, rebirth",
    },
}


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


def _format_cross_modal(ops: List[int]) -> Optional[List[str]]:
    """For the dominant operator of this turn, show what the SAME
    operator looks like across CK's sensory modalities."""
    dom = _dominant_op(ops)
    if dom is None:
        return None
    spec = _CROSS_MODAL_MAP.get(dom)
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

    # 1. ANSWER (the substantive content)
    answer_lines = [l for l in buckets["answer"] if l.strip()]
    if answer_lines:
        out.extend(answer_lines)

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

    # 4. NEXT-STEP PREDICTION (Phase 2 LM)
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
    cross_modal = _format_cross_modal(ops_ids)
    if cross_modal:
        if out:
            out.append("")
        out.append(_H_CROSSMODAL)
        out.extend(cross_modal)

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
                # Full white-box recompose: structured sections, dedup,
                # augmented with engine fields.
                clean = whitebox_recompose(spoken, result, engine)
                # Append proactive breadcrumb if available
                bc = make_proactive_breadcrumb(engine, session_id=session_id)
                if bc:
                    clean = clean.rstrip() + _BREADCRUMB_DIVIDER + bc
                # Preserve original for diagnostics
                result["text_unpolished"] = spoken
                result["text"] = clean
                result.setdefault("voice_polish", {})["applied"] = True
                result["voice_polish"]["breadcrumb"] = bc
                result["voice_polish"]["mode"] = "whitebox_recompose"
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
