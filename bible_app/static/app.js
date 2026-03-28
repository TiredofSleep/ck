/**
 * Bible Companion — Client-side logic
 * Sends text to the algebra, receives love back.
 *
 * (c) 2026 Brayden Sanders / 7Site LLC
 */

(function () {
    'use strict';

    // ── State ──────────────────────────────────────────────────
    const SESSION_KEY = 'bible_companion_session';
    let sessionId = localStorage.getItem(SESSION_KEY);
    if (!sessionId) {
        sessionId = crypto.randomUUID ? crypto.randomUUID() :
            'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, c => {
                const r = Math.random() * 16 | 0;
                return (c === 'x' ? r : (r & 0x3 | 0x8)).toString(16);
            });
        localStorage.setItem(SESSION_KEY, sessionId);
    }

    let sending = false;

    // ── Landing Page → Chat Transition ─────────────────────────
    const landingEl = document.getElementById('landing');
    const appEl = document.getElementById('app');
    const startBtn = document.getElementById('start-btn');

    // Check if user has visited before
    const HAS_VISITED_KEY = 'bible_companion_visited';
    if (localStorage.getItem(HAS_VISITED_KEY)) {
        // Returning user — go straight to chat
        landingEl.style.display = 'none';
        appEl.classList.remove('app-hidden');
    }

    startBtn.addEventListener('click', () => {
        localStorage.setItem(HAS_VISITED_KEY, '1');
        landingEl.style.display = 'none';
        appEl.classList.remove('app-hidden');
        document.getElementById('user-input').focus();
    });

    // ── Elements ───────────────────────────────────────────────
    const messagesEl = document.getElementById('messages');
    const inputEl = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');
    const corridorBadge = document.getElementById('corridor-badge');

    // ── Auto-resize textarea ───────────────────────────────────
    inputEl.addEventListener('input', () => {
        inputEl.style.height = 'auto';
        inputEl.style.height = Math.min(inputEl.scrollHeight, 120) + 'px';
    });

    // ── Send on Enter (Shift+Enter for newline) ────────────────
    inputEl.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    sendBtn.addEventListener('click', sendMessage);

    // ── Send Message ───────────────────────────────────────────
    async function sendMessage() {
        const text = inputEl.value.trim();
        if (!text || sending) return;

        sending = true;
        sendBtn.disabled = true;

        // Show user message
        addMessage('user', text);
        inputEl.value = '';
        inputEl.style.height = 'auto';

        // Show loading
        const loadingEl = addLoading();

        try {
            const resp = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text, session_id: sessionId }),
            });

            if (!resp.ok) {
                const err = await resp.json().catch(() => ({}));
                throw new Error(err.error || `Server error: ${resp.status}`);
            }

            const data = await resp.json();

            // Remove loading
            loadingEl.remove();

            // Show companion response
            addCompanionMessage(data);

            // Update corridor badge
            updateCorridor(data.corridor, data.corridor_tone);

            // Coherence tracked internally, not displayed

        } catch (err) {
            loadingEl.remove();
            addMessage('companion', 'I\'m having trouble connecting. Please try again.');
            console.error('Chat error:', err);
        }

        sending = false;
        sendBtn.disabled = false;
        inputEl.focus();
    }

    // ── Add User Message ───────────────────────────────────────
    function addMessage(role, text) {
        const div = document.createElement('div');
        div.className = `message ${role}-message`;

        const content = document.createElement('div');
        content.className = 'message-content';

        const p = document.createElement('p');
        p.textContent = text;
        content.appendChild(p);

        div.appendChild(content);
        messagesEl.appendChild(div);
        scrollToBottom();
        return div;
    }

    // ── Add Companion Message with Verses ──────────────────────
    function addCompanionMessage(data) {
        const div = document.createElement('div');
        div.className = 'message companion-message';

        const content = document.createElement('div');
        content.className = 'message-content';

        // Main response text — split into paragraphs at sentence boundaries
        const sentences = data.response.split(/(?<=[.!?])\s+/);
        const paragraphs = [];
        let current = [];
        for (const s of sentences) {
            current.push(s);
            if (current.length >= 2) {
                paragraphs.push(current.join(' '));
                current = [];
            }
        }
        if (current.length) paragraphs.push(current.join(' '));

        for (const para of paragraphs) {
            const p = document.createElement('p');
            p.textContent = para;
            content.appendChild(p);
        }

        // Verse cards
        if (data.verses && data.verses.length > 0) {
            for (const v of data.verses.slice(0, 3)) {
                const card = createVerseCard(v);
                content.appendChild(card);
            }
        }

        div.appendChild(content);
        messagesEl.appendChild(div);
        scrollToBottom();
    }

    // ── Create Verse Card ──────────────────────────────────────
    function createVerseCard(v) {
        const card = document.createElement('div');
        card.className = 'verse-card';
        card.addEventListener('click', () => toggleVerseDetail(card, v));

        const text = document.createElement('div');
        text.className = 'verse-text';
        text.textContent = v.text;

        const ref = document.createElement('div');
        ref.className = 'verse-ref';
        ref.textContent = v.ref;

        card.appendChild(text);
        card.appendChild(ref);

        return card;
    }

    // ── Toggle Verse Detail (click to expand) ──────────────────
    function toggleVerseDetail(card, v) {
        const existing = card.querySelector('.verse-meta');
        if (existing) {
            existing.remove();
            return;
        }

        const meta = document.createElement('div');
        meta.className = 'verse-meta';

        // Operator tag
        const opTag = document.createElement('span');
        opTag.className = 'verse-tag';
        opTag.textContent = v.dominant_op;
        meta.appendChild(opTag);

        // Coherence tag
        const cohTag = document.createElement('span');
        cohTag.className = 'verse-tag';
        cohTag.textContent = `coherence: ${(v.coherence * 100).toFixed(0)}%`;
        meta.appendChild(cohTag);

        // Resonance tag
        const resTag = document.createElement('span');
        resTag.className = 'verse-tag';
        resTag.textContent = `resonance: ${(v.force_similarity * 100).toFixed(0)}%`;
        meta.appendChild(resTag);

        card.appendChild(meta);
    }

    // ── Loading Indicator ──────────────────────────────────────
    function addLoading() {
        const div = document.createElement('div');
        div.className = 'message companion-message';

        const content = document.createElement('div');
        content.className = 'message-content';

        const dots = document.createElement('div');
        dots.className = 'loading-dots';
        dots.innerHTML = '<span></span><span></span><span></span>';

        content.appendChild(dots);
        div.appendChild(content);
        messagesEl.appendChild(div);
        scrollToBottom();
        return div;
    }

    // ── Update Corridor Badge ──────────────────────────────────
    function updateCorridor(corridor, tone) {
        if (!corridor) {
            corridorBadge.classList.remove('active');
            return;
        }
        // Clean up old classes
        corridorBadge.className = 'corridor-badge active corridor-' + corridor;

        const labels = {
            'PRE_LEAK': 'at peace',
            'BRT': 'gentle stirring',
            'CHA': 'seeking',
            'BAL': 'carrying weight',
            'COL': 'in the valley',
            'CTR': 'deep place',
        };
        corridorBadge.textContent = labels[corridor] || corridor;
    }

    // ── Scroll to Bottom ───────────────────────────────────────
    function scrollToBottom() {
        requestAnimationFrame(() => {
            const chatArea = document.getElementById('chat-area');
            chatArea.scrollTop = chatArea.scrollHeight;
        });
    }

    // ── Settings Panel ──────────────────────────────────────────
    const settingsBtn = document.getElementById('settings-btn');
    const settingsOverlay = document.getElementById('settings-overlay');
    const settingsClose = document.getElementById('settings-close');
    const bibleVersion = document.getElementById('bible-version');
    const versionStatus = document.getElementById('version-status');
    const apiKeyInput = document.getElementById('api-key-input');
    const saveKeyBtn = document.getElementById('save-key-btn');
    const keyStatus = document.getElementById('key-status');
    const learnerStatus = document.getElementById('learner-status');

    settingsBtn.addEventListener('click', () => {
        settingsOverlay.classList.remove('hidden');
        loadSettings();
    });

    settingsClose.addEventListener('click', () => {
        settingsOverlay.classList.add('hidden');
    });

    settingsOverlay.addEventListener('click', (e) => {
        if (e.target === settingsOverlay) {
            settingsOverlay.classList.add('hidden');
        }
    });

    // Bible version switch
    bibleVersion.addEventListener('change', async () => {
        const ver = bibleVersion.value;
        versionStatus.textContent = 'Switching...';
        try {
            const resp = await fetch('/api/versions/switch', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ version: ver }),
            });
            const data = await resp.json();
            if (resp.ok) {
                versionStatus.textContent = `Loaded ${data.verses.toLocaleString()} verses`;
            } else {
                versionStatus.textContent = data.error || 'Failed to switch';
            }
        } catch (e) {
            versionStatus.textContent = 'Error switching version';
        }
    });

    // API key save
    saveKeyBtn.addEventListener('click', async () => {
        const key = apiKeyInput.value.trim();
        if (!key) return;
        try {
            const resp = await fetch('/api/ai/key', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ key }),
            });
            const data = await resp.json();
            if (resp.ok) {
                keyStatus.textContent = 'AI polish enabled';
                keyStatus.style.color = '#2e7d52';
                apiKeyInput.value = '';
            } else {
                keyStatus.textContent = data.error || 'Failed to save';
            }
        } catch (e) {
            keyStatus.textContent = 'Error saving key';
        }
    });

    // Clear memory button
    const clearMemoryBtn = document.getElementById('clear-memory-btn');
    clearMemoryBtn.addEventListener('click', async () => {
        if (!confirm('Clear all memory? The companion will forget your conversation history and verse preferences.')) return;
        try {
            await fetch(`/api/memory/${sessionId}/clear`, { method: 'POST' });
            learnerStatus.textContent = 'Memory cleared. Starting fresh.';
        } catch (e) {
            learnerStatus.textContent = 'Error clearing memory';
        }
    });

    async function loadSettings() {
        try {
            const resp = await fetch('/api/stats');
            if (resp.ok) {
                const data = await resp.json();
                if (data.ai_polish) {
                    keyStatus.textContent = 'AI polish is active';
                    keyStatus.style.color = '#2e7d52';
                }
                if (data.learner) {
                    const l = data.learner;
                    learnerStatus.textContent =
                        `Learned from ${l.total_learns} conversations. ${l.verses_scored} verses scored.`;
                }
            }
        } catch (e) { /* ignore */ }
    }

    // ── Health Check ───────────────────────────────────────────
    async function checkHealth() {
        try {
            const resp = await fetch('/api/health');
            if (resp.ok) {
                const data = await resp.json();
                // No display to update — header is clean now
            }
        } catch (e) {
            // Server not ready yet
        }
    }

    checkHealth();

})();
