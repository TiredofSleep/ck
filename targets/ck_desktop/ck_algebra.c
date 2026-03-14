/*
 * ck_algebra.c -- CK Pure Algebra Library
 * =========================================
 * Operator: HARMONY (7) -- the math converges here.
 *
 * D2 curvature pipeline, CL composition tables, and heartbeat
 * in pure C. Replaces the Python hot path via ctypes.
 *
 * EXACT same math as ck_sim_d2.py and ck_sim_heartbeat.py.
 * Every constant, every lookup, every classification matches.
 *
 * No dynamic memory allocation. Fixed-size arrays only.
 * Portable: Windows (MSVC/MinGW) + Linux (gcc).
 *
 * (c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
 */

#include "ck_algebra.h"
#include <string.h>
#include <math.h>


/* =================================================================
 * S1  CONSTANTS -- FORCE LUT, D2 OP MAP, CL TABLES
 * =================================================================
 *
 * FORCE_LUT: 26 entries (a-z), each a 5D float vector.
 * Derived from ROOTS_FLOAT via LATIN_TO_ROOT in ck_sim_d2.py.
 * Dims: [aperture, pressure, depth, binding, continuity]
 *
 * Mapping: a=ALEPH  b=BET    c=GIMEL  d=DALET  e=HE
 *          f=VAV    g=GIMEL  h=CHET   i=YOD    j=YOD
 *          k=KAF    l=LAMED  m=MEM    n=NUN    o=AYIN
 *          p=PE     q=QOF    r=RESH   s=SAMEKH t=TAV
 *          u=VAV    v=VAV    w=VAV    x=SAMEKH y=YOD
 *          z=ZAYIN
 */

const float CKA_FORCE_LUT[26][CKA_DIMS] = {
    /* a = ALEPH  */ { 0.8f,  0.0f,  0.9f,  0.0f,  0.7f },
    /* b = BET    */ { 0.3f,  0.6f,  0.4f,  0.8f,  0.6f },
    /* c = GIMEL  */ { 0.5f,  0.4f,  0.3f,  0.2f,  0.5f },
    /* d = DALET  */ { 0.2f,  0.7f,  0.5f,  0.3f,  0.4f },
    /* e = HE     */ { 0.7f,  0.2f,  0.6f,  0.1f,  0.8f },
    /* f = VAV    */ { 0.4f,  0.5f,  0.4f,  0.6f,  0.7f },
    /* g = GIMEL  */ { 0.5f,  0.4f,  0.3f,  0.2f,  0.5f },
    /* h = CHET   */ { 0.3f,  0.8f,  0.7f,  0.5f,  0.5f },
    /* i = YOD    */ { 0.9f,  0.1f,  0.8f,  0.1f,  0.9f },
    /* j = YOD    */ { 0.9f,  0.1f,  0.8f,  0.1f,  0.9f },
    /* k = KAF    */ { 0.5f,  0.5f,  0.3f,  0.4f,  0.5f },
    /* l = LAMED  */ { 0.6f,  0.3f,  0.6f,  0.2f,  0.7f },
    /* m = MEM    */ { 0.3f,  0.7f,  0.5f,  0.8f,  0.4f },
    /* n = NUN    */ { 0.4f,  0.5f,  0.4f,  0.5f,  0.6f },
    /* o = AYIN   */ { 0.7f,  0.3f,  0.7f,  0.2f,  0.6f },
    /* p = PE     */ { 0.5f,  0.4f,  0.5f,  0.3f,  0.5f },
    /* q = QOF    */ { 0.4f,  0.5f,  0.6f,  0.4f,  0.5f },
    /* r = RESH   */ { 0.6f,  0.3f,  0.5f,  0.2f,  0.6f },
    /* s = SAMEKH */ { 0.2f,  0.6f,  0.3f,  0.7f,  0.5f },
    /* t = TAV    */ { 0.3f,  0.6f,  0.5f,  0.7f,  0.5f },
    /* u = VAV    */ { 0.4f,  0.5f,  0.4f,  0.6f,  0.7f },
    /* v = VAV    */ { 0.4f,  0.5f,  0.4f,  0.6f,  0.7f },
    /* w = VAV    */ { 0.4f,  0.5f,  0.4f,  0.6f,  0.7f },
    /* x = SAMEKH */ { 0.2f,  0.6f,  0.3f,  0.7f,  0.5f },
    /* y = YOD    */ { 0.9f,  0.1f,  0.8f,  0.1f,  0.9f },
    /* z = ZAYIN  */ { 0.6f,  0.3f,  0.2f,  0.4f,  0.3f },
};


