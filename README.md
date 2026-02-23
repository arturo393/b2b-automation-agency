# 🦁 B2B Automation Agency

**Intelligent Sales Agents & Document Pipelines Powered by Gemini 2.5 Flash**

This repository is a fully operational Automated Sales Agency. It uses AI to solve the two biggest bottlenecks in B2B business: **Lead Generation** and **Document Backlog**.

---

## 🛠 Project Structure

- **`agency/`**: Core intelligence modules.
  - **`hunter/`**: The "Hunter" sales agent. Finds, grades, and reaches out to leads.
  - **`product/`**: The "Document Intelligence" product. Multimodal PDF/Image parsing.
  - **`utils/`**: Shared Gemini client and helper modules.
- **`infrastructure/`**: Terraform configurations for Cloud Run and Artifact Registry.
- **`scripts/`**: Deployment and utility scripts.
- **`data/`**: Results from the Hunter runs (Leads CSVs, Logs).
- **`outbox/`**: Personalized email drafts and "Proof of Work" reports for prospects.
- **`archive/`**: Legacy project files.

---

## 🚀 Key Features

### 1. 🦁 The Hunter (Sales Agent)
An autonomous agent that:
1.  **Hunts**: Searches Google for businesses in specific niches.
2.  **Analyzes**: "Browses" the prospect's website to understand their business.
3.  **Grades**: Uses Gemini to score the lead based on automation potential.
4.  **Drafts**: Composes highly personalized cold emails.
5.  **Proves**: Generates a PDF "Proof of Work" showcasing your intelligence capabilities.

### 2. 📄 Document Intelligence Pipeline
A multimodal engine that converts unstructured documents into actionable data:
- **Vision Support**: Parses PNGs, JPEGs, and PDFs.
- **Structured Output**: Returns clean JSON for invoices, contracts, and POs.
- **Cost Efficient**: Optimized for Gemini 2.5 Flash.

### 3. 🏛️ GovTech Bidding Agent
A specialized agent for public sector tenders ("Licitaciones"):
- **Analyzer**: Reads heavy "Bases Técnicas" PDFs to extract budgets, deadlines, and technical requirements.
- **Scorer**: Evaluates our technical fit and recommends Bid / No-Bid.
- **Proposal Drafter**: Automatically drafts a Technical Proposal outline in Markdown tailored to the tender's requirements.

---

## ⚙️ Quick Start

### 1. Setup
```bash
# Clone and install
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Configure environment (Gemini API Key needed)
cp .env.example .env
```

### 2. Find Leads
```bash
python3 -m agency.hunter.main --keyword="logistics companies chile" --limit=3 --proof --history
```

### 3. Parse a Document
```bash
python3 tests/test_parser_multimodal.py
```

---

## 🛡 Go-To-Market
Check out `GO_TO_MARKET.md` for the full strategy on how to use this code to get your first paying B2B client.

---

## ☁️ Deployment
Managed via Terraform. Deploy to Google Cloud Run Jobs for on-demand execution:
```bash
./scripts/deploy_demo.sh
```
