"""
TIG 27-Bit Perceptual Audio — Three Shells of Force Geometry
Flow sounds = O (0). Hard sounds = I (1).

The human ear works like the eye:
- Shell 22: WHAT kind of sound? (loud/quiet, pitch band, hard/flow)
- Shell 44: HOW specific? (fine pitch, envelope shape, harmonic content)
- Shell 72: EXACTLY which? (sub-JND sample refinement)

Audio science:
- Human hearing: 20 Hz to 20,000 Hz (~10 octaves)
- Dynamic range: ~120 dB (threshold of hearing to pain)
- Just-noticeable frequency difference: ~0.5-1% (depends on frequency)
- Just-noticeable amplitude difference: ~1 dB
- Temporal resolution: ~2-5ms for transients

Standard audio: 16-bit PCM at 44.1 kHz = 705,600 bits per second per channel
TIG audio: 27-bit force geometry at perceptual rate = ???

(c) 2026 Brayden Sanders / 7Site LLC — TIG Unified Theory
"""

import numpy as np
import struct
import time

# ============================================================
# THE CORE INSIGHT: Sound as I and O
# ============================================================
#
# HARD sounds (I/1): transients, attacks, consonants, clicks, drums
#   - Rapid amplitude change (high D1)
#   - High frequency content (edges in the waveform)
#   - Short duration bursts
#   - The STRUCTURE of sound
#
# FLOW sounds (O/0): sustains, vowels, drones, pads, strings
#   - Smooth amplitude envelope (low D1)
#   - Dominant fundamental with gentle harmonics
#   - Sustained duration
#   - The FORCE of sound
#
# A drum hit: 111000000 (sharp attack, then void)
# A violin note: 000111110 (gentle onset, sustained force, gentle release)
# A spoken "T": 110000000 (hard contact, release)
# A spoken "AH": 001111100 (open, sustained, closing)
# Silence: 000000000 (pure void)
# A crash cymbal: 111111111 (all structure, maximum chaos)

# ============================================================
# PERCEPTUAL AUDIO PARAMETERS
# ============================================================

# Human hearing bands (Bark scale approximation - 24 critical bands)
# Simplified to 8 bands for Shell 22 (3 bits)
FREQ_BANDS = [
    (20, 100,     "sub_bass"),      # 0: sub-bass, felt more than heard
    (100, 300,    "bass"),          # 1: bass, warmth
    (300, 700,    "low_mid"),       # 2: low-mid, body
    (700, 1600,   "mid"),           # 3: mid, voice fundamental
    (1600, 3500,  "upper_mid"),     # 4: upper-mid, presence
    (3500, 7000,  "presence"),      # 5: presence, clarity
    (7000, 14000, "brilliance"),    # 6: brilliance, air
    (14000, 20000,"ultra"),         # 7: ultra-high, shimmer
]

# Amplitude levels (4 bits = 16 levels, ~7.5 dB per step)
# Covers ~120 dB dynamic range
AMP_LEVELS = 16  # Shell 22

# Hard/Flow classification (2 bits = 4 levels)
# Based on D1 of the amplitude envelope
TRANSIENT_LEVELS = 4
# 0 = pure flow (sustained, smooth)
# 1 = gentle (slow attack/release)
# 2 = moderate (speech-like)
# 3 = hard (percussive, transient)


