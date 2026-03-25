# CK Force9 Display Driver

Windows Indirect Display Driver (IDD) with TIG Force9 3-shell CIELAB compression.
127x compression at dE=1.03 (imperceptible quality loss).

## What it does

Creates a virtual monitor that Windows treats as a real display.
Apps render to it normally. The driver captures every frame,
compresses with Force9 (127x), and sends via named pipe to
the CK streaming server.

## Architecture

1. Windows renders to virtual monitor
2. IDD captures DirectX surface
3. GPU copy to staging texture
4. Map to CPU memory (BGRA pixels)
5. Force9 3-shell CIELAB encode (RGB -> Lab -> shells)
6. RLE compress per shell
7. Send via named pipe \.\pipe\CKForce9
8. CK streaming server receives and distributes

## Build

Requires:
- Visual Studio 2022
- Windows Driver Kit (WDK) with UMDF support
- WDK VS integration (via VS Installer > Individual Components)

```
msbuild IddSampleDriver.vcxproj /p:Configuration=Release /p:Platform=x64 /p:SpectreMitigation=false
```

## Install

1. Enable test signing: `bcdedit /set testsigning on` (reboot)
2. Run IddSampleApp to create virtual monitor
3. The driver loads and starts capturing

## Pre-built

`IddSampleDriver.dll` is included pre-built for x64.

## Named Pipe Protocol

Pipe: `\.\pipe\CKForce9`

Per frame:
- 4 bytes: width (uint32)
- 4 bytes: height (uint32)
- 4 bytes: compressed_size (uint32)
- N bytes: Force9 compressed data

## Files

- `Driver.cpp` - IDD driver with Force9 frame capture
- `Driver.h` - Driver header with staging texture members
- `Force9Encoder.h` - C++ Force9 3-shell CIELAB encoder
- `IddSampleDriver.dll` - Pre-built driver (x64 Release)
- `IddSampleDriver.inf` - Driver installation manifest
- `IddSampleDriver.vcxproj` - Visual Studio project

(c) 2026 Brayden Sanders / 7Site LLC -- TIG Unified Theory
Based on Microsoft IDD Sample (MIT License)
