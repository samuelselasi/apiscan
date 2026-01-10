from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Dict, Optional
import base64


class AuthType(str, Enum):
    none = "none"
    bearer = "bearer"
    api_key = "api-key"
    basic = "basic"


@dataclass(frozen=True)
class AuthConfig:
    auth_type: AuthType = AuthType.none

    # bearer/api-key token
    token: Optional[str] = None

    # api-key header name
    api_key_name: str = "X-API-Key"

    # basic auth creds
    username: Optional[str] = None
    password: Optional[str] = None


@dataclass(frozen=True)
class RequestContext:
    headers: Dict[str, str]
    auth: AuthConfig

    def build_headers(self) -> Dict[str, str]:
        """
        Returns merged headers including auth headers.
        Auth is applied as headers by default (safe, non-invasive).
        """
        merged = dict(self.headers or {})

        if self.auth.auth_type == AuthType.none:
            return merged

        if self.auth.auth_type == AuthType.bearer:
            if self.auth.token:
                merged["Authorization"] = f"Bearer {self.auth.token}"
            return merged

        if self.auth.auth_type == AuthType.api_key:
            if self.auth.token:
                merged[self.auth.api_key_name] = self.auth.token
            return merged

        if self.auth.auth_type == AuthType.basic:
            if self.auth.username is not None and self.auth.password is not None:
                raw = f"{self.auth.username}:{self.auth.password}".encode("utf-8")
                merged["Authorization"] = "Basic " + base64.b64encode(raw).decode("ascii")
            return merged

        return merged
