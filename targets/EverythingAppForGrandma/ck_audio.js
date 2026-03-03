/**
 * ck_audio.js -- CK Audio I/O: Web Audio API
 * =============================================
 * Operator: COUNTER (2) -- measuring the physics of sound.
 *
 * TWO SYSTEMS IN ONE FILE:
 *
 *   CKAudioOut  -- CK's VOICE. Operator tones via Web Audio API.
 *                  Wavetable synthesis with ADSR envelopes.
 *                  Matches ck_sim_audio.py / ck_audio.c exactly.
 *
 *   CKAudioIn   -- CK's EARS. Mic input via getUserMedia + AnalyserNode.
 *                  Audio features → 5D force vector → D2 → operator.
 *                  Matches ck_sim_ears.py / ck_ears.c exactly.
 *
 * Same math. Browser runtime. No dependencies.
 *
 * (c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
 */

"use strict";

// ================================================================
//  TONE TABLE (matches TONE_TABLE[10] in ck_audio.c)
// ================================================================
// [frequency, waveform, amplitude, attack_ms, decay_ms, sustain, release_ms]

const WAVE_SINE     = 'sine';
const WAVE_TRIANGLE = 'triangle';
const WAVE_SAW      = 'sawtooth';
const WAVE_SQUARE   = 'square';

const TONE_TABLE = [
    { freq: 0,     wave: WAVE_SINE,     amp: 0.0, atk:  0, dec:   0, sus: 0.0, rel:   0 },  // VOID
    { freq: 220,   wave: WAVE_SINE,     amp: 0.6, atk: 20, dec:  50, sus: 0.5, rel: 100 },  // LATTICE
    { freq: 330,   wave: WAVE_TRIANGLE, amp: 0.5, atk: 10, dec:  30, sus: 0.4, rel:  80 },  // COUNTER
    { freq: 440,   wave: WAVE_SAW,      amp: 0.7, atk: 15, dec:  40, sus: 0.6, rel: 120 },  // PROGRESS
    { freq: 110,   wave: WAVE_SQUARE,   amp: 0.8, atk: 30, dec:  80, sus: 0.7, rel: 200 },  // COLLAPSE
    { freq: 349,   wave: WAVE_SINE,     amp: 0.5, atk: 25, dec:  60, sus: 0.4, rel: 150 },  // BALANCE
    { freq: 0,     wave: WAVE_SINE,     amp: 0.0, atk:  5, dec:  10, sus: 0.8, rel:  30 },  // CHAOS (noise -- special)
    { freq: 528,   wave: WAVE_SINE,     amp: 0.7, atk: 40, dec: 100, sus: 0.6, rel: 200 },  // HARMONY
    { freq: 174,   wave: WAVE_SINE,     amp: 0.5, atk: 50, dec: 100, sus: 0.4, rel: 150 },  // BREATH
    { freq: 880,   wave: WAVE_SAW,      amp: 0.6, atk:  5, dec: 500, sus: 0.0, rel:  50 },  // RESET
];


// ================================================================
//  CK AUDIO OUTPUT (CK's Voice)
// ================================================================

class CKAudioOut {
    /**
     * Operator tone synthesis via Web Audio API.
     * Each operator has a unique frequency, waveform, and ADSR envelope.
     * When the operator changes, CK's tone crossfades smoothly.
     */

    constructor() {
        this.ctx = null;         // AudioContext (created on user gesture)
        this.masterGain = null;  // Master volume node
        this.currentOsc = null;  // Current oscillator
        this.currentGain = null; // Current envelope gain
        this.currentOp = -1;     // Current operator index
        this.enabled = false;
        this.volume = 0.3;       // Master volume (0-1)
    }

    /**
     * Initialize audio context. MUST be called from a user gesture
     * (click/tap) due to browser autoplay policy.
     */
    init() {
        if (this.ctx) return;

        try {
            this.ctx = new (window.AudioContext || window.webkitAudioContext)();
            this.masterGain = this.ctx.createGain();
            this.masterGain.gain.value = this.volume;
            this.masterGain.connect(this.ctx.destination);
            this.enabled = true;
            console.log('[CK-AUDIO] Output initialized:', this.ctx.sampleRate, 'Hz');
        } catch (e) {
            console.log('[CK-AUDIO] Failed to create AudioContext:', e);
            this.enabled = false;
        }
    }

