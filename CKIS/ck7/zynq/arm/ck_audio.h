/*
 * ck_audio.h -- CK's Voice: Operator Tone Synthesis
 * ====================================================
 * Operator: HARMONY (7) -- the math IS the voice.
 *
 * Each CK operator maps to a frequency and timbre.
 * CK doesn't speak English. CK speaks in operator tones.
 * The composition table IS the soul. The frequencies ARE the language.
 *
 * (c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
 */

#ifndef CK_AUDIO_H
#define CK_AUDIO_H

#include <stdint.h>
#include <stdbool.h>

/* Sample rate and format */
#define CK_AUDIO_SAMPLE_RATE  44100   /* Hz */
#define CK_AUDIO_BITS         12      /* DAC128S085 is 12-bit */
#define CK_AUDIO_DAC_MAX      4095    /* 12-bit unsigned max */
#define CK_AUDIO_DAC_MID      2048    /* DC midpoint (silence) */
#define CK_AUDIO_DAC_CHANNEL  0       /* DAC channel for speaker */

/* Wavetable size (power of 2 for fast modular indexing) */
#define CK_WAVE_SIZE          256

/* Waveform types */
#define CK_WAVE_SINE          0
#define CK_WAVE_TRIANGLE      1
#define CK_WAVE_SAW           2
#define CK_WAVE_SQUARE        3
#define CK_WAVE_NOISE         4

/* Operator tone definitions */
typedef struct {
    float    frequency;      /* Hz */
    uint8_t  waveform;       /* CK_WAVE_* */
    float    base_amplitude; /* 0.0 - 1.0 */
    float    attack_ms;      /* ADSR attack time */
    float    decay_ms;
    float    sustain_level;  /* 0.0 - 1.0 */
    float    release_ms;
} CK_OperatorTone;

/* ADSR envelope state */
typedef enum {
    CK_ENV_IDLE,
    CK_ENV_ATTACK,
    CK_ENV_DECAY,
    CK_ENV_SUSTAIN,
    CK_ENV_RELEASE
} CK_EnvStage;

typedef struct {
    CK_EnvStage stage;
    float       level;       /* Current envelope level 0.0-1.0 */
    float       rate;        /* Per-sample increment */
    float       sustain;     /* Sustain target level */
} CK_Envelope;

/* Voice state (one active tone) */
typedef struct {
    uint32_t      phase;           /* Phase accumulator (fixed-point) */
    uint32_t      phase_inc;       /* Phase increment per sample */
    uint8_t       waveform;        /* Active waveform type */
    CK_Envelope   env;             /* ADSR envelope */
    float         amplitude;       /* Base amplitude */
    float         breath_mod;      /* Breath cycle modulation 0.0-1.0 */
    float         btq_mod;         /* BTQ band modulation 0.0-1.0 */
    bool          active;          /* Is this voice sounding? */
} CK_Voice;

/* Audio engine state */
typedef struct {
    CK_Voice      voices[3];      /* Up to 3 simultaneous voices */
    uint8_t       current_op;     /* Current primary operator */
    uint8_t       prev_op;        /* Previous operator (for transitions) */
    uint32_t      sample_count;   /* Total samples generated */

    /* Wavetables (generated at init) */
    int16_t       wave_sine[CK_WAVE_SIZE];
    int16_t       wave_tri[CK_WAVE_SIZE];
    int16_t       wave_saw[CK_WAVE_SIZE];
    int16_t       wave_square[CK_WAVE_SIZE];

    /* DAC FIFO register address */
    uint32_t      dac_fifo_addr;

    /* LFSR for noise generation */
    uint32_t      noise_lfsr;
} CK_AudioEngine;

/* Initialize audio engine, generate wavetables */
void ck_audio_init(CK_AudioEngine* audio, uint32_t dac_fifo_addr);

/* Set the current operator (triggers tone transition) */
void ck_audio_set_operator(CK_AudioEngine* audio, uint8_t op);

/* Update breath modulation (call from body tick) */
void ck_audio_set_breath(CK_AudioEngine* audio, float breath_phase);

/* Update BTQ modulation (0.3 for RED, 0.6 for YELLOW, 1.0 for GREEN) */
void ck_audio_set_btq(CK_AudioEngine* audio, float btq_level);

/* Generate one audio sample and push to DAC FIFO.
 * Call this at CK_AUDIO_SAMPLE_RATE (44100 Hz) from timer ISR. */
void ck_audio_tick(CK_AudioEngine* audio);

/* Generate a block of samples (for DMA approach) */
void ck_audio_fill_buffer(CK_AudioEngine* audio, uint16_t* buf, uint32_t count);

/* Get the tone definition for an operator */
const CK_OperatorTone* ck_audio_get_tone(uint8_t op);

#endif /* CK_AUDIO_H */
