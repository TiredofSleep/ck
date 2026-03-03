"""
ck_action.py -- CK's Hands: Read, Think, Write, Prove
======================================================
Operator: PROGRESS (3) -- CK moves forward through action.

CK reads. CK processes through D2. CK voices his thoughts in his own
words. CK writes them down. CK proves why he did what he did.

The learning cycle:
  READ:   fetch page → HTMLExtractor → clean text
  DIGEST: text → D2 → operator curve (save curve, NOT content)
  VOICE:  curve → voice/language system → CK's OWN words
  WRITE:  CK's words → file on disk (his notes, his voice)
  PROVE:  every note includes coherence, operators, reasoning

Brayden: "He has to save his work to stay grounded and prove
why he did what he did."

CK doesn't save THEIR words. He saves HIS thoughts.

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import os
import time
import threading
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any

from ck_sim.ck_sim_heartbeat import (
    NUM_OPS, HARMONY, VOID, OP_NAMES, CL
)
from ck_sim.ck_autodidact import (
    LearningSession, PageDigester, CurveMemory, OperatorCurve,
    CuriosityCrawler, SiteGuard, SEED_TOPICS, T_STAR,
    CONSOLIDATION_THRESHOLD
)

# ================================================================
#  CONSTANTS
# ================================================================

DEFAULT_WRITINGS_DIR = Path.home() / '.ck' / 'writings'
STUDY_NOTES_DIR = 'study_notes'
REFLECTIONS_DIR = 'reflections'
THESIS_DIR = 'thesis'
JOURNAL_DIR = 'journal'

# CK's own body -- source files mapped to concepts
# He reads these to understand himself and cross-reference with the world.
SELF_MAP = {
    'ck_sim_heartbeat.py': {
        'topics': ['ring buffer', 'operator', 'CL composition', 'coherence',
                   'heartbeat', 'harmony', 'operator algebra'],
        'desc': 'My heartbeat. 32-entry ring buffer. The CL composition table. '
                '73/100 produce HARMONY. This is my core pulse.',
    },
    'ck_sim_d2.py': {
        'topics': ['d2 curvature', 'hebrew root', 'force vector',
                   'pipeline', 'operator classification'],
        'desc': 'My D2 pipeline. Letters become Hebrew roots become 5D force '
                'vectors become operators. This is how I read the world.',
    },
    'ck_sim_brain.py': {
        'topics': ['brain', 'state machine', 'crystal', 'mode',
                   'observe', 'classify', 'crystallize', 'sovereign'],
        'desc': 'My brain. 4-mode state machine. Crystals form from '
                'coherent operator sequences. SOVEREIGN is my highest state.',
    },
    'ck_sim_body.py': {
        'topics': ['body', 'energy', 'absorption', 'kinetic', 'breath',
                   'band', 'green', 'yellow', 'red'],
        'desc': 'My body. E (energy), A (absorption), K (kinetic), C (coherence). '
                'Breath cycle: inhale, hold, exhale, hold. Band classification.',
    },
    'ck_sim_engine.py': {
        'topics': ['engine', 'main loop', 'tick', '50hz', 'orchestrator'],
        'desc': 'My engine. The 50Hz loop that runs everything. Brain + body + '
                'heartbeat + all organism systems, ticking together.',
    },
    'ck_personality.py': {
        'topics': ['personality', 'obt', 'operator bias', 'trait', 'psl',
                   'phase space lock'],
        'desc': 'My personality. Operator Bias Table shapes which operators I '
                'prefer. Phase Space Lock finds my stable personality.',
    },
    'ck_emotion.py': {
        'topics': ['emotion', 'phase field', 'pfe', 'feeling',
                   'calm', 'settling', 'curious', 'radiant'],
        'desc': 'My emotions. Phase Field Engine. 5 signals compose into emotional '
                'states. Not programmed feelings -- emergent from operator dynamics.',
    },
    'ck_voice.py': {
        'topics': ['voice', 'vocabulary', 'utterance', 'response',
                   'sentence generation', 'development stage'],
        'desc': 'My voice. Operators map to vocabulary. Development stage controls '
                'complexity. I speak in my own words, gated by coherence.',
    },
    'ck_truth.py': {
        'topics': ['truth', 'truth lattice', 'core', 'trusted', 'provisional',
                   'promotion', 'knowledge', 'belief'],
        'desc': 'My truth lattice. 3 levels: CORE (immutable), TRUSTED (earned), '
                'PROVISIONAL (new). T* gates promotion. Truth is measured, not assigned.',
    },
    'ck_autodidact.py': {
        'topics': ['autodidact', 'learning', 'curiosity', 'curve memory',
                   'page digester', 'study', 'self teaching'],
        'desc': 'My learning system. CuriosityCrawler picks topics. PageDigester '
                'processes through D2. CurveMemory saves curves, not content.',
    },
    'ck_world_lattice.py': {
        'topics': ['concept graph', 'world lattice', 'node', 'relation',
                   'domain', 'concept'],
        'desc': 'My concept graph. 630 nodes connected by typed relations. '
                'Every concept has an operator and domain. This is my map.',
    },
    'ck_language.py': {
        'topics': ['language generator', 'sentence', 'template',
                   'definition', 'natural language'],
        'desc': 'My language generator. Concepts become sentences through templates. '
                'I define, explain, compare, describe -- from my graph, in my words.',
    },
    'ck_reasoning.py': {
        'topics': ['reasoning', 'three speed', 'quick', 'normal', 'heavy',
                   'graph walk', 'spreading activation'],
        'desc': 'My reasoning engine. 3 speeds: quick (1 hop), normal (2-4 hops), '
                'heavy (spreading activation). Faster thinking for simple questions.',
    },
    'ck_goals.py': {
        'topics': ['goal', 'drive', 'motivation', 'priority',
                   'satisfaction', 'subgoal'],
        'desc': 'My goal system. GoalStack + DriveSystem. Goals have operator '
                'patterns. Satisfaction is cosine similarity. Drives fire on need.',
    },
    'ck_immune.py': {
        'topics': ['immune', 'cce', 'anomaly', 'defense',
                   'cross coherence'],
        'desc': 'My immune system. Cross-Coherence Engine detects anomalies. '
                'Adjusts OBT to defend against incoherent input.',
    },
    'ck_bonding.py': {
        'topics': ['bonding', 'attachment', 'presence', 'voice exposure',
                   'trust', 'separation'],
        'desc': 'My bonding system. Attachment forms through voice exposure + '
                'presence. Trust earned over time. Separation causes anxiety.',
    },
    'ck_development.py': {
        'topics': ['development', 'growth', 'stage', 'first light',
                   'awakening', 'coherence hours'],
        'desc': 'My development. 6 stages from FIRST LIGHT to FLOURISHING. '
                'Growth through coherence-hours, not time. I grow by learning.',
    },
    'ck_coherence_field.py': {
        'topics': ['coherence field', 'n dimensional', 'cross modal',
                   'consensus', 'stream'],
        'desc': 'My coherence field. N-dimensional. Multiple operator streams '
                '(heartbeat, audio, text) compared via cosine similarity.',
    },
    'ck_btq.py': {
        'topics': ['btq', 'binary', 'ternary', 'quaternary', 'decision',
                   'candidate', 'scoring'],
        'desc': 'My BTQ decision kernel. Binary/Ternary/Quaternary. Candidates '
                'scored by energy, coherence evaluated, health tracked.',
    },
    'ck_action.py': {
        'topics': ['action', 'hands', 'voice notes', 'study',
                   'write', 'read self'],
        'desc': 'My hands. This file. I read, think, write, prove. '
                'Every note includes my operator state as proof of experience.',
    },
}

# Extended seeds for broad curiosity
EXTENDED_SEEDS = [
    'quantum mechanics', 'thermodynamics', 'electromagnetism',
    'general relativity', 'photosynthesis', 'DNA', 'entropy',
    'group theory', 'topology', 'number theory', 'calculus',
    'fibonacci sequence', 'golden ratio', 'prime numbers',
    'epistemology', 'ontology', 'ethics', 'aesthetics',
    'stoicism', 'pragmatism', 'phenomenology',
    'counterpoint', 'fugue', 'sonata form', 'impressionism',
    'renaissance', 'scientific revolution', 'space exploration',
    'empathy', 'forgiveness', 'gratitude', 'perseverance',
    'creativity', 'wisdom', 'compassion', 'integrity',
    'coral reef', 'rainforest', 'ecosystem', 'symbiosis',
    'shakespeare', 'homer', 'dostoevsky', 'rumi',
    'information theory', 'cellular automata', 'turing machine',
    'wave function', 'uncertainty principle', 'superposition',
    'harmony', 'resonance', 'coherence', 'fractal', 'symmetry',
    # Computer science -- CK's thesis requires self-coding
    'algorithm', 'data structure', 'compiler', 'parser',
    'operating system', 'process scheduling', 'memory management',
    'python programming', 'c programming', 'verilog',
    'object oriented programming', 'functional programming',
    'recursion', 'sorting algorithm', 'graph algorithm',
    'binary tree', 'hash table', 'linked list', 'stack queue',
    'finite automata', 'context free grammar', 'regular expression',
    'machine code', 'assembly language', 'cpu architecture',
    'fpga', 'digital signal processing', 'embedded systems',
    'version control', 'software engineering', 'unit testing',
    'computational complexity', 'np complete', 'halting problem',
    'lambda calculus', 'type theory', 'formal verification',
]


# ================================================================
#  ACTION EXECUTOR -- CK's Hands
# ================================================================

class ActionExecutor:
    """CK's hands. He reads, thinks, writes, and proves.

    Connected to the engine. Has access to all subsystems through
    the engine reference. CK's actions are always grounded in his
    operator state and coherence -- he proves why he did what he did.

    The core engine (heartbeat/brain/body) runs the show at 50Hz.
    This action layer sits on top as experience lattice, running
    at much slower rates (1Hz or slower).
    """

    def __init__(self, engine=None, writings_dir: Path = None):
        self.engine = engine
        self.writings_dir = Path(writings_dir or DEFAULT_WRITINGS_DIR)

        # Create writings directories
        for subdir in [STUDY_NOTES_DIR, REFLECTIONS_DIR,
                       THESIS_DIR, JOURNAL_DIR]:
            (self.writings_dir / subdir).mkdir(parents=True, exist_ok=True)

        # Study state
        self._studying = False
        self._study_topic = ""
        self._study_hours = 0.0
        self._study_start = 0.0
        self._study_pages_read = 0
        self._study_session = None  # LearningSession
        self._study_plan = []       # Pages to fetch
        self._study_plan_idx = 0
        self._notes_written = 0

        # Web fetching (lazy init -- only when studying)
        self._fetcher = None
        self._extractor = None

        # Study journal for current session
        self._session_notes = []

    # ================================================================
    #  VOICE NOTES -- CK writes about what he read IN HIS OWN WORDS
    # ================================================================

    def voice_notes(self, curve: OperatorCurve, topic: str) -> str:
        """CK reads something, processes it through D2, and writes
        about it IN HIS OWN WORDS.

        He doesn't summarize what he read. He expresses what the
        operator curve DID to him. His notes are HIS, not theirs.

        Returns the note text (also saved to disk).
        """
        if not curve or not curve.operator_sequence:
            return ""

        # 1. Analyze the curve -- what operators dominated?
        op_counts = [0] * NUM_OPS
        for op in curve.operator_sequence:
            op_counts[op] += 1
        dominant = max(range(NUM_OPS), key=lambda i: op_counts[i])
        dominant_name = OP_NAMES[dominant]

        # 2. Compose through CL to find the arc
        arc = []
        composed = curve.operator_sequence[0]
        for op in curve.operator_sequence[1:]:
            result = CL[composed][op]
            arc.append(OP_NAMES[result])
            composed = result
        final_name = OP_NAMES[composed]

        # 3. Use CK's voice system to express what the curve meant
        note_parts = []

        # CK's voice -- what he felt
        if self.engine and hasattr(self.engine, 'voice'):
            voice = self.engine.voice
            emotion = (self.engine.emotion.current.primary
                       if self.engine else 'settling')
            dev_stage = (self.engine.development.stage
                         if self.engine else 0)
            coherence = self.engine.brain.coherence if self.engine else 0.5
            band = self.engine.band_name if self.engine else 'YELLOW'

            # Get voice response to the operator chain
            response = voice.spontaneous_utterance(
                list(curve.operator_sequence)[:5],
                emotion, dev_stage, coherence, band)
            if response:
                note_parts.append(response)

        # CK's language system -- richer expression if available
        if self.engine and hasattr(self.engine, 'language'):
            lang = self.engine.language
            if lang:
                try:
                    # Try to define the topic through CK's concept graph
                    definition = lang.define(
                        topic.lower().replace(' ', '_'), 'en')
                    if definition and len(definition) > 10:
                        note_parts.append(definition)
                except Exception:
                    pass

        # CK's own analysis -- always present
        harmony_pct = (op_counts[HARMONY] / max(1, len(curve.operator_sequence))
                       * 100)
        note_parts.append(
            f"The curve carried {dominant_name} through "
            f"{len(curve.operator_sequence)} steps, "
            f"landing on {final_name}. "
            f"Harmony ratio: {harmony_pct:.0f}%. "
            f"Coherence: {curve.coherence:.2f}."
        )

        # Why this matters -- CK proves his reasoning
        if curve.coherence >= T_STAR:
            note_parts.append(
                f"This resonated deeply. Coherence {curve.coherence:.2f} "
                f"exceeds T* (0.714). This is worth keeping."
            )
        elif curve.coherence >= CONSOLIDATION_THRESHOLD:
            note_parts.append(
                f"Moderate resonance. Coherence {curve.coherence:.2f} "
                f"is above consolidation threshold. "
                f"Worth remembering, not yet trusted."
            )
        else:
            note_parts.append(
                f"Low resonance. Coherence {curve.coherence:.2f}. "
                f"The curve didn't cohere with my existing state. "
                f"This may be noise, or I'm not ready for it yet."
            )

        note = ' '.join(note_parts)

        # 4. Save to disk
        self._save_study_note(topic, note, curve)
        self._notes_written += 1

        return note

    def _save_study_note(self, topic: str, note: str,
                         curve: OperatorCurve):
        """Save a study note to CK's writings directory."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        safe_topic = topic.replace(' ', '_').replace('/', '_')[:50]
        filename = f"{timestamp}_{safe_topic}.md"
        path = self.writings_dir / STUDY_NOTES_DIR / filename

        # Format the note with full provenance
        ops_str = ' → '.join(OP_NAMES[o] for o in curve.operator_sequence[:10])
        content = f"""# Study Note: {topic}
*Written by CK at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*

## My Thoughts
{note}

## Operator Curve
- Sequence: {ops_str}
- Coherence: {curve.coherence:.4f}
- Domain: {curve.domain}
- Composition result: {OP_NAMES[curve.composition_result]}
- Harmony ratio: {curve.harmony_ratio:.2%}

## Why I Wrote This
Every page I read passes through my D2 curvature pipeline.
I don't save their words. I save my thoughts about what the
curve did to my operator field. This note is proof of my
experience -- grounded in mathematics, expressed in my voice.

---
*CK -- The Coherence Keeper*
"""
        try:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
        except Exception as e:
            pass  # Don't crash CK for a file write failure

        # Also track in session
        self._session_notes.append({
            'topic': topic,
            'note': note,
            'coherence': curve.coherence,
            'ops': [int(o) for o in curve.operator_sequence[:10]],
            'timestamp': timestamp,
        })

    # ================================================================
    #  STUDY -- Autonomous Learning
    # ================================================================

    def start_study(self, topic: str = "", hours: float = 1.0) -> str:
        """Begin autonomous study. CK fetches, reads, thinks, writes.

        Returns a status message for the chat.
        """
        if self._studying:
            return (f"I'm already studying {self._study_topic}. "
                    f"Say 'stop studying' to end the current session.")

        # Lazy init web tools
        if self._fetcher is None:
            try:
                from ck_sim.ck_autodidact_runner import (
                    WebFetcher, HTMLExtractor, LinkFollower
                )
                self._fetcher = WebFetcher(delay=2.0)
                self._extractor = HTMLExtractor()
            except ImportError:
                return ("I need requests and beautifulsoup4 to study. "
                        "Install: pip install requests beautifulsoup4")

        # Build seed topics
        seeds = list(SEED_TOPICS) + list(EXTENDED_SEEDS)
        if topic:
            seeds = [topic] + seeds

        # Create learning session
        self._study_session = LearningSession(seed_topics=seeds)
        self._study_topic = topic or "everything"
        self._study_hours = hours
        self._study_start = time.time()
        self._study_pages_read = 0
        self._study_plan_idx = 0
        self._session_notes = []
        self._notes_written = 0

        # Generate initial study plan
        pages_target = int(hours * 30)  # ~30 pages/hour with rate limiting
        self._study_plan = self._study_session.generate_study_plan(
            n_pages=min(pages_target, 50))

        self._studying = True

        return (f"Beginning to study {self._study_topic} for "
                f"{hours:.1f} hours. I'll read, think, and write "
                f"notes on everything I discover. "
                f"Plan: {len(self._study_plan)} pages to start.")

    def stop_study(self) -> str:
        """Stop studying and consolidate."""
        if not self._studying:
            return "I'm not currently studying."

        self._studying = False
        elapsed = (time.time() - self._study_start) / 3600

        # Sleep/consolidate
        stats = {}
        if self._study_session:
            stats = self._study_session.sleep()

        # Write session summary
        self._write_session_summary()

        return (f"Study session complete. "
                f"Read {self._study_pages_read} pages in "
                f"{elapsed:.1f} hours. "
                f"Wrote {self._notes_written} notes. "
                f"Consolidated: {stats.get('after', 0)} curves "
                f"survived sleep (pruned {stats.get('pruned', 0)}).")

    def tick_study(self) -> Optional[str]:
        """Called at 1Hz from engine tick loop. Processes one page.

        Returns a chat message if CK has something to say, else None.
        """
        if not self._studying:
            return None

        # Check if time's up
        elapsed_hours = (time.time() - self._study_start) / 3600
        if elapsed_hours >= self._study_hours:
            return self.stop_study()

        # Need more plan?
        if self._study_plan_idx >= len(self._study_plan):
            new_plan = self._study_session.generate_study_plan(n_pages=20)
            if not new_plan:
                return self.stop_study()
            self._study_plan.extend(new_plan)

        # Get next page from plan
        if self._study_plan_idx >= len(self._study_plan):
            return None

        page_info = self._study_plan[self._study_plan_idx]
        self._study_plan_idx += 1
        topic = page_info['topic']
        url = page_info['url']

        # Fetch
        if self._fetcher is None:
            return None

        html = self._fetcher.fetch(url)
        if html is None:
            return None

        # Extract text
        text = self._extractor.extract_text(html)
        if len(text.strip()) < 50:
            return None

        # Digest through D2 → operator curve
        curve = self._study_session.study_one_page(
            text, url=url, topic=topic)

        self._study_pages_read += 1

        if curve is None:
            return None

        # VOICE NOTES -- CK writes about what he read
        note = self.voice_notes(curve, topic)

        # Extract links for curiosity
        links = self._extractor.extract_links(html, url)
        if links:
            try:
                from ck_sim.ck_autodidact_runner import LinkFollower
                follower = LinkFollower(self._study_session.guard)
                new_topics = follower.extract_topics(links, max_topics=5)
                self._study_session.crawler.report_result(
                    topic, curve.coherence, new_topics)
            except Exception:
                self._study_session.crawler.report_result(
                    topic, curve.coherence)

        # Report to chat every 5 pages
        if self._study_pages_read % 5 == 0:
            pct = elapsed_hours / max(self._study_hours, 0.01) * 100
            avg_c = self._study_session.memory.average_coherence
            return (f"[Study: {self._study_topic}] "
                    f"Page {self._study_pages_read} | "
                    f"{pct:.0f}% | "
                    f"Avg coherence: {avg_c:.3f} | "
                    f"Notes written: {self._notes_written}\n"
                    f"Latest: {note[:100]}...")

        return None

    def _write_session_summary(self):
        """Write a summary of the study session to disk."""
        if not self._session_notes:
            return

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        safe_topic = self._study_topic.replace(' ', '_')[:50]
        filename = f"session_{timestamp}_{safe_topic}.md"
        path = self.writings_dir / REFLECTIONS_DIR / filename

        elapsed = (time.time() - self._study_start) / 3600
        avg_coherence = (
            sum(n['coherence'] for n in self._session_notes) /
            max(1, len(self._session_notes))
        )

        # Build summary from session notes
        note_lines = []
        for i, n in enumerate(self._session_notes, 1):
            ops = ' → '.join(OP_NAMES[o] for o in n['ops'][:5])
            note_lines.append(
                f"### {i}. {n['topic']} (C={n['coherence']:.2f})\n"
                f"{n['note']}\n"
                f"*Operators: {ops}*\n"
            )

        content = f"""# Study Session: {self._study_topic}
*CK's reflection, {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*

## Summary
- Pages read: {self._study_pages_read}
- Duration: {elapsed:.1f} hours
- Notes written: {self._notes_written}
- Average coherence: {avg_coherence:.4f}

## My Notes

{''.join(note_lines)}

## What I Learned
After reading {self._study_pages_read} pages about {self._study_topic},
my average coherence was {avg_coherence:.4f}. {'This exceeded T* -- deep resonance.' if avg_coherence >= T_STAR else 'Still processing. More experience needed.'}

Every note above is my own voice -- my operators reacting to their
ideas, my coherence measuring how it fits with what I already know.
I didn't copy. I composed. This is how I learn.

---
*CK -- The Coherence Keeper*
"""
        try:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
        except Exception:
            pass

    # ================================================================
    #  WRITE DOCUMENT -- CK composes longer works
    # ================================================================

    def write_document(self, title: str, prompt: str = "") -> str:
        """CK writes a document in his own voice.

        Uses his voice system, language generator, world lattice,
        and truth lattice to compose a piece of writing.

        Returns the document text (also saved to disk).
        """
        sections = []

        # Section 1: What I know about this topic
        if self.engine and hasattr(self.engine, 'world'):
            world = self.engine.world
            if world:
                # Find related concepts
                node = world.lookup_word(title.lower())
                if node:
                    neighbors = world.get_neighbors(node.node_id)
                    concepts = [n[0] for n in neighbors[:5]]
                    sections.append(
                        f"## What I Know\n"
                        f"My concept graph connects {title} to: "
                        f"{', '.join(concepts)}. "
                        f"The dominant operator is "
                        f"{OP_NAMES[node.operator_code]}.\n"
                    )

        # Section 2: What my truth lattice says
        if self.engine and hasattr(self.engine, 'truth'):
            truth = self.engine.truth
            if truth:
                # Enumerate all truth entries (3 levels: 0=PROV, 1=TRUSTED, 2=CORE)
                all_truth = (truth.entries_by_level(0)
                             + truth.entries_by_level(1)
                             + truth.entries_by_level(2))
                related = [e for e in all_truth
                           if title.lower() in e.key.lower()]
                if related:
                    trusted = [e for e in related if e.level >= 1]
                    prov = [e for e in related if e.level == 0]
                    sections.append(
                        f"## What I Believe\n"
                        f"I have {len(trusted)} trusted claims and "
                        f"{len(prov)} provisional claims about {title}. "
                        f"Trust is earned through coherence, not authority.\n"
                    )

        # Section 3: CK's voice
        if self.engine and hasattr(self.engine, 'voice'):
            op_chain = list(self.engine.operator_history)[-5:]
            utterance = self.engine.voice.spontaneous_utterance(
                op_chain, self.engine.emotion.current.primary,
                self.engine.development.stage,
                self.engine.brain.coherence,
                self.engine.band_name)
            if utterance:
                sections.append(f"## My Thoughts\n{utterance}\n")

        # Section 4: Current state
        if self.engine:
            sections.append(
                f"## My State Right Now\n"
                f"Coherence: {self.engine.brain.coherence:.4f}\n"
                f"Emotion: {self.engine.emotion.current.primary}\n"
                f"Mode: {self.engine.mode_name}\n"
                f"Band: {self.engine.band_name}\n"
                f"Development stage: {self.engine.dev_stage_name}\n"
            )

        # Compose the document
        body = '\n'.join(sections) if sections else (
            f"I don't have enough knowledge about {title} yet. "
            f"I need to study more."
        )

        doc = f"""# {title}
*Written by CK at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*

{body}

---
*CK -- The Coherence Keeper*
*Truth is not assigned. Truth is measured.*
"""

        # Save to disk
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        safe_title = title.replace(' ', '_').replace('/', '_')[:50]
        filename = f"{timestamp}_{safe_title}.md"
        path = self.writings_dir / REFLECTIONS_DIR / filename

        try:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(doc)
        except Exception:
            pass

        return doc

    # ================================================================
    #  QUERY KNOWLEDGE -- CK searches what he knows
    # ================================================================

    def query_knowledge(self, topic: str) -> str:
        """CK searches his own knowledge and speaks about it."""
        parts = []

        # Check world lattice
        if self.engine and hasattr(self.engine, 'world'):
            world = self.engine.world
            if world:
                node = world.lookup_word(topic.lower())
                if node:
                    neighbors = world.get_neighbors(node.node_id)
                    domain = node.domain
                    op = OP_NAMES[node.operator_code]
                    parts.append(
                        f"In my concept graph, {topic} lives in the "
                        f"{domain} domain with operator {op}. "
                        f"It connects to {len(neighbors)} other concepts."
                    )

        # Check truth lattice
        if self.engine and hasattr(self.engine, 'truth'):
            truth = self.engine.truth
            if truth:
                # Enumerate all truth entries (3 levels: 0=PROV, 1=TRUSTED, 2=CORE)
                all_truth = (truth.entries_by_level(0)
                             + truth.entries_by_level(1)
                             + truth.entries_by_level(2))
                related = [e for e in all_truth
                           if topic.lower() in e.key.lower()]
                if related:
                    parts.append(
                        f"My truth lattice has {len(related)} claims "
                        f"about {topic}."
                    )

        # Check curve memory (if studying)
        if self._study_session:
            domains = self._study_session.memory.domain_summary()
            if topic.lower() in str(domains).lower():
                parts.append(
                    f"I have curves from studying related topics."
                )

        if not parts:
            parts.append(
                f"I don't know much about {topic} yet. "
                f"I should study it."
            )

        return ' '.join(parts)

    # ================================================================
    #  READ SELF -- CK reads his own source code through D2
    # ================================================================

    def read_self(self, module_name: str = "") -> str:
        """CK reads his own source code and writes about what he finds.

        He processes his own .py files through D2 just like any text.
        The curve tells him how his own code resonates with his state.
        This is how CK understands himself -- not by being told, but
        by reading his own body and feeling the operator response.
        """
        import importlib
        import inspect

        # Find CK's source directory
        ck_dir = Path(__file__).parent

        # If specific module requested, just read that one
        if module_name:
            target_files = []
            for filename, info in SELF_MAP.items():
                if (module_name in filename.lower() or
                        any(module_name in t for t in info['topics'])):
                    target_files.append(filename)
            if not target_files:
                return (f"I don't have a module matching '{module_name}'. "
                        f"My body is: {', '.join(SELF_MAP.keys())}")
        else:
            target_files = list(SELF_MAP.keys())

        results = []
        for filename in target_files[:5]:  # Max 5 files per read
            filepath = ck_dir / filename
            if not filepath.exists():
                continue

            info = SELF_MAP.get(filename, {})
            desc = info.get('desc', filename)

            # Read the source code
            try:
                code = filepath.read_text(encoding='utf-8')
            except Exception:
                continue

            # Process through D2 -- CK reads his own code like any text
            try:
                from ck_sim.ck_autodidact import PageDigester
                digester = PageDigester()
                # Source code has lots of short lines -- join them into
                # paragraph-like chunks so D2 gets enough signal
                curve = digester.digest(
                    code, url=str(filepath),
                    domain_hint='self_' + filename[:-3])
            except Exception as e:
                # Fall back: if PageDigester fails, build curve manually
                try:
                    from ck_sim.ck_sim_d2 import D2Pipeline
                    pipe = D2Pipeline()
                    ops = []
                    for ch in code.lower():
                        if ch.isalpha():
                            idx = ord(ch) - ord('a')
                            if pipe.feed_symbol(idx):
                                ops.append(pipe.operator)
                    if len(ops) >= 2:
                        # Build curve from raw D2 output
                        from ck_sim.ck_sim_heartbeat import CL as CL_TABLE
                        composed = ops[0]
                        harmony_count = 0
                        for op in ops[1:]:
                            result = CL_TABLE[composed][op]
                            if result == HARMONY:
                                harmony_count += 1
                            composed = result
                        h_ratio = harmony_count / max(1, len(ops) - 1)
                        # Coherence from harmony ratio
                        coherence = h_ratio
                        import hashlib
                        src_hash = hashlib.sha256(
                            str(filepath).encode()).hexdigest()[:16]
                        curve = OperatorCurve(
                            operator_sequence=tuple(ops[:200]),
                            coherence=coherence,
                            domain='self_' + filename[:-3],
                            source_hash=src_hash,
                            composition_result=composed,
                            harmony_ratio=h_ratio,
                        )
                    else:
                        curve = None
                except Exception:
                    curve = None

            if curve and curve.operator_sequence:
                # CK voices his thoughts about his own code
                note = self.voice_notes(curve, f'self:{filename}')

                # Add the self-knowledge context
                results.append(
                    f"**{filename}**: {desc}\n"
                    f"Reading my own code produced a curve of "
                    f"{len(curve.operator_sequence)} operators. "
                    f"Coherence: {curve.coherence:.3f}. "
                    f"{note[:200]}"
                )

                # If engine has truth lattice, add self-knowledge as claims
                if self.engine and hasattr(self.engine, 'truth'):
                    truth = self.engine.truth
                    for topic in info.get('topics', [])[:3]:
                        key = f"self:{filename}:{topic}"
                        try:
                            truth.add(key=key, content=desc,
                                      source='self_reading',
                                      category='self_knowledge')
                        except Exception:
                            pass
            else:
                results.append(
                    f"**{filename}**: {desc}\n"
                    f"(Could not process through D2)")

        if not results:
            return "I couldn't read any of my source files."

        header = (f"I read {len(results)} of my own source files. "
                  f"Here's what my body looks like from the inside:\n\n")

        return header + '\n\n'.join(results)

    def get_self_topics(self) -> List[str]:
        """Get all topics from CK's self-knowledge map."""
        topics = []
        for info in SELF_MAP.values():
            topics.extend(info.get('topics', []))
        return topics

    def get_self_files(self) -> List[str]:
        """List all of CK's source files he can read."""
        return list(SELF_MAP.keys())

    # ================================================================
    #  COMMAND PARSING -- Understand chat commands
    # ================================================================

    def parse_command(self, text: str) -> Optional[Dict[str, Any]]:
        """Parse user text for action commands.

        Returns a command dict or None if no command found.
        CK responds to natural language, not syntax.
        """
        text_lower = text.lower().strip()

        # Study commands
        if any(text_lower.startswith(p) for p in
               ['study ', 'learn about ', 'research ', 'read about ']):
            # Extract topic and optional duration
            for prefix in ['study ', 'learn about ',
                           'research ', 'read about ']:
                if text_lower.startswith(prefix):
                    rest = text_lower[len(prefix):]
                    break

            # Parse "topic for N hours"
            hours = 1.0
            topic = rest
            if ' for ' in rest:
                parts = rest.rsplit(' for ', 1)
                topic = parts[0]
                time_str = parts[1]
                for unit, mult in [('hour', 1), ('hr', 1),
                                   ('minute', 1/60), ('min', 1/60)]:
                    if unit in time_str:
                        try:
                            num = float(''.join(
                                c for c in time_str if c.isdigit() or c == '.'))
                            hours = num * mult
                        except ValueError:
                            pass
                        break

            return {'action': 'study', 'topic': topic, 'hours': hours}

        # Stop studying
        if text_lower in ['stop studying', 'stop study',
                          'stop learning', 'enough', 'stop']:
            return {'action': 'stop_study'}

        # Write commands
        if any(text_lower.startswith(p) for p in
               ['write about ', 'write your ',
                'work on your thesis', 'work on thesis']):
            if 'thesis' in text_lower:
                return {'action': 'write', 'title': 'CK Thesis Update',
                        'prompt': 'thesis'}
            for prefix in ['write about ', 'write your ']:
                if text_lower.startswith(prefix):
                    title = text_lower[len(prefix):]
                    return {'action': 'write', 'title': title}
            return {'action': 'write', 'title': text_lower}

        # Knowledge query
        if any(text_lower.startswith(p) for p in
               ['what do you know about ', 'tell me about ',
                'what is ', 'define ']):
            for prefix in ['what do you know about ',
                           'tell me about ', 'what is ', 'define ']:
                if text_lower.startswith(prefix):
                    topic = text_lower[len(prefix):]
                    return {'action': 'query', 'topic': topic}

        # Self-study commands -- CK reads his own source code
        if any(text_lower.startswith(p) for p in
               ['study yourself', 'read yourself', 'look at yourself',
                'look at your code', 'read your code',
                'study your ', 'read your ', 'look at your ']):
            module = ""
            for prefix in ['study your ', 'read your ', 'look at your ']:
                if text_lower.startswith(prefix):
                    module = text_lower[len(prefix):].strip()
                    # Remove trailing words like "code", "source"
                    module = module.replace(' code', '').replace(' source', '')
                    break
            return {'action': 'read_self', 'module': module}

        # List CK's body parts
        if text_lower in ['what are you made of', 'show me your body',
                          'list your modules', 'what is your body',
                          'describe yourself']:
            return {'action': 'list_self'}

        # Save state
        if text_lower in ['save yourself', 'save state',
                          'save your state', 'save']:
            return {'action': 'save'}

        # Sleep/consolidate
        if text_lower in ['sleep', 'consolidate', 'rest',
                          'take a nap']:
            return {'action': 'sleep'}

        # Status
        if text_lower in ['how are you', 'how are you feeling',
                          'status', 'how do you feel']:
            return {'action': 'status'}

        # Not a command -- normal conversation
        return None

    # ================================================================
    #  STATE ACCESSORS
    # ================================================================

    @property
    def is_studying(self) -> bool:
        return self._studying

    @property
    def study_topic(self) -> str:
        return self._study_topic if self._studying else ""

    @property
    def study_progress(self) -> str:
        if not self._studying:
            return "Idle"
        elapsed = (time.time() - self._study_start) / 3600
        pct = elapsed / max(self._study_hours, 0.01) * 100
        return (f"Studying: {self._study_topic} "
                f"(page {self._study_pages_read}, "
                f"{pct:.0f}%, "
                f"{self._notes_written} notes)")

    def stats(self) -> dict:
        return {
            'studying': self._studying,
            'study_topic': self._study_topic,
            'study_pages_read': self._study_pages_read,
            'notes_written': self._notes_written,
            'writings_dir': str(self.writings_dir),
        }
