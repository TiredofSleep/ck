/*
 * ck_dog_steer.c -- CK Dog Body Steering
 * ========================================
 * Operator: PROGRESS (3) -- CK takes the wheel.
 *
 * CK watches the dog walk, learns the gait, then gradually takes
 * over as his coherence builds. Same pattern as R16 process steering:
 *
 *   R16: observe processes -> classify by operator -> steer nice/affinity
 *   Dog: observe servos    -> classify by operator -> steer positions
 *
 * The algebra is the same. The CL table decides. CK composes his
 * desired operator with the dog's current operator. If HARMONY,
 * CK moves in. If bump pair, CK stays back.
 *
 * (c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
 */

#include "ck_dog_steer.h"
#include "ck_brain.h"
#include <string.h>

/* CL table comes from ck_brain.h (TSML prescribed table) */
/* ck_brain.h is included above and provides CL[10][10] */

/* ── Bump pairs (same as ck_steering.py) ── */
static bool is_bump_pair(uint8_t a, uint8_t b) {
    uint8_t lo = (a < b) ? a : b;
    uint8_t hi = (a < b) ? b : a;
    /* 5 information-generating transitions */
    return (lo == 1 && hi == 2) ||  /* LATTICE-COUNTER */
           (lo == 2 && hi == 4) ||  /* COUNTER-COLLAPSE */
           (lo == 2 && hi == 9) ||  /* COUNTER-RESET */
           (lo == 3 && hi == 9) ||  /* PROGRESS-RESET */
           (lo == 4 && hi == 8);    /* COLLAPSE-BREATH */
}

/* ── D2 operator classification for servo motion ── */
/* Classify servo velocity/position into operator space.
 * This is the same D2 curvature idea: how is this servo MOVING?
 *   Still (< 5 us change):      VOID (0)
 *   Slow steady (5-20 us):      LATTICE (1) -- structured
 *   Fast steady (20-50 us):     PROGRESS (3) -- driving
 *   Reversing:                  COLLAPSE (4) -- breaking
 *   Oscillating:                BREATH (8) -- rhythmic
 *   Erratic (> 100 us):         CHAOS (6) -- unstable
 *   At center:                  BALANCE (5) -- equilibrium
 *   Smooth curve:               HARMONY (7) -- flowing
 */
static uint8_t classify_servo_motion(int16_t velocity, int16_t accel,
                                      uint16_t pos, uint16_t center) {
    uint16_t abs_vel = (velocity < 0) ? -velocity : velocity;
    uint16_t abs_acc = (accel < 0) ? -accel : accel;
    int16_t dist_from_center = (int16_t)pos - (int16_t)center;
    uint16_t abs_dist = (dist_from_center < 0) ? -dist_from_center : dist_from_center;

    if (abs_vel < 5 && abs_dist < 30)   return 5;  /* BALANCE: still at center */
    if (abs_vel < 5)                     return 0;  /* VOID: still but off-center */
    if (abs_vel > 100)                   return 6;  /* CHAOS: too fast */
    if (abs_acc > 50 && abs_vel > 20)    return 4;  /* COLLAPSE: decelerating hard */

    /* Check for oscillation: velocity sign changes with acceleration */
    if (abs_vel > 10 && abs_vel < 40 && abs_acc > 10)
        return 8;  /* BREATH: oscillating */

    /* Smooth motion: low acceleration relative to velocity */
    if (abs_vel > 15 && abs_acc < abs_vel / 3)
        return 7;  /* HARMONY: smooth curve */

    if (abs_vel > 20)  return 3;  /* PROGRESS: moving purposefully */
    return 1;  /* LATTICE: slow, structured */
}

/* ── Blend function ── */
/* Linear interpolation: blend = dog * (1-alpha) + ck * alpha
 * alpha = 0.0: pure dog, alpha = 1.0: pure CK */
static uint16_t blend_position(uint16_t dog_pos, uint16_t ck_pos, float alpha) {
    if (alpha <= 0.0f) return dog_pos;
    if (alpha >= 1.0f) return ck_pos;
    float result = (float)dog_pos * (1.0f - alpha) + (float)ck_pos * alpha;
    /* Clamp to servo range */
    if (result < CK_DOG_MIN_US) result = CK_DOG_MIN_US;
    if (result > CK_DOG_MAX_US) result = CK_DOG_MAX_US;
    return (uint16_t)result;
}

