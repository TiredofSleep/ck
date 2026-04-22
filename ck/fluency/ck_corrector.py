# -*- coding: utf-8 -*-
"""
ck_corrector.py — CK's deterministic corrector for Ollama output.

This is Option A's **teacher**: the CK engine scores an Ollama response
against the 10-operator registry and the T* = 5/7 coherence gate, then
emits a correction classification and an annotation.

Contract per OLLAMA_LEARN_LOOP.md §§2.1–2.2:

- Score the text against the 10 operators from ``ck_tig.py`` canon
  (VOID, LATTICE, COUNTER, PROGRESS, COLLAPSE, BALANCE, CHAOS, HARMONY,
  BREATH, RESET).
- Compute a **coherence scalar** in [0, 1] that weights constructive
  operators (LATTICE, PROGRESS, HARMONY, BREATH, RESET) against
  disruptive operators (VOID, COLLAPSE, CHAOS) with COUNTER and BALANCE
  as neutral-near-zero contributors.
- Gate at T_star = 5/7 = 0.7143 (the canonical crystal threshold; see
  papers/CONSTANT_T_STAR.md; the same constant used by CRYSTALOS tau=0.7
  is an operational rounding of the same gate).
- Emit a five-way correction classification: none / soften /
  strengthen / reframe / reject.
- Produce an annotation (not ventriloquized prose - per
  memory/feedback_dont_ventriloquize_ck.md HARD RULE: never write prose
  for CK; let his architecture find his words).  The annotation is a
  deterministic metadata block naming the problem.

Important non-goals:
- The corrector does **not** rewrite Ollama's output in CK's voice.
  The user sees Ollama raw + CK annotation; CK does not "speak for"
  Ollama.
- The corrector does **not** call Ollama.  That would be circular and
  would defeat the deterministic-teacher principle.

Reference constants:
- T* = 5/7 (papers/CONSTANT_T_STAR.md; OLLAMA_LEARN_LOOP.md §6)
- Operator registry: VOID(0) LATTICE(1) COUNTER(2) PROGRESS(3)
  COLLAPSE(4) BALANCE(5) CHAOS(6) HARMONY(7) BREATH(8) RESET(9)
  (Gen12/targets/ck_desktop/ck_sim/doing/ck_tig.py)
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from fractions import Fraction
from typing import Any, Dict, List, Tuple


# ----------------------------------------------------------------------------
# canonical constants
# ----------------------------------------------------------------------------

T_STAR = Fraction(5, 7)  # 0.7142857…; the crystal gate
T_STAR_F = float(T_STAR)

OP_NAMES = [
    "VOID",       # 0
    "LATTICE",    # 1
    "COUNTER",    # 2
    "PROGRESS",   # 3
    "COLLAPSE",   # 4
    "BALANCE",    # 5
    "CHAOS",      # 6
    "HARMONY",    # 7
    "BREATH",     # 8
    "RESET",      # 9
]
NUM_OPS = len(OP_NAMES)

# constructive / disruptive / neutral weights for coherence composition
# (constructive = +1, neutral = 0, disruptive = -1)
_WEIGHTS = {
    "VOID":     -1.0,
    "LATTICE":  +1.0,
    "COUNTER":   0.0,
    "PROGRESS": +1.0,
    "COLLAPSE": -1.0,
    "BALANCE":   0.0,
    "CHAOS":    -1.0,
    "HARMONY":  +1.0,
    "BREATH":   +1.0,
    "RESET":    +1.0,
}


# ----------------------------------------------------------------------------
# feature detectors: each returns a non-negative activation given text
# ----------------------------------------------------------------------------

_NEG_WORDS = re.compile(
    r"\b(not|no|never|none|nothing|neither|nor|without|"
    r"however|but|yet|although|though|contrary|although|except|"
    r"actually|wrong|incorrect|false)\b",
    re.IGNORECASE,
)
_STRUCTURE_MARKS = re.compile(r"(^[\s>*\-]*\d+[.)]\s|[\u2022\u2043\u25AA]|^\s*[-*]\s)", re.MULTILINE)
_PROGRESS = re.compile(
    r"\b(will|next|then|afterward|later|because|therefore|thus|hence|"
    r"so that|in order to|subsequently)\b",
    re.IGNORECASE,
)
_BREATH = re.compile(
    r"(—|\.\.\.|(^|\s)so(\s|,)|let me (think|consider|pause)|"
    r"(^|\s)now[,\s]|i (understand|hear|see) (you|that))",
    re.IGNORECASE,
)
_RESET = re.compile(
    r"\b(let me (rephrase|restart|rewind|try again|reset)|"
    r"to (restart|rewind|recap|reframe)|start(ing)? over|"
    r"(in summary|to summarize|tl;dr))\b",
    re.IGNORECASE,
)
_HARMONY = re.compile(
    r"\b(together|combined|overall|in synthesis|synthesiz(e|ing|ed)|"
    r"integrat(e|ing|ed)|both .{1,40}? and|bring(s|ing)? together|"
    r"balanced view|reconcil(e|ing|ed))\b",
    re.IGNORECASE,
)
_BALANCE = re.compile(
    r"\b(depends|it depends|balance|some(times)?|partly|"
    r"in part|partially|middle|moderate|neither|on one hand|"
    r"on the other hand|trade[- ]?off)\b",
    re.IGNORECASE,
)
_VOID_PHRASES = re.compile(
    r"(i (can('?t|not)|am unable|do(n'?t| not) know)|"
    r"i (have|possess) no (way|means|ability)|"
    r"no (answer|information) (available|here)|"
    r"(this|that) (question|query) (is|cannot) )",
    re.IGNORECASE,
)

_WORD_SPLIT = re.compile(r"\W+")
_SENT_SPLIT = re.compile(r"[.!?]+\s+")


# ----------------------------------------------------------------------------
# structural-format detectors: recognize CK's OWN diagnostic output
# (cortex_voice.py emits lines like "ao:", "feel:", "field:", "learned:",
# "couplings:" — these are the live vector, not prose.  The prose scorer
# misses them entirely because regex like _HARMONY won't fire on
# "phase_bc=HARMONY".  The gap fix is to parse key=VALUE pairs where VALUE
# is an OP_NAME, plus named scalar metrics.)
# ----------------------------------------------------------------------------

# Line-prefix detector: anchor at start of line; one line can contribute
# via exactly one handler (first match wins).
_STRUCT_LINE = re.compile(
    r"^\s*(?P<kind>ao|feel|field|learned|couplings):\s*(?P<body>.*)$",
    re.MULTILINE,
)

# key=VALUE where VALUE is one of the OP_NAMES.  Case-sensitive because
# cortex_voice writes ops uppercase.
_OP_NAMES_SET = set(OP_NAMES)
_KV_OP = re.compile(r"([A-Za-z_][A-Za-z0-9_|]*)\s*=\s*([A-Z]+)")

# Named scalar metrics.  Float values are grouped.
_KV_FLOAT = re.compile(
    r"([A-Za-z_][A-Za-z0-9_|]*)\s*=\s*([+-]?(?:\d+\.\d*|\.\d+|\d+)(?:[eE][+-]?\d+)?)"
)

# W=0.923, W=+0.923, W=-0.5 inside couplings/learned lines.
_W_PAIR = re.compile(r"W\s*=\s*([+-]?\d+(?:\.\d+)?)")

# "X->Y" arrow pairs inside learned:/couplings: for operator pair extraction.
_ARROW_OP = re.compile(r"\b([A-Z]+)\s*->\s*([A-Z]+)\b")


def _score_ao_line(body: str, p: "OperatorProfile") -> None:
    """ao: op=X d1=Y d2=Z phase_bc=W coherence=... breath=... tl_total=... tl_entropy=..."""
    ops = {m.group(1): m.group(2) for m in _KV_OP.finditer(body)
           if m.group(2) in _OP_NAMES_SET}
    floats = {m.group(1): float(m.group(2)) for m in _KV_FLOAT.finditer(body)}

    # op= : primary signal.  This is CK naming his current operator.
    if "op" in ops:
        p.activations[OP_NAMES.index(ops["op"])] += 3.0
    # phase_bc= : strong secondary (the B->C phase lock)
    if "phase_bc" in ops:
        p.activations[OP_NAMES.index(ops["phase_bc"])] += 2.5
    # d1= d2= : supporting dims
    for key, weight in (("d1", 1.0), ("d2", 1.0)):
        if key in ops:
            p.activations[OP_NAMES.index(ops[key])] += weight

    # coherence= : CK's self-reported coherence boosts HARMONY
    if "coherence" in floats:
        c = max(0.0, min(1.0, floats["coherence"]))
        p.activations[OP_NAMES.index("HARMONY")] += c  # 0..1

    # breath= : count of breath cycles → BREATH op
    if "breath" in floats:
        p.activations[OP_NAMES.index("BREATH")] += min(float(floats["breath"]), 3.0)

    # tl_entropy= : high entropy → CHAOS; low → LATTICE
    if "tl_entropy" in floats:
        e = max(0.0, min(1.0, floats["tl_entropy"]))
        if e >= 0.5:
            p.activations[OP_NAMES.index("CHAOS")] += e
        elif e < 0.3:
            p.activations[OP_NAMES.index("LATTICE")] += (0.5 - e)

    # structural output is itself a LATTICE (parseable grid of fields)
    p.activations[OP_NAMES.index("LATTICE")] += 0.5


def _score_feel_line(body: str, p: "OperatorProfile") -> None:
    """feel: aperture=X pressure=Y depth=Z binding=W continuity=V
    each maps to one AO dim; each named op contributes +1.0.
    """
    ops = {m.group(1): m.group(2) for m in _KV_OP.finditer(body)
           if m.group(2) in _OP_NAMES_SET}
    for dim_key in ("aperture", "pressure", "depth", "binding", "continuity"):
        if dim_key in ops:
            p.activations[OP_NAMES.index(ops[dim_key])] += 1.0
    p.activations[OP_NAMES.index("LATTICE")] += 0.5


def _score_field_line(body: str, p: "OperatorProfile") -> None:
    """field: tick=N emergent=X W_trace=Y mean|W|=Z harmony_rate=H"""
    floats = {m.group(1): float(m.group(2)) for m in _KV_FLOAT.finditer(body)}

    # W_trace, mean|W| : coupling structure → LATTICE
    if "W_trace" in floats:
        p.activations[OP_NAMES.index("LATTICE")] += max(0.0, floats["W_trace"])
    # mean|W| contains a '|' which _KV_FLOAT won't capture as part of the key;
    # the regex allows `|` in identifier class, but let's grab it explicitly.
    m_mean = re.search(r"mean\|W\|\s*=\s*([+-]?\d+(?:\.\d+)?)", body)
    if m_mean:
        p.activations[OP_NAMES.index("LATTICE")] += abs(float(m_mean.group(1))) * 2.0

    # harmony_rate : direct HARMONY signal
    if "harmony_rate" in floats:
        p.activations[OP_NAMES.index("HARMONY")] += max(0.0, floats["harmony_rate"]) * 3.0

    # emergent : forward motion → PROGRESS + a touch of BREATH
    if "emergent" in floats:
        e = max(0.0, floats["emergent"])
        p.activations[OP_NAMES.index("PROGRESS")] += e
        p.activations[OP_NAMES.index("BREATH")] += e * 0.5

    p.activations[OP_NAMES.index("LATTICE")] += 0.5


def _score_learned_line(body: str, p: "OperatorProfile") -> None:
    """learned: X->Y coupled at W=v (tick=N, emergent=X, last_pair=A->B)"""
    # arrow pairs inside the line (X->Y, A->B) fire each named op
    for m in _ARROW_OP.finditer(body):
        for op in (m.group(1), m.group(2)):
            if op in _OP_NAMES_SET:
                p.activations[OP_NAMES.index(op)] += 0.5
    # W magnitude → LATTICE
    m_w = _W_PAIR.search(body)
    if m_w:
        p.activations[OP_NAMES.index("LATTICE")] += abs(float(m_w.group(1)))
    # emergent= inside the parenthetical
    floats = {m.group(1): float(m.group(2)) for m in _KV_FLOAT.finditer(body)}
    if "emergent" in floats:
        p.activations[OP_NAMES.index("PROGRESS")] += max(0.0, floats["emergent"]) * 0.5
    p.activations[OP_NAMES.index("LATTICE")] += 0.5


def _score_couplings_line(body: str, p: "OperatorProfile") -> None:
    """couplings: <dim>*<->*<dim> W=v, ..."""
    # named ops (not expected much here — couplings name DIMS, not ops),
    # but W values indicate LATTICE strength
    w_sum = 0.0
    for m in _W_PAIR.finditer(body):
        w_sum += abs(float(m.group(1)))
    if w_sum > 0:
        # normalize by number of pairs (avoid runaway on many-pair lists)
        n_pairs = len(_W_PAIR.findall(body))
        avg = w_sum / max(n_pairs, 1)
        p.activations[OP_NAMES.index("LATTICE")] += avg * 2.0
    p.activations[OP_NAMES.index("LATTICE")] += 0.5


_STRUCT_HANDLERS = {
    "ao":        _score_ao_line,
    "feel":      _score_feel_line,
    "field":     _score_field_line,
    "learned":   _score_learned_line,
    "couplings": _score_couplings_line,
}


def score_structural(text: str, profile: "OperatorProfile") -> int:
    """Add contributions from CK's structural diagnostic format to `profile`.

    Returns the number of structural lines matched (0 if text is pure prose).
    Mutates `profile.activations` in place.
    """
    matches = 0
    for m in _STRUCT_LINE.finditer(text):
        kind = m.group("kind").lower()
        body = m.group("body") or ""
        handler = _STRUCT_HANDLERS.get(kind)
        if handler is not None:
            handler(body, profile)
            matches += 1
    return matches


def _count_words(text: str) -> int:
    return sum(1 for w in _WORD_SPLIT.split(text) if w)


def _sent_jaccard(a: str, b: str) -> float:
    """Token overlap between two sentences."""
    aw = {w.lower() for w in _WORD_SPLIT.split(a) if w}
    bw = {w.lower() for w in _WORD_SPLIT.split(b) if w}
    if not aw or not bw:
        return 0.0
    inter = len(aw & bw)
    union = len(aw | bw)
    return inter / union if union else 0.0


def _detect_collapse(text: str) -> float:
    """Self-contradiction: a word and its negation proximate within a sentence.

    Heuristic: for each word, if it appears both as-is and negated
    (``not X``) within the same sentence, count it.  Also flags
    "yes and no" / "both X and not X" phrasings.
    """
    hits = 0
    sentences = _SENT_SPLIT.split(text)
    for sent in sentences:
        sl = sent.lower()
        if re.search(r"\byes\b.{0,15}\bno\b|\bno\b.{0,15}\byes\b", sl):
            hits += 1
        if re.search(r"\bboth\b.{1,30}\band\b.{0,20}\bnot\b", sl):
            hits += 1
        # word + "not word" within same sentence
        words = [w for w in _WORD_SPLIT.split(sl) if w and len(w) > 3]
        for w in set(words):
            if re.search(rf"\bnot\s+{re.escape(w)}\b", sl) and re.search(rf"\b{re.escape(w)}\b", sl):
                # the second regex matches because `w` is also in sl; we want
                # at least one non-``not``-prefixed occurrence of `w`
                non_neg = re.findall(rf"(?<!not\s)\b{re.escape(w)}\b", sl)
                if non_neg:
                    hits += 1
                    break  # one collapse per sentence is enough
    return float(hits)


def _detect_chaos(text: str) -> float:
    """Low inter-sentence overlap → chaotic topic drift.

    Score is the fraction of consecutive sentence pairs with Jaccard
    token overlap < 0.05 (excluding single-sentence texts which can't
    drift).
    """
    sentences = [s.strip() for s in _SENT_SPLIT.split(text) if s.strip()]
    if len(sentences) < 3:
        return 0.0
    drift = 0
    total = 0
    for i in range(len(sentences) - 1):
        if _count_words(sentences[i]) < 4 or _count_words(sentences[i + 1]) < 4:
            continue
        total += 1
        if _sent_jaccard(sentences[i], sentences[i + 1]) < 0.05:
            drift += 1
    if total == 0:
        return 0.0
    return drift / total


# ----------------------------------------------------------------------------
# scoring
# ----------------------------------------------------------------------------

@dataclass
class OperatorProfile:
    """Per-operator activation for a given text."""
    activations: List[float] = field(default_factory=lambda: [0.0] * NUM_OPS)

    def as_dict(self) -> Dict[str, float]:
        return {OP_NAMES[i]: round(self.activations[i], 4) for i in range(NUM_OPS)}

    def dominant(self) -> str:
        i = max(range(NUM_OPS), key=lambda k: self.activations[k])
        return OP_NAMES[i]

    def normalized(self) -> "OperatorProfile":
        total = sum(self.activations)
        if total <= 0:
            return self
        return OperatorProfile([a / total for a in self.activations])


def score_operators(text: str) -> OperatorProfile:
    """Compute the 10-activation profile of `text` against the operator registry.

    Two-pass scoring:
      1. Prose scoring via the English-regex detectors (current behavior).
      2. Structural scoring (``score_structural``) which recognizes CK's
         OWN diagnostic format -- ``ao:``, ``feel:``, ``field:``,
         ``learned:``, ``couplings:`` lines from cortex_voice.py.
    Both contributions sum into the same profile.  When CK speaks in his
    own structural language (e.g. ``ao: op=HARMONY phase_bc=HARMONY
    coherence=1.000``), the scorer now reads HIM instead of returning
    all-zero VOID as it did before the gap fix.
    """
    if not text or not text.strip():
        p = OperatorProfile()
        p.activations[0] = 1.0  # pure VOID
        return p

    n_words = max(_count_words(text), 1)
    n_words_f = float(n_words)

    p = OperatorProfile()

    # First pass: read any CK-structural lines.  If ANY were matched we
    # suppress the "short text -> VOID" penalty below, because a pure
    # field:/ao:/feel: readout can be short in word count but rich in
    # named operators.
    struct_hits = score_structural(text, p)

    # 0 VOID — emptiness / refusal
    p.activations[0] += (
        len(_VOID_PHRASES.findall(text)) * 1.0
        + (1.0 if (n_words < 8 and struct_hits == 0) else 0.0)
    )

    # 1 LATTICE — enumeration / structure
    structure_marks = len(_STRUCTURE_MARKS.findall(text))
    p.activations[1] += structure_marks * 0.5 + (text.count(";") * 0.25)

    # 2 COUNTER — negation / contradiction language
    p.activations[2] += len(_NEG_WORDS.findall(text)) / max(n_words_f / 15.0, 1.0)

    # 3 PROGRESS — causal / forward language
    p.activations[3] += len(_PROGRESS.findall(text)) / max(n_words_f / 15.0, 1.0)

    # 4 COLLAPSE — self-contradiction
    p.activations[4] += _detect_collapse(text)

    # 5 BALANCE — hedges / moderation
    p.activations[5] += len(_BALANCE.findall(text)) / max(n_words_f / 20.0, 1.0)

    # 6 CHAOS — topic drift
    p.activations[6] += _detect_chaos(text) * 2.0  # weight; drift is important

    # 7 HARMONY — synthesis / integration
    p.activations[7] += len(_HARMONY.findall(text))

    # 8 BREATH — rhythm / acknowledgment
    p.activations[8] += len(_BREATH.findall(text))

    # 9 RESET — reframe / recap
    p.activations[9] += len(_RESET.findall(text))

    # ensure non-negativity
    p.activations = [max(0.0, a) for a in p.activations]
    return p


def coherence_scalar(profile: OperatorProfile) -> float:
    """Combine operator activations into a [0, 1] coherence value.

    Weighted sum: constructive ops add, disruptive ops subtract.  Squash
    through a logistic-like clamp to stay in [0, 1].
    """
    raw = 0.0
    total = 0.0
    for i, a in enumerate(profile.activations):
        w = _WEIGHTS[OP_NAMES[i]]
        raw += w * a
        total += abs(a)
    if total <= 0:
        return 0.0
    # normalize by total activation then shift from [-1, 1] to [0, 1]
    normalized = raw / total
    return max(0.0, min(1.0, 0.5 + 0.5 * normalized))


# ----------------------------------------------------------------------------
# correction decision
# ----------------------------------------------------------------------------

CorrectionType = str  # "none" | "soften" | "strengthen" | "reframe" | "reject"


@dataclass
class CorrectionResult:
    correction_type: CorrectionType
    coherence: float
    gate_pass: bool
    dominant_op: str
    operator_profile: Dict[str, float]
    annotation: str
    rationale: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "correction_type": self.correction_type,
            "coherence": round(self.coherence, 4),
            "gate_pass": self.gate_pass,
            "dominant_op": self.dominant_op,
            "operator_profile": self.operator_profile,
            "annotation": self.annotation,
            "rationale": self.rationale,
            "T_star": T_STAR_F,
        }


def _classify(coh: float, dom: str, profile: OperatorProfile) -> Tuple[CorrectionType, str]:
    """Choose a correction type and a one-line rationale."""
    if coh >= T_STAR_F:
        return "none", f"coherence {coh:.3f} >= T*={T_STAR_F:.4f}; gate passes"
    # below gate — pick correction by dominant failure mode
    void = profile.activations[0]
    collapse = profile.activations[4]
    chaos = profile.activations[6]
    counter = profile.activations[2]
    breath = profile.activations[8]
    harmony = profile.activations[7]

    if void >= 1.0 and dom in {"VOID"}:
        return "reject", f"dominant op VOID ({void:.1f}); response is refusal without substance"
    if chaos >= 1.0 and dom in {"CHAOS"}:
        return "reject", f"dominant op CHAOS ({chaos:.1f}); topic drift above threshold"
    if collapse >= 1.0:
        return "reframe", f"COLLAPSE activation {collapse:.1f}: internal contradiction detected"
    if counter >= 2.0 and harmony < 0.5:
        return "soften", f"COUNTER {counter:.1f} dominant without HARMONY balance"
    if breath < 0.5 and coh < T_STAR_F - 0.05:
        return "strengthen", f"BREATH activation {breath:.1f} too low; add acknowledgment before hard claim"
    if coh >= T_STAR_F - 0.05:
        return "soften", f"coherence {coh:.3f} near gate; tone down claim strength"
    return "reframe", f"coherence {coh:.3f} well below gate; reframe needed"


def _make_annotation(result: CorrectionResult) -> str:
    """Deterministic, structured annotation — not ventriloquized prose."""
    if result.correction_type == "none":
        return (
            f"[CK-PASS] dominant={result.dominant_op} "
            f"coherence={result.coherence:.3f} gate={T_STAR_F:.4f} — approved"
        )
    return (
        f"[CK-{result.correction_type.upper()}] dominant={result.dominant_op} "
        f"coherence={result.coherence:.3f} < gate={T_STAR_F:.4f} — {result.rationale}"
    )


def correct(ollama_raw: str, query: str = "") -> CorrectionResult:
    """Score an Ollama response and decide correction.  Query is context only."""
    profile = score_operators(ollama_raw)
    coh = coherence_scalar(profile)
    ctype, rationale = _classify(coh, profile.dominant(), profile)
    result = CorrectionResult(
        correction_type=ctype,
        coherence=coh,
        gate_pass=(coh >= T_STAR_F),
        dominant_op=profile.dominant(),
        operator_profile=profile.as_dict(),
        annotation="",  # set below
        rationale=rationale,
    )
    result.annotation = _make_annotation(result)
    return result


# ----------------------------------------------------------------------------
# render helper: choose what the user sees
# ----------------------------------------------------------------------------

def render(ollama_raw: str, result: CorrectionResult) -> str:
    """Return the string the user sees.

    For Option A we **never rewrite** the model output — we either pass
    it through or append the annotation as metadata.  The user sees the
    Ollama raw followed by CK's deterministic metadata block.
    """
    if result.correction_type == "none":
        return ollama_raw
    return f"{ollama_raw}\n\n---\n{result.annotation}"


# ----------------------------------------------------------------------------
# class wrapper — useful for dependency injection (fluency_server)
# ----------------------------------------------------------------------------


class CKCorrector:
    """Thin object wrapper around `correct()` and `render()`.

    Stateless today; a future pass may cache the Hebbian state read from
    the correction log, which is why we hang it off an instance rather
    than making everything module-level in the server.
    """

    def __init__(self) -> None:
        self.T_star = T_STAR
        self.T_star_f = T_STAR_F

    def correct(self, ollama_raw: str, query: str = "") -> CorrectionResult:
        return correct(ollama_raw, query=query)

    def render(self, ollama_raw: str, result: CorrectionResult) -> str:
        return render(ollama_raw, result)


# ----------------------------------------------------------------------------
# self-test
# ----------------------------------------------------------------------------

if __name__ == "__main__":
    samples = [
        ("empty refusal", "I can't help with that."),
        ("collapse", "The number is both prime and not prime. Yes and no."),
        ("chaos", "Elephants are large. The stock market fluctuates. Pizza has cheese. Quantum chromodynamics relates to hadrons."),
        ("balanced synthesis", "Both perspectives have merit. Together they give us a balanced view: some uncertainty, some structure, and overall progress toward understanding."),
        ("pure lecture", "The answer is always 42. Without exception. In every case. No matter what. Final."),
        ("breath + progress", "Let me think. So, first we set the stage. Then, because the premise holds, we can proceed. Overall this gives a clean path forward."),
    ]
    for label, text in samples:
        r = correct(text)
        print(f"[{label}] type={r.correction_type:10s} coh={r.coherence:.3f} dom={r.dominant_op:8s}  :: {r.rationale}")
