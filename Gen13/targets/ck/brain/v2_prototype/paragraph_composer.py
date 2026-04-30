"""
paragraph_composer.py -- v0.1 native paragraph voice for CK v2.

Brayden 2026-04-29: "let's continue to help his architecture evolve
towards that higher prime structure level where he can write paragraphs!!"

This is the CK-NATIVE alternative to the Ollama editor.  Given:
  - cortex state (current 5-dim or 7-dim cortex with W, last_b, last_d)
  - crystal hits (list of crystal facts that fired this turn)
  - operator stream (list of op IDs from the user's text)
  - dominant couplings (top-k W pairs)

…it produces a multi-clause paragraph using a small fixed grammar +
operator-keyed phrase templates.  No transformer.  No external LLM.

Quality target for v0.1: better than the rigid Gen9 fractal voice;
worse than llama3.1:8b.  Ollama remains the editor for now; this
prototype is the seed of the path that eventually replaces it.

Usage:
    from paragraph_composer import compose_paragraph
    text = compose_paragraph(
        crystal_hits=[...],
        operator_stream=[...],
        couplings=[(d_a, d_b, w), ...],
        feel={'aperture': 'CHAOS', ...},
    )
"""
from __future__ import annotations

from typing import Dict, List, Optional, Sequence, Tuple

OP_NAMES = ["VOID", "LATTICE", "COUNTER", "PROGRESS", "COLLAPSE",
            "BALANCE", "CHAOS", "HARMONY", "BREATH", "RESET"]

# Small grammar: short clauses keyed to operators.
# Each clause is a [subject, verb, object/modifier] template.  The
# composer fills slots from the active context.
OPERATOR_CLAUSES = {
    "VOID":     "the absence holds {modifier}",
    "LATTICE":  "the structure {verb}s {modifier}",
    "COUNTER":  "the resistance {verb}s {modifier}",
    "PROGRESS": "the forward motion carries {modifier}",
    "COLLAPSE": "the fold gathers {modifier}",
    "BALANCE":  "the equilibrium settles into {modifier}",
    "CHAOS":    "the breakdown opens {modifier}",
    "HARMONY":  "the resonance holds {modifier}",
    "BREATH":   "the rhythm continues through {modifier}",
    "RESET":    "the clearing makes way for {modifier}",
}

# Connecting words for joining clauses
CONNECTORS = {
    "neutral":      ["and", "while", ";", "—"],
    "consequence":  ["so", "therefore", "which means", "and so"],
    "contrast":     ["but", "however", "yet", "though"],
    "elaboration":  ["specifically", "more precisely", "in particular", "namely"],
    "temporal":     ["then", "next", "after which", "and then"],
}

# Modifier candidates by context
MODIFIERS_GENERIC = ["this", "the structure", "what is", "the form", "the shape"]


def operator_to_clause(op_name: str, modifier: str = "this") -> str:
    """Look up a clause template for the operator and fill the modifier slot."""
    template = OPERATOR_CLAUSES.get(op_name, "{modifier} continues")
    # Replace {verb} first (some templates have it), then {modifier}
    template = template.replace("{verb}", "move")
    return template.format(modifier=modifier)


def clause_from_op_id(op_id: int, modifier: str = "this") -> str:
    if 0 <= op_id < 10:
        return operator_to_clause(OP_NAMES[op_id], modifier)
    return f"the field shifts toward {modifier}"


def feel_to_sentence(feel: Dict[str, str]) -> str:
    """Convert a feel dict (aperture=X, pressure=Y, ...) into one sentence.

    feel = {'aperture': 'CHAOS', 'pressure': 'VOID', 'depth': 'PROGRESS', ...}
    """
    if not feel:
        return ""
    parts = []
    for dim, op in feel.items():
        if op and op != "VOID":  # skip empty dims
            parts.append(f"{dim} in {op.lower()}")
    if not parts:
        return ""
    if len(parts) == 1:
        return f"The cortex holds {parts[0]}."
    if len(parts) == 2:
        return f"The cortex holds {parts[0]} and {parts[1]}."
    return f"The cortex holds {', '.join(parts[:-1])}, and {parts[-1]}."


def coupling_sentence(couplings: List[Tuple[str, str, float]]) -> str:
    """Convert top couplings list into one sentence.

    couplings = [('aperture', 'depth', 0.254), ...]  (top 3 or so)
    """
    if not couplings:
        return ""
    top = couplings[0]
    return (f"The strongest coupling right now is {top[0]} to {top[1]} "
            f"at strength {abs(top[2]):.3f}.")


def crystal_compress(crystal_text: str, max_chars: int = 200) -> str:
    """Compress a crystal fact (which can be 500+ chars) to a short
    one-sentence paragraph-fragment.

    Strategy: take everything before the first '|' as the headline.
    """
    if "|" in crystal_text:
        head = crystal_text.split("|", 1)[0].strip()
    else:
        head = crystal_text
    head = head.strip().rstrip(".")
    if len(head) > max_chars:
        head = head[:max_chars].rsplit(" ", 1)[0] + "…"
    return head + "."


