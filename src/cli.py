"""
Command-line interface for ThreatSutra.
This module is the entry point for running the ThreatSutra pipeline.
It starts the orchestration process, displays analysis progress, and
presents the generated results through a command-line interface.
Additional helper functions support user interaction and output handling
used by the CLI.
"""
import os
import json
from datetime import datetime
from orchestrator import run_pipeline


def print_header(text: str) -> None:
    print("\n" + "=" * 60)
    print(text)
    print("=" * 60)

def ask_for_approval() -> str: #Prompts the user to review and approve generated content before it is finalized.
    while True:
        choice = input(
            "\nApprove this output? [y]es / [n]o / [e]dit manually: "
        ).strip().lower()
        if choice in ("y", "yes"):
            return "approve"
        if choice in ("n", "no"):
            return "reject"
        if choice in ("e", "edit"):
            return "edit"
        print("Please type y, n, or e.")

def edit_text(label: str, current_text: str) -> str:
    print(f"\nCurrent {label}:\n{current_text}")
    new_text = input(
        f"Type the replacement {label} (or press Enter to keep it):\n> "
    ).strip()
    return new_text if new_text else current_text

def save_output(result: dict, decision: str) -> None:    #Saves the reviewed output to the outputs/ folder as a JSON file.
    project_root = os.path.dirname(os.path.dirname(__file__))
    output_dir = os.path.join(project_root, "outputs")
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"review_{timestamp}.json"
    output_path = os.path.join(output_dir, filename)
    output_data = {
        "timestamp": timestamp,
        "decision": decision,
        "source_threat_id": result["source_threat_id"],
        "source_card_id": result["source_card_id"],
        "evil_user_story": result["evil_user_story"],
        "verification_test": result["verification_test"],
    }
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=4, ensure_ascii=False)
    print(f"\nOutput saved successfully to:\n{output_path}")

def main():
    print_header("ThreatSutra")
    print("Loading project data and preparing security analysis...")
    results = run_pipeline()
    for index, result in enumerate(results, start=1):
        threat = result["threat"]
        card = result["cornucopia_card"]
        print_header(f"THREAT {index} of {len(results)} (number: {threat.get('number')})")
        print(f"Title       : {threat.get('title')}")
        print(f"Card        : {card.get('id')} - {card.get('name')}")
        print(f"Milestones  : {len(result['milestones'])} open")
    print_header("Analysis Complete")
    print(f"Successfully processed {len(results)} threat(s).")

if __name__ == "__main__":
    main()