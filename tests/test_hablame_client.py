import asyncio
import respx
import httpx
from backend.app.hablame_client import HablameClient


def test_send_sms_success():
    client = HablameClient(apikey="b")
    bulk = [{"numero": "1", "sms": "hi"}]
    with respx.mock as router:
        route = router.post("https://api103.hablame.co/api/sms/v3/send/marketing/bulk").mock(
            return_value=httpx.Response(200, json_data={"ok": True})
        )
        resp = asyncio.run(client.send_sms(bulk))
        assert resp.status_code == 200
        assert route.called


def test_get_sms_status():
    client = HablameClient(apikey="b")
    with respx.mock as router:
        route = router.get("https://api103.hablame.co/api/sms/v3/status/123").mock(
            return_value=httpx.Response(200, json_data={"ok": True})
        )
        resp = asyncio.run(client.get_sms_status("123"))
        assert resp.status_code == 200
        assert route.called


def test_get_account_info():
    client = HablameClient(apikey="b")
    with respx.mock as router:
        route = router.get("https://api103.hablame.co/api/sms/v3/account").mock(
            return_value=httpx.Response(200, json_data={"ok": True})
        )
        resp = asyncio.run(client.get_account_info())
        assert resp.status_code == 200
        assert route.called


def test_list_countries():
    client = HablameClient(apikey="b")
    with respx.mock as router:
        route = router.get("https://api103.hablame.co/api/sms/v3/country").mock(
            return_value=httpx.Response(200, json_data={"ok": True})
        )
        resp = asyncio.run(client.list_countries())
        assert resp.status_code == 200
        assert route.called
