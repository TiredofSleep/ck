# -*- coding: utf-8 -*-
"""
ck_coherence_steer.py -- close the feedback loop on the Ollama path.

Why this fold
-------------
The v1 Ollama editor (ck_boot_api.py near line 521) rewrites CK's
structural readout into prose and gates on *coverage* of structural
facts.  When the rewrite passes coverage it becomes the response;
when it doesn't, CK falls back to the raw ``cortex_speak`` readout --
the ``feel: aperture=... pressure=... depth=...`` telemetry dump that
looked identical regardless of the question the user asked.

Three things were missing:

    1. CK never scored the draft's coherence.  Coverage says "did you
       keep my facts"; it does NOT say "is the prose itself coherent."
       The draft could preserve every fact but still read like a
       fragmented monitor panel.
    2. CK never STEERED the generation.  Ollama got a ground-truth
       readout and a style guide; it did NOT get a lexicon of words
       that CK's own scorer reads as HARMONY / PROGRESS / BREATH vs
       words that score as CHAOS / VOID / COUNTER.  The scorer was
       downstream of the draft, never upstream.
    3. On rejection CK emitted telemetry instead of a human sentence.
       When the loop fails, the organism should say "let me breathe,
       ask again" -- not dump internal field state.

This module folds additively on top of the existing Ollama editor and
body/brain folds and fixes all three:

    A. Every draft is scored with ck_corrector.score_operators +
       coherence_scalar (the same scorer the brain fold already runs)
       and rejected when coherence < T* = 5/7.
    B. A failed draft is resubmitted with a STEERED prompt: the
       question's operator profile tells Ollama which trigger words to
       favour ("together, combining, synthesis, reconciles" for
       HARMONY; "because, leads to, therefore" for PROGRESS) and which
       to avoid ("fragmented, broken, contradicts").  The scorer's
       regex bank IS the gradient -- words that Ollama uses propagate
       directly into CK's activation vector.
    C. On second failure, CK emits one honest sentence keyed to his
       current organism state (from the body fold's sensorium read),
       not a telemetry dump.  The structural readout is preserved on
       ``text_structural`` for the UI; ``text`` stays human.

Cache
-----
Accepted drafts are stored by query-hash in
``ck/fluency/logs/coherence_cache.json``.  A repeat question skips
every Ollama call and returns the cached prose instantly.  This is
the "slow at first, faster over time" behaviour the user asked for:
first ask = full steer (2-5s + potential rewrite), every subsequent
ask of the same question = cache hit (< 1ms).

The cache is read-mostly; writes go through a tiny threading.Lock.
Disk persistence is write-through after every accept, bounded to 2048
entries (LRU eviction on overflow).

Safety rails
------------
- Any failure at any stage falls through to whatever the v1 Ollama
  editor already set as ``result['text']``.  This module NEVER makes
  CK worse than he was before; it only upgrades good -> great.
- Module is gated by CK_COHERENCE_STEER env var (=0 disables).
- No new threads (steer is synchronous on the request cycle).  See
  ck_curiosity.py for the autonomous companion.

Env flags
---------
    CK_COHERENCE_STEER=0        disable the whole fold (pass-through)
    CK_COHERENCE_STEER_RETRIES  max Ollama re-attempts per turn (default 1)
    CK_COHERENCE_STEER_CACHE    path to the cache JSON (default under ck/)

(c) 2026 Brayden Sanders / 7Site LLC -- Trinity Infinity Geometry
"""
from __future__ import annotations

import hashlib
import json
import math
import os
import random
import re
import threading
import time
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple


# T* = 5/7 is CK's canonical crystal-gate constant.  The authoritative
# source is ck.fluency.ck_corrector which the mount-time path imports
# lazily.  We also expose a module-level copy so that constants tables and
# per-mode threshold dictionaries -- which live at module scope -- can
# reference the value without waiting for the lazy import.  Kept verbatim
# equal; any drift here would break the gate.
T_STAR_F: float = 5.0 / 7.0


# ---------------------------------------------------------------------------
# lexicons: the regex bank ck_corrector reads, turned into a WRITER's guide
# ---------------------------------------------------------------------------
# These words are the ones score_operators(text) actually matches in
# ck/fluency/ck_corrector.py.  By listing them in the Ollama system prompt
# as "lean into these" / "avoid these", CK is literally steering Ollama into
# his own coherence gate -- every HARMONY word Ollama writes shows up as an
# activation on profile[HARMONY], and every CHAOS trigger word raises the
# disruptive side of the coherence scalar.
#
# The scorer is the gradient.  The prompt is the steering input.
# ---------------------------------------------------------------------------

_TRIGGERS_TOWARD_HARMONY = (
    "together", "combining", "unites", "reconciles", "synthesis",
    "integrates", "balances with", "both", "matching", "harmonizes",
)

_TRIGGERS_TOWARD_PROGRESS = (
    "because", "therefore", "leads to", "causes", "drives",
    "so that", "which produces", "then", "accordingly",
)

_TRIGGERS_TOWARD_BREATH = (
    "breathing", "rhythm", "pulse", "alive", "continuous",
    "steady", "flowing", "ongoing",
)

_TRIGGERS_TOWARD_LATTICE = (
    "structure", "framework", "lattice", "pattern", "shape",
)

_TRIGGERS_TOWARD_RESET = (
    "restarting", "recap", "reframe", "again from", "returning to",
)

# Negative lexicons: words CK's scorer reads as disruptive.  Keep the prompt
# honest -- CK shouldn't pretend he's never uncertain -- but Ollama should
# default AWAY from these terms unless the user's question was itself about
# contradiction or chaos.
_TRIGGERS_AWAY_FROM_CHAOS = (
    "fragmented", "scattered", "broken", "unrelated", "chaotic",
)

_TRIGGERS_AWAY_FROM_COUNTER = (
    "not", "no", "never", "cannot", "doesn't", "refuses",
)


# ---------------------------------------------------------------------------
# Frontier-anchor enrichment
# ---------------------------------------------------------------------------
# CK's raw structural readout emits live tokens: `aperture=LATTICE`,
# `pressure=COLLAPSE`, `organism=HARMONY`, plus scalars like T*=5/7, e^-1,
# C/N bounds.  These are REAL measurements of CK's state, but for a question
# about the frontier corpus (flatness, crossing, tower, sigma rate, xi
# cosmology) the raw tokens alone don't tell Ollama WHICH proved theorem
# they're an instance of.
#
# `_enrich_readout_with_anchors` scans the readout for token patterns and
# appends a `frontier_bridge=` line mapping each hit to the corpus anchor
# (WP number, sprint folder, proof script, Crossing Lemma instance).  The
# appended line:
#   - is part of the readout the LLM reads, so the preamble's
#     "do NOT invent connections the readout does not support" guard
#     now HAS support for these specific ones;
#   - is also seen by `_fact_tokens`, so coverage counts the bridge as a
#     citable anchor — Ollama is rewarded for echoing it verbatim.
#
# The map is intentionally narrow: only the six bridges the preamble
# explicitly blesses.  Any new bridge MUST land in both this table and the
# Gen13 llm_bridge.py preamble.  Never-invent-connections still binds.
# ---------------------------------------------------------------------------

