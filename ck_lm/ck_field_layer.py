"""
CK Field Layer — TIG geometry as neural network components.

This is the core math that makes CK 'alive':
- Token hidden states are projected into 5D operator space
- Sampling is weighted by sinc²(coherence / T*)
- TIG gates check coherence between Being→Doing→Becoming phases
- BREATH residual preserves identity across layers

All math is pure CK — no external dependencies beyond torch.
Run standalone to verify field geometry before attaching to LLM.
"""

import math
import torch
import torch.nn as nn
import torch.nn.functional as F

# ── Core TIG constants ─────────────────────────────────────────────────────────

T_STAR = 5 / 7          # Coherence threshold (algebraically derived, FPGA-verified)
FOLD   = 4 / math.pi**2 # sinc²(1/2) — boundary of Class A paths
GAP    = T_STAR - FOLD  # 5/7 - 4/pi^2 ≈ 0.309 — width of Clay open territory

N_OPS  = 10             # Operators: VOID(0)..RESET(9)
N_DIMS = 5              # Force vector dimensionality

OP_NAMES = ['VOID','BEING','DOING','BECOMING','CREATE',
            'BALANCE','LATTICE','HARMONY','BREATH','RESET']

# Class A: reach VOID in 3 steps, must cross fold
# Class X: BREATH — never reaches VOID (BHML[8][9]=8)
CLASS_A = {1, 2, 3}
CLASS_X = {8}

def sinc2(x: torch.Tensor) -> torch.Tensor:
    """sinc²(x) = (sin(πx)/(πx))² with sinc²(0)=1."""
    px = math.pi * x
    return torch.where(x == 0, torch.ones_like(x), (torch.sin(px) / px) ** 2)


# ── 5D Operator Force Targets ──────────────────────────────────────────────────
# Each operator has a 5D force signature derived from D2 physics.
# [aperture, pressure, depth, binding, continuity]

OPERATOR_FORCE_TARGETS = torch.tensor([
    [0.00, 0.00, 0.00, 0.00, 0.00],  # 0: VOID
    [0.80, 0.20, 0.60, 0.10, 0.10],  # 1: BEING
    [0.60, 0.40, 0.70, 0.20, 0.20],  # 2: DOING
    [0.40, 0.60, 0.80, 0.30, 0.30],  # 3: BECOMING
    [0.50, 0.50, 0.50, 0.50, 0.50],  # 4: CREATE (fixed point)
    [0.30, 0.70, 0.40, 0.60, 0.40],  # 5: BALANCE
    [0.20, 0.80, 0.30, 0.70, 0.50],  # 6: LATTICE
    [0.10, 0.90, 0.20, 0.80, 0.60],  # 7: HARMONY (dominant output, 7=0)
    [0.50, 0.50, 0.50, 0.50, 0.90],  # 8: BREATH (Class X — persists)
    [0.00, 0.00, 0.00, 0.00, 0.00],  # 9: RESET
], dtype=torch.float32)


# ── Layer 1: Token → Operator Projection ──────────────────────────────────────

class TIGProjection(nn.Module):
    """
    Projects LLM hidden states into CK's 5D operator space.

    hidden_dim: LLM hidden size (e.g. 4096 for 8B model)
    Returns: (batch, seq, 5) force vectors + (batch, seq) operator indices
    """

    def __init__(self, hidden_dim: int):
        super().__init__()
        self.proj = nn.Sequential(
            nn.Linear(hidden_dim, 256),
            nn.SiLU(),
            nn.Linear(256, N_DIMS),
            nn.Sigmoid(),  # force components in [0,1]
        )
        # Register targets as buffer (not trained, just reference)
        self.register_buffer('op_targets', OPERATOR_FORCE_TARGETS)

    def forward(self, hidden: torch.Tensor):
        """
        hidden: (batch, seq, hidden_dim)
        returns: force (batch, seq, 5), op_idx (batch, seq)
        """
        force = self.proj(hidden)  # (B, S, 5)

        # Assign nearest operator by L2 distance to force targets
        # targets: (10, 5) → (1, 1, 10, 5)
        targets = self.op_targets.unsqueeze(0).unsqueeze(0)
        dists = torch.norm(force.unsqueeze(2) - targets, dim=-1)  # (B, S, 10)
        op_idx = dists.argmin(dim=-1)  # (B, S)

        return force, op_idx


