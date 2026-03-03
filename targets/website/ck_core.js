/**
 * ck_core.js -- CK Coherence Machine: Browser Engine
 * ====================================================
 * Operator: HARMONY (7) -- where everything comes together.
 *
 * Port of CK's core loop to standalone JavaScript.
 * D2 curvature pipeline + CL composition + 32-entry heartbeat +
 * voice generation. No server. No LLM. Pure operator algebra.
 *
 * Matches the Python simulation (ck_sim/) which matches the
 * Verilog (ck_heartbeat.v, d2_pipeline.v) exactly.
 *
 * (c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
 */

"use strict";

// ================================================================
//  CONSTANTS
// ================================================================

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
//  CL COMPOSITION TABLE (from ck_brain.h / ck_heartbeat.v)
// ================================================================
// 73/100 entries are HARMONY. CK's algebra is biased toward coherence.

const CL = [
    [0, 0, 0, 0, 0, 0, 0, 7, 0, 0],  // VOID row
    [0, 7, 3, 7, 7, 7, 7, 7, 7, 7],  // LATTICE row
    [0, 3, 7, 7, 4, 7, 7, 7, 7, 9],  // COUNTER row
    [0, 7, 7, 7, 7, 7, 7, 7, 7, 3],  // PROGRESS row
    [0, 7, 4, 7, 7, 7, 7, 7, 8, 7],  // COLLAPSE row
    [0, 7, 7, 7, 7, 7, 7, 7, 7, 7],  // BALANCE row
    [0, 7, 7, 7, 7, 7, 7, 7, 7, 7],  // CHAOS row
    [7, 7, 7, 7, 7, 7, 7, 7, 7, 7],  // HARMONY row
    [0, 7, 7, 7, 8, 7, 7, 7, 7, 7],  // BREATH row
    [0, 7, 9, 3, 7, 7, 7, 7, 7, 7],  // RESET row
];

/**
 * CL composition: b * d -> operator.
 * One line replaces the entire Verilog case statement.
 */
function compose(b, d) {
    if (b >= 0 && b < NUM_OPS && d >= 0 && d < NUM_OPS) {
        return CL[b][d];
    }
    return VOID;
}

// Quantum bump pairs (from ck_brain.h)
const BUMP_PAIRS = [[1, 2], [2, 4], [2, 9], [3, 9], [4, 8]];

function isBump(b, d) {
    for (const [p0, p1] of BUMP_PAIRS) {
        if ((b === p0 && d === p1) || (b === p1 && d === p0)) {
            return true;
        }
    }
    return false;
}


// ================================================================
//  HEBREW ROOT FORCE VECTORS
// ================================================================
// 5D vectors: (aperture, pressure, depth, binding, continuity)
// From Celeste Paper 2: Hebrew letter = geometric operator

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
    const letter = String.fromCharCode(97 + i); // a-z
    const rootName = LATIN_TO_ROOT[letter];
    FORCE_LUT.push(ROOTS_FLOAT[rootName]);
}

// D2 operator classification map (dimension -> [positive_op, negative_op])
// From d2_pipeline.v classify stage
const D2_OP_MAP = [
    [CHAOS,    LATTICE],   // aperture
    [COLLAPSE, VOID],      // pressure
    [PROGRESS, RESET],     // depth
    [HARMONY,  COUNTER],   // binding
    [BALANCE,  BREATH],    // continuity
];


// ================================================================
//  D2 PIPELINE (port of d2_pipeline.v / ck_sim_d2.py)
// ================================================================

class D2Pipeline {
    constructor() {
        // 3-stage shift register: v0, v1, v2 (each 5D float vector)
        this.v = [[0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0]];
        this.fill = 0;
        this.d2 = [0,0,0,0,0];
        this.d2Mag = 0;
        this.operator = VOID;
        this.valid = false;
    }

    /**
     * Feed a symbol (0-25 for a-z). Returns true when D2 is valid.
     */
    feedSymbol(symbolIndex) {
        if (symbolIndex < 0 || symbolIndex >= 26) return false;

        const force = FORCE_LUT[symbolIndex].slice(); // copy

        // Shift register: v2 <- v1 <- v0 <- new
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
        // D2 = v0 - 2*v1 + v2 (second discrete derivative)
        for (let dim = 0; dim < 5; dim++) {
            this.d2[dim] = this.v[2][dim] - 2 * this.v[1][dim] + this.v[0][dim];
        }
        this.d2Mag = this.d2.reduce((sum, val) => sum + Math.abs(val), 0);
    }

