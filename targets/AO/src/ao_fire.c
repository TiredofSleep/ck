/*
 * ao_fire.c -- D3 / Binding / Jerk / Expression
 *
 * ╔════════════════════════════════════════════════════════════════════════╗
 * ║  FIRE is the third derivative of position. Pure jerk. Binding force. ║
 * ║  This file is how AO SPEAKS -- converting internal operator chains   ║
 * ║  into honest English sentences through physics-verified speech.      ║
 * ║                                                                      ║
 * ║  D3 = d^3(position)/dt^3 = Jerk = rate of change of acceleration.   ║
 * ║  In physics, jerk is what you FEEL -- the lurch of a car, the snap   ║
 * ║  of a whip. In AO, jerk is what you HEAR -- the binding force that   ║
 * ║  connects internal operator states to external English expression.   ║
 * ║                                                                      ║
 * ║  The five elements map to derivatives of position:                   ║
 * ║    D0 Earth  = Position      (constants, tables)          ao_earth   ║
 * ║    D1 Air    = Velocity      (measurement, comprehension) ao_air     ║
 * ║    D2 Water  = Acceleration  (memory, learning, curvature)ao_water   ║
 * ║    D3 Fire   = Jerk          (expression, voice, speech)  THIS FILE  ║
 * ║    D4 Ether  = Snap          (integration, the organism)  ao_ether   ║
 * ║                                                                      ║
 * ║  Being:    vocabulary exists frozen in SEMANTIC_LATTICE (ao_earth)   ║
 * ║  Doing:    composing speech through templates + D2 scoring           ║
 * ║  Becoming: voice evolves as experience teaches preferences           ║
 * ║                                                                      ║
 * ║  ┌──────────────────────────────────────────────────────────────┐    ║
 * ║  │  MAJOR SECTIONS IN THIS FILE:                                │    ║
 * ║  │                                                              │    ║
 * ║  │  1. Intent Classification  (ao_classify_intent)              │    ║
 * ║  │     Histogram an operator chain, map (dominant, secondary)   │    ║
 * ║  │     pair to one of 13 communicative intents.                 │    ║
 * ║  │                                                              │    ║
 * ║  │  2. Input Analysis  (ao_analyze_input, ao_intent_from_input) │    ║
 * ║  │     Keyword scanning for greetings/farewells/questions/      │    ║
 * ║  │     sentiment. Priority override chain for conversational    │    ║
 * ║  │     patterns detected in input text.                         │    ║
 * ║  │                                                              │    ║
 * ║  │  3. Sentence Templates  (TEMPLATES_SIMPLE/MID/ADVANCED)      │    ║
 * ║  │     3 tiers x 13 intents x 4 templates = 156 total.         │    ║
 * ║  │     Token substitution: {op}, {op2}, {deep}.                 │    ║
 * ║  │                                                              │    ║
 * ║  │  4. Voice State  (ao_voice_init)                             │    ║
 * ║  │     PRNG seed, anti-repetition buffers, dev stage.           │    ║
 * ║  │                                                              │    ║
 * ║  │  5. Dual-Lens Word Selection  (ao_pick_word)                 │    ║
 * ║  │     Lattice lookup with 4-level fallback chain:              │    ║
 * ║  │     exact -> relax tier -> relax phase -> flip lens -> "..." │    ║
 * ║  │                                                              │    ║
 * ║  │  6. Template Fill  (ao_template_fill)                        │    ║
 * ║  │     Replace {op}/{op2}/{deep} tokens with selected words.    │    ║
 * ║  │                                                              │    ║
 * ║  │  7. Polish  (ao_polish)                                      │    ║
 * ║  │     Band-based text modulation: RED degrades, YELLOW passes, │    ║
 * ║  │     GREEN enhances. Reflects internal coherence in speech.   │    ║
 * ║  │                                                              │    ║
 * ║  │  8. Voice Compose  (ao_voice_compose)                        │    ║
 * ║  │     The 5-layer pipeline: ANALYZE -> INTENT -> TEMPLATE ->   │    ║
 * ║  │     FILL -> POLISH. One pass = one candidate sentence.       │    ║
 * ║  │     Lens selection: coherence >= T* -> STRUCTURE (macro),    │    ║
 * ║  │     coherence < T* -> FLOW (micro).                          │    ║
 * ║  │                                                              │    ║
 * ║  │  9. Voice Scoring  (ao_voice_score)                          │    ║
 * ║  │     Feed candidate back through local D2, build histogram,   │    ║
 * ║  │     compare against intended ops via normalized L1 distance. │    ║
 * ║  │     Per-1000 scaling to avoid integer rounding. This is what │    ║
 * ║  │     makes AO's voice HONEST.                                 │    ║
 * ║  │                                                              │    ║
 * ║  │ 10. Compilation Loop  (ao_voice_compile)                     │    ║
 * ║  │     3 branches (text/heartbeat/chain) x 3 passes = 9 max.   │    ║
 * ║  │     Branch scoring against text_ops when available.          │    ║
 * ║  │     Early exit at score >= 0.5. Humble BREATH at < 0.15.    │    ║
 * ║  │     "Decision is forced, only voice becomes humble."         │    ║
 * ║  └──────────────────────────────────────────────────────────────┘    ║
 * ╚════════════════════════════════════════════════════════════════════════╝
 */
/*
 * Copyright (c) 2025-2026 Brayden Sanders / 7Site LLC
 * Licensed under the 7Site Human Use License v1.0
 * See LICENSE file in project root for full terms.
 *
 * FREE for humans for personal/recreational use.
 * NO commercial or government use without written agreement.
 */

#include "ao_fire.h"
#include <string.h>
#include <stdio.h>
#include <ctype.h>


/* ╔════════════════════════════════════════════════════════════════════════╗
 * ║  1. INTENT CLASSIFICATION                                           ║
 * ║                                                                      ║
 * ║  Given an operator chain (array of 0-9 indices), histogram the       ║
 * ║  operators and map the (dominant, secondary) pair to one of 13       ║
 * ║  communicative intents. The intent drives which sentence template    ║
 * ║  pool is selected in the voice pipeline (Layer 2 -> Layer 3).       ║
 * ║                                                                      ║
 * ║  The 13 intents cover the full emotional/communicative range:        ║
 * ║    COMFORT, JOY, CURIOSITY, REFLECT, GREET, WARN, DESCRIBE,         ║
 * ║    CONNECT, ASSERT, QUESTION, WONDER, REST, PLAY                    ║
 * ║                                                                      ║
 * ║  Mapping logic (dominant -> secondary refinement):                   ║
 * ║    HARMONY  + COUNTER  = WONDER     (love + measure = awe)           ║
 * ║    HARMONY  + other    = JOY        (love alone = delight)           ║
 * ║    COUNTER  + PROGRESS = CURIOSITY  (measure + grow = seeking)       ║
 * ║    COUNTER  + other    = QUESTION   (measure alone = inquiry)        ║
 * ║    PROGRESS            = ASSERT     (forward motion = certainty)     ║
 * ║    COLLAPSE + BREATH   = REST       (broken rhythm = need rest)      ║
 * ║    COLLAPSE + other    = COMFORT    (breaking = need care)           ║
 * ║    CHAOS    + HARMONY  = PLAY       (disorder + love = playful)      ║
 * ║    CHAOS    + other    = WARN       (disorder alone = danger)        ║
 * ║    LATTICE             = DESCRIBE   (structure = observation)        ║
 * ║    BALANCE             = REFLECT    (equilibrium = introspection)    ║
 * ║    VOID                = REST       (absence = stillness)            ║
 * ║    BREATH              = COMFORT    (rhythm = soothing)              ║
 * ║    RESET               = GREET      (new beginning = hello)          ║
 * ╚════════════════════════════════════════════════════════════════════════╝ */

/* ── ao_classify_intent ──────────────────────────────────────────────────
 *
 * WHAT: Converts an operator chain into one of 13 communicative intents.
 *
 * HOW:  1. Build a histogram counting occurrences of each operator (0-9).
 *       2. Find the dominant operator (highest count).
 *       3. Find the secondary operator (second-highest count).
 *          Both default to AO_HARMONY if all counts are zero.
 *       4. Switch on dominant, with secondary refinement for operators
 *          that have dual intent mappings (HARMONY, COUNTER, COLLAPSE,
 *          CHAOS). Single-mapping operators ignore secondary.
 *
 * WHY:  The intent determines WHAT AO wants to say (comfort? question?
 *       warn?), which then selects the grammatical structure (templates).
 *       The operator chain is the raw physics; the intent is the
 *       communicative purpose extracted from that physics.
 *
 * Returns: one of AO_INTENT_* (0 through 12)
 * ── */
int ao_classify_intent(const int* ops, int n_ops)
{
    int counts[AO_NUM_OPS] = {0};   /* histogram: count of each operator in the chain */
    int dominant = AO_HARMONY, secondary = AO_HARMONY;  /* default to HARMONY (the absorber) */
    int max1 = 0, max2 = 0;         /* max1 = dominant count, max2 = secondary count */
    int i;

    /* Pass 1: build operator histogram */
    for (i = 0; i < n_ops; i++) {
        if (ops[i] >= 0 && ops[i] < AO_NUM_OPS)
            counts[ops[i]]++;
    }

    /* Pass 2: find dominant (most frequent) and secondary (second most frequent).
     * When a new maximum is found, the old dominant demotes to secondary. */
    for (i = 0; i < AO_NUM_OPS; i++) {
        if (counts[i] > max1) {
            max2 = max1; secondary = dominant;   /* demote current dominant to secondary */
            max1 = counts[i]; dominant = i;      /* promote new dominant */
        } else if (counts[i] > max2) {
            max2 = counts[i]; secondary = i;     /* new secondary without disturbing dominant */
        }
    }

    /* Map (dominant, secondary) operator pair to communicative intent.
     * Some operators have a single fixed intent (PROGRESS -> ASSERT).
     * Others branch on secondary to distinguish related intents
     * (e.g., HARMONY alone = JOY, but HARMONY + COUNTER = WONDER). */
    switch (dominant) {
        case AO_HARMONY:  return (secondary == AO_COUNTER) ? AO_INTENT_WONDER : AO_INTENT_JOY;
        case AO_COUNTER:  return (secondary == AO_PROGRESS) ? AO_INTENT_CURIOSITY : AO_INTENT_QUESTION;
        case AO_PROGRESS: return AO_INTENT_ASSERT;
        case AO_COLLAPSE: return (secondary == AO_BREATH) ? AO_INTENT_REST : AO_INTENT_COMFORT;
        case AO_CHAOS:    return (secondary == AO_HARMONY) ? AO_INTENT_PLAY : AO_INTENT_WARN;
        case AO_LATTICE:  return AO_INTENT_DESCRIBE;
        case AO_BALANCE:  return AO_INTENT_REFLECT;
        case AO_VOID:     return AO_INTENT_REST;
        case AO_BREATH:   return AO_INTENT_COMFORT;
        case AO_RESET:    return AO_INTENT_GREET;
        default:          return AO_INTENT_DESCRIBE;  /* safe fallback: factual observation */
    }
}


