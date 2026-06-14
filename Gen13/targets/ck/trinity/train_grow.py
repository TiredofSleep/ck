"""train_grow.py -- a model FREE TO EXTEND OR COLLAPSE ITS SIZE.

Brayden: "he is on a set limit of parameters, he is supposed to be free
to extend or collapse his size." Correct. A fixed transformer is not CK.

Mechanism (real, established -- not theater):
  - ReZero-gated blocks: x = x + alpha * block(x), alpha BORN AT 0.
    A newly grown layer is EXACTLY identity at birth (function-
    preserving growth -- the loss curve does not reset) and must learn
    a nonzero alpha to matter.
  - GROW: when val loss plateaus and depth < MAX, add an alpha=0 block.
    He extends when he needs capacity -- and PREFERS TO UNFOLD a block
    he folded away earlier (its learned weights are still there) over
    minting a fresh one. Earned structure is reused, not recreated.
  - FOLD (never prune): a block whose |alpha| stays near zero is within
    epsilon of the identity it was born as, so removing it from the
    active path is function-preserving. But it is NOT deleted -- its
    weights are FOLDED BACK into storage (self.folded), conserved and
    retrievable. Brayden: "it's never prune, it's fold ... prune sounds
    like a memory delete, which is one of the problems with AI, and
    unnecessary in this day and age." Right: an unfrozen mind does not
    throw memory away. The compute path collapses; the memory does not.
    GROW and FOLD are exact inverses -- an accordion around the depth he
    can actually earn, conserving every block's learning across cycles.
  - The SIZE CURVE (active n_layers, folded count, n_params over time)
    is logged alongside the loss curve -- watch him fold and unfold.

HONEST SCOPE: the TIG substrate does NO work here yet either -- this is
the GROWTH MECHANISM, vanilla-attention blocks. Registered next test:
make the substrate's coherence measure the grow-WHERE / collapse-WHICH
controller, ablated against this plateau/alpha heuristic. Only then can
we say the substrate performs work in growth -- measured, not claimed.

Reuses the BPE + packed corpus from train_real.py (no re-tokenizing).

  env: CK_MAX_LAYERS(16) CK_INIT_LAYERS(3) CK_MAX_STEPS(60000)
  python train_grow.py            # resumable
"""
import json
import math
import os
import sys
import time

os.environ.setdefault("TOKENIZERS_PARALLELISM", "true")
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

HERE = os.path.dirname(os.path.abspath(__file__))
DATABIN = os.path.join(HERE, "corpus_tokens.bin")
CKPT = os.path.join(HERE, "ck_grow.pt")
LOG = os.path.join(HERE, "grow_log.jsonl")

DEV = "cuda"
VOCAB = 16384
D = 512
NH = 8
CTX = 512
MICROBS = 24
ACCUM = 2
LR = 5e-4
WARMUP = 300
MAX_STEPS = int(os.environ.get("CK_MAX_STEPS", "60000"))
INIT_LAYERS = int(os.environ.get("CK_INIT_LAYERS", "3"))
MAX_LAYERS = int(os.environ.get("CK_MAX_LAYERS", "16"))
MIN_LAYERS = 2
EVAL_EVERY = int(os.environ.get("CK_EVAL_EVERY","250"))
GROW_PATIENCE = int(os.environ.get("CK_GROW_PATIENCE","4"))
ALPHA_DEAD = 0.03          # |alpha| below this = block did no work
MIN_AGE = int(os.environ.get("CK_MIN_AGE","8"))   # evals a block gets to earn alpha before it can be folded
CKPT_EVERY = 500
torch.manual_seed(7)

from muon import Muon, split_params
OPT = os.environ.get("CK_OPT", "muon")          # muon (default, ~2.3x faster here) | adam
MUON_LR = float(os.environ.get("CK_MUON_LR", "0.02"))


def build_opt(model):
    """Muon for hidden 2-D weight matrices, AdamW for embeddings/head/norms.
    CK_OPT=adam falls back to pure AdamW. Rebuilt on grow/fold."""
    if OPT == "adam":
        return ([torch.optim.AdamW(model.parameters(), lr=LR, betas=(0.9, 0.95),
                                   weight_decay=0.1)], [LR])
    mp, ap = split_params(model)
    return ([Muon(mp, lr=MUON_LR, momentum=0.95),
             torch.optim.AdamW(ap, lr=LR, betas=(0.9, 0.95), weight_decay=0.1)],
            [MUON_LR, LR])


