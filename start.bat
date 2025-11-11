@echo off
chcp 65001 >nul
cls

echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║  🚌 Sistema de Gestión de Rutas de Transporte Escolar         ║
echo ║     Por: MINEDEC - Costa                                      ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

REM Verificar si Python está instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python 3 no está instalado
    echo 📥 Instala Python desde: https://www.python.org/downloads/
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo ✓ %PYTHON_VERSION% detectado
echo.

REM Crear entorno virtual si no existe
if not exist "venv" (
    echo 📦 Creando entorno virtual...
    python -m venv venv
    echo ✓ Entorno virtual creado
) else (
    echo ✓ Entorno virtual encontrado
)

echo.

REM Activar entorno virtual
echo 🔧 Activando entorno virtual...
call venv\Scripts\activate.bat
echo ✓ Entorno activado
echo.

REM Instalar dependencias
echo 📚 Instalando dependencias...
pip install -q -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ Error al instalar dependencias
    pause
    exit /b 1
)
echo ✓ Dependencias instaladas
echo.

REM Crear directorio templates si no existe
if not exist "templates" (
    mkdir templates
    echo ✓ Directorio 'templates' creado
)

echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║  ✨ Listo para iniciar                                        ║
echo ║                                                                ║
echo ║  🚀 Iniciando aplicación...                                   ║
echo ║  🌐 Abre tu navegador en: http://localhost:5000              ║
echo ║                                                                ║
echo ║  💡 Tip: Usa el archivo 'ejemplo_rutas.csv' para probar      ║
echo ║                                                                ║
echo ║  Presiona Ctrl+C para detener                                 ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

REM Ejecutar la aplicación
python app.py

pause
