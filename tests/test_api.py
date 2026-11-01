import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.mark.asyncio
async def test_root_endpoint():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "online"


@pytest.mark.asyncio
async def test_health_endpoint():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "daily_reminder" in data


@pytest.mark.asyncio
async def test_webhook_telegram_endpoint():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        sample_payload = {
            "update_id": 10000,
            "message": {
                "message_id": 1,
                "from": {
                    "id": 12345678,
                    "is_bot": False,
                    "first_name": "Santhil",
                },
                "chat": {
                    "id": 12345678,
                    "first_name": "Santhil",
                    "type": "private",
                },
                "date": 1730000000,
                "text": "Hello bot!",
            },
        }
        response = await client.post("/webhook/telegram", json=sample_payload)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert data["received"] is True


@pytest.mark.asyncio
async def test_manual_reminder_endpoint_unconfigured():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/test-reminder")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "triggered"
        assert data["telegram_response"]["ok"] is False
