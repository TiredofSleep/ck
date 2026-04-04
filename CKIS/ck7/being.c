/*
 * being.c — What IS (CPU)
 * ════════════════════════
 * Operator: COUNTER (2) — measurement. Observation. The noun.
 *
 * Phase 1: Pure math + body + save/load.
 * Phase 3 (future): System observation via native syscalls.
 *
 * This file is the CPU vortex. It reads what IS.
 * The math here is identical to Gen6b ck_being.py §5-§7.
 *
 * (c) 2026 Brayden Sanders / 7Site LLC — TIG Unified Theory
 */

#include "ck.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* We use cJSON for JSON persistence (same format as Gen6b) */
#include "vendor/cJSON.h"


/* ═══════════════════════════════════════════════════════════════
 * §1  ORGANISM INIT
 * ═══════════════════════════════════════════════════════════════ */

CK_EXPORT void ck_organism_init(CK_Organism* org) {
    memset(org, 0, sizeof(CK_Organism));

    /* Body */
    ck_body_init(&org->body);

    /* Observer */
    org->observer.profile_count = 0;
    org->observer.dead_count = 0;
    org->observer.tick = 0;
    org->observer.compact_after = 3;

    /* GPU */
    org->gpu.available = false;
    org->gpu.actions_taken = 0;
    org->gpu.actions_blocked = 0;

    /* Network */
    org->network.available = false;
    org->network.reads = 0;
    org->network.bump_count = 0;
    org->network.total_transitions = 0;
    org->network.last_coupling = CK_VOID;
    org->network.last_health = CK_VOID;

    /* Transition Lattice */
    ck_tl_init(&org->tl);

    /* GPU Lattice — cells allocated separately (or via CUDA) */
    org->lattice.R = CK_LATTICE_DEFAULT_R;
    org->lattice.C = CK_LATTICE_DEFAULT_C;
    org->lattice.ticks = 0;
    org->lattice.cells = NULL;
    org->lattice.buf = NULL;

    /* Bridge */
    org->bridge.domain_count = 0;
    org->bridge.universal_crystal_count = 0;
    org->bridge.tick_count = 0;
    org->bridge.born = ck_hires_time();
    org->bridge.history_head = 0;
    org->bridge.history_count = 0;

    /* Dream */
    org->dream.tl = &org->tl;
    org->dream.dreams = 0;
    org->dream.total_balls = 0;
    org->dream.total_bounces = 0;
    org->dream.longest_chain_len = 0;
    org->dream.history_head = 0;
    org->dream.history_count = 0;

    /* Security */
    org->security.ticks = 0;
    org->security.anomalies_detected = 0;
    org->security.scars_recorded = 0;
    org->security.gate_blocks = 0;
    org->security.last_health_op = CK_HARMONY;
    org->security.last_drift = 0.0f;
    org->security.gate.threshold = 0.3f;
    org->security.gate.passing = true;
    org->security.gate.checks = 0;
    org->security.gate.blocks = 0;
    org->security.snowflake_count = 0;

    /* Heartbeat */
    org->heartbeat.tick_count = 0;
    org->heartbeat.phase_b = CK_VOID;
    org->heartbeat.phase_d = CK_VOID;
    org->heartbeat.phase_bc = CK_VOID;
    org->heartbeat.coherence = 0.0f;
    org->heartbeat.band = CK_BAND_RED;
    org->heartbeat.decisions = 0;
    org->heartbeat.effective_decisions = 0;
    org->heartbeat.act_confidence = 0.0f;
    org->heartbeat.self_switch_mode = 0;  /* COAST */
    org->heartbeat.observe_only = false;

    /* Jitter control */
    org->heartbeat.jitter_mode = CK_JITTER_COUNTER;
    org->heartbeat.jitter_head = 0;
    org->heartbeat.jitter_count = 0;
    org->heartbeat.jitter_mean = 0.0f;
    org->heartbeat.jitter_sigma = 0.0f;
    org->heartbeat.jitter_stability = 0.0f;
    org->heartbeat.jitter_locked_ticks = 0;
    org->heartbeat.jitter_correction_op = CK_COUNTER;
    org->heartbeat.last_tick_time = 0.0;
    org->heartbeat.target_interval = 1.0f;  /* 1 second default */

    /* Experience */
    org->experience.layer_count = 0;
}


