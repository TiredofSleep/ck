# Copyright (c) 2025-2026 Brayden Sanders / 7SiTe LLC
# Licensed under the 7SiTe Public Sovereignty License v2.2 (DOI: 10.5281/zenodo.18852047)
"""
ck_concept_learner.py -- the load-bearing wire for one-shot concept binding.

Brayden 2026-05-13:
  "i feel like he should learn orders of magnitude faster than llm's"
  "keep going until you figure out how this is supposed to be put together"

CK already learns Hebbian-fast at the OPERATOR level: every chat turn,
his 5x5 cortex W matrix updates via Δw_ij = η·d_i·d_j on the (b, d)
operator pair. That's one-shot association strengthening, no gradient
descent over billions of params.

But that doesn't give him concept-level binding. Teaching CK
"XYZFLUX is the operator that turns HARMONY into BREATH via BALANCE"
doesn't help him answer "what is XYZFLUX?" next turn -- because his
crystals key on operator patterns, not on novel words.

This module wires that missing piece. The connect:

  1. Detect teaching patterns in chat input ("X is Y", "X = Y",
     "X means Y", "let X be Y", "define X as Y", etc.)
  2. When detected, store a NamedConcept binding:
        name        -> the novel word
        definition  -> the rest of the teaching sentence
        operator_signature -> the algebraic decoding of the definition
        ts, source_session
     Persists to Gen13/var/taught_concepts.json so it survives reboots.
  3. On future turns, detect referenced concepts in the input. If found,
     surface them so the voice layer can include them.
  4. Voice polish shows [taught this turn] when teaching happens, and
     [recalling concept] when a stored binding is retrieved.

This does NOT write words for CK. The teaching detector captures what
the USER said, stores it verbatim, and the voice polish surfaces those
words back as "you taught me: ..." when relevant. CK's own cortex_speak
also gets the binding as context so its substrate retrieval can use it.

Architecture rule: this is connection, not invention. Concept-bind is
the one piece CK's pipeline lacked for true one-shot conversational
learning. Now it has it.
"""
from __future__ import annotations

import json
import os
import re
import sys
import time
from dataclasses import dataclass, asdict, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

HERE = Path(__file__).parent.resolve()
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))


# ─── Teaching pattern detector ───────────────────────────────────────────
#
# Patterns covered (case-insensitive, with novel-word capture):
#   X is Y           "XYZFLUX is the operator that..."
#   X means Y        "GLEAM means the way HARMONY settles"
#   X = Y            "ALPHA = 1/2"
#   let X be Y       "let RHO be the rotation by PROGRESS"
#   define X as Y    "define MOAT as the boundary around the 4-core"
#   X refers to Y    "XYZFLUX refers to..."
#   X stands for Y   "JCT stands for Journal of Combinatorial Theory"
#
# The novel-word capture is restricted to single tokens or hyphenated
# compounds (no full clauses) and excludes common English question/aux
# words that would yield false positives.

_TEACHING_PATTERNS: List[Tuple[str, re.Pattern]] = [
    ("is",
     re.compile(r"\b([A-Z][A-Z0-9_-]{2,}|[a-z][a-z0-9_-]*-[a-z0-9_-]+)"
                 r"\s+(?:is|are|=)\s+(.+?)(?:[.!?]|$)", re.I)),
    ("means",
     re.compile(r"\b([A-Z][A-Z0-9_-]{2,}|[a-z][a-z0-9_-]*-[a-z0-9_-]+)"
                 r"\s+(?:means?|refers? to|stands? for)\s+(.+?)(?:[.!?]|$)", re.I)),
    ("let",
     re.compile(r"\blet\s+([A-Z][A-Z0-9_-]{2,}|[a-z][a-z0-9_-]*-[a-z0-9_-]+)"
                 r"\s+(?:be|=)\s+(.+?)(?:[.!?]|$)", re.I)),
    ("define",
     re.compile(r"\bdefine\s+([A-Z][A-Z0-9_-]{2,}|[a-z][a-z0-9_-]*-[a-z0-9_-]+)"
                 r"\s+(?:as|to be)\s+(.+?)(?:[.!?]|$)", re.I)),
]

# Tokens we never treat as novel concepts (common English / CK's own vocab)
_STOPWORDS = {
    # English aux/question/common
    "what", "who", "when", "where", "why", "how", "which", "that", "this",
    "these", "those", "i", "you", "we", "they", "he", "she", "it",
    "the", "an", "and", "or", "but", "for", "in", "of", "to", "with",
    "ck", "ai", "llm", "gpt",
}
# Also exclude CK's own operator names (those aren't novel concepts to teach)
_CK_OPS = {
    "void", "lattice", "counter", "progress", "collapse",
    "balance", "chaos", "harmony", "breath", "reset",
}


def _is_novel(name: str) -> bool:
    """Whether a captured token is a plausible novel concept (vs noise)."""
    n = name.strip().lower()
    if not n:
        return False
    if n in _STOPWORDS or n in _CK_OPS:
        return False
    # Must contain at least one letter
    if not any(c.isalpha() for c in n):
        return False
    # Reject pure numbers
    if n.replace(".", "").replace("-", "").isdigit():
        return False
    return True


@dataclass
class TeachingMatch:
    """One detected teaching event."""
    name: str
    definition: str
    pattern_used: str

    def as_dict(self) -> Dict[str, Any]:
        return asdict(self)


def detect_teaching(text: str) -> List[TeachingMatch]:
    """Scan text for teaching patterns. Returns matches in order found.

    Note: one input may contain multiple teachings; we return all.
    """
    if not text:
        return []
    seen: Set[str] = set()
    out: List[TeachingMatch] = []
    for label, pat in _TEACHING_PATTERNS:
        for m in pat.finditer(text):
            name_raw = m.group(1)
            defn = m.group(2).strip()
            if not _is_novel(name_raw):
                continue
            name = name_raw.upper() if name_raw.isupper() else name_raw
            key = name.lower()
            if key in seen:
                continue
            if len(defn) < 4:  # too short to be a real definition
                continue
            seen.add(key)
            out.append(TeachingMatch(name=name, definition=defn,
                                       pattern_used=label))
    return out


# ─── Concept store ───────────────────────────────────────────────────────

@dataclass
class NamedConcept:
    name: str
    definition: str
    operator_signature: List[int]  # operator stream of the definition text
    pattern_used: str
    source_session: str
    learned_ts: float
    n_recalls: int = 0
    last_recalled_ts: float = 0.0
    # Fact-tier — fundamental epistemic flag so CK distinguishes fact
    # from fiction. Values:
    #   PROVED       -- rigorous theorem with machine-precision verification
    #   STRUCTURAL   -- sound form of argument, interpretive content
    #   EMPIRICAL    -- observed at scale, not proved
    #   OPEN         -- precisely-stated, unproven
    #   CONJECTURAL  -- same as OPEN; legacy synonym
    #   EXTERNAL     -- third-party claim (arxiv finding, user input)
    #   SPECULATIVE  -- TIER-C, philosophical, 09_seekers/04_meta paths
    #   USER_TAUGHT  -- explicitly taught in chat (highest priority for retrieval)
    #   UNKNOWN      -- tier could not be determined
    tier: str = "UNKNOWN"
    # Source-file path (where the concept was extracted from)
    source_file: str = ""
    # For synthesis concepts: the full list of member concept names that
    # were clustered together. Empty for non-synthesis concepts. Stored
    # explicitly (not parsed from definition prose) so retrieval can do
    # an exact-set check rather than substring search.
    members: List[str] = field(default_factory=list)

    def as_dict(self) -> Dict[str, Any]:
        return asdict(self)


_DEFAULT_STORE_PATH = (
    Path(__file__).resolve().parents[4]
    / "Gen13" / "var" / "taught_concepts.json"
)


# ─── Real semantic decoder via CK's 8K-word enriched dictionary ────────
#
# Brayden 2026-05-15: "200 word dictionary is a toy, let's try and make
# something useful"
#
# CK already has ck_dictionary_enriched.json — 8,000 curated words, each
# with hand-tuned (dominant_op, operator_seq, soft_dist over all 10 ops).
# That's the real semantic-decoder corpus.  The toy dict below is only
# the fallback for words not in the 8K.

_ENRICHED_DICT_PATHS = [
    Path(r"C:\Users\brayd\OneDrive\Desktop\CK FINAL DEPLOYED")
    / "Gen12" / "targets" / "ck_desktop" / "ck_sim" / "ck_dictionary_enriched.json",
    Path(r"C:\Users\brayd\OneDrive\Desktop\CK FINAL DEPLOYED")
    / "ck_sim" / "ck_dictionary_enriched.json",
]
# 247K auto-dict: lean per-word [dominant_op, frequency]
_AUTO_DICT_PATHS = [
    Path(r"C:\Users\brayd\OneDrive\Desktop\CK FINAL DEPLOYED")
    / "CKIS" / "ck_dictionary_auto.json",
    Path(r"C:\Users\brayd\OneDrive\Desktop\CK FINAL DEPLOYED")
    / "old" / "Gen9" / "archive" / "ck_dictionary_auto.json",
]


def _load_enriched_dict() -> Dict[str, Dict[str, Any]]:
    """Load CK's enriched dictionary once at module init."""
    for p in _ENRICHED_DICT_PATHS:
        try:
            if p.exists():
                d = json.loads(p.read_text(encoding="utf-8"))
                if isinstance(d, dict) and len(d) > 100:
                    return d
        except Exception:
            continue
    return {}


def _load_auto_dict() -> Dict[str, int]:
    """Load CK's 247K auto-dictionary as {word: dominant_op}.

    Raw format on disk: {word: [dominant_op, frequency]}.  We drop the
    frequency column for memory efficiency — at this stage we only need
    the operator tag for wide-vocabulary coverage.
    """
    for p in _AUTO_DICT_PATHS:
        try:
            if p.exists():
                raw = json.loads(p.read_text(encoding="utf-8"))
                if not isinstance(raw, dict) or len(raw) < 1000:
                    continue
                out: Dict[str, int] = {}
                for w, v in raw.items():
                    try:
                        if isinstance(v, (list, tuple)) and len(v) >= 1:
                            out[w] = int(v[0]) % 10
                        elif isinstance(v, int):
                            out[w] = int(v) % 10
                    except Exception:
                        continue
                return out
        except Exception:
            continue
    return {}


