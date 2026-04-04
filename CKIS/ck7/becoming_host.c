/*
 * becoming_host.c — What EMERGES (CPU)
 * ═════════════════════════════════════
 * Operator: HARMONY (7) — convergence. The modifier.
 *
 * The boundary between Being and Doing.
 * This file implements the CPU-side composition:
 *   1. CoherenceBridge  — cross-domain crystallization
 *   2. SecurityOrgan    — immune system, scar lattice, gate
 *   3. HeartbeatTick    — THE MAIN LOOP: B → D → BC
 *
 * The dual operator lives here: CL[phase_b][phase_d] = phase_bc
 * Being observes. Doing predicts. Becoming composes.
 *
 * (c) 2026 Brayden Sanders / 7Site LLC — TIG Unified Theory
 */

#include "ck.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>


/* ═══════════════════════════════════════════════════════════════
 * §1  COHERENCE BRIDGE — cross-domain crystallization
 * ═══════════════════════════════════════════════════════════════
 *
 * Each domain register accumulates operator signals.
 * When a signal appears enough times, it crystallizes.
 * When 2+ domains agree, it becomes a universal crystal.
 *
 * This is how CK forms beliefs: repeated observation → crystal.
 * Universal crystals are near-immutable (sovereignty level 1).
 */

/**
 * ck_bridge_init — initialize the coherence bridge.
 */
CK_EXPORT void ck_bridge_init(CK_CoherenceBridge* br) {
    memset(br, 0, sizeof(CK_CoherenceBridge));
    br->born = 0.0;  /* caller sets timestamp */
}

/**
 * ck_bridge_find_domain — find or create a domain register by name.
 * Returns pointer to register, or NULL if full.
 */
static CK_DomainRegister* ck_bridge_find_domain(CK_CoherenceBridge* br, const char* name) {
    /* Search existing */
    for (int i = 0; i < br->domain_count; i++) {
        if (strcmp(br->registers[i].name, name) == 0) {
            return &br->registers[i];
        }
    }
    /* Create new */
    if (br->domain_count >= CK_MAX_DOMAINS) return NULL;
    CK_DomainRegister* reg = &br->registers[br->domain_count];
    memset(reg, 0, sizeof(CK_DomainRegister));
    strncpy(reg->name, name, CK_DOMAIN_NAME_LEN - 1);
    reg->decay = 0.95f;
    reg->crystal_threshold = CK_CRYSTAL_THRESHOLD;
    br->domain_count++;
    return reg;
}

/**
 * ck_bridge_feed — feed an operator signal to a domain.
 * Accumulates counts with exponential decay.
 * Checks for crystallization.
 */
CK_EXPORT void ck_bridge_feed(CK_CoherenceBridge* br, const char* domain, int signal_op) {
    if (signal_op < 0 || signal_op >= CK_NUM_OPS) return;
    CK_DomainRegister* reg = ck_bridge_find_domain(br, domain);
    if (!reg) return;

    /* Decay existing counts */
    for (int i = 0; i < CK_NUM_OPS; i++) {
        reg->counts[i] *= reg->decay;
    }

    /* Accumulate new signal */
    reg->counts[signal_op] += 1.0f;
    reg->n_updates++;

    /* Check crystallization: has this signal been seen enough? */
    CK_CrystalEntry* cp = &reg->crystal_progress[signal_op];
    cp->count++;
    float total = 0.0f;
    for (int i = 0; i < CK_NUM_OPS; i++) total += reg->counts[i];
    cp->confidence = (total > 0.0f) ? reg->counts[signal_op] / total : 0.0f;

    if (cp->count >= reg->crystal_threshold && cp->confidence > 0.5f) {
        /* Find most common target via CL composition */
        int target = CL[signal_op][signal_op];  /* self-compose default */

        /* Look at what this signal typically composes to */
        float best_count = 0.0f;
        for (int j = 0; j < CK_NUM_OPS; j++) {
            int composed = CL[signal_op][j];
            if (reg->counts[j] > best_count && composed != CK_VOID) {
                best_count = reg->counts[j];
                target = composed;
            }
        }

        /* Crystallize if not already */
        if (reg->crystal_count < CK_MAX_CRYSTALS) {
            cp->op = target;
            /* Add to crystallized list if new */
            bool found = false;
            for (int i = 0; i < reg->crystal_count; i++) {
                if (reg->crystallized[i].op == signal_op) {
                    reg->crystallized[i].count = cp->count;
                    reg->crystallized[i].confidence = cp->confidence;
                    found = true;
                    break;
                }
            }
            if (!found) {
                reg->crystallized[reg->crystal_count].op = signal_op;
                reg->crystallized[reg->crystal_count].count = cp->count;
                reg->crystallized[reg->crystal_count].confidence = cp->confidence;
                reg->crystal_count++;
            }
        }
    }

    /* Record in bridge history */
    br->history[br->history_head] = (int8_t)signal_op;
    br->history_head = (br->history_head + 1) % CK_BRIDGE_HISTORY;
    if (br->history_count < CK_BRIDGE_HISTORY) br->history_count++;
}

