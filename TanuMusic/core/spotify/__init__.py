from typing import List, Optional
from TanuMusic.helpers import Track

from .utils import SpotifyUtils
from .client import SpotifyAuthManager
from .embeds import EmbedScraper
from .search import SpotifySearcher

class Spotify:
    def __init__(self):
        self._utils = SpotifyUtils()
        self._auth = SpotifyAuthManager()
        self._embeds = EmbedScraper()
        self._searcher = SpotifySearcher(self._auth, self._embeds, self._utils)

    def valid(self, url: str) -> bool:
        return self._utils.valid(url)

    def is_playlist(self, url: str) -> bool:
        return self._utils.is_playlist(url)

    async def search(self, url: str, m_id: int) -> Optional[Track]:
        return await self._searcher.search(url, m_id)

    async def playlist(self, limit: int, user: str, url: str, offset: int = 0) -> List[Track]:
        return await self._searcher.playlist(limit, user, url, offset)

    def is_configured(self) -> bool:
        return self._auth.is_configured()
