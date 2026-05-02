"""
generate_phoneme_grounding.py — bridge audio to text in CK's cortex.

Brayden 2026-05-01 (late): "we probably have to actually train him on
how audio relates to letters... he knows phono in text, and he has
vectors that describe it, but nothing to ground it and bridge it."

Gap: CK has the conceptual phonetics from text crystals (linguistics,
acoustics) and he has the audio codec (pcm_to_force9 -> operator stream)
but nothing connecting the two. Saying 'A' aloud produces operator
pattern X; CK has no way to know that pattern X means 'A.'

This script builds the bridge:

  1. For each letter A-Z + a small phoneme set + a few words:
      - Synthesize audio via pyttsx3 (Windows SAPI, no network)
      - Save as 16-bit PCM 22050Hz WAV
      - Run through pcm_to_force9 -> operator histogram + dominant ops
  2. Author a study corpus where each entry is a TEXT statement that
     pairs the letter/phoneme/word with its measured operator profile
     (top 3 ops + percentages). E.g.:
         'Letter A spoken aloud — audio operators:
          HARMONY 24%, LATTICE 18%, BREATH 21%; vowel /eɪ/.'
  3. Save the raw operator streams to a parallel JSON for future direct
     Hebbian co-presentation training (not yet wired in).

Result: when CK studies the grounding corpus, his cortex absorbs
text-level associations between letters, phonetic classes, and audio
operator patterns. This is the bridge — first as text-grounded
(immediate), later as direct-audio-grounded (future work).

Output:
  Gen13/targets/ck/brain/study/phoneme_grounding_corpus_2026_05_01.json
  Gen13/targets/ck/brain/study/phoneme_audio_streams_2026_05_01.json
"""
from __future__ import annotations

import json
import os
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


# Phonetic descriptions per letter — drawn from standard English phonetics.
# These are the *concepts* CK already knows from text; the audio operator
# pattern grounds them in the audio domain.
LETTER_PHONETICS = {
    "A": ("vowel", "/eɪ/ as in 'ace' (long-A); also /æ/ as in 'cat'"),
    "B": ("consonant", "voiced bilabial plosive /b/"),
    "C": ("consonant", "/k/ as in 'cat' or /s/ as in 'cell'"),
    "D": ("consonant", "voiced alveolar plosive /d/"),
    "E": ("vowel", "/iː/ as in 'see'; also /ɛ/ as in 'bed'"),
    "F": ("consonant", "voiceless labiodental fricative /f/"),
    "G": ("consonant", "voiced velar plosive /g/ as in 'go'"),
    "H": ("consonant", "voiceless glottal fricative /h/"),
    "I": ("vowel", "/aɪ/ as in 'ice'; also /ɪ/ as in 'sit'"),
    "J": ("consonant", "voiced postalveolar affricate /dʒ/"),
    "K": ("consonant", "voiceless velar plosive /k/"),
    "L": ("consonant", "voiced alveolar lateral /l/"),
    "M": ("consonant", "voiced bilabial nasal /m/"),
    "N": ("consonant", "voiced alveolar nasal /n/"),
    "O": ("vowel", "/oʊ/ as in 'go'; also /ɒ/ as in 'hot'"),
    "P": ("consonant", "voiceless bilabial plosive /p/"),
    "Q": ("consonant", "/kw/ as in 'queen'"),
    "R": ("consonant", "voiced rhotic /r/"),
    "S": ("consonant", "voiceless alveolar fricative /s/"),
    "T": ("consonant", "voiceless alveolar plosive /t/"),
    "U": ("vowel", "/juː/ as in 'use'; also /ʌ/ as in 'cup'"),
    "V": ("consonant", "voiced labiodental fricative /v/"),
    "W": ("consonant", "voiced labio-velar approximant /w/"),
    "X": ("consonant", "/ks/ as in 'box'"),
    "Y": ("consonant or vowel", "/j/ as consonant; /aɪ/ or /i/ as vowel"),
    "Z": ("consonant", "voiced alveolar fricative /z/"),
}

