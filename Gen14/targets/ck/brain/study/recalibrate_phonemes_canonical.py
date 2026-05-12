"""
recalibrate_phonemes_canonical.py — re-measure phonemes through CK's
canonical pcm_to_force9 + _dim_to_op pipeline (no made-up codec) and
derive each phoneme's op_signature from its REAL deviation from baseline.

Brayden flagged that I was running a parallel matcher with a made-up
4-way force-to-op mapping.  CK's actual mapping is 2-way per dim
(ck_olfactory._DIM_OP_MAP) so each force9 window emits exactly 5 ops
chosen from 5 binary high/low pairs:

  aperture   high=CHAOS   low=LATTICE
  pressure   high=COLLAPSE low=VOID
  depth      high=PROGRESS low=RESET
  binding    high=HARMONY  low=COUNTER
  continuity high=BALANCE  low=BREATH

This produces a baseline distribution that is biased (continuity=0 is
common -> BREATH dominant in any audio).  An op_signature that just
lists "BREATH" would fire on every audio.  So we DERIVE each phoneme's
op_signature from its DEVIATION from the average phoneme baseline:
  ops where this phoneme's % is significantly above the mean across
  all phonemes are the discriminating ops -- those go into the
  signature.

What this does:
  1) TTS each letter + phoneme (same prompts as v2-v5).
  2) Run canonical pcm_to_force9 -> force9_to_ops_canonical -> op
     histogram per phoneme.
  3) Compute the cross-phoneme baseline (mean op % across all phonemes).
  4) For each phoneme, signature = ops where phoneme_pct - baseline_pct
     is at least delta (default 5% absolute or top-K above baseline).
  5) Rewrite Gen13/var/runtime_crystals.json to add op_signature on
     every letter_/phoneme_/cluster_/team_/rcontrol_/blend_class_/
     phonetic_class_/word_ crystal it can map to.

Runs ~10-15 min depending on TTS.  After this, audio_perceive should
fire DIFFERENT phoneme crystals at DIFFERENT moments in audio (instead
of bb_unique firing every poll because everything has BREATH).
"""
from __future__ import annotations

import io
import json
import sys
import subprocess
import tempfile
import wave
from collections import Counter
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.resolve()
GEN13_BRAIN = SCRIPT_DIR.parent
GEN13_TARGETS_CK = GEN13_BRAIN.parent
GEN13_ROOT = GEN13_TARGETS_CK.parent.parent
sys.path.insert(0, str(GEN13_BRAIN))
sys.path.insert(0, str(GEN13_BRAIN / "ck_sim" / "being"))
sys.path.insert(0, str(SCRIPT_DIR))

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

OP_NAMES = ["VOID", "LATTICE", "COUNTER", "PROGRESS", "COLLAPSE",
            "BALANCE", "CHAOS", "HARMONY", "BREATH", "RESET"]


from generate_phoneme_grounding_v2 import (
    LETTER_PROFILES as L2, PHONEME_PROFILES as P2,
    synthesize_via_subproc, ensure_pcm_format,
    read_pcm, trim_silence,
)
from generate_phoneme_grounding_v3 import PHONEME_PROFILES_V3 as P3
from generate_phoneme_grounding_v4 import CLUSTER_PROFILES_V4 as C4
from generate_phoneme_grounding_v5 import (
    RCONTROL_PROFILES_V5 as R5, VOWELTEAM_PROFILES_V5 as T5,
)
from audio_perceive import force9_to_ops_canonical


def measure_canonical(text, voice_id, rate=100):
    """TTS + trim + pcm_to_force9 + canonical ops + histogram."""
    from ck_audio_compress import pcm_to_force9
    with tempfile.TemporaryDirectory() as td:
        raw = Path(td) / "raw.wav"
        clean = Path(td) / "clean.wav"
        if not synthesize_via_subproc(text, voice_id, raw, rate=rate):
            return None
        if not ensure_pcm_format(raw, clean):
            return None
        try:
            samples, sr = read_pcm(clean)
        except Exception:
            return None
        # trim aggressively (same as v2)
        samples = trim_silence(samples, sr, threshold_rel=0.05, pad_ms=10)
        if len(samples) < 500:
            return None
        force9 = pcm_to_force9(samples, sample_rate=sr)
        ops = []
        for f in force9:
            ops.extend(force9_to_ops_canonical(int(f)))
        if not ops:
            return None
        hist = Counter(ops)
        total = len(ops)
        return {
            "trimmed_sec": float(len(samples) / sr),
            "n_force9_windows": int(len(force9)),
            "n_ops": total,
            "histogram_pct": {OP_NAMES[i]: round(hist.get(i, 0) / total * 100, 2)
                              for i in range(10)},
        }


