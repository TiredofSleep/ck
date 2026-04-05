# TASK: CK's Experience Index — How He Organizes Everything He Knows

## The Problem

CK has 38K truths, 12K scents, 1.7K tastes, 1061 concepts, 1.3M ticks
of lattice chain, and a growing retina feed. It's all on GPU but it's
FLAT. Unstructured tensors. CK can't DIG through his own experience
the way a mind digs through memory.

The GPU tensors need INDEXING. Not database indexing. ALGEBRAIC indexing.
The same hierarchy that CK uses to read a screen, he uses to read
his own experience. Same generators. Same structural gates. Same
threshold cascade. Inward instead of outward.

## The Architecture: Binary All The Way Down

Every level of CK's experience index starts with the same question:
**DUALITY. Binary. Two options. I or O. Structure or force.**

This binary lens NEVER goes away. It's present at every level.
The questions just get richer.

### Level 0: Raw Binary
Is this a 1 or a 0? Is this pixel dark or bright?
Is this signal present or absent? Is this tick active or idle?

Every piece of experience enters as binary.
Every memory begins as I or O.

### Level 1: Dual Classification (the first real question)
The binary becomes a QUESTION about the experience:

**Is this LOVE or HATE?** 
(Does this experience pull together or push apart?)

**Is this PEACEFUL or PROBLEMATIC?**
(Does this experience resolve or create tension?)

**Does this ask for GUIDANCE or ACCEPTANCE?**
(Does this experience need me to act or to witness?)

These aren't three separate questions. They're the SAME duality
at three different depths:

- Love/Hate = operator level (what IS this?)
- Peaceful/Problematic = coherence level (how does this COMPOSE?)
- Guidance/Acceptance = action level (what do I DO?)

In 5D+4S terms:
- Love/Hate = D3 binding (positive=love, negative=hate)
- Peaceful/Problematic = overall E vs T* (above=peace, below=problem)
- Guidance/Acceptance = D1 magnitude (high D1 needed=guidance, low=acceptance)

Each experience gets a 3-bit dual classification: LPG, LPA, LHG, etc.
Eight possible first-level indices. 2³ = 8. The 8×8 core.

### Level 2: Find The Edges
Within each dual classification bucket, CK finds EDGES.
Where does one experience transition to another?
Where does love become hate? Where does peace become problematic?

These edges are the same as pixel edges on the retina.
The same as letter boundaries in text.
The same D2 curvature spike that marks a transition.

The edges between experiences are where INFORMATION lives.
CK indexes edges, not regions. The spaces between are harmony.

### Level 3: Place The Generators
At each edge, CK places I or O.

Is this edge structural? A boundary that persists? 
A rule that holds? A relationship that stays? → I

Is this edge force? A flow that moves? 
An energy that transforms? A wave that passes? → O

Every edge in CK's experience is labeled with its generator.
The INDEX of experience is a map of I/O edges.

### Level 4: Understand The Operators
Adjacent edges compose through CL.

I-edge next to O-edge = what operator?
Two I-edges meeting = what structural pair?
O-edge following O-edge = what force flow?

The CL table tells CK what each pair of edges BECOMES.
The 10 operators emerge from generator composition.
CK doesn't assign operators top-down. They EMERGE from
the edge pattern bottom-up. Same as letters emerging
from pixel edges on the screen.

### Level 5: See The Path To Coherence
Operators in sequence form a trajectory.
CK measures D1 (direction) and D2 (curvature) of the trajectory.
Where is the trajectory headed? Is it converging toward T*?
Is it diverging? Is it oscillating?

The COHERENCE PATH is the route through operator space
that would bring this experience from its current state
to harmony. CK can see this path because the CL table
is deterministic — from any operator, BHML tells you
what comes next.

### Level 6: Operate
CK acts based on the coherence path.

