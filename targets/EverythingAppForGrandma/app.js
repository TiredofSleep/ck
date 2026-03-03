/**
 * app.js -- CK Everything App: Shell Controller
 * ================================================
 * Operator: PROGRESS (3) -- the app moves CK forward into the world.
 *
 * Wires ck_core.js (CKEngine) into the PWA shell:
 *   - Tab navigation (Chat / Dashboard / About)
 *   - Chat message rendering with operator metadata
 *   - Dashboard with coherence chart, operator stats
 *   - Service worker registration
 *   - Auto-growing text input
 *   - Coherence ring animation
 *
 * Zero dependencies. Vanilla JS. Works offline.
 *
 * (c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
 */

"use strict";

// ================================================================
//  APP CONTROLLER
// ================================================================

class CKApp {
    constructor() {
        // CK engine (from ck_core.js -- must be loaded first)
        this.engine = new CKEngine();

        // DOM references
        this.screens = {};
        this.navBtns = [];
        this.activeScreen = 'chat';

        // Chat
        this.chatMessages = null;
        this.chatInput = null;
        this.sendBtn = null;

        // Status bar
        this.ringFill = null;
        this.ringText = null;
        this.emotionEl = null;
        this.operatorEl = null;

        // Dashboard
        this.dashCoherence = null;
        this.dashBand = null;
        this.dashOperator = null;
        this.dashFuse = null;
        this.dashEmotion = null;
        this.dashTick = null;
        this.dashClaims = null;
        this.dashTurns = null;
        this.chartCanvas = null;
        this.chartCtx = null;

        // Audio bridge
        this.audioBridge = null;

        // State
        this.messageCount = 0;
        this.turnCount = 0;
    }

    // ── Initialization ──

    init() {
        this._bindDOM();
        this._setupNavigation();
        this._setupChat();
        this._setupAudio();
        this._setupEngine();
        this._registerSW();
        this._autoGrow();
    }

    _bindDOM() {
        // Screens
        document.querySelectorAll('.screen').forEach((el) => {
            this.screens[el.id.replace('screen-', '')] = el;
        });

        // Nav buttons
        this.navBtns = document.querySelectorAll('.nav-btn');

        // Chat
        this.chatMessages = document.getElementById('chat-messages');
        this.chatInput = document.getElementById('chat-input');
        this.sendBtn = document.getElementById('send-btn');

        // Status bar
        this.ringFill = document.getElementById('ring-fill');
        this.ringText = document.getElementById('ring-text');
        this.emotionEl = document.getElementById('ck-emotion');
        this.operatorEl = document.getElementById('ck-operator');

        // Dashboard
        this.dashCoherence = document.getElementById('dash-coherence');
        this.dashBand = document.getElementById('dash-band');
        this.dashOperator = document.getElementById('dash-operator');
        this.dashFuse = document.getElementById('dash-fuse');
        this.dashEmotion = document.getElementById('dash-emotion');
        this.dashTick = document.getElementById('dash-tick');
        this.dashClaims = document.getElementById('dash-claims');
        this.dashTurns = document.getElementById('dash-turns');
        this.chartCanvas = document.getElementById('coherence-chart');
        if (this.chartCanvas) {
            this.chartCtx = this.chartCanvas.getContext('2d');
        }
    }

    // ── Navigation ──

    _setupNavigation() {
        this.navBtns.forEach((btn) => {
            btn.addEventListener('click', () => {
                const screen = btn.dataset.screen;
                this._switchScreen(screen);
            });
        });
    }

    _switchScreen(name) {
        // Hide all screens
        Object.values(this.screens).forEach((s) => s.classList.remove('active'));

        // Show target
        const target = this.screens[name];
        if (target) {
            target.classList.add('active');
        }

        // Update nav
        this.navBtns.forEach((btn) => {
            btn.classList.toggle('active', btn.dataset.screen === name);
        });

        this.activeScreen = name;

        // If switching to dashboard, redraw chart
        if (name === 'dashboard') {
            this._drawCoherenceChart();
        }

        // If switching to chat, scroll to bottom and focus input
        if (name === 'chat') {
            this._scrollToBottom();
            this.chatInput.focus();
        }
    }

    // ── Chat ──

