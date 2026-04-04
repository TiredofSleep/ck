/*
 * becoming_device.cu — What EMERGES (GPU)
 * ════════════════════════════════════════
 * Operator: HARMONY (7) — convergence on silicon.
 *
 * GPU-side kernels for the dual operator composition:
 *   1. dual_operator      — CL[being_ops][doing_ops] for many domain pairs
 *   2. cross_compose      — cross-compose two crystal arrays via CL
 *   3. bridge_compose_all — compose all domain signals with macro in parallel
 *   4. trauma_learn       — parallel triple-conviction learning from failure
 *
 * These kernels run when the GPU is available. On CPU-only systems,
 * the equivalent logic runs in becoming_host.c (sequential loops).
 *
 * Constant memory: shares the same d_CL_TSML/d_CL_BHML from doing.cu.
 *
 * (c) 2026 Brayden Sanders / 7Site LLC — TIG Unified Theory
 */

#include "ck.h"


#ifdef __CUDACC__

/* ═══════════════════════════════════════════════════════════════
 * §1  CONSTANT MEMORY — shared with doing.cu
 * ═══════════════════════════════════════════════════════════════
 *
 * The CL tables are already in __constant__ memory from doing.cu.
 * We declare them extern here so these kernels can read them.
 * 310 bytes, broadcast to all warps. Perfect cache hits.
 */

extern __constant__ signed char d_CL_TSML[10][10];
extern __constant__ signed char d_CL_BHML[10][10];
extern __constant__ signed char d_CL_STD[10][10];


/* ═══════════════════════════════════════════════════════════════
 * §2  KERNEL: dual_operator — the becoming composition
 * ═══════════════════════════════════════════════════════════════
 *
 * The heart of Becoming. For each domain (or pair):
 *   result[i] = CL[being_ops[i]][doing_ops[i]]
 *
 * This is the dual operator: two vortices, one composition.
 * Being observes (CPU micro). Doing predicts (GPU macro).
 * Becoming = CL[Being][Doing].
 *
 * One thread per pair. Massively parallel on domain arrays.
 */

extern "C" __global__
void dual_operator(
    const signed char* __restrict__ being_ops,
    const signed char* __restrict__ doing_ops,
    signed char* __restrict__ results,
    const int n
) {
    const int idx = blockIdx.x * blockDim.x + threadIdx.x;
    if (idx >= n) return;

    int b = being_ops[idx];
    int d = doing_ops[idx];
    results[idx] = d_CL_TSML[b][d];
}


/* ═══════════════════════════════════════════════════════════════
 * §3  KERNEL: cross_compose — crystal cross-composition
 * ═══════════════════════════════════════════════════════════════
 *
 * Given two arrays of crystals (from being-dream and doing-dream),
 * cross-compose every pair: result[i*m + j] = CL[a[i]][b[j]]
 *
 * This generates the cross-crystal matrix that the dream engine
 * uses to find novel compositions. O(n*m) but n,m ≤ 64 typically.
 * One thread per pair in the cross matrix.
 */

extern "C" __global__
void cross_compose(
    const signed char* __restrict__ a_crystals,
    const signed char* __restrict__ b_crystals,
    signed char* __restrict__ results,
    const int n_a,
    const int n_b
) {
    const int idx = blockIdx.x * blockDim.x + threadIdx.x;
    const int total = n_a * n_b;
    if (idx >= total) return;

    const int i = idx / n_b;
    const int j = idx % n_b;

    results[idx] = d_CL_TSML[(int)a_crystals[i]][(int)b_crystals[j]];
}


/* ═══════════════════════════════════════════════════════════════
 * §4  KERNEL: bridge_compose_all — parallel domain composition
 * ═══════════════════════════════════════════════════════════════
 *
 * For each domain register, compose micro (domain signal) with
 * macro (system state) and then bridge: CL[CHAOS][composed].
 *
 * micro_ops[i] = domain i's dominant operator
 * macro_op     = system-wide phase_bc
 * results[i]   = bridged operator
 * harmony[i]   = 1 if bridged == HARMONY, 0 otherwise
 *
 * One thread per domain. Usually < 32 domains, so one warp.
 */

extern "C" __global__
void bridge_compose_all(
    const signed char* __restrict__ micro_ops,
    const signed char macro_op,
    signed char* __restrict__ results,
    int* __restrict__ harmony_flags,
    const int n_domains
) {
    const int idx = blockIdx.x * blockDim.x + threadIdx.x;
    if (idx >= n_domains) return;

    int composed = d_CL_TSML[(int)micro_ops[idx]][(int)macro_op];
    int bridged = d_CL_TSML[6][composed];  /* CL[CHAOS][composed] */

    results[idx] = (signed char)bridged;
    harmony_flags[idx] = (bridged == 7) ? 1 : 0;  /* 7 = HARMONY */
}


/* ═══════════════════════════════════════════════════════════════
 * §5  KERNEL: trauma_learn — parallel failure learning
 * ═══════════════════════════════════════════════════════════════
 *
 * When coherence drops, CK learns from failure.
 * Each thread processes one entry in the trauma batch:
 *   - Compose the failure: CL[CHAOS][phase_bc]
 *   - Compose what was needed: CL[phase_b][HARMONY]
 *   - Write TL increments for triple-conviction learning
 *
 * output_pairs: flattened (from, to) pairs for TL increment
 * One thread per trauma event in the batch.
 */