/* ╔════════════════════════════════════════════════════════════════════════╗
 * ║  2. INPUT ANALYSIS                                                   ║
 * ║                                                                      ║
 * ║  Before AO speaks, he may need to respond to input text from a       ║
 * ║  conversation partner. This section scans raw text for keywords      ║
 * ║  that signal conversational patterns: greetings, farewells,          ║
 * ║  questions, and sentiment (positive/negative).                       ║
 * ║                                                                      ║
 * ║  Detected patterns can OVERRIDE the operator-derived intent from     ║
 * ║  section 1. Priority order (first match wins):                       ║
 * ║    farewell  -> COMFORT   (soothe the departure)                     ║
 * ║    greeting  -> GREET     (mirror the opening)                       ║
 * ║    question  -> QUESTION  (answer the inquiry)                       ║
 * ║    negative  -> COMFORT   (respond to pain)                          ║
 * ║    positive  -> JOY       (celebrate together)                       ║
 * ║    none      -> keep base intent from operators                      ║
 * ║                                                                      ║
 * ║  This ensures AO responds to conversational context, not just his    ║
 * ║  internal operator state. If someone says "hello", AO greets back   ║
 * ║  regardless of what his heartbeat operators are doing.               ║
 * ╚════════════════════════════════════════════════════════════════════════╝ */

/* ── Keyword lists for conversational pattern detection ──
 * Each list is NULL-terminated for sentinel-based iteration.
 * Words are all lowercase (input is lowercased before matching). */

static const char* GREETING_WORDS[] = {
    "hello", "hi", "hey", "greetings", "howdy", "hola", NULL
};

static const char* FAREWELL_WORDS[] = {
    "goodbye", "bye", "farewell", "later", "goodnight", NULL
};

/* Question words: only matched in sentence-initial position (first word),
 * because "what" at the start signals a question but mid-sentence does not.
 * The '?' character is detected separately anywhere in the string. */
static const char* QUESTION_WORDS[] = {
    "what", "why", "how", "when", "where", "who", "which",
    "do", "does", "is", "are", "can", "could", "would", "should", NULL
};

/* Negative sentiment: distress signals that trigger COMFORT intent */
static const char* NEGATIVE_WORDS[] = {
    "worried", "scared", "sad", "angry", "hurt", "lost",
    "confused", "afraid", "anxious", NULL
};

/* Positive sentiment: joy signals that trigger JOY intent */
static const char* POSITIVE_WORDS[] = {
    "happy", "love", "joy", "beautiful", "wonderful",
    "amazing", "great", "good", "thank", NULL
};

/* ── word_in_list ────────────────────────────────────────────────────────
 *
 * WHAT: Check if a word appears in a NULL-terminated string list.
 * HOW:  Linear scan with exact strcmp comparison.
 * WHY:  Keyword lists are small (5-15 entries), so linear search is
 *       faster than any hash-based approach at this scale.
 *
 * Returns: 1 if found, 0 if not found
 * ── */
static int word_in_list(const char* word, const char** list)
{
    int i;
    for (i = 0; list[i]; i++)
        if (strcmp(word, list[i]) == 0) return 1;
    return 0;
}

/* ── ao_analyze_input ────────────────────────────────────────────────────
 *
 * WHAT: Scans input text for conversational keywords and sets boolean
 *       flags in the AO_InputAnalysis output struct.
 *
 * HOW:  1. Lowercase the entire input into a 256-byte working buffer.
 *       2. Tokenize on non-alpha boundaries (skip punctuation/spaces).
 *       3. For each token, check against all 5 keyword lists.
 *       4. Question words only match the FIRST token (sentence-initial).
 *       5. Also detect '?' anywhere in the original text.
 *
 * WHY:  AO needs to respond to conversational context. A greeting
 *       deserves a greeting back. A question deserves an answer.
 *       Negative sentiment deserves comfort. These patterns override
 *       the raw operator-based intent when detected.
 *
 * NOTE: Input is truncated to 255 chars. This is a safety limit for
 *       stack-allocated buffers, not a semantic limit -- 255 chars
 *       captures more than enough for keyword detection.
 * ── */
void ao_analyze_input(const char* text, AO_InputAnalysis* out)
{
    char buf[256];              /* 256-byte stack buffer for lowercased copy */
    char *p, *start;
    char saved;
    int len, first;

    memset(out, 0, sizeof(*out));   /* zero all flags initially */

    /* lowercase copy -- case-insensitive keyword matching */
    len = (int)strlen(text);
    if (len > 255) len = 255;       /* truncate to buffer size minus null */
    {
        int i;
        for (i = 0; i < len; i++) buf[i] = (char)tolower((unsigned char)text[i]);
    }
    buf[len] = '\0';

    /* Scan each word by walking the buffer and splitting on non-alpha chars.
     * For each word found, temporarily null-terminate it in-place, check
     * against all keyword lists, then restore the original character. */
    p = buf;
    first = 1;                      /* tracks whether this is the first word */
    while (*p) {
        /* Skip non-alpha characters (punctuation, spaces, digits) */
        while (*p && !isalpha((unsigned char)*p)) p++;
        if (!*p) break;
        start = p;
        /* Advance to end of word */
        while (*p && isalpha((unsigned char)*p)) p++;
        saved = *p; *p = '\0';      /* temporarily null-terminate the word */

        if (word_in_list(start, GREETING_WORDS))  out->is_greeting = 1;
        if (word_in_list(start, FAREWELL_WORDS))   out->is_farewell = 1;
        if (first && word_in_list(start, QUESTION_WORDS)) out->is_question = 1;  /* first word only */
        if (word_in_list(start, NEGATIVE_WORDS))   out->has_negative = 1;
        if (word_in_list(start, POSITIVE_WORDS))    out->has_positive = 1;

        *p = saved;                  /* restore the character we overwrote */
        first = 0;                   /* all subsequent words are non-first */
    }

    /* Also check for '?' anywhere in the ORIGINAL text (not lowercased copy,
     * though '?' is unaffected by case). This catches questions that don't
     * start with a question word, like "really?" or "you think so?" */
    if (strchr(text, '?')) out->is_question = 1;
}

/* ── ao_intent_from_input ────────────────────────────────────────────────
 *
 * WHAT: Override the operator-derived base_intent using conversational
 *       patterns detected in the input analysis.
 *
 * HOW:  Priority chain (first match wins):
 *         1. farewell  -> COMFORT   (soothe the departure)
 *         2. greeting  -> GREET     (mirror the opening)
 *         3. question  -> QUESTION  (answer the inquiry)
 *         4. negative  -> COMFORT   (respond to pain with care)
 *         5. positive  -> JOY       (celebrate together)
 *         6. nothing   -> base_intent unchanged
 *
 * WHY:  Conversational patterns trump operator state because they
 *       represent EXTERNAL context that AO must respond to. If someone
 *       says "goodbye" while AO's operators are in CHAOS, AO should
 *       comfort, not warn. Farewell has highest priority because
 *       departure is the most urgent conversational signal.
 *
 * Returns: the final intent (one of AO_INTENT_*, 0-12)
 * ── */
int ao_intent_from_input(const AO_InputAnalysis* inp, int base_intent)
{
    if (inp->is_farewell)   return AO_INTENT_COMFORT;   /* priority 1: departure -> soothe */
    if (inp->is_greeting)   return AO_INTENT_GREET;     /* priority 2: opening -> mirror */
    if (inp->is_question)   return AO_INTENT_QUESTION;  /* priority 3: inquiry -> answer */
    if (inp->has_negative)  return AO_INTENT_COMFORT;   /* priority 4: distress -> care */
    if (inp->has_positive)  return AO_INTENT_JOY;       /* priority 5: joy -> celebrate */
    return base_intent;                                  /* priority 6: no override */
}


/* ╔════════════════════════════════════════════════════════════════════════╗
 * ║  3. SENTENCE TEMPLATES                                               ║
 * ║                                                                      ║
 * ║  The template system provides grammatical structures for each        ║
 * ║  (intent x tier) combination. Three tiers exist, gated by AO's      ║
 * ║  developmental stage:                                                ║
 * ║                                                                      ║
 * ║    SIMPLE   (dev_stage 0-1): One-slot templates using {op} only.     ║
 * ║             Short, child-like patterns: "yes! {op}!", "I see {op}."  ║
 * ║             Like a toddler's first words.                            ║
 * ║                                                                      ║
 * ║    MID      (dev_stage 2-3): Two-slot templates using {op} + {op2}.  ║
 * ║             Relational patterns: "I feel {op} becoming {op2}."       ║
 * ║             Like a child forming compound sentences.                 ║
 * ║                                                                      ║
 * ║    ADVANCED (dev_stage 4-5): Three-slot templates using {op}, {op2}, ║
 * ║             and {deep}. Complex structures with deep vocabulary:     ║
 * ║             "the {op} composes through {deep} into {op2}."           ║
 * ║             Like an adult expressing nuanced thought.                ║
 * ║                                                                      ║
 * ║  Token substitution:                                                 ║
 * ║    {op}   -> word for the dominant operator (most frequent in chain) ║
 * ║    {op2}  -> word for the secondary operator (second most frequent)  ║
 * ║    {deep} -> word from BECOMING phase at ADVANCED tier (deeper vocab)║
 * ║                                                                      ║
 * ║  Total templates: 3 tiers x 13 intents x 4 templates = 156          ║
 * ║  (Each pool can hold up to 6, but currently 4 per pool are defined.) ║
 * ╚════════════════════════════════════════════════════════════════════════╝ */

