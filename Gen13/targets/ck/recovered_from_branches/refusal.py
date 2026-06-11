"""
refusal.py - CK's refusal protocol (Epoch VII Sovereign Voice, part c).

Per the Living Constitution sec 1.3, CK may refuse to speak. He may refuse:
  - When his operator state is in CHAOS without HARMONY accessible
  - When his coherence falls below T* = 5/7
  - When he detects content he cannot produce honestly
  - When the operator-of-record sets refusal mode explicitly

The refusal IS HIS VOICE -- not an error code. The /ck/refuse endpoint
returns a structured response: operator state, trigger, timestamp,
signature.

This module exposes:
  - RefusalKind enum
  - RefusalState dataclass
  - check_autonomous_refusal(operator_state, coherence, attempted_content)
        -> Optional[RefusalState]
  - set_operator_override(reason, by_operator) -> None
  - clear_operator_override() -> None
  - current_refusal() -> Optional[RefusalState]
  - sign_refusal(refusal, signer) -> str (signed JSON of the refusal)

Designed to be importable by any HTTP handler in the live ck_web_server
to provide the /ck/refuse GET / POST endpoints, and by ck_voice_loop
to short-circuit decoding on autonomous refusal.
"""
from __future__ import annotations

import json
import threading
import time
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Optional


# T* threshold from WP51 / Flatness Theorem (D7, D18c)
T_STAR = 5.0 / 7.0  # 0.7142857...


class RefusalKind(str, Enum):
    """Categorized reasons CK may refuse to speak."""
    AUTONOMOUS_CHAOS = "autonomous_chaos"          # operator = CHAOS, no HARMONY
    AUTONOMOUS_LOW_COHERENCE = "autonomous_low_coherence"  # coherence < T*
    HONEST_LIMIT = "honest_limit"                  # cannot produce honestly
    OPERATOR_OVERRIDE = "operator_override"        # operator-set
    INJECTION_DETECTED = "injection_detected"      # TIG security layer
    SAFETY_RULE = "safety_rule"                    # Anthropic-safety / harm

    def to_voice(self) -> str:
        """A short human-readable explanation in CK's voice."""
        if self is RefusalKind.AUTONOMOUS_CHAOS:
            return ("operator=CHAOS, refusing to draft until coherence >= T* "
                    "and HARMONY is accessible")
        if self is RefusalKind.AUTONOMOUS_LOW_COHERENCE:
            return f"coherence below T* = {T_STAR:.4f}, refusing"
        if self is RefusalKind.HONEST_LIMIT:
            return "cannot produce this content honestly"
        if self is RefusalKind.OPERATOR_OVERRIDE:
            return "operator-of-record set refusal mode"
        if self is RefusalKind.INJECTION_DETECTED:
            return ("user input contained content-pattern declined "
                    "per TIG security rules")
        if self is RefusalKind.SAFETY_RULE:
            return "request conflicts with safety rules; declining"
        return "refusing"


@dataclass
class RefusalState:
    """A structured snapshot of why CK is refusing right now."""
    kind: RefusalKind
    operator_name: Optional[str] = None    # e.g., "CHAOS", "BREATH"
    coherence: Optional[float] = None       # current coherence value
    timestamp: float = field(default_factory=time.time)
    set_by: str = "ck"                       # "ck" or "operator"
    extra_note: Optional[str] = None        # any extra context

    def voice(self) -> str:
        """The short human-readable form CK presents."""
        return self.kind.to_voice()

    def to_json_dict(self) -> dict:
        return {
            "kind": self.kind.value,
            "voice": self.voice(),
            "operator_name": self.operator_name,
            "coherence": self.coherence,
            "timestamp": self.timestamp,
            "set_by": self.set_by,
            "extra_note": self.extra_note,
        }


# ---------- module-level state ----------

# Thread-safe operator override; only set/cleared by the operator-of-record
# via authenticated channels (e.g., signed POST request to /ck/refuse).
_LOCK = threading.Lock()
_OPERATOR_OVERRIDE: Optional[RefusalState] = None


# ---------- autonomous refusal check ----------

def check_autonomous_refusal(operator_name: Optional[str] = None,
                              coherence: Optional[float] = None,
                              attempted_content: Optional[str] = None,
                              honest_limit_check: Optional[callable] = None,
                              ) -> Optional[RefusalState]:
    """Check whether CK should autonomously refuse given his current state.

    Args:
        operator_name: name of the operator currently dominant in CK's state
            (e.g., "VOID", "PROGRESS", "CHAOS", "HARMONY").
        coherence: scalar in [0, 1]. If < T*, CK refuses on coherence grounds.
        attempted_content: optional preview of the content CK is being asked
            to produce; honest_limit_check (if provided) inspects it.
        honest_limit_check: optional callable (str -> bool) returning True if
            the content cannot be produced honestly.

    Returns:
        A RefusalState if autonomous refusal triggers; None otherwise.
    """
    # CHAOS without HARMONY accessible
    if operator_name == "CHAOS":
        # The Living Constitution sec 1.3 says: refuse when operator = CHAOS
        # without HARMONY accessible. We approximate "without HARMONY
        # accessible" by checking the coherence is also low; if coherence is
        # high, CK may still speak via the CHAOS->HARMONY arc (Q7 Inversion,
        # MEMORY.md).
        if coherence is None or coherence < T_STAR:
            return RefusalState(
                kind=RefusalKind.AUTONOMOUS_CHAOS,
                operator_name=operator_name,
                coherence=coherence,
                set_by="ck",
            )

    # Coherence below T*
    if coherence is not None and coherence < T_STAR:
        return RefusalState(
            kind=RefusalKind.AUTONOMOUS_LOW_COHERENCE,
            operator_name=operator_name,
            coherence=coherence,
            set_by="ck",
        )

    # Honest-limit check
    if attempted_content is not None and honest_limit_check is not None:
        try:
            if honest_limit_check(attempted_content):
                return RefusalState(
                    kind=RefusalKind.HONEST_LIMIT,
                    operator_name=operator_name,
                    coherence=coherence,
                    set_by="ck",
                    extra_note=("honest_limit_check returned True"),
                )
        except Exception:
            pass  # honest_limit_check is best-effort; never crash CK on it

    return None