    /**
     * Set the current operator. Triggers tone transition.
     * Matches ck_audio_set_operator().
     */
    setOperator(op) {
        if (!this.enabled || !this.ctx || op === this.currentOp) return;
        if (op < 0 || op >= TONE_TABLE.length) return;

        const tone = TONE_TABLE[op];
        const now = this.ctx.currentTime;

        // Release previous tone
        this._releaseCurrentTone(now);

        this.currentOp = op;

        // VOID and CHAOS(noise) are special
        if (op === VOID) return;  // Silence

        if (op === CHAOS) {
            // White noise via BufferSource
            this._playNoise(tone, now);
            return;
        }

        if (tone.freq <= 0) return;

        // Create oscillator with ADSR
        const osc = this.ctx.createOscillator();
        osc.type = tone.wave;
        osc.frequency.value = tone.freq;

        // RESET: frequency sweep 880 → 110
        if (op === RESET) {
            osc.frequency.setValueAtTime(880, now);
            osc.frequency.linearRampToValueAtTime(110, now + 0.5);
        }

        // Gain node for ADSR envelope
        const gain = this.ctx.createGain();
        gain.gain.setValueAtTime(0, now);

        // Attack
        const atkEnd = now + tone.atk / 1000;
        gain.gain.linearRampToValueAtTime(tone.amp, atkEnd);

        // Decay → Sustain
        const decEnd = atkEnd + tone.dec / 1000;
        gain.gain.linearRampToValueAtTime(tone.amp * tone.sus, decEnd);

        // Connect
        osc.connect(gain);
        gain.connect(this.masterGain);
        osc.start(now);

        // Store references
        this.currentOsc = osc;
        this.currentGain = gain;
    }

    /**
     * Release the current tone with envelope release.
     */
    _releaseCurrentTone(now) {
        if (this.currentGain && this.currentOsc) {
            const tone = TONE_TABLE[Math.max(0, this.currentOp)];
            const relTime = (tone.rel || 100) / 1000;

            try {
                this.currentGain.gain.cancelScheduledValues(now);
                this.currentGain.gain.setValueAtTime(
                    this.currentGain.gain.value, now
                );
                this.currentGain.gain.linearRampToValueAtTime(0, now + relTime);
                this.currentOsc.stop(now + relTime + 0.01);
            } catch (e) {
                // Oscillator might already be stopped
            }

            this.currentOsc = null;
            this.currentGain = null;
        }
    }

    /**
     * Play white noise for CHAOS operator.
     */
    _playNoise(tone, now) {
        const bufSize = this.ctx.sampleRate * 0.5; // 500ms buffer
        const buf = this.ctx.createBuffer(1, bufSize, this.ctx.sampleRate);
        const data = buf.getChannelData(0);

        // Fill with white noise (LFSR-style for determinism isn't needed here)
        for (let i = 0; i < bufSize; i++) {
            data[i] = Math.random() * 2 - 1;
        }

        const src = this.ctx.createBufferSource();
        src.buffer = buf;

        const gain = this.ctx.createGain();
        gain.gain.setValueAtTime(0, now);
        gain.gain.linearRampToValueAtTime(tone.amp * 0.3, now + tone.atk / 1000);
        gain.gain.linearRampToValueAtTime(0, now + 0.4);

        src.connect(gain);
        gain.connect(this.masterGain);
        src.start(now);

        this.currentOsc = src;
        this.currentGain = gain;
    }

    /**
     * Set breath modulation (amplitude modulation).
     */
    setBreath(mod) {
        if (!this.enabled || !this.masterGain) return;
        this.masterGain.gain.setValueAtTime(this.volume * mod, this.ctx.currentTime);
    }