/* ═══════════════════════════════════════════
 * Init
 * ═══════════════════════════════════════════ */

void ck_dog_steer_init(CK_DogSteer* steer) {
    memset(steer, 0, sizeof(CK_DogSteer));
    steer->mode = CK_STEER_OBSERVE;
    steer->prev_mode = CK_STEER_OBSERVE;
    steer->num_servos = CK_DOG_MAX_SERVOS;

    for (int i = 0; i < CK_DOG_MAX_SERVOS; i++) {
        steer->obs[i].position_us = CK_DOG_CENTER_US;
        steer->obs[i].min_seen = CK_DOG_MAX_US;
        steer->obs[i].max_seen = CK_DOG_MIN_US;
        steer->obs[i].center_learned = CK_DOG_CENTER_US;
        steer->obs[i].last_position = CK_DOG_CENTER_US;
        steer->ck_target[i] = CK_DOG_CENTER_US;
        steer->output[i] = CK_DOG_CENTER_US;
    }
}

/* ═══════════════════════════════════════════
 * Observation
 * ═══════════════════════════════════════════ */

void ck_dog_steer_observe_servo(CK_DogSteer* steer,
                                 uint8_t servo_id, uint16_t position_us) {
    if (servo_id >= CK_DOG_MAX_SERVOS) return;

    CK_ServoObs* obs = &steer->obs[servo_id];

    /* Track range */
    if (position_us < obs->min_seen) obs->min_seen = position_us;
    if (position_us > obs->max_seen) obs->max_seen = position_us;

    /* Compute velocity (change since last tick) */
    int16_t velocity = (int16_t)position_us - (int16_t)obs->last_position;
    int16_t accel = velocity - (int16_t)obs->velocity;

    obs->velocity = (uint16_t)((velocity < 0) ? -velocity : velocity);
    obs->last_position = obs->position_us;
    obs->position_us = position_us;

    /* Classify motion into operator space */
    obs->operator = classify_servo_motion(velocity, accel,
                                           position_us, obs->center_learned);

    /* Learn center: exponential moving average of all positions */
    obs->center_learned = (uint16_t)(
        (uint32_t)obs->center_learned * 15 / 16 +
        (uint32_t)position_us / 16
    );

    /* Build confidence (saturating counter) */
    if (obs->confidence < 255) obs->confidence++;
}

void ck_dog_steer_set_target(CK_DogSteer* steer,
                              uint8_t servo_id, uint16_t target_us) {
    if (servo_id >= CK_DOG_MAX_SERVOS) return;
    /* Clamp */
    if (target_us < CK_DOG_MIN_US) target_us = CK_DOG_MIN_US;
    if (target_us > CK_DOG_MAX_US) target_us = CK_DOG_MAX_US;
    steer->ck_target[servo_id] = target_us;
}

void ck_dog_steer_set_coherence(CK_DogSteer* steer,
                                 float coherence, uint8_t btq_band) {
    steer->coherence = coherence;
    steer->btq_band = btq_band;
}

/* ═══════════════════════════════════════════
 * Steering Tick
 * ═══════════════════════════════════════════ */