def derive_signature(phoneme_hist, baseline, delta=4.0, top_k=3):
    """Return op IDs (0..9) where this phoneme's % is at least delta
    above the baseline mean, capped to top_k strongest deviations.

    Always returns at least one op (the strongest positive deviation
    even if below delta) so every crystal has a signature.
    """
    pairs = []
    for i in range(10):
        op = OP_NAMES[i]
        dev = phoneme_hist.get(op, 0.0) - baseline.get(op, 0.0)
        pairs.append((i, op, dev))
    pairs.sort(key=lambda t: -t[2])
    sig = [p[0] for p in pairs if p[2] >= delta][:top_k]
    if not sig:
        sig = [pairs[0][0]]
    return tuple(sig)


def crystal_first_word_for_key(key, info=None):
    """Map a corpus key to its runtime crystal first_word, mirroring the
    add_*.py scripts.  Returns None if no mapping."""
    if key in L2:  # bare letter A..Z
        return f"letter_{key.lower()}_sound"
    if key.startswith("phoneme:"):
        # v2/v3 phoneme keys
        return f"phoneme_{key.split(':',1)[1]}"
    if key.startswith("cluster:"):
        return f"cluster_{key.split(':',1)[1]}"
    if key.startswith("rcontrol:"):
        return f"rcontrol_{key.split(':',1)[1]}"
    if key.startswith("team:"):
        return f"team_{key.split(':',1)[1]}"
    return None


