pyinstaller --clean --onefile --name ciel-server-monitor run.py

New-Item -Force -Type Directory ./dist/assets
Copy-Item -Force -Recurse ./assets/* ./dist/assets

New-Item -Force -Type Directory ./dist/config
Copy-Item -Force -Recurse ./config/* ./dist/config

New-Item -Force -Type Directory ./dist/logs
New-Item -Force -Type Directory ./dist/logs/runtime