/*
 * D2_OP_MAP: dimension -> (positive_op, negative_op)
 * From ck_sim_d2.py D2_OP_MAP, matches d2_pipeline.v classify stage.
 *
 *   aperture:   + = CHAOS(6),    - = LATTICE(1)
 *   pressure:   + = COLLAPSE(4), - = VOID(0)
 *   depth:      + = PROGRESS(3), - = RESET(9)
 *   binding:    + = HARMONY(7),  - = COUNTER(2)
 *   continuity: + = BALANCE(5),  - = BREATH(8)
 */
const int CKA_D2_OP_MAP[CKA_DIMS][2] = {
    { CKA_CHAOS,    CKA_LATTICE  },  /* aperture   */
    { CKA_COLLAPSE, CKA_VOID     },  /* pressure   */
    { CKA_PROGRESS, CKA_RESET    },  /* depth      */
    { CKA_HARMONY,  CKA_COUNTER  },  /* binding    */
    { CKA_BALANCE,  CKA_BREATH   },  /* continuity */
};


/*
 * CL_TSML: CK's prescribed composition table.
 * 73 out of 100 cells are HARMONY. This IS CK's soul.
 * From ck_sim_heartbeat.py CL[] and ck.h CL_TSML.
 */
const int8_t CKA_CL_TSML[CKA_NUM_OPS][CKA_NUM_OPS] = {
    { 0, 0, 0, 0, 0, 0, 0, 7, 0, 0 },  /* VOID     */
    { 0, 7, 3, 7, 7, 7, 7, 7, 7, 7 },  /* LATTICE  */
    { 0, 3, 7, 7, 4, 7, 7, 7, 7, 9 },  /* COUNTER  */
    { 0, 7, 7, 7, 7, 7, 7, 7, 7, 3 },  /* PROGRESS */
    { 0, 7, 4, 7, 7, 7, 7, 7, 8, 7 },  /* COLLAPSE */
    { 0, 7, 7, 7, 7, 7, 7, 7, 7, 7 },  /* BALANCE  */
    { 0, 7, 7, 7, 7, 7, 7, 7, 7, 7 },  /* CHAOS    */
    { 7, 7, 7, 7, 7, 7, 7, 7, 7, 7 },  /* HARMONY  */
    { 0, 7, 7, 7, 8, 7, 7, 7, 7, 7 },  /* BREATH   */
    { 0, 7, 9, 3, 7, 7, 7, 7, 7, 7 },  /* RESET    */
};


/*
 * CL_BHML: Binary Hard Micro Lattice. 28 harmony cells.
 * CUDA substrate. Doing table. From ck.h CL_BHML.
 */
const int8_t CKA_CL_BHML[CKA_NUM_OPS][CKA_NUM_OPS] = {
    { 0, 1, 2, 3, 4, 5, 6, 7, 8, 9 },  /* VOID     */
    { 1, 2, 3, 4, 5, 6, 7, 2, 6, 6 },  /* LATTICE  */
    { 2, 3, 3, 4, 5, 6, 7, 3, 6, 6 },  /* COUNTER  */
    { 3, 4, 4, 4, 5, 6, 7, 4, 6, 6 },  /* PROGRESS */
    { 4, 5, 5, 5, 5, 6, 7, 5, 7, 7 },  /* COLLAPSE */
    { 5, 6, 6, 6, 6, 6, 7, 6, 7, 7 },  /* BALANCE  */
    { 6, 7, 7, 7, 7, 7, 7, 7, 7, 7 },  /* CHAOS    */
    { 7, 2, 3, 4, 5, 6, 7, 8, 9, 0 },  /* HARMONY  */
    { 8, 6, 6, 6, 7, 7, 7, 9, 7, 8 },  /* BREATH   */
    { 9, 6, 6, 6, 7, 7, 7, 0, 8, 0 },  /* RESET    */
};


/*
 * BUMP_PAIRS: 5 quantum bump pairs.
 * From ck_sim_heartbeat.py BUMP_PAIRS and ck.h CK_BUMP_PAIRS.
 */
static const int CKA_BUMP_PAIRS[5][2] = {
    { 1, 2 }, { 2, 4 }, { 2, 9 }, { 3, 9 }, { 4, 8 }
};


