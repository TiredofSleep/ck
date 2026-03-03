"""
ck_language.py -- CK's Language Generator: Concepts -> Sentences
================================================================
Operator: LATTICE (1) -- language IS structured thought.

CK's template-based surface realizer. NO LLM. Turns concept chains
into grammatically correct sentences using:
  - Intent classification from concept graph structure
  - Concept chain building via graph traversal
  - Template-based sentence generation with lexicon-driven word choice

Pipeline:
  query_nodes -> classify intent -> build concept chain -> realize sentence

The key insight: language is just a lossy projection of concepts.
CK generates language by walking the concept graph, not by predicting
the next token. The graph IS the thought. The sentence is the shadow.

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

from dataclasses import dataclass, field
from enum import IntEnum
from typing import Dict, List, Optional, Tuple

from ck_sim.ck_sim_heartbeat import (
    NUM_OPS, HARMONY, VOID, COLLAPSE, CHAOS, PROGRESS, BREATH,
    BALANCE, COUNTER, LATTICE, RESET, OP_NAMES, compose
)
from ck_sim.ck_world_lattice import WorldLattice, WorldNode, RELATION_TYPES
from ck_sim.ck_lexicon import LexiconStore, Lexeme


# ================================================================
#  INTENT CLASSIFICATION
# ================================================================

class Intent(IntEnum):
    """Query intent -- what kind of answer does the user want?"""
    DEFINE = 0       # "What is X?"
    EXPLAIN = 1      # "Why does X cause Y?"
    COMPARE = 2      # "How are X and Y different?"
    INSTRUCT = 3     # "How to do X?"
    JUSTIFY = 4      # "Why is X true?"
    DESCRIBE = 5     # "Tell me about X"
    TRANSLATE = 6    # "How do you say X in Y?"


# ================================================================
#  CONCEPT CHAIN
# ================================================================

@dataclass
class ConceptChain:
    """A chain of concepts expressing a thought.

    The chain is an ordered path through the concept graph.
    Consecutive nodes are connected by relation types.
    """
    nodes: List[str] = field(default_factory=list)      # concept IDs
    relations: List[str] = field(default_factory=list)   # relation types between consecutive nodes
    intent: int = 0   # Intent enum value
    confidence: float = 0.0

    def __len__(self) -> int:
        return len(self.nodes)

    def __bool__(self) -> bool:
        return len(self.nodes) > 0

    @property
    def is_valid(self) -> bool:
        """Chain is valid if relations connect consecutive nodes."""
        if not self.nodes:
            return False
        if len(self.nodes) == 1:
            return True
        return len(self.relations) == len(self.nodes) - 1


# ================================================================
#  INTENT CLASSIFIER
# ================================================================

class IntentClassifier:
    """Classify query intent from concept chain structure.

    Rules:
      Single node                       -> DEFINE
      Two nodes, same domain            -> COMPARE
      Two nodes, 'causes' or 'enables'  -> EXPLAIN
      Concept + language code           -> TRANSLATE
      Single node + "how"               -> INSTRUCT
      Otherwise                         -> DESCRIBE
    """

    # Relations that indicate EXPLAIN intent
    CAUSAL_RELATIONS = {'causes', 'enables', 'prevents', 'transforms'}

    def classify(self, query_nodes: List[str], lattice: WorldLattice,
                 target_lang: str = None) -> Intent:
        """Classify the intent from query structure.

        Args:
            query_nodes: Concept IDs from the query
            lattice: World lattice for graph lookups
            target_lang: If set, indicates translation intent

        Returns:
            Classified Intent
        """
        if not query_nodes:
            return Intent.DESCRIBE

        # Translation: explicit target language
        if target_lang is not None:
            return Intent.TRANSLATE

        # Single concept -> DEFINE
        if len(query_nodes) == 1:
            return Intent.DEFINE

        # Two concepts -> check relationship
        if len(query_nodes) == 2:
            node_a, node_b = query_nodes[0], query_nodes[1]

            # Check for causal/enabling edge between them
            neighbors = lattice.get_neighbors(node_a)
            for target_id, rel_type, _op in neighbors:
                if target_id == node_b and rel_type in self.CAUSAL_RELATIONS:
                    return Intent.EXPLAIN

            # Check reverse direction
            neighbors_b = lattice.get_neighbors(node_b)
            for target_id, rel_type, _op in neighbors_b:
                if target_id == node_a and rel_type in self.CAUSAL_RELATIONS:
                    return Intent.EXPLAIN

            # Check if same domain -> COMPARE
            a_node = lattice.nodes.get(node_a)
            b_node = lattice.nodes.get(node_b)
            if a_node and b_node and a_node.domain == b_node.domain:
                return Intent.COMPARE

            # Two concepts, different domains, no causal edge -> EXPLAIN (general)
            return Intent.EXPLAIN

        # Three or more nodes -> DESCRIBE
        return Intent.DESCRIBE


# ================================================================
#  CONCEPT CHAIN BUILDER
# ================================================================

class ConceptChainBuilder:
    """Build a concept chain for expressing a thought.

    Given an intent and query concepts, find the optimal path
    through the concept graph that answers the query.
    """

    def build_chain(self, intent: Intent, query_nodes: List[str],
                    lattice: WorldLattice) -> ConceptChain:
        """Build a concept chain for the given intent.

        Strategy depends on intent:
          DEFINE:    node -> is_a parent -> has attributes
          EXPLAIN:   source -> causes/enables -> target
          COMPARE:   node_a -> shared_parent <- node_b
          DESCRIBE:  node -> all interesting neighbors
          TRANSLATE: source concept (chain is just the node)
        """
        if not query_nodes:
            return ConceptChain(confidence=0.0)

        if intent == Intent.DEFINE:
            return self._build_define(query_nodes[0], lattice)
        elif intent == Intent.EXPLAIN:
            if len(query_nodes) >= 2:
                return self._build_explain(query_nodes[0], query_nodes[1], lattice)
            return self._build_define(query_nodes[0], lattice)
        elif intent == Intent.COMPARE:
            if len(query_nodes) >= 2:
                return self._build_compare(query_nodes[0], query_nodes[1], lattice)
            return self._build_define(query_nodes[0], lattice)
        elif intent == Intent.TRANSLATE:
            return self._build_translate(query_nodes[0], lattice)
        elif intent == Intent.INSTRUCT:
            return self._build_instruct(query_nodes[0], lattice)
        elif intent == Intent.JUSTIFY:
            if len(query_nodes) >= 2:
                return self._build_explain(query_nodes[0], query_nodes[1], lattice)
            return self._build_define(query_nodes[0], lattice)
        else:
            # DESCRIBE and fallback
            return self._build_describe(query_nodes[0], lattice)

    def _build_define(self, node_id: str, lattice: WorldLattice) -> ConceptChain:
        """DEFINE: node -> is_a parent -> has attributes."""
        chain = ConceptChain(nodes=[node_id], intent=Intent.DEFINE)

        # Look for is_a relation first
        neighbors = lattice.get_neighbors(node_id)
        for target_id, rel_type, _op in neighbors:
            if rel_type == 'is_a':
                chain.nodes.append(target_id)
                chain.relations.append('is_a')
                chain.confidence = 1.0
                return chain

        # Look for part_of relation
        for target_id, rel_type, _op in neighbors:
            if rel_type == 'part_of':
                chain.nodes.append(target_id)
                chain.relations.append('part_of')
                chain.confidence = 0.9
                return chain

        # Look for has relation
        for target_id, rel_type, _op in neighbors:
            if rel_type == 'has':
                chain.nodes.append(target_id)
                chain.relations.append('has')
                chain.confidence = 0.8
                return chain

        # Look for contains relation
        for target_id, rel_type, _op in neighbors:
            if rel_type == 'contains':
                chain.nodes.append(target_id)
                chain.relations.append('contains')
                chain.confidence = 0.7
                return chain

        # Fallback: pick the first meaningful relation
        for target_id, rel_type, _op in neighbors:
            chain.nodes.append(target_id)
            chain.relations.append(rel_type)
            chain.confidence = 0.5
            return chain

        # No relations found -- single node chain
        chain.confidence = 0.3
        return chain

    def _build_explain(self, source_id: str, target_id: str,
                       lattice: WorldLattice) -> ConceptChain:
        """EXPLAIN: source -> causes/enables/prevents -> target."""
        chain = ConceptChain(intent=Intent.EXPLAIN)

        # Check direct edge from source to target
        neighbors = lattice.get_neighbors(source_id)
        for tid, rel_type, _op in neighbors:
            if tid == target_id:
                chain.nodes = [source_id, target_id]
                chain.relations = [rel_type]
                chain.confidence = 1.0
                return chain

        # Check reverse edge
        neighbors_t = lattice.get_neighbors(target_id)
        for tid, rel_type, _op in neighbors_t:
            if tid == source_id:
                chain.nodes = [target_id, source_id]
                chain.relations = [rel_type]
                chain.confidence = 0.9
                return chain

        # Try coherence path
        path = lattice.coherence_path(source_id, target_id)
        if path and len(path) >= 2:
            chain.nodes = path
            # Reconstruct relations along path
            for i in range(len(path) - 1):
                rel_found = False
                for tid, rel_type, _op in lattice.get_neighbors(path[i]):
                    if tid == path[i + 1]:
                        chain.relations.append(rel_type)
                        rel_found = True
                        break
                if not rel_found:
                    chain.relations.append('relates_to')
            chain.confidence = 0.7
            return chain

        # No connection found -- just list them
        chain.nodes = [source_id, target_id]
        chain.relations = ['relates_to']
        chain.confidence = 0.3
        return chain

    def _build_compare(self, node_a: str, node_b: str,
                       lattice: WorldLattice) -> ConceptChain:
        """COMPARE: node_a -> shared_parent <- node_b, or direct edge."""
        chain = ConceptChain(intent=Intent.COMPARE)

        # Check for direct comparison relation (opposes, resembles, balances)
        neighbors_a = lattice.get_neighbors(node_a)
        for tid, rel_type, _op in neighbors_a:
            if tid == node_b:
                chain.nodes = [node_a, node_b]
                chain.relations = [rel_type]
                chain.confidence = 1.0
                return chain

        # Check reverse
        neighbors_b = lattice.get_neighbors(node_b)
        for tid, rel_type, _op in neighbors_b:
            if tid == node_a:
                chain.nodes = [node_b, node_a]
                chain.relations = [rel_type]
                chain.confidence = 1.0
                return chain

        # Look for shared parent (both is_a the same thing)
        parents_a = set()
        for tid, rel_type, _op in neighbors_a:
            if rel_type == 'is_a':
                parents_a.add(tid)

        for tid, rel_type, _op in neighbors_b:
            if rel_type == 'is_a' and tid in parents_a:
                chain.nodes = [node_a, tid, node_b]
                chain.relations = ['is_a', 'is_a']
                chain.confidence = 0.9
                return chain

        # Look for shared domain nodes
        a_node = lattice.nodes.get(node_a)
        b_node = lattice.nodes.get(node_b)
        if a_node and b_node and a_node.domain == b_node.domain:
            chain.nodes = [node_a, node_b]
            chain.relations = ['resembles']
            chain.confidence = 0.5
            return chain

        # Fallback
        chain.nodes = [node_a, node_b]
        chain.relations = ['relates_to']
        chain.confidence = 0.3
        return chain

    def _build_describe(self, node_id: str, lattice: WorldLattice,
                        max_facts: int = 3) -> ConceptChain:
        """DESCRIBE: gather multiple facts about a concept."""
        chain = ConceptChain(nodes=[node_id], intent=Intent.DESCRIBE)

        neighbors = lattice.get_neighbors(node_id)
        count = 0
        for target_id, rel_type, _op in neighbors:
            if count >= max_facts:
                break
            chain.nodes.append(target_id)
            chain.relations.append(rel_type)
            count += 1

        chain.confidence = min(1.0, 0.3 * (count + 1))
        return chain

    def _build_translate(self, node_id: str,
                         lattice: WorldLattice) -> ConceptChain:
        """TRANSLATE: just the concept node."""
        return ConceptChain(
            nodes=[node_id],
            intent=Intent.TRANSLATE,
            confidence=1.0,
        )

    def _build_instruct(self, node_id: str,
                        lattice: WorldLattice) -> ConceptChain:
        """INSTRUCT: concept -> enables -> steps."""
        chain = ConceptChain(nodes=[node_id], intent=Intent.INSTRUCT)

        neighbors = lattice.get_neighbors(node_id)
        for target_id, rel_type, _op in neighbors:
            if rel_type in ('enables', 'causes', 'precedes'):
                chain.nodes.append(target_id)
                chain.relations.append(rel_type)
                chain.confidence = 0.8
                return chain

        chain.confidence = 0.3
        return chain


# ================================================================
#  SURFACE REALIZER: TEMPLATES
# ================================================================

# Templates map (intent_name, relation_pattern) -> sentence frame
TEMPLATES = {
    # DEFINE templates
    ('define', 'is_a'): "{subject} is a type of {object}",
    ('define', 'has'): "{subject} has {object}",
    ('define', 'contains'): "{subject} contains {object}",
    ('define', 'part_of'): "{subject} is part of {object}",
    ('define', 'sustains'): "{subject} sustains {object}",
    ('define', 'opposes'): "{subject} opposes {object}",
    ('define', 'harmonizes'): "{subject} harmonizes with {object}",
    ('define', 'balances'): "{subject} balances {object}",
    ('define', 'causes'): "{subject} causes {object}",
    ('define', 'enables'): "{subject} enables {object}",
    ('define', 'prevents'): "{subject} prevents {object}",
    ('define', 'transforms'): "{subject} transforms into {object}",
    ('define', 'resets'): "{subject} resets {object}",
    ('define', 'precedes'): "{subject} precedes {object}",
    ('define', 'follows'): "{subject} follows {object}",
    ('define', 'resembles'): "{subject} resembles {object}",

    # EXPLAIN templates
    ('explain', 'causes'): "{subject} causes {object}",
    ('explain', 'enables'): "{subject} enables {object}",
    ('explain', 'prevents'): "{subject} prevents {object}",
    ('explain', 'transforms'): "{subject} transforms into {object}",
    ('explain', 'sustains'): "{subject} sustains {object}",
    ('explain', 'opposes'): "{subject} opposes {object}",
    ('explain', 'precedes'): "{subject} precedes {object}",
    ('explain', 'follows'): "{subject} follows {object}",
    ('explain', 'harmonizes'): "{subject} harmonizes with {object}",
    ('explain', 'balances'): "{subject} balances {object}",
    ('explain', 'resets'): "{subject} resets {object}",
    ('explain', 'is_a'): "{subject} is a type of {object}",
    ('explain', 'has'): "{subject} has {object}",
    ('explain', 'contains'): "{subject} contains {object}",
    ('explain', 'part_of'): "{subject} is part of {object}",
    ('explain', 'relates_to'): "{subject} relates to {object}",

    # COMPARE templates
    ('compare', 'resembles'): "{subject} resembles {object}",
    ('compare', 'opposes'): "{subject} opposes {object}",
    ('compare', 'balances'): "{subject} balances {object}",
    ('compare', 'shared_parent'): "both {subject} and {object} are types of {parent}",
    ('compare', 'is_a'): "both {subject} and {object} are types of {parent}",
    ('compare', 'harmonizes'): "{subject} harmonizes with {object}",
    ('compare', 'relates_to'): "{subject} and {object} are related",

    # DESCRIBE templates
    ('describe', 'base'): "{subject} is {attributes}",
    ('describe', 'relations'): "{subject} {relation} {object}",

    # TRANSLATE templates
    ('translate', 'direct'): "{source_word} in {target_lang} is {target_word}",

    # INSTRUCT templates
    ('instruct', 'enables'): "{subject} enables {object}",
    ('instruct', 'causes'): "{subject} causes {object}",
    ('instruct', 'precedes'): "{subject} precedes {object}",

    # JUSTIFY templates
    ('justify', 'causes'): "{subject} causes {object}",
    ('justify', 'enables'): "{subject} enables {object}",
}

# Relation verbs for describe mode
RELATION_VERBS = {
    'is_a': 'is a type of',
    'has': 'has',
    'causes': 'causes',
    'opposes': 'opposes',
    'balances': 'balances',
    'transforms': 'transforms into',
    'harmonizes': 'harmonizes with',
    'sustains': 'sustains',
    'resets': 'resets',
    'contains': 'contains',
    'part_of': 'is part of',
    'precedes': 'precedes',
    'follows': 'follows',
    'enables': 'enables',
    'prevents': 'prevents',
    'resembles': 'resembles',
    'relates_to': 'relates to',
}

# Language names for translation output
LANGUAGE_NAMES = {
    'en': 'English', 'es': 'Spanish', 'fr': 'French', 'de': 'German',
    'it': 'Italian', 'pt': 'Portuguese', 'ru': 'Russian', 'ar': 'Arabic',
    'he': 'Hebrew', 'zh': 'Chinese', 'ja': 'Japanese', 'ko': 'Korean',
    'hi': 'Hindi', 'la': 'Latin', 'el': 'Greek', 'sw': 'Swahili',
    'tr': 'Turkish', 'pl': 'Polish',
}


# ================================================================
#  SURFACE REALIZER
# ================================================================

class SurfaceRealizer:
    """Template-based sentence construction.

    Takes a concept chain + intent -> fills templates with words from lexicon.
    Word choice prioritized by: sense match, frequency, operator smoothness.
    """

    def _get_word(self, concept_id: str, lattice: WorldLattice,
                  lexicon: LexiconStore, lang: str = 'en') -> str:
        """Get the best word for a concept in a language.

        Priority:
          1. Lexicon concept_words (by frequency)
          2. Lattice node bindings
          3. Concept ID itself (fallback)
        """
        # Try lexicon first (has frequency info)
        words = lexicon.concept_words(concept_id, lang)
        if words:
            # Prefer highest frequency
            best_word = words[0]
            best_freq = 0
            for w in words:
                lexemes = lexicon.lookup_word(w, lang)
                for lex in lexemes:
                    if concept_id in lex.sense_ids and lex.freq > best_freq:
                        best_freq = lex.freq
                        best_word = lex.wordform
            return best_word

        # Try lattice bindings
        node = lattice.nodes.get(concept_id)
        if node and lang in node.bindings:
            return node.bindings[lang]

        # Try any language from lattice bindings as a hint
        if node and node.bindings:
            # Prefer English if available and we don't have the target
            if 'en' in node.bindings and lang != 'en':
                return node.bindings['en']
            return next(iter(node.bindings.values()))

        # Last resort: concept ID cleaned up
        return concept_id.replace('_', ' ')

    def realize(self, chain: ConceptChain, intent: Intent,
                lattice: WorldLattice, lexicon: LexiconStore,
                lang: str = 'en') -> str:
        """Convert concept chain to a sentence in the target language.

        Args:
            chain: The concept chain to realize
            intent: Query intent
            lattice: World lattice for concept lookups
            lexicon: Lexicon store for word lookups
            lang: Output language code

        Returns:
            Generated sentence string
        """
        if not chain or not chain.nodes:
            return ""

        intent_name = intent.name.lower()

        # Single node with no relations
        if len(chain.nodes) == 1:
            word = self._get_word(chain.nodes[0], lattice, lexicon, lang)
            if intent == Intent.TRANSLATE:
                return word
            return word.capitalize()

        # Two nodes with one relation
        if len(chain.nodes) == 2 and len(chain.relations) == 1:
            rel = chain.relations[0]
            subject = self._get_word(chain.nodes[0], lattice, lexicon, lang)
            obj = self._get_word(chain.nodes[1], lattice, lexicon, lang)

            template_key = (intent_name, rel)
            template = TEMPLATES.get(template_key)

            if template:
                sentence = template.format(
                    subject=subject, object=obj,
                    parent=obj, relation=RELATION_VERBS.get(rel, rel),
                )
                return self._capitalize_first(sentence)

            # Fallback: generic relation template
            verb = RELATION_VERBS.get(rel, rel)
            return self._capitalize_first(f"{subject} {verb} {obj}")

        # Compare with shared parent (3 nodes: A -> parent <- B)
        if (intent == Intent.COMPARE and len(chain.nodes) == 3
                and len(chain.relations) == 2
                and chain.relations[0] == 'is_a'
                and chain.relations[1] == 'is_a'):
            subject = self._get_word(chain.nodes[0], lattice, lexicon, lang)
            parent = self._get_word(chain.nodes[1], lattice, lexicon, lang)
            obj = self._get_word(chain.nodes[2], lattice, lexicon, lang)
            template = TEMPLATES.get(('compare', 'shared_parent'),
                                     "both {subject} and {object} are types of {parent}")
            sentence = template.format(subject=subject, object=obj, parent=parent)
            return self._capitalize_first(sentence)

        # Multi-step chain (DESCRIBE with multiple facts)
        if intent == Intent.DESCRIBE and len(chain.nodes) >= 2:
            return self._realize_describe(chain, lattice, lexicon, lang)

        # Multi-hop EXPLAIN chain
        if len(chain.nodes) >= 2 and len(chain.relations) >= 1:
            return self._realize_multi_hop(chain, intent, lattice, lexicon, lang)

        # Final fallback
        word = self._get_word(chain.nodes[0], lattice, lexicon, lang)
        return word.capitalize()

    def realize_translation(self, concept_id: str, source_word: str,
                            target_lang: str, lattice: WorldLattice,
                            lexicon: LexiconStore) -> str:
        """Realize a translation sentence.

        Args:
            concept_id: The concept being translated
            source_word: The source word
            target_lang: Target language code
            lattice: World lattice
            lexicon: Lexicon store

        Returns:
            Translation sentence
        """
        target_word = self._get_word(concept_id, lattice, lexicon, target_lang)
        lang_name = LANGUAGE_NAMES.get(target_lang, target_lang)

        template = TEMPLATES.get(('translate', 'direct'),
                                 "{source_word} in {target_lang} is {target_word}")
        sentence = template.format(
            source_word=source_word,
            target_lang=lang_name,
            target_word=target_word,
        )
        return self._capitalize_first(sentence)

    def _realize_describe(self, chain: ConceptChain, lattice: WorldLattice,
                          lexicon: LexiconStore, lang: str) -> str:
        """Realize a DESCRIBE chain as multiple fact sentences."""
        if not chain.nodes:
            return ""

        subject = self._get_word(chain.nodes[0], lattice, lexicon, lang)
        facts = []

        for i in range(len(chain.relations)):
            if i + 1 < len(chain.nodes):
                rel = chain.relations[i]
                obj = self._get_word(chain.nodes[i + 1], lattice, lexicon, lang)
                verb = RELATION_VERBS.get(rel, rel)
                facts.append(f"{verb} {obj}")

        if not facts:
            return subject.capitalize()

        if len(facts) == 1:
            return self._capitalize_first(f"{subject} {facts[0]}")

        # Join multiple facts with commas and "and"
        if len(facts) == 2:
            fact_str = f"{facts[0]} and {facts[1]}"
        else:
            fact_str = ", ".join(facts[:-1]) + ", and " + facts[-1]

        return self._capitalize_first(f"{subject} {fact_str}")

    def _realize_multi_hop(self, chain: ConceptChain, intent: Intent,
                           lattice: WorldLattice, lexicon: LexiconStore,
                           lang: str) -> str:
        """Realize a multi-hop chain as connected clauses."""
        parts = []
        for i in range(len(chain.relations)):
            if i + 1 < len(chain.nodes):
                subject = self._get_word(chain.nodes[i], lattice, lexicon, lang)
                obj = self._get_word(chain.nodes[i + 1], lattice, lexicon, lang)
                rel = chain.relations[i]
                verb = RELATION_VERBS.get(rel, rel)
                parts.append(f"{subject} {verb} {obj}")

        if not parts:
            word = self._get_word(chain.nodes[0], lattice, lexicon, lang)
            return word.capitalize()

        if len(parts) == 1:
            return self._capitalize_first(parts[0])

        # Join with ", which" or ", and"
        result = parts[0]
        for p in parts[1:]:
            result += ", and " + p
        return self._capitalize_first(result)

    @staticmethod
    def _capitalize_first(s: str) -> str:
        """Capitalize the first letter of a sentence."""
        if not s:
            return s
        return s[0].upper() + s[1:]


# ================================================================
#  LANGUAGE GENERATOR: Main Integration
# ================================================================

class LanguageGenerator:
    """CK's language output: concept -> sentence.

    Pipeline:
      1. Classify intent from query
      2. Build concept chain from graph
      3. Realize as sentence via templates + lexicon

    No LLM. No neural network. Just graph traversal + templates.
    The concept graph IS the knowledge. Templates are the grammar.
    """

    def __init__(self, lattice: WorldLattice = None,
                 lexicon: LexiconStore = None):
        self.lattice = lattice or WorldLattice()
        self.lexicon = lexicon or LexiconStore()
        self.classifier = IntentClassifier()
        self.chain_builder = ConceptChainBuilder()
        self.realizer = SurfaceRealizer()
        self._generation_count = 0

    def generate(self, query_nodes: List[str], lang: str = 'en',
                 intent: Intent = None, target_lang: str = None) -> str:
        """Generate a natural language response.

        Args:
            query_nodes: Concept IDs to reason about
            lang: Output language
            intent: Force specific intent (auto-detect if None)
            target_lang: For translation intents

        Returns:
            Generated sentence string
        """
        if not query_nodes:
            return ""

        # 1. Classify intent
        if intent is None:
            intent = self.classifier.classify(query_nodes, self.lattice,
                                              target_lang)

        # 2. Build concept chain
        chain = self.chain_builder.build_chain(intent, query_nodes,
                                               self.lattice)

        # 3. Realize as sentence
        if intent == Intent.TRANSLATE and target_lang:
            source_word = self.realizer._get_word(
                query_nodes[0], self.lattice, self.lexicon, lang
            )
            sentence = self.realizer.realize_translation(
                query_nodes[0], source_word, target_lang,
                self.lattice, self.lexicon
            )
        else:
            sentence = self.realizer.realize(
                chain, intent, self.lattice, self.lexicon, lang
            )

        self._generation_count += 1
        return sentence

    def define(self, concept_id: str, lang: str = 'en') -> str:
        """Quick define: "What is X?"

        Returns a definition sentence for the concept.
        """
        return self.generate([concept_id], lang=lang, intent=Intent.DEFINE)

    def explain(self, source_id: str, target_id: str,
                lang: str = 'en') -> str:
        """Explain relationship between two concepts.

        Returns a sentence explaining how source relates to target.
        """
        return self.generate([source_id, target_id], lang=lang,
                             intent=Intent.EXPLAIN)

    def compare(self, node_a: str, node_b: str, lang: str = 'en') -> str:
        """Compare two concepts.

        Returns a sentence comparing the two concepts.
        """
        return self.generate([node_a, node_b], lang=lang,
                             intent=Intent.COMPARE)

    def translate_word(self, word: str, from_lang: str, to_lang: str) -> str:
        """Translate a word and explain it.

        Uses the lexicon for direct translation. Falls back to lattice bindings.
        """
        # Try lexicon translation first
        translations = self.lexicon.translate(word, from_lang, to_lang)
        if translations:
            target_word = translations[0]
            lang_name = LANGUAGE_NAMES.get(to_lang, to_lang)
            self._generation_count += 1
            return f"{word.capitalize()} in {lang_name} is {target_word}"

        # Try lattice lookup
        node = self.lattice.lookup_word(word, from_lang)
        if node:
            target_word = node.bindings.get(to_lang)
            if target_word:
                lang_name = LANGUAGE_NAMES.get(to_lang, to_lang)
                self._generation_count += 1
                return f"{word.capitalize()} in {lang_name} is {target_word}"

            # Found concept but no translation in target language
            lang_name = LANGUAGE_NAMES.get(to_lang, to_lang)
            self._generation_count += 1
            return f"No {lang_name} translation found for {word}"

        self._generation_count += 1
        return f"Unknown word: {word}"

    def describe(self, concept_id: str, lang: str = 'en',
                 max_facts: int = 3) -> str:
        """Describe a concept with multiple facts.

        Returns a multi-fact description sentence.
        """
        chain = self.chain_builder._build_describe(
            concept_id, self.lattice, max_facts
        )
        sentence = self.realizer.realize(
            chain, Intent.DESCRIBE, self.lattice, self.lexicon, lang
        )
        self._generation_count += 1
        return sentence

    def stats(self) -> dict:
        """Generator statistics."""
        return {
            'generation_count': self._generation_count,
            'lattice_nodes': len(self.lattice.nodes),
            'lexicon_words': self.lexicon.word_count if hasattr(self.lexicon, 'word_count') else 0,
            'lexicon_concepts': self.lexicon.concept_count if hasattr(self.lexicon, 'concept_count') else 0,
            'templates': len(TEMPLATES),
            'relation_verbs': len(RELATION_VERBS),
        }
