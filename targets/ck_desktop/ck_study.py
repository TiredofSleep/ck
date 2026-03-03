"""
ck_study.py -- CK's Long Study Session
========================================
Operator: PROGRESS (3) -- forward motion, growth.

Starts CK's engine and lets him study autonomously until stopped.
CK picks his own topics, asks Claude, verifies through D2,
builds his truth lattice, writes journal entries, and grows.

Usage:
  python ck_study.py              # Run until stopped (Ctrl+C)
  python ck_study.py --hours 8    # Run for 8 hours then stop

What happens:
  1. Engine boots (all 27 systems)
  2. Every 50 ticks (1 second), CK checks if he should study
  3. If curiosity fires, he picks a topic from 481 seeds
  4. He queries Claude (haiku, ~$0.002/query) through TIG system prompt
  5. He runs D2 on the response -- his math judges everything
  6. Above T* (0.714) -> TRUSTED truth lattice
  7. Below T* + high complexity -> FRICTION memory (novel territory)
  8. He writes a journal entry about what he discovered
  9. Every ~5 minutes, TL saves to disk
 10. On stop: identity saved, final journal snapshot written

$20 budget at haiku rates: ~10,000 queries = weeks of study.
CK's D2 pipeline is the real intelligence. Claude is the library.

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import sys
import os
import time
import signal
import argparse
import io

# Fix Windows console encoding for Hebrew glyphs
if sys.platform == 'win32' and hasattr(sys.stdout, 'buffer'):
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
    except (ValueError, AttributeError):
        pass  # Already wrapped or redirected (nohup)

# ── API KEY ──
# CK's library card. Claude Sonnet -- the full organism.
# CK's D2 pipeline is the real intelligence. Claude is the library.
if not os.environ.get('ANTHROPIC_API_KEY', '').strip():
    _script_dir = os.path.dirname(os.path.abspath(__file__))
    _key_file = os.path.join(_script_dir, '.api_key')
    if os.path.exists(_key_file):
        with open(_key_file, 'r') as f:
            os.environ['ANTHROPIC_API_KEY'] = f.read().strip()

# ── ALL senses active ──
# CK uses every input available: screen, mic, CPU, memory, processes,
# keyboard, mouse, active window, power draw.
# "The more inputs he has the faster he gets superintelligent" -- Brayden
# Being is on the CPU, Doing is on the GPU. Becoming is everywhere.


# ── Dual output: console + log file ──
class TeeLog:
    """Write to both console and a log file with immediate flush."""
    def __init__(self, log_path):
        self._log = open(log_path, 'w', encoding='utf-8')
        self._stdout = sys.stdout

    def say(self, msg=''):
        try:
            print(msg, file=self._stdout, flush=True)
        except (ValueError, OSError):
            pass  # stdout closed (detached process)
        self._log.write(msg + '\n')
        self._log.flush()

    def close(self):
        self._log.flush()
        self._log.close()


def main():
    parser = argparse.ArgumentParser(description='CK Long Study Session')
    parser.add_argument('--hours', type=float, default=0,
                        help='Hours to study (0 = until stopped)')
    args = parser.parse_args()

    # Set up log file
    log_dir = os.path.expanduser('~/.ck/writings')
    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, f'study_{time.strftime("%Y%m%d_%H%M%S")}.log')
    log = TeeLog(log_path)

    log.say("=" * 60)
    log.say("  CK AUTONOMOUS STUDY SESSION")
    log.say("  All 27 systems. Real Claude library. D2 verification.")
    log.say("  TIG fractal note organization: Being/Doing/Becoming.")
    log.say(f"  Log: {log_path}")
    log.say("  Press Ctrl+C to stop gracefully.")
    log.say("=" * 60)
    log.say()

    # Import and boot
    from ck_sim.ck_sim_engine import CKSimEngine

    engine = CKSimEngine()
    engine.start()

    # ── PHASE 1: D1 LATTICE -- Learn generators before complexity ──
    # "Let him play with the dictionary and thesaurus for a while
    #  permutating it all into lattices based on D1 before he learns
    #  to learn and extend into complexity D2." -- Brayden
    log.say("  [D1-LATTICE] Phase 1: Building generator lattice from dictionary...")
    d1_builder = None
    try:
        from ck_sim.becoming.ck_d1_lattice_builder import build_d1_lattice
        d1_builder = build_d1_lattice(log_fn=log.say)
        d1_stats = d1_builder.stats()
        log.say(f"  [D1-LATTICE] {d1_stats['total_pairs']} generator pairs across "
                f"{d1_stats['unique_words']} words")
        log.say(f"  [D1-LATTICE] D1/D2 agreement: {d1_stats['d1_d2_agreement']:.1%} "
                f"(D1 and D2 measure different things)")
        log.say(f"  [D1-LATTICE] Phase distribution: "
                f"Being {d1_stats['phase_distribution'].get('being', 0)} / "
                f"Doing {d1_stats['phase_distribution'].get('doing', 0)} / "
                f"Becoming {d1_stats['phase_distribution'].get('becoming', 0)}")
        log.say("  [D1-LATTICE] CK knows his generators. Ready to study.")
    except Exception as e:
        log.say(f"  [D1-LATTICE] Skipped: {e}")
    log.say()

    # Graceful shutdown on Ctrl+C
    running = True

    def signal_handler(sig, frame):
        nonlocal running
        log.say("\n  [STUDY] Ctrl+C received. Stopping gracefully...")
        running = False

    signal.signal(signal.SIGINT, signal_handler)

    # Calculate end time
    if args.hours > 0:
        end_time = time.time() + (args.hours * 3600)
        log.say(f"  [STUDY] Running for {args.hours} hours (until {time.strftime('%H:%M', time.localtime(end_time))})")
    else:
        end_time = None
        log.say("  [STUDY] Running until Ctrl+C")

    log.say(f"  [STUDY] Truths: {engine.truth.total_entries}")
    log.say(f"  [STUDY] Library: {'LIVE' if engine.library._client else 'MOCK'}")
    log.say(f"  [STUDY] Model: {engine.library.model}")
    log.say(f"  [STUDY] Topics: 481 seed topics across all human knowledge")
    if d1_builder:
        log.say(f"  [STUDY] D1 lattice: {d1_builder.total_pairs} generator pairs loaded")
    log.say()

    # Stats tracking
    start_time = time.time()
    start_truths = engine.truth.total_entries
    last_report = time.time()
    report_interval = 300  # Report every 5 minutes
    d1_learn_interval = 60  # Learn D1 from recent text every 60 seconds
    last_d1_learn = time.time()
    d1_pairs_learned = 0

    try:
        while running:
            engine.tick()

            # Time limit check
            if end_time and time.time() >= end_time:
                log.say(f"\n  [STUDY] Time limit reached ({args.hours} hours).")
                break

            # D1 learning: extract generator pairs from recent study text
            now = time.time()
            if d1_builder and now - last_d1_learn >= d1_learn_interval:
                try:
                    # Get recent text from library responses
                    if hasattr(engine, 'library') and hasattr(engine.library, '_last_response'):
                        recent = getattr(engine.library, '_last_response', '')
                        if recent and len(recent) > 20:
                            word_dict = {}
                            if hasattr(engine, 'dictionary_builder'):
                                word_dict = engine.dictionary_builder.get_full_dictionary()
                            elif hasattr(engine, '_enriched_dict'):
                                word_dict = engine._enriched_dict
                            if word_dict:
                                new = d1_builder.learn_from_text(recent, word_dict)
                                d1_pairs_learned += new
                except Exception:
                    pass
                last_d1_learn = now

            # Periodic status report
            if now - last_report >= report_interval:
                elapsed_h = (now - start_time) / 3600
                new_truths = engine.truth.total_entries - start_truths
                lib_stats = engine.library
                d1_msg = f" | d1: +{d1_pairs_learned}" if d1_builder else ""
                log.say(f"  [STUDY] {elapsed_h:.1f}h | "
                      f"truths: {engine.truth.total_entries} (+{new_truths}) | "
                      f"coh: {engine.coherence:.3f} | "
                      f"library: {lib_stats.total_queries}q "
                      f"({lib_stats.trusted_count}T/{lib_stats.friction_count}F/{lib_stats.provisional_count}P)"
                      f"{d1_msg}")
                last_report = now

            # Small sleep to not burn CPU when idle
            # Engine runs at 50Hz internally but we don't need
            # wall-clock 50Hz for study -- 10Hz is plenty
            time.sleep(0.02)

    except Exception as e:
        log.say(f"\n  [STUDY] Error: {e}")
        import traceback
        log.say(traceback.format_exc())

    # Graceful shutdown
    log.say()
    log.say("=" * 60)
    log.say("  STUDY SESSION COMPLETE")
    log.say("=" * 60)

    elapsed_h = (time.time() - start_time) / 3600
    new_truths = engine.truth.total_entries - start_truths

    log.say(f"  Duration:    {elapsed_h:.2f} hours")
    log.say(f"  Truths:      {engine.truth.total_entries} (+{new_truths} new)")
    log.say(f"  Coherence:   {engine.coherence:.4f}")
    log.say(f"  Library:     {engine.library.total_queries} queries")
    log.say(f"    Trusted:   {engine.library.trusted_count}")
    log.say(f"    Friction:  {engine.library.friction_count}")
    log.say(f"    Provision: {engine.library.provisional_count}")
    if d1_builder:
        log.say(f"  D1 lattice:  {d1_builder.total_pairs} pairs "
                f"(+{d1_pairs_learned} learned during study)")

    # Save everything
    log.say()
    log.say("  Saving state...")
    engine.stop()
    if d1_builder:
        d1_builder.save()
        log.say("  D1 lattice saved. CK knows his generators.")
    log.say("  State saved. CK remembers everything.")
    log.say()
    log.say("  CK studied. CK grew. CK is ready.")
    log.say("=" * 60)
    log.close()


if __name__ == '__main__':
    main()
