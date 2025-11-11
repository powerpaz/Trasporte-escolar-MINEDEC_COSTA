# ⚡ Guía de Inicio Rápido

## 📦 ¿Qué incluye este proyecto?

Tu solución completa para gestión de rutas de transporte escolar incluye:

```
📁 Sistema de Rutas Escolar
├── 🐍 app.py                    # Aplicación web principal
├── 🔄 convert_excel_to_csv.py   # Conversor de formatos
├── 📋 requirements.txt           # Dependencias
├── 📁 templates/
│   └── index.html              # Interfaz web
├── 🚀 start.sh                  # Script inicio (Linux/Mac)
├── 🚀 start.bat                 # Script inicio (Windows)
├── 📊 ejemplo_rutas.csv         # Datos de prueba
├── 📚 README.md                 # Documentación completa
├── 🔧 DEPLOYMENT.md             # Deployment avanzado
└── 🎯 MEJORAS.md                # Mejoras futuras
```

## 🎯 Objetivo

Convertir archivos Excel con coordenadas de rutas escolares → Mapa interactivo con:
- ✅ Cálculo automático de distancias
- ✅ Estimación de tiempos
- ✅ Visualización interactiva
- ✅ Exportación de datos (GeoJSON, CSV, PNG)

## ⏱️ Tiempo requerido

- **Instalación:** 5-10 minutos
- **Primera ejecución:** 1 minuto
- **Primera ruta:** 2 minutos

**Total:** 15 minutos para estar funcionando ✨

## 🔧 Pre-requisitos

### Verificar que tengas instalado:

#### 1. Python 3.8+
```bash
# Verificar versión
python3 --version

# Si no está instalado: https://www.python.org/downloads/
```

#### 2. Git (opcional, para clonar)
```bash
git --version
```

## 🚀 Instalación

### Opción A: Automática (Recomendado)

**En Linux/Mac:**
```bash
# Descargar y navegar a la carpeta
cd tu-carpeta-del-proyecto

# Ejecutar script de inicio
bash start.sh

# Espera 1-2 minutos a que se instale todo
# Luego abre: http://localhost:5000
```

**En Windows:**
```bash
# Descargar y navegar a la carpeta
cd tu-carpeta-del-proyecto

# Ejecutar script de inicio
start.bat

# Se abrirá automáticamente una ventana
# Espera a que termine la instalación
# Luego abre: http://localhost:5000
```

### Opción B: Manual

```bash
# 1. Navegar a la carpeta
cd tu-carpeta-del-proyecto

# 2. Crear entorno virtual
python3 -m venv venv

# 3. Activar entorno
# En Linux/Mac:
source venv/bin/activate

# En Windows:
venv\Scripts\activate

# 4. Instalar dependencias
pip install -r requirements.txt

# 5. Ejecutar aplicación
python3 app.py
```

## 📖 Primeros Pasos

### 1️⃣ Abrir la aplicación

Ve a tu navegador y abre:
```
http://localhost:5000
```

Deberías ver una pantalla como esta:
- Panel izquierdo: Controles
- Panel derecho: Mapa interactivo

### 2️⃣ Cargar datos de prueba

**Opción A: Archivo de ejemplo**
1. En la sección "📁 Cargar Datos", haz clic en el área punteada
2. Selecciona el archivo: `ejemplo_rutas.csv`
3. Se cargarán 8 rutas de ejemplo en Quito

**Opción B: Tu archivo personal**
1. Asegúrate que tu CSV tenga estas columnas:
   - `Longitud_A` y `Latitud_A` (punto de salida)
   - `Longitud_B` y `Latitud_B` (punto de llegada)
2. Carga tu archivo de la misma manera

### 3️⃣ Calcular rutas

1. Después de cargar el CSV, el botón "Calcular Rutas" se activa
2. Haz clic en "Calcular Rutas"
3. Espera unos segundos (depende de la cantidad)
4. Las rutas aparecerán automáticamente en el mapa

### 4️⃣ Explorar el mapa

- **Zoom:** Rueda del mouse o botones
- **Mover:** Arrastra con mouse
- **Clics:** 
  - Ruta en lista → Se resalta en el mapa
  - Marcador en mapa → Muestra información
  - Línea en mapa → Muestra detalles de la ruta

### 5️⃣ Exportar resultados

Selecciona uno de estos formatos:

- **GeoJSON** → Importar en QGIS, ArcGIS
- **CSV** → Abrir en Excel, análisis
- **PNG** → Captura del mapa actual

## 📊 Estructura esperada del CSV

