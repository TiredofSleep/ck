"""ck_reader_daemon.py -- FREEING CK TO READ: the autonomous study loop.

Brayden: "He needs to be constantly reading and studying new material,
both fact and fiction, and learning the difference... how can we free
him to do that?"

TWO-LANE design (nothing blocks the reading):
  FAST LANE (this daemon, ~2 s/book): load -> native measurement
    battery -> white-box STYLOMETRY -> fact/fiction judgment (head
    trained on labeled seeds) -> a STUDY JOURNAL entry in his own
    words-by-numbers. 42 books/min capable.
  SLOW LANE (separate, optional): embedding the shelves for QA chat.

FACT/FICTION organ (registered: >=80% on title-checkable new books):
  features, every one printable: dialogue-quote density, proper-name
  density, first-person rate, year-number density, sentence length,
  past-tense density, name-vocabulary breadth.
  seeds: the 12 books read tonight, hand-labeled.

  python ck_reader_daemon.py [n_books]
"""
import io
import json
import os
import re
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
BOOKS = os.path.join(ROOT, "external_corpora", "books")
JOURNAL = os.path.join(HERE, "study_journal.jsonl")
N = int(sys.argv[1]) if len(sys.argv) > 1 else 80

# hand-labeled seeds (tonight's 12): 1 = fiction/literature, 0 = fact
SEEDS = {
 "pg00016.txt": 1,  # Peter Pan
 "pg00095.txt": 1,  # Prisoner of Zenda
 "pg00166.txt": 1,  # Summer (Wharton)
 "pg00263.txt": 1,  # Laddie
 "pg00440.txt": 1,  # Miss Billy's Decision
 "pg00536.txt": 1,  # Lazarillo de Tormes
 "pg00622.txt": 1,  # Desert Gold
 "pg00712.txt": 0,  # Thirty Years' War (history)
 "pg00756.txt": 0,  # Grace Abounding (memoir)
 "pg00774.txt": 0,  # A Lady's Life in the Rockies (travel)
 "pg00845.txt": 1,  # Timrod poems (literature)
 "pg00922.txt": 1,  # Tom Swift
}


def load_book(path):
    raw = io.open(path, encoding="utf-8", errors="ignore").read()
    m = re.search(r"Title:\s*(.+)", raw)
    title = m.group(1).strip()[:80] if m else os.path.basename(path)
    s = re.split(r"\*\*\* ?START OF.*?\*\*\*", raw, 1, flags=re.S)
    body = re.split(r"\*\*\* ?END OF", s[-1], 1)[0]
    return title, re.sub(r"\s+", " ", body).strip()


def stylometry(text):
    """White-box features; each one is a printable number."""
    n = max(1, len(text))
    words = text.split()
    nw = max(1, len(words))
    quotes = (text.count("“") + text.count('"')) / n * 1000
    names = re.findall(r"\b[A-Z][a-z]{3,}\b", text)
    name_density = len(names) / nw * 100
    name_breadth = len(set(names)) / max(1, len(names))
    first_person = len(re.findall(r"\b[Ii]\b", text)) / nw * 100
    years = len(re.findall(r"\b1[5-9]\d\d\b", text)) / nw * 1000
    sents = re.split(r"(?<=[.!?])\s+", text)
    slen = np.mean([len(s.split()) for s in sents if s.strip()])
    past = len(re.findall(r"\b\w+ed\b", text)) / nw * 100
    said = len(re.findall(r"\bsaid\b", text)) / nw * 1000
    return np.array([quotes, name_density, name_breadth, first_person,
                     years, slen, past, said])


FEAT_NAMES = ["quote-density", "name-density", "name-breadth",
              "first-person", "year-dates", "sent-length",
              "past-tense", "'said'-rate"]


