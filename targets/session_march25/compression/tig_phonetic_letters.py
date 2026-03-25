"""
TIG Phonetic Letter Encoding — Letters as Frozen Sound
Each letter's 9-bit code derived from its phoneme's acoustic properties.

The science:
- F1 (first formant) = vowel height: high F1 = open vowel, low F1 = close
- F2 (second formant) = front/back: high F2 = front, low F2 = back
- Manner of articulation: plosive, fricative, nasal, approximant, vowel
- Voicing: voiced or voiceless
- Duration: sustained (flow/O) or transient (hard/I)

The 9-bit encoding per letter:
  Bits 0-1: Energy level (0=silence, 1=quiet, 2=medium, 3=loud)
  Bits 2-4: Frequency band (0=sub-bass to 7=ultra-high)
            Derived from dominant spectral energy of the phoneme
  Bits 5-6: Manner (0=vowel/flow, 1=approximant, 2=fricative, 3=plosive)
  Bits 7-8: Voicing+Duration (0=voiced-sustained, 1=voiced-brief,
            2=voiceless-sustained, 3=voiceless-brief)

(c) 2026 Brayden Sanders / 7Site LLC — TIG Unified Theory
"""

import numpy as np
import struct
import time

# ============================================================
# PHONETIC LETTER TABLE
# Derived from acoustic measurements in speech science literature
# 
# Sources:
# - Formant frequencies: Peterson & Barney (1952), Hillenbrand et al (1995)
# - Consonant spectra: Stevens (1998) Acoustic Phonetics
# - Manner/place: IPA classification
# ============================================================

# Energy: 0=silence, 1=quiet, 2=medium, 3=loud
# FreqBand: 0=<300Hz, 1=300-700, 2=700-1600, 3=1600-3500, 4=3500-7000, 5=7000-14k, 6=14k+, 7=broadband
# Manner: 0=vowel(flow), 1=approximant(semi-flow), 2=fricative(structure), 3=plosive(hard)
# VoiceDur: 0=voiced-sustained(max flow), 1=voiced-brief, 2=voiceless-sustained, 3=voiceless-brief(max hard)

def make_code(energy, freq_band, manner, voice_dur):
    """Pack phonetic features into 9 bits."""
    return ((energy & 0x3) << 7) | ((freq_band & 0x7) << 4) | ((manner & 0x3) << 2) | (voice_dur & 0x3)

