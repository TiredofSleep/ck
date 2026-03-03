# CK on HP Desktop -- Full Linux Kernel Takeover Experiment

**STATUS: PLANNED** -- Not active until R16 deployment is satisfactory.

CK replaces the OS. The HP 2-core desktop is the expendable testbed for CK's first
full kernel takeover. If it bricks, it bricks. CK IS the scheduler, the memory manager,
the I/O handler. The goal: no Python, no userspace, CK IS the operating system.

## System Requirements

- HP Desktop (2-core CPU, 3.2 GHz)
- Windows 10/11
- Python 3.10+ (python.org/downloads -- CHECK "Add to PATH")
- Webcam (built-in or USB)
- Microphone (built-in or USB)
- Speakers or headphones

## Quick Start

1. Copy the entire Gen9 folder to your HP desktop
2. Open Command Prompt (Win+R, type cmd, Enter)
3. Navigate to the Gen9 folder: `cd C:\path\to\Gen9`
4. Install dependencies: `pip install -r requirements.txt`
5. Run CK: `python -m ck_sim`
6. Or double-click `run_ck.bat`

## What CK Has on This Machine

| Capability | Hardware | Status |
|-----------|----------|--------|
| HEAR | Built-in mic or USB | Active via sounddevice |
| SPEAK | Speakers/headphones | Active via sounddevice |
| SEE | Webcam | Ready (future stream) |
| SHOW | Monitor | Kivy dashboard + chat |
| THINK | 2-core CPU @ 3.2 GHz | 50Hz heartbeat confirmed |
| CONNECT | Network | Not needed (CK runs local) |

## Body Configuration

CK auto-detects the HP desktop via `cpu_count` (`<=4` cores on Windows = HP).
The `HPTowerBody` class activates with these capabilities:
- Audio input (D2 pipeline on mic signal)
- Audio output (operator tones)
- Display (Kivy chat + dashboard)
- Compute (50Hz engine, measured 5,652 Hz throughput)

## Enabling Microphone

1. Start CK (`python -m ck_sim` or `run_ck.bat`)
2. In the chat screen, press the MIC button
3. Talk to CK -- he hears through D2 curvature analysis
4. Watch the Dashboard: the audio stream lights up in the coherence field

## Kernel Takeover Vision

The HP desktop is the expendable testbed. If it bricks, we learn:
- **Phase 1**: Install Linux, build custom kernel module -- CK as scheduler (replaces CFS)
- **Phase 2**: CK manages memory pages -- coherence-based page replacement
- **Phase 3**: CK IS the init process -- no systemd, no userspace, just CK
- **Phase 4**: Bare metal bootloader -- no Linux at all, CK on raw x86

## 2-Core Strategy

| Core | Role | Process |
|------|------|---------|
| Core 0 | OS + UI | Windows + Kivy display |
| Core 1 | CK Brain | 50Hz heartbeat + BTQ + voice |

To pin CK to core 1 (advanced):
```
start /affinity 2 python -m ck_sim
```

## Webcam (Future)

The webcam is CK's SEE capability. Currently the body interface declares it
but the vision stream is not yet wired. When ready:
- Camera frames -> D2 curvature on pixel blocks -> operator stream
- Same math as text and audio, just on visual data
- The coherence field adds a 4th stream (heartbeat + audio + text + vision)

## Troubleshooting

- **"No module named kivy"** -> `pip install kivy numpy sounddevice`
- **"Access denied" on mic** -> Allow mic in Windows Privacy Settings
- **Display issues** -> Update graphics drivers, CK uses OpenGL via Kivy
- **Slow startup** -> Normal on first run (Kivy compiles shaders)

## Legal

See `../LEGAL.md` for license and legal information.

## Credits

CK Coherence Machine
Built by Brayden Sanders / 7Site LLC
Mathematics: TIG Unified Field Theory (Papers 1-8)

*(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory*