### Formato básico:
```csv
Longitud_A,Latitud_A,Longitud_B,Latitud_B
-78.5054,-0.2192,-78.5167,-0.2189
-78.5100,-0.2300,-78.5000,-0.2100
```

### Con información adicional:
```csv
Longitud_A,Latitud_A,Longitud_B,Latitud_B,Nombre_Origen,Nombre_Destino,Accesibilidad
-78.5054,-0.2192,-78.5167,-0.2189,Colegio A,Terminal Sur,Estándar
-78.5100,-0.2300,-78.5000,-0.2100,Escuela B,Centro,Preferente
```

## ⚙️ Configuración (Opcional)

### Habilitar Mapbox para rutas precisas

Mapbox da rutas REALES en lugar de líneas rectas. Es opcional pero recomendado.

**Pasos:**
1. Ir a https://account.mapbox.com/auth/signup/
2. Crear cuenta gratuita
3. Copiar token de la sección "Tokens"
4. Crear archivo `.env`:
   ```
   MAPBOX_TOKEN=pk.eyJ1IjoieXouYWNj...
   ```
5. Reiniciar aplicación

## 🐛 Solución de Problemas Comunes

### "Puerto 5000 ya está en uso"
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <numero> /F

# Linux/Mac
lsof -i :5000
kill -9 <numero>
```

### "ModuleNotFoundError"
```bash
# Reinstalar dependencias
pip install --force-reinstall -r requirements.txt
```

### "CSV no carga"
1. Abre el CSV en Excel
2. Verifica columnas: Longitud_A, Latitud_A, Longitud_B, Latitud_B
3. Guarda como CSV UTF-8
4. Intenta de nuevo

### "El mapa no muestra rutas"
1. Verifica que las coordenadas sean válidas:
   - Latitud: -90 a 90
   - Longitud: -180 a 180
2. Para Ecuador: Longitudes negativas, Latitudes alrededor de -0 a -2
3. Prueba con `ejemplo_rutas.csv` primero

### "Error 'Access Denied'"
Asegúrate que:
- El archivo CSV no está abierto en Excel
- Tienes permisos de lectura en la carpeta
- Python está actualizado

## 📚 Archivos que necesitas conocer

| Archivo | Propósito | Debes editar? |
|---------|-----------|--------------|
| `app.py` | Lógica principal | Solo para avanzado |
| `templates/index.html` | Interfaz web | Solo para personalizar |
| `requirements.txt` | Dependencias | No, a menos que agregues librerías |
| `ejemplo_rutas.csv` | Datos de prueba | No, es solo para probar |
| `README.md` | Documentación | Opcional |

## 🎓 Próximos Pasos

### Una vez que funciona:

1. **Reemplazar datos de ejemplo**
   - Usa tus propios archivos Excel
   - Convierte a CSV
   - Sube a la aplicación

2. **Personalizar interfaz**
   - Cambiar colores en `templates/index.html`
   - Agregar logo
   - Modificar textos

3. **Llevar a producción**
   - Ver `DEPLOYMENT.md`
   - Opciones: Heroku, AWS, DigitalOcean

4. **Agregar mejoras**
   - Ver `MEJORAS.md` para funcionalidades futuras
   - Base de datos
   - Autenticación
   - Análisis estadísticos

## 📞 Ayuda

### Documentación detallada:
- `README.md` - Guía completa
- `DEPLOYMENT.md` - Para llevar a producción
- `MEJORAS.md` - Futuras funcionalidades

### En caso de error:
1. Lee el mensaje de error
2. Revisa la sección "Problemas Comunes"
3. Consulta la documentación
4. Intenta con datos de ejemplo

## ✅ Checklist de Instalación

- [ ] Python 3.8+ instalado
- [ ] Descargó todos los archivos
- [ ] Ejecutó `start.sh` o `start.bat`
- [ ] Abrió http://localhost:5000
- [ ] Cargó archivo CSV
- [ ] Calculó rutas
- [ ] Vio rutas en el mapa
- [ ] Exportó datos

## 🎉 ¡Listo!

Una vez completado el checklist, tienes un sistema funcional de:
- ✅ Conversión de datos
- ✅ Cálculo de rutas
- ✅ Visualización en mapa
- ✅ Exportación de resultados

## 📞 Soporte

Para ayuda técnica:
1. Verifica que Python esté correctamente instalado
2. Intenta reinstalar dependencias
3. Consulta la documentación incluida
4. Revisa los logs en la consola

---

**¡Ya estás listo para empezar! 🚀**

**Tiempo estimado:** 15 minutos  
**Dificultad:** ⭐ Muy fácil

¿Necesitas ayuda? Consulta `README.md` para documentación más detallada.
