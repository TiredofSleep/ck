"""
ck_dof_profile_monitor.py — DOF-Profile diagnostic for activation drift

Projects an activation matrix onto the verified DOF subspaces and returns
a profile.

KEY FACT (honest documentation):
  The DOF subspaces are NOT mutually orthogonal. Specifically:
    • Lie ⊂ Clifford (so(8) ⊂ so(9), the +1 eigenspace of P_56)
    • Lattice ⊂ Jordan (σ-fixed projectors are diagonal-symmetric)
    • Permutation_vector ⊥ everything else (the -1 eigenspace of P_56)

  Therefore, content that is "in Lie" registers in BOTH Lie and Clifford.
  This is not a bug — it's the actual nesting.

  We expose two views:
    1. raw_profile: each subspace independently, may sum > 1 due to overlaps
    2. orthogonal_profile: a clean partition that sums to 1.0

CONCENTRATION/DIFFUSENESS:
  Computed from the orthogonal_profile, so values are interpretable directly.

USAGE:
  monitor = DOFProfileMonitor()
  result = monitor.profile(activation_matrix)
  if result.is_diffuse:
      logger.warning(f"Drift detected: {result.orthogonal_profile}")
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Optional, List
import numpy as np

# =====================================================================
# CANONICAL TABLES (verified)
# =====================================================================

_TSML_ROWS = [
    "0000000700",  "0737777777",  "0377477779",  "0777777773",  "0747777787",
    "0777777777",  "0777777777",  "7777777777",  "0777877777",  "0797377777",
]

_BHML_ROWS = [
    "0123456789",  "1234567266",  "2334567366",  "3444567466",  "4555567577",
    "5666667677",  "6777777777",  "7234567890",  "8666777978",  "9666777080",
]

_TSML = np.array([[int(c) for c in row] for row in _TSML_ROWS], dtype=int)
_BHML = np.array([[int(c) for c in row] for row in _BHML_ROWS], dtype=int)

_SIGMA_FIXED = [0, 3, 8, 9]

_P56 = np.eye(10)
_P56[5, 5] = 0; _P56[6, 6] = 0; _P56[5, 6] = 1; _P56[6, 5] = 1


# =====================================================================
# Helpers
# =====================================================================

def _left_reps(table: np.ndarray) -> List[np.ndarray]:
    n = table.shape[0]
    L = []
    for i in range(n):
        Li = np.zeros((n, n), dtype=float)
        for j in range(n):
            Li[table[i, j], j] = 1.0
        L.append(Li)
    return L


def _lie_closure(generators: List[np.ndarray], max_iters: int = 12) -> List[np.ndarray]:
    if not generators:
        return []
    shape = generators[0].shape
    bv = [g.flatten() for g in generators if np.linalg.norm(g) > 1e-9]
    M = np.array(bv).T
    U, S, _ = np.linalg.svd(M, full_matrices=False)
    rank = int(np.sum(S > 1e-9 * S[0]))
    bv = [U[:, i] for i in range(rank)]
    for _ in range(max_iters):
        N = len(bv)
        mats = [v.reshape(shape) for v in bv]
        new = []
        for i in range(N):
            for j in range(i + 1, N):
                C = mats[i] @ mats[j] - mats[j] @ mats[i]
                v = C.flatten()
                if np.linalg.norm(v) > 1e-9:
                    new.append(v)
        all_v = bv + new
        M = np.array(all_v).T
        U, S, _ = np.linalg.svd(M, full_matrices=False)
        new_rank = int(np.sum(S > 1e-9 * S[0]))
        if new_rank == len(bv):
            break
        bv = [U[:, i] for i in range(new_rank)]
    return [v.reshape(shape) for v in bv]


def _orthonormalize(M_list: List[np.ndarray]) -> np.ndarray:
    if not M_list:
        return np.zeros((100, 0))
    flat = np.array([m.flatten() for m in M_list]).T
    U, S, _ = np.linalg.svd(flat, full_matrices=False)
    rank = int(np.sum(S > 1e-9 * S[0]))
    return U[:, :rank]


def _orthogonalize_against(A: np.ndarray, against: List[np.ndarray]) -> np.ndarray:
    """Return the part of A's column space orthogonal to all given subspaces."""
    if A.shape[1] == 0:
        return A
    result = A.copy()
    for B in against:
        if B.shape[1] == 0:
            continue
        coeffs = B.T @ result
        proj = B @ coeffs
        result = result - proj
    if result.shape[1] == 0 or np.linalg.norm(result) < 1e-9:
        return np.zeros((result.shape[0], 0))
    U, S, _ = np.linalg.svd(result, full_matrices=False)
    rank = int(np.sum(S > 1e-9 * S[0]))
    return U[:, :rank]