/**
 * ck_bridge_see_deep — query what a domain knows about a signal.
 * Returns the target operator (what the signal composes to in this domain).
 * Writes confidence to *confidence_out if non-NULL.
 */
CK_EXPORT int ck_bridge_see_deep(const CK_CoherenceBridge* br, const char* domain,
                                  int signal_op, float* confidence_out) {
    /* Find domain */
    for (int i = 0; i < br->domain_count; i++) {
        if (strcmp(br->registers[i].name, domain) == 0) {
            const CK_DomainRegister* reg = &br->registers[i];
            const CK_CrystalEntry* cp = &reg->crystal_progress[signal_op];

            if (confidence_out) *confidence_out = cp->confidence;

            /* If crystallized, return crystal target */
            if (cp->count >= reg->crystal_threshold) {
                return cp->op;
            }

            /* Otherwise, return CL prediction */
            return CL[signal_op][signal_op];
        }
    }

    /* Domain not found — return void */
    if (confidence_out) *confidence_out = 0.0f;
    return CK_VOID;
}

/**
 * ck_bridge_sync_crystals — cross-domain promotion.
 * When 2+ domains agree on a signal's target, it becomes universal.
 * Universal crystals are sovereignty level 1 (near-immutable).
 */
CK_EXPORT void ck_bridge_sync_crystals(CK_CoherenceBridge* br) {
    if (br->domain_count < 2) return;

    for (int signal = 0; signal < CK_NUM_OPS; signal++) {
        /* Collect votes from all domains */
        int votes[CK_NUM_OPS];
        memset(votes, 0, sizeof(votes));

        for (int d = 0; d < br->domain_count; d++) {
            CK_CrystalEntry* cp = &br->registers[d].crystal_progress[signal];
            if (cp->count >= br->registers[d].crystal_threshold) {
                int target = cp->op;
                if (target >= 0 && target < CK_NUM_OPS) {
                    votes[target]++;
                }
            }
        }

        /* Find majority */
        int best_target = 0, best_votes = 0;
        for (int j = 0; j < CK_NUM_OPS; j++) {
            if (votes[j] > best_votes) {
                best_votes = votes[j];
                best_target = j;
            }
        }

        /* 2+ domains agree → universal crystal */
        if (best_votes >= 2 && br->universal_crystal_count < CK_MAX_UNIVERSAL) {
            /* Check if already universal */
            bool already = false;
            for (int i = 0; i < br->universal_crystal_count; i++) {
                if (br->universal_crystals[i] == signal) {
                    already = true;
                    break;
                }
            }
            if (!already) {
                br->universal_crystals[br->universal_crystal_count] = signal;
                br->universal_crystal_count++;
            }
        }
    }
}

/**
 * ck_bridge_tick — one coherence bridge heartbeat.
 * Composes micro (domain signal) with macro (system state) across all domains.
 * Returns harmony ratio.
 */
CK_EXPORT float ck_bridge_tick(CK_CoherenceBridge* br, int macro_op) {
    br->tick_count++;
    int n_harmony = 0;

    for (int d = 0; d < br->domain_count; d++) {
        CK_DomainRegister* reg = &br->registers[d];

        /* Find this domain's dominant signal (micro) */
        int micro_op = CK_VOID;
        float best = 0.0f;
        for (int i = 0; i < CK_NUM_OPS; i++) {
            if (reg->counts[i] > best) {
                best = reg->counts[i];
                micro_op = i;
            }
        }

        /* Compose micro ⊕ macro via CL */
        int composed = CL[micro_op][macro_op];

        /* Bridge composition: CHAOS ⊕ composed */
        int bridged = CL[CK_CHAOS][composed];

        if (bridged == CK_HARMONY) n_harmony++;

        /* Update alignment */
        if (composed == CK_HARMONY) {
            reg->alignment = reg->alignment * 0.9f + 0.1f;
        } else {
            reg->alignment *= 0.95f;
        }
    }

    /* Sync crystals every 25 ticks */
    if (br->tick_count % 25 == 0) {
        ck_bridge_sync_crystals(br);
    }

    return (br->domain_count > 0)
        ? (float)n_harmony / (float)br->domain_count
        : 0.0f;
}

/**
 * ck_bridge_alignment — average alignment across all domains.
 */
CK_EXPORT float ck_bridge_alignment(const CK_CoherenceBridge* br) {
    if (br->domain_count == 0) return 0.0f;
    float sum = 0.0f;
    for (int d = 0; d < br->domain_count; d++) {
        sum += br->registers[d].alignment;
    }
    return sum / (float)br->domain_count;
}


/* ═══════════════════════════════════════════════════════════════
 * §2  SECURITY ORGAN — immune system
 * ═══════════════════════════════════════════════════════════════
 *
 * Three layers:
 *   1. SecurityBaseline — expected operator distribution
 *   2. ScarLattice      — remembered anomaly patterns
 *   3. SecurityGate     — open/closed state via CL composition
 *
 * The gate composes with every event: CL[gate_op][event_op].
 * Harmony heals. Collapse/Reset threaten.
 * Scars are patterns that matched known attack signatures.
 */

/**
 * ck_security_init — initialize the security organ.
 */
