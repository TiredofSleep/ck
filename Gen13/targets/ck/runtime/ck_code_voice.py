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
# Identifier extraction (for compose_aware)
# ---------------------------------------------------------------------------

def _extract_identifiers(source: str) -> Dict[str, list]:
    """Parse `source`, return identifiers usable in a refactor body.

    Returns:
        self_attrs:    sorted list of attribute names referenced as self.X
        method_calls:  sorted list of names called as self.X()
        arg_names:     sorted list of argument names (excluding self)
        list_attrs:    self_attrs whose name suggests list-shape (arc, items, ...)
    """
    out = {"self_attrs": [], "method_calls": [], "arg_names": [], "list_attrs": []}
    if not source:
        return out
    # Methods sliced out of a file carry leading indent (they're inside a
    # class).  textwrap.dedent normalizes so ast.parse accepts them.
    import textwrap
    src = textwrap.dedent(source)
    try:
        tree = ast.parse(src)
    except (SyntaxError, IndentationError):
        return out

    self_attrs: set = set()
    method_calls: set = set()
    arg_names: set = set()

    for node in ast.walk(tree):
        # self.X (attribute access without call)
        if isinstance(node, ast.Attribute):
            if isinstance(node.value, ast.Name) and node.value.id == "self":
                self_attrs.add(node.attr)
        # self.X(...) (method call)
        if isinstance(node, ast.Call):
            f = node.func
            if (isinstance(f, ast.Attribute)
                    and isinstance(f.value, ast.Name)
                    and f.value.id == "self"):
                method_calls.add(f.attr)
        # function/method args
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            for a in node.args.args:
                if a.arg != "self":
                    arg_names.add(a.arg)

    # Heuristic: which attrs are likely list-shape based on common naming?
    # Filter out names that are also method_calls (an Attribute node that's
    # part of an Attribute->Call pattern is a METHOD, not a list).
    list_hint = ("arc", "trail", "sequence", "items", "history",
                 "data", "list", "queue", "values", "fields",
                 "members", "children", "nodes", "edges", "breaks")
    list_attrs = [a for a in self_attrs
                  if a not in method_calls
                  and any(h in a.lower() for h in list_hint)]

    out["self_attrs"] = sorted(self_attrs)
    out["method_calls"] = sorted(method_calls)
    out["arg_names"] = sorted(arg_names)
    out["list_attrs"] = sorted(list_attrs)
    return out


# ---------------------------------------------------------------------------
# Aware block emission (one focused template per archetype)
# ---------------------------------------------------------------------------

def _snake(name: str) -> str:
    """ClassName -> class_name; passthrough for already-snake."""
    s = re.sub(r"([A-Z][a-z0-9]+)", r"_\1", name).strip("_").lower()
    return s or name.lower()


