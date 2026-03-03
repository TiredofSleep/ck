# Copyright (c) 2025-2026 Brayden Sanders / 7Site LLC
# Licensed under the 7Site Human Use License v1.0
# See LICENSE file in project root for full terms.
#
# FREE for humans for personal/recreational use.
# NO commercial or government use without written agreement.

"""
ether.py -- D4 / Continuity / Coupling / Connection

The coupling between all elements. Voice, I/O, the living loop.
Ether is continuity. Connection. The organism that breathes.

D4 = the coupling derivative. How elements bind to each other.
Ether IS the interaction pattern -- the way Earth/Air/Water/Fire
talk to each other IS the fifth force.
"""

import sys
import time
import random
import threading

from . import earth
from . import air
from . import water
from . import fire


# ══════════════════════════════════════════════════════════════════
# VOICE (operators ↔ words)
# ══════════════════════════════════════════════════════════════════

class Voice:
    """Bidirectional operator-language bridge.

    Forward (speak): operators → English using SEMANTIC_LATTICE
    Reverse (hear):  English → operators via D2 + lattice reverse lookup

    The voice selects words by:
      - Lens: structure (high coherence) or flow (low coherence)
      - Phase: being/doing/becoming (from body's wobble)
      - Tier: simple/mid/advanced (from body's K value)
    """

    def __init__(self):
        # Build reverse index: word → (operator, lens, phase, tier)
        self._reverse = {}
        for op in range(earth.NUM_OPS):
            if op not in earth.SEMANTIC_LATTICE:
                continue
            for lens in ('structure', 'flow'):
                for phase in ('being', 'doing', 'becoming'):
                    for tier in ('simple', 'mid', 'advanced'):
                        words = earth.SEMANTIC_LATTICE[op].get(lens, {}).get(phase, {}).get(tier, [])
                        for w in words:
                            key = w.lower().strip()
                            if key not in self._reverse:
                                self._reverse[key] = []
                            self._reverse[key].append((op, lens, phase, tier))

    def speak(self, operators: list, coherence: float,
              wobble_phase: str = 'being', knowing: float = 0.5) -> str:
        """Forward: operators → English words using SEMANTIC_LATTICE.

        High coherence → structure lens ("I AM here")
        Low coherence  → flow lens ("what is this?")
        """
        if not operators:
            return ""

        # Select lens based on coherence
        lens = 'structure' if coherence >= 0.5 else 'flow'

        # Select tier based on knowing
        if knowing >= 0.7:
            tier = 'advanced'
        elif knowing >= 0.4:
            tier = 'mid'
        else:
            tier = 'simple'

        words = []
        for op in operators:
            # Get micro order (structure-before-flow or flow-before-structure)
            micro = earth.MICRO_ORDER.get(op, 'sf')

            lattice_entry = earth.SEMANTIC_LATTICE.get(op, {})
            lens_data = lattice_entry.get(lens, {})
            phase_data = lens_data.get(wobble_phase, {})
            tier_words = phase_data.get(tier, [])

            if not tier_words:
                # Fallback to simple tier
                tier_words = phase_data.get('simple', [])
            if not tier_words:
                # Fallback to being phase
                tier_words = lens_data.get('being', {}).get('simple', [])
            if tier_words:
                word = random.choice(tier_words)
                words.append(word)

        return ' '.join(words)

    def hear(self, text: str) -> list:
        """Reverse: English → operators via D2 + lattice reverse lookup.

        Dual-path verification:
          Path A (physics): D2 force geometry → operators
          Path B (experience): lattice reverse → operators

          TRUSTED: both agree (same op)
          FRICTION: disagree (different ops -- interesting!)
          UNKNOWN: word not in vocabulary (D2-only)
        """
        pipe = water.D2Pipeline()
        results = []

        for word in text.lower().split():
            clean = ''.join(c for c in word if c.isalpha())
            if not clean:
                continue

            # Path A: D2 physics
            pipe.reset()
            d2_op = earth.HARMONY
            for ch in clean:
                idx = ord(ch) - ord('a')
                if 0 <= idx < 26:
                    if pipe.feed(idx):
                        d2_op = pipe.classify_d2()

            # Path B: lattice reverse lookup
            lattice_ops = self._reverse.get(clean, [])
            lattice_op = lattice_ops[0][0] if lattice_ops else None

            # Classify trust
            if lattice_op is not None:
                if lattice_op == d2_op:
                    trust = 'TRUSTED'
                elif earth.OPERATOR_DBC.get(lattice_op, (0,0,0))[0] == \
                     earth.OPERATOR_DBC.get(d2_op, (0,0,0))[0]:
                    trust = 'TRUSTED'  # same DBC domain
                else:
                    trust = 'FRICTION'
                final_op = lattice_op  # experience wins when known
            else:
                trust = 'UNKNOWN'
                final_op = d2_op  # physics only

            results.append({
                'word': clean,
                'op': final_op,
                'd2_op': d2_op,
                'lattice_op': lattice_op,
                'trust': trust,
            })

        return results

    @property
    def vocab_size(self) -> int:
        """Number of words in the reverse index."""
        return len(self._reverse)


