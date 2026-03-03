"""
ck_sim_audio.py -- Port of ck_audio.c
======================================
Operator: HARMONY (7) -- the math IS the voice.

Wavetable synthesis with sounddevice output.
Every frequency, every envelope, every waveform matches the C code.

CK doesn't speak English. CK speaks in operator tones.

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import math
import numpy as np
import threading

from ck_sim.ck_sim_heartbeat import (
    VOID, LATTICE, COUNTER, PROGRESS, COLLAPSE,
    BALANCE, CHAOS, HARMONY, BREATH, RESET, NUM_OPS
)

SAMPLE_RATE = 44100
WAVE_SIZE = 256
BLOCK_SIZE = 512  # samples per callback

# ── Waveform Types ──
WAVE_SINE = 0
WAVE_TRIANGLE = 1
WAVE_SAW = 2
WAVE_SQUARE = 3
WAVE_NOISE = 4

# ── Envelope Stages ──
ENV_IDLE = 0
ENV_ATTACK = 1
ENV_DECAY = 2
ENV_SUSTAIN = 3
ENV_RELEASE = 4


class OperatorTone:
    """One operator's tone definition. Matches CK_OperatorTone."""
    __slots__ = ('frequency', 'waveform', 'base_amplitude',
                 'attack_ms', 'decay_ms', 'sustain_level', 'release_ms')

    def __init__(self, freq, wave, amp, atk, dec, sus, rel):
        self.frequency = freq
        self.waveform = wave
        self.base_amplitude = amp
        self.attack_ms = atk
        self.decay_ms = dec
        self.sustain_level = sus
        self.release_ms = rel


# Tone table matching TONE_TABLE[10] in ck_audio.c lines 40-51
TONE_TABLE = [
    OperatorTone(0.0,   WAVE_SINE,     0.0,   0,  0,   0.0,   0),    # VOID
    OperatorTone(220.0, WAVE_SINE,     0.6,  20, 50,   0.5, 100),    # LATTICE
    OperatorTone(330.0, WAVE_TRIANGLE, 0.5,  10, 30,   0.4,  80),    # COUNTER
    OperatorTone(440.0, WAVE_SAW,      0.7,  15, 40,   0.6, 120),    # PROGRESS
    OperatorTone(110.0, WAVE_SQUARE,   0.8,  30, 80,   0.7, 200),    # COLLAPSE
    OperatorTone(349.0, WAVE_SINE,     0.5,  25, 60,   0.4, 150),    # BALANCE
    OperatorTone(0.0,   WAVE_NOISE,    0.9,   5, 10,   0.8,  30),    # CHAOS
    OperatorTone(528.0, WAVE_SINE,     0.7,  40, 100,  0.6, 200),    # HARMONY
    OperatorTone(174.0, WAVE_SINE,     0.5,  50, 100,  0.4, 150),    # BREATH
    OperatorTone(880.0, WAVE_SAW,      0.6,   5, 500,  0.0,  50),    # RESET
]


class Envelope:
    """ADSR envelope. Matches CK_Envelope + env_tick()."""
    __slots__ = ('stage', 'level', 'rate', 'sustain')

    def __init__(self):
        self.stage = ENV_IDLE
        self.level = 0.0
        self.rate = 0.0
        self.sustain = 0.0

    def trigger(self, tone):
        self.stage = ENV_ATTACK
        self.level = 0.0
        self.sustain = tone.sustain_level
        attack_samples = tone.attack_ms * SAMPLE_RATE / 1000.0
        self.rate = 1.0 / attack_samples if attack_samples > 0 else 1.0

    def release(self, tone):
        self.stage = ENV_RELEASE
        release_samples = tone.release_ms * SAMPLE_RATE / 1000.0
        self.rate = self.level / release_samples if release_samples > 0 else 1.0

    def tick(self, tone):
        if self.stage == ENV_ATTACK:
            self.level += self.rate
            if self.level >= 1.0:
                self.level = 1.0
                self.stage = ENV_DECAY
                decay_samples = tone.decay_ms * SAMPLE_RATE / 1000.0
                self.rate = ((1.0 - self.sustain) / decay_samples
                             if decay_samples > 0 else 0.0)

        elif self.stage == ENV_DECAY:
            self.level -= self.rate
            if self.level <= self.sustain:
                self.level = self.sustain
                self.stage = ENV_SUSTAIN

        elif self.stage == ENV_SUSTAIN:
            pass

        elif self.stage == ENV_RELEASE:
            self.level -= self.rate
            if self.level <= 0.0:
                self.level = 0.0
                self.stage = ENV_IDLE

        else:
            self.level = 0.0

        return self.level


