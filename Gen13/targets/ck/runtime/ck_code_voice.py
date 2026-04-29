"""
ck_code_voice.py -- Pure-CK code emitter (Python, first iteration).

Mirror of ck_tig_voice.py for code instead of prose.

  trajectory of operators -> CODE_VOCAB lookup -> Python block

  LATTICE  -> class / dataclass / type
  COUNTER  -> if / len / compare
  PROGRESS -> for / yield / recurse
  COLLAPSE -> sum / reduce / fold
  BALANCE  -> assign / equality
  HARMONY  -> return value
  BREATH   -> async / await / sleep / yield
  RESET    -> del / clear / exit
  CHAOS    -> try/except / random
  VOID     -> pass / None / NotImplemented

No LLM. Composition is driven by the operator algebra; word picks are
indexed by operator. Every emitted block is checked with ast.parse so
the output is syntactically valid Python or the function returns None.

This is iteration 1. Single language. One block per call. The aim is
to give CK a writer to match his existing reader (`/spectrometer`),
not to rival a compiler.

(c) 2026 Brayden Sanders / 7Site LLC -- Trinity Infinity Geometry
"""
from __future__ import annotations

import ast
import random
import re
from typing import Dict, List, Optional

OP_NAMES = ["VOID", "LATTICE", "COUNTER", "PROGRESS", "COLLAPSE",
            "BALANCE", "CHAOS", "HARMONY", "BREATH", "RESET"]
VOID, LATTICE, COUNTER, PROGRESS, COLLAPSE = 0, 1, 2, 3, 4
BALANCE, CHAOS, HARMONY, BREATH, RESET = 5, 6, 7, 8, 9


# ---------------------------------------------------------------------------
# CODE_VOCAB: per-operator code-construct vocabulary, indexed by archetype.
# Same shape as TIGVoice's DOMAIN_VOCAB.
# ---------------------------------------------------------------------------

CODE_VOCAB: Dict[int, Dict[str, List[str]]] = {
    VOID: {
        "names":  ["nothing", "stub", "placeholder", "_unused"],
        "values": ["None", "pass", "NotImplemented", "..."],
        "verbs":  ["pass", "return None", "raise NotImplementedError"],
    },
    LATTICE: {
        "names":  ["Frame", "Lattice", "Structure", "Schema", "Record"],
        "values": ["@dataclass", "class", "NamedTuple", "TypedDict"],
        "verbs":  ["defines", "declares", "structures", "frames"],
    },
    COUNTER: {
        "names":  ["count", "size", "n", "k", "boundary", "delta"],
        "values": ["len(x)", "len(items)", "len(arc)", "max(0, n)"],
        "verbs":  ["measures", "counts", "compares", "bounds"],
    },
    PROGRESS: {
        "names":  ["step", "iter", "advance", "walk", "trajectory"],
        "values": ["for x in xs", "for i in range(n)", "yield x", "recurse(rest)"],
        "verbs":  ["iterates", "advances", "walks", "yields"],
    },
    COLLAPSE: {
        "names":  ["total", "fold", "compressed", "projected"],
        "values": ["sum(xs)", "min(xs)", "max(xs)",
                   "reduce(lambda a, b: a + b, xs)"],
        "verbs":  ["reduces", "folds", "compresses", "projects"],
    },
    BALANCE: {
        "names":  ["lhs", "rhs", "fixed_point", "equilibrium"],
        "values": ["a == b", "x = y", "x is y", "abs(a - b) < eps"],
        "verbs":  ["equates", "balances", "assigns", "preserves"],
    },
    CHAOS: {
        "names":  ["entropy", "bifurcation", "exception", "noise"],
        "values": ["random.choice(pool)", "try / except",
                   "raise ValueError", "shuffle(xs)"],
        "verbs":  ["randomizes", "diverges", "raises", "shuffles"],
    },
    HARMONY: {
        "names":  ["result", "answer", "solution", "fixed_point"],
        "values": ["return value", "return cls(...)",
                   "return x", "yield x"],
        "verbs":  ["returns", "yields", "settles", "resolves"],
    },
    BREATH: {
        "names":  ["pulse", "tick", "beat", "rhythm"],
        "values": ["await coro", "async def", "asyncio.sleep(0)",
                   "yield from xs"],
        "verbs":  ["awaits", "sleeps", "breathes", "yields"],
    },
    RESET: {
        "names":  ["clear", "reset", "purge", "shutdown"],
        "values": ["del x", "x.clear()", "sys.exit(0)", "x = None"],
        "verbs":  ["clears", "deletes", "purges", "resets"],
    },
}


# ---------------------------------------------------------------------------
# FRAMES: code skeletons keyed by operator. Each is a fill-in-the-blank
# template. `_compose_frame` does the substitution.
# ---------------------------------------------------------------------------

