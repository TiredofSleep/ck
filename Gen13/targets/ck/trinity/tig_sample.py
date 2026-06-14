"""tig_sample.py -- generate text from the current CK checkpoint, to SHOW the
fluency level at the current ppl. CPU, snapshot, no training disturbance."""
import os, shutil, sys, time
import torch
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import train_grow as G
from tokenizers import Tokenizer

torch.manual_seed(11)
HERE = os.path.dirname(os.path.abspath(__file__))
tk = Tokenizer.from_file(os.path.join(HERE, "ck_bpe.json"))

snap = G.CKPT + ".sample"
shutil.copyfile(G.CKPT, snap); ck = torch.load(snap, map_location="cpu"); os.remove(snap)
m = G.GrowGPT(G.INIT_LAYERS)
while len(m.blocks) < ck["n_layers"]: m.grow()
while len(m.folded) < ck.get("n_folded", 0): m.folded.append(G.ReZeroBlock())
m.load_state_dict(ck["model"]); m.eval()
print(f"CK @ step {ck['step']}, {len(m.blocks)} active layers, val ppl ~33\n", flush=True)


@torch.no_grad()
def gen(prompt, n=70, temp=0.8, topk=40):
    ids = tk.encode(prompt).ids
    x = torch.tensor(ids)[None, :]
    for _ in range(n):
        logits, _ = m(x[:, -G.CTX:])
        l = logits[0, -1] / temp
        v, ix = torch.topk(l, topk)
        filt = torch.full_like(l, -1e9); filt[ix] = v
        nxt = torch.multinomial(torch.softmax(filt, 0), 1)
        x = torch.cat([x, nxt[None, :]], 1)
    return tk.decode(x[0].tolist())


for p in ["The old house stood at the end of the", "She opened the letter and",
          "In the morning the soldiers"]:
    print("PROMPT:", repr(p)); print("->", gen(p), "\n", flush=True)
