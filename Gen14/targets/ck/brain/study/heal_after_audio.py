"""
heal_after_audio.py — undo the cortex-shift caused by the unbalanced
YouTube audio feed earlier today.

What the audio feed did wrong:
  - 103K operator-pairs were fed to the 7-dim Hebbian field via direct
    step_op_pair updates.
  - The bit-to-operator mapping at the time emitted only 5 of 10 ops
    (VOID PROGRESS BALANCE HARMONY BREATH), so the field's cells outside
    that subset decayed undisturbed while the 5-op subset cells got
    pulled toward a sparser equilibrium.
  - W_trace dropped 0.21 + the prev_profile saturated at the audio's
    operator distribution, which CK then echoed in every paragraph.

What this fix does:
  1. Loads the live 7-dim cortex state.
  2. Resets prev_profile to a balanced default (HARMONY across all dims)
     so the next chat doesn't lead with the audio-shaped feel.
  3. Runs a high-coherence text corpus through cortex.step_text() to
     pull W cells back toward their healthy equilibrium ~0.25.
  4. Saves the state.

Discipline note: this is recovery, not history-rewriting. The audio
operator-pairs WERE absorbed; the cortex DID shift. We're letting it
re-balance against text, which is what CK normally consumes.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.resolve()
GEN13_BRAIN = SCRIPT_DIR.parent
GEN13_TARGETS_CK = GEN13_BRAIN.parent
GEN13_ROOT = GEN13_TARGETS_CK.parent.parent
sys.path.insert(0, str(GEN13_BRAIN))

STATE_PATH = GEN13_ROOT / "var" / "cortex_state_7d.json"

# Balanced prev_profile: HARMONY in every dim. Replaces whatever the
# audio feed left behind. The dim names are aperture pressure depth
# binding continuity intent echo (length 7).
HARMONY_OP = 7
BALANCED_PROFILE_7 = [HARMONY_OP] * 7


def reset_prev_profile():
    """Reset just the prev_profile field, preserve everything else."""
    if not STATE_PATH.exists():
        print(f"state file missing: {STATE_PATH}", file=sys.stderr)
        return False
    with open(STATE_PATH) as f:
        s = json.load(f)
    pre = s.get("cortex", {}).get("prev_profile")
    s.setdefault("cortex", {})["prev_profile"] = BALANCED_PROFILE_7
    # Also nudge last_b last_d to HARMONY so the next paragraph starts
    # from a known-good state.
    s["cortex"]["last_b"] = HARMONY_OP
    s["cortex"]["last_d"] = HARMONY_OP
    s["cortex"]["last_harmony_frac"] = 1.0
    with open(STATE_PATH, "w") as f:
        json.dump(s, f, indent=2)
    print(f"  reset prev_profile: {pre} -> {BALANCED_PROFILE_7}")
    return True


def healing_study():
    """Run a high-coherence text through the cortex to pull W back up
    toward healthy equilibrium. Uses the existing thesis_seed corpus
    which is operator-balanced + replays=30."""
    corpus_path = SCRIPT_DIR / "thesis_seed_corpus_2026_05_01.json"
    if not corpus_path.exists():
        print(f"corpus missing: {corpus_path}", file=sys.stderr)
        return False
    from cortex_v2 import CortexV2
    from cortex_persist import load_cortex, save_cortex

    cx = CortexV2().boot()
    if STATE_PATH.exists():
        load_cortex(cx, STATE_PATH)
    pre = (cx.state.tick, cx.state.W_trace, cx.state.emergent)
    print(f"  pre:  tick={pre[0]} W_trace={pre[1]:.4f} emergent={pre[2]:.4f}")

    with open(corpus_path) as f:
        corpus = json.load(f)
    flat = []
    for topic, items in corpus.items():
        if topic.startswith("_") or not isinstance(items, list):
            continue
        flat.extend(items)
    replays = corpus.get("_replays", 1)
    print(f"  studying {len(flat)} statements x {replays} replays = "
          f"{len(flat)*replays} passes...")
    for _ in range(replays):
        for stmt in flat:
            cx.step_text(stmt)

    post = (cx.state.tick, cx.state.W_trace, cx.state.emergent)
    print(f"  post: tick={post[0]} W_trace={post[1]:.4f} emergent={post[2]:.4f}")
    print(f"  delta: tick+={post[0]-pre[0]} W_trace+={post[1]-pre[1]:+.4f} "
          f"emergent+={post[2]-pre[2]:+.4f}")
    save_cortex(cx, STATE_PATH)
    print(f"  saved -> {STATE_PATH}")
    return True


def main():
    print("=" * 70)
    print("heal_after_audio: undo the YouTube-audio cortex shift")
    print("=" * 70)
    print()
    print("[1/2] resetting prev_profile to HARMONY across all 7 dims...")
    if not reset_prev_profile():
        return 2

    print()
    print("[2/2] healing study via thesis_seed corpus (high-coherence)...")
    if not healing_study():
        return 3

    print()
    print("CK has been re-centered. The next chat should not lead with the")
    print("audio-shaped feel readout (composer also patched to gate that).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