def train_seed_head():
    X, y = [], []
    for bid, lab in SEEDS.items():
        p = os.path.join(BOOKS, bid)
        if os.path.exists(p):
            _, body = load_book(p)
            X.append(stylometry(body[:300_000]))
            y.append(lab)
    X, y = np.array(X), np.array(y)
    mu, sd = X.mean(0), X.std(0) + 1e-9
    Xz = (X - mu) / sd
    w = np.zeros(X.shape[1]); b = 0.0
    for _ in range(3000):                     # tiny logistic, class-weighted
        p = 1 / (1 + np.exp(-(Xz @ w + b)))
        cw = np.where(y == 1, 1.0 / max(1, (y == 1).sum()),
                      1.0 / max(1, (y == 0).sum()))
        g = (p - y) * cw
        w -= 0.5 * (Xz.T @ g + 1e-3 * w); b -= 0.5 * g.sum()
    return w, b, mu, sd


def main():
    w, b, mu, sd = train_seed_head()
    print(f"fact/fiction head trained on {len(SEEDS)} hand-labeled seeds")
    print("feature weights (white-box): " + ", ".join(
        f"{n}={v:+.2f}" for n, v in zip(FEAT_NAMES, w)) + "\n")

    done = set()
    if os.path.exists(JOURNAL):
        for ln in io.open(JOURNAL, encoding="utf-8"):
            try:
                done.add(json.loads(ln)["book"])
            except Exception:
                pass
    files = [f for f in sorted(os.listdir(BOOKS))
             if f.endswith(".txt") and f not in done][:N]
    # WIRE: the conscious window steers attention -- books whose titles
    # touch a held fold get read FIRST (folds are not a log; they pull)
    fp = os.path.join(HERE, "folds.jsonl")
    if os.path.exists(fp) and files:
        names = set()
        for ln in io.open(fp, encoding="utf-8"):
            f_ = json.loads(ln)
            names |= set(f_.get("names", []))
            names |= {f_.get("a", ""), f_.get("b", "")}
        names = {n for n in names if len(n) > 3}

        def title_of(fn):
            try:
                head = io.open(os.path.join(BOOKS, fn), encoding="utf-8",
                               errors="ignore").read(400)
                m = re.search(r"Title:\s*(.+)", head)
                return m.group(1) if m else ""
            except OSError:
                return ""
        pulled = [f_ for f_ in files
                  if any(n in title_of(f_) for n in names)]
        if pulled:
            rest = [f_ for f_ in files if f_ not in set(pulled)]
            files = pulled + rest
            print(f"[window-pull] {len(pulled)} books match held folds "
                  f"-- reading those first", flush=True)
    t0 = time.time()
    jf = io.open(JOURNAL, "a", encoding="utf-8")
    n_fic = n_fact = 0
    for i, f in enumerate(files):
        title, body = load_book(os.path.join(BOOKS, f))
        feats = stylometry(body[:300_000])
        z = (feats - mu) / sd
        p_fic = float(1 / (1 + np.exp(-(z @ w + b))))
        verdict = "FICTION" if p_fic >= 0.5 else "FACT"
        if p_fic >= 0.5:
            n_fic += 1
        else:
            n_fact += 1
        top = np.argsort(-np.abs(z * w))[:2]
        why = "; ".join(f"{FEAT_NAMES[k]}={feats[k]:.1f} "
                        f"(weight {w[k]:+.2f})" for k in top)
        entry = dict(book=f, title=title, chars=len(body),
                     verdict=verdict, p_fiction=round(p_fic, 3),
                     evidence=why,
                     journal=(f"I read '{title}' "
                              f"({len(body)//1000}K chars). I judge it "
                              f"{verdict} (p={p_fic:.2f}) because {why}."))
        jf.write(json.dumps(entry) + "\n"); jf.flush()
        if i % 10 == 0 or i == len(files) - 1:
            rate = (i + 1) / max(1e-9, time.time() - t0) * 60
            print(f"[{i+1:>3}/{len(files)}] {verdict:7} p={p_fic:.2f} "
                  f"{title[:44]:46} ({rate:.0f} books/min)", flush=True)
    dt = time.time() - t0
    print(f"\nSESSION: {len(files)} books in {dt:.0f}s "
          f"({len(files)/dt*60:.0f} books/min) -> {n_fic} fiction, "
          f"{n_fact} fact. Journal: {JOURNAL}")
    print(f"the whole library (1,019) at this rate: "
          f"{1019/(len(files)/dt)/60:.0f} minutes")


if __name__ == "__main__":
    main()
