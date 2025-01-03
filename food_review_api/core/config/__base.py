"""Food Review API base configuration class definition."""

from abc import ABC
from typing import ClassVar

from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
)

from food_review_api.core.config.__config_service_source import (
    ConfigServiceSettingsSource,
)


class BaseConfiguration(BaseSettings, ABC):
    """Base configuration settings."""

    environment: ClassVar[str]
    service_name: ClassVar[str | None] = None
    config_file_local: ClassVar[str | None] = None

    model_config = SettingsConfigDict(
        env_nested_delimiter="__",
        env_parse_none_str="null",
        extra="ignore",
        nested_model_default_partial_update=True,
    )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        """Define the sources and their order for loading the settings values.

        Args:
        ----
            settings_cls: The Settings class.
            init_settings: The `InitSettingsSource` instance.
            env_settings: The `EnvSettingsSource` instance.
            dotenv_settings: The `DotEnvSettingsSource` instance.
            file_secret_settings: The `SecretsSettingsSource` instance.

        Returns:
        -------
            Tuple of setting sources in order for loading settings values.

        """
        config_service_settings = ConfigServiceSettingsSource(
            settings_cls=settings_cls,
            service_name=cls.service_name,
            environment=cls.environment,
            config_file_local=cls.config_file_local,
        )
        return (
            init_settings,
            env_settings,
            config_service_settings,
            dotenv_settings,
            file_secret_settings,
        )
