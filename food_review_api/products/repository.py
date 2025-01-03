"""Food Review API products repository class definition."""

import pandas as pd

from food_review_api.core.config.database import DatabaseConfig
from food_review_api.products.schemas import Product, Review


class ProductNotFoundInRepositoryError(KeyError):
    """Exception thrown when trying to get a missing product from the repository."""


class ProductRepository:
    """product repository class.

    This class is meant to hold the loaded products from the product registry, and
    provide a common interface to manage products.
    """

    def __init__(self) -> None:
        """Initialize product repository with empty product storage."""
        self.clear()

    @property
    def available_products(self) -> int:
        """Get available products identifiers."""
        return list(self._products.keys())

    @property
    def product_count(self) -> int:
        """Get product count."""
        return len(self._products)

    @property
    def review_count(self) -> int:
        """Get reviews count."""
        return self._review_count

    def clear(self) -> None:
        """Clear repository product storage."""
        self._products: dict[str, Product] = {}
        self._products_metadata: DatabaseConfig | None = None
        self._review_count: int | None = None
        self._reviews_per_product: pd.DataFrame | None = None

    def load(self, db: DatabaseConfig) -> None:
        """Load products from a CSV file into the repository.

        This method loads the CSV file, and then processes the loaded data to extract
        the product IDs and their associated reviews. The reviews are then grouped by
        product ID and used to create `Product` instances which are stored in the
        repository.

        Args:
            db: The configuration for the database containing the CSV file.

        Raises:
            FileNotFoundError: If the specified file does not exist.
        """
        reviews = self._load_reviews_csv(db.filename)
        self._review_count = reviews.shape[0]
        self._reviews_per_product = reviews.value_counts("product_id")
        grouped_reviews = self._group_reviews_by_product(reviews)

        # Create product instances
        self._products = {
            product_id: Product(
                product_id=product_id,
                reviews=[Review(**review) for review in reviews],
                number_of_reviews=len(reviews),
            )
            for product_id, reviews in grouped_reviews.items()
        }
        self._products_metadata = db

    def most_commented_products(self, n: int = 3) -> pd.Series:
        """Get products with most reviews."""
        if not self._products:
            raise RuntimeError("Products not loaded")

        return self._reviews_per_product.nlargest(n, keep="all")

    def least_commented_products(self, n: int = 3) -> pd.Series:
        """Get products with lowest reviews."""
        if not self._products:
            raise RuntimeError("Products not loaded")

        return self._reviews_per_product.nsmallest(n, keep="all")

    def _load_reviews_csv(self, filename: str) -> pd.DataFrame:
        """Load the reviews CSV file into a pandas DataFrame.

        Args:
            filename: The path to the CSV file.

        Returns:
            A pandas DataFrame containing the loaded data.
        """
        dtypes = {
            "id": pd.Int64Dtype(),
            "product_id": pd.StringDtype(),
            "user_id": pd.StringDtype(),
            "profile_name": pd.StringDtype(),
            "helpfulness_numerator": pd.Int8Dtype(),
            "helpfulness_denominator": pd.Int8Dtype(),
            "score": pd.Int8Dtype(),
            "time": pd.Int64Dtype(),
            "summary": pd.StringDtype(),
            "text": pd.StringDtype(),
        }
        reviews = pd.read_csv(
            filename,
            header=0,
            names=dtypes.keys(),
            dtype=dtypes,
            nrows=100,
        )
        return reviews

    def _group_reviews_by_product(self, reviews: pd.DataFrame) -> dict[str, list]:
        """Group reviews by product.

        Args:
            reviews (pd.DataFrame): The DataFrame containing the reviews.

        Returns:
            dict[str, list]: A dictionary where the keys are the product IDs and
            the values are the grouped reviews.
        """
        return (
            reviews.groupby("product_id")
            .apply(lambda x: x.to_dict(orient="records"))
            .to_dict()
        )

    def get(self, name: str) -> Product:
        """Get loaded product instance by name."""
        try:
            return self._products[name]
        except KeyError:
            raise ProductNotFoundInRepositoryError(name)

    def __getitem__(self, key: str) -> Product:
        """Wrapper on get loaded product to support self[key] accessor."""
        return self.get(key)

    def has_product(self, name: str) -> bool:
        """Check if a product is loaded by product name."""
        return name in self._products


product_repository = ProductRepository()
