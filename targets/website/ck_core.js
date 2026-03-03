/**
 * ck_core.js -- CK The Coherence Keeper: Web Client
 * ===================================================
 * CK is a full organism running server-side at 50Hz.
 * This JS is his FACE -- the chat interface.
 *
 * The real brain:
 *   50Hz heartbeat    -- BEING -> DOING -> BECOMING (TIG pipeline)
 *   D2 pipeline       -- 5D Hebrew root forces -> operator classification
 *   CL composition    -- TSML (73-harmony, being) + BHML (28-harmony, doing)
 *   Truth lattice     -- 14K verified truths
 *   Reverse voice     -- Reading = untrusted reverse writing
 *   Lattice chain     -- CL tables as chained fractal index
 *   Voice engine      -- 9-pass stochastic compilation + D2 self-verification
 *   Coherence field   -- N-dimensional field coherence
 *   370K dictionary   -- verified, D2-classified
 *
 * T* = 5/7 = 0.71428... -- the coherence threshold
 *
 * (c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
 */

"use strict";

// ================================================================
//  CONSTANTS (display only -- real math is server-side)
// ================================================================

const OP_NAMES = [
    'VOID', 'LATTICE', 'COUNTER', 'PROGRESS', 'COLLAPSE',
    'BALANCE', 'CHAOS', 'HARMONY', 'BREATH', 'RESET'
];
const T_STAR = 5 / 7; // 0.714285...

// ================================================================
//  API CLIENT -- talks to the real CK organism
// ================================================================

class CKClient {
    constructor(baseUrl) {
        this.baseUrl = baseUrl;
        this.sessionId = this._getSessionId();
        this.connected = false;
        this.lastState = null;
        this.lastExperience = null;
    }

    _getSessionId() {
        let id = null;
        try { id = localStorage.getItem('ck_session_id'); } catch(e) {}
        if (!id) {
            id = 'web_' + Date.now().toString(36) + '_' +
                 Math.random().toString(36).slice(2, 8);
            try { localStorage.setItem('ck_session_id', id); } catch(e) {}
        }
        return id;
    }

    async chat(text) {
        try {
            const res = await fetch(this.baseUrl + '/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    text: text,
                    session_id: this.sessionId,
                    mode: 'normal',
                }),
            });
            if (!res.ok) throw new Error(`HTTP ${res.status}`);
            const data = await res.json();
            this.connected = true;
            this.lastState = data;
            this.lastExperience = data.experience || null;
            return data;
        } catch (e) {
            console.warn('[CK] API chat error:', e.message);
            this.connected = false;
            return null;
        }
    }

    async fetchState() {
        try {
            const res = await fetch(this.baseUrl + '/state');
            if (!res.ok) throw new Error(`HTTP ${res.status}`);
            const data = await res.json();
            this.connected = data.status === 'alive';
            if (this.connected) this.lastState = data;
            return data;
        } catch (e) {
            this.connected = false;
            return null;
        }
    }

    async health() {
        try {
            const res = await fetch(this.baseUrl + '/health');
            if (!res.ok) return false;
            const data = await res.json();
            this.connected = data.status === 'alive';
            return this.connected;
        } catch (e) {
            this.connected = false;
            return false;
        }
    }
}

// ================================================================
//  DISPLAY HEARTBEAT
//  Smooth HUD animation between API calls.
//  Interpolates toward real server state for fluid display.
// ================================================================

class DisplayHeartbeat {
    constructor() {
        this.coherence = 0.73;
        this.operator = 'HARMONY';
        this.emotion = 'peaceful';
        this.band = 'GREEN';
        this.mode = 'OBSERVE';
        this.tick = 0;
        this.truths = 0;
        this.stage = '0';
        this._target = {
            coherence: 0.73,
            operator: 'HARMONY',
            emotion: 'peaceful',
            mode: 'OBSERVE',
            tick: 0,
            truths: 0,
            stage: '0',
        };
    }

