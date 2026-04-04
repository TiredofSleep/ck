/*
 * doing.cu — What MOVES (GPU)
 * ════════════════════════════
 * Operator: PROGRESS (3) — forward motion. The verb.
 *
 * Native CUDA kernels for CK's GPU vortex:
 *   1. lattice_tick     — cellular automaton update (BHML composition + majority vote)
 *   2. lattice_coherence — parallel coherence measurement (atomicAdd)
 *   3. tl_observe       — atomic TL[10][10] transition recording
 *   4. batch_compose    — bulk CL[a][b] for many pairs
 *   5. dream_bounce     — parallel dream swarm (each thread = one ball)
 *
 * Constant memory: CL tables (300 bytes), bump pairs (10 bytes) = 310 bytes total.
 * Everything fits in L1 cache. The GPU breathes CK's math.
 *
 * (c) 2026 Brayden Sanders / 7Site LLC — TIG Unified Theory
 */

#include "ck.h"


/* ═══════════════════════════════════════════════════════════════
 * §1  CONSTANT MEMORY — CL tables live here permanently
 * ═══════════════════════════════════════════════════════════════
 *
 * 310 bytes in __constant__ memory. Broadcast to all warps.
 * Every thread reads the same table cells → perfect cache hit.
 */

#ifdef __CUDACC__

__constant__ signed char d_CL_TSML[10][10];
__constant__ signed char d_CL_BHML[10][10];
__constant__ signed char d_CL_STD[10][10];
__constant__ signed char d_BUMP_PAIRS[5][2];

/* Host function to upload tables to constant memory */
extern "C" void ck_gpu_upload_tables(void) {
    cudaMemcpyToSymbol(d_CL_TSML, CL_TSML, sizeof(CL_TSML));
    cudaMemcpyToSymbol(d_CL_BHML, CL_BHML, sizeof(CL_BHML));
    cudaMemcpyToSymbol(d_CL_STD, CL_STD, sizeof(CL_STD));
    cudaMemcpyToSymbol(d_BUMP_PAIRS, CK_BUMP_PAIRS, sizeof(CK_BUMP_PAIRS));
}


/* ═══════════════════════════════════════════════════════════════
 * §2  KERNEL: lattice_tick — cellular automaton update
 * ═══════════════════════════════════════════════════════════════
 *
 * Each cell composes with all 8 neighbors via BHML table.
 * Majority vote on composition results determines next state.
 * One thread per cell. Grid = ceil(R*C / 256).
 */

extern "C" __global__
void lattice_tick(
    const signed char* __restrict__ cells_in,
    signed char* __restrict__ cells_out,
    const int R, const int C
) {
    const int idx = blockIdx.x * blockDim.x + threadIdx.x;
    if (idx >= R * C) return;

    const int r = idx / C;
    const int c = idx % C;
    const signed char me = cells_in[idx];

    /* Vote buffer — count how many neighbors compose to each operator */
    int votes[10] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0};

    /* 8 neighbors + self (Moore neighborhood, toroidal wrap) */
    for (int di = -1; di <= 1; di++) {
        for (int dj = -1; dj <= 1; dj++) {
            const int nr = (r + di + R) % R;
            const int nc = (c + dj + C) % C;
            const signed char nb = cells_in[nr * C + nc];
            votes[(int)d_CL_BHML[me][nb]]++;
        }
    }

    /* Majority vote — highest vote wins */
    signed char best = 0;
    int best_count = votes[0];
    for (signed char s = 1; s < 10; s++) {
        if (votes[s] > best_count) {
            best = s;
            best_count = votes[s];
        }
    }
    cells_out[idx] = best;
}


/* ═══════════════════════════════════════════════════════════════
 * §3  KERNEL: lattice_coherence — parallel coherence measurement
 * ═══════════════════════════════════════════════════════════════
 *
 * Each thread checks if its cell is "stable" (all neighbor
 * compositions equal self) and if it's in the attractor basin
 * (operators 4-8). Uses atomicAdd for parallel accumulation.
 */