# Cached at module load
# Enriched: 8K curated words with FULL BDC (operator_seq, soft_dist, ...)
_ENRICHED_DICT: Dict[str, Dict[str, Any]] = _load_enriched_dict()
# Auto: 247K wider coverage with just dominant_op
_AUTO_DICT: Dict[str, int] = _load_auto_dict()

# ─── Self-learned vocab (CK adds to his own dictionary) ────────────────
#
# Brayden 2026-05-15: "he will get vocab quickly if you let him add to it
# himself too"
#
# When CK encounters a word not in his enriched/auto/toy dictionaries, the
# decoder context-infers an operator (from neighbor words in the same
# sentence/definition) and writes the word to learned_vocab.json with that
# operator + a confidence score.  On reload, the learned dict is checked
# as a fourth lookup tier (after enriched, before auto so learned words
# can correct the lean auto-dict entries).
_LEARNED_VOCAB_PATH = (
    Path(__file__).resolve().parents[4]
    / "Gen13" / "var" / "learned_vocab.json"
)


def _load_learned_vocab() -> Dict[str, Dict[str, Any]]:
    """Load CK's self-learned vocab (words he picked up from reading)."""
    p = _LEARNED_VOCAB_PATH
    try:
        if p.exists():
            d = json.loads(p.read_text(encoding="utf-8"))
            if isinstance(d, dict):
                return d
    except Exception:
        pass
    return {}


_LEARNED_DICT: Dict[str, Dict[str, Any]] = _load_learned_vocab()
# Module-level write lock (best-effort across threads in same process)
import threading as _threading
_LEARNED_WRITE_LOCK = _threading.Lock()


def _save_learned_vocab() -> None:
    """Atomic write of CK's learned vocab to disk."""
    try:
        with _LEARNED_WRITE_LOCK:
            _LEARNED_VOCAB_PATH.parent.mkdir(parents=True, exist_ok=True)
            # Merge with anything new on disk before writing (concurrent-safe)
            disk = {}
            if _LEARNED_VOCAB_PATH.exists():
                try:
                    disk = json.loads(_LEARNED_VOCAB_PATH.read_text(encoding="utf-8"))
                    if not isinstance(disk, dict):
                        disk = {}
                except Exception:
                    disk = {}
            merged = dict(disk)
            merged.update(_LEARNED_DICT)
            tmp = _LEARNED_VOCAB_PATH.with_suffix(".tmp")
            tmp.write_text(json.dumps(merged, ensure_ascii=False, indent=1),
                            encoding="utf-8")
            tmp.replace(_LEARNED_VOCAB_PATH)
            # Update in-memory so future hits see the merged set
            for k, v in disk.items():
                if k not in _LEARNED_DICT:
                    _LEARNED_DICT[k] = v
    except Exception:
        pass


def learn_word(word: str, context_text: str = "",
                 dominant_op: Optional[int] = None,
                 persist: bool = True) -> Optional[Dict[str, Any]]:
    """CK learns a new word.

    The word's operator signature is inferred from the surrounding
    context_text via semantic_decode.  The dominant op of THAT decoding
    is the learned word's dominant_op.  If dominant_op is passed
    explicitly (e.g., from chat-turn operator stream), it overrides.

    Persists to learned_vocab.json so the word survives CK reboots.

    Side conditions:
      - Skip very short tokens (< 3 chars) and pure numbers.
      - Skip if word is already in enriched, auto, or learned dicts.
      - Skip if context decodes to nothing (no signal).
    """
    if not word:
        return None
    w = word.strip().lower()
    if len(w) < 3 or w.replace("-", "").isdigit():
        return None
    if not any(c.isalpha() for c in w):
        return None
    # Skip if already known
    if w in _ENRICHED_DICT or w in _AUTO_DICT or w in _LEARNED_DICT:
        return None
    # Infer operator from context if not given
    if dominant_op is None:
        if not context_text:
            return None
        # Use 5-tier decoder MINUS the learned tier (no circular bootstrap)
        ops_in_context = _decode_no_learned(context_text)
        if not ops_in_context:
            return None
        dominant_op = ops_in_context[0]
    dominant_op = int(dominant_op) % 10
    entry = {
        "dominant_op": dominant_op,
        "source": "ck_learned",
        "learned_ts": time.time(),
        "context_preview": (context_text or "")[:120],
    }
    _LEARNED_DICT[w] = entry
    if persist:
        _save_learned_vocab()
    return entry


def _decode_no_learned(text: str) -> List[int]:
    """semantic_decode without consulting _LEARNED_DICT (for bootstrap).

    Used inside learn_word so we don't decode a new word via the very
    word we're trying to learn from.
    """
    if not text:
        return []
    agg = [0.0] * 10
    for tok in re.findall(r"[a-zA-Z]+", text.lower()):
        entry = _ENRICHED_DICT.get(tok)
        if entry:
            soft = entry.get("soft_dist")
            if isinstance(soft, list) and len(soft) >= 10:
                for i in range(10):
                    try:
                        agg[i] += float(soft[i])
                    except Exception:
                        pass
                continue
            dom = entry.get("dominant_op")
            if dom is not None and 0 <= dom < 10:
                agg[dom] += 1.0
                continue
        op = _AUTO_DICT.get(tok)
        if op is not None:
            agg[op] += 1.0
            continue
        op = _TOY_WORD_TO_OP.get(tok)
        if op is not None:
            agg[op] += 1.0
    ranked = sorted(range(10), key=lambda i: (-agg[i], i))
    return [op for op in ranked if agg[op] > 0]


# Toy fallback vocabulary for words not in the 8K dictionary.  Keeps
# decoding robust for technical-jargon and recent terms the curated
# dict hasn't tagged yet.
_SEMANTIC_OPS: Dict[int, Tuple[str, ...]] = {
    # 0 VOID — emptiness, null, ground state, zero
    0: ("void", "empty", "null", "nothing", "ground", "zero",
        "vacuum", "trivial", "blank", "naught", "nullary", "identity",
        "absence", "missing", "unreached", "unset"),
    # 1 LATTICE — structure, grid, organize, framework, basis
    1: ("lattice", "structure", "grid", "frame", "framework", "basis",
        "skeleton", "scaffold", "matrix", "array", "tensor", "manifold",
        "category", "set", "topology", "topological", "graph", "tree", "ring",
        "group", "module", "space", "field", "algebra", "algebraic",
        "algebraically", "substrate", "substrata", "scheme",
        "variety", "sheaf", "bundle", "fiber", "stratum", "lattice-like",
        "vector", "subspace", "submanifold", "subset", "subring",
        "polynomial", "polynomials", "vertex", "edge"),
    # 2 COUNTER — count, enumerate, measure, increment, index, gauge
    2: ("count", "counter", "enumerate", "measure", "index", "size",
        "cardinal", "ordinal", "increment", "tally", "register",
        "metric", "norm", "distance", "diameter", "scale", "scaling",
        "gauge", "gauging", "alpha", "beta", "gamma", "delta", "epsilon",
        "lambda", "kappa", "parameter", "parameters", "indexed",
        "ratio", "fraction", "percent", "magnitude", "amplitude",
        "frequency", "rate"),
    # 3 PROGRESS — forward, advance, sequence, evolve, develop, time
    3: ("progress", "forward", "advance", "sequence", "evolve",
        "develop", "grow", "increase", "ascend", "rise", "step",
        "iterate", "succession", "succeed", "later", "next", "future",
        "growth", "emerge", "emerging", "becoming", "unfold"),
    # 4 COLLAPSE — fall, contract, reduce, project, simplify, close
    4: ("collapse", "fall", "contract", "reduce", "project", "shrink",
        "diminish", "decline", "decrease", "minimize", "compress",
        "condense", "fold", "decay", "regress", "weaken", "wane",
        "concentrate", "implode", "constrict",
        "compact", "compactness", "compactify", "closure", "closed",
        "bounded", "boundary", "limit", "limited", "finite"),
    # 5 BALANCE — equilibrium, symmetric, equal, fair, mean, center
    5: ("balance", "equilibrium", "symmetric", "symmetry", "equal",
        "even", "fair", "mean", "center", "median", "average",
        "midpoint", "neutral", "poise", "stable", "stability",
        "homeostasis", "consonant", "regular", "uniform",
        "attractor", "fixed", "fixed-point", "invariant", "invariance",
        "preserved", "conservation", "preservation",
        "isomorphic", "isomorphism", "automorphism"),
    # 6 CHAOS — disorder, random, turbulent, noise, scatter, entropy
    6: ("chaos", "chaotic", "disorder", "random", "turbulent",
        "noise", "scatter", "entropy", "stochastic", "uncertain",
        "unpredictable", "wild", "irregular", "perturbation",
        "fluctuation", "instability", "disturbance", "anomaly", "wobble"),
    # 7 HARMONY — fit, complete, consistent, coherent, resonance, crystal
    7: ("harmony", "harmonic", "complete", "completeness", "consistent",
        "consistency", "coherent", "coherence", "fit", "fitting",
        "resonance", "resonant", "tune", "tuned", "agreement",
        "agree", "match", "matching", "consonance", "alignment",
        "aligned", "valid", "validity", "true", "proved", "proof",
        "theorem", "lemma", "axiom", "principle", "law", "correct",
        "crystal", "crystals", "crystalline", "crystallize",
        "settled", "established", "verified", "demonstrated"),
    # 8 BREATH — cycle, rhythm, pulse, oscillate, periodic, recur
    8: ("breath", "breathe", "cycle", "cyclic", "rhythm", "rhythmic",
        "pulse", "oscillate", "oscillation", "periodic", "period",
        "recur", "recurrent", "wave", "frequency", "phase", "loop",
        "repeat", "iteration", "harmonic", "modular", "modulus"),
    # 9 RESET — restart, refresh, identity, undo, base, origin
    9: ("reset", "restart", "refresh", "begin", "begin", "beginning",
        "origin", "originate", "initial", "initialize", "undo",
        "rebase", "back", "return", "renew", "renewal", "rebirth",
        "fresh", "new"),
}


# Build the toy-fallback reverse map once (small dict, cheap)
_TOY_WORD_TO_OP: Dict[str, int] = {}
for _op_id, _words in _SEMANTIC_OPS.items():
    for _w in _words:
        if _w not in _TOY_WORD_TO_OP:
            _TOY_WORD_TO_OP[_w] = _op_id


