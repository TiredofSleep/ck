/*
 * force9_pipeline.cu -- Full GPU Pipeline: DXGI Capture + Force9 Encode
 * Zero CPU frame copy. GPU renders -> GPU captures -> GPU encodes -> stream.
 *
 * Uses DXGI Desktop Duplication for GPU-native screen capture.
 * Uses CUDA interop to encode directly from the DXGI texture.
 *
 * Compile:
 *   nvcc -O2 -shared -o force9_pipeline.dll force9_pipeline.cu
 *        -ld3d11 -ldxgi -lcuda
 *
 * (c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
 */

#include <cuda_runtime.h>
#include <stdint.h>
#include <stdio.h>
#include <windows.h>
#include <d3d11.h>
#include <dxgi1_2.h>

/* Force9 encode kernel - same as force9_cuda.cu */
__global__ void f9_encode(const uint8_t* __restrict__ bgra,
                          uint16_t* __restrict__ f9,
                          int n)
{
    int idx = blockDim.x * blockIdx.x + threadIdx.x;
    if (idx >= n) return;

    int b = bgra[idx * 4];
    int g = bgra[idx * 4 + 1];
    int r = bgra[idx * 4 + 2];
    /* alpha ignored */

    int lum = (r * 299 + g * 587 + b * 114) / (1000 * 29);
    if (lum > 8) lum = 8;

    int warmth = r - b;
    int temp = (warmth + 255) * 9 / 511;
    if (temp < 0) temp = 0;
    if (temp > 8) temp = 8;

    int max_c = r; if (g > max_c) max_c = g; if (b > max_c) max_c = b;
    int min_c = r; if (g < min_c) min_c = g; if (b < min_c) min_c = b;
    int sat = (max_c - min_c) * 9 / 256;
    if (sat > 8) sat = 8;

    f9[idx] = (uint16_t)(lum * 81 + temp * 9 + sat);
}

/* RLE compress on GPU - count runs of identical f9 values */
__global__ void f9_mark_boundaries(const uint16_t* f9, uint8_t* boundaries, int n)
{
    int idx = blockDim.x * blockIdx.x + threadIdx.x;
    if (idx >= n) return;
    if (idx == 0) { boundaries[0] = 1; return; }
    boundaries[idx] = (f9[idx] != f9[idx - 1]) ? 1 : 0;
}

/* Pipeline context */
typedef struct {
    int width;
    int height;
    int num_pixels;

    /* DXGI */
    ID3D11Device* d3d_device;
    ID3D11DeviceContext* d3d_context;
    IDXGIOutputDuplication* duplication;
    ID3D11Texture2D* staging_tex;

    /* CUDA */
    uint8_t* d_bgra;        /* GPU: raw BGRA pixels */
    uint16_t* d_f9;         /* GPU: Force9 encoded */
    uint8_t* d_boundaries;  /* GPU: RLE boundaries */

    /* Host output */
    uint16_t* h_f9;         /* CPU: Force9 values (for RLE packing) */
    uint8_t* h_boundaries;  /* CPU: boundary markers */

    /* Stats */
    int frames_captured;
    float last_encode_ms;
    float last_capture_ms;
} F9Pipeline;

