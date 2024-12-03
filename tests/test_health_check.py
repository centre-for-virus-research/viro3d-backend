from fastapi import Response
from httpx import ASGITransport, AsyncClient
import pytest
from app.main import app

@pytest.mark.asyncio
async def test_health_check():

    async_client = AsyncClient(transport=ASGITransport(app=app), base_url="http://test")
    response: Response = await async_client.get(
        url=f"/health_check/"
    )
    
    assert response.status_code == 200