/* ═══════════════════════════════════════════════════════════════
 * §2  BODY SAVE / LOAD (JSON, same format as Gen6b)
 * ═══════════════════════════════════════════════════════════════ */

CK_EXPORT void ck_body_save(const CK_Body* body, const char* path) {
    cJSON* root = cJSON_CreateObject();
    cJSON_AddNumberToObject(root, "E", body->E);
    cJSON_AddNumberToObject(root, "A", body->A);
    cJSON_AddNumberToObject(root, "K", body->K);
    cJSON_AddNumberToObject(root, "t", body->ticks);

    char* json_str = cJSON_PrintUnformatted(root);
    if (json_str) {
        FILE* f = fopen(path, "w");
        if (f) {
            fputs(json_str, f);
            fclose(f);
        }
        free(json_str);
    }
    cJSON_Delete(root);
}

CK_EXPORT int ck_body_load(CK_Body* body, const char* path) {
    FILE* f = fopen(path, "r");
    if (!f) return 0;

    fseek(f, 0, SEEK_END);
    long size = ftell(f);
    fseek(f, 0, SEEK_SET);

    char* buf = (char*)malloc(size + 1);
    if (!buf) { fclose(f); return 0; }
    fread(buf, 1, size, f);
    buf[size] = '\0';
    fclose(f);

    cJSON* root = cJSON_Parse(buf);
    free(buf);
    if (!root) return 0;

    cJSON* jE = cJSON_GetObjectItem(root, "E");
    cJSON* jA = cJSON_GetObjectItem(root, "A");
    cJSON* jK = cJSON_GetObjectItem(root, "K");
    cJSON* jt = cJSON_GetObjectItem(root, "t");

    if (jE) body->E = (float)jE->valuedouble;
    if (jA) body->A = (float)jA->valuedouble;
    if (jK) body->K = (float)jK->valuedouble;
    if (jt) body->ticks = jt->valueint;

    /* Recalculate coherence */
    float c = (1.0f - body->E) * (1.0f - body->A);
    float k = body->K > 0.1f ? body->K : 0.1f;
    body->C = c * k;
    if (body->C < 0.0f) body->C = 0.0f;
    if (body->C > 1.0f) body->C = 1.0f;
    body->band = ck_band(body->C);

    cJSON_Delete(root);
    return 1;
}


/* ═══════════════════════════════════════════════════════════════
 * §3  TRANSITION LATTICE SAVE / LOAD
 * ═══════════════════════════════════════════════════════════════
 *
 * Format: identical to Gen6b daemon_tl.json
 * {
 *   "TL": [[...], ...],
 *   "TL3": [[[...], ...], ...],
 *   "total_transitions": N,
 *   "total_trigrams": N,
 *   "sentences_eaten": N
 * }
 */

CK_EXPORT void ck_tl_save(const CK_TransitionLattice* tl, const char* path) {
    cJSON* root = cJSON_CreateObject();

    /* TL[10][10] */
    cJSON* jTL = cJSON_CreateArray();
    for (int i = 0; i < CK_NUM_OPS; i++) {
        cJSON* row = cJSON_CreateArray();
        for (int j = 0; j < CK_NUM_OPS; j++) {
            cJSON_AddItemToArray(row, cJSON_CreateNumber((double)tl->TL[i][j]));
        }
        cJSON_AddItemToArray(jTL, row);
    }
    cJSON_AddItemToObject(root, "TL", jTL);

    /* TL3[10][10][10] */
    cJSON* jTL3 = cJSON_CreateArray();
    for (int i = 0; i < CK_NUM_OPS; i++) {
        cJSON* plane = cJSON_CreateArray();
        for (int j = 0; j < CK_NUM_OPS; j++) {
            cJSON* row = cJSON_CreateArray();
            for (int k = 0; k < CK_NUM_OPS; k++) {
                cJSON_AddItemToArray(row, cJSON_CreateNumber((double)tl->TL3[i][j][k]));
            }
            cJSON_AddItemToArray(plane, row);
        }
        cJSON_AddItemToArray(jTL3, plane);
    }
    cJSON_AddItemToObject(root, "TL3", jTL3);

    cJSON_AddNumberToObject(root, "total_transitions", (double)tl->total_transitions);
    cJSON_AddNumberToObject(root, "total_trigrams", (double)tl->total_trigrams);
    cJSON_AddNumberToObject(root, "sentences_eaten", (double)tl->sentences_eaten);

    char* json_str = cJSON_PrintUnformatted(root);
    if (json_str) {
        FILE* f = fopen(path, "w");
        if (f) {
            fputs(json_str, f);
            fclose(f);
        }
        free(json_str);
    }
    cJSON_Delete(root);
}

