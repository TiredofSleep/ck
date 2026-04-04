/*
 * ck_ears.c -- CK Hears: Sound → D2 Curvature → Operator
 * =========================================================
 * Operator: COUNTER (2) -- measuring the physics of sound.
 *
 * Audio feature extraction → 5D force vector → D2 curvature
 * → operator classification. Same math as text, different input.
 *
 * (c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
 */

#include "ck_ears.h"
#include "ck_brain.h"  /* REG_RD, operator constants */
#include <math.h>
#include <string.h>

/* ── Initialization ── */

void ck_ears_init(CK_Ears* ears, uint32_t mic_fifo_addr) {
    memset(ears, 0, sizeof(CK_Ears));
    ears->mic_fifo_addr = mic_fifo_addr;
    ears->operator = VOID;
}

/* ── Audio Feature Extraction ── */

static float compute_rms(const int32_t* buf, uint16_t len) {
    /* RMS energy of the frame */
    float sum_sq = 0.0f;
    for (uint16_t i = 0; i < len; i++) {
        float s = (float)buf[i] / 8388608.0f;  /* 24-bit signed → -1.0..1.0 */
        sum_sq += s * s;
    }
    return sqrtf(sum_sq / (float)len);
}

static float compute_zcr(const int32_t* buf, uint16_t len) {
    /* Zero-crossing rate: proxy for frequency content */
    uint32_t crossings = 0;
    for (uint16_t i = 1; i < len; i++) {
        if ((buf[i] >= 0 && buf[i-1] < 0) || (buf[i] < 0 && buf[i-1] >= 0)) {
            crossings++;
        }
    }
    return (float)crossings / (float)len;
}

static float compute_centroid(const int32_t* buf, uint16_t len) {
    /*
     * Spectral centroid approximation using zero-crossing rate.
     * True spectral centroid needs FFT. ZCR correlates well
     * with centroid for simple signals. Range: 0.0 (low freq) to 1.0 (high).
     */
    float zcr = compute_zcr(buf, len);
    /* Normalize: ZCR of 0.5 = Nyquist/2 = ~12kHz at 48kHz sample rate */
    return fminf(zcr * 2.0f, 1.0f);
}

static float compute_autocorrelation(const int32_t* buf, uint16_t len) {
    /*
     * Simple autocorrelation at lag = len/4 (~5ms at 48kHz with 512 samples).
     * High autocorrelation = tonal/periodic.
     * Low autocorrelation = noisy/chaotic.
     */
    uint16_t lag = len / 4;
    float num = 0.0f, denom = 0.0f;
    for (uint16_t i = 0; i < len - lag; i++) {
        float a = (float)buf[i] / 8388608.0f;
        float b = (float)buf[i + lag] / 8388608.0f;
        num += a * b;
        denom += a * a;
    }
    if (denom < 1e-10f) return 0.0f;
    float acr = num / denom;
    return fmaxf(fminf(acr, 1.0f), -1.0f);
}

/* ── Force Vector from Audio Features ── */

static CK_ForceVector features_to_force(float rms, float zcr,
                                          float centroid, float autocorr,
                                          float prev_rms) {
    CK_ForceVector f;

    /* Aperture: spectral bandwidth
     * Low ZCR + high autocorr = narrow (pure tone)
     * High ZCR + low autocorr = wide (noise) */
    f.aperture = (1.0f - autocorr) * zcr;

    /* Pressure: energy level */
    f.pressure = fminf(rms * 10.0f, 1.0f);  /* Scale up (mic signals are quiet) */

    /* Depth: spectral centroid (low freq = deep, high freq = shallow) */
    f.depth = centroid;

    /* Binding: periodicity (how tonal/structured the sound is) */
    f.binding = fmaxf(autocorr, 0.0f);

    /* Continuity: frame-to-frame stability */
    float energy_change = fabsf(rms - prev_rms);
    f.continuity = 1.0f - fminf(energy_change * 20.0f, 1.0f);

    return f;
}

/* ── D2 Curvature (same math as text D2, applied to sound) ── */

static CK_ForceVector compute_d2(CK_ForceVector v0, CK_ForceVector v1, CK_ForceVector v2) {
    /* Second derivative: d2 = v0 - 2*v1 + v2 */
    CK_ForceVector d2;
    d2.aperture   = v0.aperture   - 2.0f * v1.aperture   + v2.aperture;
    d2.pressure   = v0.pressure   - 2.0f * v1.pressure   + v2.pressure;
    d2.depth      = v0.depth      - 2.0f * v1.depth      + v2.depth;
    d2.binding    = v0.binding    - 2.0f * v1.binding     + v2.binding;
    d2.continuity = v0.continuity - 2.0f * v1.continuity  + v2.continuity;
    return d2;
}

static float d2_magnitude(CK_ForceVector d2) {
    return sqrtf(d2.aperture * d2.aperture +
                 d2.pressure * d2.pressure +
                 d2.depth * d2.depth +
                 d2.binding * d2.binding +
                 d2.continuity * d2.continuity);
}

/* ── Operator Classification from D2 ── */

