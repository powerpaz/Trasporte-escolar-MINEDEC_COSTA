#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# app.py — Sistema de Rutas de Transporte Escolar (Flask)
#
# Endpoints:
#   GET  /                      → página principal (templates/index.html)
#   POST /api/upload-csv        → carga y valida CSV (long/lat A/B)
#   POST /api/calculate-routes  → calcula distancias (haversine) y devuelve GeoJSON
#
# Requisitos: Flask, pandas

import os
import io
import math
import re
from typing import Tuple, List

from flask import Flask, render_template, request, jsonify
import pandas as pd

app = Flask(__name__)

# -----------------------------------------------------------------------------
# Validación de CSV
# -----------------------------------------------------------------------------
REQ_COLS = ['longitud_a', 'latitud_a', 'longitud_b', 'latitud_b']

def _normalize_cols(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [re.sub(r"\s+", "_", str(c).strip().lower()) for c in df.columns]
    return df

def _coerce_num(s):
    if pd.isna(s):
        return None
    v = str(s).strip()
    if v == '':
        return None
    v = v.replace(',', '.')
    try:
        return float(v)
    except ValueError:
        return None

def validate_csv_df(df: pd.DataFrame) -> Tuple[pd.DataFrame, List[str]]:
    """Normaliza columnas, valida requeridas y convierte lat/long a float.
    Devuelve (df_normalizado, errores).
    """
    errors: List[str] = []
    df = _normalize_cols(df)
    missing = [c for c in REQ_COLS if c not in df.columns]
    if missing:
        errors.append(f"Faltan columnas requeridas: {', '.join(missing)}")
        return df, errors

    # Convertir a float seguro
    for c in REQ_COLS:
        df[c] = df[c].map(_coerce_num)

    # Filas inválidas (coordenadas faltantes o no numéricas)
    mask_bad = df[REQ_COLS].isna().any(axis=1)
    bad_idx = df.index[mask_bad].tolist()
    if bad_idx:
        errors.append(f"{len(bad_idx)} filas con coordenadas inválidas (ej: {bad_idx[:15]}...)")
    return df, errors

# -----------------------------------------------------------------------------
# Cálculo de distancia (Haversine)
# -----------------------------------------------------------------------------
def haversine_km(lon1, lat1, lon2, lat2) -> float:
    R = 6371.0088  # Radio promedio de la Tierra en km
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

# -----------------------------------------------------------------------------
# Almacenamiento simple en memoria (para demo/sesión única)
# -----------------------------------------------------------------------------
DF_STORE = {
    "df": None
}

# -----------------------------------------------------------------------------
# Rutas
# -----------------------------------------------------------------------------
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

@app.route("/api/upload-csv", methods=["POST"])
def upload_csv():
    if 'file' not in request.files:
        return jsonify({"status": "error", "error": "No se encontró archivo en el formulario (clave 'file')."}), 400

    f = request.files['file']
    if not f or f.filename == "":
        return jsonify({"status": "error", "error": "Archivo no proporcionado."}), 400

    # Intentar múltiples codificaciones
    encodings = ["utf-8", "utf-8-sig", "latin-1"]
    last_exc = None
    for enc in encodings:
        try:
            f.stream.seek(0)
            df = pd.read_csv(io.TextIOWrapper(f.stream, encoding=enc), dtype=str)
            df, errs = validate_csv_df(df)
            if errs:
                return jsonify({"status": "error", "errors": errs}), 400
            DF_STORE["df"] = df
            return jsonify({"status": "ok", "rows": int(len(df))})
        except Exception as e:
            last_exc = str(e)
            continue

    return jsonify({"status": "error", "error": f"No se pudo leer el CSV. Último error: {last_exc}"}), 400

@app.route("/api/calculate-routes", methods=["POST"])
def calculate_routes():
    df = DF_STORE.get("df")
    if df is None or df.empty:
        return jsonify({"status": "error", "error": "No hay datos cargados. Sube un CSV primero en /api/upload-csv."}), 400

    # Opcional: limitar cantidad de rutas para pruebas
    try:
        body = request.get_json(silent=True) or {}
    except Exception:
        body = {}
    limit = body.get("limit")
    if isinstance(limit, int) and limit > 0:
        df_calc = df.head(limit).copy()
    else:
        df_calc = df.copy()

    # Calcular distancia por fila
    dists = []
    for _, r in df_calc.iterrows():
        lon1 = float(r["longitud_a"])
        lat1 = float(r["latitud_a"])
        lon2 = float(r["longitud_b"])
        lat2 = float(r["latitud_b"])
        d_km = haversine_km(lon1, lat1, lon2, lat2)
        dists.append(d_km)
    df_calc["dist_km"] = dists

    total_km = float(sum(dists))
    total_routes = int(len(df_calc))

    # Construir GeoJSON mínimo de LineString
    features = []
    for _, r in df_calc.iterrows():
        features.append({
            "type": "Feature",
            "properties": {
                "dist_km": float(r["dist_km"])
            },
            "geometry": {
                "type": "LineString",
                "coordinates": [
                    [float(r["longitud_a"]), float(r["latitud_a"])],
                    [float(r["longitud_b"]), float(r["latitud_b"])]
                ]
            }
        })

    geojson = {
        "type": "FeatureCollection",
        "features": features
    }

    return jsonify({
        "status": "ok",
        "summary": {
            "total_routes": total_routes,
            "total_km": total_km
        },
        "geojson": geojson
    })

# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=True)