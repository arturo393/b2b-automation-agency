# B2B Automation Agency (Powered by Vertex AI)

Transforming manual business processes into automated, intelligent pipelines.

## Value Proposition
We help companies cut operational costs by deploying **Custom AI Agents** that handle:
- 📄 Document Processing (Invoices, Contracts)
- 📧 Lead Qualification & Outreach
- 📊 Data Extraction & Reporting

## Core Technology
- **Engine**: Google Vertex AI + Gemini 1.5 Flash
- **Infrastructure**: Google Cloud Functions / Cloud Run
- **Language**: Python 3.11+

## Getting Started

### 1. Setup Environment
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

### 2. Run the "Hunter" (Sales Agent)
Our internal tool to find clients automatically.

```bash
python -m agency.hunter.main --mode=search --keyword="logistics companies in Chile"
```
