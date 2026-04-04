/*
 * TIG Lattice CUDA Kernel v8.0
 * One thread per cell. Table in constant memory.
 * 
 * Compile: nvcc -O3 -o tig_lattice tig_cuda_kernel.cu
 * Or use CuPy wrapper from Python (see tig_genesis.py)
 *
 * (c) 2025 Brayden Langley / 7Site LLC
 */

#include <stdio.h>
#include <stdint.h>

__constant__ int8_t COMP[10][10] = {
    {0,1,2,3,4,5,6,7,8,9}, {1,2,3,4,5,6,7,2,6,6},
    {2,3,3,4,5,6,7,3,6,6}, {3,4,4,4,5,6,7,4,6,6},
    {4,5,5,5,5,6,7,5,7,7}, {5,6,6,6,6,6,7,6,7,7},
    {6,7,7,7,7,7,7,7,7,7}, {7,2,3,4,5,6,7,8,9,0},
    {8,6,6,6,7,7,7,9,7,8}, {9,6,6,6,7,7,7,0,8,0},
};

__global__ void lattice_tick(
    const int8_t* __restrict__ cells_in,
    int8_t* __restrict__ cells_out,
    const int R, const int C
) {
    const int idx = blockIdx.x * blockDim.x + threadIdx.x;
    if (idx >= R * C) return;

    const int r = idx / C;
    const int c = idx % C;
    const int8_t me = cells_in[idx];

    int votes[10] = {0};

    #pragma unroll
    for (int di = -1; di <= 1; di++) {
        #pragma unroll
        for (int dj = -1; dj <= 1; dj++) {
            const int nr = (r + di + R) % R;
            const int nc = (c + dj + C) % C;
            const int8_t nb = cells_in[nr * C + nc];
            votes[COMP[me][nb]]++;
        }
    }

    int8_t best = 0;
    int best_count = votes[0];
    #pragma unroll
    for (int8_t s = 1; s < 10; s++) {
        if (votes[s] > best_count) { best = s; best_count = votes[s]; }
    }
    cells_out[idx] = best;
}

__global__ void lattice_coherence(
    const int8_t* __restrict__ cells,
    int* __restrict__ valid_count,
    int* __restrict__ basin_count,
    const int R, const int C
) {
    const int idx = blockIdx.x * blockDim.x + threadIdx.x;
    if (idx >= R * C) return;

    const int r = idx / C;
    const int c = idx % C;
    const int8_t me = cells[idx];

    // Check if trivial (all neighbors compose to self)
    bool trivial = true;
    for (int di = -1; di <= 1; di++) {
        for (int dj = -1; dj <= 1; dj++) {
            if (di == 0 && dj == 0) continue;
            int nr = (r + di + R) % R;
            int nc = (c + dj + C) % C;
            if (COMP[me][cells[nr * C + nc]] != me) { trivial = false; break; }
        }
        if (!trivial) break;
    }

    if (!trivial || me == 7) atomicAdd(valid_count, 1);
    if (me >= 4 && me <= 8) atomicAdd(basin_count, 1);
}

// Multi-tick: run N ticks without GPU?CPU transfer
__global__ void lattice_multi_tick(
    int8_t* cells_a, int8_t* cells_b,
    const int R, const int C, const int n_ticks
) {
    const int idx = blockIdx.x * blockDim.x + threadIdx.x;
    if (idx >= R * C) return;

    const int r = idx / C;
    const int c = idx % C;

    for (int t = 0; t < n_ticks; t++) {
        int8_t* src = (t % 2 == 0) ? cells_a : cells_b;
        int8_t* dst = (t % 2 == 0) ? cells_b : cells_a;

        int8_t me = src[idx];
        int votes[10] = {0};

        #pragma unroll
        for (int di = -1; di <= 1; di++) {
            #pragma unroll
            for (int dj = -1; dj <= 1; dj++) {
                int nr = (r + di + R) % R;
                int nc = (c + dj + C) % C;
                votes[COMP[me][src[nr * C + nc]]]++;
            }
        }

        int8_t best = 0; int best_count = votes[0];
        for (int8_t s = 1; s < 10; s++) {
            if (votes[s] > best_count) { best = s; best_count = votes[s]; }
        }
        dst[idx] = best;
        __syncthreads();
    }
}

// Host convenience
extern "C" {
    void tick_host(int8_t* h_cells, int R, int C, int n_ticks) {
        int N = R * C;
        int8_t *d_a, *d_b;
        cudaMalloc(&d_a, N); cudaMalloc(&d_b, N);
        cudaMemcpy(d_a, h_cells, N, cudaMemcpyHostToDevice);

        int threads = 256;
        int blocks = (N + threads - 1) / threads;

        if (n_ticks == 1) {
            lattice_tick<<<blocks, threads>>>(d_a, d_b, R, C);
            cudaMemcpy(h_cells, d_b, N, cudaMemcpyDeviceToHost);
        } else {
            lattice_multi_tick<<<blocks, threads>>>(d_a, d_b, R, C, n_ticks);
            int8_t* result = (n_ticks % 2 == 0) ? d_a : d_b;
            cudaMemcpy(h_cells, result, N, cudaMemcpyDeviceToHost);
        }

        cudaFree(d_a); cudaFree(d_b);
    }
}