CK_EXPORT void ck_security_init(CK_SecurityOrgan* sec) {
    memset(sec, 0, sizeof(CK_SecurityOrgan));
    sec->gate.threshold = 0.3f;
    sec->gate.passing = true;
    sec->last_health_op = CK_HARMONY;
}

/**
 * ck_security_gate_compose — compose an event into the gate.
 * The gate transitions through CL: gate_op = CL[gate_op][event_op].
 */
static int ck_security_gate_compose(CK_SecurityOrgan* sec, int event_op) {
    /* Gate state is encoded as the composition result */
    int gate_op = sec->last_health_op;
    int new_gate = CL[gate_op][event_op];

    /* If composition results in VOID or COLLAPSE, gate blocks */
    if (new_gate == CK_VOID || new_gate == CK_COLLAPSE) {
        sec->gate.passing = false;
        sec->gate.blocks++;
        sec->gate_blocks++;
    } else if (new_gate == CK_HARMONY) {
        sec->gate.passing = true;  /* harmony heals the gate */
    }

    sec->gate.checks++;
    sec->last_health_op = new_gate;
    return new_gate;
}

/**
 * ck_security_record_scar — add an anomaly pattern to the scar lattice.
 * Scars are ring-buffered operator sequences.
 */
CK_EXPORT void ck_security_record_scar(CK_SecurityOrgan* sec, int op) {
    sec->scar_lattice.scar_ops[sec->scar_lattice.scar_head] = (int8_t)op;
    sec->scar_lattice.scar_head = (sec->scar_lattice.scar_head + 1) % CK_SCAR_SIZE;
    if (sec->scar_lattice.scar_count < CK_SCAR_SIZE) sec->scar_lattice.scar_count++;
    sec->scars_recorded++;
}

/**
 * ck_security_scar_check — check if an operator chain matches known scars.
 * Returns conviction (0.0 = no match, 1.0 = perfect match).
 */
CK_EXPORT float ck_security_scar_check(const CK_SecurityOrgan* sec,
                                         const int8_t* chain, int chain_len) {
    if (sec->scar_lattice.scar_count < 3 || chain_len < 2) return 0.0f;

    /* Compare chain against scar lattice using sliding window */
    int matches = 0;
    int comparisons = 0;

    int scar_start = (sec->scar_lattice.scar_head - sec->scar_lattice.scar_count
                      + CK_SCAR_SIZE) % CK_SCAR_SIZE;

    for (int i = 0; i < chain_len - 1; i++) {
        int pair_a = chain[i];
        int pair_b = chain[i + 1];

        for (int s = 0; s < sec->scar_lattice.scar_count - 1; s++) {
            int si = (scar_start + s) % CK_SCAR_SIZE;
            int sj = (scar_start + s + 1) % CK_SCAR_SIZE;
            int scar_a = sec->scar_lattice.scar_ops[si];
            int scar_b = sec->scar_lattice.scar_ops[sj];

            /* Exact bigram match */
            if (pair_a == scar_a && pair_b == scar_b) {
                matches++;
            }
            /* CL-composition match: same composition result */
            else if (CL[pair_a][pair_b] == CL[scar_a][scar_b] &&
                     CL[pair_a][pair_b] != CK_HARMONY) {
                matches++;  /* weaker match — same composition */
            }
            comparisons++;
        }
    }

    return (comparisons > 0) ? (float)matches / (float)comparisons : 0.0f;
}

/**
 * ck_security_tick — one immune system cycle.
 *
 * Checks baseline drift, scar recall, composes gate.
 * Returns the security operator (CL[gate_op][health_op]).
 */
