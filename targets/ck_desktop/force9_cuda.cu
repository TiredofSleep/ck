/*
 * force9_cuda.cu -- Force9 GPU Encoder
 * Full pipeline: RGB -> 9x9x9 Force Cube -> RLE -> packed bytes
 * All on GPU. Zero CPU involvement for encode.
 *
 * Compile: nvcc -O2 -shared -o force9_cuda.dll force9_cuda.cu
 * Python:  ctypes.CDLL("force9_cuda.dll")
 *
 * (c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
 */

#include <cuda_runtime.h>
#include <stdint.h>

extern "C" {

/* Encode RGB pixels to Force9 packed values (9x9x9 cube).
 * One thread per pixel. Fully parallel.
 *
 * rgb:    input RGB pixels (3 bytes per pixel, N pixels)
 * f9:     output Force9 packed values (uint16, N values)
 * n:      number of pixels
 */
__global__ void force9_encode_kernel(
    const uint8_t* __restrict__ rgb,
    uint16_t* __restrict__ f9,
    int n)
{
    int idx = blockDim.x * blockIdx.x + threadIdx.x;
    if (idx >= n) return;

    int r = rgb[idx * 3];
    int g = rgb[idx * 3 + 1];
    int b = rgb[idx * 3 + 2];

    /* Luminance: perceptual brightness 0-8 */
    int lum = (r * 299 + g * 587 + b * 114) / (1000 * 29);
    if (lum > 8) lum = 8;

    /* Temperature: warm(red) vs cool(blue) 0-8 */
    int warmth = r - b; /* -255 to +255 */
    int temp = (warmth + 255) * 9 / 511;
    if (temp < 0) temp = 0;
    if (temp > 8) temp = 8;

    /* Saturation: vivid vs gray 0-8 */
    int max_c = r; if (g > max_c) max_c = g; if (b > max_c) max_c = b;
    int min_c = r; if (g < min_c) min_c = g; if (b < min_c) min_c = b;
    int sat = (max_c - min_c) * 9 / 256;
    if (sat > 8) sat = 8;

    f9[idx] = (uint16_t)(lum * 81 + temp * 9 + sat);
}

/* Find RLE run boundaries.
 * Marks positions where value changes.
 *
 * f9:         input Force9 values
 * boundaries: output boolean array (1 = value changed from previous)
 * n:          number of values
 */
__global__ void rle_boundaries_kernel(
    const uint16_t* __restrict__ f9,
    uint8_t* __restrict__ boundaries,
    int n)
{
    int idx = blockDim.x * blockIdx.x + threadIdx.x;
    if (idx >= n) return;

    if (idx == 0) {
        boundaries[0] = 1; /* first value is always a boundary */
    } else {
        boundaries[idx] = (f9[idx] != f9[idx - 1]) ? 1 : 0;
    }
}

/* Decode Force9 packed value to RGB.
 * One thread per pixel.
 *
 * f9:  input Force9 packed values
 * rgb: output RGB pixels (3 bytes per pixel)
 * n:   number of pixels
 */
__global__ void force9_decode_kernel(
    const uint16_t* __restrict__ f9,
    uint8_t* __restrict__ rgb,
    int n)
{
    int idx = blockDim.x * blockIdx.x + threadIdx.x;
    if (idx >= n) return;

    uint16_t val = f9[idx];
    int lum = val / 81;
    int temp = (val % 81) / 9;
    int sat = val % 9;

    int brightness = lum * 255 / 8;
    int warmth = (temp - 4) * 32;
    float sat_scale = sat / 8.0f;

    int r = (int)(brightness + warmth * sat_scale);
    int g = (int)(brightness - fabsf((float)warmth) * sat_scale * 0.3f);
    int b = (int)(brightness - warmth * sat_scale);

    if (r < 0) r = 0; if (r > 255) r = 255;
    if (g < 0) g = 0; if (g > 255) g = 255;
    if (b < 0) b = 0; if (b > 255) b = 255;

    rgb[idx * 3]     = (uint8_t)r;
    rgb[idx * 3 + 1] = (uint8_t)g;
    rgb[idx * 3 + 2] = (uint8_t)b;
}

/* Host API: allocate GPU buffers */
typedef struct {
    uint8_t*  d_rgb;        /* GPU RGB buffer */
    uint16_t* d_f9;         /* GPU Force9 buffer */
    uint8_t*  d_boundaries; /* GPU RLE boundary marks */
    uint8_t*  d_rgb_out;    /* GPU decoded RGB output */
    int       width;
    int       height;
    int       n_pixels;
    int       allocated;
} Force9Context;

__host__ Force9Context* force9_create(int width, int height) {
    Force9Context* ctx = (Force9Context*)malloc(sizeof(Force9Context));
    ctx->width = width;
    ctx->height = height;
    ctx->n_pixels = width * height;

    cudaMalloc(&ctx->d_rgb, ctx->n_pixels * 3);
    cudaMalloc(&ctx->d_f9, ctx->n_pixels * sizeof(uint16_t));
    cudaMalloc(&ctx->d_boundaries, ctx->n_pixels);
    cudaMalloc(&ctx->d_rgb_out, ctx->n_pixels * 3);
    ctx->allocated = 1;

    return ctx;
}

__host__ void force9_destroy(Force9Context* ctx) {
    if (ctx && ctx->allocated) {
        cudaFree(ctx->d_rgb);
        cudaFree(ctx->d_f9);
        cudaFree(ctx->d_boundaries);
        cudaFree(ctx->d_rgb_out);
        ctx->allocated = 0;
    }
    free(ctx);
}

/* Encode: RGB -> Force9. Returns Force9 values in d_f9.
 * h_rgb: host RGB buffer (width*height*3 bytes)
 */
__host__ float force9_encode(Force9Context* ctx, const uint8_t* h_rgb) {
    cudaEvent_t start, stop;
    cudaEventCreate(&start);
    cudaEventCreate(&stop);
    cudaEventRecord(start);

    /* Copy RGB to GPU */
    cudaMemcpy(ctx->d_rgb, h_rgb, ctx->n_pixels * 3, cudaMemcpyHostToDevice);

    /* Encode */
    int threads = 256;
    int blocks = (ctx->n_pixels + threads - 1) / threads;
    force9_encode_kernel<<<blocks, threads>>>(ctx->d_rgb, ctx->d_f9, ctx->n_pixels);

    /* Find RLE boundaries */
    rle_boundaries_kernel<<<blocks, threads>>>(ctx->d_f9, ctx->d_boundaries, ctx->n_pixels);

    cudaEventRecord(stop);
    cudaEventSynchronize(stop);

    float ms = 0;
    cudaEventElapsedTime(&ms, start, stop);
    cudaEventDestroy(start);
    cudaEventDestroy(stop);
    return ms;
}

/* Get encoded Force9 values from GPU.
 * h_f9: host buffer (width*height * sizeof(uint16_t))
 */
__host__ void force9_get_f9(Force9Context* ctx, uint16_t* h_f9) {
    cudaMemcpy(h_f9, ctx->d_f9, ctx->n_pixels * sizeof(uint16_t), cudaMemcpyDeviceToHost);
}

/* Get RLE boundaries from GPU.
 * h_boundaries: host buffer (width*height bytes)
 */
__host__ void force9_get_boundaries(Force9Context* ctx, uint8_t* h_boundaries) {
    cudaMemcpy(h_boundaries, ctx->d_boundaries, ctx->n_pixels, cudaMemcpyDeviceToHost);
}

/* Decode: Force9 -> RGB on GPU.
 * h_f9:  host Force9 values (width*height * sizeof(uint16_t))
 * h_rgb: host output RGB buffer (width*height*3 bytes)
 */
__host__ float force9_decode(Force9Context* ctx, const uint16_t* h_f9, uint8_t* h_rgb) {
    cudaEvent_t start, stop;
    cudaEventCreate(&start);
    cudaEventCreate(&stop);
    cudaEventRecord(start);

    cudaMemcpy(ctx->d_f9, h_f9, ctx->n_pixels * sizeof(uint16_t), cudaMemcpyHostToDevice);

    int threads = 256;
    int blocks = (ctx->n_pixels + threads - 1) / threads;
    force9_decode_kernel<<<blocks, threads>>>(ctx->d_f9, ctx->d_rgb_out, ctx->n_pixels);

    cudaMemcpy(h_rgb, ctx->d_rgb_out, ctx->n_pixels * 3, cudaMemcpyDeviceToHost);

    cudaEventRecord(stop);
    cudaEventSynchronize(stop);

    float ms = 0;
    cudaEventElapsedTime(&ms, start, stop);
    cudaEventDestroy(start);
    cudaEventDestroy(stop);
    return ms;
}

/* Get encode time for the GPU kernels only (no memcpy) */
__host__ float force9_encode_gpu_only(Force9Context* ctx) {
    cudaEvent_t start, stop;
    cudaEventCreate(&start);
    cudaEventCreate(&stop);
    cudaEventRecord(start);

    int threads = 256;
    int blocks = (ctx->n_pixels + threads - 1) / threads;
    force9_encode_kernel<<<blocks, threads>>>(ctx->d_rgb, ctx->d_f9, ctx->n_pixels);
    rle_boundaries_kernel<<<blocks, threads>>>(ctx->d_f9, ctx->d_boundaries, ctx->n_pixels);

    cudaEventRecord(stop);
    cudaEventSynchronize(stop);

    float ms = 0;
    cudaEventElapsedTime(&ms, start, stop);
    cudaEventDestroy(start);
    cudaEventDestroy(stop);
    return ms;
}

} /* extern "C" */
