"""Test Food Review API lifespan function definition."""

from unittest.mock import patch

import pytest
from pytest import fixture

from food_review_api.api import lifespan as lifespan_module


@fixture(autouse=True)
def mock_startup_event():
    """Mock the startup_event function of the lifespan module.

    Yields:
        unittest.mock.MagicMock: A mock object for the startup_event function.
    """
    with patch.object(lifespan_module, "startup_event") as _mock:
        yield _mock


@fixture(autouse=True)
def mock_shutdown_event():
    """Mock the shutdown_event function of the lifespan module.

    Yields:
        unittest.mock.MagicMock: A mock object for the shutdown_event function.
    """
    with patch.object(lifespan_module, "shutdown_event") as _mock:
        yield _mock


@pytest.mark.asyncio
async def test_lifespan_startup_event_called(app):
    """
    Verify that the startup_event function is called once when the API application is
    started.
    """
    with patch("food_review_api.api.lifespan.startup_event") as mock_startup_event:
        async with lifespan_module.lifespan(app):
            pass
        mock_startup_event.assert_called_once()


@pytest.mark.asyncio
async def test_lifespan_shutdown_event_called(app, mock_shutdown_event):
    """
    Verify that the shutdown_event function is called once when the API application is
    shut down (i.e., when the TestClient is torn down).
    """
    with patch("food_review_api.api.lifespan.shutdown_event") as mock_shutdown_event:
        async with lifespan_module.lifespan(app):
            pass
        mock_shutdown_event.assert_called_once()