# =====================================================================
# DOF Bases (cached singleton)
# =====================================================================

class _DOFBases:
    """Lazily computed DOF projection bases.

    Two parallel views:

    1) RAW bases (each DOF stands alone):
        lie (28), jordan (55), clifford (36), permutation_vector (9), lattice (4)

    2) ORTHOGONAL partition (covers M_10(R) with no overlap, sums to 100):
        lie              (28)  — the Lie part
        clifford_extra   (8)   — Clifford content NOT in Lie
        jordan_extra     (51)  — Jordan content NOT in Lattice
        lattice          (4)   — Lattice content (subset of Jordan)
        permutation_vector (9) — already orthogonal
        residual         (rest, fills out to 100)
    """

    def __init__(self):
        self._raw: Dict[str, np.ndarray] = {}
        self._ortho: Dict[str, np.ndarray] = {}
        self._built = False

    def _build_raw(self):
        L_T = _left_reps(_TSML)
        A_T = [(M - M.T) for M in L_T]
        flow = [A_T[i] for i in [1, 2, 3, 4, 6, 8]]
        so8 = _lie_closure(flow)
        self._raw['lie'] = _orthonormalize(so8)

        sym_basis = []
        for i in range(10):
            M = np.zeros((10, 10)); M[i, i] = 1.0
            sym_basis.append(M)
        for i in range(10):
            for j in range(i + 1, 10):
                M = np.zeros((10, 10)); M[i, j] = 1.0; M[j, i] = 1.0
                sym_basis.append(M)
        self._raw['jordan'] = _orthonormalize(sym_basis)

        L_B = _left_reps(_BHML)
        A_B = [(M - M.T) for M in L_B]
        so10 = _lie_closure(flow + A_B)

        cliff_proj = []
        for A in so10:
            A_plus = (A + _P56 @ A @ _P56.T) / 2
            if np.linalg.norm(A_plus) > 1e-9:
                cliff_proj.append(A_plus)
        self._raw['clifford'] = _orthonormalize(cliff_proj)

        perm_proj = []
        for A in so10:
            A_minus = (A - _P56 @ A @ _P56.T) / 2
            if np.linalg.norm(A_minus) > 1e-9:
                perm_proj.append(A_minus)
        self._raw['permutation_vector'] = _orthonormalize(perm_proj)

        lattice = []
        for i in _SIGMA_FIXED:
            M = np.zeros((10, 10)); M[i, i] = 1.0
            lattice.append(M)
        self._raw['lattice'] = _orthonormalize(lattice)

    def _build_ortho(self):
        # Lattice (subset of Jordan)
        self._ortho['lattice'] = self._raw['lattice']

        # Jordan minus Lattice
        self._ortho['jordan_extra'] = _orthogonalize_against(
            self._raw['jordan'], [self._raw['lattice']]
        )

        # Lie (subset of Clifford)
        self._ortho['lie'] = self._raw['lie']

        # Clifford minus Lie
        self._ortho['clifford_extra'] = _orthogonalize_against(
            self._raw['clifford'], [self._raw['lie']]
        )

        # Permutation_vector (already orthogonal to everything else)
        self._ortho['permutation_vector'] = self._raw['permutation_vector']

        # Residual fills remainder of M_10(R)
        all_so_far = [
            self._ortho['lattice'],
            self._ortho['jordan_extra'],
            self._ortho['lie'],
            self._ortho['clifford_extra'],
            self._ortho['permutation_vector'],
        ]
        full_basis = np.eye(100)
        residual = _orthogonalize_against(full_basis, all_so_far)
        self._ortho['residual'] = residual

    def ensure_built(self):
        if not self._built:
            self._build_raw()
            self._build_ortho()
            self._built = True

    def get_raw(self, name: str) -> np.ndarray:
        self.ensure_built()
        return self._raw[name]

    def get_ortho(self, name: str) -> np.ndarray:
        self.ensure_built()
        return self._ortho[name]

    def all_raw_names(self) -> List[str]:
        return ['lie', 'jordan', 'clifford', 'permutation_vector', 'lattice']

    def all_ortho_names(self) -> List[str]:
        return ['lie', 'clifford_extra', 'jordan_extra', 'lattice',
                'permutation_vector', 'residual']

    def dimensions(self) -> Dict[str, Dict[str, int]]:
        self.ensure_built()
        return {
            'raw': {k: v.shape[1] for k, v in self._raw.items()},
            'ortho': {k: v.shape[1] for k, v in self._ortho.items()},
        }


