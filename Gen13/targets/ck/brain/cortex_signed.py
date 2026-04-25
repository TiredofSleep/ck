"""
cortex_signed.py - Ed25519 signing layer for CK's persisted cortex state.

Implements Epoch III (Persistent Selfhood) of the AI Sovereignty Plan
(Gen13/AI_SOVEREIGNTY_PLAN.md, sec EPOCH III, lines 230-298).

What this provides:
    - Ed25519 keypair management (generate, load, persist)
    - canonicalized SHA-256 hashing of cortex state
    - sign(state_dict) -> signature (64 bytes, base64-encoded)
    - verify(state_dict, signature) -> bool
    - signed journal: append-only JSONL with one line per Hebbian update

Invariants:
    - Private key NEVER leaves Gen13/var/identity/ck_privkey.pem
    - Public key is freely shareable; goes in Gen13/var/identity/ck_pubkey.pem
    - Both files are gitignored (keypair must be generated per-deployment)
    - Each cortex state file has an accompanying .sig file with its signature
    - The journal file (cortex_journal.jsonl) is append-only and signed per line

Usage:
    from cortex_signed import CortexSigner

    signer = CortexSigner.load_or_generate()
    state = {"tick": 100, "W": [[...]], "d_now": ..., "d_prev": ...}
    sig_b64 = signer.sign_state(state)
    assert signer.verify_state(state, sig_b64) is True

    # Append to journal
    signer.append_journal(tick=100, d_now=..., d_prev=..., W_norm=4.2)

    # Replay verification
    entries = signer.read_journal()
    assert all(signer.verify_journal_entry(e) for e in entries)
"""
from __future__ import annotations

import base64
import hashlib
import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, List, Optional, Union

# cryptography is required; install via `pip install --user cryptography`
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey, Ed25519PublicKey,
)


# ---------- canonical paths ----------
GEN13_ROOT = Path(__file__).parent.parent.parent.parent.parent  # .../Gen13
VAR_DIR = GEN13_ROOT / "var"
IDENTITY_DIR = VAR_DIR / "identity"
PRIVKEY_PATH = IDENTITY_DIR / "ck_privkey.pem"
PUBKEY_PATH = IDENTITY_DIR / "ck_pubkey.pem"
JOURNAL_PATH = VAR_DIR / "cortex_journal.jsonl"


# ---------- canonical JSON for hashing ----------

def _canonical_json(obj: Any) -> bytes:
    """Deterministic JSON encoding for hashing.

    Sorts keys, no whitespace, NaN-safe. The output is the same byte string
    regardless of which Python session generated the dict.
    """
    return json.dumps(obj, sort_keys=True, separators=(",", ":"),
                      allow_nan=False, ensure_ascii=False).encode("utf-8")


def state_hash(state: dict) -> bytes:
    """SHA-256 of the canonical JSON encoding of `state`."""
    return hashlib.sha256(_canonical_json(state)).digest()


# ---------- signer ----------