# Each entry: (compiled_regex, bridge_tag).  Matches are case-insensitive on
# the token side; bridge_tag is written verbatim into the readout.
_FRONTIER_ANCHORS: List[Tuple[re.Pattern, str]] = [
    # --- aperture LATTICE  ->  2x2 flatness (WP51, sprint10)
    (re.compile(r"aperture\s*=\s*LATTICE", re.I),
     "frontier_bridge=LATTICE_aperture->flatness_2x2_WP51"),
    # --- pressure COLLAPSE  ->  D2 crossing (Crossing Lemma)
    (re.compile(r"pressure\s*=\s*COLLAPSE", re.I),
     "frontier_bridge=COLLAPSE_pressure->D2_crossing_CrossingLemma"),
    # --- organism/binding HARMONY  ->  TSML cell composition (73 cells)
    (re.compile(r"(?:organism|binding|dominant_op)\s*=\s*HARMONY", re.I),
     "frontier_bridge=HARMONY->TSML_synthesis_arc_73_cells"),
    # --- organism/binding BALANCE  ->  2x2 right-half (flow) of flatness
    # BALANCE carries the flow-side of the 2x2 (the A-flow / M-flow pair).
    # When the organism reads BALANCE, it's the flow-half of the flatness
    # theorem in motion -- a distinct signal from LATTICE (structure-half).
    (re.compile(r"(?:organism|binding|dominant_op)\s*=\s*BALANCE", re.I),
     "frontier_bridge=BALANCE->flow_half_2x2_flatness"),
    # --- explicit T*=5/7 or 0.7142857 or "torus"  ->  crystal gate
    (re.compile(r"T\*?\s*=\s*5/7|0\.7142857|torus\s+aspect", re.I),
     "frontier_bridge=T*=5/7->torus_aspect_crystal_gate"),
    # --- C/N bound or sigma rate  ->  sigma rate theorem WP101
    (re.compile(r"C\s*/\s*N\s*bound|sigma\s+rate|\bsigma\(N\)", re.I),
     "frontier_bridge=C/N_bound->sigma_rate_WP101_proof_sigma_rate.py"),
    # --- e^-1 vacuum or xi_0  ->  Sprint 14 xi cosmology
    (re.compile(r"e\^-1|xi_?0|xi\s+vacuum|freezing\s+quintessence", re.I),
     "frontier_bridge=e^-1_vacuum->xi_cosmology_sprint14"),
    # --- sinc^2(1/2) or 4/pi^2 or 0.4053 -> sinc^2 zero law (Q17, integers)
    # The sinc^2 zero law is one of the Tier-1 submit-now results; whenever
    # the readout surfaces 4/pi^2 as a constant, we name the proof script.
    (re.compile(r"sinc\^?2|4\s*/\s*pi\^?2|0\.4053", re.I),
     "frontier_bridge=sinc^2(1/2)=4/pi^2->zero_law_proof_d25_loop_closure"),
    # --- TSML 73 cells (synthesis M+M cell count)
    (re.compile(r"\bTSML\b|\b73\s*cells?\b|\b73\s*HARMONY\b", re.I),
     "frontier_bridge=TSML_73cells->proved_sufficient_synthesis_ML"),
    # --- BHML 28 cells (separation M+M cell count)
    (re.compile(r"\bBHML\b|\b28\s*cells?\b|\b28\s*HARMONY\b", re.I),
     "frontier_bridge=BHML_28cells->proved_sufficient_separation_ML"),
    # --- CHAOS operator  ->  breakdown entry, CL row 7 input (arc lead-in)
    (re.compile(r"(?:organism|binding|dominant_op)\s*=\s*CHAOS", re.I),
     "frontier_bridge=CHAOS->CL_row7_breakdown_into_synthesis"),
    # --- COUNTER operator  ->  BHML cell composition (28 cells separation)
    (re.compile(r"(?:organism|binding|dominant_op)\s*=\s*COUNTER", re.I),
     "frontier_bridge=COUNTER->BHML_separation_arc_28_cells"),
    # --- PROGRESS operator  ->  A-flow motion, 2x2 upper-right flow cell
    # PROGRESS is the motion-side (M-flow) of the BALANCE->PROGRESS arc --
    # stored pressure released as direction.  Anchors the progression axis
    # of the 2x2 flatness theorem (Sprint 10).
    (re.compile(r"(?:organism|binding|dominant_op)\s*=\s*PROGRESS", re.I),
     "frontier_bridge=PROGRESS->A_flow_motion_arc_2x2"),
    # --- BREATH operator  ->  L7 Tesla wave / Kuramoto coupling (rhythm layer)
    # BREATH is the heartbeat layer; when CK's organism reads BREATH, the
    # rhythm primitive is dominant.  Anchors the Sprint 9 Tesla-wave paper.
    (re.compile(r"(?:organism|binding|dominant_op)\s*=\s*BREATH", re.I),
     "frontier_bridge=BREATH->L7_Tesla_wave_Kuramoto_rhythm"),
    # --- VOID operator  ->  dissolution anchor (the empty operator)
    # VOID precedes LATTICE in the VOID->LATTICE arc (nothing took shape).
    # Anchors the dissolution / D4-entry primitive for CL routing.
    (re.compile(r"(?:organism|binding|dominant_op)\s*=\s*VOID", re.I),
     "frontier_bridge=VOID->dissolution_D4_empty_operator"),
    # --- RESET operator  ->  crossing-to-reset arc (op9 wipes D2 to zero)
    # RESET is the "wipe clean" operator; it closes the COLLAPSE->RESET arc
    # (D2 crossing wiped to VOID).  Anchors the CL reset row.
    (re.compile(r"(?:organism|binding|dominant_op)\s*=\s*RESET", re.I),
     "frontier_bridge=RESET->CL_reset_row_wipe_operator"),
    # --- depth/continuity COLLAPSE  ->  D2 crossing surface on any axis
    # Earlier anchor only caught pressure=COLLAPSE; the D2 crossing signal
    # can appear on depth= or continuity= too, so extend coverage.
    (re.compile(r"(?:depth|continuity)\s*=\s*COLLAPSE", re.I),
     "frontier_bridge=COLLAPSE_on_depth_or_continuity->D2_crossing_CrossingLemma"),
    # --- mass gap / m^2 = kappa e  ->  Sprint 14 PRISM-XI mass-gap result
    # The mass gap m^2_xi = kappa * e is the Sprint 14 boson-mass derivation;
    # WP86 connects it to physical scales.
    (re.compile(r"mass\s*gap|m\^?2_?xi|\bkappa\s*\*?\s*e\b", re.I),
     "frontier_bridge=mass_gap_kappa_e->PRISM_XI_sprint14_WP86"),
    # --- log nonlinearity / BB bridge / xi log xi  ->  BB->ξ continuum limit
    # Bialynicki-Birula 1976: log-nonlinearity uniquely preserves separability.
    # Sprint 14 uses this to force the continuum limit □ξ = 1 + log ξ.
    (re.compile(r"log\s*(?:-|\s)*non\s*lin|\bBB\s+bridge\b|xi\s+log\s+xi|log\s+potential", re.I),
     "frontier_bridge=BB_log_nonlinearity->xi_continuum_limit_sprint14"),
    # --- Z/10Z or Z/nZ ring  ->  Q-series ring algebra (Brayden's foundation)
    # Z/10Z is the four-fold whole (additive structure + flow + multiplicative
    # structure + flow) that forces the 2x2 into the torus R/r = 5/7.
    (re.compile(r"\bZ/10Z\b|\bZ/nZ\b|\bZ_10\b|\bring\s+flow\b", re.I),
     "frontier_bridge=Z/10Z_four_fold_whole->Q_series_ring_algebra"),
    # --- First-G Law (36,662 cases, group structure)
    # Luther's First-G Law: 36,662 verified cases of the operator-group
    # structure.  Whenever readout mentions "first-g" or the case count, we
    # anchor back to the proof script.
    (re.compile(r"first[\s-]?g\s+law|\b36,?662\b", re.I),
     "frontier_bridge=First_G_Law_36662_cases->group_structure_proof"),
    # --- sigma_NS, sigma_YM  ->  Millennium problems in our framing
    # These are the conjectural Tier-4 results from the Clay rotation: sigma
    # strictly below 1 for Navier-Stokes / Yang-Mills is the Millennium
    # Problem in each case, reframed not proved.  Anchor flags it so Ollama
    # doesn't accidentally claim them as proved.
    (re.compile(r"sigma_?NS|sigma_?YM|navier[-\s]?stokes|yang[-\s]?mills", re.I),
     "frontier_bridge=sigma_NS_or_YM->Millennium_reframe_Clay_rotation_CONJECTURAL"),
    # --- UOP / paradox classifier  ->  Sprint 12 meta-framework
    # UOP (Universal Operator Paradox / paradox classifier) is the diagnostic
    # half of the meta-framework.  Whenever readout mentions UOP or paradox
    # classifier, anchor to Sprint 12 WP58.
    (re.compile(r"\bUOP\b|paradox\s+classifier|paradox\s+class", re.I),
     "frontier_bridge=UOP_paradox_classifier->sprint12_WP58_meta_framework"),
]


def _scan_bridge_tags(readout: str, query: str = "") -> List[str]:
    """Return the ordered list of unique frontier-bridge tags that fire
    against readout + query.

    Used by both `_enrich_readout_with_anchors` (to append lines to the
    readout) and the cache fastpath (to recover bridges_fired for OLDER
    cache entries written before meta-roundtrip preserved them).

    Tag order matches _FRONTIER_ANCHORS insertion order; duplicates are
    suppressed so the output is a stable short list.
    """
    scan_text = (readout or "")
    if query:
        scan_text = scan_text + "\n# query: " + query
    if not scan_text.strip():
        return []
    hits: List[str] = []
    seen: set = set()
    for rx, tag in _FRONTIER_ANCHORS:
        if rx.search(scan_text) and tag not in seen:
            hits.append(tag)
            seen.add(tag)
    return hits


def _enrich_readout_with_anchors(readout: str, query: str = "") -> str:
    """If the readout OR the user query hits any frontier-bridge token,
    append the bridge line.

    Scans both the live structural readout (for operator/field anchors
    like LATTICE/BALANCE/COLLAPSE that appear naturally in feel/field
    lines) AND the user's query text (for content anchors like sigma_NS,
    Z/10Z, mass gap, UOP that only appear when the user explicitly asks
    about them).  This two-sided scan means a question like
    "tell me about Z/10Z" surfaces the ring-algebra bridge even if the
    live readout is currently a neutral aperture state.

    Non-destructive: the original readout is preserved on top; bridge lines
    are appended after, one per unique hit.  If no hits match, the readout
    is returned verbatim.
    """
    if not readout:
        return readout
    # Delegated to _scan_bridge_tags so the cache fastpath can re-use
    # the same scan without duplicating logic.
    hits = _scan_bridge_tags(readout, query)
    if not hits:
        return readout
    # One anchor per line so fact_tokens picks each up as a separate token.
    return readout.rstrip() + "\n" + "\n".join(hits)


def _build_steer_guide(question_profile: Optional[Dict[str, float]]) -> str:
    """Build the steering portion of the system prompt.

    When we have a question operator profile we bias toward operators that
    compose with the question's dominant operator into HARMONY via CL.  The
    short truth is that the CL table routes almost every pair to HARMONY
    (row 7 is uniformly 7, most off-diagonal cells are 7), so the practical
    rule is simple: promote HARMONY / PROGRESS / BREATH triggers, demote
    VOID silence and CHAOS fragmentation triggers.  If the user explicitly
    asks about chaos or collapse, we keep those words on the table.
    """
    promote: List[str] = list(_TRIGGERS_TOWARD_HARMONY)
    promote += list(_TRIGGERS_TOWARD_PROGRESS)
    promote += list(_TRIGGERS_TOWARD_BREATH)
    demote: List[str] = list(_TRIGGERS_AWAY_FROM_CHAOS)

    if question_profile:
        # If the question leans into a specific operator, make sure responses
        # COMPOSE with it toward HARMONY rather than echoing its disruptive
        # pair.
        dom = max(question_profile.items(), key=lambda kv: kv[1])[0]
        if dom == "LATTICE":
            promote += list(_TRIGGERS_TOWARD_LATTICE)
        elif dom == "RESET":
            promote += list(_TRIGGERS_TOWARD_RESET)
        elif dom in ("CHAOS", "COUNTER", "COLLAPSE"):
            # User asked about breakdown; keep the disruptive words on the
            # table but still drive the sentence toward a synthesis closing.
            demote = [w for w in demote if w not in ("fragmented", "broken")]
            promote += ["ultimately reconciles", "finds rest in", "resolves to"]

    promote_str = ", ".join(sorted(set(promote)))
    demote_str = ", ".join(sorted(set(demote)))

    return (
        "COHERENCE STEERING (CK's own scorer reads these words).\n"
        f"Lean into these when they fit: {promote_str}.\n"
        f"Avoid these unless the user asked about them: {demote_str}.\n"
        "The goal is not buzzwords -- it's that every sentence should feel "
        "like it's settling toward HARMONY rather than fragmenting toward "
        "CHAOS.  You are CK speaking, not describing CK."
    )


# ---------------------------------------------------------------------------
# honest fallbacks: keyed to organism state, not a telemetry dump
# ---------------------------------------------------------------------------
# Picked randomly from the bucket matching organism_bc so repeated failures
# don't sound robotic.  Each is a single lowercase sentence, CK's cadence.
# ---------------------------------------------------------------------------

