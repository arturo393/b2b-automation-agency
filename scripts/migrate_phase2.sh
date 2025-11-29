#!/bin/bash
# Script de Migración Fase 2 - Post GitHub Rename
# Este script actualiza las referencias locales después de renombrar el repo en GitHub

set -e  # Exit on error

echo "🔄 Fase 2: Actualización Post-Rename"
echo "======================================"
echo ""

# 1. Actualizar remote URL
echo "📡 1. Actualizando remote URL..."
git remote set-url origin https://github.com/arturo393/defi-monitor.git
echo "✅ Remote actualizado"
echo ""

# 2. Verificar remote
echo "🔍 2. Verificando remote..."
git remote -v
echo ""

# 3. Fetch para sincronizar
echo "🔄 3. Sincronizando con remoto..."
git fetch origin
echo "✅ Sincronizado"
echo ""

# 4. Verificar branch tracking
echo "🌿 4. Verificando branch tracking..."
git branch -vv
echo ""

echo "✅ Fase 2 completada!"
echo ""
echo "Próximo paso: Renombrar directorio local"
echo "Comando: cd /Users/arturo && mv defi-newsletter defi-monitor"