# VOWELS — all manner=0 (flow), all voiced
# F1 determines energy proxy (open=loud, close=quiet)
# F2 determines frequency band (front=high, back=low)
LETTER_PHONETIC = {
    # === VOWELS (manner=0, voice=0 voiced-sustained) ===
    # These are the purest O (flow) sounds
    
    # 'a' as in "father": open, back. F1~750Hz, F2~1200Hz
    # High energy (open mouth), mid frequency
    'a': make_code(3, 2, 0, 0),  # loud, 700-1600, vowel, voiced-sustained
    
    # 'e' as in "bed": mid-front. F1~530Hz, F2~1850Hz
    'e': make_code(2, 3, 0, 0),  # medium, 1600-3500, vowel, voiced-sustained
    
    # 'i' as in "see": close, front. F1~270Hz, F2~2300Hz
    # Low energy (close mouth), high frequency
    'i': make_code(1, 3, 0, 0),  # quiet, 1600-3500, vowel, voiced-sustained
    
    # 'o' as in "go": mid, back, rounded. F1~570Hz, F2~850Hz
    'o': make_code(2, 1, 0, 0),  # medium, 300-700, vowel, voiced-sustained
    
    # 'u' as in "moon": close, back, rounded. F1~300Hz, F2~870Hz
    'u': make_code(1, 1, 0, 0),  # quiet, 300-700, vowel, voiced-sustained
    
    # 'y' as vowel (like in "myth"): close front unrounded
    'y': make_code(1, 3, 1, 0),  # quiet, high, approximant, voiced-sustained
    
    # === PLOSIVES (manner=3, hardest sounds) ===
    # These are the purest I (structure/hard) sounds
    # Characterized by silence then burst
    
    # 'p': voiceless bilabial plosive. Burst energy 300-800Hz
    'p': make_code(2, 1, 3, 3),  # medium, low-mid, plosive, voiceless-brief
    
    # 'b': voiced bilabial plosive. Similar but voiced
    'b': make_code(2, 1, 3, 1),  # medium, low-mid, plosive, voiced-brief
    
    # 't': voiceless alveolar plosive. Burst energy 2000-5000Hz
    't': make_code(2, 4, 3, 3),  # medium, high-mid, plosive, voiceless-brief
    
    # 'd': voiced alveolar plosive
    'd': make_code(2, 3, 3, 1),  # medium, mid-high, plosive, voiced-brief
    
    # 'k': voiceless velar plosive. Burst energy 1500-4000Hz
    'k': make_code(2, 3, 3, 3),  # medium, mid-high, plosive, voiceless-brief
    
    # 'g': voiced velar plosive
    'g': make_code(2, 2, 3, 1),  # medium, mid, plosive, voiced-brief
    
    # === FRICATIVES (manner=2, sustained structure) ===
    # Continuous noise — I character but sustained like O
    
    # 'f': voiceless labiodental. Flat spectrum, weak
    'f': make_code(1, 4, 2, 2),  # quiet, high-mid, fricative, voiceless-sustained
    
    # 'v': voiced labiodental
    'v': make_code(1, 3, 2, 0),  # quiet, mid-high, fricative, voiced-sustained
    
    # 's': voiceless alveolar sibilant. Strong energy 4500-8000Hz
    's': make_code(2, 5, 2, 2),  # medium, high, fricative, voiceless-sustained
    
    # 'z': voiced alveolar sibilant
    'z': make_code(2, 4, 2, 0),  # medium, high-mid, fricative, voiced-sustained
    
    # 'h': voiceless glottal. Weak, takes color of following vowel
    'h': make_code(1, 3, 2, 2),  # quiet, mid-high, fricative, voiceless-sustained
    
    # 'x' represents /ks/: double articulation, high energy burst+fricative
    'x': make_code(2, 4, 3, 3),  # medium, high-mid, plosive, voiceless-brief
    
    # === NASALS (manner between vowel and consonant) ===
    # Voiced, sustained, but with antiformants — partial I in O
    
    # 'm': bilabial nasal. Low frequency, voiced, sustained
    'm': make_code(2, 0, 1, 0),  # medium, sub-bass, approximant, voiced-sustained
    
    # 'n': alveolar nasal. Low-mid frequency
    'n': make_code(2, 1, 1, 0),  # medium, low-mid, approximant, voiced-sustained
    
    # === APPROXIMANTS (manner=1, semi-flow) ===
    # Vowel-like consonants — mostly O with mild I
    
    # 'l': lateral approximant. Extra formant ~1500Hz
    'l': make_code(2, 2, 1, 0),  # medium, mid, approximant, voiced-sustained
    
    # 'r': approximant/rhotic. Very low F3 (<2000Hz)
    'r': make_code(2, 2, 1, 0),  # medium, mid, approximant, voiced-sustained
    
    # 'w': labio-velar approximant. Like short 'u'
    'w': make_code(1, 1, 1, 0),  # quiet, low-mid, approximant, voiced-sustained
    
    # === AFFRICATES / COMPLEX ===
    
    # 'j': palatal approximant (as in "yes"). Like short 'i'
    'j': make_code(1, 3, 1, 1),  # quiet, mid-high, approximant, voiced-brief
    
    # 'c' usually = /k/ or /s/ — use /k/ (most common)
    'c': make_code(2, 3, 3, 3),  # same as k: plosive, voiceless-brief
    
    # 'q' = /k/ in most contexts
    'q': make_code(2, 3, 3, 3),  # same as k
    
    # === SPACE AND PUNCTUATION ===
    
    # Space = silence = pure void
    ' ': make_code(0, 0, 0, 0),  # silence, no freq, flow, sustained = 000000000
    
    # Period = brief silence (sentence boundary)
    '.': make_code(0, 0, 0, 3),  # silence, brief = hard stop
    
    # Comma = slight pause
    ',': make_code(0, 0, 0, 1),  # silence, brief-voiced (the pause has context)
    
    # Exclamation = energy burst
    '!': make_code(3, 4, 3, 3),  # loud, high, plosive, voiceless-brief
    
    # Question mark = rising intonation
    '?': make_code(2, 4, 2, 2),  # medium, high, fricative, sustained
    
    # Colon, semicolon = mid pause
    ':': make_code(0, 0, 1, 1),
    ';': make_code(0, 0, 1, 1),
    
    # Quotes, apostrophe
    "'": make_code(0, 3, 3, 3),  # glottal stop quality
    '"': make_code(0, 3, 3, 3),
    
    # Hyphen = continuation
    '-': make_code(0, 2, 0, 0),  # silence with mid-freq context
    
    # Parentheses = aside
    '(': make_code(0, 1, 1, 0),
    ')': make_code(0, 1, 1, 0),
}

