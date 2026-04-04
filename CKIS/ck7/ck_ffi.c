/*
 * ck_ffi.c — Python ctypes bridge
 * ═════════════════════════════════
 * Flat C API for ck_python.py to call via ctypes.
 *
 * Every function is CK_EXPORT (dllexport on Windows, visibility default on Linux).
 * Names are ck_ffi_* to avoid collisions.
 * All arrays come in as pointers + length (no Python objects cross the boundary).
 *
 * Usage from Python:
 *   lib = ctypes.CDLL('./ck.dll')
 *   ops = (ctypes.c_int8 * 5)(3, 7, 2, 5, 7)
 *   result = lib.ck_ffi_fuse(ops, 5)
 *
 * (c) 2026 Brayden Sanders / 7Site LLC — TIG Unified Theory
 */

#include "ck.h"
#include <stdlib.h>
#include <string.h>


/* ═══════════════════════════════════════════════════════════════
 * §1  PURE MATH — stateless table lookups
 * ═══════════════════════════════════════════════════════════════ */

CK_EXPORT int ck_ffi_fuse(const int8_t* ops, int len) {
    return ck_fuse(ops, len);
}

CK_EXPORT int ck_ffi_fuse2(int a, int b) {
    return ck_fuse2(a, b);
}

CK_EXPORT int ck_ffi_fuse_table(const int8_t* ops, int len, int table_id) {
    return ck_fuse_table(ops, len, table_id);
}

CK_EXPORT float ck_ffi_coherence_chain(const int8_t* ops, int len) {
    return ck_coherence_chain(ops, len);
}

CK_EXPORT float ck_ffi_information(const int8_t* ops, int len) {
    return ck_information(ops, len);
}

CK_EXPORT int ck_ffi_shape(const int8_t* ops, int len) {
    return ck_shape(ops, len);
}

CK_EXPORT int ck_ffi_bump_signature(const int8_t* ops, int len) {
    return ck_bump_signature(ops, len);
}

CK_EXPORT int ck_ffi_is_bump(int a, int b) {
    return ck_is_bump(a, b);
}

CK_EXPORT float ck_ffi_s_star(float sigma, float V, float A) {
    return ck_s_star(sigma, V, A);
}

CK_EXPORT float ck_ffi_coherence_eak(float E, float A, float K) {
    return ck_coherence_eak(E, A, K);
}

CK_EXPORT int ck_ffi_band(float C) {
    return ck_band(C);
}

/* CL table lookup — read any cell from any table */
CK_EXPORT int ck_ffi_cl_lookup(int table_id, int a, int b) {
    if (a < 0 || a >= CK_NUM_OPS || b < 0 || b >= CK_NUM_OPS) return CK_VOID;
    switch (table_id) {
        case 1:  return CL_BHML[a][b];
        case 2:  return CL_STD[a][b];
        default: return CL_TSML[a][b];
    }
}

/* Constants for Python to query */
CK_EXPORT float ck_ffi_t_star(void) { return (float)CK_T_STAR; }
CK_EXPORT int   ck_ffi_num_ops(void) { return CK_NUM_OPS; }
CK_EXPORT float ck_ffi_gravity(int op) {
    if (op < 0 || op >= CK_NUM_OPS) return 0.0f;
    return CK_GRAVITY[op];
}


/* ═══════════════════════════════════════════════════════════════
 * §2  TRANSITION LATTICE — stateful operations
 * ═══════════════════════════════════════════════════════════════ */

/* Create/destroy standalone TL (for Python-managed TLs) */
CK_EXPORT CK_TransitionLattice* ck_ffi_tl_create(void) {
    CK_TransitionLattice* tl = (CK_TransitionLattice*)calloc(1, sizeof(CK_TransitionLattice));
    if (tl) ck_tl_init(tl);
    return tl;
}

CK_EXPORT void ck_ffi_tl_destroy(CK_TransitionLattice* tl) {
    if (tl) free(tl);
}