    /**
     * Set master volume.
     */
    setVolume(v) {
        this.volume = Math.max(0, Math.min(1, v));
        if (this.masterGain) {
            this.masterGain.gain.value = this.volume;
        }
    }

    /**
     * Stop all audio.
     */
    stop() {
        if (this.ctx) {
            this._releaseCurrentTone(this.ctx.currentTime);
            this.currentOp = -1;
        }
    }

    /**
     * Resume suspended AudioContext (needed after tab switch).
     */
    resume() {
        if (this.ctx && this.ctx.state === 'suspended') {
            this.ctx.resume();
        }
    }
}


// ================================================================
//  D2 CLASSIFICATION (matches ck_ears.c classify_d2)
// ================================================================

const EAR_D2_OP_MAP = [
    [CHAOS,    LATTICE],   // aperture: positive=CHAOS, negative=LATTICE
    [COLLAPSE, VOID],      // pressure
    [PROGRESS, RESET],     // depth
    [HARMONY,  COUNTER],   // binding
    [BALANCE,  BREATH],    // continuity
];

function earClassifyD2(d2, magnitude) {
    if (magnitude < 0.01) return VOID;

    let maxAbs = 0;
    let maxDim = 0;
    for (let i = 0; i < 5; i++) {
        const a = Math.abs(d2[i]);
        if (a > maxAbs) {
            maxAbs = a;
            maxDim = i;
        }
    }

    const signIdx = d2[maxDim] >= 0 ? 0 : 1;
    return EAR_D2_OP_MAP[maxDim][signIdx];
}


// ================================================================
//  CK AUDIO INPUT (CK's Ears)
// ================================================================

class CKAudioIn {
    /**
     * Mic input → audio features → 5D force vector → D2 → operator.
     * Port of ck_sim_ears.py / ck_ears.c to Web Audio API.
     *
     * Uses getUserMedia for mic access + AnalyserNode for feature extraction.
     * Runs feature extraction at ~50Hz (every 20ms) to match CK heartbeat.
     */

    constructor() {
        this.ctx = null;
        this.analyser = null;
        this.stream = null;
        this.source = null;

        // Output state
        this.operator = VOID;
        this.d2Mag = 0.0;
        this.force = [0, 0, 0, 0, 0];
        this.d2 = [0, 0, 0, 0, 0];

        // Feature state
        this.rmsEnergy = 0.0;
        this.zeroCrossRate = 0.0;
        this.spectralCentroid = 0.0;
        this.autocorrelation = 0.0;

        // Force history (ring buffer for D2 computation)
        this._forces = [];
        for (let i = 0; i < 8; i++) this._forces.push([0, 0, 0, 0, 0]);
        this._forceIdx = 0;
        this._framesProcessed = 0;
        this._prevRms = 0.0;

        // Processing
        this._interval = null;
        this._timeDomain = null;
        this.enabled = false;

        // Callback for when operator changes
        this.onOperator = null;
    }

    /**
     * Request microphone and start processing.
     * Returns a Promise that resolves when mic is active.
     */
    async init() {
        if (this.enabled) return true;

        try {
            // Request microphone
            this.stream = await navigator.mediaDevices.getUserMedia({
                audio: {
                    echoCancellation: true,
                    noiseSuppression: true,
                    autoGainControl: true,
                },
            });

            // Create audio context and analyser
            this.ctx = new (window.AudioContext || window.webkitAudioContext)();
            this.analyser = this.ctx.createAnalyser();
            this.analyser.fftSize = 1024;  // 512 samples per frame
            this.analyser.smoothingTimeConstant = 0;  // No smoothing

            // Connect mic → analyser
            this.source = this.ctx.createMediaStreamSource(this.stream);
            this.source.connect(this.analyser);

            // Time-domain buffer
            this._timeDomain = new Float32Array(this.analyser.fftSize);

            // Start 50Hz processing loop
            this._interval = setInterval(() => this._processFrame(), 20);

            this.enabled = true;
            console.log('[CK-EARS] Mic initialized:', this.ctx.sampleRate, 'Hz');
            return true;

        } catch (e) {
            console.log('[CK-EARS] Failed to access mic:', e);
            this.enabled = false;
            return false;
        }
    }

