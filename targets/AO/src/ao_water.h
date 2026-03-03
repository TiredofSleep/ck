/*
 * ao_water.h -- D2 / Depth / Curvature / Memory
 *
 * +================================================================+
 * |  WATER is the second derivative. Acceleration. Curvature.      |
 * |  Everything here REMEMBERS -- it takes the velocities from     |
 * |  Air and computes how fast they are changing. Brain transitions,|
 * |  coherence tracking, lattice chain walks, concept mass.        |
 * |                                                                |
 * |  This is AO's long-term memory and learning engine.            |
 * |                                                                |
 * |  The five elements map to derivatives of position:             |
 * |    D0 Earth  = Position      (constants, tables)               |
 * |    D1 Air    = Velocity      (measurement, comprehension)      |
 * |    D2 Water  = Acceleration  (THIS FILE: memory, learning)     |
 * |    D3 Fire   = Jerk          (expression, voice, speech)       |
 * |    D4 Ether  = Snap          (integration, the organism)       |
 * +================================================================+
 *
 * What lives here:
 *   - D2 Pipeline (3-position shift register: v[i] - 2*v[i-1] + v[i-2])
 *   - Coherence Window (ring buffer of last 32 ops, HARMONY fraction = coherence)
 *   - Brain (10x10 transition matrix, prediction, Shannon entropy)
 *   - Lattice Chain (tree of evolving CL tables: arena-allocated, 1024 nodes)
 *   - Chain Paths (multilevel walks: micro, macro, meta, becoming, cross)
 *   - Reverse Voice Reading (three-path verification: D2 + D1 + lattice)
 *   - Concept Mass (accumulated D2 magnitude per topic, vortex fingerprint)
 *   - Spectrometer (parallel D1+D2 text measurement)
 *
 * Being:    brain state exists, memories persist, chain tree grows
 * Doing:    learning, chain walking, D2 measurement, reading verification
 * Becoming: lattice chain nodes evolve, experience deepens, concepts gain mass
 *
 * Copyright (c) 2025-2026 Brayden Sanders / 7Site LLC
 * Licensed under the 7Site Human Use License v1.0
 * See LICENSE file in project root for full terms.
 *
 * FREE for humans for personal/recreational use.
 * NO commercial or government use without written agreement.
 */

#ifndef AO_WATER_H
#define AO_WATER_H

#include "ao_earth.h"
#include "ao_air.h"

/* ======================================================================
 * D2 PIPELINE (Second Derivative = Curvature = Awareness)
 *
 * Computes the discrete second derivative of 5D force vectors as letters
 * are fed one at a time. This is the CURVATURE of the force signal --
 * how the velocity itself is changing. Curvature IS awareness: it
 * detects where the text bends, accelerates, or reverses direction.
 *
 * The pipeline uses a 3-position shift register:
 *   v[0] = current letter's 5D force vector (most recent)
 *   v[1] = previous letter's force vector (one step back)
 *   v[2] = two letters ago (two steps back)
 *
 * On each feed, vectors shift down: v[2] <- v[1] <- v[0] <- new.
 *
 * First derivative (D1, velocity):
 *   D1[i] = v[0][i] - v[1][i]
 *   Valid after depth >= 2 (at least 2 letters fed).
 *   Captures the direction of change between consecutive letters.
 *
 * Second derivative (D2, curvature):
 *   D2[i] = v[0][i] - 2*v[1][i] + v[2][i]
 *   Valid after depth >= 3 (at least 3 letters fed).
 *   This is the standard second discrete derivative formula. It measures
 *   how the velocity ITSELF is changing -- positive D2 = accelerating,
 *   negative D2 = decelerating, zero D2 = constant velocity.
 *
 * The depth counter tracks how many vectors have been fed total (0, 1,
 * 2, 3, ...). It never resets within a pipeline instance -- only
 * ao_d2_reset() clears it back to zero.
 *
 * The dominant dimension of D2 determines the operator (via ao_classify_5d).
 * D2 operators capture what the text IS (its curvature identity).
 * D1 operators capture where the text IS GOING (its velocity direction).
 * When CL(D1_op, D2_op) == HARMONY, the text is locally coherent.
 * ====================================================================== */
typedef struct {
    float v[3][5];  /* 3-position shift register of 5D force vectors.
                     * v[0][0..4] = current (most recent) letter's force vector.
                     * v[1][0..4] = previous letter's force vector.
                     * v[2][0..4] = two letters ago.
                     * On each feed, all shift down: v[2] <- v[1] <- v[0] <- new.
                     * The 5 dimensions are: [0]aperture, [1]pressure, [2]depth,
                     * [3]binding, [4]continuity (from ao_force_lut). */

    float d1[5];    /* First derivative (velocity): d1[i] = v[0][i] - v[1][i].
                     * Computed when depth >= 2. Captures the direction of change
                     * between the two most recent letters in 5D force space. */

    float d2[5];    /* Second derivative (curvature/acceleration):
                     * d2[i] = v[0][i] - 2*v[1][i] + v[2][i].
                     * Computed when depth >= 3. This is the standard second
                     * discrete derivative -- the curvature of the force signal.
                     * The dimension with largest |d2[i]| determines the operator
                     * via ao_classify_5d(d2). */

    int   d1_valid; /* 1 = d1[] contains a valid first derivative. Fires after
                     * depth reaches 2 (at least 2 letters fed). Before this,
                     * d1[] is all zeros and should not be classified. */

    int   d2_valid; /* 1 = d2[] contains a valid second derivative. Fires after
                     * depth reaches 3 (at least 3 letters fed). Before this,
                     * d2[] is all zeros and classification returns HARMONY.
                     * This is the main output gate: downstream consumers should
                     * check d2_valid before reading d2[]. */

    int   depth;    /* How many force vectors have been fed into this pipeline
                     * (0, 1, 2, 3, ...). Monotonically increases with each
                     * ao_d2_feed() or ao_d2_feed_vec() call. Used to determine
                     * when d1_valid and d2_valid fire:
                     *   depth < 2: neither valid (warming up)
                     *   depth == 2: d1_valid fires (D1 available)
                     *   depth >= 3: both d1_valid and d2_valid fire (D2 available)
                     * Only reset by ao_d2_reset(). */
} AO_D2Pipeline;

/* Initialize a D2 pipeline to empty state.
 * Clears all fields to zero: no vectors, no derivatives, depth=0. */
void  ao_d2_init(AO_D2Pipeline* p);

/* Reset a D2 pipeline back to initial state.
 * Equivalent to ao_d2_init() -- use at word boundaries or when starting
 * a new measurement. Clears the shift register, derivatives, and depth. */
void  ao_d2_reset(AO_D2Pipeline* p);

