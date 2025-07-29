import json
from typing import Any, Optional

class Response:
    def __init__(self, status_code: int = 200, text: str = "", json_data: Any = None):
        self.status_code = status_code
        self.text = text
        self._json = json_data

    def json(self) -> Any:
        if self._json is not None:
            return self._json
        try:
            return json.loads(self.text)
        except Exception:
            return None

class AsyncClient:
    def __init__(self, timeout: Optional[float] = None):
        self.timeout = timeout

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        pass

    async def request(self, method: str, url: str, **kwargs) -> Response:
        raise NotImplementedError("AsyncClient.request must be mocked during tests")

    async def post(self, url: str, **kwargs) -> Response:
        return await self.request("POST", url, **kwargs)

    async def get(self, url: str, **kwargs) -> Response:
        return await self.request("GET", url, **kwargs)

    async def aclose(self):
        pass
