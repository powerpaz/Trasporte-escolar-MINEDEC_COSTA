# 🚌 Sistema de Gestión de Rutas de Transporte Escolar

[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0-green)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-Open-yellow)](LICENSE)

Sistema completo para convertir datos de rutas escolares en mapas interactivos con cálculo automático de distancias y tiempos.

## ✨ Características

- ✅ **Conversión Excel → CSV** preservando caracteres especiales
- ✅ **Cálculo automático** de distancias y tiempos de viaje
- ✅ **Mapa interactivo** con Leaflet + Mapbox
- ✅ **Exportación múltiple**: GeoJSON, CSV, PNG
- ✅ **Interfaz web** moderna y responsiva
- ✅ **Instalación automática** (scripts incluidos)

## 🚀 Inicio Rápido
```bash
# 1. Clona el repositorio
git clone https://github.com/TU_USUARIO/Rutas-Escolar-MINEDEC.git
cd Rutas-Escolar-MINEDEC

# 2. Linux/Mac
bash scripts/start.sh

# 3. Windows
scripts/start.bat

# 4. Abre en navegador
# http://localhost:5000
```

## 📋 Requisitos

- Python 3.8+
- Navegador moderno
- Conexión a internet

## 📚 Documentación

- [INICIO_RAPIDO.md](INICIO_RAPIDO.md) - Primeros pasos
- [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) - Producción
- [docs/MEJORAS.md](docs/MEJORAS.md) - Roadmap
- [docs/MANIFEST.md](docs/MANIFEST.md) - Especificaciones

## 📊 Estructura de Datos

Tu CSV debe tener:
```csv
Longitud_A, Latitud_A, Longitud_B, Latitud_B
-78.5054, -0.2192, -78.5167, -0.2189
```

## 🔧 Configuración Avanzada

Mapbox (opcional, para rutas precisas):
```bash
echo "MAPBOX_TOKEN=tu_token_aqui" > .env
```

## 📞 Soporte

- Revisa [INICIO_RAPIDO.md](INICIO_RAPIDO.md)
- Consulta [docs/](docs/) para más info
- Crea un [Issue](../../issues) si encuentras problemas

## ⚖️ Licencia

Abierta para uso educativo y comercial. Ver detalles en cada archivo.

## 👥 Desarrollado para

MINEDEC - Costa (Transporte Escolar)

---

**Versión:** 1.0.0 | **Estado:** ✅ Producción lista
