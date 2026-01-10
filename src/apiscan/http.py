from __future__ import annotations

import httpx
from dataclasses import dataclass
from typing import Optional

from apiscan.auth import RequestContext


@dataclass
class HttpClient:
    base_url: str
    timeout: int = 10
    context: Optional[RequestContext] = None

    async def __aenter__(self):
        self._client = httpx.AsyncClient(
            base_url=self.base_url,
            timeout=self.timeout,
            follow_redirects=True,
        )
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self._client.aclose()
        return False

    def _headers(self) -> dict:
        if self.context:
            return self.context.build_headers()
        return {}

    async def get(self, path: str):
        return await self._client.get(path, headers=self._headers())

    async def options(self, path: str):
        return await self._client.options(path, headers=self._headers())
