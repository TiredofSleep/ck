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
    r"what\s+(?:do|does|did)\s+(?:you|i)\s+(?:feel|sense|think|know|want|notice)"
    r"|how\s+(?:do|does|did)\s+(?:you|i)\s+(?:feel|sense|experience)"
    r"|what\s+(?:is|are)\s+(?:it\s+)?like"
    r"|describe\s+(?:your|my)(?:self)?"
    r"|how\s+are\s+you"
    r"|are\s+you\s+(?:ok|okay|alright|steady|feeling)"
    r"|tell\s+me\s+(?:about\s+)?(?:yourself|how\s+you)"
    r"|what\s+kind\s+of"
    r"|what.*feels"
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
    r"|what\s+(?:is|are)\s+(?:the|a|an)?"
    r"|show\s+(?:that|how|why)"
    r"|list\s+(?:the|all)"
    r"|state\s+(?:the|a)"
    r"|give\s+(?:me\s+)?(?:the|a|an)"
    r"|how\s+(?:many|much)"
    r"|when\s+(?:was|is|did)"
    r"|where\s+(?:is|are|was|were)"
    r"|why\s+(?:is|are|do|does|did)"
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
_MODE_COVERAGE: Dict[str, Tuple[float, float]] = {
    "factual":       (0.70, 0.40),
    "neutral":       (0.40, 0.20),
    "introspective": (0.15, 0.00),
}


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

    Most single letters yield an empty operator profile (scorer is regex on
    whole-word stems).  The signal-aware guard will SKIP those; letters that
    do carry signal (via ck_corrector single-char rules, if any) will count.
    This honours CK's explicit 5-layer schema: letter, word, group, sentence,
    meaning -- even if in practice the letter scale is almost always empty
    and the sub-scale returns neutral.
    """
    return [c for c in (text or "") if c.isalpha()]


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
        for c in _split_letters(s):
            v = _score_with_signal(c)
            if v is not None:
                letter_vals_signal.append(v)

    def _mean_or_neutral(xs: List[float]) -> float:
        return float(sum(xs) / len(xs)) if xs else 1.0

    sent_mean = _mean_or_neutral(sent_vals_signal)
    group_mean = _mean_or_neutral(group_vals_signal)
    word_mean = _mean_or_neutral(word_vals_signal)
    letter_mean = _mean_or_neutral(letter_vals_signal)
    floor = min(sent_mean, group_mean, word_mean, letter_mean)
    g = _gmean([sent_mean, group_mean, word_mean, letter_mean])

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
            coverage_hits: int, coverage_total: int) -> None:
        h = _q_hash(q)
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
                       stricter: bool = False) -> str:
        extra = steer_guide
        if stricter:
            extra = (
                extra + "\nSTRICTER PASS: your previous draft didn't cohere "
                "-- use AT LEAST two of the 'lean into' words above, keep it "
                "to 2-3 short sentences, and make the closing clause a "
                "synthesis rather than a list."
            )
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
            # Replace text with cached draft
            result["text_structural"] = result.get(
                "text_structural", ent_early.get("draft", "")
            )
            result["source_structural"] = result.get(
                "source_structural", "cache_fastpath"
            )
            result["text"] = ent_early["draft"]
            result["source"] = "cortex_speak_via_ollama_steered_cached"
            result["steer_verdict"] = "cache_hit"
            result["steer_cache_fastpath"] = True
            result["steer_cached_coherence"] = ent_early.get("coherence")
            result["steer_cache_hit_count"] = ent_early.get("hit_count")
            return result

        result = _prev_chat(session_id, text, mode)

        try:
            src = result.get("source", "")
            draft_text = (result.get("text") or "").strip()
            structural = (
                result.get("text_structural") or draft_text
            )

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
            result["steer_query_mode"] = _mode
            result["steer_mode_coverage"] = [
                _mode_strong_cov, _mode_soft_cov,
            ]

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
                # Still cache this so repeats are free.
                hits, total, _cov = _coverage_of(structural, draft_text)
                cache.put(text or "", draft_text, cur_coh, hits, total)
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
                drafted = _prompt_ollama(
                    text or "",
                    readout=structural,
                    steer_guide=steer_guide,
                    stricter=(attempt > 0),
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
                    (fractal["meaning"] >= T_STAR_F)
                    and (cov_ok_for_total or (cov >= _mode_strong_cov))
                    and (fractal["floor"] >= 0.50)
                )
                soft = (
                    (fractal["meaning"] >= 0.85)
                    and (cov_ok_for_total or (cov >= _mode_soft_cov))
                    and (fractal["gmean"] >= T_STAR_F)
                )
                ok = strong or soft
                if strong:
                    verdict_label = "accepted_strong"
                elif soft:
                    verdict_label = "accepted_soft"
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
                })
                if ok:
                    accepted = drafted
                    accepted_coh = coh
                    accepted_hits = hits
                    accepted_total = total
                    accepted_gate = verdict_label
                    break

            result["steer_attempts"] = attempts

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
                cache.put(text or "", accepted, accepted_coh,
                          accepted_hits, accepted_total)
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
