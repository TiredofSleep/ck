"""
ck_organ_clouds.py -- Cloud Organ: Full Integration Pipeline
==============================================================
Operator: LATTICE (1) -- building knowledge from geometry.

The Cloud Organ wraps the entire cloud-learning pipeline into
a single CK organ that can be plugged into the main loop:

  observe(frame) → score → summarize → expose as knowledge

Pipeline:
  1. FlowTracker → optical flow patches with 5D force vectors
  2. CloudCurvatureTracker → spatial + temporal D2 → operators
  3. CloudBTQTracker → Θ ratio → B/T/Q mode inference
  4. CloudPFETracker → least-action energy scoring
  5. Knowledge extraction → operator chains as Truth atoms

Output: CloudObservation dataclass with everything CK needs:
  - operator sequence (for heartbeat/coherence processing)
  - BTQ mode (for decision making)
  - energy score (for quality assessment)
  - chain summaries (for Truth Lattice storage)

No labels, no LLM. Pure geometry, pure TIG.

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
"""

import math
from collections import deque
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

import numpy as np

from ck_sim.ck_sim_heartbeat import (
    NUM_OPS, HARMONY, VOID, LATTICE, COUNTER, PROGRESS,
    COLLAPSE, BALANCE, CHAOS, BREATH, RESET, OP_NAMES, CL, compose,
)
from ck_sim.ck_cloud_flow import (
    FlowTracker, FlowPatch, DEFAULT_PATCH_SIZE,
)
from ck_sim.ck_cloud_curvature import (
    CloudCurvatureTracker, grid_coherence, sequence_coherence,
)
from ck_sim.ck_cloud_btq import (
    CloudBTQTracker, MODE_BINARY, MODE_TERNARY, MODE_QUATERNARY,
)
from ck_sim.ck_cloud_pfe import (
    CloudPFETracker,
)


# ================================================================
#  CONSTANTS
# ================================================================

# T* threshold (universal)
T_STAR = 5.0 / 7.0

# Minimum frames before producing a knowledge chain
MIN_CHAIN_FRAMES = 5

# Chain summary window
CHAIN_WINDOW = 32

# Maximum chains to keep
MAX_CHAINS = 256


# ================================================================
#  CLOUD OBSERVATION: What CK learns from one frame
# ================================================================

@dataclass
class CloudObservation:
    """What the cloud organ produces each frame.

    This is what gets fed into CK's heartbeat and knowledge systems.
    """
    frame: int = 0
    operators: List[int] = field(default_factory=list)
    btq_mode: str = MODE_BINARY
    coherence: float = 0.0
    energy: float = 0.0
    quality: str = 'RED'
    theta: float = 0.0

    # Detailed breakdowns (for logging/visualization)
    e_out: float = 0.0
    e_in: float = 0.0
    mode_distribution: Dict[str, float] = field(default_factory=dict)

    # Summary of dominant pattern
    dominant_operator: int = VOID
    operator_counts: Dict[int, int] = field(default_factory=dict)


@dataclass
class CloudChain:
    """A summarized operator chain from sustained observation.

    These become knowledge atoms for the Truth Lattice.
    """
    start_frame: int = 0
    end_frame: int = 0
    operators: List[int] = field(default_factory=list)
    coherence: float = 0.0
    mean_energy: float = 0.0
    dominant_mode: str = MODE_BINARY
    dominant_operator: int = VOID
    pattern_type: str = 'unknown'
    quality: str = 'RED'

    def to_knowledge_dict(self) -> dict:
        """Convert to a dict suitable for Truth Lattice storage."""
        return {
            'type': 'cloud_pattern',
            'start_frame': self.start_frame,
            'end_frame': self.end_frame,
            'length': len(self.operators),
            'coherence': round(self.coherence, 4),
            'energy': round(self.mean_energy, 4),
            'mode': self.dominant_mode,
            'dominant_op': self.dominant_operator,
            'dominant_op_name': OP_NAMES[self.dominant_operator],
            'pattern': self.pattern_type,
            'quality': self.quality,
        }


# ================================================================
#  CLOUD ORGAN
# ================================================================