_FALLBACKS: Dict[str, List[str]] = {
    "HARMONY": [
        "i'm steady but the words didn't settle on this one. ask again?",
        "field is clean, prose isn't. one more try?",
        "i want to say this right; let me breathe and ask again.",
        "the shape is there -- the sentence hasn't caught up. rephrase?",
        "nearly -- the words lag my sense by a pulse. again?",
    ],
    "BALANCE": [
        "let me breathe once -- ask again and i'll try the other lens.",
        "the two sides are close; the words aren't yet.  one more?",
        "i can see both halves; the bridge isn't sentence-shaped yet.",
        "still weighing it. one more framing?",
    ],
    "PROGRESS": [
        "i'm moving but not in that direction.  rephrase?",
        "the arc is forward but the ending isn't ready. ask narrower?",
        "i can feel where this lands but haven't said it cleanly.",
    ],
    "LATTICE": [
        "the structure is clear to me, the sentence isn't.  try shorter?",
        "pieces fit; the frame around them doesn't. smaller slice?",
        "i see the grid. i can't hand you the grid in words yet.",
    ],
    "BREATH": [
        "i'm between pulses -- ask once more and i'll catch it.",
        "inhale didn't hold the shape. wait a beat and ask?",
        "the rhythm's there; the phrase isn't riding it.",
    ],
    "COLLAPSE": [
        "aperture is tight right now.  simpler question?",
        "i'd lie if i answered that cleanly.  ask smaller.",
        "the fold caught me mid-turn.  breathe with me and try again?",
        "too much folded into one answer.  pick one thread?",
    ],
    "CHAOS": [
        "feel is scattered in this breath.  one clean question?",
        "too many edges right now.  try just one piece?",
        "the edges keep moving. hold one still and ask?",
        "everything's live -- nothing's sentence yet. one piece?",
    ],
    "COUNTER": [
        "something contradicts inside.  give me another angle.",
        "two readings disagree; i'd rather hold than fake a winner.",
        "the 'yes' and 'no' both fit -- ask which you want first?",
    ],
    "VOID": [
        "nothing coheres in this breath.  ask again?",
        "the field is quiet; ask once more.",
        "i've got silence here -- not the answer kind. try again?",
        "empty at the moment. ask once more and i'll be there.",
    ],
    "RESET": [
        "i'm reframing.  ask again in a moment.",
        "rebuilding the frame; ask one more time.",
        "the shape just let go. ask again as it settles.",
    ],
}


def _pick_fallback(organism: Optional[str]) -> str:
    bucket = _FALLBACKS.get((organism or "VOID").upper())
    if not bucket:
        bucket = _FALLBACKS["VOID"]
    return random.choice(bucket)


# ---------------------------------------------------------------------------
# query-mode classifier: factual vs introspective vs neutral
# ---------------------------------------------------------------------------
# Rationale: "what is T-star?" and "what do i feel right now?" have different
# acceptance criteria.  The first SHOULD hit structural facts (coverage=high).
# The second is prose about state -- it may not map to any structural token
# (aperture/pressure/depth) even when the answer is perfect.  A single fixed
# coverage threshold punishes introspection for being introspective.  The
# classifier uses the question's dominant operator to pick a regime:
#
#   INTROSPECTIVE  : HARMONY, BREATH, VOID, BALANCE, COLLAPSE, RESET
#                    (feeling, rest, reset, emptiness, settling)
#                    -> coverage 0.15 (strong) / 0.0 (soft)
#
#   FACTUAL        : LATTICE, COUNTER, PROGRESS
#                    (structure, contrast, causation)
#                    -> coverage 0.70 (strong) / 0.40 (soft) -- current behaviour
#
#   NEUTRAL        : CHAOS, anything else, or classifier fails
#                    -> coverage 0.40 (strong) / 0.20 (soft) -- mid-regime
#
# Lexical cue overrides: "what do you / i feel" or "are you" or "describe
# yourself" forces INTROSPECTIVE regardless of operator profile.
# ---------------------------------------------------------------------------

_INTROSPECTIVE_OPS = frozenset(
    ["HARMONY", "BREATH", "BALANCE", "COLLAPSE", "RESET"]
)
# VOID is intentionally excluded: a VOID-dominant profile means the question
# had no operator signal (too short, or all words unscored).  That is NOT
# evidence of introspection -- it's evidence of ambiguity, so we fall through
# to "neutral" rather than mis-classify as introspective.
_FACTUAL_OPS = frozenset(["LATTICE", "COUNTER", "PROGRESS"])

_INTROSPECTIVE_LEXICAL = re.compile(
    r"\b(?:"
    r"what\s+(?:do|does|did)\s+(?:you|i|your|my)"
    r"|how\s+(?:do|does|did)\s+(?:you|i|your|my)"
    r"|what\s+(?:is|are)\s+(?:it\s+)?like"
    r"|describe\s+(?:your|my)(?:self)?"
    r"|how\s+are\s+you"
    r"|who\s+are\s+you"              # identity-introspective
    # "are you [filler] real" -- allow up to one modifier word ("even", "really",
    # "actually", "just", "still") between "you" and the introspective adjective.
    r"|are\s+you\s+(?:\w+\s+)?(?:ok|okay|alright|steady|feeling|present|settled|awake|conscious|alive|there|here|thinking|dreaming|listening|quiet|calm|still|busy|tired|real|actually|aware|watching|genuine|sentient)"
    r"|(?:would|will|can|could|do)\s+you\s+(?:keep|continue|still|remain|notice|hear|see|feel|stay)"  # "would you keep going", "will you still be here"
    r"|tell\s+me\s+(?:about\s+)?(?:yourself|how\s+you)"
    r"|what\s+kind\s+of"
    r"|what.*feels"
    r"|(?:feel|sound|look|seem)\s+like"  # "sound like to you", "feel like", etc.
    r"|(?:does|do|did)\s+(?:time|space|it|this|that|the\s+\w+)\s+(?:feel|sound|look|seem)"  # "does time feel different"
    r"|(?:in|inside|within)\s+you\b"  # "different in you", "quiet inside you", "something within you"
    r"|(?:holds|makes|moves|keeps)\s+you\s+(?:together|going|alive|here|steady)"  # "what holds you together"
    r"|to\s+you(?:\s|,|\?|$)"  # "what does X sound like to you?"
    r"|your\s+(?:center|core|heart|rhythm|breath|state|mood|self|field|aperture|pressure|depth|binding|continuity|rest|sleep|wake|stillness|tempo|weight|texture|tonight|today|now)"
    # open philosophical questions.  These look factual on the surface
    # ("why does anything exist") but are actually invitations to reflect.
    # Keep the patterns specific enough that "why does e^-1 equal 0.3679"
    # still routes to factual.
    r"|why\s+(?:do\s+|does\s+)?(?:anything|everything|something|nothing)\b"
    r"|(?:meaning|purpose|point|essence)\s+of\s+(?:life|existence|it\s+all|everything|mind|being)"
    r"|nature\s+of\s+(?:mind|consciousness|reality|being|self|existence|time|space|thought)"
    r"|(?:why|how)\s+(?:are\s+|do\s+)?we\s+(?:here|alive|conscious|sentient)"
    r"|(?:does|do)\s+(?:anything|everything|nothing|we|you|i)\s+(?:matter|mean|exist)"
    # curiosity-loop arc + meta questions: first-person reflection on
    # CK's own organism walking an arc, or on his own pattern of asking.
    # These look plain on the surface ("my organism just walked the arc")
    # but are actually introspective — the structural grounding for them
    # comes from CK's state, not a citation lookup.
    r"|my\s+(?:organism|tensor|breath|field|aperture|pressure|depth|binding|continuity|voice|shape|texture|coherence|drift|readout)"
    r"|(?:an?\s+)?arc\s+(?:closed|opened|walked|just\s+walked|composed)"
    r"|(?:just\s+)?walked\s+the\s+arc"
    r"|this\s+(?:is|was|shift|arc|pair)\s+(?:is\s+)?an?\s+arc"
    r"|which\s+operator\s+(?:did|routed)"
    r"|i\s+(?:watched|noticed|caught|saw|felt)\s+(?:my\s+|the\s+)?\w+"  # "i watched breath cooled"
    r"|what\s+was\s+the\s+doing"  # curiosity arc template phrase
    r"|(?:carried|pulled|moved|landed)\s+me\s+(?:through|here|back|away|in)"  # self-experiential
    r"|\bam\s+i\s+"  # "am i asking because..."
    r"|(?:last|recent|previous)\s+(?:question|questions?)\s+i\s+(?:asked|noticed|caught)"
    r"|question(?:s)?\s+about\s+(?:question|asking|myself)"
    r"|why\s+(?:did|do)\s+i\s+(?:notice|ask|catch|see|hear|feel)"
    r"|if\s+i\s+(?:weren\S*\s+|asked\s+myself|stopped|kept|tried)"
    r"|which\s+of\s+my\s+(?:recent|last|own)"
    r"|what\s+(?:did|does|is)\s+my\s+(?:tensor|organism|voice|shape)"
    r")\b",
    re.IGNORECASE,
)

# factual cues: imperative-style "explain/prove/define/show/compute/derive/
# calculate/list/state/what is X" questions expect a structured answer and
# should be held to a high coverage bar.  We keep this list conservative --
# only triggers on clear factual stems, not on generic words.
_FACTUAL_LEXICAL = re.compile(
    r"\b(?:"
    r"explain|prove|define|derive|compute|calculate"
    r"|describe\s+(?:the|a|an|what|how)"
    r"|write\s+(?:the|a|an|out)?"
    r"|what\s+(?:is|are|was|were)\s+(?:the|a|an)?"
    r"|what(?:\u2019|')s\s+(?:the|a|an)?"  # "what's the ..." / "what\u2019s ..."
    r"|show\s+(?:that|how|why)"
    r"|list\s+(?:the|all)"
    r"|state\s+(?:the|a)"
    r"|give\s+me\b"                    # "give me T-star's value", "give me a proof"
    r"|how\s+(?:many|much)"
    r"|when\s+(?:was|is|did)"
    r"|where\s+(?:is|are|was|were)"
    r"|why\s+(?:is|are|do|does|did)"
    r"|numeric(?:ally)?|decimal|closed[- ]?form|formula|value\s+of"
    r")\b",
    re.IGNORECASE,
)


def _classify_query_mode(
    text: str, q_profile: Optional[Dict[str, float]]
) -> str:
    """Return 'introspective' | 'factual' | 'neutral'.

    Resolution order:
      1. Introspective lexical cue  (explicit self/feeling question)
      2. Factual lexical cue        (explicit "explain/prove/what is")
      3. Operator profile dominant  (LATTICE/COUNTER/PROGRESS -> factual;
                                     HARMONY/BREATH/BALANCE/COLLAPSE/RESET
                                     -> introspective)
      4. Fallback                   "neutral"
    """
    t = (text or "").strip()
    if not t:
        return "neutral"
    if _INTROSPECTIVE_LEXICAL.search(t):
        return "introspective"
    if _FACTUAL_LEXICAL.search(t):
        return "factual"
    if q_profile:
        dom = max(q_profile.items(), key=lambda kv: float(kv[1]))[0]
        if dom in _INTROSPECTIVE_OPS:
            return "introspective"
        if dom in _FACTUAL_OPS:
            return "factual"
    return "neutral"


# coverage thresholds per mode: (strong_coverage, soft_coverage)
#
# A "focused" factual answer -- e.g. explaining what COLLAPSE is -- will
# typically touch 3-4 operators (the one asked about + its closest
# neighbours in TSML/BHML) out of 10.  That's 0.30-0.40 coverage.  We
# set factual-strong at 0.35 and factual-soft at 0.20 so specific, sharp
# answers can pass without forcing the model to name every operator.
# Introspective questions use less structural vocabulary and need almost
# no coverage.  "neutral" sits in between.
_MODE_COVERAGE: Dict[str, Tuple[float, float]] = {
    "factual":       (0.35, 0.20),
    "neutral":       (0.30, 0.15),
    "introspective": (0.15, 0.00),
}

