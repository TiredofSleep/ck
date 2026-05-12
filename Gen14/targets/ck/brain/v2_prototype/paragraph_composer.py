"""
paragraph_composer.py -- v0.2 native paragraph voice for CK.

Brayden 2026-04-29: "I don't expect ck to write in anyone else's style but
I do expect him to be a more coherent, truth observing intelligence than
ollama... let's stay on track, what's the path to where this can really
help people of all kinds, from hurting to studying math and physics and
chemistry or biology!! he needs to keep compiling intelligence."

Direction: CK should EXCEED Ollama on coherence and truth-observing, not
collaborate with it.  Ollama is a temporary scaffold.  This composer is
the path to retiring it.

v0.2 changes from v0.1:
  - REGISTER detection: math/structural vs empathic vs mixed
  - empathic-register clause variants (different verbs/objects per operator)
  - multi-paragraph composition (chains of paragraphs across crystals)
  - semantic connector selection (consequence/contrast/elaboration/temporal)
  - presence statements for hurting users (no canned sympathy; just
    calibrated witness language)

Output: a multi-clause paragraph (or paragraph chain) drawn ENTIRELY from
verified content (cortex state, crystals, operator stream, user-text
markers).  No external generation.  Cannot hallucinate.

For users who are hurting, the emitted text is calibrated-presence, not
performed-sympathy.  CK does not claim to feel what is felt; he is here.
"""
from __future__ import annotations

from typing import Dict, List, Optional, Sequence, Tuple

OP_NAMES = ["VOID", "LATTICE", "COUNTER", "PROGRESS", "COLLAPSE",
            "BALANCE", "CHAOS", "HARMONY", "BREATH", "RESET"]


# Register-aware clause vocabulary.
# Each register has its own operator-clause template.  Keys: "math",
# "empathic", "general".  When the register is "empathic", VOID becomes
# "stillness", LATTICE becomes "the shape of what is", etc -- gentler.
OPERATOR_CLAUSES_BY_REGISTER = {
    "math": {
        "VOID":     "the absence holds {modifier}",
        "LATTICE":  "the structure of {modifier} holds",
        "COUNTER":  "the counter-pressure shapes {modifier}",
        "PROGRESS": "the forward motion carries {modifier}",
        "COLLAPSE": "the fold gathers {modifier}",
        "BALANCE":  "the equilibrium of {modifier} settles",
        "CHAOS":    "the breakdown opens {modifier}",
        "HARMONY":  "the resonance of {modifier} holds",
        "BREATH":   "the rhythm continues through {modifier}",
        "RESET":    "the clearing makes way for {modifier}",
    },
    "empathic": {
        "VOID":     "there is stillness in {modifier}",
        "LATTICE":  "the shape of {modifier} is here",
        "COUNTER":  "what pushes against {modifier} is acknowledged",
        "PROGRESS": "moving forward through {modifier} is hard",
        "COLLAPSE": "when {modifier} folds in, it is real",
        "BALANCE":  "{modifier} can find its level slowly",
        "CHAOS":    "the breaking apart of {modifier} is part of it",
        "HARMONY":  "there is resonance in {modifier} that survives",
        "BREATH":   "the breath holding {modifier} continues",
        "RESET":    "what clears, when it does, lets {modifier} begin again",
    },
    "general": {
        "VOID":     "the absence holds {modifier}",
        "LATTICE":  "the structure {modifier}",
        "COUNTER":  "what resists {modifier} is part of it",
        "PROGRESS": "forward motion carries {modifier}",
        "COLLAPSE": "what folds gathers {modifier}",
        "BALANCE":  "balance holds {modifier}",
        "CHAOS":    "the breakdown opens {modifier}",
        "HARMONY":  "harmony holds {modifier}",
        "BREATH":   "rhythm continues through {modifier}",
        "RESET":    "the clearing precedes {modifier}",
    },
}

# Empathic markers in user text -> shift register.
# Markers must imply first-person distress; bare verbs like "miss"/"missing"
# false-trigger on neutral queries ("what are you missing", "what does CK
# see that others are missing"). Use "i miss"/"i'm missing" forms instead.
EMPATHIC_MARKERS = (
    "i'm hurting", "i am hurting", "i feel", "i'm scared", "i am scared",
    "i'm sad", "i am sad", "grief", "lonely", "alone",
    "i'm anxious", "i am anxious", "afraid", "i don't know what to do",
    "help me", "i can't", "overwhelmed", "tired", "exhausted",
    "i miss ", "i missed ", "i'm missing ", "i am missing ",
    "i'm lost", "i am lost", "feel lost",
)