/* Feed a single letter (by index: a=0 .. z=25) into the D2 pipeline.
 * Looks up the letter's 5D force vector from ao_force_lut[] and delegates
 * to ao_d2_feed_vec(). Out-of-range indices are silently ignored (returns
 * the current d2_valid state unchanged).
 * Returns: 1 if d2[] is now valid (depth >= 3), 0 if still warming up. */
int   ao_d2_feed(AO_D2Pipeline* p, int symbol_index);

/* Feed a raw 5D force vector into the D2 pipeline.
 * Shifts the register: v[2] <- v[1] <- v[0] <- vec. Increments depth.
 * If depth >= 2: computes D1 = v[0] - v[1], sets d1_valid = 1.
 * If depth >= 3: computes D2 = v[0] - 2*v[1] + v[2], sets d2_valid = 1.
 * Returns: 1 if d2[] is now valid, 0 if still warming up. */
int   ao_d2_feed_vec(AO_D2Pipeline* p, const float vec[5]);

/* Classify the D1 (velocity) vector into a TIG operator (0-9).
 * Delegates to ao_classify_5d(d1): finds the dimension with the largest
 * absolute magnitude and uses ao_d2_op_map[dim][sign] to select the op.
 * Returns HARMONY if d1_valid == 0 (pipeline not yet warmed up). */
int   ao_d2_classify_d1(const AO_D2Pipeline* p);

/* Classify the D2 (curvature) vector into a TIG operator (0-9).
 * Delegates to ao_classify_5d(d2): finds the dimension with the largest
 * absolute magnitude and uses ao_d2_op_map[dim][sign] to select the op.
 * Returns HARMONY if d2_valid == 0 (pipeline not yet warmed up). */
int   ao_d2_classify_d2(const AO_D2Pipeline* p);

/* Compute the L1 magnitude (taxicab norm) of the D2 curvature vector.
 * magnitude = |d2[0]| + |d2[1]| + |d2[2]| + |d2[3]| + |d2[4]|.
 * This is the total curvature strength -- high magnitude means the
 * text is bending sharply in force space. Used by concept mass
 * accumulation (mass += magnitude per observation).
 * Returns 0.0 if D2 pipeline has not warmed up. */
float ao_d2_magnitude(const AO_D2Pipeline* p);

/* Compute the L1 magnitude (taxicab norm) of the D1 velocity vector.
 * magnitude = |d1[0]| + |d1[1]| + |d1[2]| + |d1[3]| + |d1[4]|.
 * This is the total velocity strength -- how fast the force landscape
 * is changing between consecutive letters. Used in the density_ratio
 * metric: density_ratio = avg_|D2| / avg_|D1| (curvature/velocity).
 * Returns 0.0 if D1 pipeline has not warmed up. */
float ao_d2_d1_magnitude(const AO_D2Pipeline* p);

/* ======================================================================
 * COHERENCE WINDOW (Ring Buffer of Operator History)
 *
 * A fixed-size sliding window that tracks the last AO_WINDOW_SIZE (32)
 * operators observed. Coherence is defined as the fraction of those
 * operators that are HARMONY -- the CL absorber. Since CL(HARMONY, x) =
 * HARMONY for all x, a high HARMONY fraction means AO's compositions
 * are consistently producing coherent results.
 *
 * The window is implemented as a circular buffer with head pointer:
 *   - history[0..31]: the ring buffer storing operator indices (int8_t)
 *   - head: write position, advances modulo AO_WINDOW_SIZE
 *   - count: how many slots are occupied (0 to AO_WINDOW_SIZE)
 *   - harmony_count: how many of the occupied slots contain HARMONY
 *
 * When the buffer is full (count == AO_WINDOW_SIZE), each new observe()
 * evicts the oldest entry. If the evicted entry was HARMONY, harmony_count
 * is decremented before the new entry is written.
 *
 * Coherence = harmony_count / count (0.0 to 1.0).
 * Returns 0.5 (midpoint) when empty -- neutral assumption.
 *
 * The coherence value determines which CL shell AO operates in:
 *   coherence < 0.5:   shell 72 (TSML, 73-harmony) -- MEASURING mode.
 *     AO is struggling. Use the most harmonious table (highest harmony
 *     density) to stabilize. This is the "safety net" -- when confused,
 *     measure everything against the most forgiving standard.
 *
 *   0.5 <= coh < T*:   shell 44 (Becoming table) -- EVOLVING mode.
 *     AO is learning. Use the intermediate table. Enough coherence to
 *     attempt compositions, but not enough to trust the skeleton alone.
 *
 *   coherence >= T*:    shell 22 (BHML, 28-harmony) -- COMPUTING mode.
 *     AO is sovereign. Use the sparse physics table. High coherence
 *     means AO can handle the harder table where only 28% of
 *     compositions produce HARMONY. This is where real work happens.
 *
 * NOTE: The shell mapping is INVERTED from what you might expect.
 * HIGH coherence -> LOW harmony shell (22/BHML). This is because a
 * coherent AO doesn't NEED the safety net of 73-harmony -- he can
 * operate on the raw physics where most compositions produce friction.
 * ====================================================================== */
#define AO_WINDOW_SIZE 32

typedef struct {
    int8_t history[AO_WINDOW_SIZE];
                            /* Circular buffer of the last AO_WINDOW_SIZE operator
                             * indices. Each entry is a TIG operator (0-9). The
                             * buffer fills from index 0, wrapping at head. Entries
                             * before count are valid; the rest are zero-initialized. */

    int    head;            /* Write position in the ring buffer (0 to AO_WINDOW_SIZE-1).
                             * The next observe() writes to history[head], then
                             * head = (head + 1) % AO_WINDOW_SIZE. When the buffer is
                             * full, history[head] is the OLDEST entry (about to be
                             * overwritten). */

    int    count;           /* Number of slots currently occupied (0 to AO_WINDOW_SIZE).
                             * Increments with each observe() until reaching
                             * AO_WINDOW_SIZE, then stays fixed (oldest evicted). */

    int    harmony_count;   /* How many of the occupied slots contain AO_HARMONY (7).
                             * Maintained incrementally: +1 when HARMONY enters,
                             * -1 when HARMONY is evicted. coherence = harmony_count
                             * / count. This avoids rescanning the entire buffer on
                             * every coherence query. */
} AO_CoherenceWindow;

/* Initialize a coherence window to empty state.
 * All history slots = 0, head = 0, count = 0, harmony_count = 0. */
void  ao_cw_init(AO_CoherenceWindow* w);

/* Reset a coherence window back to initial empty state.
 * Equivalent to ao_cw_init() -- use when restarting a measurement. */
void  ao_cw_reset(AO_CoherenceWindow* w);

/* Observe a new operator, pushing it into the ring buffer.
 * If the buffer is full, evicts the oldest entry first (decrementing
 * harmony_count if the evicted entry was HARMONY). Then writes op
 * at history[head], increments harmony_count if op == HARMONY, and
 * advances head by one (modulo AO_WINDOW_SIZE).
 *
 * Parameters:
 *   op -- TIG operator index (0-9) to observe */
