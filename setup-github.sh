#!/bin/bash
# Script para conectar el proyecto con el nuevo repositorio de GitHub

echo "🔗 Configurando conexión con GitHub..."
echo ""

# Cambiar el remoto al nuevo repositorio
echo "📍 Cambiando remoto a: https://github.com/amayaeguizabal7/second-brain.git"
git remote set-url origin https://github.com/amayaeguizabal7/second-brain.git

echo ""
echo "✅ Remoto actualizado. Verificando..."
git remote -v

echo ""
echo "📤 Subiendo código a GitHub..."
git push -u origin main

echo ""
echo "✨ ¡Listo! Tu código está en: https://github.com/amayaeguizabal7/second-brain"
echo ""
echo "🎯 Próximo paso: Configurar Render con este repositorio"

