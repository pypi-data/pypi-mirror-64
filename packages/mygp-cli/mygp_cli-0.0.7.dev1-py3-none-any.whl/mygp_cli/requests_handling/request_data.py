from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Optional

from mygp_cli.state import Url


class HeadersBuilder:
    def __init__(self, headers=None) -> None:
        super().__init__()
        if headers is None:
            self._headers: Dict[str, str] = {}
        else:
            self._headers = headers.copy()

    def add_auth_bearer(self, token: str) -> HeadersBuilder:
        self._headers["Authorization"] = f"Bearer {token}"
        return HeadersBuilder(self._headers)

    def build(self) -> Dict[str, str]:
        return self._headers.copy()


@dataclass(frozen=True)
class RequestData:
    """Contains the data needed to issue a HTTP request."""

    class Method(Enum):
        POST = 0
        GET = 1

    method: Method
    url: Url
    form_parameters: Dict[str, str] = field(default_factory=dict)
    json: Optional[Dict] = None
    headers: Dict[str, str] = field(default_factory=dict)
