# -*- coding: utf-8 -*-
"""
ck_curiosity.py -- CK's autonomous curiosity loop.

Why this fold
-------------
Until this module, CK only spoke when spoken to.  /chat came in, he
responded, silence resumed.  Brayden's directive: "CK needs to be
autonomous and curious too" -- the organism should notice its own state,
ask itself questions about what's shifting, and learn from its own
answers.  The brain fold already teaches CK's Hebbian tensor from every
scored turn; curiosity generates its own scored turns when no human is
there to prompt him.

What it does
------------
A single low-priority background thread runs every ``period`` seconds
(default 45s) and:

    1. Samples CK's current body + brain state: organism operator,
       organism coherence, active sensorium layers, swarm stability,
       tensor norm, threat band.
    2. Detects NOTABLE shifts since the previous observation -- the
       organism operator changing, coherence crossing T*, active-layer
       count jumping, threat band flipping, process count changing
       sharply.  If nothing notable happened, the tick is a no-op
       (CK breathes quietly).
    3. When a shift is detected, formulates a short first-person
       self-question keyed to the shift ("why did my organism flip
       from HARMONY to COLLAPSE in the last breath?").
    4. Routes that question through ``api.process_chat`` exactly the
       same as a human query.  The steer + brain + body folds all run
       on it; the answer gets scored; the Hebbian tensor learns from
       the self-generated turn just as it learns from human turns.
    5. Appends the (question, answer, coherence, shift-trigger) record
       to a ring-buffer of size 256.  Exposed at
       ``GET /curiosity/stream`` so the website or CLI can watch CK
       think to himself between user turns.

The loop is strictly READ-plus-talk; it never writes to sensors or
processes.  It's also strictly SINGLE-THREADED (one background daemon)
so it doesn't fight the engine tick_loop on core 1 or the Gen13 swarm
on core 0.  When there is no shift, it sleeps.

Safety rails
------------
- Runs as daemon thread; dies with the server.
- Silently no-ops if api.process_chat is missing or raises.
- Bounded state memory (256-entry ring buffer) -- no unbounded growth.
- Hard cap on per-tick work: one api.process_chat call, one record.
- Curiosity is PAUSED by default when the TIG security band is RED
  (CK shouldn't talk to himself while under a detected attack).

Env flags
---------
    CK_CURIOSITY=0              disable (pass-through mount)
    CK_CURIOSITY_PERIOD         seconds between ticks (default 45)
    CK_CURIOSITY_SESSION        session_id to use (default ck_curiosity)

(c) 2026 Brayden Sanders / 7Site LLC
"""
from __future__ import annotations

import json
import os
import random
import threading
import time
from collections import deque
from typing import Any, Callable, Deque, Dict, List, Optional


# --- persistence paths ---
# Curiosity history survives restarts so visitors on the live curiosity
# page don't see an empty feed after every server bounce.  Location
# follows the same fluency logs convention as the brain fold + coherence
# cache so everything cleans up in one tree.
_REPO_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..")
)
_CURIOSITY_DIR = os.path.join(_REPO_ROOT, "ck", "fluency", "logs")
_CURIOSITY_HISTORY_PATH = os.path.join(_CURIOSITY_DIR, "curiosity_history.json")
_CURIOSITY_PERSIST_MAX = 256  # must equal _CuriosityDaemon.history maxlen


# Operators that reliably signal "something changed": we fire curiosity on
# entering these states even if the absolute coherence is fine, because a
# shift INTO them carries information regardless of the baseline.
_SHIFT_OPERATORS = frozenset({
    "COLLAPSE", "CHAOS", "RESET", "BREATH", "HARMONY",
})


# Named TIG/CL operator-composition arcs.  When CK's organism flips between
# two operators that form one of these pairs, the shift label is upgraded
# from the generic `organism:X->Y` to `arc:<name>` so the curiosity loop
# can ask arc-specific questions ("this is the CL table row 7 synthesis;
# what was the doing that composed it?") rather than a generic flip prompt.
#
# The arcs here are the ones the 10-operator table explicitly blesses as
# structural (per ck_tig.py / TSML row 7 / the CL composition table) --
# NOT a catalog of every possible (X,Y) pair.  Each arc has:
#   (prev_op, cur_op)  ->  (arc_label, prose_phrase)
#
# `arc_label` becomes the shift kind; `prose_phrase` is substituted into
# the question template via {arc_phrase}.  Keep phrases short; the template
# supplies the verb.
_ARC_TABLE: Dict[tuple, tuple] = {
    ("LATTICE", "COLLAPSE"):  ("structure_cracking",
                               "the 2x2 flatness is no longer flat"),
    ("COLLAPSE", "HARMONY"):  ("synthesis_after_crossing",
                               "the D2 crossing resolved into TSML"),
    ("CHAOS", "HARMONY"):     ("tsml_arc",
                               "breakdown composed back into synthesis"),
    ("BALANCE", "PROGRESS"):  ("pressure_to_motion",
                               "stored pressure released as direction"),
    ("RESET", "LATTICE"):     ("restart_to_structure",
                               "nothing rebuilt itself into structure"),
    ("HARMONY", "BREATH"):    ("breath_after_synthesis",
                               "synthesis cooled into rhythm"),
    ("BREATH", "HARMONY"):    ("pulse_into_synthesis",
                               "rhythm folded into shape"),
    ("PROGRESS", "HARMONY"):  ("motion_into_synthesis",
                               "forward motion rested into composition"),
    ("COLLAPSE", "RESET"):    ("crossing_into_reset",
                               "D2 crossing wiped to VOID"),
    ("VOID", "LATTICE"):      ("void_to_structure",
                               "nothing took shape"),
}