static uint8_t classify_d2(CK_ForceVector d2, float magnitude) {
    /*
     * Same classification logic as text D2:
     * Find dominant dimension, use sign to pick operator.
     *
     * Dimension → Operator pairs:
     *   aperture+  = CHAOS (6)     aperture-  = LATTICE (1)
     *   pressure+  = COLLAPSE (4)  pressure-  = VOID (0)
     *   depth+     = PROGRESS (3)  depth-     = RESET (9)
     *   binding+   = HARMONY (7)   binding-   = COUNTER (2)
     *   continuity+= BALANCE (5)   continuity-= BREATH (8)
     */

    /* Near-zero magnitude: VOID (silence) */
    if (magnitude < 0.01f) return VOID;

    /* Find dominant dimension */
    float dims[5] = { d2.aperture, d2.pressure, d2.depth,
                       d2.binding, d2.continuity };
    float max_abs = 0.0f;
    int max_dim = 0;

    for (int i = 0; i < 5; i++) {
        float a = fabsf(dims[i]);
        if (a > max_abs) {
            max_abs = a;
            max_dim = i;
        }
    }

    /* Map dimension + sign to operator */
    static const uint8_t OP_MAP[5][2] = {
        /* dim          positive    negative */
        /* aperture  */ { CHAOS,     LATTICE  },
        /* pressure  */ { COLLAPSE,  VOID     },
        /* depth     */ { PROGRESS,  RESET    },
        /* binding   */ { HARMONY,   COUNTER  },
        /* continuity*/ { BALANCE,   BREATH   },
    };

    int sign_idx = (dims[max_dim] >= 0.0f) ? 0 : 1;
    return OP_MAP[max_dim][sign_idx];
}

/* ── Feed One Sample ── */

bool ck_ears_feed_sample(CK_Ears* ears, int32_t sample) {
    ears->frame_buf[ears->frame_pos++] = sample;

    if (ears->frame_pos < CK_EAR_FRAME_SIZE) {
        return false;  /* Frame not yet full */
    }

    /* Frame complete -- analyze */
    ears->frame_pos = 0;

    /* 1. Extract features */
    float prev_rms = ears->rms_energy;
    ears->rms_energy = compute_rms(ears->frame_buf, CK_EAR_FRAME_SIZE);
    ears->zero_cross_rate = compute_zcr(ears->frame_buf, CK_EAR_FRAME_SIZE);
    ears->spectral_centroid = compute_centroid(ears->frame_buf, CK_EAR_FRAME_SIZE);
    ears->autocorrelation = compute_autocorrelation(ears->frame_buf, CK_EAR_FRAME_SIZE);

    /* 2. Build force vector */
    CK_ForceVector force = features_to_force(
        ears->rms_energy, ears->zero_cross_rate,
        ears->spectral_centroid, ears->autocorrelation,
        prev_rms
    );

    /* 3. Store in history ring */
    ears->forces[ears->force_idx] = force;
    ears->force_idx = (ears->force_idx + 1) % CK_EAR_HISTORY;

    /* 4. Compute D2 curvature (need at least 3 frames) */
    if (ears->frames_processed >= 2) {
        uint8_t i2 = (ears->force_idx + CK_EAR_HISTORY - 1) % CK_EAR_HISTORY;
        uint8_t i1 = (ears->force_idx + CK_EAR_HISTORY - 2) % CK_EAR_HISTORY;
        uint8_t i0 = (ears->force_idx + CK_EAR_HISTORY - 3) % CK_EAR_HISTORY;

        ears->d2 = compute_d2(ears->forces[i0], ears->forces[i1], ears->forces[i2]);
        ears->d2_magnitude = d2_magnitude(ears->d2);

        /* 5. Classify operator */
        ears->operator = classify_d2(ears->d2, ears->d2_magnitude);
    }

    ears->frames_processed++;
    ears->frame_ready = true;

    return true;
}

/* ── Process Available Mic Samples ── */

int ck_ears_process(CK_Ears* ears) {
    ears->frame_ready = false;

    /* Read available samples from mic FIFO (via AXI register) */
    /* The I2S receiver writes 24-bit samples to a FIFO.
     * ARM reads sample_out register, then pulses sample_read. */
    uint32_t available = REG_RD(ears->mic_fifo_count_addr);

    for (uint32_t i = 0; i < available; i++) {
        /* Read 24-bit sample, sign-extend to 32-bit */
        int32_t sample = (int32_t)(REG_RD(ears->mic_fifo_addr) & 0xFFFFFF);
        if (sample & 0x800000) sample |= 0xFF000000;  /* Sign extend */

        /* Acknowledge read */
        REG_WR(ears->mic_fifo_read_addr, 1);

        if (ck_ears_feed_sample(ears, sample)) {
            /* New frame analyzed, operator available */
            return (int)ears->operator;
        }
    }

    return -1;  /* No new frame yet */
}

CK_ForceVector ck_ears_get_force(CK_Ears* ears) {
    uint8_t latest = (ears->force_idx + CK_EAR_HISTORY - 1) % CK_EAR_HISTORY;
    return ears->forces[latest];
}

CK_ForceVector ck_ears_get_d2(CK_Ears* ears) {
    return ears->d2;
}
