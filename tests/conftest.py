"""Test Food Review API common fixtures."""

from pathlib import Path
from unittest.mock import patch

import pandas as pd
from pytest import fixture

from food_review_api.core.config.configuration import Configuration
from food_review_api.products.repository import ProductRepository


@fixture
def mock_reviews():
    return pd.DataFrame(
        {
            "id": [1, 2, 3],
            "product_id": ["product1", "product2", "product1"],
            "user_id": ["user1", "user2", "user1"],
            "profile_name": ["profile1", "profile2", "profile3"],
            "helpfulness_numerator": [1, 2, 3],
            "helpfulness_denominator": [1, 2, 3],
            "score": [1, 2, 3],
            "time": [1, 2, 3],
            "summary": ["summary1", "summary2", "summary3"],
            "text": ["text1", "text2", "text3"],
        }
    )


@fixture(scope="session")
def config_file_local():
    """Return the path to the test configuration file.

    This fixture returns the path to the test configuration file located in the
    same directory as this file. The test configuration file is a YAML file
    containing the configuration for the test environment.

    The test configuration file is used by the test suite to configure the
    application and its dependencies, such as the database connection.

    Returns:
        Path: The path to the test configuration file.
    """
    return Path(__file__).parent / "application-test.yaml"


@fixture(scope="session")
def environment():
    """Return the name of the environment for the test suite.

    This fixture returns the name of the environment for the test suite. The
    environment name is used to configure the application and its dependencies,
    such as the database connection.

    Returns:
        str: The name of the environment for the test suite.
    """
    return "test"


@fixture(scope="session")
def service_name():
    """Return the name of the service for the test suite.

    This fixture returns the name of the service for the test suite. The service
    name is used to configure the application and its dependencies, such as the
    database connection.

    Returns:
        str: The name of the service for the test suite.
    """
    return "test-food-review-api"


@fixture(scope="session", autouse=True)
def setup_configuration(config_file_local: Path, environment: str, service_name: str):
    """Configure the application configuration object for the test suite.

    This fixture patches the application configuration object with the test
    configuration file, environment name, and service name. This ensures that the
    application is configured correctly for the test suite.

    Args:
        config_file_local (Path): The path to the test configuration file.
        environment (str): The name of the environment for the test suite.
        service_name (str): The name of the service for the test suite.

    Yields:
        None
    """
    with (
        patch.object(Configuration, "config_file_local", config_file_local),
        patch.object(Configuration, "environment", environment),
        patch.object(Configuration, "service_name", service_name),
    ):
        yield


@fixture
def config():
    """Return an instance of the application configuration class.

    This fixture returns an instance of the application configuration class. The
    instance is configured with the test configuration file, environment name,
    and service name, which are set up by the setup_configuration fixture.

    Returns:
        Configuration: An instance of the application configuration class.
    """
    return Configuration()


@fixture
def product_repository():
    """
    Returns an instance of the ProductRepository class.

    This fixture returns an instance of the ProductRepository class, which is used
    to store and manage model instances.

    Returns:
        ProductRepository: An instance of the ProductRepository class.
    """
    return ProductRepository()
