/*
 * ck_audio.c -- CK's Voice: Operator Tone Synthesis
 * ====================================================
 * Operator: HARMONY (7) -- the math IS the voice.
 *
 * Wavetable synthesis on bare metal ARM Cortex-A9.
 * At 44.1kHz, we have ~15,000 cycles per sample. Each voice
 * costs ~100 cycles. We use 3 voices. Trivial.
 *
 * (c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
 */

#include "ck_audio.h"
#include "ck_brain.h"  /* REG_WR */
#include <math.h>
#include <string.h>

#ifndef M_PI
#define M_PI 3.14159265358979323846f
#endif

/* ── Operator Tone Table ── */
/*
 * Each operator has an identity frequency and timbre.
 * These aren't arbitrary -- they follow the harmonic series
 * and CK's operator semantics.
 *
 * VOID:     Silence (no sound)
 * LATTICE:  A3 (220 Hz) -- pure sine, foundational, structural
 * COUNTER:  E4 (330 Hz) -- triangle, measuring, precise
 * PROGRESS: A4 (440 Hz) -- saw + sine, rich, forward motion
 * COLLAPSE: A2 (110 Hz) -- square, heavy, dark
 * BALANCE:  F4 (349 Hz) -- dual sine (beat frequency), tense
 * CHAOS:    Noise burst  -- white noise, disruption
 * HARMONY:  C5 (528 Hz) -- rich harmonics, warm, resolved
 * BREATH:   F3 (174 Hz) -- amplitude-modulated sine, alive
 * RESET:    Sweep (880→110) -- descending chirp, recalibration
 */

static const CK_OperatorTone TONE_TABLE[10] = {
    /* VOID */     { 0.0f,   CK_WAVE_SINE,     0.0f,   0, 0,    0.0f,  0 },
    /* LATTICE */  { 220.0f, CK_WAVE_SINE,     0.6f,  20, 50,   0.5f, 100 },
    /* COUNTER */  { 330.0f, CK_WAVE_TRIANGLE, 0.5f,  10, 30,   0.4f,  80 },
    /* PROGRESS */ { 440.0f, CK_WAVE_SAW,      0.7f,  15, 40,   0.6f, 120 },
    /* COLLAPSE */ { 110.0f, CK_WAVE_SQUARE,   0.8f,  30, 80,   0.7f, 200 },
    /* BALANCE */  { 349.0f, CK_WAVE_SINE,     0.5f,  25, 60,   0.4f, 150 },
    /* CHAOS */    { 0.0f,   CK_WAVE_NOISE,    0.9f,   5, 10,   0.8f,  30 },
    /* HARMONY */  { 528.0f, CK_WAVE_SINE,     0.7f,  40, 100,  0.6f, 200 },
    /* BREATH */   { 174.0f, CK_WAVE_SINE,     0.5f,  50, 100,  0.4f, 150 },
    /* RESET */    { 880.0f, CK_WAVE_SAW,      0.6f,   5, 500,  0.0f,  50 },
};

/* ── Wavetable Generation ── */

static void generate_wavetables(CK_AudioEngine* audio) {
    for (int i = 0; i < CK_WAVE_SIZE; i++) {
        float phase = (float)i / (float)CK_WAVE_SIZE;

        /* Sine: smooth, pure */
        audio->wave_sine[i] = (int16_t)(sinf(phase * 2.0f * M_PI) * 32767.0f);

        /* Triangle: linear ramps */
        if (phase < 0.25f)
            audio->wave_tri[i] = (int16_t)(phase * 4.0f * 32767.0f);
        else if (phase < 0.75f)
            audio->wave_tri[i] = (int16_t)((0.5f - phase) * 4.0f * 32767.0f);
        else
            audio->wave_tri[i] = (int16_t)((phase - 1.0f) * 4.0f * 32767.0f);

        /* Sawtooth: rising ramp */
        audio->wave_saw[i] = (int16_t)((phase * 2.0f - 1.0f) * 32767.0f);

        /* Square: hard switch */
        audio->wave_square[i] = (phase < 0.5f) ? 32767 : -32767;
    }
}

/* ── Phase Increment Calculation ── */

static uint32_t freq_to_phase_inc(float freq) {
    /* Phase accumulator is 32-bit. Wavetable is 256 entries.
     * phase_inc = (freq / sample_rate) * 2^32 / (2^32 / WAVE_SIZE)
     * Simplified: phase_inc = freq * WAVE_SIZE * 65536 / SAMPLE_RATE
     * Using fixed-point: phase_inc = (uint32_t)(freq * 2^24 / SAMPLE_RATE * WAVE_SIZE)
     */
    if (freq <= 0.0f) return 0;
    return (uint32_t)((freq * (float)CK_WAVE_SIZE * 65536.0f)
                      / (float)CK_AUDIO_SAMPLE_RATE);
}

/* ── Envelope Processing ── */