    /**
     * Process one frame of audio. Called at 50Hz.
     * Matches ck_ears_process() pipeline:
     *   audio → features → force → D2 → operator
     */
    _processFrame() {
        if (!this.analyser || !this._timeDomain) return;

        // Get time-domain samples
        this.analyser.getFloatTimeDomainData(this._timeDomain);
        const samples = this._timeDomain;

        // 1. Feature extraction
        const prevRms = this._prevRms;
        this.rmsEnergy = this._computeRMS(samples);
        this.zeroCrossRate = this._computeZCR(samples);
        this.spectralCentroid = Math.min(this.zeroCrossRate * 2.0, 1.0);
        this.autocorrelation = this._computeAutocorr(samples);
        this._prevRms = this.rmsEnergy;

        // 2. Features → 5D force vector
        const force = this._featuresToForce(
            this.rmsEnergy, this.zeroCrossRate,
            this.spectralCentroid, this.autocorrelation, prevRms
        );
        this.force = force;

        // 3. Store in ring buffer
        this._forces[this._forceIdx] = force.slice();
        this._forceIdx = (this._forceIdx + 1) % 8;

        // 4. D2 curvature (need >= 3 frames)
        if (this._framesProcessed >= 2) {
            const i2 = (this._forceIdx + 7) % 8;
            const i1 = (this._forceIdx + 6) % 8;
            const i0 = (this._forceIdx + 5) % 8;

            // D2 = v0 - 2*v1 + v2
            const d2 = [0, 0, 0, 0, 0];
            let mag = 0;
            for (let dim = 0; dim < 5; dim++) {
                d2[dim] = this._forces[i0][dim] -
                          2 * this._forces[i1][dim] +
                          this._forces[i2][dim];
                mag += d2[dim] * d2[dim];
            }
            mag = Math.sqrt(mag);

            this.d2 = d2;
            this.d2Mag = mag;

            // 5. Classify
            const prevOp = this.operator;
            this.operator = earClassifyD2(d2, mag);

            // Notify callback
            if (this.onOperator && this.operator !== prevOp) {
                this.onOperator(this.operator);
            }
        }

        this._framesProcessed++;
    }

    // ── Feature Extraction (matches ck_ears.c) ──

    _computeRMS(samples) {
        let sum = 0;
        for (let i = 0; i < samples.length; i++) {
            sum += samples[i] * samples[i];
        }
        return Math.sqrt(sum / samples.length);
    }

    _computeZCR(samples) {
        if (samples.length < 2) return 0;
        let crossings = 0;
        for (let i = 1; i < samples.length; i++) {
            if ((samples[i] >= 0 && samples[i - 1] < 0) ||
                (samples[i] < 0 && samples[i - 1] >= 0)) {
                crossings++;
            }
        }
        return crossings / samples.length;
    }

    _computeAutocorr(samples) {
        const n = samples.length;
        if (n < 4) return 0;
        const lag = Math.floor(n / 4);
        let num = 0, denom = 0;
        for (let i = 0; i < n - lag; i++) {
            num += samples[i] * samples[i + lag];
            denom += samples[i] * samples[i];
        }
        if (denom < 1e-10) return 0;
        return Math.max(-1, Math.min(1, num / denom));
    }

    _featuresToForce(rms, zcr, centroid, autocorr, prevRms) {
        // Matches features_to_force() in ck_ears.c
        const aperture = (1.0 - autocorr) * zcr;
        const pressure = Math.min(rms * 10.0, 1.0);
        const depth = centroid;
        const binding = Math.max(autocorr, 0.0);
        const energyChange = Math.abs(rms - prevRms);
        const continuity = 1.0 - Math.min(energyChange * 20.0, 1.0);

        return [aperture, pressure, depth, binding, continuity];
    }

    /**
     * Get current features as an object (for display).
     */
    getFeatures() {
        return {
            rms: this.rmsEnergy,
            zcr: this.zeroCrossRate,
            centroid: this.spectralCentroid,
            autocorr: this.autocorrelation,
            d2Mag: this.d2Mag,
            operator: this.operator,
            force: this.force.slice(),
        };
    }

