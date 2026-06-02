"""Controlled HTTP helper for market source adapter fetches."""

from __future__ import annotations

import json
import socket
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


class SourceTimeoutError(TimeoutError):
    """Raised when the controlled source exceeds the configured timeout."""


@dataclass(frozen=True)
class ControlledHTTPResponse:
    """HTTP response data preserved by the adapter boundary."""

    status_code: int
    payload: Any
    retrieved_at: str
    content_type: str | None = None


def fetch_json(
    endpoint_url: str,
    *,
    timeout_seconds: float = 5.0,
    credential: str | None = None,
) -> ControlledHTTPResponse:
    """Fetch JSON from one controlled endpoint using only the standard library."""

    headers = {"Accept": "application/json"}
    if credential:
        headers["Authorization"] = f"Bearer {credential}"
    request = Request(endpoint_url, headers=headers, method="GET")

    try:
        with urlopen(request, timeout=timeout_seconds) as response:  # noqa: S310 - controlled endpoint only
            body = response.read().decode("utf-8")
            return ControlledHTTPResponse(
                status_code=response.status,
                payload=json.loads(body),
                retrieved_at=_now(),
                content_type=response.headers.get("Content-Type"),
            )
    except HTTPError as exc:
        body = exc.read().decode("utf-8") if exc.fp else ""
        try:
            payload: Any = json.loads(body) if body else None
        except json.JSONDecodeError:
            payload = body
        return ControlledHTTPResponse(
            status_code=exc.code,
            payload=payload,
            retrieved_at=_now(),
            content_type=exc.headers.get("Content-Type") if exc.headers else None,
        )
    except (TimeoutError, socket.timeout) as exc:
        raise SourceTimeoutError("controlled source request timed out") from exc
    except URLError as exc:
        if isinstance(exc.reason, (TimeoutError, socket.timeout)):
            raise SourceTimeoutError("controlled source request timed out") from exc
        raise


def _now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
