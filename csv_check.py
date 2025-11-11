#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Validador de CSV para el Sistema de Rutas de Transporte Escolar.

Uso:
  python3 csv_check.py ejemplo_rutas.csv

Valida:
- Presencia de columnas requeridas (case-insensitive, espacios -> guiones bajos).
- Tipos numéricos en lat/long (permite coma/ punto y limpia espacios).
- Reporte de filas inválidas.
"""
import sys
import csv
import io
import re

REQ = ['longitud_a', 'latitud_a', 'longitud_b', 'latitud_b']

def normalize_header(h):
    return re.sub(r'\s+', '_', h.strip().lower())

def to_float(x):
    if x is None:
        return None
    s = str(x).strip()
    if not s:
        return None
    # Cambia coma por punto si viene con formato regional
    s = s.replace(',', '.')
    try:
        return float(s)
    except ValueError:
        return None

def main(path):
    # Intentar UTF-8 con fallback a latin-1
    encodings = ['utf-8', 'utf-8-sig', 'latin-1']
    last_err = None
    for enc in encodings:
        try:
            with io.open(path, 'r', encoding=enc, newline='') as f:
                reader = csv.reader(f)
                headers = next(reader)
                original_headers = headers[:]
                headers = [normalize_header(h) for h in headers]
                break
        except Exception as e:
            last_err = e
    else:
        print(f"[ERROR] No se pudo leer el CSV con codificaciones {encodings}: {last_err}")
        sys.exit(1)

    missing = [c for c in REQ if c not in headers]
    if missing:
        print("[ERROR] Faltan columnas requeridas:", ', '.join(missing))
        print("Cabeceras detectadas (normalizadas):", headers)
        print("Sugerencia: asegúrate de incluir exactamente:", ', '.join(REQ))
        sys.exit(2)

    idx = {h: headers.index(h) for h in REQ}
    invalid_rows = []
    total = 0
    with io.open(path, 'r', encoding=enc, newline='') as f:
        reader = csv.reader(f)
        _ = next(reader)  # skip header
        for i, row in enumerate(reader, start=2):  # línea 2 por cabecera
            total += 1
            la = to_float(row[idx['latitud_a']])
            loa = to_float(row[idx['longitud_a']])
            lb = to_float(row[idx['latitud_b']])
            lob = to_float(row[idx['longitud_b']])
            if None in (la, loa, lb, lob):
                invalid_rows.append(i)

    print(f"[OK] CSV leído correctamente con encoding '{enc}'. Filas de datos: {total}")
    if invalid_rows:
        print(f"[WARN] {len(invalid_rows)} filas con valores no numéricos en lat/long (líneas: {invalid_rows[:15]}...)" )
        sys.exit(3)
    else:
        print("[OK] Todas las filas tienen latitudes/longitudes numéricas.")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Uso: python3 csv_check.py <ruta_csv>")
        sys.exit(64)
    main(sys.argv[1])