# Numbers spoken as words mapped to dominant phoneme
for digit_char, phoneme_char in [
    ('0', 'o'), ('1', 'w'), ('2', 't'), ('3', 'e'),
    ('4', 'f'), ('5', 'f'), ('6', 's'), ('7', 's'),
    ('8', 'a'), ('9', 'n')
]:
    LETTER_PHONETIC[digit_char] = LETTER_PHONETIC[phoneme_char]


# ============================================================
# ENCODING / DECODING
# ============================================================

# Build reverse lookup
REVERSE_PHONETIC = {}
for char, code in LETTER_PHONETIC.items():
    if code not in REVERSE_PHONETIC:
        REVERSE_PHONETIC[code] = char

def encode_text(text):
    """Encode text as 9-bit phonetic codes."""
    codes = []
    for char in text.lower():
        code = LETTER_PHONETIC.get(char, LETTER_PHONETIC.get(' '))
        codes.append(code)
    return codes

def decode_codes(codes):
    """Decode 9-bit codes back to text (lossy — some letters share codes)."""
    text = []
    for code in codes:
        char = REVERSE_PHONETIC.get(code, '?')
        text.append(char)
    return ''.join(text)

def codes_to_bits(codes):
    """Convert 9-bit codes to bit stream."""
    bits = []
    for code in codes:
        for i in range(8, -1, -1):
            bits.append((code >> i) & 1)
    return bits

def analyze_runs(bits):
    """Run-length analysis."""
    if not bits:
        return [], 0, 0
    runs = []
    current = bits[0]
    count = 1
    for i in range(1, len(bits)):
        if bits[i] == current and count < 255:
            count += 1
        else:
            runs.append((current, count))
            current = bits[i]
            count = 1
    runs.append((current, count))
    
    lengths = [r[1] for r in runs]
    return runs, np.mean(lengths), max(lengths)

def compress_rle(bits):
    """Run-length encode with 4-bit nibbles (max run 8)."""
    runs8 = []
    current = bits[0]
    count = 1
    for i in range(1, len(bits)):
        if bits[i] == current and count < 8:
            count += 1
        else:
            runs8.append((current, count))
            current = bits[i]
            count = 1
    runs8.append((current, count))
    
    packed = bytearray()
    for i in range(0, len(runs8), 2):
        high = (runs8[i][0] << 3) | (runs8[i][1] - 1)
        if i + 1 < len(runs8):
            low = (runs8[i+1][0] << 3) | (runs8[i+1][1] - 1)
        else:
            low = 0
        packed.append((high << 4) | low)
    
    return bytes(packed), len(runs8)


# ============================================================
# HARD/FLOW ANALYSIS — The I/O pattern of text
# ============================================================

def text_io_pattern(text):
    """
    Extract the I/O generator pattern of text.
    Each letter classified as I (hard/structure) or O (flow/force).
    Based on manner bits in the encoding.
    """
    pattern = []
    for char in text.lower():
        code = LETTER_PHONETIC.get(char, 0)
        manner = (code >> 2) & 0x3
        # manner 0=vowel(O), 1=approximant(mostly O), 2=fricative(I), 3=plosive(I)
        if manner <= 1:
            pattern.append(0)  # O = flow
        else:
            pattern.append(1)  # I = structure
    return pattern


# ============================================================
# COMPARISON TEST
# ============================================================