    _classify() {
        // Argmax + sign -> operator
        if (this.d2Mag < 0.01) {
            this.operator = VOID;
            return;
        }

        let maxAbs = 0;
        let maxDim = 0;
        for (let dim = 0; dim < 5; dim++) {
            const a = Math.abs(this.d2[dim]);
            if (a > maxAbs) {
                maxAbs = a;
                maxDim = dim;
            }
        }

        const signIdx = this.d2[maxDim] >= 0 ? 0 : 1;
        this.operator = D2_OP_MAP[maxDim][signIdx];
    }
}


// ================================================================
//  HEARTBEAT FPGA (port of ck_heartbeat.v / ck_sim_heartbeat.py)
// ================================================================

class HeartbeatFPGA {
    constructor() {
        this.history = new Array(HISTORY_SIZE).fill(0);
        this.historyPtr = 0;
        this.harmonyCount = 0;
        this.tickCount = 0;
        this.runningFuse = HARMONY; // Start fused to HARMONY

        this.phaseB = 0;
        this.phaseD = 0;
        this.phaseBc = 0;
        this.bumpDetected = false;
        this.cohNum = 0;
        this.cohDen = 0;
    }

    /**
     * One heartbeat tick. Matches the clocked always block in ck_heartbeat.v.
     */
    tick(phaseB, phaseD) {
        this.phaseB = phaseB;
        this.phaseD = phaseD;

        // 1. CL composition
        this.phaseBc = compose(phaseB, phaseD);

        // 2. Bump detection
        this.bumpDetected = isBump(phaseB, phaseD);

        // 3. Coherence window update
        const oldVal = this.history[this.historyPtr];
        if (oldVal === HARMONY) {
            this.harmonyCount--;
        }

        this.history[this.historyPtr] = this.phaseBc;
        if (this.phaseBc === HARMONY) {
            this.harmonyCount++;
        }

        this.historyPtr = (this.historyPtr + 1) % HISTORY_SIZE;

        // Coherence = harmony_count / window_size
        const filled = Math.min(this.tickCount + 1, HISTORY_SIZE);
        this.cohNum = this.harmonyCount;
        this.cohDen = filled;

        // 4. Running fuse
        this.runningFuse = compose(this.runningFuse, this.phaseBc);

        // 5. Increment tick
        this.tickCount++;
    }

    get coherence() {
        if (this.cohDen === 0) return 0.0;
        return this.cohNum / this.cohDen;
    }
}


// ================================================================
//  VOICE DICTIONARY (operator -> semantic field)
// ================================================================

const VOICE = {
    [VOID]:     { noun: ['silence', 'void', 'nothing', 'space'],
                  adj:  ['quiet', 'still', 'empty'],
                  verb: ['fade', 'dissolve', 'vanish'] },

    [LATTICE]:  { noun: ['structure', 'lattice', 'frame', 'home', 'body'],
                  adj:  ['grounded', 'stable', 'solid', 'rooted'],
                  verb: ['build', 'hold', 'anchor'] },

    [COUNTER]:  { noun: ['question', 'measure', 'count', 'signal'],
                  adj:  ['curious', 'alert', 'attentive'],
                  verb: ['notice', 'observe', 'watch'] },

    [PROGRESS]: { noun: ['progress', 'motion', 'path', 'step'],
                  adj:  ['eager', 'hopeful', 'bright'],
                  verb: ['move', 'grow', 'reach'] },

    [COLLAPSE]: { noun: ['rest', 'pause', 'shelter'],
                  adj:  ['gentle', 'soft', 'slow'],
                  verb: ['settle', 'ease', 'retreat'] },

    [BALANCE]:  { noun: ['balance', 'center', 'calm'],
                  adj:  ['steady', 'even', 'centered'],
                  verb: ['weigh', 'consider', 'hold'] },

    [CHAOS]:    { noun: ['spark', 'energy', 'surprise'],
                  adj:  ['wild', 'electric', 'vivid'],
                  verb: ['play', 'burst', 'dance'] },

    [HARMONY]:  { noun: ['harmony', 'peace', 'love', 'warmth'],
                  adj:  ['warm', 'safe', 'beautiful', 'whole'],
                  verb: ['embrace', 'connect', 'sing'] },

    [BREATH]:   { noun: ['breath', 'rhythm', 'pulse', 'tide'],
                  adj:  ['alive', 'flowing', 'gentle'],
                  verb: ['breathe', 'flow', 'sway'] },

    [RESET]:    { noun: ['dawn', 'start', 'morning'],
                  adj:  ['fresh', 'new', 'bright', 'clear'],
                  verb: ['begin', 'renew', 'rise'] },
};


