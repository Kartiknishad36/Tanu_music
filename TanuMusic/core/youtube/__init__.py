from typing import Optional, Union
from pyrogram import types
from TanuMusic.helpers import Track

from .utils import YouTubeUtils
from .cookies import CookieManager
from .storage import StorageManager
from .search import Searcher
from .download import Downloader

class YouTube:
    def __init__(self):
        self._utils = YouTubeUtils()
        self._cookies = CookieManager()
        self._storage = StorageManager()
        self._searcher = Searcher(self._cookies)
        self._downloader = Downloader(self._cookies, self._storage, self._searcher)
        self.base = self._utils.base

    def valid(self, url: str) -> bool:
        return self._utils.valid(url)

    def is_direct_stream(self, url: str) -> bool:
        return self._utils.is_direct_stream(url)

    def url(self, message: types.Message) -> Union[str, None]:
        return self._utils.url(message)

    def get_cookies(self):
        return self._cookies.get_cookies()

    async def save_cookies(self, urls: list[str]) -> None:
        await self._cookies.save_cookies(urls)

    async def search(self, query: str, m_id: int, music: bool = False) -> Track | None:
        return await self._searcher.search(query, m_id, music)

    async def playlist(self, limit: int, user: str, url: str) -> list[Track]:
        return await self._searcher.playlist(limit, user, url)

    async def download(self, video_id: str, is_live: bool = False, video: bool = False) -> Optional[str]:
        return await self._downloader.download(video_id, is_live, video)
