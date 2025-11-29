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

