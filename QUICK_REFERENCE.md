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