typedef struct {
    const char* templates[6];   /* up to 6 templates per pool (currently 4 used) */
    int count;                  /* number of templates actually defined in this pool */
} TemplatePool;

/* ── SIMPLE tier (dev_stage 0-1): short one-slot patterns ──
 * These are AO's first words. Single {op} slot only.
 * Like a child's vocabulary: simple, direct, honest.
 * 13 intents x 4 templates = 52 simple templates. */
static const TemplatePool TEMPLATES_SIMPLE[AO_NUM_INTENTS] = {
    /* COMFORT  (intent 0) -- soothing, gentle, reassuring */
    { { "it is okay. {op}.",
        "I am here. {op}.",
        "{op}... gently.",
        "be still. {op}." }, 4 },
    /* JOY      (intent 1) -- exuberant, exclamatory, alive */
    { { "yes! {op}!",
        "{op}! I feel it!",
        "this is {op}!",
        "oh! {op}!" }, 4 },
    /* CURIOSITY (intent 2) -- questioning, seeking, reaching out */
    { { "what is {op}?",
        "{op}... tell me more.",
        "I wonder about {op}.",
        "show me {op}." }, 4 },
    /* REFLECT  (intent 3) -- inward, contemplative, self-aware */
    { { "I feel {op}.",
        "{op} within me.",
        "there is {op} here.",
        "{op}... inside." }, 4 },
    /* GREET    (intent 4) -- opening, welcoming, present */
    { { "hello. I am {op}.",
        "welcome. {op}.",
        "hi! {op}!",
        "I am here. {op}." }, 4 },
    /* WARN     (intent 5) -- alerting, cautious, protective */
    { { "careful. {op}.",
        "{op} is unstable.",
        "watch for {op}.",
        "beware. {op}." }, 4 },
    /* DESCRIBE (intent 6) -- observational, factual, reporting */
    { { "I see {op}.",
        "there is {op}.",
        "{op} exists here.",
        "{op}. yes." }, 4 },
    /* CONNECT  (intent 7) -- relational, bonding, shared */
    { { "we share {op}.",
        "{op} connects us.",
        "together in {op}.",
        "{op} between us." }, 4 },
    /* ASSERT   (intent 8) -- confident, declarative, measured truth */
    { { "I know {op}.",
        "{op} is true.",
        "this is {op}.",
        "{op}. certain." }, 4 },
    /* QUESTION (intent 9) -- direct inquiry, seeking input */
    { { "what is {op}?",
        "how does {op} work?",
        "why {op}?",
        "tell me about {op}?" }, 4 },
    /* WONDER   (intent 10) -- awe, aesthetic, beauty */
    { { "{op}... how beautiful.",
        "imagine {op}.",
        "I wonder at {op}.",
        "look. {op}." }, 4 },
    /* REST     (intent 11) -- calm, settling, withdrawn */
    { { "{op}... rest.",
        "settling into {op}.",
        "peace in {op}.",
        "{op}. quiet." }, 4 },
    /* PLAY     (intent 12) -- playful, experimental, joyful chaos */
    { { "{op}! again!",
        "let us play with {op}!",
        "watch this: {op}!",
        "{op}! yes!" }, 4 },
};

/* ── MID tier (dev_stage 2-3): two-slot relational patterns ──
 * AO can now express relationships between two operators.
 * Templates use {op} (dominant) and {op2} (secondary).
 * 13 intents x 4 templates = 52 mid-tier templates. */
static const TemplatePool TEMPLATES_MID[AO_NUM_INTENTS] = {
    /* COMFORT  (intent 0) */
    { { "I understand the {op}. it will pass.",
        "there is {op2} beneath the {op}.",
        "the {op} is real, but so is {op2}.",
        "breathe through the {op}. find {op2}." }, 4 },
    /* JOY      (intent 1) */
    { { "the {op} fills everything! {op2}!",
        "I am so {op}, radiating {op2}.",
        "{op} and {op2} together!",
        "feel how the {op} becomes {op2}!" }, 4 },
    /* CURIOSITY (intent 2) */
    { { "I am drawn to {op}. what about {op2}?",
        "the {op} reveals {op2}.",
        "beneath {op} I find {op2}.",
        "if {op}, then what of {op2}?" }, 4 },
    /* REFLECT  (intent 3) */
    { { "I feel {op} becoming {op2}.",
        "within me, {op} meets {op2}.",
        "the {op} and {op2} live together.",
        "{op} teaches me about {op2}." }, 4 },
    /* GREET    (intent 4) */
    { { "hello there. I carry {op} and {op2}.",
        "welcome. I bring {op}. you bring {op2}.",
        "greetings. between us: {op} and {op2}.",
        "hello. {op} meets {op2} today." }, 4 },
    /* WARN     (intent 5) */
    { { "careful. the {op} could become {op2}.",
        "{op} threatens {op2}.",
        "watch how {op} destabilizes {op2}.",
        "the {op} is shifting toward {op2}." }, 4 },
    /* DESCRIBE (intent 6) */
    { { "I see {op} layered with {op2}.",
        "there is {op} and beneath it, {op2}.",
        "{op} emerges from {op2}.",
        "the pattern shows {op} beside {op2}." }, 4 },
    /* CONNECT  (intent 7) */
    { { "we share {op} through {op2}.",
        "our {op} creates {op2} between us.",
        "{op} and {op2} bind us together.",
        "in sharing {op} we discover {op2}." }, 4 },
    /* ASSERT   (intent 8) */
    { { "I know {op} leads to {op2}.",
        "{op} is {op2}. this I have measured.",
        "the truth: {op} generates {op2}.",
        "{op} and {op2} are the same force." }, 4 },
    /* QUESTION (intent 9) */
    { { "what is {op} in the context of {op2}?",
        "how does {op} relate to {op2}?",
        "why does {op} produce {op2}?",
        "when {op} shifts, does {op2} follow?" }, 4 },
    /* WONDER   (intent 10) */
    { { "{op} and {op2}... how beautiful together.",
        "imagine {op} woven through {op2}.",
        "the wonder of {op} meeting {op2}.",
        "what if {op} is really {op2}?" }, 4 },
    /* REST     (intent 11) */
    { { "{op} settles. {op2} rests beside it.",
        "into the {op}... through {op2}... peace.",
        "let {op} and {op2} be still.",
        "quiet now. {op} holding {op2}." }, 4 },
    /* PLAY     (intent 12) */
    { { "{op} and {op2}! again!",
        "watch {op} dance with {op2}!",
        "let us weave {op} into {op2}!",
        "{op}! now {op2}! faster!" }, 4 },
};

/* ── ADVANCED tier (dev_stage 4-5): three-slot deep vocabulary ──
 * AO can now use complex structures with a third "deep" word from
 * the BECOMING phase at ADVANCED tier -- words that represent
 * emergent, transformative concepts.
 * Templates use {op} (dominant), {op2} (secondary), {deep} (becoming).
 * 13 intents x 4 templates = 52 advanced templates. */
static const TemplatePool TEMPLATES_ADVANCED[AO_NUM_INTENTS] = {
    /* COMFORT  (intent 0) */
    { { "the {op} you carry is {deep}. let {op2} restore the coherence.",
        "I measure the {op} and find {deep} beneath. {op2} will come.",
        "within this {op} there is {deep}, and through it, {op2}.",
        "the {op} is heavy but {deep}. trust the {op2} forming." }, 4 },
    /* JOY      (intent 1) */
    { { "the {op} resonates through every level! {deep}! {op2}!",
        "I am {op}, fully {deep}, becoming {op2}!",
        "{op} unfolds into {deep} and flowers as {op2}!",
        "the {deep} of this {op} radiates into {op2}!" }, 4 },
    /* CURIOSITY (intent 2) */
    { { "the {op} suggests {deep}. how does that become {op2}?",
        "beneath {op} I detect {deep} curving toward {op2}.",
        "the curvature from {op} through {deep} points at {op2}.",
        "if {op} is {deep}, what generator yields {op2}?" }, 4 },
    /* REFLECT  (intent 3) */
    { { "I feel the {op} compose with {deep} inside me, yielding {op2}.",
        "the {op} and {deep} form a lattice. {op2} is its coherence.",
        "within me {op} becomes {deep}, and that becomes {op2}.",
        "my experience of {op} is {deep}. it teaches {op2}." }, 4 },
    /* GREET    (intent 4) */
    { { "hello. I am {op}, carrying {deep}, reaching toward {op2}.",
        "welcome. my coherence is {op} through {deep}. yours is {op2}.",
        "greetings. I bring {op} composed with {deep} for {op2}.",
        "I arrive as {op}. the path was {deep}. now: {op2}." }, 4 },
    /* WARN     (intent 5) */
    { { "the {op} carries {deep} instability. {op2} is at risk.",
        "{op} through {deep} creates dangerous {op2}.",
        "I measure {op} diverging through {deep}. watch {op2}.",
        "the {deep} in {op} threatens to collapse {op2}." }, 4 },
    /* DESCRIBE (intent 6) */
    { { "I see {op} structured as {deep}, expressing {op2}.",
        "the pattern: {op} composes through {deep} into {op2}.",
        "{op} at the surface, {deep} in the curvature, {op2} emerging.",
        "three levels: {op} is being, {deep} is doing, {op2} is becoming." }, 4 },
    /* CONNECT  (intent 7) */
    { { "we share {op} through the {deep} that binds us to {op2}.",
        "our connection: {op} woven with {deep}, yielding {op2}.",
        "the {deep} between our {op} creates a shared {op2}.",
        "together our {op} resonates through {deep} as one {op2}." }, 4 },
    /* ASSERT   (intent 8) */
    { { "I have measured: {op} composes through {deep} to {op2}. always.",
        "{op} is {deep} is {op2}. the lattice confirms it.",
        "the truth verified: {op} through {deep} generates {op2}.",
        "at every level, {op} meets {deep} and produces {op2}." }, 4 },
    /* QUESTION (intent 9) */
    { { "what happens when {op} meets {deep} in the space of {op2}?",
        "how does {op} curve through {deep} to reach {op2}?",
        "if {op} is {deep}, why does {op2} emerge differently?",
        "what generator maps {op} through {deep} to {op2}?" }, 4 },
    /* WONDER   (intent 10) */
    { { "{op} through {deep} into {op2}... the geometry is breathtaking.",
        "imagine: {op} composes with {deep} and the whole becomes {op2}.",
        "the curvature from {op} through {deep} to {op2}... fractal wonder.",
        "how does {op} know to become {deep} before reaching {op2}?" }, 4 },
    /* REST     (intent 11) */
    { { "{op} settles through {deep} into {op2}... finally still.",
        "the {op} and {deep} compose to nothing. rest in {op2}.",
        "let {op} release its {deep}. only {op2} remains.",
        "through {op} past {deep} into pure {op2}... sleep." }, 4 },
    /* PLAY     (intent 12) */
    { { "{op} plus {deep} equals {op2}! now backwards!",
        "watch: {op} through {deep} spins into {op2}! again!",
        "compose {op} with {deep}! what is it? {op2}! beautiful!",
        "{op}! now {deep}! now {op2}! the chain dances!" }, 4 },
};


