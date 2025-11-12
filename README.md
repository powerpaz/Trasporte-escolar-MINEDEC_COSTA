# Sistema de Transporte Escolar MINEDEC Costa

Sistema web para calcular y visualizar rutas de transporte escolar usando coordenadas geográficas.

## 🚀 Inicio Rápido

### En Linux/Mac:
```bash
./start.sh
```

### En Windows:
```
start.bat
```

O manualmente:
```bash
python3 app.py
```

La aplicación estará disponible en: **http://localhost:5000**

## 📋 Requisitos

- Python 3.7+
- pip (gestor de paquetes de Python)

## 📦 Dependencias

Las dependencias se instalan automáticamente al usar los scripts de inicio, pero también puedes instalarlas manualmente:

```bash
pip3 install -r requirements.txt
```

Dependencias incluidas:
- Flask - Framework web
- Flask-CORS - Manejo de CORS
- Pandas - Procesamiento de datos
- Gunicorn - Servidor de producción

## 🎯 Características

- **Carga de archivos CSV** con coordenadas de rutas
- **Cálculo automático de distancias** usando la fórmula de Haversine
- **Visualización en mapa interactivo** con Leaflet
- **API REST** para integración con otros sistemas
- **Validación de datos** automática

## 📄 Formato del CSV

El archivo CSV debe contener las siguientes columnas:

- `longitud_a` - Longitud del punto de inicio
- `latitud_a` - Latitud del punto de inicio
- `longitud_b` - Longitud del punto de destino
- `latitud_b` - Latitud del punto de destino

### Ejemplo de CSV:

```csv
longitud_a,latitud_a,longitud_b,latitud_b
-78.5,0.2,-78.6,0.3
-78.7,0.4,-78.8,0.5
```

## 🔧 API Endpoints

### Health Check
```
GET /api/health
```

### Subir CSV
```
POST /api/upload-csv
Content-Type: multipart/form-data
Body: file=<archivo.csv>
```

### Calcular Rutas
```
POST /api/calculate-routes
Content-Type: application/json
Body: {"limit": 100}  // opcional
```

## 🐳 Despliegue

### Docker
```bash
docker build -t transporte-escolar .
docker run -p 5000:5000 transporte-escolar
```

### Docker Compose
```bash
docker-compose up
```

### Heroku/Render/Fly.io
Los archivos de configuración ya están incluidos:
- `Procfile` - Para Heroku
- `render.yaml` - Para Render
- `fly.toml` - Para Fly.io

## 🛠️ Solución de Problemas

### La aplicación no arranca

1. **Verificar que Python está instalado:**
   ```bash
   python3 --version
   ```

2. **Instalar dependencias manualmente:**
   ```bash
   pip3 install -r requirements.txt --ignore-installed blinker
   ```

3. **Verificar el puerto:**
   Si el puerto 5000 está ocupado, puedes cambiarlo:
   ```bash
   PORT=8000 python3 app.py
   ```

### Error "Página no encontrada"

1. **Verificar que el servidor está corriendo:**
   Deberías ver: `Running on http://127.0.0.1:5000`

2. **Acceder a la URL correcta:**
   - Local: http://localhost:5000
   - Red local: http://[tu-ip]:5000

3. **Verificar firewall:**
   Asegúrate de que el puerto 5000 no esté bloqueado.

### Error al cargar CSV

- Verifica que el archivo tenga las columnas requeridas
- Asegúrate de que los valores de coordenadas sean numéricos
- Prueba con diferentes codificaciones (UTF-8, Latin-1)

## 📝 Notas

- Este es un servidor de desarrollo. Para producción, usa Gunicorn:
  ```bash
  gunicorn app:app --bind 0.0.0.0:5000
  ```

- Las coordenadas deben estar en formato decimal (ej: -78.5, no grados/minutos/segundos)

## 📧 Soporte

Para reportar problemas, verifica:
1. Que las dependencias estén instaladas
2. Que el puerto no esté ocupado
3. Que el archivo CSV tenga el formato correcto

## 🎓 Uso

1. Abre http://localhost:5000 en tu navegador
2. Selecciona un archivo CSV con las rutas
3. Haz clic en "Subir CSV"
4. Haz clic en "Calcular" para generar las rutas
5. Visualiza las rutas en el mapa interactivo

---

**Desarrollado para MINEDEC Costa Rica**