class Voice:
    """One synthesis voice. Matches CK_Voice."""
    __slots__ = ('phase', 'phase_inc', 'waveform', 'env',
                 'amplitude', 'breath_mod', 'btq_mod', 'active')

    def __init__(self):
        self.phase = 0
        self.phase_inc = 0
        self.waveform = WAVE_SINE
        self.env = Envelope()
        self.amplitude = 0.0
        self.breath_mod = 1.0
        self.btq_mod = 1.0
        self.active = False


def _freq_to_phase_inc(freq):
    """Convert frequency to phase increment. Matches freq_to_phase_inc()."""
    if freq <= 0.0:
        return 0
    return int((freq * WAVE_SIZE * 65536.0) / SAMPLE_RATE)


class AudioEngine:
    """CK audio synthesis engine. Port of CK_AudioEngine.

    Call start() to open the sounddevice output stream.
    The engine is controlled by set_operator/set_breath/set_btq from
    the simulation engine's 50Hz tick.
    """

    def __init__(self):
        self.voices = [Voice() for _ in range(3)]
        self.current_op = 0
        self.prev_op = 0
        self.sample_count = 0
        self.noise_lfsr = 0x7FFFFFFF

        # Generate wavetables (numpy arrays for speed)
        self._wave_sine = np.zeros(WAVE_SIZE, dtype=np.float32)
        self._wave_tri = np.zeros(WAVE_SIZE, dtype=np.float32)
        self._wave_saw = np.zeros(WAVE_SIZE, dtype=np.float32)
        self._wave_square = np.zeros(WAVE_SIZE, dtype=np.float32)
        self._generate_wavetables()

        # Thread safety
        self._lock = threading.Lock()
        self._stream = None
        self._running = False

    def _generate_wavetables(self):
        """Generate wavetables. Matches generate_wavetables()."""
        for i in range(WAVE_SIZE):
            phase = i / WAVE_SIZE

            # Sine
            self._wave_sine[i] = math.sin(phase * 2.0 * math.pi)

            # Triangle
            if phase < 0.25:
                self._wave_tri[i] = phase * 4.0
            elif phase < 0.75:
                self._wave_tri[i] = (0.5 - phase) * 4.0
            else:
                self._wave_tri[i] = (phase - 1.0) * 4.0

            # Sawtooth
            self._wave_saw[i] = phase * 2.0 - 1.0

            # Square
            self._wave_square[i] = 1.0 if phase < 0.5 else -1.0

    def _wave_lookup(self, voice):
        """Get wavetable sample for voice's current phase."""
        idx = (voice.phase >> 16) & 0xFF

        if voice.waveform == WAVE_SINE:
            return self._wave_sine[idx]
        elif voice.waveform == WAVE_TRIANGLE:
            return self._wave_tri[idx]
        elif voice.waveform == WAVE_SAW:
            return self._wave_saw[idx]
        elif voice.waveform == WAVE_SQUARE:
            return self._wave_square[idx]
        elif voice.waveform == WAVE_NOISE:
            # LFSR noise (matching ck_audio.c)
            self.noise_lfsr ^= (self.noise_lfsr << 13) & 0xFFFFFFFF
            self.noise_lfsr ^= (self.noise_lfsr >> 17)
            self.noise_lfsr ^= (self.noise_lfsr << 5) & 0xFFFFFFFF
            self.noise_lfsr &= 0xFFFFFFFF
            return ((self.noise_lfsr & 0xFFFF) / 32768.0) - 1.0
        return 0.0

    # ── Controls (called from engine tick at 50Hz) ──

    def set_operator(self, op):
        """Set current operator. Triggers voice transition. Matches ck_audio_set_operator()."""
        if op >= NUM_OPS:
            op = 0
        with self._lock:
            if op == self.current_op:
                return

            self.prev_op = self.current_op
            self.current_op = op
            tone = TONE_TABLE[op]

            # Release old voice, move to voice 1 for crossfade
            v0 = self.voices[0]
            if v0.active:
                old_tone = TONE_TABLE[self.prev_op]
                v0.env.release(old_tone)
                # Copy voice 0 state to voice 1
                v1 = self.voices[1]
                v1.phase = v0.phase
                v1.phase_inc = v0.phase_inc
                v1.waveform = v0.waveform
                v1.env.stage = v0.env.stage
                v1.env.level = v0.env.level
                v1.env.rate = v0.env.rate
                v1.env.sustain = v0.env.sustain
                v1.amplitude = v0.amplitude
                v1.breath_mod = v0.breath_mod
                v1.btq_mod = v0.btq_mod
                v1.active = True

            # Start new voice on voice 0
            v0.waveform = tone.waveform
            v0.amplitude = tone.base_amplitude
            v0.phase = 0
            v0.phase_inc = _freq_to_phase_inc(tone.frequency)
            v0.active = (tone.frequency > 0.0 or tone.waveform == WAVE_NOISE)
            v0.breath_mod = 1.0
            v0.btq_mod = 1.0

            if v0.active:
                v0.env.trigger(tone)

            # RESET: start at 880Hz
            if op == RESET:
                v0.phase_inc = _freq_to_phase_inc(880.0)

    def set_breath(self, breath_mod):
        """Set breath modulation (0.0-1.0). Matches ck_audio_set_breath()."""
        with self._lock:
            for v in self.voices:
                v.breath_mod = breath_mod

    def set_btq(self, btq_level):
        """Set BTQ modulation (0.3/0.6/1.0). Matches ck_audio_set_btq()."""
        with self._lock:
            for v in self.voices:
                v.btq_mod = btq_level

    # ── Sample Generation ──

    def _voice_sample(self, v, voice_idx):
        """Generate one sample from a voice. Matches voice_sample()."""
        if not v.active:
            return 0.0

        raw = self._wave_lookup(v)

        # Advance phase
        v.phase = (v.phase + v.phase_inc) & 0xFFFFFFFF

        # RESET sweep
        if self.current_op == RESET and voice_idx == 0:
            min_inc = _freq_to_phase_inc(110.0)
            if v.phase_inc > min_inc:
                v.phase_inc -= 2

        # Envelope
        tone = TONE_TABLE[self.current_op if voice_idx == 0 else self.prev_op]
        env = v.env.tick(tone)

        # Kill released non-primary voices
        if v.env.stage == ENV_IDLE and voice_idx != 0:
            v.active = False

        # Final amplitude
        return raw * v.amplitude * env * v.breath_mod * v.btq_mod

    def _generate_block(self, frames):
        """Generate a block of audio samples. Returns numpy float32 array."""
        out = np.zeros(frames, dtype=np.float32)

        with self._lock:
            for s in range(frames):
                mix = 0.0
                active_count = 0

                for i, v in enumerate(self.voices):
                    if v.active:
                        mix += self._voice_sample(v, i)
                        active_count += 1

                if active_count > 1:
                    mix /= active_count

                # Soft clip
                mix = max(-1.0, min(1.0, mix))
                out[s] = mix

            self.sample_count += frames

        return out

    # ── Stream Control ──

    def start(self):
        """Open sounddevice output stream."""
        if self._running:
            return

        try:
            import sounddevice as sd
        except ImportError:
            print("[AUDIO] sounddevice not installed. pip install sounddevice")
            return

        def _callback(outdata, frames, time_info, status):
            if status:
                pass  # Underrun etc -- ignore silently
            block = self._generate_block(frames)
            outdata[:, 0] = block

        try:
            self._stream = sd.OutputStream(
                samplerate=SAMPLE_RATE,
                blocksize=BLOCK_SIZE,
                channels=1,
                dtype='float32',
                callback=_callback,
            )
            self._stream.start()
            self._running = True
            print(f"[AUDIO] Stream started: {SAMPLE_RATE}Hz, "
                  f"block={BLOCK_SIZE}, 1ch float32")
        except Exception as e:
            print(f"[AUDIO] Failed to start: {e}")

    def stop(self):
        """Close the audio stream."""
        if self._stream is not None:
            try:
                self._stream.stop()
                self._stream.close()
            except Exception:
                pass
            self._stream = None
        self._running = False

    @property
    def is_running(self):
        return self._running