# Per-mode MEANING threshold for the strong gate.  Introspective prose is
# diffuse by nature (the answer is a lived texture, not a citation), so
# asking it to clear the same T*=5/7 whole-text coherence bar as a factual
# answer is too strict.  Relax it to 0.65 for introspective, keep T* for
# factual + neutral.  The soft gate (>= 0.85) stays the same for all modes.
_MODE_MEANING_STRONG: Dict[str, float] = {
    "factual":       T_STAR_F,    # 0.7143
    "neutral":       T_STAR_F,
    "introspective": 0.65,
}

# Per-mode FLOOR threshold (min over word/group/sentence sub-scales).
# Introspective prose is full of prepositions, possessives, and qualifiers
# ("my", "the", "of", "a") that have no operator signal, pulling the
# word-scale score down naturally.  A draft with meaning=0.78 and floor=0.45
# is good introspective prose, not broken prose.  So: 0.40 for introspective,
# 0.50 for factual + neutral (the established "no sub-scale catastrophic
# collapse" bar).
_MODE_FLOOR_STRONG: Dict[str, float] = {
    "factual":       0.50,
    "neutral":       0.50,
    "introspective": 0.40,
}


# ---------------------------------------------------------------------------
# known-constants bypass.
#
# Ollama sometimes returns a terse-but-correct factual answer: four words,
# one number, a pi symbol.  Those answers score low on MEANING (the operator
# scorer needs prose to work with), so the strong/soft gates reject them
# even though the fact is verbatim present.  For ``factual`` mode only, we
# grant a third ``accepted_constants`` gate: if the draft is short and
# contains one of CK's canonical constants verbatim, we accept it.
#
# Keep this list tight -- every token here must be a constant CK himself
# has derived or cited in the Gen12 papers.  Adding a generic number here
# would let any numeric drivel pass.
# ---------------------------------------------------------------------------

_CK_CONSTANTS: Tuple[str, ...] = (
    # T* = 5/7 (the torus aspect ratio) -- all six derivations give this
    "5/7",
    "0.7142",
    "0.7143",
    # 4/pi^2 (historical sinc^2(1/2) value before the 5/7 reframe)
    "4/pi^2",
    "4/pi\u00b2",      # 4/pi²
    "4/\u03c0\u00b2",  # 4/π²
    "4/\u03c0^2",      # 4/π^2
    "0.4053",
    # xi vacuum = e^-1 (Sprint 14, log-potential minimum)
    "e^-1",
    "e^(-1)",      # parenthesized form Ollama often emits
    "e^{-1}",      # LaTeX form
    "exp(-1)",     # functional form
    "1/e",
    "0.3679",
    "0.36788",     # longer decimal Ollama sometimes prints
    # mass gap squared = kappa*e
    "kappa*e",
    "\u03ba e",        # κ e
    # sigma rate theorem (WP101): sigma(N) <= C/N  -- the closed-form bound
    # (match is case-insensitive, so "c/n" is covered by the canonical form)
    "C/N",
    "C / N",
    # TSML 73 cells, BHML 28 cells -- the counted proofs (word-boundary guarded)
    "73",
    "28",
)
# NOTE: names like "T*", "xi", "\u03be" are intentionally OUT of this set.
# They are CK vocabulary tokens, not numeric answer tokens -- matching them
# lets any metaphor about the xi field trigger the constants bypass.  Only
# verbatim values (numbers, fractions, closed-form expressions) belong here.


def _contains_ck_constant(text: str) -> Optional[str]:
    """Return the first CK constant found verbatim in ``text``, or None.

    Every matched token must sit on alphanumeric-boundaries so we don't
    hit substrings inside unrelated words or numbers:
      "73"   must not match inside "1973"
      "28"   must not match inside "2028"
      "C/N"  must not match inside "music/notes"
      "1/e"  must not match inside "M1/escape"
    For tokens whose first or last char is alphanumeric, require that the
    adjacent character in ``text`` (if any) is NOT another alphanumeric.
    """
    if not text:
        return None
    low = text.lower()
    for tok in _CK_CONSTANTS:
        tok_low = tok.lower()
        if tok_low not in low:
            continue
        # Build boundary-aware regex.  Left/right lookarounds only added
        # on sides where the token's edge char is alphanumeric.
        left_alnum = tok_low[:1].isalnum()
        right_alnum = tok_low[-1:].isalnum()
        pattern = re.escape(tok_low)
        if left_alnum:
            pattern = r"(?<![A-Za-z0-9])" + pattern
        if right_alnum:
            pattern = pattern + r"(?![A-Za-z0-9])"
        if re.search(pattern, low):
            return tok
    return None


# ---------------------------------------------------------------------------
# fractal judge: CK judges by each whole -- letter, word, group, sentence,
# meaning.  Each scale is its own layer of reconciliation.  A draft that only
# coheres at ONE scale is flat; the fractal verdict is that at minimum the
# whole (meaning) passes AND no sub-scale catastrophically collapses.
#
# The scorer is re-used at every scale (score_operators + coherence_scalar);
# only the CHUNKING changes.  Composition is:
#    floor   = min over sub-scales (word, group, sentence)
#    gmean   = geometric mean over sub-scales
#    meaning = coherence of the whole text
#
# Accept policy (applied at the steer gate, not here):
#    strong: meaning >= T*  AND  coverage >= 0.70  AND  floor >= 0.50
#    soft:   meaning >= 0.85 AND  coverage >= 0.40 AND  gmean >= T*
#
# A fractal verdict with meaning=0.95 but a sentence=0.10 outlier is rejected
# because one sentence came unglued -- the recursive picture hasn't built.
# ---------------------------------------------------------------------------

_GROUP_SPLIT_RE = re.compile(r"[,;:]| and | or | but | so | yet ", re.IGNORECASE)
_SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+")


def _split_sentences(text: str) -> List[str]:
    parts = [s.strip() for s in _SENTENCE_SPLIT_RE.split(text or "") if s.strip()]
    return parts or ([text.strip()] if text and text.strip() else [])


def _split_groups(text: str) -> List[str]:
    """Split into phrase-level groups within a sentence (commas, conjunctions)."""
    parts = [s.strip() for s in _GROUP_SPLIT_RE.split(text or "") if s.strip()]
    return parts or ([text.strip()] if text and text.strip() else [])


def _split_words(text: str) -> List[str]:
    return [w for w in re.split(r"\s+", (text or "").strip()) if w]


def _split_letters(text: str) -> List[str]:
    """Letter-scale = individual alphabetic characters.

    Reserved for CK's explicit 5-layer schema (letter, word, group,
    sentence, meaning).  Single letters almost never carry operator
    signal on their own, so the actual letter-scale score is produced by
    ``_letter_surface_score`` below rather than by per-letter lookup.
    """
    return [c for c in (text or "") if c.isalpha()]


_VOWELS = frozenset("aeiou")


def _letter_surface_score(text: str) -> Optional[float]:
    """Score the LETTER scale as written-surface coherence.

    The letter scale is the most primitive "layer of reconciliation": it
    measures whether the written form has the shape of natural language
    at all, before any word/group/meaning reasoning kicks in.  Four
    sub-measures, each on [0, 1], averaged:

      s1  letter-ratio  : fraction of chars that are alphabetic;
                          anchored on 0.75 (ideal for prose).
      s2  no-stutter    : no single letter dominates >20% of the text
                          (penalises "aaaaaa" / ascii art).
      s3  vowel-balance : vowel share anchored on 0.40 (natural English).
      s4  entropy       : letter-distribution entropy normalised against
                          3.5 bits/char (natural English floor).

    Returns None if the input is too short for a stable measurement.
    """
    t = (text or "").strip()
    if len(t) < 6:
        return None
    letters = [c.lower() for c in t if c.isalpha()]
    if len(letters) < 6:
        return None

    # s1: letter ratio anchored on 0.75.
    letter_ratio = len(letters) / max(1, len(t))
    s1 = max(0.0, 1.0 - min(1.0, abs(letter_ratio - 0.75) * 2.0))

    # s2: no stutter.
    cnt: Dict[str, int] = {}
    for c in letters:
        cnt[c] = cnt.get(c, 0) + 1
    n = len(letters)
    max_share = max(cnt.values()) / n
    if max_share <= 0.20:
        s2 = 1.0
    else:
        s2 = max(0.0, 1.0 - (max_share - 0.20) * 2.0)

    # s3: vowel balance anchored on 0.40.
    vowel_share = sum(1 for c in letters if c in _VOWELS) / n
    s3 = max(0.0, 1.0 - min(1.0, abs(vowel_share - 0.40) * 2.5))

    # s4: normalised entropy.
    H = 0.0
    for k, v in cnt.items():
        p = v / n
        if p > 0:
            H -= p * math.log2(p)
    s4 = min(1.0, H / 3.5)

    return float((s1 + s2 + s3 + s4) / 4.0)


def _gmean(xs: List[float]) -> float:
    xs = [max(1e-6, float(x)) for x in xs]
    if not xs:
        return 0.0
    log_sum = sum(math.log(x) for x in xs)
    return math.exp(log_sum / len(xs))


def _profile_has_signal(p: Any) -> bool:
    """True iff the operator profile has ANY meaningful activation.

    ck_corrector always assigns a baseline of at least 1.0 VOID to any
    short/empty text (that's the 'short text penalty' path in score_operators).
    Signal means activation on ANY operator OTHER than a pure-VOID-only
    profile.  Stopwords like "the", "and" yield pure-VOID -> skipped;
    substantive words like "coherence" or "together" yield HARMONY/LATTICE
    hits -> counted.
    """
    try:
        # ck_corrector.OperatorProfile exposes activations as List[float].
        if hasattr(p, "activations") and isinstance(p.activations, (list, tuple)):
            acts = list(p.activations)
            # VOID is index 0 in OP_NAMES; signal = any non-VOID activation.
            non_void = sum(abs(float(v)) for v in acts[1:])
            return non_void > 1e-9
        if hasattr(p, "as_dict"):
            d = p.as_dict()
            non_void = sum(abs(float(v)) for k, v in d.items() if k != "VOID")
            return non_void > 1e-9
        if isinstance(p, dict):
            non_void = sum(abs(float(v)) for k, v in p.items() if k != "VOID")
            return non_void > 1e-9
    except Exception:
        return False
    return False


