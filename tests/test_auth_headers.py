import httpx
import pytest

from apiscan.http import HttpClient
from apiscan.auth import RequestContext, AuthConfig, AuthType


@pytest.mark.asyncio
async def test_bearer_token_is_sent(monkeypatch):
    captured = {"auth": None}

    def handler(request: httpx.Request) -> httpx.Response:
        captured["auth"] = request.headers.get("Authorization")
        return httpx.Response(200, json={"ok": True})

    transport = httpx.MockTransport(handler)

    real_async_client = httpx.AsyncClient

    def client_factory(*args, **kwargs):
        kwargs["transport"] = transport
        kwargs["follow_redirects"] = True
        return real_async_client(*args, **kwargs)

    monkeypatch.setattr(httpx, "AsyncClient", client_factory)

    ctx = RequestContext(
        headers={},
        auth=AuthConfig(auth_type=AuthType.bearer, token="abc123"),
    )

    async with HttpClient("https://example.com", context=ctx) as client:
        await client.get("/")

    assert captured["auth"] == "Bearer abc123"


@pytest.mark.asyncio
async def test_custom_header_is_sent(monkeypatch):
    captured = {"xclient": None}

    def handler(request: httpx.Request) -> httpx.Response:
        captured["xclient"] = request.headers.get("X-Client")
        return httpx.Response(200, json={"ok": True})

    transport = httpx.MockTransport(handler)

    real_async_client = httpx.AsyncClient

    def client_factory(*args, **kwargs):
        kwargs["transport"] = transport
        kwargs["follow_redirects"] = True
        return real_async_client(*args, **kwargs)

    monkeypatch.setattr(httpx, "AsyncClient", client_factory)

    ctx = RequestContext(
        headers={"X-Client": "apiscan"},
        auth=AuthConfig(auth_type=AuthType.none),
    )

    async with HttpClient("https://example.com", context=ctx) as client:
        await client.get("/")

    assert captured["xclient"] == "apiscan"