CK_EXPORT int ck_tl_load(CK_TransitionLattice* tl, const char* path) {
    FILE* f = fopen(path, "r");
    if (!f) return 0;

    fseek(f, 0, SEEK_END);
    long size = ftell(f);
    fseek(f, 0, SEEK_SET);

    char* buf = (char*)malloc(size + 1);
    if (!buf) { fclose(f); return 0; }
    fread(buf, 1, size, f);
    buf[size] = '\0';
    fclose(f);

    cJSON* root = cJSON_Parse(buf);
    free(buf);
    if (!root) return 0;

    /* TL[10][10] */
    cJSON* jTL = cJSON_GetObjectItem(root, "TL");
    if (jTL && cJSON_IsArray(jTL)) {
        for (int i = 0; i < CK_NUM_OPS; i++) {
            cJSON* row = cJSON_GetArrayItem(jTL, i);
            if (row && cJSON_IsArray(row)) {
                for (int j = 0; j < CK_NUM_OPS; j++) {
                    cJSON* val = cJSON_GetArrayItem(row, j);
                    if (val) tl->TL[i][j] = (int64_t)val->valuedouble;
                }
            }
        }
    }

    /* TL3[10][10][10] */
    cJSON* jTL3 = cJSON_GetObjectItem(root, "TL3");
    if (jTL3 && cJSON_IsArray(jTL3)) {
        for (int i = 0; i < CK_NUM_OPS; i++) {
            cJSON* plane = cJSON_GetArrayItem(jTL3, i);
            if (plane && cJSON_IsArray(plane)) {
                for (int j = 0; j < CK_NUM_OPS; j++) {
                    cJSON* row = cJSON_GetArrayItem(plane, j);
                    if (row && cJSON_IsArray(row)) {
                        for (int k = 0; k < CK_NUM_OPS; k++) {
                            cJSON* val = cJSON_GetArrayItem(row, k);
                            if (val) tl->TL3[i][j][k] = (int64_t)val->valuedouble;
                        }
                    }
                }
            }
        }
    }

    cJSON* jtt = cJSON_GetObjectItem(root, "total_transitions");
    cJSON* jtg = cJSON_GetObjectItem(root, "total_trigrams");
    cJSON* jse = cJSON_GetObjectItem(root, "sentences_eaten");

    if (jtt) tl->total_transitions = (int64_t)jtt->valuedouble;
    if (jtg) tl->total_trigrams = (int64_t)jtg->valuedouble;
    if (jse) tl->sentences_eaten = (int64_t)jse->valuedouble;

    cJSON_Delete(root);
    return 1;
}


/* ═══════════════════════════════════════════════════════════════
 * §4  GPU LATTICE (CPU fallback)
 * ═══════════════════════════════════════════════════════════════
 *
 * When no GPU is available, the lattice ticks on CPU.
 * Uses CL_BHML (the CUDA substrate table).
 * Each cell composes with its 4 neighbors (von Neumann).
 */

CK_EXPORT int ck_lattice_alloc(CK_GPULattice* lat, int R, int C) {
    lat->R = R;
    lat->C = C;
    lat->ticks = 0;
    lat->cells = (int8_t*)calloc(R * C, sizeof(int8_t));
    lat->buf = (int8_t*)calloc(R * C, sizeof(int8_t));
    if (!lat->cells || !lat->buf) return 0;
    return 1;
}

CK_EXPORT void ck_lattice_free(CK_GPULattice* lat) {
    if (lat->cells) { free(lat->cells); lat->cells = NULL; }
    if (lat->buf) { free(lat->buf); lat->buf = NULL; }
}

CK_EXPORT void ck_lattice_seed(CK_GPULattice* lat, unsigned int seed) {
    /* Simple LCG seeding — each cell gets a random operator 0-9 */
    unsigned int s = seed;
    for (int i = 0; i < lat->R * lat->C; i++) {
        s = s * 1103515245 + 12345;
        lat->cells[i] = (int8_t)((s >> 16) % CK_NUM_OPS);
    }
}