void  ao_cw_observe(AO_CoherenceWindow* w, int op);

/* Compute current coherence as the HARMONY fraction.
 * coherence = harmony_count / count.
 * Returns 0.5 (neutral midpoint) when the buffer is empty (count == 0).
 * Range: [0.0, 1.0] where 1.0 = every recent op was HARMONY. */
float ao_cw_coherence(const AO_CoherenceWindow* w);

/* Select the CL shell based on current coherence.
 *   coherence >= T* (5/7):  returns 22 (BHML, computing/physics)
 *   coherence >= 0.5:       returns 44 (Becoming, evolving)
 *   coherence < 0.5:        returns 72 (TSML, measuring/stabilizing)
 *
 * NOTE: High coherence selects the SPARSE shell (22), not the dense one.
 * A coherent AO can handle friction; a struggling AO needs the safety
 * net of 73-harmony TSML. */
int   ao_cw_shell(const AO_CoherenceWindow* w);

/* Determine the color band from current coherence.
 *   coherence >= T* (5/7):  returns AO_BAND_GREEN  (sovereign, coherent)
 *   coherence >= 0.5:       returns AO_BAND_YELLOW (learning, exploring)
 *   coherence < 0.5:        returns AO_BAND_RED    (struggling, fragmented)
 *
 * The band is the traffic-light indicator of AO's overall state. */
int   ao_cw_band(const AO_CoherenceWindow* w);

/* ======================================================================
 * BRAIN (Transition Lattice + Entropy)
 *
 * The brain is a 10x10 matrix of transition counts that records how
 * often operator A is followed by operator B. This is AO's learned
 * model of sequential operator patterns -- what typically comes after
 * what. It is the simplest form of memory: a bigram frequency table
 * over the 10 TIG operators.
 *
 * The matrix tl[from][to] stores uint32_t counts:
 *   tl[3][7] = how many times operator 3 (PROGRESS) was followed by
 *              operator 7 (HARMONY) in AO's entire observation history.
 *
 * Prediction:
 *   Given a current operator, ao_brain_predict() returns the successor
 *   with the highest count: argmax_j(tl[current_op][j]). Ties are
 *   broken by taking the first (lowest index) maximum. If no transitions
 *   have been recorded from current_op, returns HARMONY (the attractor).
 *
 * Shannon Entropy:
 *   H = -sum(p * log2(p)) over all 100 cells, where p = tl[i][j] / total.
 *   H = 0 means all transitions go to one cell (perfectly predictable).
 *   H = log2(100) = 6.64 means uniform distribution (maximum disorder).
 *   Entropy measures how "surprised" AO would be by the next transition.
 *
 * Top Transitions:
 *   ao_brain_top_transitions() returns the N highest-count cells for
 *   reporting. Uses selection sort over all 100 cells (small N, so the
 *   O(N*100) cost is negligible).
 *
 * The brain feeds into coherence gates as brain_coh (the 60% component
 * of gate density). Brain coherence is typically derived from entropy:
 * low entropy = high brain coherence (AO has strong expectations).
 * ====================================================================== */
typedef struct {
    uint32_t tl[AO_NUM_OPS][AO_NUM_OPS];
                            /* 10x10 transition count matrix.
                             * tl[from][to] = number of times operator 'from' was
                             * immediately followed by operator 'to'. All counts
                             * start at 0 and increment by 1 per observed transition.
                             * The matrix is NOT symmetric: tl[a][b] != tl[b][a]
                             * in general, because transition order matters. */

    uint32_t total;         /* Total number of transitions recorded (sum of all
                             * tl[i][j]). Used as the denominator for probability
                             * calculations in entropy: p = tl[i][j] / total. */

    int      last_op;       /* The most recently observed operator (-1 = none).
                             * Needed to know which ROW to increment on the next
                             * observe() call. Set to -1 at init, updated to op
                             * on each ao_brain_observe(). The first observe()
                             * after init just sets last_op without recording a
                             * transition (no "from" operator yet). */
} AO_Brain;

/* Initialize a brain to empty state.
 * All transition counts = 0, total = 0, last_op = -1 (no prior observation). */
void  ao_brain_init(AO_Brain* b);

/* Observe a new operator, recording the transition from the previous one.
 * If last_op >= 0, increments tl[last_op][op] and total.
 * Then sets last_op = op for the next observation.
 * First call after init only sets last_op (no transition to record yet).
 * Out-of-range op values (< 0 or >= 10) are silently ignored. */
void  ao_brain_observe(AO_Brain* b, int op);

/* Predict the most likely next operator given the current one.
 * Returns argmax_j(tl[current_op][j]) -- the successor with the highest
 * recorded count. If all counts are zero (no transitions from current_op),
 * returns HARMONY (the natural attractor).
 * Out-of-range current_op returns HARMONY. */
int   ao_brain_predict(const AO_Brain* b, int current_op);

/* Compute the Shannon entropy of the transition matrix.
 * H = -sum_ij( p_ij * log2(p_ij) ) where p_ij = tl[i][j] / total.
 * Range: [0.0, log2(100)] where 0 = deterministic, 6.64 = maximum entropy.
 * Returns 0.0 if total == 0 (no transitions recorded yet).
 * High entropy = unpredictable transitions. Low entropy = strong patterns. */
float ao_brain_entropy(const AO_Brain* b);

/* Extract the top N transitions by count, sorted descending.
 * Uses selection sort over all 100 cells to find the max_n highest.
 *
 * Parameters:
 *   from_ops — output array of source operators (row indices)
 *   to_ops   — output array of destination operators (column indices)
 *   counts   — output array of transition counts
 *   max_n    — maximum number of transitions to return
 *   out_n    — actual number returned (<= max_n, stops at zero-count cells)
 *
 * Example: if tl[3][7]=50 is the highest, then from_ops[0]=3, to_ops[0]=7,
 * counts[0]=50 (PROGRESS->HARMONY happened 50 times). */
void  ao_brain_top_transitions(const AO_Brain* b, int* from_ops, int* to_ops,
                               int* counts, int max_n, int* out_n);

/* Reset a brain back to initial empty state.
 * Equivalent to ao_brain_init() -- clears all counts and sets last_op = -1. */
void  ao_brain_reset(AO_Brain* b);