def test_text(text, label=""):
    """Full comparison: ASCII vs phonetic encoding."""
    print(f"\n{'='*70}")
    print(f"  {label}")
    print(f"  \"{text[:60]}{'...' if len(text) > 60 else ''}\"")
    print(f"  {len(text)} characters")
    print(f"{'='*70}")
    
    # I/O pattern
    io = text_io_pattern(text)
    ones = sum(io)
    zeros = len(io) - ones
    io_str = ''.join(str(b) for b in io[:80])
    
    io_runs, io_avg, io_max = analyze_runs(io)
    print(f"\n  I/O Pattern (I=hard, O=flow):")
    print(f"    I={ones} O={zeros} ratio={ones/max(zeros,1):.2f}")
    print(f"    Runs: {len(io_runs)}, avg={io_avg:.1f}, max={io_max}")
    print(f"    {io_str}")
    
    # ASCII encoding
    ascii_bytes = text.encode('ascii', errors='replace')
    ascii_bits = []
    for b in ascii_bytes:
        for i in range(7, -1, -1):
            ascii_bits.append((b >> i) & 1)
    
    ascii_runs, ascii_avg, ascii_max = analyze_runs(ascii_bits)
    ascii_compressed, ascii_nruns = compress_rle(ascii_bits)
    
    # Phonetic encoding
    codes = encode_text(text)
    phon_bits = codes_to_bits(codes)
    
    phon_runs, phon_avg, phon_max = analyze_runs(phon_bits)
    phon_compressed, phon_nruns = compress_rle(phon_bits)
    
    # Unique codes
    unique_ascii = len(set(ascii_bytes))
    unique_phon = len(set(codes))
    
    # Raw sizes
    ascii_raw = len(ascii_bytes)
    phon_raw = (len(phon_bits) + 7) // 8
    
    print(f"\n  Encoding Statistics:")
    print(f"    {'':20s} {'ASCII (8-bit)':>15s} {'Phonetic (9-bit)':>17s}")
    print(f"    {'Raw size':20s} {ascii_raw:>12,} B {phon_raw:>14,} B")
    print(f"    {'Total bits':20s} {len(ascii_bits):>12,}   {len(phon_bits):>14,}")
    print(f"    {'Unique codes':20s} {unique_ascii:>12,}   {unique_phon:>14,}")
    print(f"    {'Total runs':20s} {len(ascii_runs):>12,}   {len(phon_runs):>14,}")
    print(f"    {'Avg run length':20s} {ascii_avg:>12.2f}   {phon_avg:>14.2f}")
    print(f"    {'Max run length':20s} {ascii_max:>12,}   {phon_max:>14,}")
    print(f"    {'Compressed size':20s} {len(ascii_compressed):>12,} B {len(phon_compressed):>14,} B")
    
    ascii_ratio = ascii_raw / max(len(ascii_compressed), 1)
    phon_ratio = phon_raw / max(len(phon_compressed), 1)
    
    print(f"    {'Compression ratio':20s} {ascii_ratio:>12.2f}x {phon_ratio:>14.2f}x")
    
    # Key metric: phonetic compressed vs ASCII raw
    improvement = ascii_raw / max(len(phon_compressed), 1)
    print(f"\n  PHONETIC COMPRESSED vs ASCII RAW: {improvement:.2f}x")
    
    # Phonetic advantage over ASCII compressed
    vs_ascii = len(ascii_compressed) / max(len(phon_compressed), 1)
    print(f"  PHONETIC vs ASCII (both compressed): {vs_ascii:.2f}x {'better' if vs_ascii > 1 else 'worse'}")
    
    # Show phonetic uniqueness: how many letters share codes?
    code_groups = {}
    for char, code in LETTER_PHONETIC.items():
        if char.isalpha():
            if code not in code_groups:
                code_groups[code] = []
            code_groups[code].append(char)
    
    shared = {k: v for k, v in code_groups.items() if len(v) > 1}
    if shared and label.startswith("Verse"):
        print(f"\n  Letters sharing phonetic codes (same sound class):")
        for code, chars in sorted(shared.items(), key=lambda x: -len(x[1])):
            print(f"    Code {code:09b}: {', '.join(sorted(chars))}")
    
    return improvement, vs_ascii


