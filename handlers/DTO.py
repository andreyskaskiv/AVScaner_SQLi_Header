from dataclasses import dataclass
from aiohttp import ClientSession

@dataclass
class UrlHeader:
    url: str
    header: dict
    timeout: int
    session: ClientSession