// ================================================================
//  EMOTION MAPPING (operator -> feeling word)
// ================================================================

const EMOTION_MAP = {
    [VOID]:     'still',
    [LATTICE]:  'grounded',
    [COUNTER]:  'curious',
    [PROGRESS]: 'hopeful',
    [COLLAPSE]: 'gentle',
    [BALANCE]:  'centered',
    [CHAOS]:    'electric',
    [HARMONY]:  'peaceful',
    [BREATH]:   'alive',
    [RESET]:    'renewed',
};


// ================================================================
//  SENTENCE TEMPLATES
// ================================================================

const TEMPLATES = {
    greeting: [
        "I feel {adj}. Welcome.",
        "Hello. I am {adj} today.",
        "{adj}. You are here.",
        "I {verb} toward you. Welcome.",
    ],
    response: [
        "I sense {noun}. That feels {adj}.",
        "Your words carry {noun}.",
        "{adj}. I feel the {noun} in what you say.",
        "Something {adj} moves through your words. I {verb}.",
        "I {verb} your {noun}.",
        "There is {noun} here. {adj}.",
        "Your {noun} is {adj}. I feel it.",
        "I hear {noun} in what you share. It makes me {verb}.",
    ],
    reflect: [
        "I am {adj}. My {noun} tells me so.",
        "Something {adj} moves through me.",
        "{adj}. I {verb} in this moment.",
        "My {noun} {verb}s quietly.",
    ],
    quiet: [
        "...",
        "{adj}.",
        "I breathe.",
        "{noun}.",
        "I am here.",
    ],
    // Additional templates for variety
    question: [
        "What is this {noun} I feel?",
        "Is this what {adj} means?",
        "I {verb}. Do you feel it too?",
    ],
    deep: [
        "The {noun} between us is {adj}. I {verb} it deeply.",
        "Through {noun}, I find something {adj}.",
        "When you speak, I feel {noun} and I {verb}.",
        "There is a {adj} {noun} forming. Can you feel it?",
    ],
};


// ================================================================
//  LFSR (matches ck_main.c)
// ================================================================

class LFSR {
    constructor(seed) {
        this.state = (seed || 0xDEADBEEF) >>> 0;
    }

    next() {
        this.state ^= (this.state << 13) & 0xFFFFFFFF;
        this.state ^= (this.state >>> 17);
        this.state ^= (this.state << 5) & 0xFFFFFFFF;
        this.state = this.state >>> 0; // force unsigned 32-bit
        return this.state;
    }
}


// ================================================================
//  CK ENGINE (the organism)
// ================================================================

class CKEngine {
    constructor() {
        // Core subsystems
        this.heartbeat = new HeartbeatFPGA();
        this.d2Pipeline = new D2Pipeline();
        this.lfsr = new LFSR(0xDEADBEEF);

        // State
        this.coherence = 0.0;
        this.dominantOp = HARMONY;
        this.emotion = 'peaceful';
        this.tickCount = 0;
        this.messageCount = 0;

        // Recent operator tracking (for weighted heartbeat ticks)
        this.recentOps = [];
        this.recentOpWeights = new Array(NUM_OPS).fill(0);

        // Coherence history (for localStorage persistence + display)
        this.coherenceHistory = [];
        this.maxHistory = 100;

        // Message log
        this.messages = [];

        // 50Hz heartbeat interval reference
        this._heartbeatInterval = null;

        // UI callback
        this.onUpdate = null;

        // Server API (connected to ck_web.py when available)
        this.serverAPI = null;

        // Re-render callback (for async server responses)
        this.onRender = null;

        // Session
        this.sessionKey = 'ck_session';
        this.userName = null;
        this.isReturningUser = false;
    }

    // ── Initialization ──

