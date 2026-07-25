"""
cornucopia.py 
Client for retrieving OWASP Cornucopia cards. Uses the Cornucopia API to retrieve all standards for a given edition
and performs card lookups from the cached response. Cards are located by matching the supplied identifier against the
returned standards. 
"""
import requests

BASE_URL = "https://cornucopia.owasp.org/api"
DEFAULT_LANGUAGE = "en"
REQUEST_TIMEOUT_SECONDS = 10

# Every edition the API supports. See EDITION_BY_THREAT_TYPE in
# orchestrator.py for how a threat's `type` field selects one of these.
SUPPORTED_EDITIONS = {"webapp", "mobileapp", "companion", "dbd", "eop"}

class CornucopiaClient:
    """Retrieves and caches Cornucopia cards by edition."""

    def __init__(self, base_url: str = BASE_URL, language: str = DEFAULT_LANGUAGE,
                 timeout: int = REQUEST_TIMEOUT_SECONDS):
        self.base_url = base_url
        self.language = language
        self.timeout = timeout
        self._cards_by_edition = {}  # edition -> standards list, cached per instance

    def get_cards(self, edition: str) -> list:
        """
        Returns every card for one edition. Results are cached per client instance, so looking up several cards from the same
        edition only fetches that edition once.
        """
        if edition not in SUPPORTED_EDITIONS:
            raise ValueError(f"Unknown Cornucopia edition '{edition}'.")
        if edition in self._cards_by_edition:
            return self._cards_by_edition[edition]
        url = f"{self.base_url}/cre/{edition}/{self.language}"
        try:
            response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()
        except requests.RequestException as exc:
            raise RuntimeError(f"Could not fetch Cornucopia edition '{edition}' from {url}: {exc}") from exc
        try:
            payload = response.json()
        except ValueError as exc:
            raise RuntimeError(f"Cornucopia API response for edition '{edition}' from {url} was not valid JSON.") from exc
        standards = payload.get("standards", [])
        self._cards_by_edition[edition] = standards
        return standards

    def find_card(self, edition: str, card_id: str) -> dict:
        """
        Returns the Cornucopia card whose section identifier matches the supplied Threat Dragon card number.
        Raises a RuntimeError if no card is found.
        """
        if not card_id:
            raise ValueError("card_id is required to look up a Cornucopia card.")
        for card in self.get_cards(edition):
            if card.get("sectionID") == card_id:
                return card
        raise RuntimeError(f"No card '{card_id}' found in Cornucopia edition '{edition}'.") 