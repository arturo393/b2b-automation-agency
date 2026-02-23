# 👔 B2B Brand Authority & Professionalism

To close high-ticket contracts ($5,000+ USD), the agency must look like a solid partner, not a freelance experiment. This guide outlines the setup for Issue #21.

---

## 1. LinkedIn Profile Optimization
Your personal brand is the first thing a CEO/COO will check after receiving your email.

### Headline Template:
> **Founder @ [Agency Name] | Helping [Niche] Companies Save 60% in Operational Costs via Intelligent AI Automation | GovTech & B2B Specialist**

### About Section Structure:
1. **The Hook**: "Did you know that 40% of administrative time in [Industry] is lost in manual data entry?"
2. **The Result**: "We deploy custom AI agents that process complex documents (Invoices, BLs, Contracts) in milliseconds with 99.5% accuracy."
3. **The Proof**: "Built on Gemini 2.5 Flash, our pipelines integrate directily into SAP, Softland, and major ERPs."
4. **Call to Action**: "Send me a DM for a 5-min demo of your own documents being parsed."

---

## 2. Professional Email Setup (DNS)
Before running **The Hunter**, you MUST set up these three records in your domain's DNS to avoid being flagged as SPAM.

### A. SPF (Sender Policy Framework)
Tells the world which servers are allowed to send email for you.
- **Value (Google Workspace)**: `v=spf1 include:_spf.google.com ~all`

### B. DKIM (DomainKeys Identified Mail)
Adds a digital signature to your emails.
- **Action**: Generate this key in your Google Workspace Admin Console and add it as a TXT record.

### C. DMARC (Domain-based Message Authentication)
Tells servers what to do if SPF or DKIM fails.
- **Value (Initial)**: `v=DMARC1; p=none; rua=mailto:admin@yourdomain.com`

---

## 3. Email "Warmup" Strategy
Do NOT send 100 emails on day 1 with a new domain.
1. **Week 1**: Send 5-10 manual emails to friends/colleagues. Have them reply and mark as "Not Spam".
2. **Week 2**: Use an automated warmup tool (e.g., Apollo, Instantly, or Woodpecker).
3. **Week 3**: Start the **Hunter** at low volume (10-15 emails/day).

---

## 4. Brand Assets
- **Logo**: Sleek, minimalist, high-contrast. Use blue/dark-mode colors to project stability.
- **Signature**: Keep it clean. Name, Role, Link to Loom Demo, and a small "Powered by Gemini" badge to show tech-savviness.
