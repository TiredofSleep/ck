"""
ck_russell_codec.py -- Russell Toroidal Geometry Wrapper Codec
===============================================================
Operator: SPIRAL (3) -- Walter Russell's torus maps to TIG operators.

Maps ANY problem's TopologyLens output to 6D Russell toroidal coordinates.
This is a cross-cutting wrapper, not a per-problem codec.

Russell's Toroidal Geometry:
  - Poles = stillness/identity (TIG-1 axial, TIG-2 counter-lattice)
  - Equator = compression/expansion (TIG-4 collapse/expansion)
  - Spirals = motion from pole to equator (TIG-3 spiral vortex)
  - Sheath = harmonic envelope (TIG-7)
  - Center = void (TIG-0)
  - Whole = completed torus (TIG-8)

6D Russell Embedding (Phi_R):
  [divergence, curl, helicity, axial_contrast, imbalance, void_proximity]

delta_R measures how far a problem's I/0 flow deviates from perfect
toroidal symmetry. Used to determine if Russell geometry is:
  - PRIMARY: captures structure standard delta misses
  - DERIVED: correlates strongly with standard delta (redundant but isomorphic)
  - REDUNDANT: adds no information

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import math
from typing import Dict, List, Optional, Tuple

from ck_sim.being.ck_sdv_safety import clamp, safe_div, safe_sqrt, safe_log


# ================================================================
#  RUSSELL-TIG OPERATOR CORRESPONDENCE
# ================================================================

RUSSELL_TIG_MAP = {
    'axial_pole':       1,   # TIG-1: still axis, identity/lattice
    'counter_lattice':  2,   # TIG-2: counter-rotation, duality
    'spiral_vortex':    3,   # TIG-3: spiral motion from pole to equator
    'collapse_expand':  4,   # TIG-4: equatorial compression/expansion
    'harmonic_sheath':  7,   # TIG-7: harmonic envelope/resonance
    'central_void':     0,   # TIG-0: void at center of torus
    'toroidal_whole':   8,   # TIG-8: completed whole
}

# Reverse map: TIG digit -> Russell component
TIG_TO_RUSSELL = {v: k for k, v in RUSSELL_TIG_MAP.items()}


# ================================================================
#  RUSSELL CODEC
# ================================================================

class RussellCodec:
    """Maps TopologyLens output to 6D Russell toroidal coordinates.

    The torus has a natural coordinate system:
      - Axial (poles): where I lives (stillness, identity)
      - Equatorial (belt): where 0 lives (boundary, world-shell)
      - Spiral: how flow connects poles to equator
      - Sheath: harmonic envelope wrapping the whole

    The 6D embedding captures:
      divergence:      Compression/expansion balance (equatorial dynamics)
      curl:            Rotational tendency (spiral motion strength)
      helicity:        Axial spiral threading (pole-to-equator alignment)
      axial_contrast:  Pole asymmetry (I strength vs 0 strength)
      imbalance:       Compression-to-expansion ratio
      void_proximity:  Distance to central void (TIG-0 presence)
    """

    def compute_russell_coords(self, topo_output: dict) -> dict:
        """Map TopologyLens standardized_output to 6D Russell embedding.

        Args:
            topo_output: dict from TopologyLens.standardized_output()

        Returns:
            dict with 6D coords + metadata
        """
        core = topo_output.get('core', {})
        boundary = topo_output.get('boundary', {})
        flow = topo_output.get('flow', {})
        defect = topo_output.get('defect', 0.0)

        core_mag = core.get('magnitude', 0.0)
        boundary_mag = boundary.get('magnitude', 0.0)
        core_feats = core.get('features', [])
        boundary_feats = boundary.get('features', [])

        # ── 1. Divergence: compression/expansion balance ──
        # Core pulling inward (compression) vs boundary pushing outward (expansion)
        # Perfect balance = 0, pure compression = -1, pure expansion = +1
        total_mag = core_mag + boundary_mag
        divergence = clamp(
            safe_div(boundary_mag - core_mag, total_mag + 0.001),
            -1.0, 1.0
        )

        # ── 2. Curl: rotational tendency ──
        # Measures the "twist" in the I->0 flow
        # Use flow alignment as proxy: low alignment = high rotation
        alignment = flow.get('alignment', 0.0)
        curl = clamp(1.0 - abs(alignment), 0.0, 1.0)

        # ── 3. Helicity: axial spiral threading ──
        # How well the spiral connects pole to equator
        # High helicity = smooth spiral, low = disconnected
        diff_mag = flow.get('difference_magnitude', 0.0)
        direction = flow.get('direction', 0.0)
        # Helicity is the product of magnitude and directional coherence
        helicity = clamp(diff_mag * abs(direction), 0.0, 10.0) / 10.0

        # ── 4. Axial contrast: pole asymmetry ──
        # How different the two poles (I) are from each other
        # In Russell's torus: north pole = compression start, south = expansion start
        if core_feats:
            n = len(core_feats)
            mid = n // 2
            upper = sum(core_feats[:max(mid, 1)]) / max(mid, 1)
            lower = sum(core_feats[mid:]) / max(n - mid, 1) if mid < n else upper
            axial_contrast = clamp(abs(upper - lower), 0.0, 1.0)
        else:
            axial_contrast = 0.0

        # ── 5. Imbalance: compression-to-expansion ratio ──
        # Perfect toroidal symmetry = balanced compression and expansion
        # The defect itself measures this: high defect = high imbalance
        imbalance = clamp(defect, 0.0, 1.0)

        # ── 6. Void proximity: distance to central void (TIG-0) ──
        # The center of the torus is pure void -- no information, no topology
        # Proximity to void = how close to total coherence collapse
        # Low core+boundary magnitude = close to void
        void_proximity = clamp(
            1.0 - safe_div(total_mag, 3.0, default=1.0),
            0.0, 1.0
        )

        return {
            'divergence': divergence,
            'curl': curl,
            'helicity': helicity,
            'axial_contrast': axial_contrast,
            'imbalance': imbalance,
            'void_proximity': void_proximity,
        }

    def coords_to_vector(self, coords: dict) -> List[float]:
        """Convert Russell coords dict to a 6D vector."""
        return [
            coords['divergence'],
            coords['curl'],
            coords['helicity'],
            coords['axial_contrast'],
            coords['imbalance'],
            coords['void_proximity'],
        ]

    def delta_russell(self, coords: dict) -> float:
        """Russell defect: measures toroidal imbalance.

        Perfect toroidal symmetry:
          - divergence = 0 (balanced compression/expansion)
          - curl moderate (spiral flow present but not dominant)
          - helicity moderate (connected spiral)
          - axial_contrast = 0 (symmetric poles)
          - imbalance = 0 (standard delta = 0)
          - void_proximity low (not collapsed)

        delta_R = weighted deviation from toroidal ideal.
        """
        div_dev = abs(coords['divergence'])  # Should be 0
        curl_dev = abs(coords['curl'] - 0.5) * 2.0  # Should be moderate
        hel_dev = abs(coords['helicity'] - 0.5) * 2.0  # Should be moderate
        axial_dev = coords['axial_contrast']  # Should be 0
        imb_dev = coords['imbalance']  # Should be 0
        void_dev = coords['void_proximity']  # Should be low

        # Weighted combination (TIG operator weights)
        # Heavier weight on imbalance (the actual defect) and divergence
        delta_r = (
            0.25 * div_dev +
            0.10 * curl_dev +
            0.10 * hel_dev +
            0.15 * axial_dev +
            0.25 * imb_dev +
            0.15 * void_dev
        )
        return clamp(delta_r, 0.0, 1.0)

    def russell_tig_signature(self, coords: dict) -> List[int]:
        """Map Russell coordinates to TIG operator signature.

        Returns the dominant TIG operators activated by this configuration.
        """
        signature = []

        # Void proximity high -> TIG-0
        if coords['void_proximity'] > 0.7:
            signature.append(0)

        # Axial contrast high -> TIG-1 (axial pole)
        if coords['axial_contrast'] > 0.3:
            signature.append(1)

        # Divergence significant -> TIG-2 (counter-lattice duality)
        if abs(coords['divergence']) > 0.3:
            signature.append(2)

        # Curl high -> TIG-3 (spiral)
        if coords['curl'] > 0.5:
            signature.append(3)

        # Imbalance high -> TIG-4 (collapse/expansion)
        if coords['imbalance'] > 0.3:
            signature.append(4)

        # Helicity moderate + curl moderate -> TIG-7 (harmonic sheath)
        if 0.2 < coords['helicity'] < 0.8 and 0.2 < coords['curl'] < 0.8:
            signature.append(7)

        # Low delta overall -> TIG-8 (toroidal whole = HARMONY)
        if self.delta_russell(coords) < 0.2:
            signature.append(8)

        return signature if signature else [0]  # Default to void

    def classify_russell(self, delta_r: float, delta_standard: float,
                         correlation: float = 0.0) -> str:
        """Determine Russell geometry's relationship to standard delta.

        Args:
            delta_r: Russell toroidal defect
            delta_standard: Standard spectrometer defect
            correlation: Pearson correlation between delta_R and delta_standard
                        across multiple seeds (0.0 if not computed)

        Returns:
            'primary':   delta_R captures structure delta_standard misses
            'derived':   delta_R correlates strongly (isomorphic view)
            'redundant': delta_R adds no information
        """
        # If correlation is available, use it directly
        if abs(correlation) > 0.0:
            if abs(correlation) > 0.85:
                return 'derived'
            elif abs(correlation) < 0.3:
                if abs(delta_r - delta_standard) > 0.15:
                    return 'primary'
                return 'redundant'
            else:
                return 'derived'  # Moderate correlation = related but not identical

        # Fallback: compare single-point values
        diff = abs(delta_r - delta_standard)
        if diff < 0.05:
            return 'derived'  # Very similar -> likely redundant/derived
        elif delta_r > delta_standard + 0.15:
            return 'primary'  # Russell sees more defect -> captures something new
        elif delta_r < delta_standard - 0.15:
            return 'primary'  # Russell sees less defect -> different perspective
        else:
            return 'derived'

    def full_analysis(self, topo_output: dict) -> dict:
        """Complete Russell analysis of a TopologyLens output.

        Returns everything needed for the Russell section of the meta-lens report.
        """
        coords = self.compute_russell_coords(topo_output)
        delta_r = self.delta_russell(coords)
        delta_std = topo_output.get('defect', 0.0)
        classification = self.classify_russell(delta_r, delta_std)
        tig_sig = self.russell_tig_signature(coords)

        return {
            'problem_id': topo_output.get('problem_id', 'unknown'),
            'coords': coords,
            'coords_vector': self.coords_to_vector(coords),
            'delta_russell': delta_r,
            'delta_standard': delta_std,
            'delta_difference': abs(delta_r - delta_std),
            'classification': classification,
            'tig_signature': tig_sig,
            'tig_signature_names': [TIG_TO_RUSSELL.get(t, f'tig_{t}') for t in tig_sig],
        }


# ================================================================
#  CORRELATION HELPER (for multi-seed classification)
# ================================================================

def compute_russell_correlation(delta_rs: List[float],
                                 delta_stds: List[float]) -> float:
    """Pearson correlation between Russell and standard deltas.

    Used for the classify_russell determination across multiple seeds.
    """
    n = len(delta_rs)
    if n < 3:
        return 0.0

    mean_r = sum(delta_rs) / n
    mean_s = sum(delta_stds) / n

    cov = sum((delta_rs[i] - mean_r) * (delta_stds[i] - mean_s) for i in range(n))
    var_r = sum((delta_rs[i] - mean_r) ** 2 for i in range(n))
    var_s = sum((delta_stds[i] - mean_s) ** 2 for i in range(n))

    denom = safe_sqrt(var_r) * safe_sqrt(var_s)
    return safe_div(cov, denom, default=0.0)