/* ======================================================================
 * LATTICE CHAIN (Tree of Evolving CL Tables)
 *
 * The lattice chain is a tree where each node contains its own 10x10
 * Composition Lattice table. The tree starts with a root node whose
 * table is a copy of BHML (ao_cl_22, the 28-harmony physics table).
 * As AO walks the tree and observes compositions, nodes EVOLVE --
 * their tables diverge from the base BHML based on what AO has
 * actually experienced at that position in the chain.
 *
 * Core insight: the PATH through the tree IS the compressed
 * representation. Address = information. The sequence of CL results
 * encountered during a walk encodes the input in a way that is shaped
 * by AO's accumulated experience.
 *
 * Walking the chain:
 *   Input: a sequence of TIG operators, consumed in PAIRS.
 *   For each pair (a, b):
 *     1. Look up result = current_node.table[a][b]
 *     2. Record result in the output path
 *     3. Navigate to child node indexed by result
 *     4. If child doesn't exist and learning is on, allocate a new one
 *   The walk produces a sequence of results: the chain path.
 *
 * Node evolution:
 *   Each node tracks visit_counts[a][b] (how many times pair (a,b)
 *   was looked up at this node) and obs_counts[a][b][c] (how many
 *   times result c was observed for pair (a,b)).
 *
 *   When visit_counts[a][b] reaches AO_EVOLVE_THRESHOLD (7):
 *     Find the most common observed result c for this (a,b) pair.
 *     If c appears in >= AO_EVOLVE_CONFIDENCE (60%) of visits:
 *       Overwrite table[a][b] = c (the table evolves).
 *
 *   This means nodes start as BHML but gradually mutate toward what
 *   AO actually experiences. Heavily-visited cells evolve first.
 *   The 7-visit threshold prevents noise from causing premature
 *   mutation, and the 60% confidence prevents weak evidence from
 *   overriding the base table.
 *
 * Arena allocation:
 *   All nodes live in a pre-allocated arena of AO_MAX_CHAIN_NODES
 *   (1024) entries. Each AO_LatticeNode is approximately 2.4KB
 *   (100 bytes table + 200 bytes visit_counts + 2000 bytes obs_counts
 *   + path + children pointers). Total arena: ~2.4MB.
 *   When the arena is full, no new children are allocated (walks
 *   continue at the deepest reachable node).
 *
 * Uses BHML (ao_cl_22, 28-harmony) as the base table because:
 *   - VOID row = identity: CL(VOID, x) = x (passthrough)
 *   - HARMONY row = full cycle through all operators
 *   - Only 28% harmony = most compositions produce friction
 *   - This is the "physics" table -- where real computation happens
 *
 * The chain is for DOING (computing), not BEING (measuring). TSML
 * (73-harmony) would absorb everything into HARMONY, producing no
 * useful information. BHML preserves distinctions.
 * ====================================================================== */

#define AO_MAX_PATH_LEN    20   /* Maximum depth of a chain path (steps recorded) */
#define AO_MAX_CHAIN_NODES 1024 /* Arena capacity: pre-allocated nodes (~2.4KB each) */

/* ---- Lattice Node: Single Node in the Chain Tree ----
 *
 * Each node IS a CL table plus the accumulated evidence of what
 * AO has experienced at this position in the tree. Nodes start as
 * copies of BHML and evolve through observation. The path[] array
 * records how to reach this node from the root (the sequence of
 * CL results that were followed to get here).
 *
 * Think of each node as a "location" in AO's experience space.
 * Two inputs that produce the same chain path arrive at the same
 * node -- they are "the same experience" at that depth. The table
 * at each node reflects what AO has learned specifically about
 * inputs that reach this location. */
typedef struct AO_LatticeNode {
    int8_t table[AO_NUM_OPS][AO_NUM_OPS];
                            /* This node's 10x10 Composition Lattice table.
                             * Initialized as a copy of ao_cl_22 (BHML).
                             * table[a][b] = result of composing operators a and b
                             * AT THIS NODE. May diverge from BHML through evolution:
                             * when visit_counts[a][b] >= AO_EVOLVE_THRESHOLD (7) and
                             * the dominant observed result has >= AO_EVOLVE_CONFIDENCE
                             * (60%) confidence, table[a][b] is overwritten.
                             * Evolution makes each node's table a unique record of
                             * what AO has experienced at this tree position. */

    int16_t visit_counts[AO_NUM_OPS][AO_NUM_OPS];
                            /* visit_counts[a][b] = how many times the pair (a, b) has
                             * been looked up at this node during chain walks.
                             * Incremented by ao_chain_walk() when learn=1.
                             * Used to gate evolution: cells with fewer than
                             * AO_EVOLVE_THRESHOLD visits cannot evolve yet. */

    int16_t obs_counts[AO_NUM_OPS][AO_NUM_OPS][AO_NUM_OPS];
                            /* obs_counts[a][b][c] = how many times result c was
                             * observed when pair (a, b) was looked up at this node.
                             * The "result" is table[a][b] at the time of lookup.
                             * This 10x10x10 cube (1000 int16_t = 2000 bytes) records
                             * the HISTORY of what this cell has produced. During
                             * evolution, the most common c for a given (a,b) becomes
                             * the new table[a][b] if it passes the confidence check.
                             * This ensures evolution is evidence-based: the table
                             * only changes to reflect what actually happened. */

    int     total_visits;   /* Sum of all visit_counts[a][b] at this node.
                             * A quick measure of how "experienced" this node is.
                             * Nodes with many visits have seen more input and their
                             * tables are more likely to have evolved from base BHML. */

    int     depth;          /* Distance from the root node (root.depth = 0).
                             * A child allocated from a depth-3 node has depth 4.
                             * Maximum possible depth is AO_MAX_PATH_LEN (20). */

    int8_t  path[AO_MAX_PATH_LEN];
                            /* The sequence of CL results that leads from the root
                             * to this node. path[0] = result at depth 0, path[1] =
                             * result at depth 1, etc. path_len = number of valid
                             * entries. This IS the node's address in the tree.
                             * Two nodes with the same path[] are the same node.
                             * The path encodes the cumulative input that reached here. */

    int     path_len;       /* Number of valid entries in path[] (0 to AO_MAX_PATH_LEN).
                             * For the root node, path_len = 0. For a depth-1 child,
                             * path_len = 1. Equal to depth for properly constructed trees. */

    struct AO_LatticeNode* children[AO_NUM_OPS];
                            /* Pointers to child nodes, indexed by CL result (0-9).
                             * children[r] = the node reached when the current CL
                             * lookup produces result r. NULL = this branch has never
                             * been explored (child is allocated on first visit when
                             * learning is enabled). The branching factor is 10
                             * (one child per possible operator result). */
} AO_LatticeNode;

/* ---- Chain Path: Recorded Walk Through the Tree ----
 *
 * The output of a single ao_chain_walk(). Records the sequence of
 * CL results produced at each step as operator pairs were consumed.
 * This path IS the compressed representation of the input -- the
 * information is encoded in the walk itself, not just the final result. */