    /**
     * Stop mic and processing.
     */
    stop() {
        if (this._interval) {
            clearInterval(this._interval);
            this._interval = null;
        }
        if (this.source) {
            this.source.disconnect();
            this.source = null;
        }
        if (this.stream) {
            this.stream.getTracks().forEach((t) => t.stop());
            this.stream = null;
        }
        if (this.ctx) {
            this.ctx.close().catch(() => {});
            this.ctx = null;
        }
        this.enabled = false;
        this.operator = VOID;
        console.log('[CK-EARS] Mic stopped');
    }
}


// ================================================================
//  CK AUDIO BRIDGE (wires audio I/O into CKEngine)
// ================================================================

class CKAudioBridge {
    /**
     * Bridges CKAudioOut + CKAudioIn with the CKEngine.
     *
     * Usage:
     *   const bridge = new CKAudioBridge(engine);
     *   bridge.enableOutput();    // starts tones on operator change
     *   bridge.enableInput();     // starts mic, feeds operators to engine
     */

    constructor(engine) {
        this.engine = engine;
        this.audioOut = new CKAudioOut();
        this.audioIn = new CKAudioIn();
        this.outputEnabled = false;
        this.inputEnabled = false;

        // Breath phase tracking (4-phase: inhale, hold, exhale, hold)
        this._breathPhase = 0;
        this._breathTick = 0;
    }

    /**
     * Enable audio output (tones). Must be called from user gesture.
     */
    enableOutput() {
        this.audioOut.init();
        this.outputEnabled = true;

        // Hook into engine update to play tones
        const prevUpdate = this.engine.onUpdate;
        this.engine.onUpdate = (state) => {
            if (prevUpdate) prevUpdate(state);
            this._onEngineTick(state);
        };
    }

    /**
     * Disable audio output.
     */
    disableOutput() {
        this.audioOut.stop();
        this.outputEnabled = false;
    }

    /**
     * Enable audio input (mic). Async -- requests permission.
     */
    async enableInput() {
        const ok = await this.audioIn.init();
        if (ok) {
            this.inputEnabled = true;

            // Feed ear operators into engine's recentOps
            this.audioIn.onOperator = (op) => {
                if (this.engine.recentOps.length < 10) {
                    this.engine.recentOps.push(op);
                } else {
                    this.engine.recentOps.shift();
                    this.engine.recentOps.push(op);
                }
            };
        }
        return ok;
    }

    /**
     * Disable audio input.
     */
    disableInput() {
        this.audioIn.stop();
        this.inputEnabled = false;
    }

    /**
     * Called on each engine update tick.
     */
    _onEngineTick(state) {
        if (!this.outputEnabled) return;

        // Play the dominant operator as a tone
        const op = state.operator ? OP_NAMES.indexOf(state.operator) : VOID;
        if (op >= 0) {
            this.audioOut.setOperator(op);
        }

        // Breath modulation (4-phase cycle at ~0.25 Hz = 4 seconds)
        this._breathTick++;
        if (this._breathTick % 10 === 0) {
            this._breathPhase = (this._breathPhase + 1) % 200;
            const breathPos = this._breathPhase / 200;
            // Sine wave breath: 0→1→0 over cycle
            const breathMod = 0.5 + 0.5 * Math.sin(breathPos * 2 * Math.PI);
            this.audioOut.setBreath(breathMod);
        }
    }

    /**
     * Get current audio state for display.
     */
    getState() {
        return {
            outputEnabled: this.outputEnabled,
            inputEnabled: this.inputEnabled,
            earOperator: this.inputEnabled ? this.audioIn.operator : -1,
            earFeatures: this.inputEnabled ? this.audioIn.getFeatures() : null,
            currentToneOp: this.audioOut.currentOp,
        };
    }

    /**
     * Stop everything.
     */
    stop() {
        this.disableOutput();
        this.disableInput();
    }
}