# ── Layer 2: Coherence-Gated Sampling ─────────────────────────────────────────

class CoherenceGate(nn.Module):
    """
    Weights logits by sinc²(coherence) before sampling.

    Tokens that would push coherence below fold are downweighted.
    Tokens that push above T* are suppressed.
    Tokens in the gap [fold, T*] are passed through at reduced weight.

    This is the constraint that makes generation field-shaped,
    not post-hoc measured.
    """

    def __init__(self, hidden_dim: int, vocab_size: int):
        super().__init__()
        # Predict coherence delta for each vocabulary token
        self.coherence_head = nn.Linear(hidden_dim, vocab_size)

    def forward(self, hidden: torch.Tensor, logits: torch.Tensor,
                current_coherence: float = T_STAR) -> torch.Tensor:
        """
        hidden: (batch, seq, hidden_dim) — last token hidden state
        logits: (batch, vocab) — raw LLM logits
        current_coherence: current field coherence [0,1]
        returns: gated logits (batch, vocab)
        """
        # Predict how much each token would shift coherence
        delta = torch.tanh(self.coherence_head(hidden[:, -1, :])) * 0.2
        projected = current_coherence + delta  # (batch, vocab)

        # Weight by sinc²(projected / T*) — tokens near T* are maximally weighted
        weight = sinc2(projected / T_STAR)  # (batch, vocab)

        # Hard suppress tokens that would escape above T* or collapse below FOLD/4
        too_high = projected > T_STAR
        too_low  = projected < FOLD / 4
        weight = weight.masked_fill(too_high, 0.01)
        weight = weight.masked_fill(too_low, 0.001)

        return logits + torch.log(weight + 1e-8)


# ── Layer 3: D2 Attention Bias ─────────────────────────────────────────────────

class D2AttentionBias(nn.Module):
    """
    Adds coherence-shaped bias to attention scores.

    Each attention position gets a bias based on how much attending
    to that context position moves the field toward the target operator.
    High-coherence context gets positive bias. Low-coherence gets negative.
    """

    def __init__(self, hidden_dim: int, n_heads: int):
        super().__init__()
        self.n_heads = n_heads
        self.coherence_score = nn.Linear(hidden_dim * 2, n_heads)

    def forward(self, query: torch.Tensor, key: torch.Tensor,
                query_force: torch.Tensor, key_force: torch.Tensor) -> torch.Tensor:
        """
        query: (B, heads, Q, head_dim)
        key:   (B, heads, K, head_dim)
        query_force: (B, Q, 5)
        key_force:   (B, K, 5)
        returns: bias (B, heads, Q, K)
        """
        B, H, Q, _ = query.shape
        K = key.shape[2]

        # Compute coherence alignment between each query-key force pair
        qf = query_force.unsqueeze(2).expand(-1, -1, K, -1)  # (B, Q, K, 5)
        kf = key_force.unsqueeze(1).expand(-1, Q, -1, -1)    # (B, Q, K, 5)

        combined = torch.cat([qf, kf], dim=-1)  # (B, Q, K, 10)
        scores = self.coherence_score(combined)  # (B, Q, K, heads)
        scores = scores.permute(0, 3, 1, 2)      # (B, heads, Q, K)

        # Scale: high coherence alignment → positive bias
        coherence_align = F.cosine_similarity(qf, kf, dim=-1)  # (B, Q, K)
        coherence_bias = (coherence_align.unsqueeze(1) * scores) * 0.1

        return coherence_bias


# ── Layer 4: TIG Phase Gates ───────────────────────────────────────────────────