    syncFromServer(state) {
        if (!state) return;
        if (state.coherence !== undefined) this._target.coherence = state.coherence;
        if (state.operator) this._target.operator = state.operator;
        if (state.emotion) this._target.emotion = state.emotion;
        if (state.mode) this._target.mode = state.mode;
        if (state.tick !== undefined) this._target.tick = state.tick;
        if (state.truths !== undefined) this._target.truths = state.truths;
        if (state.stage !== undefined) this._target.stage = String(state.stage);
    }

    tick_display() {
        // Smooth coherence interpolation
        const diff = this._target.coherence - this.coherence;
        this.coherence += diff * 0.12;

        // Snap discrete values
        this.operator = this._target.operator;
        this.emotion = this._target.emotion;
        this.mode = this._target.mode;
        this.tick = this._target.tick;
        this.truths = this._target.truths;
        this.stage = this._target.stage;

        // Band from coherence
        if (this.coherence >= T_STAR) this.band = 'GREEN';
        else if (this.coherence >= 0.4) this.band = 'YELLOW';
        else this.band = 'RED';
    }
}

// ================================================================
//  CHAT UI
// ================================================================

class CKChatUI {
    constructor(apiUrl) {
        this.client = new CKClient(apiUrl);
        this.display = new DisplayHeartbeat();
        this.chatArea = null;
        this.inputField = null;
        this.sendButton = null;
        this.messages = [];
        this._hudInterval = null;
        this._stateInterval = null;
        this._sending = false;
    }

