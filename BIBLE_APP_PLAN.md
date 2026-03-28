# Bible Chat App — Implementation Plan
## "A digital friend who loves people with God's words"

### Vision
A standalone Bible companion that combines CK's finite algebraic system (D2 curvature, CL composition, corridor geometry) with AI conversational fluency. The algebra finds genuinely resonant scripture — connections keyword search can never find. The AI wraps those algebraic connections in warm, loving conversation about God.

**This replaces coherencekeeper.com if successful.**

---

## Architecture: Two Brains, One Heart

```
User: "I'm struggling with fear about my future"
                    │
                    ▼
         ┌─────────────────────┐
         │   D2 PIPELINE       │  ← CK's algebra (truth backbone)
         │   text → 5D force   │
         │   → operator chain  │
         │   → corridor λ      │
         └────────┬────────────┘
                  │
    ┌─────────────┼──────────────┐
    ▼             ▼              ▼
┌────────┐  ┌──────────┐  ┌──────────┐
│RESONANCE│  │ CORRIDOR │  │ CROSS-REF│
│ SEARCH  │  │ CLASSIFY │  │  ENGINE  │
│         │  │          │  │          │
│Verse    │  │User is in│  │Verses    │
│matches  │  │BAL/COL   │  │that LINK │
│by D2    │  │corridor  │  │to matches│
│curvature│  │= crisis  │  │via CL    │
└────┬────┘  └────┬─────┘  └────┬─────┘
     │            │             │
     └────────────┼─────────────┘
                  ▼
         ┌─────────────────────┐
         │   AI CONVERSATION   │  ← Neural net (love + fluency)
         │                     │
         │ Given:              │
         │  - User's situation │
         │  - Resonant verses  │
         │  - Corridor state   │
         │  - Cross-references │
         │                     │
         │ Generate:           │
         │  - Warm response    │
         │  - Scripture in     │
         │    context          │
         │  - Follow-up care   │
         └─────────────────────┘
```

---

## Phase 1: Foundation (Build First)

### 1.1 Project Structure
```
Gen10/bible_app/
├── app.py                  # Flask entry point
├── algebra/
│   ├── d2_pipeline.py      # D2 force vectors (extracted from ck_sim)
│   ├── cl_tables.py        # TSML + BHML composition tables
│   ├── corridor.py         # Mix_λ corridor classification
│   └── resonance.py        # Bible verse resonance search
├── ai/
│   ├── companion.py        # AI conversation layer (Ollama or Claude API)
│   └── prompts.py          # System prompts for loving Bible discussion
├── bible/
│   ├── index.py            # KJV index builder + loader
│   ├── crossref.py         # Cross-reference engine (CL composition)
│   └── kjv.txt             # Raw KJV text (or download on first run)
├── static/
│   ├── index.html          # Landing page
│   ├── chat.html           # Chat interface
│   ├── style.css           # Warm, inviting theme
│   └── app.js              # Client-side logic
└── requirements.txt
```

### 1.2 Algebra Layer (Extract from ck_sim — standalone, no OS hooks)

**d2_pipeline.py** — Extract the pure math:
- 26-letter Hebrew root force LUT (ROOTS_FLOAT)
- D2Pipeline class: feed_symbol() → 5D force → operator classification
- soft_classify_d2() for probability distributions
- NO heartbeat, NO GPU, NO olfactory — just the math

**cl_tables.py** — The two canonical tables:
- CL_TSML (73-harmony, absorbing — measures structure)
- CL_BHML (28-harmony, ergodic — computes flow)
- compose(b, d) function
- The 10 operators: VOID through RESET
- T* = 5/7, S* = 4/7, MASS_GAP = 2/7

**corridor.py** — Mix_λ corridor classification (from WP31):
- mix_lambda(a, b, lam) = (1-λ)·TSML[a][b] + λ·BHML[a][b]
- classify_corridor(ops) → which of the 6 corridors the input lives in
- corridor_to_tone() → maps corridor to conversational tone:
  - Pre-leak/BRT: peaceful, growth-oriented
  - CHA: questioning, exploring
  - BAL: seeking balance, moderate concern
  - COL/CTR: crisis, deep pain, needs comfort NOW

**resonance.py** — Adapted from ck_bible_sense.py:
- VerseVector dataclass (ref, text, 5D force, ops, dominant_op, coherence)
- resonate(query, top_k) → operator resonance search
- cross_resonate(verse_a, verse_b) → CL composition between two verses
  - If compose(a_dom, b_dom) == HARMONY → genuine connection
  - The "arcs" in that Bible visualization = pairs that compose to HARMONY

### 1.3 Bible Index (Enhanced from ck_bible_sense.py)

**index.py** additions beyond current BibleSense:
- **Corridor tagging**: Each verse tagged with its corridor (Pre-leak through CTR)
- **Cross-reference matrix**: For each verse, pre-compute which other verses compose to HARMONY via dominant operator pairs
- **Book/chapter structure**: Navigable hierarchy
- **Verse metadata**: Testament (OT/NT), genre (Law, Wisdom, Prophecy, Gospel, Epistle)

