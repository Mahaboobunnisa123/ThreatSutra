""" 
cli.py - Entry point for ThreatSutra.
What it does:
  1. Runs the orchestrator to generate an evil user story and a verification test
  2. Shows both on screen
  3. Asks you to approve, reject, or edit (Issue #7 human review gate)
"""
import os
import json
from datetime import datetime
from orchestrator import run_pipeline

def print_header(text: str) -> None:
    print("\n" + "=" * 60)
    print(text)
    print("=" * 60)

def ask_for_approval() -> str:
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
    print_header("ThreatSutra: Evil User Story + Verification Test Generator")
    print("Generating evil user story and verification test from sample data...")
    result = run_pipeline()
    print_header("GENERATED EVIL USER STORY")
    print(result["evil_user_story"])
    print_header("GENERATED VERIFICATION TEST")
    print(result["verification_test"])
    decision = ask_for_approval()
    if decision == "reject":
        save_output(result, "rejected")
        print("\nRejected. Output has been saved.")
        return
    if decision == "edit":
        result["evil_user_story"] = edit_text("evil user story", result["evil_user_story"])
        result["verification_test"] = edit_text("verification test",result["verification_test"])
        print_header("FINAL OUTPUT AFTER EDIT")
        print(f"Evil user story  : {result['evil_user_story']}")
        print(f"Verification test: {result['verification_test']}")
        save_output(result, "edited")
    elif decision == "approve":
        save_output(result, "approved")
        print("The generated Evil User Story and Verification Test have been approved.")
    print_header("REVIEW COMPLETED")
    print("Human review completed successfully.")
    print("The reviewed output has been saved in the outputs folder.")

if __name__ == "__main__":
    main()