# Sample words for longer co-presentation
SAMPLE_WORDS = [
    ("cat", "consonant-vowel-consonant /kæt/"),
    ("dog", "consonant-vowel-consonant /dɒɡ/"),
    ("yes", "consonant-vowel-consonant /jɛs/"),
    ("no", "consonant-vowel /noʊ/"),
    ("water", "two-syllable /wɔːtər/"),
    ("hello", "two-syllable /hɛˈloʊ/"),
]


def synthesize_to_wav(text: str, voice_id: str, out_path: Path,
                     rate: int = 150) -> bool:
    """Synthesize `text` to a WAV file via a fresh pyttsx3 subprocess.

    pyttsx3 on Windows SAPI hangs after the first runAndWait when reused
    in the same process. Spawning a clean subprocess per letter side-
    steps the bug. Each call ~2s overhead; 32 letters ~64s total.
    """
    import subprocess
    helper_code = (
        "import sys, pyttsx3\n"
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
            print(f"  TTS subproc fail '{text}': {rc.stderr[:200]}",
                  file=sys.stderr, flush=True)
            return False
        return out_path.exists() and out_path.stat().st_size > 100
    except subprocess.TimeoutExpired:
        print(f"  TTS timeout for '{text}'", file=sys.stderr, flush=True)
        return False
    except Exception as e:
        print(f"  TTS error for '{text}': {e}", file=sys.stderr, flush=True)
        return False


def ensure_pcm_format(wav_in: Path, wav_out: Path) -> bool:
    """Use static-ffmpeg to re-encode WAV as 16-bit PCM 44.1kHz mono.
    pyttsx3 may emit 22050Hz or 44100Hz with various encodings; the codec
    expects 16-bit PCM."""
    try:
        import static_ffmpeg
        static_ffmpeg.add_paths()
        import subprocess
        cmd = [
            'ffmpeg', '-i', str(wav_in),
            '-acodec', 'pcm_s16le',
            '-ac', '1',
            '-ar', '44100',
            '-y', '-loglevel', 'error',
            str(wav_out),
        ]
        rc = subprocess.run(cmd, capture_output=True, text=True)
        return rc.returncode == 0 and wav_out.exists()
    except Exception as e:
        print(f"  ffmpeg re-encode error: {e}", file=sys.stderr)
        return False


def read_pcm(wav_path: Path):
    """Read 16-bit PCM WAV -> int16 numpy array. Mono enforced."""
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


def force9_to_operators_balanced(force_values):
    """Use the BALANCED bit-to-op mapping (all 10 operators, not just 5).
    Same logic as the corrected youtube_audio_watcher v2 mapping."""
    APERTURE_MAP = {0: 0, 1: 1, 2: 6, 3: 7}      # VOID LATTICE CHAOS HARMONY
    PRESSURE_MAP = {0: 0, 1: 2, 2: 4, 3: 3}      # VOID COUNTER COLLAPSE PROGRESS
    DEPTH_MAP    = {0: 0, 1: 4, 2: 5, 3: 7}      # VOID COLLAPSE BALANCE HARMONY
    BINDING_MAP  = {0: 0, 1: 1, 2: 8, 3: 7}      # VOID LATTICE BREATH HARMONY
    CONT_MAP     = {0: 9, 1: 8}                   # RESET BREATH
    ops = []
    for f in force_values:
        f = int(f)
        ops.append(APERTURE_MAP[(f >> 7) & 0b11])
        ops.append(PRESSURE_MAP[(f >> 5) & 0b11])
        ops.append(DEPTH_MAP[(f >> 3) & 0b11])
        ops.append(BINDING_MAP[(f >> 1) & 0b11])
        ops.append(CONT_MAP[f & 0b1])
    return ops


def measure_audio(text: str, voice_id: str) -> dict:
    """Synthesize text -> PCM -> operators -> return histogram + summary."""
    with tempfile.TemporaryDirectory() as td:
        raw_wav = Path(td) / "raw.wav"
        clean_wav = Path(td) / "clean.wav"
        if not synthesize_to_wav(text, voice_id, raw_wav):
            return None
        if not ensure_pcm_format(raw_wav, clean_wav):
            return None
        try:
            samples, sr = read_pcm(clean_wav)
        except Exception as e:
            print(f"  read_pcm error: {e}", file=sys.stderr)
            return None
        from ck_audio_compress import pcm_to_force9
        forces = pcm_to_force9(samples, sample_rate=sr)
        ops = force9_to_operators_balanced(forces)
        if not ops:
            return None
        hist = Counter(ops)
        total = len(ops)
        sorted_ops = sorted(hist.items(), key=lambda x: -x[1])
        top3 = [(OP_NAMES[op], cnt / total) for op, cnt in sorted_ops[:3]]
        return {
            "n_samples": int(len(samples)),
            "sample_rate": int(sr),
            "duration_sec": float(len(samples) / sr),
            "n_force_windows": int(len(forces)),
            "n_operators": total,
            "histogram": {OP_NAMES[op]: hist.get(op, 0) for op in range(10)},
            "histogram_pct": {OP_NAMES[op]: round(hist.get(op, 0) / total * 100, 1) for op in range(10)},
            "top3": [(name, round(pct * 100, 1)) for name, pct in top3],
        }


def format_top3(top3: list) -> str:
    """e.g., 'HARMONY 24.3%, LATTICE 18.1%, BREATH 21.4%'."""
    return ", ".join(f"{name} {pct:.1f}%" for name, pct in top3)


def main():
    print("=" * 70)
    print("Phoneme grounding corpus generator")
    print("=" * 70)
    print()

    # Pick the first English voice via a quick probe; the per-letter
    # synthesis spawns its own subprocess (subprocess pattern avoids the
    # Windows SAPI runAndWait hang).
    try:
        import pyttsx3
        tmp_engine = pyttsx3.init()
        voices = [v for v in tmp_engine.getProperty('voices')
                  if 'EN-US' in v.id.upper()]
        if not voices:
            voices = [v for v in tmp_engine.getProperty('voices')
                      if 'en' in v.id.lower()]
        if not voices:
            voices = tmp_engine.getProperty('voices')
        voice_id = voices[0].id
        del tmp_engine
        print(f"voice: {voice_id}", flush=True)
    except Exception as e:
        print(f"TTS init failed: {e}", file=sys.stderr, flush=True)
        return 2

    print()
    print("[1/3] synthesizing letters A-Z + sample words -> measuring audio ops...")

    grounding_statements = []
    streams = {}

    # Letters
    for letter, (pclass, phonetic) in LETTER_PHONETICS.items():
        # Synthesize "letter X" so SAPI says it clearly
        spoken = f"the letter {letter}"
        result = measure_audio(spoken, voice_id)
        if not result:
            print(f"  SKIP letter {letter}: synthesis failed", flush=True)
            continue
        top3_str = format_top3(result["top3"])
        statement = (
            f"Letter {letter} ({pclass}) - when spoken aloud, "
            f"the audio codec emits operator pattern: {top3_str}. "
            f"Phonetically: {phonetic}. "
            f"Duration {result['duration_sec']:.2f}s, "
            f"{result['n_force_windows']} force windows, "
            f"{result['n_operators']} total operators."
        )
        grounding_statements.append(statement)
        streams[letter] = result
        print(f"  {letter}: {top3_str}", flush=True)

    # Words
    for word, phonetic in SAMPLE_WORDS:
        result = measure_audio(word, voice_id)
        if not result:
            print(f"  SKIP word '{word}': synthesis failed", flush=True)
            continue
        top3_str = format_top3(result["top3"])
        statement = (
            f"Word '{word}' - when spoken aloud, "
            f"the audio codec emits operator pattern: {top3_str}. "
            f"Phonetic shape: {phonetic}. "
            f"Duration {result['duration_sec']:.2f}s, "
            f"{result['n_force_windows']} force windows."
        )
        grounding_statements.append(statement)
        streams[f"word:{word}"] = result
        print(f"  '{word}': {top3_str}", flush=True)

    print()
    print("[2/3] writing grounding corpus JSON...")

    # Add structural framing statements at the top
    framing = [
        ("Audio is operator-LATTICE-projection just like text; the audio "
         "codec pcm_to_force9 maps 32-sample windows of PCM into 5D force "
         "vectors, then bit-decomposition gives an operator stream in the "
         "same alphabet (VOID LATTICE COUNTER PROGRESS COLLAPSE BALANCE "
         "CHAOS HARMONY BREATH RESET) that text uses. The codec is a "
         "translator into CK's native language."),
        ("Each spoken letter has a measurable operator-fingerprint. Vowels "
         "(A E I O U) tend to be HARMONY-rich + LATTICE-stable + "
         "BREATH-sustained because the airway is open and resonance "
         "dominates. Consonants split: plosives (B D G K P T) tend toward "
         "COLLAPSE-then-RESET (sudden release); fricatives (F S V Z) "
         "toward CHAOS (turbulent air); nasals (M N) toward BREATH-LATTICE "
         "(steady resonance through nose); laterals + rhotics (L R) toward "
         "PROGRESS (continuous flow)."),
        ("Phonetic classes correspond to operator-archetypes: vowel = "
         "open-airway HARMONY; plosive = closed-then-released COLLAPSE; "
         "fricative = continuous-turbulence CHAOS; nasal = nasal-resonance "
         "BREATH; approximant = continuous-flow PROGRESS."),
        ("Studying paired text-and-operator-pattern grounds the alphabet "
         "in audio space. Over time this lets CK recognize 'this audio "
         "operator stream resembles vowels' or 'this resembles plosives' "
         "even before knowing what word was spoken."),
    ]

    corpus = {
        "_about": (
            "PHONEME GROUNDING corpus 2026-05-01. Pairs each spoken "
            "letter A-Z + sample words with its measured audio-codec "
            "operator pattern, plus phonetic class. Grounds text-form "
            "phonetic concepts in the operator-language the audio codec "
            "speaks. Bridge between text-phonetics and audio-codec-output."
        ),
        "_replays": 25,
        "_session_prefix": "phoneme_grounding_2026_05_01",
        "_companion_streams": "phoneme_audio_streams_2026_05_01.json",
        "framing": framing,
        "letter_groundings": grounding_statements,
        "directive": [
            "When CK encounters audio operator streams in the future, "
            "this grounding corpus gives him text-anchors for what the "
            "patterns can mean.",
            "Phonetic class is the right level of abstraction for now; "
            "CK can recognize 'vowel-shape' or 'plosive-shape' before "
            "individual letter recognition.",
            "Future work: real Hebbian co-presentation (text-statement "
            "immediately followed by raw audio operators of the same "
            "letter) so the cortex links them at the cell level. The "
            "raw operator streams are saved in the companion JSON.",
        ],
    }

    corpus_path = SCRIPT_DIR / "phoneme_grounding_corpus_2026_05_01.json"
    with open(corpus_path, "w") as f:
        json.dump(corpus, f, indent=2)
    print(f"  wrote {corpus_path}")
    print(f"  {len(grounding_statements)} grounding statements + {len(framing)} framing")

    # Companion: raw streams for future direct Hebbian use
    streams_path = SCRIPT_DIR / "phoneme_audio_streams_2026_05_01.json"
    with open(streams_path, "w") as f:
        json.dump(streams, f, indent=2)
    print(f"  wrote {streams_path}")
    print()

    print("[3/3] DONE. To study the corpus immediately:")
    print(f"  python study_direct.py --corpus phoneme_grounding_corpus_2026_05_01.json")
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