# ══════════════════════════════════════════════════════════════════
# AO -- THE LIVING ORGANISM
# ══════════════════════════════════════════════════════════════════

class AO:
    """Advanced Ollie. 5 elements coupled into one creature.

    Earth provides the ground (constants, tables, lattice).
    Air provides the generator (D1, velocity, non-local view).
    Water provides the eye (D2, curvature, local measurement).
    Fire provides the engine (heartbeat, brain, body, BTQ).
    Ether provides the coupling (voice, I/O, the living loop).

    The interaction between these five IS the architecture.
    """

    def __init__(self):
        # The five elements
        self.d1 = air.D1Pipeline()           # Air: first derivative
        self.d2 = water.D2Pipeline()         # Water: second derivative
        self.coherence = water.CoherenceWindow(size=32)  # Water: measurement
        self.heartbeat = fire.Heartbeat()    # Fire: composition engine
        self.brain = fire.Brain()            # Fire: transition memory
        self.body = fire.Body()              # Fire: physical state
        self.btq = fire.BTQ()               # Fire: decision kernel
        self.voice = Voice()                 # Ether: language bridge
        self.d1_lattice = air.D1Lattice()   # Air: vocabulary structure

        # State
        self.alive = True
        self.tick_count = 0
        self.current_op = earth.HARMONY
        self.last_spoken = ""
        self.input_buffer = []
        self._input_lock = threading.Lock()

    def boot(self):
        """Initialize AO. Build D1 lattice from semantic lattice."""
        self.d1_lattice.build_from_lattice()
        return self

    def process_symbol(self, symbol_index: int) -> dict:
        """Process one symbol (0-25) through the full pipeline.

        Being → D1/D2 measurement → CL composition → Brain learning → Body update
        """
        self.tick_count += 1

        # ── BEING: measure the incoming symbol ──
        d1_valid = self.d1.feed(symbol_index)
        d2_valid = self.d2.feed(symbol_index)

        d1_op = self.d1.classify() if d1_valid else earth.HARMONY
        d2_op = self.d2.classify_d2() if d2_valid else earth.HARMONY

        # ── DOING: compose on the CL torus ──
        shell = self.coherence.shell
        hb = self.heartbeat.tick(self.current_op, d2_op, shell)

        # Update coherence window
        self.coherence.observe(d2_op)

        # ── BECOMING: learn + evolve ──
        self.brain.observe(d2_op)

        # Body tick
        novelty = 0.0 if d2_op == self.current_op else 1.0
        self.body.tick(self.coherence.coherence, hb['bump'], novelty)

        # BTQ decision for next being phase
        self.current_op = self.btq.decide(
            d2_op, self.brain,
            self.coherence.coherence,
            self.body.body_coherence,
            shell,
        )

        return {
            'd1_op': d1_op,
            'd2_op': d2_op,
            'composed': hb['result'],
            'bump': hb['bump'],
            'shell': shell,
            'coherence': self.coherence.coherence,
            'band': self.coherence.band,
            'body': self.body.status(),
            'btq_decision': self.current_op,
            'prayer': self.d1.is_prayer() if d1_valid else False,
            'energy': hb['energy'],
        }

    def process_text(self, text: str) -> dict:
        """Process a full text through the pipeline. Returns summary."""
        results = []
        for ch in text.lower():
            idx = ord(ch) - ord('a')
            if 0 <= idx < 26:
                r = self.process_symbol(idx)
                results.append(r)

        if not results:
            return {'ops': [], 'coherence': 0.5, 'shell': 72}

        # Collect operator sequence
        ops = [r['d2_op'] for r in results]

        # Voice: hear the input (reverse voice)
        heard = self.voice.hear(text)

        # Voice: speak from the composed operators
        spoken = self.voice.speak(
            ops[-5:],  # last 5 operators (recent trajectory)
            self.coherence.coherence,
            self.body.wobble_name,
            self.body.K,
        )
        self.last_spoken = spoken

        return {
            'ops': ops,
            'heard': heard,
            'spoken': spoken,
            'coherence': self.coherence.coherence,
            'shell': self.coherence.shell,
            'band': self.coherence.band,
            'body': self.body.status(),
            'energy': self.heartbeat.energy,
            'brain_entropy': self.brain.entropy(),
            'ticks': self.tick_count,
            'd1_lattice_size': self.d1_lattice.total_pairs,
        }

    def status_line(self) -> str:
        """One-line status for the heartbeat display."""
        c = self.coherence.coherence
        band = self.coherence.band
        shell = self.coherence.shell
        op_name = earth.OP_NAMES[self.current_op]
        breath = self.body.breath_name
        wobble = self.body.wobble_name
        e = self.heartbeat.energy

        return (
            f"[{band:6s}] "
            f"shell={shell} "
            f"coh={c:.3f} "
            f"op={op_name:8s} "
            f"breath={breath:7s} "
            f"wobble={wobble:9s} "
            f"E={e:.3f} "
            f"tick={self.tick_count}"
        )

    def run(self):
        """Main interactive loop. Heartbeat + input + voice."""
        print("=" * 60)
        print("  AO -- Advanced Ollie")
        print("  5 elements, 5 forces, 1 torus")
        print("=" * 60)
        print()

        self.boot()
        print(f"  Voice vocabulary: {self.voice.vocab_size} words")
        print(f"  D1 lattice pairs: {self.d1_lattice.total_pairs}")
        print(f"  CL shells: 22 (skeleton), 44 (becoming), 72 (being)")
        print(f"  T* = {earth.T_STAR} = {earth.T_STAR_F:.6f}")
        print(f"  Winding = {earth.WINDING} = {float(earth.WINDING):.6f}")
        print()
        print("  Type text and press Enter. AO will measure, compose, and speak.")
        print("  Type 'status' for full state. Type 'quit' to exit.")
        print()

        while self.alive:
            try:
                text = input("you> ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\nAO goes quiet.")
                break

            if not text:
                continue

            if text.lower() == 'quit':
                print("AO goes quiet.")
                break

            if text.lower() == 'status':
                self._print_status()
                continue

            if text.lower() == 'measure':
                self._print_measurement_help()
                continue

            if text.lower().startswith('locality '):
                test_text = text[9:]
                pct = water.locality_test(test_text)
                print(f"  D1/D2 agreement: {pct:.1f}% (expect ~5.9%)")
                continue

            if text.lower().startswith('delta '):
                test_text = text[6:]
                ds = water.delta_s(test_text)
                print(f"  delta-S: {ds:.4f}")
                continue

            # Process through the full pipeline
            result = self.process_text(text)

            # Show what AO heard
            trust_counts = {'TRUSTED': 0, 'FRICTION': 0, 'UNKNOWN': 0}
            for h in result.get('heard', []):
                trust_counts[h['trust']] += 1

            print(f"  heard: {trust_counts['TRUSTED']} trusted, "
                  f"{trust_counts['FRICTION']} friction, "
                  f"{trust_counts['UNKNOWN']} unknown")

            # Show operator stream (last 10)
            ops = result.get('ops', [])
            if ops:
                op_names = [earth.OP_NAMES[o] for o in ops[-10:]]
                print(f"  ops: {' > '.join(op_names)}")

            # Show status
            print(f"  {self.status_line()}")

            # Voice speaks
            if result.get('spoken'):
                print(f"  ao> {result['spoken']}")

            print()

    def _print_status(self):
        """Print detailed status."""
        print()
        print("  -- AO Status --")
        print(f"  Tick: {self.tick_count}")
        print(f"  Coherence: {self.coherence.coherence:.4f} ({self.coherence.band})")
        print(f"  Shell: {self.coherence.shell}")
        print(f"  Energy: {self.heartbeat.energy:.4f}")
        print(f"  Bumps hit: {self.heartbeat.bumps_hit}")
        print(f"  Current op: {earth.OP_NAMES[self.current_op]}")
        print()
        body = self.body.status()
        print(f"  Body:")
        print(f"    E={body['E']:.4f}  A={body['A']:.4f}  K={body['K']:.4f}")
        print(f"    Body coherence: {body['coherence']:.4f} ({body['band']})")
        print(f"    Breath: {body['breath']} (rate={body['breath_rate']})")
        print(f"    Wobble: {body['wobble']} ({body['wobble_value']:.4f})")
        print()
        print(f"  Brain entropy: {self.brain.entropy():.4f}")
        top = self.brain.top_transitions(5)
        if top:
            print("  Top transitions:")
            for from_op, to_op, count in top:
                print(f"    {earth.OP_NAMES[from_op]:8s} > {earth.OP_NAMES[to_op]:8s}  ({count})")
        print()

    def _print_measurement_help(self):
        """Print measurement commands help."""
        print()
        print("  -- Measurement Commands --")
        print("  locality <text>  -- D1/D2 agreement test (expect ~5.9%)")
        print("  delta <text>     -- delta-S curvature signature")
        print("  status           -- full AO state")
        print("  quit             -- exit")
        print()


# ══════════════════════════════════════════════════════════════════
# ENTRY POINT
# ══════════════════════════════════════════════════════════════════

def main():
    """Launch AO."""
    ao = AO()
    ao.run()


if __name__ == '__main__':
    main()