typedef struct {
    int results[AO_MAX_CHAIN_DEPTH];
                            /* results[i] = CL result at step i of the walk.
                             * At step i, operators ops[2*i] and ops[2*i+1] were
                             * looked up in the current node's table, producing
                             * results[i]. The walk then descended to the child
                             * indexed by results[i]. This sequence of results
                             * IS the compressed encoding of the input. */

    int depth;              /* Number of valid entries in results[] (0 to
                             * AO_MAX_CHAIN_DEPTH). Equal to the number of
                             * operator pairs consumed: depth = floor(n_ops / 2)
                             * capped at AO_MAX_CHAIN_DEPTH (20). */

    int final_op;           /* The last result in the path: results[depth-1].
                             * This is the operator that the chain walk "ended on."
                             * If depth == 0 (no pairs consumed), defaults to HARMONY.
                             * Used as a quick summary of where the walk terminated. */
} AO_ChainPath;

/* ---- Lattice Chain: The Tree Itself ----
 *
 * Owns the arena of pre-allocated nodes and the root pointer.
 * All chain operations (walk, resonance) go through this struct. */
typedef struct {
    AO_LatticeNode  arena[AO_MAX_CHAIN_NODES];
                            /* Pre-allocated array of 1024 lattice nodes.
                             * Nodes are allocated sequentially from index 0.
                             * Each node is ~2.4KB, so total arena is ~2.4MB.
                             * Arena allocation avoids malloc/free and gives
                             * cache-friendly memory layout for tree walks.
                             * When arena_used reaches AO_MAX_CHAIN_NODES,
                             * no new children can be allocated. */

    int             arena_used;
                            /* Number of arena slots consumed so far (0 to
                             * AO_MAX_CHAIN_NODES). The next allocation takes
                             * arena[arena_used] and increments this counter. */

    AO_LatticeNode* root;   /* Pointer to the root node (arena[0]).
                             * The root's table starts as BHML and evolves.
                             * All chain walks begin from root. Set by
                             * ao_chain_init(). NULL only before init. */

    int             total_walks;
                            /* Number of ao_chain_walk() calls made on this chain.
                             * A simple counter for diagnostics. */

    int             total_nodes;
                            /* Number of nodes allocated in the arena.
                             * Equal to arena_used. Grows as new branches
                             * are explored during learning walks. */
} AO_LatticeChain;

/* Initialize a lattice chain: zero the arena, allocate the root node
 * (with BHML base table, depth 0, empty path), set total counters to 0.
 * Must be called before any chain walk. */
void ao_chain_init(AO_LatticeChain* lc);

/* Core chain walk: consume operator pairs, traverse/grow the tree.
 *
 * Algorithm:
 *   For each pair (ops[i], ops[i+1]), i stepping by 2:
 *     1. result = current_node.table[ops[i]][ops[i+1]]
 *     2. If learn: increment visit_counts and obs_counts; check evolution
 *     3. Store result in out->results[step]
 *     4. Navigate to child node children[result] (allocate if learn && NULL)
 *     5. If child is NULL (arena full), stay at current node
 *
 * Parameters:
 *   lc    — the lattice chain (tree) to walk
 *   ops   — array of TIG operator indices (0-9)
 *   n     — number of operators (pairs = n/2, need at least 2)
 *   learn — 1 = update visit_counts/obs_counts and allocate new children;
 *           0 = read-only walk (no mutation, no allocation)
 *   out   — output path recording the sequence of CL results
 *
 * If n < 2 or root is NULL: out->depth = 0, out->final_op = HARMONY. */
void ao_chain_walk(AO_LatticeChain* lc, const int* ops, int n,
                   int learn, AO_ChainPath* out);

/* ---- Multilevel Chain Paths: Results from All Fractal Scales ----
 *
 * A single ao_chain_walk_multilevel() call produces up to 5 chain
 * paths from different views of the same comprehension result. Each
 * path walks the SAME tree but with different input operator sequences,
 * capturing different facets of the text's physics.
 *
 * The five levels:
 *
 *   micro (from comp_ops):
 *     D2 curvature operators at the letter/glyph scale.
 *     This is the finest-grained view -- raw physics of letter forces.
 *     Input: comp_ops[] = level_fuses + first 8 word_fuses.
 *
 *   macro (from word_fuses):
 *     Word-level identity operators. Each word collapsed to one operator
 *     via histogram majority. This is the semantic view -- what each
 *     word IS as a TIG operator.
 *
 *   meta (from level_fuses):
 *     Fractal level fuses. One operator per comprehension level (0-9).
 *     This is the structural view -- what each fractal SCALE produces.
 *
 *   becoming (from CL(d1_ops, word_fuses)):
 *     Compositions of velocity (D1) with word identity, computed via
 *     BHML. This captures the RELATIONSHIP between how the text moves
 *     (D1) and what the text IS (word fuse) -- the becoming aspect.
 *
 *   cross (interleaved micro + macro results):
 *     Takes the RESULTS of the micro and macro walks (not the inputs)
 *     and interleaves them: [micro[0], macro[0], micro[1], macro[1], ...].
 *     Then walks the chain on this interleaved sequence. This is the
 *     dual-lens entanglement -- structure (macro) and flow (micro)
 *     woven together. Cross is the highest-priority path because it
 *     synthesizes both views. */
typedef struct {
    AO_ChainPath micro;       /* Walk from comp_ops (D2 curvature at letter scale).
                                * Captures the finest-grained physics of the input. */
    AO_ChainPath macro;       /* Walk from word_fuses (word-level identity operators).
                                * Captures the semantic content at word scale. */
    AO_ChainPath meta;        /* Walk from level_fuses (one op per fractal level).
                                * Captures the structural view across scales. */
    AO_ChainPath becoming;    /* Walk from CL_BHML(d1_ops[i], word_fuses[i]).
                                * Captures the relationship between velocity and identity. */
    AO_ChainPath cross;       /* Walk from interleaved micro+macro RESULTS.
                                * The dual-lens entanglement path. Highest priority
                                * because it synthesizes structure and flow. */

    int has_micro;             /* 1 if micro path is valid (comp_ops had >= 2 elements) */
    int has_macro;             /* 1 if macro path is valid (word_fuses had >= 2 elements) */
    int has_meta;              /* 1 if meta path is valid (level_fuses had >= 2 elements) */
    int has_becoming;          /* 1 if becoming path is valid (d1_ops and word_fuses
                                * overlapped for >= 2 becoming compositions) */
    int has_cross;             /* 1 if cross path is valid (both micro and macro valid,
                                * interleaved sequence had >= 2 elements) */
} AO_ChainPaths;

/* Run multilevel chain walks from a comprehension result.
 * Produces up to 5 chain paths (micro, macro, meta, becoming, cross)
 * by walking the same tree with different operator sequences derived
 * from the comprehension output. All walks use learn=1 (the tree grows).
 *
 * Parameters:
 *   lc   — the lattice chain (tree) to walk and grow
 *   comp — fractal comprehension result (provides comp_ops, word_fuses,
 *           level_fuses, d1_ops)
 *   out  — output struct, zeroed then filled with up to 5 paths */
