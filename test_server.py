#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Script de prueba para verificar endpoints básicos del servidor Flask.
# Requisitos:
#   - Servidor ejecutando en http://localhost:5000
#   - Archivo 'ejemplo_rutas.csv' presente en el directorio del proyecto

import os
import sys
import requests

BASE_URL = os.environ.get("BASE_URL", "http://localhost:5000")
CSV_PATH = os.environ.get("CSV_PATH", "ejemplo_rutas.csv")

def assert_status(resp, code=200, msg=""):
    if resp.status_code != code:
        raise AssertionError(f"{msg} (status={resp.status_code}, body={resp.text[:300]})")

def test_index():
    r = requests.get(BASE_URL, timeout=10)
    assert_status(r, 200, "Index debe responder 200 OK")

def test_upload_csv():
    if not os.path.exists(CSV_PATH):
        print(f"ADVERTENCIA: {CSV_PATH} no existe. Se omite prueba de carga CSV.")
        return
    files = {"file": (os.path.basename(CSV_PATH), open(CSV_PATH, "rb"), "text/csv")}
    r = requests.post(f"{BASE_URL}/api/upload-csv", files=files, timeout=20)
    assert_status(r, 200, "Upload CSV debe responder 200 OK")
    try:
        _ = r.json()
    except Exception as e:
        raise AssertionError(f"Respuesta de /api/upload-csv no es JSON válido: {e}")

def test_calculate_routes():
    payload = {}  # Ajusta si tu app requiere parámetros
    r = requests.post(f"{BASE_URL}/api/calculate-routes", json=payload, timeout=30)
    assert_status(r, 200, "Calculate routes debe responder 200 OK")
    try:
        _ = r.json()
    except Exception as e:
        raise AssertionError(f"Respuesta de /api/calculate-routes no es JSON válido: {e}")

if __name__ == "__main__":
    print("="*50)
    print("Ejecutando pruebas contra:", BASE_URL)
    ok = 0
    tests = [
        ("Index", test_index),
        ("Upload CSV", test_upload_csv),
        ("Calculate Routes", test_calculate_routes),
    ]
    for name, fn in tests:
        try:
            fn()
            print(f"✓ {name}")
            ok += 1
        except Exception as e:
            print(f"✗ {name}: {e}")
            sys.exit(1)
    print("-"*50)
    print(f"✓ All tests passed! ({ok}/{len(tests)})")
    print("="*50)
