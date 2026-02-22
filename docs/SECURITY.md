# 🛡️ Security Strategy: B2B Automation Agency

## 1. Data Privacy Policy
- **Zero-Logging of Content**: We extract data and deliver JSON. We do not store client document originals unless explicitly requested for backup purposes.
- **In-Memory Processing**: Use Cloud Run temporary storage for processing, ensuring data is wiped upon container termination.

## 2. Infrastructure Security (GCP)
- **Secret Manager**: Move all API Keys (Gemini, Google Search) to GCP Secret Manager.
- **IAM (Identity & Access Management)**: Use specific Service Accounts for:
  - `hunter-sa`: Search and analyze leads.
  - `pipeline-sa`: Process client documents.
- **VPC Service Controls**: (Next step) Isolate processing environment from the public internet where possible.

## 3. Compliance Roadmap
- [ ] Implement data encryption at rest (CMEK).
- [ ] Define a clear Data Processing Agreement (DPA) for clients.
- [ ] Audit logs for every API call made by the system.
