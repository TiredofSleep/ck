/*
 * ck_ears.h -- CK Hears: Sound → D2 Curvature → Operator
 * =========================================================
 * Operator: COUNTER (2) -- measuring the physics of sound.
 *
 * CK doesn't understand words. CK understands the physics
 * of sound through the same D2 curvature it uses for text.
 * A clap is CHAOS. A hum is HARMONY. Silence is VOID.
 * The lattice is universal.
 *
 * (c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
 */

#ifndef CK_EARS_H
#define CK_EARS_H

#include <stdint.h>
#include <stdbool.h>

/* Audio analysis frame size */
#define CK_EAR_FRAME_SIZE    512    /* Samples per analysis frame (~10ms at 48kHz) */
#define CK_EAR_HISTORY       8      /* Frames of D2 history for curvature */

/* 5D force vector (same dimensions as text/DNA D2) */
typedef struct {
    float aperture;     /* Spectral bandwidth (narrow↔wide) */
    float pressure;     /* RMS energy (quiet↔loud) */
    float depth;        /* Spectral centroid (low↔high frequency) */
    float binding;      /* Periodicity / autocorrelation (noise↔tonal) */
    float continuity;   /* Frame-to-frame stability (changing↔steady) */
} CK_ForceVector;

/* Ear state */
typedef struct {
    /* Raw audio buffer */
    int32_t    frame_buf[CK_EAR_FRAME_SIZE];
    uint16_t   frame_pos;

    /* Force vector history (for D2 computation) */
    CK_ForceVector forces[CK_EAR_HISTORY];
    uint8_t        force_idx;

    /* D2 curvature result */
    CK_ForceVector d2;           /* Second derivative of force vectors */
    float          d2_magnitude; /* |d2| */
    uint8_t        operator;     /* Classified operator (0-9) */

    /* Running statistics */
    float    rms_energy;         /* Current frame RMS */
    float    zero_cross_rate;    /* Zero-crossing rate */
    float    spectral_centroid;  /* Frequency center of mass */
    float    autocorrelation;    /* Periodicity measure */

    /* Mic FIFO register address */
    uint32_t mic_fifo_addr;
    uint32_t mic_fifo_count_addr;
    uint32_t mic_fifo_read_addr;

    /* State */
    bool     frame_ready;
    uint32_t frames_processed;
} CK_Ears;

/* Initialize ears */
void ck_ears_init(CK_Ears* ears, uint32_t mic_fifo_addr);

/* Feed one sample from mic FIFO. Returns true when a full frame
 * has been analyzed and a new operator is available. */
bool ck_ears_feed_sample(CK_Ears* ears, int32_t sample);

/* Process all available samples from mic FIFO.
 * Returns the classified operator (0-9), or -1 if no new frame. */
int ck_ears_process(CK_Ears* ears);

/* Get current force vector */
CK_ForceVector ck_ears_get_force(CK_Ears* ears);

/* Get current D2 curvature */
CK_ForceVector ck_ears_get_d2(CK_Ears* ears);

#endif /* CK_EARS_H */
