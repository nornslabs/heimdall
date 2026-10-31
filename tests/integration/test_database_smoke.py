import os

import asyncpg
import pytest

pytestmark = pytest.mark.integration


async def test_postgres_is_reachable() -> None:
    url = os.environ.get("DATABASE_URL")
    if not url:
        pytest.skip("DATABASE_URL is not set")
    conn = await asyncpg.connect(url)
    try:
        assert await conn.fetchval("SELECT 1") == 1
    finally:
        await conn.close()
