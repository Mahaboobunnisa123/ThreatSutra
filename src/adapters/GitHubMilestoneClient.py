"""
Retrieves GitHub milestone information.

This module provides read-only access to GitHub milestone data used as
project context during the ThreatSutra analysis pipeline.
"""
import os
import requests

DEFAULT_TIMEOUT_SECONDS = 10

class GitHubMilestoneClient:
    """Fetches milestones for one GitHub repository."""
    def __init__(self, repo: str, token: str = None, timeout: int = DEFAULT_TIMEOUT_SECONDS):
        self.repo = repo
        self.token = token or os.environ.get("GITHUB_API")
        self.timeout = timeout

    def get_milestones(self, state: str = "open") -> list:
        """
        Returns the repository's milestones. Authenticates with GITHUB_API if it's set, to avoid the
        unauthenticated API's low rate limit; works without one too.Returns [] and prints a warning on any failure, so a milestone
        lookup problem never stops threat/card processing.
        """
        url = f"https://api.github.com/repos/{self.repo}/milestones"
        headers = {"Accept": "application/vnd.github+json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"

        try:
            response = requests.get(url, params={"state": state}, headers=headers, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as exc:
            print(f"Warning: could not fetch GitHub milestones for '{self.repo}': {exc}")
            return []
