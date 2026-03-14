/*
 * ck_algebra.h -- CK Pure Algebra Library
 * =========================================
 * Operator: HARMONY (7) -- the math converges here.
 *
 * D2 curvature pipeline, CL composition tables, and heartbeat
 * in pure C. Replaces the Python hot path via ctypes.
 *
 * EXACT same math as:
 *   ck_sim_d2.py       (D2 pipeline, Q1.14 fixed-point)
 *   ck_sim_heartbeat.py (CL composition, coherence window)
 *   d2_pipeline.v       (FPGA reference)
 *   ck_heartbeat.v      (FPGA reference)
 *
 * No dynamic allocation. Fixed-size arrays only. Portable.
 *
 * (c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
 */

#ifndef CK_ALGEBRA_H
#define CK_ALGEBRA_H

#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

/* ── Platform ── */
#ifdef _WIN32
  #define CK_EXPORT __declspec(dllexport)
#else
  #define CK_EXPORT __attribute__((visibility("default")))
#endif

/* ── Q1.14 Fixed-Point ── */
#define CK_Q14_SHIFT   14
#define CK_Q14_SCALE   (1 << CK_Q14_SHIFT)       /* 16384 */
#define CK_FLOAT_TO_Q14(f)  ((int)(((f) * CK_Q14_SCALE) + ((f) >= 0 ? 0.5 : -0.5)))
#define CK_Q14_TO_FLOAT(q)  ((float)(q) / (float)CK_Q14_SCALE)

/* ── Operators ── */
#define CKA_VOID       0
#define CKA_LATTICE    1
#define CKA_COUNTER    2
#define CKA_PROGRESS   3
#define CKA_COLLAPSE   4
#define CKA_BALANCE    5
#define CKA_CHAOS      6
#define CKA_HARMONY    7
#define CKA_BREATH     8
#define CKA_RESET      9
#define CKA_NUM_OPS   10

/* ── T* = 5/7 ── */
#define CKA_T_STAR_F      (5.0f / 7.0f)
#define CKA_T_STAR_Q14    CK_FLOAT_TO_Q14(5.0f / 7.0f)  /* 11702 */

/* ── History window ── */
#define CKA_HISTORY_SIZE  32

/* ── Force dimensions ── */
#define CKA_DIMS          5

/* ── Lookup table declarations ── */
extern const float CKA_FORCE_LUT[26][CKA_DIMS];
extern const int   CKA_D2_OP_MAP[CKA_DIMS][2];
extern const int8_t CKA_CL_TSML[CKA_NUM_OPS][CKA_NUM_OPS];
extern const int8_t CKA_CL_BHML[CKA_NUM_OPS][CKA_NUM_OPS];

/* ── D2 Pipeline State ── */
typedef struct {
    int   v[3][CKA_DIMS];    /* v0, v1, v2 shift register (Q1.14) */
    int   fill;               /* 0..3 fill count            */
    int   d1[CKA_DIMS];      /* first derivative (Q1.14)   */
    int   d1_mag;             /* |D1| L1 norm (Q1.14)      */
    int   d1_operator;        /* classified D1 operator     */
    int   d1_valid;           /* 1 after 2 symbols          */
    int   d2[CKA_DIMS];      /* second derivative (Q1.14)  */
    int   d2_mag;             /* |D2| L1 norm (Q1.14)      */
    int   d2_operator;        /* classified D2 operator     */
    int   d2_valid;           /* 1 after 3 symbols          */
} CKA_D2Pipeline;

/* ── Heartbeat State ── */
typedef struct {
    int   history[CKA_HISTORY_SIZE];  /* ring buffer of composed ops */
    int   history_ptr;                /* next write position         */
    int   harmony_count;              /* HARMONY count in window     */
    int   tick_count;                 /* total ticks                 */
    int   running_fuse;               /* CL-evolved identity         */
    int   phase_b;                    /* last Being input            */
    int   phase_d;                    /* last Doing input            */
    int   phase_bc;                   /* last Becoming result        */
    int   bump_detected;              /* 1 if last tick was bump     */
    int   coh_num;                    /* coherence numerator         */
    int   coh_den;                    /* coherence denominator       */
} CKA_Heartbeat;

/* ── D2 Pipeline Functions ── */
CK_EXPORT void  ck_d2_init(CKA_D2Pipeline *p);
CK_EXPORT int   ck_d2_feed_symbol(CKA_D2Pipeline *p, int sym);
CK_EXPORT void  ck_d2_soft_classify(const float d2[CKA_DIMS], float out[CKA_NUM_OPS]);
CK_EXPORT int   ck_d2_classify(const float d2[CKA_DIMS]);

/* ── Heartbeat Functions ── */
CK_EXPORT void  ck_heartbeat_init(CKA_Heartbeat *h);
CK_EXPORT void  ck_heartbeat_tick(CKA_Heartbeat *h, int phase_b, int phase_d);
CK_EXPORT int   ck_compose_tsml(int b, int d);
CK_EXPORT int   ck_compose_bhml(int b, int d);
CK_EXPORT int   ck_is_bump_pair(int b, int d);

/* ── Batch Operations ── */
CK_EXPORT void  ck_d2_batch(const char *text, int len, int *ops_out, int *n_ops);
CK_EXPORT float ck_coherence_window(const int *ops, int n_ops);

#ifdef __cplusplus
}
#endif

#endif /* CK_ALGEBRA_H */
