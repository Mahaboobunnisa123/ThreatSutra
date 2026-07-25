"""   This file holds the exact wording we send to the AI model. Keeping prompt text here (instead of inside orchestrator.py) means
we can tweak wording without touching the logic that calls the AI.
"""
def build_evil_user_story_prompt(threat: dict) -> str:
    """
    Builds the prompt for Issue #6: generate an evil user story.
    """
    description = threat.get("description", "")
    what_can_go_wrong = threat.get("what_can_go_wrong", "")
    prompt = (
        "You are helping write a security 'evil user story' for a development team.\n\n"
        "An evil user story describes what an attacker could do, written from the "
        "attacker's point of view, so the development team understands the risk.\n\n"
        f"Threat description:\n{description}\n\n"
        f"What can go wrong:\n{what_can_go_wrong}\n\n"
        "Write ONE evil user story in this exact format:\n"
        "As a [type of attacker], I want to [do something bad], "
        "so that [attacker's goal/benefit].\n\n"
        "Keep it to a single sentence. Do not add extra commentary."
    )
    return prompt

def build_verification_test_prompt(card: dict) -> str:
    """
    Builds the prompt for Issue #5: generate a verification test.
    """
    requirement = card.get("requirement", "")
    mitigation = card.get("mitigation", "")
    prompt = (
        "You are helping write a short verification test for a security requirement.\n\n"
        f"Security requirement:\n{requirement}\n\n"
        f"Mitigation guidance:\n{mitigation}\n\n"
        "Write ONE verification test that a developer or tester could follow to check "
        "this requirement is met. Use this format:\n"
        "Given [setup], When [action], Then [expected secure outcome].\n\n"
        "Keep it to a single sentence. Do not add extra commentary."
    )
    return prompt
