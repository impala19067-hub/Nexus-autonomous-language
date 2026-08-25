# -*- mode: python ; coding: utf-8 -*-

datas_list = [
    # Core stdlib folder
    ('sapphire_lang', 'sapphire_lang'),
    
    # Standalone Compiled Executables
    ('sapphire.exe', '.'),
    ('emerald.exe', '.'),
    ('Emerald_Studio.exe', '.'),
    ('Sapphire_Compiler.exe', '.'),
    ('compiler.exe', '.'),
    ('sapphire_voice_tutor.exe', '.'),
    ('sapphire_tutor.exe', '.'),
    ('uninstall.exe', '.'),
    ('uninstall_sapphire.exe', '.'),

    # Python Scripts & Launchers
    ('emerald_studio.py', '.'),
    ('sapphire_studio.py', '.'),
    ('sapphire_compiler.py', '.'),
    ('sapphire_cli.py', '.'),
    ('sapphire_voice_tutor.py', '.'),
    ('sapphire_tutor.py', '.'),
    ('uninstall_sapphire.py', '.'),
    ('install_sapphire.bat', '.'),

    # All 5 PDF Manuals
    ('Sapphire_Coding_and_Usage_Guide.pdf', '.'),
    ('Building_Advanced_Autonomous_AI.pdf', '.'),
    ('Sapphire_Autonomy_and_Performance_Benchmarks.pdf', '.'),
    ('Beginners_Guide_Your_First_Autonomous_AI.pdf', '.'),
    ('Sapphire_Language_Specification_and_Automation_Manual.pdf', '.'),
    ('INSTALLATION_AND_USAGE_GUIDE.md', '.'),
    ('README.md', '.'),
]

a = Analysis(
    ['sapphire_setup_wizard.py'],
    pathex=[],
    binaries=[],
    datas=datas_list,
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
