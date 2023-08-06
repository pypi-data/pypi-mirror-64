from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Dict


@dataclass(frozen=True)
class HttpStatus:
    """HTTP status of the response."""
    status_code: int

    @staticmethod
    # pylint: disable=invalid-name
    def ok() -> HttpStatus:
        return HttpStatus(200)

    @staticmethod
    def created() -> HttpStatus:
        return HttpStatus(201)

    @staticmethod
    def accepted() -> HttpStatus:
        return HttpStatus(202)

    @staticmethod
    def not_found() -> HttpStatus:
        return HttpStatus(404)

    @staticmethod
    def internal_server_error() -> HttpStatus:
        return HttpStatus(500)


@dataclass(frozen=True)
class ResponseData:
    """Contains HTTP response."""
    status: HttpStatus
    reason: Optional[str] = None
    content_type: Optional[str] = None
    payload_json: Optional[Dict] = None