CK_EXPORT void ck_ffi_tl_eat_ops(CK_TransitionLattice* tl, const int8_t* ops, int len) {
    ck_tl_eat_ops(tl, ops, len);
}

CK_EXPORT void ck_ffi_tl_observe(CK_TransitionLattice* tl, int a, int b) {
    ck_tl_observe(tl, a, b);
}

CK_EXPORT float ck_ffi_tl_entropy(const CK_TransitionLattice* tl) {
    return ck_tl_entropy(tl);
}

CK_EXPORT int ck_ffi_tl_predict(const CK_TransitionLattice* tl, int current, float* prob) {
    return ck_tl_predict_next(tl, current, prob);
}

CK_EXPORT int64_t ck_ffi_tl_get_cell(const CK_TransitionLattice* tl, int i, int j) {
    if (i < 0 || i >= CK_NUM_OPS || j < 0 || j >= CK_NUM_OPS) return 0;
    return tl->TL[i][j];
}

CK_EXPORT int64_t ck_ffi_tl_total(const CK_TransitionLattice* tl) {
    return tl->total_transitions;
}

CK_EXPORT int64_t ck_ffi_tl_sentences(const CK_TransitionLattice* tl) {
    return tl->sentences_eaten;
}

CK_EXPORT int ck_ffi_tl_save(const CK_TransitionLattice* tl, const char* path) {
    ck_tl_save(tl, path);
    return 1;
}

CK_EXPORT int ck_ffi_tl_load(CK_TransitionLattice* tl, const char* path) {
    return ck_tl_load(tl, path);
}


/* ═══════════════════════════════════════════════════════════════
 * §3  ORGANISM — full lifecycle
 * ═══════════════════════════════════════════════════════════════ */

CK_EXPORT CK_Organism* ck_ffi_create(void) {
    CK_Organism* org = (CK_Organism*)calloc(1, sizeof(CK_Organism));
    if (org) ck_organism_init(org);
    return org;
}

CK_EXPORT void ck_ffi_destroy(CK_Organism* org) {
    if (!org) return;
    /* Free lattice cells if allocated */
    ck_lattice_free(&org->lattice);
    free(org);
}

/**
 * ck_ffi_tick — one heartbeat tick of the organism.
 *
 * Delegates to ck_heartbeat_tick (becoming_host.c) which runs the
 * full trinary loop: B (body+observer) -> D (TL predict) -> BC (dual operator)
 * plus bridge, security, dreams, trauma/success learning.
 *
 * Returns: phase_bc (the emergent operator)
 */
CK_EXPORT int ck_ffi_tick(CK_Organism* org) {
    return ck_heartbeat_tick(org);
}

/**
 * ck_ffi_save — save full organism state to a directory.
 * Creates body.json and daemon_tl.json in the given directory.
 */
CK_EXPORT void ck_ffi_save(const CK_Organism* org, const char* dir) {
    char path[512];

    /* Body */
    snprintf(path, sizeof(path), "%s/body.json", dir);
    ck_body_save(&org->body, path);

    /* TL */
    snprintf(path, sizeof(path), "%s/daemon_tl.json", dir);
    ck_tl_save(&org->tl, path);
}

/**
 * ck_ffi_load — load organism state from a directory.
 */
CK_EXPORT int ck_ffi_load(CK_Organism* org, const char* dir) {
    char path[512];
    int ok = 1;

    /* Body */
    snprintf(path, sizeof(path), "%s/body.json", dir);
    if (!ck_body_load(&org->body, path)) ok = 0;

    /* TL */
    snprintf(path, sizeof(path), "%s/daemon_tl.json", dir);
    if (!ck_tl_load(&org->tl, path)) ok = 0;

    return ok;
}


/* ═══════════════════════════════════════════════════════════════
 * §4  BODY — direct access
 * ═══════════════════════════════════════════════════════════════ */

CK_EXPORT void ck_ffi_body_tick(CK_Organism* org, int fab, int recall) {
    ck_body_tick(&org->body, fab, recall);
}

