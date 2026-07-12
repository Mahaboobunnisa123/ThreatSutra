""" What it does:
  1. Load sample_data data (Threat Dragon and Cornucopia card)
  2. Build the two prompts using prompts.py
  3. Send each prompt to the AI model
  4. Return the evil user story and the verification test together
"""
import json
import os
from dotenv import load_dotenv
from google import genai
from prompts import build_evil_user_story_prompt, build_verification_test_prompt
from validation import is_valid_threat, is_valid_card
load_dotenv()
PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
SAMPLE_DIR = os.path.join(PROJECT_ROOT, "sample_data")
THREAT_SAMPLE_PATH = os.path.join(SAMPLE_DIR, "threat_dragon_sample.json")
CARD_SAMPLE_PATH = os.path.join(SAMPLE_DIR, "cornucopia_card_sample.json")

def load_data(path: str) -> dict:         #Reads a JSON fixture file from disk and returns it as a dictionary
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

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

def generate_evil_user_story(threat: dict) -> str:      #Issue-6: turns a threat data into an evil user story
    if not is_valid_threat(threat):
        raise ValueError("Threat data did not pass validation.")
    prompt = build_evil_user_story_prompt(threat)
    return call_ai_model(prompt)

def generate_verification_test(card: dict) -> str:      #Issue-5: turns a card data into a verification test.
    if not is_valid_card(card):
        raise ValueError("Card data did not pass validation.")
    prompt = build_verification_test_prompt(card)
    return call_ai_model(prompt)

def run_pipeline() -> dict:              #Runs the pipeline using sample data and returns a dictionary with both generated outputs, ready for human review.
    threat = load_data(THREAT_SAMPLE_PATH)
    card = load_data(CARD_SAMPLE_PATH)
    evil_user_story = generate_evil_user_story(threat)
    verification_test = generate_verification_test(card)
    return {
        "source_threat_id": threat.get("threat_id"),
        "source_card_id": card.get("card_id"),
        "evil_user_story": evil_user_story,
        "verification_test": verification_test,
    }
