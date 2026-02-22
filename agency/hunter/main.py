"""
Main entrypoint for the B2B Automation Agency Hunter.
Uses Vertex AI (Application Default Credentials) — no API key needed.
"""
import argparse
import csv
import os
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

from agency.hunter.lead_scraper import LeadHunter
from agency.hunter.lead_grader import LeadGrader
from agency.hunter.outreach_composer import OutreachComposer
from agency.hunter.page_fetcher import PageFetcher
from agency.product.proof_of_work import generate_proof_of_work


def save_leads(leads: list, output_dir: str = "data", timestamp: str = None):
    Path(output_dir).mkdir(exist_ok=True)
    if not timestamp:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{output_dir}/leads_{timestamp}.csv"
    if not leads:
        return
    with open(filename, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=leads[0].keys())
        writer.writeheader()
        writer.writerows(leads)
    print(f"\n💾 Saved {len(leads)} leads → {filename}")


def log_history(keyword: str, total: int, qualified: int, log_file: str = "data/logs/trading_log.csv"):
    """Saves run summary to a cumulative log (as requested in user memories)."""
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    file_exists = os.path.isfile(log_file)
    with open(log_file, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["timestamp", "keyword", "total_found", "qualified", "status"])
        writer.writerow([
            datetime.now().isoformat(),
            keyword,
            total,
            qualified,
            "SUCCESS" if qualified > 0 else "NO_LEADS"
        ])
    print(f"📖 History updated in {log_file}")


def main():
    parser = argparse.ArgumentParser(description="🦁 B2B Agency Hunter Agent")
    parser.add_argument("--keyword", type=str, default="logistics companies chile",
                        help="Search keyword to find leads")
    parser.add_argument("--limit", type=int, default=5,
                        help="Number of leads to process")
    parser.add_argument("--min-score", type=int, default=5,
                        help="Minimum score (0-10) to qualify a lead")
    parser.add_argument("--proof", action="store_true",
                        help="Generate a Proof-of-Work report for qualified leads")
    parser.add_argument("--history", action="store_true",
                        help="Log the run results to central history file")
    args = parser.parse_args()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    print("\n🦁 The Hunter is waking up...")
    print(f"   Keyword : {args.keyword}")
    print(f"   Limit   : {args.limit}")
    print(f"   Min Score: {args.min_score}/10\n")

    # 1. Find Leads
    hunter = LeadHunter()
    leads = hunter.hunt(args.keyword, num_results=args.limit)

    if not leads:
        print("❌ No leads found. Try a different keyword.")
        return

    # 2. Grade Leads
    grader = LeadGrader()
    composer = OutreachComposer()
    fetcher = PageFetcher()
    qualified = []

    print(f"\n🧠 Processing {len(leads)} leads...\n")
    for lead in leads:
        url = lead.get("url")
        # Try to fetch real content, fallback to snippets
        page_text = fetcher.fetch(url) if url else ""
        
        if not page_text or len(page_text) < 200:
            print(f"   ℹ️  Page text too short/missing, using search snippet for: {lead.get('title')}")
            page_text = lead.get("description", "") + " " + lead.get("title", "")
        
        scored = grader.grade_lead(lead, page_text=page_text)

        if scored.get("score", 0) >= args.min_score:
            # 3. Write personalized email
            email = composer.compose_email(scored)
            scored["email_draft"] = email
            
            # Save email to a separate file for easy access
            outbox_path = f"outbox/email_{scored.get('company_name', 'Lead').replace(' ', '_')}_{timestamp}.txt"
            os.makedirs("outbox", exist_ok=True)
            with open(outbox_path, "w") as f_email:
                f_email.write(email)
            scored["email_file"] = outbox_path

            print(f"\n📧 Email Draft Saved to: {outbox_path}")
            print(f"{'─'*50}\n{email}\n{'─'*50}")

            # 4. (Optional) Generate Proof of Work attachment
            if args.proof:
                pow_path = generate_proof_of_work(scored.get("company_name", "Prospect"))
                scored["proof_of_work"] = pow_path

            qualified.append(scored)
        else:
            name = scored.get("company_name", scored.get("title", "Unknown"))
            print(f"   🚫 Disqualified: {name} ({scored.get('score', 0)}/10)")

    # 5. Save results
    save_leads(qualified, timestamp=timestamp)
    if args.history:
        log_history(args.keyword, len(leads), len(qualified))
    
    print(f"\n✅ Done. {len(qualified)}/{len(leads)} leads qualified.")


if __name__ == "__main__":
    main()