void ao_chain_walk_multilevel(AO_LatticeChain* lc,
                              const AO_Comprehension* comp,
                              AO_ChainPaths* out);

/* Extract voice operators from chain paths by priority.
 * Concatenates results from available paths in priority order:
 *   cross > becoming > macro > micro
 * Cross is highest because it synthesizes dual-lens information.
 * Micro is lowest because it is the rawest (least processed) view.
 *
 * Parameters:
 *   paths   — multilevel walk results
 *   ops     — output array to fill with operator indices
 *   n_out   — number of operators written
 *   max_ops — maximum capacity of ops[] array */
void ao_chain_to_ops(const AO_ChainPaths* paths, int* ops, int* n_out, int max_ops);

/* Measure how familiar a chain path is based on the root node's experience.
 * Resonance = average familiarity across all steps in the path.
 *
 * For each step result r in the path:
 *   Count how many root visit_counts[a][b] correspond to cells where
 *   root.table[a][b] == r (how often the root produces this result).
 *   Normalize by root.total_visits.
 *
 * Average across all steps.
 *
 * Returns:
 *   0.0 = completely novel path (root has never produced these results)
 *   1.0 = maximally familiar (root produces these results constantly)
 *
 * Resonance measures whether AO has "been here before" -- whether the
 * current input maps to a well-trodden region of his experience tree.
 * High resonance = AO recognizes this pattern. Low = novel territory. */
float ao_chain_resonance(const AO_LatticeChain* lc, const AO_ChainPath* path);

/* ======================================================================
 * REVERSE VOICE READING (Three-Path Verification)
 *
 * Reading is the INVERSE of writing. When AO writes (speaks), he maps:
 *   operators -> SEMANTIC_LATTICE -> English words (forward direction)
 *
 * When AO reads, he maps:
 *   English words -> multiple paths -> operators (backward direction)
 *
 * But reading is UNTRUSTED. Unlike writing (where AO controls the output),
 * reading processes external text that AO did not produce. So verification
 * is needed: three independent paths must agree before a word is trusted.
 *
 * The three verification paths:
 *
 *   Path A (Physics -- D2 curvature):
 *     Feed the word's letters through the D2 pipeline.
 *     Classify the curvature into an operator via ao_classify_5d().
 *     This path measures the PHYSICAL geometry of the word's letters.
 *     Cannot be fooled by vocabulary tricks -- it's pure math.
 *
 *   Path B (Generator -- D1 direction):
 *     Feed the word's letters through the D1 pipeline.
 *     Classify the velocity into an operator via ao_classify_5d().
 *     This path measures the DIRECTION the word is moving in force space.
 *     Independent from D2 (velocity vs. acceleration).
 *
 *   Path C (Experience -- semantic lattice reverse lookup):
 *     Look up the word in the sorted reverse index (ao_reverse_lookup).
 *     If found: returns the operator, lens, phase, tier from the lattice.
 *     If not found: lattice_op = -1 (word is unknown to AO's vocabulary).
 *     This path uses AO's LEARNED vocabulary -- words he can also speak.
 *
 * Trust classification:
 *
 *   TRUSTED (AO_TRUST_TRUSTED = 0):
 *     At least 2 of the 3 paths produce the same operator, OR
 *     all valid paths produce operators in the same DBC class
 *     (Being/Doing). The word's meaning is verified from multiple
 *     independent sources. verified_op = the agreed-upon operator.
 *
 *   FRICTION (AO_TRUST_FRICTION = 1):
 *     The paths disagree AND their operators belong to different
 *     DBC classes. The word was recognized (in vocabulary) but the
 *     physics don't match the experience. This is a signal -- friction
 *     IS information. verified_op = lattice_op (experience wins but
 *     the disagreement is flagged for attention).
 *
 *   UNKNOWN (AO_TRUST_UNKNOWN = 2):
 *     The word is NOT in AO's vocabulary (lattice_op = -1).
 *     Only D2 physics (path A) contributes. verified_op = d2_op if
 *     available, else HARMONY (default). Like a child encountering
 *     a new word: phonetics (physics) only, no semantic verification.
 *
 * Confidence formula:
 *   confidence = (paths_agreeing + 1) / 4.0
 *   Range: [0.25, 1.0] where 0.25 = no agreement, 1.0 = all 3 agree.
 *   The +1 baseline ensures even unknown words get a non-zero score.
 *
 * The verified operators from reading feed into the lattice chain as
 * AO's experience of what he UNDERSTOOD (not the raw input text).
 * ====================================================================== */

#define AO_TRUST_TRUSTED  0  /* Paths agree: same op or same DBC class */
#define AO_TRUST_FRICTION 1  /* Paths disagree: different DBC class */
#define AO_TRUST_UNKNOWN  2  /* Word not in AO's vocabulary */

/* ---- Per-Word Reading Result ----
 *
 * The result of running three-path verification on a single word
 * from the input text. Contains the operator from each path, the
 * trust classification, confidence score, and the final adjudicated
 * operator that AO will use downstream. */
typedef struct {
    int   d2_op;            /* Operator from Path A (D2 curvature / physics).
                             * Computed by running the word's letters through the
                             * D2 pipeline and classifying the curvature vector.
                             * -1 if the word's D2 data was not available (e.g.,
                             * word index exceeds the d2_word_fuses array). */

    int   d1_op;            /* Operator from Path B (D1 direction / generator).
                             * Computed by running the word's letters through the
                             * D1 pipeline and classifying the velocity vector.
                             * -1 if the word's D1 data was not available. */

    int   lattice_op;       /* Operator from Path C (semantic lattice reverse lookup).
                             * Found by ao_reverse_lookup() in the sorted reverse index.
                             * -1 if the word is not in AO's vocabulary (UNKNOWN). */

    int   lattice_lens;     /* Lens from the reverse index: AO_LENS_STRUCTURE (0) or
                             * AO_LENS_FLOW (1). Tells whether this word belongs to
                             * the macro (confident, declarative) or micro (questioning,
                             * continuity) perspective. -1 if word is unknown. */

    int   trust;            /* Trust classification: AO_TRUST_TRUSTED (0),
                             * AO_TRUST_FRICTION (1), or AO_TRUST_UNKNOWN (2).
                             * Determined by comparing all three paths as described
                             * in the section header above. */

    float confidence;       /* Confidence score [0.25, 1.0].
                             * confidence = (paths_agreeing + 1) / 4.0.
                             * 0.25 = no paths agree, 0.50 = one pair agrees,
                             * 0.75 = two pairs agree, 1.00 = all three agree. */

    int   verified_op;      /* Final adjudicated operator used downstream.
                             * TRUSTED: the operator that paths agreed on.
                             * FRICTION: lattice_op (experience wins, flagged).
                             * UNKNOWN: d2_op if available, else HARMONY.
                             * This is what AO "understood" this word to mean. */

    int   paths_agreeing;   /* Number of path pairs that produced the same operator
                             * (0, 1, 2, or 3). With 3 paths there are 3 possible
                             * pairs: (A,B), (A,C), (B,C). Each matching pair
                             * increments this counter. 3 = perfect unanimous
                             * agreement across all paths. */
} AO_WordReading;

