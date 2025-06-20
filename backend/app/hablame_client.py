import os
import asyncio
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

    async def _request(self, method: str, url: str, **kwargs) -> httpx.Response:
        """Realiza una petición HTTP con lógica de reintentos."""
        retries_429 = 3
        retries_5xx = 1
        backoff = 1
        while True:
            async with httpx.AsyncClient() as client:
                resp = await client.request(method, url, **kwargs)

            if resp.status_code == 429 and retries_429 > 0:
                await asyncio.sleep(backoff)
                backoff *= 2
                retries_429 -= 1
                continue

            if resp.status_code >= 500 and resp.status_code != 429 and retries_5xx > 0:
                retries_5xx -= 1
                continue

            return resp

    async def ping(self) -> httpx.Response:
        url = f"{self.base_url}/sms/v3/ping"
        return await self._request("GET", url, headers=self._headers())

    async def auth(self) -> httpx.Response:
        url = f"{self.base_url}/sms/v3/authenticate"
        return await self._request("POST", url, headers=self._headers())

    async def send_sms(self, bulk: List[Dict[str, Any]]) -> httpx.Response:
        url = f"{self.base_url}/sms/v3/send/marketing/bulk"
        payload = {
            "flash": "0",
            "sc": "890202",
            "request_dlvr_rcpt": "0",
            "bulk": bulk,
        }
        return await self._request("POST", url, headers=self._headers(), json=payload)

    async def get_sms_status(self, message_id: str) -> httpx.Response:
        url = f"{self.base_url}/sms/v3/status/{message_id}"
        return await self._request("GET", url, headers=self._headers())

    async def get_account_info(self) -> httpx.Response:
        url = f"{self.base_url}/sms/v3/account"
        return await self._request("GET", url, headers=self._headers())

    async def list_countries(self) -> httpx.Response:
        url = f"{self.base_url}/sms/v3/country"
        return await self._request("GET", url, headers=self._headers())