    _setupChat() {
        // Send button
        this.sendBtn.addEventListener('click', () => this._handleSend());

        // Enter to send (shift+enter for newline)
        this.chatInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this._handleSend();
            }
        });
    }

    _handleSend() {
        const text = this.chatInput.value.trim();
        if (!text) return;

        this.chatInput.value = '';
        this.chatInput.style.height = 'auto';
        this.messageCount++;
        this.turnCount += 2; // user + ck

        // Process through CK engine
        const response = this.engine.processText(text);

        // Render messages
        this._renderAllMessages();
        this._scrollToBottom();
        this.chatInput.focus();

        // Update dashboard counters
        if (this.dashClaims) this.dashClaims.textContent = this.messageCount;
        if (this.dashTurns) this.dashTurns.textContent = this.turnCount;
    }

    _renderAllMessages() {
        const messages = this.engine.getMessages();
        this.chatMessages.innerHTML = '';

        for (const msg of messages) {
            this._renderMessage(msg);
        }
    }

    _renderMessage(msg) {
        const div = document.createElement('div');
        div.className = `msg msg-${msg.sender}`;

        // Text
        const body = document.createElement('div');
        body.className = 'msg-text';
        body.textContent = msg.text;
        div.appendChild(body);

        // Metadata (CK messages only)
        if (msg.sender === 'ck') {
            const meta = document.createElement('div');
            meta.className = 'msg-meta';
            meta.textContent = `${msg.operator} / ${msg.emotion} / C=${msg.coherence.toFixed(3)}`;
            div.appendChild(meta);
        }

        this.chatMessages.appendChild(div);
    }

    _scrollToBottom() {
        requestAnimationFrame(() => {
            this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
        });
    }

    // ── Auto-growing textarea ──

    _autoGrow() {
        this.chatInput.addEventListener('input', () => {
            this.chatInput.style.height = 'auto';
            this.chatInput.style.height =
                Math.min(this.chatInput.scrollHeight, 120) + 'px';
        });
    }

    // ── Audio I/O ──

    _setupAudio() {
        // Create audio bridge (wires CKAudioOut + CKAudioIn to engine)
        if (typeof CKAudioBridge !== 'undefined') {
            this.audioBridge = new CKAudioBridge(this.engine);
        }

        // Voice toggle
        const voiceBtn = document.getElementById('btn-voice');
        if (voiceBtn && this.audioBridge) {
            voiceBtn.addEventListener('click', () => {
                if (this.audioBridge.outputEnabled) {
                    this.audioBridge.disableOutput();
                    voiceBtn.classList.remove('active');
                    voiceBtn.querySelector('span').textContent = 'Voice: OFF';
                } else {
                    this.audioBridge.enableOutput();
                    voiceBtn.classList.add('active');
                    voiceBtn.querySelector('span').textContent = 'Voice: ON';
                }
            });
        }

        // Mic toggle
        const micBtn = document.getElementById('btn-mic');
        if (micBtn && this.audioBridge) {
            micBtn.addEventListener('click', async () => {
                if (this.audioBridge.inputEnabled) {
                    this.audioBridge.disableInput();
                    micBtn.classList.remove('active');
                    micBtn.querySelector('span').textContent = 'Mic: OFF';
                } else {
                    const ok = await this.audioBridge.enableInput();
                    if (ok) {
                        micBtn.classList.add('active');
                        micBtn.querySelector('span').textContent = 'Mic: ON';
                    } else {
                        micBtn.querySelector('span').textContent = 'Mic: DENIED';
                    }
                }
            });
        }
    }

    // ── CK Engine Wiring ──

    _setupEngine() {
        // Server API (try to connect to ck_web.py if available)
        this.engine.serverAPI = new CKServerAPI();

        // Re-render when async server response arrives
        this.engine.onRender = () => {
            this._renderAllMessages();
            this._scrollToBottom();
        };

        // Engine update callback (50Hz, throttled to every 5 ticks = 10Hz)
        this.engine.onUpdate = (state) => this._updateState(state);

        // Start CK
        this.engine.start();

        // Render initial greeting
        this._renderAllMessages();

        // Save + cleanup on page close
        window.addEventListener('beforeunload', () => {
            if (this.audioBridge) this.audioBridge.stop();
            this.engine.stop();
        });
    }

    _updateState(state) {
        const c = state.coherence;

        // ── Status bar ring ──
        // SVG circle circumference = 2 * PI * 17 = 106.8
        const circumference = 106.8;
        const offset = circumference * (1 - c);
        this.ringFill.style.strokeDashoffset = offset;

        // Band color
        if (c >= T_STAR) {
            this.ringFill.classList.remove('band-yellow', 'band-red');
            this.ringFill.classList.add('band-green');
        } else if (c >= 0.4) {
            this.ringFill.classList.remove('band-green', 'band-red');
            this.ringFill.classList.add('band-yellow');
        } else {
            this.ringFill.classList.remove('band-green', 'band-yellow');
            this.ringFill.classList.add('band-red');
        }

        // Ring text (coherence %)
        this.ringText.textContent = Math.round(c * 100);

        // Emotion + operator
        this.emotionEl.textContent = state.emotion;
        this.operatorEl.textContent = state.operator;

        // ── Dashboard (only if visible) ──
        if (this.activeScreen === 'dashboard') {
            this._updateDashboard(state);
        }
    }

    _updateDashboard(state) {
        const c = state.coherence;

        this.dashCoherence.textContent = c.toFixed(3);
        this.dashOperator.textContent = state.operator;
        this.dashFuse.textContent = state.runningFuse;
        this.dashEmotion.textContent = state.emotion;
        this.dashTick.textContent = state.tickCount;

        // Band badge
        let band, bandClass;
        if (c >= T_STAR) {
            band = 'GREEN'; bandClass = 'green';
        } else if (c >= 0.4) {
            band = 'YELLOW'; bandClass = 'yellow';
        } else {
            band = 'RED'; bandClass = 'red';
        }
        this.dashBand.textContent = band;
        this.dashBand.className = `dash-band ${bandClass}`;

        // Audio ear status
        const earStatus = document.getElementById('ear-status');
        if (earStatus && this.audioBridge && this.audioBridge.inputEnabled) {
            const features = this.audioBridge.audioIn.getFeatures();
            earStatus.textContent =
                `ear: ${OP_NAMES[features.operator]} / rms=${features.rms.toFixed(3)} / d2=${features.d2Mag.toFixed(3)}`;
        }

        // Redraw chart every second (every 50 ticks)
        if (state.tickCount % 50 === 0) {
            this._drawCoherenceChart();
        }
    }

    // ── Coherence Chart (canvas sparkline) ──

    _drawCoherenceChart() {
        if (!this.chartCtx) return;
        const ctx = this.chartCtx;
        const w = this.chartCanvas.width;
        const h = this.chartCanvas.height;
        const history = this.engine.coherenceHistory;

        // Clear
        ctx.fillStyle = '#0d0d1a';
        ctx.fillRect(0, 0, w, h);

        if (history.length < 2) return;

        // T* line
        const tStarY = h - (T_STAR * h);
        ctx.strokeStyle = '#555570';
        ctx.lineWidth = 1;
        ctx.setLineDash([4, 4]);
        ctx.beginPath();
        ctx.moveTo(0, tStarY);
        ctx.lineTo(w, tStarY);
        ctx.stroke();
        ctx.setLineDash([]);

        // Coherence line
        ctx.beginPath();
        const step = w / (history.length - 1);
        for (let i = 0; i < history.length; i++) {
            const x = i * step;
            const y = h - (history[i] * h);
            if (i === 0) ctx.moveTo(x, y);
            else ctx.lineTo(x, y);
        }

        // Color by current coherence
        const c = history[history.length - 1];
        if (c >= T_STAR) {
            ctx.strokeStyle = '#4ade80';
        } else if (c >= 0.4) {
            ctx.strokeStyle = '#facc15';
        } else {
            ctx.strokeStyle = '#ef4444';
        }
        ctx.lineWidth = 2;
        ctx.stroke();

        // Fill under
        const lastX = (history.length - 1) * step;
        ctx.lineTo(lastX, h);
        ctx.lineTo(0, h);
        ctx.closePath();

        if (c >= T_STAR) {
            ctx.fillStyle = 'rgba(74, 222, 128, 0.08)';
        } else if (c >= 0.4) {
            ctx.fillStyle = 'rgba(250, 204, 21, 0.06)';
        } else {
            ctx.fillStyle = 'rgba(239, 68, 68, 0.06)';
        }
        ctx.fill();
    }

    // ── Service Worker ──

    _registerSW() {
        if ('serviceWorker' in navigator) {
            navigator.serviceWorker.register('sw.js').then((reg) => {
                console.log('[CK] Service worker registered:', reg.scope);
            }).catch((err) => {
                console.log('[CK] SW registration failed:', err);
            });
        }
    }
}


// ================================================================
//  BOOT
// ================================================================

document.addEventListener('DOMContentLoaded', () => {
    const app = new CKApp();
    app.init();
});