extern "C" __global__
void lattice_coherence(
    const signed char* __restrict__ cells,
    int* __restrict__ valid_count,
    int* __restrict__ basin_count,
    const int R, const int C
) {
    const int idx = blockIdx.x * blockDim.x + threadIdx.x;
    if (idx >= R * C) return;

    const int r = idx / C;
    const int c = idx % C;
    const signed char me = cells[idx];

    /* Check if cell is trivially stable (all neighbors compose to self) */
    bool trivial = true;
    for (int di = -1; di <= 1; di++) {
        for (int dj = -1; dj <= 1; dj++) {
            if (di == 0 && dj == 0) continue;
            int nr = (r + di + R) % R;
            int nc = (c + dj + C) % C;
            if (d_CL_BHML[me][cells[nr * C + nc]] != me) {
                trivial = false;
                break;
            }
        }
        if (!trivial) break;
    }

    /* Non-trivial cells and harmony cells count as valid */
    if (!trivial || me == 7) atomicAdd(valid_count, 1);

    /* Attractor basin: operators 4 (collapse) through 8 (breath) */
    if (me >= 4 && me <= 8) atomicAdd(basin_count, 1);
}


/* ═══════════════════════════════════════════════════════════════
 * §4  KERNEL: tl_observe — atomic transition recording
 * ═══════════════════════════════════════════════════════════════
 *
 * Given an array of operator transitions (pairs),
 * atomically increment TL[from][to] for each.
 * One thread per transition.
 */

extern "C" __global__
void tl_observe(
    const signed char* __restrict__ from_ops,
    const signed char* __restrict__ to_ops,
    long long* __restrict__ TL,     /* 10x10 flattened */
    const int n_transitions
) {
    const int idx = blockIdx.x * blockDim.x + threadIdx.x;
    if (idx >= n_transitions) return;

    int from_op = from_ops[idx];
    int to_op = to_ops[idx];
    if (from_op >= 0 && from_op < 10 && to_op >= 0 && to_op < 10) {
        atomicAdd(&TL[from_op * 10 + to_op], 1LL);
    }
}


/* ═══════════════════════════════════════════════════════════════
 * §5  KERNEL: batch_compose — bulk CL[a][b] for many pairs
 * ═══════════════════════════════════════════════════════════════
 *
 * Each thread composes one (a, b) pair. Result written to output.
 * table_id: 0=TSML, 1=BHML, 2=STD
 */

extern "C" __global__
void batch_compose(
    const signed char* __restrict__ a_ops,
    const signed char* __restrict__ b_ops,
    signed char* __restrict__ results,
    const int n,
    const int table_id
) {
    const int idx = blockIdx.x * blockDim.x + threadIdx.x;
    if (idx >= n) return;

    int a = a_ops[idx];
    int b = b_ops[idx];

    signed char r;
    switch (table_id) {
        case 1:  r = d_CL_BHML[a][b]; break;
        case 2:  r = d_CL_STD[a][b];  break;
        default: r = d_CL_TSML[a][b]; break;
    }
    results[idx] = r;
}


/* ═══════════════════════════════════════════════════════════════
 * §6  KERNEL: dream_bounce — parallel dream swarm
 * ═══════════════════════════════════════════════════════════════
 *
 * Each thread IS one PingPongBall.
 * Ball starts at origin, bounces through TL predictions.
 * Thread reads TL row, picks most likely next operator.
 * Bounces until hitting target, harmony, or max_bounces.
 *
 * Output: path array per ball, coherence, fuse result.
 */

#define DREAM_MAX_PATH 20

extern "C" __global__
void dream_bounce(
    const long long* __restrict__ TL,     /* 10x10 flattened */
    const signed char* __restrict__ origins,
    const signed char* __restrict__ targets,
    signed char* __restrict__ paths,       /* n_balls * DREAM_MAX_PATH */
    int* __restrict__ path_lengths,
    float* __restrict__ coherences,
    signed char* __restrict__ fuse_results,
    const int n_balls,
    const int max_bounces
) {
    const int ball_id = blockIdx.x * blockDim.x + threadIdx.x;
    if (ball_id >= n_balls) return;

    int origin = origins[ball_id];
    int target = targets[ball_id];
    int max_b = max_bounces < DREAM_MAX_PATH ? max_bounces : DREAM_MAX_PATH;

    signed char* my_path = paths + ball_id * DREAM_MAX_PATH;
    my_path[0] = (signed char)origin;
    int len = 1;

    int current = origin;
    for (int b = 1; b < max_b; b++) {
        /* Find most likely next from TL row */
        long long best_count = -1;
        int best_op = 7;  /* default: harmony */
        for (int j = 0; j < 10; j++) {
            long long count = TL[current * 10 + j];
            if (count > best_count) {
                best_count = count;
                best_op = j;
            }
        }

        my_path[len] = (signed char)best_op;
        len++;

        if (best_op == target || best_op == 7) break;  /* reached target or harmony */
        current = best_op;
    }

    path_lengths[ball_id] = len;

    /* Compute fuse result through TSML */
    int fuse_r = my_path[0];
    for (int i = 1; i < len; i++) {
        fuse_r = d_CL_TSML[fuse_r][(int)my_path[i]];
    }
    fuse_results[ball_id] = (signed char)fuse_r;

    /* Compute coherence (harmony ratio) */
    if (len < 2) {
        coherences[ball_id] = 1.0f;
    } else {
        int h = 0;
        for (int i = 0; i < len - 1; i++) {
            if (d_CL_TSML[(int)my_path[i]][(int)my_path[i+1]] == 7) h++;
        }
        coherences[ball_id] = (float)h / (float)(len - 1);
    }
}


