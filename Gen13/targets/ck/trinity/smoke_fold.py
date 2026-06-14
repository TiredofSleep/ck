"""smoke_fold.py -- verify fold/unfold conserves weights and round-trips through a
checkpoint. CPU-only (CUDA hidden by caller) so it never touches the GPU."""
import torch

import train_grow as G

m = G.GrowGPT(3)
print("start:", len(m.blocks), "active,", len(m.folded), "folded")

# grow twice from empty storage -> both 'new'
assert m.grow() == "new" and m.grow() == "new"
assert len(m.blocks) == 5 and len(m.folded) == 0

# give block 1 a recognizable fingerprint, then fold it
fp = torch.randn_like(m.blocks[1].mlp[0].weight)
m.blocks[1].mlp[0].weight.data.copy_(fp)
saved = m.blocks[1].mlp[0].weight.detach().clone()
m.fold(1)
assert len(m.blocks) == 4 and len(m.folded) == 1, "fold must move, not delete"

# the folded block's weights are CONSERVED in storage (no memory delete)
assert torch.equal(m.folded[0].mlp[0].weight, saved), "folded weights must be intact"

# grow now UNFOLDS the stored block (reuse), restoring its exact weights
tag = m.grow()
assert tag == "unfolded" and len(m.blocks) == 5 and len(m.folded) == 0
assert torch.equal(m.blocks[-1].mlp[0].weight, saved), "unfold must restore weights"
assert m.blocks[-1].age == 0, "unfolded block re-earns its place"
print("fold/unfold conserves weights: OK")

# checkpoint round-trip with a non-empty storage
m.fold(0)  # 4 active, 1 folded
ck = {"model": m.state_dict(), "n_layers": len(m.blocks),
      "n_folded": len(m.folded)}
m2 = G.GrowGPT(3)
while len(m2.blocks) < ck["n_layers"]:
    m2.grow()
while len(m2.folded) < ck["n_folded"]:
    m2.folded.append(G.ReZeroBlock())
m2.load_state_dict(ck["model"])   # strict=True; structures must match exactly
print("checkpoint round-trip (4 active + 1 folded): OK")

# legacy checkpoint (no folded key, no folded.* params) must still load
ck_legacy = {k: v for k, v in m.state_dict().items() if not k.startswith("folded")}
m3 = G.GrowGPT(3)
while len(m3.blocks) < 4:
    m3.grow()
m3.load_state_dict(ck_legacy)   # 0 folded -> empty ModuleList adds no keys
print("legacy (no-folded) checkpoint loads: OK")


# --- momentum preservation across fold (build_opt(prev=...)) ---
def state_of(opts, p):
    for o in opts:
        if p in o.state:
            return o.state[p]
    return None


m4 = G.GrowGPT(4)
opts, _ = G.build_opt(m4)
idx = torch.randint(0, G.VOCAB, (2, 16))
tgt = torch.randint(0, G.VOCAB, (2, 16))
_, loss = m4(idx, tgt)
for o in opts:
    o.zero_grad()
loss.backward()
for o in opts:
    o.step()                                   # populates per-param momentum state
shared = state_of(opts, m4.tok.weight)         # whichever optimizer owns it
active = state_of(opts, m4.blocks[0].mlp[0].weight)
assert shared and active, "params should carry optimizer state after a step"

m4.fold(3)
opts2, _ = G.build_opt(m4, opts)               # rebuild WITH prev -> carry momentum
assert state_of(opts2, m4.tok.weight) is shared, \
    "shared param momentum must persist across fold (same state object)"
assert state_of(opts2, m4.blocks[0].mlp[0].weight) is active, \
    "surviving active block momentum must persist across fold"
opts_cold, _ = G.build_opt(m4)                 # no prev -> the old cold reset
assert state_of(opts_cold, m4.tok.weight) is None, \
    "cold rebuild starts empty (the bug the fix removes)"
print("momentum preserved across fold (cold rebuild loses it): OK")
print("ALL SMOKE TESTS PASSED")