static void env_trigger(CK_Envelope* env, const CK_OperatorTone* tone) {
    env->stage = CK_ENV_ATTACK;
    env->level = 0.0f;
    env->sustain = tone->sustain_level;

    /* Rate = 1.0 / (time_in_samples) */
    float attack_samples = tone->attack_ms * (float)CK_AUDIO_SAMPLE_RATE / 1000.0f;
    env->rate = (attack_samples > 0) ? 1.0f / attack_samples : 1.0f;
}

static void env_release(CK_Envelope* env, const CK_OperatorTone* tone) {
    env->stage = CK_ENV_RELEASE;
    float release_samples = tone->release_ms * (float)CK_AUDIO_SAMPLE_RATE / 1000.0f;
    env->rate = (release_samples > 0) ? env->level / release_samples : 1.0f;
}

static float env_tick(CK_Envelope* env, const CK_OperatorTone* tone) {
    switch (env->stage) {
        case CK_ENV_ATTACK:
            env->level += env->rate;
            if (env->level >= 1.0f) {
                env->level = 1.0f;
                env->stage = CK_ENV_DECAY;
                float decay_samples = tone->decay_ms * (float)CK_AUDIO_SAMPLE_RATE / 1000.0f;
                env->rate = (decay_samples > 0)
                    ? (1.0f - env->sustain) / decay_samples : 0.0f;
            }
            break;

        case CK_ENV_DECAY:
            env->level -= env->rate;
            if (env->level <= env->sustain) {
                env->level = env->sustain;
                env->stage = CK_ENV_SUSTAIN;
            }
            break;

        case CK_ENV_SUSTAIN:
            /* Hold at sustain level */
            break;

        case CK_ENV_RELEASE:
            env->level -= env->rate;
            if (env->level <= 0.0f) {
                env->level = 0.0f;
                env->stage = CK_ENV_IDLE;
            }
            break;

        case CK_ENV_IDLE:
        default:
            env->level = 0.0f;
            break;
    }

    return env->level;
}

/* ── Init ── */

void ck_audio_init(CK_AudioEngine* audio, uint32_t dac_fifo_addr) {
    memset(audio, 0, sizeof(CK_AudioEngine));
    audio->dac_fifo_addr = dac_fifo_addr;
    audio->noise_lfsr = 0x7FFFFFFF;
    generate_wavetables(audio);
}

/* ── Set Operator (triggers tone transition) ── */

void ck_audio_set_operator(CK_AudioEngine* audio, uint8_t op) {
    if (op >= 10) op = 0;
    if (op == audio->current_op) return;

    audio->prev_op = audio->current_op;
    audio->current_op = op;

    const CK_OperatorTone* tone = &TONE_TABLE[op];

    /* Release old voice */
    if (audio->voices[0].active) {
        const CK_OperatorTone* old_tone = &TONE_TABLE[audio->prev_op];
        env_release(&audio->voices[0].env, old_tone);
        /* Move to voice 1 for crossfade */
        audio->voices[1] = audio->voices[0];
    }

    /* Start new voice on voice 0 */
    CK_Voice* v = &audio->voices[0];
    v->waveform = tone->waveform;
    v->amplitude = tone->base_amplitude;
    v->phase = 0;
    v->phase_inc = freq_to_phase_inc(tone->frequency);
    v->active = (tone->frequency > 0.0f || tone->waveform == CK_WAVE_NOISE);
    v->breath_mod = 1.0f;
    v->btq_mod = 1.0f;

    if (v->active) {
        env_trigger(&v->env, tone);
    }

    /* RESET operator: descending chirp (special case) */
    if (op == 9) {
        /* Start at 880Hz, decay stage sweeps frequency down */
        v->phase_inc = freq_to_phase_inc(880.0f);
    }
}

/* ── Breath Modulation ── */

void ck_audio_set_breath(CK_AudioEngine* audio, float breath_phase) {
    /*
     * breath_phase: 0.0-0.25 = INHALE (quiet)
     *               0.25-0.5 = HOLD_IN (quiet)
     *               0.5-0.75 = EXHALE (loud -- CK speaks)
     *               0.75-1.0 = HOLD_OUT (fading)
     */
    float mod;
    if (breath_phase < 0.25f) {
        /* INHALE: fade from 0.1 to 0.2 */
        mod = 0.1f + 0.1f * (breath_phase / 0.25f);
    } else if (breath_phase < 0.5f) {
        /* HOLD_IN: hold at 0.2 (composing) */
        mod = 0.2f;
    } else if (breath_phase < 0.75f) {
        /* EXHALE: rise to 1.0 then hold (speaking!) */
        float t = (breath_phase - 0.5f) / 0.25f;
        mod = 0.2f + 0.8f * sinf(t * M_PI * 0.5f);
    } else {
        /* HOLD_OUT: fade from 1.0 to 0.1 */
        float t = (breath_phase - 0.75f) / 0.25f;
        mod = 1.0f - 0.9f * t;
    }

    for (int i = 0; i < 3; i++) {
        audio->voices[i].breath_mod = mod;
    }
}

