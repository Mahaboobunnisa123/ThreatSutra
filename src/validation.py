"""
validation.py

Provides the validation interface used throughout the ThreatSutra pipeline.This module currently exposes placeholder validation functions so other
parts of the application can rely on a stable API while the validationlayer evolves.
In the future, these functions will validate data received from external
sources such as:
- OWASP Threat Dragon
- OWASP Cornucopia
- GitHub

Additional validation rules (such as required fields, character restrictions, length limits, and content validation) will be implemented here as the project matures.
"""
MAX_FIELD_LENGTH = 4000        # per text field
MAX_TOTAL_LENGTH = 20000       # all text fields of one object combined
MAX_LIST_LENGTH = 500          # threats / milestones accepted from one source
REQUIRED_THREAT_FIELDS = ("id", "type", "cardNumber", "title", "description", "mitigation")
REQUIRED_CARD_FIELDS = ("sectionID", "name", "description")
REQUIRED_MILESTONE_FIELDS = ("number", "title")
OPTIONAL_CARD_TEXT_FIELDS = ("doctype", "id", "section", "hyperlink", "tooltype")
OPTIONAL_MILESTONE_TEXT_FIELDS = ("description", "state", "html_url")

class ValidationError(ValueError):     # Raised when external data fails validation. Subclasses ValueError so existing callers that catch ValueError keep working.
  def _fail(source: str, message: str) -> None:
    """Raises a ValidationError that names the source and the exact problem."""
    raise ValidationError(f"Invalid {source}: {message}")  

  def is_valid_threat(threat: dict) -> bool:
    """
    Determine whether a Threat Dragon threat is valid. This is currently a placeholder implementation that accepts all input.
    It exists to establish a stable validation interface for the rest of the application.
    Future implementations may verify:
    - Required fields
    - Field types
    - Empty values
    - Character restrictions
    - Maximum field lengths
    - Other validation rules as needed
    Args:
        threat: A dictionary representing a Threat Dragon threat.
    Returns:
        True if the threat is considered valid.
    """
    return True

  def is_valid_card(card: dict) -> bool:
    """
    Determine whether a Cornucopia card is valid.
    This is currently a placeholder implementation that accepts all input. It exists to establish a stable validation interface for the rest of
    the application.
    Future implementations may verify:
    - Required fields
    - Field types
    - Empty values
    - Character restrictions
    - Maximum field lengths
    - Other validation rules as needed
    Args:
        card: A dictionary representing a Cornucopia card.
    Returns:
        True if the card is considered valid.
    """
    return True