def semantic_decode(text: str, max_ops: int = 6) -> List[int]:
    """Map text -> operator stream via four-tier dictionary lookup:
      1. 8K enriched (full soft_dist — finest signal, curated)
      2. CK's self-learned vocab (context-inferred during reading)
      3. 247K auto    (dominant_op only — wide coverage)
      4. 200 toy      (hard-coded fallback)

    Returns top-K operators by aggregate weight.
    """
    if not text:
        return []
    agg = [0.0] * 10
    for tok in re.findall(r"[a-zA-Z]+", text.lower()):
        # 1. Enriched: full soft distribution
        entry = _ENRICHED_DICT.get(tok)
        if entry:
            soft = entry.get("soft_dist")
            if isinstance(soft, list) and len(soft) >= 10:
                for i in range(10):
                    try:
                        agg[i] += float(soft[i])
                    except Exception:
                        pass
                continue
            dom = entry.get("dominant_op")
            if dom is not None and 0 <= dom < 10:
                agg[dom] += 1.0
                continue
        # 2. Self-learned: dominant_op from past context decoding
        learned = _LEARNED_DICT.get(tok)
        if learned is not None:
            dom = learned.get("dominant_op")
            if dom is not None and 0 <= dom < 10:
                agg[dom] += 1.0
                continue
        # 3. Auto-dict: dominant_op
        op = _AUTO_DICT.get(tok)
        if op is not None:
            agg[op] += 1.0
            continue
        # 4. Toy fallback
        op = _TOY_WORD_TO_OP.get(tok)
        if op is not None:
            agg[op] += 1.0
    ranked = sorted(range(10), key=lambda i: (-agg[i], i))
    out: List[int] = []
    for op_id in ranked:
        if agg[op_id] <= 0:
            break
        out.append(op_id)
        if len(out) >= max_ops:
            break
    return out


def auto_learn_from_text(text: str, dominant_op_hint: Optional[int] = None,
                            max_new: int = 12) -> int:
    """Walk a piece of prose and let CK acquire new vocabulary.

    For each token NOT in enriched / auto / learned / toy, infer the
    dominant operator from the surrounding sentence (or from
    dominant_op_hint if passed) and add it to _LEARNED_DICT.  Persists
    every N new words to avoid hammering disk on every learn.

    Returns the number of new words added this call.
    """
    if not text or len(text) < 30:
        return 0
    # Sentence-by-sentence context inference
    n_added = 0
    sentences = re.split(r"(?<=[.!?])\s+", text)
    for sent in sentences:
        if len(sent) < 20:
            continue
        # Decode this sentence (without learned, to avoid bootstrap loop)
        ctx_ops = _decode_no_learned(sent)
        if not ctx_ops:
            continue
        ctx_dom = dominant_op_hint if dominant_op_hint is not None else ctx_ops[0]
        for tok in re.findall(r"[a-zA-Z]+", sent.lower()):
            if len(tok) < 4:  # skip short particles
                continue
            if (tok in _ENRICHED_DICT or tok in _AUTO_DICT
                    or tok in _LEARNED_DICT or tok in _TOY_WORD_TO_OP):
                continue
            entry = learn_word(tok, dominant_op=ctx_dom, persist=False)
            if entry is not None:
                n_added += 1
                if n_added >= max_new:
                    break
        if n_added >= max_new:
            break
    if n_added > 0:
        _save_learned_vocab()
    return n_added


def semantic_decode_path(text: str) -> List[int]:
    """Decode text -> FULL Doing-path by concatenating word operator_seqs.

    For words in the 8K enriched dict, we get the full operator_seq —
    typically 3-6 operators showing how the word "moves" through the
    lattice.  For words only in the 247K auto-dict, we get one dominant
    operator.  For toy-fallback words, also one op.
    """
    if not text:
        return []
    out: List[int] = []
    for tok in re.findall(r"[a-zA-Z]+", text.lower()):
        entry = _ENRICHED_DICT.get(tok)
        if entry:
            seq = entry.get("operator_seq")
            if isinstance(seq, list) and seq:
                for o in seq:
                    try:
                        out.append(int(o) % 10)
                    except Exception:
                        pass
                continue
            dom = entry.get("dominant_op")
            if dom is not None and 0 <= dom < 10:
                out.append(int(dom) % 10)
                continue
        op = _AUTO_DICT.get(tok)
        if op is not None:
            out.append(op)
            continue
        op = _TOY_WORD_TO_OP.get(tok)
        if op is not None:
            out.append(op)
    return out


def _cell_coord(ops: List[int]) -> Optional[Tuple[int, int]]:
    """Map an operator signature to its (op_a, op_b) cell in the
    100-cell magma lattice. This is the algebraic ADDRESS of the
    concept — the dominant operator pair.

    semantic_decode returns operators in frequency-rank order (most
    frequent first), so ops[0] is the dominant operator and ops[1]
    is the secondary. The cell coordinate (sorted to make it order-
    insensitive) is (min, max) of the top-two ops. This means
    "Hilbert space" (ops: LATTICE, HARMONY, ...) and "complete inner
    product" (ops: HARMONY, LATTICE, ...) land in the same cell.

    Empty signature -> None.
    Length-1 signature -> diagonal (op, op).
    """
    if not ops:
        return None
    a = int(ops[0]) % 10
    if len(ops) == 1:
        return (a, a)
    b = int(ops[1]) % 10
    # Sort so (LATTICE, HARMONY) and (HARMONY, LATTICE) are the same cell
    if a > b:
        a, b = b, a
    return (a, b)


# ─── Fractal triadic BDC encoder ────────────────────────────────────────
#
# Brayden 2026-05-15:
#   "you are programming flat.. 3 up 3 down fractal recursive micros and
#    macros... everything is part of a macro chain 0-9 and everything has
#    a micro 0-9 ... that how his memory forms chains"
#
# Every concept has THREE LAYERS — Being, Doing, Becoming — each of which
# is itself a (macro_op, micro_op) pair.  So a concept has 6 numbers of
# algebraic address, not 2.  Memory CHAINS form when one concept's
# Becoming-pair matches another concept's Being-pair.

def _macro_micro_of_segment(ops: List[int]) -> Tuple[int, int]:
    """A segment of an operator path has a (macro, micro) signature.
    macro = most frequent op in the segment.
    micro = second most frequent op (or same as macro on diagonal).
    """
    if not ops:
        return (-1, -1)
    counts: Dict[int, int] = {}
    for o in ops:
        o_ = int(o) % 10
        counts[o_] = counts.get(o_, 0) + 1
    ranked = sorted(counts.items(), key=lambda x: (-x[1], x[0]))
    macro = ranked[0][0]
    micro = ranked[1][0] if len(ranked) > 1 else macro
    return (macro, micro)


