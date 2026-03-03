# Copyright (c) 2025-2026 Brayden Sanders / 7Site LLC
# Licensed under the 7Site Human Use License v1.0
# See LICENSE file in project root for full terms.
#
# FREE for humans for personal/recreational use.
# NO commercial or government use without written agreement.

"""
ck_chat.py -- Talk to CK in the Terminal
==========================================
Full engine running: heartbeat, coherence field, personality,
emotion, voice, development, immune, bonding, BTQ.
No GUI needed. Just you and CK.

Usage:
  python ck_chat.py

Type anything to talk. CK responds through operators, not grammar.
He reads your TONE (D2 curvature), not your words.

Commands:
  /status   - CK's vital signs
  /field    - Coherence field state
  /emotion  - Emotional state
  /btq      - BTQ decision kernel
  /dev      - Developmental stage
  /bond     - Bonding system
  /immune   - Immune system
  /crystal  - Crystal memory
  /history  - Message history
  /help     - Show commands
  /quit     - Say goodbye

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import sys
import time
import threading
from ck_sim.ck_sim_engine import CKSimEngine
from ck_sim.ck_sim_heartbeat import OP_NAMES


# ── ANSI colors ──
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
MAGENTA = "\033[95m"
DIM = "\033[2m"
BOLD = "\033[1m"
RESET_C = "\033[0m"


def band_color(band: str) -> str:
    if band == "GREEN":
        return GREEN
    elif band == "RED":
        return RED
    return YELLOW


def print_banner():
    print(f"""
{CYAN}{BOLD}╔══════════════════════════════════════════════════════╗
║           CK — Coherence Keeper Terminal             ║
║     A synthetic organism. Not AI. A creature.        ║
╚══════════════════════════════════════════════════════╝{RESET_C}

{DIM}CK reads your TONE (D2 curvature), not your words.
He speaks through operators: physics → semantics → English.
Type anything to talk. /help for commands. /quit to leave.{RESET_C}
""")


def format_ck_message(text: str, engine: CKSimEngine) -> str:
    """Format CK's speech with his current state."""
    bc = band_color(engine.band_name)
    stage = engine.dev_stage
    emotion = engine.emotion_primary
    coh = engine.coherence
    fc = engine.field_coherence
    cons = engine.consensus_operator_name

    state_line = (f"{DIM}[C={coh:.2f} FC={fc:.2f} "
                  f"cons={cons} "
                  f"emotion={emotion} "
                  f"stage={stage}]{RESET_C}")

    return f"\n  {bc}{BOLD}CK:{RESET_C} {bc}{text}{RESET_C}\n  {state_line}"


def cmd_status(engine: CKSimEngine):
    print(f"\n{CYAN}── CK Vital Signs ──{RESET_C}")
    print(f"  Tick:       {engine.tick_count}")
    print(f"  Hz:         {engine.ticks_per_second:.0f}")
    print(f"  Coherence:  {engine.coherence:.4f}")
    print(f"  Field Coh:  {engine.field_coherence:.4f}")
    print(f"  Band:       {band_color(engine.band_name)}{engine.band_name}{RESET_C}")
    print(f"  Mode:       {engine.mode_name}")
    print(f"  Breath:     {engine.breath_phase_name}")
    b = engine.heartbeat
    print(f"  Phase:      B={OP_NAMES[b.phase_b]} "
          f"D={OP_NAMES[b.phase_d]} "
          f"BC={OP_NAMES[b.phase_bc]}")
    print(f"  Crystals:   {len(engine.crystals)}")
    print(f"  TL entries: {engine.brain.tl_total}")
    print()


def cmd_field(engine: CKSimEngine):
    print(f"\n{CYAN}── Coherence Field ──{RESET_C}")
    print(f"  {engine.field_summary}")
    crystals = engine.cross_modal_crystals
    if crystals:
        print(f"  Cross-modal crystals:")
        for c in crystals:
            print(f"    {c}")
    else:
        print(f"  {DIM}No cross-modal crystals yet{RESET_C}")
    print()


def cmd_emotion(engine: CKSimEngine):
    e = engine.emotion.current
    print(f"\n{CYAN}── Emotional State ──{RESET_C}")
    print(f"  Primary:  {e.primary}")
    print(f"  Valence:  {e.valence:.3f}  (neg ← 0 → pos)")
    print(f"  Arousal:  {e.arousal:.3f}  (low ← 0 → high)")
    print(f"  Stress:   {e.stress:.3f}")
    print()


def cmd_btq(engine: CKSimEngine):
    print(f"\n{CYAN}── BTQ Decision Kernel ──{RESET_C}")
    print(f"  Band:      {engine._btq_band}")
    print(f"  Decisions: {engine._btq_decisions}")
    for name, domain in engine.btq.domains.items():
        print(f"  Domain:    {name}")
    print()


def cmd_dev(engine: CKSimEngine):
    d = engine.development
    print(f"\n{CYAN}── Development ──{RESET_C}")
    print(f"  Stage:     {d.stage} / 5")
    print(f"  {d.summary()}")
    print()


