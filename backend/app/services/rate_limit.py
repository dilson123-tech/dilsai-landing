from __future__ import annotations

from dataclasses import dataclass
from math import ceil
from threading import Lock
from time import monotonic

from fastapi import Request


@dataclass(frozen=True)
class RateLimitResult:
    allowed: bool
    limit: int
    remaining: int
    reset_at: float
    retry_after: int


class InMemoryRateLimiter:
    def __init__(self) -> None:
        self._buckets: dict[tuple[str, str], tuple[int, float]] = {}
        self._lock = Lock()

    def check(
        self,
        identifier: str,
        bucket: str,
        limit: int,
        window_seconds: int,
        now: float | None = None,
    ) -> RateLimitResult:
        current_time = monotonic() if now is None else now
        safe_window = max(1, int(window_seconds))
        safe_limit = int(limit)

        if safe_limit <= 0:
            return RateLimitResult(
                allowed=True,
                limit=safe_limit,
                remaining=0,
                reset_at=current_time + safe_window,
                retry_after=0,
            )

        key = (identifier, bucket)

        with self._lock:
            count, reset_at = self._buckets.get(key, (0, current_time + safe_window))

            if current_time >= reset_at:
                count = 0
                reset_at = current_time + safe_window

            if count >= safe_limit:
                retry_after = max(1, ceil(reset_at - current_time))
                return RateLimitResult(
                    allowed=False,
                    limit=safe_limit,
                    remaining=0,
                    reset_at=reset_at,
                    retry_after=retry_after,
                )

            count += 1
            self._buckets[key] = (count, reset_at)

            return RateLimitResult(
                allowed=True,
                limit=safe_limit,
                remaining=max(0, safe_limit - count),
                reset_at=reset_at,
                retry_after=0,
            )

    def reset(self) -> None:
        with self._lock:
            self._buckets.clear()


def get_client_identifier(request: Request) -> str:
    forwarded_for = request.headers.get("x-forwarded-for", "")
    if forwarded_for:
        first_ip = forwarded_for.split(",", 1)[0].strip()
        if first_ip:
            return first_ip

    if request.client and request.client.host:
        return request.client.host

    return "unknown"