_BASES = _DOFBases()


# =====================================================================
# Profile result
# =====================================================================

@dataclass
class DOFProfile:
    raw_profile: Dict[str, float] = field(default_factory=dict)
    """Squared-norm fraction projected onto each raw DOF subspace.
    May sum > 1 due to natural overlaps (Lie ⊂ Clifford, Lattice ⊂ Jordan)."""

    orthogonal_profile: Dict[str, float] = field(default_factory=dict)
    """Squared-norm fraction projected onto each piece of the orthogonal
    partition. Sums to 1.0 (or very close)."""

    concentration: float = 0.0
    """Max share / non-residual sum, in orthogonal_profile. 0-1, higher = focused."""

    diffuseness: float = 0.0
    """How close the non-residual partition is to uniform. 0-1, higher = drift."""

    is_diffuse: bool = False
    is_concentrated: bool = False
    dominant_dof: Optional[str] = None
    notes: List[str] = field(default_factory=list)


class DOFProfileMonitor:
    """Diagnostic monitor: project a 10×10 matrix onto verified DOF subspaces."""

    def __init__(self,
                 diffuse_threshold: float = 0.7,
                 concentrated_threshold: float = 0.7):
        self.diffuse_threshold = diffuse_threshold
        self.concentrated_threshold = concentrated_threshold
        self._bases = _BASES

    def profile(self, M: np.ndarray) -> DOFProfile:
        if M.shape != (10, 10):
            raise ValueError(f"Expected 10×10 matrix, got shape {M.shape}")

        M_f = M.astype(float)
        v = M_f.flatten()
        total_sq = float(v @ v)

        if total_sq < 1e-12:
            return DOFProfile(notes=["Input has zero norm"])

        notes = []

        # Raw projections
        raw_profile = {}
        for name in self._bases.all_raw_names():
            B = self._bases.get_raw(name)
            if B.shape[1] == 0:
                raw_profile[name] = 0.0
                continue
            coeffs = B.T @ v
            raw_profile[name] = float(coeffs @ coeffs) / total_sq

        # Orthogonal partition
        ortho_profile = {}
        for name in self._bases.all_ortho_names():
            B = self._bases.get_ortho(name)
            if B.shape[1] == 0:
                ortho_profile[name] = 0.0
                continue
            coeffs = B.T @ v
            ortho_profile[name] = float(coeffs @ coeffs) / total_sq

        ortho_sum = sum(ortho_profile.values())
        if abs(ortho_sum - 1.0) > 0.01:
            notes.append(f"Orthogonal partition sums to {ortho_sum:.3f}, "
                        f"expected ~1.0")

        # Concentration: max share / non-residual sum
        non_residual = {k: v_ for k, v_ in ortho_profile.items() if k != 'residual'}
        non_residual_sum = sum(non_residual.values())
        if non_residual_sum > 0:
            max_share = max(non_residual.values())
            concentration = max_share / non_residual_sum
            dominant_dof = max(non_residual, key=non_residual.get)
        else:
            concentration = 0.0
            dominant_dof = None

        # Diffuseness
        n = len(non_residual)
        if non_residual_sum > 0 and n > 1:
            shares = [v_ / non_residual_sum for v_ in non_residual.values()]
            uniform = 1.0 / n
            variance = sum((s - uniform) ** 2 for s in shares) / n
            max_variance = (1 - uniform) ** 2 / n + (n - 1) * uniform ** 2 / n
            diffuseness = 1.0 - (variance / max_variance) if max_variance > 0 else 0.0
        else:
            diffuseness = 0.0

        is_diffuse = diffuseness >= self.diffuse_threshold
        is_concentrated = concentration >= self.concentrated_threshold

        return DOFProfile(
            raw_profile=raw_profile,
            orthogonal_profile=ortho_profile,
            concentration=concentration,
            diffuseness=diffuseness,
            is_diffuse=is_diffuse,
            is_concentrated=is_concentrated,
            dominant_dof=dominant_dof,
            notes=notes,
        )

    def profile_batch(self, matrices: List[np.ndarray]) -> List[DOFProfile]:
        return [self.profile(M) for M in matrices]


