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

class ValidationError(ValueError): # Raised when external data fails validation. Subclasses ValueError so existing callers that catch ValueError keep working.
    pass
def _fail(source: str, message: str) -> None:
    """Raises a ValidationError that names the source and the exact problem."""
    raise ValidationError(f"Invalid {source}: {message}")

def _require_mapping(value, source: str) -> None:
    if not isinstance(value, dict):
        _fail(source, f"expected a JSON object, got {type(value).__name__}.")

def _has_control_chars(text: str) -> bool:
    """True if text contains control characters other than tab/newline/carriage return."""
    return any(ord(ch) < 32 and ch not in "\t\n\r" for ch in text)

def _validate_text(value, field: str, source: str, required: bool = True) -> int:
    """
    Validates one text field and returns its length.
    Checks type, emptiness (when required), control characters, and length cap.
    """
    if value is None:
        if required:
            _fail(source, f"required field '{field}' is missing or null.")
        return 0
    if not isinstance(value, str):
        _fail(source, f"field '{field}' must be text, got {type(value).__name__}.")
    if required and not value.strip():
        _fail(source, f"required field '{field}' is empty.")
    if len(value) > MAX_FIELD_LENGTH:
        _fail(source, f"field '{field}' is {len(value)} characters, over the {MAX_FIELD_LENGTH} limit.")
    if _has_control_chars(value):
        _fail(source, f"field '{field}' contains control characters and was rejected.")
    return len(value)

def _validate_total_length(total: int, source: str) -> None:
    if total > MAX_TOTAL_LENGTH:
        _fail(source, f"combined text is {total} characters, over the {MAX_TOTAL_LENGTH} limit.")

def _validate_list(items, source: str) -> None:
    if not isinstance(items, list):
        _fail(source, f"expected a list, got {type(items).__name__}.")
    if len(items) > MAX_LIST_LENGTH:
        _fail(source, f"{len(items)} items received, over the {MAX_LIST_LENGTH} limit.")

def sanitize_text(text: str) -> str:
    """
    Strips control characters from text so it is safe to print or store.
    Provided here so later issues (review display, LLM output handling) reuse
    one implementation instead of writing their own.
    """
    if not isinstance(text, str):
        return ""
    return "".join(ch for ch in text if ord(ch) >= 32 or ch in "\t\n")

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