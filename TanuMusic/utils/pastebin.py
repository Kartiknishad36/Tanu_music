import socket
from asyncio import get_running_loop
from functools import partial

import aiohttp


def _netcat(host, port, content):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    s.sendall(content.encode())
    s.shutdown(socket.SHUT_WR)
    while True:
        data = s.recv(4096).decode("utf-8").strip("\n\x00")
        if not data:
            break
        return data
    s.close()


async def paste(content):
    loop = get_running_loop()
    link = await loop.run_in_executor(None, partial(_netcat, "ezup.dev", 9999, content))
    return link


async def pastebin(content: str):
    async with aiohttp.ClientSession() as session:
        async with session.post(
            "https://hastebin.com/documents", data=content.encode()
        ) as resp:
            if resp.status != 200:
                return await paste(content)
            data = await resp.json()
            return f"https://hastebin.com/{data['key']}"
