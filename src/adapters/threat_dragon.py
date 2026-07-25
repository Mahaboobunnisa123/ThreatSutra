"""
threat_dragon.py

Reads and parses Threat Dragon threat models. This module loads Threat Dragon JSON files and extracts structured
threat information for use throughout the ThreatSutra pipeline.
"""
import json
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DFD_PATH = os.path.join(PROJECT_ROOT, "docs", "diagrams", "DFD_ThreatSutra.json")

class ThreatDragonReader:
    """Reads every threat out of a Threat Dragon model file."""
    def __init__(self, path: str = DFD_PATH):
        self.path = path

    def read_threats(self) -> list:
        """
        Returns every threat found anywhere in the model, as a flat list of dicts, in the order they appear. Threats are returned exactly
        as Threat Dragon stores them (title, description, mitigation, cardNumber, type, etc.) - no field renaming here, so nothing is
        silently lost before later issues decide how to use each field.A diagram or cell with no threats (e.g. a diagram that hasn't
        been threat-modeled yet) is simply skipped, not an error.
        """
        with open(self.path, "r", encoding="utf-8") as f:
            model = json.load(f)
        threats = []
        diagrams = model.get("detail", {}).get("diagrams", [])
        for diagram in diagrams:
            for cell in diagram.get("cells", []):
                cell_data = cell.get("data", {})
                threats.extend(cell_data.get("threats", []))
        return threats
