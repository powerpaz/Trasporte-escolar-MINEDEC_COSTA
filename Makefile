.PHONY: install run test stop check

PY=python3
PIP=pip3

install:
	@if [ -f requirements.txt ]; then \
		$(PIP) install -r requirements.txt; \
	else \
		$(PIP) install -r requirements.extra.txt; \
	fi
	@$(PIP) show Flask >/dev/null 2>&1 || $(PIP) install Flask==3.1.2
	@$(PIP) show pandas >/dev/null 2>&1 || $(PIP) install pandas==2.3.3

run:
	@nohup $(PY) app.py > server.log 2>&1 & \
	echo $$! > .flask.pid && echo "[INFO] Flask PID: $$(cat .flask.pid)"

test:
	@$(PY) test_server.py

stop:
	@bash stop.sh || true
	@rm -f .flask.pid || true
	@echo "[OK] stop"

check:
	@$(PY) csv_check.py ejemplo_rutas.csv