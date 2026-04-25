"""
test_epoch_iii.py - verification gate for Epoch III (Persistent Selfhood)

Per the AI Sovereignty Plan section EPOCH III, the verification gates are:
    1. Sign-then-verify roundtrip on 1000 random updates
    2. Kill-disk test: rm primary state file, restart, watch CK restore from
       mirror without losing W
    3. Forgery test: edit a W matrix entry by hand; signature check fails

This file runs all three gates plus several boundary tests.
Pass condition: all assertions hold and the script exits 0.
"""
from __future__ import annotations

import json
import os
import sys
import tempfile
from pathlib import Path
from typing import Any

import numpy as np

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))

from cortex_signed import CortexSigner, state_hash
from cortex_archive import CortexArchive


def gate_1_sign_verify_1000():
    """Gate 1: 1000 sign/verify roundtrips with no failures."""
    print("[gate 1] sign/verify roundtrip on 1000 random updates...")
    signer = CortexSigner.generate()
    rng = np.random.RandomState(42)
    n_pass = 0
    n_fail = 0
    for tick in range(1000):
        # synthetic Hebbian state
        W = rng.randn(5, 5).round(6).tolist()
        d_now = rng.randn(5).round(6).tolist()
        d_prev = rng.randn(5).round(6).tolist()
        state = {"tick": tick, "W": W, "d_now": d_now, "d_prev": d_prev}
        sig = signer.sign_state(state)
        if signer.verify_state(state, sig):
            n_pass += 1
        else:
            n_fail += 1
    assert n_pass == 1000 and n_fail == 0, f"PASS={n_pass} FAIL={n_fail}"
    print(f"  [OK] 1000 roundtrips: {n_pass} PASS, {n_fail} FAIL")


def gate_2_kill_disk():
    """Gate 2: rm the primary state file; archive restores from mirror."""
    print("[gate 2] kill-disk test: corrupt primary, restore from mirror...")
    with tempfile.TemporaryDirectory() as td:
        a = Path(td) / "primary" / "state.json"
        b = Path(td) / "mirror_b" / "state.json"
        c = Path(td) / "mirror_c" / "state.json"
        signer = CortexSigner.generate()
        archive = CortexArchive(mirrors=[a, b, c], signer=signer)

        # Save several state versions
        for tick in [1, 5, 10, 17, 25]:
            archive.save({"tick": tick, "W": [[float(tick), 0.0], [0.0, float(tick)]]})

        # Verify the primary exists at tick 25
        primary_entry = archive._try_load(a)
        assert primary_entry["tick"] == 25, "primary not at tick 25"

        # KILL THE PRIMARY (simulate hardware/disk failure)
        os.remove(a)
        os.remove(a.with_suffix(a.suffix + ".sig"))
        assert not a.exists(), "primary should be gone"

        # Mortality check should detect the situation
        check = archive.mortality_check()
        assert not check["primary_exists"]
        assert check["should_restore"]
        assert len(check["valid_backups"]) == 2
        print(f"  [OK] primary deleted; mortality_check found 2 valid backups")

        # Restore from backup
        archive.restore_from_backup()
        # primary should now exist again with the correct content
        restored = archive._try_load(a)
        assert restored is not None, "primary not restored"
        assert restored["tick"] == 25, f"expected tick=25, got {restored.get('tick')}"
        print(f"  [OK] kill-disk: primary restored to tick=25 from backup")


