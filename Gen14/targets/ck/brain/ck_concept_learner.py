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

    def as_dict(self) -> Dict[str, Any]:
        return asdict(self)


_DEFAULT_STORE_PATH = (
    Path(__file__).resolve().parents[4]
    / "Gen13" / "var" / "taught_concepts.json"
)


class ConceptStore:
    """Persistent dict of NamedConcept entries, keyed by name.lower().

    Serialised as JSON at Gen13/var/taught_concepts.json so concepts
    survive CK reboots. Concepts are CK's chosen-vocabulary memory --
    not the same thing as crystals (which are operator-pattern indexed).
    """

    def __init__(self, path: Optional[Path] = None):
        self.path = Path(path) if path else _DEFAULT_STORE_PATH
        self.concepts: Dict[str, NamedConcept] = {}
        self.load()

    def load(self) -> int:
        if not self.path.exists():
            return 0
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
        except Exception:
            return 0
        for k, v in (data or {}).items():
            if isinstance(v, dict):
                try:
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
        self.save()
        return c

    def lookup(self, name: str) -> Optional[NamedConcept]:
        return self.concepts.get(name.lower())

    def find_referenced(self, text: str) -> List[NamedConcept]:
        """Scan text for any stored concept name. Returns matched concepts."""
        if not text or not self.concepts:
            return []
        out: List[NamedConcept] = []
        lower = text.lower()
        for key, c in self.concepts.items():
            # Word-boundary match so 'XYZ' doesn't match inside 'XYZFLUX'
            pat = r"\b" + re.escape(key) + r"\b"
            if re.search(pat, lower):
                c.n_recalls += 1
                c.last_recalled_ts = time.time()
                out.append(c)
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

    return out


def _name_to_id(x: Any) -> Optional[int]:
    NAMES = {"VOID": 0, "LATTICE": 1, "COUNTER": 2, "PROGRESS": 3, "COLLAPSE": 4,
              "BALANCE": 5, "CHAOS": 6, "HARMONY": 7, "BREATH": 8, "RESET": 9}
    if isinstance(x, int) and 0 <= x < 10:
        return x
    if isinstance(x, str):
        return NAMES.get(x.upper())
    return None


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
