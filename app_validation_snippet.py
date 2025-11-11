# --- SNIPPET: Validación robusta de CSV -------------------------------------
import re
import pandas as pd

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

def validate_csv_df(df: pd.DataFrame) -> tuple[pd.DataFrame, list]:
    """Normaliza columnas, valida requeridas y convierte lat/long a float.
    Devuelve (df_normalizado, errores) donde errores es lista de strings.
    """
    errors = []
    df = _normalize_cols(df)
    missing = [c for c in REQ_COLS if c not in df.columns]
    if missing:
        errors.append(f"Faltan columnas requeridas: {', '.join(missing)}")
        return df, errors

    for c in REQ_COLS:
        df[c] = df[c].map(_coerce_num)

    # Filas inválidas (coordenadas faltantes o no numéricas)
    mask_bad = df[REQ_COLS].isna().any(axis=1)
    bad_idx = df.index[mask_bad].tolist()
    if bad_idx:
        errors.append(f"{len(bad_idx)} filas con coordenadas inválidas: {bad_idx[:15]}...")
    return df, errors

# Ejemplo de uso dentro de tu endpoint /api/upload-csv:
# file = request.files.get('file')
# df = pd.read_csv(file, encoding='utf-8', dtype=str)
# df, errs = validate_csv_df(df)
# if errs:
#     return jsonify({'status':'error', 'errors': errs}), 400
# g.df_csv = df  # guardar en contexto si usas Flask g
# return jsonify({'status':'ok', 'rows': len(df)})
# -----------------------------------------------------------------------------