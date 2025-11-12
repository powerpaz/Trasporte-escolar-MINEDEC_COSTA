#!/bin/bash

echo "======================================"
echo "Iniciando Aplicación de Transporte Escolar"
echo "======================================"
echo ""

# Verificar si Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "Error: Python3 no está instalado."
    exit 1
fi

# Verificar si las dependencias están instaladas
echo "Verificando dependencias..."
if ! python3 -c "import flask" &> /dev/null; then
    echo "Instalando dependencias..."
    pip3 install -r requirements.txt --ignore-installed blinker
fi

echo ""
echo "Iniciando servidor Flask..."
echo "La aplicación estará disponible en: http://localhost:5000"
echo ""
echo "Para detener el servidor, presiona Ctrl+C"
echo ""

# Iniciar la aplicación
python3 app.py
