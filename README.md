# 📊 DeFi Monitor - Dashboard Automatizado

> Monitor automatizado de yields en DeFi - Tracking en tiempo real de protocolos DeFi con alertas inteligentes

[![GitHub Actions](https://img.shields.io/badge/CI-GitHub%20Actions-2088FF?logo=github-actions)](https://github.com/arturo393/defi-monitor/actions)
[![Python 3.11](https://img.shields.io/badge/Python-3.11-3776AB?logo=python)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 🎯 Objetivo

Crear un dashboard automatizado que:
- 📊 **Monitorea yields** de 20+ protocolos DeFi en tiempo real
- 🔔 **Envía alertas** cuando yields superan umbrales configurables
- 📈 **Guarda histórico** de APYs para análisis de tendencias
- 🤖 **Actualiza automáticamente** cada 6 horas vía GitHub Actions
- 💰 **Genera ingresos** mediante suscripciones ($15/mes)

---

## 🛠️ Tech Stack

- **Python 3.11** - Backend y automatización
- **DeFi Llama API** - Datos en tiempo real de protocolos DeFi
- **GitHub Actions** - CI/CD y automatización de updates
- **Jira** - Project management y tracking
- **JSON** - Formato de datos para dashboard

---

## 📁 Estructura del Proyecto

```
defi-monitor/
├── .github/
│   └── workflows/
│       └── monitor-dashboard.yml    # Automation (cada 6h)

## Modo Silencioso
- Sin notificaciones externas: no Email/SMS.
- Genera solo logs y `data/dashboard.json`.
- `JIRA_PROJECT_KEY=DM` y `DATABASE_URL` son opcionales para integraciones.

├── scripts/
│   ├── collect_defi_data.py         # Fetch datos DeFi Llama
│   ├── generate_dashboard.py        # Generar JSON dashboard
│   ├── jira_integration.py          # Integración Jira
│   └── legacy/                      # Scripts obsoletos (Newsletter)
├── data/
│   ├── protocols.json               # Datos de protocolos
│   └── dashboard.json               # Dashboard generado
├── docs/
│   ├── ROADMAP.md                   # Plan de desarrollo
│   ├── MONETIZATION.md              # Estrategia de monetización
│   └── ARCHITECTURE.md              # Arquitectura técnica
├── learning/
│   ├── aave-notes.md                # Notas sobre Aave
│   └── defi-glossary.md             # Glosario DeFi
├── .env.example                     # Variables de entorno
├── requirements.txt                 # Dependencias Python
└── README.md                        # Este archivo
```

---

## 🚀 Quick Start

### 1. Clonar el repositorio

```bash
git clone https://github.com/arturo393/defi-monitor.git
cd defi-monitor
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Configurar variables de entorno

```bash
cp .env.example .env
nano .env  # Editar con tus credenciales
```

**Variables requeridas:**
```bash
# Jira (para project management)
JIRA_EMAIL=your-email@example.com
JIRA_API_TOKEN=your-token
JIRA_SERVER=https://your-domain.atlassian.net
JIRA_PROJECT_KEY=DM

# DeFi Llama API (no requiere token)
DEFI_LLAMA_BASE_URL=https://api.llama.fi
```

### 4. Ejecutar scripts

```bash
# Recolectar datos de DeFi Llama
python scripts/collect_defi_data.py

# Generar dashboard JSON
python scripts/generate_dashboard.py

# Verificar dashboard generado
cat data/dashboard.json
```

---

## �� Dashboard JSON Schema

El archivo `data/dashboard.json` contiene:

```json
{
  "updated_at": "2025-11-28T20:00:00",
  "version": "1.0",
  "summary": {
    "total_protocols": 10,
    "avg_tvl": 34664707531,
    "total_tvl": 346647075319,
    "avg_apy": 5.2,
    "max_apy": 12.5
  },
  "top_protocols": [
    {
      "name": "Lido",
      "tvl": 32000000000,
      "apy": 3.2,
      "category": "Liquid Staking"
    }
  ],
  "alerts": [
    {
      "protocol": "Aave V3",
      "apy": 55.3,
      "type": "high_yield",
      "severity": "medium",
      "message": "Aave V3 tiene APY de 55.30% (>50%)"
    }
  ],
  "metadata": {
    "source": "DeFi Llama API",
    "refresh_interval": "6 hours"
  }
}
```

---

## 🤖 Automatización

### GitHub Actions Workflow

El dashboard se actualiza **automáticamente cada 6 horas**:

- **Horarios:** 00:00, 06:00, 12:00, 18:00 UTC
- **Workflow:** `.github/workflows/monitor-dashboard.yml`
- **Pasos:**
  1. Fetch datos de DeFi Llama
  2. Generar dashboard JSON
  3. Verificar alertas
  4. Commit automático de datos actualizados

### Ejecución Manual

```bash
# Trigger workflow desde GitHub UI:
Actions → DeFi Monitor Dashboard Update → Run workflow

# O ejecutar localmente:
./scripts/refactor_phase3.sh
```

---

## 🔔 Sistema de Alertas

### Criterios de Alerta

| Tipo | Condición | Severidad |
|------|-----------|-----------|
| `high_yield` | APY > 50% | Medium |
| `high_yield` | APY > 100% | High |

### Configuración Futura (Roadmap)

- ✅ Detección automática de yields altos
- 🚧 Envío por email (SMTP)
- 🚧 Envío por SMS (Twilio)
- 🚧 Webhooks para integraciones custom

---

## 💰 Monetización

### Modelo de Negocio

| Plan | Precio | Features |
|------|--------|----------|
| **Free** | $0/mes | Dashboard público, datos cada 6h |
| **Pro** | $15/mes | Alertas email, datos cada 1h, históricos 30 días |
| **Enterprise** | $50/mes | API access, webhooks, históricos ilimitados |

Ver más en [docs/MONETIZATION.md](docs/MONETIZATION.md)

---

## 📈 Roadmap

### ✅ Fase 1: MVP (Completado)
- [x] Recolección de datos DeFi Llama
- [x] Generación de dashboard JSON
- [x] Automatización GitHub Actions
- [x] Sistema de alertas básico

### 🚧 Fase 2: Alertas (En progreso)
- [ ] Integración SMTP para emails
- [ ] Integración Twilio para SMS
- [ ] Configuración de umbrales personalizados
- [ ] Dashboard web básico (frontend)

### 📅 Fase 3: API REST (Q1 2026)
- [ ] FastAPI backend
- [ ] Endpoints para yields, protocolos, históricos
- [ ] Autenticación JWT
- [ ] Rate limiting

### 📅 Fase 4: Monetización (Q2 2026)
- [ ] Integración Stripe
- [ ] Sistema de suscripciones
- [ ] Dashboard premium features
- [ ] Analytics y métricas de usuarios

Ver roadmap completo en [docs/ROADMAP.md](docs/ROADMAP.md)

---

## 🧪 Testing

```bash
# Test data collection
python scripts/collect_defi_data.py

# Test dashboard generation
python scripts/generate_dashboard.py

# Verify JSON output
cat data/dashboard.json | python -m json.tool
```

---

## 📚 Documentación

- **[ROADMAP.md](docs/ROADMAP.md)** - Plan de desarrollo a 6 meses
- **[MONETIZATION.md](docs/MONETIZATION.md)** - Estrategia de ingresos
- **[ARCHITECTURE.md](docs/ARCHITECTURE.md)** - Arquitectura técnica
- **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - Comandos útiles
- **[MIGRATION_PLAN.md](MIGRATION_PLAN.md)** - Plan de migración desde Newsletter

---

## 🔗 Links Útiles

- **GitHub Repo:** [github.com/arturo393/defi-monitor](https://github.com/arturo393/defi-monitor)
- **DeFi Llama API:** [docs.llama.fi](https://defillama.com/docs/api)
- **Jira Board:** [averas-1744767979220.atlassian.net](https://averas-1744767979220.atlassian.net)

---

## 🤝 Contribuir

Este es un proyecto personal, pero las sugerencias son bienvenidas:

1. Fork el repo
2. Crea una branch (`git checkout -b feature/amazing-feature`)
3. Commit tus cambios (`git commit -m 'Add amazing feature'`)
4. Push a la branch (`git push origin feature/amazing-feature`)
5. Abre un Pull Request

---

## 📝 Changelog

### v1.0.0 (28 Nov 2025) - Migración de DeFi Newsletter

**BREAKING CHANGES:**
- Migrado de `defi-newsletter` a `defi-monitor`
- Newsletter generation eliminada
- Focus en dashboard automatizado con yields

**Nuevas Features:**
- ✅ Dashboard JSON generator
- ✅ GitHub Actions automation (cada 6h)
- ✅ Sistema de alertas (APY > 50%)
- ✅ Integración DeFi Llama API

**Deprecado:**
- ❌ Beehiiv/Substack publishing
- ❌ Newsletter Markdown generation
- ❌ Weekly schedule (ahora cada 6h)

Ver detalles completos en [MIGRATION_PLAN.md](MIGRATION_PLAN.md)

---

## 📄 Licencia

MIT License - Ver [LICENSE](LICENSE) para más detalles

---

## 👨‍💻 Autor

**Arturo** - [GitHub](https://github.com/arturo393)

---

## 🙏 Agradecimientos

- **DeFi Llama** - Por proveer API gratuita de datos DeFi
- **GitHub Actions** - Por automatización CI/CD gratuita
- **Python Community** - Por excelentes librerías

---

**¿Te gusta este proyecto?** Dale una ⭐ en GitHub!