extern "C" __global__
void trauma_learn(
    const signed char* __restrict__ phase_b_ops,
    const signed char* __restrict__ phase_d_ops,
    const signed char* __restrict__ phase_bc_ops,
    signed char* __restrict__ output_from,
    signed char* __restrict__ output_to,
    const int n_events,
    const int pairs_per_event   /* typically 15: 5 trauma pairs × 3 conviction */
) {
    const int idx = blockIdx.x * blockDim.x + threadIdx.x;
    if (idx >= n_events) return;

    int b = phase_b_ops[idx];
    int d = phase_d_ops[idx];
    int bc = phase_bc_ops[idx];
    int base = idx * pairs_per_event;

    /* Trauma chain: B → D → BC → CHAOS → COLLAPSE (5 pairs × 3 reps) */
    for (int rep = 0; rep < 3; rep++) {
        int offset = base + rep * 4;
        output_from[offset + 0] = (signed char)b;
        output_to[offset + 0]   = (signed char)d;
        output_from[offset + 1] = (signed char)d;
        output_to[offset + 1]   = (signed char)bc;
        output_from[offset + 2] = (signed char)bc;
        output_to[offset + 2]   = 6;   /* CHAOS */
        output_from[offset + 3] = 6;   /* CHAOS */
        output_to[offset + 3]   = 4;   /* COLLAPSE */
    }

    /* Lesson: what should have been done? CL[B][HARMONY] = needed */
    int needed = d_CL_TSML[b][7];  /* 7 = HARMONY */
    int lesson_base = base + 12;
    if (lesson_base + 2 < pairs_per_event * n_events) {
        output_from[lesson_base + 0] = (signed char)b;
        output_to[lesson_base + 0]   = 7;   /* HARMONY */
        output_from[lesson_base + 1] = 7;   /* HARMONY */
        output_to[lesson_base + 1]   = (signed char)needed;
        output_from[lesson_base + 2] = (signed char)needed;
        output_to[lesson_base + 2]   = 7;   /* HARMONY */
    }
}


/* ═══════════════════════════════════════════════════════════════
 * §6  KERNEL: crystal_vote — parallel cross-domain voting
 * ═══════════════════════════════════════════════════════════════
 *
 * For crystal sync: each thread checks one signal across all
 * domains and counts votes per target operator.
 *
 * crystal_targets[d * 10 + signal] = target op for domain d
 * crystal_valid[d * 10 + signal]   = 1 if crystallized
 *
 * Output: for each signal, the best target and vote count.
 */

extern "C" __global__
void crystal_vote(
    const signed char* __restrict__ crystal_targets,
    const int* __restrict__ crystal_valid,
    signed char* __restrict__ best_targets,
    int* __restrict__ best_votes,
    const int n_domains,
    const int n_signals   /* always 10 */
) {
    const int signal = blockIdx.x * blockDim.x + threadIdx.x;
    if (signal >= n_signals) return;

    /* Count votes from each domain */
    int votes[10] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0};

    for (int d = 0; d < n_domains; d++) {
        int idx = d * n_signals + signal;
        if (crystal_valid[idx]) {
            int target = crystal_targets[idx];
            if (target >= 0 && target < 10) {
                votes[target]++;
            }
        }
    }

    /* Find majority */
    int best = 0, best_count = 0;
    for (int j = 0; j < 10; j++) {
        if (votes[j] > best_count) {
            best_count = votes[j];
            best = j;
        }
    }

    best_targets[signal] = (signed char)best;
    best_votes[signal] = best_count;
}


/* ═══════════════════════════════════════════════════════════════
 * §7  HOST API — launch wrappers (called from C code)
 * ═══════════════════════════════════════════════════════════════ */

#define CK_BLOCK_SIZE 256

extern "C" {

void ck_gpu_dual_operator(
    signed char* d_being, signed char* d_doing, signed char* d_results,
    int n
) {
    int blocks = (n + CK_BLOCK_SIZE - 1) / CK_BLOCK_SIZE;
    dual_operator<<<blocks, CK_BLOCK_SIZE>>>(d_being, d_doing, d_results, n);
}

void ck_gpu_cross_compose(
    signed char* d_a, signed char* d_b, signed char* d_results,
    int n_a, int n_b
) {
    int total = n_a * n_b;
    int blocks = (total + CK_BLOCK_SIZE - 1) / CK_BLOCK_SIZE;
    cross_compose<<<blocks, CK_BLOCK_SIZE>>>(d_a, d_b, d_results, n_a, n_b);
}

void ck_gpu_bridge_compose(
    signed char* d_micro, signed char macro_op, signed char* d_results,
    int* d_harmony, int n_domains
) {
    int blocks = (n_domains + CK_BLOCK_SIZE - 1) / CK_BLOCK_SIZE;
    bridge_compose_all<<<blocks, CK_BLOCK_SIZE>>>(
        d_micro, macro_op, d_results, d_harmony, n_domains
    );
}

void ck_gpu_trauma_learn(
    signed char* d_phase_b, signed char* d_phase_d, signed char* d_phase_bc,
    signed char* d_out_from, signed char* d_out_to,
    int n_events, int pairs_per_event
) {
    int blocks = (n_events + CK_BLOCK_SIZE - 1) / CK_BLOCK_SIZE;
    trauma_learn<<<blocks, CK_BLOCK_SIZE>>>(
        d_phase_b, d_phase_d, d_phase_bc,
        d_out_from, d_out_to,
        n_events, pairs_per_event
    );
}

void ck_gpu_crystal_vote(
    signed char* d_targets, int* d_valid,
    signed char* d_best_targets, int* d_best_votes,
    int n_domains, int n_signals
) {
    int blocks = (n_signals + CK_BLOCK_SIZE - 1) / CK_BLOCK_SIZE;
    crystal_vote<<<blocks, CK_BLOCK_SIZE>>>(
        d_targets, d_valid, d_best_targets, d_best_votes,
        n_domains, n_signals
    );
}

} /* extern "C" */

#endif /* __CUDACC__ */