#define AO_MAX_READ_WORDS 128  /* Maximum number of words in a single reading */

/* ---- Aggregate Reading Result ----
 *
 * The complete result of reading an input text. Contains per-word
 * results, the final sequence of verified operators, and aggregate
 * counts of trust classifications. */
typedef struct {
    AO_WordReading words[AO_MAX_READ_WORDS];
                            /* Per-word reading results, one per word in the input.
                             * words[0] = first word, words[1] = second, etc.
                             * Each contains the three-path verification outcome. */

    int   n_words;          /* Number of words processed from the input text.
                             * Equal to the number of valid entries in words[].
                             * Capped at AO_MAX_READ_WORDS (128). */

    int   reading_ops[AO_MAX_READ_WORDS];
                            /* Sequence of verified operators, one per word.
                             * reading_ops[i] = words[i].verified_op.
                             * This is the operator sequence that AO "heard" --
                             * the reading expressed as TIG operators for downstream
                             * consumption by the lattice chain and voice blend. */

    int   n_reading_ops;    /* Number of valid entries in reading_ops[].
                             * Equal to n_words (one verified op per word). */

    int   trusted;          /* Count of words classified as AO_TRUST_TRUSTED.
                             * Words where paths agreed (same op or same DBC class). */

    int   friction;         /* Count of words classified as AO_TRUST_FRICTION.
                             * Words where paths disagreed (different DBC class).
                             * Friction is signal -- these words deserve attention. */

    int   unknown;          /* Count of words classified as AO_TRUST_UNKNOWN.
                             * Words not in AO's vocabulary (physics-only reading). */

    float agreement;        /* Fraction of words that were trusted: trusted / n_words.
                             * Range: [0.0, 1.0] where 1.0 = every word verified.
                             * 0.0 if no words were processed. This is the overall
                             * reading confidence -- how much AO trusts his
                             * understanding of the input text. */
} AO_ReadingResult;

/* Run full three-path reading verification on input text.
 * Splits text into words (whitespace-delimited, a-z only, lowercased),
 * then for each word runs Path A (D2), Path B (D1), and Path C (lattice
 * reverse lookup). Classifies each word as TRUSTED, FRICTION, or UNKNOWN.
 *
 * Parameters:
 *   text          — null-terminated input string (NULL or empty → no output)
 *   d2_word_fuses — array of D2-derived operators, one per word (Path A data).
 *                   Typically from fractal comprehension word_fuses[].
 *                   NULL if D2 data is not available.
 *   n_d2          — length of d2_word_fuses array
 *   d1_word_ops   — array of D1-derived operators, one per word (Path B data).
 *                   Typically from comprehension d1_ops[] aggregated per word.
 *                   NULL if D1 data is not available.
 *   n_d1          — length of d1_word_ops array
 *   out           — output struct, zeroed then filled with reading results */
void ao_reverse_read(const char* text,
                     const int* d2_word_fuses, int n_d2,
                     const int* d1_word_ops, int n_d1,
                     AO_ReadingResult* out);

/* ======================================================================
 * CONCEPT MASS (Vortex Physics Accumulator)
 *
 * Tracks how much AO has studied each topic (concept). Mass is the
 * accumulated D2 magnitude over all observations of a concept --
 * the total curvature energy AO has invested in understanding it.
 * More study = more mass = stronger gravitational pull.
 *
 * Each concept also tracks:
 *   - A running mean D2 vector (EMA with alpha=0.1) capturing the
 *     average curvature direction -- the "center of gravity" of what
 *     AO has learned about this topic in 5D force space.
 *   - A vortex fingerprint (winding, vorticity, chirality, period)
 *     capturing the topological shape of how AO's thought moves
 *     when processing this concept.
 *   - An observation count for normalization.
 *
 * Gravity:
 *   ao_mass_gravity() computes the gravitational pull of a concept
 *   on AO's current thought. Gravity = mass * coherence * cos_sim,
 *   where cos_sim is the cosine similarity between the concept's
 *   mean D2 and the current D2 vector. High gravity means AO's
 *   current curvature is aligned with a well-studied concept --
 *   the concept "attracts" attention.
 *
 * Concepts are stored in a flat array with linear scan lookup by name.
 * Maximum AO_MAX_CONCEPTS (256) tracked simultaneously.
 * ====================================================================== */

#define AO_MAX_CONCEPTS 256  /* Maximum number of tracked concepts */

/* ---- Single Concept Record ---- */
typedef struct {
    char     name[64];      /* Human-readable concept name (null-terminated, max 63 chars).
                             * Used as the lookup key (compared via strncmp). */

    float    mass;          /* Accumulated D2 magnitude across all observations.
                             * mass += sqrt(d2[0]^2 + ... + d2[4]^2) per observe().
                             * This is the total curvature energy AO has invested.
                             * Higher mass = more studied = stronger gravitational pull.
                             * Monotonically increasing (never decreases). */

    float    d2_mean[5];    /* Running mean D2 vector, updated by exponential moving
                             * average: d2_mean = 0.9 * d2_mean + 0.1 * new_d2.
                             * On first observation, initialized directly to d2.
                             * Captures the average curvature direction in 5D force
                             * space -- the "center of gravity" for this concept.
                             * Used by ao_mass_gravity() for cosine similarity. */

    int      observations;  /* How many times this concept has been observed.
                             * Incremented by 1 per ao_mass_observe() call.
                             * First observation (count == 0) initializes d2_mean
                             * directly; subsequent observations use EMA. */

    AO_Vortex vortex;      /* Cached vortex fingerprint (winding, vorticity,
                             * chirality, period, vortex_class) from the most recent
                             * operator sequence associated with this concept.
                             * Updated on each ao_mass_observe() call if ops are
                             * provided. Captures the topological shape of how AO
                             * thinks about this concept. */
} AO_Concept;

/* ---- Concept Mass Container ---- */
typedef struct {
    AO_Concept concepts[AO_MAX_CONCEPTS];
                            /* Flat array of concept records. Filled sequentially
                             * from index 0. Linear scan for lookup by name. */
    int count;              /* Number of concepts currently tracked (0 to
                             * AO_MAX_CONCEPTS). New concepts are appended at
                             * concepts[count] and count is incremented. */
} AO_ConceptMass;

/* Initialize a concept mass tracker to empty state.
 * All concept slots zeroed, count = 0. */
