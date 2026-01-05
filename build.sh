
#!/usr/bin/env bash
set -e

APP_NAME="ytdown"

echo "> Building $APP_NAME"

python3 -m pip install -r requirements.txt

rm -rf build dist

pyinstaller \
  --onedir \
  --name "$APP_NAME" \
  --clean \
  --add-data "version.json:." \
  --add-data "src/update:update" \
  --add-data "src/updater_deb.py:." \
  --add-data "src/updater.py:." \
  src/ytdown.py

echo "> Build finished: dist/$APP_NAME"

