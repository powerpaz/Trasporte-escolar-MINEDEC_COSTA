#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Aplicación Flask para gestión de rutas de transporte escolar
Integración con Leaflet y Mapbox para visualización de mapas
"""

from flask import Flask, render_template, request, jsonify, send_file
import pandas as pd
import json
import requests
import math
from datetime import datetime
import os
from pathlib import Path

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max

# Configuración de Mapbox (reemplaza con tu token)
MAPBOX_TOKEN = os.environ.get('MAPBOX_TOKEN', 'pk.eyJ1IjoiZXhhbXBsZSIsImEiOiJjbGV4YW1wbGUifQ.example')

# Almacenar rutas en memoria
routes_data = {}

def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calcula la distancia entre dos puntos usando la fórmula Haversine
    Retorna distancia en km
    """
    R = 6371  # Radio de la Tierra en km
    
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * \
        math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    
    c = 2 * math.asin(math.sqrt(a))
    return R * c

def estimate_travel_time(distance_km, speed_kmh=30):
    """
    Estima el tiempo de viaje basado en distancia y velocidad promedio
    Retorna tiempo en minutos
    """
    return round((distance_km / speed_kmh) * 60, 2)

def get_mapbox_route(lat1, lon1, lat2, lon2):
    """
    Obtiene la ruta desde Mapbox Directions API
    """
    try:
        url = f"https://api.mapbox.com/directions/v5/mapbox/driving/{lon1},{lat1};{lon2},{lat2}"
        params = {
            'access_token': MAPBOX_TOKEN,
            'geometries': 'geojson',
            'overview': 'full',
            'steps': True
        }
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data['routes']:
                route = data['routes'][0]
                return {
                    'geometry': route['geometry'],
                    'distance': route['distance'] / 1000,  # convertir a km
                    'duration': route['duration'] / 60,    # convertir a minutos
                    'steps': len(route['steps'])
                }
    except Exception as e:
        print(f"Error obteniendo ruta de Mapbox: {e}")
    
    return None

@app.route('/')
def index():
    return render_template('index.html', mapbox_token=MAPBOX_TOKEN)

