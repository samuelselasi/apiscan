import json
import httpx
import pytest


def make_transport(routes):
    """
    routes: dict of ("METHOD", "https://host/path") -> httpx.Response
    """
    def handler(request: httpx.Request) -> httpx.Response:
        key = (request.method.upper(), str(request.url))
        if key in routes:
            return routes[key]
        return httpx.Response(404, json={"detail": "not found"})

    return httpx.MockTransport(handler)


@pytest.fixture
def base_url():
    return "https://example.com"


@pytest.fixture
def sample_openapi_spec():
    return {
        "openapi": "3.0.0",
        "info": {"title": "Demo API", "version": "1.0"},
        "paths": {
            "/": {"get": {}},
            "/health": {"get": {}},
            "/users": {"get": {}, "post": {}},
        },
    }
