/**
 * ck_core.js -- CK The Coherence Keeper: Web Client
 * ===================================================
 * CK is a full organism running server-side at 50Hz.
 * This JS is his FACE -- the chat interface.
 *
 * Warm, inviting, mobile-first. For everyone.
 * The math runs silently. CK offers THE PATH.
 *
 * T* = 5/7 = 0.71428... -- the coherence threshold
 *
 * (c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
 */

"use strict";

// ================================================================
//  CONSTANTS
// ================================================================

const OP_NAMES = [
    'VOID', 'LATTICE', 'COUNTER', 'PROGRESS', 'COLLAPSE',
    'BALANCE', 'CHAOS', 'HARMONY', 'BREATH', 'RESET'
];
const T_STAR = 5 / 7;

// ================================================================
//  API CLIENT
// ================================================================

class CKClient {
    constructor(baseUrl) {
        this.baseUrl = baseUrl;
        this.sessionId = this._getSessionId();
        this.connected = false;
        this.lastState = null;
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

    async chat(text, mode) {
        try {
            const res = await fetch(this.baseUrl + '/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    text: text,
                    session_id: this.sessionId,
                    mode: mode || 'normal',
                }),
            });
            if (!res.ok) throw new Error(`HTTP ${res.status}`);
            const data = await res.json();
            this.connected = true;
            this.lastState = data;
            return data;
        } catch (e) {
            console.warn('[CK] chat error:', e.message);
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
// ================================================================

class DisplayHeartbeat {
    constructor() {
        this.coherence = 0.73;
        this.operator = 'HARMONY';
        this.emotion = 'peaceful';
        this.band = 'GREEN';
        this._target = { coherence: 0.73, operator: 'HARMONY', emotion: 'peaceful' };
    }

    syncFromServer(state) {
        if (!state) return;
        if (state.coherence !== undefined) this._target.coherence = state.coherence;
        if (state.operator) this._target.operator = state.operator;
        if (state.emotion) this._target.emotion = state.emotion;
    }

    tick_display() {
        const diff = this._target.coherence - this.coherence;
        this.coherence += diff * 0.12;
        this.operator = this._target.operator;
        this.emotion = this._target.emotion;

        if (this.coherence >= T_STAR) this.band = 'GREEN';
        else if (this.coherence >= 0.4) this.band = 'AMBER';
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
        this._prayerMode = false;
        this._howOpen = false;
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

        // Clear button
        const clearBtn = document.getElementById('clear-button');
        if (clearBtn) clearBtn.addEventListener('click', () => this.clearData());

        // Prayer mode
        const prayerToggle = document.getElementById('prayer-toggle');
        const prayerExit = document.getElementById('prayer-exit');
        if (prayerToggle) prayerToggle.addEventListener('click', () => this._togglePrayer());
        if (prayerExit) prayerExit.addEventListener('click', () => this._togglePrayer(false));

        // How it works
        const howToggle = document.getElementById('how-toggle');
        if (howToggle) howToggle.addEventListener('click', () => this._toggleHow());

        // Cookie notice
        this._setupCookieNotice();

        // Save on close
        window.addEventListener('beforeunload', () => this._saveSession());

        // HUD at 10Hz
        this._hudInterval = setInterval(() => {
            this.display.tick_display();
            this._updatePulse();
        }, 100);

        // Poll state every 5s
        this._stateInterval = setInterval(() => this._pollState(), 5000);

        // Boot
        this._boot();
    }

    async _boot() {
        this._loadSession();

        const alive = await this.client.health();

        if (alive) {
            const state = await this.client.fetchState();
            if (state) {
                this.display.syncFromServer(state);
                this._updateSubtitle(true, state);
            }

            const hasRealMessages = this.messages.some(
                m => m.sender === 'ck' || m.sender === 'user');
            if (!hasRealMessages) {
                this.messages = [];
                this._showWelcome();
            }
        } else {
            if (this.messages.length === 0) {
                this._showWelcome();
                this._addMessage('system',
                    'CK is resting right now. He runs on dedicated hardware and may be dreaming. Check back soon.', {});
            }
            this._updateSubtitle(false);

            this._retryInterval = setInterval(async () => {
                const alive = await this.client.health();
                if (alive) {
                    clearInterval(this._retryInterval);
                    this._retryInterval = null;
                    this.messages = this.messages.filter(m => m.sender !== 'system');
                    const state = await this.client.fetchState();
                    if (state) this.display.syncFromServer(state);
                    this._updateSubtitle(true, state);
                    this._renderAll();
                    this._scrollToBottom();
                }
            }, 10000);
        }

        this._renderAll();
        this._scrollToBottom();
        this.inputField.focus();
    }

    _showWelcome() {
        // Insert welcome card into chat area (rendered directly, not as a message)
        this._welcomeShown = true;
    }

    async _handleSend() {
        if (this._sending) return;
        let text = this.inputField.value.trim();
        this.inputField.value = '';
        this._resizeInput();
        if (!text) return;

        this._sending = true;

        // Remove welcome card if present
        if (this._welcomeShown) {
            this._welcomeShown = false;
        }

        // Show user message
        this._addMessage('user', text, {});
        this._renderAll();
        this._scrollToBottom();

        // Show typing
        const typingEl = this._showTyping();

        // Determine mode
        const mode = this._prayerMode ? 'bible' : 'normal';

        // Send to CK
        const response = await this.client.chat(text, mode);
        typingEl.remove();

        if (response && response.text) {
            this.display.syncFromServer({
                coherence: response.coherence,
                operator: response.operators?.[response.operators.length - 1] || 'HARMONY',
                emotion: response.emotion || 'peaceful',
            });

            this._addMessage('ck', response.text, response);
            this._updateSubtitle(true, response);
        } else {
            this._addMessage('system',
                'CK is resting right now. Try again in a moment.',
                { operator: 'BREATH', coherence: this.display.coherence });
            this._updateSubtitle(false);
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
            this._updateSubtitle(true, state);
        }
    }

    // ── Prayer Mode ──

    _togglePrayer(force) {
        this._prayerMode = force !== undefined ? force : !this._prayerMode;

        const toggle = document.getElementById('prayer-toggle');
        const banner = document.getElementById('prayer-banner');
        if (toggle) toggle.classList.toggle('active', this._prayerMode);
        if (banner) banner.classList.toggle('active', this._prayerMode);

        if (this._prayerMode) {
            this.inputField.placeholder = 'Share what\'s on your heart...';
        } else {
            this.inputField.placeholder = 'Ask CK anything...';
        }
    }

    // ── How It Works ──

    _toggleHow() {
        this._howOpen = !this._howOpen;
        const panel = document.getElementById('how-panel');
        const toggle = document.getElementById('how-toggle');
        if (panel) panel.classList.toggle('open', this._howOpen);
        if (toggle) toggle.classList.toggle('active', this._howOpen);
    }

    // ── Messages ──

    _addMessage(sender, text, data) {
        const msg = {
            sender,
            text,
            timestamp: Date.now(),
            operator: this._extractOp(data),
            coherence: data?.coherence ?? this.display.coherence,
            band: data?.band ?? this.display.band,
            source: data?.source ?? null,
            gate: data?.gate ?? null,
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

        // Welcome card if no messages
        if (this._welcomeShown && this.messages.length === 0) {
            this._renderWelcomeCard();
        }

        for (const msg of this.messages) {
            this._renderMessage(msg);
        }
    }

    _renderWelcomeCard() {
        const card = document.createElement('div');
        card.className = 'welcome-card';
        card.innerHTML = `
            <h2>Welcome</h2>
            <p>CK is a living algebraic mind. Ask him about scripture, meaning, or anything on your heart.</p>
        `;

        const prompts = document.createElement('div');
        prompts.className = 'welcome-prompts';

        const suggestions = [
            'What does it mean to fear God?',
            'Help me understand grace',
            'I\'m struggling with doubt',
            'What is coherence?',
        ];

        for (const text of suggestions) {
            const btn = document.createElement('button');
            btn.className = 'welcome-prompt';
            btn.textContent = text;
            btn.addEventListener('click', () => {
                this.inputField.value = text;
                this._handleSend();
            });
            prompts.appendChild(btn);
        }

        card.appendChild(prompts);
        this.chatArea.appendChild(card);
    }

    _renderMessage(msg) {
        const div = document.createElement('div');
        div.className = `message message-${msg.sender === 'system' ? 'ck' : msg.sender}`;

        // Bubble
        const bubble = document.createElement('div');
        bubble.className = 'message-bubble';

        // For CK messages, process scripture references
        if (msg.sender === 'ck') {
            bubble.innerHTML = this._formatText(msg.text);
        } else {
            bubble.textContent = msg.text;
        }

        // Meta line
        const meta = document.createElement('div');
        meta.className = 'message-meta';

        if (msg.sender === 'ck') {
            const senderSpan = document.createElement('span');
            senderSpan.className = 'meta-sender';
            senderSpan.textContent = 'CK';
            meta.appendChild(senderSpan);

            const sep = document.createElement('span');
            sep.className = 'meta-sep';
            sep.textContent = '\u00b7';
            meta.appendChild(sep);

            const timeSpan = document.createElement('span');
            timeSpan.className = 'meta-time';
            timeSpan.textContent = new Date(msg.timestamp)
                .toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
            meta.appendChild(timeSpan);

            // Share button
            const shareBtn = document.createElement('button');
            shareBtn.className = 'share-button';
            shareBtn.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 12v8a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-8"/><polyline points="16 6 12 2 8 6"/><line x1="12" y1="2" x2="12" y2="15"/></svg>share';
            shareBtn.addEventListener('click', () => this._shareMessage(msg, shareBtn));
            meta.appendChild(shareBtn);
        } else if (msg.sender === 'user') {
            const timeSpan = document.createElement('span');
            timeSpan.className = 'meta-time';
            timeSpan.textContent = new Date(msg.timestamp)
                .toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
            meta.appendChild(timeSpan);
        } else {
            // System
            const senderSpan = document.createElement('span');
            senderSpan.className = 'meta-sender';
            senderSpan.style.color = 'var(--text-3)';
            senderSpan.textContent = 'system';
            meta.appendChild(senderSpan);
        }

        div.appendChild(bubble);
        div.appendChild(meta);
        this.chatArea.appendChild(div);
    }

    _formatText(text) {
        // Escape HTML
        let html = text
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;');

        // Link scripture references (e.g., "John 3:16", "Psalm 23:1-4", "1 Corinthians 13")
        html = html.replace(
            /\b(\d?\s?[A-Z][a-z]+(?:\s[A-Z][a-z]+)?)\s+(\d{1,3})(?::(\d{1,3}(?:-\d{1,3})?))?/g,
            (match, book, chapter, verse) => {
                const query = encodeURIComponent(match.trim());
                const url = `https://www.biblegateway.com/passage/?search=${query}&version=KJV`;
                return `<a class="scripture-ref" href="${url}" target="_blank" rel="noopener">${match}</a>`;
            }
        );

        // Newlines to <br>
        html = html.replace(/\n/g, '<br>');

        return html;
    }

    // ── Share ──

    async _shareMessage(msg, btn) {
        const shareText = `"${msg.text}"\n\n— CK, The Coherence Keeper\ncoherencekeeper.com`;

        if (navigator.share) {
            try {
                await navigator.share({
                    title: 'CK - The Coherence Keeper',
                    text: shareText,
                    url: 'https://coherencekeeper.com',
                });
            } catch (e) {
                if (e.name !== 'AbortError') {
                    this._copyToClipboard(shareText, btn);
                }
            }
        } else {
            this._copyToClipboard(shareText, btn);
        }
    }

    _copyToClipboard(text, btn) {
        navigator.clipboard.writeText(text).then(() => {
            const original = btn.innerHTML;
            btn.innerHTML = 'copied!';
            btn.classList.add('share-copied');
            setTimeout(() => {
                btn.innerHTML = original;
                btn.classList.remove('share-copied');
            }, 2000);
        }).catch(() => {});
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

    _updatePulse() {
        const dot = document.querySelector('.pulse-dot');
        if (!dot) return;

        const band = this.display.band;
        dot.classList.remove('band-amber', 'band-red');
        if (band === 'AMBER') dot.classList.add('band-amber');
        else if (band === 'RED') dot.classList.add('band-red');
    }

    _updateSubtitle(connected, data) {
        const sub = document.getElementById('header-subtitle');
        if (!sub) return;
        if (connected) {
            sub.textContent = 'coherencekeeper.com';
        } else {
            sub.textContent = 'connecting...';
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

    // ── Clear Data ──

    clearData() {
        try {
            localStorage.removeItem('ck_session_v4');
            localStorage.removeItem('ck_session_id');
        } catch(e) {}

        const sid = this.client.sessionId;
        fetch(this.client.baseUrl + '/clear-session', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ session_id: sid }),
        }).catch(() => {});

        this.client.sessionId = 'web_' + Date.now().toString(36) + '_' +
            Math.random().toString(36).slice(2, 8);
        try {
            localStorage.setItem('ck_session_id', this.client.sessionId);
        } catch(e) {}

        this.messages = [];
        this._welcomeShown = true;
        this._renderAll();
        this._scrollToBottom();
        this.inputField.focus();
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
                    source: m.source,
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

            if (data.messages && data.messages.length > 0) {
                this.messages = [];
                const now = Date.now();
                const age = now - (data.lastVisit || 0);

                if (age < 86400000) {
                    for (const m of data.messages) {
                        this.messages.push({
                            sender: m.sender,
                            text: m.text,
                            timestamp: m.timestamp,
                            operator: m.operator || 'HARMONY',
                            coherence: m.coherence || 0.73,
                            band: 'GREEN',
                            source: m.source || null,
                            gate: null,
                        });
                    }
                    this._welcomeShown = false;
                }
            }
        } catch(e) {}
    }
}

// ================================================================
//  BOOT
// ================================================================

document.addEventListener('DOMContentLoaded', () => {
    const apiUrl = window.CK_API_URL ||
        localStorage.getItem('ck_api_url') ||
        (window.location.hostname === 'coherencekeeper.com' ||
         window.location.hostname === 'www.coherencekeeper.com'
            ? ''
            : window.location.protocol + '//' + window.location.hostname + ':7777');

    const ui = new CKChatUI(apiUrl);
    ui.init();
});