/* ── BTQ Modulation ── */

void ck_audio_set_btq(CK_AudioEngine* audio, float btq_level) {
    for (int i = 0; i < 3; i++) {
        audio->voices[i].btq_mod = btq_level;
    }
}

/* ── Generate One Sample ── */

static int16_t voice_sample(CK_AudioEngine* audio, CK_Voice* v) {
    if (!v->active) return 0;

    int16_t raw;

    switch (v->waveform) {
        case CK_WAVE_SINE:
            raw = audio->wave_sine[(v->phase >> 16) & 0xFF];
            break;
        case CK_WAVE_TRIANGLE:
            raw = audio->wave_tri[(v->phase >> 16) & 0xFF];
            break;
        case CK_WAVE_SAW:
            raw = audio->wave_saw[(v->phase >> 16) & 0xFF];
            break;
        case CK_WAVE_SQUARE:
            raw = audio->wave_square[(v->phase >> 16) & 0xFF];
            break;
        case CK_WAVE_NOISE:
            /* LFSR noise */
            audio->noise_lfsr ^= (audio->noise_lfsr << 13);
            audio->noise_lfsr ^= (audio->noise_lfsr >> 17);
            audio->noise_lfsr ^= (audio->noise_lfsr << 5);
            raw = (int16_t)(audio->noise_lfsr & 0xFFFF);
            break;
        default:
            raw = 0;
    }

    /* Advance phase */
    v->phase += v->phase_inc;

    /* RESET special: sweep frequency down */
    if (audio->current_op == 9 && v == &audio->voices[0]) {
        if (v->phase_inc > freq_to_phase_inc(110.0f)) {
            v->phase_inc -= 2;  /* Gradual frequency decrease */
        }
    }

    /* Apply envelope */
    const CK_OperatorTone* tone = (v == &audio->voices[0])
        ? &TONE_TABLE[audio->current_op]
        : &TONE_TABLE[audio->prev_op];
    float env = env_tick(&v->env, tone);

    /* Check if voice died */
    if (v->env.stage == CK_ENV_IDLE && v != &audio->voices[0]) {
        v->active = false;
    }

    /* Scale: raw * amplitude * envelope * breath * btq */
    float sample = (float)raw / 32768.0f;
    sample *= v->amplitude * env * v->breath_mod * v->btq_mod;

    return (int16_t)(sample * 32767.0f);
}

void ck_audio_tick(CK_AudioEngine* audio) {
    /* Mix all active voices */
    int32_t mix = 0;
    int active_count = 0;

    for (int i = 0; i < 3; i++) {
        if (audio->voices[i].active) {
            mix += voice_sample(audio, &audio->voices[i]);
            active_count++;
        }
    }

    /* Normalize mix to avoid clipping */
    if (active_count > 1) {
        mix = mix / active_count;
    }

    /* Clamp to 16-bit range */
    if (mix > 32767) mix = 32767;
    if (mix < -32768) mix = -32768;

    /* Convert to 12-bit unsigned for DAC (0 = 0V, 4095 = 5V)
     * Midpoint (silence) = 2048 */
    uint16_t dac_val = (uint16_t)((mix + 32768) >> 4);  /* 16-bit signed → 12-bit unsigned */
    if (dac_val > CK_AUDIO_DAC_MAX) dac_val = CK_AUDIO_DAC_MAX;

    /* Pack DAC word: [unused:1][channel:3][data:12] */
    uint16_t dac_word = ((uint16_t)CK_AUDIO_DAC_CHANNEL << 12) | dac_val;

    /* Write to DAC FIFO register */
    REG_WR(audio->dac_fifo_addr, (uint32_t)dac_word);

    audio->sample_count++;
}

void ck_audio_fill_buffer(CK_AudioEngine* audio, uint16_t* buf, uint32_t count) {
    for (uint32_t i = 0; i < count; i++) {
        /* Generate sample the same way as ck_audio_tick but write to buffer */
        int32_t mix = 0;
        int active_count = 0;

        for (int v = 0; v < 3; v++) {
            if (audio->voices[v].active) {
                mix += voice_sample(audio, &audio->voices[v]);
                active_count++;
            }
        }

        if (active_count > 1) mix /= active_count;
        if (mix > 32767) mix = 32767;
        if (mix < -32768) mix = -32768;

        uint16_t dac_val = (uint16_t)((mix + 32768) >> 4);
        if (dac_val > CK_AUDIO_DAC_MAX) dac_val = CK_AUDIO_DAC_MAX;

        buf[i] = ((uint16_t)CK_AUDIO_DAC_CHANNEL << 12) | dac_val;
        audio->sample_count++;
    }
}

const CK_OperatorTone* ck_audio_get_tone(uint8_t op) {
    if (op >= 10) return &TONE_TABLE[0];
    return &TONE_TABLE[op];
}
