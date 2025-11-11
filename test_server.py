#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de prueba para verificar la funcionalidad del servidor
"""

import requests
import os
import sys

# Configurar base URL
BASE_URL = "http://localhost:5000"

def test_index():
    """Prueba que el índice carga correctamente"""
    try:
        response = requests.get(BASE_URL)
        if response.status_code == 200:
            print("✓ Index page loads successfully")
            return True
        else:
            print(f"✗ Index page failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("✗ Cannot connect to server. Make sure Flask is running on port 5000")
        return False

def test_upload_csv():
    """Prueba la carga de CSV"""
    csv_path = "ejemplo_rutas.csv"

    if not os.path.exists(csv_path):
        print(f"✗ CSV file not found: {csv_path}")
        return False

    try:
        with open(csv_path, 'rb') as f:
            files = {'file': (csv_path, f, 'text/csv')}
            response = requests.post(f"{BASE_URL}/api/upload-csv", files=files)

        if response.status_code == 200:
            data = response.json()
            print(f"✓ CSV uploaded successfully: {data.get('rows', 0)} rows")
            return True
        else:
            data = response.json()
            print(f"✗ CSV upload failed: {data.get('error', 'Unknown error')}")
            return False
    except Exception as e:
        print(f"✗ Exception during CSV upload: {e}")
        return False

def test_calculate_routes():
    """Prueba el cálculo de rutas"""
    try:
        response = requests.post(f"{BASE_URL}/api/calculate-routes")

        if response.status_code == 200:
            data = response.json()
            print(f"✓ Routes calculated successfully: {data.get('total_rutas', 0)} routes")
            return True
        else:
            data = response.json()
            print(f"✗ Route calculation failed: {data.get('error', 'Unknown error')}")
            return False
    except Exception as e:
        print(f"✗ Exception during route calculation: {e}")
        return False

def main():
    print("=" * 50)
    print("Testing Transport Route System")
    print("=" * 50)
    print()

    # Test 1: Index page
    print("[1/3] Testing index page...")
    if not test_index():
        print("\nServer is not running. Start it with: python3 app.py")
        sys.exit(1)
    print()

    # Test 2: CSV Upload
    print("[2/3] Testing CSV upload...")
    if not test_upload_csv():
        print("\nCSV upload failed")
        sys.exit(1)
    print()

    # Test 3: Calculate routes
    print("[3/3] Testing route calculation...")
    if not test_calculate_routes():
        print("\nRoute calculation failed")
        sys.exit(1)
    print()

    print("=" * 50)
    print("✓ All tests passed!")
    print("=" * 50)

if __name__ == "__main__":
    main()