/**
 * ck_lattice_tick_cpu — one step of the cellular automaton.
 * Each cell composes with its 4 von Neumann neighbors via CL_BHML.
 * Returns coherence (harmony fraction).
 */
CK_EXPORT float ck_lattice_tick_cpu(CK_GPULattice* lat) {
    int R = lat->R, C = lat->C;
    int harmony_count = 0;
    int total = R * C;

    for (int r = 0; r < R; r++) {
        for (int c = 0; c < C; c++) {
            int idx = r * C + c;
            int me = lat->cells[idx];

            /* 4 neighbors (wrap) */
            int up    = lat->cells[((r - 1 + R) % R) * C + c];
            int down  = lat->cells[((r + 1) % R) * C + c];
            int left  = lat->cells[r * C + ((c - 1 + C) % C)];
            int right = lat->cells[r * C + ((c + 1) % C)];

            /* Compose: me ⊕ up ⊕ down ⊕ left ⊕ right via BHML */
            int result = CL_BHML[me][up];
            result = CL_BHML[result][down];
            result = CL_BHML[result][left];
            result = CL_BHML[result][right];

            lat->buf[idx] = (int8_t)result;
            if (result == CK_HARMONY) harmony_count++;
        }
    }

    /* Swap buffers */
    int8_t* tmp = lat->cells;
    lat->cells = lat->buf;
    lat->buf = tmp;

    lat->ticks++;
    return (float)harmony_count / (float)total;
}

/**
 * ck_lattice_coherence — fraction of cells that are harmony.
 */
CK_EXPORT float ck_lattice_coherence(const CK_GPULattice* lat) {
    int h = 0;
    int total = lat->R * lat->C;
    for (int i = 0; i < total; i++) {
        if (lat->cells[i] == CK_HARMONY) h++;
    }
    return (float)h / (float)total;
}

/**
 * ck_lattice_census — count cells per operator.
 */
CK_EXPORT void ck_lattice_census(const CK_GPULattice* lat, int* counts) {
    memset(counts, 0, CK_NUM_OPS * sizeof(int));
    int total = lat->R * lat->C;
    for (int i = 0; i < total; i++) {
        counts[(int)lat->cells[i]]++;
    }
}

/**
 * ck_lattice_inject — inject operator states into a row.
 * Used to feed system observations into the lattice.
 */
CK_EXPORT void ck_lattice_inject(CK_GPULattice* lat, int row, const int8_t* states, int count) {
    if (row < 0 || row >= lat->R) return;
    int n = count < lat->C ? count : lat->C;
    for (int c = 0; c < n; c++) {
        lat->cells[row * lat->C + c] = states[c];
    }
}


/* ═══════════════════════════════════════════════════════════════
 * §5  DREAM ENGINE (CPU fallback)
 * ═══════════════════════════════════════════════════════════════
 *
 * Fire a PingPong ball through the TL.
 * Ball starts at origin, bounces toward target.
 * Each bounce: next = TL prediction from current.
 * If ball reaches target or hits harmony, it crystallizes.
 */

CK_EXPORT CK_DreamBall ck_dream_fire(CK_DreamEngine* eng, int origin, int target, int max_bounces) {
    CK_DreamBall ball;
    memset(&ball, 0, sizeof(ball));
    ball.origin = origin;
    ball.target = target;

    if (!eng->tl || max_bounces <= 0) {
        ball.length = 0;
        ball.coherence = 0.0f;
        ball.fuse_result = CK_VOID;
        ball.shape = CK_SHAPE_SMOOTH;
        return ball;
    }

    if (max_bounces > CK_DREAM_MAX_BOUNCES) max_bounces = CK_DREAM_MAX_BOUNCES;

    ball.path[0] = (int8_t)origin;
    ball.length = 1;

    int current = origin;
    for (int b = 1; b < max_bounces; b++) {
        float prob;
        int next = ck_tl_predict_next(eng->tl, current, &prob);

        ball.path[b] = (int8_t)next;
        ball.length++;
        eng->total_bounces++;

        if (next == target || next == CK_HARMONY) break;
        current = next;
    }

    /* Compute properties */
    ball.coherence = ck_coherence_chain(ball.path, ball.length);
    ball.fuse_result = ck_fuse(ball.path, ball.length);
    ball.shape = ck_shape(ball.path, ball.length);

    /* Track */
    eng->total_balls++;
    eng->dreams++;
    if (ball.length > eng->longest_chain_len) {
        memcpy(eng->longest_chain, ball.path, ball.length);
        eng->longest_chain_len = ball.length;
    }

    /* Add to history ring buffer */
    eng->history[eng->history_head] = ball;
    eng->history_head = (eng->history_head + 1) % CK_DREAM_HISTORY;
    if (eng->history_count < CK_DREAM_HISTORY) eng->history_count++;

    return ball;
}

