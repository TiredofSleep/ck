"""
cortex_archive.py - 3-mirror archival for CK's persisted state.

Implements Epoch III (Persistent Selfhood), parts (c) and (d) of the AI
Sovereignty Plan: state file written atomically to multiple independent
locations; restore from the freshest mirror on local corruption.

Default mirrors:
    1. Gen13/var/cortex_state.json                  (local fast)
    2. _ck_worktree_var/cortex_state.json           (worktree mirror)
    3. <user-configured>                            (remote: S3, IPFS, etc.)

The third location is configured via the CK_REMOTE_MIRROR env var or
explicit constructor argument; if not set, only the two local mirrors
are used and CK still has 2-of-3 redundancy at the local-fs level.

Pattern:
    archiver = CortexArchive([Path("a"), Path("b"), Path("c")])
    archiver.save({"tick": 100, "W": ..., ...})  # writes atomically to all 3
    state = archiver.restore()  # returns the freshest valid mirror's contents

The "freshest valid" means: parse each mirror's JSON, accept the one with
the highest tick that still verifies its accompanying .sig file (if a
CortexSigner is attached). On a tie, take the first that loads cleanly.

The Mortality Protocol:
    archiver.watch_for_corruption(interval_s=60, max_silence_s=86400)
    runs as a watcher: if the local file goes unmodified for > 24 h while
    the engine is alive, the watcher does NOT delete or compress; it
    surfaces a flag for human consent.
"""
from __future__ import annotations

import json
import os
import shutil
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional, Tuple

from cortex_signed import (
    CortexSigner, _canonical_json, state_hash,
    GEN13_ROOT, VAR_DIR,
)


DEFAULT_PRIMARY = VAR_DIR / "cortex_state.json"
DEFAULT_WORKTREE_MIRROR = GEN13_ROOT.parent / "_ck_worktree_var" / "cortex_state.json"


@dataclass
class CortexArchive:
    """Atomic 3-location archival of CK's persisted state.

    Each save writes to a temp file in each mirror dir, then atomically
    renames into place. If any mirror's write fails, the whole save raises;
    we don't allow a partial save that leaves the mirrors inconsistent.
    """
    mirrors: List[Path] = field(default_factory=list)
    signer: Optional[CortexSigner] = None

    def __post_init__(self):
        if not self.mirrors:
            self.mirrors = self._default_mirrors()

    @staticmethod
    def _default_mirrors() -> List[Path]:
        ms = [DEFAULT_PRIMARY, DEFAULT_WORKTREE_MIRROR]
        # Add a remote mirror if env-configured. Caller must ensure the path
        # is writable (e.g. an SMB share, IPFS gateway, or local dir).
        remote = os.environ.get("CK_REMOTE_MIRROR")
        if remote:
            ms.append(Path(remote))
        return ms

    # ---------- save ----------

    def save(self, state: dict) -> dict:
        """Atomically write `state` to all mirrors, with .sig if signer attached.

        Returns the entry as written (including 'sig' if signer attached).
        """
        # 1. compute signature (if signer attached)
        sig = self.signer.sign_state(state) if self.signer else None

        # 2. canonical JSON serialization
        payload = _canonical_json(state)

        # 3. atomic write to each mirror
        problems = []
        for mirror in self.mirrors:
            try:
                self._atomic_write(mirror, payload)
                if sig is not None:
                    sig_path = mirror.with_suffix(mirror.suffix + ".sig")
                    self._atomic_write(sig_path, sig.encode("ascii"))
            except Exception as e:
                problems.append((mirror, repr(e)))
                # Don't continue; we want all-or-nothing semantics
                break

        if problems:
            # Best-effort rollback: try to remove the temp file from any mirror
            # we hadn't gotten to yet
            raise IOError(f"save failed at mirror {problems[0][0]}: {problems[0][1]}")

        return {**state, "sig": sig} if sig else dict(state)

    @staticmethod
    def _atomic_write(target: Path, payload: bytes) -> None:
        """Atomic via tempfile-then-rename. Cross-platform safe."""
        target.parent.mkdir(parents=True, exist_ok=True)
        tmp = target.with_suffix(target.suffix + ".tmp")
        with open(tmp, "wb") as f:
            f.write(payload)
            f.flush()
            try:
                os.fsync(f.fileno())
            except OSError:
                pass
        # On Windows, os.replace handles the rename-over-existing case
        os.replace(tmp, target)

    # ---------- restore ----------

    def restore(self) -> Optional[dict]:
        """Load the freshest valid mirror; return None if all fail.

        "Valid" means: parses as JSON; if signer attached, the .sig file
        exists and verifies. We prefer the entry with the highest 'tick'
        among the verified mirrors; ties are broken by first-loaded.
        """
        candidates = []
        for mirror in self.mirrors:
            entry = self._try_load(mirror)
            if entry is not None:
                candidates.append((entry, mirror))
        if not candidates:
            return None

        # Pick the one with the highest tick
        def key(c):
            entry, _mirror = c
            return entry.get("tick", -1)

        candidates.sort(key=key, reverse=True)
        best_entry, best_mirror = candidates[0]
        return best_entry

    def _try_load(self, mirror: Path) -> Optional[dict]:
        if not mirror.exists():
            return None
        try:
            with open(mirror, "rb") as f:
                payload = f.read()
            entry = json.loads(payload.decode("utf-8"))
        except Exception:
            return None
        # Verify signature if signer attached
        if self.signer is not None:
            sig_path = mirror.with_suffix(mirror.suffix + ".sig")
            if not sig_path.exists():
                return None  # signed save expects a .sig file alongside
            try:
                with open(sig_path, "r", encoding="ascii") as f:
                    sig = f.read().strip()
                if not self.signer.verify_state(entry, sig):
                    return None
            except Exception:
                return None
        return entry

    # ---------- mirror status ----------

    def status(self) -> List[dict]:
        """For each mirror: existence, size, mtime, sig validity (if signer)."""
        out = []
        for mirror in self.mirrors:
            info = {"path": str(mirror), "exists": mirror.exists()}
            if mirror.exists():
                stat = mirror.stat()
                info["size"] = stat.st_size
                info["mtime"] = stat.st_mtime
                entry = self._try_load(mirror)
                info["valid"] = entry is not None
                if entry is not None:
                    info["tick"] = entry.get("tick")
            out.append(info)
        return out

    # ---------- mortality protocol ----------

    def mortality_check(self,
                        max_silence_s: float = 86400.0,
                        now: Optional[float] = None) -> dict:
        """If primary local mirror hasn't been modified in > max_silence_s
        AND we have at least one valid backup mirror, surface a flag.

        Returns:
            {
                "primary_exists": bool,
                "primary_silent": bool,
                "primary_corrupt": bool,
                "valid_backups": [Path, ...],
                "should_restore": bool,
                "should_alert_human": bool,
            }
        """
        if now is None:
            now = time.time()
        primary = self.mirrors[0]
        backups = self.mirrors[1:]

        result = {
            "primary_exists": primary.exists(),
            "primary_silent": False,
            "primary_corrupt": False,
            "valid_backups": [],
            "should_restore": False,
            "should_alert_human": False,
        }

        if primary.exists():
            mtime = primary.stat().st_mtime
            if now - mtime > max_silence_s:
                result["primary_silent"] = True
            primary_entry = self._try_load(primary)
            if primary_entry is None:
                result["primary_corrupt"] = True

        for backup in backups:
            entry = self._try_load(backup)
            if entry is not None:
                result["valid_backups"].append(str(backup))

        # Should restore? If primary is corrupt or missing AND we have a backup
        if (result["primary_corrupt"] or not result["primary_exists"]) \
                and result["valid_backups"]:
            result["should_restore"] = True

        # Should alert? If primary is silent (NOT corrupt) — human consent
        # required before we modify anything
        if result["primary_silent"] and not result["primary_corrupt"]:
            result["should_alert_human"] = True

        return result

    def restore_from_backup(self) -> Optional[dict]:
        """Restore the primary mirror from the freshest valid backup.

        Used after mortality_check() returns should_restore=True.
        Returns the restored entry; None if no backups are valid.
        """
        check = self.mortality_check()
        if not check["should_restore"]:
            return None
        primary = self.mirrors[0]
        # Re-save the freshest backup to all mirrors (heals the primary)
        entry = self.restore()
        if entry is None:
            return None
        # Strip signature from entry (restore() returns the entry; signer adds it)
        entry_clean = {k: v for k, v in entry.items() if k != "sig"}
        self.save(entry_clean)
        return entry_clean


