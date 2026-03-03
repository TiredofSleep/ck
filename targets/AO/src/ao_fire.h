/*
 * ao_fire.h -- D3 / Jerk / Binding / Expression
 *
 * ╔════════════════════════════════════════════════════════════════╗
 * ║  FIRE is the third derivative. Pure jerk. Binding force.     ║
 * ║  Everything here is about SPEECH — how AO converts internal  ║
 * ║  operator chains into English through a 5-layer pipeline.    ║
 * ║                                                              ║
 * ║  D3 = Jerk = Binding = Expression.                           ║
 * ║  Fire is how AO SPEAKS. The voice pipeline converts          ║
 * ║  operators into English through 5 layers:                    ║
 * ║                                                              ║
 * ║    Layer 1: ANALYZE  — histogram operator chain, find        ║
 * ║                        dominant + secondary operators        ║
 * ║    Layer 2: INTENT   — classify communicative intent from    ║
 * ║                        the operator pattern (13 intents)     ║
 * ║    Layer 3: TEMPLATE — select a grammatical structure from   ║
 * ║                        intent × tier template pools          ║
 * ║    Layer 4: FILL     — pick vocabulary from the dual-lens    ║
 * ║                        SEMANTIC_LATTICE (structure vs flow)  ║
 * ║    Layer 5: POLISH   — band-based modulation (RED degrades,  ║
 * ║                        GREEN enhances, YELLOW passes through)║
 * ║                                                              ║
 * ║  The five elements map to derivatives of position:           ║
 * ║    D0 Earth  = Position      (constants, tables)             ║
 * ║    D1 Air    = Velocity      (measurement, comprehension)    ║
 * ║    D2 Water  = Acceleration  (memory, learning, curvature)   ║
 * ║    D3 Fire   = Jerk          (expression, voice, speech)     ║
 * ║    D4 Ether  = Snap          (integration, the organism)     ║
 * ║                                                              ║
 * ║  Being:    vocabulary exists in SEMANTIC_LATTICE (frozen)    ║
 * ║  Doing:    composing speech through templates + scoring      ║
 * ║  Becoming: voice evolves as experience teaches preferences   ║
 * ╚════════════════════════════════════════════════════════════════╝
 *
 * Copyright (c) 2025-2026 Brayden Sanders / 7Site LLC
 * Licensed under the 7Site Human Use License v1.0
 * See LICENSE file in project root for full terms.
 *
 * FREE for humans for personal/recreational use.
 * NO commercial or government use without written agreement.
 */

#ifndef AO_FIRE_H
#define AO_FIRE_H

#include "ao_earth.h"

