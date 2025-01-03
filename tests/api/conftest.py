"""Test Food Review API common fixtures."""

import pytest_asyncio
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient
from pytest import fixture

from food_review_api.api import build_service_app


@fixture
def app():
    """Return a configured FastAPI app instance.

    Returns:
        fastapi.FastAPI: A configured FastAPI app instance.
    """
    return build_service_app()


@fixture
def client(app):
    """Return a FastAPI TestClient instance.

    Yields:
        fastapi.testclient.TestClient: A TestClient instance bound to the
            application instance.
    """
    client = TestClient(app)
    yield client


@pytest_asyncio.fixture(scope="function")
async def async_client(app):
    """Return an httpx AsyncClient instance.

    Yields:
        httpx.AsyncClient: An AsyncClient instance bound to the application
            instance.
    """
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        yield client