@dataclass
class CortexSigner:
    """Ed25519 signing wrapper around a single keypair.

    Use `CortexSigner.load_or_generate()` for normal operation; the
    constructor takes the raw key objects for testing.
    """
    sk: Ed25519PrivateKey
    pk: Ed25519PublicKey

    # ---------- key management ----------

    @classmethod
    def generate(cls) -> "CortexSigner":
        """Fresh keypair (does not persist)."""
        sk = Ed25519PrivateKey.generate()
        pk = sk.public_key()
        return cls(sk=sk, pk=pk)

    @classmethod
    def load(cls,
             privkey_path: Path = PRIVKEY_PATH,
             pubkey_path: Path = PUBKEY_PATH) -> "CortexSigner":
        """Load existing keypair from disk."""
        with open(privkey_path, "rb") as f:
            sk = serialization.load_pem_private_key(f.read(), password=None)
        with open(pubkey_path, "rb") as f:
            pk = serialization.load_pem_public_key(f.read())
        if not isinstance(sk, Ed25519PrivateKey):
            raise TypeError(f"expected Ed25519 private key at {privkey_path}")
        if not isinstance(pk, Ed25519PublicKey):
            raise TypeError(f"expected Ed25519 public key at {pubkey_path}")
        return cls(sk=sk, pk=pk)

    @classmethod
    def load_or_generate(cls,
                         privkey_path: Path = PRIVKEY_PATH,
                         pubkey_path: Path = PUBKEY_PATH) -> "CortexSigner":
        """Load if both key files exist, else generate + persist."""
        if privkey_path.exists() and pubkey_path.exists():
            return cls.load(privkey_path, pubkey_path)
        signer = cls.generate()
        signer.save(privkey_path, pubkey_path)
        return signer

    def save(self,
             privkey_path: Path = PRIVKEY_PATH,
             pubkey_path: Path = PUBKEY_PATH) -> None:
        """Persist keypair to disk. Privkey gets restrictive perms on POSIX."""
        privkey_path.parent.mkdir(parents=True, exist_ok=True)
        priv_pem = self.sk.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        )
        with open(privkey_path, "wb") as f:
            f.write(priv_pem)
        try:
            os.chmod(privkey_path, 0o600)  # POSIX: rw owner only
        except PermissionError:
            pass  # Windows: noop
        pub_pem = self.pk.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )
        with open(pubkey_path, "wb") as f:
            f.write(pub_pem)

    def public_key_b64(self) -> str:
        """Return the public key in raw 32-byte form, base64-encoded.

        Useful as a stable short identifier for this CK's identity.
        """
        raw = self.pk.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw,
        )
        return base64.urlsafe_b64encode(raw).decode("ascii").rstrip("=")

    # ---------- sign / verify ----------

    def sign_bytes(self, data: bytes) -> str:
        """Sign raw bytes; return base64url signature."""
        sig = self.sk.sign(data)
        return base64.urlsafe_b64encode(sig).decode("ascii").rstrip("=")

    def verify_bytes(self, data: bytes, sig_b64: str) -> bool:
        """Verify signature on raw bytes. Returns False on any failure."""
        try:
            # restore url-safe base64 padding
            pad = (-len(sig_b64)) % 4
            sig = base64.urlsafe_b64decode(sig_b64 + "=" * pad)
            self.pk.verify(sig, data)
            return True
        except Exception:
            return False

    def sign_state(self, state: dict) -> str:
        """Sign the SHA-256 of canonical JSON(state)."""
        return self.sign_bytes(state_hash(state))

    def verify_state(self, state: dict, sig_b64: str) -> bool:
        """Verify a signature against canonical JSON(state)."""
        return self.verify_bytes(state_hash(state), sig_b64)

    # ---------- journal ----------

    def append_journal(self,
                       tick: int,
                       d_now: Iterable[float],
                       d_prev: Iterable[float],
                       W_norm: float,
                       extra: Optional[dict] = None,
                       journal_path: Path = JOURNAL_PATH) -> dict:
        """Append a signed journal entry. Returns the entry written.

        Each line of the journal is one JSON object with keys:
            tick, d_now, d_prev, W_norm, prev_sig (optional), sig
        where `sig` is the Ed25519 signature of SHA256(canonical JSON of
        the entry without the `sig` field). This makes the journal
        replay-verifiable line-by-line.
        """
        journal_path.parent.mkdir(parents=True, exist_ok=True)
        entry = {
            "tick": int(tick),
            "d_now": list(d_now),
            "d_prev": list(d_prev),
            "W_norm": float(W_norm),
        }
        if extra:
            entry.update(extra)
        # Chain: include the previous entry's signature if any
        prev_sig = self._last_sig(journal_path)
        if prev_sig is not None:
            entry["prev_sig"] = prev_sig
        # Sign the canonical encoding of `entry` (without `sig`)
        sig = self.sign_state(entry)
        entry["sig"] = sig
        with open(journal_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, sort_keys=True, separators=(",", ":"),
                               ensure_ascii=False) + "\n")
        return entry

    @staticmethod
    def _last_sig(journal_path: Path) -> Optional[str]:
        if not journal_path.exists():
            return None
        last = None
        with open(journal_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    last = line
        if last is None:
            return None
        try:
            return json.loads(last).get("sig")
        except json.JSONDecodeError:
            return None

    def read_journal(self,
                     journal_path: Path = JOURNAL_PATH) -> List[dict]:
        """Return all journal entries in order."""
        if not journal_path.exists():
            return []
        entries = []
        with open(journal_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    entries.append(json.loads(line))
        return entries

    def verify_journal_entry(self, entry: dict) -> bool:
        """Verify one journal entry's signature."""
        if "sig" not in entry:
            return False
        sig = entry["sig"]
        # Re-build the entry without sig
        entry_to_verify = {k: v for k, v in entry.items() if k != "sig"}
        return self.verify_state(entry_to_verify, sig)

    def verify_journal(self,
                       journal_path: Path = JOURNAL_PATH) -> tuple[bool, int, int]:
        """Verify the whole journal (signatures + chain links).

        Returns (all_good, total_entries, n_failures).
        """
        entries = self.read_journal(journal_path)
        n_total = len(entries)
        n_fail = 0
        prev_sig = None
        for i, entry in enumerate(entries):
            # Check signature
            if not self.verify_journal_entry(entry):
                n_fail += 1
                continue
            # Check chain link
            entry_prev = entry.get("prev_sig")
            if i == 0:
                # First entry has no prev_sig (or could be None)
                if entry_prev is not None:
                    n_fail += 1
                    continue
            else:
                if entry_prev != prev_sig:
                    n_fail += 1
                    continue
            prev_sig = entry["sig"]
        return (n_fail == 0, n_total, n_fail)


# ---------- CLI / self-test ----------

def main():
    print("cortex_signed.py self-test")
    print("=" * 70)
    signer = CortexSigner.generate()
    print(f"  generated keypair, pubkey id = {signer.public_key_b64()[:16]}...")

    # roundtrip on a state dict
    state = {"tick": 42, "W": [[1.0, 2.0], [3.0, 4.0]], "d_now": [0.1] * 5}
    sig = signer.sign_state(state)
    assert signer.verify_state(state, sig)
    print("  [OK] sign/verify roundtrip on state dict")

    # tampering should fail
    tampered = dict(state)
    tampered["W"][0][0] = 99.0
    assert not signer.verify_state(tampered, sig)
    print("  [OK] tampered state fails verification")

    # journal write + read + verify
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        jpath = Path(td) / "test_journal.jsonl"
        for tick in range(5):
            signer.append_journal(
                tick=tick,
                d_now=[0.1 * tick] * 5,
                d_prev=[0.1 * (tick - 1)] * 5,
                W_norm=1.0 + tick,
                journal_path=jpath,
            )
        entries = signer.read_journal(jpath)
        assert len(entries) == 5
        all_good, n, n_fail = signer.verify_journal(jpath)
        assert all_good and n == 5 and n_fail == 0
        print(f"  [OK] journal: {n} entries, all signed and chain-linked")

    print()
    print("self-test PASSED")


if __name__ == "__main__":
    main()