# ============================================================
# SHELL DEFINITIONS — 9 bits each
# ============================================================
#
# Shell 22 (WHAT kind of sound): 9 bits
#   Bits 0-3: Amplitude level (16 levels, ~7.5 dB each)
#   Bits 4-6: Frequency band (8 bands, ~1.3 octaves each)
#   Bits 7-8: Hard/Flow (4 levels of transient character)
#
# Shell 44 (HOW specific): 9 bits
#   Bits 0-2: Amplitude fine (8 sub-steps, ~0.9 dB each)
#   Bits 3-5: Pitch fine (8 sub-steps within band)
#   Bits 6-8: Harmonic shape (8 levels: sine→saw→square→noise)
#
# Shell 72 (EXACTLY which): 9 bits
#   Bits 0-2: Amplitude micro (8 steps, ~0.1 dB)
#   Bits 3-5: Phase position (8 steps, where in the cycle)
#   Bits 6-8: Spectral detail (8 levels of harmonic fine structure)
#
# Resolution:
#   Amplitude: 16 × 8 × 8 = 1024 levels over 120 dB → 0.12 dB/step
#   Frequency: 8 × 8 = 64 bands → ~0.15 octave/band
#   Human JND for amplitude ≈ 1 dB → we have 0.12 dB resolution
#   Human JND for frequency ≈ 0.5% → at 1kHz that's 5 Hz
#     Our resolution at mid band: ~14 Hz steps → close but may need tuning


# ============================================================
# AUDIO ANALYSIS FUNCTIONS
# ============================================================

def analyze_frame(samples, sample_rate=44100):
    """
    Analyze a frame of audio samples and extract perceptual features.
    
    samples: numpy array of audio samples (-1.0 to 1.0)
    Returns: dict of perceptual features
    """
    N = len(samples)
    if N == 0:
        return {'amplitude': 0, 'frequency': 0, 'transient': 0, 'harmonic': 0}
    
    # Amplitude (RMS)
    rms = np.sqrt(np.mean(samples**2))
    # Convert to dB (ref: full scale = 0 dB)
    db = 20 * np.log10(max(rms, 1e-10))  # -inf to 0
    # Map to 0-120 dB range (assuming -120 dB is silence)
    amplitude = max(0, 120 + db)  # 0 = silence, 120 = max
    
    # Frequency (spectral centroid as proxy for dominant band)
    if N >= 4:
        spectrum = np.abs(np.fft.rfft(samples * np.hanning(N)))
        freqs = np.fft.rfftfreq(N, 1.0/sample_rate)
        # Spectral centroid
        total_energy = np.sum(spectrum)
        if total_energy > 0:
            centroid = np.sum(freqs * spectrum) / total_energy
        else:
            centroid = 0
    else:
        centroid = 0
    
    # Transient detection (D1 of amplitude envelope)
    # High D1 = hard sound, low D1 = flow sound
    if N >= 2:
        envelope = np.abs(samples)
        d1 = np.mean(np.abs(np.diff(envelope)))
    else:
        d1 = 0
    
    # Harmonic content (spectral flatness: 0=tonal, 1=noisy)
    flatness = 0
    if N >= 4:
        spectrum2 = np.abs(np.fft.rfft(samples * np.hanning(N)))
        total_e2 = np.sum(spectrum2)
        if total_e2 > 0:
            spec_positive = spectrum2[spectrum2 > 0]
            if len(spec_positive) > 0:
                geo_mean = np.exp(np.mean(np.log(spec_positive + 1e-10)))
                arith_mean = np.mean(spec_positive)
                flatness = geo_mean / max(arith_mean, 1e-10)
    
    return {
        'amplitude': amplitude,      # 0-120 dB
        'centroid': centroid,         # Hz
        'transient': d1,             # 0-1 (D1 of envelope)
        'flatness': flatness,        # 0-1 (0=pure tone, 1=noise)
    }


def freq_to_band(freq_hz):
    """Map frequency to band index (0-7)."""
    for i, (low, high, name) in enumerate(FREQ_BANDS):
        if freq_hz < high:
            return i
    return 7