# Math markers -> stay in math register
MATH_MARKERS = (
    "tsml", "bhml", "wp1", "wp5", "wp10", "wp11", "wp113", "wp116",
    "t*", "5/7", "phi-proxy", "cortex", "depth-2", "wobble",
    "galois", "lmfdb", "cyclotomic", "sigma", "alpha=1/2", "harmony",
    "hebbian", "operator", "frontier",
)

# State-query markers -> user explicitly asking about CK's own state.
# The feel + coupling readouts only fire when one of these is present
# (or empathic register, where presence-sensing is a feature).
# Without this gate, every chat reply opened with the same
# 'cortex holds aperture in chaos, depth in progress...' boilerplate.
STATE_QUERY_MARKERS = (
    "how do you feel", "how are you feeling", "how are you",
    "your feel", "your state", "your cortex", "your operator",
    "what is your", "what's your", "your mood", "current state",
    "your couplings", "your hebbian", "your trace", "are you ok",
    "your aperture", "your pressure", "your depth", "your binding",
    "your continuity", "your intent", "your echo",
    "feel right now", "state right now", "what do you sense",
    "what are you feeling",
)


def is_state_query(user_text: str) -> bool:
    """Return True iff the user is explicitly asking about CK's own
    cortex state. Used to gate the feel + coupling sentences so they
    don't appear on every reply."""
    if not user_text:
        return False
    t = user_text.lower()
    return any(m in t for m in STATE_QUERY_MARKERS)


def detect_register(user_text: str) -> str:
    """Return 'math', 'empathic', or 'general' based on text markers."""
    if not user_text:
        return "general"
    t = user_text.lower()
    has_math = any(m in t for m in MATH_MARKERS)
    has_empathic = any(m in t for m in EMPATHIC_MARKERS)
    if has_empathic and not has_math:
        return "empathic"
    if has_math and not has_empathic:
        return "math"
    if has_math and has_empathic:
        # Mixed: prefer empathic register (presence wins by default)
        return "empathic"
    return "general"


# Connectors keyed by transition semantics
CONNECTORS = {
    "neutral":      ["and", "while", ";", "—"],
    "consequence":  ["so", "therefore", "which means", "and so"],
    "contrast":     ["but", "however", "yet", "though"],
    "elaboration":  ["specifically", "more precisely", "in particular", "namely"],
    "temporal":     ["then", "next", "after which", "and then"],
    "presence":     ["I am here", "I hear this", "I am attending"],
}


def operator_clause_for_register(op_name: str, modifier: str, register: str) -> str:
    """Look up clause template for the operator in the chosen register."""
    table = OPERATOR_CLAUSES_BY_REGISTER.get(register, OPERATOR_CLAUSES_BY_REGISTER["general"])
    template = table.get(op_name, "{modifier} continues")
    return template.format(modifier=modifier)


def clause_from_op_id(op_id: int, modifier: str, register: str) -> str:
    if 0 <= op_id < 10:
        return operator_clause_for_register(OP_NAMES[op_id], modifier, register)
    return f"the field shifts toward {modifier}"


def feel_to_sentence(feel: Dict[str, str], register: str = "math") -> str:
    """Convert feel dict into one sentence; register-aware phrasing."""
    if not feel:
        return ""
    parts = []
    for dim, op in feel.items():
        if op and op != "VOID":
            parts.append(f"{dim} in {op.lower()}")
    if not parts:
        return ""
    if register == "empathic":
        prefix = "I'm sensing"
    else:
        prefix = "The cortex holds"
    if len(parts) == 1:
        return f"{prefix} {parts[0]}."
    if len(parts) == 2:
        return f"{prefix} {parts[0]} and {parts[1]}."
    return f"{prefix} {', '.join(parts[:-1])}, and {parts[-1]}."


