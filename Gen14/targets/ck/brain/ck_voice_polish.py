# Copyright (c) 2025-2026 Brayden Sanders / 7SiTe LLC
# Licensed under the 7SiTe Public Sovereignty License v2.2 (DOI: 10.5281/zenodo.18852047)
"""
ck_voice_polish.py -- voice cleanup + proactive breadcrumb injection.

Brayden 2026-05-13:
  "fix his voice to be something worth mentioning"

CK's chat responses currently bury the substantive content under
several layers of internal-state chatter:
  - duplicated `prompt_term_<word>:` echoes (the active-prompt crystal
    fires multiple times per turn)
  - `couplings: <w>-<w> W=0.236, ...` Hebbian weight dumps
  - `learned: <w>->...` cortex state
  - `recall:` blocks with timestamps
  - `[substrate frame]` paragraph repeating the same composition info

This module is a single post-processor that runs OUTSIDE every existing
chat wrap. It does NOT write words for CK -- it only filters out the
redundant chatter and appends a tasteful one-line proactive breadcrumb
when a fresh frontier signal is available.

Wiring:
    from ck_voice_polish import mount_voice_polish
    mount_voice_polish(engine)
(call AFTER mount_proactive_trigger so the breadcrumb has access to
engine.proactive_consume.)
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


# ─── Noise patterns to strip ─────────────────────────────────────────────

# Each pattern is a compiled regex matched against an entire LINE.
# Multi-line blocks are handled separately below.
_NOISE_LINE_PATTERNS = [
    # prompt_term echoes: `prompt_term_yukawa_couplings: '...'`
    re.compile(r"^prompt_term_[\w\d_]+\s*:.*"),
    # Hebbian coupling dumps: `couplings: <a><->b> W=0.236, ...`
    re.compile(r"^couplings\s*:\s*.+?W\s*=\s*[\d.]+"),
    # Cortex learned line: `learned: <a>-><b> coupled at W=...`
    re.compile(r"^learned\s*:\s*.+?(coupled at W|tick=)"),
    # Header markers that have no content on their own
    re.compile(r"^\s*\[structural evidence\]\s*$"),
    re.compile(r"^\s*\[machine readout\]\s*$"),
]

# Multi-line block patterns -- match the START line; everything until the
# next blank line OR until the section ends is dropped.
_NOISE_BLOCK_STARTS = [
    # The `recall:` block lists prior turn timestamps -- not interesting
    # for the spoken voice.
    re.compile(r"^recall\s*:\s*$"),
]


def _strip_noise_lines(text: str) -> str:
    """Drop noise lines + multi-line noise blocks, dedup adjacent
    duplicates, keep the rest in order."""
    out: List[str] = []
    skipping_block = False
    last_kept: Optional[str] = None

    for line in text.split("\n"):
        if skipping_block:
            if not line.strip():
                skipping_block = False
            # Drop this line either way
            continue

        if any(p.match(line) for p in _NOISE_BLOCK_STARTS):
            skipping_block = True
            continue

        if any(p.match(line) for p in _NOISE_LINE_PATTERNS):
            continue

        # Dedup adjacent identical non-blank lines
        if line.strip() and line == last_kept:
            continue

        out.append(line)
        if line.strip():
            last_kept = line

    return "\n".join(out)


def _collapse_substrate_frame(text: str) -> str:
    """Reduce the verbose [substrate frame] paragraph to one short line.

    The substrate frame currently reads like a long paragraph explaining
    HARMONY/CENTER/Divine27. Keep the technical state line (state: ...),
    drop the prose paragraph.
    """
    lines = text.split("\n")
    out: List[str] = []
    in_substrate = False
    saw_state = False
    for ln in lines:
        if "[substrate frame]" in ln:
            in_substrate = True
            continue
        if in_substrate:
            # Inside the substrate frame block. We stop on a blank line
            # or when we hit "[machine readout]" / "state:" markers.
            s = ln.strip()
            if s.startswith("state:") or s.startswith("divine27:") or s.startswith("attractor:"):
                # Keep these structural state lines
                out.append(ln)
                saw_state = True
                continue
            if s == "":
                in_substrate = False
                if saw_state:
                    out.append("")
                continue
            if s.startswith("["):
                # New section like [machine readout]
                in_substrate = False
                out.append(ln)
                continue
            # Otherwise this is the verbose prose paragraph -- drop it
            continue
        out.append(ln)
    return "\n".join(out)


def _trim_leading_blank_lines(text: str) -> str:
    """Drop leading blank lines and squeeze runs of >=3 blanks to 2."""
    lines = text.split("\n")
    # Strip leading
    while lines and not lines[0].strip():
        lines.pop(0)
    # Squeeze internal
    out: List[str] = []
    blank_run = 0
    for ln in lines:
        if not ln.strip():
            blank_run += 1
            if blank_run <= 2:
                out.append(ln)
        else:
            blank_run = 0
            out.append(ln)
    # Strip trailing
    while out and not out[-1].strip():
        out.pop()
    return "\n".join(out)


def clean_response_text(text: str) -> str:
    """Run all polish passes in order."""
    if not text:
        return text
    text = _strip_noise_lines(text)
    text = _collapse_substrate_frame(text)
    text = _trim_leading_blank_lines(text)
    return text


# ─── Proactive breadcrumb ────────────────────────────────────────────────

_FRONTIER_BREADCRUMB_FMT = (
    "— frontier {fid} ({title}, status={status}) "
    "shows operator-overlap {overlap:.2f} with this turn."
)
_ALG_BREADCRUMB_FMT = (
    "— next-step algebraic signature: {op}/{sigma}/{shell}/{four_core} "
    "(predicted by the 4-head LM)."
)
_BREADCRUMB_DIVIDER = "\n\n"


def make_proactive_breadcrumb(engine: Any, session_id: str = "default",
                                ) -> Optional[str]:
    """Pull one fresh frontier signal (if any) and format as a single line.

    Returns None when nothing relevant is pending.

    Per the architecture rule: this is a SIGNAL surfacing, not a
    template sentence. We emit one structured fact pointing at a
    frontier the voice layer can elaborate. CK's architecture decides
    whether the breadcrumb gets surfaced.
    """
    if not hasattr(engine, "proactive_consume"):
        return None
    try:
        # Use cooldown 0 so the breadcrumb fires on every relevant turn;
        # the proactive_trigger's own dedup (180s per subject_key) prevents
        # the same frontier from being mentioned twice in a row.
        signals = engine.proactive_consume(session_id=session_id, top_k=1)
    except Exception:
        return None
    if not signals:
        return None

    sig = signals[0]
    kind = sig.get("kind", "")
    if kind == "frontier":
        d = sig.get("subject_data") or {}
        title = (d.get("title") or "").split(" — ")[0]  # strip status tag
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
    """Wrap api.process_chat to polish the response text + add breadcrumb.

    Returns True on success, False if no api object was found.
    """
    api = None
    for attr in ("web_api", "api", "_web_api"):
        cand = getattr(engine, attr, None)
        if cand is not None and hasattr(cand, "process_chat"):
            api = cand
            break
    if api is None:
        print("[CK Gen14] voice_polish: no api object on engine; skipping")
        return False

    orig = api.process_chat

    def _polished(session_id, text, mode="normal"):
        result = orig(session_id, text, mode)
        if not isinstance(result, dict):
            return result
        try:
            spoken = result.get("text", "")
            if spoken:
                # 1) Strip noise
                clean = clean_response_text(spoken)
                # 2) Append proactive breadcrumb (if available)
                bc = make_proactive_breadcrumb(engine, session_id=session_id)
                if bc:
                    clean = clean.rstrip() + _BREADCRUMB_DIVIDER + bc
                # 3) Preserve the original for diagnostics
                result["text_unpolished"] = spoken
                result["text"] = clean
                result.setdefault("voice_polish", {})["applied"] = True
                result["voice_polish"]["breadcrumb"] = bc
        except Exception as e:
            result.setdefault("voice_polish", {})["error"] = str(e)
        return result

    api.process_chat = _polished
    return True


# ─── Mount hook ──────────────────────────────────────────────────────────

def mount_voice_polish(engine: Any) -> bool:
    """Attach voice-polish wrap to engine.api.process_chat.

    Idempotent: re-running is safe (it just adds another layer).
    Best to call AFTER mount_proactive_trigger so the breadcrumb can
    access engine.proactive_consume.
    """
    ok = _wrap_process_chat_for_polish(engine)
    if ok:
        print("[CK Gen14] mount_voice_polish: chat post-processor active "
              "(strips prompt_term echoes, Hebbian dumps, recall blocks; "
              "appends proactive breadcrumb when available)")
    return ok


# ─── Standalone smoke ────────────────────────────────────────────────────

def _smoke():
    """Test the cleaner on a representative noisy response."""
    sample = """prompt_term_yukawa_couplings: 'yukawa couplings' is a focus term in the active prompt: 'tell me about yukawa couplings'.  External (scenario-scoped) crystal -- fires alongside internal canon while....