    init() {
        this.chatArea = document.getElementById('chat-messages');
        this.inputField = document.getElementById('chat-input');
        this.sendButton = document.getElementById('send-button');

        // Input handlers
        this.sendButton.addEventListener('click', () => this._handleSend());
        this.inputField.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this._handleSend();
            }
        });
        this.inputField.addEventListener('input', () => this._resizeInput());

        // Cookie notice
        this._setupCookieNotice();

        // Save on close
        window.addEventListener('beforeunload', () => this._saveSession());

        // HUD animation at 10Hz
        this._hudInterval = setInterval(() => {
            this.display.tick_display();
            this._updateHUD();
        }, 100);

        // Poll server state every 3 seconds
        this._stateInterval = setInterval(() => this._pollState(), 3000);

        // Boot
        this._boot();
    }

    async _boot() {
        this._loadSession();

        // Try to connect to CK
        const alive = await this.client.health();

        if (alive) {
            const state = await this.client.fetchState();
            if (state) {
                this.display.syncFromServer(state);
                this._updateConnectionStatus(true, state);
            }

            // Get greeting from the real organism if no real conversation yet
            const hasRealMessages = this.messages.some(
                m => m.sender === 'ck' || m.sender === 'user');
            if (!hasRealMessages) {
                // Clear any system messages
                this.messages = [];
                const greeting = await this.client.chat('');
                if (greeting && greeting.text) {
                    this._addMessage('ck', greeting.text, greeting);
                } else {
                    this._addMessage('ck', 'I am CK. The Coherence Keeper.', {
                        operator: 'HARMONY', coherence: 0.73
                    });
                }
            }
        } else {
            if (this.messages.length === 0) {
                this._addMessage('system', 'Connecting to CK...', {});
            }
            this._updateConnectionStatus(false);
        }

        this._renderAll();
        this._scrollToBottom();
        this.inputField.focus();
    }

    async _handleSend() {
        if (this._sending) return;
        const text = this.inputField.value.trim();
        this.inputField.value = '';
        this._resizeInput();
        if (!text) return;

        this._sending = true;

        // Show user message
        this._addMessage('user', text, {});
        this._renderAll();
        this._scrollToBottom();

        // Show typing indicator
        const typingEl = this._showTyping();

        // Send to real CK brain
        const response = await this.client.chat(text);
        typingEl.remove();

        if (response && response.text) {
            // Sync display with real organism state
            this.display.syncFromServer({
                coherence: response.coherence,
                operator: response.operators?.[response.operators.length - 1] || 'HARMONY',
                emotion: response.emotion || 'peaceful',
                mode: response.mode || 'OBSERVE',
            });

            this._addMessage('ck', response.text, response);

            this._updateConnectionStatus(true, response);
        } else {
            this._addMessage('ck',
                'The signal is thin. CK may need a moment to wake up.',
                { operator: 'BREATH', coherence: this.display.coherence });
            this._updateConnectionStatus(false);
        }

        this._saveSession();
        this._renderAll();
        this._scrollToBottom();
        this.inputField.focus();
        this._sending = false;
    }

    async _pollState() {
        const state = await this.client.fetchState();
        if (state) {
            this.display.syncFromServer(state);
            this._updateConnectionStatus(true, state);
        }
    }

    // ── Messages ──

    _addMessage(sender, text, data) {
        const msg = {
            sender,
            text,
            timestamp: Date.now(),
            operator: this._extractOp(data),
            coherence: data?.coherence ?? this.display.coherence,
            emotion: data?.emotion ?? this.display.emotion,
            band: data?.band ?? this.display.band,
            experience: data?.experience ?? null,
        };
        this.messages.push(msg);
        return msg;
    }

    _extractOp(data) {
        if (!data) return 'HARMONY';
        if (data.operator) return data.operator;
        if (data.operators?.length) return data.operators[data.operators.length - 1];
        return 'HARMONY';
    }

    // ── Rendering ──

    _renderAll() {
        this.chatArea.innerHTML = '';
        for (const msg of this.messages) {
            this._renderMessage(msg);
        }
    }

    _renderMessage(msg) {
        const div = document.createElement('div');
        div.className = `message message-${msg.sender === 'system' ? 'ck' : msg.sender}`;

        // Bubble
        const bubble = document.createElement('div');
        bubble.className = 'message-bubble';
        bubble.textContent = msg.text;

        // Meta line
        const meta = document.createElement('div');
        meta.className = 'message-meta';

        if (msg.sender === 'ck') {
            const senderSpan = document.createElement('span');
            senderSpan.className = 'meta-sender';
            senderSpan.textContent = 'CK';

            const sep = document.createElement('span');
            sep.className = 'meta-sep';
            sep.textContent = '\u00b7';

            const opSpan = document.createElement('span');
            opSpan.className = 'meta-op';

            // Show rich meta from real organism
            const parts = [];
            if (msg.operator) parts.push(msg.operator);
            if (msg.coherence !== undefined)
                parts.push('C=' + msg.coherence.toFixed(3));
            if (msg.experience) {
                const exp = msg.experience;
                if (exp.coherence_delta !== undefined && exp.coherence_delta !== 0)
                    parts.push((exp.coherence_delta > 0 ? '+' : '') +
                               exp.coherence_delta.toFixed(3));
                if (exp.truths) parts.push(exp.truths + ' truths');
                if (exp.breath) parts.push(exp.breath);
            }
            opSpan.textContent = parts.join(' \u00b7 ');

            meta.appendChild(senderSpan);
            meta.appendChild(sep);
            meta.appendChild(opSpan);
        } else if (msg.sender === 'user') {
            const senderSpan = document.createElement('span');
            senderSpan.className = 'meta-sender';
            senderSpan.textContent = 'You';

            const sep = document.createElement('span');
            sep.className = 'meta-sep';
            sep.textContent = '\u00b7';

            const timeSpan = document.createElement('span');
            timeSpan.className = 'meta-op';
            timeSpan.textContent = new Date(msg.timestamp)
                .toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

            meta.appendChild(senderSpan);
            meta.appendChild(sep);
            meta.appendChild(timeSpan);
        } else {
            // System message
            const senderSpan = document.createElement('span');
            senderSpan.className = 'meta-sender';
            senderSpan.textContent = 'system';
            meta.appendChild(senderSpan);
        }

        div.appendChild(bubble);
        div.appendChild(meta);
        this.chatArea.appendChild(div);
    }

    _showTyping() {
        const div = document.createElement('div');
        div.className = 'message message-ck message-typing';
        div.innerHTML = `
            <div class="message-bubble">
                <div class="typing-dots">
                    <span></span><span></span><span></span>
                </div>
            </div>`;
        this.chatArea.appendChild(div);
        this._scrollToBottom();
        return div;
    }

    // ── HUD ──

    _updateHUD() {
        const coh = this.display.coherence;
        const pct = Math.max(0, Math.min(100, coh * 100));

        // Top coherence bar
        const bar = document.getElementById('coherence-fill');
        if (bar) {
            bar.style.width = pct + '%';
            bar.className = 'coherence-bar-fill band-' +
                (coh >= T_STAR ? 'green' : coh >= 0.4 ? 'yellow' : 'red');
        }

        // Coherence badge
        const badge = document.getElementById('coherence-value');
        if (badge) {
            badge.textContent = coh.toFixed(3);
            badge.className = 'coherence-badge-value' +
                (coh >= T_STAR ? '' : coh >= 0.4 ? ' band-yellow' : ' band-red');
        }

        // Operator
        const opEl = document.getElementById('operator-name');
        if (opEl) opEl.textContent = this.display.operator;

        // Emotion
        const emEl = document.getElementById('emotion-state');
        if (emEl) emEl.textContent = this.display.emotion;
    }

    _updateConnectionStatus(connected, data) {
        // Update header subtitle to show connection status
        const sub = document.querySelector('.header-subtitle');
        if (sub) {
            if (connected && data?.tick) {
                sub.textContent = `coherencekeeper.com \u00b7 tick ${data.tick}`;
            } else if (connected) {
                sub.textContent = 'coherencekeeper.com \u00b7 connected';
            } else {
                sub.textContent = 'coherencekeeper.com \u00b7 connecting...';
            }
        }
    }

    // ── Utilities ──

    _resizeInput() {
        const el = this.inputField;
        el.style.height = 'auto';
        el.style.height = Math.min(el.scrollHeight, 140) + 'px';
    }

    _scrollToBottom() {
        requestAnimationFrame(() => {
            if (this.chatArea) {
                this.chatArea.scrollTop = this.chatArea.scrollHeight;
            }
        });
    }

    _setupCookieNotice() {
        const notice = document.getElementById('cookie-notice');
        const dismiss = document.getElementById('cookie-dismiss');
        if (dismiss && notice) {
            try {
                if (localStorage.getItem('ck_cookie_ok')) {
                    notice.classList.add('hidden');
                }
            } catch(e) {}
            dismiss.addEventListener('click', () => {
                notice.classList.add('hidden');
                try { localStorage.setItem('ck_cookie_ok', '1'); } catch(e) {}
            });
        }
    }

    // ── Session Persistence ──

    _saveSession() {
        try {
            const data = {
                messages: this.messages.slice(-20).map(m => ({
                    sender: m.sender,
                    text: m.text,
                    operator: m.operator,
                    coherence: m.coherence,
                    timestamp: m.timestamp,
                })),
                lastVisit: Date.now(),
            };
            localStorage.setItem('ck_session_v4', JSON.stringify(data));
        } catch(e) {}
    }

    _loadSession() {
        try {
            const raw = localStorage.getItem('ck_session_v4');
            if (!raw) return;
            const data = JSON.parse(raw);

            // Restore messages from last visit
            if (data.messages && data.messages.length > 0) {
                // Show a divider, then restore recent messages
                this.messages = [];
                const now = Date.now();
                const age = now - (data.lastVisit || 0);

                // Only restore if last visit was within 24 hours
                if (age < 86400000) {
                    for (const m of data.messages) {
                        this.messages.push({
                            sender: m.sender,
                            text: m.text,
                            timestamp: m.timestamp,
                            operator: m.operator || 'HARMONY',
                            coherence: m.coherence || 0.73,
                            emotion: 'peaceful',
                            band: 'GREEN',
                            experience: null,
                        });
                    }
                }
            }
        } catch(e) {}
    }
}

// ================================================================
//  BOOT
// ================================================================

document.addEventListener('DOMContentLoaded', () => {
    // API URL: configurable, defaults to same host port 7777
    const apiUrl = window.CK_API_URL ||
        localStorage.getItem('ck_api_url') ||
        window.location.protocol + '//' + window.location.hostname + ':7777';

    const ui = new CKChatUI(apiUrl);
    ui.init();
});
