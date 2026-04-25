"""
ck_viz_trail.py — Descent Signature Visualization

Three-panel visualization for IHÉS demonstration:

  Panel 1: TRAIL TRACE
    2D PCA of the trail (depth 0..6).
    Shows where the input starts and where it descends to.
    Each input gets its own colored line.

  Panel 2: VECTOR-DOF HEATMAP  
    For each trail step, fraction of mass on:
      - σ-fixed indices {0, 3, 8, 9}  (VOID, PROGRESS, BREATH, RESET)
      - 6-cycle indices {1, 2, 4, 5, 6, 7}
      - HARMONY index {7}
      - VOID index {0}
    These are vector-level partitions, NOT the matrix-level DOFs from 
    DOFProfileMonitor (which require sym/antisym content that distributions
    don't have).

  Panel 3: SIGNATURE SUMMARY
    [H_0, half_life, asymp, peak_disp] — the 4D compact signature.

DESIGN NOTES:
  - Default depth = 6 (not 20). Past depth 5 the trail is at attractor.
  - Default α = 0.5 (verified optimal mix).
  - PCA fitted on a reference set of trails for stable axes across queries.
  - All numbers shown are direct measurements, not interpretations.

USAGE:
  from ck_viz_trail import visualize_query
  fig = visualize_query("I want to be more patient", reference_set=DEFAULT_REFS)
  fig.savefig("descent.png")

  # For interactive comparison
  from ck_viz_trail import compare_queries
  fig = compare_queries(["harmony", "conflict", "stillness"])
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

from encoder_v1 import encode, encode_with_explanation


# ============================================================
# CK lattice processor (inline)
# ============================================================

TSML_ROWS = ["0000000700","0737777777","0377477779","0777777773","0747777787",
             "0777777777","0777777777","7777777777","0777877777","0797377777"]
TSML = np.array([[int(c) for c in row] for row in TSML_ROWS], dtype=float)

BHML_ROWS = ["0123456789","1234567266","2334567366","3444567466","4555567577",
             "5666667677","6777777777","7234567890","8666777978","9666777080"]
BHML = np.array([[int(c) for c in row] for row in BHML_ROWS], dtype=float)

OP_NAMES = ['VOID', 'LATTICE', 'COUNTER', 'PROGRESS', 'COLLAPSE',
            'BALANCE', 'CHAOS', 'HARMONY', 'BREATH', 'RESET']

SIGMA_FIXED = [0, 3, 8, 9]
SIX_CYCLE = [1, 2, 4, 5, 6, 7]


def fuse(p, q, table):
    r = np.zeros(10)
    for a in range(10):
        for b in range(10):
            r[int(table[a, b])] += p[a] * q[b]
    return r


def normalize_l1(v):
    s = v.sum()
    return v / s if s > 1e-12 else v


def entropy(p, eps=1e-12):
    return -np.sum(p[p > eps] * np.log(p[p > eps]))


def ck_process(p_init, depth=6, alpha=0.5):
    p = normalize_l1(np.asarray(p_init, dtype=float))
    trail = [p.copy()]
    for _ in range(depth):
        p_t = normalize_l1(fuse(p, p, table=TSML))
        p_b = normalize_l1(fuse(p, p, table=BHML))
        p = normalize_l1(alpha * p_t + (1 - alpha) * p_b)
        trail.append(p.copy())
    return trail


def trail_signature(trail):
    H_seq = [entropy(p) for p in trail]
    H_0 = H_seq[0]
    target = H_0 / 2
    half_life = next((d for d, h in enumerate(H_seq) if h < target), len(H_seq))
    asymp = H_seq[-1]
    monotonic = np.minimum.accumulate(H_seq)
    peak_disp = float(np.max(np.array(H_seq) - monotonic))
    return [H_0, float(half_life), asymp, peak_disp]


# ============================================================
# Vector-level DOF projection (CORRECTED from matrix-level DOFs)
# ============================================================

def vector_dof_profile(p):
    """
    Vector-level partition of distribution mass.
    
    Returns dict with mass on:
      - sigma_fixed: {0, 3, 8, 9}
      - six_cycle:   {1, 2, 4, 5, 6, 7}
      - void:        {0}
      - harmony:     {7}
      - breath:      {8}
      - reset:       {9}
    
    These are direct measurements on the distribution, not 10x10 matrix DOF
    projections (which require sym/antisym content distributions don't have).
    """
    return {
        'sigma_fixed': float(sum(p[i] for i in SIGMA_FIXED)),
        'six_cycle':   float(sum(p[i] for i in SIX_CYCLE)),
        'void':        float(p[0]),
        'harmony':     float(p[7]),
        'breath':      float(p[8]),
        'reset':       float(p[9]),
    }


# ============================================================
# Visualization
# ============================================================

def visualize_query(text, reference_set=None, depth=6, alpha=0.5,
                    save_path=None, title=None):
    """
    Three-panel visualization of how text descends through CK's lattice.
    
    Args:
        text: input string
        reference_set: list of texts to fit PCA axes (for stable cross-query axes)
                       If None, uses just this query (axes only meaningful for one query)
        depth: number of fuse iterations (default 6 — past attractor)
        alpha: T/B mix coefficient (default 0.5 — verified optimal)
        save_path: where to save the figure (None = don't save)
        title: figure title (default = the text)
    
    Returns:
        matplotlib figure
    """
    # Encode and process
    enc = encode_with_explanation(text)
    p_0 = enc['distribution']
    trail = ck_process(p_0, depth=depth, alpha=alpha)
    sig = trail_signature(trail)
    
    # Fit PCA on reference set for stable axes
    if reference_set is None:
        # Use this query's trail itself (axes only meaningful for one query)
        all_states = np.array(trail)
    else:
        all_states_list = [trail]
        for ref_text in reference_set:
            ref_p = encode(ref_text)
            ref_trail = ck_process(ref_p, depth=depth, alpha=alpha)
            all_states_list.append(ref_trail)
        all_states = np.vstack([np.array(t) for t in all_states_list])
    
    # Center and PCA
    mean = all_states.mean(axis=0)
    centered = all_states - mean
    U, S, Vt = np.linalg.svd(centered, full_matrices=False)
    pc1, pc2 = Vt[0], Vt[1]
    
    # Project trail to 2D
    trail_arr = np.array(trail)
    trail_centered = trail_arr - mean
    trail_2d = np.column_stack([trail_centered @ pc1, trail_centered @ pc2])
    
    # ============================================================
    # Build figure
    # ============================================================
    fig = plt.figure(figsize=(15, 5))
    gs = GridSpec(1, 3, figure=fig, width_ratios=[1.2, 1.2, 0.6])
    
    ax_trail = fig.add_subplot(gs[0])
    ax_dof   = fig.add_subplot(gs[1])
    ax_sig   = fig.add_subplot(gs[2])
    
    # ============================================================
    # Panel 1: Trail trace in 2D PCA
    # ============================================================
    ax_trail.plot(trail_2d[:, 0], trail_2d[:, 1], 'o-', color='steelblue',
                  linewidth=1.5, markersize=8, alpha=0.8)
    
    # Mark depth labels
    for d, (x, y) in enumerate(trail_2d):
        ax_trail.annotate(f'd={d}', (x, y), textcoords='offset points',
                          xytext=(8, 8), fontsize=9, color='darkblue')
    
    # Mark start and end specially
    ax_trail.plot(trail_2d[0, 0], trail_2d[0, 1], 'go', markersize=14,
                  label='input', zorder=5)
    ax_trail.plot(trail_2d[-1, 0], trail_2d[-1, 1], 'r*', markersize=18,
                  label='attractor', zorder=5)
    
    ax_trail.set_xlabel(f'PC1 ({S[0]/S.sum()*100:.0f}% var)')
    ax_trail.set_ylabel(f'PC2 ({S[1]/S.sum()*100:.0f}% var)')
    ax_trail.set_title('Trail Trace (PCA)', fontsize=11, fontweight='bold')
    ax_trail.legend(loc='best', fontsize=9)
    ax_trail.grid(True, alpha=0.3)
    
    # ============================================================
    # Panel 2: Vector-DOF heatmap
    # ============================================================
    dof_names = ['sigma_fixed', 'six_cycle', 'void', 'harmony', 'breath', 'reset']
    dof_labels = ['σ-fixed\n{0,3,8,9}', '6-cycle\n{1,2,4,5,6,7}',
                  'VOID\n{0}', 'HARMONY\n{7}', 'BREATH\n{8}', 'RESET\n{9}']
    
    dof_matrix = np.zeros((len(dof_names), depth + 1))
    for d, p in enumerate(trail):
        prof = vector_dof_profile(p)
        for i, name in enumerate(dof_names):
            dof_matrix[i, d] = prof[name]
    
    im = ax_dof.imshow(dof_matrix, aspect='auto', cmap='viridis',
                       vmin=0, vmax=1, origin='lower')
    ax_dof.set_yticks(range(len(dof_names)))
    ax_dof.set_yticklabels(dof_labels, fontsize=8)
    ax_dof.set_xticks(range(depth + 1))
    ax_dof.set_xticklabels([f'd={d}' for d in range(depth + 1)])
    ax_dof.set_title('Vector-DOF Mass Distribution', fontsize=11, fontweight='bold')
    
    # Annotate cells
    for i in range(len(dof_names)):
        for d in range(depth + 1):
            val = dof_matrix[i, d]
            color = 'white' if val < 0.5 else 'black'
            ax_dof.text(d, i, f'{val:.2f}', ha='center', va='center',
                        fontsize=7, color=color)
    
    plt.colorbar(im, ax=ax_dof, fraction=0.046, pad=0.04)
    
    # ============================================================
    # Panel 3: Signature summary
    # ============================================================
    ax_sig.axis('off')
    
    text_top = enc['top_operators']
    
    summary = f"""
INPUT
{text!r}

ENCODER
Tokens: {len(enc['tokens'])}
Coverage: {enc['coverage']*100:.0f}%
Top: {text_top[0][0]} ({text_top[0][1]:.2f})
     {text_top[1][0]} ({text_top[1][1]:.2f})
     {text_top[2][0]} ({text_top[2][1]:.2f})

DESCENT SIGNATURE
H_0       = {sig[0]:.3f}
half_life = {int(sig[1])}
asymp     = {sig[2]:.3f}
peak_disp = {sig[3]:.3f}

PIPELINE
depth = {depth}
α     = {alpha} (T+B mix)
"""
    ax_sig.text(0.05, 0.5, summary, fontsize=9, family='monospace',
                verticalalignment='center', transform=ax_sig.transAxes)
    
    # ============================================================
    # Title
    # ============================================================
    fig.suptitle(title or f'Descent Signature: {text!r}',
                 fontsize=12, fontweight='bold', y=1.02)
    
    fig.tight_layout()
    
    if save_path:
        fig.savefig(save_path, dpi=120, bbox_inches='tight')
    
    return fig


def compare_queries(texts, depth=6, alpha=0.5, save_path=None):
    """
    Compare multiple queries' trails on a shared 2D plot.
    Shows how semantically different inputs descend differently.
    """
    # Get all trails
    trails = [ck_process(encode(t), depth=depth, alpha=alpha) for t in texts]
    
    # Fit PCA on combined data
    all_states = np.vstack([np.array(t) for t in trails])
    mean = all_states.mean(axis=0)
    centered = all_states - mean
    U, S, Vt = np.linalg.svd(centered, full_matrices=False)
    pc1, pc2 = Vt[0], Vt[1]
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    colors = plt.cm.tab10(np.linspace(0, 1, len(texts)))
    
    for text, trail, color in zip(texts, trails, colors):
        trail_arr = np.array(trail)
        trail_2d = (trail_arr - mean) @ np.column_stack([pc1, pc2])
        
        ax.plot(trail_2d[:, 0], trail_2d[:, 1], 'o-', color=color,
                linewidth=1.5, markersize=8, alpha=0.7,
                label=text[:30] + ('...' if len(text) > 30 else ''))
        ax.plot(trail_2d[0, 0], trail_2d[0, 1], 'o', color=color,
                markersize=14, markeredgecolor='black', markeredgewidth=2)
        ax.plot(trail_2d[-1, 0], trail_2d[-1, 1], '*', color=color,
                markersize=20, markeredgecolor='black', markeredgewidth=1)
    
    ax.set_xlabel(f'PC1 ({S[0]/S.sum()*100:.0f}% var)')
    ax.set_ylabel(f'PC2 ({S[1]/S.sum()*100:.0f}% var)')
    ax.set_title('Compared Descent Trails — large dot = input, star = attractor',
                 fontsize=12, fontweight='bold')
    ax.legend(loc='best', fontsize=9)
    ax.grid(True, alpha=0.3)
    
    fig.tight_layout()
    
    if save_path:
        fig.savefig(save_path, dpi=120, bbox_inches='tight')
    
    return fig


# ============================================================
# Self-test demonstration
# ============================================================

if __name__ == "__main__":
    import os
    os.makedirs('/mnt/user-data/outputs/viz', exist_ok=True)
    
    # Reference set for stable PCA axes
    references = [
        "patience and persistence",
        "harmony and gentleness",
        "structure and order",
        "chaos and turbulence",
        "reset and renewal",
        "void and silence",
    ]
    
    # Single-query demo
    print("Generating single-query visualizations...")
    queries = [
        "I need patience to endure",
        "Find peace and stillness",
        "Build a strong framework",
        "Reset everything fresh",
    ]
    
    for i, q in enumerate(queries):
        fig = visualize_query(q, reference_set=references,
                              save_path=f'/mnt/user-data/outputs/viz/single_{i}.png')
        plt.close(fig)
        print(f"  Saved: single_{i}.png — {q!r}")
    
    # Comparison demo
    print("\nGenerating comparison visualization...")
    fig = compare_queries(queries,
                          save_path='/mnt/user-data/outputs/viz/comparison.png')
    plt.close(fig)
    print(f"  Saved: comparison.png")
    
    # Contrastive demo (semantically different)
    print("\nGenerating contrastive demo...")
    contrastive = [
        "harmony peace love together",
        "chaos storm conflict turbulence",
        "patience endure persist",
    ]
    fig = compare_queries(contrastive,
                          save_path='/mnt/user-data/outputs/viz/contrastive.png')
    plt.close(fig)
    print(f"  Saved: contrastive.png")
    
    print("\n✓ All visualizations generated.")
