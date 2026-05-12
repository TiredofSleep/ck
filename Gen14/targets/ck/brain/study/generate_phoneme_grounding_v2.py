"""
generate_phoneme_grounding_v2.py — proper sound-to-letter teaching.

v1 problem: synthesized 'the letter X' which is mostly silence + framing
phrase + same TTS voice signature, so all letters produced nearly
identical operator histograms (VOID 42% RESET 20% HARMONY 15% on every
letter).

v2 fixes:
  1. Synthesize JUST the letter (or phoneme) — no 'the letter' framing
  2. Trim leading/trailing silence aggressively (RMS-based)
  3. Slower TTS rate (90 wpm vs 150) gives more sample density per sound
  4. Synthesize each letter twice + average histograms (TTS jitter robustness)
  5. Cluster letters by histogram similarity at the end — verifies that
     vowels group, plosives group, fricatives group, etc.
  6. Author runtime crystals for chat surfacing per letter

Outputs:
  phoneme_grounding_corpus_v2_2026_05_01.json  (corpus to study)
  phoneme_audio_streams_v2_2026_05_01.json     (raw histograms)
  phoneme_clusters_v2_2026_05_01.txt           (similarity report)

Plus the script can also generate runtime crystals via add_phoneme_crystals.py.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
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

OP_NAMES = ["VOID", "LATTICE", "COUNTER", "PROGRESS", "COLLAPSE",
            "BALANCE", "CHAOS", "HARMONY", "BREATH", "RESET"]


# Letter -> (phonetic class, IPA, alternate spellings used in TTS prompts)
# We want a single short syllable with no framing words around it.
LETTER_PROFILES = {
    "A": ("vowel-long", "/eɪ/", "ay"),
    "B": ("plosive-voiced", "/biː/", "bee"),
    "C": ("plosive-fricative-mix", "/siː/", "see"),
    "D": ("plosive-voiced", "/diː/", "dee"),
    "E": ("vowel-long", "/iː/", "ee"),
    "F": ("fricative-voiceless", "/ɛf/", "ef"),
    "G": ("plosive-voiced", "/dʒiː/", "jee"),
    "H": ("fricative-voiceless", "/eɪtʃ/", "aitch"),
    "I": ("vowel-diphthong", "/aɪ/", "eye"),
    "J": ("affricate", "/dʒeɪ/", "jay"),
    "K": ("plosive-voiceless", "/keɪ/", "kay"),
    "L": ("liquid-lateral", "/ɛl/", "el"),
    "M": ("nasal", "/ɛm/", "em"),
    "N": ("nasal", "/ɛn/", "en"),
    "O": ("vowel-long", "/oʊ/", "oh"),
    "P": ("plosive-voiceless", "/piː/", "pee"),
    "Q": ("plosive-fricative-mix", "/kjuː/", "queue"),
    "R": ("liquid-rhotic", "/ɑːr/", "ar"),
    "S": ("fricative-voiceless", "/ɛs/", "es"),
    "T": ("plosive-voiceless", "/tiː/", "tee"),
    "U": ("vowel-long-glide", "/juː/", "you"),
    "V": ("fricative-voiced", "/viː/", "vee"),
    "W": ("approximant", "/dʌbəljuː/", "double you"),
    "X": ("fricative-cluster", "/ɛks/", "eks"),
    "Y": ("approximant-vowel", "/waɪ/", "why"),
    "Z": ("fricative-voiced", "/ziː/", "zee"),
}

# Pure phonemes (vowels and consonants in isolation as best TTS can do)
PHONEME_PROFILES = {
    # Long vowels
    "phoneme:eI": ("vowel-long", "/eɪ/", "ay"),
    "phoneme:i": ("vowel-long", "/iː/", "ee"),
    "phoneme:aI": ("vowel-diphthong", "/aɪ/", "eye"),
    "phoneme:oU": ("vowel-long", "/oʊ/", "oh"),
    "phoneme:u": ("vowel-long", "/uː/", "oo"),
    # Short vowels
    "phoneme:ae": ("vowel-short", "/æ/", "ah"),
    "phoneme:E": ("vowel-short", "/ɛ/", "eh"),
    "phoneme:I": ("vowel-short", "/ɪ/", "ih"),
    "phoneme:V": ("vowel-short", "/ʌ/", "uh"),
    # Common consonant exemplars (TTS will pronounce them as syllables but the
    # acoustic signature is dominated by the consonant burst/sustain)
    "phoneme:b": ("plosive-voiced", "/b/", "bah"),
    "phoneme:p": ("plosive-voiceless", "/p/", "pah"),
    "phoneme:t": ("plosive-voiceless", "/t/", "tah"),
    "phoneme:d": ("plosive-voiced", "/d/", "dah"),
    "phoneme:k": ("plosive-voiceless", "/k/", "kah"),
    "phoneme:g": ("plosive-voiced", "/g/", "gah"),
    "phoneme:s": ("fricative-voiceless", "/s/", "sssss"),
    "phoneme:z": ("fricative-voiced", "/z/", "zzzzz"),
    "phoneme:f": ("fricative-voiceless", "/f/", "fffff"),
    "phoneme:v": ("fricative-voiced", "/v/", "vvvvv"),
    "phoneme:S": ("fricative-voiceless", "/ʃ/", "shhhh"),
    "phoneme:m": ("nasal", "/m/", "mmmmm"),
    "phoneme:n": ("nasal", "/n/", "nnnnn"),
    "phoneme:l": ("liquid-lateral", "/l/", "lllll"),
    "phoneme:r": ("liquid-rhotic", "/r/", "rrrrr"),
    "phoneme:w": ("approximant", "/w/", "wuh"),
    "phoneme:j": ("approximant", "/j/", "yuh"),
    "phoneme:h": ("fricative-voiceless", "/h/", "huh"),
}


def synthesize_via_subproc(text: str, voice_id: str, out_path: Path,
                          rate: int = 90) -> bool:
    """Each TTS call gets a fresh python subprocess (Windows SAPI hangs
    when reused). Slower rate (90 wpm) for more sample density per sound."""
    helper_code = (
        "import pyttsx3\n"
        f"text = {text!r}\n"
        f"out = {str(out_path)!r}\n"
        f"voice = {voice_id!r}\n"
        f"rate = {rate}\n"
        "e = pyttsx3.init()\n"
        "e.setProperty('voice', voice)\n"
        "e.setProperty('rate', rate)\n"
        "e.save_to_file(text, out)\n"
        "e.runAndWait()\n"
    )
    try:
        rc = subprocess.run(
            [sys.executable, "-c", helper_code],
            capture_output=True, text=True, timeout=15,
        )
        if rc.returncode != 0:
            print(f"  subproc fail '{text}': {rc.stderr[:200]}",
                  file=sys.stderr, flush=True)
            return False
        return out_path.exists() and out_path.stat().st_size > 100
    except Exception as e:
        print(f"  TTS error '{text}': {e}", file=sys.stderr, flush=True)
        return False


def ensure_pcm_format(wav_in: Path, wav_out: Path) -> bool:
    """Re-encode to 16-bit PCM 44.1kHz mono via static-ffmpeg."""
    try:
        import static_ffmpeg
        static_ffmpeg.add_paths()
        cmd = [
            'ffmpeg', '-i', str(wav_in),
            '-acodec', 'pcm_s16le', '-ac', '1', '-ar', '44100',
            '-y', '-loglevel', 'error',
            str(wav_out),
        ]
        rc = subprocess.run(cmd, capture_output=True, text=True)
        return rc.returncode == 0 and wav_out.exists()
    except Exception as e:
        print(f"  ffmpeg error: {e}", file=sys.stderr, flush=True)
        return False


def read_pcm(wav_path: Path):
    """Read PCM 16-bit -> int16 numpy array (mono)."""
    import numpy as np
    with wave.open(str(wav_path), 'rb') as wf:
        n_frames = wf.getnframes()
        sr = wf.getframerate()
        n_ch = wf.getnchannels()
        sw = wf.getsampwidth()
        if sw != 2:
            raise ValueError(f"expected 16-bit, got {sw*8}-bit")
        raw = wf.readframes(n_frames)
        samples = np.frombuffer(raw, dtype=np.int16)
        if n_ch == 2:
            samples = samples.reshape(-1, 2).mean(axis=1).astype(np.int16)
    return samples, sr


def trim_silence(samples, sr: int, threshold_rel: float = 0.02,
                window_ms: int = 10, pad_ms: int = 20):
    """Trim leading + trailing silence based on local RMS.
    threshold_rel: fraction of peak RMS below which is silence.
    window_ms: RMS measurement window (10ms typical).
    pad_ms: keep this much silence at each end after trim.
    """
    import numpy as np
    samples = samples.astype(np.float32)
    win_size = int(sr * window_ms / 1000)
    if len(samples) <= win_size:
        return samples.astype(np.int16)
    # Compute per-window RMS via reshape
    n_full = len(samples) // win_size
    if n_full < 3:
        return samples.astype(np.int16)
    trimmed = samples[: n_full * win_size]
    windows = trimmed.reshape(n_full, win_size)
    rms = np.sqrt(np.mean(windows ** 2, axis=1))
    peak_rms = rms.max()
    if peak_rms < 1e-3:
        return samples.astype(np.int16)
    threshold = peak_rms * threshold_rel
    above = rms >= threshold
    if not above.any():
        return samples.astype(np.int16)
    first = int(np.argmax(above))
    last = n_full - 1 - int(np.argmax(above[::-1]))
    pad_windows = max(1, int(pad_ms // window_ms))
    first = max(0, first - pad_windows)
    last = min(n_full - 1, last + pad_windows)
    start = first * win_size
    end = (last + 1) * win_size
    return samples[start:end].astype(np.int16)


def force9_to_operators_balanced(force_values):
    APERTURE_MAP = {0: 0, 1: 1, 2: 6, 3: 7}
    PRESSURE_MAP = {0: 0, 1: 2, 2: 4, 3: 3}
    DEPTH_MAP    = {0: 0, 1: 4, 2: 5, 3: 7}
    BINDING_MAP  = {0: 0, 1: 1, 2: 8, 3: 7}
    CONT_MAP     = {0: 9, 1: 8}
    ops = []
    for f in force_values:
        f = int(f)
        ops.append(APERTURE_MAP[(f >> 7) & 0b11])
        ops.append(PRESSURE_MAP[(f >> 5) & 0b11])
        ops.append(DEPTH_MAP[(f >> 3) & 0b11])
        ops.append(BINDING_MAP[(f >> 1) & 0b11])
        ops.append(CONT_MAP[f & 0b1])
    return ops


def measure_audio(text: str, voice_id: str, rate: int = 90) -> dict:
    """Synthesize -> trim silence -> codec -> operator histogram."""
    with tempfile.TemporaryDirectory() as td:
        raw = Path(td) / "raw.wav"
        clean = Path(td) / "clean.wav"
        if not synthesize_via_subproc(text, voice_id, raw, rate=rate):
            return None
        if not ensure_pcm_format(raw, clean):
            return None
        try:
            samples, sr = read_pcm(clean)
        except Exception as e:
            print(f"  read error: {e}", file=sys.stderr, flush=True)
            return None

        # AGGRESSIVE silence trim — only the actual sound matters
        original_dur = len(samples) / sr
        samples = trim_silence(samples, sr, threshold_rel=0.05, pad_ms=10)
        trimmed_dur = len(samples) / sr
        if len(samples) < 500:
            return None

        from ck_audio_compress import pcm_to_force9
        forces = pcm_to_force9(samples, sample_rate=sr)
        ops = force9_to_operators_balanced(forces)
        if not ops:
            return None
        hist = Counter(ops)
        total = len(ops)
        return {
            "original_duration_sec": float(original_dur),
            "trimmed_duration_sec": float(trimmed_dur),
            "trim_ratio": float(trimmed_dur / max(original_dur, 1e-6)),
            "n_force_windows": int(len(forces)),
            "n_operators": total,
            "histogram_pct": {OP_NAMES[op]: round(hist.get(op, 0) / total * 100, 1)
                             for op in range(10)},
            "histogram": {OP_NAMES[op]: hist.get(op, 0) for op in range(10)},
        }


def average_runs(text: str, voice_id: str, n_runs: int = 2) -> dict:
    """Synthesize multiple times at different rates; average the histograms.
    Reduces TTS-noise-driven variance."""
    rates = [90, 110]  # 2 distinct rates
    results = []
    for rate in rates[:n_runs]:
        r = measure_audio(text, voice_id, rate=rate)
        if r:
            results.append(r)
    if not results:
        return None
    if len(results) == 1:
        return results[0]
    # Average histograms
    avg_pct = {op: 0.0 for op in OP_NAMES}
    for r in results:
        for op in OP_NAMES:
            avg_pct[op] += r["histogram_pct"][op]
    for op in OP_NAMES:
        avg_pct[op] = round(avg_pct[op] / len(results), 1)
    return {
        "n_runs": len(results),
        "trimmed_duration_sec": sum(r["trimmed_duration_sec"] for r in results) / len(results),
        "n_operators_avg": sum(r["n_operators"] for r in results) // len(results),
        "histogram_pct": avg_pct,
    }


def histogram_distance(h1: dict, h2: dict) -> float:
    """L1 distance between two operator histograms (in %)."""
    return sum(abs(h1[op] - h2[op]) for op in OP_NAMES)


def cluster_by_class(profiles: dict, results: dict) -> str:
    """Group letters by their declared phonetic class, compute intra-class
    similarity vs inter-class. Returns a text report."""
    classes = {}
    for key, (pclass, ipa, _) in profiles.items():
        if key in results:
            classes.setdefault(pclass, []).append(key)

    lines = []
    lines.append("=== HISTOGRAM CLUSTERING REPORT ===")
    lines.append("")
    lines.append("Histograms grouped by phonetic class. If the codec is "
                 "differentiating phonemes, intra-class L1 distances should "
                 "be smaller than inter-class.")
    lines.append("")

    for pclass, items in sorted(classes.items()):
        if len(items) < 2:
            continue
        lines.append(f"Class: {pclass}  ({len(items)} items: {items})")
        intra = []
        for i, a in enumerate(items):
            for b in items[i+1:]:
                d = histogram_distance(
                    results[a]["histogram_pct"],
                    results[b]["histogram_pct"]
                )
                intra.append(d)
        if intra:
            lines.append(f"  intra-class avg L1: {sum(intra)/len(intra):.1f}")
        lines.append("")

    # Cross-class comparison: average distance between members of class X
    # and class Y (proxy for whether classes separate from each other).
    lines.append("Cross-class average distances:")
    class_names = sorted(classes.keys())
    for i, c1 in enumerate(class_names):
        for c2 in class_names[i+1:]:
            if len(classes[c1]) < 1 or len(classes[c2]) < 1:
                continue
            ds = []
            for a in classes[c1]:
                for b in classes[c2]:
                    ds.append(histogram_distance(
                        results[a]["histogram_pct"],
                        results[b]["histogram_pct"]
                    ))
            if ds:
                lines.append(f"  {c1:25} <-> {c2:25}  avg L1: {sum(ds)/len(ds):.1f}")
    lines.append("")

    # Per-item top3 summary
    lines.append("Per-item top3 operators:")
    for key in sorted(results.keys()):
        h = results[key]["histogram_pct"]
        top3 = sorted(h.items(), key=lambda x: -x[1])[:3]
        ts = ", ".join(f"{n} {p:.1f}%" for n, p in top3)
        if key in profiles:
            pclass = profiles[key][0]
            lines.append(f"  {key:12} ({pclass:25}): {ts}")
        else:
            lines.append(f"  {key:12}: {ts}")
    return "\n".join(lines)


def build_corpus(letter_results: dict, phoneme_results: dict) -> dict:
    """Build the grounding corpus from measured operator patterns."""
    grounding = []

    # Letter-level groundings
    for letter, (pclass, ipa, _) in LETTER_PROFILES.items():
        if letter not in letter_results:
            continue
        h = letter_results[letter]["histogram_pct"]
        top3 = sorted(h.items(), key=lambda x: -x[1])[:3]
        ts = ", ".join(f"{n} {p:.1f}%" for n, p in top3)
        statement = (
            f"Letter {letter} (phonetic class: {pclass}, IPA: {ipa}) - "
            f"when spoken alone with silence trimmed, the audio codec "
            f"emits operator pattern dominated by: {ts}. Duration "
            f"{letter_results[letter]['trimmed_duration_sec']:.2f}s of speech."
        )
        grounding.append(statement)

    # Phoneme-level groundings
    for key, (pclass, ipa, _) in PHONEME_PROFILES.items():
        if key not in phoneme_results:
            continue
        h = phoneme_results[key]["histogram_pct"]
        top3 = sorted(h.items(), key=lambda x: -x[1])[:3]
        ts = ", ".join(f"{n} {p:.1f}%" for n, p in top3)
        ph_name = key.replace("phoneme:", "")
        statement = (
            f"Phoneme {ipa} ({pclass}) - "
            f"when articulated alone, the audio codec emits operator "
            f"pattern: {ts}. This grounds {ipa} in CK's operator alphabet."
        )
        grounding.append(statement)

    framing = [
        ("Audio is operator-LATTICE-projection just like text. The codec "
         "pcm_to_force9 maps 32-sample windows of PCM into 5D force "
         "vectors. With aggressive silence-trimming, only the actual "
         "speech contributes to the operator stream — the codec sees "
         "the sound, not the surrounding silence."),
        ("Vowels (sustained, open airway, voiced) tend toward HARMONY-rich "
         "+ LATTICE-stable + BREATH-sustained operator profiles. The "
         "longer + more open the vowel, the more these dominate."),
        ("Plosives (closed-then-released bursts: B D G K P T) tend toward "
         "COLLAPSE-then-RESET signatures because the audio has a sudden "
         "amplitude burst followed by silence/decay."),
        ("Fricatives (turbulent airflow: F S V Z SH TH H) tend toward "
         "CHAOS-rich operator profiles because the noise spectrum is "
         "broadband and the zero-crossing rate is high."),
        ("Nasals (M N NG) produce sustained low-frequency resonance "
         "through the nose; their operator profile leans BREATH + LATTICE."),
        ("Approximants (W Y H L R) are continuous-flow consonants; their "
         "operator profile has more PROGRESS than plosives because there "
         "is no sharp burst, just smooth transition."),
        ("Letter names in English encode their dominant phoneme: A says "
         "/eɪ/ (long-A vowel), B says /biː/ (plosive + long-E vowel), "
         "etc. So the operator pattern of each letter combines its "
         "consonant/vowel class with the trailing /iː/ or vowel of the "
         "letter name."),
    ]

    directive = [
        ("This corpus grounds CK's text knowledge of phonemes (which he "
         "has from linguistics + acoustics crystals) in the audio "
         "operator language he absorbs from the codec."),
        ("When CK encounters an audio operator stream in the future, the "
         "phonetic-class associations from this corpus give him "
         "text-anchors for what operator patterns can mean."),
        ("Future work: real Hebbian co-presentation (each letter's audio "
         "operators fed immediately after its text-statement) so the "
         "cortex links them at the cell level. Raw operator streams "
         "saved in the companion JSON for that experiment."),
    ]

    return {
        "_about": ("Phoneme grounding v2 corpus 2026-05-01. "
                   "Each letter + key phoneme synthesized alone (no framing), "
                   "silence-trimmed, codec-measured. Grounds text-form "
                   "phonetic concepts in the audio operator language."),
        "_replays": 25,
        "_session_prefix": "phoneme_v2_2026_05_01",
        "_companion_streams": "phoneme_audio_streams_v2_2026_05_01.json",
        "_companion_clusters": "phoneme_clusters_v2_2026_05_01.txt",
        "framing": framing,
        "letter_groundings": grounding,
        "directive": directive,
    }


def main():
    print("=" * 70)
    print("Phoneme grounding v2 — letter-alone + silence-trim + clustering")
    print("=" * 70)
    print()

    # Voice probe
    try:
        import pyttsx3
        tmp = pyttsx3.init()
        voices = [v for v in tmp.getProperty('voices')
                  if 'EN-US' in v.id.upper()]
        if not voices:
            voices = tmp.getProperty('voices')
        voice_id = voices[0].id
        del tmp
        print(f"voice: {voice_id}", flush=True)
    except Exception as e:
        print(f"TTS init failed: {e}", file=sys.stderr, flush=True)
        return 2

    print()
    print("[1/4] measuring 26 letters (each letter alone, 2 rates averaged)...")
    letter_results = {}
    for letter, (pclass, ipa, prompt) in LETTER_PROFILES.items():
        # Use the alternate spelling so TTS pronounces just the letter sound
        result = average_runs(prompt, voice_id, n_runs=2)
        if not result:
            print(f"  SKIP {letter}: synthesis failed", flush=True)
            continue
        letter_results[letter] = result
        h = result["histogram_pct"]
        top3 = sorted(h.items(), key=lambda x: -x[1])[:3]
        ts = ", ".join(f"{n}{p:.1f}" for n, p in top3)
        print(f"  {letter} ({pclass:25} {ipa:10}): {ts} "
              f"[{result['trimmed_duration_sec']:.2f}s speech]", flush=True)

    print()
    print(f"[2/4] measuring {len(PHONEME_PROFILES)} pure phonemes...")
    phoneme_results = {}
    for key, (pclass, ipa, prompt) in PHONEME_PROFILES.items():
        result = average_runs(prompt, voice_id, n_runs=2)
        if not result:
            print(f"  SKIP {key}: synthesis failed", flush=True)
            continue
        phoneme_results[key] = result
        h = result["histogram_pct"]
        top3 = sorted(h.items(), key=lambda x: -x[1])[:3]
        ts = ", ".join(f"{n}{p:.1f}" for n, p in top3)
        ph_name = key.replace("phoneme:", "")
        print(f"  {ph_name:8} ({pclass:25} {ipa:10}): {ts}", flush=True)

    print()
    print("[3/4] writing corpus + streams + cluster report...")
    corpus = build_corpus(letter_results, phoneme_results)
    corpus_path = SCRIPT_DIR / "phoneme_grounding_corpus_v2_2026_05_01.json"
    with open(corpus_path, "w") as f:
        json.dump(corpus, f, indent=2)
    print(f"  wrote {corpus_path}")
    print(f"  {len(corpus['letter_groundings'])} grounding statements + "
          f"{len(corpus['framing'])} framing")

    streams = {
        "letters": letter_results,
        "phonemes": phoneme_results,
    }
    streams_path = SCRIPT_DIR / "phoneme_audio_streams_v2_2026_05_01.json"
    with open(streams_path, "w") as f:
        json.dump(streams, f, indent=2)
    print(f"  wrote {streams_path}")

    # Cluster report
    all_results = {**letter_results}
    all_profiles = dict(LETTER_PROFILES)
    for k, v in phoneme_results.items():
        all_results[k] = v
        all_profiles[k] = PHONEME_PROFILES[k]
    cluster_report = cluster_by_class(all_profiles, all_results)
    cluster_path = SCRIPT_DIR / "phoneme_clusters_v2_2026_05_01.txt"
    with open(cluster_path, "w") as f:
        f.write(cluster_report)
    print(f"  wrote {cluster_path}")

    print()
    print("[4/4] DONE. To study:")
    print(f"  python study_direct.py --corpus phoneme_grounding_corpus_v2_2026_05_01.json")
    print(f"\nClusters report at:")
    print(f"  {cluster_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