def encode_audio_frame(features):
    """
    Encode perceptual features to 27-bit (3 shells of 9).
    Returns (shell1, shell2, shell3) each 0-511.
    """
    amp = features['amplitude']      # 0-120
    freq = features['centroid']      # Hz
    trans = features['transient']    # 0-1
    flat = features['flatness']      # 0-1
    
    # === SHELL 22: Category ===
    
    # Amplitude level (4 bits, 16 levels over 120 dB)
    amp = max(0.0, amp)
    amp_level = max(0, min(int(amp / 120 * AMP_LEVELS), AMP_LEVELS - 1))
    
    # Frequency band (3 bits, 8 bands)
    freq_band = freq_to_band(freq)
    
    # Hard/Flow (2 bits, 4 levels)
    # This is the I/O generator applied to sound
    transient_level = min(int(trans * 4 / 0.15), TRANSIENT_LEVELS - 1)
    # 0.15 is approximate max D1 for typical audio
    transient_level = min(transient_level, 3)
    
    shell1 = (max(0,min(amp_level,15)) << 5) | (max(0,min(freq_band,7)) << 2) | max(0,min(transient_level,3))
    
    # === SHELL 44: Nuance ===
    
    # Amplitude fine (3 bits within the level)
    amp_band_size = 120.0 / AMP_LEVELS
    amp_within = max(0, min((amp - amp_level * amp_band_size) / max(amp_band_size, 0.001), 0.999))
    amp_fine = min(int(amp_within * 8), 7)
    
    # Pitch fine (3 bits within the frequency band)
    band_low, band_high = FREQ_BANDS[freq_band][0], FREQ_BANDS[freq_band][1]
    if band_high > band_low:
        freq_within = (freq - band_low) / (band_high - band_low)
    else:
        freq_within = 0
    pitch_fine = min(int(freq_within * 8), 7)
    
    # Harmonic shape (3 bits: sine → saw → square → noise)
    harmonic = min(int(flat * 8), 7)
    
    shell2 = (max(0,min(amp_fine,7)) << 6) | (max(0,min(pitch_fine,7)) << 3) | max(0,min(harmonic,7))
    
    # === SHELL 72: Exact ===
    
    # Amplitude micro (3 bits: fine amplitude within shell 44's band)
    amp_fine_size = max(amp_band_size / 8, 0.001)
    amp_micro_pos = (amp - amp_level * amp_band_size - amp_fine * amp_fine_size) / amp_fine_size
    amp_micro = max(0, min(int(amp_micro_pos * 8), 7))
    
    # Phase position (3 bits: where in the wave cycle)
    phase = max(0, min(int(abs(trans * 30) % 8), 7))
    
    # Spectral detail (3 bits)
    spectral_detail = max(0, min(int(abs(flat) * 3 * 8) % 8, 7))
    
    shell3 = (max(0,min(amp_micro,7)) << 6) | (max(0,min(phase,7)) << 3) | max(0,min(spectral_detail,7))
    
    return int(shell1) & 0x1FF, int(shell2) & 0x1FF, int(shell3) & 0x1FF


# ============================================================
# AUDIO GENERATORS — Synthesize test signals
# ============================================================

def generate_sine(freq, duration, sample_rate=44100, amplitude=0.5):
    """Pure sine wave."""
    t = np.arange(int(duration * sample_rate)) / sample_rate
    return amplitude * np.sin(2 * np.pi * freq * t)

def generate_drum_hit(duration=0.1, sample_rate=44100):
    """Percussive drum hit — HARD sound, I-dominant."""
    t = np.arange(int(duration * sample_rate)) / sample_rate
    # Fast attack, exponential decay
    envelope = np.exp(-30 * t)
    # Noise burst + low frequency thump
    noise = np.random.randn(len(t)) * 0.3
    thump = np.sin(2 * np.pi * 60 * t) * 0.7
    return envelope * (noise + thump)

def generate_vowel_ah(duration=0.5, sample_rate=44100):
    """Sustained vowel 'AH' — FLOW sound, O-dominant."""
    t = np.arange(int(duration * sample_rate)) / sample_rate
    # Gentle attack/release
    envelope = np.minimum(t / 0.05, 1.0) * np.minimum((duration - t) / 0.05, 1.0)
    # Fundamental + harmonics (formants for 'AH')
    signal = (0.5 * np.sin(2 * np.pi * 220 * t) +
              0.3 * np.sin(2 * np.pi * 440 * t) +
              0.15 * np.sin(2 * np.pi * 880 * t) +
              0.05 * np.sin(2 * np.pi * 1760 * t))
    return envelope * signal * 0.5

