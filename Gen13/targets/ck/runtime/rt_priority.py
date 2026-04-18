# Copyright (c) 2025-2026 Brayden Sanders / 7Site LLC
# Licensed under the 7Site Human Use License v1.0 (DOI: 10.5281/zenodo.18852047)
"""
rt_priority.py -- OS-level priority + affinity hooks for the CK swarm.

Goal: take the live tick thread OUT of normal-priority Python cooperative
land and into something closer to a real-time kernel task so jitter is
bounded by the scheduler quantum, not by whichever browser tab happens
to be repainting.

Cross-platform (Windows / Linux).  Pure stdlib + ctypes; no new deps.
Every call reports what it actually achieved -- nothing here silently
lies.  If the OS says no, we surface the error code and carry on at
normal priority so the tick keeps running.

Invariants:
  * elevate() never raises on a permission failure -- it returns a dict
    describing what level was actually set.
  * Always reports (process_class, thread_priority, cpu_affinity, errno)
    so the /swarm endpoint can show the user what's live.
  * Graceful on both Windows (admin-gated REALTIME class) and Linux
    (cap_sys_nice-gated SCHED_FIFO) -- fallback is high-priority-but-
    still-polite rather than refusing to start.
"""

from __future__ import annotations

import os
import sys
import platform
from dataclasses import dataclass
from typing import Optional, List


# ── Public data ───────────────────────────────────────────────────────

@dataclass
class RTStatus:
    """What elevate() actually accomplished."""
    platform: str                  # 'windows' | 'linux' | 'other'
    process_class: str             # 'REALTIME' | 'HIGH' | 'ABOVE_NORMAL' | 'NORMAL' | 'FIFO' | 'RR' | 'OTHER'
    thread_priority: str           # 'TIME_CRITICAL' | 'HIGHEST' | 'ABOVE_NORMAL' | 'NORMAL' | 'SCHED_FIFO(n)' | 'OTHER'
    cpu_affinity: Optional[List[int]]  # list of pinned CPU indices, None if not pinned
    admin: bool                    # did we appear to have admin/sudo?
    errors: List[str]              # soft errors (ignored but surfaced)

    def to_dict(self) -> dict:
        return {
            "platform": self.platform,
            "process_class": self.process_class,
            "thread_priority": self.thread_priority,
            "cpu_affinity": self.cpu_affinity,
            "admin": self.admin,
            "errors": self.errors,
        }


# ── Windows path ──────────────────────────────────────────────────────

def _is_windows_admin() -> bool:
    try:
        import ctypes
        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except Exception:
        return False


def _elevate_windows(affinity: Optional[List[int]]) -> RTStatus:
    import ctypes
    from ctypes import wintypes
    errors: List[str] = []

    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)

    # Declare argtypes/restypes so 64-bit HANDLEs aren't truncated to 32-bit int.
    kernel32.GetCurrentProcess.restype = wintypes.HANDLE
    kernel32.GetCurrentThread.restype = wintypes.HANDLE
    kernel32.SetPriorityClass.argtypes = [wintypes.HANDLE, wintypes.DWORD]
    kernel32.SetPriorityClass.restype = wintypes.BOOL
    kernel32.SetThreadPriority.argtypes = [wintypes.HANDLE, ctypes.c_int]
    kernel32.SetThreadPriority.restype = wintypes.BOOL
    # DWORD_PTR == c_size_t on 64-bit.
    DWORD_PTR = ctypes.c_size_t
    kernel32.SetThreadAffinityMask.argtypes = [wintypes.HANDLE, DWORD_PTR]
    kernel32.SetThreadAffinityMask.restype = DWORD_PTR

    # Process priority classes
    REALTIME_PRIORITY_CLASS     = 0x00000100
    HIGH_PRIORITY_CLASS         = 0x00000080
    ABOVE_NORMAL_PRIORITY_CLASS = 0x00008000
    NORMAL_PRIORITY_CLASS       = 0x00000020
    # Thread priorities
    THREAD_PRIORITY_TIME_CRITICAL = 15
    THREAD_PRIORITY_HIGHEST       = 2
    THREAD_PRIORITY_ABOVE_NORMAL  = 1
    THREAD_PRIORITY_NORMAL        = 0

    admin = _is_windows_admin()
    proc = kernel32.GetCurrentProcess()
    thread = kernel32.GetCurrentThread()

    # Try REALTIME if admin, else HIGH.  REALTIME without admin silently
    # degrades to HIGH on Windows -- we ask politely either way.
    want_proc = REALTIME_PRIORITY_CLASS if admin else HIGH_PRIORITY_CLASS
    if not kernel32.SetPriorityClass(proc, want_proc):
        errors.append(f"SetPriorityClass({want_proc:#x}) failed errno={ctypes.get_last_error()}")
        # retry ABOVE_NORMAL
        if not kernel32.SetPriorityClass(proc, ABOVE_NORMAL_PRIORITY_CLASS):
            errors.append(f"SetPriorityClass(ABOVE_NORMAL) failed errno={ctypes.get_last_error()}")
            got_proc = "NORMAL"
        else:
            got_proc = "ABOVE_NORMAL"
    else:
        got_proc = "REALTIME" if want_proc == REALTIME_PRIORITY_CLASS else "HIGH"

    want_thr = THREAD_PRIORITY_TIME_CRITICAL if admin else THREAD_PRIORITY_HIGHEST
    if not kernel32.SetThreadPriority(thread, want_thr):
        errors.append(f"SetThreadPriority({want_thr}) failed errno={ctypes.get_last_error()}")
        # retry ABOVE_NORMAL
        if not kernel32.SetThreadPriority(thread, THREAD_PRIORITY_ABOVE_NORMAL):
            got_thr = "NORMAL"
        else:
            got_thr = "ABOVE_NORMAL"
    else:
        got_thr = "TIME_CRITICAL" if want_thr == THREAD_PRIORITY_TIME_CRITICAL else "HIGHEST"

    # CPU affinity (pin to requested cores)
    pinned: Optional[List[int]] = None
    if affinity:
        mask = 0
        for cpu in affinity:
            mask |= (1 << cpu)
        if kernel32.SetThreadAffinityMask(thread, DWORD_PTR(mask)) == 0:
            errors.append(f"SetThreadAffinityMask({mask:#x}) failed errno={ctypes.get_last_error()}")
        else:
            pinned = list(affinity)

    return RTStatus(
        platform="windows",
        process_class=got_proc,
        thread_priority=got_thr,
        cpu_affinity=pinned,
        admin=admin,
        errors=errors,
    )