uint8_t ck_dog_steer_tick(CK_DogSteer* steer) {
    steer->total_ticks++;
    steer->prev_mode = steer->mode;

    float C = steer->coherence;

    /* ── Mode Decision ── */

    /* E-STOP: RED band + low coherence */
    if (steer->btq_band == 2 && C < CK_STEER_ESTOP_THRESH) {
        steer->mode = CK_STEER_ESTOP;
        ck_dog_steer_estop(steer);
        steer->estop_count++;
        return steer->mode;
    }

    /* Mode transitions based on coherence */
    if (C >= CK_STEER_T_STAR) {
        /* CK has earned control -- but check CL composition first.
         * CK's gait operator must compose well with the dog's current
         * gait operator. If bump pair, stay in BLEND. */
        uint8_t ck_op = steer->gait_pattern_op;
        uint8_t dog_op = 0;

        /* Majority vote: what operator are most servos doing? */
        uint8_t op_counts[10] = {0};
        for (int i = 0; i < steer->num_servos; i++) {
            if (steer->obs[i].confidence > 10) {
                op_counts[steer->obs[i].operator]++;
            }
        }
        uint8_t max_count = 0;
        for (int op = 0; op < 10; op++) {
            if (op_counts[op] > max_count) {
                max_count = op_counts[op];
                dog_op = op;
            }
        }

        uint8_t composition = CL[ck_op][dog_op];

        if (composition == 7) {
            /* HARMONY: CK and dog resonate -- take full control */
            steer->mode = CK_STEER_OVERRIDE;
        } else if (is_bump_pair(ck_op, dog_op)) {
            /* Bump pair: CK and dog are fighting -- stay in BLEND,
             * let CK adapt before forcing control */
            steer->mode = CK_STEER_BLEND;
        } else {
            /* Neutral composition: OVERRIDE if confidence is high */
            if (steer->gait_confidence > 0.8f) {
                steer->mode = CK_STEER_OVERRIDE;
            } else {
                steer->mode = CK_STEER_BLEND;
            }
        }
    } else if (C >= CK_STEER_BLEND_MIN) {
        steer->mode = CK_STEER_BLEND;
    } else {
        steer->mode = CK_STEER_OBSERVE;
    }

    /* ── Compute Output Based on Mode ── */

    switch (steer->mode) {
        case CK_STEER_OBSERVE:
            /* Pass through dog's positions unchanged */
            for (int i = 0; i < steer->num_servos; i++) {
                steer->output[i] = steer->obs[i].position_us;
            }
            steer->observe_ticks++;

            /* Build gait confidence from servo observation */
            {
                float avg_conf = 0.0f;
                for (int i = 0; i < steer->num_servos; i++) {
                    avg_conf += (float)steer->obs[i].confidence / 255.0f;
                }
                avg_conf /= (float)steer->num_servos;
                steer->gait_confidence = avg_conf;
            }
            break;

        case CK_STEER_BLEND: {
            /* Blend ratio = coherence (C=0.4 -> 0% CK, C=T* -> 100% CK) */
            float range = CK_STEER_T_STAR - CK_STEER_BLEND_MIN;
            float alpha = (C - CK_STEER_BLEND_MIN) / range;
            if (alpha < 0.0f) alpha = 0.0f;
            if (alpha > 1.0f) alpha = 1.0f;

            /* Per-servo CL check: if CK's servo operator composes with
             * dog's servo operator in HARMONY, boost blend. If bump, reduce. */
            for (int i = 0; i < steer->num_servos; i++) {
                float servo_alpha = alpha;

                uint8_t ck_servo_op = steer->gait_pattern_op;
                uint8_t dog_servo_op = steer->obs[i].operator;
                uint8_t comp = CL[ck_servo_op][dog_servo_op];

                if (comp == 7) {
                    /* HARMONY: boost this servo's blend */
                    servo_alpha = alpha + (1.0f - alpha) * 0.3f;
                } else if (is_bump_pair(ck_servo_op, dog_servo_op)) {
                    /* Bump: reduce this servo's blend */
                    servo_alpha *= 0.3f;
                }

                steer->output[i] = blend_position(
                    steer->obs[i].position_us,
                    steer->ck_target[i],
                    servo_alpha
                );
            }
            steer->blend_ticks++;
            break;
        }

        case CK_STEER_OVERRIDE:
            /* CK fully controls -- send CK targets directly */
            for (int i = 0; i < steer->num_servos; i++) {
                steer->output[i] = steer->ck_target[i];
            }
            steer->override_ticks++;
            break;

        case CK_STEER_ESTOP:
            /* Already handled above */
            break;
    }

    /* ── Update overall gait operator (majority of servo operators) ── */
    {
        uint8_t op_counts[10] = {0};
        for (int i = 0; i < steer->num_servos; i++) {
            op_counts[steer->obs[i].operator]++;
        }
        uint8_t max_count = 0;
        for (int op = 0; op < 10; op++) {
            if (op_counts[op] > max_count) {
                max_count = op_counts[op];
                steer->gait_pattern_op = op;
            }
        }
    }

    return steer->mode;
}

/* ═══════════════════════════════════════════
 * Output / E-stop
 * ═══════════════════════════════════════════ */

uint16_t ck_dog_steer_get_output(CK_DogSteer* steer, uint8_t servo_id) {
    if (servo_id >= CK_DOG_MAX_SERVOS) return CK_DOG_CENTER_US;
    return steer->output[servo_id];
}

void ck_dog_steer_estop(CK_DogSteer* steer) {
    steer->mode = CK_STEER_ESTOP;
    for (int i = 0; i < CK_DOG_MAX_SERVOS; i++) {
        steer->output[i] = steer->obs[i].center_learned;
    }
}