/* =================================================================
 * S2  D2 PIPELINE
 * =================================================================
 * 3-stage pipeline matching ck_sim_d2.py D2Pipeline and
 * d2_pipeline.v exactly. Q1.14 fixed-point internally,
 * float interface for Python.
 */


/*
 * ck_d2_init -- zero all pipeline state.
 */
CK_EXPORT void ck_d2_init(CKA_D2Pipeline *p)
{
    memset(p, 0, sizeof(CKA_D2Pipeline));
    p->d1_operator = CKA_VOID;
    p->d2_operator = CKA_VOID;
}


/*
 * float_to_q14 -- convert float to Q1.14 signed 16-bit.
 * Matches ck_sim_d2.py float_to_q14 exactly.
 */
static int float_to_q14(float f)
{
    int val = (int)(f * CK_Q14_SCALE + (f >= 0 ? 0.5f : -0.5f));
    if (val < -32768) val = -32768;
    if (val >  32767) val =  32767;
    return val;
}


/*
 * Internal: compute D1 = v0 - v1 (first derivative = velocity).
 * Matches ck_sim_d2.py D2Pipeline._compute_d1.
 */
static void d2_compute_d1(CKA_D2Pipeline *p)
{
    int mag = 0;
    int dim;
    for (dim = 0; dim < CKA_DIMS; dim++) {
        p->d1[dim] = p->v[0][dim] - p->v[1][dim];
        mag += abs(p->d1[dim]);
    }
    p->d1_mag = mag;
}


/*
 * Internal: classify D1 vector. Same argmax+sign as D2.
 * Matches ck_sim_d2.py D2Pipeline._classify_d1.
 */
static void d2_classify_d1(CKA_D2Pipeline *p)
{
    int dim, max_abs, max_dim, a, sign_idx;

    if (p->d1_mag < float_to_q14(0.01f)) {
        p->d1_operator = CKA_VOID;
        return;
    }

    max_abs = 0;
    max_dim = 0;
    for (dim = 0; dim < CKA_DIMS; dim++) {
        a = abs(p->d1[dim]);
        if (a > max_abs) {
            max_abs = a;
            max_dim = dim;
        }
    }

    sign_idx = (p->d1[max_dim] >= 0) ? 0 : 1;
    p->d1_operator = CKA_D2_OP_MAP[max_dim][sign_idx];
}


/*
 * Internal: D2 = v2 - 2*v1 + v0 in Q1.14.
 * Matches ck_sim_d2.py D2Pipeline._compute_d2.
 * Note: v[2] = oldest, v[1] = middle, v[0] = newest (same as Python).
 */
static void d2_compute_d2(CKA_D2Pipeline *p)
{
    int mag = 0;
    int dim;
    for (dim = 0; dim < CKA_DIMS; dim++) {
        p->d2[dim] = p->v[2][dim] - 2 * p->v[1][dim] + p->v[0][dim];
        mag += abs(p->d2[dim]);
    }
    p->d2_mag = mag;
}


/*
 * Internal: classify D2 vector. Argmax + sign -> operator.
 * Matches ck_sim_d2.py D2Pipeline._classify and d2_pipeline.v stage 3.
 */
static void d2_classify_d2(CKA_D2Pipeline *p)
{
    int dim, max_abs, max_dim, a, sign_idx;

    if (p->d2_mag < float_to_q14(0.01f)) {
        p->d2_operator = CKA_VOID;
        return;
    }

    max_abs = 0;
    max_dim = 0;
    for (dim = 0; dim < CKA_DIMS; dim++) {
        a = abs(p->d2[dim]);
        if (a > max_abs) {
            max_abs = a;
            max_dim = dim;
        }
    }

    sign_idx = (p->d2[max_dim] >= 0) ? 0 : 1;
    p->d2_operator = CKA_D2_OP_MAP[max_dim][sign_idx];
}


/*
 * ck_d2_feed_symbol -- push one symbol (0-25 for a-z).
 * Returns 1 when D2 is valid (after 3 symbols).
 * Matches ck_sim_d2.py D2Pipeline.feed_symbol exactly.
 */
