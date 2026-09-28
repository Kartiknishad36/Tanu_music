import re
from typing import Tuple, Optional

class SpotifyUtils:
    def __init__(self):
        self.url_regex = re.compile(
            r"(?:https?://)?(?:open\.)?spotify\.com/(?:intl-[a-zA-Z-]+/)?(playlist|track|album|artist)/([a-zA-Z0-9]+)(?:[?&][^\s]*)?"
        )
        self.uri_regex = re.compile(
            r"spotify:(playlist|track|album|artist):([a-zA-Z0-9]+)"
        )

    def _parse(self, url: str) -> Tuple[Optional[str], Optional[str]]:
        if not url:
            return None, None
        match = self.url_regex.search(url)
        if match:
            return match.group(1), match.group(2)
        match_uri = self.uri_regex.search(url)
        if match_uri:
            return match_uri.group(1), match_uri.group(2)
        return None, None

    def valid(self, url: str) -> bool:
        item_type, item_id = self._parse(url)
        return bool(item_type and item_id)

    def is_playlist(self, url: str) -> bool:
        item_type, _ = self._parse(url)
        return item_type in ("playlist", "album", "artist")
