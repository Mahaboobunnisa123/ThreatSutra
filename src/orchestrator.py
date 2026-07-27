"""
Coordinates the ThreatSutra analysis pipeline.
This module orchestrates the flow of data between project inputs,context preparation, AI generation, validation, review, and downstream
integration components.
"""
import os
from dotenv import load_dotenv
from google import genai
from src.adapters.ThreatDragonReader import ThreatDragonReader
from src.adapters.CornucopiaClient import CornucopiaClient
from src.adapters.GitHubMilestoneClient import GitHubMilestoneClient
from prompts import build_evil_user_story_prompt, build_verification_test_prompt
from validation import is_valid_threat, is_valid_card

load_dotenv()

GITHUB_REPO = os.environ.get("GITHUB_REPO", "owaspcornucopia/ThreatSutra")

# A Threat Dragon threat's `type` field tells us which Cornucopia edition
# its card belongs to. Only these two appear in the current model; add
# to this mapping if a future threat model uses one of the others
# (mobileapp, dbd, eop).
EDITION_BY_THREAT_TYPE = {
    "cornucopia": "webapp",
    "cornucopia-companion": "companion",
}
DEFAULT_EDITION = "webapp"

def resolve_edition(threat: dict) -> str:      #Maps a Threat Dragon threat's `type` field to a Cornucopia edition.
    threat_type = threat.get("type")
    if threat_type not in EDITION_BY_THREAT_TYPE:
        raise ValueError(
            f"Unknown Threat Dragon threat type '{threat_type}' - no Cornucopia "
            f"edition mapping exists for it. Add it to EDITION_BY_THREAT_TYPE "
            f"in orchestrator.py (currently mapped types: {sorted(EDITION_BY_THREAT_TYPE)})."
        )
    return EDITION_BY_THREAT_TYPE[threat_type]

def call_ai_model(prompt: str) -> str:     #Sends a prompt to the Gemini model and returns the plain text response using the Google GenAI client. Raises an error if GEMINI_API_KEY is not set.
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is not set. Copy .env.example to .env, "
            "add your key, and load it before running the CLI."
        )
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )
    return response.text.strip()

def generate_evil_user_story(threat: dict) -> str:      #Issue-6: turns threat data into an evil user story. 
    if not is_valid_threat(threat):
        raise ValueError("Threat data did not pass validation.")
    prompt = build_evil_user_story_prompt(threat)
    return call_ai_model(prompt)

def generate_verification_test(card: dict) -> str:      #Issue-5: turns card data into a verification test. 
    if not is_valid_card(card):
        raise ValueError("Card data did not pass validation.")
    prompt = build_verification_test_prompt(card)
    return call_ai_model(prompt)

def process_threat(threat: dict, cornucopia_client: CornucopiaClient, milestones: list) -> dict:
    """
    Processes exactly one Threat Dragon threat: resolves its Cornucopia edition, finds the matching card, and combines threat + card +
    milestone context into one normalized dict. No LLM calls here yet.
    """
    edition = resolve_edition(threat)
    card = cornucopia_client.find_card(edition, threat.get("cardNumber"))
    return {
        "threat": threat,
        "cornucopia_card": card,
        "milestones": milestones,
    }

def run_pipeline() -> list:              #Runs the pipeline for every Threat Dragon threat, one threat at a time, and returns normalized threat+card+milestone context for each 
    threats = ThreatDragonReader().read_threats()
    cornucopia_client = CornucopiaClient()
    milestones = GitHubMilestoneClient(GITHUB_REPO).get_milestones()
    return [process_threat(threat, cornucopia_client, milestones) for threat in threats]
