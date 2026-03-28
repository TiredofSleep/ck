"""Bible Voice — algebraic composition for scripture-grounded conversation."""

from .bible_lattice import (
    BIBLE_LATTICE, MACRO_CHAINS,
    classify_intent, detect_macro_chains,
)
from .composer import BibleVoice
