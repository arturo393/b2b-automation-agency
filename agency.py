import argparse
import sys
from agency.hunter import main as hunter_main
from agency.product.tender_analyzer import TenderAnalyzer
from agency.product.proposal_drafter import ProposalDrafter

def run_hunt(args):
    # Hijack sys.argv and call hunter main
    sys.argv = [sys.argv[0]]
    if args.keyword:
        sys.argv.extend(["--keyword", args.keyword])
    if args.limit:
        sys.argv.extend(["--limit", str(args.limit)])
    if args.proof:
        sys.argv.append("--proof")
    if args.history:
        sys.argv.append("--history")
    hunter_main.main()

def run_bid(args):
    analyzer = TenderAnalyzer()
    analysis = analyzer.analyze_file(args.file)
    print("\n🏛️ Tender Analysis Complete:")
    import json
    print(json.dumps(analysis, indent=2, ensure_ascii=False))

    if analysis.get("bid_recommendation") and args.draft:
        drafter = ProposalDrafter()
        drafter.draft_proposal(analysis)

def main():
    parser = argparse.ArgumentParser(description="🦁 B2B Automation Agency CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Hunt Command
    hunt_parser = subparsers.add_parser("hunt", help="Find and grade private sector leads")
    hunt_parser.add_argument("--keyword", type=str, help="Search keyword")
    hunt_parser.add_argument("--limit", type=int, help="Number of leads")
    hunt_parser.add_argument("--proof", action="store_true", help="Generate Proof of Work")
    hunt_parser.add_argument("--history", action="store_true", help="Log results to history")

    # Bid Command
    bid_parser = subparsers.add_parser("bid", help="Analyze government tenders (Licitaciones)")
    bid_parser.add_argument("--file", type=str, required=True, help="Path to Tender PDF or Text file")
    bid_parser.add_argument("--draft", action="store_true", help="Automatically draft a technical proposal if recommended")

    args = parser.parse_args()

    if args.command == "hunt":
        run_hunt(args)
    elif args.command == "bid":
        run_bid(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