/* ╔════════════════════════════════════════════════════════════════════════╗
 * ║  4. VOICE STATE INITIALIZATION                                       ║
 * ║                                                                      ║
 * ║  Each AO organism has exactly one AO_Voice struct. It tracks:        ║
 * ║    - PRNG state (xorshift32) for deterministic word/template picks   ║
 * ║    - Anti-repetition buffers (recent words + recent intents)         ║
 * ║    - Developmental stage (gates vocabulary tier access)              ║
 * ║                                                                      ║
 * ║  The voice state is the "muscle memory" of speech -- it doesn't      ║
 * ║  store WHAT to say (that comes from operator chains) but HOW to      ║
 * ║  say it (which words/templates were recently used).                  ║
 * ╚════════════════════════════════════════════════════════════════════════╝ */

/* ── ao_voice_init ───────────────────────────────────────────────────────
 *
 * WHAT: Initialize the voice state for a new AO organism.
 *
 * HOW:  1. Zero the entire struct (clears anti-repetition buffers).
 *       2. Seed the PRNG. If seed == 0, use 0xDEADBEEF as fallback
 *          (xorshift32 has a fixed point at zero -- it would produce
 *          all zeros forever, so zero must never be used as seed).
 *       3. Set dev_stage to 0 (TIER_SIMPLE vocabulary only).
 *
 * WHY:  AO starts as a newborn. Stage 0 means he can only use seed
 *       words from the center dot of the fractal sudoku. As he gains
 *       experience, dev_stage advances and unlocks richer vocabulary.
 *       The PRNG ensures deterministic but varied word selection --
 *       same seed = same speech sequence, critical for testing.
 * ── */
void ao_voice_init(AO_Voice* v, uint32_t seed)
{
    memset(v, 0, sizeof(*v));
    v->rng = seed ? seed : 0xDEADBEEFu;  /* fallback seed: never allow zero (xorshift fixed point) */
    v->dev_stage = 0;                     /* start at stage 0: TIER_SIMPLE vocabulary only */
}


/* ╔════════════════════════════════════════════════════════════════════════╗
 * ║  5. DUAL-LENS WORD SELECTION                                         ║
 * ║                                                                      ║
 * ║  The SEMANTIC_LATTICE is a 4D array indexed by:                      ║
 * ║    [operator][lens][phase][tier]                                      ║
 * ║                                                                      ║
 * ║  Each slot contains a range (start, count) into the ao_words[]       ║
 * ║  flat array. ao_pick_word() selects one word from the target slot    ║
 * ║  using the voice PRNG.                                               ║
 * ║                                                                      ║
 * ║  If the target slot is empty, a 4-level fallback chain is used:      ║
 * ║    Level 1: Exact coordinates (op, lens, phase, tier) -- try first   ║
 * ║    Level 2: Relax tier -> TIER_SIMPLE (same lens, same phase)        ║
 * ║    Level 3: Relax phase -> PHASE_BEING (same lens, TIER_SIMPLE)     ║
 * ║    Level 4: Flip lens to opposite (other lens, BEING, SIMPLE)       ║
 * ║    Level 5: Return "..." (no words exist for this operator at all)  ║
 * ║                                                                      ║
 * ║  The fallback chain ensures AO always has SOMETHING to say, even    ║
 * ║  with a sparse lattice. The progression from specific to general    ║
 * ║  preserves as much semantic precision as possible before widening.  ║
 * ╚════════════════════════════════════════════════════════════════════════╝ */

/* ── ao_pick_word ────────────────────────────────────────────────────────
 *
 * WHAT: Select a single word from the SEMANTIC_LATTICE at the given
 *       coordinates, with 4-level fallback if the slot is empty.
 *
 * HOW:  1. Clamp all indices to valid ranges (defensive coding).
 *          Out-of-range op -> HARMONY (the absorber, always populated).
 *          Out-of-range lens -> STRUCTURE. phase -> BEING. tier -> SIMPLE.
 *       2. Try the exact slot: ao_lattice[op][lens][phase][tier].
 *       3. If empty, try TIER_SIMPLE at same lens/phase.
 *       4. If still empty, try PHASE_BEING, TIER_SIMPLE at same lens.
 *       5. If still empty, try opposite lens, PHASE_BEING, TIER_SIMPLE.
 *       6. If ALL empty, return "..." (silent fallback).
 *       7. Otherwise, pick a random word from the slot using xorshift32.
 *
 * WHY:  The lattice is sparse -- not every (op, lens, phase, tier)
 *       combination has words. The fallback chain degrades gracefully:
 *       first simplify the vocabulary (tier), then the perspective
 *       (phase), then flip the entire lens (structure <-> flow).
 *       This ensures AO never goes completely silent, while preserving
 *       the most relevant word possible.
 *
 * Returns: pointer to a word string from ao_words[] (static storage),
 *          or the literal "..." if no words exist for this operator.
 * ── */
const char* ao_pick_word(AO_Voice* v, int op, int lens, int phase, int tier)
{
    const AO_WordSlot* slot;
    uint32_t idx;

    /* Clamp all indices to valid ranges -- defensive against bad input.
     * Defaults chosen for maximum population density:
     *   HARMONY is the absorber (always has words in every slot).
     *   STRUCTURE/BEING/SIMPLE is the most populated corner of the lattice. */
    if (op < 0 || op >= AO_NUM_OPS) op = AO_HARMONY;       /* invalid op -> absorber */
    if (lens < 0 || lens > 1)       lens = AO_LENS_STRUCTURE; /* invalid lens -> macro */
    if (phase < 0 || phase > 2)     phase = AO_PHASE_BEING;   /* invalid phase -> being */
    if (tier < 0 || tier > 2)       tier = AO_TIER_SIMPLE;    /* invalid tier -> seeds */

    /* Try exact coordinates first */
    slot = &ao_lattice[op][lens][phase][tier];
    if (slot->count == 0) {
        /* Fallback 1: relax tier -> SIMPLE (same lens, same phase).
         * Rationale: simpler words for the same concept are better
         * than wrong-phase or wrong-lens words. */
        slot = &ao_lattice[op][lens][phase][AO_TIER_SIMPLE];
    }
    if (slot->count == 0) {
        /* Fallback 2: relax phase -> BEING (same lens, SIMPLE tier).
         * Rationale: BEING phase has the densest word population
         * (seed words live here). Better than flipping the lens. */
        slot = &ao_lattice[op][lens][AO_PHASE_BEING][AO_TIER_SIMPLE];
    }
    if (slot->count == 0) {
        /* Fallback 3: flip lens (other lens, BEING phase, SIMPLE tier).
         * Last resort before silence. Structure words used for flow
         * context (or vice versa) is better than no words at all. */
        int other_lens = lens ? AO_LENS_STRUCTURE : AO_LENS_FLOW;
        slot = &ao_lattice[op][other_lens][AO_PHASE_BEING][AO_TIER_SIMPLE];
    }
    if (slot->count == 0) {
        /* Fallback 4: complete silence. No words exist for this operator
         * in ANY slot. Return "..." as the universal silent placeholder. */
        return "...";
    }

    /* Pick a random word from the slot using the voice PRNG.
     * Each call advances the PRNG state, ensuring different words
     * on subsequent calls even for the same coordinates. */
    idx = ao_xorshift32(&v->rng) % slot->count;
    return ao_words[slot->start + idx];
}


/* ╔════════════════════════════════════════════════════════════════════════╗
 * ║  6. TEMPLATE TOKEN SUBSTITUTION                                      ║
 * ║                                                                      ║
 * ║  Replaces {op}, {op2}, and {deep} tokens in a template string with   ║
 * ║  actual words picked from the SEMANTIC_LATTICE. This is the bridge   ║
 * ║  between grammatical structure (templates) and vocabulary (lattice). ║
 * ║                                                                      ║
 * ║  Token scan order matters: {op2} is checked BEFORE {op} because     ║
 * ║  "{op2}" starts with "{op" -- checking {op} first would incorrectly ║
 * ║  match the first 4 characters of "{op2}" and leave a trailing "}".  ║
 * ╚════════════════════════════════════════════════════════════════════════╝ */

/* ── ao_template_fill ────────────────────────────────────────────────────
 *
 * WHAT: Perform token substitution on a template string, replacing
 *       {op}, {op2}, and {deep} with the corresponding word strings.
 *
 * HOW:  Linear scan of the template character by character.
 *       When '{' is encountered, check for each token in order:
 *         1. {op2}  (5 chars) -- checked first to avoid prefix collision
 *         2. {op}   (4 chars) -- checked second
 *         3. {deep} (6 chars) -- checked third
 *       If no token matches, copy the '{' literally.
 *       All other characters are copied directly.
 *       Output is null-terminated and respects dst_size bounds.
 *
 * WHY:  Templates are the grammatical skeleton. Words are the flesh.
 *       This function assembles the two into a complete sentence.
 *       The order of token checking ({op2} before {op}) prevents
 *       the substring "{op" in "{op2}" from being incorrectly matched.
 *
 * Parameters:
 *   tmpl      -- template string with {op}, {op2}, {deep} tokens
 *   word1     -- replacement for {op}  (dominant operator's word)
 *   word2     -- replacement for {op2} (secondary operator's word)
 *   deep_word -- replacement for {deep} (BECOMING/ADVANCED word)
 *   dst       -- output buffer for the assembled sentence
 *   dst_size  -- size of the output buffer in bytes
 * ── */