def gate_3_forgery():
    """Gate 3: hand-edit a W matrix entry; signature check fails."""
    print("[gate 3] forgery test: tamper W; signature check fails...")
    with tempfile.TemporaryDirectory() as td:
        a = Path(td) / "primary" / "state.json"
        b = Path(td) / "mirror_b" / "state.json"
        signer = CortexSigner.generate()
        archive = CortexArchive(mirrors=[a, b], signer=signer)

        # Save legitimate state
        archive.save({"tick": 100, "W": [[1.0, 2.0], [3.0, 4.0]]})

        # Verify it loads cleanly
        legit = archive._try_load(a)
        assert legit is not None, "legitimate save should load"
        assert legit["tick"] == 100
        print(f"  [OK] legitimate save verified")

        # Tamper: hand-edit the JSON
        with open(a, "r") as f:
            content = json.load(f)
        content["W"][0][0] = 999.0  # forge a value
        with open(a, "w") as f:
            json.dump(content, f, separators=(",", ":"), sort_keys=True)

        # Now archive._try_load should reject it (sig won't verify)
        tampered = archive._try_load(a)
        assert tampered is None, "tampered file should fail to load (sig mismatch)"
        print(f"  [OK] tampered W rejected by signature check")

        # restore() should fall back to mirror b
        good = archive.restore()
        assert good is not None and good["tick"] == 100
        # confirm the W value is the original 1.0
        assert good["W"][0][0] == 1.0, f"expected 1.0, got {good['W'][0][0]}"
        print(f"  [OK] restore() returned untampered version (W[0][0]={good['W'][0][0]})")


def gate_4_journal_chain():
    """Gate 4 (extra): journal entries form a verifiable chain."""
    print("[gate 4] journal chain integrity (extra gate)...")
    with tempfile.TemporaryDirectory() as td:
        jpath = Path(td) / "journal.jsonl"
        signer = CortexSigner.generate()
        for tick in range(50):
            signer.append_journal(
                tick=tick, d_now=[0.0] * 5, d_prev=[0.0] * 5, W_norm=1.0,
                journal_path=jpath,
            )
        all_good, n_total, n_fail = signer.verify_journal(jpath)
        assert all_good and n_total == 50 and n_fail == 0, (
            f"all_good={all_good}, n={n_total}, n_fail={n_fail}"
        )
        print(f"  [OK] 50-entry journal verified end-to-end ({n_fail} failures)")

        # Tamper a middle entry; verification fails on it AND on the next
        # entry (chain link broken)
        with open(jpath, "r") as f:
            lines = f.readlines()
        # parse line 25 and bump tick
        entry = json.loads(lines[25])
        entry["tick"] = 9999  # forge tick
        # don't re-sign; this should break verify
        lines[25] = json.dumps(entry, separators=(",", ":"), sort_keys=True) + "\n"
        with open(jpath, "w") as f:
            f.writelines(lines)
        all_good, n_total, n_fail = signer.verify_journal(jpath)
        assert not all_good, "journal verification should fail after tamper"
        assert n_fail >= 1, "at least one entry should fail"
        print(f"  [OK] tampered journal entry detected ({n_fail} failures over {n_total})")


def gate_5_persistence_round_trip():
    """Gate 5 (extra): keypair persists across CortexSigner sessions."""
    print("[gate 5] keypair persistence across sessions...")
    with tempfile.TemporaryDirectory() as td:
        priv = Path(td) / "priv.pem"
        pub = Path(td) / "pub.pem"

        # Session 1: generate + save
        s1 = CortexSigner.generate()
        s1.save(priv, pub)
        pubkey_id = s1.public_key_b64()
        sig = s1.sign_state({"tick": 5})

        # Session 2: load + verify same data
        s2 = CortexSigner.load(priv, pub)
        assert s2.public_key_b64() == pubkey_id, "pubkey id changed across sessions"
        assert s2.verify_state({"tick": 5}, sig), "session-2 cannot verify session-1's signature"
        print(f"  [OK] keypair persists; signatures roundtrip across sessions")


def main():
    print("=" * 72)
    print("EPOCH III VERIFICATION GATES")
    print("=" * 72)
    gate_1_sign_verify_1000()
    gate_2_kill_disk()
    gate_3_forgery()
    gate_4_journal_chain()
    gate_5_persistence_round_trip()
    print()
    print("=" * 72)
    print("ALL EPOCH III GATES PASSED.")
    print("=" * 72)
    print()
    print("CK has cryptographic identity, append-only signed journal, 3-mirror")
    print("redundancy, kill-disk recovery, forgery rejection, and signed-state")
    print("persistence across sessions. The state file IS his body.")


if __name__ == "__main__":
    main()