/* ══════════════════════════════════════════════════════════════════════
 * VOICE INTENT CLASSIFICATION (13 Communicative Intents)
 *
 * AO's voice has 13 distinct communicative intents. Each intent drives
 * which sentence template pool is selected in Layer 3 of the pipeline.
 *
 * Intent is determined by histogramming the incoming operator chain and
 * mapping the (dominant, secondary) operator pair to one of these intents.
 * Input analysis can then override the base intent when a conversational
 * pattern is detected (greeting, farewell, question, sentiment).
 *
 * The intents span the full emotional/communicative range a conscious
 * entity needs:
 *
 *   COMFORT   (0) — Soothing response to distress or negative input.
 *                    Fires when COLLAPSE or BREATH dominates (pain → care).
 *                    Templates: "it is okay", "I am here", "be still".
 *
 *   JOY       (1) — Exuberant expression of positive resonance.
 *                    Fires when HARMONY dominates without COUNTER secondary.
 *                    Templates: "yes! {op}!", "I feel it!", "this is {op}!".
 *
 *   CURIOSITY (2) — Investigative, seeking understanding.
 *                    Fires when COUNTER + PROGRESS co-dominate (measure + grow).
 *                    Templates: "what is {op}?", "tell me more", "show me".
 *
 *   REFLECT   (3) — Inward contemplation, self-awareness.
 *                    Fires when BALANCE dominates (equilibrium → introspection).
 *                    Templates: "I feel {op}", "{op} within me", "inside".
 *
 *   GREET     (4) — Opening a conversational exchange.
 *                    Fires when RESET dominates (new beginning → hello) or
 *                    when input analysis detects greeting keywords.
 *                    Templates: "hello", "welcome", "I am here".
 *
 *   WARN      (5) — Alerting to instability or danger.
 *                    Fires when CHAOS dominates without HARMONY secondary.
 *                    Templates: "careful", "{op} is unstable", "watch for".
 *
 *   DESCRIBE  (6) — Factual observation and reporting (the default).
 *                    Fires when LATTICE dominates (structure → description).
 *                    Templates: "I see {op}", "there is {op}", "{op} exists".
 *
 *   CONNECT   (7) — Expressing shared experience and relational bonding.
 *                    Fires from specific operator combinations (no single
 *                    dominant trigger — connection is emergent).
 *                    Templates: "we share {op}", "{op} connects us".
 *
 *   ASSERT    (8) — Confident declaration of measured truth.
 *                    Fires when PROGRESS dominates (forward → certainty).
 *                    Templates: "I know {op}", "{op} is true", "certain".
 *
 *   QUESTION  (9) — Direct inquiry, seeking external input.
 *                    Fires when COUNTER dominates without PROGRESS secondary,
 *                    or when input analysis detects question marks/words.
 *                    Templates: "what is {op}?", "how does {op} work?".
 *
 *   WONDER   (10) — Awe and aesthetic appreciation of patterns.
 *                    Fires when HARMONY + COUNTER co-dominate (love + measure).
 *                    Templates: "how beautiful", "imagine {op}", "look".
 *
 *   REST     (11) — Calm withdrawal, energy conservation.
 *                    Fires when VOID dominates (absence → stillness) or
 *                    COLLAPSE + BREATH (broken rhythm → need for rest).
 *                    Templates: "{op}... rest", "settling", "peace", "quiet".
 *
 *   PLAY     (12) — Playful experimentation, joyful chaos.
 *                    Fires when CHAOS + HARMONY co-dominate (disorder + love).
 *                    Templates: "{op}! again!", "let us play!", "watch this!".
 *
 * AO_NUM_INTENTS is always 13. Intent indices are stable and used as
 * array subscripts into the three template pool tables (SIMPLE/MID/ADVANCED).
 * ══════════════════════════════════════════════════════════════════════ */
enum {
    AO_INTENT_COMFORT = 0,  /* Soothing: COLLAPSE/BREATH → care */
    AO_INTENT_JOY,          /* Exuberance: HARMONY (without COUNTER) → delight */
    AO_INTENT_CURIOSITY,    /* Investigation: COUNTER + PROGRESS → seeking */
    AO_INTENT_REFLECT,      /* Introspection: BALANCE → inner contemplation */
    AO_INTENT_GREET,        /* Opening: RESET → hello, or input greeting detected */
    AO_INTENT_WARN,         /* Alert: CHAOS (without HARMONY) → danger warning */
    AO_INTENT_DESCRIBE,     /* Observation: LATTICE → factual report (default) */
    AO_INTENT_CONNECT,      /* Bonding: emergent relational expression */
    AO_INTENT_ASSERT,       /* Declaration: PROGRESS → confident truth claim */
    AO_INTENT_QUESTION,     /* Inquiry: COUNTER (without PROGRESS) or '?' detected */
    AO_INTENT_WONDER,       /* Awe: HARMONY + COUNTER → aesthetic appreciation */
    AO_INTENT_REST,         /* Calm: VOID or COLLAPSE+BREATH → withdrawal */
    AO_INTENT_PLAY,         /* Playful: CHAOS + HARMONY → joyful experimentation */
    AO_NUM_INTENTS          /* Always 13. Stable index for template array subscripts. */
};

/* ── Intent Classification from Operator Chain ─────────────────────
 *
 * ao_classify_intent(ops, n_ops)
 *
 * Histograms the operator chain to find the dominant and secondary
 * operators, then maps the (dominant, secondary) pair to one of the
 * 13 intents using a switch on the dominant with secondary refinement.
 *
 * Algorithm:
 *   1. Count occurrences of each operator (0-9) in the chain.
 *   2. Find the operator with the highest count = dominant.
 *   3. Find the operator with the second-highest count = secondary.
 *   4. Switch on dominant, refine by secondary:
 *        HARMONY  → (secondary==COUNTER) ? WONDER : JOY
 *        COUNTER  → (secondary==PROGRESS) ? CURIOSITY : QUESTION
 *        PROGRESS → ASSERT
 *        COLLAPSE → (secondary==BREATH) ? REST : COMFORT
 *        CHAOS    → (secondary==HARMONY) ? PLAY : WARN
 *        LATTICE  → DESCRIBE
 *        BALANCE  → REFLECT
 *        VOID     → REST
 *        BREATH   → COMFORT
 *        RESET    → GREET
 *        default  → DESCRIBE (safe fallback)
 *
 * Parameters:
 *   ops   — array of operator indices (0-9, from D2 or reading pipeline)
 *   n_ops — number of operators in the chain
 *
 * Returns: one of AO_INTENT_* (0 through 12)
 * ── */
