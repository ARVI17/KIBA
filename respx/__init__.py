from contextlib import ContextDecorator
import httpx

class Route:
    def __init__(self, method: str, url: str):
        self.method = method.upper()
        self.url = url
        self.return_value = None
        self.called = False

    def mock(self, *, return_value: httpx.Response):
        self.return_value = return_value
        return self

class Mocker(ContextDecorator):
    def __init__(self):
        self.routes = []

    def __enter__(self):
        self._orig_request = httpx.AsyncClient.request

        async def _request(self_client, method: str, url: str, **kwargs):
            for r in self.routes:
                if r.method == method.upper() and r.url == url:
                    r.called = True
                    return r.return_value
            raise AssertionError(f"Unexpected request {method} {url}")

        httpx.AsyncClient.request = _request
        return self

    def __exit__(self, exc_type, exc, tb):
        httpx.AsyncClient.request = self._orig_request
        self.routes.clear()

    def post(self, url: str) -> Route:
        route = Route("POST", url)
        self.routes.append(route)
        return route

    def get(self, url: str) -> Route:
        route = Route("GET", url)
        self.routes.append(route)
        return route

mock = Mocker()