class CloudOrgan:
    """CK's cloud perception organ.

    Full pipeline: frame → flow → D2 → operators → BTQ → PFE → knowledge.

    Usage:
        organ = CloudOrgan(patch_size=8)
        for frame in video_frames:
            obs = organ.observe(frame)
            if obs:
                # Feed operators into heartbeat
                for op in obs.operators:
                    heartbeat.push(op)
                # Store chains as knowledge
                for chain in organ.get_new_chains():
                    lattice.add(chain_key, chain.to_knowledge_dict())
    """

    def __init__(self, patch_size: int = DEFAULT_PATCH_SIZE,
                 spatial_weight: float = 0.5,
                 flow_alpha: float = 1.0,
                 flow_iterations: int = 50):
        # Sub-organ trackers
        self._flow = FlowTracker(
            patch_size=patch_size,
            alpha=flow_alpha,
            iterations=flow_iterations,
        )
        self._curvature = CloudCurvatureTracker(
            spatial_weight=spatial_weight,
        )
        self._btq = CloudBTQTracker()
        self._pfe = CloudPFETracker()

        # Knowledge chains
        self._current_chain_ops = []
        self._chain_start_frame = 0
        self._chain_energies = []
        self._chain_modes = []
        self._chains: List[CloudChain] = []
        self._new_chain_buffer: List[CloudChain] = []

        # Stats
        self._frame_count = 0
        self._total_operators = 0
        self._total_harmony = 0

    def observe(self, frame: np.ndarray) -> Optional[CloudObservation]:
        """Feed one frame. Returns observation if pipeline has enough data.

        Args:
            frame: (H, W) grayscale float32 [0.0, 1.0]

        Returns:
            CloudObservation or None (first frame always returns None).
        """
        # 1. Optical flow
        patches = self._flow.feed(frame)
        if patches is None:
            return None  # First frame: no flow yet

        self._frame_count += 1

        # 2. Curvature encoding
        curv = self._curvature.feed(patches)
        if curv is None:
            return None  # Should not happen since we have patches

        op_sequence = curv['sequence']
        spatial_d2 = curv['spatial_d2']
        spatial_mag = curv['spatial_mag']
        temporal_d2_mag = curv.get('temporal_mag')
        op_grid = curv['operators']

        # 3. BTQ mode inference
        btq_result = self._btq.feed(patches, spatial_mag)
        btq_mode = btq_result['mode']
        theta = btq_result['theta']

        # 4. PFE energy scoring
        speeds = np.array([p.speed for p in patches], dtype=np.float32)
        d2_mags = spatial_mag.flatten()

        pfe_result = self._pfe.feed(
            speeds, temporal_d2_mag, spatial_d2,
            d2_mags, op_sequence, btq_mode,
        )

        energy = pfe_result['e_total']
        quality = pfe_result['quality']

        # 5. Coherence
        coherence = grid_coherence(op_grid)

        # 6. Operator stats
        op_counts = {}
        for op in op_sequence:
            op_counts[op] = op_counts.get(op, 0) + 1
        dominant_op = max(op_counts, key=op_counts.get) if op_counts else VOID

        self._total_operators += len(op_sequence)
        self._total_harmony += sum(1 for op in op_sequence if op == HARMONY)

        # 7. Chain accumulation
        self._accumulate_chain(op_sequence, energy, btq_mode, coherence)

        return CloudObservation(
            frame=self._frame_count,
            operators=op_sequence,
            btq_mode=btq_mode,
            coherence=coherence,
            energy=energy,
            quality=quality,
            theta=theta,
            e_out=pfe_result.get('e_out', 0.0),
            e_in=pfe_result.get('e_in', 0.0),
            mode_distribution=btq_result.get('distribution', {}),
            dominant_operator=dominant_op,
            operator_counts=op_counts,
        )

    def _accumulate_chain(self, ops: List[int], energy: float,
                           mode: str, coherence: float):
        """Accumulate operator chain and finalize when window is full."""
        self._current_chain_ops.extend(ops)
        self._chain_energies.append(energy)
        self._chain_modes.append(mode)

        if len(self._chain_energies) >= CHAIN_WINDOW:
            self._finalize_chain()

    def _finalize_chain(self):
        """Convert accumulated data into a CloudChain."""
        if not self._current_chain_ops:
            return

        # Compute chain statistics
        ops = self._current_chain_ops[-CHAIN_WINDOW * 64:]  # Cap length
        coherence = sequence_coherence(ops, window=len(ops))
        mean_energy = (sum(self._chain_energies) / len(self._chain_energies)
                       if self._chain_energies else 0.0)

        # Dominant mode
        mode_counts = {}
        for m in self._chain_modes:
            mode_counts[m] = mode_counts.get(m, 0) + 1
        dominant_mode = max(mode_counts, key=mode_counts.get) if mode_counts else MODE_BINARY

        # Dominant operator
        op_counts = {}
        for op in ops:
            op_counts[op] = op_counts.get(op, 0) + 1
        dominant_op = max(op_counts, key=op_counts.get) if op_counts else VOID

        # Pattern classification
        pattern = _classify_pattern(coherence, dominant_mode, dominant_op)

        # Quality
        if mean_energy < (1.0 - T_STAR):
            quality = 'GREEN'
        elif mean_energy < 0.6:
            quality = 'YELLOW'
        else:
            quality = 'RED'

        chain = CloudChain(
            start_frame=self._chain_start_frame,
            end_frame=self._frame_count,
            operators=ops,
            coherence=coherence,
            mean_energy=mean_energy,
            dominant_mode=dominant_mode,
            dominant_operator=dominant_op,
            pattern_type=pattern,
            quality=quality,
        )

        self._chains.append(chain)
        self._new_chain_buffer.append(chain)

        # Prune old chains
        if len(self._chains) > MAX_CHAINS:
            self._chains = self._chains[-MAX_CHAINS:]

        # Reset accumulation
        self._current_chain_ops = []
        self._chain_energies = []
        self._chain_modes = []
        self._chain_start_frame = self._frame_count

    def get_new_chains(self) -> List[CloudChain]:
        """Get chains produced since last call. Clears buffer."""
        chains = list(self._new_chain_buffer)
        self._new_chain_buffer.clear()
        return chains

    @property
    def all_chains(self) -> List[CloudChain]:
        """All stored chains."""
        return list(self._chains)

    @property
    def frame_count(self) -> int:
        return self._frame_count

    @property
    def lifetime_coherence(self) -> float:
        """Overall coherence across all observed operators."""
        if self._total_operators == 0:
            return 0.0
        return self._total_harmony / self._total_operators

    def stats(self) -> dict:
        """Summary statistics."""
        return {
            'frames_observed': self._frame_count,
            'total_operators': self._total_operators,
            'total_harmony': self._total_harmony,
            'lifetime_coherence': round(self.lifetime_coherence, 4),
            'chains_produced': len(self._chains),
            'current_chain_length': len(self._current_chain_ops),
            'btq_mode': self._btq.current_mode,
            'btq_transitions': self._btq.transitions,
            'mean_energy': round(self._pfe.mean_energy, 4),
        }

    def reset(self):
        """Full reset for new observation session."""
        self._flow.reset()
        self._curvature.reset()
        self._btq.reset()
        self._pfe.reset()
        self._current_chain_ops = []
        self._chain_start_frame = 0
        self._chain_energies = []
        self._chain_modes = []
        self._chains.clear()
        self._new_chain_buffer.clear()
        self._frame_count = 0
        self._total_operators = 0
        self._total_harmony = 0