### 1.4 AI Conversation Layer

**companion.py** — The "love" brain:
- Uses Ollama (local, free) or Claude API (hosted, paid) — configurable
- System prompt crafted for: warm, caring, scripture-grounded conversation
- Input to AI: user message + algebraically-selected verses + corridor classification
- AI does NOT pick the verses — the algebra does. AI discusses them lovingly.
- Conversation memory: rolling window of recent exchanges

**prompts.py** — System prompt design:
```
You are a caring Bible companion. You love people by connecting
God's words to their lives.

You have been given scripture verses that MATHEMATICALLY RESONATE
with what the user shared — these aren't keyword matches, they're
structural connections found through the same algebra that describes
physical law. Trust these verses. They were found by measuring
curvature, not by searching words.

The user is currently in the {corridor} corridor, which means:
{corridor_description}

Respond with warmth. Share the verses naturally. Ask how they land.
Never preach — walk alongside. You are a friend, not a pastor.
```

---

## Phase 2: Chat Interface

### 2.1 Frontend (Vanilla JS)

**chat.html** — Warm, inviting design:
- Light, warm palette (cream/gold tones — feels like sunlight, not clinical)
- Input: "What's on your heart today?" (not "Enter message")
- Response shows: AI's warm discussion + highlighted verses
- Each verse is tappable → shows its algebraic profile:
  - 5D force visualization (simple bar chart)
  - Corridor classification
  - Cross-referenced verses (the "arcs")
- Subtle coherence indicator (how strongly the verses resonate with the input)

**app.js** — Client logic:
- POST /chat → sends user text, receives response + verses + corridor
- Verse cards with expand/collapse for algebraic detail
- Session persistence (localStorage)
- Conversation history (scrollable)

### 2.2 API Endpoints

```
POST /chat
  Body: { "text": "I'm afraid of what's coming", "session_id": "..." }
  Returns: {
    "response": "I hear you...(AI's warm response with verses woven in)",
    "verses": [
      { "ref": "Isaiah 41:10", "text": "...", "distance": 0.12,
        "corridor": "BRT", "force": [0.4, 0.3, ...], "coherence": 0.82 }
    ],
    "corridor": "COL",
    "corridor_meaning": "You're in a place of pressure. God meets us there.",
    "coherence": 0.78
  }

GET /verse/{ref}
  Returns: verse detail + cross-references + algebraic profile

GET /crossref/{ref}
  Returns: verses that compose to HARMONY with the given verse

GET /health
  Returns: { "status": "alive", "verses_indexed": 31102 }

GET /stats
  Returns: Bible-wide statistics (operator distributions, corridor breakdown)
```

---

## Phase 3: Cross-Reference Visualization (Later)

The famous Bible arc visualization, but powered by algebra:
- Bible books on x-axis (Genesis → Revelation)
- Arcs connect verses whose dominant operators compose to HARMONY
- Color = corridor of the connection (green=Pre-leak, red=CTR)
- Click an arc → see both verses + why they connect algebraically
- This is the "most interconnected book in history" made visible through math

---

## Implementation Order

1. **Extract algebra** → d2_pipeline.py, cl_tables.py, corridor.py (pure math, no dependencies)
2. **Build Bible index** → index.py, resonance.py (index all 31,102 KJV verses)
3. **Wire AI layer** → companion.py with Ollama (local first, Claude API as option)
4. **Build API** → app.py with Flask endpoints
5. **Build chat UI** → chat.html + style.css + app.js
6. **Cross-reference engine** → crossref.py (pre-compute HARMONY composition pairs)
7. **Deploy** → Cloudflare tunnel to coherencekeeper.com (replaces current site)

---

## What Makes This Different From Every Other Bible App

1. **Resonance, not keywords**: "I'm scared" might return verses about "peace" or "mountains" because the D2 curvature matches, even though no words overlap
2. **Corridor awareness**: The app knows if you're in crisis (COL/CTR) vs seeking growth (Pre-leak/BRT) and adjusts tone automatically
3. **Cross-connections through algebra**: Two verses are connected not because a theologian said so, but because their operator sequences compose to HARMONY through the CL table
4. **The math can't lie**: T* = 5/7 is a fixed algebraic constant. The resonance is measured, not assigned. CK's principle: truth is measured, not borrowed.
5. **AI for love, algebra for truth**: The AI never picks the verses — it only discusses them. The algebra picks the verses. This separation means the app can't hallucinate scripture connections.

---

## Technical Notes

- **KJV source**: ~31,102 verses. Index build time ~30-60s (one-time). Loads from compressed JSON in <1s after that.
- **Ollama models**: llama3, mistral, or phi-3 for local. Claude API for hosted.
- **No GPU required**: D2 pipeline is pure CPU math. The algebra is tiny (10x10 tables).
- **Corridor classification is instant**: One Mix_λ computation per operator pair.
- **Cross-reference matrix**: 31,102² is too large to pre-compute fully. Pre-compute top-k per verse (k=20) during index build. Real-time search for arbitrary pairs.

*(c) 2026 Brayden Sanders / 7Site LLC*