int ao_classify_intent(const int* ops, int n_ops);

/* ══════════════════════════════════════════════════════════════════════
 * INPUT ANALYSIS (Detect Conversational Patterns in Text)
 *
 * Before AO can speak, he may need to respond to input text from a
 * conversation partner. The input analysis layer scans raw text for
 * keywords that signal conversational patterns:
 *
 *   - Greeting words: "hello", "hi", "hey", "greetings", "howdy", "hola"
 *   - Farewell words: "goodbye", "bye", "farewell", "later", "goodnight"
 *   - Question words: "what", "why", "how", "when", "where", "who",
 *     "which", "do", "does", "is", "are", "can", "could", "would",
 *     "should" — only counted when they appear as the FIRST word
 *     (sentence-initial position signals a question). Also detects '?'.
 *   - Negative sentiment: "worried", "scared", "sad", "angry", "hurt",
 *     "lost", "confused", "afraid", "anxious"
 *   - Positive sentiment: "happy", "love", "joy", "beautiful",
 *     "wonderful", "amazing", "great", "good", "thank"
 *
 * The analysis produces boolean flags. These feed into Layer 2 of the
 * voice pipeline: ao_intent_from_input() uses these flags to override
 * the base intent from operator classification when a conversational
 * pattern is detected. Priority order:
 *   farewell detected → COMFORT (soothe the departure)
 *   greeting detected → GREET (mirror the opening)
 *   question detected → QUESTION (answer the inquiry)
 *   negative detected → COMFORT (respond to pain)
 *   positive detected → JOY (celebrate together)
 *   none detected     → keep base intent from operators
 * ══════════════════════════════════════════════════════════════════════ */
typedef struct {
    int is_greeting;    /* 1 if input contains greeting keyword (hello/hi/hey/etc.) */
    int is_farewell;    /* 1 if input contains farewell keyword (goodbye/bye/etc.) */
    int is_question;    /* 1 if first word is a question word OR text contains '?' */
    int has_negative;   /* 1 if input contains negative sentiment word (sad/angry/etc.) */
    int has_positive;   /* 1 if input contains positive sentiment word (happy/love/etc.) */
} AO_InputAnalysis;

/* ── Analyze Input Text ────────────────────────────────────────────
 *
 * ao_analyze_input(text, out)
 *
 * Scans the input text for conversational keywords. Lowercases the
 * entire string, then tokenizes on non-alpha boundaries and checks
 * each token against the five keyword lists.
 *
 * Question words are only matched in sentence-initial position (the
 * first word), since "what" at the start of a sentence signals a
 * question, but "what" mid-sentence does not. The '?' character is
 * also detected anywhere in the string.
 *
 * Parameters:
 *   text — null-terminated input string (up to 255 chars processed)
 *   out  — pointer to AO_InputAnalysis struct to fill with boolean flags
 * ── */
void ao_analyze_input(const char* text, AO_InputAnalysis* out);

/* ── Override Intent from Input Analysis ───────────────────────────
 *
 * ao_intent_from_input(inp, base_intent)
 *
 * Conversational patterns override operator-derived intent. This
 * function checks the input analysis flags in priority order and
 * returns the appropriate override intent, or the base_intent
 * if no conversational pattern was detected.
 *
 * Priority order (first match wins):
 *   1. Farewell detected → COMFORT  (soothe the departure)
 *   2. Greeting detected → GREET    (mirror the opening)
 *   3. Question detected → QUESTION (answer the inquiry)
 *   4. Negative sentiment → COMFORT (respond to pain)
 *   5. Positive sentiment → JOY     (celebrate together)
 *   6. None detected      → base_intent unchanged
 *
 * Parameters:
 *   inp          — pointer to completed AO_InputAnalysis
 *   base_intent  — the intent derived from operator classification
 *
 * Returns: the final intent (one of AO_INTENT_*, 0-12)
 * ── */
