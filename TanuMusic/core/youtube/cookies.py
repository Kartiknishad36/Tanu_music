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
            if os.path.exists("TanuMusic/cookies"):
                for file in os.listdir("TanuMusic/cookies"):
                    if file.endswith(".txt"):
                        self.cookies.append(file)
            self.checked = True
        if not self.cookies:
            if not self.warned:
                self.warned = True
                logger.warning("Cookies are missing; downloads might fail.")
            return None
        return f"TanuMusic/cookies/{random.choice(self.cookies)}"

    async def save_cookies(self, urls: list[str]) -> None:
        logger.info("Saving cookies from urls...")
        saved_count = 0
        os.makedirs("TanuMusic/cookies", exist_ok=True)
        for url in urls:
            try:
                path = f"TanuMusic/cookies/cookie{random.randint(10000, 99999)}.txt"
                link = url.replace("me/", "me/raw/")
                async with aiohttp.ClientSession() as session:
                    async with session.get(link) as resp:
                        if resp.status != 200:
                            logger.error(f"Cookie download failed: HTTP {resp.status} from {url}")
                            continue
                        content = await resp.read()
                        if not content or len(content) < 50:
                            logger.error(f"Cookie file empty or invalid from {url}")
                            continue
                        with open(path, "wb") as fw:
                            fw.write(content)
                        if os.path.exists(path) and os.path.getsize(path) > 0:
                            cookie_filename = os.path.basename(path)
                            if cookie_filename not in self.cookies:
                                self.cookies.append(cookie_filename)
                            saved_count += 1
                            logger.info(f"Saved: {cookie_filename}")
            except Exception as e:
                logger.error(f"Cookie save error: {e}")
        if saved_count == 0:
            logger.error("No cookies saved! Check COOKIE_URL. YouTube downloads may fail.")
        else:
            logger.info(f"Cookies ready: {saved_count} file(s)")