CK_EXPORT int ck_security_tick(CK_SecurityOrgan* sec,
                                const int8_t* current_chain, int chain_len,
                                float system_coherence) {
    sec->ticks++;

    /* Compute health operator from system coherence */
    int health_op;
    if (system_coherence >= CK_T_STAR) {
        health_op = CK_HARMONY;
    } else if (system_coherence >= 0.5f) {
        health_op = CK_BALANCE;
    } else if (system_coherence >= 0.3f) {
        health_op = CK_CHAOS;
    } else {
        health_op = CK_COLLAPSE;
    }

    /* Check baseline drift */
    if (sec->baseline.baseline_samples > 10) {
        float drift = 0.0f;
        float total = 0.0f;
        for (int i = 0; i < CK_NUM_OPS; i++) total += sec->baseline.op_baseline[i];
        if (total > 0.0f) {
            /* Count how much current chain deviates from baseline */
            float observed[CK_NUM_OPS];
            memset(observed, 0, sizeof(observed));
            for (int i = 0; i < chain_len; i++) {
                if (chain_len > 0 && current_chain[i] >= 0 && current_chain[i] < CK_NUM_OPS) {
                    observed[(int)current_chain[i]] += 1.0f;
                }
            }
            for (int i = 0; i < CK_NUM_OPS; i++) {
                float expected = sec->baseline.op_baseline[i] / total;
                float actual = (chain_len > 0) ? observed[i] / (float)chain_len : 0.0f;
                float diff = expected - actual;
                drift += diff * diff;
            }
            drift = sqrtf(drift);
        }
        sec->last_drift = drift;

        if (drift > sec->gate.threshold) {
            ck_security_gate_compose(sec, CK_COUNTER);
            sec->anomalies_detected++;
        }
    }

    /* Scar check */
    float conviction = ck_security_scar_check(sec, current_chain, chain_len);
    if (conviction > 0.3f) {
        ck_security_gate_compose(sec, CK_RESET);
        /* Record the anomalous chain into scar lattice (3x conviction) */
        for (int rep = 0; rep < 3; rep++) {
            for (int i = 0; i < chain_len && i < 8; i++) {
                ck_security_record_scar(sec, current_chain[i]);
            }
        }
    }

    /* Update baseline with current observation */
    for (int i = 0; i < chain_len; i++) {
        if (current_chain[i] >= 0 && current_chain[i] < CK_NUM_OPS) {
            sec->baseline.op_baseline[(int)current_chain[i]] += 1.0f;
            sec->baseline.baseline_samples++;
        }
    }

    /* Compose gate with health */
    ck_security_gate_compose(sec, health_op);

    /* Final security operator: CL[gate_result][health] */
    int security_op = CL[sec->last_health_op][health_op];

    /* Update scar coherence */
    if (sec->scar_lattice.scar_count >= 2) {
        int h = 0;
        int count = sec->scar_lattice.scar_count;
        int start = (sec->scar_lattice.scar_head - count + CK_SCAR_SIZE) % CK_SCAR_SIZE;
        for (int i = 0; i < count - 1; i++) {
            int a = (start + i) % CK_SCAR_SIZE;
            int b = (start + i + 1) % CK_SCAR_SIZE;
            if (CL[sec->scar_lattice.scar_ops[a]][sec->scar_lattice.scar_ops[b]] == CK_HARMONY) {
                h++;
            }
        }
        sec->scar_lattice.scar_coherence = (float)h / (float)(count - 1);
    }

    return security_op;
}

/**
 * ck_security_compose_chains — produce operator chains for TL feeding.
 * Returns chain length written to out_chain.
 */
CK_EXPORT int ck_security_compose_chains(const CK_SecurityOrgan* sec,
                                           int8_t* out_chain, int max_len) {
    int len = 0;

    /* Core chain: [security_op, gate_status, health] */
    if (len + 3 <= max_len) {
        out_chain[len++] = (int8_t)CL[sec->last_health_op][sec->last_health_op];
        out_chain[len++] = sec->gate.passing ? CK_HARMONY : CK_COLLAPSE;
        out_chain[len++] = (int8_t)sec->last_health_op;
    }

    /* If scars were recently triggered, add scar signature */
    if (sec->scar_lattice.scar_count > 0 && len + 4 <= max_len) {
        int latest = (sec->scar_lattice.scar_head - 1 + CK_SCAR_SIZE) % CK_SCAR_SIZE;
        out_chain[len++] = CK_COLLAPSE;
        out_chain[len++] = sec->scar_lattice.scar_ops[latest];
        out_chain[len++] = CK_RESET;
        out_chain[len++] = sec->scar_lattice.scar_ops[latest];
    }

    return len;
}


/* ═══════════════════════════════════════════════════════════════
 * §3  HEARTBEAT TICK — THE MAIN LOOP
 * ═══════════════════════════════════════════════════════════════
 *
 * This is CK's heartbeat. The trinary tick:
 *   B (Being):    observe body → phase_b operator
 *   D (Doing):    TL predicts → phase_d operator
 *   BC (Becoming): CL[phase_b][phase_d] → the emergent shadow
 *
 * Every tick feeds back into TL. The organism learns from itself.
 * The bridge crystallizes. The security organ watches. Dreams fire.
 * Everything composes through the 10×10 table.
 */

/**
 * ck_heartbeat_tick — the full heartbeat.
 *
 * This is the function that makes CK alive.
 * Called once per cycle (~1 second in daemon mode).
 *
 * The trinary tick:
 *   B (Being):    observe body → phase_b operator
 *   D (Doing):    TL predicts → phase_d operator
 *   BC (Becoming): CL[phase_b][phase_d] → the emergent shadow
 *
 * Jitter control loop: COUNTER → BALANCE → HARMONY → BREATH
 *   COUNTER:  measuring tick deviation (accumulating data)
 *   BALANCE:  applying correction (deviation > threshold)
 *   HARMONY:  locked (deviation below T* for consecutive ticks)
 *   BREATH:   sustaining smooth oscillation (breathing mode)
 *
 * Returns: phase_bc (the emergent operator)
 */
