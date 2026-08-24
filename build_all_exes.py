import subprocess
import shutil
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

BASE = r"C:\Users\Dhairya Gadhavi\Documents\Sapphire"

def build_all():
    specs = [
        "sapphire.spec",
        "Emerald_Studio.spec",
        "sapphire_voice_tutor.spec",
        "Sapphire_Setup_Wizard.spec"
    ]
    
    for spec in specs:
        spec_path = os.path.join(BASE, spec)
        print(f"[*] Building {spec} with PyInstaller...")
        res = subprocess.run(["pyinstaller", "--noconfirm", "--distpath", BASE, spec_path], cwd=BASE)
        if res.returncode != 0:
            print(f"[ERROR] Failed building {spec}")
        else:
            print(f"[OK] Successfully built {spec}")
            
    # Also create aliases
    if os.path.exists(os.path.join(BASE, "Emerald_Studio.exe")):
        shutil.copy2(os.path.join(BASE, "Emerald_Studio.exe"), os.path.join(BASE, "emerald.exe"))
        print("[OK] Created alias: emerald.exe")
        
    if os.path.exists(os.path.join(BASE, "sapphire_voice_tutor.exe")):
        shutil.copy2(os.path.join(BASE, "sapphire_voice_tutor.exe"), os.path.join(BASE, "sapphire_tutor.exe"))
        print("[OK] Created alias: sapphire_tutor.exe")

if __name__ == "__main__":
    build_all()