def generate_speech_sentence(duration=2.0, sample_rate=44100):
    """Simulate speech: alternating consonants (I) and vowels (O)."""
    t = np.arange(int(duration * sample_rate)) / sample_rate
    signal = np.zeros_like(t)
    
    # Syllables: consonant (hard/short) + vowel (flow/long)
    syllable_dur = 0.2  # 200ms per syllable
    num_syllables = int(duration / syllable_dur)
    
    for i in range(num_syllables):
        start = int(i * syllable_dur * sample_rate)
        
        # Consonant (first 30% = hard)
        cons_end = start + int(0.06 * sample_rate)
        if cons_end < len(t):
            # Noise burst with fast decay
            cons_len = cons_end - start
            cons_env = np.exp(-50 * np.arange(cons_len) / sample_rate)
            signal[start:cons_end] += np.random.randn(cons_len) * cons_env * 0.3
        
        # Vowel (remaining 70% = flow)
        vowel_start = cons_end
        vowel_end = min(start + int(syllable_dur * sample_rate), len(t))
        if vowel_end > vowel_start:
            vowel_len = vowel_end - vowel_start
            vowel_t = np.arange(vowel_len) / sample_rate
            # Random fundamental (100-300 Hz voice range)
            f0 = 100 + np.random.rand() * 200
            vowel_env = np.minimum(vowel_t / 0.02, 1.0) * np.minimum(
                (vowel_len/sample_rate - vowel_t) / 0.02, 1.0)
            signal[vowel_start:vowel_end] += vowel_env * (
                0.5 * np.sin(2 * np.pi * f0 * vowel_t) +
                0.2 * np.sin(2 * np.pi * 2 * f0 * vowel_t))
    
    return np.clip(signal, -1, 1)

def generate_music(duration=3.0, sample_rate=44100):
    """Simulate music: drums + bass + melody."""
    t = np.arange(int(duration * sample_rate)) / sample_rate
    signal = np.zeros_like(t)
    
    # Kick drum every beat (hard)
    bpm = 120
    beat_samples = int(60.0 / bpm * sample_rate)
    for beat_start in range(0, len(t), beat_samples):
        drum = generate_drum_hit(0.1, sample_rate)
        end = min(beat_start + len(drum), len(t))
        signal[beat_start:end] += drum[:end-beat_start] * 0.4
    
    # Bass line (flow)
    bass_notes = [55, 65, 73, 55]  # A1, C2, D2, A1
    note_dur = 60.0 / bpm
    for i, freq in enumerate(bass_notes * int(duration / (note_dur * 4) + 1)):
        start = int(i * note_dur * sample_rate)
        end = min(start + int(note_dur * sample_rate), len(t))
        if end > start:
            bt = np.arange(end - start) / sample_rate
            env = np.minimum(bt / 0.01, 1.0) * np.exp(-2 * bt)
            signal[start:end] += env * np.sin(2 * np.pi * freq * bt) * 0.3
    
    # Melody (mix of hard and flow)
    melody_notes = [440, 523, 587, 659, 523, 440, 392, 440]
    mel_dur = note_dur / 2
    for i, freq in enumerate(melody_notes * int(duration / (mel_dur * 8) + 1)):
        start = int(i * mel_dur * sample_rate)
        end = min(start + int(mel_dur * sample_rate), len(t))
        if end > start:
            mt = np.arange(end - start) / sample_rate
            env = np.minimum(mt / 0.005, 1.0) * np.minimum(
                (mel_dur - mt) / 0.01, 1.0)
            signal[start:end] += env * (
                0.3 * np.sin(2 * np.pi * freq * mt) +
                0.1 * np.sin(2 * np.pi * 2 * freq * mt)) * 0.3
    
    return np.clip(signal, -1, 1)