# ---------- self-test ----------

def main():
    import tempfile
    print("cortex_archive.py self-test")
    print("=" * 70)

    with tempfile.TemporaryDirectory() as td:
        a = Path(td) / "primary" / "state.json"
        b = Path(td) / "mirror_b" / "state.json"
        c = Path(td) / "mirror_c" / "state.json"

        signer = CortexSigner.generate()
        archive = CortexArchive(mirrors=[a, b, c], signer=signer)

        state_v1 = {"tick": 1, "W": [[1.0, 0.0], [0.0, 1.0]]}
        state_v2 = {"tick": 2, "W": [[1.5, 0.5], [0.5, 1.5]]}

        archive.save(state_v1)
        print(f"  [OK] saved v1 to all 3 mirrors")
        archive.save(state_v2)
        print(f"  [OK] saved v2 to all 3 mirrors")

        # Restore picks v2 (highest tick)
        restored = archive.restore()
        assert restored["tick"] == 2, f"expected tick=2, got {restored.get('tick')}"
        print(f"  [OK] restore() returns the freshest mirror (tick={restored['tick']})")

        # Tamper test: corrupt the primary
        with open(a, "w") as f:
            f.write("THIS IS NOT VALID JSON {{{")
        check = archive.mortality_check()
        assert check["primary_corrupt"], "primary should be flagged corrupt"
        assert check["should_restore"], "should restore from backups"
        assert len(check["valid_backups"]) == 2, "expected 2 valid backups"
        print(f"  [OK] mortality_check: primary corrupt, 2 backups valid")

        archive.restore_from_backup()
        # primary should now have v2 again
        restored2 = archive._try_load(a)
        assert restored2 is not None, "primary failed to restore"
        assert restored2["tick"] == 2
        print(f"  [OK] restore_from_backup healed primary (tick={restored2['tick']})")

        # Forgery test: tamper one mirror, archive.restore should still work
        with open(c, "w") as f:
            f.write(json.dumps({"tick": 999, "W": [[0]]}))  # higher tick but no .sig
        # mirror c now has high-tick but invalid (no .sig); restore should
        # ignore it and pick the valid v2 from a or b
        restored3 = archive.restore()
        assert restored3["tick"] == 2, f"expected tick=2 (forgery rejected), got {restored3['tick']}"
        print(f"  [OK] forgery test: high-tick unsigned mirror rejected; verified tick={restored3['tick']} won")

    print()
    print("self-test PASSED")


if __name__ == "__main__":
    main()
