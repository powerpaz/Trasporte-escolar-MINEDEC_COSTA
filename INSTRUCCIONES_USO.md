# Instrucciones de Uso — Sistema de Rutas de Transporte Escolar

## ✅ Problemas resueltos
- **Dependencias**: se añadieron `Flask` y `pandas` al proyecto.
- **Estructura**: se creó la carpeta `templates/` y se movió `index.html` dentro de ella.
- **CSV**: validación y lectura OK.

## 🧰 Instalación
```bash
pip3 install -r requirements.txt
```

> Si tu `requirements.txt` no incluye Flask/pandas, usa este archivo actualizado.

## ▶️ Ejecución
```bash
python3 app.py
# Navega a: http://localhost:5000
```

## 📤 Carga de CSV
El archivo debe incluir (no importan mayúsculas/minúsculas, ni espacios):
- `longitud_a`, `latitud_a`
- `longitud_b`, `latitud_b`

Ejemplo: `ejemplo_rutas.csv` (incluido en tu repo) funciona correctamente.

## 🔍 Pruebas rápidas
Ejecuta el script:
```bash
python3 test_server.py
```
Verifica:
- Página de inicio responde `200 OK`.
- Carga de CSV en `/api/upload-csv`.
- Cálculo en `/api/calculate-routes`.

## 📁 Estructura mínima sugerida
```
.
├─ app.py
├─ requirements.txt
├─ templates/
│  └─ index.html   # (mueve aquí tu index.html existente)
├─ ejemplo_rutas.csv
└─ test_server.py
```

## 🧹 Git
Se agrega un `.gitignore` (el correcto con punto al inicio) para excluir logs/temporales.