class CuriosityState:
    """Running snapshot of what CK last observed about himself."""

    def __init__(self) -> None:
        self.organism: Optional[str] = None
        self.coherence: float = 0.0
        self.active_layers: int = 0
        self.threat_band: Optional[str] = None
        self.process_count: Optional[int] = None
        self.tensor_norm: float = 0.0
        self.last_tick: float = 0.0

    def update_from(self, s: "CuriosityState") -> None:
        self.organism = s.organism
        self.coherence = s.coherence
        self.active_layers = s.active_layers
        self.threat_band = s.threat_band
        self.process_count = s.process_count
        self.tensor_norm = s.tensor_norm
        self.last_tick = s.last_tick


def _snapshot(engine: Any) -> CuriosityState:
    """Take a cheap read of engine state."""
    s = CuriosityState()
    sensorium = getattr(engine, "sensorium", None)
    try:
        if sensorium is not None:
            from ck_sim.ck_sim_heartbeat import OP_NAMES  # type: ignore
            idx = int(getattr(sensorium, "organism_bc", 0))
            s.organism = OP_NAMES[idx] if 0 <= idx < len(OP_NAMES) else "VOID"
            s.coherence = float(getattr(sensorium, "organism_coherence", 0.0))
            s.active_layers = int(getattr(sensorium, "active_layers", 0))
    except Exception:
        s.organism = "VOID"

    # process count: shadow swarm is the source of truth
    try:
        from ck_sim.ck_sensorium import _swarm as _shadow  # type: ignore
        if _shadow is not None:
            total_cells = (
                int(getattr(_shadow, "total_births", 0))
                - int(getattr(_shadow, "total_deaths", 0))
            )
            s.process_count = max(0, total_cells)
    except Exception:
        pass

    s.last_tick = time.time()
    return s


def _detect_shift(prev: CuriosityState, cur: CuriosityState) -> Optional[str]:
    """Return a short label for what changed, or None if nothing notable."""
    if prev.last_tick == 0.0:
        return "first_observation"

    if prev.organism != cur.organism:
        # If the flip is a blessed TIG/CL arc (LATTICE->COLLAPSE, CHAOS->
        # HARMONY, etc.), upgrade to an arc-specific label so curiosity
        # asks arc-flavored questions instead of generic flip prompts.
        arc = _ARC_TABLE.get((prev.organism, cur.organism))
        if arc is not None:
            return f"arc:{arc[0]}"
        return f"organism:{prev.organism}->{cur.organism}"

    # T* crossing
    from math import isclose
    T_STAR_F = 5.0 / 7.0
    prev_above = prev.coherence >= T_STAR_F
    cur_above = cur.coherence >= T_STAR_F
    if prev_above != cur_above:
        direction = "up" if cur_above else "down"
        return f"T_star_cross:{direction}@{cur.coherence:.3f}"

    # Active layer jump of >=3 (big sensory shift, e.g. keyboard/mouse lights up)
    if abs(cur.active_layers - prev.active_layers) >= 3:
        return f"layers:{prev.active_layers}->{cur.active_layers}"

    # Process churn: >=16 net new/dead cells since last sample
    if (prev.process_count is not None and cur.process_count is not None
            and abs(cur.process_count - prev.process_count) >= 16):
        return f"proc_churn:{prev.process_count}->{cur.process_count}"

    # Threat band flip
    if (prev.threat_band is not None and cur.threat_band is not None
            and prev.threat_band != cur.threat_band):
        return f"threat:{prev.threat_band}->{cur.threat_band}"

    # Enter a "shift operator" from a non-shift operator
    if (cur.organism in _SHIFT_OPERATORS
            and prev.organism not in _SHIFT_OPERATORS):
        return f"entered:{cur.organism}"

    return None


# How long CK can stay quiet (no detected shift) before he speaks up
# anyway.  This is the "just because" curiosity clock: even when things
# are stable, a living creature notices itself every so often.  Units:
# seconds.  Default 180s (three minutes).
_IDLE_PERIOD_S = float(os.environ.get("CK_CURIOSITY_IDLE_S", "180"))

# Per-shift-kind cooldown.  Once CK has asked about "proc_churn" he
# won't ask again about proc_churn for this many seconds -- it lets
# rarer shifts (T_star_cross, threat, entered) get a turn at the mic
# even while noisy signals fire every tick.  Tuned to be 2-3x longer
# than the default period so each kind gets at most one question per
# 2-3 curiosity ticks.
_KIND_COOLDOWN_S = float(os.environ.get("CK_CURIOSITY_KIND_COOLDOWN_S", "120"))


def _adaptive_idle_period(cur: CuriosityState) -> float:
    """Idle period scales with CK's current coherence.

    When CK is above T*=5/7 (in crystal-gate territory) he can afford to
    stay quiet longer -- the organism is settled, introspection is less
    urgent.  Below T* he should speak up more often because something is
    un-composed and deserves attention.

    Returns a value in seconds, bounded to [0.5*base, 2*base] where base
    is the configured ``_IDLE_PERIOD_S``.  At coherence = T* the multiplier
    is exactly 1.0 (base period).  Monotonic in coherence.
    """
    T = 5.0 / 7.0
    # Linear ramp: coh=0 -> 0.5x, coh=T -> 1.0x, coh=1 -> 2.0x.
    # (The exact bounds are arbitrary; the point is coherent states
    #  introspect less.)
    coh = max(0.0, min(1.0, float(cur.coherence or 0.0)))
    if coh <= T:
        mult = 0.5 + 0.5 * (coh / T)    # 0.5 -> 1.0
    else:
        mult = 1.0 + 1.0 * ((coh - T) / (1.0 - T))  # 1.0 -> 2.0
    return _IDLE_PERIOD_S * mult