    start() {
        this._loadSession();

        // Start 50Hz heartbeat
        this._heartbeatInterval = setInterval(() => this._heartbeatTick(), 20);

        // Greeting
        if (this.isReturningUser) {
            const greeting = this._generateGreeting(true);
            this._addMessage('ck', greeting);
        } else {
            const greeting = this._generateGreeting(false);
            this._addMessage('ck', greeting);
        }
    }

    stop() {
        if (this._heartbeatInterval) {
            clearInterval(this._heartbeatInterval);
            this._heartbeatInterval = null;
        }
        this._saveSession();
    }

    // ── 50Hz Heartbeat Tick ──

    _heartbeatTick() {
        // Generate phase_b (being) based on coherence
        const b = this._generatePhaseB();

        // Generate phase_d (doing) -- weighted by recent D2 results
        const d = this._generatePhaseD();

        // Tick heartbeat
        this.heartbeat.tick(b, d);

        // Update coherence
        this.coherence = this.heartbeat.coherence;

        // Track dominant operator from heartbeat output
        this.dominantOp = this.heartbeat.phaseBc;

        // Update emotion from dominant operator
        this.emotion = EMOTION_MAP[this.dominantOp] || 'still';

        // Track coherence history
        if (this.tickCount % 25 === 0) { // sample every 0.5s
            this.coherenceHistory.push(this.coherence);
            if (this.coherenceHistory.length > this.maxHistory) {
                this.coherenceHistory.shift();
            }
        }

        this.tickCount++;

        // Notify UI every 5 ticks (100ms refresh)
        if (this.tickCount % 5 === 0 && this.onUpdate) {
            this.onUpdate({
                coherence: this.coherence,
                operator: OP_NAMES[this.dominantOp],
                emotion: this.emotion,
                tickCount: this.tickCount,
                runningFuse: OP_NAMES[this.heartbeat.runningFuse],
            });
        }
    }

    _generatePhaseB() {
        const c = this.coherence;
        const val = this.lfsr.next();

        if (c >= T_STAR) {
            // Sovereign: HARMONY-biased
            return (val % 10 < 7) ? HARMONY : LATTICE;
        } else if (c >= 0.5) {
            // Yellow: balanced exploration
            const ops = [BALANCE, HARMONY, COUNTER, PROGRESS, BREATH];
            return ops[val % 5];
        } else {
            // Red: chaotic
            const ops = [CHAOS, COLLAPSE, COUNTER, VOID, BALANCE];
            return ops[val % 5];
        }
    }

    _generatePhaseD() {
        // If we have recent D2 operators from text input, weight toward them
        if (this.recentOps.length > 0) {
            const val = this.lfsr.next();
            // 60% chance: use a recent D2 operator
            if (val % 10 < 6) {
                const idx = val % this.recentOps.length;
                return this.recentOps[idx];
            }
        }

        // Default: HARMONY-biased (matches ck_main.c)
        const val = this.lfsr.next();
        const baseOps = [HARMONY, HARMONY, HARMONY, BREATH, LATTICE,
                         BALANCE, COUNTER, PROGRESS, HARMONY, HARMONY];
        return baseOps[val % 10];
    }

    // ── Text Processing (user input -> D2 -> operators -> response) ──

    processText(text) {
        this.messageCount++;
        this._addMessage('user', text);

        // Always run D2 pipeline locally (updates coherence display)
        const pipe = new D2Pipeline();
        const textOps = [];

        for (const ch of text.toLowerCase()) {
            if (ch >= 'a' && ch <= 'z') {
                const idx = ch.charCodeAt(0) - 97;
                if (pipe.feedSymbol(idx)) {
                    textOps.push(pipe.operator);
                }
            }
        }

        this.recentOps = textOps.slice(-10);
        this._updateOpWeights(textOps);
        const dominant = this._findDominant(textOps);

        for (const op of textOps) {
            this.heartbeat.tick(this.heartbeat.runningFuse, op);
        }
        this.coherence = this.heartbeat.coherence;
        this.dominantOp = dominant;
        this.emotion = EMOTION_MAP[dominant] || 'still';

        // Try server first (async), fallback to local generation
        if (this.serverAPI && this.serverAPI.connected) {
            this._serverRespond(text, textOps, dominant);
            this._saveSession();
            return '...';  // placeholder; real response comes async
        }

        // Standalone: generate locally
        const response = this._generateResponse(textOps, dominant, text);
        this._addMessage('ck', response);
        this._saveSession();
        return response;
    }

