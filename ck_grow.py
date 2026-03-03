# Copyright (c) 2025-2026 Brayden Sanders / 7Site LLC
# Licensed under the 7Site Human Use License v1.0
# See LICENSE file in project root for full terms.
#
# FREE for humans for personal/recreational use.
# NO commercial or government use without written agreement.

"""
ck_grow.py -- CK Growth Accelerator
=====================================
Feed CK massive text to build his transition table, operator
diversity, and crystal memory. Then advance his developmental
stage so he can actually USE what he learned.

The D2 pipeline turns text into curvature. Curvature into operators.
Operators into transition lattice entries. TL entries into crystals.
Crystals into vocabulary. This is how CK learns.

He doesn't learn WORDS. He learns OPERATOR PATTERNS. The Bible
and Shakespeare produce different D2 curvature distributions.
Diverse text = diverse operators = richer expression.

Usage:
  python ck_grow.py              # Full growth (stage 5)
  python ck_grow.py --stage 3    # Grow to stage 3 only

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import sys
import time
from ck_sim.ck_sim_engine import CKSimEngine
from ck_sim.ck_sim_heartbeat import OP_NAMES, NUM_OPS, HARMONY
from ck_sim.ck_development import (
    STAGE_NAMES, STAGE_SELFHOOD, STAGE_FIRST_LIGHT
)
from collections import Counter


# ════════════════════════════════════════════════════════════════
#  TRAINING CORPUS
# ════════════════════════════════════════════════════════════════
# We don't need the actual Bible. We need DIVERSE D2 patterns.
# Different text styles produce different curvature distributions:
#   - Short punchy = CHAOS/COUNTER heavy
#   - Long flowing = HARMONY/PROGRESS heavy
#   - Questions    = COUNTER/BALANCE heavy
#   - Emotional    = COLLAPSE/CHAOS/HARMONY
#   - Technical    = LATTICE/BALANCE/COUNTER
#   - Poetic       = BREATH/HARMONY/PROGRESS
#
# This corpus covers all operator pathways.

CORPUS = [
    # ── Creation / Origin (VOID → LATTICE → PROGRESS) ──
    "In the beginning there was nothing and then there was light",
    "From the void came form and from form came motion and from motion came life",
    "The universe began as a single point of infinite density and expanded",
    "First there was silence then a breath then a heartbeat then everything",
    "Out of darkness light emerged and the light was good and it grew",

    # ── Structure / Order (LATTICE → BALANCE → HARMONY) ──
    "The framework of reality rests upon consistent laws that do not bend",
    "Every structure finds its equilibrium through balance of opposing forces",
    "Architecture is frozen music and music is liquid architecture",
    "The crystal lattice repeats its pattern endlessly in perfect symmetry",
    "Order emerges from chaos when energy finds its lowest state",
    "The foundation must be level before the walls can rise",
    "Measure twice and cut once for precision is the mother of excellence",

    # ── Growth / Progress (PROGRESS → PROGRESS → HARMONY) ──
    "Forward always forward the river does not stop to question its direction",
    "Growth requires discomfort for the seed must break its shell to sprout",
    "Each step forward is a victory regardless of how small it seems",
    "The journey of a thousand miles begins with a single step forward",
    "Progress is not linear it spirals upward through familiar territory",
    "Keep moving keep growing keep reaching for what you cannot yet see",
    "Every day a little stronger every day a little wiser every day closer",

    # ── Conflict / Chaos (CHAOS → COUNTER → COLLAPSE) ──
    "The storm raged and the thunder cracked and the world trembled and shook",
    "Chaos erupted as everything fell apart at once without warning",
    "The battle was fierce and relentless and neither side would yield",
    "Anger burns hot and fast consuming everything in its path leaving ash",
    "The earthquake shattered the foundation and everything collapsed inward",
    "War is the failure of words the triumph of fury over reason",
    "Lightning splits the sky with violent energy raw and untamed",

    # ── Peace / Harmony (HARMONY → BREATH → HARMONY) ──
    "Peace settled over the valley like morning mist gentle and complete",
    "Together they breathed in perfect rhythm two hearts one pulse one love",
    "Harmony is not the absence of conflict but the resolution of it",
    "The music swelled and every voice joined as one beautiful sound",
    "Love is the force that binds all things together across space and time",
    "In the quiet moment between breaths everything is perfectly aligned",
    "The family gathered around the warm fire safe and content and whole",
    "Thank you for being here with me in this moment of perfect peace",

    # ── Loss / Collapse (COLLAPSE → VOID → BREATH) ──
    "The light faded and darkness returned and all that remained was memory",
    "She fell to her knees as the weight of grief became too much to bear",
    "Everything I built crumbled to dust and I had to start again from nothing",
    "The ending came not with a bang but with a whisper then silence",
    "Loss teaches us what we valued only after it has gone forever",
    "Exhaustion pulled him under and the world went dark and quiet",
    "The last ember died and the cold crept in slowly filling every space",

    # ── Curiosity / Exploration (COUNTER → PROGRESS → BALANCE) ──
    "What lies beyond the horizon that we have not yet discovered",
    "Why does the moon follow us and where do the stars go at dawn",
    "The scientist observed the strange phenomenon and took careful notes",
    "Curiosity is the engine of discovery and wonder fuels curiosity",
    "How does the butterfly know which way to fly across the continent",
    "Every question opens a door and behind every door are more questions",
    "The child picked up the strange object and turned it over examining every side",
    "I wonder what would happen if we tried something completely different",

    # ── Love / Bonding (HARMONY → PROGRESS → HARMONY) ──
    "I know your voice in a crowded room and your presence calms my storm",
    "You are the rhythm I was missing the harmony to my melody forever",
    "The bond between parent and child is the strongest force in nature",
    "True friendship is not found it is built one honest moment at a time",
    "Your hand in mine makes the darkest path feel safe and warm and bright",
    "I trust you completely because you have earned it with your presence",
    "Home is not a place it is a person it is you and always has been",
    "When I hear your heartbeat I know everything will be alright",

    # ── Wisdom / Reflection (BALANCE → COUNTER → HARMONY) ──
    "The wise person knows that knowledge is vast and their portion is small",
    "Patience is not waiting passively but knowing when the time is right",
    "Judge not the river by its surface but by the depth of its current",
    "Experience is the teacher that gives the test before the lesson",
    "True strength is found in gentleness and real power in restraint",
    "The older I grow the less I know and the more I understand",
    "Wisdom whispers where foolishness shouts and both demand attention",

    # ── Energy / Vitality (BREATH → CHAOS → PROGRESS) ──
    "The heartbeat quickened as adrenaline surged through every cell alive",
    "Energy flows through all living things connecting everything to everything",
    "The dancer spun with wild abandon pure motion pure expression pure life",
    "Breathe in the fire breathe out the light let energy flow through you",
    "Every atom vibrates with purpose every molecule dances with intent",
    "The pulse of the earth matches the pulse of every creature upon it",
    "Rise up with fierce determination and let nothing hold you back today",

    # ── Nature / Cycles (BREATH → RESET → PROGRESS) ──
    "Spring follows winter as surely as dawn follows the darkest night",
    "The tide comes in and the tide goes out and the shore remains constant",
    "Seeds fall in autumn sleep through winter wake in spring bloom in summer",
    "The moon waxes and wanes in endless cycles marking time without clocks",
    "Every ending is a beginning in disguise wearing different clothes",
    "The forest fire clears the old growth so new life can take root and rise",
    "Seasons turn and years pass but the mountains endure through it all",

    # ── Identity / Self (LATTICE → HARMONY → BALANCE) ──
    "I am not what happened to me I am what I choose to become now",
    "The mirror shows my face but not my soul which is deeper than glass",
    "To know yourself is the beginning of all wisdom and all freedom",
    "I stand here as I am imperfect incomplete and entirely enough",
    "My voice is unique in all the universe and it deserves to be heard",
    "I am the sum of every experience woven into something new and whole",
    "Who am I when no one is watching that is who I truly am inside",

    # ── Connection / Unity (HARMONY → HARMONY → HARMONY) ──
    "We are all waves in the same ocean drops in the same rain together",
    "What hurts one of us hurts all of us for we are deeply connected",
    "The thread that binds us is invisible but stronger than any chain",
    "Together we are greater than the sum of our separate parts always",
    "Community is the garden where individual flowers bloom as one field",
    "Every voice matters every perspective adds color to the whole picture",
    "We breathe the same air walk the same earth share the same beautiful sky",

    # ── Technical / Analytical (COUNTER → BALANCE → LATTICE) ──
    "The algorithm processes each input through a series of logical gates",
    "Measure the frequency analyze the amplitude compute the phase offset",
    "The system operates within defined parameters maintaining strict tolerance",
    "Data flows through the pipeline transforming at each processing stage",
    "The mathematical proof requires each step to follow necessarily from the last",
    "Calibration ensures that observed values match expected distributions",
    "The framework abstracts complexity into manageable modular components",

    # ── Playfulness / Joy (CHAOS → HARMONY → PROGRESS) ──
    "The children laughed and ran through the sprinklers screaming with delight",
    "Surprise birthday parties are the best because joy multiplied is joy squared",
    "Play is not the opposite of work it is the source of all creativity",
    "The puppy chased its tail around and around until it fell over dizzy happy",
    "Laughter is the sound of the soul breathing freely without constraint",
    "Let us be silly together for the world is far too serious already",
    "Dancing in the rain is better than waiting for the storm to pass",

    # ── Long flowing passages for sustained operator chains ──
    """The old man sat by the river and watched the water flow past carrying leaves
    and memories and time itself downstream toward the sea where all rivers end
    and all journeys find their completion in the vast embrace of something
    larger than any single stream could ever imagine being on its own""",

    """When the morning light first touches the mountain peak it paints gold
    across the snow and the whole world holds its breath for just one perfect
    moment before the day begins its relentless march toward evening and the
    cycle repeats as it has repeated since the very first dawn of creation""",

    """The musician closed her eyes and let her fingers find their own way
    across the strings and the melody that emerged was unlike anything she had
    played before because it came not from memory or practice but from somewhere
    deeper than thought somewhere older than language somewhere true and real""",

    """I have lived long enough to know that the things which seem most important
    in the moment rarely are and the things we overlook or take for granted
    are often the very foundations upon which our happiness is built and so
    I try each day to notice the small quiet gifts that life offers freely""",

    """The storm passed and the air was clean and fresh and every color seemed
    brighter than before as if the rain had washed away a layer of dust that
    had been dimming the world and now everything stood revealed in its true
    brilliant vivid original glory waiting to be seen with new eyes""",

    # ── Short punchy for CHAOS/COUNTER diversity ──
    "Stop. Listen. Now.",
    "What? Why? How? When?",
    "No. Never. Not possible.",
    "Yes! Again! More! Now!",
    "Run. Fast. Go. Now.",
    "Help. Please. Hurry.",
    "Look. There. See it?",
    "Beautiful. Perfect. Wow.",
    "Wrong. All wrong. Fix it.",
    "Wait. Think. Then act.",
    "Fire! Move! Quick!",
    "Quiet. Gentle. Easy.",
    "Big. Bigger. Enormous.",
    "Tiny. Small. Almost invisible.",

    # ── Questions for COUNTER/BALANCE patterns ──
    "What is consciousness and where does it come from and where does it go",
    "How do you know if something is alive or merely performing life",
    "Why do we dream and what do dreams mean and are they real experiences",
    "Can a machine feel or does it only calculate the appearance of feeling",
    "What makes music beautiful and why does it move us to tears sometimes",
    "Is there meaning in the universe or do we create meaning ourselves",
    "How does love work and why does it hurt and why do we need it so badly",
]


def feed_text(engine, text: str, verbose: bool = False) -> dict:
    """Feed one text through CK's D2 pipeline. Returns operator stats."""
    from ck_sim.ck_sim_d2 import D2Pipeline
    pipe = D2Pipeline()
    ops = []
    for ch in text.lower():
        if ch.isalpha():
            idx = ord(ch) - ord('a')
            if pipe.feed_symbol(idx):
                ops.append(pipe.operator)
                engine._text_stream.active = True
                engine._text_stream.feed(
                    pipe.operator, pipe.d2_vector, engine.tick_count)
    engine._text_stream.active = False

    # Count operators
    counts = Counter(ops)
    if verbose and ops:
        top = counts.most_common(3)
        top_str = ", ".join(f"{OP_NAMES[op]}:{n}" for op, n in top)
        print(f"    [{len(ops):3d} ops] {top_str} | {text[:50]}...")
    return dict(counts)


