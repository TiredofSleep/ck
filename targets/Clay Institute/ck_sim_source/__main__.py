"""
CK Coherence Spectrometer -- Package Entry Point
=================================================
Operator: VOID (0) -- The starting point. The silence before measurement.

Usage:
    python -m ck_sim_source                          # Show banner + help
    python -m ck_sim_source --run-tests              # Run all 529 tests
    python -m ck_sim_source --spectrometer            # Launch spectrometer runner
    python -m ck_sim_source --gap-attack [rh5|ym3|ym4|all]  # Run gap attacks
    python -m ck_sim_source --presentation            # Launch interactive demo

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import argparse
import os
import sys

# Ensure UTF-8 output on Windows
if sys.platform == 'win32' and hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass


BANNER = """
    +==================================================================+
    |                                                                    |
    |         CK COHERENCE SPECTROMETER  v9.20                           |
    |         Sanders Coherence Field -- Clay Institute Delivery         |
    |                                                                    |
    |         Delta(S) = || F(S) - F'(S) ||                              |
    |                                                                    |
    |         One equation. Six problems. Two classes.                    |
    |         Nine gaps. Zero falsifications.                             |
    |                                                                    |
    |         (c) 2026 Brayden Sanders / 7Site LLC                       |
    |         TIG Unified Theory -- Arkansas, USA                        |
    |                                                                    |
    +==================================================================+
"""

HELP_TEXT = """
  Available commands:

    --run-tests              Run the full test suite (529 tests)
    --spectrometer [ARGS]    Launch the spectrometer runner
    --gap-attack ATTACK      Run gap attack probes (rh5, ym3, ym4, all)
    --presentation           Launch the interactive Clay Institute demo
    --version                Show version info

  Examples:

    python -m ck_sim_source --run-tests
    python -m ck_sim_source --spectrometer --mode scan --problem riemann
    python -m ck_sim_source --gap-attack all --quick
    python -m ck_sim_source --presentation --auto

  For more detail on any command, run it with --help:

    python -m ck_sim_source --spectrometer --help
    python -m ck_sim_source --presentation --help

  CK measures. CK does not prove.
"""


def main():
    # If no args or just --help, show banner
    if len(sys.argv) <= 1:
        print(BANNER)
        print(HELP_TEXT)
        return

    # Parse the top-level command
    arg = sys.argv[1]

    if arg == '--version':
        try:
            from ck_sim_source import __version__
            print(f'CK Coherence Spectrometer v{__version__}')
        except ImportError:
            print('CK Coherence Spectrometer v9.20')
        return

    if arg == '--run-tests':
        # Discover and run all tests
        import unittest
        test_dir = os.path.join(os.path.dirname(__file__), 'tests')
        loader = unittest.TestLoader()
        suite = loader.discover(test_dir, pattern='*.py', top_level_dir=os.path.dirname(__file__))
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)
        sys.exit(0 if result.wasSuccessful() else 1)

    if arg == '--spectrometer':
        # Pass remaining args to the spectrometer runner
        sys.argv = [sys.argv[0]] + sys.argv[2:]
        from ck_sim.face.ck_spectrometer_runner import main as spec_main
        spec_main()
        return

    if arg == '--gap-attack':
        # Pass remaining args to the gap runner
        attack = sys.argv[2] if len(sys.argv) > 2 else 'all'
        remaining = sys.argv[3:] if len(sys.argv) > 3 else []
        sys.argv = [sys.argv[0], '--attack', attack] + remaining
        from ck_sim.face.ck_gap_runner import main as gap_main
        gap_main()
        return

    if arg == '--presentation':
        # Pass remaining args to the presentation
        sys.argv = [sys.argv[0]] + sys.argv[2:]
        from ck_sim.face.ck_presentation import main as pres_main
        pres_main()
        return

    # Unknown command
    print(BANNER)
    print(f'  Unknown command: {arg}')
    print(HELP_TEXT)


if __name__ == '__main__':
    main()