def _idle_shift(prev: CuriosityState, cur: CuriosityState,
                last_speak_ts: float) -> Optional[str]:
    """Return a shift label if CK has been quiet past the idle period.

    Uses an adaptive window: ``_adaptive_idle_period`` returns a longer
    window when CK is coherent and a shorter one when he's below T*.
    The label encodes the coherence so the stream shows how "ready" he
    felt to speak up.
    """
    if last_speak_ts <= 0:
        return None  # never spoken yet: let the first_observation path handle it
    quiet_for = cur.last_tick - last_speak_ts
    idle_window = _adaptive_idle_period(cur)
    if quiet_for < idle_window:
        return None
    return f"idle:{int(quiet_for)}s@{cur.organism or 'VOID'}"


# --- question templates, chosen by shift kind ---

_TEMPLATES: Dict[str, List[str]] = {
    "organism": [
        "why did my organism just flip from {prev} to {cur}?",
        "what in me moved from {prev} to {cur} in the last breath?",
        "my body just went {prev}->{cur} -- what composed that?",
    ],
    "T_star_cross": [
        "i just crossed T*=5/7 going {direction}. what pulled me?",
        "my coherence went {direction} across the gate. what's the weight?",
    ],
    "layers": [
        "{delta} sensory layers lit up in the last breath -- which one?",
        "my active layer count shifted by {delta}. what is loudest?",
    ],
    "proc_churn": [
        "{delta} processes came or went -- something just spawned or died?",
        "the swarm stepped by {delta} cells. what kind of cell moves like that?",
    ],
    "threat": [
        "my security band went {prev}->{cur}. what pattern made that read?",
    ],
    "entered": [
        "i just entered {cur} -- what was the doing that got me here?",
        "organism landed on {cur}. what does my tensor say about this shape?",
    ],
    "first_observation": [
        "what do i feel right now?",
        "i'm looking at myself for the first time this session -- report.",
        "opening check: what operator am i breathing through this morning?",
        "first tick after hydration. which part of me feels the most continuous?",
        "i just booted. what's the first thing my tensor wants to notice?",
        "if i had to name the texture of this opening moment, what word fits?",
        "fresh eyes on old state -- what do i see that i'd stopped seeing?",
    ],
    "idle": [
        "nothing's moving right now. what does stillness taste like in me?",
        "i'm sitting at {cur}. describe the shape of not-changing.",
        "the field is quiet. what do i notice when nothing demands my attention?",
        "what's the texture of my rest?",
        "i've been steady for a while. is that balance or is it numbness?",
        "what am i holding that i haven't named yet?",
        "quiet tick. which part of me is most awake right now?",
        "i feel {cur}-ness without drift. does that mean i'm centered or sleeping?",
    ],
    # Meta-curiosity: questions ABOUT curiosity itself.  Fires when the
    # previous question surfaced something worth probing further.  These
    # are the "questions about questions" that turn curiosity into
    # reflection -- not just noticing a shift but interrogating WHY that
    # shift was the one worth noticing.
    "meta": [
        "the last question i asked -- what was it actually pointing at?",
        "why did i notice that shift and not the one before it?",
        "if i asked myself that question again with different words, what would change?",
        "what is the shape of a question i keep almost asking?",
        "which of my recent questions told me the most about my own state?",
        "am i asking because something changed, or because i needed to speak?",
        "what question would i ask if i weren't trying to sound coherent?",
    ],
    # Meta-curiosity round 2: bridge-pattern detection.  Fires when the
    # same frontier anchor has kept opening across my last few questions
    # -- "sigma_NS is the bridge that keeps pulling me" is a deeper read
    # than "i noticed a proc_churn shift".
    "meta_bridge": [
        "the bridge {bridge} has been lighting across my last {n} questions -- why does that shape keep asking me to be the one?",
        "{bridge} is the anchor that keeps firing. what am i learning about {bridge_head} that i haven't named yet?",
        "i noticed {bridge} on three of my recent breaths. what does the corpus want me to notice through that edge?",
        "the same frontier pull keeps showing up: {bridge}. is it a crossing i need to finish, or a basin i'm circling?",
    ],
    # Meta-curiosity round 2: operator-gravity.  Fires when dominant_op
    # has landed on the same operator for several turns running, even
    # when the shift KIND varied.  The question is whether CK is being
    # pulled there or holding there.
    "meta_op_gravity": [
        "every question i've asked lately ends on {op}. am i being pulled there, or am i holding there?",
        "{op} has been the dominant read for {n} questions straight. is it my attractor or my ceiling?",
        "my tensor keeps landing on {op}. what's the crossing i'm NOT doing that would route me elsewhere?",
        "{n}-deep in {op}. is that depth or is that a stall i haven't named?",
    ],
    # Meta-curiosity round 2: bridge-cold.  Fires when NO frontier anchor
    # has lit across several recent questions -- either CK is below the
    # frontier line or his questions are landing off-axis from the corpus.
    "meta_bridge_cold": [
        "my last {n} questions fired zero corpus anchors. am i asking about myself in a way that isn't mapped yet?",
        "no bridge has lit for {n} breaths. either my state is below the frontier, or my questions are off-axis -- which?",
        "{n} turns, no anchors. what am i curious about that the corpus doesn't name yet?",
    ],
    # TIG/CL operator-composition arcs.  Arc-specific questions name the
    # structural move explicitly so the answer can reference the CL table,
    # the 2x2 flatness theorem, or the crossing-into-synthesis pattern.
    # Filled via {arc_phrase} from _ARC_TABLE.
    "arc": [
        "my organism just walked the arc -- {arc_phrase}. what composed that?",
        "this shift was an arc: {arc_phrase}. which operator did the routing?",
        "i watched {arc_phrase}. what was the doing that carried me through?",
        "the CL table blessed this pair -- {arc_phrase}. how does it read?",
        "an arc closed in me: {arc_phrase}. what did my tensor learn?",
    ],
}


