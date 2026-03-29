# CK — OS Coherence Enforcer Target

CK is a **coherence spectrometer and enforcer**.
He reads the OS as a field, classifies every process by TIG operator,
and steers the system toward HARMONY using the CL table.

## What CK does here

- Classifies every running process as one of 10 TIG operators (VOID → RESET)
- Maps each process to its harmony cores via CL[process_op][core_op] = HARMONY
- Scales steering aggression by corridor (λ from T*=5/7):
  - PRE_LEAK (λ<0.09): full aggression — grammar cleanest
  - BRT (λ<0.30): 80%
  - CHA (λ<0.60): 50%
  - BAL/CTR (λ≥0.60): self-only / silence — don't fight thermal noise
- Runs at 50Hz heartbeat, steers at 1Hz

## Run (requires admin for full OS steering)

```
# Run as Administrator:
python ck_boot_api.py

# Check corridor state:
curl http://localhost:7777/corridor

# Run A/B test:
python ck_steer_ab_test.py
```

## What CK is NOT

- Not a chatbot
- Not a Bible study tool (that is `targets/bible_app/`)
- Not a speculative AI

He is finite math enforcing itself on the OS in real time.