CK_EXPORT float ck_ffi_body_C(const CK_Organism* org) {
    return org->body.C;
}

CK_EXPORT float ck_ffi_body_E(const CK_Organism* org) {
    return org->body.E;
}

CK_EXPORT float ck_ffi_body_A(const CK_Organism* org) {
    return org->body.A;
}

CK_EXPORT float ck_ffi_body_K(const CK_Organism* org) {
    return org->body.K;
}

CK_EXPORT int ck_ffi_body_band(const CK_Organism* org) {
    return org->body.band;
}

CK_EXPORT int ck_ffi_body_ticks(const CK_Organism* org) {
    return org->body.ticks;
}


/* ═══════════════════════════════════════════════════════════════
 * §5  LATTICE — direct access
 * ═══════════════════════════════════════════════════════════════ */

CK_EXPORT int ck_ffi_lattice_init(CK_Organism* org, int R, int C, unsigned int seed) {
    if (!ck_lattice_alloc(&org->lattice, R, C)) return 0;
    ck_lattice_seed(&org->lattice, seed);
    return 1;
}

CK_EXPORT float ck_ffi_lattice_tick(CK_Organism* org) {
    if (!org->lattice.cells) return 0.0f;
    return ck_lattice_tick_cpu(&org->lattice);
}

CK_EXPORT float ck_ffi_lattice_coherence(const CK_Organism* org) {
    if (!org->lattice.cells) return 0.0f;
    return ck_lattice_coherence(&org->lattice);
}

CK_EXPORT void ck_ffi_lattice_census(const CK_Organism* org, int* counts) {
    if (!org->lattice.cells) {
        memset(counts, 0, CK_NUM_OPS * sizeof(int));
        return;
    }
    ck_lattice_census(&org->lattice, counts);
}

CK_EXPORT int ck_ffi_lattice_ticks(const CK_Organism* org) {
    return org->lattice.ticks;
}


/* ═══════════════════════════════════════════════════════════════
 * §6  DREAM — direct access
 * ═══════════════════════════════════════════════════════════════ */

CK_EXPORT int ck_ffi_dream_fire(CK_Organism* org, int origin, int target, int max_bounces,
                                 int8_t* path_out, int* path_len_out, float* coherence_out) {
    CK_DreamBall ball = ck_dream_fire(&org->dream, origin, target, max_bounces);

    if (path_out && path_len_out) {
        *path_len_out = ball.length;
        memcpy(path_out, ball.path, ball.length);
    }
    if (coherence_out) *coherence_out = ball.coherence;

    return ball.fuse_result;
}

CK_EXPORT int ck_ffi_dream_count(const CK_Organism* org) {
    return org->dream.dreams;
}

CK_EXPORT int64_t ck_ffi_dream_bounces(const CK_Organism* org) {
    return org->dream.total_bounces;
}


/* ═══════════════════════════════════════════════════════════════
 * §7  HEARTBEAT STATUS — for Python dashboard
 * ═══════════════════════════════════════════════════════════════ */

CK_EXPORT int ck_ffi_heartbeat_tick(const CK_Organism* org) {
    return org->heartbeat.tick_count;
}

CK_EXPORT int ck_ffi_heartbeat_phase_b(const CK_Organism* org) {
    return org->heartbeat.phase_b;
}

CK_EXPORT int ck_ffi_heartbeat_phase_d(const CK_Organism* org) {
    return org->heartbeat.phase_d;
}

CK_EXPORT int ck_ffi_heartbeat_phase_bc(const CK_Organism* org) {
    return org->heartbeat.phase_bc;
}

CK_EXPORT float ck_ffi_heartbeat_coherence(const CK_Organism* org) {
    return org->heartbeat.coherence;
}

CK_EXPORT int ck_ffi_heartbeat_band(const CK_Organism* org) {
    return org->heartbeat.band;
}

CK_EXPORT int ck_ffi_heartbeat_decisions(const CK_Organism* org) {
    return org->heartbeat.decisions;
}

