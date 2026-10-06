from app.services.rate_limit import InMemoryRateLimiter


def test_rate_limiter_blocks_after_limit_and_resets_after_window():
    limiter = InMemoryRateLimiter()

    first = limiter.check(
        identifier="127.0.0.1",
        bucket="chat",
        limit=2,
        window_seconds=60,
        now=100.0,
    )
    second = limiter.check(
        identifier="127.0.0.1",
        bucket="chat",
        limit=2,
        window_seconds=60,
        now=101.0,
    )
    blocked = limiter.check(
        identifier="127.0.0.1",
        bucket="chat",
        limit=2,
        window_seconds=60,
        now=102.0,
    )
    after_reset = limiter.check(
        identifier="127.0.0.1",
        bucket="chat",
        limit=2,
        window_seconds=60,
        now=161.0,
    )

    assert first.allowed is True
    assert first.remaining == 1
    assert second.allowed is True
    assert second.remaining == 0
    assert blocked.allowed is False
    assert blocked.retry_after == 58
    assert after_reset.allowed is True
    assert after_reset.remaining == 1


def test_rate_limiter_separates_buckets_and_identifiers():
    limiter = InMemoryRateLimiter()

    assert limiter.check("user-a", "chat", 1, 60, now=10.0).allowed is True
    assert limiter.check("user-a", "chat", 1, 60, now=11.0).allowed is False

    assert limiter.check("user-a", "materials", 1, 60, now=12.0).allowed is True
    assert limiter.check("user-b", "chat", 1, 60, now=13.0).allowed is True


def test_material_endpoint_rate_limit_returns_429_for_expensive_route():
    from fastapi.testclient import TestClient

    from app.main import app, rate_limiter, settings

    old_enabled = settings.rate_limit_enabled
    old_material_limit = settings.rate_limit_material_per_minute
    old_window = settings.rate_limit_window_seconds

    try:
        settings.rate_limit_enabled = True
        settings.rate_limit_material_per_minute = 1
        settings.rate_limit_window_seconds = 60
        rate_limiter.reset()

        client = TestClient(app)

        first = client.post(
            "/api/v1/materials/extract-text",
            content=b"not-a-supported-file",
            headers={"Content-Type": "application/octet-stream"},
        )
        second = client.post(
            "/api/v1/materials/extract-text",
            content=b"not-a-supported-file",
            headers={"Content-Type": "application/octet-stream"},
        )

        assert first.status_code == 415
        assert second.status_code == 429
        assert second.headers["Retry-After"]
        assert second.json()["rate_limit"]["bucket"] == "materials"

    finally:
        settings.rate_limit_enabled = old_enabled
        settings.rate_limit_material_per_minute = old_material_limit
        settings.rate_limit_window_seconds = old_window
        rate_limiter.reset()
