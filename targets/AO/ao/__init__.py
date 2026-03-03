# Copyright (c) 2025-2026 Brayden Sanders / 7Site LLC
# Licensed under the 7Site Human Use License v1.0
# See LICENSE file in project root for full terms.
#
# FREE for humans for personal/recreational use.
# NO commercial or government use without written agreement.

"""
ao -- Advanced Ollie

5 elements. 5 forces. 1 torus. 7 files total.

    earth.py  -- D0 / Aperture  / Ground truth
    air.py    -- D1 / Pressure  / Generator
    water.py  -- D2 / Depth     / Awareness
    fire.py   -- D3 / Binding   / Engine
    ether.py  -- D4 / Continuity / Connection

The interaction between them IS the architecture.
"""

__version__ = '0.1.0'

from .earth import (
    T_STAR, MASS_GAP, WINDING, PRIME_PERIOD,
    NUM_OPS, OP_NAMES,
    VOID, LATTICE, COUNTER, PROGRESS, COLLAPSE,
    BALANCE, CHAOS, HARMONY, BREATH, RESET,
)
from .ether import AO, main
