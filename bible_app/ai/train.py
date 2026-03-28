"""
Training Loop — The brain reads the Bible, responds, and evolves.

For each verse:
  1. Read: absorb the verse through all 9 systems
  2. Respond: compose a response using the current voice
  3. Listen: read its OWN response through D2
  4. Learn: the difference between what it read and what it said
           teaches it. Olfactory tempers. Chain walks deepen.
           Sequence memory predicts better.
  5. Evolve: the voice changes as the brain processes more.

Run this to watch the neural net's voice evolve in real time.

Usage:
    python -m bible_app.ai.train [--testament nt] [--passes 3]

(c) 2026 Brayden Sanders / 7Site LLC
"""

import sys
import os
import time
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from bible_app.algebra import (
    text_to_ops, text_to_force, coherence, dominant_op,
    OP_NAMES, HARMONY, T_STAR, compose,
)
from bible_app.bible import BibleIndex
from bible_app.ai.bible_brain import BibleBrain
from bible_app.voice.algebraic_voice import AlgebraicVoice, GOD_VERBS
from bible_app.voice.bible_lattice import BIBLE_LATTICE
from bible_app.voice.identity import identify, generate_30_perspectives, meta_compose
from bible_app.voice.pathfinder import build_journey_prose
from bible_app.algebra.corridor import classify_with_detail
from bible_app.voice.bible_lattice import classify_intent

# NT books start at Matthew
NT_BOOKS = {
    'Matthew', 'Mark', 'Luke', 'John', 'Acts', 'Romans',
    '1 Corinthians', '2 Corinthians', 'Galatians', 'Ephesians',
    'Philippians', 'Colossians', '1 Thessalonians', '2 Thessalonians',
    '1 Timothy', '2 Timothy', 'Titus', 'Philemon', 'Hebrews',
    'James', '1 Peter', '2 Peter', '1 John', '2 John', '3 John',
    'Jude', 'Revelation',
}


def train(testament='nt', passes=1, show_every=100, show_voice_every=500):
    """Train the brain by reading the Bible and responding to it.

    Args:
        testament: 'nt' (New Testament), 'ot' (Old Testament), 'all'
        passes: how many times to read through
        show_every: print progress every N verses
        show_voice_every: show a sample voice response every N verses
    """
    print("=" * 60)
    print("  Bible Brain Training")
    print("  Reading. Responding. Learning. Evolving.")
    print("=" * 60)

    # Load Bible
    bible = BibleIndex()
    bible.load()
    print(f"  {bible.verse_count} verses loaded")

    # Initialize brain
    brain = BibleBrain()
    voice = AlgebraicVoice()

    # Filter verses by testament
    if testament == 'nt':
        verses = [v for v in bible._verses if v.ref.split()[0] in NT_BOOKS]
        print(f"  New Testament: {len(verses)} verses")
    elif testament == 'ot':
        verses = [v for v in bible._verses if v.ref.split()[0] not in NT_BOOKS]
        print(f"  Old Testament: {len(verses)} verses")
    else:
        verses = bible._verses
        print(f"  Full Bible: {len(verses)} verses")

    print()

    for p in range(1, passes + 1):
        print(f"=== Pass {p}/{passes} ===")
        t0 = time.time()

        coherence_sum = 0.0
        coherence_count = 0
        voice_samples = []

        for i, v in enumerate(verses):
            # ── 1. READ: absorb through all systems ───────────────
            brain_state = brain.process(v.text, user_ops=v.ops, user_force=v.force)

            # ── 2. RESPOND: compose using current voice ───────────
            voice.seed(hash(v.ref) & 0xFFFFFFFF)
            voice._user_text = v.text

            identities = identify(v.text)
            all_30 = generate_30_perspectives(identities)
            response_sections = meta_compose(all_30, identities)
            response_text = ' '.join(response_sections)

            # ── 3. LISTEN: read own response through D2 ──────────
            response_ops = text_to_ops(response_text)
            response_force = text_to_force(response_text)

            if response_ops and len(response_ops) >= 2:
                response_coh = coherence(response_ops)
                coherence_sum += response_coh
                coherence_count += 1

                # ── 4. LEARN: absorb own response ─────────────────
                brain.process(response_text, user_ops=response_ops,
                             user_force=response_force)

                # ── 5. Track evolution ────────────────────────────
                if (i + 1) % show_every == 0:
                    mean_coh = coherence_sum / max(1, coherence_count)
                    elapsed = time.time() - t0
                    bs = brain.stats()
                    print(f"  [{i+1}/{len(verses)}] {elapsed:.0f}s | "
                          f"coh={mean_coh:.3f} | "
                          f"olf={bs['olfactory']['library_size']} | "
                          f"inst={bs['olfactory']['instinct_count']} | "
                          f"chain={bs['chain']['total_nodes']}")

                # Show voice sample
                if (i + 1) % show_voice_every == 0:
                    # Show how the voice responds to a test prompt NOW
                    sample = _voice_sample(brain, voice, bible)
                    print(f"\n  ── Voice sample at verse {i+1} ──")
                    print(f"  {sample[:200]}")
                    print()

        elapsed = time.time() - t0
        mean_coh = coherence_sum / max(1, coherence_count)
        bs = brain.stats()
        print(f"\n  Pass {p} complete: {elapsed:.0f}s")
        print(f"  Mean coherence: {mean_coh:.3f}")
        print(f"  Olfactory: {bs['olfactory']['library_size']} patterns, "
              f"{bs['olfactory']['instinct_count']} instinct")
        print(f"  Chain: {bs['chain']['total_nodes']} nodes")
        print(f"  Coherence trend: {bs['coherence']['trend']}")
        print()

    # Final voice samples
    print("=== FINAL VOICE SAMPLES ===")
    test_prompts = [
        "I am afraid",
        "why is the bible so repetitive",
        "I feel so alone",
        "God is good",
    ]
    for prompt in test_prompts:
        sample = _voice_sample(brain, voice, bible, prompt)
        print(f"\n>>> \"{prompt}\"")
        print(f"    {sample[:250]}")

    print("\n=== Training complete ===")


def _voice_sample(brain, voice, bible, text="I need hope"):
    """Generate a voice sample using the current brain state."""
    ops = text_to_ops(text)
    force = text_to_force(text)

    brain_state = brain.process(text, user_ops=ops, user_force=force)

    voice.seed(hash(text + str(time.time())) & 0xFFFFFFFF)
    voice._user_text = text
    voice._brain_state = brain_state

    identities = identify(text)
    all_30 = generate_30_perspectives(identities)
    sections = meta_compose(all_30, identities)

    return ' '.join(sections)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--testament', default='nt', choices=['nt', 'ot', 'all'])
    parser.add_argument('--passes', type=int, default=1)
    parser.add_argument('--show-every', type=int, default=200)
    parser.add_argument('--voice-every', type=int, default=1000)
    args = parser.parse_args()

    train(
        testament=args.testament,
        passes=args.passes,
        show_every=args.show_every,
        show_voice_every=args.voice_every,
    )