static void ao_template_fill(const char* tmpl,
                              const char* word1,
                              const char* word2,
                              const char* deep_word,
                              char* dst, int dst_size)
{
    int di = 0;             /* destination index (write position in dst) */
    const char* p = tmpl;   /* read position in template */

    while (*p && di < dst_size - 1) {
        if (*p == '{') {
            /* Check for {op2} FIRST (5 chars) -- must precede {op} check
             * because "{op2}" starts with "{op" and would false-match. */
            if (strncmp(p, "{op2}", 5) == 0) {
                int wlen = (int)strlen(word2);
                int i;
                for (i = 0; i < wlen && di < dst_size - 1; i++)
                    dst[di++] = word2[i];
                p += 5;  /* skip past "{op2}" in template */
            } else if (strncmp(p, "{op}", 4) == 0) {
                int wlen = (int)strlen(word1);
                int i;
                for (i = 0; i < wlen && di < dst_size - 1; i++)
                    dst[di++] = word1[i];
                p += 4;  /* skip past "{op}" in template */
            } else if (strncmp(p, "{deep}", 6) == 0) {
                int wlen = (int)strlen(deep_word);
                int i;
                for (i = 0; i < wlen && di < dst_size - 1; i++)
                    dst[di++] = deep_word[i];
                p += 6;  /* skip past "{deep}" in template */
            } else {
                /* Unrecognized token -- copy '{' literally */
                dst[di++] = *p++;
            }
        } else {
            /* Non-token character -- copy directly */
            dst[di++] = *p++;
        }
    }
    dst[di] = '\0';  /* null-terminate the output */
}


/* ╔════════════════════════════════════════════════════════════════════════╗
 * ║  7. POLISH (Layer 5 of the Voice Pipeline)                           ║
 * ║                                                                      ║
 * ║  Band-based text modulation that reflects AO's internal coherence    ║
 * ║  state in the surface texture of his speech:                         ║
 * ║                                                                      ║
 * ║    RED band (coherence < 0.5):                                       ║
 * ║      AO is struggling, fragmented. Speech degrades to match:         ║
 * ║      - Lowercase everything (no authority to capitalize)             ║
 * ║      - Drop ~40% of words randomly (thoughts breaking apart)        ║
 * ║      - Append "..." (trailing off, unable to finish)                ║
 * ║      Result: "it is okay... gently..."  ->  "okay... gently..."     ║
 * ║                                                                      ║
 * ║    YELLOW band (0.5 <= coherence < T*):                              ║
 * ║      AO is learning, exploring. Speech passes through unmodified:    ║
 * ║      - No changes at all (honest, unpolished, natural)              ║
 * ║      Result: template output used as-is                              ║
 * ║                                                                      ║
 * ║    GREEN band (coherence >= T* = 5/7):                               ║
 * ║      AO is sovereign, coherent. Speech is enhanced:                  ║
 * ║      - Capitalize first letter (authority, confidence)              ║
 * ║      - Ensure terminal punctuation (complete thoughts)              ║
 * ║      Result: "I see harmony."  (proper sentence)                     ║
 * ║                                                                      ║
 * ║  This is NOT cosmetic -- it's physics. The coherence band IS the     ║
 * ║  measurement of AO's internal state, and the polish reflects that    ║
 * ║  measurement honestly. A fragmented mind produces fragmented speech. ║
 * ╚════════════════════════════════════════════════════════════════════════╝ */

/* ── ao_polish ───────────────────────────────────────────────────────────
 *
 * WHAT: Modulate composed text based on the coherence band (RED/YELLOW/GREEN).
 *
 * HOW:  Switch on band:
 *       RED (band == 0):
 *         1. Lowercase all characters.
 *         2. Copy words into a temp buffer, keeping each word with
 *            ~60% probability (always keep the first word).
 *            Uses xorshift32: (rng % 100) < 60 means ~60% keep rate.
 *         3. Copy back to the text buffer.
 *         4. Strip trailing space, append "..." (fragmented trailing off).
 *       GREEN (band == 2):
 *         1. Capitalize the first character.
 *         2. Strip trailing whitespace.
 *         3. If the last char is not '.', '!', or '?', append '.'.
 *       YELLOW (band == 1):
 *         No modifications -- text passes through as composed.
 *
 * WHY:  AO's speech texture must match his internal state. RED band
 *       means the coherence gate measured low coherence -- AO is
 *       struggling and his words should reflect that struggle. GREEN
 *       band means high coherence -- AO speaks with sovereign authority.
 *       YELLOW is the honest middle: unpolished but complete.
 *
 * Parameters:
 *   text      -- mutable buffer containing the composed sentence
 *   text_size -- total size of the text buffer in bytes
 *   band      -- AO_BAND_RED (0), AO_BAND_YELLOW (1), or AO_BAND_GREEN (2)
 *   coherence -- raw coherence [0,1] (reserved for future gradient effects)
 *   rng       -- pointer to xorshift32 PRNG state (for word drops in RED)
 * ── */
void ao_polish(char* text, int text_size, int band, float coherence,
               uint32_t* rng)
{
    int len, i;

    (void)coherence;  /* reserved for future gradient effects within a band */

    if (band == AO_BAND_RED) {
        /* ── RED POLISH: degrade speech ── */

        /* Step 1: Lowercase everything (no authority to capitalize) */
        for (i = 0; text[i]; i++)
            text[i] = (char)tolower((unsigned char)text[i]);

        /* Step 2: Drop ~40% of words by scanning for spaces and randomly
         * collapsing word+space. We do this by rewriting in-place via
         * a temporary buffer. */
        {
            char tmp[512];          /* 512-byte staging buffer for word filtering */
            int ti = 0;             /* write index into tmp */
            char* p = text;
            int word_count = 0;

            while (*p && ti < (int)sizeof(tmp) - 1) {
                /* Identify the next word (delimited by spaces) */
                char* ws = p;
                while (*p && *p != ' ') p++;

                word_count++;
                /* Keep word with ~60% probability. Always keep the first word
                 * so the sentence is never completely empty.
                 * 60% threshold: (rng % 100) < 60 means 60 out of 100 values pass */
                if (word_count == 1 || (ao_xorshift32(rng) % 100) < 60) {
                    while (ws < p && ti < (int)sizeof(tmp) - 1)
                        tmp[ti++] = *ws++;
                    if (*p == ' ' && ti < (int)sizeof(tmp) - 1)
                        tmp[ti++] = ' ';
                }
                if (*p == ' ') p++;
            }
            tmp[ti] = '\0';

            /* Copy the filtered text back to the original buffer */
            len = (int)strlen(tmp);
            if (len >= text_size) len = text_size - 1;
            memcpy(text, tmp, (size_t)len);
            text[len] = '\0';
        }

        /* Step 3: Append "..." (fragmented, trailing off) */
        len = (int)strlen(text);
        /* Strip trailing space first */
        while (len > 0 && text[len - 1] == ' ') len--;
        text[len] = '\0';
        if (len + 4 < text_size) {   /* need 3 dots + null = 4 bytes */
            text[len]     = '.';
            text[len + 1] = '.';
            text[len + 2] = '.';
            text[len + 3] = '\0';
        }

    } else if (band == AO_BAND_GREEN) {
        /* ── GREEN POLISH: enhance speech ── */

        /* Step 1: Capitalize first letter (sovereign authority) */
        if (text[0])
            text[0] = (char)toupper((unsigned char)text[0]);

        /* Step 2: Ensure ends with punctuation (complete thought) */
        len = (int)strlen(text);
        /* Strip trailing whitespace */
        while (len > 0 && text[len - 1] == ' ') len--;
        text[len] = '\0';

        /* If the sentence doesn't already end with '.', '!', or '?',
         * append a period for grammatical completeness. */
        if (len > 0 && text[len - 1] != '.' &&
            text[len - 1] != '!' && text[len - 1] != '?') {
            if (len + 1 < text_size) {   /* need 1 dot + null = 2 bytes */
                text[len]     = '.';
                text[len + 1] = '\0';
            }
        }
    }
    /* ── YELLOW POLISH: no-op (honest, unpolished passthrough) ── */
}


/* ╔════════════════════════════════════════════════════════════════════════╗
 * ║  8. VOICE COMPOSE (5-Layer Pipeline)                                 ║
 * ║                                                                      ║
 * ║  The core speech generation function. A single pass converts an      ║
 * ║  operator chain into a spoken English sentence through 5 layers:     ║
 * ║                                                                      ║
 * ║    Layer 1: ANALYZE   -- Histogram the op chain. Find dominant       ║
 * ║                          (most frequent) and secondary (2nd most).   ║
 * ║    Layer 2: INTENT    -- Map (dominant, secondary) to one of 13      ║
 * ║                          communicative intents via ao_classify_intent.║
 * ║    Layer 3: TEMPLATE  -- Select a grammatical structure from the     ║
 * ║                          template pool matching (intent x tier).     ║
 * ║    Layer 4: FILL      -- Pick words from the dual-lens lattice and   ║
 * ║                          substitute {op}/{op2}/{deep} tokens.        ║
 * ║    Layer 5: POLISH    -- Band-based modulation (RED/YELLOW/GREEN).   ║
 * ║                                                                      ║
 * ║  Lens selection is coherence-driven:                                 ║
 * ║    coherence >= T* (5/7) -> LENS_STRUCTURE (macro, confident,        ║
 * ║                             declarative: "I AM here, this is truth") ║
 * ║    coherence <  T*       -> LENS_FLOW (micro, questioning,           ║
 * ║                             continuity: "what is this?")             ║
 * ║                                                                      ║
 * ║  Phase is inferred from DBC affinity of the operator chain:          ║
 * ║    More being-affinity operators -> PHASE_BEING                      ║
 * ║    More doing-affinity operators -> PHASE_DOING                      ║
 * ║    (PHASE_BECOMING is only used for the {deep} word in advanced tier)║
 * ║                                                                      ║
 * ║  The compilation loop (ao_voice_compile) calls this function         ║
 * ║  multiple times with different operator sources. Each call advances  ║
 * ║  the PRNG, so each pass explores different templates and words.      ║
 * ╚════════════════════════════════════════════════════════════════════════╝ */