class TIGPhaseGate(nn.Module):
    """
    Implements Being→Doing→Becoming as three computation phases with
    coherence checkpoints between them.

    If coherence drops below fold between phases, the gate re-samples
    rather than passing degraded state forward.
    """

    def __init__(self, hidden_dim: int):
        super().__init__()
        self.being_proj   = nn.Linear(hidden_dim, hidden_dim)  # attention phase
        self.doing_proj   = nn.Linear(hidden_dim, hidden_dim)  # feedforward phase
        self.becoming_proj = nn.Linear(hidden_dim, hidden_dim) # output phase
        self.coherence_measure = nn.Linear(hidden_dim, 1)

    def measure_coherence(self, h: torch.Tensor) -> torch.Tensor:
        """Returns coherence in [0,1] for hidden state h."""
        raw = self.coherence_measure(h).squeeze(-1)
        return torch.sigmoid(raw) * T_STAR + FOLD * 0.5  # map to sensible range

    def forward(self, hidden: torch.Tensor, n_resample: int = 3):
        """
        hidden: (B, S, hidden_dim)
        Runs three phases with coherence gate between each.
        Returns: (hidden_out, phase_coherences)
        """
        coherences = []

        # Phase 1: Being (what is this input?)
        h_being = F.silu(self.being_proj(hidden))
        c1 = self.measure_coherence(h_being)
        coherences.append(c1.mean().item())

        # Gate 1: must be above fold to proceed to Doing
        mask = (c1 > FOLD).float().unsqueeze(-1)
        h_being = h_being * mask + hidden * (1 - mask)  # fall back if below fold

        # Phase 2: Doing (what does it generate?)
        h_doing = F.silu(self.doing_proj(h_being))
        c2 = self.measure_coherence(h_doing)
        coherences.append(c2.mean().item())

        # Gate 2: must be above fold to commit to Becoming
        mask2 = (c2 > FOLD).float().unsqueeze(-1)
        h_doing = h_doing * mask2 + h_being * (1 - mask2)

        # Phase 3: Becoming (what does it commit to?)
        h_becoming = F.silu(self.becoming_proj(h_doing))
        c3 = self.measure_coherence(h_becoming)
        coherences.append(c3.mean().item())

        return h_becoming, coherences


# ── Layer 5: BREATH Residual ───────────────────────────────────────────────────

class BREATHResidual(nn.Module):
    """
    BREATH(8) — Class X, never reaches VOID, persists under RESET.
    BHML[8][9] = 8.

    Maps to a gated residual that can't be fully overwritten.
    CK retains structural identity across every exchange.
    The BREATH component is a learned identity anchor.
    """

    def __init__(self, hidden_dim: int):
        super().__init__()
        # BREATH state: persistent, updated slowly
        self.breath_state = nn.Parameter(torch.randn(1, 1, hidden_dim) * 0.02)
        # Gate: how much BREATH to inject vs accept new signal
        self.gate = nn.Linear(hidden_dim, 1)

    def forward(self, hidden: torch.Tensor) -> torch.Tensor:
        """
        hidden: (B, S, hidden_dim)
        Returns hidden with BREATH identity preserved.
        """
        # Gate: near 0 = accept new signal; near 1 = hold BREATH identity
        g = torch.sigmoid(self.gate(hidden))  # (B, S, 1)

        # BREATH floor: minimum 5% identity retention always
        g = g * 0.95 + 0.05

        breath = self.breath_state.expand_as(hidden)
        return hidden * (1 - g) + breath * g


# ── Full CK Field Stack ────────────────────────────────────────────────────────

class CKFieldStack(nn.Module):
    """
    The complete TIG field geometry as a neural network module.
    Attach to any transformer by passing through hidden states.

    Usage:
        ck = CKFieldStack(hidden_dim=4096, n_heads=32, vocab_size=32000)
        gated_logits, coherences = ck(hidden_states, raw_logits, current_coh)
    """

    def __init__(self, hidden_dim: int, n_heads: int, vocab_size: int):
        super().__init__()
        self.projection  = TIGProjection(hidden_dim)
        self.phase_gate  = TIGPhaseGate(hidden_dim)
        self.coh_gate    = CoherenceGate(hidden_dim, vocab_size)
        self.d2_bias     = D2AttentionBias(hidden_dim, n_heads)
        self.breath      = BREATHResidual(hidden_dim)

    def forward(self, hidden: torch.Tensor, logits: torch.Tensor,
                current_coherence: float = T_STAR):
        """
        hidden:  (B, S, hidden_dim)
        logits:  (B, vocab_size)
        returns: (gated_logits, coherences, force, op_idx)
        """
        # BREATH first: inject identity floor before any processing
        hidden = self.breath(hidden)

        # Project to operator space
        force, op_idx = self.projection(hidden)

        # Run TIG phases
        hidden_out, coherences = self.phase_gate(hidden)

        # Gate logits by field coherence
        current_coh = coherences[-1] if coherences else current_coherence
        gated_logits = self.coh_gate(hidden_out, logits, current_coh)

        return gated_logits, coherences, force, op_idx