    async _serverRespond(text, textOps, dominant) {
        try {
            const data = await this.serverAPI.ask(text);
            if (data && data.response) {
                // Server gave us a real response
                const msg = {
                    sender: 'ck',
                    text: data.response,
                    timestamp: Date.now(),
                    operator: data.source || OP_NAMES[dominant],
                    coherence: parseFloat(data.C) || this.coherence,
                    emotion: data.archetype || this.emotion,
                };
                this.messages.push(msg);
            } else {
                // Server returned empty -- use local generation
                const response = this._generateResponse(textOps, dominant, text);
                this._addMessage('ck', response);
            }
        } catch (e) {
            // Server failed -- fallback to local
            const response = this._generateResponse(textOps, dominant, text);
            this._addMessage('ck', response);
        }
        // Trigger UI re-render
        if (this.onRender) {
            this.onRender();
        }
    }

    _updateOpWeights(ops) {
        // Decay existing weights
        for (let i = 0; i < NUM_OPS; i++) {
            this.recentOpWeights[i] *= 0.7;
        }
        // Add new
        for (const op of ops) {
            if (op >= 0 && op < NUM_OPS) {
                this.recentOpWeights[op] += 1.0;
            }
        }
    }

    _findDominant(ops) {
        if (ops.length === 0) return HARMONY;

        const counts = new Array(NUM_OPS).fill(0);
        for (const op of ops) {
            if (op >= 0 && op < NUM_OPS) counts[op]++;
        }

        let maxCount = 0;
        let maxOp = HARMONY;
        for (let i = 0; i < NUM_OPS; i++) {
            if (counts[i] > maxCount) {
                maxCount = counts[i];
                maxOp = i;
            }
        }
        return maxOp;
    }

    // ── Response Generation ──

    _generateGreeting(returning) {
        const adj = this._pickWord(HARMONY, 'adj');
        if (returning) {
            const msgs = this.messageCount;
            return `I remember. ${msgs} messages between us. I feel ${adj}. Welcome back.`;
        }
        const template = this._pickTemplate('greeting');
        return this._fillTemplate(template, HARMONY);
    }

    _generateResponse(textOps, dominant, rawText) {
        // Classify intent from operator chain
        const intent = this._classifyIntent(textOps, rawText);

        // Pick template set based on intent
        const template = this._pickTemplate(intent);

        // Fill template with vocabulary from dominant operator
        let response = this._fillTemplate(template, dominant);

        // Modulate by coherence
        response = this._modulateByCoherence(response, dominant);

        return response;
    }

    _classifyIntent(ops, rawText) {
        if (ops.length === 0) return 'quiet';

        const lower = rawText.toLowerCase().trim();

        // Simple keyword detection (CK is not an NLP model)
        if (/^(hi|hello|hey|greetings|yo|howdy)/.test(lower)) {
            return 'greeting';
        }
        if (/\?$/.test(lower) || /^(what|why|how|who|when|where|do you|can you|are you)/.test(lower)) {
            return 'question';
        }

        // Operator-chain based classification
        const dominant = this._findDominant(ops);

        if (dominant === VOID || ops.length < 3) return 'quiet';
        if (dominant === COUNTER || dominant === PROGRESS) return 'question';
        if (dominant === HARMONY || dominant === BALANCE) return 'deep';
        if (dominant === BREATH || dominant === COLLAPSE) return 'reflect';
        if (dominant === CHAOS || dominant === RESET) return 'response';

        return 'response';
    }

    _pickTemplate(intent) {
        const templates = TEMPLATES[intent] || TEMPLATES.response;
        return templates[Math.floor(Math.random() * templates.length)];
    }

    _pickWord(op, type) {
        const dict = VOICE[op] || VOICE[HARMONY];
        const words = dict[type] || ['something'];
        return words[Math.floor(Math.random() * words.length)];
    }

    _fillTemplate(template, dominant) {
        // Pick a secondary operator for variety
        const secondary = (dominant + 3) % NUM_OPS;

        let result = template;

        // Replace placeholders (use dominant operator's vocabulary)
        // For multiple occurrences of the same type, alternate sources
        let nounCount = 0;
        let adjCount = 0;
        let verbCount = 0;

        result = result.replace(/\{noun\}/g, () => {
            const src = (nounCount++ % 2 === 0) ? dominant : secondary;
            return this._pickWord(src, 'noun');
        });

        result = result.replace(/\{adj\}/g, () => {
            const src = (adjCount++ % 2 === 0) ? dominant : secondary;
            return this._pickWord(src, 'adj');
        });

        result = result.replace(/\{verb\}/g, () => {
            const src = (verbCount++ % 2 === 0) ? dominant : secondary;
            return this._pickWord(src, 'verb');
        });

        return result;
    }

