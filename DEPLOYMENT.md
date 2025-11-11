# 🔧 Guía de Configuración Avanzada

## Configuración de Mapbox (Recomendado)

### Paso 1: Crear cuenta en Mapbox

1. Ir a https://account.mapbox.com/auth/signup/
2. Registrarse con email
3. Verificar email
4. Acceder al dashboard

### Paso 2: Obtener token

1. En el dashboard, ir a "Tokens"
2. Click en "Create a token"
3. Asignar nombre: "rutas-escolar"
4. Escoger permisos: Direcciones, Estilos, Hosting
5. Click "Create token"
6. Copiar el token

### Paso 3: Configurar en la aplicación

**Opción A: Variables de entorno (.env)**
```bash
# Crear archivo .env
echo "MAPBOX_TOKEN=pk.eyJ1IjoieWslYWNjIiwgImEiOiJjbGV4YW1wbGUifQ.example" > .env
```

**Opción B: Archivo de configuración**
En `app.py`, línea 16:
```python
MAPBOX_TOKEN = 'pk.eyJ1IjoieXsuYWNjIiwgImEiOiJjbGV4YW1wbGUifQ.example'
```

**Opción C: Parámetro al iniciar**
```bash
MAPBOX_TOKEN=tu_token python3 app.py
```

## Desplegar en Producción

### Opción 1: Heroku

```bash
# 1. Crear cuenta en heroku.com
# 2. Instalar CLI
curl https://cli-assets.heroku.com/install.sh | sh

# 3. Login
heroku login

# 4. Crear app
heroku create mi-rutas-escolar

# 5. Agregar token
heroku config:set MAPBOX_TOKEN=tu_token_aqui

# 6. Desplegar
git push heroku main

# 7. Ver logs
heroku logs --tail
```

### Opción 2: AWS Lambda

Requiere:
- Serverless Framework
- AWS CLI configurado

```bash
# Instalar Serverless
npm install -g serverless

# Empaquetar
serverless package --function app

# Desplegar
serverless deploy
```

### Opción 3: Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=app.py
ENV MAPBOX_TOKEN=${MAPBOX_TOKEN}

EXPOSE 5000

CMD ["python", "app.py"]
```

**Construir imagen:**
```bash
docker build -t rutas-escolar .
docker run -p 5000:5000 -e MAPBOX_TOKEN=tu_token rutas-escolar
```

### Opción 4: DigitalOcean App Platform

1. Crear cuenta en DigitalOcean
2. Conectar repositorio GitHub
3. Crear App Platform
4. Seleccionar rama a desplegar
5. Configurar variables de entorno
6. Deploy

## Optimizaciones de Rendimiento

### 1. Caché de resultados

```python
from functools import lru_cache
import json

@lru_cache(maxsize=1000)
def cached_route_calc(origin_lat, origin_lon, dest_lat, dest_lon):
    # Cálculo de ruta cacheado
    pass
```

### 2. Procesamiento asincrónico

```python
from celery import Celery

app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379'
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])

@celery.task
def calculate_routes_async(data):
    # Procesamiento en background
    return results
```

### 3. Compresión de respuestas

```python
from flask_compress import Compress

Compress(app)
```

### 4. Límite de velocidad

```python
from flask_limiter import Limiter

limiter = Limiter(app, key_func=lambda: request.remote_addr)

@app.route('/api/calculate-routes', methods=['POST'])
@limiter.limit("10 per minute")
def calculate_routes():
    pass
```

## Seguridad

### CORS Configuration

```python
from flask_cors import CORS

CORS(app, resources={
    r"/api/*": {
        "origins": ["https://midominio.com"],
        "methods": ["GET", "POST"],
        "allow_headers": ["Content-Type"]
    }
})
```

### Rate Limiting por IP

```python
@app.route('/api/upload-csv', methods=['POST'])
@limiter.limit("5 per day")
def upload_csv():
    pass
```

### Validación de entrada

```python
import bleach