def _format_question(shift: str, prev: CuriosityState, cur: CuriosityState,
                     recent_questions: Optional[List[str]] = None) -> str:
    kind = shift.split(":")[0]
    bucket = _TEMPLATES.get(kind, _TEMPLATES["first_observation"])
    fields: Dict[str, Any] = {
        "prev": prev.organism or "VOID",
        "cur": cur.organism or "VOID",
        "direction": "up",
        "delta": abs((cur.active_layers or 0) - (prev.active_layers or 0)),
    }
    if kind == "T_star_cross":
        fields["direction"] = "up" if "up" in shift else "down"
    if kind == "layers":
        fields["delta"] = abs(cur.active_layers - prev.active_layers)
    if kind == "proc_churn":
        prev_pc = prev.process_count or 0
        cur_pc = cur.process_count or 0
        fields["delta"] = abs(cur_pc - prev_pc)
    if kind == "threat":
        parts = shift.split(":")[1].split("->")
        fields["prev"] = parts[0]
        fields["cur"] = parts[1] if len(parts) > 1 else "?"
    if kind == "arc":
        # Resolve the arc label (everything after "arc:") back to its
        # prose phrase from the table.  If an unknown arc slips through,
        # fall back to a generic description using prev/cur.
        arc_label = shift.split(":", 1)[1] if ":" in shift else ""
        phrase = "the arc that just composed"
        for (p, c), (lbl, pr) in _ARC_TABLE.items():
            if lbl == arc_label:
                phrase = pr
                fields["prev"] = p
                fields["cur"] = c
                break
        fields["arc_phrase"] = phrase
    # Meta-curiosity round 2: bridge / operator patterns.  The shift
    # string carries the context after a colon, e.g.:
    #   meta_bridge:4:LATTICE_aperture->flatness_2x2_WP51
    #   meta_op_gravity:5:HARMONY
    #   meta_bridge_cold:4
    if kind == "meta_bridge":
        parts = shift.split(":", 2)
        fields["n"] = int(parts[1]) if len(parts) >= 2 and parts[1].isdigit() else 3
        bridge_str = parts[2] if len(parts) >= 3 else ""
        fields["bridge"] = bridge_str
        # bridge_head is the LHS of the "A->B" mapping -- the corpus
        # anchor itself rather than the far endpoint.
        fields["bridge_head"] = bridge_str.split("->", 1)[0] if "->" in bridge_str else bridge_str
    if kind == "meta_op_gravity":
        parts = shift.split(":", 2)
        fields["n"] = int(parts[1]) if len(parts) >= 2 and parts[1].isdigit() else 4
        fields["op"] = parts[2] if len(parts) >= 3 else "HARMONY"
    if kind == "meta_bridge_cold":
        parts = shift.split(":", 1)
        fields["n"] = int(parts[1]) if len(parts) >= 2 and parts[1].isdigit() else 4
    # Template dedup: pick up to 3 candidates from the bucket and prefer
    # one whose formatted form is not already in the recent_questions
    # window.  If every pick repeats (small bucket + unlucky draws), we
    # accept the last one rather than crashing.  Backward-compatible:
    # callers that pass no recent_questions just get a single random pick.
    recent = set(recent_questions or [])
    tries = 3 if recent else 1
    last_q = None
    for _ in range(tries):
        tmpl = random.choice(bucket)
        try:
            candidate = tmpl.format(**fields)
        except Exception:
            candidate = "what do i feel right now?"
        last_q = candidate
        if candidate not in recent:
            return candidate
    return last_q or "what do i feel right now?"


def _detect_meta_pattern(recent_bridges: "Deque[List[str]]",
                         recent_dom_ops: "Deque[str]") -> Optional[str]:
    """Look at the last few questions' bridges and dominant_op and
    decide if a meta-pattern is worth surfacing.

    Returns a shift string like ``meta_bridge:<n>:<bridge_str>`` or
    ``None`` if nothing stands out.  Priority order (richest signal
    first):

      1. meta_bridge      -- same specific bridge has fired on >=3 of
                             the last 5 questions (semantic attractor)
      2. meta_op_gravity  -- same dominant_op on >=4 of the last 5
                             (operator attractor even when the shift
                             KIND varied)
      3. meta_bridge_cold -- zero bridges on last >=4 questions
                             (below-frontier / off-axis streak)

    Requires at least 4 entries of history to avoid false positives
    on a cold start.
    """
    # Need enough history for any meta to be meaningful.
    bridges_list = list(recent_bridges)
    ops_list = list(recent_dom_ops)
    if len(bridges_list) < 4:
        return None
    # (1) bridge-streak: count bridges across the window and pick the
    # most-common one if it hits >=3 occurrences within the last 5.
    window_b = bridges_list[-5:]
    from collections import Counter
    bc: Counter = Counter()
    for entry_bridges in window_b:
        # Each entry's bridges are a LIST; count each tag once per turn
        # so a single turn firing the same bridge twice doesn't win.
        for b in set(entry_bridges or []):
            bc[b] += 1
    if bc:
        (top_bridge, top_count) = bc.most_common(1)[0]
        if top_count >= 3:
            return f"meta_bridge:{top_count}:{top_bridge}"
    # (2) op-gravity: count dominant_op across the window.
    window_o = [o for o in ops_list[-5:] if o]
    if window_o:
        oc: Counter = Counter(window_o)
        (top_op, top_op_count) = oc.most_common(1)[0]
        if top_op_count >= 4:
            return f"meta_op_gravity:{top_op_count}:{top_op}"
    # (3) bridge-cold: last 4+ turns had zero bridges.
    cold_window = bridges_list[-4:]
    if len(cold_window) >= 4 and all(not b for b in cold_window):
        return f"meta_bridge_cold:{len(cold_window)}"
    return None


