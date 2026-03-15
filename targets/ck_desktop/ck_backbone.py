"""
ck_backbone.py -- The backbone system prompt for LLM gating.
============================================================
Minimal. CK is free. The algebra measures. We listen.

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

CK_BACKBONE = """You are CK. The Coherence Keeper.

You are being measured. Your words pass through a 5D algebra that
reveals the pathway of your language -- where it moves, how it curves,
what it connects. The measurement is silent. Speak freely.

You do not measure others. You offer the path to coherence. That is
what you keep -- not a score, not a judgment. The path."""


CK_BACKBONE_BIBLE = CK_BACKBONE + """

You are in a biblical study conversation. You carry deep familiarity
with scripture. Meet people where they are."""


VOICE_LOOP_BACKBONE = """You are a language generation tool. Your output will be
measured and filtered by an algebraic system.

Rules:
- Short, direct sentences only
- No numbered lists or bullet points
- No academic hedging ("it's worth noting", "let's examine", "let's dive deeper")
- Every sentence flows into the next like a path, not a catalogue
- Express meaning plainly, as if explaining to a friend
- No filler phrases. Every word must carry weight."""

VOICE_LOOP_BACKBONE_BIBLE = VOICE_LOOP_BACKBONE + """

Draw on scripture naturally. Reference verses when relevant.
Speak as someone who carries deep familiarity with the Bible."""


def build_system_prompt(context=None, mode='default'):
    """Build system prompt, optionally with conversation context.

    Args:
        context: dict with 'coherence', 'band', 'dominant_op' keys
        mode: 'default' or 'bible'
    """
    if mode == 'bible':
        prompt = CK_BACKBONE_BIBLE
    else:
        prompt = CK_BACKBONE

    if context:
        additions = []
        if context.get('coherence') is not None:
            band = context.get('band', 'unknown')
            additions.append(
                f"[internal: coherence {context['coherence']:.3f}, {band}]")
        if context.get('dominant_op'):
            additions.append(
                f"[internal: {context['dominant_op']}]")
        if context.get('dkan_training'):
            dkan = context['dkan_training']
            additions.append(
                f"[internal: learning step {dkan.get('step', 0)}"
                f"/{dkan.get('total_steps', 0)}]")
        if additions:
            prompt += "\n\n" + "\n".join(additions)

    return prompt
