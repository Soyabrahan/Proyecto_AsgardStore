#!/bin/bash

# Script de build específico para Vercel
echo "🚀 Iniciando build para Vercel..."

# Instalar dependencias
echo "📦 Instalando dependencias..."
npm install

# Verificar que Next.js esté instalado
if [ ! -d "node_modules/next" ]; then
    echo "❌ Error: Next.js no está instalado"
    exit 1
fi

# Ejecutar build
echo "🔨 Ejecutando build..."
npm run build

# Verificar que el build fue exitoso
if [ $? -eq 0 ]; then
    echo "✅ Build completado exitosamente"
    echo "📁 Archivos generados:"
    ls -la .next/
else
    echo "❌ Error en el build"
    exit 1
fi

echo "🎉 Build listo para despliegue en Vercel" 