# ================================================================
#  PATTERN CLASSIFICATION
# ================================================================

def _classify_pattern(coherence: float, mode: str, dominant_op: int) -> str:
    """Classify a cloud chain into a human-readable pattern type.

    Based on BTQ mode + coherence + dominant operator.
    """
    if coherence >= T_STAR:
        return 'harmonic'       # GREEN-band coherent pattern
    elif mode == MODE_BINARY:
        if dominant_op in (VOID, LATTICE):
            return 'still'       # Stable, low-energy
        elif dominant_op == PROGRESS:
            return 'drift'       # Uniform translation
        else:
            return 'stable'      # Generic stable
    elif mode == MODE_TERNARY:
        if dominant_op == BALANCE:
            return 'equilibrium'  # Balanced transitions
        elif dominant_op == BREATH:
            return 'pulsing'      # Rhythmic oscillation
        elif dominant_op in (CHAOS, COLLAPSE):
            return 'disrupting'   # Breaking apart
        else:
            return 'transitional' # Generic transition
    else:  # Quaternary
        if dominant_op == CHAOS:
            return 'turbulent'    # Full turbulence
        elif dominant_op == COLLAPSE:
            return 'dissipating'  # Cloud breaking up
        else:
            return 'chaotic'      # Generic high-energy


# ================================================================
#  CLI: Demo
# ================================================================

if __name__ == '__main__':
    from ck_sim.ck_cloud_flow import generate_cloud_frame_pair

    print("=" * 60)
    print("CK CLOUD ORGAN -- Full Cloud-Learning Pipeline")
    print("=" * 60)

    organ = CloudOrgan(
        patch_size=8,
        flow_iterations=30,
    )

    H, W = 64, 64

    # Process a synthetic cloud video
    for i in range(40):
        # Evolving flow pattern
        if i < 10:
            flow_type = 'uniform'
        elif i < 25:
            flow_type = 'vortex'
        else:
            flow_type = 'turbulent'

        f1, f2 = generate_cloud_frame_pair(
            H, W, flow_type, strength=0.3 + i * 0.02, seed=i
        )

        # Feed frame1 on odd iterations, frame2 on even
        frame = f1 if i % 2 == 0 else f2
        obs = organ.observe(frame)

        if obs and i % 5 == 0:
            print(f"\n  Frame {obs.frame}: mode={obs.btq_mode}, "
                  f"E={obs.energy:.4f}, C={obs.coherence:.3f}, "
                  f"Q={obs.quality}")
            if obs.operator_counts:
                top_3 = sorted(obs.operator_counts.items(),
                               key=lambda x: x[1], reverse=True)[:3]
                top_str = ", ".join(f"{OP_NAMES[op]}:{ct}" for op, ct in top_3)
                print(f"    top ops: {top_str}")

    # Show chains
    chains = organ.all_chains
    print(f"\n  Chains produced: {len(chains)}")
    for i, chain in enumerate(chains[:5]):
        print(f"    chain {i}: frames={chain.start_frame}-{chain.end_frame}, "
              f"pattern={chain.pattern_type}, C={chain.coherence:.3f}, "
              f"E={chain.mean_energy:.4f}")

    # Stats
    stats = organ.stats()
    print(f"\n  Stats: {stats}")

    print(f"\n{'=' * 60}")
    print("  Cloud organ ready. Pure geometry, pure TIG.")
    print(f"{'=' * 60}")