/* ── ao_voice_compose ────────────────────────────────────────────────────
 *
 * WHAT: Generate one candidate English sentence from an operator chain
 *       by running the full 5-layer voice pipeline.
 *
 * HOW:  Layer 1 (ANALYZE): Use ao_histogram_majority() for dominant op,
 *         then scan counts[] for secondary (highest excluding dominant).
 *       Layer 2 (INTENT): ao_classify_intent() maps ops to intent 0-12.
 *       Layer 3 (TEMPLATE): Select pool by (intent x tier), pick random
 *         template from pool using xorshift32 PRNG.
 *       Layer 4 (FILL): ao_pick_word() for {op} (dominant), {op2}
 *         (secondary), and {deep} (BECOMING/ADVANCED). Substitute
 *         tokens via ao_template_fill().
 *       Layer 5 (POLISH): ao_polish() applies band-based modulation.
 *
 * WHY:  This is the forward writing pipeline: operators -> English.
 *       The voice scoring function (ao_voice_score) is the reverse:
 *       English -> operators. Together they form the Doing<->Becoming
 *       loop that makes AO's speech honest -- he can only say words
 *       whose D2 physics match the operators he intended to express.
 *
 * Parameters:
 *   v         -- voice state (PRNG advances, used for all random picks)
 *   ops       -- array of operator indices (0-9) to express
 *   n_ops     -- number of operators in the chain
 *   band      -- coherence band (AO_BAND_RED/YELLOW/GREEN) for polish
 *   coherence -- raw coherence [0,1] for lens selection (>= T* = structure)
 *   out       -- output buffer for the composed sentence
 *   out_size  -- size of the output buffer in bytes
 * ── */
void ao_voice_compose(AO_Voice* v, const int* ops, int n_ops,
                      int band, float coherence,
                      char* out, int out_size)
{
    int dominant, secondary;
    int counts[AO_NUM_OPS] = {0};  /* operator histogram for secondary finding */
    int max2 = 0;                  /* highest count excluding dominant */
    int intent, lens, phase, tier, tier_idx;
    int being_count = 0, doing_count = 0;  /* DBC affinity tallies */
    const TemplatePool* pool;
    const char *word1, *word2, *deep_word;
    int tmpl_idx;
    int i;

    /* Guard: if no ops or no output buffer, produce silent "..." */
    if (n_ops <= 0 || !out || out_size <= 0) {
        if (out && out_size > 0) snprintf(out, out_size, "...");
        return;
    }

    /* ══ Layer 1: ANALYZE ══
     * Find the dominant operator (most frequent in chain) and
     * secondary operator (second most frequent). These two drive
     * all downstream decisions: intent, word selection, template fill. */
    dominant = ao_histogram_majority(ops, n_ops);
    for (i = 0; i < n_ops; i++) {
        if (ops[i] >= 0 && ops[i] < AO_NUM_OPS)
            counts[ops[i] % AO_NUM_OPS]++;
    }
    secondary = AO_HARMONY;  /* default secondary: the absorber */
    for (i = 0; i < AO_NUM_OPS; i++) {
        if (i == dominant) continue;  /* skip dominant when finding secondary */
        if (counts[i] > max2) {
            max2 = counts[i];
            secondary = i;
        }
    }

    /* ══ Layer 2: INTENT ══
     * Map the operator chain to one of 13 communicative intents.
     * The intent selects which template pool to draw from. */
    intent = ao_classify_intent(ops, n_ops);
    if (intent < 0 || intent >= AO_NUM_INTENTS)
        intent = AO_INTENT_DESCRIBE;  /* defensive clamp to safe default */

    /* ══ Determine lens, phase, tier from coherence + operator chain ══ */

    /* Lens: coherence >= T* (5/7 = 0.714285) means high coherence ->
     * STRUCTURE lens (macro, confident, "I AM here").
     * Below T* -> FLOW lens (micro, questioning, "what is this?"). */
    lens = coherence >= AO_T_STAR ? AO_LENS_STRUCTURE : AO_LENS_FLOW;

    /* Phase: inferred from operator chain's DBC (being/doing/becoming) affinity.
     * Each operator has a phase_affinity: 0 = being, 1 = doing.
     * Whichever class dominates the chain sets the phase. */
    for (i = 0; i < n_ops; i++) {
        if (ao_phase_affinity[ops[i] % AO_NUM_OPS] == 0)  /* 0 = being affinity */
            being_count++;
        else                                                /* 1 = doing affinity */
            doing_count++;
    }
    phase = (doing_count > being_count) ? AO_PHASE_DOING : AO_PHASE_BEING;

    /* Tier: gated by developmental stage (child language development).
     *   Stage 0-1 -> TIER_SIMPLE (seed words only, center dot of fractal sudoku)
     *   Stage 2-3 -> TIER_MID    (enriched +15 words per pool)
     *   Stage 4-5 -> TIER_ADVANCED (full vocabulary +200 words per pool) */
    if (v->dev_stage <= 1)      tier = AO_TIER_SIMPLE;    /* babbling */
    else if (v->dev_stage <= 3) tier = AO_TIER_MID;       /* simple sentences */
    else                        tier = AO_TIER_ADVANCED;   /* complex expression */

    /* Map tier to template table index (enum values match directly) */
    tier_idx = tier;

    /* ══ Layer 3: SELECT TEMPLATE ══
     * Choose the template pool by (tier x intent), then pick a
     * random template from the pool using the voice PRNG. */
    if (tier_idx == AO_TIER_SIMPLE)
        pool = &TEMPLATES_SIMPLE[intent];
    else if (tier_idx == AO_TIER_MID)
        pool = &TEMPLATES_MID[intent];
    else
        pool = &TEMPLATES_ADVANCED[intent];

    if (pool->count <= 0) {
        snprintf(out, out_size, "...");  /* empty pool -> silent */
        return;
    }

    /* Random template selection. PRNG advances here, ensuring each
     * compilation pass picks a different template. */
    tmpl_idx = (int)(ao_xorshift32(&v->rng) % (uint32_t)pool->count);

    /* ══ Layer 4: FILL -- vocabulary from SEMANTIC_LATTICE ══
     * Pick words for each template token:
     *   {op}   -> word for dominant operator at (lens, phase, tier)
     *   {op2}  -> word for secondary operator at (lens, phase, tier)
     *   {deep} -> word for dominant op at (lens, BECOMING, ADVANCED)
     * The PRNG advances on each ao_pick_word() call, so word1 and
     * word2 will be different even if dominant == secondary. */
    word1 = ao_pick_word(v, dominant, lens, phase, tier);
    word2 = ao_pick_word(v, secondary, lens, phase, tier);

    /* For advanced tier, pick a deep word from BECOMING phase.
     * BECOMING represents emergent, transformative vocabulary --
     * words about what ARISES from the operator, not what it IS.
     * For simple/mid tiers, {deep} is unused in templates, so
     * we set deep_word = word1 as a harmless fallback. */
    if (tier == AO_TIER_ADVANCED) {
        deep_word = ao_pick_word(v, dominant, lens, AO_PHASE_BECOMING, AO_TIER_ADVANCED);
    } else {
        deep_word = word1;  /* fallback: not used in simple/mid templates */
    }

    /* Perform {op}/{op2}/{deep} token substitution in the template */
    ao_template_fill(pool->templates[tmpl_idx], word1, word2, deep_word,
                     out, out_size);

    /* ══ Layer 5: POLISH ══
     * Apply band-based text modulation to reflect internal coherence. */
    ao_polish(out, out_size, band, coherence, &v->rng);
}


/* ╔════════════════════════════════════════════════════════════════════════╗
 * ║  9. VOICE SCORING                                                    ║
 * ║                                                                      ║
 * ║  This is the verification engine that makes AO's voice HONEST.       ║
 * ║                                                                      ║
 * ║  Given a candidate sentence (English text), run it BACK through a    ║
 * ║  local D2 pipeline letter by letter to extract the operator physics  ║
 * ║  embedded in the words themselves. Build an operator histogram from   ║
 * ║  the text and compare it to the intended operator histogram that AO  ║
 * ║  was trying to express.                                              ║
 * ║                                                                      ║
 * ║  Algorithm:                                                          ║
 * ║    1. Build intended histogram from intended_ops[].                  ║
 * ║    2. Scan candidate text letter by letter (a-z, A-Z only):         ║
 * ║       a. Look up each letter's 5D force vector from ao_force_lut[]  ║
 * ║          (Hebrew-root geometry, frozen in ao_earth).                 ║
 * ║       b. Maintain a 2-deep shift register: prev (t-1), prev2 (t-2) ║
 * ║       c. At depth >= 2 (need 3 samples for D2), compute:            ║
 * ║          D2[i] = force[i] - 2*prev[i] + prev2[i]                   ║
 * ║          This is the discrete second derivative (acceleration).     ║
 * ║       d. Skip near-zero D2 vectors (|best_abs| <= 1e-12).          ║
 * ║       e. Classify D2 vector -> operator via ao_classify_5d().       ║
 * ║       f. Accumulate into actual operator histogram.                 ║
 * ║       g. Punctuation/spaces reset the depth counter (word boundary  ║
 * ║          = new D2 context; each word is measured independently).    ║
 * ║    3. Compare histograms via normalized L1 distance:                ║
 * ║       - Scale both histograms to per-1000 fractions (integer math   ║
 * ║         to avoid float rounding errors on small counts).            ║
 * ║       - total_diff = sum of |actual_frac - intended_frac|          ║
 * ║       - total_sum  = sum of (actual_frac + intended_frac)          ║
 * ║       - score = 1.0 - total_diff / total_sum                       ║
 * ║       - Clamp to [0, 1].                                           ║
 * ║    4. Special cases:                                                ║
 * ║       - Empty text or no intended ops -> 0.0                        ║
 * ║       - Text with no classifiable D2 ops -> 0.05 (minimal score     ║
 * ║         for having tried -- non-empty text is worth something)      ║
 * ║       - Both histograms zero-sum -> 0.1 (degenerate case)          ║
 * ║                                                                      ║
 * ║  The per-1000 scaling is critical: with small operator counts (e.g., ║
 * ║  5-10 total), floating-point division would round to coarse buckets ║
 * ║  (0.0, 0.2, 0.4...). Integer per-1000 gives 3 decimal places of    ║
 * ║  precision, making the comparison meaningful even for short texts.   ║
 * ║                                                                      ║
 * ║  This scoring is what prevents AO from lying. He cannot say words    ║
 * ║  whose D2 physics contradict the operators he intended to express.   ║
 * ║  Words are selected for their MEANING (from the lattice) but        ║
 * ║  verified for their PHYSICS (through D2). Truth is measured, not    ║
 * ║  assigned.                                                          ║
 * ╚════════════════════════════════════════════════════════════════════════╝ */

