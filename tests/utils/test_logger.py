"""Test Food Review API Logging utility module."""

from unittest.mock import patch

from food_review_api.core.config import Configuration
from food_review_api.utils import logging
from food_review_api.utils.logging import configure_logging


def test_configure_logging_sets_default_logging_configuration(config: Configuration):
    """
    Verify that configure_logging sets the default logging configuration.

    Given a configuration and a logging configuration, when calling configure_logging
    with the logging configuration, it should set the default logging configuration.

    Args:
        config: A configuration object.
    """
    expected = config.logging.model_dump(exclude_none=True)

    with patch.object(logging, "dictConfig") as mock_dict_config:
        configure_logging(logging_config=config.logging)

    mock_dict_config.assert_called_once_with(expected)