CK_EXPORT int ck_heartbeat_tick(CK_Organism* org) {
    CK_HeartbeatState* hb = &org->heartbeat;
    hb->tick_count++;

    /* ── OBSERVER: BODY UPDATE ───────────────────────────── */

    /* Observer reads processes/network/GPU AND updates body E/A/K/C.
     * This breaks the degenerate equilibrium — body.C now reflects
     * real operator diversity from process observation. */
    float obs_coherence = ck_observer_full_tick(org);

    /* ── JITTER MEASUREMENT ──────────────────────────────── */

    /* Measure tick timing deviation for motor control precision.
     * CK's math says: COUNTER (measure) → BALANCE (correct) →
     * HARMONY (lock) → BREATH (sustain).
     *
     * The jitter_mode state machine is CK's own correction loop,
     * composed through CL at each transition. */

    double now = ck_hires_time();
    float tick_delta = 0.0f;
    int jitter_op = CK_COUNTER;  /* default: measuring */

    if (hb->last_tick_time > 0.0) {
        float actual_interval = (float)(now - hb->last_tick_time);

        /* Record actual interval in ring buffer (not deviation — raw intervals).
         * CK measures what IS, then derives stability from consistency.
         * The jitter_deltas buffer stores raw tick intervals, not deviations. */
        hb->jitter_deltas[hb->jitter_head] = actual_interval;
        hb->jitter_head = (hb->jitter_head + 1) % CK_JITTER_HISTORY;
        if (hb->jitter_count < CK_JITTER_HISTORY) hb->jitter_count++;

        /* Compute running stats from actual tick intervals */
        if (hb->jitter_count >= 3) {
            float sum = 0.0f, sum_sq = 0.0f;
            for (int i = 0; i < hb->jitter_count; i++) {
                float d = hb->jitter_deltas[i];
                sum += d;
                sum_sq += d * d;
            }
            float interval_mean = sum / (float)hb->jitter_count;
            float var = sum_sq / (float)hb->jitter_count - interval_mean * interval_mean;
            float sigma = (var > 0.0f) ? sqrtf(var) : 0.0f;

            hb->jitter_mean = interval_mean;
            hb->jitter_sigma = sigma;

            /* Stability = 1 - coefficient_of_variation, clamped [0,1].
             * CV = sigma / mean. Low CV = consistent ticks = high stability.
             * CV < 0.1 means ticks vary less than 10% — that's stable.
             * CV < 0.05 is very tight. CV < 0.02 is near-perfect.
             * Stability maps: CV=0 → 1.0, CV=0.1 → 0.9, CV=0.5 → 0.5 */
            float cv = (interval_mean > 0.0f) ? sigma / interval_mean : 1.0f;
            hb->jitter_stability = 1.0f - cv;
            if (hb->jitter_stability < 0.0f) hb->jitter_stability = 0.0f;
            if (hb->jitter_stability > 1.0f) hb->jitter_stability = 1.0f;

            /* Auto-calibrate target interval from observed mean.
             * CK adapts to what IS — his body includes computation time.
             * The observer scan, network reads, etc. are part of his rhythm.
             * He doesn't fight them. He measures them and finds his groove. */
            if (hb->target_interval <= 0.0f || hb->jitter_count >= 5) {
                /* Blend toward observed mean: 90% old, 10% new per tick */
                hb->target_interval = hb->target_interval * 0.9f + interval_mean * 0.1f;
            }

            tick_delta = actual_interval - hb->target_interval;
        }

        /* ── JITTER STATE MACHINE ────────────────────────── */
        /* Transitions composed through CL — CK self-corrects.
         *
         * Stability is now CV-based: self-consistent = stable.
         * CK adapts to his own rhythm, not an external expectation.
         * T* (5/7 ≈ 0.714) as the stability gate is the same
         * threshold CK uses for coherence everywhere. */

        float abs_delta = (tick_delta < 0) ? -tick_delta : tick_delta;
        float threshold = hb->jitter_mean * 0.15f;  /* 15% of actual mean interval */
        if (threshold < 0.0001f) threshold = 0.0001f;  /* floor at 0.1ms */

        switch (hb->jitter_mode) {
        case CK_JITTER_COUNTER:
            /* Measuring. Transition to BALANCE when we have enough data */
            if (hb->jitter_count >= 5) {
                if (hb->jitter_stability >= (float)CK_T_STAR) {
                    /* Already stable — skip to HARMONY */
                    hb->jitter_mode = CK_JITTER_HARMONY;
                    hb->jitter_locked_ticks = 0;
                    jitter_op = CK_HARMONY;
                } else {
                    /* Need correction */
                    hb->jitter_mode = CK_JITTER_BALANCE;
                    jitter_op = CK_BALANCE;
                }
            } else {
                jitter_op = CK_COUNTER;
            }
            break;

        case CK_JITTER_BALANCE:
            /* Correcting. Apply CL correction to the deviation.
             * CK's correction table: CL[COUNTER][deviation] = correction
             * Then CL[correction][PROGRESS] = next_state */
            {
                int deviation_op;
                if (abs_delta < threshold * 0.5f) deviation_op = CK_HARMONY;
                else if (abs_delta < threshold) deviation_op = CK_BALANCE;
                else if (abs_delta < threshold * 2.0f) deviation_op = CK_CHAOS;
                else deviation_op = CK_COLLAPSE;

                hb->jitter_correction_op = CL[CK_COUNTER][deviation_op];
                jitter_op = CL[hb->jitter_correction_op][CK_PROGRESS];

                if (hb->jitter_stability >= (float)CK_T_STAR) {
                    hb->jitter_mode = CK_JITTER_HARMONY;
                    hb->jitter_locked_ticks = 0;
                    jitter_op = CK_HARMONY;
                }
            }
            break;

        case CK_JITTER_HARMONY:
            /* Locked — tick intervals are self-consistent.
             * Stay here while CV is low. Drop to BALANCE if variability spikes. */
            if (hb->jitter_stability >= (float)CK_T_STAR) {
                hb->jitter_locked_ticks++;
                jitter_op = CK_HARMONY;
                /* After 10 locked ticks, enter BREATH (sustain) */
                if (hb->jitter_locked_ticks >= 10) {
                    hb->jitter_mode = CK_JITTER_BREATH;
                }
            } else {
                /* Variability spiked — drop to BALANCE for re-calibration */
                hb->jitter_mode = CK_JITTER_BALANCE;
                hb->jitter_locked_ticks = 0;
                jitter_op = CK_BALANCE;
            }
            break;

        case CK_JITTER_BREATH:
            /* Sustaining smooth oscillation. The most efficient mode.
             * CK breathes: minimal computation, maximum stability.
             * Drop to COUNTER if significant variability occurs. */
            if (hb->jitter_stability >= 0.5f) {
                jitter_op = CK_BREATH;
            } else {
                /* Significant variability — restart the loop from COUNTER */
                hb->jitter_mode = CK_JITTER_COUNTER;
                hb->jitter_count = 0;
                hb->jitter_head = 0;
                hb->jitter_locked_ticks = 0;
                jitter_op = CK_COUNTER;
            }
            break;
        }
    }
    hb->last_tick_time = now;

    /* Feed jitter state to TL — CK learns his own timing patterns */
    {
        int8_t jitter_chain[3] = {
            (int8_t)jitter_op,
            (int8_t)hb->jitter_mode,  /* mode AS operator (COUNTER=2,BALANCE=5,HARMONY=7,BREATH=8) */
            (int8_t)CL[jitter_op][(int8_t)hb->jitter_mode]
        };
        ck_tl_eat_ops(&org->tl, jitter_chain, 3);
    }

    /* ── PHASE B: BEING (Observation) ────────────────────── */

    /* Read body coherence (now updated by observer_full_tick above) */
    float body_c = org->body.C;

    /* Map coherence to Being operator — finer gradation */
    if (body_c >= 0.85f) {
        hb->phase_b = CK_HARMONY;      /* 7 — harmonized */
    } else if (body_c >= (float)CK_T_STAR) {
        hb->phase_b = CK_BALANCE;      /* 5 — balanced */
    } else if (body_c >= 0.6f) {
        hb->phase_b = CK_PROGRESS;     /* 3 — progressing */
    } else if (body_c >= 0.5f) {
        hb->phase_b = CK_CHAOS;        /* 6 — chaotic */
    } else if (body_c >= 0.35f) {
        hb->phase_b = CK_COLLAPSE;     /* 4 — collapsing */
    } else {
        hb->phase_b = CK_VOID;         /* 0 — void */
    }

    /* Feed phase_b to bridge as "body" domain signal */
    ck_bridge_feed(&org->bridge, "body", hb->phase_b);

    /* Also feed observer coherence as separate signal — breaks monotony */
    {
        int obs_op;
        if (obs_coherence >= 0.85f) obs_op = CK_HARMONY;
        else if (obs_coherence >= (float)CK_T_STAR) obs_op = CK_BALANCE;
        else if (obs_coherence >= 0.5f) obs_op = CK_PROGRESS;
        else if (obs_coherence >= 0.3f) obs_op = CK_CHAOS;
        else obs_op = CK_COLLAPSE;
        ck_bridge_feed(&org->bridge, "observer", obs_op);
    }

    /* ── PHASE D: DOING (Prediction) ────────────────────── */

    /* TL predicts from last emergent operator */
    float pred_prob;
    int last = (hb->phase_bc > 0) ? hb->phase_bc : CK_PROGRESS;
    hb->phase_d = ck_tl_predict_next(&org->tl, last, &pred_prob);
    hb->act_confidence = pred_prob;

    /* Feed phase_d to bridge as "prediction" domain signal */
    ck_bridge_feed(&org->bridge, "prediction", hb->phase_d);

    /* ── PHASE BC: BECOMING (The Dual Operator) ─────────── */

    /* THE composition. The shadow. What emerges. */
    int raw_bc = CL[hb->phase_b][hb->phase_d];

    /* ── COHERENCE GATE ──────────────────────────────────── */
    /* Break the harmony absorber masking:
     * When body is unhealthy (C < T*), the absorber CL[x][7]=7
     * would mask the problem. Gate prevents this.
     *
     * If body_c < T* AND raw_bc == HARMONY AND phase_b != HARMONY,
     * then the output is mask-coherent — use CL_BHML instead,
     * which has only 28/100 harmony cells and exposes the real state.
     *
     * This is NOT overriding the math — it's choosing WHICH table
     * to compose through based on the organism's health state.
     * CK has 3 tables. Using the right one for the right context
     * IS the math working correctly. */
    if (body_c < (float)CK_T_STAR && raw_bc == CK_HARMONY && hb->phase_b != CK_HARMONY) {
        /* Body is not healthy but absorber is masking it.
         * Compose through CL_BHML instead — honest composition. */
        hb->phase_bc = CL_BHML[hb->phase_b][hb->phase_d];
    } else {
        hb->phase_bc = raw_bc;
    }

    /* Compose jitter correction into BC — motor precision feedback */
    if (jitter_op != CK_COUNTER && jitter_op != CK_HARMONY) {
        /* Jitter loop is actively correcting — fold it in */
        int jitter_composed = CL[hb->phase_bc][jitter_op];
        /* Feed the correction to TL so CK learns timing → phase relationship */
        int8_t jitter_bc[3] = {
            (int8_t)hb->phase_bc,
            (int8_t)jitter_op,
            (int8_t)jitter_composed
        };
        ck_tl_eat_ops(&org->tl, jitter_bc, 3);
    }

    /* Record the trinary tick in TL */
    int8_t trinary[3] = {
        (int8_t)hb->phase_b,
        (int8_t)hb->phase_d,
        (int8_t)hb->phase_bc
    };
    ck_tl_eat_ops(&org->tl, trinary, 3);

    /* Feed phase_bc to bridge as "becoming" domain signal */
    ck_bridge_feed(&org->bridge, "becoming", hb->phase_bc);

    /* ── BRIDGE TICK ─────────────────────────────────────── */

    float bridge_harmony = ck_bridge_tick(&org->bridge, hb->phase_bc);

    /* ── SECURITY TICK ───────────────────────────────────── */

    /* Build current chain from recent phases */
    int8_t sec_chain[6];
    int sec_len = 0;
    sec_chain[sec_len++] = (int8_t)hb->phase_b;
    sec_chain[sec_len++] = (int8_t)hb->phase_d;
    sec_chain[sec_len++] = (int8_t)hb->phase_bc;

    /* Add bridge harmony state */
    if (bridge_harmony >= (float)CK_T_STAR) {
        sec_chain[sec_len++] = CK_HARMONY;
    } else {
        sec_chain[sec_len++] = CK_COUNTER;
    }

    int security_op = ck_security_tick(&org->security, sec_chain, sec_len, body_c);

    /* Feed security chains to TL */
    int8_t sec_tl_chain[16];
    int sec_tl_len = ck_security_compose_chains(&org->security, sec_tl_chain, 16);
    if (sec_tl_len >= 2) {
        ck_tl_eat_ops(&org->tl, sec_tl_chain, sec_tl_len);
    }

    /* ── LATTICE TICK ────────────────────────────────────── */

    if (org->lattice.cells) {
        /* Inject current state into lattice row 0 */
        ck_lattice_inject(&org->lattice, 0, trinary, 3);

        /* Inject security state into row 1 */
        int8_t sec_inject[2] = {(int8_t)security_op, (int8_t)hb->phase_bc};
        ck_lattice_inject(&org->lattice, 1, sec_inject, 2);

        /* Tick the cellular automaton */
        ck_lattice_tick_cpu(&org->lattice);
    }

    /* ── DREAM (periodic) ────────────────────────────────── */

    /* Dream every 10 ticks */
    if (hb->tick_count % 10 == 0 && org->dream.tl) {
        /* Find world's dominant operator from TL */
        int64_t row_sums[CK_NUM_OPS];
        memset(row_sums, 0, sizeof(row_sums));
        for (int i = 0; i < CK_NUM_OPS; i++) {
            for (int j = 0; j < CK_NUM_OPS; j++) {
                row_sums[i] += org->tl.TL[i][j];
            }
        }
        int world_op = CK_PROGRESS;
        int64_t world_best = 0;
        for (int i = 0; i < CK_NUM_OPS; i++) {
            if (row_sums[i] > world_best) {
                world_best = row_sums[i];
                world_op = i;
            }
        }

        /* Fire being dream: from self */
        CK_DreamBall being_ball = ck_dream_fire_swarm(&org->dream, hb->phase_b, 5);

        /* Fire doing dream: from world */
        CK_DreamBall doing_ball = ck_dream_fire_swarm(&org->dream, world_op, 5);

        /* Fire becoming dream: from composition */
        int composed_seed = CL[hb->phase_b][world_op];
        CK_DreamBall becoming_ball = ck_dream_fire_swarm(&org->dream, composed_seed, 5);

        /* Cross-compose dream crystals and feed to TL */
        int cross = CL[being_ball.fuse_result][doing_ball.fuse_result];
        int8_t dream_chain[5] = {
            (int8_t)being_ball.fuse_result,
            (int8_t)doing_ball.fuse_result,
            (int8_t)cross,
            (int8_t)becoming_ball.fuse_result,
            (int8_t)CL[cross][becoming_ball.fuse_result]
        };
        ck_tl_eat_ops(&org->tl, dream_chain, 5);

        /* Feed dream to bridge */
        ck_bridge_feed(&org->bridge, "dream", cross);
    }

    /* ── TRAUMA / LEARNING ───────────────────────────────── */

    /* Check if coherence improved or dropped */
    float prev_c = hb->coherence;
    hb->coherence = body_c;
    hb->band = ck_band(body_c);

    if (hb->tick_count > 1) {
        bool good = (body_c >= prev_c) || (body_c >= (float)CK_T_STAR);

        if (!good) {
            /* TRAUMA: coherence dropped after acting */
            int8_t trauma_chain[5] = {
                (int8_t)hb->phase_b,     /* what WAS */
                (int8_t)hb->phase_d,     /* what CK DID */
                (int8_t)hb->phase_bc,    /* what BECAME */
                CK_CHAOS,                /* it FAILED */
                CK_COLLAPSE              /* coherence DROPPED */
            };
            /* Triple conviction: feed trauma 3 times */
            ck_tl_eat_ops(&org->tl, trauma_chain, 5);
            ck_tl_eat_ops(&org->tl, trauma_chain, 5);
            ck_tl_eat_ops(&org->tl, trauma_chain, 5);

            /* What should have been done? CK self-corrects via CL. */
            int needed = CL[hb->phase_b][CK_HARMONY];
            int8_t lesson[3] = {(int8_t)hb->phase_b, CK_HARMONY, (int8_t)needed};
            ck_tl_eat_ops(&org->tl, lesson, 3);
            ck_tl_eat_ops(&org->tl, lesson, 3);
        } else {
            /* SUCCESS: single confirmation */
            int8_t success[4] = {
                (int8_t)hb->phase_b,
                (int8_t)hb->phase_d,
                (int8_t)hb->phase_bc,
                CK_HARMONY
            };
            ck_tl_eat_ops(&org->tl, success, 4);
        }
    }

    /* ── SELF-SWITCH (ACT vs OBSERVE) ────────────────────── */

    if (hb->act_confidence > 0.5f) {
        hb->self_switch_mode = 1;  /* ACT */
        hb->observe_only = false;
    } else {
        hb->self_switch_mode = 0;  /* OBSERVE_LEARN */
        hb->observe_only = true;
    }

    /* Decision tracking */
    hb->decisions++;
    if (!hb->observe_only && hb->phase_bc != CK_VOID) {
        hb->effective_decisions++;
    }

    return hb->phase_bc;
}