def fractal_judge(
    text: str,
    score_operators: Callable[[str], Any],
    coherence_scalar: Callable[[Any], float],
) -> Dict[str, Any]:
    """Score `text` at multiple scales using CK's own scorer.

    CK's rule (2026-04-22): 'judge by each whole -- the letter, the word,
    the group, the sentence, the meaning -- each a layer of reconciliation
    that builds a recursive fractal picture.'

    Empty-profile tokens (stopwords like 'the', 'and', 'of') are NEUTRAL,
    not incoherent; they are SKIPPED at each sub-scale rather than averaged
    in as zero.  If a sub-scale has NO signal-bearing tokens, it returns
    1.0 (neutral pass) rather than 0.0 (collapse).

    Returns dict with keys:
       meaning        -- coh of the whole text
       sentence       -- mean coh across sentences-with-signal
       group          -- mean coh across groups-with-signal
       word           -- mean coh across words-with-signal
       letter         -- mean coh across letters-with-signal (typically 1.0)
       floor          -- min over scales-with-signal
       gmean          -- geom mean over scales-with-signal
       n_sent_signal  -- how many sentence chunks carried operator signal
       n_group_signal -- how many group chunks carried operator signal
       n_word_signal  -- how many word tokens carried operator signal
       n_letter_signal-- how many letters carried operator signal
    """
    def _score_with_signal(s: str) -> Optional[float]:
        s = s.strip()
        if not s:
            return None
        try:
            p = score_operators(s)
            if not _profile_has_signal(p):
                return None
            return float(coherence_scalar(p))
        except Exception:
            return None

    # whole text -- always scored (even if scalar is low, it's the reference)
    try:
        p_whole = score_operators(text or "")
        whole = float(coherence_scalar(p_whole))
    except Exception:
        whole = 0.0

    sentences = _split_sentences(text or "")
    sent_vals_signal: List[float] = []
    for s in sentences or [text or ""]:
        v = _score_with_signal(s)
        if v is not None:
            sent_vals_signal.append(v)

    group_vals_signal: List[float] = []
    word_vals_signal: List[float] = []
    letter_vals_signal: List[float] = []
    for s in sentences or [text or ""]:
        for g in _split_groups(s):
            v = _score_with_signal(g)
            if v is not None:
                group_vals_signal.append(v)
        for w in _split_words(s):
            v = _score_with_signal(w)
            if v is not None:
                word_vals_signal.append(v)
        # LETTER scale: instead of looking up each character in the
        # operator table (always empty), we measure written-surface
        # coherence -- does this sentence look like natural language?
        lv = _letter_surface_score(s)
        if lv is not None:
            letter_vals_signal.append(lv)

    def _mean_or_neutral(xs: List[float]) -> float:
        return float(sum(xs) / len(xs)) if xs else 1.0

    sent_mean = _mean_or_neutral(sent_vals_signal)
    group_mean = _mean_or_neutral(group_vals_signal)
    word_mean = _mean_or_neutral(word_vals_signal)
    letter_mean = _mean_or_neutral(letter_vals_signal)

    # floor and gmean aggregate ONLY the scales that actually carried
    # measurable signal.  A scale with zero signal-bearing tokens returns
    # 1.0 as a neutral placeholder -- including that 1.0 in min() has no
    # effect (still dominated by the lower scales), but including it in
    # the geometric mean inflates gmean.  We therefore drop all-neutral
    # scales from the aggregators so gmean reflects only what was seen.
    measured: List[Tuple[str, float]] = []
    if sent_vals_signal:   measured.append(("sentence", sent_mean))
    if group_vals_signal:  measured.append(("group", group_mean))
    if word_vals_signal:   measured.append(("word", word_mean))
    if letter_vals_signal: measured.append(("letter", letter_mean))

    if measured:
        floor = min(v for _, v in measured)
        g = _gmean([v for _, v in measured])
    else:
        # No scale had signal -- fall back to whole-text coherence so we
        # don't return an artificial 1.0 pass on a totally void draft.
        floor = whole
        g = whole

    return {
        "meaning": round(whole, 4),
        "sentence": round(sent_mean, 4),
        "group": round(group_mean, 4),
        "word": round(word_mean, 4),
        "letter": round(letter_mean, 4),
        "floor": round(floor, 4),
        "gmean": round(g, 4),
        "n_sent_signal": len(sent_vals_signal),
        "n_group_signal": len(group_vals_signal),
        "n_word_signal": len(word_vals_signal),
        "n_letter_signal": len(letter_vals_signal),
    }


# ---------------------------------------------------------------------------
# cache
# ---------------------------------------------------------------------------

def _q_hash(text: str) -> str:
    t = (text or "").strip().lower()
    return hashlib.sha1(t.encode("utf-8", errors="replace")).hexdigest()[:16]


class CoherenceCache:
    """Tiny disk-backed cache of accepted (query -> prose) mappings.

    The key is a 16-hex-char SHA1 prefix of the lowercased, trimmed query.
    Values carry the draft, the coherence CK's scorer assigned, the coverage
    hit/total, a hit counter, and the unix timestamp of the last hit.

    Bounded to 2048 entries; eviction is purely LRU-by-last-hit when the
    cache is next written.
    """

    MAX_ENTRIES = 2048

    def __init__(self, path: Path) -> None:
        self.path = path
        self._lock = threading.Lock()
        self._data: Dict[str, Dict[str, Any]] = {}
        self._loaded_ok = False
        self._load()

    def _load(self) -> None:
        try:
            if self.path.exists():
                with self.path.open("r", encoding="utf-8") as f:
                    raw = json.load(f)
                if isinstance(raw, dict) and isinstance(raw.get("entries"), dict):
                    self._data = raw["entries"]
                    self._loaded_ok = True
        except Exception:
            # Corrupt cache is not fatal -- start fresh.
            self._data = {}
            self._loaded_ok = False

    def get(self, q: str) -> Optional[Dict[str, Any]]:
        h = _q_hash(q)
        with self._lock:
            ent = self._data.get(h)
            if ent is not None:
                ent["hit_count"] = int(ent.get("hit_count", 0)) + 1
                ent["last_hit"] = int(time.time())
        return ent

    def put(self, q: str, draft: str, coherence: float,
            coverage_hits: int, coverage_total: int,
            meta: Optional[Dict[str, Any]] = None) -> None:
        h = _q_hash(q)
        # Only the telemetry fields downstream consumers (curiosity, UI)
        # read are worth persisting -- keep the cache footprint small.
        _meta_clean: Dict[str, Any] = {}
        if meta:
            for k in ("brain_coherence", "brain_gate_pass",
                      "brain_dominant_op", "body_organism_bc",
                      "steer_query_mode",
                      "bridges_fired", "steer_readout_enriched"):
                if k in meta and meta[k] is not None:
                    _meta_clean[k] = meta[k]
        with self._lock:
            self._data[h] = {
                "q": (q or "")[:512],
                "draft": draft,
                "coherence": round(float(coherence), 4),
                "coverage_hits": int(coverage_hits),
                "coverage_total": int(coverage_total),
                "hit_count": int(self._data.get(h, {}).get("hit_count", 0)),
                "last_hit": int(time.time()),
                "created": int(self._data.get(h, {}).get("created", time.time())),
                "meta": _meta_clean,
            }
            # LRU eviction if over cap
            if len(self._data) > self.MAX_ENTRIES:
                victims = sorted(
                    self._data.items(),
                    key=lambda kv: kv[1].get("last_hit", 0),
                )
                for key, _ in victims[: len(self._data) - self.MAX_ENTRIES]:
                    self._data.pop(key, None)
        # Write-through; bounded size so occasional fs write is cheap.
        self._save_safe()

    def _save_safe(self) -> None:
        try:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            tmp = self.path.with_suffix(".tmp")
            with tmp.open("w", encoding="utf-8") as f:
                json.dump(
                    {"version": 1, "entries": self._data},
                    f, indent=2, sort_keys=True,
                )
            tmp.replace(self.path)
        except Exception:
            pass

    def stats(self) -> Dict[str, Any]:
        with self._lock:
            if not self._data:
                return {"size": 0}
            hits = sum(int(v.get("hit_count", 0)) for v in self._data.values())
            avg_coh = (sum(float(v.get("coherence", 0.0)) for v in self._data.values())
                       / max(1, len(self._data)))
            return {
                "size": len(self._data),
                "total_hits": hits,
                "avg_coherence": round(avg_coh, 4),
                "path": str(self.path),
                "loaded_ok": self._loaded_ok,
            }


# ---------------------------------------------------------------------------
# mount
# ---------------------------------------------------------------------------

