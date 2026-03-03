# HP Desktop -- Engineer Notes

Technical deployment notes for CK on the HP 2-core tower.

---

## HPTowerBody Class

Defined in `ck_sim/ck_body_interface.py` (line 322).

`HPTowerBody` extends `CKBody` and represents the HP desktop hardware.
It is registered in `BODY_REGISTRY` under the key `'hp'`.

### PlatformSpec

```python
PlatformSpec(
    name="HP-Tower",
    cpu_cores=2,
    cpu_mhz=3200,
    ram_mb=8192,
    capabilities=[
        Capability.HEAR,     # Microphone input
        Capability.SPEAK,    # Audio output (speaker/DAC)
        Capability.SEE,      # Webcam
        Capability.SHOW,     # Monitor (Kivy display)
        Capability.THINK,    # Compute (2-core CPU)
        Capability.CONNECT,  # Network (WiFi/Ethernet)
    ],
    audio_sample_rate=44100,
    display_width=1920,
    display_height=1080,
    tick_hz=50,
    tick_budget_ms=20.0,
)
```

### Capabilities Breakdown

| Capability | IntEnum Value | HP Hardware | Notes |
|-----------|---------------|-------------|-------|
| HEAR | 0 | Built-in or USB mic | Active via sounddevice |
| SPEAK | 1 | Speakers/headphones | Active via sounddevice |
| SEE | 2 | USB webcam | Declared, not yet wired |
| SHOW | 5 | Monitor (1920x1080) | Kivy dashboard + chat |
| THINK | 6 | 2-core Intel @ 3.2 GHz | 50Hz engine loop |
| CONNECT | 7 | Network adapter | Available but CK runs local |

Note: `MOVE` (3) and `FEEL` (4) are NOT present -- the HP tower has no motors,
no IMU, no accelerometer. This is a stationary body.

### Methods

- `sense()` -> Returns `_sensors` dict with `mic_rms` and `mic_operator` keys
- `express(commands)` -> Currently a no-op (pass); audio output is handled by the engine's audio pipeline, not by the body directly
- `start()` -> Prints startup message
- `stop()` -> Prints shutdown message
- `update_sensors(mic_rms, mic_operator, **kwargs)` -> Called by engine each tick to feed sensor data from the audio pipeline

### BTQ Constraints

`HPTowerBody` does not override `get_btq_constraints()`, so it uses the base
`CKBody` defaults:

```python
{
    'max_velocity': 3.0,
    'max_accel': 15.0,
    'max_jerk': 100.0,
    'max_torque': 1.0,      # No motors, but BTQ still checks bounds
    'max_energy_per_cycle': 3.0,
    'tick_budget_ms': 20.0,
}
```

Since the HP tower has no actuators, the velocity/accel/jerk/torque limits are
irrelevant for motor safety but still constrain the internal operator velocity
in the BTQ B-block. This prevents CK from "thinking too fast" even on a
stationary platform.

---

## Platform Auto-Detection

Defined in `ck_body_interface.py`, function `detect_platform()`.

Detection logic for the HP tower:

```python
system = platform.system().lower()  # 'windows'
cpu_count = os.cpu_count()           # 2

if system == 'windows':
    if cpu_count <= 4:
        return 'hp'       # <-- HP Tower matched
    return 'r16'           # 16-core Ryzen
```

The heuristic: on Windows, 4 or fewer logical cores maps to `'hp'`.
More than 4 cores maps to `'r16'` (the 16-core Ryzen development PC).

This means any Windows machine with 1-4 cores will get the HP body.
If the user has a different low-core Windows machine, they can override
by passing `platform='sim'` or another key to `create_body()`.

---

## DeploymentConfig

Defined in `ck_sim/ck_deploy.py`. The HP deployment is registered under key `'hp'`:

