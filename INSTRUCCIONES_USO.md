# Instrucciones de Uso - Sistema de Rutas de Transporte Escolar

## Problemas Resueltos

Se han corregido los siguientes problemas:

1. ✅ **Dependencias faltantes**: Flask y pandas ahora están instalados
2. ✅ **Estructura de carpetas**: Se creó la carpeta `templates/` requerida por Flask
3. ✅ **Procesamiento de CSV**: El sistema ahora procesa correctamente archivos CSV

## Cómo Usar el Sistema

### Paso 1: Instalar dependencias

```bash
pip3 install -r requirements.txt
```

### Paso 2: Iniciar el servidor

```bash
python3 app.py
```

El servidor se iniciará en `http://localhost:5000`

### Paso 3: Abrir la aplicación

Abre tu navegador web y visita:
```
http://localhost:5000
```

### Paso 4: Cargar tu archivo CSV

1. En la interfaz web, haz clic en el área de "Cargar Datos"
2. Selecciona tu archivo CSV (o arrástralo)
3. El archivo debe tener las siguientes columnas (en cualquier orden):
   - `Longitud_A` o `longitud_a` (coordenada de origen)
   - `Latitud_A` o `latitud_a` (coordenada de origen)
   - `Longitud_B` o `longitud_b` (coordenada de destino)
   - `Latitud_B` o `latitud_b` (coordenada de destino)
   - Columnas opcionales: `Nombre_Origen`, `Nombre_Destino`, `Accesibilidad`, etc.

### Paso 5: Calcular rutas

1. Una vez cargado el CSV, haz clic en "Calcular Rutas"
2. El sistema calculará las distancias y tiempos estimados para cada ruta
3. Las rutas aparecerán en el mapa y en la lista lateral

### Paso 6: Exportar resultados

Puedes exportar los resultados en varios formatos:
- **GeoJSON**: Para usar en otros sistemas GIS
- **CSV**: Para análisis en Excel o herramientas similares
- **Imagen**: Captura del mapa con las rutas visualizadas

## Formato del CSV de Ejemplo

El archivo `ejemplo_rutas.csv` tiene el formato correcto:

```csv
Longitud_A,Latitud_A,Longitud_B,Latitud_B,Nombre_Origen,Nombre_Destino,Accesibilidad,Conductor,Telefono
-78.5054,-0.2192,-78.5167,-0.2189,Colegio Central Quito,Terminal Sur Quito,Estándar,Juan García,0999123456
```

## Ejecutar Pruebas

Para verificar que el sistema funciona correctamente:

```bash
# Iniciar el servidor en una terminal
python3 app.py

# En otra terminal, ejecutar las pruebas
python3 test_server.py
```

## Solución de Problemas

### El servidor no inicia
- Verifica que todas las dependencias estén instaladas: `pip3 list | grep -E "(Flask|pandas)"`
- Asegúrate de que el puerto 5000 no esté en uso: `lsof -i :5000`

### No se procesa el CSV
- Verifica que el CSV tenga las columnas correctas (con las mayúsculas/minúsculas que prefieras)
- Asegúrate de que el archivo esté codificado en UTF-8
- Verifica que las coordenadas sean números válidos

### Las rutas no se calculan
- Verifica que las coordenadas estén en formato correcto (latitud/longitud)
- Asegúrate de que las coordenadas estén en el rango válido:
  - Latitud: -90 a 90
  - Longitud: -180 a 180

## Notas Importantes

1. **No uses App.js directamente**: El archivo `App.js` es un sistema legacy que lee Excel. Usa el sistema Flask (index.html + app.py)
2. **Token de Mapbox**: Por defecto el sistema usa OpenStreetMap. Si quieres usar Mapbox, configura la variable de entorno `MAPBOX_TOKEN`
3. **Modo de desarrollo**: El servidor actual es para desarrollo. Para producción, usa un servidor WSGI como Gunicorn

## Estructura del Proyecto

```
.
├── app.py                  # Backend Flask (servidor principal)
├── templates/
│   └── index.html         # Interfaz web
├── ejemplo_rutas.csv      # CSV de ejemplo
├── test_server.py         # Script de pruebas
├── requirements.txt       # Dependencias Python
└── INSTRUCCIONES_USO.md  # Este archivo
```

## Contacto y Soporte

Si tienes problemas, revisa los logs del servidor en `server.log` o contacta al equipo de desarrollo.