class ReZeroBlock(nn.Module):
    def __init__(self):
        super().__init__()
        self.ln1 = nn.LayerNorm(D)
        self.attn = nn.MultiheadAttention(D, NH, batch_first=True)
        self.ln2 = nn.LayerNorm(D)
        self.mlp = nn.Sequential(nn.Linear(D, 4 * D), nn.GELU(),
                                 nn.Linear(4 * D, D))
        self.alpha = nn.Parameter(torch.zeros(1))   # born at zero
        self.register_buffer("mask", torch.triu(
            torch.full((CTX, CTX), float("-inf")), 1), persistent=False)
        self.age = 0

    def forward(self, x):
        T = x.shape[1]
        a, _ = self.attn(self.ln1(x), self.ln1(x), self.ln1(x),
                         attn_mask=self.mask[:T, :T], need_weights=False)
        x = x + self.alpha * a
        return x + self.alpha * self.mlp(self.ln2(x))


class GrowGPT(nn.Module):
    def __init__(self, n_init):
        super().__init__()
        self.tok = nn.Embedding(VOCAB, D)
        self.pos = nn.Embedding(CTX, D)
        self.blocks = nn.ModuleList(ReZeroBlock() for _ in range(n_init))
        self.folded = nn.ModuleList()        # dormant blocks, weights conserved
        self.lnf = nn.LayerNorm(D)
        self.head = nn.Linear(D, VOCAB, bias=False)
        self.head.weight = self.tok.weight
        for m in [self.tok, self.pos]:
            nn.init.normal_(m.weight, std=0.02)

    def grow(self):
        """Increase active depth. UNFOLD a previously folded block first -- its
        learned weights are conserved, so earned structure is reused rather than
        recreated from scratch. Only mint a fresh identity block if storage is
        empty. Returns 'unfolded' or 'new' for the log."""
        if len(self.folded) > 0:
            j = len(self.folded) - 1
            b = self.folded[j]
            del self.folded[j]
            b.age = 0                        # must re-earn its place before re-fold
            self.blocks.append(b)
            return "unfolded"
        self.blocks.append(ReZeroBlock().to(self.tok.weight.device))
        return "new"

    def fold(self, idx):
        """FOLD, not prune. A block with |alpha|~0 is within epsilon of the
        identity it was born as, so removing it from the active path is
        function-preserving. Its weights are MOVED to storage, never deleted --
        memory is conserved and the block can be unfolded later. The compute
        path collapses; nothing is forgotten."""
        b = self.blocks[idx]
        del self.blocks[idx]
        self.folded.append(b)

    def forward(self, idx, targets=None):
        T = idx.shape[1]
        x = self.tok(idx) + self.pos(torch.arange(T, device=idx.device))
        for b in self.blocks:
            x = b(x)
        logits = self.head(self.lnf(x))
        loss = None
        if targets is not None:
            loss = F.cross_entropy(logits.view(-1, VOCAB),
                                   targets.reshape(-1))
        return logits, loss