@app.route('/api/search', methods=['POST'])
def search():
    query = request.json.get('q', '')
    # Limpiar entrada
    clean_query = bleach.clean(query, strip=True)
    pass
```

### Certificado SSL

```bash
# Con Let's Encrypt en Linux
sudo apt-get install certbot python3-certbot-nginx
sudo certbot certonly --nginx -d midominio.com
```

## Monitoreo

### Logs estructurados

```python
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

logger.info('Ruta calculada', extra={
    'distancia': 5.2,
    'tiempo': 12,
    'usuario_id': user_id
})
```

### Métricas con Prometheus

```python
from prometheus_client import Counter, Histogram

request_count = Counter(
    'api_requests_total',
    'Total de requests',
    ['method', 'endpoint']
)

request_duration = Histogram(
    'api_request_duration_seconds',
    'Duración del request'
)
```

### Alertas con Sentry

```python
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

sentry_sdk.init(
    dsn="https://key@sentry.io/project",
    integrations=[FlaskIntegration()]
)
```

## Base de Datos

### Agregar persistencia con PostgreSQL

```python
from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:pass@localhost/rutas_db'
db = SQLAlchemy(app)

class Route(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre_origen = db.Column(db.String(200))
    nombre_destino = db.Column(db.String(200))
    lat_a = db.Column(db.Float)
    lon_a = db.Column(db.Float)
    lat_b = db.Column(db.Float)
    lon_b = db.Column(db.Float)
    distancia = db.Column(db.Float)
    tiempo = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
```

## API REST Completo

### Endpoints adicionales

```python
# GET todas las rutas
@app.route('/api/rutas', methods=['GET'])
def get_all_routes():
    pass

# GET ruta por ID
@app.route('/api/rutas/<int:route_id>', methods=['GET'])
def get_route(route_id):
    pass

# PUT actualizar ruta
@app.route('/api/rutas/<int:route_id>', methods=['PUT'])
def update_route(route_id):
    pass

# DELETE eliminar ruta
@app.route('/api/rutas/<int:route_id>', methods=['DELETE'])
def delete_route(route_id):
    pass
```

## Testing

### Tests unitarios

```python
import pytest

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_upload_csv(client):
    response = client.post('/api/upload-csv', 
        data={'file': (open('test.csv'), 'test.csv')})
    assert response.status_code == 200

def test_calculate_routes(client):
    response = client.post('/api/calculate-routes')
    assert response.status_code == 200
```

**Ejecutar tests:**
```bash
pytest -v
pytest --cov=app  # Con cobertura
```

## Documentación API con Swagger

```python
from flasgger import Swagger

swagger = Swagger(app)

@app.route('/api/calculate-routes', methods=['POST'])
def calculate_routes():
    """
    Calcula rutas de transporte
    ---
    responses:
      200:
        description: Rutas calculadas
        schema:
          type: object
          properties:
            rutas:
              type: array
              items:
                type: object
                properties:
                  distancia_km:
                    type: number
                  tiempo_minutos:
                    type: number
    """
    pass
```

Acceder a documentación: http://localhost:5000/apidocs/

## Troubleshooting

### Error: "ModuleNotFoundError"
```bash
pip install --force-reinstall -r requirements.txt
```

### Puerto 5000 ocupado
```bash
# Linux/Mac
lsof -i :5000
kill -9 <PID>

# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

### Mapbox no responde
```bash
# Verificar token
curl "https://api.mapbox.com/directions/v5/mapbox/driving/-78.5,-0.2;-78.5,-0.2?access_token=tu_token"

# Aumentar timeout
requests.get(url, timeout=30)
```

### CSV no se procesa
```python
# Verificar encoding
with open('archivo.csv', 'rb') as f:
    print(f.read(4))  # Debería mostrar bytes
    
# Reconvertir
df = pd.read_csv('archivo.csv', encoding='latin-1')
df.to_csv('archivo_utf8.csv', encoding='utf-8')
```

---

**Versión:** 1.0.0  
**Última actualización:** 2025