FRAMES: Dict[int, List[str]] = {
    VOID: [
        "def {name}({arg}):\n    pass",
        "def {name}({arg}):\n    return None",
        "{name} = None",
    ],
    LATTICE: [
        "@dataclass\nclass {Name}:\n    {field}: {ftype}",
        "class {Name}:\n    def __init__(self, {arg}):\n        self.{arg} = {arg}",
    ],
    COUNTER: [
        "def {name}({arg}) -> int:\n    return len({arg})",
        "if len({arg}) > {n}:\n    return True\nreturn False",
    ],
    PROGRESS: [
        "def {name}({arg}):\n    for x in {arg}:\n        yield x",
        "def {name}(n: int):\n    if n <= 0:\n        return 0\n    return 1 + {name}(n - 1)",
        "for x in {arg}:\n    yield x",
    ],
    COLLAPSE: [
        "def {name}({arg}) -> float:\n    return sum({arg})",
        "def {name}({arg}):\n    return min({arg}) if {arg} else None",
    ],
    BALANCE: [
        "def {name}(a, b) -> bool:\n    return a == b",
        "def {name}(a: float, b: float, eps: float = 1e-9) -> bool:\n    return abs(a - b) < eps",
        "{lhs} = {rhs}",
    ],
    CHAOS: [
        "def {name}({arg}):\n    try:\n        return {arg}[0]\n    except (IndexError, TypeError):\n        return None",
        "import random\ndef {name}(pool):\n    return random.choice(pool)",
    ],
    HARMONY: [
        "def {name}({arg}):\n    return {arg}",
        "def {name}({arg}):\n    return {arg} if {arg} is not None else None",
    ],
    BREATH: [
        "import asyncio\nasync def {name}({arg}):\n    await asyncio.sleep(0)\n    return {arg}",
        "def {name}({arg}):\n    while True:\n        yield {arg}",
    ],
    RESET: [
        "def {name}({arg}):\n    {arg}.clear()\n    return {arg}",
        "def {name}():\n    return None",
    ],
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_IDENT = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


def _safe_ident(word: str, fallback: str) -> str:
    """Coerce `word` into a Python identifier, or return `fallback`."""
    if not word:
        return fallback
    w = re.sub(r"[^A-Za-z0-9_]", "_", word.lower())
    w = re.sub(r"_+", "_", w).strip("_")
    if not w or not _IDENT.match(w) or w[0].isdigit():
        return fallback
    # Avoid Python reserved words
    import keyword as _kw
    if _kw.iskeyword(w):
        return fallback
    return w


def _capitalize(name: str) -> str:
    """For class names: turn `session_field` into `SessionField`."""
    parts = re.split(r"[_\s]+", name)
    return "".join(p[:1].upper() + p[1:] for p in parts if p) or "Anon"


def dominant_op(trajectory: List[int]) -> int:
    """Pick the most frequent operator in the chain.
    Ties broken by latest occurrence so the chain's closing flavor wins."""
    if not trajectory:
        return HARMONY
    counts: Dict[int, int] = {}
    for op in trajectory:
        counts[op] = counts.get(op, 0) + 1
    top = max(counts.values())
    # Among ties, prefer the one that appears latest.
    last_idx_for_top = -1
    winner = HARMONY
    for i, op in enumerate(trajectory):
        if counts[op] == top and i > last_idx_for_top:
            last_idx_for_top = i
            winner = op
    return winner


def _anchor_name(user_text: str, default: str) -> str:
    """Pull a content word from the user prompt to anchor the function/class name."""
    if not user_text:
        return default
    stop = {"the", "a", "an", "is", "are", "was", "were", "be", "to", "of",
            "in", "and", "or", "it", "you", "i", "we", "they", "do", "did",
            "has", "have", "that", "this", "for", "at", "on", "with", "what",
            "how", "when", "why", "can", "my", "your", "me", "him", "her",
            "us", "not", "no", "so", "make", "give", "show", "write", "tell",
            "function", "method", "code", "python", "class", "def"}
    candidates = [
        w.lower().strip(".,?!;:'\"()[]{}")
        for w in user_text.split()
        if len(w) >= 3 and w.lower() not in stop
    ]
    for c in candidates:
        ident = _safe_ident(c, "")
        if ident:
            return ident
    return default


def _validate_python(code: str) -> bool:
    """ast.parse the generated block. Return True if it parses."""
    try:
        ast.parse(code)
        return True
    except (SyntaxError, ValueError):
        return False


# ---------------------------------------------------------------------------
# Compose
# ---------------------------------------------------------------------------

class CKCodeVoice:
    """Pure-CK Python emitter. Operator trajectory in, parseable code out."""

    def __init__(self, seed: Optional[int] = None):
        self.rng = random.Random(seed)
        self._last_block: Optional[str] = None

    def compose(
        self,
        trajectory: List[int],
        user_text: str = "",
        coherence: float = 0.5,
        max_attempts: int = 6,
    ) -> Optional[str]:
        """Emit one Python block driven by the operator trajectory.

        Returns the code string on success, or None if no valid block
        could be assembled in `max_attempts` tries.
        """
        if not trajectory:
            return None

        op = dominant_op(trajectory)
        frames = FRAMES.get(op, FRAMES[HARMONY])

        # Substitution pool from the dominant op + neighbors
        names = list(CODE_VOCAB[op]["names"])
        # Anchor: pull a content word from the user prompt as the primary name
        primary = _anchor_name(user_text, names[0] if names else "ck_block")

        # Try a few frame choices until one parses
        for _ in range(max_attempts):
            frame = self.rng.choice(frames)
            field_pool = ["x", "y", "n", "k", "value", "items", "arc", "field"]
            type_pool = ["int", "float", "list", "dict", "Optional[float]"]
            # Build substitution dict; only the keys present in the frame matter
            subs = {
                "name": primary,
                "Name": _capitalize(primary),
                "arg":  self.rng.choice(field_pool),
                "n":    str(self.rng.choice([0, 1, 5, 10])),
                "field": self.rng.choice(field_pool),
                "ftype": self.rng.choice(type_pool),
                "lhs": self.rng.choice(field_pool),
                "rhs": self.rng.choice(["0", "0.0", "[]", "None", "0.5"]),
            }
            try:
                block = frame.format(**subs)
            except (KeyError, IndexError):
                continue

            # If block uses @dataclass it needs the import
            if "@dataclass" in block:
                block = "from dataclasses import dataclass\n\n" + block

            if _validate_python(block):
                self._last_block = block
                return block

        return None

    def compose_with_header(
        self,
        trajectory: List[int],
        user_text: str = "",
        coherence: float = 0.5,
    ) -> Optional[str]:
        """compose() plus a one-line algebraic header comment."""
        block = self.compose(trajectory, user_text, coherence)
        if block is None:
            return None
        op = dominant_op(trajectory)
        chain_str = " -> ".join(OP_NAMES[o] for o in trajectory[:10])
        verb = self.rng.choice(CODE_VOCAB[op]["verbs"])
        header = (
            f"# CK trajectory: {chain_str}\n"
            f"# dominant op: {OP_NAMES[op]} ({verb})\n"
        )
        return header + block


# ---------------------------------------------------------------------------
# Module-level singleton + convenience wrapper
# ---------------------------------------------------------------------------

_singleton: Optional[CKCodeVoice] = None


def get_code_voice() -> CKCodeVoice:
    global _singleton
    if _singleton is None:
        _singleton = CKCodeVoice()
    return _singleton


def code_respond(
    trajectory: List[int],
    user_text: str = "",
    coherence: float = 0.5,
) -> Optional[str]:
    """Convenience wrapper. Returns code string or None."""
    try:
        return get_code_voice().compose_with_header(trajectory, user_text, coherence)
    except Exception:
        return None


# ---------------------------------------------------------------------------
# Self-test (run as script)
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    voice = CKCodeVoice(seed=42)
    print("=" * 70)
    print("ck_code_voice.py self-test")
    print("=" * 70)

    test_cases = [
        # (label, prompt, trajectory)
        ("HARMONY-dominant — return helper",
         "write a helper that returns the result",
         [LATTICE, COUNTER, HARMONY, HARMONY, HARMONY, BALANCE]),
        ("PROGRESS-dominant — iterator",
         "iterate over the trajectory",
         [LATTICE, PROGRESS, PROGRESS, PROGRESS, HARMONY]),
        ("COLLAPSE-dominant — reducer",
         "compute the total",
         [LATTICE, COLLAPSE, COLLAPSE, COLLAPSE, HARMONY]),
        ("LATTICE-dominant — dataclass",
         "define a session record",
         [LATTICE, LATTICE, LATTICE, BALANCE, HARMONY]),
        ("COUNTER-dominant — measure",
         "count the items in the arc",
         [COUNTER, COUNTER, COUNTER, BALANCE, HARMONY]),
        ("CHAOS-dominant — try/except",
         "wrap a fallible operation",
         [CHAOS, CHAOS, COLLAPSE, HARMONY]),
        ("BREATH-dominant — async",
         "yield rhythmically",
         [BREATH, BREATH, BREATH, PROGRESS, HARMONY]),
        ("RESET-dominant — cleanup",
         "purge the cache",
         [RESET, RESET, BALANCE, HARMONY]),
        ("BALANCE-dominant — equality check",
         "check equality of two fields",
         [BALANCE, BALANCE, COUNTER, HARMONY]),
        ("VOID-dominant — stub",
         "leave a stub",
         [VOID, VOID, HARMONY]),
    ]

    passed = 0
    for label, prompt, traj in test_cases:
        block = voice.compose_with_header(traj, user_text=prompt, coherence=0.8)
        ok = block is not None and _validate_python(
            "\n".join(line for line in block.splitlines() if not line.startswith("#"))
        )
        status = "PASS" if ok else "FAIL"
        if ok:
            passed += 1
        print(f"\n--- {label} [{status}] ---")
        print(f"prompt: {prompt}")
        print(f"trajectory: {[OP_NAMES[o] for o in traj]}")
        if block:
            print(block)
        else:
            print("(no block produced)")

    print("\n" + "=" * 70)
    print(f"Summary: {passed} / {len(test_cases)} blocks parseable")
    print("=" * 70)