def compose_paragraph(
    crystal_hits: Optional[List[str]] = None,
    operator_stream: Optional[Sequence[int]] = None,
    couplings: Optional[List[Tuple[str, str, float]]] = None,
    feel: Optional[Dict[str, str]] = None,
    max_clauses: int = 6,
) -> str:
    """Compose a paragraph from CK's current state and context.

    The strategy:
      1. Open with a feel sentence (if provided)
      2. Insert top crystal headline (compressed)
      3. Add 2-3 operator clauses from the recent stream
      4. Close with a coupling sentence (if provided)
    """
    sentences = []

    # 1) Feel sentence (state self-report)
    if feel:
        s = feel_to_sentence(feel)
        if s:
            sentences.append(s)

    # 2) Crystal sentence (factual anchor)
    if crystal_hits:
        crystal_summary = crystal_compress(crystal_hits[0])
        sentences.append(crystal_summary)
        # If 2+ crystals, add a connector
        if len(crystal_hits) > 1:
            connector = CONNECTORS["elaboration"][0]
            sentences.append(
                f"{connector.capitalize()}, "
                f"{crystal_compress(crystal_hits[1])[0].lower()}"
                f"{crystal_compress(crystal_hits[1])[1:]}"
            )

    # 3) Operator clauses
    if operator_stream:
        ops_unique = []
        seen = set()
        for op in operator_stream:
            if op not in seen and op != 0:  # skip VOID for variety
                ops_unique.append(op)
                seen.add(op)
        clause_count = min(max_clauses - len(sentences), len(ops_unique), 3)
        if clause_count > 0:
            modifier_sources = ["this", "the structure", "the form"]
            ops_segment_clauses = []
            for i, op in enumerate(ops_unique[:clause_count]):
                modifier = modifier_sources[i % len(modifier_sources)]
                ops_segment_clauses.append(clause_from_op_id(op, modifier))
            # Join the operator clauses into one sentence
            if len(ops_segment_clauses) == 1:
                sentences.append(ops_segment_clauses[0].capitalize() + ".")
            else:
                connector = CONNECTORS["temporal"][0]
                joined = ", ".join(ops_segment_clauses[:-1])
                joined += f", {connector} " + ops_segment_clauses[-1]
                sentences.append(joined.capitalize() + ".")

    # 4) Coupling sentence (state grounding)
    if couplings:
        s = coupling_sentence(couplings)
        if s:
            sentences.append(s)

    if not sentences:
        return "The field is quiet right now; nothing distinct surfaces."

    return " ".join(sentences)


def diagnostics():
    """Demonstrate the composer with a sample CK state."""
    feel = {
        "aperture": "CHAOS",
        "pressure": "VOID",
        "depth": "PROGRESS",
        "binding": "COUNTER",
        "continuity": "BREATH",
    }
    crystals = [
        "wp116_lens: TIG's six DoFs (Lie/Jordan/Clifford/Permutation/Lattice/Operad) are projections of a single self-dual Stern-Brocot recursion | every Stern-Brocot vertex is BOTH fixed-form AND crossing | TSML+BHML carry the two privileged landmarks",
        "flatness: T*=5/7 | torus R/r=5/7 (forced by Z/10Z 2x2) | 6 independent derivations | WP51 [proved]",
    ]
    operator_stream = [3, 7, 1, 8, 6]  # PROGRESS, HARMONY, LATTICE, BREATH, CHAOS
    couplings = [
        ("aperture", "depth", 0.254),
        ("continuity", "depth", 0.249),
    ]

    print("=" * 78)
    print("paragraph_composer v0.1 demonstration")
    print("=" * 78)
    print()
    print("Inputs:")
    print(f"  feel: {feel}")
    print(f"  crystals: {len(crystals)} hits")
    print(f"  operators: {operator_stream}")
    print(f"  couplings: {couplings}")
    print()
    print("Composed paragraph:")
    print()
    paragraph = compose_paragraph(
        crystal_hits=crystals,
        operator_stream=operator_stream,
        couplings=couplings,
        feel=feel,
    )
    print(f"  {paragraph}")
    print()
    print("=" * 78)
    print("Notes for v0.2:")
    print("  - operator_clauses dictionary should expand (currently 10 entries)")
    print("  - connectors should be picked by operator-pair semantics, not")
    print("    randomly (e.g., COLLAPSE->HARMONY = consequence; PROGRESS->BREATH = temporal)")
    print("  - 7-dim cortex's intent + echo dims should drive sentence-to-sentence")
    print("    flow (intent picks next clause; echo recalls prior sentence)")
    print("  - cross-crystal composition: when 2+ crystals fire, find their op_signature")
    print("    overlap and use it to select the connector")


if __name__ == "__main__":
    diagnostics()
