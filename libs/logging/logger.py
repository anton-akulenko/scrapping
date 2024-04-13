from __future__ import annotations

import sys
from typing import Any, TYPE_CHECKING

from loguru import logger

if TYPE_CHECKING:
    from libs.logging.wrappers import PropertyWrapper


class Logging:
    """Class with setup of all logging levels and formats."""

    prefix: str | None = None
    prefix_args: Any | None = None

    @staticmethod
    def echo(message: str) -> None:
        """Print report message."""
        prefix = ""
        if Logging.prefix is not None:
            prefix = Logging.prefix if Logging.prefix_args is None else Logging.prefix.format(*Logging.prefix_args)
        logger.opt(colors=True).info(prefix + message)

    @staticmethod
    def clear_prefix() -> None:
        """Reset output prefix."""
        Logging.prefix = None
        Logging.prefix_args = None

    @staticmethod
    def prepare_to_output(prefix: str | None = None, prefix_args: tuple[PropertyWrapper] | None = None) -> None:
        """Prepare logger for console output format."""
        logger.remove()
        logger.add(
            sys.stdout,
            format="{message}",
            level="INFO",
            colorize=True,
        )
        Logging.prefix = prefix
        Logging.prefix_args = prefix_args