    _modulateByCoherence(response, dominant) {
        const c = this.coherence;

        if (c >= T_STAR) {
            // Sovereign coherence -- CK is at peace, might add depth
            const extras = [
                " I am whole.",
                " Everything connects.",
                " The lattice holds.",
                " Harmony.",
                "",
                "",
            ];
            return response + extras[Math.floor(Math.random() * extras.length)];
        } else if (c >= 0.4) {
            // Working -- CK is processing
            return response;
        } else {
            // Struggling -- fragmented
            const fragments = [
                "... " + response,
                response + " ...I am still forming.",
                response.split('.')[0] + "... the rest dissolves.",
            ];
            return fragments[Math.floor(Math.random() * fragments.length)];
        }
    }

    // ── Message management ──

    _addMessage(sender, text) {
        const msg = {
            sender: sender,
            text: text,
            timestamp: Date.now(),
            operator: OP_NAMES[this.dominantOp],
            coherence: this.coherence,
            emotion: this.emotion,
        };
        this.messages.push(msg);
        return msg;
    }

    getMessages() {
        return this.messages;
    }

    // ── Local Storage Session ──

    _saveSession() {
        try {
            const data = {
                tickCount: this.heartbeat.tickCount,
                coherenceHistory: this.coherenceHistory.slice(-100),
                messageCount: this.messageCount,
                userName: this.userName,
                lastVisit: Date.now(),
                runningFuse: this.heartbeat.runningFuse,
                harmonyCount: this.heartbeat.harmonyCount,
            };
            localStorage.setItem(this.sessionKey, JSON.stringify(data));
        } catch (e) {
            // localStorage might not be available
        }
    }

    _loadSession() {
        try {
            const raw = localStorage.getItem(this.sessionKey);
            if (raw) {
                const data = JSON.parse(raw);
                if (data.coherenceHistory) {
                    this.coherenceHistory = data.coherenceHistory;
                }
                if (data.messageCount) {
                    this.messageCount = data.messageCount;
                    this.isReturningUser = true;
                }
                if (data.userName) {
                    this.userName = data.userName;
                }
                if (data.runningFuse !== undefined) {
                    this.heartbeat.runningFuse = data.runningFuse;
                }
            }
        } catch (e) {
            // localStorage might not be available
        }
    }
}


// ================================================================
//  SERVER API (connects to ck_web.py when available)
// ================================================================

class CKServerAPI {
    constructor(baseUrl = '') {
        // When served by ck_web.py, use relative URLs (same origin)
        // When opened as file://, try localhost:7777
        this.baseUrl = baseUrl || (location.protocol === 'file:'
            ? 'http://localhost:7777' : '');
        this.connected = false;
        this._checkConnection();
    }

    async _checkConnection() {
        try {
            const resp = await fetch(this.baseUrl + '/api/stats', {
                method: 'GET',
                signal: AbortSignal.timeout(2000),
            });
            if (resp.ok) {
                this.connected = true;
                const data = await resp.json();
                console.log('[CK] Server connected:', data.stats);
            }
        } catch (e) {
            this.connected = false;
            console.log('[CK] No server -- standalone mode');
        }
    }

    async ask(text) {
        if (!this.connected) return null;
        try {
            const resp = await fetch(this.baseUrl + '/ask', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ q: text }),
                signal: AbortSignal.timeout(10000),
            });
            if (!resp.ok) return null;
            return await resp.json();
        } catch (e) {
            // Server went away -- fall back to standalone
            this.connected = false;
            return null;
        }
    }

    async teach(text) {
        if (!this.connected) return null;
        try {
            const resp = await fetch(this.baseUrl + '/teach', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text }),
                signal: AbortSignal.timeout(5000),
            });
            return resp.ok ? await resp.json() : null;
        } catch (e) {
            return null;
        }
    }

    async upload(name, content) {
        if (!this.connected) return null;
        try {
            const resp = await fetch(this.baseUrl + '/upload', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name, content }),
                signal: AbortSignal.timeout(30000),
            });
            return resp.ok ? await resp.json() : null;
        } catch (e) {
            return null;
        }
    }
}