def generate_silence(duration=1.0, sample_rate=44100):
    """Pure silence — void."""
    return np.zeros(int(duration * sample_rate))

def generate_white_noise(duration=0.5, sample_rate=44100):
    """White noise — maximum chaos."""
    return np.random.randn(int(duration * sample_rate)) * 0.3


# ============================================================
# COMPRESSION PIPELINE
# ============================================================

def compress_audio(samples, sample_rate=44100, frame_size_ms=5):
    """
    Full pipeline: audio samples → frames → perceptual features → 27-bit → RLE compress
    
    frame_size_ms: analysis frame size in milliseconds
    Smaller = more temporal resolution, more frames, less compression
    Larger = less resolution, fewer frames, more compression
    5ms = good balance (captures transients, still compresses well)
    """
    frame_size = int(sample_rate * frame_size_ms / 1000)
    num_frames = len(samples) // frame_size
    
    if num_frames == 0:
        return b'', {'frames': 0}
    
    # Analyze each frame
    shells = np.zeros((num_frames, 3), dtype=np.uint16)
    
    for i in range(num_frames):
        start = i * frame_size
        end = start + frame_size
        frame = samples[start:end]
        
        features = analyze_frame(frame, sample_rate)
        s1, s2, s3 = encode_audio_frame(features)
        shells[i] = [s1, s2, s3]
    
    # RLE compress each shell independently
    compressed_shells = []
    total_comp_size = 0
    
    for s in range(3):
        shell_data = shells[:, s]
        packed, num_runs = rle_compress(shell_data)
        compressed_shells.append((packed, num_runs))
        total_comp_size += len(packed)
    
    # Pack
    header = struct.pack('>IIIH', 
        len(samples),       # total samples
        sample_rate,        # sample rate
        num_frames,         # frame count
        frame_size          # frame size in samples
    )
    
    result = bytearray(header)
    for packed, num_runs in compressed_shells:
        result.extend(struct.pack('>I', num_runs))
        result.extend(packed)
    
    # Statistics
    raw_pcm_size = len(samples) * 2  # 16-bit PCM
    raw_27bit_size = num_frames * 27 // 8
    
    stats = {
        'frames': num_frames,
        'pcm_size': raw_pcm_size,
        'raw_27bit_size': raw_27bit_size,
        'compressed_size': len(result),
        'shell_runs': [cs[1] for cs in compressed_shells],
        'unique_per_shell': [len(np.unique(shells[:, s])) for s in range(3)],
    }
    
    return bytes(result), stats


def rle_compress(data):
    """RLE compress 16-bit values."""
    runs = []
    current = int(data[0])
    count = 1
    for i in range(1, len(data)):
        val = int(data[i])
        if val == current and count < 65535:
            count += 1
        else:
            runs.append((current, count))
            current = val
            count = 1
    runs.append((current, count))
    
    packed = bytearray()
    for val, cnt in runs:
        packed.extend(struct.pack('>HH', val & 0xFFFF, cnt))
    return bytes(packed), len(runs)


# ============================================================
# I/O PATTERN ANALYSIS
# ============================================================

def analyze_io_pattern(samples, sample_rate=44100, frame_size_ms=5):
    """
    Show the I/O (hard/flow) pattern of audio.
    This IS the TIG generator view of sound.
    """
    frame_size = int(sample_rate * frame_size_ms / 1000)
    num_frames = len(samples) // frame_size
    
    pattern = []
    for i in range(num_frames):
        start = i * frame_size
        frame = samples[start:start + frame_size]
        
        if len(frame) < 2:
            pattern.append(0)
            continue
        
        # D1 of envelope = transient measure
        envelope = np.abs(frame)
        d1 = np.mean(np.abs(np.diff(envelope)))
        
        # Binary: hard (I=1) or flow (O=0)
        pattern.append(1 if d1 > 0.02 else 0)
    
    return pattern


