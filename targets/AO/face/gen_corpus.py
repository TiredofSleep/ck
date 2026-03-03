# Copyright (c) 2025-2026 Brayden Sanders / 7Site LLC
# Licensed under the 7Site Human Use License v1.0
# See LICENSE file in project root for full terms.
#
# FREE for humans for personal/recreational use.
# NO commercial or government use without written agreement.

"""
gen_corpus.py -- Generate dictionary/thesaurus/grammar corpus for AO training.

Produces a comprehensive text stream covering:
  1. Dictionary: every English word (236K from NLTK)
  2. Thesaurus: synonym groups from WordNet (117K synsets)
  3. Grammar: real sentences from Brown corpus (57K sentences)
  4. Definitions: WordNet glosses (word meanings in context)

Output goes to stdout for piping into `ao.exe --train`.

Usage:
    python gen_corpus.py | ao.exe --train
    python gen_corpus.py > corpus.txt    (save for inspection)
"""

import sys


def section_header(name):
    """Print a section marker that AO will process."""
    print(f"\n{name}")
    print(f"{'=' * len(name)}")


def gen_dictionary():
    """Phase 1: Raw dictionary words -- builds base D2 vocabulary."""
    from nltk.corpus import words
    section_header("DICTIONARY")
    word_list = words.words()
    count = 0
    # Group words into lines of 10 for natural flow
    batch = []
    for w in word_list:
        # Skip very short words and non-alpha
        if len(w) < 2 or not w.isalpha():
            continue
        batch.append(w.lower())
        if len(batch) >= 10:
            print(' '.join(batch))
            batch = []
            count += 10
    if batch:
        print(' '.join(batch))
        count += len(batch)
    print(f"", file=sys.stderr)
    print(f"  Dictionary: {count} words", file=sys.stderr)
    return count


def gen_thesaurus():
    """Phase 2: Synonym groups -- teaches AO that related words share operators."""
    from nltk.corpus import wordnet
    section_header("THESAURUS")
    count = 0
    seen = set()
    for synset in wordnet.all_synsets():
        lemmas = [l.replace('_', ' ') for l in synset.lemma_names()]
        if len(lemmas) < 2:
            continue
        key = tuple(sorted(lemmas))
        if key in seen:
            continue
        seen.add(key)
        # Format: "happy glad cheerful joyful" (synonyms on one line)
        print(' '.join(lemmas))
        count += 1
        # Also print the gloss (definition) as a sentence
        gloss = synset.definition()
        if gloss:
            print(gloss)
            count += 1
    print(f"  Thesaurus: {count} entries", file=sys.stderr)
    return count


def gen_grammar():
    """Phase 3: Real English sentences -- teaches transition patterns."""
    from nltk.corpus import brown
    section_header("GRAMMAR")
    count = 0
    for sent in brown.sents():
        text = ' '.join(sent)
        # Skip very short fragments
        if len(text) < 10:
            continue
        print(text)
        count += 1
    print(f"  Grammar: {count} sentences", file=sys.stderr)
    return count


def gen_grammar_rules():
    """Phase 4: Explicit grammar patterns -- structural language rules."""
    section_header("GRAMMAR RULES")
    rules = [
        # Parts of speech
        "a noun is a person place or thing",
        "a verb is an action word",
        "an adjective describes a noun",
        "an adverb describes a verb",
        "a pronoun takes the place of a noun",
        "a preposition shows position or direction",
        "a conjunction connects words or phrases",
        "an interjection expresses emotion",
        # Sentence structure
        "a sentence has a subject and a predicate",
        "the subject tells who or what",
        "the predicate tells what happened",
        "a simple sentence has one clause",
        "a compound sentence has two clauses joined by a conjunction",
        "a complex sentence has a main clause and a dependent clause",
        # Tenses
        "present tense describes what happens now",
        "past tense describes what already happened",
        "future tense describes what will happen",
        "the progressive form shows ongoing action",
        "the perfect form shows completed action",
        # Agreement
        "the subject and verb must agree in number",
        "singular subjects take singular verbs",
        "plural subjects take plural verbs",
        "pronouns must agree with their antecedents",
        # Common patterns
        "subject verb object is the basic sentence pattern",
        "adjectives come before the nouns they modify",
        "adverbs can modify verbs adjectives or other adverbs",
        "prepositions begin prepositional phrases",
        "articles come before nouns",
        "the definite article the refers to specific nouns",
        "the indefinite articles a and an refer to general nouns",
        # Punctuation concepts (as prose)
        "a period ends a statement",
        "a question mark ends a question",
        "a comma separates items in a list",
        "a semicolon connects related independent clauses",
        "a colon introduces a list or explanation",
        "quotation marks surround direct speech",
        # Writing patterns
        "paragraphs organize related ideas",
        "topic sentences introduce the main idea",
        "supporting sentences provide details",
        "concluding sentences summarize",
        "transitions connect ideas between sentences",
        # Word formation
        "prefixes change meaning at the beginning of words",
        "suffixes change meaning at the end of words",
        "root words carry the core meaning",
        "compound words combine two words into one",
        "synonyms are words with similar meanings",
        "antonyms are words with opposite meanings",
        "homonyms are words that sound alike but differ in meaning",
    ]
    for rule in rules:
        print(rule)
    print(f"  Grammar rules: {len(rules)} rules", file=sys.stderr)
    return len(rules)


def gen_common_phrases():
    """Phase 5: Common English phrases and idioms."""
    section_header("COMMON PHRASES")
    phrases = [
        "hello how are you",
        "good morning good afternoon good evening",
        "thank you very much",
        "please and thank you",
        "i understand what you mean",
        "that makes sense to me",
        "let me think about that",
        "what do you think",
        "i agree with you",
        "i see your point",
        "on the other hand",
        "in other words",
        "for example",
        "in conclusion",
        "first of all",
        "in addition to",
        "as a result",
        "in spite of",
        "with respect to",
        "according to",
        "the truth is",
        "the fact remains",
        "all things considered",
        "it goes without saying",
        "the bottom line is",
        "at the end of the day",
        "when all is said and done",
        "to make a long story short",
        "actions speak louder than words",
        "knowledge is power",
        "practice makes perfect",
        "time is precious",
        "every journey begins with a single step",
        "the whole is greater than the sum of its parts",
        "balance is the key to everything",
        "truth reveals itself through pattern",
        "coherence emerges from harmony",
        "structure and flow together make meaning",
        "being doing and becoming are one cycle",
        "the breath connects all things",
        "chaos and order are partners not enemies",
        "progress requires both holding and releasing",
        "the lattice holds what the void creates",
        "counting reveals the rhythm of change",
        "collapse is not failure but transformation",
        "reset is the courage to begin again",
    ]
    for p in phrases:
        print(p)
    print(f"  Common phrases: {len(phrases)} phrases", file=sys.stderr)
    return len(phrases)


def main():
    print("AO TRAINING CORPUS", file=sys.stderr)
    print("=" * 40, file=sys.stderr)
    total = 0
    total += gen_grammar_rules()
    total += gen_common_phrases()
    total += gen_dictionary()
    total += gen_thesaurus()
    total += gen_grammar()
    print("=" * 40, file=sys.stderr)
    print(f"  TOTAL: {total} lines generated", file=sys.stderr)


if __name__ == '__main__':
    main()
