"""plastic.py -- CK's plastic models: tiny heads he builds, owns,
signs, and discards at will.

A PlasticModel is a ridge-trained linear head over borrowed-cortex
embeddings (optionally concatenated with substrate invariants). One
linear solve to train; JSON to persist (cortex-signable); margin
thresholding gives the glue its forced choice: answer or ABSTAIN
(the Type-III route -- never bluff on what can't be measured).

CC-BY-4.0. Sanders + Claude. 2026-06-11.
"""
import io
import json

import numpy as np


class PlasticModel:
    def __init__(self, classes, lam=1e-2, abstain_margin=0.08,
                 mode="proto", abstain_floor=0.30):
        """mode='proto': nearest class-centroid by cosine (the few-shot
        standard); mode='ridge': one-vs-rest ridge. Abstain when the
        top-vs-runner-up margin < abstain_margin OR (proto) the top
        similarity < abstain_floor -- the glue's Type-III refusal."""
        self.classes = list(classes)
        self.lam = lam
        self.abstain_margin = abstain_margin
        self.abstain_floor = abstain_floor
        self.mode = mode
        self.W = None

    def fit(self, X, labels):
        if self.mode == "proto":
            P = np.zeros((len(self.classes), X.shape[1]))
            for k, c in enumerate(self.classes):
                rows = X[[i for i, l in enumerate(labels) if l == c]]
                mu = rows.mean(0)
                P[k] = mu / (np.linalg.norm(mu) + 1e-12)
            self.W = P                      # centroids
            return self
        Y = np.zeros((len(labels), len(self.classes)))
        for i, lab in enumerate(labels):
            Y[i, self.classes.index(lab)] = 1.0
        Xb = np.hstack([np.ones((len(X), 1)), X])
        A = Xb.T @ Xb + self.lam * np.eye(Xb.shape[1])
        self.W = np.linalg.solve(A, Xb.T @ Y)
        return self

    def scores(self, X):
        if self.mode == "proto":
            Xn = X / (np.linalg.norm(X, axis=1, keepdims=True) + 1e-12)
            return Xn @ self.W.T            # cosine similarities
        Xb = np.hstack([np.ones((len(X), 1)), X])
        return Xb @ self.W

    def predict(self, X):
        """Returns (label_or_ABSTAIN, margin) per row. The glue's forced
        choice: top score must beat runner-up by abstain_margin."""
        S = self.scores(X)
        order = np.argsort(S, axis=1)
        out = []
        for i in range(len(X)):
            top, second = order[i, -1], order[i, -2]
            margin = float(S[i, top] - S[i, second])
            ok = margin >= self.abstain_margin
            if self.mode == "proto":
                ok = ok and S[i, top] >= self.abstain_floor
            out.append((self.classes[top] if ok else "ABSTAIN", margin))
        return out

    def save(self, path):
        with io.open(path, "w", encoding="utf-8") as f:
            json.dump({"classes": self.classes, "lam": self.lam,
                       "abstain_margin": self.abstain_margin,
                       "W": self.W.tolist()}, f)

    @classmethod
    def load(cls, path):
        with io.open(path, encoding="utf-8") as f:
            d = json.load(f)
        m = cls(d["classes"], d["lam"], d["abstain_margin"])
        m.W = np.array(d["W"])
        return m