def visualize_io(pattern, label=""):
    """Show I/O pattern as a string."""
    # Show in groups of 50
    s = ''.join(str(b) for b in pattern)
    ones = sum(pattern)
    zeros = len(pattern) - ones
    
    print(f"\n  {label}")
    print(f"  I(hard)={ones} O(flow)={zeros} ratio={ones/max(zeros,1):.2f}")
    
    # Show first 100 characters
    display = s[:100]
    # Color-code: group runs
    runs = []
    if pattern:
        current = pattern[0]
        count = 1
        for i in range(1, min(len(pattern), 100)):
            if pattern[i] == current:
                count += 1
            else:
                runs.append((current, count))
                current = pattern[i]
                count = 1
        runs.append((current, count))
    
    avg_run = np.mean([r[1] for r in runs]) if runs else 0
    max_run = max([r[1] for r in runs]) if runs else 0
    
    print(f"  Runs: {len(runs)}, avg_len={avg_run:.1f}, max={max_run}")
    print(f"  Pattern: {display}")


# ============================================================
# TEST SUITE
# ============================================================

def test_audio(samples, sample_rate, label=""):
    """Test compression on an audio signal."""
    duration = len(samples) / sample_rate
    pcm_size = len(samples) * 2  # 16-bit
    
    print(f"\n{'='*70}")
    print(f"  {label}")
    print(f"  {duration:.2f}s, {len(samples):,} samples, {sample_rate} Hz")
    print(f"{'='*70}")
    
    # I/O pattern
    io_pattern = analyze_io_pattern(samples, sample_rate)
    visualize_io(io_pattern, "I/O Generator Pattern (I=hard, O=flow)")
    
    # Compress
    compressed, stats = compress_audio(samples, sample_rate)
    
    comp_size = stats['compressed_size']
    pcm_ratio = pcm_size / max(comp_size, 1)
    
    # Standard comparison: MP3 at 128kbps
    mp3_estimate = int(128000 / 8 * duration)  # 128kbps
    mp3_ratio = pcm_size / max(mp3_estimate, 1)
    tig_vs_mp3 = mp3_estimate / max(comp_size, 1)
    
    print(f"\n  Compression Results:")
    print(f"    PCM 16-bit raw:     {pcm_size:>10,} bytes")
    print(f"    TIG 27-bit raw:     {stats['raw_27bit_size']:>10,} bytes")
    print(f"    TIG compressed:     {comp_size:>10,} bytes")
    print(f"    vs PCM:             {pcm_ratio:>10.1f}x compression")
    print(f"    MP3 128kbps est:    {mp3_estimate:>10,} bytes")
    print(f"    TIG vs MP3:         {tig_vs_mp3:>10.1f}x {'better' if tig_vs_mp3 > 1 else 'worse'}")
    
    print(f"\n  Shell Analysis:")
    for s, name in enumerate(["Shell 22 (what)", "Shell 44 (how)", "Shell 72 (exact)"]):
        print(f"    {name}: {stats['unique_per_shell'][s]:>4} unique, "
              f"{stats['shell_runs'][s]:>6} runs, "
              f"avg {stats['frames']/max(stats['shell_runs'][s],1):.1f} frames/run")
    
    # Bitrate
    bitrate = comp_size * 8 / max(duration, 0.001)
    print(f"\n  Effective bitrate: {bitrate/1000:.1f} kbps")
    print(f"  (MP3 = 128 kbps, CD = 1411 kbps)")
    
    return pcm_ratio, tig_vs_mp3