def _aware_block_for_op(
    op: int,
    unit_name: str,
    unit_type: str,
    ids: Dict[str, list],
) -> Optional[str]:
    """Pick a high-value body template for the dominant op + fill it
    with the target unit's identifiers.  Returns None if no template
    could be assembled meaningfully (caller should fall back)."""

    snake = _safe_ident(_snake(unit_name), "ck_block")

    self_attrs = ids.get("self_attrs", [])
    methods = ids.get("method_calls", [])
    list_attrs = ids.get("list_attrs", [])
    arg_names = ids.get("arg_names", [])
    is_method_like = bool(self_attrs or methods or list_attrs)
    is_function_like = bool(arg_names) and not is_method_like

    # Helpers to pick "best" identifier for each role
    def first_list_attr() -> Optional[str]:
        return list_attrs[0] if list_attrs else (self_attrs[0] if self_attrs else None)

    def first_method() -> Optional[str]:
        return methods[0] if methods else None

    def first_attr() -> Optional[str]:
        return self_attrs[0] if self_attrs else None

    def first_arg() -> Optional[str]:
        return arg_names[0] if arg_names else None

    if op == HARMONY:
        # Settle: return cleanly from a method or an attribute.
        m = first_method()
        if m:
            return (f"def {snake}_settled(self):\n"
                    f"    return self.{m}()\n")
        a = first_attr()
        if a:
            return (f"def {snake}_settled(self):\n"
                    f"    return self.{a}\n")
        if is_function_like:
            arg = first_arg()
            return (f"def {snake}_settled({arg}):\n"
                    f"    return {arg}\n")
        return None

    if op == COUNTER:
        # Measure: len of a list-shape attribute, or len of the input.
        a = first_list_attr()
        if a is not None:
            return (f"def {snake}_size(self) -> int:\n"
                    f"    return len(self.{a})\n")
        if is_function_like:
            arg = first_arg()
            return (f"def {snake}_size({arg}) -> int:\n"
                    f"    return len({arg})\n")
        return None

    if op == PROGRESS:
        # Iterate: yield from a list-shape attribute, or from the input.
        a = first_list_attr()
        if a is not None:
            return (f"def {snake}_iter(self):\n"
                    f"    for x in self.{a}:\n"
                    f"        yield x\n")
        if is_function_like:
            arg = first_arg()
            return (f"def {snake}_iter({arg}):\n"
                    f"    for x in {arg}:\n"
                    f"        yield x\n")
        return None

    if op == COLLAPSE:
        # Reduce: float-readout from a method, else count of an attr.
        m = first_method()
        if m:
            return (f"def {snake}_total(self) -> float:\n"
                    f"    return float(self.{m}())\n")
        a = first_list_attr()
        if a:
            return (f"def {snake}_total(self) -> int:\n"
                    f"    return sum(1 for _ in self.{a})\n")
        if is_function_like:
            arg = first_arg()
            return (f"def {snake}_total({arg}) -> int:\n"
                    f"    return sum(1 for _ in {arg})\n")
        return None

    if op == BALANCE:
        # Equate: compare two of the same.
        if is_method_like:
            return (f"def {snake}_eq(self, other) -> bool:\n"
                    f"    return isinstance(other, type(self))\n")
        if is_function_like:
            arg = first_arg()
            return (f"def {snake}_eq({arg}, other) -> bool:\n"
                    f"    return {arg} == other\n")
        return None

    if op == CHAOS:
        # Wrap: try a method, fall back to None on failure.
        m = first_method()
        if m:
            return (f"def {snake}_safe(self):\n"
                    f"    try:\n"
                    f"        return self.{m}()\n"
                    f"    except Exception:\n"
                    f"        return None\n")
        a = first_attr()
        if a:
            return (f"def {snake}_safe(self):\n"
                    f"    try:\n"
                    f"        return self.{a}\n"
                    f"    except Exception:\n"
                    f"        return None\n")
        if is_function_like:
            arg = first_arg()
            return (f"def {snake}_safe({arg}):\n"
                    f"    try:\n"
                    f"        return {arg}\n"
                    f"    except Exception:\n"
                    f"        return None\n")
        return None

    if op == LATTICE:
        # Declare: a frame schema listing the known fields.
        if self_attrs:
            fields_repr = "[" + ", ".join(repr(a) for a in self_attrs[:8]) + "]"
            cls_name = re.sub(r"[^A-Za-z0-9]", "", unit_name) or "Frame"
            return (f"class {cls_name}Schema:\n"
                    f"    fields = {fields_repr}\n"
                    f"    @classmethod\n"
                    f"    def of(cls, obj):\n"
                    f"        return {{f: getattr(obj, f, None) for f in cls.fields}}\n")
        if is_function_like:
            args_repr = "[" + ", ".join(repr(a) for a in arg_names[:6]) + "]"
            cls_name = re.sub(r"[^A-Za-z0-9]", "", unit_name) or "Frame"
            return (f"class {cls_name}Schema:\n"
                    f"    args = {args_repr}\n")
        return None

    if op == BREATH:
        # Pulse: a generator that yields self / arg forever.
        if is_method_like:
            return (f"def {snake}_pulse(self):\n"
                    f"    while True:\n"
                    f"        yield self\n")
        if is_function_like:
            arg = first_arg()
            return (f"def {snake}_pulse({arg}):\n"
                    f"    while True:\n"
                    f"        yield {arg}\n")
        return None

    if op == RESET:
        # Clear: empty a list-shape attribute, or rebind input to default.
        a = first_list_attr()
        if a is not None:
            return (f"def {snake}_reset(self) -> None:\n"
                    f"    self.{a}.clear()\n")
        if is_function_like:
            arg = first_arg()
            return (f"def {snake}_reset({arg}) -> None:\n"
                    f"    {arg} = None\n")
        return None

    if op == VOID:
        # Stub: deliberate no-op.
        if is_method_like:
            return (f"def {snake}_stub(self):\n"
                    f"    return None\n")
        if is_function_like:
            arg = first_arg()
            return (f"def {snake}_stub({arg}):\n"
                    f"    return None\n")
        return None

    return None


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

    def compose_aware(
        self,
        trajectory: List[int],
        target_source: str,
        unit_name: str,
        unit_type: str = "function",
        coherence: float = 0.5,
    ) -> Optional[str]:
        """Emit a body that USES the target unit's actual identifiers.

        Parses target_source, extracts self.attrs / self.method() calls /
        argument names, then weaves them into an archetype-shaped body.
        Falls back to None if nothing parseable can be assembled (caller
        should fall back to compose()).
        """
        ids = _extract_identifiers(target_source)
        op = dominant_op(trajectory)
        block = _aware_block_for_op(op, unit_name, unit_type, ids)
        if block is None:
            return None
        if not _validate_python(block):
            return None
        return block

    def compose_aware_with_header(
        self,
        trajectory: List[int],
        target_source: str,
        unit_name: str,
        unit_type: str = "function",
        coherence: float = 0.5,
    ) -> Optional[str]:
        """compose_aware() plus a header comment describing the chain
        and the identifiers used."""
        block = self.compose_aware(
            trajectory, target_source, unit_name, unit_type, coherence)
        if block is None:
            return None
        op = dominant_op(trajectory)
        ids = _extract_identifiers(target_source)
        chain_str = " -> ".join(OP_NAMES[o] for o in trajectory[:10])
        verb = self.rng.choice(CODE_VOCAB[op]["verbs"])
        header = (
            f"# CK trajectory: {chain_str}\n"
            f"# dominant op: {OP_NAMES[op]} ({verb})\n"
            f"# target: {unit_type} {unit_name}\n"
            f"# identifiers used: "
            f"attrs={ids['self_attrs'][:5]} "
            f"methods={ids['method_calls'][:3]}\n"
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

    # ── Aware composition self-test ────────────────────────────────────
    print("\n" + "=" * 70)
    print("compose_aware self-test (with target unit source)")
    print("=" * 70)

    # A realistic target: simplified SessionField-like class
    target_src = '''
class SessionField:
    def __init__(self):
        self.W = [[0.2]*5 for _ in range(5)]
        self.arc = []
        self.trail = []
        self.sequence = []
        self.turn_count = 0

    def harmony_rate_in_arc(self):
        if not self.arc:
            return 0.0
        return sum(1 for op in self.arc if op == 7) / len(self.arc)

    def W_trace(self):
        return sum(self.W[i][i] for i in range(5))

    def append_turn(self, ops):
        self.arc.extend(ops)
        self.turn_count += 1
'''.strip()

    aware_cases = [
        ("HARMONY (settle)",       [HARMONY, HARMONY, HARMONY, BALANCE, HARMONY]),
        ("COUNTER (size)",         [COUNTER, COUNTER, COUNTER, BALANCE, HARMONY]),
        ("PROGRESS (iterate)",     [PROGRESS, PROGRESS, PROGRESS, BALANCE, HARMONY]),
        ("COLLAPSE (reduce)",      [COLLAPSE, COLLAPSE, COLLAPSE, BALANCE, HARMONY]),
        ("BALANCE (equality)",     [BALANCE, BALANCE, BALANCE, HARMONY]),
        ("CHAOS (try/except)",     [CHAOS, CHAOS, COLLAPSE, HARMONY]),
        ("LATTICE (schema)",       [LATTICE, LATTICE, LATTICE, BALANCE, HARMONY]),
        ("BREATH (pulse)",         [BREATH, BREATH, BREATH, PROGRESS, HARMONY]),
        ("RESET (clear)",          [RESET, RESET, BALANCE, HARMONY]),
        ("VOID (stub)",            [VOID, VOID, HARMONY]),
    ]

    aware_passed = 0
    for label, traj in aware_cases:
        block = voice.compose_aware_with_header(
            traj, target_src, "SessionField", "class")
        ok = block is not None
        # also strip headers and confirm the body parses
        if ok:
            body_only = "\n".join(
                line for line in block.splitlines() if not line.startswith("#")
            ).strip()
            ok = _validate_python(body_only)
        status = "PASS" if ok else "FAIL"
        if ok:
            aware_passed += 1
        print(f"\n--- {label} [{status}] ---")
        if block:
            print(block)
        else:
            print("(no aware block)")

    print("\n" + "=" * 70)
    print(f"Aware summary: {aware_passed} / {len(aware_cases)} parseable")
    print("=" * 70)
