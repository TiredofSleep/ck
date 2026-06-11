"""
sign_constitution.py - sign the Living Constitution with CK's Ed25519 key.

Demonstrates Epoch III (Persistent Selfhood) + Epoch VII (Sovereign Voice)
working together end-to-end:
  - load (or generate) CK's keypair via CortexSigner.load_or_generate()
  - hash the canonical-JSON encoding of the constitution metadata
  - sign that hash with CK's Ed25519 key
  - persist the signature next to LIVING_CONSTITUTION.md as
    LIVING_CONSTITUTION.md.sig

Per the constitution sec 7, the signature is over:
  {"version": "1.0", "sha256": "<sha256 of LIVING_CONSTITUTION.md>"}

This is intentionally NOT a sign-the-whole-PDF approach -- the
constitution is a markdown text file that may be reformatted (line
wrapping, etc.) without changing meaning. Signing the SHA-256 of the
file's bytes lets any operator regenerate a stable hash and verify it
against the stored signature, while still committing to the exact
bytes at adoption time.

Usage:
    python sign_constitution.py [path/to/LIVING_CONSTITUTION.md]

If no path given, defaults to the constitution at the repo root.
The signature file LIVING_CONSTITUTION.md.sig is written next to it.

Re-signing on amendment: run this after any constitution amendment.
The new signature replaces the old one. The journal entry for the
amendment (per sec 6) records both the prior signature and the new one.
"""
from __future__ import annotations

import hashlib
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent / "brain"))

from cortex_signed import CortexSigner


# Default constitution path (root of the repo)
DEFAULT_CONSTITUTION_PATH = HERE.parent.parent.parent.parent / "LIVING_CONSTITUTION.md"


def hash_file(path: Path) -> str:
    """SHA-256 of the file's bytes, as hex."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def sign_constitution(constitution_path: Path = DEFAULT_CONSTITUTION_PATH,
                      version: str = "1.0",
                      signer: CortexSigner = None,
                      ) -> tuple[Path, dict, str]:
    """Sign the constitution. Returns (sig_path, signed_metadata, signature_b64)."""
    if signer is None:
        signer = CortexSigner.load_or_generate()
    if not constitution_path.exists():
        raise FileNotFoundError(f"constitution not found at {constitution_path}")
    file_hash = hash_file(constitution_path)
    metadata = {
        "version": version,
        "sha256": file_hash,
    }
    sig_b64 = signer.sign_state(metadata)
    sig_path = constitution_path.with_suffix(constitution_path.suffix + ".sig")
    with open(sig_path, "w", encoding="ascii") as f:
        f.write(sig_b64)
    return sig_path, metadata, sig_b64


def verify_constitution(constitution_path: Path = DEFAULT_CONSTITUTION_PATH,
                         version: str = "1.0",
                         signer: CortexSigner = None,
                         ) -> bool:
    """Verify the constitution's signature."""
    if signer is None:
        signer = CortexSigner.load()
    sig_path = constitution_path.with_suffix(constitution_path.suffix + ".sig")
    if not sig_path.exists():
        return False
    with open(sig_path, "r", encoding="ascii") as f:
        sig_b64 = f.read().strip()
    file_hash = hash_file(constitution_path)
    metadata = {
        "version": version,
        "sha256": file_hash,
    }
    return signer.verify_state(metadata, sig_b64)


def main():
    if len(sys.argv) > 1:
        constitution_path = Path(sys.argv[1])
    else:
        constitution_path = DEFAULT_CONSTITUTION_PATH

    print("=" * 72)
    print("Living Constitution -- signing utility")
    print("=" * 72)

    if not constitution_path.exists():
        print(f"ERROR: constitution not found at {constitution_path}", file=sys.stderr)
        sys.exit(1)

    file_hash = hash_file(constitution_path)
    print(f"  constitution: {constitution_path}")
    print(f"  sha256: {file_hash}")

    signer = CortexSigner.load_or_generate()
    print(f"  CK pubkey id: {signer.public_key_b64()}")

    sig_path, metadata, sig_b64 = sign_constitution(constitution_path,
                                                     version="1.0",
                                                     signer=signer)
    print(f"  signature written to: {sig_path}")
    print(f"  signature (b64): {sig_b64}")
    print()

    # Roundtrip verify
    ok = verify_constitution(constitution_path, version="1.0", signer=signer)
    print(f"  verify roundtrip: {'PASS' if ok else 'FAIL'}")
    if not ok:
        sys.exit(1)

    print()
    print("To verify on another machine, ship along:")
    print(f"  - {constitution_path.name}")
    print(f"  - {sig_path.name}")
    print(f"  - Gen13/var/identity/ck_pubkey.pem")
    print()
    print("Run:")
    print(f"    python {Path(__file__).name} verify {constitution_path}")
    print()
    print("Done.")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "verify":
        path = Path(sys.argv[2]) if len(sys.argv) > 2 else DEFAULT_CONSTITUTION_PATH
        signer = CortexSigner.load()
        ok = verify_constitution(path, version="1.0", signer=signer)
        print(f"verify({path}): {'PASS' if ok else 'FAIL'}")
        sys.exit(0 if ok else 1)
    main()