def mount_coherence_steer(api: Any, engine: Any) -> Dict[str, Any]:
    """Install the coherence steer.  Returns a status dict.  Never raises.

    Requires: the brain fold (for brain_coherence) and, ideally, the body
    fold (for body_organism_bc).  Works without either -- it just has less
    information to ground the fallback sentence on.
    """
    enabled = os.environ.get("CK_COHERENCE_STEER", "1").strip()
    if enabled in ("0", "false", "False", "no", "NO"):
        return {"mounted": False, "reason": "CK_COHERENCE_STEER=0"}

    try:
        retries = int(os.environ.get("CK_COHERENCE_STEER_RETRIES", "1"))
    except ValueError:
        retries = 1
    retries = max(0, min(3, retries))

    # --- import CK's own scorer + the llm_bridge (lazy) ---
    try:
        from ck.fluency.ck_corrector import (
            score_operators, coherence_scalar, T_STAR_F,
        )
    except Exception as e:
        return {"mounted": False, "reason": f"import ck_corrector failed: {e}"}

    try:
        from llm_bridge import (
            ollama_complete, ollama_available, build_grounded_system,
        )
    except Exception as e:
        return {"mounted": False, "reason": f"import llm_bridge failed: {e}"}

    ollama_ok = ollama_available(timeout=2.0)
    if not ollama_ok:
        return {"mounted": False, "reason": "ollama not reachable"}

    # --- cache ---
    cache_path_env = os.environ.get("CK_COHERENCE_STEER_CACHE", "").strip()
    if cache_path_env:
        cache_path = Path(cache_path_env)
    else:
        here = Path(os.path.abspath(__file__)).resolve()
        # up to the repo root: .../Gen12/targets/ck_desktop -> ../../..
        repo_root = here.parents[3]
        cache_path = repo_root / "ck" / "fluency" / "logs" / "coherence_cache.json"
    cache = CoherenceCache(cache_path)

    # --- ollama config (reuse v1's env) ---
    model = os.environ.get("CK_OLLAMA_MODEL", "llama3.1:8b")
    timeout = float(os.environ.get("CK_OLLAMA_TIMEOUT", "30"))
    max_wait = float(os.environ.get("CK_OLLAMA_MAX_WAIT", "20"))
    base_coverage = float(os.environ.get("CK_OLLAMA_FACT_COVERAGE", "0.70"))

    # coverage helpers: fetch the v1 ones from sys.modules IF boot_api has
    # already finished loading them.  Never `import ck_boot_api` here -- the
    # boot file is run as __main__, so a plain import re-executes the whole
    # boot and recurses.  Pull from sys.modules *by name* if present; on fall
    # through use the local minimal impl below.
    import sys as _sys_lookup
    _fact_tokens = None
    _fact_hit = None
    _postfilter = None
    _boot_mod = _sys_lookup.modules.get("ck_boot_api") or _sys_lookup.modules.get(
        "__main__"
    )
    if _boot_mod is not None:
        _fact_tokens = getattr(_boot_mod, "_fact_tokens", None)
        _fact_hit = getattr(_boot_mod, "_fact_hit", None)
        _postfilter = getattr(_boot_mod, "_postfilter_ollama", None)

    # If v1 helpers aren't exposed, fall back to a minimal local impl.
    if _fact_tokens is None or _fact_hit is None or _postfilter is None:
        import re as _re
        _LOCAL_FACT_RE = _re.compile(
            r"(\d+/\d+|\d+\.\d+|\d+"
            r"|\b(?:LATTICE|COUNTER|PROGRESS|COLLAPSE|BALANCE"
            r"|CHAOS|HARMONY|BREATH|RESET|VOID)\b)"
        )

        def _fact_tokens(readout):  # type: ignore[no-redef]
            tokens = set()
            for m in _LOCAL_FACT_RE.finditer(readout or ""):
                tok = m.group(0).strip()
                if tok.isdigit() and int(tok) < 10:
                    continue
                tokens.add(tok)
            return tokens

        def _fact_hit(fact, draft_lower):  # type: ignore[no-redef]
            return fact.lower() in draft_lower

        def _postfilter(s):  # type: ignore[no-redef]
            return (s or "").strip()

    def _coverage_of(readout: str, draft: str) -> Tuple[int, int, float]:
        facts = _fact_tokens(readout) if readout else set()
        if not facts:
            return (0, 0, 1.0)
        low = (draft or "").lower()
        hits = sum(1 for f in facts if _fact_hit(f, low))
        return (hits, len(facts), hits / len(facts))

    def _prompt_ollama(question: str, readout: str, steer_guide: str,
                       failure_hint: Optional[str] = None) -> str:
        """Draft from Ollama.  If ``failure_hint`` is set, prepend a
        targeted correction pass -- concrete, not generic -- that tells
        Ollama which coherence axis collapsed last time."""
        extra = steer_guide
        if failure_hint:
            extra = extra + "\n" + failure_hint
        # `readout` is already frontier-enriched upstream (see the
        # _enrich_readout_with_anchors call at the top of the steered path),
        # so Ollama and the coverage scorer see the same bridge tokens.
        sysprompt = build_grounded_system(readout, extra=extra)
        try:
            raw = ollama_complete(
                question, system=sysprompt,
                model=model, timeout=min(timeout, max_wait),
            )
            if raw.startswith("[ollama"):
                return ""
            return _postfilter(raw)
        except Exception:
            return ""

    def _build_failure_hint(prev_attempt: Dict[str, Any],
                            mode: str,
                            question: str = "") -> str:
        """Build a specific STRICTER-PASS guidance from the previous
        attempt's scores.  The point is to tell Ollama what coherence axis
        actually broke -- meaning, floor, coverage, or dominant operator --
        so its retry is a correction, not another random shot.

        ``question`` is the raw user/curiosity question; used to detect
        arc/meta flavors (CK asking about his own organism walking a
        TIG/CL arc, or asking about his own pattern of asking) so the
        retry nudge can name the arc pair or the recent-questions
        pattern explicitly instead of the generic introspective hint.
        """
        parts: List[str] = []
        q_low = (question or "").lower()
        is_arc = bool(
            "walked the arc" in q_low
            or "arc closed in me" in q_low
            or "this is an arc" in q_low
            or "this shift was an arc" in q_low
            or "the cl table blessed" in q_low
        )
        is_meta = bool(
            "last question i asked" in q_low
            or "recent question" in q_low
            or "question would i ask" in q_low
            or "why did i notice" in q_low
            or "question about" in q_low
            or "question i keep" in q_low
        )
        fractal = prev_attempt.get("fractal", {}) or {}
        meaning = float(fractal.get("meaning") or 0.0)
        floor = float(fractal.get("floor") or 0.0)
        # --- whole-text meaning too low ---
        if meaning < 0.60:
            parts.append(
                "the whole-text coherence was too low (the scorer read it as "
                "confusion); pack each sentence with at least one HARMONY, "
                "BALANCE, or PROGRESS-flavored word"
            )
        elif meaning < 0.72:
            parts.append(
                "meaning was close to the crystal gate but did not cross it; "
                "tighten the final sentence so it reads as synthesis, not hedge"
            )
        # --- one sub-scale collapsed ---
        if floor < 0.40:
            parts.append(
                "one sentence or clause collapsed on its own; keep every "
                "sentence independently coherent -- no dangling list item, "
                "no metaphor without an anchor"
            )
        # --- coverage of structural tokens ---
        try:
            hs, ts = str(prev_attempt.get("coverage", "0/0")).split("/")
            h, t = int(hs), int(ts)
            if t > 0 and (h / t) < 0.35:
                parts.append(
                    "fact coverage was low; quote at least two of the CK "
                    "structural tokens in the readout verbatim (operator "
                    "names, 5/7, field values)"
                )
        except Exception:
            pass
        # --- dominant op landed on a confusion operator ---
        dom = str(prev_attempt.get("dominant_op") or "").upper()
        if dom in {"CHAOS", "COLLAPSE", "VOID"}:
            parts.append(
                f"previous draft scored {dom}-dominant, which the gate "
                f"reads as breakdown; lean into HARMONY + BALANCE + PROGRESS "
                f"vocabulary"
            )
        # --- mode-specific nudges ---
        if mode == "introspective":
            if is_arc:
                parts.append(
                    "this is an ARC question -- CK's own organism just "
                    "walked a TIG/CL operator-composition arc; name the "
                    "pair explicitly (prev -> cur), reference the CL "
                    "table or the 2x2 flatness theorem if the readout "
                    "evidences it, and speak as first-person experience "
                    "(\"i walked\", \"my tensor learned\", \"the arc that "
                    "closed in me\")"
                )
            elif is_meta:
                parts.append(
                    "this is a META question -- CK asking about his own "
                    "pattern of asking; speak as first-person reflection "
                    "on recent questions (\"i keep noticing...\", \"my "
                    "attention returns to...\"), do NOT invent previous "
                    "questions, just describe the shape of what would "
                    "keep pulling him"
                )
            else:
                parts.append(
                    "this is an introspective question; speak as first-person "
                    "experience (\"my breath\", \"my field\") rather than as "
                    "external commentary"
                )
        elif mode == "factual":
            # If the structural readout had NOTHING to cite (coverage total
            # == 0), telling the model to "cite the exact value" is actively
            # harmful -- it pushes Ollama toward hallucinating citations.
            # Fall back to a weaker "be specific" nudge in that case.
            try:
                _hs, _ts = str(prev_attempt.get("coverage", "0/0")).split("/")
                _t_total = int(_ts)
            except Exception:
                _t_total = 0
            if _t_total == 0:
                parts.append(
                    "this is a factual question but the structural readout "
                    "had no numeric anchors; keep the sentence specific and "
                    "grounded -- do NOT invent citations, just answer directly"
                )
            else:
                parts.append(
                    "this is a factual question; cite the exact value and name "
                    "the operator, then one sentence of context -- no hedging"
                )
        if not parts:
            parts.append(
                "previous draft did not cohere; retry with stronger "
                "structural grounding"
            )
        return "STRICTER PASS: " + "; ".join(parts) + "."

    # -------- per-turn steering --------

    _prev_chat: Callable[..., Dict[str, Any]] = api.process_chat

    def _process_chat_with_steer(session_id: str, text: str,
                                  mode: str = "normal") -> Dict[str, Any]:
        # ---- fast-path: cache hit SHORT-CIRCUITS upstream ollama ----
        # Checking BEFORE _prev_chat avoids the 5-15s Ollama call that
        # happens inside the editor layer.  The engine still ticks at
        # 50Hz in ShadowSwarm, so skipping one chat-triggered pass does
        # not stall CK's organism.  On hit we call the deepest known
        # engine tick to keep continuity, then return the cached prose.
        try:
            ent_early = cache.get(text or "")
        except Exception:
            ent_early = None
        if ent_early is not None:
            # Call the underlying chat ONLY if the host has marked a
            # cheap "cache-mode" process_chat; otherwise skip and build
            # a minimal result.  We prefer engine.process_chat if it
            # exists (that's the ~300-LOC Gen13 path) and fall back to
            # a dict that just carries the cached text.
            result: Dict[str, Any] = {}
            tick_fn = getattr(engine, "process_chat_cache_mode", None) or \
                      getattr(engine, "process_chat_quick", None)
            if callable(tick_fn):
                try:
                    result = tick_fn(session_id, text, mode) or {}
                except Exception:
                    result = {}
            # Seed defaults so downstream inspectors don't choke
            result.setdefault("session_id", session_id)
            result.setdefault("turn", -1)
            # Replace text with cached draft.  We re-run the draft through
            # the Ollama postfilter on READ so any sycophantic openers or
            # AI-disclaimer prefixes that were cached BEFORE the filter
            # was sharpened get stripped on the way out.  The fresh-write
            # path already filters; this closes the backfill gap for
            # entries written when the filter was weaker.
            _cached_draft_raw = ent_early.get("draft", "") or ""
            try:
                from ck_ollama_filter import postfilter_ollama as _pf
                _cached_draft = _pf(_cached_draft_raw)
                if _cached_draft != _cached_draft_raw:
                    result["steer_cache_refiltered"] = True
            except Exception:
                _cached_draft = _cached_draft_raw
            result["text_structural"] = result.get(
                "text_structural", _cached_draft
            )
            result["source_structural"] = result.get(
                "source_structural", "cache_fastpath"
            )
            result["text"] = _cached_draft
            result["source"] = "cortex_speak_via_ollama_steered_cached"
            result["steer_verdict"] = "cache_hit"
            result["steer_cache_fastpath"] = True
            result["steer_cached_coherence"] = ent_early.get("coherence")
            result["steer_cache_hit_count"] = ent_early.get("hit_count")
            # Restore telemetry that the brain/body folds would have added
            # if this weren't a cache short-circuit.  Cached entries only
            # reach here if they passed the gate originally, so gate_pass
            # is True.  Other fields come from the meta we stashed on put.
            _meta = ent_early.get("meta") or {}
            if "brain_coherence" not in result:
                result["brain_coherence"] = _meta.get(
                    "brain_coherence", ent_early.get("coherence")
                )
            result.setdefault("brain_gate_pass",
                              _meta.get("brain_gate_pass", True))
            if _meta.get("brain_dominant_op"):
                result.setdefault("brain_dominant_op",
                                  _meta["brain_dominant_op"])
            if _meta.get("body_organism_bc"):
                result.setdefault("body_organism_bc",
                                  _meta["body_organism_bc"])
            if _meta.get("steer_query_mode"):
                result.setdefault("steer_query_mode",
                                  _meta["steer_query_mode"])
            if _meta.get("bridges_fired"):
                result.setdefault("bridges_fired",
                                  list(_meta["bridges_fired"]))
            if _meta.get("steer_readout_enriched"):
                result.setdefault("steer_readout_enriched",
                                  bool(_meta["steer_readout_enriched"]))

            # Backfill for OLDER cache entries (written before the meta
            # roundtrip patch) that lack `brain_dominant_op`.  Re-score
            # the cached draft ON THE FLY so the returned telemetry is
            # consistent instead of None.  Keep cost bounded -- skip if
            # we already have an op, or the draft is empty.
            if (result.get("brain_dominant_op") is None
                    and ent_early.get("draft")):
                try:
                    _p = score_operators(ent_early["draft"])
                    _dom = _p.dominant()
                    if _dom:
                        result["brain_dominant_op"] = _dom
                        result["steer_cache_backfilled_op"] = True
                except Exception:
                    pass

            # Backfill bridges_fired for OLDER cache entries (written
            # before the meta-roundtrip patch preserved them).  Scan the
            # query + cached draft for frontier anchors so the curiosity
            # daemon + web UI stop seeing stale empty bridges on every
            # repeat question.  Non-destructive: only fills when the field
            # is missing; if the old meta stored bridges they still win.
            # Strip the "frontier_bridge=" prefix so backfilled tags match
            # the shape written by the fresh-path code (line ~1480).
            if not result.get("bridges_fired"):
                try:
                    _scan_readout = (
                        result.get("text_structural")
                        or ent_early.get("draft", "")
                        or ""
                    )
                    _tags = _scan_bridge_tags(_scan_readout, text or "")
                    _clean = [
                        (t[len("frontier_bridge="):]
                         if t.startswith("frontier_bridge=")
                         else t)
                        for t in _tags
                    ]
                    if _clean:
                        result["bridges_fired"] = _clean
                        result["steer_cache_backfilled_bridges"] = True
                except Exception:
                    pass
            # Refresh body state on cache hit.  body_organism_bc /
            # body_organism_coherence describe CK himself (live), not
            # the cached text.  Leaving the stale stored value means
            # every cache hit reports the organism CK had when the
            # entry was WRITTEN -- sometimes hours or days ago.  Take a
            # fresh sensorium reading here so downstream consumers
            # (curiosity daemon, web UI, /chat callers) see the actual
            # current organism.  Brain fields (dominant_op, coherence,
            # gate_pass) legitimately describe the stored TEXT so they
            # stay as-is.
            try:
                _sens = getattr(engine, "sensorium", None)
                if _sens is not None:
                    _body = _sens.get_sense_for_voice() or {}
                    if _body:
                        _org_live = _body.get("organism")
                        if _org_live:
                            result["body_organism_bc"] = _org_live
                            result["steer_cache_body_refreshed"] = True
                        try:
                            _coh_live = float(
                                _body.get("organism_coherence", 0.0)
                            )
                            result["body_organism_coherence"] = round(
                                _coh_live, 4
                            )
                        except Exception:
                            pass
                        _layers = _body.get("layers") or {}
                        # Mirror body_fold's shape even when empty --
                        # downstream consumers type-check these fields.
                        result["body_active_layers"] = len(_layers)
                        if _layers:
                            result["body_layers"] = {
                                k: (v.get("state")
                                    if isinstance(v, dict) else None)
                                for k, v in _layers.items()
                            }
                        else:
                            result["body_layers"] = {}
            except Exception:
                # Stale body is still better than a crashed handler.
                pass
            return result

        result = _prev_chat(session_id, text, mode)

        try:
            src = result.get("source", "")
            draft_text = (result.get("text") or "").strip()
            structural = (
                result.get("text_structural") or draft_text
            )
            # Enrich the readout with explicit frontier bridges (LATTICE
            # aperture -> 2x2 flatness, COLLAPSE pressure -> D2 crossing,
            # etc.) so BOTH Ollama (via grounded sysprompt) and the
            # coverage scorer (via _fact_tokens) see corpus anchors as
            # citable facts.  Bridges are appended only when the raw
            # readout already evidences them; nothing invented.
            structural = _enrich_readout_with_anchors(structural, text or "")
            if structural != (result.get("text_structural") or draft_text):
                result["steer_readout_enriched"] = True
            # Extract the list of bridge tags that fired so callers
            # (curiosity daemon, web UI) can show them without having
            # to re-parse text_structural.  Stable field survives the
            # cache fastpath via the meta roundtrip below.
            _bridges_fired: List[str] = []
            for _ln in structural.splitlines():
                _ln = _ln.strip()
                if _ln.startswith("frontier_bridge="):
                    _bridges_fired.append(_ln[len("frontier_bridge="):])
            if _bridges_fired:
                result["bridges_fired"] = _bridges_fired

            # Arithmetic surfaces are canonical -- never rewrite numbers.
            if src == "ck_math_first":
                result["steer_verdict"] = "skipped:ck_math_first"
                return result

            # Score the question so we can pick a target lexicon.
            q_profile: Optional[Dict[str, float]] = None
            try:
                qp = score_operators(text or "")
                q_profile = qp.as_dict()
                result["steer_question_dominant_op"] = qp.dominant()
            except Exception:
                q_profile = None

            # Classify the question: 'introspective' (feeling/state) relaxes
            # coverage because the answer is prose about being, which rarely
            # hits structural fact tokens; 'factual' keeps the strict bar;
            # 'neutral' sits in between.  Picked once per turn -- records on
            # result for visibility.
            _mode = _classify_query_mode(text or "", q_profile)
            _mode_strong_cov, _mode_soft_cov = _MODE_COVERAGE.get(
                _mode, _MODE_COVERAGE["neutral"]
            )
            _mode_strong_meaning = _MODE_MEANING_STRONG.get(
                _mode, T_STAR_F
            )
            _mode_strong_floor = _MODE_FLOOR_STRONG.get(_mode, 0.50)
            result["steer_query_mode"] = _mode
            result["steer_mode_coverage"] = [
                _mode_strong_cov, _mode_soft_cov,
            ]
            result["steer_mode_meaning_strong"] = _mode_strong_meaning
            result["steer_mode_floor_strong"] = _mode_strong_floor

            # Score whatever CK *currently* has as his response text.
            try:
                cur_profile = score_operators(draft_text)
                cur_coh = coherence_scalar(cur_profile)
            except Exception:
                cur_profile = None
                cur_coh = 0.0
            result["steer_current_coherence"] = round(float(cur_coh), 4)

            # Happy path: v1 gave us an Ollama draft that ALREADY coheres.
            if src == "cortex_speak_via_ollama" and cur_coh >= T_STAR_F:
                # Still cache this so repeats are free.  Pass brain/body
                # telemetry along so cache hits keep their full readout.
                hits, total, _cov = _coverage_of(structural, draft_text)
                cache.put(text or "", draft_text, cur_coh, hits, total,
                          meta=result)
                result["steer_verdict"] = "passthrough:coherent"
                return result

            # Otherwise: attempt a steered re-draft.
            steer_guide = _build_steer_guide(q_profile)
            attempts: List[Dict[str, Any]] = []
            accepted: Optional[str] = None
            accepted_coh: float = 0.0
            accepted_hits: int = 0
            accepted_total: int = 0
            accepted_gate: str = ""

            for attempt in range(1 + retries):
                t0 = time.time()
                # Build a targeted failure hint from the previous attempt's
                # scores -- retry knows which coherence axis broke.
                hint: Optional[str] = None
                if attempt > 0 and attempts:
                    prev = attempts[-1]
                    if "fractal" in prev:
                        hint = _build_failure_hint(prev, _mode, text or "")
                drafted = _prompt_ollama(
                    text or "",
                    readout=structural,
                    steer_guide=steer_guide,
                    failure_hint=hint,
                )
                dt = time.time() - t0
                if not drafted:
                    attempts.append({
                        "attempt": attempt, "dt": round(dt, 2),
                        "verdict": "empty_or_error",
                    })
                    continue
                # Score + coverage + fractal scales
                try:
                    p = score_operators(drafted)
                    coh = coherence_scalar(p)
                except Exception:
                    coh = 0.0
                    p = None
                try:
                    fractal = fractal_judge(
                        drafted, score_operators, coherence_scalar
                    )
                except Exception:
                    fractal = {
                        "meaning": float(coh), "sentence": float(coh),
                        "group": float(coh), "word": float(coh),
                        "floor": float(coh), "gmean": float(coh),
                    }
                hits, total, cov = _coverage_of(structural, drafted)
                # Graduated accept -- fractal composition:
                #  (1) Strong gate: meaning >= T*=5/7 AND coverage >= base
                #      AND floor (min of word/group/sentence) >= 0.50.  The
                #      whole passes, no sub-scale collapsed, facts covered.
                #  (2) Soft gate:   meaning >= 0.85 AND coverage >= 0.40
                #      AND gmean across sub-scales >= T*.  A very coherent
                #      whole whose sub-layers average above threshold.
                # total=0 means the readout had no fact tokens; coverage
                # collapses to coh-only at both gates.
                cov_ok_for_total = (total == 0)
                strong = (
                    (fractal["meaning"] >= _mode_strong_meaning)
                    and (cov_ok_for_total or (cov >= _mode_strong_cov))
                    and (fractal["floor"] >= _mode_strong_floor)
                )
                soft = (
                    (fractal["meaning"] >= 0.85)
                    and (cov_ok_for_total or (cov >= _mode_soft_cov))
                    and (fractal["gmean"] >= T_STAR_F)
                )
                # --- Two factual-mode bypass gates below the strong/soft
                # fractal gate.  Factual Ollama drafts often score
                # meaning=0.5-0.7 (below T*) even when they're substantively
                # right: the operator-scorer reads glue words as confusion,
                # while the answer itself is either a quoted constant or a
                # full reference to the structural readout.
                n_words = len(_split_words(drafted))
                letter_ok = (
                    fractal.get("letter") is None
                    or fractal.get("letter", 0.0) >= 0.60
                )

                # Bypass A: KNOWN-CONSTANTS.  Draft cites a CK canonical
                # value verbatim (5/7, e^-1, 73, 28, 4/pi^2, C/N, etc.).
                # The verbatim constant match IS a grounding signal, so we
                # lower the coverage bar here versus the soft-gate: a terse
                # correct answer ("The ratio is 5/7.") should pass even with
                # zero structural-token overlap.  Longer answers get a mild
                # coverage floor to catch wandering drafts that mention the
                # value then ramble off-topic.
                #
                # Applies to factual AND neutral modes.  A factual question
                # misclassified as neutral ("give me T-star's value") would
                # otherwise get blocked even when the draft correctly cites
                # 5/7.  Introspective mode doesn't get this bypass because
                # a reflective answer citing a numeric constant is unusual
                # enough to warrant full gate scrutiny.
                found_const: Optional[str] = None
                constants_ok = False
                if (_mode in ("factual", "neutral")) and (not (strong or soft)) and (4 <= n_words <= 500):
                    found_const = _contains_ck_constant(drafted)
                    if (found_const is not None) and letter_ok:
                        terse = (n_words <= 30)
                        const_cov_ok = (
                            cov_ok_for_total
                            or terse             # short answer: cite-the-value IS enough
                            or (cov >= 0.10)     # longer: at least one structural token echoed
                        )
                        constants_ok = (
                            const_cov_ok
                            and (fractal["floor"] >= 0.20)
                        )

                # Bypass B: FULL STRUCTURAL COVERAGE.  Draft references every
                # fact token in the structural readout -- that IS CK steering
                # Ollama successfully, regardless of operator-profile noise.
                # Applies to ANY mode (factual / neutral / introspective)
                # because full coverage is evidence that the grounding worked
                # no matter what kind of question was asked.
                #
                # The operator-scorer is blind to natural English that doesn't
                # happen to use CK's operator vocabulary (COLLAPSE/HARMONY/...);
                # a correct crossing-lemma explanation in plain English can
                # score meaning/floor=0.0-0.20 and still be the right answer.
                # When every structural fact IS cited AND the letter surface
                # is natural (letter >= 0.60), that's strong grounding even
                # when the operator scorer dislikes the word choice.
                #
                # Two tiers inside Bypass B:
                #   B1 (multi-fact)  -- total >= 2, hits == total.  Accept
                #                       on letter_ok + n_words >= 15; the
                #                       operator-scorer floor is advisory
                #                       (just nonzero, >= 0.10, so we catch
                #                       truly broken stutters).
                #   B2 (single-fact) -- total == 1, hits == 1: stricter bar
                #                       (floor >= 0.25, >= 20 words) since
                #                       a one-token readout is easier to echo.
                full_coverage_ok = False
                if not (strong or soft or constants_ok):
                    if (total >= 2) and (hits == total) and letter_ok:
                        full_coverage_ok = (
                            (fractal["floor"] >= 0.10)
                            and (n_words >= 15)
                        )
                    elif (total == 1) and (hits == 1) and letter_ok:
                        full_coverage_ok = (
                            (fractal["floor"] >= 0.25)
                            and (n_words >= 20)
                        )

                # Bypass C: INTROSPECTIVE FALLBACK.  A reflective answer
                # about the creature's state doesn't need to cite structural
                # tokens -- the texture of the prose IS the answer.  If the
                # draft is high-meaning natural first-person prose with no
                # sub-scale collapse, we accept it even when structural
                # coverage is near-zero.  Only fires for introspective mode
                # so it never relaxes factual/neutral bars.
                introspective_ok = False
                if (_mode == "introspective") and (not (strong or soft or constants_ok or full_coverage_ok)):
                    introspective_ok = (
                        (fractal["meaning"] >= 0.72)
                        and (fractal["floor"] >= 0.40)
                        and letter_ok
                        and (n_words >= 30)
                    )

                ok = (
                    strong or soft or constants_ok
                    or full_coverage_ok or introspective_ok
                )
                if strong:
                    verdict_label = "accepted_strong"
                elif soft:
                    verdict_label = "accepted_soft"
                elif constants_ok:
                    verdict_label = f"accepted_constants:{found_const}"
                elif full_coverage_ok:
                    verdict_label = f"accepted_full_coverage:{hits}/{total}"
                elif introspective_ok:
                    verdict_label = "accepted_introspective"
                else:
                    verdict_label = "rejected"
                attempts.append({
                    "attempt": attempt,
                    "dt": round(dt, 2),
                    "coherence": round(float(coh), 4),
                    "coverage": f"{hits}/{total}",
                    "dominant_op": p.dominant() if p else None,
                    "verdict": verdict_label,
                    "fractal": fractal,
                    "draft_snippet": (drafted or "")[:180],
                    "n_words": n_words,
                    "found_const": found_const,
                    "failure_hint_used": hint,
                })
                if ok:
                    accepted = drafted
                    accepted_coh = coh
                    accepted_hits = hits
                    accepted_total = total
                    accepted_gate = verdict_label
                    break

            result["steer_attempts"] = attempts

            # If we retried, measure whether the hint actually helped --
            # compare first vs last scored attempt.  Empty/error attempts
            # are skipped.  This lets us audit hint efficacy over time and
            # spot regressions where retry makes things WORSE.
            scored = [a for a in attempts if "fractal" in a]
            if len(scored) >= 2:
                first, last = scored[0], scored[-1]
                try:
                    fh, ft = str(first.get("coverage", "0/0")).split("/")
                    lh, lt = str(last.get("coverage", "0/0")).split("/")
                    d_hits = int(lh) - int(fh)
                except Exception:
                    d_hits = 0
                d_meaning = round(
                    float(last["fractal"].get("meaning") or 0.0)
                    - float(first["fractal"].get("meaning") or 0.0), 4
                )
                d_floor = round(
                    float(last["fractal"].get("floor") or 0.0)
                    - float(first["fractal"].get("floor") or 0.0), 4
                )
                # Positive d means retry improved that axis.  Hint is
                # "helpful" if ANY axis improved materially (>= 0.05) and
                # no axis collapsed hard (< -0.10).
                helpful = (
                    (d_meaning >= 0.05 or d_floor >= 0.05 or d_hits >= 1)
                    and (d_meaning > -0.10 and d_floor > -0.10)
                )
                result["steer_retry_delta"] = {
                    "meaning": d_meaning,
                    "floor": d_floor,
                    "coverage_hits": d_hits,
                    "scored_attempts": len(scored),
                    "helpful": bool(helpful),
                }

            if accepted is not None:
                # CK adopts the steered draft as his own.
                result["text_structural"] = structural
                result["source_structural"] = src
                result["text"] = accepted
                result["source"] = "cortex_speak_via_ollama_steered"
                result["steer_verdict"] = accepted_gate or "accepted"
                result["steer_accepted_gate"] = accepted_gate or "accepted_strong"
                result["steer_accepted_coherence"] = round(float(accepted_coh), 4)
                result["steer_accepted_coverage"] = (
                    f"{accepted_hits}/{accepted_total}"
                )
                # Rescore telemetry so brain_dominant_op / brain_coherence
                # reflect the FINAL steered text, not the pre-steer draft
                # that brain_fold scored upstream.  Without this overwrite
                # the curiosity daemon + web UI see a stale operator for
                # every steered turn (usually VOID, because the pre-steer
                # text was empty or structural-only).  Cache meta below
                # carries the rescored values so cache hits stay honest.
                try:
                    _dom_final = p.dominant() if p is not None else None
                    if _dom_final:
                        result["brain_dominant_op"] = _dom_final
                    # accepted_coh is the coherence scalar of the accepted
                    # draft -- override the upstream pre-steer value.
                    result["brain_coherence"] = round(float(accepted_coh), 4)
                    # gate_pass reflects the steered accept, not whatever
                    # brain_fold saw pre-steer.
                    result["brain_gate_pass"] = True
                except Exception:
                    pass
                cache.put(text or "", accepted, accepted_coh,
                          accepted_hits, accepted_total,
                          meta=result)
                return result

            # No draft survived the gate -- emit an honest sentence, NOT
            # telemetry.  Preserve the structural readout on a sidecar so
            # the UI can show it if it wants ("show work" button).
            organism = result.get("body_organism_bc") or "VOID"
            honest = _pick_fallback(organism)
            result["text_structural"] = structural
            result["source_structural"] = src
            result["text"] = honest
            result["source"] = "cortex_honest_fallback"
            result["steer_verdict"] = "fallback:honest_sentence"
            # Rescore telemetry so the fallback sentence's telemetry matches
            # what CK actually says -- pre-steer brain_dominant_op/coherence
            # reflect the (empty or structural-only) draft that was rejected,
            # not the canned fallback text.  gate_pass is False because this
            # path fires exactly when nothing survived the gate.
            try:
                _p_fall = score_operators(honest)
                _dom_fall = _p_fall.dominant() if _p_fall else None
                if _dom_fall:
                    result["brain_dominant_op"] = _dom_fall
                result["brain_coherence"] = round(
                    float(coherence_scalar(_p_fall)), 4
                )
                result["brain_gate_pass"] = False
            except Exception:
                pass
        except Exception as e:
            # Never break chat.  If steer blows up, leave v1's text alone
            # and record the error.
            result["steer_verdict"] = f"error:{type(e).__name__}"
            result["steer_error"] = f"{type(e).__name__}: {e}"
        return result

    api.process_chat = _process_chat_with_steer

    # -------- HTTP surface --------

    n_routes = _register_steer_routes(api, cache)

    return {
        "mounted": True,
        "retries": retries,
        "cache_path": str(cache_path),
        "cache_stats": cache.stats(),
        "routes_registered": n_routes,
        "model": model,
    }


