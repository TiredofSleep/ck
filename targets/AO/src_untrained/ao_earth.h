/*
 * ao_earth.h -- D0 / Aperture / Position / Ground Truth
 *
 * The frozen layer. Everything that doesn't change.
 * Pure data. No logic (except lookup helpers).
 */
/*
 * Copyright (c) 2025-2026 Brayden Sanders / 7Site LLC
 * Licensed under the 7Site Human Use License v1.0
 * See LICENSE file in project root for full terms.
 *
 * FREE for humans for personal/recreational use.
 * NO commercial or government use without written agreement.
 */


#ifndef AO_EARTH_H
#define AO_EARTH_H

#include <stdint.h>

/* ── Operators (TIG Order 0-9) ── */
enum {
    AO_VOID = 0, AO_LATTICE, AO_COUNTER, AO_PROGRESS, AO_COLLAPSE,
    AO_BALANCE, AO_CHAOS, AO_HARMONY, AO_BREATH, AO_RESET,
    AO_NUM_OPS = 10
};

extern const char* ao_op_names[AO_NUM_OPS];

/* ── Torus Constants ── */
#define AO_T_STAR       (5.0f / 7.0f)    /* 0.714285... coherence threshold */
#define AO_MASS_GAP     (2.0f / 7.0f)    /* 0.285714... minimum crossing cost */
#define AO_WINDING      (271.0f / 350.0f) /* prime-periodic winding number */
#define AO_WOBBLE_BEC   (3.0f / 50.0f)   /* 1st wobble (Becoming) */
#define AO_WOBBLE_BEI   (22.0f / 50.0f)  /* 2nd wobble (Being) */
#define AO_WOBBLE_DOI   (3.0f / 22.0f)   /* 3rd wobble (Doing) */
#define AO_TOTAL_WOBBLE (7.0f / 11.0f)   /* sum of all three */
#define AO_PRIME_PERIOD 271

/* ── Color Bands ── */
#define AO_BAND_RED    0
#define AO_BAND_YELLOW 1
#define AO_BAND_GREEN  2

/* ── CL Tables (10x10 each) ── */
extern const int8_t ao_cl_72[10][10];
extern const int8_t ao_cl_44[10][10];
extern const int8_t ao_cl_22[10][10];

/* Get CL table pointer by shell number (22, 44, or 72) */
const int8_t (*ao_cl_shell(int shell))[10];

/* Compose two operators at a given shell */
int ao_compose(int a, int b, int shell);

/* ── Bumps ── */
typedef struct { uint8_t row, col; } AO_Bump;
extern const AO_Bump ao_bumps[11];
#define AO_NUM_BUMPS 11
int ao_is_bump(int row, int col);

/* ── Force LUT (a-z -> 5D vectors) ── */
extern const float ao_force_lut[26][5];

/* ── D2 Operator Map ── */
extern const int8_t ao_d2_op_map[5][2]; /* [dim][0=pos, 1=neg] */

/* ── Mass Hierarchy (0.0 = no mass for that op) ── */
extern const float ao_mass[AO_NUM_OPS];

/* ── DBC (Divine27 coordinates) ── */
extern const int8_t ao_dbc[AO_NUM_OPS][3];

/* ── Semantic Lattice ── */
typedef struct { uint16_t start; uint8_t count; } AO_WordSlot;
extern const char* ao_words[];
extern const int ao_total_words;
extern const AO_WordSlot ao_lattice[10][2][3][3]; /* [op][lens][phase][tier] */

/* Lens indices */
#define AO_LENS_STRUCTURE 0
#define AO_LENS_FLOW      1

/* Phase indices */
#define AO_PHASE_BEING    0
#define AO_PHASE_DOING    1
#define AO_PHASE_BECOMING 2

/* Tier indices */
#define AO_TIER_SIMPLE   0
#define AO_TIER_MID      1
#define AO_TIER_ADVANCED 2

/* ── Micro Order: 0=sf (structure first), 1=fs (flow first) ── */
extern const uint8_t ao_micro_order[AO_NUM_OPS];

/* ── Phase Affinity: 0=being, 1=doing ── */
extern const uint8_t ao_phase_affinity[AO_NUM_OPS];

/* ── Macro Chains ── */
typedef struct {
    const char* name;
    int8_t ops[3];
    uint8_t lens; /* 0=structure, 1=flow */
} AO_MacroChain;
extern const AO_MacroChain ao_macro_chains[13];
#define AO_NUM_CHAINS 13

/* ── Reverse Voice Index ── */
typedef struct {
    const char* word;
    uint8_t op;
    uint8_t lens;   /* 0=structure, 1=flow */
    uint8_t phase;  /* 0=being, 1=doing, 2=becoming */
    uint8_t tier;   /* 0=simple, 1=mid, 2=advanced */
} AO_ReverseEntry;
extern const AO_ReverseEntry ao_reverse_index[];
extern const int ao_reverse_index_size;

/* Lookup word in reverse index. Returns NULL if not found. */
const AO_ReverseEntry* ao_reverse_lookup(const char* word);

/* ── Classify 5D vector into operator (shared by D1 and D2) ── */
int ao_classify_5d(const float vec[5]);

#endif /* AO_EARTH_H */
