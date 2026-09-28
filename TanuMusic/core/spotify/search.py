from typing import List, Optional
from TanuMusic.helpers import Track

class SpotifySearcher:
    def __init__(self, auth, embeds, utils):
        self._auth = auth
        self._embeds = embeds
        self._utils = utils

    async def search(self, url: str, m_id: int) -> Optional[Track]:
        return None

    async def playlist(self, limit: int, user: str, url: str, offset: int = 0) -> List[Track]:
        return []