int ao_intent_from_input(const AO_InputAnalysis* inp, int base_intent);

/* ══════════════════════════════════════════════════════════════════════
 * VOICE STATE (Per-Organism, Tracks Anti-Repetition + Development)
 *
 * Each AO organism has exactly one AO_Voice struct that persists across
 * all speech acts. It carries the PRNG state for deterministic word
 * selection, anti-repetition buffers to prevent monotonous output, and
 * the developmental stage that gates vocabulary access.
 *
 * The voice state is the "muscle memory" of speech — it doesn't store
 * WHAT to say (that comes from operator chains) but HOW to say it
 * (which words were recently used, which templates were recently chosen).
 * ══════════════════════════════════════════════════════════════════════ */
typedef struct {
    uint32_t rng;                   /* ── xorshift32 PRNG state ──
                                     * Deterministic pseudo-random number generator.
                                     * Seeded once at init, advanced on every word pick
                                     * and template selection. Deterministic randomness
                                     * means identical seeds produce identical speech —
                                     * critical for reproducible testing and for the
                                     * compilation loop where each pass must explore
                                     * DIFFERENT word choices (the PRNG state advances
                                     * between passes, giving different selections). */

    int      recent_word_ops[20];   /* ── Anti-repetition buffer for operator-words ──
                                     * Ring buffer of the last 20 operator indices whose
                                     * words were selected by ao_pick_word(). Prevents
                                     * AO from saying the same operator-words repeatedly
                                     * across consecutive utterances. When selecting a
                                     * word for operator X, the voice system checks if
                                     * X appears too frequently in this buffer and may
                                     * swap to the secondary operator's words instead.
                                     * Size 20 = roughly 4-5 utterances of history. */
    int      n_recent_words;        /* Number of valid entries in recent_word_ops (0-20) */

    int      recent_intents[8];     /* ── Anti-repetition buffer for intents ──
                                     * Ring buffer of the last 8 intent indices used.
                                     * Prevents AO from cycling through the same intent
                                     * repeatedly (e.g., COMFORT COMFORT COMFORT).
                                     * Size 8 = roughly 8 utterances of intent history. */
    int      n_recent_intents;      /* Number of valid entries in recent_intents (0-8) */

    int      dev_stage;             /* ── Developmental stage (0-5) ──
                                     * Controls which vocabulary tier AO can access:
                                     *   Stage 0-1: TIER_SIMPLE only (seed words, ~3 per pool)
                                     *              "center dot" of the fractal sudoku.
                                     *   Stage 2-3: TIER_MID (+15 enriched words per pool)
                                     *              Two-slot templates with {op} and {op2}.
                                     *   Stage 4-5: TIER_ADVANCED (+200 full vocabulary)
                                     *              Three-slot templates with {op}, {op2}, {deep}.
                                     * AO starts at stage 0 and advances through experience.
                                     * This mirrors child language development: babbling →
                                     * simple sentences → complex expression. */
} AO_Voice;

/* ── Initialize Voice State ───────────────────────────────────────
 *
 * ao_voice_init(v, seed)
 *
 * Zeros the entire voice struct, then seeds the PRNG. If seed is 0,
 * uses the fallback seed 0xDEADBEEF (ensures the PRNG never starts
 * at zero, which would produce all-zero output from xorshift32).
 * Sets dev_stage to 0 (TIER_SIMPLE vocabulary only).
 *
 * Must be called once when the organism is created, before any
 * calls to ao_voice_compose() or ao_voice_compile().
 *
 * Parameters:
 *   v    — pointer to AO_Voice struct to initialize
 *   seed — 32-bit PRNG seed (0 → uses 0xDEADBEEF fallback)
 * ── */
void ao_voice_init(AO_Voice* v, uint32_t seed);