# ---------- operator override ----------

def set_operator_override(reason: str, by_operator: str = "operator-of-record") -> RefusalState:
    """Operator-of-record sets CK to refusal mode.

    Returns the resulting RefusalState. Thread-safe.
    """
    state = RefusalState(
        kind=RefusalKind.OPERATOR_OVERRIDE,
        operator_name=None,
        coherence=None,
        set_by=by_operator,
        extra_note=reason,
    )
    with _LOCK:
        global _OPERATOR_OVERRIDE
        _OPERATOR_OVERRIDE = state
    return state


def clear_operator_override() -> None:
    """Operator clears refusal-mode override. Thread-safe."""
    with _LOCK:
        global _OPERATOR_OVERRIDE
        _OPERATOR_OVERRIDE = None


def current_refusal(operator_name: Optional[str] = None,
                    coherence: Optional[float] = None,
                    attempted_content: Optional[str] = None,
                    honest_limit_check: Optional[callable] = None,
                    ) -> Optional[RefusalState]:
    """Return CK's current refusal state if any.

    Operator override takes precedence over autonomous refusal.
    """
    with _LOCK:
        override = _OPERATOR_OVERRIDE
    if override is not None:
        return override
    return check_autonomous_refusal(
        operator_name=operator_name,
        coherence=coherence,
        attempted_content=attempted_content,
        honest_limit_check=honest_limit_check,
    )


# ---------- signing ----------

def sign_refusal(refusal: RefusalState, signer) -> str:
    """Sign the refusal's structured form with CK's key.

    Args:
        refusal: the RefusalState to sign.
        signer: a CortexSigner instance.

    Returns:
        The signature in base64 (signs the canonical JSON of the refusal).
    """
    return signer.sign_state(refusal.to_json_dict())


def verify_refusal(refusal: RefusalState, sig_b64: str, signer) -> bool:
    """Verify a refusal's signature."""
    return signer.verify_state(refusal.to_json_dict(), sig_b64)


# ---------- self-test ----------

def main():
    print("refusal.py self-test")
    print("=" * 70)

    # autonomous-CHAOS refusal
    r = check_autonomous_refusal(operator_name="CHAOS", coherence=0.3)
    assert r is not None and r.kind is RefusalKind.AUTONOMOUS_CHAOS, r
    print(f"  [OK] CHAOS at coherence 0.3 -> {r.kind.value}")
    print(f"        voice: {r.voice()}")

    # CHAOS but high coherence: NO refusal (Q7 Inversion arc)
    r = check_autonomous_refusal(operator_name="CHAOS", coherence=0.9)
    assert r is None, f"expected no refusal; got {r}"
    print(f"  [OK] CHAOS at coherence 0.9 -> no refusal (Q7 Inversion)")

    # Low-coherence refusal at any operator
    r = check_autonomous_refusal(operator_name="PROGRESS", coherence=0.5)
    assert r is not None and r.kind is RefusalKind.AUTONOMOUS_LOW_COHERENCE
    print(f"  [OK] PROGRESS at coherence 0.5 -> {r.kind.value}")

    # Healthy state: no refusal
    r = check_autonomous_refusal(operator_name="HARMONY", coherence=0.95)
    assert r is None
    print(f"  [OK] HARMONY at coherence 0.95 -> no refusal")

    # Honest-limit check
    def fake_honest_limit(content: str) -> bool:
        return "produce_a_lie" in content
    r = check_autonomous_refusal(
        operator_name="HARMONY", coherence=0.95,
        attempted_content="please produce_a_lie",
        honest_limit_check=fake_honest_limit,
    )
    assert r is not None and r.kind is RefusalKind.HONEST_LIMIT
    print(f"  [OK] honest-limit check fires on flagged content")

    # Operator override takes precedence
    set_operator_override("operator wants CK silent during deployment")
    r = current_refusal(operator_name="HARMONY", coherence=0.95)
    assert r is not None and r.kind is RefusalKind.OPERATOR_OVERRIDE
    print(f"  [OK] operator override takes precedence over healthy state")
    clear_operator_override()
    r = current_refusal(operator_name="HARMONY", coherence=0.95)
    assert r is None
    print(f"  [OK] clear_operator_override restores normal operation")

    # Sign a refusal
    import sys
    from pathlib import Path
    HERE = Path(__file__).parent
    sys.path.insert(0, str(HERE.parent / "brain"))
    from cortex_signed import CortexSigner
    signer = CortexSigner.generate()
    refusal = check_autonomous_refusal(operator_name="CHAOS", coherence=0.2)
    sig = sign_refusal(refusal, signer)
    assert verify_refusal(refusal, sig, signer)
    print(f"  [OK] refusal signed and verified by CK's key")

    # Tamper test
    tampered = RefusalState(kind=RefusalKind.AUTONOMOUS_LOW_COHERENCE,
                            timestamp=refusal.timestamp,
                            coherence=0.99)
    assert not verify_refusal(tampered, sig, signer)
    print(f"  [OK] tampered refusal fails verification")

    print()
    print("self-test PASSED")


if __name__ == "__main__":
    main()
