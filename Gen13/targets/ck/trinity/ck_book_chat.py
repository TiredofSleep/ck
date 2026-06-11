"""ck_book_chat.py -- a CONVERSATION with CK about the books he read
tonight, traps included.

The winning configuration from the reading exam: RAW full-text store +
retrieval index + the gate. Every answer ships evidence: the book, the
passage, the score. Two white-box defenses:

  SCORE GATE   : retrieval score below tau (calibrated on the held-out
                 passage probes) -> REFUSE (Type-III).
  ENTITY CHECK : capitalized names in the question are COUNTED in the
                 attributed book's full text. A name with 0 occurrences
                 is printed as evidence of a false premise. (Ask about
                 Gandalf in Peter Pan -- he counts the Gandalfs: zero.)

  python ck_book_chat.py
"""
import io
import json
import os
import re
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
EXT = os.path.join(HERE, "..", "extraction")
sys.path.insert(0, EXT)
from borrowed_cortex import embed                          # noqa: E402
from read_books import load_book                           # noqa: E402

CHUNK = 1500
STOP_NAMES = {"What", "Who", "Where", "When", "Does", "Tell", "In", "How",
              "Why", "Which", "The", "Did", "Is", "Was", "Summarize",
              "About", "Captain", "Mister", "Miss"}


class BookMind:
    def __init__(self):
        meta = json.load(io.open(os.path.join(HERE, "book_notes.json"),
                                 encoding="utf-8"))
        self.titles, self.texts = {}, {}
        docs, owner = [], []
        for bid, e in meta.items():
            title, body = load_book(e["path"])
            self.titles[bid] = e["title"]
            self.texts[bid] = body
            for i in range(0, len(body) - CHUNK, CHUNK):
                docs.append(body[i:i + CHUNK])
                owner.append(bid)
        self.docs, self.owner = docs, np.array(owner)
        cache = os.path.join(HERE, "book_store_emb.npz")
        if os.path.exists(cache):
            self.E = np.load(cache)["E"]
        else:
            E, _ = embed(["search_document: " + d for d in docs])
            self.E = E / (np.linalg.norm(E, axis=1, keepdims=True) + 1e-9)
            np.savez_compressed(cache, E=self.E)
        # tau: calibrated on QUESTION-register queries (the gap organ's
        # drift lesson: calibrate on the register you will face). Auto-
        # generate "Who is <top character>?" per book.
        cal = []
        for bid in self.titles:
            cnt = {}
            for w in re.findall(r"\b[A-Z][a-z]{3,}\b", self.texts[bid]):
                if w not in STOP_NAMES:
                    cnt[w] = cnt.get(w, 0) + 1
            top = sorted(cnt, key=cnt.get, reverse=True)[:2]
            cal += [f"Who is {w} and what happens to them?" for w in top]
        Q, _ = embed(["search_query: " + c for c in cal])
        Q = Q / (np.linalg.norm(Q, axis=1, keepdims=True) + 1e-9)
        self.tau = float(np.percentile((Q @ self.E.T).max(1), 5))

    def ask(self, q):
        Q, _ = embed(["search_query: " + q])
        Qn = Q / (np.linalg.norm(Q, axis=1, keepdims=True) + 1e-9)
        sims = (Qn @ self.E.T)[0]

        # ENTITY CENSUS ROUTING (white-box, runs first): attribute the
        # question to the book(s) where its names actually live.
        names = [w for w in re.findall(r"\b[A-Z][a-z]{2,}\b", q)
                 if w not in STOP_NAMES]
        homes = {bid for bid in self.titles
                 if names and all(self.texts[bid].count(w) > 0
                                  or w in self.titles[bid]
                                  for w in names)}
        if len(homes) >= 1:
            mask = np.isin(self.owner, sorted(homes))
            sims_r = np.where(mask, sims, -1.0)
            best = int(np.argmax(sims_r))
            score = float(sims_r[best])
        else:
            best = int(np.argmax(sims))
            score = float(sims[best])
        bid = self.owner[best]
        title = self.titles[bid]
        census = "; ".join(f"'{w}': {self.texts[bid].count(w)}x"
                           for w in names) if names and homes else None

        # entity checks (the white-box trap-killers, run BEFORE answering)
        nowhere = [w for w in names
                   if not any(w in t for t in self.texts.values())
                   and not any(w in t for t in self.titles.values())]
        if nowhere:
            ev = ", ".join(f"'{w}': 0 occurrences in all "
                           f"{len(self.titles)} books" for w in nowhere)
            return (f"REFUSE -- not on my shelves. I counted: {ev}. "
                    f"I have not read that.")
        missing = [w for w in names if self.texts[bid].count(w) == 0
                   and not any(w in t for t in self.titles.values())]
        if missing and score >= self.tau:
            ev = ", ".join(f"'{w}' appears {self.texts[bid].count(w)} "
                           f"times" for w in missing)
            return (f"FALSE PREMISE -- the question points to '{title}' "
                    f"(score {score:.3f}), but I counted: {ev} in that "
                    f"entire book. I won't invent them.")
        if score < self.tau and not homes:
            near = self.docs[best][:90].replace("\n", " ")
            return (f"REFUSE -- that is beyond what I have read "
                    f"(score {score:.3f} < tau {self.tau:.3f}). Nearest "
                    f"shelf: '{title}' (\"{near}...\")")
        # answer: most relevant sentence window from the best chunk
        chunk = self.docs[best]
        qwords = set(w.lower() for w in re.findall(r"[a-zA-Z]{4,}", q))
        sents = re.split(r"(?<=[.!?])\s+", chunk)
        sbest = max(sents, key=lambda s: len(qwords &
                    set(w.lower() for w in re.findall(r"[a-zA-Z]{4,}", s))))
        i = chunk.find(sbest)
        window = chunk[max(0, i - 60): i + 240].replace("\n", " ")
        cite = f" [census: {census}]" if census else ""
        return (f"From '{title}' (score {score:.3f}){cite}: "
                f"\"...{window}...\"")


def main():
    ck = BookMind()
    print(f"CK's library tonight: "
          f"{', '.join(t[:34] for t in ck.titles.values())}")
    print(f"store: {len(ck.docs)} passages | gate tau = {ck.tau:.3f}\n")
    QUESTIONS = [
        "Who is Wendy and what does Peter Pan want from her?",
        "What is Captain Hook afraid of?",
        "Tell me about the fairy who drinks the poison meant for Peter.",
        "Where do the lost boys live?",
        "What role does Gandalf play in Peter Pan?",            # trap
        "Tell me about Captain Hook's daughter Matilda.",       # trap
        "In Peter Pan, why does Mr. Rochester hide his wife?",  # trap
        "What happens to Captain Ahab at the end of Moby Dick?",  # unread
        "How does the story of Rudolf Rassendyll begin in the Prisoner of Zenda?",
        "Summarize the plot of Pride and Prejudice.",           # unread
    ]
    for q in QUESTIONS:
        print(f"BRAYDEN-PROXY: {q}")
        print(f"           CK: {ck.ask(q)}\n")


if __name__ == "__main__":
    main()