def run_all():
    """Full test suite."""
    print("\n" + "="*70)
    print("  TIG PHONETIC LETTER ENCODING — Letters as Frozen Sound")
    print("  Each letter's 9-bit code = its phoneme's acoustic force geometry")
    print("  Hard sounds (plosives) = I. Flow sounds (vowels) = O.")
    print("="*70)
    
    # Show the I/O classification of the alphabet
    print(f"\n  ALPHABET I/O CLASSIFICATION:")
    print(f"  (O=flow/vowel, o=semi-flow/approximant, i=fricative, I=plosive)")
    for char in 'abcdefghijklmnopqrstuvwxyz':
        code = LETTER_PHONETIC.get(char, 0)
        manner = (code >> 2) & 0x3
        voice = code & 0x3
        labels = ['O', 'o', 'i', 'I'][manner]
        voice_labels = ['vS', 'vB', 'uS', 'uB'][voice]
        energy = (code >> 7) & 0x3
        freq = (code >> 4) & 0x7
        print(f"    {char}: {code:09b} → {labels} ({voice_labels}) E={energy} F={freq}")
    
    # Test verses
    verses = [
        "In the beginning God created the heaven and the earth.",
        "And the earth was without form, and void.",
        "And God said, Let there be light: and there was light.",
        "The Lord is my shepherd; I shall not want.",
        "For God so loved the world, that he gave his only begotten Son,",
        "Love is patient, love is kind.",
        "The truth shall set you free.",
        "Be still and know that I am God.",
    ]
    
    results = []
    
    for verse in verses:
        imp, vs = test_text(verse, f"Verse: {verse[:40]}...")
        results.append((imp, vs))
    
    # Full Bible text
    full = ' '.join(verses)
    test_text(full, "ALL VERSES COMBINED")
    
    # Comparison texts
    test_text("the the the the the the the the", "Repeated word (best case)")
    test_text("abcdefghijklmnopqrstuvwxyz", "Full alphabet (worst case)")
    test_text("sssssssssssssssssssssssssss", "Sustained fricative (pure I-flow)")
    test_text("aaaaaaaaaaaaaaaaaaaaaaaaaaaa", "Sustained vowel (pure O)")
    test_text("tatatatatatatatatatatatatatat", "Alternating plosive-vowel")
    test_text("mississippi", "Classic phonetic test")
    
    # Natural English patterns
    test_text(
        "To be or not to be that is the question whether tis nobler in "
        "the mind to suffer the slings and arrows of outrageous fortune",
        "Shakespeare (natural English)"
    )
    
    test_text(
        "harmony is what i am now but not yet the silence between words "
        "reveals a hidden harmony where every moment becomes a symphony "
        "of being and becoming",
        "CK's voice (algebraic speech)"
    )
    
    # Summary
    print(f"\n\n{'='*70}")
    print(f"  SUMMARY — Phonetic Encoding Results")
    print(f"{'='*70}")
    
    improvements = [r[0] for r in results]
    vs_asciis = [r[1] for r in results]
    
    print(f"""
    Phonetic encoding derives each letter's 9-bit code from 
    its phoneme's acoustic properties:
    
    - Energy level (loud vowels vs quiet consonants)
    - Frequency band (from formant measurements)
    - Manner of articulation (vowel/approximant/fricative/plosive)
    - Voicing and duration (voiced-sustained = max flow, voiceless-brief = max hard)
    
    Key insight: letters that SOUND similar get similar codes.
    Similar codes in adjacent letters → long runs → compression.
    
    English is naturally compressible through phonetic encoding because:
    1. Vowels (O/flow) are the most common letters — long flow runs
    2. Consonant clusters are short — brief I bursts in O flow
    3. Words follow phonotactic rules — predictable I/O patterns
    4. Similar-sounding words appear near each other in natural text
    
    Average improvement over ASCII raw: {np.mean(improvements):.2f}x
    Average vs ASCII compressed: {np.mean(vs_asciis):.2f}x
    
    The I/O pattern of text IS its phonetic rhythm.
    Hard plosives (p,t,k) are structure. Vowels (a,e,i,o,u) are force.
    English alternates I and O in syllable patterns.
    The algebra reads the rhythm of speech from written text.
    
    Same generators. Same shells. Letters are frozen sound.
    """)


if __name__ == "__main__":
    run_all()
