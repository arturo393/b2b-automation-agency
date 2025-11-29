#!/bin/bash
# Fase 4: Actualización masiva de documentación
set -e

echo "📚 Fase 4: Actualización de Documentación"
echo "=========================================="
echo ""

# 1. Crear directorio legacy para docs obsoletos
echo "📦 1. Creando directorio docs/legacy..."
mkdir -p docs/legacy
echo "✅ Directorio creado"
echo ""

# 2. Mover documentos obsoletos
echo "🗄️  2. Moviendo documentos obsoletos..."
for doc in SUCCESS.md START_HERE.md SETUP_STATUS.md docs/NEWSLETTER-PLATFORMS.md; do
  if [ -f "$doc" ]; then
    mv "$doc" docs/legacy/ 2>/dev/null || true
    echo "  ✅ $(basename $doc) → docs/legacy/"
  fi
done
echo ""

# 3. Actualizar QUICK_REFERENCE.md
echo "📝 3. Actualizando QUICK_REFERENCE.md..."
cat > QUICK_REFERENCE.md << 'EOF'
# 🚀 Quick Reference - DeFi Monitor

Comandos y referencias rápidas para desarrollo diario.

## 📊 Comandos Principales

### Recolectar Datos
```bash
python scripts/collect_defi_data.py
```

### Generar Dashboard
```bash
python scripts/generate_dashboard.py
```

### Ver Dashboard
```bash
cat data/dashboard.json | python -m json.tool
# O usar jq:
cat data/dashboard.json | jq '.summary'
```

### Ejecutar Todo el Pipeline
```bash
python scripts/collect_defi_data.py && \
python scripts/generate_dashboard.py
```

## 🔧 Configuración

### Variables de Entorno
```bash
# Copiar template
cp .env.example .env

# Editar configuración
nano .env
```

### Jira Integration
```bash
# Test conexión
python scripts/test_jira_connection.py

# Actualizar token
python scripts/update_jira_token.py
```

## 📁 Estructura

```
defi-monitor/
├── scripts/
│   ├── collect_defi_data.py        # Fetch DeFi Llama
│   ├── generate_dashboard.py       # Generar JSON
│   └── jira_integration.py         # Jira tasks
├── data/
│   ├── protocols.json               # Raw data
│   └── dashboard.json               # Processed
└── docs/                            # Documentation
```

## 🤖 GitHub Actions

### Trigger Manual
```bash
# Desde GitHub UI:
Actions → DeFi Monitor Dashboard Update → Run workflow
```

### Ver Logs
```bash
# Desde GitHub:
Actions → Latest run → View logs
```

## 🔍 Debugging

### Ver Protocolos
```bash
cat data/protocols.json | jq '.protocols[] | {name, tvl}'
```

### Ver Alertas
```bash
cat data/dashboard.json | jq '.alerts'
```

### Ver Summary
```bash
cat data/dashboard.json | jq '.summary'
```

## 📊 Jira Tasks

| Key | Summary | Priority |
|-----|---------|----------|
| DM-1 | Setup DeFi Monitor Infrastructure | High |
| DM-2 | Implement Yield Tracking API | High |
| DM-3 | Build Dashboard Generator | High |
| DM-4 | Configure Alert System | Medium |

## 🔗 Links Útiles

- **Repo:** https://github.com/arturo393/defi-monitor
- **DeFi Llama API:** https://defillama.com/docs/api
- **Jira:** https://averas-1744767979220.atlassian.net

## 💡 Tips

- Dashboard se actualiza cada 6 horas automáticamente
- Alertas se generan para APY > 50%
- Usar `jq` para parsear JSON fácilmente
- Git histórico guarda todos los datos pasados

EOF
echo "✅ QUICK_REFERENCE.md actualizado"
echo ""

# 4. Actualizar docs/ROADMAP.md
echo "📝 4. Actualizando docs/ROADMAP.md..."
cat > docs/ROADMAP.md << 'EOF'
# 🗺️ Roadmap - DeFi Monitor (6 Meses)

## ✅ Fase 1: MVP (Completado)
- [x] Data collection con DeFi Llama API
- [x] Dashboard JSON generator
- [x] GitHub Actions automation (cada 6h)
- [x] Sistema de alertas básico

## 🚧 Fase 2: Alertas (Dic 2025)
- [ ] Email alerts (SMTP)
- [ ] SMS alerts (Twilio)
- [ ] Dashboard web básico
- [ ] 10 beta testers

## 📅 Fase 3: API REST (Ene-Feb 2026)
- [ ] FastAPI backend
- [ ] Endpoints /yields, /protocols, /historical
- [ ] JWT authentication
- [ ] Deploy en Railway

