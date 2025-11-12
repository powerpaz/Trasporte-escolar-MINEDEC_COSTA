@echo off
echo ======================================
echo Iniciando Aplicacion de Transporte Escolar
echo ======================================
echo.

REM Verificar si Python esta instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python no esta instalado.
    pause
    exit /b 1
)

echo Verificando dependencias...
python -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo Instalando dependencias...
    pip install -r requirements.txt --ignore-installed blinker
)

echo.
echo Iniciando servidor Flask...
echo La aplicacion estara disponible en: http://localhost:5000
echo.
echo Para detener el servidor, presiona Ctrl+C
echo.

REM Iniciar la aplicacion
python app.py