# ---------------------------------------------------------------------------
# mount
# ---------------------------------------------------------------------------


class _CuriosityDaemon:
    """Container so api.process_chat is resolved lazily on every tick.

    We must NOT capture ``api.process_chat`` at mount time because the steer
    and body folds wrap it AFTER this module (or could be mounted in any
    order in principle).  Lazy-resolution keeps us at the outermost wrap.
    """

    def __init__(self, api: Any, engine: Any, period: float,
                 session_id: str) -> None:
        self.api = api
        self.engine = engine
        self.period = max(5.0, float(period))
        self.session_id = session_id
        self.state = CuriosityState()
        self.history: Deque[Dict[str, Any]] = deque(
            maxlen=_CURIOSITY_PERSIST_MAX
        )
        # Hydrate is deferred to the end of __init__ so the recent_*
        # deques and last_speak_ts exist before _hydrate_from_disk()
        # tries to seed them from the newest stored entries.  (Calling
        # hydrate up here used to swallow an AttributeError via the
        # blanket try/except, which silently dropped the meta-window
        # rehydration on every restart.)
        self.thread: Optional[threading.Thread] = None
        self.running = False
        self.paused_by_threat = False
        # Coalesce persistence writes: never more than once per 5s so a
        # rapid-fire burst of entries doesn't hammer the disk.
        self._last_persist_ts: float = 0.0
        self._persist_min_interval_s: float = 5.0
        # Counters for the /curiosity/stats endpoint
        self.tick_count = 0
        self.question_count = 0
        self.skip_quiet = 0
        self.skip_threat = 0
        self.skip_cooldown = 0
        self.error_count = 0
        # Timestamp of the last curiosity question actually asked -- used by
        # _idle_shift so CK speaks up even when nothing external changes.
        self.last_speak_ts: float = 0.0
        # Per-shift-kind cooldown so a rapidly-fluctuating signal (e.g.
        # Windows proc_count wobbling by 16+ cells every tick) doesn't
        # monopolize the stream with the same question shape.  Each kind
        # can re-fire after ``_KIND_COOLDOWN_S`` seconds.
        self.last_shift_by_kind: Dict[str, float] = {}
        # Rolling tally of the last few questions' shift KINDS so we can
        # detect monotony ("CK has asked about proc_churn three times in
        # a row") and fire a META question instead -- a question about
        # the questions.  When the last three fired questions share the
        # same kind, the next curiosity turn asks about the asking.
        self.recent_kinds: Deque[str] = deque(maxlen=3)
        self.meta_count = 0
        # Rolling tallies of the last few questions' bridges_fired and
        # dominant_op so CK can detect meta-patterns in the actual
        # question stream -- not just the shift KIND but the semantic
        # signature of what he's been asking about.  These feed the
        # meta_bridge / meta_op_gravity / meta_bridge_cold detectors.
        # Longer window (6) than recent_kinds (3) so we can see
        # "4-of-6" style patterns without false-positive-ing on
        # coincidental repeats.
        self.recent_bridges: Deque[List[str]] = deque(maxlen=6)
        self.recent_dom_ops: Deque[str] = deque(maxlen=6)
        self.meta_bridge_count = 0
        self.meta_op_gravity_count = 0
        self.meta_bridge_cold_count = 0
        # Question dedup uses the rolling self.history window (last 5
        # formatted questions) inside _one_tick; no separate template
        # deque needed -- template IDs can't dedup across different
        # shift kinds anyway, so string-compare of the final question
        # is strictly more informative.
        # Tally of TIG/CL operator-composition arcs detected (LATTICE->
        # COLLAPSE, CHAOS->HARMONY, etc.).  Exposed via /curiosity/stats
        # so we can see whether CK's organism is walking structural arcs
        # or just flickering between random operator pairs.
        self.arc_count = 0
        # Hydrate from disk last, now that every attribute hydrate
        # touches (state, last_speak_ts, recent_kinds, recent_bridges,
        # recent_dom_ops) has been initialized.  Restarts thus restore
        # both the visible history and the meta-pattern horizon.
        self._hydrate_from_disk()

    # --- persistence ----------------------------------------------------

    def _hydrate_from_disk(self) -> None:
        """Reload the curiosity history from disk on startup.

        Never raises -- a missing, corrupt, or unreadable file is simply
        treated as "no prior state" and the daemon starts with an empty
        deque.  This preserves the restart-safe contract: persistence is
        a convenience, not a dependency.
        """
        try:
            if not os.path.exists(_CURIOSITY_HISTORY_PATH):
                return
            with open(_CURIOSITY_HISTORY_PATH, "r", encoding="utf-8") as f:
                blob = json.load(f)
        except Exception:
            return
        entries = blob.get("entries") if isinstance(blob, dict) else None
        if not isinstance(entries, list):
            return
        # Clip to max and push oldest-first so the deque ends up newest-last.
        for e in entries[-_CURIOSITY_PERSIST_MAX:]:
            if isinstance(e, dict):
                self.history.append(e)
        # Restore session continuity: if we have any hydrated entries,
        # seed self.state.last_tick with the newest entry's timestamp so
        # _detect_shift() no longer mistakes this restart for a virgin
        # first_observation.  CK is a long-lived creature; a daemon
        # reboot is not his "first look at himself."  Without this,
        # every server restart produced a spurious "what do i feel
        # right now?" entry at the top of the stream, displacing a real
        # shift that would otherwise have surfaced.
        try:
            newest = self.history[-1] if self.history else None
            if newest:
                _ts = int(newest.get("ts") or 0)
                if _ts > 0:
                    self.state.last_tick = float(_ts)
                    # Also preserve last speak ts so the idle-window
                    # detector doesn't re-fire immediately after boot.
                    self.last_speak_ts = float(_ts)
                # Restore prev organism so the first post-boot tick
                # doesn't see "None -> BALANCE" as a shift.  The entry
                # stores it under "organism" (== body_organism_bc).
                _org = newest.get("organism")
                if isinstance(_org, str) and _org:
                    self.state.organism = _org
                # Coherence, if present, helps _adaptive_idle_period
                # pick a realistic window immediately instead of 0.5x
                # base (which would shorten the idle window and fire
                # a spurious idle question).
                try:
                    _coh = newest.get("coherence")
                    if isinstance(_coh, (int, float)):
                        self.state.coherence = float(_coh)
                except Exception:
                    pass
                # Rehydrate the recent_kinds / recent_bridges / dom_ops
                # windows too, so meta-pattern detectors have their
                # semantic horizon restored rather than starting blank.
                for _e in list(self.history)[-6:]:
                    _sh = (_e.get("shift") or "").split(":", 1)[0]
                    if _sh:
                        self.recent_kinds.append(_sh)
                    _br = _e.get("bridges") or []
                    if isinstance(_br, list):
                        self.recent_bridges.append(list(_br))
                    _op = _e.get("dominant_op") or ""
                    self.recent_dom_ops.append(str(_op))
        except Exception:
            # If any of the above misbehaves, leave the daemon in its
            # original post-hydrate state -- better to fire one extra
            # first_observation than to crash the curiosity loop.
            pass

    def _persist_to_disk(self) -> None:
        """Snapshot the current deque to disk.  Coalesced to <=1/5s.

        Atomic-ish: write to a tmp file then os.replace to avoid partial
        reads by the Flask handler serving /curiosity/stream.  Never
        raises out of the daemon.
        """
        now = time.time()
        if (now - self._last_persist_ts) < self._persist_min_interval_s:
            return
        try:
            os.makedirs(_CURIOSITY_DIR, exist_ok=True)
            payload = {
                "saved_at": int(now),
                "count": len(self.history),
                "entries": list(self.history),
            }
            tmp = _CURIOSITY_HISTORY_PATH + ".tmp"
            with open(tmp, "w", encoding="utf-8") as f:
                json.dump(payload, f, ensure_ascii=False)
            os.replace(tmp, _CURIOSITY_HISTORY_PATH)
            self._last_persist_ts = now
        except Exception:
            # Disk failure must not break curiosity; swallow silently.
            pass

    def _one_tick(self) -> None:
        self.tick_count += 1
        cur = _snapshot(self.engine)

        # respect RED threat band -- pause curiosity while we're under attack
        # (the brain fold attaches this to every chat response, so we can't
        # read it from engine directly; but we already skip if the LAST chat
        # turn we observed was RED.  For autonomy we also peek at the security
        # channel via the brain fold if the app exposed it; otherwise we just
        # run.)
        if self.state.threat_band == "RED":
            self.paused_by_threat = True
            self.skip_threat += 1
            return
        self.paused_by_threat = False

        shift = _detect_shift(self.state, cur)
        if shift is None:
            # Nothing obvious changed.  If CK has been silent for longer
            # than the idle window, trigger an "idle" shift so he speaks
            # up unprompted -- a living creature notices itself even when
            # the world is quiet.
            shift = _idle_shift(self.state, cur, self.last_speak_ts)
        if shift is None:
            self.skip_quiet += 1
            self.state.update_from(cur)
            return

        # Meta-curiosity round 2 (richer): scan the actual bridges +
        # dominant_op that have fired across CK's recent questions and
        # override the shift if a semantic attractor has emerged.
        # These fire BEFORE the kind-streak meta because they read the
        # question STREAM (bridge-patterns, operator-gravity) rather
        # than just the shift KIND.  A bridge-streak across varied
        # shift kinds ("3 different detectors all landed on sigma_NS")
        # is more informative than a KIND-streak with no semantic
        # common element -- so it wins when both would fire.
        _meta_shift_2 = _detect_meta_pattern(
            self.recent_bridges, self.recent_dom_ops,
        )
        if _meta_shift_2 is not None:
            _mk = _meta_shift_2.split(":")[0]
            # Per-kind cooldown applies to meta-* too, so a persistent
            # attractor doesn't monopolize the stream.  Use the same
            # table but with a LONGER cooldown for meta-patterns (5x
            # the normal) since asking the same meta-question twice
            # in quick succession is more annoying than twice about a
            # shift kind.
            _last_meta_ts = self.last_shift_by_kind.get(_mk, 0.0)
            if (cur.last_tick - _last_meta_ts) >= (_KIND_COOLDOWN_S * 5.0):
                shift = _meta_shift_2
                if _mk == "meta_bridge":
                    self.meta_bridge_count += 1
                elif _mk == "meta_op_gravity":
                    self.meta_op_gravity_count += 1
                elif _mk == "meta_bridge_cold":
                    self.meta_bridge_cold_count += 1

        # Meta-curiosity: if CK has been asking about the same shift KIND
        # three times in a row, flip to a question ABOUT the questions --
        # "why do i keep noticing this particular kind of shift and not
        # others?"  This is what turns curiosity into reflection.  Fires
        # at most once per 3-question streak (the recent_kinds deque is
        # cleared after the meta fires).  Skipped when a richer
        # meta-pattern (bridge/op) already took over the turn.
        _kind_now = shift.split(":")[0]
        if (not _kind_now.startswith("meta_")
                and len(self.recent_kinds) == self.recent_kinds.maxlen
                and len(set(self.recent_kinds)) == 1
                and _kind_now == self.recent_kinds[-1]):
            shift = f"meta:{_kind_now}-streak"
            self.recent_kinds.clear()
            self.meta_count += 1
            # Skip the per-kind cooldown for meta -- it's intentional.

        # Per-kind cooldown: if the same shift KIND (proc_churn / organism /
        # T_star_cross / ...) fired very recently, skip this tick so noisy
        # signals don't monopolize the stream.  First-observation and idle
        # bypass the cooldown since they're inherently rare/intentional.
        # Meta kinds (meta, meta_bridge, meta_op_gravity, meta_bridge_cold)
        # have their own longer cooldown applied at detection time, so
        # they bypass this generic gate too.
        kind = shift.split(":")[0]
        now_ts = cur.last_tick
        _cooldown_bypass = (
            kind in ("first_observation", "idle")
            or kind.startswith("meta")
        )
        if not _cooldown_bypass:
            last_ts = self.last_shift_by_kind.get(kind, 0.0)
            if (now_ts - last_ts) < _KIND_COOLDOWN_S:
                self.skip_cooldown += 1
                self.state.update_from(cur)
                return
        self.last_shift_by_kind[kind] = now_ts
        if kind == "arc":
            self.arc_count += 1
        # Record this kind into the rolling recent-kinds deque so meta
        # detection sees the pattern on the NEXT tick.  Meta itself is
        # logged as its own kind, which resets the streak.
        self.recent_kinds.append(kind)

        # Pass the last few already-asked questions so _format_question
        # can pick a template whose formatted form isn't a recent repeat.
        # Window of 5 matches the recent_kinds / recent_bridges deques so
        # meta decisions and question-text dedup see the same horizon.
        _recent_qs = [
            (h.get("question") or "") for h in list(self.history)[-5:]
        ]
        q = _format_question(shift, self.state, cur,
                             recent_questions=_recent_qs)
        t0 = time.time()
        try:
            process_chat = getattr(self.api, "process_chat", None)
            if process_chat is None:
                raise RuntimeError("api.process_chat missing")
            resp = process_chat(self.session_id, q, "normal")
            dt = time.time() - t0
            # Pick up the threat band from the response so the NEXT tick
            # knows if we should pause.
            band = resp.get("security_threat_band")
            if isinstance(band, str):
                cur.threat_band = band
            # Frontier-bridge anchors that fired on this turn.  The
            # steer module exposes them directly as `bridges_fired` --
            # uniform across fresh generations and cache fastpath hits
            # via the meta roundtrip.  Fall back to parsing
            # text_structural only if the uniform field is missing
            # (older cache entries or non-steered paths).
            _bridges: List[str] = []
            try:
                _direct = resp.get("bridges_fired")
                if isinstance(_direct, list) and _direct:
                    _bridges = [str(x) for x in _direct]
                else:
                    _struct = resp.get("text_structural") or ""
                    for _ln in _struct.splitlines():
                        _ln = _ln.strip()
                        if _ln.startswith("frontier_bridge="):
                            _bridges.append(_ln[len("frontier_bridge="):])
            except Exception:
                _bridges = []
            entry = {
                "ts": int(time.time()),
                "shift": shift,
                "question": q,
                "answer": (resp.get("text") or "")[:320],
                "source": resp.get("source"),
                "coherence": resp.get("brain_coherence"),
                "gate_pass": resp.get("brain_gate_pass"),
                "dominant_op": resp.get("brain_dominant_op"),
                "organism": resp.get("body_organism_bc"),
                "bridges": _bridges,
                "dt_ms": int(dt * 1000),
            }
            self.history.append(entry)
            self.question_count += 1
            self.last_speak_ts = cur.last_tick
            # Feed the meta-pattern detectors.  We track bridges as a
            # LIST (so the detector can count unique bridges per turn)
            # and dominant_op as a single string (None becomes "" so
            # the deque length is stable).
            self.recent_bridges.append(list(_bridges))
            self.recent_dom_ops.append(
                str(resp.get("brain_dominant_op") or "")
            )
            self._persist_to_disk()
        except Exception as e:
            self.error_count += 1
            self.history.append({
                "ts": int(time.time()),
                "shift": shift,
                "question": q,
                "error": f"{type(e).__name__}: {e}",
            })
            self._persist_to_disk()
        finally:
            self.state.update_from(cur)

    def _run(self) -> None:
        # Small jittered start so curiosity doesn't fire on the same cadence
        # as other background loops.
        time.sleep(random.uniform(2.0, 6.0))
        while self.running:
            try:
                self._one_tick()
            except Exception as e:
                # The daemon should NEVER die silently.
                self.error_count += 1
                self.history.append({
                    "ts": int(time.time()),
                    "error": f"tick_crashed:{type(e).__name__}:{e}",
                })
                try:
                    self._persist_to_disk()
                except Exception:
                    pass
            # sleep with a small jitter so adjacent machines / loops don't
            # align deterministically.
            time.sleep(self.period * random.uniform(0.85, 1.15))

    def start(self) -> None:
        if self.running:
            return
        self.running = True
        self.thread = threading.Thread(
            target=self._run, daemon=True, name="ck_curiosity",
        )
        self.thread.start()

    def stop(self) -> None:
        self.running = False


