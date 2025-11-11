#!/usr/bin/env bash
set -euo pipefail

# Intenta detener procesos Flask comunes
if pgrep -f "python3 app.py" >/dev/null 2>&1; then
  echo "[INFO] Stopping python3 app.py ..."
  pkill -f "python3 app.py" || true
fi

if pgrep -f "flask run" >/dev/null 2>&1; then
  echo "[INFO] Stopping 'flask run' ..."
  pkill -f "flask run" || true
fi

echo "[OK] Procesos Flask detenidos (si estaban activos)."