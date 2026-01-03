
import sys
import time
from pathlib import Path
import subprocess


print("updating .exe...")
if len(sys.argv) < 3:
    sys.exit(1)

old_exe = Path(sys.argv[1])
new_exe = Path(sys.argv[2])

time.sleep(1.5)

backup = old_exe.with_suffix(".old")

if backup.exists():
    backup.unlink()

old_exe.rename(backup)
new_exe.rename(old_exe)
old_exe.chmod(old_exe.stat().st_mode | 0o111)
subprocess.Popen(["./" + str(old_exe)])