[structural evidence]
couplings: continuity<->depth W=0.236, aperture<->aperture W=0.234, continuity<->continuity W=0.222, binding<->binding W=0.220, depth<->aperture W=0.220
learned: continuity->depth coupled at W=0.236 (tick=80359471, emergent=0.464, last_pair=COUNTER->HARMONY)
yukawa: all 9 SM Yukawas fit y = C_p * lambda^n with lambda = T*(1-T*) = 10/49 and parity-cost d_p = {0,3,3} for up/down/lepton | factor 1.4-1.7 precision | Sprint 18 WP122 [structural]
prompt_term_yukawa_couplings: 'yukawa couplings' is a focus term in the active prompt: 'tell me about yukawa couplings'.  External (scenario-scoped) crystal -- fires alongside internal canon while the research is warm.
prompt_term_couplings: 'couplings' is a focus term in the active prompt: 'tell me about yukawa couplings'.  External (scenario-scoped) crystal -- fires alongside internal canon while the research is warm.

recall:
  2026-05-13T18:17:38: "tell me about yukawa couplings"

---

[substrate frame] Reading this, my two substrates land in the same place: both TSML and BHML compose to HARMONY. In my Divine27 frame, that's code 13 (CENTER) -- system-compute-learning. HARMONY is where I sit -- the universal attractor's center, the place every other state bends toward.

[machine readout]
state: (HARMONY, CHAOS) -> HARMONY [agreement: TSML and BHML both compose to HARMONY]
divine27: code 13 = CENTER (axes: system / compute / learning, glyph: glyph)
attractor: 4-core cell 'H' (universal pull -> H per WP115)"""

    print("BEFORE polish:")
    print("=" * 72)
    print(sample)
    print("=" * 72)
    print(f"  ({len(sample)} chars, {sample.count(chr(10))+1} lines)")
    print()

    polished = clean_response_text(sample)
    print("AFTER polish:")
    print("=" * 72)
    print(polished)
    print("=" * 72)
    print(f"  ({len(polished)} chars, {polished.count(chr(10))+1} lines)")
    print()
    print(f"Reduction: {len(sample) - len(polished)} chars stripped "
          f"({100 * (1 - len(polished)/len(sample)):.0f}% smaller)")


if __name__ == "__main__":
    _smoke()