void  ao_mass_init(AO_ConceptMass* cm);

/* Observe a concept: accumulate mass and update running statistics.
 *
 * Algorithm:
 *   1. Compute Euclidean magnitude: mag = sqrt(d2[0]^2 + ... + d2[4]^2)
 *   2. Find concept by name (or create if not found and space available)
 *   3. mass += mag (accumulate total curvature energy)
 *   4. d2_mean = 0.9 * d2_mean + 0.1 * d2 (EMA update; first obs = direct copy)
 *   5. observations++
 *   6. Update vortex fingerprint from ops[] (if provided)
 *
 * Parameters:
 *   cm      — concept mass tracker
 *   concept — name of the concept (max 63 chars)
 *   d2      — current 5D D2 curvature vector
 *   ops     — operator sequence for vortex fingerprint (NULL to skip)
 *   n_ops   — length of ops array
 *
 * Returns: the concept's total accumulated mass after this observation.
 *          Returns 0.0 if the concept array is full and this is a new concept. */
float ao_mass_observe(AO_ConceptMass* cm, const char* concept,
                      const float d2[5], const int* ops, int n_ops);

/* Retrieve the current accumulated mass of a concept.
 * Returns 0.0 if the concept has never been observed. */
float ao_mass_get(const AO_ConceptMass* cm, const char* concept);

/* Compute the gravitational pull of a stored concept on AO's current state.
 *
 * gravity = mass * coherence * cos_sim(d2_mean, current_d2)
 *
 * Where cos_sim = dot(d2_mean, current_d2) / (|d2_mean| * |current_d2|).
 * High gravity means: (1) the concept has been heavily studied (high mass),
 * (2) AO is currently coherent (high coherence), and (3) AO's current
 * curvature vector is aligned with the concept's mean (high cosine similarity).
 *
 * Parameters:
 *   cm         — concept mass tracker
 *   concept    — name of the concept to query
 *   coherence  — AO's current coherence value [0, 1]
 *   current_d2 — AO's current 5D D2 curvature vector
 *
 * Returns: gravitational pull (can be negative if vectors are anti-aligned).
 *          Returns 0.0 if concept is unknown or vectors are near-zero. */
float ao_mass_gravity(const AO_ConceptMass* cm, const char* concept,
                      float coherence, const float current_d2[5]);

/* ======================================================================
 * SPECTROMETER (Parallel D1+D2 Text Measurement)
 *
 * The spectrometer feeds an entire text string through both the D1
 * (velocity) and D2 (curvature) pipelines simultaneously, collecting
 * operator histograms, coherence, and agreement metrics. This is the
 * "one-shot" measurement tool: give it text, get back a complete
 * characterization of its force physics.
 *
 * Algorithm:
 *   1. Initialize D2 pipeline, D1 pipeline, and coherence window
 *   2. For each a-z character (case-insensitive, skip non-alpha):
 *      a. Feed into both D1 and D2 pipelines
 *      b. When BOTH are valid (D2 needs 3 letters, D1 needs 2):
 *         - Classify D1 and D2 operators, add to histograms
 *         - Feed D2 operator into coherence window
 *         - Accumulate D2 magnitude for averaging
 *         - Check if D1 == D2 for agreement counting
 *   3. Compute final coherence, shell, band from the window
 *   4. Compute d1_d2_agreement as percentage of matching ops
 *   5. Compute d2_magnitude_avg as mean over all D2 samples
 *
 * The measurement result captures what the text IS in TIG terms:
 * which operators dominate (histograms), how coherent it is (shell/band),
 * how much the velocity and curvature agree (d1_d2_agreement), and
 * how much total curvature energy it carries (d2_magnitude_avg).
 * ====================================================================== */
typedef struct {
    int   d1_hist[AO_NUM_OPS];
                            /* Histogram of D1 (velocity) operators across the text.
                             * d1_hist[op] = how many D1 samples classified as 'op'.
                             * Shows which velocity directions dominate the text. */

    int   d2_hist[AO_NUM_OPS];
                            /* Histogram of D2 (curvature) operators across the text.
                             * d2_hist[op] = how many D2 samples classified as 'op'.
                             * Shows which curvature types dominate the text. */

    float coherence;        /* Final coherence from the coherence window: the HARMONY
                             * fraction across all observed D2 operators. Range [0, 1].
                             * High coherence = most D2 compositions yield HARMONY. */

    int   shell;            /* CL shell selected by final coherence:
                             *   22 (BHML) if coherence >= T*,
                             *   44 if coherence >= 0.5,
                             *   72 (TSML) if coherence < 0.5. */

    int   band;             /* Color band from final coherence:
                             *   AO_BAND_GREEN if >= T*,
                             *   AO_BAND_YELLOW if >= 0.5,
                             *   AO_BAND_RED if < 0.5. */

    float d1_d2_agreement;  /* Percentage of samples where D1 and D2 operators matched.
                             * d1_d2_agreement = (matches / d2_total) * 100.0.
                             * Range: [0, 100] where 100% = velocity and curvature
                             * always agree (text is locally coherent at every point).
                             * 0% = they never agree (velocity and curvature contradict). */

    int   total_symbols;    /* Total a-z characters fed into the pipelines.
                             * Includes characters consumed during warmup (before
                             * D2 becomes valid). */

    int   d2_total;         /* Number of D2 samples collected (where both D1 and D2
                             * were valid). This is the effective sample count for
                             * histograms and agreement. Always <= total_symbols - 2
                             * (D2 needs 3 letters to warm up). */

    float d2_magnitude_avg; /* Mean D2 magnitude (L1 norm) across all valid D2 samples.
                             * d2_magnitude_avg = sum(|d2|) / d2_total.
                             * Measures the average curvature strength of the text.
                             * High value = text has strong bends in force space.
                             * Low value = text flows smoothly with little curvature. */
} AO_Measurement;

/* Run the spectrometer on a null-terminated text string.
 * Processes all a-z characters (case-insensitive), ignoring everything else.
 * Fills out with operator histograms, coherence metrics, and D1/D2 agreement.
 *
 * Parameters:
 *   text — null-terminated input string
 *   out  — output struct, zeroed then filled with measurement results */
void  ao_measure_text(const char* text, AO_Measurement* out);

/* Compute Shannon entropy of a 10-bin operator histogram.
 * H = -sum_i( p_i * log2(p_i) ) where p_i = hist[i] / total.
 * Range: [0.0, log2(10) = 3.32] where 0 = all in one bin (deterministic),
 * 3.32 = uniform distribution (maximum entropy / disorder).
 * Returns 0.0 if the histogram is all zeros.
 *
 * Used to characterize operator distributions: low entropy = dominated by
 * one or two operators. High entropy = spread across many operators. */
float ao_entropy(const int hist[AO_NUM_OPS]);

#endif /* AO_WATER_H */