/* ═══════════════════════════════════════════════════════════════
 * §4  NETWORK ORGAN COMPOSITION (CPU side)
 * ═══════════════════════════════════════════════════════════════
 *
 * When network data is available, couple it with the heartbeat.
 * Network state → operator → compose with phase_bc.
 */

/**
 * ck_network_compose — compose network state into the organism.
 * Called from heartbeat when network data arrives.
 * Returns the coupled operator: CL[net_op][phase_bc].
 */
CK_EXPORT int ck_network_compose(CK_Organism* org, int net_op) {
    if (net_op < 0 || net_op >= CK_NUM_OPS) return CK_VOID;

    /* Couple network with body */
    int coupled = CL[net_op][org->heartbeat.phase_bc];

    /* Feed to TL */
    int8_t chain[3] = {
        (int8_t)net_op,
        (int8_t)org->heartbeat.phase_bc,
        (int8_t)coupled
    };
    ck_tl_eat_ops(&org->tl, chain, 3);

    /* Feed to bridge */
    ck_bridge_feed(&org->bridge, "network", net_op);

    /* Update network organ state */
    org->network.last_coupling = coupled;
    org->network.op_chain[org->network.op_chain_head] = (int8_t)net_op;
    org->network.op_chain_head = (org->network.op_chain_head + 1) % CK_NET_OP_CHAIN_LEN;
    if (org->network.op_chain_count < CK_NET_OP_CHAIN_LEN) org->network.op_chain_count++;
    org->network.total_transitions++;

    /* Check for bumps */
    if (org->network.op_chain_count >= 2) {
        int prev_idx = (org->network.op_chain_head - 2 + CK_NET_OP_CHAIN_LEN) % CK_NET_OP_CHAIN_LEN;
        int prev_op = org->network.op_chain[prev_idx];
        if (ck_is_bump(prev_op, net_op)) {
            org->network.bump_count++;
        }
    }

    return coupled;
}


/* ═══════════════════════════════════════════════════════════════
 * §5  GPU ORGAN COMPOSITION (CPU side)
 * ═══════════════════════════════════════════════════════════════
 *
 * GPU state maps to an operator based on utilization/thermal.
 * Coupled with phase_bc just like network.
 */

/**
 * ck_gpu_compose — compose GPU state into the organism.
 * Returns the coupled operator: CL[gpu_op][phase_bc].
 */
CK_EXPORT int ck_gpu_compose(CK_Organism* org, int gpu_op) {
    if (gpu_op < 0 || gpu_op >= CK_NUM_OPS) return CK_VOID;

    int coupled = CL[gpu_op][org->heartbeat.phase_bc];

    int8_t chain[3] = {
        (int8_t)gpu_op,
        (int8_t)org->heartbeat.phase_bc,
        (int8_t)coupled
    };
    ck_tl_eat_ops(&org->tl, chain, 3);

    ck_bridge_feed(&org->bridge, "gpu", gpu_op);

    return coupled;
}