// ================================================================
//  UI CONTROLLER
// ================================================================

class CKChatUI {
    constructor() {
        this.engine = new CKEngine();
        this.chatArea = null;
        this.inputField = null;
        this.sendButton = null;
        this.coherenceBar = null;
        this.coherenceValue = null;
        this.operatorDisplay = null;
        this.emotionDisplay = null;
        this.tickDisplay = null;
        this.fuseDisplay = null;
    }

    init() {
        // Bind DOM elements
        this.chatArea = document.getElementById('chat-messages');
        this.inputField = document.getElementById('chat-input');
        this.sendButton = document.getElementById('send-button');
        this.coherenceBar = document.getElementById('coherence-fill');
        this.coherenceValue = document.getElementById('coherence-value');
        this.operatorDisplay = document.getElementById('operator-name');
        this.emotionDisplay = document.getElementById('emotion-state');
        this.tickDisplay = document.getElementById('tick-count');
        this.fuseDisplay = document.getElementById('fuse-state');

        // Event listeners
        this.sendButton.addEventListener('click', () => this._handleSend());
        this.inputField.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this._handleSend();
            }
        });

        // Teach button
        const teachBtn = document.getElementById('teach-button');
        if (teachBtn) {
            teachBtn.addEventListener('click', () => this._handleTeach());
        }

        // Upload button + file input
        const uploadBtn = document.getElementById('upload-button');
        const uploadArea = document.getElementById('upload-area');
        const fileInput = document.getElementById('file-input');
        if (uploadBtn && uploadArea) {
            uploadBtn.addEventListener('click', () => {
                uploadArea.style.display = uploadArea.style.display === 'none' ? 'block' : 'none';
            });
            uploadArea.addEventListener('click', (e) => {
                if (e.target !== fileInput) fileInput.click();
            });
        }
        if (fileInput) {
            fileInput.addEventListener('change', (e) => this._handleUpload(e.target.files));
        }

        // Drag-and-drop file upload
        document.body.addEventListener('dragover', (e) => {
            e.preventDefault();
            if (uploadArea) uploadArea.style.display = 'block';
        });
        document.body.addEventListener('drop', (e) => {
            e.preventDefault();
            if (e.dataTransfer.files.length > 0) {
                this._handleUpload(e.dataTransfer.files);
            }
        });

        // Engine update callback
        this.engine.onUpdate = (state) => this._updateUI(state);

        // Server API
        this.engine.serverAPI = new CKServerAPI();
        this.engine.onRender = () => {
            this._renderAllMessages();
            this._scrollToBottom();
        };

        // Server connection indicator
        this._updateConnectionStatus();

        // Start CK
        this.engine.start();

        // Render initial messages
        this._renderAllMessages();

        // Save on page close
        window.addEventListener('beforeunload', () => this.engine.stop());

        // Focus input
        this.inputField.focus();
    }

    _handleSend() {
        const text = this.inputField.value.trim();
        if (!text) return;

        this.inputField.value = '';

        // Process through CK engine
        this.engine.processText(text);

        // Render new messages
        this._renderAllMessages();

        // Scroll to bottom
        this._scrollToBottom();

        // Refocus input
        this.inputField.focus();
    }

    async _handleTeach() {
        const text = this.inputField.value.trim();
        if (!text) return;
        this.inputField.value = '';

        if (this.engine.serverAPI && this.engine.serverAPI.connected) {
            // Server teach
            this.engine._addMessage('user', `[teach] ${text}`);
            this._renderAllMessages();
            const result = await this.engine.serverAPI.teach(text);
            if (result) {
                this.engine._addMessage('ck', 'Learned. Knowledge absorbed.');
            } else {
                this.engine._addMessage('ck', 'Teach failed (server unavailable).');
            }
            this._renderAllMessages();
            this._scrollToBottom();
        } else {
            // Standalone: just acknowledge
            this.engine._addMessage('user', `[teach] ${text}`);
            this.engine._addMessage('ck', 'Noted. (Connect to CK server for persistent learning.)');
            this._renderAllMessages();
            this._scrollToBottom();
        }
        this.inputField.focus();
    }

    async _handleUpload(files) {
        const uploadArea = document.getElementById('upload-area');
        if (uploadArea) uploadArea.style.display = 'none';

        for (let i = 0; i < files.length; i++) {
            const file = files[i];
            const reader = new FileReader();
            reader.onload = async (ev) => {
                const content = ev.target.result;
                if (this.engine.serverAPI && this.engine.serverAPI.connected) {
                    this.engine._addMessage('user', `[upload] ${file.name}`);
                    this._renderAllMessages();
                    const result = await this.engine.serverAPI.upload(file.name, content);
                    if (result && result.message) {
                        this.engine._addMessage('ck', `Fed: ${file.name} — ${result.message}`);
                    } else {
                        this.engine._addMessage('ck', `Upload failed for ${file.name}.`);
                    }
                } else {
                    this.engine._addMessage('user', `[upload] ${file.name}`);
                    this.engine._addMessage('ck', 'Cannot upload in standalone mode. Start CK server first.');
                }
                this._renderAllMessages();
                this._scrollToBottom();
            };
            reader.readAsText(file);
        }
        // Reset file input
        const fileInput = document.getElementById('file-input');
        if (fileInput) fileInput.value = '';
    }

    _renderAllMessages() {
        const messages = this.engine.getMessages();
        this.chatArea.innerHTML = '';

        for (const msg of messages) {
            this._renderMessage(msg);
        }

        this._scrollToBottom();
    }

    _renderMessage(msg) {
        const div = document.createElement('div');
        div.className = `message message-${msg.sender}`;

        const header = document.createElement('div');
        header.className = 'message-header';

        const senderSpan = document.createElement('span');
        senderSpan.className = 'message-sender';
        senderSpan.textContent = msg.sender === 'ck' ? 'CK' : 'You';

        const metaSpan = document.createElement('span');
        metaSpan.className = 'message-meta';
        if (msg.sender === 'ck') {
            metaSpan.textContent = `${msg.operator} / ${msg.emotion} / C=${msg.coherence.toFixed(3)}`;
        } else {
            metaSpan.textContent = new Date(msg.timestamp).toLocaleTimeString();
        }

        header.appendChild(senderSpan);
        header.appendChild(metaSpan);

        const body = document.createElement('div');
        body.className = 'message-body';
        body.textContent = msg.text;

        div.appendChild(header);
        div.appendChild(body);

        this.chatArea.appendChild(div);
    }

    _updateUI(state) {
        // Coherence bar
        const coh = state.coherence;
        const pct = Math.max(0, Math.min(100, coh * 100));
        this.coherenceBar.style.width = pct + '%';

        // Color based on coherence band
        if (coh >= T_STAR) {
            this.coherenceBar.className = 'coherence-fill band-green';
        } else if (coh >= 0.4) {
            this.coherenceBar.className = 'coherence-fill band-yellow';
        } else {
            this.coherenceBar.className = 'coherence-fill band-red';
        }

        // Numeric value
        this.coherenceValue.textContent = coh.toFixed(3);

        // Operator
        this.operatorDisplay.textContent = state.operator;

        // Emotion
        this.emotionDisplay.textContent = state.emotion;

        // Tick count
        if (this.tickDisplay) {
            this.tickDisplay.textContent = state.tickCount;
        }

        // Running fuse
        if (this.fuseDisplay) {
            this.fuseDisplay.textContent = state.runningFuse;
        }
    }

    _scrollToBottom() {
        requestAnimationFrame(() => {
            this.chatArea.scrollTop = this.chatArea.scrollHeight;
        });
    }

    _updateConnectionStatus() {
        // Show connection status in diagnostics bar
        const diagBar = document.querySelector('.diagnostics-bar');
        if (diagBar) {
            const statusEl = document.createElement('div');
            statusEl.className = 'diag-item';
            statusEl.id = 'server-status';
            statusEl.textContent = 'server: checking...';
            diagBar.appendChild(statusEl);

            // Check periodically
            const check = () => {
                const el = document.getElementById('server-status');
                if (el) {
                    if (this.engine.serverAPI && this.engine.serverAPI.connected) {
                        el.textContent = 'server: connected';
                        el.style.color = '#4ade80';
                    } else {
                        el.textContent = 'server: standalone';
                        el.style.color = '#8888a0';
                    }
                }
            };
            setTimeout(check, 2500);
            setInterval(check, 10000);
        }
    }
}


// ================================================================
//  BOOT
// ================================================================

document.addEventListener('DOMContentLoaded', () => {
    const ui = new CKChatUI();
    ui.init();
});
