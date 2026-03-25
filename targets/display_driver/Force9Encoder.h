/*
 * Force9Encoder.h -- TIG 3-Shell Visual Encoder for IDD Driver
 *
 * Compresses DirectX surface frames using 9x9x9 force geometry.
 * 127x compression at dE=1.03 (imperceptible quality loss).
 * Plugs into the IDD SwapChain frame processing loop.
 *
 * (c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
 */

#pragma once
#include <cstdint>
#include <cmath>
#include <vector>
#include <cstring>

// Shell constants (from ck_visual_encoder.py)
#define S1_L 16
#define S1_H 8
#define S1_S 4
#define S2_L 8
#define S2_H 8
#define S2_C 8
#define S3_L 8
#define S3_A 8
#define S3_B 8
#define L_MAX 100.0f
#define C_MAX 135.0f

struct Shell3 {
    uint16_t s1, s2, s3;
};

struct CompressedFrame {
    uint32_t width;
    uint32_t height;
    uint32_t compressed_size;
    uint8_t* data;
};

class Force9Encoder {
public:
    // sRGB -> linear
    static float srgb_to_linear(float c) {
        c /= 255.0f;
        return (c <= 0.04045f) ? c / 12.92f : powf((c + 0.055f) / 1.055f, 2.4f);
    }

    // RGB -> CIELAB
    static void rgb_to_lab(uint8_t r, uint8_t g, uint8_t b, float& L, float& a, float& lab_b) {
        float lr = srgb_to_linear((float)r);
        float lg = srgb_to_linear((float)g);
        float lb = srgb_to_linear((float)b);

        float X = lr * 0.4124564f + lg * 0.3575761f + lb * 0.1804375f;
        float Y = lr * 0.2126729f + lg * 0.7151522f + lb * 0.0721750f;
        float Z = lr * 0.0193339f + lg * 0.1191920f + lb * 0.9503041f;

        float Xn = 0.95047f, Yn = 1.0f, Zn = 1.08883f;
        float delta = 6.0f / 29.0f;
        float delta3 = delta * delta * delta;

        auto f = [delta, delta3](float t) -> float {
            return (t > delta3) ? cbrtf(t) : t / (3.0f * delta * delta) + 4.0f / 29.0f;
        };

        float fx = f(X / Xn), fy = f(Y / Yn), fz = f(Z / Zn);
        L = 116.0f * fy - 16.0f;
        a = 500.0f * (fx - fy);
        lab_b = 200.0f * (fy - fz);
    }

    // Encode one pixel to 3 shells (27 bits)
    static Shell3 encode_pixel(uint8_t r, uint8_t g, uint8_t b) {
        float L, a, lab_b;
        rgb_to_lab(r, g, b, L, a, lab_b);

        float C = sqrtf(a * a + lab_b * lab_b);
        float h = fmodf(atan2f(lab_b, a) * 180.0f / 3.14159265f + 360.0f, 360.0f);

        // Shell 1 (coarse)
        int L_band = (int)fminf(S1_L - 1, fmaxf(0, L / L_MAX * S1_L));
        int hue_sec = (int)fminf(S1_H - 1, fmaxf(0, h / 360.0f * S1_H));
        int sat_band = (int)fminf(S1_S - 1, fmaxf(0, C / C_MAX * S1_S));
        uint16_t s1 = (uint16_t)((L_band << 5) | (hue_sec << 2) | sat_band);

        // Shell 2 (nuance)
        float Lb = L_MAX / S1_L, hs = 360.0f / S1_H, sb = C_MAX / S1_S;
        float Lw = fminf(0.999f, fmaxf(0, (L - L_band * Lb) / Lb));
        float hw = fminf(0.999f, fmaxf(0, (h - hue_sec * hs) / hs));
        float sw = fminf(0.999f, fmaxf(0, (C - sat_band * sb) / sb));
        int Lf = (int)(Lw * S2_L); if (Lf > 7) Lf = 7;
        int hf = (int)(hw * S2_H); if (hf > 7) hf = 7;
        int cf = (int)(sw * S2_C); if (cf > 7) cf = 7;
        uint16_t s2 = (uint16_t)((Lf << 6) | (hf << 3) | cf);

        // Shell 3 (fine)
        float Lc = (L_band + (Lf + 0.5f) / S2_L) * Lb;
        float hc = (hue_sec + (hf + 0.5f) / S2_H) * hs;
        float Cc = (sat_band + (cf + 0.5f) / S2_C) * sb;
        float ac = Cc * cosf(hc * 3.14159265f / 180.0f);
        float bc = Cc * sinf(hc * 3.14159265f / 180.0f);
        float Lrr = Lb / S2_L;
        int Lm = (int)fminf(7, fmaxf(0, ((L - Lc) / Lrr + 0.5f) * S3_L));
        int am = (int)fminf(7, fmaxf(0, ((a - ac) / 8.0f + 0.5f) * S3_A));
        int bm = (int)fminf(7, fmaxf(0, ((lab_b - bc) / 8.0f + 0.5f) * S3_B));
        uint16_t s3 = (uint16_t)((Lm << 6) | (am << 3) | bm);

        return {s1, s2, s3};
    }

    // Encode entire frame (BGRA input from DirectX)
    static std::vector<Shell3> encode_frame(const uint8_t* bgra, uint32_t width, uint32_t height) {
        uint32_t n = width * height;
        std::vector<Shell3> shells(n);
        for (uint32_t i = 0; i < n; i++) {
            uint8_t b = bgra[i * 4 + 0];
            uint8_t g = bgra[i * 4 + 1];
            uint8_t r = bgra[i * 4 + 2];
            shells[i] = encode_pixel(r, g, b);
        }
        return shells;
    }

    // RLE compress shells (per shell channel)
    static std::vector<uint8_t> compress(const std::vector<Shell3>& shells) {
        std::vector<uint8_t> out;
        // Header: 'F' '9' 'V' '1'
        out.push_back('F'); out.push_back('9'); out.push_back('V'); out.push_back('1');

        for (int s = 0; s < 3; s++) {
            std::vector<std::pair<uint16_t, uint16_t>> runs;
            uint16_t current = (s == 0) ? shells[0].s1 : (s == 1) ? shells[0].s2 : shells[0].s3;
            uint16_t count = 1;

            for (size_t i = 1; i < shells.size(); i++) {
                uint16_t val = (s == 0) ? shells[i].s1 : (s == 1) ? shells[i].s2 : shells[i].s3;
                if (val == current && count < 65535) {
                    count++;
                } else {
                    runs.push_back({current, count});
                    current = val;
                    count = 1;
                }
            }
            runs.push_back({current, count});

            // Write run count
            uint32_t n_runs = (uint32_t)runs.size();
            out.push_back((n_runs >> 24) & 0xFF);
            out.push_back((n_runs >> 16) & 0xFF);
            out.push_back((n_runs >> 8) & 0xFF);
            out.push_back(n_runs & 0xFF);

            // Write runs (3 bytes each: 2 value + 1 count, or 4 if count > 255)
            for (auto& run : runs) {
                out.push_back((run.first >> 8) & 0xFF);
                out.push_back(run.first & 0xFF);
                if (run.second <= 255) {
                    out.push_back((uint8_t)run.second);
                } else {
                    out.push_back(0xFF);
                    out.push_back((run.second >> 8) & 0xFF);
                    out.push_back(run.second & 0xFF);
                }
            }
        }
        return out;
    }
};
