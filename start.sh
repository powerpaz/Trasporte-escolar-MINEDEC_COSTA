#!/bin/bash
# Script de inicio para la aplicación de Rutas de Transporte Escolar

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║  🚌 Sistema de Gestión de Rutas de Transporte Escolar         ║"
echo "║     Por: MINEDEC - Costa                                      ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Verificar si Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 no está instalado"
    echo "📥 Instala Python desde: https://www.python.org/downloads/"
    exit 1
fi

echo "✓ Python 3 detectado: $(python3 --version)"
echo ""

# Crear entorno virtual si no existe
if [ ! -d "venv" ]; then
    echo "📦 Creando entorno virtual..."
    python3 -m venv venv
    echo "✓ Entorno virtual creado"
else
    echo "✓ Entorno virtual encontrado"
fi

echo ""

# Activar entorno virtual
echo "🔧 Activando entorno virtual..."
source venv/bin/activate

echo "✓ Entorno activado"
echo ""

# Instalar dependencias
echo "📚 Instalando dependencias..."
pip install -q -r requirements.txt
echo "✓ Dependencias instaladas"
echo ""

# Crear directorio de templates si no existe
if [ ! -d "templates" ]; then
    mkdir -p templates
    echo "✓ Directorio 'templates' creado"
fi

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║  ✨ Listo para iniciar                                        ║"
echo "║                                                                ║"
echo "║  🚀 Iniciando aplicación...                                   ║"
echo "║  🌐 Abre tu navegador en: http://localhost:5000              ║"
echo "║                                                                ║"
echo "║  💡 Tip: Usa el archivo 'ejemplo_rutas.csv' para probar      ║"
echo "║                                                                ║"
echo "║  Presiona Ctrl+C para detener                                 ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Ejecutar la aplicación
python3 app.py
