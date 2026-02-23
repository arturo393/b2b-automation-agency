# Changelog

All notable changes to this project will be documented in this file.

## [1.0.0] - 2026-02-22
### Added
- **Lion Hunter Agent**: Autonomous B2B lead generation agent.
- **Multimodal Document Intelligence**: Parsing of PDFs and images using Gemini 2.5 Flash.
- **GovTech Bidding Agent**: Automated analysis of Technical Requirements (Bases Técnicas) and Technical Proposal generation for government tenders.
- **Infrastructure as Code**: Terraform configurations for GCP Cloud Run and Artifact Registry.
- **Page Fetcher**: Web scraping capability for deeper lead analysis.
- **Enhanced Outreach Composer**: Personalized email generation based on web scraping data.
- **Go-To-Market Strategy**: Comprehensive guide for agency operation.

### Changed
- **Repository Transformation**: Migrated project from DeFi/Freelance portfolio to B2B Automation Agency.
- **Gemini Transition**: Moved from Vertex AI ADC to direct REST API with programmatic key management.
- **Architecture**: Improved data storage with separate `data/` and `outbox/` directories.

### Fixed
- Lead Scraper reliability through a 3-tier fallback system (CSE, GoogleSearch, Mock).
- Multimodal parsing with Base64 encoding for REST API compatibility.
- Main execution loop stability and error handling.
