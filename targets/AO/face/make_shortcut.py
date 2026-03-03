# Copyright (c) 2025-2026 Brayden Sanders / 7Site LLC
# Licensed under the 7Site Human Use License v1.0
# See LICENSE file in project root for full terms.
#
# FREE for humans for personal/recreational use.
# NO commercial or government use without written agreement.

"""
make_shortcut.py -- Create desktop shortcut for AO

Run once: python make_shortcut.py
Creates AO.lnk on desktop with custom icon.
"""

import os
import sys
import subprocess
import tempfile
import struct


def generate_ico(path):
    """Generate a 16x16 .ico: green circle on dark blue."""
    W, H = 16, 16
    pixels = bytearray()
    for y in range(H):
        for x in range(W):
            dx, dy = x - 8, y - 8
            if dx * dx + dy * dy <= 36:
                pixels.extend([0x33, 0xcc, 0x33, 0xff])
            else:
                pixels.extend([0x2e, 0x1a, 0x1a, 0xff])
    pixel_data = bytes(pixels)
    bmp_header = struct.pack('<IiiHHIIiiII',
                             40, W, H * 2, 1, 32, 0, len(pixel_data), 0, 0, 0, 0)
    image_data = bmp_header + pixel_data
    ico_header = struct.pack('<HHH', 0, 1, 1)
    ico_entry = struct.pack('<BBBBHHII',
                            W, H, 0, 0, 1, 32, len(image_data), 6 + 16)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'wb') as f:
        f.write(ico_header + ico_entry + image_data)


def main():
    # OneDrive may redirect Desktop
    desktop = os.path.join(os.path.expanduser('~'), 'OneDrive', 'Desktop')
    if not os.path.isdir(desktop):
        desktop = os.path.join(os.path.expanduser('~'), 'Desktop')
    face_dir = os.path.dirname(os.path.abspath(__file__))
    script = os.path.join(face_dir, 'ao_face.pyw')
    ico_dir = os.path.join(os.path.expanduser('~'), '.ao')
    ico_path = os.path.join(ico_dir, 'ao.ico')

    # Find pythonw.exe
    python_dir = os.path.dirname(sys.executable)
    pythonw = os.path.join(python_dir, 'pythonw.exe')
    if not os.path.exists(pythonw):
        pythonw = sys.executable  # fallback

    # Generate icon
    generate_ico(ico_path)
    print(f'Icon: {ico_path}')

    # Create shortcut via VBScript
    lnk_path = os.path.join(desktop, 'AO.lnk')
    vbs = f'''Set ws = CreateObject("WScript.Shell")
Set sc = ws.CreateShortcut("{lnk_path}")
sc.TargetPath = "{pythonw}"
sc.Arguments = """{script}"""
sc.WorkingDirectory = "{face_dir}"
sc.IconLocation = "{ico_path}"
sc.Description = "AO -- Advanced Ollie"
sc.Save
'''
    vbs_path = os.path.join(tempfile.gettempdir(), '_ao_shortcut.vbs')
    with open(vbs_path, 'w') as f:
        f.write(vbs)

    try:
        subprocess.run(['cscript', '//nologo', vbs_path], check=True)
        os.remove(vbs_path)
        print(f'Shortcut: {lnk_path}')
        print('Done! Double-click AO on your desktop.')
    except Exception as e:
        os.remove(vbs_path)
        print(f'Error creating shortcut: {e}')
        print(f'You can manually create a shortcut to: {pythonw} "{script}"')


if __name__ == '__main__':
    main()
