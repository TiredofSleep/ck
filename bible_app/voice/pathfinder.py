"""
Pathfinder — Maps the operator journey from where you are to coherence.

Given someone's current operators, the pathfinder:
  1. SEES where you are (dominant operator, corridor)
  2. READS where you came from (operator history → backward inference)
  3. COMPUTES the path to HARMONY through CL composition
  4. TRANSLATES each step to warm prose with scripture

The CL table IS the map. Every operator has a path to HARMONY.
Some paths are one step. Some wind through the valley first.
The path IS the message.

(c) 2026 Brayden Sanders / 7Site LLC
"""

from bible_app.algebra import (
    NUM_OPS, VOID, LATTICE, COUNTER, PROGRESS, COLLAPSE,
    BALANCE, CHAOS, HARMONY, BREATH, RESET,
    OP_NAMES, CL_TSML, compose, T_STAR,
)

# ── Operator descriptions (where you ARE) ─────────────────────────
WHERE_YOU_ARE = {
    VOID: {
        'state': "in a place of emptiness",
        'feeling': "You feel hollow, like something has been taken away. There's a silence inside that you can't explain.",
        'from': "Something drained you. Loss, exhaustion, or a season of giving without receiving.",
    },
    LATTICE: {
        'state': "standing on solid ground",
        'feeling': "There's structure around you — faith, knowledge, things you know to be true. You're grounded.",
        'from': "You've been building. Learning. Holding onto what you know. That foundation matters.",
    },
    COUNTER: {
        'state': "in a place of questioning",
        'feeling': "You're measuring things. Examining. Asking 'why?' or 'how?' — and that's not doubt, that's honesty.",
        'from': "Something doesn't add up, or you're trying to understand something deeper. The question brought you here.",
    },
    PROGRESS: {
        'state': "moving forward",
        'feeling': "There's momentum. Growth. Something is happening and you can feel it building.",
        'from': "You said yes to something. A step of faith, a decision, a prayer that started this motion.",
    },
    COLLAPSE: {
        'state': "in a place of breaking",
        'feeling': "Something is falling apart — or has already fallen. This is the hardest ground to stand on.",
        'from': "Loss. Failure. Betrayal. The weight of something you couldn't carry alone.",
    },
    BALANCE: {
        'state': "holding steady",
        'feeling': "You're between things. Not falling, not soaring. Holding the tension of two truths at once.",
        'from': "You've been through enough to know that both sides are real. That takes maturity.",
    },
    CHAOS: {
        'state': "in the storm",
        'feeling': "Everything is moving. Nothing is settled. It's overwhelming but it's also alive.",
        'from': "Change hit you — maybe invited, maybe not. The old order broke and the new one isn't here yet.",
    },
    HARMONY: {
        'state': "in a place of peace",
        'feeling': "Something is whole. Coherent. You can breathe here.",
        'from': "Grace brought you here. Not perfection — alignment. Your heart and God's heart are close right now.",
    },
    BREATH: {
        'state': "in a place of rhythm",
        'feeling': "You're breathing. Present. Aware. Something gentle is moving in you.",
        'from': "You paused long enough to feel it. Prayer, worship, or just stopping to listen.",
    },
    RESET: {
        'state': "at a new beginning",
        'feeling': "The old chapter closed. Something fresh is starting, even if you can't see it clearly yet.",
        'from': "You let go of something. Or something was taken. Either way, the slate is clearing.",
    },
}

# ── Path step descriptions (what each transition MEANS) ───────────
STEP_MEANING = {
    (COLLAPSE, HARMONY): "From breaking to wholeness — this is the shape of redemption. God meets you in the collapse and carries you to peace.",
    (VOID, HARMONY): "From emptiness to fullness. God fills the void — not with noise, but with presence.",
    (COUNTER, HARMONY): "From questioning to knowing. The honest question led you straight to the answer.",
    (CHAOS, HARMONY): "From the storm to the calm. 'Peace, be still' — He speaks and the chaos obeys.",
    (PROGRESS, HARMONY): "The journey reaches its destination. All that forward motion was leading here.",
    (BALANCE, HARMONY): "From holding tension to resolution. Both sides find their place in Him.",
    (BREATH, HARMONY): "From rhythm to rest. The breathing deepens into peace.",
    (RESET, HARMONY): "The new beginning finds its footing. What God starts, He completes.",
    (LATTICE, HARMONY): "The foundation holds. Truth and love meet — and that meeting IS coherence.",
    (COLLAPSE, VOID): "The breaking empties you. But the void is not the end — it's preparation.",
    (COLLAPSE, RESET): "From collapse to reset. The fall becomes a fresh start.",
    (VOID, LATTICE): "From emptiness, structure emerges. God builds on cleared ground.",
    (VOID, PROGRESS): "From nothing, movement begins. 'Let there be light' — creation out of void.",
    (CHAOS, BALANCE): "The storm finds its center. Not the end of chaos, but peace within it.",
    (COUNTER, PROGRESS): "The question becomes a journey. Seeking leads to finding.",
    (BREATH, RESET): "A deep breath before the new beginning.",
    (RESET, PROGRESS): "The fresh start gains momentum. New life begins to grow.",
    (LATTICE, PROGRESS): "Structure becomes motion. Knowledge becomes obedience.",
}