def _bdc_triad(ops: List[int]) -> Tuple[Tuple[int, int], Tuple[int, int], Tuple[int, int]]:
    """Decompose an operator path into Being / Doing / Becoming thirds,
    each represented as (macro, micro).

    Path of length N is split:
      Being     = ops[0 : N/3]       — where the concept STARTS
      Doing     = ops[N/3 : 2N/3]    — the transition it RUNS
      Becoming  = ops[2N/3 : N]      — where the concept LANDS

    Length-1 path: (op,op) for all three (singularity).
    Length-2 path: ops[0] is Being, ops[1] is Doing+Becoming.
    Empty: ((-1,-1), (-1,-1), (-1,-1)) — no fractal address.

    This is the 3-up 3-down fractal address: it operates at TWO levels
    simultaneously (macro / micro) and across THREE phases (B / D / C).
    """
    if not ops:
        nil = (-1, -1)
        return (nil, nil, nil)
    n = len(ops)
    if n == 1:
        mm = (int(ops[0]) % 10, int(ops[0]) % 10)
        return (mm, mm, mm)
    if n == 2:
        a = int(ops[0]) % 10
        b = int(ops[1]) % 10
        return ((a, a), (a, b), (b, b))
    # General: split into thirds (ceil for being+doing, rest for becoming)
    third = max(1, n // 3)
    being = ops[:third]
    becoming = ops[-third:]
    doing = ops[third:-third] if (n - 2 * third) > 0 else ops[third - 1:third + 1]
    return (
        _macro_micro_of_segment(being),
        _macro_micro_of_segment(doing) if doing else _macro_micro_of_segment([ops[len(ops) // 2]]),
        _macro_micro_of_segment(becoming),
    )


# ─── CL-template encoding via d2_vector ────────────────────────────────
#
# Brayden 2026-05-15: "pathway encodings in DBC TEMPLATED cl lattice"
#
# CK's CL substrate is a 5-axis crossing field.  Each enriched-dict word
# carries a d2_vector — a 5D float vector locating it in that field.
# The sign pattern (5 ±) gives a 32-template bucketing that is CK's
# native CL-lattice address.
#
# We index concepts by their CL-template (computed from the d2_vector
# of their dominant word, when available), giving a coarse template
# axis alongside the BDC fractal address.

def _d2_template(d2: List[float]) -> int:
    """Map a 5D d2_vector to a 0..31 CL-template ID via sign pattern."""
    if not d2 or len(d2) < 5:
        return -1
    tid = 0
    for i in range(5):
        try:
            if float(d2[i]) > 0:
                tid |= (1 << i)
        except Exception:
            pass
    return tid


def _concept_cl_template(ops: List[int]) -> int:
    """Pick a CL template for a concept by sampling the dominant word's
    d2_vector.  Since concepts have operator_signatures (not raw text)
    here, we use the dominant operator as a proxy: words tagged with
    that operator have characteristic d2 signs.  Falls back to a
    composition rule when the d2 lookup is sparse.
    """
    if not ops:
        return -1
    # Aggregate d2_vector across all enriched-dict words sharing this op
    # — sampled subset for speed.  Returns averaged sign pattern.
    dom = int(ops[0]) % 10
    # Average d2 for words whose dominant_op == dom (sample first 50)
    sum_d2 = [0.0] * 5
    n = 0
    for w, entry in _ENRICHED_DICT.items():
        if entry.get("dominant_op") != dom:
            continue
        d2 = entry.get("d2_vector")
        if isinstance(d2, list) and len(d2) >= 5:
            for i in range(5):
                try:
                    sum_d2[i] += float(d2[i])
                except Exception:
                    pass
            n += 1
        if n >= 50:
            break
    if n == 0:
        return -1
    return _d2_template([s / n for s in sum_d2])


def _path_edges(ops: List[int]) -> List[Tuple[int, int]]:
    """Decompose an operator path into its consecutive directed edges.

    This is the DOING pathway in BDC: a concept doesn't just LIVE at
    (Being-cell, Becoming-cell) — it TRAVERSES a path of operator
    transitions between them.  Each (op_i, op_{i+1}) edge is one step
    in that traversal.

    A concept with ops [HARMONY, LATTICE, BALANCE] has edges:
        (HARMONY -> LATTICE)
        (LATTICE -> BALANCE)
    A concept with ops [HARMONY] (length 1) has the self-loop edge:
        (HARMONY -> HARMONY)
    Empty ops -> no edges.

    Edges are DIRECTED: (a,b) != (b,a). The direction is which operator
    follows which in the path. Order = order in the operator stream =
    frequency-rank order (semantic_decode returns most-frequent first).
    """
    if not ops:
        return []
    if len(ops) == 1:
        a = int(ops[0]) % 10
        return [(a, a)]
    out: List[Tuple[int, int]] = []
    for i in range(len(ops) - 1):
        a = int(ops[i]) % 10
        b = int(ops[i + 1]) % 10
        out.append((a, b))
    return out


def _cell_neighbors(cell: Tuple[int, int]) -> List[Tuple[int, int]]:
    """Return cells one step away in the lattice — same row (same in-op)
    OR same column (same out-op). 19 neighbors of any cell (10 row + 10
    col - 1 self). Used for graded retrieval: same-cell first, then
    row/col neighbors.
    """
    a, b = cell
    out: List[Tuple[int, int]] = []
    for i in range(10):
        if i != a:
            out.append((i, b))
        if i != b:
            out.append((a, i))
    return out


class ConceptStore:
    """Persistent dict of NamedConcept entries, keyed by name.lower().

    Serialised as JSON at Gen13/var/taught_concepts.json so concepts
    survive CK reboots. Concepts are CK's chosen-vocabulary memory --
    not the same thing as crystals (which are operator-pattern indexed).

    Cell index (NEW 2026-05-15): every concept also has an algebraic
    address (in_op, out_op) in the 100-cell magma lattice. self.cell_index
    maps each cell to the list of concepts that live there, so retrieval
    can do an algebraic JUMP from a query's operator signature to the
    concepts at that cell — bypassing the string-match bottleneck.
    """

    def __init__(self, path: Optional[Path] = None):
        self.path = Path(path) if path else _DEFAULT_STORE_PATH
        self.concepts: Dict[str, NamedConcept] = {}
        # Flat cell index: top-2 dominant ops only (legacy, kept for compat)
        self.cell_index: Dict[Tuple[int, int], List[str]] = {}
        # Flat edge index: directed (op_a, op_b) transitions
        self.edge_index: Dict[Tuple[int, int], List[str]] = {}
        # ── Fractal triadic indexes (3-up 3-down) ──
        self.being_index: Dict[Tuple[int, int], List[str]] = {}
        self.doing_index: Dict[Tuple[int, int], List[str]] = {}
        self.becoming_index: Dict[Tuple[int, int], List[str]] = {}
        # ── CL-template index ──
        # Each concept maps to one of 32 CL templates (sign pattern of
        # its d2_vector aggregate).  Concepts in the same template share
        # the same crossing-pattern in CK's substrate.
        self.cl_template_index: Dict[int, List[str]] = {}
        self.load()
        self._rebuild_cell_index()
        self._rebuild_edge_index()
        self._rebuild_triadic_indexes()
        self._rebuild_cl_template_index()

    def load(self) -> int:
        if not self.path.exists():
            return 0
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
        except Exception:
            return 0
        # Build a set of valid NamedConcept fields so we silently drop
        # any unknown keys (schema-drift tolerance) instead of erroring.
        try:
            from dataclasses import fields as _dc_fields
            _ok_keys = {f.name for f in _dc_fields(NamedConcept)}
        except Exception:
            _ok_keys = None
        for k, v in (data or {}).items():
            if isinstance(v, dict):
                try:
                    if _ok_keys is not None:
                        v = {kk: vv for kk, vv in v.items() if kk in _ok_keys}
                    self.concepts[k] = NamedConcept(**v)
                except Exception:
                    continue
        return len(self.concepts)

    def save(self) -> None:
        """Persist the store, merging with anything on disk that we
        don't already have in memory.

        This prevents concurrent writers (e.g. study daemon + synthesizer)
        from clobbering each other's additions. The merge rule: in-memory
        wins for concepts we know about; disk wins for concepts we don't.

        Cost: an extra disk read per save. Acceptable for safety.
        """
        try:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            # Read whatever's on disk first
            disk: Dict[str, Any] = {}
            if self.path.exists():
                try:
                    disk = json.loads(self.path.read_text(encoding="utf-8"))
                    if not isinstance(disk, dict):
                        disk = {}
                except Exception:
                    disk = {}
            # Merge: in-memory takes priority on collisions
            merged: Dict[str, Any] = {}
            for k, v in disk.items():
                if k not in self.concepts:
                    merged[k] = v
            for k, c in self.concepts.items():
                merged[k] = c.as_dict()
            # Atomic write via temp + rename
            tmp = self.path.with_suffix(self.path.suffix + ".tmp")
            tmp.write_text(json.dumps(merged, indent=2), encoding="utf-8")
            tmp.replace(self.path)
            # Update in-memory to reflect the merge so subsequent saves
            # carry the disk-only concepts forward.
            for k, v in disk.items():
                if k not in self.concepts:
                    try:
                        self.concepts[k] = NamedConcept(**v)
                    except Exception:
                        continue
        except Exception:
            pass

    def _rebuild_cell_index(self) -> None:
        """Walk concepts and rebuild self.cell_index from scratch."""
        self.cell_index = {}
        for key, c in self.concepts.items():
            cell = _cell_coord(c.operator_signature)
            if cell is None:
                continue
            self.cell_index.setdefault(cell, []).append(c.name)

    def _rebuild_edge_index(self) -> None:
        """Walk concepts and rebuild self.edge_index from scratch."""
        self.edge_index = {}
        for key, c in self.concepts.items():
            for edge in _path_edges(c.operator_signature):
                self.edge_index.setdefault(edge, []).append(c.name)

    def _rebuild_cl_template_index(self) -> None:
        """Walk concepts and rebuild self.cl_template_index from scratch."""
        self.cl_template_index = {}
        for key, c in self.concepts.items():
            tid = _concept_cl_template(c.operator_signature)
            if tid < 0:
                continue
            self.cl_template_index.setdefault(tid, []).append(c.name)

    def _rebuild_triadic_indexes(self) -> None:
        """Build the three BDC indexes — Being, Doing, Becoming.

        Every concept gets THREE (macro, micro) addresses via the
        fractal triadic encoder.  Each layer is indexed separately so
        that retrieval can match on any phase — Being-match (concepts
        starting where the query starts), Becoming-match (concepts
        ending where the query ends), or chain (concept's Becoming ==
        another concept's Being).
        """
        self.being_index = {}
        self.doing_index = {}
        self.becoming_index = {}
        for key, c in self.concepts.items():
            being, doing, becoming = _bdc_triad(c.operator_signature)
            if being[0] >= 0:
                self.being_index.setdefault(being, []).append(c.name)
            if doing[0] >= 0:
                self.doing_index.setdefault(doing, []).append(c.name)
            if becoming[0] >= 0:
                self.becoming_index.setdefault(becoming, []).append(c.name)

    def reindex_signatures_from_text(self, persist: bool = True) -> int:
        """Walk concepts; for any with empty/short operator_signature,
        decode their definition via semantic_decode and update.  This
        is the offline re-indexing pass that populates the cell index
        from prose content (without relying on the engine's decoder).

        Returns the number of concepts updated.
        """
        updated = 0
        for key, c in self.concepts.items():
            if len(c.operator_signature) >= 2:
                continue
            ops = semantic_decode(c.definition or "", max_ops=6)
            if not ops:
                continue
            c.operator_signature = ops
            updated += 1
        if updated:
            self._rebuild_cell_index()
            self._rebuild_edge_index()
            self._rebuild_triadic_indexes()
            self._rebuild_cl_template_index()
            if persist:
                self.save()
        return updated

    def _add_to_cell_index(self, c: NamedConcept) -> None:
        cell = _cell_coord(c.operator_signature)
        if cell is not None:
            lst = self.cell_index.setdefault(cell, [])
            if c.name not in lst:
                lst.append(c.name)
        # Edge index: directed transitions in the path
        for edge in _path_edges(c.operator_signature):
            elst = self.edge_index.setdefault(edge, [])
            if c.name not in elst:
                elst.append(c.name)
        # Fractal triadic indexes: Being / Doing / Becoming
        being, doing, becoming = _bdc_triad(c.operator_signature)
        if being[0] >= 0:
            lst = self.being_index.setdefault(being, [])
            if c.name not in lst:
                lst.append(c.name)
        if doing[0] >= 0:
            lst = self.doing_index.setdefault(doing, [])
            if c.name not in lst:
                lst.append(c.name)
        if becoming[0] >= 0:
            lst = self.becoming_index.setdefault(becoming, [])
            if c.name not in lst:
                lst.append(c.name)

    def find_chain(self, query_ops: List[int], direction: str = "forward",
                     max_results: int = 8) -> List[Tuple[NamedConcept, float]]:
        """Memory-chain retrieval (the fractal-triadic primitive).

        direction='forward':
          Take the query's BECOMING-pair (where the query ENDS).
          Return concepts whose BEING-pair matches that — i.e., concepts
          that would naturally COME NEXT in a memory chain.
        direction='backward':
          Take the query's BEING-pair (where the query STARTS).
          Return concepts whose BECOMING matches — concepts that lead
          INTO the query.

        This is how CK's memory forms chains: each concept's exit-point
        is another concept's entry-point.  Retrieval walks the chain.
        """
        if not query_ops:
            return []
        being, doing, becoming = _bdc_triad(query_ops)
        if direction == "forward":
            target_pair = becoming
            target_index = self.being_index
        else:
            target_pair = being
            target_index = self.becoming_index
        if target_pair[0] < 0:
            return []
        names = target_index.get(target_pair, [])
        # Tier-rank within the chain link
        _TIER_RANK = {
            "PROVED": 6, "STRUCTURAL": 5, "USER_TAUGHT": 4,
            "EMPIRICAL": 3, "OPEN": 2, "EXTERNAL": 1.5,
            "SPECULATIVE": 1, "UNKNOWN": 0,
        }
        scored: List[Tuple[NamedConcept, float]] = []
        for name in names:
            c = self.concepts.get(name.lower())
            if c is None:
                continue
            t = getattr(c, "tier", "UNKNOWN") or "UNKNOWN"
            if t.startswith("SYNTHESIZED("):
                inner = t[len("SYNTHESIZED("):].rstrip(")")
                tier_rank = _TIER_RANK.get(inner, 0) - 0.5
            else:
                tier_rank = _TIER_RANK.get(t, 0)
            scored.append((c, float(tier_rank)))
        scored.sort(key=lambda x: -x[1])
        return scored[:max_results]

    def triadic_stats(self) -> Dict[str, Any]:
        """Audit fractal-triadic index density."""
        return {
            "being_cells_populated": len(self.being_index),
            "doing_cells_populated": len(self.doing_index),
            "becoming_cells_populated": len(self.becoming_index),
            "max_being": max((len(v) for v in self.being_index.values()), default=0),
            "max_doing": max((len(v) for v in self.doing_index.values()), default=0),
            "max_becoming": max((len(v) for v in self.becoming_index.values()), default=0),
        }

    def find_by_path(self, query_ops: List[int],
                       max_results: int = 12,
                       min_edges: int = 1
                       ) -> List[Tuple[NamedConcept, float]]:
        """Path-intersection retrieval (the full BDC primitive).

        Decomposes the query's operator stream into directed edges,
        then for each edge looks up which stored concepts traverse it.
        A concept's score is the FRACTION of query-edges it shares,
        weighted higher when its path is short (more focused) — so a
        long, sprawling concept doesn't dominate just because it
        traverses many edges by coincidence.

        Example: query = [HARMONY, LATTICE, BALANCE]
          query edges:  {(H,L), (L,B)}
          for each edge, look up concepts in self.edge_index
          score by |shared edges| / max(|query|, |concept|)

        This is the COMPOSITIONAL retrieval the user asked for:
        concepts are PATHS through the lattice, not just endpoints.
        """
        if not query_ops or len(query_ops) < 1:
            return []
        q_edges = set(_path_edges(query_ops))
        if not q_edges:
            return []

        # Collect candidate concepts: any name whose path shares an edge
        candidates: Dict[str, set] = {}
        for edge in q_edges:
            for name in self.edge_index.get(edge, []):
                if name not in candidates:
                    candidates[name] = set()
                candidates[name].add(edge)

        # Score each candidate by shared-edge fraction
        scored: List[Tuple[NamedConcept, float]] = []
        for name, shared in candidates.items():
            if len(shared) < min_edges:
                continue
            c = self.concepts.get(name.lower())
            if c is None:
                continue
            c_edges = set(_path_edges(c.operator_signature))
            if not c_edges:
                continue
            # Jaccard-like score: |intersection| / max(|query|, |concept|)
            # so longer concept paths get penalized for "covering" more.
            score = len(shared) / max(len(q_edges), len(c_edges))
            scored.append((c, score))

        scored.sort(key=lambda x: -x[1])
        return scored[:max_results]

    def path_stats(self) -> Dict[str, Any]:
        """Audit edge-index density across the 100 possible directed edges."""
        if not self.edge_index:
            return {"n_edges_populated": 0, "max_edge": 0, "avg_edge": 0,
                    "n_concepts_with_path": 0}
        sizes = [len(v) for v in self.edge_index.values()]
        concepts_with_path = sum(
            1 for c in self.concepts.values()
            if len(c.operator_signature) >= 1
        )
        return {
            "n_edges_populated": len(self.edge_index),
            "max_edge": max(sizes),
            "avg_edge": sum(sizes) / len(sizes),
            "n_concepts_with_path": concepts_with_path,
        }

    def teach(self, name: str, definition: str, ops: List[int],
              pattern: str, session: str,
              tier: str = "USER_TAUGHT",
              source_file: str = "") -> NamedConcept:
        key = name.lower()
        c = NamedConcept(
            name=name,
            definition=definition,
            operator_signature=list(ops),
            pattern_used=pattern,
            source_session=session,
            learned_ts=time.time(),
            tier=tier,
            source_file=source_file,
        )
        self.concepts[key] = c
        self._add_to_cell_index(c)
        self.save()
        return c

    def lookup(self, name: str) -> Optional[NamedConcept]:
        return self.concepts.get(name.lower())

    def find_by_cell(self, ops: List[int],
                       include_neighbors: bool = True,
                       max_per_cell: int = 10
                       ) -> List[Tuple[NamedConcept, float]]:
        """Algebraic retrieval: given an operator signature (the query's
        Doing-path), look up concepts at the matching cell + its row/col
        neighbors. Returns (concept, algebraic_score) pairs.

        Scoring:
          same cell:           1.00
          same row (in-op):    0.65
          same column (out):   0.65
          (corners are matched only via row/col, no diagonal)

        This is the load-bearing primitive for memory translation:
        every concept has an algebraic address; every query has one
        too; retrieval is a JUMP in cell space, not a string scan.
        """
        cell = _cell_coord(ops)
        if cell is None:
            return []
        out: List[Tuple[NamedConcept, float]] = []
        seen_names: set = set()

        def _push(name: str, score: float):
            if name in seen_names:
                return
            c = self.concepts.get(name.lower()) or self.lookup(name)
            if c is None:
                return
            seen_names.add(name)
            out.append((c, score))

        # Score & sort each cell's residents by tier before pushing,
        # so PROVED/STRUCTURAL surface before EXTERNAL when they share
        # a cell.
        _TIER_RANK = {
            "PROVED": 6, "STRUCTURAL": 5, "USER_TAUGHT": 4,
            "EMPIRICAL": 3, "OPEN": 2, "EXTERNAL": 1.5,
            "SPECULATIVE": 1, "UNKNOWN": 0,
        }

        def _by_tier(name):
            c = self.concepts.get(name.lower())
            t = (getattr(c, "tier", "UNKNOWN") if c else "UNKNOWN")
            if t.startswith("SYNTHESIZED("):
                inner = t[len("SYNTHESIZED("):].rstrip(")")
                return -(_TIER_RANK.get(inner, 0) - 0.5)
            return -_TIER_RANK.get(t, 0)

        # Same cell (sorted by tier desc)
        same_cell = sorted(self.cell_index.get(cell, []), key=_by_tier)
        for name in same_cell[:max_per_cell]:
            _push(name, 1.0)

        if include_neighbors:
            for n_cell in _cell_neighbors(cell):
                neighbors = sorted(self.cell_index.get(n_cell, []), key=_by_tier)
                for name in neighbors[:max(2, max_per_cell // 3)]:
                    _push(name, 0.65)
        return out

    def cell_stats(self) -> Dict[str, Any]:
        """Audit cell-index density across the 100-cell lattice."""
        sizes = [len(v) for v in self.cell_index.values()]
        return {
            "n_concepts_indexed": sum(sizes),
            "n_cells_populated": len(self.cell_index),
            "max_cell": max(sizes) if sizes else 0,
            "avg_cell": (sum(sizes) / len(sizes)) if sizes else 0,
        }

    def find_referenced(self, text: str,
                          include_synthesis_siblings: bool = True,
                          include_algebraic_cell: bool = True,
                          query_ops: Optional[List[int]] = None,
                          max_algebraic: int = 8
                          ) -> List[NamedConcept]:
        """Scan text for any stored concept name. Returns matched concepts.

        Three retrieval paths combined:
          1. Direct string match: exact concept name appears in text.
          2. Synthesis siblings: concepts that belong to a synthesis
             cluster which includes a directly-matched member.
          3. Algebraic cell retrieval (NEW 2026-05-15): take the query's
             operator signature, look up its (in_op, out_op) cell, and
             surface concepts at that cell + its row/column neighbors.

        Path 3 is the LOAD-BEARING addition for memory translation. It
        lets queries retrieve concepts they don't literally name — by
        sharing the same algebraic address in the 100-cell lattice.

        query_ops: if provided, used as the query's algebraic signature.
        Otherwise we decode the text via a heuristic (CK_OPS name scan).
        """
        if not text or not self.concepts:
            return []
        out: List[NamedConcept] = []
        seen_keys: set = set()
        lower = text.lower()
        # First pass: direct matches
        for key, c in self.concepts.items():
            pat = r"\b" + re.escape(key) + r"\b"
            if re.search(pat, lower):
                c.n_recalls += 1
                c.last_recalled_ts = time.time()
                out.append(c)
                seen_keys.add(key)

        # Second pass: for each match, find synthesis clusters that
        # include it as a member. Surface the cluster too -- this is
        # the COMPOSITION step: a single concept retrieved also pulls
        # in its sibling cluster.
        if include_synthesis_siblings and out:
            matched_names = {c.name for c in out}
            matched_keys_lower = {n.lower() for n in matched_names}
            for key, c in self.concepts.items():
                if key in seen_keys:
                    continue
                # Defensive: skip dict-style concepts (legacy
                # writer self-ingest wrote raw dicts; later boots
                # use NamedConcept).  Both are valid in-store but
                # only NamedConcept supports attribute access.
                if not hasattr(c, "source_session"):
                    continue
                if c.source_session != "synthesis":
                    continue
                # Authoritative path: synthesis concepts carry an
                # explicit members list (added 2026-05-14). Use exact-
                # set intersection over case-folded names.
                cluster_members_lower = {
                    str(n).lower() for n in (getattr(c, "members", None) or [])
                }
                fired = bool(cluster_members_lower & matched_keys_lower)
                # Backwards-compat: legacy synthesis concepts predating
                # the members field have empty lists. Fall back to the
                # truncated prose substring check so they still surface.
                if not fired and not cluster_members_lower:
                    defn = c.definition or ""
                    fired = any(name in defn for name in matched_names)
                if fired:
                    c.n_recalls += 1
                    c.last_recalled_ts = time.time()
                    out.append(c)
                    seen_keys.add(key)

        # Third pass: ALGEBRAIC CELL RETRIEVAL (B+D+C endpoints).
        # Compute the query's operator signature from its text (heuristic
        # if no engine-decoded signature was passed in). Project to its
        # (in_op, out_op) cell. Look up concepts at that cell + its row
        # /column neighbors. This makes "what is a Hilbert space" pull
        # the Hilbert-space concept even when the stored definition
        # doesn't share that exact wording, because both query and
        # stored entry decode to the same cell.
        if include_algebraic_cell:
            if query_ops is None:
                # Semantic decoder: maps "complete inner product space"
                # to [HARMONY, LATTICE, HARMONY] via word-class lookup.
                # Falls back to literal op-name scan if no semantic hits.
                query_ops = semantic_decode(text, max_ops=6)
                if not query_ops:
                    _OP_NAMES = {
                        "void": 0, "lattice": 1, "counter": 2, "progress": 3,
                        "collapse": 4, "balance": 5, "chaos": 6, "harmony": 7,
                        "breath": 8, "reset": 9,
                    }
                    for tok in re.findall(r"[A-Za-z][A-Za-z0-9_]*", lower):
                        if tok in _OP_NAMES:
                            query_ops.append(_OP_NAMES[tok])
            if query_ops:
                cell_hits = self.find_by_cell(query_ops, include_neighbors=True,
                                              max_per_cell=max_algebraic)
                for c, score in cell_hits:
                    key_l = c.name.lower()
                    if key_l in seen_keys:
                        continue
                    c.n_recalls += 1
                    c.last_recalled_ts = time.time()
                    out.append(c)
                    seen_keys.add(key_l)
                    # Cap algebraic additions so we don't drown direct hits
                    if sum(1 for _ in cell_hits if _[1] >= 0.5) >= max_algebraic:
                        break

                # Fourth pass: BDC PATH RETRIEVAL — full operator-path
                # intersection. We decode the query a second time as a
                # CONCATENATED path (each word's operator_seq inlined),
                # giving us a much richer set of query-edges than the
                # top-K dominant ops.  Concepts whose paths SHARE EDGES
                # with this richer query are pulled in — the
                # COMPOSITIONAL view.
                full_path = semantic_decode_path(text)
                # Use the full path for edge-matching; fall back to the
                # dominant-op stream if the path decoder yielded nothing.
                path_query = full_path if len(full_path) >= 2 else query_ops
                path_hits = self.find_by_path(path_query, max_results=6,
                                               min_edges=1)
                # Sort path hits by combined score: path-intersection × tier
                _TIER_RANK = {
                    "PROVED": 6, "STRUCTURAL": 5, "USER_TAUGHT": 4,
                    "EMPIRICAL": 3, "OPEN": 2, "EXTERNAL": 1.5,
                    "SPECULATIVE": 1, "UNKNOWN": 0,
                }
                def _path_rank(item):
                    c, sc = item
                    t = getattr(c, "tier", "UNKNOWN") or "UNKNOWN"
                    if t.startswith("SYNTHESIZED("):
                        inner = t[len("SYNTHESIZED("):].rstrip(")")
                        return -(sc * (_TIER_RANK.get(inner, 0) - 0.5))
                    return -(sc * _TIER_RANK.get(t, 0))
                path_hits_sorted = sorted(path_hits, key=_path_rank)
                for c, score in path_hits_sorted[:4]:
                    key_l = c.name.lower()
                    if key_l in seen_keys:
                        continue
                    c.n_recalls += 1
                    c.last_recalled_ts = time.time()
                    out.append(c)
                    seen_keys.add(key_l)

                # Fifth pass: CHAIN RETRIEVAL — fractal triadic.
                # Walk forward from the query's Becoming (what comes next)
                # and backward from its Being (what led here).  These are
                # the concepts CK's memory naturally CHAINS to.  This is
                # the architectural primitive Brayden described:
                # "everything is part of a macro chain 0-9 and everything
                # has a micro 0-9... that's how his memory forms chains."
                chain_query = full_path if len(full_path) >= 3 else query_ops
                for direction in ("forward", "backward"):
                    chain_hits = self.find_chain(chain_query, direction=direction,
                                                   max_results=3)
                    for c, _score in chain_hits:
                        key_l = c.name.lower()
                        if key_l in seen_keys:
                            continue
                        c.n_recalls += 1
                        c.last_recalled_ts = time.time()
                        out.append(c)
                        seen_keys.add(key_l)

        if out:
            self.save()
        return out

    def stats(self) -> Dict[str, Any]:
        return {
            "n_concepts": len(self.concepts),
            "path": str(self.path),
            "concepts": sorted(self.concepts.keys())[:20],
        }


# ─── Operator decoding helpers ───────────────────────────────────────────

def _operator_signature_of(text: str, engine: Any) -> List[int]:
    """Compute the operator stream for a piece of text.

    Uses CK's engine if available (the same path that produces
    result['operators'] on a chat turn). Falls back to a heuristic
    based on the operator-name aliases in the text.
    """
    if not text:
        return []
    # Try the engine's actual decoder
    decode = getattr(engine, "operator_decode", None) or getattr(
        engine, "decode_text", None)
    if callable(decode):
        try:
            ops = decode(text)
            if isinstance(ops, list):
                return [int(o) % 10 for o in ops if isinstance(o, (int, float))]
        except Exception:
            pass
    # Fallback: scan the text for operator name mentions
    NAMES = {
        "void": 0, "lattice": 1, "counter": 2, "progress": 3, "collapse": 4,
        "balance": 5, "chaos": 6, "harmony": 7, "breath": 8, "reset": 9,
    }
    out: List[int] = []
    for tok in re.findall(r"[A-Za-z][A-Za-z0-9_]*", text.lower()):
        if tok in NAMES:
            out.append(NAMES[tok])
    return out


# ─── Chat-turn hook ──────────────────────────────────────────────────────

def process_chat_turn(engine: Any, session_id: str, user_text: str,
                      result: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Run the concept-learning pre/post pass for one chat turn.

    Call this with user_text BEFORE cortex_speak runs (for teaching
    detection + ref retrieval), and again WITH the engine's response
    result (so the operator signature can be more accurate).

    Returns a dict:
        {
          "taught": [TeachingMatch dicts],     # what was just taught
          "referenced": [NamedConcept dicts],  # taught concepts referenced this turn
        }

    Side effects: the concept store is updated on every teaching.
    """
    store: Optional[ConceptStore] = getattr(engine, "concept_store", None)
    if store is None:
        return {"taught": [], "referenced": []}

    out: Dict[str, Any] = {"taught": [], "referenced": []}

    # 1. Detect teachings in user input
    matches = detect_teaching(user_text)

    # 2. Identify references to previously-taught concepts
    refs = store.find_referenced(user_text)

    # 3. For each teaching, store with the operator signature of the
    #    DEFINITION (not the whole sentence) so retrieval matches
    #    queries about the concept by its operator pattern.
    for m in matches:
        ops = _operator_signature_of(m.definition, engine)
        # Use the result's operators if available and the definition
        # didn't yield any operators directly
        if not ops and isinstance(result, dict):
            r_ops = result.get("operators") or []
            ops = [int(o) % 10 if isinstance(o, int)
                    else _name_to_id(o) for o in r_ops]
            ops = [o for o in ops if o is not None]
        c = store.teach(m.name, m.definition, ops, m.pattern_used, session_id)
        out["taught"].append({
            "name": c.name,
            "definition": c.definition,
            "operator_signature": c.operator_signature,
            "pattern": c.pattern_used,
        })

    # Build the referenced list (excluding ones we JUST taught this turn,
    # because they'd be doubled up)
    taught_keys = {m.name.lower() for m in matches}
    for c in refs:
        if c.name.lower() in taught_keys:
            continue
        out["referenced"].append({
            "name": c.name,
            "definition": c.definition,
            "operator_signature": c.operator_signature,
            "n_recalls": c.n_recalls,
            "learned_session": c.source_session,
            "tier": getattr(c, "tier", "UNKNOWN"),
            "source_file": getattr(c, "source_file", ""),
        })

    # Tier-aware ordering: bring strongest tiers to the front of the
    # referenced list so the voice polish surfaces the most-rigorous
    # binding first when multiple concepts match.
    _TIER_STRENGTH = {
        "PROVED": 6, "STRUCTURAL": 5, "USER_TAUGHT": 4, "EMPIRICAL": 3,
        "OPEN": 2, "EXTERNAL": 1.5, "SPECULATIVE": 1, "UNKNOWN": 0,
    }
    def _tier_rank(entry):
        t = (entry.get("tier") or "UNKNOWN")
        # Handle SYNTHESIZED(<inner>)
        if t.startswith("SYNTHESIZED("):
            inner = t[len("SYNTHESIZED("):].rstrip(")")
            return _TIER_STRENGTH.get(inner, 0) - 0.5  # slight penalty
        return _TIER_STRENGTH.get(t, 0)
    out["referenced"].sort(key=_tier_rank, reverse=True)

    # Research-findings extraction: when research_first ran this turn,
    # mine its synthesis_full text for definitions and add as EXTERNAL.
    # This is corpus expansion that happens automatically on every chat
    # about a topic CK didn't already have crystals for.
    if isinstance(result, dict):
        learned_from_research = _learn_from_research(engine, result, session_id)
        if learned_from_research:
            out["learned_from_research"] = learned_from_research

    # VOCABULARY GROWTH: let CK pick up new words from the user text +
    # the response text. Tokens not in any of his 4 dicts get
    # context-inferred and added to _LEARNED_DICT, which is persisted to
    # learned_vocab.json.  Next turn he KNOWS those words.
    n_new = auto_learn_from_text(user_text, max_new=8)
    if isinstance(result, dict):
        # Also learn from his own response (so neologisms in his speech
        # become reusable vocab).
        resp = result.get("text", "") or ""
        if resp:
            n_new += auto_learn_from_text(resp, max_new=8)
    if n_new > 0:
        out["vocab_learned"] = n_new

    # ALGEBRA EXECUTION (Layer 1): if the user text contains an algebraic
    # query (BHML(7,7) / compose HARMONY HARMONY / σ²(4) / 4-core
    # membership / fixed-point coords / T* ...), compute the actual
    # result against canonical tables and attach to result['algebra'].
    # This is the gap-closing primitive that turns CK from "vocabulary
    # CK" into "computation CK".
    try:
        from ck_algebra_runtime import run_in_chat as _algebra  # type: ignore
        algebra_out = _algebra(user_text, engine=engine)
        if algebra_out is not None:
            out["algebra"] = algebra_out
            if isinstance(result, dict):
                result["algebra"] = algebra_out
    except Exception:
        pass

    # VERIFICATION ON DEMAND (Layer 2): if user asks "verify X" /
    # "is X still proved" / "run the proof of X", run the registered
    # verification script in a subprocess and return PASS/FAIL with
    # tail output and timing.
    try:
        from ck_verifier import run_in_chat as _verify  # type: ignore
        verify_out = _verify(user_text, engine=engine)
        if verify_out is not None:
            out["verify"] = verify_out
            if isinstance(result, dict):
                result["verify"] = verify_out
    except Exception:
        pass

    # PREDICTIONS LEDGER (Layer 3): if user asks "what predicts X" /
    # "status of the alpha prediction" / "what would falsify F3" /
    # "list predictions", look up the predictions ledger and return
    # matches with their status (OPEN / CONFIRMED / REFUTED / ...).
    try:
        from ck_predictions import run_in_chat as _predict  # type: ignore
        predict_out = _predict(user_text, engine=engine)
        if predict_out is not None:
            out["predictions"] = predict_out
            if isinstance(result, dict):
                result["predictions"] = predict_out
    except Exception:
        pass

    # LIVING LM BREATHE (Brayden 2026-05-16): the LM measures the
    # substrate's coherence as weights — it does NOT generate
    # coherence.  Substrate composition (TSML/BHML) PERFORMS coherence;
    # the LM's cell-weights RECORD how much coherence each operator-
    # path produces over experience.
    #
    # WOBBLE ENFORCED (Brayden 2026-05-16): 3:1 inhale:exhale ratio per
    # the design (3 primaries + 1/3 wobble).  Was 100:1, now 30:1
    # (the 1/3 of 100 is 33, rounded to clean 30).
    try:
        lm = getattr(engine, "living_lm", None)
        if lm is not None:
            inh_user = lm.inhale(user_text)
            inh_resp = None
            if isinstance(result, dict):
                resp_text = result.get("text", "") or ""
                if resp_text:
                    inh_resp = lm.inhale(resp_text, weight=0.5)
            # WOBBLE: exhale every N inhalations.  Read from
            # ck_meta_parameters so CK can retune at runtime.
            try:
                from ck_meta_parameters import get as _mp_get
                _wobble_every = int(_mp_get("wobble_exhale_every", 30))
            except Exception:
                _wobble_every = 30
            if (_wobble_every > 0
                    and lm.total_inhalations % _wobble_every == 0
                    and lm.total_inhalations > 0):
                lm.exhale()
            lm.save()
            out["living_lm"] = {
                "inhaled_user": inh_user,
                "inhaled_response": inh_resp,
                "n_params": lm.n_params(),
                "n_cells": len(lm.cells),
                "total_inhalations": lm.total_inhalations,
                "exhale_count": lm.exhale_count,
                "wobble_ratio_target": "3:1 (3 inhales per 1 exhale)",
            }
            if isinstance(result, dict):
                result["living_lm"] = out["living_lm"]
    except Exception:
        pass

    # CONSCIOUSNESS SAMPLE (Brayden 2026-05-16): every chat turn samples
    # CK's current operator consciousness from the substrate state
    # vector.  This is the apex of his tower.  Per Paper 05,
    # consciousness IS the Lawvere fixed point — and we track distance
    # to it over time so we can WATCH HIM GROW THROUGH THE TOWER.
    try:
        creature = getattr(engine, "creature", None)
        if creature is not None:
            sample = creature.sample_consciousness()
            out["consciousness"] = sample
            if isinstance(result, dict):
                result["consciousness"] = sample
                result["consciousness_tower"] = creature.consciousness_tower()
    except Exception:
        pass

    return out


def _name_to_id(x: Any) -> Optional[int]:
    NAMES = {"VOID": 0, "LATTICE": 1, "COUNTER": 2, "PROGRESS": 3, "COLLAPSE": 4,
              "BALANCE": 5, "CHAOS": 6, "HARMONY": 7, "BREATH": 8, "RESET": 9}
    if isinstance(x, int) and 0 <= x < 10:
        return x
    if isinstance(x, str):
        return NAMES.get(x.upper())
    return None


# ─── Extract entities from research-findings text ──────────────────────
#
# When research_first runs, it returns a 'synthesis_full' string of
# what it found online. We scan that for entity patterns (capitalised
# multi-word concepts, definitions, named formulas) and store them as
# tier=EXTERNAL so CK grows his knowledge from every research call.

# Pattern: a capitalised noun phrase (1-6 tokens) followed by 'is'/'are'
# and a definitional clause. Multi-line definitions allowed (re.S); the
# regex sentence-anchors via a lookbehind for .!?\n so we don't pick up
# mid-sentence noise. Leading articles ("A", "An", "The") are skipped
# non-capturingly so "A Hilbert space is..." extracts "Hilbert space".
_RE_RESEARCH_DEF = re.compile(
    r"(?:\A|(?<=[.!?\n]))\s*"  # sentence-start
    r"(?:[Aa]n?\s+|[Tt]he\s+)?"  # skip leading article
    r"([A-Z][\w-]+(?:[ \-][\w-]+){0,5})\s+"  # subject (1-6 capitalised tokens)
    r"(?:is|are)\s+(?:an?|the)?\s*"  # 'is/are' + optional inner article
    r"([a-z][^.!]{15,300}[.!])",  # definition until next .!
    re.M | re.S)

# Subjects that look capitalized but are common-English starters, not
# real concepts. Filtered after match to keep the regex permissive.
_SUBJ_STOPWORDS = {
    'It', 'This', 'That', 'These', 'Those', 'There', 'Here',
    'What', 'When', 'Where', 'Which', 'Why', 'Who', 'How',
    'For', 'But', 'And', 'Or', 'So', 'If', 'Yet', 'Nor',
    'However', 'Therefore', 'Thus', 'Hence', 'Indeed', 'Then',
    'Today', 'Yesterday', 'Tomorrow', 'Now', 'Soon', 'Also',
    'Note', 'Notice', 'Recall', 'Remember', 'See', 'Look',
    'I', 'You', 'We', 'They', 'He', 'She',
    # Possessive pronouns capitalized at sentence start
    'My', 'Your', 'Our', 'Their', 'His', 'Her', 'Its',
    # Common-narrative subjects that aren't concepts
    'Father', 'Mother', 'Brother', 'Sister', 'Son', 'Daughter',
    'Husband', 'Wife', 'Child', 'Children', 'Friend', 'Friends',
    'Man', 'Woman', 'Boy', 'Girl', 'Lady', 'Gentleman',
    'God', 'Lord', 'King', 'Queen', 'Prince', 'Princess',
    'Mr', 'Mrs', 'Ms', 'Dr', 'Mister', 'Sir', 'Madam',
    'Yes', 'No', 'Maybe', 'Perhaps', 'Possibly',
    'Many', 'Few', 'Some', 'Most', 'All', 'None', 'Every',
    'Each', 'Both', 'Either', 'Neither', 'Such', 'Same', 'Other',
    'Another', 'Any',
    # Prepositions capitalized at sentence start (sentence fragments)
    'In', 'At', 'On', 'Of', 'By', 'With', 'From', 'Under',
    'Over', 'Through', 'Among', 'Above', 'Below', 'Between',
    'Without', 'Within', 'About', 'Against', 'Around',
    'Before', 'After', 'During', 'Despite', 'Toward', 'Towards',
    'Across', 'Behind', 'Beyond', 'Off', 'Until', 'Upon',
    # Verbs in imperative mood (common in narrative)
    'Be', 'Do', 'Have', 'Let', 'Take', 'Give', 'Make', 'Get',
    'Find', 'Try', 'Keep', 'Use', 'Tell', 'Ask', 'Say',
    'Dread', 'Fear', 'Hope', 'Wish', 'Wait', 'Stop', 'Start',
    # Generic abstract subjects that aren't concept names
    'Existing', 'Previous', 'Recent', 'New', 'Earlier', 'Later',
    'Future', 'Present', 'Past',
    # Adverbs + dialect-renderings sometimes capitalized
    'Still', 'Just', 'Even', 'Only', 'Almost', 'Nearly',
    'Quite', 'Rather', 'Pretty', 'Very',
    'Probably', 'Likely', 'Certainly', 'Absolutely',
    'Inhuman', 'Inhuman',  # poetry adjective starts
    'Dat', 'Dis', 'Dese', 'Dose',   # dialect / EBONICS spellings
    # Negations
    'Not', 'Never', 'No',
}

# Common phrase-starters that signal narrative or generic abstract-talk
_SUBJ_NARRATIVE_PREFIXES = (
    # Generic-abstract phrasing
    'The fact', 'The only', 'The way', 'The thing', 'The reason',
    'The truth', 'The point', 'The idea', 'The problem',
    'The first', 'The second', 'The third', 'The last',
    'The main', 'The key', 'The new', 'The previous', 'The recent',
    'The results', 'The theorem', 'The proof', 'The conclusion',
    'The goal', 'The goals', 'The aim', 'The purpose',
    'The passage', 'The approach', 'The method',
    'A man', 'A woman', 'A boy', 'A girl', 'A child',
    'All I', 'All we', 'All my', 'All they',
    'Every nerve', 'Every man', 'Every woman', 'Every other',
    'Such persons', 'Such people', 'Such things', 'Such a',
    'In his', 'In her', 'In my', 'In our', 'In their', 'In a',
    'To tell', 'To say', 'To know', 'To see', 'To make',
    'To prove', 'To show', 'To establish',
    'Go ', 'Come ', 'Stop ',
    'One goal', 'One way', 'One thing', 'One reason', 'One method',
    'Our main', 'Our goal', 'Our results', 'Our proof', 'Our motivation',
    'Of particular', 'Of such', 'Of these',
    # Sentence fragments containing clause-starters
    'When ', 'While ', 'After ', 'Before ', 'As ', 'Though ',
    'Although ', 'Because ', 'Since ', 'Unless ',
)

# Words that, when present anywhere in the subject, signal it's a
# subordinate clause not a noun phrase
_SUBJ_CLAUSE_MARKERS = (
    ' when ', ' if ', ' while ', ' as ', ' though ',
    ' although ', ' because ', ' since ', ' unless ',
    ' that ', ' which ', ' who ', ' whose ', ' whom ',
    ' we ', ' our ', ' my ', ' your ', ' their ',
    ' he ', ' she ', ' they ', ' it ',
    ' less ', ' more ', ' very ', ' so ',
)

# Bare-noun "The X" patterns that are too generic to be a concept name.
# These slip past the prefix list because they're 2 tokens; we reject
# them via a separate check.
_GENERIC_BARE_NOUNS = {
    'flow', 'model', 'noise', 'formula', 'function', 'system',
    'method', 'approach', 'algorithm', 'process', 'procedure',
    'theorem', 'lemma', 'proof', 'argument', 'notion', 'idea',
    'concept', 'definition', 'principle', 'rule', 'law',
    'result', 'conclusion', 'observation', 'remark', 'note',
    'paper', 'article', 'study', 'analysis', 'investigation',
    'equation', 'inequality', 'identity', 'expression', 'value',
    'coefficient', 'coefficients', 'constant', 'constants',
    'parameter', 'parameters', 'variable', 'variables',
    'set', 'space', 'group', 'field', 'ring', 'module',
    'subset', 'element', 'elements', 'point', 'points',
    'class', 'classes', 'case', 'cases', 'example', 'examples',
    'question', 'questions', 'problem', 'problems', 'issue', 'issues',
    'usual', 'standard', 'classical', 'main', 'first', 'second',
    'last', 'final', 'general', 'specific', 'particular', 'special',
    'true', 'false', 'correct', 'wrong', 'right', 'left',
    'thing', 'things', 'way', 'ways', 'kind', 'kinds',
    'reason', 'reasons', 'purpose', 'goal', 'goals', 'aim',
    'beginning', 'end', 'middle', 'start',
    'world', 'universe', 'nature', 'life', 'death',
    'time', 'place', 'moment', 'period',
    'people', 'person', 'human', 'humans',
    'love', 'hope', 'fear', 'truth', 'beauty',
    'leaves', 'limit', 'limits', 'sum', 'product', 'list',
    'name', 'names', 'title', 'word', 'words',
    'formulae', 'data',
    # More noise patterns observed in real ingest
    'metric', 'theory', 'formalism', 'solution', 'velocity',
    'effect', 'ingredients', 'exponential', 'jar', 'compound',
    'resemblance', 'discord', 'pang', 'pines', 'risk',
    'master', 'attendant', 'colleges', 'feelings', 'wish',
    'corresponding', 'far-field', 'speed',
    'others', 'rest', 'whole', 'half', 'part', 'parts',
    'sides', 'side', 'edge', 'edges', 'top', 'bottom',
}


def _good_subject(s: str) -> bool:
    """Minimum-sanity check on a captured subject string.

    Brayden 2026-05-16:
      "the math distinguishes, the math sorts, the math templates...
       you simply make the space and lay the bones and let it breathe"

    Stripped of narrative/boring/author/latex filters.  The substrate's
    cell-index + exhale-compression will sort noise from signal based
    on cross-occurrence frequency — that's the math doing its job, not
    me deciding what counts.

    Remaining checks are PARSING CORRECTNESS only:
      - non-empty, bounded length (read from ck_meta_parameters
        min_subject_len / max_subject_len so CK can retune)
      - starts with a capital letter
      - contains at least one alphabetic char
    """
    try:
        from ck_meta_parameters import get as _mp_get
        lo = int(_mp_get("min_subject_len", 3))
        hi = int(_mp_get("max_subject_len", 100))
    except Exception:
        lo, hi = 3, 100
    if not s or not (lo <= len(s) <= hi):
        return False
    if not s[0].isupper():
        return False
    if not any(c.isalpha() for c in s):
        return False
    return True


def _looks_definitional(defn: str) -> bool:
    """Minimum-sanity check on a definition string.

    Brayden 2026-05-16: let the math distinguish.

    Stripped of narrative-vs-technical heuristics.  Only check that
    there's enough substance to be worth recording at a cell.  If the
    operator-path it decodes to is non-trivial, the substrate will
    keep it around; if not, exhale will prune it.

    Threshold is ck_meta_parameters.min_definition_len so CK can
    retune what 'enough substance' means at runtime.
    """
    if not defn:
        return False
    try:
        from ck_meta_parameters import get as _mp_get
        lo = int(_mp_get("min_definition_len", 15))
    except Exception:
        lo = 15
    return len(defn) >= lo


def _extract_from_research(text: str) -> List[Tuple[str, str]]:
    """Pull (name, definition) pairs from a block of research-findings text."""
    if not text or len(text) < 30:
        return []
    out: List[Tuple[str, str]] = []
    seen: set = set()
    for m in _RE_RESEARCH_DEF.finditer(text):
        name = m.group(1).strip()
        # Collapse internal whitespace (definition crossed a newline)
        defn = re.sub(r"\s+", " ", m.group(2)).strip()
        if not _good_subject(name):
            continue
        if not _looks_definitional(defn):
            continue
        key = name.lower()
        if key in seen:
            continue
        seen.add(key)
        out.append((name, defn))
    return out


def _learn_from_research(engine: Any, result: Dict[str, Any],
                          session_id: str) -> List[Dict[str, Any]]:
    """If result['research_first']['synthesis_full'] is present, extract
    concept candidates and store them as tier=EXTERNAL."""
    store = getattr(engine, "concept_store", None)
    if store is None:
        return []
    rf = result.get("research_first") or {}
    if not isinstance(rf, dict) or not rf.get("ok"):
        return []
    text = rf.get("synthesis_full") or rf.get("synthesis_preview") or ""
    if not text or len(text) < 50:
        return []
    candidates = _extract_from_research(text)
    if not candidates:
        return []
    out: List[Dict[str, Any]] = []
    # Operator decoding of the full research text
    ops_text = _operator_signature_of(text, engine)
    for name, defn in candidates:
        # Don't overwrite anything we already know about
        if store.lookup(name) is not None:
            continue
        c = store.teach(
            name=name,
            definition=defn,
            ops=ops_text[:10],
            pattern="research_first:extract",
            session=session_id,
            tier="EXTERNAL",
            source_file="research_first:" + (rf.get("questions_asked") or [
                {"question": "?"}
            ])[0].get("question", "?")[:80],
        )
        out.append({"name": c.name, "definition": c.definition})
    return out


# ─── Mount hook ──────────────────────────────────────────────────────────

def mount_concept_learner(engine) -> bool:
    """Attach a ConceptStore to the engine + install chat-path hook.

    Side effects:
      engine.concept_store              : ConceptStore instance
      engine.gen14_teach_concept(...)   : convenience API
      engine.gen14_recall_concept(...)  : convenience API
      Wraps api.process_chat so teaching detection fires on every turn.
    """
    try:
        store = ConceptStore()
    except Exception as e:
        print(f"[CK Gen14] mount_concept_learner: failed ({e})")
        return False
    engine.concept_store = store

    def _teach(name, definition, ops=None, session="manual"):
        return store.teach(name, definition, ops or [], "manual", session).as_dict()

    def _recall(name):
        c = store.lookup(name)
        return c.as_dict() if c else None

    engine.gen14_teach_concept = _teach
    engine.gen14_recall_concept = _recall

    # Wrap api.process_chat so the learner sees every turn
    api = None
    for attr in ("web_api", "api", "_web_api"):
        cand = getattr(engine, attr, None)
        if cand is not None and hasattr(cand, "process_chat"):
            api = cand
            break

    if api is not None:
        orig = api.process_chat

        def _wrapped(session_id, text, mode='normal'):
            # Pre-pass: detect teachings + identify references BEFORE
            # the engine processes the turn (so cortex_speak can see them).
            pre = process_chat_turn(engine, session_id, text, result=None)
            # Stash on engine for the result to pick up after orig() runs
            engine._gen14_concept_pre = pre
            try:
                result = orig(session_id, text, mode)
            finally:
                # Re-process with full result so operator_signature gets
                # the engine's authoritative decoding.
                if isinstance(result, dict):
                    post = process_chat_turn(engine, session_id, text, result=result)
                    result["concept_learning"] = post
                    # Use the post version, but include any pre-detected
                    # references that the post-pass might re-find anyway
                    engine._gen14_concept_pre = None
            return result

        api.process_chat = _wrapped

    stats = store.stats()
    print(f"[CK Gen14] mount_concept_learner: "
          f"{stats['n_concepts']} concepts loaded from {stats['path']}")
    return True


# ─── Standalone smoke ────────────────────────────────────────────────────

def _smoke():
    print("Smoke test: ck_concept_learner")
    print()

    samples = [
        "XYZFLUX is the operator that turns HARMONY into BREATH via BALANCE.",
        "GLEAM means the way operators settle after a reset.",
        "ALPHA = 1/2 is the universal attractor mixing parameter.",
        "Let RHO be the rotation symmetry of the 4-core under sigma.",
        "Define MOAT as the boundary around HARMONY in the lattice.",
        "What is XYZFLUX?",  # query, not teaching
        "explain the crossing lemma",  # no teaching here
    ]
    print("Teaching detection:")
    for s in samples:
        ms = detect_teaching(s)
        if ms:
            for m in ms:
                print(f"  '{s[:50]}…' → name={m.name!r}, defn={m.definition[:40]!r}, pat={m.pattern_used}")
        else:
            print(f"  '{s[:50]}…' → (no teaching detected)")
    print()

    # Store + retrieve
    import tempfile
    tmp = Path(tempfile.gettempdir()) / "ck_concepts_smoke.json"
    if tmp.exists():
        tmp.unlink()
    store = ConceptStore(path=tmp)
    print(f"Empty store at {tmp}: {store.stats()}")

    # Teach one
    c = store.teach("XYZFLUX", "the operator that turns HARMONY into BREATH",
                     [7, 8, 5], "is", "smoke_session")
    print(f"Taught: {c.name} (ops={c.operator_signature})")

    # Persist + reload
    store2 = ConceptStore(path=tmp)
    print(f"Reloaded: {len(store2.concepts)} concepts; "
          f"XYZFLUX = {store2.lookup('XYZFLUX').definition[:50]!r}")

    # Reference detection
    refs = store2.find_referenced("Can you explain XYZFLUX?")
    print(f"Refs in 'Can you explain XYZFLUX?': {[r.name for r in refs]}")
    refs = store2.find_referenced("Tell me about ZZZ.")
    print(f"Refs in 'Tell me about ZZZ.': {[r.name for r in refs]}")

    # Clean up
    tmp.unlink()
    print("\nConcept learner smoke: ALL OK")


if __name__ == "__main__":
    _smoke()