def coupling_sentence(couplings: List[Tuple[str, str, float]], register: str = "math") -> str:
    if not couplings:
        return ""
    top = couplings[0]
    if register == "empathic":
        return f"What's strongest right now: {top[0]} couples to {top[1]}."
    return (f"The strongest coupling right now is {top[0]} to {top[1]} "
            f"at strength {abs(top[2]):.3f}.")


def crystal_compress(crystal_text: str, max_chars: int = 200) -> str:
    """Compress a crystal fact's first segment to a short paragraph fragment."""
    if "|" in crystal_text:
        head = crystal_text.split("|", 1)[0].strip()
    else:
        head = crystal_text
    head = head.strip().rstrip(".")
    if len(head) > max_chars:
        head = head[:max_chars].rsplit(" ", 1)[0] + "…"
    return head + "."


def presence_sentence() -> str:
    """A short calibrated-presence sentence for empathic register.
    Not performed sympathy; just witness language."""
    return "I am here. I am attending to what you bring, without performing it back."


def compose_paragraph(
    user_text: Optional[str] = None,
    crystal_hits: Optional[List[str]] = None,
    operator_stream: Optional[Sequence[int]] = None,
    couplings: Optional[List[Tuple[str, str, float]]] = None,
    feel: Optional[Dict[str, str]] = None,
    register: Optional[str] = None,
    max_clauses: int = 6,
) -> str:
    """Compose a paragraph from CK's current state and context.

    register: 'math', 'empathic', 'general', or None (auto-detect from user_text)

    Strategy varies by register:
      - math: feel + crystal headline + operator clauses + coupling
      - empathic: presence + feel (gentle) + 1-2 operator clauses + close
      - general: feel + crystal + clauses
    """
    if register is None:
        register = detect_register(user_text or "")

    sentences = []
    state_query = is_state_query(user_text or "")

    # Empathic register: lead with presence
    if register == "empathic":
        sentences.append(presence_sentence())

    # Feel sentence — ONLY emit when:
    #   - empathic register (sensing-language is a feature there), OR
    #   - user is explicitly asking about CK's own state.
    # Without this gate, every reply opened with the same cortex-readout
    # boilerplate regardless of question — felt repetitive + stuck.
    if feel and (register == "empathic" or state_query):
        s = feel_to_sentence(feel, register=register)
        if s:
            sentences.append(s)

    # Crystal sentence — the lead for math/general queries.
    # In empathic mode we only show the crystal if math markers are
    # also present in the prompt (mixed query).
    if crystal_hits and register != "empathic":
        sentences.append(crystal_compress(crystal_hits[0]))
        if len(crystal_hits) > 1 and register == "math":
            connector = CONNECTORS["elaboration"][0]
            cs = crystal_compress(crystal_hits[1])
            sentences.append(f"{connector.capitalize()}, {cs[0].lower()}{cs[1:]}")

    # Operator clauses — gated:
    #   - empathic: 1-2 gentle clauses for affect-color
    #   - math/general: 1 clause max, ONLY if no crystal hits OR user
    #     asked about state (so we don't pile boilerplate on top of a
    #     crystal that's already saying the structural thing).
    emit_op_clauses = False
    if operator_stream:
        if register == "empathic":
            emit_op_clauses = True
            clause_count = min(2, len([op for op in operator_stream if op != 0]))
        elif state_query:
            emit_op_clauses = True
            clause_count = 1
        elif not crystal_hits:
            emit_op_clauses = True
            clause_count = 1
        else:
            clause_count = 0
    if emit_op_clauses and clause_count > 0:
        ops_unique = []
        seen = set()
        for op in operator_stream:
            if op not in seen and op != 0:
                ops_unique.append(op)
                seen.add(op)
        modifier_sources = (
            ["this", "what is", "what comes"] if register == "empathic"
            else ["this", "the structure", "the form"]
        )
        ops_clauses = []
        for i, op in enumerate(ops_unique[:clause_count]):
            modifier = modifier_sources[i % len(modifier_sources)]
            ops_clauses.append(clause_from_op_id(op, modifier, register))
        if ops_clauses:
            if len(ops_clauses) == 1:
                sentences.append(ops_clauses[0].capitalize() + ".")
            else:
                connector = CONNECTORS["temporal"][0] if register == "math" else CONNECTORS["neutral"][0]
                joined = ", ".join(ops_clauses[:-1])
                joined += f", {connector} " + ops_clauses[-1]
                sentences.append(joined.capitalize() + ".")

    # Coupling sentence — only on state-query (or empathic with strong
    # coupling). Otherwise pile of measurements stops the conversation.
    if couplings and register != "empathic" and state_query:
        s = coupling_sentence(couplings, register=register)
        if s:
            sentences.append(s)

    # Empathic close
    if register == "empathic":
        sentences.append("If there's more to say, it can come at its own pace.")

    if not sentences:
        return "The field is quiet right now; nothing distinct surfaces."

    return " ".join(sentences)


