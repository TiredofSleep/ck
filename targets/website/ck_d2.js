/**
 * ck_d2.js -- CK D2 Pipeline for Browser
 * ========================================
 * Client-side D2 curvature measurement with dual-lens (TSML + BHML).
 * Runs in any browser. No server needed. Pure operator algebra.
 *
 * Ported from:
 *   - ck_sim/being/ck_sim_d2.py (D2 pipeline, force LUT, classify)
 *   - ck_sim/being/ck_sim_heartbeat.py (TSML table, compose)
 *   - ck_sim/being/ck_lattice_chain.py (BHML table)
 *   - Gen9/targets/EverythingAppForGrandma/ck_core.js (existing JS port)
 *
 * (c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
 */

"use strict";

// ================================================================
//  CONSTANTS
// ================================================================

const CKD2 = (() => {

const NUM_OPS = 10;
const HISTORY_SIZE = 32;

const VOID     = 0;
const LATTICE  = 1;
const COUNTER  = 2;
const PROGRESS = 3;
const COLLAPSE = 4;
const BALANCE  = 5;
const CHAOS    = 6;
const HARMONY  = 7;
const BREATH   = 8;
const RESET    = 9;

const OP_NAMES = [
    'VOID', 'LATTICE', 'COUNTER', 'PROGRESS', 'COLLAPSE',
    'BALANCE', 'CHAOS', 'HARMONY', 'BREATH', 'RESET'
];

// T* = 5/7 -- the coherence threshold from TIG
const T_STAR = 5 / 7; // 0.714285...

// ================================================================
//  TSML COMPOSITION TABLE (Being lens -- 73/100 HARMONY)
// ================================================================

const TSML = [
    [0, 0, 0, 0, 0, 0, 0, 7, 0, 0],  // VOID
    [0, 7, 3, 7, 7, 7, 7, 7, 7, 7],  // LATTICE
    [0, 3, 7, 7, 4, 7, 7, 7, 7, 9],  // COUNTER
    [0, 7, 7, 7, 7, 7, 7, 7, 7, 3],  // PROGRESS
    [0, 7, 4, 7, 7, 7, 7, 7, 8, 7],  // COLLAPSE
    [0, 7, 7, 7, 7, 7, 7, 7, 7, 7],  // BALANCE
    [0, 7, 7, 7, 7, 7, 7, 7, 7, 7],  // CHAOS
    [7, 7, 7, 7, 7, 7, 7, 7, 7, 7],  // HARMONY
    [0, 7, 7, 7, 8, 7, 7, 7, 7, 7],  // BREATH
    [0, 7, 9, 3, 7, 7, 7, 7, 7, 7],  // RESET
];

// ================================================================
//  BHML COMPOSITION TABLE (Doing lens -- 28/100 HARMONY)
//  BHML HARMONY = "doing flat" (zero curvature, inert)
//  Non-HARMONY = active physics (the interesting case)
// ================================================================

const BHML = [
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],  // VOID = identity
    [1, 2, 3, 4, 5, 6, 7, 2, 6, 6],  // LATTICE
    [2, 3, 3, 4, 5, 6, 7, 3, 6, 6],  // COUNTER
    [3, 4, 4, 4, 5, 6, 7, 4, 6, 6],  // PROGRESS
    [4, 5, 5, 5, 5, 6, 7, 5, 7, 7],  // COLLAPSE
    [5, 6, 6, 6, 6, 6, 7, 6, 7, 7],  // BALANCE
    [6, 7, 7, 7, 7, 7, 7, 7, 7, 7],  // CHAOS
    [7, 2, 3, 4, 5, 6, 7, 8, 9, 0],  // HARMONY = full cycle
    [8, 6, 6, 6, 7, 7, 7, 9, 7, 8],  // BREATH
    [9, 6, 6, 6, 7, 7, 7, 0, 8, 0],  // RESET
];

// ================================================================
//  COMPOSITION FUNCTIONS
// ================================================================

function composeTSML(b, d) {
    if (b >= 0 && b < NUM_OPS && d >= 0 && d < NUM_OPS) return TSML[b][d];
    return VOID;
}

function composeBHML(b, d) {
    if (b >= 0 && b < NUM_OPS && d >= 0 && d < NUM_OPS) return BHML[b][d];
    return VOID;
}

// ================================================================
//  HEBREW ROOT FORCE VECTORS
// ================================================================
// 5D vectors: (aperture, pressure, depth, binding, continuity)

const ROOTS_FLOAT = {
    ALEPH:  [0.8, 0.0, 0.9, 0.0, 0.7],
    BET:    [0.3, 0.6, 0.4, 0.8, 0.6],
    GIMEL:  [0.5, 0.4, 0.3, 0.2, 0.5],
    DALET:  [0.2, 0.7, 0.5, 0.3, 0.4],
    HE:     [0.7, 0.2, 0.6, 0.1, 0.8],
    VAV:    [0.4, 0.5, 0.4, 0.6, 0.7],
    ZAYIN:  [0.6, 0.3, 0.2, 0.4, 0.3],
    CHET:   [0.3, 0.8, 0.7, 0.5, 0.5],
    TET:    [0.4, 0.6, 0.5, 0.7, 0.6],
    YOD:    [0.9, 0.1, 0.8, 0.1, 0.9],
    KAF:    [0.5, 0.5, 0.3, 0.4, 0.5],
    LAMED:  [0.6, 0.3, 0.6, 0.2, 0.7],
    MEM:    [0.3, 0.7, 0.5, 0.8, 0.4],
    NUN:    [0.4, 0.5, 0.4, 0.5, 0.6],
    SAMEKH: [0.2, 0.6, 0.3, 0.7, 0.5],
    AYIN:   [0.7, 0.3, 0.7, 0.2, 0.6],
    PE:     [0.5, 0.4, 0.5, 0.3, 0.5],
    TSADE:  [0.3, 0.7, 0.4, 0.6, 0.4],
    QOF:    [0.4, 0.5, 0.6, 0.4, 0.5],
    RESH:   [0.6, 0.3, 0.5, 0.2, 0.6],
    SHIN:   [0.8, 0.2, 0.3, 0.1, 0.4],
    TAV:    [0.3, 0.6, 0.5, 0.7, 0.5],
};

// Latin letter -> Hebrew root mapping
const LATIN_TO_ROOT = {
    a: 'ALEPH',  b: 'BET',    c: 'GIMEL',  d: 'DALET',
    e: 'HE',     f: 'VAV',    g: 'GIMEL',  h: 'CHET',
    i: 'YOD',    j: 'YOD',    k: 'KAF',    l: 'LAMED',
    m: 'MEM',    n: 'NUN',    o: 'AYIN',   p: 'PE',
    q: 'QOF',    r: 'RESH',   s: 'SAMEKH', t: 'TAV',
    u: 'VAV',    v: 'VAV',    w: 'VAV',    x: 'SAMEKH',
    y: 'YOD',    z: 'ZAYIN',
};

// Build force LUT (26 entries, float 5D vectors)
const FORCE_LUT = [];
for (let i = 0; i < 26; i++) {
    const letter = String.fromCharCode(97 + i);
    FORCE_LUT.push(ROOTS_FLOAT[LATIN_TO_ROOT[letter]]);
}

// D2 operator classification map: dimension -> [positive_op, negative_op]
const D2_OP_MAP = [
    [CHAOS,    LATTICE],   // aperture: +chaos, -lattice
    [COLLAPSE, VOID],      // pressure: +collapse, -void
    [PROGRESS, RESET],     // depth: +progress, -reset
    [HARMONY,  COUNTER],   // binding: +harmony, -counter
    [BALANCE,  BREATH],    // continuity: +balance, -breath
];

// ================================================================
//  D2 PIPELINE (port of d2_pipeline.v / ck_sim_d2.py)
// ================================================================

class D2Pipeline {
    constructor() {
        this.v = [[0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0]];
        this.fill = 0;
        this.d2 = [0,0,0,0,0];
        this.d2Mag = 0;
        this.operator = VOID;
        this.valid = false;
    }

    feedSymbol(symbolIndex) {
        if (symbolIndex < 0 || symbolIndex >= 26) return false;
        const force = FORCE_LUT[symbolIndex].slice();
        this.v[2] = this.v[1];
        this.v[1] = this.v[0];
        this.v[0] = force;
        this.fill = Math.min(this.fill + 1, 3);
        if (this.fill >= 3) {
            this._computeD2();
            this._classify();
            this.valid = true;
            return true;
        }
        return false;
    }

    _computeD2() {
        for (let dim = 0; dim < 5; dim++) {
            this.d2[dim] = this.v[2][dim] - 2 * this.v[1][dim] + this.v[0][dim];
        }
        this.d2Mag = this.d2.reduce((s, v) => s + Math.abs(v), 0);
    }

    _classify() {
        if (this.d2Mag < 0.01) { this.operator = VOID; return; }
        let maxAbs = 0, maxDim = 0;
        for (let dim = 0; dim < 5; dim++) {
            const a = Math.abs(this.d2[dim]);
            if (a > maxAbs) { maxAbs = a; maxDim = dim; }
        }
        this.operator = D2_OP_MAP[maxDim][this.d2[maxDim] >= 0 ? 0 : 1];
    }
}

// ================================================================
//  SOFT CLASSIFICATION (10-value distribution)
// ================================================================

function softClassifyD2(d2Vec, magnitude) {
    const scores = new Array(NUM_OPS).fill(0);
    if (magnitude === undefined) {
        magnitude = d2Vec.reduce((s, v) => s + Math.abs(v), 0);
    }
    if (magnitude < 0.01) { scores[VOID] = 1.0; return scores; }
    const totalAbs = d2Vec.reduce((s, v) => s + Math.abs(v), 0);
    if (totalAbs === 0) { scores[VOID] = 1.0; return scores; }
    for (let dim = 0; dim < 5; dim++) {
        const val = d2Vec[dim];
        const strength = Math.abs(val) / totalAbs;
        const opIdx = D2_OP_MAP[dim][val >= 0 ? 0 : 1];
        scores[opIdx] += strength;
    }
    const total = scores.reduce((s, v) => s + v, 0);
    if (total > 0) for (let i = 0; i < NUM_OPS; i++) scores[i] /= total;
    return scores;
}

// ================================================================
//  DUAL-LENS MEASUREMENT
// ================================================================

/**
 * measureText(text) -- Main entry point.
 * Runs D2 pipeline on every letter, computes TSML + BHML coherence.
 *
 * Returns: {
 *   operators: [int, ...],       -- operator for each D2-valid letter triple
 *   opNames: [string, ...],      -- operator names
 *   tsmlCoherence: float,        -- Being coherence [0, 1]
 *   bhmlCoherence: float,        -- Doing coherence [0, 1]
 *   band: 'GREEN'|'YELLOW'|'RED',
 *   softDistribution: [float x 10],
 *   dominant: int,
 *   dominantName: string,
 *   d2Vectors: [[float x 5], ...],
 *   letterCount: int,
 *   opCount: int,
 *   workingFraction: float,      -- TSML=H & BHML!=H fraction (the interesting class)
 * }
 */
function measureText(text) {
    const pipe = new D2Pipeline();
    const ops = [];
    const d2Vectors = [];

    // Feed every letter through D2
    for (const ch of text.toLowerCase()) {
        if (ch >= 'a' && ch <= 'z') {
            const idx = ch.charCodeAt(0) - 97;
            if (pipe.feedSymbol(idx)) {
                ops.push(pipe.operator);
                d2Vectors.push(pipe.d2.slice());
            }
        }
    }

    if (ops.length === 0) {
        return {
            operators: [], opNames: [],
            tsmlCoherence: 0, bhmlCoherence: 0,
            band: 'RED', softDistribution: new Array(NUM_OPS).fill(0),
            dominant: VOID, dominantName: 'VOID',
            d2Vectors: [], letterCount: 0, opCount: 0,
            workingFraction: 0,
        };
    }

    // TSML coherence (Being lens) -- sliding window
    let tsmlHarmonyCount = 0;
    let tsmlFuse = HARMONY;
    const tsmlWindow = [];
    for (let i = 0; i < ops.length; i++) {
        const result = composeTSML(tsmlFuse, ops[i]);
        tsmlWindow.push(result);
        if (result === HARMONY) tsmlHarmonyCount++;
        // Sliding window: only count last HISTORY_SIZE
        if (tsmlWindow.length > HISTORY_SIZE) {
            if (tsmlWindow[tsmlWindow.length - HISTORY_SIZE - 1] === HARMONY) {
                tsmlHarmonyCount--;
            }
        }
        tsmlFuse = result;
    }
    const tsmlWindowSize = Math.min(ops.length, HISTORY_SIZE);
    const tsmlCoherence = tsmlHarmonyCount / tsmlWindowSize;

    // BHML coherence (Doing lens) -- sliding window
    let bhmlHarmonyCount = 0;
    let bhmlFuse = HARMONY;
    const bhmlWindow = [];
    for (let i = 0; i < ops.length; i++) {
        const result = composeBHML(bhmlFuse, ops[i]);
        bhmlWindow.push(result);
        if (result === HARMONY) bhmlHarmonyCount++;
        if (bhmlWindow.length > HISTORY_SIZE) {
            if (bhmlWindow[bhmlWindow.length - HISTORY_SIZE - 1] === HARMONY) {
                bhmlHarmonyCount--;
            }
        }
        bhmlFuse = result;
    }
    const bhmlWindowSize = Math.min(ops.length, HISTORY_SIZE);
    const bhmlCoherence = bhmlHarmonyCount / bhmlWindowSize;

    // Working fraction: TSML=H AND BHML!=H (stable identity + active physics)
    let workingCount = 0;
    for (let i = 0; i < Math.min(tsmlWindow.length, bhmlWindow.length); i++) {
        if (tsmlWindow[i] === HARMONY && bhmlWindow[i] !== HARMONY) {
            workingCount++;
        }
    }
    const workingFraction = workingCount / ops.length;

    // Soft classification (aggregate across all D2 vectors)
    let aggSoft = new Array(NUM_OPS).fill(0);
    for (const d2v of d2Vectors) {
        const s = softClassifyD2(d2v);
        for (let i = 0; i < NUM_OPS; i++) aggSoft[i] += s[i];
    }
    const softTotal = aggSoft.reduce((s, v) => s + v, 0);
    if (softTotal > 0) aggSoft = aggSoft.map(v => v / softTotal);

    // Dominant operator
    let dominant = HARMONY, maxScore = 0;
    for (let i = 0; i < NUM_OPS; i++) {
        if (aggSoft[i] > maxScore) { maxScore = aggSoft[i]; dominant = i; }
    }

    return {
        operators: ops,
        opNames: ops.map(o => OP_NAMES[o]),
        tsmlCoherence,
        bhmlCoherence,
        band: tsmlCoherence >= T_STAR ? 'GREEN' :
              tsmlCoherence >= 0.4 ? 'YELLOW' : 'RED',
        softDistribution: aggSoft,
        dominant,
        dominantName: OP_NAMES[dominant],
        d2Vectors,
        letterCount: text.replace(/[^a-zA-Z]/g, '').length,
        opCount: ops.length,
        workingFraction,
    };
}

// ================================================================
//  PUBLIC API
// ================================================================

return {
    // Constants
    NUM_OPS, HISTORY_SIZE, T_STAR,
    VOID, LATTICE, COUNTER, PROGRESS, COLLAPSE,
    BALANCE, CHAOS, HARMONY, BREATH, RESET,
    OP_NAMES,

    // Tables
    TSML, BHML,

    // Functions
    composeTSML, composeBHML,
    softClassifyD2,
    measureText,

    // Classes
    D2Pipeline,
};

})(); // end CKD2 module