```python
DeploymentConfig(
    name="HP 2-Core Tower",
    platform_key="hp",
    description=(
        "Older HP tower. 2-core Intel, 8GB RAM. "
        "Screen, speakers, mic, webcam. Tighter tick budget."
    ),
    btq_w_out=0.5,
    btq_w_in=0.5,
    btq_candidates=8,          # Fewer candidates for 2-core (R16 uses 16)
    health_window=50,           # Smaller health window (R16 uses 100)
    tick_hz=50,
    max_crystals=5000,          # Half of R16's 10,000
    audio_sample_rate=44100,
)
```

### Key Tuning Differences vs R16

| Parameter | HP Tower | R16 PC | Reason |
|-----------|----------|--------|--------|
| btq_candidates | 8 | 16 | Fewer candidates reduces BTQ compute per decision |
| health_window | 50 | 100 | Smaller window = faster health response, less memory |
| max_crystals | 5,000 | 10,000 | Half the crystal budget for 8GB RAM |
| btq_decision_hz | 5 | 5 | Same decision rate (5 decisions/sec) |
| btq_w_out / btq_w_in | 0.5 / 0.5 | 0.5 / 0.5 | Balanced safety/curiosity on both |

The HP deployment is intentionally conservative. With only 2 cores and 8GB RAM,
the crystal budget and candidate count are halved to stay within the tick budget.

---

## Tick Budget Analysis

- **Tick rate**: 50 Hz = 20 ms per tick
- **Measured throughput**: 5,652 Hz on the HP tower (from engine benchmark)
- **Headroom**: 5,652 / 50 = **112x headroom** over the 50Hz target
- **Per-tick time**: 1000 / 5652 = **0.177 ms** actual compute per tick
- **Budget used**: 0.177 / 20.0 = **0.88%** of the 20 ms budget

This means CK uses less than 1% of available compute on the HP tower.
The remaining 99% is available for:
- Kivy rendering (Core 0)
- Audio I/O (sounddevice runs in its own thread)
- Future webcam processing
- OS overhead

Even with the webcam stream active (estimated 2-5 ms per frame for D2 on
color histograms), the tick budget has enormous room.

---

## Audio Pipeline

The full audio path on the HP desktop:

```
Physical mic
    |
    v
sounddevice (44100 Hz, mono, float32 buffer)
    |
    v
RMS calculation (root-mean-square of audio chunk)
    |
    v
D2 curvature analysis (second derivative on RMS envelope)
    |
    v
Operator classification (D2 value -> one of 9 CL operators)
    |
    v
update_sensors(mic_rms=rms, mic_operator=op)
    |
    v
Engine tick: operator enters coherence field
    |
    v
BTQ evaluates: audio operator joins heartbeat + text streams
    |
    v
express() -> audio_op tone played through speakers
```

### Audio Details

- **Sample rate**: 44,100 Hz (CD quality)
- **Channels**: 1 (mono)
- **Buffer**: Float32, processed in chunks by sounddevice callback
- **D2 pipeline**: Same curvature math used on text, applied to audio amplitude envelope
- **Operator mapping**: D2 values map to the 9 CL operators (0-8), which are the same operators used for text and heartbeat -- unified algebra across all modalities

---

## Future Webcam Integration

The `HPTowerBody` declares `Capability.SEE` but the vision stream is not yet
connected. The planned integration:

### Architecture

```
USB Webcam
    |
    v
OpenCV VideoCapture (640x480 or 1280x720)
    |
    v
Frame grab (every N ticks, not every tick)
    |
    v
Color histogram computation (per-block or full-frame)
    |
    v
D2 curvature on histogram deltas (frame-to-frame change)
    |
    v
Operator classification (same 9 CL operators)
    |
    v
update_sensors(camera_operator=op, camera_motion=delta)
    |
    v
Coherence field: 4th stream (heartbeat + audio + text + vision)
```

### Design Notes

- Frame grab should NOT happen every tick (50 fps is unnecessary and expensive).
  Target: 5-10 fps for vision operators, decimated from the camera's native rate.