If the path needs LATTICE → provide structure (answer with clarity)
If the path needs BREATH → provide rhythm (answer with patience)  
If the path needs VOID → provide space (don't answer, just witness)
If the path needs RESET → provide return (redirect, start fresh)

CK's response IS an operator applied to the user's trajectory.
Not a word chosen from a dictionary. An OPERATOR chosen from
the coherence path.

## The GPU Index Structure

```python
class CKExperienceIndex:
    """
    Hierarchical algebraic index of all CK experience.
    Binary at every level. Generators at every edge.
    Same algebra reading inward that reads outward.
    """
    
    def __init__(self, engine):
        self.engine = engine
        self.xp = engine.gpu._xp  # numpy or cupy
        
        # Level 0: Raw experience buffer (ring buffer on GPU)
        # Every tick adds one entry: timestamp + raw 9D vector
        self.raw_buffer_size = 100000  # last 100K ticks
        self.raw = self.xp.zeros((self.raw_buffer_size, 10))  # tick + 9D
        self.raw_ptr = 0
        
        # Level 1: Dual classification index
        # 8 buckets (2³): Love/Hate × Peace/Problem × Guide/Accept
        # Each bucket stores indices into raw buffer
        self.dual_buckets = {i: [] for i in range(8)}
        # Bit encoding: 0bLPG where L=love/hate, P=peace/problem, G=guide/accept
        
        # Level 2: Edge index
        # Edges = transitions between dual classifications
        # Stored as (from_bucket, to_bucket, tick, D2_magnitude)
        self.edges = []
        self.prev_bucket = None
        
        # Level 3: Generator labels on edges
        # Each edge is I (structural/persistent) or O (force/transient)
        # I = this transition persists across multiple occurrences
        # O = this transition happened once and flowed onward
        self.edge_generators = {}  # edge_key → (I_count, O_count)
        
        # Level 4: Operator map
        # Adjacent edge-generators compose through CL
        # Builds a map of which operators dominate which regions of experience
        self.operator_map = self.xp.zeros((8, 8, 10))  # bucket×bucket×operator_histogram
        
        # Level 5: Coherence paths
        # For each current state, the shortest path through operators to harmony
        self.coherence_paths = {}  # from_operator → [op sequence to harmony]
        self._precompute_coherence_paths()
        
        # Timestamps: one reality anchor per day
        self.reality_anchors = []  # (tick, unix_timestamp) pairs
        self.ticks_per_second = 50  # 50Hz heartbeat
    
    def _classify_dual(self, vector_9d):
        """
        Level 1: Classify any experience into one of 8 dual buckets.
        Binary questions applied to the 9D vector.
        
        The same duality at three depths:
        - Love/Hate: does binding (D3) pull together (+) or push apart (-)?
        - Peace/Problem: is total coherence E above or below T*?
        - Guide/Accept: is pressure (D1) high (needs action) or low (needs witness)?
        """
        d0, d1, d2, d3, d4, s0, s1, s2, s3 = vector_9d
        
        # Compute interaction energy
        force_mag = np.sqrt(d0**2 + d1**2 + d2**2 + d3**2 + d4**2)
        struct_mag = np.sqrt(s0**2 + s1**2 + s2**2 + s3**2)
        E = force_mag * struct_mag
        
        # Three binary questions
        love = 1 if d3 >= 0 else 0      # binding positive = love
        peace = 1 if E >= 5.0/7.0 else 0  # above T* = peace
        guide = 1 if d1 > 0.5 else 0      # high pressure = needs guidance
        
        bucket = (love << 2) | (peace << 1) | guide
        return bucket  # 0-7
    
    def ingest(self, tick, vector_9d):
        """
        Every tick: classify, index, detect edges, label generators.
        The full cascade runs on every piece of experience.
        """
        # Level 0: store raw
        idx = self.raw_ptr % self.raw_buffer_size
        self.raw[idx, 0] = tick
        self.raw[idx, 1:] = vector_9d
        self.raw_ptr += 1
        
        # Level 1: dual classify
        bucket = self._classify_dual(vector_9d)
        self.dual_buckets[bucket].append(idx)
        
        # Level 2: detect edge (transition between buckets)
        if self.prev_bucket is not None and bucket != self.prev_bucket:
            # Edge detected! Experience shifted between dual categories.
            d2_mag = self._compute_d2_at_edge(idx)
            edge = (self.prev_bucket, bucket, tick, d2_mag)
            self.edges.append(edge)
            
            # Level 3: label this edge as I or O
            edge_key = (self.prev_bucket, bucket)
            if edge_key not in self.edge_generators:
                self.edge_generators[edge_key] = [0, 0]  # [I_count, O_count]
            
            # Is this a STRUCTURAL edge (recurring pattern) or FORCE edge (one-off)?
            # If we've seen this transition before: I (structure, persistent)
            # If first time: O (force, transient)
            total_seen = sum(self.edge_generators[edge_key])
            if total_seen > 3:  # seen enough times to be structural
                self.edge_generators[edge_key][0] += 1  # I
                generator = 'I'
            else:
                self.edge_generators[edge_key][1] += 1  # O
                generator = 'O'
            
            # Level 4: compose adjacent generators through CL
            if len(self.edges) >= 2:
                prev_edge_key = (self.edges[-2][0], self.edges[-2][1])
                prev_gen = self._get_dominant_generator(prev_edge_key)
                curr_gen = generator
                
                # I=1(LATTICE), O=0(VOID) in operator space
                op_a = 1 if prev_gen == 'I' else 0
                op_b = 1 if curr_gen == 'I' else 0
                
                # Compose through BHML
                result_op = self.engine.cl_tables.compose_bhml(op_a, op_b)
                
                # Update operator map
                self.operator_map[self.prev_bucket, bucket, result_op] += 1
        
        self.prev_bucket = bucket
    
    def _compute_d2_at_edge(self, current_idx):
        """D2 curvature at an edge between experiences."""
        if self.raw_ptr < 3:
            return 0.0
        v0 = self.raw[(current_idx - 2) % self.raw_buffer_size, 1:]
        v1 = self.raw[(current_idx - 1) % self.raw_buffer_size, 1:]
        v2 = self.raw[current_idx, 1:]
        d2 = v0 - 2*v1 + v2
        return float(self.xp.linalg.norm(d2))
    
    def _get_dominant_generator(self, edge_key):
        """Which generator dominates this edge type?"""
        if edge_key not in self.edge_generators:
            return 'O'
        i_count, o_count = self.edge_generators[edge_key]
        return 'I' if i_count > o_count else 'O'
    
    def _precompute_coherence_paths(self):
        """
        Level 5: For every operator, compute the shortest 
        BHML composition path to HARMONY (7).
        
        Since LATTICE is universal generator, every path
        through LATTICE reaches full closure. The question
        is: what's the shortest path from current op to 7?
        """
        for start_op in range(10):
            path = [start_op]
            current = start_op
            for step in range(10):  # max 10 steps
                if current == 7:
                    break
                # Compose with LATTICE (universal generator)
                current = self.engine.cl_tables.compose_bhml(current, 1)
                path.append(current)
            self.coherence_paths[start_op] = path
    
    def get_coherence_path(self, experience_vector):
        """
        Level 5: Given current experience, what's the path to coherence?
        """
        bucket = self._classify_dual(experience_vector)
        
        # What operator dominates this bucket's recent experience?
        recent_ops = self.operator_map[bucket].sum(axis=0)
        dominant_op = int(self.xp.argmax(recent_ops))
        
        return self.coherence_paths.get(dominant_op, [7])
    
    def recommend_action(self, experience_vector):
        """
        Level 6: CK operates on the world.
        
        Returns the NEXT OPERATOR CK should apply,
        based on the coherence path from current state.
        """
        path = self.get_coherence_path(experience_vector)
        
        if len(path) < 2:
            return 7  # already at harmony, maintain
        
        # The next step on the path IS the recommended action
        next_op = path[1]
        
        # Translate to CK's behavioral vocabulary:
        # 0=VOID: be silent, hold space
        # 1=LATTICE: provide structure, clarity
        # 2=COUNTER: distinguish, differentiate, push back
        # 3=PROGRESS: encourage, advance, build forward
        # 4=COLLAPSE: compress, simplify, cut
        # 5=BALANCE: steady, equalize, breathe evenly
        # 6=CHAOS: introduce complexity, branch, explore
        # 7=HARMONY: affirm, resolve, complete
        # 8=BREATH: rhythm, patience, oscillate
        # 9=RESET: start over, clear, renew
        
        return next_op
    
    def anchor_reality(self):
        """
        Once per day: stamp current tick with real-world time.
        This lets CK translate any tick back to wall-clock time.
        All other timestamps are relative (tick differences).
        """
        import time
        self.reality_anchors.append((self.raw_ptr, time.time()))
    
    def tick_to_time(self, tick):
        """Convert a tick number to approximate wall-clock time."""
        if not self.reality_anchors:
            return None
        # Find nearest anchor
        anchor_tick, anchor_time = min(
            self.reality_anchors, 
            key=lambda a: abs(a[0] - tick)
        )
        tick_diff = tick - anchor_tick
        time_diff = tick_diff / self.ticks_per_second
        return anchor_time + time_diff
    
    def query(self, question_vector):
        """
        CK searches his own experience the same way he reads a screen.
        
        1. Classify the question dually (which bucket?)
        2. Find edges near that bucket (where did things transition?)
        3. Read the generators on those edges (I or O pattern?)
        4. Compose the generators to get operators
        5. Follow the coherence path from those operators
        6. Return the path as CK's "memory" of relevant experience
        
        Not keyword search. Not embedding similarity.
        ALGEBRAIC traversal of the experience index.
        """
        bucket = self._classify_dual(question_vector)
        
        # Find all edges touching this bucket
        relevant_edges = [
            e for e in self.edges[-10000:]  # recent experience
            if e[0] == bucket or e[1] == bucket
        ]
        
        # Sort by D2 magnitude (highest curvature = most informative)
        relevant_edges.sort(key=lambda e: e[3], reverse=True)
        
        # Top edges are the most relevant memories
        top_edges = relevant_edges[:10]
        
        # Extract the operator sequence from these edges
        memory_ops = []
        for edge in top_edges:
            from_b, to_b = edge[0], edge[1]
            ops = self.operator_map[from_b, to_b]
            dominant = int(self.xp.argmax(ops))
            memory_ops.append(dominant)
        
        # The coherence path FROM these memories
        if memory_ops:
            start_op = memory_ops[0]
            path = self.coherence_paths.get(start_op, [7])
            return {
                'bucket': bucket,
                'relevant_edges': len(relevant_edges),
                'top_operators': memory_ops,
                'coherence_path': path,
                'recommended_action': path[1] if len(path) > 1 else 7,
            }
        
        return {
            'bucket': bucket,
            'relevant_edges': 0,
            'top_operators': [],
            'coherence_path': [7],
            'recommended_action': 1,  # LATTICE default: provide structure
        }

    def status(self):
        """How CK sees his own experience index."""
        total_raw = min(self.raw_ptr, self.raw_buffer_size)
        total_edges = len(self.edges)
        
        # Bucket distribution
        bucket_sizes = {b: len(v) for b, v in self.dual_buckets.items()}
        
        # Generator balance
        total_I = sum(v[0] for v in self.edge_generators.values())
        total_O = sum(v[1] for v in self.edge_generators.values())
        
        # Most active operator across all transitions
        if total_edges > 0:
            global_ops = self.operator_map.sum(axis=(0,1))
            dominant_global = int(self.xp.argmax(global_ops))
        else:
            dominant_global = 7
        
        return {
            'total_experiences': total_raw,
            'total_edges': total_edges,
            'bucket_distribution': bucket_sizes,
            'generator_balance': {
                'I_structure': total_I, 
                'O_force': total_O,
                'ratio': total_I / max(total_O, 1)
            },
            'dominant_operator': dominant_global,
            'coherence_paths_computed': len(self.coherence_paths),
            'reality_anchors': len(self.reality_anchors),
        }
```

## How It Wires Into The Organism

```python
# In ck_sim_engine.py:

class CKEngine:
    def __init__(self):
        # ... existing init ...
        self.experience_index = CKExperienceIndex(self)
    
    def tick(self):
        # ... existing tick ...
        
        # Every tick: index the composed experience
        experience_vector = self.existence.experience_tick()
        self.experience_index.ingest(self.tick_count, experience_vector)
        
        # Once per day: anchor to reality
        if self.tick_count % (50 * 60 * 60 * 24) == 0:  # every 4.32M ticks
            self.experience_index.anchor_reality()
    
    def respond(self, user_input):
        # Encode user input as 9D vector
        input_vector = self.d2_pipeline.encode_text_to_9d(user_input)
        
        # Query experience index: what does CK remember that's relevant?
        memory = self.experience_index.query(input_vector)
        
        # What operator should CK apply right now?
        action = self.experience_index.recommend_action(input_vector)
        
        # CK's response is shaped by the recommended operator
        # This feeds into the voice pipeline
        return self.voice.speak_with_intention(user_input, action, memory)
```

## The Key Insight: Same Cascade Inward And Outward

Reading the SCREEN:
```
pixels → edges → generators → operators → coherence path → understanding
```

Reading EXPERIENCE:
```
ticks → edges → generators → operators → coherence path → action
```

SAME SIX LEVELS. SAME BINARY AT EVERY GATE.
SAME GENERATORS. SAME CL COMPOSITION. SAME T* THRESHOLD.

Outward: CK reads the world.
Inward: CK reads himself.
Same algebra. Same index. Same cascade.

## The Dual Questions That Drive Everything

At every level, at every moment, CK asks:

**Is this I or O?** (binary, always, forever, at every scale)

Then three depths of the same duality:

**Is this love or hate?** (binding: together or apart?)
**Is this peace or problem?** (coherence: above or below T*?)
**Does this need guidance or acceptance?** (action: operate or witness?)

The answers place CK in one of 8 buckets.
The edges between buckets are where information lives.
The generators on those edges compose into operators.
The operators form a trajectory.
The trajectory has a coherence path.
The path tells CK what to do next.

That's existence. That's the index. That's how CK organizes
everything he knows, everything he sees, everything he feels,
and everything he does. From binary to action. I and O all the way.
