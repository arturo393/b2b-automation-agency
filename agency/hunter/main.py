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
from agency.product.proof_of_work import generate_proof_of_work


def save_leads(leads: list, output_dir: str = "data"):
    Path(output_dir).mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{output_dir}/leads_{timestamp}.csv"
    if not leads:
        return
    with open(filename, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=leads[0].keys())
        writer.writeheader()
        writer.writerows(leads)
    print(f"\n💾 Saved {len(leads)} leads → {filename}")


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
    args = parser.parse_args()

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
    qualified = []

    print(f"\n🧠 Grading {len(leads)} leads with Vertex AI...\n")
    for lead in leads:
        # In production: fetch real page text via requests + BeautifulSoup
        page_text = lead.get("description", "") + " " + lead.get("title", "")
        scored = grader.grade_lead(lead, page_text=page_text)

        if scored.get("score", 0) >= args.min_score:
            # 3. Write personalized email
            email = composer.compose_email(scored)
            scored["email_draft"] = email
            print(f"\n📧 Email Draft:\n{'─'*50}\n{email}\n{'─'*50}")

            # 4. (Optional) Generate Proof of Work attachment
            if args.proof:
                pow_path = generate_proof_of_work(scored.get("company_name", "Prospect"))
                scored["proof_of_work"] = pow_path

            qualified.append(scored)
        else:
            name = scored.get("company_name", scored.get("title", "Unknown"))
            print(f"   🚫 Disqualified: {name} ({scored.get('score', 0)}/10)")

    # 5. Save results
    save_leads(qualified)
    print(f"\n✅ Done. {len(qualified)}/{len(leads)} leads qualified.")


if __name__ == "__main__":
    main()