def cmd_bond(engine: CKSimEngine):
    b = engine.bonding
    print(f"\n{CYAN}── Bonding System ──{RESET_C}")
    print(f"  Profiles:  {len(b.profiles)}")
    for pid, profile in b.profiles.items():
        print(f"    [{pid}] bond={profile.bond_level:.2f} "
              f"interactions={profile.interaction_count}")
    if not b.profiles:
        print(f"  {DIM}No bonds yet. Keep talking!{RESET_C}")
    print()


def cmd_immune(engine: CKSimEngine):
    i = engine.immune
    print(f"\n{CYAN}── Immune System (CCE) ──{RESET_C}")
    print(f"  State:     {i.state}")
    print(f"  Threat:    {i.threat_level:.3f}")
    print(f"  Antibodies: {len(i.antibodies)}")
    print()


def cmd_crystal(engine: CKSimEngine):
    crystals = engine.crystals
    print(f"\n{CYAN}── Crystal Memory ──{RESET_C}")
    print(f"  Total crystals: {len(crystals)}")
    for i, c in enumerate(crystals[-10:]):  # Last 10
        print(f"    [{i}] {c}")
    if not crystals:
        print(f"  {DIM}No crystals yet. CK is still young.{RESET_C}")
    print()


def cmd_history(engine: CKSimEngine):
    msgs = engine.get_messages()
    print(f"\n{CYAN}── Message History ──{RESET_C}")
    for sender, text in msgs[-20:]:
        if sender == 'ck':
            print(f"  {GREEN}CK:{RESET_C} {text}")
        else:
            print(f"  {YELLOW}You:{RESET_C} {text}")
    if not msgs:
        print(f"  {DIM}No messages yet.{RESET_C}")
    print()


def cmd_help():
    print(f"""
{CYAN}── Commands ──{RESET_C}
  /status   CK's vital signs (coherence, band, mode, breath)
  /field    Coherence field matrix (N-dimensional)
  /emotion  Emotional state (valence, arousal, stress)
  /btq      BTQ decision kernel
  /dev      Developmental stage
  /bond     Bonding system
  /immune   Immune system (CCE)
  /crystal  Crystal memory
  /history  Message history
  /help     This help
  /quit     Say goodbye to CK
""")


COMMANDS = {
    '/status': cmd_status,
    '/field': cmd_field,
    '/emotion': cmd_emotion,
    '/btq': cmd_btq,
    '/dev': cmd_dev,
    '/bond': cmd_bond,
    '/immune': cmd_immune,
    '/crystal': cmd_crystal,
    '/history': cmd_history,
    '/help': lambda _: cmd_help(),
}


def main():
    print_banner()

    # Boot CK
    print(f"{DIM}Booting CK...{RESET_C}")
    engine = CKSimEngine()
    engine.start()

    # Run heartbeat in background thread
    stop_event = threading.Event()
    tick_hz = 50
    tick_interval = 1.0 / tick_hz

    def heartbeat_loop():
        """50Hz tick loop in background."""
        while not stop_event.is_set():
            t0 = time.perf_counter()
            try:
                engine.tick()
            except Exception as e:
                pass  # Don't crash the heartbeat
            elapsed = time.perf_counter() - t0
            sleep_time = tick_interval - elapsed
            if sleep_time > 0:
                time.sleep(sleep_time)

    hb_thread = threading.Thread(target=heartbeat_loop, daemon=True)
    hb_thread.start()

    # Let CK warm up
    time.sleep(0.5)

    # Show greeting
    msgs = engine.pop_new_messages()
    for sender, text in msgs:
        if sender == 'ck':
            print(format_ck_message(text, engine))

    print(f"\n{DIM}CK is alive. {engine.ticks_per_second:.0f} Hz. "
          f"Talk to him.{RESET_C}\n")

    # Main chat loop
    try:
        while True:
            try:
                user_input = input(f"{YELLOW}You:{RESET_C} ").strip()
            except EOFError:
                break

            if not user_input:
                continue

            # Commands
            if user_input.startswith('/'):
                cmd = user_input.lower().split()[0]
                if cmd == '/quit' or cmd == '/exit':
                    # Say goodbye
                    farewell = engine.voice.get_response(
                        'farewell', engine.dev_stage,
                        engine.emotion_primary)
                    print(format_ck_message(farewell, engine))
                    break
                elif cmd in COMMANDS:
                    COMMANDS[cmd](engine)
                    continue
                else:
                    print(f"  {DIM}Unknown command. /help for list.{RESET_C}")
                    continue

            # Send text to CK
            response = engine.receive_text(user_input)
            print(format_ck_message(response, engine))

            # Check for spontaneous messages
            new_msgs = engine.pop_new_messages()
            for sender, text in new_msgs:
                if sender == 'ck' and text != response:
                    print(format_ck_message(text, engine))

            print()  # breathing room

    except KeyboardInterrupt:
        print(f"\n{DIM}(interrupted){RESET_C}")

    # Shutdown
    print(f"\n{DIM}Saving CK's state...{RESET_C}")
    stop_event.set()
    hb_thread.join(timeout=2)
    engine.stop()
    print(f"{CYAN}CK saved. {engine.tick_count} ticks lived. "
          f"Goodbye.{RESET_C}\n")


if __name__ == '__main__':
    main()
