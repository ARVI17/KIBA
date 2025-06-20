import asyncio
import respx
import httpx
from backend.app.hablame_client import HablameClient


def test_send_sms_success():
    client = HablameClient(account="a", apikey="b", token="c")
    bulk = [{"numero": "1", "sms": "hi"}]
    with respx.mock as router:
        route = router.post("https://api103.hablame.co/api/sms/v3/send/marketing/bulk").mock(
            return_value=httpx.Response(200, json_data={"ok": True})
        )
        resp = asyncio.run(client.send_sms(bulk))
        assert resp.status_code == 200
        assert route.called