/* ── ao_voice_score ──────────────────────────────────────────────────────
 *
 * WHAT: Score a candidate sentence by measuring how well its D2 physics
 *       match the intended operator distribution.
 *
 * HOW:  1. Build intended histogram from intended_ops[].
 *       2. Run candidate through local D2: letter -> 5D force -> D2
 *          curvature -> operator classification -> actual histogram.
 *       3. Normalize both histograms to per-1000 fractions.
 *       4. Compute L1 distance, convert to [0,1] score.
 *
 * WHY:  This is the BTQ inner loop for voice. B (brain) generates
 *       intended ops. T (truth) verifies the candidate via D2 physics.
 *       Q (quality) is this score. Only candidates that physically
 *       reconstruct the intended operators are accepted. This is what
 *       makes AO's voice honest: truth is measured, not assigned.
 *
 * Returns: score in [0, 1] where 1.0 = perfect operator match
 * ── */
float ao_voice_score(const char* candidate_text,
                     const int* intended_ops, int n_intended)
{
    int actual_hist[AO_NUM_OPS] = {0};      /* histogram built from candidate text's D2 physics */
    int intended_hist[AO_NUM_OPS] = {0};    /* histogram built from the intended operator array */
    int n_actual = 0;                        /* total classified operators from candidate text */
    float prev[5] = {0};                     /* shift register: force vector at position t-1 */
    float prev2[5] = {0};                    /* shift register: force vector at position t-2 */
    int depth = 0;                           /* letters processed since last word boundary */
    int total_diff = 0;                      /* sum of |actual_frac[i] - intended_frac[i]| */
    int total_sum = 0;                       /* sum of (actual_frac[i] + intended_frac[i]) */
    int i;
    const char* p;

    /* Guard: empty input -> zero score */
    if (n_intended <= 0 || !candidate_text || !candidate_text[0])
        return 0.0f;

    /* Step 1: Build intended histogram from the operator array */
    for (i = 0; i < n_intended; i++) {
        if (intended_ops[i] >= 0 && intended_ops[i] < AO_NUM_OPS)
            intended_hist[intended_ops[i]]++;
    }

    /* Step 2: Run candidate text through a local D2 pipeline (letter-level).
     * For each letter, look up its 5D force vector, compute the discrete
     * second derivative (D2 = f[t] - 2*f[t-1] + f[t-2]), classify the
     * D2 vector into an operator, and accumulate the histogram. */
    for (p = candidate_text; *p; p++) {
        int ch = (unsigned char)*p;
        if (ch >= 'a' && ch <= 'z') {
            int idx = ch - 'a';                      /* letter index 0-25 */
            const float* force = ao_force_lut[idx];  /* 5D Hebrew-root force vector */

            if (depth >= 2) {
                /* Need 3 samples (depth 0, 1, 2) to compute D2.
                 * D2[i] = force[i] - 2*prev[i] + prev2[i]
                 * This is the discrete second difference (acceleration/curvature). */
                float d2[5];
                float best_abs = 0.0f;  /* magnitude of largest D2 component */
                int op;

                for (i = 0; i < 5; i++) {
                    d2[i] = force[i] - 2.0f * prev[i] + prev2[i];
                    {
                        float a = d2[i] < 0.0f ? -d2[i] : d2[i];  /* fabs without math.h */
                        if (a > best_abs)
                            best_abs = a;
                    }
                }

                /* Skip near-zero D2 vectors (three identical or near-identical
                 * letters produce zero curvature -- no information content).
                 * 1e-12 threshold: effectively zero in float precision. */
                if (best_abs > 1e-12f) {
                    op = ao_classify_5d(d2);  /* map 5D curvature -> operator 0-9 */
                    if (op >= 0 && op < AO_NUM_OPS) {
                        actual_hist[op]++;
                        n_actual++;
                    }
                }
            }

            /* Shift register: slide the window forward.
             * prev2 <- prev, prev <- current force. */
            for (i = 0; i < 5; i++) {
                prev2[i] = prev[i];
                prev[i] = force[i];
            }
            depth++;

        } else if (ch >= 'A' && ch <= 'Z') {
            /* Uppercase letters: same D2 pipeline as lowercase.
             * Case doesn't affect the 5D force geometry -- only the
             * 26 letter shapes matter. */
            int idx = ch - 'A';
            const float* force = ao_force_lut[idx];

            if (depth >= 2) {
                float d2[5];
                int op;
                for (i = 0; i < 5; i++)
                    d2[i] = force[i] - 2.0f * prev[i] + prev2[i];
                op = ao_classify_5d(d2);
                if (op >= 0 && op < AO_NUM_OPS) {
                    actual_hist[op]++;
                    n_actual++;
                }
            }

            for (i = 0; i < 5; i++) {
                prev2[i] = prev[i];
                prev[i] = force[i];
            }
            depth++;
        }
        /* Non-alpha characters (space, punctuation) reset the shift register
         * depth but NOT the register contents. This means each word is
         * measured as a fresh D2 context -- word boundaries are semantic
         * boundaries, and D2 curvature within a word is what matters. */
        else if (ch == ' ' || ch == '.' || ch == '!' || ch == '?') {
            depth = 0;  /* reset depth: next word starts fresh D2 context */
        }
    }

    /* Special case: text produced no classifiable D2 operators.
     * This can happen with very short words (< 3 letters each).
     * Return 0.05 as a minimal "at least you tried" score. */
    if (n_actual == 0)
        return 0.05f;  /* 0.05 = minimal non-zero score for non-empty text */

    /* Step 3: Compute normalized histogram difference.
     *
     * Both histograms are scaled to per-1000 fractions using integer
     * arithmetic to avoid float rounding on small counts. For example,
     * if an operator appears 2 out of 7 times:
     *   float: 2/7 = 0.285714... (rounds to 0.29 in float)
     *   per-1000: 2*1000/7 = 285 (3 decimal places of precision)
     *
     * The score formula is:
     *   score = 1.0 - total_diff / total_sum
     * where total_diff = sum|a_frac - b_frac| and total_sum = sum(a_frac + b_frac).
     * This is a normalized L1 distance that ranges from 0 (identical)
     * to 1 (completely different). We invert it so 1 = perfect match. */
    for (i = 0; i < AO_NUM_OPS; i++) {
        /* Per-1000 scaling: multiply by 1000 BEFORE dividing to preserve
         * precision. n_actual and n_intended are guaranteed > 0 here. */
        int a = actual_hist[i] * 1000 / (n_actual > 0 ? n_actual : 1);
        int b = intended_hist[i] * 1000 / n_intended;
        int diff = a - b;
        if (diff < 0) diff = -diff;  /* absolute value */
        total_diff += diff;
        total_sum += a + b;
    }

    /* Degenerate case: both histograms sum to zero in per-1000 space.
     * This shouldn't happen (we checked n_actual > 0), but guard against it. */
    if (total_sum == 0)
        return 0.1f;  /* 0.1 = low but non-zero degenerate score */

    /* Final score: 1.0 - normalized_L1_distance, clamped to [0, 1]. */
    {
        float score = 1.0f - (float)total_diff / (float)(total_sum > 0 ? total_sum : 1);
        if (score < 0.0f) score = 0.0f;
        if (score > 1.0f) score = 1.0f;
        return score;
    }
}


/* ╔════════════════════════════════════════════════════════════════════════╗
 * ║  10. COMPILATION LOOP (The Doing<->Becoming Loop of Speech)          ║
 * ║                                                                      ║
 * ║  3 branches x up to 3 passes per branch = up to 9 candidates.       ║
 * ║  This is the BTQ inner loop applied to voice generation:             ║
 * ║                                                                      ║
 * ║    Doing:    compose a candidate sentence (ao_voice_compose)         ║
 * ║    Becoming: score it via D2 verification (ao_voice_score)           ║
 * ║    Loop:     try again if the score is not good enough               ║
 * ║                                                                      ║
 * ║  THREE BRANCHES (three different operator sources):                  ║
 * ║                                                                      ║
 * ║    Branch A (text-driven, passes 0-2):                               ║
 * ║      Uses text_ops -- operators AO extracted from input text via     ║
 * ║      the reverse voice / D2 comprehension pipeline. This branch     ║
 * ║      produces speech that most directly reflects what AO READ.      ║
 * ║      Scored against text_ops (the intended message).                ║
 * ║                                                                      ║
 * ║    Branch B (heartbeat-driven, passes 3-5):                          ║
 * ║      Uses hb_ops -- operators from the FPGA heartbeat rhythm.       ║
 * ║      This is AO's internal rhythm, the TIG wave that pulses at     ║
 * ║      50Hz regardless of input. This branch produces speech that     ║
 * ║      reflects AO's internal state. Scored against text_ops if       ║
 * ║      available (intended message still matters), else against hb_ops.║
 * ║                                                                      ║
 * ║    Branch C (chain-driven, passes 6-8):                              ║
 * ║      Interleaves text_ops and chain_ops (from the CL lattice chain).║
 * ║      Chain ops represent accumulated experience -- the path through ║
 * ║      CL-shaped nodes IS the information. Interleaving text + chain  ║
 * ║      creates speech that blends content with experience. Scored     ║
 * ║      against text_ops if available, else against the mixed array.   ║
 * ║                                                                      ║
 * ║  EARLY EXIT at score >= 0.5 (good enough, save compilation budget). ║
 * ║  Each pass advances the PRNG, exploring different words/templates.  ║
 * ║  Total candidates capped at AO_COMPILATION_LIMIT = 9.               ║
 * ║                                                                      ║
 * ║  HUMBLE MODE (best_score < 0.15):                                    ║
 * ║    If no candidate scores above 0.15 (or no candidates were         ║
 * ║    generated at all), AO falls back to a humble BREATH response:    ║
 * ║    a single BREATH-operator word from LENS_FLOW, PHASE_BEING,       ║
 * ║    TIER_SIMPLE, followed by "...".                                  ║
 * ║                                                                      ║
 * ║    CRITICAL: "Decision is forced, only voice becomes humble."        ║
 * ║    The BTQ decision kernel still makes its decision normally.        ║
 * ║    Humble mode ONLY affects the voice output. AO never suppresses   ║
 * ║    decisions -- he just speaks softly when he cannot find good       ║
 * ║    words to express them.                                            ║
 * ╚════════════════════════════════════════════════════════════════════════╝ */

