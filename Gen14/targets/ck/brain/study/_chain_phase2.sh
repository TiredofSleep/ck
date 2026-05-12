#!/bin/bash
# Wait for current replay (PID 6433 / WINPID 29588) to finish, then launch Phase 2
echo "[chain] waiting for replay PID 6433 to exit..."
while ps -W 2>&1 | grep -q "29588"; do
  sleep 30
done
echo "[chain] replay done at $(date +%H:%M:%S); launching Phase 2 corpus..."
/c/ck_venv/lora312/Scripts/python.exe corpus_ingest.py --corpus phase2_corpus.json --replays 1 --delay 0.2 --log phase2_log.jsonl 2>&1
echo "[chain] Phase 2 finished at $(date +%H:%M:%S)"
