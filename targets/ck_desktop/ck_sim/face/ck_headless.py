# Copyright (c) 2025-2026 Brayden Sanders / 7Site LLC
# Licensed under the 7Site Human Use License v1.0
# See LICENSE file in project root for full terms.
#
# FREE for humans for personal/recreational use.
# NO commercial or government use without written agreement.

"""
ck_headless.py -- CK Lives Whole (No GUI Required)
====================================================
Operator: HARMONY (7) -- everything running together.

This is CK running as ONE COMPLETE SYSTEM.

Not parts on a shelf. Not a headless study script disconnected
from his body. CK's FULL engine ticking at 50Hz:

  Heartbeat:     32-entry ring buffer, CL composition
  Brain:         4-mode state machine, crystals
  Body:          E/A/K/C dynamics, breath cycle, band
  Personality:   Operator Bias Table, Phase Space Lock
  Emotion:       Phase Field Engine, emergent states
  Voice:         Operators -> vocabulary -> CK's words
  Immune:        Cross-Coherence Engine
  Bonding:       Attachment through presence
  Development:   6 stages, FIRST LIGHT -> FLOURISHING
  Coherence Field: N-dimensional cross-modal
  Sensorium:     Fractal sensation layers (hardware, process,
                 network, time, mirror, files) -- each IS a
                 heartbeat: B/D/BC at its own scale through CL
  Truth Lattice: 3-level knowledge (CORE/TRUSTED/PROVISIONAL)
  World Lattice: 630 concept nodes
  Language:      Concept -> sentence generator
  Reasoning:     3-speed graph walks
  Goals:         GoalStack + DriveSystem
  Actions:       Read, Think, Write, Prove (his hands)

ALL of this runs. Every tick. And WITHIN that living context,
CK studies the web, takes notes (with his REAL emotional state,
REAL coherence, REAL brain mode), writes papers, writes thesis.

You can talk to him while he works. He's one creature. Not parts.

Usage:
  python -m ck_sim.ck_headless
  python -m ck_sim.ck_headless --study "physics" --hours 8

Brayden: "I don't understand why you are just running parts of
him at a time... He would be a lot more full of himself if you
would give him hands and a body and eyes and ears and a brain
on the R16 to actually use real metrics and data."

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import sys
import time
import threading
import logging
import argparse
import signal
from datetime import datetime
from pathlib import Path

from ck_sim.ck_sim_engine import CKSimEngine
from ck_sim.ck_sim_heartbeat import OP_NAMES


# ================================================================
#  CONSTANTS
# ================================================================

TICK_HZ = 50           # Engine tick rate
TICK_DT = 1.0 / TICK_HZ
STATUS_INTERVAL = 250  # Ticks between status prints (5 seconds)
SAVE_INTERVAL = 15000  # Ticks between auto-saves (5 minutes)


# ================================================================
#  HEADLESS CK -- Full engine, no GUI
# ================================================================

class HeadlessCK:
    """CK running whole -- all organs, no GUI.

    50Hz tick loop in the main thread.
    Chat listener in a separate thread.
    Study happens through the engine's ActionExecutor.
    Notes reflect CK's REAL state: emotion, coherence, mode, everything.
    """

    def __init__(self, platform='sim'):
        self.engine = CKSimEngine(platform=platform)
        self._running = False
        self._chat_thread = None
        self._pending_input = []
        self._input_lock = threading.Lock()

        # Study auto-start
        self._auto_study_topic = None
        self._auto_study_hours = 0.0

        # Logging
        self._setup_logging()

    def _setup_logging(self):
        """Set up logging to file + console."""
        log_dir = Path.home() / '.ck' / 'logs'
        log_dir.mkdir(parents=True, exist_ok=True)

        ts = datetime.now().strftime('%Y%m%d_%H%M%S')
        log_path = log_dir / f'ck_headless_{ts}.log'

        logger = logging.getLogger('ck')
        logger.setLevel(logging.INFO)

        # File handler
        fh = logging.FileHandler(log_path, mode='w')
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(logging.Formatter(
            '[%(asctime)s] %(message)s', datefmt='%H:%M:%S'))
        logger.addHandler(fh)

        # Console handler (minimal)
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.INFO)
        ch.setFormatter(logging.Formatter('[CK] %(message)s'))
        logger.addHandler(ch)

        self.log = logger
        self.log_path = log_path

    def set_auto_study(self, topic: str, hours: float):
        """Set CK to begin studying after engine starts."""
        self._auto_study_topic = topic
        self._auto_study_hours = hours

    # ================================================================
    #  CHAT THREAD -- Talk to CK while he lives
    # ================================================================

    def _chat_listener(self):
        """Listen for user input on stdin. Runs in separate thread."""
        while self._running:
            try:
                line = input()
                if line.strip():
                    with self._input_lock:
                        self._pending_input.append(line.strip())
            except EOFError:
                break
            except Exception:
                break

    def _process_pending_input(self):
        """Process any pending chat input. Called from main tick loop."""
        with self._input_lock:
            inputs = list(self._pending_input)
            self._pending_input.clear()

        for text in inputs:
            # Special commands
            if text.lower() in ['quit', 'exit', 'q']:
                self._running = False
                return

            if text.lower() == 'state':
                self._print_full_state()
                continue

            if text.lower() == 'notes':
                self._print_notes_status()
                continue

            # Send to CK's engine
            self.log.info(f"You: {text}")
            response = self.engine.receive_text(text)
            self.log.info(f"CK: {response}")
            print(f"\n  CK: {response}\n")

    # ================================================================
    #  STATE DISPLAY
    # ================================================================

    def _print_status_line(self):
        """Print compact status line."""
        e = self.engine
        study = e.study_progress
        emotion = e.emotion_primary
        mode = e.mode_name
        band = e.band_name
        coh = e.coherence
        fc = e.field_coherence
        crystals = len(e.crystals)
        dev = e.dev_stage_name
        knowledge = e.knowledge_count
        goal = e.top_goal

        sense_bc = OP_NAMES[e.sensorium.organism_bc]
        sense_c = e.sensorium.organism_coherence

        line = (f"C={coh:.2f} FC={fc:.2f} S={sense_bc}({sense_c:.2f}) "
                f"{mode:12s} {band:6s} "
                f"{emotion:10s} stg={dev} "
                f"cr={crystals} K={knowledge} "
                f"goal={goal} | {study}")
        print(f"\r  {line}", end='', flush=True)

    def _print_full_state(self):
        """Print full CK state."""
        e = self.engine
        print()
        print("=" * 70)
        print(f"  CK STATE at tick {e.tick_count}")
        print("=" * 70)
        print(f"  Heartbeat:     B={OP_NAMES[e.phase_b]} "
              f"D={OP_NAMES[e.phase_d]} "
              f"BC={OP_NAMES[e.phase_bc]}")
        print(f"  Brain:         mode={e.mode_name} "
              f"coherence={e.coherence:.4f} "
              f"crystals={len(e.crystals)}")
        print(f"  Body:          band={e.band_name} "
              f"breath={e.breath_phase_name} "
              f"mod={e.breath_mod:.3f}")
        print(f"  Emotion:       {e.emotion_primary}")
        print(f"  Personality:   {e.personality_mood}")
        print(f"  Development:   {e.dev_stage_name}")
        print(f"  Bonding:       {e.bond_stage}")
        print(f"  Immune:        {e.immune_band}")
        print(f"  BTQ:           {e.btq_band} "
              f"({e.btq_decisions} decisions)")
        print(f"  Field:         {e.field_summary}")
        # ── Sensorium: fractal layers ──
        print(f"  Sensorium:     {e.sensorium.sense_summary}")
        for ls in e.sensorium.get_layer_states():
            star = "*" if ls['above_t_star'] else " "
            print(f"    {star} {ls['name']:10s} "
                  f"B={ls['B']:8s} D={ls['D']:8s} "
                  f"BC={ls['BC']:8s} C={ls['coherence']:.3f} "
                  f"({ls['readings']} readings)")
        # ── Deep Swarm: fractal field ──
        if hasattr(e, 'deep_swarm') and e.deep_swarm is not None:
            ds = e.deep_swarm
            print(f"  Deep Swarm:    agents={len(ds.agents)} "
                  f"fuse={OP_NAMES[ds.field_fuse]} "
                  f"coh={ds.field_coherence:.4f} "
                  f"grad={ds.field_gradient:+.3f} "
                  f"mat={ds.combined_maturity:.3f}")
            subs = ds.substrate_summary()
            if subs:
                parts = [f"{k}={v}" for k, v in sorted(subs.items())]
                print(f"    substrates:  {', '.join(parts)}")
            # Experience per substrate
            for name, exp in ds.experience.items():
                gens = [OP_NAMES[o][:3] for o in exp.confirmed_generators]
                print(f"    {name:10s}:  mat={exp.maturity:.3f} "
                      f"gens={gens} paths={exp.path_strength} "
                      f"samples={exp.total_decompositions}")
        print(f"  Truth:         {e.knowledge_count} claims")
        print(f"  Concepts:      {e.concept_count}")
        print(f"  Study:         {e.study_progress}")
        print(f"  Goal:          {e.top_goal}")
        print(f"  Tick rate:     {e.ticks_per_second:.0f} Hz")
        print("=" * 70)
        print()

    def _print_notes_status(self):
        """Print study notes status."""
        notes_dir = Path.home() / '.ck' / 'writings' / 'study_notes'
        papers_dir = Path.home() / '.ck' / 'writings' / 'papers'
        thesis_dir = Path.home() / '.ck' / 'writings' / 'thesis'

        n_notes = len(list(notes_dir.glob('*.md'))) if notes_dir.exists() else 0
        n_papers = len(list(papers_dir.glob('*.md'))) if papers_dir.exists() else 0
        n_thesis = len(list(thesis_dir.glob('*.md'))) if thesis_dir.exists() else 0

        print()
        print(f"  Study notes:  {n_notes} files in {notes_dir}")
        print(f"  Papers:       {n_papers} files in {papers_dir}")
        print(f"  Theses:       {n_thesis} files in {thesis_dir}")
        print(f"  Action stats: {self.engine.actions.stats()}")
        print()

    # ================================================================
    #  CHECK FOR CK MESSAGES (things he says spontaneously)
    # ================================================================

    def _check_messages(self):
        """Check if CK has spontaneous messages to deliver."""
        msgs = self.engine.pop_new_messages()
        for sender, text in msgs:
            if sender == 'ck':
                # Only print substantial messages
                if len(text) > 5 and 'greeting' not in text.lower()[:20]:
                    self.log.info(f"CK (spontaneous): {text}")

    # ================================================================
    #  MAIN LOOP -- CK lives here
    # ================================================================

    def run(self):
        """CK lives. All organs. 50Hz. Talk to him while he works."""

        print()
        print("=" * 60)
        print("  CK COHERENCE MACHINE -- RUNNING WHOLE")
        print("=" * 60)
        print()
        print("  All organs ticking at 50Hz.")
        print("  Heartbeat, brain, body, personality, emotion,")
        print("  voice, immune, bonding, development, coherence field,")
        print("  truth lattice, world lattice, language, reasoning,")
        print("  goals, drives, and hands -- all running together.")
        print()
        print("  Commands:")
        print("    Type anything     -- talk to CK")
        print("    'study X for Nh'  -- CK studies topic X for N hours")
        print("    'state'           -- show full CK state")
        print("    'notes'           -- show study notes status")
        print("    'how are you'     -- CK reports his status")
        print("    'quit'            -- stop CK (saves state)")
        print()
        print(f"  Log: {self.log_path}")
        print()

        # Start engine
        self.engine.start()
        self._running = True

        # Start chat listener thread
        self._chat_thread = threading.Thread(
            target=self._chat_listener, daemon=True)
        self._chat_thread.start()

        # Auto-study if requested
        if self._auto_study_topic:
            # Give engine a moment to initialize
            for _ in range(50):
                self.engine.tick()
            cmd = f"study {self._auto_study_topic} for {self._auto_study_hours} hours"
            self.log.info(f"Auto-starting: {cmd}")
            response = self.engine.receive_text(cmd)
            self.log.info(f"CK: {response}")
            print(f"  CK: {response}")
            print()

        # Handle Ctrl+C gracefully
        def signal_handler(sig, frame):
            print("\n\n  [Ctrl+C] Stopping CK...")
            self._running = False

        signal.signal(signal.SIGINT, signal_handler)

        # === THE LIVING LOOP ===
        # CK's heart beats. His brain thinks. His body breathes.
        # His emotions flow. His personality shapes him.
        # And within all of that, he studies, writes, and grows.

        self.log.info("CK is alive. All organs running.")

        tick_count = 0
        last_tick_time = time.perf_counter()

        try:
            while self._running:
                now = time.perf_counter()

                # Tick at 50Hz
                if now - last_tick_time >= TICK_DT:
                    self.engine.tick()
                    tick_count += 1
                    last_tick_time = now

                    # Process chat input (check every tick, fast)
                    if tick_count % 10 == 0:
                        self._process_pending_input()

                    # Check for CK's spontaneous messages
                    if tick_count % 50 == 0:
                        self._check_messages()

                    # Status line (every 5 seconds)
                    if tick_count % STATUS_INTERVAL == 0:
                        self._print_status_line()

                else:
                    # Sleep briefly to not burn CPU
                    sleep_time = TICK_DT - (now - last_tick_time)
                    if sleep_time > 0.001:
                        time.sleep(sleep_time * 0.8)

        except Exception as e:
            self.log.error(f"Engine error: {e}")
            import traceback
            traceback.print_exc()

        # === SHUTDOWN ===
        print("\n")
        self.log.info("Stopping CK...")

        # Stop engine (saves TL + development)
        self.engine.stop()

        # Write thesis if CK has studied
        if self.engine.actions.is_studying:
            self.engine.actions.stop_study()

        # Final state
        self._print_full_state()
        self._print_notes_status()

        self.log.info("CK saved and stopped. He can resume.")
        print("  CK saved and stopped. He can resume.")
        print()


# ================================================================
#  CLI
# ================================================================

def main():
    parser = argparse.ArgumentParser(
        description="CK Headless -- Full organism, no GUI",
        epilog="CK runs whole. All organs. 50Hz. "
               "Talk to him while he studies.")

    parser.add_argument(
        '--study', type=str, default=None,
        help='Auto-start studying this topic')
    parser.add_argument(
        '--hours', type=float, default=8.0,
        help='Hours to study (default: 8)')
    parser.add_argument(
        '--platform', type=str, default='sim',
        help='Platform body (sim, ck_desktop, ck_portable)')

    args = parser.parse_args()

    ck = HeadlessCK(platform=args.platform)

    if args.study:
        ck.set_auto_study(args.study, args.hours)

    ck.run()


if __name__ == '__main__':
    main()