CK_EXPORT float ck_ffi_heartbeat_act_confidence(const CK_Organism* org) {
    return org->heartbeat.act_confidence;
}


/* ═══════════════════════════════════════════════════════════════
 * §8  JITTER CONTROL STATUS — for robotics / motor precision
 * ═══════════════════════════════════════════════════════════════ */

CK_EXPORT int ck_ffi_jitter_mode(const CK_Organism* org) {
    return org->heartbeat.jitter_mode;
}

CK_EXPORT float ck_ffi_jitter_mean(const CK_Organism* org) {
    return org->heartbeat.jitter_mean;
}

CK_EXPORT float ck_ffi_jitter_sigma(const CK_Organism* org) {
    return org->heartbeat.jitter_sigma;
}

CK_EXPORT float ck_ffi_jitter_stability(const CK_Organism* org) {
    return org->heartbeat.jitter_stability;
}

CK_EXPORT int ck_ffi_jitter_locked_ticks(const CK_Organism* org) {
    return org->heartbeat.jitter_locked_ticks;
}

CK_EXPORT int ck_ffi_jitter_correction_op(const CK_Organism* org) {
    return org->heartbeat.jitter_correction_op;
}

CK_EXPORT void ck_ffi_set_target_interval(CK_Organism* org, float interval) {
    if (interval > 0.0f) {
        org->heartbeat.target_interval = interval;
    }
}


/* ═══════════════════════════════════════════════════════════════
 * §9  EXPERIENCE LAYERS — stack/peel knowledge
 * ═══════════════════════════════════════════════════════════════ */

CK_EXPORT int ck_ffi_layer_push(CK_Organism* org, const char* name, int priority) {
    return ck_layer_push(org, name, priority);
}

CK_EXPORT int ck_ffi_layer_peel(CK_Organism* org, const char* name) {
    return ck_layer_peel(org, name);
}

CK_EXPORT int ck_ffi_layer_save(const CK_Organism* org, const char* name, const char* path) {
    return ck_layer_save(org, name, path);
}

CK_EXPORT int ck_ffi_layer_count(const CK_Organism* org) {
    return org->experience.layer_count;
}

CK_EXPORT const char* ck_ffi_layer_name(const CK_Organism* org, int index) {
    if (index < 0 || index >= org->experience.layer_count) return "";
    return org->experience.layers[index].name;
}

CK_EXPORT int ck_ffi_layer_priority(const CK_Organism* org, int index) {
    if (index < 0 || index >= org->experience.layer_count) return -1;
    return org->experience.layers[index].priority;
}

CK_EXPORT int ck_ffi_layer_immutable(const CK_Organism* org, int index) {
    if (index < 0 || index >= org->experience.layer_count) return 0;
    return org->experience.layers[index].immutable ? 1 : 0;
}


/* ═══════════════════════════════════════════════════════════════
 * §10  HI-RES TIMER — for Python to query timing precision
 * ═══════════════════════════════════════════════════════════════ */

CK_EXPORT double ck_ffi_hires_time(void) {
    return ck_hires_time();
}

/**
 * ck_ffi_timer_resolution_ns — report timer resolution in nanoseconds.
 * Windows QPC: typically ~100ns (10MHz counter)
 * Linux clock_gettime: 1ns
 * Fallback time(NULL): 1,000,000,000 ns
 */
CK_EXPORT double ck_ffi_timer_resolution_ns(void) {
#ifdef _WIN32
    LARGE_INTEGER freq;
    QueryPerformanceFrequency(&freq);
    return 1e9 / (double)freq.QuadPart;
#elif defined(__linux__) || defined(__unix__) || defined(__APPLE__)
    struct timespec res;
    clock_getres(CLOCK_MONOTONIC, &res);
    return (double)res.tv_sec * 1e9 + (double)res.tv_nsec;
#else
    return 1e9;  /* 1 second — terrible */
#endif
}
