"""Test Food Review API health router definition."""

from http import HTTPStatus

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_health_route_returns_healthy_string(async_client: AsyncClient):
    """Test `/health` endpoint."""
    response = await async_client.get("/health")
    assert response.status_code == HTTPStatus.OK
