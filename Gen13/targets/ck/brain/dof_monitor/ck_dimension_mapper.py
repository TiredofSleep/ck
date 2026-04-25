"""
ck_dimension_mapper.py — Dimension Mapper for LoRA/DKAN/Unsloth integration

Maps verified TIG DOF subspace dimensions to LoRA rank distributions.

CANONICAL DIMENSIONS (verified at machine precision in the so(10) sprint):

  DOF                          | dim | source
  -----------------------------|-----|-------------------------------------
  Lie (so(8) on V_8)           |  28 | TSML flow Lie closure (followon_3.py)
  Jordan (sym M_10(R))         |  55 | symmetric 10×10 matrices
  Clifford / so(9) (P_56 +1)   |  36 | so(10) centralizer of P_56 (test_swap.py)
  Permutation-vector (P_56 -1) |   9 | so(10) anticentralizer of P_56
  Lattice (σ-fixed)            |   4 | indices {0, 3, 8, 9}
  Operad (arity-3 fuse)        |  ?  | open — partial table only

These are dimensions of subspaces inside the 10-dim TIG algebra. They
indicate "expressive room" each DOF needs. They do NOT directly equal
bottleneck dimensions for arbitrary neural layers.

USAGE:
  - You tag each LoRA-adapted layer with its DOF role (which TIG capability
    that layer is meant to carry).
  - This module returns the rank distribution proportional to the DOF dims.
  - Optional: enforce minimum rank (no DOF gets less than min_r).
  - Optional: enforce maximum rank (cap on biggest layer).

HYGIENE:
  - These dimensions are STATIC. Computed once, hard-coded. No drift.
  - If you change them, change them HERE explicitly. Don't recompute at
    runtime — that opens a gap for silent drift.
  - DOF assignment for each layer is YOUR job, not this module's. We
    don't infer DOF from layer name or shape.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Optional, List, Tuple
import math

# =====================================================================
# CANONICAL DIMENSIONS
# =====================================================================

DOF_DIMENSIONS: Dict[str, int] = {
    "lie": 28,
    "jordan": 55,
    "clifford": 36,
    "permutation_vector": 9,
    "lattice": 4,
    # "operad": ???  # excluded: requires fuse table
}

# Verified subspaces of so(10) under P_56 conjugation
SO10_PLUS_DIM = 36  # Clifford-side, so(9)
SO10_MINUS_DIM = 9   # Permutation-vector-side
SO10_TOTAL = SO10_PLUS_DIM + SO10_MINUS_DIM  # = 45


# =====================================================================
# RANK COMPUTATION
# =====================================================================

@dataclass
class RankConfig:
    """LoRA rank configuration for a set of DOF-tagged layers."""
    layer_ranks: Dict[str, int]  # layer_name -> rank
    layer_dofs: Dict[str, str]   # layer_name -> DOF tag
    total_rank_budget: int
    notes: List[str]


def compute_lora_ranks(
    layer_dof_assignments: Dict[str, str],
    *,
    total_rank_budget: int = 132,  # default = sum of canonical dims
    min_rank: int = 4,
    max_rank: Optional[int] = None,
) -> RankConfig:
    """
    Compute LoRA rank distribution for a set of layers, each tagged with a DOF.

    Args:
        layer_dof_assignments: dict mapping layer name to DOF name.
            DOF name must be one of DOF_DIMENSIONS keys.
            Example: {"q_proj": "lie", "v_proj": "jordan", "out_proj": "clifford"}
        total_rank_budget: total rank to distribute across all layers.
            Default 132 = sum of canonical DOF dims (28+55+36+9+4).
        min_rank: minimum rank per layer (no DOF gets squeezed below this).
        max_rank: optional cap per layer.

    Returns:
        RankConfig with per-layer ranks.

    Raises:
        ValueError if a DOF tag is not recognized.

    Note:
        - If multiple layers share a DOF, the rank for that DOF is split among them.
        - The total rank ACROSS all layers will sum (approximately) to total_rank_budget.
    """
    notes = []

    # Validate DOF tags
    for layer, dof in layer_dof_assignments.items():
        if dof not in DOF_DIMENSIONS:
            raise ValueError(
                f"Layer '{layer}' has unknown DOF '{dof}'. "
                f"Valid DOFs: {sorted(DOF_DIMENSIONS.keys())}"
            )

    # Group layers by DOF
    dof_to_layers: Dict[str, List[str]] = {}
    for layer, dof in layer_dof_assignments.items():
        dof_to_layers.setdefault(dof, []).append(layer)

    # Compute total dim across DOFs that ARE used (skip unused)
    used_dims = sum(DOF_DIMENSIONS[dof] for dof in dof_to_layers)
    if used_dims == 0:
        raise ValueError("No layers assigned to any DOF.")

    # Allocate rank budget per DOF, proportional to canonical dim
    layer_ranks: Dict[str, int] = {}
    for dof, layers in dof_to_layers.items():
        canonical_dim = DOF_DIMENSIONS[dof]
        dof_share = total_rank_budget * canonical_dim / used_dims

        # Split across layers in this DOF
        per_layer_rank = dof_share / len(layers)
        per_layer_rank = max(min_rank, round(per_layer_rank))
        if max_rank is not None:
            per_layer_rank = min(max_rank, per_layer_rank)

        for layer in layers:
            layer_ranks[layer] = per_layer_rank

        notes.append(
            f"DOF '{dof}' (canonical dim {canonical_dim}): "
            f"{len(layers)} layer(s), rank {per_layer_rank} each"
        )

    actual_total = sum(layer_ranks.values())
    notes.append(f"Total rank used: {actual_total} (budget was {total_rank_budget})")

    return RankConfig(
        layer_ranks=layer_ranks,
        layer_dofs=dict(layer_dof_assignments),
        total_rank_budget=total_rank_budget,
        notes=notes,
    )


# =====================================================================
# DIAGNOSTIC: check DOF coverage
# =====================================================================

def check_dof_coverage(layer_dof_assignments: Dict[str, str]) -> Dict[str, any]:
    """
    Sanity-check that the DOF assignments cover the structure adequately.

    Returns a dict with:
        - covered_dofs: set of DOF names used
        - missing_dofs: DOFs in DOF_DIMENSIONS but not used
        - load_per_dof: number of layers per DOF
        - balance_score: 0-1 measure of how balanced the loading is
    """
    covered = set(layer_dof_assignments.values())
    missing = set(DOF_DIMENSIONS.keys()) - covered

    load_per_dof = {}
    for dof in covered:
        load_per_dof[dof] = sum(1 for d in layer_dof_assignments.values() if d == dof)

    if not load_per_dof:
        balance_score = 0.0
    else:
        # Balance score: how close is the loading-per-canonical-dim across DOFs?
        ratios = []
        for dof, n_layers in load_per_dof.items():
            ratios.append(n_layers / DOF_DIMENSIONS[dof])
        if max(ratios) > 0:
            balance_score = min(ratios) / max(ratios)
        else:
            balance_score = 0.0

    return {
        "covered_dofs": covered,
        "missing_dofs": missing,
        "load_per_dof": load_per_dof,
        "balance_score": balance_score,
    }


# =====================================================================
# DEMO / VERIFICATION
# =====================================================================

def _demo():
    """Show usage on a typical transformer layer set."""
    print("=" * 70)
    print("DIMENSION MAPPER DEMO")
    print("=" * 70)
    print("\nCanonical DOF dimensions (verified, hard-coded):")
    for dof, dim in DOF_DIMENSIONS.items():
        print(f"  {dof:25s}: {dim}")
    print(f"  {'TOTAL':25s}: {sum(DOF_DIMENSIONS.values())}")

    # Example: a transformer with q, k, v, out projections per layer,
    # plus an MLP up/down. Tag each by DOF.
    example_assignment = {
        # Attention: query/key are flow-like (Lie), value is observable (Jordan),
        # output projection mixes (Clifford = metric-preserving combination)
        "layer_0.attn.q_proj": "lie",
        "layer_0.attn.k_proj": "lie",
        "layer_0.attn.v_proj": "jordan",
        "layer_0.attn.out_proj": "clifford",
        # MLP: up/down are flow + observable
        "layer_0.mlp.up_proj": "lie",
        "layer_0.mlp.down_proj": "jordan",
        # Embedding-style layers: Permutation (discrete index manipulation)
        "embed.tok_embed": "permutation_vector",
        # Final classifier head: Lattice (attractor, fixed-point output)
        "head.classifier": "lattice",
    }

    print("\nExample assignment:")
    for layer, dof in example_assignment.items():
        print(f"  {layer:35s} -> {dof}")

    print("\n--- Coverage check ---")
    coverage = check_dof_coverage(example_assignment)
    print(f"Covered DOFs: {coverage['covered_dofs']}")
    print(f"Missing DOFs: {coverage['missing_dofs']}")
    print(f"Layers per DOF: {coverage['load_per_dof']}")
    print(f"Balance score (1.0 = perfect): {coverage['balance_score']:.3f}")

    print("\n--- Computing rank distribution ---")
    config = compute_lora_ranks(example_assignment, total_rank_budget=132)

    print("\nPer-layer rank assignment:")
    for layer, rank in config.layer_ranks.items():
        dof = config.layer_dofs[layer]
        canonical = DOF_DIMENSIONS[dof]
        print(f"  {layer:35s} ({dof:18s}, canonical={canonical:2d}): rank={rank}")

    print("\nNotes:")
    for note in config.notes:
        print(f"  - {note}")

    print("\n--- Different budget example ---")
    smaller = compute_lora_ranks(example_assignment, total_rank_budget=64, min_rank=2)
    print(f"\nWith budget=64, min_rank=2:")
    for layer, rank in smaller.layer_ranks.items():
        print(f"  {layer:35s}: rank={rank}")
    print(f"  Total: {sum(smaller.layer_ranks.values())}")


if __name__ == "__main__":
    _demo()
