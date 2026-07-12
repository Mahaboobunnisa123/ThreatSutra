"""
validation.py

The DFD identifies several threats (for example VE3 - unvalidated input)
that this file will eventually defend against, by checking that data
coming from GitHub issues, the Cornucopia API, and the Threat Dragon
JSON file is well-formed and safe before it reaches the AI orchestrator.

For NOW, we only define the shape of these functions so the rest of
the code can import and call them. They currently allow everything
through. Real checks will be added in a later week once the input
validation approach is agreed with the mentor.
"""

def is_valid_threat(threat: dict) -> bool:
    """
    PLACEHOLDER. Will eventually check that a threat dictionary has the
    required fields and that text fields don't contain unexpected or
    unsafe characters. For now, always returns True.
    """
    # TODO: real validation - required fields, character whitelist, length limits
    return True

def is_valid_card(card: dict) -> bool:
    """
    PLACEHOLDER. Will eventually check that a Cornucopia card dictionary
    has the required fields and safe content. For now, always returns True.
    """
    # TODO: real validation - required fields, character whitelist, length limits
    return True
