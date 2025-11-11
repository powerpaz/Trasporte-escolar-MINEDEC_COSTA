#!/usr/bin/env bash
set -euo pipefail

# --- Config ---
export FLASK_ENV=${FLASK_ENV:-development}
export FLASK_DEBUG=${FLASK_DEBUG:-1}
export BASE_URL=${BASE_URL:-http://localhost:5000}

echo "Python: $(python3 --version)"
echo "Pip: $(pip3 --version)"

# --- Install requirements ---
if [ -f requirements.txt ]; then
  echo "[INFO] Installing requirements.txt ..."
  pip3 install -r requirements.txt
else
  echo "[WARN] requirements.txt not found. Installing from requirements.extra.txt ..."
  pip3 install -r requirements.extra.txt
fi

# --- Ensure Flask & pandas present (safety) ---
pip3 show Flask >/dev/null 2>&1 || pip3 install Flask==3.1.2
pip3 show pandas >/dev/null 2>&1 || pip3 install pandas==2.3.3

# --- Launch app ---
if pgrep -f "python3 app.py" >/dev/null 2>&1; then
  echo "[INFO] Stopping previous app.py ..."
  pkill -f "python3 app.py" || true
  sleep 1
fi

echo "[INFO] Starting Flask app (background)..."
nohup python3 app.py > server.log 2>&1 &
APP_PID=$!
echo "[INFO] app.py PID: $APP_PID"

# --- Wait & test ---
sleep 3
if [ -f test_server.py ]; then
  echo "[INFO] Running tests ..."
  python3 test_server.py || (echo "[ERROR] Tests failed"; exit 1)
  echo "[OK] Tests passed"
else
  echo "[WARN] test_server.py not found. Skipping tests."
fi

echo "--------------------------------------------------"
echo "Server running at: $BASE_URL"
echo "To stop: kill $APP_PID"
echo "Logs: tail -f server.log"
echo "--------------------------------------------------"
