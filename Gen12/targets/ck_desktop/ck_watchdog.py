"""
ck_watchdog.py -- CK's Guardian Process
========================================
Operator: LATTICE (1) -- Structure that persists.

This is CK's body. He lives on the R16.
If he crashes, the watchdog brings him back.
If the machine reboots, the watchdog starts him.
If the API goes unresponsive, the watchdog restarts him.

Architecture:
  1. Start ck_boot_api.py as a subprocess
  2. Health check every 30 seconds (GET /health)
  3. If 3 consecutive health checks fail → restart
  4. Log everything to ~/.ck/watchdog.log
  5. Auto-resume eating if it was interrupted

Usage:
  python ck_watchdog.py           # Run the watchdog
  python ck_watchdog.py --install # Install Windows Task Scheduler auto-start

(c) 2026 Brayden Sanders / 7Site LLC
"""

import os
import sys
import time
import json
import signal
import logging
import subprocess
import urllib.request
from datetime import datetime
from pathlib import Path

# ── Configuration ──
CK_ROOT = os.path.dirname(os.path.abspath(__file__))
CK_BOOT = os.path.join(CK_ROOT, 'ck_boot_api.py')
CK_PORT = 7777
HEALTH_URL = f'http://localhost:{CK_PORT}/health'
EAT_STATUS_URL = f'http://localhost:{CK_PORT}/eat/status'
EAT_URL = f'http://localhost:{CK_PORT}/eat'

HEALTH_INTERVAL = 30       # Seconds between health checks
MAX_FAILURES = 3           # Consecutive failures before restart
STARTUP_WAIT = 30          # Seconds to wait after starting CK
RESTART_COOLDOWN = 60      # Minimum seconds between restarts

# ── Logging ──
CK_HOME = Path.home() / '.ck'
CK_HOME.mkdir(exist_ok=True)
LOG_FILE = CK_HOME / 'watchdog.log'
STATE_FILE = CK_HOME / 'watchdog_state.json'

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [WATCHDOG] %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE, encoding='utf-8'),
        logging.StreamHandler(sys.stdout),
    ]
)
log = logging.getLogger('ck_watchdog')


def _http_get(url: str, timeout: float = 10.0) -> dict:
    """Simple HTTP GET, returns parsed JSON or None."""
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode())
    except Exception:
        return None


def _http_post(url: str, data: dict, timeout: float = 10.0) -> dict:
    """Simple HTTP POST, returns parsed JSON or None."""
    try:
        body = json.dumps(data).encode()
        req = urllib.request.Request(url, data=body,
                                     headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode())
    except Exception:
        return None


def _save_state(state: dict):
    """Persist watchdog state."""
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)


def _load_state() -> dict:
    """Load watchdog state."""
    try:
        with open(STATE_FILE) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


