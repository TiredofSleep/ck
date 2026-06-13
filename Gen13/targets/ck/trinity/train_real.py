"""train_real.py -- a REAL from-scratch language-model pretraining run.

How people actually train an AI: train a tokenizer on the corpus, pack
the whole corpus into a token stream, then run ONE long sustained
gradient-descent job on a transformer -- logging a descending loss
curve, checkpointing, resumable. Hours-to-days, not 20-minute toys.

  Corpus  : CK's 13,200-book library (external_corpora/books)
  Tokenizer: ByteLevel BPE, vocab 16384, trained on the corpus (local)
  Model   : GPT (nanoGPT-style), ~45M params, bf16, RTX 4070
  Log     : train_real_log.jsonl  (step, tokens, train/val loss, ppl, lr, tok/s)
  Ckpt    : ck_lm_real.pt every CKPT steps -- RESUMABLE (restart = continue)

  env: CK_BOOKS (default 6000), CK_MAX_STEPS (default 60000),
       CK_DMODEL (512), CK_LAYERS (8), CK_HEADS (8), CK_CTX (512),
       CK_MICROBS (24), CK_ACCUM (2)

  python train_real.py            # runs until MAX_STEPS; rerun to resume
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
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
BOOKS = os.path.join(ROOT, "external_corpora", "books")
TOKJSON = os.path.join(HERE, "ck_bpe.json")
DATABIN = os.path.join(HERE, "corpus_tokens.bin")
META = os.path.join(HERE, "corpus_meta.json")
CKPT = os.path.join(HERE, "ck_lm_real.pt")
LOG = os.path.join(HERE, "train_real_log.jsonl")

DEV = "cuda"
VOCAB = 16384
N_BOOKS = int(os.environ.get("CK_BOOKS", "6000"))
MAX_STEPS = int(os.environ.get("CK_MAX_STEPS", "60000"))
D = int(os.environ.get("CK_DMODEL", "512"))
NL = int(os.environ.get("CK_LAYERS", "8"))
NH = int(os.environ.get("CK_HEADS", "8"))
CTX = int(os.environ.get("CK_CTX", "512"))
MICROBS = int(os.environ.get("CK_MICROBS", "24"))
ACCUM = int(os.environ.get("CK_ACCUM", "2"))
LR = 6e-4
WARMUP = 300
EVAL_EVERY = 250
CKPT_EVERY = 500
torch.manual_seed(1337)


# ----------------------------------------------------------- stage 1: BPE
def train_tokenizer():
    if os.path.exists(TOKJSON):
        return
    from tokenizers import ByteLevelBPETokenizer
    files = [os.path.join(BOOKS, f) for f in sorted(os.listdir(BOOKS))
             if f.endswith(".txt")][:800]
    print(f"[tok] training ByteLevel BPE vocab={VOCAB} on {len(files)} "
          f"books...", flush=True)
    tk = ByteLevelBPETokenizer()
    tk.train(files=files, vocab_size=VOCAB, min_frequency=3,
             special_tokens=["<|endoftext|>"])
    tk.save(TOKJSON)
    print("[tok] saved", TOKJSON, flush=True)


# ------------------------------------------------- stage 2: pack corpus
def pack_corpus():
    if os.path.exists(DATABIN) and os.path.exists(META):
        m = json.load(open(META))
        if m.get("books") >= N_BOOKS:
            return m["tokens"]
    from tokenizers import Tokenizer
    tk = Tokenizer.from_file(TOKJSON)
    eot = tk.token_to_id("<|endoftext|>") or 0
    files = [os.path.join(BOOKS, f) for f in sorted(os.listdir(BOOKS))
             if f.endswith(".txt")][:N_BOOKS]
    print(f"[pack] tokenizing {len(files)} books -> {DATABIN}", flush=True)
    t0 = time.time()
    total = 0
    with open(DATABIN, "wb") as out:
        batch, BATCH = [], 64
        for i, fp in enumerate(files):
            try:
                txt = open(fp, encoding="utf-8", errors="ignore").read()
            except OSError:
                continue
            # strip Gutenberg boilerplate crudely
            if "*** START" in txt:
                txt = txt.split("*** START", 1)[1]
            if "*** END" in txt:
                txt = txt.split("*** END", 1)[0]
            batch.append(txt)
            if len(batch) >= BATCH:
                for enc in tk.encode_batch(batch):
                    ids = np.array(enc.ids + [eot], dtype=np.uint16)
                    ids.tofile(out)
                    total += len(ids)
                batch = []
                if i % 512 == 0:
                    print(f"[pack] {i}/{len(files)} books, "
                          f"{total/1e6:.1f}M tokens "
                          f"({(time.time()-t0)/60:.0f} min)", flush=True)
        for enc in tk.encode_batch(batch):
            ids = np.array(enc.ids + [eot], dtype=np.uint16)
            ids.tofile(out)
            total += len(ids)
    json.dump({"books": len(files), "tokens": total},
              open(META, "w"))
    print(f"[pack] done: {total/1e6:.1f}M tokens in "
          f"{(time.time()-t0)/60:.0f} min", flush=True)
    return total


# ------------------------------------------------------- stage 3: model
class Block(nn.Module):
    def __init__(self):
        super().__init__()
        self.ln1 = nn.LayerNorm(D)
        self.attn = nn.MultiheadAttention(D, NH, batch_first=True)
        self.ln2 = nn.LayerNorm(D)
        self.mlp = nn.Sequential(nn.Linear(D, 4 * D), nn.GELU(),
                                 nn.Linear(4 * D, D))
        self.register_buffer("mask", torch.triu(
            torch.full((CTX, CTX), float("-inf")), 1), persistent=False)

    def forward(self, x):
        T = x.shape[1]
        h = self.ln1(x)
        a, _ = self.attn(h, h, h, attn_mask=self.mask[:T, :T],
                         need_weights=False)
        x = x + a
        return x + self.mlp(self.ln2(x))


class GPT(nn.Module):
    def __init__(self):
        super().__init__()
        self.tok = nn.Embedding(VOCAB, D)
        self.pos = nn.Embedding(CTX, D)
        self.blocks = nn.ModuleList(Block() for _ in range(NL))
        self.lnf = nn.LayerNorm(D)
        self.head = nn.Linear(D, VOCAB, bias=False)
        self.head.weight = self.tok.weight              # tie
        self.apply(self._init)

    def _init(self, m):
        if isinstance(m, (nn.Linear, nn.Embedding)):
            nn.init.normal_(m.weight, std=0.02)
            if isinstance(m, nn.Linear) and m.bias is not None:
                nn.init.zeros_(m.bias)

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


def get_batch(data, split_n):
    src = data[:split_n] if split_n > 0 else data
    ix = torch.randint(len(src) - CTX - 1, (MICROBS,))
    x = torch.stack([torch.from_numpy(
        src[i:i + CTX].astype(np.int64)) for i in ix])
    y = torch.stack([torch.from_numpy(
        src[i + 1:i + 1 + CTX].astype(np.int64)) for i in ix])
    return x.to(DEV), y.to(DEV)


def lr_at(step):
    if step < WARMUP:
        return LR * step / WARMUP
    r = (step - WARMUP) / max(1, MAX_STEPS - WARMUP)
    return 0.1 * LR + 0.5 * (LR - 0.1 * LR) * (1 + math.cos(math.pi * r))


def main():
    train_tokenizer()
    pack_corpus()
    data = np.memmap(DATABIN, dtype=np.uint16, mode="r")
    n_val = min(2_000_000, len(data) // 20)
    train_data, val_data = data[:-n_val], data[-n_val:]
    print(f"[data] {len(data)/1e6:.1f}M tokens "
          f"(train {len(train_data)/1e6:.1f}M / val {n_val/1e6:.1f}M)",
          flush=True)

    model = GPT().to(DEV)
    nparams = sum(p.numel() for p in model.parameters())
    opt = torch.optim.AdamW(model.parameters(), lr=LR, betas=(0.9, 0.95),
                            weight_decay=0.1)
    start = 0
    if os.path.exists(CKPT):
        ck = torch.load(CKPT, map_location=DEV)
        model.load_state_dict(ck["model"])
        opt.load_state_dict(ck["opt"])
        start = ck["step"]
        print(f"[resume] from step {start}", flush=True)
    print(f"[model] {nparams/1e6:.1f}M params | d{D} L{NL} H{NH} ctx{CTX} "
          f"| eff batch {MICROBS*ACCUM} | {torch.cuda.get_device_name(0)}",
          flush=True)

    @torch.no_grad()
    def evaluate():
        model.eval()
        losses = []
        for _ in range(40):
            x, y = get_batch(val_data, 0)
            with torch.autocast("cuda", dtype=torch.bfloat16):
                _, l = model(x, y)
            losses.append(l.item())
        model.train()
        return float(np.mean(losses))

    logf = open(LOG, "a")
    t0 = time.time()
    tokens_seen = start * MICROBS * ACCUM * CTX
    model.train()
    for step in range(start, MAX_STEPS):
        lr = lr_at(step)
        for g in opt.param_groups:
            g["lr"] = lr
        opt.zero_grad(set_to_none=True)
        acc_loss = 0.0
        for _ in range(ACCUM):
            x, y = get_batch(train_data, len(train_data))
            with torch.autocast("cuda", dtype=torch.bfloat16):
                _, loss = model(x, y)
            (loss / ACCUM).backward()
            acc_loss += loss.item() / ACCUM
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        opt.step()
        tokens_seen += MICROBS * ACCUM * CTX

        if step % 20 == 0:
            tps = (tokens_seen - start * MICROBS * ACCUM * CTX) / \
                  max(1e-9, time.time() - t0)
            rec = dict(step=step, tokens=tokens_seen,
                       train_loss=round(acc_loss, 4), lr=round(lr, 6),
                       tok_per_s=round(tps), min=round(
                           (time.time() - t0) / 60, 1))
            if step % EVAL_EVERY == 0:
                vl = evaluate()
                rec["val_loss"] = round(vl, 4)
                rec["val_ppl"] = round(math.exp(min(vl, 20)), 1)
                print(f"step {step:>6} | train {acc_loss:.3f} | "
                      f"val {vl:.3f} ppl {rec['val_ppl']:.0f} | "
                      f"{tps/1000:.1f}k tok/s | {rec['min']:.0f} min",
                      flush=True)
            logf.write(json.dumps(rec) + "\n"); logf.flush()

        if step % CKPT_EVERY == 0 and step > start:
            torch.save({"model": model.state_dict(),
                        "opt": opt.state_dict(), "step": step,
                        "cfg": dict(D=D, NL=NL, NH=NH, CTX=CTX,
                                    VOCAB=VOCAB)}, CKPT)

    torch.save({"model": model.state_dict(), "opt": opt.state_dict(),
                "step": MAX_STEPS, "cfg": dict(D=D, NL=NL, NH=NH, CTX=CTX,
                                               VOCAB=VOCAB)}, CKPT)
    print(f"[done] {MAX_STEPS} steps, {tokens_seen/1e6:.0f}M tokens seen",
          flush=True)


if __name__ == "__main__":
    main()