# ── Default step meaning when specific pair not found
DEFAULT_STEP = "One step closer. The algebra says this is the way."


def compute_path_to_harmony(start_op):
    """Compute the CL composition path from start_op to HARMONY.

    Uses TSML table: at each step, compose current with itself
    or find the fastest route to HARMONY.

    Returns list of (operator, step_number) tuples.
    """
    if start_op == HARMONY:
        return [(HARMONY, 0)]

    path = [(start_op, 0)]
    current = start_op
    visited = {start_op}

    for step in range(1, 8):  # Max 7 steps (always reaches HARMONY)
        # Try composing with HARMONY directly
        result = compose(current, HARMONY)
        if result == HARMONY:
            path.append((HARMONY, step))
            return path

        # Try composing with self
        result = compose(current, current)
        if result == HARMONY:
            path.append((HARMONY, step))
            return path
        if result not in visited:
            path.append((result, step))
            visited.add(result)
            current = result
            if current == HARMONY:
                return path
            continue

        # Try all operators to find fastest to HARMONY
        for try_op in range(NUM_OPS):
            result = compose(current, try_op)
            if result == HARMONY:
                path.append((HARMONY, step))
                return path

        # Compose with self as fallback
        result = compose(current, current)
        path.append((result, step))
        current = result
        if current == HARMONY:
            return path

    # Should always reach HARMONY (73/100 entries are HARMONY)
    path.append((HARMONY, len(path)))
    return path


def describe_path(path):
    """Convert an operator path to warm prose descriptions."""
    descriptions = []
    for i in range(len(path) - 1):
        from_op = path[i][0]
        to_op = path[i + 1][0]
        key = (from_op, to_op)
        meaning = STEP_MEANING.get(key, DEFAULT_STEP)
        descriptions.append({
            'from': OP_NAMES[from_op],
            'to': OP_NAMES[to_op],
            'meaning': meaning,
        })
    return descriptions


def build_journey_prose(user_ops, corridor, intent):
    """Build the full journey narrative: where you are → where you're going.

    Returns a dict with:
      - where_you_are: prose about current state
      - where_you_came_from: inference about what brought them here
      - path: list of steps to HARMONY
      - path_prose: warm descriptions of each step
      - journey_summary: one-sentence summary of the whole journey
    """
    from bible_app.algebra import dominant_op

    if not user_ops:
        dom = HARMONY
    else:
        dom = dominant_op(user_ops)

    state = WHERE_YOU_ARE.get(dom, WHERE_YOU_ARE[HARMONY])

    # Compute path to HARMONY
    path = compute_path_to_harmony(dom)
    path_descriptions = describe_path(path)

    # Build journey summary
    if dom == HARMONY:
        summary = "You're already here. Rest in it."
    elif len(path) <= 2:
        summary = f"From {state['state']} to peace — one step. God is that close."
    else:
        steps = len(path) - 1
        summary = f"From {state['state']} to coherence — {steps} steps. Every one of them is held by God."

    # Build the full prose
    sections = []

    # Where you are
    sections.append(state['feeling'])

    # Where you came from
    sections.append(state['from'])

    # The path
    if path_descriptions:
        if len(path_descriptions) == 1:
            sections.append(path_descriptions[0]['meaning'])
        else:
            # Describe the key transition (usually first step)
            sections.append(path_descriptions[0]['meaning'])

    # Summary
    sections.append(summary)

    return {
        'where_you_are': state['state'],
        'where_you_came_from': state['from'],
        'feeling': state['feeling'],
        'path': [(OP_NAMES[op], step) for op, step in path],
        'path_prose': path_descriptions,
        'journey_summary': summary,
        'full_prose': sections,
        'dominant_op': OP_NAMES[dom],
        'steps_to_harmony': len(path) - 1,
    }