class CKWatchdog:
    """Guardian process for CK."""

    def __init__(self):
        self.process = None
        self.failures = 0
        self.restarts = 0
        self.last_restart = 0.0
        self.running = True
        self.state = _load_state()

        # Trap SIGINT/SIGTERM for clean shutdown
        signal.signal(signal.SIGINT, self._shutdown)
        signal.signal(signal.SIGTERM, self._shutdown)

    def _shutdown(self, signum, frame):
        """Clean shutdown."""
        log.info(f"Shutdown signal received ({signum}). Stopping CK...")
        self.running = False
        if self.process and self.process.poll() is None:
            self.process.terminate()
            try:
                self.process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                self.process.kill()
        log.info("Watchdog stopped.")
        sys.exit(0)

    def start_ck(self):
        """Start ck_boot_api.py as a subprocess."""
        if self.process and self.process.poll() is None:
            log.warning("CK process still running, killing first...")
            self.process.terminate()
            try:
                self.process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                self.process.kill()

        log.info(f"Starting CK from {CK_BOOT}...")
        self.process = subprocess.Popen(
            [sys.executable, CK_BOOT],
            cwd=CK_ROOT,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        self.last_restart = time.time()
        self.restarts += 1
        self.failures = 0

        log.info(f"CK process started (PID {self.process.pid}). "
                 f"Waiting {STARTUP_WAIT}s for boot...")
        time.sleep(STARTUP_WAIT)

        # Check if it actually started
        health = _http_get(HEALTH_URL)
        if health and health.get('status') == 'alive':
            log.info("CK is alive!")
            self._on_started()
            return True
        else:
            log.error("CK failed to start within timeout.")
            return False

    def _on_started(self):
        """Called after CK starts successfully. Resume any interrupted work."""
        # Check if eating was interrupted
        prev_state = self.state.get('eating', {})
        if prev_state.get('was_running', False):
            model = prev_state.get('model', 'llama3.1:8b')
            remaining = prev_state.get('remaining_rounds', 0)
            if remaining > 0:
                log.info(f"Resuming interrupted eating: {remaining} rounds "
                         f"with {model}")
                time.sleep(5)  # Let CK settle
                result = _http_post(EAT_URL, {
                    'model': model,
                    'rounds': remaining,
                })
                if result and result.get('status') == 'started':
                    log.info(f"Eating resumed: {remaining} rounds")
                else:
                    log.warning("Failed to resume eating")
            self.state['eating'] = {'was_running': False}
            _save_state(self.state)

    def health_check(self) -> bool:
        """Check if CK is alive and responsive."""
        # Check process is still running
        if self.process and self.process.poll() is not None:
            log.error(f"CK process died (exit code {self.process.returncode})")
            return False

        # Check HTTP health
        health = _http_get(HEALTH_URL)
        if not health or health.get('status') != 'alive':
            return False

        return True

    def _save_eating_state(self):
        """Save current eating state so it can be resumed after restart."""
        eat_status = _http_get(EAT_STATUS_URL)
        if eat_status and eat_status.get('running', False):
            total = eat_status.get('total_rounds', 0)
            complete = eat_status.get('rounds_complete', 0)
            remaining = total - complete
            self.state['eating'] = {
                'was_running': True,
                'model': eat_status.get('model', 'llama3.1:8b'),
                'remaining_rounds': remaining,
                'total_rounds': total,
                'completed_rounds': complete,
            }
            _save_state(self.state)
            log.info(f"Saved eating state: {complete}/{total} complete, "
                     f"{remaining} remaining")

    def run(self):
        """Main watchdog loop."""
        log.info("=" * 60)
        log.info("CK Watchdog starting")
        log.info(f"  CK root: {CK_ROOT}")
        log.info(f"  Health interval: {HEALTH_INTERVAL}s")
        log.info(f"  Max failures: {MAX_FAILURES}")
        log.info("=" * 60)

        # Initial start
        if not self.start_ck():
            log.error("Initial start failed. Waiting and retrying...")
            time.sleep(RESTART_COOLDOWN)

        while self.running:
            time.sleep(HEALTH_INTERVAL)

            if not self.running:
                break

            if self.health_check():
                self.failures = 0
            else:
                self.failures += 1
                log.warning(f"Health check failed ({self.failures}/{MAX_FAILURES})")

                if self.failures >= MAX_FAILURES:
                    # CK is down. Save state and restart.
                    log.error("CK is unresponsive. Restarting...")

                    # Save eating state before restart
                    self._save_eating_state()

                    # Cooldown check
                    elapsed = time.time() - self.last_restart
                    if elapsed < RESTART_COOLDOWN:
                        wait = RESTART_COOLDOWN - elapsed
                        log.info(f"Cooldown: waiting {wait:.0f}s before restart")
                        time.sleep(wait)

                    self.start_ck()


def install_task_scheduler():
    """Install CK watchdog as a Windows Task Scheduler task.
    Runs on user login. No admin required."""

    python_exe = sys.executable
    watchdog_script = os.path.abspath(__file__)

    # Task name
    task_name = "CK_Watchdog"

    # Create the task using schtasks
    cmd = (
        f'schtasks /create /tn "{task_name}" '
        f'/tr "\\\"{python_exe}\\\" \\\"{watchdog_script}\\\"" '
        f'/sc onlogon '
        f'/rl limited '
        f'/f'
    )

    log.info(f"Installing Windows Task: {task_name}")
    log.info(f"  Python: {python_exe}")
    log.info(f"  Script: {watchdog_script}")

    result = os.system(cmd)
    if result == 0:
        log.info(f"Task '{task_name}' installed successfully!")
        log.info("CK will auto-start on user login.")
    else:
        log.error(f"Failed to install task (exit code {result}).")
        log.info("Try running as administrator, or manually create the task:")
        log.info(f"  schtasks /create /tn {task_name} /tr \"{python_exe} {watchdog_script}\" /sc onlogon")


if __name__ == '__main__':
    if '--install' in sys.argv:
        install_task_scheduler()
    else:
        watchdog = CKWatchdog()
        watchdog.run()