@app.route('/api/upload-csv', methods=['POST'])
def upload_csv():
    """
    Carga un archivo CSV con datos de rutas
    """
    try:
        file = request.files['file']
        
        if not file or file.filename == '':
            return jsonify({'error': 'No se subió archivo'}), 400
        
        if not file.filename.endswith('.csv'):
            return jsonify({'error': 'Solo se aceptan archivos CSV'}), 400
        
        # Leer CSV preservando caracteres especiales
        df = pd.read_csv(file, encoding='utf-8')
        
        # Normalizar nombres de columnas
        df.columns = [col.lower().replace(' ', '_') for col in df.columns]
        
        # Validar columnas
        required = ['longitud_a', 'latitud_a', 'longitud_b', 'latitud_b']
        missing = [col for col in required if col not in df.columns]
        
        if missing:
            return jsonify({
                'error': f'Faltan columnas: {", ".join(missing)}',
                'encontradas': df.columns.tolist()
            }), 400
        
        # Almacenar datos
        routes_data['df'] = df
        routes_data['filename'] = file.filename
        
        return jsonify({
            'success': True,
            'rows': len(df),
            'columns': df.columns.tolist(),
            'preview': df.head().to_dict(orient='records')
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/calculate-routes', methods=['POST'])
def calculate_routes():
    """
    Calcula rutas con distancia, tiempo y accesibilidad
    """
    try:
        if 'df' not in routes_data:
            return jsonify({'error': 'No hay datos cargados'}), 400
        
        df = routes_data['df'].copy()
        routes = []
        
        for idx, row in df.iterrows():
            try:
                lat_a = float(row['latitud_a'])
                lon_a = float(row['longitud_a'])
                lat_b = float(row['latitud_b'])
                lon_b = float(row['longitud_b'])
                
                # Calcular distancia Haversine
                distance = haversine_distance(lat_a, lon_a, lat_b, lon_b)
                
                # Estimar tiempo
                travel_time = estimate_travel_time(distance)
                
                # Intentar obtener ruta de Mapbox
                mapbox_route = get_mapbox_route(lat_a, lon_a, lat_b, lon_b)
                
                if mapbox_route:
                    distance = mapbox_route['distance']
                    travel_time = mapbox_route['duration']
                    geometry = mapbox_route['geometry']
                else:
                    geometry = {
                        'type': 'LineString',
                        'coordinates': [[lon_a, lat_a], [lon_b, lat_b]]
                    }
                
                # Crear objeto de ruta
                route = {
                    'id': idx,
                    'origen': {
                        'latitud': lat_a,
                        'longitud': lon_a,
                        'nombre': row.get('nombre_origen', f'Origen {idx}')
                    },
                    'destino': {
                        'latitud': lat_b,
                        'longitud': lon_b,
                        'nombre': row.get('nombre_destino', f'Destino {idx}')
                    },
                    'distancia_km': round(distance, 2),
                    'tiempo_minutos': round(travel_time, 2),
                    'accesibilidad': row.get('accesibilidad', 'Estándar'),
                    'geometry': geometry,
                    'datos_adicionales': {col: row[col] for col in df.columns 
                                        if col not in ['latitud_a', 'longitud_a', 'latitud_b', 'longitud_b']}
                }
                
                routes.append(route)
            
            except Exception as e:
                print(f"Error procesando fila {idx}: {e}")
                continue
        
        routes_data['routes'] = routes
        
        return jsonify({
            'success': True,
            'total_rutas': len(routes),
            'rutas': routes
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/routes', methods=['GET'])
def get_routes():
    """
    Retorna las rutas calculadas
    """
    if 'routes' not in routes_data:
        return jsonify({'rutas': []}), 200
    
    return jsonify({'rutas': routes_data['routes']})

@app.route('/api/export-geojson', methods=['GET'])
def export_geojson():
    """
    Exporta las rutas como GeoJSON
    """
    try:
        if 'routes' not in routes_data:
            return jsonify({'error': 'No hay rutas para exportar'}), 400
        
        features = []
        for route in routes_data['routes']:
            feature = {
                'type': 'Feature',
                'geometry': route['geometry'],
                'properties': {
                    'id': route['id'],
                    'origen': route['origen']['nombre'],
                    'destino': route['destino']['nombre'],
                    'distancia_km': route['distancia_km'],
                    'tiempo_minutos': route['tiempo_minutos'],
                    'accesibilidad': route['accesibilidad']
                }
            }
            features.append(feature)
        
        geojson = {
            'type': 'FeatureCollection',
            'features': features,
            'fecha_exportacion': datetime.now().isoformat()
        }
        
        return jsonify(geojson)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/export-csv', methods=['GET'])
def export_csv():
    """
    Exporta las rutas calculadas como CSV
    """
    try:
        if 'routes' not in routes_data:
            return jsonify({'error': 'No hay rutas para exportar'}), 400
        
        export_data = []
        for route in routes_data['routes']:
            export_data.append({
                'ID': route['id'],
                'Origen': route['origen']['nombre'],
                'Origen_Latitud': route['origen']['latitud'],
                'Origen_Longitud': route['origen']['longitud'],
                'Destino': route['destino']['nombre'],
                'Destino_Latitud': route['destino']['latitud'],
                'Destino_Longitud': route['destino']['longitud'],
                'Distancia_km': route['distancia_km'],
                'Tiempo_minutos': route['tiempo_minutos'],
                'Accesibilidad': route['accesibilidad']
            })
        
        df = pd.DataFrame(export_data)
        csv_path = '/tmp/rutas_exportadas.csv'
        df.to_csv(csv_path, index=False, encoding='utf-8')
        
        return send_file(csv_path, mimetype='text/csv', 
                        as_attachment=True, 
                        download_name=f'rutas_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv')
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/map-screenshot', methods=['POST'])
def map_screenshot():
    """
    Prepara los datos para captura de pantalla del mapa
    Usa html2canvas en el frontend
    """
    try:
        if 'routes' not in routes_data:
            return jsonify({'error': 'No hay mapa para exportar'}), 400
        
        return jsonify({
            'success': True,
            'message': 'Use html2canvas en el navegador para capturar',
            'rutas_count': len(routes_data['routes'])
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Endpoint no encontrado'}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({'error': 'Error del servidor'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