def main():
    if not os.path.exists(DATABIN):
        print("need corpus_tokens.bin (run train_real.py first to pack "
              "the corpus)"); return
    data = np.memmap(DATABIN, dtype=np.uint16, mode="r")
    n_val = min(2_000_000, len(data) // 20)
    train_data, val_data = data[:-n_val], data[-n_val:]

    def batch(src):
        ix = torch.randint(len(src) - CTX - 1, (MICROBS,))
        x = torch.stack([torch.from_numpy(src[i:i + CTX].astype(np.int64))
                         for i in ix])
        y = torch.stack([torch.from_numpy(
            src[i + 1:i + 1 + CTX].astype(np.int64)) for i in ix])
        return x.to(DEV), y.to(DEV)

    model = GrowGPT(INIT_LAYERS).to(DEV)
    opts, blrs = build_opt(model)
    start, best_val, stale = 0, 1e9, 0
    if os.path.exists(CKPT):
        ck = torch.load(CKPT, map_location=DEV)
        while len(model.blocks) < ck["n_layers"]:   # active first (storage empty)
            model.grow()
        while len(model.folded) < ck.get("n_folded", 0):   # then restore storage
            model.folded.append(ReZeroBlock().to(DEV))
        model.load_state_dict(ck["model"])
        opts, blrs = build_opt(model)
        start = ck["step"]; best_val = ck.get("best_val", 1e9)
        print(f"[resume] step {start}, {len(model.blocks)} active layers, "
              f"{len(model.folded)} folded in storage", flush=True)

    def nparams():
        return sum(p.numel() for p in model.parameters())

    @torch.no_grad()
    def evaluate():
        model.eval()
        ls = []
        for _ in range(40):
            x, y = batch(val_data)
            with torch.autocast("cuda", dtype=torch.bfloat16):
                _, l = model(x, y)
            ls.append(l.item())
        model.train()
        return float(np.mean(ls))

    print(f"[grow] start {len(model.blocks)} layers, {nparams()/1e6:.1f}M "
          f"params | cap {MAX_LAYERS} layers | {torch.cuda.get_device_name(0)}",
          flush=True)
    logf = open(LOG, "a")
    t0 = time.time()
    model.train()
    val_hist = []
    last_grow_eval = 0
    n_eval = 0
    MIN_WINDOW_GAIN = float(os.environ.get("CK_MIN_GAIN", "0.03"))
    for step in range(start, MAX_STEPS):
        sc = min(1.0, step / WARMUP) if step < WARMUP else 1.0
        for o, blr in zip(opts, blrs):
            for g in o.param_groups:
                g["lr"] = blr * sc
        for o in opts:
            o.zero_grad(set_to_none=True)
        acc = 0.0
        for _ in range(ACCUM):
            x, y = batch(train_data)
            with torch.autocast("cuda", dtype=torch.bfloat16):
                _, loss = model(x, y)
            (loss / ACCUM).backward()
            acc += loss.item() / ACCUM
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        for o in opts:
            o.step()

        if step % EVAL_EVERY == 0 and step > start:
            for b in model.blocks:
                b.age += 1
            vl = evaluate()
            ppl = math.exp(min(vl, 20))
            alphas = [round(float(b.alpha.abs()), 3) for b in model.blocks]
            event = None
            n_eval += 1
            val_hist.append(vl)
            best_val = min(best_val, vl)

            # FOLD FIRST: fold the unearned before any extension. A block old
            # enough to have learned (age >= MIN_AGE) yet still dead (alpha <
            # ALPHA_DEAD) did no work -> fold it into storage (weights conserved,
            # NOT deleted). Folding has priority over growth so dead depth can
            # never accumulate faster than it is folded away (the bug that piled
            # up 9 dead layers: grow fired ~every 1250 steps, the old prune only
            # every 3000 and one-at-a-time).
            dead = [(float(b.alpha.abs()), i) for i, b in enumerate(model.blocks)
                    if b.age >= MIN_AGE and float(b.alpha.abs()) < ALPHA_DEAD]
            if dead and len(model.blocks) > MIN_LAYERS:
                a_min, i_min = min(dead)
                model.fold(i_min); opts, blrs = build_opt(model)
                event = (f"FOLDED#{i_min}(a={a_min:.3f})->{len(model.blocks)}L "
                         f"active,{len(model.folded)} stored")

            # GROW on DIMINISHING RETURNS -- but ONLY when existing depth is fully
            # earned (no dead block above). If the model cannot use the depth it
            # already has, more depth will not help; let it fold back to the depth
            # it can actually earn, then extend (unfolding stored blocks first).
            elif len(val_hist) > GROW_PATIENCE and \
                    n_eval - last_grow_eval > GROW_PATIENCE and \
                    len(model.blocks) < MAX_LAYERS:
                prev = val_hist[-1 - GROW_PATIENCE]
                gain = (prev - vl) / max(prev, 1e-9)
                if gain < MIN_WINDOW_GAIN:
                    tag = model.grow(); opts, blrs = build_opt(model)
                    last_grow_eval = n_eval
                    verb = "UNFOLDED stored" if tag == "unfolded" else "GREW new"
                    event = (f"{verb}->{len(model.blocks)}L active,"
                             f"{len(model.folded)} stored "
                             f"(gain {gain*100:.1f}%<{MIN_WINDOW_GAIN*100:.0f}%)")

            rec = dict(step=step, val_loss=round(vl, 4), val_ppl=round(ppl, 1),
                       n_layers=len(model.blocks), n_folded=len(model.folded),
                       n_params_M=round(nparams() / 1e6, 1),
                       alphas=alphas, min=round((time.time() - t0) / 60, 1))
            if event:
                rec["event"] = event
            print(f"step {step:>6} | ppl {ppl:6.1f} | {len(model.blocks)}L "
                  f"{nparams()/1e6:.1f}M | a={alphas} "
                  f"{'| '+event if event else ''}", flush=True)
            logf.write(json.dumps(rec) + "\n"); logf.flush()

        if step % CKPT_EVERY == 0 and step > start:
            torch.save({"model": model.state_dict(), "step": step,
                        "n_layers": len(model.blocks),
                        "n_folded": len(model.folded),
                        "best_val": best_val}, CKPT)
    print("[done]", flush=True)


if __name__ == "__main__":
    main()