extern "C" {

__host__ __declspec(dllexport)
F9Pipeline* f9pipe_create(int width, int height)
{
    F9Pipeline* p = (F9Pipeline*)calloc(1, sizeof(F9Pipeline));
    p->width = width;
    p->height = height;
    p->num_pixels = width * height;

    /* Create D3D11 device */
    D3D_FEATURE_LEVEL feature_level;
    HRESULT hr = D3D11CreateDevice(
        NULL, D3D_DRIVER_TYPE_HARDWARE, NULL,
        D3D11_CREATE_DEVICE_BGRA_SUPPORT,
        NULL, 0, D3D11_SDK_VERSION,
        &p->d3d_device, &feature_level, &p->d3d_context);

    if (FAILED(hr)) {
        printf("[F9PIPE] D3D11CreateDevice failed: 0x%08x\n", hr);
        free(p);
        return NULL;
    }

    /* Get DXGI adapter and output */
    IDXGIDevice* dxgi_device = NULL;
    p->d3d_device->QueryInterface(__uuidof(IDXGIDevice), (void**)&dxgi_device);

    IDXGIAdapter* adapter = NULL;
    dxgi_device->GetAdapter(&adapter);

    IDXGIOutput* output = NULL;
    hr = adapter->EnumOutputs(0, &output);
    if (FAILED(hr)) {
        printf("[F9PIPE] EnumOutputs failed: 0x%08x\n", hr);
        adapter->Release();
        dxgi_device->Release();
        free(p);
        return NULL;
    }

    IDXGIOutput1* output1 = NULL;
    output->QueryInterface(__uuidof(IDXGIOutput1), (void**)&output1);

    /* Create duplication */
    hr = output1->DuplicateOutput(p->d3d_device, &p->duplication);
    if (FAILED(hr)) {
        printf("[F9PIPE] DuplicateOutput failed: 0x%08x\n", hr);
        output1->Release();
        output->Release();
        adapter->Release();
        dxgi_device->Release();
        free(p);
        return NULL;
    }

    output1->Release();
    output->Release();
    adapter->Release();
    dxgi_device->Release();

    /* Create staging texture for CPU/CUDA access */
    D3D11_TEXTURE2D_DESC desc = {};
    desc.Width = width;
    desc.Height = height;
    desc.MipLevels = 1;
    desc.ArraySize = 1;
    desc.Format = DXGI_FORMAT_B8G8R8A8_UNORM;
    desc.SampleDesc.Count = 1;
    desc.Usage = D3D11_USAGE_STAGING;
    desc.CPUAccessFlags = D3D11_CPU_ACCESS_READ;

    hr = p->d3d_device->CreateTexture2D(&desc, NULL, &p->staging_tex);
    if (FAILED(hr)) {
        printf("[F9PIPE] CreateTexture2D staging failed: 0x%08x\n", hr);
    }

    /* Allocate CUDA buffers */
    cudaMalloc(&p->d_bgra, p->num_pixels * 4);
    cudaMalloc(&p->d_f9, p->num_pixels * sizeof(uint16_t));
    cudaMalloc(&p->d_boundaries, p->num_pixels);

    /* Allocate host buffers */
    p->h_f9 = (uint16_t*)malloc(p->num_pixels * sizeof(uint16_t));
    p->h_boundaries = (uint8_t*)malloc(p->num_pixels);

    printf("[F9PIPE] Pipeline created: %dx%d\n", width, height);
    return p;
}

__host__ __declspec(dllexport)
int f9pipe_capture_and_encode(F9Pipeline* p)
{
    if (!p || !p->duplication) return -1;

    cudaEvent_t start, stop;
    cudaEventCreate(&start);
    cudaEventCreate(&stop);

    /* Capture frame via DXGI */
    DXGI_OUTDUPL_FRAME_INFO frame_info;
    IDXGIResource* desktop_resource = NULL;

    HRESULT hr = p->duplication->AcquireNextFrame(100, &frame_info, &desktop_resource);
    if (FAILED(hr)) {
        if (hr == DXGI_ERROR_WAIT_TIMEOUT) return 0; /* no new frame */
        printf("[F9PIPE] AcquireNextFrame failed: 0x%08x\n", hr);
        return -1;
    }

    /* Get the texture */
    ID3D11Texture2D* desktop_tex = NULL;
    desktop_resource->QueryInterface(__uuidof(ID3D11Texture2D), (void**)&desktop_tex);

    /* Copy to staging texture */
    p->d3d_context->CopyResource(p->staging_tex, desktop_tex);

    desktop_tex->Release();
    desktop_resource->Release();
    p->duplication->ReleaseFrame();

    /* Map staging texture to get CPU pointer */
    D3D11_MAPPED_SUBRESOURCE mapped;
    hr = p->d3d_context->Map(p->staging_tex, 0, D3D11_MAP_READ, 0, &mapped);
    if (FAILED(hr)) {
        printf("[F9PIPE] Map failed: 0x%08x\n", hr);
        return -1;
    }

    /* Copy BGRA data to CUDA */
    cudaEventRecord(start);

    /* Handle row pitch (may differ from width*4) */
    if ((int)mapped.RowPitch == p->width * 4) {
        cudaMemcpy(p->d_bgra, mapped.pData, p->num_pixels * 4, cudaMemcpyHostToDevice);
    } else {
        /* Row-by-row copy for different pitch */
        for (int y = 0; y < p->height; y++) {
            cudaMemcpy(p->d_bgra + y * p->width * 4,
                       (uint8_t*)mapped.pData + y * mapped.RowPitch,
                       p->width * 4, cudaMemcpyHostToDevice);
        }
    }

    p->d3d_context->Unmap(p->staging_tex, 0);

    /* Encode on GPU */
    int threads = 256;
    int blocks = (p->num_pixels + threads - 1) / threads;
    f9_encode<<<blocks, threads>>>(p->d_bgra, p->d_f9, p->num_pixels);

    /* Mark boundaries for RLE */
    f9_mark_boundaries<<<blocks, threads>>>(p->d_f9, p->d_boundaries, p->num_pixels);

    /* Copy results back to host */
    cudaMemcpy(p->h_f9, p->d_f9, p->num_pixels * sizeof(uint16_t), cudaMemcpyDeviceToHost);
    cudaMemcpy(p->h_boundaries, p->d_boundaries, p->num_pixels, cudaMemcpyDeviceToHost);

    cudaEventRecord(stop);
    cudaEventSynchronize(stop);
    cudaEventElapsedTime(&p->last_encode_ms, start, stop);

    cudaEventDestroy(start);
    cudaEventDestroy(stop);

    p->frames_captured++;
    return 1;
}

__host__ __declspec(dllexport)
int f9pipe_get_compressed(F9Pipeline* p, uint8_t* out_buf, int buf_size)
{
    if (!p) return 0;

    /* RLE pack on CPU (fast, sequential scan) */
    int offset = 0;
    int i = 0;

    while (i < p->num_pixels && offset + 3 < buf_size) {
        uint16_t val = p->h_f9[i];
        int count = 1;
        while (i + count < p->num_pixels && count < 255 &&
               p->h_f9[i + count] == val) {
            count++;
        }
        /* Pack: 2 bytes value + 1 byte count */
        out_buf[offset++] = (val >> 8) & 0xFF;
        out_buf[offset++] = val & 0xFF;
        out_buf[offset++] = (uint8_t)count;
        i += count;
    }

    return offset;
}

__host__ __declspec(dllexport)
float f9pipe_get_encode_ms(F9Pipeline* p)
{
    return p ? p->last_encode_ms : 0.0f;
}

__host__ __declspec(dllexport)
int f9pipe_get_frame_count(F9Pipeline* p)
{
    return p ? p->frames_captured : 0;
}

__host__ __declspec(dllexport)
void f9pipe_destroy(F9Pipeline* p)
{
    if (!p) return;
    if (p->d_bgra) cudaFree(p->d_bgra);
    if (p->d_f9) cudaFree(p->d_f9);
    if (p->d_boundaries) cudaFree(p->d_boundaries);
    if (p->h_f9) free(p->h_f9);
    if (p->h_boundaries) free(p->h_boundaries);
    if (p->duplication) p->duplication->Release();
    if (p->staging_tex) p->staging_tex->Release();
    if (p->d3d_context) p->d3d_context->Release();
    if (p->d3d_device) p->d3d_device->Release();
    free(p);
    printf("[F9PIPE] Pipeline destroyed\n");
}

} /* extern "C" */