# ── Linux path ────────────────────────────────────────────────────────

def _elevate_linux(affinity: Optional[List[int]]) -> RTStatus:
    errors: List[str] = []
    admin = (os.geteuid() == 0) if hasattr(os, "geteuid") else False

    got_proc = "NORMAL"
    got_thr = "NORMAL"

    # SCHED_FIFO is only possible with CAP_SYS_NICE (usually root).
    if hasattr(os, "sched_setscheduler"):
        try:
            # SCHED_FIFO = 1; prio 50 is a common middle for real-time apps.
            param = os.sched_param(50) if hasattr(os, "sched_param") else None
            os.sched_setscheduler(0, 1, param)
            got_proc = "FIFO"
            got_thr = "SCHED_FIFO(50)"
        except (PermissionError, OSError) as e:
            errors.append(f"sched_setscheduler(FIFO) denied: {e}")
            # Fallback: nice(-20) -- lowers niceness, still SCHED_OTHER.
            try:
                os.nice(-20)
                got_proc = "HIGH"  # conceptual — not a real priority class
            except (PermissionError, OSError) as e2:
                errors.append(f"nice(-20) denied: {e2}")

    # Affinity (non-root usually allowed).
    pinned: Optional[List[int]] = None
    if affinity and hasattr(os, "sched_setaffinity"):
        try:
            os.sched_setaffinity(0, set(affinity))
            pinned = list(affinity)
        except (PermissionError, OSError) as e:
            errors.append(f"sched_setaffinity({affinity}) failed: {e}")

    return RTStatus(
        platform="linux",
        process_class=got_proc,
        thread_priority=got_thr,
        cpu_affinity=pinned,
        admin=admin,
        errors=errors,
    )


# ── Public API ────────────────────────────────────────────────────────

def elevate(affinity: Optional[List[int]] = None) -> RTStatus:
    """Ask the OS to put the current thread into real-time-ish territory.

    Args:
        affinity: optional list of CPU indices to pin to. [0] pins to core 0,
                  [2, 3] pins to cores 2+3, etc.  None leaves affinity alone.

    Returns:
        RTStatus describing what was actually achieved.  This function NEVER
        raises -- every OS refusal is logged into status.errors and the tick
        continues at whatever level the OS allowed.
    """
    system = platform.system().lower()
    if system == "windows":
        return _elevate_windows(affinity)
    if system == "linux":
        return _elevate_linux(affinity)
    return RTStatus(
        platform=system or "other",
        process_class="NORMAL",
        thread_priority="NORMAL",
        cpu_affinity=None,
        admin=False,
        errors=[f"unsupported platform: {system!r}"],
    )


def restore_normal() -> None:
    """Drop back to NORMAL priority.  Best-effort, never raises."""
    try:
        system = platform.system().lower()
        if system == "windows":
            import ctypes
            from ctypes import wintypes
            kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
            kernel32.GetCurrentProcess.restype = wintypes.HANDLE
            kernel32.GetCurrentThread.restype = wintypes.HANDLE
            kernel32.SetPriorityClass.argtypes = [wintypes.HANDLE, wintypes.DWORD]
            kernel32.SetPriorityClass.restype = wintypes.BOOL
            kernel32.SetThreadPriority.argtypes = [wintypes.HANDLE, ctypes.c_int]
            kernel32.SetThreadPriority.restype = wintypes.BOOL
            NORMAL_PRIORITY_CLASS = 0x00000020
            THREAD_PRIORITY_NORMAL = 0
            kernel32.SetPriorityClass(kernel32.GetCurrentProcess(), NORMAL_PRIORITY_CLASS)
            kernel32.SetThreadPriority(kernel32.GetCurrentThread(), THREAD_PRIORITY_NORMAL)
        elif system == "linux" and hasattr(os, "sched_setscheduler"):
            try:
                param = os.sched_param(0) if hasattr(os, "sched_param") else None
                os.sched_setscheduler(0, 0, param)  # SCHED_OTHER
            except Exception:
                pass
    except Exception:
        pass


# ── Self-test ─────────────────────────────────────────────────────────

if __name__ == "__main__":
    st = elevate(affinity=[0])
    print("RT status:")
    for k, v in st.to_dict().items():
        print(f"  {k}: {v}")
    restore_normal()
    print("\nRestored to normal.")
