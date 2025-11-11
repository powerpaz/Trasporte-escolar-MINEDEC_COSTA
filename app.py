#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, io, math, re
from typing import Tuple, List
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
# Permite llamadas desde dominios externos (GitHub Pages)
CORS(app, resources={r"/api/*": {"origins": "*"}})

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
    errors: List[str] = []
    df = _normalize_cols(df)
    missing = [c for c in REQ_COLS if c not in df.columns]
    if missing:
        errors.append(f"Faltan columnas requeridas: {', '.join(missing)}")
        return df, errors
    for c in REQ_COLS:
        df[c] = df[c].map(_coerce_num)
    mask_bad = df[REQ_COLS].isna().any(axis=1)
    bad_idx = df.index[mask_bad].tolist()
    if bad_idx:
        errors.append(f"{len(bad_idx)} filas con coordenadas inválidas (ej: {bad_idx[:15]}...)")
    return df, errors

def haversine_km(lon1, lat1, lon2, lat2) -> float:
    R = 6371.0088
    phi1 = math.radians(lat1); phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

DF_STORE = {"df": None}

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

@app.route("/api/upload-csv", methods=["POST"])
def upload_csv():
    if 'file' not in request.files:
        return jsonify({"status": "error", "error": "No se encontró archivo (clave 'file')."}), 400
    f = request.files['file']
    if not f or f.filename == "":
        return jsonify({"status": "error", "error": "Archivo no proporcionado."}), 400
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
        return jsonify({"status": "error", "error": "No hay datos cargados. Sube un CSV primero."}), 400
    body = request.get_json(silent=True) or {}
    limit = body.get("limit")
    df_calc = df.head(limit).copy() if isinstance(limit, int) and limit > 0 else df.copy()
    dists = []
    for _, r in df_calc.iterrows():
        d_km = haversine_km(float(r["longitud_a"]), float(r["latitud_a"]),
                            float(r["longitud_b"]), float(r["latitud_b"]))
        dists.append(d_km)
    df_calc["dist_km"] = dists
    total_km = float(sum(dists)); total_routes = int(len(df_calc))
    features = []
    for _, r in df_calc.iterrows():
        features.append({
            "type": "Feature",
            "properties": {"dist_km": float(r["dist_km"])},
            "geometry": {
                "type": "LineString",
                "coordinates": [
                    [float(r["longitud_a"]), float(r["latitud_a"])],
                    [float(r["longitud_b"]), float(r["latitud_b"])]
                ]
            }
        })
    return jsonify({
        "status": "ok",
        "summary": {"total_routes": total_routes, "total_km": total_km},
        "geojson": {"type": "FeatureCollection", "features": features}
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=False)