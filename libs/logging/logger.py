import sys

from loguru import logger


class Logging:
    """Class with setup of all logging levels and formats."""

    prefix = None
    prefix_args = None

    @staticmethod
    def echo(message):
        """Print report message."""
        prefix = ""
        if Logging.prefix is not None:
            prefix = Logging.prefix if Logging.prefix_args is None else Logging.prefix.format(*Logging.prefix_args)
        logger.opt(colors=True).info(prefix + message)

    @staticmethod
    def clear_prefix():
        """Reset output prefix."""
        Logging.prefix = None
        Logging.prefix_args = None

    @staticmethod
    def prepare_to_output(prefix, prefix_args=None):
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
