# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['sapphire_setup_wizard.py'],
    pathex=[],
    binaries=[],
    datas=[('sapphire_lang', 'sapphire_lang'), ('emerald_studio.py', '.'), ('sapphire_studio.py', '.'), ('docs/Sapphire_Coding_and_Usage_Guide.pdf', '.'), ('docs/Building_Advanced_Autonomous_AI.pdf', '.'), ('docs/Sapphire_Autonomy_and_Performance_Benchmarks.pdf', '.'), ('docs/Beginners_Guide_Your_First_Autonomous_AI.pdf', '.'), ('INSTALLATION_AND_USAGE_GUIDE.md', '.')],
    hiddenimports=['pyttsx3.drivers.sapi5', 'win32com', 'comtypes'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Sapphire_Setup_Wizard',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