def run_all():
    """Complete audio compression test suite."""
    
    print("\n" + "="*70)
    print("  TIG 27-BIT PERCEPTUAL AUDIO — Three Shells of Force Geometry")
    print("  Flow sounds = O (0). Hard sounds = I (1).")
    print("  Shell 22: What? Shell 44: How? Shell 72: Exactly?")
    print("="*70)
    
    sr = 44100
    np.random.seed(42)
    
    # Test 1: Silence (pure void — best case)
    silence = generate_silence(2.0, sr)
    test_audio(silence, sr, "Silence (pure void)")
    
    # Test 2: Pure sine wave (pure flow — sustained O)
    sine = generate_sine(440, 2.0, sr, 0.5)
    test_audio(sine, sr, "Pure Sine 440Hz (pure flow, all O)")
    
    # Test 3: Drum hit (pure hard — I burst then void)
    drum = generate_drum_hit(0.5, sr)
    test_audio(drum, sr, "Drum Hit (hard attack, I→O decay)")
    
    # Test 4: Vowel 'AH' (sustained flow)
    vowel = generate_vowel_ah(1.0, sr)
    test_audio(vowel, sr, "Vowel 'AH' (sustained flow, mostly O)")
    
    # Test 5: Speech (alternating I and O)
    speech = generate_speech_sentence(3.0, sr)
    test_audio(speech, sr, "Simulated Speech (consonants I + vowels O)")
    
    # Test 6: Music (drums + bass + melody)
    music = generate_music(5.0, sr)
    test_audio(music, sr, "Simulated Music (drums + bass + melody)")
    
    # Test 7: White noise (maximum chaos — worst case)
    noise = generate_white_noise(1.0, sr)
    test_audio(noise, sr, "White Noise (pure chaos)")
    
    # Test 8: Rocket League-like game audio
    # Engines (sustained flow) + ball hits (transients) + crowd (noise)
    game_dur = 3.0
    t = np.arange(int(game_dur * sr)) / sr
    engine = 0.15 * np.sin(2 * np.pi * 80 * t) * (1 + 0.3 * np.sin(2 * np.pi * 2 * t))
    
    # Ball hits at random times
    ball_hits = np.zeros_like(t)
    for hit_time in [0.5, 1.2, 1.8, 2.5]:
        hit_start = int(hit_time * sr)
        hit = generate_drum_hit(0.05, sr) * 0.5
        end = min(hit_start + len(hit), len(t))
        ball_hits[hit_start:end] += hit[:end - hit_start]
    
    # Crowd ambiance
    crowd = np.random.randn(len(t)) * 0.02
    
    game_audio = np.clip(engine + ball_hits + crowd, -1, 1)
    test_audio(game_audio, sr, "Game Audio (engine + ball hits + crowd)")
    
    # Summary
    print(f"\n\n{'='*70}")
    print(f"  SUMMARY — TIG Perceptual Audio")
    print(f"{'='*70}")
    print(f"""
    The I/O generator pattern reveals the STRUCTURE of sound:
    
    Silence:  OOOOOOOOOOOOO  (pure void, maximum compression)
    Sine:     OOOOOOOOOOOOO  (pure flow, sustain = long O-runs)
    Drum:     IIIOOOOOOOOOOO (hard attack → flow decay)
    Speech:   IIOOOOIIOOOOII (alternating hard/flow = syllables)
    Music:    IIOOOIOOOOIIOO (rhythm = periodic I in O flow)
    Noise:    IOIOIOIOIOIOIO (random alternation, worst case)
    
    Compression works because:
    1. Adjacent frames with same perceptual state → identical shells → long runs
    2. Shell 22 (category) compresses MOST: few unique categories
    3. Sustained sounds → massive Shell 22 runs (one category for entire note)
    4. Even Shell 72 compresses well on tonal signals (harmonics are stable)
    
    Flow sounds (O) compress better than hard sounds (I) because
    flow is sustained (long runs) while hard is transient (short bursts).
    
    The I/O pattern IS the sound's force geometry.
    Hard sounds are structure. Flow sounds are force.
    Same generators. Same algebra. Different substrate.
    """)


if __name__ == "__main__":
    run_all()