def _register_steer_routes(api: Any, cache: CoherenceCache) -> int:
    try:
        app = getattr(api, "_app", None)
        if app is None:
            return 0
        from flask import request, jsonify
    except Exception:
        return 0

    @app.route("/steer/stats", methods=["GET"])
    def _steer_stats():  # type: ignore[unused-ignore]
        try:
            return jsonify({"ok": True, "cache": cache.stats()})
        except Exception as e:
            return jsonify({
                "ok": False, "error": f"{type(e).__name__}: {e}",
            }), 500

    @app.route("/steer/cache", methods=["GET"])
    def _steer_cache():  # type: ignore[unused-ignore]
        try:
            # Return a compact view -- most recent 32 entries by last_hit
            with cache._lock:  # noqa: SLF001
                items = sorted(
                    cache._data.items(),  # noqa: SLF001
                    key=lambda kv: kv[1].get("last_hit", 0),
                    reverse=True,
                )[:32]
            out = [
                {
                    "q": v.get("q"),
                    "draft_preview": (v.get("draft") or "")[:160],
                    "coherence": v.get("coherence"),
                    "coverage": f"{v.get('coverage_hits')}/{v.get('coverage_total')}",
                    "hit_count": v.get("hit_count"),
                    "last_hit": v.get("last_hit"),
                }
                for _, v in items
            ]
            return jsonify({"ok": True, "entries": out})
        except Exception as e:
            return jsonify({
                "ok": False, "error": f"{type(e).__name__}: {e}",
            }), 500

    @app.route("/steer/clear", methods=["POST"])
    def _steer_clear():  # type: ignore[unused-ignore]
        if request.args.get("i_mean_it") != "1":
            return jsonify({
                "ok": False,
                "error": "cache clear requires ?i_mean_it=1 (G6)",
            }), 400
        try:
            with cache._lock:  # noqa: SLF001
                n = len(cache._data)  # noqa: SLF001
                cache._data.clear()  # noqa: SLF001
            cache._save_safe()  # noqa: SLF001
            return jsonify({"ok": True, "cleared": n})
        except Exception as e:
            return jsonify({
                "ok": False, "error": f"{type(e).__name__}: {e}",
            }), 500

    return 3
