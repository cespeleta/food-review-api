"""Food Review API logging configuration class definition."""

from typing import Annotated

from pydantic import AfterValidator, BaseModel


def remove_level_from_handler_config(handlers: dict[str, dict] | None):
    """Validator to remove level field from handlers configuration dict."""
    if handlers is None:
        return handlers
    return {
        handler: {
            handler_config_key: handler_config_value
            for handler_config_key, handler_config_value in handler_config.items()
            if handler_config_key != "level"
        }
        for handler, handler_config in handlers.items()
    }


class LoggingConfig(BaseModel):
    """Logging configuration model, to be used through logging.config.dictConfig."""

    version: int = 1
    disable_existing_loggers: bool = False
    incremental: bool = False
    formatters: dict[str, dict] | None = None
    filters: dict[str, dict] | None = None
    handlers: Annotated[
        dict[str, dict] | None, AfterValidator(remove_level_from_handler_config)
    ] = None
    loggers: dict[str, dict] | None = None
    root: dict | None = None