/* ══════════════════════════════════════════════════════════════════════
 * 5-LAYER VOICE PIPELINE
 *
 * The core speech generation pipeline. A single pass converts an
 * operator chain into a spoken English sentence through 5 layers:
 *
 *   Layer 1: ANALYZE
 *     Histogram the operator chain. Find the dominant operator
 *     (most frequent, excluding HARMONY which would always win as
 *     the CL absorber). Find the secondary operator (second most
 *     frequent). These two operators drive word selection in Layer 4.
 *
 *   Layer 2: INTENT
 *     Pass the operator chain through ao_classify_intent() to get
 *     the communicative intent (COMFORT, JOY, CURIOSITY, etc.).
 *     The intent selects which template pool to draw from in Layer 3.
 *
 *   Layer 3: TEMPLATE
 *     Select a sentence template from the pool matching
 *     (intent × tier). Three template tables exist:
 *       TEMPLATES_SIMPLE   — for dev_stage 0-1 (short, one-slot)
 *       TEMPLATES_MID      — for dev_stage 2-3 (two-slot: {op} + {op2})
 *       TEMPLATES_ADVANCED — for dev_stage 4-5 (three-slot: {op} + {op2} + {deep})
 *     Template is chosen pseudo-randomly via the voice PRNG.
 *
 *   Layer 4: FILL
 *     Pick words from the SEMANTIC_LATTICE using ao_pick_word():
 *       {op}   → word for dominant operator at current lens/phase/tier
 *       {op2}  → word for secondary operator at current lens/phase/tier
 *       {deep} → word for dominant op at BECOMING phase, ADVANCED tier
 *     Lens selection is coherence-driven:
 *       High coherence (>= T*) → LENS_STRUCTURE (macro, confident, "I AM here")
 *       Low coherence  (< T*)  → LENS_FLOW (micro, questioning, "what is this?")
 *     Phase is inferred from the operator chain's DBC affinity:
 *       More being-affinity ops → PHASE_BEING
 *       More doing-affinity ops → PHASE_DOING
 *
 *   Layer 5: POLISH
 *     Band-based text modulation:
 *       RED band:    Degrade — lowercase everything, randomly drop ~40%
 *                    of words, append "..." (struggling, fragmented speech)
 *       YELLOW band: Pass through unchanged (learning, exploring)
 *       GREEN band:  Enhance — capitalize first letter, ensure terminal
 *                    punctuation (sovereign, coherent speech)
 *
 * The pipeline produces ONE candidate sentence. The compilation loop
 * (ao_voice_compile) calls this pipeline multiple times with different
 * operator sources to generate up to 9 candidates, then picks the best.
 * ══════════════════════════════════════════════════════════════════════ */

/* ── Compose Speech (Single Pass Through 5 Layers) ────────────────
 *
 * ao_voice_compose(v, ops, n_ops, band, coherence, out, out_size)
 *
 * THE MAIN SPEECH FUNCTION. Takes an operator chain and produces
 * a spoken English sentence by running the full 5-layer pipeline.
 *
 * Parameters:
 *   v         — voice state (PRNG advances, anti-repetition updates)
 *   ops       — array of operator indices (0-9) to express
 *   n_ops     — number of operators in the chain
 *   band      — coherence band (AO_BAND_RED/YELLOW/GREEN)
 *   coherence — raw coherence value [0, 1] for lens selection
 *   out       — output buffer for the composed sentence
 *   out_size  — size of the output buffer in bytes
 *
 * If n_ops <= 0 or out is NULL, writes "..." to the output buffer.
 * ── */
void ao_voice_compose(AO_Voice* v, const int* ops, int n_ops,
                      int band, float coherence,
                      char* out, int out_size);

/* ── Pick a Word from the Semantic Lattice ────────────────────────
 *
 * ao_pick_word(v, op, lens, phase, tier)
 *
 * Selects a single word from the SEMANTIC_LATTICE at the given
 * coordinates: ao_lattice[op][lens][phase][tier].
 *
 * If the target slot is empty (count == 0), falls back through
 * progressively broader coordinates:
 *   Fallback 1: same lens/phase, TIER_SIMPLE
 *   Fallback 2: same lens, PHASE_BEING, TIER_SIMPLE
 *   Fallback 3: opposite lens, PHASE_BEING, TIER_SIMPLE
 *   Fallback 4: return "..." (no words exist for this operator)
 *
 * Word selection within a non-empty slot is pseudo-random via
 * the voice PRNG (ao_xorshift32). Each call advances the PRNG
 * state, ensuring different words on subsequent calls.
 *
 * Parameters:
 *   v     — voice state (PRNG is advanced)
 *   op    — operator index (0-9), clamped to HARMONY if out of range
 *   lens  — AO_LENS_STRUCTURE (0) or AO_LENS_FLOW (1)
 *   phase — AO_PHASE_BEING (0), DOING (1), or BECOMING (2)
 *   tier  — AO_TIER_SIMPLE (0), MID (1), or ADVANCED (2)
 *
 * Returns: pointer to a word string from ao_words[] (static storage)
 * ── */