- D2 on color histograms captures "visual change" without any neural network.
  A sudden shift in color distribution = high curvature = operator change.
- The coherence field currently merges 3 streams. Adding vision makes it 4.
  The field equations are already N-stream capable.
- OpenCV is the only new dependency. Everything else uses existing CK math.

### Estimated Compute Cost

- OpenCV frame grab: < 1 ms
- Color histogram: < 0.5 ms
- D2 + operator classification: < 0.1 ms
- Total per vision tick: ~1.5 ms (well within the 20 ms budget)

---

## Body E/A/K Mapping

CK's internal state tracks three quantities from TIG:
- **E** (Energy): How much is happening
- **A** (Alignment): How coherent is the activity
- **K** (Curvature): How fast things are changing

On a desktop (no motors, no battery), these map differently than on a robot:

| Quantity | Robot (Dog) | Desktop (HP) |
|----------|-------------|--------------|
| E (Energy) | Battery level + motor current | CPU load (os.cpu_percent or tick time) |
| A (Alignment) | IMU orientation stability | Mic input level (how much CK is "attending") |
| K (Curvature) | Joint velocity, gait phase | Session duration / conversation turn rate |

### Desktop-Specific Interpretation

- **E from CPU load**: On the HP tower, E reflects computational effort. High E
  means many crystals forming, heavy BTQ evaluation, audio + display active.
  Low E means idle heartbeat only. This replaces battery/motor energy on robots.

- **A from mic input**: Alignment measures how much CK is engaged with input.
  Active microphone with speech = high A (CK is "listening"). Silence = low A.
  On a robot, this would come from IMU stability (body is balanced).

- **K from session duration**: Curvature measures the rate of change over time.
  Early in a session, K is high (everything is new). As the session continues
  and patterns stabilize, K decreases. Conversation turn rate modulates this:
  rapid back-and-forth = high K, long pauses = K decay.

### No Motors, No Battery

The HP body has no `MOVE` or `FEEL` capabilities. This means:
- `n_motors = 0`, `motor_max_torque = 0.0`
- `has_battery = False`, `battery_wh = 0.0`
- BTQ motor-safety constraints are present but inert (no actuators to constrain)
- The dog's locomotion domain is absent; only memory and bio domains are active

---

## 2-Core Pinning Strategy

The HP tower has exactly 2 logical cores. The deployment strategy:

| Core | Affinity Mask | Role |
|------|--------------|------|
| Core 0 | 0x1 | Windows OS + Kivy display + audio I/O |
| Core 1 | 0x2 | CK engine (50Hz tick + BTQ + operator streams) |

To pin CK to Core 1:
```
start /affinity 2 python -m ck_sim
```

The `/affinity 2` flag sets the affinity mask to binary `10`, which is Core 1.

### Why Pin?

On a 2-core machine, Windows scheduler can bounce CK between cores, causing
cache misses and jitter. Pinning CK to Core 1 gives it a dedicated core while
Windows and Kivy share Core 0. This reduces tick jitter and improves coherence
field stability.

### Current Reality

Without pinning, CK still runs fine. The 112x headroom means even with scheduler
jitter, CK never misses a tick. Pinning is an optimization for the future when
the webcam stream and more complex BTQ decisions consume more of the budget.

---

## File References

- Body class: `ck_sim/ck_body_interface.py` -> `HPTowerBody` (line 322)
- Deployment config: `ck_sim/ck_deploy.py` -> `DEPLOYMENTS['hp']` (line 106)
- Auto-detection: `ck_sim/ck_body_interface.py` -> `detect_platform()` (line 434)
- Capability enum: `ck_sim/ck_body_interface.py` -> `Capability` (line 37)
- PlatformSpec: `ck_sim/ck_body_interface.py` -> `PlatformSpec` (line 54)
- Body registry: `ck_sim/ck_body_interface.py` -> `BODY_REGISTRY` (line 414)

---

*(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory*