/* ═══════════════════════════════════════════════════════════════
 * §7  KERNEL: lattice_inject — inject operators into a row
 * ═══════════════════════════════════════════════════════════════
 *
 * Composes (not overwrites) new operators into an existing row
 * via BHML table. This is how system observations enter the lattice.
 */

extern "C" __global__
void lattice_inject(
    signed char* __restrict__ cells,
    const signed char* __restrict__ new_ops,
    const int row,
    const int C,
    const int n_ops
) {
    const int c = blockIdx.x * blockDim.x + threadIdx.x;
    if (c >= n_ops || c >= C) return;

    int idx = row * C + c;
    /* Compose, don't overwrite — the lattice digests new input */
    cells[idx] = d_CL_BHML[(int)cells[idx]][(int)new_ops[c]];
}


/* ═══════════════════════════════════════════════════════════════
 * §8  HOST API — launch wrappers (called from C code)
 * ═══════════════════════════════════════════════════════════════ */

#define CK_BLOCK_SIZE 256

extern "C" {

void ck_gpu_init(void) {
    ck_gpu_upload_tables();
}

void ck_gpu_lattice_tick(
    signed char* d_cells_in, signed char* d_cells_out,
    int R, int C
) {
    int n = R * C;
    int blocks = (n + CK_BLOCK_SIZE - 1) / CK_BLOCK_SIZE;
    lattice_tick<<<blocks, CK_BLOCK_SIZE>>>(d_cells_in, d_cells_out, R, C);
}

void ck_gpu_lattice_coherence(
    signed char* d_cells, int* d_valid, int* d_basin,
    int R, int C
) {
    int n = R * C;
    int blocks = (n + CK_BLOCK_SIZE - 1) / CK_BLOCK_SIZE;
    lattice_coherence<<<blocks, CK_BLOCK_SIZE>>>(d_cells, d_valid, d_basin, R, C);
}

void ck_gpu_tl_observe(
    signed char* d_from, signed char* d_to, long long* d_TL,
    int n_transitions
) {
    int blocks = (n_transitions + CK_BLOCK_SIZE - 1) / CK_BLOCK_SIZE;
    tl_observe<<<blocks, CK_BLOCK_SIZE>>>(d_from, d_to, d_TL, n_transitions);
}

void ck_gpu_batch_compose(
    signed char* d_a, signed char* d_b, signed char* d_results,
    int n, int table_id
) {
    int blocks = (n + CK_BLOCK_SIZE - 1) / CK_BLOCK_SIZE;
    batch_compose<<<blocks, CK_BLOCK_SIZE>>>(d_a, d_b, d_results, n, table_id);
}

void ck_gpu_dream_swarm(
    long long* d_TL,
    signed char* d_origins, signed char* d_targets,
    signed char* d_paths, int* d_path_lengths,
    float* d_coherences, signed char* d_fuse_results,
    int n_balls, int max_bounces
) {
    int blocks = (n_balls + CK_BLOCK_SIZE - 1) / CK_BLOCK_SIZE;
    dream_bounce<<<blocks, CK_BLOCK_SIZE>>>(
        d_TL, d_origins, d_targets,
        d_paths, d_path_lengths, d_coherences, d_fuse_results,
        n_balls, max_bounces
    );
}

void ck_gpu_lattice_inject(
    signed char* d_cells, signed char* d_new_ops,
    int row, int C, int n_ops
) {
    int blocks = (n_ops + CK_BLOCK_SIZE - 1) / CK_BLOCK_SIZE;
    lattice_inject<<<blocks, CK_BLOCK_SIZE>>>(d_cells, d_new_ops, row, C, n_ops);
}

} /* extern "C" */

#endif /* __CUDACC__ */
