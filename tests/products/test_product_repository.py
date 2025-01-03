"""Food Review API models repository class defintion."""

from unittest.mock import MagicMock, patch

import pytest
from pytest import raises

from food_review_api.core.config.database import DatabaseConfig
from food_review_api.products.repository import ProductNotFoundInRepositoryError
from food_review_api.products.schemas.product import Product


def test_product_repository_init(product_repository):
    """
    Verify that the ProductRepository is correctly initialized.

    This test verifies that the ProductRepository is correctly initialized with empty
    model storage, and that the metadata is set to None.
    """
    assert product_repository._products == {}
    assert product_repository._products_metadata is None
    assert product_repository._review_count is None
    assert product_repository._reviews_per_product is None


def test_product_repository_clear(product_repository):
    """
    Verify that clear() method correctly resets repository state.

    This test verifies that the repository is correctly reset after calling clear().
    It creates a repository with a model and some data, and checks that after calling
    clear(), all data is erased.
    """
    product_repository._products = {"model1": MagicMock()}
    product_repository._products_metadata = {"data1": "value1"}
    product_repository.clear()
    assert product_repository._products == {}
    assert product_repository._products_metadata is None


def test_product_repository_raises_error_when_getting_missing_model(product_repository):
    """
    Verify that __getitem__() method raises ProductNotFoundInRepositoryError when model is missing.

    This test verifies that the __getitem__() method raises a ProductNotFoundInRepositoryError
    exception when the model is not found in the repository.
    """
    missing_model_name = "missing model"

    with raises(ProductNotFoundInRepositoryError) as error:
        product_repository[missing_model_name]

    assert missing_model_name in str(error.value)


def test_load_raises_file_not_found_error(product_repository):
    """Verify that load() method raises FileNotFoundError if the CSV file does not exist."""
    with patch(
        "food_review_api.products.repository.ProductRepository._load_reviews_csv"
    ) as mock_load_reviews_csv:
        mock_load_reviews_csv.side_effect = FileNotFoundError
        db = DatabaseConfig(filename="non_existent_file.csv")
        with pytest.raises(FileNotFoundError):
            product_repository.load(db)


def test_load_correctly_loads_products(product_repository, mock_reviews):
    """Verify that load() method correctly loads products from a CSV file."""
    with patch(
        "food_review_api.products.repository.ProductRepository._load_reviews_csv"
    ) as mock_load_reviews_csv:
        mock_load_reviews_csv.return_value = mock_reviews
        db = DatabaseConfig(filename="test_file.csv", version="1")
        product_repository.load(db)
        assert len(product_repository._products) == 2


def test_load_correctly_sets_review_count(product_repository, mock_reviews):
    """Verify that load() method correctly sets the review count."""
    with patch(
        "food_review_api.products.repository.ProductRepository._load_reviews_csv"
    ) as mock_load_reviews_csv:
        mock_load_reviews_csv.return_value = mock_reviews
        db = DatabaseConfig(filename="test_file.csv")
        product_repository.load(db)
        assert product_repository._review_count == 3


def test_load_correctly_sets_reviews_per_product(product_repository, mock_reviews):
    """Verify that load() method correctly sets the reviews per product."""
    with patch(
        "food_review_api.products.repository.ProductRepository._load_reviews_csv"
    ) as mock_load_reviews_csv:
        mock_load_reviews_csv.return_value = mock_reviews
        db = DatabaseConfig(filename="test_file.csv")
        product_repository.load(db)
        assert product_repository._reviews_per_product["product1"] == 2
        assert product_repository._reviews_per_product["product2"] == 1


def test_load_correctly_creates_product_instances(product_repository, mock_reviews):
    """Verify that load() method correctly creates Product instances."""
    with patch(
        "food_review_api.products.repository.ProductRepository._load_reviews_csv"
    ) as mock_load_reviews_csv:
        mock_load_reviews_csv.return_value = mock_reviews
        db = DatabaseConfig(filename="test_file.csv")
        product_repository.load(db)
        assert isinstance(product_repository._products["product1"], Product)
        assert isinstance(product_repository._products["product2"], Product)
        assert len(product_repository._products["product1"].reviews) == 2
        assert len(product_repository._products["product2"].reviews) == 1


def test_load_correctly_sets_products_metadata(product_repository, mock_reviews):
    """Verify that load() method correctly sets the products metadata."""
    with patch(
        "food_review_api.products.repository.ProductRepository._load_reviews_csv"
    ) as mock_load_reviews_csv:
        mock_load_reviews_csv.return_value = mock_reviews
        db = DatabaseConfig(filename="test_file.csv")
        product_repository.load(db)
        assert product_repository._products_metadata == db


def test_product_repository_get(product_repository):
    """Verify that get() method correctly returns a model instance."""
    product_repository._products = {"model1": MagicMock()}
    assert product_repository.get("model1") == product_repository._products["model1"]


def test_product_repository_getitem(product_repository):
    """Verify that __getitem__() method correctly returns a model instance."""
    product_repository._products = {"model1": MagicMock()}
    assert product_repository["model1"] == product_repository._products["model1"]


def test_product_repository_has_product(product_repository):
    """Verify that has_product() method correctly checks if a model is loaded."""
    product_repository._products = {"model1": MagicMock()}
    assert product_repository.has_product("model1")
    assert not product_repository.has_product("model2")
