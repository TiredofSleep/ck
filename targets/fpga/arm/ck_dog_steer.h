/*
 * ck_dog_steer.h -- CK Dog Body Steering
 * ========================================
 * Operator: PROGRESS (3) -- CK takes the wheel.
 *
 * Same philosophy as R16 OS steering (ck_steering.py):
 *   - CK observes the dog's existing behavior
 *   - Classifies it by operator (what IS the gait doing?)
 *   - Gradually takes over as coherence builds
 *   - Emergency stops if coherence drops
 *
 * The dog already has a controller board with its own gait.
 * CK doesn't replace it -- CK STEERS it. When CK is coherent
 * enough (GREEN band, C > T*), CK's gait overrides the dog's.
 * When CK is uncertain (YELLOW/RED), CK observes and learns.
 *
 * Three steering modes:
 *   OBSERVE:  CK watches the dog's existing gait, learns servo positions
 *   BLEND:    CK's gait mixed with dog's (coherence = blend ratio)
 *   OVERRIDE: CK fully controls all servos (GREEN band only)
 *
 * Transition: OBSERVE -> BLEND -> OVERRIDE follows coherence.
 *   C < 0.4:         OBSERVE (CK is learning)
 *   0.4 <= C < T*:   BLEND (CK contributes proportionally)
 *   C >= T* (5/7):   OVERRIDE (CK has earned control)
 *   C < 0.2 + RED:   E-STOP (immediate center all servos)
 *
 * (c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
 */

#ifndef CK_DOG_STEER_H
#define CK_DOG_STEER_H

#include <stdint.h>
#include <stdbool.h>

/* ── Steering Modes ── */
#define CK_STEER_OBSERVE   0   /* Watch and learn */
#define CK_STEER_BLEND     1   /* Mix CK gait with dog gait */
#define CK_STEER_OVERRIDE  2   /* CK fully controls */
#define CK_STEER_ESTOP     3   /* Emergency stop */

/* ── Coherence Thresholds ── */
#define CK_STEER_T_STAR       0.714285f  /* 5/7 -- OVERRIDE threshold */
#define CK_STEER_BLEND_MIN    0.4f       /* Below this: OBSERVE only */
#define CK_STEER_ESTOP_THRESH 0.2f       /* E-stop threshold */

/* ── Servo Limits ── */
#define CK_DOG_MAX_SERVOS    12          /* 3 joints x 4 legs */
#define CK_DOG_CENTER_US     1500        /* Center position (microseconds) */
#define CK_DOG_MIN_US        500         /* Min servo range */
#define CK_DOG_MAX_US        2500        /* Max servo range */

/* ── Servo Observation (what CK sees the dog doing) ── */
typedef struct {
    uint16_t position_us;     /* Current position in microseconds */
    uint16_t velocity;        /* Change rate (us per tick) */
    uint8_t  operator;        /* D2-classified operator of this servo's motion */
    uint8_t  confidence;      /* How well CK understands this servo (0-255) */
    uint16_t min_seen;        /* Minimum position observed */
    uint16_t max_seen;        /* Maximum position observed */
    uint16_t center_learned;  /* Learned center position */
    uint16_t last_position;   /* Previous tick position */
} CK_ServoObs;

/* ── Dog Steering State ── */
typedef struct {
    /* Mode */
    uint8_t  mode;            /* Current steering mode */
    uint8_t  prev_mode;       /* Previous mode (for transition detection) */

    /* Coherence input (from brain via shared memory) */
    float    coherence;       /* Current C value */
    uint8_t  btq_band;        /* 0=GREEN, 1=YELLOW, 2=RED */

    /* Servo observations (what the dog is doing) */
    CK_ServoObs obs[CK_DOG_MAX_SERVOS];
    uint8_t  num_servos;      /* Number of active servos detected */

    /* CK's desired positions (from FPGA gait vortex) */
    uint16_t ck_target[CK_DOG_MAX_SERVOS];

    /* Blended output (what actually gets sent) */
    uint16_t output[CK_DOG_MAX_SERVOS];

    /* Gait phase tracking */
    uint32_t observe_ticks;   /* Ticks spent observing */
    uint32_t blend_ticks;     /* Ticks spent blending */
    uint32_t override_ticks;  /* Ticks spent in override */
    uint32_t estop_count;     /* Number of e-stops triggered */

    /* Learning */
    uint8_t  gait_pattern_op; /* D2 operator of the overall gait pattern */
    float    gait_confidence; /* How well CK understands the gait (0.0-1.0) */
    uint32_t total_ticks;     /* Total steering ticks */
} CK_DogSteer;

/* ── Functions ── */

/* Initialize steering engine */
void ck_dog_steer_init(CK_DogSteer* steer);

/* Main steering tick (called from Core 1 body loop at 50 Hz)
 * Reads coherence from shared memory, servo positions from dog,
 * decides mode, computes output positions.
 * Returns current steering mode. */
uint8_t ck_dog_steer_tick(CK_DogSteer* steer);

/* Feed an observed servo position from the dog's controller */
void ck_dog_steer_observe_servo(CK_DogSteer* steer,
                                 uint8_t servo_id, uint16_t position_us);

/* Set CK's desired target for a servo (from FPGA gait vortex) */
void ck_dog_steer_set_target(CK_DogSteer* steer,
                              uint8_t servo_id, uint16_t target_us);

/* Update coherence input (from brain shared memory) */
void ck_dog_steer_set_coherence(CK_DogSteer* steer,
                                 float coherence, uint8_t btq_band);

/* Get the blended output position for a servo */
uint16_t ck_dog_steer_get_output(CK_DogSteer* steer, uint8_t servo_id);

/* Force e-stop (centers all servos immediately) */
void ck_dog_steer_estop(CK_DogSteer* steer);

#endif /* CK_DOG_STEER_H */