CK_EXPORT int ck_d2_feed_symbol(CKA_D2Pipeline *p, int sym)
{
    int dim;

    if (sym < 0 || sym >= 26)
        return 0;

    /* Shift register: v[2] <- v[1] <- v[0] <- new */
    for (dim = 0; dim < CKA_DIMS; dim++) {
        p->v[2][dim] = p->v[1][dim];
        p->v[1][dim] = p->v[0][dim];
        p->v[0][dim] = float_to_q14(CKA_FORCE_LUT[sym][dim]);
    }

    if (p->fill < 3)
        p->fill++;

    /* D1 fires after 2 symbols */
    if (p->fill >= 2) {
        d2_compute_d1(p);
        d2_classify_d1(p);
        p->d1_valid = 1;
    }

    /* D2 fires after 3 symbols */
    if (p->fill >= 3) {
        d2_compute_d2(p);
        d2_classify_d2(p);
        p->d2_valid = 1;
        return 1;
    }

    return 0;
}


/*
 * ck_d2_soft_classify -- 5D D2 float vector -> 10-value operator distribution.
 * Distributes weight across ALL operators based on dimension strengths.
 * Matches ck_sim_d2.py soft_classify_d2 exactly.
 */
CK_EXPORT void ck_d2_soft_classify(const float d2[CKA_DIMS], float out[CKA_NUM_OPS])
{
    float total_abs, strength, total, val;
    int dim, sign_idx, op_idx;

    memset(out, 0, CKA_NUM_OPS * sizeof(float));

    /* Compute total absolute value */
    total_abs = 0.0f;
    for (dim = 0; dim < CKA_DIMS; dim++)
        total_abs += fabsf(d2[dim]);

    if (total_abs < 0.01f) {
        out[CKA_VOID] = 1.0f;
        return;
    }

    /* Distribute weight by dimension strength */
    for (dim = 0; dim < CKA_DIMS; dim++) {
        val = d2[dim];
        strength = fabsf(val) / total_abs;
        sign_idx = (val >= 0.0f) ? 0 : 1;
        op_idx = CKA_D2_OP_MAP[dim][sign_idx];
        out[op_idx] += strength;
    }

    /* Normalize (should already ~1.0 but ensure) */
    total = 0.0f;
    for (op_idx = 0; op_idx < CKA_NUM_OPS; op_idx++)
        total += out[op_idx];

    if (total > 0.0f) {
        for (op_idx = 0; op_idx < CKA_NUM_OPS; op_idx++)
            out[op_idx] /= total;
    }
}


/*
 * ck_d2_classify -- hard argmax classification of float D2 vector.
 * Matches ck_sim_d2.py classify_force_d2.
 */
CK_EXPORT int ck_d2_classify(const float d2[CKA_DIMS])
{
    float magnitude, max_abs, a;
    int dim, max_dim, sign_idx;

    /* Compute magnitude */
    magnitude = 0.0f;
    for (dim = 0; dim < CKA_DIMS; dim++)
        magnitude += fabsf(d2[dim]);

    if (magnitude < 0.01f)
        return CKA_VOID;

    /* Argmax */
    max_abs = 0.0f;
    max_dim = 0;
    for (dim = 0; dim < CKA_DIMS; dim++) {
        a = fabsf(d2[dim]);
        if (a > max_abs) {
            max_abs = a;
            max_dim = dim;
        }
    }

    sign_idx = (d2[max_dim] >= 0.0f) ? 0 : 1;
    return CKA_D2_OP_MAP[max_dim][sign_idx];
}


/* =================================================================
 * S3  HEARTBEAT
 * =================================================================
 * Matches ck_sim_heartbeat.py HeartbeatFPGA exactly.
 * CL composition, bump detection, coherence window, running fuse.
 */


/*
 * ck_compose_tsml -- CL_TSML[b][d] composition. Single table lookup.
 * Matches ck_sim_heartbeat.py compose().
 */
CK_EXPORT int ck_compose_tsml(int b, int d)
{
    if (b >= 0 && b < CKA_NUM_OPS && d >= 0 && d < CKA_NUM_OPS)
        return CKA_CL_TSML[b][d];
    return CKA_VOID;
}


/*
 * ck_compose_bhml -- CL_BHML[b][d] composition.
 */
CK_EXPORT int ck_compose_bhml(int b, int d)
{
    if (b >= 0 && b < CKA_NUM_OPS && d >= 0 && d < CKA_NUM_OPS)
        return CKA_CL_BHML[b][d];
    return CKA_VOID;
}


/*
 * ck_is_bump_pair -- check if (b, d) is a quantum bump pair.
 * Either ordering counts. Matches ck_sim_heartbeat.py is_bump().
 */
