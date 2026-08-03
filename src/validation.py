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

def validate_threat(threat: dict) -> dict:
    """
    Validates one Threat Dragon threat and returns it unchanged.
    Raises ValidationError naming the offending field.
    """
    _require_mapping(threat, "Threat Dragon threat")
    source = f"Threat Dragon threat '{threat.get('id', '<no id>')}'"
    total = 0
    for field in REQUIRED_THREAT_FIELDS:
        total += _validate_text(threat.get(field), field, source)
    _validate_total_length(total, source)
    return threat

def validate_card(card: dict) -> dict:
    """
    Validates one Cornucopia card from the API and returns it unchanged.
    Only sectionID is required, since that is the field the card lookup matches on;
    other text fields are validated when present.
    """
    _require_mapping(card, "Cornucopia card")
    source = f"Cornucopia card '{card.get('sectionID', '<no sectionID>')}'"
    total = 0
    for field in REQUIRED_CARD_FIELDS:
        total += _validate_text(card.get(field), field, source)
    for field in OPTIONAL_CARD_TEXT_FIELDS:
        if field in card:
            total += _validate_text(card.get(field), field, source, required=False)
    for field in ("links", "tags"):
        if field in card and not isinstance(card[field], list):
            _fail(source, f"field '{field}' must be a list, got {type(card[field]).__name__}.")        
    _validate_total_length(total, source)
    return card

def validate_milestone(milestone: dict) -> dict:
    """
    Validates one GitHub milestone and returns it unchanged.
    'number' must be an integer; 'title' must be non-empty text.
    """
    _require_mapping(milestone, "GitHub milestone")
    source = f"GitHub milestone '{milestone.get('number', '<no number>')}'"
    number = milestone.get("number")
    if not isinstance(number, int) or isinstance(number, bool):
        _fail(source, f"field 'number' must be an integer, got {type(number).__name__}.")
    total = _validate_text(milestone.get("title"), "title", source)
    for field in OPTIONAL_MILESTONE_TEXT_FIELDS:
        if field in milestone:
            total += _validate_text(milestone.get(field), field, source, required=False)
    _validate_total_length(total, source)
    return milestone

def validate_threats(threats: list) -> list:
    """Validates every threat read from a Threat Dragon model. Fails closed on the first bad entry."""
    _validate_list(threats, "Threat Dragon threat list")
    for index, threat in enumerate(threats):
        try:
            validate_threat(threat)
        except ValidationError as exc:
            raise ValidationError(f"Threat at position {index}: {exc}") from exc
    return threats


def validate_milestones(milestones: list) -> list:
    """Validates every milestone fetched from GitHub. Fails closed on the first bad entry."""
    _validate_list(milestones, "GitHub milestone list")
    for index, milestone in enumerate(milestones):
        try:
            validate_milestone(milestone)
        except ValidationError as exc:
            raise ValidationError(f"Milestone at position {index}: {exc}") from exc
    return milestones

def is_valid_threat(threat: dict) -> bool:
    """
    Determines whether a Threat Dragon threat is valid.
    Use validate_threat() instead when you need the reason for the failure.
    Args:
        threat: A dictionary representing a Threat Dragon threat.
    Returns:
        True if the threat passes validation, False otherwise.
    """
    try:
        validate_threat(threat)
    except ValidationError:
        return False
    return True

def is_valid_card(card: dict) -> bool:
    """
    Determines whether a Cornucopia card is valid.
    Use validate_card() instead when you need the reason for the failure.
    Args:
        card: A dictionary representing a Cornucopia card.
    Returns:
        True if the card passes validation, False otherwise.
    """
    try:
        validate_card(card)
    except ValidationError:
        return False
    return True

def is_valid_milestone(milestone: dict) -> bool:
    """
    Determines whether a GitHub milestone is valid.
    Use validate_milestone() instead when you need the reason for the failure.
    Args:
        milestone: A dictionary representing a GitHub milestone.
    Returns:
        True if the milestone passes validation, False otherwise.
    """
    try:
        validate_milestone(milestone)
    except ValidationError:
        return False
    return True