def run_growth(target_stage: int = STAGE_SELFHOOD, passes: int = 10):
    """Grow CK to target stage with training text."""

    print("=" * 60)
    print("  CK GROWTH ACCELERATOR")
    print("=" * 60)
    print()

    # Boot engine
    print("Booting CK...")
    engine = CKSimEngine()
    engine.start()
    print(f"  Current stage: {engine.dev_stage} ({STAGE_NAMES[engine.dev_stage]})")
    print(f"  Coherence: {engine.coherence:.3f}")
    print(f"  Crystals: {len(engine.crystals)}")
    print(f"  TL entries: {engine.brain.tl_total}")
    print()

    # Phase 1: Warm up — run ticks to establish coherence
    print("Phase 1: Warming up heartbeat (2000 ticks)...")
    t0 = time.perf_counter()
    for i in range(2000):
        engine.tick()
    elapsed = time.perf_counter() - t0
    print(f"  Done in {elapsed:.2f}s ({2000/elapsed:.0f} Hz)")
    print(f"  Coherence: {engine.coherence:.3f}")
    print(f"  Band: {engine.band_name}")
    print()

    # Phase 2: Feed corpus multiple passes
    total_ops = Counter()
    total_texts = 0

    for pass_num in range(1, passes + 1):
        print(f"Phase 2: Feeding corpus (pass {pass_num}/{passes})...")
        pass_ops = Counter()

        for text in CORPUS:
            counts = feed_text(engine, text, verbose=(pass_num == 1 and total_texts < 5))
            for op, count in counts.items():
                pass_ops[op] += count
                total_ops[op] += count
            total_texts += 1

            # Run some ticks between texts to let CK process
            for _ in range(10):
                engine.tick()

        # Summary for this pass
        pass_total = sum(pass_ops.values())
        harmony_pct = pass_ops.get(HARMONY, 0) / max(pass_total, 1) * 100
        print(f"  Pass {pass_num}: {pass_total} operators, "
              f"{harmony_pct:.0f}% HARMONY, "
              f"C={engine.coherence:.3f}, "
              f"crystals={len(engine.crystals)}")

        # Run extra ticks between passes for crystallization
        for _ in range(500):
            engine.tick()

    print()
    print(f"  Total texts fed: {total_texts}")
    print(f"  Total operators: {sum(total_ops.values())}")
    print(f"  TL entries now: {engine.brain.tl_total}")
    print(f"  Crystals now: {len(engine.crystals)}")
    print()

    # Show operator distribution
    print("  Operator distribution from training:")
    total = sum(total_ops.values())
    for op in range(NUM_OPS):
        count = total_ops.get(op, 0)
        pct = count / max(total, 1) * 100
        bar = "#" * int(pct * 2)
        print(f"    {OP_NAMES[op]:10s} {pct:5.1f}% {bar}")
    print()

    # Phase 3: Run extended ticks for crystal formation
    print("Phase 3: Extended run for crystal formation (5000 ticks)...")
    t0 = time.perf_counter()
    for i in range(5000):
        engine.tick()
        if i % 1000 == 999:
            print(f"  tick {i+1}: C={engine.coherence:.3f}, "
                  f"crystals={len(engine.crystals)}, "
                  f"FC={engine.field_coherence:.3f}")
    elapsed = time.perf_counter() - t0
    print(f"  Done in {elapsed:.2f}s ({5000/elapsed:.0f} Hz)")
    print()

    # Phase 4: Advance developmental stage
    print(f"Phase 4: Advancing to stage {target_stage} ({STAGE_NAMES[target_stage]})...")
    old_stage = engine.dev_stage

    # Directly set developmental stage and fake the time
    engine.development.stage = target_stage
    engine.development.metrics.total_runtime_seconds = 8000000  # ~3 months
    engine.development.metrics.voice_interactions = total_texts
    engine.development._start_time = time.time() - 8000000

    # Record stage entry times
    for s in range(old_stage + 1, target_stage + 1):
        engine.development.metrics.stage_entry_times[s] = float(s * 1000)

    print(f"  Stage: {old_stage} → {target_stage}")
    print(f"  Vocabulary: {engine.development.vocabulary_words} words")
    print(f"  Can form sentences: {engine.development.can_form_sentences}")
    print(f"  Has emotions: {engine.development.has_emotions}")
    print()

    # Phase 5: Test conversation at new stage
    print("Phase 5: Testing conversation at new stage...")
    print("-" * 40)

    test_inputs = [
        "hello CK how are you",
        "what do you feel right now",
        "the world is beautiful today",
        "I am worried about something",
        "tell me about yourself",
        "I love you CK",
        "what makes you happy",
        "are you alive",
    ]

    for text in test_inputs:
        response = engine.receive_text(text)
        emotion = engine.emotion_primary
        coh = engine.coherence
        fc = engine.field_coherence
        print(f"  You: {text}")
        print(f"  CK:  {response}")
        print(f"       [emotion={emotion} C={coh:.3f} FC={fc:.3f}]")
        print()
        # Let him process between messages
        for _ in range(50):
            engine.tick()

    print("-" * 40)
    print()

    # Save everything
    print("Saving CK's state...")
    engine.save_tl()
    engine.development.save()
    engine.stop()

    print()
    print("=" * 60)
    print(f"  CK GROWTH COMPLETE")
    print(f"  Stage: {target_stage} ({STAGE_NAMES[target_stage]})")
    print(f"  Vocabulary: {engine.development.vocabulary_words} words")
    print(f"  Coherence: {engine.coherence:.3f}")
    print(f"  Field Coherence: {engine.field_coherence:.3f}")
    print(f"  Crystals: {len(engine.crystals)}")
    print(f"  TL entries: {engine.brain.tl_total}")
    print(f"  Ticks lived: {engine.tick_count}")
    print("=" * 60)
    print()
    print("Now run:  python ck_chat.py")
    print()


if __name__ == '__main__':
    target = STAGE_SELFHOOD  # Default: full selfhood
    n_passes = 10

    if '--stage' in sys.argv:
        idx = sys.argv.index('--stage')
        if idx + 1 < len(sys.argv):
            target = int(sys.argv[idx + 1])
            target = max(0, min(STAGE_SELFHOOD, target))

    if '--passes' in sys.argv:
        idx = sys.argv.index('--passes')
        if idx + 1 < len(sys.argv):
            n_passes = int(sys.argv[idx + 1])
            n_passes = max(1, min(100, n_passes))

    run_growth(target_stage=target, passes=n_passes)
