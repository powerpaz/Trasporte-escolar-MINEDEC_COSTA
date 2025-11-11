#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Conversor de Excel a CSV para rutas de transporte escolar
Preserva caracteres especiales y valida estructura de datos
"""

import pandas as pd
import csv
import sys
import os
from pathlib import Path

def convert_excel_to_csv(input_file, output_file=None, encoding='utf-8'):
    """
    Convierte archivo Excel a CSV preservando caracteres especiales
    
    Soporta: .xls, .xlsx, .xlsm
    """
    if output_file is None:
        output_file = input_file.replace('.xls', '.csv').replace('.xlsx', '.csv')
    
    try:
        print(f"📂 Leyendo archivo: {input_file}")
        
        # Detectar tipo de archivo
        if input_file.endswith('.xls'):
            # Usar engine xlrd para .xls
            df = pd.read_excel(input_file, engine='xlrd')
        else:
            # Usar openpyxl para .xlsx y .xlsm
            df = pd.read_excel(input_file, engine='openpyxl')
        
        print(f"✓ Datos cargados: {len(df)} filas, {len(df.columns)} columnas")
        print(f"📋 Columnas detectadas: {', '.join(df.columns)}")
        
        # Guardar como CSV con UTF-8
        df.to_csv(output_file, index=False, encoding=encoding, quoting=csv.QUOTE_MINIMAL)
        
        print(f"✓ CSV creado: {output_file}")
        print(f"✓ Encoding: {encoding}")
        
        return output_file, df
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None, None

def validate_route_data(df):
    """
    Valida que el CSV tenga las columnas necesarias para rutas
    """
    required_columns = {
        'longitud_a': ['longitud_a', 'longitude_a', 'long_a', 'lng_a'],
        'latitud_a': ['latitud_a', 'latitude_a', 'lat_a'],
        'longitud_b': ['longitud_b', 'longitude_b', 'long_b', 'lng_b'],
        'latitud_b': ['latitud_b', 'latitude_b', 'lat_b'],
    }
    
    normalized_columns = {col.lower().replace(' ', '_'): col for col in df.columns}
    found = {}
    
    for key, alternatives in required_columns.items():
        for alt in alternatives:
            if alt in normalized_columns:
                found[key] = normalized_columns[alt]
                break
    
    if len(found) == 4:
        print(f"✓ Estructura válida para rutas")
        return True, found
    else:
        print(f"⚠️  Falta de columnas. Encontradas: {found}")
        return False, found

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python3 convert_excel_to_csv.py archivo.xls [output.csv]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    if not os.path.exists(input_file):
        print(f"❌ Archivo no encontrado: {input_file}")
        sys.exit(1)
    
    csv_file, df = convert_excel_to_csv(input_file, output_file)
    
    if df is not None:
        valid, columns = validate_route_data(df)