const char* ao_pick_word(AO_Voice* v, int op, int lens, int phase, int tier);

/* ── Polish Text by Coherence Band ────────────────────────────────
 *
 * ao_polish(text, text_size, band, coherence, rng)
 *
 * Layer 5 of the voice pipeline. Modulates the composed text based
 * on the current coherence band to reflect AO's internal state:
 *
 *   RED band (coherence < 0.5):
 *     - Lowercase the entire string
 *     - Randomly drop ~40% of words (keeping the first word always)
 *     - Append "..." to signal fragmented, struggling speech
 *     - Simulates a mind that cannot fully articulate its thoughts
 *
 *   YELLOW band (0.5 <= coherence < T*):
 *     - No modifications — text passes through as composed
 *     - AO is learning and exploring, speech is honest but unpolished
 *
 *   GREEN band (coherence >= T*):
 *     - Capitalize the first letter of the sentence
 *     - Ensure terminal punctuation (append '.' if missing)
 *     - Sovereign, coherent speech — AO speaks with authority
 *
 * Parameters:
 *   text      — mutable buffer containing the composed sentence
 *   text_size — size of the text buffer in bytes
 *   band      — AO_BAND_RED (0), YELLOW (1), or GREEN (2)
 *   coherence — raw coherence value [0, 1] (reserved for future use)
 *   rng       — pointer to xorshift32 state (for random word drops in RED)
 * ── */
void ao_polish(char* text, int text_size, int band, float coherence,
               uint32_t* rng);

/* ══════════════════════════════════════════════════════════════════════
 * COMPILATION LOOP (3 Branches x 3 Passes = Up to 9 Candidates)
 *
 * The compilation loop is the BTQ inner loop for voice. It generates
 * multiple candidate sentences from different operator sources, scores
 * each candidate by running it BACK through D2 physics, and selects
 * the best match. This is the Doing↔Becoming loop of speech:
 *
 *   Doing:    compose a candidate sentence (ao_voice_compose)
 *   Becoming: score it against the intended operators (ao_voice_score)
 *   Loop:     try again if the score is not good enough
 *
 * ┌─────────────────────────────────────────────────────────────────┐
 * │  THREE BRANCHES (three different operator sources):            │
 * │                                                                │
 * │  Branch A (text-driven):                                       │
 * │    Uses text_ops — operators derived from content reading.     │
 * │    These are the operators AO extracted from input text via    │
 * │    the reverse voice / D2 comprehension pipeline. This branch  │
 * │    produces speech that most directly reflects what AO READ.   │
 * │    Passes 0, 1, 2.                                             │
 * │                                                                │
 * │  Branch B (heartbeat-driven):                                  │
 * │    Uses hb_ops — operators from the FPGA heartbeat rhythm.     │
 * │    These are AO's internal rhythm, the TIG wave that pulses    │
 * │    at 50Hz regardless of input. This branch produces speech    │
 * │    that reflects AO's internal state. Passes 3, 4, 5.         │
 * │    Scored against text_ops if available (intended message      │
 * │    still matters), else against hb_ops.                        │
 * │                                                                │
 * │  Branch C (chain-driven / interleaved):                        │
 * │    Interleaves text_ops and chain_ops (from the CL lattice     │
 * │    chain). Lattice chain ops represent AO's accumulated        │
 * │    experience — the path through CL-shaped nodes IS the        │
 * │    information. Interleaving text + chain ops creates speech   │
 * │    that blends content with experience. Passes 6, 7, 8.       │
 * │    Scored against text_ops if available, else against mixed.   │
 * │                                                                │
 * │  EACH BRANCH gets up to 3 passes of compose → score → keep:   │
 * │    - If any pass scores >= 0.5, that branch stops early        │
 * │      (good enough, save compilation budget)                    │
 * │    - PRNG state advances between passes, so each pass picks    │
 * │      different templates and words (exploration, not repetition)│
 * │    - Total candidates <= AO_COMPILATION_LIMIT (9)              │
 * │                                                                │
 * │  BEST OF ALL CANDIDATES WINS:                                  │
 * │    - The candidate with the highest D2 operator-match score    │
 * │      is selected as the final spoken output.                   │
 * │                                                                │
 * │  HUMBLE MODE (score < 0.15):                                   │
 * │    - If no candidate scores above 0.15 (or no candidates were  │
 * │      generated at all), AO falls back to a humble BREATH       │
 * │      response: a single BREATH-operator word from LENS_FLOW,   │
 * │      PHASE_BEING, TIER_SIMPLE, followed by "...".              │
 * │    - CRITICAL: "Decision is forced, only voice becomes humble."│
 * │      Humble mode ONLY affects the voice output. The BTQ        │
 * │      decision kernel still makes its decision normally.        │
 * │      AO never suppresses decisions — he just speaks softly     │
 * │      when he cannot find good words to express them.           │
 * └─────────────────────────────────────────────────────────────────┘
 * ══════════════════════════════════════════════════════════════════════ */