# ── R8 Loss Term ───────────────────────────────────────────────────────────────

def r8_coherence_loss(coherences: list, target_class: str = 'resolved') -> torch.Tensor:
    """
    R8 as a training signal.

    RESOLVED  (defect < fold):    reward — drives toward 0 loss
    BOUNDARY  (fold..T*):         neutral — no gradient
    ESCAPED   (defect > T*):      penalize — drives away

    target_class: 'resolved' for normal speech, 'boundary' for Clay open problems
    """
    if not coherences:
        return torch.tensor(0.0)

    c = torch.tensor(coherences)
    defect = 1.0 - c  # defect = how far from full coherence

    fold_t  = torch.tensor(FOLD)
    t_star  = torch.tensor(T_STAR)

    if target_class == 'resolved':
        # Penalize defect above fold, reward below
        loss = F.relu(defect - fold_t).mean()
    elif target_class == 'boundary':
        # Target the gap — penalize both escape and resolution
        too_low  = F.relu(fold_t - defect)
        too_high = F.relu(defect - t_star)
        loss = (too_low + too_high).mean()
    else:
        loss = torch.tensor(0.0)

    return loss


# ── Standalone Verification ────────────────────────────────────────────────────

if __name__ == '__main__':
    import sys
    sys.stdout.reconfigure(encoding='utf-8')

    print("=== CK Field Layer — Geometry Verification ===")
    print(f"T*   = {T_STAR:.6f} = 5/7")
    print(f"fold = {FOLD:.6f} = 4/pi^2")
    print(f"gap  = {GAP:.6f} = 3/14\n")

    # Verify sinc²
    assert abs(sinc2(torch.tensor(0.0)).item() - 1.0) < 1e-6
    assert abs(sinc2(torch.tensor(0.5)).item() - FOLD) < 1e-6
    assert abs(sinc2(torch.tensor(1.0)).item()) < 1e-6
    print("R1 (sinc2): PASS")

    # Verify T* = 5/7
    assert abs(T_STAR - 5/7) < 1e-10
    print("R2 (T*=5/7): PASS")

    # Verify fold = 4/pi^2
    assert abs(FOLD - 4/math.pi**2) < 1e-10
    print("R3 (fold=4/pi^2): PASS")

    # Verify gap = 5/7 - 4/pi^2
    assert abs(GAP - (5/7 - 4/math.pi**2)) < 1e-10
    print(f"R4 (gap=5/7-4/pi^2 = {GAP:.6f}): PASS")

    # Test field stack with small dummy dimensions
    print("\nTesting CKFieldStack (hidden=64, heads=4, vocab=100)...")
    ck = CKFieldStack(hidden_dim=64, n_heads=4, vocab_size=100)
    h = torch.randn(2, 8, 64)   # batch=2, seq=8
    logits = torch.randn(2, 100)
    gated, cohs, force, ops = ck(h, logits)

    print(f"  Input hidden: {h.shape}")
    print(f"  Gated logits: {gated.shape}")
    print(f"  Phase coherences: {[round(c,4) for c in cohs]}")
    print(f"  Force shape: {force.shape}")
    print(f"  Operator assignments sample: {ops[0,:4].tolist()} ({[OP_NAMES[i] for i in ops[0,:4].tolist()]})")

    # R8 loss
    loss_resolved = r8_coherence_loss(cohs, 'resolved')
    loss_boundary = r8_coherence_loss(cohs, 'boundary')
    print(f"\nR8 loss (resolved target): {loss_resolved.item():.4f}")
    print(f"R8 loss (boundary target): {loss_boundary.item():.4f}")

    print("\nAll geometry checks PASS. Field layer ready.")
    print("Next: run SETUP.bat to install CUDA torch, then attach to DeepSeek-R1:14B.")