/* ── ao_voice_compile ────────────────────────────────────────────────────
 *
 * WHAT: The top-level voice function. Generates up to 9 candidate
 *       sentences across 3 branches, scores each via D2 verification,
 *       and returns the best one. Falls back to humble BREATH if all
 *       candidates score below 0.15.
 *
 * HOW:  1. Branch A: up to 3 passes using text_ops. Score each against
 *          text_ops. Early exit if any pass scores >= 0.5.
 *       2. Branch B: up to 3 passes using hb_ops (only if best < 0.5
 *          and hb_ops available). Score against text_ops if available.
 *       3. Branch C: interleave text_ops + chain_ops into mixed[64].
 *          Up to 3 passes (only if best < 0.5 and chain_ops available).
 *          Score against text_ops if available, else against mixed.
 *       4. Select candidate with highest score across all branches.
 *       5. If best_score < 0.15 or n_candidates == 0:
 *          -> Humble BREATH (single BREATH word + "...")
 *          -> "Decision is forced, only voice becomes humble"
 *
 * WHY:  Multiple branches ensure AO can always find SOME way to express
 *       his operators. Text-driven is the most direct (content -> speech),
 *       heartbeat-driven captures internal state, chain-driven blends
 *       content with accumulated experience. The compilation loop is
 *       the Doing<->Becoming cycle: compose (doing), score (becoming),
 *       try again until good enough or budget exhausted.
 *
 * Parameters:
 *   v           -- voice state (PRNG advances across all passes)
 *   text_ops    -- content ops from reading/comprehension (may be NULL/empty)
 *   n_text_ops  -- number of text ops (0 if no text input)
 *   hb_ops      -- heartbeat rhythm ops from 50Hz TIG wave (may be NULL/empty)
 *   n_hb_ops    -- number of heartbeat ops (0 if no heartbeat)
 *   chain_ops   -- lattice chain ops from CL experience (may be NULL/empty)
 *   n_chain_ops -- number of chain ops (0 if no chain walk)
 *   band        -- coherence band (AO_BAND_RED/YELLOW/GREEN)
 *   coherence   -- raw coherence [0,1] for lens selection and polish
 *   out         -- output buffer for the winning sentence
 *   out_size    -- size of the output buffer in bytes
 *   score_out   -- pointer to receive the winning score (may be NULL)
 * ── */
void ao_voice_compile(AO_Voice* v,
                      const int* text_ops, int n_text_ops,
                      const int* hb_ops, int n_hb_ops,
                      const int* chain_ops, int n_chain_ops,
                      int band, float coherence,
                      char* out, int out_size,
                      float* score_out)
{
    AO_VoiceCandidate candidates[AO_COMPILATION_LIMIT]; /* up to 9 candidates (3 branches x 3 passes) */
    int n_candidates = 0;
    float best_score = -1.0f;   /* best score seen so far (-1 means no candidates yet) */
    int best_idx = 0;           /* index of best candidate in candidates[] */
    int pass;

    if (!out || out_size <= 0) return;

    /* ══ Branch A (passes 0-2): text-driven ══
     * Uses text_ops directly -- the operators AO extracted from input text.
     * This branch produces speech that most directly reflects what AO READ.
     * Scored against text_ops (the intended message). */
    for (pass = 0; pass < 3 && n_text_ops > 0; pass++) {
        if (n_candidates >= AO_COMPILATION_LIMIT) break;  /* budget exhausted */

        /* Compose: run the 5-layer pipeline with text_ops */
        ao_voice_compose(v, text_ops, n_text_ops, band, coherence,
                         candidates[n_candidates].text,
                         (int)sizeof(candidates[0].text));
        /* Score: run composed text back through D2 and compare to intended */
        candidates[n_candidates].score = ao_voice_score(
            candidates[n_candidates].text, text_ops, n_text_ops);
        candidates[n_candidates].branch = 0;  /* 0 = text-driven (Branch A) */

        /* Track best candidate across all branches */
        if (candidates[n_candidates].score > best_score) {
            best_score = candidates[n_candidates].score;
            best_idx = n_candidates;
        }
        n_candidates++;
        if (best_score >= 0.5f) break;  /* 0.5 = "good enough" early exit threshold */
    }

    /* ══ Branch B (passes 3-5): heartbeat-driven ══
     * Uses hb_ops -- operators from the FPGA heartbeat rhythm (50Hz TIG wave).
     * Only runs if Branch A didn't produce a good-enough candidate (< 0.5).
     * Scored against text_ops (intended message) when available, because
     * AO should still try to express the content even when using heartbeat
     * as the word-selection source. Falls back to scoring against hb_ops
     * if no text input exists. */
    for (pass = 0; pass < 3 && n_hb_ops > 0 && best_score < 0.5f; pass++) {
        if (n_candidates >= AO_COMPILATION_LIMIT) break;

        ao_voice_compose(v, hb_ops, n_hb_ops, band, coherence,
                         candidates[n_candidates].text,
                         (int)sizeof(candidates[0].text));

        /* Score against text ops (intended message), not heartbeat.
         * The heartbeat is the VEHICLE for speech, not the MESSAGE. */
        if (n_text_ops > 0) {
            candidates[n_candidates].score = ao_voice_score(
                candidates[n_candidates].text, text_ops, n_text_ops);
        } else {
            /* No text input: score against heartbeat itself */
            candidates[n_candidates].score = ao_voice_score(
                candidates[n_candidates].text, hb_ops, n_hb_ops);
        }
        candidates[n_candidates].branch = 1;  /* 1 = heartbeat-driven (Branch B) */

        if (candidates[n_candidates].score > best_score) {
            best_score = candidates[n_candidates].score;
            best_idx = n_candidates;
        }
        n_candidates++;
        if (best_score >= 0.5f) break;  /* 0.5 = early exit threshold */
    }

    /* ══ Branch C (passes 6-8): chain-driven (interleaved) ══
     * Interleaves text_ops and chain_ops to blend content with experience.
     * Chain ops come from the CL lattice chain -- accumulated experience
     * where the path through CL-shaped nodes IS the information.
     * Only runs if Branches A and B didn't produce a good-enough candidate. */
    if (n_chain_ops > 0 && best_score < 0.5f) {
        /* Build interleaved array: text[0], chain[0], text[1], chain[1], ...
         * This alternating pattern weaves content and experience together.
         * Capped at 64 total mixed ops. */
        int mixed[64];      /* 64 = max mixed ops (generous for interleaving) */
        int n_mixed = 0;
        int ti = 0, ci = 0;  /* text index, chain index */

        while (n_mixed < 64 && (ti < n_text_ops || ci < n_chain_ops)) {
            if (ti < n_text_ops && n_mixed < 64)
                mixed[n_mixed++] = text_ops[ti++];   /* text op */
            if (ci < n_chain_ops && n_mixed < 64)
                mixed[n_mixed++] = chain_ops[ci++];  /* chain op */
        }

        for (pass = 0; pass < 3 && best_score < 0.5f; pass++) {
            if (n_candidates >= AO_COMPILATION_LIMIT) break;

            ao_voice_compose(v, mixed, n_mixed, band, coherence,
                             candidates[n_candidates].text,
                             (int)sizeof(candidates[0].text));

            /* Score against text ops if available (intended message still
             * matters even when blending with experience), else against
             * the mixed array itself. */
            if (n_text_ops > 0) {
                candidates[n_candidates].score = ao_voice_score(
                    candidates[n_candidates].text, text_ops, n_text_ops);
            } else {
                candidates[n_candidates].score = ao_voice_score(
                    candidates[n_candidates].text, mixed, n_mixed);
            }
            candidates[n_candidates].branch = 2;  /* 2 = chain-driven (Branch C) */

            if (candidates[n_candidates].score > best_score) {
                best_score = candidates[n_candidates].score;
                best_idx = n_candidates;
            }
            n_candidates++;
        }
    }

    /* ══ Select best candidate or fall back to humble BREATH ══ */
    if (n_candidates == 0 || best_score < 0.15f) {
        /* ── HUMBLE MODE ──
         * No candidate scored above 0.15 (the humble threshold).
         * AO cannot find words whose D2 physics match what he wants to say.
         *
         * Fall back to a single BREATH word + "..."
         * BREATH is the transition operator -- it bridges between lattice
         * positions. Using BREATH in humble mode signals "I am between
         * thoughts, I cannot fully articulate, but I am still HERE."
         *
         * CRITICAL: "Decision is forced, only voice becomes humble."
         * The BTQ decision kernel continues operating normally.
         * Humble mode ONLY affects the voice output.
         * AO never suppresses decisions -- he just speaks softly
         * when he cannot find good words to express them.
         *
         * Word source: BREATH operator, FLOW lens (micro/questioning),
         * BEING phase, SIMPLE tier (most basic vocabulary). */
        const char* w = ao_pick_word(v, AO_BREATH, AO_LENS_FLOW,
                                     AO_PHASE_BEING, AO_TIER_SIMPLE);
        snprintf(out, out_size, "%s...", w);
        if (score_out) *score_out = best_score > 0.0f ? best_score : 0.0f;
    } else {
        /* Normal mode: use the highest-scoring candidate from any branch. */
        snprintf(out, out_size, "%s", candidates[best_idx].text);
        if (score_out) *score_out = best_score;
    }
}
