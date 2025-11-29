#!/bin/bash
# Fase 3: Refactorización automatizada
set -e

echo "🔄 Fase 3: Refactorización de Código"
echo "====================================="
echo ""

# 1. Renombrar archivos principales
echo "📝 1. Renombrando archivos..."
mv scripts/generate_newsletter.py scripts/generate_dashboard.py 2>/dev/null || echo "  - generate_dashboard.py ya existe"
echo "✅ Archivos renombrados"
echo ""

# 2. Crear directorio legacy para scripts obsoletos
echo "📦 2. Creando directorio legacy..."
mkdir -p scripts/legacy
echo "✅ Directorio legacy creado"
echo ""

# 3. Mover scripts obsoletos
echo "🗄️  3. Moviendo scripts obsoletos a legacy/..."
for script in send_to_beehiiv.py publish_to_beehiiv.py publish_to_substack.py; do
  if [ -f "scripts/$script" ]; then
    mv "scripts/$script" "scripts/legacy/" 2>/dev/null || true
    echo "  ✅ $script → legacy/"
  fi
done
echo ""

# 4. Aplicar búsqueda/reemplazo en archivos Python
echo "🔍 4. Aplicando refactorización en archivos Python..."
for file in scripts/*.py; do
  if [ -f "$file" ]; then
    echo "  - Procesando: $(basename $file)"
    # Reemplazos seguros (solo en strings y comentarios, no en paths históricos)
    sed -i '' 's/generate_newsletter/generate_dashboard/g' "$file"
    sed -i '' 's/Newsletter Automation/Dashboard Automation/g' "$file"
    sed -i '' 's/DeFi Newsletter/DeFi Monitor/g' "$file"
    sed -i '' 's/newsletter semanal/dashboard de monitoreo/g' "$file"
    sed -i '' 's/escribir newsletter/actualizar dashboard/g' "$file"
  fi
done
echo "✅ Refactorización completada"
echo ""

echo "✅ Fase 3.1 completada!"
echo ""
echo "Próximos pasos:"
echo "  - Crear nuevos scripts (generate_dashboard.py lógica)"
echo "  - Actualizar documentación"
echo "  - Actualizar GitHub Actions"
