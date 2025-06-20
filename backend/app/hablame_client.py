import os
import httpx
from typing import Any, Dict, List


class HablameClient:
    """Pequeño cliente async para la API de Hablame"""

    def __init__(self, apikey: str | None = None, base_url: str = "https://api103.hablame.co/api"):
        self.apikey = apikey or os.getenv("HABLAME_API_KEY")
        self.base_url = base_url.rstrip("/")

    def _headers(self) -> Dict[str, str]:
        return {
            "Content-Type": "application/json",
            "ApiKey": self.apikey or "",
        }

    async def ping(self) -> httpx.Response:
        url = f"{self.base_url}/sms/v3/ping"
        async with httpx.AsyncClient() as client:
            return await client.get(url, headers=self._headers())

    async def auth(self) -> httpx.Response:
        url = f"{self.base_url}/sms/v3/authenticate"
        async with httpx.AsyncClient() as client:
            return await client.post(url, headers=self._headers())

    async def send_sms(self, bulk: List[Dict[str, Any]]) -> httpx.Response:
        url = f"{self.base_url}/sms/v3/send/marketing/bulk"
        payload = {
            "flash": "0",
            "sc": "890202",
            "request_dlvr_rcpt": "0",
            "bulk": bulk,
        }
        async with httpx.AsyncClient() as client:
            return await client.post(url, headers=self._headers(), json=payload)

