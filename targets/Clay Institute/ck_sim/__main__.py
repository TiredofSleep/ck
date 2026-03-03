"""
CK -- The Coherence Keeper
===========================
Allow running with: python -m ck_sim

Modes:
  python -m ck_sim                  # GUI (Kivy)
  python -m ck_sim --headless       # Terminal only (no GUI)
  python -m ck_sim --gui            # Force GUI even without display detection

On Linux without $DISPLAY, headless mode is selected automatically.

(c) 2026 Brayden Sanders / 7Site LLC
"""
import sys
import os
import argparse


def _has_display():
    """Check whether a graphical display is available."""
    if sys.platform == 'win32':
        return True  # Windows always has a display context
    if sys.platform == 'darwin':
        return True  # macOS always has a display context
    # Linux / other: check DISPLAY or WAYLAND_DISPLAY
    return bool(os.environ.get('DISPLAY') or os.environ.get('WAYLAND_DISPLAY'))


def main():
    parser = argparse.ArgumentParser(
        prog='ck_sim',
        description='CK -- The Coherence Keeper. A living coherence organism.',
    )
    parser.add_argument('--headless', action='store_true',
                        help='Run without GUI (terminal only, 50Hz heartbeat)')
    parser.add_argument('--gui', action='store_true',
                        help='Force GUI mode even if no display detected')
    parser.add_argument('--study', type=str, default=None,
                        help='Auto-study topic (headless mode)')
    parser.add_argument('--hours', type=float, default=0,
                        help='Auto-study duration in hours (headless mode)')
    args = parser.parse_args()

    use_headless = args.headless

    # Auto-detect: no display on Linux → headless
    if not use_headless and not args.gui and not _has_display():
        print("[CK] No display detected -- starting in headless mode.")
        print("[CK] Use --gui to force GUI mode.\n")
        use_headless = True

    if use_headless:
        from ck_sim.face.ck_headless import HeadlessCK
        ck = HeadlessCK(platform='sim')
        if args.study:
            ck.set_auto_study(args.study, args.hours or 1.0)
        ck.run()
    else:
        from ck_sim.face.ck_sim_app import CKSimApp
        CKSimApp().run()


if __name__ == '__main__':
    main()