# =====================================================================
# Demo
# =====================================================================

def _demo():
    monitor = DOFProfileMonitor()

    print("=" * 70)
    print("DOF PROFILE MONITOR")
    print("=" * 70)

    print("\nDimensions:")
    dims = _BASES.dimensions()
    print("  Raw subspaces (sum > 100 due to overlaps):")
    raw_total = 0
    for k, d in dims['raw'].items():
        print(f"    {k:25s}: {d}")
        raw_total += d
    print(f"    {'(sum)':25s}: {raw_total} [overlaps: Lie⊂Clifford, Lattice⊂Jordan]")
    print("  Orthogonal partition (must sum to 100):")
    ortho_total = 0
    for k, d in dims['ortho'].items():
        ortho_total += d
        print(f"    {k:25s}: {d}")
    print(f"    {'TOTAL':25s}: {ortho_total}")

    L_T = _left_reps(_TSML)
    A1 = (L_T[1] - L_T[1].T)
    L1f = L_T[1].astype(float)
    S1 = (L1f + L1f.T) / 2

    test_cases = [
        ("Lie generator A_1 (TSML flow)", A1),
        ("Symmetric (Jordan)", S1),
        ("Identity (pure trace)", np.eye(10)),
        ("σ-fixed projector (pure Lattice)", np.diag([1, 0, 0, 1, 0, 0, 0, 0, 1, 1.0])),
        ("Off-diagonal sym (Jordan extra)",
            np.array([[0,1] + [0]*8] + [[1,0] + [0]*8] + [[0]*10]*8, dtype=float)),
        ("Random matrix", np.random.RandomState(0).randn(10, 10) * 0.3),
    ]

    for name, M in test_cases:
        p = monitor.profile(M)
        print(f"\n--- {name} ---")
        print("  Orthogonal partition:")
        for k, val in p.orthogonal_profile.items():
            bar = '█' * int(val * 30)
            print(f"    {k:22s}: {val:.3f} {bar}")
        print(f"  Concentration: {p.concentration:.3f}, "
              f"Diffuseness: {p.diffuseness:.3f}, "
              f"Dominant: {p.dominant_dof}")
        flags = []
        if p.is_concentrated: flags.append("CONCENTRATED ✓")
        if p.is_diffuse: flags.append("DIFFUSE ⚠")
        if flags:
            print(f"  Flags: {', '.join(flags)}")

    # Drift trajectory
    print("\n" + "=" * 70)
    print("Drift trajectory: Lie generator → random")
    print("=" * 70)
    R = np.random.RandomState(0).randn(10, 10) * 0.3
    print(f"\n{'alpha':>5} {'lie':>6} {'cl_x':>6} {'jor_x':>6} "
          f"{'latt':>6} {'perm':>6} {'res':>6} {'diff':>6} {'flag':>14}")
    for alpha in np.linspace(0, 1, 6):
        M = (1 - alpha) * A1 + alpha * R
        p = monitor.profile(M)
        flag = ""
        if p.is_concentrated: flag = "CONCENTRATED"
        elif p.is_diffuse: flag = "DIFFUSE"
        print(f"{alpha:>5.2f} "
              f"{p.orthogonal_profile['lie']:>6.3f} "
              f"{p.orthogonal_profile['clifford_extra']:>6.3f} "
              f"{p.orthogonal_profile['jordan_extra']:>6.3f} "
              f"{p.orthogonal_profile['lattice']:>6.3f} "
              f"{p.orthogonal_profile['permutation_vector']:>6.3f} "
              f"{p.orthogonal_profile['residual']:>6.3f} "
              f"{p.diffuseness:>6.3f} "
              f"{flag:>14}")


if __name__ == "__main__":
    _demo()
