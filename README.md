# 🚌 Sistema de Gestión de Rutas de Transporte Escolar

Sistema completo para convertir datos de Excel/CSV a rutas interactivas en mapa, con cálculo automático de distancias, tiempos de viaje y exportación de datos.

## ✨ Características

- ✅ **Conversión Excel a CSV** - Preserva caracteres especiales (acentos, ñ, etc.)
- ✅ **Cálculo automático de distancias** - Usa fórmula Haversine y API Mapbox
- ✅ **Estimación de tiempos** - Basado en velocidad promedio y rutas reales
- ✅ **Mapa interactivo** - Leaflet con OpenStreetMap y Mapbox Satellite
- ✅ **Múltiples marcadores** - Origen (lleno) y destino (semitraslúcido)
- ✅ **Estadísticas en tiempo real** - Distancia total y tiempo promedio
- ✅ **Exportación flexible**:
  - GeoJSON (para SIG)
  - CSV (para análisis)
  - PNG (captura de pantalla del mapa)
- ✅ **Interfaz responsive** - Funciona en desktop, tablet y móvil
- ✅ **Accesibilidad** - Indicador de accesibilidad en rutas

## 📋 Requisitos de Datos

Tu CSV debe tener estas columnas (pueden variar el nombre):

```
Longitud_A, Latitud_A, Longitud_B, Latitud_B
```

**Variaciones aceptadas:**
- `longitude_a, latitude_a, longitude_b, latitude_b`
- `long_a, lat_a, long_b, lat_b`
- `lng_a, lat_a, lng_b, lat_b`
- Con espacios: `Longitud A`, `Latitud A`, etc.

**Columnas opcionales:**
- `nombre_origen` - Nombre del punto de origen
- `nombre_destino` - Nombre del punto de destino
- `accesibilidad` - Tipo de accesibilidad (Estándar, Preferente, etc.)
- Cualquier otra columna se incluirá en los detalles

## 🚀 Instalación y Uso

### 1. Preparar el Entorno

