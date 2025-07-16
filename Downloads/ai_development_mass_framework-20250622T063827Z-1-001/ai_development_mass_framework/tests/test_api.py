import pytest
from httpx import AsyncClient
from main import app

@pytest.mark.asyncio
async def test_health_check():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        resp = await ac.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "healthy"

@pytest.mark.asyncio
async def test_arbitrage_opportunities():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        resp = await ac.get("/api/arbitrage/opportunities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert all("symbol" in o for o in data)

# Add more endpoint tests as needed for public and private APIs
# Example: test authentication, trading, analytics, etc.