## 📅 Fase 4: Monetización (Mar-Abr 2026)
- [ ] Stripe integration
- [ ] Plans: Free, Pro ($15), Enterprise ($50)
- [ ] Landing page
- [ ] 20 suscriptores pagos ($300 MRR)

## 🎯 Objetivos 6 Meses
- 100 usuarios activos
- $1000 MRR
- 20+ protocolos monitoreados
- 99.9% uptime

Ver detalles en README.md
EOF
echo "✅ docs/ROADMAP.md actualizado"
echo ""

# 5. Actualizar docs/MONETIZATION.md
echo "📝 5. Actualizando docs/MONETIZATION.md..."
cat > docs/MONETIZATION.md << 'EOF'
# 💰 Plan de Monetización - DeFi Monitor

## 📊 Modelo de Negocio

### Plans y Pricing

| Plan | Precio | Features |
|------|--------|----------|
| **Free** | $0/mes | Dashboard público, datos cada 6h, sin alertas |
| **Pro** | $15/mes | Alertas email, datos cada 1h, históricos 30 días |
| **Enterprise** | $50/mes | API access, webhooks, históricos ilimitados |

## 🎯 Proyecciones

### Año 1
- Q1: 10 suscriptores ($150 MRR)
- Q2: 20 suscriptores ($400 MRR)
- Q3: 50 suscriptores ($1000 MRR)
- Q4: 100 suscriptores ($2000 MRR)

### Costos Estimados
- Hosting: $20/mes (Railway)
- Twilio SMS: $10/mes
- SendGrid: $15/mes
- **Total:** $45/mes

### Break-even: 3 suscriptores Pro

## 💡 Value Proposition

**Para traders DeFi:**
- Ahorra 2h/día de research manual
- No pierdas yields altos (>50%)
- Históricos para backtesting

**ROI:** Un solo yield alto detectado paga 12 meses de suscripción

## 🚀 Estrategia de Lanzamiento

1. Beta gratuito (2 meses)
2. Trial de 14 días
3. Launch en Twitter/Reddit
4. Programa de afiliados (20% comisión)

EOF
echo "✅ docs/MONETIZATION.md actualizado"
echo ""

# 6. Crear docs/ARCHITECTURE.md
echo "📝 6. Creando docs/ARCHITECTURE.md..."
cat > docs/ARCHITECTURE.md << 'EOF'
# 🏗️ Arquitectura - DeFi Monitor

## 📊 Overview

```
┌─────────────────┐
│  DeFi Llama API │
└────────┬────────┘
         │
         ▼
┌─────────────────────────┐
│ collect_defi_data.py    │ (GitHub Actions cada 6h)
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│  data/protocols.json    │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│ generate_dashboard.py   │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│  data/dashboard.json    │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│  Git Commit (histórico) │
└─────────────────────────┘
```

## 🔧 Components

### 1. Data Collector
- **Archivo:** `scripts/collect_defi_data.py`
- **Input:** DeFi Llama API
- **Output:** `data/protocols.json`
- **Frecuencia:** Cada 6 horas

### 2. Dashboard Generator
- **Archivo:** `scripts/generate_dashboard.py`
- **Input:** `data/protocols.json`
- **Output:** `data/dashboard.json`
- **Features:**
  - Summary stats (TVL, APY)
  - Top 10 protocols
  - Alert detection (APY > 50%)

### 3. Alert System (Futuro)
- **Archivo:** `scripts/send_alerts.py`
- **Channels:** Email (SMTP), SMS (Twilio)
- **Triggers:** Configurables por usuario

### 4. API REST (Futuro)
- **Framework:** FastAPI
- **Endpoints:** /yields, /protocols, /historical
- **Auth:** JWT tokens

## 🗄️ Data Flow

1. **Fetch:** GitHub Actions → DeFi Llama API
2. **Store:** Raw data → `protocols.json`
3. **Process:** Python → Generate summary/alerts
4. **Persist:** Processed → `dashboard.json`
5. **Archive:** Git commit → Historical data

## 🔐 Security

- API keys en `.env` (no commiteado)
- JWT tokens para autenticación
- Rate limiting en API
- HTTPS only

## 📈 Scalability

- **Current:** Single Python process
- **Future:** 
  - FastAPI + Gunicorn
  - PostgreSQL para históricos
  - Redis cache
  - CDN para static assets

EOF
echo "✅ docs/ARCHITECTURE.md creado"
echo ""

echo "✅ Fase 4 completada!"
echo ""
echo "Documentos actualizados:"
echo "  ✅ README.md (nuevo)"
echo "  ✅ QUICK_REFERENCE.md"
echo "  ✅ docs/ROADMAP.md"
echo "  ✅ docs/MONETIZATION.md"
echo "  ✅ docs/ARCHITECTURE.md (nuevo)"
echo ""
echo "Documentos deprecados movidos a docs/legacy/"