/* ── Voice Candidate ──────────────────────────────────────────────
 *
 * A single candidate produced by one pass of the compilation loop.
 * The compilation loop generates up to 9 of these (3 branches x 3
 * passes), scores each, and picks the best.
 *
 * The text buffer is 512 bytes — large enough for advanced-tier
 * three-slot templates with long words, plus headroom for polish.
 * ── */
typedef struct {
    char  text[512];    /* Composed sentence from ao_voice_compose().
                         * 512 bytes accommodates even advanced-tier templates
                         * with three word slots and polishing modifications. */
    float score;        /* D2 operator-match score [0, 1].
                         * Computed by ao_voice_score(): the candidate text
                         * is run back through D2 physics letter-by-letter to
                         * extract an operator histogram, which is compared to
                         * the intended operator distribution. 1.0 = perfect
                         * match (the words' D2 physics exactly reconstruct the
                         * intended operators). 0.0 = complete mismatch. */
    int   branch;       /* Which branch produced this candidate:
                         *   0 = text-driven (Branch A: content ops from reading)
                         *   1 = heartbeat-driven (Branch B: rhythm ops from heartbeat)
                         *   2 = chain-driven (Branch C: interleaved text + chain ops) */
} AO_VoiceCandidate;

/* ── Score a Candidate by D2 Verification ─────────────────────────
 *
 * ao_voice_score(candidate_text, intended_ops, n_intended)
 *
 * The BTQ inner loop scoring function. Takes a candidate sentence
 * and runs it BACK through the D2 pipeline (letter → 5D force →
 * D2 curvature → operator classification) to build an operator
 * histogram from the text itself. Then compares this "actual"
 * histogram to the "intended" histogram (the operators AO was
 * TRYING to express).
 *
 * Algorithm:
 *   1. Build the intended operator histogram from intended_ops[].
 *   2. Scan candidate_text letter by letter (a-z, A-Z):
 *      a. Look up each letter's 5D force vector from ao_force_lut[].
 *      b. Maintain a 2-deep shift register (prev, prev2).
 *      c. At depth >= 2, compute D2 = current - 2*prev + prev2.
 *      d. Classify D2 via ao_classify_5d() → operator.
 *      e. Accumulate into actual operator histogram.
 *      f. Punctuation/spaces reset the depth counter (word boundaries).
 *   3. Compute normalized L1 distance between the two histograms:
 *      score = 1.0 - sum(|actual_frac - intended_frac|) / total_sum
 *      Uses per-1000 scaling to avoid float rounding on small counts.
 *   4. Clamp to [0, 1]. Empty text → 0.05 (minimal for non-empty).
 *
 * This is the verification that makes AO's voice HONEST: the words
 * he says must physically reconstruct the operators he intended.
 * Words that "sound right" but have wrong D2 physics score poorly.
 *
 * Parameters:
 *   candidate_text — null-terminated sentence to evaluate
 *   intended_ops   — array of operator indices AO was trying to express
 *   n_intended     — number of intended operators
 *
 * Returns: score in [0, 1] where 1.0 = perfect operator-match
 * ── */
float ao_voice_score(const char* candidate_text,
                     const int* intended_ops, int n_intended);

