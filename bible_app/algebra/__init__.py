"""CK Algebra — standalone finite algebraic system. No OS hooks, no GPU, pure math."""

from .cl_tables import (
    NUM_OPS, VOID, LATTICE, COUNTER, PROGRESS, COLLAPSE,
    BALANCE, CHAOS, HARMONY, BREATH, RESET,
    OP_NAMES, T_STAR, S_STAR, MASS_GAP,
    CL_TSML, CL_BHML, CORNERS, GAPS,
    compose, compose_bhml, mix_lambda, coherence, dominant_op,
)
from .d2_pipeline import (
    D2Pipeline, text_to_force, text_to_ops, text_to_force_and_ops,
    word_triadic_signature, classify_d2, soft_classify_d2,
    cosine_similarity, force_distance, ROOTS_FLOAT,
)
from .corridor import (
    classify_corridor, corridor_tone, classify_with_detail, CORRIDORS,
)
