import os
import random
import aiohttp
from TanuMusic import logger


class CookieManager:
    def __init__(self):
        self.cookies = []
        self.checked = False
        self.warned = False

    def get_cookies(self):
        if not self.checked:
            path = "TanuMusic/cookies"
            if os.path.isdir(path):
                for file in os.listdir(path):
                    if file.endswith(".txt") and file.lower() not in ("readme.txt",):
                        full = os.path.join(path, file)
                        if os.path.getsize(full) > 50:
                            self.cookies.append(file)
            self.checked = True
        if not self.cookies:
            if not self.warned:
                self.warned = True
                logger.warning("Cookies missing — search may still work; downloads may fail.")
            return None
        chosen = random.choice(self.cookies)
        full = f"TanuMusic/cookies/{chosen}"
        if not os.path.exists(full):
            return None
        return full

    def _to_raw(self, url: str) -> str:
        u = url.strip()
        if "pastebin.com/" in u and "/raw/" not in u:
            # https://pastebin.com/XXXX -> https://pastebin.com/raw/XXXX
            parts = u.rstrip("/").split("/")
            code = parts[-1]
            return f"https://pastebin.com/raw/{code}"
        if "paste.ee/" in u and "/r/" in u and "/raw/" not in u:
            return u.replace("/r/", "/p/") if False else u  # paste.ee raw is often same
        if "batbin.me/" in u and "/raw" not in u:
            return u.rstrip("/") + "/raw"
        return u

    async def save_cookies(self, urls) -> None:
        if isinstance(urls, str):
            urls = [urls]
        if not urls:
            return
        logger.info("Saving cookies from urls...")
        saved = 0
        os.makedirs("TanuMusic/cookies", exist_ok=True)
        for url in urls:
            if not url:
                continue
            try:
                link = self._to_raw(url)
                path = f"TanuMusic/cookies/cookie{random.randint(10000, 99999)}.txt"
                async with aiohttp.ClientSession() as session:
                    async with session.get(link, timeout=aiohttp.ClientTimeout(total=30)) as resp:
                        if resp.status != 200:
                            logger.error(f"Cookie HTTP {resp.status} from {link}")
                            continue
                        content = await resp.read()
                        if not content or len(content) < 50:
                            logger.error(f"Cookie empty from {link}")
                            continue
                        # Basic netscape check
                        text = content.decode("utf-8", errors="ignore")
                        if "youtube.com" not in text and ".youtube.com" not in text:
                            logger.warning("Cookie file has no youtube.com entries — may not help")
                        with open(path, "wb") as fw:
                            fw.write(content)
                        name = os.path.basename(path)
                        if name not in self.cookies:
                            self.cookies.append(name)
                        saved += 1
                        logger.info(f"Saved cookie: {name}")
            except Exception as e:
                logger.error(f"Cookie save error: {e}")
        self.checked = True
        if saved == 0:
            logger.error("No cookies saved. Check COOKIE_URL is a raw paste link.")
        else:
            logger.info(f"Cookies ready: {saved} file(s)")