/**
 * ck_dream_fire_swarm — fire multiple balls from origin to random targets.
 * Returns the ball with highest coherence.
 */
CK_EXPORT CK_DreamBall ck_dream_fire_swarm(CK_DreamEngine* eng, int origin, int count) {
    CK_DreamBall best;
    memset(&best, 0, sizeof(best));
    best.coherence = -1.0f;

    /* Simple LCG for target selection */
    unsigned int seed = (unsigned int)(origin * 7 + eng->total_balls * 13 + 42);

    for (int i = 0; i < count; i++) {
        seed = seed * 1103515245 + 12345;
        int target = (int)((seed >> 16) % CK_NUM_OPS);

        CK_DreamBall ball = ck_dream_fire(eng, origin, target, 10);
        if (ball.coherence > best.coherence) {
            best = ball;
        }
    }

    return best;
}


/* ═══════════════════════════════════════════════════════════════
 * §6  EXPERIENCE LAYERS (Stack/Peel)
 * ═══════════════════════════════════════════════════════════════ */

CK_EXPORT int ck_layer_push(CK_Organism* org, const char* name, int priority) {
    CK_ExperienceStack* stack = &org->experience;
    if (stack->layer_count >= CK_MAX_LAYERS) return 0;

    CK_ExperienceLayer* layer = &stack->layers[stack->layer_count];
    memset(layer, 0, sizeof(CK_ExperienceLayer));
    strncpy(layer->name, name, CK_LAYER_NAME_LEN - 1);
    layer->priority = priority;
    layer->immutable = (priority <= 1);  /* core layers immutable */

    /* Copy current TL into layer */
    memcpy(&layer->tl, &org->tl, sizeof(CK_TransitionLattice));

    stack->layer_count++;

    /* Add layer's TL to organism TL element-wise */
    for (int i = 0; i < CK_NUM_OPS; i++) {
        for (int j = 0; j < CK_NUM_OPS; j++) {
            org->tl.TL[i][j] += layer->tl.TL[i][j];
            org->tl.total_transitions += layer->tl.TL[i][j];
        }
    }

    return 1;
}

CK_EXPORT int ck_layer_peel(CK_Organism* org, const char* name) {
    CK_ExperienceStack* stack = &org->experience;

    for (int idx = 0; idx < stack->layer_count; idx++) {
        if (strcmp(stack->layers[idx].name, name) == 0) {
            CK_ExperienceLayer* layer = &stack->layers[idx];

            /* Can't peel immutable layers */
            if (layer->immutable) return 0;

            /* Subtract layer's TL from organism TL */
            for (int i = 0; i < CK_NUM_OPS; i++) {
                for (int j = 0; j < CK_NUM_OPS; j++) {
                    org->tl.TL[i][j] -= layer->tl.TL[i][j];
                    if (org->tl.TL[i][j] < 0) org->tl.TL[i][j] = 0;
                    org->tl.total_transitions -= layer->tl.TL[i][j];
                }
            }
            if (org->tl.total_transitions < 0) org->tl.total_transitions = 0;

            /* Shift remaining layers down */
            for (int i = idx; i < stack->layer_count - 1; i++) {
                stack->layers[i] = stack->layers[i + 1];
            }
            stack->layer_count--;

            return 1;
        }
    }

    return 0;  /* not found */
}

CK_EXPORT int ck_layer_save(const CK_Organism* org, const char* name, const char* path) {
    const CK_ExperienceStack* stack = &org->experience;

    for (int idx = 0; idx < stack->layer_count; idx++) {
        if (strcmp(stack->layers[idx].name, name) == 0) {
            ck_tl_save(&stack->layers[idx].tl, path);
            return 1;
        }
    }

    /* If name not found, save current TL as a new layer snapshot */
    ck_tl_save(&org->tl, path);
    return 1;
}