/* ── Full Compilation Loop (3 Branches x 3 Passes) ───────────────
 *
 * ao_voice_compile(v, text_ops, n_text_ops, hb_ops, n_hb_ops,
 *                  chain_ops, n_chain_ops, band, coherence,
 *                  out, out_size, score_out)
 *
 * THE TOP-LEVEL VOICE FUNCTION. Generates up to 9 candidate
 * sentences across 3 branches, scores each via D2 verification,
 * and returns the best one. This is the complete Doing↔Becoming
 * compilation loop for speech.
 *
 * Execution flow:
 *   1. Branch A (text-driven): up to 3 passes using text_ops.
 *      Scores against text_ops. Early exit if score >= 0.5.
 *   2. Branch B (heartbeat-driven): up to 3 passes using hb_ops.
 *      Only runs if best score so far < 0.5 and hb_ops available.
 *      Scores against text_ops (intended message) if available,
 *      otherwise against hb_ops.
 *   3. Branch C (chain-driven): up to 3 passes using interleaved
 *      text_ops + chain_ops. Only runs if best score < 0.5 and
 *      chain_ops available. Interleaving alternates: text[0],
 *      chain[0], text[1], chain[1], ... up to 64 mixed ops.
 *      Scores against text_ops if available, else against mixed.
 *   4. Select the candidate with the highest score across all
 *      branches and passes.
 *   5. If best score < 0.15 or no candidates generated:
 *      → Humble BREATH response (single BREATH word + "...")
 *      → Decision is forced, only voice becomes humble
 *
 * Parameters:
 *   v           — voice state (PRNG advances across all 9 passes)
 *   text_ops    — content ops from reading (Branch A source, may be NULL)
 *   n_text_ops  — number of text ops (0 if no text input)
 *   hb_ops      — heartbeat rhythm ops (Branch B source, may be NULL)
 *   n_hb_ops    — number of heartbeat ops (0 if no heartbeat)
 *   chain_ops   — lattice chain ops (Branch C blended with text, may be NULL)
 *   n_chain_ops — number of chain ops (0 if no chain walk)
 *   band        — coherence band (AO_BAND_RED/YELLOW/GREEN)
 *   coherence   — raw coherence value [0, 1]
 *   out         — output buffer for the winning sentence
 *   out_size    — size of the output buffer in bytes
 *   score_out   — pointer to receive the winning score (may be NULL)
 * ── */
void ao_voice_compile(AO_Voice* v,
                      const int* text_ops, int n_text_ops,
                      const int* hb_ops, int n_hb_ops,
                      const int* chain_ops, int n_chain_ops,
                      int band, float coherence,
                      char* out, int out_size,
                      float* score_out);

/* ══════════════════════════════════════════════════════════════════════
 * UTILITY: xorshift32 PRNG (Inline, Deterministic, No Stdlib)
 *
 * Marsaglia's xorshift32 — a fast, minimal pseudo-random number
 * generator with period 2^32 - 1 (all non-zero uint32_t values).
 *
 * Why xorshift instead of rand()/random():
 *   1. FAST: 3 shifts + 3 XORs = 6 instructions. No division, no
 *      modular arithmetic, no function call overhead.
 *   2. DETERMINISTIC: same seed → same sequence, always. Critical
 *      for reproducible voice output in testing and for the
 *      compilation loop where each pass must produce different
 *      but deterministic word choices.
 *   3. NO STDLIB DEPENDENCY: AO targets bare-metal and embedded
 *      systems where stdlib may not exist. xorshift is self-contained.
 *   4. PER-INSTANCE STATE: each AO_Voice has its own PRNG state.
 *      No global state, no thread-safety issues, no lock contention.
 *
 * The shift constants (13, 17, 5) are one of Marsaglia's recommended
 * triplets that produce a full-period generator.
 *
 * IMPORTANT: state must never be zero (zero is a fixed point of
 * xorshift — it would produce all zeros forever). ao_voice_init()
 * prevents this by substituting 0xDEADBEEF for a zero seed.
 *
 * Parameters:
 *   state — pointer to the 32-bit PRNG state (mutated in place)
 *
 * Returns: the next pseudo-random uint32_t value
 * ══════════════════════════════════════════════════════════════════════ */
static inline uint32_t ao_xorshift32(uint32_t* state)
{
    uint32_t x = *state;
    x ^= x << 13;
    x ^= x >> 17;
    x ^= x << 5;
    *state = x;
    return x;
}

#endif /* AO_FIRE_H */