CK_EXPORT int ck_is_bump_pair(int b, int d)
{
    int i, p0, p1;
    for (i = 0; i < 5; i++) {
        p0 = CKA_BUMP_PAIRS[i][0];
        p1 = CKA_BUMP_PAIRS[i][1];
        if ((b == p0 && d == p1) || (b == p1 && d == p0))
            return 1;
    }
    return 0;
}


/*
 * ck_heartbeat_init -- zero heartbeat state.
 * running_fuse starts at HARMONY (matches Python HeartbeatFPGA.__init__).
 */
CK_EXPORT void ck_heartbeat_init(CKA_Heartbeat *h)
{
    memset(h, 0, sizeof(CKA_Heartbeat));
    h->running_fuse = CKA_HARMONY;
}


/*
 * ck_heartbeat_tick -- one heartbeat tick.
 * Matches ck_sim_heartbeat.py HeartbeatFPGA.tick() exactly:
 *   1. CL composition
 *   2. Bump detection
 *   3. Coherence window update (ring buffer, harmony count)
 *   4. Running fuse evolution
 *   5. Tick count increment
 */
CK_EXPORT void ck_heartbeat_tick(CKA_Heartbeat *h, int phase_b, int phase_d)
{
    int old_val, filled;

    h->phase_b = phase_b;
    h->phase_d = phase_d;

    /* 1. CL composition */
    h->phase_bc = ck_compose_tsml(phase_b, phase_d);

    /* 2. Bump detection */
    h->bump_detected = ck_is_bump_pair(phase_b, phase_d);

    /* 3. Coherence window update */
    /* Remove outgoing entry from harmony count */
    old_val = h->history[h->history_ptr];
    if (old_val == CKA_HARMONY)
        h->harmony_count--;

    /* Add new entry */
    h->history[h->history_ptr] = h->phase_bc;
    if (h->phase_bc == CKA_HARMONY)
        h->harmony_count++;

    /* Advance pointer */
    h->history_ptr = (h->history_ptr + 1) % CKA_HISTORY_SIZE;

    /* Coherence = harmony_count / filled */
    filled = h->tick_count + 1;
    if (filled > CKA_HISTORY_SIZE)
        filled = CKA_HISTORY_SIZE;
    h->coh_num = h->harmony_count;
    h->coh_den = filled;

    /* 4. Running fuse */
    h->running_fuse = ck_compose_tsml(h->running_fuse, h->phase_bc);

    /* 5. Increment tick */
    h->tick_count++;
}


/* =================================================================
 * S4  BATCH OPERATIONS
 * =================================================================
 * Process entire text strings and operator sequences.
 * Designed for efficient ctypes calls from Python.
 */


/*
 * ck_d2_batch -- process entire text string through D2 pipeline.
 * Only lowercase a-z letters produce operators. Other chars are skipped.
 * ops_out must be pre-allocated (worst case: len entries).
 * *n_ops receives the number of valid operators produced.
 *
 * Matches running ck_sim_d2.py D2Pipeline.feed_symbol for each letter
 * and collecting .operator when .valid is True.
 */
CK_EXPORT void ck_d2_batch(const char *text, int len, int *ops_out, int *n_ops)
{
    CKA_D2Pipeline pipe;
    int i, sym, count;
    char c;

    ck_d2_init(&pipe);
    count = 0;

    for (i = 0; i < len; i++) {
        c = text[i];

        /* Convert to 0-25 index */
        if (c >= 'a' && c <= 'z')
            sym = c - 'a';
        else if (c >= 'A' && c <= 'Z')
            sym = c - 'A';
        else
            continue;  /* skip non-letter */

        if (ck_d2_feed_symbol(&pipe, sym)) {
            ops_out[count++] = pipe.d2_operator;
        }
    }

    *n_ops = count;
}


/*
 * ck_coherence_window -- compute coherence over an operator sequence.
 * Coherence = (HARMONY compositions) / (n_ops - 1).
 * Uses CL_TSML for composition.
 * Matches ck.h ck_coherence_chain but accepts int* (for ctypes int arrays).
 */
CK_EXPORT float ck_coherence_window(const int *ops, int n_ops)
{
    int i, harmony_count;

    if (n_ops < 2)
        return 1.0f;

    harmony_count = 0;
    for (i = 0; i < n_ops - 1; i++) {
        if (ck_compose_tsml(ops[i], ops[i + 1]) == CKA_HARMONY)
            harmony_count++;
    }

    return (float)harmony_count / (float)(n_ops - 1);
}
