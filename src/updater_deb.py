
#!/usr/bin/env python3

import sys
import time
from pathlib import Path
import subprocess
import os

if len(sys.argv) < 3:
    sys.exit(1)

old_exe = Path(sys.argv[1]).resolve()
new_exe = Path(sys.argv[2]).resolve()

# wait for main app to fully exit
time.sleep(0.5)

backup = old_exe.with_suffix(".old")

if backup.exists():
    backup.unlink()

# replace binary
old_exe.rename(backup)
new_exe.rename(old_exe)

# ensure executable bit
old_exe.chmod(old_exe.stat().st_mode | 0o111)

# restart app
subprocess.Popen([str(old_exe)])