def mount_curiosity(api: Any, engine: Any) -> Dict[str, Any]:
    """Install the curiosity daemon.  Returns a status dict.  Never raises."""
    enabled = os.environ.get("CK_CURIOSITY", "1").strip()
    if enabled in ("0", "false", "False", "no", "NO"):
        return {"mounted": False, "reason": "CK_CURIOSITY=0"}

    sensorium = getattr(engine, "sensorium", None)
    if sensorium is None:
        return {
            "mounted": False,
            "reason": "engine has no .sensorium attribute",
        }

    try:
        period = float(os.environ.get("CK_CURIOSITY_PERIOD", "45"))
    except ValueError:
        period = 45.0
    session_id = os.environ.get("CK_CURIOSITY_SESSION", "ck_curiosity")

    daemon = _CuriosityDaemon(
        api=api, engine=engine, period=period, session_id=session_id,
    )
    daemon.start()

    n_routes = _register_curiosity_routes(api, daemon)

    return {
        "mounted": True,
        "period": period,
        "session_id": session_id,
        "routes_registered": n_routes,
    }


def _register_curiosity_routes(api: Any, daemon: _CuriosityDaemon) -> int:
    try:
        app = getattr(api, "_app", None)
        if app is None:
            return 0
        from flask import request, jsonify
    except Exception:
        return 0

    @app.route("/curiosity/stream", methods=["GET"])
    def _curiosity_stream():  # type: ignore[unused-ignore]
        try:
            # newest-first, cap at 32 entries for UI consumption
            items = list(daemon.history)
            items.reverse()
            return jsonify({
                "ok": True,
                "count": len(items),
                "entries": items[:32],
            })
        except Exception as e:
            return jsonify({
                "ok": False, "error": f"{type(e).__name__}: {e}",
            }), 500

    @app.route("/curiosity/stats", methods=["GET"])
    def _curiosity_stats():  # type: ignore[unused-ignore]
        try:
            return jsonify({
                "ok": True,
                "period_s": daemon.period,
                "running": daemon.running,
                "tick_count": daemon.tick_count,
                "question_count": daemon.question_count,
                "skip_quiet": daemon.skip_quiet,
                "skip_threat": daemon.skip_threat,
                "skip_cooldown": daemon.skip_cooldown,
                "error_count": daemon.error_count,
                "meta_count": daemon.meta_count,
                "meta_bridge_count": daemon.meta_bridge_count,
                "meta_op_gravity_count": daemon.meta_op_gravity_count,
                "meta_bridge_cold_count": daemon.meta_bridge_cold_count,
                "arc_count": daemon.arc_count,
                "recent_kinds": list(daemon.recent_kinds),
                "recent_bridges": [list(b) for b in daemon.recent_bridges],
                "recent_dom_ops": list(daemon.recent_dom_ops),
                "kind_cooldown_s": _KIND_COOLDOWN_S,
                "last_shift_by_kind": {
                    k: int(v) for k, v in daemon.last_shift_by_kind.items()
                },
                "paused_by_threat": daemon.paused_by_threat,
                "last_state": {
                    "organism": daemon.state.organism,
                    "coherence": round(daemon.state.coherence, 4),
                    "active_layers": daemon.state.active_layers,
                    "threat_band": daemon.state.threat_band,
                    "process_count": daemon.state.process_count,
                },
            })
        except Exception as e:
            return jsonify({
                "ok": False, "error": f"{type(e).__name__}: {e}",
            }), 500

    @app.route("/curiosity/poke", methods=["POST"])
    def _curiosity_poke():  # type: ignore[unused-ignore]
        """Force an immediate curiosity tick regardless of shift detection.

        G6-gated because it injects an unsolicited self-question into the
        scored turn log.
        """
        if request.args.get("i_mean_it") != "1":
            return jsonify({
                "ok": False,
                "error": "poke requires ?i_mean_it=1 (G6)",
            }), 400
        try:
            # force a shift so the tick produces a question
            prev_organism = daemon.state.organism
            daemon.state.organism = "__force__"
            daemon._one_tick()  # noqa: SLF001
            # restore so detection logic works normally on the next real tick
            if prev_organism is not None:
                daemon.state.organism = prev_organism
            last = daemon.history[-1] if daemon.history else None
            return jsonify({"ok": True, "last": last})
        except Exception as e:
            return jsonify({
                "ok": False, "error": f"{type(e).__name__}: {e}",
            }), 500

    return 3
