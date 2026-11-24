# -*- mode: python ; coding: utf-8 -*-

from pathlib import Path

block_cipher = None
PROJECT_ROOT = Path(SPECPATH).resolve()

a = Analysis(
    [str(PROJECT_ROOT / "stop_windows_update" / "main.py")],
    pathex=[str(PROJECT_ROOT)],
    binaries=[],
    datas=[],
    hiddenimports=[
        "win32timezone",
        "pywintypes",
        "win32service",
        "win32serviceutil",
        "win32event",
        "win32con",
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name="service_stop_windows_update",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)