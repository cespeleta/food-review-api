"""Food Review configuration class definition."""

from logging import getLogger
from os import PathLike
from pathlib import Path
from typing import Any, ClassVar

import yaml
from pydantic_settings import BaseSettings, InitSettingsSource

logger = getLogger(__name__)


class ConfigServiceSettingsSource(InitSettingsSource):
    """Pydantic Settings Source class for loading values from config."""

    DEFAULT_CONFIG_FILE_LOCAL: ClassVar[PathLike] = Path("application-local.yaml")
    LOCAL_ENVIRONMENTS: ClassVar[list[str]] = ["local", "test"]

    def __init__(
        self,
        settings_cls: type[BaseSettings],
        environment: str,
        service_name: str | None = None,
        config_file_local: PathLike | None = None,
    ):
        if config_file_local is None:
            config_file_local = self.DEFAULT_CONFIG_FILE_LOCAL
        super().__init__(settings_cls, init_kwargs={})
        self.service_name = service_name
        self.environment = environment
        self.config_file_local = config_file_local

    def _load_local_config(self, source: str = "application-local.yaml"):
        """Fetch configuration from local yaml.

        Args:
            source (str, optional): Filename of the yaml to read from.
            Defaults to "application-local.yaml".

        Raises:
            ex: If configuration file is not found in the directory.

        Returns:
            dict: Dictionary representing the configuration
        """
        try:
            config = yaml.safe_load(Path(source).read_text())
            logger.debug("local config loaded")
            return config
        except FileNotFoundError as ex:
            logger.error(
                "local config not found, expecting application-local.yaml in root directory"
            )
            raise ex

    def __call__(self) -> dict[str, Any]:
        """Load variables from cloud configurations through the ConfigServer."""
        return self._load_local_config(self.config_file_local)