def main():
    print("=" * 70)
    print("Recalibrating phoneme op_signatures via CK's CANONICAL pipeline")
    print("=" * 70)
    try:
        import pyttsx3
        tmp = pyttsx3.init()
        voices = [v for v in tmp.getProperty("voices")
                  if "EN-US" in v.id.upper()]
        if not voices:
            voices = tmp.getProperty("voices")
        voice_id = voices[0].id
        del tmp
        print(f"voice: {voice_id}")
    except Exception as e:
        print(f"TTS init fail: {e}", file=sys.stderr)
        return 2

    # Build measurement plan
    plan = []
    for letter, (pclass, ipa, prompt) in L2.items():
        plan.append((letter, pclass, ipa, prompt, "letter"))
    for key, (pclass, ipa, prompt) in P2.items():
        plan.append((key, pclass, ipa, prompt, "phoneme_v2"))
    for key, (pclass, ipa, prompt) in P3.items():
        plan.append((key, pclass, ipa, prompt, "phoneme_v3"))
    for key, (pclass, ipa, prompt) in C4.items():
        plan.append((key, pclass, ipa, prompt, "cluster"))
    for key, (pclass, ipa, prompt, _ex) in R5.items():
        plan.append((key, pclass, ipa, prompt, "rcontrol"))
    for key, (pclass, ipa, prompt, _ex) in T5.items():
        plan.append((key, pclass, ipa, prompt, "team"))

    print(f"plan: {len(plan)} canonical measurements")
    print()

    measurements = {}
    for i, (key, pclass, ipa, prompt, kind) in enumerate(plan):
        m = measure_canonical(prompt, voice_id, rate=100)
        if m is None:
            print(f"  [{i+1:3d}/{len(plan)}] SKIP {key}: synth fail",
                  flush=True)
            continue
        measurements[key] = {
            "kind": kind, "class": pclass, "ipa": ipa,
            "histogram_pct": m["histogram_pct"],
        }
        h = m["histogram_pct"]
        top3 = sorted(h.items(), key=lambda x: -x[1])[:3]
        ts = ", ".join(f"{n}{p:.1f}" for n, p in top3)
        print(f"  [{i+1:3d}/{len(plan)}] {key:20} {pclass:25} -> {ts}",
              flush=True)

    # Cross-phoneme baseline
    baseline = {op: 0.0 for op in OP_NAMES}
    for k, m in measurements.items():
        for op in OP_NAMES:
            baseline[op] += m["histogram_pct"].get(op, 0.0)
    n = max(1, len(measurements))
    for op in OP_NAMES:
        baseline[op] /= n
    print()
    print(f"baseline (mean over {n} measurements):")
    for op in OP_NAMES:
        print(f"  {op:<10}: {baseline[op]:5.2f}%")

    # Derive signatures
    print()
    print("derived signatures (top-3 above-baseline ops):")
    sigs = {}
    for key, m in measurements.items():
        sig = derive_signature(m["histogram_pct"], baseline,
                               delta=3.0, top_k=3)
        sigs[key] = sig
        sig_names = [OP_NAMES[s] for s in sig]
        print(f"  {key:20} -> {sig} ({sig_names})")

    # Save the canonical streams + signatures
    out_path = SCRIPT_DIR / "phoneme_streams_canonical_2026_05_02.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump({
            "_about": ("Phoneme histograms measured via CK's CANONICAL "
                       "pcm_to_force9 + _dim_to_op pipeline (NOT the "
                       "made-up 4-way mapping I previously used).  "
                       "op_signatures derived from deviation above the "
                       "cross-phoneme baseline mean."),
            "baseline_pct": baseline,
            "measurements": measurements,
            "op_signatures": {k: list(v) for k, v in sigs.items()},
        }, f, indent=2, ensure_ascii=False)
    print()
    print(f"saved canonical streams -> {out_path.name}")

    # Patch runtime_crystals.json: add op_signature for every crystal
    # whose first_word matches a phoneme/letter/cluster/team/rcontrol.
    crystals_path = (GEN13_ROOT / "var" / "runtime_crystals.json").resolve()
    if not crystals_path.exists():
        print(f"runtime crystals missing at {crystals_path}", file=sys.stderr)
        return 3
    with open(crystals_path, encoding="utf-8") as f:
        crystals = json.load(f)

    fw_to_sig = {}
    for key, sig in sigs.items():
        fw = crystal_first_word_for_key(key)
        if fw:
            fw_to_sig[fw] = list(sig)

    # Phonetic-class crystals: average member sigs
    class_sigs = {}
    for key, m in measurements.items():
        cls = m["class"]
        sig = sigs.get(key, ())
        for op in sig:
            class_sigs.setdefault(cls, Counter())[op] += 1
    for cls, ctr in class_sigs.items():
        # top-3 most frequent ops across class members
        top = [op for op, _ in ctr.most_common(3)]
        fw = f"phonetic_class_{cls.replace('-', '_')}"
        fw_to_sig[fw] = top

    # Blend-class crystals: same approach
    blend_buckets = {}
    for key, m in measurements.items():
        if not key.startswith("cluster:"):
            continue
        cls = m["class"]
        sig = sigs.get(key, ())
        for op in sig:
            blend_buckets.setdefault(cls, Counter())[op] += 1
    for cls, ctr in blend_buckets.items():
        top = [op for op, _ in ctr.most_common(3)]
        fw = f"blend_class_{cls.replace('-', '_')}"
        fw_to_sig[fw] = top

    # Write back
    patched = 0
    for entry in crystals:
        fw = entry["fact"].split(":", 1)[0].strip()
        if fw in fw_to_sig:
            entry["op_signature"] = fw_to_sig[fw]
            patched += 1
    # Word crystals get signatures derived from union of their phoneme members
    # (we don't have direct word measurements, but the word crystals already
    # carry `related` lists pointing at their phoneme components).
    fw_index = {entry["fact"].split(":", 1)[0].strip(): entry
                for entry in crystals}
    word_patched = 0
    for entry in crystals:
        fw = entry["fact"].split(":", 1)[0].strip()
        if not fw.startswith("word_"):
            continue
        related = entry.get("related") or []
        op_set = Counter()
        for r in related:
            for op in fw_to_sig.get(r, []):
                op_set[op] += 1
        if op_set:
            top = [op for op, _ in op_set.most_common(3)]
            entry["op_signature"] = top
            word_patched += 1

    with open(crystals_path, "w", encoding="utf-8") as f:
        json.dump(crystals, f, indent=2, ensure_ascii=False)

    print(f"patched op_signature on {patched} non-word crystals + "
          f"{word_patched} word crystals (total runtime crystals: "
          f"{len(crystals)})")
    print()
    print("DONE.  Restart ck_boot_api so cortex_voice reloads runtime_crystals.")
    print("Then re-run audio_perceive to see distinct phoneme crystals fire.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