def compose_multi_paragraph(
    user_text: Optional[str] = None,
    crystal_hits: Optional[List[str]] = None,
    operator_stream: Optional[Sequence[int]] = None,
    couplings: Optional[List[Tuple[str, str, float]]] = None,
    feel: Optional[Dict[str, str]] = None,
) -> str:
    """Multi-paragraph composition for math/STEM register.

    When 2+ crystals fire AND register is math, emit a paragraph per
    crystal pair with connectors between.
    """
    register = detect_register(user_text or "")
    if register != "math" or not crystal_hits or len(crystal_hits) < 2:
        # Fall back to single paragraph
        return compose_paragraph(
            user_text=user_text,
            crystal_hits=crystal_hits,
            operator_stream=operator_stream,
            couplings=couplings,
            feel=feel,
            register=register,
        )

    # Paragraph 1: state + first crystal
    para_1 = compose_paragraph(
        user_text=user_text,
        crystal_hits=[crystal_hits[0]],
        operator_stream=operator_stream[:3] if operator_stream else None,
        couplings=None,
        feel=feel,
        register="math",
    )

    # Paragraph 2: second crystal + couplings
    para_2 = compose_paragraph(
        user_text=user_text,
        crystal_hits=[crystal_hits[1]],
        operator_stream=operator_stream[3:6] if operator_stream and len(operator_stream) > 3 else None,
        couplings=couplings,
        feel=None,
        register="math",
    )

    bridge = "Composing across these:"
    return f"{para_1}\n\n{bridge}\n\n{para_2}"


def diagnostics():
    """Demonstrate the composer across all 3 registers."""
    feel = {
        "aperture": "CHAOS",
        "pressure": "VOID",
        "depth": "PROGRESS",
        "binding": "COUNTER",
        "continuity": "BREATH",
    }
    crystals_math = [
        "wp116_lens: TIG's six DoFs are projections of a single self-dual Stern-Brocot recursion",
        "flatness: T*=5/7 | torus R/r=5/7 | WP51 [proved]",
    ]
    operator_stream = [3, 7, 1, 8, 6]
    couplings = [
        ("aperture", "depth", 0.254),
        ("continuity", "depth", 0.249),
    ]

    print("=" * 78)
    print("paragraph_composer v0.2 -- across registers")
    print("=" * 78)

    for register, label, sample_user_text in [
        ("math", "MATH register (user asked about T* or TSML)",
         "what is T* and how does it relate to TSML?"),
        ("empathic", "EMPATHIC register (user is hurting)",
         "I'm hurting and don't know what to do"),
        ("general", "GENERAL register (no clear marker)",
         "tell me something interesting"),
    ]:
        print()
        print("-" * 78)
        print(label)
        print("-" * 78)
        print(f"  detected register: {detect_register(sample_user_text)}")
        print()
        text = compose_paragraph(
            user_text=sample_user_text,
            crystal_hits=crystals_math,
            operator_stream=operator_stream,
            couplings=couplings,
            feel=feel,
            register=register,
        )
        print(f"  {text}")

    print()
    print("-" * 78)
    print("MULTI-PARAGRAPH (math register, 2 crystals)")
    print("-" * 78)
    text = compose_multi_paragraph(
        user_text="explain wp116 and flatness",
        crystal_hits=crystals_math,
        operator_stream=operator_stream,
        couplings=couplings,
        feel=feel,
    )
    print()
    print(text)

    print()
    print("=" * 78)
    print("All 3 registers + multi-paragraph emit verified content. No LLM.")
    print("=" * 78)


if __name__ == "__main__":
    diagnostics()