```bash
# Clonar o descargar el proyecto
cd tu-proyecto

# Crear entorno virtual (opcional pero recomendado)
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

### 2. Configurar Mapbox (Opcional pero Recomendado)

Para obtener rutas más precisas y usar mapa satelital:

```bash
# Crear archivo .env
echo "MAPBOX_TOKEN=tu_token_aqui" > .env
```

Obtener token en: https://account.mapbox.com/auth/signup/

### 3. Convertir Excel a CSV

**Opción A: Script automático**
```bash
python3 convert_excel_to_csv.py tu_archivo.xls
```

**Opción B: Manual desde la web (ver paso 4)**

### 4. Ejecutar la Aplicación

```bash
python3 app.py
```

Accede a: http://localhost:5000

## 📖 Guía de Uso

### En la Web

1. **Cargar datos**
   - Arrastra tu CSV a la zona de carga o haz clic
   - El archivo se valida automáticamente

2. **Calcular rutas**
   - Click en "Calcular Rutas"
   - Espera a que se procesen (puede tardar según la cantidad)
   - Las rutas aparecerán en el mapa

3. **Ver detalles**
   - Click en cualquier ruta en la lista lateral
   - Se mostrará modal con información detallada

4. **Exportar**
   - **GeoJSON**: Para usar en QGIS, ArcGIS u otros SIG
   - **CSV**: Tabla con cálculos para análisis en Excel
   - **PNG**: Captura del mapa actual

## 🗺️ Estructura del Mapa

**Colores:** Cada ruta tiene color único para identificación rápida

**Marcadores:**
- 🔵 Círculo lleno = Origen (salida)
- 🔵 Círculo semitransparente = Destino (llegada)
- 📍 Línea entre puntos = Ruta

**Interactividad:**
- Click en ruta en lista = Resalta en mapa
- Hover sobre elementos = Muestra información
- Zoom automático al cargar

## 📊 Información Calculada

Para cada ruta se calcula:

| Campo | Descripción | Fuente |
|-------|-------------|--------|
| Distancia (km) | Entre origen y destino | Mapbox o Haversine |
| Tiempo (minutos) | Tiempo estimado de viaje | Basado en distancia |
| Accesibilidad | Tipo de acceso especial | Del CSV |
| Número de pasos | Etapas de la ruta (si Mapbox) | API Mapbox |

## 🔧 Personalización

### Cambiar colores de rutas

En `templates/index.html`, línea ~300:
```javascript
const colors = ['#667eea', '#764ba2', '#f56565', '#48bb78', '#ed8936'];
```

### Cambiar proveedor de mapa

En `templates/index.html`, función `initMap()`:
```javascript
// Cambiar a Mapbox Satellite
L.tileLayer(`https://api.mapbox.com/styles/v1/mapbox/satellite-v9/tiles/{z}/{x}/{y}@2x?access_token=${mapboxToken}`).addTo(map);
```

### Ajustar velocidad promedio

En `app.py`, función `estimate_travel_time()`:
```python
def estimate_travel_time(distance_km, speed_kmh=30):  # Cambiar 30 por tu valor
```

## 📁 Estructura del Proyecto

```
proyecto/
├── app.py                      # Aplicación Flask principal
├── convert_excel_to_csv.py     # Script conversor
├── requirements.txt            # Dependencias Python
├── templates/
│   └── index.html             # Interfaz web
├── static/                     # (Opcional) CSS/JS adicional
└── .env                        # Variables de entorno
```

## 🚨 Problemas Comunes

### "El CSV no se carga"
- Verifica que sea UTF-8 encoding
- Asegúrate que las columnas sean: Longitud_A, Latitud_A, Longitud_B, Latitud_B

### "El mapa no muestra rutas"
- Verifica que las coordenadas sean válidas (lat: -90 a 90, lon: -180 a 180)
- Para Ecuador, usar: lon negativos (oeste), lat positivos (sur)

### "Error al conectar con Mapbox"
- Verifica token válido en `.env`
- El script seguirá funcionando con OpenStreetMap

### "Archivo Excel corrupto"
- Convierte primero en Excel a CSV (Archivo > Guardar Como > CSV UTF-8)
- Luego sube el CSV

## 📝 Ejemplos de Datos

### CSV correcto:
```csv
Longitud_A,Latitud_A,Longitud_B,Latitud_B,Nombre_Origen,Nombre_Destino,Accesibilidad
-78.5,-0.22,-78.51,-0.23,Colegio Central,Estación Sur,Estándar
-78.52,-0.24,-78.53,-0.25,Escuela Norte,Parque Principal,Preferente
```

### Excel con caracteres especiales:
```
Incluso con "ñ", "á", "é", "í", "ó", "ú" → Se preservan correctamente ✓
```

## 🔒 Notas de Seguridad

- Los datos se almacenan temporalmente en memoria
- No se guarda información en base de datos
- Cada sesión es independiente
- Para producción, añade autenticación

## 📚 APIs y Librerías

- **Leaflet.js** - Mapas interactivos
- **Flask** - Framework web Python
- **Pandas** - Procesamiento de datos
- **Requests** - Cliente HTTP para Mapbox
- **html2canvas** - Captura de pantalla del cliente

## 🌐 Compatibilidad

- ✅ Chrome/Edge (recomendado)
- ✅ Firefox
- ✅ Safari
- ✅ Navegadores móviles
- ⚠️ IE 11 (limitado)

## 📞 Soporte

Para problemas o sugerencias:

1. Revisa los logs en la consola (F12 en navegador)
2. Verifica el formato de datos en CSV
3. Intenta con un ejemplo más pequeño primero

## 📄 Licencia

Este proyecto es de código abierto y libre para usar.

---

**Versión:** 1.0.0  
**Última actualización:** 2025  
**Autor:** Equipo de Desarrollo
